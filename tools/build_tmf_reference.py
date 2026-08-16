#!/usr/bin/env python3
"""Vivarcus TMF 文件分类参考 static page builder.

Zero-dependency (Python 3 stdlib only) build script:
  source data in  release-payloads/desired/clinical-operations/etmf/data/templates/*.csv
  (zh: *.zh.csv, en: *.csv)
generates:
  website/tmf-reference.html   (static page, committed to git)

Run: cd website && python3 tools/build_tmf_reference.py

页面为单 URL 双语（沿用营销页惯例：/tmf-reference.html?lang=en）：
  - zh/en 数据均嵌入页面 JSON，运行时按语言渲染树与 EDL
  - 服务端静态输出 zh 版本作为 SEO / no-JS 兜底
  - 页面文案（hero/CTA 等）由页面内 TMF_TEXT 切换；共享 chrome（header/footer）
    走站点 i18n-data.js；meta 走 seo-head.js 的 data-i18n-meta
"""

import csv
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent  # website/
PAYLOAD = ROOT.parent / "release-payloads/desired/clinical-operations/etmf/data/templates"

MODEL_BY_LANG = {"zh": "TMF 参考模型 v3.0", "en": "TMF RM v3.0"}

# 部门/必备性/层级中文标签，与产品 picklist 语义一致
DEPT_LABEL = {
    "zh": {
        "clinical_operations__c": "临床运营",
        "supplies__c": "试验供应",
        "data_management__c": "数据管理",
        "biostatistics__c": "生物统计",
        "regulatory_affairs__c": "法规事务",
        "safety__c": "药物安全",
        "medical_writing__c": "医学写作",
        "quality_assurance__c": "质量保证",
        "project_management__c": "项目管理",
        "medical_affairs__c": "医学事务",
    },
    "en": {
        "clinical_operations__c": "Clinical Operations",
        "supplies__c": "Trial Supplies",
        "data_management__c": "Data Management",
        "biostatistics__c": "Biostatistics",
        "regulatory_affairs__c": "Regulatory Affairs",
        "safety__c": "Drug Safety",
        "medical_writing__c": "Medical Writing",
        "quality_assurance__c": "Quality Assurance",
        "project_management__c": "Project Management",
        "medical_affairs__c": "Medical Affairs",
    },
}
REQ_LABEL = {
    "zh": {"required__v": "必需", "notrequired__v": "不要求", "pending_decision__v": "待定"},
    "en": {"required__v": "Required", "notrequired__v": "Not Required", "pending_decision__v": "Pending Decision"},
}
LEVEL_LABEL = {
    "zh": {"study_level__v": "研究", "country_level__v": "国家/地区", "site_level__v": "中心"},
    "en": {"study_level__v": "Study", "country_level__v": "Country", "site_level__v": "Site"},
}


def esc(s):
    return html.escape(s or "", quote=True)


# ------------------------------------------------------------------ data --

def read_artifact_tree(lang):
    """TMF 参考模型 v3.0：zone -> section -> artifact。"""
    fname = "artifact__v.zh.csv" if lang == "zh" else "artifact__v.csv"
    rows = list(csv.DictReader((PAYLOAD / fname).open(encoding="utf-8")))
    rows = [r for r in rows if r["model__v.name__v"] == MODEL_BY_LANG[lang]]
    by_parent = {}
    for r in rows:
        by_parent.setdefault(r["parent_artifact__v.external_id__v"], []).append(r)
    zones = [r for r in rows if r["number__v"].count(".") == 0]
    tree = []
    for z in zones:
        sections = []
        for s in sorted(by_parent.get(z["external_id__v"], []), key=lambda r: r["number__v"]):
            arts = [[a["number__v"], a["name__v"], a["description__v"]]
                    for a in sorted(by_parent.get(s["external_id__v"], []), key=lambda r: r["number__v"])]
            sections.append({"num": s["number__v"], "name": s["name__v"], "arts": arts})
        tree.append({"num": z["number__v"], "name": z["name__v"], "sections": sections})
    return tree


