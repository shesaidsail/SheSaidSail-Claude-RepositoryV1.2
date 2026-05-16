# STAGE 1 AIRTABLE FIELD PATCH REPORT
**Project:** She Said Sail + Mare Executive — Make.com Automation System  
**Base:** appdZ49WqgjRXxA1R  
**Prepared by:** Production Reliability Engineering  
**Date:** 2026-05-16  
**Purpose:** Complete inventory of every Airtable field addition required before Stage 1 scenarios can operate  
**Status:** OPEN — fields must be added and verified before any Make scenario is activated

---

## Overview

This report documents every field that must be added to Airtable before Stage 1 Make.com scenarios are built and activated. Fields are grouped by table. Each field entry includes its exact name, type, configuration, and the downstream consequence of omitting it.

**Total fields to add:** 27  
**Tables affected:** 5 (Bookings, Requests, Clients, Audit_Log, Automation_Health)  
**New tables to create:** 1 (Automation_Health)

---

## Add Order: Dependency Sequence

Some fields depend on other fields existing first (e.g., formula fields that reference other fields). Follow this sequence:

```
Phase 1 — Foundation (no dependencies):
  [1]  Automation_Health table — create entire table (BLK-003)
  [2]  Requests.Environment
  [3]  Clients.Environment
  [4]  Bookings.Environment
  [5]  Audit_Log.Environment

Phase 2 — Operational fields (depend on Phase 1):
  [6]  Bookings.Idempotency_Key
  [7]  Bookings.Make_Processing
  [8]  Bookings.Needs_Make_Processing
  [9]  Bookings.Last_Make_Run
  [10] Requests.Assigned_Concierge (if missing)
  [11] Requests.Assignment_Status (if missing)

Phase 3 — Formula fields (depend on Phase 2 fields existing):
  [12] Bookings.D7_Review_Eligible  (depends on Charter_Date and Review_Sent)
  [13] Audit_Log.Event_ID           (depends on Audit_Log existing with its fields)

Phase 4 — Audit and logging fields:
  [14–27] All remaining Audit_Log fields
```

---

## TABLE: Automation_Health (NEW TABLE)

This table must be created from scratch. It contains the global control record for Make.com kill switch functionality.

| # | Field Name | Field Type | Values / Formula | Default | Required By | Blocker | Verification |
|---|-----------|-----------|-----------------|---------|-------------|---------|--------------|
| 1 | Record_Type | Single Line Text | Free text | `global_control` | ALL scenarios | BLK-003 | Value = "global_control" in sole record |
| 2 | Automations_Paused | Checkbox | true / false | false (unchecked) | ALL scenarios | BLK-003 | Toggle to true; confirm Make stops |
| 3 | Maintenance_Mode | Checkbox | true / false | false | ALL scenarios | BLK-003 | Field visible in table |
| 4 | Paused_By | Single Line Text | Free text | (empty) | Ops monitoring | BLK-003 | Accepts text input |
| 5 | Paused_At | Date and Time | ISO 8601 | (empty) | Ops monitoring | BLK-003 | Accepts datetime |
| 6 | Pause_Reason | Long Text | Free text | (empty) | Ops monitoring | BLK-003 | Accepts multi-line text |
| 7 | Emergency_Contact | Single Line Text | Slack handle | `@luciana` | Ops monitoring | BLK-003 | Field visible |
| 8 | Environment | Single Select | production, sandbox, test | sandbox | BLK-001 | BLK-001 | Default = sandbox |

**Post-creation action:** Create exactly ONE record with `Record_Type = global_control`, `Automations_Paused = false`, `Environment = sandbox`.

**Risk if missing:** No kill switch. Runaway scenarios cannot be stopped from Airtable. BLK-003 remains open.

---

## TABLE: Requests

The Requests table captures inbound leads. Make.com M-LEAD-INTAKE and M-BRAND-ROUTER read from and write to this table.

| # | Field Name | Field Type | Values / Formula | Default | Required By | Blocker | Add Order | Verification |
|---|-----------|-----------|-----------------|---------|-------------|---------|-----------|--------------|
| 9 | Environment | Single Select | production, sandbox, test | sandbox | M-LEAD-INTAKE, M-BRAND-ROUTER, ALL | BLK-001 | Phase 1 | Filter view to Environment=sandbox; confirm test records appear |
| 10 | Assigned_Concierge | Single Line Text | Concierge name | (empty) | M-CONCIERGE-ASSIGNMENT | — | Phase 2 | Write test name; confirm field saves |
| 11 | Assignment_Status | Single Select | unassigned, assigned, in_progress, closed | unassigned | M-CONCIERGE-ASSIGNMENT | — | Phase 2 | Confirm all 4 options selectable |
| 12 | Make_Last_Processed | Date and Time | ISO 8601 | (empty) | M-BRAND-ROUTER (audit trail) | — | Phase 2 | Field accepts datetime write from Make |
| 13 | Routing_Decision | Single Select | she_said_sail, mare_executive, ambiguous | (empty) | M-BRAND-ROUTER | — | Phase 2 | Confirm 3 options selectable |
| 14 | Routing_Confidence | Number | 0.00–1.00 (decimal) | (empty) | M-BRAND-ROUTER | — | Phase 2 | Accepts decimal number |

