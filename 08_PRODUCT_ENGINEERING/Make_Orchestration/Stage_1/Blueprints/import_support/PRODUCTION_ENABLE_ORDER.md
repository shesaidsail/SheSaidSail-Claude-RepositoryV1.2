# PRODUCTION ENABLE ORDER — Stage 1 Make Scenarios
**Version:** 1.0
**Date:** 2026-05-16
**Purpose:** Controlled production activation sequence after sandbox validation is complete

---

## Authorization Requirements

Production activation requires ALL of the following:

- [ ] All 16 sandbox tests passed (see SANDBOX_TEST_SEQUENCE.md)
- [ ] Will has signed off on sandbox test results
- [ ] Production Airtable base `appdZ49WqgjRXxA1R` has all required tables created (including Automation_Health and Concierge_Operators)
- [ ] Stripe Live Mode credentials connected to production Make scenarios
- [ ] Gmail production OAuth connected (hello@shesaidsail.com, hello@mareexecutive.com)
- [ ] Rollback procedure reviewed and confirmed (see MAKE_ROLLBACK_PROTOCOLS.md if available)
- [ ] Production Stripe webhook registered (separate from sandbox webhook)
- [ ] Monitoring active (Make alert emails configured)

---

## Production Enable Sequence

**Enable ONE scenario at a time. Verify before enabling the next.**

### STEP 1 — Enable M-AUDIT-LOGGER (Production)

**Enable it first.** All other scenarios call it. If it is not live, audit events will fail silently.

1. Open the Production version of M-AUDIT-LOGGER in Make
2. Verify all connections point to production Airtable base `appdZ49WqgjRXxA1R`
3. Verify Audit Log table ID is `tblrMpTfMk8q1eNHp`
4. Toggle scenario ON
5. Send a test audit event to the production webhook URL
6. Confirm audit log record appears in production Airtable

**Wait 5 minutes. Confirm no errors in Make execution log before proceeding.**

---

### STEP 2 — Enable M-SLACK-ALERTS (Production)

1. Verify Slack connection uses production workspace
2. Verify Will's Slack Member ID is set
3. Toggle scenario ON
4. Send a test AUTOMATION_ERROR alert to verify Slack delivery
5. Confirm message appears in #sss-ops-alerts

**Wait 5 minutes. Confirm no errors.**

---

### STEP 3 — Enable M-LEAD-INTAKE (Production)

1. Verify Airtable connection points to `appdZ49WqgjRXxA1R` Requests table `tblTlSB9CO4dTGodg`
2. Verify HTTP module URLs point to production M-AUDIT-LOGGER and M-SLACK-ALERTS
3. Toggle scenario ON
4. Send a minimal test lead (use a clearly flagged test name like "PRODUCTION_TEST_DO_NOT_CONTACT")
5. Confirm Request record created in production Airtable with correct fields
6. Delete the test record from Airtable immediately after confirming

**Wait 5 minutes. Confirm no errors.**

---

### STEP 4 — Enable M-BRAND-ROUTER (Production)

1. Verify HTTP modules point to production M-LEAD-INTAKE and M-AUDIT-LOGGER URLs
2. Toggle scenario ON
3. Send a test brand router event
4. Confirm routing to M-LEAD-INTAKE worked
5. Delete test records from Airtable

**Wait 5 minutes.**

---

### STEP 5 — Enable M-CONCIERGE-ASSIGNMENT (Production)

**Prerequisite:** At least one Concierge_Operators record must exist in production Airtable with Status="ACTIVE" and Available=true for Miami + SSS.

1. Verify Airtable connection targets production base
2. Verify Concierge_Operators table ID is correct
3. Toggle scenario ON
4. Do NOT send a full test — the scenario will fire from the Airtable workflow when a Request status changes. Monitor only.

---

### STEP 6 — Enable M-STRIPE-DEPOSIT (Production)

**WARNING: This scenario creates real Stripe Payment Links when triggered. Only enable when ready to send to real clients.**

1. Verify Stripe connection is in LIVE mode (not test mode)
2. Verify Gmail connection uses production accounts
3. Verify all Airtable connections point to production base
4. Toggle scenario ON
5. Do NOT send a test trigger — monitor for real activations

---

### STEP 7 — Enable M-BOOKING-CONFIRMATION (Production)

**Enable before M-BOOKING-CREATION** so confirmation is ready when bookings start coming in.

1. Verify Gmail connections are correct for both SSS and ME brands
2. Verify SMS connection is live
3. Verify Airtable connection targets production base
4. Toggle scenario ON

---

### STEP 8 — Enable M-BOOKING-CREATION (Production — LAST)

**FINAL STEP. This connects to live Stripe webhooks and will trigger on real payments.**

1. Verify production Stripe webhook is registered (from WEBHOOK_REGISTRATION_CHECKLIST.md)
2. Verify Stripe signing secret is configured in production scenario
3. Verify HTTP module for M-BOOKING-CONFIRMATION points to production URL
4. Toggle scenario ON
5. Monitor Make execution log for the next 30 minutes

**Do NOT enable until all other 7 scenarios are confirmed live and error-free.**

---

## Post-Enable Monitoring

For the first 48 hours after full production activation:

- [ ] Check Make execution logs every 2 hours
- [ ] Confirm all scenarios show "Success" status on recent runs
- [ ] Monitor #sss-ops-alerts for any automation error alerts
- [ ] Confirm Audit Log is receiving entries from all scenarios
- [ ] Confirm Automation_Health is being updated correctly
- [ ] Report any anomalies to Will immediately

---

## Rollback Procedure

If any scenario fails in production:

1. **Immediately toggle the failing scenario OFF** in Make
2. Post to #sss-ops-alerts: "MAKE SCENARIO [NAME] DEACTIVATED — [reason]"
3. Assess whether other scenarios must also be deactivated (check dependency map)
4. Create an Audit Log entry in Airtable (manual): Event_Type="SCENARIO_ROLLBACK", Scenario_ID, Actor="Will", reason
5. Review Make execution log for the failure point
6. Fix the issue in the sandbox environment first
7. Re-test in sandbox
8. Re-enable production only after Will approval

**Rollback does NOT require deleting the scenario.** Simply toggle it OFF and fix.
