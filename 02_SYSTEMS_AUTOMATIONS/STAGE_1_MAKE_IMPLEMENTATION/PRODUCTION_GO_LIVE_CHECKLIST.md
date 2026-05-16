# PRODUCTION_GO_LIVE_CHECKLIST

**Status:** PRODUCTION GATE DOCUMENT
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Ops Lead:** Luciana
**Scope:** She Said Sail + Mare Executive — Stage 1 Make Scenarios (All 8)
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Go-Live Rule:** This checklist must reach 100% completion — zero open items, zero conditional passes — before any Stage 1 scenario is activated against real client data. Each item is signed off by the responsible party (Will, Luciana, or system-verified). The Final Verdict at the bottom of this document is the official go-live authorization. No verbal approval substitutes for a completed checklist.

---

## SECTION 1 — CREDENTIALS AND CONNECTIONS

Every Make connection listed below must be confirmed live in the Make production workspace. "Live" means an authenticated test call returned a successful response within the last 48 hours. Expired OAuth tokens, rotated API keys, and connection warnings are immediate blockers.

| # | Connection | Make Module Type | Auth Method | Test Method | Status | Confirmed By | Date |
|---|-----------|-----------------|-------------|-------------|--------|-------------|------|
| 1.01 | Airtable — SSS Operations (appdZ49WqgjRXxA1R) | Airtable module | Personal Access Token | List Records call on Requests table | [ ] | | |
| 1.02 | Airtable — SSS Financials (apprDKQtV2GInThwE) | Airtable module | Personal Access Token | List Records call on P&L Per Charter table | [ ] | | |
| 1.03 | Stripe — Production API | Stripe module | Secret Key (live mode) | Retrieve Products call | [ ] | | |
| 1.04 | Stripe — Webhooks | Make Webhook (inbound) | Signing Secret | Stripe webhook test event received | [ ] | | |
| 1.05 | Slack — #sss-ops-alerts | Slack module | OAuth App | Send test message to #sss-ops-alerts | [ ] | | |
| 1.06 | Slack — #sss-emergency-ops | Slack module | OAuth App | Send test message to #sss-emergency-ops | [ ] | | |
| 1.07 | Slack — Will DM | Slack module | OAuth App | Send test DM to Will | [ ] | | |
| 1.08 | Slack — Luciana DM | Slack module | OAuth App | Send test DM to Luciana | [ ] | | |
| 1.09 | Gmail — hello@shesaidsail.com | Gmail module | OAuth | Send test email to internal test address | [ ] | | |
| 1.10 | Quo SMS | HTTP module | API Key | Send test SMS to internal test number | [ ] | | |
| 1.11 | Anthropic API (Claude) | HTTP module | Bearer Token | Completion call with 5-word prompt | [ ] | | |

**Section 1 Sign-Off:** [ ] All 11 connections confirmed live
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 2 — WEBHOOK REGISTRATION

All webhooks must be registered in their source systems, not merely created in Make. A webhook URL that exists in Make but is not registered in Stripe or Webflow will never receive events. Each webhook must have been confirmed by receiving a test event — not just by the URL being valid.

| # | Webhook Name | Make Scenario | Source System | Registered In | Events Subscribed | Test Event Received | Status | Date |
|---|-------------|--------------|---------------|--------------|-------------------|--------------------| -------|------|
| 2.01 | WHK-SSS-LEAD-PROD | M-LEAD-INTAKE | Webflow | Webflow form settings | Form submission | [ ] | [ ] | |
| 2.02 | WHK-ME-LEAD-PROD | M-LEAD-INTAKE (ME route) | Webflow | Webflow form settings | Form submission | [ ] | [ ] | |
| 2.03 | WHK-SSS-STRIPE-DEPOSIT-PROD | M-STRIPE-DEPOSIT | Stripe | Stripe dashboard → Webhooks | payment_intent.succeeded, checkout.session.completed | [ ] | [ ] | |
| 2.04 | WHK-SSS-AIRTABLE-ROUTER-PROD | M-BRAND-ROUTER | Airtable | Airtable Automations → Webhook | Record created in Requests | [ ] | [ ] | |
| 2.05 | WHK-SSS-BOOKING-CREATED-PROD | M-BOOKING-CREATION | Airtable | Airtable Automations → Webhook | Record created in Bookings | [ ] | [ ] | |
| 2.06 | WHK-SSS-CONCIERGE-PROD | M-CONCIERGE-ASSIGNMENT | Airtable | Airtable Automations → Webhook | Status field changed on Requests | [ ] | [ ] | |

