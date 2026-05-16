# M-STRIPE-DEPOSIT — Make.com Scenario Build Specification

**Document Version:** 1.0
**Status:** PENDING BUILD
**Last Updated:** 2026-05-16
**Author:** Systems Architecture
**Pipeline Stage:** Stage 1 — Lead Intake
**Execution Order:** Fourth scenario in Stage 1 pipeline (after M-CONCIERGE-ASSIGNMENT, before M-BOOKING-CREATION)

---

## CRITICAL STAGE 1 SAFETY RULES

> Read before building. Violations of these rules create real financial or operational risk.

1. **TEST MODE ONLY:** This scenario uses Stripe's TEST API key (`sk_test_...`). No real charges are created. Do not substitute the live key (`sk_live_...`) until Stage 2 production validation is complete.
2. **NO CLIENT EMAIL/SMS:** In Stage 1, the Stripe deposit link is NOT automatically sent to the client. The link is posted to `#sss-ops-alerts` in Slack for Luciana to review and forward manually. Any module that sends the link directly to a client email or phone number is a build error.
3. **NO STRIPE WEBHOOK:** The Stripe webhook that confirms payment success is NOT registered in Stage 1. Do not register a Stripe webhook endpoint until sandbox payment tests pass and Stage 2 begins.
4. **ENVIRONMENT GUARD:** Every execution must check `{{1.environment}}` and refuse to process if it is not `"sandbox"` in Stage 1.

---

## 1. Scenario Name

`M-STRIPE-DEPOSIT`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references in M-CONCIERGE-ASSIGNMENT (caller) and M-BOOKING-CREATION (downstream). This ID is required for the Audit Log `Triggered_By_Scenario` field.

---

## 3. Trigger Type

**Primary Trigger:** HTTP webhook called by M-CONCIERGE-ASSIGNMENT after successful concierge assignment. M-CONCIERGE-ASSIGNMENT passes the Airtable Request Record ID and context in the webhook payload.

**Secondary Trigger (Manual Re-trigger):** When M-CONCIERGE-ASSIGNMENT Route B fires (no concierge found), Luciana completes manual assignment and must manually trigger this scenario. This is done by posting the webhook payload via a simple Postman or curl command. A Make "Run Once" execution with a manual payload is also acceptable in Stage 1.

**Future Trigger (Stage 2):** Airtable Watch on Requests table when `Agent_Status` changes to `"READY_FOR_DEPOSIT"` — not implemented in Stage 1.

**Webhook Configuration:**

| Parameter           | Value                                                   |
|---------------------|---------------------------------------------------------|
| Webhook Name        | `make-stripe-deposit-trigger`                           |
| Method              | POST                                                    |
| Content-Type        | `application/json`                                      |
| Authentication      | Custom header `X-Make-Secret: {{env.MAKE_WEBHOOK_SECRET}}` |
| Max Payload Size    | 1 MB                                                    |

**Inbound Payload from M-CONCIERGE-ASSIGNMENT:**

```json
{
  "request_id": "recXXXXXXXXXXXXXX",
  "brand": "SSS",
  "city": "Barcelona",
  "client_name": "Jane Hoffman",
  "client_email": "jane.hoffman@example.com",
  "package_interest": "Mediterranean Sunset Charter",
  "concierge_assigned": "Sofia Reyes",
  "submitted_at": "2026-05-16T14:32:00.000Z",
  "source_scenario": "M-CONCIERGE-ASSIGNMENT",
  "environment": "sandbox"
}
```

**Required Fields (all must be present; missing fields trigger error handler at Module 1):**
- `request_id` — Airtable Record ID of the Request (`rec...`)
- `brand` — `"SSS"` or `"ME"`
- `city` — string
- `client_name` — for Stripe metadata and Slack notification
- `package_interest` — used to look up Packages table; also used in Stripe line item name
- `environment` — must be `"sandbox"` in Stage 1

---

## 4. Exact Module Sequence

### Module 1 — [Webhook] Receive Trigger from M-CONCIERGE-ASSIGNMENT

**Make Module Type:** Webhooks > Custom Webhook
**Position:** Module 1

**Validation at this step:**
- `request_id` is present and begins with `rec`
- `brand` is `"SSS"` or `"ME"`
- `environment` is `"sandbox"` (Stage 1 hard requirement — halt if not sandbox)
- `package_interest` is non-empty string

**Environment Guard (Critical):**

```
If {{1.environment}} != "sandbox" → halt scenario immediately.
Post Slack alert: "[SAFETY HALT] M-STRIPE-DEPOSIT received non-sandbox environment value: {{1.environment}}. Execution blocked. Review immediately."
Write Audit Log: Event_Type = "ENVIRONMENT_GUARD_TRIGGERED"
Do NOT make any Stripe API calls.
```

**Output Variables Set:**
```
{{1.request_id}}
{{1.brand}}
{{1.city}}
{{1.client_name}}
{{1.client_email}}
{{1.package_interest}}
{{1.concierge_assigned}}
{{1.submitted_at}}
{{1.environment}}
```

---

### Module 2 — [Airtable] Get Request Record

**Make Module Type:** Airtable > Get a Record
**Position:** Module 2

**Configuration:**

| Parameter    | Value                                    |
|--------------|------------------------------------------|
| Connection   | `airtable-sss-main-connection`           |
| Base ID      | `appdZ49WqgjRXxA1R`                      |
| Table ID     | `tblTlSB9CO4dTGodg` (Requests)           |
| Record ID    | `{{1.request_id}}`                       |

**Fields to retrieve:**

| Airtable Field Name    | Purpose                                                |
|------------------------|--------------------------------------------------------|
| `Request_ID`           | Human-readable ID for Audit Log and Stripe metadata    |
| `Brand`                | Confirm brand (double-check against payload)           |
| `City`                 | Confirm city                                           |
| `Client_Name`          | For Stripe metadata                                    |
| `Client_Email`         | For Stripe session (future use; stored now)            |
| `Package_Interest`     | Package name for Packages table lookup                 |
| `Agent_Status`         | Guard: confirm assignment is complete                  |
| `Concierge_Assigned`   | Confirm assignment exists before creating deposit      |
| `Stripe_Session_ID`    | Duplicate prevention: must be empty to proceed         |
| `Deposit_Link`         | Duplicate prevention: must be empty to proceed         |
| `Group_Size`           | For package lookup context                             |

**Guard Conditions (checked in Module 3):**
```
Agent_Status = "AI_RESPONDING" (confirms concierge has been assigned)
Stripe_Session_ID IS EMPTY (prevents duplicate Stripe session creation)
Deposit_Link IS EMPTY (secondary duplicate check)
```

