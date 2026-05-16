# POST-PHASE-4 SCHEMA REGISTRY
## She Said Sail + Mare Executive — Airtable Architecture for Stage 1 Make Build

**Document Version:** 1.0  
**Status:** PRODUCTION IMPLEMENTATION REFERENCE  
**Effective Date:** May 2026  
**Owner:** Will (Founder)  
**Scope:** All tables read or written by Stage 1 Make scenarios  
**Classification:** Confidential — Internal Use Only  
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED  
**Systems Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION  
**Airtable Ops Base:** appdZ49WqgjRXxA1R  
**Airtable Financials Base:** apprDKQtV2GInThwE  

> **Registry Authority Statement**
>
> This document is the definitive field-level schema reference for the post-Phase-4 Airtable architecture. It governs every table that Stage 1 Make scenarios may read or write. No Make module may reference a field not listed here as Make-accessible. No Make module may write to a field marked PROTECTED. All schema gaps listed in Section 6 must be resolved before the affected scenario enters sandbox testing.

---

## TABLE OF CONTENTS

| Section | Title |
|---------|-------|
| 1 | Registry Status — Phase 3 and Phase 4 Summary |
| 2 | Table Registry — All Tables Used by Stage 1 |
| 3 | Field Addition Queue — Priority-Ordered Pre-Launch Requirements |
| 4 | Protected Fields — Make Must Never Overwrite |
| 5 | Airtable API Token Scope for Stage 1 |
| 6 | Known Gaps and Unknowns — Blockers Requiring Confirmation |

---

## SECTION 1 — REGISTRY STATUS

### 1.1 Phase 3 Migration Summary

Phase 3 consolidated 9 tables from 3 fragmented source bases into the governed SSS Operations base (appdZ49WqgjRXxA1R). All 60 records were migrated with full governance field decoration (UUID, Environment, Brand, Source_System, Legacy_Record_ID). Source bases remain intact for rollback.

| Table | Source Base | Destination Table ID | Records | Phase 3 Status |
|-------|-------------|---------------------|---------|----------------|
| Vessel_Maintenance | apppFfA2VZVmamvXe | tblmYWqqIu1Cidb4g | 2 | COMPLETE |
| Emergency_Escalations | apppFfA2VZVmamvXe | tblDbeRf3qO3xvqhK | 2 | COMPLETE |
| Incident_Reports | apppFfA2VZVmamvXe | tblO22Hh9lSTnhuu7 | 2 | COMPLETE |
| Operational_Audits | apppFfA2VZVmamvXe | tblAHYfl31529xUGr | 2 | COMPLETE |
| City_Financials | apppFfA2VZVmamvXe | tblycuku5Yq9s3fIw | 2 | COMPLETE |
| Concierge_Operators | app2FbmVD44BXShyx | tblX61IB2qjDmac8l | 3 | COMPLETE |
| Emergency_Protocols | app2FbmVD44BXShyx | tblsTbNXo4Pa9mDSW | 8 | COMPLETE |
| Make_Scenarios | app2FbmVD44BXShyx | tbl08IpivapVQZUto | 8 | COMPLETE |
| Influencers | appVWYY9Fp6tKu94m | tbl69Cguka4K4qgPO | 31 | COMPLETE |
| Guests | apppFfA2VZVmamvXe | tblpj4SwaSXu2vbVN | 0 | COMPLETE (empty) |
| Regional_Directors | apppFfA2VZVmamvXe | tblBK5EBPh5ppc8vw | 0 | COMPLETE (empty) |
| ME_Pricing | app2FbmVD44BXShyx | — | 5 | DEFERRED — Phase 4 merge into Packages |

### 1.2 Phase 4 Optimization Status

Phase 4 targets schema optimization of existing high-risk tables. These tables have active records and active or pending Make dependencies. All Phase 4 changes execute during confirmed low-traffic windows (Sunday night preferred) with Will on standby.

| Table | Table ID | Phase 4 Action | Current Fields | Target Fields | Phase 4 Status |
|-------|----------|---------------|---------------|---------------|----------------|
| Requests | tblTlSB9CO4dTGodg | Optimize — add 5 autonomy fields | ~57 | 45 optimized | IN PROGRESS |
| Bookings | tbl72omPibBkn2hZL | Reduce — extract 59 fields to related tables | 129 | 70 | IN PROGRESS |
| Packages | tblwDw2hkKW5moSr9 | Rebuild — add 17 fields, merge ME_Pricing | 8 | 25 | IN PROGRESS |
| AI_Prompt_Versions | tbl0FJkA1E6a70cxX | Replace — retire 9-field version, install 26-field schema | 9 | 26 | IN PROGRESS |
| Partner Outreach | tblnjGWa6JNiogfCo | Reduce — extract relationship data to linked table | 84 | 45 | IN PROGRESS |

### 1.3 Make-Readiness Summary

| Table | Make-Readiness | Blocking Issues |
|-------|---------------|-----------------|
| Requests | PARTIAL | Missing 3 autonomy fields; Environment field unconfirmed |
| Bookings | BLOCKED | 129 fields; missing Idempotency_Key; circular trigger risk; Environment field missing |
| Clients | PARTIAL | Needs UUID formula field and Environment field |
| Audit Log | BLOCKED | Missing 8 governance fields required by M-AUDIT-LOGGER |
| Concierge_Operators | READY | Phase 3 migration complete; all required fields present |
| Packages | BLOCKED | Missing Deposit_Rate_Pct and 16 other required fields |
| Automation_Health | BLOCKED — TABLE DOES NOT EXIST | Must be created before Stage 1 build |
| Emergency_Escalations | READY | Phase 3 migration complete; Stage 1 does not write to this table |
| AI_Prompt_Versions | BLOCKED | Current 9-field schema missing Make_Variable_Name, Will_Approved, Status |

---

## SECTION 2 — TABLE REGISTRY

### 2.1 Requests (tblTlSB9CO4dTGodg)

**Role in Stage 1:** Primary trigger table. M-LEAD-INTAKE creates records here. M-CONCIERGE-ASSIGNMENT reads and updates records here. M-BOOKING-CREATION promotes records to Bookings.

| Attribute | Value |
|-----------|-------|
| Table ID | tblTlSB9CO4dTGodg |
| Current Field Count | ~57 |
| Target Field Count (post-Phase-4) | 45 optimized |
| Phase 3 Status | Not applicable — native main base table |
| Phase 4 Status | IN PROGRESS — adding 5 autonomy fields |
| Make-Readiness | PARTIAL |

**Fields Used by Stage 1:**

