# STAGE_1_IMPLEMENTATION_GUIDE
## She Said Sail + Mare Executive — Make.com Stage 1 Build
### Step-by-Step Implementation Reference for Senior Systems Builder

**Status:** PRODUCTION IMPLEMENTATION GUIDE
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** 8 Stage 1 Make Scenarios — Lead to Booking Confirmation Pipeline
**Classification:** Confidential — Internal Systems Documentation
**Reference Architecture:** MAKE_MASTER_ARCHITECTURE.md (this folder)
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Implementation Authority Statement**
>
> This guide is the step-by-step build reference for Stage 1. It is read alongside MAKE_MASTER_ARCHITECTURE.md, which governs all security, idempotency, error handling, and environment standards. This guide covers implementation sequence, module-by-module build steps, test procedures, and promotion gates. Any ambiguity between this guide and the master architecture is resolved by the master architecture.

---

## TABLE OF CONTENTS

| Section | Title |
|---------|-------|
| 1 | Pre-Implementation Checklist |
| 2 | Make Folder Structure Setup |
| 3 | Implementation Order and Rationale |
| 4 | Scenario Build Guide — M-AUDIT-LOGGER |
| 5 | Scenario Build Guide — M-BRAND-ROUTER |
| 6 | Scenario Build Guide — M-LEAD-INTAKE |
| 7 | Scenario Build Guide — M-SLACK-ALERTS |
| 8 | Scenario Build Guide — M-CONCIERGE-ASSIGNMENT |
| 9 | Scenario Build Guide — M-BOOKING-CREATION |
| 10 | Scenario Build Guide — M-STRIPE-DEPOSIT |
| 11 | Scenario Build Guide — M-BOOKING-CONFIRMATION |
| 12 | Inter-Scenario Dependencies |
| 13 | Sandbox Test Flow |
| 14 | Production Promotion Checklist |
| 15 | Rollback Procedures |
| 16 | Human Approval Gates |
| 17 | Known Blockers |
| 18 | Success Criteria |

---

## SECTION 1 — PRE-IMPLEMENTATION CHECKLIST

Complete every item in this checklist before opening Make and building a single scenario. Attempting to build without these items in place wastes time and creates security risks.

### 1.1 Credentials Required

Collect and verify each credential before starting. Store ALL credentials in Make's built-in connection vault — never in a text file, Slack message, or email.

| Credential | Where to Get It | Make Connection Name | Status |
|------------|----------------|---------------------|--------|
| Airtable Personal Access Token (main base) | Airtable → Developer Hub → Personal Access Tokens | `SSS-Airtable-Production` | [ ] Verified |
| Airtable Personal Access Token (sandbox base) | Same — scoped to sandbox base only | `SSS-Airtable-Sandbox` | [ ] Verified |
| Stripe Secret Key — Test Mode | Stripe Dashboard → Developers → API Keys → Secret key (test) | `SSS-Stripe-Test` | [ ] Verified |
| Stripe Webhook Signing Secret | Stripe Dashboard → Developers → Webhooks → Add endpoint → Signing secret | `SSS-Stripe-Webhook-Secret` (stored in Data Store) | [ ] Verified |
| Slack Bot OAuth Token | Slack API → Your Apps → SSS Ops Bot → OAuth & Permissions → Bot Token | `SSS-Slack-Bot` | [ ] Verified |
| Gmail OAuth (SSS) | Google Workspace → hello@shesaidsail.com → OAuth connection in Make | `SSS-Gmail-Hello` | [ ] Verified |
| Gmail OAuth (ME) | Google Workspace → hello@mareexecutive.com → OAuth connection in Make | `ME-Gmail-Hello` | [ ] Verified |
| Claude API Bearer Token | Anthropic Console → API Keys | `SSS-Claude-API` | [ ] Verified |
| Quo SMS API Key | Quo SMS Dashboard → API Settings | `SSS-QuoSMS` (connect but suppress Stage 1) | [ ] Verified |

### 1.2 Airtable Configuration Verification

Before building Make scenarios that write to Airtable, verify these table and field prerequisites exist. If any are missing, do NOT proceed — fix Airtable first.

**Requests Table (tblTlSB9CO4dTGodg) — Required Fields:**

| Field Name | Type | Notes |
|-----------|------|-------|
| Status | Single Select | Must include: NEW, ASSIGNED, AVAILABILITY_CONFIRMED, BOOKING_CREATED |
| Brand | Single Select | Must include: SSS, ME |
| Environment | Single Select | Must include: Production, Sandbox |
| Source_System | Single Select | Must include: Make, Manual, API |
| Idempotency_Key | Single Line Text | Must exist; must be indexed for fast search |
| Assigned_Concierge | Linked Record | Links to Concierge_Operators table |
| Agent_Status | Single Select | Must include: AI_RESPONDING, HUMAN_REVIEW, ESCALATED, CLOSED |
| Last_AI_Action | DateTime | |
| AI_Confidence_Score | Number | 0–100 |

**Bookings Table (tbl72omPibBkn2hZL) — Required Fields:**

| Field Name | Type | Notes |
|-----------|------|-------|
| Status | Single Select | Must include: AVAILABILITY_PENDING, AVAILABILITY_CONFIRMED, DEPOSIT_SENT, DEPOSIT_PAID, CONFIRMED |
| Brand | Single Select | SSS, ME |
| Environment | Single Select | Production, Sandbox |
| Emergency_Flag | Checkbox | |
| Automations_Paused | Checkbox | |
| Stripe_Deposit_Link | URL | |
| Stripe_Payment_Link_ID | Single Line Text | |
| Confirmation_Sent_At | DateTime | |
| Request_ID | Linked Record | Links to Requests table |

**Audit Log Table (tblrMpTfMk8q1eNHp) — Required Fields:**

| Field Name | Type | Notes |
|-----------|------|-------|
| Audit_Key | Single Line Text | Indexed |
| Event_Type | Single Select | Full list per Section 8 of master architecture |
| Scenario_Name | Single Line Text | |
| Brand | Single Select | SSS, ME |
| Environment | Single Select | Production, Sandbox |
| Actor | Single Select | Make, Claude, Human |
| Affected_Record_ID | Single Line Text | |
| Affected_Table | Single Line Text | |
| Prompt_Version_ID | Single Line Text | |
| Outcome | Single Select | SUCCESS, FAILURE, SKIP |
| Timestamp | DateTime | |

**Clients Table (tblr84vRIWC5HmKvo) — Required Fields:**

| Field Name | Type | Notes |
|-----------|------|-------|
| Email | Email | Must be indexed |
| Brand | Single Select | SSS, ME |
| Environment | Single Select | Production, Sandbox |
| Source_System | Single Select | Make, Manual |

**Founder Decisions Table (tblFCE26qDwfp4Jwd) — Required Fields:**

| Field Name | Type | Notes |
|-----------|------|-------|
| Decision_Type | Single Select | Must include: SEV-2, STAGE_1_COMPLETE, EMERGENCY |
| Status | Single Select | OPEN, RESOLVED, ESCALATED |
| Brand | Single Select | SSS, ME |
| Environment | Single Select | Production, Sandbox |

### 1.3 Make Workspace Configuration

| Item | Required State | Status |
|------|---------------|--------|
| Make team workspace created | Yes | [ ] Done |
| Workspace name set to `She Said Sail + Mare Executive` | Yes | [ ] Done |
| Make Data Store created and named `SSS-Config` | Yes | [ ] Done |
| Data Store keys populated (see Section 4.1 of master architecture) | Yes | [ ] Done |
| Make Connections — all 9 connections created and tested | Yes | [ ] Done |
| Sandbox base ID confirmed and loaded into Data Store | Yes | [ ] Done |

