# BOOKING CREATION — TEST PROCEDURE

**Classification:** Confidential — Internal Use Only
**Owner:** Will (Founder)
**Effective Date:** May 2026
**Scenario:** SSS-BOOKING-CREATION
**Mode:** Stripe TEST MODE only. No live charges. No live client messages.

---

## SAFETY RULES

1. Stripe must be in TEST MODE before running any test — verify in Stripe dashboard (orange "Test mode" banner)
2. All test Airtable records must use `Environment = Sandbox` — this prevents triggering production automation chains
3. Use only test email addresses and test phone numbers you control
4. If any real client receives an unexpected email or SMS: immediately toggle the scenario OFF and alert Will

---

## PREREQUISITES

Before running tests, confirm:

- [ ] `SSS-BOOKING-CREATION` scenario is imported, fully rebound, all placeholders replaced
- [ ] Scenario is currently **OFF** (run tests manually using "Run once")
- [ ] `SSS-AUDIT-LOGGER` scenario is active
- [ ] `SSS-SLACK-ALERTS` scenario is active
- [ ] Airtable Requests table has a test record (see Setup below)
- [ ] Stripe dashboard: TEST MODE confirmed

---

## TEST SETUP — CREATE TEST REQUEST RECORD

In Airtable → She Said Sail base → Requests table, create a record with these values:

| Field | Value |
|-------|-------|
| Status | `NEW` (do not set to AVAILABILITY_CONFIRMED yet) |
| Environment | `Sandbox` |
| First Name | `Test` |
| Last Name | `Booking` |
| Email | your-test-email@yourdomain.com |
| Phone | +15550000001 (or a number you control) |
| Experience | `Sunset Sail 3-Hour` |
| Base Price | `10000` (represents $10,000 — deposit will be $5,000) |
| Preferred Date | `2026-07-01` |
| Guest Count | `8` |
| Occasion | `Birthday` |
| Boarding Location | `Miami Beach Marina` |
| Add-Ons Selected | `None` |
| Special Requests | `TEST RECORD - DO NOT PROCESS` |
| Brand | `SSS` |

Save the record and note its Airtable Record ID (visible in the URL when the record is expanded).

---

## TEST 1 — BOOKING CREATION (CORE TEST)

**Tests:** Full scenario flow from trigger through email + SMS

### Procedure

1. In Make → SSS-BOOKING-CREATION, click **Run once**
2. The scenario enters listening mode (waiting for a triggering record)
3. In Airtable → Requests table, find your test record
4. Change its **Status** field from `NEW` to `AVAILABILITY_CONFIRMED`
5. Wait up to 30 seconds for Make to detect the record

### Expected Execution Path

```
Module 1 (Watch) → detects record
Module 2 (Search) → finds no existing Booking (first run)
Module 3 (Router) → routes to "New booking — process"
Module 4 (Create) → creates Booking record
Module 5 (Stripe) → creates Payment Link (TEST mode)
Module 6 (Update) → sets Status = DEPOSIT_SENT, writes Stripe URL
Module 7 (Filter) → Automations_Paused = false → PASSES
Module 8 (Gmail) → sends deposit email
Module 9 (SMS) → sends SMS via Quo
Module 10 (HTTP) → writes Audit Log
Module 11 (HTTP) → posts Slack alert
```

### Pass Criteria

- [ ] Make execution shows all modules green (no errors)
- [ ] New Booking record exists in Airtable → Bookings table
- [ ] Booking record `Idempotency_Key` = `BOOKING-[request record ID]`
- [ ] Booking record `Status` = `DEPOSIT_SENT`
- [ ] Booking record `Stripe Payment Link` field contains a URL
- [ ] Stripe Payment Link URL format: begins with `https://buy.stripe.com/test_`
- [ ] Deposit email received at test email address
- [ ] Email contains a clickable "Pay Deposit Now" button
- [ ] Email payment link matches the Stripe URL in Airtable
- [ ] Stripe dashboard (test mode) → Payment Links shows the newly created link
- [ ] Audit Log record created in Airtable
- [ ] Slack alert posted to #sss-ops-alerts

### Stripe Payment Link Verification

After the email arrives, click the payment link. Confirm:
- URL begins with `https://buy.stripe.com/test_`
- Stripe checkout page loads showing a deposit amount
- Amount shown = 50% of Base Price (e.g., $5,000 if Base Price was 10000)
- Product name shown = `Sunset Sail 3-Hour — Deposit (50%)`
- Do NOT complete the payment during this test

### Fail Actions

