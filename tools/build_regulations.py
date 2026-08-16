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
    {
        "src": "annex-c-essentials.md",
        "src_en": "annex-c-essentials.en.md",
        "file": "annex-c.html",
        "prefix": "annexc",
        "title": "ICH E6(R3) 附录 C 必备记录表：52 条中文对照与 TMF 归类 | Vivarcus",
        "desc": "ICH E6(R3) 附录 C 必备记录表逐条中文对照：28 条必备性判定标准、52 条必备记录与 TMF Reference Model v3.0 区域/文件项归类、启动前标记与 TMF 实操要点，搭 TMF 目录与核对 EDL 的直接依据。",
        "eyebrow": "法规库 · ICH",
        "hero": "E6(R3) 附录 C 必备记录表",
        "subtitle": "TMF 该存什么的官方依据：52 条必备记录逐条对照 TMF Reference Model v3.0，附 28 条判定标准与启动前标记。",
        "cta_title": "附录 C 的 52 条记录，Vivarcus eTMF 的 EDL 里已经内置",
        "cta_desc": "TMF RM v3.0 目录结构 + 按研究类型自动生成预期文档清单，对照表不用再手工维护。",
        "cta_secondary_href": "tmf-reference.html",
        "cta_secondary_label": "TMF 分类参考",
    },
    {
        "src": "retention-essentials.md",
        "src_en": "retention-essentials.en.md",
        "file": "retention.html",
        "prefix": "retention",
        "title": "临床试验记录保存期限专题：2026 GCP 第 16/29 条与 ICH E6(R3) 9.5 | Vivarcus",
        "desc": "临床试验记录保存期限专题：2026 GCP 第 16/29 条与 ICH E6(R3) 9.5 的官方要求对照、三种情形速查表（获批上市后 5 年/终止后 5 年、BE 留样 2 年）、到期处置流程与 eTMF/CTMS 合规落点。",
        "eyebrow": "法规库 · 专题",
        "hero": "记录保存期限专题",
        "subtitle": "什么记录、保存多久、起算点怎么算、到期能不能销毁——第 16/29 条与 R3 9.5 的要求合成一张速查表。",
        "cta_title": "保存期限台账与到期处置，Vivarcus eTMF 里可以管起来",
        "cta_desc": "记录留存策略、到期提醒、销毁/移交工作流留痕——对应第 16/29 条与 R3 2.12.12/3.16.3，核查现场可直接演示。",
        "cta_secondary_href": "gcp-2026.html",
        "cta_secondary_label": "2026 版 GCP 要点",
    },
    {
        "src": "safety-reporting-essentials.md",
        "src_en": "safety-reporting-essentials.en.md",
        "file": "safety-reporting.html",
        "prefix": "safety",
        "title": "临床试验安全性报告专题：2026 GCP 第 26/44 条与 ICH E6(R3) | Vivarcus",
        "desc": "临床试验安全性报告专题：2026 GCP 第 26/44 条与 ICH E6(R3) 2.7.2/3.13 官方要求对照、SAE/SUSAR/DSUR 时限速查表（24h/7·15 天）、报告路径与分工、盲态管理与实操要点。",
        "eyebrow": "法规库 · 专题",
        "hero": "安全性报告专题",
        "subtitle": "SAE 多久报、SUSAR 怎么判、签阅怎么留痕——第 26/44 条与 R3 3.8/3.13 合成一张时限速查表与报告路径图。",
        "cta_title": "SAE/SUSAR 的时限与签阅，Vivarcus CTMS 里可以管起来",
        "cta_desc": "事件登记时间戳、时限提醒、报告发送接收留痕、签阅状态跟踪——获知到报告的完整时间线可直接导出。",
        "cta_secondary_href": "timeline-calendar.html",
        "cta_secondary_label": "临床试验时限日历",
    },
    {
        "src": "ethics-review-essentials.md",
        "src_en": "ethics-review-essentials.en.md",
        "file": "ethics-review.html",
        "prefix": "ethics",
        "title": "临床试验伦理审查专题：2026 GCP 第 14-17 条与 ICH E6(R3) | Vivarcus",
        "desc": "伦理审查专题：2026 GCP 第 14-17 条与 ICH E6(R3) Annex 1 第 1 节官方要求对照、意见分类与跟踪审查（≤12 个月）、特殊情形审查、审查全流程时限速查与稽查自查要点。",
        "eyebrow": "法规库 · 专题",
        "hero": "伦理审查专题",
        "subtitle": "审查什么文件、意见分几类、多久跟踪一次——第 14-17 条与 E6(R3) Annex 1 第 1 节合成一张流程速查表。",
        "cta_title": "批件-版本对照与跟踪审查日历，Vivarcus eTMF 里可以管起来",
        "cta_desc": "伦理批件与文件版本一一对应、跟踪审查到期提醒、递交与意见往返记录链归档——对应第 14-17 条，核查现场可直接演示。",
        "cta_secondary_href": "safety-reporting.html",
        "cta_secondary_label": "安全性报告专题",
    },
    {
        "src": "submission-essentials.md",
        "src_en": "submission-essentials.en.md",
        "file": "submission.html",
        "prefix": "submission",
        "title": "临床试验递交专题：IND 默示许可与递交后义务 | Vivarcus",
        "desc": "临床试验递交专题：IND 60 个工作日默示许可、CDE 沟通交流会议时限（I/II/III 类 30/60/75 个工作日）、登记公示与 SUSAR/DSUR/变更/暂停终止等递交后义务的时间线速查。",
        "eyebrow": "法规库 · 专题",
        "hero": "递交专题（IND/CTA）",
        "subtitle": "默示许可 60 个工作日怎么算、沟通会议选哪类、递交后还有哪些义务——一张时间线速查表。",
        "cta_title": "递交日历与批件管理，Vivarcus eTMF 里可以管起来",
        "cta_desc": "默示许可倒计时、沟通会议与递交回执归档、许可-版本对照、登记平台信息同步提醒——从受理到首例入组每个节点都有到期提醒与归档位置。",
        "cta_secondary_href": "timeline-calendar.html",
        "cta_secondary_label": "临床试验时限日历",
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
