#!/usr/bin/env python3
"""Vivarcus Help Center static site builder.

Zero-dependency (Python 3 stdlib only) build script:
  markdown sources in  help-src/**/*.{zh,en}.md
  config in          help-src/config.json
  templates in       help-src/templates/*.html
generates:
  website/help/{zh,en}/**/*.html     (static pages, committed to git)
  website/help/search-index.{zh,en}.json
  website/sitemap.xml                (marketing pages + help pages, hreflang pairs)

Run: make website-help-build   (or: cd website && python3 tools/build_help.py)
"""

import html
import json
import re
from pathlib import Path
from string import Template

ROOT = Path(__file__).resolve().parent.parent  # website/
SRC = ROOT / "help-src"
TPL = SRC / "templates"
OUT = ROOT / "help"

LANGS = ["zh", "en"]
LANG_CODE = {"zh": "zh-CN", "en": "en-US"}
OG_LOCALE = {"zh": "zh_CN", "en": "en_US"}
NOTE_LABEL = {"zh": "注意", "en": "Note"}


# ---------------------------------------------------------------- markdown --

def inline(text: str, rel_prefix: str) -> str:
    """Inline markup: **bold**, `code`, [text](url). Escapes HTML first."""
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", lambda m: (
        f'<a href="{rewrite_url(m.group(2), rel_prefix)}">{m.group(1)}</a>'
    ), text)
    return text


def rewrite_url(url: str, rel_prefix: str) -> str:
    """Resolve md link targets for the current page depth.

    #anchor          -> unchanged
    http(s)://, mailto: -> unchanged
    /site-root-path  -> rel_prefix + path (marketing pages etc.)
    bare relative    -> unchanged (resolves within the current language dir)
    """
    url = url.strip()
    if url.startswith("#") or re.match(r"^https?://", url) or url.startswith("mailto:"):
        return url
    if url.startswith("/"):
        return rel_prefix + url
    return url


def _slug(text: str, counter: list) -> str:
    s = re.sub(r"[^\w\- ]", "", text.strip().lower())
    s = re.sub(r"\s+", "-", s).strip("-")
    if s:
        return s
    counter[0] += 1
    return f"h{counter[0]}"


def render_md(body: str, lang: str, rel_prefix: str):
    """Render the restricted markdown subset. Returns (html, toc_list, h2_list).

    Subset: ##/### headings, paragraphs, -/*/1. lists (one nesting level),
    | tables, > note blocks, standalone <img> passthrough, inline markup.
    """
    out = []
    toc = []  # (id, text) for h2
    headings = []  # h2 texts for the search index
    counter = [0]
    para = []
    note = []  # current note block lines
    list_buf = []  # (indent, ordered, inline_html)
    table_buf = []  # raw | lines

    def flush_para():
        if para:
            out.append("<p>" + inline(" ".join(para), rel_prefix) + "</p>")
            para.clear()

    def flush_list():
        if not list_buf:
            return
        parts = [f"<{'ol' if list_buf[0][1] else 'ul'}>"]
        open_lis = []  # 0 top, 1 nested
        for indent, ordered, text in list_buf:
            level = 1 if indent > 0 else 0
            while open_lis and open_lis[-1] > level:
                popped = open_lis.pop()
                parts.append("</ul></li>" if popped == 1 else "</li>")
            parts.append("<li>" + text)
            open_lis.append(level)
            if level == 1:
                parts.append("<ul>")
        while open_lis:
            popped = open_lis.pop()
            parts.append("</ul></li>" if popped == 1 else "</li>")
        parts.append("</ol>" if list_buf[0][1] else "</ul>")
        out.append("".join(parts))
        list_buf.clear()

    def flush_table():
        if not table_buf:
            return
        rows = []
        for line in table_buf:
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
        if len(rows) >= 2 and all(re.match(r"^:?-{2,}:?$", c) for c in rows[1]):
            head, body = rows[0], rows[2:]
        else:
            head, body = [], rows
        h = ""
        if head:
            h = "<thead><tr>" + "".join(
                f"<th>{inline(c, rel_prefix)}</th>" for c in head) + "</tr></thead>"
        b = "<tbody>" + "".join(
            "<tr>" + "".join(f"<td>{inline(c, rel_prefix)}</td>" for c in r) + "</tr>"
            for r in body) + "</tbody>"
        out.append('<div class="help-table-wrap"><table>' + h + b + "</table></div>")
        table_buf.clear()

    def flush_note():
        if not note:
            return
        paras = [p for p in ("\n".join(note)).split("\n\n") if p.strip()]
        inner = "".join(
            f"<p>{inline(re.sub(r'\s+', ' ', p).strip(), rel_prefix)}</p>" for p in paras)
        out.append(
            f'<div class="help-note"><p class="help-note__label">{NOTE_LABEL[lang]}</p>{inner}</div>'
        )
        note.clear()

    for raw in body.split("\n"):
        line = raw.rstrip()

        m = re.match(r"^(#{2,3})\s+(.+)$", line)
        if m:
            flush_para(); flush_list(); flush_table(); flush_note()
            level = len(m.group(1))
            sid = _slug(m.group(2), counter)
            out.append(f'<h{level} id="{sid}">{inline(m.group(2), rel_prefix)}</h{level}>')
            if level == 2:
                toc.append((sid, m.group(2)))
                headings.append(m.group(2))
            continue

        if line.startswith(">"):
            flush_para(); flush_list(); flush_table()
            note.append(line.lstrip(">").strip())
            continue

        if line.lstrip().startswith("|") and line.strip().endswith("|"):
            flush_para(); flush_list(); flush_note()
            table_buf.append(line)
            continue

        m = re.match(r"^(\s*)([-*+]|\d+\.)\s+(.+)$", line)
        if m:
            flush_para(); flush_table(); flush_note()
            indent = len(m.group(1))
            ordered = bool(re.match(r"\d+\.", m.group(2)))
            list_buf.append((indent, ordered, inline(m.group(3), rel_prefix)))
            continue

        m = re.match(r"^\s*<img\s[^>]+>\s*$", line)
        if m:
            flush_para(); flush_list(); flush_table(); flush_note()
            tag = rewrite_url(m.group(0).strip(), rel_prefix)
            tag = re.sub(r"\bsrc=\"([^\"]+)\"", lambda mm: f'src="{rewrite_url(mm.group(1), rel_prefix)}"', tag)
            if "loading=" not in tag:
                tag = tag[:-1] + ' loading="lazy">'
            out.append(tag)
            continue

        if not line.strip():
            flush_para(); flush_list(); flush_table(); flush_note()
            continue

        flush_list(); flush_table(); flush_note()
        para.append(line.strip())

    flush_para(); flush_list(); flush_table(); flush_note()
    return "\n".join(out), toc, headings