**Webhook Security Verification:**

| # | Check | Status |
|---|-------|--------|
| 2.W1 | All inbound webhooks validate Authorization Bearer header as Step 1 | [ ] |
| 2.W2 | Stripe webhooks validate signing secret (not just bearer token) | [ ] |
| 2.W3 | Timestamp validation rejects events older than 5 minutes | [ ] |
| 2.W4 | Webhook URLs use HTTPS only — no HTTP endpoints exist | [ ] |
| 2.W5 | Stripe webhook endpoint only accepts Stripe IP ranges where applicable | [ ] |

**Section 2 Sign-Off:** [ ] All webhooks registered and confirmed with test events
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 3 — AIRTABLE SCHEMA VALIDATION

Every field that a Stage 1 Make scenario reads or writes must exist in the correct table with the correct field type. A missing field causes a silent failure — Make receives null, proceeds, and creates a corrupt or incomplete record.

### 3.1 Universal Required Fields — All Production Tables

Confirm the following fields exist on ALL tables accessed by Stage 1 Make scenarios:

| Field | Type | Tables to Check | Status |
|-------|------|----------------|--------|
| UUID (RECORD_ID() formula) | Formula | Requests, Bookings, Clients, Audit Log, Automation_Health | [ ] |
| Environment | Single Select: Production / Sandbox / Development | Requests, Bookings, Clients, Audit Log, Automation_Health | [ ] |
| Brand | Single Select: SSS / ME | Requests, Bookings, Audit Log, Automation_Health | [ ] |
| Source_System | Single Select: Stripe / Airtable / Make / Manual / API | Requests, Bookings, Audit Log | [ ] |
| Created_At | DateTime (Airtable Created Time or formula) | Requests, Bookings, Audit Log, Automation_Health | [ ] |

### 3.2 Requests Table (tblTlSB9CO4dTGodg) — Required Fields

| # | Field Name | Type | Required By | Status |
|---|-----------|------|------------|--------|
| 3.R01 | Agent_Status | Single Select: AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED | M-BRAND-ROUTER, M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.R02 | Brand_Routed | Single Select: SSS / ME | M-BRAND-ROUTER output | [ ] |
| 3.R03 | Idempotency_Key | Single Line Text | M-LEAD-INTAKE | [ ] |
| 3.R04 | Escalation_Reason | Long Text | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.R05 | Last_AI_Action | DateTime | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.R06 | AI_Confidence_Score | Number (0–100) | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.R07 | Last_Human_Touch | DateTime | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.R08 | Source_Form | Single Line Text | M-LEAD-INTAKE | [ ] |
| 3.R09 | Automations_Paused | Checkbox | All outbound scenarios | [ ] |

### 3.3 Bookings Table (tbl72omPibBkn2hZL) — Required Fields

| # | Field Name | Type | Required By | Status |
|---|-----------|------|------------|--------|
| 3.B01 | Idempotency_Key | Single Line Text | M-BOOKING-CREATION | [ ] |
| 3.B02 | Emergency_Flag | Checkbox | M-SLACK-ALERTS, HEALTH-001 | [ ] |
| 3.B03 | Automations_Paused | Checkbox | All outbound scenarios | [ ] |
| 3.B04 | HV_Client | Checkbox | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.B05 | Stripe_Payment_Intent_ID | Single Line Text | M-STRIPE-DEPOSIT | [ ] |
| 3.B06 | Stripe_Deposit_Link | URL | M-STRIPE-DEPOSIT | [ ] |
| 3.B07 | Deposit_Paid_At | DateTime | M-STRIPE-DEPOSIT | [ ] |
| 3.B08 | Concierge_Assigned | Linked Record → Brokers | M-CONCIERGE-ASSIGNMENT | [ ] |
| 3.B09 | D7_Review_Eligible | Formula | M-BOOKING-CONFIRMATION | [ ] |
| 3.B10 | Confirmation_Sent_At | DateTime | M-BOOKING-CONFIRMATION | [ ] |
| 3.B11 | Status | Single Select (full lifecycle values) | All scenarios | [ ] |

