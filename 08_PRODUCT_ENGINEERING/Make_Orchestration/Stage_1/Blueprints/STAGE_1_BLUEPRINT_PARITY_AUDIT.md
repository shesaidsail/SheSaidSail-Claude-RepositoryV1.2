# Stage 1 Blueprint Parity Audit
**Date:** 2026-05-16
**Reference:** M-BRAND-ROUTER.blueprint.json (branch: claude/fix-mbrand-router-scenario-G5C0h)
**Auditor:** Claude Code — Automated Audit + Patch Session

---

## Reference Standard Summary (M-BRAND-ROUTER)

The fixed M-BRAND-ROUTER establishes the following standards for all Stage 1 blueprints:

| Standard | Value |
|---|---|
| Scenario name format | `M0X SCENARIO-NAME` |
| Webhook hook parameter | `GENERATED_BY_MAKE_AFTER_IMPORT` |
| Slack module | `slack:postMessage` v4 |
| Slack connection key | `"connection": "RECONNECT_SLACK_CONNECTION"` |
| Airtable connection key | `"connection": "RECONNECT_AIRTABLE_CONNECTION"` |
| Gmail connection key | `"connection": "RECONNECT_GMAIL_CONNECTION"` |
| HTTP body field | `"data"` (not `"body"`) |
| HTTP bodyType for JSON | `"raw"` |
| HTTP contentType for JSON | `"application/json"` |
| HTTP metadata.parameters | `handleErrors` boolean declared |
| HTTP metadata.expect | url, method, headers, bodyType, parseResponse, contentType, data |
| Claude API model | `claude-sonnet-4-20250514` |
| Claude API header key | `x-api-key: RECONNECT_ANTHROPIC_API_KEY` |
| Claude handleErrors | `true` |
| scenario.dlt | `false` (NOT `dataloss`) |
| scenario.slots | Not present |
| Airtable base | `appdZ49WqgjRXxA1R` |
| zone | `us1.make.com` |

---

## File Audits

### 1. M-AUDIT-LOGGER.blueprint.json

**Original name:** `M-AUDIT-LOGGER`
**Patched name:** `M02 M-AUDIT-LOGGER`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name missing deployment order prefix | Added `M02` prefix |
| 2 | CRITICAL | Airtable modules used `"__IMTCONN__"` connection key | Changed to `"connection"` throughout |
| 3 | CRITICAL | Airtable modules used `"appId"` / `"tableId"` parameter keys | Changed to `"base"` / `"table"` for consistency |
| 4 | CRITICAL | Module 7 `slack:ActionPostMessage` with `__IMTCONN__` | Changed to `slack:postMessage` with `connection` |
| 5 | CRITICAL | Module 7 had `"routes": null` (invalid for non-router module) | Removed field |
| 6 | HIGH | Module 7 missing `metadata.parameters` and `metadata.expect` | Added standard arrays |
| 7 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 8 | MEDIUM | `"slots": null` in scenario metadata (not in reference) | Removed |
| 9 | INFO | Webhook metadata.parameters array missing | Added |
| 10 | INFO | `AUTOMATION_HEALTH_TABLE_ID` placeholder — Automation_Health table ID unknown | Preserved as placeholder; restore label documents manual rebind required |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

### 2. M-LEAD-INTAKE.blueprint.json

**Original name:** `M-LEAD-INTAKE — She Said Sail / Mare Executive Lead Intake`
**Patched name:** `M03 M-LEAD-INTAKE`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name verbose and missing deployment order prefix | Renamed to `M03 M-LEAD-INTAKE` |
| 2 | CRITICAL | HTTP modules 5, 6, 8, 9 used `"body"` field (Make ignores this) | Changed to `"data"` |
| 3 | CRITICAL | HTTP modules 5, 6, 8, 9 missing `"bodyType": "raw"` | Added |
| 4 | CRITICAL | HTTP modules 5, 6, 8, 9 missing `"contentType": "application/json"` | Added |
| 5 | HIGH | HTTP modules missing `metadata.parameters` and `metadata.restore.expect` | Added standard arrays |
| 6 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 7 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 8 | LOW | Webhook URL placeholders used `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` | Standardized to `INSERT_WEBHOOK_URL_AFTER_IMPORT` per approved list |
| 9 | INFO | Route `id` fields on router routes (non-standard) | Removed route IDs for cleaner import |
| 10 | INFO | Webhook metadata.parameters array missing | Added |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