def parse_frontmatter(text: str):
    """Parse '---' delimited frontmatter. Supports key: value and '  - item' lists."""
    meta = {}
    if not text.startswith("---"):
        return meta, text
    end = text.find("\n---", 3)
    if end == -1:
        return meta, text
    key = None
    for line in text[3:end].strip().split("\n"):
        s = line.strip()
        if s.startswith("- ") and key:
            meta.setdefault(key, []).append(s[2:].strip())
        elif ":" in s:
            k, v = s.split(":", 1)
            key = k.strip()
            meta[key] = v.strip() if v.strip() else []
    return meta, text[end + 4:].lstrip("\n")


# ---------------------------------------------------------------- article io --

def load_articles(cfg):
    """Load all article sources. Returns {app: {slug: {lang: {meta, body}}}}."""
    apps = {}
    for app in cfg["apps"]:
        key = app["key"]
        apps[key] = {}
        appdir = SRC / key
        if not appdir.is_dir():
            continue
        for zh_path in sorted(appdir.glob("*.zh.md")):
            slug = zh_path.stem[:-3]  # strip ".zh"
            apps[key][slug] = {}
            for lang in LANGS:
                p = appdir / f"{slug}.{lang}.md"
                if not p.is_file():
                    print(f"  WARN: missing {p.relative_to(ROOT)}")
                    continue
                meta, body = parse_frontmatter(p.read_text(encoding="utf-8"))
                meta.setdefault("title", slug)
                meta.setdefault("description", "")
                meta.setdefault("last_updated", "2026-08-15")
                meta.setdefault("related", [])
                apps[key][slug][lang] = {"meta": meta, "body": body}
    return apps


# ------------------------------------------------------------- html fragments --

def header_html(lang, ui, rel_prefix, site_home, help_home_rel, switch_url):
    switch_label = ui["lang_switch"]
    other_code = LANG_CODE["en" if lang == "zh" else "zh"]
    return f"""<header class="help-header">
  <div class="help-header__inner">
    <a href="{site_home}" class="help-header__brand" aria-label="Vivarcus">
      <span class="help-header__logo-dark">Vivar</span><span class="help-header__logo-accent">cus</span>
    </a>
    <span class="help-header__divider" aria-hidden="true">/</span>
    <a href="{help_home_rel}" class="help-header__help-label">{ui['help_center']}</a>
    <div class="help-header__actions">
      <a href="{rel_prefix}/{'trial.html?lang=en' if lang == 'en' else 'trial.html'}" class="help-header__trial">{ui['trial']}</a>
      <a href="{switch_url}" class="help-header__lang" hreflang="{other_code}">{switch_label}</a>
    </div>
  </div>
</header>"""


