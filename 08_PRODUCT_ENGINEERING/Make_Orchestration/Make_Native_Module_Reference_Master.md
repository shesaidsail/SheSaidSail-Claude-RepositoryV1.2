# Make Native Module Reference Master
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION REFERENCE
**Source of Truth:** SheSaidSail_Make_Modules_Master_List.pdf (approved module inventory)

---

## Purpose

This file is the canonical reference for every native Make module available to the She Said Sail + Mare Executive production account. All entries are extracted verbatim from the approved PDF module inventory. No modules have been added, inferred, or hallucinated.

**Audit usage:** When a blueprint JSON uses a module, cross-reference this file to determine whether a native equivalent exists. If a module identifier does not map to an entry in this file, it must be flagged as unverified.

**Make internal module IDs vs display names:** The PDF uses Make's UI display names. Blueprint JSON files use Make's internal module identifiers (e.g., `slack:CreateMessage` is the internal ID for the display name "Send a Message"). Cross-referencing between JSON identifiers and PDF display names requires name-to-ID mapping knowledge; ambiguous mappings are flagged in the Gap Audit.

---

## Category Legend

- **NATIVE-VERIFIED** — Module confirmed in approved PDF inventory; safe to use natively
- **PDF-ONLY** — Module exists in PDF but not yet used in any Stage 1 blueprint
- **TRIGGER-UNVERIFIED** — Make trigger/watch modules; PDF lists only action modules; trigger availability requires separate verification in Make UI

---

# Airtable

## Category: Records — Action Modules

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Records | Yes — idempotency checks, booking lookups | Yes | NATIVE-VERIFIED |
| Get a Record | Yes — full record fetch before processing | Yes | NATIVE-VERIFIED |
| Create a Record | Yes — lead creation, audit log writes | Yes | NATIVE-VERIFIED |
| Update a Record | Yes — status updates, field writes | Yes | NATIVE-VERIFIED |
| Upsert a Record | Not used in Stage 1 | Yes (for create-or-update patterns) | PDF-ONLY |
| Delete a Record | Not used in Stage 1 | Yes | PDF-ONLY |
| Bulk Create Records (advanced) | Not used in Stage 1 | Yes (for batch creates) | PDF-ONLY |
| Bulk Update Records (advanced) | Not used in Stage 1 | Yes (for batch updates) | PDF-ONLY |
| Bulk Upsert Records (advanced) | Not used in Stage 1 | Yes (for batch upsert) | PDF-ONLY |
| Bulk Delete Records (advanced) | Not used in Stage 1 | Yes (for batch deletes) | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback for unsupported operations | PDF-ONLY |

**Notes:**
- PDF does not list any Airtable trigger/watch modules. Blueprint JSON uses `airtable:TriggerNewRecord` in M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION. This module is NOT listed in the PDF; availability must be confirmed in Make UI under Airtable app triggers.
- All action modules confirmed available and native. Internal Make IDs: `airtable:ActionCreateRecord`, `airtable:ActionUpdateRecord`, `airtable:ActionSearchRecords`, `airtable:ActionGetRecord`.

---

# Slack

## Category: Messages

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search for Message | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Private Channel Message | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Public Channel Message | Not used in Stage 1 | N/A | PDF-ONLY |
| List Replies | Not used in Stage 1 | N/A | PDF-ONLY |
| Send a Message | Yes — all alert routes, operational notifications | Yes — replaces HTTP Slack webhook posts | NATIVE-VERIFIED |
| Edit a Message | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Message | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Files

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Files | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Upload a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Send a File Message | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a File | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Channels

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Channels | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| List Members in a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Set the Topic of a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Set the Purpose of a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Join a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Leave a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Archive a Channel | Not used in Stage 1 | N/A | PDF-ONLY |
| Unarchive a Channel | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Reactions & Pins

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Reactions | Not used in Stage 1 | N/A | PDF-ONLY |
| Add a Reaction | Not used in Stage 1 | N/A | PDF-ONLY |
| Remove a Reaction | Not used in Stage 1 | N/A | PDF-ONLY |
| Add a Star | Not used in Stage 1 | N/A | PDF-ONLY |
| Remove a Star | Not used in Stage 1 | N/A | PDF-ONLY |
| Save an Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Remove Saved Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Pin a Message | Not used in Stage 1 | N/A | PDF-ONLY |
| Unpin a Message | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Users

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search for User | Not used in Stage 1 | N/A | PDF-ONLY |
| List Users | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Invite Users | Not used in Stage 1 | N/A | PDF-ONLY |
| Kick a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Reminder | Not used in Stage 1 | N/A | PDF-ONLY |
| Set a Status | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

