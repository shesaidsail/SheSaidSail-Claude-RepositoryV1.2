# M-BOOKING-CONFIRMATION — Scenario Specification

**Scenario ID:** M-BOOKING-CONFIRMATION
**Version:** 1.0
**Status:** Ready for Import
**Last Updated:** 2026-05-16
**Zone:** us1.make.com

---

## Overview

M-BOOKING-CONFIRMATION is the final step in the Stage 1 booking funnel. It sends branded confirmation communications to the client (email + optional SMS) when a deposit payment is confirmed. It then advances the Booking record status and fires audit and Slack notifications.

This scenario is designed to be called by M-BOOKING-CREATION immediately after a deposit is processed, but can also be triggered standalone (e.g., for manual confirmation resends, retries, or testing).

**Brand routing:** The scenario branches on `brand` to send SSS-branded or ME-branded communications from the appropriate sender address, with brand-specific tone and visual design.

**Status progression logic:**
- If `Agreement_Signed = true` on the Booking record → Status advances to `CONFIRMED`
- If `Agreement_Signed = false` AND `Total_Amount > $5,000` → Status advances to `AGREEMENT_PENDING`
- Otherwise → Status advances to `CONFIRMED`

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-BOOKING-CONFIRMATION Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | None (internal Make-to-Make calls; secure by URL obscurity) |
| Method | POST |
| Content-Type | application/json |

---

## Incoming Payload Schema

```json
{
  "booking_id": "recXXXXXXXXXXXXXX",
  "brand": "SSS | ME",
  "client_email": "client@example.com",
  "client_name": "Jane Smith",
  "client_phone": "+1-555-123-4567",
  "charter_date": "2026-08-15",
  "city": "Miami",
  "package_name": "Full Day Luxury Charter",
  "deposit_amount": 1500,
  "deposit_paid_at": "2026-05-16T14:30:00Z",
  "concierge_name": "",
  "concierge_email": "",
  "environment": "production"
}
```

| Field | Required | Notes |
|---|---|---|
| booking_id | Yes | Airtable record ID in `tbl72omPibBkn2hZL` — used to fetch full booking data |
| brand | Yes | `SSS` or `ME` — drives email/SMS template and sender address |
| client_email | Yes | Recipient for confirmation email |
| client_name | Yes | Fallback display name if Airtable record doesn't have first_name |
| client_phone | No | If present, triggers SMS. If empty, SMS module is skipped. |
| charter_date | Yes | Displayed in email subject and body |
| city | Yes | Departure city for booking summary |
| package_name | Yes | Package display name for booking summary |
| deposit_amount | Yes | Dollar amount (not cents) |
| deposit_paid_at | No | Timestamp of deposit payment |
| concierge_name | No | If empty, M-BOOKING-CONFIRMATION resolves from Airtable Booking record |
| concierge_email | No | If empty, resolved from Airtable |
| environment | No | Passed through to audit log |

> **Data priority rule:** Module 2 fetches the full Booking record from Airtable and uses those values authoritatively. Payload fields serve as fallback via `{{ifempty(2.fields.X, 1.x)}}`. This ensures the email reflects the actual booking state, not potentially stale webhook payload data.

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the POST payload from M-BOOKING-CREATION or a manual trigger. All fields available via `{{1.*}}`.

---

### Module 2 — Airtable ActionGetRecord — Fetch Full Booking
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Record ID:** `{{1.booking_id}}`
- **Purpose:** Retrieve authoritative booking data including concierge assignment, Agreement_Signed flag, Total_Amount, Balance_Due, Package_Name, and Client_First_Name.
- **Key fields used downstream:** `2.fields.Charter_Date`, `2.fields.City`, `2.fields.Package_Name`, `2.fields.Deposit_Amount`, `2.fields.Balance_Due`, `2.fields.Concierge_Name`, `2.fields.Concierge_Email`, `2.fields.Agreement_Signed`, `2.fields.Total_Amount`, `2.fields.Client_First_Name`

---

### Module 3 — Router: Brand SSS vs Brand ME

**Route 1 "SSS Confirmation"** — filter: `{{1.brand}}` = `"SSS"`