def read_edl(lang):
    """标准 EDL 条目按部门分组；里程碑名经 milestone_template 映射。"""
    mfname = "milestone_template__v.zh.csv" if lang == "zh" else "milestone_template__v.csv"
    milestones = {}
    with (PAYLOAD / mfname).open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            milestones.setdefault(r["milestone_type__v"], r["name__v"])
    fname = "edl_item_template__v.zh.csv" if lang == "zh" else "edl_item_template__v.csv"
    rows = list(csv.DictReader((PAYLOAD / fname).open(encoding="utf-8")))
    groups = {d: [] for d in DEPT_LABEL[lang]}
    unknown = []
    for r in rows:
        d = r["etmf_department__v"] or ""
        item = [
            r["name__v"],
            LEVEL_LABEL[lang].get(r["level__v"], r["level__v"] or "—"),
            REQ_LABEL[lang].get(r["requiredness__v"], r["requiredness__v"] or "—"),
            r["expected_steady_state_count__v"] or "—",
            milestones.get(r["milestone_type__v"] or "", ""),
        ]
        if d in groups:
            groups[d].append(item)
        else:
            unknown.append(item)
    out = [{"dept": DEPT_LABEL[lang][d], "rows": sorted(items, key=lambda x: x[0])}
           for d, items in groups.items() if items]
    if unknown:
        out.append({"dept": "其他" if lang == "zh" else "Other",
                    "rows": sorted(unknown, key=lambda x: x[0])})
    return out


# ---------------------------------------------------------------- page JS --

