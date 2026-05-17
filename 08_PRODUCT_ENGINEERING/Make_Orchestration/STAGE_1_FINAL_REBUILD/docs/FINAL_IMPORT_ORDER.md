# FINAL IMPORT ORDER — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Status:** PRODUCTION-READY  
**Owner:** Will (Founder)  
**Base:** appdZ49WqgjRXxA1R (She Said Sail)

---

## MANDATORY IMPORT SEQUENCE

Import order is strict. Scenarios that are called by other scenarios MUST be live and have their webhook URLs copied before dependent scenarios are imported.

| Step | File | Make Scenario Name | Trigger Type | Depends On | Priority |
|------|------|--------------------|--------------|------------|----------|
| 1 | `M-OPS-LOGGER-ALERTER.json` | SSS-OPS-LOGGER-ALERTER | Webhook (called by all) | None | **FIRST — CRITICAL** |
| 2 | `M-BRAND-ROUTER.json` | SSS-BRAND-ROUTER | Webhook (sync response) | Step 1 | Second |
| 3 | `M-LEAD-INTAKE.json` | SSS-LEAD-INTAKE | Webhook (Webflow) | Steps 1, 2 | Third |
| 4 | `M-STRIPE-DEPOSIT.json` | SSS-STRIPE-DEPOSIT | Webhook (Stripe) | Step 1 | Fourth |
| 5 | `M-BOOKING-CREATION.json` | SSS-BOOKING-CREATION | Airtable poll | Step 1 | Fifth |
| 6 | `M-CONCIERGE-ASSIGNMENT.json` | SSS-CONCIERGE-ASSIGNMENT | Airtable poll | Step 1 | Sixth |
| 7 | `M-BOOKING-CONFIRMATION.json` | SSS-BOOKING-CONFIRMATION | Airtable poll | Steps 1, 6 | Seventh |

**DO NOT import out of order. Do not activate any scenario before Step 1 is live.**

---

## STEP-BY-STEP IMPORT PROCESS

### STEP 1: Import M-OPS-LOGGER-ALERTER

```
File: blueprints/M-OPS-LOGGER-ALERTER.json
```

**Import in Make:**
1. Go to Make.com → Scenarios → Create new scenario
2. Click Import blueprint → Upload `M-OPS-LOGGER-ALERTER.json`
3. Scenario name will be `SSS-OPS-LOGGER-ALERTER`

=== MANUAL ACTION REQUIRED ===
After import — before proceeding to Step 2:

A) Rebind Airtable connection on Module 3:
   - Click Module 3 → Connection → Select your SSS Airtable PAT
   - Base: She Said Sail (appdZ49WqgjRXxA1R)
   - Table: Audit Log (tblrMpTfMk8q1eNHp)

B) Rebind Slack OAuth connection on Modules 8, 10, 12:
   - Module 8: Slack connection → Channel: #sss-emergency-ops
   - Module 10: Slack connection → Channel: #sss-lead-intake
   - Module 12: Slack connection → Channel: #sss-ops-alerts

C) Copy the webhook URL:
   - Click Module 1 (Custom Webhook) → Copy address
   - === INSERT YOUR VALUE HERE === (save this URL — you will paste it into ALL other scenarios)
   - Label it: OPS_LOGGER_ALERTER_WEBHOOK_URL

D) Save and activate the scenario (toggle to ON)

E) Test: Send a POST request to the webhook URL with:
   `{"triggering_event": "test", "environment": "Production"}`
   Verify an Audit Log record is created in Airtable.

**Verification gate: Do not proceed until test passes.**

---

### STEP 2: Import M-BRAND-ROUTER

```
File: blueprints/M-BRAND-ROUTER.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable connection on Modules 6 and 9:
   - Table: Requests (tblTlSB9CO4dTGodg)

B) In Module 12 body, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`
   with the URL copied in Step 1C

C) Copy THIS scenario's webhook URL (Module 1)
   - Label it: BRAND_ROUTER_WEBHOOK_URL

D) Activate

**Verification gate: Send `{"source_url": "https://shesaidsail.com", "request_record_id": "test"}` → response should be `{"brand": "SSS", ...}`**