#### Module 4 — Gmail ActionSendEmail (SSS)
| Property | Value |
|---|---|
| Connection | RECONNECT_GMAIL_CONNECTION (hello@shesaidsail.com) |
| From | hello@shesaidsail.com |
| To | `{{1.client_email}}` |
| Subject | `Your She Said Sail Charter is Confirmed — {charter_date formatted}` |
| Format | HTML |
| Tone | Warm, celebratory, personal |
| Content includes | Charter details table, concierge intro, what's next steps, balance due reminder, emergency contact |

#### Module 5 — HTTP POST to Quo SMS API (SSS)
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (RECONNECT_SMS_CONNECTION)
- **Filter:** Only fires when `{{1.client_phone}}` is not empty
- **SMS body:** `"Hi {client_name}! Your SSS charter on {date} is confirmed. {concierge_name} will be in touch within 48 hours. Questions? Reply here or email hello@shesaidsail.com"`

---

**Route 2 "ME Confirmation"** — filter: `{{1.brand}}` = `"ME"`

#### Module 6 — Gmail ActionSendEmail (ME)
| Property | Value |
|---|---|
| Connection | RECONNECT_GMAIL_CONNECTION (hello@mareexecutive.com) |
| From | hello@mareexecutive.com |
| To | `{{1.client_email}}` |
| Subject | `Your Mare Executive Charter is Confirmed — {charter_date formatted}` |
| Format | HTML |
| Tone | Formal, professional, executive |
| Content includes | Charter details table, charter manager intro, next steps, balance due reminder |

#### Module 7 — HTTP POST to Quo SMS API (ME)
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (RECONNECT_SMS_CONNECTION)
- **Filter:** Only fires when `{{1.client_phone}}` is not empty
- **SMS body:** `"Dear {client_name}, your Mare Executive charter on {date} is confirmed. {concierge_name} will be in touch within 48 hours. For assistance: hello@mareexecutive.com"`

---

### Module 8 — Airtable ActionUpdateRecord — Update Booking Status
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Record ID:** `{{1.booking_id}}`

| Field | Value |
|---|---|
| Confirmation_Sent_At | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}` |
| Status | `CONFIRMED` if `Agreement_Signed = true`; `AGREEMENT_PENDING` if `Total_Amount > 5000` and `Agreement_Signed = false`; else `CONFIRMED` |

**Make expression for Status:**
```
{{if(2.fields.Agreement_Signed = true, 'CONFIRMED', if(2.fields.Total_Amount > 5000, 'AGREEMENT_PENDING', 'CONFIRMED'))}}
```

---

### Module 9 — HTTP POST to M-SLACK-ALERTS
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-SLACK-ALERTS webhook)
- **alert_type:** `BOOKING_CONFIRMED`
- **urgency:** `MEDIUM`
- **message:** `"Booking confirmed: {client_name} | {charter_date} | {city} | {package_name} | ${deposit_amount} deposit received"`

---

### Module 10 — HTTP POST to M-AUDIT-LOGGER
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER webhook)
- **event_type:** `CONFIRMATION_SENT`
- **action:** `CONFIRMATION_EMAIL_AND_SMS_SENT`
- **actor:** `Make-Autonomous`

| Audit Payload Field | Value |
|---|---|
| scenario_id | `M-BOOKING-CONFIRMATION` |
| record_id | `{{1.booking_id}}` |
| brand | `{{1.brand}}` |
| client_email | `{{1.client_email}}` |
| client_phone | `{{1.client_phone}}` |
| charter_date | `{{2.fields.Charter_Date}}` |
| new_status | Resolved status (CONFIRMED or AGREEMENT_PENDING) |
| sms_sent | `true` if client_phone was present, else `false` |

---

## Error Handling

| Module | Handler |
|---|---|
| Module 11 | HTTP POST to M-AUDIT-LOGGER with `SCENARIO_ERROR` event — attached to Make error handler route |
| Module 12 | `slack:ActionPostMessage` to `#sss-ops-alerts` — urgent error alert flagging possible undelivered confirmation |

**Critical Note:** If this scenario errors, the client may not have received their confirmation email. The Slack alert explicitly flags this and instructs manual follow-up. Booking Status may not have been advanced to CONFIRMED.

---

## Field Mappings Summary

