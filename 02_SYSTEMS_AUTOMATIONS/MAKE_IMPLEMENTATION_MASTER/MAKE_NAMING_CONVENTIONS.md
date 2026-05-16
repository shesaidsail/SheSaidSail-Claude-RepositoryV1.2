# MAKE_NAMING_CONVENTIONS

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Canonical naming conventions for all Make scenarios, routers, folders, variables, webhooks, and logs. Consistency prevents confusion and enables offshore maintainability.
**Classification:** Confidential — Internal Use Only

---

## WHY NAMING CONVENTIONS MATTER

When a Make scenario is built by one person and maintained by another — or when debugging at 11pm during a charter weekend — naming conventions are the difference between a 2-minute fix and a 2-hour hunt. Every element of every scenario follows these conventions without exception.

---

## SECTION 1 — SCENARIO NAMING

### 1.1 Scenario ID Format

```
M-[FUNCTION]-[SPECIFICITY]
```

| Component | Convention |
|-----------|-----------|
| `M-` | Mandatory prefix — identifies as a Make scenario |
| `[FUNCTION]` | All caps — single descriptive function word or compound |
| `[SPECIFICITY]` | Optional — adds context when multiple scenarios share a function |

**Examples:**
```
M-LEAD-INTAKE
M-BRAND-ROUTER
M-BOOKING-CREATION
M-STRIPE-DEPOSIT
M-BOOKING-CONFIRMATION
M-BASIC-LIFECYCLE
M-REVIEW-REQUEST
M-YACHT-AVAILABILITY-LOCK
M-DOUBLE-BOOKING-CHECK
M-FAILED-PAYMENT-HANDLER
M-CHARTER-BRIEF
M-ESCALATION-ROUTER
M-AUTOMATION-HEALTH
M-AI-LEAD-SCORING
M-FOUNDER-DIGEST
M-CREATIVE-INTELLIGENCE
M-CREATIVE-FATIGUE
M-SYNTER-SYNC
```

### 1.2 Scenario Display Name in Make

Use the full descriptive name in the Make scenario Name field — not the ID:

| Scenario ID | Make Display Name |
|------------|-------------------|
| M-LEAD-INTAKE | SSS + ME — Lead Intake Handler |
| M-BRAND-ROUTER | SSS + ME — Brand Classification Router |
| M-BOOKING-CREATION | SSS + ME — Booking Creation Handler |
| M-STRIPE-DEPOSIT | SSS + ME — Stripe Deposit Handler |
| M-BOOKING-CONFIRMATION | SSS + ME — Booking Confirmation Sender |
| M-CONCIERGE-ASSIGNMENT | SSS + ME — Concierge Assignment Notifier |
| M-BASIC-LIFECYCLE | SSS + ME — Charter Lifecycle Scheduler |
| M-REVIEW-REQUEST | SSS + ME — Post-Charter Review Request |
| M-YACHT-AVAILABILITY-LOCK | SSS + ME — Yacht Availability Lock |
| M-DOUBLE-BOOKING-CHECK | SSS + ME — Double Booking Prevention |
| M-FAILED-PAYMENT-HANDLER | SSS + ME — Failed Payment Handler |
| M-VENDOR-NOTIFICATIONS | SSS + ME — Vendor Notification Handler |
| M-CHARTER-BRIEF | SSS + ME — Charter Brief Generator |
| M-ESCALATION-ROUTER | SSS + ME — Escalation Router |
| M-REFERRAL-ENGINE | SSS + ME — Referral Activation Engine |
| M-REBOOKING-ENGINE | SSS + ME — Rebooking Offer Engine |
| M-AUTOMATION-HEALTH | SSS + ME — Automation Health Monitor |
| M-AI-LEAD-SCORING | SSS + ME — AI Lead Scoring Engine |
| M-LTV-ENGINE | SSS + ME — Client LTV Tracker |
| M-REVENUE-HEALTH | SSS + ME — Revenue Health Monitor |
| M-PRICING-INTELLIGENCE | SSS + ME — Pricing Intelligence Report |
| M-FOUNDER-DIGEST | SSS + ME — Founder Thursday Digest |
| M-CITY-HEALTH | SSS + ME — City Health Scorer |
| M-PARTNER-SCORING | SSS + ME — Partner Quality Scorer |
| M-CONCIERGE-INTELLIGENCE | SSS + ME — Concierge Performance Report |
| M-CREATIVE-INTELLIGENCE | SSS + ME — Creative Performance Analyzer |
| M-CREATIVE-FATIGUE | SSS + ME — Creative Fatigue Detector |
| M-SYNTER-SYNC | SSS + ME — Financial Sync to Financials Base |
| M-CAMPAIGN-RECOMMENDER | SSS + ME — AI Campaign Recommender |
| M-SOP-INTELLIGENCE | SSS + ME — SOP Intelligence Analyzer |
| M-CITY-LAUNCH | SSS + ME — City Launch Automation |
| M-EXECUTIVE-DASHBOARD | SSS + ME — Executive Dashboard Feeder |
| M-OWNER-HUB | SSS + ME — Owner Hub Feed Generator |
| M-OPS-HUB | SSS + ME — Ops Hub Feed Generator |

