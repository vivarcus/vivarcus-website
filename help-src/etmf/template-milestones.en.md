---
title: Milestone Templates (Master Sets / Sets / Milestones / Dependencies)
description: Learn the four-level milestone template structure — Template Milestone Master Set, Template Milestone Set, Template Milestone, and Template Milestone Dependency — and how it drives study milestone generation.
last_updated: 2026-08-15
related:
  - milestones
  - template-edls
  - study-hierarchy
---

## The Four-Level Structure

The milestone template system has four levels, applied to a study as a master set during **Plan Study**:

| Level | Object | Purpose |
|-------|--------|---------|
| Master set | Template Milestone Master Set | Packages the study/country/site initialization sets |
| Set | Template Milestone Set | One level's milestone collection (hangs on a Story Event) |
| Milestone | Template Milestone | A single milestone template: type, sequence, duration, completion rules |
| Dependency | Template Milestone Dependency | Previous → next date derivation |

## Template Milestone Master Sets

A **Template Milestone Master Set** packages three initialization sets into one choice for the study (**Admin Setup → Template Milestone Master Sets**):

| Field | Notes |
|-------|-------|
| **Name** | Master set name (required, unique) |
| **Study Initialization Set** | Study-level initialization set (required, must be a Study-level set) |
| **Study Country Initialization Set** | Country-level initialization set (required) |
| **Study Site Initialization Set** | Site-level initialization set (required) |

> The product ships the `Standard Study Level` master set, binding the Generic Study / Country / Site Candidate initialization sets — ready to use.

## Template Milestone Sets

A **Template Milestone Set** is one level's collection of milestone templates, hanging on a **Story Event** that decides when the set is applied to a study:

| Field | Notes |
|-------|-------|
| **Name** | Set name (required) |
| **Level** | Required: `Study` / `Country` / `Site` |
| **Story Event** | Trigger event (required), e.g. `Candidate Study`, `Study Management`, `Protocol Amendment` |
| **Template Country** | Optional; restricts the set to one country |

The product ships 14 standard sets (Generic Study Candidate, Study Management, First Study Site Initiated, Study Closing, Site Initiated, etc.); events carry a creation trigger (Initialization / State Change / Ad Hoc).

## Template Milestones

A **Template Milestone** is the blueprint of a study milestone (**Admin Setup → Template Milestones**):

| Field | Notes |
|-------|-------|
| **Milestone Type** | Required, e.g. `Study Start`, `First Subject In (FSI)`, `Last Subject Last Visit (LSO)`, `Database Lock` |
| **Milestone Set** | The owning set (required) |
| **Sequence** | Order within the set |
| **Expected Duration (Days)** | Expected duration (0–2000 days) |
| **Expected Duration - Resubmit** | Expected duration for resubmissions |
| **Template EDL** | Optionally bind a Template EDL to generate expected documents |
| **Template IRB / EC Type** | `Central` / `Local` |
| **Autocomplete** | `All Dependencies` / `Any Dependency` / `Off` |
| **Gating Override Eligible** | Whether the dependency gate may be overridden |
| **Milestone Category** | Core Milestones / Startup / Monitoring / Inspection Readiness etc. |

Templates come in four object types — **Standard** (default), **Point in Time**, **Event**, **Monitoring Event** — with 100+ seeded milestone templates.

## Template Milestone Dependencies

A **Template Milestone Dependency** defines a previous → next relationship between two template milestones (**Admin Setup → Template Milestone Dependencies**):

| Field | Notes |
|-------|-------|
| **Milestone Set** | The owning set (required) |
| **Previous Template Milestone** | Previous milestone (required) |
| **Next Template Milestone** | Next milestone (required) |
| **Date Offset** | Date offset (0–3650 days) |
| **Dependency Type** | The object type |

The dependency type decides how dates derive:

| Type | Meaning |
|------|---------|
| **Finish to Finish** (default) | Next date = previous actual finish + Date Offset |
| **Rollup (min date)** | Rollup of the minimum date (e.g. country FSI into study FSI) |
| **Rollup (max date)** | Rollup of the maximum date (e.g. country LSI/LSO into study LSI/LSO) |

> The dependency gate is enforced on the study side: **Mark Complete** on a downstream milestone is rejected while the upstream is incomplete, unless a Gating Override Date is set.

## Applying to a Study

When **All Actions → Plan Study** picks a master set, the system generates milestones from the three initialization sets as the study enters Planning; countries/sites apply their own templates when entering Initiating. Study milestones start as **Unplanned** and are scheduled via **Plan Milestone** (see [Milestones](milestones.html)).

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | All four template objects: Create, Read, Edit | Maintaining master sets, sets, milestone and dependency templates |

**Clinical Application Administrator** manages all milestone templates; **Document Contributor** is read-only.
