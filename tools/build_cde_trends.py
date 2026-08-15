#!/usr/bin/env python3
"""CDE 可视化页 static page builder (zh-only).

Zero-dependency (Python 3 stdlib only) build script:
  source data:  cde_data.py（平台信息统计官方口径）+ cde_indications.py（检索归类）
generates:
  website/cde-trials.html   (static page, committed to git)

Run: cd website && python3 tools/build_cde_trends.py

图表约定（dataviz 方法）：
- 内联 SVG，颜色走 .viz-root CSS 变量（浅色为站内品牌色 azure/brand/teal，
  经 validate_palette.js 校验通过；深色步进仅随 data-theme="dark" 生效）
- 悬浮 tooltip 为 JS 叠加层；命中区域大于标记本身
- 数据即口径：官方统计原样呈现；适应症归类标注「编者整理」
"""

import json
from pathlib import Path

import sitegen
from cde_data import AS_OF, DRUG_TYPE, SCOPE, TOTAL, YEARLY

ROOT = Path(__file__).resolve().parent.parent  # website/

try:
    from cde_indications import BE_COUNT, INDICATION_RANKING, TRIALS_CRAWLED
except ImportError:
    INDICATION_RANKING, BE_COUNT, TRIALS_CRAWLED = [], 0, 0


# ---------- helpers ----------

def fmt(n):
    return f"{n:,}"


def pct(v, total):
    return f"{v / total * 100:.1f}%"


# ---------- SVG chart builders ----------

def trend_svg():
    years = [y for y, _ in YEARLY]
    values = [v for _, v in YEARLY]
    n = len(years)
    x0, x1, y0, y1 = 64, 936, 24, 336
    ymax = 5600
    step = (x1 - x0) / (n - 1)

    def X(i):
        return x0 + i * step

    def Y(v):
        return y1 - (v / ymax) * (y1 - y0)

    parts = []
    # gridlines + y ticks
    for t in range(0, 6000, 1000):
        y = Y(t)
        parts.append(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" class="viz-grid"/>')
        parts.append(f'<text x="{x0 - 8}" y="{y + 4:.1f}" class="viz-tick" text-anchor="end">{t:,}</text>')
    # x ticks (every other year + 2026)
    for i, y in enumerate(years):
        if i % 2 == 0 or y == "2026":
            parts.append(f'<text x="{X(i):.1f}" y="{y1 + 22}" class="viz-tick" text-anchor="middle">{y}</text>')
    # line: solid 2013-2025, dashed to 2026
    solid_pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(values[:-1]))
    parts.append(f'<polyline points="{solid_pts}" class="viz-line"/>')
    i_last = n - 1
    parts.append(f'<line x1="{X(i_last - 1):.1f}" y1="{Y(values[-2]):.1f}" '
                 f'x2="{X(i_last):.1f}" y2="{Y(values[-1]):.1f}" class="viz-line viz-line-dashed"/>')
    # markers
    for i, v in enumerate(values[:-1]):
        parts.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="4" class="viz-marker"/>')
    parts.append(f'<circle cx="{X(i_last):.1f}" cy="{Y(values[-1]):.1f}" r="4" class="viz-marker viz-marker-open"/>')
    # direct labels: 2025 peak + 2026 partial
    i_peak = values.index(max(values))
    parts.append(f'<text x="{X(i_peak):.1f}" y="{Y(values[i_peak]) - 12:.1f}" '
                 f'class="viz-label" text-anchor="middle">{values[i_peak]:,}</text>')
    parts.append(f'<text x="{X(i_last):.1f}" y="{Y(values[-1]) + 22:.1f}" '
                 f'class="viz-note" text-anchor="middle">{values[-1]:,}</text>')
    # annotation: 722 dip
    i_dip = 2  # 2015
    parts.append(f'<text x="{X(i_dip + 0.5):.1f}" y="{Y(1300):.1f}" class="viz-note">'
                 f'2015-2016 回落：722 自查核查</text>')
    # hit areas (per year)
    for i in range(n):
        parts.append(f'<rect x="{X(i) - step / 2:.1f}" y="{y0}" width="{step:.1f}" '
                     f'height="{y1 - y0}" class="viz-hit" data-t="trend" data-i="{i}"/>')
    return ('<svg viewBox="0 0 960 372" class="viz-svg" data-trend="1" role="img" '
            'aria-label="2013 至 2026 年平台登记公示试验数量折线图">\n'
            + "\n".join(f"  {p}" for p in parts) + "\n</svg>")


