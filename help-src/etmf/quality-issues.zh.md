---
title: 质量问题（Quality Issues）
description: Quality Issue 记录文档缺陷并跟踪从发现到关闭的整改。了解四种状态、创建方式、与文档的双向关联，以及在 TMF 主页中的统计视图。
last_updated: 2026-08-15
related:
  - review-workflow
  - tmf-homepage
  - tmf-viewer
---

## 什么是 Quality Issue

TMF 文档在生命周期中可能出现各种缺陷：缺页、签名不完整、内容错误、版本混乱等。**Quality Issue（质量问题）** 用于记录这些缺陷、关联到具体文档，并跟踪从发现到关闭的整改进度——是 TMF 质量闭环的核心工具，也用于记录稽查发现。

## 状态流转

| 状态 | 含义 | 可执行动作 |
|------|------|------------|
| **Initiated** | 已记录，尚未分配/跟进 | **打开** |
| **打开** | 跟进中，等待整改 | **Close** |
| **已关闭** | 已解决/已验证 | **Deactivate** |
| **非活动** | 已归档（不在默认列表出现） | 只读 |

典型流转：**Initiated → 打开 → 已关闭**；需要从活跃视图移除时再 Deactivate。

> **Close vs Deactivate**：Close 表示问题已解决，记录仍在活跃视图可查；Deactivate 是归档操作，将记录移入 Inactive。

## 创建质量问题

推荐从文档创建（自动预填关联）：

1. 打开文档详情 → **质量问题** 相关对象区 → **Create**（从文档创建时 Related Document / Study 已预填）。
2. 填写：

| 字段 | 说明 |
|------|------|
| **Quality Issue ID** | 系统自动编号 `QI-{######}`（中文界面中该字段标签为 Quality Issue ID，非"名称"） |
| **Study** | 所属研究 |
| **Related Document** | 关联有缺陷的文档 |
| **QC Issue Type** | Missing / Inaccurate Content / Duplicate / Expired / Incomplete Metadata / Misclassified / Signature Not Present |
| **分配给** | 整改责任人 |
| **Due Date** | 要求解决日期 |
| **QC Issue Comments** | 缺陷具体描述 |

## 双向关联

QI 与文档是双向关联的：从 QI 详情可点击 **Related Document** 跳转到缺陷文档；在文档详情也能看到挂载的质量问题——审计时追溯链路完整。

## 在 TMF 主页查看

**TMF 主页 → 质量问题** Widget 按类型分组展示，可过滤 **打开 / 已关闭 / 全部 / 分配给我的**。创建并 Open 的 QI 会出现在 Open 视图中。

> 需要在相关文档类型上配置 Quality Issue 字段后，该类型文档的质量问题才会出现在 Homepage。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Quality Issue：Create、Read、Edit | 创建并维护质量问题 |
| 生命周期动作 | Quality Issue：**打开**、**Close**、**Deactivate** | 推进整改闭环 |
| 对象 | Document：Read | 从文档创建 QI 并查看双向关联 |

创建 QI 的入口通常挂在文档详情页的相关对象区；对文档有 Read 权限即可看到该文档挂载的质量问题。