**Notes:**
- `slack:CreateMessage` is the Make internal ID for "Send a Message." All Slack alert modules in Stage 1 blueprints use this and are verified native.
- DM routing in M-SLACK-ALERTS uses the channel field with a User ID (not a module name) — this is a field value, not a separate module.

---

# Anthropic Claude

## Category: Prompts & Messages

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Simple Text Prompt | Candidate for M-BRAND-ROUTER, M-BOOKING-CREATION | Yes — may replace HTTP POST to Anthropic API | NATIVE-VERIFIED (see notes) |
| Create a Prompt | Candidate — not used in Stage 1 as named | N/A | PDF-ONLY |

## Category: Files

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Files | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Download a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Upload a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a File | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Skills

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Skills | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Skill | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Skill | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Skill | Not used in Stage 1 | N/A | PDF-ONLY |
| List Skill Versions | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Skill Version | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Skill Version | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Skill Version | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

**CRITICAL NOTES — Anthropic Claude:**
- The blueprint JSON uses internal identifier `anthropic:ActionCreateMessage`. This identifier does NOT appear by that display name in the PDF. The PDF lists "Simple Text Prompt" and "Create a Prompt."
- In Make.com's Anthropic Claude native app, "Simple Text Prompt" is the display name most likely mapped to `anthropic:ActionCreateMessage`. However, this mapping is **unconfirmed** against the PDF.
- The `anthropic:ActionCreateMessage` module in blueprints is configured with `model`, `max_tokens`, `temperature`, `system`, and `messages` parameters. The STAGE_1_NATIVE_REBINDING_GUIDE.md already notes: "If Make's native Anthropic module does not show a temperature field, it may default to 1.0." This suggests the module may not support full parameter control.
- **MUST VERIFY** in Make UI: open Anthropic Claude app and confirm whether "Simple Text Prompt" exposes `model`, `max_tokens`, `temperature`, `system`, and `messages` fields. If it does not, the blueprints using `anthropic:ActionCreateMessage` will require patching before import.
- Model version `claude-sonnet-4-20250514` used in M-BRAND-ROUTER and M-BOOKING-CREATION must be confirmed as available in the Make Anthropic module's model dropdown.

---

# Gmail

## Category: Email

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Send an email | Yes — auto-reply, deposit email, confirmation email, charter brief, balance reminder | Yes — replaces HTTP Gmail API calls | NATIVE-VERIFIED |
| Reply to an email | Not used in Stage 1 | N/A | PDF-ONLY |
| Search emails | Not used in Stage 1 | N/A | PDF-ONLY |
| Get an email | Not used in Stage 1 | N/A | PDF-ONLY |
| Copy an email | Not used in Stage 1 | N/A | PDF-ONLY |
| Move an email | Not used in Stage 1 | N/A | PDF-ONLY |
| Update email labels | Not used in Stage 1 | N/A | PDF-ONLY |
| Mark an email as read | Not used in Stage 1 | N/A | PDF-ONLY |
| Mark an email as unread | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete an email | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a draft email | Not used in Stage 1 | N/A | PDF-ONLY |
| Send a draft email | Not used in Stage 1 | N/A | PDF-ONLY |
| List email attachments and media | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

**Notes:**
- `gmail:ActionSendEmail` is the Make internal ID for "Send an email." Used in 5 blueprints. Fully verified native.
- All Gmail modules in blueprints send from `hello@shesaidsail.com`. The Gmail connection must be authorized with the Google account that owns this address.

