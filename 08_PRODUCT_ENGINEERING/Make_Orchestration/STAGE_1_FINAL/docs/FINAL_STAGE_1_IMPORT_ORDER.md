# FINAL STAGE 1 IMPORT ORDER
## She Said Sail — Make Orchestration Stage 1

**Status:** PRODUCTION  
**Version:** 1.0  
**Owner:** Will Hunt  
**Date:** May 2026  
**Authority:** 08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/

---

## CRITICAL PRE-IMPORT RULES

1. **Import in exact order listed below.** Infrastructure scenarios must exist before operational scenarios call them.
2. **Complete credential binding before activating any scenario.** All `{{VARIABLE}}` tokens must be replaced.
3. **Validate each scenario in Sandbox before activating in Production.**
4. **Register all webhooks at their respective platforms after import, before activation.**
5. **Never activate M-LEAD-INTAKE, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, or M-BOOKING-CONFIRMATION until M-AUDIT-LOGGER and M-SLACK-ALERTS are live and tested.**

---

## IMPORT ORDER

### STEP 1 — M-AUDIT-LOGGER
**File:** `blueprints/M-AUDIT-LOGGER.json`  
**Scenario ID:** AUDIT-001  
**Type:** Infrastructure  
**Why first:** Every other Stage 1 scenario calls this endpoint to write audit records. It must exist and respond before any operational scenario is activated.  

After import:
- Copy the generated webhook URL
- Store as `AUDIT_LOGGER_WEBHOOK_URL` in Make credential vault
- Set `AUDIT_LOGGER_WEBHOOK_SECRET` (generate random 32-char string)
- Test with a POST to the webhook URL — verify Airtable record created in Audit Log table
- Activate in Production

---

### STEP 2 — M-SLACK-ALERTS
**File:** `blueprints/M-SLACK-ALERTS.json`  
**Scenario ID:** ALERTS-001  
**Type:** Infrastructure  
**Why second:** Operational scenarios use this for error routing and status notifications. Must be live before any scenario can send Slack alerts.  

After import:
- Copy the generated webhook URL
- Store as `SLACK_ALERTS_WEBHOOK_URL` in Make credential vault
- Set `SLACK_ALERTS_WEBHOOK_SECRET` (generate random 32-char string)
- Bind `SLACK_CONNECTION_ID` — Slack OAuth connection to SSS workspace
- Bind `SLACK_WILL_DM_ID` — Will's Slack member ID (format: U0XXXXXXXX)
- Test with a POST sending alert_level=SEV-1 — verify message in #sss-emergency-ops AND Will DM
- Test with alert_level=SEV-2 — verify message in #sss-ops-alerts only
- Activate in Production

---

### STEP 3 — M-BRAND-ROUTER
**File:** `blueprints/M-BRAND-ROUTER.json`  
**Scenario ID:** BRAND-ROUTER-001  
**Type:** Infrastructure  
**Why third:** M-LEAD-INTAKE calls this as its first action. Must exist before lead intake is activated.  

After import:
- Copy the generated webhook URL
- Store as `BRAND_ROUTER_WEBHOOK_URL` in Make credential vault
- Set `BRAND_ROUTER_WEBHOOK_SECRET` (generate random 32-char string)
- Bind `AIRTABLE_BASE_ID_PRODUCTION` = `appdZ49WqgjRXxA1R`
- Bind `AIRTABLE_BASE_ID_ME` (Mare Executive base ID — confirm from Airtable)
- Test with source=shesaidsail.com — verify returns brand=SSS
- Test with form_brand=mare — verify returns brand=ME
- Activate in Production

---

### STEP 4 — M-LEAD-INTAKE
**File:** `blueprints/M-LEAD-INTAKE.json`  
**Scenario ID:** INBOUND-001  
**Type:** Operational  
**Depends on:** M-BRAND-ROUTER, M-AUDIT-LOGGER, M-SLACK-ALERTS  

After import:
- Copy the generated webhook URL
- Store as `LEAD_INTAKE_WEBHOOK_URL`
- Set `LEAD_INTAKE_WEBHOOK_SECRET`
- Register webhook in Webflow: Site Settings > Integrations > Webhooks > form_submission
- Test with a sandbox form submission — verify Airtable Request record created with Agent_Status=AI_RESPONDING
- Verify Slack notification in #sss-ops-alerts
- Verify Audit Log entry written
- Verify duplicate suppression (submit same email twice within 24h — second should not create new record)
- Activate in Production

---

### STEP 5 — M-STRIPE-DEPOSIT
**File:** `blueprints/M-STRIPE-DEPOSIT.json`  
**Scenario ID:** BOOKING-001  
**Type:** Operational (Stripe API)  
**Depends on:** M-AUDIT-LOGGER  