### 3.4 Audit Log Table (tblrMpTfMk8q1eNHp) — Required Fields

| # | Field Name | Type | Required By | Status |
|---|-----------|------|------------|--------|
| 3.A01 | Audit_ID | Formula: AUD-YYYY-NNNN | M-AUDIT-LOGGER | [ ] |
| 3.A02 | Scenario_ID | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A03 | Action_Type | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A04 | Record_ID_Affected | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A05 | Table_Affected | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A06 | Idempotency_Key | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A07 | Execution_Timestamp | DateTime | M-AUDIT-LOGGER | [ ] |
| 3.A08 | Approval_State | Single Select: AUTONOMOUS / PENDING_HUMAN / HUMAN_APPROVED | M-AUDIT-LOGGER | [ ] |
| 3.A09 | Prompt_Version | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A10 | Rollback_Linkage | Single Line Text | M-AUDIT-LOGGER | [ ] |
| 3.A11 | Brand | Single Select: SSS / ME | M-AUDIT-LOGGER | [ ] |
| 3.A12 | Environment | Single Select | M-AUDIT-LOGGER | [ ] |

### 3.5 Automation_Health Table — Required Fields

| # | Field Name | Type | Status |
|---|-----------|------|--------|
| 3.H01 | Scenario_ID | Single Line Text | [ ] |
| 3.H02 | Last_Execution_Timestamp | DateTime | [ ] |
| 3.H03 | Last_Success_Timestamp | DateTime | [ ] |
| 3.H04 | Execution_Status | Single Select: SUCCESS / FAILURE / RETRY / SKIPPED | [ ] |
| 3.H05 | Failure_Count_1hr | Number | [ ] |
| 3.H06 | Last_Error_Code | Single Line Text | [ ] |
| 3.H07 | Health_Check_Result | Single Select: OK / WARNING / CRITICAL | [ ] |
| 3.H08 | Alert_Sent | Checkbox | [ ] |

**Section 3 Sign-Off:** [ ] All required fields confirmed present with correct types
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 4 — SANDBOX TEST RESULTS

All 13 test cases must have been executed in the sandbox environment with confirmed pass results. No test case may have a status of PARTIAL, SKIP, or DEFERRED. Each test result must be documented with a test data reference (TEST-[FUNCTION]-NNNN format) and signed off.

| # | Test Case | Scenario(s) Tested | Test Data Ref | Expected Result | Actual Result | Pass/Fail | Confirmed By | Date |
|---|-----------|-------------------|--------------|----------------|---------------|-----------|-------------|------|
| 4.01 | SSS lead intake — full brand routing to SSS | M-BRAND-ROUTER, M-LEAD-INTAKE | TEST-LEAD-0001 | Request record created with Brand = SSS, Slack alert to #sss-ops-alerts | | [ ] | | |
| 4.02 | ME lead intake — full brand routing to ME | M-BRAND-ROUTER, M-LEAD-INTAKE | TEST-LEAD-0002 | Request record created with Brand = ME, correct ME routing logic | | [ ] | | |
| 4.03 | Duplicate lead submission (same email, < 10 min) | M-LEAD-INTAKE | TEST-LEAD-0003 | Idempotency check blocks second record creation; first record updated | | [ ] | | |
| 4.04 | Concierge auto-assignment — standard SSS request | M-CONCIERGE-ASSIGNMENT | TEST-CONCIERGE-0001 | Broker assigned based on availability; Slack alert fired | | [ ] | | |
| 4.05 | Concierge assignment — HV_Client flag trigger | M-CONCIERGE-ASSIGNMENT | TEST-CONCIERGE-0002 | HV_Client = true routed to senior broker; additional Slack alert | | [ ] | | |
| 4.06 | Stripe deposit link creation | M-STRIPE-DEPOSIT | TEST-STRIPE-0001 | Stripe payment link created; Booking.Stripe_Deposit_Link populated | | [ ] | | |
| 4.07 | Stripe deposit webhook received — booking status update | M-STRIPE-DEPOSIT | TEST-STRIPE-0002 | Booking status → DEPOSIT_PAID; confirmation triggered | | [ ] | | |
| 4.08 | Booking record creation from confirmed request | M-BOOKING-CREATION | TEST-BOOKING-0001 | Booking record created with all required fields; linked to Request and Client | | [ ] | | |
| 4.09 | Booking confirmation email + Slack notification | M-BOOKING-CONFIRMATION | TEST-BOOKING-0002 | Confirmation email sent to test inbox; Slack alert to #sss-ops-alerts | | [ ] | | |
| 4.10 | Emergency_Flag = true — all automations halt | M-SLACK-ALERTS, HEALTH-001 | TEST-EMERGENCY-0001 | SEV-1 alert to Will DM + #sss-emergency-ops; all outbound paused | | [ ] | | |
| 4.11 | Audit Log entry written for every Tier A action | M-AUDIT-LOGGER | TEST-AUDIT-0001 | Every scenario that runs produces a corresponding AUD-YYYY-NNNN record | | [ ] | | |
| 4.12 | HEALTH-001 detects failure condition and alerts | HEALTH-001, M-SLACK-ALERTS | TEST-HEALTH-0001 | Deliberately inject failure; confirm HEALTH-001 detects and alerts within 15 min | | [ ] | | |
| 4.13 | Sandbox records never appear in production views | All scenarios | TEST-ENV-0001 | All sandbox records have Environment = Sandbox; production Airtable views exclude them | | [ ] | | |

