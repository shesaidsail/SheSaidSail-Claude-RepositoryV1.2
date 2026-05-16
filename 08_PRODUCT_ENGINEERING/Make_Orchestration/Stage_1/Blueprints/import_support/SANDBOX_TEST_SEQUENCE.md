# SANDBOX TEST SEQUENCE — Stage 1 Make Scenarios
**Version:** 1.0
**Date:** 2026-05-16
**Purpose:** Step-by-step sandbox validation tests for all 8 Stage 1 scenarios

---

## Prerequisites

Before running any test:
- [ ] All 8 scenarios imported and configured (see MAKE_IMPORT_INSTRUCTIONS.md)
- [ ] All credentials reconnected (see CREDENTIAL_REBINDING_CHECKLIST.md)
- [ ] All webhook URLs updated in HTTP modules (see WEBHOOK_REGISTRATION_CHECKLIST.md)
- [ ] All scenarios connected to SANDBOX Airtable base (NOT appdZ49WqgjRXxA1R production)
- [ ] Stripe in TEST mode
- [ ] Gmail sending to test email addresses ONLY (use your own email or a test inbox)
- [ ] SMS sending to a test phone number you own
- [ ] All scenarios are ACTIVE (turned ON) in Make — they must be active to receive webhook calls

---

## Test Environment Setup

| Item | Sandbox Value |
|------|--------------|
| Airtable Base | Sandbox base (NOT appdZ49WqgjRXxA1R) |
| Stripe Mode | Test (toggle ON in Stripe Dashboard) |
| Email Recipients | Your test email (e.g., will+test@shesaidsail.com) |
| Phone Recipients | Your test phone number |
| Slack Channels | Same channels (messages will appear but are test data) |
| Environment Field | Set to "sandbox" in all test payloads |

---

## TEST 1 — M-AUDIT-LOGGER Baseline

**Goal:** Confirm the audit logger receives events and writes to Airtable.

```bash
curl -X POST [M-AUDIT-LOGGER-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-AUDIT-LOGGER.test.json
```

**Expected Results:**
- [ ] HTTP 200 response from Make
- [ ] New record created in Audit Log table in sandbox Airtable
- [ ] Record contains: Scenario_ID, Event_Type, Brand, Record_ID, Timestamp, Environment="sandbox"

**Idempotency Test:**
- Send the same payload a second time (same idempotency_key)
- Expected: HTTP 200 but NO second Airtable record created

---

## TEST 2 — M-SLACK-ALERTS Baseline

**Goal:** Confirm Slack routing works for all 4 alert types.

**Test 2a — New Lead alert:**
```bash
curl -X POST [M-SLACK-ALERTS-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d '{"alert_type":"NEW_LEAD","brand":"SSS","message":"TEST: New lead received","record_id":"TEST-001","urgency":"LOW","metadata":{"lead_name":"Test User","city":"Miami","date_requested":"2026-06-15","budget_range":"$3,000-$5,000"},"timestamp":"2026-05-16T10:00:00Z"}'
```
- Expected: Message appears in #sss-leads

**Test 2b — Booking alert:**
- Send with alert_type="BOOKING_CREATED"
- Expected: Message in #sss-bookings

**Test 2c — Emergency alert:**
- Send with alert_type="EMERGENCY", urgency="CRITICAL"
- Expected: Message in #sss-emergency-ops AND DM to Will

---

## TEST 3 — M-BRAND-ROUTER → M-LEAD-INTAKE Chain

**Goal:** Confirm brand routing and lead creation work end-to-end.

```bash
curl -X POST [M-BRAND-ROUTER-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-BRAND-ROUTER.test.json
```

**Expected Results:**
- [ ] M-BRAND-ROUTER executes, routes to SSS path
- [ ] M-LEAD-INTAKE webhook is called (check M-LEAD-INTAKE execution log in Make)
- [ ] New Request record created in sandbox Airtable with Status="NEW", Agent_Status="HUMAN_REVIEW"
- [ ] M-AUDIT-LOGGER called and record created
- [ ] M-SLACK-ALERTS called and Slack message appears in #sss-leads

**Duplicate Test:**
- Send the same payload again (same email address)
- Expected: M-LEAD-INTAKE detects duplicate, updates existing record (does NOT create second record)

---

## TEST 4 — M-LEAD-INTAKE Standalone

**Goal:** Test lead intake directly without brand router.

```bash
curl -X POST [M-LEAD-INTAKE-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-LEAD-INTAKE.test.json
```

**Expected Results:**
- [ ] New Request record in sandbox Airtable with all fields populated
- [ ] Audit log entry created
- [ ] Slack lead alert sent

---

## TEST 5 — M-CONCIERGE-ASSIGNMENT

**Goal:** Confirm concierge lookup and assignment.

**Setup:** Create a test Concierge_Operators record in sandbox Airtable with:
- City = "Miami"
- Brand = "SSS"
- Status = "ACTIVE"
- Available = true
- Name = "Test Concierge"
- Email = your test email

Then create a test Request record in sandbox Airtable and note its record ID.

```bash
curl -X POST [M-CONCIERGE-ASSIGNMENT-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-CONCIERGE-ASSIGNMENT.test.json
```

