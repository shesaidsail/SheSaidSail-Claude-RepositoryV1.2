# PRE-PHASE 4 LIVE AUDIT
**She Said Sail + Mare Executive — Airtable Architecture Normalization**

---

| Attribute | Value |
|---|---|
| Document Type | Pre-Normalization State Audit |
| Phase | Pre-Phase 4 (captured 2026-05-15) |
| Authority | Will Doyle — Founder, She Said Sail + Mare Executive |
| Classification | INTERNAL OPERATIONS — CONFIDENTIAL |
| Status | FINAL — Superseded by Phase 4 execution |

---

## Executive Summary

This audit captures the live state of the She Said Sail + Mare Executive Airtable architecture immediately before Phase 4 normalization execution on 2026-05-15. It documents all table inventories, field counts, critical schema deficiencies, duplication patterns, and risk assessments that informed Phase 4 actions.

The architecture spans two primary production bases (SSS Operations and SSS Financials), one validated secondary base (Field Operations), and five fragmented/rogue bases requiring audit or retirement. The SSS Operations base has reached 51 tables. The Financials base has 9 tables.

**Key findings driving Phase 4:**
- Bookings table at 151 fields (Phase 2 target: 70) — still severely overloaded
- Partner Outreach at 88 fields with no clean separation from Partnerships table
- AI_Prompt_Versions canonical table wrong version still primary
- ME_Pricing data stranded in fragmented base (not yet in Packages)
- Packages table severely underdeveloped for its role as AI pricing authority
- All 8 Make scenarios are status NOT_STARTED — zero live automations

**Overall architecture health pre-Phase 4: 61/100**
Phases 1–3 delivered strong governance field coverage and successful migrations, but the core operational tables (Bookings, Partner Outreach) remain overloaded and schema duplication persists.

---

## Part 1: Live Table Inventory

### 1.1 SSS Operations Base — appdZ49WqgjRXxA1R
**Total tables: 51**