**Section 4 Sign-Off:** [ ] All 13 test cases passed — no partial or deferred results
**Confirmed By (Will):** __________________ **Date:** __________________
**Confirmed By (Luciana):** __________________ **Date:** __________________

---

## SECTION 5 — AUDIT LOGGING VERIFICATION

Every Stage 1 scenario must write to the Audit Log before it is considered production-ready. This section verifies that each scenario's audit trail is complete and correct.

| # | Scenario | Audit Action Written | Audit_ID Format Correct | Idempotency_Key Present | Brand Field Correct | Environment Field Correct | Rollback_Linkage Present | Status |
|---|----------|--------------------|-----------------------|------------------------|--------------------|--------------------------|-----------------------|--------|
| 5.01 | M-BRAND-ROUTER | Brand routing decision logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.02 | M-LEAD-INTAKE | Request record creation logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.03 | M-SLACK-ALERTS | Alert send event logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.04 | M-CONCIERGE-ASSIGNMENT | Broker assignment decision logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.05 | M-STRIPE-DEPOSIT | Deposit link creation + webhook receipt logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.06 | M-BOOKING-CREATION | Booking record creation logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.07 | M-BOOKING-CONFIRMATION | Confirmation send logged | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 5.08 | M-AUDIT-LOGGER | Self-log (audit logger logs its own execution) | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

**Additional Audit Verification:**

| # | Check | Status |
|---|-------|--------|
| 5.09 | No Audit Log records exist with null Scenario_ID | [ ] |
| 5.10 | No Audit Log records exist with null Execution_Timestamp | [ ] |
| 5.11 | Audit Log is write-only from Make — no Make module reads and overwrites existing records | [ ] |
| 5.12 | Audit Log field permissions prevent human editing of Execution_Timestamp | [ ] |

**Section 5 Sign-Off:** [ ] All scenarios confirmed to write correctly to Audit Log
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 6 — DUPLICATE PREVENTION VERIFICATION

Idempotency is the prevention of duplicate execution when a scenario retries. Each scenario that creates a record or sends a message must have a confirmed idempotency check that has been tested with a forced retry.

| # | Scenario | Idempotency Key Format | Check Location | Duplicate Blocked in Test | Status |
|---|----------|----------------------|----------------|--------------------------|--------|
| 6.01 | M-LEAD-INTAKE | `LEAD-INTAKE-{{email_hash}}-{{epoch}}` | Requests.Idempotency_Key lookup before record creation | [ ] | [ ] |
| 6.02 | M-BOOKING-CREATION | `BOOKING-CREATION-{{request_id}}-{{epoch}}` | Bookings.Idempotency_Key lookup before record creation | [ ] | [ ] |
| 6.03 | M-STRIPE-DEPOSIT | `STRIPE-DEPOSIT-{{booking_id}}-{{stripe_event_id}}` | Automation_Health lookup before processing | [ ] | [ ] |
| 6.04 | M-BOOKING-CONFIRMATION | `BOOKING-CONF-{{booking_id}}-{{epoch}}` | Automation_Health.Confirmation_Sent_At null check | [ ] | [ ] |
| 6.05 | M-CONCIERGE-ASSIGNMENT | `CONCIERGE-{{request_id}}-{{epoch}}` | Requests.Concierge_Assigned null check | [ ] | [ ] |
| 6.06 | M-SLACK-ALERTS | `ALERT-{{scenario_id}}-{{record_id}}-{{epoch_hour}}` | Automation_Health.Alert_Sent check (per hour dedup) | [ ] | [ ] |