**Error Handler on Module 2:**
- Record not found: post Slack critical alert, write Audit Log `Event_Type = "RECORD_NOT_FOUND"`, halt.

---

### Module 3 — [Filter] Guard: Assignment Confirmed, No Existing Stripe Session

**Make Module Type:** Filter (built-in)
**Position:** Module 3

**Filter Conditions:**

```
{{2.Agent_Status}} Equal to (text) "AI_RESPONDING"
AND
{{2.Stripe_Session_ID}} Does not exist (empty / null)
AND
{{2.Deposit_Link}} Does not exist (empty / null)
```

**If filter does not pass:**
- If `Stripe_Session_ID` is already populated: scenario halts. Log `Event_Type = "DUPLICATE_SESSION_PREVENTED"` to Audit Log. Post Slack: `"[INFO] M-STRIPE-DEPOSIT: Stripe session already exists for Request {{1.request_id}}. Skipping duplicate creation."`
- If `Agent_Status` is not `AI_RESPONDING`: scenario halts. Log `Event_Type = "ASSIGNMENT_NOT_CONFIRMED"`. Post Slack alert for Luciana.

---

### Module 4 — [Airtable] Search Packages Table — Brand + Package Name Match

**Make Module Type:** Airtable > Search Records
**Position:** Module 4

> **Note:** The Packages table is assumed to exist in base `appdZ49WqgjRXxA1R`. If Packages table does not yet exist or is not yet populated, proceed to Router Module 5 Route B (default deposit) and flag as a build blocker (see Section — Open Issues).

**Configuration:**

| Parameter       | Value                                                                         |
|-----------------|-------------------------------------------------------------------------------|
| Connection      | `airtable-sss-main-connection`                                                |
| Base ID         | `appdZ49WqgjRXxA1R`                                                          |
| Table Name      | `Packages` (confirm exact table name and ID at build time)                    |
| Filter Formula  | See below                                                                     |
| Max Records     | 5                                                                             |

**Airtable Filter Formula (exact):**

```
AND(
  {Live} = TRUE(),
  {Brand} = "{{2.Brand}}",
  OR(
    {Package_Name} = "{{2.Package_Interest}}",
    FIND("{{2.Package_Interest}}", {Package_Name}) > 0
  )
)
```

> **Fallback:** If no exact match, try brand-only match to retrieve any package for that brand as a fallback price reference. This is handled in Router Module 5.

**Fields to retrieve from Packages:**

| Field Name       | Purpose                                              |
|------------------|------------------------------------------------------|
| `Package_Name`   | Confirm match; used in Stripe line item name         |
| `Package_Price`  | Base price for deposit calculation                   |
| `Brand`          | Confirm brand match                                  |
| `City`           | Confirm city match (if city-specific package)        |
| `Currency`       | Should be `USD`; confirm before Stripe call          |
| `Live`           | Confirm package is active                            |
| `Description`    | For Stripe product_data.description (future use)     |

---

### Module 5 — [Router] Package Found or Use Default

**Make Module Type:** Router (built-in)
**Position:** Module 5

**Route A — Package Found:**
```
Condition: {{4[1].Package_Price}} Exists AND {{4[1].Package_Price}} Greater than 0
```
Proceeds to Module 6A (Calculate Deposit from Package Price).

**Route B — No Package Found (Default Deposit):**
```
Fallback route (no additional condition)
```
Proceeds to Module 6B (Apply Default Deposit Amount).

> **Route B triggers a review flag.** The Request record is updated with `Package_Match_Status = "DEFAULT_APPLIED"` and a Slack alert is posted for Luciana to verify the deposit amount before forwarding the link to the client.

---

### Module 6A — [Math] Calculate Deposit from Package Price

**Make Module Type:** Tools > Set Variable (or Math expression inline)
**Position:** Module 6A (Route A only)

**Calculation:**

```
deposit_amount_usd_cents = ROUND({{4[1].Package_Price}} * 0.50 * 100, 0)
deposit_amount_display   = {{4[1].Package_Price}} * 0.50
package_name             = {{4[1].Package_Name}}
package_price            = {{4[1].Package_Price}}
currency                 = {{4[1].Currency}} (default: "usd" if empty)
```

**Set Variables:**

| Variable                   | Value                                            |
|----------------------------|--------------------------------------------------|
| `deposit_amount_cents`     | `{{round(4[1].Package_Price * 0.50 * 100, 0)}}` |
| `deposit_amount_display`   | `{{round(4[1].Package_Price * 0.50, 2)}}`        |
| `package_name_for_stripe`  | `{{4[1].Package_Name}}`                          |
| `package_price`            | `{{4[1].Package_Price}}`                         |
| `currency`                 | `{{if(4[1].Currency; lower(4[1].Currency); "usd")}}` |
| `package_match_status`     | `MATCHED`                                        |

> **Stripe requires `unit_amount` in the smallest currency unit (cents for USD).** A $5,000 package → deposit = $2,500 → `unit_amount = 250000`. Always multiply by 100 and round to integer.

---

### Module 6B — [Set Variable] Apply Default Deposit Amount

**Make Module Type:** Tools > Set Variable
**Position:** Module 6B (Route B — no package found)

**Default values:**

| Variable                   | Value                                             |
|----------------------------|---------------------------------------------------|
| `deposit_amount_cents`     | `75000` (= $750.00 default deposit, test value)   |
| `deposit_amount_display`   | `750.00`                                          |
| `package_name_for_stripe`  | `{{1.package_interest}}` (raw input, unverified)  |
| `package_price`            | `null`                                            |
| `currency`                 | `usd`                                             |
| `package_match_status`     | `DEFAULT_APPLIED`                                 |

> **Stage 1 Default:** $750.00 is a placeholder for testing only. Confirm the real default deposit floor with Will before production. This value is purely a sandbox test figure.

---

### Module 7 — [HTTP] Create Stripe Checkout Session (TEST MODE)

**Make Module Type:** HTTP > Make a Request
**Position:** Module 7 (both routes converge here)

**Configuration:**

| Parameter       | Value                                                                         |
|-----------------|-------------------------------------------------------------------------------|
| URL             | `https://api.stripe.com/v1/checkout/sessions`                                |
| Method          | POST                                                                          |
| Content-Type    | `application/x-www-form-urlencoded`                                           |
| Authorization   | Basic Auth — Username: `{{env.STRIPE_TEST_SECRET_KEY}}`, Password: *(empty)*  |

