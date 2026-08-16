#!/usr/bin/env python3
"""Generate the whitepaper page from docs/marketing/whitepaper-china-tmf.md.

Run from repo root:  python3 website/tools/build_whitepaper.py
Content source of truth: docs/marketing/whitepaper-china-tmf.md (+ .en.md twin)
Generated page: website/whitepaper.html (bilingual: zh body inline, en body
embedded as JSON and swapped at runtime; hero/meta/CTA keys live in js/i18n-data.js)

CDE charts: the md twins only mark placement with a lone "@@chart:cde@@" line;
the build replaces it with static bilingual chart blocks (trend + drug mix)
generated from cde_data.py via the same SVG builders as the cde-trials page.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitegen  # noqa: E402
from build_cde_trends import VIZ_CHART_CSS, fmt, pct, stacked_bar_svg, trend_svg  # noqa: E402
from cde_data import AS_OF, DRUG_TYPE, YEARLY  # noqa: E402

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


CHART_MARKER = "<p>@@chart:cde@@</p>"

WP_EXTRA_STYLE = VIZ_CHART_CSS + """
    .viz-chart-link { font-size: 0.9rem; margin: 0 0 0.4rem; }
"""


def chart_block(lang):
    """Static CDE chart block for the whitepaper body (baked language).

    Figures come from cde_data.py at build time so the whitepaper stays in
    sync with the cde-trials page; interactive exploration lives there and is
    linked below the charts."""
    peak_year, peak_val = max(YEARLY, key=lambda p: p[1])
    first_val = YEARLY[0][1]
    growth = f"约 {peak_val / first_val:.0f} 倍"
    drug_total = sum(v for _, v in DRUG_TYPE)
    bio_pct = pct(dict(DRUG_TYPE)["生物制品"], drug_total)
    if lang == "en":
        title1 = "Industry backdrop: over a decade of trial growth"
        sub1 = (f"Drug trial registrations grew from {fmt(first_val)} in 2013 to "
                f"{fmt(peak_val)} in {peak_year} — about {peak_val / first_val:.0f}x; "
                f"2026 is a partial year as of {AS_OF}. Inspection attention rises with trial volume.")
        title2 = "A shifting innovative-drug mix"
        sub2 = (f"Biological products account for {bio_pct} of categorized registrations — "
                f"a direct signal of the changing innovative-drug mix.")
        link = "Explore the interactive charts and full data →"
    else:
        title1 = "行业背景：登记试验量十余年增长"
        sub1 = (f"药物临床试验登记量从 2013 年的 {fmt(first_val)} 项增至 {peak_year} 年的 "
                f"{fmt(peak_val)} 项，增长{growth}；2026 年为截至 {AS_OF} 的部分年份。"
                f"检查关注度随试验体量同步上升。")
        title2 = "创新药结构变化：生物制品占比提升"
        sub2 = f"分类口径下生物制品占 {bio_pct}——创新药结构变化的直观信号。"
        link = "查看交互版图表与完整数据 →"
    return f"""
        <div class="viz-root">
          <div class="viz-chart">
            <h3>{title1}</h3>
            <p class="viz-chart-sub">{sub1}</p>
            {trend_svg(lang=lang, interactive=False)}
          </div>
          <div class="viz-chart">
            <h3>{title2}</h3>
            <p class="viz-chart-sub">{sub2}</p>
            {stacked_bar_svg(DRUG_TYPE, lang=lang)}
          </div>
          <p class="viz-chart-link"><a href="cde-trials.html">{link}</a></p>
        </div>"""


def main():
    body = body_from(SRC)
    body_en = body_from(SRC_EN)
    if CHART_MARKER not in body:
        print("WARNING: @@chart:cde@@ marker not found in zh source")
    if CHART_MARKER not in body_en:
        print("WARNING: @@chart:cde@@ marker not found in en source")
    body = body.replace(CHART_MARKER, chart_block("zh"), 1)
    body_en = body_en.replace(CHART_MARKER, chart_block("en"), 1)
    html = sitegen.render_page(META, body, CTA_TITLE, CTA_DESC,
                               CTA_SECONDARY_HREF, CTA_SECONDARY_LABEL,
                               extra_style=WP_EXTRA_STYLE, i18n="whitepaper")
    swap = BODY_SWAP % json.dumps(body_en, ensure_ascii=False)
    html = html.replace("</body>", swap + "</body>")
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html)
    print("%-20s %8d bytes" % (META["file"], os.path.getsize(OUT)))


if __name__ == "__main__":
    main()
