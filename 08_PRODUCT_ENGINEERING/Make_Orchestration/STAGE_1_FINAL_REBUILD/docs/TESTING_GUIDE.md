# TESTING GUIDE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Status:** SANDBOX TESTING — use Sandbox environment flag for all tests

---

## TESTING PRINCIPLES

1. All tests use `Environment: Sandbox` or test email/phone addresses
2. All Stripe tests use TEST mode (sk_test_...)
3. Verify audit log entry after each test
4. Verify Slack notification after each test
5. Never run tests against real booking records unless instructed

---

## TEST ENVIRONMENT SETUP

Before running tests:
- [ ] Stripe is in TEST mode
- [ ] A test Request record exists in Airtable (Status: NEW, Environment: Sandbox)
- [ ] A test Booking record exists in Airtable (Status: AVAILABILITY_CONFIRMED, Environment: Sandbox)
- [ ] Concierge_Operators table has at least one Active record

---

## TEST 1: Ops Logger Alerter — Log Only

**Scenario:** SSS-OPS-LOGGER-ALERTER  
**Trigger:** POST to OPS_LOGGER_ALERTER_WEBHOOK_URL  
**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_1_log_only`

**Expected results:**
- [ ] HTTP 200 response received
- [ ] Airtable Audit Log: new record created with correct fields
- [ ] Slack: NO message (alert_type not provided)

---

## TEST 2: Ops Logger Alerter — OPS Alert

**Scenario:** SSS-OPS-LOGGER-ALERTER  
**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_2_ops_alert`

**Expected results:**
- [ ] Airtable Audit Log: record created
- [ ] Slack #sss-ops-alerts: message with 🟢 icon received

---

## TEST 3: Ops Logger Alerter — LEAD Alert

**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_3_lead_alert`

**Expected results:**
- [ ] Airtable Audit Log: record created
- [ ] Slack #sss-lead-intake: lead notification message received

---

## TEST 4: Ops Logger Alerter — EMERGENCY Alert

**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_4_emergency_alert`

**Expected results:**
- [ ] Airtable Audit Log: record created
- [ ] Slack #sss-emergency-ops: EMERGENCY message received with 🚨 icon

---

## TEST 5: Brand Router — SSS Classification

**Scenario:** SSS-BRAND-ROUTER  
**Trigger:** POST to BRAND_ROUTER_WEBHOOK_URL  
**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_5_brand_sss`

**Expected results:**
- [ ] Response body: `{"brand": "SSS", "brand_name_full": "She Said Sail", "routing_confidence": "HIGH"}`
- [ ] Airtable Requests: record Brand field updated to SSS (if request_record_id is a valid record ID)

---

## TEST 6: Brand Router — ME Classification

**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_6_brand_me`

**Expected results:**
- [ ] Response body: `{"brand": "ME", "brand_name_full": "Mare Executive", ...}`

---

## TEST 7: Brand Router — UNKNOWN Classification

