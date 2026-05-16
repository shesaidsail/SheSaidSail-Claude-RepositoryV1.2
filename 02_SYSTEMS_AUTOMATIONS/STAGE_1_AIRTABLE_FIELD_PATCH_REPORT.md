# STAGE 1 AIRTABLE FIELD PATCH REPORT
## She Said Sail — Pre-Sandbox Make Build Field Audit

**Status:** COMPLETE — No Field Additions Required
**Date:** 2026-05-16
**Base Audited:** appdZ49WqgjRXxA1R (SSS Operations — Production)
**Branch:** claude/resolve-stage1-blockers-usbYp
**Authority:** 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION
**Classification:** Confidential — Internal Use Only

---

## AUDIT SCOPE

This report audits the three tables with outstanding field requirements per the Stage 1 blockers:

1. Bookings (tbl72omPibBkn2hZL)
2. Requests (tblTlSB9CO4dTGodg)
3. Audit Log (tblrMpTfMk8q1eNHp)

Fields audited against the requirements in:
- Build Spec Section 3.2 (Bookings)
- Build Spec Section 3.3 (Requests)
- Build Spec Section 3.6 (Audit Log)
- Systems Intelligence Architecture Section 2.3 (Universal Required Fields)
- Systems Intelligence Architecture Section 2.5 (Bookings)
- Systems Intelligence Architecture Section 2.6 (Requests)
- Systems Intelligence Architecture Section 15.2 (Audit Log)

---

## SECTION 1 — BOOKINGS TABLE AUDIT

**Table ID:** tbl72omPibBkn2hZL
**Field Count at Audit:** 152
**Audit Result:** All required fields present — no additions made

### 1.1 Required Fields — Status

| Required Field | Field ID | Type | Status | Notes |
|---|---|---|---|---|
| Environment | fldb2hN3kxhS3TwUT | singleSelect | ✓ PRESENT | Options: Production / Sandbox / Development |
| UUID | fldaIK4KGF5N4PG8v | formula | ✓ PRESENT | Formula: RECORD_ID() |
| Source_System | fld9DWeMLPP7Iq1NW | singleSelect | ✓ PRESENT | Options: Stripe / Airtable / Make / Manual / API |
| Idempotency_Key | fldjxNVa8Cr9RJhIq | singleLineText | ✓ PRESENT | Written by Make on first execution |
| D7_Review_Eligible | fldDaIF93uwAQ6m8E | formula | ✓ PRESENT | CHARTER-006 gate field |
| Refund_Issued | fldImSr8nOLb60UaZ | checkbox | ✓ PRESENT | |
| Refund_Amount | fldNzrIi2fM36TYUJ | currency | ✓ PRESENT | Protected field — Will only |
| Agent_Status | fldHxIcogJjxFodS1 | singleSelect | ✓ PRESENT | Options: AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED |
| AI_Confidence_Score | fldlT6q0ADIMyx7MC | number | ✓ PRESENT | 0–100 |
| Last_Human_Touch | fld20YCVPEsYAQKqr | dateTime | ✓ PRESENT | |
| Last_AI_Action | fldac8tOX86zhnVBx | dateTime | ✓ PRESENT | |
| Emergency_Flag | fldHxfGgVuAH1SKBO | checkbox | ✓ PRESENT | EMERGENCY-001 trigger field |
| Automations_Paused | flduB7GqI7TOdQKUB | checkbox | ✓ PRESENT | Pre-send gate — all outbound scenarios |
| Chargeback_Risk | fldDG8mWQNfsIbtVw | singleSelect | ✓ PRESENT | Options: LOW / MEDIUM / HIGH / ACTIVE |
| Agreement_Signed | fldlldzw0ocw5FMXB | checkbox | ✓ PRESENT | Required for CONFIRMED on bookings > $5,000 |
| Brand | fldG71fePcaCp9uZN | singleSelect | ✓ PRESENT | Options: SSS / ME |
| Charter_Grade | fldjmUqi39RMWI8qI | singleSelect | ✓ PRESENT | A / B / C / D / F |
| Refund_Status | fld31RWwrhbNmq48y | singleSelect | ✓ PRESENT | Protected field |

### 1.2 Core Operational Fields — Confirmed Present

