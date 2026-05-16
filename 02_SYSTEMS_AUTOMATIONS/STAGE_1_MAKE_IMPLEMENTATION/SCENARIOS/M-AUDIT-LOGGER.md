# M-AUDIT-LOGGER — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Cross-Scenario Sub-Scenario (called by ALL scenarios)  
**Execution Order:** Final step of every Stage 1 scenario before completion

---

## 1. Scenario Name

`M-AUDIT-LOGGER`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here. Every other Stage 1 scenario references this ID for its outbound call. Update all callers when this ID is assigned:
> - M-BRAND-ROUTER
> - M-LEAD-INTAKE
> - M-SLACK-ALERTS
> - M-CONCIERGE-ASSIGNMENT
> - M-STRIPE-DEPOSIT
> - M-BOOKING-CREATION
> - M-BOOKING-CONFIRMATION

---

## 3. Trigger Type

**Pattern:** Sub-scenario — called by ALL other Stage 1 scenarios as their final step before completion.

**Invocation method:** HTTP POST to M-AUDIT-LOGGER's Make webhook URL. The webhook receives a structured JSON payload assembled by the calling scenario.

**M-AUDIT-LOGGER does not initiate any business logic.** It is a write-only, append-only logging sub-scenario. Its sole function is to receive a structured payload and write exactly one Airtable Audit Log record per invocation.

**Calling scenarios invoke M-AUDIT-LOGGER synchronously** — they wait for a success/failure signal before completing. This ensures each calling scenario knows whether its action was logged.

**Webhook URL:** To be registered in Make.com upon scenario creation. Provide to all calling scenarios at build time.

**Webhook input schema:**

```json
{
  "triggering_event": "string",
  "source_data": "string",
  "scenario_name": "string",
  "output": "string",
  "destination": "string",
  "approval_state": "string",
  "brand": "string",
  "city": "string",
  "environment": "string",
  "affected_record_id": "string",
  "prompt_version": "string | null",
  "ai_confidence_score": "number | null"
}
```

---

## 4. Purpose — Design Principle

**M-AUDIT-LOGGER exists because every autonomous action must be traceable.**

In a Make.com automation system where scenarios execute asynchronously and invisibly, the Audit Log is the system's memory. It answers:
- What did the system do?
- When did it do it?
- What data did it act on?
- Who or what triggered it?
- Was a human involved?
- What was the result?

**Core design principles:**

1. **One record per autonomous action.** Each time a Tier A scenario takes an action on behalf of the business (creating a Booking, sending a Slack alert, generating a Stripe link), exactly one Audit Log record is written. No batching. No summarizing. One action = one log entry.

2. **The Audit Log is append-only.** M-AUDIT-LOGGER only creates records. It never updates or deletes them. The Airtable Audit Log table (`tblrMpTfMk8q1eNHp`) has no Make automation configured to modify existing records.

3. **A failed Audit Log write is a system-level failure (SEV-1).** If M-AUDIT-LOGGER cannot write its record, the calling scenario's action is effectively unverifiable. The system treats this as a critical reliability failure, not a soft error.

4. **M-AUDIT-LOGGER must be built and operational before any other Stage 1 scenario goes to sandbox.** All other scenarios depend on it being functional.

5. **M-AUDIT-LOGGER has no retry logic on the Airtable write.** If the write fails, it fails immediately and signals failure to the caller. Retry is the caller's responsibility. This keeps M-AUDIT-LOGGER simple and fast.

---

## 5. Exact Module Sequence

### Module 1 — [Webhook] Receive Audit Payload

**Make Module Type:** Webhooks — Custom Webhook  
**Method:** POST  
**Content-Type:** `application/json`

**Expected payload fields (all required unless marked optional):**