**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_7_brand_unknown`

**Expected results:**
- [ ] Response body contains `"brand": "UNKNOWN"`
- [ ] Slack #sss-ops-alerts: WARNING alert about unknown brand

---

## TEST 8: Lead Intake — Full Flow

**Scenario:** SSS-LEAD-INTAKE  
**Trigger:** POST to LEAD_INTAKE_WEBHOOK_URL  
**Test payload:** See `testing/TEST_PAYLOADS.json` → `test_8_lead_intake`

**Expected results:**
- [ ] Airtable Requests: new record created with Status=NEW
- [ ] Gmail: auto-reply sent to test email address
- [ ] Slack #sss-lead-intake: lead notification message
- [ ] Airtable Audit Log: entry created
- [ ] Idempotency: submit SAME payload again → no new record created (verify only 1 record exists)

---

## TEST 9: Lead Intake — Idempotency Check

**Action:** Submit the same TEST 8 payload again (identical email + preferred_date + guest_count)

**Expected results:**
- [ ] NO new Airtable record created
- [ ] Scenario exits silently at Module 4 filter

---

## TEST 10: Stripe Deposit — Payment Received

**Scenario:** SSS-STRIPE-DEPOSIT  
**Trigger:** Use Stripe Dashboard → Developers → Webhooks → Send test webhook  
**Event:** `payment_intent.succeeded`

=== STRIPE TEST MODE REQUIRED ===

Before testing:
1. Create a test Booking record in Airtable with Status=DEPOSIT_SENT, Environment=Production
2. Note the record ID
3. Create a Stripe test payment intent with metadata `booking_id` set to that record ID
4. Send the webhook event

**Expected results:**
- [ ] Airtable Bookings: Status updated to DEPOSIT_PAID
- [ ] Stripe_Payment_Intent_ID field populated
- [ ] Slack #sss-ops-alerts: deposit confirmed message
- [ ] Audit Log entry created

**Idempotency test:** Send same webhook event again
- [ ] Module 5 filter blocks (Status already DEPOSIT_PAID)
- [ ] No duplicate update

---

## TEST 11: Booking Creation — End to End

**Scenario:** SSS-BOOKING-CREATION  
**Trigger:** Set a test Request record Status to AVAILABILITY_CONFIRMED

=== STRIPE TEST MODE REQUIRED ===

Setup:
1. Create or update an Airtable Request record:
   - Status: AVAILABILITY_CONFIRMED
   - Environment: Production
   - Base Price: 200 (for $100 deposit = 10000 cents)
   - All required fields populated

Expected results:
- [ ] Airtable Bookings: new record created with Status=AVAILABILITY_CONFIRMED
- [ ] Stripe: price created via /v1/prices → price ID appears in Booking record
- [ ] Stripe: payment link created via /v1/payment_links → URL appears in Booking record
- [ ] Airtable Bookings: Status updated to DEPOSIT_SENT
- [ ] Gmail: deposit email sent to client with payment link
- [ ] Quo SMS: text message sent (verify if Quo is in test mode)
- [ ] Slack #sss-ops-alerts: booking created notification
- [ ] Audit Log entry created

**Idempotency test:** Run scenario again with same request
- [ ] Module 4 filter blocks — no duplicate booking created

---

## TEST 12: Concierge Assignment — Found

**Scenario:** SSS-CONCIERGE-ASSIGNMENT  
**Trigger:** Update a test Booking record Status to DEPOSIT_PAID

Setup:
1. Verify Concierge_Operators has an Active record for the booking's City
2. Update test Booking: Status=DEPOSIT_PAID, Concierge_Assigned=false, Environment=Production

Expected results:
- [ ] Airtable Bookings: Concierge_Assigned = true
- [ ] Concierge_Name populated with the operator's name
- [ ] Charter Notes updated with assignment entry
- [ ] Slack #sss-ops-alerts: concierge assigned notification
- [ ] Audit Log entry

---

## TEST 13: Concierge Assignment — Not Found

Setup:
1. Set booking City to a city with NO active concierge operator

Expected results:
- [ ] Concierge_Assigned remains false
- [ ] Slack #sss-ops-alerts: WARNING — manual assignment required
- [ ] Audit Log entry with approval_state=PENDING_HUMAN

---

## TEST 14: Booking Confirmation — Full Flow

**Scenario:** SSS-BOOKING-CONFIRMATION  
**Trigger:** Update test Booking Status to CONFIRMED

Setup:
1. Booking record: Status=CONFIRMED, Concierge_Assigned=true, Confirmation_Sent=false, Automations_Paused=false, Emergency_Flag=false, Environment=Production
2. Linked Client record in Clients table with real test email

Expected results:
- [ ] Gmail: confirmation email sent to client email
- [ ] Quo SMS: confirmation text sent
- [ ] Airtable Bookings: Confirmation_Sent=true, D0 Sent=true
- [ ] Slack #sss-ops-alerts: confirmation sent notification
- [ ] Audit Log entry

**Idempotency test:** Set Status=CONFIRMED again
- [ ] Module 5 filter blocks (Confirmation_Sent=true)
- [ ] No duplicate email/SMS sent

---

## TEST 15: Safety Gate — Automations Paused

Setup: Set a Booking Automations_Paused=true, Status=CONFIRMED

**Expected results for M-BOOKING-CONFIRMATION:**
- [ ] Module 2 filter blocks
- [ ] No email, SMS, or Slack sent
- [ ] No Airtable updates

---

## PASS CRITERIA

All 15 tests must pass before Stage 1 is considered production-ready.

| Test | Pass | Notes |
|------|------|-------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |
| 6 | | |
| 7 | | |
| 8 | | |
| 9 | | |
| 10 | | |
| 11 | | |
| 12 | | |
| 13 | | |
| 14 | | |
| 15 | | |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — TESTING_GUIDE.md*
