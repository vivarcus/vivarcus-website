---
title: Using Vault AI in Record Context
description: Open a record, then use the Vault AI chat panel to ask, summarize, and translate; use Start Trace to keep a dedicated conversation per record.
last_updated: 2026-08-15
related:
  - overview
  - chat
---

## Opening Record Context

Open any record detail page (study, document, organization, etc.) and click the **Vault AI** button in the top-right header. The floating panel recognizes the current record and switches to its dedicated conversation; the input placeholder becomes "Ask about this record…".

With no record open, the panel instead prompts "Open a record to chat with Vault AI".

<img src="/assets/help/screenshots/en/vault-ai-panel-empty.png" alt="Vault AI chat panel without a record open, prompting to open a record">

*No record open: the panel asks you to open one first.*

## Quick Actions

The record-context panel offers quick actions:

| Action | What it does |
|--------|--------------|
| **Ask** | Free-form questions about the current record |
| **Summarize Record** | One-click structured summary: key fields, milestones, document requirements, and to-dos |
| **Translate Record** | Translate record content into another language |

Clicking an action sends the request immediately. On a study record, for example, **Summarize Record** produces a summary with the study number, phase, status, milestones, EDL requirements, and open tasks.

<img src="/assets/help/screenshots/en/vault-ai-panel-record.png" alt="Vault AI chat panel opened on an organization record, with an Ask about this record input">

*The chat panel on an organization record, ready for questions about it.*

## Start Trace

The **Start Trace** button at the top of the panel keeps a dedicated conversation for the current record:

- The record's conversation appears in the panel's Recent Chats list, named after the record ID.
- Returning to the record restores its conversation automatically (when auto-switch is enabled by an administrator).
- Keep asking in the panel at any time; questions stay scoped to that record.

## Docking the Panel

Click **Panel** at the top of the panel to dock it to the right side of the page: browse the record fields on the left while the conversation stays open on the right. Once docked, you can:

- **Fullscreen**: expand to a full-page chat;
- **Floating**: return to the centered popup mode;
- **Close**: dismiss the panel.

<img src="/assets/help/screenshots/en/vault-ai-panel-docked.png" alt="Vault AI chat panel docked on the right side of the page, next to the Acme Clinical Research record details">

*Docked mode: browse the record on the left, keep chatting on the right.*

## Tips

- Conversations are independent per record; a conversation on a record is shared with other users who have access to it.
- For cross-record questions (e.g. "How many studies are in this vault?"), use the Vault AI tab — see [Chatting with Vault AI](chat.html).
