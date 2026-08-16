#!/usr/bin/env python3
"""Generate the whitepaper page from docs/marketing/whitepaper-china-tmf.md.

Run from repo root:  python3 website/tools/build_whitepaper.py
Content source of truth: docs/marketing/whitepaper-china-tmf.md (+ .en.md twin)
Generated page: website/whitepaper.html (bilingual: zh body inline, en body
embedded as JSON and swapped at runtime; hero/meta/CTA keys live in js/i18n-data.js)
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitegen  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "docs", "marketing", "whitepaper-china-tmf.md")
SRC_EN = os.path.join(ROOT, "docs", "marketing", "whitepaper-china-tmf.en.md")
OUT = os.path.join(ROOT, "website", "whitepaper.html")

META = {
    "title": "中国临床试验 TMF 管理白皮书：合规责任、风险与数字化路径 | Vivarcus",
    "desc": "中国临床试验 TMF 管理白皮书：TMF 合规责任在申办方、Excel/网盘管理的七类结构性风险、2026 版 GCP 数据治理对文件管理的影响、分阶段数字化路径与 eTMF 选型清单。",
    "file": "whitepaper.html",
    "eyebrow": "行业资源 · 白皮书",
    "hero": "中国临床试验 TMF 管理白皮书",
    "subtitle": "合规责任、常见风险与数字化路径——面向 biotech 与 CRO 的临床运营、质量管理与决策者。",
}
CTA_TITLE = "白皮书里的数字化能力，Vivarcus eTMF 开箱即用"
CTA_DESC = "EDL 自动生成、文档生命周期与稽查轨迹、完整性/及时性/质量指标看板——对应 2026 GCP 数据治理要求，开箱即用。"
CTA_SECONDARY_HREF = "regulations.html"
CTA_SECONDARY_LABEL = "法规库"

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


def body_from(md_path):
    """Read a whitepaper markdown source and convert the public-facing part.

    Drops the md subtitle line (moved into the page hero) and any internal
    sections below the "附：" marker — the public page must never carry
    the internal checklist.
    """
    with open(md_path, encoding="utf-8") as f:
        lines = f.read().split("\n")

    kept = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("**——") and stripped.endswith("**"):
            continue
        if stripped.startswith("## 附："):
            break
        kept.append(line)

    return sitegen.convert("\n".join(kept))


def main():
    body = body_from(SRC)
    body_en = body_from(SRC_EN)
    html = sitegen.render_page(META, body, CTA_TITLE, CTA_DESC,
                               CTA_SECONDARY_HREF, CTA_SECONDARY_LABEL,
                               i18n="whitepaper")
    swap = BODY_SWAP % json.dumps(body_en, ensure_ascii=False)
    html = html.replace("</body>", swap + "</body>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("%-20s %8d bytes" % (META["file"], os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
