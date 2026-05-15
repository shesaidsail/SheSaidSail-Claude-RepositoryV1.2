# TABLE CONSOLIDATION RECOMMENDATIONS
## She Said Sail + Mare Executive — Airtable Schema Decisions

**Document ID:** TABLE_CONSOLIDATION_RECOMMENDATIONS
**Status:** CONSOLIDATION AUTHORITY
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## SECTION 1 — DECISION FRAMEWORK

Every table recommendation follows one of five dispositions:

| Disposition | Definition |
|------------|-----------|
| **BUILD** | Create this table — it carries records that cannot live as fields on another table |
| **FIELDS** | Collapse to fields on an existing table — no separate table needed |
| **VIEW** | Convert to a filtered/sorted view of an existing table — no new table needed |
| **DEFER** | Build this in a future phase when volume or complexity justifies it |
| **ELIMINATE** | Remove entirely — no value worth the complexity cost |

**Decision criteria:**
- Does this table require time-series records (one per period)? → BUILD
- Does this table require an immutable append-only log? → BUILD
- Is this data a property of one existing record? → FIELDS
- Is this data a subset of an existing table? → VIEW
- Is this table needed for current operational scale? → DEFER if not
- Is the value less than the overhead? → ELIMINATE

---

## SECTION 2 — COMPLETE TABLE DECISION REGISTER

### 2.1 SSS Operations Base — All Tables

