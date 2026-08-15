#!/usr/bin/env python3
"""CTCAE 分级速查器 static page builder (zh-only).

Zero-dependency (Python 3 stdlib only) build script:
  source data in  docs/marketing/ctcae/ctcae-v5-zh.csv  (curated subset,
  high-frequency terms, self-produced Chinese translation)
generates:
  website/ctcae.html   (static page, committed to git)

Run: cd website && python3 tools/build_ctcae.py

页面约定：zh-only 正文（共享 chrome 走站点 i18n-data.js）；数据以 JSON 嵌入
页面，内联渲染器构建 DOM；搜索沿用 tmf-reference 的委托 + .hidden 模式。
"""

import csv
import json
from pathlib import Path

import sitegen

ROOT = Path(__file__).resolve().parent.parent  # website/
SRC = ROOT.parent / "docs/marketing/ctcae/ctcae-v5-zh.csv"


def read_terms():
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    socs, order = [], {}
    for r in rows:
        key = r["soc_zh"]
        if key not in order:
            order[key] = len(socs)
            socs.append({"soc_zh": key, "soc_en": r["soc_en"], "terms": []})
        socs[order[key]]["terms"].append({
            "zh": r["term_zh"],
            "en": r["term_en"],
            "grades": [r["g1"], r["g2"], r["g3"], r["g4"], r["g5"]],
            "note": r["note"],
        })
    return socs


PAGE_JS = """<script>
    var CTC_DATA = JSON.parse(document.getElementById('ctcae-data').textContent);
    var GRADE_HEADERS = ['1 轻度', '2 中度', '3 重度', '4 危及生命', '5 死亡'];

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function renderList() {
      var html = '';
      CTC_DATA.socs.forEach(function (soc) {
        var terms = '';
        soc.terms.forEach(function (t) {
          var chips = '';
          for (var g = 0; g < 5; g++) {
            if (t.grades[g]) chips += '<span class="ctcae-chip g' + (g + 1) + '">' + (g + 1) + '</span>';
          }
          var cells = '';
          for (var c = 0; c < 5; c++) cells += '<td>' + esc(t.grades[c] || '—') + '</td>';
          var note = t.note ? '<p class="ctcae-term-note">注：' + esc(t.note) + '</p>' : '';
          var hay = (t.zh + ' ' + t.en + ' ' + soc.soc_zh + ' ' + (t.note || '')).toLowerCase();
          terms += '<details class="ctcae-term" data-search="' + esc(hay) + '"><summary>' +
                   '<span class="ctcae-term-zh">' + esc(t.zh) + '</span> ' +
                   '<span class="ctcae-term-en">' + esc(t.en) + '</span>' + chips + '</summary>' +
                   '<div class="ctcae-scroll"><table class="ctcae-grade"><thead><tr><th>' +
                   GRADE_HEADERS.join('</th><th>') +
                   '</th></tr></thead><tbody><tr>' + cells + '</tr></tbody></table></div>' +
                   note + '</details>';
        });
        html += '<details class="ctcae-soc"><summary>' + esc(soc.soc_zh) +
                ' <span class="ctcae-soc-en">' + esc(soc.soc_en) + '</span>' +
                '<span class="ctcae-count">· ' + soc.terms.length + ' 条</span></summary>' +
                '<div class="ctcae-soc-body">' + terms + '</div></details>';
      });
      document.getElementById('ctcae-list').innerHTML = html;
    }

    document.addEventListener('DOMContentLoaded', renderList);

    // 客户端搜索：命中条目自动展开所属系统；无命中系统隐藏（事件委托，重渲染后仍有效）
    document.addEventListener('input', function (e) {
      if (!e.target || e.target.id !== 'ctcae-search-input') return;
      var q = e.target.value.trim().toLowerCase();
      var terms = document.querySelectorAll('.ctcae-term');
      var socs = document.querySelectorAll('.ctcae-soc');
      if (!q) {
        terms.forEach(function (t) { t.classList.remove('hidden'); });
        socs.forEach(function (s) { s.classList.remove('hidden'); s.removeAttribute('open'); });
        return;
      }
      terms.forEach(function (t) {
        var hit = t.getAttribute('data-search').indexOf(q) !== -1;
        t.classList.toggle('hidden', !hit);
        if (hit) { var soc = t.closest('.ctcae-soc'); if (soc) soc.setAttribute('open', ''); }
      });
      socs.forEach(function (s) {
        s.classList.toggle('hidden', s.querySelectorAll('.ctcae-term:not(.hidden)').length === 0);
      });
    });
  </script>"""

