# FINAL_PRODUCTION_AIRTABLE_ARCHITECTURE.md
**Date:** 2026-05-16
**Phase:** Phase 4 → Phase 5
**Status:** AUTHORITATIVE — Target production architecture for SSS + ME
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## Principle

One base. One record per entity. One source of truth per concept. Every field earns its place. No field that Make cannot write to. No table that has no active purpose. No formula that depends on a field that will be deleted.

---

## Production Base Architecture

### Primary Operational Base: SSS Operations (appdZ49WqgjRXxA1R)

This is the **only base Make scenarios write to**. This is the **only base Claude AI reads from**. This is the **only base Will manages day-to-day**. All other bases are either source archives (pending retirement) or specialty integrations.

---

## Table Map — SSS Operations Base

### Tier 1 — Core Transactional (High Write Volume)

These tables receive Make writes on every booking event. Schema must be stable and lean.

#### 1.1 Bookings (tbl72omPibBkn2hZL)
**Purpose:** Single source of truth for every charter booking across SSS and ME.
**Target field count:** 128 (currently 151 — remove 23 deprecated fields)
**Make write authority:** YES — after deprecated fields removed and native automations inventoried
**Critical fields:**
- `Environment` (fldb2hN3kxhS3TwUT) — sandbox gate
- `Automations_Paused` (flduB7GqI7TOdQKUB) — emergency stop
- `Idempotency_Key` (fldjxNVa8Cr9RJhIq) — dedup key for Make
- `Agent_Status` (fldHxIcogJjxFodS1) — AI routing (PENDING / IN_PROGRESS / ESCALATED / CLOSED)
- `AI_Confidence_Score` (fldlT6q0ADIMyx7MC) — confidence threshold for escalation
- `D7_Review_Eligible` (fldDaIF93uwAQ6m8E) — review gate formula
- `PL_Sync_Status` (flds34c99jwYH5ypi) — financial sync state
- `Automation_Health` link (fldutXOFOw7H3DLy7) — pointer to D-day tracking records

**What Make does NOT write to Bookings:** D-day tracking checkboxes (write to Automation_Health instead).

#### 1.2 Requests (tblTlSB9CO4dTGodg)
**Purpose:** Inbound charter inquiry pipeline. Triggers M-BRAND-ROUTER on new record creation.
**Make write authority:** YES — fully ready
**Critical fields:**
- `Environment` (fldF8PaiQacfKVtyE) — sandbox gate
- `Agent_Status` (fldxuo4jAq24oczGu — aiText) — AI routing
- `Brand_Detected` (fldC2fXzo3x9rpQbJ) — output from M-BRAND-ROUTER
- `Converted_To_Booking` (flduZNR7PRNxd7jwk) — conversion tracking
- `Lead_Response_Time_Min` (fldU5IpaRJI8bx18h) — SLA tracking

#### 1.3 Conversations (tblhMocOusidgd3N0)
**Purpose:** Message thread storage for AI context injection. 23 fields — correct size.
**Make write authority:** YES — fully ready
**Critical fields:**
- `Brand_Router_Output` (fldBalTPiand0JMjL) — AI routing decision
- `Escalation_Flag` (fldfEtg2n1yY8duIL) — human handoff trigger
- `Memory_Flag` (fld0ZH1zca7wZANl4) — context window boundary

---

### Tier 2 — Reference / Lookup (Read by Make, Rarely Written)

These tables Make reads from to make routing and quoting decisions.

#### 2.1 Packages (tblwDw2hkKW5moSr9)
**Purpose:** Authoritative package catalog for both SSS and ME brands.
**Make read authority:** YES — reads for quote generation, filters on Live=true AND Will_Approved=true
**Current records:** 5 ME (complete) + 132 SSS (Brand/City/costs TBD)
**Key routing logic for Make:**
```
Filter: Live = true AND Will_Approved = true AND Brand = {detected_brand} AND City = {client_city}
Select: package where Min_Guests ≤ {guest_count} ≤ Max_Guests
Validate: Implied_Margin ≥ Margin_Floor_Pct
Return: Includes_Formatted + Add_Ons_Matrix for AI proposal generation
```

