# M-STRIPE-DEPOSIT — Scenario Specification

**Scenario ID:** M-STRIPE-DEPOSIT  
**Version:** 1.0  
**Status:** Ready for Import  
**Last Updated:** 2026-05-16  
**Zone:** us1.make.com  
**Airtable Base:** appdZ49WqgjRXxA1R  

---

## Overview

M-STRIPE-DEPOSIT handles deposit collection for confirmed charter bookings. When a Booking reaches `DEPOSIT_READY` status (concierge assigned, availability confirmed, client details verified), this scenario fires. It fetches the Booking and Package records from Airtable, creates a Stripe Payment Link for the deposit amount, writes the link back to the Booking record, and delivers the deposit request to the client via both email (Gmail) and SMS (Quo SMS). All activity is logged to M-AUDIT-LOGGER and confirmed in M-SLACK-ALERTS. Error handling captures Stripe failures specifically, since a failed payment link creation must never silently pass.

**Upstream trigger:** Another Make scenario or Airtable automation POSTs to this webhook when `Booking.Status = DEPOSIT_READY`.

**External services called:** Stripe API (payment link creation), Gmail (client email), Quo SMS API (client SMS).

**Downstream scenarios called:** M-AUDIT-LOGGER (module 8), M-SLACK-ALERTS (module 9).

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-STRIPE-DEPOSIT Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | None (internal Make-to-Make calls; secured by URL obscurity) |
| Method | POST |
| Content-Type | application/json |

---

## Incoming Payload Schema

```json
{
  "booking_id": "string — Airtable Record ID from Bookings table (e.g. recXXXXXXXXXXXXXX)",
  "brand": "string — SSS | MARE_EXECUTIVE",
  "client_email": "string — client's email address for deposit email",
  "client_phone": "string — client's phone number in E.164 format (e.g. +13055550123)",
  "client_name": "string — client's full name",
  "deposit_amount_cents": "integer — deposit amount in US cents (e.g. 50000 = $500.00)",
  "charter_date": "string — charter date (e.g. 2026-07-04 or July 4, 2026)",
  "city": "string — MIA | TPA | CHS",
  "package_name": "string — exact name matching a Packages table record",
  "environment": "string — production | staging | development"
}
```

All fields are required. `deposit_amount_cents` must be an integer (not a string). Stripe will reject amounts below 50 cents.

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the POST payload. All fields available downstream via `{{1.*}}`.

### Module 2 — Airtable ActionGetRecord (`airtable:ActionGetRecord`)
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Record ID:** `{{1.booking_id}}`
- **Purpose:** Fetches the full Booking record for state verification and access to any fields not in the webhook payload. Downstream references: `{{2.fields.*}}`.

