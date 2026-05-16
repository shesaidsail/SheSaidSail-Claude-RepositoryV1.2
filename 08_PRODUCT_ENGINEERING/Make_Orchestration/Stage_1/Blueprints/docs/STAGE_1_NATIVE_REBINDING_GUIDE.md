# Stage 1 Native Rebinding Guide
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION REFERENCE

---

## Purpose

This guide provides step-by-step rebinding instructions for every connection, webhook URL, and credential placeholder in the 8 Stage 1 blueprints. Complete every step in order. Do not activate any scenario until all connections and placeholders are resolved.

**Import order matters — follow sequence in Section 1.**

---

## Section 1 — Import Order

Import blueprints in this exact sequence. M-AUDIT-LOGGER and M-SLACK-ALERTS must be imported first so their webhook URLs are available when configuring later blueprints.

| Order | Blueprint | Reason |
|---|---|---|
| 1 | M-AUDIT-LOGGER | All others call this — get its webhook URL first |
| 2 | M-SLACK-ALERTS | M-BRAND-ROUTER and others call this |
| 3 | M-BRAND-ROUTER | Called by M-LEAD-INTAKE |
| 4 | M-LEAD-INTAKE | Depends on M-BRAND-ROUTER and M-AUDIT-LOGGER URLs |
| 5 | M-STRIPE-DEPOSIT | Standalone — Stripe webhook, Airtable, Gmail, Slack |
| 6 | M-CONCIERGE-ASSIGNMENT | Depends on M-AUDIT-LOGGER URL |
| 7 | M-BOOKING-CREATION | Depends on M-AUDIT-LOGGER URL |
| 8 | M-BOOKING-CONFIRMATION | Depends on M-AUDIT-LOGGER URL |

---

## Section 2 — Airtable Native Connection

**Placeholder:** `RECONNECT_AIRTABLE_CONNECTION`

**Used in:** All 8 blueprints (every Airtable module)

**Steps:**
1. Open any Airtable module (e.g., M-AUDIT-LOGGER module 2)
2. Click "Add a connection" or the connection dropdown
3. Select "Airtable" → "OAuth" (recommended) or "API Key"
4. If OAuth: authorize the Google/Airtable account that owns base `appdZ49WqgjRXxA1R`
5. If API Key: paste Airtable Personal Access Token from credential vault
6. Name the connection: `SSS — Airtable Production`
7. Click "Save"
8. In Make, select this connection for ALL Airtable modules across all 8 blueprints
9. Verify base `appdZ49WqgjRXxA1R` is selectable in the Base ID field

**Test:** Run M-AUDIT-LOGGER manually with a test payload. Verify a new record appears in the Audit Log table in Airtable.

---

## Section 3 — Slack Native Connection

**Placeholder:** `RECONNECT_SLACK_CONNECTION`

**Used in:** M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION

**Steps:**
1. Open any Slack module (e.g., M-SLACK-ALERTS module 3)
2. Click "Add a connection"
3. Select "Slack" → click "Sign in with Slack"
4. Authorize the She Said Sail Slack workspace
5. Name the connection: `SSS — Slack Production`
6. Select this connection for ALL Slack modules across all blueprints
7. Verify channels are accessible: `#sss-ops-alerts`, `#sss-emergency-ops`

**Will's Slack User ID (for L3/L4 DM routes in M-SLACK-ALERTS):**
1. In Slack, go to Will's profile
2. Click "More" → "Copy member ID"
3. Format: `U0XXXXXXXXX`
4. In M-SLACK-ALERTS, modules 5 and 7: replace `RECONNECT_WILL_SLACK_USER_ID` with Will's member ID
5. In Make, the "channel" field for DMs accepts a User ID directly

**Test:** Run M-SLACK-ALERTS with `{"alert_level":"L1","message_text":"Test alert","brand":"SSS","environment":"Production","idempotency_key":"TEST-001"}` and verify message appears in `#sss-ops-alerts`.

---

## Section 4 — Anthropic Claude Native Connection

**Placeholder:** `RECONNECT_CLAUDE_API_KEY`

**Used in:** M-BRAND-ROUTER (module 3), M-BOOKING-CREATION (module 7)

**Steps:**
1. Open M-BRAND-ROUTER module 3 (Anthropic Claude)
2. Click "Add a connection"
3. Select "Anthropic" → enter API key from credential vault
4. Name the connection: `SSS — Anthropic Claude Production`
5. Verify model field is set to `claude-sonnet-4-20250514`
6. Verify max_tokens is `600`
7. Verify temperature is `0.4`
8. Select this same connection for M-BOOKING-CREATION module 7

