# M-LEAD-INTAKE — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Lead Intake  
**Execution Order:** Module 1 in Stage 1 pipeline (entry point for all inbound leads)

---

## 1. Scenario Name

`M-LEAD-INTAKE`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references in M-BRAND-ROUTER, M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, and all Audit Log entries.

---

## 3. Trigger Type

**Pattern:** Custom Webhook (Make-generated URL)  
**Make Module Type:** Webhooks > Custom Webhook  
**Method:** POST  
**Content-Type:** application/json  
**Authentication:** Bearer Token (validated in Module 2)

**Inbound Sources:**
| Source | Mechanism |
|--------|-----------|
| Website contact form | Form submits POST to webhook URL |
| Typeform | Typeform webhook integration sends POST on submission |
| Instagram DM (via Zapier or ManyChat) | Third-party routes DM data to webhook URL |
| Direct (manual entry by Luciana) | Luciana posts payload via Postman or internal tool |

**Webhook URL pattern (to be generated in Make.com):**
```
https://hook.us1.make.com/[WEBHOOK-ID]
```

> Record the generated webhook URL here after scenario creation. Distribute to all source integrations.

**Full Inbound Payload Structure:**
```json
{
  "source": "website_form",
  "brand_hint": "SSS",
  "first_name": "Sarah",
  "last_name": "Johnson",
  "email": "sarah@example.com",
  "phone": "+13055551234",
  "city": "Miami",
  "charter_date": "2026-06-15",
  "group_size": "8",
  "occasion": "Bachelorette",
  "package_interest": "Sunset Sail",
  "budget": "$500-$1000",
  "message": "Looking for a bachelorette party cruise for 8 people",
  "utm_source": "instagram",
  "utm_campaign": "spring_2026",
  "submitted_at": "2026-05-16T14:30:00Z"
}
```

**Required fields (webhook rejects 400 if missing):**
- `email`
- `submitted_at`
- `source`

**Optional fields (proceed with null if missing):**
- All other fields

---

## 4. Exact Module Sequence

### Module 1 — [Webhook] Receive Inbound Payload

**Make Module Type:** Webhooks > Custom Webhook  
**Position:** Module 1 (scenario trigger)  
**Purpose:** Receive and parse the inbound lead payload. Make automatically parses JSON body into individual field variables.

**Webhook Settings:**
- Maximum payload size: 1 MB
- IP restriction: None (public endpoint; authentication handled via bearer token in Module 2)
- Webhook response: Immediate 200 OK (processing continues asynchronously)

**Data Structure Defined in Make Webhook Settings:**
Register the following fields so Make maps them correctly:

| Field Name | Type | Required |
|------------|------|----------|
| `source` | Text | Yes |
| `brand_hint` | Text | No |
| `first_name` | Text | No |
| `last_name` | Text | No |
| `email` | Text | Yes |
| `phone` | Text | No |
| `city` | Text | No |
| `charter_date` | Date | No |
| `group_size` | Text | No |
| `occasion` | Text | No |
| `package_interest` | Text | No |
| `budget` | Text | No |
| `message` | Text | No |
| `utm_source` | Text | No |
| `utm_campaign` | Text | No |
| `submitted_at` | Date/Time | Yes |

---

### Module 2 — [HTTP] Bearer Token Validation

**Make Module Type:** Tools > Set Variable (with filter) OR HTTP > Make a Request (to internal validation endpoint)  
**Position:** Module 2  
**Purpose:** Validate the `Authorization: Bearer [TOKEN]` header on the incoming request. Reject unauthorized requests before any data processing.

**Implementation approach (inline — no external HTTP call):**
Make does not natively expose request headers inside a Custom Webhook module for header-based auth. Use one of these two approaches:

**Approach A (Recommended) — Embed token in payload:**
Add `"api_key": "[SECRET_TOKEN]"` to the payload. Module 2 uses a Filter to halt if `{{1.api_key}}` does not equal the expected secret.

**Filter Configuration:**
- Label: `Bearer Token Valid`
- Condition: `{{1.api_key}}` equals `[BEARER_TOKEN_VALUE]`
- If condition not met: Stop processing (Make halts the scenario execution without error response)

**Approach B — Use Make's built-in webhook authentication:**
In the webhook module settings, enable IP allowlist or shared secret. Make validates before the scenario runs.

> **Action Required:** Confirm with Will which approach to use. Store the token value in Make > Scenario > Keys (encrypted). Do NOT hardcode the token in the scenario formula.

