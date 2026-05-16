# POST-IMPORT QA CHECKLIST — Stage 1 Make Scenarios
**Version:** 1.0
**Date:** 2026-05-16
**Purpose:** Validate all 8 scenarios are correctly configured after import, before sandbox activation

---

## Pre-Activation QA — Run Before Turning Any Scenario On

### Global Checks (All Scenarios)

- [ ] All 8 scenarios appear in the Make scenario folder "Stage 1 — Core Operations"
- [ ] All 8 scenarios show zero disconnected modules (no red error indicators)
- [ ] All scenarios are set to **OFF** (inactive) — do not turn on until sandbox test passes
- [ ] All `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` strings have been replaced with real URLs
- [ ] All `AUTOMATION_HEALTH_TABLE_ID` and `CONCIERGE_OPERATORS_TABLE_ID` replaced with real Airtable table IDs
- [ ] `WILL_SLACK_USER_ID_PLACEHOLDER` replaced with Will's Slack Member ID
- [ ] All scenarios are connected to the **Sandbox** Airtable base (NOT production) for initial testing
- [ ] All scenarios are set to use **Stripe Test Mode** (NOT live mode)
- [ ] Scenario environment labels are set (Make scenario description should include "SANDBOX" or "PRODUCTION")

---

## Per-Scenario QA

### M-AUDIT-LOGGER QA

- [ ] Webhook trigger is active and URL is copied
- [ ] Module 2 (Airtable Search) targets correct table: `tblrMpTfMk8q1eNHp` (Audit Log) in sandbox base
- [ ] Module 3 (Airtable Create) targets correct table: `tblrMpTfMk8q1eNHp` with all required fields mapped
- [ ] Module 5 (Airtable Update) targets `Automation_Health` table with correct table ID
- [ ] Idempotency filter correctly checks `length(records) = 0` before writing
- [ ] Slack error module targets `#sss-ops-alerts`
- [ ] Test: POST M-AUDIT-LOGGER.test.json → confirm Audit Log record created in sandbox Airtable
- [ ] Test: POST duplicate idempotency_key → confirm NO second record created (idempotency working)

---

### M-BRAND-ROUTER QA

- [ ] Webhook trigger active
- [ ] Router Route 1 filter: `brand = "SSS"` — confirm correct
- [ ] Router Route 2 filter: `brand = "ME"` — confirm correct
- [ ] SetVariable in Route 1 sets: brand_name, brand_email, brand_slack_channel, airtable_base, package_table
- [ ] HTTP module in Route 1 points to M-LEAD-INTAKE (not placeholder)
- [ ] HTTP module in Route 2 points to M-LEAD-INTAKE (not placeholder)
- [ ] HTTP module for M-AUDIT-LOGGER points to real URL
- [ ] Test: POST M-BRAND-ROUTER.test.json with brand="SSS" → confirm routed to M-LEAD-INTAKE
- [ ] Test: POST with brand="ME" → confirm routed to M-LEAD-INTAKE with ME context

---

### M-LEAD-INTAKE QA

- [ ] Webhook trigger active
- [ ] Airtable Search targets Requests table `tblTlSB9CO4dTGodg` in sandbox base
- [ ] Router Route 1 "New Lead" filter: `length(records) = 0`
- [ ] Router Route 2 "Duplicate Lead" filter: `length(records) > 0`
- [ ] Airtable Create Record maps all required fields: First_Name, Last_Name, Email, Phone, City, Date_Requested, Party_Size, Budget_Range, Notes, Package_Interest, Brand, Source_System, Status, Environment, Agent_Status
- [ ] Status set to "NEW" on new records
- [ ] Agent_Status set to "HUMAN_REVIEW" on new records
- [ ] HTTP to M-AUDIT-LOGGER points to real URL
- [ ] HTTP to M-SLACK-ALERTS points to real URL
- [ ] Test: POST M-LEAD-INTAKE.test.json → confirm Request record created in sandbox Airtable
- [ ] Test: POST same email again → confirm duplicate detected, no second record created

---

### M-SLACK-ALERTS QA

- [ ] Webhook trigger active
- [ ] Router has 4 routes: Lead Alerts, Booking Alerts, Ops Alerts, Emergency
- [ ] Route 1 "Lead Alerts" filter: `alert_type = "NEW_LEAD"`
- [ ] Route 2 "Booking Alerts" filter: `alert_type = "BOOKING_CREATED"` (and others)
- [ ] Route 3 "Ops Alerts" filter: `alert_type = "CONCIERGE_ASSIGNED"` (and others)
- [ ] Route 4 "Emergency" filter: `alert_type = "EMERGENCY"`
- [ ] Emergency route sends to BOTH `#sss-emergency-ops` channel AND DM to Will
- [ ] Will's Slack Member ID is correctly set (not placeholder)
- [ ] Test: POST M-SLACK-ALERTS.test.json with alert_type="NEW_LEAD" → confirm Slack message in #sss-leads
- [ ] Test: POST with alert_type="EMERGENCY" → confirm message in #sss-emergency-ops AND DM to Will

