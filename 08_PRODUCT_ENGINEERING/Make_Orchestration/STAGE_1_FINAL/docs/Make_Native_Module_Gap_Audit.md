# MAKE NATIVE MODULE GAP AUDIT
## She Said Sail — Stage 1 Blueprint Compatibility Review

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  
**Scope:** All 8 Stage 1 Make blueprints  
**Purpose:** Document every native vs. HTTP module decision, deprecated module replacements, and known gaps requiring manual credential binding.

---

## EXECUTIVE SUMMARY

Stage 1 uses a mixed module strategy: Make native modules where they are stable and well-maintained, HTTP direct API calls where native modules are deprecated, version-locked, or insufficiently flexible for production requirements.

**Critical Finding:** The Make native Stripe connector `stripe:ActionCreatePaymentLink` relies on Stripe API version 2019-02-11 and is incompatible with Stripe's current metadata requirements and webhook event schema. All Stage 1 Stripe operations use `http:ActionSendData` calling the Stripe REST API directly with `Stripe-Version: 2023-10-16` header.

---

## MODULE INVENTORY BY SCENARIO

### M-AUDIT-LOGGER

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `gateway:CustomWebHook` | Native | Receive inbound audit event | VERIFIED — Native, stable |
| `builtin:BasicFeeder` | Native | Construct audit record payload | VERIFIED — Native, stable |
| `airtable:ActionCreateRecord` | Native | Write record to Audit Log table | VERIFIED — Native v3, stable |
| `gateway:WebhookRespond` | Native | Return 200 with record ID | VERIFIED — Native, stable |

**Gaps:** None. All native. No Stripe dependency.

---

### M-SLACK-ALERTS

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `gateway:CustomWebHook` | Native | Receive inbound alert | VERIFIED — Native, stable |
| `builtin:BasicFeeder` | Native | Route by severity level | VERIFIED — Native, stable |
| `slack:CreateAMessage` | Native | Post to channel | VERIFIED — Native v4, stable |
| `slack:CreateAMessage` (DM) | Native | DM Will on SEV-1 | VERIFIED — Native v4, conditional |
| `gateway:WebhookRespond` | Native | Return 200 | VERIFIED — Native, stable |

**Gaps:** 
- `SLACK_WILL_DM_ID` must be manually bound at import. Get from Slack: right-click profile > Copy member ID.
- Slack channel IDs must be verified in workspace. Channel names used as labels but binding requires channel ID.

---

### M-BRAND-ROUTER

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `gateway:CustomWebHook` | Native | Receive brand detection request | VERIFIED — Native, stable |
| `builtin:BasicFeeder` (x2) | Native | Normalize inputs, compute brand | VERIFIED — Native, stable |
| `airtable:ActionCreateRecord` | Native | Write brand classification audit log | VERIFIED — Native v3, stable |
| `gateway:WebhookRespond` | Native | Return brand token to caller | VERIFIED — Native, stable |

**Gaps:** 
- ME brand signals are keyword-based. If Mare Executive source URL patterns change, the classification logic in module 3 must be updated.
- `AIRTABLE_BASE_ID_ME` must be confirmed — Mare Executive base may have a different ID than the primary ops base.

---

### M-LEAD-INTAKE

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `gateway:CustomWebHook` | Native | Receive Webflow form submission | VERIFIED — Native, stable |
| `http:ActionSendData` | HTTP | Call M-BRAND-ROUTER | DELIBERATE — calls internal Make webhook |
| `json:ParseJSON` | Native | Parse brand router response | VERIFIED — Native, stable |
| `airtable:SearchRecords` | Native | Deduplicate check | VERIFIED — Native v3, stable |
| `airtable:ActionCreateRecord` | Native | Create Request record | VERIFIED — Native v3, stable |
| `http:ActionSendData` (x2) | HTTP | Call M-SLACK-ALERTS + M-AUDIT-LOGGER | DELIBERATE — calls internal Make webhooks |
| `gateway:WebhookRespond` | Native | Return 200 | VERIFIED — Native, stable |

**Gaps:**
- Webflow form field names must match the field mapping in module 1. Webflow sends `name`, `email`, `phone`, `occasion`, `preferred_date`, `guest_count`, `budget`, `message`, `source`. Verify field names in Webflow Form Settings before activating.
- If Webflow sends different field names, update the mapper in module 5 (`airtable:ActionCreateRecord`).

---

