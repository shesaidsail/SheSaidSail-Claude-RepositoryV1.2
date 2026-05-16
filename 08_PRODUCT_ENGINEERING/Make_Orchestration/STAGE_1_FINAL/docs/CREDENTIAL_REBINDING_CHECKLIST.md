# CREDENTIAL REBINDING CHECKLIST
## She Said Sail — Stage 1 Make Orchestration

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  
**Use:** Complete this checklist after importing each blueprint, before activating any scenario.

---

## HOW TO BIND CREDENTIALS IN MAKE

1. After importing a blueprint, Make will prompt you to reconnect or create connections for each native module.
2. For `{{VARIABLE}}` tokens in HTTP module headers and mappers, replace them manually in the module's "Headers" and "Body" fields.
3. Store all secrets in Make's **Connections** section or in a secure external vault. Never hardcode secrets in scenario names or notes.

---

## MASTER CREDENTIAL LIST

### Infrastructure Credentials (Bind First)

| Variable | Description | How to Get | Used By |
|----------|-------------|-----------|---------|
| `AIRTABLE_BASE_ID_PRODUCTION` | SSS Ops Airtable base ID | `appdZ49WqgjRXxA1R` — already known | All scenarios |
| `AIRTABLE_PAT` | Airtable Personal Access Token | Airtable > Account > Developer Hub > Personal Access Tokens > Create token (scopes: data.records:read, data.records:write) | All scenarios |
| `AUDIT_LOGGER_WEBHOOK_URL` | Make webhook URL for M-AUDIT-LOGGER | Generated when M-AUDIT-LOGGER is imported — copy from module 1 | M-LEAD-INTAKE, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `AUDIT_LOGGER_WEBHOOK_SECRET` | Bearer token for M-AUDIT-LOGGER auth | Generate: `openssl rand -hex 32` or any 32-char random string | M-AUDIT-LOGGER (set in webhook module), all callers |
| `SLACK_ALERTS_WEBHOOK_URL` | Make webhook URL for M-SLACK-ALERTS | Generated when M-SLACK-ALERTS is imported — copy from module 1 | M-LEAD-INTAKE, M-BOOKING-CREATION |
| `SLACK_ALERTS_WEBHOOK_SECRET` | Bearer token for M-SLACK-ALERTS auth | Generate: `openssl rand -hex 32` | M-SLACK-ALERTS (set in webhook module), all callers |
| `BRAND_ROUTER_WEBHOOK_URL` | Make webhook URL for M-BRAND-ROUTER | Generated when M-BRAND-ROUTER is imported — copy from module 1 | M-LEAD-INTAKE |
| `BRAND_ROUTER_WEBHOOK_SECRET` | Bearer token for M-BRAND-ROUTER auth | Generate: `openssl rand -hex 32` | M-BRAND-ROUTER (set in webhook module), M-LEAD-INTAKE |

### Platform Connections

| Variable | Description | How to Get | Used By |
|----------|-------------|-----------|---------|
| `SLACK_CONNECTION_ID` | Make Slack OAuth connection | Make > Connections > Add > Slack > Authorize SSS workspace | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `GMAIL_CONNECTION_ID` | Make Gmail OAuth connection | Make > Connections > Add > Gmail > Authorize hello@shesaidsail.com | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| `STRIPE_SECRET_KEY` | Stripe API key for Payment Links | Stripe Dashboard > Developers > API Keys > Create restricted key > permission: payment_links:write | M-STRIPE-DEPOSIT |
| `STRIPE_WEBHOOK_SIGNING_SECRET` | Stripe webhook signing secret | Stripe Dashboard > Developers > Webhooks > (after registration) > Signing secret | M-BOOKING-CREATION |
| `AIRTABLE_BASE_ID_ME` | Mare Executive Airtable base ID | Open Mare Executive base in Airtable > copy from URL (`app...`) | M-BRAND-ROUTER |

### Slack Person IDs

| Variable | Description | How to Get | Used By |
|----------|-------------|-----------|---------|
| `SLACK_WILL_DM_ID` | Will's Slack member ID | Slack > Will's profile > More (...) > Copy member ID (format: U0XXXXXXXXX) | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT |
| `SLACK_LUCIANA_ID` | Luciana's Slack member ID | Slack > Luciana's profile > More (...) > Copy member ID (format: U0XXXXXXXXX) | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |

### Airtable Record IDs

| Variable | Description | How to Get | Used By |
|----------|-------------|-----------|---------|
| `LUCIANA_AIRTABLE_RECORD_ID` | Luciana's record ID in Airtable | Open Concierge_Operators or Team_Members table > Luciana's row > URL shows record ID (format: recXXXXXXXXXXXXXX) | M-CONCIERGE-ASSIGNMENT |

### Webhook Instance IDs (Internal Make)

These are automatically assigned by Make when you import each blueprint. Copy them from the webhook module in each scenario.

| Variable | Scenario | Copy From |
|----------|---------|-----------|
| `AUDIT_LOGGER_WEBHOOK_ID` | M-AUDIT-LOGGER | Module 1 webhook configuration |
| `SLACK_ALERTS_WEBHOOK_ID` | M-SLACK-ALERTS | Module 1 webhook configuration |
| `BRAND_ROUTER_WEBHOOK_ID` | M-BRAND-ROUTER | Module 1 webhook configuration |
| `LEAD_INTAKE_WEBHOOK_ID` | M-LEAD-INTAKE | Module 1 webhook configuration |
| `STRIPE_DEPOSIT_WEBHOOK_ID` | M-BOOKING-CREATION | Module 1 webhook configuration |

---

## BINDING CHECKLIST BY SCENARIO