### 1.3 Scenario Description Field

Every scenario's Description field in Make must contain:

```
[SCENARIO_ID] | Stage [N] | Trigger: [trigger type] | Autonomy: Tier [A/B/C]
Purpose: [one sentence]
Last updated: [date] by [initials]
```

Example:
```
M-LEAD-INTAKE | Stage 1 | Trigger: Webflow Webhook | Autonomy: Tier A
Purpose: Captures inbound leads from website form and creates Airtable Request + Client records.
Last updated: 2026-05-15 by WM
```

---

## SECTION 2 — MODULE NAMING WITHIN SCENARIOS

Every module inside a Make scenario has a label. Labels follow this pattern:

```
[step_number]. [VERB] — [OBJECT]
```

Examples:
```
1. VALIDATE — Stripe signature
2. GET — Booking record from Airtable
3. CHECK — Emergency_Flag + Automations_Paused
4. BRANCH — HV_Client routing
5. SEND — Confirmation email via Gmail
6. UPDATE — Bookings.Confirmation_Sent_At
7. LOG — Audit_Log entry
8. RESPOND — 200 OK to Stripe
```

**Standard verbs for module labels:**
- `VALIDATE` — authentication, signature verification, timestamp check
- `GET` — read a record from Airtable or any source
- `SEARCH` — query records with filters
- `CHECK` — evaluate a condition (boolean check)
- `BRANCH` — router or conditional path
- `CALCULATE` — mathematical or formula operation
- `SEND` — outbound message (email, SMS, Slack)
- `CREATE` — create a new record
- `UPDATE` — update an existing record
- `CALL` — external API call (Stripe, Claude, Quo)
- `LOG` — write to Audit_Log
- `RESPOND` — webhook response
- `PAGINATE` — loop / iteration
- `AGGREGATE` — sum, count, average operations
- `EXIT` — intentional early exit with logging

---

## SECTION 3 — VARIABLE NAMING

### 3.1 Make Variables (Set Variable modules)

All custom variables in Make use snake_case:

| Variable Purpose | Name Convention | Example |
|-----------------|----------------|---------|
| Derived calculations | `[noun]_[descriptor]` | `deposit_amount`, `days_until_charter`, `idempotency_key` |
| Record IDs | `[table]_record_id` | `booking_record_id`, `client_record_id` |
| Flags | `is_[condition]` or `has_[attribute]` | `is_emergency`, `has_hv_flag`, `is_eligible` |
| Timestamps | `[event]_at` | `sent_at`, `locked_at`, `checked_at` |
| Counts | `[noun]_count` | `failure_count`, `booking_count` |
| Amounts | `[noun]_amount` | `deposit_amount`, `balance_amount` |
| Scores | `[noun]_score` | `lead_score`, `health_score` |

### 3.2 AI Prompt Version Variable Names (Make_Variable_Name field in Airtable)

These are the exact string values used in Make to look up the correct prompt from AI_Prompt_Versions table:

| Scenario | Make_Variable_Name Value |
|---------|------------------------|
| M-CHARTER-BRIEF | `CHARTER_BRIEF_SYSTEM` |
| M-AI-LEAD-SCORING | `LEAD_SCORING_SYSTEM` |
| M-FOUNDER-DIGEST | `FOUNDER_DIGEST_SYSTEM` |
| M-PRICING-INTELLIGENCE | `PRICING_INTELLIGENCE_SYSTEM` |
| M-CONCIERGE-INTELLIGENCE | `CONCIERGE_INTELLIGENCE_SYSTEM` |
| M-CREATIVE-INTELLIGENCE | `CREATIVE_INTELLIGENCE_SYSTEM` |
| M-CAMPAIGN-RECOMMENDER | `CAMPAIGN_RECOMMENDER_SYSTEM` |
| M-SOP-INTELLIGENCE | `SOP_INTELLIGENCE_SYSTEM` |

---

## SECTION 4 — FOLDER STRUCTURE IN MAKE

```
She Said Sail + Mare Executive/
├── STAGE_1_CORE/
├── STAGE_2_OPERATIONS/
├── STAGE_3_INTELLIGENCE/
├── STAGE_4_SCALE/
└── SHARED_UTILITIES/
```

Rules:
- Every scenario lives in exactly one folder
- No scenario lives in the root — always in a stage folder
- SHARED_UTILITIES contains reusable sub-scenarios and utilities only
- Never create a folder named "Test" or "Draft" in production Make workspace — use the SSS Sandbox Make organization for that

---

## SECTION 5 — WEBHOOK NAMING

### 5.1 Make Webhook URL Labels

