---
title: Clinical Tasks
description: Learn the Clinical User Task object types, how to create tasks, and the Open → Investigating / Implementing / Escalated → Resolved state flow with automatic metrics.
last_updated: 2026-08-15
related:
  - template-tasks
  - milestones
  - review-workflow
---

## What Is a Clinical Task

A **Clinical User Task** is a to-do/issue item on the study hierarchy: assigned to someone, with a category, priority, and due date, tracked until resolved. Tasks appear in several places — on the eTMF side mainly **Planning → Clinical Tasks**; CTMS monitoring follow-up items are built on the same object (see [Monitoring Follow Up Items & CTMS Clinical Tasks](../ctms/clinical-tasks.html)).

## Task Types (Object Types)

The type determines which level the task hangs on and whether it links to a monitoring event:

| Type | Level | Notes |
|------|-------|-------|
| **Study Task** (default) | Study | Study-level task; can link milestones and template tasks |
| **Study Country Task** | Study Country | Country-level task |
| **Study Site Task** | Study Site | Site-level task |
| **Monitoring Follow Up Item** | Study Site | CTMS monitoring follow-up; must link a monitoring event of the same site |

The **Study Tasks / Study Country Tasks / Study Site Tasks** sections on study/country/site detail pages filter tasks by type.

## Creating a Task

1. Go to **Planning → Clinical Tasks** → create, and pick a type (default **Study Task**).
2. Fill in:

| Field | Notes |
|-------|-------|
| **Name** | Task name (required) |
| **Study / Study Country / Study Site** | Cascading selection by type |
| **Category** | Required; one of 12 values such as `Essential Documents/ISF`, `Informed Consent`, `Data Collection/Data Entry/Query Resolution` |
| **Priority** | Required: `Low` / `Medium` / `High` |
| **Assigned To** | Assignee |
| **Opened Date** | Required; must not be after today |
| **Due Date** | Must not be before Opened Date |
| **Required** | Whether the task is required |
| **Milestone** | Optional link so the task counts toward milestone completeness |

3. After saving, the task is in **Open** state and the assignee is notified; the **My Tasks** page centralizes everything assigned to you.

## States & Actions

| State | Available actions |
|-------|-------------------|
| **Open** | **Investigate**, **Implement**, **Escalate**, **Resolve** |
| **Investigating** | **Implement**, **Escalate**, **Resolve** |
| **Implementing** | **Escalate**, **Resolve** |
| **Escalated** | **Investigating**, **Implementing**, **Resolve** |
| **Resolved** | None (terminal, record becomes read-only) |

> Entering Escalated accumulates escalation counts and dates; **Resolve** automatically checks **Complete** and stamps **Completion Date**, and computes **Days Open / Days Investigating / Days Implementing**.

## Validation Rules

- **Opened Date** must not be after today;
- **Due Date** must not be before **Opened Date**.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| No Milestone field when creating | Use the default Study Task type; the Monitoring Follow Up Item type has a slimmer field set |
| Want to edit after Resolved | Resolved is a terminal read-only state; create a new task instead |
| Assignee gets no notification | Make sure **Assigned To** is set; assignment and reassignment notifications go to the assignee |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Clinical User Task: Create, Read, Edit | Creating and maintaining tasks |
| Lifecycle actions | **Investigate**, **Implement**, **Escalate**, **Resolve** | Advancing tasks to resolution |
| Object | Milestone: Read | Linking milestones and affecting their completeness |

**Clinical Application Administrator** and **Document Contributor** can both edit tasks and run all lifecycle actions; task visibility is trimmed by study sharing, and assignees typically see tasks assigned to them.