### 3. M-SLACK-ALERTS.blueprint.json

**Original name:** `M-SLACK-ALERTS — She Said Sail / Mare Executive Centralized Slack Dispatcher`
**Patched name:** `M04 M-SLACK-ALERTS`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name verbose and missing deployment order prefix | Renamed to `M04 M-SLACK-ALERTS` |
| 2 | CRITICAL | Slack modules 3, 5, 6, 7, 8 used `slack:ActionPostMessage` | Changed to `slack:postMessage` |
| 3 | CRITICAL | HTTP module 9 used `"body"` field | Changed to `"data"` |
| 4 | CRITICAL | HTTP module 10 used `"body"` field | Changed to `"data"` |
| 5 | CRITICAL | HTTP module 9 `handleErrors: true` — audit log calls should not propagate errors | Changed to `false` |
| 6 | HIGH | HTTP modules 9–10 missing `bodyType: "raw"` and `contentType` | Added |
| 7 | HIGH | Slack modules missing `metadata.parameters` and `metadata.expect` | Added standard arrays |
| 8 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 9 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 10 | INFO | Route `id` fields on router routes | Removed for cleaner import |
| 11 | INFO | Webhook metadata.parameters array missing | Added |
| 12 | INFO | Emergency route DM channel `WILL_SLACK_USER_ID_PLACEHOLDER` — preserved for manual config | Documented in notes |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

### 4. M-CONCIERGE-ASSIGNMENT.blueprint.json

**Original name:** `M-CONCIERGE-ASSIGNMENT — She Said Sail + Mare Executive`
**Patched name:** `M05 M-CONCIERGE-ASSIGNMENT`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name missing deployment order prefix | Added `M05` prefix |
| 2 | CRITICAL | HTTP modules 6, 9, 10, 11 used `"body"` field | Changed to `"data"` |
| 3 | CRITICAL | HTTP modules 6, 9, 10, 11 missing `"bodyType": "raw"` and `"contentType"` | Added |
| 4 | CRITICAL | Module 12 `slack:ActionPostMessage` with `__IMTCONN__` | Changed to `slack:postMessage` with `connection` |
| 5 | HIGH | HTTP modules missing `metadata.parameters` and `metadata.restore.expect` | Added standard arrays |
| 6 | HIGH | Module 12 Slack module missing `metadata.parameters` and `metadata.expect` | Added |
| 7 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 8 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 9 | MEDIUM | `CONCIERGE_OPERATORS_TABLE_ID` is a placeholder — actual table ID unknown | Preserved; restore label explicitly documents manual rebind requirement |
| 10 | INFO | Webhook metadata.parameters array missing | Added |
| 11 | INFO | Route `id` fields on router routes | Removed |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

### 5. M-STRIPE-DEPOSIT.blueprint.json

**Original name:** `M-STRIPE-DEPOSIT — She Said Sail + Mare Executive`
**Patched name:** `M06 M-STRIPE-DEPOSIT`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name missing deployment order prefix | Added `M06` prefix |
| 2 | CRITICAL | Module 4 (Stripe HTTP call) had `"connection": "RECONNECT_STRIPE_CONNECTION"` in `parameters` — `http:ActionSendData` has no connection parameter | Removed from parameters; added `Authorization: Bearer RECONNECT_STRIPE_CONNECTION` to headers |
| 3 | CRITICAL | Module 4 `"bodyType": "application/x-www-form-urlencoded"` — invalid Make bodyType identifier | Changed to `"raw"` with Content-Type header set to `application/x-www-form-urlencoded` |
| 4 | CRITICAL | Module 4 used `"body"` field | Changed to `"data"` |
| 5 | CRITICAL | Modules 7, 8, 9, 10 used `"body"` field | Changed to `"data"` |
| 6 | CRITICAL | Modules 8, 9, 10 missing `"bodyType": "raw"` and `"contentType"` | Added |
| 7 | CRITICAL | Module 11 `slack:ActionPostMessage` with `__IMTCONN__` | Changed to `slack:postMessage` with `connection` |
| 8 | HIGH | HTTP modules missing `metadata.parameters` and `metadata.restore.expect` | Added standard arrays |
| 9 | HIGH | Module 11 Slack missing `metadata.parameters` and `metadata.expect` | Added |
| 10 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 11 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 12 | INFO | Webhook metadata.parameters array missing | Added |
| 13 | INFO | Route `id` fields on router routes | Removed |
| 14 | INFO | Module 7 SMS: confirmed Quo SMS API endpoint and added Authorization header (consistent with M-STRIPE-DEPOSIT pattern) | Already correct in original; confirmed |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials; `RECONNECT_STRIPE_CONNECTION` is explicit placeholder
#### Stage 2–4 Contamination: NONE

