# STAGE 1 TESTING CHECKLIST
## She Said Sail — Make Orchestration

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  
**Complete this checklist before signing off on any scenario for Production.**

---

## M-AUDIT-LOGGER TESTS

- [ ] **T-AU-01** POST to webhook URL with all required fields → Airtable Audit Log record created
- [ ] **T-AU-02** Response body contains `audit_uuid` and `airtable_record_id`
- [ ] **T-AU-03** `Audit_UUID` field in Airtable record is unique (not empty, not duplicate)
- [ ] **T-AU-04** `Timestamp` field in Airtable record matches current time (within 5s)
- [ ] **T-AU-05** POST with missing `actor` field → scenario handles gracefully (no crash)
- [ ] **T-AU-06** POST with empty body → returns non-500 response

**Pass criteria:** All 6 pass before activating

---

## M-SLACK-ALERTS TESTS

- [ ] **T-SA-01** POST with `alert_level=SEV-1` → message appears in #sss-emergency-ops
- [ ] **T-SA-02** POST with `alert_level=SEV-1` → Will receives DM (separate message)
- [ ] **T-SA-03** POST with `alert_level=SEV-2` → message in #sss-ops-alerts ONLY (no Will DM)
- [ ] **T-SA-04** POST with `alert_level=INFO` → message in #sss-ops-alerts ONLY
- [ ] **T-SA-05** Slack blocks render correctly (not raw JSON)
- [ ] **T-SA-06** Booking ID appears in message when provided
- [ ] **T-SA-07** `N/A` appears for booking_id when not provided

**Pass criteria:** All 7 pass before activating

---

## M-BRAND-ROUTER TESTS

- [ ] **T-BR-01** POST with `source=shesaidsail.com` → response: `brand=SSS`
- [ ] **T-BR-02** POST with `form_brand=mare` → response: `brand=ME`
- [ ] **T-BR-03** POST with `source=mare-executive.com` → response: `brand=ME`
- [ ] **T-BR-04** POST with `form_brand=sss` → response: `brand=SSS`
- [ ] **T-BR-05** POST with no brand signals → response: `brand=SSS` (default)
- [ ] **T-BR-06** Audit Log entry created with `Action_Type=BRAND_CLASSIFICATION`
- [ ] **T-BR-07** Response includes `prompt_prefix`, `slack_channel`, `airtable_base` fields

**Pass criteria:** All 7 pass before activating

---

## M-LEAD-INTAKE TESTS

- [ ] **T-LI-01** Submit Webflow form (or POST directly) → Airtable Request record created
- [ ] **T-LI-02** Request record has `Agent_Status=AI_RESPONDING`
- [ ] **T-LI-03** Request record has correct `Brand` from M-BRAND-ROUTER classification
- [ ] **T-LI-04** Slack notification sent to #sss-ops-alerts with client name, email, brand
- [ ] **T-LI-05** Audit Log entry created with `Action_Type=REQUEST_CREATED`
- [ ] **T-LI-06** Submit same email within 24h → second Request record NOT created
- [ ] **T-LI-07** Submit same email after 24h → second Request record IS created
- [ ] **T-LI-08** Scenario responds 200 even when duplicate is suppressed
- [ ] **T-LI-09** Phone field empty → handled gracefully (not required)
- [ ] **T-LI-10** All Airtable required fields populated (Name, Email, Source, Brand, Environment, Created_At)

**Pass criteria:** All 10 pass before activating

---

## M-STRIPE-DEPOSIT TESTS

- [ ] **T-SD-01** Booking at Status=AVAILABILITY_CONFIRMED, Deposit_Link_Sent=false → Stripe Payment Link created
- [ ] **T-SD-02** Stripe API call uses `Stripe-Version: 2023-10-16` header (verify in Stripe logs)
- [ ] **T-SD-03** Stripe Payment Link has correct `metadata.booking_id`
- [ ] **T-SD-04** Stripe Payment Link has correct `metadata.airtable_record_id`
- [ ] **T-SD-05** Stripe Payment Link has `metadata.payment_type=deposit`
- [ ] **T-SD-06** Booking updated: Status=DEPOSIT_SENT, Stripe_Payment_Link_URL populated
- [ ] **T-SD-07** Deposit confirmation email sent to client email address
- [ ] **T-SD-08** Email contains payment link URL
- [ ] **T-SD-09** Email contains correct charter date, vessel, package, guest count
- [ ] **T-SD-10** Idempotency: trigger scenario again on same Booking → no duplicate Payment Link created (Deposit_Link_Sent=true filter blocks re-run)
- [ ] **T-SD-11** Audit Log entry created with `Action_Type=DEPOSIT_LINK_CREATED`
- [ ] **T-SD-12** Deposit amount = Package_Price × 0.5 (verify in Stripe link amount)

**Pass criteria:** All 12 pass before activating

---

## M-BOOKING-CREATION TESTS