### Module 3 — Airtable SearchRecords (`airtable:SearchRecords`)
- **Table:** Packages (`tblwDw2hkKW5moSr9`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Filter formula:** `AND({Package_Name} = '{{1.package_name}}')`
- **Max records:** 1
- **Fields returned:** Package_Name, Description, Price, Duration_Hours, Brand, City
- **Purpose:** Retrieve package description and details for the Stripe product description and email body. Accessed as `{{first(3.records).fields.*}}`.

### Module 4 — HTTP POST to Stripe API (`http:ActionSendData`)
- **URL:** `https://api.stripe.com/v1/payment_links`
- **Method:** POST
- **Content-Type:** `application/x-www-form-urlencoded`
- **Connection:** RECONNECT_STRIPE_CONNECTION
- **handleErrors:** `true` (Stripe errors must surface to the error handler — do not swallow silently)
- **parseResponse:** `true` (response body parsed as JSON; fields accessible as `{{4.*}}`)

**Key request body parameters:**

| Parameter | Value |
|---|---|
| `line_items[0][price_data][currency]` | `usd` |
| `line_items[0][price_data][unit_amount]` | `{{1.deposit_amount_cents}}` (integer cents) |
| `line_items[0][price_data][product_data][name]` | `Deposit — {package_name} \| {charter_date} \| {brand}` |
| `line_items[0][price_data][product_data][description]` | Charter deposit for `{client_name}` — `{Package.Description}` |
| `line_items[0][quantity]` | `1` |
| `after_completion[type]` | `redirect` |
| `after_completion[redirect][url]` | `https://shesaidsail.com/booking-confirmed` |
| `metadata[booking_id]` | `{{1.booking_id}}` |
| `metadata[brand]` | `{{1.brand}}` |
| `metadata[environment]` | `{{1.environment}}` |
| `metadata[type]` | `deposit` |
| `metadata[client_name]` | `{{1.client_name}}` |
| `metadata[charter_date]` | `{{1.charter_date}}` |

**Response fields used downstream:**
- `{{4.id}}` — Stripe Payment Link ID (e.g. `plink_1ABC...`)
- `{{4.url}}` — Shareable payment URL (e.g. `https://buy.stripe.com/...`)

### Module 5 — Airtable ActionUpdateRecord (`airtable:ActionUpdateRecord`)
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Record ID:** `{{1.booking_id}}`

| Airtable Field | Value |
|---|---|
| `Deposit_Link` | `{{4.url}}` — Stripe payment link URL |
| `Stripe_Payment_Link_ID` | `{{4.id}}` — Stripe link object ID |
| `Status` | `DEPOSIT_SENT` (hardcoded) |
| `Deposit_Sent_At` | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}` |
| `Deposit_Amount` | `{{1.deposit_amount_cents / 100}}` — dollar value (numeric) |

### Module 6 — Gmail ActionSendEmail (`gmail:ActionSendEmail`)
- **To:** `{{1.client_email}}`
- **Subject:** `Your {brand} Charter Deposit Link — {charter_date}`
- **Body type:** HTML
- **Connection:** RECONNECT_GMAIL_CONNECTION
- **Content includes:** Client name, package name, charter date, city, brand, deposit amount ($), branded CTA button linking to `{{4.url}}`, fallback plain-text URL, and instructions about the remaining balance.

### Module 7 — HTTP POST to Quo SMS API (`http:ActionSendData`)
- **URL:** `https://api.quosms.com/v1/messages` (placeholder — confirm production endpoint)
- **Method:** POST
- **Content-Type:** `application/json`
- **Authorization:** `Bearer RECONNECT_SMS_CONNECTION` (replace token after import)
- **handleErrors:** `false` (SMS failure is non-critical — does not block audit/Slack steps)
- **SMS body:** `Hi {client_name}, your {brand} charter deposit of ${amount} for {charter_date} is ready. Pay securely here: {4.url} — Reply STOP to unsubscribe.`

### Module 8 — HTTP POST to M-AUDIT-LOGGER (`http:ActionSendData`)
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER webhook)
- **event_type:** `DEPOSIT_LINK_SENT`
- **Payload includes:** client_name, client_email, client_phone, charter_date, package_name, city, deposit_amount_cents, deposit_amount_dollars, stripe_payment_link_id (`{{4.id}}`), stripe_payment_link_url (`{{4.url}}`)
- **idempotency_key:** `M-STRIPE-DEPOSIT-{booking_id}-{YYYYMMDDHHmmss}`

### Module 9 — HTTP POST to M-SLACK-ALERTS (`http:ActionSendData`)
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-SLACK-ALERTS webhook)
- **alert_type:** `STRIPE_LINK_SENT`
- **urgency:** `LOW`
- **message:** `"Deposit link sent to {client_name} for {charter_date} - ${deposit_amount}"`
- **metadata:** booking_id, client_name, client_email, charter_date, package_name, city, deposit_amount_cents, stripe_link_id, stripe_link_url, environment

---

### Modules 10–11 — Error Handler
Fire only when `{{error}}` is non-empty (upstream module failure).

**Module 10 — HTTP POST to M-AUDIT-LOGGER**
- **event_type:** `SCENARIO_ERROR`
- **payload:** error_message, error_module, client_name, client_email, charter_date, package_name, deposit_amount_cents
- **idempotency_key:** `M-STRIPE-DEPOSIT-ERR-{booking_id}-{YYYYMMDDHHmmss}`

