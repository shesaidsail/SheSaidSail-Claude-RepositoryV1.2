# MAKE NATIVE MODULE REFERENCE MASTER
## She Said Sail — Stage 1 Blueprint Reference

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Date:** May 2026  
**Scope:** All modules used or considered for Stage 1 scenarios

---

## MODULE CATALOG

### Trigger Modules

#### `airtable:TriggerWatchRecords` v3
- **Type:** Polling trigger (not instant)
- **Use:** Watch Airtable table for new/updated records
- **Required parameters:** `base` (base ID), `table` (table name or ID), `triggerField` (Updated_At or Created_At), `maxResults`
- **Polling interval:** Set in Make scenario settings (minimum: 1 minute on paid plan)
- **Used in:** M-STRIPE-DEPOSIT, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION
- **Notes:** Must use v3. v1/v2 are deprecated. If triggering on status changes, the Airtable record must have an Updated_At timestamp field that Make can compare against.

#### `gateway:CustomWebHook` v1
- **Type:** Instant webhook trigger
- **Use:** Receive inbound HTTP POST requests
- **Required parameters:** `hook` (webhook ID — assigned by Make on creation), `maxResults`
- **Response:** Use `gateway:WebhookRespond` to return a custom response. If no response module, Make returns 200 with empty body.
- **Used in:** M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BRAND-ROUTER, M-LEAD-INTAKE, M-BOOKING-CREATION
- **Notes:** Each webhook gets a unique URL. Store URL in credential vault after import. Add bearer token validation for security.

---

### Action Modules

#### `airtable:ActionCreateRecord` v3
- **Type:** Action
- **Use:** Create a new record in an Airtable table
- **Required parameters:** `base`, `table`, `fields` (object)
- **Returns:** Record object including `id` (Airtable record ID)
- **Used in:** M-AUDIT-LOGGER, M-BRAND-ROUTER, M-LEAD-INTAKE
- **Notes:** v3 required. Field names must match exactly — Airtable field names are case-sensitive. For linked record fields, pass an array of objects: `[{"id": "recXXXX"}]`

#### `airtable:ActionUpdateRecord` v3
- **Type:** Action
- **Use:** Update an existing Airtable record
- **Required parameters:** `base`, `table`, `id` (record ID), `fields` (object)
- **Returns:** Updated record object
- **Used in:** M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION
- **Notes:** `id` must be the Airtable record ID (format: `recXXXXXXXXXXXXXX`). Pass only the fields you want to update — other fields are unchanged.

#### `airtable:SearchRecords` v3
- **Type:** Action
- **Use:** Search for records in Airtable using a filterByFormula expression
- **Required parameters:** `base`, `table`, `formula`
- **Returns:** Array of matching records
- **Used in:** M-LEAD-INTAKE (deduplication), M-BOOKING-CREATION (idempotency)
- **Notes:** Formula uses Airtable formula syntax. String comparison: `{Field} = 'value'`. Date comparison: `IS_AFTER({Created_At}, DATEADD(TODAY(), -24, 'hours'))`. Returns empty array if no matches — does not error.

#### `slack:CreateAMessage` v4
- **Type:** Action
- **Use:** Send a message to a Slack channel or DM
- **Required parameters:** `connection`, `channelId`, `text`
- **Optional parameters:** `blocks` (Block Kit JSON for rich formatting)
- **Used in:** M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION
- **Notes:** Use v4 for Block Kit support. channelId accepts both channel ID (C0XXXXXXXXX) and user ID (U0XXXXXXXXX) for DMs. For user DMs, pass the user's member ID as channelId.

#### `gmail:ActionSendEmail` v1
- **Type:** Action
- **Use:** Send an email via Gmail
- **Required parameters:** `connection`, `to`, `subject`, `bodyType`, `body`
- **Optional parameters:** `from` (requires send-as permission), `cc`, `bcc`
- **Used in:** M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION
- **Notes:** OAuth connection must have Gmail send permissions. For `hello@shesaidsail.com`, the Google Workspace admin must grant send-as access to the authenticating account, or authenticate as hello@ directly.

#### `gateway:WebhookRespond` v1
- **Type:** Action
- **Use:** Return an HTTP response to the webhook caller
- **Required parameters:** `status` (HTTP status code), `body` (response body string)
- **Optional parameters:** `headers`
- **Used in:** M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BRAND-ROUTER, M-LEAD-INTAKE, M-BOOKING-CREATION
- **Notes:** Must be reached for the webhook caller to receive a response. If the scenario errors before reaching this module, the caller waits until timeout. For Stripe webhooks: CRITICAL — Stripe requires 200 response within 30 seconds or it will retry the event.