> **Authorization Detail:** Stripe uses HTTP Basic Auth with the secret key as the username and an empty password. In Make, set the Authorization type to "Basic Auth," enter the test key (`sk_test_...`) as the username, and leave the password blank. Do NOT use Bearer token format for this endpoint.

**Request Body (form-encoded key-value pairs):**

```
mode=payment
payment_method_types[0]=card
line_items[0][price_data][currency]={{currency}}
line_items[0][price_data][unit_amount]={{deposit_amount_cents}}
line_items[0][price_data][product_data][name]=Deposit – {{package_name_for_stripe}}
line_items[0][price_data][product_data][description]=50% deposit for {{1.brand}} charter inquiry from {{1.client_name}}
line_items[0][quantity]=1
metadata[sss_request_id]={{2.Request_ID}}
metadata[airtable_record_id]={{1.request_id}}
metadata[brand]={{1.brand}}
metadata[city]={{1.city}}
metadata[client_name]={{1.client_name}}
metadata[package_name]={{package_name_for_stripe}}
metadata[deposit_amount]={{deposit_amount_display}}
metadata[package_price]={{package_price}}
metadata[concierge_assigned]={{1.concierge_assigned}}
metadata[environment]=sandbox
metadata[source_scenario]=M-STRIPE-DEPOSIT
success_url={{env.STRIPE_SUCCESS_URL}}?session_id={CHECKOUT_SESSION_ID}
cancel_url={{env.STRIPE_CANCEL_URL}}?request_id={{1.request_id}}
expires_at={{addSeconds(now, 86400)}}
```

> **Note on `expires_at`:** Set checkout session to expire after 24 hours. Stripe accepts a Unix timestamp integer. Make's `addSeconds(now, 86400)` gives now + 24 hours. Format as Unix epoch: `{{toTimestamp(addSeconds(now, 86400))}}`.

**Full Stripe API Request (JSON representation for reference):**

```json
{
  "mode": "payment",
  "payment_method_types": ["card"],
  "line_items": [
    {
      "price_data": {
        "currency": "usd",
        "unit_amount": 250000,
        "product_data": {
          "name": "Deposit – Mediterranean Sunset Charter",
          "description": "50% deposit for SSS charter inquiry from Jane Hoffman"
        }
      },
      "quantity": 1
    }
  ],
  "metadata": {
    "sss_request_id": "SSS-2026-0042",
    "airtable_record_id": "recXXXXXXXXXXXXXX",
    "brand": "SSS",
    "city": "Barcelona",
    "client_name": "Jane Hoffman",
    "package_name": "Mediterranean Sunset Charter",
    "deposit_amount": "2500.00",
    "package_price": "5000.00",
    "concierge_assigned": "Sofia Reyes",
    "environment": "sandbox",
    "source_scenario": "M-STRIPE-DEPOSIT"
  },
  "success_url": "https://shesaidsail.com/deposit-success?session_id={CHECKOUT_SESSION_ID}",
  "cancel_url": "https://shesaidsail.com/deposit-cancel?request_id=recXXXXXXXXXXXXXX",
  "expires_at": 1747484400
}
```

**Expected Stripe API Response (success):**

```json
{
  "id": "cs_test_a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6",
  "object": "checkout.session",
  "url": "https://checkout.stripe.com/c/pay/cs_test_a1B2c3D4e5F6g7H8i9J0k1L2m3N4o5P6#fidkdWxOYHwnPyd1blpxYHZxWjA0TmZkNXVOdGZxX0xTNEx0NWBxfj...",
  "payment_status": "unpaid",
  "status": "open",
  "mode": "payment",
  "currency": "usd",
  "amount_total": 250000,
  "metadata": { ... },
  "expires_at": 1747484400,
  "livemode": false
}
```

> **Verify `livemode: false`** in the response. If `livemode: true` appears, the wrong API key is configured. Halt scenario immediately and alert Will.

**Output Variables:**

| Variable                         | Source in Response           |
|----------------------------------|------------------------------|
| `stripe_session_id`              | `{{7.id}}`                   |
| `stripe_checkout_url`            | `{{7.url}}`                  |
| `stripe_payment_status`          | `{{7.payment_status}}`       |
| `stripe_livemode`                | `{{7.livemode}}`             |
| `stripe_amount_total`            | `{{7.amount_total}}`         |
| `stripe_expires_at`              | `{{7.expires_at}}`           |

---

### Module 8 — [Router] Stripe API Success or Failure

**Make Module Type:** Router (built-in)
**Position:** Module 8

**Route A — Stripe Success:**
```
Condition: {{7.id}} Exists AND {{7.id}} starts with "cs_"
AND {{7.livemode}} Equal to (boolean) false
```
Proceeds to Module 9 (Update Request Record).

**Route B — Stripe Error or Live Mode Detected:**
```
Fallback route
Additional check: If {{7.livemode}} = true → post CRITICAL alert before halting
```
Proceeds to Module 8B (Error Handler — Stripe Failure).

---

### Module 8B — [Slack + Airtable] Stripe Failure Handler

**Make Module Type:** Slack > Create a Message + Airtable > Update a Record
**Position:** Module 8B (Route B only)

**Actions:**
1. Post Slack critical alert (see Section 6 — Error Handling)
2. Update Request record: `Stripe_Error = "{{7.error.message}}"`, `Stripe_Error_At = {{now}}`
3. Write Audit Log: `Event_Type = "STRIPE_SESSION_CREATION_FAILED"`
4. Halt scenario — do NOT proceed to Module 9

---

### Module 9 — [Airtable] Update Request Record with Stripe Data

**Make Module Type:** Airtable > Update a Record
**Position:** Module 9 (Route A only, after Stripe success)

**Configuration:**

| Parameter    | Value                                    |
|--------------|------------------------------------------|
| Connection   | `airtable-sss-main-connection`           |
| Base ID      | `appdZ49WqgjRXxA1R`                      |
| Table ID     | `tblTlSB9CO4dTGodg` (Requests)           |
| Record ID    | `{{1.request_id}}`                       |

**Field Writes (exact Airtable field names):**

