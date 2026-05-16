# FINAL_PRODUCTION_AIRTABLE_ARCHITECTURE

**Status:** PRODUCTION REFERENCE
**Version:** 1.0 — Post-Phase-4 Consolidated Architecture
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** SSS Operations Base + SSS Financials Base — Stage 1 Make Scenario Access Only
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Scope of This Document:** This document describes only the Airtable tables, fields, and access patterns relevant to the eight Stage 1 Make scenarios (M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, M-AUDIT-LOGGER) and the two infrastructure scenarios (M-HEALTH-001, M-HEALTH-FAILSAFE). Tables not accessed by Stage 1 are omitted from this document. The full schema specification for all tables is documented in `02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md`.

---

## 1. PRODUCTION BASE INVENTORY

| Base | Base ID | Role | Make Access |
|------|---------|------|-------------|
| SSS Operations | `appdZ49WqgjRXxA1R` | All core ops, intelligence, governance tables | Primary read/write base for all Stage 1 scenarios |
| SSS Financials | `apprDKQtV2GInThwE` | Financial intelligence, investor reporting, payouts | Write-only for M-AUDIT-LOGGER cross-base sync |

**Base Access Authentication:**

| Base | Auth Method | Token Type | Scope |
|------|------------|-----------|-------|
| SSS Operations | Personal Access Token | Scoped — defined field writes only | See Section 8 |
| SSS Financials | Personal Access Token (separate token) | Scoped — write-only on P&L Per Charter | See Section 9 |

**Two separate tokens are required.** A single token with access to both bases violates the principle of minimal privilege. The SSS Financials token is write-only from Make — no scenario reads financial data except for reconciliation checks in M-AUDIT-LOGGER.

---

## 2. UNIVERSAL REQUIRED FIELDS — ALL STAGE 1 TABLES

Every table accessed by Stage 1 Make scenarios must carry these fields. No exceptions. Make will not process a record that is missing any of these fields correctly.

| Field Name | Airtable Type | Formula / Value | Purpose | Make Access |
|-----------|---------------|----------------|---------|-------------|
| `UUID` | Formula | `RECORD_ID()` | Permanent immutable identifier — referenced by Make as the unique key for all cross-table operations | Read only |
| `Environment` | Single Select | Production / Sandbox / Development | Make reads this as Step 1 gate — exits if not Production in production scenarios | Read only |
| `Brand` | Single Select | SSS / ME | Brand context — required for M-BRAND-ROUTER output, all audit entries, all Slack alerts | Read / Write |
| `Source_System` | Single Select | Stripe / Airtable / Make / Manual / API | Documents which system created or last modified the record | Write (Make sets to `Make` on all its writes) |
| `Created_At` | Created Time (Airtable native) or DateTime formula | Auto-populated by Airtable | Immutable creation timestamp | Read only |

---

## 3. TABLE-BY-TABLE REFERENCE — SSS OPERATIONS BASE

### 3.1 Requests Table

| Attribute | Value |
|-----------|-------|
| Table Name | Requests |
| Table ID | `tblTlSB9CO4dTGodg` |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Inbound lead intake, brand routing, concierge assignment, pre-booking qualification. Every client inquiry becomes one Requests record. |
| Make Access Pattern | Read-Write |
| Circular Trigger Risk | YES — Airtable automation on Requests may re-trigger Make on status field change. Mitigation: all Airtable-native automations on Requests must be scoped to specific field changes only; never `record updated` generic trigger. |

**Key Fields Used by Stage 1:**

