# STAGE 1 TEST RESULTS — TRACKER AND TEMPLATE
**Project:** She Said Sail + Mare Executive — Make.com Automation System
**Base (Production):** appdZ49WqgjRXxA1R
**Prepared by:** Production Reliability Engineering
**Date Prepared:** 2026-05-16
**Document Status:** PRE-POPULATED — AWAITING MAKE BUILD AND SANDBOX EXECUTION
**Stage:** Stage 1 (8 core scenarios)

---

> **IMPORTANT — BUILD STATUS AS OF 2026-05-16**
>
> Make.com scenario builds have NOT yet been started. This document is the pre-populated test framework, written during the documentation phase so testing can proceed immediately once the Make build phase is complete. ALL tests below are status NOT RUN. No sandbox has been configured. No test payloads have been submitted. The Stripe environment is TEST MODE — no live charges will occur at any point during Stage 1 testing.
>
> No client emails or SMS messages are sent during Stage 1. Luciana sends all client communications manually. All automated email/SMS sends during testing go exclusively to internal test addresses.
>
> 9 blockers (BLK-001 through BLK-009) must be resolved before testing begins. See STAGE_1_BLOCKER_RESOLUTION_REPORT.md for resolution procedures.

---

## TEST RUN HEADER TEMPLATE

Complete this header at the start of every test run. File one signed copy per test run date.

```
TEST RUN — STAGE 1 MAKE.COM SCENARIOS
=======================================
Test Run Date:           _______________
Test Run Start Time:     _______________
Test Run End Time:       _______________
Primary Tester:          Luciana
Witness / Co-tester:     Will (required for T-004, T-009, T-013 Level 4 alerts)

Environment:             SANDBOX — NOT PRODUCTION
Airtable Sandbox Base:   [ID of Sandbox base — NOT appdZ49WqgjRXxA1R]
Stripe Mode:             TEST MODE (sk_test_ key confirmed active)
Make Scenario Folder:    She Said Sail / Stage 1 / SANDBOX

Make Scenario Versions Tested:
  M-BRAND-ROUTER:           v ___________
  M-LEAD-INTAKE:            v ___________
  M-SLACK-ALERTS:           v ___________
  M-CONCIERGE-ASSIGNMENT:   v ___________
  M-STRIPE-DEPOSIT:         v ___________
  M-BOOKING-CREATION:       v ___________
  M-BOOKING-CONFIRMATION:   v ___________
  M-AUDIT-LOGGER:           v ___________

Pre-Test Sandbox Reset Confirmed:
  [ ] All prior test records deleted from Sandbox Airtable base
  [ ] Open Stripe test payment intents cancelled
  [ ] Audit_Log sandbox records cleared
  [ ] Automation_Failures sandbox records cleared
  [ ] Make scenario execution history shows no pending runs
  [ ] Automations_Paused = FALSE confirmed in Automation_Health

Luciana pre-test sign-off: ________________________  Time: _______________
```

---

## TEST SUMMARY TABLE

| Test ID | Test Name | Test Type | Scenarios Exercised | Status | Pass/Fail |
|---------|-----------|-----------|---------------------|--------|-----------|
| T-001 | Fake Lead — SSS Brand Full Pipeline | Integration | All 8 | NOT RUN | — |
| T-002 | Fake Lead — ME Brand Full Pipeline | Integration | All 8 | NOT RUN | — |
| T-003 | Fake Booking Record Creation | Unit | M-BOOKING-CREATION, M-AUDIT-LOGGER | NOT RUN | — |
| T-004 | Stripe Test-Mode Deposit Session | Unit | M-STRIPE-DEPOSIT, M-AUDIT-LOGGER | NOT RUN | — |
| T-005 | Duplicate Submission Rejected | Edge Case | M-BRAND-ROUTER, M-LEAD-INTAKE | NOT RUN | — |
| T-006 | Missing-Field Payload Handled | Edge Case | M-BRAND-ROUTER, M-LEAD-INTAKE | NOT RUN | — |
| T-007 | Malformed JSON Rejected | Failure Path | M-BRAND-ROUTER | NOT RUN | — |
| T-008 | Webhook Replay Rejected (>5 min) | Failure Path | M-BRAND-ROUTER, M-LEAD-INTAKE | NOT RUN | — |
| T-009 | Forced Airtable Failure — 4-Level Error Chain | Failure Path | M-LEAD-INTAKE, M-AUDIT-LOGGER, M-SLACK-ALERTS | NOT RUN | — |
| T-010 | Rollback — Scenario Disabled, Data Integrity Preserved | Failure Path | M-BOOKING-CREATION | NOT RUN | — |
| T-011 | Audit Log Verification — All Scenarios | Integration | M-AUDIT-LOGGER (all callers) | NOT RUN | — |
| T-012 | Automation Health Record Verification | Unit | All scenarios (health check step) | NOT RUN | — |
| T-013 | Slack Alert Verification — All Alert Types | Unit | M-SLACK-ALERTS | NOT RUN | — |

**Required pass rate before Production promotion: 13/13 (100%). No partial credit. No exceptions.**

---

## TEST RECORDS

---

### T-001 — Fake Lead Test: SSS Brand Full Pipeline

