---
title: 问题与方案偏离
description: 了解 Issue 的四种类型（Protocol Deviation / Observation / Protocol Violation / Risk Mitigation Action）、创建与推进方式、开始方案偏离审查的团队前置条件，以及与 eTMF 质量问题的对照。
last_updated: 2026-08-15
related:
  - subjects
  - monitoring-visits
  - overview
---

## Issue 类型与常用动作

**Issue** 捕获方案偏离、观察项等过程问题，可关联研究 / 中心 / 受试者，并与 eTMF 质量问题同平台共存。

| 类型 | 起始状态 | 常用动作 |
|------|----------|----------|
| **Protocol Deviation**（试验方案偏离） | **打开** | **开始方案偏离审查** |
| **Observation**（观察） | **打开** | **解决问题** 或 **Promote to Protocol Deviation** |
| **Protocol Violation**（试验方案违背） | **打开** | 按页面可用动作推进 |
| **Risk Mitigation Action**（风险缓解措施） | **打开** | **Assign Risk Mitigation** |

典型路径：**登记偏离（Open）→ 审查或解决 → 已解决**。

## 创建方案偏离

1. 导航 **Issue Management → Protocol Deviations**（或 **All Issues**）→ **创建**，类型选 **Protocol Deviation**。
2. 填写：

| 字段 | 说明 |
|------|------|
| **Issue Log ID** | 偏离标识（或接受系统自动编号） |
| **Study** | 必填 |
| **研究国家/地区 / 研究地点** | 建议填写，便于仪表盘裁剪 |
| **Subject** | 关联受试者 |
| **Date Identified** | 发现日期（必填） |
| **Date of Issue** | 实际发生日 |
| **Summary** | 摘要（必填），如 `Visit window deviation: Cycle 1 Day 25 (window Day 21±3)` |
| **Category** | 分类，如 `F. 访视计划 Visit Schedule` |
| **Severity** | 严重性，如 `Minor` |
| **Description** | 详细描述 |

## 推进偏离（正式路径）

1. 在偏离详情填写 **Resolution**（解决方案）与 Root Cause（根本原因，可选），保存。
2. **所有操作 → 开始方案偏离审查**：
   - **Reviewer: PM** 选研究团队中的 CTMS Study Manager 成员。
   - **Reviewer: Medical** 选 Contributor 成员。
   - 填截止日期并提交，进入 PD 审查工作流。
3. 在 **我的任务** 完成审查任务，完成后状态趋向 **已解决**。

> **选不到人？** 参与人候选来自偏离 Sharing 中的 study_manager / contributor 角色（由研究团队 Matching Rule 写入）。确认研究团队已入队且勾选 **Grant Access to Related Records**；若偏离在入队前已创建，打开偏离 → **Sharing Settings** 手动加入这两个角色，或编辑保存一次偏离以触发 Matching 重算。

## 快捷闭环：Observation

时间有限时的简化路径：**问题管理 → 观察** → 创建，填写 Study / Site / Summary 保存（状态 Open），填写 **Resolution** 后 **所有操作 → 解决问题**，状态变为 **Resolved**（Resolved Date 自动写入）。

> Protocol Deviation 与 Observation 可用动作不同：Observation 用 **解决问题**；PD 优先 **开始方案偏离审查**。Resolved 通常要求 Resolution 非空。

## 风险缓解措施（Risk Mitigation Action）

**Risk Mitigation Action（RMA）** 登记针对研究风险的缓解行动——「识别出风险后，决定做什么、由谁完成」。它与偏离/观察同属 Issue 对象、共用生命周期，但走专用的指派流程。**问题管理 → Risk Mitigation Actions** → 创建：

| 字段 | 说明 |
|------|------|
| **Study** | 所属研究（必填，从研究风险评估带入） |
| **研究国家/地区 / 研究地点** | 可选，按范围裁剪 |
| **Study Risk Assessment / Study Risk / Study Risk Mitigation** | 关联的风险链：风险评估 → 风险 → 风险缓解措施 |
| **Date Identified** | 识别日期（必填） |
| **Summary** | 摘要（必填），如 `增加筛选期实验室复测` |
| **Description** | 缓解措施的具体描述 |
| **Resolution** | 解决方案（进入 Resolved 前必填） |

## 指派与闭环（Assign Risk Mitigation）

**所有操作 → Assign Risk Mitigation** 启动 **完成风险缓解** 工作流：

| 步骤 | 内容 | 状态 |
|------|------|------|
| 1 | 选择 **Mitigation Owner**（缓解措施负责人）并提交 | → **Assigned** |
| 2 | 负责人收到 **Complete Mitigation Action** 任务，按 Description 完成缓解措施并填写 **Resolution** | 任务完成 |
| 3 | 系统自动收尾 | → **Resolved**（**Resolved Date** 自动写入） |

> 与其他类型一样，RMA 也可走通用动作（**Investigate / Implement / Escalate / 解决问题**）；**Change Issue Type** 可在 Issue 类型间转换（如 Observation 提升为 Risk Mitigation Action）。

## 与 eTMF 质量问题对照

同一 Vault 中过程侧 Issue 与文档侧 Quality Issue 并存：Issue 记录"过程出了什么问题"（偏离、观察），Quality Issue 记录"文档出了什么缺陷"（缺页、签名不完整）。稽查时可相互引用，形成「过程偏离 ↔ 文档质量」的完整追溯。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Issue（Protocol Deviation / Observation）：Create、Read、Edit | 登记与维护问题 |
| 对象动作 | Issue：**开始方案偏离审查**、**解决问题**、**Assign Risk Mitigation**、**Change Issue Type** | 审查、闭环与缓解措施指派 |
| 团队角色 | Study Person：**CTMS Study Manager** + **Contributor** 入队并 Grant Access | Start PD Review 的审查人候选来源 |
| 对象 | Clinical User Task：Read、Edit | 在我的任务完成审查任务 |

若偏离在入队前创建导致选不到人：打开偏离 → **Sharing Settings** 手动加入角色，或编辑保存一次触发 Matching 重算。
