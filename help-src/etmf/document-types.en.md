---
title: Document Types
description: Learn the Type → Subtype → Classification document taxonomy, numbering rules, seeded categories, and mapping to TMF reference model artifacts.
last_updated: 2026-08-15
related:
  - template-edls
  - models-artifacts
  - upload-documents
---

## The Three-Level Taxonomy

**Document Type** is the master data for the TMF document taxonomy, in a **Type → Subtype → Classification** hierarchy:

| Level | Meaning | Example |
|-------|---------|---------|
| **Type** | Top-level category | Regulatory, Safety Reporting |
| **Subtype** | Division under a type | Regulatory → Reports |
| **Classification** | Finest category | General → Relevant Communications |

Each entry marks its level with the **Level** field and hangs under its parent via the **Parent Type** self-reference, forming the taxonomy tree. The taxonomy feeds the type/subtype/classification triple referenced by EDL templates, and it is the matching basis for automatic document filing.

## Seeded Document Types

The product ships 11 top-level Types (plus a platform-level `General`), each with a document number prefix:

| Type | Number format |
|------|---------------|
| Regulatory | `REG-{####}` |
| Safety Reporting | `SAF-{####}` |
| Trial Management | `TM-{####}` |
| Site Management | `SITE-{####}` |
| Data Management | `DM-{####}` |
| IP and Trial Supplies | `IP-{####}` |
| IRB or IEC and other Approvals | `IRB-{####}` |
| Central Trial Documents | `CTD-{####}` |
| Central and Local Testing | `CLT-{####}` |
| Statistics | `STAT-{####}` |
| Third Parties | `TP-{####}` |

Subtypes and Classifications are seeded as well (e.g. Regulatory → Reports, Data Management → Database/Data Capture).

## Document Numbering

A Type carries a **Document Number Format** and **Start Number**; documents of that type are numbered sequentially from it. When creating a new Type, configure both so documents never lack a numbering rule.

## Mapping to Reference Model Artifacts

Each taxonomy entry can map to TMF reference model artifacts:

| Field | Meaning |
|-------|---------|
| **eTMF RM v2.0 / eTMF RM v3.0** | Maps to an artifact of TMF RM v2.0 / v3.0 |
| **Vault Clinical Docs** | Maps to a Vault Clinical Docs artifact |

Once mapped, documents can be browsed by reference model hierarchy in the **TMF Viewer**, and the `Binder Section to Document Type` model files documents by matching Type/Subtype/Classification to binder section names (see [Models & Artifacts](models-artifacts.html)).

## Use in EDL Templates

**Template Expected Documents** entries reference this taxonomy through the Type / Subtype / Classification fields, and study-side EDL Items inherit the same classification (see [Template EDLs & Template Expected Documents](template-edls.html)). Changing the taxonomy affects every template and existing study that references it — assess the impact before changing.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Document Type: Create, Read, Edit | Maintaining the taxonomy tree and numbering rules |

**Clinical Application Administrator** maintains the taxonomy; **Document Contributor** is read-only.
