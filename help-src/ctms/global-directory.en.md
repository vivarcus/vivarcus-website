---
title: Global Directory
description: Learn the four master-data sub-tabs of the Global Directory — Organizations, Products, Study Product Roles, and Personnel — and how the study hierarchy references them.
last_updated: 2026-08-15
related:
  - study-personnel
  - site-lifecycle
  - overview
---

## Organizations

An **Organization** is master data for companies/institutions/sites, referenced by studies via Study Organization. Maintain under **Global Directory → Organizations**:

| Field | Notes |
|-------|-------|
| **Organization** | Organization name (required, unique) |
| **Organization Type** | Organization type (object type), e.g. `Institution` |
| **Parent Organization** | Parent organization (self-reference) |
| **Status** | `Active` / `Inactive` (lifecycle-driven) |

The **Study Participation** section on the detail page shows every study the organization participates in; organizations can also be created inline from the **Study Organizations** section on the study detail (see [Study Personnel & Communication](study-personnel.html)).

## Products

A **Product** is master data for the active ingredient or asset used in a study. Maintain under **Global Directory → Products**: **Product Name** (required, unique), **Status**, **External ID**. Products attach to a study through a **Study Product** — created from the **Studies** section on the **Product** detail page or the **Study Products** section on the **Study** detail page, with the product's role in that study (below).

## Study Product Roles

A **Study Product Role** defines the role a product plays in a study; five are seeded:

| Role | Meaning |
|------|---------|
| **Lead Agent** | Lead (investigational) agent |
| **Comparator Agent** | Comparator agent |
| **Placebo** | Placebo |
| **Device** | Device |
| **Diagnostic** | Diagnostic product |

Pick the **Study Role** when creating a Study Product to express "what this product does in this study".

## Personnel

A **Person** is the global directory of people — investigators, site staff, vendor personnel, internal personnel, and IRB/IEC members — and the source for the study team (Study Person). Maintain under **Global Directory → Personnel**:

| Field | Notes |
|-------|-------|
| **First / Last Name** | First / last name (required) |
| **Email** | Email (required) |
| **Person Type** | Object type: `Internal` (default), `Investigator`, `Site Staff`, `Vendor`, `IRB/IEC` |
| **Vault User** | Links a Vault user (unique); shared fields stay in sync |
| **Manager** | Manager (self-reference) |
| **External ID / CDX ID / Global ID** | Integration mapping fields |
| **Debarred / Key Opinion Leader / NPI Number** | Compliance and profile flags |

The **Study Participation** section shows the person's study team records; **Contact Information** holds contact details. Run **Promote to User** to promote a person to a Vault user. The Study Person's person field can create a Person inline (see [Study Personnel & Communication](study-personnel.html)).

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Same organization/person registered in many studies | Keep master data in the global directory; reference it from studies via Study Organization / Study Person |
| Promote to User not visible | Confirm the person isn't linked to a Vault user yet and you hold the permission |
| Can't find a product | Create it under **Global Directory → Products** first, then attach it to the study from the Study Products section |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Organization / Product / Study Product Role / Person: Create, Read, Edit | Maintaining global directory master data |

**CTMS Study Manager** can create organizations (Institution / IRB-IEC / Sponsor / Vendor types), products, product roles, and all person types; **CRA** and **Central Monitor** are mostly read-only; deletion is limited to **CTMS Business/System Administrators**.