**Module 11 — Slack ActionPostMessage (`slack:ActionPostMessage`)**
- **Channel:** `#sss-ops-alerts`
- **Text:** Formatted error alert with brand, booking_id, client name and email, charter_date, package, deposit amount, error details, environment. Includes a warning note that the Stripe payment link may not have been created and manual follow-up is required.
- **Connection:** RECONNECT_SLACK_CONNECTION

---

## Field Mappings Summary

| Source | Destination | Module |
|---|---|---|
| `{{1.booking_id}}` | Airtable GetRecord ID | 2 |
| `{{1.package_name}}` | Airtable SearchRecords filter | 3 |
| `{{1.deposit_amount_cents}}` | Stripe `unit_amount` | 4 |
| `{{1.brand}}`, `{{1.charter_date}}`, `{{1.package_name}}` | Stripe product name | 4 |
| `{{1.booking_id}}`, `{{1.brand}}`, `{{1.environment}}` | Stripe metadata | 4 |
| `{{4.url}}` | Airtable `Deposit_Link` | 5 |
| `{{4.id}}` | Airtable `Stripe_Payment_Link_ID` | 5 |
| `DEPOSIT_SENT` | Airtable `Status` | 5 |
| `now()` formatted | Airtable `Deposit_Sent_At` | 5 |
| `{{1.deposit_amount_cents / 100}}` | Airtable `Deposit_Amount` | 5 |
| `{{1.client_email}}` | Gmail `to` | 6 |
| `{{4.url}}` | Gmail body payment link | 6 |
| `{{1.client_phone}}` | SMS `to` | 7 |
| `{{4.url}}` | SMS body deposit link | 7 |

---

## Error Handling

| Failure Point | Behavior |
|---|---|
| Module 2 (Airtable Get Booking) fails | Error handler fires (modules 10–11). Stripe link NOT created. Manual follow-up required. |
| Module 3 (Airtable Search Package) fails | Error handler fires. Stripe link NOT created. |
| Module 4 (Stripe API) fails | `handleErrors: true` — error surfaces. Error handler fires. Booking NOT updated. Email/SMS NOT sent. This is the most critical failure point. |
| Module 5 (Airtable Update) fails | Error handler fires. Stripe link WAS created but not recorded in Airtable. Ops must manually retrieve link from Stripe dashboard by `booking_id` metadata and update the Booking record. |
| Module 6 (Gmail) fails | `handleErrors: false` on HTTP calls within Gmail module — but Gmail `ActionSendEmail` errors bubble. Stripe link IS created but client not notified. |
| Module 7 (SMS) fails | `handleErrors: false` — non-critical. SMS failure does not interrupt audit/Slack. Email is the primary notification channel. |
| Modules 8–9 (Audit/Slack) fail | `handleErrors: false` — non-critical. Core deposit flow already complete. |

**Critical note on Stripe partial failure (module 5 fails after module 4 succeeds):** The Stripe link exists in Stripe's system but the Airtable `Deposit_Link` field will be blank. The error handler alert includes the booking_id. Ops must search Stripe dashboard by `metadata.booking_id` to retrieve the link URL and manually update the Booking record.

---

## Idempotency Logic

This scenario does not include an explicit idempotency check on the Booking record before creating the Stripe link. The upstream caller is responsible for gating the trigger (only fire when `Status = DEPOSIT_READY` and `Deposit_Link` is empty).

**Risk:** If the same `booking_id` is received twice, a second Stripe Payment Link will be created. To prevent this:
1. The Airtable automation that triggers this webhook should check that `Deposit_Link` is empty before firing.
2. **Future enhancement:** Add module 2a that reads `{{2.fields.Deposit_Link}}` — if non-empty, halt execution with a `builtin:SetVariable` + Router gate before calling Stripe.

The audit log idempotency key (`M-STRIPE-DEPOSIT-{booking_id}-{YYYYMMDDHHmmss}`) is unique per execution. Duplicate runs will generate separate audit records with different timestamps, making double-charges traceable.

