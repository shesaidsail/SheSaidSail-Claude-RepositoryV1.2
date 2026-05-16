# M-BRAND-ROUTER Fix Report

**Date:** 2026-05-16
**File:** `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-BRAND-ROUTER.blueprint.json`
**Status at start:** File did not exist in repository — created from spec.

---

## Summary

The blueprint JSON file was absent from the repository. It has been created from scratch, conforming exactly to the M01 M-BRAND-ROUTER authoritative spec. All 7 error classes from the spec have been addressed in the new file.

---

## Module-by-Module Change Log

### Module 1 — Webhook (gateway:CustomWebHook)

| Field | Before | After | Status |
|---|---|---|---|
| Hook ID | (file absent) | `RECONNECT_WEBHOOK_ID` placeholder | CREATED |

Not touched beyond creation — webhook module left with placeholder per spec instruction.

---

### Module 2 — Router (builtin:BasicRouter)

| Field | Before | After | Status |
|---|---|---|---|
| Router structure | (file absent) | 3 routes: SSS, ME, Fallback | CREATED |

Router filter conditions created per spec. Not modified beyond initial creation per spec instruction.

---

### Module 3 — Slack (Fallback/Ambiguous alert)

**ERROR 5 applied.**

| Field | Before | After | Status |
|---|---|---|---|
| Channel | (file absent) | `ops-alerts` | CREATED |
| Text | (file absent) | `[M01] BRAND UNDETECTED — defaulted to SSS \| Record: {{1.id}} \| Source: {{1.Lead_Source}} \| LUCIANA REVIEW REQUIRED` | CREATED |
| Connection | (file absent) | `RECONNECT_SLACK_CONNECTION` | CREATED |

---

### Module 4 — HTTP legacy 4 (SSS Airtable PATCH)

**ERROR 4 applied. Verified correct per spec.**

| Field | Before | After | Status |
|---|---|---|---|
| URL | (file absent) | `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}` | CREATED |
| Method | (file absent) | `PATCH` | CREATED |
| Authorization header | (file absent) | `Bearer RECONNECT_AIRTABLE_CONNECTION` | CREATED |
| Content-Type header | (file absent) | `application/json` | CREATED |
| Body type | (file absent) | `raw` | CREATED |
| Content type | (file absent) | `application/json` | CREATED |
| Request content | (file absent) | `{"fields":{"Brand":"She Said Sail"}}` | CREATED |
| Parse response | (file absent) | `true` (Yes) | CREATED |
| Evaluate all states as errors | (file absent) | `false` (No) — per ERROR 7 spec | CREATED |

---

### Module 5 — HTTP legacy 5 (SSS Claude API call)

**ERRORS 1, 2, 3, 4, 6, 7 applied.**

| Field | Before | After | Status |
|---|---|---|---|
| URL | (file absent) | `https://api.anthropic.com/v1/messages` | CREATED |
| Method | (file absent) | `POST` | CREATED — ERROR 4 |
| model | (file absent) | `claude-sonnet-4-20250514` | CREATED — ERROR 1 |
| max_tokens | (file absent) | `600` | CREATED — ERROR 2 |
| temperature | (file absent) | `0.4` | CREATED — ERROR 3 |
| system | (file absent) | `RECONNECT_SSS_SYSTEM_PROMPT` | CREATED |
| messages[0].role | (file absent) | `user` | CREATED |
| messages[0].content | (file absent) | `Brand routing confirmed: She Said Sail (default). RecordId: {{1.recordId}} \| Lead_Source: {{1.Lead_Source}} \| Website_Source: {{1.Website_Source}} \| Landing_Page: {{1.Landing_Page}}` | CREATED |
| x-api-key header | (file absent) | `RECONNECT_ANTHROPIC_API_KEY` | CREATED |
| anthropic-version header | (file absent) | `2023-06-01` | CREATED — ERROR 6 |
| Content-Type header | (file absent) | `application/json` | CREATED |
| Evaluate all states as errors | (file absent) | `true` (Yes) | CREATED — ERROR 7 |
| Parse response | (file absent) | `true` (Yes) | CREATED |

---

### Module 6 — Slack (SSS success alert)

**ERROR 5 applied.**

| Field | Before | After | Status |
|---|---|---|---|
| Channel | (file absent) | `ops-alerts` | CREATED |
| Text | (file absent) | `[M01] Brand routed: She Said Sail \| Record: {{1.id}} \| Source: {{1.Lead_Source}} \| Prompt: SSS_SYSTEM` | CREATED |
| Connection | (file absent) | `RECONNECT_SLACK_CONNECTION` | CREATED |

---

### Module 7 — HTTP legacy 7 (ME Airtable PATCH)

**ERROR 4 applied. Verified correct per spec.**

