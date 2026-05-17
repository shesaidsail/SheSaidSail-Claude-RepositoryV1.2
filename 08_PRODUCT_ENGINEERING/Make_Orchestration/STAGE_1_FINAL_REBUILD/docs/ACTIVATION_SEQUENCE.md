# ACTIVATION SEQUENCE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Ordered activation steps after all scenarios are imported and rebound

This document covers the FINAL activation sequence — the last steps before Stage 1 is live and processing real data.

---

## PRE-ACTIVATION GATES

ALL of the following must be true before activating any scenario:

- [ ] All 7 blueprints imported successfully
- [ ] All connection rebinding complete (no red indicators)
- [ ] All placeholder values replaced (no PASTE_...HERE strings remain)
- [ ] Airtable pre-work complete (all required fields exist)
- [ ] Slack channels exist: #sss-emergency-ops, #sss-lead-intake, #sss-ops-alerts
- [ ] All 15 sandbox tests passed (see TESTING_GUIDE.md)
- [ ] Stripe is in TEST mode for initial activation
- [ ] Founder Decision record created in Airtable (Type: SYSTEM, documenting Stage 1 activation)

=== DO NOT PROCEED WITHOUT ALL GATES PASSING ===

---

## ACTIVATION ORDER

Activate one scenario at a time. Verify each before proceeding.

### ACTIVATE 1: SSS-OPS-LOGGER-ALERTER

1. Toggle scenario to ON in Make
2. Send test payload: `{"triggering_event": "Stage 1 Activation", "environment": "Production", "brand": "SSS", "city": "Miami", "alert_type": "OPS", "severity": "INFO", "title": "Stage 1 Activation Complete", "body": "SSS-OPS-LOGGER-ALERTER is now live."}`
3. Verify: Airtable Audit Log record created
4. Verify: Slack #sss-ops-alerts receives message
5. Status: ✅ ACTIVE

### ACTIVATE 2: SSS-BRAND-ROUTER

1. Toggle to ON
2. Send test: `{"source_url": "https://shesaidsail.com/test", "request_record_id": "test"}`
3. Verify: response body contains brand=SSS
4. Status: ✅ ACTIVE

### ACTIVATE 3: SSS-LEAD-INTAKE

1. Toggle to ON
2. === TEST WEBFLOW FORM === Submit the Webflow inquiry form with test data
3. Verify: Requests record created, auto-reply email sent, Slack notification
4. Status: ✅ ACTIVE

### ACTIVATE 4: SSS-STRIPE-DEPOSIT

1. Toggle to ON
2. === STRIPE TEST === Use Stripe Dashboard → Send test webhook → payment_intent.succeeded
3. Verify: scenario receives event, processes through filter gates
4. Status: ✅ ACTIVE

### ACTIVATE 5: SSS-BOOKING-CREATION

1. Toggle to ON (schedule: every 15 minutes)
2. Status: ✅ ACTIVE (will fire when a Request reaches AVAILABILITY_CONFIRMED)

### ACTIVATE 6: SSS-CONCIERGE-ASSIGNMENT

1. Toggle to ON (schedule: every 15 minutes)
2. Status: ✅ ACTIVE (will fire when a Booking reaches DEPOSIT_PAID with Concierge_Assigned=false)

### ACTIVATE 7: SSS-BOOKING-CONFIRMATION

1. Toggle to ON (schedule: every 15 minutes)
2. Status: ✅ ACTIVE (will fire when a Booking reaches CONFIRMED with Confirmation_Sent=false)

---

## POST-ACTIVATION STATUS TRACKING

Fill this in during activation:

| Scenario | Activated | Activated At | First Run Status | Notes |
|----------|-----------|--------------|-----------------|-------|
| SSS-OPS-LOGGER-ALERTER | ☐ | | | |
| SSS-BRAND-ROUTER | ☐ | | | |
| SSS-LEAD-INTAKE | ☐ | | | |
| SSS-STRIPE-DEPOSIT | ☐ | | | |
| SSS-BOOKING-CREATION | ☐ | | | |
| SSS-CONCIERGE-ASSIGNMENT | ☐ | | | |
| SSS-BOOKING-CONFIRMATION | ☐ | | | |

---

## SWITCHING FROM TEST TO LIVE STRIPE

After all sandbox testing is complete:

=== MANUAL ACTION REQUIRED ===
=== FOUNDER AUTHORIZATION REQUIRED ===

1. Create a Founder Decision record (Type: SYSTEM) documenting the Stripe live switch
2. In SSS-BOOKING-CREATION:
   - Open Module 6 → Authorization header → Replace sk_test_ with sk_live_
   - Open Module 7 → Authorization header → Replace sk_test_ with sk_live_
   - Save scenario
3. In Stripe Dashboard → Switch to LIVE mode:
   - Add new webhook endpoint with STRIPE_DEPOSIT_WEBHOOK_URL
   - Event: payment_intent.succeeded
   - Copy new signing secret
4. Run one real test transaction with minimum value to confirm end-to-end
5. Document in Audit Log

---

## ONGOING OPERATIONS

After activation:
- Monitor Make scenario run history for errors (Make → History)
- Monitor Airtable Audit Log for any PENDING_HUMAN entries requiring action
- Monitor Slack #sss-ops-alerts daily
- Check Make billing/operations quota monthly

Scheduled scenario polling interval: 15 minutes (default)
Adjust in Make → Scenario Settings → Scheduling if needed.

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — ACTIVATION_SEQUENCE.md*
