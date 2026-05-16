# POST_PHASE_4_SCHEMA_REGISTRY.md
**Date:** 2026-05-16
**Phase:** Phase 4
**Status:** AUTHORITATIVE — Production schema state as of Phase 4 completion
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## Purpose

This document is the single source of truth for the SSS Operations base (appdZ49WqgjRXxA1R) schema as of Phase 4. Field counts, field IDs, types, and Phase 4 change annotations are recorded for every table. Update this document when schema changes are made.

---

## Base: SSS Operations (appdZ49WqgjRXxA1R)

### Table Registry

| Table Name | Table ID | Field Count | Phase 4 Changes | Make Ready |
|---|---|---|---|---|
| Bookings | tbl72omPibBkn2hZL | 151 | Pending: -23 deprecated fields → target 128 | PARTIAL |
| Requests | tblTlSB9CO4dTGodg | ~30 | None | READY |
| Packages | tblwDw2hkKW5moSr9 | ~28 | +14 fields added, +5 ME records | READY (ME); SSS pending data |
| Contacts | tblContactsXXXXXX | ~20 | None | READY |
| Conversations | tblhMocOusidgd3N0 | 23 | None | READY |
| AI_Audit | tbltItmUMLearQ7mC | 22 | None | READY |
| Automation_Health | tblCVpMsX4ZvnsJqL | ~18 | None | READY |
| AI_Prompt_Versions | tbl0FJkA1E6a70cxX | 9 | Pending: replace with 20-field schema | NOT READY |
| Make_Scenarios | tbl08IpivapVQZUto | ~15 | None | READY |
| Emergency_Protocols | tblsTbNXo4Pa9mDSW | ~12 | None | READY |
| Concierge_Operators | tblX61IB2qjDmac8l | ~14 | None | READY |
| Emergency_Escalations | tblDbeRf3qO3xvqhK | ~10 | None | READY |
| Partner_Outreach | tblPartnerXXXXXXX | 88 | Pending: -22 fields → Partnerships | CAUTION |
| Partnerships | tble5DcTo8mahr3lp | ~20 | None (receiving 22 fields) | READY |
| Influencers | tbl69Cguka4K4qgPO | ~18 | None | READY |
| Vessel_Maintenance | tblmYWqqIu1Cidb4g | ~12 | None | READY |
| Incident_Reports | tblO22Hh9lSTnhuu7 | ~10 | None | READY |
| Operational_Audits | tblAHYfl31529xUGr | ~15 | None | READY |
| City_Financials | tblycuku5Yq9s3fIw | ~12 | None | READY |
| Guests | tblpj4SwaSXu2vbVN | ~10 | None | READY |
| Regional_Directors | tblBK5EBPh5ppc8vw | ~10 | None | READY |
| Yacht_Availability | tblDOoV4CHh8t4qpj | 13 | Pending: replace with 15-field schema | NOT READY |
| Audit_Log | tblAuditLogXXXXXX | ~15 | None | READY |
| State_Transition_Log | tblStateXXXXXXXXX | ~12 | None | READY |
| Founder_Decisions | tblFounderXXXXXXX | ~15 | None | READY |
| Brand | tbllNjlllEhG92Ozo | — | Pending: rename to _PLACEHOLDER_Brand | N/A |
| Services | tblBOgArrdfPkvR8B | — | Pending: rename to _PLACEHOLDER_Services | N/A |
| Expansion_Pipeline | tbllga7euKfd2ykM5 | — | Pending: rename to _PLACEHOLDER_Expansion_Pipeline | N/A |

---

## Critical Table Detail: Packages (tblwDw2hkKW5moSr9)

Phase 4 added 14 new fields to this table. Full field registry:

### Phase 4 New Fields (Added 2026-05-16)

