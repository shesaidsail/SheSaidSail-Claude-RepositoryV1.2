# MAKE.COM TESTING PROTOCOLS — STAGE 1
## She Said Sail + Mare Executive — QA and Validation Governance

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Effective Date:** May 2026  
**Owner:** Will (Founder)  
**Applies To:** All 8 Stage 1 Make.com Scenarios  
**Classification:** Confidential — Internal Use Only  
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

## SECTION 1 — TESTING PHILOSOPHY

### 1.1 Test Every Path, Including Failure Paths

A scenario that passes only the happy path is not tested — it is hoped. Every Stage 1 scenario must demonstrate correct behavior across four dimensions before Production activation:

1. **Happy path:** valid input, all APIs responding, correct output produced
2. **Failure paths:** each API fails in isolation; the correct error handling fires
3. **Edge cases:** duplicate submissions, missing fields, malformed payloads, expired webhooks
4. **Data integrity:** no orphaned records, no duplicate writes, idempotency verified

If a failure path is not tested, the failure path is not trusted. The retry architecture documented in ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md has no value unless each level of that hierarchy is confirmed to fire under simulated failure conditions.

### 1.2 Test Execution Authority

| Test Type | Executed By | Sign-Off Required |
|-----------|-------------|-------------------|
| Unit tests (individual scenario) | Luciana | Luciana signs test results |
| Integration test (end-to-end flow) | Luciana + Will present | Both sign results |
| Failure-path tests | Luciana | Luciana signs; Will reviews |
| Stripe test-mode tests | Luciana (Will must be present) | Both sign |
| Production smoke test (post go-live) | Will | Will signs |

---

## SECTION 2 — SANDBOX ENVIRONMENT SETUP

### 2.1 Required Sandbox Configuration

Before any test is executed, confirm ALL of the following are true:

| Requirement | Verification Method | Owner |
|------------|---------------------|-------|
| SSS Sandbox Airtable base exists (separate base, not a repurposed production base) | Check base list in Airtable — must not be appdZ49WqgjRXxA1R | Will |
| Sandbox base has identical table schema to production base | Field-by-field comparison; document differences | Luciana |
| Environment field present and set to "Sandbox" on all test records | Filter Sandbox base: Environment IS EMPTY = 0 records | Luciana |
| Stripe test-mode API keys configured in Make Sandbox scenarios | Make > Connections > Stripe — confirm "Test mode" label visible | Will |
| Gmail test inbox configured (internal address — not a real client address) | Confirm test inbox: ops-test@shesaidsail.com (or equivalent) | Will |
| Quo SMS test numbers configured (no real client numbers in any test fixture) | Confirm test numbers in Make Quo SMS connection | Will |
| Slack test workspace or test channels for alert validation | Confirm alerts route to #sss-ops-alerts-sandbox or a test channel | Luciana |
| Make Sandbox scenario set isolated from Production scenarios (separate scenario IDs) | Confirm in Make — sandbox and production must not share a scenario | Will |
| Webflow sandbox form configured to POST to Make Sandbox webhook URL (not Production) | Test the form endpoint URL — confirm it is the sandbox webhook | Will |

### 2.2 Sandbox Reset Protocol

Before each test run, Luciana executes the Sandbox reset:
1. Delete all Sandbox test records from Sandbox Airtable base (filter Environment = Sandbox, delete all)
2. Clear any open Stripe test payment intents (Stripe test dashboard > filter by test mode > cancel all open intents)
3. Clear Sandbox Automation_Failures table records
4. Clear Sandbox Audit_Log records
5. Confirm Make scenario execution counters are reset (Make > Scenario > History > confirm no pending executions)

---

## SECTION 3 — STANDARD TEST DATA

### 3.1 Fake Lead Payload — SSS Brand (JSON)

Use this exact JSON payload for all SSS fake lead tests. Do NOT use real client names, real email addresses, or real phone numbers.

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

### 3.2 Fake Lead Payload — ME Brand (JSON)

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

### 3.3 Fake Stripe Webhook Payload (payment_intent.succeeded)

```json
{
  "id": "evt_test_STRIPE001",
  "object": "event",
  "type": "payment_intent.succeeded",
  "created": 1747432800,
  "livemode": false,
  "data": {
    "object": {
      "id": "pi_test_STRIPE001",
      "object": "payment_intent",
      "amount": 150000,
      "currency": "usd",
      "status": "succeeded",
      "metadata": {
        "airtable_request_id": "recTEST0000001",
        "brand": "SSS",
        "client_email": "ops-test+sss@shesaidsail.com",
        "environment": "Sandbox"
      }
    }
  }
}
```

