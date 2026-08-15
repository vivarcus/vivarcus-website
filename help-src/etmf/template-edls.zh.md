---
title: 模板 EDL 与预期文档模板
description: 了解 Template Expected Document List（模板 EDL）的层级结构与 Template Expected Documents（预期文档模板）的关键字段，以及模板变更如何影响既有研究。
last_updated: 2026-08-15
related:
  - edl
  - document-types
  - study-hierarchy
---

## 概念：模板 → 研究

**Template EDL**（预期文档列表的模板）定义「某个层级应收集哪些文档」的清单模板，可复用到多个研究；它的条目叫 **Template Expected Document**（预期文档的模板）。研究执行 **计划研究** 时选择模板 EDL，系统把模板复制为研究级 EDL 与 EDL Item（运行时条目回指源模板）。

模板 EDL 支持**层级嵌套**：通过 **Parent** 字段可让国家/中心级模板继承研究级模板（如 `Standard | Study Level` → `Standard | Country Level` → `Standard | Site Level`）。

## 创建模板 EDL

**管理员设置 → 预期文档列表的模板** → 创建：

| 字段 | 说明 |
|------|------|
| **Name** | 模板名（必填且唯一） |
| **Level** | 层级：`Study` / `Country` / `Site` |
| **Milestone Type** | 可选；限定模板适用的里程碑类型 |
| **Parent** | 可选；上级模板，用于层级继承 |

保存后在模板详情页的 **EDL Item Templates** 区添加预期文档模板条目。

## 预期文档的模板（EDL Item Template）

**管理员设置 → 预期文档的模板** 汇总全部条目；每条定义一个预期文档模板：

| 字段 | 说明 |
|------|------|
| **Name** | 条目名，如 `Clinical Study Report (CSR)` |
| **模板 EDL** | 所属模板（必填） |
| **Type / Subtype / Classification** | 文档分类三要素（来自 [文档类型](document-types.html)，不可编辑） |
| **Requiredness** | 必填性（必填）：`Required` / `Not Required` / `Pending Decision` |
| **# Expected** | 预期稳态文档份数 |
| **Department** | 负责部门，如 Biostatistics、Data Management |
| **Study Team Role / Study Organization Role / Study Product Role** | 绑定负责角色，用于按角色生成预期文档 |
| **Milestone Type / Owning Milestone Type** | 归属里程碑类型，如 `IR - First Study Site Initiated` |
| **Auto-assign Version Number** | 是否自动分配版本号 |

> 出厂预置数百条预期文档模板（CSR、Annotated CRF、Audit Certificate 等），可直接沿用或按机构 SOP 调整。

## 模板变更如何影响研究

| 字段 | 含义 |
|------|------|
| **Template Behavior** | `Reuse`（沿用）/ `Update`（更新既有研究条目）/ `Create`（新建条目） |
| **Fields to Update** | 变更推送范围，可多选：`# Expected`、`Requiredness` |

修改模板后，系统按 Template Behavior 与 Fields to Update 决定是否同步到已使用该模板的研究，实现「改一处、多研究生效」。

## 应用到研究

研究处于 **候选人** 状态时，执行 **所有操作 → 计划研究**，在弹窗中选择 **模板 EDL** 与 **里程碑主集**、填写研究开始日期，系统即按模板生成研究级 EDL（详见 [研究层级](study-hierarchy.html)）。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | 模板 EDL / Template Expected Document：Create、Read、Edit | 维护模板清单与条目 |

**Clinical Application Administrator** 管理全部模板；**Document Contributor** 只读。