### 1.4 Webhook URL Registration

After building each webhook-triggered scenario, register the webhook URL with the sending system. Do NOT start testing until URLs are registered.

| Scenario | Sending System | Where to Register |
|----------|---------------|------------------|
| M-BRAND-ROUTER | Webflow, Typeform | Form → Settings → Webhooks → Add endpoint |
| M-STRIPE-DEPOSIT (inbound) | Stripe | Stripe Dashboard → Developers → Webhooks → Add endpoint → paste Make URL |

Stripe webhook events to register:
- `payment_intent.succeeded`
- `payment_link.payment.completed`
- `checkout.session.completed`

### 1.5 Sandbox Base Preparation

Create a dedicated Airtable sandbox base that mirrors the production schema. It does not need real data. It needs the correct tables, fields, and select option values. Name it: `SSS Sandbox — Stage 1 Testing`. Record its base ID and load it into the Make Data Store as `SANDBOX_AIRTABLE_BASE_ID`.

---

## SECTION 2 — MAKE FOLDER STRUCTURE SETUP

Create the exact folder structure below before creating any scenarios. Scenarios created without a home folder must be moved before testing begins.

**Steps:**
1. Open Make workspace
2. Navigate to Scenarios → New Folder
3. Create the following folders in exact order:

```
Top Level:
  ├── SSS — She Said Sail
  ├── ME — Mare Executive
  ├── SHARED — Cross-Brand Scenarios
  └── ARCHIVED

Under SHARED:
  ├── Core Infrastructure
  ├── Stripe Events
  ├── Emergency Protocol
  └── Scheduled Jobs

Under SSS — She Said Sail:
  ├── Stage 1 — Lead to Booking
  ├── Stage 2 — Charter Execution      [placeholder — do not build yet]
  ├── Stage 3 — Intelligence            [placeholder — do not build yet]
  └── Stage 4 — Growth                  [placeholder — do not build yet]

Under ME — Mare Executive:
  ├── Stage 1 — Lead to Booking
  ├── Stage 2 — Charter Execution      [placeholder — do not build yet]
  ├── Stage 3 — Intelligence            [placeholder — do not build yet]
  └── Stage 4 — Growth                  [placeholder — do not build yet]
```

All 8 Stage 1 scenarios live in `SHARED / Core Infrastructure` or `SHARED / Stripe Events`. Stage 1 scenarios are brand-agnostic at the infrastructure level — brand routing happens inside the scenarios.

---

## SECTION 3 — IMPLEMENTATION ORDER AND RATIONALE

Build scenarios in this exact sequence. The rationale explains why each scenario must exist before the next one can be built and tested.

| Build Order | Scenario | Rationale |
|------------|----------|-----------|
| 1st | M-AUDIT-LOGGER | Every other scenario calls this one. It must exist and be testable before any other scenario can log. Build it first; test it standalone. |
| 2nd | M-BRAND-ROUTER | Entry point for all inbound leads. Must be stable before M-LEAD-INTAKE can receive a routed payload. |
| 3rd | M-LEAD-INTAKE | Creates the Airtable Request record that triggers scenarios 4 and 5. Cannot be tested without M-BRAND-ROUTER passing a payload. |
| 4th | M-SLACK-ALERTS | Triggered by Airtable watch on new Request records. Requires Request records to exist (from M-LEAD-INTAKE). |
| 5th | M-CONCIERGE-ASSIGNMENT | Also triggered by new Request records. Must be built after M-SLACK-ALERTS because both watch the same trigger — build order prevents trigger collision during testing. |
| 6th | M-BOOKING-CREATION | Creates Booking records from qualified Requests. Requires Requests to exist (M-LEAD-INTAKE) and Concierge to be assigned (M-CONCIERGE-ASSIGNMENT). |
| 7th | M-STRIPE-DEPOSIT | Triggers on Booking status change from M-BOOKING-CREATION. Requires Bookings to exist before this scenario can be triggered and tested. |
| 8th | M-BOOKING-CONFIRMATION | Final confirmation step. Requires the full pipeline (lead → request → booking → deposit link) to work before this is meaningful to test. |

---

## SECTION 4 — SCENARIO BUILD GUIDE: M-AUDIT-LOGGER

### 4.1 Purpose
Writes immutable Audit Log records to Airtable. Called by every other scenario via internal HTTP webhook. Build and test this first — no other scenario is complete without a working logger.

### 4.2 Trigger Configuration
**Type:** Instant (Webhook)
**Method:** POST
**URL:** Copy the Make-generated webhook URL after creation. Store in Data Store as `INTERNAL_AUDIT_WEBHOOK_URL`.

### 4.3 Module Sequence

```
Module 1: Webhook (Instant trigger)
  → Receives JSON payload from calling scenario
  → Required fields: event_type, scenario_name, brand, environment,
    actor, affected_record_id, affected_table, prompt_version_id,
    outcome, error_code, notes

Module 2: Tools → Set Variable
  → audit_key = {{scenario_name}}_{{affected_record_id}}_{{event_type}}_{{formatDate(now, 'YYYYMMDD')}}
  → timestamp_utc = {{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}

Module 3: Airtable → Search Records
  → Connection: SSS-Airtable-Sandbox (or Production per environment)
  → Table: Audit Log (tblrMpTfMk8q1eNHp)
  → Filter: {Audit_Key} = {{audit_key}}
  → Max records: 1
  → Purpose: deduplication check

Module 4: Router (conditional)
  → Path A: IF Module 3 found records AND timestamp within 60 seconds
      → Tools → Set Variable: outcome = "SKIP_DUPLICATE"
      → HTTP → Make a request: POST to INTERNAL_AUDIT_WEBHOOK_URL
        with minimal WARN payload (no infinite loop — use a flag field)
      → Stop (do not create duplicate)
  → Path B: IF no match (new unique event)
      → Continue to Module 5

Module 5: Airtable → Create a Record
  → Connection: SSS-Airtable-Sandbox
  → Table: Audit Log
  → Fields:
      Audit_Key:          {{audit_key}}
      Event_Type:         {{event_type}}
      Scenario_Name:      {{scenario_name}}
      Brand:              {{brand}}
      Environment:        {{environment}}
      Actor:              {{actor}}
      Affected_Record_ID: {{affected_record_id}}
      Affected_Table:     {{affected_table}}
      Prompt_Version_ID:  {{prompt_version_id}}
      Outcome:            {{outcome}}
      Error_Code:         {{error_code}}
      Timestamp:          {{timestamp_utc}}
      Notes:              {{notes}}

Module 6: Error Handler (attached to Module 5)
  → On error: HTTP POST to Slack webhook (hardcoded fallback — not via SSS-Slack-Bot)
  → Message: "CRITICAL: Audit Log write failed. Scenario: {{scenario_name}}. Record: {{affected_record_id}}. Time: {{timestamp_utc}}"
  → Recipient: Will's DM (personal Slack webhook URL stored in Data Store as WILL_SLACK_DM_WEBHOOK)
```

### 4.4 Sandbox Test Procedure
1. Enable scenario
2. Send test POST to webhook URL with sample payload:
```json
{
  "event_type": "REQUEST_CREATED",
  "scenario_name": "M-LEAD-INTAKE",
  "brand": "SSS",
  "environment": "Sandbox",
  "actor": "Make",
  "affected_record_id": "TEST-001",
  "affected_table": "Requests",
  "prompt_version_id": "",
  "outcome": "SUCCESS",
  "error_code": "",
  "notes": "Sandbox test — M-AUDIT-LOGGER standalone verification"
}
```
3. Verify: record appears in Audit Log table with all fields populated
4. Send identical payload a second time within 60 seconds
5. Verify: no duplicate record created; second call suppressed by deduplication check

