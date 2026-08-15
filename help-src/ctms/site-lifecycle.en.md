---
title: Site Lifecycle: Candidate to Active
description: Learn the full country and site lifecycle: Select Country, Qualify Site, Select Site, Initiate Site, plus the On Hold and Will Not Participate exception paths.
last_updated: 2026-08-15
related:
  - study-lifecycle
  - subjects
  - monitoring-visits
---

## Site State Main Path

| State | Meaning | Key actions |
|-------|---------|-------------|
| **Candidate** | Candidate | **Qualify Site** / **Place Site on Hold** / **Site Will Not Participate** |
| **Qualifying** | Qualifying | **Select Site** |
| **Initiating** | Initiating | **Initiate Site** (requires parent Study to be Active) |
| **Active** | Activated, can enroll | Day-to-day operations |

## Creating & Selecting a Country

1. **Study Countries** → Create: select the **Study** and **Country**, save (state Candidate, Name auto-generated).
2. Open the country detail page → **All Actions → Select Country**, fill in **Country Selected Date**, submit. The state becomes **Initiating**; country-level milestones can be generated.

> A site can only enter Initiating if its parent Country is **not** Candidate — CTMS site activation must follow this lifecycle, not just record creation.

## Main Path: Candidate → Qualifying → Initiating → Active

| Step | Action | Result |
|------|--------|--------|
| 1 | **Study Sites** → Create: **Study Site Number** = `Site-001`, **Study Country** = the country record; leave **Study Number** blank (derived automatically) | State Candidate |
| 2 | **All Actions → Qualify Site** | State Qualifying; site-level milestones can be generated |
| 3 | **All Actions → Select Site**, fill in **Site Selected Date** | State Initiating |
| 4 | Confirm the parent Study is Active → **All Actions → Initiate Site** | State Active |

## Exception Path: On Hold

Run **Place Site on Hold** on a Candidate site, fill in the hold reason (e.g. `PI on medical leave`); the state becomes **Qualifying Hold**. To resume, run **Remove Site Hold** — the site returns to Qualifying and can continue Select / Initiate.

## Exception Path: Will Not Participate

Run **Site Will Not Participate** on a Candidate site, fill in Reason / Notes (e.g. `Imaging capability insufficient`); the state becomes **Not Selected**.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Qualify Site fails | The parent Study must not still be Candidate; run Plan Study first |
| Select Site / Initiate Site fails | The Country must run Select Country first; Initiate Site requires the parent Study to be Active |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Study Country / Study Site: Create, Read, Edit | Creating countries and sites |
| Lifecycle action | Study Country: **Select Country** | Country selection (prerequisite for site activation) |
| Lifecycle action | Study Site: **Qualify Site**, **Select Site**, **Initiate Site**, **Place Site on Hold**, **Remove Site Hold**, **Site Will Not Participate** | Main path and exception paths of the site lifecycle |

Note the lifecycle gates: Initiate Site requires the parent Study to be Active and the parent Country to have completed Select Country.