| Field Name | Field ID | Type | Phase 4 Purpose |
|---|---|---|---|
| City | fldiyXqFO7oOEyiCS | singleSelect | City-based routing for Make |
| Min_Guests | fldDBD22ElrnOvqt0 | number | Guest range validation |
| Max_Guests | fldA21eZf3e1vQ2in | number | Guest range validation |
| Margin_Floor_Pct | fldlBBMZ56TgEXvPX | percent | Minimum margin enforcement |
| Peak_Multiplier | fldLcwB7iBeeWklHr | number | Seasonal pricing |
| F&B_Cost_Target | fldd7tBGIGEDT6UWE | currency | Cost target (USD) |
| Vessel_Cost_Target | fldn3hedx6nlyRIDz | currency | Cost target (USD) |
| Labor_Cost_Target | fldAuqJ250x6OxOEj | currency | Cost target (USD) |
| Includes_Formatted | flduN43vf5nM5jp7z | multilineText | AI-readable inclusions |
| Add_Ons_Matrix | fldh2MxmJWpDmbrps | multilineText | AI-readable add-ons |
| Live | fldSpvpAthpuLeIMX | checkbox | Gating: only Live=true packages quoted |
| Will_Approved | fldpdjERlNOwmM9NK | checkbox | Approval gate |
| Total_Internal_Cost | fldmuWRy71JOLjBod | formula | Sum of 3 cost targets |
| Implied_Margin | fldCefqEQSMCOXNNc | formula | (Price − Total_Internal_Cost) / Price |

### Pre-Existing Fields (Selection of Key Fields)

| Field Name | Field ID | Type | Notes |
|---|---|---|---|
| Package_Name | (primary) | singleLineText | Primary field |
| Brand | fld1aGGMv49nBkC2s | singleSelect | SSS or ME |
| Source_System | fldSource | singleSelect | Governance |
| Environment | fldEnv | singleSelect | Governance |
| Legacy_Record_ID | fldLegacy | singleLineText | Governance |

### ME_Pricing Records (Phase 4 Created)

| Record ID | Package Name | City | Brand |
|---|---|---|---|
| receKte1p4egjf3Jw | Client Hosting Charter — Miami | Miami | Mare Executive |
| recfpvh5MdGkrajlc | Principal Private Charter — Miami | Miami | Mare Executive |
| rec1cktDMLPV8PHvQ | Client Hosting Charter — Fort Lauderdale | Fort Lauderdale | Mare Executive |
| recAQMYUI5wWpQeVX | Sunset Close Charter — Miami | Miami | Mare Executive |
| recHuXfKlLArY4LB9 | Executive Retreat — Full Day Miami | Miami | Mare Executive |

---

## Critical Table Detail: Bookings (tbl72omPibBkn2hZL)

### Key Make-Ready Fields (Confirmed Present)

| Field Name | Field ID | Type | Purpose |
|---|---|---|---|
| Environment | fldb2hN3kxhS3TwUT | singleSelect | Sandbox isolation |
| Automations_Paused | flduB7GqI7TOdQKUB | checkbox | Emergency stop |
| Idempotency_Key | fldjxNVa8Cr9RJhIq | singleLineText | Dedup |
| Agent_Status | fldHxIcogJjxFodS1 | singleSelect | AI routing gate |
| AI_Confidence_Score | fldlT6q0ADIMyx7MC | number | Confidence threshold |
| D7_Review_Eligible | fldDaIF93uwAQ6m8E | formula | Review gate |
| PL_Sync_Status | flds34c99jwYH5ypi | singleSelect | Financial sync gate |
| Automation_Health link | fldutXOFOw7H3DLy7 | linkedRecord | → Automation_Health |

### 23 Fields Pending Retirement (Phase 4 Deferred)

See PHASE_4_FIELD_RETIREMENTS.md for full detail with field IDs. Summary:

**D-Day Tracking Checkboxes (now duplicated by Automation_Health):**
D0_Sent, D1_Sent, D3_Sent, D7_Sent, D9_Gift_Sent, D14_Sent, D30_Sent, D60_Sent

**High-Value Tracking Checkboxes:**
HV_D2_Call_Done, HV_D5_Sent, HV_D21_Sent, HV_D23_Sent

**Reminder Checkboxes:**
D7_Reminder_Sent, D10_Reminder_Sent, D72hr_Reminder_Sent, D48hr_Reminder_Sent

**Operational Checkboxes:**
Charter_Brief_Sent, Charter_Brief_All_Vendors_Confirmed, T7_Confirmed, T48_Captain_Confirmed, Crew_Report_Submitted, Vendor_Ratings_Entered

**Duplicate Text Field:**
Conversations (multilineText — duplicated by Conversations table link)

**Target field count post-retirement: 128**

---

## Critical Table Detail: AI_Prompt_Versions (tbl0FJkA1E6a70cxX)

### Current State (9 fields — NOT READY)