| Field Name | Type | Purpose | Make Write Permission | Scenario |
|------------|------|---------|----------------------|----------|
| Name / Request_ID | Formula / Text | Human-readable record ID (REQ-YYYY-NNNN) | READ ONLY after creation | All |
| Brand | Single Select: SSS / ME / AMBIGUOUS | Output from M-BRAND-ROUTER | WRITE (M-LEAD-INTAKE) | M-LEAD-INTAKE |
| Brand_Confidence | Single Select: HIGH / LOW | Router confidence level | WRITE (M-LEAD-INTAKE) | M-LEAD-INTAKE |
| Brand_Signal_Source | Text | hint / occasion / keyword / default | WRITE (M-LEAD-INTAKE) | M-LEAD-INTAKE |
| Requires_Human_Brand_Review | Checkbox | Flag for Luciana review | WRITE (M-LEAD-INTAKE) | M-LEAD-INTAKE |
| Status | Single Select | NEW / ASSIGNED / AVAILABILITY_CONFIRMED / BOOKING_CREATED | WRITE | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION |
| Agent_Status | Single Select: AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED | AI authority state | WRITE | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT |
| Concierge_Assigned | Linked Record (Concierge_Operators) | Assigned operator | WRITE (M-CONCIERGE-ASSIGNMENT) | M-CONCIERGE-ASSIGNMENT |
| Assignment_Timestamp | DateTime | When concierge was assigned | WRITE (M-CONCIERGE-ASSIGNMENT) | M-CONCIERGE-ASSIGNMENT |
| Linked_Booking_ID | Text | Reference to created Booking record | WRITE (M-BOOKING-CREATION) | M-BOOKING-CREATION |
| Environment | Single Select: Production / Sandbox / Development | Sandbox isolation gate | WRITE at creation (M-LEAD-INTAKE) | M-LEAD-INTAKE |
| Source_System | Single Select | Make / Airtable / Manual / API | WRITE at creation | M-LEAD-INTAKE |
| Idempotency_Key | Text | SHA256(email+charter_date+brand+source) | WRITE at creation; READ for dedup | M-LEAD-INTAKE |
| Email | Email | Client email — dedup key | READ for dedup; WRITE at creation | M-LEAD-INTAKE |
| Charter_Date | Date | Requested charter date — dedup key | READ for dedup; WRITE at creation | M-LEAD-INTAKE |
| Created_At | DateTime | Record creation timestamp | READ ONLY (Airtable system) | All |
| Last_AI_Action | DateTime | Timestamp of last Make action on record | WRITE | M-SLACK-ALERTS |
| Stripe_Link | URL | Reference copy of deposit link | WRITE (M-STRIPE-DEPOSIT) | M-STRIPE-DEPOSIT |
| Deposit_Sent_At | DateTime | When deposit link was sent | WRITE (M-STRIPE-DEPOSIT) | M-STRIPE-DEPOSIT |

**Blocker Fields — Must Exist Before Stage 1:**

| Field Name | Type | Status | Blocks | Priority |
|------------|------|--------|--------|----------|
| Environment | Single Select | MISSING — must add | ALL scenarios | CRITICAL |
| Idempotency_Key | Text | MISSING — must add | M-LEAD-INTAKE | CRITICAL |
| Escalation_Reason | Long Text | MISSING — must add | M-CONCIERGE-ASSIGNMENT | HIGH |
| AI_Confidence_Score | Number 0-100 | MISSING — must add | M-BRAND-ROUTER, future INBOUND-002 | HIGH |
| Last_Human_Touch | DateTime | MISSING — must add | Future INBOUND-002 | MEDIUM |

**Read Pattern for Make:**
M-CONCIERGE-ASSIGNMENT watches Requests using Airtable polling (15-minute interval) filtered to: `Status = NEW` AND `Concierge_Assigned IS EMPTY`. M-LEAD-INTAKE queries Requests before creation to check idempotency key. M-BOOKING-CREATION reads the full Request record as the data source for Booking creation.

**Write Pattern for Make:**
M-LEAD-INTAKE creates new Requests via API. All subsequent writes are UPDATE operations targeting specific fields only — never a full-record overwrite. Every Make write to Requests must include the `Environment` field value and must respect the `Automations_Paused` field if present.

**Circular Trigger Risk:** LOW. Requests table triggers M-CONCIERGE-ASSIGNMENT via Airtable watch. M-CONCIERGE-ASSIGNMENT writes back to Requests. The idempotency check on `Concierge_Assigned IS EMPTY` prevents the Airtable watch from re-triggering assignment after it is set. Confirm the Airtable watch filter includes `Concierge_Assigned IS EMPTY` — this is the guard that breaks the potential loop.

---

### 2.2 Bookings (tbl72omPibBkn2hZL)

**Role in Stage 1:** Central lifecycle record. M-BOOKING-CREATION creates records here. M-STRIPE-DEPOSIT writes Stripe fields. M-BOOKING-CONFIRMATION reads and writes confirmation state.

| Attribute | Value |
|-----------|-------|
| Table ID | tbl72omPibBkn2hZL |
| Current Field Count | 129 |
| Target Field Count (post-Phase-4) | 70 |
| Phase 3 Status | Not applicable — native main base table |
| Phase 4 Status | IN PROGRESS — extracting financial fields to P&L Per Charter; extracting automation tracking fields to Automation_Health |
| Make-Readiness | BLOCKED |

**Fields Safe to Write in Stage 1 (pre-Phase-4-completion):**

The 129-field Bookings table contains three categories of fields from Make's perspective. Stage 1 must write only to Category A fields. Category B fields may be read but not written. Category C fields are strictly protected.

| Category | Description | Make Behavior |
|----------|-------------|---------------|
| A — Stage 1 Write-Safe | Core booking lifecycle fields that Stage 1 creates and manages | WRITE permitted |
| B — Stage 1 Read-Only | Fields containing data Make needs but must not modify | READ only |
| C — Protected | Financial, formula, and governance fields | NEVER touch |

**Category A — Stage 1 Write-Safe Fields:**

| Field Name | Type | Written By | Scenario |
|------------|------|-----------|----------|
| Booking_ID | Formula / Text | Created by M-BOOKING-CREATION | M-BOOKING-CREATION |
| Source_Request_ID | Text | Links back to originating Request | M-BOOKING-CREATION |
| Client (linked) | Linked Record | Links to Clients table record | M-BOOKING-CREATION |
| Brand | Single Select: SSS / ME | Passed from Request | M-BOOKING-CREATION |
| Charter_Date | Date | Passed from Request | M-BOOKING-CREATION |
| Group_Size | Number | Passed from Request | M-BOOKING-CREATION |
| Package (linked) | Linked Record | Links to Packages table | M-BOOKING-CREATION |
| City | Single Select | Passed from Request | M-BOOKING-CREATION |
| Status | Single Select | AVAILABILITY_PENDING → AVAILABILITY_CONFIRMED → DEPOSIT_SENT → DEPOSIT_PAID → CONFIRMED | M-BOOKING-CREATION, M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| Environment | Single Select | Production / Sandbox | M-BOOKING-CREATION |
| Source_System | Single Select | Make | M-BOOKING-CREATION |
| Idempotency_Key | Text | SHA256(Request_ID+scenario+timestamp) | M-BOOKING-CREATION |
| Stripe_Link | URL | Payment link URL from Stripe API | M-STRIPE-DEPOSIT |
| Stripe_Payment_Intent_ID | Text | Stripe PI ID for dedup and rollback | M-STRIPE-DEPOSIT |
| Deposit_Amount | Currency | Calculated deposit = Package_Price × Deposit_Rate_Pct | M-STRIPE-DEPOSIT |
| Deposit_Sent_At | DateTime | When deposit link was generated | M-STRIPE-DEPOSIT |
| Confirmation_Sent | Checkbox | True when confirmation email has been sent | M-BOOKING-CONFIRMATION |
| Confirmation_Sent_At | DateTime | Timestamp of confirmation send | M-BOOKING-CONFIRMATION |
| Confirmation_Channel | Single Select: Email / SMS | Channel used for confirmation | M-BOOKING-CONFIRMATION |
| Automations_Paused | Checkbox | Circuit breaker — Make reads this FIRST on every execution | READ by all; WRITE by Luciana manually only |
| Emergency_Flag | Checkbox | Emergency circuit breaker | READ by all; WRITE by Luciana/Will manually only |
| Last_Automation_Timestamp | DateTime | Last Make execution timestamp on this record | WRITE by all Stage 1 scenarios |