def footer_html(lang, ui, rel_prefix, site_home):
    return f"""<footer class="help-footer">
  <div class="help-footer__inner">
    <span class="help-footer__copyright">© 2026 Vivarcus</span>
    <nav class="help-footer__nav">
      <a href="{rel_prefix}/{'trial.html?lang=en' if lang == 'en' else 'trial.html'}">{ui['trial']}</a>
      <a href="{site_home}">{ui['back_to_site']}</a>
    </nav>
  </div>
</footer>"""


def item_href(item, lang):
    """Sidebar/app-index link for a config item.

    anchor may be a plain string (slugged like a heading) or a per-language
    dict {"zh": ..., "en": ...}; the text must match the target heading text.
    """
    href = item["article"] + ".html"
    anchor = item.get("anchor")
    if anchor:
        text = anchor.get(lang, anchor) if isinstance(anchor, dict) else anchor
        href += "#" + _slug(text, [0])
    return href


def sidebar_html(app, lang, ui, current_slug):
    parts = [f'<p class="help-sidebar__title"><a href="index.html">{app["name"][lang]}</a></p>',
             '<nav class="help-sidebar__nav">']
    for group in app["groups"]:
        open_attr = " open" if any(
            i.get("article") == current_slug for i in group["items"]) else ""
        parts.append(f'<details class="help-sidebar__group"{open_attr}>')
        parts.append(f"<summary>{html.escape(group['label'][lang])}</summary>")
        parts.append("<ul>")
        for item in group["items"]:
            label = html.escape(item["label"][lang])
            if item.get("article"):
                href = item_href(item, lang)
                active = ' class="active"' if item["article"] == current_slug else ""
                parts.append(f'<li><a href="{href}"{active}>{label}</a></li>')
            else:
                parts.append(
                    f'<li class="help-sidebar__todo">{label}'
                    f'<span class="help-tag-todo">{ui["coming_soon"]}</span></li>'
                )
        parts.append("</ul></details>")
    parts.append("</nav>")
    return "\n".join(parts)


def groups_html(app, lang, ui):
    parts = []
    for group in app["groups"]:
        parts.append(f'<section class="help-group"><h2>{html.escape(group["label"][lang])}</h2><ul>')
        for item in group["items"]:
            label = html.escape(item["label"][lang])
            if item.get("article"):
                href = item_href(item, lang)
                parts.append(f'<li><a href="{href}">{label}</a></li>')
            else:
                parts.append(
                    f'<li class="help-group__todo">{label}'
                    f'<span class="help-tag-todo">{ui["coming_soon"]}</span></li>'
                )
        parts.append("</ul></section>")
    return "\n".join(parts)


def app_cards_html(cfg, lang):
    icons = {"etmf": "ic--folder-open", "ctms": "ic--chart-line"}
    parts = []
    for app in cfg["apps"]:
        parts.append(
            f'<a class="help-app-card" href="{app["key"]}/index.html">'
            f'<span class="help-app-card__icon"><i class="ic {icons[app["key"]]}" aria-hidden="true"></i></span>'
            f'<span class="help-app-card__body"><span class="help-app-card__name">{app["name"][lang]}</span>'
            f'<span class="help-app-card__tagline">{html.escape(app["tagline"][lang])}</span></span>'
            f"</a>"
        )
    return "\n".join(parts)


def faq_html(lang, rel_prefix):
    p = SRC / f"faq.{lang}.md"
    if not p.is_file():
        return ""
    parts = []
    for block in p.read_text(encoding="utf-8").strip().split("\n## "):
        lines = block.strip().split("\n")
        question = lines[0].lstrip("# ").strip()
        body = "\n".join(lines[1:]).strip()
        body_html, _, _ = render_md(body, lang, rel_prefix)
        parts.append(
            f'<details class="help-faq__item"><summary>{inline(question, rel_prefix)}</summary>'
            f'<div class="help-faq__body">{body_html}</div></details>'
        )
    return "\n".join(parts)