| Field | Value |
|-------|-------|
| **Test ID** | T-001 |
| **Test Name** | Fake Lead — She Said Sail Brand Full Pipeline |
| **Test Type** | Integration |
| **Scenarios Exercised** | M-BRAND-ROUTER → M-LEAD-INTAKE → M-SLACK-ALERTS → M-CONCIERGE-ASSIGNMENT → M-AUDIT-LOGGER |
| **Estimated Duration** | 15–30 minutes |
| **Will Present Required** | No (Luciana primary) |

**Pre-Conditions Required:**
- [ ] All 9 blockers (BLK-001 through BLK-009) resolved
- [ ] Sandbox Airtable base configured with correct schema (identical to production)
- [ ] Environment field present and defaulting to `sandbox` on all Sandbox base tables
- [ ] Automations_Paused = FALSE in Sandbox Automation_Health control record
- [ ] Make SSS_AIRTABLE_PAT connection verified (HTTP 200 on test GET)
- [ ] SSS_SLACK_BOT invited to #sss-ops-alerts
- [ ] At least one active Concierge_Operators record in Sandbox base
- [ ] Sandbox reset completed per Test Run Header protocol

**Test Data — Exact Payload to POST:**
```json
{
  "submission_id": "WEBFLOW-TEST-SSS-001",
  "submitted_at": "2026-05-16T22:00:00Z",
  "form_name": "SSS Charter Inquiry",
  "brand": "SSS",
  "lead": {
    "first_name": "Alexandra",
    "last_name": "Testclient",
    "email": "ops-test+sss@shesaidsail.com",
    "phone": "+13055550100",
    "preferred_contact": "email"
  },
  "inquiry": {
    "charter_type": "Private Luxury Charter",
    "preferred_date": "2026-07-15",
    "preferred_date_alternate": "2026-07-22",
    "group_size": 8,
    "duration_hours": 4,
    "city": "Miami",
    "occasion": "Birthday",
    "catering_interest": true,
    "budget_range": "$2,500 - $5,000",
    "how_heard": "Instagram",
    "notes": "TEST SUBMISSION — DO NOT PROCESS AS REAL LEAD"
  },
  "metadata": {
    "source": "Webflow",
    "ip_address": "192.0.2.1",
    "user_agent": "Make-Test-Agent/1.0"
  }
}
```
**Delivery method:** POST to WHK-SSS-LEAD-INTAKE-SANDBOX with valid Bearer token and current timestamp.

**Expected Outcome (all must be true):**
1. M-BRAND-ROUTER receives payload; routes to SSS pipeline; no errors in Make execution log
2. Requests table: new record created with `Brand = SSS`, `Environment = sandbox`, `Idempotency_Key` non-null, all inquiry fields populated
3. Clients table: new record created for Alexandra Testclient with email `ops-test+sss@shesaidsail.com`; linked to Request record
4. M-SLACK-ALERTS: message received in #sss-ops-alerts within 60 seconds; contains "Alexandra Testclient" and "SSS"
5. M-CONCIERGE-ASSIGNMENT: `Assigned_Concierge` field populated on the Request record; `Assigned_At` timestamp present
6. M-AUDIT-LOGGER: at least 4 Audit_Log entries from this run, one per scenario that executed, each with non-null `Scenario_Name`, `Execution_ID`, `Created_At`
7. Automation_Failures table: 0 new records after this run

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Make Execution IDs** | [TO BE FILLED — copy from Make execution history] |
| **Airtable Request Record ID** | [TO BE FILLED] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-002 — Fake Lead Test: ME Brand Full Pipeline

| Field | Value |
|-------|-------|
| **Test ID** | T-002 |
| **Test Name** | Fake Lead — Mare Executive Brand Full Pipeline |
| **Test Type** | Integration |
| **Scenarios Exercised** | M-BRAND-ROUTER → M-LEAD-INTAKE → M-SLACK-ALERTS → M-CONCIERGE-ASSIGNMENT → M-AUDIT-LOGGER |
| **Estimated Duration** | 15–30 minutes |
| **Will Present Required** | No (Luciana primary) |
| **Prerequisite** | T-001 must have passed |

