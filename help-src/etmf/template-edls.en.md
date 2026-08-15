---
title: Template EDLs & Template Expected Documents
description: Learn the Template Expected Document List hierarchy, the key fields of Template Expected Documents, and how template changes propagate to existing studies.
last_updated: 2026-08-15
related:
  - edl
  - document-types
  - study-hierarchy
---

## Concept: Template → Study

A **Template EDL** (Template Expected Document List) defines "which documents are expected at a level" and can be reused across studies; its entries are **Template Expected Documents**. When a study runs **Plan Study**, the chosen Template EDL is copied into the study-level EDL and its EDL Items (runtime entries point back to the source template).

Template EDLs support **hierarchical nesting**: the **Parent** field lets country/site templates inherit from a study template (e.g. `Standard | Study Level` → `Standard | Country Level` → `Standard | Site Level`).

## Creating a Template EDL

**Admin Setup → Template Expected Document Lists** → create:

| Field | Notes |
|-------|-------|
| **Name** | Template name (required, unique) |
| **Level** | `Study` / `Country` / `Site` |
| **Milestone Type** | Optional; restricts the template to a milestone type |
| **Parent** | Optional; parent template for inheritance |

After saving, add Template Expected Document entries in the **EDL Item Templates** section of the template detail page.

## Template Expected Documents (EDL Item Templates)

**Admin Setup → Template Expected Documents** aggregates all entries; each defines one expected-document template:

| Field | Notes |
|-------|-------|
| **Name** | Entry name, e.g. `Clinical Study Report (CSR)` |
| **Template EDL** | The owning template (required) |
| **Type / Subtype / Classification** | The document taxonomy triple (from [Document Types](document-types.html), not editable) |
| **Requiredness** | Required: `Required` / `Not Required` / `Pending Decision` |
| **# Expected** | Expected steady-state count |
| **Department** | Owning department, e.g. Biostatistics, Data Management |
| **Study Team Role / Study Organization Role / Study Product Role** | Binds responsible roles for role-based expected documents |
| **Milestone Type / Owning Milestone Type** | The owning milestone type, e.g. `IR - First Study Site Initiated` |
| **Auto-assign Version Number** | Auto-assign document version numbers |

> The product ships hundreds of Template Expected Documents (CSR, Annotated CRF, Audit Certificate, etc.) — reuse them as-is or adjust to your SOP.

## How Template Changes Affect Studies

| Field | Meaning |
|-------|---------|
| **Template Behavior** | `Reuse` / `Update` (update existing study entries) / `Create` (create new entries) |
| **Fields to Update** | Scope of pushed changes, multi-select: `# Expected`, `Requiredness` |

After a template change, the system applies Template Behavior and Fields to Update to decide whether to sync studies already using the template — "change once, apply to many studies".

## Applying to a Study

While the study is in **Candidate** state, run **All Actions → Plan Study**, pick the **Template EDL** and **Milestone Master Set**, enter the study start date, and the system generates the study-level EDL (see [Study Hierarchy](study-hierarchy.html)).

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Template EDL / Template Expected Document: Create, Read, Edit | Maintaining template lists and entries |

**Clinical Application Administrator** manages all templates; **Document Contributor** is read-only.
