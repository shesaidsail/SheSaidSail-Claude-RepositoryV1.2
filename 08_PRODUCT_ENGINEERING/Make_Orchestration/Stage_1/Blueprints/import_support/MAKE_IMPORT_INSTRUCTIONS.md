# MAKE IMPORT INSTRUCTIONS — Stage 1 Blueprint Package
**Version:** 1.0
**Date:** 2026-05-16
**Audience:** Will (Founder) or designated Systems Engineer

---

## Pre-Import Requirements

Before importing any blueprint, confirm all of the following:

- [ ] You have Make.com account access with permission to create scenarios
- [ ] You have a dedicated Make Team or Organization for SSS/ME
- [ ] Airtable Personal Access Token (PAT) is available and scoped to base `appdZ49WqgjRXxA1R`
- [ ] Slack OAuth app is connected to the SSS Slack workspace in Make
- [ ] Gmail OAuth connection is available for `hello@shesaidsail.com` and `hello@mareexecutive.com`
- [ ] Stripe connection is available in Make (live AND test mode keys ready)
- [ ] Quo SMS API key is available
- [ ] The following Slack channels exist: `#sss-leads`, `#me-leads`, `#sss-bookings`, `#sss-ops`, `#sss-ops-alerts`, `#sss-emergency-ops`
- [ ] Airtable tables `Automation_Health` and `Concierge_Operators` have been created in base `appdZ49WqgjRXxA1R` and their Table IDs recorded
- [ ] Will's Slack Member ID has been noted (find it in Slack → Profile → More → Copy Member ID)

---

## Step-by-Step Import Process

### STEP 1 — Create Make Team and Folder Structure

1. Log into Make.com
2. Create a new team (if not existing): **She Said Sail + Mare Executive**
3. Inside the team, create a scenario folder: **Stage 1 — Core Operations**
4. All 8 Stage 1 scenarios should be imported into this folder

---

### STEP 2 — Import M-AUDIT-LOGGER (MUST BE FIRST)

1. In Make, go to **Scenarios** → **Create a new scenario**
2. Click the **three-dot menu** → **Import Blueprint**
3. Upload file: `M-AUDIT-LOGGER.blueprint.json`
4. Make will show a "Reconnect modules" dialog — do this now:
   - Reconnect the **Airtable** module with your Airtable connection (Personal Access Token)
   - Reconnect the **Slack** module with your Slack connection
5. Update the Airtable module for Automation_Health: replace `AUTOMATION_HEALTH_TABLE_ID` with the actual Table ID from your Airtable base
6. Save the scenario (do NOT activate yet)
7. **CRITICAL:** Go to the webhook trigger module → Copy the generated webhook URL
8. Record this URL: `M-AUDIT-LOGGER Webhook URL = ___________________`
   - You will paste this URL into every other scenario's HTTP module that calls M-AUDIT-LOGGER

---

### STEP 3 — Import M-SLACK-ALERTS

1. Create a new scenario → Import Blueprint → Upload `M-SLACK-ALERTS.blueprint.json`
2. Reconnect the **Slack** module
3. Replace `WILL_SLACK_USER_ID_PLACEHOLDER` with Will's actual Slack Member ID
4. In the HTTP module(s) calling M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` with the M-AUDIT-LOGGER webhook URL from Step 2
5. Save (do NOT activate)
6. **CRITICAL:** Copy the generated webhook URL for M-SLACK-ALERTS
7. Record: `M-SLACK-ALERTS Webhook URL = ___________________`

---

### STEP 4 — Import M-BRAND-ROUTER

1. Create new scenario → Import Blueprint → Upload `M-BRAND-ROUTER.blueprint.json`
2. Reconnect Airtable and Slack modules
3. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`:
   - HTTP module calling M-AUDIT-LOGGER → paste M-AUDIT-LOGGER webhook URL
   - HTTP module calling M-LEAD-INTAKE → leave blank for now (import M-LEAD-INTAKE next)
4. Save (do NOT activate)
5. Record: `M-BRAND-ROUTER Webhook URL = ___________________`

---

### STEP 5 — Import M-LEAD-INTAKE

