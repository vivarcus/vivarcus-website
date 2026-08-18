#!/usr/bin/env python3
"""Query Alibaba Cloud CDN stats for vivarcus.com marketing site.

Requires: aliyun CLI configured with CDN access.

Examples:
  python3 website/tools/cdn_stats.py --days 2
  python3 website/tools/cdn_stats.py --date 2026-08-17 --logs
"""

from __future__ import annotations

import argparse
import collections
import gzip
import io
import json
import re
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

CST = timezone(timedelta(hours=8))
DOMAINS = "vivarcus.com,www.vivarcus.com"
APEX = "vivarcus.com"


def run_aliyun(api: str, **kwargs: str) -> dict:
    cmd = ["aliyun", "cdn", api]
    for key, value in kwargs.items():
        cmd.append(f"--{key}")
        cmd.append(value)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip())
    return json.loads(result.stdout)


def day_window(d: date) -> tuple[str, str]:
    """Beijing calendar day -> UTC ISO start/end for CDN APIs."""
    start_cst = datetime(d.year, d.month, d.day, tzinfo=CST)
    end_cst = start_cst + timedelta(days=1)
    return (
        start_cst.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        end_cst.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    )


def fmt_bytes(n: int) -> str:
    if n < 1024 ** 2:
        return f"{n / 1024:.1f} KB"
    return f"{n / 1024 ** 2:.2f} MB"


def sum_pv_uv(start: str, end: str) -> tuple[int, int, int, int]:
    pv_total = uv_total = 0
    for domain in ("vivarcus.com", "www.vivarcus.com"):
        pv = run_aliyun("DescribeDomainPvData", DomainName=domain, StartTime=start, EndTime=end)
        uv = run_aliyun("DescribeDomainUvData", DomainName=domain, StartTime=start, EndTime=end)
        pv_total += sum(int(x["Value"]) for x in pv["PvDataInterval"]["UsageData"])
        uv_total += sum(int(x["Value"]) for x in uv["UvDataInterval"]["UsageData"])
    return pv_total, uv_total, 0, 0


def sum_traffic(start: str, end: str) -> int:
    data = run_aliyun(
        "DescribeDomainTrafficData",
        DomainName=DOMAINS,
        StartTime=start,
        EndTime=end,
        Interval="86400",
    )
    return sum(int(x["Value"]) for x in data["TrafficDataPerInterval"]["DataModule"])


def top_urls(start: str, end: str, limit: int = 12) -> list[tuple[str, int]]:
    data = run_aliyun(
        "DescribeDomainTopUrlVisit",
        DomainName=APEX,
        StartTime=start,
        EndTime=end,
        SortBy="pv",
    )
    items = data.get("AllUrlList", {}).get("UrlList", [])
    rows: list[tuple[str, int]] = []
    for item in items[:limit]:
        url = item["UrlDetail"]
        path = url.replace("https://vivarcus.com", "").replace("http://vivarcus.com", "") or "/"
        rows.append((path, int(item["VisitData"])))
    return rows


def top_referers(start: str, end: str, limit: int = 8) -> list[tuple[str, int, float]]:
    data = run_aliyun(
        "DescribeDomainTopReferVisit",
        DomainName=APEX,
        StartTime=start,
        EndTime=end,
        SortBy="pv",
    )
    items = data.get("TopReferList", {}).get("ReferList", [])
    rows: list[tuple[str, int, float]] = []
    for item in items[:limit]:
        rows.append(
            (
                item["ReferDetail"],
                int(item["VisitData"]),
                float(item.get("VisitProportion", 0)) * 100,
            )
        )
    return rows


def log_urls(start: str, end: str) -> list[str]:
    data = run_aliyun(
        "DescribeCdnDomainLogs",
        DomainName=APEX,
        StartTime=start,
        EndTime=end,
    )
    urls: list[str] = []
    for detail in data["DomainLogDetails"]["DomainLogDetail"]:
        for item in detail["LogInfos"]["LogInfoDetail"]:
            path = item["LogPath"]
            if not path.startswith("http"):
                path = "https://" + path
            urls.append(path)
    return urls