### Risk Table — Requests

| Field | Risk if Missing |
|-------|----------------|
| Environment | Test records contaminate production data. No sandbox isolation. BLK-001 blocks ALL scenarios. |
| Assigned_Concierge | M-CONCIERGE-ASSIGNMENT cannot write assignment. Field write fails silently or errors. |
| Assignment_Status | Cannot track assignment workflow state. Ops team has no visibility into unassigned queue. |
| Make_Last_Processed | No audit trail of when Make last touched a Requests record. |
| Routing_Decision | Brand routing decision is not persisted. If Make reruns, no way to detect prior routing. |
| Routing_Confidence | Cannot distinguish high-confidence from ambiguous routing decisions for review queue. |

### Verification Procedure — Requests Table

```
1. Open Requests table in Airtable
2. Confirm all 6 fields appear in field list
3. Create test record:
   - Environment = sandbox
   - Routing_Decision = she_said_sail
   - Assignment_Status = unassigned
4. Confirm record saves without error
5. Run M-LEAD-INTAKE in Make test mode with payload:
   { "name": "Test Client", "brand": "SSS", "city": "Sydney" }
6. Confirm Make creates a Requests record with Environment = sandbox
7. Confirm Routing_Decision is populated after M-BRAND-ROUTER runs
```

---

## TABLE: Bookings

The Bookings table is the most complex — 129 existing fields. Make.com M-BOOKING-CREATION writes new Booking records. The fields below are additions required for Stage 1 functionality and circular trigger prevention.

| # | Field Name | Field Type | Values / Formula | Default | Required By | Blocker | Add Order | Verification |
|---|-----------|-----------|-----------------|---------|-------------|---------|-----------|--------------|
| 15 | Environment | Single Select | production, sandbox, test | sandbox | M-BOOKING-CREATION, ALL | BLK-001 | Phase 1 | Filter view to sandbox; no prod records appear |
| 16 | Idempotency_Key | Single Line Text | SHA256 hash (64 chars) | (empty) | M-BOOKING-CREATION | BLK-002 | Phase 2 | Accepts 64-char string; unique constraint ideal |
| 17 | Make_Processing | Checkbox | true / false | false | M-BOOKING-CREATION | BLK-007 | Phase 2 | Toggle test; confirm checkbox saves |
| 18 | Needs_Make_Processing | Single Line Text | "process" or empty | (empty) | M-BOOKING-CREATION (trigger field) | BLK-007 | Phase 2 | Set to "process"; confirm Make trigger fires |
| 19 | Last_Make_Run | Date and Time | ISO 8601 | (empty) | M-BOOKING-CREATION (audit) | BLK-007 | Phase 2 | Accepts datetime from Make |
| 20 | Review_Sent | Checkbox | true / false | false | D7_Review_Eligible formula | BLK-005 | Phase 2 | Checkbox saves correctly |
| 21 | D7_Review_Eligible | Formula | `IF(AND(NOT(IS_ERROR({Charter_Date})), DATETIME_DIFF(TODAY(), {Charter_Date}, 'days') >= 7, NOT({Review_Sent})), TRUE(), FALSE())` | Computed | Stage 2 (document now) | BLK-005 | Phase 3 (depends on Review_Sent existing) | Create booking 8 days past; confirm TRUE |

### D7_Review_Eligible Formula Detail

```
Field Type: Formula
Return type: Boolean (or Number where 1=true, 0=false — confirm Airtable behavior)

Formula:
IF(
  AND(
    NOT(IS_ERROR({Charter_Date})),
    DATETIME_DIFF(TODAY(), {Charter_Date}, 'days') >= 7,
    NOT({Review_Sent})
  ),
  TRUE(),
  FALSE()
)

Field name dependencies:
- {Charter_Date} — must be a Date/Time field named exactly "Charter_Date"
- {Review_Sent} — must be a Checkbox field named exactly "Review_Sent"

If your Bookings table uses different field names for charter date, 
adjust the formula accordingly. Check current Bookings field names 
before entering this formula.
```