def stacked_bar_svg(data):
    """Horizontal 100% stacked bar for a part-to-whole of 3 categories."""
    total = sum(v for _, v in data)
    bar_w, bar_h, x, y = 780, 48, 150, 24
    parts = []
    cx = x
    seg_colors = ["viz-s1", "viz-s2", "viz-s3"]
    seg_inks = ["viz-s1-ink", "viz-s2-ink", "viz-s3-ink"]
    for i, (name, v) in enumerate(data):
        w = bar_w * v / total
        gap = 2 if i < len(data) - 1 else 0
        parts.append(f'<rect x="{cx:.1f}" y="{y}" width="{max(w - gap, 1):.1f}" height="{bar_h}" '
                     f'class="viz-seg {seg_colors[i]}" data-t="stack" data-i="{i}"/>')
        label = f"{name} {fmt(v)} · {pct(v, total)}"
        fits = w > 6.5 * len(label) + 40
        if fits:
            parts.append(f'<text x="{cx + w / 2:.1f}" y="{y + bar_h / 2 + 4:.1f}" '
                         f'class="viz-seg-label {seg_inks[i]}" text-anchor="middle">{label}</text>')
        cx += w
    # external label for segments that didn't fit
    cx = x
    for i, (name, v) in enumerate(data):
        w = bar_w * v / total
        label = f"{name} {fmt(v)} · {pct(v, total)}"
        if w <= 6.5 * len(label) + 40:
            parts.append(f'<text x="{cx + w + 10:.1f}" y="{y + bar_h / 2 + 4:.1f}" class="viz-seg-label-ext">{label}</text>')
        cx += w
    return ('<svg viewBox="0 0 960 96" class="viz-svg" role="img" aria-label="药物类别分布堆叠条形图">\n'
            + "\n".join(f"  {p}" for p in parts) + "\n</svg>")


def scope_bars_svg(data):
    """Horizontal bar list for magnitude comparison (single measure)."""
    total = sum(v for _, v in data)
    maxv = max(v for _, v in data)
    label_w, x, y0, row_h, gap = 150, 150, 16, 34, 14
    bar_max = 640
    parts = []
    for i, (name, v) in enumerate(data):
        y = y0 + i * (row_h + gap)
        parts.append(f'<text x="{label_w - 14}" y="{y + 16}" class="viz-tick" text-anchor="end">{name}</text>')
        w = max(bar_max * v / maxv, 2)
        parts.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="22" rx="4" '
                     f'class="viz-bar" data-t="scope" data-i="{i}"/>')
        parts.append(f'<text x="{x + w + 10:.1f}" y="{y + 16}" class="viz-label">{fmt(v)} · {pct(v, total)}</text>')
    h = y0 + len(data) * (row_h + gap) - gap + 6
    return (f'<svg viewBox="0 0 960 {h}" class="viz-svg" role="img" aria-label="试验范围条形图">\n'
            + "\n".join(f"  {p}" for p in parts) + "\n</svg>")


