# Final Stage 1 Import Order
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION IMPORT GUIDE
**Branch:** `claude/final-blueprint-audit-athcl`

---

## Pre-Import Prerequisites

Complete every item before opening Make.com.

- [ ] Access to She Said Sail production Make.com organization confirmed
- [ ] Credential vault open with the following available:
  - Airtable Personal Access Token (or OAuth account for base `appdZ49WqgjRXxA1R`)
  - Anthropic API key
  - Gmail OAuth account for `hello@shesaidsail.com`
  - Slack workspace access for She Said Sail
  - Stripe Restricted Key with `payment_links:write`, `products:write`, `prices:write`
  - Quo SMS API endpoint URL and API key
- [ ] Squarespace site editor access for the lead intake form
- [ ] Stripe Dashboard access (Developers → Webhooks)
- [ ] Airtable base `appdZ49WqgjRXxA1R` live and accessible
- [ ] Will's Slack User ID (format: `U0XXXXXXXXX`) available
- [ ] Founder Decision logged in Airtable for production activation

---

## Section 1 — Blueprint File Inventory

All 8 files located at:
`08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/`

| File | Status | Patch Applied |
|---|---|---|
| `M-AUDIT-LOGGER.blueprint.json` | FINAL — no patch required | None |
| `M-SLACK-ALERTS.blueprint.json` | FINAL — no patch required | None |
| `M-BRAND-ROUTER.blueprint.json` | FINAL — no patch required | None |
| `M-LEAD-INTAKE.blueprint.json` | FINAL — no patch required | None |
| `M-STRIPE-DEPOSIT.blueprint.json` | FINAL — no patch required | None |
| `M-BOOKING-CREATION.blueprint.json` | FINAL — no patch required | None |
| `M-CONCIERGE-ASSIGNMENT.blueprint.json` | **PATCHED 2026-05-16** | Module 6: `stripe:ActionCreatePaymentLink` → `stripe:MakeAnAPICall` POST `/v1/payment_links`. Unit_amount corrected to multiply by 100 (cents). |
| `M-BOOKING-CONFIRMATION.blueprint.json` | **PATCHED 2026-05-16** | Module 6: `stripe:ActionCreatePaymentLink` → `stripe:MakeAnAPICall` POST `/v1/payment_links`. |

---

## Section 2 — Exact Import Order

**CRITICAL: Do not deviate from this sequence.** M-AUDIT-LOGGER and M-SLACK-ALERTS must be imported first so their webhook URLs are available when configuring later scenarios.

### Import Sequence

| Step | Blueprint | Reason for Position |
|---|---|---|
| 1 | `M-AUDIT-LOGGER.blueprint.json` | All other scenarios call this — webhook URL must be collected first |
| 2 | `M-SLACK-ALERTS.blueprint.json` | M-BRAND-ROUTER and others dispatch alerts here — URL needed before others activate |
| 3 | `M-BRAND-ROUTER.blueprint.json` | Called by M-LEAD-INTAKE — webhook URL must be collected before step 4 |
| 4 | `M-LEAD-INTAKE.blueprint.json` | Depends on M-BRAND-ROUTER and M-AUDIT-LOGGER URLs |
| 5 | `M-STRIPE-DEPOSIT.blueprint.json` | Standalone — only needs Airtable, Gmail, Slack, and Audit Logger URL |
| 6 | `M-BOOKING-CREATION.blueprint.json` | Depends on M-AUDIT-LOGGER URL only |
| 7 | `M-CONCIERGE-ASSIGNMENT.blueprint.json` | Depends on M-AUDIT-LOGGER URL only |
| 8 | `M-BOOKING-CONFIRMATION.blueprint.json` | Depends on M-AUDIT-LOGGER URL only |

### How to Import Each Blueprint

1. In Make.com, go to **Scenarios**
2. Click **Create a new scenario**
3. In the scenario editor, click the **three-dot menu** (top right) → **Import Blueprint**
4. Select the `.blueprint.json` file
5. Click **Save** — do NOT activate (leave toggle OFF/grey)
6. Rename the scenario in Make to match the blueprint `name` field exactly
7. Proceed to collect webhook URL (for webhook-triggered scenarios) and then to Section 3 rebinding

---

## Section 3 — Required Credential Rebindings

Complete these bindings after import. All connections appear as "unbound" immediately after import — this is expected.

### 3A — Airtable Connection

**Placeholder:** `RECONNECT_AIRTABLE_CONNECTION`
**Used in:** All 8 scenarios (every Airtable module)

