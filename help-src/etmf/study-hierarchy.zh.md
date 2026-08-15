---
title: 研究层级：创建研究、国家与中心
description: 学习创建 Study、配置里程碑主集与模板 EDL、执行 Plan Study 与 Ready to Enroll，以及创建研究国家/地区与研究地点的完整流程。
last_updated: 2026-08-15
related:
  - edl
  - milestones
  - tmf-homepage
---

## 三级结构

临床研究的所有文档、里程碑和质量记录，都组织在 **研究（Study）→ 研究国家/地区（Study Country）→ 研究地点（Study Site）** 三级结构下：

| 层级 | 对象 | 作用 |
|------|------|------|
| Study | 研究 | 试验主干的载体；生命周期驱动里程碑与 EDL 生成 |
| Study Country | 研究国家/地区 | 按国家裁剪文档与里程碑范围 |
| Study Site | 研究地点 | 研究中心级文档的归档落点 |

> 研究须推进到 **Active** 状态，系统才会生成里程碑清单和预期文档清单（EDL）。

## 创建研究

1. 登录系统，选择 Vault，进入 **Study Info → Studies**，点击 **Create**。
2. 填写 **Study Number**（中文界面：**研究编号**）与 **Study Phase**（如 `Phase III`），保存。

创建成功后研究处于 **Candidate** 状态。

## 配置并启动研究

研究从 Candidate 到 Active 需要两步：

| 动作 | 操作 | 结果 |
|------|------|------|
| 配置 | 在研究详情的 **Study Configuration Details** 中，选择 **Milestone Master Set**（里程碑主集）与 **Template EDL**（预期文档列表模板） | 配置保存 |
| **Plan Study** | **All Actions → Plan Study**，填写 **Study Start Date**，提交 | 状态变为 **Planning**，自动生成里程碑与预期文档 |
| **Ready to Enroll** | **All Actions → Ready to Enroll**，提交 | 状态变为 **Active** |

完成后可在研究详情中看到 **Milestones** 列表与 **Expected Documents** 列表。

> 若 Plan Study 不可用，请确认已填写 Milestone Master Set 和 Template EDL。

## 创建研究国家/地区

进入 **Study Info → Study Countries**，创建：

| 字段 | 说明 |
|------|------|
| **Study Number** | 选择所属研究 |
| **Country** | 选择国家/地区（如 United States） |
| **Study Country Name** | 选择 Country 后自动生成，无需手动填写 |

## 创建研究地点

进入 **Study Info → Study Sites**，创建：

| 字段 | 说明 |
|------|------|
| **Study Site Number** | 中心编号（如 `Site-001`）；Name 与此为同一字段 |
| **Study Country** | 选择所属研究国家/地区 |
| **Study Number** | 留空，系统自动从 Study Country 推导 |

保存后打开中心详情，确认 **Study Number** 已自动指向所属研究。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| 创建 Study 时找不到 Name 字段 | 中文界面中该字段标签为 **Study Number**（研究编号） |
| Study Country 的 Name 无法编辑 | Name 在选择 Country 后自动生成 |
| 找不到 Site Number 字段 | Name 和 Site Number 是同一个字段：**Study Site Number** |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study / Study Country / Study Site：Create、Read、Edit | 创建研究、国家与中心并维护字段 |
| 生命周期动作 | Study：**Plan Study**、**Ready to Enroll** | 推进研究状态，生成里程碑与 EDL |
| 生命周期动作 | Study Country：**Select Country** | 选定国家（CTMS 中心启动的前置） |

**Clinical Application Administrator** 具备上述全部权限；**Document Contributor** 对研究层级为只读，可查看但不能创建或推进生命周期。
