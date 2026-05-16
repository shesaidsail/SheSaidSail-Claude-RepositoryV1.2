# Stage 1 Make Blueprint Reimport Instructions
**Date:** 2026-05-16
**Status:** All 8 blueprints patched and validated — ready for import

---

## Should You Reimport All 8 Files or Only the Patched 7?

**Reimport all 8 files.**

M-BRAND-ROUTER was previously fixed and is the reference standard. All 7 remaining files have now been patched to match. Importing all 8 together ensures a clean, consistent scenario set in Make with no version drift. If M-BRAND-ROUTER is already live in Make, you may skip reimporting it — but reimporting does not harm it; Make will create a new scenario alongside the existing one, and you can delete the old version.

---

## Import Order

Import in this exact order. Each scenario depends on the one(s) above it for its webhook URLs.

| Order | Scenario | File | Why This Order |
|---|---|---|---|
| 1 | M-AUDIT-LOGGER | `M-AUDIT-LOGGER.blueprint.json` | Receives audit events from all other scenarios; must be live first |
| 2 | M-SLACK-ALERTS | `M-SLACK-ALERTS.blueprint.json` | Receives alert payloads from all other scenarios; must be live before they call it |
| 3 | M-BRAND-ROUTER | `M-BRAND-ROUTER.blueprint.json` | Entry point for all lead traffic; references M-AUDIT-LOGGER and M-SLACK-ALERTS |
| 4 | M-LEAD-INTAKE | `M-LEAD-INTAKE.blueprint.json` | Lead record creation; calls M-AUDIT-LOGGER and M-SLACK-ALERTS |
| 5 | M-CONCIERGE-ASSIGNMENT | `M-CONCIERGE-ASSIGNMENT.blueprint.json` | Assigns concierge after availability confirmation; calls M-SLACK-ALERTS, M-AUDIT-LOGGER |
| 6 | M-BOOKING-CONFIRMATION | `M-BOOKING-CONFIRMATION.blueprint.json` | Import before M-STRIPE-DEPOSIT so its webhook URL is ready to paste into M-BOOKING-CREATION |
| 7 | M-STRIPE-DEPOSIT | `M-STRIPE-DEPOSIT.blueprint.json` | Creates Stripe payment link; sends deposit email and SMS |
| 8 | M-BOOKING-CREATION | `M-BOOKING-CREATION.blueprint.json` | Receives Stripe webhook; triggers M-BOOKING-CONFIRMATION last in chain |

---

## Step-by-Step Import Process

### Step 1: Import Each Blueprint

For each file:
1. In Make, click **Create a new scenario**
2. Click the three-dot menu → **Import Blueprint**
3. Upload the `.json` file from `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/`
4. Make will create the scenario in an **inactive** state — do not activate yet

Repeat for all 8 files in the order listed above.

---

### Step 2: Record Webhook URLs

After importing each scenario, Make generates a unique webhook URL. You must record these before activating anything.

For each scenario that has a `gateway:CustomWebHook` trigger (all 8):
1. Click the webhook trigger module (module 1)
2. Click **Copy address to clipboard**
3. Paste into the table below and into your ops docs

| Scenario | Webhook URL (fill in after import) |
|---|---|
| M-AUDIT-LOGGER | _________________________________ |
| M-SLACK-ALERTS | _________________________________ |
| M-BRAND-ROUTER | _________________________________ |
| M-LEAD-INTAKE | _________________________________ |
| M-CONCIERGE-ASSIGNMENT | _________________________________ |
| M-BOOKING-CONFIRMATION | _________________________________ |
| M-STRIPE-DEPOSIT | _________________________________ |
| M-BOOKING-CREATION | _________________________________ |

---

### Step 3: Rebind Credentials in Every Scenario

After importing each scenario, open it and rebind every placeholder connection. Make will show a red warning on any module that has an unresolved connection.

#### Airtable (all scenarios except M-BRAND-ROUTER which uses HTTP)
- Open each Airtable module (SearchRecords, CreateRecord, UpdateRecord, GetRecord)
- Click the module → **Connection** → select or create your Airtable connection
- Required in: M-AUDIT-LOGGER, M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION

#### Slack (all scenarios)
- Open each `slack:postMessage` module
- Click **Connection** → select your She Said Sail Slack workspace connection
- Required in: all 8 scenarios

#### Gmail
- Open each `gmail:ActionSendEmail` module
- Click **Connection** → select the appropriate Gmail connection
  - SSS email modules: connect `hello@shesaidsail.com`
  - ME email modules: connect `hello@mareexecutive.com` (or your ops sending address)
- Required in: M-CONCIERGE-ASSIGNMENT (module 7), M-STRIPE-DEPOSIT (module 6), M-BOOKING-CONFIRMATION (modules 4, 6)