**Idempotency Test Protocol:** For each scenario above, the test must include deliberately re-submitting the trigger event (replaying the webhook or re-creating the trigger condition). The test passes only if the second execution produces no duplicate record and no duplicate outbound message.

**Section 6 Sign-Off:** [ ] All scenarios confirmed idempotent under forced retry conditions
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 7 — ERROR HANDLING VERIFICATION

All four error levels from the Make error handling standard must be tested for each production scenario. A scenario that fails gracefully at level 1 but crashes at level 3 is not production-ready.

**Error Level Reference:**

| Level | Trigger | Expected Behavior |
|-------|---------|-------------------|
| L1 — First Failure | Single execution failure | Log to Automation_Failures; retry after 2 minutes |
| L2 — Second Failure | Retry fails | Retry after 5 minutes; increment failure count |
| L3 — Third Failure | Third consecutive failure | Slack alert to Luciana via #sss-ops-alerts |
| L4 — Fourth Failure | Fourth consecutive failure | Slack DM to Will; scenario pauses; create Founder Decision: SEV-2 |

| # | Scenario | L1 Tested & Passes | L2 Tested & Passes | L3 Alert Received | L4 Alert Received | Scenario Pauses at L4 | Founder Decision Created at L4 | Status |
|---|----------|--------------------|--------------------|--------------------|-------------------|----------------------|-------------------------------|--------|
| 7.01 | M-BRAND-ROUTER | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.02 | M-LEAD-INTAKE | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.03 | M-SLACK-ALERTS | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.04 | M-CONCIERGE-ASSIGNMENT | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.05 | M-STRIPE-DEPOSIT | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.06 | M-BOOKING-CREATION | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.07 | M-BOOKING-CONFIRMATION | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |
| 7.08 | M-AUDIT-LOGGER | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] | [ ] |

**Note on M-AUDIT-LOGGER failures:** If M-AUDIT-LOGGER itself fails, this is automatically classified as a potential SEV-1 (Audit Log gap). The error handling for M-AUDIT-LOGGER must escalate directly to SEV-2 on first failure, not after four attempts.

**Section 7 Sign-Off:** [ ] All four error levels tested for all eight scenarios
**Confirmed By:** __________________ **Date:** __________________

---

## SECTION 8 — ROLLBACK VALIDATION

Every Stage 1 scenario must have a confirmed rollback procedure. The rollback procedure must be documented in the Deployment Log and must have been tested in sandbox before this checklist is signed. A rollback that has never been run is not a rollback — it is a theory.

| # | Scenario | Rollback Action | Rollback Tested in Sandbox | Rollback Time (Estimated) | Rollback Documented in Deployment Log | Status |
|---|----------|----------------|--------------------------|--------------------------|--------------------------------------|--------|
| 8.01 | M-BRAND-ROUTER | Deactivate scenario; manually re-route Requests by updating Brand_Routed field in Airtable | [ ] | < 5 min | [ ] | [ ] |
| 8.02 | M-LEAD-INTAKE | Deactivate scenario; manually create Request records from form submissions received in Gmail | [ ] | < 10 min | [ ] | [ ] |
| 8.03 | M-SLACK-ALERTS | Deactivate scenario; Will and Luciana monitor Airtable directly for emergency and escalation flags | [ ] | < 2 min | [ ] | [ ] |
| 8.04 | M-CONCIERGE-ASSIGNMENT | Deactivate scenario; Luciana manually assigns concierge from Airtable Requests view | [ ] | < 5 min | [ ] | [ ] |
| 8.05 | M-STRIPE-DEPOSIT | Deactivate scenario; manually generate Stripe payment links from Stripe dashboard; share via email | [ ] | < 15 min | [ ] | [ ] |
| 8.06 | M-BOOKING-CREATION | Deactivate scenario; Luciana manually creates Booking records from confirmed Requests | [ ] | < 10 min | [ ] | [ ] |
| 8.07 | M-BOOKING-CONFIRMATION | Deactivate scenario; Luciana manually sends confirmation email from Gmail template | [ ] | < 10 min | [ ] | [ ] |
| 8.08 | M-AUDIT-LOGGER | Deactivate scenario; all other scenarios pause until M-AUDIT-LOGGER is restored (no Tier A actions without audit trail) | [ ] | < 2 min | [ ] | [ ] |