**On Failure (token mismatch):**
- Log to Audit Log: `Event_Type = AUTH_FAILURE`, `Status = REJECTED`
- Do NOT write to Requests table
- Do NOT send Slack alert (to avoid alert flooding from probes)
- Halt scenario silently

---

### Module 3 — [Tools] Timestamp Validation

**Make Module Type:** Tools > Set Variable + Filter  
**Position:** Module 3  
**Purpose:** Reject payloads older than 5 minutes to prevent replay attacks and stale data entry.

**Timestamp Calculation:**
```
age_seconds = dateDifference(now, parseDate({{1.submitted_at}}, "YYYY-MM-DDTHH:mm:ssZ"), "seconds")
```

**Filter:**
- Label: `Timestamp within 5 minutes`
- Condition: `{{age_seconds}}` less than or equal to `300`
- If condition not met: Stop processing

**On Timestamp Failure:**
- Log to Audit Log: `Event_Type = TIMESTAMP_REJECTED`, `Request_Email = {{1.email}}`, `submitted_at = {{1.submitted_at}}`, `Status = REJECTED`
- Halt scenario

**Exception — Direct source bypass:**
If `{{1.source}}` equals `direct` (manual entry by Luciana), skip timestamp validation. Luciana may manually enter leads that are hours old.

**Filter adjustment for direct source:**
```
(age_seconds <= 300) OR ({{1.source}} = "direct")
```

---

### Module 4 — [Router + Text Parser + Set Variable] M-BRAND-ROUTER Logic Block

**Make Module Type:** Router + Text Parser (Match Pattern) x2 + Set Variable x3 + Router  
**Position:** Modules 4.1 through 4.8 (as documented in M-BRAND-ROUTER.md)  
**Purpose:** Classify incoming lead as SSS, ME, or AMBIGUOUS using the 3-tier classification logic.

**Reference:** See M-BRAND-ROUTER.md for full module-by-module specification.

**Output variables available after Module 4.8:**
- `brand_classification` — SSS | ME | AMBIGUOUS
- `brand_confidence` — HIGH | LOW
- `brand_signal_source` — hint | occasion | keyword | default
- `requires_human_review` — true | false

---

### Module 5 — [Tools] Environment Check

**Make Module Type:** Tools > Set Variable + Filter  
**Position:** Module 5  
**Purpose:** Prevent sandbox/test records from flowing into the production Airtable base. Test payloads must include `"environment": "sandbox"` to be caught here.

**Filter:**
- Label: `Production environment only`
- Condition: `{{1.environment}}` does NOT equal `sandbox`
- If condition not met: Log to Audit Log (`Event_Type = SANDBOX_INTERCEPT`) and stop

**Sandbox detection signals:**
| Signal | Value | Action |
|--------|-------|--------|
| `environment` field | `sandbox` | Stop |
| `email` contains | `+test` or `@test.` | Stop |
| `first_name` | `TEST` (all caps) | Stop |

---

### Module 6 — [Tools] Generate Idempotency Key

**Make Module Type:** Tools > Set Variable  
**Position:** Module 6  
**Purpose:** Generate a unique key for this payload to enable deduplication.

**Idempotency Key Formula:**
```
idempotency_key = sha256(
  lower(trim({{1.email}})) + "|" + 
  lower(trim({{1.phone}})) + "|" + 
  formatDate(parseDate({{1.submitted_at}}, "YYYY-MM-DDTHH:mm:ssZ"), "YYYY-MM-DDTHH:mm:ss")
)
```

**Make formula syntax:**
```
{{sha256(lower(trim(1.email)) + "|" + lower(trim(1.phone)) + "|" + formatDate(parseDate(1.submitted_at, "YYYY-MM-DDTHH:mm:ssZ"), "YYYY-MM-DDTHH:mm:ss"))}}
```

**Fallback (if phone is missing):**
```
{{sha256(lower(trim(1.email)) + "|" + "no-phone" + "|" + formatDate(parseDate(1.submitted_at, "YYYY-MM-DDTHH:mm:ssZ"), "YYYY-MM-DDTHH:mm:ss"))}}
```

**Variable name:** `idempotency_key`

---

### Module 7 — [Airtable] Duplicate Check

