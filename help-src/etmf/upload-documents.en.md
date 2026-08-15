---
title: Uploading & Matching Documents
description: Learn the recommended path of creating documents from EDL Items, the three creation methods (Upload / Placeholder / From Template), and the alternative path of creating from the document library.
last_updated: 2026-08-15
related:
  - edl
  - review-workflow
  - tmf-viewer
---

## Creating Documents from an EDL Item (Recommended)

Creating documents **from an EDL Item** is recommended — the system carries over fields such as Study and Classification, which maximizes matching success:

1. Open the study → **Expected Documents** list, choose an entry (e.g. a Protocol entry), and open its detail page to check **Document Type / Classification**, **# Expected**, **Completeness**.
2. **All Actions → Create Document**.
3. Choose a creation method (see below), fill in the Name (e.g. `EXP-Protocol-v1`), verify Study and Document Type / Classification were carried over, upload the PDF, and save.

The document is created in the **In Progress** state at version ~**0.1**.

## Three Creation Methods

| Method | Description | Use when |
|--------|-------------|----------|
| **Upload** | Upload a source file (PDF etc.) | Regular case with an existing file |
| **Placeholder** | Create a document without a file | The file is not ready yet |
| **From Template** | Create from a document template | The document type has an available template |

> Creating from an EDL Item only pre-fills fields; the match relationship is established automatically after the document is saved (see matching rules in [EDL & Expected Documents](edl.html)).

## Creating from the Document Library (Alternative)

If you don't use the EDL Item entry point:

1. Open **Documents** (the library) → **Create**.
2. Manually fill in **Study** and **Document Type / Classification** (must match the target EDL Item).
3. Upload the file and save.

Field alignment is the key to matching when creating manually: a match is established only when all configured matching fields agree.

## What Happens After Saving

- The document enters a controlled lifecycle (In Progress) and can be submitted for review (see [Review & Approval](review-workflow.html)).
- The system automatically matches relevant EDL Items; results appear in each entry's **Matched Documents** section.
- Approved documents whose classification maps to the reference model are automatically filed into Master File Binders (see [TMF Viewer & Master File Binders](tmf-viewer.html)).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Create Document is missing | Verify the account has expected-document action permissions and the entry is Active |
| Matched Documents is empty | Verify the document's Study, Classification etc. match the EDL Item; wait a few seconds and refresh, or run Match Documents |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Document: Create, Edit | Uploading source files, saving documents |
| Object action | EDL Item: **Create Document** | Creating from an expected document entry (recommended path) |
| Object | EDL Item: Read | Viewing entry details and Matched Documents |

**Document Contributor** has all of the above. Read-only roles can browse the document library but cannot create or upload.