| Table | Disposition | Rationale | Phase |
|-------|------------|-----------|-------|
| **Requests** | KEEP + OPTIMIZE | Core ops — inbound lead pipeline | Phase 3 (current) |
| **Bookings** | KEEP + OPTIMIZE | Core ops — master booking record | Phase 3 |
| **Clients** | KEEP + OPTIMIZE + new intelligence fields | Core ops + Phase 4 LTV/relationship/risk fields | Phase 3 + Phase 4 |
| **Guests** | MIGRATE from fragmented base | Separate from Clients — group member data | Phase 3 |
| **Yachts** | KEEP + OPTIMIZE | Core ops — vessel inventory | Phase 3 |
| **Yacht_Availability** | REPLACE with richer schema | Core ops — availability calendar | Phase 3 |
| **Vessel_Maintenance** | MIGRATE | Operational safety record | Phase 3 |
| **Brokers** | KEEP + OPTIMIZE | Core ops — charter coordination | Phase 3 |
| **Vendors** | KEEP + OPTIMIZE | Core ops — supplier management | Phase 3 |
| **Packages** | REBUILD (8 → 25+ fields) + intelligence fields | Core ops + pricing intelligence + offer performance | Phase 3 + Phase 4 |
| **Cities** | KEEP + OPTIMIZE | Geographic operations | Phase 3 |
| **City_Financials** | MIGRATE | City-level P&L intelligence | Phase 3 |
| **Regional_Directors** | MIGRATE | Future-state scaling architecture | Phase 3 |
| **Concierge_Operators** | MIGRATE | Ops team records | Phase 3 |
| **Lessons** | KEEP + OPTIMIZE (per LESSONS_ENGINE_SPEC) | Institutional intelligence — critical | Phase 3 |
| **Approval Queue** | KEEP + OPTIMIZE | Founder decision architecture | Phase 3 |
| **Founder Decisions** | KEEP + OPTIMIZE | Formal decision record | Phase 3 |
| **Audit Log** | EXPAND (absorbs AI quality records) | Immutable action record — add Audit_Category | Phase 3 + Phase 4 |
| **State Transition Log** | KEEP separate | Granular state change log — different purpose from Audit Log | Phase 3 |
| **AI_Prompt_Versions** | REPLACE (9 → 26 field schema) | Prompt governance — critical for rollback | Phase 3 |
| **AI_Audit** | ELIMINATE as standalone | MERGE into Audit Log via Audit_Category field | Phase 4 (merge during expansion) |
| **Make_Scenarios** | MIGRATE | Scenario registry and dependency map | Phase 3 |
| **Automation_Health** | CREATE | Per-booking automation send state tracking | Phase 3 |
| **Governance_Reviews** | CREATE | Review history log | Phase 3 |
| **Cybersecurity_Incidents** | CREATE | Security event log | Phase 3 |
| **Incapacitation_Actions** | CREATE | Luciana interim authority log | Phase 3 |
| **Emergency_Escalations** | MIGRATE | Emergency event log | Phase 3 |
| **Emergency_Protocols** | MIGRATE | Emergency SOP reference | Phase 3 |
| **Partner Outreach** | KEEP + OPTIMIZE (84 → 45 fields) | Planner pipeline — reduced scope | Phase 3 |
| **Affiliates** | KEEP + OPTIMIZE + referral intelligence fields | Referral tracking + intelligence | Phase 3 + Phase 4 |
| **Influencers** | MIGRATE | Creator management | Phase 3 |
| **Organic Content** | KEEP + OPTIMIZE + creative intelligence fields | Content performance + creative intel | Phase 3 + Phase 4 |
| **Paid Ads** | KEEP + OPTIMIZE + creative attribution fields | Ad intelligence + creative intel | Phase 3 + Phase 4 |
| **Creative_Assets** | BUILD (Phase 4) | Master creative asset library — no existing equivalent | Phase 4 |
| **Copy/Creative_Assets** | EVALUATE for merge | Assess overlap with new Creative_Assets table | Phase 3 decision |
| **Website/Landing Page** | KEEP | Solid schema — no changes needed | Phase 3 |
| **Google Reviews** | KEEP | Review tracking — confirmed solid | Phase 3 |
| **Calls Recommended** | KEEP | Relationship intelligence trigger surface | Phase 3 |
| **Dashboard Notes** | KEEP | Internal ops notes | Phase 3 |
| **Conversations** | KEEP + OPTIMIZE | Communication history | Phase 3 |
| **Expenses** | CREATE | Financial ops — expense tracking | Phase 3 |
| **Contractors** | CREATE | Contractor records and payouts | Phase 3 |
| **Team_Members** | CREATE | Staff directory | Phase 3 |
| **Campaign_Creatives** | DEFER to Phase 5 | Premature at current creative volume; Organic_Content + Paid_Ads cover this | Phase 5 |
| **Creative_Scoring** | ELIMINATE as table | Fields on Creative_Assets — Performance_Score, Score_Tier | Eliminated |
| **Winning_Creatives** | CONVERT TO VIEW | Filtered view of Creative_Assets (Winner_Status = true, Will_Approved = true) | Phase 4 (view creation) |
| **Creative_Fatigue** | DEFER to Phase 5 | Fatigue fields on Campaign_Creatives when built | Phase 5 |
| **Client_LTV_Scores** | ELIMINATE as table → FIELDS | LTV_Score, LTV_Tier, Churn_Risk fields on Clients | Phase 4 |
| **Relationship_Scores** | ELIMINATE as table → FIELDS | Relationship_Score on Clients; Relationship_Depth_Score on Partner_Outreach | Phase 4 |
| **Referral_Network** | ELIMINATE as table → FIELDS | Referral_Quality_Score, Revenue_Generated_LTD, Referral_Velocity on Affiliates | Phase 4 |
| **Offer_Performance** | ELIMINATE as table → FIELDS | Margin_Score, Attach_Rate_Pct, Performance_Tier on Packages | Phase 4 |
| **Revenue_Snapshots** | BUILD (Phase 4) | Weekly time-series — requires standalone records, cannot be fields | Phase 4 |
| **Demand_Signals** | BUILD (Phase 4) | Weekly time-series — requires standalone records | Phase 4 |
| **Pricing_Recommendations** | BUILD (Phase 4) | Immutable recommendation log — audit trail for pricing decisions | Phase 4 |
| **Yield_Log** | BUILD (Phase 4) | Immutable yield record — rate decision audit | Phase 4 |

### 2.2 SSS Financials Base — All Tables