**Category B — Stage 1 Read-Only Fields:**

| Field Name | Type | Why Make Reads It | Why Make Must Not Write It |
|------------|------|------------------|---------------------------|
| Package_Price | Currency | Needed to calculate Deposit_Amount | Formula-derived or human-set pricing — Make overwrites create data integrity breach |
| HV_Client | Checkbox | High-value routing flag | Set by Luciana based on client relationship intel |
| Broker (linked) | Linked Record | For context in confirmation email | Set by Luciana after broker coordination |
| Assigned_Concierge | Linked Record | For context in confirmation email | Set via Concierge_Operators assignment — Requests table owns this, not Bookings |
| Chargeback_Risk | Single Select | Risk gate for Stage 2 review trigger | Will and Luciana only |

**Phase-4 Fields Being Extracted (Do Not Reference in Stage 1):**

The following 20 fields are being extracted from Bookings to Automation_Health as part of Phase 4. Stage 1 scenarios must not write to these fields directly — Stage 2 will write through the Automation_Health linked record.

`D0_Sent, D1_Sent, D3_Sent, D7_Sent, D9_Gift_Sent, D14_Sent, D30_Sent, D60_Sent, HV_D2_Call_Done, HV_D5_Sent, HV_D21_Sent, HV_D23_Sent, D7_Reminder_Sent, D10_Reminder_Sent, D72hr_Reminder_Sent, D48hr_Reminder_Sent, Charter_Brief_Sent, Charter_Brief_All_Vendors_Confirmed, T7_Confirmed, T48_Captain_Confirmed`

**Circular Trigger Risk:** HIGH. Bookings has 129 fields. Any native Airtable automation watching "record updated" will fire on every Make write. Before Make builds any scenario that writes to Bookings: (1) Will must complete a full audit of all native Airtable automations on this table, (2) every native automation watching Bookings must be scoped to specific field changes — never the generic record update trigger. This audit is BLK-009 in the Stage 1 Blocker Resolution Report and is a hard prerequisite for M-BOOKING-CREATION.

---

### 2.3 Clients (tblr84vRIWC5HmKvo)

**Role in Stage 1:** Client creation and deduplication in M-LEAD-INTAKE and M-BOOKING-CREATION. Read-only in M-BOOKING-CONFIRMATION for personalization.

| Attribute | Value |
|-----------|-------|
| Table ID | tblr84vRIWC5HmKvo |
| Current Field Count | ~40 |
| Phase 3 Status | Not applicable — native main base table |
| Phase 4 Status | Optimize — add UUID formula and Environment field |
| Make-Readiness | PARTIAL |

**Fields for Client Creation in M-BOOKING-CREATION:**

| Field Name | Type | Make Operation | Source | Required for Stage 1 |
|------------|------|---------------|--------|----------------------|
| Name | Text | WRITE at creation | Webhook payload | YES |
| Email | Email | WRITE at creation; READ for dedup | Webhook payload | YES |
| Phone | Phone Number | WRITE at creation | Webhook payload | YES |
| Brand | Single Select: SSS / ME | WRITE at creation | M-BRAND-ROUTER output | YES |
| Source_System | Single Select | WRITE at creation | Hardcoded: Make | YES |
| Environment | Single Select | WRITE at creation | Make environment variable | YES — FIELD MUST BE ADDED |
| UUID | Formula: RECORD_ID() | READ only — auto-generated | Airtable | YES — FIELD MUST BE ADDED |
| CLT_ID | Formula / Text | READ only after creation | Airtable formula | YES |
| Created_At | DateTime | READ only | Airtable system | YES |
| HV_Client | Checkbox | READ only in Stage 1 | Set by Luciana manually | READ ONLY |
| Lifetime_Bookings | Count / Rollup | READ only | Auto-populated by linked Bookings | READ ONLY |

**Deduplication Logic:** M-LEAD-INTAKE searches Clients by exact email match before any record creation. If email match found: link existing Client ID to new Request, do not create new Client record, log `CLIENT_LINKED` to Audit Log. If no match: create new Client record, link to Request, log `CLIENT_CREATED`.

---

### 2.4 Audit Log (tblrMpTfMk8q1eNHp)

**Role in Stage 1:** Append-only immutable log. Every Tier A autonomous action by any Stage 1 scenario must produce one Audit Log record via M-AUDIT-LOGGER. No Make scenario has UPDATE or DELETE access to this table.

| Attribute | Value |
|-----------|-------|
| Table ID | tblrMpTfMk8q1eNHp |
| Current Field Count | 17 |
| Required Field Count (post-expansion) | 25 |
| Phase 4 Status | IN PROGRESS — adding 8 governance fields |
| Make-Readiness | BLOCKED — 8 fields missing |

**All Fields Including the 8 Missing Fields That Must Be Added:**

| Field Name | Type | Status | Required For | Make Write Permission |
|------------|------|--------|-------------|----------------------|
| Audit_Key | Text | EXISTS | Deduplication soft-check | WRITE at creation |
| Event_Type | Single Select | EXISTS | Event classification | WRITE at creation |
| Scenario_Name | Text | EXISTS | Human-readable source | WRITE at creation |
| Brand | Single Select: SSS / ME | EXISTS | Brand attribution | WRITE at creation |
| Environment | Single Select | EXISTS | Sandbox isolation | WRITE at creation |
| Actor | Single Select: Make / Claude / Human | EXISTS | Action attribution | WRITE at creation |
| Affected_Record_ID | Text | EXISTS | Record linkage | WRITE at creation |
| Affected_Table | Text | EXISTS | Table name context | WRITE at creation |
| Outcome | Single Select: SUCCESS / FAILURE / SKIP | EXISTS | Result state | WRITE at creation |
| Timestamp | DateTime | EXISTS | Immutable event time | WRITE at creation |
| Notes | Long Text | EXISTS | Error messages, context | WRITE at creation |
| Error_Code | Text | EXISTS | HTTP/Make error codes | WRITE at creation |
| Log_ID | Formula / Text | MISSING — MUST ADD | M-AUDIT-LOGGER self-reference and cross-linking | WRITE at creation |
| Source_Scenario_ID | Text | MISSING — MUST ADD | Make scenario numeric ID (e.g., 4829371) — required by immutability governance | WRITE at creation |
| Prompt_Version_ID | Text | MISSING — MUST ADD | AIV-NNNN — required on every Claude-invoked action | WRITE at creation; blank when no Claude invoked |
| AI_Confidence_Score | Number 0-100 | MISSING — MUST ADD | Required by Article IX of Founder Control Framework | WRITE at creation; blank when not applicable |
| Approval_State | Single Select: AUTONOMOUS / PENDING_HUMAN / HUMAN_APPROVED / HUMAN_REJECTED / VOIDED | MISSING — MUST ADD | AI authority boundary enforcement | WRITE at creation; VOIDED update by Will only |
| Reviewed_By | Text | MISSING — MUST ADD | Human reviewer name for Tier B outputs | WRITE by human reviewers |
| Rollback_Linkage | Text | MISSING — MUST ADD | Record ID and reversal action for undo reference | WRITE at correction time |
| City | Single Select | MISSING — MUST ADD | City-level analytics | WRITE at creation |
| Model_Version | Text | MISSING — MUST ADD | Claude model version (e.g., claude-sonnet-4-6) — required when Claude invoked | WRITE at creation |
| Source_Data | Long Text | MISSING — MUST ADD | Snapshot of input payload — required for rollback reference | WRITE at creation |
| Idempotency_Key | Text | MISSING — MUST ADD | scenario_id + record_id + event_type + date — prevents log flooding | WRITE at creation |