**Make Module Type:** Airtable > Search Records  
**Position:** Module 7  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblTlSB9CO4dTGodg` (Requests)  
**Purpose:** Search for an existing Requests record with the same idempotency key to prevent duplicate processing.

**Search Configuration:**
- Filter by formula: `{Idempotency_Key} = "{{idempotency_key}}"`
- Maximum records: 1
- Fields to retrieve: `Record_ID`, `Idempotency_Key`, `Status`, `Created_At`

**Result handling (Router after Module 7):**

| Outcome | Condition | Next Module |
|---------|-----------|-------------|
| Duplicate found | `{{7.total_records}} > 0` | Module 7A — Log duplicate and STOP |
| New record | `{{7.total_records}} = 0` | Module 8 — Create Airtable record |

---

### Module 7A — [Airtable + Stop] Duplicate Handler

**Make Module Type:** Airtable > Create Record (Audit Log) + Tools > Stop  
**Position:** Module 7A (on duplicate route)  
**Purpose:** Log the duplicate detection event and halt processing.

**Audit Log record to create:**

| Field | Value |
|-------|-------|
| `Event_Type` | `DUPLICATE_DETECTED` |
| `Scenario_Name` | `M-LEAD-INTAKE` |
| `Email` | `{{1.email}}` |
| `Idempotency_Key` | `{{idempotency_key}}` |
| `Existing_Record_ID` | `{{7.records[].id}}` |
| `Timestamp` | `{{now}}` |
| `Execution_ID` | `{{executionId}}` |
| `Status` | `SKIPPED` |
| `Notes` | `Duplicate payload detected. Idempotency key matched existing record. Processing halted.` |

**After Audit Log write:** Halt scenario with status `Complete` (not Error).

---

### Module 8 — [Airtable] Create Request Record

**Make Module Type:** Airtable > Create Record  
**Position:** Module 8  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblTlSB9CO4dTGodg` (Requests)  
**Purpose:** Create the canonical lead record in Airtable from the validated, classified payload.

**Complete Airtable Field Mapping:**

| Airtable Field Name | Make Source | Formula / Transform |
|---------------------|-------------|---------------------|
| `First_Name` | `{{1.first_name}}` | `trim({{1.first_name}})` |
| `Last_Name` | `{{1.last_name}}` | `trim({{1.last_name}})` |
| `Full_Name` | Computed | `{{trim(1.first_name)}} {{trim(1.last_name)}}` |
| `Email` | `{{1.email}}` | `lower(trim({{1.email}}))` |
| `Phone` | `{{1.phone}}` | As received |
| `City` | `{{1.city}}` | `trim({{1.city}})` |
| `Charter_Date` | `{{1.charter_date}}` | `formatDate(parseDate({{1.charter_date}}, "YYYY-MM-DD"), "YYYY-MM-DD")` |
| `Group_Size` | `{{1.group_size}}` | `toNumber({{1.group_size}})` |
| `Occasion` | `{{1.occasion}}` | As received |
| `Package_Interest` | `{{1.package_interest}}` | As received |
| `Budget` | `{{1.budget}}` | As received |
| `Message` | `{{1.message}}` | As received |
| `Source` | `{{1.source}}` | As received |
| `UTM_Source` | `{{1.utm_source}}` | As received |
| `UTM_Campaign` | `{{1.utm_campaign}}` | As received |
| `Submitted_At` | `{{1.submitted_at}}` | `parseDate({{1.submitted_at}}, "YYYY-MM-DDTHH:mm:ssZ")` |
| `Brand` | `{{brand_classification}}` | SSS \| ME \| AMBIGUOUS |
| `Brand_Confidence` | `{{brand_confidence}}` | HIGH \| LOW |
| `Brand_Signal_Source` | `{{brand_signal_source}}` | hint \| occasion \| keyword \| default |
| `Requires_Human_Brand_Review` | `{{requires_human_review}}` | Checkbox (true/false) |
| `Idempotency_Key` | `{{idempotency_key}}` | SHA256 hash string |
| `Status` | Hardcoded | `New` |
| `Stage` | Hardcoded | `Lead Intake` |
| `Pipeline_Stage` | Hardcoded | `1` |
| `Created_At` | `{{now}}` | ISO 8601 datetime |
| `Intake_Execution_ID` | `{{executionId}}` | Make execution ID |
| `Automations_Paused` | Hardcoded | `false` |
| `Emergency_Flag` | Hardcoded | `false` |