**Pre-Conditions Required:**
- [ ] All pre-conditions from T-001 remain satisfied
- [ ] ME brand Slack channel confirmed (or ME label routing in #sss-ops-alerts confirmed per SA-002 issue resolution)
- [ ] ME concierge assignment rules documented and at least one ME-capable operator in Concierge_Operators table
- [ ] Sandbox reset completed (do not reuse T-001 sandbox state)

**Test Data — Exact Payload to POST:**
```json
{
  "submission_id": "WEBFLOW-TEST-ME-001",
  "submitted_at": "2026-05-16T22:05:00Z",
  "form_name": "ME Executive Charter Inquiry",
  "brand": "ME",
  "lead": {
    "first_name": "Jonathan",
    "last_name": "Testexec",
    "email": "ops-test+me@shesaidsail.com",
    "phone": "+13055550200",
    "company": "Test Corp LLC",
    "role": "CEO",
    "preferred_contact": "phone"
  },
  "inquiry": {
    "charter_type": "Corporate Executive Charter",
    "preferred_date": "2026-07-20",
    "preferred_date_alternate": "2026-07-27",
    "group_size": 12,
    "duration_hours": 6,
    "city": "Miami",
    "occasion": "Client Entertainment",
    "catering_interest": true,
    "av_requirements": true,
    "budget_range": "$10,000+",
    "how_heard": "LinkedIn",
    "notes": "TEST SUBMISSION — DO NOT PROCESS AS REAL LEAD"
  },
  "metadata": {
    "source": "Webflow",
    "ip_address": "192.0.2.2",
    "user_agent": "Make-Test-Agent/1.0"
  }
}
```
**Delivery method:** POST to WHK-ME-LEAD-INTAKE-SANDBOX with valid Bearer token and current timestamp.

**Expected Outcome (all must be true):**
1. M-BRAND-ROUTER: payload routed to ME pipeline; `Brand = ME` confirmed in routing context
2. Requests table: new record with `Brand = ME`, `Environment = sandbox`, `company` and `role` fields populated
3. Clients table: new Client record for Jonathan Testexec; linked to Request
4. Slack alert: routed to correct ME channel (or #sss-ops-alerts with ME brand label — per SA-002 resolution); message contains "ME" brand label
5. Concierge assignment: ME-appropriate concierge assigned; `Assigned_At` populated
6. Audit_Log: minimum 4 entries with `Brand = ME` context; no SSS brand confusion in log
7. Zero records in Automation_Failures after this run
8. CRITICAL CHECK: No SSS-branded content anywhere in the ME record or alerts

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Make Execution IDs** | [TO BE FILLED] |
| **Airtable Request Record ID** | [TO BE FILLED] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-003 — Fake Booking Record Creation

| Field | Value |
|-------|-------|
| **Test ID** | T-003 |
| **Test Name** | Fake Booking — Booking Record Creation Verification |
| **Test Type** | Unit |
| **Scenarios Exercised** | M-BOOKING-CREATION, M-AUDIT-LOGGER |
| **Estimated Duration** | 10–20 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] T-001 completed and passed (produces the Sandbox Request and Client records this test depends on)
- [ ] Deposit_Paid = TRUE manually set on the T-001 Request record in Sandbox
- [ ] BLK-007 resolved (circular trigger guard implemented)
- [ ] BLK-002 resolved (Idempotency_Key field exists on Bookings table)
- [ ] At least one Yacht record exists in Sandbox Packages/Yachts table
- [ ] Needs_Make_Processing trigger field present on Bookings table (per BLK-007 resolution)

**Test Procedure:**
1. Open T-001 Request record in Sandbox Airtable base
2. Confirm `Deposit_Paid = TRUE`
3. Set `Needs_Make_Processing = "process"` on the Request record to trigger M-BOOKING-CREATION
4. Wait up to 60 seconds; monitor Make execution log for M-BOOKING-CREATION run

**Expected Outcome (all must be true):**
1. M-BOOKING-CREATION fires exactly once (check Make history — confirm no cascade of runs)
2. Bookings table: new record created with `Environment = sandbox`
3. Booking record fields: `Status` = correct initial status (CONFIRMED or DEPOSIT_PAID per spec); `Client` linked to T-001 Client record; `Yacht` linked; `Package` linked
4. `Idempotency_Key` field on Booking: non-null, SHA-256 format
5. `Make_Processing` field on Bookings: returns to FALSE after scenario completes
6. No second Booking record created if trigger is observed twice
7. Audit_Log: one entry with `Scenario_Name = M-BOOKING-CREATION` and correct `Execution_ID`
8. Zero records in Automation_Failures

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Booking Record ID Created** | [TO BE FILLED] |
| **Idempotency_Key Value** | [TO BE FILLED — record for audit] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-004 — Stripe Test-Mode Deposit Session Creation

| Field | Value |
|-------|-------|
| **Test ID** | T-004 |
| **Test Name** | Stripe Test-Mode Deposit — Payment Intent Creation and URL Return |
| **Test Type** | Unit |
| **Scenarios Exercised** | M-STRIPE-DEPOSIT, M-AUDIT-LOGGER |
| **Estimated Duration** | 20–40 minutes |
| **Will Present Required** | YES — Stripe test operations require Will present |

**Pre-Conditions Required:**
- [ ] BLK-008 resolved (Stripe webhook URL generated and registered in Stripe test dashboard)
- [ ] `SSS_STRIPE_TEST_SECRET` connection verified in Make (sk_test_ prefix confirmed)
- [ ] `SSS_STRIPE_WEBHOOK_SECRET_TEST` stored in Make Data Store
- [ ] Stripe signature validation module present in M-STRIPE-DEPOSIT (step 1)
- [ ] Stripe test-mode email notifications DISABLED in Stripe dashboard settings
- [ ] Packages table exists in Sandbox base with at least one record including a price field
- [ ] T-001 Request record available in Sandbox with correct Package linkage

**Test Procedure:**
1. Confirm Stripe dashboard is in TEST MODE (verify "TEST DATA" banner visible)
2. Trigger M-STRIPE-DEPOSIT via the internal call from M-LEAD-INTAKE flow, or manually set the Request status field to the trigger condition
3. Confirm Make execution log shows M-STRIPE-DEPOSIT run
4. In Stripe dashboard (Test Mode → Payments), confirm new Payment Intent or Checkout Session appears
5. Use Stripe test card `4242 4242 4242 4242` (exp: any future date, CVV: any 3 digits) to simulate payment
6. Verify Stripe fires `payment_intent.succeeded` or `checkout.session.completed` webhook to Make webhook URL
7. Confirm Make receives and processes the Stripe webhook event

**Expected Outcome (all must be true):**
1. Stripe test Payment Intent or Checkout Session created; `livemode = false` in Stripe object (CRITICAL — verify this field)
2. Payment Intent amount in cents matches expected deposit (e.g., 30% of package price × 100 for cents)
3. Currency = correct value for the booking (confirm per SD-006 resolution — currency assumption documented)
4. Stripe metadata on the Payment Intent includes: `airtable_request_id`, `brand`, `environment = sandbox`
5. Make webhook URL receives the `payment_intent.succeeded` event from Stripe
6. Stripe signature validation in Make: passes (no HTTP 400 returned to Stripe)
7. Stripe dashboard shows event delivery status = "Delivered" (HTTP 200)
8. Airtable Sandbox Request record updated: `Deposit_Paid = TRUE`, `Deposit_Amount` populated, `Stripe_Payment_Intent_ID` populated
9. Audit_Log: one entry with `Scenario_Name = M-STRIPE-DEPOSIT`
10. Zero `Automation_Failures` records after this run
11. CRITICAL: No live charges on any real credit card — verify Stripe dashboard confirms `livemode = false`

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Will Present — Confirmed** | [TO BE FILLED — Yes / No] |
| **Date / Time** | [TO BE FILLED] |
| **Stripe Payment Intent ID (test)** | [TO BE FILLED — pi_test_...] |
| **Stripe Event ID (test)** | [TO BE FILLED — evt_test_...] |
| **Deposit Amount (cents)** | [TO BE FILLED] |
| **livemode field value** | [TO BE FILLED — must be false] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-005 — Duplicate Submission: Second Webhook Rejected

| Field | Value |
|-------|-------|
| **Test ID** | T-005 |
| **Test Name** | Duplicate Submission — Second Webhook with Same Payload Rejected |
| **Test Type** | Edge Case |
| **Scenarios Exercised** | M-BRAND-ROUTER, M-LEAD-INTAKE |
| **Estimated Duration** | 10 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] T-001 completed (SSS test Request record exists in Sandbox)
- [ ] Idempotency check implemented in M-BRAND-ROUTER or M-LEAD-INTAKE (per architecture spec)
- [ ] Sandbox base accessible