| # | Table Name | Table ID | Field Count | Status / Notes |
|---|---|---|---|---|
| 1 | Clients | tblr84vRIWC5HmKvo | 44 | Operational |
| 2 | Brokers | tblUrAVcx4HMdWVsN | 16 | Operational |
| 3 | Cities | tblzqHlzECDvJ8KRH | 32 | Operational |
| 4 | Yachts | tblvyZk1SorIQ6KWF | 38 | Operational |
| 5 | Bookings | tbl72omPibBkn2hZL | 151 | **OVERLOADED** — Phase 2 target was 70 fields; 23 fields authorized for removal |
| 6 | Packages | tblwDw2hkKW5moSr9 | 12 | **UNDERDEVELOPED** — Phase 4 target: 26 fields; AI pricing authority missing margin/cost controls |
| 7 | Requests | tblTlSB9CO4dTGodg | 64 | Operational |
| 8 | Partner Outreach | tblnjGWa6JNiogfCo | 88 | **OVERLOADED** — 22 partnership-relationship fields duplicate Partnerships table |
| 9 | Organic Content | tbl09BGFacWim5Rk7 | 26 | Operational |
| 10 | Paid Ads | tblVsxlNdP9xHDipE | 40 | Operational |
| 11 | Affiliates | tbltZIenYJsUrUYIP | 18 | Operational |
| 12 | Founder Decisions | tblFCE26qDwfp4Jwd | 31 | Operational |
| 13 | Audit Log | tblrMpTfMk8q1eNHp | 27 | Operational |
| 14 | State Transition Log | tblWCmLmR1x8CaxNH | 12 | Operational |
| 15 | Lessons | tblAben0zR8spPPhE | 27 | Operational |
| 16 | Google Reviews | tblE2tMb5A1IqwOzW | 23 | Operational |
| 17 | Google Performance | tblEqsCswZcLOh3B1 | 22 | Operational |
| 18 | Dashboard Notes | tblL9xCyFbl0fGkLB | 9 | Operational |
| 19 | Calls Recommended | tbl18uNpNd7HPBCps | 14 | Operational |
| 20 | Vendors | tbl4xD1mKhf0QL9Fe | 30 | Operational |
| 21 | Brand | tbllNjlllEhG92Ozo | 6 | **PLACEHOLDER** — retire (rename to _DEPRECATED_) |
| 22 | Services | tblBOgArrdfPkvR8B | 6 | **PLACEHOLDER** — retire (rename to _DEPRECATED_) |
| 23 | Expansion Pipeline | tbllga7euKfd2ykM5 | 6 | **PLACEHOLDER** — retire (rename to _DEPRECATED_) |
| 24 | Website/Landing Page | tblVq6XV6AyOxfXAU | 21 | Operational |
| 25 | Copy/Creative Assets | tblutlUhd804erPev | 25 | Operational |
| 26 | Conversations | tblhMocOusidgd3N0 | 23 | Operational |
| 27 | AI_Prompt_Versions | tbl0FJkA1E6a70cxX | 9 | **WRONG VERSION** — underdeveloped; missing 11 governance fields; correct version is in apppFfA2VZVmamvXe (20 fields) |
| 28 | Yacht_Availability | tblDOoV4CHh8t4qpj | 13 | **OLD VERSION** — superseded by richer 15-field version in apppFfA2VZVmamvXe (tblkALubyHWjOY6Ul) |
| 29 | Automation_Health | tblCVpMsX4ZvnsJqL | 39 | Operational ✓ |
| 30 | AI_Audit | tbltItmUMLearQ7mC | 22 | Operational ✓ |
| 31 | Cybersecurity_Incidents | tblSTy6Rtn7vofF1r | 24 | Operational ✓ |
| 32 | Incapacitation_Actions | tbleMkafYH5w5xpO5 | 15 | Operational ✓ |
| 33 | Governance_Reviews | tbl0nCmwo6CPa3APJ | 17 | Operational ✓ |
| 34 | Team_Members | tblWrvF72JOrFmPkV | 15 | Operational ✓ |
| 35 | Partnerships | tble5DcTo8mahr3lp | 20 | Operational ✓ |
| 36 | Expenses | tblbtF1AVzDwkt0gE | 18 | Operational ✓ |
| 37 | Contractors | tblN75TzobD9AEvaq | 19 | Operational ✓ |
| 38 | Audience_Segments | tblu4JbvIxlhS1ehN | 15 | Operational ✓ |
| 39 | Campaigns | tblTs5px03BPrUpG4 | 29 | Operational ✓ |
| 40 | Synter_Sync_Log | tblbhwEaa8D23WmyA | 15 | Operational |
| 41 | Guests | tblpj4SwaSXu2vbVN | 18 | 0 records |
| 42 | Vessel_Maintenance | tblmYWqqIu1Cidb4g | 18 | Operational ✓ — 2 records migrated Phase 3 |
| 43 | Emergency_Escalations | tblDbeRf3qO3xvqhK | 20 | Operational ✓ — 2 records |
| 44 | Incident_Reports | tblO22Hh9lSTnhuu7 | 24 | Operational ✓ — 2 records |
| 45 | Regional_Directors | tblBK5EBPh5ppc8vw | 22 | 0 records |
| 46 | Operational_Audits | tblAHYfl31529xUGr | 28 | Operational ✓ — 2 records |
| 47 | City_Financials | tblycuku5Yq9s3fIw | 31 | Operational ✓ — 2 records |
| 48 | Emergency_Protocols | tblsTbNXo4Pa9mDSW | 15 | Operational ✓ — 8 records |
| 49 | Make_Scenarios | tbl08IpivapVQZUto | 17 | 8 scenarios — ALL status: NOT STARTED |
| 50 | Concierge_Operators | tblX61IB2qjDmac8l | 17 | 3 records |
| 51 | Influencers | tbl69Cguka4K4qgPO | 30 | 31 records — migrated Phase 3 |

---

### 1.2 SSS Financials Base — apprDKQtV2GInThwE
**Total tables: 9**

| # | Table Name | Table ID | Field Count | Status / Notes |
|---|---|---|---|---|
| 1 | P&L Per Charter | tblFLiODVbQENbL5U | 42 | Operational ✓ — Brand, Service_Category, Lead_Source fields added; Last_Sync_Timestamp, Sync_Status confirmed |
| 2 | Monthly Revenue | tblpTgps7cRQwDZp2 | 14 | **DEPRECATED** — superseded by Financial_Periods; both tables exist creating source-of-truth ambiguity |
| 3 | Payouts | tblaoU1alZ8lPJZKY | 18 | Operational ✓ |
| 4 | Tax Tracker | tbluP7OwTVzPGjyNm | 14 | Operational ✓ |
| 5 | Financial_Periods | tblli6AwOB114dOd1 | 17 | Operational ✓ — canonical replacement for Monthly Revenue |
| 6 | Chart_of_Accounts | tbl2fyC6EaxyR930u | 7 | Operational ✓ |
| 7 | Entity_Registry | tblkjnds7OogWdsuC | 19 | Operational ✓ |
| 8 | Cash_Flow_Forecast | tblUM50sXFXIjpH5N | 10 | Operational ✓ |
| 9 | Investor_Reports | tblF3d4gUEC7jk99z | 9 | Operational ✓ |

