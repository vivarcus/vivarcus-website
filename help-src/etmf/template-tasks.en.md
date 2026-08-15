---
title: Template Tasks
description: Learn how a Template Task predefines work for a template milestone and becomes a Clinical User Task once the study is generated.
last_updated: 2026-08-15
related:
  - clinical-tasks
  - template-milestones
  - milestones
---

## What Is a Template Task

A **Template Task** predefines work due when a template milestone takes effect; once the study is generated from the template, it becomes a study-side **Clinical User Task** (see [Clinical Tasks](clinical-tasks.html)).

For example, the `Study Start` milestone carries `Confirm TMF Filing Plan` (required, 14-day turnaround); `Final Database Lock` carries `Prepare Database Lock Checklist` (7 days).

## Key Fields

Maintain under **Admin Setup → Template Tasks**:

| Field | Notes |
|-------|-------|
| **Name** | Task name (required, unique) |
| **Milestone Set** | The owning set (required) |
| **Milestone** | The linked template milestone (required) |
| **Required** | Whether required (default no); required tasks count toward milestone completeness |
| **Expected Turnaround Time (Days)** | Expected completion time (0–200 days) |
| **Category** | Task category (required), e.g. `Essential Documents/ISF`, `Data Collection/Data Entry/Query Resolution` |
| **Priority** | Required: `Low` / `Medium` / `High` |

## Relationship to Runtime Tasks

A template task hangs on both a set and a milestone; when the study runs **Plan Study** and milestones are generated from the template, the system copies template tasks into study-side clinical tasks, inheriting category, priority, requiredness, and expected turnaround. Completed runtime tasks count toward the owning milestone's completeness (see [Milestones](milestones.html)).

> Template tasks define only "what to do"; assignment (Assigned To), dates, and resolution live on the study-side task. Changing a template does not change tasks already generated.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Template Task: Create, Read, Edit | Predefining task lists for milestones |

**Clinical Application Administrator** manages template tasks; **Document Contributor** is read-only.