**Test Procedure:**
1. POST the T-001 SSS payload (submission_id: WEBFLOW-TEST-SSS-001) a second time to WHK-SSS-LEAD-INTAKE-SANDBOX
2. Use identical payload — same submission_id, same email, same all fields
3. Submit within 30 seconds of T-001 completion (or immediately if running as standalone)
4. Wait 60 seconds; check Make execution log and Airtable

**Expected Outcome (all must be true):**
1. Make shows two scenario execution runs (one for each POST)
2. Second run: execution terminates at idempotency check step — no further modules execute
3. Requests table: record count for `submission_id = WEBFLOW-TEST-SSS-001` remains exactly 1
4. No second Client record created for Alexandra Testclient
5. No second Slack alert fired (check #sss-ops-alerts message count)
6. Audit_Log: second run produces an entry with `Event_Type = DUPLICATE_PREVENTED` (or equivalent)
7. Zero unintended records in any table

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Request Record Count After Test** | [TO BE FILLED — must be 1] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-006 — Missing-Field Test: Incomplete Payload Handled Gracefully

| Field | Value |
|-------|-------|
| **Test ID** | T-006 |
| **Test Name** | Missing-Field Test — Incomplete Payload Handled Gracefully |
| **Test Type** | Edge Case |
| **Scenarios Exercised** | M-BRAND-ROUTER, M-LEAD-INTAKE |
| **Estimated Duration** | 10 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] Sandbox reset (clean state — no prior test records)
- [ ] Input validation module confirmed present in M-BRAND-ROUTER or M-LEAD-INTAKE

**Test Data — Payload with `email` field removed:**
```json
{
  "submission_id": "WEBFLOW-TEST-SSS-NOEMAIL",
  "submitted_at": "2026-05-16T22:10:00Z",
  "form_name": "SSS Charter Inquiry",
  "brand": "SSS",
  "lead": {
    "first_name": "Alexandra",
    "last_name": "Testclient",
    "phone": "+13055550100",
    "preferred_contact": "email"
  },
  "inquiry": {
    "charter_type": "Private Luxury Charter",
    "preferred_date": "2026-07-15",
    "group_size": 8,
    "notes": "TEST — MISSING EMAIL FIELD"
  },
  "metadata": {
    "source": "Webflow",
    "ip_address": "192.0.2.1",
    "user_agent": "Make-Test-Agent/1.0"
  }
}
```

