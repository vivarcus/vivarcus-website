---
title: Study Personnel & User Role Setup
description: Learn how to add people to the study team, grant access to related records (URS), generate expected documents by role, and how User Role Setup records are structured and maintained.
last_updated: 2026-08-15
related:
  - study-hierarchy
  - edl
  - overview
---

## Study Personnel

A **Study Person** record attaches a Person to a study (and optionally a country/site), with a **Study Team Role** and start/end dates. The study team is the source of study contacts and drives role-based expected-document generation.

Create from **Admin Setup → Study Personnel**:

| Field | Notes |
|-------|-------|
| **Person** | The person (required); pick from the global directory or create inline |
| **Full Name** | Filled in automatically |
| **Study** | The owning study (required) |
| **Study Country / Study Site** | Cascading study → country → site selection |
| **Study Team Role** | Team role (required), e.g. Study Manager, Contributor, CRA |
| **Grant Access to Related Records** | When checked, the system creates a User Role Setup record granting access to related records |
| **Start / End Date** | Assignment dates |

> Checking **Grant Access to Related Records** is the key step that lets team members actually open study data; without it the person is registered as a contact only.

Role changes drive role-based expected documents: the **Expected Documents** section on the detail page shows the EDL Items generated for that role. Common actions:

| Action | Purpose |
|--------|---------|
| **Create Study Contact** (and In Bulk) | Quickly create study contacts |
| **Resend Study Invitation** (and In Bulk) | Resend the study invitation |
| **Make Inactive** | Remove the person from the team (history kept) |
| **Retrigger EDL Item Creation** | Regenerate expected documents after a role change |

## User Role Setup

**User Role Setup (URS)** is a system-managed **record-level security** object: one record represents "this user has this role in this study/country/site context". It is usually **created automatically** — for example when Grant Access to Related Records is checked on a Study Person; administrators review and maintain it under **Admin Setup → User Role Setup**.

| Field | Notes |
|-------|-------|
| **User** | The granted user |
| **Role** | The granted role (e.g. study_manager, contributor) |
| **Study / Study Country / Study Site** | The scope, cascading |
| **Blinding** | Blinding scope (e.g. Blinded / Unblinded) |
| **Name** | Auto-numbered: `DAC-{######}` |

> URS underpins Vault record-level security (dynamic access control). To change team access, adjust the Study Person's Grant Access and role rather than hand-editing URS records.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Team member can't see study data | Confirm **Grant Access to Related Records** is checked and the team role matches study sharing |
| Expected Documents section is empty | The role hasn't triggered generation; run **Retrigger EDL Item Creation** |
| Odd URS records | They are system-maintained in most cases; verify Grant Access and role setup before editing manually |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | Study Person: Create, Read, Edit | Maintaining the study team and contacts |
| Object actions | Study Person: **Create Study Contact**, **Resend Study Invitation**, **Retrigger EDL Item Creation** | Contacts, invitations, expected-document generation |
| Object | User Role Setup: Read (Create, Edit) | Viewing (managing) record-level grants |

**Clinical Application Administrator** fully manages Study Personnel and URS; **Document Contributor** is read-only on Study Personnel.