### Circular Trigger Prevention — Bookings Field Notes

The `Needs_Make_Processing` + `Make_Processing` fields work together as a two-phase lock:

```
Normal flow:
1. Human or native automation sets Needs_Make_Processing = "process"
2. Make watches ONLY Needs_Make_Processing field → trigger fires
3. Make sets Make_Processing = true (locks the record)
4. Make performs all Bookings operations
5. Make sets Make_Processing = false, clears Needs_Make_Processing = ""
6. Step 5 write → does NOT re-trigger Make because Make watches Needs_Make_Processing only,
   and it is now empty (empty does not equal "process" → filter fails → no trigger)

Guard against concurrent runs:
- If Make trigger fires and Make_Processing = true → another run is in progress
- Scenario halts immediately, logs DUPLICATE_PREVENTED to Audit_Log
```

### Risk Table — Bookings

| Field | Risk if Missing |
|-------|----------------|
| Environment | Test bookings appear in production reports. Sandbox data poisons live dataset. |
| Idempotency_Key | Duplicate booking records created on Make retry. Possible double-charge via Stripe. |
| Make_Processing | Circular trigger: every Make write re-triggers Make → infinite loop → API rate limit exceeded → Make account throttled. |
| Needs_Make_Processing | No safe trigger mechanism. Bookings table cannot be watched by Make without circular trigger risk. |
| Last_Make_Run | No audit trail for Make activity on Bookings records. |
| Review_Sent | D7_Review_Eligible formula cannot evaluate correctly. |
| D7_Review_Eligible | Stage 2 review automation cannot identify eligible bookings. Retrofitting after Stage 2 build is costly. |

### Verification Procedure — Bookings Table

```
Step 1: Field presence verification
- Open Bookings table
- Confirm all 7 new fields appear in field list
- Confirm field types match specification

Step 2: Idempotency_Key deduplication test
- Trigger M-BOOKING-CREATION twice with identical payload
- Confirm exactly 1 Booking record created
- Confirm 2nd run creates Audit_Log record: Event_Type = DUPLICATE_PREVENTED

Step 3: Circular trigger test
- Set Needs_Make_Processing = "process" on a test Booking
- Confirm M-BOOKING-CREATION fires ONCE
- Wait 5 minutes; confirm no additional executions in Make history
- Confirm Make_Processing = false and Needs_Make_Processing = "" after scenario

Step 4: D7_Review_Eligible formula test
- Create Booking: Charter_Date = [today minus 8 days], Review_Sent = unchecked
- Confirm D7_Review_Eligible = true
- Create Booking: Charter_Date = [today minus 3 days], Review_Sent = unchecked
- Confirm D7_Review_Eligible = false
- Create Booking: Charter_Date = [today minus 8 days], Review_Sent = checked
- Confirm D7_Review_Eligible = false (already reviewed)
```

---

## TABLE: Clients

The Clients table stores persistent client profiles. M-LEAD-INTAKE checks for existing client records before creating new ones.

| # | Field Name | Field Type | Values / Formula | Default | Required By | Blocker | Add Order | Verification |
|---|-----------|-----------|-----------------|---------|-------------|---------|-----------|--------------|
| 22 | Environment | Single Select | production, sandbox, test | sandbox | M-LEAD-INTAKE, M-BOOKING-CREATION | BLK-001 | Phase 1 | Sandbox filter confirms isolation |
| 23 | Last_Make_Touch | Date and Time | ISO 8601 | (empty) | M-LEAD-INTAKE (audit) | — | Phase 2 | Make writes datetime; field saves |
| 24 | Source_Request_ID | Single Line Text | Airtable Record ID | (empty) | M-LEAD-INTAKE (linkage) | — | Phase 2 | Accepts Airtable record ID string |

### Risk Table — Clients

| Field | Risk if Missing |
|-------|----------------|
| Environment | Test client profiles appear in production CRM views. Client deduplication logic cannot be scoped to environment. |
| Last_Make_Touch | No audit trail. Cannot detect if a Clients record was last modified by Make or a human. |
| Source_Request_ID | No traceable link from Client back to originating Request. Client acquisition source is lost. |

### Verification Procedure — Clients Table

```
1. Confirm all 3 fields appear in Clients field list
2. Trigger M-LEAD-INTAKE with a new client email
3. Confirm Clients record created with Environment = sandbox
4. Trigger M-LEAD-INTAKE again with the same email (deduplication test)
5. Confirm no second Clients record is created
6. Confirm Source_Request_ID on existing Client record is updated or unchanged
```

