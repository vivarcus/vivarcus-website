---
title: Site SAE Tracking
description: Learn how to register serious adverse events (SAEs) at study sites in Site Monitoring, including required fields, links to monitoring events, and maintenance responsibilities.
last_updated: 2026-08-15
related:
  - monitoring-visits
  - subjects
  - site-lifecycle
---

## What Is SAE Tracking

**Site SAE Tracking** records SAE (serious adverse event) information arising at a study site during a study, for CRAs and the monitoring team to track. Entry point: **Site Monitoring → Site SAE Tracking**; you can also register from the **Site SAE Tracking** section of a **Monitoring Event** detail page.

## Registering an SAE

Create a record; **Name** auto-numbers (`SAE-{######}`):

| Field | Notes |
|-------|-------|
| **Study / Study Country / Study Site** | Owning levels (required, cascading); auto-filled when created from a monitoring event |
| **Subject** | The subject (required, filtered by site) |
| **Monitoring Event** | Optionally link the event where the SAE was identified |
| **SAE Name** | SAE name (e.g. the event description) |
| **SAE Start Date** | SAE start date (required) |
| **SAE End Date** | SAE end date |
| **SAE Severity** | `Mild` / `Moderate` / `Severe` |
| **Outcome** | Outcome (required) |
| **Related? / Expected?** | Relationship to the study drug / whether expected |
| **SAE Report Final** | Whether the SAE report is final |

> This page is a **tracking ledger**: register basic SAE information and outcomes; formal pharmacovigilance reporting and submission still follow your institution's SOP in the designated system.

## States & Maintenance

The lifecycle has only **Active → Inactive** (**Status** is lifecycle-driven, not hand-editable), with no automation. Records are maintained manually by the CRA and study team; follow up at monitoring visits and switch the record to Inactive once closed out.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Can't pick a Subject | The subject must belong to the chosen study site; pick the right Study Site first |
| Fields are empty when creating from a monitoring event | Create from the Site SAE Tracking section on the event detail so Study/Site fill automatically |
| Status can't be edited | Status is lifecycle-driven; use lifecycle actions to switch Active / Inactive |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Site SAE Tracking: Create, Read, Edit | Registering and maintaining SAE tracking records |

The **CRA** is the primary user; **CTMS Study Manager** and **Central Monitor** can also create and edit; delete and workflow execution are limited to **CTMS Business/System Administrators**.
