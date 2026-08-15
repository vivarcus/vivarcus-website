---
title: Issues & Protocol Deviations
description: Learn the four Issue types (Protocol Deviation / Observation / Protocol Violation / Risk Mitigation Action), creation and advancement paths, team prerequisites for Start PD Review, and comparison with eTMF quality issues.
last_updated: 2026-08-15
related:
  - subjects
  - monitoring-visits
  - overview
---

## Issue Types & Common Actions

**Issues** capture process problems such as protocol deviations and observations, can link to study / site / subject, and coexist with eTMF quality issues on the same platform.

| Type | Initial state | Common actions |
|------|---------------|----------------|
| **Protocol Deviation** | **Open** | **Start PD Review** |
| **Observation** | **Open** | **Resolve Issue** or **Promote to Protocol Deviation** |
| **Protocol Violation** | **Open** | Advance via available page actions |
| **Risk Mitigation Action** | **Open** | **Assign Risk Mitigation** |

Typical path: **Register deviation (Open) → review or resolve → Resolved**.

## Creating a Protocol Deviation

1. Navigate to **Issue Management → Protocol Deviations** (or **All Issues**) → **Create**, type **Protocol Deviation**.
2. Fill in:

| Field | Notes |
|-------|-------|
| **Issue Log ID** | Deviation identifier (or accept the auto-number) |
| **Study** | Required |
| **Study Country / Study Site** | Recommended, for dashboard scoping |
| **Subject** | Link the subject |
| **Date Identified** | Discovery date (required) |
| **Date of Issue** | When it actually happened |
| **Summary** | Required, e.g. `Visit window deviation: Cycle 1 Day 25 (window Day 21±3)` |
| **Category** | e.g. `F. Visit Schedule` |
| **Severity** | e.g. `Minor` |
| **Description** | Detailed description |

## Advancing a Deviation (Formal Path)

1. Fill in **Resolution** (and optionally Root Cause) on the deviation detail page, save.
2. **All Actions → Start PD Review**:
   - **Reviewer: PM**: select a CTMS Study Manager member from the study team.
   - **Reviewer: Medical**: select a Contributor member.
   - Fill in the deadline and submit to enter the PD review workflow.
3. Complete review tasks in **My Tasks**; the state trends to **Resolved** afterwards.

> **Can't find people?** Candidates come from the study_manager / contributor roles in the deviation's Sharing (written by the study team matching rule). Verify the study team is onboarded with **Grant Access to Related Records** checked; if the deviation predates onboarding, open the deviation → **Sharing Settings** to add those roles manually, or edit and save the deviation once to trigger matching re-evaluation.

## Quick Closure: Observation

A shorter path when time is limited: **Issue Management → Observations** → Create, fill in Study / Site / Summary and save (state Open), fill in **Resolution**, then **All Actions → Resolve Issue** — the state becomes **Resolved** (Resolved Date auto-written).

> Protocol Deviation and Observation have different available actions: Observations use **Resolve Issue**; PDs prefer **Start PD Review**. Resolved usually requires a non-empty Resolution.

## Risk Mitigation Actions (RMA)

A **Risk Mitigation Action (RMA)** registers the mitigating action for a study risk — "after identifying a risk, decide what to do and who completes it". It shares the Issue object and lifecycle with deviations/observations but follows a dedicated assignment flow. **Issue Management → Risk Mitigation Actions** → Create:

| Field | Notes |
|-------|-------|
| **Study** | The owning study (required, defaults from the study risk assessment) |
| **Study Country / Study Site** | Optional, for scoping |
| **Study Risk Assessment / Study Risk / Study Risk Mitigation** | The linked risk chain: assessment → risk → mitigation |
| **Date Identified** | Identification date (required) |
| **Summary** | Required, e.g. `Add repeat screening labs` |
| **Description** | What the mitigation action does |
| **Resolution** | Required before entering Resolved |

## Assign Risk Mitigation

**All Actions → Assign Risk Mitigation** starts the **Complete Risk Mitigation** workflow:

| Step | What happens | State |
|------|--------------|-------|
| 1 | Pick a **Mitigation Owner** and submit | → **Assigned** |
| 2 | The owner receives the **Complete Mitigation Action** task: perform the action per Description and fill in **Resolution** | Task completed |
| 3 | The system closes the record out | → **Resolved** (**Resolved Date** auto-written) |

> Like other types, an RMA can also use the generic actions (**Investigate / Implement / Escalate / Resolve Issue**); **Change Issue Type** converts between Issue types (e.g. promoting an Observation to a Risk Mitigation Action).

## Comparison with eTMF Quality Issues

In the same Vault, process-side Issues and document-side Quality Issues coexist: Issues record "what went wrong in the process" (deviations, observations), Quality Issues record "what defect exists in a document" (missing pages, incomplete signatures). During audits they can reference each other, forming a complete "process deviation ↔ document quality" traceability chain.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Issue (Protocol Deviation / Observation): Create, Read, Edit | Registering and maintaining issues |
| Object action | Issue: **Start PD Review**, **Resolve Issue**, **Assign Risk Mitigation**, **Change Issue Type** | Review, closure, and mitigation assignment |
| Team role | Study Person: **CTMS Study Manager** + **Contributor** onboarded with Grant Access | Source of reviewer candidates for Start PD Review |
| Object | Clinical User Task: Read, Edit | Completing review tasks in My Tasks |

If a deviation predates team onboarding and no people can be selected: open the deviation → **Sharing Settings** to add roles manually, or edit and save once to trigger matching re-evaluation.
