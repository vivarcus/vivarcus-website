---
title: 研究人员与通信（研究团队 / 组织 / 通信日志）
description: 了解 Study Personnel & Communication 标签的三个子页：研究团队（研究人员）、研究组织与研究通信日志的字段与创建入口。
last_updated: 2026-08-15
related:
  - site-lifecycle
  - global-directory
  - study-lifecycle
---

## 研究人员（Study Personnel）

**Study Person** 把全局目录人员挂到研究（及国家/中心），指定团队角色与起止日期。**Study Personnel & Communication → Study Personnel** 创建：

| 字段 | 说明 |
|------|------|
| **Person** | 人员（必填），从全局目录选择或内联创建 |
| **Full Name** | 自动带出 |
| **Study** | 所属研究（必填） |
| **Study Country / Study Site** | 按研究→国家→中心级联 |
| **Study Team Role** | 团队角色（必填）：CRA、Lead CRA、Study Manager、CTMS Study Manager、Contributor、Central Monitor、CTA 等 |
| **Primary Contact Information** | 主要联系信息（可内联创建） |
| **Grant Access to Related Records** | 勾选后生成 User Role Setup 授予相关记录访问权 |
| **Start / End Date** | 任职起止日期 |

> 关于访问授权（URS）与按角色生成预期文档的机制，见 [研究人员与用户角色设置](../etmf/study-personnel.html)。人员退出团队用 **Make Inactive**（自动清访问权限并置结束日期）。

研究团队可细化到**职责**：`Study Person Responsibility` 把人员与研究/国家/中心挂上具体职责（Principal Investigator、Subinvestigator、Clinical Research Coordinator、Regulatory Coordinator、Pharmacist、Study Nurse 等 10 类预置职责），在人员详情页维护。

## 研究组织（Study Organizations）

**Study Organization** 记录哪些组织参与了研究（可到国家/中心），**Study Personnel & Communication → Study Organizations** 创建：

| 字段 | 说明 |
|------|------|
| **Organization** | 组织（必填），从全局目录选择或内联创建 |
| **Study** | 所属研究（必填） |
| **Study Country / Study Site** | 可选，级联限定 |
| **Location** | 组织地点（按所选组织过滤） |
| **Primary Payee** | 是否主要付款方 |
| **Start / End Date** | 参与起止日期 |

组织也可从 **Study / Study Country / Study Site** 详情页的 **Study Organizations** 区创建；组织详情页 **Study Participation** 区反向展示其参与的所有研究。

## 研究通信日志（Study Communication Log）

**Study Communication Log** 记录与中心/研究人员的通信往来（呼叫、邮件、传真、信函），形成可审计记录。两种类型：

| 类型 | 说明 |
|------|------|
| **Site Communication**（默认） | 中心通信；研究/国家/中心/通信对象必填 |
| **Other Communication** | 其他通信；层级与对象均可选 |

| 字段 | 说明 |
|------|------|
| **Communication Type** | 通信类型（必填）：`Call` / `Email` / `Fax` / `Letter` / `Other` |
| **Primary Communication With** | 主要通信对象（如主要研究者） |
| **Responsible Person** | 负责人员（必填） |
| **Contact Date** | 首次联系时间 |
| **Description** | 摘要（必填，≤75 字符） |
| **Detail** | 详细内容（供审计方理解通信目的与结果） |
| **Related Inquiry** | 关联往来记录，形成通信链 |

创建入口：**Site** 详情页的 **Study Site Communications** 区（中心通信）；**Study / Study Country** 详情页对应区（其他通信）；以及本子页列表。通信记录可被方案偏离（PDV）的 **Related Communication** 字段引用。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 团队角色列表没有 Principal Investigator | 角色来自 Study Team Role 主数据，可由管理员扩展；PI/Sub-I 角色会额外触发预期文档生成 |
| 组织列表选不到 CRO/IRB 类型 | 本版本组织不按 Sponsor/CRO/Site 枚举区分，用 **Organization Type**（如 Institution）与 Primary Payee 表达 |
| 通信日志必填项报错 | Site Communication 类型要求研究/国家/中心与通信对象；不涉及中心的通信用 Other Communication 类型 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study Person：Create、Read、Edit | 维护研究团队（不可删除，用 Make Inactive） |
| 对象 | Study Organization：Create、Read、Edit | 维护研究参与组织 |
| 对象 | Study Communication Log：Create、Read、Edit | 记录通信往来 |

**CTMS Study Manager**、**CRA** 与 **Central Monitor** 均可维护团队与通信；**CTMS Business Administrator** 可删除记录；**Document Contributor** 只读。