def parse_log_line(line: str) -> tuple[str, str] | None:
    match = re.search(r'"GET (https?://[^"]+)" (\d+)', line)
    if not match:
        return None
    url = match.group(1)
    ua_match = re.search(r'"([^"]*)"\s+"[^"]*"\s+\S+\s*$', line)
    ua = ua_match.group(1) if ua_match else ""
    path = url.split("vivarcus.com", 1)[-1].split("?")[0] or "/"
    return path, ua


def classify(ua: str, path: str) -> str:
    ua_l = ua.lower()
    if "wp-admin" in path:
        return "WordPress扫描"
    if "gptbot" in ua_l:
        return "GPTBot"
    if "oai-searchbot" in ua_l:
        return "OAI-SearchBot"
    if "googlebot" in ua_l:
        return "Googlebot"
    if "bingbot" in ua_l:
        return "Bingbot"
    if "bot" in ua_l or "spider" in ua_l:
        return "其他爬虫"
    if not ua or ua == "-":
        return "无 UA"
    return "浏览器/真人"


def analyze_logs(start: str, end: str) -> tuple[collections.Counter[str], collections.Counter[str], int]:
    path_c: collections.Counter[str] = collections.Counter()
    bot_c: collections.Counter[str] = collections.Counter()
    lines = 0
    for url in log_urls(start, end):
        data = urllib.request.urlopen(url, timeout=30).read()
        with gzip.GzipFile(fileobj=io.BytesIO(data)) as gz:
            for raw in gz:
                parsed = parse_log_line(raw.decode("utf-8", "replace"))
                if not parsed:
                    continue
                path, ua = parsed
                lines += 1
                path_c[path] += 1
                bot_c[classify(ua, path)] += 1
    return path_c, bot_c, lines


def report_day(d: date, with_logs: bool) -> None:
    start, end = day_window(d)
    pv, uv, _, _ = sum_pv_uv(start, end)
    traffic = sum_traffic(start, end)
    print(f"\n{'=' * 56}")
    print(f"{d.isoformat()}（北京时间）  PV {pv}  UV累加 {uv}  流量 {fmt_bytes(traffic)}")

    print("\n热门 URL:")
    for path, count in top_urls(start, end):
        print(f"  {count:>4}  {path}")

    print("\nReferer:")
    for ref, count, pct in top_referers(start, end):
        print(f"  {count:>4} ({pct:.1f}%)  {ref}")

    if with_logs:
        try:
            path_c, bot_c, lines = analyze_logs(start, end)
            print(f"\n离线日志（{lines} 行）访问类型:")
            for name, count in bot_c.most_common():
                print(f"  {name}: {count} ({count / lines * 100:.1f}%)")
            print("\n日志路径 Top 10:")
            for path, count in path_c.most_common(10):
                print(f"  {count:>4}  {path}")
        except Exception as exc:  # noqa: BLE001 — CLI tool, surface API errors
            print(f"\n离线日志解析失败: {exc}")


def main() -> None:
    parser = argparse.ArgumentParser(description="CDN stats for vivarcus.com")
    parser.add_argument("--days", type=int, default=2, help="recent N calendar days (Beijing)")
    parser.add_argument("--date", help="single day YYYY-MM-DD (Beijing)")
    parser.add_argument("--logs", action="store_true", help="parse offline CDN logs")
    args = parser.parse_args()

    if args.date:
        days = [datetime.strptime(args.date, "%Y-%m-%d").date()]
    else:
        today = datetime.now(CST).date()
        days = [today - timedelta(days=i) for i in range(args.days - 1, -1, -1)]

    print("vivarcus.com CDN 统计（阿里云）")
    for d in days:
        report_day(d, args.logs)


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)
