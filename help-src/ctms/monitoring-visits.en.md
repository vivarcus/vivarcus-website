---
title: Monitoring Visits (Monitoring Events)
description: Learn how to create the four visit types (PSV/SIV/IMV/COV) and advance the full lifecycle: Expected → Planning → Confirmed → In Progress → Final.
last_updated: 2026-08-15
related:
  - site-lifecycle
  - subjects
  - issue-management
  - dashboards
---

## Visit Types

A **Monitoring Event** is the planning and execution vehicle for CRA on-site/remote monitoring, with four core visit types out of the box:

| Type | Meaning |
|------|---------|
| **PSV** (Pre-Study Visit) | Before the study |
| **SIV** (Site Initiation Visit) | Site initiation |
| **IMV** (Interim Monitoring Visit) | Interim monitoring |
| **COV** (Site Close Out Visit) | Site close-out |

## Visit States (Main Path)

| State | Meaning | Available actions |
|-------|---------|-------------------|
| **Expected** | Registered, awaiting scheduling | **Plan Visit** |
| **Planning** | Being scheduled | **Confirm Visit** |
| **Confirmed** | Confirmed | **Start Trip Report** |
| **In Progress** | Visit underway | **Start Review** etc. |
| **In Review → Passed Review → Final** | Review to finalization | **Complete Review** → **Finalize** |

## Creating a Monitoring Visit

1. Navigate to **Site Monitoring → Monitoring Events** → create, and choose a visit type (e.g. **Interim Monitoring Visit**).
2. Fill in:

| Field | Notes |
|-------|-------|
| **Name** | Visit name (e.g. `CTMS-IMV-20260802`) |
| **Study / Study Country / Study Site** | All three are required |
| **Study Person** | Select an onboarded CRA |
| **Planned Start / Planned End** | Planned dates |

The record is saved in the **Expected** state.

## Advancing the Full Lifecycle

| Step | Action | State change |
|------|--------|--------------|
| 1 | **Plan Visit**, confirm planned dates | Expected → **Planning** |
| 2 | **Confirm Visit** | → **Confirmed** |
| 3 | **Start Trip Report**, fill Actual Start/End Date | → **In Progress** |
| 4 | **Start Review** | → **In Review** |
| 5 | **Complete Review** | → **Passed Review** |
| 6 | **Finalize** | → **Final** |

> When entering Planning / Confirmed / In Progress, the system may auto-seed Follow-Up / Issues / Monitored Enrollment data; empty lists don't affect the main path.

## Viewing on Dashboards

- **CRA Homepage → Monitoring Plan**: lists scope-filtered visit plans with drill-down into Monitoring Event details.
- **Study Management Homepage → Monitoring Status**: counts distributed by visit type.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Creating a Monitoring Event fails validation | Study, Study Country, and Site are all required |
| Homepage Monitoring Status is empty | Verify the right Study is selected and the visit's Study/Country/Site bindings are correct |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Monitoring Event: Create, Read, Edit | Creating and maintaining visits |
| Lifecycle action | Monitoring Event: **Plan Visit**, **Confirm Visit**, **Start Trip Report**, **Start Review**, **Complete Review**, **Finalize** | The full visit lifecycle |
| Object | Study Person: Read | Assigning a CRA (study team must be onboarded) |

Monitoring visits require Study / Country / Site bindings; CRAs typically only see visits assigned to them or within their scope.