| Symptom | Diagnosis | Fix |
|---------|-----------|-----|
| Module 5 (Stripe) errors | Stripe connection not bound or wrong mode | Rebind Stripe module to TEST connection |
| Module 5 errors with "price_data invalid" | price_data structure corrupted by UI interaction | Re-import `CLEAN_M-BOOKING-CREATION.json` — do not edit Stripe module manually |
| Module 6 errors on "Stripe Payment Link" field | Field doesn't exist in Airtable | Create URL field named exactly `Stripe Payment Link` in Bookings table |
| Module 8 (Gmail) errors | Gmail connection unbound | Rebind Gmail to hello@shesaidsail.com |
| Module 10 (Audit Logger) errors | Placeholder URL not replaced | Replace URL in module 10 |
| Module 11 (Slack Alerts) errors | Placeholder URL not replaced | Replace URL in module 11 |
| Stripe link is NOT in test format | Stripe connection is LIVE mode | Stop immediately — switch Stripe to test mode, rebind module 5 |

---

## TEST 2 — IDEMPOTENCY (DUPLICATE PREVENTION)

**Tests:** Router filter prevents duplicate booking on re-trigger

### Procedure

1. In Make, click **Run once** again
2. The test record in Airtable still has `Status = AVAILABILITY_CONFIRMED`
3. Make searches for an existing Booking with `Idempotency_Key = BOOKING-[same record ID]`

### Expected Execution Path

```
Module 1 (Watch) → detects record (still AVAILABILITY_CONFIRMED)
Module 2 (Search) → finds existing Booking record
Module 3 (Router) → {{2.id}} is NOT empty → filter condition fails → route skipped
```

All modules 4–11 should NOT execute.

### Pass Criteria

- [ ] Make execution completes without error
- [ ] No new Booking record created in Airtable (still only 1 Booking for this request)
- [ ] No second deposit email sent
- [ ] No second SMS sent
- [ ] Make execution log shows modules 4–11 were skipped (router filter blocked them)

---

## TEST 3 — AUTOMATIONS_PAUSED GATE

**Tests:** Module 7 filter exits scenario if Automations_Paused is true

### Procedure

1. In Airtable → Bookings table, find the Booking created in Test 1
2. Manually set `Automations_Paused` = true (check the checkbox)
3. Delete that Booking record (so idempotency won't block the next test run)
4. In Make, click **Run once**
5. The trigger fires on the same Request record

### Expected Execution Path

```
Module 1 → detects record
Module 2 → no existing Booking (we deleted it)
Module 3 → routes to "New booking — process"
Module 4 → creates new Booking record (with Automations_Paused = false, as hardcoded)
Module 5 → creates Stripe Payment Link
Module 6 → updates Booking to DEPOSIT_SENT
Module 7 → Automations_Paused = false (because module 4 creates it as false) → PASSES
```

**Note:** The Automations_Paused gate in module 7 checks the value SET by the booking creation in module 4. Since module 4 always creates bookings with `Automations_Paused = false`, module 7 will always pass on initial creation. This gate protects against scenarios where the booking record is mutated between creation and outbound dispatch (future use).

### Cleanup

After this test, reset the Airtable test environment:
- Set the test Request record Status back to `NEW` or delete it
- Set the test Booking record Environment to `Sandbox` if it was set to Production

---

## TEST 4 — STRIPE PAYMENT LINK AMOUNT VERIFICATION

**Tests:** Deposit calculation is correct (50% of Base Price, in cents)

### Calculation Check

Given the test record with `Base Price = 10000`:
- Formula: `round(multiply(toNumber(10000); 50))` = `round(500000)` = `500000`
- Stripe receives `unit_amount = 500000` (cents)
- Stripe displays: **$5,000.00**

### Verification

1. Open the Stripe Payment Link from Test 1 in a browser
2. Confirm the checkout page shows: $5,000.00
3. Confirm the product name: `Sunset Sail 3-Hour — Deposit (50%)`
4. Confirm the description: `Deposit for Test Booking — 2026-07-01`

### Pass Criteria

- [ ] Amount shown = $5,000 (50% of $10,000 Base Price)
- [ ] Product name correct
- [ ] Deposit description includes client name and date

---

## POST-TEST CLEANUP

After all tests pass:

1. In Airtable → Requests table: set test record Status back to `NEW` and Environment to `Sandbox`
2. In Airtable → Bookings table: delete test Booking records created during testing
3. In Stripe (test mode) → Payment Links: created test links can remain (they are test-only)
4. In Make: toggle SSS-BOOKING-CREATION from "Run once" mode to active schedule

---

## ACTIVATION

After all 4 tests pass:

1. Toggle `SSS-BOOKING-CREATION` scenario **ON**
2. Set schedule: Every 15 minutes
3. Record the scenario ID in Airtable → Make_Scenarios table
4. Notify Will that Booking Creation is live

---

## PASS SUMMARY

| Test | Description | Result |
|------|-------------|--------|
| 1 — Core flow | Booking created, Stripe link generated, email + SMS sent | ☐ |
| 2 — Idempotency | No duplicate booking on re-trigger | ☐ |
| 3 — Automations_Paused | Gate present and verified | ☐ |
| 4 — Amount check | Deposit = 50% of Base Price, formatted correctly | ☐ |

**All 4 must pass before scenario is declared production-ready.**

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*
*08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/docs/BOOKING-CREATION-TESTING.md*