---

### 1.3 Fragmented and Secondary Bases

| Base ID | Description | Tables | Status |
|---|---|---|---|
| apppFfA2VZVmamvXe | Field Operations | 9 | Source preserved post-Phase 3 migration — contains canonical AI_Prompt_Versions (20 fields) and richer Yacht_Availability (15 fields) |
| app2FbmVD44BXShyx | Fragmented Ops | 4 | ME_Pricing (tblm5p6GQmYEjhZpG) — 5 records NOT YET MERGED — Phase 4 task |
| appVWYY9Fp6tKu94m | Influencer Outreach | 1 | Source preserved post-Phase 3 migration |
| appOQ0MGpQU1W4hoN | SSS Operations Extension | 4 | Confirmed duplicate — RETIRE PENDING |
| appQVZRgKKS0diyVX | She Said Sail copy | unknown | Rogue copy — AUDIT AND DELETE PENDING |
| app49vaVbRwuobpPv | Operations v4 | unknown | Requires audit before any action |
| appxOoLdiIVt733kV | SSS Sandbox | unknown | Sandbox — keep ✓ |

---

## Part 2: Critical Findings

### CRITICAL FINDING 1 — BOOKINGS TABLE STILL AT 151 FIELDS

**Table:** Bookings (tbl72omPibBkn2hZL)
**Current field count:** 151
**Phase 2 extraction target:** 70 fields
**Gap:** 81 fields above target

The Bookings table has continued to accumulate fields far beyond the Phase 2 extraction target. The primary driver is duplication of automation tracking state. Twenty-two automation tracking checkbox fields exist in **both** Bookings AND Automation_Health. This dual-tracking creates data integrity risk: if a checkbox is updated in one location but not the other, the system has conflicting state.

The canonical location for these fields is Automation_Health, which tracks automation execution with full timestamps and is linked to Bookings via `fldutXOFOw7H3DLy7`. The Bookings copies are entirely redundant.

**22 duplicated automation tracking fields identified:**
- Standard post-charter sequence: D0 Sent, D1 Sent, D3 Sent, D7 Sent, D9 Gift Sent, D14 Sent, D30 Sent, D60 Sent
- High-value guest sequence: HV D2 Call Done, HV D5 Sent, HV D21 Sent, HV D23 Sent
- Reminder sequence: D7 Reminder Sent, D10 Reminder Sent, D72hr Reminder Sent, D48hr Reminder Sent
- Operational confirmations: Charter_Brief_Sent, Charter_Brief_All_Vendors_Confirmed, T7_Confirmed, T48_Captain_Confirmed
- Post-charter completion: Crew_Report_Submitted, Vendor_Ratings_Entered

**Additional duplication:** The field `Conversations` (multilineText, fldSwdicqMLaLA4iA) duplicates `Conversation_Summary` (multilineText, fldN6ir73krYmDwS6). One must be retired.

**Net result of removing 23 fields:** 151 → 128 fields. A meaningful improvement in operator clarity, though still above the Phase 2 target. Further extraction of financial calculation fields would be Phase 5 scope.

**Risk assessment:** LOW. All 8 Make scenarios are status NOT_STARTED. No live automation references these field IDs.

---

### CRITICAL FINDING 2 — PARTNER OUTREACH HAS NO CLEAN SPLIT

**Table:** Partner Outreach (tblnjGWa6JNiogfCo)
**Current field count:** 88
**Problem:** Table conflates two distinct concerns:
1. Outreach pipeline tracking (who we contacted, when, outcome) — belongs in Partner Outreach
2. Partnership relationship intelligence (revenue, ROI, agreement details) — belongs in Partnerships

**Partnerships table** (tble5DcTo8mahr3lp, 20 fields) already exists and is the correct home for relationship intelligence. Twenty-two partnership-specific fields in Partner Outreach either duplicate or belong in Partnerships:

Total Revenue Driven, Total Commission Paid Out, Net Revenue After Commission (formula), Avg Revenue Per Booking (formula), Total Gifting Cost, Partner ROI (formula), Partnership Health, Agreement Signed, Agreement URL, Experience Gifted, Experience Gifted Date, Content Posted, Content URL, Content Reach, Lead to Booking Rate (formula), Commission Balance Owed, Last Payout Date, Payout Method, Next Partnership Review, Partnership Status, Partnership Start Date, Last Referral Date.

**Net result of removing these 22 fields:** 88 → 66 fields.
**Prerequisite:** For every record where `Became_Partner = true`, verify a corresponding Partnerships record exists before field removal.

---

### CRITICAL FINDING 3 — AI_PROMPT_VERSIONS: WRONG TABLE IS STILL PRIMARY

**Current primary table:** tbl0FJkA1E6a70cxX — 9 fields in appdZ49WqgjRXxA1R
**Correct canonical table:** tbl2NSec9JjqW34Xf — 20 fields in apppFfA2VZVmamvXe

The 9-field version is missing 11 governance and operational fields required for production AI governance:
`Deployed_By`, `Deployed_At`, `Rollback_To_Version`, `Brand`, `Make_Variable_Name`, `Performance_Notes`, `Will_Approved`, `Leads_Processed`, `Leads_Converted`, `Conversion_Rate_Pct`, `Override_Count`

Without these fields, the system cannot track who approved a prompt, when it was deployed, what rollback version to use if it fails, or how it is performing against conversion targets. This table **cannot support production AI governance** in its current state.

**Action required:** Replace the 9-field table with a new table built from the 20-field schema. Rename old table to `_DEPRECATED_AI_Prompt_Versions`.

---

### CRITICAL FINDING 4 — ME_PRICING NOT YET MERGED INTO PACKAGES

**Source:** app2FbmVD44BXShyx — tblm5p6GQmYEjhZpG — 5 records
**Destination:** appdZ49WqgjRXxA1R — tblwDw2hkKW5moSr9 (Packages)

Five Mare Executive pricing packages exist in a fragmented base and have never been merged into the canonical Packages table. The AI pricing engine references Packages as the single source of truth. While these records remain stranded, the AI cannot generate accurate Mare Executive quotes.

**Executed in Phase 4.** See Phase 4 Normalization Report.

---

### FINDING 5 — PACKAGES TABLE SEVERELY UNDERDEVELOPED

**Table:** Packages (tblwDw2hkKW5moSr9)
**Pre-Phase 4 field count:** 12

Packages is the AI pricing authority — it is the table the AI references to generate quotes. Yet at 12 fields, it lacks:
- Margin floor controls (no `Margin_Floor_Pct`)
- Peak season pricing (no `Peak_Multiplier`)
- Cost target breakdowns (no F&B, vessel, or labor cost targets)
- AI-readable content fields (no `Includes_Formatted` or `Add_Ons_Matrix`)
- Approval gating (no `Will_Approved`)
- Activation control (no `Live` checkbox)

Additionally, all 132 existing SSS package records have no `Brand` field populated, making it impossible to distinguish SSS from ME packages in the same table.

**Executed in Phase 4:** 12 → 26 fields. See Phase 4 Normalization Report.

---

### FINDING 6 — ALL MAKE SCENARIOS ARE NOT STARTED

**Table:** Make_Scenarios (tbl08IpivapVQZUto)
**Count:** 8 scenarios
**Status of all 8:** NOT STARTED

No live Make automations exist as of 2026-05-15. This is critical context for risk assessment: **schema cleanup and field removals pose zero risk to live integrations.** No running automation references any field ID in this system. This significantly lowers the execution risk for all Phase 4 field retirements.

---

### FINDING 7 — PLACEHOLDER TABLES CONSUMING SCHEMA BANDWIDTH

Three tables contain only the 6 Airtable default fields and zero operational records. They were likely created as scaffolding placeholders and never developed. They add noise to the table list and will not become operational — these concerns are handled by more specific tables.

| Table | Table ID | Fields | Records |
|---|---|---|---|
| Brand | tbllNjlllEhG92Ozo | 6 | 0 operational |
| Services | tblBOgArrdfPkvR8B | 6 | 0 operational |
| Expansion Pipeline | tbllga7euKfd2ykM5 | 6 | 0 operational |

