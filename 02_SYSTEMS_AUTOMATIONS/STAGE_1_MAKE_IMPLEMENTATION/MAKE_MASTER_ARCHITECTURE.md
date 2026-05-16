# MAKE_MASTER_ARCHITECTURE
## She Said Sail + Mare Executive — Make.com Orchestration Layer
### Master Architecture Reference Document

**Status:** PRODUCTION IMPLEMENTATION REFERENCE
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail (SSS) · Mare Executive (ME) · Stage 1 Build · All Make Scenarios
**Classification:** Confidential — Internal Systems Documentation
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Systems Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

> **Architecture Authority Statement**
>
> This document is the definitive technical reference for the Make.com orchestration layer. It defines folder structure, scenario catalog, security model, error handling, idempotency strategy, audit requirements, and all inter-system connection standards. All Make scenario builds must conform to every standard defined here. No deviation is permitted without a Founder Decision record and a documented amendment to this file.

---

## TABLE OF CONTENTS

| Section | Title |
|---------|-------|
| 1 | Executive Summary |
| 2 | Make Folder Structure |
| 3 | Stage 1 Scenario Catalog |
| 4 | Environment Strategy |
| 5 | Webhook Security Model |
| 6 | Idempotency Strategy |
| 7 | Error Handling Hierarchy |
| 8 | Audit Logging Requirements |
| 9 | Duplicate Prevention Strategy |
| 10 | Circuit Breaker Pattern |
| 11 | Connection Catalog |
| 12 | System Data Flow Diagram |
| 13 | Rollback Capability Summary |
| 14 | Stage 1 → Stage 2 Boundary |

---

## SECTION 1 — EXECUTIVE SUMMARY

### 1.1 The Make Orchestration Layer

Make.com is the exclusive orchestration layer for She Said Sail and Mare Executive. It is Layer 4 in the seven-layer operating stack. Every cross-system write, every webhook event handler, every scheduled automation, and every multi-step workflow executes through a Make scenario. No external system writes directly to Airtable, Stripe, Gmail, Slack, or Quo SMS without passing through Make.

Make's role is execution — not intelligence, not storage, not decision-making. Intelligence is delegated to Claude (Layer 2). Storage lives in Airtable (Layer 3). Payments are authoritative in Stripe (Layer 6). Make is the connective tissue that moves data, triggers events, enforces business rules, and ensures every action is logged.

### 1.2 Two Brands, One Operational System

She Said Sail (SSS) and Mare Executive (ME) share a single Make infrastructure. The brand router (M-BRAND-ROUTER) is the mandatory first classification step for every inbound lead. Brand misrouting is a system failure — SSS content sent to an ME lead or vice versa violates brand positioning and triggers an immediate Slack alert.

All scenarios that produce client-facing output receive the brand classifier result before any content generation or message send. Brand is stamped on every Airtable record. Brand is logged in every Audit Log entry.

### 1.3 Stage 1 Scope

Stage 1 covers the complete inbound lead → booking confirmation pipeline with Stripe test-mode deposits and full audit logging. Eight scenarios are built in Stage 1. They form a complete, independently testable pipeline. Stage 2 adds charter execution, post-charter intelligence, and financial automation.

### 1.4 Non-Negotiable Make Rules

- Every scenario includes error handling with retry logic and failure notification. No bare scenario runs unguarded.
- Circular dependencies are prohibited. Make → Airtable trigger → Make re-trigger of the same scenario is a fatal architecture error.
- All scenarios operate in the tagged environment (Production / Sandbox). Sandbox scenarios never write to production Airtable bases.
- Every scenario is documented with its scenario ID, trigger type, and dependency map before it reaches production.
- Idempotency checks run before any record creation or message send. Duplicates are never acceptable.

---

## SECTION 2 — MAKE FOLDER STRUCTURE

### 2.1 Folder Hierarchy

All Make scenarios are organized into four top-level folders. Scenarios must live in the correct folder. Do not mix brands, environments, or lifecycle stages within a single folder.

```
Make Workspace: She Said Sail + Mare Executive
│
├── 📁 SSS — She Said Sail
│   ├── 📁 Stage 1 — Lead to Booking
│   ├── 📁 Stage 2 — Charter Execution
│   ├── 📁 Stage 3 — Intelligence + Reporting
│   └── 📁 Stage 4 — Growth + Outreach
│
├── 📁 ME — Mare Executive
│   ├── 📁 Stage 1 — Lead to Booking
│   ├── 📁 Stage 2 — Charter Execution
│   ├── 📁 Stage 3 — Intelligence + Reporting
│   └── 📁 Stage 4 — Growth + Outreach
│
├── 📁 SHARED — Cross-Brand Scenarios
│   ├── 📁 Core Infrastructure
│   │   ├── M-BRAND-ROUTER
│   │   ├── M-AUDIT-LOGGER
│   │   └── M-HEALTH-MONITOR
│   ├── 📁 Stripe Events
│   ├── 📁 Emergency Protocol
│   └── 📁 Scheduled Jobs
│
└── 📁 ARCHIVED
    ├── 📁 Deprecated v1
    └── 📁 Sandbox Snapshots
```

### 2.2 Naming Convention

All scenarios follow this naming pattern without exception:

```
[BRAND]-[DOMAIN]-[ACTION]-[VERSION]
```

| Token | Values | Example |
|-------|--------|---------|
| BRAND | SSS / ME / SHARED | SSS |
| DOMAIN | LEAD / BOOKING / STRIPE / AUDIT / SLACK / CONCIERGE / HEALTH | LEAD |
| ACTION | INTAKE / ROUTER / ALERT / CREATE / CONFIRM / LOGGER | INTAKE |
| VERSION | v1, v2, v3 | v1 |