| Table | Disposition | Rationale | Phase |
|-------|------------|-----------|-------|
| **P&L Per Charter** | RESTRUCTURE | Core financial intelligence — Booking_ID stays as singleLineText with sync validation | Phase 3 |
| **Financial_Periods** | CREATE (replaces Monthly Revenue) | Monthly period close workflow — full spec per Systems_Intelligence_Architecture | Phase 3 |
| **Payouts** | OPTIMIZE | Add Founder Decision link, approval gate | Phase 3 |
| **Tax Tracker** | KEEP | Correct schema — no changes | Phase 3 |
| **Chart_of_Accounts** | CREATE | Financial structure backbone | Phase 3 |
| **Entity_Registry** | CREATE | Legal entity and financial backbone | Phase 3 |
| **Expenses** | MOVE HERE from Operations | Belongs in financial base for accounting separation | Phase 3 |
| **Cash_Flow_Forecast** | DEFER to Phase 5 | Premature — requires 6+ months of Financial_Periods data to model | Phase 5 |
| **Investor_Reports** | DEFER to Phase 5 | Acquisition readiness prep — not needed until investment process begins | Phase 5 |
| **Monthly Revenue (old)** | RETIRE | Replaced by Financial_Periods | Phase 3 |

---

## SECTION 3 — INTELLIGENCE FIELDS SPECIFICATION

### 3.1 Clients Table — Phase 4 Intelligence Fields to Add

| Field | Type | Purpose | Computed By |
|-------|------|---------|------------|
| LTV_Score | Number (0–100) | Composite lifetime value score | Make weekly |
| LTV_Tier | Formula | PLATINUM / GOLD / SILVER / STANDARD | Airtable formula from LTV_Score |
| Relationship_Score | Number (0–100) | Depth of relationship beyond transactions | Make weekly |
| Churn_Risk | Single Select | LOW / MEDIUM / HIGH / CRITICAL | Make weekly |
| Client_Risk_Score | Number (0–100) | Combined risk indicator | Make weekly |
| Referral_Quality_Score | Number (0–100) | Quality and revenue of referrals sent | Make monthly |
| Next_Booking_Probability | Number (0–100) | AI-assessed rebooking likelihood | Make monthly |
| VIP_Flag | Checkbox | High-value designation — Will-only modification | Manual |
| Days_Since_Last_Charter | Formula | DATETIME_DIFF(TODAY(), last charter date, 'days') | Airtable formula |
| Total_Revenue_LTD | Rollup | SUM of Gross_Revenue from linked Bookings (Completed) | Airtable rollup |
| Booking_Count | Count | COUNT of linked Bookings (Completed) | Airtable count |
| Intelligence_Last_Updated | DateTime | Last time LTV/relationship scores were refreshed | Make (auto) |

### 3.2 Packages Table — Phase 4 Intelligence Fields to Add

| Field | Type | Purpose | Computed By |
|-------|------|---------|------------|
| Margin_Score | Number (0–100) | Normalized margin health vs. portfolio | Make weekly |
| Attach_Rate_Pct | Number | % of bookings with add-ons | Airtable formula |
| Performance_Tier | Formula | A / B / C / D based on Bookings_Count + Margin_Score | Airtable formula |
| Bookings_Count_LTD | Count | Total confirmed bookings using this package | Airtable count |
| Avg_Margin_Achieved | Rollup | Average actual margin from linked Bookings | Airtable rollup |
| Revenue_Contribution_Pct | Formula | This package's % of total portfolio revenue | Airtable formula |
| Recommended_Multiplier | Number | AI-suggested rate multiplier (pending Will review) | Make (Pricing_Recommendations module) |

### 3.3 Affiliates Table — Phase 4 Intelligence Fields to Add

| Field | Type | Purpose | Computed By |
|-------|------|---------|------------|
| Referral_Quality_Score | Number (0–100) | Revenue quality and conversion of referrals | Make monthly |
| Revenue_Generated_LTD | Rollup | Total revenue from bookings linked to this affiliate | Airtable rollup |
| Avg_Booking_Value | Rollup | Average booking value for affiliated bookings | Airtable rollup |
| Referral_Velocity | Formula | Referrals per 90 days | Airtable formula |
| Network_Depth | Number | Number of affiliate-to-affiliate connections | Make monthly |