---

## TABLE: Audit_Log

The Audit_Log table is written by M-AUDIT-LOGGER. It is an append-only log — records are created, never updated or deleted. All fields below must exist before M-AUDIT-LOGGER is activated.

| # | Field Name | Field Type | Values / Formula | Default | Required By | Blocker | Add Order | Verification |
|---|-----------|-----------|-----------------|---------|-------------|---------|-----------|--------------|
| 25 | Event_ID | Single Line Text | SHA256 hash | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts 64-char SHA256 string |
| 26 | Event_Type | Single Select | See enum below | (empty) | M-AUDIT-LOGGER | — | Phase 4 | All enum values selectable |
| 27 | Event_Status | Single Select | SUCCESS, FAILURE, SKIPPED, PARTIAL | (empty) | M-AUDIT-LOGGER | — | Phase 4 | All 4 options present |
| 28 | Scenario_Name | Single Line Text | e.g., M-BRAND-ROUTER | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts text |
| 29 | Scenario_Version | Single Line Text | e.g., 1.0.0 | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts semver string |
| 30 | Make_Execution_ID | Single Line Text | Make bundle/execution ID | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts alphanumeric string |
| 31 | Triggered_By | Single Line Text | webhook, schedule, manual | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts text |
| 32 | Affected_Table | Single Line Text | e.g., Bookings | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts text |
| 33 | Affected_Record_ID | Single Line Text | Airtable record ID | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts rec-prefixed ID |
| 34 | Brand | Single Select | she_said_sail, mare_executive, both, none | (empty) | M-AUDIT-LOGGER | — | Phase 4 | All 4 options present |
| 35 | Environment | Single Select | production, sandbox, test | sandbox | M-AUDIT-LOGGER | BLK-001 | Phase 1 (add with other env fields) | Sandbox filter works |
| 36 | Action_Taken | Long Text | Human-readable description | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts multi-line text |
| 37 | Fields_Modified | Long Text | JSON array string | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts JSON string |
| 38 | Previous_Values | Long Text | JSON object string | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts JSON string |
| 39 | New_Values | Long Text | JSON object string | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts JSON string |
| 40 | Error_Code | Single Line Text | HTTP code or custom | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts alphanumeric |
| 41 | Error_Message | Long Text | Error detail | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts long text |
| 42 | Client_ID | Single Line Text | Airtable record ID | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts rec-prefixed ID |
| 43 | Request_ID | Single Line Text | Airtable record ID | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts rec-prefixed ID |
| 44 | Booking_ID | Single Line Text | Airtable record ID | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts rec-prefixed ID |
| 45 | Duration_MS | Number | Integer milliseconds | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts positive integer |
| 46 | Timestamp | Date and Time | ISO 8601 | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts datetime |
| 47 | Notes | Long Text | Free text | (empty) | M-AUDIT-LOGGER | — | Phase 4 | Accepts multi-line text |

### Event_Type Single Select Enum Values
```
LEAD_RECEIVED
BRAND_ROUTED
CONCIERGE_ASSIGNED
DEPOSIT_LINK_CREATED
DEPOSIT_RECEIVED
BOOKING_CREATED
CONFIRMATION_SENT
DUPLICATE_PREVENTED
AUTOMATION_PAUSED_CHECK
ERROR_OCCURRED
SCENARIO_STARTED
SCENARIO_COMPLETED
```

### Risk Table — Audit_Log

| Risk | Consequence |
|------|-------------|
| Any field missing | Make write to Audit_Log will partially succeed or fail. Log entries will be incomplete. Incident investigation will be impaired. |
| Event_Type missing enum values | Make cannot write the Event_Type value; Airtable rejects the write; Audit_Log entry is lost. |
| Environment field missing | Cannot distinguish test audit entries from production audit entries. |
| Timestamp missing | Audit log has no temporal ordering. Incident timeline reconstruction is impossible. |

### Verification Procedure — Audit_Log Table

```
1. Confirm all 23 fields (including Environment from Phase 1) exist in Audit_Log
2. Confirm Event_Type single select has all 12 enum values
3. Confirm Event_Status has all 4 values
4. Confirm Brand has all 4 values
5. Run M-AUDIT-LOGGER manually in Make test mode with a synthetic event payload
6. Confirm a new record appears in Audit_Log with all fields populated
7. Attempt to UPDATE the created Audit_Log record from Make — confirm this is BLOCKED
   (M-AUDIT-LOGGER should never update Audit_Log records; only create)
8. Confirm Environment = sandbox on the test entry
```

---