1. Open any Airtable module in M-AUDIT-LOGGER (module 2)
2. Click "Add a connection" → select Airtable → OAuth or API Key
3. Authorize with the account owning base `appdZ49WqgjRXxA1R`
4. Name the connection: `SSS — Airtable Production`
5. Apply this same connection to every Airtable module across all 8 scenarios

**Airtable IDs to verify match the live production base:**

| Constant | ID | Purpose |
|---|---|---|
| Base ID | `appdZ49WqgjRXxA1R` | She Said Sail production base |
| Requests/Leads table | `tblTlSB9CO4dTGodg` | Inbound leads from Squarespace |
| Audit Log table | `tblrMpTfMk8q1eNHp` | Idempotency store + audit events |
| Bookings table | `tbl72omPibBkn2hZL` | Charter bookings |

**Verify these IDs in Airtable:** open each table, check the URL — the table ID follows `tbl` in the URL path.

### 3B — Slack Connection

**Placeholder:** `RECONNECT_SLACK_CONNECTION`
**Used in:** M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION

1. Open any Slack module (e.g., M-SLACK-ALERTS module 3)
2. Click "Add a connection" → select Slack → Sign in with Slack
3. Authorize the She Said Sail workspace
4. Name the connection: `SSS — Slack Production`
5. Apply to all Slack modules across all 6 scenarios

**Channels required:** confirm the connection account is a member of:
- `#sss-ops-alerts`
- `#sss-emergency-ops`

### 3C — Anthropic Claude Connection

**Placeholder:** `RECONNECT_CLAUDE_API_KEY`
**Used in:** M-BRAND-ROUTER (module 3), M-BOOKING-CREATION (module 7)

1. Open M-BRAND-ROUTER module 3 (Anthropic Claude)
2. Click "Add a connection" → select Anthropic → enter API key
3. Name the connection: `SSS — Anthropic Claude Production`
4. Verify model field is set to `claude-sonnet-4-20250514`
5. Verify max_tokens: `600`, temperature: `0.4`
6. Apply same connection to M-BOOKING-CREATION module 7

**IMPORTANT:** If Make's Anthropic module does not expose a `temperature` field, this defaults to 1.0. Document this in Airtable Founder Decisions table and do not revert to HTTP without explicit Founder Decision from Will.

### 3D — Gmail Connection

**Placeholder:** `RECONNECT_GMAIL_CONNECTION`
**Used in:** M-LEAD-INTAKE (module 7), M-CONCIERGE-ASSIGNMENT (module 8), M-STRIPE-DEPOSIT (module 8), M-BOOKING-CREATION (module 8), M-BOOKING-CONFIRMATION (module 8)

1. Open M-LEAD-INTAKE module 7 (Gmail)
2. Click "Add a connection" → select Gmail → Sign in with Google
3. Authorize with the account owning `hello@shesaidsail.com`
4. Name the connection: `SSS — Gmail hello@shesaidsail.com`
5. Apply to all 5 Gmail modules across all 5 scenarios
6. In each module confirm the "From" field is `hello@shesaidsail.com`

**Safety step before activation:** Before activating any Gmail scenario, set "To" field temporarily to an internal test address, send one test, then restore to the dynamic mapping. Do not send to real clients until tests pass.

### 3E — Stripe Connection

**Placeholder:** `RECONNECT_STRIPE_CONNECTION`
**Used in:** M-CONCIERGE-ASSIGNMENT (module 6), M-BOOKING-CONFIRMATION (module 6)

1. Open M-CONCIERGE-ASSIGNMENT module 6 (Stripe — Make an API Call)
2. Click "Add a connection" → select Stripe → enter Stripe Restricted Key
3. Required key permissions: `payment_links:write`, `products:write`, `prices:write`
4. Do NOT use the full Stripe Secret Key — use a Restricted Key scoped to minimum required permissions
5. Name the connection: `SSS — Stripe Production`
6. Apply same connection to M-BOOKING-CONFIRMATION module 6

**Stripe module note (M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION):**
Module 6 in both patched blueprints uses `stripe:MakeAnAPICall` with a form-encoded body calling `POST /v1/payment_links`. The response from Stripe's Payment Links API returns a JSON object with `id` and `url` at the top level. These are referenced downstream as `{{6.id}}` and `{{6.url}}`. Verify these fields populate correctly in the first test run. If the Stripe MakeAnAPICall module wraps the response in a `body` object, update references to `{{6.body.id}}` and `{{6.body.url}}` in modules 7, 8, 9, and 10 of each blueprint.

