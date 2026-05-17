# ROLLBACK GUIDE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Rollback procedures for every scenario

---

## ROLLBACK PRINCIPLES

1. Rollback by DEACTIVATING — never delete scenarios during an incident
2. Rollback in reverse import order (7 → 1)
3. Log every rollback action in Airtable Audit Log manually
4. Create a Founder Decision record for all rollbacks
5. After rollback, investigate root cause before re-activating

---

## IMMEDIATE PAUSE PROCEDURE

If something is wrong and you need to stop ALL automation immediately:

=== EMERGENCY PROCEDURE ===

1. In Make: Go to each scenario → Toggle OFF (deactivate)
   Priority order: M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-LEAD-INTAKE, M-BRAND-ROUTER, M-OPS-LOGGER-ALERTER

2. In Airtable: Set `Automations_Paused = true` on ALL active booking records
   (This prevents any partially-completed scenarios from triggering outbound comms)

3. In Airtable: Set `Emergency_Flag = true` on affected booking records if needed

4. Post to Slack #sss-emergency-ops manually: document what happened and which scenarios were paused

5. Create Audit Log entry manually with approval_state=FOUNDER_REQUIRED

---

## SCENARIO-LEVEL ROLLBACK

### Roll Back: SSS-BOOKING-CONFIRMATION (Scenario 7)

**When to use:** Confirmation emails sent incorrectly or to wrong clients

1. Deactivate SSS-BOOKING-CONFIRMATION in Make (toggle OFF)
2. In Airtable Bookings: Find affected records → Set Confirmation_Sent=false if rollback requires resend
3. Set D0 Sent=false if needed
4. Contact clients if incorrect confirmation was sent
5. Investigate root cause
6. Fix and re-import if scenario was corrupted, or re-activate if it was a data issue

**Data impact:** Setting Confirmation_Sent=false will allow the scenario to re-fire on next trigger if re-activated.

---

### Roll Back: SSS-CONCIERGE-ASSIGNMENT (Scenario 6)

**When to use:** Wrong concierge assigned, or Concierge_Operators table was incorrect

1. Deactivate SSS-CONCIERGE-ASSIGNMENT in Make
2. In Airtable Bookings: Set Concierge_Assigned=false on affected records
3. Clear Concierge_Name field if incorrect
4. Fix Concierge_Operators table
5. Re-activate when corrected

**Data impact:** Setting Concierge_Assigned=false re-queues the booking for assignment on next trigger.

---

### Roll Back: SSS-BOOKING-CREATION (Scenario 5)

**When to use:** Bookings created incorrectly, Stripe payment links generated in error

1. Deactivate SSS-BOOKING-CREATION in Make
2. In Stripe Dashboard: Deactivate any incorrectly-generated payment links
3. In Airtable Bookings: Delete or archive incorrect booking records
4. In Airtable Requests: Revert Status from AVAILABILITY_CONFIRMED if needed
5. Fix the root cause (data or configuration)
6. Re-activate

**STRIPE NOTE:** Deactivate (not delete) payment links in Stripe Dashboard → Payment Links → find the link → toggle off.

---

### Roll Back: SSS-STRIPE-DEPOSIT (Scenario 4)

**When to use:** Deposits being incorrectly marked as paid, or wrong bookings being updated

1. Deactivate SSS-STRIPE-DEPOSIT in Make
2. In Airtable Bookings: Revert Status from DEPOSIT_PAID if needed (rare — do not do this if money actually moved)
3. In Stripe: Do NOT reverse payments unless instructed by Founder — contact Stripe support if needed
4. Fix root cause (usually a booking lookup formula issue)
5. Re-activate

---

### Roll Back: SSS-LEAD-INTAKE (Scenario 3)

**When to use:** Duplicate records being created, incorrect brand classification, emails not sending

1. Deactivate SSS-LEAD-INTAKE in Make
2. In Airtable Requests: Delete duplicate records created during the issue period
3. Fix root cause (usually a Webflow payload format change or Airtable field name change)
4. Re-activate after fix

---

### Roll Back: SSS-BRAND-ROUTER (Scenario 2)

**When to use:** All leads being classified as UNKNOWN, or wrong brand being assigned

1. Deactivate SSS-BRAND-ROUTER in Make (this also stops M-LEAD-INTAKE brand classification)
2. In Airtable: Manually set Brand field on affected records
3. Fix root cause (usually a source_url format change from Webflow)
4. Re-activate

---

### Roll Back: SSS-OPS-LOGGER-ALERTER (Scenario 1)

**WARNING:** Rolling back this scenario stops ALL logging and Slack alerts across all other scenarios. Only do this if the scenario itself is causing problems.

**When to use:** OPS-LOGGER-ALERTER is causing Airtable permission errors or Slack failures that cascade to block other scenarios

1. Before deactivating: Confirm no other scenario will fail because of missing logger calls (other scenarios handle logger failures silently via `handleErrors: false`)
2. Deactivate SSS-OPS-LOGGER-ALERTER in Make
3. All other scenarios will continue to run — they will not receive Slack alerts or write audit logs until the logger is restored
4. Fix root cause (usually a connection rebinding issue or Airtable table field change)
5. Re-activate and verify Audit Log records are being created

---

## FULL ROLLBACK SEQUENCE

If you need to deactivate everything (nuclear option):

1. Deactivate SSS-BOOKING-CONFIRMATION
2. Deactivate SSS-CONCIERGE-ASSIGNMENT
3. Deactivate SSS-BOOKING-CREATION
4. Deactivate SSS-STRIPE-DEPOSIT
5. Deactivate SSS-LEAD-INTAKE
6. Deactivate SSS-BRAND-ROUTER
7. Deactivate SSS-OPS-LOGGER-ALERTER
8. Set Automations_Paused=true on all active Booking records in Airtable
9. Document in Airtable Audit Log (manual entry)
10. Create Founder Decision record documenting the full rollback

---

## POST-ROLLBACK CHECKLIST

After any rollback:
- [ ] Root cause documented
- [ ] Affected records in Airtable corrected
- [ ] Any client-facing issues addressed (wrong emails, etc.)
- [ ] Founder Decision record created
- [ ] Audit Log entry created
- [ ] Fix deployed before re-activation
- [ ] Re-activation tested in sandbox first

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — ROLLBACK_GUIDE.md*
