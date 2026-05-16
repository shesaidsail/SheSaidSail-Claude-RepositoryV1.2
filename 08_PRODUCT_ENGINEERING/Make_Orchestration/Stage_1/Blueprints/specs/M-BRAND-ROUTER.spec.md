# M-BRAND-ROUTER — Scenario Spec

**Scenario ID:** M-BRAND-ROUTER
**Version:** 1.0.0
**Last Updated:** 2026-05-16
**Author:** She Said Sail / Mare Executive Engineering
**Airtable Base:** appdZ49WqgjRXxA1R
**Zone:** us1.make.com

---

## Overview

M-BRAND-ROUTER is the top-level dispatcher for all inbound events entering the She Said Sail / Mare Executive Make.com automation stack. It accepts raw payloads from external sources (Webflow form hooks, API integrations, Zapier bridges, or manual test calls), determines which brand the lead belongs to (SSS or ME), sets brand-specific configuration variables, and forwards an enriched payload to M-LEAD-INTAKE for downstream processing.

After routing, it fires an audit event to M-AUDIT-LOGGER to record the routing decision in the immutable audit trail.

**Key responsibilities:**
- Accept inbound events via instant webhook
- Inspect the `brand` field and route to the correct brand path (SSS or ME)
- Set brand-specific configuration variables (email, Slack channel, Airtable table references)
- HTTP POST the enriched payload to M-LEAD-INTAKE
- HTTP POST an audit event to M-AUDIT-LOGGER
- Alert `#sss-ops-alerts` on Slack if any module fails

---

## Trigger

**Type:** Instant webhook (`gateway:CustomWebHook`)
**Hook ID:** `GENERATED_BY_MAKE_AFTER_IMPORT` — must be replaced after scenario import
**Method:** POST
**Content-Type:** application/json

### Expected Inbound Payload Schema

```json
{
  "brand":        "string — SSS | ME",
  "source":       "string — origin of the event (e.g. webflow-form, api, manual)",
  "lead_data":    "object — freeform lead details (name, email, dates, yacht, message, etc.)",
  "timestamp":    "string — ISO 8601 UTC timestamp of when the event was generated",
  "environment":  "string — production | staging | test"
}
```

---

## Module Flow

| # | Module | Type | Description |
|---|--------|------|-------------|
| 1 | Webhook Trigger | `gateway:CustomWebHook` | Receives raw inbound event JSON |
| 2 | Brand Router | `builtin:BasicRouter` | Splits flow into SSS path (Route 1) and ME path (Route 2) |
| 3 | Set SSS Config | `builtin:SetVariable` | Sets brand_config variable for She Said Sail (Route 1) |
| 4 | POST to M-LEAD-INTAKE (SSS) | `http:ActionSendData` | Forwards enriched payload to M-LEAD-INTAKE webhook (Route 1) |
| 5 | Set ME Config | `builtin:SetVariable` | Sets brand_config variable for Mare Executive (Route 2) |
| 6 | POST to M-LEAD-INTAKE (ME) | `http:ActionSendData` | Forwards enriched payload to M-LEAD-INTAKE webhook (Route 2) |
| 7 | POST to M-AUDIT-LOGGER | `http:ActionSendData` | Fires audit event recording the routing decision (runs after router) |
| 8 | Slack Error Alert | `slack:ActionPostMessage` | Fires only on upstream module failure — posts to `#sss-ops-alerts` |

---

## Router Routes

### Route 1 — "SSS Brand"

**Filter condition:** `{{1.brand}} = "SSS"` (text:equal)

**Actions:**
1. SetVariable `brand_config` (module 3) — populates SSS-specific values
2. HTTP POST to M-LEAD-INTAKE (module 4) — merges webhook body with brand_config

**Body sent to M-LEAD-INTAKE:**
```
{{toJSON(mergeCollections(1, map(3, 'brand_config')))}}
```
This merges all fields from the webhook trigger (module 1) with the brand_config object (module 3), producing a single enriched object.

### Route 2 — "ME Brand"

**Filter condition:** `{{1.brand}} = "ME"` (text:equal)

**Actions:**
1. SetVariable `brand_config` (module 5) — populates ME-specific values
2. HTTP POST to M-LEAD-INTAKE (module 6) — merges webhook body with brand_config

---

## Brand Config Variables

### SSS — She Said Sail

| Variable | Value |
|----------|-------|
| `brand_name` | `She Said Sail` |
| `brand_email` | `hello@shesaidsail.com` |
| `brand_slack_channel` | `#sss-leads` |
| `airtable_base` | `appdZ49WqgjRXxA1R` |
| `package_table` | `tblwDw2hkKW5moSr9` |

### ME — Mare Executive

