# M-CONCIERGE-ASSIGNMENT — Make.com Scenario Build Specification

**Document Version:** 1.0
**Status:** PENDING BUILD
**Last Updated:** 2026-05-16
**Author:** Systems Architecture
**Pipeline Stage:** Stage 1 — Lead Intake
**Execution Order:** Third scenario in Stage 1 pipeline (after M-LEAD-INTAKE, before M-STRIPE-DEPOSIT)

---

## 1. Scenario Name

`M-CONCIERGE-ASSIGNMENT`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references in M-LEAD-INTAKE (caller) and M-STRIPE-DEPOSIT (downstream). This ID is required for the Audit Log `Triggered_By_Scenario` field.

---

## 3. Trigger Type

**Primary Trigger:** HTTP webhook called by M-LEAD-INTAKE immediately after a Request record is created in Airtable. M-LEAD-INTAKE passes the Airtable Request Record ID in the webhook payload.

**Secondary Trigger (Fallback Watch):** Airtable Watch Records module on the Requests table (tblTlSB9CO4dTGodg), filtered to fire when `Agent_Status` changes to `"NEW"`. This catches any Request records created manually or by systems other than M-LEAD-INTAKE.

> **Trigger Priority:** The HTTP webhook is the preferred path for automated flow. The Airtable Watch trigger is a safety net only. Both paths feed the same module sequence beginning at Module 2 (Get Request Record). Set the Airtable Watch trigger to poll every 5 minutes in Stage 1.

**Webhook Configuration:**

| Parameter           | Value                                              |
|---------------------|----------------------------------------------------|
| Webhook Name        | `make-concierge-assignment-trigger`                |
| Method              | POST                                               |
| Content-Type        | `application/json`                                 |
| Authentication      | Custom header `X-Make-Secret: {{env.MAKE_WEBHOOK_SECRET}}` |
| Max Payload Size    | 1 MB                                               |

**Inbound Payload from M-LEAD-INTAKE:**

```json
{
  "request_id": "recXXXXXXXXXXXXXX",
  "brand": "SSS",
  "city": "Barcelona",
  "client_name": "Jane Hoffman",
  "package_interest": "Mediterranean Sunset Charter",
  "submitted_at": "2026-05-16T14:32:00.000Z",
  "source_scenario": "M-LEAD-INTAKE",
  "environment": "sandbox"
}
```

**Required Fields (all must be present; missing fields trigger error handler at Module 1):**
- `request_id` — Airtable Record ID of the Request
- `brand` — `SSS` or `ME`
- `city` — string, must match a value in Concierge_Operators.Cities
- `client_name` — for Slack notification and Audit Log

---

## 4. Exact Module Sequence

### Module 1 — [Webhook] Receive Trigger from M-LEAD-INTAKE

**Make Module Type:** Webhooks > Custom Webhook (or Airtable > Watch Records for fallback)
**Position:** Module 1

**Validation at this step:**
- Verify `request_id` is present and begins with `rec` (length ≥ 17 characters)
- Verify `brand` is exactly `"SSS"` or `"ME"` (case-sensitive)
- Verify `city` is non-empty string
- If validation fails: route to Error Handler (see Section 10), do NOT proceed to Module 2

**Output Variables Set:**
```
{{1.request_id}}
{{1.brand}}
{{1.city}}
{{1.client_name}}
{{1.package_interest}}
{{1.submitted_at}}
{{1.environment}}
```

---

### Module 2 — [Airtable] Get Request Record

**Make Module Type:** Airtable > Get a Record
**Position:** Module 2

**Configuration:**

| Parameter    | Value                                    |
|--------------|------------------------------------------|
| Connection   | `airtable-sss-main-connection`           |
| Base ID      | `appdZ49WqgjRXxA1R`                      |
| Table ID     | `tblTlSB9CO4dTGodg` (Requests)           |
| Record ID    | `{{1.request_id}}`                       |

**Fields to retrieve (do not retrieve all fields — select only required):**

| Airtable Field Name    | Purpose                                         |
|------------------------|-------------------------------------------------|
| `Request_ID`           | Human-readable ID for Audit Log                 |
| `Brand`                | Confirm brand (double-check against webhook)    |
| `City`                 | Confirm city (double-check against webhook)     |
| `Client_Name`          | For Slack notification                          |
| `Package_Interest`     | For Slack notification                          |
| `Agent_Status`         | Guard: must be `"NEW"` to proceed               |
| `Concierge_Assigned`   | Guard: must be empty to prevent double-assign   |
| `Submitted_At`         | For Audit Log                                   |

**Guard Conditions (implemented as a subsequent Filter module before Module 3):**

```
Condition 1: {{2.Agent_Status}} = "NEW"
Condition 2: {{2.Concierge_Assigned}} IS EMPTY
```

If either guard fails: route to Duplicate Prevention handler (see Section 12). Log to Audit Log with `Event_Type = "ASSIGNMENT_SKIPPED"` and reason. Do NOT throw an error — this is a legitimate skip condition.

**Error Handler on Module 2:**
- If record not found (Airtable returns 404): post Slack alert `"[CRITICAL] M-CONCIERGE-ASSIGNMENT: Request record {{1.request_id}} not found in Airtable. Manual investigation required."` and halt scenario.

