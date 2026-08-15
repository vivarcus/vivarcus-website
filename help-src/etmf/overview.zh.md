---
title: 什么是 eTMF 与 TMF 参考模型
description: 了解 Vivarcus eTMF 的核心概念：研究层级、预期文档清单（EDL）、里程碑、TMF 参考模型，以及管收审变查五环节的典型工作流。
last_updated: 2026-08-15
related:
  - study-hierarchy
  - edl
  - tmf-homepage
---

## 什么是 eTMF

eTMF（electronic Trial Master File，电子试验主文件）是临床试验全过程文档的电子档案系统。试验期间产生的每一份关键文档——试验方案、伦理批件、知情同意书、研究者手册、监查报告等——都按规则归入试验主文件，确保试验"讲得清来龙去脉"，随时满足稽查与监管要求。

Vivarcus eTMF 面向申办方与 CRO，提供文档的收集、审阅、批准、归档与稽查就绪度跟踪。核心使用环节可以概括为五个字：**管 → 收 → 审 → 变 → 查**。

## 核心概念

### 研究层级

所有文档、里程碑和质量记录都组织在 **研究（Study）→ 研究国家/地区（Study Country）→ 研究地点（Study Site）** 三级结构下。创建研究、推进生命周期后，系统自动生成里程碑清单与预期文档清单。详见 [研究层级](study-hierarchy.html)。

### 预期文档清单（EDL）

EDL（Expected Document List）是"这份 TMF 应该收齐哪些文档"的清单，条目称为预期文档（EDL Item）。系统以 EDL 为准绳判断文档完整度，也是文档自动归档的目标位置来源。详见 [EDL 与预期文档](edl.html)。

### 里程碑

里程碑描述研究的关键节点（如首例受试者入组、数据库锁定），带计划日期与实际日期，驱动 TMF 主页的完整度计算。详见 [里程碑](milestones.html)。

### 文档生命周期

文档在 Vivarcus 中经历受控的生命周期：草稿 → 审阅 → 批准 → 稳态。已批准文档自动进入 Master File 归档位置，可按 TMF 参考模型浏览。详见 [审阅与批准](review-workflow.html) 与 [TMF 查看器](tmf-viewer.html)。

## TMF 参考模型

TMF 参考模型（TMF Reference Model）是行业通用的试验主文件分类标准，把 TMF 文档划分为若干区（Zone）、节（Section）与工件（Artifact）。Vivarcus 的默认文档类型结构与自动归档路径均以该模型为基础，保证归档结构能被申办方、CRO 与稽查方共同理解。

## 一个典型的工作流

| 环节 | 含义 | 涉及功能 |
|------|------|----------|
| **管** | 建研究层级、配置 EDL 与里程碑 | 研究生命周期、Plan Study |
| **收** | 上传文档、自动匹配归档 | 上传与匹配、EDL |
| **审** | 审阅、QC、批准与质量问题闭环 | 审阅工作流、质量问题 |
| **变** | 方案升版后的级联影响跟踪 | 文档升版、预期文档匹配 |
| **查** | 按参考模型浏览、稽查就绪自检 | TMF 主页、TMF 查看器 |

## 开始之前

> 使用 Chrome 或 Edge 浏览器，建议窗口宽度不小于 1280px。首次试用请向您的管理员确认登录地址、账号与角色。研究须推进到 Active 状态后，系统才会生成里程碑与 EDL。

## 所需权限与角色

| 权限集 | 定位 | 典型能力 |
|--------|------|----------|
| **Clinical Application Administrator** | 临床应用管理员 | 全部对象 CRUD 与生命周期动作 |
| **Document Contributor** | 文档 Contributor | 研究类对象只读；文档、EDL、临床任务可编辑 |
| **External Inspector** | 外部稽查员 | 只读 |

权限分两层：**Security Profile / 权限集**决定能做什么动作；**Team Role + Grant Access**（研究团队）决定能看到哪些研究的数据。各功能的细粒度权限见对应文章的「所需权限与角色」小节。