## Summary: All Fields by Table and Phase

| Phase | Table | Field | Type | Blocker |
|-------|-------|-------|------|---------|
| 1 | Automation_Health | (entire table — 8 fields) | Various | BLK-003 |
| 1 | Requests | Environment | Single Select | BLK-001 |
| 1 | Clients | Environment | Single Select | BLK-001 |
| 1 | Bookings | Environment | Single Select | BLK-001 |
| 1 | Audit_Log | Environment | Single Select | BLK-001 |
| 2 | Bookings | Idempotency_Key | Single Line Text | BLK-002 |
| 2 | Bookings | Make_Processing | Checkbox | BLK-007 |
| 2 | Bookings | Needs_Make_Processing | Single Line Text | BLK-007 |
| 2 | Bookings | Last_Make_Run | Date/Time | BLK-007 |
| 2 | Bookings | Review_Sent | Checkbox | BLK-005 |
| 2 | Requests | Assigned_Concierge | Single Line Text | — |
| 2 | Requests | Assignment_Status | Single Select | — |
| 2 | Requests | Make_Last_Processed | Date/Time | — |
| 2 | Requests | Routing_Decision | Single Select | — |
| 2 | Requests | Routing_Confidence | Number | — |
| 2 | Clients | Last_Make_Touch | Date/Time | — |
| 2 | Clients | Source_Request_ID | Single Line Text | — |
| 3 | Bookings | D7_Review_Eligible | Formula | BLK-005 |
| 4 | Audit_Log | Event_ID | Single Line Text | — |
| 4 | Audit_Log | Event_Type | Single Select (12 values) | — |
| 4 | Audit_Log | Event_Status | Single Select (4 values) | — |
| 4 | Audit_Log | Scenario_Name | Single Line Text | — |
| 4 | Audit_Log | Scenario_Version | Single Line Text | — |
| 4 | Audit_Log | Make_Execution_ID | Single Line Text | — |
| 4 | Audit_Log | Triggered_By | Single Line Text | — |
| 4 | Audit_Log | Affected_Table | Single Line Text | — |
| 4 | Audit_Log | Affected_Record_ID | Single Line Text | — |
| 4 | Audit_Log | Brand | Single Select (4 values) | — |
| 4 | Audit_Log | Action_Taken | Long Text | — |
| 4 | Audit_Log | Fields_Modified | Long Text | — |
| 4 | Audit_Log | Previous_Values | Long Text | — |
| 4 | Audit_Log | New_Values | Long Text | — |
| 4 | Audit_Log | Error_Code | Single Line Text | — |
| 4 | Audit_Log | Error_Message | Long Text | — |
| 4 | Audit_Log | Client_ID | Single Line Text | — |
| 4 | Audit_Log | Request_ID | Single Line Text | — |
| 4 | Audit_Log | Booking_ID | Single Line Text | — |
| 4 | Audit_Log | Duration_MS | Number | — |
| 4 | Audit_Log | Timestamp | Date/Time | — |
| 4 | Audit_Log | Notes | Long Text | — |

---

## Final Verification Gate

Before any Stage 1 Make scenario is activated in production mode, complete this checklist:

```
[ ] Automation_Health table created with 8 fields
[ ] Automation_Health has exactly 1 control record (global_control)
[ ] Automations_Paused = false confirmed
[ ] Kill switch tested: set true → scenario stops; set false → scenario runs
[ ] All 5 tables have Environment field (Single Select, 3 options)
[ ] Bookings.Idempotency_Key exists (Single Line Text)
[ ] Bookings.Make_Processing exists (Checkbox)
[ ] Bookings.Needs_Make_Processing exists (Single Line Text)
[ ] Bookings.Last_Make_Run exists (Date/Time)
[ ] Bookings.Review_Sent exists (Checkbox)
[ ] Bookings.D7_Review_Eligible formula evaluates correctly on test records
[ ] Requests has all 5 new fields (Assigned_Concierge through Routing_Confidence)
[ ] Clients has all 3 new fields (Environment, Last_Make_Touch, Source_Request_ID)
[ ] Audit_Log has all 23 fields with correct enum values
[ ] Airtable native automations inventory complete (BLK-009)
[ ] All conflicting native automations deactivated for Stage 1
[ ] Will has reviewed and approved all field additions
[ ] Luciana has confirmed Automation_Health kill switch works from Airtable mobile
```

**Owner for sign-off:** Will (field additions) + Luciana (kill switch test)  
**Do not proceed to Make scenario activation until all boxes are checked.**

---

*Document last updated: 2026-05-16. Update field status as fields are added and verified.*
