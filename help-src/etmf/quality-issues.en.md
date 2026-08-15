---
title: Quality Issues
description: A Quality Issue records document defects and tracks remediation from discovery to closure. Learn the four states, creation paths, the two-way link with documents, and the TMF Homepage statistics view.
last_updated: 2026-08-15
related:
  - review-workflow
  - tmf-homepage
  - tmf-viewer
---

## What Is a Quality Issue

TMF documents can develop defects over their lifecycle: missing pages, incomplete signatures, wrong content, version confusion. A **Quality Issue** records these defects, links them to a specific document, and tracks remediation from discovery to closure — the core tool of the TMF quality loop, also used to record inspection findings.

## State Flow

| State | Meaning | Available actions |
|-------|---------|-------------------|
| **Initiated** | Recorded, not yet assigned/followed up | **Open** |
| **Open** | In progress, awaiting remediation | **Close** |
| **Closed** | Resolved / verified | **Deactivate** |
| **Inactive** | Archived (hidden from default lists) | Read-only |

Typical flow: **Initiated → Open → Closed**; use Deactivate afterwards if you want it out of active views.

> **Close vs Deactivate**: Close means the issue is resolved and the record stays visible in active views; Deactivate archives it into Inactive.

## Creating a Quality Issue

Creating from the document is recommended (links are pre-filled):

1. Open the document detail page → **Quality Issues** related section → **Create** (Related Document / Study are pre-filled when created from a document).
2. Fill in:

| Field | Notes |
|-------|-------|
| **Quality Issue ID** | Auto-numbered `QI-{######}` |
| **Study** | The owning study |
| **Related Document** | The defective document |
| **QC Issue Type** | Missing / Inaccurate Content / Duplicate / Expired / Incomplete Metadata / Misclassified / Signature Not Present |
| **Assigned To** | The remediation owner |
| **Due Date** | The required resolution date |
| **QC Issue Comments** | Description of the defect |

## Two-Way Linkage

QIs and documents are linked in both directions: from a QI's detail page, click **Related Document** to jump to the defective document; on the document detail page you can see its attached quality issues — the full traceability chain for audits.

## Viewing on the TMF Homepage

The **TMF Homepage → Quality Issues** widget groups issues by type, filterable by **Open / Closed / All / Assigned to me**. QIs you create and Open appear in the Open view.

> Quality issues only appear on the Homepage for document types configured with the Quality Issue field.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Quality Issue: Create, Read, Edit | Creating and maintaining quality issues |
| Lifecycle action | Quality Issue: **Open**, **Close**, **Deactivate** | Advancing the remediation loop |
| Object | Document: Read | Creating QIs from documents and viewing the two-way link |

The QI creation entry usually lives in the related-object section of the document detail page; Read access to a document lets you see the quality issues attached to it.
