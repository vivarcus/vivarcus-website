#!/usr/bin/env python3
"""稽查发现分类对照表 static page builder (zh-only).

Zero-dependency (Python 3 stdlib only) build script:
  source data:  audit_findings_data.py（本目录，内容即数据源）
generates:
  website/audit-findings.html   (static page, committed to git)

Run: cd website && python3 tools/build_audit_findings.py

页面约定：zh-only 正文；发现库以 JSON 嵌入页面；按章/主题/严重程度筛选 +
关键词搜索；分组表格 + CSV 导出（UTF-8 BOM，Excel/WPS 直接打开，无门控）。
条款定位原则见 audit_findings_data.py 头部说明（不臆造条号）。
"""

import json
from pathlib import Path

import sitegen
from audit_findings_data import (
    CHAPTERS, CHAPTERS_EN, CLAUSE_EN, FINDINGS, SEVERITY, SEVERITY_EN,
    TOPICS, TOPICS_EN,
)

ROOT = Path(__file__).resolve().parent.parent  # website/

CH = dict(CHAPTERS)
TOP = dict(TOPICS)
SEV = dict(SEVERITY)


PAGE_JS = """<script>
    var AF_DATA = JSON.parse(document.getElementById('af-data').textContent);

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function isEn() { return !!(window.I18N && I18N.getLang() === 'en'); }

    function currentControls() {
      var severities = [];
      document.querySelectorAll('input[name="af-sev"]:checked').forEach(function (c) { severities.push(c.value); });
      severities.sort();
      return {
        chapter: document.getElementById('af-chapter').value,
        topic: document.getElementById('af-topic').value,
        severities: severities,
        q: document.getElementById('af-search').value.trim().toLowerCase(),
      };
    }

    function matches(f, c) {
      if (c.chapter !== 'all' && f.chapter !== c.chapter) return false;
      if (c.topic !== 'all' && f.topic !== c.topic) return false;
      if (c.severities.indexOf(f.severity) === -1) return false;
      if (c.q) {
        var hay = (f.finding + ' ' + f.check + ' ' + f.clause + ' ' + f.e6 +
                   ' ' + (f.finding_en || '') + ' ' + (f.check_en || '')).toLowerCase();
        if (hay.indexOf(c.q) === -1) return false;
      }
      return true;
    }

    function renderSelectOptions() {
      var en = isEn();
      var ch = document.getElementById('af-chapter');
      var html = '<option value="all" selected>' + (en ? 'All Chapters' : '全部章节') + '</option>';
      AF_DATA.chapters.forEach(function (c) {
        html += '<option value="' + c.key + '">' + esc(en ? c.label_en : c.label) + '</option>';
      });
      ch.innerHTML = html;
      var tp = document.getElementById('af-topic');
      html = '<option value="all" selected>' + (en ? 'All Topics' : '全部主题') + '</option>';
      AF_DATA.topics.forEach(function (t) {
        html += '<option value="' + t.key + '">' + esc(en ? t.label_en : t.label) + '（' + t.count + '）</option>';
      });
      tp.innerHTML = html;
      var sevBox = document.querySelector('#af-controls .af-sevs');
      html = '';
      Object.keys(AF_DATA.sev).forEach(function (k) {
        html += '<label><input type="checkbox" name="af-sev" value="' + k + '" checked /> ' +
                esc(en ? AF_DATA.sev_en[k] : AF_DATA.sev[k]) + '</label>';
      });
      sevBox.innerHTML = html;
    }

    // 过滤后的行（主题顺序），同时供预览与 CSV 导出使用
    function filteredRows(c) {
      var rows = [];
      AF_DATA.topics.forEach(function (t) {
        if (c.topic !== 'all' && t.key !== c.topic) return;
        AF_DATA.findings.forEach(function (f) {
          if (f.topic !== t.key || !matches(f, c)) return;
          rows.push({ finding: f, topic: t });
        });
      });
      return rows;
    }

    function sevBadge(s) {
      var en = isEn();
      var cls = s === 'critical' ? 'af-sev-critical' : (s === 'major' ? 'af-sev-major' : 'af-sev-minor');
      return '<span class="af-badge ' + cls + '">' + esc((en ? AF_DATA.sev_en : AF_DATA.sev)[s] || s) + '</span>';
    }

    function renderPreview() {
      var c = currentControls();
      var en = isEn();
      var rows = filteredRows(c);
      var nCritical = rows.filter(function (r) { return r.finding.severity === 'critical'; }).length;
      var nHot = rows.filter(function (r) { return r.finding.hot; }).length;
      var head = en
        ? '<th>#</th><th>Finding</th><th>Clause (2026 GCP)</th><th>E6(R3)</th><th>Severity</th><th>Self-Check Point</th>'
        : '<th>#</th><th>发现描述</th><th>条款定位（2026 GCP）</th><th>E6(R3)</th><th>严重程度</th><th>自查落点</th>';
      var html = '', idx = 0, curTopic = null;
      rows.forEach(function (r) {
        if (curTopic !== r.topic.key) {
          if (curTopic !== null) html += '</tbody></table></div>';
          curTopic = r.topic.key;
          html += '<h3 class="af-topic-head">' + esc(en ? r.topic.label_en : r.topic.label) +
                  ' <span class="af-topic-count">' +
                  rows.filter(function (x) { return x.topic.key === curTopic; }).length + (en ? ' items' : ' 条') + '</span></h3>';
          html += '<div class="af-scroll"><table class="af-table"><thead><tr>' + head +
            '</tr></thead><tbody>';
        }
        idx++;
        var f = r.finding;
        html += '<tr>' +
          '<td class="af-idx">' + idx + '</td>' +
          '<td class="af-finding">' + esc(en ? f.finding_en : f.finding) +
            (f.hot ? ' <span class="af-badge af-hot">' + (en ? 'HOT' : '高频') + '</span>' : '') + '</td>' +
          '<td class="af-clause">' + esc(en ? (f.clause_en || f.clause) : f.clause) + '</td>' +
          '<td class="af-e6">' + esc(en ? (f.e6_en || f.e6) : f.e6) + '</td>' +
          '<td>' + sevBadge(f.severity) + '</td>' +
          '<td class="af-check">' + esc(en ? f.check_en : f.check) + '</td>' +
          '</tr>';
      });
      html += '</tbody></table></div>';
      var list = document.getElementById('af-preview');
      list.innerHTML = html || ('<p class="af-empty">' + (en
        ? 'No findings under the current filters. Please relax the filters or clear the search term.'
        : '当前筛选条件下没有条目。请放宽筛选条件或清空搜索词。') + '</p>');
      document.getElementById('af-stats').textContent = en
        ? 'Total ' + rows.length + ' · Critical ' + nCritical + ' · HOT ' + nHot
        : '共 ' + rows.length + ' 条 · 严重 ' + nCritical + ' · 高频 ' + nHot;
    }

    function csvCell(s) {
      s = String(s == null ? '' : s);
      if (/[",\\n\\r]/.test(s)) s = '"' + s.replace(/"/g, '""') + '"';
      return s;
    }

    function downloadCsv() {
      var c = currentControls();
      var en = isEn();
      var rows = filteredRows(c);
      if (!rows.length) { renderPreview(); return; }
      var header = en
        ? '\\uFEFFNo.,Topic,Finding,Clause (2026 GCP),E6(R3) Mapping,Severity,Self-Check Point'
        : '\\uFEFF序号,主题,发现描述,条款定位（2026 GCP）,E6(R3) 映射,严重程度,自查落点';
      var lines = [header];
      rows.forEach(function (r, i) {
        lines.push([
          i + 1,
          en ? r.topic.label_en : r.topic.label,
          en ? r.finding.finding_en : r.finding.finding,
          en ? (r.finding.clause_en || r.finding.clause) : r.finding.clause,
          en ? (r.finding.e6_en || r.finding.e6) : r.finding.e6,
          (en ? AF_DATA.sev_en : AF_DATA.sev)[r.finding.severity] || '',
          en ? r.finding.check_en : r.finding.check,
        ].map(csvCell).join(','));
      });
      var now = new Date();
      var dateStr = now.getFullYear() + String(now.getMonth() + 1).padStart(2, '0') + String(now.getDate()).padStart(2, '0');
      var fname = 'vivarcus-audit-findings-' + dateStr + '.csv';
      var blob = new Blob([lines.join('\\r\\n')], { type: 'text/csv;charset=utf-8' });
      var a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = fname;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 2000);
    }

    document.addEventListener('DOMContentLoaded', function () {
      renderSelectOptions();
      renderPreview();
    });

    window.addEventListener('langchange', function () {
      renderSelectOptions();
      renderPreview();
    });

    document.addEventListener('change', function (e) {
      if (!e.target) return;
      if (e.target.id === 'af-chapter' || e.target.id === 'af-topic' || e.target.name === 'af-sev') { renderPreview(); }
    });

    var searchTimer = null;
    document.addEventListener('input', function (e) {
      if (!e.target || e.target.id !== 'af-search') return;
      clearTimeout(searchTimer);
      searchTimer = setTimeout(renderPreview, 150);
    });

    document.addEventListener('click', function (e) {
      if (e.target && e.target.id === 'af-csv-btn') downloadCsv();
      if (e.target && e.target.id === 'af-print-btn') Tools.printReport();
    });
  </script>"""

