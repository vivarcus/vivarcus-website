---
title: Subject Registration & Status Tracking
description: Learn the subject status flow (Consented → In Screening → Enrolled), registration fields, and how to record exception paths such as screen failures.
last_updated: 2026-08-15
related:
  - site-lifecycle
  - monitoring-visits
  - issue-management
---

## Common Subject States

| State | Meaning |
|-------|---------|
| **Consented** | Informed consent obtained |
| **In Screening** | In screening |
| **Screen Failure** | Screening failed |
| **Enrolled** | Enrolled |
| **Withdrawn** | Withdrawn |

## Registering & Enrolling

1. Open the **Subjects** list → **Create**.
2. Fill in:

| Field | Notes |
|-------|-------|
| **Subject ID** | Subject identifier (e.g. `CTMS-OV-20260802-001`) |
| **Study** | The owning study |
| **Study Country** | Study country |
| **Study Site** | Study site — must be an **Active** site |
| **Subject Status** | First `Consented`, then `In Screening`, finally `Enrolled` (can save in steps) |
| **Initial Consent Date** | Consent date |
| **Screened Date** | Screening date |
| **Enrolled Date** | Enrollment date |

## Screen Failure (Exception Path)

Create another subject record with **Subject Status** = `Screen Failure`, fill in **Screen Failed Date**, and save. Exception paths are recorded alongside successful enrollments and can be referenced by issue/deviation records.

## Subject Visits

A Subject Visit records the plan and execution of one visit for one subject, managed under **Study Info → Subject Visits**:

| Field | Notes |
|-------|-------|
| **Subject** | The owning subject (required) |
| **Visit / Visit Name / Visit Sequence** | Visit definition, name, and sequence (e.g. `Cycle 1 Day 1`) |
| **Visit Status** | Visit state, e.g. `Planned` |
| **Planned Date** | Planned visit date |
| **Visit Date** | Actual visit date; **Overdue Date** marks late visits for tracking |

To create a visit record, pick the **Subject** first, then fill in the visit definition and planned date according to the study plan; once executed, update **Visit Date** and status to build a full visit trail on the subject detail.

## Relationship to Deviations & Visits

Subject records are the anchor for enrollment progress and deviation traceability:

- A **Protocol Deviation / Issue** can link a **Subject** field to show which subject the problem concerns (see [Issues & Protocol Deviations](issue-management.html)).
- Enrollment data recorded in monitoring visits shares the same source as subject records, useful for scope-based verification (see [Monitoring Visits](monitoring-visits.html)).

> Some dashboard/metric aggregations depend on backend seeding and frontend aggregation; a trial environment may show 0 or empty charts — a known difference. What matters is that subject records themselves can be created, queried, and referenced by deviations.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Subject: Create, Read, Edit | Registering subjects and advancing status |
| Field | Subject status fields (Subject Status etc.): Edit | Consented → In Screening → Enrolled progression |

Subjects must hang under an Active site; users without Read access to a site will not see its subjects in lists.
