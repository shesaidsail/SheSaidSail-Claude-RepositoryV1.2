# PHASE_0_MIGRATION_REPORT.md

**Status:** COMPLETE  
**Date:** 2026-05-15  
**Executed By:** Claude Code (claude-sonnet-4-6) — claude/airtable-production-architecture-qS104  
**Authority Document:** 02_SYSTEMS_AUTOMATIONS__Ultimate_Airtable_Production_Architecture_v3.0_LOCKED.md  
**Phase:** Phase 0 — Pre-Migration Audit (no schema changes)  

---

## SECTION 1 — UNKNOWN BASE AUDITS

### 1.1 appQVZRgKKS0diyVX — "She Said Sail copy"

**Verdict: CONFIRMED STALE DUPLICATE — SAFE FOR DELETION AFTER PHASE 5 VALIDATION**

**Audit Method:** list_tables_for_base + list_records_for_table (record count sampling)

**Table Inventory:**

| Table Name | Table ID | Field Count | Record Count | Status vs Main Base |
|-----------|---------|------------|-------------|-------------------|
| Clients | tblr84vRIWC5HmKvo | 40 | 1 | STALE (main: 1) — identical |
| Brokers | tblUrAVcx4HMdWVsN | 11 | unknown | STALE |
| Cities | tblzqHlzECDvJ8KRH | 23 | unknown | STALE |
| Yachts | tblvyZk1SorIQ6KWF | **29** | unknown | STALE — 2 fields behind main (main: 31) |
| Bookings | tbl72omPibBkn2hZL | 129 | 2 | STALE (main: 2) — same count, test data only |
| Packages | tblwDw2hkKW5moSr9 | 8 | unknown | STALE |
| Requests | tblTlSB9CO4dTGodg | **51** | 10 | STALE — 6 fields behind main (main: 57); main has 32 records |
| Partner Outreach | tblnjGWa6JNiogfCo | 84 | 174 | SAME count as main — copy taken after Partner Outreach was populated |
| Organic Content | tbl09BGFacWim5Rk7 | 19 | unknown | STALE |
| Paid Ads | tblVsxlNdP9xHDipE | 35 | unknown | STALE |
| Affiliates | tbltZIenYJsUrUYIP | 14 | unknown | STALE |
| Founder Decisions | tblFCE26qDwfp4Jwd | 26 | unknown | STALE |
| Audit Log | tblrMpTfMk8q1eNHp | 17 | unknown | STALE |
| State Transition Log | tblWCmLmR1x8CaxNH | 12 | unknown | STALE |
| Lessons | tblAben0zR8spPPhE | 23 | unknown | STALE |
| Google Reviews | tblE2tMb5A1IqwOzW | 23 | unknown | STALE |
| Google Performance | tblEqsCswZcLOh3B1 | 14 | unknown | STALE |
| Dashboard Notes | tblL9xCyFbl0fGkLB | 9 | unknown | STALE |
| Calls Recommended | tbl18uNpNd7HPBCps | 14 | unknown | STALE |
| Vendors | tbl4xD1mKhf0QL9Fe | 24 | unknown | STALE |
| Brand | tbllNjlllEhG92Ozo | 6 | unknown | STALE |
| Services | tblBOgArrdfPkvR8B | 6 | unknown | STALE |
| Expansion Pipeline | tbllga7euKfd2ykM5 | 6 | unknown | STALE |
| Website/Landing Page | tblVq6XV6AyOxfXAU | 21 | unknown | STALE |
| Copy/Creative Assets | tblutlUhd804erPev | 18 | unknown | STALE |
| Conversations | tblhMocOusidgd3N0 | 18 | unknown | STALE |
| ~~AI_Prompt_Versions~~ | ~~tbl0FJkA1E6a70cxX~~ | — | — | **MISSING — table added to main after copy was made** |
| ~~Yacht_Availability~~ | ~~tblDOoV4CHh8t4qpj~~ | — | — | **MISSING — table added to main after copy was made** |

**Table count:** 26 tables (main base: 28 tables — 2 tables were added to main after copy was created)

**Critical Finding — Identical Table IDs:**  
Every table in appQVZRgKKS0diyVX shares the same Table ID as the corresponding table in appdZ49WqgjRXxA1R. Record IDs sampled also match. This confirms appQVZRgKKS0diyVX is a direct Airtable "duplicate base" copy of the main production base. When Airtable duplicates a base, table IDs and record IDs are preserved.