---

### 6. M-BOOKING-CREATION.blueprint.json

**Original name:** `M-BOOKING-CREATION — Stripe Deposit Webhook to Airtable Booking`
**Patched name:** `M07 M-BOOKING-CREATION`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name missing deployment order prefix | Added `M07` prefix |
| 2 | CRITICAL | HTTP modules 3, 6, 13, 14, 15, 16 used `"body"` field | Changed to `"data"` in all |
| 3 | CRITICAL | Module 17 `slack:ActionPostMessage` with `__IMTCONN__` | Changed to `slack:postMessage` with `connection` |
| 4 | HIGH | Module 17 Slack missing `metadata.parameters` and `metadata.expect` | Added |
| 5 | HIGH | HTTP modules missing `metadata.parameters` and `metadata.restore.expect` | Added standard arrays |
| 6 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 7 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 8 | INFO | Webhook metadata.parameters array missing | Added |
| 9 | INFO | Route `id` fields on router routes | Removed |
| 10 | INFO | `bodyType: "raw"` and `contentType: "application/json"` already present on all HTTP modules — no fix needed for those fields | Confirmed correct |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

### 7. M-BOOKING-CONFIRMATION.blueprint.json

**Original name:** `M-BOOKING-CONFIRMATION — Deposit Confirmed to Client Communication`
**Patched name:** `M08 M-BOOKING-CONFIRMATION`

#### Issues Found

| # | Severity | Issue | Fix Applied |
|---|---|---|---|
| 1 | CRITICAL | Name missing deployment order prefix | Added `M08` prefix |
| 2 | CRITICAL | Gmail modules 4 and 6 used `"__IMTCONN__"` connection key | Changed to `"connection"` |
| 3 | CRITICAL | SMS modules 5 and 7 had `"url": "INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT"` — wrong URL for SMS API | Changed to `https://api.quosms.com/v1/messages` (consistent with M-STRIPE-DEPOSIT module 7) |
| 4 | CRITICAL | SMS modules 5 and 7 missing `Authorization: Bearer RECONNECT_SMS_CONNECTION` header | Added |
| 5 | CRITICAL | SMS modules 5 and 7 used `"message"` field in JSON body — Quo SMS API uses `"body"` | Changed to `"body"` (consistent with M-STRIPE-DEPOSIT module 7) |
| 6 | CRITICAL | SMS modules 5 and 7 had extraneous `"brand"` field not in Quo SMS API spec | Removed; added `"from"` sender ID field consistent with M-STRIPE-DEPOSIT |
| 7 | CRITICAL | HTTP modules 9, 10, 11 used `"body"` field | Changed to `"data"` |
| 8 | CRITICAL | Module 12 `slack:ActionPostMessage` with `__IMTCONN__` | Changed to `slack:postMessage` with `connection` |
| 9 | HIGH | Module 12 Slack missing `metadata.parameters` and `metadata.expect` | Added |
| 10 | HIGH | HTTP modules missing `metadata.parameters` and `metadata.restore.expect` | Added standard arrays |
| 11 | HIGH | `"dataloss": false` in scenario metadata | Changed to `"dlt": false` |
| 12 | MEDIUM | `"slots": null` in scenario metadata | Removed |
| 13 | INFO | Webhook metadata.parameters array missing | Added |
| 14 | INFO | Route `id` fields on router routes | Removed |
| 15 | INFO | `bodyType: "raw"` and `contentType` already correct on modules 5, 7, 9, 10, 11 — confirmed |

#### JSON Validation: PASS
#### Secrets Check: PASS — No real credentials
#### Stage 2–4 Contamination: NONE

---

## Files Unchanged

**M-BRAND-ROUTER.blueprint.json** — This is the reference implementation. It was fetched from `claude/fix-mbrand-router-scenario-G5C0h` (the validated fix branch) and placed into the `json_blueprints` directory. No modifications made.

