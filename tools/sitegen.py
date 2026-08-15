#!/usr/bin/env python3
"""Shared skeleton + markdown converter for generated content pages (zh-only).

Used by build_regulations.py (法规库). build_templates.py currently keeps its own
copy of the skeleton (pending merge once parallel edits settle); the header/footer
chrome here mirrors the current site state, including the 模板库 nav entry.
"""
import re

HEAD = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="@@DESC@@" />
  <title>@@TITLE@@</title>
  <link rel="canonical" href="https://vivarcus.com/@@FILE@@" />
  <link rel="alternate" hreflang="zh-CN" href="https://vivarcus.com/@@FILE@@" />
  <link rel="alternate" hreflang="x-default" href="https://vivarcus.com/@@FILE@@" />
  <meta property="og:type" content="website" />
  <meta property="og:site_name" content="Vivarcus" />
  <meta property="og:url" content="https://vivarcus.com/@@FILE@@" />
  <meta property="og:title" content="@@TITLE@@" />
  <meta property="og:description" content="@@DESC@@" />
  <meta property="og:locale" content="zh_CN" />
  <meta property="og:image" content="https://vivarcus.com/assets/og-image.png" />
  <meta property="og:image:alt" content="@@TITLE@@" />
  <link rel="icon" type="image/svg+xml" href="assets/favicon.svg" />
  <link rel="stylesheet" href="css/icons.css" />
  <link rel="stylesheet" href="css/style.css" />
  <script src="js/i18n-data.js"></script>
  <script src="js/seo-head.js"></script>
  <style>
    .content-wrap { padding: 1.5rem 0 3rem; }
    .content-inner { max-width: 56rem; }
    .content-inner h2 { margin: 2.2rem 0 0.8rem; font-size: 1.25rem; }
    .content-inner h3 { margin: 1.8rem 0 0.6rem; font-size: 1.08rem; }
    .content-inner h4 { margin: 1.4rem 0 0.5rem; font-size: 1rem; }
    .content-inner p { line-height: 1.8; }
    .content-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; margin: 0.9rem 0 1.4rem; }
    .content-table th, .content-table td { text-align: left; padding: 0.55rem 0.8rem; border-top: 1px solid var(--border, #d8dde4); vertical-align: top; }
    .content-table th { font-size: 0.8rem; opacity: 0.65; font-weight: 600; white-space: nowrap; }
    .content-scroll { overflow-x: auto; -webkit-overflow-scrolling: touch; }
    .content-note { font-size: 0.88rem; opacity: 0.85; border-left: 3px solid var(--accent, #2563eb); padding: 0.6rem 1rem; margin: 1.2rem 0; background: var(--bg-soft, #f6f8fa); border-radius: 0 6px 6px 0; }
    .content-note p { margin: 0.25rem 0; }
    .content-back { margin: 1.2rem 0 0; font-size: 0.9rem; }
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
          <i class="ic ic--book-open" aria-hidden="true"></i>
          <span>@@EYEBROW@@</span>
        </span>
        <h1 class="page-hero-title">@@HERO@@</h1>
        <p class="page-hero-subtitle">@@SUBTITLE@@</p>
      </div>
    </section>

    <section class="section content-wrap">
      <div class="container content-inner">
@@BODY@@
      </div>
    </section>
"""

CTA = """    <section class="cta-section" data-reveal>
      <div class="container">
        <div class="cta-content">
          <h2>@@CTA_TITLE@@</h2>
          <p>@@CTA_DESC@@</p>
          <div class="cta-actions">
            <a href="trial.html" class="btn btn-primary btn-lg">
              <span data-i18n="common.nav.trial">试用申请</span>
              <i class="ic ic--arrow-right" aria-hidden="true"></i>
            </a>
            <a href="@@CTA_SECONDARY_HREF@@" class="btn btn-outline btn-lg">@@CTA_SECONDARY_LABEL@@</a>
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
          <a href="ich-e6r3.html" data-i18n="common.footer.regulations">法规库</a>
          <a href="release-26r3.html" data-i18n="common.footer.release">发布说明</a>
          <a href="help/zh/index.html" data-lang-href-zh="help/zh/index.html" data-lang-href-en="help/en/index.html" data-i18n="common.footer.help">帮助中心</a>
          <a href="products.html" data-i18n="common.footer.productsPage">产品介绍</a>
          <a href="about.html" data-i18n="common.footer.about">关于我们</a>
        </div>

        <div class="footer-col">
          <h4 data-i18n="common.footer.links">链接</h4>
          <a href="trial.html" data-i18n="common.footer.trial">试用申请</a>
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
    html = ['<div class="content-scroll"><table class="content-table"><thead><tr>',
            "".join("<th>%s</th>" % c for c in header), "</tr></thead><tbody>"]
    for r in body:
        cells = [inline(c.strip()) for c in r.strip().strip("|").split("|")]
        html.append("<tr>" + "".join("<td>%s</td>" % c for c in cells) + "</tr>")
    html.append("</tbody></table></div>")
    return "\n".join(html)


def convert(md_text):
    """Convert the supported markdown subset to HTML (same rules as build_templates)."""
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
            out.append('<aside class="content-note">'
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

        if stripped.startswith(">"):
            flush_p(); flush_list()
            note_buf.append(stripped.lstrip(">").strip())
            i += 1
            continue

        m = re.match(r"^(#{2,4})\s+(.*)$", stripped)
        if m:
            flush_all()
            level = len(m.group(1))
            out.append("<h%d>%s</h%d>" % (level, inline(m.group(2)), level))
            i += 1
            continue

        if is_table_row(stripped) and i + 1 < len(lines) and is_sep_row(lines[i + 1]):
            flush_all()
            rows = [stripped]
            i += 1
            while i < len(lines) and is_table_row(lines[i].rstrip()):
                rows.append(lines[i].rstrip())
                i += 1
            out.append(table(rows))
            continue

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

        flush_note(); flush_list()
        p_buf.append(stripped)
        i += 1

    flush_all()
    return "\n".join(out)


def render_page(meta, body, cta_title, cta_desc, cta_secondary_href, cta_secondary_label):
    """meta: dict(title, desc, file, eyebrow, hero, subtitle)"""
    html = HEAD.replace("@@TITLE@@", meta["title"]).replace("@@DESC@@", meta["desc"]) \
        .replace("@@FILE@@", meta["file"]).replace("@@EYEBROW@@", meta["eyebrow"]) \
        .replace("@@HERO@@", meta["hero"]).replace("@@SUBTITLE@@", meta["subtitle"]) \
        .replace("@@BODY@@", body)
    html += CTA.replace("@@CTA_TITLE@@", cta_title).replace("@@CTA_DESC@@", cta_desc) \
        .replace("@@CTA_SECONDARY_HREF@@", cta_secondary_href) \
        .replace("@@CTA_SECONDARY_LABEL@@", cta_secondary_label)
    html += FOOT
    return html
