# MAKE_MASTER_ARCHITECTURE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail + Mare Executive — All Make Scenarios, All Stages
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Systems Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

## DOCUMENT PURPOSE

This document is the top-level orchestration map for all Make.com automation at She Said Sail and Mare Executive. It defines the complete scenario catalog, deployment stage model, orchestration principles, naming conventions, and inter-scenario dependencies. Every scenario in production must be registered here and traceable to this map.

This is not theoretical. Every module referenced maps to real Make modules. Every Airtable field referenced exists in the production base (appdZ49WqgjRXxA1R) or will exist after the Airtable pre-Make build completes.

---

## SECTION 1 — ORCHESTRATION PRINCIPLES

### 1.1 Make's Role in the Stack

Make is Layer 4 — the Orchestration Layer. It executes. It does not decide, reason, or govern. Claude reasons at Layer 2. Airtable stores truth at Layer 3. Make moves data between systems and triggers timed actions.

Make never:
- Holds business logic that belongs in Airtable formulas
- Holds AI reasoning that belongs in Claude
- Executes client-facing financial actions without an Airtable state change first
- Runs without logging the result to Airtable

### 1.2 Global Architecture Rules (All Scenarios)

| Rule | Enforcement |
|------|-------------|
| Single-responsibility per scenario | One scenario = one operational purpose |
| Airtable-first state | Booking state lives in Airtable. Make reads it. Make writes it. Make never assumes it. |
| Check Emergency_Flag + Automations_Paused first | Every client-facing scenario checks both fields before any outbound action |
| Check Environment field | Production scenarios exit immediately if Environment ≠ Production |
| Idempotency required | Every create/send scenario checks Idempotency_Key before acting |
| Audit Log entry mandatory | Every Tier A autonomous action writes to Audit Log before completion |
| Error handling required | Every scenario implements the 4-failure escalation chain |
| No circular triggers | No scenario may trigger another scenario that triggers the first |
| Sandbox safety | Sandbox scenarios write only to the SSS Sandbox base — never production |

### 1.3 Brand Router Rule

M-BRAND-ROUTER executes as the first module in every inbound lead flow and every AI content generation task. Brand classification is written to the Airtable record before any other processing continues. A brand routing failure — SSS content generated for ME client or vice versa — halts the scenario and creates a Slack alert.

### 1.4 Trigger Discipline

| Trigger Type | Use Case | Risk |
|-------------|----------|------|
| Webhook (Airtable) | Record created / field changed | Risk: circular trigger if Make writes back to same field |
| Webhook (Stripe) | Payment events | Risk: replay attack — timestamp validation required |
| Webhook (Webflow) | Form submissions | Risk: duplicate submission — idempotency check required |
| Schedule | Timed daily/weekly actions | Risk: missed execution — HEALTH-001 monitors |
| HTTP (Make → Make) | Scenario chaining | Prohibited — use Airtable state change as handoff instead |

---

## SECTION 2 — STAGED DEPLOYMENT MODEL

The system deploys in four sequential stages. Each stage is independently operational. No stage requires the next stage to be running. Later stages add capability without disrupting earlier stages.

```
STAGE 1 — CORE OPERATIONAL MVP
  Revenue generation. Lead → Booking → Payment → Confirmation → Review.
  Ads can run safely when Stage 1 is complete.

STAGE 2 — OPERATIONAL AUTOMATION
  Reduce manual load. Add safety nets. Add vendor/captain logistics.
  Business operates reliably without constant manual intervention.

STAGE 3 — INTELLIGENCE LAYER
  AI-driven founder leverage. Revenue health. LTV tracking. Digests.
  Founder operates strategically rather than operationally.

STAGE 4 — ADVANCED SCALING + CREATIVE INTELLIGENCE
  Multi-city engine. Creative scoring. Campaign intelligence.
  Platform-ready. Acquisition-ready. Scale-ready.
```

---

## SECTION 3 — COMPLETE SCENARIO CATALOG

### STAGE 1 — CORE OPERATIONAL MVP