**Test:** Run M-BRAND-ROUTER with a test payload containing an inquiry clearly aligned with She Said Sail (e.g., "Looking to book a bachelorette party on a yacht in Miami"). Verify Claude returns `{"brand":"SSS","confidence":90+,"reason":"..."}`.

**Important:** If Make's native Anthropic module does not show a temperature field, it may default to 1.0. In this case, note the difference and verify with the governance owner (Will) before proceeding. Do not use HTTP fallback without Founder Decision.

---

## Section 5 — Gmail Native Connection

**Placeholder:** `RECONNECT_GMAIL_CONNECTION`

**Used in:** M-LEAD-INTAKE (module 7), M-CONCIERGE-ASSIGNMENT (module 8), M-STRIPE-DEPOSIT (module 8), M-BOOKING-CREATION (module 8), M-BOOKING-CONFIRMATION (module 8)

**Steps:**
1. Open M-LEAD-INTAKE module 7 (Gmail Send Email)
2. Click "Add a connection"
3. Select "Gmail" → Sign in with Google
4. Authorize the Google account associated with `hello@shesaidsail.com`
5. Name the connection: `SSS — Gmail hello@shesaidsail.com`
6. Select this connection for ALL Gmail modules across all blueprints
7. In each module, verify "From" field is set to `hello@shesaidsail.com`

**Pre-activation safety step:**
- Before activating any scenario that sends client emails, temporarily set the "To" field to an internal test email
- Send one test email per scenario
- Restore "To" to the dynamic field mapping after confirming delivery
- Do not activate client-facing email scenarios in production until test confirmed

**Test:** Run M-LEAD-INTAKE with a test payload using an internal email as `email`. Confirm auto-reply is received.

---

## Section 6 — Stripe Native Connection

**Placeholder:** `RECONNECT_STRIPE_CONNECTION`

**Used in:** M-CONCIERGE-ASSIGNMENT (module 6), M-BOOKING-CONFIRMATION (module 6)

**Steps:**
1. Open M-CONCIERGE-ASSIGNMENT module 6 (Stripe Create Payment Link)
2. Click "Add a connection"
3. Select "Stripe" → enter Stripe Restricted Key from credential vault
   - Key must have permissions: Payment Links (write), Products (write)
   - Do NOT use the full Secret Key — use a Restricted Key scoped to payment links only
4. Name the connection: `SSS — Stripe Production`
5. Select this same connection for M-BOOKING-CONFIRMATION module 6

**Stripe Restricted Key scope required:**
- `payment_links:write`
- `products:write`
- `prices:write`

**Test:** Run M-CONCIERGE-ASSIGNMENT in sandbox mode against a test booking record. Verify a Stripe Payment Link is created and the URL is written back to Airtable.

---

## Section 7 — Stripe Webhook Setup (M-STRIPE-DEPOSIT)

**This is separate from the Stripe connection above.**

**Steps:**
1. Import M-STRIPE-DEPOSIT blueprint into Make
2. After import, the webhook module (module 1) will generate a webhook URL
3. Copy the Make webhook URL (format: `https://hook.us1.make.com/XXXXX`)
4. Go to Stripe Dashboard → Developers → Webhooks → Add endpoint
5. Paste the Make webhook URL as the endpoint URL
6. Select events to subscribe: `payment_intent.succeeded`
7. Click "Add endpoint"
8. Copy the "Signing secret" (starts with `whsec_`)
9. Store the signing secret in Make Data Store — do NOT put in the blueprint
10. In Make, in the M-STRIPE-DEPOSIT webhook module settings, enable "Stripe-Signature" header validation if available

**Idempotency note:** Stripe retries webhooks on failure. The blueprint includes idempotency protection — it checks the Audit Log before processing each event. Do not disable this check.

---

## Section 8 — Quo SMS HTTP Module Rebinding

**Placeholder:** `RECONNECT_QUO_API_ENDPOINT` and `RECONNECT_QUO_API_KEY`

**Used in:** M-CONCIERGE-ASSIGNMENT (module 9), M-BOOKING-CONFIRMATION (module 9)

**Steps:**
1. Retrieve Quo API endpoint URL from credential vault
2. Retrieve Quo API key from credential vault
3. Open M-CONCIERGE-ASSIGNMENT module 9 (HTTP — Quo SMS)
4. Replace `RECONNECT_QUO_API_ENDPOINT` in the URL field with the actual Quo API endpoint
5. Replace `RECONNECT_QUO_API_KEY` in the Authorization header value with the actual API key
6. Repeat for M-BOOKING-CONFIRMATION module 9
7. **Recommended:** Store credentials in Make Data Store and reference via variables — do not embed directly in the HTTP module body