---

### STEP 3: Import M-LEAD-INTAKE

```
File: blueprints/M-LEAD-INTAKE.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable connection on Modules 3 and 7 → Requests (tblTlSB9CO4dTGodg)

B) Rebind Gmail OAuth on Module 8 → hello@shesaidsail.com

C) In Module 5 body, replace:
   `PASTE_BRAND_ROUTER_WEBHOOK_URL_HERE`
   with BRAND_ROUTER_WEBHOOK_URL from Step 2C

D) In Module 9 body, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`
   with OPS_LOGGER_ALERTER_WEBHOOK_URL from Step 1C

E) Copy THIS scenario's webhook URL (Module 1)
   - Label it: LEAD_INTAKE_WEBHOOK_URL

F) Register LEAD_INTAKE_WEBHOOK_URL in Webflow:
   Webflow CMS → Site Settings → Integrations → Form Webhooks → Add webhook

G) Activate

---

### STEP 4: Import M-STRIPE-DEPOSIT

```
File: blueprints/M-STRIPE-DEPOSIT.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable on Modules 4 and 7 → Bookings (tbl72omPibBkn2hZL)

B) In Module 8 body, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`
   with OPS_LOGGER_ALERTER_WEBHOOK_URL

C) Copy THIS scenario's webhook URL (Module 1)
   - Label it: STRIPE_DEPOSIT_WEBHOOK_URL

D) === STRIPE TEST MODE REQUIRED ===
   In Stripe Dashboard (TEST mode) → Developers → Webhooks:
   - Add endpoint: paste STRIPE_DEPOSIT_WEBHOOK_URL
   - Select event: `payment_intent.succeeded` only
   - Copy signing secret to credential vault

E) Activate

---

### STEP 5: Import M-BOOKING-CREATION

```
File: blueprints/M-BOOKING-CREATION.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable on Modules 1, 3, 5, 9:
   - Module 1: Requests (tblTlSB9CO4dTGodg)
   - Modules 3, 5, 9: Bookings (tbl72omPibBkn2hZL)

B) Rebind Gmail OAuth on Module 11 → hello@shesaidsail.com

C) In Module 6 headers, replace:
   `PASTE_STRIPE_SECRET_KEY_HERE` → your Stripe TEST secret key (sk_test_...)

D) In Module 7 headers, replace:
   `PASTE_STRIPE_SECRET_KEY_HERE` → same Stripe TEST secret key

E) In Module 12 body, replace:
   `PASTE_QUO_SMS_API_KEY_HERE` → your Quo SMS API key

F) In Module 13 body, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`

G) Set Make scheduling: 15-minute polling interval

H) Activate (in TEST MODE — verify Stripe calls use sk_test_ key)

---

### STEP 6: Import M-CONCIERGE-ASSIGNMENT

```
File: blueprints/M-CONCIERGE-ASSIGNMENT.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable on Modules 1, 4, 7:
   - Module 1: Bookings (tbl72omPibBkn2hZL)
   - Module 4: Concierge_Operators (tblX61IB2qjDmac8l)
   - Module 7: Bookings (tbl72omPibBkn2hZL)

B) In Modules 8 and 10 bodies, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`

C) Set Make scheduling: 15-minute polling

D) Activate

---

### STEP 7: Import M-BOOKING-CONFIRMATION

```
File: blueprints/M-BOOKING-CONFIRMATION.json
```

=== MANUAL ACTION REQUIRED ===

A) Rebind Airtable on Modules 1, 6, 10:
   - Module 1: Bookings (tbl72omPibBkn2hZL)
   - Module 6: Clients (tblr84vRIWC5HmKvo)
   - Module 10: Bookings (tbl72omPibBkn2hZL)

B) Rebind Gmail OAuth on Module 8 → hello@shesaidsail.com

C) In Module 9 body, replace:
   `PASTE_QUO_SMS_API_KEY_HERE`

D) In Module 11 body, replace:
   `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE`

E) Set Make scheduling: 15-minute polling

F) Activate

**All 7 scenarios are now live. Proceed to TESTING_GUIDE.md.**

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — FINAL_IMPORT_ORDER.md*