---

### Module 3 — [Filter] Guard: Status=NEW and Unassigned

**Make Module Type:** Filter (built-in)
**Position:** Module 3 (between Module 2 and Module 4)

**Filter Conditions:**

```
{{2.Agent_Status}} Equal to (text) "NEW"
AND
{{2.Concierge_Assigned}} Does not exist (empty)
```

**If filter does not pass:** scenario halts at this point. No error is thrown. The Audit Log write in Module 11 still fires via an alternate route (see Error Handling Section 10).

---

### Module 4 — [Airtable] Search Concierge_Operators — Brand + City Match

**Make Module Type:** Airtable > Search Records
**Position:** Module 4

**Configuration:**

| Parameter       | Value                                                          |
|-----------------|----------------------------------------------------------------|
| Connection      | `airtable-sss-main-connection`                                 |
| Base ID         | `appdZ49WqgjRXxA1R`                                           |
| Table Name      | `Concierge_Operators` (migrated from app2FbmVD44BXShyx)        |
| Filter Formula  | See below                                                      |
| Sort Field      | `Current_Load` — Ascending                                     |
| Max Records     | 10                                                             |

**Airtable Filter Formula (exact):**

```
AND(
  {Active} = TRUE(),
  {Brand} = "{{2.Brand}}",
  FIND("{{2.City}}", {Cities}) > 0
)
```

> **Implementation Note:** The `Cities` field in Concierge_Operators is expected to be a multi-select or comma-delimited text field. `FIND()` performs a substring match. If Cities is a multi-select, the formula `FIND("{{2.City}}", ARRAYJOIN({Cities}, ",")) > 0` should be used instead. Confirm field type before build.

**Fields to retrieve:**

| Field Name          | Purpose                                      |
|---------------------|----------------------------------------------|
| `Concierge_ID`      | Record ID for downstream update              |
| `Name`              | Human-readable name for assignment           |
| `Brand`             | Confirm brand match                          |
| `Cities`            | Confirm city coverage                        |
| `Current_Load`      | Used for sort; lowest = first candidate      |
| `Active`            | Confirm active status                        |
| `Email`             | Future use (Stage 2 notification)            |

**Output:** Array of matching concierge records, sorted by Current_Load ascending. The first element `{{4[]}}` is the selected candidate.

---

### Module 5 — [Router] Concierge Found or Not Found

**Make Module Type:** Router (built-in)
**Position:** Module 5

**Route A — Concierge Found:**
```
Condition: {{4[].length}} Greater than 0
(or: {{4[1].Concierge_ID}} Exists)
```
Proceeds to Module 6 (Update Request — Assign).

**Route B — No Concierge Available:**
```
Condition: {{4[].length}} Equal to 0
(or: {{4[1].Concierge_ID}} Does not exist)
```
Proceeds to Module 6B (Escalation — Flag for Luciana).

---

### Module 6A — [Airtable] Update Request Record: Assign Concierge

**Make Module Type:** Airtable > Update a Record
**Position:** Module 6A (Route A only)

**Configuration:**

| Parameter    | Value                                    |
|--------------|------------------------------------------|
| Connection   | `airtable-sss-main-connection`           |
| Base ID      | `appdZ49WqgjRXxA1R`                      |
| Table ID     | `tblTlSB9CO4dTGodg` (Requests)           |
| Record ID    | `{{1.request_id}}`                       |

**Field Writes (exact field names as they appear in Airtable):**

| Airtable Field Name      | Value Written                                      | Format          |
|--------------------------|----------------------------------------------------|-----------------|
| `Agent_Status`           | `AI_RESPONDING`                                    | Single select   |
| `Concierge_Assigned`     | `{{4[1].Name}}`                                    | Text            |
| `Assignment_Timestamp`   | `{{now}}`                                          | ISO 8601        |
| `Assigned_Concierge_ID`  | `{{4[1].Concierge_ID}}`                            | Text (record ID)|
| `Assignment_Method`      | `AUTOMATED`                                        | Single select   |

**Error Handler on Module 6A:**
- On Airtable write failure: capture error, post Slack alert with full context, write Audit Log entry with `Event_Type = "ASSIGNMENT_WRITE_FAILED"`, increment retry counter (see Section 11).
- Do NOT proceed to Module 7 if this write fails — downstream modules depend on this record state.

---

### Module 6B — [Airtable] Update Request Record: Flag for Manual Assignment

**Make Module Type:** Airtable > Update a Record
**Position:** Module 6B (Route B only — no concierge found)

**Configuration:**

| Parameter    | Value                                    |
|--------------|------------------------------------------|
| Connection   | `airtable-sss-main-connection`           |
| Base ID      | `appdZ49WqgjRXxA1R`                      |
| Table ID     | `tblTlSB9CO4dTGodg` (Requests)           |
| Record ID    | `{{1.request_id}}`                       |

**Field Writes:**

| Airtable Field Name      | Value Written                                      | Format        |
|--------------------------|----------------------------------------------------|---------------|
| `Agent_Status`           | `NEEDS_MANUAL_ASSIGNMENT`                          | Single select |
| `Assignment_Method`      | `MANUAL_REQUIRED`                                  | Single select |
| `Assignment_Timestamp`   | `{{now}}`                                          | ISO 8601      |
| `Assignment_Failure_Reason` | `No active concierge found for Brand={{2.Brand}}, City={{2.City}}` | Text |

