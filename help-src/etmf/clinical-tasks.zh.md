---
title: 临床任务（Clinical Tasks）
description: 了解临床用户任务（Clinical User Task）的对象类型、创建方式、Open → Investigating / Implementing / Escalated → Resolved 状态流转与自动统计。
last_updated: 2026-08-15
related:
  - template-tasks
  - milestones
  - review-workflow
---

## 什么是临床任务

**Clinical User Task**（临床用户任务）是挂在研究层级上的待办/问题条目：指派给某人，跟踪类别、优先级、截止日期，直至解决。任务出现在多个入口，eTMF 侧主要是 **计划 → 临床任务**；CTMS 侧的监查跟进项也基于同一对象（见 [监查跟进项与 CTMS 临床任务](../ctms/clinical-tasks.html)）。

## 任务类型（Object Type）

类型决定任务挂在哪个层级、是否关联监查事件：

| 类型 | 层级 | 说明 |
|------|------|------|
| **研究任务**（默认） | 研究 | 研究级任务，可关联里程碑与模板任务 |
| **Study Country Task** | 研究国家/地区 | 国家/地区级任务 |
| **Study Site Task** | 研究地点 | 中心级任务 |
| **监查事件跟进项** | 研究中心 | CTMS 监查跟进项，必须关联同一中心的监查事件 |

研究/国家/中心详情页的 **Study Tasks / Study Country Tasks / Study Site Tasks** 区块按类型过滤展示对应任务。

## 创建任务

1. 导航 **计划 → 临床任务** → 创建，选择类型（默认 **研究任务**）。
2. 填写：

| 字段 | 说明 |
|------|------|
| **Name** | 任务名称（必填） |
| **研究 / 研究国家/地区 / 研究地点** | 按类型级联选择 |
| **Category** | 类别（必填），如 `Essential Documents/ISF`、`Informed Consent`、`Data Collection/Data Entry/Query Resolution` 等 12 类 |
| **Priority** | 优先级（必填）：`Low` / `Medium` / `High` |
| **分配给** | 指派人 |
| **Opened Date** | 未处理日期（必填，不能晚于今天） |
| **Due Date** | 截止日期（不能早于 Opened Date） |
| **Required** | 是否必做 |
| **Milestone** | 可关联里程碑，让任务计入里程碑完成度 |

3. 保存后任务处于 **打开** 状态，被指派人会收到通知；**我的任务** 页可集中处理所有指派给自己的任务。

## 状态与动作

| 状态 | 可用动作 |
|------|----------|
| **打开** | **Investigate**（开始调查）、**Implement**（直接实施）、**Escalate**（上报）、**Resolve**（解决） |
| **Investigating** | **Implement**、**Escalate**、**Resolve** |
| **Implementing** | **Escalate**、**Resolve** |
| **Escalated** | **Investigating**、**Implementing**、**Resolve** |
| **已解决** | 无（终态，记录变为只读） |

> 进入 Escalated 会累计上报次数与日期；**Resolve** 后系统自动勾选 **Complete** 并写入 **Completion Date**，同时计算 **Days Open / Days Investigating / Days Implementing** 三个时长指标。

## 校验规则

- **Opened Date** 不能晚于今天；
- **Due Date** 不能早于 **Opened Date**。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 创建时没有 Milestone 字段 | 使用默认类型研究任务；监查事件跟进项类型字段集更精简 |
| Resolved 后想修改 | Resolved 为终态只读；如需修正请重新创建任务 |
| 收不到任务通知 | 确认任务已填写 **分配给**；指派与改派通知均发给被指派人 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Clinical User Task：Create、Read、Edit | 创建并维护任务 |
| 生命周期动作 | **Investigate**、**Implement**、**Escalate**、**Resolve** | 推进任务直至解决 |
| 对象 | Milestone：Read | 关联里程碑并影响其完成度 |

**Clinical Application Administrator** 与 **Document Contributor** 均可编辑任务并执行全部生命周期动作；任务详情按研究 Sharing 裁剪，指派人通常可见被指派给自己的任务。