| Field | Field ID | Type |
|---|---|---|
| Booking ID | fldfhYXwP5E4agChR | formula |
| Status | fldf51usvsXDhp2tf | singleSelect |
| Charter Date | fldCzvnOsy7WgdOTa | dateTime |
| Client (linked) | fldLaXR9F9auWh1CX | multipleRecordLinks |
| Yacht (linked) | fldXCjzBCmX9nkVrG | multipleRecordLinks |
| Package (linked) | fld9Da38i9cyejgsu | multipleRecordLinks |
| City (linked) | fldDYU12jK3MGVh5O | multipleRecordLinks |
| Brokers (linked) | fldurhNwSNuZ4R3O7 | multipleRecordLinks |
| Stripe Checkout URL | fldWLHumliz28w0Sb | url |
| Stripe Payment Intent ID | fldtQ5VtfW0MgvaS6 | singleLineText |
| Balance Payment Link | fldCGiLpMHlwQ1f1E | url |
| Balance Paid | fldvAs16tfzdkOkOE | checkbox |
| Balance Due Date | fldxPFUgOXt5JayF2 | date |
| Package Price | fldvHvLaQ8BUhkplm | currency |
| Net Profit | fldo5UE1UGJHBbj44 | formula |
| Margin Pct | fldClbWCv5IhDVW46 | formula |
| Audit_Log (linked) | fldK9ePiLrWfvrjpA | multipleRecordLinks |
| Founder Decisions (linked) | fldRYVllHIFoNcjJE | multipleRecordLinks |
| Automation_Health (linked) | fldutXOFOw7H3DLy7 | multipleRecordLinks |
| Occasions | fldghdjUFtlwGblxf | singleSelect |
| HV Booking | fld7b21pShgN7UV7p | checkbox |

### 1.3 Warnings — Bookings

**⚠ WARNING: HV Booking naming inconsistency**

- Current field name: `HV Booking` (fld7b21pShgN7UV7p)
- Governance spec name: `HV_Client`
- Field type: checkbox ✓ correct
- Impact on Make: None — Make references field ID, not display name
- Impact on Airtable views/formulas: Affects any formula referencing `{HV Booking}` vs `{HV_Client}` by name. D7_Review_Eligible formula should use field ID, which is correct.
- Resolution: Rename field to `HV_Client` before production promotion. This is a cosmetic fix only. Coordinate with Will during a low-traffic window. No record data is affected.
- Priority: LOW — does not block sandbox or production Make build

### 1.4 Fields Not Added (Confirmed Out of Stage 1 Scope)

The following fields from the full Build Spec are acknowledged but not required for Stage 1 Make build. They will be addressed in Phase 4:

- P&L field extraction (Boat Cost, Labor Cost, F&B Cost, City Manager Payout → P&L Per Charter sync)
- Automation tracking extraction (D0–D60 send checkboxes → Automation_Health table)
- Crew reporting extraction (Crew Report, Charter_NPS → Operational_Audits table)
- Packages table rebuild (8 → 25 fields)
- AI_Prompt_Versions table replacement

---

## SECTION 2 — REQUESTS TABLE AUDIT

**Table ID:** tblTlSB9CO4dTGodg
**Field Count at Audit:** 64
**Audit Result:** All required fields present — WARNING on Agent_Status field type

### 2.1 Required Fields — Status

| Required Field | Field ID | Type | Status | Notes |
|---|---|---|---|---|
| Agent_Status | fld7T2dzrtKEdJqD1 | multilineText | ⚠ WRONG TYPE | Should be singleSelect — see Warning 2-A |
| Last_AI_Action | fldPbC4QrMurdswml | dateTime | ✓ PRESENT | |
| Escalation_Reason | fldHjvNndj3BYZTCI | multilineText | ✓ PRESENT | Long text — correct |
| AI_Confidence_Score | fldMvecutRDu7kUlh | number | ✓ PRESENT | 0–100 |
| Last_Human_Touch | fld9hYAcrLEZ4ADui | dateTime | ✓ PRESENT | |
| Environment | fldF8PaiQacfKVtyE | singleSelect | ✓ PRESENT | |
| UUID | fldbPAwXaY0FyUKLx | formula | ✓ PRESENT | RECORD_ID() |
| Source_System | fldhWyTQgG1AYpsZp | singleSelect | ✓ PRESENT | |
| Brand | fldHehlMwdqIjX3sq | singleSelect | ✓ PRESENT | |

### 2.2 Warnings — Requests

**⚠ WARNING 2-A: Agent_Status Field Type Mismatch — MUST FIX BEFORE INBOUND-002**

| Property | Current | Required |
|---|---|---|
| Field name | Agent Status | Agent_Status |
| Field ID | fld7T2dzrtKEdJqD1 | — |
| Type | multilineText | singleSelect |
| Required options | — | AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED |

**Why this blocks INBOUND-002:**
Make's INBOUND-002 scenario filters Requests where Agent_Status = AI_RESPONDING. A multilineText field cannot be matched by exact equality in Airtable's filter API. Make will either:
- Return all records (no filter effect)
- Return zero records (invalid filter)
Either outcome means INBOUND-002 silently fails or processes every request regardless of agent state.