**Error Handler on Module 8:**
- If Airtable write fails: retry 3x at 15-second intervals
- After 3 failures: write to Audit Log (Error), send Slack alert to #sss-ops-alerts, halt scenario
- Do NOT proceed to Module 9 if record creation fails

**Output:** `{{8.id}}` — the Airtable Record ID of the newly created Request record.

---

### Module 9 — [Airtable] Write Idempotency Key Confirmation

**Make Module Type:** Airtable > Update Record  
**Position:** Module 9  
**Purpose:** Confirm that the idempotency key is persisted in the record (handles edge case where Module 8 created the record but the key field failed to write).

**Update Configuration:**
- Record ID: `{{8.id}}`
- Field: `Idempotency_Key`
- Value: `{{idempotency_key}}`
- Field: `Request_ID_Display`
- Value: `REQ-{{formatDate(now, "YYYYMMDD")}}-{{substring(8.id, 3, 6)}}`

> The `Request_ID_Display` is a human-readable identifier for use in Slack alerts and email communications. Format: `REQ-20260516-abc123`.

---

### Module 10 — [HTTP] Call M-SLACK-ALERTS

**Make Module Type:** HTTP > Make a Request  
**Position:** Module 10  
**Purpose:** Trigger M-SLACK-ALERTS scenario with the new Request ID so a formatted Slack alert is posted to #sss-ops-alerts.

**Request Configuration:**
- Method: POST
- URL: `[M-SLACK-ALERTS Webhook URL — to be registered]`
- Content-Type: `application/json`
- Authorization: `Bearer [INTER-SCENARIO TOKEN]`

**Request Body:**
```json
{
  "request_id": "{{8.id}}",
  "request_id_display": "{{9.Request_ID_Display}}",
  "alert_type": "new_lead",
  "triggered_by": "M-LEAD-INTAKE",
  "execution_id": "{{executionId}}",
  "brand_classification": "{{brand_classification}}",
  "requires_human_review": "{{requires_human_review}}"
}
```

**Error Handler on Module 10:**
- If M-SLACK-ALERTS call fails: do NOT halt M-LEAD-INTAKE
- Log failure to Audit Log: `Event_Type = SLACK_TRIGGER_FAILED`
- Continue to Module 11 (Audit Log write)
- Slack failure is non-fatal to intake flow

---

### Module 11 — [Airtable] Write Audit Log Entry