---

## SECTION 4 — UNIT TEST SUITE PER SCENARIO

### 4.1 M-AUDIT-LOGGER Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| AU-01 | Log creation on trigger | Fake module execution event | New record in Audit_Log with all required fields populated | All fields present; no null values on required fields |
| AU-02 | Correct Scenario_Name written | Trigger from M-LEAD-INTAKE | Audit_Log.Scenario_Name = "M-LEAD-INTAKE" | Field matches exactly |
| AU-03 | Execution_ID written | Any trigger | Audit_Log.Execution_ID = Make's {{executionId}} | Field is non-empty, format: alphanumeric |
| AU-04 | Timestamp accuracy | Any trigger | Audit_Log.Created_At within ±30 seconds of actual trigger time | Timestamp verified against system clock |
| AU-05 | No duplicate log entries | Same trigger twice | Exactly 1 new Audit_Log record | Record count = 1 after both triggers |

**Executor:** Luciana  
**Pass threshold:** All 5 tests pass

---

### 4.2 M-BRAND-ROUTER Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| BR-01 | SSS routing | SSS fake payload (Section 3.1) | Routes to M-LEAD-INTAKE; Brand field = SSS | Downstream M-LEAD-INTAKE receives trigger |
| BR-02 | ME routing | ME fake payload (Section 3.2) | Routes to ME lead handling; Brand field = ME | Downstream scenario receives trigger with Brand = ME |
| BR-03 | Idempotency — duplicate webhook | SSS fake payload sent twice (same submission_id) | First: creates record. Second: no new record. | Requests table count = 1 after both submissions |
| BR-04 | Invalid brand field | Payload with brand = "UNKNOWN" | Error logged to Automation_Failures; no record created | Automation_Failures record with Error_Code = INVALID_BRAND |
| BR-05 | Missing submission_id | Payload without submission_id field | Execution terminates; error logged | Automation_Failures record; no Request record created |

**Executor:** Luciana  
**Pass threshold:** All 5 tests pass

---

### 4.3 M-LEAD-INTAKE Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| LI-01 | Request record creation | SSS fake payload | New Request record in Airtable with all required fields | Record created; Brand = SSS; Environment = Sandbox |
| LI-02 | Client record creation | SSS fake payload — new client | New Client record created; linked to Request | Client record created; linked record field populated |
| LI-03 | Existing client — no duplicate | SSS fake payload — email matches existing client | No new Client record; existing client linked to Request | Client count unchanged; Request linked to existing Client |
| LI-04 | Idempotency_Key written | SSS fake payload | Request.Idempotency_Key = computed hash | Field non-empty; format matches SHA-256 output |
| LI-05 | Audit_Log entry created | Any valid payload | Audit_Log entry with Scenario_Name = M-LEAD-INTAKE | Audit_Log record exists with correct scenario name and execution ID |

**Executor:** Luciana  
**Pass threshold:** All 5 tests pass

---