**Resolution procedure (must execute before INBOUND-002 build):**
1. Export Requests table to CSV — capture all current Agent Status text values
2. Create new field: name `Agent_Status`, type `singleSelect`, options: `AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED`
3. Review exported values, map to closest option, update records manually where needed
4. Rename old field: `Agent_Status_DEPRECATED_TEXT`
5. Make scenario references update to new field ID (TBD after creation)
6. Confirm Airtable views referencing old field are updated
7. Log change in Audit Log: Action_Type = SCHEMA_CHANGE, Source_System = Manual

**Note on Agent Status (Visible) field (fldxuo4jAq24oczGu, aiText):** This is a separate Airtable AI-generated field, not a governance field. It is not used by Make. Do not modify.

### 2.3 Core Operational Fields — Confirmed Present

| Field | Field ID | Type |
|---|---|---|
| Request ID | fldRwKUcrhfKlmZPL | autoNumber |
| Status | fldv1NEyNPuXqv5bT | singleSelect |
| First Name | fldouoNURHn5Emq6l | singleLineText |
| Last Name | fldsQWCChboxSDeoE | singleLineText |
| Email | fldbsr8J2CGxOR76b | email |
| Phone | fldrzCt39oqn2Lo5N | phoneNumber |
| Preferred Date | fldiz7m1LjsTIXYUH | date |
| Guest Count | fldDJzUNAaucWL6g7 | number |
| Occasion | fldsKHDXCN4O1mnBl | singleSelect |
| Stripe Payment Link | fldxHIEuR1TZxUZJU | url |
| Converted_To_Booking | flduZNR7PRNxd7jwk | checkbox |
| Do_Not_Auto_Send | fld6gF1E5wZ3rHmUg | checkbox |
| Test_Mode | fld9j5cCPNuJwWHgY | checkbox |
| Brand_Detected | fldC2fXzo3x9rpQbJ | singleSelect |

---

## SECTION 3 — AUDIT LOG TABLE AUDIT

**Table ID:** tblrMpTfMk8q1eNHp
**Field Count at Audit:** 27
**Audit Result:** All 8 required governance fields present — no additions required

### 3.1 Required Governance Fields (Section 3.6 of Build Spec) — Status

| Required Field | Field ID | Type | Status |
|---|---|---|---|
| Prompt_Version | fld9zzJ1I6T36Ntz9 | singleLineText | ✓ PRESENT |
| AI_Confidence_Score | fld3BLRrstQ63pFOT | number | ✓ PRESENT |
| Approval_State | fldbFhF24sLLjuGeU | singleSelect | ✓ PRESENT |
| Reviewed_By | fld1flh6agYM8s6BE | singleLineText | ✓ PRESENT |
| Rollback_Linkage | fldN1w5pouMkVSdKN | singleLineText | ✓ PRESENT |
| Environment | fldhyiPPZT11OZ4Di | singleSelect | ✓ PRESENT |
| Brand | fldKAcFSFLXQjtAdu | singleSelect | ✓ PRESENT |
| City | fldAluJ5XTPdispDD | singleLineText | ✓ PRESENT |

### 3.2 Full Audit Log Schema — Confirmed

| Field | Field ID | Type |
|---|---|---|
| Log Entry | fldE6qMerDiHwDYLd | multilineText (primary) |
| Action Type | fldMxH58m0A6ijvaH | singleSelect |
| Timestamp | fldSffNxegZPYLfxv | dateTime |
| Changed Table | fldIku0PufvqXqieh | singleSelect |
| Scenario ID | fldI6kmwtjrR2yeQi | singleLineText |
| Actor | fldtQgM2KgxJWJEZD | singleLineText |
| AI Change Description | fldPea0POrx1TbpN0 | aiText |
| Related Booking | fld0d3LPH68zvWNsC | multipleRecordLinks |
| Related Yacht | fldunOHlAWY0m6SWN | multipleRecordLinks |
| Severity Level | fldLqo06YKIwYll1t | singleSelect |
| Automated Action | fldZ4dobYIusZLVL5 | checkbox |
| Follow-up Required | fldr9t0TdgIhgtKgu | checkbox |
| Linked Client | fldG2TfZv4J7MC5Gu | multipleRecordLinks |
| Linked Broker | fld8xr6ViAQsLTIDc | multipleRecordLinks |
| Prior State | fldAtzMmMZj7WKYC8 | singleLineText |
| New State | fldJ7HLsMmWbOErAO | singleLineText |
| Payload Summary | fldU2QuTX8Gjf2CKJ | multilineText |
| Environment | fldhyiPPZT11OZ4Di | singleSelect |
| UUID | fldHl2wQLhBtL5vjL | formula |
| Source_System | fldO0gSri074JWjKn | singleSelect |
| Brand | fldKAcFSFLXQjtAdu | singleSelect |
| Prompt_Version | fld9zzJ1I6T36Ntz9 | singleLineText |
| AI_Confidence_Score | fld3BLRrstQ63pFOT | number |
| Approval_State | fldbFhF24sLLjuGeU | singleSelect |
| Reviewed_By | fld1flh6agYM8s6BE | singleLineText |
| Rollback_Linkage | fldN1w5pouMkVSdKN | singleLineText |
| City | fldAluJ5XTPdispDD | singleLineText |