---

### M-CONCIERGE-ASSIGNMENT QA

- [ ] Webhook trigger active
- [ ] Airtable Get Record targets Requests table `tblTlSB9CO4dTGodg`
- [ ] Airtable Search targets Concierge_Operators table (correct table ID)
- [ ] Search filter: City = city AND Brand = brand AND Status = "ACTIVE" AND Available = true
- [ ] Router Route 1 "Concierge Found": filter `length(records) > 0`
- [ ] Router Route 2 "No Concierge Available": filter `length(records) = 0`
- [ ] Gmail module configured with correct sender and "From" address
- [ ] Airtable Update sets Assigned_Concierge (linked record), Status="CONCIERGE_ASSIGNED"
- [ ] Test: POST M-CONCIERGE-ASSIGNMENT.test.json → confirm concierge assigned in sandbox Airtable
- [ ] Test: POST with city/brand with no active concierge → confirm "No Concierge Available" route fires, Slack alert sent

---

### M-STRIPE-DEPOSIT QA

- [ ] Webhook trigger active
- [ ] Airtable Get Record targets Bookings table `tbl72omPibBkn2hZL`
- [ ] Airtable Search targets Packages table `tblwDw2hkKW5moSr9`
- [ ] Stripe module uses **TEST mode** connection (not live)
- [ ] Stripe Payment Link metadata includes: booking_id, brand, environment, type="deposit"
- [ ] Airtable Update sets: Deposit_Link, Status="DEPOSIT_SENT", Deposit_Sent_At, Deposit_Amount
- [ ] Gmail uses correct sender address
- [ ] SMS HTTP module has correct endpoint URL (not placeholder)
- [ ] Test: POST M-STRIPE-DEPOSIT.test.json → confirm Stripe test payment link created
- [ ] Test: Confirm Airtable Booking record updated with deposit link in sandbox base
- [ ] Test: Confirm test email sent to test address (do NOT use real client email in sandbox)
- [ ] Test: Confirm SMS sent to test number (do NOT use real client phone in sandbox)

---

### M-BOOKING-CREATION QA

- [ ] Webhook trigger active
- [ ] Stripe webhook registered in Stripe Dashboard (Test Mode) pointing to this URL
- [ ] Stripe signing secret configured
- [ ] Sandbox guard route correctly filters `environment = "sandbox"` to prevent accidental production data processing
- [ ] Idempotency check: Airtable search for existing Stripe_Payment_Intent_ID before creating booking
- [ ] Airtable Create Record maps all Booking fields correctly
- [ ] Airtable Update sets Request.Status = "DEPOSIT_PAID" after booking created
- [ ] HTTP to M-BOOKING-CONFIRMATION points to real URL
- [ ] HTTP to M-AUDIT-LOGGER points to real URL
- [ ] HTTP to M-SLACK-ALERTS points to real URL
- [ ] Test: Use Stripe Dashboard Test Mode → "Send test event" → `payment_intent.succeeded` with test metadata
- [ ] Test: Confirm Booking record created in sandbox Airtable
- [ ] Test: Confirm M-BOOKING-CONFIRMATION triggered (check downstream scenario execution log)

---

### M-BOOKING-CONFIRMATION QA

- [ ] Webhook trigger active
- [ ] Airtable Get Record targets Bookings table `tbl72omPibBkn2hZL`
- [ ] Router Route 1 "SSS Confirmation" filter: `brand = "SSS"`
- [ ] Router Route 2 "ME Confirmation" filter: `brand = "ME"`
- [ ] Gmail SSS module uses hello@shesaidsail.com as sender
- [ ] Gmail ME module uses hello@mareexecutive.com as sender
- [ ] Airtable Update sets: Confirmation_Sent_At, and Status = "CONFIRMED" (if Agreement_Signed) or "AGREEMENT_PENDING"
- [ ] SMS modules have correct endpoint (not placeholder)
- [ ] Test: POST M-BOOKING-CONFIRMATION.test.json with brand="SSS" → confirm SSS confirmation email sent to test address
- [ ] Test: POST with brand="ME" → confirm ME confirmation email sent to test address
- [ ] Test: Confirm Airtable Booking Status updated in sandbox base

---

## Final Sign-Off

| Check | Status | Signed Off By |
|-------|--------|---------------|
| All 8 scenarios pass individual QA | [ ] | |
| Full end-to-end sandbox test complete | [ ] | |
| No production data was touched during sandbox testing | [ ] | |
| Will has reviewed and approved | [ ] | |
| Production enable order reviewed (PRODUCTION_ENABLE_ORDER.md) | [ ] | |
| Rollback procedure confirmed available | [ ] | |
