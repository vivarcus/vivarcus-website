---
title: 什么是 CTMS 与研究运营闭环
description: CTMS 管过程：研究、站点、受试者、监查与问题。了解启站队人监偏盘七环节，以及与 eTMF 的分工。
last_updated: 2026-08-15
related:
  - study-lifecycle
  - dashboards
  - issue-management
---

## 什么是 CTMS

CTMS（Clinical Trial Management System，临床试验管理系统）是临床运营的过程管理系统：研究从启动到关闭的全部运营数据——中心、团队、受试者、监查访视、问题——都在这里登记、流转与汇总。

**eTMF 管文件，CTMS 管过程**。两者在同一 Clinical Operations Vault、同一套研究层级下协同：文档归档靠 eTMF，过程追踪靠 CTMS。

## 七环节闭环

CTMS 的核心使用环节可以概括为七个字：

| 环节 | 含义 | 相关功能 |
|------|------|----------|
| **启** | 研究激活、招募计划 | 研究生命周期、注册指标、Metrics Over Time |
| **站** | 国家/中心生命周期与异常路径 | Qualify / Select / 启动机构 |
| **队** | 研究团队与沟通 | Study Person、Team Role、Grant Access |
| **人** | 受试者筛选、入组与退出 | Subjects、Subject Visits |
| **监** | 监查访视全生命周期 | Monitoring Events（PSV/SIV/IMV/COV） |
| **偏** | 方案偏离/观察项闭环 | Issues、Observations、Protocol Deviations |
| **盘** | 运营仪表盘 | 研究管理主页、CRA 主页 |

## 与 eTMF 共享的研究层级

过程数据同样挂在 **研究（Study）→ 研究国家/地区（Study Country）→ 研究地点（Study Site）** 三级结构下。不同的是：

- 研究须推进到 **计划** 才会展开里程碑；推进到 **活动** 后，中心才能完成启动（**启动机构**）。
- 中心进入 Initiating 要求父 Country 先执行 **选择国家/地区**——CTMS 的中心启动必须走生命周期，不能只建记录。

## 典型旅程

```
启 → 建研究 + 计划研究 + 招募指标 Planned + 注册准备就绪（活动）
站 → 国家选择国家/地区；中心资格认定 → 选择 → 启动（活动）
队 → Study Person 入队（Study Manager / Contributor / CRA）
人 → 受试者 Consented → In Screening → Enrolled
监 → Monitoring Event：Expected → Planning → Confirmed → In Progress → Final
偏 → Protocol Deviation / Observation 闭环
盘 → 两张 Homepage 按研究/国家/中心范围裁剪
```

## 所需权限与角色

| 权限集/角色 | 定位 |
|-------------|------|
| **Study Manager** | 研究经理：研究生命周期、招募计划、团队 |
| **Clinical Research Associates** | CRA：监查访视、中心日常 |
| **Central Monitor** | 中心监查：CRA 能力 + 集中监查视角 |
| **Clinical Business Administrator** | 业务管理员：研究配置与目录维护 |

权限分两层：**Security Profile / 权限集**决定能做什么动作；**Team Role + Grant Access**（研究团队）决定能看到哪些研究的数据。