---

# Google Calendar

## Category: Events

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Events | Not used in Stage 1 | N/A | PDF-ONLY |
| Get an Event | Not used in Stage 1 | N/A | PDF-ONLY |
| Create an Event | Not used in Stage 1 | N/A | PDF-ONLY |
| Duplicate an Event | Not used in Stage 1 | N/A | PDF-ONLY |
| Update an Event | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete an Event | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Calendars

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Calendars | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Calendar | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Calendar | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Calendar | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Calendar | Not used in Stage 1 | N/A | PDF-ONLY |
| Clear a Calendar | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Access Control

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Access Control Rules | Not used in Stage 1 | N/A | PDF-ONLY |
| Get an Access Control Rule | Not used in Stage 1 | N/A | PDF-ONLY |
| Create an Access Control Rule | Not used in Stage 1 | N/A | PDF-ONLY |
| Update an Access Control Rule | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete an Access Control Rule | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |
| Get Free/Busy Information | Not used in Stage 1 | N/A | PDF-ONLY |

**Notes:** Google Calendar is not used in any Stage 1 blueprint. Available for Stage 2+ charter scheduling automation.

---

# Google Docs

## Category: Documents

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Documents | Not used in Stage 1 | N/A | PDF-ONLY |
| Get Content of a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Document from a Template | Not used in Stage 1 | N/A | PDF-ONLY |
| Insert a Paragraph to a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Insert an Image to a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Replace an Image with a New Image | Not used in Stage 1 | N/A | PDF-ONLY |
| Replace a Text in a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Download a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |
| Make All Links in a Document Clickable | Not used in Stage 1 | N/A | PDF-ONLY |

**Notes:** Google Docs is not used in any Stage 1 blueprint. Available for Stage 2+ charter brief document generation.

---

# DocuSign

## Category: Envelopes

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Envelopes | Not used in Stage 1 | N/A | PDF-ONLY |
| Get an Envelope Status | Not used in Stage 1 | N/A | PDF-ONLY |
| Download a Document | Not used in Stage 1 | N/A | PDF-ONLY |
| Get an Envelope Form Data | Not used in Stage 1 | N/A | PDF-ONLY |
| Send a Document to Sign | Not used in Stage 1 | N/A | PDF-ONLY |
| Send a Document from Template to Sign | Not used in Stage 1 | N/A | PDF-ONLY |
| Void an Envelope | Not used in Stage 1 | N/A | PDF-ONLY |
| List Envelope Documents | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Signing Groups

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Signing Groups | Not used in Stage 1 | N/A | PDF-ONLY |
| Create Signing Groups | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

## Category: Templates & Bulk Send

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Create Template from Document | Not used in Stage 1 | N/A | PDF-ONLY |
| List Templates | Not used in Stage 1 | N/A | PDF-ONLY |
| List Template Documents | Not used in Stage 1 | N/A | PDF-ONLY |
| Update Template | Not used in Stage 1 | N/A | PDF-ONLY |
| Create Bulk Send List | Not used in Stage 1 | N/A | PDF-ONLY |
| Add to Bulk Send List | Not used in Stage 1 | N/A | PDF-ONLY |
| Test Bulk Send List | Not used in Stage 1 | N/A | PDF-ONLY |
| Bulk Send Envelope from Template | Not used in Stage 1 | N/A | PDF-ONLY |
| Create Long-lived Pre-filled Webform Link | Not used in Stage 1 | N/A | PDF-ONLY |
| Create Short-lived Pre-filled Webform Link | Not used in Stage 1 | N/A | PDF-ONLY |

**Notes:** DocuSign is not used in any Stage 1 blueprint. Available for agreement/contract signing automation in Stage 2+.

---

# Google Drive

