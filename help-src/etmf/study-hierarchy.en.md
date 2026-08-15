---
title: Study Hierarchy: Creating Studies, Countries & Sites
description: Learn how to create a Study, configure milestone master sets and template EDLs, run Plan Study and Ready to Enroll, and create study countries and sites.
last_updated: 2026-08-15
related:
  - edl
  - milestones
  - tmf-homepage
---

## The Three-Level Structure

All documents, milestones, and quality records of a clinical trial are organized under a three-level structure: **Study → Study Country → Study Site**.

| Level | Object | Purpose |
|-------|--------|---------|
| Study | Study | Carrier of the trial backbone; its lifecycle drives milestone and EDL generation |
| Study Country | Study Country | Scopes documents and milestones by country |
| Study Site | Study Site | Filing location for site-level documents |

> Milestones and Expected Document Lists (EDLs) are only generated after the study reaches the **Active** state.

## Creating a Study

1. Log in, select your Vault, open **Study Info → Studies**, and click **Create**.
2. Fill in **Study Number** and **Study Phase** (e.g. `Phase III`), then save.

The study is created in the **Candidate** state.

## Configuring and Activating a Study

Two steps take a study from Candidate to Active:

| Action | Steps | Result |
|--------|-------|--------|
| Configure | In **Study Configuration Details** on the study detail page, select **Milestone Master Set** and **Template EDL** | Configuration saved |
| **Plan Study** | **All Actions → Plan Study**, fill in **Study Start Date**, submit | State becomes **Planning**; milestones and expected documents are generated automatically |
| **Ready to Enroll** | **All Actions → Ready to Enroll**, submit | State becomes **Active** |

Afterwards, the **Milestones** list and **Expected Documents** list appear on the study detail page.

> If Plan Study is unavailable, verify that Milestone Master Set and Template EDL are filled in.

## Creating a Study Country

Open **Study Info → Study Countries** and create:

| Field | Notes |
|-------|-------|
| **Study Number** | Select the parent study |
| **Country** | Select the country (e.g. United States) |
| **Study Country Name** | Auto-generated after selecting Country; no manual entry needed |

## Creating a Study Site

Open **Study Info → Study Sites** and create:

| Field | Notes |
|-------|-------|
| **Study Site Number** | Site number (e.g. `Site-001`); Name is this same field |
| **Study Country** | Select the parent study country |
| **Study Number** | Leave blank — derived automatically from the Study Country |

After saving, open the site detail page and confirm that **Study Number** points to the parent study automatically.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| No Name field when creating a Study | The field is labeled **Study Number** |
| Study Country Name is read-only | It is auto-generated after selecting Country |
| No Site Number field | Name and Site Number are one field: **Study Site Number** |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Study / Study Country / Study Site: Create, Read, Edit | Creating studies, countries and sites, maintaining fields |
| Lifecycle action | Study: **Plan Study**, **Ready to Enroll** | Advancing study state, generating milestones and EDLs |
| Lifecycle action | Study Country: **Select Country** | Selecting the country (prerequisite for CTMS site activation) |

**Clinical Application Administrator** has all of the above; **Document Contributor** is read-only on the study hierarchy and cannot create or advance lifecycles.
