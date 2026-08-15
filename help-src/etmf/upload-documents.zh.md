---
title: 上传文档与文档匹配
description: 学习从 EDL Item 创建并上传文档的推荐路径、三种创建方式（Upload / Placeholder / From Template），以及从文档库手工创建的备选路径。
last_updated: 2026-08-15
related:
  - edl
  - review-workflow
  - tmf-viewer
---

## 从 EDL Item 创建文档（推荐）

推荐**从 EDL Item 直接创建文档**，系统自动带出研究、分类等字段，匹配成功率最高：

1. 打开研究 → **Expected Documents** 列表，选择一条条目（如 Protocol 相关）打开详情，确认 **Document Type / Classification**、**# Expected**、**Completeness** 等字段。
2. **All Actions → Create Document**。
3. 选择创建方式（见下），填写 Name（如 `EXP-Protocol-v1`），确认 Study、Document Type / Classification 已自动带出，上传 PDF，保存。

文档创建成功后状态为 **In Progress**，版本约 **0.1**。

## 三种创建方式

| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **Upload** | 上传源文件（PDF 等） | 有现成文件的常规场景 |
| **Placeholder** | 创建无文件的占位文档 | 文件暂未拿到，先占位 |
| **From Template** | 从文档模板创建 | 该文档类型配置了可用模板 |

> 从 EDL Item 创建文档时，系统**仅自动填充字段**，不会立即建立匹配关系；匹配在文档保存后由系统自动完成（见 [EDL 与预期文档](edl.html) 的匹配规则）。

## 从文档库创建（备选）

若不从 EDL Item 入口创建：

1. 进入 **Documents**（文档库）→ **Create**。
2. 手工填写 **Study** 与 **Document Type / Classification**（须与目标 EDL Item 一致）。
3. 上传文件并保存。

手工创建时字段对齐是匹配成功的关键：配置的全部匹配字段值一致才建立匹配。

## 保存后发生了什么

- 文档进入受控生命周期（In Progress），可提交审阅（见 [审阅与批准](review-workflow.html)）。
- 系统自动对相关 EDL Item 执行匹配；结果可见于条目的 **Matched Documents** 区域。
- 已批准且分类映射到参考模型的文档，会自动归档到 Master File Binder（见 [TMF Viewer 与 Master File Binder](tmf-viewer.html)）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 找不到 Create Document | 确认当前账号有预期文档操作权限；条目状态为 Active |
| Matched Documents 为空 | 确认文档的 Study、Classification 等与 EDL Item 一致；等待几秒刷新，或执行 Match Documents |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Document：Create、Edit | 上传源文件、保存文档 |
| 对象动作 | EDL Item：**Create Document** | 从预期文档条目创建（推荐路径） |
| 对象 | EDL Item：Read | 查看条目详情与 Matched Documents |

**Document Contributor** 具备上述权限。只读角色可浏览文档库，但不能创建或上传。
