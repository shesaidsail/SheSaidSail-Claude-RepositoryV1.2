# STAGE 1 ACTIVATION SEQUENCE
## She Said Sail — Make Orchestration

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  

---

## ACTIVATION PREREQUISITES

All of the following must be true before activating any scenario:

- [ ] All 8 blueprints imported into Make
- [ ] All credentials bound per `CREDENTIAL_REBINDING_CHECKLIST.md`
- [ ] All scenarios validated in Sandbox
- [ ] Webflow webhook registered
- [ ] Stripe webhook registered
- [ ] Airtable Audit Log table live with required fields
- [ ] Airtable Requests table has Agent_Status field
- [ ] Airtable Bookings table has Confirmation_Sent and Concierge_Assigned fields
- [ ] Will has reviewed and approved activation
- [ ] Deployment Log record pre-created (fill in timestamps as you go)

---

## ACTIVATION SEQUENCE

### Day 1 — Infrastructure Layer

**Time required:** ~2 hours

**10:00 AM — Activate M-AUDIT-LOGGER**
1. Open M-AUDIT-LOGGER in Make
2. Toggle scenario to ON
3. Test: POST to webhook URL with sample audit payload
4. Verify: Airtable Audit Log table receives new record
5. Log: Status = ACTIVE, timestamp = (now)
6. Wait 5 minutes — confirm no errors in execution history

**10:15 AM — Activate M-SLACK-ALERTS**
1. Open M-SLACK-ALERTS in Make
2. Toggle scenario to ON
3. Test SEV-1: POST with alert_level=SEV-1
4. Verify: message in #sss-emergency-ops AND Will DM
5. Test SEV-2: POST with alert_level=SEV-2
6. Verify: message in #sss-ops-alerts only
7. Log: Status = ACTIVE, timestamp = (now)

**10:30 AM — Activate M-BRAND-ROUTER**
1. Open M-BRAND-ROUTER in Make
2. Toggle scenario to ON
3. Test SSS: POST with source=shesaidsail.com
4. Verify: response body contains brand=SSS
5. Test ME: POST with form_brand=mare
6. Verify: response body contains brand=ME
7. Log: Status = ACTIVE, timestamp = (now)

**10:45 AM — Infrastructure Checkpoint**
- [ ] M-AUDIT-LOGGER: ACTIVE, responding correctly
- [ ] M-SLACK-ALERTS: ACTIVE, routing correctly
- [ ] M-BRAND-ROUTER: ACTIVE, classifying correctly
- Infrastructure layer confirmed. Proceed to operational layer.

---

### Day 1 — Operational Lead Intake

**11:00 AM — Activate M-LEAD-INTAKE**
1. Open M-LEAD-INTAKE in Make
2. Toggle scenario to ON
3. Test: Submit She Said Sail inquiry form (use a test email)
4. Wait up to 30 seconds
5. Verify in Airtable: new Request record with Agent_Status=AI_RESPONDING
6. Verify in Slack: notification in #sss-ops-alerts
7. Verify in Airtable Audit Log: new entry with Action_Type=REQUEST_CREATED
8. Test deduplication: submit same email again immediately
9. Verify: no duplicate Request record created
10. Log: Status = ACTIVE, timestamp = (now)

**11:30 AM — Lead Intake Confirmed**
- [ ] M-LEAD-INTAKE: ACTIVE, creating Requests correctly

---

### Day 2 — Stripe & Booking Layer

**Day 2 is intentionally separate.** Stripe scenarios affect financial records. Validate Day 1 fully before proceeding.

**Morning — Confirm Day 1 Scenarios Still Running Clean**
- Check Make execution history for M-LEAD-INTAKE
- Check Airtable Audit Log for any errors
- Check #sss-ops-alerts for any anomalies
- If clean: proceed to Stripe activation

**10:00 AM — Activate M-STRIPE-DEPOSIT**
1. Open M-STRIPE-DEPOSIT in Make
2. Toggle scenario to ON
3. In Airtable test base: create a test Booking with Status=AVAILABILITY_CONFIRMED, Deposit_Link_Sent=false
4. Wait up to 5 minutes (polling scenario)
5. Verify: Stripe Payment Link created in Stripe test dashboard
6. Verify: Booking updated to Status=DEPOSIT_SENT
7. Verify: Stripe_Payment_Link_URL populated on Booking record
8. Verify: Deposit confirmation email sent (check test inbox)
9. Verify: Audit Log entry written
10. Log: Status = ACTIVE, timestamp = (now)

**10:30 AM — Activate M-BOOKING-CREATION**
1. Open M-BOOKING-CREATION in Make
2. Toggle scenario to ON
3. In Stripe test mode: send test webhook event checkout.session.completed
4. Include in metadata: booking_id, airtable_record_id (from test Booking), payment_type=deposit, environment=Production
5. Verify: Booking updated to Status=DEPOSIT_PAID
6. Verify: Slack notification in #sss-ops-alerts
7. Verify: Audit Log entry written
8. Test idempotency: send same Stripe event ID again
9. Verify: Booking NOT updated a second time (idempotency working)
10. Log: Status = ACTIVE, timestamp = (now)

**11:00 AM — Activate M-CONCIERGE-ASSIGNMENT**
1. Open M-CONCIERGE-ASSIGNMENT in Make
2. Toggle scenario to ON
3. Test: set test Booking to Status=DEPOSIT_PAID, Concierge_Assigned=false
4. Wait up to 5 minutes (polling scenario)
5. Verify: Booking updated with Concierge_Assigned=true
6. Verify: Luciana receives Slack DM with booking details
7. Test HV: set HV_Client=true on a test Booking at DEPOSIT_PAID
8. Verify: Will also receives Slack DM
9. Verify: Audit Log entry written
10. Log: Status = ACTIVE, timestamp = (now)

**11:30 AM — Activate M-BOOKING-CONFIRMATION**
1. Open M-BOOKING-CONFIRMATION in Make
2. Toggle scenario to ON
3. Test: set test Booking to Status=CONFIRMED, Confirmation_Sent=false, HV_Client=false
4. Wait up to 5 minutes (polling scenario)
5. Verify: confirmation email sent to test email address
6. Verify: Booking updated with Confirmation_Sent=true
7. Verify: Audit Log entry written
8. Test HV guard: set HV_Client=true, set test Booking to CONFIRMED
9. Verify: email NOT sent automatically, Luciana receives DM instead
10. Test emergency guard: set Emergency_Flag=true, Status=CONFIRMED
11. Verify: scenario skips — no email sent
12. Log: Status = ACTIVE, timestamp = (now)

---

### Activation Complete

**Final Checklist:**
- [ ] All 8 scenarios: ACTIVE in Production
- [ ] All audit log entries confirmed writing
- [ ] All Slack notifications confirmed routing
- [ ] Deployment Log entry completed
- [ ] Will notified: Stage 1 is live
- [ ] Luciana briefed: what's automated, what's manual

**Post-Activation Monitoring (First 48 Hours):**
- Check Make execution history every 4 hours
- Check #sss-ops-alerts for alerts
- Check Airtable Audit Log for volume
- Verify first real lead processed correctly when it arrives

---

*She Said Sail · Stage 1 Activation Sequence*  
*CONFIDENTIAL — INTERNAL USE ONLY*