**Stage 1 scenario names:**

| Scenario ID | Full Name | Folder |
|-------------|-----------|--------|
| M-BRAND-ROUTER | SHARED-LEAD-ROUTER-v1 | SHARED / Core Infrastructure |
| M-LEAD-INTAKE | SHARED-LEAD-INTAKE-v1 | SHARED / Core Infrastructure |
| M-SLACK-ALERTS | SHARED-SLACK-LEADALERT-v1 | SHARED / Core Infrastructure |
| M-CONCIERGE-ASSIGNMENT | SHARED-CONCIERGE-ASSIGN-v1 | SHARED / Core Infrastructure |
| M-STRIPE-DEPOSIT | SHARED-STRIPE-DEPOSIT-v1 | SHARED / Stripe Events |
| M-BOOKING-CREATION | SHARED-BOOKING-CREATE-v1 | SHARED / Core Infrastructure |
| M-BOOKING-CONFIRMATION | SHARED-BOOKING-CONFIRM-v1 | SHARED / Core Infrastructure |
| M-AUDIT-LOGGER | SHARED-AUDIT-LOGGER-v1 | SHARED / Core Infrastructure |

---

## SECTION 3 — STAGE 1 SCENARIO CATALOG

### 3.1 Scenario Overview Table

| # | Scenario | Purpose | Trigger Type | Autonomy Tier | Writes Audit Log |
|---|----------|---------|-------------|---------------|-----------------|
| 1 | M-BRAND-ROUTER | Classifies every inbound lead as SSS or ME | Webhook (inbound) | A | Yes |
| 2 | M-LEAD-INTAKE | Captures webhook payload; creates/deduplicates Airtable Request record | Webhook (inbound) | A | Yes |
| 3 | M-SLACK-ALERTS | Sends ops team Slack notification of new lead | Airtable record trigger | A | Yes |
| 4 | M-CONCIERGE-ASSIGNMENT | Assigns concierge operator to the request | Airtable record trigger | A | Yes |
| 5 | M-STRIPE-DEPOSIT | Generates Stripe test-mode deposit payment link | Airtable field change | A | Yes |
| 6 | M-BOOKING-CREATION | Creates/updates Booking record from qualified Request | Airtable field change | A | Yes |
| 7 | M-BOOKING-CONFIRMATION | Sends client confirmation (test-mode only in Stage 1) | Airtable field change | A (test-mode) | Yes |
| 8 | M-AUDIT-LOGGER | Writes immutable Audit Log record to Airtable | Called by all other scenarios | A | Self-logging |

### 3.2 Scenario Detail — M-BRAND-ROUTER

| Attribute | Value |
|-----------|-------|
| Purpose | Classify every inbound lead as SSS or ME based on source, form fields, and submission context |
| Trigger | Webhook POST from Webflow, Typeform, or manual API submission |
| Input | Raw webhook payload containing lead data |
| Classification Logic | Form ID → brand map; URL path detection; explicit brand field; fallback to Claude classification |
| Output | Enriched payload with `brand` field set to `SSS` or `ME` |
| Failure Mode | Unclassifiable leads default to `SSS`; Slack alert fires to `#sss-ops-alerts` for human review |
| Connection Dependencies | Webhook receiver; Claude API (fallback); Slack |
| Writes to Airtable | No — passes payload to M-LEAD-INTAKE |
| Writes Audit Log | Yes — via M-AUDIT-LOGGER call |
| Error Handling | Any classification failure generates Slack alert before fallback default is applied |

### 3.3 Scenario Detail — M-LEAD-INTAKE

| Attribute | Value |
|-----------|-------|
| Purpose | Capture webhook payload; deduplicate against existing Requests; create or update Airtable Request record |
| Trigger | Receives enriched payload from M-BRAND-ROUTER |
| Deduplication Key | `email + charter_date + brand` composite — checked against Requests table before write |
| Record Creation | Creates new Request record with all mapped fields; sets `Source_System = Make`, `Environment = Sandbox/Production`, `Status = NEW` |
| Idempotency | `Idempotency_Key = SHA256(email + charter_date + submission_timestamp)` stored in Request record |
| Connection Dependencies | Airtable (Requests table: tblTlSB9CO4dTGodg) |
| Writes to Airtable | Yes — Requests table |
| Writes Audit Log | Yes — via M-AUDIT-LOGGER call immediately after record creation |
| Error Handling | Airtable write failure: retry twice; then Slack alert; then Founder escalation |

### 3.4 Scenario Detail — M-SLACK-ALERTS

| Attribute | Value |
|-----------|-------|
| Purpose | Notify ops team of new inbound lead in real time |
| Trigger | Airtable: new record in Requests table with `Status = NEW` |
| Channel | `#sss-ops-alerts` for SSS leads; `#me-ops-alerts` (or `#sss-ops-alerts` as fallback) for ME leads |
| Message Contents | Lead name, email, charter date, group size, brand, Request ID, direct link to Airtable record |
| Connection Dependencies | Airtable (watch trigger); Slack |
| Writes to Airtable | Yes — updates `Last_AI_Action` timestamp on Request record |
| Writes Audit Log | Yes — event type: `SLACK_ALERT_SENT` |
| Error Handling | Slack send failure: retry twice; log failure to Automation Failures table; Slack DM to Will as fallback |

