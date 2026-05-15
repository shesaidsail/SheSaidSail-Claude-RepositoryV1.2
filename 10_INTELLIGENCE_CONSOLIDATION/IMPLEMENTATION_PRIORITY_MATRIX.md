# IMPLEMENTATION PRIORITY MATRIX
## She Said Sail + Mare Executive — System Priority Classification

**Document ID:** IMPLEMENTATION_PRIORITY_MATRIX
**Status:** CONSOLIDATION AUTHORITY
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## CLASSIFICATION KEY

| Class | Definition |
|-------|-----------|
| **CRITICAL NOW** | Must exist before Phase 4 begins. Blocking dependency. |
| **PHASE 4** | High ROI, build in Phase 4 after Phase 3 complete. |
| **FUTURE SCALE** | Justified at 3+ cities or 200+ bookings/month. |
| **OPTIONAL** | Nice to have. Low operational leverage. |
| **OVERENGINEERED** | Complexity exceeds value at current scale. |
| **ELIMINATE** | Remove from architecture entirely. |

---

## SECTION 1 — TABLE PRIORITY

| Table | Priority | ROI Rationale |
|-------|---------|--------------|
| **Requests (optimized)** | CRITICAL NOW | Phase 2 inbound agent blocked without autonomy fields |
| **Bookings (optimized, reduced to 70 fields)** | CRITICAL NOW | Every Make scenario depends on Bookings |
| **Clients (optimized + intelligence fields)** | CRITICAL NOW | Context injection for every client interaction |
| **Packages (rebuilt, 25+ fields)** | CRITICAL NOW | AI cannot quote pricing without this; margin floor enforcement blocked |
| **AI_Prompt_Versions (26-field schema)** | CRITICAL NOW | Prompt rollback governance blocked without correct schema |
| **Audit Log (expanded)** | CRITICAL NOW | Every Tier A action requires audit record — currently incomplete |
| **Lessons (optimized per LESSONS_ENGINE_SPEC)** | CRITICAL NOW | Institutional intelligence; AI quality compounds from day 1 |
| **Automation_Health** | CRITICAL NOW | Field extraction from Bookings removes 20 send-state fields from core table |
| **Emergency_Escalations (migrated)** | CRITICAL NOW | Emergency governance requires this table |
| **Cybersecurity_Incidents** | CRITICAL NOW | Governance requirement — no audit trail for security events |
| **Incapacitation_Actions** | CRITICAL NOW | Governance requirement — Luciana authority framework |
| **Financial_Periods** | CRITICAL NOW | Monthly close workflow blocked without this |
| **Chart_of_Accounts** | CRITICAL NOW | Financial OS requires this before any accounting integration |
| **Entity_Registry** | CRITICAL NOW | Legal and financial backbone — acquisition readiness |
| **Expenses** | CRITICAL NOW | Financial OS requirement — no expense tracking without it |
| **Contractors** | CRITICAL NOW | Payout architecture blocked without this |
| **Governance_Reviews** | CRITICAL NOW | Governance compliance requires formal review history |
| **Creative_Assets** | PHASE 4 | High ROI — enables content performance intelligence and pattern recognition |
| **Revenue_Snapshots** | PHASE 4 | Required for Revenue Health Score — highest-leverage intelligence card |
| **Demand_Signals** | PHASE 4 | Pricing intelligence blocked without demand time-series |
| **Pricing_Recommendations** | PHASE 4 | Founder pricing review surface — directly affects margin |
| **Yield_Log** | PHASE 4 | Required for yield recommendation audit trail |
| **Make_Scenarios (registry)** | PHASE 4 | Needed before HEALTH-001 implementation; low priority until Phase 4 orchestrators are built |
| **Campaign_Creatives** | FUTURE SCALE | Justified when running 3+ paid campaigns/week simultaneously |
| **Creative_Fatigue** | FUTURE SCALE | Justified when creative volume creates genuine fatigue risk |
| **Cash_Flow_Forecast** | FUTURE SCALE | Justified after 6+ months of Financial_Periods data |
| **Investor_Reports** | FUTURE SCALE | Build during acquisition readiness prep |
| **AI_Audit (standalone)** | ELIMINATE | Merged into Audit_Log |
| **Client_LTV_Scores (standalone)** | ELIMINATE | Fields on Clients |
| **Relationship_Scores (standalone)** | ELIMINATE | Fields on Clients + Partner_Outreach |
| **Referral_Network (standalone)** | ELIMINATE | Fields on Affiliates |
| **Offer_Performance (standalone)** | ELIMINATE | Fields on Packages |
| **Creative_Scoring (standalone)** | ELIMINATE | Fields on Creative_Assets |
| **Winning_Creatives (standalone)** | ELIMINATE | View of Creative_Assets |