---

## SECTION 5 — SCENARIO BUILD GUIDE: M-BRAND-ROUTER

### 5.1 Purpose
Classifies every inbound lead as SSS or ME. Mandatory first step in pipeline.

### 5.2 Trigger Configuration
**Type:** Instant (Webhook)
**Method:** POST
**Security:** Bearer token validation must be Module 1 — no processing before auth check.

### 5.3 Module Sequence

```
Module 1: Webhook (Instant trigger)
  → Receives raw lead payload

Module 2: Tools → Set Variable
  → incoming_brand = null (initial state)

Module 3: Router — Brand Classification Logic
  Path A: IF payload.form_id EXISTS in brand_form_map Data Store key
    → Set incoming_brand = brand_form_map[payload.form_id]
    → (Map: each Webflow/Typeform form ID maps to SSS or ME)

  Path B: ELSE IF payload.brand EXISTS and IN ['SSS', 'ME']
    → Set incoming_brand = payload.brand

  Path C: ELSE IF payload.page_url CONTAINS 'mareexecutive'
    → Set incoming_brand = 'ME'

  Path D: ELSE IF payload.page_url CONTAINS 'shesaidsail' OR NULL
    → Set incoming_brand = 'SSS'

  Path E: ELSE (unclassifiable — Claude fallback)
    → HTTP Module: POST to Claude API
    → System prompt: "Classify the following lead submission as either SSS (She Said Sail, luxury consumer sailing charter) or ME (Mare Executive, premium corporate/executive charter) based on the inquiry text, email domain, and context. Return JSON: {brand: 'SSS'|'ME', confidence: 0-100, reason: string}"
    → Parse response → Set incoming_brand = response.brand
    → If confidence < 70: still apply brand but flag for review

Module 4: HTTP → POST to Slack (conditional — only if Path E taken OR confidence < 70)
  → Channel: #sss-ops-alerts
  → Message: "Brand classification used Claude fallback. Lead: {{email}}. Brand assigned: {{incoming_brand}}. Confidence: {{confidence}}. Manual review advised."

Module 5: Tools → Set Variable
  → enriched_payload = merge(original_payload, {brand: incoming_brand})

Module 6: HTTP → Make a request
  → Method: POST
  → URL: M-LEAD-INTAKE webhook URL (from Data Store: LEAD_INTAKE_WEBHOOK_URL)
  → Headers: Authorization: Bearer {{INTERNAL_WEBHOOK_TOKEN}}
  → Body: {{enriched_payload}}

Module 7: HTTP → POST to M-AUDIT-LOGGER webhook
  → Payload: {event_type: "LEAD_CLASSIFIED", scenario_name: "M-BRAND-ROUTER",
    brand: {{incoming_brand}}, environment: {{ENV}}, actor: "Make",
    affected_record_id: {{payload.email}}, affected_table: "N/A",
    outcome: "SUCCESS", notes: "Classification method: {{path_taken}}"}

Module 8: Error Handler (global)
  → Catch all errors
  → Log to M-AUDIT-LOGGER with outcome: "FAILURE"
  → Post to #sss-ops-alerts
```

### 5.4 Data Store: brand_form_map
Create a Data Store record mapping form IDs to brands:
```
{
  "wf_form_abc123": "SSS",
  "wf_form_def456": "ME",
  "tf_form_ghi789": "SSS",
  "tf_form_jkl012": "ME"
}
```
Update this map every time a new form is added. It is the primary classification signal.

### 5.5 Sandbox Test Procedure
1. POST test payload with `form_id` matching a known SSS entry → verify brand = SSS
2. POST test payload with `brand: "ME"` explicit field → verify brand = ME
3. POST test payload with `page_url` containing "mareexecutive.com" → verify brand = ME
4. POST test payload with no classification signals → verify Claude fallback fires; Slack alert appears; brand still assigned
5. Verify M-LEAD-INTAKE receives the enriched payload in each case

---

## SECTION 6 — SCENARIO BUILD GUIDE: M-LEAD-INTAKE

### 6.1 Purpose
Creates the Airtable Request record. Deduplicates against existing records. Stores idempotency key.

### 6.2 Trigger Configuration
**Type:** Instant (Webhook — called by M-BRAND-ROUTER)
**Method:** POST

### 6.3 Airtable Field Mapping

| Payload Field | Airtable Field | Notes |
|--------------|---------------|-------|
| `email` | Email | Required |
| `first_name` | First_Name | Required |
| `last_name` | Last_Name | Required |
| `phone` | Phone | Optional |
| `charter_date` | Charter_Date | Required — validate date format |
| `group_size` | Group_Size | Required — validate integer |
| `brand` | Brand | Set by M-BRAND-ROUTER — never from raw payload |
| `occasion` | Occasion | Optional |
| `message` | Inquiry_Message | Optional |
| `form_id` | Source_Form_ID | |
| `page_url` | Source_URL | |
| computed | Idempotency_Key | SHA256(email+charter_date+brand) |
| system | Status | Always: NEW |
| system | Source_System | Always: Make |
| system | Environment | From Data Store: current environment |
| system | Created_At | formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ') |

### 6.4 Module Sequence

```
Module 1: Webhook (Instant trigger)
  → Receives enriched payload from M-BRAND-ROUTER

Module 2: Tools → Set Variable
  → idempotency_key = sha256({{email}} + {{charter_date}} + {{brand}})
  → Note: Make's SHA256 function: sha256(text)
  → Concatenate with no delimiter: {{email}}{{charter_date}}{{brand}}

Module 3: Airtable → Search Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests (tblTlSB9CO4dTGodg)
  → Filter formula: {Idempotency_Key} = "{{idempotency_key}}"
  → Max records: 1

Module 4: Router (duplicate check)
  Path A: IF Module 3 found record (duplicate detected)
    → Module 4a: HTTP POST to M-AUDIT-LOGGER
        event_type: "DUPLICATE_REJECTED"
        affected_record_id: {{Module3.id}}
        outcome: "SKIP"
        notes: "Duplicate key: {{idempotency_key}}"
    → Module 4b: Set Variable → response = {status: "DUPLICATE", request_id: {{Module3.id}}}
    → STOP (do not create record)

  Path B: IF no match (new unique lead)
    → Continue to Module 5

Module 5: Airtable → Create a Record
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests
  → Fields: all mapped fields from Section 6.3

Module 6: HTTP POST to M-AUDIT-LOGGER
  → event_type: "REQUEST_CREATED"
  → affected_record_id: {{Module5.id}}
  → affected_table: "Requests"
  → brand: {{brand}}
  → outcome: "SUCCESS"

Module 7: Error Handler (attached to Module 5)
  → On Airtable write failure:
      → Retry: wait 2 minutes; attempt Module 5 again (max 2 retries)
      → After 3rd failure: POST to Slack #sss-ops-alerts
      → After 30 minutes unresolved: POST to M-AUDIT-LOGGER (outcome: FAILURE)
        + create Founder Decision record (Decision_Type: SEV-2)
```

### 6.5 Sandbox Test Procedure
1. Trigger full pipeline from M-BRAND-ROUTER with fresh test payload
2. Verify: Request record created in sandbox Airtable with all fields populated
3. Verify: Idempotency_Key field populated on record
4. Trigger again with identical payload (same email + charter_date + brand)
5. Verify: NO second Request record created; Audit Log shows DUPLICATE_REJECTED
6. Verify: M-AUDIT-LOGGER called and record exists for REQUEST_CREATED event

