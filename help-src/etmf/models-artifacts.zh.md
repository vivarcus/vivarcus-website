---
title: 参考模型与工件（Models & Artifacts）
description: 了解 TMF 参考模型（Model）与工件（Artifact）层级、出厂预置的模型与工件树，以及文档分类到工件的映射如何支撑自动归档与 TMF 查看器。
last_updated: 2026-08-15
related:
  - tmf-viewer
  - document-types
  - overview
---

## 参考模型（Model）

**Model**（参考模型）是 TMF 参考模型的容器——例如 DIA TMF 参考模型 v2.0 / v3.0。**管理员设置 → 参考模型** 维护：

| 字段 | 说明 |
|------|------|
| **Name** | 模型名（必填且唯一） |
| **Description** | 模型说明 |
| **Display in TMF Viewer** | 是否在 TMF 查看器中展示（默认是） |

出厂预置 5 个模型：

| 模型 | 用途 |
|------|------|
| **TMF RM v2.0**（2012） | DIA TMF 参考模型 v2.0 |
| **TMF RM v3.0**（2015） | DIA TMF 参考模型 v3.0 |
| **Document Type Hierarchy** | 按文档类型层级浏览 |
| **Vault Clinical Docs** | Vault 临床文档模型 |
| **Binder Section to Document Type** | 自动归档模型：按文档的 Type/Subtype/Classification 匹配 Binder Section 名称归档 |

## 工件（Artifact）

**Artifact**（工件）是参考模型内的层级节点（Zone / Section），构成 TMF 标准层级树，如 `01 Trial Management → 01.01 Trial Oversight → 01.01.01 Trial Master File Plan`。**管理员设置 → 工件** 维护：

| 字段 | 说明 |
|------|------|
| **Model** | 所属参考模型（必填） |
| **Name** | 工件名 |
| **Number** | 层级编号，如 `01.01.01` |
| **Parent Artifact** | 上级工件，自引用建树 |
| **Description** | 工件定义文本（取自 TMF 参考模型） |

> 出厂预置 TMF RM v2.0 的完整工件树，各工件带官方定义文本，可作内部 SOP 与稽查对照的标准层级。

## 与文档归档的关系

Document Type 上的 **eTMF RM v2.0 / eTMF RM v3.0 / Vault Clinical Docs** 字段把文档分类映射到工件（见 [文档类型](document-types.html)）；**Binder Section to Document Type** 模型则按文档分类匹配归档位置。两者结合实现：文档保存后自动归档到参考模型对应的位置，并在 **TMF 查看器**中按模型-工件层级浏览（见 [TMF 查看器](tmf-viewer.html)）。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Model / Artifact：Create、Read、Edit | 维护参考模型与工件树 |

模型与工件为系统管理主数据，出厂已配好；**Clinical Application Administrator** 可按需增改，**Document Contributor** 只读。
