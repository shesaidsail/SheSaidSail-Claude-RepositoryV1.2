# M-AUDIT-LOGGER — Scenario Spec

**Scenario ID:** M-AUDIT-LOGGER
**Version:** 1.0.0
**Last Updated:** 2026-05-16
**Author:** She Said Sail / Mare Executive Engineering
**Airtable Base:** appdZ49WqgjRXxA1R

---

## Overview

M-AUDIT-LOGGER is the central audit sink for the entire Make.com automation stack. Every other scenario in the SSS/ME pipeline calls this scenario via HTTP POST to record immutable audit events. It also maintains the Automation_Health table so the ops team can monitor the live/error status of each scenario without opening Make.

**Key responsibilities:**
- Accept a structured audit event payload via webhook
- Perform an idempotency check before writing (prevents duplicate records on retries)
- Write an immutable record to the Airtable Audit Log table
- Update the Automation_Health table when a scenario completes or errors
- Alert #sss-ops-alerts on Slack if any module fails

---

## Trigger

**Type:** Instant webhook (`gateway:CustomWebHook`)
**Hook ID:** `GENERATED_BY_MAKE_AFTER_IMPORT` — must be replaced after scenario import
**Method:** POST
**Content-Type:** application/json

### Expected Inbound Payload Schema

```json
{
  "scenario_id":      "string — Make scenario that fired this event (e.g. M-BRAND-ROUTER)",
  "event_type":       "string — lifecycle event (e.g. BRAND_ROUTED, SCENARIO_COMPLETE, SCENARIO_ERROR)",
  "brand":            "string — SSS | ME",
  "record_id":        "string — Airtable record ID affected (may be empty)",
  "table_name":       "string — Airtable table name affected (may be empty)",
  "action":           "string — short verb describing what happened",
  "actor":            "string — system or user that triggered the action",
  "timestamp":        "string — ISO 8601 UTC timestamp",
  "payload":          "object — freeform context data",
  "environment":      "string — production | staging | test",
  "idempotency_key":  "string — globally unique key for this event (used for dedup)"
}
```

---

## Module Flow

| # | Module | Type | Description |
|---|--------|------|-------------|
| 1 | Webhook Trigger | `gateway:CustomWebHook` | Receives the inbound audit event JSON |
| 2 | Search Audit Log | `airtable:SearchRecords` | Looks up `Idempotency_Key` in Audit Log table — if found, flow skips write |
| 3 | Router | `builtin:BasicRouter` | Splits into Route 1 (write audit) and Route 2 (update health) |
| 4 | Create Audit Record | `airtable:ActionCreateRecord` | Writes the immutable audit record (Route 1, runs only if idempotency check passes) |
| 5 | Search Health Record | `airtable:SearchRecords` | Finds the Automation_Health row matching `scenario_id` (Route 2) |
| 6 | Update Health Record | `airtable:ActionUpdateRecord` | Updates `Last_Run_At`, `Last_Run_Status`, increments `Error_Count` on SCENARIO_ERROR |
| 7 | Slack Error Alert | `slack:ActionPostMessage` | Fires only on upstream module failure — posts to `#sss-ops-alerts` |

---

## Router Routes

### Route 1 — "Write Audit Log"

**Filter condition:** `length(records from module 2) = 0`
(i.e., no existing record with that idempotency_key — safe to write)

**Action:** `airtable:ActionCreateRecord` to table `tblrMpTfMk8q1eNHp`

### Route 2 — "Update Automation Health"

**Filter condition (OR logic):**
- `event_type = "SCENARIO_COMPLETE"` OR
- `event_type = "SCENARIO_ERROR"`

**Action:** Search Automation_Health for matching `scenario_id`, then update that record.
Note: Route 2 executes independently of Route 1. Both routes may execute in the same run if the event qualifies.

---

## Field Mappings

### Audit Log Table (tblrMpTfMk8q1eNHp) — Create Record