---

## SECTION 7 — SCENARIO BUILD GUIDE: M-SLACK-ALERTS

### 7.1 Purpose
Notifies the ops team in real time when a new lead Request record is created.

### 7.2 Trigger Configuration
**Type:** Airtable — Watch Records
**Table:** Requests (tblTlSB9CO4dTGodg)
**Filter:** Status = NEW

### 7.3 Module Sequence

```
Module 1: Airtable → Watch Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests
  → Trigger on: new records only
  → Filter: Status = "NEW"

Module 2: Router (brand channel selection)
  Path A: brand = SSS → channel = #sss-ops-alerts
  Path B: brand = ME  → channel = #me-ops-alerts (or #sss-ops-alerts as fallback)

Module 3: Slack → Create a Message
  → Connection: SSS-Slack-Bot
  → Channel: {{channel from Module 2}}
  → Message:
    ```
    :sailboat: *NEW LEAD — {{brand}}*

    *Name:* {{First_Name}} {{Last_Name}}
    *Email:* {{Email}}
    *Charter Date:* {{Charter_Date}}
    *Group Size:* {{Group_Size}}
    *Occasion:* {{Occasion}}
    *Request ID:* {{Record_ID}}

    <https://airtable.com/{{base_id}}/{{table_id}}/{{record_id}}|Open in Airtable>
    ```

Module 4: Airtable → Update a Record
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests
  → Record ID: {{Module1.id}}
  → Fields:
      Last_AI_Action: {{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}

Module 5: HTTP POST to M-AUDIT-LOGGER
  → event_type: "SLACK_ALERT_SENT"
  → affected_record_id: {{Module1.id}}
  → outcome: "SUCCESS"

Module 6: Error Handler (attached to Module 3)
  → Slack send failure:
      → Retry twice (2 minute interval)
      → After 3rd failure: log to Automation Failures table
      → Fallback: HTTP POST directly to Will's personal Slack webhook DM
```

### 7.4 Sandbox Test Procedure
1. Create a test Request record manually in Airtable sandbox with Status = NEW
2. Verify: Slack message appears in #sss-ops-alerts within 2 minutes
3. Verify: Airtable Request record's Last_AI_Action field is updated
4. Verify: Audit Log record created with event_type = SLACK_ALERT_SENT

---

## SECTION 8 — SCENARIO BUILD GUIDE: M-CONCIERGE-ASSIGNMENT

### 8.1 Purpose
Assigns an available concierge operator to the new Request. Updates Request status to ASSIGNED.

### 8.2 Trigger Configuration
**Type:** Airtable — Watch Records
**Table:** Requests
**Filter:** Status = NEW AND Assigned_Concierge is empty

**Important:** Use a separate Airtable Watch trigger from M-SLACK-ALERTS. Do not combine into one scenario — they have different downstream actions and different error handling requirements.

### 8.3 Module Sequence

```
Module 1: Airtable → Watch Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests
  → Filter: Status = "NEW" AND Assigned_Concierge is blank

Module 2: Airtable → Search Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Concierge_Operators
  → Filter: {Status} = "AVAILABLE" AND {Brand} = "{{Module1.Brand}}"
  → Sort: Current_Load (ascending) — lowest load first
  → Max records: 5

Module 3: Router (availability check)
  Path A: IF Module 2 returned 0 records (no concierge available)
    → Slack POST to #sss-ops-alerts: "No concierge available for {{Brand}} lead {{Record_ID}}. Manual assignment required."
    → Airtable Update Request: Agent_Status = "HUMAN_REVIEW"; Escalation_Reason = "No concierge available at time of intake"
    → HTTP POST to M-AUDIT-LOGGER (outcome: SKIP; notes: "No available concierge")
    → STOP

  Path B: IF Module 2 returned records
    → Continue to Module 4

Module 4: Tools → Set Variable
  → selected_concierge = Module2.records[0]
  → (Round-robin alternative: use Data Store key CONCIERGE_ROUND_ROBIN_INDEX; increment on each assignment)

Module 5: Airtable → Update a Record
  → Table: Requests
  → Record ID: {{Module1.id}}
  → Fields:
      Assigned_Concierge: [{{selected_concierge.id}}]  (linked record array)
      Status: "ASSIGNED"
      Last_AI_Action: {{now}}

Module 6: HTTP POST to M-AUDIT-LOGGER
  → event_type: "CONCIERGE_ASSIGNED"
  → affected_record_id: {{Module1.id}}
  → notes: "Assigned: {{selected_concierge.Name}}"
  → outcome: "SUCCESS"

Module 7: Error Handler
  → Airtable update failure → retry twice → Slack alert → Founder Decision SEV-2
```

### 8.4 Round-Robin Logic (Data Store Implementation)
```
Data Store key: CONCIERGE_ROUND_ROBIN_INDEX (integer)

At assignment:
  1. Read current index
  2. Select concierge at position: index MOD available_count
  3. Increment index by 1
  4. Write new index back to Data Store
```

### 8.5 Sandbox Test Procedure
1. Ensure at least 2 records in Concierge_Operators table with Status = AVAILABLE and Brand = SSS
2. Trigger pipeline with test lead
3. Verify: Request record's Assigned_Concierge field is populated
4. Verify: Request Status = ASSIGNED
5. Create 3 test leads in sequence; verify round-robin selects different concierges
6. Set all concierges to UNAVAILABLE; trigger test lead; verify HUMAN_REVIEW path fires and Slack alert appears

---

## SECTION 9 — SCENARIO BUILD GUIDE: M-BOOKING-CREATION

### 9.1 Purpose
Creates the Booking record in Airtable when a Request has been assigned and availability is confirmed. Links Booking → Request → Client.

### 9.2 Trigger Configuration
**Type:** Airtable — Watch Records
**Table:** Requests
**Filter:** Status = AVAILABILITY_CONFIRMED

Note: Status = AVAILABILITY_CONFIRMED is set by Luciana manually after verifying availability, OR by a future M-AVAILABILITY-CHECK scenario (Stage 2). In Stage 1, Luciana manually changes this field.

### 9.3 Module Sequence

```
Module 1: Airtable → Watch Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Requests
  → Filter: Status = "AVAILABILITY_CONFIRMED"

Module 2: Airtable → Search Records (Booking dedup)
  → Table: Bookings (tbl72omPibBkn2hZL)
  → Filter: {Request_ID} = "{{Module1.id}}"
  → Max records: 1

Module 3: Router (booking dedup check)
  Path A: IF booking exists for this Request
    → HTTP POST to M-AUDIT-LOGGER (outcome: SKIP; event: DUPLICATE_REJECTED)
    → STOP (do not create second booking)
  Path B: No existing booking → continue

Module 4: Airtable → Search Records (Client dedup)
  → Table: Clients (tblr84vRIWC5HmKvo)
  → Filter: {Email} = "{{Module1.Email}}"
  → Max records: 1

Module 5: Router (client dedup)
  Path A: Client exists → client_id = Module4.records[0].id
           → HTTP POST to M-AUDIT-LOGGER (event: CLIENT_LINKED)
  Path B: No client → continue to Module 6

Module 6 (Path B only): Airtable → Create a Record
  → Table: Clients
  → Fields:
      Name: {{First_Name}} {{Last_Name}}
      Email: {{Email}}
      Phone: {{Phone}}
      Brand: {{Brand}}
      Environment: {{ENV}}
      Source_System: Make
  → Set client_id = new record ID
  → HTTP POST to M-AUDIT-LOGGER (event: CLIENT_CREATED)

Module 7: Airtable → Create a Record
  → Table: Bookings
  → Fields:
      Status:             "AVAILABILITY_PENDING"
      Brand:              {{Brand}}
      Environment:        {{ENV}}
      Source_System:      Make
      Request_ID:         [{{Module1.id}}]
      Client:             [{{client_id}}]
      Charter_Date:       {{Charter_Date}}
      Group_Size:         {{Group_Size}}
      Occasion:           {{Occasion}}
      Emergency_Flag:     false
      Automations_Paused: false
      City:               {{City}} (if in payload; else blank for Luciana to set)

Module 8: Airtable → Update a Record
  → Table: Requests
  → Record ID: {{Module1.id}}
  → Fields:
      Status: "BOOKING_CREATED"

Module 9: HTTP POST to M-AUDIT-LOGGER
  → event_type: "BOOKING_CREATED"
  → affected_record_id: {{Module7.id}}
  → affected_table: "Bookings"
  → notes: "Linked to Request {{Module1.id}}; Client {{client_id}}"
  → outcome: "SUCCESS"

Module 10: Error Handler (global — wraps Modules 6, 7, 8)
  → Any failure triggers: rollback attempt (update Request status back to AVAILABILITY_CONFIRMED)
  → Log failure to Automation Failures table
  → Slack alert to #sss-ops-alerts
  → If Booking was partially created: flag record Status = VOID; log to Audit Log with CORRECTION note
```

