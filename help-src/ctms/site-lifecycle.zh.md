---
title: 中心生命周期：Candidate 到 Active
description: 学习国家与中心的完整生命周期：Select Country、Qualify Site、Select Site、Initiate Site，以及 On Hold 与 Will Not Participate 两条异常路径。
last_updated: 2026-08-15
related:
  - study-lifecycle
  - subjects
  - monitoring-visits
---

## 中心状态主路径

| 状态 | 含义 | 关键动作 |
|------|------|----------|
| **Candidate** | 候选 | **Qualify Site** / **Place Site on Hold** / **Site Will Not Participate** |
| **Qualifying** | 资格认定中 | **Select Site** |
| **Initiating** | 启动中 | **Initiate Site**（需父 Study 已 Active） |
| **Active** | 已激活，可入组 | 日常运营 |

## 创建并选定国家

1. **Study Countries** → Create：**Study** 选研究，**Country** 选国家/地区，保存（状态 Candidate，Name 自动生成）。
2. 打开国家详情 → **All Actions → Select Country**，填 **Country Selected Date**，提交。状态变为 **Initiating**，可生成国家级里程碑。

> 中心进入 Initiating 要求父 Country **不是** Candidate——CTMS 的中心启动必须先走这一步，不能只建记录。

## 主路径：Candidate → Qualifying → Initiating → Active

| 步骤 | 操作 | 结果 |
|------|------|------|
| 1 | **Study Sites** → Create：**Study Site Number** = `Site-001`，**Study Country** 选国家记录；**Study Number** 留空（自动推导） | 状态 Candidate |
| 2 | **All Actions → Qualify Site** | 状态 Qualifying，可生成中心级里程碑 |
| 3 | **All Actions → Select Site**，填 **Site Selected Date** | 状态 Initiating |
| 4 | 确认父 Study 已 Active → **All Actions → Initiate Site** | 状态 Active |

## 异常路径：On Hold

对 Candidate 中心执行 **Place Site on Hold**，填写 Hold 原因（如 `PI on medical leave`），状态变为 **Qualifying Hold**。恢复时执行 **Remove Site Hold**，回到 Qualifying 后可继续 Select / Initiate。

## 异常路径：不参与

对 Candidate 中心执行 **Site Will Not Participate**，填写 Reason / Notes（如 `Imaging capability insufficient`），状态变为 **Not Selected**。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| Qualify Site 失败 | 父 Study 不能仍是 Candidate；先完成 Plan Study |
| Select Site / Initiate Site 失败 | Country 须先 Select Country；Initiate Site 要求父 Study 为 Active |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study Country / Study Site：Create、Read、Edit | 创建国家与中心 |
| 生命周期动作 | Study Country：**Select Country** | 国家选定（中心启动的前置） |
| 生命周期动作 | Study Site：**Qualify Site**、**Select Site**、**Initiate Site**、**Place Site on Hold**、**Remove Site Hold**、**Site Will Not Participate** | 中心生命周期主路径与异常路径 |

注意生命周期门禁：Initiate Site 要求父 Study 已 Active，且父 Country 已完成 Select Country。