## Category: Files & Folders

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search for Files/Folders | Not used in Stage 1 | N/A | PDF-ONLY |
| Download a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a File from Text | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Folder | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a File/Folder Shortcut | Not used in Stage 1 | N/A | PDF-ONLY |
| Upload a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Rename a Folder | Not used in Stage 1 | N/A | PDF-ONLY |
| Move a File/Folder to Trash | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a File/Folder | Not used in Stage 1 | N/A | PDF-ONLY |
| Copy a File | Not used in Stage 1 | N/A | PDF-ONLY |
| Move a File/Folder | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Share Link | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a File/Folder Access | Not used in Stage 1 | N/A | PDF-ONLY |
| Revoke a File/Folder Access | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Folder ID for a Path | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a File/Folder Path for an ID | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

## Category: Shared Drives

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search for Shared Drives | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Shared Drive | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Shared Drive | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Shared Drive | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Shared Drive | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: File Revisions

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List File Revisions | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a File Revision | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a File Revision | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a File Revision | Not used in Stage 1 | N/A | PDF-ONLY |

**Notes:** Google Drive is not used in any Stage 1 blueprint. Available for Stage 2+ document storage automation.

---

# Instagram for Business

## Category: Posts & Media

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Get user insights | Not used in Stage 1 | N/A | PDF-ONLY |
| Get post insights | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a photo post | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a reel post | Not used in Stage 1 | N/A | PDF-ONLY |
| Create carousel post | Not used in Stage 1 | N/A | PDF-ONLY |
| List posts | Not used in Stage 1 | N/A | PDF-ONLY |
| List public user posts | Not used in Stage 1 | N/A | PDF-ONLY |
| Get post | Not used in Stage 1 | N/A | PDF-ONLY |
| Download media | Not used in Stage 1 | N/A | PDF-ONLY |
| Get carousel media | Not used in Stage 1 | N/A | PDF-ONLY |
| Get public user info | Not used in Stage 1 | N/A | PDF-ONLY |
| List post comments | Not used in Stage 1 | N/A | PDF-ONLY |
| List comment replies | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a comment | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a reply | Not used in Stage 1 | N/A | PDF-ONLY |
| List stories | Not used in Stage 1 | N/A | PDF-ONLY |

**Notes:** Instagram for Business is not used in any Stage 1 blueprint. Available for marketing automation in later stages.

---

# WordPress

## Category: Posts

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Create a Post | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Post | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Post | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Post | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Posts | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Categories & Tags

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Create a Category | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Category | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Category | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Category | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Categories | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Tag | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Tag | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Tag | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Tag | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Tags | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Taxonomies | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Comments

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Create a Comment | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Comment | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Comment | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Comment | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Comments | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Media & Users

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Create a Media Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Media Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Media Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a Media Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Media Items | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Get a User | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Users | Not used in Stage 1 | N/A | PDF-ONLY |
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |

**Notes:** WordPress is not used in any Stage 1 blueprint. Available for content/SEO automation in later stages.

---

# Stripe

## Category: Payment Intents

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Make an API Call | Not used in Stage 1 | N/A — fallback | PDF-ONLY |
| List Payment Intents | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |
| Confirm a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |
| Capture a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |
| Cancel a Payment Intent | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Customers

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Customers | Not used in Stage 1 | N/A | PDF-ONLY |
| Search Customers (Advanced) | Not used in Stage 1 | N/A | PDF-ONLY |
| List All Customers | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Customer | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve a Customer | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Customer | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Customer | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Refunds & Payouts

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List All Refunds | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Refund | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve a Refund | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Refund | Not used in Stage 1 | N/A | PDF-ONLY |
| List All Payouts | Not used in Stage 1 | N/A | PDF-ONLY |
| Create a Payout | Not used in Stage 1 | N/A | PDF-ONLY |
| Cancel a Payout | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve a Payout | Not used in Stage 1 | N/A | PDF-ONLY |
| Update a Payout | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Balance

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Retrieve Balance | Not used in Stage 1 | N/A | PDF-ONLY |
| List All Balance History | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve a Balance Transaction | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Invoices

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Invoices | Not used in Stage 1 | N/A | PDF-ONLY |
| List All Invoice Line Items | Not used in Stage 1 | N/A | PDF-ONLY |
| Create an Invoice | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve an Invoice | Not used in Stage 1 | N/A | PDF-ONLY |
| Update an Invoice | Not used in Stage 1 | N/A | PDF-ONLY |
| Finalize a Draft Invoice | Not used in Stage 1 | N/A | PDF-ONLY |
| Void an Invoice | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete a Draft Invoice | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Invoice Items

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| Search Invoice Items | Not used in Stage 1 | N/A | PDF-ONLY |
| Create an Invoice Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Retrieve an Invoice Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Update an Invoice Item | Not used in Stage 1 | N/A | PDF-ONLY |
| Delete an Invoice Item | Not used in Stage 1 | N/A | PDF-ONLY |