### 9.4 Sandbox Test Procedure
1. Manually set a sandbox Request record Status to AVAILABILITY_CONFIRMED
2. Verify: Booking record created in sandbox with Status = AVAILABILITY_PENDING
3. Verify: Booking linked to the Request record
4. Verify: Client record created OR existing client linked (test both paths)
5. Change same Request status to AVAILABILITY_CONFIRMED again (simulate re-trigger)
6. Verify: NO second Booking created; Audit Log shows DUPLICATE_REJECTED

---

## SECTION 10 — SCENARIO BUILD GUIDE: M-STRIPE-DEPOSIT

### 10.1 Purpose
Creates a Stripe test-mode Payment Link for the deposit amount. Writes the link back to the Booking record.

### 10.2 Trigger Configuration
**Type:** Airtable — Watch Records
**Table:** Bookings
**Filter:** Status = AVAILABILITY_CONFIRMED AND Stripe_Deposit_Link is empty

### 10.3 Module Sequence

```
Module 1: Airtable → Watch Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Bookings
  → Filter: Status = "AVAILABILITY_CONFIRMED" AND Stripe_Deposit_Link blank

Module 2: Airtable → Get a Record (fetch full booking data)
  → Table: Bookings
  → Record ID: {{Module1.id}}

Module 3: Tools → Check Circuit Breaker
  → Data Store → Get key: STRIPE_CIRCUIT_STATE
  → IF value = "OPEN": jump to Module 3a (circuit breaker path)
  → IF value = "CLOSED" or "HALF_OPEN": continue to Module 4

Module 3a (Circuit Breaker OPEN path):
  → HTTP POST to M-AUDIT-LOGGER (event: CIRCUIT_BREAKER_TRIGGERED; outcome: SKIP)
  → Airtable Update Booking: add note to Charter_Notes = "Stripe deposit link creation skipped — circuit breaker OPEN at {{now}}"
  → STOP

Module 4: Tools → Check Emergency Flag
  → IF Module2.Emergency_Flag = true: exit
      → HTTP POST to M-AUDIT-LOGGER (outcome: SKIP; notes: "Emergency_Flag active")
      → STOP

Module 5: Tools → Set Variable (Stripe idempotency key)
  → stripe_idem_key = "stripe_" + {{Module2.Record_ID}} + "_deposit_" + formatDate(now, 'YYYYMMDDHH')

Module 6: HTTP → Make a request (Stripe API — create Payment Link)
  → Connection: SSS-Stripe-Test
  → URL: https://api.stripe.com/v1/payment_links
  → Method: POST
  → Headers:
      Authorization: Bearer {{STRIPE_TEST_SECRET_KEY}}
      Idempotency-Key: {{stripe_idem_key}}
  → Body (form-encoded):
      line_items[0][price_data][currency]: usd
      line_items[0][price_data][unit_amount]: {{deposit_amount_cents}}
      line_items[0][price_data][product_data][name]: "Charter Deposit — {{Brand}} — {{Module2.Charter_Date}}"
      line_items[0][quantity]: 1
      metadata[booking_id]: {{Module2.id}}
      metadata[brand]: {{Brand}}
      metadata[environment]: Sandbox

Module 7: Router (Stripe response check)
  Path A: Success (HTTP 200)
    → Continue to Module 8
  Path B: Error
    → Data Store: increment STRIPE_ERROR_COUNT
    → IF STRIPE_ERROR_COUNT >= 3: set STRIPE_CIRCUIT_STATE = "OPEN"
    → HTTP POST to M-AUDIT-LOGGER (outcome: FAILURE; error_code: {{http_status}})
    → Retry after 2 minutes (handled by Make retry settings on Module 6)

Module 8: Airtable → Update a Record
  → Table: Bookings
  → Record ID: {{Module2.id}}
  → Fields:
      Stripe_Deposit_Link:    {{Module6.url}}
      Stripe_Payment_Link_ID: {{Module6.id}}
      Status:                 "DEPOSIT_SENT"

Module 9: HTTP POST to M-AUDIT-LOGGER
  → event_type: "STRIPE_DEPOSIT_LINK_CREATED"
  → affected_record_id: {{Module2.id}}
  → notes: "Stripe link ID: {{Module6.id}}; Test mode: YES"
  → outcome: "SUCCESS"

Module 10: Error Handler
  → Stripe failure: route through circuit breaker logic; max 3 retries; then Founder Decision SEV-2
  → Airtable write failure: retry twice; Slack alert; do NOT mark Status = DEPOSIT_SENT until confirmed written
```

### 10.4 Sandbox Test Procedure
1. Manually set a sandbox Booking Status to AVAILABILITY_CONFIRMED (with no existing deposit link)
2. Verify: Stripe test-mode Payment Link created (visible in Stripe test dashboard)
3. Verify: Booking record updated with Stripe_Deposit_Link URL and Stripe_Payment_Link_ID
4. Verify: Booking Status = DEPOSIT_SENT
5. Set STRIPE_CIRCUIT_STATE = "OPEN" in Data Store; trigger again
6. Verify: scenario exits without calling Stripe; CIRCUIT_BREAKER_TRIGGERED appears in Audit Log
7. Reset STRIPE_CIRCUIT_STATE = "CLOSED"
8. Set Booking Emergency_Flag = true; trigger
9. Verify: scenario exits; Audit Log shows SKIP reason Emergency_Flag

---

## SECTION 11 — SCENARIO BUILD GUIDE: M-BOOKING-CONFIRMATION

### 11.1 Purpose
Sends booking confirmation to client after deposit is received. In Stage 1: internal test address only. Claude generates the brand-appropriate email.

### 11.2 Trigger Configuration
**Type:** Airtable — Watch Records
**Table:** Bookings
**Filter:** Status = DEPOSIT_PAID

Note: Status = DEPOSIT_PAID is set by Stripe webhook handler (future M-STRIPE-WEBHOOK scenario in Stage 2). In Stage 1 sandbox testing, Luciana manually sets this status to trigger the confirmation test.

### 11.3 Module Sequence

