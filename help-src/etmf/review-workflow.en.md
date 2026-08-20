---
title: Document Review, Approval & Versioning
description: Learn the full controlled document lifecycle: submit for review, content review, QC, approval, electronic signature, and versioning when amendments occur.
last_updated: 2026-08-20
related:
  - upload-documents
  - quality-issues
  - milestones
---

## The Document Lifecycle

Documents move through a controlled lifecycle in Vivarcus:

| State | Meaning |
|-------|---------|
| **In Progress** | Draft (version ~0.1) |
| **In Review** | Submitted, awaiting content review |
| **In QC Review** | Content review passed, awaiting QC |
| **In Approval** | QC passed, awaiting approval |
| **Approved** | Approved (version ~1.0), steady state |

## Submitting for Review

Open the document detail page → **All Actions → Submit for Review**:

1. Assign a **Reviewer** and a **QC Reviewer** (search any Vault user; choose yourself in a single-account trial).
2. Fill in **Due Date** and submit. The state becomes **In Review**.

## Review, QC & Approval

| Task | Steps | Result |
|------|-------|--------|
| **Review Content** | Open it in **My Tasks** and complete it, choose **Send to QC** (no Accept step) | State becomes In QC Review |
| **QC Review** | Complete it, choose **Passed** | State becomes In Approval |
| **Approve Document** | **All Actions → Approve**, assign an Approver and submit; complete the approval task in **My Tasks** (with electronic signature if required) | State becomes Approved, version ~1.0 |

> Short on time? Use **All Actions → Promote to Approved** to skip the review steps.

## Versioning Documents

Amendments and content updates require a new version:

1. Run **New Version In Progress** (or **Upload New Version**) on the approved document.
2. Upload the new file (optionally rename, e.g. `EXP-Protocol-v2`) and save.
3. Run the review and approval again (or **Promote to Approved**).

The same document family keeps its version history; the steady-state version advances (e.g. **2.0**).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Submit for Review is missing | Verify the document is saved and the account has document action permissions |
| Cannot find users in the start dialog | Search by name or email; you do not need to grant Reviewer / QC Reviewer in Sharing first |
| Electronic signature step fails | Follow the on-page prompts; contact support if it persists |
| Want to skip review | Use **Promote to Approved** |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Document: Read, Edit | Opening documents, submitting for review, versioning |
| Lifecycle action | Document: **Submit for Review**, **Review Content**, **QC Review**, **Approve**, **Promote to Approved** | Advancing the document lifecycle |
| Workflow | E-signature, Read & Understood | Approval signatures and notification distribution (per workflow config) |
| Object | Clinical User Task: Read, Edit | Completing review tasks in My Tasks |

In a single-account trial the same account can complete every step; in multi-role environments admins grant the relevant lifecycle actions by responsibility.