After Module 6B: proceeds to Module 8B (Escalation Slack Alert), skips Module 7 (load increment) and Module 8A (standard assignment Slack).

---

### Module 7 — [Airtable] Update Concierge_Operators: Increment Current_Load

**Make Module Type:** Airtable > Update a Record
**Position:** Module 7 (Route A only, after Module 6A succeeds)

**Configuration:**

| Parameter    | Value                                              |
|--------------|----------------------------------------------------|
| Connection   | `airtable-sss-main-connection`                     |
| Base ID      | `appdZ49WqgjRXxA1R`                               |
| Table ID     | `Concierge_Operators` table ID (confirm at build)  |
| Record ID    | `{{4[1].Concierge_ID}}`                            |

**Field Writes:**

| Airtable Field Name | Value Written                    | Format |
|---------------------|----------------------------------|--------|
| `Current_Load`      | `{{4[1].Current_Load + 1}}`      | Number |

> **Important:** This is a non-atomic increment operation (read-then-write). In high-concurrency scenarios, two simultaneous assignments for the same concierge could write the same incremented value. In Stage 1 (low volume), this is acceptable. Stage 2 should implement a dedicated load-tracking formula or use Airtable automations for atomic updates. Document this as a known limitation.

**Error Handler on Module 7:**
- On write failure: post Slack alert `"[WARNING] M-CONCIERGE-ASSIGNMENT: Failed to increment Current_Load for {{4[1].Name}}. Manual correction required in Concierge_Operators."` Assignment already written — do not roll back Module 6A. Continue to Module 8A.

---

### Module 8A — [Slack] Post Assignment Notification

**Make Module Type:** Slack > Create a Message
**Position:** Module 8A (Route A — successful assignment)

See Section 13 for full message format.

---

### Module 8B — [Slack] Post Escalation Alert (No Concierge)

**Make Module Type:** Slack > Create a Message
**Position:** Module 8B (Route B — no concierge found)

See Section 13 for full escalation message format.

---

### Module 9A — [Airtable] Write Audit Log Entry (Assignment Success)

**Make Module Type:** Airtable > Create a Record
**Position:** Module 9A (Route A, after Module 8A)

See Section 14 for exact field writes.

---

### Module 9B — [Airtable] Write Audit Log Entry (Escalation)

**Make Module Type:** Airtable > Create a Record
**Position:** Module 9B (Route B, after Module 8B)

See Section 14 for exact field writes.

---

### Module 10 — [HTTP] Trigger M-STRIPE-DEPOSIT (Route A only)

**Make Module Type:** HTTP > Make a Request
**Position:** Module 10 (Route A only, after Module 9A succeeds)

**Configuration:**

| Parameter      | Value                                              |
|----------------|----------------------------------------------------|
| Method         | POST                                               |
| URL            | `{{env.MAKE_STRIPE_DEPOSIT_WEBHOOK_URL}}`          |
| Content-Type   | `application/json`                                 |
| Auth Header    | `X-Make-Secret: {{env.MAKE_WEBHOOK_SECRET}}`       |

**Payload:**

```json
{
  "request_id": "{{1.request_id}}",
  "brand": "{{2.Brand}}",
  "city": "{{2.City}}",
  "client_name": "{{2.Client_Name}}",
  "package_interest": "{{2.Package_Interest}}",
  "concierge_assigned": "{{4[1].Name}}",
  "submitted_at": "{{2.Submitted_At}}",
  "source_scenario": "M-CONCIERGE-ASSIGNMENT",
  "environment": "{{1.environment}}"
}
```

> **Stage 1 Note:** Route B (no concierge) does NOT trigger M-STRIPE-DEPOSIT. Stripe deposit flow requires a valid concierge assignment. Luciana must trigger M-STRIPE-DEPOSIT manually after completing manual assignment.

---

## 5. Router Logic — Exact Filter Conditions

### Router at Module 5

**Route A — Concierge Found (takes priority):**

```
Filter: Total number of bundles output by Module 4 > 0
Implementation: Use Make's built-in "Number of bundles" output variable
Condition type: Numeric greater than
Value: 0
```

**Route B — No Concierge (fallback, always true if Route A fails):**

```
No additional filter — this route fires if Route A condition is not met.
Set Route B as the "Else" or "Fallback" route in Make Router configuration.
```

### Filter Formula Breakdown (Module 4 — Airtable Search)

The three-condition match must ALL be true:

| Condition         | Formula Component               | Explanation                                   |
|-------------------|---------------------------------|-----------------------------------------------|
| Active status     | `{Active} = TRUE()`             | Excludes inactive/offboarded concierges       |
| Brand match       | `{Brand} = "{{2.Brand}}"`       | Exact match: "SSS" or "ME"                    |
| City coverage     | `FIND("{{2.City}}", {Cities}) > 0` | Substring match allows multi-city concierges |

**Sort:** `Current_Load ASC` — ensures least-loaded concierge is first in result array.

**Tie-breaking:** When multiple concierges share the same Current_Load, Airtable returns in creation-order. This is acceptable for Stage 1. Stage 2 should add secondary sort by `Last_Assigned_At ASC` (oldest last-assignment gets priority) for fair distribution.