```
Module 1: Airtable → Watch Records
  → Connection: SSS-Airtable-Sandbox
  → Table: Bookings
  → Filter: Status = "DEPOSIT_PAID"

Module 2: Airtable → Get a Record (full booking)
  → Table: Bookings
  → Record ID: {{Module1.id}}

Module 3: Airtable → Get a Record (linked client)
  → Table: Clients
  → Record ID: {{Module2.Client[0].id}}

Module 4: Guards — Exit conditions check
  → IF Emergency_Flag = true: exit + audit log SKIP
  → IF Automations_Paused = true: exit + audit log SKIP
  → IF Environment = "Production" AND Stage1_Mode = true: force test recipient
  → IF Confirmation_Sent_At is NOT empty: exit (already confirmed; dedup) + audit log SKIP

Module 5: Tools → Set Variable (test mode enforcement)
  → recipient_email = IF(ENV = "Sandbox", "hello@shesaidsail.com", Module3.Email)
  → Stage 1 rule: ALWAYS use internal test address

Module 6: HTTP → Make a request (Claude API — generate confirmation email)
  → URL: https://api.anthropic.com/v1/messages
  → Method: POST
  → Headers:
      x-api-key: {{CLAUDE_API_KEY}}
      anthropic-version: 2023-06-01
      Content-Type: application/json
  → Body:
    {
      "model": "claude-sonnet-4-6",
      "max_tokens": 1024,
      "system": "You are the concierge communication system for {{Brand}}. {{brand_voice_instruction}}. Generate a professional, warm booking confirmation email. Use only confirmed data from the context provided. Do not invent, estimate, or infer any details not present in the context.",
      "messages": [{
        "role": "user",
        "content": "Generate a booking confirmation email.\n\nClient: {{Module3.Name}}\nCharter Date: {{Module2.Charter_Date}}\nGroup Size: {{Module2.Group_Size}}\nOccasion: {{Module2.Occasion}}\nBooking ID: {{Module2.Record_ID}}\nBrand: {{Brand}}\n\nInclude: confirmation of deposit received, charter date, next steps (balance timing), contact information. Do not include pricing details beyond deposit confirmation."
      }]
    }

Module 7: Tools → Parse Claude response
  → email_body = Module6.content[0].text

Module 8: Gmail → Send an Email
  → Connection: SSS-Gmail-Hello (for SSS) OR ME-Gmail-Hello (for ME)
  → To: {{recipient_email}} (test address in Stage 1)
  → Subject: "Your Charter is Confirmed — {{Brand}} | {{Module2.Charter_Date}}"
  → Body: {{email_body}}

Module 9: Airtable → Update a Record (only after confirmed send)
  → Table: Bookings
  → Record ID: {{Module2.id}}
  → Fields:
      Status:               "CONFIRMED"
      Confirmation_Sent_At: {{formatDate(now, 'YYYY-MM-DDTHH:mm:ssZ')}}

Module 10: HTTP POST to M-AUDIT-LOGGER
  → event_type: "BOOKING_CONFIRMATION_SENT"
  → affected_record_id: {{Module2.id}}
  → notes: "Recipient: {{recipient_email}} (test mode). Brand: {{Brand}}. Prompt used: AIV-current."
  → outcome: "SUCCESS"

Module 11: Error Handler
  → Gmail failure: retry twice; do NOT update Status = CONFIRMED until email confirmed sent
  → Claude failure (timeout): retry once with reduced prompt; if second failure: Slack alert; queue for human send
  → Claude content refusal: immediate Slack alert to #sss-ops-alerts; do not retry; route to Luciana for manual send
```

### 11.4 Brand Voice Instruction (Data Store)

Store brand voice instructions in Data Store, not in the scenario module directly:

```
BRAND_VOICE_SSS:
"She Said Sail tone: warm, celebratory, premium but approachable. Customers are celebrating life moments. Lead with their excitement. Use first name. No corporate language."

BRAND_VOICE_ME:
"Mare Executive tone: polished, efficient, discreet. Clients are executives and corporate event planners. Lead with professionalism and precision. Confirm logistics clearly. No casual language."
```

### 11.5 Sandbox Test Procedure
1. Manually set a sandbox Booking Status to DEPOSIT_PAID
2. Verify: Gmail email sent to hello@shesaidsail.com (internal test)
3. Open email — verify: brand-appropriate tone, correct charter date, correct Booking ID, no invented details
4. Verify: Booking Status = CONFIRMED in Airtable
5. Verify: Confirmation_Sent_At timestamp populated
6. Verify: Audit Log contains BOOKING_CONFIRMATION_SENT event with prompt_version_id
7. Set Confirmation_Sent_At to a past value; trigger again; verify: SKIP fires (no duplicate email)
8. Set Emergency_Flag = true; trigger; verify: email NOT sent; SKIP logged

---

## SECTION 12 — INTER-SCENARIO DEPENDENCIES

### 12.1 Dependency Map

```
External Source → [webhook POST] → M-BRAND-ROUTER
                                        │
                                        │ [HTTP POST]
                                        ▼
                                   M-LEAD-INTAKE
                                        │
                                        │ [Airtable record created → Status=NEW]
                                        ▼
                         ┌──────────────┴──────────────┐
                         ▼                             ▼
                   M-SLACK-ALERTS          M-CONCIERGE-ASSIGNMENT
                   (parallel)              (parallel)
                         │                             │
                         └──────────────┬──────────────┘
                                        │ [Luciana sets Status=AVAILABILITY_CONFIRMED]
                                        ▼
                                M-BOOKING-CREATION
                                        │
                                        │ [Airtable: Booking created, Status=AVAILABILITY_PENDING]
                                        │ [Luciana confirms availability → Status=AVAILABILITY_CONFIRMED]
                                        ▼
                                M-STRIPE-DEPOSIT
                                        │
                                        │ [Airtable: Status=DEPOSIT_SENT]
                                        │ [Client pays → Stripe webhook → Status=DEPOSIT_PAID]
                                        │ [Stage 1: Luciana manually sets Status=DEPOSIT_PAID]
                                        ▼
                               M-BOOKING-CONFIRMATION
                                        │
                                        │ [Airtable: Status=CONFIRMED]
                                        ▼
                               Pipeline Complete (Stage 1)

All scenarios → [HTTP POST] → M-AUDIT-LOGGER (at completion of each action)
```

### 12.2 Manual Gates in Stage 1

Two status transitions require human action in Stage 1. These are intentional — Stage 2 will automate them.

| Gate | Who Sets It | When | Future Automation |
|------|-------------|------|------------------|
| Request Status → AVAILABILITY_CONFIRMED | Luciana | After manually checking yacht availability | M-AVAILABILITY-CHECK (Stage 2) |
| Booking Status → DEPOSIT_PAID | Luciana (sandbox) / Stripe webhook (production) | After deposit received | M-STRIPE-WEBHOOK (Stage 2) |

---

## SECTION 13 — SANDBOX TEST FLOW

### 13.1 Full Pipeline Test — Fake Lead to Audit Verification

Run this test suite in order after all 8 scenarios are built. Do not run it until all 8 are in place.

**Test Lead Data:**
```
First Name: Test
Last Name:  Sandbox
Email:      sandbox-test@shesaidsail.com
Phone:      +1-555-000-0001
Charter Date: [30 days from today]
Group Size: 8
Brand:      SSS
Occasion:   Anniversary
Form ID:    [SSS test form ID]
```

**Step-by-Step Test Procedure:**

