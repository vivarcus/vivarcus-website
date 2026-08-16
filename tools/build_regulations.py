#!/usr/bin/env python3
"""Generate regulation library pages from docs/marketing/regulations/*.md.

Run from repo root:  python3 website/tools/build_regulations.py
Content source of truth: docs/marketing/regulations/*.md (+ .en.md English twins)
Generated pages: website/*.html (bilingual: zh body inline, en body embedded as
JSON and swapped at runtime; hero/meta/CTA keys live in js/i18n-data.js)
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitegen  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MD_DIR = os.path.join(ROOT, "docs", "marketing", "regulations")
OUT_DIR = os.path.join(ROOT, "website")

PAGES = [
    {
        "src": "ich-e6r3-essentials.md",
        "src_en": "ich-e6r3-essentials.en.md",
        "file": "ich-e6r3.html",
        "prefix": "ichr3",
        "title": "ICH E6(R3) 中文要点：11 条原则与对临床运营的影响 | Vivarcus",
        "desc": "ICH E6(R3) GCP 中文要点：11 条原则逐条解读、与 2026 版 GCP 对应关系、数据治理与稽查轨迹要求、附录 C 必备记录表，附临床运营落地清单。",
        "eyebrow": "法规库 · ICH",
        "hero": "ICH E6(R3) 中文要点",
        "subtitle": "11 条原则逐条解读 + 与 2026 版 GCP 的对应 + eTMF 合规落点。9 月 1 日新 GCP 施行前，这一页可以当作团队速查表。",
        "cta_title": "E6(R3) 的数据治理要求，Vivarcus eTMF 里已经内置",
        "cta_desc": "稽查轨迹、元数据管理、数据更正流程——对应 2026 GCP 第五章与 R3 原则 9.4，开箱即用。",
        "cta_secondary_href": "tmf-reference.html",
        "cta_secondary_label": "TMF 分类参考",
    },
    {
        "src": "gcp-2026-essentials.md",
        "src_en": "gcp-2026-essentials.en.md",
        "file": "gcp-2026.html",
        "prefix": "gcp2026",
        "title": "2026 版 GCP 要点：数据治理、保存期限与关键变化 | Vivarcus",
        "desc": "2026 版 GCP（2026-09-01 施行）中文要点：82→54 条六章结构、新增第五章数据治理（元数据与稽查轨迹、盲态完整性、计算机化系统）、保存期限与关键变化对照、9/1 前落地清单。",
        "eyebrow": "法规库 · 中国法规",
        "hero": "2026 版 GCP 要点",
        "subtitle": "9 月 1 日施行：82 → 54 条、新增第五章数据治理。这一页把关键变化、保存期限与落地清单整理成速查表。",
        "cta_title": "第五十一条到五十三条，Vivarcus eTMF 里已经内置",
        "cta_desc": "稽查轨迹、元数据管理、受控数据更正、权限分层与电子签名——对应 2026 GCP 数据治理章，开箱即用。",
        "cta_secondary_href": "ich-e6r3.html",
        "cta_secondary_label": "ICH E6(R3) 要点",
    },
    {
        "src": "audit-trail-essentials.md",
        "src_en": "audit-trail-essentials.en.md",
        "file": "audit-trail.html",
        "prefix": "audittrail",
        "title": "稽查轨迹专题：2026 GCP 第 51/53 条与 ICH E6(R3) 要求 | Vivarcus",
        "desc": "稽查轨迹合规专题：ICH E6(R3) 术语表定义与 Annex 1 第 4.2.3 节逐项要求、2026 版 GCP 第 51/53 条对照、系统层/流程层/文件层 10 项落地自查清单。",
        "eyebrow": "法规库 · 专题",
        "hero": "稽查轨迹专题",
        "subtitle": "9 月 1 日施行后，稽查轨迹从系统加分项变成硬性合规要求。这一页把 GCP 与 E6(R3) 的官方要求合成一张可执行的自查清单。",
        "cta_title": "稽查轨迹、版本史与权限留痕，Vivarcus eTMF 原生支持",
        "cta_desc": "初始值不遮盖、变更可追溯、工作流动作留痕、权限台账可导出——对应 2026 GCP 51/53 条与 E6(R3) 4.2.3，核查现场可直接演示。",
        "cta_secondary_href": "gcp-2026.html",
        "cta_secondary_label": "2026 版 GCP 要点",
    },
]

# Runtime body swap: zh body stays in the DOM; the EN body (from the .en.md twin)
# is embedded as JSON and swapped into .content-inner on load / langchange.
BODY_SWAP = """  <script type="application/json" id="body-data-en">%s</script>
  <script>
    (function () {
      var el = document.querySelector('.content-inner');
      var zhHTML = el.innerHTML;
      var enHTML = JSON.parse(document.getElementById('body-data-en').textContent);
      function applyBody() {
        var en = !!(window.I18N && I18N.getLang() === 'en');
        el.innerHTML = en ? enHTML : zhHTML;
      }
      applyBody();
      window.addEventListener('langchange', applyBody);
    })();
  </script>
"""


def rewrite_links(body):
    """Fix docs-relative links (../x.html) to website-relative (x.html)."""
    return re.sub(r'href="\.\./([^"]+\.html)"', r'href="\1"', body)


def main():
    for spec in PAGES:
        src = os.path.join(MD_DIR, spec["src"])
        with open(src, encoding="utf-8") as f:
            body = rewrite_links(sitegen.convert(f.read()))
        html = sitegen.render_page(
            {k: spec[k] for k in ("title", "desc", "file", "eyebrow", "hero", "subtitle")},
            body, spec["cta_title"], spec["cta_desc"],
            spec["cta_secondary_href"], spec["cta_secondary_label"],
            i18n=spec["prefix"])
        src_en = os.path.join(MD_DIR, spec["src_en"])
        with open(src_en, encoding="utf-8") as f:
            body_en = rewrite_links(sitegen.convert(f.read()))
        swap = BODY_SWAP % json.dumps(body_en, ensure_ascii=False)
        html = html.replace("</body>", swap + "</body>")
        path = os.path.join(OUT_DIR, spec["file"])
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print("%-20s %8d bytes" % (spec["file"], os.path.getsize(path)))


if __name__ == "__main__":
    main()
