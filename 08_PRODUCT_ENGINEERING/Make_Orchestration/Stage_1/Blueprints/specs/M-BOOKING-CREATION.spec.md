# M-BOOKING-CREATION — Scenario Specification

**Scenario ID:** M-BOOKING-CREATION
**Version:** 1.1
**Status:** Ready for Import
**Last Updated:** 2026-05-16
**Zone:** us1.make.com

---

## Overview

M-BOOKING-CREATION is triggered by a Stripe `payment_intent.succeeded` webhook when a deposit payment succeeds. It is the bridge between Stripe payment confirmation and the Airtable Bookings record lifecycle. The scenario validates the environment, guards against duplicate webhook delivery (idempotency), looks up the related Request and Client records, and either creates a new Booking record or updates an existing one. It then updates the originating Request status and fires downstream calls to M-BOOKING-CONFIRMATION, M-AUDIT-LOGGER, and M-SLACK-ALERTS.

This scenario handles both code paths:
- **Create path:** No `booking_id` in Stripe metadata — a new Booking record is created.
- **Update path:** `booking_id` present in Stripe metadata — an existing pre-created Booking record is updated with payment data.

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-BOOKING-CREATION Stripe Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | Stripe webhook signature (see notes below) |
| Method | POST |
| Content-Type | application/json |

**Stripe Signature Note:** Make's raw `gateway:CustomWebHook` does not natively validate the Stripe-Signature header. After import, choose one of:
1. Switch module 1 to `stripe:TriggerNewEvent` (native Stripe trigger with built-in signature verification) and reconnect the Stripe connection.
2. Add a downstream HTTP validation step calling a validation Lambda/function with the raw body and `Stripe-Signature` header.
3. Accept URL-obscurity security for internal/low-risk environments.

---

## Incoming Stripe Webhook Payload Schema

```json
{
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_stripe_payment_intent_id",
      "amount": 150000,
      "currency": "usd",
      "metadata": {
        "booking_id": "recXXXXXXXXXXXXXX",
        "brand": "SSS",
        "environment": "production",
        "type": "deposit"
      },
      "customer_details": {
        "email": "client@example.com"
      }
    }
  }
}
```

| Field | Path | Notes |
|---|---|---|
| Stripe Payment Intent ID | `data.object.id` | Used as idempotency key |
| Amount (cents) | `data.object.amount` | Divide by 100 for USD |
| Booking Record ID | `data.object.metadata.booking_id` | Empty = create path; present = update path |
| Brand | `data.object.metadata.brand` | `SSS` or `ME` |
| Environment | `data.object.metadata.environment` | `production`, `sandbox`, or empty |
| Client Email | `data.object.customer_details.email` | Used to look up Request and Client |

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the raw Stripe POST payload. All fields accessible via `{{1.*}}` references.

---

### Module 2 — Router: Sandbox Guard vs Production

**Route 1 "Sandbox Guard"** — filter: `{{1.data.object.metadata.environment}}` = `"sandbox"`

#### Module 3 — HTTP POST to M-AUDIT-LOGGER
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER)
- **event_type:** `SANDBOX_WEBHOOK_RECEIVED`
- **action:** `SANDBOX_GUARD_BLOCKED`
- Flow terminates after this module. No booking record is created.

**Route 2 "Production"** — filter: environment = `"production"` OR empty

---

### Module 4 — Airtable SearchRecords — Idempotency Check
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Formula:** `AND({Stripe_Payment_Intent_ID} = '{{1.data.object.id}}', NOT({Status} = 'VOID'))`
- **Max Records:** 1
- **Purpose:** Detect if this Payment Intent ID was already processed (Stripe retry scenario).

---

### Module 5 — Router: Already Processed vs New Payment

**Route A "Already Processed"** — filter: `{{length(4.records)}}` > 0

#### Module 6 — HTTP POST to M-AUDIT-LOGGER
- **event_type:** `DUPLICATE_WEBHOOK`
- **action:** `DUPLICATE_STRIPE_WEBHOOK_SKIPPED`
- Flow terminates. No changes made to existing booking.

**Route B "New Payment"** — filter: `{{length(4.records)}}` = 0

---

### Module 7 — Airtable SearchRecords — Find Request
- **Table:** Requests (`tblTlSB9CO4dTGodg`)
- **Formula:** `OR(RECORD_ID() = '{{1.data.object.metadata.booking_id}}', {Email} = '{{1.data.object.customer_details.email}}')`
- **Sort:** Created_At descending (most recent first)
- **Max Records:** 1
- **Fields fetched:** Email, Status, First_Name, Last_Name, City, Charter_Date, Package_Interest, Brand, Party_Size, Budget_Range