**Make Module Type:** Airtable > Create Record  
**Position:** Module 11  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblrMpTfMk8q1eNHp` (Audit Log)  
**Purpose:** Write the canonical audit entry for this lead intake event.

**Audit Log Field Mapping:**

| Audit Log Field | Value |
|-----------------|-------|
| `Event_Type` | `LEAD_INTAKE_COMPLETE` |
| `Scenario_Name` | `M-LEAD-INTAKE` |
| `Execution_ID` | `{{executionId}}` |
| `Request_ID` | `{{8.id}}` |
| `Request_ID_Display` | `{{9.Request_ID_Display}}` |
| `Email` | `{{1.email}}` |
| `Brand` | `{{brand_classification}}` |
| `Brand_Confidence` | `{{brand_confidence}}` |
| `Source` | `{{1.source}}` |
| `Idempotency_Key` | `{{idempotency_key}}` |
| `Timestamp` | `{{now}}` |
| `Status` | `SUCCESS` |
| `Slack_Trigger_Status` | `SUCCESS` or `FAILED` (from Module 10 result) |
| `Notes` | `Lead intake completed. Record created. Slack triggered.` |

---

### Module 12 — [Airtable] Write Automation Health Entry

**Make Module Type:** Airtable > Update Record (or Create Record in Health table)  
**Position:** Module 12  
**Purpose:** Update the automation health dashboard with last-run metadata for M-LEAD-INTAKE.

**Health Record Fields (update existing health record for this scenario):**

| Field | Value |
|-------|-------|
| `Scenario_Name` | `M-LEAD-INTAKE` |
| `Last_Run_At` | `{{now}}` |
| `Last_Run_Status` | `SUCCESS` |
| `Last_Execution_ID` | `{{executionId}}` |
| `Total_Runs_Today` | Incremented by 1 (formula field in Airtable) |
| `Last_Request_ID` | `{{8.id}}` |
| `Error_Count_Today` | No change on success |

---

### Module 13 — [Emergency Flag Check] — Runs at scenario start (pre-filter)

**Implementation note:** The Emergency_Flag and Automations_Paused checks are implemented as Make Filters positioned immediately after Module 1 (Webhook) and before Module 2 (Auth). This ensures no processing occurs when the system is administratively paused.

**Emergency_Flag Check:**
- Make module: Tools > HTTP request to Airtable to fetch the system config record
- Alternatively: Use a hardcoded scenario-level variable that Will or Luciana can toggle
- If `Emergency_Flag = true`: Log to Audit Log, send Slack alert to Luciana and Will directly, halt all processing

**Automations_Paused Check:**
- Same pattern as Emergency_Flag
- If `Automations_Paused = true`: Log to Audit Log, halt processing silently

> **Architecture Decision Required:** Confirm whether Emergency_Flag and Automations_Paused are stored in a dedicated Airtable system config table or as Make scenario variables. If Airtable: add Module 1.5 (Airtable fetch of config record) before Module 2. If Make variables: configure in scenario settings.

---

## 5. Router Logic

The complete intake routing decision tree:

```
WEBHOOK RECEIVED
│
├── Auth token invalid → REJECT (log, halt)
│
├── Timestamp > 5 min old AND source != "direct" → REJECT (log, halt)
│
├── Emergency_Flag = true → HALT (alert Will + Luciana, log)
│
├── Automations_Paused = true → HALT (log silently)
│
├── Environment = "sandbox" → INTERCEPT (log, halt)
│
├── Run M-BRAND-ROUTER logic block
│   ├── brand_hint valid → classify by hint (HIGH confidence)
│   ├── occasion match → classify by occasion (HIGH confidence)
│   ├── keyword match → classify by keyword (LOW confidence)
│   └── no signals → AMBIGUOUS (requires_human_review = true)
│
├── Idempotency check → duplicate found? → LOG + HALT
│
├── Create Airtable Request record
│
├── Call M-SLACK-ALERTS (non-fatal if fails)
│
└── Write Audit Log + Health → COMPLETE
```

---

## 6. Airtable Field Mapping

Full mapping documented in Module 8 table above. Summary of key transformations:

| Transform | Applied To |
|-----------|-----------|
| `lower(trim(...))` | email |
| `trim(...)` | first_name, last_name, city |
| `toNumber(...)` | group_size |
| `parseDate(...)` | charter_date, submitted_at |
| `formatDate(...)` | charter_date (stored as YYYY-MM-DD) |
| `sha256(...)` | idempotency_key |

---

## 7. Webhook Structure

**Endpoint:** Custom Make webhook (generated URL)  
**Method:** POST  
**Headers Required:**
```
Content-Type: application/json
Authorization: Bearer [TOKEN]
```

**Successful Response:** HTTP 200 with body:
```json
{ "status": "received", "message": "Lead intake processing initiated." }
```

**Rejection Response (auth fail, timestamp fail):** HTTP 200 (Make webhooks always return 200; rejection is silent to prevent enumeration attacks). Processing is halted internally.

**Webhook Security Controls:**
1. Bearer token in payload `api_key` field
2. Timestamp validation (5-minute window)
3. Environment flag intercept
4. Idempotency key deduplication

---

## 8. Error Handling Logic

4-level error handling framework applied across all modules:

| Level | Trigger | Module(s) | Action |
|-------|---------|-----------|--------|
| Level 1 — Field Error | Missing or malformed field (e.g., unparseable date) | 1, 6, 8 | Use null/default value, continue, flag in Audit Log |
| Level 2 — Module Error | Airtable write fails, HTTP call fails | 8, 10, 11 | Retry per retry policy; if exhausted, log + alert + halt |
| Level 3 — Route Error | No route matches in any Router module | 4.5, post-7 | Fallback route catches all; set AMBIGUOUS or log |
| Level 4 — Scenario Crash | Unhandled exception | Any module | Make Error Handler module: write to Audit Log, Slack alert to #sss-ops-alerts, halt |

**Error Handler Modules (Make Error Handler):**
Attach to these modules:
- Module 8 (Airtable Create) — most critical
- Module 11 (Audit Log write)
- Module 4.3 and 4.4 (Text Parsers in brand router)

**Error Escalation:**
- Level 1-2 errors: Slack alert to #sss-ops-alerts
- Level 3-4 errors: Slack DM to Luciana + Slack alert to #sss-ops-alerts
- 3+ consecutive errors within 1 hour: Slack DM to Will

---

## 9. Retry Logic

| Module | Failure Scenario | Retries | Interval |
|--------|-----------------|---------|----------|
| Module 8 — Airtable Create | Airtable API timeout or 5xx | 3 | 15 seconds |
| Module 9 — Airtable Update | Airtable API timeout | 2 | 10 seconds |
| Module 10 — HTTP to M-SLACK-ALERTS | Webhook URL unreachable | 2 | 10 seconds |
| Module 11 — Audit Log | Airtable API timeout | 3 | 15 seconds |
| Module 7 — Airtable Search | Airtable API timeout | 2 | 10 seconds |

**Global retry setting:** Make.com Scenario Settings > Error handling > Auto-retry: 3 attempts, 10-second intervals for all modules not explicitly configured above.

**No-retry modules:**
- Module 2 (Auth) — deterministic, retry does not change outcome
- Module 3 (Timestamp) — deterministic
- Module 5 (Environment check) — deterministic

---

## 10. Duplicate Prevention

**Primary mechanism:** Idempotency key (Module 6) + Airtable search (Module 7).

**Key generation:** `SHA256(lower(email) + "|" + lower(phone) + "|" + submitted_at_normalized)`

**Deduplication window:** Unlimited — if a record with the same idempotency key exists in Airtable at any time, the new payload is rejected as duplicate.

**Edge cases:**
| Scenario | Handling |
|----------|----------|
| Same email, different submitted_at | Different idempotency key → new record created |
| Same email + phone, submitted_at within 1 second rounding | Same key → duplicate rejected |
| Phone field missing | Key uses "no-phone" literal → deduplication by email + timestamp only |
| Scenario re-run (Make retry) | Same idempotency key → duplicate rejected → no double records |
| Manually entered "direct" lead with old timestamp | Environment check bypasses timestamp; idempotency key still checked |

**Idempotency key stored in:** `Idempotency_Key` field of Requests table (`tblTlSB9CO4dTGodg`).

---

## 11. Slack Alert Structure

M-LEAD-INTAKE does not post directly to Slack. It calls M-SLACK-ALERTS (Module 10) with the Request ID. The Slack alert structure is documented in M-SLACK-ALERTS.md.

**Exception — Direct error alerts from M-LEAD-INTAKE:**

If Module 8 (Airtable Create) fails after all retries, M-LEAD-INTAKE posts this minimal alert directly to #sss-ops-alerts:

```json
{
  "text": ":red_circle: *M-LEAD-INTAKE FAILURE* — Airtable record creation failed after 3 retries.",
  "attachments": [
    {
      "color": "#FF0000",
      "fields": [
        { "title": "Email", "value": "{{1.email}}", "short": true },
        { "title": "Source", "value": "{{1.source}}", "short": true },
        { "title": "Execution ID", "value": "{{executionId}}", "short": false },
        { "title": "Error", "value": "{{error.message}}", "short": false }
      ]
    }
  ]
}
```

---

## 12. Audit Log Writes

**Table:** `tblrMpTfMk8q1eNHp`

Audit Log events written by M-LEAD-INTAKE:

| Event | Module | Event_Type | Status |
|-------|--------|-----------|--------|
| Auth failure | 2 | `AUTH_FAILURE` | `REJECTED` |
| Timestamp rejected | 3 | `TIMESTAMP_REJECTED` | `REJECTED` |
| Sandbox intercept | 5 | `SANDBOX_INTERCEPT` | `SKIPPED` |
| Duplicate detected | 7A | `DUPLICATE_DETECTED` | `SKIPPED` |
| Brand classified | 4.8 | `BRAND_CLASSIFIED` | `SUCCESS` |
| Record created | 8 | `RECORD_CREATED` | `SUCCESS` |
| Record creation failed | 8 | `RECORD_CREATE_FAILED` | `ERROR` |
| Slack trigger failed | 10 | `SLACK_TRIGGER_FAILED` | `WARNING` |
| Intake complete | 11 | `LEAD_INTAKE_COMPLETE` | `SUCCESS` |

---

## 13. Automation Health Writes

**Location:** Dedicated Automation Health table or system config record (confirm table ID with Airtable schema).

**On successful completion:**

| Field | Value |
|-------|-------|
| `Scenario` | `M-LEAD-INTAKE` |
| `Last_Success_At` | `{{now}}` |
| `Last_Execution_ID` | `{{executionId}}` |
| `Consecutive_Failures` | `0` (reset on success) |
| `Last_Request_ID` | `{{8.id}}` |

**On failure:**

| Field | Value |
|-------|-------|
| `Last_Failure_At` | `{{now}}` |
| `Last_Failure_Execution_ID` | `{{executionId}}` |
| `Consecutive_Failures` | Incremented |
| `Last_Error_Message` | Error text from Make |

---

## 14. Rollback Procedure

If M-LEAD-INTAKE creates a bad record (e.g., wrong data, test record in production):

**Step-by-step rollback:**

1. Identify the record in Airtable Requests table (`tblTlSB9CO4dTGodg`) by Record ID (from Slack alert or Audit Log).
2. In Airtable: set `Status = "Voided"` and `Stage = "Rollback"` on the bad record.
3. Add note to `Internal_Notes`: `"Record voided by [name] on [date]. Reason: [reason]. Original Execution ID: [executionId]."`.
4. Do NOT delete the record — Airtable records are append-only for auditability. Voiding is the correct approach.
5. Write a rollback entry to Audit Log: `Event_Type = RECORD_VOIDED`, `Request_ID = [bad record ID]`, `Notes = reason`.
6. If a Slack alert was already sent for this record: post a follow-up message in #sss-ops-alerts: `"[TEST]` or `[VOID]` notice referencing the original alert.
7. If M-CONCIERGE-ASSIGNMENT was triggered for this record: void the assignment in the same way (update Assignment record status to "Voided").
8. If the idempotency key is blocking legitimate re-processing: the bad record must be voided AND its `Idempotency_Key` field cleared (or the legitimate re-submission will need a new `submitted_at` value).

