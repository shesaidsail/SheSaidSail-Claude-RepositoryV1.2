# MAKE.COM DEPLOYMENT ORDER — STAGE 1
## She Said Sail + Mare Executive — Production Deployment Governance

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Effective Date:** May 2026  
**Owner:** Will (Founder)  
**Applies To:** All 8 Stage 1 Make.com Scenarios  
**Classification:** Confidential — Internal Use Only  
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

## SECTION 1 — DEPLOYMENT PATH MANDATE

### 1.1 The Mandatory Three-Environment Path

Every scenario must traverse all three environments in sequence. There are no exceptions. A scenario may not be deployed to Production without documented evidence of Sandbox completion and Will sign-off.

```
DEVELOPMENT → SANDBOX → PRODUCTION

Development:  Build and unit test in Make's development workspace.
              No live Airtable base. No live client data. Test JSON fixtures only.

Sandbox:      Connect to SSS Sandbox base (dedicated — never a repurposed production base).
              All Stripe calls use test-mode keys. All Gmail sends route to internal test inbox.
              All Quo SMS sends route to test numbers. Luciana executes test suite per protocol.

Production:   Will signs off after Sandbox pass. Activated only outside charter hours.
              Full monitoring from first execution.
```

### 1.2 Promotion Criteria (Sandbox → Production)

A scenario is eligible for Production promotion only when ALL of the following are true:

1. All test cases in MAKE_TESTING_PROTOCOLS.md pass with no open defects
2. Error handling paths tested and verified (forced failures produce correct Automation_Failures records)
3. Idempotency protection verified (duplicate webhook replay produces no duplicate records)
4. Environment guard verified (Sandbox records rejected by production scenario logic)
5. Luciana has signed the Sandbox Test Results template for this scenario
6. Will has reviewed and signed the Production Activation Checklist (Section 7)

### 1.3 Timing Constraint — No Deployment During Charter Hours

**Blocked deployment window:** 08:00–20:00 local time in any active charter city.

Active charter cities as of May 2026: Miami (ET), [additional cities per expansion].

**Permitted deployment windows:**
- 20:00 – 08:00 local (ET) on any non-charter day
- Pre-deployment check: Luciana confirms no active charters within the next 4 hours before any production activation

Rationale: A scenario misconfiguration during active charter hours could disrupt real client communications or Stripe payment flows with no time to recover.

---

## SECTION 2 — DEPLOYMENT ORDER FOR ALL 8 STAGE 1 SCENARIOS

### 2.1 Canonical Deployment Order

The 8 scenarios must be deployed in this exact order. Each scenario depends on the one(s) above it being functional before it can be fully validated.

| Deploy Order | Scenario ID | Scenario Name | Rationale |
|-------------|-------------|---------------|-----------|
| 1 | M-AUDIT-LOGGER | Audit Logger | Must exist before any other scenario runs. All scenarios write to Audit Log. Cannot log if logger is not deployed first. |
| 2 | M-BRAND-ROUTER | Brand Router | Entry point for all inbound webhooks. Must be deployed and verified before any lead can enter the system. |
| 3 | M-LEAD-INTAKE | Lead Intake | Depends on M-BRAND-ROUTER routing correctly. Depends on M-AUDIT-LOGGER for execution logging. |
| 4 | M-SLACK-ALERTS | Slack Alerts | Depends on M-LEAD-INTAKE generating trigger events. Must be verified before Luciana is notified of any live lead. |
| 5 | M-CONCIERGE-ASSIGNMENT | Concierge Assignment | Depends on M-LEAD-INTAKE creating Request records with correct Brand field. Must fire after Request is created and Slack alert is sent. |
| 6 | M-STRIPE-DEPOSIT | Stripe Deposit | Depends on M-CONCIERGE-ASSIGNMENT confirming assignment and M-LEAD-INTAKE creating Request record. Stripe test-mode only in Sandbox. |
| 7 | M-BOOKING-CREATION | Booking Creation | Depends on M-STRIPE-DEPOSIT deposit confirmation. Creates the Booking record that all downstream systems reference. |
| 8 | M-BOOKING-CONFIRMATION | Booking Confirmation | Depends on M-BOOKING-CREATION creating a valid Booking record. Last scenario in the chain. Sends client-facing communications. |