| Airtable Field | Source |
|----------------|--------|
| Scenario_ID | `{{1.scenario_id}}` |
| Event_Type | `{{1.event_type}}` |
| Brand | `{{1.brand}}` |
| Record_ID | `{{1.record_id}}` |
| Table_Name | `{{1.table_name}}` |
| Action | `{{1.action}}` |
| Actor | `{{1.actor}}` |
| Timestamp | `{{1.timestamp}}` |
| Payload_JSON | `{{toString(1.payload)}}` — stringified JSON |
| Environment | `{{1.environment}}` |
| Idempotency_Key | `{{1.idempotency_key}}` |
| Source_System | `"Make"` (hardcoded) |

### Automation_Health Table (AUTOMATION_HEALTH_TABLE_ID) — Update Record

| Airtable Field | Source |
|----------------|--------|
| Last_Run_At | `{{1.timestamp}}` |
| Last_Run_Status | `{{1.event_type}}` |
| Error_Count | Increments by 1 if `event_type = SCENARIO_ERROR`, otherwise unchanged |

---

## Idempotency Logic

1. Module 2 searches `tblrMpTfMk8q1eNHp` for any record where `Idempotency_Key = {{1.idempotency_key}}`.
2. If **one or more records are found** (`length(2.records) > 0`): Route 1 filter evaluates to false — the write is skipped. The scenario still returns HTTP 200 (Make's webhook auto-responds).
3. If **no records are found** (`length(2.records) = 0`): Route 1 filter evaluates to true — the audit record is created.
4. Route 2 (health update) is NOT gated by the idempotency check — health updates always fire on SCENARIO_COMPLETE/SCENARIO_ERROR events regardless.

**Idempotency Key convention (recommended):** `{SCENARIO_ID}-{EVENT_TYPE}-{RECORD_ID}-{YYYYMMDD-HHmmss}`

---

## Error Handling

Module 7 (`slack:ActionPostMessage`) is a downstream error-handler. In Make, this is configured by attaching the module to the error-handler route of the scenario. It fires when any upstream module throws an unhandled error.

**Alert fields in Slack message:**
- Scenario name
- Error message and module that failed
- Idempotency key
- Event type
- Brand
- Timestamp

**Channel:** `#sss-ops-alerts`

---

## Placeholders to Rebind After Import

| Placeholder | What to Replace With |
|-------------|----------------------|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | The webhook hook ID auto-assigned by Make after you create the hook |
| `RECONNECT_AIRTABLE_CONNECTION` | Your live Airtable OAuth or API key connection in Make |
| `RECONNECT_SLACK_CONNECTION` | Your live Slack OAuth connection in Make |
| `AUTOMATION_HEALTH_TABLE_ID` | The real Airtable table ID for the Automation_Health table (create it first, then get the ID from Airtable API or URL) |

---

## Test Steps

1. Copy the test payload from `test_payloads/M-AUDIT-LOGGER.test.json`.
2. Activate the scenario in Make (set to ON, instant trigger).
3. Copy the webhook URL from the trigger module.
4. POST the test payload to the webhook URL using curl or Postman:
   ```bash
   curl -X POST "https://hook.us1.make.com/<YOUR_HOOK_ID>" \
     -H "Content-Type: application/json" \
     -d @M-AUDIT-LOGGER.test.json
   ```
5. Verify a new record appears in Airtable Audit Log table (`tblrMpTfMk8q1eNHp`) with all fields populated.
6. POST the same payload a second time (same `idempotency_key`) — confirm no duplicate record is created.
7. POST the `SCENARIO_COMPLETE` variant payload — confirm the Automation_Health row for `M-TEST-SCENARIO` is updated (`Last_Run_At`, `Last_Run_Status`).
8. POST the `SCENARIO_ERROR` variant payload — confirm `Error_Count` increments by 1.
9. Simulate an error (e.g. temporarily invalidate the Airtable connection) and confirm a Slack alert appears in `#sss-ops-alerts`.