### ☐ M-AUDIT-LOGGER
- [ ] Airtable connection bound (PAT)
- [ ] `AIRTABLE_BASE_ID_PRODUCTION` = `appdZ49WqgjRXxA1R`
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` — set in webhook module, copy URL and secret to vault
- [ ] Test: POST to webhook URL → verify Airtable Audit Log record created
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-SLACK-ALERTS
- [ ] Slack OAuth connection bound
- [ ] `SLACK_WILL_DM_ID` — Will's Slack member ID bound
- [ ] `SLACK_ALERTS_WEBHOOK_SECRET` — set in webhook module, copy URL and secret to vault
- [ ] Test SEV-1: verify #sss-emergency-ops AND Will DM
- [ ] Test SEV-2: verify #sss-ops-alerts only
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-BRAND-ROUTER
- [ ] Airtable connection bound
- [ ] `AIRTABLE_BASE_ID_PRODUCTION` = `appdZ49WqgjRXxA1R`
- [ ] `AIRTABLE_BASE_ID_ME` — confirmed and bound
- [ ] `BRAND_ROUTER_WEBHOOK_SECRET` — set in webhook module, copy URL and secret to vault
- [ ] Test SSS routing: source=shesaidsail.com → brand=SSS
- [ ] Test ME routing: form_brand=mare → brand=ME
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-LEAD-INTAKE
- [ ] Airtable connection bound
- [ ] `BRAND_ROUTER_WEBHOOK_URL` bound (from M-BRAND-ROUTER)
- [ ] `BRAND_ROUTER_WEBHOOK_SECRET` bound
- [ ] `SLACK_ALERTS_WEBHOOK_URL` bound (from M-SLACK-ALERTS)
- [ ] `SLACK_ALERTS_WEBHOOK_SECRET` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_URL` bound (from M-AUDIT-LOGGER)
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` bound
- [ ] `LEAD_INTAKE_WEBHOOK_SECRET` — set in webhook module
- [ ] Webflow webhook registered (see WEBHOOK_REGISTRATION_INSTRUCTIONS.md)
- [ ] Test: submit Webflow form → Request record created in Airtable
- [ ] Test deduplication: submit same email twice → second suppressed
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-STRIPE-DEPOSIT
- [ ] Airtable connection bound
- [ ] `STRIPE_SECRET_KEY` — Stripe restricted key with payment_links:write
- [ ] `GMAIL_CONNECTION_ID` — Gmail OAuth for hello@shesaidsail.com
- [ ] `AUDIT_LOGGER_WEBHOOK_URL` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` bound
- [ ] Test: create test Booking with Status=AVAILABILITY_CONFIRMED → Stripe Payment Link created
- [ ] Verify: Booking updated to DEPOSIT_SENT, Stripe_Payment_Link_URL populated
- [ ] Verify: deposit email sent
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-BOOKING-CREATION
- [ ] Airtable connection bound
- [ ] `STRIPE_DEPOSIT_WEBHOOK_SECRET` — set in webhook module
- [ ] `STRIPE_WEBHOOK_SIGNING_SECRET` — from Stripe Dashboard after webhook registration
- [ ] `SLACK_ALERTS_WEBHOOK_URL` bound
- [ ] `SLACK_ALERTS_WEBHOOK_SECRET` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_URL` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` bound
- [ ] Stripe webhook endpoint registered (see WEBHOOK_REGISTRATION_INSTRUCTIONS.md)
- [ ] Test: send Stripe test webhook → Booking updated to DEPOSIT_PAID
- [ ] Test idempotency: send same event ID twice → second ignored
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-CONCIERGE-ASSIGNMENT
- [ ] Airtable connection bound
- [ ] Slack OAuth connection bound
- [ ] `LUCIANA_AIRTABLE_RECORD_ID` bound
- [ ] `SLACK_LUCIANA_ID` bound
- [ ] `SLACK_WILL_DM_ID` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_URL` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` bound
- [ ] Verify: Bookings table has `Concierge_Assigned` checkbox field
- [ ] Verify: Bookings table has `Assigned_Concierge` linked record field
- [ ] Test: set Booking to DEPOSIT_PAID → Luciana receives Slack DM
- [ ] Test HV: set HV_Client=true → Will also receives DM
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

### ☐ M-BOOKING-CONFIRMATION
- [ ] Airtable connection bound
- [ ] Gmail OAuth connection bound (same as M-STRIPE-DEPOSIT)
- [ ] Slack OAuth connection bound
- [ ] `SLACK_LUCIANA_ID` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_URL` bound
- [ ] `AUDIT_LOGGER_WEBHOOK_SECRET` bound
- [ ] Verify: Bookings table has `Confirmation_Sent` checkbox field
- [ ] Test: set Booking to CONFIRMED, HV_Client=false → confirmation email sent
- [ ] Test HV: set HV_Client=true → email suppressed, Luciana DM sent
- [ ] Test emergency guard: set Emergency_Flag=true → scenario skips
- [ ] Status: ☐ SANDBOX VALIDATED ☐ PRODUCTION ACTIVE

---

## CREDENTIAL STORAGE RULES

Per governance (Financial_OS_v1.0 and Founder_Control_Framework_v2.0):

- All API keys and secrets stored in Make credential vault only
- Never commit secrets to GitHub
- Never paste secrets in Slack messages
- Rotate Stripe keys every 90 days
- Rotate Airtable PAT if any team member offboards
- STRIPE_SECRET_KEY must be a restricted key — never the full Stripe secret

---

*She Said Sail · Stage 1 Credential Rebinding Checklist*  
*CONFIDENTIAL — INTERNAL USE ONLY*