### 2.2 Rationale for Reverse-Deploy-Then-Forward Approach

M-AUDIT-LOGGER deploys first because every scenario writes to the Audit Log. Deploying M-BRAND-ROUTER before M-AUDIT-LOGGER would result in unlogged executions from the first moment of production activation — a governance violation.

M-BOOKING-CONFIRMATION deploys last because it sends real emails and SMS to clients. Any misconfiguration in the scenarios upstream of it (routing, assignment, Stripe) must be resolved before client-facing messages are permitted.

---

## SECTION 3 — PREREQUISITES PER SCENARIO

### 3.1 M-AUDIT-LOGGER

**Airtable prerequisites:**
- Audit_Log table (tblrMpTfMk8q1eNHp) has all 8 expanded governance fields added (per Airtable Spec Section 3.6)
- Execution_ID, Scenario_Name, Gap_Flag, Gap_Duration_Minutes fields exist

**Make prerequisites:**
- Make connection to She Said Sail Airtable base authenticated (production API key)
- Airtable connection scoped to Audit_Log table write permissions confirmed

**Human prerequisites:**
- None. This scenario has no external API dependencies.

### 3.2 M-BRAND-ROUTER

**Airtable prerequisites:**
- M-AUDIT-LOGGER deployed and passing (Deploy Order 1 complete)
- Requests table (tblTlSB9CO4dTGodg) has Environment field added
- Brand field on Requests confirmed as Single Select: SSS / ME

**Make prerequisites:**
- Webflow webhook endpoint configured in Make (Custom Webhook trigger)
- Webhook URL shared with Webflow developer for form POST configuration
- Idempotency_Key field added to Requests table

**Human prerequisites:**
- Will approves the brand routing rules (SSS form → SSS routing; ME form → ME routing)

### 3.3 M-LEAD-INTAKE

**Airtable prerequisites:**
- M-BRAND-ROUTER deployed and passing (Deploy Order 2 complete)
- Requests table all required fields exist (per Airtable Spec Section 3.3)
- Clients table (tblr84vRIWC5HmKvo) has UUID formula and Environment field added

**Make prerequisites:**
- Airtable connection authenticated with write access to Requests and Clients tables
- Idempotency check module configured before first Airtable write

**Human prerequisites:**
- Luciana confirms she has access to the Requests table view in Airtable
- Will approves the lead intake field mapping (webhook payload → Airtable fields)

### 3.4 M-SLACK-ALERTS

**Airtable prerequisites:**
- M-LEAD-INTAKE deployed and passing (Deploy Order 3 complete)

**Make prerequisites:**
- Slack connection authenticated in Make (OAuth app, not legacy token)
- #sss-ops-alerts channel confirmed to exist in the She Said Sail Slack workspace
- #sss-emergency-ops channel confirmed to exist
- Luciana's Slack user ID confirmed (for DM fallback)
- Will's Slack user ID confirmed (for Level 4 DM)

**Human prerequisites:**
- Luciana confirms she receives test Slack alert in #sss-ops-alerts
- Will confirms he receives test DM

### 3.5 M-CONCIERGE-ASSIGNMENT

**Airtable prerequisites:**
- M-SLACK-ALERTS deployed and passing (Deploy Order 4 complete)
- Concierge_Operators table migrated to main base from app2FbmVD44BXShyx (per Airtable Spec Section 5 Phase 3 Step 10)

**Make prerequisites:**
- Assignment logic rules documented and hardcoded in scenario (or read from Concierge_Operators table)
- Airtable write access to Requests.Assigned_Concierge field confirmed

**Human prerequisites:**
- Luciana confirms concierge assignment routing rules are correct
- Will approves assignment logic before production activation

### 3.6 M-STRIPE-DEPOSIT