- [ ] **T-BC-01** Send Stripe test webhook `checkout.session.completed` with all required metadata → Booking updated to DEPOSIT_PAID
- [ ] **T-BC-02** Booking has `Stripe_Deposit_Payment_Intent` field populated
- [ ] **T-BC-03** Booking has `Deposit_Paid_At` timestamp populated
- [ ] **T-BC-04** Slack notification in #sss-ops-alerts with booking ID and amount
- [ ] **T-BC-05** Audit Log entry created with `Action_Type=DEPOSIT_RECEIVED`
- [ ] **T-BC-06** Idempotency: send same Stripe event ID twice → Booking NOT updated twice (Audit Log search blocks second run)
- [ ] **T-BC-07** Event type ≠ `checkout.session.completed` → scenario skips (filter blocks)
- [ ] **T-BC-08** `metadata.payment_type ≠ deposit` → scenario skips (filter blocks)
- [ ] **T-BC-09** `metadata.environment ≠ Production` → scenario skips (filter blocks)
- [ ] **T-BC-10** Scenario returns 200 to Stripe within 30 seconds (Stripe requires <30s acknowledgment)

**Pass criteria:** All 10 pass before activating

---

## M-CONCIERGE-ASSIGNMENT TESTS

- [ ] **T-CA-01** Booking at Status=DEPOSIT_PAID, Concierge_Assigned=false → Booking updated with Concierge_Assigned=true
- [ ] **T-CA-02** Luciana receives Slack DM with complete booking details (client, date, vessel, package, guests, occasion, contact)
- [ ] **T-CA-03** DM includes deposit amount paid
- [ ] **T-CA-04** `Concierge_Assigned_At` timestamp populated on Booking
- [ ] **T-CA-05** Audit Log entry created with `Action_Type=CONCIERGE_ASSIGNED`
- [ ] **T-CA-06** Booking already has Concierge_Assigned=true → scenario does NOT trigger (filter blocks)
- [ ] **T-CA-07** HV_Client=true → Will also receives DM with HV alert language
- [ ] **T-CA-08** HV DM includes clear instruction: all communications require Will review

**Pass criteria:** All 8 pass before activating

---

## M-BOOKING-CONFIRMATION TESTS

- [ ] **T-CF-01** Booking at Status=CONFIRMED, Confirmation_Sent=false, HV_Client=false → confirmation email sent to client
- [ ] **T-CF-02** Email contains: charter date, vessel, package, guests, occasion, add-ons, boarding address
- [ ] **T-CF-03** Email contains: deposit paid amount, balance due amount, balance due date
- [ ] **T-CF-04** Email `From` address is hello@shesaidsail.com
- [ ] **T-CF-05** Booking updated: Confirmation_Sent=true, Confirmation_Sent_At populated
- [ ] **T-CF-06** Audit Log entry created with `Action_Type=CONFIRMATION_SENT`
- [ ] **T-CF-07** HV_Client=true → email NOT sent, Luciana DM sent instead
- [ ] **T-CF-08** Emergency_Flag=true → scenario skips entirely (no email, no Luciana DM)
- [ ] **T-CF-09** Automations_Paused=true → scenario skips entirely
- [ ] **T-CF-10** Confirmation_Sent=true already → scenario does NOT trigger again (filter blocks)
- [ ] **T-CF-11** Balance due date = Charter_Date minus 3 days (verify calculation in email)

**Pass criteria:** All 11 pass before activating

---

## END-TO-END FLOW TEST

After all 8 scenarios pass individual tests:

- [ ] **T-E2E-01** Submit inquiry form → Request created, Slack notified, Audit logged
- [ ] **T-E2E-02** Manually set Booking to AVAILABILITY_CONFIRMED → Payment Link created, email sent, Booking = DEPOSIT_SENT
- [ ] **T-E2E-03** Complete Stripe checkout (test mode) → Booking = DEPOSIT_PAID, Slack notified, Audit logged
- [ ] **T-E2E-04** Booking = DEPOSIT_PAID triggers concierge assignment → Luciana DM, Audit logged
- [ ] **T-E2E-05** Manually set Booking to CONFIRMED → Confirmation email sent, Audit logged
- [ ] **T-E2E-06** Check Airtable Audit Log — all 5 action types present for this booking
- [ ] **T-E2E-07** Check #sss-ops-alerts — all relevant notifications present
- [ ] **T-E2E-08** No duplicate records in Airtable
- [ ] **T-E2E-09** No duplicate emails sent

**Pass criteria:** All 9 pass before signing off Stage 1 as Production-ready

---

**Sign-off:**

| Person | Date | Status |
|--------|------|--------|
| Will Hunt | | ☐ APPROVED FOR PRODUCTION |
| Luciana | | ☐ WORKFLOWS CONFIRMED |

---

*She Said Sail · Stage 1 Testing Checklist*  
*CONFIDENTIAL — INTERNAL USE ONLY*