PAGE_JS = """<script>
    // 页面文案（含计数），由生成器填充
    var TMF_TEXT = {tmf_text_json};
    var TMF_DATA = JSON.parse(document.getElementById('tmf-data').textContent);

    function esc(s) { return String(s == null ? '' : s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

    function currentLang() {
      var p = new URLSearchParams(location.search).get('lang');
      if (p === 'en' || p === 'zh') return p;
      try { var s = localStorage.getItem('vivarcus-lang'); if (s === 'en' || s === 'zh') return s; } catch (e) {}
      return 'zh';
    }

    function renderTree(lang) {
      var t = TMF_TEXT[lang], d = TMF_DATA[lang];
      var html = '';
      d.zones.forEach(function (z) {
        var n = 0, body = '';
        z.sections.forEach(function (s) {
          n += s.arts.length;
          body += '<div class="tmf-section-title">' + esc(s.num) + ' ' + esc(s.name) + '</div>';
          s.arts.forEach(function (a) {
            body += '<div class="tmf-artifact"><span class="tmf-num">' + esc(a[0]) +
                    '</span><span class="tmf-name">' + esc(a[1]) +
                    '</span><span class="tmf-desc">' + esc(a[2]) + '</span></div>';
          });
        });
        html += '<div class="tmf-zone"><h3><span>' + esc(z.num) + ' ' + esc(z.name) +
                '</span><span class="tmf-count">' + t.count.replace('{n}', n) +
                ' ▾</span></h3><div class="tmf-zone-body">' + body + '</div></div>';
      });
      return html;
    }

    function renderEdl(lang) {
      var t = TMF_TEXT[lang], d = TMF_DATA[lang];
      var html = '';
      d.edl.forEach(function (g) {
        var rows = '';
        g.rows.forEach(function (r) {
          rows += '<tr class="tmf-edl-row"><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) +
                  '</td><td>' + esc(r[2]) + '</td><td>' + esc(r[3]) +
                  '</td><td>' + esc(r[4]) + '</td></tr>';
        });
        html += '<details class="tmf-edl-group"><summary>' + esc(g.dept) +
                ' <span class="tmf-count">' + t.edlCount.replace('{n}', g.rows.length) +
                '</span></summary><div class="tmf-edl-scroll"><table class="tmf-edl-table"><thead><tr><th>' +
                t.edlHeaders.join('</th><th>') +
                '</th></tr></thead><tbody>' + rows + '</tbody></table></div></details>';
      });
      return html;
    }

    function applyChrome(lang) {
      var t = TMF_TEXT[lang];
      ['eyebrow', 'heroTitle', 'heroSubtitle', 'treeTitle', 'edlTitle', 'edlNote',
       'note', 'ctaTitle', 'ctaDesc'].forEach(function (k) {
        var el = document.getElementById('tmf-' + k);
        if (el) el.textContent = t[k];
      });
      var input = document.getElementById('tmf-search-input');
      if (input) input.placeholder = t.searchPlaceholder;
    }

    function renderAll(lang) {
      applyChrome(lang);
      document.getElementById('tmf-tree').innerHTML = renderTree(lang);
      document.getElementById('tmf-edl').innerHTML = renderEdl(lang);
      document.getElementById('tmf-search-input').value = '';
    }

    document.addEventListener('DOMContentLoaded', function () {
      renderAll(currentLang());
    });
    window.addEventListener('langchange', function (e) {
      renderAll(e.detail && e.detail.lang === 'en' ? 'en' : 'zh');
    });

    // 客户端搜索：按名称/编号/描述过滤，自动展开命中区域（事件委托，重渲染后仍有效）
    document.addEventListener('input', function (e) {
      if (!e.target || e.target.id !== 'tmf-search-input') return;
      var q = e.target.value.trim().toLowerCase();
      var artifacts = document.querySelectorAll('.tmf-artifact');
      var edlRows = document.querySelectorAll('.tmf-edl-row');
      var zones = document.querySelectorAll('.tmf-zone');
      var groups = document.querySelectorAll('.tmf-edl-group');
      if (!q) {
        artifacts.forEach(function (a) { a.classList.remove('hidden'); });
        edlRows.forEach(function (r) { r.classList.remove('hidden'); });
        zones.forEach(function (z) { z.classList.remove('hidden'); z.classList.remove('open'); });
        groups.forEach(function (g) { g.classList.remove('hidden'); g.removeAttribute('open'); });
        return;
      }
      artifacts.forEach(function (a) {
        var hit = a.textContent.toLowerCase().indexOf(q) !== -1;
        a.classList.toggle('hidden', !hit);
        if (hit) { var zone = a.closest('.tmf-zone'); if (zone) zone.classList.add('open'); }
      });
      zones.forEach(function (z) {
        z.classList.toggle('hidden', z.querySelectorAll('.tmf-artifact:not(.hidden)').length === 0);
      });
      edlRows.forEach(function (r) {
        r.classList.toggle('hidden', r.textContent.toLowerCase().indexOf(q) === -1);
      });
      groups.forEach(function (g) {
        var visible = g.querySelectorAll('.tmf-edl-row:not(.hidden)').length > 0;
        g.classList.toggle('hidden', !visible);
        if (visible) g.setAttribute('open', '');
      });
    });

    // 区域展开/收起（事件委托）
    document.addEventListener('click', function (e) {
      var h = e.target.closest('.tmf-zone > h3');
      if (h) h.parentElement.classList.toggle('open');
    });
  </script>"""