**Airtable prerequisites:**
- M-CONCIERGE-ASSIGNMENT deployed and passing (Deploy Order 5 complete)
- Bookings table (tbl72omPibBkn2hZL) has Environment field added

**Make prerequisites:**
- Stripe connection in Make configured with TEST mode API key for Sandbox
- Stripe connection in Make configured with LIVE mode API key for Production (stored separately — never cross-contaminate)
- Stripe webhook endpoint configured (Stripe → Make) for payment_intent.succeeded event
- Stripe signing secret stored as encrypted Make variable

**Human prerequisites:**
- Will audits Stripe Developer → Webhooks panel and confirms endpoint URL (per Airtable Spec Section 6.5)
- Will approves the deposit amount calculation logic (linked to Packages table)
- Will signs off on Stripe live-key activation before Production go-live

### 3.7 M-BOOKING-CREATION

**Airtable prerequisites:**
- M-STRIPE-DEPOSIT deployed and passing (Deploy Order 6 complete)
- Bookings table field reduction complete: target 70 fields maximum (per Airtable Spec Section 1.3)
- Packages table rebuilt with pricing fields (per Airtable Spec Section 3.5)

**Make prerequisites:**
- Airtable write access to Bookings table confirmed
- Linked record writes tested (Booking → Client, Booking → Yacht, Booking → Package)

**Human prerequisites:**
- Luciana confirms the Bookings table view shows the new record correctly after test
- Will approves the Booking record creation logic and default field values

### 3.8 M-BOOKING-CONFIRMATION

**Airtable prerequisites:**
- M-BOOKING-CREATION deployed and passing (Deploy Order 7 complete)