---

## Section 4 — Required Webhook Rebindings

After each webhook-triggered scenario is imported, Make generates a new webhook URL. These URLs must be collected and applied as described below.

### 4A — Webhook URLs to Collect (in import order)

| After importing | Collect URL for | URL variable name |
|---|---|---|
| M-AUDIT-LOGGER | Module 1 webhook URL | `AUDIT_LOGGER_URL` |
| M-SLACK-ALERTS | Module 1 webhook URL | `SLACK_ALERTS_URL` |
| M-BRAND-ROUTER | Module 1 webhook URL | `BRAND_ROUTER_URL` |
| M-LEAD-INTAKE | Module 1 webhook URL | `LEAD_INTAKE_URL` |
| M-STRIPE-DEPOSIT | Module 1 webhook URL | `STRIPE_DEPOSIT_URL` |

To collect: click module 1 in each scenario → click "Copy address to clipboard" → save in a secure temporary document.

### 4B — HTTP Module URL Placeholders to Replace

After all 8 scenarios are imported and webhook URLs collected:

| Scenario | Module | Placeholder | Replace With |
|---|---|---|---|
| M-SLACK-ALERTS | Module 8 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-BRAND-ROUTER | Module 10 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-LEAD-INTAKE | Module 6 | `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` | `BRAND_ROUTER_URL` |
| M-LEAD-INTAKE | Module 9 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-CONCIERGE-ASSIGNMENT | Module 10 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-CONCIERGE-ASSIGNMENT | Module 11 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-STRIPE-DEPOSIT | Module 10 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-BOOKING-CREATION | Module 11 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-BOOKING-CREATION | Module 12 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-BOOKING-CONFIRMATION | Module 11 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |
| M-BOOKING-CONFIRMATION | Module 12 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | `AUDIT_LOGGER_URL` |

### 4C — Slack User ID Placeholder

| Scenario | Modules | Placeholder | Replace With |
|---|---|---|---|
| M-SLACK-ALERTS | Modules 5 and 7 | `RECONNECT_WILL_SLACK_USER_ID` | Will's Slack member ID (format: `U0XXXXXXXXX`) |

To find Will's Slack member ID: In Slack, open Will's profile → click "More" → "Copy member ID."

### 4D — Quo SMS Placeholders

| Scenario | Module | Placeholder | Replace With |
|---|---|---|---|
| M-CONCIERGE-ASSIGNMENT | Module 9 (URL field) | `RECONNECT_QUO_API_ENDPOINT` | Quo API endpoint from credential vault |
| M-CONCIERGE-ASSIGNMENT | Module 9 (Authorization header value) | `RECONNECT_QUO_API_KEY` | Quo API key from credential vault |
| M-BOOKING-CONFIRMATION | Module 9 (URL field) | `RECONNECT_QUO_API_ENDPOINT` | Quo API endpoint from credential vault |
| M-BOOKING-CONFIRMATION | Module 9 (Authorization header value) | `RECONNECT_QUO_API_KEY` | Quo API key from credential vault |

Store Quo credentials in Make Data Store — do not leave as inline plain text in the module field.

### 4E — External Webhook Registrations

**Squarespace (M-LEAD-INTAKE):**
1. Copy `LEAD_INTAKE_URL`
2. Log into Squarespace site editor → open the lead intake form block
3. Edit → Storage → Add → Webhook → paste `LEAD_INTAKE_URL` → Save
4. Submit a test form submission to confirm payload delivery
5. Verify these field names match the blueprint's `expect` schema in module 1:
   - `name` → Lead Full Name
   - `email` → Lead Email
   - `phone` → Lead Phone
   - `inquiry_text` → Inquiry Message (Squarespace internal name may differ)
   - `event_date` → Requested Event Date
   - `guest_count` → Guest Count
   - `source_page` → Source Page URL
   - `form_name` → Squarespace Form Name
6. If Squarespace delivers different field names, update the mapper in M-LEAD-INTAKE module 1

**Stripe (M-STRIPE-DEPOSIT):**
1. Copy `STRIPE_DEPOSIT_URL`
2. Log into Stripe Dashboard → Developers → Webhooks → Add endpoint
3. Paste `STRIPE_DEPOSIT_URL` as the endpoint URL
4. Subscribe to events: `payment_intent.succeeded` only
5. Save → copy the Signing Secret (`whsec_...`)
6. Store Signing Secret in Make Data Store — do NOT embed in blueprint
7. In M-STRIPE-DEPOSIT webhook module settings: enable Stripe-Signature header validation if available