| Field Name | Type | Read By | Written By | Notes |
|-----------|------|---------|-----------|-------|
| `UUID` | Formula: RECORD_ID() | All scenarios | System | Primary key for cross-table reference |
| `Environment` | Single Select | M-LEAD-INTAKE (gate check) | M-LEAD-INTAKE | Set to `Production` on creation |
| `Brand` | Single Select | M-BRAND-ROUTER | M-BRAND-ROUTER | Set to SSS or ME after classification |
| `Brand_Routed` | Single Select: SSS / ME | M-CONCIERGE-ASSIGNMENT | M-BRAND-ROUTER | Confirms routing completed |
| `Agent_Status` | Single Select | M-CONCIERGE-ASSIGNMENT | M-CONCIERGE-ASSIGNMENT | AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED |
| `Idempotency_Key` | Single Line Text | M-LEAD-INTAKE (dedup check) | M-LEAD-INTAKE | Checked before record creation to prevent duplicates |
| `Source_Form` | Single Line Text | — | M-LEAD-INTAKE | Webflow form ID or form name |
| `Client_Name` | Single Line Text | M-CONCIERGE-ASSIGNMENT | M-LEAD-INTAKE | From form submission |
| `Client_Email` | Email | M-BOOKING-CREATION | M-LEAD-INTAKE | PII — restricted field access |
| `Client_Phone` | Phone Number | M-BOOKING-CREATION | M-LEAD-INTAKE | PII — restricted field access |
| `Requested_Date` | Date | M-CONCIERGE-ASSIGNMENT | M-LEAD-INTAKE | Charter date requested |
| `Group_Size` | Number | M-CONCIERGE-ASSIGNMENT | M-LEAD-INTAKE | Guest count |
| `Package_Interest` | Single Select | M-CONCIERGE-ASSIGNMENT | M-LEAD-INTAKE | Package name from form |
| `Automations_Paused` | Checkbox | All outbound scenarios | M-CONCIERGE-ASSIGNMENT | Safety gate — if true, no outbound messages |
| `Concierge_Assigned` | Linked Record → Brokers | M-BOOKING-CREATION | M-CONCIERGE-ASSIGNMENT | Broker record linked on assignment |
| `Escalation_Reason` | Long Text | — | M-CONCIERGE-ASSIGNMENT | Populated when routing to HUMAN_REVIEW |
| `AI_Confidence_Score` | Number (0–100) | — | M-CONCIERGE-ASSIGNMENT | From Claude classification |
| `Last_AI_Action` | DateTime | — | M-CONCIERGE-ASSIGNMENT | Timestamp of last autonomous action |
| `Last_Human_Touch` | DateTime | — | Manual / M-CONCIERGE-ASSIGNMENT | Set by Luciana on manual intervention |
| `Source_System` | Single Select | — | M-LEAD-INTAKE | Set to `Make` |
| `Brand` | Single Select | M-BRAND-ROUTER | M-BRAND-ROUTER | SSS or ME |

**Circular Trigger Mitigation for Requests:**
- No Airtable-native automation may watch `record updated` on Requests generically
- Any Airtable automation on Requests must specify field: `Agent_Status changed` or `Brand_Routed changed`
- M-BRAND-ROUTER and M-CONCIERGE-ASSIGNMENT must include a loop-break guard: if the scenario has already written `Brand_Routed` in this execution cycle, it does not re-trigger

---

### 3.2 Bookings Table

| Attribute | Value |
|-----------|-------|
| Table Name | Bookings |
| Table ID | `tbl72omPibBkn2hZL` |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Master operational record for every confirmed charter. Lifecycle state machine from AVAILABILITY_PENDING through COMPLETED or CANCELLED. |
| Make Access Pattern | Read-Write |
| Circular Trigger Risk | HIGH — Bookings has 129 fields (post-migration: 70). Any field update on a Bookings record triggers all Airtable-native automations watching this table. Mitigation: mandatory field-specific trigger scoping on all Airtable automations; M-BOOKING-CREATION writes all required fields in a single API call to minimize trigger events. |

**Key Fields Used by Stage 1:**