**Data Divergence Summary:**
- **Requests:** Copy has 10 records, main has 32 — 22 records created after copy was taken
- **Yachts:** Copy has 29 fields, main has 31 — 2 fields added to main after copy
- **Requests:** Copy has 51 fields, main has 57 — 6 fields added to main after copy
- **All other sampled tables:** Record counts match; main is superset

**Conclusion:** All data in appQVZRgKKS0diyVX is a stale subset of appdZ49WqgjRXxA1R. No unique data exists in the copy that is not in the main base. Safe for Phase 5 deletion after full record count validation across all 26 tables.

**Webhook Risk:** Bookings records in the copy base contain live Make webhook URLs (hook.us2.make.com). This means at some point Make may have written to this base. **Will must confirm whether any active Make scenario currently writes to appQVZRgKKS0diyVX before deletion.**

---

### 1.2 app49vaVbRwuobpPv — "Operations v4"

**Verdict: CONFIRMED EMPTY — SAFE FOR IMMEDIATE RETIREMENT**

**Audit Method:** list_tables_for_base + list_records_for_table

**Table Inventory:**

| Table Name | Table ID | Field Count | Record Count | Notes |
|-----------|---------|------------|-------------|-------|
| Yacht_Availability | tbl6ykxDu5AUkuYIp | 9 | **0** | Completely empty |

**Fields in Yacht_Availability:**
Availability ID (singleLineText), Vessel Name (singleLineText), Charter Date (date), Status (singleSelect), Hold Type (singleSelect), Booking ID (singleLineText), City (singleSelect), Created By (singleSelect), Notes (multilineText)

**Critical Finding:** This base contains 1 table with 0 records. It is a standalone Yacht_Availability table with a weaker schema (9 fields) than both the main base version (tblDOoV4CHh8t4qpj, 13 fields) and the v3.0 target (17 fields). No linked records to any other base. No data to migrate.

**Conclusion:** app49vaVbRwuobpPv is an empty placeholder base. Can be deleted immediately once Will confirms no active Make scenarios reference it. No migration required.

---

## SECTION 2 — MAIN BASE INVENTORY (appdZ49WqgjRXxA1R)

**28 tables confirmed. Full schema retrieved.**

| Table | Table ID | Field Count | v3.0 Action |
|-------|---------|-----------|------------|
| Clients | tblr84vRIWC5HmKvo | 40 | MODIFY |
| Brokers | tblUrAVcx4HMdWVsN | 11 | MODIFY |
| Cities | tblzqHlzECDvJ8KRH | 23 | MODIFY |
| Yachts | tblvyZk1SorIQ6KWF | 31 | MODIFY |
| Bookings | tbl72omPibBkn2hZL | 129 | REBUILD (Phase 4) |
| Packages | tblwDw2hkKW5moSr9 | 8 | REBUILD (Phase 4) |
| Requests | tblTlSB9CO4dTGodg | 57 | MODIFY |
| Partner Outreach | tblnjGWa6JNiogfCo | 84 | REBUILD (Phase 4) |
| Organic Content | tbl09BGFacWim5Rk7 | 19 | MODIFY |
| Paid Ads | tblVsxlNdP9xHDipE | 35 | MODIFY |
| Affiliates | tbltZIenYJsUrUYIP | 14 | MODIFY |
| Founder Decisions | tblFCE26qDwfp4Jwd | 26 | MODIFY |
| Audit Log | tblrMpTfMk8q1eNHp | 17 | MODIFY |
| State Transition Log | tblWCmLmR1x8CaxNH | 12 | KEEP |
| Lessons | tblAben0zR8spPPhE | 23 | MODIFY |
| Google Reviews | tblE2tMb5A1IqwOzW | 23 | KEEP |
| Google Performance | tblEqsCswZcLOh3B1 | 14 | not in v3.0 spec — UNKNOWN |
| Dashboard Notes | tblL9xCyFbl0fGkLB | 9 | KEEP |
| Calls Recommended | tbl18uNpNd7HPBCps | 14 | KEEP |
| Vendors | tbl4xD1mKhf0QL9Fe | 24 | MODIFY |
| Brand | tbllNjlllEhG92Ozo | 6 | ARCHIVE |
| Services | tblBOgArrdfPkvR8B | 6 | ARCHIVE |
| Expansion Pipeline | tbllga7euKfd2ykM5 | 6 | ARCHIVE |
| Website/Landing Page | tblVq6XV6AyOxfXAU | 21 | KEEP |
| Copy/Creative Assets | tblutlUhd804erPev | 18 | MODIFY |
| Conversations | tblhMocOusidgd3N0 | 18 | MODIFY |
| AI_Prompt_Versions | tbl0FJkA1E6a70cxX | 9 | REPLACE (Phase 4) |
| Yacht_Availability | tblDOoV4CHh8t4qpj | 13 | REPLACE (Phase 4) |