#### 2.2 AI_Prompt_Versions (tbl0FJkA1E6a70cxX → NEW TABLE)
**Purpose:** Version-controlled prompt library for all Claude API calls.
**Current state:** NOT READY — 9-field table missing critical routing fields
**Target state:** 20-field table with Make_Variable_Name, Will_Approved, Status, Rollback_To_Version
**Make read authority:** YES — after table replacement
**Key routing logic for Make:**
```
Filter: Status = LIVE AND Will_Approved = true
Select: record where Make_Variable_Name = {scenario_variable}
Return: Prompt_Text for Claude API injection
```

#### 2.3 Emergency_Protocols (tblsTbNXo4Pa9mDSW)
**Purpose:** Pre-authored response templates for all emergency scenarios.
**Make read authority:** YES — M-EMERGENCY-ESCALATION reads Protocol_Name and Client_Communication_Template
**Records:** 8 protocols covering all severity levels

#### 2.4 Concierge_Operators (tblX61IB2qjDmac8l)
**Purpose:** Operator registry with authority levels and availability for escalation routing.
**Make read authority:** YES — reads Authority_Level and Emergency_Eligible for escalation chain

#### 2.5 Yacht_Availability (tblDOoV4CHh8t4qpj → NEW SCHEMA)
**Purpose:** Real-time hold tracking for yacht inventory management.
**Current state:** NOT READY — 13-field schema missing Hours_Until_Expiry formula
**Target state:** 15-field schema from apppFfA2VZVmamvXe
**Make write authority:** YES — after schema replacement

---

### Tier 3 — Audit / Governance (Written by Make, Rarely Read by Humans)

These tables exist to prove the system is working correctly. Make writes to all three consistently.

#### 3.1 Automation_Health (tblCVpMsX4ZvnsJqL)
**Purpose:** D-day tracking extracted from Bookings. One Automation_Health record per Booking.
**Make write authority:** YES — all D-day completion timestamps written here, NOT to Bookings
**Critical rule:** Make MUST write D-day completions to Automation_Health. Never to Bookings D-day checkboxes.
**Key fields:** Health_Status, Failed_Executions, Last_Make_Write, all D-day timestamp fields

#### 3.2 AI_Audit (tbltItmUMLearQ7mC)
**Purpose:** Per-action log of every Claude API call made by Make.
**Make write authority:** YES — written after every Claude API invocation
**22 fields** including: Action_Type, AI_Model, Prompt_Version, Confidence_Score, Approval_State, Reviewed_By, Rollback_Linkage

#### 3.3 Audit_Log
**Purpose:** Human-readable log of all significant system events.
**Make write authority:** YES — supplemental to AI_Audit
**When Make writes:** On booking state changes, escalations, and system errors

#### 3.4 State_Transition_Log
**Purpose:** Tracks every state change for every Booking.
**Make write authority:** YES — written on every Agent_Status change

---

### Tier 4 — Operational Intelligence (Human-Managed)

Make does not write to these tables. Will and operators manage them directly.

#### 4.1 Partner_Outreach (tblPartnerXXXXXXX)
**Purpose:** Outreach pipeline for prospective partners.
**Target field count:** 66 (currently 88 — remove 22 fields moving to Partnerships)
**Make write authority:** NO

#### 4.2 Partnerships (tble5DcTo8mahr3lp)
**Purpose:** Active partner relationship intelligence. Receiving 22 fields from Partner_Outreach.
**Make write authority:** NO

#### 4.3 Influencers (tbl69Cguka4K4qgPO)
**Purpose:** Influencer outreach registry. 31 records migrated in Phase 3.
**Make write authority:** NO

#### 4.4 Make_Scenarios (tbl08IpivapVQZUto)
**Purpose:** Registry of all Make scenarios with deploy order, status, and risk level.
**Make write authority:** NO — Will manages manually

#### 4.5 Vessel_Maintenance (tblmYWqqIu1Cidb4g)
**Purpose:** Pre-season and ongoing vessel inspection records.
**Make write authority:** NO

#### 4.6 Incident_Reports (tblO22Hh9lSTnhuu7)
**Purpose:** Incident documentation for insurance and pattern analysis.
**Make write authority:** NO

#### 4.7 Operational_Audits (tblAHYfl31529xUGr)
**Purpose:** Monthly operational performance records.
**Make write authority:** NO

#### 4.8 City_Financials (tblycuku5Yq9s3fIw)
**Purpose:** Per-city monthly financial rollups.
**Make write authority:** NO

