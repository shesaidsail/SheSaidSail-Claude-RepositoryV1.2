# 02_SYSTEMS_AUTOMATIONS__Ultimate_Airtable_Production_Architecture_v3.0_LOCKED

**Status:** LOCKED — PRODUCTION IMPLEMENTATION PLAN
**Version:** 3.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail + Mare Executive — All Bases, All Tables, All Automations
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Source Document:** 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION
**Purpose:** v3 hardening pass — production cleanup, normalization, and Make build readiness

---

## WHAT CHANGED FROM v2.0

v2.0 was the audit. v3.0 is the implementation plan.

v2.0 identified the problems. v3.0 defines the exact fix for each one: which fields to keep, which to delete, which tables to build, in what order, with what schema, ready to hand directly to a Make builder without further architecture work.

Key upgrades from v2.0:
- Bookings target reduced from 70 fields to 60 fields with full field-by-field breakdown
- Partner Outreach target reduced from 45 to 40 fields with Partnerships split schema defined
- Marketing + Synter intelligence layer added with exact table schemas
- Migration phases tightened with go/no-go validation gates
- Make safety fields specified per table, not just per system
- Readiness scoring tied to specific unblocked milestones

---

## SECTION 1 — PRESERVED AUDIT FINDINGS

*All findings preserved from v2.0 live audit. Do not remove or alter these findings.*

### 1.1 Live Base Inventory

| Base Name | Base ID | Tables | Status | Verdict |
|-----------|---------|--------|--------|---------|
| She Said Sail | appdZ49WqgjRXxA1R | 28 | Live — primary ops base | KEEP + OPTIMIZE |
| She Said Sail — Financials | apprDKQtV2GInThwE | 4 | Live — financial intelligence | KEEP + UPGRADE |
| She Said Sail — Operations v4 | apppFfA2VZVmamvXe | 9 | Live — richer schema variants | MIGRATE INTO PRIMARY, THEN RETIRE |
| She Said Sail — Operations v4 | app2FbmVD44BXShyx | 4 | Duplicate name, different content | MIGRATE INTO PRIMARY, THEN RETIRE |
| SSS Operations Extension | appOQ0MGpQU1W4hoN | 4 | All 4 tables duplicate app2FbmVD44BXShyx | RETIRE IMMEDIATELY |
| Influencer Outreach | appVWYY9Fp6tKu94m | 1 | Isolated — no cross-base links | MERGE INTO PRIMARY, THEN RETIRE |
| She Said Sail copy | appQVZRgKKS0diyVX | UNKNOWN | Rogue copy — uncontrolled | ARCHIVE AND DELETE |
| Operations v4 | app49vaVbRwuobpPv | UNKNOWN | Schema not retrieved — connection issue | MISSING INFO NEEDED |

**Audit Score — Current State:**

| Dimension | Score | Reason |
|-----------|-------|--------|
| Operational Quality | 4/10 | Core tables exist but fragmented across 8 bases |
| Automation Readiness | 3/10 | No single base contains all Make dependencies |
| Financial Readiness | 4/10 | Financial base unlinked from ops records |
| AI Readiness | 3/10 | AI_Prompt_Versions duplicated with conflicting schemas |
| Scaling Readiness | 2/10 | Architecture cannot survive a third city without rebuild |

---

### 1.2 Critical Audit Findings

**FINDING 1 — SEVERE BASE FRAGMENTATION**
8 bases exist where governance requires 2 (Production + Financials) plus 1 optional Sandbox. Tables that must be linked to each other are in different bases. Airtable does not support cross-base linked records. This breaks every rollup, every formula dependency, and every Make scenario that reads related records in a single query.

**FINDING 2 — DUPLICATE TABLES WITH CONFLICTING SCHEMAS**

| Table | Base Instances | Field Counts |
|-------|---------------|-------------|
| Emergency_Protocols | apppFfA2VZVmamvXe, app2FbmVD44BXShyx, appOQ0MGpQU1W4hoN | 10 / 10 / 10 |
| Make_Scenarios | app2FbmVD44BXShyx, appOQ0MGpQU1W4hoN | 12 / 12 |
| ME_Pricing | app2FbmVD44BXShyx, appOQ0MGpQU1W4hoN | 12 / 12 |
| Concierge_Operators | app2FbmVD44BXShyx, appOQ0MGpQU1W4hoN | 12 / 12 |
| AI_Prompt_Versions | appdZ49WqgjRXxA1R (9 fields), apppFfA2VZVmamvXe (26 fields) | 9 / 26 |
| Yacht_Availability | appdZ49WqgjRXxA1R (13 fields), apppFfA2VZVmamvXe (17 fields) | 13 / 17 |

No single source of truth exists for any of these tables.

**FINDING 3 — BOOKINGS TABLE OVERLOAD**
Bookings (tbl72omPibBkn2hZL) contains 129 fields. Make modules reading this table must handle 129 fields per API call. AI context injection includes irrelevant fields. Formula recalculation on every field write slows all automations. Target after v3.0 normalization: 60 fields.

**FINDING 4 — FINANCIAL BASE IS UNLINKED**
P&L Per Charter Booking_ID field is typed singleLineText, not linked record. No rollup from Bookings to P&L is possible without Make writing both records. Any Booking change does not propagate to P&L Per Charter automatically.

**FINDING 5 — MISSING MANDATORY GOVERNANCE TABLES**

| Required Table | Governance Source | Current Status |
|----------------|-----------------|----------------|
| Expenses | Financial_OS_v1.0 | MISSING |
| Contractors | Financial_OS_v1.0 | MISSING |
| Financial_Periods | Systems_Intelligence_Architecture_v2.0 | MISSING |
| Chart_of_Accounts | Financial_OS_v1.0 | MISSING |
| Incapacitation_Actions | Founder_Control_Framework_v2.0 Art. VII | MISSING |
| Cybersecurity_Incidents | Founder_Control_Framework_v2.0 Art. VIII | MISSING |
| Governance_Reviews | Founder_Control_Framework_v2.0 Art. XVIII | MISSING |
| AI_Audit | Systems_Intelligence_Architecture_v2.0 | MISSING |
| Team_Members | Operational_Memory_Layer_v1.0 | MISSING |
| Automation_Health | Systems_Intelligence_Architecture_v2.0 | MISSING |

**FINDING 6 — PARTNER OUTREACH TABLE OVERLOAD**
Partner Outreach (tblnjGWa6JNiogfCo) contains 84 fields. The table conflates the outreach pipeline (lead tracking, outreach stages) with relationship intelligence (partnership ROI, commission history, content tracking). These are two separate operational concerns.

**FINDING 7 — PACKAGES TABLE SEVERELY UNDERDEVELOPED**
Packages (tblwDw2hkKW5moSr9) has only 8 fields and is the pricing authority for all booking quotes. Missing: F&B cost targets, margin floor enforcement, peak multipliers, add-on pricing matrix, city-specific variants, and AI-readable includes/excludes fields.

**FINDING 8 — AI_PROMPT_VERSIONS HAS WRONG SCHEMA IN MAIN BASE**
Main base version (tbl0FJkA1E6a70cxX) has 9 fields. Missing 17 required governance fields including Deployed_By, Deployed_At, Rollback_To_Version, Brand, Make_Variable_Name, Will_Approved. Correct 26-field schema lives in apppFfA2VZVmamvXe (tbl2NSec9JjqW34Xf).

**FINDING 9 — ROGUE COPY BASE**
She Said Sail copy (appQVZRgKKS0diyVX) exists with unknown contents. Created outside the governed amendment process. Must be audited, confirmed as duplicate, and deleted.

**FINDING 10 — PLACEHOLDER TABLES CONSUMING SCHEMA SPACE**
Brand (tbllNjlllEhG92Ozo), Services (tblBOgArrdfPkvR8B), and Expansion Pipeline (tbllga7euKfd2ykM5) each contain only 6 generic Airtable default fields. Never built out. Archive and remove.

**FINDING 11 — ENVIRONMENT GOVERNANCE NOT IMPLEMENTED**
Environment field (Production / Sandbox / Development) is absent from the majority of tables in the main base. Sandbox records cannot be isolated from production data.

**FINDING 12 — UUID GOVERNANCE NOT IMPLEMENTED**
No dedicated UUID field on any table in the main base. Audit trails cannot reference records by immutable human-readable ID without a formula extracting RECORD_ID().

---

## SECTION 2 — FINAL BASE ARCHITECTURE

Three bases. No exceptions. No analytics base — Airtable is not the right tool for analytics aggregation at this stage.

| Base | Base ID | Role | Make Access |
|------|---------|------|------------|
| SSS Operations | appdZ49WqgjRXxA1R | All core operations, intelligence, governance, marketing | Full read/write |
| SSS Financials | apprDKQtV2GInThwE | Financial intelligence, investor reporting, payouts, P&L | Full read/write |
| SSS Sandbox | UNKNOWN — create fresh | Testing only | Read/write from sandbox Make connections only |