---

## 15. Sandbox Test Procedure

**Prerequisites:**
- Make.com scenario in INACTIVE state
- All module connections authenticated (Airtable, Slack)
- Test webhook URL noted
- Airtable base: `appdZ49WqgjRXxA1R` accessible
- Slack channel #sss-ops-alerts accessible

**Test Cases:**

### Test 1 — Happy Path (SSS, website form)
**Payload:**
```json
{
  "api_key": "[BEARER_TOKEN]",
  "source": "website_form",
  "brand_hint": "SSS",
  "first_name": "Sarah",
  "last_name": "Johnson",
  "email": "sarah+test1@example.com",
  "phone": "+13055551234",
  "city": "Miami",
  "charter_date": "2026-06-15",
  "group_size": "8",
  "occasion": "Bachelorette",
  "package_interest": "Sunset Sail",
  "budget": "$500-$1000",
  "message": "Looking for a bachelorette party cruise for 8 people",
  "utm_source": "instagram",
  "utm_campaign": "spring_2026",
  "submitted_at": "[CURRENT_TIMESTAMP]"
}
```
**Expected:** Record created in Airtable, Brand=SSS, Slack alert posted, Audit Log entry created.

### Test 2 — Duplicate Detection
**Payload:** Same as Test 1, same `submitted_at`  
**Expected:** `DUPLICATE_DETECTED` in Audit Log, no new Airtable record, no Slack alert.

