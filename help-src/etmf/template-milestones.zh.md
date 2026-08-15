---
title: 里程碑模板（主集 / 模板集 / 里程碑 / 依赖）
description: 了解里程碑模板的四层结构：Template Milestone Master Set、Template Milestone Set、Template Milestone 与 Template Milestone Dependency，以及它们如何驱动研究里程碑生成。
last_updated: 2026-08-15
related:
  - milestones
  - template-edls
  - study-hierarchy
---

## 四层结构

里程碑模板体系分四层，研究执行 **Plan Study** 时按主集打包应用到研究：

| 层 | 对象 | 作用 |
|----|------|------|
| 主集 | Template Milestone Master Set | 打包研究/国家/中心三个初始化集 |
| 模板集 | Template Milestone Set | 一个层级的一套里程碑（挂一个 Story Event） |
| 里程碑 | Template Milestone | 单个里程碑模板：类型、顺序、时长、完成规则 |
| 依赖 | Template Milestone Dependency | 前驱→后继的日期推算关系 |

## 模板里程碑主集（Master Set）

**Template Milestone Master Set** 把三个初始化集打包成一次绑定到研究的选择项（**Admin Setup → Template Milestone Master Sets**）：

| 字段 | 说明 |
|------|------|
| **Name** | 主集名（必填且唯一） |
| **Study Initialization Set** | 研究级初始化集（必填，须为 Study 层级模板集） |
| **Study Country Initialization Set** | 国家/地区级初始化集（必填） |
| **Study Site Initialization Set** | 中心级初始化集（必填） |

> 出厂预置 `Standard Study Level` 主集，绑定 Generic Study / Country / Site Candidate 三个初始化集，可直接使用。

## 里程碑模板集（Milestone Set）

**Template Milestone Set**（里程碑模板集）是某一层级的一套里程碑模板，挂在一个 **Story Event**（故事事件）上——事件决定该集何时被应用到研究：

| 字段 | 说明 |
|------|------|
| **Name** | 模板集名（必填） |
| **Level** | 层级（必填）：`Study` / `Country` / `Site` |
| **Story Event** | 触发事件（必填），如 `Candidate Study`、`Study Management`、`Protocol Amendment` |
| **Template Country** | 可选；限定为某国家/地区特定的集 |

出厂预置 14 个标准集（Generic Study Candidate、Study Management、First Study Site Initiated、Study Closing、Site Initiated 等），事件带创建触发器（Initialization / State Change / Ad Hoc）。

## 里程碑模板（Milestone）

**Template Milestone**（里程碑模板）是研究里程碑的蓝本（**Admin Setup → Template Milestones**）：

| 字段 | 说明 |
|------|------|
| **Milestone Type** | 里程碑类型（必填），如 `Study Start`、`First Subject In (FSI)`、`Last Subject Last Visit (LSO)`、`Database Lock` |
| **Milestone Set** | 所属模板集（必填） |
| **Sequence** | 集内顺序 |
| **Expected Duration (Days)** | 预期时长（0–2000 天） |
| **Expected Duration - Resubmit** | 重新提交的预期时长 |
| **Template EDL** | 可绑定模板 EDL，里程碑生效时生成预期文档 |
| **Template IRB / EC Type** | `Central` / `Local` |
| **Autocomplete** | 自动完成规则：`All Dependencies` / `Any Dependency` / `Off` |
| **Gating Override Eligible** | 是否允许跳过依赖门禁 |
| **Milestone Category** | 类别：Core Milestones / Startup / Monitoring / Inspection Readiness 等 |

模板按类型（object type）分 **Standard**（默认）、**Point in Time**（时间点）、**Event**（事件）、**Monitoring Event**（监查事件）四类；出厂预置 100+ 条里程碑模板。

## 里程碑依赖关系模板（Dependency）

**Template Milestone Dependency**（里程碑依赖关系模板）定义两个模板里程碑之间的前驱→后继关系（**Admin Setup → Template Milestone Dependencies**）：

| 字段 | 说明 |
|------|------|
| **Milestone Set** | 所属模板集（必填） |
| **Previous Template Milestone** | 前驱里程碑（必填） |
| **Next Template Milestone** | 后继里程碑（必填） |
| **Date Offset** | 日期偏移（0–3650 天） |
| **Dependency Type** | 依赖类型（object type） |

依赖类型决定日期推算方式：

| 类型 | 含义 |
|------|------|
| **Finish to Finish**（默认） | 完成到完成；后继日期 = 前驱实际完成日 + Date Offset |
| **Rollup (min date)** | 汇总最小日期（如国家 FSI 汇总到研究 FSI） |
| **Rollup (max date)** | 汇总最大日期（如国家 LSI/LSO 汇总到研究 LSI/LSO） |

> 依赖门禁在研究侧强制执行：下游里程碑 **Mark Complete** 时上游未完成会被拒绝，除非设置 Gating Override Date。

## 应用到研究

**All Actions → Plan Study** 选择主集后，研究进入 Planning 时系统按主集的三级初始化集生成里程碑；国家/中心进入 Initiating 时同样应用各自模板。研究侧里程碑初始为 **Unplanned**，通过 **Plan Milestone** 排期（见 [里程碑](milestones.html)）。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | 四个模板对象：Create、Read、Edit | 维护主集、模板集、里程碑与依赖模板 |

**Clinical Application Administrator** 管理全部里程碑模板；**Document Contributor** 只读。