### 3.5 Scenario Detail — M-CONCIERGE-ASSIGNMENT

| Attribute | Value |
|-----------|-------|
| Purpose | Assign a concierge operator to the request based on availability and brand |
| Trigger | Airtable: Request record updated with `Status = NEW` and no `Assigned_Concierge` value |
| Assignment Logic | Reads Concierge_Operators table; filters by `Brand = SSS/ME`, `Status = AVAILABLE`; selects by round-robin index or lowest current load |
| Output | Updates Request record: `Assigned_Concierge` = selected concierge record ID; `Status = ASSIGNED` |
| Fallback | If no concierge available: alert `#sss-ops-alerts`; set `Status = UNASSIGNED_PENDING`; Slack DM to Will |
| Connection Dependencies | Airtable (Requests, Concierge_Operators tables) |
| Writes to Airtable | Yes — Requests table (`Assigned_Concierge`, `Status`) |
| Writes Audit Log | Yes — event type: `CONCIERGE_ASSIGNED` |
| Error Handling | Airtable read/write failure triggers Slack alert before any assignment attempt |

### 3.6 Scenario Detail — M-STRIPE-DEPOSIT

| Attribute | Value |
|-----------|-------|
| Purpose | Generate Stripe test-mode deposit payment link tied to the booking |
| Trigger | Airtable: Booking record with `Status = AVAILABILITY_CONFIRMED` and no `Stripe_Deposit_Link` value |
| Stripe Mode | TEST MODE in Stage 1. Production Stripe is never touched during Stage 1. |
| Payment Link | Stripe Payment Link created for deposit amount; description includes Booking ID and brand |
| Circuit Breaker | If Booking `Emergency_Flag = true`, scenario exits without creating link; logs skip to Audit Log |
| Output | Writes `Stripe_Deposit_Link` and `Stripe_Payment_Link_ID` to Booking record |
| Connection Dependencies | Airtable (Bookings: tbl72omPibBkn2hZL); Stripe API (test mode) |
| Writes to Airtable | Yes — Bookings table |
| Writes Audit Log | Yes — event type: `STRIPE_DEPOSIT_LINK_CREATED`; includes Stripe Payment Link ID |
| Error Handling | Stripe API failure: retry twice; then Slack alert; link creation never retried more than 3 times without human review |

### 3.7 Scenario Detail — M-BOOKING-CREATION

| Attribute | Value |
|-----------|-------|
| Purpose | Create or update Booking record in Airtable from a qualified, assigned Request |
| Trigger | Airtable: Request record with `Status = ASSIGNED` and `AI_Confidence_Score >= 70` (or Luciana manual promotion) |
| Deduplication | Checks Bookings table for existing record with matching `Request_ID` before creation |
| Record Population | Maps all relevant fields from Request to Booking; links Booking → Request → Client records |
| Status Set | `Booking.Status = AVAILABILITY_PENDING` on creation |
| Client Deduplication | Searches Clients table by email; creates new Client record only if no match found |
| Connection Dependencies | Airtable (Requests, Bookings, Clients tables) |
| Writes to Airtable | Yes — Bookings table; conditionally Clients table |
| Writes Audit Log | Yes — event type: `BOOKING_CREATED` with Booking ID and linked Request ID |
| Error Handling | All three Airtable writes (Request update, Booking create, Client create/link) wrapped in error handlers; partial write failure triggers full rollback attempt and Slack alert |

### 3.8 Scenario Detail — M-BOOKING-CONFIRMATION

| Attribute | Value |
|-----------|-------|
| Purpose | Send client confirmation of booking (test-mode only during Stage 1) |
| Trigger | Airtable: Booking record `Status = DEPOSIT_PAID` (Stripe webhook confirmation received) |
| Stage 1 Mode | TEST MODE ONLY. Email sends to `hello@shesaidsail.com` (internal) — never to real client email in Stage 1 |
| Content | Brand-appropriate confirmation email generated by Claude; includes Booking ID, charter date, deposit confirmation |
| Guards | `Emergency_Flag = false`; `Automations_Paused = false`; `Environment = Sandbox` (Stage 1 enforcement) |
| Connection Dependencies | Airtable (Bookings, Clients); Claude API; Gmail (internal test address only) |
| Writes to Airtable | Yes — Bookings table: `Status = CONFIRMED`; `Confirmation_Sent_At` timestamp |
| Writes Audit Log | Yes — event type: `BOOKING_CONFIRMATION_SENT`; includes recipient, brand, prompt version ID |
| Error Handling | Gmail send failure: retry twice; then Slack alert; `Status` NOT updated to CONFIRMED until email confirmed sent |

### 3.9 Scenario Detail — M-AUDIT-LOGGER

| Attribute | Value |
|-----------|-------|
| Purpose | Write immutable Audit Log record to Airtable for every Tier A autonomous action |
| Trigger | Called by all other Stage 1 scenarios via HTTP module (internal Make webhook) |
| Record Contents | Event type, scenario ID, brand, environment, timestamp, actor (Make/Claude/Human), record IDs affected, prompt version (if AI action), outcome (SUCCESS/FAILURE/SKIP) |
| Immutability | Audit Log records are append-only. No Make scenario has write access to modify existing Audit Log records. |
| Failure Mode | If Audit Log write fails: Slack DM to Will immediately; the originating action is still logged as attempted in Automation Failures table |
| Connection Dependencies | Airtable (Audit Log: tblrMpTfMk8q1eNHp) |
| Writes to Airtable | Yes — Audit Log table only |
| Writes Audit Log | Self — this is the logger |
| Error Handling | Audit Log write failure is treated as a SEV-2 event; Will is notified regardless of time |

