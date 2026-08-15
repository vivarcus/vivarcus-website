---
title: Planning & Completing Milestones
description: Learn the three milestone states, planning actions, completion order under dependency constraints, and how to view a milestone's expected documents.
last_updated: 2026-08-15
related:
  - edl
  - tmf-homepage
  - study-hierarchy
---

## Milestone States

Milestones mark key study events (e.g. first subject enrolled, database lock) and help the team track progress. After creating a study and running Plan Study, the system generates milestone records from the Milestone Master Set.

| State | Meaning | Available actions |
|-------|---------|-------------------|
| **Unplanned** | Not yet planned | Plan Milestone, Mark Complete, View Expected Documents |
| **Planned** | Scheduled | View Expected Documents |
| **Complete** | Done | Read-only |

## Planning (Plan Milestone)

1. Open the study → **Milestones** list — you'll see several **Unplanned** records.
2. Open a milestone (e.g. **Study Start**).
3. **All Actions → Plan Milestone**, fill in **Planned Finish Date**, and submit. The state becomes **Planned**.

## Completing Milestones (with Dependency Constraints)

Some milestones depend on others: upstream milestones must be completed before downstream ones.

1. Find a pair of dependent milestones; the downstream detail page shows **Dependencies** pointing to the upstream.
2. If none exist, add one manually on the downstream milestone: select the upstream milestone with type **Finish to Start**.
3. Running **Mark Complete** on the downstream milestone is rejected while the upstream is incomplete.
4. Complete the upstream first (fill **Actual Finish Date**), then the downstream.

> If Mark Complete is rejected, complete the upstream milestones in the dependency chain first.

## Viewing Related Expected Documents

Open any milestone → **All Actions → View Expected Documents** to enter the milestone workspace with the related expected document list; click an entry name to open its detail page and Matched Documents.

## Relationship to the TMF Homepage

The **Upcoming Milestones** widget lists milestones without an Actual Finish Date (i.e. Unplanned / Planned records), filterable by **Milestone Category** — the daily entry point for "what to do next".

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Milestone: Read, Edit | Viewing milestones, editing planned dates |
| Lifecycle action | Milestone: **Plan Milestone**, **Mark Complete** | Scheduling and completing |
| Object | Milestone Dependency: Create | Adding upstream/downstream dependencies |
| Object | EDL Item: Read | Viewing related entries via **View Expected Documents** |

Dependency gates are enforced server-side: even with Mark Complete permission, the action is rejected while upstream milestones are incomplete.
