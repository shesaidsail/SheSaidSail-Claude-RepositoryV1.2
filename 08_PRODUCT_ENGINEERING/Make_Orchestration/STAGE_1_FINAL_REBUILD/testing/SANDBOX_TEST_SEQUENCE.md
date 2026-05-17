# SANDBOX TEST SEQUENCE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Step-by-step sandbox test execution guide with commands

---

## SETUP: Install Testing Tool

Use curl (available in any terminal) or Postman to send test payloads.

**curl template:**
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '<PAYLOAD_JSON>' \
  '<WEBHOOK_URL>'
```

---

## PHASE 1: Test Infrastructure Layer (Scenarios 1-2)

### Test 1.1 — OPS-LOGGER-ALERTER: Log Only

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"triggering_event":"Sandbox test 1.1 - log only","source_data":"curl test","output":"Testing log-only path","approval_state":"AUTONOMOUS","brand":"SSS","city":"Miami","environment":"Production","destination":"Airtable Audit Log"}' \
  'OPS_LOGGER_ALERTER_WEBHOOK_URL'
```

**Verify in Airtable:** Audit Log table has new record  
**Verify in Slack:** NO message in any channel  
**Pass:** ✅ / Fail: ❌

---

### Test 1.2 — OPS-LOGGER-ALERTER: OPS Alert

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"triggering_event":"Sandbox test 1.2 - OPS alert","source_data":"curl test","output":"Testing OPS alert path","approval_state":"AUTONOMOUS","brand":"SSS","city":"Miami","environment":"Production","destination":"Slack","alert_type":"OPS","severity":"INFO","title":"Test 1.2 OPS Alert","body":"Sandbox test — OPS routing verification","booking_id":"TEST-1.2"}' \
  'OPS_LOGGER_ALERTER_WEBHOOK_URL'
```

**Verify:** Audit Log record created + Slack #sss-ops-alerts green 🟢 message  
**Pass:** ✅ / Fail: ❌

---

### Test 1.3 — OPS-LOGGER-ALERTER: LEAD Alert

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"triggering_event":"Sandbox test 1.3 - LEAD alert","source_data":"curl test","output":"Testing LEAD routing","approval_state":"AUTONOMOUS","brand":"SSS","city":"Miami","environment":"Production","destination":"Slack","alert_type":"LEAD","severity":"INFO","title":"Test 1.3 Lead Alert","body":"Test lead","booking_id":"TEST-1.3","lead_name":"Test User","occasion":"Birthday","preferred_date":"2026-08-01","guest_count":"6","source":"https://shesaidsail.com"}' \
  'OPS_LOGGER_ALERTER_WEBHOOK_URL'
```

**Verify:** Slack #sss-lead-intake receives lead message  
**Pass:** ✅ / Fail: ❌

---

### Test 1.4 — OPS-LOGGER-ALERTER: EMERGENCY Alert

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"triggering_event":"Sandbox test 1.4 - EMERGENCY alert","source_data":"staged test","output":"Testing emergency routing","approval_state":"FOUNDER_REQUIRED","brand":"SSS","city":"Miami","environment":"Production","destination":"Slack","alert_type":"EMERGENCY","severity":"CRITICAL","title":"STAGED TEST EMERGENCY — IGNORE","body":"Sandbox test only. No action required.","booking_id":"TEST-EMERGENCY"}' \
  'OPS_LOGGER_ALERTER_WEBHOOK_URL'
```

**Verify:** Slack #sss-emergency-ops receives 🚨 EMERGENCY message  
**Pass:** ✅ / Fail: ❌

---

### Test 1.5 — BRAND-ROUTER: SSS Classification

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"source_url":"https://shesaidsail.com/inquire","request_record_id":"PENDING"}' \
  'BRAND_ROUTER_WEBHOOK_URL'
```

**Verify:** Response body contains `"brand":"SSS"` and `"routing_confidence":"HIGH"`  
**Pass:** ✅ / Fail: ❌

---

### Test 1.6 — BRAND-ROUTER: ME Classification

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"source_url":"https://mareexecutive.com/booking","request_record_id":"PENDING"}' \
  'BRAND_ROUTER_WEBHOOK_URL'
```

**Verify:** Response body contains `"brand":"ME"`  
**Pass:** ✅ / Fail: ❌

---

### Test 1.7 — BRAND-ROUTER: UNKNOWN Classification

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"source_url":"https://randomsite.com/form","request_record_id":"PENDING"}' \
  'BRAND_ROUTER_WEBHOOK_URL'
```

**Verify:** Response contains `"brand":"UNKNOWN"` + Slack #sss-ops-alerts WARNING  
**Pass:** ✅ / Fail: ❌

---

## PHASE 2: Test Lead Intake (Scenario 3)

### Test 2.1 — LEAD-INTAKE: First Submission

Use a real email address you can receive at:

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Test","last_name":"User","email":"YOUR_TEST_EMAIL@gmail.com","phone":"+13055550101","yacht":"Azimut 55","experience":"Sunset Sail","duration":"3 hours","preferred_date":"2026-08-01","guest_count":"6","add_ons":"Champagne","occasion":"Birthday","special_requests":"None","source_url":"https://shesaidsail.com/inquire","form_name":"Main Inquiry Form","city":"Miami"}' \
  'LEAD_INTAKE_WEBHOOK_URL'