| Variable | Value |
|----------|-------|
| `brand_name` | `Mare Executive` |
| `brand_email` | `hello@mareexecutive.com` |
| `brand_slack_channel` | `#me-leads` |
| `airtable_base` | `appdZ49WqgjRXxA1R` |
| `package_table` | `tblwDw2hkKW5moSr9` |

---

## Audit Event (Module 7)

Module 7 fires after the router completes, regardless of which route was taken. It posts the following structured JSON to M-AUDIT-LOGGER:

| Field | Value |
|-------|-------|
| `scenario_id` | `M-BRAND-ROUTER` (hardcoded) |
| `event_type` | `BRAND_ROUTED` (hardcoded) |
| `brand` | `{{1.brand}}` (from webhook trigger) |
| `record_id` | `""` (empty — no Airtable record yet) |
| `table_name` | `""` (empty at this stage) |
| `action` | `ROUTED_TO_LEAD_INTAKE` (hardcoded) |
| `actor` | `make-automation` (hardcoded) |
| `timestamp` | `{{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}` |
| `payload` | `{ source, lead_data }` from trigger |
| `environment` | `{{1.environment}}` |
| `idempotency_key` | `M-BRAND-ROUTER-{brand}-{YYYYMMDDHHmmss}-{source}` |

---

## Error Handling

Module 8 (`slack:ActionPostMessage`) is a downstream error-handler. It is attached to the scenario error-handler route in Make and fires when any upstream module throws an unhandled error.

**Alert fields in Slack message:**
- Scenario name (M-BRAND-ROUTER)
- Error message and module that failed
- Brand received
- Source
- Environment
- Timestamp

**Channel:** `#sss-ops-alerts`

**Note:** The Slack error module itself does NOT have an error handler to avoid infinite loops.

---

## Idempotency Logic

M-BRAND-ROUTER does not perform its own idempotency check. It delegates deduplication responsibility to:
- **M-LEAD-INTAKE** — for the lead record creation/update
- **M-AUDIT-LOGGER** — for the audit event write (using `idempotency_key`)

The `idempotency_key` generated in module 7's body is constructed from scenario ID, brand, timestamp (seconds resolution), and source — providing natural deduplication for audit events without a pre-flight search.

---

## Placeholders to Rebind After Import

| Placeholder | Location | What to Replace With |
|-------------|----------|----------------------|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 (webhook hook ID) | The webhook hook ID auto-assigned by Make after you create and save the hook |
| `RECONNECT_SLACK_CONNECTION` | Module 8 (Slack) | Your live Slack OAuth connection in Make |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` | Modules 4 & 6 (HTTP POST to M-LEAD-INTAKE) | The webhook URL of the live M-LEAD-INTAKE scenario |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` | Module 7 (HTTP POST to M-AUDIT-LOGGER) | The webhook URL of the live M-AUDIT-LOGGER scenario |

**Important:** Modules 4/6 and module 7 each use `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` as a placeholder but must be replaced with **different** URLs after import:
- Modules 4 & 6 → M-LEAD-INTAKE webhook URL
- Module 7 → M-AUDIT-LOGGER webhook URL

---

## Test Steps

1. Copy the test payload from `test_payloads/M-BRAND-ROUTER.test.json`.
2. Activate the scenario in Make (set to ON, instant trigger).
3. Copy the webhook URL from the trigger module (module 1).
4. POST the SSS test payload to the webhook URL:
   ```bash
   curl -X POST "https://hook.us1.make.com/<YOUR_HOOK_ID>" \
     -H "Content-Type: application/json" \
     -d @M-BRAND-ROUTER.test.json
   ```
5. Verify in Make's execution history that:
   - Route 1 (SSS Brand) executed
   - Module 3 SetVariable has `brand_name = "She Said Sail"`
   - Module 4 HTTP POST returned 200 (M-LEAD-INTAKE accepted it)
   - Module 7 HTTP POST returned 200 (M-AUDIT-LOGGER accepted it)
6. Repeat with the ME variant payload (`brand: "ME"`) — confirm Route 2 executes and `brand_name = "Mare Executive"`.
7. POST a payload with `brand: "UNKNOWN"` — confirm neither route fires, scenario still completes, and no Slack alert fires (this is expected — unrecognised brands are silently dropped at the router; add an else route later if needed).
8. Simulate an error (e.g. use an invalid M-LEAD-INTAKE URL in module 4) — confirm a Slack alert appears in `#sss-ops-alerts` with the error details.
9. Check the Airtable Audit Log (`tblrMpTfMk8q1eNHp`) for a new record with `Scenario_ID = "M-BRAND-ROUTER"` and `Event_Type = "BRAND_ROUTED"`.
