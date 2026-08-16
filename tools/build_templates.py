#!/usr/bin/env python3
"""Generate template library detail pages from docs/marketing/templates/*.md.

Run from repo root:  python3 website/tools/build_templates.py
Content source of truth: docs/marketing/templates/*.md
Generated pages: website/template-*.html (zh-only; site chrome keeps common i18n)
"""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(ROOT, "docs", "marketing", "templates")
OUT_DIR = os.path.join(ROOT, "website")

# (source md, output html, title, meta description, eyebrow, hero title, hero subtitle)
PAGES = [
    ("01-monitoring-visit-report.md", "template-monitoring-visit-report.html",
     "监查访视报告模板（MVR）— 临床试验免费模板 | Vivarcus",
     "监查访视报告模板（MVR）：访视信息、知情同意、SDV、药物管理、安全性报告、发现与 CAPA 全字段结构，附填写示例与常见错误对照，免费使用。",
     "模板库 · 访视报告", "监查访视报告模板（MVR）",
     "监查访视报告是监查质量的直接证据。本模板覆盖访视信息、遗留跟进、知情同意、SDV、药物管理、安全性报告与发现闭环，可直接复制使用。"),
    ("01a-monitoring-visit-report-example.md", "template-mvr-example.html",
     "监查访视报告填写示例与常见错误 TOP 10 | Vivarcus",
     "监查访视报告（MVR）填写示例：一份填好的完整示范（逐条注解为什么这么写）+ 常见错误 TOP 10 对照 + 提交前自检清单。",
     "模板库 · 填写示例", "MVR 填写示例与常见错误对照",
     "空白模板解决\"有什么字段\"，这篇解决\"怎么填才对\"：虚构示例逐条注解，加稽查视角的常见错误对照。"),
    ("02-site-initiation-report.md", "template-site-initiation-report.html",
     "中心启动访视报告模板（SIV）| Vivarcus",
     "中心启动访视报告模板（SIV）：培训内容核对表、参训签名表、中心资质与设施核对、文件到位情况、遗留事项与启动结论。",
     "模板库 · 访视报告", "中心启动访视报告模板（SIV）",
     "启动培训签名表是稽查必查项。本模板含培训主题核对、参训签名、资质设施核对与启动结论，现场/远程启动均适用。"),
    ("03-closeout-visit-report.md", "template-closeout-visit-report.html",
     "关中心访视报告模板（COV）| Vivarcus",
     "关中心访视报告模板（COV）：数据清理核对、药物清点、生物样本处理、文件归档、伦理结题通知与归档声明，稽查高发环节逐项核对。",
     "模板库 · 访视报告", "关中心访视报告模板（COV）",
     "关中心是稽查高发环节：数据未清理、药物清点不平、伦理未结题是最常见发现。本模板逐项核对后再签署归档声明。"),
    ("04-protocol-deviation-log.md", "template-protocol-deviation-log.html",
     "方案偏离日志模板（Protocol Deviation Log）| Vivarcus",
     "方案偏离日志模板（PD Log）：偏离描述、重要偏离判定参考、根因分析与 CAPA、报告记录。PD 是稽查必查文件，每条都要闭环。",
     "模板库 · 记录表格", "方案偏离日志模板（PD Log）",
     "PD 日志稽查常见问题不是\"没记录\"，而是\"没分析、没 CAPA、没闭环\"。本模板含重要偏离判定参考与管理要求。"),
    ("05-icf-review-checklist.md", "template-icf-checklist.html",
     "知情同意审核清单模板（ICF）| Vivarcus",
     "知情同意审核清单模板（ICF）：版本与伦理批准核对、必备要素核对、特殊情形（弱势群体/未成年人/见证人）、语言可读性与签署页核对。",
     "模板库 · 检查清单", "知情同意审核清单模板（ICF）",
     "ICF 是检查中发现级别最高的文件：版本混用、签署时间晚于研究程序最常见。本清单覆盖必备要素与特殊情形。"),
    ("06-tmf-index.md", "template-tmf-index.html",
     "TMF 文件清单模板（EDL）— 试验主文件必备文件索引 | Vivarcus",
     "TMF 文件清单模板（简版 EDL）：按启动前/进行中/结束后三阶段整理的试验主文件必备文件索引，标注核心项与负责方，附自查方法。",
     "模板库 · 文件清单", "TMF 文件清单模板（简版 EDL）",
     "建立 TMF/ISF 结构、中心启动文件核对、稽查前完整性自查的三阶段必备文件索引，标注稽查核心项。"),
    ("07-sop-framework.md", "template-sop-framework.html",
     "SOP 框架模板：标准操作规程撰写规范 | Vivarcus",
     "SOP 框架模板：文件控制页、目的/范围/职责、流程图、程序步骤、记录与表格、修订历史，附 SOP 撰写自检清单。",
     "模板库 · 体系文件", "SOP 框架模板",
     "稽查发现中最常见的一类就是\"SOP 与实际操作不一致\"。本模板给出 SOP 结构规范与发布前自检清单。"),
    ("08-audit-readiness-checklist.md", "template-audit-readiness-checklist.html",
     "稽查准备清单模板（Audit Readiness Checklist）| Vivarcus",
     "稽查准备清单模板：中心层面（人员授权/知情同意/ISF/数据质量/安全性/药物管理）与项目层面自查清单，附常见稽查发现 TOP 与现场配合准备。",
     "模板库 · 检查清单", "稽查准备清单模板",
     "稽查前 2-4 周按\"中心自查 → 项目汇总 → 整改闭环\"三步走。本清单打印出来逐项打勾，本身就是稽查准备的有效证据。"),
    ("09-training-log.md", "template-training-log.html",
     "临床试验培训记录表模板（Training Log）| Vivarcus",
     "临床试验培训记录表模板：培训基本信息、签到签名表、效果评估与补训安排。培训记录是稽查必查项，须本人当场签字。",
     "模板库 · 记录表格", "培训记录表模板（Training Log）",
     "培训记录稽查必查两条时间逻辑：培训早于首次执行任务、文件升版后重新培训。本模板当场签字、版本关联、到期复训。"),
    ("10-sae-report-template.md", "template-sae-report.html",
     "SAE 报告模板：严重不良事件报告表 | Vivarcus",
     "SAE 报告模板：受试者信息、事件描述、严重性标准、相关性评估、报告时限记录（24 小时/7 天/15 天）与签署。不替代官方法规表格。",
     "模板库 · 报告模板", "SAE 报告模板（严重不良事件报告表）",
     "SAE 报告最关键三件事：时限（获知后 24 小时内报告）、诊断（写诊断不写症状）、签名（PI 本人签署）。"),
    ("11-site-initiation-checklist.md", "template-site-initiation-checklist.html",
     "中心启动检查清单模板（Site Initiation Checklist）| Vivarcus",
     "中心启动检查清单模板：启动前准备（合同/伦理/人员/物资）、启动访视当日培训逐项核对、入组前确认。打印即用，与启动访视报告配套。",
     "模板库 · 检查清单", "中心启动检查清单模板",
     "启动访视最怕培训走过场、签名事后补。本清单一页纸：启动前自查 + 当日逐项打勾 + 入组前确认。"),
    ("12-monitoring-visit-checklist.md", "template-monitoring-visit-checklist.html",
     "监查访视检查清单模板（Monitoring Visit Checklist）| Vivarcus",
     "监查访视检查清单模板：访视前准备、访视中逐项核对（ICF/入排/SDV/药物/安全性/偏离/ISF）、访视后收尾。与 MVR 报告模板配套，勾完照抄成稿。",
     "模板库 · 检查清单", "监查访视检查清单模板",
     "访视前/中/后三阶段勾选式核对，直接对应监查访视报告的章节——避免只打勾不写证据。"),
    ("13-closeout-checklist.md", "template-closeout-checklist.html",
     "关中心检查清单模板（Close-out Checklist）| Vivarcus",
     "关中心检查清单模板：数据清理、药物清点、生物样本、文件归档、通知收尾五类逐项关闭。关中心访视前 2 周先自查，稽查高发环节提前堵漏。",
     "模板库 · 检查清单", "关中心检查清单模板",
     "关中心是稽查高发环节：数据没清干净、药物对不上账、伦理没结题通知最常见。关中心前 2 周先用本清单自查。"),
]