---

## 6. Airtable Field Mapping

### Requests Table (tblTlSB9CO4dTGodg) — Fields Written by This Scenario

| Field Name                | Data Type     | Written Value                                         | Route  |
|---------------------------|---------------|-------------------------------------------------------|--------|
| `Agent_Status`            | Single Select | `AI_RESPONDING`                                       | A      |
| `Agent_Status`            | Single Select | `NEEDS_MANUAL_ASSIGNMENT`                             | B      |
| `Concierge_Assigned`      | Text          | `{{4[1].Name}}` (e.g., `"Sofia Reyes"`)               | A      |
| `Assigned_Concierge_ID`   | Text          | `{{4[1].Concierge_ID}}` (Airtable record ID)          | A      |
| `Assignment_Timestamp`    | DateTime      | `{{now}}` in ISO 8601 UTC                             | A + B  |
| `Assignment_Method`       | Single Select | `AUTOMATED`                                           | A      |
| `Assignment_Method`       | Single Select | `MANUAL_REQUIRED`                                     | B      |
| `Assignment_Failure_Reason`| Long Text    | Reason string with Brand and City                     | B only |

### Concierge_Operators Table — Fields Written by This Scenario

| Field Name       | Data Type | Written Value                           | Route |
|------------------|-----------|-----------------------------------------|-------|
| `Current_Load`   | Number    | `{{4[1].Current_Load + 1}}`             | A     |

> **Read-only fields (not written, only read):** `Name`, `Brand`, `Cities`, `Active`, `Email`, `Concierge_ID`

### Single Select Values — Must Exist in Airtable Before Build

Verify the following single-select options exist in Airtable before scenario activation:

| Table    | Field                  | Required Options                                    |
|----------|------------------------|-----------------------------------------------------|
| Requests | `Agent_Status`         | `NEW`, `AI_RESPONDING`, `NEEDS_MANUAL_ASSIGNMENT`   |
| Requests | `Assignment_Method`    | `AUTOMATED`, `MANUAL_REQUIRED`                      |

---

## 7. Webhook Structure

**Inbound (from M-LEAD-INTAKE):** Documented in Section 3.

**Outbound (to M-STRIPE-DEPOSIT):** Documented in Module 10.

**No external webhooks are registered or consumed by this scenario.** All Airtable interactions are direct API calls via Make's Airtable module, not webhooks.

---

## 8. Stripe Metadata Structure

**N/A** — This scenario does not interact with Stripe. Stripe integration begins in M-STRIPE-DEPOSIT.

---

## 9. Email / SMS Template Variables

**N/A** — This scenario does not send emails or SMS. All external communication in Stage 1 is via Slack to the internal ops team. Client-facing communication is handled manually by Luciana.

---

## 10. Error Handling Logic

### Error Class 1 — Inbound Payload Validation Failure (Module 1)

**Trigger:** `request_id` missing, `brand` invalid, or `city` empty.

**Action:**
1. Set Make error handler type: "Resume" with custom path
2. Post to Slack `#sss-ops-alerts`:
   ```
   [INTAKE ERROR] M-CONCIERGE-ASSIGNMENT received malformed payload.
   Missing field: {{error.field}}
   Raw payload: {{1}}
   Time: {{now}}
   Action required: Check M-LEAD-INTAKE output mapping.
   ```
3. Write Audit Log entry with `Event_Type = "PAYLOAD_VALIDATION_FAILED"`
4. Halt scenario (do not proceed to Module 2)

---

### Error Class 2 — Request Record Not Found (Module 2)

**Trigger:** Airtable returns 404 or empty result for `{{1.request_id}}`.

**Action:**
1. Post Slack critical alert (see above in Module 2 spec)
2. Write Audit Log: `Event_Type = "RECORD_NOT_FOUND"`, `Request_ID = {{1.request_id}}`
3. Halt scenario

---

### Error Class 3 — No Concierge Available (Module 5, Route B)

**Trigger:** Module 4 search returns 0 results.

**This is not an error — it is a valid operational state.** The scenario follows Route B:
1. Update Request: `Agent_Status = "NEEDS_MANUAL_ASSIGNMENT"` (Module 6B)
2. Post escalation Slack alert (Module 8B)
3. Write Audit Log: `Event_Type = "CONCIERGE_NOT_FOUND"` (Module 9B)
4. Do NOT trigger M-STRIPE-DEPOSIT
5. Scenario completes successfully with `Status = ESCALATED`

**Luciana's required action:** Review `#sss-ops-alerts`, manually assign a concierge in Airtable, then manually trigger M-STRIPE-DEPOSIT.

---

### Error Class 4 — Airtable Write Failure on Request Record (Module 6A)

**Trigger:** Airtable API returns 4xx or 5xx on the Update Record call.

**Action:**
1. Capture error: `{{error.message}}`, `{{error.statusCode}}`
2. Post Slack alert:
   ```
   [WRITE FAILURE] M-CONCIERGE-ASSIGNMENT: Failed to update Request record.
   Request ID: {{1.request_id}}
   Concierge Selected: {{4[1].Name}}
   Error: {{error.message}} (HTTP {{error.statusCode}})
   Time: {{now}}
   Action: Manual assignment write required in Airtable.
   ```
