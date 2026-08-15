---
title: 全局目录（Global Directory）
description: 了解 Global Directory 的四个主数据子页：组织、产品、研究产品角色与人员，以及它们如何被研究层级引用。
last_updated: 2026-08-15
related:
  - study-personnel
  - site-lifecycle
  - overview
---

## 组织

**Organization**（组织）是公司/机构/研究中心的主数据，供各研究通过 Study Organization 引用。**Global Directory → Organizations** 维护：

| 字段 | 说明 |
|------|------|
| **Organization** | 组织名（必填且唯一） |
| **Organization Type** | 组织类型（对象类型），如 `Institution` |
| **Parent Organization** | 上级组织（自引用） |
| **Status** | `Active` / `Inactive`（生命周期驱动） |

详情页 **Study Participation** 区展示该组织参与的所有研究；组织也可在研究详情页的 **Study Organizations** 区内联创建（见 [研究人员与通信](study-personnel.html)）。

## 产品

**Product**（产品）是研究使用的活性成分/资产主数据。**Global Directory → Products** 维护：**Product Name**（必填且唯一）、**Status**、**External ID**。产品通过 **Study Product**（研究产品）挂到具体研究——在 **Product** 详情页的 **Studies** 区或 **Study** 详情页的 **Study Products** 区创建，并指定该产品在本研究的角色（见下）。

## 研究产品角色

**Study Product Role**（研究产品角色）定义产品在研究中的角色，出厂预置 5 类：

| 角色 | 含义 |
|------|------|
| **Lead Agent** | 主导药物（试验药） |
| **Comparator Agent** | 对照药物 |
| **Placebo** | 安慰剂 |
| **Device** | 设备 |
| **Diagnostic** | 诊断产品 |

创建 Study Product 时选择 **Study Role**，即可表达「该产品在本研究中的作用」。

## 人员

**Person**（人员）是全局人员目录：研究者、中心人员、供应商人员、内部人员与 IRB/IEC 人员，是研究团队（Study Person）的人员来源。**Global Directory → Personnel** 维护：

| 字段 | 说明 |
|------|------|
| **First / Last Name** | 名 / 姓（必填） |
| **Email** | 邮箱（必填） |
| **Person Type** | 人员类型（对象类型）：`Internal`（默认）、`Investigator`、`Site Staff`、`Vendor`、`IRB/IEC` |
| **Vault User** | 关联 Vault 用户（唯一），同步共享字段 |
| **Manager** | 上级（自引用） |
| **External ID / CDX ID / Global ID** | 集成映射字段 |
| **Debarred / Key Opinion Leader / NPI Number** | 合规与画像标记 |

详情页 **Study Participation** 区展示该人员参与的研究团队记录；**Contact Information** 区维护联系方式。人员可执行 **Promote to User** 提升为 Vault 用户。研究人员（Study Person）的人员字段可内联创建 Person（见 [研究人员与通信](study-personnel.html)）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 组织/人员在多个研究重复登记 | 主数据建在全局目录，研究侧通过 Study Organization / Study Person 引用即可 |
| Promote to User 不可见 | 确认该人员尚未关联 Vault User，且具备相应权限 |
| 找不到某产品 | 先确认产品已在 **Global Directory → Products** 创建，再在 Study Products 区挂到研究 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Organization / Product / Study Product Role / Person：Create、Read、Edit | 维护全局目录主数据 |

**CTMS Study Manager** 可创建组织（Institution / IRB-IEC / Sponsor / Vendor 类型）、产品、产品角色与各类人员；**CRA** 与 **Central Monitor** 以查看为主；删除由 **CTMS Business/System Administrator** 执行。