| Field Name | Type | Read By | Written By | Notes |
|-----------|------|---------|-----------|-------|
| `UUID` | Formula: RECORD_ID() | All scenarios | System | Primary key |
| `Environment` | Single Select | All scenarios (gate) | M-BOOKING-CREATION | Must be Production before any scenario acts |
| `Brand` | Single Select | All scenarios | M-BOOKING-CREATION | SSS or ME — from linked Request |
| `Status` | Single Select | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION, HEALTH-001 | M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION | Full lifecycle: NEW → AVAILABILITY_PENDING → AVAILABILITY_CONFIRMED → DEPOSIT_SENT → DEPOSIT_PAID → AGREEMENT_PENDING → CONFIRMED → BALANCE_DUE → PAID → COMPLETED → CANCELLED / VOID |
| `Emergency_Flag` | Checkbox | M-SLACK-ALERTS, HEALTH-001, all outbound | M-SLACK-ALERTS (on detection) | If true: all outbound paused; SEV-1 fired immediately |
| `Automations_Paused` | Checkbox | All outbound scenarios (Step 1 gate) | M-SLACK-ALERTS | If true: scenario exits before any client-facing action |
| `HV_Client` | Checkbox | M-CONCIERGE-ASSIGNMENT | M-BOOKING-CREATION (copied from Request) | High-value client — affects concierge routing |
| `Idempotency_Key` | Single Line Text | M-BOOKING-CREATION (dedup check) | M-BOOKING-CREATION | Checked before record creation |
| `Stripe_Payment_Intent_ID` | Single Line Text | — | M-STRIPE-DEPOSIT | Populated on deposit link creation |
| `Stripe_Deposit_Link` | URL | — | M-STRIPE-DEPOSIT | Payment link sent to client |
| `Deposit_Amount` | Currency | — | M-STRIPE-DEPOSIT | From Stripe payment intent |
| `Deposit_Paid_At` | DateTime | — | M-STRIPE-DEPOSIT (on webhook receipt) | Timestamp of confirmed payment |
| `Concierge_Assigned` | Linked Record → Brokers | M-STRIPE-DEPOSIT | M-CONCIERGE-ASSIGNMENT | Broker handling this booking |
| `D7_Review_Eligible` | Formula | M-BOOKING-CONFIRMATION | System (formula) | TRUE when all review eligibility conditions met — Make reads, never writes |
| `Confirmation_Sent_At` | DateTime | M-BOOKING-CONFIRMATION (idempotency) | M-BOOKING-CONFIRMATION | Prevents duplicate confirmation sends |
| `Source_System` | Single Select | — | M-BOOKING-CREATION | Set to `Make` |
| `Request_ID` | Linked Record → Requests | M-BOOKING-CREATION | M-BOOKING-CREATION | Links Booking to originating Request |
| `Client_ID` | Linked Record → Clients | M-BOOKING-CREATION | M-BOOKING-CREATION | Links Booking to Client record |

**Circular Trigger Mitigation for Bookings:**
- All Airtable-native automations on Bookings must specify exact field changes, never generic record updates
- M-STRIPE-DEPOSIT writes `Status`, `Stripe_Payment_Intent_ID`, `Deposit_Paid_At` in a single update call
- M-BOOKING-CREATION writes all new-booking fields in a single create call
- Make modules include a guard: check if `Idempotency_Key` is already set before any write operation

---

### 3.3 Clients Table

| Attribute | Value |
|-----------|-------|
| Table Name | Clients |
| Table ID | `tblr84vRIWC5HmKvo` |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Client identity, PII storage, charter history, preference intelligence. |
| Make Access Pattern | Read-Write (M-LEAD-INTAKE creates; M-BOOKING-CREATION links) |
| Circular Trigger Risk | LOW — Clients table has minimal Airtable automations. M-LEAD-INTAKE creates a Client record only if no existing record matches the email. |

**Key Fields Used by Stage 1:**

| Field Name | Type | Read By | Written By | Notes |
|-----------|------|---------|-----------|-------|
| `UUID` | Formula: RECORD_ID() | M-BOOKING-CREATION | System | Used to link Booking to Client |
| `Name` | Single Line Text | M-BOOKING-CONFIRMATION | M-LEAD-INTAKE | Full client name |
| `Email` | Email | M-LEAD-INTAKE (dedup check) | M-LEAD-INTAKE | Checked for existing client before creation |
| `Phone` | Phone Number | — | M-LEAD-INTAKE | PII |
| `Brand` | Single Select | — | M-LEAD-INTAKE | SSS or ME — from Brand Router |
| `Environment` | Single Select | M-LEAD-INTAKE | M-LEAD-INTAKE | Production |
| `HV_Client` | Checkbox | M-CONCIERGE-ASSIGNMENT | Manual / Will only | High-value designation |
| `Charter_History_Count` | Rollup from Bookings | M-CONCIERGE-ASSIGNMENT | System (rollup) | Number of past confirmed bookings |
| `Source_System` | Single Select | — | M-LEAD-INTAKE | Set to `Make` |

**Dedup Logic for Client Creation:**
```
Step 1: Search Clients WHERE Email = webflow_form_email
Step 2: IF existing client found → use existing record ID → do not create duplicate
Step 3: IF no match → create new Client record → capture new record ID
Step 4: Link Client record to Request record
```

---

### 3.4 Brokers Table