---

## Section 5 — Required Airtable Field Checks

Before activating any scenario, verify these Airtable fields exist with exact names and types in the production base.

### Requests/Leads Table (`tblTlSB9CO4dTGodg`)

| Field Name | Type | Used In |
|---|---|---|
| Lead_Name | Single line text | M-LEAD-INTAKE |
| Source_Email | Email | M-LEAD-INTAKE (idempotency key) |
| Phone | Phone number | M-LEAD-INTAKE |
| Inquiry_Text | Long text | M-LEAD-INTAKE, M-BRAND-ROUTER |
| Requested_Event_Date | Date | M-LEAD-INTAKE |
| Guest_Count | Number | M-LEAD-INTAKE |
| Source_Page | URL | M-LEAD-INTAKE |
| Form_Name | Single line text | M-LEAD-INTAKE |
| Status | Single select | M-LEAD-INTAKE (value: NEW) |
| Agent_Status | Single select | M-LEAD-INTAKE (AI_RESPONDING), M-BRAND-ROUTER (AI_RESPONDING, HUMAN_REVIEW) |
| Brand | Single select | M-BRAND-ROUTER (SSS, ME, AMBIGUOUS) |
| AI_Confidence_Score | Number | M-BRAND-ROUTER |
| Brand_Classification_Reason | Long text | M-BRAND-ROUTER |
| Escalation_Reason | Long text | M-BRAND-ROUTER |
| Source_System | Single line text | M-LEAD-INTAKE |
| Environment | Single select | M-LEAD-INTAKE |
| Idempotency_Key | Single line text | M-LEAD-INTAKE |
| Created_At | Date/time | M-LEAD-INTAKE |

### Audit Log Table (`tblrMpTfMk8q1eNHp`)

| Field Name | Type | Used In |
|---|---|---|
| Scenario_ID | Single line text | M-AUDIT-LOGGER |
| Action_Type | Single line text | M-AUDIT-LOGGER |
| Brand | Single select | M-AUDIT-LOGGER |
| Booking_ID | Single line text | M-AUDIT-LOGGER |
| Request_ID | Single line text | M-AUDIT-LOGGER |
| Actor | Single select | M-AUDIT-LOGGER (AI, SYSTEM, Human) |
| Autonomy_Tier | Single select | M-AUDIT-LOGGER (A, B, C) |
| Prompt_Version | Single line text | M-AUDIT-LOGGER |
| AI_Confidence_Score | Number | M-AUDIT-LOGGER |
| Approval_State | Single line text | M-AUDIT-LOGGER |
| Environment | Single select | M-AUDIT-LOGGER |
| Idempotency_Key | Single line text | M-AUDIT-LOGGER (also used by all scenarios for idempotency lookup) |
| Payload_Summary | Long text | M-AUDIT-LOGGER |
| Outcome | Single select | M-AUDIT-LOGGER (SUCCESS, FAILURE, SKIPPED) |
| Error_Message | Long text | M-AUDIT-LOGGER |
| City | Single line text | M-AUDIT-LOGGER |
| Logged_At | Date/time | M-AUDIT-LOGGER |

### Bookings Table (`tbl72omPibBkn2hZL`)