EXTRA_STYLE = """
    .af-howto { display: flex; flex-wrap: wrap; gap: 1rem 1.6rem; margin: 0 0 1.2rem; padding: 1rem 1.1rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 10px; background: var(--bg-soft, #f6f8fa); }
    .af-howto-item { flex: 1 1 15rem; font-size: 0.88rem; line-height: 1.65; }
    .af-howto-item strong { display: block; margin-bottom: 0.15rem; }
    .af-controls { display: flex; flex-wrap: wrap; gap: 1rem 1.4rem; margin-bottom: 0.9rem; }
    .af-field { display: flex; flex-direction: column; gap: 0.35rem; }
    .af-field > label, .af-field > .af-field-label { font-size: 0.82rem; opacity: 0.65; font-weight: 600; }
    .af-field select, .af-field input[type="text"] {
      padding: 0.5rem 0.8rem; font-size: 0.92rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 8px; outline: none;
      background: var(--bg, #fff); color: inherit; min-width: 10rem;
    }
    .af-field input[type="text"] { min-width: 14rem; }
    .af-field select:focus, .af-field input[type="text"]:focus { border-color: var(--accent, #2563eb); }
    .af-sevs { display: flex; gap: 1rem; flex-wrap: wrap; font-size: 0.9rem; padding: 0.45rem 0; }
    .af-sevs label { display: inline-flex; align-items: center; gap: 0.3rem; cursor: pointer; }
    .af-toolbar {
      display: flex; flex-wrap: wrap; align-items: center; gap: 0.9rem 1.2rem;
      margin: 1rem 0 1.4rem; padding: 0.8rem 1rem; border: 1px solid var(--border, #d8dde4);
      border-radius: 10px; background: var(--bg-soft, #f6f8fa); font-size: 0.9rem;
    }
    .af-stats { margin-left: auto; opacity: 0.85; white-space: nowrap; }
    .af-topic-head { margin: 1.6rem 0 0.5rem; font-size: 1.02rem; }
    .af-topic-count { font-weight: 400; font-size: 0.78rem; opacity: 0.6; margin-left: 0.4rem; }
    .af-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .af-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; margin: 0 0 0.6rem; min-width: 46rem; }
    .af-table th, .af-table td { text-align: left; padding: 0.5rem 0.7rem; border-top: 1px solid var(--border, #d8dde4); vertical-align: top; }
    .af-table th { font-size: 0.78rem; opacity: 0.6; font-weight: 600; white-space: nowrap; }
    .af-idx { opacity: 0.55; font-family: ui-monospace, monospace; white-space: nowrap; }
    .af-finding { line-height: 1.55; min-width: 16rem; }
    .af-clause { white-space: nowrap; opacity: 0.85; }
    .af-e6 { opacity: 0.75; white-space: nowrap; font-size: 0.82rem; }
    .af-check { line-height: 1.55; min-width: 16rem; opacity: 0.9; }
    .af-badge {
      font-size: 0.7rem; line-height: 1.4; padding: 0 0.4rem; border-radius: 4px;
      border: 1px solid var(--border, #d8dde4); opacity: 0.8; white-space: nowrap;
    }
    .af-sev-critical { color: #b91c1c; border-color: rgba(220, 38, 38, 0.4); }
    .af-sev-major { color: #b45309; border-color: rgba(217, 119, 6, 0.4); }
    .af-sev-minor { color: #1d4ed8; border-color: rgba(37, 99, 235, 0.35); }
    .af-hot { color: #b45309; border-color: rgba(217, 119, 6, 0.4); margin-left: 0.3rem; }
    .af-legend { font-size: 0.84rem; opacity: 0.8; line-height: 1.8; margin: 0.6rem 0 0; }
    .af-empty { padding: 1.5rem 0; opacity: 0.7; }
    .af-preview { margin-top: 1rem; }
    @media print {
      body.tools-print-mode .site-header, body.tools-print-mode .page-hero,
      body.tools-print-mode .cta-section, body.tools-print-mode .site-footer,
      body.tools-print-mode .no-print { display: none !important; }
    }
  """