| Attribute | Value |
|-----------|-------|
| Table Name | Brokers |
| Table ID | `tblUrAVcx4HMdWVsN` |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Concierge / broker directory with availability, performance scores, and city assignments. |
| Make Access Pattern | Read-only for Stage 1 (M-CONCIERGE-ASSIGNMENT reads to find available broker; write access not needed at Stage 1) |
| Circular Trigger Risk | NONE — Stage 1 does not write to Brokers |

**Key Fields Used by Stage 1:**

| Field Name | Type | Read By | Notes |
|-----------|------|---------|-------|
| `UUID` | Formula: RECORD_ID() | M-CONCIERGE-ASSIGNMENT | Used to link to Requests and Bookings |
| `Name` | Single Line Text | M-CONCIERGE-ASSIGNMENT | Broker full name |
| `Is_Available` | Checkbox | M-CONCIERGE-ASSIGNMENT | Only assign if true |
| `Brand_Specialization` | Multiple Select: SSS / ME | M-CONCIERGE-ASSIGNMENT | Match brand of request |
| `City` | Single Select | M-CONCIERGE-ASSIGNMENT | Match city of request |
| `Current_Active_Requests` | Count | M-CONCIERGE-ASSIGNMENT | Load balancing — prefer broker with fewest active |
| `Is_Senior` | Checkbox | M-CONCIERGE-ASSIGNMENT | HV_Client requests require senior broker |

---

### 3.5 Audit Log Table

| Attribute | Value |
|-----------|-------|
| Table Name | Audit Log |
| Table ID | `tblrMpTfMk8q1eNHp` |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Immutable, append-only record of every Tier A autonomous action. Every Make scenario writes here through M-AUDIT-LOGGER before the action is considered complete. |
| Make Access Pattern | Write-only (append only — no updates to existing records ever) |
| Circular Trigger Risk | LOW — Audit Log has no outbound Airtable automations. No scenario triggers on Audit Log record creation. |

**Key Fields Used by Stage 1:**

| Field Name | Type | Written By | Notes |
|-----------|------|-----------|-------|
| `Audit_ID` | Formula: AUD-YYYY-NNNN | System (formula from counter) | Immutable human-readable ID |
| `Scenario_ID` | Single Line Text | M-AUDIT-LOGGER | e.g., `M-LEAD-INTAKE` |
| `Action_Type` | Single Line Text | M-AUDIT-LOGGER | e.g., `RECORD_CREATED`, `STATUS_UPDATED`, `MESSAGE_SENT` |
| `Record_ID_Affected` | Single Line Text | M-AUDIT-LOGGER | Airtable UUID of affected record |
| `Table_Affected` | Single Line Text | M-AUDIT-LOGGER | e.g., `Requests`, `Bookings` |
| `Idempotency_Key` | Single Line Text | M-AUDIT-LOGGER | Key used by the originating scenario |
| `Execution_Timestamp` | DateTime | M-AUDIT-LOGGER | When the action executed — immutable after write |
| `Approval_State` | Single Select | M-AUDIT-LOGGER | AUTONOMOUS / PENDING_HUMAN / HUMAN_APPROVED |
| `Brand` | Single Select | M-AUDIT-LOGGER | SSS or ME |
| `Environment` | Single Select | M-AUDIT-LOGGER | Production |
| `Prompt_Version` | Single Line Text | M-AUDIT-LOGGER | AIV-NNNN — required when action involves Claude |
| `Rollback_Linkage` | Single Line Text | M-AUDIT-LOGGER | Record ID and action that would undo this — required before action is complete |
| `Source_System` | Single Select | M-AUDIT-LOGGER | Always `Make` |
| `City` | Single Select | M-AUDIT-LOGGER | City context of the action |

**Immutability Controls:**
- Audit Log records are never updated after creation — only new records are appended
- Make API token has append-only (create) permission on Audit Log — no update or delete
- No human edit permitted on `Execution_Timestamp`, `Scenario_ID`, `Idempotency_Key`, or `Action_Type`
- Airtable field permissions lock these fields to read-only for all roles except the Make API token (create only)

---

### 3.6 Automation_Health Table

| Attribute | Value |
|-----------|-------|
| Table Name | Automation_Health |
| Table ID | NEW TABLE — create per Airtable Final Build Spec |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Tracks execution state for each scenario, replaces 20+ send-state fields formerly on Bookings. Written by every Stage 1 scenario and read by HEALTH-001. |
| Make Access Pattern | Read-Write |
| Circular Trigger Risk | NONE — No Airtable-native automations watch this table. HEALTH-001 writes here but does not trigger on changes here. |