| Field Name | Type | Used In |
|---|---|---|
| Booking_Name | Single line text | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Client_Name | Single line text | M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Client_Email | Email | M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Client_Phone | Phone number | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| Charter_Date | Date | M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Charter_Start_Time | Single line text | M-BOOKING-CREATION |
| Charter_Duration_Hours | Number | M-BOOKING-CREATION |
| Guest_Count | Number | M-BOOKING-CREATION |
| Package_Name | Single line text | M-BOOKING-CREATION |
| Package_Price | Currency/Number | M-CONCIERGE-ASSIGNMENT (deposit calc), M-BOOKING-CONFIRMATION (balance calc) |
| Vessel_Name | Single line text | M-BOOKING-CREATION |
| Departure_Location | Single line text | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| City | Single line text | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Brand | Single select | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Status | Single select | M-CONCIERGE-ASSIGNMENT (triggers AVAILABILITY_CONFIRMED), M-STRIPE-DEPOSIT (→ DEPOSIT_PAID), M-BOOKING-CONFIRMATION (→ BALANCE_DUE) |
| Agreement_Signed | Checkbox | M-BOOKING-CREATION (trigger formula) |
| Charter_Brief_Sent | Checkbox | M-BOOKING-CREATION (trigger formula + update) |
| Charter_Brief_Sent_At | Date/time | M-BOOKING-CREATION |
| Charter_Brief_Text | Long text | M-BOOKING-CREATION |
| Balance_Reminder_Sent | Checkbox | M-BOOKING-CONFIRMATION (trigger formula + update) |
| Balance_Reminder_Sent_At | Date/time | M-BOOKING-CONFIRMATION |
| Stripe_Deposit_Link | URL | M-CONCIERGE-ASSIGNMENT |
| Stripe_Payment_Link_ID | Single line text | M-CONCIERGE-ASSIGNMENT |
| Stripe_Balance_Link | URL | M-BOOKING-CONFIRMATION |
| Stripe_Balance_Payment_Link_ID | Single line text | M-BOOKING-CONFIRMATION |
| Stripe_Payment_Intent_ID | Single line text | M-STRIPE-DEPOSIT |
| Deposit_Amount_Received | Currency/Number | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION (balance calc) |
| Deposit_Paid_At | Date/time | M-STRIPE-DEPOSIT |
| Idempotency_Key | Single line text | M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Emergency_Flag | Checkbox | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION (guard) |
| Automations_Paused | Checkbox | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION (guard) |
| City_Manager_Name | Single line text | M-BOOKING-CREATION |
| City_Manager_Email | Email | M-BOOKING-CREATION |
| Special_Requests | Long text | M-BOOKING-CREATION |
| Food_Beverage_Notes | Long text | M-BOOKING-CREATION |
| Dietary_Restrictions | Long text | M-BOOKING-CREATION |

---

## Section 6 — Test Procedures

Run each test before activating the scenario. Use internal test data only — never target real clients or real Stripe transactions.

### Test 1 — M-AUDIT-LOGGER

**What to test:** Airtable write  
**Method:** Send a POST request to `AUDIT_LOGGER_URL` using Make's "Run once" or an external tool (e.g., Postman)

```json
{
  "scenario_id": "TEST",
  "action_type": "IMPORT_TEST",
  "brand": "SSS",
  "request_id": "TEST-001",
  "actor": "SYSTEM",
  "autonomy_tier": "A",
  "environment": "Production",
  "idempotency_key": "TEST-AUDIT-001",
  "payload_summary": "Stage 1 import test — M-AUDIT-LOGGER",
  "outcome": "SUCCESS"
}
```

**Pass criteria:** New record appears in Airtable Audit Log table `tblrMpTfMk8q1eNHp` with all fields populated.

---

### Test 2 — M-SLACK-ALERTS

**What to test:** Slack message delivery across alert levels  
**Method:** POST to `SLACK_ALERTS_URL`

L1 test:
```json
{"alert_level":"L1","scenario_id":"TEST","brand":"SSS","message_text":"Stage 1 import test — L1 alert","environment":"Production","idempotency_key":"TEST-SLACK-001"}
```