HEAD = """<!DOCTYPE html>
<html lang="zh-CN" data-i18n-title="@@I18N@@.meta.title">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" data-i18n-meta="@@I18N@@.meta.desc" content="@@DESC@@" />
  <title>@@TITLE@@</title>
  <link rel="canonical" href="https://vivarcus.com/@@FILE@@" />
  <link rel="alternate" hreflang="zh-CN" href="https://vivarcus.com/@@FILE@@" />
  <link rel="alternate" hreflang="en-US" href="https://vivarcus.com/@@FILE@@?lang=en" />
  <link rel="alternate" hreflang="x-default" href="https://vivarcus.com/@@FILE@@" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Vivarcus" />
  <meta property="og:url" content="https://vivarcus.com/@@FILE@@" />
  <meta property="og:title" data-i18n-og="@@I18N@@.meta.title" content="@@TITLE@@" />
  <meta property="og:description" data-i18n-og="@@I18N@@.meta.desc" content="@@DESC@@" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:locale:alternate" content="en_US" />
  <meta property="og:image" content="https://vivarcus.com/assets/og-image.png" />
  <meta property="og:image:alt" content="@@TITLE@@" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="css/icons.css" />
  <link rel="stylesheet" href="css/style.css" />
  <script src="js/i18n-data.js"></script>
  <script src="js/seo-head.js"></script>
  <script src="js/tracking.js"></script>
  <style>
    .template-wrap { padding: 1.5rem 0 3rem; }
    .template-content { max-width: 56rem; }
    .template-content h2 { margin: 2.2rem 0 0.8rem; font-size: 1.25rem; }
    .template-content h3 { margin: 1.8rem 0 0.6rem; font-size: 1.08rem; }
    .template-content h4 { margin: 1.4rem 0 0.5rem; font-size: 1rem; }
    .template-content p { line-height: 1.8; }
    .template-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; margin: 0.9rem 0 1.4rem; }
    .template-table th, .template-table td { text-align: left; padding: 0.55rem 0.8rem; border-top: 1px solid var(--border, #d8dde4); vertical-align: top; }
    .template-table th { font-size: 0.8rem; opacity: 0.65; font-weight: 600; white-space: nowrap; }
    .template-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .template-note { font-size: 0.88rem; opacity: 0.85; border-left: 3px solid var(--accent, #2563eb); padding: 0.6rem 1rem; margin: 1.2rem 0; background: var(--bg-soft, #f6f8fa); border-radius: 0 6px 6px 0; }
    .template-note p { margin: 0.25rem 0; }
    .template-back { margin: 1.2rem 0 0; font-size: 0.9rem; }
    .template-guide { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0.75rem; margin: 1.2rem 0 1.5rem; }
    .template-guide-item { border: 1px solid var(--border, #d8dde4); border-radius: 8px; padding: 0.8rem 0.9rem; }
    .template-guide-item strong { display: block; margin-bottom: 0.25rem; font-size: 0.78rem; }
    .template-guide-item span { font-size: 0.86rem; line-height: 1.6; opacity: 0.78; }
    .template-related { margin: -0.25rem 0 1.4rem; font-size: 0.88rem; }
    @media (max-width: 720px) { .template-guide { grid-template-columns: 1fr; } }
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
        <a href="templates.html" data-i18n="common.nav.templates">模板库</a>
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
          <span data-i18n="@@I18N@@.hero.eyebrow">@@EYEBROW@@</span>
        </span>
        <h1 class="page-hero-title" data-i18n="@@I18N@@.hero.title">@@HERO@@</h1>
        <p class="page-hero-subtitle" data-i18n="@@I18N@@.hero.subtitle">@@SUBTITLE@@</p>
      </div>
    </section>

    <section class="section template-wrap">
      <div class="container template-content">
        <p class="template-back"><a href="templates.html" data-i18n="tpl.common.back">&larr; 返回模板库</a></p>
<div id="tpl-content">
@@GUIDE@@
@@BODY@@
</div>
        <script type="application/json" id="tpl-data-en">{"guide": @@GUIDE_EN_JSON@@, "body": @@BODY_EN_JSON@@}</script>
        <script>
          (function () {
            var el = document.getElementById('tpl-content');
            var zhHTML = el.innerHTML;
            var data = JSON.parse(document.getElementById('tpl-data-en').textContent);
            function apply() {
              var en = !!(window.I18N && I18N.getLang() === 'en');
              el.innerHTML = en ? (data.guide + data.body) : zhHTML;
            }
            window.addEventListener('langchange', apply);
          })();
        </script>
      </div>
    </section>
"""