**Expected Outcome (all must be true):**
1. Scenario execution reaches validation step; terminates gracefully (no unhandled exception)
2. Make returns HTTP 200 to the sending system (not 500 — a 500 causes the sender to retry indefinitely)
3. Zero Request records created in Sandbox base
4. Zero Client records created
5. Automation_Failures table: one new record with `Error_Code = MISSING_REQUIRED_FIELD` (or equivalent), `Field_Name` indicates `email`
6. Slack alert sent to Luciana in #sss-ops-alerts notifying of the rejected submission
7. Audit_Log: one entry noting the rejected submission and reason

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **HTTP Response Returned to Sender** | [TO BE FILLED — must be 200] |
| **Automation_Failures Record ID** | [TO BE FILLED] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-007 — Bad-Payload Test: Malformed JSON Rejected with HTTP 400 / Graceful Handling

| Field | Value |
|-------|-------|
| **Test ID** | T-007 |
| **Test Name** | Bad-Payload Test — Malformed JSON Rejected |
| **Test Type** | Failure Path |
| **Scenarios Exercised** | M-BRAND-ROUTER (webhook receiver) |
| **Estimated Duration** | 10 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] Make webhook endpoint for M-BRAND-ROUTER / M-LEAD-INTAKE accessible (WHK-SSS-LEAD-INTAKE-SANDBOX URL generated)
- [ ] Error handling for JSON parse failure implemented in the webhook receiver step

**Test Procedure:**
POST the following malformed JSON body to WHK-SSS-LEAD-INTAKE-SANDBOX:
```
Content-Type: application/json
Authorization: Bearer [valid_token]
Body: {"brand": "SSS", "lead": {bad json here, missing closing braces
```

**Expected Outcome (all must be true):**
1. Make webhook parser catches the malformed body at ingestion
2. Scenario terminates immediately — no downstream modules execute
3. HTTP response to sender: Make returns a response that does NOT trigger a retry storm (either HTTP 200 with error body, or HTTP 400 — document which behavior Make exhibits and verify it matches the architecture spec)
4. Zero Requests records created
5. Zero Client records created
6. Automation_Failures: one new record with `Error_Code = MALFORMED_PAYLOAD`
7. Audit_Log: one entry noting malformed payload rejection

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **HTTP Status Returned** | [TO BE FILLED] |
| **Automation_Failures Record ID** | [TO BE FILLED] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-008 — Webhook Replay Test: Timestamp >5 Minutes Rejected with 401 / Guard

| Field | Value |
|-------|-------|
| **Test ID** | T-008 |
| **Test Name** | Webhook Replay Test — Timestamp Older Than 5 Minutes Rejected |
| **Test Type** | Failure Path |
| **Scenarios Exercised** | M-BRAND-ROUTER, M-LEAD-INTAKE |
| **Estimated Duration** | 10 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] Timestamp validation module implemented in M-BRAND-ROUTER or M-LEAD-INTAKE
- [ ] Rejection threshold configured: reject if `submitted_at` is more than 5 minutes in the past
- [ ] Test environment clock accurate (UTC)

**Test Data — Valid SSS Payload with Stale Timestamp:**
```json
{
  "submission_id": "WEBFLOW-TEST-SSS-REPLAY",
  "submitted_at": "2026-05-16T21:00:00Z",
  "form_name": "SSS Charter Inquiry",
  "brand": "SSS",
  "lead": {
    "first_name": "Alexandra",
    "last_name": "Testclient",
    "email": "ops-test+sss@shesaidsail.com",
    "phone": "+13055550100",
    "preferred_contact": "email"
  },
  "inquiry": {
    "charter_type": "Private Luxury Charter",
    "preferred_date": "2026-07-15",
    "group_size": 8,
    "notes": "TEST — REPLAY ATTACK SIMULATION — TIMESTAMP IS 60+ MINUTES OLD"
  },
  "metadata": {
    "source": "Webflow",
    "ip_address": "192.0.2.1",
    "user_agent": "Make-Test-Agent/1.0"
  }
}
```
Note: The `submitted_at` value of `2026-05-16T21:00:00Z` is intentionally far in the past. Adjust to be 10+ minutes before actual test execution time when running.

**Expected Outcome (all must be true):**
1. Timestamp validation fires immediately after webhook is received
2. Execution terminates — no Airtable writes, no Slack alerts, no downstream scenario calls
3. HTTP response to sender: 401 Unauthorized (or HTTP 200 with rejection body — document actual Make behavior)
4. Zero Request records created
5. Automation_Failures: one new record with `Error_Code = WEBHOOK_REPLAY` and the stale timestamp logged
6. Audit_Log: one entry noting replay rejection

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **HTTP Status Returned** | [TO BE FILLED] |
| **Automation_Failures Error_Code** | [TO BE FILLED — must be WEBHOOK_REPLAY or equivalent] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-009 — Failure-Path Test: Forced Airtable Write Failure Triggers 4-Level Error Chain

| Field | Value |
|-------|-------|
| **Test ID** | T-009 |
| **Test Name** | Failure Path — Forced Airtable Write Failure Triggers Full 4-Level Error Escalation Chain |
| **Test Type** | Failure Path |
| **Scenarios Exercised** | M-LEAD-INTAKE, M-AUDIT-LOGGER, M-SLACK-ALERTS |
| **Estimated Duration** | 45–90 minutes (error chain includes timed retries — 3 × 2-minute waits minimum) |
| **Will Present Required** | YES — Level 4 DM goes to Will; Will must confirm receipt |