---

## SECTION 4 — ENVIRONMENT STRATEGY

### 4.1 Environment Tiers

| Environment | Make Tag | Airtable Base | Stripe Mode | Client Comms | Purpose |
|-------------|----------|---------------|-------------|--------------|---------|
| Sandbox | `ENV=SANDBOX` | Dedicated sandbox base (separate from appdZ49WqgjRXxA1R) | Test mode | Never real clients | Integration testing, scenario validation |
| Production | `ENV=PRODUCTION` | appdZ49WqgjRXxA1R (main); apprDKQtV2GInThwE (financials) | Live mode (Stage 2+) | Real clients (Stage 2+) | Live operations |

### 4.2 Stage 1 Environment Rules

- ALL Stage 1 testing runs in Sandbox environment
- Stripe is ALWAYS test mode during Stage 1
- Gmail sends during Stage 1 are ALWAYS to internal test addresses (`hello@shesaidsail.com`, `hello@mareexecutive.com`)
- No real client data flows through any Stage 1 scenario during sandbox testing
- The `Environment` field is set by Make on every Airtable write — human override is not permitted
- Promotion from Sandbox to Production requires: Founder Decision record, full sandbox test suite passing, rollback procedure validated

### 4.3 Environment Variable Storage

All environment-specific values (API keys, base IDs, webhook URLs, Slack channel IDs) are stored in Make's built-in Data Store under the key prefix matching the environment. Direct credential embedding in scenario modules is prohibited.

```
Data Store Key Pattern:
  [ENV]_[SERVICE]_[KEY_NAME]

Examples:
  SANDBOX_AIRTABLE_BASE_ID
  SANDBOX_STRIPE_SECRET_KEY
  PRODUCTION_AIRTABLE_BASE_ID
  PRODUCTION_STRIPE_SECRET_KEY
  SHARED_SLACK_BOT_TOKEN
```

---

## SECTION 5 — WEBHOOK SECURITY MODEL

### 5.1 Security Layers (Applied in Order)

Every Make webhook endpoint implements the following security stack. Validation layers execute in order — failure at any layer terminates the request immediately with no processing.

```
Inbound Request
     │
     ▼
[1] IP Allowlist Check
     │ Fail → 403 Forbidden (no logging)
     ▼
[2] Authorization Bearer Token Validation
     │ Fail → 401 Unauthorized; log attempt to Audit Log
     ▼
[3] Timestamp Validation (reject if > 5 minutes old)
     │ Fail → 400 Bad Request; log replay attempt to Audit Log
     ▼
[4] Signing Secret Validation (HMAC-SHA256 for Stripe events)
     │ Fail → 401 Unauthorized; Slack alert to #sss-ops-alerts
     ▼
[5] Payload Schema Validation
     │ Fail → 400 Bad Request; log schema mismatch
     ▼
[6] Processing Begins
```

### 5.2 Bearer Token Configuration

| Webhook Type | Token Location | Rotation Cadence |
|--------------|---------------|-----------------|
| Inbound lead (Webflow/Typeform) | Make webhook URL + `Authorization: Bearer {TOKEN}` header | Quarterly or on personnel change |
| Internal Make-to-Make calls | Shared internal token stored in Data Store | Quarterly |
| Stripe webhook | Stripe signing secret (not Bearer) | On Stripe dashboard rotation |

### 5.3 Stripe Signing Secret Validation

Stripe webhooks to Make are validated using `Stripe-Signature` header HMAC verification. The webhook handler in M-STRIPE-DEPOSIT performs this validation before any processing:

```
Expected signature = HMAC_SHA256(
  key    = stripe_webhook_signing_secret,
  data   = timestamp + "." + raw_payload_body
)

If computed != received: reject with 401; alert #sss-ops-alerts
```

Raw payload body must be read before any JSON parsing — HMAC is over the raw bytes.

### 5.4 IP Allowlisting

Where provider-enforced IP ranges are available, Make webhook endpoints apply IP allowlisting as the outermost layer:

| Source | IP Allowlist Available | Ranges |
|--------|----------------------|--------|
| Stripe | Yes | Published in Stripe docs; updated automatically |
| Webflow | Yes | Published in Webflow docs |
| Typeform | Limited | Document current ranges; validate quarterly |
| Internal Make | N/A | Bearer token is primary control |

---

## SECTION 6 — IDEMPOTENCY STRATEGY

### 6.1 Why Idempotency Is Mandatory

Make scenarios can re-execute due to:
- Webhook retries from the sending platform
- Make's own retry logic on transient failures
- Manual scenario re-runs during debugging
- Network timeouts where the action completed but Make didn't receive the acknowledgment

Without idempotency controls, a single lead submission can create duplicate Request records, duplicate Booking records, and send duplicate confirmation emails to clients. In a luxury charter context, duplicate communications are a brand failure.

### 6.2 Idempotency Key Pattern

```
Idempotency_Key = SHA256(
  email
  + charter_date (ISO 8601)
  + brand (SSS or ME)
  + submission_source (webflow / typeform / api)
)
```

This key is computed at M-LEAD-INTAKE entry and stored in the Request record.

### 6.3 Idempotency Check Sequence

```
1. Compute Idempotency_Key from incoming payload
2. Search Requests table: filter by Idempotency_Key = computed value
3. If match found:
     a. Log duplicate attempt to Audit Log (event: DUPLICATE_REJECTED)
     b. Return existing Request ID to caller
     c. Do NOT create new record
     d. Do NOT send duplicate Slack alert
4. If no match found:
     a. Create Request record with Idempotency_Key stored
     b. Continue pipeline
```