### Module 8 — Airtable SearchRecords — Find Client
- **Table:** Clients (`tblr84vRIWC5HmKvo`)
- **Formula:** `AND({Email} = '{{1.data.object.customer_details.email}}')`
- **Max Records:** 1
- **Fields fetched:** Email, First_Name, Last_Name, Phone, Brand

---

### Module 9 — Router: Booking Exists vs Create Booking

**Route "Booking Exists — Update"** — filter: `{{1.data.object.metadata.booking_id}}` ≠ empty

#### Module 10 — Airtable ActionUpdateRecord — Update Booking
- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Record ID:** `{{1.data.object.metadata.booking_id}}`

| Field | Value |
|---|---|
| Status | `DEPOSIT_PAID` |
| Deposit_Paid_At | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}` |
| Stripe_Payment_Intent_ID | `{{1.data.object.id}}` |
| Stripe_Amount_Received | `{{divide(1.data.object.amount, 100)}}` |
| Environment | `{{1.data.object.metadata.environment}}` |

**Route "Create Booking"** — filter: `{{1.data.object.metadata.booking_id}}` = empty

#### Module 11 — Airtable ActionCreateRecord — Create Booking
- **Table:** Bookings (`tbl72omPibBkn2hZL`)

| Field | Value |
|---|---|
| Status | `DEPOSIT_PAID` |
| Brand | `{{1.data.object.metadata.brand}}` |
| Client_ID | `[{{first(8.records).id}}]` (linked record array) |
| Request_ID | `[{{first(7.records).id}}]` (linked record array) |
| City | `{{first(7.records).fields.City}}` |
| Charter_Date | `{{first(7.records).fields.Charter_Date}}` |
| Package_ID | `{{first(7.records).fields.Package_Interest}}` |
| Deposit_Amount | `{{divide(1.data.object.amount, 100)}}` |
| Deposit_Paid_At | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}` |
| Stripe_Payment_Intent_ID | `{{1.data.object.id}}` |
| Stripe_Amount_Received | `{{divide(1.data.object.amount, 100)}}` |
| Environment | `{{1.data.object.metadata.environment}}` |
| Source_System | `Stripe` |
| Created_At | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}` |

> **Note:** `Booking_ID` is a formula field auto-generated by Airtable. `Client_ID` and `Request_ID` must be passed as single-element JSON arrays (linked record format).

---

### Module 12 — Airtable ActionUpdateRecord — Update Request
- **Table:** Requests (`tblTlSB9CO4dTGodg`)
- **Record ID:** `{{first(7.records).id}}`

| Field | Value |
|---|---|
| Status | `DEPOSIT_PAID` |
| Linked_Booking_ID | `[{{ifempty(1.data.object.metadata.booking_id, ifempty(11.id, 10.id))}}]` |
| Updated_At | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}` |

**Booking ID Resolution Logic:**
1. Use `metadata.booking_id` if present (update path — module 10 ran)
2. Fall back to `11.id` (create path — module 11 ran)
3. Fall back to `10.id` (should not occur; safety fallback)

---

### Module 13 — HTTP POST to M-BOOKING-CONFIRMATION
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-BOOKING-CONFIRMATION webhook)

| Payload Field | Value |
|---|---|
| booking_id | Resolved booking record ID |
| brand | `{{1.data.object.metadata.brand}}` |
| client_email | `{{1.data.object.customer_details.email}}` |
| client_name | `{{first(7.records).fields.First_Name}} {{first(7.records).fields.Last_Name}}` |
| client_phone | `{{first(8.records).fields.Phone}}` |
| charter_date | `{{first(7.records).fields.Charter_Date}}` |
| city | `{{first(7.records).fields.City}}` |
| package_name | `{{first(7.records).fields.Package_Interest}}` |
| deposit_amount | Amount in dollars |
| deposit_paid_at | Current timestamp |
| concierge_name | Empty (M-BOOKING-CONFIRMATION resolves from Airtable) |
| concierge_email | Empty (M-BOOKING-CONFIRMATION resolves from Airtable) |
| environment | `{{1.data.object.metadata.environment}}` |

### Module 14 — HTTP POST to M-AUDIT-LOGGER
- **event_type:** `BOOKING_CREATED` or `BOOKING_UPDATED` (conditional on whether booking_id was in metadata)
- **action:** `DEPOSIT_PAYMENT_PROCESSED`
- **Includes:** idempotency_key, stripe_payment_intent_id, amount_received, client_email, request_id

### Module 15 — HTTP POST to M-SLACK-ALERTS
- **alert_type:** `BOOKING_CREATED`
- **urgency:** `HIGH`
- **message:** Full booking summary including client name, city, charter date, deposit amount

---

## Error Handling

| Module | Handler |
|---|---|
| Module 16 | HTTP POST to M-AUDIT-LOGGER with `SCENARIO_ERROR` event — attached to Make error handler route |
| Module 17 | `slack:ActionPostMessage` to `#sss-ops-alerts` — urgent error alert with Stripe Payment Intent ID and instruction to verify manually |