3. Write Audit Log: `Event_Type = "AIRTABLE_WRITE_FAILED"`, `Module = "6A-UPDATE-REQUEST"`
4. DO NOT proceed to Module 7 (do not increment Current_Load — no assignment has been confirmed)
5. Halt scenario with `Status = FAILED`

---

### Error Class 5 — Airtable Write Failure on Current_Load Increment (Module 7)

**Trigger:** Airtable API returns error on Concierge_Operators update.

**Action:**
1. Post Slack warning (non-critical — assignment already saved)
2. Write Audit Log: `Event_Type = "LOAD_INCREMENT_FAILED"`, `Concierge = {{4[1].Name}}`
3. Continue scenario to Module 8A — do NOT halt. Assignment is valid; only load count is stale.
4. Flag for manual correction in Slack message.

---

### Error Class 6 — Slack Post Failure (Modules 8A or 8B)

**Trigger:** Slack API error (token expired, channel not found, rate limit).

**Action:**
1. Log error via Make's built-in error log
2. Write Audit Log: `Event_Type = "SLACK_POST_FAILED"`
3. Continue scenario — Slack failure is non-blocking. Core assignment data is already in Airtable.

---

### Error Class 7 — M-STRIPE-DEPOSIT Trigger Failure (Module 10)

**Trigger:** HTTP POST to M-STRIPE-DEPOSIT webhook returns non-2xx.

**Action:**
1. Post Slack alert:
   ```
   [HANDOFF FAILURE] M-CONCIERGE-ASSIGNMENT: Failed to trigger M-STRIPE-DEPOSIT.
   Request ID: {{1.request_id}}
   HTTP Status: {{10.statusCode}}
   Action: Manually trigger M-STRIPE-DEPOSIT for this request.
   ```
2. Write Audit Log: `Event_Type = "DOWNSTREAM_TRIGGER_FAILED"`, `Target = "M-STRIPE-DEPOSIT"`
3. Halt — M-STRIPE-DEPOSIT must be re-triggered manually

---

## 11. Retry Logic

**Global Make Scenario Setting:** Enable auto-retry for the scenario.

| Module   | Retry on Error | Max Retries | Retry Interval | Retry Condition                    |
|----------|---------------|-------------|----------------|------------------------------------|
| Module 2 | Yes           | 3           | 30 seconds     | HTTP 429 (rate limit) or 5xx       |
| Module 4 | Yes           | 3           | 30 seconds     | HTTP 429 or 5xx                    |
| Module 6A| Yes           | 3           | 60 seconds     | HTTP 429 or 5xx only (NOT 4xx)     |
| Module 7 | Yes           | 2           | 30 seconds     | HTTP 429 or 5xx only               |
| Module 8A| No            | 0           | N/A            | Slack failures are non-blocking    |
| Module 10| Yes           | 2           | 120 seconds    | Non-2xx response from downstream   |

**After max retries exhausted:** Fire the error handler for that module class (see Section 10) and halt with `FAILED` status.

**Incomplete Run Storage:** Enable Make's "Store Incomplete Executions" setting. Set retention to 7 days. Will and Luciana can re-run failed executions from the Make execution history panel.

---

## 12. Duplicate Prevention

### Prevention Layer 1 — Guard Filter at Module 3

The filter at Module 3 checks:
- `Agent_Status = "NEW"` — if already `"AI_RESPONDING"`, scenario halts before making any changes.
- `Concierge_Assigned` is empty — if already populated, assignment has already occurred.

This is the primary guard against double-assignment.

### Prevention Layer 2 — Airtable Field State Check (Module 2)

The full record is read in Module 2, providing current field state at time of execution. This is the read-before-write pattern. If the record has moved out of `NEW` state between when M-LEAD-INTAKE fired the trigger and when Module 2 executes, the guard at Module 3 will catch it.

### Prevention Layer 3 — Single Select Lock

`Agent_Status` is a single-select field. Airtable enforces only one value. If two simultaneous runs attempt to write `"AI_RESPONDING"` at the same time, both writes succeed (last-write wins), but only one concierge name is recorded in `Concierge_Assigned`. This is a known race condition acceptable in Stage 1 due to low volume (typically 1-5 requests/day). Document for Stage 2 remediation.

### Known Limitation — Not Atomic

Airtable does not support atomic test-and-set operations. The read (Module 2) and write (Module 6A) are not atomic. In Stage 1 this is acceptable. Stage 2 mitigation: add a `Processing_Lock` checkbox field to Requests that is set to `true` in Module 6A and checked as part of the Module 3 filter.

---

## 13. Slack Alert Structure

### Channel: `#sss-ops-alerts`

### Alert Type A — Successful Assignment

**Format (Slack Block Kit text):**

```
✅ *CONCIERGE ASSIGNED* | {{2.Brand}} — {{2.City}}

*Client:* {{2.Client_Name}}
*Package Interest:* {{2.Package_Interest}}
*Assigned To:* {{4[1].Name}}
*Concierge Load (after assignment):* {{4[1].Current_Load + 1}} active requests
*Request ID:* {{2.Request_ID}}
*Airtable Record:* {{1.request_id}}
*Assignment Method:* AUTOMATED
*Timestamp:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

_Next step: M-STRIPE-DEPOSIT is being triggered automatically._
```

