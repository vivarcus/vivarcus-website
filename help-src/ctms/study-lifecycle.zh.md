---
title: 研究生命周期：创建、计划与激活
description: 学习 CTMS 研究从 Candidate 到 Active 的完整流程：配置招募计划、补齐招募里程碑日期、填写注册指标 Planned、Plan Subject Recruitment 与 Ready to Enroll。
last_updated: 2026-08-15
related:
  - overview
  - site-lifecycle
  - dashboards
---

## 状态流转

研究从创建到激活：

| 状态 | 含义 | 关键动作 |
|------|------|----------|
| **Candidate** | 候选 | 配置 + **Plan Study** |
| **Planning** | 计划 | 展开里程碑与 EDL |
| **Active** | 进行中 | **Ready to Enroll** 后进入；中心可 Initiate Site |

## 创建研究

进入 **Studies** 列表 → **Create**，填写 **Study Number**（研究编号）与 **Study Phase**（如 `Phase III`），保存。研究创建成功，状态为 **Candidate**。

## 配置与 Plan Study

1. 打开研究详情 → **Study Configuration Details**：
   - **Milestone Master Set**（里程碑主集）与 **Template EDL**（模板 EDL）必填。
   - **Recruitment Planning Metrics**（招募计划指标）：勾选 `Screened`、`Enrolled`（可选 `Randomized`）。
   - **Recruitment Planning Frequency**（招募计划频率）：如 `Monthly`。
   - **Recruitment Planning Level**（招募计划级别）：如 `Study`。
   - **Metric Calculation**（指标计算）：`Date-Based`（基于日期）。
2. **All Actions → Plan Study**，填写 **Study Start Date**，提交。状态变为 **Planning**，自动生成研究级里程碑与 EDL。

## 补齐招募里程碑日期

生成 **Enrollment Metrics Over Time**（随时间推移的注册指标）前，须为勾选的招募指标补齐**成对里程碑**的结束日：

| 招募指标 | First 里程碑 | Last 里程碑 |
|----------|--------------|-------------|
| Screened | First Study Subject Screened | Last Study Subject Screened |
| Enrolled | First Study Subject In | Last Study Subject In |

对每条里程碑：**Plan Milestone**（若 Unplanned）或 **Edit**，填写 **Planned Finish Date**。

> **Last 须 ≥ First**，否则该指标不会生成 Metrics Over Time。注意选用**研究级**条目，勿误选中心级同名条目。

## 填写注册指标 Planned

研究下已播种 **Enrollment Metrics**（注册指标，如 Total Screened / Total Enrolled）。打开记录 **Edit**，将 **Planned** 设为计划人数（如 Screened=100、Enrolled=80）。**Planned > 0** 是生成 Metrics Over Time 的门禁之一。

## Plan Subject Recruitment

研究详情 → **All Actions → Plan Subject Recruitment**，展开 **Enrollment Metrics Over Time** 出现 Screened / Enrolled 的分月记录。该操作**幂等**，重复执行不会增加记录。

## 激活研究

**All Actions → Ready to Enroll**，提交。状态变为 **Active**；里程碑保留，通常新增 Primary / Final Database Lock 等条目。激活后中心才能执行 **Initiate Site**（见 [中心生命周期](site-lifecycle.html)）。

## 常见问题

| 现象 | 处理建议 |
|------|----------|
| Plan Subject Recruitment 无 Metrics Over Time | 按门禁核对：Metric Calculation 为 Date-Based；招募计划配置已保存；First/Last 成对里程碑有结束日且 Last ≥ First；Total Screened/Enrolled 的 Planned > 0 |
| 找不到注册指标 | Plan Study 后出现；研究详情注册指标区块，或 **Study Management → Enrollment Metrics** |
| 找不到 First/Last Subject 里程碑 | 确认已 Plan Study 且状态为 Planning；选用 Study 级条目 |

## 所需权限与角色

| 类型 | 权限 | 作用 |
|------|------|------|
| 对象 | Study：Create、Read、Edit | 创建研究、维护配置与招募计划字段 |
| 生命周期动作 | Study：**Plan Study**、**Ready to Enroll** | 推进状态、生成里程碑/EDL/指标 |
| 对象 | Milestone：Read、Edit | 补齐招募里程碑结束日 |
| 对象 | Enrollment Metrics：Read、Edit | 填写 Planned |
| 对象动作 | Study：**Plan Subject Recruitment** | 生成 Metrics Over Time |

招募计划相关字段需具备 Edit 权限；只读角色无法填写 Planned 与里程碑日期。