### 6.4 Stripe Idempotency Keys

All Stripe API calls from Make include Stripe's native idempotency key header:

```
Idempotency-Key: stripe_{BookingID}_{action}_{timestamp_floor_to_hour}
```

Example: `stripe_BK-2026-0047_deposit_link_2026051614`

This prevents duplicate payment link creation if the Stripe module retries after a timeout.

### 6.5 Audit Log Deduplication

The Audit Log uses `Audit_Key = scenario_id + record_id + event_type + date` as a soft deduplication check. If an identical Audit_Key is found within the last 60 seconds, the second write is suppressed with a WARN log only. This prevents Audit Log flooding during retry storms.

---

## SECTION 7 — ERROR HANDLING HIERARCHY

### 7.1 Four-Level Error Handling Standard

Every production scenario implements all four error levels. Bypassing any level requires a documented exception in this file.

| Level | Trigger | Action | SLA |
|-------|---------|--------|-----|
| **L1 — Log** | Any module error | Write to Automation Failures table (tbl for AF); include error code, module name, scenario ID, timestamp, payload snapshot | Immediate |
| **L2 — Retry** | L1 log written; error is retriable (network, timeout, rate limit) | Retry after 2 minutes; then 5 minutes; maximum 3 total attempts | Within 7 minutes |
| **L3 — Slack Alert** | 3rd retry failed OR error is non-retriable (auth failure, schema error) | Post to `#sss-ops-alerts`: scenario name, error summary, affected record ID, direct Airtable link | Within 10 minutes |
| **L4 — Founder Escalation** | L3 fired AND no resolution within 30 minutes OR error involves financial data OR error involves client communication failure | Slack DM to Will; create Founder Decision record type `SEV-2`; scenario pauses until cleared | Within 30 minutes |

### 7.2 Error Classification

| Error Type | Level | Retriable | Auto-Resume |
|------------|-------|-----------|------------|
| HTTP 429 (rate limit) | L1 → L2 | Yes — wait 60s between retries | Yes |
| HTTP 5xx (server error) | L1 → L2 | Yes | Yes |
| HTTP 401 (auth failure) | L1 → L3 | No — human must rotate credentials | No |
| HTTP 400 (bad request) | L1 → L3 | No — payload or schema error | No |
| Airtable record not found | L1 → L2 → L3 | Retry twice; then human review | Conditional |
| Stripe API error (non-400) | L1 → L2 → L4 | Yes — financial context requires L4 | No |
| Claude API timeout | L1 → L2 | Yes | Yes |
| Claude content refusal | L1 → L3 | No — prompt issue; human review | No |
| Slack send failure | L1 → L2 → L4 | Yes — but Will DM as fallback if Slack down | No |
| Audit Log write failure | L4 immediately | No — treated as SEV-2 always | No |

### 7.3 Error Notification Template

All L3 Slack alerts use this format in `#sss-ops-alerts`:

```
:red_circle: *AUTOMATION FAILURE — ACTION REQUIRED*

*Scenario:* {scenario_name} ({scenario_id})
*Error:* {error_type} — {error_message}
*Record:* {record_id} | {airtable_link}
*Timestamp:* {iso_timestamp}
*Attempt:* {attempt_number} of 3
*Status:* Retrying / Paused / Awaiting Human

*Required Action:* {human_action_required}
```

---

## SECTION 8 — AUDIT LOGGING REQUIREMENTS

### 8.1 What Must Be Logged

Every Tier A autonomous action generates an Audit Log record (tblrMpTfMk8q1eNHp) before that action is considered complete. An action with no Audit Log entry is an incomplete action.

| Action Type | Must Log | Event Type Code |
|-------------|---------|----------------|
| Inbound lead received and classified | Yes | `LEAD_CLASSIFIED` |
| Request record created in Airtable | Yes | `REQUEST_CREATED` |
| Duplicate request rejected | Yes | `DUPLICATE_REJECTED` |
| Slack notification sent | Yes | `SLACK_ALERT_SENT` |
| Concierge assigned to request | Yes | `CONCIERGE_ASSIGNED` |
| Booking record created | Yes | `BOOKING_CREATED` |
| Stripe deposit link created | Yes | `STRIPE_DEPOSIT_LINK_CREATED` |
| Booking confirmation sent | Yes | `BOOKING_CONFIRMATION_SENT` |
| Error retry attempted | Yes | `ERROR_RETRY_ATTEMPTED` |
| Scenario paused by circuit breaker | Yes | `CIRCUIT_BREAKER_TRIGGERED` |
| Idempotency key match — duplicate suppressed | Yes | `DUPLICATE_REJECTED` |

### 8.2 Audit Log Record Required Fields

| Field | Type | Value |
|-------|------|-------|
| Audit_Key | Text | `{scenario_id}_{record_id}_{event_type}_{YYYYMMDD}` |
| Event_Type | Single Select | From approved event type list above |
| Scenario_ID | Text | Make scenario internal ID |
| Scenario_Name | Text | Human-readable name (e.g., M-LEAD-INTAKE) |
| Brand | Single Select | SSS / ME |
| Environment | Single Select | Production / Sandbox |
| Actor | Single Select | Make / Claude / Human |
| Affected_Record_ID | Text | Airtable record ID of the primary record affected |
| Affected_Table | Text | Table name (e.g., Requests, Bookings) |
| Prompt_Version_ID | Text | AIV-NNNN — required if Claude was invoked; blank otherwise |
| Outcome | Single Select | SUCCESS / FAILURE / SKIP |
| Error_Code | Text | HTTP status code or Make error code — blank on success |
| Timestamp | DateTime | UTC timestamp of action execution |
| Notes | Long Text | Any additional context; error message on failure |