EXTRA_STYLE = """
    .ctcae-search { max-width: 42rem; margin: 0 auto 2.2rem; }
    .ctcae-search input {
      width: 100%; padding: 0.9rem 1.2rem; font-size: 1rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 8px; outline: none;
    }
    .ctcae-search input:focus { border-color: var(--accent, #2563eb); }
    .ctcae-legend { font-size: 0.86rem; opacity: 0.8; line-height: 1.8; margin-bottom: 2.2rem; }
    .ctcae-soc { margin-bottom: 0.9rem; border: 1px solid var(--border, #d8dde4); border-radius: 10px; overflow: hidden; }
    .ctcae-soc > summary {
      padding: 0.85rem 1.1rem; font-weight: 600; cursor: pointer;
      display: flex; flex-wrap: wrap; align-items: baseline; gap: 0.4rem 0.6rem;
    }
    .ctcae-soc > summary .ctcae-soc-en { font-weight: 400; font-size: 0.8rem; opacity: 0.55; }
    .ctcae-soc > summary .ctcae-count { font-weight: 400; font-size: 0.8rem; opacity: 0.65; margin-left: auto; }
    .ctcae-soc-body { padding: 0 1.1rem 0.4rem; }
    .ctcae-term { border-top: 1px dashed var(--border, #d8dde4); padding: 0.25rem 0; }
    .ctcae-term > summary { padding: 0.5rem 0.2rem; cursor: pointer; }
    .ctcae-term-zh { font-weight: 500; }
    .ctcae-term-en { font-size: 0.82rem; opacity: 0.6; margin-left: 0.3rem; }
    .ctcae-chip {
      display: inline-block; font-size: 0.68rem; line-height: 1.35; padding: 0 0.34rem;
      border-radius: 4px; border: 1px solid var(--border, #d8dde4); color: inherit;
      opacity: 0.7; margin-left: 0.3rem; vertical-align: 0.12rem;
    }
    .ctcae-chip.g3 { color: #b45309; border-color: rgba(217, 119, 6, 0.4); opacity: 0.9; }
    .ctcae-chip.g4, .ctcae-chip.g5 { color: #b91c1c; border-color: rgba(185, 28, 28, 0.4); opacity: 0.95; }
    .ctcae-grade { width: 100%; border-collapse: collapse; font-size: 0.86rem; margin: 0.3rem 0 0.2rem; }
    .ctcae-grade th, .ctcae-grade td {
      text-align: left; padding: 0.45rem 0.7rem; border-top: 1px solid var(--border, #d8dde4);
      vertical-align: top; min-width: 9rem; line-height: 1.65;
    }
    .ctcae-grade th { font-size: 0.75rem; opacity: 0.65; font-weight: 600; white-space: nowrap; }
    .ctcae-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .ctcae-term-note { margin: 0.3rem 0 0.6rem; font-size: 0.82rem; opacity: 0.75; line-height: 1.7; }
    .ctcae-term.hidden, .ctcae-soc.hidden { display: none !important; }
    .ctcae-related { margin-top: 2.4rem; font-size: 0.9rem; }
  """


def build_page():
    socs = read_terms()
    n_terms = sum(len(s["terms"]) for s in socs)
    n_socs = len(socs)

    body = f"""
        <aside class="content-note">
          <p><strong>版本与范围：</strong>NCI CTCAE v5.0（2017-11-27 发布）。本页收录肿瘤试验高频使用的<strong>精选常用条目</strong>（{n_terms} 条，覆盖 {n_socs} 个系统），非全量版本。</p>
          <p><strong>免责声明：</strong>中文为本站自产整理、非官方译本；正式使用请以 NCI CTCAE v5.0 英文原文及方案、伦理委员会要求为准。</p>
        </aside>

        <div class="ctcae-search">
          <input id="ctcae-search-input" type="search"
                 placeholder="搜索中文名、英文名或系统…（如：贫血、neutropenia、心脏）"
                 aria-label="搜索 CTCAE 术语" />
        </div>

        <p class="ctcae-legend">
          <strong>分级总则：</strong>1 轻度：无症状或轻微；2 中度：需要较小、局部或非侵入性治疗；影响工具性日常生活活动；
          3 重度：具有重要医学意义但不会立即危及生命；影响自理性日常生活活动；4 危及生命：需要紧急治疗；5 死亡：与不良事件相关的死亡。
          级别描述中的分号指「或者」；「—」表示该等级不存在；并非所有条目都包含全部 5 个等级。
          工具性日常生活活动指做饭、购买衣物、使用电话、理财等；自理性日常生活活动指洗澡、穿脱衣、吃饭、如厕、服药等。
        </p>

        <h2 class="section-title">按系统（SOC）浏览</h2>
        <div id="ctcae-list"></div>
        <script type="application/json" id="ctcae-data">{{ctcae_data_json}}</script>

        <p class="ctcae-related">
          相关资源：<a href="glossary.html">术语词典</a> ·
          <a href="template-sae-report.html">SAE 报告模板</a> ·
          <a href="tmf-reference.html">TMF 分类参考</a>
        </p>
"""
    body = body.replace("{ctcae_data_json}", json.dumps({"socs": socs}, ensure_ascii=False))

    meta = {
        "title": "CTCAE 分级速查器：CTCAE 5.0 常用不良事件分级中文对照 | Vivarcus",
        "desc": (f"CTCAE v5.0 不良事件分级速查：肿瘤试验高频 AE 精选条目 {n_terms} 条（贫血、中性粒细胞减少、"
                 "肝功能异常、免疫相关不良事件等），1-5 级定义中文对照，按系统分类浏览、中英文搜索，附版本与免责说明。"),
        "file": "ctcae.html",
        "eyebrow": "行业资源 · CTCAE 速查",
        "hero": "CTCAE 分级速查器",
        "subtitle": f"肿瘤试验高频不良事件分级：{n_terms} 条精选常用条目，1-5 级中文对照，按系统浏览、中英文搜索。",
    }
    html = sitegen.render_page(
        meta, body,
        cta_title="AE 分级和报告闭环，Vivarcus eTMF 里已经内置",
        cta_desc="AE/SAE 结构化记录、分级字段、时限提醒与文档归档一体管理，不用再靠 Excel 和记忆。",
        cta_secondary_href="glossary.html",
        cta_secondary_label="术语词典",
        extra_style=EXTRA_STYLE,
    )
    html = html.replace("</body>", PAGE_JS + "</body>")
    out = ROOT / "ctcae.html"
    out.write_text(html, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} ({n_terms} terms, {n_socs} SOCs)")


if __name__ == "__main__":
    build_page()
