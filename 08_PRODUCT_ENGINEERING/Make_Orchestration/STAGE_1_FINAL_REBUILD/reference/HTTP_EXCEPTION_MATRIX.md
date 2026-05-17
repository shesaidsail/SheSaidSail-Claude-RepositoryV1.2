# HTTP EXCEPTION MATRIX — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Documents all cases where HTTP (instead of native Make modules) is used, and why

---

## EXCEPTION 1: Stripe POST /v1/prices (M-BOOKING-CREATION Module 6)

**Why HTTP instead of native Stripe module:**
The native Stripe module `stripe:createPaymentLink` is deprecated and import-incompatible with Make's current blueprint importer. It does not support `price_data` in the payment_links endpoint correctly.

The correct Stripe API flow requires:
1. First create a Price object (POST /v1/prices)
2. Then create a Payment Link using the price ID (POST /v1/payment_links)

**HTTP Configuration:**
```
URL: https://api.stripe.com/v1/prices
Method: POST
Content-Type: application/x-www-form-urlencoded
Stripe-Version: 2023-10-16
Authorization: Bearer {STRIPE_SECRET_KEY}
```

**Body parameters (URL-encoded):**
```
unit_amount = {deposit_amount_cents}
currency = usd
product_data[name] = {experience} Deposit 50pct
product_data[metadata][booking_id] = {booking_id}
product_data[metadata][request_id] = {request_id}
product_data[metadata][client] = {client_name}
```

**Response fields used:**
- `{{6.data.id}}` — Stripe price ID (passed to Module 7)

---

## EXCEPTION 2: Stripe POST /v1/payment_links (M-BOOKING-CREATION Module 7)

**Why HTTP:**
Same reason as Exception 1. Continuation of the two-step Stripe payment link creation flow.

**HTTP Configuration:**
```
URL: https://api.stripe.com/v1/payment_links
Method: POST
Content-Type: application/x-www-form-urlencoded
Stripe-Version: 2023-10-16
Idempotency-Key: {idempotency_key}-paylink
Authorization: Bearer {STRIPE_SECRET_KEY}
```

**Body parameters (URL-encoded):**
```
line_items[0][price] = {price_id from Module 6}
line_items[0][quantity] = 1
metadata[booking_id] = {booking_id}
metadata[request_id] = {request_id}
metadata[client_name] = {client_name}
metadata[brand] = {brand}
after_completion[type] = redirect
after_completion[redirect][url] = https://shesaidsail.com/booking-confirmed
```

**Response fields used:**
- `{{7.data.url}}` — Stripe payment link URL (stored in Airtable, sent in email + SMS)
- `{{7.data.id}}` — Stripe payment link ID (stored in Airtable for reference)

**Idempotency:**
The `Idempotency-Key` header prevents duplicate payment links if the module retries. Value format: `BOOKING-{request_id}-{YYYYMMDD}-paylink`.

---

## EXCEPTION 3: Quo SMS API (M-BOOKING-CREATION Module 12, M-BOOKING-CONFIRMATION Module 9)

**Why HTTP:**
There is no native Quo SMS module in Make's app library. HTTP is the only option.

**HTTP Configuration:**
```
URL: https://api.quosms.com/v1/messages
Method: POST
Content-Type: application/json
Authorization: Bearer {QUO_API_KEY}
```

**handleErrors: true** — SMS failures should not block the booking workflow. If SMS fails, the scenario continues and logs the failure. Email is the primary communication channel.

---

## EXCEPTION 4: Internal Webhook Calls (Multiple Scenarios)

**Why HTTP:**
Calling one Make scenario from another requires HTTP POST to the target webhook URL. Make has no native module for scenario-to-scenario calls.

**Affected modules:**
- M-BRAND-ROUTER Module 12 → OPS-LOGGER-ALERTER
- M-LEAD-INTAKE Module 5 → BRAND-ROUTER (synchronous)
- M-LEAD-INTAKE Module 9 → OPS-LOGGER-ALERTER
- M-STRIPE-DEPOSIT Module 8 → OPS-LOGGER-ALERTER
- M-BOOKING-CREATION Module 13 → OPS-LOGGER-ALERTER
- M-CONCIERGE-ASSIGNMENT Modules 8, 10 → OPS-LOGGER-ALERTER
- M-BOOKING-CONFIRMATION Module 11 → OPS-LOGGER-ALERTER

**HTTP Configuration (all internal calls):**
```
Method: POST
Content-Type: application/json
handleErrors: false
```

**Pattern:** Fire-and-forget for OPS-LOGGER-ALERTER calls. Synchronous with response parsing for BRAND-ROUTER call (M-LEAD-INTAKE Module 5).

---

## EXCEPTION SUMMARY

| Exception | Scenario | Modules | Justification | handleErrors |
|-----------|----------|---------|---------------|-------------|
| Stripe Price API | M-BOOKING-CREATION | 6 | No working native Stripe payment link module | false (retry on failure) |
| Stripe Payment Links API | M-BOOKING-CREATION | 7 | Two-step Stripe flow required | false (retry on failure) |
| Quo SMS API | M-BOOKING-CREATION | 12 | No native Quo SMS in Make | true (non-blocking) |
| Quo SMS API | M-BOOKING-CONFIRMATION | 9 | No native Quo SMS in Make | true (non-blocking) |
| Internal webhook calls | Multiple | Various | Make has no native scenario-to-scenario module | false |

---

## STRIPE API NOTES

**Stripe API version:** `2023-10-16` (pinned in all Stripe HTTP calls via `Stripe-Version` header)

**Authentication:** Bearer token in Authorization header
- TEST mode: `sk_test_...`
- LIVE mode: `sk_live_...`

**Idempotency handling:**
- Module 7 (payment_links) uses `Idempotency-Key` header
- Module 6 (prices) does not have idempotency header — multiple runs may create duplicate price objects (harmless, one is used per booking)
- The idempotency check at the booking level (Module 3-4) prevents duplicate bookings, which prevents duplicate Stripe calls in normal operation

**Error response format (from Stripe):**
If Stripe returns a 4xx/5xx error, `{{6.data.error.message}}` contains the error description. With `handleErrors: false`, the scenario will fail and Make will log the error in the scenario history.

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — HTTP_EXCEPTION_MATRIX.md*