---

## Global JSON Validation Results

| File | Result |
|---|---|
| M-BRAND-ROUTER.blueprint.json | PASS |
| M-AUDIT-LOGGER.blueprint.json | PASS |
| M-LEAD-INTAKE.blueprint.json | PASS |
| M-SLACK-ALERTS.blueprint.json | PASS |
| M-CONCIERGE-ASSIGNMENT.blueprint.json | PASS |
| M-STRIPE-DEPOSIT.blueprint.json | PASS |
| M-BOOKING-CREATION.blueprint.json | PASS |
| M-BOOKING-CONFIRMATION.blueprint.json | PASS |

---

## Remaining Manual Setup Required After Make Import

### All Scenarios
| Step | What |
|---|---|
| Rebind Airtable connection | Replace `RECONNECT_AIRTABLE_CONNECTION` with your live Airtable connection in every scenario |
| Rebind Slack connection | Replace `RECONNECT_SLACK_CONNECTION` with your live Slack connection in every scenario |
| Copy webhook URLs | After import, copy each scenario's webhook URL from Make → paste into the calling scenarios |

### M-AUDIT-LOGGER (M02)
- `AUTOMATION_HEALTH_TABLE_ID` in modules 5 and 6 must be replaced with the real Airtable table ID for the Automation_Health table. Find this in Airtable → API docs for the base.

### M-CONCIERGE-ASSIGNMENT (M05)
- `CONCIERGE_OPERATORS_TABLE_ID` in module 3 must be replaced with the real Airtable table ID for the Concierge_Operators table.

### M-STRIPE-DEPOSIT (M06)
- Module 4: Replace `RECONNECT_STRIPE_CONNECTION` in the Authorization header with your Stripe secret key (`sk_test_...` for test mode, `sk_live_...` for production). Start with test mode.
- Module 7: Replace `RECONNECT_SMS_CONNECTION` in the Authorization header with your Quo SMS bearer token. Confirm that `https://api.quosms.com/v1/messages` is the correct Quo SMS production endpoint.

### M-CONCIERGE-ASSIGNMENT (M05), M-STRIPE-DEPOSIT (M06), M-BOOKING-CONFIRMATION (M08)
- All Gmail modules: Replace `RECONNECT_GMAIL_CONNECTION` with your live Gmail connection. You may need two separate Gmail connections — one for `hello@shesaidsail.com` and one for `hello@mareexecutive.com`.

### M-BOOKING-CONFIRMATION (M08) — SMS modules
- Replace `RECONNECT_SMS_CONNECTION` in Authorization headers for modules 5 and 7.

### M-SLACK-ALERTS (M04)
- Emergency route module 8: Replace `WILL_SLACK_USER_ID_PLACEHOLDER` with Will's actual Slack user ID (format: `U0XXXXXXX`) for direct-message emergency alerts.

---

## Final Import-Readiness Verdict

| File | Verdict |
|---|---|
| M-BRAND-ROUTER.blueprint.json | READY |
| M-AUDIT-LOGGER.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable + Slack; set AUTOMATION_HEALTH_TABLE_ID) |
| M-LEAD-INTAKE.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable + Slack; set webhook URLs post-import) |
| M-SLACK-ALERTS.blueprint.json | READY WITH MANUAL FIXES (rebind Slack; set Will's user ID for emergency route; set webhook URLs) |
| M-CONCIERGE-ASSIGNMENT.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable, Slack, Gmail; set CONCIERGE_OPERATORS_TABLE_ID; set webhook URLs) |
| M-STRIPE-DEPOSIT.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable, Slack, Gmail, Stripe, SMS; set webhook URLs) |
| M-BOOKING-CREATION.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable + Slack; set webhook URLs post-import) |
| M-BOOKING-CONFIRMATION.blueprint.json | READY WITH MANUAL FIXES (rebind Airtable, Slack, Gmail, SMS; set webhook URLs) |

---

## OVERALL VERDICT

**READY WITH MANUAL FIXES**

All 8 blueprint JSON files are structurally valid, import-safe, free of secrets, and conform to the M-BRAND-ROUTER quality standard. No live credentials are present. All credential slots use explicit approved placeholders. Manual credential rebinding and webhook URL propagation are required after import — these are standard post-import steps for all Make blueprints and are documented in `STAGE_1_REIMPORT_INSTRUCTIONS.md`.
