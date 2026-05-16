# Stage 1 Native-First Reimport Instructions
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION REFERENCE

---

## Purpose

Step-by-step instructions for importing all 8 Stage 1 blueprints into Make.com. These instructions assume a fresh import into a production Make organization. Follow exactly — do not activate scenarios until all steps are complete.

---

## Prerequisites

Before starting import:
- [ ] You have Make.com organization access for She Said Sail production
- [ ] You have all credential vault secrets available (Airtable, Slack, Anthropic, Gmail, Stripe, Quo)
- [ ] You have Squarespace site editor access for the intake form
- [ ] You have Stripe Dashboard access (Developers → Webhooks)
- [ ] You have the 8 blueprint JSON files from this repository folder
- [ ] Airtable base `appdZ49WqgjRXxA1R` is live and accessible
- [ ] Founder Decision logged for production activation

---

## Step 1 — Access Make.com Scenarios

1. Log into Make.com at `https://www.make.com`
2. Navigate to the She Said Sail production team/organization
3. Go to **Scenarios** in the left navigation
4. Create a new folder: `Stage 1 — Production` (to keep scenarios organized)

---

## Step 2 — Import Each Blueprint

For each blueprint file, repeat this process:

1. In Make Scenarios, click **Create a new scenario**
2. In the scenario editor, click the **three-dot menu** (top right) → **Import Blueprint**
3. Click **Browse** and select the `.blueprint.json` file from:
   `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/`
4. Click **Save** — the scenario will load with all modules, routers, and filters intact
5. **Do not activate yet** — leave scenario OFF (toggle at bottom left stays grey)
6. Rename the scenario in Make to match the blueprint name exactly

**Import order (critical — follow this sequence):**
1. `M-AUDIT-LOGGER.blueprint.json`
2. `M-SLACK-ALERTS.blueprint.json`
3. `M-BRAND-ROUTER.blueprint.json`
4. `M-LEAD-INTAKE.blueprint.json`
5. `M-STRIPE-DEPOSIT.blueprint.json`
6. `M-CONCIERGE-ASSIGNMENT.blueprint.json`
7. `M-BOOKING-CREATION.blueprint.json`
8. `M-BOOKING-CONFIRMATION.blueprint.json`

---

## Step 3 — After Each Import: Copy Webhook URL

For scenarios with a **CustomWebHook trigger module** (modules 1 in M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BRAND-ROUTER, M-LEAD-INTAKE, M-STRIPE-DEPOSIT):

1. Click module 1 (the webhook trigger)
2. Click **Copy address to clipboard**
3. Save the URL in a secure temporary document — you will need it in Step 5

**Webhook URLs to collect:**
| Scenario | URL variable name | Use |
|---|---|---|
| M-AUDIT-LOGGER | `AUDIT_LOGGER_URL` | Paste into all other scenarios |
| M-SLACK-ALERTS | `SLACK_ALERTS_URL` | Not used by other scenarios (called via M-SLACK-ALERTS only) |
| M-BRAND-ROUTER | `BRAND_ROUTER_URL` | Paste into M-LEAD-INTAKE module 6 |
| M-LEAD-INTAKE | `LEAD_INTAKE_URL` | Paste into Squarespace form |
| M-STRIPE-DEPOSIT | `STRIPE_DEPOSIT_URL` | Paste into Stripe Dashboard webhook |

---

## Step 4 — Bind All Connections

For each scenario, open every module that shows a connection error (red icon) and bind the appropriate connection.

See `STAGE_1_NATIVE_REBINDING_GUIDE.md` for full connection instructions.

**Quick reference:**
| Module Type | Connection Name | Placeholder Replaced |
|---|---|---|
| Airtable (all) | `SSS — Airtable Production` | `RECONNECT_AIRTABLE_CONNECTION` |
| Slack (all) | `SSS — Slack Production` | `RECONNECT_SLACK_CONNECTION` |
| Anthropic Claude | `SSS — Anthropic Claude Production` | `RECONNECT_CLAUDE_API_KEY` |
| Gmail (all) | `SSS — Gmail hello@shesaidsail.com` | `RECONNECT_GMAIL_CONNECTION` |
| Stripe | `SSS — Stripe Production` | `RECONNECT_STRIPE_CONNECTION` |

---

## Step 5 — Replace HTTP URL Placeholders

In each HTTP module that contains a placeholder URL, replace the placeholder with the real value collected in Step 3.

**M-AUDIT-LOGGER:** No HTTP modules to update.

**M-SLACK-ALERTS — Module 8:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-BRAND-ROUTER — Module 10:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-LEAD-INTAKE — Module 6:**
- URL field: replace `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` with `BRAND_ROUTER_URL`

**M-LEAD-INTAKE — Module 9:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-CONCIERGE-ASSIGNMENT — Module 9 (Quo SMS):**
- URL field: replace `RECONNECT_QUO_API_ENDPOINT` with Quo API endpoint from credential vault
- Authorization header value: replace `RECONNECT_QUO_API_KEY` with Quo API key

**M-CONCIERGE-ASSIGNMENT — Modules 10 and 11:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-STRIPE-DEPOSIT — Module 10:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-BOOKING-CREATION — Modules 11 and 12:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-BOOKING-CONFIRMATION — Module 9 (Quo SMS):**
- URL field: replace `RECONNECT_QUO_API_ENDPOINT` with Quo API endpoint
- Authorization header value: replace `RECONNECT_QUO_API_KEY` with Quo API key

