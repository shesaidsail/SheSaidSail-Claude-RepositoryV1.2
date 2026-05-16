# MAKE_SCENARIO_REGISTRY

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Master registry of all Make scenarios across all stages. Every production scenario must be registered here.
**Classification:** Confidential — Internal Use Only

---

## REGISTRY INSTRUCTIONS

When a scenario is built and promoted to production:
1. Add Make Scenario ID (from Make dashboard)
2. Add production activation date
3. Update Status to ACTIVE
4. Add any dependency scenario IDs discovered during build

This registry is also maintained as an Airtable table (Make_Scenarios) in the main operations base. The GitHub version is the governance authority when conflicts exist.

---

## STAGE 1 — CORE OPERATIONAL MVP

| Scenario ID | Make Scenario ID | Name | Status | Trigger Type | Autonomy | Activated |
|------------|-----------------|------|--------|-------------|---------|-----------|
| M-LEAD-INTAKE | TBD | Lead Intake Handler | DESIGN | Webhook (Webflow) | Tier A | — |
| M-BRAND-ROUTER | TBD | Brand Classification Router | DESIGN | Sub-scenario | Tier A | — |
| M-BOOKING-CREATION | TBD | Booking Creation Handler | DESIGN | Airtable Webhook | Tier A | — |
| M-STRIPE-DEPOSIT | TBD | Stripe Deposit Link Generator | DESIGN | Stripe Webhook | Tier A | — |
| M-BOOKING-CONFIRMATION | TBD | Booking Confirmation Handler | DESIGN | Airtable Webhook | Tier A | — |
| M-CONCIERGE-ASSIGNMENT | TBD | Concierge Assignment Notifier | DESIGN | Airtable Webhook | Tier A | — |
| M-BASIC-LIFECYCLE | TBD | Basic Charter Lifecycle Scheduler | DESIGN | Schedule (daily 7am) | Tier A | — |
| M-REVIEW-REQUEST | TBD | Post-Charter Review Request | DESIGN | Schedule (daily 7am) | Tier A (conditional) | — |

---

## STAGE 2 — OPERATIONAL AUTOMATION

| Scenario ID | Make Scenario ID | Name | Status | Trigger Type | Autonomy | Activated |
|------------|-----------------|------|--------|-------------|---------|-----------|
| M-YACHT-AVAILABILITY-LOCK | TBD | Yacht Availability Lock | DESIGN | Airtable Webhook | Tier A | — |
| M-DOUBLE-BOOKING-CHECK | TBD | Double Booking Prevention | DESIGN | Airtable Webhook | Tier A | — |
| M-FAILED-PAYMENT-HANDLER | TBD | Failed Payment Handler | DESIGN | Stripe Webhook | Tier A | — |
| M-VENDOR-NOTIFICATIONS | TBD | Vendor Notification Handler | DESIGN | Airtable Webhook | Tier A | — |
| M-CHARTER-BRIEF | TBD | Charter Brief Generator | DESIGN | Airtable Webhook | Tier B | — |
| M-ESCALATION-ROUTER | TBD | Escalation Router | DESIGN | Airtable Webhook | Tier A | — |
| M-REFERRAL-ENGINE | TBD | Referral Activation Engine | DESIGN | Schedule (daily 7am) | Tier A | — |
| M-REBOOKING-ENGINE | TBD | Rebooking Offer Engine | DESIGN | Schedule (daily 7am) | Tier A | — |
| M-AUTOMATION-HEALTH | TBD | Automation Health Monitor | DESIGN | Schedule (every 15min) | Tier A | — |

---

## STAGE 3 — INTELLIGENCE LAYER

| Scenario ID | Make Scenario ID | Name | Status | Trigger Type | Autonomy | Activated |
|------------|-----------------|------|--------|-------------|---------|-----------|
| M-AI-LEAD-SCORING | TBD | AI Lead Scoring Engine | DESIGN | Airtable Webhook | Tier A | — |
| M-LTV-ENGINE | TBD | Client LTV Tracker | DESIGN | Airtable Webhook | Tier A | — |
| M-REVENUE-HEALTH | TBD | Revenue Health Monitor | DESIGN | Schedule (daily 8am) | Tier A | — |
| M-PRICING-INTELLIGENCE | TBD | Pricing Recommendation Engine | DESIGN | Schedule (weekly Mon) | Tier B | — |
| M-FOUNDER-DIGEST | TBD | Founder Thursday Digest | DESIGN | Schedule (Thu 5pm) | Tier A/B | — |
| M-CITY-HEALTH | TBD | City Health Dashboard | DESIGN | Schedule (daily 8am) | Tier A | — |
| M-PARTNER-SCORING | TBD | Partner Quality Scorer | DESIGN | Schedule (weekly Mon) | Tier A | — |
| M-CONCIERGE-INTELLIGENCE | TBD | Concierge Performance Intelligence | DESIGN | Schedule (weekly Mon) | Tier B | — |

---

## STAGE 4 — ADVANCED SCALING + CREATIVE INTELLIGENCE

