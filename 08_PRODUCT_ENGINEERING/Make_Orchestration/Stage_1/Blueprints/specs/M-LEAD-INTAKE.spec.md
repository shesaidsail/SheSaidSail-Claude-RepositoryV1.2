# M-LEAD-INTAKE — Scenario Specification

**Scenario ID:** M-LEAD-INTAKE
**Version:** 1.1
**Status:** Ready for Import
**Last Updated:** 2026-05-16
**Zone:** us1.make.com
**Brands:** She Said Sail (SSS) | Mare Executive (ME)

---

## Overview

M-LEAD-INTAKE is the entry point for all new lead data entering the She Said Sail / Mare Executive automation stack. It accepts enriched lead payloads from upstream sources (Webflow form submissions, M-BRAND-ROUTER, or direct API calls), performs an idempotency/duplicate check against Airtable, and either creates a new Request record or updates an existing open record. It then fires downstream calls to M-AUDIT-LOGGER and M-SLACK-ALERTS.

**Key behaviors:**
- Idempotency check on email + open status before creating any record
- New leads: full record creation with Status=NEW and Agent_Status=HUMAN_REVIEW
- Duplicate leads: append notes, update timestamps only — no second record created
- All outcomes logged to M-AUDIT-LOGGER; lead alerts dispatched to M-SLACK-ALERTS

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-LEAD-INTAKE Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | None (internal Make-to-Make calls; secure by URL obscurity) |
| Method | POST |
| Content-Type | application/json |

---

## Incoming Payload Schema

```json
{
  "brand": "SSS | MARE_EXECUTIVE",
  "source": "Webflow | Manual | API",
  "lead_data": {
    "first_name": "string",
    "last_name": "string",
    "email": "string (required — primary idempotency key)",
    "phone": "string",
    "city": "string",
    "date_requested": "ISO 8601 date string (e.g. 2026-07-15)",
    "party_size": "integer or string",
    "budget_range": "string (e.g. '$5,000–$10,000')",
    "notes": "string",
    "package_interest": "string"
  },
  "timestamp": "ISO 8601 datetime string",
  "environment": "production | staging | development",
  "idempotency_key": "string (UUID or deterministic hash)"
}
```

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the POST payload. All top-level fields are available downstream via `{{1.*}}`. Nested fields under `lead_data` are accessed as `{{1.lead_data.*}}`.

---

### Module 2 — Airtable SearchRecords (Duplicate / Idempotency Check)

| Property | Value |
|---|---|
| Module type | `airtable:SearchRecords` |
| Base | `appdZ49WqgjRXxA1R` |
| Table | Requests (`tblTlSB9CO4dTGodg`) |
| Filter formula | `AND({Email} = '{{1.lead_data.email}}', {Status} != 'CLOSED')` |
| Max records | 5 |
| Fields returned | Email, Status, Notes, Record_ID |
| Output | `{{2.records}}` — array, may be empty |

**Purpose:** Identifies any open (non-CLOSED) Request record for the submitted email address before creating a new one. If one or more records are found, the duplicate route fires.

---

### Module 3 — Router (`builtin:BasicRouter`)

Branches on `length(2.records)`:
- **Route 1 "New Lead"** — fires when `length(2.records) = 0`
- **Route 2 "Duplicate Lead"** — fires when `length(2.records) > 0`

---

## Route 1 — New Lead (Modules 4, 5, 6)

**Filter:** `{{length(2.records)}} = 0` (number:equal)

### Module 4 — Airtable ActionCreateRecord

| Property | Value |
|---|---|
| Module type | `airtable:ActionCreateRecord` |
| Base | `appdZ49WqgjRXxA1R` |
| Table | Requests (`tblTlSB9CO4dTGodg`) |

#### Field Mappings

| Airtable Field | Source Value |
|---|---|
| First_Name | `{{1.lead_data.first_name}}` |
| Last_Name | `{{1.lead_data.last_name}}` |
| Email | `{{1.lead_data.email}}` |
| Phone | `{{1.lead_data.phone}}` |
| City | `{{1.lead_data.city}}` |
| Date_Requested | `{{1.lead_data.date_requested}}` |
| Party_Size | `{{1.lead_data.party_size}}` |
| Budget_Range | `{{1.lead_data.budget_range}}` |
| Notes | `{{1.lead_data.notes}}` |
| Package_Interest | `{{1.lead_data.package_interest}}` |
| Brand | `{{1.brand}}` |
| Source_System | `{{1.source}}` |
| Status | `NEW` (hardcoded) |
| Environment | `{{1.environment}}` |
| Created_At | `{{1.timestamp}}` |
| Agent_Status | `HUMAN_REVIEW` (hardcoded) |
| Idempotency_Key | `{{1.idempotency_key}}` |

### Module 5 — HTTP POST to M-AUDIT-LOGGER

| Property | Value |
|---|---|
| Module type | `http:ActionSendData` |
| URL | INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER webhook) |
| Method | POST |
| handleErrors | false (non-blocking) |