**M-BOOKING-CONFIRMATION — Modules 11 and 12:**
- URL field: replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` with `AUDIT_LOGGER_URL`

**M-SLACK-ALERTS — Modules 5 and 7 (Will DM):**
- Channel field: replace `RECONNECT_WILL_SLACK_USER_ID` with Will's Slack User ID (format: `U0XXXXXXXXX`)

---

## Step 6 — Configure External Webhooks

**Squarespace form (M-LEAD-INTAKE):**
1. Copy `LEAD_INTAKE_URL` from Step 3
2. Log into Squarespace site editor
3. Open the lead intake form block → Edit → Storage → Add → Webhook
4. Paste `LEAD_INTAKE_URL`
5. Save

**Stripe webhook (M-STRIPE-DEPOSIT):**
1. Copy `STRIPE_DEPOSIT_URL` from Step 3
2. Log into Stripe Dashboard → Developers → Webhooks → Add endpoint
3. Paste `STRIPE_DEPOSIT_URL`
4. Event: `payment_intent.succeeded`
5. Save — copy the Signing Secret (`whsec_...`)
6. Store Signing Secret in Make Data Store (not in blueprint)
7. In Make, configure M-STRIPE-DEPOSIT webhook module to validate Stripe-Signature header

---

## Step 7 — Run Pre-Activation Tests

For each scenario, run one test execution with safe test data before activating.

**Test sequence:**

1. **M-AUDIT-LOGGER test:**
   - Send POST to `AUDIT_LOGGER_URL` with test JSON payload
   - Verify new record in Airtable Audit Log table `tblrMpTfMk8q1eNHp`

2. **M-SLACK-ALERTS test:**
   - Send POST with `{"alert_level":"L1","message_text":"Stage 1 import test","brand":"SSS","environment":"Production","idempotency_key":"TEST-SLACK-001"}`
   - Verify message appears in `#sss-ops-alerts`

3. **M-BRAND-ROUTER test:**
   - Create a test Airtable Request record manually
   - Send POST with the record ID and a clearly SSS-style inquiry
   - Verify Brand field updated to `SSS` in Airtable

4. **M-LEAD-INTAKE test:**
   - Submit a test form on the Squarespace site (or send webhook manually)
   - Verify Request record created, auto-reply received at test email, Slack notification posted

5. **M-STRIPE-DEPOSIT test:**
   - Send a test webhook payload (Stripe test mode) or use Stripe Dashboard → Webhooks → Send test event
   - Verify booking status updated in Airtable and confirmation email sent to test email

6. **M-CONCIERGE-ASSIGNMENT test:**
   - Update a test Booking record status to `AVAILABILITY_CONFIRMED`
   - Verify Stripe payment link created, deposit email sent to test email, Airtable updated to `DEPOSIT_SENT`
   - If Quo SMS not ready: disable Quo module temporarily for testing

7. **M-BOOKING-CREATION test:**
   - Set a test Booking to `CONFIRMED` + `Agreement_Signed = true` + `Charter_Date = today + 10 days`
   - Verify Charter Brief generated and emailed to City Manager test address

8. **M-BOOKING-CONFIRMATION test:**
   - Set a test Booking to `CONFIRMED` + `Charter_Date = today + 2 days` + `Balance_Reminder_Sent = false`
   - Verify Stripe balance link created, reminder email sent to test email

---

## Step 8 — Activate Scenarios

Only after all tests pass:

1. Open M-AUDIT-LOGGER → toggle scenario ON
2. Open M-SLACK-ALERTS → toggle ON
3. Open M-BRAND-ROUTER → toggle ON
4. Open M-LEAD-INTAKE → toggle ON
5. Open M-STRIPE-DEPOSIT → toggle ON
6. Open M-CONCIERGE-ASSIGNMENT → toggle ON
7. Open M-BOOKING-CREATION → toggle ON
8. Open M-BOOKING-CONFIRMATION → toggle ON

Log activation in Airtable Founder Decisions table with:
- Decision type: SYSTEM
- Description: Stage 1 Make blueprints activated — native-first build
- Approved by: Will
- Date: activation date

---

## Troubleshooting

| Issue | Resolution |
|---|---|
| Airtable module shows "Base not found" | Verify connection account has access to `appdZ49WqgjRXxA1R` |
| Slack module shows "Channel not found" | Verify connection account is a member of `#sss-ops-alerts` and `#sss-emergency-ops` |
| Anthropic module returns error | Check API key validity and rate limits; verify model name `claude-sonnet-4-20250514` |
| Gmail "From address not authorized" | Must authorize the specific Google account owning `hello@shesaidsail.com` |
| Stripe Payment Link creation fails | Check Restricted Key permissions include `payment_links:write` |
| Quo SMS 401 error | Verify API key is correct and not expired in credential vault |
| Stripe webhook not firing | Check Stripe Dashboard webhook status; verify event subscription is `payment_intent.succeeded` |
| Airtable trigger not firing | Verify formula filter is correct; check scenario scheduling (must be "instant" for webhooks, scheduled poll for Airtable watches) |
| Duplicate audit log entries | Check idempotency key logic — verify field names match Airtable schema |