### M-STRIPE-DEPOSIT

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `airtable:TriggerWatchRecords` | Native | Watch Bookings for AVAILABILITY_CONFIRMED | VERIFIED — Native v3, stable |
| `builtin:BasicFeeder` | Native | Compute deposit amount (50%), format fields | VERIFIED — Native, stable |
| `http:ActionSendData` | **HTTP — REPLACES DEPRECATED NATIVE** | Create Stripe Payment Link | SEE NOTE BELOW |
| `json:ParseJSON` | Native | Parse Stripe API response | VERIFIED — Native, stable |
| `airtable:ActionUpdateRecord` | Native | Update Booking to DEPOSIT_SENT | VERIFIED — Native v3, stable |
| `gmail:ActionSendEmail` | Native | Send deposit request email | VERIFIED — Native v1, stable |
| `http:ActionSendData` | HTTP | Call M-AUDIT-LOGGER | DELIBERATE — calls internal Make webhook |

**STRIPE MODULE NOTE — CRITICAL:**
> The Make native Stripe connector module `stripe:ActionCreatePaymentLink` has been **permanently removed** from all Stage 1 blueprints. It uses Stripe API version 2019-02-11 which does not support:
> - `metadata` fields on Payment Links (required for booking_id, airtable_record_id tracking)
> - `Idempotency-Key` header (required for duplicate prevention)
> - `after_completion.redirect.url` with query parameters
> - Current `checkout.session.completed` webhook schema
>
> **Replacement:** `http:ActionSendData` calling `https://api.stripe.com/v1/payment_links` with:
> - `Stripe-Version: 2023-10-16` header
> - `Authorization: Bearer {{STRIPE_SECRET_KEY}}`
> - `Idempotency-Key: deposit-{booking_id}-{YYYYMMDD}` header
> - Full metadata object with booking_id, airtable_record_id, payment_type, brand, environment

**Gaps:**
- `STRIPE_SECRET_KEY` — use a Stripe Restricted Key with permissions: `payment_links:write`. Never use the full secret key.
- Deposit calculation is `Package_Price * 0.5`. If deposit logic changes (e.g., different % for certain packages), update module 2.
- Gmail sender must be `hello@shesaidsail.com`. Verify Gmail OAuth connection grants send-as for this address.

---

### M-BOOKING-CREATION

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `gateway:CustomWebHook` | Native | Receive Stripe webhook | VERIFIED — Native, stable |
| `builtin:BasicFeeder` | Native | Extract fields from Stripe payload | VERIFIED — Native, stable |
| `builtin:BasicFeeder` (filter) | Native | Validate event type + metadata | VERIFIED — Native, conditional |
| `airtable:SearchRecords` | Native | Idempotency check in Audit Log | VERIFIED — Native v3, stable |
| `airtable:ActionUpdateRecord` | Native | Update Booking to DEPOSIT_PAID | VERIFIED — Native v3, stable |
| `http:ActionSendData` (x2) | HTTP | Call M-SLACK-ALERTS + M-AUDIT-LOGGER | DELIBERATE — calls internal Make webhooks |
| `gateway:WebhookRespond` | Native | Return 200 to Stripe | VERIFIED — Native, stable — **MUST return 200 immediately** |

**Gaps:**
- Stripe webhook signing secret validation is NOT natively implemented in Make's CustomWebHook module. After import, implement Stripe signature verification by adding a custom HTTP handler or validating the `Stripe-Signature` header in the first filter. Alternatively, use Stripe's IP allowlist to restrict who can call this endpoint.
- The Stripe event payload path `1.body.data.object.metadata.booking_id` assumes a `checkout.session.completed` event. If Stripe changes its event schema, update the field paths in module 2.

---

### M-CONCIERGE-ASSIGNMENT

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `airtable:TriggerWatchRecords` | Native | Watch Bookings for DEPOSIT_PAID | VERIFIED — Native v3, stable |
| `builtin:BasicFeeder` | Native | Extract and format booking fields | VERIFIED — Native, stable |
| `airtable:ActionUpdateRecord` | Native | Set Concierge_Assigned = true | VERIFIED — Native v3, stable |
| `slack:CreateAMessage` | Native | DM Luciana with booking details | VERIFIED — Native v4, stable |
| `slack:CreateAMessage` (conditional) | Native | DM Will for HV clients | VERIFIED — Native v4, conditional |
| `http:ActionSendData` | HTTP | Call M-AUDIT-LOGGER | DELIBERATE — calls internal Make webhook |

**Gaps:**
- `LUCIANA_AIRTABLE_RECORD_ID` — find by opening Airtable, going to the Concierge_Operators or Team_Members table, finding Luciana's record, and copying the record ID from the URL (format: `recXXXXXXXXXXXXXX`).
- `SLACK_LUCIANA_ID` — Luciana's Slack member ID. Get from Slack: open her profile > More > Copy member ID (format: `U0XXXXXXXXX`).
- The Bookings table must have a `Concierge_Assigned` checkbox field and an `Assigned_Concierge` linked record field pointing to the Concierge_Operators or Team_Members table.

---

### M-BOOKING-CONFIRMATION