### Alert Type B — Escalation (No Concierge Found)

**Format:**

```
🚨 *MANUAL ASSIGNMENT REQUIRED* | {{2.Brand}} — {{2.City}}

No active concierge found matching Brand={{2.Brand}}, City={{2.City}}.

*Client:* {{2.Client_Name}}
*Package Interest:* {{2.Package_Interest}}
*Request ID:* {{2.Request_ID}}
*Airtable Record:* {{1.request_id}}
*Timestamp:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

*Action required (Luciana):*
1. Open Airtable → Requests → Record {{1.request_id}}
2. Manually assign a concierge in the `Concierge_Assigned` field
3. Update `Agent_Status` to `AI_RESPONDING`
4. Manually trigger M-STRIPE-DEPOSIT for this request
5. Update `Assignment_Method` to `MANUAL_REQUIRED`
```

### Alert Type C — Assignment Write Failure (Error)

**Format:**

```
🔴 *SYSTEM ERROR* | M-CONCIERGE-ASSIGNMENT Write Failure

Failed to write assignment to Airtable.

*Request ID:* {{1.request_id}}
*Intended Concierge:* {{4[1].Name}}
*Error:* {{error.message}} (HTTP {{error.statusCode}})
*Timestamp:* {{formatDate(now, "MMMM D, YYYY [at] h:mm A [UTC]")}}

*Action required (Will/Luciana):*
1. Check Airtable record {{1.request_id}} — update manually if unassigned
2. Check Make execution log for full error trace
3. Re-run scenario from Make Incomplete Executions if needed
```

> All Slack messages must use the `#sss-ops-alerts` channel. Channel ID should be stored as `{{env.SLACK_OPS_CHANNEL_ID}}` to avoid hardcoding.

---

## 14. Audit Log Writes

**Table:** Audit Log (tblrMpTfMk8q1eNHp)
**Module:** 9A (success) or 9B (escalation)
**Make Module Type:** Airtable > Create a Record

### Route A — Successful Assignment

| Audit Log Field          | Value Written                                              |
|--------------------------|------------------------------------------------------------|
| `Event_Type`             | `CONCIERGE_ASSIGNED`                                       |
| `Event_Timestamp`        | `{{now}}` (ISO 8601 UTC)                                   |
| `Request_ID`             | `{{2.Request_ID}}` (human-readable ID from record)         |
| `Airtable_Record_ID`     | `{{1.request_id}}` (recXXXXXX)                             |
| `Brand`                  | `{{2.Brand}}`                                              |
| `City`                   | `{{2.City}}`                                               |
| `Client_Name`            | `{{2.Client_Name}}`                                        |
| `Concierge_Assigned`     | `{{4[1].Name}}`                                            |
| `Concierge_Load_After`   | `{{4[1].Current_Load + 1}}`                                |
| `Assignment_Method`      | `AUTOMATED`                                                |
| `Triggered_By_Scenario`  | `M-CONCIERGE-ASSIGNMENT`                                   |
| `Scenario_ID`            | `PENDING-REGISTRATION` (update after Make registration)    |
| `Execution_ID`           | `{{scenarioExecutionId}}` (Make built-in variable)         |
| `Status`                 | `SUCCESS`                                                  |
| `Notes`                  | `Concierge selected from pool of {{4[].length}} candidates`|

### Route B — Escalation (No Concierge)

| Audit Log Field          | Value Written                                              |
|--------------------------|------------------------------------------------------------|
| `Event_Type`             | `CONCIERGE_NOT_FOUND`                                      |
| `Event_Timestamp`        | `{{now}}`                                                  |
| `Request_ID`             | `{{2.Request_ID}}`                                         |
| `Airtable_Record_ID`     | `{{1.request_id}}`                                         |
| `Brand`                  | `{{2.Brand}}`                                              |
| `City`                   | `{{2.City}}`                                               |
| `Client_Name`            | `{{2.Client_Name}}`                                        |
| `Concierge_Assigned`     | *(empty)*                                                  |
| `Assignment_Method`      | `MANUAL_REQUIRED`                                          |
| `Triggered_By_Scenario`  | `M-CONCIERGE-ASSIGNMENT`                                   |
| `Execution_ID`           | `{{scenarioExecutionId}}`                                  |
| `Status`                 | `ESCALATED`                                                |
| `Notes`                  | `No active concierge for Brand={{2.Brand}}, City={{2.City}}. Flagged for Luciana.` |

---

## 15. Automation Health Writes

> In Stage 1, automation health metrics are written to the Audit Log table using a reserved `Event_Type = "HEALTH_PING"`. A dedicated health dashboard is a Stage 2 deliverable.

**Health data captured per execution (appended to Audit Log entry):**

| Metric Field                | Value                                          |
|-----------------------------|------------------------------------------------|
| `Execution_Duration_ms`     | Calculated from `submitted_at` to `{{now}}`   |
| `Modules_Executed`          | Count of modules that ran (approximate)        |
| `Route_Taken`               | `A` (assigned) or `B` (escalated)             |
| `Concierge_Pool_Size`       | `{{4[].length}}` (how many candidates found)  |
| `Scenario_Version`          | `1.0`                                          |
| `Environment`               | `{{1.environment}}` (sandbox / production)     |