**Rollback Authorization Protocol:**

| Check | Status |
|-------|--------|
| Will has been briefed on every rollback procedure and can execute each within their stated time | [ ] |
| Luciana has been briefed on every rollback procedure within her operational scope | [ ] |
| Rollback decision authority is clear: Luciana for SEV-3/SEV-4; Will for SEV-1/SEV-2 | [ ] |
| All rollback procedures are documented in the Deployment Log before go-live | [ ] |

**Section 8 Sign-Off:** [ ] All rollback procedures documented, tested, and understood by Will and Luciana
**Confirmed By (Will):** __________________ **Date:** __________________
**Confirmed By (Luciana):** __________________ **Date:** __________________

---

## SECTION 9 — SLACK ALERT VERIFICATION

Every alert type must have been successfully sent to the correct Slack channel or DM and received by the correct person. "Confirmed received" means the recipient explicitly acknowledged the test message in the channel/DM.

| # | Alert Type | Triggered By | Expected Channel | Confirmed Delivered | Received By | Status |
|---|-----------|-------------|-----------------|--------------------| ------------|--------|
| 9.01 | Lead received (new SSS inquiry) | M-LEAD-INTAKE | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.02 | Lead received (new ME inquiry) | M-LEAD-INTAKE | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.03 | Concierge assigned | M-CONCIERGE-ASSIGNMENT | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.04 | Deposit received | M-STRIPE-DEPOSIT | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.05 | Booking confirmed | M-BOOKING-CONFIRMATION | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.06 | SEV-2 automation failure | HEALTH-001 / M-SLACK-ALERTS | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.07 | Emergency_Flag detected (SEV-1) | HEALTH-001 / M-SLACK-ALERTS | #sss-emergency-ops + Will DM | [ ] | Will confirmed | [ ] |
| 9.08 | Audit Log gap detected (SEV-1) | HEALTH-001 | Will DM + #sss-emergency-ops | [ ] | Will confirmed | [ ] |
| 9.09 | Stripe webhook latency > 5 min | HEALTH-001 | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.10 | Backup overdue > 48 hours | HEALTH-001 | #sss-ops-alerts | [ ] | Luciana confirmed | [ ] |
| 9.11 | HEALTH-001 offline (failsafe alert) | HEALTH-FAILSAFE | Will DM + #sss-emergency-ops | [ ] | Will confirmed | [ ] |

**Section 9 Sign-Off:** [ ] All 11 alert types confirmed delivered and acknowledged in correct channels
**Confirmed By (Will):** __________________ **Date:** __________________
**Confirmed By (Luciana):** __________________ **Date:** __________________

---

## SECTION 10 — COMMUNICATION SAFETY

Before go-live, every outbound communication pathway must be confirmed safe — meaning test runs cannot reach real clients. This section verifies that all test data uses internal email addresses, internal phone numbers, and that no scenario can accidentally pull a real client record during testing.

| # | Check | Status |
|---|-------|--------|
| 10.01 | All sandbox Airtable records have Environment = Sandbox | [ ] |
| 10.02 | All sandbox test records use test email addresses (@shesaidsail.com internal or a dedicated test domain) | [ ] |
| 10.03 | All sandbox test records use a designated test phone number (not a real client number) | [ ] |
| 10.04 | Gmail module in sandbox scenarios is connected to a test Gmail account, not hello@shesaidsail.com | [ ] |
| 10.05 | Quo SMS module in sandbox scenarios uses a test SID / test mode — no real SMS can be sent | [ ] |
| 10.06 | Production Make scenarios include an Environment gate: first step reads Environment field; exits if value = Sandbox | [ ] |
| 10.07 | Production Airtable views are filtered to Environment = Production only — sandbox records are not visible in ops views | [ ] |
| 10.08 | No real client email addresses appear in any sandbox test record | [ ] |
| 10.09 | No real client phone numbers appear in any sandbox test record | [ ] |
| 10.10 | Luciana has reviewed and confirmed the sandbox test data inventory contains zero real client PII | [ ] |