**Note on field count:** Three additional fields from the 25-field target (Created_At, UUID, Updated_At) are Airtable system fields added automatically — not counted as manual additions. The 8 fields listed as MISSING above are the manual additions required before M-AUDIT-LOGGER can write a complete, governance-compliant record.

**Immutability Rules:**
- M-AUDIT-LOGGER's Airtable API token has CREATE permission on Audit Log ONLY — no UPDATE, no DELETE
- The one exception: `Approval_State` may be updated to `VOIDED` by Will only (separate token with restricted UPDATE scope)
- Corrections are new records with `Event_Type = AUDIT_CORRECTION` referencing original `Log_ID`

---

### 2.5 Concierge_Operators (tblX61IB2qjDmac8l)

**Role in Stage 1:** Read-only reference table. M-CONCIERGE-ASSIGNMENT queries this table to select the appropriate operator for each incoming Request based on brand specialization, availability status, and current load.

| Attribute | Value |
|-----------|-------|
| Table ID | tblX61IB2qjDmac8l |
| Phase 3 Status | COMPLETE — migrated from app2FbmVD44BXShyx (3 records: Will, Luciana, Marina) |
| Phase 4 Status | Not needed — schema is sufficient for Stage 1 |
| Make-Readiness | READY |

**Fields for Assignment Logic in M-CONCIERGE-ASSIGNMENT:**

| Field Name | Type | Make Operation | Assignment Logic Role |
|------------|------|---------------|----------------------|
| Name | Text | READ | Display in Slack alert and Audit Log |
| Brand_Specialization | Single Select: SSS / ME / Both | READ | Filter: must match incoming Request.Brand |
| Availability_Status | Single Select: AVAILABLE / UNAVAILABLE / OVERLOADED | READ | Filter: must equal AVAILABLE |
| Current_Load | Number | READ | Sort ascending — assign lowest-load operator |
| Max_Load | Number | READ | Guard: Current_Load must be less than Max_Load |
| Email | Email | READ | Slack DM fallback contact |
| Environment | Single Select | READ | Confirm operator record is Production |
| Brand | Single Select: SSS / ME / Both | READ | Secondary brand filter |
| Legacy_Record_ID | Text | READ | Phase 3 provenance (do not write) |

**Assignment Logic Query:**
```
Filter: Brand_Specialization = [request.brand] OR Brand_Specialization = "Both"
  AND Availability_Status = "AVAILABLE"
  AND Current_Load < Max_Load
Sort: Current_Load ascending
Select: First result
```

**No writes by Make:** M-CONCIERGE-ASSIGNMENT never writes to Concierge_Operators. Current_Load updates are manual — Luciana maintains this field. A Stage 2 enhancement will auto-increment Current_Load via Make when a concierge is assigned.

---

### 2.6 Packages (tblwDw2hkKW5moSr9)

**Role in Stage 1:** M-STRIPE-DEPOSIT reads Package_Price and Deposit_Rate_Pct to calculate the deposit amount. M-BOOKING-CREATION reads Package_Name and links the Package record to the Booking.

| Attribute | Value |
|-----------|-------|
| Table ID | tblwDw2hkKW5moSr9 |
| Current Field Count | 8 |
| Target Field Count (post-Phase-4) | 25 |
| Phase 4 Status | IN PROGRESS — rebuilding from 8 to 25 fields, merging ME_Pricing |
| Make-Readiness | BLOCKED — Deposit_Rate_Pct does not exist in current 8-field schema |

**Current 8 Fields (Read/Write Status for Stage 1):**

| Field Name | Type | Stage 1 Make Use | Note |
|------------|------|-----------------|------|
| Name | Text | READ — Package_Name for Booking record | Exists |
| Notes | Long Text | READ — context only | Exists |
| Assignee | User | Not used by Make | Exists — Airtable scaffold |
| Status | Single Select | READ — confirm Live before quote | Exists |
| Attachments | Attachments | Not used by Make | Exists — Airtable scaffold |
| Attachment Summary | Long Text | Not used by Make | Exists — Airtable scaffold |
| Package_Price | Currency | READ — deposit calculation base | CONFIRM field name matches exactly |
| Deposit_Rate_Pct | Percent | READ — deposit calculation rate | MISSING — must add in Phase 4 |

**17 Fields to Add in Phase 4 (with Stage 1 relevance):**

| Field to Add | Type | Stage 1 Need | Stage 2+ Need |
|--------------|------|-------------|----------------|
| Deposit_Rate_Pct | Percent | CRITICAL BLOCKER — M-STRIPE-DEPOSIT cannot calculate deposit without this | Stage 2 |
| Brand | Single Select: SSS / ME | HIGH — M-BOOKING-CREATION must filter packages by brand | Stage 2 |
| Live | Checkbox | HIGH — Make must not quote inactive packages | Stage 2 |
| City | Single Select | MEDIUM — city-specific package filtering | Stage 2 |
| Min_Guests | Number | MEDIUM — validation in M-BOOKING-CREATION | Stage 2 |
| Max_Guests | Number | MEDIUM — validation in M-BOOKING-CREATION | Stage 2 |
| Margin_Floor_Pct | Percent | LOW (Stage 1) — financial gate | Stage 2 |
| Peak_Multiplier | Number | LOW (Stage 1) | Stage 2 |
| F&B_Cost_Target | Currency | LOW (Stage 1) | Stage 2 |
| Vessel_Cost_Target | Currency | LOW (Stage 1) | Stage 2 |
| Labor_Cost_Target | Currency | LOW (Stage 1) | Stage 2 |
| Total_Internal_Cost | Formula | LOW (Stage 1) | Stage 2 |
| Implied_Margin | Formula | LOW (Stage 1) | Stage 2 |
| Includes_Formatted | Long Text | LOW (Stage 1) — AI context injection | Stage 2 |
| Add_Ons_Matrix | Long Text | LOW (Stage 1) | Stage 2 |
| Bookings_Count | Count | LOW (Stage 1) | Stage 2 |
| Avg_Margin_Achieved | Rollup | LOW (Stage 1) | Stage 2 |