---

## SECTION 2 — MAKE SCENARIO PRIORITY

| Scenario | Priority | Rationale |
|----------|---------|-----------|
| **EMERGENCY-001** | CRITICAL NOW | Safety — zero tolerance for failure |
| **AUDIT-001** | CRITICAL NOW | Governance — every Tier A action requires this |
| **HEALTH-001** | CRITICAL NOW | System integrity — automation failure detection |
| **BACKUP-001** | CRITICAL NOW | Data protection — irreplaceable operational data |
| **INBOUND-MASTER** | CRITICAL NOW | Phase 2 agent — first revenue-generating automation |
| **BOOKING-MASTER** | CRITICAL NOW | Core booking lifecycle — payment and confirmation |
| **CHARTER-MASTER** | CRITICAL NOW | D7 review requests are highest-leverage marketing action |
| **FINANCIAL-MASTER** | CRITICAL NOW | Financial period close, payout alerts, fraud detection |
| **INTELLIGENCE-MASTER (basic)** | CRITICAL NOW | Thursday Digest — founder weekly intelligence |
| **CREATIVE-MASTER** | PHASE 4 | High ROI — creative tagging and winner identification |
| **INTELLIGENCE-MASTER (enhanced)** | PHASE 4 | Full Thursday Digest with all intelligence sections |
| **OUTREACH-MASTER** | PHASE 4 | Planner outreach — Phase 4 agent scope |

---

## SECTION 3 — INTELLIGENCE MODULE PRIORITY

| Module | Priority | ROI Rationale |
|--------|---------|--------------|
| **Lessons Engine** | CRITICAL NOW | Every AI interaction quality compounds from lessons. Highest ROI of all intelligence systems. |
| **Audit + AI Governance** | CRITICAL NOW | Governance compliance; without audit logging all Tier A is ungoverned. |
| **Thursday Digest** | CRITICAL NOW | Single founder touchpoint — saves 30+ minutes/week of manual intelligence gathering. |
| **Revenue Health Score** | PHASE 4 | Single most important intelligence metric — tells founder if business is healthy. |
| **Client LTV Scoring** | PHASE 4 | Directly informs relationship priority — high leverage on repeat booking rate. |
| **Demand Intelligence** | PHASE 4 | Pricing recommendations require demand context. Direct margin impact. |
| **Creative Asset Intelligence** | PHASE 4 | Pattern recognition for creative — compounds over time. |
| **Yield Management** | PHASE 4 | Rate optimization — direct revenue impact. Implement after 6+ months of demand data. |
| **Pricing Recommendations** | PHASE 4 | Operational — founder reviews before any rate change. |
| **Relationship Depth Scoring** | PHASE 4 | Informs HV client management and planner outreach prioritization. |
| **Referral Quality Scoring** | PHASE 4 | Informs affiliate relationship investment decisions. |
| **Content ROI Attribution** | FUTURE SCALE | Requires Meta/TikTok API integration (Phase 4 pending) + 6+ months of data. |
| **Risk Intelligence scoring** | PHASE 4 | Risk fields on Bookings protect against financial integrity events. |
| **Confidence Calibration Tracking** | OPTIONAL | Useful signal but Luciana's weekly review is sufficient at current AI scale. Formal calibration tracking deferred. |
| **Adaptive SOP Engine** | ELIMINATE (standalone) | Collapsed into Lessons Engine SOP category. |
| **Campaign_Creatives deployment tracking** | FUTURE SCALE | Needed at 5+ campaigns/week. |
| **Creative Fatigue detection** | FUTURE SCALE | Needed when running 5+ creatives simultaneously with paid budget. |
| **Offer Intelligence Module** | OPTIONAL | Attach rate on Packages table is sufficient insight at current scale. |
| **Multi-entity financial consolidation** | FUTURE SCALE | Required at 3+ legal entities or when investor reporting begins. |

---

## SECTION 4 — ROI CLASSIFICATION BY REVENUE IMPACT

### Tier 1 — Direct Revenue Impact (highest ROI)

| System | Revenue Impact | Time to Value |
|--------|--------------|--------------|
| Lessons Engine | Prevents repeat operational failures; AI quality compounds → better close rates | Immediate |
| Inbound Response Agent (INBOUND-MASTER) | Sub-2-minute response → estimated 15–25% close rate improvement | Phase 2 |
| D7 Review Request (CHARTER-MASTER) | Reviews → organic reach → new leads | Existing |
| Revenue Health Score | Identifies margin erosion before it compounds | Phase 4 |
| Demand Intelligence | Prevents underpricing during surge windows | Phase 4 |
| Client LTV Scoring | Prioritizes retention of highest-value relationships | Phase 4 |

