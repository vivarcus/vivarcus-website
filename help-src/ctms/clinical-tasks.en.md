---
title: Monitoring Follow Up Items & CTMS Clinical Tasks
description: Learn the CTMS Clinical Tasks lists, how to create and link Monitoring Follow Up Items to monitoring events, and how Seed Follow Up Items supports visit reporting.
last_updated: 2026-08-15
related:
  - monitoring-visits
  - issue-management
  - dashboards
---

## Relationship to eTMF Clinical Tasks

The CTMS **Clinical Tasks** share one object with the eTMF clinical tasks (Clinical User Task, see [Clinical Tasks](../etmf/clinical-tasks.html)); they simply live in different tabs: **Site Monitoring → Clinical Tasks** and **Study Management → Clinical Tasks**. The CTMS-specific type is the **Monitoring Follow Up Item**.

## Monitoring Follow Up Items

A follow-up item is a task hanging on a monitoring event — "what needs following up after this visit" — managed under **Site Monitoring → Monitoring Follow Up Items**. It is slimmer than a regular task:

| Field | Notes |
|-------|-------|
| **Name** | Follow-up item name (required) |
| **Study / Study Country / Study Site** | Auto-filled from the monitoring event on creation |
| **Monitoring Event** | The linked event (required, must belong to the same site) |
| **Category / Priority** | Category and priority (required) |
| **Assigned To** | Assignee (usually the CRA or site coordinator) |
| **Opened Date / Due Date** | Opened date and due date |
| **Complete** | Completion flag (required field, auto-checked on Resolve) |

Create inline from the **Monitoring Follow Up Items** section of the **Monitoring Event** detail page (recommended — study/site fill automatically), or from the tab list and then link an event of the same site manually. The state flow matches regular tasks: **Open → Investigating / Implementing / Escalated → Resolved**.

## Seed Follow Up Items & Visit Reporting

Run **All Actions → Seed Follow Up Items** on a monitoring event to snapshot two sets of follow-up items onto the event, for writing visit reports / follow-up letters:

- **Monitored Open Follow Up Items**: items still open at event time;
- **Monitored Closed Follow Up Items**: items closed since the previous monitoring event.

> Seed Follow Up Items only creates link snapshots; it does not create follow-up records — register the items first (or create them inline on the event detail).

## Link to Milestone Completeness

Study-side tasks can link a **Milestone**; required tasks count toward milestone completeness once done (see [Milestone Tracking](study-metrics.html#milestone-tracking) and [Milestones](../etmf/milestones.html)).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Can't pick a Monitoring Event when creating | The item and event must belong to the same study site; pick the right Study Site first |
| Can't see my own items in the list | Make sure **Assigned To** is set; the **My Tasks** page shows everything assigned to you |
| Sections stay empty after Seed Follow Up Items | The action only links existing items; create follow-up items on the event detail first |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Clinical User Task (incl. Monitoring Follow Up Item): Create, Read, Edit | Registering and maintaining follow-up items |
| Lifecycle actions | **Investigate**, **Implement**, **Escalate**, **Resolve** | Advancing tasks to resolution |
| Object action | Monitoring Event: **Seed Follow Up Items** | Snapshotting follow-up items onto the visit |

**CRA**, **Central Monitor**, and **CTMS Study Manager** can create follow-up items and advance states; CRAs can delete items they created; **CTMS Business/System Administrators** hold full access.