| Scenario ID | Name | Trigger | Primary Tables | Autonomy Tier |
|------------|------|---------|----------------|---------------|
| M-LEAD-INTAKE | Lead Intake Handler | Webflow webhook (form submit) | Requests, Clients, Audit_Log | A |
| M-BRAND-ROUTER | Brand Classification Router | Sub-scenario called by M-LEAD-INTAKE | Requests, Audit_Log | A |
| M-BOOKING-CREATION | Booking Creation Handler | Airtable webhook: Requests.Status → AVAILABILITY_CONFIRMED | Bookings, Clients, Packages, Yachts, Audit_Log | A |
| M-STRIPE-DEPOSIT | Stripe Deposit Link Generator | Airtable webhook: Bookings.Status → DEPOSIT_SENT | Bookings, Clients, Stripe, Audit_Log | A |
| M-BOOKING-CONFIRMATION | Booking Confirmation Handler | Stripe webhook: payment_intent.succeeded (deposit) | Bookings, Clients, Audit_Log | A |
| M-CONCIERGE-ASSIGNMENT | Concierge Assignment Notifier | Airtable webhook: Bookings.Status → DEPOSIT_PAID | Bookings, Concierge_Operators, Audit_Log | A |
| M-BASIC-LIFECYCLE | Basic Charter Lifecycle Scheduler | Schedule: daily 7am | Bookings, Clients, Audit_Log | A |
| M-REVIEW-REQUEST | Post-Charter Review Request | Schedule: daily 7am — filters D7_Review_Eligible | Bookings, Clients, Audit_Log | A (conditional) |

### STAGE 2 — OPERATIONAL AUTOMATION

| Scenario ID | Name | Trigger | Primary Tables | Autonomy Tier |
|------------|------|---------|----------------|---------------|
| M-YACHT-AVAILABILITY-LOCK | Yacht Availability Lock | Airtable webhook: Bookings.Status → DEPOSIT_PAID | Yacht_Availability, Bookings, Audit_Log | A |
| M-DOUBLE-BOOKING-CHECK | Double Booking Prevention | Airtable webhook: Bookings.Status → AVAILABILITY_CONFIRMED | Yacht_Availability, Bookings, Audit_Log | A |
| M-FAILED-PAYMENT-HANDLER | Failed Payment Handler | Stripe webhook: payment_intent.payment_failed | Bookings, Clients, Audit_Log | A |
| M-VENDOR-NOTIFICATIONS | Vendor Notification Handler | Airtable webhook: Bookings.Charter_Brief_Sent → true | Vendors, Bookings, Audit_Log | A |
| M-CHARTER-BRIEF | Charter Brief Generator | Airtable webhook: Bookings.Status → CONFIRMED | Bookings, Clients, Yachts, Packages, Vendors, Audit_Log | B |
| M-ESCALATION-ROUTER | Escalation Router | Airtable webhook: Requests.Agent_Status → ESCALATED | Requests, Bookings, Founder_Decisions, Audit_Log | A |
| M-REFERRAL-ENGINE | Referral Activation Engine | Schedule: daily 7am — filters D30 eligible | Bookings, Clients, Affiliates, Audit_Log | A |
| M-REBOOKING-ENGINE | Rebooking Offer Engine | Schedule: daily 7am — filters D60 eligible | Bookings, Clients, Audit_Log | A |
| M-AUTOMATION-HEALTH | Automation Health Monitor | Schedule: every 15 minutes | Automation_Health, Make_Scenarios, Audit_Log | A |

### STAGE 3 — INTELLIGENCE LAYER