### 8.3 Audit Log Immutability

- No scenario has `UPDATE` or `DELETE` access to the Audit Log table
- Audit Log records are created via a single dedicated Airtable API token scoped only to `CREATE` on the Audit Log table
- Corrections are made by creating a new `CORRECTION` event record that references the original record — the original is never modified
- Audit Log export to CSV runs daily at 2am as part of BACKUP-001 (Stage 2)

---

## SECTION 9 — DUPLICATE PREVENTION STRATEGY

### 9.1 Three-Layer Duplicate Defense

Duplicate prevention operates at three independent layers. All three must be in place before any scenario is promoted to production.

**Layer 1 — Idempotency Key (entry prevention)**
Computed at M-LEAD-INTAKE. Checks Requests table before creating any record. If key exists, returns existing record ID and aborts creation. This is the primary defense.

**Layer 2 — Airtable Formula Field (detection)**
The Requests table contains a `Is_Duplicate` formula field that checks for records sharing the same email + charter_date combination within the same brand. When `Is_Duplicate = TRUE`, the record displays a warning flag visible in all Airtable views. This catches any duplicates that bypass Layer 1 (e.g., manual entries).

**Layer 3 — Audit Log Review (reporting)**
Weekly review of `DUPLICATE_REJECTED` events in the Audit Log. High frequency of duplicates from a specific source indicates a misconfigured sending system (e.g., Webflow form double-submitting). Threshold: > 5 duplicates per week from same source triggers investigation.

### 9.2 Client Record Deduplication

Client deduplication is separate from Request deduplication.

```
At M-BOOKING-CREATION:
1. Search Clients table by email (exact match)
2. If found: link existing Client record to new Booking; do NOT create new record
3. If not found: create new Client record; link to Booking
4. Log outcome to Audit Log: CLIENT_LINKED or CLIENT_CREATED
```

---

## SECTION 10 — CIRCUIT BREAKER PATTERN

### 10.1 Stripe Circuit Breaker

The Stripe circuit breaker prevents runaway payment link creation and protects against Stripe API abuse during error conditions.

**Circuit Breaker State Machine:**

```
State: CLOSED (normal operation)
  │
  │ [3 consecutive Stripe errors within 10 minutes]
  ▼
State: OPEN (Stripe calls suspended)
  │ → Log CIRCUIT_BREAKER_TRIGGERED to Audit Log
  │ → Alert #sss-ops-alerts with error details
  │ → All M-STRIPE-DEPOSIT executions skip Stripe call
  │ → Return CIRCUIT_OPEN to caller; set Booking flag
  │
  │ [Manual reset by Will or Luciana after investigation]
  ▼
State: HALF-OPEN (test mode)
  │ → Allow one Stripe call through
  │ → If success: return to CLOSED
  │ → If failure: return to OPEN
```

**Circuit Breaker State Storage:** Make Data Store key `STRIPE_CIRCUIT_STATE` with value `CLOSED / OPEN / HALF_OPEN` and `STRIPE_ERROR_COUNT` counter.

### 10.2 Emergency Flag Circuit Breaker

When any Booking record has `Emergency_Flag = true`, ALL automations for that booking stop immediately. M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION, and M-BOOKING-CREATION all check Emergency_Flag as their first module after data retrieval.

```
Module 1: Get Booking Record
Module 2: Check Emergency_Flag
  │ If true: log CIRCUIT_BREAKER_TRIGGERED; alert Will via DM; exit scenario
  │ If false: continue
Module 3: Main scenario logic
```

### 10.3 Automations_Paused Field

The `Automations_Paused` field on Booking records is a secondary circuit breaker that Luciana can toggle without escalating to Will. When `Automations_Paused = true`:
- M-BOOKING-CONFIRMATION skips the email send
- M-SLACK-ALERTS still fires (ops always sees the record)
- Audit Log records the skip with reason `AUTOMATIONS_PAUSED`

---

## SECTION 11 — CONNECTION CATALOG

### 11.1 Production Connection Registry

All Make connections are named exactly as listed here. Deviation in naming breaks scenario documentation integrity.

| Connection Name | Service | Auth Type | Scope | Environment |
|----------------|---------|-----------|-------|-------------|
| `SSS-Airtable-Production` | Airtable | Personal Access Token | Requests, Bookings, Clients, Audit Log, Founder Decisions | Production |
| `SSS-Airtable-Sandbox` | Airtable | Personal Access Token | Sandbox base only | Sandbox |
| `SSS-Stripe-Test` | Stripe | Secret Key (test) | Payment Links, Customers (test mode) | Stage 1 Sandbox |
| `SSS-Stripe-Production` | Stripe | Secret Key (live) | Payment Links, Customers, Webhooks | Stage 2+ Production |
| `SSS-Slack-Bot` | Slack | OAuth Bot Token | `#sss-ops-alerts`, `#sss-emergency-ops`, Will DM | Shared |
| `SSS-Gmail-Hello` | Gmail | OAuth | hello@shesaidsail.com | Production |
| `ME-Gmail-Hello` | Gmail | OAuth | hello@mareexecutive.com | Production |
| `SSS-QuoSMS` | Quo SMS | API Key | Outbound SMS to clients | Stage 2+ |
| `SSS-Claude-API` | Anthropic | Bearer Token | Claude API — all models | Shared |