| Airtable Field Name      | Value Written                              | Format          |
|--------------------------|--------------------------------------------|-----------------|
| `Deposit_Link`           | `{{7.url}}`                                | URL text        |
| `Stripe_Session_ID`      | `{{7.id}}`                                 | Text            |
| `Deposit_Amount`         | `{{deposit_amount_display}}`               | Number (decimal)|
| `Deposit_Sent_At`        | `{{now}}`                                  | ISO 8601 UTC    |
| `Package_Name_Matched`   | `{{package_name_for_stripe}}`              | Text            |
| `Package_Price`          | `{{package_price}}`                        | Number          |
| `Package_Match_Status`   | `{{package_match_status}}`                 | Single select   |
| `Agent_Status`           | `DEPOSIT_LINK_CREATED`                     | Single select   |
| `Stripe_Session_Expires` | `{{formatDate(stripe_expires_at, "X")}}`   | DateTime        |
| `Stripe_Livemode`        | `{{7.livemode}}`                           | Checkbox        |
| `Currency`               | `{{currency}}`                             | Text            |

> **`Stripe_Livemode` field:** This checkbox field records whether the session was created in live or test mode. In Stage 1, this MUST always be `false`. The field provides a permanent audit record of the mode at time of creation.

**Error Handler on Module 9:**
- On Airtable write failure: Stripe session has already been created. Post Slack critical alert with the checkout URL so Luciana can retrieve it manually. Write Audit Log: `Event_Type = "AIRTABLE_WRITE_FAILED_POST_STRIPE"`. This is a HIGH priority error — the URL may be lost if not posted to Slack.
- **Slack message must include the full `{{7.url}}`** so the link is not permanently lost.

**Single Select Values — Must Exist in Airtable Before Build:**

| Table    | Field                  | Required Options                                                          |
|----------|------------------------|---------------------------------------------------------------------------|
| Requests | `Agent_Status`         | `DEPOSIT_LINK_CREATED` (add to existing list)                             |
| Requests | `Package_Match_Status` | `MATCHED`, `DEFAULT_APPLIED`                                              |

---

### Module 10 — [Slack] Post Deposit Link Notification to #sss-ops-alerts

**Make Module Type:** Slack > Create a Message
**Position:** Module 10 (after Module 9 succeeds)

See Section 13 for full message format.

> **CRITICAL:** This Slack message is the ONLY place the deposit link goes in Stage 1. Luciana reads this message and manually forwards the link to the client. There is NO automated email or SMS to the client. This is by design.

---

### Module 11 — [Airtable] Write Audit Log Entry

**Make Module Type:** Airtable > Create a Record
**Position:** Module 11 (after Module 10)

See Section 8 for exact field writes.

---

### Module 12 — [HTTP] Trigger M-BOOKING-CREATION (Future — Stub in Stage 1)

**Make Module Type:** HTTP > Make a Request (STUBBED)
**Position:** Module 12

> **Stage 1:** M-BOOKING-CREATION is not yet built. This module is included as a placeholder. In Stage 1, set this module to call a Make webhook that immediately returns `200 OK` without doing anything (a "dead end" webhook). This allows the scenario to complete cleanly and avoids breaking the pipeline when M-BOOKING-CREATION is not yet ready.

**Payload to M-BOOKING-CREATION (when built):**

```json
{
  "request_id": "{{1.request_id}}",
  "brand": "{{1.brand}}",
  "city": "{{1.city}}",
  "client_name": "{{1.client_name}}",
  "stripe_session_id": "{{7.id}}",
  "deposit_amount": "{{deposit_amount_display}}",
  "package_name": "{{package_name_for_stripe}}",
  "concierge_assigned": "{{1.concierge_assigned}}",
  "source_scenario": "M-STRIPE-DEPOSIT",
  "environment": "{{1.environment}}"
}
```

---

## 5. Stripe Metadata Structure

**Complete metadata object written to every Stripe Checkout Session:**

```json
{
  "metadata": {
    "sss_request_id": "{{2.Request_ID}}",
    "airtable_record_id": "{{1.request_id}}",
    "brand": "{{1.brand}}",
    "city": "{{1.city}}",
    "client_name": "{{1.client_name}}",
    "client_email": "{{1.client_email}}",
    "package_name": "{{package_name_for_stripe}}",
    "deposit_amount": "{{deposit_amount_display}}",
    "package_price": "{{package_price}}",
    "concierge_assigned": "{{1.concierge_assigned}}",
    "package_match_status": "{{package_match_status}}",
    "environment": "sandbox",
    "source_scenario": "M-STRIPE-DEPOSIT",
    "scenario_version": "1.0",
    "created_at_iso": "{{formatDate(now, 'YYYY-MM-DDTHH:mm:ss[Z]')}}"
  }
}
```

**Metadata Field Specifications:**

| Key                    | Max Length | Type   | Required | Description                                      |
|------------------------|------------|--------|----------|--------------------------------------------------|
| `sss_request_id`       | 500        | String | Yes      | Human-readable Request ID from Airtable          |
| `airtable_record_id`   | 500        | String | Yes      | Airtable recXXX record ID for direct lookup      |
| `brand`                | 500        | String | Yes      | `"SSS"` or `"ME"`                                |
| `city`                 | 500        | String | Yes      | Charter city for operational routing             |
| `client_name`          | 500        | String | Yes      | For payment confirmation and ops reference       |
| `client_email`         | 500        | String | No       | Stored for future webhook processing             |
| `package_name`         | 500        | String | Yes      | Package being deposited against                  |
| `deposit_amount`       | 500        | String | Yes      | Human-readable (e.g., `"2500.00"`)               |
| `package_price`        | 500        | String | No       | Full package price; null if no package matched   |
| `concierge_assigned`   | 500        | String | Yes      | Name of assigned concierge at time of deposit    |
| `package_match_status` | 500        | String | Yes      | `MATCHED` or `DEFAULT_APPLIED`                   |
| `environment`          | 500        | String | Yes      | Always `"sandbox"` in Stage 1                    |
| `source_scenario`      | 500        | String | Yes      | `"M-STRIPE-DEPOSIT"` for traceability            |
| `scenario_version`     | 500        | String | Yes      | `"1.0"` — increment on spec changes              |
| `created_at_iso`       | 500        | String | Yes      | ISO 8601 timestamp of session creation           |

> **Stripe metadata limit:** Each key and value is limited to 500 characters. Total metadata is limited to 50 keys. This implementation uses 14 keys, well within limits.

> **Important:** When Stripe fires a webhook (Stage 2), these metadata fields allow the webhook handler to reconstruct full context without querying Airtable. Design the metadata to be self-contained.

---

## 6. Error Handling

### Error Class 1 — Environment Guard Triggered (Module 1)

**Trigger:** `{{1.environment}}` is not `"sandbox"`.

**Action:**
1. Post Slack:
   ```
   🔴 [SAFETY HALT] M-STRIPE-DEPOSIT blocked a non-sandbox execution.
   environment value received: {{1.environment}}
   Request ID: {{1.request_id}}
   Time: {{now}}
   Action required: Investigate immediately. No Stripe API calls were made.
   ```