**Configuration:** In Make scenario settings > Error handling, attach modules 16–17 to the error handler. With `maxErrors: 3` and `autoCommit: true`, Make will retry up to 3 times before triggering the error handler.

**Critical Note:** A deposit may have been received by Stripe even if this scenario errors. Always verify the Stripe payment and create/update the booking manually if the scenario fails.

---

## Idempotency Logic

| Guard | Mechanism | Result on Duplicate |
|---|---|---|
| Stripe webhook retry | Module 4 searches Bookings by `Stripe_Payment_Intent_ID` | If found → Route A → log `DUPLICATE_WEBHOOK` → stop |
| Sandbox environment | Module 2 router checks `metadata.environment = "sandbox"` | If sandbox → Route 1 → log `SANDBOX_WEBHOOK_RECEIVED` → stop |

---

## Field Mappings Summary

| Stripe Field | Airtable Field | Table |
|---|---|---|
| `data.object.id` | Stripe_Payment_Intent_ID | Bookings |
| `data.object.amount / 100` | Deposit_Amount, Stripe_Amount_Received | Bookings |
| `data.object.metadata.brand` | Brand | Bookings |
| `data.object.metadata.environment` | Environment | Bookings |
| `data.object.customer_details.email` | Client_Email (lookup key) | Bookings |
| `data.object.metadata.booking_id` | Record ID (update path) | Bookings |
| `first(7.records).id` | Request_ID (linked record) | Bookings |
| `first(8.records).id` | Client_ID (linked record) | Bookings |
| `first(7.records).fields.City` | City | Bookings |
| `first(7.records).fields.Charter_Date` | Charter_Date | Bookings |
| `"Stripe"` (hardcoded) | Source_System | Bookings |
| `"DEPOSIT_PAID"` (hardcoded) | Status | Bookings, Requests |

---

## Placeholders to Rebind After Import

| Placeholder | Location | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook ID | Make auto-assigns on import; copy the generated webhook URL and provide to Stripe |
| `RECONNECT_AIRTABLE_CONNECTION` | Modules 4, 7, 8, 10/11, 12 | Select or create the Airtable connection for base `appdZ49WqgjRXxA1R` |
| `RECONNECT_SLACK_CONNECTION` | Module 17 | Select the Slack workspace connection |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 3) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL (sandbox guard audit) |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 6) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL (duplicate webhook audit) |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 13) | HTTP URL — M-BOOKING-CONFIRMATION | Paste M-BOOKING-CONFIRMATION webhook URL |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 14) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL (booking created/updated audit) |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 15) | HTTP URL — M-SLACK-ALERTS | Paste M-SLACK-ALERTS webhook URL |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 16) | HTTP URL — M-AUDIT-LOGGER | Paste M-AUDIT-LOGGER webhook URL (error handler audit) |

---

## Test Steps

1. Import the blueprint into Make. Copy the generated webhook URL from module 1.
2. In Stripe Dashboard: add the webhook URL as a new endpoint, subscribe to `payment_intent.succeeded`, and copy the signing secret.
3. Send the **Happy Path — Create Booking** test payload from `M-BOOKING-CREATION.test.json` (no `booking_id` in metadata).
   - Verify: new Booking record created in Airtable `tbl72omPibBkn2hZL` with Status=DEPOSIT_PAID.
   - Verify: originating Request record updated with Status=DEPOSIT_PAID and Linked_Booking_ID.
   - Verify: M-BOOKING-CONFIRMATION webhook receives the trigger payload.
   - Verify: M-AUDIT-LOGGER receives BOOKING_CREATED event.
   - Verify: M-SLACK-ALERTS receives BOOKING_CREATED alert with urgency=HIGH.
4. Resend the **same payload** (Stripe retry simulation).
   - Verify: No new Booking record created. Route A fires. M-AUDIT-LOGGER receives DUPLICATE_WEBHOOK event.
5. Send the **Update Path** test payload (with `booking_id` in metadata pointing to an existing record).
   - Verify: Existing Booking record updated (Status=DEPOSIT_PAID, Stripe_Payment_Intent_ID, etc.).
   - Verify: M-AUDIT-LOGGER receives BOOKING_UPDATED event.
6. Send the **Sandbox Guard** test payload (environment=sandbox).
   - Verify: No Booking record created or modified. M-AUDIT-LOGGER receives SANDBOX_WEBHOOK_RECEIVED event.
7. Test error path: temporarily break the Airtable connection, send a production payload.
   - Verify: Module 16 fires audit log. Module 17 sends Slack alert to `#sss-ops-alerts`.
8. Verify the `first(7.records)` and `first(8.records)` references correctly resolve when the Request and Client records exist.