| Module ID | Type | Purpose | Status |
|-----------|------|---------|--------|
| `airtable:TriggerWatchRecords` | Native | Watch Bookings for CONFIRMED | VERIFIED — Native v3, stable |
| `builtin:BasicFeeder` | Native | Extract and format booking fields | VERIFIED — Native, stable |
| `builtin:BasicFeeder` (filter) | Native | HV client routing gate | VERIFIED — Native, conditional |
| `gmail:ActionSendEmail` | Native | Send confirmation email | VERIFIED — Native v1, conditional (skipped for HV) |
| `slack:CreateAMessage` | Native | DM Luciana for HV Tier B review | VERIFIED — Native v4, conditional |
| `airtable:ActionUpdateRecord` | Native | Set Confirmation_Sent = true | VERIFIED — Native v3, stable |
| `http:ActionSendData` | HTTP | Call M-AUDIT-LOGGER | DELIBERATE — calls internal Make webhook |

**Gaps:**
- `Confirmation_Sent` checkbox field must exist on the Bookings table. If missing, add it before activating this scenario.
- `Marina_Address` field must be populated on the Booking or Yacht record before confirmation is sent. If empty, the email falls back to "Address will be provided 48 hours before charter."
- Balance due date is computed as `Charter_Date - 3 days`. If the balance window policy changes, update module 2's `balance_due_date` calculation.
- Email template is hardcoded HTML. Brand-specific templates (SSS vs ME) can be added via a conditional in module 4 based on the `brand` field.

---

## NATIVE MODULE COMPATIBILITY MATRIX

| Module | Make Version | Last Verified | Notes |
|--------|-------------|---------------|-------|
| `gateway:CustomWebHook` | v1 | 2026-05-16 | Stable. No version concerns. |
| `gateway:WebhookRespond` | v1 | 2026-05-16 | Stable. |
| `builtin:BasicFeeder` | v1 | 2026-05-16 | Stable. |
| `airtable:ActionCreateRecord` | v3 | 2026-05-16 | Use v3. v1/v2 deprecated. |
| `airtable:ActionUpdateRecord` | v3 | 2026-05-16 | Use v3. v1/v2 deprecated. |
| `airtable:SearchRecords` | v3 | 2026-05-16 | Use v3. |
| `airtable:TriggerWatchRecords` | v3 | 2026-05-16 | Use v3. |
| `slack:CreateAMessage` | v4 | 2026-05-16 | Use v4 for Block Kit support. v1-v3 lack blocks. |
| `gmail:ActionSendEmail` | v1 | 2026-05-16 | Stable. OAuth required. |
| `json:ParseJSON` | v1 | 2026-05-16 | Stable. |
| `http:ActionSendData` | v3 | 2026-05-16 | Use v3. |
| `stripe:ActionCreatePaymentLink` | **DEPRECATED** | — | **DO NOT USE.** API 2019-02-11. Missing metadata support. Removed from all blueprints. |

---

## DEPRECATED MODULE REPLACEMENT RECORD

| Deprecated Module | Reason Removed | Replacement | Scenario |
|------------------|---------------|-------------|---------|
| `stripe:ActionCreatePaymentLink` | Stripe API 2019-02-11 — missing metadata, idempotency key, current webhook schema | `http:ActionSendData` → `https://api.stripe.com/v1/payment_links` with `Stripe-Version: 2023-10-16` | M-STRIPE-DEPOSIT |

---

## KNOWN GAPS REQUIRING MANUAL ACTION

| Gap | Required Action | Scenario | Priority |
|-----|----------------|---------|---------|
| Stripe webhook signature verification | Add Stripe-Signature header validation in M-BOOKING-CREATION | M-BOOKING-CREATION | HIGH |
| Webflow form field name mapping | Verify field names match mapper in M-LEAD-INTAKE | M-LEAD-INTAKE | HIGH |
| `Confirmation_Sent` field missing | Add checkbox field to Bookings table before activating | M-BOOKING-CONFIRMATION | HIGH |
| `Concierge_Assigned` field missing | Add checkbox field to Bookings table before activating | M-CONCIERGE-ASSIGNMENT | HIGH |
| `Assigned_Concierge` linked record missing | Add linked record field to Bookings → Concierge_Operators | M-CONCIERGE-ASSIGNMENT | MEDIUM |
| ME base ID unconfirmed | Confirm `AIRTABLE_BASE_ID_ME` value | M-BRAND-ROUTER | MEDIUM |
| Stripe Restricted Key permissions | Create restricted key with payment_links:write only | M-STRIPE-DEPOSIT | HIGH |
| Gmail OAuth for hello@shesaidsail.com | Verify OAuth grants send-as this address | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION | HIGH |

---

*She Said Sail · Make Native Module Gap Audit · Stage 1*  
*CONFIDENTIAL — INTERNAL USE ONLY*
