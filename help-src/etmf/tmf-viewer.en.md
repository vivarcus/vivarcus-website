---
title: TMF Viewer & Master File Binders
description: Understand the division of labor between Binders (physical filing) and the TMF Viewer (virtual browsing by reference model), and learn Create Study Binders, auto-filing, and View Model switching.
last_updated: 2026-08-15
related:
  - upload-documents
  - review-workflow
  - overview
---

## Binder vs Viewer

eTMF provides two ways to find documents by the reference model, with different roles:

| | Binder | TMF Viewer |
|--|--------|------------|
| Role | **Physical filing container** of the Master File | **Virtual view** computed from DocType → Artifact mapping |
| Creation | Requires **Create Study Binders**; supports Auto-Filing / manual links | **Independent** of whether Binders exist |
| Content | Section tree → document links (with Filing Origin) | Artifact tree + document list, computed by Study scope |

Moving documents in or out of a Binder does **not** change their position in the Viewer; Viewer positions depend only on document classification and Study scope.

## Creating Study Binders

1. Open the study → **All Actions → Create Study Binders**.
2. Select the **Model** (e.g. **TMF RM v3.0**) and **Filing Levels** (study / country / site level master files), then confirm.
3. After creation you'll see a **Study Level File**, **Country Level File**, and **Site Level File** (for existing countries/sites).

> Creating again when a same-level Binder already exists is idempotent (may count as skipped).

## Auto-Filing

Approved documents whose classification maps to the current Model are linked into the corresponding Section node with **Filing Origin = Auto-filed**:

- Country/site-level documents only land in the matching level's Binder; they do **not** fall back to Study Level.
- If the tree is empty, wait a few seconds and refresh; otherwise run **Refresh Auto-Filing**.
- Repeated refreshes do **not** create duplicate nodes.

## Using the TMF Viewer

1. Top navigation → **TMF Viewer**.
2. Select the **Study**; choose the **View Model** (ideally the same Model used for Binders).
3. Expand the Artifact tree on the left to locate documents; click a document in the right list to open its detail page.
4. Select Study Country / Study Site to scope the view; **Collapse All / Expand All** controls tree expansion.

> If the Viewer tree is empty: verify a Study is selected and documents have a Classification mapped to the current View Model.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Approved documents missing in the Binder tree | Verify the matching-level Binder exists, the Model's Artifact mapping covers the DocType, wait for the job, or run Refresh Auto-Filing |
| Refresh Auto-Filing changes nothing | Verify document Study / Country / Site exactly match the Binder level, and Classification maps to the Binder's Model |
| New uploads not visible in the Viewer | Verify Document Type / Classification maps to the TMF RM and the document's Study field is correct |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Tab | TMF Viewer: View | Accessing the TMF Viewer |
| Object | Document: Read | Browsing and opening documents |
| Object action | Study: **Create Study Binders** | Generating Master File Binders |
| Object action | Binder: **Refresh Auto-Filing** | Manually triggering auto-filing |

Read-only roles such as **External Inspector** can use the Viewer fully (virtual browsing does not depend on Binders); creating Binders and refreshing filing require edit-class permissions.