```

**Verify:** Airtable Requests record (Status=NEW, Brand=SSS) + auto-reply email + Slack lead notification + Audit Log  
**Pass:** ✅ / Fail: ❌

---

### Test 2.2 — LEAD-INTAKE: Duplicate Submission (Idempotency)

Submit the EXACT same payload as Test 2.1.

**Verify:** In Airtable — only ONE request record exists (no duplicate). Make run history shows scenario exited at Module 4.  
**Pass:** ✅ / Fail: ❌

---

## PHASE 3: Test Stripe Deposit (Scenario 4)

### Test 3.1 — Setup: Create a test Booking record in Airtable

1. In Airtable Bookings table, manually create a record:
   - Status: DEPOSIT_SENT
   - Environment: Production
   - Brand: SSS
   - City: Miami
2. Note the record ID (format: `recXXXXXXXXXXXXXX`)

### Test 3.2 — STRIPE-DEPOSIT: Send Test Webhook

In Stripe Dashboard (TEST mode):
1. Go to Developers → Webhooks → your endpoint → Send test webhook
2. Select event: `payment_intent.succeeded`
3. Edit the test payload to include in `data.object.metadata`: `"booking_id": "YOUR_AIRTABLE_RECORD_ID"`
4. Send

**Verify:** Airtable Booking record Status = DEPOSIT_PAID + Stripe_Payment_Intent_ID populated + Slack notification + Audit Log  
**Pass:** ✅ / Fail: ❌

---

## PHASE 4: Test Booking Creation (Scenario 5)

### Test 4.1 — BOOKING-CREATION: Trigger via Airtable

1. Create a test Request record in Airtable:
   - Status: NEW → then update to AVAILABILITY_CONFIRMED
   - Environment: Production
   - Base Price: 200 (=$100 deposit = 10000 cents)
   - All required fields populated
2. Wait for Make polling cycle (up to 15 minutes) OR manually click Run once in Make

**Verify:** Booking record created + Stripe price + payment link URL stored + Booking status=DEPOSIT_SENT + Gmail email + SMS + Audit Log  
**Pass:** ✅ / Fail: ❌

---

## PHASE 5: Test Concierge Assignment (Scenario 6)

### Test 5.1 — CONCIERGE-ASSIGNMENT: Auto-assign

1. Verify Concierge_Operators has an Active record for Miami
2. Find the test Booking from Phase 4
3. Update it: Status=DEPOSIT_PAID, Concierge_Assigned=false
4. Wait for Make polling

**Verify:** Concierge_Assigned=true, Concierge_Name populated, Slack notification  
**Pass:** ✅ / Fail: ❌

---

## PHASE 6: Test Booking Confirmation (Scenario 7)

### Test 6.1 — BOOKING-CONFIRMATION: Send Confirmation

1. Update test Booking: Status=CONFIRMED
2. Ensure: Concierge_Assigned=true, Confirmation_Sent=false, Automations_Paused=false, Emergency_Flag=false
3. Ensure a Clients record is linked with real test email
4. Wait for Make polling

**Verify:** Gmail confirmation email sent + SMS sent + Confirmation_Sent=true + D0 Sent=true + Audit Log  
**Pass:** ✅ / Fail: ❌

---

## PHASE 7: Safety Gate Tests

### Test 7.1 — Automations_Paused Gate

1. Update test Booking: Status=CONFIRMED, Automations_Paused=true, Confirmation_Sent=false
2. Wait for Make polling

**Verify:** NO email/SMS sent. Make run history shows exit at Module 2.  
**Pass:** ✅ / Fail: ❌

### Test 7.2 — Idempotency: Duplicate Confirmation

1. Revert: Automations_Paused=false, Confirmation_Sent=true
2. Wait for Make polling

**Verify:** NO email/SMS sent (already confirmed). Make exits at Module 5.  
**Pass:** ✅ / Fail: ❌

---

## TEST SUMMARY TABLE

| Phase | Test | Description | Pass |
|-------|------|-------------|------|
| 1 | 1.1 | OPS-LOGGER: Log only | |
| 1 | 1.2 | OPS-LOGGER: OPS alert | |
| 1 | 1.3 | OPS-LOGGER: LEAD alert | |
| 1 | 1.4 | OPS-LOGGER: EMERGENCY alert | |
| 1 | 1.5 | BRAND-ROUTER: SSS | |
| 1 | 1.6 | BRAND-ROUTER: ME | |
| 1 | 1.7 | BRAND-ROUTER: UNKNOWN | |
| 2 | 2.1 | LEAD-INTAKE: Full flow | |
| 2 | 2.2 | LEAD-INTAKE: Idempotency | |
| 3 | 3.1 | STRIPE-DEPOSIT: Payment | |
| 4 | 4.1 | BOOKING-CREATION: E2E | |
| 5 | 5.1 | CONCIERGE: Auto-assign | |
| 6 | 6.1 | CONFIRMATION: Send | |
| 7 | 7.1 | Safety gate: Paused | |
| 7 | 7.2 | Safety gate: Idempotency | |

**All 15 must pass before production activation.**

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — SANDBOX_TEST_SEQUENCE.md*