**Pre-Conditions Required:**
- [ ] All error handling modules implemented per ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md
- [ ] 4-level escalation chain configured: Level 1 (log) → Level 2 (retry ×3) → Level 3 (Slack to Luciana) → Level 4 (DM to Will + pause scenario)
- [ ] Will's Slack user ID stored in Make Data Store for Level 4 DM routing
- [ ] Sandbox Airtable PAT available with write permissions that can be temporarily modified

**Test Procedure:**
1. In Make, temporarily configure the Airtable write module in M-LEAD-INTAKE to use an invalid API token (or revoke write permission on the Requests table)
2. Submit T-001 SSS payload to WHK-SSS-LEAD-INTAKE-SANDBOX
3. Monitor Make execution log — do NOT intervene during the retry sequence
4. Wait for all retry attempts to exhaust (minimum 3 retries × 2-minute intervals = ~8 minutes minimum before Level 3 fires)
5. Confirm Level 3 Slack alert in #sss-ops-alerts (Luciana's channel)
6. After 4th failure, confirm Level 4 DM to Will
7. After test completes: restore correct Airtable credentials; clear the Automation_Failures record; manually verify logging resumes

**Expected Outcome (all must be true):**
1. Level 1: First failure creates Automation_Failures record with `Failure_Count = 1`, `Status = OPEN`
2. Level 2: Make retries the Airtable write 3 times at 2-minute intervals; each attempt increments `Failure_Count`
3. Level 3 (at Failure_Count = 3): Slack message to Luciana in #sss-ops-alerts matching template ERR-LEVEL-3; message contains `Execution_ID`, error description, affected record reference
4. Level 4 (at Failure_Count = 4): Slack DM to Will matching template ERR-LEVEL-4; scenario is paused in Make (confirm in Make scenario status)
5. Automation_Failures record final state: `Failure_Count = 4`, `Status = OPEN`, `Last_Failure_At` populated
6. Audit_Log: entries for each retry attempt and each escalation level fired
7. After credential restoration: M-LEAD-INTAKE resumes and processes original payload correctly

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Will Present — Confirmed** | [TO BE FILLED — Yes / No] |
| **Date / Time** | [TO BE FILLED] |
| **Level 3 Alert Time** | [TO BE FILLED — timestamp Slack message received] |
| **Level 4 DM Time** | [TO BE FILLED — timestamp DM received by Will] |
| **Automation_Failures Record ID** | [TO BE FILLED] |
| **Final Failure_Count** | [TO BE FILLED — must be 4] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-010 — Rollback Test: Scenario Disabled, Data Integrity Preserved

| Field | Value |
|-------|-------|
| **Test ID** | T-010 |
| **Test Name** | Rollback Test — Scenario Disabled, Data Integrity Preserved |
| **Test Type** | Failure Path |
| **Scenarios Exercised** | M-BOOKING-CREATION |
| **Estimated Duration** | 30 minutes |
| **Will Present Required** | No (Luciana follows rollback protocol step-by-step) |

**Pre-Conditions Required:**
- [ ] T-003 completed (at least one Sandbox Booking record exists)
- [ ] MAKE_ROLLBACK_PROTOCOLS.md Section 2.7 reviewed and available
- [ ] Deployment_Log table exists in Sandbox base
- [ ] Luciana is familiar with the rollback procedure document before this test begins

**Test Procedure:**
Follow MAKE_ROLLBACK_PROTOCOLS.md Section 2.7 exactly, with the Sandbox M-BOOKING-CREATION scenario as the target:
1. Set `Automations_Paused = TRUE` in Sandbox Automation_Health
2. Disable M-BOOKING-CREATION scenario in Make (not delete — disable toggle)
3. Create a Deployment_Log entry documenting the rollback event
4. Update all affected Booking records: set `Status = ROLLBACK_VOID`
5. Write Audit_Log entry for the rollback action
6. Verify no records have been deleted (rollback = flag only, never delete)
7. Record total time from start to completed rollback documentation

**Expected Outcome (all must be true):**
1. M-BOOKING-CREATION scenario status in Make: Inactive (disabled, not deleted)
2. Deployment_Log: one new record documenting the rollback with timestamp, executor name, and reason
3. All Booking records from T-003: Status = `ROLLBACK_VOID` (no records deleted)
4. Audit_Log: one entry with `Event_Type = ROLLBACK_EXECUTED` or equivalent
5. `Automations_Paused` reset to FALSE after rollback is documented (confirm scenarios resume)
6. Total elapsed time from step 1 to completed documentation: ≤30 minutes
7. Zero records deleted from any table during the rollback procedure

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Elapsed Time (minutes)** | [TO BE FILLED — must be ≤30] |
| **Booking Records Flagged ROLLBACK_VOID** | [TO BE FILLED — count] |
| **Records Deleted** | [TO BE FILLED — must be 0] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-011 — Audit Log Verification: Every Scenario Produces Correct Entry

| Field | Value |
|-------|-------|
| **Test ID** | T-011 |
| **Test Name** | Audit Log Verification — Every Scenario Produces a Correct Audit_Log Entry |
| **Test Type** | Integration |
| **Scenarios Exercised** | M-AUDIT-LOGGER (all 8 callers) |
| **Estimated Duration** | 20 minutes (post-integration test analysis) |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] T-001 full pipeline integration test has been completed in this test session
- [ ] T-003 (Booking creation) and T-004 (Stripe deposit) completed in this session
- [ ] M-AUDIT-LOGGER running and connected from all 8 scenarios
- [ ] Audit_Log table exists in Sandbox base with correct schema