**Why no analytics base:** The existing tables (Paid Ads, Organic Content, Google Reviews, Campaigns) cover marketing performance adequately. A separate analytics base would require cross-base sync with no native linked records — creating the same fragmentation problem that is being fixed. Aggregate reporting goes to Make dashboards or Airtable interfaces inside SSS Operations.

**All other bases retire after Phase 3 migration is confirmed.**

---

## SECTION 3 — COMPLETE TABLE CLEANUP PLAN

### 3.1 Instruction Key

- **KEEP** — no changes required beyond universal fields
- **MODIFY** — add fields, no deletions, no structural changes
- **REBUILD** — significant field changes: add, remove, or restructure
- **REPLACE** — retire existing table ID, create new table with correct schema, migrate records
- **MERGE** — combine two existing tables into one, retire the weaker
- **ARCHIVE** — retain all data, remove from active views, no further writes
- **DELETE** — export CSV backup, then delete

---

### 3.2 SSS Operations Base — Full Table Plan

#### KEEP (no changes beyond universal fields)

| Table | Table ID | Keep Reason |
|-------|----------|-------------|
| State Transition Log | tblWCmLmR1x8CaxNH | Feeds Audit Log at correct granularity — do not merge |
| Google Reviews | tblE2tMb5A1IqwOzW | Confirmed solid schema |
| Calls Recommended | tbl18uNpNd7HPBCps | Confirmed solid schema |
| Dashboard Notes | tblL9xCyFbl0fGkLB | Utility table — no automation dependency |
| Website/Landing Page | tblVq6XV6AyOxfXAU | Confirmed solid schema |

#### MODIFY (add fields only — no deletions)

| Table | Table ID | Changes |
|-------|----------|---------|
| Requests | tblTlSB9CO4dTGodg | Add: Escalation_Reason, AI_Confidence_Score, Last_Human_Touch; rename: Last_Agent_Message_Timestamp to Last_AI_Action; confirm Agent_Status is Single Select |
| Clients | tblr84vRIWC5HmKvo | Add: UUID (formula), Environment, Source_System, Brand |
| Yachts | tblvyZk1SorIQ6KWF | Add: Charter_Readiness (single select), Insurance_Expiry (date), Last_Inspection_Date (date), UUID (formula), Environment |
| Brokers | tblUrAVcx4HMdWVsN | Add: Performance_Score (formula or rollup), City_Health_Rollup (lookup), UUID (formula), Environment |
| Vendors | tbl4xD1mKhf0QL9Fe | Add: Insurance_Expiry (date), Insurance_Alert_Sent (checkbox), UUID (formula), Environment |
| Lessons | tblAben0zR8spPPhE | Add: UUID (formula), Environment, Brand |
| Founder Decisions | tblFCE26qDwfp4Jwd | Add: SLA_Due_Date (formula: Created_At + 24h), SLA_Breached (formula), UUID (formula), Environment |
| Audit Log | tblrMpTfMk8q1eNHp | Add: Prompt_Version (text), AI_Confidence_Score (number), Approval_State (single select), Reviewed_By (text), Rollback_Linkage (text), Environment, Brand, City |
| Affiliates | tbltZIenYJsUrUYIP | Add: Linked Partnerships records, UUID (formula), Environment |
| Organic Content | tbl09BGFacWim5Rk7 | Add: Campaign (linked to Campaigns), Performance_Score (formula), UUID (formula), Environment |
| Paid Ads | tblVsxlNdP9xHDipE | Add: Campaign (linked to Campaigns), Synter_Ad_ID (text), UUID (formula), Environment |
| Copy/Creative Assets | tblutlUhd804erPev | Add: Campaign (linked to Campaigns), Synter_Asset_ID (text), UUID (formula), Environment |
| Cities | tblzqHlzECDvJ8KRH | Add: City_Health_Score (formula), UUID (formula), Environment |
| Conversations | tblhMocOusidgd3N0 | Add: Brand_Router_Output (single select: SSS/ME), Escalation_Flag (checkbox), UUID (formula), Environment |

#### REBUILD (field add + field removal)

| Table | Table ID | Current Fields | Target Fields | Changes Summary |
|-------|----------|---------------|--------------|----------------|
| Bookings | tbl72omPibBkn2hZL | 129 | 60 | Extract finance to P&L, extract automation tracking to Automation_Health, extract audit/QA to Operational_Audits — see Section 4 |
| Partner Outreach | tblnjGWa6JNiogfCo | 84 | 40 | Extract relationship intelligence to new Partnerships table — see Section 5 |
| Packages | tblwDw2hkKW5moSr9 | 8 | 25 | Full pricing authority rebuild — see Section 6 |

#### REPLACE (retire old ID, create new with correct schema)

| Retire | Retire ID | Create As | Source Schema |
|--------|-----------|-----------|--------------|
| AI_Prompt_Versions (weak) | tbl0FJkA1E6a70cxX | AI_Prompt_Versions (new) | apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf — 26 fields — see Section 7 |
| Yacht_Availability (weak) | tblDOoV4CHh8t4qpj | Yacht_Availability (new) | apppFfA2VZVmamvXe — 17-field schema |

#### MIGRATE INTO MAIN BASE (from fragmented bases)

| Table | Source Base | Source Table ID | Migration Method |
|-------|------------|----------------|----------------|
| Guests | apppFfA2VZVmamvXe | tblkEXnrZldbk2JNg | CSV export, recreate in main, import, link to Bookings and Clients |
| Vessel_Maintenance | apppFfA2VZVmamvXe | tbl07thLiuTNymGE0 | CSV export, recreate in main, link to Yachts |
| Emergency_Escalations | apppFfA2VZVmamvXe | tbloilr1Cl4HMOlbQ | CSV export, recreate in main, link to Bookings and Emergency_Protocols |
| Incident_Reports | apppFfA2VZVmamvXe | tblgiQqr7NkmXOSWy | CSV export, recreate in main, link to Bookings |
| Regional_Directors | apppFfA2VZVmamvXe | tbl2ttsHinOEpNk1j | CSV export, recreate in main, link to Cities |
| Operational_Audits | apppFfA2VZVmamvXe | tbll6kqF7Q6y12ri3 | CSV export, recreate in main, link to Bookings |
| City_Financials | apppFfA2VZVmamvXe | tblMciqDfXEAyXLuY | CSV export, recreate in main, link to Cities |
| Emergency_Protocols | app2FbmVD44BXShyx | tblmV5ZFLhPwmvhYp | CSV export, recreate in main |
| Make_Scenarios | app2FbmVD44BXShyx | tblwG90rBtKMENs0U | CSV export, recreate in main, update all scenario IDs |
| Concierge_Operators | app2FbmVD44BXShyx | tblIP5y0ScYyZuElf | CSV export, recreate in main, link to Cities and Bookings |
| ME_Pricing | app2FbmVD44BXShyx | tblm5p6GQmYEjhZpG | Do not migrate as standalone — merge fields into rebuilt Packages table with Brand=ME |
| Influencers | appVWYY9Fp6tKu94m | tblMQ9nv5WGp3RtTP | CSV export, recreate in main, link to Partner Outreach or Campaigns |

#### CREATE (new tables — no source)

Governance and operations:
- Automation_Health — see Section 8 for schema
- AI_Audit
- Cybersecurity_Incidents
- Incapacitation_Actions
- Governance_Reviews
- Expenses
- Contractors
- Team_Members
- Partnerships (split from Partner Outreach)

Marketing and intelligence:
- Campaigns — see Section 9 for schema
- Audience_Segments — see Section 9 for schema
- Synter_Sync_Log — see Section 9 for schema

#### ARCHIVE (export CSV, disable writes, remove from active views)

| Table | Table ID | Reason |
|-------|----------|--------|
| Brand | tbllNjlllEhG92Ozo | Airtable placeholder — 6 fields — never built |
| Services | tblBOgArrdfPkvR8B | Airtable placeholder — 6 fields — never built |
| Expansion Pipeline | tbllga7euKfd2ykM5 | Airtable placeholder — 6 fields — never built |

#### DELETE (after backup confirmation)

| Base | Disposition |
|------|------------|
| appOQ0MGpQU1W4hoN (SSS Operations Extension) | Export CSV of all 4 tables: tblZxt3cULUcUyd2A, tblYyxOoLEnNyJnsZ, tblYzAzYQO1TkcQph, tblkliSCA923i5JII. Confirm contents are exact duplicates of app2FbmVD44BXShyx tables. Delete entire base. |
| appQVZRgKKS0diyVX (She Said Sail copy) | Audit all tables. Confirm all contents are duplicates. Export CSV archive. Delete entire base. |
| apppFfA2VZVmamvXe | Delete only after all 7 source tables are confirmed live in main base and Make scenario IDs are updated. |
| app2FbmVD44BXShyx | Delete only after all 4 source tables are confirmed live in main base and Make scenario IDs are updated. |
| appVWYY9Fp6tKu94m | Delete only after Influencers migration is confirmed live. |
| app49vaVbRwuobpPv | Requires Phase 0 audit first. Disposition unknown until schema is retrieved. |