#### Stripe (M-STRIPE-DEPOSIT only)
- Module 4 uses `http:ActionSendData` with `Authorization: Bearer RECONNECT_STRIPE_CONNECTION`
- After import, edit module 4 → find the Authorization header value → replace `RECONNECT_STRIPE_CONNECTION` with your Stripe secret key
- **Use `sk_test_...` first.** Only switch to `sk_live_...` after testing the full flow end-to-end

#### SMS / Quo SMS API (M-STRIPE-DEPOSIT module 7, M-BOOKING-CONFIRMATION modules 5 and 7)
- Each SMS module has an `Authorization: Bearer RECONNECT_SMS_CONNECTION` header
- Replace `RECONNECT_SMS_CONNECTION` with your Quo SMS bearer token
- Confirm the API endpoint `https://api.quosms.com/v1/messages` is correct for your Quo SMS plan
- Also confirm the `"from"` sender ID values (`"SheSaidSail"` and `"MareExecutive"`) are registered with Quo SMS

#### Anthropic / Claude API (M-BRAND-ROUTER only)
- Modules 5 and 8 in M-BRAND-ROUTER use `http:ActionSendData` for Claude API
- Find the `x-api-key` header value → replace `RECONNECT_ANTHROPIC_API_KEY` with your Anthropic API key
- Also replace `RECONNECT_SSS_SYSTEM_PROMPT` and `RECONNECT_ME_SYSTEM_PROMPT` with the approved system prompt content for each brand

---

### Step 4: Replace INSERT_WEBHOOK_URL_AFTER_IMPORT Placeholders

After recording all webhook URLs in Step 2, go back into each scenario and update the HTTP modules that call other scenarios.

#### M-BRAND-ROUTER
- No cross-scenario webhook calls in current blueprint (routes internally via BasicRouter)

#### M-LEAD-INTAKE
- Modules 5, 8 → replace with M-AUDIT-LOGGER webhook URL
- Modules 6, 9 → replace with M-SLACK-ALERTS webhook URL

#### M-SLACK-ALERTS
- Module 9 → replace with M-AUDIT-LOGGER webhook URL

#### M-CONCIERGE-ASSIGNMENT
- Module 6 → replace with M-SLACK-ALERTS webhook URL
- Module 9 → replace with M-SLACK-ALERTS webhook URL
- Module 10 → replace with M-AUDIT-LOGGER webhook URL
- Module 11 → replace with M-AUDIT-LOGGER webhook URL

#### M-STRIPE-DEPOSIT
- Module 8 → replace with M-AUDIT-LOGGER webhook URL
- Module 9 → replace with M-SLACK-ALERTS webhook URL
- Module 10 → replace with M-AUDIT-LOGGER webhook URL (error handler)

#### M-BOOKING-CREATION
- Module 3 → replace with M-AUDIT-LOGGER webhook URL
- Module 6 → replace with M-AUDIT-LOGGER webhook URL
- Module 13 → replace with M-BOOKING-CONFIRMATION webhook URL
- Module 14 → replace with M-AUDIT-LOGGER webhook URL
- Module 15 → replace with M-SLACK-ALERTS webhook URL
- Module 16 → replace with M-AUDIT-LOGGER webhook URL (error handler)

#### M-BOOKING-CONFIRMATION
- Module 9 → replace with M-SLACK-ALERTS webhook URL
- Module 10 → replace with M-AUDIT-LOGGER webhook URL
- Module 11 → replace with M-AUDIT-LOGGER webhook URL (error handler)

---

### Step 5: Fix Table ID Placeholders

Two scenarios have Airtable table ID placeholders that must be resolved manually.

#### M-AUDIT-LOGGER — AUTOMATION_HEALTH_TABLE_ID (modules 5 and 6)
1. Open Airtable → She Said Sail Primary Base (`appdZ49WqgjRXxA1R`)
2. Find the **Automation_Health** table
3. Go to Help → API Documentation → find the table ID (format: `tblXXXXXXXXXXX`)
4. In Make, edit modules 5 and 6 → update the table selection to Automation_Health
5. If this table does not exist yet, create it in Airtable first with at minimum: `Scenario_ID` (text), `Last_Run_At` (date/time), `Last_Run_Status` (text), `Error_Count` (number)

#### M-CONCIERGE-ASSIGNMENT — CONCIERGE_OPERATORS_TABLE_ID (module 3)
1. Open Airtable → She Said Sail Primary Base
2. Find the **Concierge_Operators** table
3. In Make, edit module 3 → update the table selection to Concierge_Operators
4. If this table does not exist yet, create it with: `Name`, `Email`, `Phone`, `City`, `Brand`, `Status`, `Available`

---

### Step 6: Configure Stripe Webhook in Stripe Dashboard (M-BOOKING-CREATION)

M-BOOKING-CREATION uses a `gateway:CustomWebHook` to receive Stripe `payment_intent.succeeded` events.

