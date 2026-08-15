---
title: What Is eTMF & the TMF Reference Model
description: Learn the core concepts of Vivarcus eTMF: the study hierarchy, Expected Document Lists (EDLs), milestones, the TMF Reference Model, and the five-step manage–collect–review–change–inspect workflow.
last_updated: 2026-08-15
related:
  - study-hierarchy
  - edl
  - tmf-homepage
---

## What Is eTMF

The eTMF (electronic Trial Master File) is the electronic archive of all essential documents for a clinical trial. Every critical document produced during a study — protocol, ethics approvals, informed consent forms, investigator brochures, monitoring reports — is filed into the trial master file according to defined rules, so that the trial's story is always traceable and ready for inspection.

Vivarcus eTMF serves sponsors and CROs with document collection, review, approval, filing, and inspection-readiness tracking. The core workflow can be summarized in five steps: **manage → collect → review → change → inspect**.

## Core Concepts

### Study Hierarchy

All documents, milestones, and quality records are organized under a three-level structure: **Study → Study Country → Study Site**. Once a study is created and its lifecycle advances, the system automatically generates the milestone list and the Expected Document List. See [Study Hierarchy](study-hierarchy.html).

### Expected Document List (EDL)

The EDL is the checklist of "what this TMF should contain"; its entries are called Expected Documents (EDL Items). The system measures document completeness against the EDL and uses it as the target for automatic filing. See [EDL & Expected Documents](edl.html).

### Milestones

Milestones mark key study events (e.g. first subject enrolled, database lock) with planned and actual dates, and drive the completeness calculation on the TMF Homepage. See [Milestones](milestones.html).

### Document Lifecycle

Documents move through a controlled lifecycle: Draft → Review → Approved → Steady State. Approved documents are automatically filed into their Master File locations, browsable by the TMF Reference Model. See [Review & Approval](review-workflow.html) and [TMF Viewer](tmf-viewer.html).

## The TMF Reference Model

The TMF Reference Model is the industry-standard classification for trial master file content, organizing TMF documents into Zones, Sections, and Artifacts. Vivarcus bases its default document type structure and auto-filing paths on this model, so the filing structure is commonly understood by sponsors, CROs, and inspectors alike.

## A Typical Workflow

| Stage | Meaning | Features involved |
|-------|---------|-------------------|
| **Manage** | Build the study hierarchy, configure EDL and milestones | Study lifecycle, Plan Study |
| **Collect** | Upload documents, automatic matching and filing | Upload & Matching, EDL |
| **Review** | Review, QC, approval, quality issue closure | Review workflow, Quality Issues |
| **Change** | Cascade tracking after protocol amendments | Document versioning, expected document matching |
| **Inspect** | Browse by reference model, inspection readiness check | TMF Homepage, TMF Viewer |

## Before You Start

> Use Chrome or Edge, ideally with a window width of at least 1280px. For your first trial, ask your administrator for the login URL, account, and role. Milestones and EDLs are only generated after the study reaches the Active state.

## Required Permissions & Roles

| Permission set | Role | Typical capabilities |
|----------------|------|----------------------|
| **Clinical Application Administrator** | Clinical application admin | Full CRUD and lifecycle actions on all objects |
| **Document Contributor** | Document contributor | Read-only on study objects; edit on documents, EDLs, clinical tasks |
| **External Inspector** | Agency inspector | Read-only |

Permissions have two layers: the **Security Profile / permission set** determines which actions you can perform; **Team Role + Grant Access** (study team) determines which studies' data you can see. See the "Required Permissions & Roles" section of each article for granular detail.