**Payload fields:** scenario_id=`M-LEAD-INTAKE`, event_type=`LEAD_CREATED`, brand, record_id (`{{4.id}}`), email, timestamp, environment, idempotency_key

### Module 6 — HTTP POST to M-SLACK-ALERTS

| Property | Value |
|---|---|
| Module type | `http:ActionSendData` |
| URL | INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-SLACK-ALERTS webhook) |
| Method | POST |
| handleErrors | false (non-blocking) |

**Payload fields:** alert_type=`NEW_LEAD`, brand, record_id (`{{4.id}}`), urgency=`MEDIUM`, message, timestamp, metadata (lead_name, city, date_requested, budget_range, package_interest, source, environment, party_size)

---

## Route 2 — Duplicate Lead (Modules 7, 8, 9)

**Filter:** `{{length(2.records)}} > 0` (number:greater)

### Module 7 — Airtable ActionUpdateRecord

| Property | Value |
|---|---|
| Module type | `airtable:ActionUpdateRecord` |
| Base | `appdZ49WqgjRXxA1R` |
| Table | Requests (`tblTlSB9CO4dTGodg`) |
| Record ID | `{{2.records[].id}}` (first matching record) |

#### Field Updates

| Airtable Field | Value |
|---|---|
| Updated_At | `{{1.timestamp}}` |
| Source_System | `{{1.source}}` |
| Notes | Appends: `[Re-submitted {{1.timestamp}} via {{1.source}}]: {{1.lead_data.notes}}` to existing Notes |

### Module 8 — HTTP POST to M-AUDIT-LOGGER

**Payload fields:** scenario_id=`M-LEAD-INTAKE`, event_type=`LEAD_DUPLICATE`, brand, record_id (`{{2.records[].id}}`), email, timestamp, environment, idempotency_key, duplicate_source

### Module 9 — HTTP POST to M-SLACK-ALERTS

**Payload fields:** alert_type=`NEW_LEAD`, brand, record_id (`{{2.records[].id}}`), urgency=`LOW`, message (indicates duplicate), timestamp, metadata (includes `"duplicate": true`)

---

## Idempotency

Duplicate detection uses the combination of **email address** and **open status** (`Status != CLOSED`). If a record exists with the same email and is not CLOSED, the scenario updates rather than creates. The `Idempotency_Key` field on the Airtable record allows tracing which specific payload created or last updated a record.

> Note: This is email-based idempotency. Two submissions from different email addresses for the same person will produce two records. Future enhancement: add secondary phone-number check or a deterministic composite hash key.

---

## Error Handling

| Condition | Behavior |
|---|---|
| Transient Airtable failure (module 2 or 4/7) | Make retries up to `maxErrors: 3`; autoCommit re-runs scenario |
| HTTP call failure (modules 5, 6, 8, 9) | `handleErrors: false` — failure is logged by Make but does not break the core record creation/update flow |
| Scenario-level failure before the router | No downstream notifications fire. Recommended future enhancement: add an error-handler route that calls M-AUDIT-LOGGER with SCENARIO_ERROR |

---

## Placeholders to Rebind After Import

| Placeholder | Module(s) | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook hook ID | Make auto-assigns on import; copy the generated webhook URL for use by callers |
| `RECONNECT_AIRTABLE_CONNECTION` | Modules 2, 4, 7 | Select the saved Airtable connection for base `appdZ49WqgjRXxA1R` |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×2, audit) | Modules 5, 8 — HTTP URL | Paste the live webhook URL for M-AUDIT-LOGGER |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (×2, slack) | Modules 6, 9 — HTTP URL | Paste the live webhook URL for M-SLACK-ALERTS |

---

## Test Steps

1. Deploy scenario in Make (us1.make.com) and copy the generated webhook URL.
2. Send `scenario_new_lead` payload from `M-LEAD-INTAKE.test.json` via curl or Postman.
3. Verify a new record appears in Airtable Requests table with:
   - Status = `NEW`
   - Agent_Status = `HUMAN_REVIEW`
   - All lead_data fields populated correctly
4. Verify M-AUDIT-LOGGER receives a `LEAD_CREATED` event with the correct `record_id`.
5. Verify M-SLACK-ALERTS receives a `NEW_LEAD` alert with urgency `MEDIUM`.
6. Check `#sss-leads` (or `#me-leads` for MARE_EXECUTIVE brand) in Slack for the formatted message.
7. Re-send the same payload (identical email address).
8. Verify no second record is created; existing record's `Notes` and `Updated_At` are updated.
9. Verify M-AUDIT-LOGGER receives a `LEAD_DUPLICATE` event.
10. Verify M-SLACK-ALERTS receives a `NEW_LEAD` alert with urgency `LOW` and `"duplicate": true` in metadata.
11. Send `scenario_duplicate_lead` payload from `M-LEAD-INTAKE.test.json` to explicitly test the duplicate route.
12. Test with `"environment": "staging"` to confirm the Environment field is written correctly.
13. Test with `"brand": "MARE_EXECUTIVE"` to confirm the Slack alert routes to `#me-leads`.
