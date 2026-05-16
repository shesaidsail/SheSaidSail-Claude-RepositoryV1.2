# M-CONCIERGE-ASSIGNMENT — Scenario Specification

**Scenario ID:** M-CONCIERGE-ASSIGNMENT  
**Version:** 1.0  
**Status:** Ready for Import  
**Last Updated:** 2026-05-16  
**Zone:** us1.make.com  
**Airtable Base:** appdZ49WqgjRXxA1R  

---

## Overview

M-CONCIERGE-ASSIGNMENT fires when a charter Request reaches the `AVAILABILITY_CONFIRMED` status — meaning capacity has been verified and a concierge operator must now be assigned. It searches the Concierge_Operators table for the first available, active concierge matching the request's city and brand, then assigns them and notifies them via Slack and email. If no concierge is found, it flags the Request for manual ops intervention and fires a HIGH-urgency Slack alert. All outcomes are posted to M-AUDIT-LOGGER.

**Upstream trigger:** Airtable automation or another Make scenario (e.g. M-BRAND-ROUTER or an availability-check scenario) POSTs to this scenario's webhook when `Request.Status` changes to `AVAILABILITY_CONFIRMED`.

**Downstream scenarios called:** M-SLACK-ALERTS (modules 6, 9), M-AUDIT-LOGGER (module 10), Gmail (module 7).

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-CONCIERGE-ASSIGNMENT Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | None (internal Make-to-Make calls; secured by URL obscurity) |
| Method | POST |
| Content-Type | application/json |

---

## Incoming Payload Schema

```json
{
  "request_id": "string — Airtable Record ID from Requests table (e.g. recXXXXXXXXXXXXXX)",
  "brand": "string — SSS | MARE_EXECUTIVE",
  "city": "string — MIA | TPA | CHS",
  "date_requested": "string — ISO 8601 date or human-readable date (e.g. 2026-07-04)",
  "client_name": "string — full name of the client",
  "package_interest": "string — name of the package the client is interested in",
  "environment": "string — production | staging | development"
}
```

All fields are required. Missing `request_id` will cause module 2 to fail and trigger the error handler.

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the POST payload. All fields are available downstream via `{{1.*}}` references (e.g. `{{1.request_id}}`, `{{1.city}}`).