**Make prerequisites:**
- Gmail connection authenticated (OAuth 2.0, Will's or ops Gmail account)
- Quo SMS connection authenticated and tested with internal test numbers
- Email template variables mapped to Booking and Client Airtable fields
- SMS template variables mapped and character count validated (≤160 chars per segment)

**Human prerequisites:**
- Will reviews and approves all client-facing email templates before production activation
- Luciana confirms she has received test emails and SMS at test addresses
- Will explicitly approves the Gmail OAuth account to be used for production sends

---

## SECTION 4 — HUMAN APPROVAL GATES

The following items require explicit Will sign-off before any scenario moves from Sandbox to Production. "Sign-off" means Will updates the corresponding Airtable Production_Approved field to TRUE and initials the Deployment Log.

| Gate | Item Requiring Will Approval | Scenario Affected |
|------|------------------------------|------------------|
| GATE-01 | Brand routing rules (SSS vs ME classification logic) | M-BRAND-ROUTER |
| GATE-02 | Lead intake field mapping (complete webhook payload → Airtable field list) | M-LEAD-INTAKE |
| GATE-03 | Concierge assignment logic | M-CONCIERGE-ASSIGNMENT |
| GATE-04 | Stripe live API key activation | M-STRIPE-DEPOSIT |
| GATE-05 | Deposit amount calculation and Packages table pricing logic | M-STRIPE-DEPOSIT |
| GATE-06 | Booking record creation defaults and linked record structure | M-BOOKING-CREATION |
| GATE-07 | All client-facing email and SMS templates | M-BOOKING-CONFIRMATION |
| GATE-08 | Gmail OAuth account selection for production sends | M-BOOKING-CONFIRMATION |
| GATE-09 | Full Stage 1 go-live authorization (all 8 scenarios) | All |

---

## SECTION 5 — GO-LIVE SEQUENCE

### 5.1 Wave 1 — Infrastructure Layer (No Client-Facing Risk)

Activate in Production first:
1. **M-AUDIT-LOGGER** — no external APIs, no client impact; activates immediately
2. **M-BRAND-ROUTER** — routes webhooks; client-facing only if real form submission arrives; ensure Webflow forms are NOT live yet
3. **M-SLACK-ALERTS** — internal only; Luciana and Will receive internal alerts; no client impact

Verification before Wave 2: Run an end-to-end internal test using a fake Webflow webhook payload. Confirm M-AUDIT-LOGGER logs the execution, M-BRAND-ROUTER routes correctly, M-SLACK-ALERTS sends to #sss-ops-alerts. All three must pass before Wave 2.

### 5.2 Wave 2 — Operations Layer (Airtable Writes, Internal Only)

4. **M-LEAD-INTAKE** — creates Airtable Request records; internal only; verify with fake payload
5. **M-CONCIERGE-ASSIGNMENT** — writes to Requests table; no client contact yet

Verification before Wave 3: Fake lead creates Request record with correct Brand, correct concierge assignment, correct Environment = Production. Luciana confirms she can see the record in her Airtable view.

### 5.3 Wave 3 — Payment Layer (Real Money Risk — Stripe Live Mode Required)

6. **M-STRIPE-DEPOSIT** — first scenario with real financial impact in Production; Will is required to be available during this activation

Verification before Wave 4: Complete a Stripe test-mode end-to-end in Production (using a test card, not test-mode key — Production Stripe live key with $0.00 or $1.00 test authorization). Confirm Stripe webhook reaches Make and Airtable record updates. Immediately void the test authorization.

### 5.4 Wave 4 — Client Communication Layer (Real Client Contact Risk)

7. **M-BOOKING-CREATION** — creates Booking records; no direct client contact
8. **M-BOOKING-CONFIRMATION** — LAST to go live; sends real emails and SMS

**M-BOOKING-CONFIRMATION production activation requires:**
- Will is present and monitoring
- Luciana is present and monitoring
- First real confirmation email goes to a shared internal test address before any real client address is used
- After first successful real send, Will verbally confirms to Luciana: "Production is hot"

---

## SECTION 6 — ROLLBACK TRIGGERS

The following conditions cause an immediate production rollback of the affected scenario(s). Rollback procedure is documented in MAKE_ROLLBACK_PROTOCOLS.md.

| Trigger | Severity | Scope |
|---------|----------|-------|
| Any scenario sends an email or SMS to a real client with incorrect brand (ME content to SSS client or vice versa) | CRITICAL | M-BOOKING-CONFIRMATION + M-BRAND-ROUTER rollback |
| Any scenario creates a Stripe payment intent with incorrect amount | CRITICAL | M-STRIPE-DEPOSIT rollback |
| Any scenario creates a duplicate Booking record for the same client and charter date | HIGH | M-BOOKING-CREATION rollback |
| More than 3 SEV-2 Founder Decisions created in a 60-minute window | HIGH | Full Stage 1 rollback |
| M-AUDIT-LOGGER stops producing Audit Log entries for more than 30 minutes | HIGH | Full Stage 1 pause pending investigation |
| Any production scenario processes a Sandbox record (Environment guard bypass) | HIGH | Affected scenario rollback |
| Stripe live key exposed or logged in plaintext in any Make execution log | CRITICAL | M-STRIPE-DEPOSIT immediate pause; Will security review |

---

## SECTION 7 — PRODUCTION ACTIVATION CHECKLIST PER SCENARIO

Complete this checklist for each scenario before Production activation. Will initials each item.

### Checklist Template

```
SCENARIO: [SCENARIO-ID — SCENARIO-NAME]
ACTIVATION DATE: [DATE]
ACTIVATION TIME: [TIME — must be outside 08:00–20:00 ET]
ACTIVATED BY: [Will / Luciana — requires Will present]

PRE-ACTIVATION CHECKS
[ ] All Sandbox test cases passed (attach Luciana's signed test results)
[ ] Error handling paths tested and producing correct Automation_Failures records
[ ] Idempotency protection verified — no duplicates on replay test
[ ] Environment guard tested — Sandbox records rejected
[ ] External API connections authenticated in Production Make workspace
[ ] No Sandbox API keys present in Production scenario (Stripe, Gmail, Quo SMS)
[ ] All Human Approval Gates for this scenario cleared (Section 4)
[ ] Deployment Log record created in Airtable before activation
[ ] Charter hours clearance confirmed: no active charters next 4 hours
[ ] Rollback procedure reviewed and ready (MAKE_ROLLBACK_PROTOCOLS.md)

POST-ACTIVATION CHECKS (complete within 15 minutes of activation)
[ ] Trigger a test execution and confirm Audit Log entry created
[ ] Confirm Automation_Failures table has no new records from test
[ ] Confirm scenario appears in HEALTH-001 monitoring poll
[ ] Will verbally confirms to Luciana: "[SCENARIO-NAME] is Production-active"

SIGN-OFF
Will initials: ___     Date/Time: ___
Luciana initials: ___  Date/Time: ___
```

---

## SECTION 8 — PARTIAL FAILURE HANDLING

### 8.1 Scenario: 3 of 8 Scenarios Live, Then a Failure

If a deployment failure occurs mid-sequence (e.g., Scenarios 1–3 are live, Scenario 4 fails Sandbox testing):

1. **Do not activate any further scenarios.** Scenarios 5–8 remain in Sandbox.
2. **Assess whether Scenarios 1–3 pose risk in their current state.** If M-AUDIT-LOGGER, M-BRAND-ROUTER, and M-SLACK-ALERTS are live but M-LEAD-INTAKE has not been promoted, the live scenarios are safe — they handle routing and alerting but do not write client data.
3. **Disable the webhook trigger in Webflow** while the failure is investigated. This prevents any inbound lead from reaching a partially-deployed stack.
4. **Fix in Sandbox** — do not attempt fixes in Production.
5. **Full Sandbox re-test** of the failing scenario before re-attempting promotion.
6. If the failure reveals a flaw in a scenario that is already Production-active, roll back that scenario per MAKE_ROLLBACK_PROTOCOLS.md before proceeding.

### 8.2 Determining Safe Rollback Scope

| Scenarios Live | Failure Point | Rollback Scope |
|----------------|--------------|----------------|
| 1 (M-AUDIT-LOGGER) | Scenario 2 fails | No rollback needed — Scenario 1 is safe standalone |
| 1–3 | Scenario 4 fails | No rollback needed — disable Webflow webhook trigger |
| 1–5 | Scenario 6 fails | Rollback M-STRIPE-DEPOSIT if any payment intents were created |
| 1–6 | Scenario 7 fails | Rollback M-STRIPE-DEPOSIT and M-BOOKING-CREATION if Booking records created |
| 1–7 | Scenario 8 fails | Rollback only M-BOOKING-CONFIRMATION — Scenarios 1–7 safe |

---

## SECTION 9 — DEPLOYMENT LOG REQUIREMENTS

### 9.1 Airtable Deployment Log Table

Every deployment action — promotion, activation, rollback, partial rollback — requires a write to the Deployment_Log table in the main base. This table must be created per Airtable Spec governance (it is referenced in Section 5.7 of the Systems Intelligence Architecture doc under System Health dashboard).

### 9.2 Deployment Log Fields

| Field | Type | Value |
|-------|------|-------|
| Scenario_Name | Single Line Text | e.g., M-BOOKING-CONFIRMATION |
| Action | Single Select | PROMOTED_TO_SANDBOX / ACTIVATED_IN_PRODUCTION / ROLLBACK / PAUSED |
| From_Environment | Single Select | Development / Sandbox / Production |
| To_Environment | Single Select | Sandbox / Production / Rolled Back |
| Deployed_By | Single Line Text | Will or Luciana (name) |
| Deployment_Timestamp | Date/Time | Exact activation time |
| Test_Results_Attached | Checkbox | True = Luciana's signed test results linked |
| Will_Approved | Checkbox | True = Will initiated or explicitly approved |
| Notes | Long Text | Any deviation from standard procedure; partial failure context |
| Rollback_Reason | Long Text | If Action = ROLLBACK: root cause and recovery steps |

### 9.3 Write Timing

The Deployment_Log record is written **before** activating or rolling back a scenario. The record is then updated with the outcome after the activation completes. Never write the log retroactively.

---

*Document Authority: Will (Founder)*  
*Last Review: May 2026*  
*Next Review: After Stage 1 go-live complete*
