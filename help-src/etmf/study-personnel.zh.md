---
title: 研究人员与用户角色设置
description: 了解如何把人员加入研究团队、授予相关记录访问权限（URS）、按角色生成预期文档，以及 User Role Setup 记录的结构与维护。
last_updated: 2026-08-15
related:
  - study-hierarchy
  - edl
  - overview
---

## 研究人员（Study Personnel）

**Study Person**（研究人员）把人员（Person）挂到研究（及国家/中心）上，并指定其**研究团队角色（Study Team Role）**与起止日期。研究团队是研究联系人的来源，也是「按角色生成预期文档」的依据。

在 **管理员设置 → 研究人员** 创建：

| 字段 | 说明 |
|------|------|
| **Person** | 人员（必填），可从全局目录选择或内联创建 |
| **Full Name** | 自动带出 |
| **Study** | 所属研究（必填） |
| **研究国家/地区 / 研究地点** | 按研究→国家→中心级联选择 |
| **Study Team Role** | 团队角色（必填），如 Study Manager、Contributor、CRA 等 |
| **Grant Access to Related Records** | 勾选后系统为该人员创建 User Role Setup 记录，授予相关记录访问权 |
| **Start / End Date** | 任职起止日期 |

> 勾选 **Grant Access to Related Records** 是让团队成员实际打开研究数据的关键一步；未勾选时人员仅作为联系人登记，不获得记录访问权限。

人员角色变化会**按角色生成预期文档**：详情页 **预期文档** 区展示基于其角色生成的 EDL Item。常用动作：

| 动作 | 用途 |
|------|------|
| **Create Study Contact**（含 In Bulk） | 快速创建研究联系人 |
| **Resend Study Invitation**（含 In Bulk） | 重发研究邀请通知 |
| **Make Inactive** | 人员退出团队（保留历史记录） |
| **Retrigger EDL Item Creation** | 角色变化后重新生成预期文档条目 |

## 用户角色设置（User Role Setup）

**User Role Setup（URS）** 是系统管理的**记录级安全**对象：一条记录代表「某用户在某研究/国家/中心上下文中拥有某角色」的授权。它通常**由系统自动生成**——例如勾选研究人员的 Grant Access to Related Records 时；管理员在 **管理员设置 → 用户角色设置** 中查看与维护。

| 字段 | 说明 |
|------|------|
| **User** | 被授权用户 |
| **Role** | 授予的角色（如 study_manager、contributor） |
| **研究 / 研究国家/地区 / 研究地点** | 授权范围，级联限定 |
| **Blinding** | 设盲范围（如 Blinded / Unblinded） |
| **Name** | 系统自动编号：`DAC-{######}` |

> URS 是 Vault 记录级安全（Dynamic Access Control）的基础。修改团队访问权限时，优先调整 Study Person 的 Grant Access 与角色，而不是手工编辑 URS 记录。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 团队成员看不到研究数据 | 确认 Study Person 已勾选 **Grant Access to Related Records**，且团队角色与研究 Sharing 匹配 |
| Expected Documents 区为空 | 角色未触发预期文档生成，可执行 **Retrigger EDL Item Creation** |
| URS 记录异常 | 多数场景由系统维护；手工修改前先确认 Grant Access 与角色设置是否正确 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study Person：Create、Read、Edit | 维护研究团队与联系人 |
| 对象动作 | Study Person：**Create Study Contact**、**Resend Study Invitation**、**Retrigger EDL Item Creation** | 联系人、邀请与预期文档生成 |
| 对象 | User Role Setup：Read（Create、Edit） | 查看（管理）记录级授权 |

**Clinical Application Administrator** 可完整管理研究人员与 URS；**Document Contributor** 对研究人员只读。