1. Copy the M-BOOKING-CREATION webhook URL from Step 2
2. Go to **Stripe Dashboard → Developers → Webhooks → Add endpoint**
3. Paste the URL
4. Set event type: `payment_intent.succeeded`
5. Copy the **Signing secret** — store it securely (not in Make)
6. Note: Make's native `stripe:TriggerNewEvent` module handles Stripe signature verification automatically. If you upgrade M-BOOKING-CREATION from a raw webhook to the native Stripe module after initial testing, this step becomes automatic

---

### Step 7: Configure Will's Slack User ID (M-SLACK-ALERTS Emergency Route)

In M-SLACK-ALERTS, module 8 sends a direct Slack message to `WILL_SLACK_USER_ID_PLACEHOLDER` for EMERGENCY alerts.

1. In Slack, right-click on Will's profile → **Copy member ID** (format: `U0XXXXXXX`)
2. In Make, open M-SLACK-ALERTS module 8 → update the channel value to Will's user ID

---

### Step 8: Activate Scenarios

Activate in the same order as import:

1. M-AUDIT-LOGGER — activate first
2. M-SLACK-ALERTS — activate second
3. M-BRAND-ROUTER
4. M-LEAD-INTAKE
5. M-CONCIERGE-ASSIGNMENT
6. M-BOOKING-CONFIRMATION
7. M-STRIPE-DEPOSIT
8. M-BOOKING-CREATION — activate last (receives Stripe webhooks)

**Test each scenario with a manual webhook test before activating the next one.**

---

## Modules That May Require Manual Replacement After Import

| Scenario | Module | Issue | Action |
|---|---|---|---|
| M-BOOKING-CREATION | Module 1 (Webhook trigger) | Consider upgrading to native `stripe:TriggerNewEvent` for automatic signature verification | Optional upgrade post-testing |
| M-AUDIT-LOGGER | Modules 5–6 | AUTOMATION_HEALTH_TABLE_ID placeholder | Replace with real table ID (see Step 5) |
| M-CONCIERGE-ASSIGNMENT | Module 3 | CONCIERGE_OPERATORS_TABLE_ID placeholder | Replace with real table ID (see Step 5) |
| M-STRIPE-DEPOSIT | Module 4 | Stripe secret key in Authorization header | Replace with real Stripe key (see Step 3) |
| Any | Any Airtable native module | Connection must be rebound after import | Standard Make reconnect flow |
| Any | Any slack:postMessage | Connection must be rebound after import | Standard Make reconnect flow |
| M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION | gmail:ActionSendEmail | Connection must be rebound after import | Standard Make reconnect flow |

---

## Screenshots Will Should Take If Stuck

1. **After import, before activation**: Screenshot of each scenario's module canvas showing the red "reconnect" warning icons — helps identify which modules need credential rebinding
2. **Webhook URL copy step**: Screenshot of the webhook modal for each scenario with the URL visible — acts as backup record
3. **Stripe webhook dashboard**: Screenshot of Stripe → Developers → Webhooks showing M-BOOKING-CREATION endpoint registered with correct event type
4. **First successful test run**: Screenshot of Make scenario execution history showing a successful run with all modules green
5. **M-AUDIT-LOGGER first write**: Screenshot of the Airtable Audit_Log table showing the first record written — confirms end-to-end logging is working
6. **Error handler test**: Deliberately send a malformed payload to one scenario, screenshot the Slack #ops-alerts notification that arrives — confirms error handlers are active

---

## Post-Import Checklist

- [ ] All 8 scenarios imported
- [ ] All webhook URLs recorded and distributed back into calling scenarios
- [ ] All Airtable connections rebound
- [ ] All Slack connections rebound
- [ ] All Gmail connections rebound (SSS and ME)
- [ ] Stripe secret key inserted in M-STRIPE-DEPOSIT module 4
- [ ] SMS bearer token inserted in M-STRIPE-DEPOSIT module 7 and M-BOOKING-CONFIRMATION modules 5, 7
- [ ] Claude API key inserted in M-BRAND-ROUTER modules 5 and 8
- [ ] SSS and ME system prompts inserted in M-BRAND-ROUTER modules 5 and 8
- [ ] AUTOMATION_HEALTH_TABLE_ID resolved in M-AUDIT-LOGGER
- [ ] CONCIERGE_OPERATORS_TABLE_ID resolved in M-CONCIERGE-ASSIGNMENT
- [ ] Will's Slack user ID set in M-SLACK-ALERTS module 8
- [ ] Stripe webhook endpoint registered in Stripe dashboard pointing to M-BOOKING-CREATION
- [ ] All 8 scenarios activated in correct order
- [ ] Manual test run completed for at least M-AUDIT-LOGGER and M-LEAD-INTAKE
- [ ] First successful Airtable Audit_Log record confirmed