#### 4.9 Emergency_Escalations (tblDbeRf3qO3xvqhK)
**Purpose:** Escalation event records.
**Make write authority:** YES (M-EMERGENCY-ESCALATION creates records here)

---

### Tier 5 — Structural / Placeholder (Pending Rename or Population)

These tables exist in the schema but are not yet active or are awaiting classification.

| Table | Table ID | Status | Action |
|---|---|---|---|
| Brand | tbllNjlllEhG92Ozo | PLACEHOLDER | Rename to _PLACEHOLDER_Brand |
| Services | tblBOgArrdfPkvR8B | PLACEHOLDER | Rename to _PLACEHOLDER_Services |
| Expansion_Pipeline | tbllga7euKfd2ykM5 | PLACEHOLDER | Rename to _PLACEHOLDER_Expansion_Pipeline |
| Guests | tblpj4SwaSXu2vbVN | EMPTY | Keep, no action needed |
| Regional_Directors | tblBK5EBPh5ppc8vw | EMPTY | Keep, no action needed |
| Founder_Decisions | tblFounderXXXXXXX | ACTIVE | Keep — Will manages |

---

## Make Scenario Architecture

### Deployment Order and Trigger Map

```
INBOUND INQUIRY
    └─► Requests (new record)
            └─► M-BRAND-ROUTER [Deploy #1]
                    ├─► Reads: AI_Prompt_Versions (brand routing prompt)
                    ├─► Writes: Requests.Brand_Detected
                    ├─► Writes: Conversations (context record)
                    └─► Writes: AI_Audit

BOOKING CREATION
    └─► Bookings (new record)
            ├─► M-YACHT-AVAILABILITY-LOCK [Deploy #2]
            │       ├─► Reads: Yacht_Availability
            │       ├─► Writes: Yacht_Availability (hold record)
            │       └─► Writes: Audit_Log
            │
            └─► M-DOUBLE-BOOKING-CHECK [Deploy #3]
                    ├─► Reads: Bookings (filter by yacht + date)
                    └─► Writes: Bookings.Agent_Status (ESCALATED if conflict)

BOOKING UPDATES
    ├─► M-BROKER-CONFIRMATION-GATE [Deploy #4]
    │       └─► Reads/Writes: Bookings
    │
    ├─► M-UTM-CAPTURE [Deploy #5]
    │       └─► Writes: Requests (UTM fields)
    │
    └─► M-CONVERSATION-CONTEXT-INJECT [Deploy #6]
            ├─► Reads: Conversations, AI_Prompt_Versions
            └─► Writes: Conversations.Memory_Flag

D-DAY EVENTS
    └─► Automation_Health (timestamp written)
            └─► M-CREW-REPORT-GATE [Deploy #7]
                    └─► Reads/Writes: Automation_Health, Bookings

EMERGENCY TRIGGER
    └─► M-EMERGENCY-ESCALATION [Deploy #8]
            ├─► Reads: Emergency_Protocols, Concierge_Operators
            └─► Writes: Emergency_Escalations, Audit_Log, AI_Audit
```

---

## Governance Architecture

### The 3-Layer Audit System

Every significant Make action writes to all three audit layers:

```
Layer 1: AI_Audit (tbltItmUMLearQ7mC)
    → Per-action: what prompt, what model, what confidence, what decision

Layer 2: Audit_Log
    → Per-event: what happened, when, triggered by what

Layer 3: State_Transition_Log
    → Per-booking: state machine history (PENDING → IN_PROGRESS → CLOSED)
```

### Emergency Stop Architecture

```
Check 1: Bookings.Automations_Paused = true → HALT all writes
Check 2: Bookings.Environment = Sandbox → Route to test records only
Check 3: Bookings.Idempotency_Key already processed → SKIP (dedup)
Check 4: AI_Prompt_Versions.Will_Approved = false → HALT Claude API call
Check 5: Packages.Live = false → EXCLUDE from quote generation
```

### Will Approval Gates

| Decision Point | Gate Field | Table |
|---|---|---|
| Package goes live | Will_Approved + Live | Packages |
| Prompt deployed | Will_Approved + Status=LIVE | AI_Prompt_Versions |
| Emergency protocol activated | Severity ≥ 4 → Will notified | Emergency_Protocols |
| Rollback | Requires Founder_Decisions record | Audit_Log |