2. Write Audit Log: `Event_Type = "ENVIRONMENT_GUARD_TRIGGERED"`, `Status = "HALTED"`
3. Halt — no further modules execute

---

### Error Class 2 — Stripe Live Mode Detected in Response (Module 8)

**Trigger:** `{{7.livemode}}` = `true` in Stripe API response.

**Action:**
1. Post Slack CRITICAL:
   ```
   🔴🔴 [CRITICAL] M-STRIPE-DEPOSIT created a LIVE Stripe session in Stage 1.
   Session ID: {{7.id}}
   This session must be immediately voided/expired in the Stripe Dashboard.
   Request ID: {{1.request_id}}
   Time: {{now}}
   Action required: Will + Luciana to review immediately.
   ```
2. Write Audit Log: `Event_Type = "LIVE_MODE_CONTAMINATION"`, `Status = "CRITICAL"`
3. Do NOT write session ID to Airtable (prevents this URL from being forwarded to client)
4. Halt scenario

---

### Error Class 3 — Stripe API Authentication Failure (Module 7)

**Trigger:** Stripe returns HTTP 401 (`invalid_api_key` or `api_key_expired`).

**HTTP 401 Response:**
```json
{
  "error": {
    "type": "invalid_request_error",
    "code": "api_key_invalid",
    "message": "No such API key: 'sk_test_...'"
  }
}
```

**Action:**
1. Post Slack:
   ```
   🔴 [STRIPE AUTH FAILURE] Invalid or expired API key in M-STRIPE-DEPOSIT.
   Error: {{7.error.message}}
   Request ID: {{1.request_id}}
   Action: Verify STRIPE_TEST_SECRET_KEY in Make environment variables.
   ```
2. Write Audit Log: `Event_Type = "STRIPE_AUTH_FAILED"`, `HTTP_Status = "401"`
3. Halt — do not retry (authentication errors are not transient)

---

### Error Class 4 — Stripe Rate Limit (Module 7)

**Trigger:** Stripe returns HTTP 429.

**Action:**
1. Retry after 60 seconds (up to 3 retries)
2. If still failing after retries: post Slack alert, write Audit Log `Event_Type = "STRIPE_RATE_LIMIT"`, halt
3. Store in Make Incomplete Executions for manual re-run

---

### Error Class 5 — Stripe API Network Failure (Module 7)

**Trigger:** HTTP timeout or connection error (no response from Stripe).

**Action:**
1. Retry after 30 seconds (up to 3 retries — see Section 7 Retry Logic)
2. After max retries: post Slack, write Audit Log `Event_Type = "STRIPE_NETWORK_FAILURE"`, halt

---

### Error Class 6 — Airtable Write Failure After Stripe Session Created (Module 9)

**Trigger:** Airtable returns 4xx or 5xx when writing Deposit_Link and Stripe_Session_ID.

**This is the highest-risk error state.** A Stripe session exists but the URL is not saved in Airtable.

**Action:**
1. Post Slack URGENT — **include the full checkout URL in the message**:
   ```
   🔴 [URGENT] M-STRIPE-DEPOSIT: Stripe session created but Airtable write FAILED.
   The deposit link MUST be saved manually.

   Request ID: {{1.request_id}}
   Stripe Session ID: {{7.id}}
   Deposit Link: {{7.url}}
   Deposit Amount: ${{deposit_amount_display}}
   Client: {{1.client_name}}
   Error: {{error.message}} (HTTP {{error.statusCode}})
   Time: {{now}}

   Action (Luciana): Open Airtable record {{1.request_id}} and paste:
   • Deposit_Link = {{7.url}}
   • Stripe_Session_ID = {{7.id}}
   • Deposit_Sent_At = {{formatDate(now, "MMMM D, YYYY [at] h:mm A")}}
   ```
2. Retry Airtable write once after 60 seconds
3. If retry fails: halt and require manual intervention. The Slack message above contains all needed data.

---

### Error Class 7 — Packages Table Not Found or Empty (Module 4)

**Trigger:** Module 4 search returns 0 results (or table does not exist — returns Airtable error).

**This triggers Route B (default deposit) — not a hard error.**

**Action:**
1. Set `package_match_status = "DEFAULT_APPLIED"`
2. Apply default deposit of $750.00 (sandbox placeholder)
3. Continue to Module 7
4. Include flag in Slack notification (Module 10) — see Section 13, Alert Type B format

---

## 7. Duplicate Prevention

### Prevention Layer 1 — Stripe_Session_ID Field Check (Module 3)

Before creating any Stripe session, Module 3 verifies that `Stripe_Session_ID` is empty in the Airtable record. If it is populated, the scenario halts immediately with a skip log. This is the primary guard.

### Prevention Layer 2 — Deposit_Link Field Check (Module 3)

Secondary check: `Deposit_Link` must also be empty. If only one of the two fields is populated (partial write from a prior failed run), Module 3 still catches it.

### Prevention Layer 3 — Read-before-Write Pattern

Module 2 fetches the current record state immediately before the guard check. This minimizes (but does not eliminate) the window for a race condition. In Stage 1 with low volume, this is sufficient.

### Prevention Layer 4 — Idempotency Key (Future — Stage 2)

Stripe supports idempotency keys (`Idempotency-Key` header on POST requests). In Stage 2, pass `{{1.request_id}}` as the idempotency key. If the same request ID is sent twice within 24 hours, Stripe returns the original session rather than creating a new one. This is not implemented in Stage 1 but is the correct production-grade solution.

### Known Limitation — Race Condition Window

There is a small window between Module 2 (read) and Module 7 (Stripe API call) where a duplicate trigger could also reach Module 7. Both would create separate Stripe sessions. Prevention Layer 1 catches this for the second execution only if it reads after the first execution completes Module 9. In Stage 1 with expected volume of 1-5 requests/day, simultaneous duplicates are extremely unlikely. Document for Stage 2 remediation via Stripe idempotency keys.

---

## 8. Audit Log Writes

**Table:** Audit Log (tblrMpTfMk8q1eNHp)
**Module:** 11 (success path)
**Make Module Type:** Airtable > Create a Record

### Successful Deposit Session Creation

