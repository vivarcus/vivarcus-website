---
title: Study Lifecycle: Create, Plan & Activate
description: Learn the full CTMS study journey from Candidate to Active: configuring recruitment planning, filling recruitment milestone dates, setting enrollment metric Planned values, Plan Subject Recruitment and Ready to Enroll.
last_updated: 2026-08-15
related:
  - overview
  - site-lifecycle
  - dashboards
---

## State Flow

A study goes from creation to activation:

| State | Meaning | Key actions |
|-------|---------|-------------|
| **Candidate** | Candidate | Configure + **Plan Study** |
| **Planning** | Planning | Milestones and EDL expand |
| **Active** | Active | Entered via **Ready to Enroll**; sites can be initiated |

## Creating a Study

Open the **Studies** list → **Create**, fill in **Study Number** and **Study Phase** (e.g. `Phase III`), and save. The study is created in the **Candidate** state.

## Configuring & Running Plan Study

1. Open the study detail page → **Study Configuration Details**:
   - **Milestone Master Set** and **Template EDL** are required.
   - **Recruitment Planning Metrics**: check `Screened`, `Enrolled` (optionally `Randomized`).
   - **Recruitment Planning Frequency**: e.g. `Monthly`.
   - **Recruitment Planning Level**: e.g. `Study`.
   - **Metric Calculation**: `Date-Based`.
2. **All Actions → Plan Study**, fill in **Study Start Date**, submit. The state becomes **Planning**; study-level milestones and the EDL are generated.

## Filling Recruitment Milestone Dates

Before **Enrollment Metrics Over Time** can be generated, fill in the finish dates of the **paired milestones** for each checked recruitment metric:

| Metric | First milestone | Last milestone |
|--------|-----------------|----------------|
| Screened | First Study Subject Screened | Last Study Subject Screened |
| Enrolled | First Study Subject In | Last Study Subject In |

For each milestone: **Plan Milestone** (if Unplanned) or **Edit**, and fill in **Planned Finish Date**.

> **Last must be ≥ First**, otherwise the metric generates no Metrics Over Time. Use the **study-level** entries, not site-level ones with similar names.

## Setting Enrollment Metric Planned Values

The study is seeded with **Enrollment Metrics** (e.g. Total Screened / Total Enrolled). Open each record → **Edit**, and set **Planned** to the target number (e.g. Screened=100, Enrolled=80). **Planned > 0** is one of the gates for Metrics Over Time.

## Plan Subject Recruitment

Study detail page → **All Actions → Plan Subject Recruitment**; the **Enrollment Metrics Over Time** section then shows monthly Screened / Enrolled records. The action is **idempotent** — running it again adds no records.

## Activating the Study

**All Actions → Ready to Enroll**, submit. The state becomes **Active**; milestones persist, with new entries like Primary / Final Database Lock typically added. Only after activation can sites run **Initiate Site** (see [Site Lifecycle](site-lifecycle.html)).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Plan Subject Recruitment produces no Metrics Over Time | Check the gates: Metric Calculation is Date-Based; recruitment planning config saved; paired milestones have finish dates with Last ≥ First; Total Screened/Enrolled Planned > 0 |
| Enrollment metrics missing | They appear after Plan Study; check the study detail section or **Study Management → Enrollment Metrics** |
| First/Last Subject milestones missing | Verify Plan Study ran and the state is Planning; use study-level entries |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Study: Create, Read, Edit | Creating studies, maintaining configuration and recruitment planning fields |
| Lifecycle action | Study: **Plan Study**, **Ready to Enroll** | Advancing state, generating milestones/EDLs/metrics |
| Object | Milestone: Read, Edit | Filling recruitment milestone finish dates |
| Object | Enrollment Metrics: Read, Edit | Setting Planned values |
| Object action | Study: **Plan Subject Recruitment** | Generating Metrics Over Time |

Recruitment planning fields require Edit access; read-only roles cannot fill Planned values or milestone dates.