**Stage 1 minimum viable Packages schema:** Name + Package_Price + Deposit_Rate_Pct + Brand + Live + City. These 6 fields are the minimum for Stage 1 to function. The remaining 11 additions support Stage 2 and beyond.

---

### 2.7 Automation_Health (NEW TABLE — TO BE CREATED)

**Role in Stage 1:** Every Stage 1 scenario writes health state to this table via M-AUDIT-LOGGER. The table tracks send states, error counts, and automation status per booking — extracted from the Bookings table as part of Phase 4.

| Attribute | Value |
|-----------|-------|
| Table ID | TBD — table does not yet exist; must be created before Stage 1 build |
| Phase 3 Status | Not applicable |
| Phase 4 Status | PENDING CREATION |
| Make-Readiness | BLOCKED — table does not exist |

**Full Field Specification:**

| Field Name | Type | Purpose | Make Write Permission |
|------------|------|---------|----------------------|
| AH_ID | Formula: RECORD_ID() | Immutable identifier | READ ONLY (auto) |
| Booking_ID | Text | Reference to parent Booking record | WRITE at creation |
| Booking (linked) | Linked Record | Linked record to Bookings table | WRITE at creation |
| Brand | Single Select: SSS / ME | Brand context | WRITE at creation |
| Environment | Single Select: Production / Sandbox | Sandbox isolation | WRITE at creation |
| Scenario_Name | Text | Name of last scenario that executed | WRITE on each execution |
| Scenario_ID | Text | Make numeric scenario ID | WRITE on each execution |
| Last_Execution_At | DateTime | Timestamp of most recent scenario execution | WRITE on each execution |
| Last_Execution_Status | Single Select: SUCCESS / FAILURE / SKIP | Outcome of most recent execution | WRITE on each execution |
| Error_Code | Text | HTTP or Make error code — blank on success | WRITE on failure |
| Error_Message | Long Text | Full error message — blank on success | WRITE on failure |
| Retry_Count | Number | Number of retries attempted on current error | WRITE on each retry |
| Resolution_Status | Single Select: OPEN / RESOLVED / ESCALATED | Human-visible error state | WRITE by M-AUDIT-LOGGER; UPDATE by Luciana |
| Confirmation_Sent | Checkbox | TRUE when booking confirmation email was sent | WRITE by M-BOOKING-CONFIRMATION |
| Stripe_Link_Created | Checkbox | TRUE when Stripe deposit link was generated | WRITE by M-STRIPE-DEPOSIT |
| Slack_Alert_Sent | Checkbox | TRUE when ops Slack alert was sent | WRITE by M-SLACK-ALERTS |
| Concierge_Assigned | Checkbox | TRUE when concierge assignment is complete | WRITE by M-CONCIERGE-ASSIGNMENT |
| Automations_Paused | Checkbox | Mirror of Bookings.Automations_Paused — for health view | WRITE by M-AUDIT-LOGGER |
| Stage_2_D0_Sent | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Stage_2_D1_Sent | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Stage_2_D7_Sent | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Stage_2_D30_Sent | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Stage_2_D72hr_Reminder | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Stage_2_D48hr_Reminder | Checkbox | Future Stage 2 automation tracking | Reserve — do not write in Stage 1 |
| Created_At | DateTime | Record creation — Airtable auto | READ ONLY (auto) |
| Notes | Long Text | Human override notes from Luciana | Human write only |

**Creation Instruction:** Create this table in appdZ49WqgjRXxA1R before any Stage 1 scenario enters sandbox testing. Link it to Bookings via the `Booking` linked record field. Grant Make's production API token CREATE and UPDATE access on this table only (not DELETE). Document the table ID in Section 6 of this registry once created.

---

### 2.8 Emergency_Escalations (tblDbeRf3qO3xvqhK)

**Role in Stage 1:** Stage 1 does not write to this table. It is included here because it is the destination for future EMERGENCY-001 scenario (Stage 2+) and because M-CONCIERGE-ASSIGNMENT must check Emergency_Flag before executing any assignment.

| Attribute | Value |
|-----------|-------|
| Table ID | tblDbeRf3qO3xvqhK |
| Phase 3 Status | COMPLETE — 2 training records (ESC-TRAINING-001, ESC-TRAINING-002) |
| Phase 4 Status | Not needed — schema is adequate |
| Make-Readiness | READY (Stage 2 — not needed in Stage 1) |

**Fields Needed for EMERGENCY-001 (Future — Stage 2+):**

| Field Name | Type | EMERGENCY-001 Role |
|------------|------|-------------------|
| Escalation_ID | Text / Formula | Record identifier |
| Booking (linked) | Linked Record | Links emergency to the booking it affects |
| Escalation_Type | Single Select | MEDICAL / WEATHER / LEGAL / VENDOR / DOUBLE_BOOKING / VIP / MEDIA / HQ_UNAVAILABLE |
| Severity | Single Select: 5-EMERGENCY / 4-CRITICAL / 3-URGENT / 2-HIGH / 1-STANDARD | Notification routing |
| Triggered_By | Single Select: Make / Human | Who initiated the escalation |
| Status | Single Select: OPEN / CONTAINED / RESOLVED | Current state |
| Environment | Single Select | Sandbox isolation |
| Brand | Single Select: SSS / ME | Brand context |
| Legacy_Record_ID | Text | Phase 3 provenance field |
| Created_At | DateTime | Immutable creation timestamp |

**Stage 1 Note:** Stage 1 scenarios read `Emergency_Flag` from the Bookings table as a circuit breaker — they do not read from Emergency_Escalations directly. When `Emergency_Flag = true` on any Booking, all Stage 1 scenarios for that Booking exit immediately and log `CIRCUIT_BREAKER_TRIGGERED` to Audit Log.

---

### 2.9 AI_Prompt_Versions (tbl0FJkA1E6a70cxX — RETIRE; NEW TABLE PENDING)

**Role in Stage 1:** M-BRAND-ROUTER reads the active brand router system prompt from this table. The current 9-field version in the main base is not production-ready. The correct 26-field schema from apppFfA2VZVmamvXe must be installed before M-BRAND-ROUTER can function.

| Attribute | Value |
|-----------|-------|
| Current Table ID | tbl0FJkA1E6a70cxX (9-field version — RETIRE) |
| New Table ID | TBD — create with 26-field schema, confirm ID |
| Source Schema | apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf (26 fields) |
| Phase 4 Status | IN PROGRESS — retire old, install new |
| Make-Readiness | BLOCKED |

**Fields Required for Stage 1 (Make reads only):**