**Section 10 Sign-Off:** [ ] Communication safety confirmed — no test execution can reach a real client
**Confirmed By (Will):** __________________ **Date:** __________________
**Confirmed By (Luciana):** __________________ **Date:** __________________

---

## SECTION 11 — STRIPE TEST MODE VALIDATION

Stripe has two modes: test mode and live mode. Every Stripe interaction in sandbox must use test mode keys, test payment method tokens, and Stripe's test webhook CLI. No live Stripe key may appear in a sandbox Make scenario.

| # | Check | Status |
|---|-------|--------|
| 11.01 | Sandbox Make connection to Stripe uses test-mode Secret Key (sk_test_...) | [ ] |
| 11.02 | Production Make connection to Stripe uses live-mode Secret Key (sk_live_...) | [ ] |
| 11.03 | Test deposit flow executed end-to-end using Stripe test card (4242 4242 4242 4242) | [ ] |
| 11.04 | Stripe test webhook event received by Make and processed correctly | [ ] |
| 11.05 | Booking status updated correctly (→ DEPOSIT_PAID) after test webhook received | [ ] |
| 11.06 | Stripe metadata fields populated correctly: sss_booking_id, sss_request_id (or me_booking_id, me_request_id for ME) | [ ] |
| 11.07 | Test mode payment link created and opened in browser — shows Stripe test mode banner | [ ] |
| 11.08 | No live-mode Stripe key appears in any sandbox scenario module | [ ] |
| 11.09 | Stripe webhook signing secret for sandbox is different from production signing secret | [ ] |
| 11.10 | Will has reviewed test Stripe dashboard and confirmed test payment appears correctly | [ ] |

**Section 11 Sign-Off:** [ ] Stripe test mode validation complete — end-to-end deposit flow confirmed
**Confirmed By (Will):** __________________ **Date:** __________________

---

## SECTION 12 — FOUNDER APPROVAL

Will must personally review and approve each of the eight Stage 1 scenarios before go-live. Approval is not delegable. Luciana may brief Will and prepare the review session, but the approval record requires Will's direct confirmation.

**Review Protocol:** Will reviews the scenario's Make execution diagram, the test case results, the audit log output from sandbox runs, and the rollback procedure. Approval is recorded here and in the Deployment Log.

| # | Scenario | Review Session Completed | Key Decisions Reviewed | Approved | Approval Date | Founder Decision Record # |
|---|----------|-------------------------|-----------------------|---------|--------------|--------------------------|
| 12.01 | M-BRAND-ROUTER | [ ] | Routing logic, brand classification criteria, failure behavior | [ ] | | |
| 12.02 | M-LEAD-INTAKE | [ ] | Form field mapping, record creation, duplicate prevention | [ ] | | |
| 12.03 | M-SLACK-ALERTS | [ ] | Alert routing, message templates, severity classification | [ ] | | |
| 12.04 | M-CONCIERGE-ASSIGNMENT | [ ] | Assignment logic, HV_Client routing, escalation path | [ ] | | |
| 12.05 | M-STRIPE-DEPOSIT | [ ] | Payment link creation, webhook handling, metadata fields | [ ] | | |
| 12.06 | M-BOOKING-CREATION | [ ] | Record creation logic, field mapping, linked records | [ ] | | |
| 12.07 | M-BOOKING-CONFIRMATION | [ ] | Confirmation message content, send trigger, audit trail | [ ] | | |
| 12.08 | M-AUDIT-LOGGER | [ ] | Audit field spec, write timing, immutability controls | [ ] | | |

**Additional Founder Approvals Required:**

| # | Item | Approved | Date |
|---|------|---------|------|
| 12.09 | HEALTH-001 monitoring thresholds and alert routing matrix | [ ] | |
| 12.10 | Production Airtable schema (all required fields confirmed present) | [ ] | |
| 12.11 | Rollback procedures for all 8 scenarios | [ ] | |
| 12.12 | Go-live date and time (business hours only — not during active charter) | [ ] | |