After import:
- Bind `STRIPE_SECRET_KEY` — Stripe secret key from Dashboard (use restricted key with payment_links:write permission)
- Bind `GMAIL_CONNECTION_ID` — Gmail OAuth connection for hello@shesaidsail.com
- Test in Sandbox mode: create a test Booking record with Status=AVAILABILITY_CONFIRMED, Deposit_Link_Sent=false
- Verify Stripe Payment Link created (check Stripe test dashboard)
- Verify Booking record updated to Status=DEPOSIT_SENT, Stripe_Payment_Link_URL populated
- Verify email sent to client email address
- Verify Audit Log entry written
- **IMPORTANT:** Stripe API version is `2023-10-16` — set via `Stripe-Version` header in HTTP module. Do NOT use the deprecated `stripe:ActionCreatePaymentLink` connector.
- Activate in Production

---

### STEP 6 — M-BOOKING-CREATION
**File:** `blueprints/M-BOOKING-CREATION.json`  
**Scenario ID:** BOOKING-002  
**Type:** Operational (Stripe Webhook)  
**Depends on:** M-STRIPE-DEPOSIT, M-AUDIT-LOGGER, M-SLACK-ALERTS  

After import:
- Copy the generated webhook URL
- Register in Stripe Dashboard: Developers > Webhooks > Add endpoint
  - Event: `checkout.session.completed`
  - Target URL: this scenario's Make webhook URL
  - Copy the Stripe webhook signing secret
  - Store as `STRIPE_WEBHOOK_SIGNING_SECRET` in Make credential vault
  - Store as `STRIPE_DEPOSIT_WEBHOOK_SECRET` (Make-side validation token)
- Test with Stripe test webhook (Stripe CLI or Dashboard Test mode)
- Verify Booking updated to DEPOSIT_PAID
- Verify Slack notification in #sss-ops-alerts
- Verify Audit Log entry written
- Verify idempotency: send same event twice — second should not update
- Activate in Production

---

### STEP 7 — M-CONCIERGE-ASSIGNMENT
**File:** `blueprints/M-CONCIERGE-ASSIGNMENT.json`  
**Scenario ID:** BOOKING-003  
**Type:** Operational  
**Depends on:** M-BOOKING-CREATION, M-AUDIT-LOGGER, M-SLACK-ALERTS  

After import:
- Bind `LUCIANA_AIRTABLE_RECORD_ID` — Luciana's record ID from Concierge_Operators or Team_Members table
- Bind `SLACK_LUCIANA_ID` — Luciana's Slack member ID (format: U0XXXXXXXX)
- Bind `SLACK_WILL_DM_ID` — Will's Slack member ID
- Test with a Booking record at Status=DEPOSIT_PAID, Concierge_Assigned=false
- Verify Booking updated with Concierge_Assigned=true
- Verify Luciana receives Slack DM
- Test HV_Client=true — verify Will also receives DM
- Verify Audit Log entry written
- Activate in Production

---

### STEP 8 — M-BOOKING-CONFIRMATION
**File:** `blueprints/M-BOOKING-CONFIRMATION.json`  
**Scenario ID:** BOOKING-004  
**Type:** Operational  
**Depends on:** M-CONCIERGE-ASSIGNMENT, M-AUDIT-LOGGER  

After import:
- Bind `GMAIL_CONNECTION_ID` (same OAuth connection as Step 5)
- Test with a Booking at Status=CONFIRMED, Confirmation_Sent=false, HV_Client=false
- Verify client confirmation email sent
- Verify Booking record updated: Confirmation_Sent=true
- Verify Audit Log entry written
- Test with HV_Client=true — verify email SUPPRESSED, Luciana DM sent
- Test with Emergency_Flag=true — verify scenario skips entirely
- Activate in Production

---

## POST-ACTIVATION VALIDATION SEQUENCE

After all 8 scenarios are active in Production:

1. Submit a test lead through Webflow form
2. Verify Request record created in Airtable with Agent_Status=AI_RESPONDING
3. Verify Slack notification in #sss-ops-alerts
4. Manually set a test Booking to Status=AVAILABILITY_CONFIRMED
5. Verify Stripe Payment Link created (check Stripe dashboard)
6. Verify Booking updated to DEPOSIT_SENT
7. Verify deposit confirmation email received
8. Simulate Stripe deposit webhook (use Stripe test mode)
9. Verify Booking updated to DEPOSIT_PAID
10. Verify Concierge Assignment (Luciana DM)
11. Manually set Booking to Status=CONFIRMED
12. Verify confirmation email sent
13. Verify all Audit Log records written correctly
14. Check #sss-ops-alerts for all expected notifications
15. Review Airtable Audit Log table — confirm every action is logged

---

## ROLLBACK ORDER

If any scenario causes issues, deactivate in reverse order:

1. Deactivate M-BOOKING-CONFIRMATION
2. Deactivate M-CONCIERGE-ASSIGNMENT
3. Deactivate M-BOOKING-CREATION
4. Deactivate M-STRIPE-DEPOSIT
5. Deactivate M-LEAD-INTAKE
6. Deactivate M-BRAND-ROUTER
7. Deactivate M-SLACK-ALERTS
8. Deactivate M-AUDIT-LOGGER (only if full teardown required)

Infrastructure scenarios (1-3) should remain active unless they are the specific source of failure.

---

*She Said Sail · Stage 1 Make Orchestration · Authoritative Import Guide*  
*CONFIDENTIAL — INTERNAL USE ONLY*