| Field Name | Type | Status | Make Use |
|------------|------|--------|----------|
| Prompt_Version_ID | Formula: AIV-NNNN | EXISTS (in correct schema) | M-AUDIT-LOGGER writes this ID to every Claude-invoked Audit Log record |
| Status | Single Select: DRAFT / TESTING / LIVE / DEPRECATED | EXISTS (in correct schema) | M-BRAND-ROUTER filters: Status = LIVE only |
| Content | Long Text | EXISTS (in correct schema) | M-BRAND-ROUTER injects this as Claude system prompt |
| Make_Variable_Name | Text | MISSING from current 9-field version | M-BRAND-ROUTER uses this to retrieve the correct prompt (e.g., SSS_BRAND_ROUTER_SYSTEM) |
| Will_Approved | Checkbox | MISSING from current 9-field version | Gate: Make must not use any prompt where Will_Approved = false |
| Brand | Single Select: SSS / ME | MISSING from current 9-field version | Filter: only retrieve prompt matching request brand |
| Deployed_At | DateTime | MISSING from current 9-field version | Audit trail |
| Rollback_To_Version | Text | MISSING from current 9-field version | Required before any LIVE deployment |

**All 26 Fields of Correct Schema (for implementation reference):**

`Prompt_Version_ID, Prompt_Name, Version, Status, Content, Brand, Make_Variable_Name, Deployed_By, Deployed_At, Rollback_To_Version, Will_Approved, Performance_Notes, Leads_Processed, Leads_Converted, Conversion_Rate_Pct (formula), Override_Count, AI_Confidence_Score (rollup), Notes, Assignee, Attachments, Attachment_Summary, Environment, Source_System, UUID, Created_At, Updated_At`

---

## SECTION 3 — FIELD ADDITION QUEUE

Priority-ordered list of every field that must be added before Stage 1 goes live. Fields are listed in resolution dependency order — a field that gates another must be resolved first.

| Priority | Table | Field Name | Type | Blocker Level | Stage 1 Scenario Requiring It | Est. Effort |
|----------|-------|------------|------|---------------|-------------------------------|-------------|
| 1 | Bookings | Environment | Single Select: Production / Sandbox / Development | CRITICAL — blocks ALL | All 8 scenarios | 5 min |
| 2 | Requests | Environment | Single Select: Production / Sandbox / Development | CRITICAL — blocks ALL | All 8 scenarios | 5 min |
| 3 | Clients | Environment | Single Select: Production / Sandbox / Development | CRITICAL | M-LEAD-INTAKE, M-BOOKING-CREATION | 5 min |
| 4 | Audit Log | Environment | Single Select: Production / Sandbox / Development | CRITICAL | M-AUDIT-LOGGER | 5 min |
| 5 | Bookings | Idempotency_Key | Text | CRITICAL | M-BOOKING-CREATION | 5 min |
| 6 | Requests | Idempotency_Key | Text | CRITICAL | M-LEAD-INTAKE | 5 min |
| 7 | Packages | Deposit_Rate_Pct | Percent | CRITICAL | M-STRIPE-DEPOSIT | 5 min |
| 8 | Packages | Brand | Single Select: SSS / ME | CRITICAL | M-BOOKING-CREATION | 5 min |
| 9 | Packages | Live | Checkbox | CRITICAL | M-BOOKING-CREATION | 5 min |
| 10 | Audit Log | Log_ID | Formula: RECORD_ID() alias or Text | HIGH | M-AUDIT-LOGGER | 5 min |
| 11 | Audit Log | Source_Scenario_ID | Text | HIGH | M-AUDIT-LOGGER | 5 min |
| 12 | Audit Log | Prompt_Version_ID | Text | HIGH | M-AUDIT-LOGGER (for Claude actions) | 5 min |
| 13 | Audit Log | AI_Confidence_Score | Number 0-100 | HIGH | M-AUDIT-LOGGER | 5 min |
| 14 | Audit Log | Approval_State | Single Select: AUTONOMOUS / PENDING_HUMAN / HUMAN_APPROVED / HUMAN_REJECTED / VOIDED | HIGH | M-AUDIT-LOGGER | 10 min |
| 15 | Audit Log | Model_Version | Text | HIGH | M-AUDIT-LOGGER | 5 min |
| 16 | Audit Log | Source_Data | Long Text | HIGH | M-AUDIT-LOGGER (rollback reference) | 5 min |
| 17 | Audit Log | Idempotency_Key | Text | HIGH | M-AUDIT-LOGGER (dedup guard) | 5 min |
| 18 | Audit Log | City | Single Select | HIGH | M-AUDIT-LOGGER | 5 min |
| 19 | Audit Log | Reviewed_By | Text | MEDIUM | M-AUDIT-LOGGER | 5 min |
| 20 | Audit Log | Rollback_Linkage | Text | MEDIUM | M-AUDIT-LOGGER (correction protocol) | 5 min |
| 21 | Requests | Escalation_Reason | Long Text | HIGH | M-CONCIERGE-ASSIGNMENT | 5 min |
| 22 | Requests | AI_Confidence_Score | Number 0-100 | HIGH | M-BRAND-ROUTER output | 5 min |
| 23 | Requests | Last_Human_Touch | DateTime | MEDIUM | Future INBOUND-002 | 5 min |
| 24 | Clients | UUID | Formula: RECORD_ID() | MEDIUM | M-BOOKING-CREATION (cross-reference) | 5 min |
| 25 | Bookings | D7_Review_Eligible | Formula (see spec below) | LOW (Stage 1) HIGH (Stage 2) | Future CHARTER-006 | 15 min |
| 26 | Bookings | HV_Client | Checkbox | LOW (Stage 1) | Future charter routing | 5 min |
| 27 | — | Automation_Health (entire table) | New table — 25 fields | HIGH | M-AUDIT-LOGGER, M-SLACK-ALERTS failure fallback | 45 min |
| 28 | AI_Prompt_Versions | Full 26-field schema replacement | New table replacing tbl0FJkA1E6a70cxX | HIGH | M-BRAND-ROUTER | 60 min |

**D7_Review_Eligible Formula Specification:**
```
IF(
  AND(
    NOT(OR({Charter_Grade} = "D", {Charter_Grade} = "F")),
    NOT({Emergency_Flag}),
    NOT(OR({Chargeback_Risk} = "HIGH", {Chargeback_Risk} = "ACTIVE")),
    {Status} = "COMPLETED"
  ),
  TRUE(),
  FALSE()
)
```

---

## SECTION 4 — PROTECTED FIELDS

The following fields must never be overwritten by Make under any circumstances. These are enforced at three levels: (1) API token does not have write scope on these fields where Airtable field-level permissions allow, (2) Make scenario build specifications explicitly exclude these fields from all write modules, (3) the Audit Log records any unexpected write attempt as a `PROTECTED_FIELD_VIOLATION` event.

### 4.1 Bookings — Protected Fields

| Field Name | Type | Why Protected | Who May Modify |
|------------|------|--------------|----------------|
| Net_Profit | Formula | Derived — never override; formula recalculates automatically | Formula only |
| Margin_Pct | Formula | Same — formula-derived financial KPI | Formula only |
| Package_Price | Currency | Pricing authority — changes require Founder Decision | Will only |
| Refund_Status | Single Select | Financial state — Make must not change retroactively | Will or Luciana (manual) |
| Refund_Amount | Currency | Financial record — immutable once set | Will only |
| Chargeback_Risk | Single Select | Risk classification — only Will and Luciana | Will or Luciana (manual) |
| Charter_Grade | Single Select | Post-charter quality assessment — human judgment required | Luciana only |
| Charter_NPS | Number | Net Promoter Score — client-submitted | Import process or Luciana |
| Exceptional_Charter | Checkbox | Qualitative flag — human judgment required | Luciana or Will |
| Crew_Report | Long Text | Post-charter crew submission | Crew / Luciana |
| Vendor_Ratings_Entered | Checkbox | Post-charter vendor assessment gate | Luciana only |