**Section 12 Sign-Off:** [ ] Will has reviewed and approved all eight scenarios and all additional items
**Will's Signature:** __________________ **Date:** __________________

---

## SECTION 13 — DEPLOYMENT LOG

Every scenario activation must be logged in the Deployment Log table (Airtable → SSS Operations base). This section confirms the log entries have been created.

| # | Scenario | Deployment Log Record Created | Deployment Log Record # | Activated By | Activation Timestamp | Status |
|---|----------|------------------------------|------------------------|-------------|---------------------|--------|
| 13.01 | M-BRAND-ROUTER | [ ] | | Will | | [ ] |
| 13.02 | M-LEAD-INTAKE | [ ] | | Will | | [ ] |
| 13.03 | M-SLACK-ALERTS | [ ] | | Will | | [ ] |
| 13.04 | M-CONCIERGE-ASSIGNMENT | [ ] | | Will | | [ ] |
| 13.05 | M-STRIPE-DEPOSIT | [ ] | | Will | | [ ] |
| 13.06 | M-BOOKING-CREATION | [ ] | | Will | | [ ] |
| 13.07 | M-BOOKING-CONFIRMATION | [ ] | | Will | | [ ] |
| 13.08 | M-AUDIT-LOGGER | [ ] | | Will | | [ ] |
| 13.09 | HEALTH-001 | [ ] | | Will | | [ ] |
| 13.10 | HEALTH-FAILSAFE | [ ] | | Will | | [ ] |

**Deployment Log Required Fields Per Record:**

| Field | Required Value |
|-------|---------------|
| Scenario_ID | M-[FUNCTION]-[MODIFIER] format |
| Deployed_By | Will (Founder) |
| Deployed_At | Exact timestamp |
| Environment | Production |
| Rollback_Procedure_Reference | Link to this document, Section 8 |
| Prior_Version | N/A for initial deployment |
| Sandbox_Test_Ref | TEST-[FUNCTION]-NNNN reference |
| Founder_Decision_Ref | Founder Decision record # from Section 12 |

**Section 13 Sign-Off:** [ ] All 10 scenarios have Deployment Log records
**Confirmed By (Will):** __________________ **Date:** __________________

---

## FINAL VERDICT

> This section is completed last. It cannot be signed until all 13 sections above are complete and signed.

**Checklist Completion Count:** _____ / 13 sections signed

**Open Items Count:** _____

**Conditional Passes (any item marked as "acceptable risk" or deferred):** _____

---

### READY FOR LIVE LEADS

**Condition:** All 13 sections signed. Zero open items. Zero conditional passes.

[ ] **I, Will (Founder), confirm that all 13 sections of this checklist are complete, all items have been verified by the responsible parties, and Stage 1 Make scenarios are authorized to receive and process real client leads as of the date below.**

**Authorized By (Will):** __________________ **Date and Time:** __________________

---

### READY WITH WARNINGS

**Condition:** All 13 sections signed. One or more items have documented acceptable risk, approved by Will. No critical safety or data integrity items are open.

[ ] **I, Will (Founder), confirm that Stage 1 may proceed with the following documented warnings:**

Warning 1: _______________________________________________
Warning 2: _______________________________________________
Warning 3: _______________________________________________

Mitigation for each warning: _______________________________________________

**Authorized By (Will):** __________________ **Date and Time:** __________________

---

### NOT READY

**Condition:** Any of the following are true: incomplete sections, open critical items, failed test cases, missing Founder Approval, Stripe live mode not validated, Communication Safety not confirmed.

[ ] **Stage 1 is NOT authorized for live client leads. The following blockers must be resolved:**

Blocker 1: _______________________________________________
Blocker 2: _______________________________________________
Blocker 3: _______________________________________________

**Target Completion Date:** __________________
**Next Checklist Review:** __________________

---

*End of PRODUCTION_GO_LIVE_CHECKLIST*
*Version 1.0 — This document must be re-executed for each major Stage deployment*
*Archive this completed checklist in the Deployment Log and in GitHub under 02_SYSTEMS_AUTOMATIONS/STAGE_1_MAKE_IMPLEMENTATION/*