### 3.4 Bookings Table — Phase 4 Risk Fields to Add

| Field | Type | Purpose | Computed By |
|-------|------|---------|------------|
| Risk_Score | Number (0–100) | Combined booking risk indicator | Make weekly |
| Risk_Tier | Formula | RED (<40) / ORANGE (40–60) / YELLOW (60–80) / GREEN (>80) | Airtable formula |
| Risk_Flags | Multiple Select | CHARGEBACK_HISTORY / HV_DISSATISFIED / LATE_PAYMENT / VENDOR_UNRELIABLE / WEATHER_WINDOW | Make (auto-flag) |
| Yield_Score | Number (0–100) | Margin achieved vs. city benchmark | Make post-completion |
| Upsell_Revenue | Currency | Revenue from add-ons on this booking | Airtable formula |
| Offer_Source | Single Select | DIRECT / UPSELL_D1 / UPSELL_D30 / PLANNER / AFFILIATE | Make (auto) |

### 3.5 Audit Log — Phase 4 Intelligence Fields to Add

| Field | Type | Purpose |
|-------|------|---------|
| Audit_Category | Single Select | AI_ACTION / AI_QUALITY_REVIEW / OPERATIONAL / FINANCIAL / SYSTEM / EMERGENCY |
| AI_Quality_Finding | Long Text | For AI_QUALITY_REVIEW records: Luciana's review notes |
| Quality_Reviewer | Single Select | Will / Luciana / System — for quality review records only |

---

## SECTION 4 — TABLES BY PHASE

### Phase 3 Target (all migration + optimization work)

**SSS Operations — Phase 3 final state:** 32 tables  
**SSS Financials — Phase 3 final state:** 7 tables  
**Total Phase 3 target:** 39 tables

### Phase 4 Target (intelligence layer additions)

New tables added in Phase 4:
- Creative_Assets (+1 to Operations)
- Revenue_Snapshots (+1 to Operations)
- Demand_Signals (+1 to Operations)
- Pricing_Recommendations (+1 to Operations)
- Yield_Log (+1 to Operations)

**SSS Operations — Phase 4 ceiling:** 37 tables  
**SSS Financials — Phase 4 ceiling:** 7 tables  
**Total Phase 4 ceiling:** 44 tables

### Phase 5 Target (when volume justifies)

New tables deferred to Phase 5:
- Campaign_Creatives
- Creative_Fatigue
- Cash_Flow_Forecast (Financials)
- Investor_Reports (Financials)

**Phase 5 ceiling:** ~48 tables total (still well below the 61-table sprawl the draft architecture would have produced)

---

## SECTION 5 — VIEWS TO CREATE (not tables)

| View Name | Parent Table | Filter/Sort | Purpose |
|-----------|-------------|------------|---------|
| Winning Creatives | Creative_Assets | Winner_Status = true AND Will_Approved = true | Hall of fame — no separate table needed |
| Active Lessons | Lessons | Status = Active OR Applied OR Tested | AI context candidate list |
| Pending Founder Review | Lessons | Status = Pending Review | Will's weekly review queue |
| Revenue Intelligence Cards | Revenue_Snapshots | Most recent week, all cities | Dashboard card data source |
| Demand Surge Windows | Demand_Signals | Demand_Score > 75 | Active surge periods |
| HV Client Watch | Clients | VIP_Flag = true OR LTV_Tier = PLATINUM | High-value relationship monitoring |
| Package Performance | Packages | Sorted by Performance_Tier descending | Offer optimization view |
| Fatigue Watch | Paid_Ads | Creative_Fatigue_Flag = true | Asset rotation candidates |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*TABLE_CONSOLIDATION_RECOMMENDATIONS v1.0*
*Effective May 2026*
