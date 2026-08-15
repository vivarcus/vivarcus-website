---
title: 文档审阅、批准与升版
description: 学习文档受控生命周期的完整流转：提交审查、内容审阅、QC、批准、电子签名，以及方案修订时的文档升版。
last_updated: 2026-08-15
related:
  - upload-documents
  - quality-issues
  - milestones
---

## 文档生命周期

文档在 Vivarcus 中经历受控的生命周期，典型流转：

| 状态 | 含义 |
|------|------|
| **In Progress** | 草稿（版本约 0.1） |
| **In Review** | 已提交，等待内容审阅 |
| **In QC Review** | 内容审阅通过，等待 QC |
| **In Approval** | QC 通过，等待批准 |
| **Approved** | 已批准（版本约 1.0），进入稳态 |

## 提交审查

打开文档详情 → **All Actions → Submit for Review**：

1. 指定 **Reviewer** 与 **QC Reviewer**（单账号试用时可选自己）。
2. 填写 **Due Date**，提交。状态变为 **In Review**。

## 审查、QC 与批准

| 任务 | 操作 | 结果 |
|------|------|------|
| **Review Content** | 在 **My Tasks** 中完成，选择 **Send to QC** | 状态变为 In QC Review |
| **QC Review** | 完成，选择 **Passed** | 状态变为 In Approval |
| **Approve Document** | 文档 **All Actions → Approve**，指定 Approver 提交；在 **My Tasks** 完成批准任务（含电子签名，若系统要求） | 状态变为 Approved，版本约 1.0 |

> 时间有限时可走快捷方式：直接 **All Actions → Promote to Approved**，跳过审查步骤。

## 文档升版

方案修订或内容更新需要升版：

1. 对已批准文档执行 **New Version In Progress**（或 **Upload New Version**）。
2. 上传新文件（可选修改 Name，如 `EXP-Protocol-v2`），保存。
3. 再次走审查批准（或 **Promote to Approved**）。

同一文档族保留版本历史，稳态版本号前进（如 **2.0**）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 找不到 Submit for Review | 确认文档已保存，且当前账号有文档操作权限 |
| 电子签名步骤无法完成 | 按页面提示操作；仍失败请联系支持 |
| 想跳过审查直接批准 | 使用 **Promote to Approved** |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Document：Read、Edit | 打开文档、提交审查、升版 |
| 生命周期动作 | Document：**Submit for Review**、**Review Content**、**QC Review**、**Approve**、**Promote to Approved** | 推进文档生命周期 |
| 工作流 | 电子签名（e-signature）、Read & Understood | 批准签名与通知分发（按工作流配置） |
| 对象 | Clinical User Task：Read、Edit | 在 My Tasks 完成审查任务 |

单账号试用时同一账号可完成全部步骤；多角色环境由管理员按职责授予对应生命周期动作。
