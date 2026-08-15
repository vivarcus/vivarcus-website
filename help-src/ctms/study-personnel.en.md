---
title: Study Personnel & Communication (Team / Organizations / Communication Log)
description: Learn the three sub-tabs of Study Personnel & Communication: the study team (Study Personnel), Study Organizations, and the Study Communication Log — fields and creation entry points.
last_updated: 2026-08-15
related:
  - site-lifecycle
  - global-directory
  - study-lifecycle
---

## Study Personnel

A **Study Person** attaches a global-directory person to a study (and optionally a country/site) with a team role and dates. Create under **Study Personnel & Communication → Study Personnel**:

| Field | Notes |
|-------|-------|
| **Person** | The person (required); pick from the global directory or create inline |
| **Full Name** | Filled automatically |
| **Study** | The owning study (required) |
| **Study Country / Study Site** | Cascading study → country → site |
| **Study Team Role** | Team role (required): CRA, Lead CRA, Study Manager, CTMS Study Manager, Contributor, Central Monitor, CTA, etc. |
| **Primary Contact Information** | Main contact info (create inline) |
| **Grant Access to Related Records** | When checked, creates a User Role Setup granting access to related records |
| **Start / End Date** | Assignment dates |

> For access grants (URS) and role-based expected documents, see [Study Personnel & User Role Setup](../etmf/study-personnel.html). Use **Make Inactive** to remove someone from the team (access is cleared and the end date set automatically).

Teams can be refined to **responsibilities**: a `Study Person Responsibility` links a person to a study/country/site with a concrete responsibility (Principal Investigator, Subinvestigator, Clinical Research Coordinator, Regulatory Coordinator, Pharmacist, Study Nurse, and 10 seeded responsibilities in total), maintained on the person detail page.

## Study Organizations

A **Study Organization** records which organizations participate in a study (optionally down to country/site). Create under **Study Personnel & Communication → Study Organizations**:

| Field | Notes |
|-------|-------|
| **Organization** | The organization (required); pick from the global directory or create inline |
| **Study** | The owning study (required) |
| **Study Country / Study Site** | Optional, cascading |
| **Location** | Organization location (filtered by the chosen organization) |
| **Primary Payee** | Whether this is the primary payee |
| **Start / End Date** | Participation dates |

Organizations can also be created from the **Study Organizations** sections on **Study / Study Country / Study Site** detail pages; the organization detail's **Study Participation** section shows all studies it participates in.

## Study Communication Log

The **Study Communication Log** records communications with sites and study personnel (calls, emails, faxes, letters) as an auditable trail. Two types:

| Type | Notes |
|------|-------|
| **Site Communication** (default) | Site communication; study/country/site and contact are required |
| **Other Communication** | Other communication; levels and contact are optional |

| Field | Notes |
|-------|-------|
| **Communication Type** | Required: `Call` / `Email` / `Fax` / `Letter` / `Other` |
| **Primary Communication With** | Main contact (e.g. the principal investigator) |
| **Responsible Person** | Responsible person (required) |
| **Contact Date** | Date/time of initial contact |
| **Description** | Summary (required, ≤75 chars) |
| **Detail** | Details (helps auditors understand purpose and outcome) |
| **Related Inquiry** | Links related exchanges into a communication chain |

Entry points: the **Study Site Communications** section on the **Site** detail page (site communications); the corresponding sections on **Study / Study Country** detail pages (other communications); and this sub-tab's list. Communication records can be referenced by a protocol deviation's **Related Communication** field.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| No Principal Investigator in the role list | Roles come from Study Team Role master data and can be extended by admins; PI/Sub-I roles additionally trigger expected-document generation |
| Can't pick a CRO/IRB type for organizations | This version does not enumerate organizations by Sponsor/CRO/Site; express it via **Organization Type** (e.g. Institution) and Primary Payee |
| Communication log validation fails | Site Communication requires study/country/site and contact; use Other Communication for non-site exchanges |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Study Person: Create, Read, Edit | Maintaining the study team (no delete — use Make Inactive) |
| Object | Study Organization: Create, Read, Edit | Maintaining participating organizations |
| Object | Study Communication Log: Create, Read, Edit | Recording communications |

**CTMS Study Manager**, **CRA**, and **Central Monitor** maintain teams and communications; **CTMS Business Administrator** can delete records; **Document Contributor** is read-only.