| Field Name            | Type            | Required | Description                                          |
|-----------------------|-----------------|----------|------------------------------------------------------|
| `triggering_event`    | String          | YES      | What triggered the calling scenario                  |
| `source_data`         | String          | YES      | Record IDs and key field values the scenario used    |
| `scenario_name`       | String          | YES      | Name of the calling scenario (e.g., `M-LEAD-INTAKE`)|
| `output`              | String          | YES      | What was produced by the calling scenario            |
| `destination`         | String          | YES      | Where the output was written/sent                    |
| `approval_state`      | String          | YES      | One of: `AUTONOMOUS`, `PENDING_HUMAN`, `HUMAN_APPROVED`, `HUMAN_REJECTED` |
| `brand`               | String          | YES      | `SSS` or `ME`                                        |
| `city`                | String          | YES      | City market (e.g., `Miami`, `NYC`)                  |
| `environment`         | String          | YES      | `Production`, `Sandbox`, or `Development`            |
| `affected_record_id`  | String          | YES      | Airtable record ID of the primary record acted upon  |
| `prompt_version`      | String or null  | OPTIONAL | AI prompt version — null in Stage 1                  |
| `ai_confidence_score` | Number or null  | OPTIONAL | AI confidence — null in Stage 1                      |

**Webhook response behavior:**
- On success (Airtable write succeeds): return HTTP 200 with `{"status": "logged", "audit_log_record_id": "{{created_record_id}}"}`
- On validation failure: return HTTP 400 with `{"status": "rejected", "reason": "{{missing_field_name}} is required"}`
- On Airtable write failure: return HTTP 500 with `{"status": "failed", "reason": "Airtable write error — see Slack alert"}`

---

### Module 2 — [Tools] Validate Payload — Check Required Fields

**Make Module Type:** Tools — Set Multiple Variables  
**Purpose:** Verify all required fields are present and non-empty before attempting the Airtable write.

**Validation logic (implemented as a Router with conditions):**

```
Required fields checklist:
- {{1.triggering_event}} is not empty
- {{1.source_data}} is not empty
- {{1.scenario_name}} is not empty
- {{1.output}} is not empty
- {{1.destination}} is not empty
- {{1.approval_state}} is one of: AUTONOMOUS, PENDING_HUMAN, HUMAN_APPROVED, HUMAN_REJECTED
- {{1.brand}} is one of: SSS, ME
- {{1.environment}} is one of: Production, Sandbox, Development
- {{1.affected_record_id}} is not empty
```

**Set variables:**
```
payload_valid = true (if all pass) | false (if any fail)
validation_error = "{{field_name}} is required or invalid" (if any fail)
log_timestamp = {{now}} (capture once; use consistently in Module 3)
```

**If `payload_valid = false`:**
1. Immediately post to Slack #sss-ops-alerts: "M-AUDIT-LOGGER: Invalid payload received from `{{1.scenario_name}}`. Missing/invalid field: `{{validation_error}}`. Audit log NOT written. Investigate calling scenario immediately."
2. Return HTTP 400 to calling scenario
3. Stop execution — do not attempt Airtable write with invalid data

---

### Module 3 — [Airtable] Create Audit Log Record

