---
title: What Is CTMS & the Study Operations Loop
description: CTMS manages processes: studies, sites, subjects, monitoring and issues. Learn the seven-stage loop (start–sites–team–subjects–monitor–deviations–dashboards) and the division of labor with eTMF.
last_updated: 2026-08-15
related:
  - study-lifecycle
  - dashboards
  - issue-management
---

## What Is CTMS

The CTMS (Clinical Trial Management System) is the process management system for clinical operations: all operational data of a trial from startup to close-out — sites, teams, subjects, monitoring visits, issues — is registered, moved through workflows, and summarized here.

**eTMF manages documents; CTMS manages processes.** Both work together in the same Clinical Operations Vault on the same study hierarchy: document filing via eTMF, process tracking via CTMS.

## The Seven-Stage Loop

Core CTMS usage can be summarized in seven stages:

| Stage | Meaning | Features involved |
|-------|---------|-------------------|
| **Start** | Study activation, recruitment planning | Study lifecycle, enrollment metrics, Metrics Over Time |
| **Sites** | Country/site lifecycle and exception paths | Qualify / Select / Initiate Site |
| **Team** | Study team and communication | Study Person, Team Role, Grant Access |
| **Subjects** | Screening, enrollment, withdrawal | Subjects, Subject Visits |
| **Monitor** | Monitoring visit lifecycle | Monitoring Events (PSV/SIV/IMV/COV) |
| **Deviate** | Protocol deviation / observation closure | Issues, Observations, Protocol Deviations |
| **Dashboards** | Operational dashboards | Study Management Homepage, CRA Homepage |

## The Shared Study Hierarchy

Process data lives under the same three-level structure: **Study → Study Country → Study Site**. Differences from eTMF:

- Milestones expand only when the study reaches **Planning**; sites can only be initiated (**Initiate Site**) after the study is **Active**.
- A site can only enter Initiating after its parent Country has run **Select Country** — CTMS site activation must follow the lifecycle, not just record creation.

## A Typical Journey

```
Start → Create study + Plan Study + enrollment metric Planned + Ready to Enroll (Active)
Sites → Country Select Country; Site Qualify → Select → Initiate (Active)
Team → Study Persons onboarded (Study Manager / Contributor / CRA)
Subjects → Consented → In Screening → Enrolled
Monitor → Monitoring Event: Expected → Planning → Confirmed → In Progress → Final
Deviate → Protocol Deviation / Observation closure
Dashboards → Both homepages scoped by study/country/site
```

## Required Permissions & Roles

| Permission set / role | Positioning |
|-----------------------|-------------|
| **Study Manager** | Study manager: study lifecycle, recruitment planning, team |
| **Clinical Research Associates** | CRA: monitoring visits, site day-to-day |
| **Central Monitor** | Central monitoring: CRA capabilities plus the central monitoring view |
| **Clinical Business Administrator** | Business admin: study configuration and directory maintenance |

Permissions have two layers: the **Security Profile / permission set** determines which actions you can perform; **Team Role + Grant Access** (study team) determines which studies' data you can see.
