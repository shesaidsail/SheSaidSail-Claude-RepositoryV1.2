# FAILURE TESTS — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Tests that verify failure paths, safety gates, and error handling work correctly

---

## OVERVIEW

These tests intentionally trigger failure conditions to verify that:
1. Safety gates block correctly
2. Error alerts reach Slack
3. Audit Log captures failure state
4. No unintended data changes occur during failures

---

## FAILURE TEST 1: Empty Payload to OPS-LOGGER-ALERTER

**Intent:** Verify the scenario handles malformed or empty payloads gracefully

**Action:** POST an empty JSON object `{}`

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{}' \
  'OPS_LOGGER_ALERTER_WEBHOOK_URL'
```

**Expected behavior:**
- Module 2 filter checks `ifempty(1.triggering_event; 1.environment)` — both empty
- Filter BLOCKS (condition fails — `notExist`)
- Scenario exits at Module 2
- NO Airtable record created
- NO Slack message
- No error in Make run history (silent fail due to `throw: false`)

**Pass criteria:** Make run history shows execution stopped at Module 2. No Airtable records created.

---

## FAILURE TEST 2: Lead Intake — Missing Required Fields

**Intent:** Verify partial payloads are handled with ifempty fallbacks

**Action:** POST payload with only email field

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"email":"partial@test.com"}' \
  'LEAD_INTAKE_WEBHOOK_URL'
```

**Expected behavior:**
- Scenario proceeds (email exists)
- SetVariables uses `ifempty` to handle missing fields gracefully
- Airtable record created with partial data
- Empty fields stored as empty strings
- Auto-reply email sent (to partial@test.com)
- No scenario crash

**Pass criteria:** Record created in Airtable with no blank field errors. Scenario completes without crashing.

---

## FAILURE TEST 3: Stripe Deposit — Wrong Event Type

**Intent:** Verify non-payment events are filtered out

**Action:** POST a simulated Stripe webhook with wrong event type

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"type":"payment_intent.created","data":{"object":{"id":"pi_test_123","amount_received":0,"currency":"usd"}}}' \
  'STRIPE_DEPOSIT_WEBHOOK_URL'
```

**Expected behavior:**
- Module 3 filter checks `stripe_event_type = payment_intent.succeeded`
- Filter BLOCKS (event type is `payment_intent.created`)
- No Airtable update
- No Slack message

**Pass criteria:** Make run history shows exit at Module 3. No Bookings records modified.

---

## FAILURE TEST 4: Stripe Deposit — Booking Already DEPOSIT_PAID (Idempotency)

**Intent:** Verify duplicate payment webhooks don't double-update records

**Setup:**
1. Create/find a Booking record with Status=DEPOSIT_PAID
2. Note its Stripe_Payment_Intent_ID (or set it manually)

**Action:** POST a simulated webhook for that payment_intent_id

**Expected behavior:**
- Module 4 finds the booking record
- Module 5 filter checks Status ≠ DEPOSIT_PAID → BLOCKS (status is already DEPOSIT_PAID)
- No update occurs

**Pass criteria:** Booking Status remains DEPOSIT_PAID with no Last_Automation_Timestamp change.

---

## FAILURE TEST 5: Booking Confirmation — Automations Paused

**Intent:** Verify Automations_Paused flag prevents outbound comms

**Setup:**
1. Update a test Booking: Status=CONFIRMED, Automations_Paused=true, Confirmation_Sent=false
2. Trigger M-BOOKING-CONFIRMATION polling run

**Expected behavior:**
- Module 2 checks `Automations_Paused ≠ true`
- Filter BLOCKS
- No email sent
- No SMS sent
- Confirmation_Sent remains false

**Pass criteria:** No email received. Confirmation_Sent still false. Make history shows exit at Module 2.

---

## FAILURE TEST 6: Booking Confirmation — Emergency Flag

**Intent:** Verify Emergency_Flag prevents outbound comms

**Setup:**
1. Update a test Booking: Status=CONFIRMED, Emergency_Flag=true, Automations_Paused=false, Confirmation_Sent=false
2. Trigger polling run

**Expected behavior:**
- Module 2 passes (Automations_Paused=false)
- Module 3 checks Emergency_Flag ≠ true → BLOCKS
- No email sent

**Pass criteria:** No email received. Make history shows exit at Module 3.

---

## FAILURE TEST 7: Booking Confirmation — Concierge Not Assigned

**Intent:** Verify confirmation requires concierge assignment

**Setup:**
1. Update test Booking: Status=CONFIRMED, Concierge_Assigned=false, Emergency_Flag=false, Automations_Paused=false, Confirmation_Sent=false

**Expected behavior:**
- Modules 2, 3 pass
- Module 4 checks Concierge_Assigned = true → BLOCKS (it's false)
- No email sent

**Pass criteria:** No confirmation email. Make history shows exit at Module 4.

---

## FAILURE TEST 8: Concierge Assignment — No Concierge Found

**Intent:** Verify the no-concierge-found path triggers correct alert

**Setup:**
1. Set test Booking: Status=DEPOSIT_PAID, Concierge_Assigned=false, City="ZZZNONEXISTENTCITY"
2. Wait for M-CONCIERGE-ASSIGNMENT polling

**Expected behavior:**
- Module 4 searches Concierge_Operators for City=ZZZNONEXISTENTCITY → finds nothing
- Router Branch 2 (no concierge found) executes
- Slack #sss-ops-alerts receives WARNING: "No Concierge Found"
- Audit Log entry with approval_state=PENDING_HUMAN
- Concierge_Assigned remains false

**Pass criteria:** Slack WARNING received. Airtable unchanged. Audit log shows PENDING_HUMAN.

---

## FAILURE TEST 9: Brand Router — Unknown Source URL

**Intent:** Verify UNKNOWN classification triggers alert

Already covered in Test 1.7, but verify specifically:

**Pass criteria:**
- Slack #sss-ops-alerts receives WARNING
- OPS-LOGGER-ALERTER audit log records the UNKNOWN event

---

## FAILURE TEST 10: Booking Creation — Duplicate (Idempotency)

**Intent:** Verify idempotency key prevents duplicate bookings

**Setup:**
1. Verify a test Booking already exists for a specific Request record (idempotency_key exists)
2. Manually trigger M-BOOKING-CREATION again for the same request

**Expected behavior:**
- Module 3 finds existing booking with matching idempotency_key
- Module 4 BLOCKS (booking exists)
- No new booking created
- No Stripe API call made
- No email sent

**Pass criteria:** Only one Booking record exists for this Request. Make history shows exit at Module 4.

---

## FAILURE REMEDIATION GUIDE

If a failure test does NOT produce the expected behavior:

| Failure | Check |
|---------|-------|
| Filter not blocking | Verify field name in condition matches Airtable field name exactly |
| Wrong Slack channel | Verify Slack OAuth connection is bound to correct workspace |
| Airtable record not found | Verify table ID and base ID are correct |
| Stripe call failing | Verify Stripe key format (Bearer prefix, no extra spaces) |
| Alert not appearing in Slack | Verify channel exists and bot has been added to channel |
| Make run history empty | Verify scenario is active (not paused) |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — FAILURE_TESTS.md*