CTA = """    <section class="cta-section" data-reveal>
      <div class="container">
        <div class="cta-content">
          <h2 data-i18n="@@I18N@@.cta.title">@@CTA_TITLE@@</h2>
          <p data-i18n="@@I18N@@.cta.desc">@@CTA_DESC@@</p>
          <div class="cta-actions">
            <a href="trial.html" class="btn btn-primary btn-lg">
              <span data-i18n="common.nav.trial">试用申请</span>
              <i class="ic ic--arrow-right" aria-hidden="true"></i>
            </a>
            <a href="templates.html" class="btn btn-outline btn-lg" data-i18n="tpl.common.ctaSecondary">全部模板</a>
          </div>
        </div>
      </div>
    </section>
  </main>
"""

FOOT = """
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

  <script src="js/i18n.js"></script>
  <script src="js/main.js"></script>
</body>
</html>
"""

# Per-page CTA titles; default used when not listed.
CTA_TITLES = {
    "template-tmf-index.html": "这份清单，Vivarcus eTMF 里已经内置",
    "template-audit-readiness-checklist.html": "这套自查，Vivarcus eTMF 里已经内置",
    "template-sop-framework.html": "这套流程，Vivarcus 里已经内置",
}
CTA_DESCS = {
    "template-tmf-index.html": "EDL 自动生成、文件自动归位到参考模型对应节点，比手工维护 Excel 清单快一个量级。",
    "template-audit-readiness-checklist.html": "完整性、及时性、质量三类指标实时可见，稽查前导出清单而不是突击整理。",
    "template-sop-framework.html": "流程、角色、时限在系统里结构化运转，SOP 与实操天然一致。",
}
DEFAULT_CTA_TITLE = "这些模板，Vivarcus eTMF 里已经内置"
DEFAULT_CTA_DESC = "表格可以直接使用；文件归位、版本受控和问题闭环，则可以交给系统持续管理。"