**Test Procedure:**
1. After completing T-001, T-003, and T-004, query the Sandbox Audit_Log table
2. Filter to current test session's Execution_IDs (use the Make execution IDs recorded above)
3. For each of the 8 scenarios, verify exactly one Audit_Log entry exists per scenario execution

**Required Audit_Log Fields to Verify for Each Entry:**

| Field | Requirement |
|-------|------------|
| `Scenario_Name` | Non-null; exactly matches one of the 8 scenario names |
| `Execution_ID` | Non-null; matches Make's {{executionId}} for that run |
| `Created_At` | Non-null; within ±60 seconds of scenario execution time |
| `Event_Type` | Non-null; valid value per spec |
| `Brand` | Non-null; SSS or ME — correct for the test payload |
| `Environment` | Non-null; = sandbox |
| `Status` | Non-null; SUCCESS or ERROR |
| `Record_ID` | Non-null for scenarios that create Airtable records |

**Expected Outcome (all must be true):**
1. Audit_Log entry count from this test session: ≥8 (one per scenario that ran)
2. All 8 Scenario_Name values represented (no scenario missing from the log)
3. Zero null values in required fields across all entries
4. No two entries share the same Execution_ID
5. Created_At timestamps are chronologically ordered and sensible (M-BRAND-ROUTER fires before M-LEAD-INTAKE, etc.)
6. Brand field = SSS for all T-001 entries; ME for all T-002 entries (no cross-contamination)
7. Environment = sandbox for all entries (no production entries in sandbox log)

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Audit_Log Entry Count (this session)** | [TO BE FILLED — must be ≥8] |
| **Scenarios with Missing Entries** | [TO BE FILLED — must be None] |
| **Null Fields Found** | [TO BE FILLED — must be None] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-012 — Automation Health Verification: Health Records Created Correctly

| Field | Value |
|-------|-------|
| **Test ID** | T-012 |
| **Test Name** | Automation Health Verification — Automation_Health Records Created and Kill Switch Functional |
| **Test Type** | Unit |
| **Scenarios Exercised** | All 8 scenarios (each reads the Automation_Health control record as Step 1) |
| **Estimated Duration** | 20–30 minutes |
| **Will Present Required** | No |

**Pre-Conditions Required:**
- [ ] BLK-003 resolved (Automation_Health table exists; Automations_Paused field present; one control record exists with `Record_Type = global_control`)
- [ ] All 8 scenarios configured with Automation_Health read as Step 1 followed by guard filter as Step 2

**Test Procedure — Part A: Normal Operation Confirmed**
1. Confirm `Automations_Paused = FALSE` in Sandbox Automation_Health control record
2. Submit T-001 SSS payload
3. Confirm all scenarios execute normally (T-001 expected outcome)

**Test Procedure — Part B: Kill Switch Verification**
1. In Sandbox Automation_Health: set `Automations_Paused = TRUE`; set `Paused_By = "T-012 Test"`; set `Pause_Reason = "Kill switch test — T-012"`
2. Submit a new SSS payload to WHK-SSS-LEAD-INTAKE-SANDBOX
3. Wait 60 seconds
4. Confirm NO scenario actions executed
5. Reset `Automations_Paused = FALSE` in Automation_Health

**Expected Outcome (all must be true):**
1. Part A: All 8 scenarios execute normally with `Automations_Paused = FALSE`
2. Part B, scenario behavior: Make execution log shows scenario triggered BUT stops at Step 2 (after the Automation_Health read; before any Airtable write or external call)
3. Part B, Airtable: Zero new records in Requests, Clients, or any other table during kill switch test
4. Part B, Slack: Zero Slack messages sent during kill switch test
5. Part B, Stripe: Zero Stripe API calls during kill switch test
6. After reset to FALSE: next valid submission processes normally
7. Automation_Health control record integrity: still exactly one record with `Record_Type = global_control` (not duplicated by Make)

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Date / Time** | [TO BE FILLED] |
| **Kill Switch Engaged At** | [TO BE FILLED — timestamp] |
| **Kill Switch Released At** | [TO BE FILLED — timestamp] |
| **Records Created During Kill Switch Period** | [TO BE FILLED — must be 0] |
| **Notes / Defects** | [TO BE FILLED] |

---

### T-013 — Slack Alert Verification: All Alert Types in Correct Channels

| Field | Value |
|-------|-------|
| **Test ID** | T-013 |
| **Test Name** | Slack Alert Verification — All Alert Types Arrive in Correct Channels |
| **Test Type** | Unit |
| **Scenarios Exercised** | M-SLACK-ALERTS |
| **Estimated Duration** | 20–30 minutes |
| **Will Present Required** | YES — Level 4 DM alert must be received and confirmed by Will |

**Pre-Conditions Required:**
- [ ] SSS_SLACK_BOT token active and bot invited to #sss-ops-alerts and #sss-emergency-ops
- [ ] All Slack alert templates configured in M-SLACK-ALERTS per ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md Section 5
- [ ] Will's Slack user ID stored in Make Data Store for Level 4 DM