When a webhook is created in Make, its label follows this pattern:

```
[SOURCE]-[SCENARIO_ID]-[ENVIRONMENT]
```

Examples:
```
webflow-M-LEAD-INTAKE-production
stripe-M-STRIPE-DEPOSIT-production
airtable-M-BOOKING-CREATION-production
stripe-M-FAILED-PAYMENT-HANDLER-production
```

### 5.2 Webhook Security Headers

Every inbound webhook validates:

```
Header: Authorization
Value: Bearer {{MAKE_WEBHOOK_SECRET_[SCENARIO_ID]}}
```

Webhook secret names in Make Credentials Vault follow:
```
MAKE_WEBHOOK_SECRET_M_LEAD_INTAKE
MAKE_WEBHOOK_SECRET_M_STRIPE_DEPOSIT
MAKE_WEBHOOK_SECRET_M_FAILED_PAYMENT_HANDLER
```

---

## SECTION 6 — AIRTABLE VIEW NAMING (Make-specific views)

Airtable views used exclusively by Make for webhook triggers or record searches are named:

```
MAKE — [Scenario ID] — [Filter Description]
```

Examples:
```
MAKE — M-BASIC-LIFECYCLE — Active Bookings (Production)
MAKE — M-REVIEW-REQUEST — D7 Eligible (Production)
MAKE — M-REFERRAL-ENGINE — D30 Eligible (Production)
MAKE — M-REBOOKING-ENGINE — D60 Eligible (Production)
MAKE — M-REVENUE-HEALTH — This Month Bookings
```

These views are never used by humans for operational work — they are exclusively Make feed views.

---

## SECTION 7 — SLACK CHANNEL NAMING

| Channel | Purpose | Naming Standard |
|---------|---------|----------------|
| `#sss-ops-leads` | SSS inbound lead alerts | Current — keep |
| `#me-ops-leads` | ME inbound lead alerts | Create if not exists |
| `#sss-ops-bookings` | SSS booking lifecycle events | Current — keep |
| `#me-ops-bookings` | ME booking lifecycle events | Create if not exists |
| `#sss-ops-alerts` | System health, SEV alerts, automation errors | Current — keep |
| `#sss-emergency-ops` | L4 emergency coordination only | Current — keep |

No new channels are created without Will approval. Make scenarios post to existing channels only.

---

## SECTION 8 — EMAIL TEMPLATE NAMING

Email templates (stored in Gmail drafts or template system) follow this naming:

```
[BRAND]_[TRIGGER_EVENT]_[AUDIENCE]
```

Examples:
```
SSS_DEPOSIT_REQUEST_CLIENT
SSS_DEPOSIT_CONFIRMED_CLIENT
ME_DEPOSIT_CONFIRMED_CLIENT
SSS_BOOKING_CONFIRMED_CLIENT
SSS_T72_BALANCE_REMINDER_CLIENT
SSS_T48_LOGISTICS_CLIENT
SSS_T24_REMINDER_CLIENT
SSS_D1_POSTHARTER_CLIENT
SSS_REVIEW_REQUEST_CLIENT
ME_REVIEW_REQUEST_CLIENT
SSS_REFERRAL_ACTIVATION_CLIENT
SSS_REBOOKING_CLIENT
VENDOR_CHARTER_BRIEF
```

---

## SECTION 9 — AUDIT LOG ENTRY CONVENTIONS

Every Audit_Log record written by Make follows this format in the `Triggering_Event` field:

```
[SCENARIO_ID] — [Trigger Description] — [Record ID affected]
```

Examples:
```
M-LEAD-INTAKE — Webflow form submission — REQ-2026-0047
M-STRIPE-DEPOSIT — Stripe payment_intent.succeeded — BK-2026-0023
M-BASIC-LIFECYCLE — D1 message sent — BK-2026-0019
M-REVIEW-REQUEST — D7 review request sent — BK-2026-0021
M-ESCALATION-ROUTER — L4 emergency triggered — BK-2026-0025
```

The `Output` field in Audit_Log records what was done:
```
[ACTION_TAKEN]: [DESTINATION] | [RESULT]
```

Examples:
```
Email sent: client@email.com | Delivered
Airtable record created: Bookings/rec[ID] | Success
Slack message posted: #sss-ops-bookings | Success
Stripe payment link created: pi_[ID] | Success
Emergency escalation created: EMG-2026-0003 | Success
```

---

## SECTION 10 — ERROR HANDLER NAMING

Error paths within a scenario are labeled:

```
ERR — [failure type] — [action]
```

Examples:
```
ERR — Stripe API timeout — retry 1/4
ERR — Airtable record not found — Luciana alert
ERR — Missing email — SMS only fallback
ERR — Missing contact info — Luciana DM
ERR — Claude API unavailable — manual fallback note
```

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_NAMING_CONVENTIONS v1.0*
*Effective May 2026*