PAGE_GUIDES = {
    "template-monitoring-visit-report.html": (
        "CRA、CRO 项目经理",
        "常规或远程监查访视后",
        "避免只打勾不写抽查范围、发现项无责任人与时限",
        '<a href="template-mvr-example.html"><strong>先看填写示例与常见错误 TOP 10</strong></a> · <a href="template-icf-checklist.html">ICF 审核清单</a>',
    ),
    "template-mvr-example.html": (
        "CRA、PM、质量审核人员",
        "起草或审核 MVR 前",
        "避免用主观评价代替证据、遗留问题断链",
        '<a href="template-monitoring-visit-report.html">配套空白 MVR 模板</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-site-initiation-report.html": (
        "CRA、CRO 项目团队",
        "中心启动访视完成后",
        "避免培训签名、人员授权或必备文件缺项",
        '<a href="template-training-log.html">培训记录表</a> · <a href="template-tmf-index.html">TMF 文件清单</a>',
    ),
    "template-closeout-visit-report.html": (
        "CRA、PM、中心研究团队",
        "常规关中心或提前终止时",
        "避免数据、药物、伦理结题和文件归档未闭环",
        '<a href="template-audit-readiness-checklist.html">稽查准备清单</a> · <a href="template-tmf-index.html">TMF 文件清单</a>',
    ),
    "template-protocol-deviation-log.html": (
        "CRA、CRC、PI、项目经理",
        "方案偏离识别后及时登记",
        "避免只记录事件，不做分级、根因分析和 CAPA",
        '<a href="template-monitoring-visit-report.html">监查访视报告</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-icf-checklist.html": (
        "CRA、稽查员、ICF 审核人员",
        "ICF 定稿、监查抽查或稽查自查时",
        "避免版本混用、签署缺项和时间逻辑错误",
        '<a href="template-monitoring-visit-report.html">监查访视报告</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-tmf-index.html": (
        "申办方、CRA、TMF 管理人员",
        "建库、中心启动或完整性自查时",
        "避免文件缺项、责任不清和归档位置不一致",
        '<a href="tmf-reference.html">TMF 文件分类参考</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-sop-framework.html": (
        "QA、PM、流程负责人",
        "新建或修订 SOP 时",
        "避免职责不清、流程不可执行以及 SOP 与实操脱节",
        '<a href="template-training-log.html">培训记录表</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-audit-readiness-checklist.html": (
        "QA、PM、CRA、中心研究团队",
        "稽查或监管检查前 2–4 周",
        "避免临场突击、文件调阅困难和整改项未闭环",
        '<a href="template-icf-checklist.html">ICF 审核清单</a> · <a href="template-tmf-index.html">TMF 文件清单</a> · <a href="audit-findings.html">稽查发现分类对照表</a>',
    ),
    "template-training-log.html": (
        "研究团队及培训组织者",
        "方案、SOP、系统或中心启动培训时",
        "避免先执行后培训、文件升版后未重新培训",
        '<a href="template-site-initiation-report.html">中心启动访视报告</a> · <a href="template-sop-framework.html">SOP 框架</a>',
    ),
    "template-sae-report.html": (
        "PI、CRC、CRA、安全性团队",
        "研究中心向申办方报告 SAE 时",
        "避免报告超时、用症状代替诊断或缺少 PI 签署",
        '<a href="template-monitoring-visit-report.html">监查访视报告</a> · <a href="template-audit-readiness-checklist.html">稽查准备清单</a>',
    ),
    "template-site-initiation-checklist.html": (
        "CRA、CRO 项目团队",
        "中心启动前 1-2 周与启动访视当日",
        "避免培训走过场、参训签名事后补、授权分工未落地",
        '<a href="template-site-initiation-report.html">中心启动访视报告</a> · <a href="template-training-log.html">培训记录表</a>',
    ),
    "template-monitoring-visit-checklist.html": (
        "CRA",
        "每次常规监查访视前后",
        "避免抽查无证据、遗漏药物/安全/偏离核对项",
        '<a href="template-monitoring-visit-report.html">监查访视报告模板</a> · <a href="template-mvr-example.html">填写示例与常见错误</a>',
    ),
    "template-closeout-checklist.html": (
        "CRA、PM、中心研究团队",
        "关中心访视前 2 周与访视当日",
        "避免数据未清理、药物不平账、伦理未结题",
        '<a href="template-closeout-visit-report.html">关中心访视报告</a> · <a href="template-tmf-index.html">TMF 文件清单</a>',
    ),
}