### 11.2 Connection Security Rules

- All API keys and secrets are stored exclusively in Make's built-in credential vault
- No credential appears in any scenario module configuration as a plain text value
- Every connection is tagged with its environment so sandbox scenarios cannot accidentally use production credentials
- Connection tokens are rotated quarterly at minimum; rotation is a Founder Decision action with Audit Log entry
- Any connection failure generates an L3 Slack alert regardless of scenario context

### 11.3 Quo SMS Configuration

Quo SMS is activated in Stage 2 for client-facing SMS communication. In Stage 1, Quo SMS is connected but all sends are suppressed. The connection is established and tested in Stage 1 (sending to a test phone number only) to ensure it is ready for Stage 2 promotion.

---

## SECTION 12 — SYSTEM DATA FLOW DIAGRAM

### 12.1 Stage 1 Full Pipeline — Text-Based Data Flow

```
INBOUND LEAD SOURCES
─────────────────────
  Webflow Form
  Typeform
  Manual API POST
        │
        │  HTTP POST (JSON payload)
        ▼
┌─────────────────────────────────────────────────────────┐
│  MAKE WEBHOOK ENDPOINT                                  │
│  Security: IP allowlist → Bearer token → Timestamp      │
│  → Schema validation                                    │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-BRAND-ROUTER                                         │
│  Input: raw payload                                     │
│  Logic: form ID map → URL path → explicit field         │
│         → Claude fallback classification                │
│  Output: payload + brand = SSS | ME                     │
│  Audit: LEAD_CLASSIFIED                                 │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-LEAD-INTAKE                                          │
│  Input: enriched payload (brand confirmed)              │
│  Step 1: Compute Idempotency_Key                        │
│  Step 2: Search Requests table → duplicate check        │
│  Step 3 (if new): Create Request record in Airtable     │
│          Fields: all mapped lead data                    │
│          Status = NEW; Environment = SANDBOX/PRODUCTION │
│  Step 4: Write Idempotency_Key to record                │
│  Audit: REQUEST_CREATED or DUPLICATE_REJECTED           │
└─────────────────────────────────────────────────────────┘
        │
        │  Airtable: Status = NEW (watch trigger)
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-SLACK-ALERTS (parallel with M-CONCIERGE-ASSIGNMENT)  │
│  Input: Request record from Airtable watch              │
│  Action: Post to #sss-ops-alerts (SSS) or #me-ops       │
│  Message: Lead name, email, date, group size, link      │
│  Audit: SLACK_ALERT_SENT                                │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-CONCIERGE-ASSIGNMENT                                 │
│  Input: Request record (Status = NEW)                   │
│  Step 1: Read Concierge_Operators table                 │
│  Step 2: Filter by brand + status = AVAILABLE           │
│  Step 3: Select by round-robin / lowest load            │
│  Step 4: Update Request → Assigned_Concierge; Status = ASSIGNED │
│  Audit: CONCIERGE_ASSIGNED                              │
└─────────────────────────────────────────────────────────┘
        │
        │  Human/Luciana: confirms availability
        │  Request.Status → AVAILABILITY_CONFIRMED
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-BOOKING-CREATION                                     │
│  Input: Request record (Status = AVAILABILITY_CONFIRMED)│
│  Step 1: Dedup check on Bookings table                  │
│  Step 2: Client dedup on Clients table                  │
│  Step 3: Create Booking record; link Request + Client   │
│  Step 4: Update Request Status = BOOKING_CREATED        │
│  Booking.Status = AVAILABILITY_PENDING                  │
│  Audit: BOOKING_CREATED                                 │
└─────────────────────────────────────────────────────────┘
        │
        │  Luciana confirms availability
        │  Booking.Status → AVAILABILITY_CONFIRMED
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-STRIPE-DEPOSIT                                       │
│  Input: Booking record (Status = AVAILABILITY_CONFIRMED)│
│  Step 1: Circuit breaker check (STRIPE_CIRCUIT_STATE)   │
│  Step 2: Emergency_Flag check                           │
│  Step 3: Create Stripe Payment Link (TEST MODE)         │
│  Step 4: Write Stripe_Deposit_Link to Booking           │
│  Booking.Status = DEPOSIT_SENT                          │
│  Audit: STRIPE_DEPOSIT_LINK_CREATED                     │
└─────────────────────────────────────────────────────────┘
        │
        │  Stripe webhook: payment.complete (test event)
        │  Booking.Status → DEPOSIT_PAID
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-BOOKING-CONFIRMATION                                 │
│  Input: Booking record (Status = DEPOSIT_PAID)          │
│  Step 1: Emergency_Flag + Automations_Paused check      │
│  Step 2: Assemble Claude context (brand, client, booking)│
│  Step 3: Generate confirmation email via Claude API     │
│  Step 4: Send via Gmail (TEST → internal address only)  │
│  Step 5: Update Booking.Status = CONFIRMED              │
│  Step 6: Write Confirmation_Sent_At timestamp           │
│  Audit: BOOKING_CONFIRMATION_SENT                       │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  M-AUDIT-LOGGER (called by every scenario above)        │
│  Input: structured event payload from calling scenario  │
│  Action: Create Audit Log record in Airtable            │
│  Fields: all required Audit Log fields (see Section 8)  │
│  On failure: SEV-2 immediate; Will DM                   │
└─────────────────────────────────────────────────────────┘

EXTERNAL SYSTEMS WRITTEN TO:
  Airtable: Requests, Bookings, Clients, Audit Log
  Slack: #sss-ops-alerts, #me-ops-alerts, Will DM
  Stripe: Payment Links API (test mode)
  Gmail: Internal test addresses only (Stage 1)
  Claude API: Brand routing + confirmation content generation
```