| Scenario ID | Name | Trigger | Primary Tables | Autonomy Tier |
|------------|------|---------|----------------|---------------|
| M-AI-LEAD-SCORING | AI Lead Scoring Engine | Airtable webhook: Requests.Status → NEW | Requests, Clients, AI_Prompt_Versions, Audit_Log | A |
| M-LTV-ENGINE | Client LTV Tracker | Airtable webhook: Bookings.Status → COMPLETED | Clients, Bookings, Audit_Log | A |
| M-REVENUE-HEALTH | Revenue Health Monitor | Schedule: daily 8am | Bookings, P&L_Per_Charter, Financial_Periods, Audit_Log | A |
| M-PRICING-INTELLIGENCE | Pricing Recommendation Engine | Schedule: weekly Monday 8am | Packages, Bookings, Audit_Log | B |
| M-FOUNDER-DIGEST | Founder Thursday Digest | Schedule: Thursday 5pm | Bookings, Requests, Lessons, Founder_Decisions, Audit_Log | A |
| M-CITY-HEALTH | City Health Dashboard | Schedule: daily 8am | Cities, Bookings, Audit_Log | A |
| M-PARTNER-SCORING | Partner Quality Scorer | Schedule: weekly Monday 8am | Partner_Outreach, Affiliates, Bookings, Audit_Log | A |
| M-CONCIERGE-INTELLIGENCE | Concierge Performance Intelligence | Schedule: weekly Monday 8am | Concierge_Operators, Bookings, Audit_Log | B |

### STAGE 4 — ADVANCED SCALING + CREATIVE INTELLIGENCE

| Scenario ID | Name | Trigger | Primary Tables | Autonomy Tier |
|------------|------|---------|----------------|---------------|
| M-CREATIVE-INTELLIGENCE | Creative Performance Analyzer | Schedule: weekly Monday 8am | Organic_Content, Paid_Ads, Audit_Log | A |
| M-CREATIVE-FATIGUE | Creative Fatigue Detector | Schedule: daily 8am | Paid_Ads, Organic_Content, Audit_Log | A |
| M-SYNTER-SYNC | Synter Financial Sync | Airtable webhook: Bookings.Status → COMPLETED | Bookings, P&L_Per_Charter, Financial_Periods, Audit_Log | A |
| M-CAMPAIGN-RECOMMENDER | AI Campaign Recommendation | Schedule: weekly Monday 8am | Paid_Ads, Organic_Content, AI_Prompt_Versions, Audit_Log | B |
| M-SOP-INTELLIGENCE | SOP Intelligence Analyzer | Schedule: monthly | Lessons, Audit_Log | B |
| M-CITY-LAUNCH | City Launch Automation | Airtable webhook: Cities.Active → true | Cities, Yachts, Vendors, Packages, Audit_Log | B |
| M-EXECUTIVE-DASHBOARD | Executive Dashboard Feeder | Schedule: daily 8am | Bookings, Financial_Periods, Cities, Audit_Log | A |
| M-OWNER-HUB | Owner Hub Feed Generator | Schedule: weekly Monday 8am | Bookings, Financial_Periods, Audit_Log | A |
| M-OPS-HUB | Ops Hub Feed Generator | Schedule: daily 8am | Bookings, Requests, Concierge_Operators, Audit_Log | A |

---

## SECTION 4 — INTER-SCENARIO DEPENDENCY MAP

```
INBOUND FLOW:
Webflow Form → M-LEAD-INTAKE → [M-BRAND-ROUTER] → Requests record created
                                                       ↓
                                                 M-AI-LEAD-SCORING (Stage 3)
                                                       ↓
                              Luciana reviews → AVAILABILITY_CONFIRMED
                                                       ↓
                                             M-BOOKING-CREATION
                                                       ↓
                                              M-STRIPE-DEPOSIT
                                                       ↓
STRIPE FLOW:
Stripe webhook: payment_intent.succeeded → M-BOOKING-CONFIRMATION
                                                       ↓
                                          M-CONCIERGE-ASSIGNMENT
                                                       ↓
                                          M-YACHT-AVAILABILITY-LOCK (Stage 2)
                                                       ↓
CHARTER LIFECYCLE:
M-BASIC-LIFECYCLE (daily schedule) manages:
  T-72hr → Balance reminder
  T-48hr → Charter Brief delivery (M-CHARTER-BRIEF Stage 2)
  T-24hr → Logistics reminder
  T-12hr → Final reminder
  D1     → Post-charter warmth
  D7     → M-REVIEW-REQUEST
  D30    → M-REFERRAL-ENGINE (Stage 2)
  D60    → M-REBOOKING-ENGINE (Stage 2)

INTELLIGENCE LAYER (Stage 3 — parallel to all above):
M-REVENUE-HEALTH (daily)
M-CITY-HEALTH (daily)
M-FOUNDER-DIGEST (Thursday)
M-LTV-ENGINE (on booking completion)
```