### 4.2 Clients — Protected Fields

| Field Name | Type | Why Protected |
|------------|------|--------------|
| CLT_ID | Formula | Immutable client identifier — never regenerated |
| Lifetime_Bookings | Count | Formula-derived — auto-counts linked Bookings |
| Lifetime_Revenue | Rollup | Formula-derived — auto-sums from linked Bookings |
| HV_Client | Checkbox | High-value designation — Luciana sets based on relationship intelligence; Make may not override |

### 4.3 Audit Log — Protected Fields

| Field Name | Type | Why Protected |
|------------|------|--------------|
| All existing records | All fields | Audit Log is append-only. Make has CREATE permission only. No UPDATE or DELETE on existing records. |
| Approval_State | Single Select | The one updatable field — VOIDED state may only be set by Will via a separate restricted token |

### 4.4 AI_Prompt_Versions — Protected Fields

| Field Name | Type | Why Protected |
|------------|------|--------------|
| Content | Long Text | Prompt verbatim — read-only once Status = LIVE. Changes require new version record, not overwrite. |
| Will_Approved | Checkbox | Gate field — only Will sets this to true. Make reads it but may never write it. |
| Deployed_At | DateTime | Immutable deployment timestamp |
| Rollback_To_Version | Text | Rollback reference — set at deployment; never changed after |

### 4.5 Universal Protected Fields (All Tables)

| Field Name | Type | Why Protected |
|------------|------|--------------|
| UUID / RECORD_ID() | Formula | Auto-generated by Airtable; immutable system identifier |
| Created_At / Created Time | DateTime | Immutable creation timestamp — Airtable system field |
| Legacy_Record_ID | Text | Phase 3 migration provenance — historical reference only |

---

## SECTION 5 — AIRTABLE API TOKEN SCOPE

Stage 1 requires two separate Airtable API tokens with distinct permission scopes. Combining permissions into a single token violates the principle of least privilege and creates risk of Make overwriting protected fields.

### 5.1 Token 1 — SSS-Production-Make-RW (Read-Write Token)

Used by: M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, M-SLACK-ALERTS, M-BRAND-ROUTER, M-HEALTH-MONITOR (Stage 2)

| Scope | Permission | Tables |
|-------|------------|--------|
| data.records:read | READ | Requests, Bookings, Clients, Packages, Concierge_Operators, AI_Prompt_Versions, Automation_Health |
| data.records:write | WRITE (CREATE + UPDATE) | Requests, Bookings, Clients, Automation_Health |
| data.records:write | WRITE (CREATE only) | Clients (no update — dedup prevents overwrite) |

**Explicit exclusions from this token:**
- No DELETE permission on any table
- No write access to: Audit Log, AI_Prompt_Versions, Emergency_Escalations, Protected fields listed in Section 4

### 5.2 Token 2 — SSS-AuditLog-Append (Append-Only Token)

Used by: M-AUDIT-LOGGER exclusively

| Scope | Permission | Tables |
|-------|------------|--------|
| data.records:write | CREATE ONLY | Audit Log (tblrMpTfMk8q1eNHp) |

**Explicit exclusions from this token:**
- No READ permission (M-AUDIT-LOGGER does not query before writing)
- No UPDATE permission (append-only is non-negotiable)
- No DELETE permission
- No access to any table other than Audit Log

### 5.3 Sandbox Token (Stage 1 Testing)

| Scope | Permission | Base |
|-------|------------|------|
| data.records:read | READ | Sandbox base only |
| data.records:write | CREATE + UPDATE | Sandbox base only |

Production base tokens must never be used during sandbox testing. The sandbox base must be a separate Airtable base — not the production base appdZ49WqgjRXxA1R with a filter.

### 5.4 Token Rotation and Storage

| Requirement | Detail |
|-------------|--------|
| Storage | Make Data Store only — never embedded in scenario module configuration as plain text |
| Key naming convention | `PRODUCTION_AIRTABLE_TOKEN_RW`, `PRODUCTION_AIRTABLE_TOKEN_AUDIT`, `SANDBOX_AIRTABLE_TOKEN_RW` |
| Rotation cadence | Quarterly minimum; immediately on any personnel change with access |
| Rotation protocol | Founder Decision record created; old token revoked in Airtable; new token stored in Make Data Store; all scenarios tested with new token in sandbox before production confirmation |

---

## SECTION 6 — KNOWN GAPS AND UNKNOWNS

The following items must be confirmed or resolved before the affected scenarios enter sandbox testing. Each is a hard dependency — building without confirming these items will produce scenarios that fail in unexpected ways.

### 6.1 Table IDs Not Yet Confirmed

| Table | Situation | Action Required | Blocks |
|-------|-----------|----------------|--------|
| Automation_Health | Table does not exist — must be created | Create table per Section 2.7 spec; document table ID here upon creation | M-AUDIT-LOGGER, M-SLACK-ALERTS failure fallback |
| AI_Prompt_Versions (correct schema) | Must replace tbl0FJkA1E6a70cxX with 26-field version | Execute Phase 4 AI_Prompt_Versions replacement; document new table ID | M-BRAND-ROUTER |
| SSS Sandbox Base | Must be a dedicated base separate from production | Create new base; document base ID in Make Data Store as SANDBOX_AIRTABLE_BASE_ID | ALL sandbox testing |

### 6.2 Field IDs Not Yet Retrieved

Make references fields by field ID (format: `fldXXXXXXXXXXXXXX`), not by field name. The following tables require full `get_table_schema` retrieval before Make module field mapping can be completed:

| Table | Table ID | Fields Requiring ID Retrieval | Blocks |
|-------|----------|------------------------------|--------|
| Bookings | tbl72omPibBkn2hZL | All Category A write-safe fields (see Section 2.2); Emergency_Flag; Automations_Paused | M-BOOKING-CREATION, M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| Requests | tblTlSB9CO4dTGodg | Status, Agent_Status, Brand, Concierge_Assigned, Idempotency_Key, all new fields to be added | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT |
| Clients | tblr84vRIWC5HmKvo | Email, Name, Phone, CLT_ID, HV_Client | M-LEAD-INTAKE, M-BOOKING-CREATION |
| Audit Log | tblrMpTfMk8q1eNHp | All 25 fields post-expansion | M-AUDIT-LOGGER |
| Concierge_Operators | tblX61IB2qjDmac8l | Brand_Specialization, Availability_Status, Current_Load, Max_Load | M-CONCIERGE-ASSIGNMENT |
| Packages | tblwDw2hkKW5moSr9 | Package_Price, Deposit_Rate_Pct (once added), Brand (once added), Live (once added) | M-STRIPE-DEPOSIT, M-BOOKING-CREATION |

### 6.3 Make Scenario IDs Not Yet Assigned