### Test 3 — Auth Failure
**Payload:** Test 1 payload with `api_key` set to `WRONG_TOKEN`  
**Expected:** `AUTH_FAILURE` in Audit Log, processing halted.

### Test 4 — Timestamp Rejection
**Payload:** Test 1 payload with `submitted_at` = 10 minutes ago, `source` = `website_form`  
**Expected:** `TIMESTAMP_REJECTED` in Audit Log.

### Test 5 — AMBIGUOUS Brand
**Payload:** Test 1 with `brand_hint = ""`, `occasion = "Other"`, `message = "I need a boat for a party"`  
**Expected:** Brand=AMBIGUOUS, `requires_human_review=true`, Slack alert includes ambiguous classification block.

### Test 6 — ME Brand (Corporate)
**Payload:** `brand_hint = "ME"`, `occasion = "Corporate Event"`, `message = "Corporate team building"`  
**Expected:** Brand=ME, Slack alert reflects ME branding.

### Test 7 — Sandbox Intercept
**Payload:** Test 1 with `"environment": "sandbox"`  
**Expected:** `SANDBOX_INTERCEPT` in Audit Log, no Airtable record created.

### Test 8 — Direct Source (Old Timestamp)
**Payload:** Test 1 with `source = "direct"`, `submitted_at` = 2 hours ago  
**Expected:** Timestamp validation bypassed, record created normally.