| Source | Airtable Field | Table | Notes |
|---|---|---|---|
| `1.booking_id` | Record ID | Bookings | Used to fetch full record |
| `2.fields.Charter_Date` | Charter_Date | Bookings | Authoritative date for email subject |
| `2.fields.City` | City | Bookings | Departure city |
| `2.fields.Package_Name` | Package_Name | Bookings | Display name |
| `2.fields.Deposit_Amount` | Deposit_Amount | Bookings | Confirmed deposit |
| `2.fields.Balance_Due` | Balance_Due | Bookings | Shown in email |
| `2.fields.Concierge_Name` | Concierge_Name | Bookings | Concierge intro in email |
| `2.fields.Concierge_Email` | Concierge_Email | Bookings | Contact address in email |
| `2.fields.Agreement_Signed` | Agreement_Signed | Bookings | Drives status routing |
| `2.fields.Total_Amount` | Total_Amount | Bookings | Threshold for AGREEMENT_PENDING |
| `2.fields.Client_First_Name` | Client_First_Name | Bookings | Personal salutation |
| `now()` | Confirmation_Sent_At | Bookings | Written by module 8 |

---

## Idempotency

This scenario does not implement a hard idempotency guard. If called multiple times for the same booking:
- The client will receive duplicate emails and SMS messages.
- `Confirmation_Sent_At` will be overwritten with the latest timestamp.
- Status will be re-evaluated and re-written (should be idempotent if already CONFIRMED).

**Mitigation:** M-BOOKING-CREATION calls this scenario once per Stripe webhook. The DUPLICATE_WEBHOOK guard in M-BOOKING-CREATION prevents duplicate triggers. If manual re-sends are needed, this is acceptable behavior.

Future enhancement: add a check on `Confirmation_Sent_At` before sending — if already set, skip email/SMS and only log.

---

## Placeholders to Rebind After Import

| Placeholder | Location | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook ID | Make auto-assigns on import; copy the generated webhook URL and provide to M-BOOKING-CREATION (module 13 URL) |
| `RECONNECT_AIRTABLE_CONNECTION` | Module 2, 8 | Select the Airtable connection for base `appdZ49WqgjRXxA1R` |
| `RECONNECT_GMAIL_CONNECTION` | Modules 4, 6 | Select Gmail connection for each brand sender (hello@shesaidsail.com for SSS, hello@mareexecutive.com for ME) — these may require two separate Gmail connections |
| `RECONNECT_SLACK_CONNECTION` | Module 12 | Select the Slack workspace connection |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (modules 5, 7) | HTTP URL — Quo SMS API | Paste the Quo SMS API endpoint. Add auth headers as required by Quo (API key header). |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 9) | HTTP URL — M-SLACK-ALERTS | Paste M-SLACK-ALERTS webhook URL |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 10) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 11) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL (error handler) |

---

## Test Steps

1. Import the blueprint into Make. Copy the generated webhook URL from module 1.
2. Paste this webhook URL into M-BOOKING-CREATION module 13 (M-BOOKING-CONFIRMATION trigger URL).
3. Send the **SSS Happy Path** test payload from `M-BOOKING-CONFIRMATION.test.json`.
   - Verify: Gmail sends confirmation email from hello@shesaidsail.com.
   - Verify: SMS fires (if `client_phone` is present).
   - Verify: Booking record in Airtable updated — `Confirmation_Sent_At` set, Status = `CONFIRMED` or `AGREEMENT_PENDING`.
   - Verify: M-SLACK-ALERTS receives BOOKING_CONFIRMED alert.
   - Verify: M-AUDIT-LOGGER receives CONFIRMATION_SENT event with correct fields.
4. Send the **ME Happy Path** test payload (brand = ME).
   - Verify: Email sends from hello@mareexecutive.com with ME-branded subject and body.
5. Send the **Agreement Pending** test payload (Agreement_Signed = false, Total_Amount > 5000 on the Airtable record).
   - Verify: Booking Status updated to `AGREEMENT_PENDING`.
6. Send payload with **empty client_phone**.
   - Verify: SMS modules (5/7) do not fire. Email only.
7. Send payload with **invalid booking_id** (module 2 will fail to find record).
   - Verify: Error handler fires. Module 11 sends SCENARIO_ERROR audit. Module 12 sends Slack urgent alert.
8. Verify `ifempty` fallbacks work: temporarily clear `Concierge_Name` on the Airtable record and confirm email uses the payload fallback value.