---

## 16. Rollback Procedure

**Use case:** A concierge was auto-assigned incorrectly (wrong brand, wrong city, or concierge is unavailable).

**Step-by-step rollback:**

1. **In Airtable — Requests table (tblTlSB9CO4dTGodg):**
   - Open the relevant Request record
   - Set `Agent_Status` → `NEW`
   - Clear `Concierge_Assigned` field (delete value)
   - Clear `Assigned_Concierge_ID` field
   - Set `Assignment_Method` → *(clear or reset)*
   - Clear `Assignment_Timestamp`
   - Clear `Assignment_Failure_Reason` (if set)

2. **In Airtable — Concierge_Operators table:**
   - Open the record for the incorrectly assigned concierge
   - Decrement `Current_Load` by 1 (set to `Current_Load - 1`, minimum 0)

3. **Write a manual Audit Log entry:**
   - `Event_Type = "ASSIGNMENT_ROLLED_BACK"`
   - `Notes` = reason for rollback, who performed it, timestamp

4. **Re-trigger M-CONCIERGE-ASSIGNMENT:**
   - In Make, navigate to M-CONCIERGE-ASSIGNMENT
   - Use "Run Once" with manual payload containing the `request_id`
   - Or update `Agent_Status` to `NEW` in Airtable and allow the Watch trigger to fire

> **Warning:** Do NOT re-run the scenario without first completing step 1. If `Agent_Status` is not reset to `NEW`, the guard filter at Module 3 will prevent re-assignment.

---

## 17. Sandbox Test Procedure

**Pre-conditions:**
- Airtable base `appdZ49WqgjRXxA1R` has at least one Concierge_Operators record with `Active=true`, `Brand="SSS"`, `Cities` containing `"Barcelona"`, `Current_Load=0`
- Requests table has a test record with `Agent_Status="NEW"`, `Brand="SSS"`, `City="Barcelona"`, `Concierge_Assigned` empty
- Make scenario is active with webhook URL confirmed
- Slack `#sss-ops-alerts` channel is accessible
- `environment` field = `"sandbox"` in all test payloads

**Test Case 1 — Happy Path (Concierge Found):**

```bash
curl -X POST {{MAKE_CONCIERGE_ASSIGNMENT_WEBHOOK_URL}} \
  -H "Content-Type: application/json" \
  -H "X-Make-Secret: {{MAKE_WEBHOOK_SECRET}}" \
  -d '{
    "request_id": "recTEST0000000001",
    "brand": "SSS",
    "city": "Barcelona",
    "client_name": "Test Client A",
    "package_interest": "Mediterranean Sunset Charter",
    "submitted_at": "2026-05-16T10:00:00.000Z",
    "source_scenario": "M-LEAD-INTAKE",
    "environment": "sandbox"
  }'
```

**Expected outcomes:**
- [ ] Module 2: Request record retrieved successfully
- [ ] Module 3: Guard passes (Agent_Status=NEW, no existing assignment)
- [ ] Module 4: At least 1 concierge returned, sorted by Current_Load
- [ ] Module 5: Route A fires
- [ ] Module 6A: Request record shows `Agent_Status="AI_RESPONDING"`, `Concierge_Assigned` populated
- [ ] Module 7: Assigned concierge's `Current_Load` incremented by 1
- [ ] Module 8A: Slack message appears in `#sss-ops-alerts` with correct format
- [ ] Module 9A: Audit Log record created with `Event_Type="CONCIERGE_ASSIGNED"`, `Status="SUCCESS"`
- [ ] Module 10: HTTP 200 response from M-STRIPE-DEPOSIT webhook (or stub endpoint)

**Test Case 2 — No Concierge Available:**

Use a brand/city combination with no matching active concierge (e.g., `brand="ME"`, `city="Santorini"` if no ME concierge covers Santorini).

**Expected outcomes:**
- [ ] Module 4: Returns 0 results
- [ ] Module 5: Route B fires
- [ ] Module 6B: Request shows `Agent_Status="NEEDS_MANUAL_ASSIGNMENT"`
- [ ] Module 8B: Escalation Slack alert posted with action instructions for Luciana
- [ ] Module 9B: Audit Log shows `Event_Type="CONCIERGE_NOT_FOUND"`, `Status="ESCALATED"`
- [ ] Module 10: NOT triggered (correct)

**Test Case 3 — Duplicate Prevention:**

Re-send Test Case 1 payload after it has already processed.

**Expected outcomes:**
- [ ] Module 2: Record retrieved — `Agent_Status="AI_RESPONDING"` (already processed)
- [ ] Module 3: Guard filter fails — scenario halts cleanly
- [ ] No additional writes to Airtable
- [ ] No duplicate Slack alerts
- [ ] No Audit Log entry created (or entry with `Event_Type="ASSIGNMENT_SKIPPED"`)

**Test Case 4 — Malformed Payload:**

Send payload with missing `request_id`.

**Expected outcomes:**
- [ ] Module 1: Validation fails
- [ ] Slack alert posted with `[INTAKE ERROR]` prefix
- [ ] Scenario halts — no Airtable reads or writes

---

## 18. Production Validation Checklist

Complete ALL items before switching `environment` from `sandbox` to `production`:

**Airtable:**
- [ ] Confirm `Concierge_Operators` table is fully migrated from `app2FbmVD44BXShyx` to `appdZ49WqgjRXxA1R`
- [ ] Confirm all Concierge_Operators records have `Active`, `Brand`, `Cities`, `Current_Load` fields populated
- [ ] Confirm `Cities` field type (multi-select vs. text) and update FIND() formula accordingly
- [ ] Confirm all `Agent_Status` single-select options exist: `NEW`, `AI_RESPONDING`, `NEEDS_MANUAL_ASSIGNMENT`
- [ ] Confirm `Assignment_Method` single-select options exist: `AUTOMATED`, `MANUAL_REQUIRED`
- [ ] Confirm `Assigned_Concierge_ID` field exists in Requests table
- [ ] Confirm Audit Log table has all required fields (see Section 14)

**Make:**
- [ ] Webhook URL is registered and tested
- [ ] `env.MAKE_WEBHOOK_SECRET` is set in Make environment variables
- [ ] `env.SLACK_OPS_CHANNEL_ID` is set in Make environment variables
- [ ] `env.MAKE_STRIPE_DEPOSIT_WEBHOOK_URL` is set in Make environment variables
- [ ] Airtable connection `airtable-sss-main-connection` is authorized with correct scopes
- [ ] Slack connection is authorized with `chat:write` scope for `#sss-ops-alerts`
- [ ] Error handlers are configured on all Airtable write modules
- [ ] "Store Incomplete Executions" is enabled
- [ ] Retry settings match Section 11 specifications

**Integration:**
- [ ] M-LEAD-INTAKE successfully triggers this scenario with correct payload in sandbox
- [ ] This scenario successfully triggers M-STRIPE-DEPOSIT with correct payload in sandbox
- [ ] All three sandbox test cases pass (Section 17)
- [ ] Luciana has reviewed Slack alert formats and approved
- [ ] Will has reviewed escalation procedure (Section 10, Error Class 3)

---

## 19. Open Issues

### Issue 1 — Concierge_Operators Table Empty at Build Time

**Risk:** If the Concierge_Operators table has zero records at launch, every new Request will follow Route B (escalation). All requests will land on Luciana for manual assignment. This is operationally functional but creates manual overhead.

**Resolution required before production:** Confirm with Luciana that at minimum 1 active SSS concierge and 1 active ME concierge are entered into the table before the first live request.

**Interim fallback:** If table is empty at build time, use the Route B (NEEDS_MANUAL_ASSIGNMENT) flow as the primary path during onboarding.

---

### Issue 2 — Cities Field Type Ambiguity

**Risk:** If `Cities` is a multi-select field in Airtable, the FIND() formula in Module 4 must use `ARRAYJOIN()`. If it is a plain text field, FIND() works directly. The wrong formula will cause Module 4 to return 0 results for all queries.

**Resolution:** Confirm field type in Airtable schema before writing the filter formula. Update Section 5 formula accordingly.

---

### Issue 3 — Non-Atomic Current_Load Increment

**Risk:** High-concurrency scenarios (>1 simultaneous request for same concierge) can result in stale Current_Load values. Documented in Module 7 spec.

**Stage 1 Acceptance:** Acceptable given expected volume of 1-5 requests/day.

**Stage 2 Remediation:** Implement a `Processing_Lock` field or use Airtable Automations for atomic increments.

---

### Issue 4 — Manual M-STRIPE-DEPOSIT Re-trigger on Route B

**Risk:** After Luciana completes a manual assignment (Route B), there is currently no automated way to trigger M-STRIPE-DEPOSIT. Luciana must trigger it manually in Make.

**Resolution:** In Stage 2, add an Airtable Watch trigger to M-STRIPE-DEPOSIT that fires when `Agent_Status` changes from `NEEDS_MANUAL_ASSIGNMENT` to `AI_RESPONDING`.

---

### Issue 5 — Concierge_Operators Migration Verification

**Status:** Concierge_Operators table was migrated from `app2FbmVD44BXShyx` to `appdZ49WqgjRXxA1R`. Migration must be verified as complete with all records intact and field types preserved before this scenario goes live.

**Owner:** Will / Luciana

---

## 20. Final Scenario Status

| Field                  | Value                                              |
|------------------------|----------------------------------------------------|
| **Status**             | `PENDING BUILD`                                    |
| **Scenario ID**        | `PENDING-REGISTRATION`                             |
| **Make Workspace**     | She Said Sail + Mare Executive                     |
| **Target Build Date**  | TBD                                                |
| **Builder**            | TBD                                                |
| **Reviewer**           | Luciana (Ops Lead)                                 |
| **Approver**           | Will (Founder)                                     |
| **Dependencies**       | M-LEAD-INTAKE must be built and tested first       |
| **Blocks**             | M-STRIPE-DEPOSIT cannot be tested until this passes|
| **Environment**        | SANDBOX (Stage 1)                                  |
| **Estimated Modules**  | 10-12 modules                                      |
| **Estimated Build Time** | 3-4 hours                                        |

---

*Document prepared by Systems Architecture — She Said Sail + Mare Executive Stage 1 Implementation*
*Do not activate this scenario in production until all items in Section 18 are checked.*