L3 test (uses Will's User ID — confirm DM is received):
```json
{"alert_level":"L3","scenario_id":"TEST","brand":"SSS","message_text":"Stage 1 import test — L3 escalation","environment":"Production","idempotency_key":"TEST-SLACK-002"}
```

**Pass criteria:** L1 → message appears in `#sss-ops-alerts`. L3 → message in `#sss-ops-alerts` + DM delivered to Will. Audit log entry appears in Airtable.

---

### Test 3 — M-BRAND-ROUTER

**What to test:** Claude brand classification + Airtable update  
**Method:** First create a test record manually in Airtable Requests table. Then POST to `BRAND_ROUTER_URL`:

```json
{
  "request_id": "<airtable_test_record_id>",
  "lead_name": "Test Lead",
  "lead_email": "test@internal.com",
  "inquiry_text": "I'd love to book a bachelorette yacht party in Miami for 15 ladies!",
  "source_url": "https://shesaidsail.com/book",
  "environment": "Production",
  "idempotency_key": "TEST-BRAND-001"
}
```

**Pass criteria:** Airtable Request record `Brand` updated to `SSS`, `AI_Confidence_Score` populated, `Agent_Status` = `AI_RESPONDING`. Audit log entry written.

**If AMBIGUOUS is returned:** Slack alert fires in `#sss-ops-alerts` — confirm message received.

---

### Test 4 — M-LEAD-INTAKE

**What to test:** Full intake flow — Squarespace webhook → Airtable create → Gmail auto-reply → Slack notification → Brand Router call  
**Method:** Submit a test form on the Squarespace site (or POST directly to `LEAD_INTAKE_URL` mimicking Squarespace payload)

```json
{
  "name": "Test Lead Squarespace",
  "email": "test-internal@shesaidsail.com",
  "phone": "555-000-0001",
  "inquiry_text": "Test inquiry — stage 1 import validation",
  "event_date": "2026-08-01",
  "guest_count": "12",
  "source_page": "https://shesaidsail.com/book",
  "form_name": "Main Booking Form"
}
```

**Pass criteria:** Request record created in Airtable with Status = NEW. Auto-reply email received at `test-internal@shesaidsail.com`. Slack notification posted in `#sss-ops-alerts`. M-BRAND-ROUTER triggered (Brand field updated on Airtable record). Audit log entry written.

**Field name note:** If Squarespace delivers different field names, the test will reveal the mismatch. Update module 1 mapper in Make accordingly.

---

### Test 5 — M-STRIPE-DEPOSIT

**What to test:** Stripe webhook receipt → Airtable update → Gmail confirmation  
**Method:** Use Stripe Dashboard → Developers → Webhooks → select the M-STRIPE-DEPOSIT endpoint → Send test event → `payment_intent.succeeded`

OR send a test webhook payload to `STRIPE_DEPOSIT_URL`:

```json
{
  "id": "evt_test_001",
  "type": "payment_intent.succeeded",
  "created": 1747353600,
  "data": {
    "object": {
      "id": "pi_test_001",
      "amount_received": 150000,
      "metadata": {
        "payment_link": ""
      }
    }
  }
}
```

**Before testing:** Create a test Booking record in Airtable with `Stripe_Payment_Intent_ID` = `pi_test_001` OR `Stripe_Payment_Link_ID` matching the test payload. Use `Client_Email` = `test-internal@shesaidsail.com`.

**Pass criteria:** Booking record Status updated to `DEPOSIT_PAID`. `Deposit_Amount_Received` = 1500 (amount_received / 100). Confirmation email received at test address. Slack notification in `#sss-ops-alerts`. Audit log entry written.

---

### Test 6 — M-CONCIERGE-ASSIGNMENT

**What to test:** Airtable trigger → Stripe Payment Link creation (patched: MakeAnAPICall) → Airtable update → Gmail deposit email → Slack notification  
**Method:** Create or update a test Booking record in Airtable. Set Status = `AVAILABILITY_CONFIRMED`. Ensure `Emergency_Flag` and `Automations_Paused` are unchecked.

**Required Booking record fields for test:**
- `Client_Email`: `test-internal@shesaidsail.com`
- `Client_Name`: `Test Client`
- `Client_Phone`: `555-000-0002`
- `Booking_Name`: `Test Charter - Import Test`
- `Charter_Date`: a future date (at least 7 days out)
- `Package_Price`: `2000` (test amount — 30% deposit = $600, Stripe receives 60000 cents)
- `Brand`: `SSS`
- `City`: `Miami`
- `Emergency_Flag`: unchecked
- `Automations_Paused`: unchecked

**Pass criteria:** Stripe Payment Link created successfully (URL appears in Booking record `Stripe_Deposit_Link`). Booking Status updated to `DEPOSIT_SENT`. Deposit email received at `test-internal@shesaidsail.com` with payment link URL. Slack notification in `#sss-ops-alerts`. Audit log entry written.

**If Stripe MakeAnAPICall response fields are wrapped:** If `{{6.url}}` returns empty, open Make scenario execution log, inspect module 6 output, and determine if response is `body.url` instead of `url`. If so, update modules 7, 8, 9, 10 references from `{{6.url}}` → `{{6.body.url}}` and `{{6.id}}` → `{{6.body.id}}` in both M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION, then re-test.

**SMS test (Quo):** Disable module 9 (Quo SMS) for initial testing if Quo credentials are not yet ready. Quo can be re-enabled and tested separately.

---

### Test 7 — M-BOOKING-CREATION

**What to test:** Airtable trigger → Claude charter brief generation → Gmail to City Manager → Airtable update → Slack notification  
**Method:** Create or update a test Booking record. Set the following to trigger the formula:
- Status = `CONFIRMED`
- Agreement_Signed = `true` (checked)
- Charter_Date = today + 10 days (within 14-day window)
- Charter_Brief_Sent = `false` (unchecked)
- `City_Manager_Email`: `test-internal@shesaidsail.com`
- `City_Manager_Name`: `Test City Manager`

Ensure `Emergency_Flag` and `Automations_Paused` are unchecked.

**Pass criteria:** Charter brief generated by Claude (check `Charter_Brief_Text` field in Airtable). `Charter_Brief_Sent` set to `true`. Email with charter brief received at `test-internal@shesaidsail.com`. Slack notification in `#sss-ops-alerts`. Audit log entry written.

**Verify Claude output:** The charter brief must contain only information from the provided record fields. If Claude returns an error or the brief is empty, check Anthropic connection and verify model `claude-sonnet-4-20250514` is accessible.

---

### Test 8 — M-BOOKING-CONFIRMATION

**What to test:** Airtable trigger → Stripe Payment Link creation (patched: MakeAnAPICall, balance) → Airtable update → Gmail balance reminder → Slack notification  
**Method:** Create or update a test Booking record. Set:
- Status = `CONFIRMED`
- Charter_Date = today + 2 days (within 72-hour window)
- Balance_Reminder_Sent = `false` (unchecked)
- `Package_Price`: `2000`
- `Deposit_Amount_Received`: `600` (balance = $1400, Stripe receives 140000 cents)
- `Client_Email`: `test-internal@shesaidsail.com`
- `Emergency_Flag`: unchecked
- `Automations_Paused`: unchecked

**Pass criteria:** Stripe Payment Link for balance ($1400) created. Balance link URL appears in `Stripe_Balance_Link`. Status → `BALANCE_DUE`. `Balance_Reminder_Sent` → true. Balance reminder email received at test address with payment link URL. Slack notification in `#sss-ops-alerts`. Audit log entry written.

**Same MakeAnAPICall response field note applies as Test 6.**

---

## Section 7 — Activation Order

**Only activate after ALL 8 tests pass and all placeholders are confirmed resolved.**

| Step | Scenario | Confirm Before Activating |
|---|---|---|
| 1 | M-AUDIT-LOGGER | Test 1 passed; Airtable connection bound |
| 2 | M-SLACK-ALERTS | Test 2 passed; Slack connection bound; Will's User ID set in modules 5 and 7 |
| 3 | M-BRAND-ROUTER | Test 3 passed; Anthropic connection bound; M-AUDIT-LOGGER URL set in module 10 |
| 4 | M-LEAD-INTAKE | Test 4 passed; all connections bound; Squarespace form webhook registered; M-BRAND-ROUTER and M-AUDIT-LOGGER URLs set in modules 6 and 9 |
| 5 | M-STRIPE-DEPOSIT | Test 5 passed; Stripe webhook registered in Stripe Dashboard; all connections bound; M-AUDIT-LOGGER URL set in module 10 |
| 6 | M-BOOKING-CREATION | Test 7 passed; all connections bound; M-AUDIT-LOGGER URL set in modules 11 and 12 |
| 7 | M-CONCIERGE-ASSIGNMENT | Test 6 passed; Stripe MakeAnAPICall response fields confirmed; Quo SMS credentials set; M-AUDIT-LOGGER URL set in modules 10 and 11 |
| 8 | M-BOOKING-CONFIRMATION | Test 8 passed; same Stripe confirmation as step 7; M-AUDIT-LOGGER URL set in modules 11 and 12 |

**How to activate:** In each scenario, click the toggle at the bottom left of the scenario editor to turn it ON (green). Log activation in Airtable Founder Decisions table.

---

## Section 8 — Rollback Order

If any scenario must be disabled after activation, disable in reverse activation order to prevent data loss or incomplete processing.

| Step | Scenario | Rollback Action |
|---|---|---|
| 1 | M-BOOKING-CONFIRMATION | Toggle OFF — no in-progress runs affected (polling trigger) |
| 2 | M-CONCIERGE-ASSIGNMENT | Toggle OFF — no in-progress runs affected (polling trigger) |
| 3 | M-BOOKING-CREATION | Toggle OFF — no in-progress runs affected (polling trigger) |
| 4 | M-STRIPE-DEPOSIT | Toggle OFF — Stripe will retry unprocessed webhooks when re-enabled; idempotency guard prevents duplicate processing |
| 5 | M-LEAD-INTAKE | Toggle OFF — any Squarespace submissions during downtime will not be processed; manual review required for missed leads |
| 6 | M-BRAND-ROUTER | Toggle OFF — M-LEAD-INTAKE calls will fail silently (HTTP POST with handleErrors: false) |
| 7 | M-SLACK-ALERTS | Toggle OFF — no alerts will fire; all scenarios continue but alert logging fails silently |
| 8 | M-AUDIT-LOGGER | Toggle OFF last — all other scenarios' audit HTTP calls will fail silently; core operations continue but audit trail stops |

**Emergency stop (all scenarios):** In Make.com, go to Scenarios → select all Stage 1 scenarios → bulk toggle OFF. Use this only for L4 emergency. Log in Airtable Founder Decisions immediately.

**Data integrity after rollback:**
- All idempotency keys written to Airtable Audit Log before rollback remain intact
- Re-enabling scenarios after rollback will not reprocess already-completed events (idempotency guard)
- Exception: M-STRIPE-DEPOSIT — Stripe retries pending webhooks; idempotency guard handles these correctly on re-enable
- Exception: Airtable-triggered scenarios (M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION) — on re-enable, Make will poll from last checkpoint; records updated while scenario was OFF may be reprocessed if they still match the trigger formula. Verify Booking record statuses after re-enabling.

---

## Appendix A — Full Placeholder Resolution Checklist

**Connections (all bound before testing):**
- [ ] `RECONNECT_AIRTABLE_CONNECTION` → `SSS — Airtable Production` — all 8 scenarios
- [ ] `RECONNECT_SLACK_CONNECTION` → `SSS — Slack Production` — 6 scenarios
- [ ] `RECONNECT_CLAUDE_API_KEY` → `SSS — Anthropic Claude Production` — M-BRAND-ROUTER, M-BOOKING-CREATION
- [ ] `RECONNECT_GMAIL_CONNECTION` → `SSS — Gmail hello@shesaidsail.com` — 5 scenarios
- [ ] `RECONNECT_STRIPE_CONNECTION` → `SSS — Stripe Production` — M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION

**Webhook URLs (collected post-import, applied to HTTP modules):**
- [ ] `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` → `AUDIT_LOGGER_URL` — 7 scenarios (11 modules)
- [ ] `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` → `BRAND_ROUTER_URL` — M-LEAD-INTAKE module 6

**Manual values:**
- [ ] `RECONNECT_WILL_SLACK_USER_ID` → Will's Slack member ID — M-SLACK-ALERTS modules 5 and 7
- [ ] `RECONNECT_QUO_API_ENDPOINT` → Quo endpoint — M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION module 9
- [ ] `RECONNECT_QUO_API_KEY` → Quo API key — M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION module 9

**External system registrations:**
- [ ] Squarespace form webhook → `LEAD_INTAKE_URL`
- [ ] Stripe Dashboard webhook → `STRIPE_DEPOSIT_URL`, event: `payment_intent.succeeded`

**Post-test verification (Stripe patched modules):**
- [ ] M-CONCIERGE-ASSIGNMENT module 6 `{{6.url}}` populated correctly in test run
- [ ] M-CONCIERGE-ASSIGNMENT module 6 `{{6.id}}` populated correctly in test run
- [ ] M-BOOKING-CONFIRMATION module 6 `{{6.url}}` populated correctly in test run
- [ ] M-BOOKING-CONFIRMATION module 6 `{{6.id}}` populated correctly in test run

---

## Appendix B — Known Pending Verifications

These items are flagged from the Gap Audit and remain open. They do not block import but require confirmation during rebinding.

| Item | Blueprint | What to Check |
|---|---|---|
| `anthropic:ActionCreateMessage` module ID | M-BRAND-ROUTER, M-BOOKING-CREATION | Confirm Make's Anthropic app exposes `model`, `max_tokens`, `temperature`, `system`, `messages` fields. Confirm `claude-sonnet-4-20250514` is selectable. |
| `airtable:TriggerNewRecord` trigger support | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION | Confirm Make Airtable app offers a "Watch Records" / "New Record" trigger type with formula filter support. |
| Squarespace field name mapping | M-LEAD-INTAKE | After test submission, confirm Squarespace delivers `name`, `email`, `phone`, `inquiry_text`, `event_date`, `guest_count`, `source_page`, `form_name` — update module 1 mapper if names differ. |
| Stripe MakeAnAPICall response field path | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION | After first test run: confirm `{{6.url}}` and `{{6.id}}` resolve correctly. If response is wrapped in `body`, update downstream modules to `{{6.body.url}}` and `{{6.body.id}}`. |