---

### 3.3 SSS Financials Base — Full Table Plan

| Table | Table ID | Action | Changes |
|-------|----------|--------|---------|
| P&L Per Charter | tblFLiODVbQENbL5U | MODIFY | Booking_ID stays singleLineText (cross-base constraint — cannot fix). Add: Last_Sync_Timestamp (datetime), Sync_Status (single select: PENDING/SYNCED/ERROR/STALE), UUID (formula), Environment |
| Payouts | tblaoU1alZ8lPJZKY | MODIFY | Add: Founder_Decision_Link (text), Approval_Gate (single select: PENDING/APPROVED/REJECTED), UUID (formula), Environment |
| Tax Tracker | tbluP7OwTVzPGjyNm | KEEP | Schema is correct. Add UUID and Environment only. |
| Monthly Revenue | tblpTgps7cRQwDZp2 | REPLACE | Retire. Replace with Financial_Periods (see below). |
| Financial_Periods | UNKNOWN | CREATE | Replaces Monthly Revenue. Fields: Period_ID (formula), Period_Start (date), Period_End (date), Status (single select: OPEN/CLOSED/AUDITED), Total_Revenue (rollup from P&L), Total_Expenses (rollup from Expenses), Net_Income (formula), Bookings_Count (count), Avg_Margin_Pct (rollup), Closed_By (text), Closed_At (datetime), Investor_Notes (long text), UUID (formula), Environment |
| Chart_of_Accounts | UNKNOWN | CREATE | Fields: Account_Code (text), Account_Name (text), Account_Type (single select: Revenue/COGS/OpEx/Asset/Liability/Equity), Brand (single select: SSS/ME/SHARED), Active (checkbox), Description (long text), UUID (formula) |
| Entity_Registry | UNKNOWN | CREATE | Fields: Entity_Name (text), Entity_Type (single select: LLC/Trust/Operating/Holding), Jurisdiction (text), EIN (text), Bank_Account_Last4 (text), Active (checkbox), Notes (long text), UUID (formula) |
| Cash_Flow_Forecast | UNKNOWN | CREATE | Fields: Forecast_Date (date), Period (linked to Financial_Periods), Expected_Revenue (currency), Expected_Expenses (currency), Net_Forecast (formula), Confidence (single select: HIGH/MEDIUM/LOW), Notes (long text), UUID (formula) |
| Investor_Reports | UNKNOWN | CREATE | Fields: Report_ID (formula), Period (linked to Financial_Periods), Status (single select: DRAFT/REVIEWED/SENT), Content (long text), Sent_At (datetime), Recipients (text), UUID (formula) |

---

## SECTION 4 — BOOKINGS TABLE NORMALIZATION

**Current:** 129 fields
**Target:** 60 fields
**Method:** Extract finance fields to P&L Per Charter, extract automation tracking to Automation_Health, extract audit/QA to Operational_Audits, delete redundant/deprecated fields

### 4.1 Fields to KEEP in Bookings (60 total)