| Scenario ID | Make Scenario ID | Name | Status | Trigger Type | Autonomy | Activated |
|------------|-----------------|------|--------|-------------|---------|-----------|
| M-CREATIVE-INTELLIGENCE | TBD | Creative Performance Analyzer | DESIGN | Schedule (weekly Mon) | Tier A | — |
| M-CREATIVE-FATIGUE | TBD | Creative Fatigue Detector | DESIGN | Schedule (daily 8am) | Tier A | — |
| M-SYNTER-SYNC | TBD | Synter Financial Sync | DESIGN | Airtable Webhook | Tier A | — |
| M-CAMPAIGN-RECOMMENDER | TBD | AI Campaign Recommendation | DESIGN | Schedule (weekly Mon) | Tier B | — |
| M-SOP-INTELLIGENCE | TBD | SOP Intelligence Analyzer | DESIGN | Schedule (monthly) | Tier B | — |
| M-CITY-LAUNCH | TBD | City Launch Automation | DESIGN | Airtable Webhook | Tier B | — |
| M-EXECUTIVE-DASHBOARD | TBD | Executive Dashboard Feeder | DESIGN | Schedule (daily 8am) | Tier A | — |
| M-OWNER-HUB | TBD | Owner Hub Feed Generator | DESIGN | Schedule (weekly Mon) | Tier A | — |
| M-OPS-HUB | TBD | Ops Hub Feed Generator | DESIGN | Schedule (daily 7:30am) | Tier A | — |

---

## SCENARIO DETAIL CARDS

### M-LEAD-INTAKE
- **Purpose:** Capture inbound leads. Create Requests + Clients records.
- **Trigger:** Webflow form webhook
- **Reads:** Nothing (webhook payload only on first module)
- **Writes:** Requests (create), Clients (create or find), Audit_Log (create)
- **External Calls:** Slack (post message)
- **Failure Mode:** Standard 4-failure chain → SEV-2 on 4th failure
- **Idempotency:** SHA256(email + timestamp) checked against Requests.Idempotency_Key
- **Dependencies:** M-BRAND-ROUTER (sub-call)

---

### M-BRAND-ROUTER
- **Purpose:** Classify every lead as SSS or ME before any processing.
- **Trigger:** Called by M-LEAD-INTAKE; also callable directly
- **Reads:** Referring URL, form fields, occasion field
- **Writes:** Requests.Brand, Requests.Routing_Confidence
- **External Calls:** None
- **Failure Mode:** Ambiguous → default SSS + LOW confidence + Luciana alert
- **Dependencies:** None

---

### M-BOOKING-CREATION
- **Purpose:** Create Booking from confirmed Request. Generate Stripe deposit link.
- **Trigger:** Requests.Status → AVAILABILITY_CONFIRMED
- **Reads:** Requests, Clients, Packages, Yachts
- **Writes:** Bookings (create), Requests (update Status + Booking link), Audit_Log
- **External Calls:** Stripe (create payment link), Gmail (send email), Quo SMS (send SMS), Slack
- **Failure Mode:** Stripe API failure → retry × 4 → SEV-2 → manual link creation
- **Idempotency:** Checks Bookings for existing record with same Request_Link before creating
- **Dependencies:** M-DOUBLE-BOOKING-CHECK (Stage 2 adds pre-check)

---

### M-STRIPE-DEPOSIT
- **Purpose:** Handle Stripe deposit success webhook. Update Booking. Send confirmation.
- **Trigger:** Stripe payment_intent.succeeded webhook
- **Reads:** Bookings (by metadata lookup)
- **Writes:** Bookings (update Status + payment fields), Audit_Log
- **External Calls:** Gmail, Quo SMS, Slack
- **Failure Mode:** 4-failure chain; non-200 → Stripe retries automatically for up to 72 hours
- **Idempotency:** Stripe payment_intent_id stored in Bookings.Idempotency_Key
- **Dependencies:** None (Stripe triggers directly)

---

### M-BOOKING-CONFIRMATION
- **Purpose:** Send formal charter confirmation when Booking reaches CONFIRMED status.
- **Trigger:** Bookings.Status → CONFIRMED
- **Reads:** Bookings, Clients, Packages, Yachts
- **Writes:** Bookings (update Confirmation_Sent_At), Audit_Log
- **External Calls:** Gmail, Slack
- **Failure Mode:** HV client → Tier B (Luciana sends manually); standard → autonomous
- **Dependencies:** None

---

### M-CONCIERGE-ASSIGNMENT
- **Purpose:** Notify concierge/city manager of new assignment.
- **Trigger:** Bookings.Status → DEPOSIT_PAID
- **Reads:** Bookings, Concierge_Operators, Cities
- **Writes:** Bookings (update Concierge_Notified_At), Audit_Log
- **External Calls:** Slack (DM), Gmail (backup)
- **Failure Mode:** Missing Slack ID → email fallback → missing email → Luciana DM

---