**Test Procedure:**

Alert Type 1 — New Lead Alert:
1. Submit T-001 SSS payload (or use result from T-001 if already complete)
2. Verify message appears in #sss-ops-alerts within 60 seconds

Alert Type 2 — Level 3 Failure Alert (Luciana's channel):
1. Manually create an Automation_Failures record in Sandbox with `Failure_Count = 3` and `Status = OPEN`
2. Trigger M-SLACK-ALERTS with this failure record as input (or wait for HEALTH-001 polling — or trigger manually via Make test execution)
3. Verify Level 3 alert appears in #sss-ops-alerts

Alert Type 3 — Level 4 Critical Alert (DM to Will):
1. Update the Automation_Failures record to `Failure_Count = 4`
2. Trigger Level 4 escalation path in M-SLACK-ALERTS
3. Will confirms receipt of Slack DM

**Expected Outcome for Each Alert Type:**

| Alert Type | Expected Channel / Destination | Required Content | Timing |
|------------|-------------------------------|------------------|--------|
| New Lead (SSS) | #sss-ops-alerts | Client name, brand = SSS, charter date, inquiry type | ≤60 sec |
| New Lead (ME) | #sss-ops-alerts (with ME label) or ME-specific channel | Brand = ME label visible | ≤60 sec |
| Level 3 Failure | #sss-ops-alerts | Execution_ID, error description, Failure_Count = 3, affected record link | ≤60 sec |
| Level 4 Critical | Slack DM to Will | Execution_ID, error description, Failure_Count = 4, @Will mention, link to Automation_Failures record | ≤60 sec |

Additional checks:
1. All messages render correctly — bold text renders; no raw Slack markdown syntax visible
2. No alert routing errors (message to wrong channel)
3. No duplicate alerts (each event produces exactly one alert)
4. Block Kit formatting used for lead alerts (if specified in template library)

| | |
|---|---|
| **Actual Outcome** | [TO BE FILLED] |
| **Pass / Fail** | [TO BE FILLED] |
| **Tester** | [TO BE FILLED] |
| **Will Present — DM Confirmed** | [TO BE FILLED — Yes / No] |
| **Date / Time** | [TO BE FILLED] |
| **New Lead Alert — Channel and Time** | [TO BE FILLED] |
| **Level 3 Alert — Channel and Time** | [TO BE FILLED] |
| **Level 4 DM — Received by Will at** | [TO BE FILLED] |
| **Notes / Defects** | [TO BE FILLED] |

---

## FINAL SIGN-OFF

Complete this section only after all 13 tests have been run and all rows above are filled.

```
STAGE 1 TEST RESULTS — FINAL SIGN-OFF
======================================

Test Session Date:             _______________
Total Tests Run:               13
Tests Passed:                  _____ / 13
Tests Failed:                  _____ / 13

Open Defects at Sign-Off:      _____ (must be 0 to advance to Production)
Automation_Failures at end:    _____ (must be 0)
Audit_Log gaps detected:       _____ (must be 0)

SUMMARY OF ANY DEFECTS FOUND AND RESOLVED DURING TESTING:
(List any defect that was found during testing, even if resolved before sign-off)

  1. _______________________________________________________________
  2. _______________________________________________________________
  3. _______________________________________________________________
  (add rows as needed)


LUCIANA — OPS LEAD SIGN-OFF
-----------------------------------------
I confirm that I personally executed all 13 test cases above (or the specific
test cases assigned to me), recorded all outcomes accurately, and that the
results reflect the true behavior of the Stage 1 Make.com scenarios as tested
in the Sandbox environment on the date above. All tests passed. Zero unresolved
defects remain.

Luciana signature: ________________________
Full name printed: Luciana [last name]
Date/Time signed:  _______________
Sandbox base ID tested: _______________


WILL — FOUNDER FINAL APPROVAL
-----------------------------------------
I have reviewed the test results above. I was present for the following tests:
  T-004 (Stripe test-mode deposit): [ ] Present  [ ] Not present
  T-009 (Failure-path / Level 4):   [ ] Present  [ ] Not present
  T-013 (Level 4 DM received):      [ ] Present  [ ] Not present

Based on my review of the results and Luciana's sign-off above:

[ ] APPROVED — All 13 tests passed. Zero open defects. Stage 1 is cleared
    for Production promotion. Will has reviewed all Stripe test results.
    Stripe test-mode confirmed: no live charges occurred at any point.

[ ] NOT APPROVED — Defects remain. Stage 1 is NOT cleared for Production.
    See notes below.

[ ] CONDITIONAL APPROVAL — Approved with the following conditions:
    _______________________________________________________________

Will signature:    ________________________
Full name printed: Will [last name]
Date/Time signed:  _______________

Notes: _______________________________________________________________
```

---

*Document prepared: 2026-05-16. All test statuses are NOT RUN as of this date — Make build phase has not yet begun. Update this document during sandbox testing. File signed copies in 02_SYSTEMS_AUTOMATIONS/STAGE_1_MAKE_IMPLEMENTATION/OUTPUTS/.*
*Authority: MAKE_TESTING_PROTOCOLS.md — all test cases cross-referenced to that document.*
