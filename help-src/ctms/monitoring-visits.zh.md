---
title: 监查访视（Monitoring Events）
description: 学习四类监查访视（PSV/SIV/IMV/COV）的创建与全生命周期推进：Expected → Planning → Confirmed → In Progress → Final。
last_updated: 2026-08-15
related:
  - site-lifecycle
  - subjects
  - issue-management
  - dashboards
---

## 访视类型

**Monitoring Event**（监查事件）是 CRA 现场/远程监查的计划与执行载体，出厂支持四类核心访视：

| 类型 | 含义 |
|------|------|
| **PSV**（Pre-Study Visit） | 研究前访视 |
| **SIV**（Site Initiation Visit） | 机构启动访视 |
| **IMV**（Interim Monitoring Visit） | 中期监查访视 |
| **COV**（Site Close Out Visit） | 机构关闭访视 |

## 访视状态（主路径）

| 状态 | 含义 | 可执行操作 |
|------|------|------------|
| **Expected** | 已登记、待排期 | **Plan Visit** |
| **Planning** | 排期中 | **Confirm Visit** |
| **Confirmed** | 已确认 | **Start Trip Report** |
| **In Progress** | 访视进行中 | **Start Review** 等 |
| **In Review → Passed Review → Final** | 审查至定稿 | **Complete Review** → **Finalize** |

## 创建监查访视

1. 导航 **Site Monitoring → Monitoring Events** → 创建，选择访视类型（如 **Interim Monitoring Visit**）。
2. 填写：

| 字段 | 说明 |
|------|------|
| **Name** | 访视名称（如 `CTMS-IMV-20260802`） |
| **Study / Study Country / Study Site** | 三者均为必填 |
| **Study Person** | 选已入队的 CRA |
| **Planned Start / Planned End** | 计划起止日期 |

保存后状态为 **Expected**。

## 推进全生命周期

| 步骤 | 操作 | 状态变化 |
|------|------|----------|
| 1 | **Plan Visit**，确认计划起止日期 | Expected → **Planning** |
| 2 | **Confirm Visit** | → **Confirmed** |
| 3 | **Start Trip Report**，填 Actual Start/End Date | → **In Progress** |
| 4 | **Start Review** | → **In Review** |
| 5 | **Complete Review** | → **Passed Review** |
| 6 | **Finalize** | → **Final** |

> 进入 Planning / Confirmed / In Progress 时，系统可能自动播种 Follow-Up / Issues / Monitored Enrollment 相关数据；列表为空不影响主路径。

## 在仪表盘查看

- **CRA Homepage → Monitoring Plan**：列出按范围裁剪的访视计划，可下钻到 Monitoring Event 详情。
- **Study Management Homepage → Monitoring Status**：按访视类型分布计数。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 创建 Monitoring Event 校验失败 | Study、Study Country、Site 三者均必填 |
| Homepage Monitoring Status 为空 | 确认已选对本 Study，且访视的 Study/Country/Site 绑定正确 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Monitoring Event：Create、Read、Edit | 创建并维护访视 |
| 生命周期动作 | Monitoring Event：**Plan Visit**、**Confirm Visit**、**Start Trip Report**、**Start Review**、**Complete Review**、**Finalize** | 访视全生命周期 |
| 对象 | Study Person：Read | 分配 CRA（研究团队须已入队） |

监查访视要求 Study / Country / Site 三者绑定；CRA 通常只见自己被分配或所属范围内的访视。