**Full Field Specification:**

| Field Name | Type | Written By | Read By | Notes |
|-----------|------|-----------|---------|-------|
| `UUID` | Formula: RECORD_ID() | System | HEALTH-001 | Primary key |
| `Scenario_ID` | Single Line Text | Each scenario | HEALTH-001 | e.g., `M-LEAD-INTAKE` |
| `Booking_ID` | Linked Record → Bookings | Each scenario | HEALTH-001 | Links health record to booking context |
| `Environment` | Single Select | Each scenario | HEALTH-001 | Production / Sandbox |
| `Brand` | Single Select | Each scenario | HEALTH-001 | SSS / ME |
| `Last_Execution_Timestamp` | DateTime | Each scenario | HEALTH-001 | Gap detection source |
| `Last_Success_Timestamp` | DateTime | Each scenario | HEALTH-001 | Distinguishes failure from slow execution |
| `Execution_Status` | Single Select | Each scenario | HEALTH-001 | SUCCESS / FAILURE / RETRY / SKIPPED |
| `Failure_Count_Total` | Number | Each scenario (increment on failure) | HEALTH-001 | Running total |
| `Failure_Count_1hr` | Number | HEALTH-001 | HEALTH-001 | Recalculated every 15 min |
| `Last_Error_Code` | Single Line Text | Each scenario | HEALTH-001 | SCENARIO-CODE-TIMESTAMP format |
| `Last_Error_Message` | Long Text | Each scenario | HEALTH-001 | Full error payload from Make |
| `Idempotency_Key_Used` | Single Line Text | Each scenario | — | Audit trail for dedup |
| `Audit_Log_Ref` | Single Line Text | M-AUDIT-LOGGER | HEALTH-001 | AUD-YYYY-NNNN — gap detection |
| `Stripe_Last_Webhook_Received` | DateTime | M-STRIPE-DEPOSIT | HEALTH-001 | Latency tracking |
| `Stripe_Last_Processed` | DateTime | M-STRIPE-DEPOSIT | HEALTH-001 | Latency calculation |
| `Airtable_API_Calls_1hr` | Number | HEALTH-001 | HEALTH-001 | Recalculated each run |
| `Airtable_API_Errors_1hr` | Number | HEALTH-001 | HEALTH-001 | Recalculated each run |
| `Backup_Last_Successful_Run` | DateTime | M-BACKUP-DAILY | HEALTH-001 | Age check source |
| `Health_Check_Result` | Single Select | HEALTH-001 | Ops Portal | OK / WARNING / CRITICAL |
| `Health_Check_Timestamp` | DateTime | HEALTH-001 | Ops Portal | When HEALTH-001 last ran |
| `Alert_Sent` | Checkbox | HEALTH-001 | HEALTH-001 | Prevents duplicate alerts within same check window |
| `Alert_Severity` | Single Select | HEALTH-001 | Ops Portal | SEV-1 / SEV-2 / SEV-3 / SEV-4 |
| `Source_System` | Single Select | System | — | Always `Make` |
| `Created_At` | Created Time | System | — | Record creation timestamp |

---

### 3.7 Automation_Failures Table

| Attribute | Value |
|-----------|-------|
| Table Name | Automation_Failures |
| Table ID | Existing or create per spec |
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Table Purpose | Log of every Make scenario failure. Written by each scenario's error handler. Read by HEALTH-001 for failure count metrics. |
| Make Access Pattern | Write (error handlers) / Read (HEALTH-001) |
| Circular Trigger Risk | NONE |

**Key Fields Used by Stage 1:**

| Field Name | Type | Written By | Read By | Notes |
|-----------|------|-----------|---------|-------|
| `UUID` | Formula: RECORD_ID() | System | HEALTH-001 | |
| `Scenario_ID` | Single Line Text | Error handler | HEALTH-001 | |
| `Error_Code` | Single Line Text | Error handler | HEALTH-001 | Format: SCENARIO-CODE-TIMESTAMP |
| `Error_Message` | Long Text | Error handler | — | Full Make error details |
| `Retry_Count` | Number | Error handler | HEALTH-001 | Incremented on each retry |
| `Environment` | Single Select | Error handler | HEALTH-001 | |
| `Brand` | Single Select | Error handler | HEALTH-001 | |
| `Created_At` | Created Time | System | HEALTH-001 | Used for 1-hour window calculation |
| `Resolved` | Checkbox | Manual / Make on recovery | — | Set to true when failure resolved |
| `Resolution_Notes` | Long Text | Manual | — | How it was resolved |

