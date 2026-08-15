---
title: TMF Homepage: Completeness & Inspection Readiness
description: The TMF Homepage consolidates completeness, timeliness, quality issues and tasks into one health dashboard. Learn the semantics of each widget, the Study selector, and the inspection-readiness checklist.
last_updated: 2026-08-15
related:
  - edl
  - quality-issues
  - milestones
  - overview
---

## Overview

The TMF Homepage is the daily entry point for study health, visualizing the **timeliness, completeness, and quality** of your TMF documents, plus tasks and milestones. At the top, the **Study selector**: Study is required, Study Country / Study Site are optional and scope the metrics down to a country or site.

## Widget Overview

| Widget | Shows |
|--------|-------|
| **Completeness** | Completeness percentage + Unapproved Documents count |
| **Timeliness** | Approval timeliness pie chart (threshold days configured by an admin) |
| **Upcoming Milestones** | Milestones without an Actual Finish Date, filterable by Milestone Category |
| **Quality Issues** | Quality issue pie chart, filterable by Open / Closed / All |
| **My Tasks** | Up to 10 tasks assigned to me |
| **Tasks Requiring Attention** | Overdue / Unassigned / Due Today counts |

## Completeness Semantics

- The percentage is based on EDL Items with **Requiredness = Required** under the selected milestone.
- **Unapproved Documents**: count of documents you can view whose latest version is not steady state (excluding Superseded / Obsolete); clicking opens the pre-filtered document list.
- **Review Overcount**: jumps to EDL Items with Overcount = Yes.
- **Review Pending Decisions**: jumps to EDL Items with Requiredness = Pending Decision.

## Timeliness

Timeliness tracks how long it takes to approve a document and file it in the TMF. The pie chart splits by threshold (e.g. "approved ≤30 days / >30 days"), configured by an admin under **Admin → Settings → Application Settings → eTMF Features**.

## Quality Issues & Tasks

- **Quality Issues** groups issues by type (Duplicate / Expired / Misclassified etc.), filterable by Open, Closed, All, or assigned to me. Issues only appear for document types configured with the Quality Issue field.
- **My Tasks** shows only document, envelope, and clinical user tasks; quality issue tasks are viewed in the Quality Issues widget.

## Inspection Readiness Checklist

| Check | Where to look |
|-------|---------------|
| EDL completeness | **Completeness** percentage |
| Unapproved documents | **Unapproved Documents** count → click into the list |
| Overcount / pending | **Review Overcount** / **Review Pending Decisions** |
| Timeliness | **Timeliness** threshold semantics |
| Open quality issues | **Quality Issues** → Open |
| Upcoming milestones | **Upcoming Milestones** |
| Personal tasks | **My Tasks** |

> If Timeliness shows 0%, there are usually no approved documents yet or no threshold configured; approve a document and refresh.

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Tab | TMF Homepage: View | Accessing the TMF Homepage tab |
| Object | Study / Milestone / EDL Item: Read | Data for Completeness, Upcoming Milestones and other widgets |
| Object | Document: Read | Unapproved Documents count and drill-down |
| Object | Clinical User Task: Read | My Tasks, Tasks Requiring Attention |
| Object | Quality Issue: Read | Quality Issues widget statistics |

The page only shows documents and tasks you have Read access to; data is further scoped by the study hierarchy's dynamic sharing (**Team Role + Grant Access**).
