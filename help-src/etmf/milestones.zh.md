---
title: 里程碑排期与完成
description: 了解里程碑的三种状态、排期操作、依赖约束下的完成顺序，以及查看里程碑关联预期文档的入口。
last_updated: 2026-08-15
related:
  - edl
  - tmf-homepage
  - study-hierarchy
---

## 里程碑状态

里程碑标记研究的关键节点（如首例受试者入组、数据库锁定），帮助团队跟踪进度。研究创建并 Plan Study 后，系统按 Milestone Master Set 自动生成里程碑记录。

| 状态 | 含义 | 可执行操作 |
|------|------|------------|
| **Unplanned** | 未计划 | Plan Milestone、Mark Complete、View Expected Documents |
| **Planned** | 已排期 | View Expected Documents |
| **Complete** | 已完成 | 只读查看 |

## 排期（Plan Milestone）

1. 打开研究 → **Milestones** 列表，可见多条 **Unplanned** 记录。
2. 打开一条里程碑（如 **Study Start**）。
3. **All Actions → Plan Milestone**，填写 **Planned Finish Date**，提交。状态变为 **Planned**。

## 完成里程碑（含依赖约束）

部分里程碑存在上下游依赖：须先完成上游，才能完成下游。

1. 找到一对有依赖关系的里程碑；下游详情中 **Dependencies** 指向上游。
2. 无依赖时可在下游手动添加：选择上游里程碑，类型 **Finish to Start**。
3. 对下游执行 **Mark Complete** 时，若上游未完成，操作会被拒绝。
4. 先完成上游（填 **Actual Finish Date**），再完成下游。

> Mark Complete 被拒绝时，先完成依赖链中的上游里程碑。

## 查看关联的预期文档

任选里程碑 → **All Actions → View Expected Documents**，进入里程碑工作区，显示关联的预期文档列表；点击条目名称可进入详情查看 Matched Documents。

## 与 TMF Homepage 的关系

**Upcoming Milestones** Widget 列出尚无 Actual Finish Date 的里程碑（即 Unplanned / Planned 状态的记录），可按 **Milestone Category** 过滤——是团队跟进"下一步该做什么"的日常入口。

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Milestone：Read、Edit | 查看里程碑、编辑计划日期 |
| 生命周期动作 | Milestone：**Plan Milestone**、**Mark Complete** | 排期与完成 |
| 对象 | Milestone Dependency：Create | 添加上下游依赖 |
| 对象 | EDL Item：Read | 经 **View Expected Documents** 查看关联条目 |

依赖门禁在服务端强制执行：即便有 Mark Complete 权限，上游未完成时操作仍会被拒绝。