---

### Utility Modules

#### `builtin:BasicFeeder` v1
- **Type:** Utility
- **Use:** Transform and compute values without making external calls
- **Required parameters:** `value` (array of objects with computed fields)
- **Used in:** All 8 scenarios
- **Notes:** Use as a data transformation step to compute derived values (deposit amounts, formatted dates, conditional routing) before passing to action modules. Can also serve as a conditional gate when used with filters.

#### `json:ParseJSON` v1
- **Type:** Utility
- **Use:** Parse a JSON string into a structured object accessible by later modules
- **Required parameters:** `json` (string containing valid JSON)
- **Used in:** M-BRAND-ROUTER, M-LEAD-INTAKE (parsing brand router response), M-STRIPE-DEPOSIT (parsing Stripe API response)
- **Notes:** If input is not valid JSON, the module errors. Wrap in error handling if the source is an external HTTP response.

#### `http:ActionSendData` v3
- **Type:** Action (HTTP)
- **Use:** Make an arbitrary HTTP request to any URL
- **Required parameters:** `url`, `method`, `headers`, `bodyType`, `body`
- **Used in:** All scenarios for internal Make-to-Make webhook calls; M-STRIPE-DEPOSIT for Stripe API
- **Notes:** v3 for best header support. For Stripe, set `Content-Type: application/x-www-form-urlencoded` and format body as URL-encoded key-value pairs. For internal Make webhooks, use `Content-Type: application/json` with raw JSON body.

---

## DEPRECATED MODULES — DO NOT USE

| Module | Reason | Replacement |
|--------|--------|-------------|
| `stripe:ActionCreatePaymentLink` | Stripe API 2019-02-11. Missing metadata support, idempotency-key, and current webhook schema compatibility. | `http:ActionSendData` → `https://api.stripe.com/v1/payment_links` with `Stripe-Version: 2023-10-16` |
| `airtable:ActionCreateRecord` v1 | Deprecated. Field mapping schema changed in v3. | `airtable:ActionCreateRecord` v3 |
| `airtable:ActionUpdateRecord` v1 | Deprecated. | `airtable:ActionUpdateRecord` v3 |
| `slack:CreateAMessage` v1-v3 | No Block Kit support. | `slack:CreateAMessage` v4 |

---

## MAKE FORMULA REFERENCE

Formulas used in Stage 1 blueprints:

| Formula | Description | Example |
|---------|-------------|---------|
| `uuid()` | Generate a UUID v4 | `{{uuid()}}` |
| `now` | Current datetime | `{{now}}` |
| `formatDate(date; format)` | Format a date | `{{formatDate(now; "YYYY-MM-DDTHH:mm:ssZ")}}` |
| `ifempty(value; fallback)` | Return fallback if value is empty | `{{ifempty(1.body.phone; "")}}` |
| `if(condition; true; false)` | Conditional | `{{if(2.hv_client; "HV"; "Standard")}}` |
| `contains(string; substring)` | Check if string contains substring | `{{contains(2.raw_source; "mare")}}` |
| `lower(string)` | Lowercase a string | `{{lower(1.body.email)}}` |
| `length(array)` | Count items in array | `{{length(4.records)}}` |
| `round(number)` | Round to integer | `{{round(1.Package_Price * 0.5 * 100)}}` |
| `formatNumber(n; decimals; dec_sep; tho_sep)` | Format number | `{{formatNumber(2.amount; 2; "."; ",")}}` |
| `addDays(date; days)` | Add days to date | `{{addDays(1.Charter_Date; -3)}}` |
| `split(string; delimiter)[index]` | Split string and pick element | `{{split(1.Client_Name; " ")[1]}}` |

---

## MAKE FILTER REFERENCE

Operators used in Stage 1 blueprint filters:

| Operator | Description |
|----------|-------------|
| `text:equal` | String equality |
| `text:notequal` | String not equal |
| `boolean:equal` | Boolean equality (use "true"/"false" as values) |
| `boolean:notequal` | Boolean not equal |
| `number:equal` | Numeric equality |

---

*She Said Sail · Make Native Module Reference Master*  
*CONFIDENTIAL — INTERNAL USE ONLY*