| Step | Action | Expected Result | Pass/Fail |
|------|--------|----------------|-----------|
| 1 | POST test payload to M-BRAND-ROUTER webhook | Brand = SSS set on payload | [ ] |
| 2 | Observe M-LEAD-INTAKE | Request record created in sandbox Airtable | [ ] |
| 3 | Check Airtable Request record | All fields mapped; Idempotency_Key populated; Status = NEW | [ ] |
| 4 | Observe Slack | Message appears in #sss-ops-alerts within 2 minutes | [ ] |
| 5 | Check Airtable Request record | Assigned_Concierge populated; Status = ASSIGNED | [ ] |
| 6 | Check Audit Log | REQUEST_CREATED, SLACK_ALERT_SENT, CONCIERGE_ASSIGNED events present | [ ] |
| 7 | POST same payload again (duplicate test) | No second Request record; DUPLICATE_REJECTED in Audit Log | [ ] |
| 8 | Manually set Request Status = AVAILABILITY_CONFIRMED | — | [ ] |
| 9 | Observe M-BOOKING-CREATION | Booking record created; linked to Request and Client | [ ] |
| 10 | Check Airtable Booking record | Status = AVAILABILITY_PENDING; all fields populated | [ ] |
| 11 | Check Clients table | Client record created for sandbox-test@shesaidsail.com | [ ] |
| 12 | Manually set Booking Status = AVAILABILITY_CONFIRMED | — | [ ] |
| 13 | Observe M-STRIPE-DEPOSIT | Stripe test Payment Link created | [ ] |
| 14 | Check Airtable Booking record | Stripe_Deposit_Link populated; Status = DEPOSIT_SENT | [ ] |
| 15 | Check Stripe test dashboard | Payment Link exists with correct metadata | [ ] |
| 16 | Manually set Booking Status = DEPOSIT_PAID | — | [ ] |
| 17 | Observe M-BOOKING-CONFIRMATION | Email sent to hello@shesaidsail.com | [ ] |
| 18 | Open test email | Brand voice correct; Booking ID correct; no invented data | [ ] |
| 19 | Check Airtable Booking record | Status = CONFIRMED; Confirmation_Sent_At populated | [ ] |
| 20 | Check Audit Log | All 8 event types present for this test lead run | [ ] |

### 13.2 Edge Case Tests

| Test | Procedure | Expected Result |
|------|-----------|----------------|
| Brand ME routing | POST payload with form_id mapped to ME | Brand = ME; message in #sss-ops-alerts with ME label |
| No concierge available | Set all concierges Status = UNAVAILABLE; submit lead | Slack alert; Request Status = HUMAN_REVIEW |
| Emergency Flag block | Set Booking Emergency_Flag = true; trigger deposit | Deposit scenario exits; CIRCUIT_BREAKER_TRIGGERED logged |
| Automations_Paused block | Set Automations_Paused = true; trigger confirmation | Confirmation NOT sent; SKIP logged |
| Circuit breaker trigger | Set STRIPE_CIRCUIT_STATE = OPEN; trigger deposit | Scenario exits immediately; Audit Log records skip |
| Claude classification fallback | POST payload with no form_id, no brand field, no URL | Claude API called; Slack alert for manual review; brand still assigned |

---

## SECTION 14 — PRODUCTION PROMOTION CHECKLIST

Complete every item before any scenario is promoted from Sandbox to Production. This checklist requires Will sign-off before Production switch.

### 14.1 Technical Verification

- [ ] All 8 scenarios pass full sandbox test suite (Section 13)
- [ ] All edge case tests pass (Section 13.2)
- [ ] Audit Log contains records for ALL event types in catalog
- [ ] No open L3 or L4 errors from any scenario
- [ ] Idempotency: duplicate lead test passed and verified
- [ ] Circuit breaker: OPEN state test passed and verified
- [ ] Emergency_Flag: block test passed and verified
- [ ] Rollback procedure tested for each scenario (Section 15)
- [ ] All Make connections tested with production credentials (NOT sandbox credentials)
- [ ] Stripe webhook URL registered with production Make webhook endpoint (NOT sandbox URL)
- [ ] Production Airtable base ID confirmed in Data Store (`PRODUCTION_AIRTABLE_BASE_ID`)
- [ ] Production bearer token rotated and updated in all webhook configurations
- [ ] Gmail OAuth connections verified sending from correct addresses
- [ ] Data Store environment variable `ENV` set to `PRODUCTION`

### 14.2 Governance Verification

- [ ] Founder Decision record created: Decision_Type = STAGE_1_PRODUCTION_PROMOTION
- [ ] Will has reviewed and approved all 8 scenario configurations
- [ ] Audit Log table in production base is empty (no sandbox test data leaked to production)
- [ ] Rollback contact chain confirmed: Will → Luciana escalation path tested via Slack DM

### 14.3 Production Promotion Sequence

Promote scenarios in this order. Do not promote all at once.

| Promotion Order | Scenario | Verification After Promotion |
|----------------|----------|------------------------------|
| 1 | M-AUDIT-LOGGER | Send test event; verify production Audit Log record created |
| 2 | M-BRAND-ROUTER | Submit test lead; verify classified and passed to M-LEAD-INTAKE |
| 3 | M-LEAD-INTAKE | Verify Request record created in production base |
| 4 | M-SLACK-ALERTS | Verify Slack message in #sss-ops-alerts |
| 5 | M-CONCIERGE-ASSIGNMENT | Verify concierge assignment on production Request |
| 6 | M-BOOKING-CREATION | Manually gate Request; verify Booking created in production |
| 7 | M-STRIPE-DEPOSIT | Verify test-mode link created (Stripe stays test-mode in initial production promotion) |
| 8 | M-BOOKING-CONFIRMATION | Verify confirmation email to internal address (still test-mode) |

---

## SECTION 15 — ROLLBACK PROCEDURES

### 15.1 Per-Scenario Rollback

**M-AUDIT-LOGGER Rollback**
Cannot roll back — append-only. If misconfigured: disable scenario; fix configuration; re-enable. All previously written records remain. Document any bad records with CORRECTION event records.

**M-BRAND-ROUTER Rollback**
1. Disable M-BRAND-ROUTER in Make (toggle OFF)
2. Luciana manually tags all inbound leads with brand in Airtable
3. M-LEAD-INTAKE continues to work — it accepts manually-enriched payloads
4. Fix issue; re-test in sandbox; re-enable
5. Review all leads received during outage — verify brand tags are correct

**M-LEAD-INTAKE Rollback**
1. Disable M-LEAD-INTAKE in Make
2. Luciana creates Request records manually in Airtable
3. All downstream triggers (M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT) continue to work off Airtable watch
4. No data loss risk — manual entries carry all required fields
5. Fix issue; re-test; re-enable

**M-SLACK-ALERTS Rollback**
1. Disable M-SLACK-ALERTS in Make
2. Luciana monitors Requests table directly in Airtable (saved view: "New Requests Today")
3. Zero data impact — this scenario reads only, writes only a timestamp
4. Fix and re-enable within the hour

**M-CONCIERGE-ASSIGNMENT Rollback**
1. Disable M-CONCIERGE-ASSIGNMENT
2. Luciana manually assigns concierge by editing the Assigned_Concierge field
3. No data loss risk
4. Fix and re-enable

**M-BOOKING-CREATION Rollback** (Will-only)
1. Disable M-BOOKING-CREATION immediately
2. Audit any Booking records created in the error window — check for: missing Client link, missing Request link, incorrect Status
3. For any malformed Booking: set Status = VOID; create CORRECTION Audit Log entry
4. Luciana creates Booking records manually if needed
5. Do not re-enable without Will approval and sandbox re-test

**M-STRIPE-DEPOSIT Rollback** (Will-only)
1. Disable M-STRIPE-DEPOSIT immediately
2. In Stripe Dashboard: archive any Payment Links created during the error window that were duplicates or incorrectly configured
3. Luciana sends deposit links manually (Stripe Dashboard → Payment Links → Create)
4. Document each manual link in the Booking record's Charter_Notes field
5. Do not re-enable without investigating root cause