def page_vars(lang, segments, cfg, ui, extra):
    """segments: path segments relative to site root, e.g. ['help','zh','etmf','overview.html']."""
    rel_prefix = ("../" * (len(segments) - 1)).rstrip("/")
    url = "/".join(segments)
    sibling = list(segments)
    sibling[1] = "en" if lang == "zh" else "zh"
    sibling_url = "/".join(sibling)
    site_home = rel_prefix + ("" if lang == "zh" else "?lang=en")
    return dict(
        base_url=cfg["site"]["base_url"],
        lang=lang,
        html_lang=LANG_CODE[lang],
        og_locale=OG_LOCALE[lang],
        self_lang_code=LANG_CODE[lang],
        other_lang_code=LANG_CODE["en" if lang == "zh" else "zh"],
        asset_rel=rel_prefix,
        canonical_url=cfg["site"]["base_url"] + "/" + url,
        alternate_url=cfg["site"]["base_url"] + "/" + sibling_url,
        x_default_url=cfg["site"]["base_url"] + "/" + "/".join(
            sibling if lang != "zh" else segments),
        help_home_rel=rel_prefix + f"/help/{lang}/index.html",
        switch_url=rel_prefix + "/" + sibling_url,
        **{f"ui_{k}": v for k, v in ui[lang].items()},
        **extra,
    )


def render_template(name: str, vars_) -> str:
    tpl = (TPL / name).read_text(encoding="utf-8")
    return Template(tpl).substitute(**vars_)


# -------------------------------------------------------------------- build --

def build():
    cfg = json.loads((SRC / "config.json").read_text(encoding="utf-8"))
    apps = load_articles(cfg)
    ui = cfg["ui"]
    base = cfg["site"]["base_url"]

    # ---- help home (per lang) ----
    for lang in LANGS:
        segments = ["help", lang, "index.html"]
        vars_ = page_vars(lang, segments, cfg, ui, {
            "title": cfg["home"][lang]["title"],
            "description": cfg["home"][lang]["description"],
            "home_description": cfg["home"][lang]["description"],
        })
        site_home = vars_["asset_rel"] + ("?lang=en" if lang == "en" else "")
        header = header_html(lang, ui[lang], vars_["asset_rel"], site_home, vars_["help_home_rel"], vars_["switch_url"])
        footer = footer_html(lang, ui[lang], vars_["asset_rel"], site_home)
        vars_.update(header_html=header, footer_html=footer,
                     app_cards=app_cards_html(cfg, lang), faq_html=faq_html(lang, vars_["asset_rel"]))
        page = render_template("help-home.html", vars_)
        out_path = OUT / lang / "index.html"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")
        print(f"  wrote {out_path.relative_to(ROOT)}")

    # ---- app indexes + articles ----
    for app in cfg["apps"]:
        app_key = app["key"]
        for lang in LANGS:
            segments = ["help", lang, app_key, "index.html"]
            vars_ = page_vars(lang, segments, cfg, ui, {
                "app_name": app["name"][lang],
                "app_description": app["tagline"][lang],
                "app_tagline": app["tagline"][lang],
            })
            other = next(a for a in cfg["apps"] if a["key"] != app_key)
            cross = (f'{html.escape(app["cross_hint"][lang])} '
                     f'<a href="../{other["key"]}/index.html">{other["name"][lang]}</a>')
            vars_.update(
                header_html=header_html(lang, ui[lang], vars_["asset_rel"],
                                        vars_["asset_rel"] + ("?lang=en" if lang == "en" else ""),
                                        vars_["help_home_rel"], vars_["switch_url"]),
                footer_html=footer_html(lang, ui[lang], vars_["asset_rel"],
                                        vars_["asset_rel"] + ("?lang=en" if lang == "en" else "")),
                groups_html=groups_html(app, lang, ui[lang]),
                cross_hint_html=cross,
            )
            page = render_template("app-index.html", vars_)
            out_path = OUT / lang / app_key / "index.html"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_text(page, encoding="utf-8")
            print(f"  wrote {out_path.relative_to(ROOT)}")

            # articles
            for slug, langs in sorted(apps.get(app_key, {}).items()):
                if lang not in langs:
                    continue
                meta = langs[lang]["meta"]
                segments = ["help", lang, app_key, f"{slug}.html"]
                vars_ = page_vars(lang, segments, cfg, ui, {
                    "app_name": app["name"][lang],
                    "title": meta["title"],
                    "description": meta["description"],
                    "last_updated": meta["last_updated"],
                })
                content_html, toc, headings = render_md(langs[lang]["body"], lang, vars_["asset_rel"])
                toc_html = "\n".join(f'<a href="#{sid}">{inline(t, "./")}</a>' for sid, t in toc)
                related = []
                for rel_slug in meta.get("related", []):
                    if rel_slug in apps.get(app_key, {}) and lang in apps[app_key][rel_slug]:
                        rel_title = apps[app_key][rel_slug][lang]["meta"]["title"]
                        related.append(
                            f'<li><a href="{rel_slug}.html">{html.escape(rel_title)}</a></li>')
                related_html = ""
                if related:
                    related_html = (f'<section class="help-related"><h2>{ui[lang]["related_articles"]}</h2>'
                                    f"<ul>{''.join(related)}</ul></section>")
                site_home = vars_["asset_rel"] + ("?lang=en" if lang == "en" else "")
                vars_.update(
                    content_html=content_html,
                    toc_html=toc_html,
                    related_html=related_html,
                    app_index_rel=f"index.html",
                    header_html=header_html(lang, ui[lang], vars_["asset_rel"], site_home,
                                            vars_["help_home_rel"], vars_["switch_url"]),
                    footer_html=footer_html(lang, ui[lang], vars_["asset_rel"], site_home),
                    sidebar_html=sidebar_html(app, lang, ui[lang], slug),
                )
                page = render_template("article.html", vars_)
                out_path = OUT / lang / app_key / f"{slug}.html"
                out_path.write_text(page, encoding="utf-8")
                print(f"  wrote {out_path.relative_to(ROOT)}")

    # ---- search indexes ----
    for lang in LANGS:
        index = []
        for app in cfg["apps"]:
            for slug, langs in sorted(apps.get(app["key"], {}).items()):
                if lang not in langs:
                    continue
                meta = langs[lang]["meta"]
                _, _, headings = render_md(langs[lang]["body"], lang, "./")
                index.append({
                    "app": app["key"],
                    "app_label": app["name"][lang],
                    "slug": slug,
                    "title": meta["title"],
                    "description": meta["description"],
                    "headings": headings,
                })
        p = OUT / f"search-index.{lang}.json"
        p.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"  wrote {p.relative_to(ROOT)} ({len(index)} articles)")

    # ---- sitemap.xml ----
    build_sitemap(cfg, apps)
    print("  wrote sitemap.xml")