| Audit Log Field              | Value Written                                               |
|------------------------------|-------------------------------------------------------------|
| `Event_Type`                 | `STRIPE_DEPOSIT_SESSION_CREATED`                            |
| `Event_Timestamp`            | `{{now}}` (ISO 8601 UTC)                                    |
| `Request_ID`                 | `{{2.Request_ID}}` (human-readable)                         |
| `Airtable_Record_ID`         | `{{1.request_id}}` (recXXXXXX)                              |
| `Brand`                      | `{{1.brand}}`                                               |
| `City`                       | `{{1.city}}`                                                |
| `Client_Name`                | `{{1.client_name}}`                                         |
| `Concierge_Assigned`         | `{{1.concierge_assigned}}`                                  |
| `Stripe_Session_ID`          | `{{7.id}}`                                                  |
| `Deposit_Amount`             | `{{deposit_amount_display}}`                                |
| `Package_Name`               | `{{package_name_for_stripe}}`                               |
| `Package_Match_Status`       | `{{package_match_status}}`                                  |
| `Stripe_Livemode`            | `{{7.livemode}}` (should always be `false` in Stage 1)      |
| `Deposit_Link`               | `{{7.url}}`                                                 |
| `Session_Expires_At`         | `{{7.expires_at}}`                                          |
| `Triggered_By_Scenario`      | `M-STRIPE-DEPOSIT`                                          |
| `Scenario_ID`                | `PENDING-REGISTRATION`                                      |
| `Execution_ID`               | `{{scenarioExecutionId}}`                                   |
| `Status`                     | `SUCCESS`                                                   |
| `Environment`                | `sandbox`                                                   |
| `Notes`                      | `Stripe checkout session created in TEST MODE. Luciana to forward link manually.` |

### Failed Stripe Session (Error Path)

| Audit Log Field    | Value Written                                                  |
|--------------------|----------------------------------------------------------------|
| `Event_Type`       | `STRIPE_SESSION_CREATION_FAILED`                               |
| `Status`           | `FAILED`                                                       |
| `Error_Message`    | `{{7.error.message}}`                                          |
| `HTTP_Status_Code` | `{{7.statusCode}}`                                             |
| `Notes`            | `Stripe API error. No session created. No client impact.`      |
| *(all other fields as above)* |                                                    |

---

## 9. Critical Stage 1 Safety Rule

### NO Automated Deposit Link Delivery to Client

This rule is absolute in Stage 1:

- The Stripe checkout URL (`{{7.url}}`) is posted ONLY to Slack channel `#sss-ops-alerts`
- Luciana reads the Slack message and forwards the link to the client via her preferred channel (email, WhatsApp, phone)
- No module in this scenario sends an email, SMS, or any direct client communication
- This rule exists because Stage 1 is a sandbox with a test Stripe key. Real clients must never receive test links or test payment forms.

**Build verification:** Review every module in this scenario. Confirm zero modules call:
- Any email service (SendGrid, Mailgun, Gmail, etc.)
- Any SMS service (Twilio, etc.)
- Any WhatsApp API
- Any CRM contact notification

If any such module is present: remove it before activation.

---

## 10. Rollback: Voiding a Stripe Checkout Session

**Use case:** A Stripe checkout session was created in error (wrong amount, wrong client, wrong package, or accidentally created in what turned out to be the wrong context).

**Step 1 — Expire the Stripe Session (within 24 hours):**

Stripe allows checkout sessions to be expired before payment. Make an API call:

```bash
curl -X POST https://api.stripe.com/v1/checkout/sessions/{{stripe_session_id}}/expire \
  -u sk_test_XXXXXXXXXXXXXXXXXXXX:
```

In Make, this can be executed with an HTTP module (POST, Basic Auth with test key, no body required).

**Step 2 — Update Airtable Request Record:**

| Field                   | Action                               |
|-------------------------|--------------------------------------|
| `Deposit_Link`          | Clear (delete value)                 |
| `Stripe_Session_ID`     | Clear (delete value)                 |
| `Deposit_Amount`        | Clear                                |
| `Deposit_Sent_At`       | Clear                                |
| `Stripe_Session_Expires`| Clear                                |
| `Package_Match_Status`  | Clear                                |
| `Agent_Status`          | Revert to `AI_RESPONDING`            |
| `Stripe_Error`          | Add note: "Session voided — [reason]"|

**Step 3 — Write Audit Log Entry:**

| Field          | Value                                      |
|----------------|--------------------------------------------|
| `Event_Type`   | `STRIPE_SESSION_VOIDED`                    |
| `Status`       | `ROLLED_BACK`                              |
| `Notes`        | Reason for void, who performed it, time    |

**Step 4 — Re-trigger if Needed:**

If a new session is needed with corrected data (e.g., correct package price): manually trigger M-STRIPE-DEPOSIT via webhook with corrected payload. The guard at Module 3 will now pass because `Stripe_Session_ID` and `Deposit_Link` are cleared.

> **Note:** If the client has already received the link from Luciana, Luciana must message the client to ignore the previous link and expect a corrected one. Document this in the re-trigger Slack alert.

---

## 11. Sandbox Test Procedure

**Pre-conditions:**
- Make environment variable `STRIPE_TEST_SECRET_KEY` is set to a valid `sk_test_...` key
- Make environment variable `STRIPE_SUCCESS_URL` = `https://shesaidsail.com/deposit-success` (or a test URL)
- Make environment variable `STRIPE_CANCEL_URL` = `https://shesaidsail.com/deposit-cancel` (or a test URL)
- Airtable Requests table has a test record with `Agent_Status = "AI_RESPONDING"`, `Stripe_Session_ID` empty, `Deposit_Link` empty
- Packages table has a test package record: `Package_Name = "Mediterranean Sunset Charter"`, `Brand = "SSS"`, `Package_Price = 5000`, `Live = true`
- `environment = "sandbox"` in all test payloads
- Stripe Dashboard test mode is active (verify at dashboard.stripe.com — top of page shows "Test mode")

---

**Test Case 1 — Happy Path (Package Found, Deposit Calculated):**

```bash
curl -X POST {{MAKE_STRIPE_DEPOSIT_WEBHOOK_URL}} \
  -H "Content-Type: application/json" \
  -H "X-Make-Secret: {{MAKE_WEBHOOK_SECRET}}" \
  -d '{
    "request_id": "recTEST0000000001",
    "brand": "SSS",
    "city": "Barcelona",
    "client_name": "Test Client A",
    "client_email": "test@example.com",
    "package_interest": "Mediterranean Sunset Charter",
    "concierge_assigned": "Sofia Reyes",
    "submitted_at": "2026-05-16T10:00:00.000Z",
    "source_scenario": "M-CONCIERGE-ASSIGNMENT",
    "environment": "sandbox"
  }'
```