1. Create new scenario → Import Blueprint → Upload `M-LEAD-INTAKE.blueprint.json`
2. Reconnect Airtable module
3. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`:
   - HTTP module calling M-AUDIT-LOGGER → paste M-AUDIT-LOGGER URL
   - HTTP module calling M-SLACK-ALERTS → paste M-SLACK-ALERTS URL
4. Save (do NOT activate)
5. Record: `M-LEAD-INTAKE Webhook URL = ___________________`
6. **Go back to M-BRAND-ROUTER** → Update the HTTP module calling M-LEAD-INTAKE with this URL → Save

---

### STEP 6 — Import M-CONCIERGE-ASSIGNMENT

1. Create new scenario → Import Blueprint → Upload `M-CONCIERGE-ASSIGNMENT.blueprint.json`
2. Reconnect Airtable, Slack, Gmail modules
3. Replace `CONCIERGE_OPERATORS_TABLE_ID` with actual Table ID
4. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` with appropriate URLs
5. Save. Record: `M-CONCIERGE-ASSIGNMENT Webhook URL = ___________________`

---

### STEP 7 — Import M-STRIPE-DEPOSIT

1. Create new scenario → Import Blueprint → Upload `M-STRIPE-DEPOSIT.blueprint.json`
2. Reconnect Airtable, Stripe, Gmail, SMS modules
3. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
4. Save. Record: `M-STRIPE-DEPOSIT Webhook URL = ___________________`

---

### STEP 8 — Import M-BOOKING-CONFIRMATION

1. Create new scenario → Import Blueprint → Upload `M-BOOKING-CONFIRMATION.blueprint.json`
2. Reconnect Airtable, Gmail, SMS, Slack modules
3. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
4. Save. Record: `M-BOOKING-CONFIRMATION Webhook URL = ___________________`

---

### STEP 9 — Import M-BOOKING-CREATION (LAST — requires Stripe webhook)

1. Create new scenario → Import Blueprint → Upload `M-BOOKING-CREATION.blueprint.json`
2. Reconnect Airtable, Stripe, Slack modules
3. Replace all `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` including:
   - M-AUDIT-LOGGER URL
   - M-SLACK-ALERTS URL
   - M-BOOKING-CONFIRMATION URL (from Step 8)
4. Save. Record: `M-BOOKING-CREATION Webhook URL = ___________________`
5. **Register Stripe Webhook:**
   - Go to Stripe Dashboard → Developers → Webhooks → Add endpoint
   - URL: paste M-BOOKING-CREATION webhook URL from Make
   - Events to listen to: `payment_intent.succeeded`
   - Save and copy the Stripe Webhook Signing Secret
   - Add the Signing Secret to the Stripe connection in Make

---

### STEP 10 — Sandbox Validation

**Do NOT activate production until sandbox validation passes.**

Follow the SANDBOX_TEST_SEQUENCE.md for complete test steps.

---

### STEP 11 — Production Enable

Follow PRODUCTION_ENABLE_ORDER.md. Do NOT enable all 8 simultaneously.

---

## Webhook URL Tracking Sheet

Fill this in as you import each scenario:

| Scenario | Webhook URL | Captured On |
|----------|-------------|-------------|
| M-AUDIT-LOGGER | | |
| M-SLACK-ALERTS | | |
| M-BRAND-ROUTER | | |
| M-LEAD-INTAKE | | |
| M-CONCIERGE-ASSIGNMENT | | |
| M-STRIPE-DEPOSIT | | |
| M-BOOKING-CREATION | | |
| M-BOOKING-CONFIRMATION | | |

---

## Make Limitations to Be Aware Of

1. **Blueprints do NOT import connection credentials.** Every connected service (Airtable, Slack, Gmail, Stripe) must be manually reconnected after import. This is by design — Make does not allow credential export.

2. **Webhook URLs are always regenerated on import.** There is no way to preserve the exact same webhook URL. All inter-scenario HTTP module URLs must be updated after every import.

3. **Blueprint import may warn about unrecognized module versions.** Accept and continue — this happens when the blueprint was generated against a slightly different Make module version. Verify module configuration manually.

4. **Router filter conditions may need manual review.** Some filter operators are version-specific. Verify all router conditions match the spec after import.

5. **Error handler routing** in Make is configured via the scenario's error handling panel, not as a module in the flow. After import, verify error handlers are configured for each scenario.
