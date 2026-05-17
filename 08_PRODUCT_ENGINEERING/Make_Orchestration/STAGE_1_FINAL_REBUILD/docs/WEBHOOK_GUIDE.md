# WEBHOOK GUIDE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Complete webhook URL registration and management

---

## WEBHOOK OVERVIEW

Stage 1 uses 4 webhook-triggered scenarios. Each generates a unique webhook URL in Make after import. These URLs must be:
1. Copied from Make immediately after import
2. Registered in the appropriate external system
3. Pasted into all dependent Make scenarios

---

## WEBHOOK URL TRACKING SHEET

Fill this in after importing each scenario:

| Scenario | Label | Your URL (fill in) | Registered Where |
|----------|-------|-------------------|-----------------|
| SSS-OPS-LOGGER-ALERTER | OPS_LOGGER_ALERTER_WEBHOOK_URL | `=== INSERT YOUR VALUE HERE ===` | Pasted into all other scenarios |
| SSS-BRAND-ROUTER | BRAND_ROUTER_WEBHOOK_URL | `=== INSERT YOUR VALUE HERE ===` | Pasted into M-LEAD-INTAKE Module 5 |
| SSS-LEAD-INTAKE | LEAD_INTAKE_WEBHOOK_URL | `=== INSERT YOUR VALUE HERE ===` | Registered in Webflow |
| SSS-STRIPE-DEPOSIT | STRIPE_DEPOSIT_WEBHOOK_URL | `=== INSERT YOUR VALUE HERE ===` | Registered in Stripe Dashboard |

**Copy this table to a secure document and fill it in during deployment.**

---

## HOW TO COPY A WEBHOOK URL FROM MAKE

1. Open the scenario in Make
2. Click on Module 1 (the Custom Webhook module — leftmost)
3. Click **"Copy address to clipboard"**
4. The URL format will be: `https://hook.us1.make.com/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. Store this URL in your tracking sheet immediately

---

## WEBHOOK 1: SSS-OPS-LOGGER-ALERTER

**This is the MASTER webhook — copy first, paste everywhere.**

After import and rebinding:
1. Copy webhook URL from Module 1
2. Save as: `OPS_LOGGER_ALERTER_WEBHOOK_URL`
3. Open each of the following scenarios and replace `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE` with this URL:
   - SSS-BRAND-ROUTER → Module 12 → body field
   - SSS-LEAD-INTAKE → Module 9 → url field
   - SSS-STRIPE-DEPOSIT → Module 8 → url field
   - SSS-BOOKING-CREATION → Module 13 → url field
   - SSS-CONCIERGE-ASSIGNMENT → Module 8 → url field (success branch)
   - SSS-CONCIERGE-ASSIGNMENT → Module 10 → url field (failure branch)
   - SSS-BOOKING-CONFIRMATION → Module 11 → url field

**No external system registration needed — only called by other Make scenarios.**

---

## WEBHOOK 2: SSS-BRAND-ROUTER

**Called synchronously by M-LEAD-INTAKE. Must be live before M-LEAD-INTAKE is activated.**

After import and rebinding:
1. Copy webhook URL from Module 1
2. Save as: `BRAND_ROUTER_WEBHOOK_URL`
3. Open SSS-LEAD-INTAKE → Module 5 → replace `PASTE_BRAND_ROUTER_WEBHOOK_URL_HERE` with this URL

**No external system registration needed — only called by M-LEAD-INTAKE.**

---

## WEBHOOK 3: SSS-LEAD-INTAKE

**Registered in Webflow to receive form submissions.**

=== MANUAL ACTION REQUIRED ===

After import, rebinding, and placeholder replacement:

1. Copy webhook URL from Module 1
2. Save as: `LEAD_INTAKE_WEBHOOK_URL`
3. **Register in Webflow:**
   - Log in to Webflow
   - Open the She Said Sail site
   - Go to: Site Settings → Integrations → Webhooks
   - Click Add Webhook
   - Trigger: Form Submission
   - URL: paste `LEAD_INTAKE_WEBHOOK_URL`
   - Save

=== TEST MODE ===
Test by submitting the Webflow inquiry form with test data. Verify:
- Airtable Requests record created
- Slack #sss-lead-intake receives notification
- Auto-reply email sent to test email address
- Audit Log record created

**Expected Webflow payload fields:**
```
first_name, last_name, email, phone, yacht, experience, duration,
preferred_date, guest_count, add_ons, occasion, special_requests,
source_url, form_name, city
```

---

## WEBHOOK 4: SSS-STRIPE-DEPOSIT

**Registered in Stripe to receive payment confirmations.**

=== MANUAL ACTION REQUIRED ===
=== STRIPE TEST MODE REQUIRED FOR INITIAL SETUP ===

After import and rebinding:
1. Copy webhook URL from Module 1
2. Save as: `STRIPE_DEPOSIT_WEBHOOK_URL`
3. **Register in Stripe Dashboard (TEST mode first):**
   - Log in to Stripe Dashboard
   - Switch to **TEST MODE** (toggle in top-left)
   - Go to: Developers → Webhooks
   - Click **Add endpoint**
   - Endpoint URL: paste `STRIPE_DEPOSIT_WEBHOOK_URL`
   - Events to send: select **only** `payment_intent.succeeded`
   - Click Add endpoint
   - After creation, click "Reveal" next to Signing secret
   - Copy the webhook signing secret (starts with `whsec_`)
   - **Store in your credential vault — you will need this**

4. **Test using Stripe's test tool:**
   - On the webhook endpoint page, click **Send test webhook**
   - Select event: `payment_intent.succeeded`
   - Click Send
   - Verify in Make that the scenario received and processed the event
   - Verify the Airtable Bookings record was updated

=== SWITCHING TO LIVE STRIPE WEBHOOKS ===
When ready for production:
- Switch Stripe Dashboard to LIVE mode
- Add a NEW endpoint (same URL, same event)
- Copy the new live signing secret
- Update credential vault

---

## INTERNAL WEBHOOK CALL PATTERN

Scenarios that call other scenarios via HTTP use this pattern:

```
Module type: http:ActionSendData (version 3)
Method: POST
Content-Type: application/json
URL: {webhook URL from target scenario}
Body: JSON payload
```

This is fire-and-forget — the calling scenario does not wait for a response (except M-LEAD-INTAKE → M-BRAND-ROUTER which is synchronous and reads the response).

---

## WEBHOOK SECURITY NOTE

Make webhook URLs contain a long random token and are effectively secret. However:
- Store all webhook URLs in a secure credential vault or encrypted document
- Do not commit webhook URLs to version control
- Rotate webhook URLs if they are accidentally exposed by deleting and recreating the webhook module in Make

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — WEBHOOK_GUIDE.md*
