---
title: Models & Artifacts
description: Learn the TMF reference Model and Artifact hierarchy, the seeded models and artifact tree, and how document-type-to-artifact mapping drives auto-filing and the TMF Viewer.
last_updated: 2026-08-15
related:
  - tmf-viewer
  - document-types
  - overview
---

## Models

A **Model** is the container of a TMF reference model — for example the DIA TMF Reference Model v2.0 / v3.0. Maintain under **Admin Setup → Models**:

| Field | Notes |
|-------|-------|
| **Name** | Model name (required, unique) |
| **Description** | Model description |
| **Display in TMF Viewer** | Whether to show in the TMF Viewer (default yes) |

Five models are seeded:

| Model | Purpose |
|-------|---------|
| **TMF RM v2.0** (2012) | DIA TMF Reference Model v2.0 |
| **TMF RM v3.0** (2015) | DIA TMF Reference Model v3.0 |
| **Document Type Hierarchy** | Browse by document type hierarchy |
| **Vault Clinical Docs** | Vault clinical documents model |
| **Binder Section to Document Type** | Auto-filing model: files documents by matching their Type/Subtype/Classification to binder section names |

## Artifacts

An **Artifact** is a node (Zone / Section) inside a reference model, forming the standard TMF hierarchy such as `01 Trial Management → 01.01 Trial Oversight → 01.01.01 Trial Master File Plan`. Maintain under **Admin Setup → Artifacts**:

| Field | Notes |
|-------|-------|
| **Model** | The owning model (required) |
| **Name** | Artifact name |
| **Number** | Hierarchy number, e.g. `01.01.01` |
| **Parent Artifact** | Parent artifact; self-reference builds the tree |
| **Description** | Artifact definition text (from the TMF Reference Model) |

> The complete TMF RM v2.0 artifact tree is seeded with official definitions — a standard hierarchy for internal SOPs and inspection readiness.

## Relationship to Document Filing

The **eTMF RM v2.0 / eTMF RM v3.0 / Vault Clinical Docs** fields on Document Type map the taxonomy to artifacts (see [Document Types](document-types.html)), while the **Binder Section to Document Type** model matches documents to filing locations by taxonomy. Together they auto-file documents to their reference-model location after save and make them browsable by model-artifact hierarchy in the **TMF Viewer** (see [TMF Viewer](tmf-viewer.html)).

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Model / Artifact: Create, Read, Edit | Maintaining reference models and the artifact tree |

Models and artifacts are system-managed master data, seeded out of the box; **Clinical Application Administrator** may adjust them, **Document Contributor** is read-only.