def build_page():
    data = {lang: {"zones": read_artifact_tree(lang), "edl": read_edl(lang)}
            for lang in ("zh", "en")}
    zh = data["zh"]
    n_zone = len(zh["zones"])
    n_section = sum(len(z["sections"]) for z in zh["zones"])
    n_artifact = sum(len(s["arts"]) for z in zh["zones"] for s in z["sections"])
    n_edl = sum(len(g["rows"]) for g in zh["edl"])

    tmf_text = {
        "zh": {
            "eyebrow": "行业资源 · TMF 参考",
            "heroTitle": "TMF 文件分类参考",
            "heroSubtitle": (f"DIA TMF 参考模型 v3.0 中文对照——{n_zone} 个区域、{n_section} 个分区、"
                             f"{n_artifact} 个文件项，另附标准预期文档清单（EDL）。查必备文件、搭目录结构，收藏这一页就够了。"),
            "treeTitle": f"① 参考模型：{n_zone} 个区域 → {n_section} 个分区 → {n_artifact} 个文件项",
            "searchPlaceholder": "搜索文档名称、编号或描述…（如：方案、01.01.01、监查）",
            "edlTitle": "② 预期文档清单（EDL）按部门分类",
            "edlNote": (f"以下 {n_edl} 条为 Vivarcus eTMF 标准模板预置的预期文档（Expected Document List），"
                        "与参考模型分类一一对应。层级：研究 / 国家（地区）/ 中心；数量为该文档在试验全程的预期归档份数。"),
            "note": ("说明：本页依据 DIA TMF Reference Model v3.0 整理，仅供学习参考，正式项目请以 DIA 官方发布版本为准。"
                     "参考模型来源：Vivarcus eTMF 预置的 TMF 参考模型（v3.0）与标准 EDL 模板。"),
            "ctaTitle": "这套分类，Vivarcus eTMF 里已经内置",
            "ctaDesc": "EDL 自动生成、文件自动归位到参考模型对应节点，比手工维护表格快一个量级。",
            "count": "{n} 项",
            "edlCount": "· {n} 条",
            "edlHeaders": ["预期文档", "层级", "必备性", "预期数量", "相关里程碑"],
        },
        "en": {
            "eyebrow": "Industry Resources · TMF Reference",
            "heroTitle": "TMF File Classification Reference",
            "heroSubtitle": (f"Chinese–English reference for the DIA TMF Reference Model v3.0 — "
                             f"{n_zone} zones, {n_section} sections, {n_artifact} artifacts, plus the standard "
                             "Expected Document List (EDL). Bookmark this page for essential documents and folder structures."),
            "treeTitle": f"① Reference Model: {n_zone} zones → {n_section} sections → {n_artifact} artifacts",
            "searchPlaceholder": "Search name, number or description… (e.g. protocol, 01.01.01, monitoring)",
            "edlTitle": "② Expected Document List (EDL) by Department",
            "edlNote": (f"The {n_edl} items below ship with the Vivarcus eTMF standard templates and map one-to-one "
                        "to the reference model. Levels: Study / Country / Site. Count: expected copies archived across the trial."),
            "note": ("Based on the DIA TMF Reference Model v3.0; for study use please refer to the official DIA release. "
                     "Source: the TMF Reference Model (v3.0) and standard EDL templates built into Vivarcus eTMF."),
            "ctaTitle": "Built into Vivarcus eTMF",
            "ctaDesc": "Auto-generated EDLs and auto-filing into reference-model nodes — an order of magnitude faster than maintaining spreadsheets by hand.",
            "count": "{n} items",
            "edlCount": "· {n} items",
            "edlHeaders": ["Expected Document", "Level", "Requiredness", "Expected Count", "Milestone"],
        },
    }

    page_js = PAGE_JS.replace("{tmf_text_json}", json.dumps(tmf_text, ensure_ascii=False))
    page = HEAD.replace("{tmf_data_json}", json.dumps(data, ensure_ascii=False)) \
               .replace("{page_js}", page_js)
    out = ROOT / "tmf-reference.html"
    out.write_text(page, encoding="utf-8")
    print(f"  wrote {out.relative_to(ROOT)} "
          f"({n_zone} zones, {n_section} sections, {n_artifact} artifacts, {n_edl} EDL items, zh+en)")


# ---------------------------------------------------------------- template --

HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-i18n-title="tmf.meta.title">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" data-i18n-meta="tmf.meta.desc" content="TMF 文件分类参考：DIA TMF 参考模型 v3.0 中文对照（12 个区域、49 个分区、252 个文件项），附临床试验预期文档清单（EDL）按部门分类。TMF 必备文件查这份就够。" />
  <title>TMF 文件分类参考 | Vivarcus</title>
  <link rel="canonical" href="https://vivarcus.com/tmf-reference.html" />
  <link rel="alternate" hreflang="zh-CN" href="https://vivarcus.com/tmf-reference.html" />
  <link rel="alternate" hreflang="en-US" href="https://vivarcus.com/tmf-reference.html?lang=en" />
  <link rel="alternate" hreflang="x-default" href="https://vivarcus.com/tmf-reference.html" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Vivarcus" />
  <meta property="og:url" content="https://vivarcus.com/tmf-reference.html" />
  <meta property="og:title" data-i18n-og="tmf.meta.title" content="TMF 文件分类参考 | Vivarcus" />
  <meta property="og:description" data-i18n-og="tmf.meta.desc" content="TMF 文件分类参考：DIA TMF 参考模型 v3.0 中文对照（12 个区域、49 个分区、252 个文件项），附临床试验预期文档清单（EDL）按部门分类。" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:locale:alternate" content="en_US" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="css/icons.css" />
  <link rel="stylesheet" href="css/style.css" />
  <script src="js/i18n-data.js"></script>
  <script src="js/seo-head.js"></script>
  <script src="js/tracking.js"></script>
  <style>
    .tmf-wrap { padding: 2rem 0 4rem; }
    .tmf-search { max-width: 42rem; margin: 0 auto 2.5rem; }
    .tmf-search input {
      width: 100%; padding: 0.9rem 1.2rem; font-size: 1rem;
      border: 1px solid var(--border, #d8dde4); border-radius: 8px; outline: none;
    }
    .tmf-search input:focus { border-color: var(--accent, #2563eb); }
    .tmf-zone { margin-bottom: 1.2rem; border: 1px solid var(--border, #d8dde4); border-radius: 10px; overflow: hidden; }
    .tmf-zone > h3 { margin: 0; padding: 0.9rem 1.1rem; font-size: 1.05rem; cursor: pointer; display: flex; justify-content: space-between; align-items: center; }
    .tmf-zone > h3 .tmf-count { font-size: 0.8rem; font-weight: 400; opacity: 0.65; }
    .tmf-zone-body { padding: 0 1.1rem 1rem; display: none; }
    .tmf-zone.open > .tmf-zone-body { display: block; }
    .tmf-section-title { margin: 1.2rem 0 0.4rem; font-size: 0.95rem; font-weight: 600; }
    .tmf-artifact { padding: 0.45rem 0.3rem; border-bottom: 1px dashed var(--border, #d8dde4); }
    .tmf-artifact:last-child { border-bottom: none; }
    .tmf-artifact .tmf-num { display: inline-block; min-width: 4.2rem; font-size: 0.78rem; font-family: ui-monospace, monospace; opacity: 0.6; vertical-align: top; padding-top: 0.15rem; }
    .tmf-artifact .tmf-name { font-weight: 500; }
    .tmf-artifact .tmf-desc { display: block; margin: 0.15rem 0 0 4.2rem; font-size: 0.86rem; opacity: 0.75; }
    .tmf-artifact.hidden, .tmf-zone.hidden, .tmf-edl-group.hidden { display: none !important; }
    .tmf-edl-group { margin-bottom: 1.2rem; border: 1px solid var(--border, #d8dde4); border-radius: 10px; overflow: hidden; }
    .tmf-edl-group > summary { padding: 0.9rem 1.1rem; font-weight: 600; cursor: pointer; }
    .tmf-edl-group > summary .tmf-count { font-weight: 400; opacity: 0.65; font-size: 0.85rem; }
    .tmf-edl-table { width: 100%; border-collapse: collapse; font-size: 0.88rem; }
    .tmf-edl-table th, .tmf-edl-table td { text-align: left; padding: 0.45rem 1.1rem; border-top: 1px solid var(--border, #d8dde4); }
    .tmf-edl-table th { font-size: 0.78rem; opacity: 0.65; font-weight: 600; }
    .tmf-edl-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .tmf-note { font-size: 0.82rem; opacity: 0.7; line-height: 1.7; }
  </style>
</head>
<body>

  <header class="site-header">
    <div class="container">
      <a href="/" class="header-logo" data-i18n-aria="common.logo.aria" aria-label="Vivarcus 首页">
        <span class="header-logo-dark">Vivar</span><span class="header-logo-accent">cus</span>
      </a>

      <button class="mobile-toggle" data-i18n-aria="common.menu.aria" aria-label="菜单">
        <span></span><span></span><span></span>
      </button>

      <nav class="header-nav">
        <a href="products.html" data-i18n="common.nav.products">产品</a>
        <a href="about.html" data-i18n="common.nav.about">关于</a>
        <a href="release-26r3.html" data-i18n="common.nav.release">发布说明</a>
        <a href="help/zh/index.html" data-lang-href-zh="help/zh/index.html" data-lang-href-en="help/en/index.html" data-i18n="common.nav.help">帮助中心</a>
      </nav>

      <div class="header-actions">
        <button class="lang-switch" data-lang-toggle aria-label="Switch to English">
          <span data-lang-zh>EN</span><span data-lang-en>中</span>
        </button>
        <a href="trial.html" class="btn btn-sm btn-primary" data-i18n="common.nav.trial">试用申请</a>
      </div>
    </div>
    <div class="scroll-progress" aria-hidden="true"></div>
  </header>

  <main>
    <section class="page-hero">
      <div class="container">
        <span class="page-hero-eyebrow">
          <i class="ic ic--folder-open" aria-hidden="true"></i>
          <span id="tmf-eyebrow">行业资源 · TMF 参考</span>
        </span>
        <h1 class="page-hero-title" id="tmf-heroTitle">TMF 文件分类参考</h1>
        <p class="page-hero-subtitle" id="tmf-heroSubtitle">DIA TMF 参考模型 v3.0 中文对照——12 个区域、49 个分区、252 个文件项，另附标准预期文档清单（EDL）。查必备文件、搭目录结构，收藏这一页就够了。</p>
      </div>
    </section>

    <section class="section tmf-wrap">
      <div class="container">
        <div class="tmf-search">
          <input id="tmf-search-input" type="search" placeholder="搜索文档名称、编号或描述…（如：方案、01.01.01、监查）" aria-label="搜索 TMF 文件" />
        </div>

        <h2 class="section-title" id="tmf-treeTitle">① 参考模型：12 个区域 → 49 个分区 → 252 个文件项</h2>
        <div id="tmf-tree"></div>

        <h2 class="section-title" style="margin-top:3rem;" id="tmf-edlTitle">② 预期文档清单（EDL）按部门分类</h2>
        <p class="tmf-note" id="tmf-edlNote">以下 466 条为 Vivarcus eTMF 标准模板预置的预期文档（Expected Document List），与参考模型分类一一对应。层级：研究 / 国家（地区）/ 中心；数量为该文档在试验全程的预期归档份数。</p>
        <div id="tmf-edl"></div>

        <p class="tmf-note" id="tmf-note" style="margin-top:1.5rem;">
          说明：本页依据 DIA TMF Reference Model v3.0 整理，仅供学习参考，正式项目请以 DIA 官方发布版本为准。
          参考模型来源：Vivarcus eTMF 预置的 TMF 参考模型（v3.0）与标准 EDL 模板。
        </p>
      </div>
    </section>

    <section class="cta-section" data-reveal>
      <div class="container">
        <div class="cta-content">
          <h2 id="tmf-ctaTitle">这套分类，Vivarcus eTMF 里已经内置</h2>
          <p id="tmf-ctaDesc">EDL 自动生成、文件自动归位到参考模型对应节点，比手工维护表格快一个量级。</p>
          <div class="cta-actions">
            <a href="trial.html" class="btn btn-primary btn-lg">
              <span data-i18n="common.nav.trial">试用申请</span>
              <i class="ic ic--arrow-right" aria-hidden="true"></i>
            </a>
            <a href="products.html" class="btn btn-outline btn-lg" data-i18n="common.cta.viewProducts">查看产品</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container">
      <div class="footer-grid">
        <div class="footer-brand">
          <a href="/" class="header-logo" data-i18n-aria="common.logo.aria" aria-label="Vivarcus">
            <span class="header-logo-dark">Vivar</span><span class="header-logo-accent">cus</span>
          </a>
          <p data-i18n="common.footer.brand">为生命科学行业打造的数字化平台。灵活、合规、自主可控。</p>
        </div>

        <div class="footer-col">
          <h4 data-i18n="common.footer.products">产品</h4>
          <a href="products.html" data-i18n="common.footer.etmf">eTMF</a>
          <a href="products.html" data-i18n="common.footer.ctms">CTMS</a>
          <a href="products.html" data-i18n="common.footer.startup">Study Startup</a>
        </div>

        <div class="footer-col">
          <h4 data-i18n="common.footer.resources">资源</h4>
          <a href="etmf-guide.html" data-i18n="common.footer.guide">eTMF 指南</a>
          <a href="ctms-guide.html" data-i18n="common.footer.ctmsGuide">CTMS 指南</a>
          <a href="etmf-ctms-edc.html" data-i18n="common.footer.cmp">系统对比</a>
          <a href="tmf-reference.html" data-i18n="common.footer.tmfReference">TMF 分类参考</a>
          <a href="templates.html" data-i18n="common.footer.templates">模板库</a>
          <a href="regulations.html" data-i18n="common.footer.regulations">法规库</a>
          <a href="whitepaper.html" data-i18n="common.footer.whitepaper">白皮书</a>
          <a href="glossary.html" data-i18n="common.footer.glossary">术语词典</a>
        </div>

        <div class="footer-col">
          <h4 data-i18n="common.footer.tools">工具</h4>
          <a href="ctcae.html" data-i18n="common.footer.ctcae">CTCAE 速查</a>
          <a href="pd-decision-tree.html" data-i18n="common.footer.pdTree">PD 决策树</a>
          <a href="timeline-calendar.html" data-i18n="common.footer.timeline">时限日历</a>
          <a href="visit-calculator.html" data-i18n="common.footer.visitCalc">访视计算器</a>
          <a href="sample-size-calculator.html" data-i18n="common.footer.sampleSize">样本量计算器</a>
          <a href="tmf-checker.html" data-i18n="common.footer.tmfChecker">TMF 自查器</a>
          <a href="edl-generator.html" data-i18n="common.footer.edlGenerator">EDL 生成器</a>
          <a href="audit-findings.html" data-i18n="common.footer.auditFindings">稽查对照表</a>
          <a href="cde-trials.html" data-i18n="common.footer.cdeTrials">CDE 数据</a>
        </div>

        <div class="footer-col">
          <h4 data-i18n="common.footer.links">链接</h4>
          <a href="trial.html" data-i18n="common.footer.trial">试用申请</a>
          <a href="help/zh/index.html" data-lang-href-zh="help/zh/index.html" data-lang-href-en="help/en/index.html" data-i18n="common.footer.help">帮助中心</a>
          <a href="release-26r3.html" data-i18n="common.footer.release">发布说明</a>
          <a href="https://github.com/vivarcus" target="_blank" rel="noopener" data-i18n="common.footer.github">GitHub</a>
          <a href="https://gitee.com/vivarcus" target="_blank" rel="noopener" data-i18n="common.footer.gitee">Gitee</a>
        </div>

      </div>

      <div class="footer-bottom">
        <span data-i18n="common.footer.copyright">&copy; 2010–2026 Vivarcus. 保留所有权利。</span>
      </div>
    </div>
  </footer>

  <script type="application/json" id="tmf-data">{tmf_data_json}</script>
  <script src="js/i18n.js"></script>
  <script src="js/main.js"></script>
{page_js}
</body>
</html>
"""


if __name__ == "__main__":
    build_page()
