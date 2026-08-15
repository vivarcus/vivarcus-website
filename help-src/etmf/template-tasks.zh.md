---
title: 模板任务（Template Tasks）
description: 了解 Template Task 如何为模板里程碑预定义任务，以及研究生成后如何变为临床用户任务（Clinical User Task）。
last_updated: 2026-08-15
related:
  - clinical-tasks
  - template-milestones
  - milestones
---

## 模板任务是什么

**Template Task**（模板任务）为模板里程碑预定义「该里程碑生效时需要完成的任务」，研究按模板生成后，任务变为研究侧的 **Clinical User Task**（见 [临床任务](clinical-tasks.html)）。

例如 `Study Start` 里程碑挂 `Confirm TMF Filing Plan`（确认 TMF 归档计划，必做，14 天内完成）；`Final Database Lock` 挂 `Prepare Database Lock Checklist`（准备锁库清单，7 天内完成）。

## 关键字段

**Admin Setup → Template Tasks** 维护：

| 字段 | 说明 |
|------|------|
| **Name** | 任务名（必填且唯一） |
| **Milestone Set** | 所属模板集（必填） |
| **Milestone** | 关联的模板里程碑（必填） |
| **Required** | 是否必做（默认否）；必做任务计入里程碑完成度 |
| **Expected Turnaround Time (Days)** | 预期完成时长（0–200 天） |
| **Category** | 任务类别（必填），如 `Essential Documents/ISF`、`Data Collection/Data Entry/Query Resolution` |
| **Priority** | 优先级（必填）：`Low` / `Medium` / `High` |

## 与运行时任务的关系

模板任务挂在「模板集 + 模板里程碑」两个维度上；研究执行 **Plan Study** 并按模板生成里程碑时，系统把模板任务复制为研究侧临床任务，继承类别、优先级、必做性与预期时长。运行时任务完成后计入所属里程碑的完成度（见 [里程碑](milestones.html)）。

> 模板任务只定义「该做什么」；实际指派（Assigned To）、日期与解决在研究侧的任务上维护，修改模板不会改已生成的任务。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Template Task：Create、Read、Edit | 为里程碑预定义任务清单 |

**Clinical Application Administrator** 管理模板任务；**Document Contributor** 只读。