# English metadata per page (prefix -> i18n-data.js keys). Source: hand-maintained, see js/i18n-data.js.
EN_META = {
    "template-monitoring-visit-report.html": ("tpl.mvr",
        "Monitoring Visit Report Template (MVR) — Free Clinical Trial Template | Vivarcus",
        "Monitoring visit report (MVR) template: visit information, informed consent, SDV, drug management, safety reporting, findings and CAPA — full field structure, with worked example and common error reference. Free to use.",
        "Template Library · Visit Report",
        "Monitoring Visit Report Template (MVR)",
        "The MVR is direct evidence of monitoring quality. This template covers visit information, open items, informed consent, SDV, drug management, safety reporting and finding closure — ready to copy and use."),
    "template-mvr-example.html": ("tpl.mvrex",
        "Monitoring Visit Report Worked Example & Top 10 Common Errors | Vivarcus",
        "MVR worked example: a complete filled-in sample (annotated line by line on why it is written this way) + TOP 10 common errors side by side + pre-submission self-check list.",
        "Template Library · Worked Example",
        "MVR Worked Example & Common Errors",
        "The blank template answers \"what fields exist\"; this page answers \"how to fill them in correctly\" — a fictional example annotated line by line, plus an auditor’s-eye view of common errors."),
    "template-site-initiation-report.html": ("tpl.sivr",
        "Site Initiation Visit Report Template (SIV) | Vivarcus",
        "Site initiation visit report template (SIV): training content checklist, attendance signature sheet, site qualification and facilities check, document readiness, open items and initiation conclusion.",
        "Template Library · Visit Report",
        "Site Initiation Visit Report Template (SIV)",
        "The initiation training signature sheet is a must-check audit item. This template covers training topic verification, attendance signatures, qualification/facility checks and the initiation conclusion — for on-site and remote initiations alike."),
    "template-closeout-visit-report.html": ("tpl.covr",
        "Close-out Visit Report Template (COV) | Vivarcus",
        "Close-out visit report template (COV): data cleanup verification, drug reconciliation, biospecimen handling, document archiving, ethics close-out notification and the archiving statement — item-by-item checks for audit hotspots.",
        "Template Library · Visit Report",
        "Close-out Visit Report Template (COV)",
        "Close-out is an audit hotspot: uncleaned data, unbalanced drug accountability and missing ethics close-out are the most common findings. This template verifies each item before the archiving statement is signed."),
    "template-protocol-deviation-log.html": ("tpl.pdlog",
        "Protocol Deviation Log Template | Vivarcus",
        "Protocol deviation log template (PD Log): deviation description, major-deviation determination reference, root cause analysis and CAPA, reporting records. PD logs are must-check audit documents — every entry must close the loop.",
        "Template Library · Log Form",
        "Protocol Deviation Log Template (PD Log)",
        "The common PD log audit problem is not \"no record\" but \"no analysis, no CAPA, no closure\". This template includes a major-deviation determination reference and management requirements."),
    "template-icf-checklist.html": ("tpl.icf",
        "Informed Consent Review Checklist Template (ICF) | Vivarcus",
        "Informed consent review checklist template (ICF): version and ethics approval verification, required elements, special situations (vulnerable groups/minors/witness), language readability and signature page checks.",
        "Template Library · Checklist",
        "Informed Consent Review Checklist Template (ICF)",
        "ICF issues carry the highest findings in inspections: mixed versions and consent signed after study procedures are the most common. This checklist covers required elements and special situations."),
    "template-tmf-index.html": ("tpl.tmfidx",
        "TMF Index Template (EDL) — Essential Documents Index | Vivarcus",
        "TMF index template (simplified EDL): essential document index organized by pre-study / ongoing / end-of-study stages, marking core items and responsible parties, with self-check methods.",
        "Template Library · Document List",
        "TMF Index Template (Simplified EDL)",
        "A three-stage essential document index for building the TMF/ISF structure, verifying site initiation documents and pre-audit completeness self-checks — with audit core items marked."),
    "template-sop-framework.html": ("tpl.sop",
        "SOP Framework Template: Standard Operating Procedure Writing Guide | Vivarcus",
        "SOP framework template: document control page, purpose/scope/responsibilities, flowchart, procedure steps, records and forms, revision history — with an SOP writing self-check list.",
        "Template Library · System Document",
        "SOP Framework Template",
        "One of the most common audit findings is \"SOP inconsistent with actual practice\". This template provides SOP structure standards and a pre-release self-check list."),
    "template-audit-readiness-checklist.html": ("tpl.audit",
        "Audit Readiness Checklist Template | Vivarcus",
        "Audit readiness checklist template: site-level (staff authorization/informed consent/ISF/data quality/safety/drug management) and project-level self-check lists, plus common audit finding TOPs and on-site cooperation preparation.",
        "Template Library · Checklist",
        "Audit Readiness Checklist Template",
        "In the 2-4 weeks before an audit, follow the three steps: site self-check → project consolidation → remediation closure. Print this list and tick each item — the checklist itself is valid evidence of audit preparation."),
    "template-training-log.html": ("tpl.train",
        "Clinical Trial Training Log Template | Vivarcus",
        "Clinical trial training log template: training basics, attendance signature sheet, effectiveness evaluation and make-up training arrangement. Training records are must-check audit items; signatures must be made in person on the spot.",
        "Template Library · Log Form",
        "Training Log Template",
        "Training records carry two must-check timeline logics: training before first task execution, and retraining after a document version upgrade. This template handles on-the-spot signatures, version linkage and due retraining."),
    "template-sae-report.html": ("tpl.sae",
        "SAE Report Template: Serious Adverse Event Form | Vivarcus",
        "SAE report template: subject information, event description, seriousness criteria, causality assessment, reporting timeline record (24 hours / 7 days / 15 days) and signatures. Does not replace official regulatory forms.",
        "Template Library · Report Template",
        "SAE Report Template (Serious Adverse Event Form)",
        "The three most critical things about SAE reporting: timeline (report within 24 hours of awareness), diagnosis (write the diagnosis, not the symptom) and signature (signed by the PI personally)."),
    "template-site-initiation-checklist.html": ("tpl.sivc",
        "Site Initiation Checklist Template | Vivarcus",
        "Site initiation checklist template: pre-initiation preparation (contract/ethics/staff/supplies), item-by-item training verification on initiation day, and pre-enrollment confirmation. Print and use; pairs with the initiation visit report.",
        "Template Library · Checklist",
        "Site Initiation Checklist Template",
        "The biggest initiation visit risks are going-through-the-motions training and backfilled signatures. One page: pre-initiation self-check + same-day item-by-item ticks + pre-enrollment confirmation."),
    "template-monitoring-visit-checklist.html": ("tpl.mvc",
        "Monitoring Visit Checklist Template | Vivarcus",
        "Monitoring visit checklist template: pre-visit preparation, in-visit item-by-item verification (ICF/inclusion-exclusion/SDV/drug/safety/deviations/ISF) and post-visit wrap-up. Pairs with the MVR template — tick it and copy into the report.",
        "Template Library · Checklist",
        "Monitoring Visit Checklist Template",
        "A three-stage (before/during/after) tick-style checklist that maps directly to the monitoring visit report sections — avoiding checkmarks without evidence."),
    "template-closeout-checklist.html": ("tpl.covc",
        "Close-out Checklist Template | Vivarcus",
        "Close-out checklist template: five categories item-by-item closure — data cleanup, drug reconciliation, biospecimens, document archiving and notifications. Self-check 2 weeks before the close-out visit to plug audit hotspots early.",
        "Template Library · Checklist",
        "Close-out Checklist Template",
        "Close-out is an audit hotspot: uncleaned data, drug accountability gaps and missing ethics close-out notifications are the most common. Self-check with this list 2 weeks before the close-out visit."),
}