**Make Module Type:** Airtable — Create a Record  
**Table:** Audit Log (`tblrMpTfMk8q1eNHp`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Runs only when:** `{{payload_valid}} = true`

**Complete field mapping — see Section 7 (Airtable Field Mapping) for full specification.**

**On success:** Capture `{{3.id}}` as `audit_log_record_id`. Proceed to Module 4 Route A.  
**On failure:** Proceed to Module 4 Route B (Airtable write error handler).

---

### Module 4 — [Router] Write Succeeded vs. Write Failed

**Make Module Type:** Router (built-in)  
**Purpose:** Branch based on whether the Airtable Create in Module 3 succeeded.

**Route A — Success:**
- Condition: `{{3.id}}` is not empty (record was created)
- Action: Return HTTP 200 to calling scenario webhook with body: `{"status": "logged", "audit_log_record_id": "{{3.id}}"}`
- No further action

**Route B — Failure (Airtable write error):**
- Condition: `{{3.id}}` is empty OR Module 3 threw an error
- Action: Proceed to Module 5 (SEV-1 failure handler)

---

### Module 5 — [Slack + Webhook Response] SEV-1 Failure Handler

**Make Module Type (5a):** Slack — Create a Message  
**Channel:** `#sss-ops-alerts`  
**Priority:** IMMEDIATE — this fires before any other response

**Slack message:**
```
:rotating_light: *SEV-1: AUDIT LOG WRITE FAILED*

An autonomous action has been taken but NOT logged in the Audit Log.
This is a critical system reliability failure requiring immediate investigation.

*Calling Scenario:* {{1.scenario_name}}
*Triggering Event:* {{1.triggering_event}}
*Affected Record:* {{1.affected_record_id}}
*Brand:* {{1.brand}} | *City:* {{1.city}}
*Environment:* {{1.environment}}
*Timestamp:* {{log_timestamp}}

*Action Required:*
1. Manually create an Audit Log record in Airtable for this action
2. Investigate the Airtable API error (check Make execution log for Module 3 error details)
3. Confirm M-AUDIT-LOGGER's Airtable connection is authenticated and functional
4. Do NOT restart M-AUDIT-LOGGER until the root cause is identified

*Full payload for manual entry:*
Triggering Event: {{1.triggering_event}}
Source Data: {{1.source_data}}
Output: {{1.output}}
Destination: {{1.destination}}
Approval State: {{1.approval_state}}
```

**Make Module Type (5b):** Webhooks — Webhook Response  
**Status:** 500  
**Body:** `{"status": "failed", "reason": "Airtable write failed — SEV-1 alert sent to #sss-ops-alerts. Manual audit entry required."}`

> The 500 response signals to the calling scenario that the audit write failed, allowing the caller to include this failure in its own error handling (most callers will log an additional Slack message at this point).

---

## 6. Complete Audit Log Payload Schema

This is the authoritative schema that ALL calling scenarios must use when assembling their payload for M-AUDIT-LOGGER. Deviation from this schema will cause a validation failure (Module 2).

```json
{
  "triggering_event": "string — what triggered the calling scenario. Be specific. Include record IDs and values.",
  "source_data": "string — Airtable record IDs and key field values the scenario read or acted on. Pipe-delimited for multiple values.",
  "scenario_name": "string — exact scenario name, e.g., M-LEAD-INTAKE, M-STRIPE-DEPOSIT",
  "output": "string — what the scenario produced. Include record IDs of anything created. Be specific.",
  "destination": "string — where the output was written or sent. Include table IDs for Airtable, channel names for Slack, etc.",
  "approval_state": "AUTONOMOUS | PENDING_HUMAN | HUMAN_APPROVED | HUMAN_REJECTED",
  "brand": "SSS | ME",
  "city": "string — city market. Use consistent casing: Miami, NYC, etc.",
  "environment": "Production | Sandbox | Development",
  "affected_record_id": "string — Airtable record ID (rec...) of the primary record that was created, updated, or acted upon",
  "prompt_version": "string | null — null for all Stage 1 scenarios. Will be populated when AI modules are activated.",
  "ai_confidence_score": "number | null — null for all Stage 1 scenarios. Will be populated when AI modules are activated."
}
```

**Payload examples by calling scenario:**

**From M-LEAD-INTAKE:**
```json
{
  "triggering_event": "New form submission received — source: Website SSS, email: client@example.com",
  "source_data": "Webhook payload: First_Name=Jane, Last_Name=Smith, Email=client@example.com, Charter_Date=2026-07-15, Group_Size=8, Brand_hint=SSS",
  "scenario_name": "M-LEAD-INTAKE",
  "output": "Request record created: REQ-2026-0042 (recXXXXXXXXXXXXXX). Duplicate check: PASSED (no existing record for this email+date).",
  "destination": "Airtable Requests table tblTlSB9CO4dTGodg",
  "approval_state": "AUTONOMOUS",
  "brand": "SSS",
  "city": "Miami",
  "environment": "Sandbox",
  "affected_record_id": "recXXXXXXXXXXXXXX",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

**From M-STRIPE-DEPOSIT:**
```json
{
  "triggering_event": "Deposit link generation requested for Request REQ-2026-0042 — Amount: $500.00 — Brand: SSS",
  "source_data": "Request record ID: recXXXXXXXXXXXXXX | Package_Price: 2500.00 | Deposit_Rate: 20% | Deposit_Amount: 500.00 | Client_Email: client@example.com",
  "scenario_name": "M-STRIPE-DEPOSIT",
  "output": "Stripe Payment Link created: https://buy.stripe.com/XXXXXXX | Request.Deposit_Link updated | Request.Status set to DEPOSIT_SENT",
  "destination": "Stripe API (Payment Links) + Airtable Requests table tblTlSB9CO4dTGodg",
  "approval_state": "AUTONOMOUS",
  "brand": "SSS",
  "city": "Miami",
  "environment": "Sandbox",
  "affected_record_id": "recXXXXXXXXXXXXXX",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

**From M-BOOKING-CREATION:**
```json
{
  "triggering_event": "Booking creation triggered for Request REQ-2026-0042 after Stripe deposit link confirmed",
  "source_data": "Request record ID: recXXXXXXXXXXXXXX | Client record ID: recYYYYYYYYYYYYYY (existing) | Deposit_Link present: true",
  "scenario_name": "M-BOOKING-CREATION",
  "output": "Booking record created: BK-2026-0001 (recZZZZZZZZZZZZZZ) | Client linked: recYYYYYYYYYYYYYY | Request.Booking_ID updated | Slack notification sent",
  "destination": "Airtable Bookings table tbl72omPibBkn2hZL + Airtable Requests table tblTlSB9CO4dTGodg + Slack #sss-ops-alerts",
  "approval_state": "AUTONOMOUS",
  "brand": "SSS",
  "city": "Miami",
  "environment": "Sandbox",
  "affected_record_id": "recZZZZZZZZZZZZZZ",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

**From M-BOOKING-CONFIRMATION:**
```json
{
  "triggering_event": "Confirmation email draft prepared for Booking BK-2026-0001 after Booking record creation",
  "source_data": "Booking record ID: recZZZZZZZZZZZZZZ | Client record ID: recYYYYYYYYYYYYYY | Brand: SSS | Charter_Date: 2026-07-15",
  "scenario_name": "M-BOOKING-CONFIRMATION",
  "output": "SSS confirmation email draft written to Booking.Confirmation_Email_Draft | Confirmation_Status=DRAFT_READY | Slack notification sent to #sss-ops-alerts for manual send by Luciana",
  "destination": "Airtable Bookings table tbl72omPibBkn2hZL (draft fields) + Slack #sss-ops-alerts",
  "approval_state": "PENDING_HUMAN",
  "brand": "SSS",
  "city": "Miami",
  "environment": "Sandbox",
  "affected_record_id": "recZZZZZZZZZZZZZZ",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

---

## 7. Complete Airtable Field Mapping — Audit Log Record Creation

Every field written to the Audit Log table (`tblrMpTfMk8q1eNHp`) per invocation of M-AUDIT-LOGGER.

| Airtable Field Name    | Field Type          | Value / Source                                              | Notes                                                   |
|------------------------|---------------------|-------------------------------------------------------------|---------------------------------------------------------|
| `Log_ID`               | Formula (read-only) | Auto-generated by Airtable: `AUD-` + YEAR + `-` + NNNN    | Do NOT write; Airtable formula field                    |
| `Timestamp`            | Date/Time           | `{{log_timestamp}}` — captured in Module 2                  | ISO 8601 with timezone; use Make `{{now}}` at receipt   |
| `Triggering_Event`     | Long text           | `{{1.triggering_event}}`                                    | Full string from payload                                |
| `Source_Data`          | Long text           | `{{1.source_data}}`                                         | Full string from payload                                |
| `Scenario_Name`        | Single line text    | `{{1.scenario_name}}`                                       | Exact scenario name                                     |
| `Output`               | Long text           | `{{1.output}}`                                              | Full string from payload                                |
| `Destination`          | Single line text    | `{{1.destination}}`                                         | Full string from payload                                |
| `Approval_State`       | Single select       | `{{1.approval_state}}`                                      | Must match Airtable choices: AUTONOMOUS, PENDING_HUMAN, HUMAN_APPROVED, HUMAN_REJECTED |
| `Brand`                | Single select       | `{{1.brand}}`                                               | SSS or ME                                               |
| `City`                 | Single select       | `{{1.city}}`                                                | Must match Airtable city choices                        |
| `Environment`          | Single select       | `{{1.environment}}`                                         | Production, Sandbox, or Development                     |
| `Record_ID`            | Single line text    | `{{1.affected_record_id}}`                                  | Airtable record ID (rec...) of primary affected record  |
| `Prompt_Version`       | Single line text    | `{{1.prompt_version}}` (null → empty string)                | Null in Stage 1; populated in Stage 2+ when AI active   |
| `AI_Confidence_Score`  | Number              | `{{1.ai_confidence_score}}` (null → empty)                  | Null in Stage 1; 0-100 score when AI active             |
| `Make_Run_ID`          | Single line text    | `{{bundle.bundleOrder}}` or Make execution ID               | Links Audit Log to specific Make execution for debugging|
| `Payload_Hash`         | Single line text    | MD5 or SHA-1 of full payload string (see idempotency, Section 9) | Used for duplicate detection                     |

**Field type notes for Airtable configuration:**

- `Approval_State` must be a Single Select field with exactly these choices: `AUTONOMOUS`, `PENDING_HUMAN`, `HUMAN_APPROVED`, `HUMAN_REJECTED`. Do not add additional choices without updating this spec.
- `City` must be a Single Select field. Choices must match the Requests and Bookings tables' City choices exactly.
- `Brand` must be a Single Select field with choices: `SSS`, `ME`.
- `Environment` must be a Single Select field with choices: `Production`, `Sandbox`, `Development`.
- `Record_ID` is a plain text field — NOT a linked record field. The Audit Log is intentionally not linked to other tables to prevent cascading deletes or record dependencies.

---

## 8. Why Audit Log Failures Are Treated as SEV-1

**Definition:** SEV-1 (Severity 1) is the highest priority incident classification. It requires immediate human response and overrides all other work.

**The argument:**

Every action M-AUDIT-LOGGER is asked to log has already happened. The booking was created. The Stripe link was generated. The Slack message was sent. These cannot be un-done. If M-AUDIT-LOGGER fails to write the log record, there is a gap in the system's official record — an action the system took that is not in the Audit Log.

This matters for:

1. **Compliance and accountability.** Will and Luciana need to be able to reconstruct exactly what the system did at any point in time. A gap in the Audit Log means they cannot do this.

2. **Debugging.** When something goes wrong (wrong deposit amount, wrong email sent, wrong booking status), the Audit Log is the primary forensic tool. A missing entry means the root cause may be impossible to find.

3. **Founder confidence.** Will delegated autonomous action to this system on the condition that every action is logged. An unlogged autonomous action violates this agreement.

4. **Cascade failures.** An M-AUDIT-LOGGER failure is often a symptom of a broader Airtable API issue. If Airtable is having trouble accepting writes, it may be failing silently on other writes too (booking creation, status updates). The SEV-1 alert prompts investigation across all Airtable-dependent scenarios, not just the logging step.

**Response protocol for M-AUDIT-LOGGER SEV-1:**

1. Luciana or Will acknowledges the Slack alert within 15 minutes during business hours
2. Manually create the missing Audit Log record in Airtable using the payload data in the Slack alert
3. Check Make.com execution logs for M-AUDIT-LOGGER to identify the specific error
4. Check Airtable API status (airtablestatus.com) for platform-wide issues
5. Test M-AUDIT-LOGGER with a manual webhook call before restarting automated scenarios
6. Document the incident as a corrective Audit Log entry once M-AUDIT-LOGGER is restored

---

## 9. Idempotency — Preventing Duplicate Log Entries

**The problem:** A calling scenario may call M-AUDIT-LOGGER, the Airtable write may succeed, but the HTTP response back to the caller may fail. The caller, not knowing the write succeeded, may call M-AUDIT-LOGGER again during its error handling or retry logic. This would create a duplicate Audit Log entry.

**Solution: Payload Hash deduplication**

**Step 1 — Hash generation (Module 2, during variable setup):**
```
payload_string = {{1.scenario_name}} + "|" + {{1.triggering_event}} + "|" + {{1.affected_record_id}} + "|" + {{1.output}}
payload_hash = md5(payload_string)
```
(Use Make's built-in `md5()` function, or the `sha1()` function if MD5 is unavailable.)

**Step 2 — Duplicate check (between Module 2 and Module 3):**
Before creating the Airtable record, search the Audit Log table for a record with the same `Payload_Hash`:

```
[Airtable] Search Records — Audit Log (tblrMpTfMk8q1eNHp)
Filter: {Payload_Hash} = "{{payload_hash}}"
Max records: 1
```

**Step 3 — Router branch on duplicate check:**
- If existing record found: return HTTP 200 to caller with `{"status": "already_logged", "audit_log_record_id": "{{existing_record_id}}"}`. Do NOT create a second record.
- If no existing record: proceed to Module 3 (create the record, including the `Payload_Hash` field).

**Collision risk acknowledgment:** MD5 hash collisions are theoretically possible but practically irrelevant at the volume of this system (fewer than 1,000 Audit Log entries per day). The hash is computed on payload content, not on metadata, so legitimate duplicate actions (same scenario, same record, same output) — which genuinely should be logged twice — will produce the same hash and be deduplicated. This is the correct behavior: if the action was truly duplicated, the first log entry covers it.

**When to override idempotency:** If an operator explicitly needs to force a second log entry for the same action (e.g., to document a manual re-run), they can add a `force_log = true` field to the payload and M-AUDIT-LOGGER will skip the hash check. This is a manual override only; no automated caller should ever send `force_log = true`.

---

## 10. Rollback — Audit Log Records Are Immutable

**No rollback exists for Audit Log records. This is by design.**

The Audit Log is an append-only record of what the system did. Deleting or modifying a log entry would undermine the entire purpose of the log.

**If wrong data was logged (incorrect field value, wrong record ID, etc.):**

Do not delete the incorrect record. Instead, create a corrective entry:

```json
{
  "triggering_event": "CORRECTIVE ENTRY: Manual correction for Audit Log record {{incorrect_record_id}}",
  "source_data": "Original incorrect entry: {{incorrect_record_id}} | Correction: {{description_of_what_was_wrong}}",
  "scenario_name": "MANUAL_CORRECTION",
  "output": "Corrective Audit Log entry created. See original entry {{incorrect_record_id}} for the erroneous record. Correct values: {{corrected_values}}",
  "destination": "Airtable Audit Log tblrMpTfMk8q1eNHp",
  "approval_state": "HUMAN_APPROVED",
  "brand": "{{brand}}",
  "city": "{{city}}",
  "environment": "{{environment}}",
  "affected_record_id": "{{original_affected_record_id}}",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

The corrective entry is written directly into Airtable by Luciana or Will, not via M-AUDIT-LOGGER (since the error may have been caused by M-AUDIT-LOGGER itself).

**After writing the corrective entry:** Add an internal note to the original incorrect Audit Log record in Airtable's `Notes_Internal` field (if present): "See corrective entry {{corrective_record_id}} — {{date}} — {{operator_name}}."

**Audit Log record deletion policy:** Audit Log records may only be deleted by Will. Deletion requires explicit written justification (stored in a separate deletion log). In practice, no records should ever need to be deleted — corrective entries replace the function of deletion.

---

## 11. Sandbox Test — Verification Checklist

Run the following verification steps after building M-AUDIT-LOGGER. It must be tested and confirmed working before any other Stage 1 scenario is built.

**Pre-test setup:**
- [ ] Airtable connection authenticated in Make.com (confirm API key and base access)
- [ ] Audit Log table (`tblrMpTfMk8q1eNHp`) confirmed to have all required fields (see Section 7)
- [ ] All Single Select fields have correct choices configured in Airtable
- [ ] M-AUDIT-LOGGER webhook URL noted and distributed to all calling scenario builders
- [ ] Slack #sss-ops-alerts connection authenticated

**Test 1 — Valid payload, happy path:**
- [ ] Send a valid JSON payload via HTTP POST to M-AUDIT-LOGGER webhook
- [ ] Verify: HTTP 200 response received with `{"status": "logged", "audit_log_record_id": "rec..."}`
- [ ] Verify: New record visible in Airtable Audit Log table with all fields populated
- [ ] Verify: `Timestamp` is correct
- [ ] Verify: `Log_ID` formula generated correctly (AUD-2026-NNNN format)
- [ ] Verify: `Payload_Hash` field is populated

**Test 2 — Invalid payload (missing required field):**
- [ ] Send payload with `affected_record_id` removed
- [ ] Verify: HTTP 400 response received with appropriate error message
- [ ] Verify: No Airtable record created
- [ ] Verify: Slack #sss-ops-alerts receives alert about invalid payload

**Test 3 — Idempotency (duplicate payload):**
- [ ] Send the exact same valid payload twice
- [ ] Verify: First call returns `{"status": "logged", ...}`
- [ ] Verify: Second call returns `{"status": "already_logged", "audit_log_record_id": "..."}` (same record ID)
- [ ] Verify: Only one record exists in Audit Log for this payload

**Test 4 — Simulated Airtable write failure:**
- [ ] Temporarily break the Airtable connection (wrong API key or invalid table ID)
- [ ] Send a valid payload
- [ ] Verify: HTTP 500 response received
- [ ] Verify: Slack #sss-ops-alerts receives SEV-1 alert with full payload data
- [ ] Verify: No Airtable record created (obviously)
- [ ] Restore correct Airtable connection after test

**Test 5 — Each calling scenario's audit log entry:**
Once all Stage 1 scenarios are built, run an end-to-end sandbox test and verify:
- [ ] M-LEAD-INTAKE generates correct Audit Log entry
- [ ] M-SLACK-ALERTS generates correct Audit Log entry
- [ ] M-CONCIERGE-ASSIGNMENT generates correct Audit Log entry
- [ ] M-STRIPE-DEPOSIT generates correct Audit Log entry
- [ ] M-BOOKING-CREATION generates correct Audit Log entry
- [ ] M-BOOKING-CONFIRMATION generates correct Audit Log entry
- [ ] All entries appear in Airtable Audit Log with correct `Scenario_Name` values
- [ ] `Approval_State` values are correct per scenario (AUTONOMOUS vs. PENDING_HUMAN)
- [ ] `Environment` is `Sandbox` on all test entries

**Test 6 — Sandbox vs. Production separation:**
- [ ] Confirm that sandbox test entries (Environment = Sandbox) are visually distinguishable in the Airtable Audit Log view from Production entries
- [ ] Configure an Airtable view filter: `{Environment} = "Sandbox"` — confirm only test entries appear
- [ ] Confirm this filter view is accessible to Luciana and Will

---

## 12. Final Scenario Status

**Build Status:** `PENDING BUILD`

> M-AUDIT-LOGGER is the FIRST scenario that must be built in Stage 1. No other scenario can go to sandbox until M-AUDIT-LOGGER is operational and has passed all tests in Section 11.

**Build order dependency:**
- M-AUDIT-LOGGER → ALL other Stage 1 scenarios depend on this
- Specifically: must be operational before M-LEAD-INTAKE sandbox testing begins

**Critical pre-build action items:**

| Action Item | Owner | Priority | Blocker? |
|-------------|-------|----------|---------|
| Confirm all Audit Log table fields exist in `tblrMpTfMk8q1eNHp` (see Section 7 field list) | Systems Arch | CRITICAL | YES |
| Confirm Single Select choices are configured in Airtable for `Approval_State`, `Brand`, `City`, `Environment` | Systems Arch | CRITICAL | YES |
| Authenticate Airtable connection in Make.com workspace | Will / Systems Arch | CRITICAL | YES |
| Register M-AUDIT-LOGGER webhook in Make.com and distribute URL to all scenario builders | Systems Arch | CRITICAL | YES |
| Confirm `Payload_Hash` field exists as single line text in Audit Log table | Systems Arch | HIGH | YES |
| Confirm `Make_Run_ID` field exists as single line text in Audit Log table | Systems Arch | HIGH | NO |
| Confirm Slack connection in Make.com workspace for SEV-1 alert | Will / Systems Arch | CRITICAL | YES |

**Make.com Scenario Registration Checklist:**
- [ ] Scenario created in Make.com workspace
- [ ] Scenario ID recorded in this document
- [ ] Webhook URL registered and distributed to all calling scenario builders
- [ ] Airtable connection authenticated with correct base and table permissions
- [ ] Slack connection authenticated with #sss-ops-alerts posting permission
- [ ] Validation logic (Module 2) confirmed to catch all required field failures
- [ ] Idempotency (hash deduplication) confirmed working via Test 3
- [ ] SEV-1 failure handler (Module 5) confirmed working via Test 4
- [ ] Scenario set to Active
- [ ] Scenario execution log retention set to 90 days minimum (longer than other scenarios — this is the audit trail)
- [ ] Scenario marked as "CRITICAL — DO NOT MODIFY WITHOUT ARCHITECT REVIEW" in Make.com scenario notes

---

*Document maintained by Systems Architecture. M-AUDIT-LOGGER is the foundational reliability component of the Stage 1 automation system. Any modification to this scenario requires review by the Systems Architect and must be tested in Sandbox before Production deployment.*  
*All field names and table IDs are authoritative as of 2026-05-16. Verify against live Airtable base before build.*