---

## 4. TABLE-BY-TABLE REFERENCE — SSS FINANCIALS BASE

### 4.1 P&L Per Charter Table

| Attribute | Value |
|-----------|-------|
| Table Name | P&L Per Charter |
| Table ID | `tblFLiODVbQENbL5U` |
| Base | SSS Financials (`apprDKQtV2GInThwE`) |
| Table Purpose | Financial performance record per completed charter. Written by M-AUDIT-LOGGER as part of cross-base sync when Booking status = COMPLETED. |
| Make Access Pattern | Write-only from Stage 1 (M-AUDIT-LOGGER bridges ops and financials) |
| Circular Trigger Risk | LOW — Financials base has minimal Airtable automations. No Make scenario reads this table in Stage 1. |

**Key Fields Used by Stage 1 (Write Only):**

| Field Name | Type | Written By | Notes |
|-----------|------|-----------|-------|
| `Booking_ID` | Single Line Text | M-AUDIT-LOGGER | Cross-base reference — not a linked record (cross-base limitation). Value is the human-readable BK-YYYY-NNNN ID. |
| `Brand` | Single Select | M-AUDIT-LOGGER | SSS or ME |
| `Environment` | Single Select | M-AUDIT-LOGGER | Production |
| `Last_Sync_Timestamp` | DateTime | M-AUDIT-LOGGER | When the sync write occurred |
| `Sync_Status` | Single Select | M-AUDIT-LOGGER | SYNCED / PARTIAL / FAILED — HEALTH-001 monitors COMPLETED bookings for missing SYNCED status |
| `Source_System` | Single Select | M-AUDIT-LOGGER | `Make` |

**Cross-Base Write Constraint:**
Airtable does not support linked records across bases. The `Booking_ID` field in P&L Per Charter is a `Single Line Text` field containing the human-readable booking ID. M-AUDIT-LOGGER writes the booking ID as a string. Any reconciliation or lookup must be performed by Make — not by Airtable formulas or rollups.

---

## 5. PROTECTED FIELDS — MAKE MUST NEVER OVERWRITE

The following fields are classified as protected. The Make API token's write permissions are scoped to exclude these field IDs. Any Make module that attempts to write to a protected field will receive a 403 error from the Airtable API and log to Automation_Failures.

### 5.1 Bookings Table Protected Fields

| Field | Protection Reason | Modification Authority |
|-------|------------------|----------------------|
| `Package_Price` | Immutable after Status = CONFIRMED | Will only via Founder Decision |
| `Net_Profit` | Formula — Make cannot write formula fields | System (auto-calculated) |
| `Net_Margin_Pct` | Formula — Make cannot write formula fields | System (auto-calculated) |
| `Refund_Status` | Immutable after set | Will only |
| `Refund_Amount` | Immutable after set | Will only |
| `Chargeback_Risk` | Risk classification — human judgment required | Will or Luciana only |
| `D7_Review_Eligible` | Formula — Make cannot write formula fields | System (auto-calculated) |
| `Charter_Grade` | Post-charter quality assessment | Luciana only, with Will override |
| `UUID` | Formula — Make cannot write formula fields | System |

### 5.2 Audit Log Table Protected Fields

| Field | Protection Reason |
|-------|-----------------|
| `Execution_Timestamp` | Immutable — cannot be altered after write |
| `Scenario_ID` | Immutable — audit record identity |
| `Idempotency_Key` | Immutable — dedup reference |
| `Action_Type` | Immutable — record of what happened |
| `Audit_ID` | Formula — system-generated |

### 5.3 Clients Table Protected Fields

| Field | Protection Reason |
|-------|-----------------|
| `HV_Client` | High-value designation — Will only |
| `Charter_History_Count` | Rollup — system-calculated, not editable |

---

## 6. AIRTABLE PERMISSION MODEL FOR MAKE API TOKEN

### 6.1 Token Architecture

Two separate tokens are required. Never use a single token for both bases.