def build_page():
    n = len(FINDINGS)
    n_critical = sum(1 for f in FINDINGS if f["severity"] == "critical")
    n_hot = sum(1 for f in FINDINGS if f.get("hot"))
    topics = [{"key": k, "label": v, "count": sum(1 for f in FINDINGS if f["topic"] == k)}
              for k, v in TOPICS if any(f["topic"] == k for f in FINDINGS)]

    sev_map = dict(SEVERITY)
    sev_map_en = dict(SEVERITY_EN)
    clause_en = dict(CLAUSE_EN)
    for f in FINDINGS:
        f["clause_en"] = clause_en.get(f["clause"], "")
    topics = [dict(t, label_en=dict(TOPICS_EN)[t["key"]]) for t in topics]

    data = {
        "findings": FINDINGS,
        "topics": topics,
        "chapters": [{"key": k, "label": v, "label_en": dict(CHAPTERS_EN)[k]} for k, v in CHAPTERS],
        "sev": sev_map,
        "sev_en": sev_map_en,
    }

    body = f"""
        <aside class="content-note">
          <p data-i18n-html="af.note.basis"><strong>依据：</strong>2026 版 GCP（2026-09-01 施行，NMPA 公告 2026 年第 50 号）+ ICH E6(R3)。条款定位原则：已公开解读的条文标具体条号，其余锚定「章 · 主题」；详见 <a href="gcp-2026.html">2026 版 GCP 要点</a> 与 <a href="ich-e6r3.html">ICH E6(R3) 中文要点</a>。</p>
          <p data-i18n-html="af.note.disclaimer"><strong>免责声明：</strong>发现库与严重程度分级为编者归纳的稽查实践参考，不构成合规结论；正式检查以现行法规、方案与公司 SOP 为准。</p>
        </aside>

        <div class="af-howto no-print">
          <div class="af-howto-item" data-i18n-html="af.howto.1"><strong>① 选范围</strong>按章、主题、严重程度筛选，或搜索关键词（如「稽查轨迹」「时限」）。</div>
          <div class="af-howto-item" data-i18n-html="af.howto.2"><strong>② 对照自查</strong>逐条看「自查落点」，把有风险的条目记下来，高频发现优先。</div>
          <div class="af-howto-item" data-i18n-html="af.howto.3"><strong>③ 导出整改</strong>下载 CSV 作为整改清单底稿，逐条闭环后归档。</div>
        </div>

        <div class="af-controls no-print" id="af-controls">
          <div class="af-field">
            <label for="af-chapter" data-i18n="af.field.chapter">章</label>
            <select id="af-chapter">
              <option value="all" selected>全部章节</option>
              {{chapter_options}}
            </select>
          </div>
          <div class="af-field">
            <label for="af-topic" data-i18n="af.field.topic">主题</label>
            <select id="af-topic">
              <option value="all" selected>全部主题</option>
              {{topic_options}}
            </select>
          </div>
          <div class="af-field">
            <span class="af-field-label" data-i18n="af.field.sev">严重程度</span>
            <div class="af-sevs">
              {{severity_options}}
            </div>
          </div>
          <div class="af-field">
            <label for="af-search" data-i18n="af.field.search">搜索</label>
            <input type="text" id="af-search" data-i18n-placeholder="af.search.placeholder" placeholder="关键词：如「时限」「授权」「备份」" />
          </div>
        </div>

        <div class="af-toolbar no-print">
          <span class="af-stats" id="af-stats"></span>
          <button type="button" class="btn btn-primary" id="af-csv-btn" data-i18n="af.btn.csv">下载对照表（CSV）</button>
          <button type="button" class="btn btn-outline" id="af-print-btn" data-i18n="af.btn.print">打印 / 导出 PDF</button>
        </div>

        <div id="af-preview" class="af-preview"></div>

        <p class="af-legend" data-i18n-html="af.legend">分级说明：<strong>严重</strong>=影响受试者权益/安全或数据可靠性的系统性发现；<strong>主要</strong>=违反 GCP/方案/SOP、需整改计划；<strong>一般</strong>=文档瑕疵或局部偏离。<strong>高频</strong>=稽查/核查中反复出现的发现，自查优先。</p>

        <p class="ctcae-related" style="margin-top:2.4rem;font-size:0.9rem;">
          <span data-i18n="af.related">相关资源：</span><a href="gcp-2026.html" data-i18n="af.related.gcp">2026 版 GCP 要点</a> ·
          <a href="ich-e6r3.html" data-i18n="af.related.e6r3">ICH E6(R3) 中文要点</a> ·
          <a href="template-audit-readiness-checklist.html" data-i18n="af.related.audit">稽查准备清单模板</a> ·
          <a href="tmf-checker.html" data-i18n="af.related.checker">TMF 完整性自查器</a> ·
          <a href="pd-decision-tree.html" data-i18n="af.related.pd">PD 决策树</a> ·
          <a href="timeline-calendar.html" data-i18n="af.related.tl">时限日历</a>
        </p>
        <script type="application/json" id="af-data">{{af_data_json}}</script>
"""
    chapter_options = "\n".join(
        f'              <option value="{c["key"]}">{c["label"]}</option>' for c in data["chapters"])
    topic_options = "\n".join(
        f'              <option value="{t["key"]}">{t["label"]}（{t["count"]}）</option>' for t in topics)
    severity_options = "\n".join(
        f'              <label><input type="checkbox" name="af-sev" value="{k}" checked /> {v}</label>'
        for k, v in SEVERITY)
    body = body.replace("{chapter_options}", chapter_options)
    body = body.replace("{topic_options}", topic_options)
    body = body.replace("{severity_options}", severity_options)
    body = body.replace("{af_data_json}", json.dumps(data, ensure_ascii=False))

    meta = {
        "title": "稽查发现分类对照表：常见稽查发现按 2026 GCP 章节归类 | Vivarcus",
        "desc": (f"稽查发现分类对照表：{n} 条常见稽查发现按 2026 版 GCP 六章与 ICH E6(R3) 原则归类，"
                 f"含条款定位、严重程度分级（严重 {n_critical} 条、高频 {n_hot} 条）与自查落点，"
                 f"支持筛选与 CSV 导出，稽查/飞检前自查用。"),
        "file": "audit-findings.html",
        "eyebrow": "行业资源 · 稽查工具",
        "hero": "稽查发现分类对照表",
        "subtitle": f"{n} 条常见稽查发现，按 2026 版 GCP 六章与 ICH E6(R3) 原则归类；选范围 → 对照自查 → 导出整改清单。",
    }
    html = sitegen.render_page(
        meta, body,
        cta_title="稽查准备清单与完整性指标，Vivarcus eTMF 里已经内置",
        cta_desc="发现→条款→自查落点之外，完整性、及时性、质量指标实时可见；稽查轨迹与受控数据更正对应 2026 GCP 第五章，开箱即用。",
        cta_secondary_href="template-audit-readiness-checklist.html",
        cta_secondary_label="稽查准备清单模板",
        extra_style=EXTRA_STYLE,
        i18n="af",
    )
    html = html.replace("</body>",
                        '  <script src="js/tools.js"></script>\n' + PAGE_JS + "</body>")
    out = ROOT / "audit-findings.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({n} findings, {n_critical} critical, {n_hot} hot)")


if __name__ == "__main__":
    build_page()