**If Quo is not available or unreliable:**
- Temporary manual fallback: disable SMS module in both scenarios (toggle module off in Make)
- Document that SMS sends are manual until Quo is reconnected
- Add a Slack alert to `#sss-ops-alerts` notifying Luciana to send SMS manually
- Evaluate Twilio or OpenPhone migration for Stage 2 (both have native Make modules)

**Test:** Send a test SMS to an internal phone number. Verify delivery before activating client-facing scenarios.

---

## Section 9 — Squarespace Form Webhook Setup (M-LEAD-INTAKE)

**Placeholder:** `RECONNECT_WEBHOOK_SQUARESPACE_FORM`

**Steps:**
1. Import M-LEAD-INTAKE blueprint into Make
2. After import, the webhook module (module 1) will generate a webhook URL
3. Copy the Make webhook URL
4. In Squarespace site editor: go to the intake form block
5. Click "Edit" → "Storage" tab
6. Click "Add" → "Webhook"
7. Paste the Make webhook URL
8. Save the form configuration
9. Submit a test form to verify Make receives the payload
10. Map form field names to the expected payload fields in the blueprint (names may differ by form configuration)

**Field name mapping:** Squarespace sends fields using the form's internal field names. Verify the following fields arrive correctly:
- `name` or `fullName` → lead name
- `email` → lead email
- `phone` → lead phone
- `message` or `inquiry` → inquiry text
- `date` → event date
- `guests` → guest count

If field names differ from the blueprint's expected fields, update the mapper in module 1.

---

## Section 10 — Inter-Scenario Webhook URL Binding

After importing all 8 blueprints, each HTTP module calling another scenario must be updated with the real webhook URL.

| Blueprint | Module | Placeholder | Replace With |
|---|---|---|---|
| M-LEAD-INTAKE | Module 6 | `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` | M-BRAND-ROUTER webhook URL |
| M-LEAD-INTAKE | Module 9 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-BRAND-ROUTER | Module 10 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-SLACK-ALERTS | Module 8 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-CONCIERGE-ASSIGNMENT | Module 10, 11 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-STRIPE-DEPOSIT | Module 10 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-BOOKING-CREATION | Module 11, 12 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |
| M-BOOKING-CONFIRMATION | Module 11, 12 | `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | M-AUDIT-LOGGER webhook URL |

**How to find the webhook URL:**
1. Open the target scenario in Make (e.g., M-AUDIT-LOGGER)
2. Click the webhook trigger module (module 1)
3. The webhook URL is displayed — copy it
4. Paste into the URL field of each HTTP module referencing it

---

## Section 11 — Final Pre-Activation Checklist

Before activating any scenario, verify:

- [ ] All Airtable connections bound to `SSS — Airtable Production`
- [ ] Airtable base `appdZ49WqgjRXxA1R` accessible
- [ ] All Slack connections bound to She Said Sail workspace
- [ ] Will's Slack User ID set in M-SLACK-ALERTS modules 5 and 7
- [ ] All Anthropic Claude connections bound with correct API key
- [ ] Claude model is `claude-sonnet-4-20250514` in both blueprints
- [ ] All Gmail connections bound to `hello@shesaidsail.com`
- [ ] Gmail "From" address is `hello@shesaidsail.com` in all 5 Gmail modules
- [ ] Stripe connection bound with Restricted Key
- [ ] Stripe webhook configured in Stripe Dashboard for `payment_intent.succeeded`
- [ ] Quo API endpoint and key bound in M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION
- [ ] Squarespace form webhook configured and tested
- [ ] All `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` placeholders replaced
- [ ] `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` replaced in M-LEAD-INTAKE
- [ ] Test run completed for each scenario with internal test data
- [ ] No test data targets real client email/phone
- [ ] Founder Decision recorded for production activation
- [ ] Audit Log in Airtable shows test entries from each scenario

**Activate in this order:**
1. M-AUDIT-LOGGER (activate first — all others depend on it)
2. M-SLACK-ALERTS
3. M-BRAND-ROUTER
4. M-LEAD-INTAKE
5. M-STRIPE-DEPOSIT
6. M-CONCIERGE-ASSIGNMENT
7. M-BOOKING-CREATION
8. M-BOOKING-CONFIRMATION