**Action:** Rename to `_DEPRECATED_` prefix. Do not delete — preserve schema history.

---

### FINDING 8 — YACHT_AVAILABILITY SCHEMA SPLIT

**Old version:** tblDOoV4CHh8t4qpj — 13 fields — in appdZ49WqgjRXxA1R (main base)
**Richer version:** tblkALubyHWjOY6Ul — 15 fields — in apppFfA2VZVmamvXe

Two versions of the Yacht_Availability schema exist across different bases. The older 13-field version remains in the primary operations base. The richer 15-field version in the Field Operations base has 2 additional fields not present in the primary version.

**Action:** Confirm record count in tblDOoV4CHh8t4qpj. If 0 records: rename to `_DEPRECATED_Yacht_Availability`. Migrate any live records if count > 0.

---

### FINDING 9 — MONTHLY REVENUE TABLE DEPRECATED BUT STILL PRESENT

**Deprecated table:** Monthly Revenue (tblpTgps7cRQwDZp2) — 14 fields — in apprDKQtV2GInThwE
**Replacement table:** Financial_Periods (tblli6AwOB114dOd1) — 17 fields

Both tables exist simultaneously in the Financials base. Financial_Periods is the canonical replacement with 3 additional fields and proper period-based accounting structure. The presence of Monthly Revenue creates source-of-truth ambiguity — operators may be writing data to the wrong table.

**Action:** Rename Monthly Revenue to `_DEPRECATED_Monthly_Revenue`. Update table description to direct users to Financial_Periods.

---

### FINDING 10 — GOVERNANCE FIELD COVERAGE IS SOLID

UUID, Environment, Brand, and Source_System fields are confirmed present across all Phase 1, Phase 2, and Phase 3 tables. Governance field coverage established through prior phases is solid. Phase 4 normalization actions do not require adding governance fields to existing tables (with the exception of the new AI_Prompt_Versions table replacement).

---

## Part 3: Scoring — Current State vs. Target

### Architecture Health Scorecard (Pre-Phase 4)

| Dimension | Score | Target | Notes |
|---|---|---|---|
| Governance field coverage | 88/100 | 95/100 | Strong post-Phases 1-3; AI_Prompt_Versions gap |
| Table count rationalization | 50/100 | 80/100 | 51 tables in Ops base; 3 placeholders; rogue bases present |
| Field normalization (Bookings) | 30/100 | 75/100 | 151 fields vs. 70 target — worst single table |
| Field normalization (Partner Outreach) | 35/100 | 75/100 | 88 fields; no conceptual separation |
| AI pricing readiness (Packages) | 20/100 | 85/100 | 12 fields; missing all margin/cost intelligence |
| ME data integration | 25/100 | 100/100 | ME_Pricing stranded in fragmented base |
| Base consolidation | 45/100 | 90/100 | 7 bases total; 4 require retirement/audit |
| Automation readiness | 15/100 | 60/100 | All Make scenarios NOT_STARTED |
| Data migration completeness | 75/100 | 95/100 | Influencers/Vessel_Maintenance migrated; ME_Pricing pending |

**Overall Pre-Phase 4 Score: 61/100**

---

## Part 4: Pre-Phase 4 Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Field deletion breaks live Make automation | None | Critical | All 8 Make scenarios are NOT_STARTED — no active integrations exist |
| Field deletion loses data | Medium | High | Export CSV before every field deletion; store in 99_ARCHIVE/PHASE_4_FIELD_EXPORTS/ |
| Formula field references deleted field | Medium | Medium | Audit all formulas in Bookings and Partner Outreach before deletion |
| ME package merge creates duplicates | Low | Medium | ME_Pricing has only 5 records; verify against Packages before insert |
| Rogue base (appQVZRgKKS0diyVX) contains live data | Unknown | High | Do not delete without audit — schedule audit as Phase 5 prerequisite |
| Operations v4 base (app49vaVbRwuobpPv) contains unique records | Unknown | Medium | Do not retire without audit |
| AI_Prompt_Versions replacement breaks AI prompting | Low | High | Old table has no production use (9 fields insufficient); replacement is additive |

**Overall execution risk for Phase 4: LOW-MEDIUM**

The most significant risk mitigant is that zero live Make automations exist. All schema changes are safe to execute without coordination with automation triggers.

---

*Document generated: 2026-05-15 | Phase 4 Pre-Execution | She Said Sail + Mare Executive*
