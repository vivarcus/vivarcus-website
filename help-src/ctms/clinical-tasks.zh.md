---
title: 监查跟进项与 CTMS 临床任务
description: 了解 CTMS 侧的临床任务列表、监查事件跟进项（Monitoring Follow Up Item）的创建与关联，以及关联跟进项目在访视报告中的用法。
last_updated: 2026-08-15
related:
  - monitoring-visits
  - issue-management
  - dashboards
---

## 与 eTMF 临床任务的关系

CTMS 的 **临床任务** 与 eTMF 的临床任务同属一个对象（Clinical User Task，见 [临床任务](../etmf/clinical-tasks.html)），只是从不同 tab 进入：**现场监控 → 临床任务**、**研究管理 → 临床任务**。CTMS 特有的类型是 **Monitoring Follow Up Item**（监查事件跟进项）。

## 监查事件跟进项（Monitoring Follow Up Items）

跟进项是挂在监查事件下的任务，代表「这次访视需要跟进的事」，在 **现场监控 → 监查事件跟进项** 中管理。它比普通任务更精简：

| 字段 | 说明 |
|------|------|
| **Name** | 跟进项名称（必填） |
| **研究 / 研究国家/地区 / 研究地点** | 创建时从监查事件自动带入 |
| **监查事件** | 关联的监查事件（必填，且必须属于同一中心） |
| **Category / Priority** | 类别与优先级（必填） |
| **分配给** | 指派人（通常为 CRA 或中心协调员） |
| **Opened Date / Due Date** | 未处理日期与截止日期 |
| **Complete** | 完成标记（必填字段，Resolve 后自动勾选） |

创建方式：在 **监查事件** 详情页的 **监查事件跟进项** 区直接内联创建（推荐，Study/Center 自动带入）；或从 tab 列表创建后手工关联同一中心的监查事件。状态流转与普通任务一致：**打开 → Investigating / Implementing / Escalated → 已解决**。

## 关联跟进项目与访视报告

在监查事件上执行 **所有操作 → 关联跟进项目**，系统把两类跟进项快照到事件上，供写访视报告/跟进信时引用：

- **Monitored Open Follow Up Items**：事件发生时仍打开的跟进项；
- **Monitored Closed Follow Up Items**：自上次监查事件以来已关闭的跟进项。

> 关联跟进项目只建立关联快照，不会自动创建跟进项记录——跟进项须先手工登记（或在事件详情页内联创建）。

## 与里程碑完成度的联动

研究侧任务可关联 **Milestone**；必做任务完成后计入里程碑完成度（见 [里程碑跟踪](study-metrics.html#里程碑跟踪) 与 [里程碑](../etmf/milestones.html)）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 创建跟进项选不到 Monitoring Event | 跟进项与事件必须同属一个研究中心；先选对 Study Site |
| 任务列表看不到自己的跟进项 | 确认已填写 **分配给**；**我的任务** 页可看全部指派任务 |
| 关联跟进项目后区块仍为空 | 该动作只关联已有跟进项；先在事件详情页创建跟进项再执行 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Clinical User Task（含 Monitoring Follow Up Item）：Create、Read、Edit | 登记与维护跟进项 |
| 生命周期动作 | **Investigate**、**Implement**、**Escalate**、**Resolve** | 推进任务直至解决 |
| 对象动作 | Monitoring Event：**关联跟进项目** | 快照跟进项到访视 |

**CRA**、**Central Monitor** 与 **CTMS Study Manager** 均可创建跟进项并推进状态；CRA 可删除自己创建的跟进项；**CTMS Business/System Administrator** 拥有全部权限。
