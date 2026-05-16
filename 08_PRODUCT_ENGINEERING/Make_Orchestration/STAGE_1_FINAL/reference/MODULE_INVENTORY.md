# STAGE 1 MODULE INVENTORY
## She Said Sail — Complete Module Usage by Scenario

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Date:** May 2026  

---

## MODULE COUNT SUMMARY

| Scenario | Total Modules | Native | HTTP | Filters |
|---------|--------------|--------|------|---------|
| M-AUDIT-LOGGER | 4 | 4 | 0 | 0 |
| M-SLACK-ALERTS | 5 | 5 | 0 | 1 |
| M-BRAND-ROUTER | 5 | 5 | 0 | 0 |
| M-LEAD-INTAKE | 8 | 5 | 3 | 2 |
| M-STRIPE-DEPOSIT | 7 | 5 | 2 | 0 |
| M-BOOKING-CREATION | 8 | 4 | 3 | 3 |
| M-CONCIERGE-ASSIGNMENT | 6 | 5 | 1 | 2 |
| M-BOOKING-CONFIRMATION | 7 | 5 | 1 | 3 |
| **TOTAL** | **50** | **38** | **10** | **11** |

---

## M-AUDIT-LOGGER — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `gateway:CustomWebHook` | 1 | Receive inbound audit POST | No |
| 2 | `builtin:BasicFeeder` | 1 | Construct audit record with UUID | No |
| 3 | `airtable:ActionCreateRecord` | 3 | Write to Audit Log table | Airtable API |
| 4 | `gateway:WebhookRespond` | 1 | Return 200 with record ID | No |

---

## M-SLACK-ALERTS — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `gateway:CustomWebHook` | 1 | Receive inbound alert POST | No |
| 2 | `builtin:BasicFeeder` | 1 | Route by severity, set channel | No |
| 3 | `slack:CreateAMessage` | 4 | Post to appropriate Slack channel | Slack API |
| 4 | `slack:CreateAMessage` | 4 | DM Will (SEV-1 only, filtered) | Slack API |
| 5 | `gateway:WebhookRespond` | 1 | Return 200 | No |

---

## M-BRAND-ROUTER — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `gateway:CustomWebHook` | 1 | Receive brand detection request | No |
| 2 | `builtin:BasicFeeder` | 1 | Normalize input fields | No |
| 3 | `builtin:BasicFeeder` | 1 | Compute brand classification | No |
| 4 | `airtable:ActionCreateRecord` | 3 | Log classification to Audit Log | Airtable API |
| 5 | `gateway:WebhookRespond` | 1 | Return brand token | No |

---

## M-LEAD-INTAKE — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `gateway:CustomWebHook` | 1 | Receive Webflow form submission | No |
| 2 | `http:ActionSendData` | 3 | Call M-BRAND-ROUTER | Make (internal) |
| 3 | `json:ParseJSON` | 1 | Parse brand router response | No |
| 4 | `airtable:SearchRecords` | 3 | Deduplication — check recent submissions | Airtable API |
| 5 | `airtable:ActionCreateRecord` | 3 | Create Request record (if not duplicate) | Airtable API |
| 6 | `http:ActionSendData` | 3 | Call M-SLACK-ALERTS | Make (internal) |
| 7 | `http:ActionSendData` | 3 | Call M-AUDIT-LOGGER | Make (internal) |
| 8 | `gateway:WebhookRespond` | 1 | Return 200 | No |

---

## M-STRIPE-DEPOSIT — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `airtable:TriggerWatchRecords` | 3 | Watch Bookings for AVAILABILITY_CONFIRMED | Airtable API |
| 2 | `builtin:BasicFeeder` | 1 | Compute deposit amount, format fields | No |
| 3 | `http:ActionSendData` | 3 | Create Stripe Payment Link (API v2023-10-16) | Stripe API |
| 4 | `json:ParseJSON` | 1 | Parse Stripe API response | No |
| 5 | `airtable:ActionUpdateRecord` | 3 | Update Booking to DEPOSIT_SENT | Airtable API |
| 6 | `gmail:ActionSendEmail` | 1 | Send deposit request email to client | Gmail API |
| 7 | `http:ActionSendData` | 3 | Call M-AUDIT-LOGGER | Make (internal) |

---

## M-BOOKING-CREATION — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `gateway:CustomWebHook` | 1 | Receive Stripe checkout.session.completed | No |
| 2 | `builtin:BasicFeeder` | 1 | Extract fields from Stripe payload | No |
| 3 | `builtin:BasicFeeder` | 1 | Validate event type + metadata (filter gate) | No |
| 4 | `airtable:SearchRecords` | 3 | Idempotency — check Audit Log for event ID | Airtable API |
| 5 | `airtable:ActionUpdateRecord` | 3 | Update Booking to DEPOSIT_PAID | Airtable API |
| 6 | `http:ActionSendData` | 3 | Call M-SLACK-ALERTS | Make (internal) |
| 7 | `http:ActionSendData` | 3 | Call M-AUDIT-LOGGER | Make (internal) |
| 8 | `gateway:WebhookRespond` | 1 | Return 200 to Stripe | No |

---

## M-CONCIERGE-ASSIGNMENT — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `airtable:TriggerWatchRecords` | 3 | Watch Bookings for DEPOSIT_PAID | Airtable API |
| 2 | `builtin:BasicFeeder` | 1 | Extract and format booking fields | No |
| 3 | `airtable:ActionUpdateRecord` | 3 | Set Concierge_Assigned = true | Airtable API |
| 4 | `slack:CreateAMessage` | 4 | DM Luciana with booking details | Slack API |
| 5 | `slack:CreateAMessage` | 4 | DM Will for HV clients (conditional) | Slack API |
| 6 | `http:ActionSendData` | 3 | Call M-AUDIT-LOGGER | Make (internal) |

---

## M-BOOKING-CONFIRMATION — Module Inventory

| Module # | Module ID | Version | Purpose | External Call |
|----------|-----------|---------|---------|--------------|
| 1 | `airtable:TriggerWatchRecords` | 3 | Watch Bookings for CONFIRMED | Airtable API |
| 2 | `builtin:BasicFeeder` | 1 | Extract and format booking fields | No |
| 3 | `builtin:BasicFeeder` | 1 | HV client routing gate (filter) | No |
| 4 | `gmail:ActionSendEmail` | 1 | Send confirmation email (non-HV only) | Gmail API |
| 5 | `slack:CreateAMessage` | 4 | DM Luciana for HV Tier B review | Slack API |
| 6 | `airtable:ActionUpdateRecord` | 3 | Set Confirmation_Sent = true | Airtable API |
| 7 | `http:ActionSendData` | 3 | Call M-AUDIT-LOGGER | Make (internal) |

---

## EXTERNAL API CALLS SUMMARY

| External Service | Scenarios Using It | Authentication |
|-----------------|-------------------|---------------|
| Airtable API | All 8 | Personal Access Token |
| Slack API | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION | OAuth connection |
| Stripe API | M-STRIPE-DEPOSIT | Restricted API key |
| Gmail API | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION | OAuth connection |
| Internal Make webhooks | M-LEAD-INTAKE, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION | Bearer token |

---

*She Said Sail · Stage 1 Module Inventory*  
*CONFIDENTIAL — INTERNAL USE ONLY*