def ranking_svg(ranking, topn=20):
    """Indication ranking; emphasis: top category in series hue, rest de-emphasized."""
    data = ranking[:topn]
    maxv = max(v for _, v in data)
    label_w, x, y0, row_h, gap = 150, 150, 14, 30, 10
    bar_max = 640
    parts = []
    for i, (name, v) in enumerate(data):
        y = y0 + i * (row_h + gap)
        cls = "viz-bar" if i == 0 else "viz-bar viz-bar-gray"
        parts.append(f'<text x="{label_w - 14}" y="{y + 16}" class="viz-tick" text-anchor="end">{name}</text>')
        w = max(bar_max * v / maxv, 2)
        parts.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="20" rx="4" '
                     f'class="{cls}" data-t="rank" data-i="{i}" data-idx="rank-{i}"/>')
        parts.append(f'<text x="{x + w + 10:.1f}" y="{y + 15}" class="viz-label">{fmt(v)}</text>')
    h = y0 + len(data) * (row_h + gap) - gap + 6
    return (f'<svg viewBox="0 0 960 {h}" class="viz-svg viz-ranking" role="img" aria-label="适应症排名条形图">\n'
            + "\n".join(f"  {p}" for p in parts) + "\n</svg>")


# ---------- page JS ----------

PAGE_JS = """<script>
    var CDE_DATA = JSON.parse(document.getElementById('cde-data').textContent);
    var TIP = document.getElementById('viz-tooltip');

    function showTip(html, x, y) {
      TIP.innerHTML = html;
      TIP.style.display = 'block';
      var root = TIP.parentElement.getBoundingClientRect();
      TIP.style.left = Math.min(x + 14, root.width - TIP.offsetWidth - 12) + 'px';
      TIP.style.top = Math.max(y - TIP.offsetHeight - 12, 4) + 'px';
    }
    function hideTip() { TIP.style.display = 'none'; }

    function bindSvgHover(svg) {
      svg.addEventListener('mousemove', function (e) {
        var el = e.target;
        if (!el || !el.dataset || !el.dataset.t) return;
        var i = parseInt(el.dataset.i, 10);
        var svgPos = svg.getBoundingClientRect();
        var rootPos = TIP.parentElement.getBoundingClientRect();
        var x = e.clientX - svgPos.left, y = e.clientY - svgPos.top;
        var left = svgPos.left - rootPos.left + x;
        var top = svgPos.top - rootPos.top + y;
        var t = el.dataset.t, html = '';
        if (t === 'trend') {
          var d = CDE_DATA.yearly[i];
          html = '<strong>' + d[0] + ' 年</strong><br>' + d[1].toLocaleString() + ' 项' +
                 (d[0] === '2026' ? '<br><span class="viz-tip-note">截至 2026-08-15（未完年）</span>' : '');
          highlightTrend(svg, i);
        } else if (t === 'stack') {
          var seg = CDE_DATA.drug_type[i];
          html = '<strong>' + seg[0] + '</strong><br>' + seg[1].toLocaleString() + ' 项 · ' + seg[2];
        } else if (t === 'scope') {
          var s = CDE_DATA.scope[i];
          html = '<strong>' + s[0] + '</strong><br>' + s[1].toLocaleString() + ' 项 · ' + s[2];
        } else if (t === 'rank') {
          var rk = CDE_DATA.ranking[i];
          html = '<strong>' + rk[0] + '</strong><br>' + rk[1].toLocaleString() + ' 项';
        }
        showTip(html, left, top);
      });
      svg.addEventListener('mouseleave', function () {
        hideTip();
        if (svg.dataset.trend) clearTrendHighlight(svg);
      });
    }

    function highlightTrend(svg, i) {
      clearTrendHighlight(svg);
      var hit = svg.querySelector('.viz-hit[data-i="' + i + '"]');
      if (!hit) return;
      var x = hit.getAttribute('x');
      var hl = document.createElementNS('http://www.w3.org/2000/svg', 'line');
      hl.setAttribute('x1', x); hl.setAttribute('x2', x);
      hl.setAttribute('y1', '24'); hl.setAttribute('y2', '336');
      hl.setAttribute('class', 'viz-crosshair');
      svg.appendChild(hl);
    }
    function clearTrendHighlight(svg) {
      svg.querySelectorAll('.viz-crosshair').forEach(function (l) { l.remove(); });
    }

    function renderRanking(topn) {
      var svg = document.getElementById('viz-ranking');
      if (!svg) return;
      var data = CDE_DATA.ranking.slice(0, topn);
      var labelW = 150, x = 150, y0 = 14, rowH = 30, gap = 10, barMax = 640;
      var maxv = data.length ? data[0][1] : 1;
      var html = [];
      data.forEach(function (r, i) {
        var y = y0 + i * (rowH + gap);
        var w = Math.max(barMax * r[1] / maxv, 2);
        var cls = i === 0 ? 'viz-bar' : 'viz-bar viz-bar-gray';
        html.push('<text x="' + (labelW - 14) + '" y="' + (y + 16) + '" class="viz-tick" text-anchor="end">' + esc(r[0]) + '</text>');
        html.push('<rect x="' + x + '" y="' + y + '" width="' + w.toFixed(1) + '" height="20" rx="4" class="' + cls +
                  '" data-t="rank" data-i="' + i + '"></rect>');
        html.push('<text x="' + (x + w + 10) + '" y="' + (y + 15) + '" class="viz-label">' + r[1].toLocaleString() + '</text>');
      });
      var h = y0 + data.length * (rowH + gap) - gap + 6;
      svg.setAttribute('viewBox', '0 0 960 ' + h);
      svg.innerHTML = html.join('');
    }

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    document.addEventListener('DOMContentLoaded', function () {
      document.querySelectorAll('.viz-svg').forEach(bindSvgHover);
      var toggle = document.getElementById('rank-toggle');
      if (toggle) {
        toggle.addEventListener('change', function () { renderRanking(parseInt(toggle.value, 10)); });
      }
    });
  </script>"""