---

## SECTION 13 — ROLLBACK CAPABILITY SUMMARY

### 13.1 Rollback Principles

Every production scenario has a documented rollback procedure before it goes live. Rollback is not optional. Rollback procedures are tested in Sandbox before production promotion.

| Scenario | Rollback Action | Time to Execute | Who Can Execute |
|----------|----------------|-----------------|----------------|
| M-BRAND-ROUTER | Disable scenario; revert to manual brand tagging | < 5 minutes | Will or Luciana |
| M-LEAD-INTAKE | Disable scenario; manual Airtable entry; no data loss risk | < 5 minutes | Will or Luciana |
| M-SLACK-ALERTS | Disable scenario; Luciana monitors Airtable directly | < 2 minutes | Will or Luciana |
| M-CONCIERGE-ASSIGNMENT | Disable scenario; Luciana assigns manually | < 2 minutes | Will or Luciana |
| M-STRIPE-DEPOSIT | Disable scenario; archive created Payment Links in Stripe; Luciana sends manually | < 10 minutes | Will only |
| M-BOOKING-CREATION | Disable scenario; manually correct any partial Booking records; Audit Log documents all corrections | < 15 minutes | Will only |
| M-BOOKING-CONFIRMATION | Disable scenario immediately; check Gmail sent items; contact affected client if real email sent in error | < 5 minutes + client follow-up | Will only |
| M-AUDIT-LOGGER | Cannot be rolled back — Audit Log is append-only. Correction records written. | N/A | Will only |

### 13.2 Prompt Version Rollback

If a Claude-generated output is found to be incorrect, off-brand, or outside authority scope:

1. Disable M-BOOKING-CONFIRMATION immediately
2. Identify current Prompt_Version_ID from Audit Log
3. Will deploys prior prompt version via ROLLBACK-PROMPT-001 (Stage 2 scenario; manual equivalent in Stage 1)
4. Audit Log records PROMPT_VERSION_ROLLBACK event
5. Scenario re-enabled after prompt version confirmed

Target rollback time: 15 minutes from identification to re-enable.

### 13.3 Data Correction Protocol

No Airtable record is deleted to correct a pipeline error. Corrections follow this protocol:

1. Flag the incorrect record: set `Status = VOID` or `Status = SUPERSEDED`
2. Create a corrected replacement record if needed
3. Write a Correction Audit Log record referencing both the original and replacement record IDs
4. Notify Will via Slack DM
5. Document in Founder Decisions table if financial data was affected

---

## SECTION 14 — STAGE 1 → STAGE 2 BOUNDARY

### 14.1 What IS Built in Stage 1

| Capability | Built in Stage 1 |
|------------|-----------------|
| Brand router (SSS vs ME classification) | Yes |
| Lead capture and Airtable Request creation | Yes |
| Deduplication at Request level | Yes |
| Slack ops alerts for new leads | Yes |
| Concierge assignment (round-robin) | Yes |
| Booking record creation from qualified Request | Yes |
| Stripe deposit link generation (test mode only) | Yes |
| Booking confirmation email (internal test address only) | Yes |
| Immutable Audit Log for all Tier A actions | Yes |
| Error handling — all 4 levels | Yes |
| Idempotency key pattern | Yes |
| Circuit breaker for Stripe | Yes |
| Emergency_Flag and Automations_Paused guards | Yes |

### 14.2 What is NOT Built in Stage 1

| Capability | Stage |
|------------|-------|
| Real client email sends (live Gmail) | Stage 2 |
| Quo SMS client text messages | Stage 2 |
| Stripe live mode (real payment processing) | Stage 2 |
| Charter execution automations (72hr reminder, 24hr, 12hr) | Stage 2 |
| Post-charter D1, D7, D30 automations | Stage 2 |
| Financial reconciliation (Stripe → Airtable P&L) | Stage 2 |
| Weekly financial digest | Stage 2 |
| Thursday operational intelligence digest | Stage 2 |
| Partner outreach automation | Stage 3 |
| Creative intelligence automation | Stage 3 |
| Multi-city scaling logic | Stage 3 |
| Vapi / voice agent integration | Stage 4+ |
| Daily Airtable backup automation | Stage 2 |
| 15-minute health monitoring automation | Stage 2 |

### 14.3 Stage 1 → Stage 2 Promotion Gate

Stage 2 does not begin until ALL of the following are true:

- [ ] All 8 Stage 1 scenarios pass full sandbox test suite
- [ ] Audit Log contains records for every event type in the catalog
- [ ] No open L3 or L4 errors from Stage 1 scenarios
- [ ] Stripe test-mode deposit flow is validated end-to-end
- [ ] Duplicate prevention validated (test submitted same lead twice — second rejected)
- [ ] Emergency_Flag circuit breaker validated (flag set — all relevant scenarios exit)
- [ ] Rollback procedures tested for all 7 rollback-capable scenarios
- [ ] Founder Decision record created: STAGE_1_COMPLETE
- [ ] Will has reviewed and approved promotion

---

*Document Authority: This file is the master Make architecture reference. All scenario builds, security implementations, and error handling decisions must conform to these standards. Amendment requires Founder Decision record and version increment.*

*Last Updated: May 2026 | Version: 1.0 | Owner: Will (Founder)*
