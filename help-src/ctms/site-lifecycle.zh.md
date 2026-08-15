---
title: 中心生命周期：Candidate 到 Active
description: 学习国家与中心的完整生命周期：选择国家/地区、使研究地点具有资格、选择机构、启动机构，以及 On Hold 与 Will Not Participate 两条异常路径。
last_updated: 2026-08-15
related:
  - study-lifecycle
  - subjects
  - monitoring-visits
---

## 中心状态主路径

| 状态 | 含义 | 关键动作 |
|------|------|----------|
| **候选人** | 候选 | **使研究地点具有资格** / **Place Site on Hold** / **Site Will Not Participate** |
| **合格** | 资格认定中 | **选择机构** |
| **启动** | 启动中 | **启动机构**（需父 Study 已 Active） |
| **活动** | 已激活，可入组 | 日常运营 |

## 创建并选定国家

1. **研究国家/地区** → 创建：**Study** 选研究，**Country** 选国家/地区，保存（状态 Candidate，Name 自动生成）。
2. 打开国家详情 → **所有操作 → 选择国家/地区**，填 **Country Selected Date**，提交。状态变为 **启动**，可生成国家级里程碑。

> 中心进入 Initiating 要求父 Country **不是** Candidate——CTMS 的中心启动必须先走这一步，不能只建记录。

## 主路径：Candidate → Qualifying → Initiating → Active

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | **研究地点** → 创建：**Study Site Number** = `Site-001`，**研究国家/地区** 选国家记录；**研究编号** 留空（自动推导） | 状态 Candidate |
| 2 | **所有操作 → 使研究地点具有资格** | 状态 Qualifying，可生成中心级里程碑 |
| 3 | **所有操作 → 选择机构**，填 **Site Selected Date** | 状态 Initiating |
| 4 | 确认父 Study 已 Active → **所有操作 → 启动机构** | 状态 Active |

## 异常路径：On Hold

对 Candidate 中心执行 **Place Site on Hold**，填写 Hold 原因（如 `PI on medical leave`），状态变为 **Qualifying Hold**。恢复时执行 **Remove Site Hold**，回到 Qualifying 后可继续 Select / Initiate。

## 异常路径：不参与

对 Candidate 中心执行 **Site Will Not Participate**，填写 Reason / Notes（如 `Imaging capability insufficient`），状态变为 **Not Selected**。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 使研究地点具有资格失败 | 父 Study 不能仍是 Candidate；先完成计划研究 |
| 选择机构 / 启动机构失败 | Country 须先选择国家/地区；启动机构要求父 Study 为 Active |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study Country / Study Site：Create、Read、Edit | 创建国家与中心 |
| 生命周期动作 | Study Country：**选择国家/地区** | 国家选定（中心启动的前置） |
| 生命周期动作 | Study Site：**使研究地点具有资格**、**选择机构**、**启动机构**、**Place Site on Hold**、**Remove Site Hold**、**Site Will Not Participate** | 中心生命周期主路径与异常路径 |

注意生命周期门禁：启动机构要求父 Study 已 Active，且父 Country 已完成选择国家/地区。