def build_sitemap(cfg, apps):
    def page_entry(loc_zh, loc_en, lastmod, changefreq, priority):
        return f"""  <url>
    <loc>{loc_zh}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
    <xhtml:link rel="alternate" hreflang="zh-CN" href="{loc_zh}" />
    <xhtml:link rel="alternate" hreflang="en-US" href="{loc_en}" />
    <xhtml:link rel="alternate" hreflang="x-default" href="{loc_zh}" />
  </url>"""

    base = cfg["site"]["base_url"]
    entries = []
    for p in cfg["marketing_pages"]:
        loc = base + p["loc"]
        loc_en = loc + ("?lang=en" if "?" not in loc else "&lang=en")
        entries.append(page_entry(loc, loc_en, p["lastmod"], p["changefreq"], p["priority"]))

    help_pages = []  # (zh_path, en_path, lastmod, changefreq, priority)
    for lang in LANGS:
        home_lastmod = "2026-08-15"
        help_pages.append((f"{base}/help/{lang}/index.html", home_lastmod, "weekly", "0.8"))
    for app in cfg["apps"]:
        for lang in LANGS:
            help_pages.append((f"{base}/help/{lang}/{app['key']}/index.html",
                               app.get("lastmod", "2026-08-15"), "weekly", "0.6"))
        for slug, langs in sorted(apps.get(app["key"], {}).items()):
            lastmod = langs.get("zh", langs.get("en", {}))["meta"]["last_updated"]
            for lang in LANGS:
                help_pages.append((f"{base}/help/{lang}/{app['key']}/{slug}.html",
                                   lastmod, "weekly", "0.7"))

    # pair zh/en alternates
    zh_pages = [e for e in help_pages if "/help/zh/" in e[0]]
    en_pages = [e for e in help_pages if "/help/en/" in e[0]]
    for zh_entry, en_entry in zip(zh_pages, en_pages):
        loc_zh, lastmod, freq, prio = zh_entry
        loc_en = en_entry[0]
        entries.append(page_entry(loc_zh, loc_en, lastmod, freq, prio))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
           '        xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
           + "\n".join(entries) + "\n</urlset>\n")
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")


if __name__ == "__main__":
    print("building help center…")
    build()
    print("done.")