**Identity (6 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Booking_ID | Primary field — text | Human-readable ID — keep as primary |
| UUID | Formula: RECORD_ID() | Immutable identifier |
| Environment | Single Select: Production / Sandbox / Development | Required for Make sandbox isolation |
| Brand | Single Select: SSS / ME | Required for AI context and Make routing |
| Source_System | Single Select: Stripe / Airtable / Make / Manual / API | Data origin |
| Idempotency_Key | Single Line Text | Make deduplication hash — write on first execution only |

**Lifecycle and Status (7 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Status | Single Select: INQUIRY / QUOTED / DEPOSIT_PAID / CONFIRMED / CHARTER_COMPLETE / CANCELLED / REFUNDED | Primary state machine field |
| Created_At | DateTime | Immutable creation timestamp |
| Confirmed_At | DateTime | When status first hit CONFIRMED |
| Cancelled_At | DateTime | When status first hit CANCELLED |
| Completed_At | DateTime | When status first hit CHARTER_COMPLETE |
| Last_Modified | DateTime | System-managed last update |
| Stage_Duration_Days | Formula | Current stage age in days — used by Make for SLA alerts |

**Client and Booking Details (8 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Client | Linked Record to Clients | Primary client link |
| Guest_Count | Number | Confirmed guest count |
| HV_Client | Checkbox | High-value flag — gates extra automation sequences |
| Special_Requests | Long Text | Client-submitted notes — AI context injection |
| Internal_Notes | Long Text | Ops team notes only |
| Escalation_Reason | Long Text | Populated by Make when Agent_Status = ESCALATED |
| Requests | Linked Record to Requests | Source inquiry |
| Broker | Linked Record to Brokers | Referring broker if applicable |

**Charter Details (7 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Charter_Date | Date | The date of the charter |
| Charter_Time | Time | Departure time |
| Charter_Duration_Hours | Number | Duration of charter in hours |
| City | Linked Record to Cities | Operating city |
| Yacht | Linked Record to Yachts | Assigned vessel |
| Package | Linked Record to Packages | Pricing package |
| Concierge_Operator | Linked Record to Concierge_Operators | Assigned concierge |

**Pricing and Payment (11 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Package_Price | Currency | Price from Package record — locked after CONFIRMED |
| Add_On_Total | Currency | Total add-on revenue |
| Discount_Amount | Currency | Manual discount applied — requires Founder Decision if over threshold |
| Total_Revenue | Formula | Package_Price + Add_On_Total - Discount_Amount |
| Deposit_Amount | Currency | Deposit charged |
| Deposit_Paid | Checkbox | Confirmed by Stripe webhook |
| Deposit_Date | DateTime | Stripe payment intent succeeded timestamp |
| Balance_Due | Formula | Total_Revenue - Deposit_Amount |
| Balance_Paid | Checkbox | Confirmed by Stripe webhook |
| Balance_Date | DateTime | Balance payment timestamp |
| Stripe_Payment_Intent_ID | Single Line Text | Stripe reference — required for reconciliation |

**Refund and Risk (4 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Refund_Issued | Checkbox | Triggers Make FINANCIAL-001 refund processing |
| Refund_Amount | Currency | If partial refund |
| Refund_Status | Single Select: NONE / PENDING / PARTIAL / FULL | Current refund state |
| Chargeback_Risk | Single Select: NONE / LOW / MEDIUM / HIGH / ACTIVE | Luciana or Will write only |

**AI and Agent Fields (5 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Agent_Status | Single Select: AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED | Required for Phase 2 inbound agent |
| AI_Confidence_Score | Number 0-100 | Set by Make on every AI action |
| Last_Human_Touch | DateTime | Last time a human wrote to this booking |
| Last_AI_Action | DateTime | Last AI action timestamp |
| AI_Model_Version | Text | Prompt version ID used on last AI action |

**Automation Control (5 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Automations_Paused | Checkbox | Make reads this as step 1 of every client-facing scenario — exits if true |
| Emergency_Flag | Checkbox | Hard stop on all outbound automation — set by Make EMERGENCY-001 |
| Last_Automation_Timestamp | DateTime | Last Make write to this record |
| D7_Review_Eligible | Formula | TRUE when Charter_Grade is not D or F, Emergency_Flag is false, Chargeback_Risk is not HIGH or ACTIVE, and Status is CHARTER_COMPLETE |
| Automation_Health | Linked Record to Automation_Health | One Automation_Health record per Booking |

**Post-Charter Quality (4 fields)**

| Field | Type | Notes |
|-------|------|-------|
| Charter_Grade | Single Select: A / B / C / D / F | Set by ops team post-charter — required for D7_Review_Eligible |
| Operational_Audit | Linked Record to Operational_Audits | Linked charter audit record |
| Emergency_Escalation | Linked Record to Emergency_Escalations | If escalation occurred |
| Guest_List | Linked Record to Guests | All guests on this charter |

**Financial Base Sync (3 fields)**

| Field | Type | Notes |
|-------|------|-------|
| PL_Sync_Status | Single Select: PENDING / SYNCED / ERROR / STALE | Set by Make FINANCIAL-001 after P&L write |
| PL_Last_Sync | DateTime | Timestamp of last successful P&L sync |
| PL_Record_ID | Single Line Text | The Airtable record ID of the linked P&L Per Charter record |

---

### 4.2 Fields to EXTRACT from Bookings

**Extract to P&L Per Charter (Financial base) — Make syncs on CHARTER_COMPLETE status**

Remove these fields from Bookings after Make FINANCIAL-001 is confirmed live and P&L sync is validated:

Net_Profit, Margin_Pct, City_Manager_Payout, Referral_Commission, Tax_Collected, Tax_Remitted, Total_Cost, Boat_Cost, Labor_Cost, F&B_Cost, Revenue_Per_Guest, Add_On_Revenue

Replacement in Bookings: PL_Sync_Status + PL_Last_Sync + PL_Record_ID (already in the 60-field list above).

**Extract to Automation_Health (new table) — one record per Booking**

Remove these fields from Bookings after Automation_Health table is live and Make is writing to it:

D0_Sent, D1_Sent, D3_Sent, D7_Sent, D9_Gift_Sent, D14_Sent, D30_Sent, D60_Sent, HV_D2_Call_Done, HV_D5_Sent, HV_D21_Sent, HV_D23_Sent, D7_Reminder_Sent, D10_Reminder_Sent, D72hr_Reminder_Sent, D48hr_Reminder_Sent, Charter_Brief_Sent, Charter_Brief_All_Vendors_Confirmed, T7_Confirmed, T48_Captain_Confirmed

Replacement in Bookings: Last_Automation_Timestamp + Automation_Health (linked record).

**Extract to Operational_Audits (linked record per charter)**

Remove these fields from Bookings after Operational_Audits is live:

Crew_Report, Crew_Report_Submitted, Vendor_Ratings_Entered, Exceptional_Charter, NPS_Score

Replacement in Bookings: Charter_Grade (single select) + Operational_Audit (linked record).

---

### 4.3 Fields to DELETE from Bookings (redundant or deprecated)

Before deleting any field, export CSV of that field's data.

- Any field with zero non-null values across all records (run audit in Airtable before deletion)
- Any field duplicating data already in the linked Packages record
- Any field duplicating data already in the linked Clients record
- HV Booking (rename to HV_Client — standardize field name per governance spec)

---

## SECTION 5 — PARTNER OUTREACH NORMALIZATION

**Current:** 84 fields in Partner Outreach (tblnjGWa6JNiogfCo)
**Target:** 40 fields in Partner Outreach (outreach pipeline only) + new Partnerships table (relationship intelligence)

### 5.1 Fields to KEEP in Partner Outreach (40 fields)

| Field | Type | Notes |
|-------|------|-------|
| Partner_Name | Primary field — text | Organization or individual name |
| UUID | Formula: RECORD_ID() | Immutable ID |
| Environment | Single Select: Production / Sandbox / Development | Required |
| Brand | Single Select: SSS / ME | Brand context |
| Source_System | Single Select | Data origin |
| Contact_Name | Single Line Text | Primary contact full name |
| Contact_Email | Email | Primary contact email |
| Contact_Phone | Phone | Primary contact phone |
| Contact_Title | Single Line Text | Role at their org |
| Partner_Type | Single Select: Hotel / Concierge_Service / Travel_Agent / Corporate_Events / Wedding_Planner / Photographer / Other | Pipeline categorization |
| City | Linked Record to Cities | Operating city |
| Outreach_Status | Single Select: IDENTIFIED / CONTACTED / MEETING_SCHEDULED / PROPOSAL_SENT / ACTIVE / INACTIVE / REJECTED | Pipeline state machine |
| Priority_Score | Number 1-10 | Manual or Make-set priority |
| First_Contact_Date | DateTime | Immutable — set on first outreach |
| Last_Contact_Date | DateTime | Updated by Make on every outreach action |
| Next_Follow_Up_Date | DateTime | Make uses this for sequence trigger |
| Contact_Method | Single Select: Email / Phone / LinkedIn / In_Person / WhatsApp | Channel used |
| Last_Message_Sent | Long Text | Most recent outreach message content |
| Response_Status | Single Select: NO_RESPONSE / RESPONDED / INTERESTED / NOT_INTERESTED / MEETING_BOOKED | Current response state |
| Meeting_Notes | Long Text | Notes from any calls or in-person meetings |
| Sequence_Step | Number | Current step in outreach sequence (1-N) |
| Sequence_Name | Single Line Text | Which Make sequence is active for this record |
| Automations_Paused | Checkbox | Make reads this before any outbound send |
| Campaign | Linked Record to Campaigns | Linked marketing campaign if applicable |
| Referral_Count | Count | Count of linked Bookings from this partner |
| Total_Revenue_Referred | Rollup | Sum of Total_Revenue from linked Bookings |
| Commission_Rate_Pct | Percent | Agreed commission rate |
| Commission_Type | Single Select: Per_Booking / Flat_Monthly / Revenue_Share | Commission structure |
| Partnership_Record | Linked Record to Partnerships | Link to full relationship intelligence record |
| Tags | Multiple Select | Flexible tagging |
| Assigned_To | Single Line Text | SSS team member handling this outreach |
| Source_Notes | Long Text | How this lead was identified |
| Influencer_Record | Linked Record to Influencers | If this partner has an influencer profile |
| Affiliate_Record | Linked Record to Affiliates | If this partner is an affiliate |
| Created_At | DateTime | Record creation timestamp |
| Last_Modified | DateTime | Last update timestamp |
| Idempotency_Key | Single Line Text | Make deduplication |
| Make_Execution_Log | Long Text | Last Make scenario execution result |
| Failed_Executions | Number | Count of Make execution failures on this record |
| Emergency_Flag | Checkbox | Hard stop on all outbound automation |

### 5.2 New Partnerships Table Schema

Create this table in SSS Operations. Fields to migrate from Partner Outreach (84-field version):

| Field | Type | Source |
|-------|------|--------|
| Partner | Linked Record to Partner Outreach | Primary link |
| Partnership_Status | Single Select: ACTIVE / PAUSED / EXPIRED | Active agreement status |
| Agreement_Date | Date | Signed contract date |
| Agreement_Expiry | Date | Contract renewal date |
| Contract_Notes | Long Text | Key terms summary |
| Commission_History | Long Text | Running log of commissions paid |
| Total_Commissions_Paid | Currency | All-time total |
| Relationship_Notes | Long Text | Long-form relationship intelligence |
| Content_Collaboration | Long Text | Any joint content, co-promotions |
| ROI_Score | Number | Calculated ROI of this partnership |
| Risk_Flag | Checkbox | Any concerns with this partnership |
| Risk_Notes | Long Text | If Risk_Flag is true |
| Renewal_Action | Single Select: RENEW / RENEGOTIATE / DO_NOT_RENEW | Pre-renewal decision |
| Managed_By | Single Line Text | Who owns this relationship |
| UUID | Formula: RECORD_ID() | Immutable ID |
| Environment | Single Select | Required |
| Brand | Single Select: SSS / ME | Required |
| Created_At | DateTime | Record creation |
| Last_Modified | DateTime | Last update |

---

## SECTION 6 — PACKAGES TABLE REBUILD

**Table:** tblwDw2hkKW5moSr9
**Current:** 8 fields
**Target:** 25 fields
**Action:** Add 17 fields to existing table. Do not remove the existing 8. Merge ME_Pricing records from app2FbmVD44BXShyx with Brand = ME.

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| Package_Name | Primary field — text | Existing | |
| Brand | Single Select: SSS / ME | NEW | Separates SSS and ME packages in the same table |
| City | Single Select or Linked to Cities | NEW | City-specific pricing authority |
| Status | Single Select | Existing (confirm) | |
| Base_Price | Currency | Existing (confirm field name) | Retail price charged to client |
| Duration_Hours | Number | Existing (confirm) | Charter duration |
| Min_Guests | Number | NEW | Minimum group size — AI uses for quote validation |
| Max_Guests | Number | NEW | Maximum group size — AI uses for quote validation |
| Live | Checkbox | NEW | AI will not quote any package where Live = false |
| Peak_Multiplier | Number | NEW | Multiplier applied during peak / holiday seasons |
| Margin_Floor_Pct | Percent | NEW | Minimum acceptable margin — below this requires Will approval |
| F&B_Cost_Target | Currency | NEW | Internal F&B cost target per booking |
| Vessel_Cost_Target | Currency | NEW | Internal vessel cost target per booking |
| Labor_Cost_Target | Currency | NEW | Internal crew and labor cost target |
| Total_Internal_Cost | Formula | NEW | F&B_Cost_Target + Vessel_Cost_Target + Labor_Cost_Target |
| Implied_Margin | Formula | NEW | (Base_Price - Total_Internal_Cost) / Base_Price |
| Includes_Formatted | Long Text | NEW | AI-readable bullet list of what is included — used in quote generation context |
| Excludes_Formatted | Long Text | NEW | AI-readable bullet list of what is excluded — used in quote generation context |
| Add_Ons_Matrix | Long Text | NEW | One add-on per line: Name | Retail Price | Internal Cost — AI uses for upsell quotes |
| Notes | Long Text | Existing | Internal ops notes |
| Bookings_Count | Count | NEW | Count of linked CONFIRMED Bookings using this package |
| Avg_Margin_Achieved | Rollup | NEW | Average actual margin from linked completed Bookings |
| UUID | Formula: RECORD_ID() | NEW | Immutable ID |
| Environment | Single Select | NEW | Required |
| Source_System | Single Select | NEW | Required |

**ME_Pricing merge instruction:** After Packages is rebuilt, export all ME_Pricing records from app2FbmVD44BXShyx. Map each field to the Packages schema above. Import with Brand = ME. Confirm no pricing authority duplication before retiring ME_Pricing.

---

## SECTION 7 — AI_PROMPT_VERSIONS CORRECTION

**Retire:** tbl0FJkA1E6a70cxX (9 fields — insufficient for governance)
**Replace with:** New table using schema from apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf (26 fields)

Migrate all records from tbl2NSec9JjqW34Xf to new table in main base (appdZ49WqgjRXxA1R). After migration, update all Make scenario references from the old table ID to the new table ID.

### Complete Target Schema (26 fields)

| Field | Type | Governance Requirement |
|-------|------|----------------------|
| Prompt_Version_ID | Formula: "AIV-" & RECORD_ID() | Immutable human-readable ID — primary reference in Audit Log |
| Prompt_Name | Single Line Text | Human name: SSS_INBOUND_V3, ME_QUOTE_V2 |
| Version | Number | Integer version number — increments on every edit |
| Brand | Single Select: SSS / ME | Required — SSS and ME prompts are maintained separately |
| Status | Single Select: DRAFT / TESTING / LIVE / DEPRECATED | Gate field — only one LIVE per Brand per Make_Variable_Name |
| Content | Long Text | Full prompt verbatim — Make reads this field for Claude API injection |
| Make_Variable_Name | Single Line Text | Exact Make variable: SSS_SYSTEM / ME_SYSTEM / SSS_QUOTE / ME_QUOTE |
| Will_Approved | Checkbox | Must be true before Status can be set to LIVE |
| Deployed_By | Single Line Text | Must be Will for all LIVE deployments |
| Deployed_At | DateTime | Immutable — set when Status first hits LIVE |
| Rollback_To_Version | Single Line Text | Prompt_Version_ID of the prior LIVE version — required before any deployment |
| Previous_Version | Linked Record to AI_Prompt_Versions | Self-referential link to prior version record |
| Performance_Notes | Long Text | Observed behavior notes from testing and production |
| Leads_Processed | Number | Count of leads processed using this version |
| Leads_Converted | Number | Count of conversions attributed to this version |
| Conversion_Rate_Pct | Formula | IF(Leads_Processed > 0, Leads_Converted / Leads_Processed * 100, 0) |
| Override_Count | Number | Count of times a human overrode AI output using this version |
| Assignee | User | Airtable native |
| Notes | Long Text | Internal notes |
| Attachments | Attachment | Supporting files |
| Created_At | DateTime | Record creation |
| Last_Modified | DateTime | Last update |
| Environment | Single Select: Production / Sandbox / Development | Required |
| Source_System | Single Select | Required |
| UUID | Formula: RECORD_ID() | Required |
| Audit_Log_Entries | Linked Record to Audit Log | All Audit Log records referencing this prompt version |

---

## SECTION 8 — MAKE READINESS REQUIREMENTS

### 8.1 Universal Safety Fields — Required on Every Production Table

These fields must be added to every table before any Make scenario that touches that table is built. No exceptions.

| Field | Type | Make Behavior |
|-------|------|--------------|
| UUID | Formula: RECORD_ID() | Make references this for all record lookups and audit writes |
| Environment | Single Select: Production / Sandbox / Development | Make reads as step 1 — exits if Sandbox when running in production mode |
| Brand | Single Select: SSS / ME | Make uses for routing to correct Claude prompt, correct SMS template, correct notification recipient |
| Source_System | Single Select | Make writes its own identifier when creating records |
| Created_At | DateTime | Consistent field name across all tables — do not use Airtable's "Created Time" display name |

---

### 8.2 Bookings-Specific Safety Fields

| Field | Table | Type | Make Behavior |
|-------|-------|------|--------------|
| Automations_Paused | Bookings | Checkbox | Make reads as step 1 of every client-facing scenario — exits immediately if true, writes failure to Audit Log |
| Emergency_Flag | Bookings | Checkbox | Make reads alongside Automations_Paused — exits if true |
| Idempotency_Key | Bookings | Single Line Text | Make writes hash(Booking_ID + Scenario_ID + Execution_Date) on first run — checks before acting on retries |
| D7_Review_Eligible | Bookings | Formula | Make reads before sending any review request — skips if false |
| PL_Sync_Status | Bookings | Single Select | Make FINANCIAL-001 checks this before writing to P&L — skips if already SYNCED |

---

### 8.3 Automation_Health Table — Full Schema

One record per Booking. Tracks all outbound send states. Make writes to this table instead of directly to Bookings fields.

| Field | Type | Notes |
|-------|------|-------|
| Booking | Linked Record to Bookings | Primary link — one Automation_Health per Booking |
| UUID | Formula: RECORD_ID() | Immutable ID |
| Environment | Single Select | Required |
| Brand | Single Select | Required |
| Booking_Status_At_Last_Check | Single Select | Snapshot of Booking status at last Make run |
| D0_Sent | Checkbox | Confirmation email sent |
| D0_Sent_At | DateTime | Timestamp |
| D1_Sent | Checkbox | D+1 follow-up |
| D1_Sent_At | DateTime | |
| D3_Sent | Checkbox | D+3 preparation message |
| D3_Sent_At | DateTime | |
| D7_Sent | Checkbox | D+7 check-in |
| D7_Sent_At | DateTime | |
| D9_Gift_Sent | Checkbox | D+9 gift send (HV only) |
| D9_Gift_Sent_At | DateTime | |
| D14_Sent | Checkbox | D+14 follow-up |
| D14_Sent_At | DateTime | |
| D30_Sent | Checkbox | D+30 review nudge |
| D30_Sent_At | DateTime | |
| D60_Sent | Checkbox | D+60 re-engagement |
| D60_Sent_At | DateTime | |
| HV_D2_Call_Done | Checkbox | HV only |
| HV_D5_Sent | Checkbox | HV only |
| HV_D21_Sent | Checkbox | HV only |
| HV_D23_Sent | Checkbox | HV only |
| D72hr_Reminder_Sent | Checkbox | Pre-charter 72hr reminder |
| D72hr_Sent_At | DateTime | |
| D48hr_Reminder_Sent | Checkbox | Pre-charter 48hr reminder |
| D48hr_Sent_At | DateTime | |
| Charter_Brief_Sent | Checkbox | Brief sent to client |
| Charter_Brief_Sent_At | DateTime | |
| Charter_Brief_All_Vendors_Confirmed | Checkbox | All vendors confirmed receipt |
| T7_Confirmed | Checkbox | T-7 day confirmation complete |
| T48_Captain_Confirmed | Checkbox | Captain confirmed T-48 |
| Failed_Executions | Number | Count of Make execution failures on this record |
| Last_Failure_Reason | Long Text | Last Make failure message |
| Last_Make_Write | DateTime | Timestamp of last Make update to this record |
| Health_Status | Single Select: HEALTHY / BEHIND / FAILED / PAUSED | Derived from send state vs expected state given charter date |

---

### 8.4 Make Loop Prevention Rules

These rules must be implemented in every Make scenario that writes to Airtable. These are not suggestions.

**Rule 1 — Environment Gate**
Scenario step 1: Read Environment field from the trigger record. If Environment = Sandbox and scenario is running in Production connection, stop execution. Log to Audit Log: "Sandbox record blocked production scenario."

**Rule 2 — Automations_Paused Gate**
Any scenario that sends outbound communication (SMS, email, or any client-facing message): step 2 must read Automations_Paused AND Emergency_Flag. If either is true, stop execution. Log to Audit Log.

**Rule 3 — Idempotency Check**
Any scenario that creates records or sends unique communications: check Idempotency_Key before acting. If key already matches, skip execution silently. Do not log as error.

**Rule 4 — Circular Trigger Prevention**
All Airtable native automations on Bookings must be scoped to specific field changes only, not the generic "record updated" trigger. Audit every native automation before any Make scenario writes to Bookings. Document in Make_Scenarios registry.

**Rule 5 — Retry-Safe Writes**
All Make writes to Airtable use Update Record (not Create Record) wherever possible. Prefer PUT semantics over POST to avoid duplicates on retry.

**Rule 6 — Status Field Write Protection**
Make scenarios must not overwrite Status on Bookings unless the status transition is explicitly in the scenario's authorized transition map. Unauthorized status writes require a Founder Decision record.

---

### 8.5 Make_Scenarios Table — Required Schema

Migrate from app2FbmVD44BXShyx tblwG90rBtKMENs0U. After migration, extend schema:

| Field | Type | Notes |
|-------|------|-------|
| Scenario_Name | Primary field — text | Governance ID: BOOKING-001, CHARTER-006, etc. |
| Make_Scenario_ID | Single Line Text | Actual Make platform scenario ID — UNKNOWN for all current scenarios until Will audits Make dashboard |
| Status | Single Select: PLANNED / BUILDING / TESTING / LIVE / DEPRECATED / DISABLED | Current scenario state |
| Brand | Single Select: SSS / ME / BOTH | Which brand this scenario serves |
| Trigger_Type | Single Select: Webhook / Scheduled / Manual / API | How it fires |
| Trigger_Table | Single Select | Which Airtable table triggers it |
| Trigger_Field | Single Line Text | Which field change triggers it |
| Writes_To | Long Text | All tables and fields this scenario writes to |
| Reads_From | Long Text | All tables and fields this scenario reads |
| AI_Prompt_Version | Linked Record to AI_Prompt_Versions | If this scenario calls Claude API |
| Last_Executed | DateTime | Last successful run |
| Last_Failure | DateTime | Last failure timestamp |
| Failure_Count | Number | Rolling failure count |
| Authorized_By | Single Line Text | Will approval for any LIVE scenario |
| Notes | Long Text | Build notes, known issues |
| UUID | Formula: RECORD_ID() | Required |
| Environment | Single Select | Required |

---

## SECTION 9 — MARKETING + SYNTER INTELLIGENCE LAYER

**Architecture:**

- Airtable is the marketing intelligence source of truth
- Synter is the execution layer (ad delivery, email execution, message sending)
- Claude is the strategy, copy, and intelligence layer
- Make is the sync and orchestration layer between all three

Do not replicate Synter data in Airtable. Airtable holds decisions, approvals, performance summaries, and attribution. Synter holds execution logs and delivery details.

---

### 9.1 New Tables to Create

#### Campaigns

The central marketing record. All content, ads, outreach, and spend link to a Campaign.

| Field | Type | Notes |
|-------|------|-------|
| Campaign_Name | Primary field — text | Human name: "Ibiza Summer 2026", "ME Corporate Q3" |
| Campaign_ID | Formula: "CAM-" & RECORD_ID() | Immutable ID |
| Brand | Single Select: SSS / ME | Required |
| City | Linked Record to Cities | Primary city target |
| Status | Single Select: DRAFT / ACTIVE / PAUSED / COMPLETED / ARCHIVED | Campaign state |
| Campaign_Type | Single Select: Awareness / Lead_Gen / Retargeting / Retention / Influencer / Event | |
| Start_Date | Date | |
| End_Date | Date | |
| Budget_Total | Currency | Approved campaign budget |
| Budget_Spent | Currency | Updated by Make from Synter or manual |
| Budget_Remaining | Formula | Budget_Total - Budget_Spent |
| Objective | Long Text | What this campaign is designed to achieve |
| Target_Audience | Linked Record to Audience_Segments | |
| Will_Approved | Checkbox | No campaign goes ACTIVE without this |
| Approval_Date | DateTime | |
| Leads_Generated | Rollup or Number | Count of Requests with this campaign attribution |
| Bookings_Attributed | Count | Count of Bookings attributed to this campaign |
| Revenue_Attributed | Rollup | Sum of Total_Revenue from attributed Bookings |
| CAC | Formula | Budget_Spent / Bookings_Attributed (guarded against divide by zero) |
| ROAS | Formula | Revenue_Attributed / Budget_Spent (guarded against divide by zero) |
| Paid_Ads | Linked Record to Paid Ads | All ads under this campaign |
| Organic_Content | Linked Record to Organic Content | All organic posts under this campaign |
| Creatives | Linked Record to Copy/Creative Assets | All creative assets under this campaign |
| Notes | Long Text | |
| UUID | Formula: RECORD_ID() | Required |
| Environment | Single Select | Required |
| Source_System | Single Select | Required |
| Synter_Campaign_ID | Single Line Text | Synter's internal ID for this campaign — UNKNOWN until Synter is connected |

#### Audience_Segments

Defines target audiences for campaigns. Airtable holds the definition. Synter holds the actual audience lists.

| Field | Type | Notes |
|-------|------|-------|
| Segment_Name | Primary field — text | "Ibiza HNW Female 35-55", "Corporate Events London" |
| Brand | Single Select: SSS / ME | |
| City | Linked Record to Cities | |
| Segment_Type | Single Select: Demographics / Behavioral / Lookalike / Retargeting / Custom | |
| Age_Range | Single Line Text | e.g. "30-55" |
| Key_Interests | Long Text | Interest categories used for targeting |
| Platforms | Multiple Select: Instagram / TikTok / Facebook / Google / LinkedIn / Email | Where this segment is targeted |
| Estimated_Size | Number | Approximate audience size |
| Synter_Segment_ID | Single Line Text | Synter's ID for this segment — UNKNOWN until connected |
| Campaigns | Linked Record to Campaigns | Campaigns using this segment |
| Performance_Notes | Long Text | What we know about this segment's response |
| Active | Checkbox | |
| UUID | Formula: RECORD_ID() | |
| Environment | Single Select | |
| Created_At | DateTime | |

#### Synter_Sync_Log

Audit trail of every sync between Airtable and Synter. Make writes one record per sync event.

| Field | Type | Notes |
|-------|------|-------|
| Sync_ID | Formula: "SYNC-" & RECORD_ID() | Immutable ID |
| Sync_Type | Single Select: Campaign_Push / Asset_Push / Performance_Pull / Audience_Push / Approval_Sync | Type of sync operation |
| Direction | Single Select: Airtable_to_Synter / Synter_to_Airtable | |
| Status | Single Select: SUCCESS / FAILED / PARTIAL | |
| Source_Record_ID | Single Line Text | Airtable record ID of the source record |
| Source_Table | Single Select | Which Airtable table the sync originated from |
| Synter_Record_ID | Single Line Text | Synter's corresponding record ID |
| Records_Synced | Number | Count of records in this sync batch |
| Error_Message | Long Text | Populated on FAILED or PARTIAL |
| Make_Scenario | Single Line Text | Scenario that triggered this sync |
| Executed_At | DateTime | Sync execution timestamp |
| Duration_Seconds | Number | Sync duration |
| Brand | Single Select: SSS / ME | |
| Environment | Single Select | |
| UUID | Formula: RECORD_ID() | |

---

### 9.2 Existing Marketing Table Modifications

**Paid Ads (tblVsxlNdP9xHDipE) — add fields:**
- Campaign (Linked Record to Campaigns)
- Synter_Ad_ID (Single Line Text)
- Audience_Segment (Linked Record to Audience_Segments)
- UUID (Formula: RECORD_ID())
- Environment (Single Select)

**Organic Content (tbl09BGFacWim5Rk7) — add fields:**
- Campaign (Linked Record to Campaigns)
- Platform_Performance_Score (Number — updated by Make from analytics)
- UUID (Formula: RECORD_ID())
- Environment (Single Select)

**Copy/Creative Assets (tblutlUhd804erPev) — add fields:**
- Campaign (Linked Record to Campaigns)
- Synter_Asset_ID (Single Line Text)
- Will_Approved (Checkbox)
- Approved_At (DateTime)
- UUID (Formula: RECORD_ID())
- Environment (Single Select)

**Partner Outreach — add Campaign link (already in Section 5.1 field list)**

---

### 9.3 Attribution in Bookings

Attribution is a field-level addition to Bookings, not a separate table. Add these fields in Phase 1:

| Field | Type | Notes |
|-------|------|-------|
| Attribution_Source | Single Select: Organic / Paid_Social / Referral / Partner / Direct / Email / Influencer / Unknown | How the lead arrived |
| Attribution_Campaign | Linked Record to Campaigns | Which campaign if paid or managed |
| UTM_Source | Single Line Text | Captured from inquiry form or Make |
| UTM_Medium | Single Line Text | |
| UTM_Campaign | Single Line Text | |

---

## SECTION 10 — MIGRATION ORDER

Migration protects live operations at every phase. No schema changes execute during active charter hours (8am to 8pm in any active city's local time). All changes require a Founder Decision record of type SYSTEM before execution per Article II of the Founder Control Framework.

---

### Phase 0 — Pre-Migration (no schema changes) — PREREQUISITE TO ALL PHASES

**Go/No-Go Gate:** Phase 0 must be 100% complete before any Phase 1 work begins.

1. Audit appQVZRgKKS0diyVX (She Said Sail copy): list all tables, retrieve schemas, confirm all contents are duplicates of main base records, document audit results in a new Governance_Reviews record
2. Audit app49vaVbRwuobpPv (Operations v4): run list_tables_for_base, retrieve full schema for all tables, determine if any unique content exists not captured in the main base or other fragmented bases
3. Inventory all Airtable native automations in appdZ49WqgjRXxA1R: document every native automation trigger table, trigger field, action type, and destination — this is the circular dependency map
4. Export all Make scenario IDs from the Make dashboard: document in a temporary spreadsheet, enter into Make_Scenarios registry after it is migrated in Phase 3
5. Audit Stripe webhook configuration: document all webhook endpoints, signing secrets, event types, and which Make scenario each event routes to
6. Will creates Founder Decision record: type SYSTEM, documenting the full v3.0 migration plan as authorized
7. Create SSS Sandbox base: create from scratch, do not repurpose any existing base with live data
8. Resolve architecture decisions (Section 10.1 below) before Phase 1 begins

**Validation gate:** All 8 items complete. Governance_Reviews record created. Founder Decision record exists.

---

### Phase 0 Architecture Decisions Required from Will

| Decision | Options | Recommended |
|----------|---------|-------------|
| SSS and ME packages — same table or separate | Single Packages table with Brand field vs. separate tables | Single table with Brand field — simpler, avoids another fragmentation |
| Financial_Periods — Ops base or Financials base | Ops base (linked to Bookings) vs. Financials base (near P&L) | Financials base — financial objects belong together, cross-base sync via Make already required |
| Sandbox base — create new or repurpose | Create fresh vs. repurpose app2FbmVD44BXShyx post-migration | Create fresh — eliminates residual record contamination risk |
| State Transition Log — merge into Audit Log or keep separate | Merge vs. separate | Keep separate — different granularity, different Make trigger requirements |
| Google Reviews — standalone or merge into Clients and Bookings | Standalone vs. linked records only | Standalone — confirm it links to Clients and Bookings via linked fields already |

---

### Phase 1 — Universal Field Additions (low risk, no record deletion)

**Principle:** Only adding fields. No field removals. No structural table changes.

**Go/No-Go Gate:** Confirm every Make scenario currently reading any modified table still runs correctly after each field addition. New fields are empty by default and do not break existing Make reads.

Order:

1. Add Environment field (Single Select: Production / Sandbox / Development) to: Bookings, Requests, Clients, Yachts, Brokers, Vendors, Lessons, Founder Decisions, Audit Log, Conversations, Affiliates, Partner Outreach, Organic Content, Paid Ads, Copy/Creative Assets, Cities, Packages
2. Add Brand field (Single Select: SSS / ME) to all tables currently missing it
3. Add UUID formula field (RECORD_ID()) to all tables
4. Add Source_System field (Single Select) to all tables
5. Add Idempotency_Key to Bookings
6. Add D7_Review_Eligible formula to Bookings
7. Add Refund_Amount and Refund_Issued to Bookings
8. Add PL_Sync_Status, PL_Last_Sync, PL_Record_ID to Bookings
9. Add Last_Automation_Timestamp to Bookings
10. Add Agent_Status, AI_Confidence_Score, Last_Human_Touch, Last_AI_Action, AI_Model_Version to Bookings
11. Add Attribution fields to Bookings: Attribution_Source, Attribution_Campaign, UTM_Source, UTM_Medium, UTM_Campaign
12. Add missing Requests fields: Escalation_Reason, AI_Confidence_Score, Last_Human_Touch (rename Last_Agent_Message_Timestamp to Last_AI_Action)
13. Add missing Audit Log fields: Prompt_Version, AI_Confidence_Score, Approval_State, Reviewed_By, Rollback_Linkage, Environment, Brand, City
14. Add Insurance_Expiry, Insurance_Alert_Sent, Last_Inspection_Date, Charter_Readiness to Yachts
15. Add Performance_Score to Brokers
16. Add Insurance_Expiry, Insurance_Alert_Sent to Vendors
17. Add SLA_Due_Date formula, SLA_Breached formula to Founder Decisions
18. Add Last_Sync_Timestamp, Sync_Status to P&L Per Charter
19. Add Approval_Gate, Founder_Decision_Link to Payouts

**Validate after each table:** Confirm existing Make scenarios are unaffected. Confirm Airtable native automations did not fire incorrectly.

---

### Phase 2 — Create New Governance Tables (no existing data affected)

All new tables. No existing records modified.

Order:

1. Create Automation_Health table in SSS Operations (full schema per Section 8.3). Link to Bookings.
2. Create AI_Audit table in SSS Operations. Fields: Audit_ID, Booking or Request link, Action_Type, AI_Model, Prompt_Version, Input_Summary, Output_Summary, Confidence_Score, Approval_State, Reviewed_By, Outcome, Created_At, UUID, Environment, Brand.
3. Create Cybersecurity_Incidents table.
4. Create Incapacitation_Actions table.
5. Create Governance_Reviews table.
6. Create Expenses table.
7. Create Contractors table.
8. Create Team_Members table.
9. Create Partnerships table (per Section 5.2 schema).
10. In SSS Financials: Create Chart_of_Accounts, Entity_Registry, Cash_Flow_Forecast, Investor_Reports, Financial_Periods.

**Validate after each table:** Confirm linked record fields resolve correctly. Confirm no naming conflicts with existing tables.

---

### Phase 3 — Migrate Tables from Fragmented Bases

**Method per table:**
1. Export all records from source table as CSV
2. Create new table in SSS Operations with correct schema (add UUID and Environment fields during creation)
3. Import CSV records
4. Validate record count matches source
5. Validate field mapping (no data in wrong fields)
6. Update any Make scenarios referencing source base + table ID to new base + table ID
7. Confirm all linked record fields resolve correctly within the new base
8. Do not delete source table until Phase 5

Migration order (safest first — least Make dependency risk first):

1. Guests (tblkEXnrZldbk2JNg from apppFfA2VZVmamvXe) — link to Bookings and Clients after import
2. Vessel_Maintenance (tbl07thLiuTNymGE0 from apppFfA2VZVmamvXe) — link to Yachts
3. Emergency_Escalations (tbloilr1Cl4HMOlbQ from apppFfA2VZVmamvXe) — link to Bookings
4. Incident_Reports (tblgiQqr7NkmXOSWy from apppFfA2VZVmamvXe) — link to Bookings
5. Regional_Directors (tbl2ttsHinOEpNk1j from apppFfA2VZVmamvXe) — link to Cities
6. Operational_Audits (tbll6kqF7Q6y12ri3 from apppFfA2VZVmamvXe) — link to Bookings
7. City_Financials (tblMciqDfXEAyXLuY from apppFfA2VZVmamvXe) — high field count — validate field by field
8. Emergency_Protocols (tblmV5ZFLhPwmvhYp from app2FbmVD44BXShyx) — consolidate 3 duplicate instances into one
9. Make_Scenarios (tblwG90rBtKMENs0U from app2FbmVD44BXShyx) — update all scenario IDs after import
10. Concierge_Operators (tblIP5y0ScYyZuElf from app2FbmVD44BXShyx) — link to Cities and Bookings
11. ME_Pricing (tblm5p6GQmYEjhZpG from app2FbmVD44BXShyx) — do not create standalone table — map fields to rebuilt Packages table with Brand = ME
12. Influencers (tblMQ9nv5WGp3RtTP from appVWYY9Fp6tKu94m) — link to Partner Outreach

**After all 12 migrations are validated:** Create marketing tables from Section 9 (Campaigns, Audience_Segments, Synter_Sync_Log).

---

### Phase 4 — Rebuild and Normalize High-Risk Live Tables

These changes modify live tables with active Make dependencies. This is the highest operational risk phase.

**Execution rules:**
- Execute during confirmed low-traffic window (Sunday night preferred)
- Will on standby during execution
- For every field being removed: export CSV of that field's data immediately before removal
- Rollback plan: re-add removed fields from CSV data if any Make scenario breaks
- Confirm every active Make scenario is disabled in Make before executing field removals

Order:

1. **Packages rebuild (tblwDw2hkKW5moSr9):** Add 17 new fields per Section 6. Do not remove any of the existing 8 fields yet. Import ME_Pricing records from app2FbmVD44BXShyx with Brand = ME. Validate all Bookings linked to Packages still resolve. Confirm AI quote generation (if live) reads the correct new fields.

2. **AI_Prompt_Versions replacement:** Create new AI_Prompt_Versions table in main base with full 26-field schema per Section 7. Migrate all records from apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf. Update all Make scenario references. Archive tbl0FJkA1E6a70cxX (9-field version) — mark as DEPRECATED in its Status field, do not delete until v3.0 is fully stable for 30 days.

3. **Yacht_Availability replacement:** Create new Yacht_Availability table from apppFfA2VZVmamvXe 17-field schema. Migrate all records from both old versions. Link to Yachts. Archive tblDOoV4CHh8t4qpj (13-field version).

4. **Partner Outreach reduction (tblnjGWa6JNiogfCo):** First ensure Partnerships table (created in Phase 2) has all relationship intelligence fields populated via CSV import from the 44 fields being removed from Partner Outreach. Confirm linked record between each Partner Outreach record and its Partnerships record exists. Then remove the 44 fields from Partner Outreach. Validate Make OUTREACH-001 scenario against the reduced schema.

5. **Bookings field extraction:** This is the final and highest-risk step.
   - Step A: Confirm Automation_Health table exists and is linked to all Booking records (one record each)
   - Step B: Disable all Make scenarios that write automation tracking fields to Bookings
   - Step C: Export CSV of all 20 automation tracking fields from Bookings
   - Step D: Remove the 20 automation tracking fields from Bookings
   - Step E: Update Make scenarios to write to Automation_Health instead of Bookings
   - Step F: Validate automation tracking is working correctly in Automation_Health for 48 hours before proceeding
   - Step G: Export CSV of all 12 finance fields from Bookings
   - Step H: Confirm FINANCIAL-001 is writing finance data to P&L Per Charter correctly
   - Step I: Remove the 12 finance fields from Bookings
   - Step J: Validate P&L Per Charter sync is working correctly

**Validate after each step:** Run end-to-end test booking through all scenarios. Confirm no data loss. Confirm Make scenario execution logs show clean runs.

---

### Phase 5 — Retire Fragmented Bases

Only execute after Phase 3 and Phase 4 are fully validated. Make scenarios must be confirmed to reference new table IDs only — no references to fragmented base IDs remaining.

Confirm by running a search across all Make scenario configurations for the old base IDs before executing any base deletion.

Order:

1. Export full CSV archive of all 4 tables in appOQ0MGpQU1W4hoN. Confirm all contents are confirmed duplicates. Delete appOQ0MGpQU1W4hoN.
2. Export full CSV archive of all tables in appQVZRgKKS0diyVX. Confirm all contents are confirmed duplicates. Delete appQVZRgKKS0diyVX.
3. Export full CSV archive of apppFfA2VZVmamvXe. Archive the base (do not delete immediately). Wait 14 days. If no issues surface, delete.
4. Export full CSV archive of app2FbmVD44BXShyx. Archive the base (do not delete immediately). Wait 14 days. If no issues surface, delete.
5. Export full CSV archive of appVWYY9Fp6tKu94m. Archive (do not delete immediately). Wait 14 days. If no issues surface, delete.
6. Resolve app49vaVbRwuobpPv based on Phase 0 audit findings.

---

## SECTION 11 — MISSING INFORMATION REQUIRED BEFORE MAKE BUILD

These are hard blockers. Each item must be resolved before the corresponding Make scenario can be built or activated.

### 11.1 Unknown Base Contents

| Item | Base | Required Action | Blocks |
|------|------|----------------|--------|
| Full schema of app49vaVbRwuobpPv | app49vaVbRwuobpPv | Run list_tables_for_base — connection issue in v2.0 audit | Phase 0 completion |
| Full contents of appQVZRgKKS0diyVX | appQVZRgKKS0diyVX | Run list_tables_for_base — confirm all tables are duplicates | Phase 5 safe deletion |

### 11.2 Unknown Field IDs

Full field IDs are required for Make webhook field mapping and permissions scoping. Run get_table_schema for:

- Bookings (tbl72omPibBkn2hZL) — all current 129 fields
- Requests (tblTlSB9CO4dTGodg) — all current 57 fields
- Clients (tblr84vRIWC5HmKvo) — all current 40 fields
- Founder Decisions (tblFCE26qDwfp4Jwd) — all current 26 fields

### 11.3 Unknown Make Scenario IDs

Will must audit the Make dashboard and document every live scenario ID in the Make_Scenarios registry after Phase 3 step 9.

| Scenario | Governance ID | Make Scenario ID |
|----------|--------------|-----------------|
| INBOUND-001 | INBOUND-001 | UNKNOWN |
| INBOUND-002 | INBOUND-002 | UNKNOWN |
| BOOKING-001 through BOOKING-004 | BOOKING-001 to 004 | UNKNOWN |
| CHARTER-001 through CHARTER-007 | CHARTER-001 to 007 | UNKNOWN |
| EMERGENCY-001 | EMERGENCY-001 | UNKNOWN |
| FINANCIAL-001 through FINANCIAL-003 | FINANCIAL-001 to 003 | UNKNOWN |
| INTELLIGENCE-001 | INTELLIGENCE-001 | UNKNOWN |
| BACKUP-001 | BACKUP-001 | UNKNOWN |
| HEALTH-001 | HEALTH-001 | UNKNOWN |
| ROLLBACK-PROMPT-001 | ROLLBACK-PROMPT-001 | UNKNOWN |

### 11.4 Airtable Native Automations Inventory

Not retrieved in the v2.0 audit. Required before Phase 1 begins. Will audits the Automation tab in appdZ49WqgjRXxA1R and documents every native automation: trigger table, trigger field, action type, and destination. This becomes the circular dependency map before Make writes to Bookings.

### 11.5 Stripe Webhook Configuration

Not documented. Blocks FINANCIAL-001 and all payment confirmation scenarios. Will audits Stripe Developer → Webhooks and documents: endpoint URL, signing secret rotation date, event types, and which Make scenario each event routes to.

### 11.6 Synter Connection

Synter_Campaign_ID, Synter_Ad_ID, Synter_Asset_ID, and Synter_Segment_ID fields in the marketing tables are all UNKNOWN until Synter is connected. Synter_Sync_Log is an empty table until Make SYNTER-001 scenario is built. These unknowns do not block Phase 1-4 work — they only block the marketing and Synter scenarios built after Phase 4.

---

## SECTION 12 — FINAL READINESS SCORE

### 12.1 Current State (v2.0 audit findings)

| Dimension | Score | Blocking Issue |
|-----------|-------|---------------|
| Operational Quality | 4/10 | Core tables fragmented across 8 bases |
| Automation Readiness | 3/10 | No single base contains all Make dependencies |
| Financial Readiness | 4/10 | Financial base unlinked from ops records |
| AI Readiness | 3/10 | AI_Prompt_Versions duplicated with conflicting schemas |
| Scaling Readiness | 2/10 | Cannot add a third city without a rebuild |
| Marketing Intelligence | 2/10 | No campaign authority, no attribution, no Synter connection |
| **Overall** | **3/10** | |

---

### 12.2 Post-v3.0 State (after all phases complete)

| Dimension | Score | What Changed |
|-----------|-------|-------------|
| Operational Quality | 9/10 | All tables in 2 production bases, linked records, normalized schemas |
| Automation Readiness | 9/10 | All Make safety fields implemented, Automation_Health tracking, loop prevention in place |
| Financial Readiness | 8/10 | P&L sync via Make, Financial_Periods, Chart_of_Accounts, Payouts gate — limited to 8/10 because cross-base linked records are architecturally impossible in Airtable |
| AI Readiness | 9/10 | AI_Prompt_Versions correct schema, rollback governance, Will_Approved gate, brand separation |
| Scaling Readiness | 9/10 | City-scoped packages, City linked records, Regional_Directors — new city requires data entry, not rebuild |
| Marketing Intelligence | 8/10 | Campaigns authority, attribution in Bookings, Synter_Sync_Log — limited to 8/10 until Synter is connected |
| **Overall** | **9/10** | |

---

### 12.3 Remaining Blockers Before Make Build

The following must be resolved before the Make build begins. They are ordered by priority.

| Blocker | Phase Required | Priority |
|---------|---------------|----------|
| Environment field missing on Bookings and Requests | Phase 1, item 1 | CRITICAL — fix before any Make scenario is built |
| Automations_Paused not confirmed as read-first step in all outbound scenarios | Phase 1 + Make scenario audit | CRITICAL — operational safety |
| Idempotency_Key missing on Bookings | Phase 1, item 5 | CRITICAL — prevents duplicate records on Make retry |
| Airtable native automations not inventoried | Phase 0, item 3 | CRITICAL — circular trigger risk |
| AI_Prompt_Versions wrong schema in main base | Phase 4, item 2 | HIGH — blocks all Claude API scenarios |
| D7_Review_Eligible formula missing on Bookings | Phase 1, item 6 | HIGH — blocks CHARTER-006 |
| Make_Scenarios table not in main base | Phase 3, item 9 | HIGH — blocks HEALTH-001 and governance registry |
| Make scenario IDs undocumented | Phase 0, item 4 | HIGH — cannot audit, cannot route, cannot health-check |
| Stripe webhook configuration undocumented | Phase 0, item 5 | HIGH — blocks all payment scenarios |
| Bookings table has 129 fields — circular trigger risk on every write | Phase 4, item 5 | HIGH — blocks all Bookings-writing Make scenarios from being safely tested |
| Partner Outreach at 84 fields — Make webhook payload risk | Phase 4, item 4 | MEDIUM — blocks OUTREACH-001 |
| Make_Scenarios table in non-production base | Phase 3, item 9 | MEDIUM — needed before Phase 2 Make build |
| Synter not connected | Post Phase 4 | LOW — does not block ops or financial Make scenarios |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*02_SYSTEMS_AUTOMATIONS__Ultimate_Airtable_Production_Architecture_v3.0_LOCKED*
*Effective May 2026*
*Owner: Will (Founder)*
*Source Authority: 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED*
*Source Document: 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION*
*Version: 3.0 — LOCKED*
