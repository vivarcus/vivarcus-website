---
title: 现场 SAE 跟踪（Site SAE Tracking）
description: 了解如何在 Site Monitoring 中登记研究中心发生的严重不良事件（SAE），包括必填字段、与监查事件的关联和维护职责。
last_updated: 2026-08-15
related:
  - monitoring-visits
  - subjects
  - site-lifecycle
---

## 什么是 SAE 跟踪

**Site SAE Tracking** 记录某研究中心在某研究过程中发生的 SAE（严重不良事件）信息，供 CRA 与监查团队跟踪。入口：**Site Monitoring → Site SAE Tracking**；也可从 **Monitoring Event** 详情页的 **Site SAE Tracking** 区进入与登记。

## 登记 SAE

创建记录，**Name** 自动编号（`SAE-{######}`）：

| 字段 | 说明 |
|------|------|
| **Study / Study Country / Study Site** | 所属层级（必填，级联）；从监查事件创建时自动带入 |
| **Subject** | 受试者（必填，按中心过滤） |
| **Monitoring Event** | 可关联发现该 SAE 的监查事件 |
| **SAE Name** | SAE 名称（如具体事件描述） |
| **SAE Start Date** | SAE 开始日期（必填） |
| **SAE End Date** | SAE 结束日期 |
| **SAE Severity** | 严重程度：`Mild`（温和）/ `Moderate`（中等）/ `Severe`（严重） |
| **Outcome** | 结局（必填） |
| **Related? / Expected?** | 与研究药物相关性 / 是否预期 |
| **SAE Report Final** | SAE 报告是否已定稿 |

> 本页面是**跟踪台账**：登记 SAE 基本信息与结局；正式的药物警戒报告与递交仍按机构 SOP 在对应系统完成。

## 状态与维护

生命周期仅 **Active → Inactive** 两态（**Status** 字段由生命周期驱动，不可手改），无自动计算。记录由 CRA 与研究团队手工维护；登记后随访视核对进度，闭环后可将状态置为 Inactive。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 选不到 Subject | Subject 须属于所选研究中心；先选对 Study Site |
| 从监查事件创建时字段为空 | 确认从事件详情页的 Site SAE Tracking 区创建，Study/Center 自动带入 |
| Status 无法编辑 | Status 由生命周期驱动；用生命周期动作切换 Active / Inactive |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Site SAE Tracking：Create、Read、Edit | 登记与维护 SAE 跟踪记录 |

**CRA** 为主要使用者；**CTMS Study Manager** 与 **Central Monitor** 亦可创建与编辑；删除与工作流执行仅 **CTMS Business/System Administrator**。