**Execution Steps:**
1. Activate scenario in Make.com (Run Once mode).
2. Use webhook test tool (Postman or Make's built-in webhook test) to send each payload.
3. After each test: verify Airtable record in Requests table (or verify no record on rejection tests).
4. Verify Audit Log entry with correct `Event_Type` and `Status`.
5. Verify Slack alert content in #sss-ops-alerts (prefix all test messages with `[TEST]` by adding `"environment": "test"` flag handled in Slack template).
6. Record pass/fail for each test in the test log.
7. Deactivate scenario after testing.

---

## 16. Production Validation Checklist

**Go/No-Go Criteria — ALL must pass before enabling in production:**

- [ ] All 8 sandbox test cases pass
- [ ] Airtable record created with all 27 fields correctly populated
- [ ] Idempotency key correctly generated and stored in Airtable
- [ ] Duplicate detection correctly prevents second record on identical payload
- [ ] Bearer token validation correctly rejects invalid tokens
- [ ] Timestamp validation correctly rejects payloads older than 5 minutes
- [ ] Direct source correctly bypasses timestamp validation
- [ ] Brand classification (SSS, ME, AMBIGUOUS) matches M-BRAND-ROUTER spec for all test cases
- [ ] Audit Log entries written for every event type (8 event types verified)
- [ ] M-SLACK-ALERTS successfully called and alert appears in #sss-ops-alerts
- [ ] Slack alert failure is non-fatal (scenario completes even if Slack call fails)
- [ ] Sandbox intercept correctly catches `environment=sandbox` payloads
- [ ] Health record updated after each successful run
- [ ] Error handler correctly alerts #sss-ops-alerts on Airtable failure
- [ ] Module 8 retry logic verified (force-test by temporarily invalidating Airtable connection)
- [ ] Webhook URL recorded and distributed to all source integrations
- [ ] Bearer token securely stored in Make Keys (not hardcoded in scenario)
- [ ] Will has reviewed and approved the intake flow
- [ ] Luciana has reviewed and approved field mapping and alert format

**Sign-off Required From:**
- [ ] Will (Founder) — business logic and field mapping approval
- [ ] Luciana (Ops Lead) — operational workflow and alert format approval

---

## 17. Open Issues

| ID | Issue | Owner | Status |
|----|-------|-------|--------|
| LI-001 | Confirm Emergency_Flag and Automations_Paused storage location (Airtable config table vs Make variables) | Systems | OPEN |
| LI-002 | Bearer token approach — confirm Approach A (payload api_key) vs Approach B (Make built-in webhook auth) | Will | OPEN |
| LI-003 | Health table: confirm Airtable table ID for Automation Health records | Luciana | OPEN |
| LI-004 | Typeform webhook format: confirm exact field names in Typeform payload to ensure field mapping is correct | Luciana | OPEN |
| LI-005 | Instagram DM routing: confirm which middleware (Zapier, ManyChat) bridges Instagram DMs to this webhook, and what the payload format looks like | Luciana | OPEN |
| LI-006 | `Request_ID_Display` format: confirm `REQ-YYYYMMDD-[6-char suffix]` is the desired format, or provide alternate | Will | OPEN |
| LI-007 | Charter_Date field: confirm whether Airtable field is Date type (no time) or DateTime — affects parseDate formula | Systems | OPEN |
| LI-008 | Budget field: confirm whether to store as free-text string or parse into numeric min/max range | Will | OPEN |
| LI-009 | Airtable field names: all field names in the mapping table must be confirmed against the live schema before build — use `get_table_schema(appdZ49WqgjRXxA1R, tblTlSB9CO4dTGodg)` to verify | Systems | OPEN |
| LI-010 | M-SLACK-ALERTS webhook URL: must be registered and recorded before Module 10 can be configured | Systems | OPEN |

---

## 18. Final Scenario Status

**Status: PENDING BUILD**

> This document is the authoritative build specification for M-LEAD-INTAKE. No Make.com scenario has been created yet. Begin build only after all Open Issues marked as Will or Luciana owner are resolved, and after the Go/No-Go checklist in Section 16 is signed off.

**Build sequence dependency:**
1. Build M-SLACK-ALERTS first (needed for Module 10 webhook URL)
2. Build M-BRAND-ROUTER logic block (embedded in M-LEAD-INTAKE)
3. Build M-LEAD-INTAKE (incorporates both above)
4. Test end-to-end: M-LEAD-INTAKE → M-SLACK-ALERTS