### Module 2 — Airtable ActionGetRecord (`airtable:ActionGetRecord`)
- **Table:** Requests (`tblTlSB9CO4dTGodg`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Record ID:** `{{1.request_id}}`
- **Purpose:** Retrieves the full Request record to verify current status and access all fields. Downstream modules can reference `{{2.fields.*}}` for fields not in the webhook payload.
- **Error behavior:** If the record ID is invalid, Make throws an error that routes to the error handler (modules 11–12).

### Module 3 — Airtable SearchRecords (`airtable:SearchRecords`)
- **Table:** Concierge_Operators (`CONCIERGE_OPERATORS_TABLE_ID`)
- **Base:** `appdZ49WqgjRXxA1R`
- **Filter formula:** `AND({City} = '{{1.city}}', {Brand} = '{{1.brand}}', {Status} = 'ACTIVE', {Available} = TRUE())`
- **Max records:** 1
- **Fields returned:** Name, Email, City, Brand, Status, Available, Phone
- **Purpose:** Find the first eligible concierge. Returns `{{3.records}}` — an array (empty if none found). `first(3.records)` accesses the matched operator.

### Module 4 — Router (`builtin:BasicRouter`)
Evaluates `length(3.records)` to branch execution.

---

#### Route 1 — "Concierge Found" (modules 5, 6, 7)
**Filter condition:** `{{length(3.records)}} > 0`

**Module 5 — Airtable ActionUpdateRecord**
Updates the Request record with the assigned concierge.

| Field | Value |
|---|---|
| `Assigned_Concierge` | `["{{first(3.records).id}}"]` — linked record array |
| `Status` | `CONCIERGE_ASSIGNED` (hardcoded) |
| `Assigned_At` | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}` |

**Module 6 — HTTP POST to M-SLACK-ALERTS**
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-SLACK-ALERTS webhook)
- **alert_type:** `CONCIERGE_ASSIGNED`
- **urgency:** `LOW`
- **message:** `"Concierge {Name} assigned to {client_name} for {date_requested} in {city}"`
- **metadata:** request_id, concierge_id, concierge_name, concierge_email, city, package_interest, date_requested, environment

**Module 7 — Gmail ActionSendEmail (`gmail:ActionSendEmail`)**
- **To:** `{{first(3.records).fields.Email}}` (concierge's email)
- **Subject:** `New Assignment - {client_name} | {date_requested}`
- **Body (HTML):** Assignment notification with client details, request ID, date, city, brand, package interest, and Airtable link prompt. Includes 2-hour follow-up SLA reminder.
- **Connection:** RECONNECT_GMAIL_CONNECTION

---

#### Route 2 — "No Concierge Available" (modules 8, 9)
**Filter condition:** `{{length(3.records)}} = 0`

**Module 8 — Airtable ActionUpdateRecord**
Updates the Request record to flag for manual ops intervention.

| Field | Value |
|---|---|
| `Status` | `NEEDS_MANUAL_ASSIGNMENT` (hardcoded) |

**Module 9 — HTTP POST to M-SLACK-ALERTS**
- **URL:** INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-SLACK-ALERTS webhook)
- **alert_type:** `AUTOMATION_ERROR`
- **urgency:** `HIGH`
- **message:** `"No concierge available for {city} {brand} on {date_requested}. Manual assignment required."`
- **metadata:** request_id, client_name, city, brand, date_requested, package_interest, environment

---

### Module 10 — HTTP POST to M-AUDIT-LOGGER (`http:ActionSendData`)
Runs after the Router regardless of which route was taken.

| Payload Field | Value |
|---|---|
| `scenario_id` | `M-CONCIERGE-ASSIGNMENT` |
| `event_type` | `CONCIERGE_ASSIGNED` or `ASSIGNMENT_FAILED` (conditional on `length(3.records) > 0`) |
| `brand` | `{{1.brand}}` |
| `record_id` | `{{1.request_id}}` |
| `table_name` | `Requests` |
| `action` | `CONCIERGE_ASSIGNED` or `NEEDS_MANUAL_ASSIGNMENT` |
| `actor` | `make-automation` |
| `timestamp` | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}` |
| `payload` | city, client_name, date_requested, package_interest, concierge_found (bool), concierge_id, concierge_name |
| `environment` | `{{1.environment}}` |
| `idempotency_key` | `M-CONCIERGE-ASSIGNMENT-{request_id}-{YYYYMMDDHHmmss}` |

---

### Modules 11–12 — Error Handler
Fire only when `{{error}}` is non-empty (i.e., any upstream module threw an unhandled error).

**Module 11 — HTTP POST to M-AUDIT-LOGGER**
- **event_type:** `SCENARIO_ERROR`
- **payload:** error_message, error_module, city, client_name, date_requested
- **idempotency_key:** `M-CONCIERGE-ASSIGNMENT-ERR-{request_id}-{YYYYMMDDHHmmss}`

**Module 12 — Slack ActionPostMessage (`slack:ActionPostMessage`)**
- **Channel:** `#sss-ops-alerts`
- **Text:** Formatted error message with brand, request_id, client, city, date, error details, environment, and a manual review callout.
- **Connection:** RECONNECT_SLACK_CONNECTION

---

## Field Mappings Summary

| Source | Airtable Field | Table | Module |
|---|---|---|---|
| `{{1.request_id}}` | record ID (get) | Requests | 2 |
| `{{1.city}}` + `{{1.brand}}` | filter fields | Concierge_Operators | 3 |
| `{{first(3.records).id}}` | Assigned_Concierge (linked record) | Requests | 5 |
| `CONCIERGE_ASSIGNED` | Status | Requests | 5 |
| `now()` | Assigned_At | Requests | 5 |
| `NEEDS_MANUAL_ASSIGNMENT` | Status | Requests | 8 |
| `{{first(3.records).fields.Email}}` | Gmail `to` field | — | 7 |
| `{{first(3.records).fields.Name}}` | Gmail subject + body | — | 7 |

---

## Error Handling

| Failure Point | Behavior |
|---|---|
| Module 2 (Airtable Get) fails | Error handler fires (modules 11–12). Airtable record not updated. |
| Module 3 (Airtable Search) fails | Error handler fires (modules 11–12). |
| Module 5 (Airtable Update — Route 1) fails | Error handler fires. Concierge notification not sent. |
| Module 7 (Gmail) fails | Non-critical: `handleErrors: false` on HTTP calls — audit and Slack still fire. Gmail errors should be monitored separately. |
| Module 6 or 9 (HTTP to M-SLACK-ALERTS) fails | `handleErrors: false` — does not interrupt flow. |
| Module 10 (HTTP to M-AUDIT-LOGGER) fails | `handleErrors: false` — does not interrupt flow. |