**Expected outcomes:**
- [ ] Module 1: Payload validated, environment = "sandbox" confirmed
- [ ] Module 2: Request record retrieved, `Agent_Status = "AI_RESPONDING"`, no existing session
- [ ] Module 3: Guard passes
- [ ] Module 4: Package found — `Package_Price = 5000`
- [ ] Module 5: Route A fires
- [ ] Module 6A: `deposit_amount_cents = 250000`, `deposit_amount_display = "2500.00"`
- [ ] Module 7: Stripe API returns `cs_test_...` session ID, `livemode = false`, `url` begins with `https://checkout.stripe.com`
- [ ] Module 8: Route A fires (success)
- [ ] Module 9: Airtable updated — `Deposit_Link`, `Stripe_Session_ID`, `Deposit_Amount = 2500`, `Agent_Status = "DEPOSIT_LINK_CREATED"`, `Stripe_Livemode = false`
- [ ] Module 10: Slack message posted to `#sss-ops-alerts` with correct deposit details
- [ ] Module 11: Audit Log record created with `Event_Type = "STRIPE_DEPOSIT_SESSION_CREATED"`, `Status = "SUCCESS"`, `Stripe_Livemode = false`

**Verify in Stripe Dashboard:**
- [ ] Navigate to dashboard.stripe.com → Payments → Payment Links (or Checkout Sessions)
- [ ] Confirm session `cs_test_...` appears with status `Open`
- [ ] Confirm metadata fields are all present and correct
- [ ] Confirm `livemode = false`
- [ ] Confirm `amount_total = 250000` (= $2,500.00)

**Test payment using Stripe test cards:**
- Success: `4242 4242 4242 4242`, any future expiry, any CVC, any ZIP
- Decline: `4000 0000 0000 9995`, same
- The payment result has NO effect in Stage 1 — the Stripe webhook is not registered and no downstream action fires on payment. This is expected and correct behavior.

---

**Test Case 2 — No Package Match (Default Deposit Applied):**

Use `package_interest = "Unknown Package XYZ"` to force no match.

**Expected outcomes:**
- [ ] Module 4: Returns 0 results
- [ ] Module 5: Route B fires
- [ ] Module 6B: `deposit_amount_cents = 75000`, `package_match_status = "DEFAULT_APPLIED"`
- [ ] Module 7: Stripe session created for $750.00
- [ ] Module 9: `Package_Match_Status = "DEFAULT_APPLIED"` written to Airtable
- [ ] Module 10: Slack message includes flag: "Default deposit applied — package not found. Luciana to verify before forwarding link."

---

**Test Case 3 — Duplicate Prevention:**

Re-send Test Case 1 payload (same `request_id`) after it has already processed.

**Expected outcomes:**
- [ ] Module 2: Record retrieved — `Stripe_Session_ID` is now populated
- [ ] Module 3: Guard fails — scenario halts cleanly
- [ ] No new Stripe session created
- [ ] No duplicate Slack alert
- [ ] Audit Log entry created with `Event_Type = "DUPLICATE_SESSION_PREVENTED"`

---

**Test Case 4 — Environment Guard:**

Send payload with `environment = "production"`.

**Expected outcomes:**
- [ ] Module 1: Environment guard fires
- [ ] Slack alert posted with `[SAFETY HALT]` prefix
- [ ] Audit Log: `Event_Type = "ENVIRONMENT_GUARD_TRIGGERED"`
- [ ] No Stripe API call made
- [ ] No Airtable writes (except Audit Log)

---

## 12. Stripe Webhook — Stage 2 Boundary

**This section documents a deliberate scope boundary.**

### What is NOT implemented in Stage 1:

- Stripe webhook endpoint registration
- Payment success event handling (`checkout.session.completed`)
- Payment failure event handling (`checkout.session.expired`, `payment_intent.payment_failed`)
- Automatic status updates in Airtable when payment completes
- Automatic trigger of M-BOOKING-CREATION on payment confirmation
- Client payment confirmation email

### Why this boundary exists:

Stage 1 purpose is to validate the end-to-end automation pipeline in sandbox mode without real financial transactions. The Stripe webhook represents a real-world event boundary (actual payment by a real client). Registering the webhook before the pipeline is tested creates noise and potential for confusion between test and live events.

### Stage 2 Webhook Implementation (documented here for planning):

**When Stage 2 begins, the following must be built:**

1. Register a Stripe webhook endpoint in the Stripe Dashboard (or via Stripe CLI for local testing)
2. Create a new Make scenario `M-STRIPE-WEBHOOK-HANDLER`
3. Endpoint URL: `{{env.MAKE_STRIPE_WEBHOOK_URL}}`
4. Events to subscribe:
   - `checkout.session.completed` (payment succeeded)
   - `checkout.session.expired` (client did not pay within 24 hours)
   - `payment_intent.payment_failed`
5. Verify webhook signature using `{{env.STRIPE_WEBHOOK_SIGNING_SECRET}}` (Make HTTP module → verify header `Stripe-Signature`)
6. On `checkout.session.completed`: update Request `Agent_Status = "DEPOSIT_PAID"`, trigger M-BOOKING-CREATION
7. On `checkout.session.expired`: update Request `Agent_Status = "DEPOSIT_EXPIRED"`, alert Luciana

**Blocker:** Do not register the webhook until sandbox test passes completely (all Test Cases in Section 11 pass). Premature webhook registration creates live event noise in the Stripe Dashboard.

---

## 13. Slack Alert Structure

### Channel: `#sss-ops-alerts`

### Alert Type A — Deposit Link Created (Standard, Package Matched)

```
💳 *DEPOSIT LINK CREATED* | {{1.brand}} — {{1.city}}

*Client:* {{1.client_name}}
*Package:* {{package_name_for_stripe}}
*Package Price:* ${{package_price}}
*Deposit Amount:* ${{deposit_amount_display}} (50%)
*Assigned Concierge:* {{1.concierge_assigned}}

*Stripe Session:* {{7.id}}
*Deposit Link:* {{7.url}}
*Link Expires:* 24 hours from now

*Request ID:* {{2.Request_ID}} | *Record:* {{1.request_id}}
*Mode:* TEST (sandbox — Stripe test key active)
*Timestamp:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

---
*Action required (Luciana):*
Forward the deposit link to {{1.client_name}} via your preferred channel.
Do NOT use the automated email system — Stage 1 is manual client delivery.
```

### Alert Type B — Deposit Link Created (Default Deposit Applied — No Package Match)

