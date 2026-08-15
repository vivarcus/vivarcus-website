---
title: 受试者注册与状态追踪
description: 学习受试者记录的状态流转（Consented → In Screening → Enrolled）、注册字段填写，以及筛选失败等异常路径的登记。
last_updated: 2026-08-15
related:
  - site-lifecycle
  - monitoring-visits
  - issue-management
---

## 受试者常用状态

| 状态 | 含义 |
|------|------|
| **Consented** | 已知情同意 |
| **In Screening** | 筛选中 |
| **Screen Failure** | 筛选失败 |
| **Enrolled** | 已注册（入组） |
| **Withdrawn** | 已撤回（退出） |

## 注册并入组

1. 进入 **Subjects** 列表 → **Create**。
2. 填写：

| 字段 | 说明 |
|------|------|
| **Subject ID** | 受试者标识（如 `CTMS-OV-20260802-001`） |
| **Study** | 所属研究 |
| **Study Country** | 研究国家/地区 |
| **Study Site** | 研究地点——须为 **Active** 中心 |
| **Subject Status** | 先 `Consented`，再 `In Screening`，最后 `Enrolled`（可分次保存） |
| **Initial Consent Date** | 知情同意日 |
| **Screened Date** | 筛选日 |
| **Enrolled Date** | 入组日 |

## 筛选失败（异常路径）

创建另一条受试者记录，**Subject Status** = `Screen Failure`，填 **Screen Failed Date**，保存。异常路径入账后便于与入组成功例对照，也可被问题/偏离记录引用。

## 受试者访视

受试者访视（Subject Visit）记录「某位受试者的某次访视」的计划与执行情况，在 **Study Info → Subject Visits** 中管理：

| 字段 | 说明 |
|------|------|
| **Subject** | 所属受试者（必填） |
| **Visit / Visit Name / Visit Sequence** | 访视定义、名称与序号（如 `Cycle 1 Day 1`） |
| **Visit Status** | 访视状态，如 `Planned`（已计划） |
| **Planned Date** | 计划访视日期 |
| **Visit Date** | 实际访视日期；逾期时可用 **Overdue Date** 标记跟踪 |

创建访视记录时先选 **Subject**，再按研究计划填写访视定义与计划日期；执行后更新 **Visit Date** 与状态，即可在受试者详情中看到该受试者的完整访视轨迹。

## 与偏离/访视的关联

受试者记录是入组进度与偏离追溯的锚点：

- **Protocol Deviation / Issue** 可关联 **Subject** 字段，指明问题发生在哪位受试者身上（见 [问题与方案偏离](issue-management.html)）。
- 监查访视中登记的入组数据与受试者记录同源，便于范围裁剪核对（见 [监查访视](monitoring-visits.html)）。

> 注册指标与仪表盘的部分汇总依赖后台播种与前端聚合，试用环境可能显示 0 或空图，属已知差异；重点是受试者记录本身可建、可查、可被偏离引用。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Subject：Create、Read、Edit | 注册受试者并推进状态 |
| 字段 | Subject 状态字段（Subject Status 等）：Edit | Consented → In Screening → Enrolled 状态推进 |

受试者须挂在 Active 中心下；对中心无 Read 权限的用户不会在列表中看到该中心的受试者。
