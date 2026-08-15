---
title: EDL & Expected Documents
description: Learn the concepts of Expected Document Lists (EDLs) and EDL Items, the matching rules, the recommended path of creating documents from EDL Items, and the Match Documents / Update Related Expected Documents actions.
last_updated: 2026-08-15
related:
  - upload-documents
  - tmf-homepage
  - overview
---

## What Is an EDL

The EDL (Expected Document List) is the "receivables checklist" of the TMF: it describes which documents should be collected, how many copies, and whether each is required. Admins configure EDLs via templates, and they are generated automatically onto the study (and its countries/sites) by the **Plan Study** action.

EDL entries are called **Expected Documents (EDL Items)**. The system measures document completeness against the EDL, and uses it as the source of filing locations for automatic archiving.

## Recommended Path: Create Documents from an EDL Item

Creating documents **from an EDL Item** is recommended — the system carries over fields such as Study and Classification, which maximizes matching success:

1. Open the study → **Expected Documents** list, and open any entry's detail page.
2. The detail page shows **Document Type / Classification**, **# Expected**, **Completeness**, etc.; the **Matched Documents** section is initially empty.
3. **All Actions → Create Document**, choose a creation method (Upload / Placeholder / From Template), fill in the Name and upload the file, then save.

> Creating from an EDL Item only pre-fills fields; the match relationship is established automatically after the document is saved.

## Matching Rules

The correspondence between documents and EDL Items is maintained by **automatic matching**. The system compares configured matching fields (typically Study, Study Country, Site, Classification, etc.):

- All configured matching fields equal → match established
- A field empty on both sides → treated as equal
- A value on one side and empty on the other → **no match**

When creating documents manually, make sure these fields align with the EDL Item.

## Common Actions

| Action | Purpose |
|--------|---------|
| **Match Documents** | Runs one matching pass for the entry; refreshes Matched Documents and counts |
| **Update Related Expected Documents** | Syncs **# Expected** and **Requiredness** to related entries of the same study (e.g. country/site-level counterparts) |
| **Create Document** | Creates a document from the entry (Upload / Placeholder / From Template) |

> Update Related Expected Documents syncs only counts and requiredness, not document matches.

## Checking Completeness

Counts and status on the entry detail page:

| Field | Meaning |
|-------|---------|
| **All Doc Count** | Total number of matched documents |
| **Steady State Doc Count** | Approved steady-state documents among them |
| **Completeness** | Shows **Complete** when the threshold is met |

> If All Doc Count has a value but Steady State is 0, the matched documents are not yet approved; complete the approval workflow first.

## Expected Documents (EDL Items)

The **Planning → Expected Documents** list aggregates EDL Item entries across the vault; each entry belongs to an EDL and represents "one document type expected at one location". The entry detail shows:

- **Document Type / Classification** and **# Expected** (how many are due), **Requiredness** (required or not)
- **Completeness** counts and the **Matched Documents** section
- **All Actions** offering **Create Document**, **Match Documents**, **Update Related Expected Documents** (see Common Actions above)

Open the study-scoped **Expected Documents** list from the study detail to see only that study's entries; country/site-level entries are visible on the study country/site detail pages.

## Troubleshooting

| Symptom | Suggestion |
|---------|------------|
| Matched Documents is empty | Verify the document's Study, Classification etc. match the EDL Item; wait a few seconds and refresh, or run **Match Documents** |
| Completeness stays Not Started | The document must be saved and all matching fields aligned |
| Related entries unchanged after Update Related | Verify that corresponding country/site-level entries exist in the same study |

## Required Permissions & Roles

| Type | Permission | Controls |
|------|------------|----------|
| Object | EDL / EDL Item: Read, Edit | Viewing lists and entries, editing # Expected and Requiredness |
| Object action | EDL Item: **Create Document**, **Match Documents**, **Update Related Expected Documents** | Creating documents from entries, manual matching, syncing related entries |
| Object | Document: Create, Edit | Saving new documents (matching happens automatically after save) |

**Document Contributor** has read/write on EDLs and documents; read-only roles (e.g. **External Inspector**) can view Matched Documents and counts but cannot run actions.