**M-BOOKING-CONFIRMATION Rollback** (Will-only)
1. Disable M-BOOKING-CONFIRMATION immediately
2. Check Gmail sent items at hello@shesaidsail.com and hello@mareexecutive.com for the error window
3. If any real client email was sent in error (should be impossible in Stage 1 test mode but verify):
   - Will contacts client directly within 1 hour
   - Document in Emergency Escalations table
4. Luciana sends confirmation emails manually from correct brand address
5. Do not re-enable without prompt version review and Will approval

---

## SECTION 16 — HUMAN APPROVAL GATES

The following actions require Will's explicit approval before proceeding. No scenario, automation, or Luciana-initiated action bypasses these gates.

| Gate | Description | Approval Method | Documentation |
|------|-------------|----------------|---------------|
| Stage 1 Production Promotion | Moving any scenario from Sandbox to Production | Founder Decision record + Will Slack confirmation | Founder Decisions table |
| Stripe live-mode activation | Switching M-STRIPE-DEPOSIT from test to live keys | Will changes Data Store + Founder Decision | Founder Decisions table |
| Real client email activation | Removing Stage 1 test-mode email guard | Will edits scenario directly + Founder Decision | Founder Decisions table |
| Prompt version change | Any change to Claude system prompts used in scenarios | Will approval + AI_Prompt_Versions record updated | AI_Prompt_Versions table |
| Connection credential rotation | Any credential rotation for production connections | Will executes rotation + logs in Audit Log | Audit Log |
| Circuit breaker reset (production) | Resetting STRIPE_CIRCUIT_STATE from OPEN to CLOSED after a Stripe error storm | Will reviews incident first | Founder Decisions or direct Will action |
| SEV-2 resolution | Any Founder Decision record of type SEV-2 requires Will to mark RESOLVED | Will edits record directly | Founder Decisions table |
| New scenario promotion | Any new scenario not in this Stage 1 guide | Full sandbox test cycle + Will approval | Founder Decisions table |

---

## SECTION 17 — KNOWN BLOCKERS

These blockers must be resolved before the affected scenario can be built, tested, or promoted to production.

| Blocker ID | Affected Scenario | Description | Resolution Path | Owner | Status |
|------------|------------------|-------------|----------------|-------|--------|
| BLK-001 | All scenarios | `Environment` field not confirmed present on all required Airtable tables | Verify each table in Airtable; add field if missing; each field must include `Production` and `Sandbox` as select options | Will / Builder | [ ] Open |
| BLK-002 | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION | Stripe webhook URL not yet registered in Stripe Dashboard | After building M-STRIPE-DEPOSIT, copy Make webhook URL; register in Stripe Dashboard under Developers → Webhooks | Builder | [ ] Open |
| BLK-003 | M-BRAND-ROUTER | brand_form_map Data Store not populated with actual Webflow/Typeform form IDs | Will provides form IDs from Webflow and Typeform accounts; Builder populates Data Store | Will | [ ] Open |
| BLK-004 | M-CONCIERGE-ASSIGNMENT | Concierge_Operators table not confirmed in production Airtable base | Verify table exists in appdZ49WqgjRXxA1R; if missing, Will creates table with required fields before this scenario can be built | Will | [ ] Open |
| BLK-005 | M-BOOKING-CONFIRMATION | Claude prompt version ID (AIV-NNNN) not yet created for booking confirmation prompt | Will must create an AI_Prompt_Versions record for the Stage 1 booking confirmation prompt; get the AIV ID before building this scenario | Will | [ ] Open |
| BLK-006 | All scenarios | Sandbox Airtable base not yet created | Will creates sandbox base that mirrors production schema; shares base ID with Builder | Will | [ ] Open |
| BLK-007 | M-SLACK-ALERTS | `#me-ops-alerts` Slack channel may not exist | Verify channel exists or confirm fallback to #sss-ops-alerts is acceptable for Stage 1 | Will | [ ] Open |
| BLK-008 | M-BOOKING-CREATION | Concierge_Operators table — linked record field from Requests not yet configured | Verify Assigned_Concierge field on Requests table is a Linked Record type pointing to Concierge_Operators table | Will | [ ] Open |

---

## SECTION 18 — SUCCESS CRITERIA

Stage 1 is complete and eligible for Stage 2 promotion when ALL of the following are true. Will signs off on this checklist as a Founder Decision record.

### 18.1 Functional Criteria

| Criterion | Verification Method | Pass |
|-----------|-------------------|------|
| Every inbound test lead is classified as SSS or ME within 30 seconds | Submit 10 test leads of each brand type; check Audit Log timestamps | [ ] |
| No duplicate Request records created when same lead submitted twice | Submit identical payload 5 times; verify only 1 record exists | [ ] |
| Every new Request generates a Slack alert within 2 minutes | Submit 5 test leads; verify 5 Slack messages with correct data | [ ] |
| Every Request is assigned a concierge within 2 minutes of creation | Submit 5 test leads; verify Assigned_Concierge populated on all | [ ] |
| Every qualified Request generates a Booking record with no duplicate | Run 5 through AVAILABILITY_CONFIRMED gate; verify 5 unique Bookings | [ ] |
| Every AVAILABILITY_CONFIRMED Booking generates a Stripe test Payment Link | Manually set 3 Bookings to AVAILABILITY_CONFIRMED; verify 3 links created | [ ] |
| Every DEPOSIT_PAID Booking triggers a confirmation email to internal test address | Manually set 3 Bookings to DEPOSIT_PAID; verify 3 emails received | [ ] |
| Audit Log contains records for every action in every test run | Count events in Audit Log; no gaps | [ ] |
| All 4 error handling levels fire correctly for simulated failures | Simulate L1, L2, L3, L4 error conditions per scenario; verify responses | [ ] |
| Emergency_Flag = true blocks all downstream actions | Set flag on 2 Bookings mid-pipeline; verify all automations exit | [ ] |
| Circuit breaker opens after 3 Stripe errors | Simulate 3 Stripe failures; verify OPEN state in Data Store | [ ] |

### 18.2 Governance Criteria

| Criterion | Verification Method | Pass |
|-----------|-------------------|------|
| Founder Decision record created: STAGE_1_COMPLETE | Check Founder Decisions table (tblFCE26qDwfp4Jwd) | [ ] |
| Will has reviewed Audit Log for full test suite run | Will confirms in Slack or Founder Decisions note | [ ] |
| All scenario rollback procedures tested and documented | Each rollback procedure in Section 15 executed once in sandbox | [ ] |
| Production promotion checklist (Section 14) complete | Checklist reviewed item by item with Will | [ ] |
| All known blockers (Section 17) resolved | Blocker table: all items marked as resolved | [ ] |

### 18.3 Stage 2 Unlock Condition

Stage 2 begins only after:
1. This Stage 1 success criteria checklist is 100% complete
2. Will creates Founder Decision: `STAGE_2_AUTHORIZED`
3. All Stage 1 scenarios are running stably in production for a minimum of 72 hours with no L3 or L4 errors
4. Luciana has confirmed operational readiness for charter execution automation scope

---

*Document Authority: This implementation guide is the definitive build reference for Stage 1. All scenario construction, testing, and promotion decisions follow this guide. Amendments require Founder Decision record and version increment.*

*Last Updated: May 2026 | Version: 1.0 | Owner: Will (Founder)*
*Reference: MAKE_MASTER_ARCHITECTURE.md | Constitutional: 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED*
