---
title: TMF Homepage：文档完成度与稽查就绪
description: TMF 主页把完整性、及时性、质量问题与待办汇总成一张健康仪表盘。了解各 Widget 的口径、Study 选择器与稽查就绪自检清单。
last_updated: 2026-08-15
related:
  - edl
  - quality-issues
  - milestones
  - overview
---

## 概述

TMF 主页是研究健康度的日常入口，可视化 TMF 文档的**及时性、完整性与质量**，并汇总任务与里程碑。顶部 **Study 选择器**：Study 必填，Study Country / Study Site 可选，用于把指标裁剪到国家或中心范围。

## Widget 一览

| Widget | 显示内容 |
|--------|----------|
| **Completeness** | 完整性百分比 + Unapproved Documents 计数 |
| **Timeliness** | 批准及时性饼图（阈值天数由管理员配置） |
| **Upcoming Milestones** | 尚无 Actual Finish Date 的里程碑，可按 Milestone Category 过滤 |
| **质量问题** | 质量问题饼图，可过滤 Open / Closed / 全部 |
| **我的任务** | 最多 10 条分配给我的任务 |
| **需要关注的任务** | Overdue / Unassigned / Due Today 三计数 |

## Completeness 口径

- 百分比基于所选里程碑下 **Requiredness = Required** 的 EDL Item。
- **Unapproved Documents**：用户有权限查看、且最新版本不在稳态（不含 Superseded / Obsolete）的文档数；点击进入预过滤文档列表。
- **Review Overcount**：跳转到 Overcount = Yes 的 EDL Item 列表。
- **Review Pending Decisions**：跳转到 Requiredness = Pending Decision 的 EDL Item 列表。

## Timeliness

Timeliness 跟踪文档从审批到入档 TMF 的耗时。饼图按阈值二分（如"≤30 天批准 / >30 天批准"），阈值由管理员在 **Admin → Settings → Application Settings → eTMF Features** 中配置。

## 质量问题与任务

- **质量问题** 按类型（Duplicate / Expired / Misclassified 等）分组，可过滤 Open、Closed、全部或分配给我的。需要在相关文档类型上配置 Quality Issue 字段后才会统计。
- **我的任务** 只显示 document、envelope 与 clinical user tasks；质量问题任务在质量问题 Widget 中查看。

## 稽查就绪自检清单

| 检查项 | 在哪里看 |
|--------|----------|
| EDL 完整性 | **Completeness** 百分比 |
| 未批准文档 | **Unapproved Documents** 计数 → 点击进入列表 |
| 超额 / 待定 | **Review Overcount** / **Review Pending Decisions** |
| 及时性 | **Timeliness** 阈值口径 |
| 开放质量问题 | **质量问题** → Open |
| 即将到期里程碑 | **Upcoming Milestones** |
| 个人待办 | **我的任务** |

> Timeliness 全是 0% 时，通常是没有已批准文档或阈值未配置；完成一次批准后刷新即可。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| Tab | TMF 主页：View | 访问 TMF 主页标签 |
| 对象 | Study / Milestone / EDL Item：Read | Completeness、Upcoming Milestones 等 Widget 取数 |
| 对象 | Document：Read | Unapproved Documents 计数与下钻 |
| 对象 | Clinical User Task：Read | 我的任务、Tasks Requiring Attention |
| 对象 | Quality Issue：Read | 质量问题 Widget 统计 |

页面只显示用户有 Read 权限的文档与任务；数据范围由研究层级的动态 Sharing（**Team Role + Grant Access**）裁剪。
