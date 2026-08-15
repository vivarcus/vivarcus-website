---
title: 运营仪表板：Study Management 与 CRA Homepage
description: 了解两张 CTMS 工作台的 Widget 构成与三级范围选择器：Study Management Homepage 给研究经理，CRA Homepage 给监查员。
last_updated: 2026-08-15
related:
  - monitoring-visits
  - study-lifecycle
  - overview
---

## 两张工作台

CTMS 提供两张工作台，共用 **Study / Country / Site** 三级范围选择器：

| 工作台 | 入口 | 面向角色 |
|--------|------|----------|
| **Study Management Homepage** | Study Management → Study Management Homepage | 研究经理（运营总览） |
| **CRA Homepage** | Site Monitoring → CRA Homepage | CRA（监查工作台） |

选择 Study 后 Widget 网格加载；进一步选择 Country / Site 可把指标裁剪到对应范围，清除后回到研究级。

## Study Management Homepage

| Widget | 内容 |
|--------|------|
| **Summary Metrics** | Site Status / Enrolled / Complete 等进度（无数据时可为 0） |
| **Monitoring Compliance** | Visits Overdue 口径与 Visit Report Cycle Time（可为 None Due） |
| **Monitoring Status** | 按访视类型分布计数 |
| **Milestones** | Plan Study / Ready to Enroll 生成的里程碑 |
| **My Tasks** | 个人待办 |
| **Enrollment Status** | 注册状态（允许空态） |

## CRA Homepage

| Widget | 内容 |
|--------|------|
| **Details** | 研究详细信息 |
| **Summary Metrics** | 摘要指标 |
| **Monitoring Plan** | 范围裁剪后的访视计划；点击访视名称下钻到 Monitoring Event 详情 |
| **My Tasks** | 个人待办 |
| **Enrollment Status** | 注册状态 |
| **Quality** | 质量问题/偏离计数（有 Open 偏离时可能反映在图中；允许空态） |

## 与 TMF Homepage 的分工

TMF Homepage 是**文档侧**健康度（完整性、及时性、文档质量）；两张 CTMS Homepage 是**过程侧**运营度（中心状态、访视合规、注册进度）。同一 Vault 中三个入口并存，按角色分工使用。

> Homepage Monitoring Status 为空时：确认已选对本 Study，且 Monitoring Event 的 Study/Country/Site 绑定正确，刷新页面。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| Tab | Study Management Homepage / CRA Homepage：View | 访问仪表板 |
| 对象 | Study / Study Site / Monitoring Event / Milestone / Subject / Issue：Read | 各 Widget 取数 |
| 对象 | Clinical User Task：Read | My Tasks Widget |

Widget 数据受动态 Sharing 裁剪：用户只能看到其 Team Role 授予范围（研究/国家/中心）内的数据。