### M-BASIC-LIFECYCLE
- **Purpose:** Daily lifecycle scheduler — T-72, T-48, T-24, T-12, D1 messages.
- **Trigger:** Schedule daily 7:00 AM
- **Reads:** Bookings (all active), Clients
- **Writes:** Bookings (individual send-state fields), Audit_Log
- **External Calls:** Gmail, Quo SMS, Stripe (balance link), Slack
- **Failure Mode:** Any individual booking failure → log + continue to next booking (don't halt full run)
- **Idempotency:** Each send-state field (D72hr_Reminder_Sent, etc.) acts as idempotency gate

---

### M-REVIEW-REQUEST
- **Purpose:** D7 review request for eligible completed bookings.
- **Trigger:** Schedule daily 7:00 AM
- **Reads:** Bookings (filter D7_Review_Eligible = true + D7_Sent = false)
- **Writes:** Bookings (D7_Sent = true), Audit_Log
- **External Calls:** Gmail, Quo SMS
- **Failure Mode:** Missing email → SMS only. Missing both → Luciana DM.
- **Idempotency:** D7_Sent field gates re-send

---

### M-YACHT-AVAILABILITY-LOCK
- **Purpose:** Lock yacht date in Yacht_Availability on deposit confirmation.
- **Trigger:** Bookings.Status → DEPOSIT_PAID
- **Reads:** Bookings, Yacht_Availability
- **Writes:** Yacht_Availability (update Status → BOOKED), Audit_Log
- **Failure Mode:** Conflict found → SEV-2 alert; no lock without human resolution

---

### M-DOUBLE-BOOKING-CHECK
- **Purpose:** Pre-confirmation availability safety gate.
- **Trigger:** Requests.Status → AVAILABILITY_CONFIRMED
- **Reads:** Yacht_Availability
- **Writes:** Requests (rollback Status if conflict), Audit_Log
- **Failure Mode:** Yacht not assigned → alert Luciana

---

### M-FAILED-PAYMENT-HANDLER
- **Purpose:** Handle Stripe payment failures with graduated escalation.
- **Trigger:** Stripe payment_intent.payment_failed
- **Reads:** Bookings (by Stripe metadata)
- **Writes:** Bookings (failure count + reason), Audit_Log
- **External Calls:** Gmail, Quo SMS, Slack
- **Failure Mode:** Booking not found → Luciana DM with raw Stripe data

---

### M-AUTOMATION-HEALTH
- **Purpose:** Every 15 minutes — detect anomalies, surface SEV-level alerts.
- **Trigger:** Schedule every 15 minutes
- **Reads:** Automation_Health, Bookings, Audit_Log, Make_Scenarios
- **Writes:** Automation_Health (log anomalies)
- **External Calls:** Slack
- **Known Limitation:** Cannot self-alert on its own failure. Daily human review of #sss-ops-alerts required.

---

### M-SYNTER-SYNC
- **Purpose:** Bridge completed booking financials to SSS Financials base.
- **Trigger:** Bookings.Status → COMPLETED
- **Reads:** Bookings (main base, appdZ49WqgjRXxA1R)
- **Writes:** P&L Per Charter (financials base, apprDKQtV2GInThwE), Bookings.Financial_Sync_Status
- **Cross-Base:** Make is the bridge — no linked records across bases
- **Failure Mode:** Sync failure → Sync_Status = FAILED → M-AUTOMATION-HEALTH catches within 24hrs

---

## AI PROMPT VERSION REQUIREMENTS BY SCENARIO

| Scenario | Make_Variable_Name | Required in AI_Prompt_Versions |
|---------|-------------------|-------------------------------|
| M-CHARTER-BRIEF | CHARTER_BRIEF_SYSTEM | Yes — Will_Approved = true, Status = PRODUCTION |
| M-AI-LEAD-SCORING | LEAD_SCORING_SYSTEM | Yes |
| M-FOUNDER-DIGEST | FOUNDER_DIGEST_SYSTEM | Yes |
| M-CITY-HEALTH | — | No Claude API call |
| M-PRICING-INTELLIGENCE | PRICING_INTELLIGENCE_SYSTEM | Yes |
| M-CONCIERGE-INTELLIGENCE | CONCIERGE_INTELLIGENCE_SYSTEM | Yes |
| M-CREATIVE-INTELLIGENCE | CREATIVE_INTELLIGENCE_SYSTEM | Yes |
| M-CAMPAIGN-RECOMMENDER | CAMPAIGN_RECOMMENDER_SYSTEM | Yes |
| M-SOP-INTELLIGENCE | SOP_INTELLIGENCE_SYSTEM | Yes |

---

## STATUS DEFINITIONS

| Status | Meaning |
|--------|---------|
| DESIGN | Architecture documented — not yet built in Make |
| BUILD | Being built in Make sandbox |
| SANDBOX_TEST | Built and being tested in sandbox environment |
| PRODUCTION_PENDING | Sandbox test complete — awaiting Will approval for production promotion |
| ACTIVE | Running in production |
| PAUSED | Temporarily paused — documented reason required |
| DEPRECATED | Replaced by newer version — kept for rollback reference |
| RETIRED | No longer in use — archived |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_SCENARIO_REGISTRY v1.0*
*Effective May 2026*