## Category: Payment Links

| Module Name (exact from PDF) | Usage in Stage 1 | Native Replaces HTTP? | Status |
|---|---|---|---|
| List Payment Link Lines | Not used in Stage 1 | N/A | PDF-ONLY |

**CRITICAL NOTES — Stripe:**
- **"Create a Payment Link" is NOT in the PDF.** The approved module inventory contains only "List Payment Link Lines" under the Payment Links category. There is NO "Create a Payment Link" module listed.
- Blueprint JSON files M-CONCIERGE-ASSIGNMENT (module 6) and M-BOOKING-CONFIRMATION (module 6) both use `stripe:ActionCreatePaymentLink`, which is claimed as a native module in `_native_first_notes`. This claim CANNOT be verified against the PDF.
- This is the most critical gap in the entire Stage 1 blueprint set. Both affected scenarios fail to have a verified native Stripe module for their core payment link creation step.
- **Required action before blueprint patching:** Manually open Make.com → Stripe app → confirm whether "Create a Payment Link" module exists in the account. If not present, the payment link generation step must be redesigned using either: (a) Stripe Payment Intent via native "Create a Payment Intent" module + separate client-side checkout, or (b) HTTP fallback to Stripe's Payment Links API.

---

## Appendix: Make Built-in Modules (Not Tied to External Apps)

These modules appear in blueprints and are Make-native built-ins, not app-specific:

| Make Internal ID | Display Name | Used In Stage 1 |
|---|---|---|
| `gateway:CustomWebHook` | Custom Webhook (trigger) | M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BRAND-ROUTER, M-LEAD-INTAKE, M-STRIPE-DEPOSIT |
| `builtin:BasicRouter` | Router | All 8 blueprints |
| `tools:SetVariable` | Set Variable | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `json:ParseJSON` | Parse JSON | M-BRAND-ROUTER |
| `http:ActionSendData` | HTTP — Make a Request | All 8 blueprints (inter-scenario calls, Quo SMS) |

**Notes:**
- All Make built-in modules (`gateway`, `builtin`, `tools`, `json`) are available in all Make accounts and do not require external app connections.
- `http:ActionSendData` is the Make HTTP module, used for inter-scenario webhook calls and Quo SMS. It is intentionally kept as HTTP where no native alternative exists.

---

## Appendix: Apps NOT in PDF (No Native Module Available)

These services are referenced in Stage 1 blueprints but have NO native Make module in the approved PDF inventory:

| Service | Usage in Stage 1 | Module Type Used | Must Remain |
|---|---|---|---|
| Squarespace | Form submission intake trigger | `gateway:CustomWebHook` | Yes — webhook only; no native Make Squarespace module |
| Quo SMS | Client SMS notifications | `http:ActionSendData` | Yes — HTTP only; no native Make Quo module |
| Make Cross-Scenario Calls | Calling M-AUDIT-LOGGER, M-BRAND-ROUTER from other scenarios | `http:ActionSendData` | Yes — HTTP only; no native Make cross-scenario trigger module |

---

*This file was generated from the approved PDF module inventory. Do not add modules not sourced from the PDF. Do not use this file to infer that a module exists unless it appears above with status NATIVE-VERIFIED.*