### 3.3 Gap Notes — Audit Log

**Noted gap vs. Architecture spec (Section 15.2):**
The Systems Intelligence Architecture specifies a `Prompt_Version` field as a **Linked Record** to AI_Prompt_Versions. Current implementation is `singleLineText`. This means prompt version is recorded as text (e.g., "AIV-0001") rather than a linked record.

Functional impact: Audit logs correctly record which prompt version was used. The linked-record form would enable rollup queries but is not required for Stage 1 Make build.
Resolution: Convert to linked record type in Phase 4 when AI_Prompt_Versions table migration is complete. Note in architecture amendment log.
Priority: LOW — does not block Stage 1.

---

## SECTION 4 — SANDBOX BASE AUDIT

**Base Name:** SSS Sandbox
**Base ID:** appxOoLdiIVt733kV
**Permission Level:** create
**Audit Date:** 2026-05-16

### 4.1 Tables Present

| Table Name | Table ID | Purpose |
|---|---|---|
| Sandbox_Control | tblSA3xc4vNqBAFL4 | Phase tracking and test operation log |

### 4.2 Sandbox_Control Fields

| Field | Field ID | Type |
|---|---|---|
| Test_Name | fldbBNaHhVl3oame3 | singleLineText (primary) |
| Phase | fldBJhxJLipApM8eV | singleSelect |
| Status | fldYZzPZW5378kWmk | singleSelect |
| Environment | fldqwYkuhkYMvxFez | singleSelect |
| Test_Type | fldC8wIlAssS9tMxi | singleSelect |
| Notes | fldAlW9eioJFAL9qQ | multilineText |
| Executed_By | fldgmEbwEEJyZaPAa | singleLineText |
| Executed_At | flds3HbJcPOEg3NcL | dateTime |
| Result_Detail | fldmpC1QakmYzwGjH | multilineText |
| Risk_Level | fldb0cvvrYf7fRR7c | singleSelect |

### 4.3 Sandbox Governance Verification

- [x] Sandbox base is isolated from production base (appdZ49WqgjRXxA1R) — no cross-base links exist
- [x] Sandbox_Control table description confirms: "No production data. No Make integrations. Safe to modify freely."
- [x] Base was created as new, not repurposed from a fragmented base with existing data
- [ ] Make sandbox scenarios must be configured to point to appxOoLdiIVt733kV — confirm before first test run

**Action before first Make scenario test:**
All Make scenario Airtable module connections for sandbox runs must reference `appxOoLdiIVt733kV`. Production module connections reference `appdZ49WqgjRXxA1R`. These must never be swapped.

---

## SECTION 5 — FIELD CHANGES MADE

**No Airtable field additions, deletions, or modifications were made in this patch.**

All required fields identified in the Stage 1 blockers were confirmed present in the live Airtable base. No schema changes were required.

Prior work (Phase 1 and Phase 3) had already addressed the field additions specified in the Build Spec:
- Phase 1 universal fields: Environment, UUID, Source_System (added to Bookings, Requests, Audit Log)
- Phase 1 Bookings-specific: Idempotency_Key, D7_Review_Eligible, Refund_Issued, Refund_Amount
- Phase 1 Requests-specific: Escalation_Reason, AI_Confidence_Score, Last_Human_Touch, Last_AI_Action
- Phase 1 Audit Log: All 8 governance fields

---

## WARNING REGISTER

| Warning ID | Table | Field | Issue | Blocks Sandbox? | Blocks Production? | Action Owner | Priority |
|---|---|---|---|---|---|---|---|
| W-001 | Bookings | HV Booking | Field name should be HV_Client per governance spec | No | No (cosmetic) | Will | LOW |
| W-002 | Requests | Agent_Status | Field is multilineText, must be singleSelect before INBOUND-002 | No | YES | Will + Luciana | HIGH |
| W-003 | Audit Log | Prompt_Version | Should be linked record type, not singleLineText | No | No (Phase 4) | Phase 4 | LOW |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_1_AIRTABLE_FIELD_PATCH_REPORT v1.0*
*Date: 2026-05-16*
*No schema changes made — all required fields confirmed present*
*Authority: 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION*