Missing: Make_Variable_Name, Will_Approved, Status (LIVE/DRAFT/DEPRECATED), Rollback_To_Version, Deployed_By, Deployed_At, and 5 more fields present in the authorized 20-field schema from apppFfA2VZVmamvXe (tbl2NSec9JjqW34Xf).

### Required Action

1. Rename tbl0FJkA1E6a70cxX → `_DEPRECATED_AI_Prompt_Versions`
2. Create new table from apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf schema
3. Migrate any existing records with governance fields
4. M-BRAND-ROUTER cannot be built until complete

---

## Critical Table Detail: Yacht_Availability (tblDOoV4CHh8t4qpj)

### Current State (13 fields — NOT READY)

Missing: Hours_Until_Expiry formula required by M-YACHT-AVAILABILITY-LOCK. Richer 15-field schema exists in apppFfA2VZVmamvXe (tblkALubyHWjOY6Ul).

### Required Action

1. Confirm record count in tblDOoV4CHh8t4qpj (likely 0)
2. Confirm no Make scenario references this table ID (all 8 scenarios are NOT_STARTED — confirmed safe)
3. Rename old table → `_DEPRECATED_Yacht_Availability`
4. Create new table from richer schema
5. M-YACHT-AVAILABILITY-LOCK cannot be built until complete

---

## Base Registry (All 9 Bases)

| Base ID | Base Name | Status | Phase 5 Action |
|---|---|---|---|
| appdZ49WqgjRXxA1R | SSS Operations | ACTIVE — PRODUCTION | Keep |
| apprDKQtV2GInThwE | SSS Financials | ACTIVE — PRODUCTION | Keep |
| appOQ0MGpQU1W4hoN | Unknown (higher counts EP=14, MS=20) | ACTIVE — PRESERVED | Audit in Phase 5 |
| apppFfA2VZVmamvXe | Field Operations | SOURCE INTACT | Retire Phase 5 (30-day window) |
| app2FbmVD44BXShyx | Fragmented Ops | SOURCE INTACT | Retire Phase 5 (30-day window from 2026-05-16) |
| appVWYY9Fp6tKu94m | Influencer Outreach | SOURCE INTACT | Retire Phase 5 (30-day window from 2026-05-15) |
| appCrmXXXXXXXXXX | CRM / Contacts | UNKNOWN | Audit |
| appStripeXXXXXXX | Stripe Integration | DO NOT TOUCH | Stripe manages |
| appOtherXXXXXXXX | Other | UNKNOWN | Audit |

---

## SSS Financials Base (apprDKQtV2GInThwE)

| Table Name | Table ID | Status |
|---|---|---|
| Monthly Revenue | tblpTgps7cRQwDZp2 | Pending deprecation (export CSV first) |
| Other financial tables | — | Active |

---

## Schema Change Log (Phase 4)

| Date | Change | Table | Table ID | Change Type | Executor |
|---|---|---|---|---|---|
| 2026-05-16 | +14 fields | Packages | tblwDw2hkKW5moSr9 | Additive | Claude (MCP) |
| 2026-05-16 | +5 ME records | Packages | tblwDw2hkKW5moSr9 | Additive | Claude (MCP) |
| PENDING | -23 fields | Bookings | tbl72omPibBkn2hZL | Destructive | Will (Airtable UI) |
| PENDING | -22 fields (move) | Partner_Outreach | tblPartnerXXX | Destructive | Will (Airtable UI) |
| PENDING | Replace table | AI_Prompt_Versions | tbl0FJkA1E6a70cxX | Destructive | Will (Airtable UI) |
| PENDING | Rename 3 tables | Brand, Services, Expansion | — | Non-destructive | Will (Airtable UI) |
| PENDING | Deprecate table | Monthly Revenue | tblpTgps7cRQwDZp2 | Non-destructive | Will (Airtable UI) |
| PENDING | Replace schema | Yacht_Availability | tblDOoV4CHh8t4qpj | Destructive | Will (Airtable UI) |

---

## Governance Field Standards

Every record in every production table must carry:

| Field Name | Type | Value |
|---|---|---|
| UUID | formula | RECORD_ID() |
| Environment | singleSelect | Production |
| Brand | singleSelect | She Said Sail OR Mare Executive OR Both |
| Source_System | singleSelect | Source base ID (for migrated records) |
| Legacy_Record_ID | singleLineText | Original source record ID |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL — INTERNAL USE ONLY*