### Tier 2 — Margin Protection (high ROI, prevents loss)

| System | Protection | Time to Value |
|--------|-----------|--------------|
| Anomaly Detection (enhanced) | Prevents fraud, duplicate payouts, unauthorized discounts | Phase 3 |
| Pricing Recommendations | Prevents underpricing; flags when demand warrants rate increase | Phase 4 |
| Risk Intelligence on Bookings | Early warning on high-risk bookings → proactive intervention | Phase 4 |
| Creative Fatigue detection | Prevents ROAS degradation from tired creatives | Phase 5 |

### Tier 3 — Operational Efficiency (medium ROI)

| System | Efficiency | Time to Value |
|--------|-----------|--------------|
| AI Governance (in Audit_Log) | Prevents AI drift from compounding into client-facing errors | Phase 3 |
| Automation Health table | Removes 20 fields from Bookings → faster API calls | Phase 3 |
| Thursday Digest (unified) | Reduces founder information-gathering from 30 min → 5 min/week | Phase 4 |
| Creative Asset Intelligence | Reduces creative briefing time; improves next campaign quality | Phase 4 |

### Tier 4 — Infrastructure + Compliance (necessary but not revenue-driving)

| System | Purpose | Time to Value |
|--------|---------|--------------|
| Financial_Periods + Chart_of_Accounts | Accounting compliance + acquisition readiness | Phase 3 |
| Entity_Registry | Legal backbone for multi-entity operation | Phase 3 |
| Governance_Reviews | Compliance audit trail | Phase 3 |
| Cybersecurity_Incidents | Incident response governance | Phase 3 |
| Backup + Health monitoring | Data protection and system integrity | Phase 3 (existing) |

---

## SECTION 5 — BUILD-vs-BUY DECISION: WHAT GOES IN MAKE vs. AIRTABLE

| Function | Where It Lives | Rationale |
|----------|--------------|-----------|
| LTV_Score computation | **Make** (weekly compute) + Airtable field storage | Requires reading multiple Bookings records and applying formula logic |
| Relationship_Score computation | **Make** (weekly) + Airtable field storage | Requires reading interaction history across tables |
| Demand_Score computation | **Make** (weekly) + Demand_Signals record | Aggregates across multiple signals from multiple tables |
| Revenue Health Score | **Make** (weekly) + Revenue_Snapshots record | Multi-table aggregation |
| Creative Performance Score | **Make** (weekly) + Creative_Assets field | Pulls from Organic_Content and Paid_Ads performance data |
| Risk Score | **Make** (weekly) + Bookings field | Rule-based scoring from multiple risk flags |
| D7_Review_Eligible | **Airtable formula** | Simple Boolean logic from existing fields — no Make needed |
| Net_Margin_Pct | **Airtable formula** | Direct arithmetic from existing fields |
| LTV_Tier | **Airtable formula** | Derived from LTV_Score field — no Make needed |
| Risk_Tier | **Airtable formula** | Derived from Risk_Score field — no Make needed |
| Winner_Status view | **Airtable view** | Filter on Winner_Status field — no Make, no separate table |
| Fatigue detection alerts | **Make** (weekly in CREATIVE-MASTER) | Requires trend comparison across weeks |

---

## SECTION 6 — IMPLEMENTATION SEQUENCING

No Phase 4 intelligence work begins until the Phase 3 gate is cleared.

### Phase 3 Gate Criteria (required to proceed to Phase 4)

| Gate Item | Status Needed | Owner |
|-----------|-------------|-------|
| All Phase 3 tables migrated or created | 100% complete | Will + technical operator |
| Bookings table reduced to <70 fields | Confirmed | Will |
| All Make-readiness blockers resolved (Section 4 of Build Spec) | All 9 blockers clear | Will + technical operator |
| Sandbox base exists and is isolated from production | Confirmed | Will |
| All native Airtable automations inventoried | Documented | Will |
| Packages table rebuilt (25+ fields) | Confirmed | Will |
| AI_Prompt_Versions migrated (26-field schema) | Confirmed | Will |
| Environment field on all production tables | Confirmed | Will |
| Idempotency_Key on Bookings | Confirmed | Will |
| All fragmented bases retired (Phases 0–5 of Build Spec) | Confirmed | Will |
| Stripe webhook configuration documented | Documented | Will |
| Architecture decisions resolved (Section 6.6 of Build Spec) | Will decisions recorded | Will |

Only when ALL gate criteria are met does Phase 4 begin.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*IMPLEMENTATION_PRIORITY_MATRIX v1.0*
*Effective May 2026*