| Token | Base | Scope | Stored In |
|-------|------|-------|----------|
| `MAKE-OPS-TOKEN` | SSS Operations (`appdZ49WqgjRXxA1R`) | Defined tables, defined fields — see 6.2 | Make Credential Vault (encrypted) |
| `MAKE-FIN-TOKEN` | SSS Financials (`apprDKQtV2GInThwE`) | P&L Per Charter — create and update only | Make Credential Vault (encrypted) |

### 6.2 MAKE-OPS-TOKEN Scope

| Table | Allowed Operations | Field Restrictions |
|-------|-------------------|-------------------|
| Requests | Create, Read, Update | No delete. All fields readable. Write-restricted: UUID (formula), Created_At |
| Bookings | Create, Read, Update | No delete. Protected fields excluded from write scope — see Section 5.1 |
| Clients | Create, Read, Update | No delete. HV_Client excluded from write scope |
| Brokers | Read only | No write, no delete, no create |
| Audit Log | Create only | No update, no delete, no read of other records |
| Automation_Health | Create, Read, Update | No delete |
| Automation_Failures | Create, Read | No update, no delete |

### 6.3 MAKE-FIN-TOKEN Scope

| Table | Allowed Operations | Field Restrictions |
|-------|-------------------|-------------------|
| P&L Per Charter | Create, Update | No delete, no read of financial formula fields. Write allowed: Booking_ID, Brand, Environment, Last_Sync_Timestamp, Sync_Status, Source_System only. |

### 6.4 Token Security Requirements

- Tokens are rotated every 90 days or immediately on any suspected compromise
- Rotation requires: new token generated → new token tested in sandbox → new token deployed to Make → old token revoked → Deployment Log entry
- Tokens are never stored in GitHub, Notion, Slack, or any document outside Make's encrypted credential vault
- Only Will may access or rotate the MAKE-OPS-TOKEN. Luciana may not view the token value.

---

## 7. CROSS-BASE WRITE STRATEGY

### 7.1 The Cross-Base Problem

Airtable does not support linked records, rollups, or formula references across bases. SSS Operations and SSS Financials are two separate bases. Make must bridge them manually.

### 7.2 M-AUDIT-LOGGER as the Cross-Base Bridge

M-AUDIT-LOGGER is the only scenario authorized to write to the SSS Financials base. No other Stage 1 scenario interacts with the Financials base.

**When M-AUDIT-LOGGER writes to Financials:**

```
Trigger: Booking status changes to COMPLETED (detected by M-BOOKING-CONFIRMATION or a status-change watcher)

Step 1: Read Booking record from SSS Operations base
        Fields: Booking_ID (human-readable), Brand, Environment, Net_Profit,
                Charter_Date, Package_Price, Total_Cost, Client_ID

Step 2: Check if P&L Per Charter record already exists for this Booking_ID
        (Search P&L Per Charter WHERE Booking_ID = [human_readable_booking_id])

Step 3a: IF exists AND Sync_Status = SYNCED → exit (already synced, idempotency)
Step 3b: IF exists AND Sync_Status ≠ SYNCED → update existing record
Step 3c: IF not exists → create new P&L Per Charter record

Step 4: Write to P&L Per Charter:
        Booking_ID, Brand, Environment, Last_Sync_Timestamp = NOW(), Sync_Status = SYNCED

Step 5: Write success to Audit Log (Operations base)

Step 6: Write Health state → Automation_Health (Operations base)
```

### 7.3 Reconciliation Monitoring

HEALTH-001 performs a daily reconciliation check:

```
Query 1: COUNT(Bookings WHERE Status = COMPLETED AND Environment = Production)
Query 2: COUNT(P&L Per Charter WHERE Sync_Status = SYNCED)
IF Query 1 > Query 2: Alert → FINANCIAL-SYNC-GAP — SEV-2 → Luciana
```

This check ensures no completed booking is missing a financial record. Because it is a count comparison across two bases (two separate Make API calls), it cannot catch mismatches (wrong Booking_ID in P&L Per Charter), only count gaps. A full reconciliation is a manual monthly process.

---

## 8. AUTOMATION_HEALTH TABLE — DETAILED SPECIFICATION

This table is new — it does not exist in the current main base and must be created as part of Phase 2 of the Airtable migration per `02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md`.

### 8.1 Creation Requirements