---

## SECTION 5 — SLACK CHANNEL ROUTING

| Channel | What Posts There | Scenario |
|---------|-----------------|---------|
| #sss-ops-leads | New inbound Request created | M-LEAD-INTAKE |
| #sss-ops-bookings | New Booking created, deposit confirmed | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| #sss-ops-alerts | Automation failures, SEV-2+ events | M-AUTOMATION-HEALTH, error handlers |
| #sss-emergency-ops | L4 emergency alerts only | M-ESCALATION-ROUTER |
| #me-ops-leads | New ME inbound Request | M-LEAD-INTAKE (ME brand route) |
| #me-ops-bookings | ME Booking events | M-BOOKING-CREATION (ME brand route) |
| Will DM | Emergency alerts, SEV-1, digest | M-ESCALATION-ROUTER, M-FOUNDER-DIGEST |
| Luciana DM | SEV-2, review required actions | M-AUTOMATION-HEALTH, M-ESCALATION-ROUTER |

---

## SECTION 6 — MAKE FOLDER STRUCTURE

All scenarios organized in Make under these folder names:

```
She Said Sail + Mare Executive/
├── STAGE_1_CORE/
│   ├── M-LEAD-INTAKE
│   ├── M-BRAND-ROUTER
│   ├── M-BOOKING-CREATION
│   ├── M-STRIPE-DEPOSIT
│   ├── M-BOOKING-CONFIRMATION
│   ├── M-CONCIERGE-ASSIGNMENT
│   ├── M-BASIC-LIFECYCLE
│   └── M-REVIEW-REQUEST
├── STAGE_2_OPERATIONS/
│   ├── M-YACHT-AVAILABILITY-LOCK
│   ├── M-DOUBLE-BOOKING-CHECK
│   ├── M-FAILED-PAYMENT-HANDLER
│   ├── M-VENDOR-NOTIFICATIONS
│   ├── M-CHARTER-BRIEF
│   ├── M-ESCALATION-ROUTER
│   ├── M-REFERRAL-ENGINE
│   ├── M-REBOOKING-ENGINE
│   └── M-AUTOMATION-HEALTH
├── STAGE_3_INTELLIGENCE/
│   ├── M-AI-LEAD-SCORING
│   ├── M-LTV-ENGINE
│   ├── M-REVENUE-HEALTH
│   ├── M-PRICING-INTELLIGENCE
│   ├── M-FOUNDER-DIGEST
│   ├── M-CITY-HEALTH
│   ├── M-PARTNER-SCORING
│   └── M-CONCIERGE-INTELLIGENCE
├── STAGE_4_SCALE/
│   ├── M-CREATIVE-INTELLIGENCE
│   ├── M-CREATIVE-FATIGUE
│   ├── M-SYNTER-SYNC
│   ├── M-CAMPAIGN-RECOMMENDER
│   ├── M-SOP-INTELLIGENCE
│   ├── M-CITY-LAUNCH
│   ├── M-EXECUTIVE-DASHBOARD
│   ├── M-OWNER-HUB
│   └── M-OPS-HUB
└── SHARED_UTILITIES/
    ├── ERR-HANDLER (reusable error module)
    ├── AUDIT-WRITER (reusable audit log writer)
    └── ENV-CHECK (reusable environment guard)
```

---

## SECTION 7 — PRODUCTION AIRTABLE BASE REFERENCES

| Base Name | Base ID | Role |
|-----------|---------|------|
| SSS Operations (PRIMARY) | appdZ49WqgjRXxA1R | All core ops, intelligence, governance |
| SSS Financials | apprDKQtV2GInThwE | Financial intelligence, P&L, payouts |
| SSS Sandbox | TBD | Testing only — never referenced in production scenarios |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_MASTER_ARCHITECTURE v1.0*
*Effective May 2026*
*Owner: Will (Founder)*