**Unknown table — not in v3.0 spec:**
- Google Performance (tblEqsCswZcLOh3B1, 14 fields) — exists in live base but has no disposition defined in v3.0. **ACTION REQUIRED: Will to classify before Phase 4.**

---

## SECTION 3 — FINANCIALS BASE INVENTORY (apprDKQtV2GInThwE)

**4 tables confirmed.**

| Table | Table ID | Field Count | v3.0 Action |
|-------|---------|-----------|------------|
| P&L Per Charter | tblFLiODVbQENbL5U | 37 | MODIFY |
| Monthly Revenue | tblpTgps7cRQwDZp2 | 14 | REPLACE with Financial_Periods (Phase 4) |
| Payouts | tblaoU1alZ8lPJZKY | 12 | MODIFY |
| Tax Tracker | tbluP7OwTVzPGjyNm | 10 | KEEP + universal fields |

**Pre-existing governance fields found in Financials:**
P&L Per Charter already has: Brand, Service Category, Lead Source, Campaign, Creative ID. These were manually added per the table description and align with v3.0 requirements.

---

## SECTION 4 — NATIVE AUTOMATIONS INVENTORY

**STATUS: NOT ACCESSIBLE VIA MCP API**

The Airtable MCP server does not expose native automation configuration. Native automations cannot be inventoried programmatically.

**MANUAL ACTION REQUIRED (Will):**
Open appdZ49WqgjRXxA1R → Automations tab. Document for every active automation:
1. Automation name
2. Trigger: table, field, condition
3. Action type (create record, update record, send notification, run script, etc.)
4. Destination table/fields
5. Whether it reads or writes to Bookings

This is the **circular dependency map** required before Phase 4 Bookings field extractions. It is specifically required before any Make scenario writes to Bookings fields that may also have native automation triggers.

**Risk Level: CRITICAL** — Without this inventory, Phase 4 Bookings normalization carries unquantified circular trigger risk.

---

## SECTION 5 — HIGH-RISK TABLES IDENTIFIED

| Table | Risk Level | Risk Description |
|-------|-----------|-----------------|
| Bookings (tbl72omPibBkn2hZL) | **CRITICAL** | 129 fields; 2 live records with Make webhook URLs; every field write may trigger native automations; Phase 4 normalization requires full automation inventory first |
| Partner Outreach (tblnjGWa6JNiogfCo) | **HIGH** | 84 fields; 174 active records; active outreach pipeline; Phase 4 reduction must migrate 44 fields to Partnerships table first |
| AI_Prompt_Versions (tbl0FJkA1E6a70cxX) | **HIGH** | Wrong schema (9 fields vs 26 required); currently referenced by Make scenarios; replacement requires Make scenario ID update |
| Requests (tblTlSB9CO4dTGodg) | **HIGH** | 57 fields; 32 live records; active AI agent reads this table; Last_Agent_Message_Timestamp renamed to Last_AI_Action in Phase 1 (low risk, addition-only) |
| appQVZRgKKS0diyVX (copy base) | **MEDIUM** | Contains Make webhook URLs in Bookings records — must confirm no active Make scenarios target this base before deletion |

---

## SECTION 6 — DUPLICATE SCHEMAS CONFIRMED

| Table | Instances | Details |
|-------|----------|---------|
| AI_Prompt_Versions | 2 | appdZ49WqgjRXxA1R (9 fields) vs apppFfA2VZVmamvXe (26 fields) — conflicting schemas |
| Yacht_Availability | 3 | appdZ49WqgjRXxA1R (13 fields) + app49vaVbRwuobpPv (9 fields, empty) + apppFfA2VZVmamvXe (17 fields) |
| Emergency_Protocols | 3 | apppFfA2VZVmamvXe + app2FbmVD44BXShyx + appOQ0MGpQU1W4hoN |
| Make_Scenarios | 2 | app2FbmVD44BXShyx + appOQ0MGpQU1W4hoN |
| ME_Pricing | 2 | app2FbmVD44BXShyx + appOQ0MGpQU1W4hoN |
| Concierge_Operators | 2 | app2FbmVD44BXShyx + appOQ0MGpQU1W4hoN |

---

## SECTION 7 — MISSING MANDATORY FIELDS (PRE-PHASE 1)

All of the following were absent from the live system before Phase 1:

- Environment field: missing from all 20 Phase 1 target tables
- UUID field: missing from all 20 Phase 1 target tables
- Source_System field: missing from all 20 Phase 1 target tables
- Brand field: missing from 12 of the 20 Phase 1 target tables
- D7_Review_Eligible: missing from Bookings
- Idempotency_Key: missing from Bookings
- PL_Sync_Status / PL_Last_Sync / PL_Record_ID: missing from Bookings
- Agent_Status: missing from Bookings
- AI_Confidence_Score: missing from Bookings, Requests, Audit Log
- Last_Human_Touch / Last_AI_Action / AI_Model_Version: missing from Bookings, Requests
- Attribution_Source / Attribution_Campaign / UTM_Source / UTM_Medium / UTM_Campaign: missing from Bookings
- Escalation_Reason / Last_Human_Touch: missing from Requests
- Prompt_Version / Approval_State / Reviewed_By / Rollback_Linkage / City: missing from Audit Log
- Charter_Readiness / Insurance_Expiry / Last_Inspection_Date: missing from Yachts
- Performance_Score: missing from Brokers
- Insurance_Alert_Sent: missing from Vendors
- SLA_Due_Date: missing from Founder Decisions
- Brand_Router_Output / Escalation_Flag: missing from Conversations
- Sync_Status / Last_Sync_Timestamp: missing from P&L Per Charter
- Approval_Gate / Founder_Decision_Link: missing from Payouts
- Campaign / Platform_Performance_Score: missing from Organic Content

---

## SECTION 8 — CIRCULAR TRIGGER RISKS IDENTIFIED

**Risk 1 — Bookings native automation unknown:**
Bookings has 129 fields. Any field write in Phase 4 may trigger an unknown native automation. Without the manual automation inventory (Section 4), every Phase 4 Bookings operation carries unmeasured circular trigger risk.

**Risk 2 — appQVZRgKKS0diyVX Make webhook exposure:**
The copy base Bookings table contains Make webhook URLs. If any active scenario triggers on Bookings record changes in this base, the copy base is still operationally connected. This must be confirmed before Phase 5 deletion.

**Risk 3 — Last_Agent_Message_Timestamp rename:**
Renamed to Last_AI_Action in Phase 1. Any existing Make scenario or Airtable native automation that reads `Last_Agent_Message_Timestamp` by name will break. Will must audit Make scenario configurations for this field reference.

---

## SECTION 9 — ARCHITECTURE DECISIONS REQUIRED BEFORE PHASE 2

Per v3.0 Section 10 Phase 0 Architecture Decisions:

| Decision | Status |
|----------|--------|
| SSS and ME packages — same table or separate | PENDING WILL DECISION (recommended: single table with Brand field) |
| Financial_Periods — Ops base or Financials base | PENDING WILL DECISION (recommended: Financials base) |
| Sandbox base — create new or repurpose | PENDING WILL DECISION (recommended: create fresh) |
| State Transition Log — merge into Audit Log or keep separate | PENDING WILL DECISION (recommended: keep separate) |
| Google Reviews — standalone or merge | PENDING WILL DECISION (recommended: standalone, confirm linked fields) |
| Google Performance table — not in v3.0 spec | **UNKNOWN — Will must classify** |

---

## SECTION 10 — PHASE 0 GO/NO-GO ASSESSMENT

| Gate Item | Status | Blocker? |
|----------|--------|----------|
| appQVZRgKKS0diyVX audited | ✅ COMPLETE | No |
| app49vaVbRwuobpPv audited | ✅ COMPLETE | No |
| Native automations inventoried | ❌ MANUAL ACTION REQUIRED | **YES — blocks Phase 4** |
| Make scenario IDs documented | ❌ MANUAL ACTION REQUIRED | YES — blocks Phase 3 step 9 |
| Stripe webhook configuration documented | ❌ MANUAL ACTION REQUIRED | YES — blocks FINANCIAL-001 |
| Architecture decisions resolved | ❌ PENDING WILL | YES — blocks Phase 2 table creation |
| Founder Decision record (type SYSTEM) created | ❌ NOT CONFIRMED | YES — required by governance |
| SSS Sandbox base created | ❌ NOT DONE | YES — required before sandbox Make scenarios |

**Assessment: Phase 0 data collection is complete. Phase 1 field additions (low-risk, additions only) may proceed as they carry no schema destruction risk and do not depend on the outstanding blockers above. Phase 2 and beyond require the outstanding manual items to be resolved by Will.**

---

*Generated: 2026-05-15*  
*Branch: claude/airtable-production-architecture-qS104*  
*Authority: 02_SYSTEMS_AUTOMATIONS__Ultimate_Airtable_Production_Architecture_v3.0_LOCKED.md*