---

## Placeholders to Rebind After Import

| Placeholder | Location | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook ID | Make auto-assigns on import. Copy URL and share with upstream scenario team. |
| `RECONNECT_AIRTABLE_CONNECTION` | Modules 2, 3, 5 | Select the Airtable OAuth connection for base `appdZ49WqgjRXxA1R`. |
| `RECONNECT_STRIPE_CONNECTION` | Module 4 — connection parameter | Select the Stripe OAuth connection (requires Stripe API key with Payment Links write scope). |
| `RECONNECT_GMAIL_CONNECTION` | Module 6 | Select the Gmail OAuth connection for the She Said Sail ops email account. |
| `RECONNECT_SMS_CONNECTION` | Module 7 — Authorization header | Replace the Bearer token value with the actual Quo SMS API key/token. |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×2) | Modules 8, 10 | Paste the live M-AUDIT-LOGGER webhook URL. |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×1) | Module 9 | Paste the live M-SLACK-ALERTS webhook URL. |
| `https://api.quosms.com/v1/messages` | Module 7 — URL | Confirm the Quo SMS production endpoint URL. Replace if different. |

---

## Test Steps

1. Deploy scenario in Make, set to ON, copy the generated webhook URL.
2. Ensure M-AUDIT-LOGGER and M-SLACK-ALERTS are ON. Have Stripe in test mode (use test API key in connection).
3. Ensure the Bookings record `recBK0001` exists in Airtable with `Status = DEPOSIT_READY` and `Deposit_Link` empty.
4. Ensure a Packages record exists with `Package_Name = "Sunset Sail — Miami"`.
5. **Test A — Happy Path:**
   - POST `M-STRIPE-DEPOSIT.test.json` to the webhook URL.
   - Verify: Stripe test dashboard shows a new Payment Link created with metadata `booking_id=recBK0001`, `type=deposit`.
   - Verify: Bookings record `recBK0001` shows `Status=DEPOSIT_SENT`, `Deposit_Link` = Stripe URL, `Deposit_Amount=500.00`, `Deposit_Sent_At` timestamp set.
   - Verify: Gmail sends deposit email to `jessica.chen@email.com` with embedded Stripe link.
   - Verify: SMS sent to `+13055550101` (check Quo SMS logs).
   - Verify: M-AUDIT-LOGGER receives `DEPOSIT_LINK_SENT` event with correct `stripe_payment_link_url`.
   - Verify: M-SLACK-ALERTS receives `STRIPE_LINK_SENT` alert (LOW urgency) in `#sss-ops-alerts`.
6. **Test B — Stripe API Error (simulate):**
   - Temporarily use an invalid Stripe API key in the connection, or send `deposit_amount_cents: 10` (below Stripe's 50-cent minimum).
   - POST the payload.
   - Verify: Error handler fires — Slack `#sss-ops-alerts` receives error alert with "Stripe payment link may NOT have been created" note.
   - Verify: M-AUDIT-LOGGER receives `SCENARIO_ERROR` event.
   - Verify: Airtable Booking record is NOT updated (Status remains `DEPOSIT_READY`).
7. **Test C — Invalid Booking ID:**
   - POST a payload with `booking_id: "recINVALID"`.
   - Verify: Module 2 fails, error handler fires, Slack alert posted.
8. **Test D — Mare Executive brand:**
   - POST payload with `brand: "MARE_EXECUTIVE"` and a valid MARE_EXECUTIVE booking ID.
   - Verify: Stripe product name includes `MARE_EXECUTIVE`.
   - Verify: Email subject reads `Your MARE_EXECUTIVE Charter Deposit Link — ...`.
9. **Test E — Duplicate trigger guard:**
   - Re-send the same Test A payload after the Booking already has `Deposit_Link` set.
   - Verify (manually, until idempotency guard module is added): A second Stripe link is created. Document this as a known gap for the idempotency enhancement.
10. After all tests, switch Stripe connection to production API key and update SMS connection before going live.