# English CTA overrides (others fall back to EN default)
EN_CTA_TITLES = {
    "template-tmf-index.html": "This checklist is built into Vivarcus eTMF",
    "template-audit-readiness-checklist.html": "This self-check is built into Vivarcus eTMF",
    "template-sop-framework.html": "These processes are built into Vivarcus",
}
EN_CTA_DESCS = {
    "template-tmf-index.html": "Auto-generated EDLs, documents auto-filed to the right reference model nodes — an order of magnitude faster than maintaining an Excel checklist by hand.",
    "template-audit-readiness-checklist.html": "Completeness, timeliness and quality metrics are visible in real time — export the checklist before an audit instead of last-minute scrambling.",
    "template-sop-framework.html": "Processes, roles and timelines run structurally inside the system — SOPs and practice stay consistent by design.",
}
EN_DEFAULT_CTA_TITLE = "These templates are built into Vivarcus eTMF"
EN_DEFAULT_CTA_DESC = "The forms work as-is; filing, version control and issue closure can be handed to the system for ongoing management."

# English guide blocks (audience, timing, risk, related_html) — rendered into the en body JSON
EN_GUIDES = {
    "template-monitoring-visit-report.html": (
        "CRA, CRO project managers",
        "After routine or remote monitoring visits",
        "Avoid checkmarks without sampling scope, findings without owners or due dates",
        '<a href="template-mvr-example.html"><strong>See the worked example and TOP 10 common errors first</strong></a> · <a href="template-icf-checklist.html">ICF Review Checklist</a>',
    ),
    "template-mvr-example.html": (
        "CRA, PM, quality reviewers",
        "Before drafting or reviewing an MVR",
        "Avoid subjective judgment instead of evidence, broken chains on open items",
        '<a href="template-monitoring-visit-report.html">Companion blank MVR template</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-site-initiation-report.html": (
        "CRA, CRO project team",
        "After the site initiation visit",
        "Avoid missing training signatures, staff authorizations or essential documents",
        '<a href="template-training-log.html">Training Log</a> · <a href="template-tmf-index.html">TMF Index</a>',
    ),
    "template-closeout-visit-report.html": (
        "CRA, PM, site study team",
        "At routine close-out or early termination",
        "Avoid unclosed loops in data, drug, ethics close-out and archiving",
        '<a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a> · <a href="template-tmf-index.html">TMF Index</a>',
    ),
    "template-protocol-deviation-log.html": (
        "CRA, CRC, PI, project managers",
        "Promptly after a protocol deviation is identified",
        "Avoid recording events only, without grading, root cause analysis and CAPA",
        '<a href="template-monitoring-visit-report.html">Monitoring Visit Report</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-icf-checklist.html": (
        "CRA, auditors, ICF reviewers",
        "At ICF finalization, monitoring spot-checks or audit self-checks",
        "Avoid version mixing, missing signature elements and timeline logic errors",
        '<a href="template-monitoring-visit-report.html">Monitoring Visit Report</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-tmf-index.html": (
        "Sponsors, CRA, TMF managers",
        "When building the library, initiating a site or doing completeness self-checks",
        "Avoid missing documents, unclear responsibilities and inconsistent filing locations",
        '<a href="tmf-reference.html">TMF Reference</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-sop-framework.html": (
        "QA, PM, process owners",
        "When creating or revising an SOP",
        "Avoid unclear responsibilities, unexecutable processes and SOP-practice drift",
        '<a href="template-training-log.html">Training Log</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-audit-readiness-checklist.html": (
        "QA, PM, CRA, site study team",
        "2-4 weeks before an audit or regulatory inspection",
        "Avoid last-minute scrambling, hard-to-retrieve documents and unclosed remediation items",
        '<a href="template-icf-checklist.html">ICF Review Checklist</a> · <a href="template-tmf-index.html">TMF Index</a> · <a href="audit-findings.html">Audit Findings Classification</a>',
    ),
    "template-training-log.html": (
        "Study team and training organizers",
        "At protocol, SOP, system or site initiation training",
        "Avoid task execution before training and no retraining after document upgrades",
        '<a href="template-site-initiation-report.html">Site Initiation Visit Report</a> · <a href="template-sop-framework.html">SOP Framework</a>',
    ),
    "template-sae-report.html": (
        "PI, CRC, CRA, safety team",
        "When a site reports an SAE to the sponsor",
        "Avoid late reporting, symptom-for-diagnosis and missing PI signatures",
        '<a href="template-monitoring-visit-report.html">Monitoring Visit Report</a> · <a href="template-audit-readiness-checklist.html">Audit Readiness Checklist</a>',
    ),
    "template-site-initiation-checklist.html": (
        "CRA, CRO project team",
        "1-2 weeks before initiation and on initiation day",
        "Avoid superficial training, backfilled attendance signatures and unassigned authorizations",
        '<a href="template-site-initiation-report.html">Site Initiation Visit Report</a> · <a href="template-training-log.html">Training Log</a>',
    ),
    "template-monitoring-visit-checklist.html": (
        "CRA",
        "Before and after every routine monitoring visit",
        "Avoid evidence-less spot checks and missed drug/safety/deviation verification items",
        '<a href="template-monitoring-visit-report.html">Monitoring Visit Report Template</a> · <a href="template-mvr-example.html">Worked Example & Common Errors</a>',
    ),
    "template-closeout-checklist.html": (
        "CRA, PM, site study team",
        "2 weeks before the close-out visit and on the visit day",
        "Avoid uncleaned data, unbalanced drug accountability and unclosed ethics notifications",
        '<a href="template-closeout-visit-report.html">Close-out Visit Report</a> · <a href="template-tmf-index.html">TMF Index</a>',
    ),
}