EXTRA_STYLE = """
    .viz-root {
      --viz-surface: #ffffff;
      --viz-ink: #101828;
      --viz-ink-2: #475569;
      --viz-muted: #94a3b8;
      --viz-grid: #eef1f6;
      --viz-axis: #e6eaf0;
      --viz-s1: #0b63ce;
      --viz-s2: #f58220;
      --viz-s3: #0d9488;
      --viz-gray: #94a3b8;
      --viz-s1-ink: #ffffff;
      --viz-s2-ink: #060b18;
      --viz-s3-ink: #ffffff;
    }
    :root[data-theme="dark"] .viz-root {
      --viz-surface: #1a1a19;
      --viz-ink: #ffffff;
      --viz-ink-2: #c3c2b7;
      --viz-muted: #898781;
      --viz-grid: #2c2c2a;
      --viz-axis: #383835;
      --viz-s1: #3987e5;
      --viz-s2: #d95926;
      --viz-s3: #199e70;
      --viz-gray: #898781;
      --viz-s1-ink: #0b0b0b;
      --viz-s2-ink: #0b0b0b;
      --viz-s3-ink: #0b0b0b;
    }
    .viz-root { position: relative; }
    .viz-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 0.9rem; margin: 1.6rem 0 0.6rem; }
    .viz-kpi { border: 1px solid var(--border, #d8dde4); border-radius: 10px; padding: 1rem 1.1rem; background: var(--bg-soft, #f6f8fa); }
    .viz-kpi-value { font-size: 1.6rem; font-weight: 700; font-variant-numeric: tabular-nums; line-height: 1.2; }
    .viz-kpi-caption { font-size: 0.8rem; opacity: 0.68; margin-top: 0.3rem; line-height: 1.5; }
    @media (max-width: 720px) { .viz-kpis { grid-template-columns: repeat(2, 1fr); } }
    .viz-chart { margin: 0.6rem 0 2rem; }
    .viz-chart h3 { margin: 0 0 0.3rem; font-size: 1.05rem; }
    .viz-chart-sub { font-size: 0.84rem; opacity: 0.68; margin: 0 0 0.8rem; line-height: 1.6; }
    .viz-svg { width: 100%; height: auto; display: block; }
    .viz-grid { stroke: var(--viz-grid); stroke-width: 1; }
    .viz-tick { fill: var(--viz-muted); font-size: 12px; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-variant-numeric: tabular-nums; }
    .viz-line { fill: none; stroke: var(--viz-s1); stroke-width: 2; }
    .viz-line-dashed { stroke-dasharray: 5 4; }
    .viz-marker { fill: var(--viz-s1); stroke: var(--viz-surface); stroke-width: 1.5; }
    .viz-marker-open { fill: var(--viz-surface); stroke: var(--viz-s1); stroke-width: 2; }
    .viz-label { fill: var(--viz-ink); font-size: 13px; font-weight: 600; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-variant-numeric: tabular-nums; }
    .viz-note { fill: var(--viz-ink-2); font-size: 11.5px; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
    .viz-seg { stroke: var(--viz-surface); stroke-width: 2; }
    .viz-seg-label { font-size: 12.5px; font-weight: 600; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; font-variant-numeric: tabular-nums; }
    .viz-seg-label.viz-s1-ink { fill: var(--viz-s1-ink); }
    .viz-seg-label.viz-s2-ink { fill: var(--viz-s2-ink); }
    .viz-seg-label.viz-s3-ink { fill: var(--viz-s3-ink); }
    .viz-seg-label-ext { fill: var(--viz-ink-2); font-size: 12px; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; }
    .viz-bar { fill: var(--viz-s1); }
    .viz-bar-gray { fill: var(--viz-gray); }
    .viz-hit { fill: transparent; cursor: crosshair; }
    .viz-svg [data-t]:not(.viz-hit):hover { opacity: 0.88; }
    .viz-crosshair { stroke: var(--viz-muted); stroke-width: 1; stroke-dasharray: 3 3; pointer-events: none; }
    .viz-tooltip {
      position: absolute; display: none; z-index: 10; pointer-events: none;
      background: var(--viz-ink); color: var(--viz-surface);
      border-radius: 6px; padding: 0.5rem 0.7rem; font-size: 0.82rem; line-height: 1.55;
      white-space: nowrap; box-shadow: 0 4px 14px rgba(0, 0, 0, 0.18);
    }
    .viz-tip-note { opacity: 0.7; }
    .viz-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 0.9rem 0 0; }
    .viz-table th, .viz-table td { text-align: left; padding: 0.5rem 0.7rem; border-top: 1px solid var(--border, #d8dde4); vertical-align: top; }
    .viz-table th { font-size: 0.78rem; opacity: 0.6; font-weight: 600; white-space: nowrap; }
    .viz-table td { font-variant-numeric: tabular-nums; }
    .viz-chips { display: flex; flex-wrap: wrap; gap: 0.4rem 1.1rem; margin: 0.5rem 0 0.2rem; font-size: 0.82rem; }
    .viz-chip { display: inline-flex; align-items: center; gap: 0.35rem; }
    .viz-chip i { width: 10px; height: 10px; border-radius: 3px; display: inline-block; }
    .viz-chip.c1 i { background: var(--viz-s1); }
    .viz-chip.c2 i { background: var(--viz-s2); }
    .viz-chip.c3 i { background: var(--viz-s3); }
    .viz-chip.cg i { background: var(--viz-gray); }
    .viz-rank-controls { display: flex; align-items: center; gap: 0.6rem; margin: 0.4rem 0 0.8rem; font-size: 0.86rem; }
    .viz-rank-controls select { padding: 0.4rem 0.6rem; font-size: 0.86rem; border: 1px solid var(--border, #d8dde4); border-radius: 8px; background: var(--bg, #fff); color: inherit; }
  """