**Expected Results:**
- [ ] Request record updated: Assigned_Concierge set, Status="CONCIERGE_ASSIGNED"
- [ ] Notification email sent to test concierge email
- [ ] Slack alert in #sss-ops
- [ ] Audit log entry created

**No-Concierge Test:**
- Set test Concierge_Operators record Available = false
- Send same request → Expected: Status set to "NEEDS_MANUAL_ASSIGNMENT", Slack high-urgency alert

---

## TEST 6 — M-STRIPE-DEPOSIT

**Goal:** Confirm Stripe Payment Link creation and communication.

**Setup:** Create a test Booking record in sandbox Airtable with Status="DEPOSIT_READY".

```bash
curl -X POST [M-STRIPE-DEPOSIT-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-STRIPE-DEPOSIT.test.json
```

**Expected Results:**
- [ ] Stripe test payment link created (visible in Stripe Test Dashboard)
- [ ] Booking record updated: Deposit_Link set, Status="DEPOSIT_SENT"
- [ ] Deposit request email sent to test email
- [ ] SMS sent to test number
- [ ] Audit log entry created
- [ ] Slack STRIPE_LINK_SENT alert sent

---

## TEST 7 — M-BOOKING-CREATION (Stripe Webhook Simulation)

**Goal:** Confirm booking creation from Stripe payment event.

**Method 1 — Stripe Dashboard Test Event:**
1. Go to Stripe Dashboard → Developers → Webhooks
2. Click on your registered sandbox webhook endpoint
3. Click **Send test event**
4. Select event: `payment_intent.succeeded`
5. Edit the metadata to include: `{"booking_id":"[sandbox-booking-record-id]","brand":"SSS","environment":"sandbox","type":"deposit"}`
6. Send

**Expected Results:**
- [ ] Make receives Stripe webhook event
- [ ] Idempotency check runs (search for Stripe_Payment_Intent_ID)
- [ ] Booking record created in sandbox Airtable with Status="DEPOSIT_PAID"
- [ ] Request record updated: Status="DEPOSIT_PAID"
- [ ] M-BOOKING-CONFIRMATION triggered (check execution log)
- [ ] Audit log entry created
- [ ] Slack BOOKING_CREATED alert sent

**Idempotency Test:**
- Send the same Stripe test event again
- Expected: Make detects duplicate payment_intent.id, skips booking creation, logs DUPLICATE_WEBHOOK

---

## TEST 8 — M-BOOKING-CONFIRMATION

**Goal:** Confirm confirmation emails and SMS are sent correctly.

```bash
curl -X POST [M-BOOKING-CONFIRMATION-WEBHOOK-URL] \
  -H "Content-Type: application/json" \
  -d @M-BOOKING-CONFIRMATION.test.json
```

**Expected Results:**
- [ ] SSS confirmation email received at test inbox (from hello@shesaidsail.com)
- [ ] SMS received at test number
- [ ] Booking record updated: Confirmation_Sent_At set, Status="CONFIRMED" or "AGREEMENT_PENDING"
- [ ] Slack BOOKING_CONFIRMED alert in #sss-bookings
- [ ] Audit log entry created

**ME Brand Test:**
- Send same payload with brand="ME"
- Expected: Email from hello@mareexecutive.com with ME branding

---

## TEST 9 — End-to-End Full Chain Test

**Goal:** Validate the complete Stage 1 flow from lead intake to booking confirmation.

1. POST to M-BRAND-ROUTER with SSS lead data
2. Verify Request record created in sandbox Airtable
3. Manually update Request Status to "AVAILABILITY_CONFIRMED" in sandbox Airtable
4. POST to M-CONCIERGE-ASSIGNMENT with the new Request record ID
5. Verify concierge assigned
6. Create a Booking record linked to the Request
7. POST to M-STRIPE-DEPOSIT with the Booking record ID
8. Verify deposit link created, email/SMS sent
9. Simulate Stripe payment via Stripe Dashboard test event
10. Verify Booking Status = "DEPOSIT_PAID", M-BOOKING-CONFIRMATION triggered
11. Verify confirmation email and SMS received
12. Verify all Audit Log entries exist for each step

**Expected: All 8 scenarios executed, all records updated, all communications sent.**

---

## Sandbox Test Pass Criteria

All tests must pass before production activation is authorized:

| Test | Status | Pass/Fail | Notes |
|------|--------|-----------|-------|
| TEST 1 — Audit Logger Baseline | | | |
| TEST 1 — Idempotency | | | |
| TEST 2a — Slack New Lead | | | |
| TEST 2b — Slack Booking | | | |
| TEST 2c — Slack Emergency | | | |
| TEST 3 — Brand Router Chain | | | |
| TEST 3 — Duplicate Detection | | | |
| TEST 4 — Lead Intake Standalone | | | |
| TEST 5 — Concierge Assignment | | | |
| TEST 5 — No Concierge Available | | | |
| TEST 6 — Stripe Deposit Link | | | |
| TEST 7 — Booking Creation | | | |
| TEST 7 — Stripe Idempotency | | | |
| TEST 8 — Booking Confirmation (SSS) | | | |
| TEST 8 — Booking Confirmation (ME) | | | |
| TEST 9 — End-to-End Full Chain | | | |

**Final Approval:**
- [ ] All tests passed
- [ ] Will reviewed results
- [ ] Production enable authorized