def en_page_guide(out_file):
    audience, timing, risk, related = EN_GUIDES[out_file]
    return (
        '<div class="template-guide" aria-label="Template usage notes">'
        '<div class="template-guide-item"><strong>Who it’s for</strong><span>%s</span></div>'
        '<div class="template-guide-item"><strong>When to use</strong><span>%s</span></div>'
        '<div class="template-guide-item"><strong>Key pitfalls to avoid</strong><span>%s</span></div>'
        '</div><p class="template-related"><strong>Companion resources:</strong> %s</p>'
    ) % (audience, timing, risk, related)


def page_guide(out_file):
    audience, timing, risk, related = PAGE_GUIDES[out_file]
    return (
        '<div class="template-guide" aria-label="模板使用说明">'
        '<div class="template-guide-item"><strong data-i18n="tpl.common.who">适合谁</strong><span>%s</span></div>'
        '<div class="template-guide-item"><strong data-i18n="tpl.common.when">何时使用</strong><span>%s</span></div>'
        '<div class="template-guide-item"><strong data-i18n="tpl.common.avoid">重点避免</strong><span>%s</span></div>'
        '</div><p class="template-related"><strong data-i18n="tpl.common.relatedLabel">配套资源：</strong>%s</p>'
    ) % (audience, timing, risk, related)


# ---------- markdown subset converter ----------

INLINE_RE = [
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s):
    s = esc(s)
    for rx, rep in INLINE_RE:
        s = rx.sub(rep, s)
    return s


def is_table_row(line):
    return line.startswith("|") and line.rstrip().endswith("|")


def is_sep_row(line):
    cells = [c.strip().strip(":") for c in line.strip().strip("|").split("|")]
    return all(re.fullmatch(r"-+", c) for c in cells if c)


def table(rows):
    header = [inline(c.strip()) for c in rows[0].strip().strip("|").split("|")]
    body = rows[2:]
    html = ['<div class="template-scroll"><table class="template-table"><thead><tr>',
            "".join("<th>%s</th>" % c for c in header), "</tr></thead><tbody>"]
    for r in body:
        cells = [inline(c.strip()) for c in r.strip().strip("|").split("|")]
        html.append("<tr>" + "".join("<td>%s</td>" % c for c in cells) + "</tr>")
    html.append("</tbody></table></div>")
    return "\n".join(html)