```
⚠️ *DEPOSIT LINK CREATED — REVIEW REQUIRED* | {{1.brand}} — {{1.city}}

No exact package match found for "{{1.package_interest}}".
Default deposit of ${{deposit_amount_display}} applied.

*Client:* {{1.client_name}}
*Package Interest (raw):* {{1.package_interest}}
*Default Deposit Applied:* ${{deposit_amount_display}}
*Assigned Concierge:* {{1.concierge_assigned}}

*Stripe Session:* {{7.id}}
*Deposit Link:* {{7.url}}

*Request ID:* {{2.Request_ID}} | *Record:* {{1.request_id}}
*Mode:* TEST (sandbox)
*Timestamp:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

---
*Action required (Luciana):*
1. Verify the ${{deposit_amount_display}} deposit amount is correct for this inquiry
2. If wrong: do NOT forward this link — void the session and re-trigger with correct package
3. If correct: forward deposit link to {{1.client_name}} manually
```

### Alert Type C — Stripe Session Write Failed (Emergency)

```
🔴 *EMERGENCY — DEPOSIT LINK NOT SAVED TO AIRTABLE*

Stripe session was created but Airtable write FAILED.
This link will be lost if not saved manually RIGHT NOW.

*Stripe Session ID:* {{7.id}}
*DEPOSIT LINK:* {{7.url}}

*Client:* {{1.client_name}}
*Amount:* ${{deposit_amount_display}}
*Request Record:* {{1.request_id}}
*Error:* {{error.message}}
*Time:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

*Immediate action required (Luciana/Will):*
1. Open Airtable → Requests → {{1.request_id}}
2. Paste Deposit_Link = the URL above
3. Paste Stripe_Session_ID = {{7.id}}
4. Set Deposit_Sent_At = now
5. Set Agent_Status = "DEPOSIT_LINK_CREATED"
```

---

## 14. Open Issues

### Issue 1 — Stripe Webhook URL Not Yet Registered

**Status:** BLOCKER for Stage 2. Not a blocker for Stage 1.

**Description:** The Stripe webhook that fires on payment completion (`checkout.session.completed`) has not been registered. This means paid deposits will not automatically update Airtable or trigger M-BOOKING-CREATION.

**Stage 1 Workaround:** Luciana manually monitors the Stripe Dashboard for successful test payments during sandbox testing. Airtable is updated manually when a test payment completes.

**Resolution in Stage 2:** After all Stage 1 test cases pass, register the webhook in Stripe Dashboard pointing to the M-STRIPE-WEBHOOK-HANDLER scenario URL. See Section 12 for full specification.

**Owner:** Will (Stripe account access) + Systems team (Make scenario build)

---

### Issue 2 — Packages Table Existence Unconfirmed

**Status:** BLOCKER if table does not exist.

**Description:** Module 4 assumes a `Packages` table exists in base `appdZ49WqgjRXxA1R` with fields `Package_Name`, `Package_Price`, `Brand`, `City`, `Live`. If this table does not exist or is not populated, every execution will follow Route B (default deposit).

**Resolution:** Confirm table exists and has at least one record before activating this scenario. If table needs to be created, add to pre-build checklist.

**Stage 1 Workaround:** Route B (default $750 test deposit) allows sandbox testing to proceed even if the Packages table is empty.

---

### Issue 3 — Success/Cancel URL Configuration

**Status:** Requires Will's input.

**Description:** The `success_url` and `cancel_url` in the Stripe checkout session point to the She Said Sail / Mare Executive website. These URLs must be valid, live web pages that handle the `session_id` query parameter gracefully.

**Resolution needed:** Confirm exact URLs for:
- SSS payment success page
- SSS payment cancel page
- ME payment success page (if different)
- ME payment cancel page (if different)

**Stage 1 Workaround:** Use placeholder URLs for sandbox testing. Stripe does not actually redirect in test mode unless someone clicks through the test checkout.

---

### Issue 4 — Stripe Test Key Rotation Policy

**Status:** Operational process gap.

**Description:** The Stripe test API key (`sk_test_...`) stored in Make environment variables must be rotated regularly. There is currently no documented rotation procedure.

**Resolution:** Establish key rotation schedule (quarterly). Document who has access to update `STRIPE_TEST_SECRET_KEY` in Make.

---

### Issue 5 — Default Deposit Amount ($750) is a Placeholder

**Status:** Requires Will's input before production.

**Description:** The $750 default deposit amount in Module 6B is a sandbox test placeholder. The real business rule for default deposits (when no package matches) has not been defined.

**Resolution:** Will to define: what is the minimum deposit for an unconfirmed inquiry? Is it $0 (no deposit until package confirmed)? A fixed floor? A percentage of average package price?

---

### Issue 6 — Currency Assumption

**Status:** Requires confirmation.

**Description:** This scenario assumes USD for all transactions. The `currency` variable defaults to `"usd"` if the Packages table does not specify a currency. If SSS or ME operates with EUR or GBP pricing in certain markets, the Stripe `unit_amount` calculation and the currency code must be updated accordingly.

**Resolution:** Confirm with Will: are all charter deposits processed in USD, or does currency vary by city/market?

---

## 15. Final Scenario Status

| Field                     | Value                                                       |
|---------------------------|-------------------------------------------------------------|
| **Status**                | `PENDING BUILD`                                             |
| **Scenario ID**           | `PENDING-REGISTRATION`                                      |
| **Make Workspace**        | She Said Sail + Mare Executive                              |
| **Target Build Date**     | TBD                                                         |
| **Builder**               | TBD                                                         |
| **Reviewer**              | Luciana (Ops Lead)                                          |
| **Approver**              | Will (Founder)                                              |
| **Dependencies**          | M-CONCIERGE-ASSIGNMENT must be built and tested first       |
| **Blocks**                | M-BOOKING-CREATION cannot be tested until this passes       |
| **Stripe Mode**           | TEST (Stage 1) — `sk_test_...` only                         |
| **Webhook Registered**    | NO — registered in Stage 2 only                             |
| **Environment**           | SANDBOX (Stage 1)                                           |
| **Estimated Modules**     | 12-14 modules                                               |
| **Estimated Build Time**  | 4-5 hours                                                   |
| **Open Issues Count**     | 6 (see Section 14)                                          |
| **Blockers**              | Issues 1 (webhook, Stage 2 only), 2 (Packages table)        |

---

*Document prepared by Systems Architecture — She Said Sail + Mare Executive Stage 1 Implementation*
*Do not activate this scenario in production until all items in the Production Validation Checklist are checked and all Stage 1 sandbox test cases pass.*
*Under no circumstances use the live Stripe key (`sk_live_...`) until Stage 2 sign-off is complete.*
