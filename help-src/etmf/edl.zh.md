---
title: EDL 与预期文档（Expected Documents）
description: 了解预期文档清单（EDL）与预期文档条目（EDL Item）的概念、匹配规则、从条目创建文档的推荐路径，以及匹配文档与 更新相关预期文档两个常用动作。
last_updated: 2026-08-15
related:
  - upload-documents
  - tmf-homepage
  - overview
---

## 什么是 EDL

EDL（Expected Document List，预期文档清单）是 TMF 的「应收清单」：描述这份试验主文件应收集哪些文档、需要几份、是否必填。EDL 由管理员用模板配置，在研究执行 **计划研究** 时自动生成到研究（及国家/中心）上。

EDL 的条目称为**预期文档（EDL Item / Expected Document）**。系统以 EDL 为准绳判断文档完整度，也是文档自动归档的目标位置来源。

## 推荐路径：从 EDL Item 创建文档

推荐**从 EDL Item 直接创建文档**——系统会自动带出研究、分类等字段，匹配成功率最高：

1. 打开研究 → **预期文档** 列表，任选一条条目打开详情。
2. 详情页显示 **文档类型 / Classification**、**# Expected**、**Completeness** 等字段；下方 **Matched Documents** 区域初始为空。
3. **所有操作 → 创建文档**，选择创建方式（Upload / Placeholder / From Template），填写 Name 并上传文件，保存。

> 从 EDL Item 创建文档时，系统**仅自动填充字段**，不会立即建立匹配关系；匹配在文档保存后由系统自动完成。

## 匹配规则

文档与 EDL Item 的对应关系由系统**自动匹配**维护。系统在配置的匹配字段（通常包括 Study、Study Country、Site、Classification 等）上比对：

- 配置的**全部**匹配字段值一致 → 建立匹配
- 两边某字段都为空 → 视为一致
- 一边有值、另一边为空 → **不匹配**

手工创建文档时，须确保这些字段与 EDL Item 对齐。

## 常用动作

| 动作 | 用途 |
|------|------|
| **匹配文档** | 对该条目执行一次匹配，刷新 Matched Documents 与计数 |
| **更新相关预期文档** | 将当前条目的 **# Expected** 和 **Requiredness** 同步到同研究内的相关条目（如国家/中心级对应条目） |
| **创建文档** | 从条目创建文档（上传 / 占位 / 从模板） |

> 更新相关预期文档仅同步份数与必要性，不涉及文档匹配。

## 查看完成度

条目详情页的计数与状态：

| 字段 | 含义 |
|------|------|
| **All Doc Count** | 匹配到的全部文档数 |
| **Steady State Doc Count** | 其中已批准的稳态文档数 |
| **Completeness** | 达标时显示 **Complete** |

> 若 All Doc Count 有值但 Steady State 为 0，说明匹配文档尚未批准；完成批准流程后再查看。

## 预期文档条目（EDL Item）

**计划 → 预期文档** 列表汇总全库的 EDL Item 条目；每条属于某个 EDL，代表「某个位置需要收齐的一种文档」。打开条目详情可查看：

- **文档类型 / Classification** 与 **# Expected**（应收集份数）、**Requiredness**（是否必填）
- **Completeness** 完成度计数与 **Matched Documents** 匹配文档区
- **所有操作** 提供 **创建文档**、**匹配文档**、**Update Related Expected Documents**（见上文「常用动作」）

按研究打开 **预期文档** 相关列表（如研究详情页）可只看该研究的条目；国家/中心级的条目可在研究国家/地点详情页查看。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| Matched Documents 为空 | 确认文档的 Study、Classification 等与 EDL Item 一致；等待几秒刷新，或执行 **匹配文档** |
| Completeness 仍为 Not Started | 文档须先保存；匹配字段须完全对齐 |
| Update Related 后相关条目未变 | 确认同研究内存在对应的国家/中心级相关条目 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | EDL / EDL Item：Read、Edit | 查看预期文档清单与条目、编辑 # Expected 与 Requiredness |
| 对象动作 | EDL Item：**创建文档**、**匹配文档**、**更新相关预期文档** | 从条目创建文档、手动匹配、同步相关条目 |
| 对象 | Document：Create、Edit | 保存新文档（匹配在保存后自动发生） |

**Document Contributor** 具备 EDL 与文档的读写权限；只读角色（如 **External Inspector**）可查看 Matched Documents 与计数，但无法执行动作。