Make scenario IDs (numeric format, e.g., 4829371) are assigned by Make upon scenario creation. The following scenarios have no IDs because they have not yet been built. These IDs are required in the Audit Log `Source_Scenario_ID` field and in the Make_Scenarios registry table (tbl08IpivapVQZUto).

| Scenario | Current ID | Required By |
|----------|-----------|-------------|
| M-BRAND-ROUTER | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-LEAD-INTAKE | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-SLACK-ALERTS | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-CONCIERGE-ASSIGNMENT | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-STRIPE-DEPOSIT | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-BOOKING-CREATION | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-BOOKING-CONFIRMATION | PENDING-REGISTRATION | M-AUDIT-LOGGER; Make_Scenarios registry |
| M-AUDIT-LOGGER | PENDING-REGISTRATION | Make_Scenarios registry |

**Resolution:** Will exports scenario IDs from Make dashboard after each scenario is created. IDs are entered into the Make_Scenarios table (tbl08IpivapVQZUto) and documented in MAKE_SCENARIO_REGISTRY.md within 24 hours of creation.

### 6.4 Native Airtable Automations Inventory — CRITICAL UNKNOWN

No audit of existing native Airtable automations in appdZ49WqgjRXxA1R has been completed. This is BLK-009 in the Stage 1 Blocker Resolution Report. Until this inventory is complete, M-BOOKING-CREATION cannot safely write to the Bookings table.

| Action Required | Owner | Deadline |
|----------------|-------|---------|
| Open Airtable base appdZ49WqgjRXxA1R → Automations tab | Will | Before M-BOOKING-CREATION build begins |
| Document every native automation: trigger table, trigger field, action type, destination | Will | Before M-BOOKING-CREATION build begins |
| Identify any automation with "record updated" trigger on Bookings — these create circular execution risk | Will | Before M-BOOKING-CREATION build begins |
| Scope any such automation to specific field triggers only, not generic record update | Will | Before M-BOOKING-CREATION build begins |
| Document findings as an addendum to this registry | Will | Before sandbox testing of M-BOOKING-CREATION |

### 6.5 Stripe Webhook Configuration — Undocumented

Stripe webhook endpoints and signing secrets are not documented in any governance file. The following must be confirmed before M-STRIPE-DEPOSIT can be built:

| Item | Status | Action |
|------|--------|--------|
| Webhook endpoint URL (Make) | UNKNOWN | Will audits Stripe Developer → Webhooks |
| Signing secret (for HMAC validation) | UNKNOWN — stored where? | Will confirms storage location; move to Make Data Store if not there |
| Webhook events subscribed | UNKNOWN | Must include: `payment_intent.succeeded`, `payment_link.completed` |
| Last rotation date of signing secret | UNKNOWN | Document; schedule quarterly rotation |

### 6.6 Packages Table — ME_Pricing Merge Not Yet Complete

ME_Pricing (5 records from app2FbmVD44BXShyx) has not been merged into the Packages table. Until this merge is complete, Mare Executive packages do not exist in the Packages table. M-BOOKING-CREATION for ME brand requests will find no matching Package record and will fail.

| Action | Owner | Blocks |
|--------|-------|--------|
| Execute Phase 4 Packages table rebuild (add 17 fields) | Will | M-STRIPE-DEPOSIT, M-BOOKING-CREATION for ME brand |
| Extract ME_Pricing 5 records and migrate to expanded Packages table | Will | All ME brand bookings |
| Retire app2FbmVD44BXShyx after ME_Pricing migration confirmed | Will | Phase 5 base retirement |

### 6.7 Webflow Form Field Mapping — Unconfirmed

M-LEAD-INTAKE maps Webflow form submission payload fields to Airtable Requests fields. The exact payload keys from Webflow (field slugs) have not been documented and may not match the Airtable field names directly.

| Action | Owner |
|--------|-------|
| Export Webflow form field slugs for SSS and ME contact forms | Luciana |
| Confirm mapping: Webflow slug → M-LEAD-INTAKE payload key → Airtable field name | Systems / Make builder |
| Confirm `brand_hint` field exists on both forms (required by M-BRAND-ROUTER) | Luciana |
| Document mapping in AIRTABLE_FIELD_MAPPING_REGISTRY.md | Make builder |

### 6.8 Unresolved Architecture Decisions Affecting Schema

| Decision | Options | Impact on This Registry | Owner |
|----------|---------|------------------------|-------|
| SSS and ME packages in same Packages table or separate tables | Single table with Brand field (current plan) vs. separate tables | Affects M-BOOKING-CREATION filter logic and Packages field design in Section 2.6 | Will |
| Sandbox base — create new or repurpose retired base | Create fresh (recommended) vs. repurpose app2FbmVD44BXShyx post-migration | Fresh creation required for clean token separation | Will |
| State Transition Log — keep separate from Audit Log | Keep separate (current, recommended) vs. merge | If merged, Audit Log table ID changes — all Make references update | Will |
| Automation_Health — standalone table or fields on Bookings | Standalone (current plan per Phase 4) vs. fields on Bookings | Phase 4 plan is standalone; changing this would remove the need to create the table in Section 2.7 | Will |

---

## APPENDIX — QUICK REFERENCE: STAGE 1 TABLE-SCENARIO MATRIX

| Scenario | Reads From | Writes To |
|----------|-----------|-----------|
| M-BRAND-ROUTER | AI_Prompt_Versions | — (returns variables to M-LEAD-INTAKE) |
| M-LEAD-INTAKE | Requests (dedup), Clients (dedup) | Requests (CREATE), Clients (conditional CREATE) |
| M-SLACK-ALERTS | — (stateless — uses passed payload) | Automation_Health (failure state) |
| M-CONCIERGE-ASSIGNMENT | Requests, Concierge_Operators | Requests (UPDATE: Concierge_Assigned, Agent_Status) |
| M-STRIPE-DEPOSIT | Bookings, Packages | Bookings (UPDATE: Stripe_Link, Stripe_Payment_Intent_ID, Deposit_Amount), Requests (UPDATE: Stripe_Link reference) |
| M-BOOKING-CREATION | Requests, Clients, Packages, Bookings (dedup) | Bookings (CREATE), Requests (UPDATE: Status, Linked_Booking_ID) |
| M-BOOKING-CONFIRMATION | Bookings, Clients | Bookings (UPDATE: Confirmation_Sent, Confirmation_Sent_At, Confirmation_Channel) |
| M-AUDIT-LOGGER | — (write-only) | Audit Log (CREATE only) |

---

*SHE SAID SAIL + MARE EXECUTIVE*  
*CONFIDENTIAL — INTERNAL USE ONLY*  
*POST_PHASE_4_SCHEMA_REGISTRY v1.0*  
*Effective May 2026*  
*Owner: Will (Founder)*  
*Source Authority: 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED*  
*Phase 3 Reference: PHASE_3_FRAGMENTED_BASE_MIGRATION_REPORT.md*  
*Phase 4 Reference: 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md*  
*Make Architecture Reference: STAGE_1_MAKE_IMPLEMENTATION/MAKE_MASTER_ARCHITECTURE.md*