Make's `maxErrors: 3` and `autoCommit: true` handle transient API rate limits and network failures with up to 3 automatic retries before the scenario errors out.

---

## Idempotency Logic

This scenario does not perform an explicit idempotency check (unlike M-AUDIT-LOGGER). Idempotency is enforced by the upstream caller:

- The Airtable automation or upstream scenario should only trigger this webhook once per `AVAILABILITY_CONFIRMED` transition.
- If the same `request_id` is received twice, the Airtable `ActionUpdateRecord` (module 5) is safe — it will overwrite `Status` and `Assigned_Concierge` with the same values (idempotent write).
- The audit log idempotency key includes a timestamp suffix, so duplicate calls will create separate audit entries. The ops team can identify re-runs via the timestamp.

**Future enhancement:** Add a module 2a that checks if `Assigned_Concierge` is already populated on the Request — if so, skip the assignment (true idempotency guard).

---

## Placeholders to Rebind After Import

| Placeholder | Location | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook ID | Make auto-assigns on import. Copy the generated URL and share with Airtable automation team. |
| `RECONNECT_AIRTABLE_CONNECTION` | Modules 2, 3, 5, 8 | Select the Airtable OAuth connection for base `appdZ49WqgjRXxA1R`. |
| `CONCIERGE_OPERATORS_TABLE_ID` | Module 3 — table parameter | Replace with the real Airtable table ID for Concierge_Operators (format: `tblXXXXXXXXXXXXXX`). |
| `RECONNECT_GMAIL_CONNECTION` | Module 7 | Select the Gmail OAuth connection for the She Said Sail ops email account. |
| `RECONNECT_SLACK_CONNECTION` | Module 12 | Select the Slack OAuth connection. |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×3) | Modules 6, 9, 10 | Module 6 and 9: paste the live M-SLACK-ALERTS webhook URL. Module 10: paste the live M-AUDIT-LOGGER webhook URL. |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×1) | Module 11 | Paste the live M-AUDIT-LOGGER webhook URL (same as module 10). |

---

## Test Steps

1. Deploy scenario in Make, set to ON (instant trigger), copy the generated webhook URL.
2. Confirm M-SLACK-ALERTS and M-AUDIT-LOGGER are also ON with their webhook URLs ready.
3. **Test A — Concierge Found (Miami, SSS):**
   - Ensure at least one Concierge_Operators record exists with `City=MIA`, `Brand=SSS`, `Status=ACTIVE`, `Available=true`.
   - POST `M-CONCIERGE-ASSIGNMENT.test.json` (payload A) to the webhook URL.
   - Verify: Requests record `recTEST001` has `Status=CONCIERGE_ASSIGNED`, `Assigned_Concierge` populated, `Assigned_At` timestamp set.
   - Verify: Concierge receives assignment email.
   - Verify: M-SLACK-ALERTS fires `CONCIERGE_ASSIGNED` alert (LOW urgency).
   - Verify: M-AUDIT-LOGGER receives `CONCIERGE_ASSIGNED` event.
4. **Test B — No Concierge Available:**
   - Temporarily set all MIA/SSS concierge records to `Available=false` or use a city with no active concierges.
   - POST payload B (use `city: "TPA"` if no TPA concierge exists) to the webhook URL.
   - Verify: Requests record has `Status=NEEDS_MANUAL_ASSIGNMENT`.
   - Verify: M-SLACK-ALERTS fires `AUTOMATION_ERROR` alert (HIGH urgency).
   - Verify: M-AUDIT-LOGGER receives `ASSIGNMENT_FAILED` event.
5. **Test C — Invalid Request ID:**
   - POST a payload with a bogus `request_id` (e.g. `"recINVALID"`).
   - Verify: Error handler fires — M-AUDIT-LOGGER receives `SCENARIO_ERROR` event.
   - Verify: Slack `#sss-ops-alerts` receives an error alert.
6. **Test D — Mare Executive brand:**
   - POST payload with `brand: "MARE_EXECUTIVE"` and a city where a MARE_EXECUTIVE concierge exists.
   - Verify: Brand-correct concierge is assigned (not a SSS concierge).
7. Check Airtable Audit Log table after each test to confirm entries are written with correct `idempotency_key` values.