| Field | Before | After | Status |
|---|---|---|---|
| URL | (file absent) | `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}` | CREATED |
| Method | (file absent) | `PATCH` | CREATED |
| Authorization header | (file absent) | `Bearer RECONNECT_AIRTABLE_CONNECTION` | CREATED |
| Content-Type header | (file absent) | `application/json` | CREATED |
| Body type | (file absent) | `raw` | CREATED |
| Content type | (file absent) | `application/json` | CREATED |
| Request content | (file absent) | `{"fields":{"Brand":"Mare Executive"}}` | CREATED |
| Parse response | (file absent) | `true` (Yes) | CREATED |
| Evaluate all states as errors | (file absent) | `false` (No) — per ERROR 7 spec | CREATED |

---

### Module 8 — HTTP legacy 8 (ME Claude API call)

**ERRORS 1, 2, 3, 4, 6, 7 applied.**

| Field | Before | After | Status |
|---|---|---|---|
| URL | (file absent) | `https://api.anthropic.com/v1/messages` | CREATED |
| Method | (file absent) | `POST` | CREATED — ERROR 4 |
| model | (file absent) | `claude-sonnet-4-20250514` | CREATED — ERROR 1 |
| max_tokens | (file absent) | `600` | CREATED — ERROR 2 |
| temperature | (file absent) | `0.4` | CREATED — ERROR 3 |
| system | (file absent) | `RECONNECT_ME_SYSTEM_PROMPT` | CREATED |
| messages[0].role | (file absent) | `user` | CREATED |
| messages[0].content | (file absent) | `Brand routing confirmed: Mare Executive. RecordId: {{1.recordId}} \| Lead_Source: {{1.Lead_Source}} \| Website_Source: {{1.Website_Source}} \| Landing_Page: {{1.Landing_Page}}` | CREATED |
| x-api-key header | (file absent) | `RECONNECT_ANTHROPIC_API_KEY` | CREATED |
| anthropic-version header | (file absent) | `2023-06-01` | CREATED — ERROR 6 |
| Content-Type header | (file absent) | `application/json` | CREATED |
| Evaluate all states as errors | (file absent) | `true` (Yes) | CREATED — ERROR 7 |
| Parse response | (file absent) | `true` (Yes) | CREATED |

---

### Module 9 — Slack (ME success alert)

**ERROR 5 applied.**

| Field | Before | After | Status |
|---|---|---|---|
| Channel | (file absent) | `ops-alerts` | CREATED |
| Text | (file absent) | `[M01] Brand routed: Mare Executive \| Record: {{1.id}} \| Source: {{1.Lead_Source}} \| Prompt: ME_SYSTEM` | CREATED |
| Connection | (file absent) | `RECONNECT_SLACK_CONNECTION` | CREATED |

---

## Error Checklist

| Error # | Description | Applied To | Status |
|---|---|---|---|
| ERROR 1 | Wrong Claude model (`claude-sonnet-4-20250514`) | HTTP 5, HTTP 8 | FIXED |
| ERROR 2 | Wrong max_tokens (`600`) | HTTP 5, HTTP 8 | FIXED |
| ERROR 3 | Missing temperature (`0.4`) | HTTP 5, HTTP 8 | FIXED |
| ERROR 4 | HTTP method blank | HTTP 4 (PATCH), HTTP 5 (POST), HTTP 7 (PATCH), HTTP 8 (POST) | FIXED |
| ERROR 5 | Slack channel and text missing | Slack 3, Slack 6, Slack 9 | FIXED |
| ERROR 6 | anthropic-version header missing/incorrect (`2023-06-01`) | HTTP 5, HTTP 8 | FIXED |
| ERROR 7 | Evaluate all states as errors incorrect | HTTP 5 = Yes, HTTP 8 = Yes, HTTP 4 = No, HTTP 7 = No | FIXED |

---

## Validation

- [x] Blueprint file parses as valid JSON
- [x] No secrets or API keys added — all credentials use `RECONNECT_*` placeholders
- [x] Only M-BRAND-ROUTER was modified
- [x] No Stage 2–4 contamination
- [x] All before/after fixes documented above

---

## Issues That Cannot Be Fixed in the Blueprint File

The following require manual reconnection inside the Make scenario UI — they cannot be embedded in a blueprint JSON safely:

1. **Slack connection** — must be reconnected to your workspace after import
2. **Airtable token** — `RECONNECT_AIRTABLE_CONNECTION` must be replaced with a live Airtable personal access token
3. **Anthropic API key** — `RECONNECT_ANTHROPIC_API_KEY` must be replaced with the live key
4. **Webhook URL** — Make generates a new webhook URL on import; update any upstream triggers
5. **SSS system prompt** — paste full SSS system prompt text into HTTP 5 `system` field
6. **ME system prompt** — paste full ME system prompt text into HTTP 8 `system` field

---

## Final Verdict

**READY WITH MANUAL FIXES**

The blueprint is structurally correct and spec-compliant. It can be imported into Make immediately. After import, complete the credential reconnections listed above before activating the scenario.

**Recommended workflow:**
1. Import blueprint into Make (Scenarios → Import Blueprint)
2. Follow `M_BRAND_ROUTER_MANUAL_SETUP_GUIDE.md` to reconnect all connections
3. Run a single test trigger with a known record
4. Verify Airtable Brand field updated, Claude API responded, Slack alert fired
5. Activate scenario
