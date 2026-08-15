---
title: 文档类型（Document Types）
description: 了解 Type → Subtype → Classification 三级文档分类体系、文档编号规则、预置分类，以及与 TMF 参考模型工件的映射关系。
last_updated: 2026-08-15
related:
  - template-edls
  - models-artifacts
  - upload-documents
---

## 三级分类体系

**Document Type** 是 TMF 文档分类的主数据，采用 **Type → Subtype → Classification** 三级层次：

| 层级 | 含义 | 示例 |
|------|------|------|
| **Type** | 顶级文档大类 | Regulatory、Safety Reporting |
| **Subtype** | 大类下的细分 | Regulatory → Reports |
| **Classification** | 最细的分类 | General → Relevant Communications |

每个条目通过 **Level** 字段标记层级、通过 **Parent Type** 自引用挂到上级，构成分类树。该体系是 EDL 模板引用文档类型三要素的来源，也是文档自动归档的匹配依据。

## 预置文档类型

系统出厂预置 11 个顶级 Type（另有平台层 `General`），并各配文档编号前缀：

| Type | 编号格式 |
|------|----------|
| Regulatory | `REG-{####}` |
| Safety Reporting | `SAF-{####}` |
| Trial Management | `TM-{####}` |
| Site Management | `SITE-{####}` |
| Data Management | `DM-{####}` |
| IP and Trial Supplies | `IP-{####}` |
| IRB or IEC and other Approvals | `IRB-{####}` |
| Central Trial Documents | `CTD-{####}` |
| Central and Local Testing | `CLT-{####}` |
| Statistics | `STAT-{####}` |
| Third Parties | `TP-{####}` |

Subtype 与 Classification 同样有预置条目（如 Regulatory → Reports、Data Management → Database/Data Capture）。

## 文档编号

Type 上配置 **Document Number Format**（编号格式）与 **Start Number**（起始编号），该类型下的文档自动按格式顺序编号。新建 Type 时建议同时配置两者，避免文档无编号规则。

## 映射到参考模型工件

每个文档分类条目可映射到 TMF 参考模型工件（Artifact）：

| 字段 | 含义 |
|------|------|
| **eTMF RM v2.0 / eTMF RM v3.0** | 映射到 TMF 参考模型 v2.0 / v3.0 的工件 |
| **Vault Clinical Docs** | 映射到 Vault Clinical Docs 模型工件 |

映射后，文档可依分类在 **TMF 查看器**中按参考模型层级浏览；同时支撑 `Binder Section to Document Type` 模型——文档归档时按 Type/Subtype/Classification 匹配 Binder Section 名称（见 [参考模型与工件](models-artifacts.html)）。

## 在 EDL 模板中的使用

**Template Expected Documents** 条目通过 Type / Subtype / Classification 三字段引用本文档分类，研究侧生成的 EDL Item 继承同一分类（见 [模板 EDL 与预期文档模板](template-edls.html)）。修改分类树会影响所有引用它的模板与既有研究，变更前先评估影响面。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Document Type：Create、Read、Edit | 维护三级分类树与编号规则 |

**Clinical Application Administrator** 负责维护分类；**Document Contributor** 对分类只读。