---

## Multi-Brand Architecture

### Brand Routing Logic

```
Input: Client inquiry arrives in Requests
Detection: Requests.Brand_Detected ← M-BRAND-ROUTER output

If Brand_Detected = She Said Sail:
    Filter Packages: Brand = She Said Sail
    Load Prompt: AI_Prompt_Versions where Make_Variable_Name = SSS_QUOTE_PROMPT

If Brand_Detected = Mare Executive:
    Filter Packages: Brand = Mare Executive
    Load Prompt: AI_Prompt_Versions where Make_Variable_Name = ME_QUOTE_PROMPT
```

### City Expansion Path

When a new city is added (e.g., New York, Bahamas):
1. Add City as option in Packages.City singleSelect
2. Create package records for new city
3. Add Concierge_Operators record for city manager
4. No schema changes required — architecture is city-agnostic

---

## Financial Base: SSS Financials (apprDKQtV2GInThwE)

| Table | Status |
|---|---|
| City_Financials (copy) | Keep — monthly rollups |
| Monthly Revenue | DEPRECATE — export CSV, rename _DEPRECATED_ |

Financial data flows: Bookings → City_Financials (manual or formula rollup). No Make automation writes to the financials base.

---

## Phase 5 — Base Retirement (Future)

When validation windows close:

| Base | Retirement Trigger | Earliest Date |
|---|---|---|
| apppFfA2VZVmamvXe | All migrated data confirmed complete | 2026-06-15 |
| app2FbmVD44BXShyx | ME_Pricing merge confirmed complete | 2026-06-15 |
| appVWYY9Fp6tKu94m | Influencer data confirmed in appdZ49WqgjRXxA1R | 2026-06-14 |
| appOQ0MGpQU1W4hoN | Contents audited — retire or merge | After audit |

**Retirement protocol (each base):**
1. Confirm all records migrated (count match)
2. Export full CSV backup
3. Create Founder_Decisions record documenting retirement
4. Rename all tables in source base to `_RETIRED_YYYYMMDD_[table_name]`
5. Archive CSV in `99_ARCHIVE/PHASE_5_BASE_RETIREMENTS/`
6. Do not delete — Airtable bases cannot be undeleted

---

## Priority Queue for Will

Execute in this order for maximum leverage:

### This Week (Pre-Make Build)
1. [ ] Audit Airtable native automations on Bookings (15 min)
2. [ ] Replace AI_Prompt_Versions table (30 min) — BLOCKER for M-BRAND-ROUTER
3. [ ] Replace Yacht_Availability schema (20 min) — BLOCKER for M-YACHT-AVAILABILITY-LOCK
4. [ ] Rename 3 placeholder tables (2 min) — eliminates confusion
5. [ ] Export + deprecate Monthly Revenue table (5 min)

### This Week (Data Backfill)
6. [ ] Bulk update 132 SSS packages: populate Brand=She Said Sail + City (2 hrs)
7. [ ] Populate SSS package cost targets (2 hrs)

### After Data Backfill
8. [ ] Export CSV of 23 deprecated Bookings fields, then delete (45 min)
9. [ ] Export CSV of 22 Partner Outreach fields, verify Partnerships, then delete (60 min)

### After All Above — Begin Make Build
10. [ ] Build M-BRAND-ROUTER (Deploy Order 1)
11. [ ] Build M-YACHT-AVAILABILITY-LOCK (Deploy Order 2)
12. [ ] Build M-DOUBLE-BOOKING-CHECK (Deploy Order 3)

---

## Architecture Integrity Rules

These rules must never be broken:

1. **One write target per concept.** D-day tracking writes to Automation_Health only. Never to Bookings checkboxes.
2. **Idempotency first.** Every Make scenario checks Idempotency_Key before any write.
3. **Emergency stop second.** Every Make scenario checks Automations_Paused before any outbound action.
4. **Sandbox isolation.** Every Make scenario checks Environment before writing to production records.
5. **Will_Approved gates.** No unapproved prompt or package is ever used in production.
6. **CSV before delete.** No field or record is deleted from production without a CSV backup on file.
7. **Document before execute.** Every schema change is logged in Audit_Log with executor and timestamp.
8. **Rollback always available.** No Phase 5 base retirement until validation window passes and CSV backup exists.

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL — INTERNAL USE ONLY*