| Requirement | Detail |
|-------------|--------|
| Base | SSS Operations (`appdZ49WqgjRXxA1R`) |
| Create via | Airtable UI (Will only — schema change authority) |
| Linked to | Bookings (linked record field) |
| Primary field | `UUID` formula (RECORD_ID()) |
| View | Two views: (1) All Records sorted by Last_Execution_Timestamp desc; (2) Active Failures (Execution_Status = FAILURE, Resolved = false) |
| Airtable-native automations | NONE — no Airtable automation watches this table |

### 8.2 Record Lifecycle

One Automation_Health record per scenario per day (or per booking for booking-scoped scenarios). Records are not deleted — they are retained for 90 days for trend analysis, then archived.

**Record creation trigger:** Each Make scenario creates or updates its Automation_Health record at the start of execution. If a record already exists for this Scenario_ID + today's date, the existing record is updated. If no record exists, a new one is created.

**Exception:** For booking-scoped scenarios (M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION), the record is keyed by Scenario_ID + Booking_ID. One record per scenario per booking.

---

## 9. FIELD NAMING CONFLICTS AND RESOLUTIONS

During Phase 1 migration, several field naming conflicts were identified between the existing main base schema and the governance-specified names. The following resolutions are binding.

| Conflict | Existing Field Name | Governance-Spec Name | Resolution | Notes |
|---------|--------------------|--------------------|-----------|-------|
| Request agent status | `Agent Status` (with space) | `Agent_Status` | Rename to `Agent_Status` — confirm no existing Make scenarios reference old name | Make references field by ID, not name — safe to rename |
| Last agent action | `Last_Agent_Message_Timestamp` | `Last_AI_Action` | Rename — update all Make references | |
| HV client flag | `HV Booking` | `HV_Client` | Rename to `HV_Client` — matches governance spec | |
| Charter send states (20+ fields) | `D0 Sent`, `D1 Sent`, etc. | Moved to `Automation_Health` table | Extract to Automation_Health per Phase 3 migration; remove from Bookings after verification | Stage 1 does not use these fields; extraction is Phase 3 work |
| UUID field | Does not exist — Airtable record ID is used implicitly | `UUID` (Formula: RECORD_ID()) | Add `UUID` formula field to all required tables | Make will reference UUID by field name; ensure field name is exactly `UUID` |
| Environment | Does not exist on most tables | `Environment` | Add to all Stage 1 tables before any Make scenario is activated | Critical blocker — without this, sandbox isolation is impossible |
| Source System | Inconsistent or missing | `Source_System` | Add with consistent naming and choices: Stripe / Airtable / Make / Manual / API | |
| Financial base Booking_ID | `Booking_ID` typed as singleLineText | `Booking_ID` (singleLineText — cross-base limitation) | Accept limitation — document explicitly. Make writes human-readable ID. No linked record possible. | |

---

## 10. STAGE 1 SCENARIO → TABLE ACCESS MAP

Quick reference: which scenarios read and write which tables.

| Scenario | Requests | Bookings | Clients | Brokers | Audit Log | Automation_Health | Automation_Failures | P&L Per Charter |
|---------|----------|----------|---------|---------|-----------|------------------|--------------------|-|
| M-BRAND-ROUTER | R/W | — | — | — | W | W | W (on failure) | — |
| M-LEAD-INTAKE | W (create) | — | R/W | — | W | W | W (on failure) | — |
| M-SLACK-ALERTS | R | R | — | — | W | W | W (on failure) | — |
| M-CONCIERGE-ASSIGNMENT | R/W | R | — | R | W | W | W (on failure) | — |
| M-STRIPE-DEPOSIT | — | R/W | — | — | W | W | W (on failure) | — |
| M-BOOKING-CREATION | R | W (create) | R | — | W | W | W (on failure) | — |
| M-BOOKING-CONFIRMATION | — | R/W | R | — | W | W | W (on failure) | — |
| M-AUDIT-LOGGER | — | — | — | — | W (create only) | W | — | W |
| M-HEALTH-001 | — | R | — | — | R | R/W | R | — |
| M-HEALTH-FAILSAFE | — | — | — | — | — | R | — | — |

**Legend:** R = Read, W = Write, R/W = Read and Write, — = No access

---

*End of FINAL_PRODUCTION_AIRTABLE_ARCHITECTURE*
*Version 1.0 — Post-Phase-4 Consolidated Architecture*
*Schema changes to any table in this document require: Will approval, a Founder Decision record of type SYSTEM, and a Deployment Log entry. No exception.*
*Next review: upon Stage 2 Make scenario implementation or any migration phase completion*