### 4.4 M-SLACK-ALERTS Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| SA-01 | New lead alert fires | New Request record created | Slack message in #sss-ops-alerts with client name and brand | Message received in correct channel within 60 seconds |
| SA-02 | ME brand alert — correct channel | ME Request record | Slack message routed to correct ME ops channel (or #sss-ops-alerts with ME label) | Brand label correct in message |
| SA-03 | Level 3 failure alert | Simulated Automation_Failures record with Failure_Count = 3 | Slack alert to Luciana in #sss-ops-alerts using Level 3 template | Message matches template from Error Handling doc Section 5.1 |
| SA-04 | Level 4 alert — DM to Will | Simulated Automation_Failures record with Failure_Count = 4 | Slack DM to Will using Level 4 template | DM received by Will; scenario shows paused status |
| SA-05 | No duplicate alerts | Same Request record triggers twice | Exactly one Slack alert | Message count in channel = 1 |

**Executor:** Luciana (Will must be present for SA-04)  
**Pass threshold:** All 5 tests pass

---

### 4.5 M-CONCIERGE-ASSIGNMENT Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| CA-01 | SSS concierge assigned | SSS Request record | Requests.Assigned_Concierge = Luciana (or correct concierge per rules) | Field populated; correct concierge name |
| CA-02 | ME concierge assigned | ME Request record | Requests.Assigned_Concierge = correct ME concierge | Field populated; correct concierge per ME rules |
| CA-03 | Assignment timestamp written | Any valid Request | Requests.Assigned_At = current timestamp | Field populated; timestamp within ±60 seconds of test execution |
| CA-04 | No overwrite of manual assignment | Request with Assigned_Concierge already set manually | No change to Assigned_Concierge field | Field value unchanged |
| CA-05 | Audit_Log entry | Any valid assignment | Audit_Log entry with Scenario_Name = M-CONCIERGE-ASSIGNMENT | Audit_Log record created |

**Executor:** Luciana  
**Pass threshold:** All 5 tests pass

---

### 4.6 M-STRIPE-DEPOSIT Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| SD-01 | Stripe test payment intent created | Valid Request record + Package pricing | Stripe test payment intent created; PI ID written to Airtable | Stripe dashboard shows test PI; Airtable.Stripe_Payment_Intent_ID populated |
| SD-02 | Correct deposit amount | Request linked to Package with known price | PI amount = correct deposit (e.g., 30% of package price in cents) | Stripe PI amount matches formula output |
| SD-03 | Payment success webhook received | Fake Stripe payload from Section 3.3 | Airtable record updated: Deposit_Paid = true; Deposit_Amount written | Both fields updated within 60 seconds of webhook |
| SD-04 | Invalid Stripe signature rejected | Fake payload with tampered signature | Execution terminated; Automation_Failures record created | Error_Code = STRIPE_INVALID_SIGNATURE |
| SD-05 | Audit_Log entry | Any valid PI creation | Audit_Log entry with Scenario_Name = M-STRIPE-DEPOSIT | Audit_Log record created |

**Executor:** Luciana (Will must be present — involves Stripe)  
**Pass threshold:** All 5 tests pass

---

### 4.7 M-BOOKING-CREATION Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| BC-01 | Booking record created | Valid Request + confirmed deposit | New Booking record in Airtable | Record created; Status = CONFIRMED (or DEPOSIT_PAID per workflow) |
| BC-02 | Linked records correct | Booking creation | Booking.Client = correct Client; Booking.Yacht = correct Yacht; Booking.Package = correct Package | All three linked record fields populated |
| BC-03 | Environment field set | Booking creation in Sandbox | Booking.Environment = Sandbox | Field = Sandbox |
| BC-04 | No duplicate Booking | Same trigger fires twice | Exactly 1 Booking record | Booking count = 1 after two triggers |
| BC-05 | Audit_Log entry | Any valid Booking creation | Audit_Log entry with Scenario_Name = M-BOOKING-CREATION | Audit_Log record created |

**Executor:** Luciana  
**Pass threshold:** All 5 tests pass

---

### 4.8 M-BOOKING-CONFIRMATION Unit Tests

| Test # | Test Name | Input | Expected Output | Pass Criteria |
|--------|-----------|-------|-----------------|---------------|
| CF-01 | Confirmation email sent | Valid Booking record | Email received at test inbox (ops-test+sss@shesaidsail.com) with correct content | Email received; contains client name, charter date, vessel name, deposit amount |
| CF-02 | Confirmation SMS sent | Valid Booking record with phone | SMS received at test number with correct content | SMS received within 60 seconds; ≤160 characters |
| CF-03 | Brand-correct template used | SSS Booking | Email uses SSS template (SSS logo, SSS language, SSS contact details) | No ME branding in SSS email |
| CF-04 | ME brand-correct template | ME Booking | Email uses ME template | No SSS branding in ME email |
| CF-05 | Audit_Log entry | Any valid confirmation | Audit_Log entry with Scenario_Name = M-BOOKING-CONFIRMATION | Audit_Log record created |

**Executor:** Luciana (Will must confirm CF-03 and CF-04 template compliance)  
**Pass threshold:** All 5 tests pass

---

## SECTION 5 — INTEGRATION TEST: FULL FAKE LEAD FLOW

### 5.1 End-to-End Integration Test Procedure

This test exercises all 8 scenarios in sequence using a single fake lead payload.

**Pre-requisites:** All 8 unit test suites have passed. Sandbox environment is reset (Section 2.2).

**Executor:** Luciana (primary); Will present for Stripe and confirmation steps.

```
STEP 1 — Trigger
Submit SSS fake payload (Section 3.1) via Webflow sandbox form
→ Confirm webhook received in Make (check Make > Scenario > History)

STEP 2 — M-BRAND-ROUTER
Verify: payload routed to SSS path; Brand = SSS in routing context
→ Check Make execution log; confirm no errors

STEP 3 — M-LEAD-INTAKE
Verify: Request record created in Sandbox Airtable base
→ Check: all required fields populated; Idempotency_Key written; Environment = Sandbox

STEP 4 — M-SLACK-ALERTS
Verify: Slack alert received in #sss-ops-alerts (or sandbox Slack channel) within 60 seconds
→ Check: alert contains Alexandra Testclient name; Brand = SSS

STEP 5 — M-CONCIERGE-ASSIGNMENT
Verify: Request.Assigned_Concierge field populated
→ Check: correct concierge per assignment rules; Assigned_At timestamp written

STEP 6 — M-STRIPE-DEPOSIT
Manually advance the test: update Request.Status to "AVAILABILITY_CONFIRMED" to trigger deposit
→ Verify: Stripe test payment intent created; PI ID written to Airtable
→ Simulate payment: use Stripe test dashboard to confirm the PI
→ Verify: Stripe webhook received by Make; Deposit_Paid = TRUE; Deposit_Amount written

STEP 7 — M-BOOKING-CREATION
Verify: Booking record created in Sandbox base
→ Check: Status = correct value; all linked records populated (Client, Yacht, Package)

STEP 8 — M-BOOKING-CONFIRMATION
Verify: Confirmation email received at ops-test+sss@shesaidsail.com
→ Verify: Confirmation SMS received at test phone number
→ Check: content is correct (client name, charter date, deposit amount, vessel name)
→ Check: SSS brand template used

STEP 9 — M-AUDIT-LOGGER
Verify: Audit_Log contains entries from all 8 scenarios
→ Count: minimum 8 Audit_Log entries with distinct Scenario_Name values

STEP 10 — Error Handling Verification
→ Confirm: zero records in Automation_Failures table after this successful run
→ Confirm: zero Founder Decision records created
→ Confirm: no duplicate Requests, Clients, or Bookings records
```

**Pass criteria:** All 10 steps produce expected outcomes with zero unexpected errors.

---

## SECTION 6 — SPECIFIC TEST CASES

### Test Case 1 — Fake Lead Test (SSS Brand)

| Field | Value |
|-------|-------|
| Test ID | TC-01 |
| Payload | Section 3.1 SSS JSON payload |
| Executor | Luciana |
| Pass Criteria | Request record created with Brand = SSS; Audit_Log entry created; Slack alert fired to #sss-ops-alerts |
| Fail Criteria | Any field missing; Brand misrouted as ME; Audit_Log entry absent |

---

### Test Case 2 — Fake Lead Test (ME Brand)

| Field | Value |
|-------|-------|
| Test ID | TC-02 |
| Payload | Section 3.2 ME JSON payload |
| Executor | Luciana |
| Pass Criteria | Request record created with Brand = ME; correct ME concierge assigned; ME brand template used in any notifications |
| Fail Criteria | Brand = SSS on record; SSS template used for ME lead |

---

### Test Case 3 — Fake Booking Test

| Field | Value |
|-------|-------|
| Test ID | TC-03 |
| Setup | Manually create a test Request record in Sandbox with all required fields; mark Deposit_Paid = TRUE |
| Executor | Luciana |
| Pass Criteria | M-BOOKING-CREATION fires; Booking record created with correct Status, correct linked Client, Yacht, Package; Audit_Log entry written |
| Fail Criteria | Booking not created; missing linked record; Environment = Production on Sandbox record |

---

### Test Case 4 — Stripe Test-Mode Deposit Test

| Field | Value |
|-------|-------|
| Test ID | TC-04 |
| Setup | Valid Request record in Sandbox; Stripe test-mode keys active |
| Action | Trigger M-STRIPE-DEPOSIT; use Stripe test card 4242 4242 4242 4242 to complete payment |
| Executor | Luciana (Will present) |
| Pass Criteria | Test payment intent created with correct amount in cents; payment_intent.succeeded webhook received by Make; Deposit_Paid = TRUE written to Airtable; Audit_Log entry created |
| Fail Criteria | Payment intent amount incorrect; webhook not received; Airtable field not updated; live Stripe key used instead of test key |

---

### Test Case 5 — Duplicate Submission Test

| Field | Value |
|-------|-------|
| Test ID | TC-05 |
| Action | Submit SSS fake payload (Section 3.1) twice within 30 seconds (same submission_id) |
| Executor | Luciana |
| Pass Criteria | Exactly 1 Request record created; Audit_Log shows 1 execution processed; 1 execution terminated as duplicate |
| Fail Criteria | 2 Request records created; 2 Slack alerts fired; 2 Audit_Log entries for new record creation |

---

### Test Case 6 — Missing-Field Test (Incomplete Webhook Payload)

| Field | Value |
|-------|-------|
| Test ID | TC-06 |
| Action | Submit SSS payload with `email` field removed from the JSON |
| Executor | Luciana |
| Pass Criteria | Execution terminates safely; Automation_Failures record created with Error_Code = MISSING_REQUIRED_FIELD; no partial Request record created; Slack alert to Luciana in #sss-ops-alerts |
| Fail Criteria | Partial Request record created with null email; scenario errors without logging; no alert to Luciana |

---

### Test Case 7 — Bad Payload Test (Malformed JSON)

| Field | Value |
|-------|-------|
| Test ID | TC-07 |
| Action | POST malformed JSON to the Make webhook endpoint: `{"brand": "SSS", "lead": {bad json here}` |
| Executor | Luciana |
| Pass Criteria | Webhook parser catches malformed JSON; Automation_Failures record created with Error_Code = MALFORMED_PAYLOAD; HTTP 200 returned to sender (no retry storm); no Airtable records created |
| Fail Criteria | Scenario throws unhandled exception; no Automation_Failures log; HTTP 500 or 4xx returned triggering sender retry |

---

### Test Case 8 — Webhook Replay Test (Replay Older Than 5 Minutes)

| Field | Value |
|-------|-------|
| Test ID | TC-08 |
| Action | POST valid SSS payload with timestamp field set to 10 minutes in the past |
| Executor | Luciana |
| Pass Criteria | Timestamp validation fires; execution terminates immediately; Automation_Failures record with Error_Code = WEBHOOK_REPLAY; HTTP 200 returned; no Request record created |
| Fail Criteria | Old payload processed as valid; Request record created; no replay detection log |

---

### Test Case 9 — Failure-Path Test (Force Airtable Write Failure)

| Field | Value |
|-------|-------|
| Test ID | TC-09 |
| Setup | Temporarily revoke Make's Airtable API token write permission for the Requests table |
| Action | Submit valid SSS fake payload |
| Executor | Luciana |
| Pass Criteria | Level 1 failure logged; retry fires after 2 minutes; after 3 retries, Luciana receives Slack alert (Level 3); after 4th retry fails, Will receives DM (Level 4); Automation_Failures record has Failure_Count = 4 and Status = OPEN |
| Fail Criteria | Silent failure — no Automation_Failures record; no Slack alert; Make execution history shows error but no escalation |
| Post-test cleanup | Restore API token permissions; manually trigger M-AUDIT-LOGGER to verify logging resumes |

---

### Test Case 10 — Rollback Test

| Field | Value |
|-------|-------|
| Test ID | TC-10 |
| Setup | Create 3 Sandbox Request records and 1 Sandbox Booking record using fake data |
| Action | Execute M-BOOKING-CREATION rollback procedure per MAKE_ROLLBACK_PROTOCOLS.md Section 2.7 |
| Executor | Luciana (following rollback protocol document step by step) |
| Pass Criteria | Scenario paused in Make within 5 minutes; Deployment_Log record created; all affected Booking records flagged Status = ROLLBACK_VOID; Audit_Log entry created; 0 records deleted |
| Fail Criteria | Any record deleted; Deployment_Log not written; Audit_Log entry absent; rollback takes more than 30 minutes |

---

### Test Case 11 — Audit Log Verification Test

| Field | Value |
|-------|-------|
| Test ID | TC-11 |
| Setup | Run Integration Test (Section 5.1) |
| Action | Query Audit_Log for all entries from the integration test run |
| Executor | Luciana |
| Pass Criteria | Minimum 8 Audit_Log entries (one per scenario); each entry has non-null Scenario_Name, Execution_ID, Created_At; no two entries have identical Execution_ID values |
| Fail Criteria | Fewer than 8 entries; any entry missing required fields; duplicate Execution_IDs |

---

### Test Case 12 — Automation Health Verification

| Field | Value |
|-------|-------|
| Test ID | TC-12 |
| Setup | All 8 scenarios running; HEALTH-001 running in Sandbox with 15-minute poll |
| Action | Manually pause M-LEAD-INTAKE for 20 minutes; observe HEALTH-001 behavior |
| Executor | Will |
| Pass Criteria | HEALTH-001 detects logging gap after 15-minute poll; creates Automation_Failures record with Error_Code = SILENT_FAILURE_SUSPECTED; sends Slack alert to Luciana in #sss-ops-alerts |
| Fail Criteria | HEALTH-001 does not alert; Automation_Failures not created; no Slack notification |

---

### Test Case 13 — Slack Alert Verification

| Field | Value |
|-------|-------|
| Test ID | TC-13 |
| Action | Simulate each Slack alert type: new lead alert (SA-01), Level 3 failure alert (SA-03), Level 4 DM (SA-04) |
| Executor | Luciana (Will present for Level 4 DM verification) |
| Pass Criteria | All three alert types received in correct Slack destination within 60 seconds; message content matches templates exactly as defined in ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md Section 5; no formatting errors (bold text renders, emoji renders) |
| Fail Criteria | Any alert not received; wrong channel; template content missing required fields (Execution ID, error message, affected record link) |

---

### Test Case 14 — Email and SMS Test-Mode Verification

| Field | Value |
|-------|-------|
| Test ID | TC-14 |
| Setup | M-BOOKING-CONFIRMATION in Sandbox mode; test inbox and test phone number configured |
| Action | Trigger confirmation flow for SSS fake booking |
| Executor | Luciana |
| Pass Criteria | Email received at ops-test+sss@shesaidsail.com within 120 seconds; SMS received at test number within 60 seconds; email body contains all required fields (client name, charter date, vessel, deposit amount, SSS brand); SMS is ≤160 characters per segment; no real client email or phone number in the test (verify Make variable binding) |
| Fail Criteria | Email sent to any address other than the test inbox; SMS sent to any number other than the test number; email missing required fields; SMS exceeds 160 characters without visible segmentation; ME template used for SSS booking |

---

## SECTION 7 — PASS/FAIL CRITERIA SUMMARY

A scenario advances to Production promotion only when:

| Requirement | Threshold |
|------------|-----------|
| Unit tests | 100% pass rate — no partial credit |
| Integration test | All 10 steps pass in a single uninterrupted run |
| Specific test cases | All 14 test cases pass |
| Zero open Automation_Failures records after test run | Required |
| Zero Audit_Log gaps detected | Required |
| Luciana has signed test results document | Required |
| Will has reviewed results | Required |

A single failing test case blocks Production promotion. There are no exceptions. If a test case fails, the defect must be fixed in Development, re-tested in Sandbox from the beginning of that test case group (not just the individual test), and re-signed before promotion.

---

## SECTION 8 — TEST RESULTS TEMPLATE

Complete one of these documents for each scenario, for each Sandbox test run. Store signed copies in the STAGE_1_MAKE_IMPLEMENTATION directory.

```
TEST RESULTS — [SCENARIO-ID — SCENARIO-NAME]
Test Run Date: _______________
Test Run Start Time: _______________
Test Run End Time: _______________
Tester (Primary): Luciana
Tester (Witness/Will): [Present / Not present — note which tests required Will]
Sandbox Base: [Airtable base ID of Sandbox base]
Make Scenario Version Tested: [Make scenario version number]

UNIT TESTS
Test AU-01 / BR-01 / LI-01 / SA-01 / CA-01 / SD-01 / BC-01 / CF-01: [ ] PASS  [ ] FAIL
[repeat for each unit test in the scenario's test suite]

SPECIFIC TEST CASES APPLICABLE TO THIS SCENARIO
[List test case IDs that apply; mark PASS or FAIL for each]

DEFECTS FOUND
[If any FAIL: describe defect, exact module where it occurred, expected vs actual behavior]

DEFECTS RESOLVED BEFORE SIGN-OFF
[If defects found and fixed: describe fix; confirm re-test passed]

OVERALL RESULT
[ ] ALL TESTS PASSED — ELIGIBLE FOR PRODUCTION PROMOTION
[ ] TESTS FAILED — DO NOT PROMOTE — defects listed above

Luciana signature: ________________________  Date/Time: _______________
Will review: ________________________       Date/Time: _______________
Will production approval: [ ] Approved  [ ] Not approved  [ ] Conditional (notes below)

Notes: _______________________________________________________________
```

---

*Document Authority: Will (Founder)*  
*Last Review: May 2026*  
*Next Review: After Stage 1 go-live complete; update with any new test cases discovered post-launch*