def build_page():
    drug_total = sum(v for _, v in DRUG_TYPE)
    scope_total = sum(v for _, v in SCOPE)
    peak_year, peak_val = max(YEARLY, key=lambda p: p[1])
    first_val = YEARLY[0][1]
    growth = f"约 {peak_val / first_val:.0f} 倍"
    bio_val = dict(DRUG_TYPE)["生物制品"]
    intl_val = dict(SCOPE)["国际多中心试验"]

    kpi_html = f"""
        <div class="viz-kpis">
          <div class="viz-kpi">
            <div class="viz-kpi-value">{fmt(TOTAL)}</div>
            <div class="viz-kpi-caption">平台登记（已公示）试验总数<br />截至 {AS_OF}</div>
          </div>
          <div class="viz-kpi">
            <div class="viz-kpi-value">{fmt(peak_val)}</div>
            <div class="viz-kpi-caption">{peak_year} 年登记峰值<br />较 2013 年 {growth}</div>
          </div>
          <div class="viz-kpi">
            <div class="viz-kpi-value">{fmt(bio_val)}</div>
            <div class="viz-kpi-caption">生物制品（分类口径）<br />占比 {pct(bio_val, drug_total)}</div>
          </div>
          <div class="viz-kpi">
            <div class="viz-kpi-value">{fmt(intl_val)}</div>
            <div class="viz-kpi-caption">国际多中心试验<br />占比 {pct(intl_val, scope_total)}</div>
          </div>
        </div>"""

    drug_table = "".join(
        f"<tr><td>{n}</td><td>{fmt(v)}</td><td>{pct(v, drug_total)}</td></tr>"
        for n, v in DRUG_TYPE)
    scope_table = "".join(
        f"<tr><td>{n}</td><td>{fmt(v)}</td><td>{pct(v, scope_total)}</td></tr>"
        for n, v in SCOPE)

    # 适应症排名区块（抓取数据就绪时输出；图表剔除「其他」，表格保留全量）
    ranking_html = ""
    ranking_table = ""
    ranking_chart = [(n, v) for n, v in INDICATION_RANKING if n != "其他"]
    other_n = dict(INDICATION_RANKING).get("其他", 0)
    rank_topn = min(len(ranking_chart), 20)
    if INDICATION_RANKING:
        nonbe = TRIALS_CRAWLED - BE_COUNT
        be_pct = BE_COUNT / TRIALS_CRAWLED * 100 if TRIALS_CRAWLED else 0
        ranking_html = f"""
        <div class="viz-chart">
          <h3>适应症排名（非 BE 注册试验，编者归类）</h3>
          <p class="viz-chart-sub">全部 {fmt(TRIALS_CRAWLED)} 项登记中，生物等效性（BE）试验 {fmt(BE_COUNT)} 项（{be_pct:.1f}%）；本图统计其余 {fmt(nonbe)} 项非 BE 注册试验的适应症大类，未归类 {fmt(other_n)} 项见表格。最高位以品牌色强调，其余降阶为灰。</p>
          <div class="viz-rank-controls no-print">
            <label for="rank-toggle">显示</label>
            <select id="rank-toggle">
              <option value="10">前 10</option>
              <option value="20" selected>前 20</option>
            </select>
          </div>
          <div id="viz-ranking">{ranking_svg(ranking_chart, rank_topn)}</div>
        </div>"""
        ranking_table = "".join(
            f"<tr><td>{i + 1}</td><td>{n}</td><td>{fmt(v)}</td></tr>"
            for i, (n, v) in enumerate(INDICATION_RANKING))

    body = f"""
        <aside class="content-note">
          <p><strong>数据来源：</strong><a href="https://www.chinadrugtrials.org.cn/" target="_blank" rel="noopener">药物临床试验登记与信息公示平台</a>（CDE）「信息统计」与检索结果，截至 {AS_OF}；平台登记（已公示）试验总数 {fmt(TOTAL)} 项。</p>
          <p><strong>口径说明：</strong>趋势、药物类别与试验范围为平台官方统计口径；药物类别与试验范围两项分类统计合计约 {fmt(drug_total)} 项，与总数之差为平台未归类部分。适应症排名为检索结果逐条归类（<strong>编者整理，非官方统计</strong>）。本页不构成投资或商业决策依据。</p>
        </aside>

        <div class="viz-root" id="viz-root">
          <div id="viz-tooltip" class="viz-tooltip"></div>
          {kpi_html}

          <div class="viz-chart">
            <h3>登记试验逐年趋势（2013–2026）</h3>
            <p class="viz-chart-sub">2013 年平台启用以来登记量增长 {growth}；2026 年为截至 {AS_OF} 的部分年份。悬浮查看各年数量。</p>
            {trend_svg()}
          </div>

          <div class="viz-chart">
            <h3>药物类别分布</h3>
            <p class="viz-chart-sub">化学药物仍是主体，生物制品占 {pct(bio_val, drug_total)}——创新药结构变化的直观信号。</p>
            {stacked_bar_svg(DRUG_TYPE)}
            <div class="viz-chips">
              <span class="viz-chip c1"><i></i>化学药物</span>
              <span class="viz-chip c2"><i></i>生物制品</span>
              <span class="viz-chip c3"><i></i>中药/天然药物</span>
            </div>
            <table class="viz-table"><thead><tr><th>类别</th><th>数量</th><th>占比（分类口径）</th></tr></thead>
            <tbody>{drug_table}</tbody></table>
          </div>

          <div class="viz-chart">
            <h3>试验范围：国内试验 vs 国际多中心</h3>
            <p class="viz-chart-sub">{pct(intl_val, scope_total)} 的国际多中心试验——中国创新药全球化与全球新药进中国的共同入口。</p>
            {scope_bars_svg(SCOPE)}
            <table class="viz-table"><thead><tr><th>范围</th><th>数量</th><th>占比</th></tr></thead>
            <tbody>{scope_table}</tbody></table>
          </div>
          {ranking_html}
          {('<h3 style="margin-top:2rem;">适应症归类明细</h3><table class="viz-table"><thead><tr><th>#</th><th>大类</th><th>数量</th></tr></thead><tbody>'
            + ranking_table + '</tbody></table>') if ranking_table else ''}
        </div>

        <p class="ctcae-related" style="margin-top:2.4rem;font-size:0.9rem;">
          相关资源：<a href="whitepaper.html">中国 TMF 管理白皮书</a> ·
          <a href="gcp-2026.html">2026 版 GCP 要点</a> ·
          <a href="tmf-reference.html">TMF 分类参考</a> ·
          <a href="etmf-guide.html">eTMF 指南</a>
        </p>
        <script type="application/json" id="cde-data">{{cde_data_json}}</script>
"""
    chart_data = {
        "yearly": YEARLY,
        "drug_type": [[n, v, pct(v, drug_total)] for n, v in DRUG_TYPE],
        "scope": [[n, v, pct(v, scope_total)] for n, v in SCOPE],
        "ranking": ranking_chart[:20],
    }
    body = body.replace("{cde_data_json}", json.dumps(chart_data, ensure_ascii=False))

    meta = {
        "title": "中国药物临床试验数据：登记趋势与适应症排名 | Vivarcus",
        "desc": (f"中国药物临床试验登记数据可视化：2013–2026 年登记趋势（截至 {AS_OF} 共 {fmt(TOTAL)} 项）、"
                 f"药物类别与国内/国际多中心分布、适应症排名。数据来自 CDE 药物临床试验登记与信息公示平台，图表可交互查看。"),
        "file": "cde-trials.html",
        "eyebrow": "行业资源 · 数据观察",
        "hero": "中国药物临床试验数据",
        "subtitle": f"CDE 登记平台公示数据：2013–2026 年登记趋势、药物类别与试验范围分布、适应症排名（截至 {AS_OF}）。",
    }
    html = sitegen.render_page(
        meta, body,
        cta_title="试验量 10 年增长 15 倍，检查关注度同步上升",
        cta_desc="登记量激增的时代，TMF 就该自动化：Vivarcus eTMF 内置完整性指标、稽查轨迹与 TMF 参考模型，开箱即用。",
        cta_secondary_href="whitepaper.html",
        cta_secondary_label="中国 TMF 管理白皮书",
        extra_style=EXTRA_STYLE,
    )
    html = html.replace("</body>",
                        '  <script src="js/tools.js"></script>\n' + PAGE_JS + "</body>")
    out = ROOT / "cde-trials.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} (yearly={len(YEARLY)}, "
          f"ranking={len(INDICATION_RANKING)}, be={BE_COUNT}, crawled={TRIALS_CRAWLED})")


if __name__ == "__main__":
    build_page()
