---
title: 里程碑跟踪与注册指标
description: 了解研究管理的里程碑跟踪（Milestone Tracking）与注册指标（Enrollment Metrics）：从计划研究生成到排期完成、指标播种与 Metrics Over Time 的门禁。
last_updated: 2026-08-15
related:
  - study-lifecycle
  - dashboards
  - site-lifecycle
---

## 里程碑跟踪

**研究管理 → 里程碑跟踪** 列出全库研究里程碑（对象 Milestone，与 eTMF 共用），研究经理在此跟踪各研究关键节点：

| 列表列 | 含义 |
|--------|------|
| **Milestone** | 里程碑名（来自模板） |
| **研究 / 研究国家/地区 / 研究地点** | 所属层级 |
| **Milestone Type** | 类型，如 `First Subject In (FSI)`、`Database Lock` |
| **Baseline / 已计划 / Actual Finish Date** | 基线、计划与实际完成日期 |
| **% Complete / Completeness** | 完成度（自动计算，图标呈现） |
| **Completed EDL Item Records** | 已完成的预期文档条目数 |

里程碑由 **计划研究** 按主集模板自动生成（初始 **未计划**），国家/中心进入 Initiating 时生成各自层级里程碑。排期与完成：

1. **计划里程碑**：填 **计划完成日期**，系统联动下游依赖日期，状态 → **已计划**。
2. **Mark Complete**：填 **Actual Finish Date**，状态 → **Complete**。

> 依赖门禁服务端强制：下游 **Mark Complete** 时上游未完成会被拒绝，除非设置 **Gating Override Date**。

完成度由「前序里程碑完成 + 必做任务完成 + 预期文档收集与批准」自动计算；用 **查看预期文档** 查看关联 EDL Item。详细状态流转见 [里程碑](../etmf/milestones.html)。

## 注册指标

**研究管理 → 注册指标** 维护各层级的入组指标（对象 Metric）。研究进入 Planning/Active、国家/中心进入 Initiating 时，系统**自动播种**每条指标一条记录（初值 0），按层级分三类：

| 类型 | 层级 |
|------|------|
| **Study Metric** | 研究级 |
| **Study Country Metric** | 国家/地区级 |
| **Study Site Metric**（默认） | 中心级 |

**Metric Type** 共 11 类：Total In Screening、Total Screened、Total Screen Failed、Total Enrolled、Total Withdrawn、Total Completed、Enrollment Rate (subjects per month)、Screen Failure Rate (%)、Drop Out Rate (%)、Total Randomized、Total End of Treatment。

维护方式：数值**手动填写**——**Planned**（计划数）、**Forecast**（预测数）、**Actual**（实际数）；**Planned Roll Up** 由子级 Planned 自动汇总。

> 研究配置 **Metrics Not In Use** 可裁剪不播种的指标类型，并从主页移除对应元素。

### Metrics Over Time

执行对象工作流（研究/国家/中心详情页的 **所有操作**，如 Create Metrics Over Time）可按 **Recruitment Planning Frequency**（默认按月）生成各期间 planned/actual/forecast 记录。前置门禁：

- 研究的 **Metric Calculation** 为 Date-Based；
- 招募指标成对里程碑（First/Last）已有结束日期（Last ≥ First）；
- 对应指标的 **Planned > 0**。

生成的趋势数据叠加到 **研究管理主页** 的 Enrollment Status 折线图（仅研究/国家级展示，中心级入组看受试者列表）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| Milestone Tracking 列表为空 | 研究须先执行 **计划研究** 并推进到 Planning；国家/中心须进入 Initiating |
| Metrics Over Time 生成失败 | 核对三个门禁：Date-Based、First/Last Milestone日期、Planned > 0 |
| Enrollment Status 图无数据 | 折线图仅研究/国家级展示；确认 enrollment_status 与 metrics_over_time 数据已播种 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Milestone：Read、Edit | 查看与排期里程碑 |
| 生命周期动作 | Milestone：**计划里程碑**、**Mark Complete** | 排期与完成 |
| 对象 | Metric：Create、Read、Edit | 维护 Planned / Forecast / Actual |
| 对象动作 | Metric：**Create Metrics Over Time**（研究/国家/中心） | 生成期间趋势数据 |

**CTMS Study Manager**、**CRA** 与 **Central Monitor** 可维护指标与里程碑；**CTMS Business/System Administrator** 另有删除与工作流执行权限。