def convert(md_text):
    lines = md_text.split("\n")
    out, p_buf, note_buf = [], [], []
    list_items = []
    list_tag = "ul"
    i = 0

    def flush_p():
        nonlocal p_buf
        if p_buf:
            out.append("<p>" + "<br />".join(inline(b) for b in p_buf) + "</p>")
            p_buf = []

    def flush_note():
        nonlocal note_buf
        if note_buf:
            out.append('<aside class="template-note">'
                       + "".join("<p>%s</p>" % inline(b) for b in note_buf)
                       + "</aside>")
            note_buf = []

    def flush_list():
        nonlocal list_items, list_tag
        if list_items:
            out.append("<%s>" % list_tag
                       + "".join("<li>%s</li>" % inline(li) for li in list_items)
                       + "</%s>" % list_tag)
            list_items = []
        list_tag = "ul"

    def flush_all():
        flush_p(); flush_note(); flush_list()

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()

        if i == 0 and stripped.startswith("# "):
            i += 1
            continue

        if not stripped or stripped == "---":
            flush_all()
            i += 1
            continue

        # blockquote (note block: 版本/适用/免责 or 提示)
        if stripped.startswith(">"):
            flush_p(); flush_list()
            note_buf.append(stripped.lstrip(">").strip())
            i += 1
            continue

        # headings (## -> h2, ### -> h3, #### -> h4)
        m = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if m:
            flush_all()
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            i += 1
            continue

        # table
        if is_table_row(stripped) and i + 1 < len(lines) and is_sep_row(lines[i + 1]):
            flush_all()
            rows = [stripped]
            i += 1
            while i < len(lines) and is_table_row(lines[i].rstrip()):
                rows.append(lines[i].rstrip())
                i += 1
            out.append(table(rows))
            continue

        # lists
        m = re.match(r"^(\s*)([-*]|\d+[.)])\s+(.*)$", line)
        if m and m.group(3):
            flush_p(); flush_note()
            new_tag = "ul" if m.group(2) in ("-", "*") else "ol"
            if new_tag != list_tag:
                flush_list()
                list_tag = new_tag
            list_items.append(m.group(1) + m.group(3))
            i += 1
            continue

        # paragraph
        flush_note(); flush_list()
        p_buf.append(stripped)
        i += 1

    flush_all()
    return "\n".join(out)


MD_LINK_MAP = {src: out for src, out, *_ in PAGES}


def rewrite_links(body):
    """Rewire intra-template markdown links (e.g. 01-...md) to their web pages."""
    def repl(m):
        target = m.group(1)
        return 'href="%s"' % MD_LINK_MAP.get(target, target)
    return re.sub(r'href="([^"]+\.md)"', repl, body)


def _js_json(s):
    import json
    return json.dumps(s, ensure_ascii=False)


def build_page(spec):
    src, out_file, title, desc, eyebrow, hero, subtitle = spec
    with open(os.path.join(MD_DIR, src), encoding="utf-8") as f:
        body = rewrite_links(convert(f.read()))
    body = body.replace("v0.1 草稿", "参考版")
    body = re.sub(
        r"｜<strong>验证单品</strong>：本篇是模板库的测试样本，发布试水后按数据决定是否为其余模板制作同类增值内容",
        "",
        body,
    )

    prefix, en_title, en_desc, en_eyebrow, en_hero, en_subtitle = EN_META[out_file]
    en_src = src[:-3] + ".en.md"
    with open(os.path.join(MD_DIR, en_src), encoding="utf-8") as f:
        en_body = rewrite_links(convert(f.read()))
    en_body = en_body.replace("v0.1 草稿", "Reference version")
    en_guide = en_page_guide(out_file)

    html = HEAD.replace("@@TITLE@@", title).replace("@@DESC@@", desc) \
        .replace("@@FILE@@", out_file).replace("@@EYEBROW@@", eyebrow) \
        .replace("@@HERO@@", hero).replace("@@SUBTITLE@@", subtitle) \
        .replace("@@I18N@@", prefix) \
        .replace("@@GUIDE@@", page_guide(out_file)) \
        .replace("@@BODY@@", body) \
        .replace("@@GUIDE_EN_JSON@@", _js_json(en_guide)) \
        .replace("@@BODY_EN_JSON@@", _js_json(en_body))
    html += CTA.replace("@@CTA_TITLE@@", CTA_TITLES.get(out_file, DEFAULT_CTA_TITLE)) \
        .replace("@@CTA_DESC@@", CTA_DESCS.get(out_file, DEFAULT_CTA_DESC)) \
        .replace("@@I18N@@", prefix)
    html += FOOT
    path = os.path.join(OUT_DIR, out_file)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def main():
    for spec in PAGES:
        path = build_page(spec)
        size = os.path.getsize(path)
        print("%-55s %8d bytes" % (os.path.basename(path), size))


if __name__ == "__main__":
    main()
