# REVENUE INTELLIGENCE IMPLEMENTATION ROADMAP
**Document ID:** 10_REVENUE__REVENUE_IMPLEMENTATION_ROADMAP_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

This roadmap defines the phased implementation sequence for the Revenue + Relationship Intelligence Layer. It establishes dependencies, build priorities, and success metrics for each phase. No phase should be built before its prerequisites are complete.

**Implementation Prerequisite:** The Airtable consolidation described in `02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md` must be at least 70% complete before Phase 1 of this roadmap begins. Intelligence built on fragmented data produces unreliable signals.

---

## SECTION 2: PHASE OVERVIEW

| Phase | Name | Duration | Primary Deliverable |
|---|---|---|---|
| Phase 1 | Data Foundation | 3–4 weeks | New tables, field extensions, clean data baseline |
| Phase 2 | LTV + Relationship Intelligence | 4–5 weeks | LTV scores, relationship scores, churn alerts live |
| Phase 3 | Pricing + Yield Intelligence | 4–5 weeks | Pricing recommendations in Approval Queue, yield log active |
| Phase 4 | Referral + Offer Intelligence | 3–4 weeks | Referral network mapped, offer performance tracking live |
| Phase 5 | Revenue Dashboards + Alerts | 2–3 weeks | Founder Dashboard intelligence cards, weekly digest automated |
| Phase 6 | Intelligence Compounding | Ongoing | Models improve via outcome tracking, annual recalibration |

**Total Time to Full Intelligence Layer:** 16–21 weeks from start

---

## SECTION 3: PHASE 1 — DATA FOUNDATION

**Duration:** 3–4 weeks
**Owner:** Luciana (data operations) + System Administrator

### Objective
Establish the clean data infrastructure that all intelligence modules depend on. No intelligence is accurate without clean, complete, consistently structured data.

### Tasks

**1.1 Airtable Table Creation**

Create the following new tables in SSS Operations base:
- `Revenue_Snapshots` — append-only, weekly period captures
- `Client_LTV_Scores` — one record per client per computation cycle
- `Relationship_Scores` — one record per client/partner per cycle
- `Referral_Network` — referral attribution graph
- `Offer_Performance` — one record per offer per period
- `Pricing_Recommendations` — pending/approved/denied pricing signals
- `Demand_Signals` — rolling demand metrics per city
- `Yield_Log` — rate recommendation history

**1.2 Existing Table Field Extensions**

Extend the following existing tables with new intelligence fields:

*Clients table:*
- LTV_Score, LTV_Tier, Relationship_Score, Churn_Risk, Referral_Quality_Score
- Next_Booking_Probability, VIP_Flag_Recommended, Days_Since_Last_Charter
- Lifecycle_Stage, Relationship_Milestone_Date, Re_Engagement_Due
- Referral_Network_Depth, Corporate_Account_Flag

*Bookings table:*
- Yield_Score, Demand_Window, Offer_Source, Upsell_Revenue
- Upsell_Attach_Rate, Referral_Chain_ID

*Packages table:*
- Margin_Score, Attach_Rate, Revenue_Contribution_Pct
- Performance_Tier, Recommended_Multiplier, Occasion_Affinity
- Status, Last_Reviewed_Date, Min_LTV_Tier

*Affiliates table:*
- Referral_Quality_Score, Network_Depth, Revenue_Generated_LTD, Avg_Booking_Value

*Partner_Outreach table:*
- Relationship_Depth_Score, Revenue_Attributed, Referral_Velocity

*Requests table:*
- Referral_Attribution_Confidence (upgrade existing Source field logic)

**1.3 Historical Data Backfill**

- Assign Lifecycle_Stage to all existing clients based on booking history
- Compute Realized_LTV for all clients with completed bookings
- Tag all existing Requests with Source attribution where determinable
- Assign initial Charter_Grade to historical bookings where Charter_Grade field was not populated

**1.4 UUID and Environment Governance**

- Verify all new tables have UUID, Environment, Created_At, Updated_At, Brand, City fields
- Confirm Audit_Log table linkage fields on Pricing_Recommendations and Yield_Log

### Phase 1 Success Criteria

- [ ] All 8 new tables created and field-complete
- [ ] All existing table field extensions deployed
- [ ] 90%+ of active clients have Lifecycle_Stage populated
- [ ] 90%+ of historical bookings have Source or clean UNKNOWN flag
- [ ] No orphaned records without UUID in new tables
- [ ] Sandbox environment verified separate from Production

---

## SECTION 4: PHASE 2 — LTV + RELATIONSHIP INTELLIGENCE

**Duration:** 4–5 weeks
**Owner:** System Administrator (Make/Claude) + Luciana (review + validation)

### Objective
Make the LTV Engine and Relationship Scoring live, producing weekly automated scores and actionable alerts for Luciana and Founder.

### Tasks

**2.1 Make Scenario: Weekly LTV Computation**

Scenario ID: `REV-001 LTV_Weekly_Refresh`
- Trigger: Scheduled (Sunday 11:00 PM local time)
- Action: Pull all Clients with 1+ completed booking
- Compute: Realized_LTV, Projected_LTV_12M, Composite_LTV, LTV_Tier, RFM scores, Churn_Risk, Next_Booking_Probability
- Write: New record to Client_LTV_Scores per client
- Update: LTV_Tier, Churn_Risk, Next_Booking_Probability on Clients table
- Alert: If Tier_Changed = TRUE, generate appropriate alert

**2.2 Make Scenario: Post-Booking LTV Update**

Scenario ID: `REV-002 LTV_Booking_Trigger`
- Trigger: Booking Status → COMPLETED
- Action: Recompute LTV for linked client immediately
- Update: Clients table fields
- Alert: If DIAMOND or PLATINUM client completes booking, generate relationship prompt for Luciana

**2.3 Make Scenario: Weekly Relationship Score Refresh**

Scenario ID: `REV-003 Relationship_Weekly_Refresh`
- Trigger: Scheduled (Sunday 11:30 PM)
- Action: Compute Relationship_Score for all active clients and partners
- Write: New Relationship_Scores record per client/partner
- Alert: AT_RISK clients → Luciana. CHAMPION_AT_RISK → Founder.

**2.4 Make Scenario: Lifecycle Stage Automation**

Scenario ID: `REV-004 Lifecycle_Stage_Update`
- Trigger: Booking Status → COMPLETED (any booking)
- Action: Re-evaluate client Lifecycle_Stage based on total completed bookings and referral count
- Update: Clients.Lifecycle_Stage
- Alert: Stage upgrades trigger appropriate recognition prompt

**2.5 Claude Prompt: LTV Narrative Summary**

Claude prompt added to weekly LTV computation:
- Input: Top 5 clients by Churn_Risk = CRITICAL, Tier = GOLD+
- Output: 1-paragraph plain-English narrative per client with recommended re-engagement approach
- Destination: Luciana Slack DM (Tier B — Luciana reviews before any action)

**2.6 Validation Period (2 weeks)**

Before considering Phase 2 complete:
- Luciana manually reviews 20 LTV scores against her qualitative knowledge of clients
- Any score that "feels wrong" is investigated and formula adjusted
- Relationship_Score calibration: Luciana confirms Tier 1 clients are ones she would intuitively call VIPs

### Phase 2 Success Criteria

- [ ] Weekly LTV computation running without errors for 4 consecutive weeks
- [ ] Post-booking LTV trigger firing correctly on all COMPLETED bookings
- [ ] Churn Risk alerts generating correctly (sample audit by Luciana)
- [ ] Lifecycle Stage updating correctly on booking completion
- [ ] Luciana validation: 85%+ LTV tiers feel accurate vs qualitative knowledge
- [ ] Zero DIAMOND-tier clients with undetected CRITICAL churn risk

---

## SECTION 5: PHASE 3 — PRICING + YIELD INTELLIGENCE

**Duration:** 4–5 weeks
**Owner:** System Administrator + Founder (review and calibration)

### Objective
Make pricing recommendations live in the Approval Queue, with demand signals feeding yield recommendations weekly. All recommendations require founder or Luciana review before any action.

### Tasks

**3.1 Make Scenario: Weekly Demand Signal Computation**

Scenario ID: `REV-005 Demand_Signal_Weekly`
- Trigger: Scheduled (Monday 6:00 AM)
- Action: Aggregate Requests volume, lead time, occasion distribution for each city
- Compute: Demand_Score per city per 30-day forward window
- Write: Demand_Signals table record
- Alert: If Demand_Score > 75 for 5 consecutive days → SURGE_WINDOW alert to Founder

**3.2 Make Scenario: Yield Recommendation Generation**

Scenario ID: `REV-006 Yield_Recommendation`
- Trigger: Demand_Signal record created with Demand_Score > 65
- Action: For each active package in this city, compute Recommended_Price using yield formula
- Write: Pricing_Recommendations record (Approval_Status = PENDING)
- Notify: Luciana via Slack with link to review queue

**3.3 Make Scenario: Stale Recommendation Cleanup**

Scenario ID: `REV-007 Pricing_Recommendation_Cleanup`
- Trigger: Scheduled (daily)
- Action: Mark PENDING recommendations older than 72 hours as EXPIRED
- Alert: Luciana if >3 recommendations expired unreviewed in 7 days

**3.4 Airtable Interface: Pricing Approval Queue**

Build Airtable Interface for Luciana:
- View: All PENDING Pricing_Recommendations sorted by City, Date_Window
- Actions: APPROVE / DENY buttons (updates Approval_Status, logs Reviewed_By)
- Display: Reasoning column showing Claude's plain-English justification

**3.5 Claude Prompt: Pricing Reasoning Narrative**

Each Pricing_Recommendation includes a Claude-generated reasoning field:
- State the demand conditions driving the recommendation
- State the margin impact at recommended price
- State the margin impact at base price
- Recommend action in plain English
- Include a luxury positioning note if relevant

**3.6 Founder Calibration Session**

After 30 days of recommendations accumulating, Founder and Luciana review:
- Are the demand signals matching intuition?
- Are the multipliers appropriate for the brand?
- Are there adjustments needed to the demand score formula?
- Set official multiplier cap for each city/brand combination

### Phase 3 Success Criteria

- [ ] Weekly demand signals generating without error for 4 weeks
- [ ] Pricing recommendations appearing in Approval Queue correctly
- [ ] Luciana reviewing recommendations within 48 hours (measured by Approval_Status timestamps)
- [ ] Zero recommendations applied to bookings without Approval_Status = APPROVED
- [ ] Founder calibration session completed and multiplier caps documented
- [ ] Stale recommendation cleanup running correctly

---

## SECTION 6: PHASE 4 — REFERRAL + OFFER INTELLIGENCE

**Duration:** 3–4 weeks
**Owner:** System Administrator + Luciana

### Objective
Map the referral network, activate referral quality scoring, and launch offer performance tracking to identify underperforming and star-tier packages and add-ons.

### Tasks

**4.1 Make Scenario: Referral Attribution on Request**

Scenario ID: `REV-008 Referral_Attribution`
- Trigger: New Request record created
- Action: If Source = REFERRAL_CLIENT / AFFILIATE / PLANNER, create Referral_Network record linking referrer to new client
- Flag: If Source = UNKNOWN after 48 hours, generate Luciana prompt to capture source

**4.2 Make Scenario: Weekly Referral Quality Score**

Scenario ID: `REV-009 Referral_Quality_Weekly`
- Trigger: Scheduled (Monday 7:00 AM)
- Action: Compute Referral_Quality_Score for all referral sources with 2+ attributed requests
- Write: Score to Affiliates.Referral_Quality_Score and Partner_Outreach.Relationship_Depth_Score
- Alert: ELITE_REFERRER cooling alert, attribution gap alert

**4.3 Make Scenario: Referral Moment Identification**

Scenario ID: `REV-010 Referral_Moment`
- Trigger: Booking Charter_Grade updated to A
- Action: Check contraindication conditions (complaint, chargeback risk)
- If clear: Generate Luciana prompt with referral invitation language for Luciana's review and personalization
- Log: Referral moment generated → Audit_Log

**4.4 Make Scenario: Monthly Offer Performance Computation**

Scenario ID: `REV-011 Offer_Performance_Monthly`
- Trigger: Scheduled (1st of month)
- Action: For each active package and add-on, compute Attach_Rate, Revenue_Contribution_Pct, Avg_Offer_Margin, Performance_Score
- Write: Offer_Performance record per offer per period
- Alert: FAILING tier offers → Founder for decision. Underperforming → Luciana.

**4.5 Claude Prompt: Offer Recommendation Narrative**

Monthly offer performance report includes Claude narrative:
- Which offers are driving the most margin
- Which offers have declining attach rates and why (where data supports a hypothesis)
- One recommended bundle to test for next period
- One offer recommended for retirement consideration

### Phase 4 Success Criteria

- [ ] Referral attribution captured on 90%+ of requests (Source ≠ UNKNOWN)
- [ ] Referral_Network table populated with all attributable referral chains
- [ ] Referral_Quality_Score computed for all active referral sources
- [ ] Referral moment prompts generating correctly post A-grade charter
- [ ] Monthly offer performance report generating correctly
- [ ] At least 1 offer identified for retirement or repricing by end of first month

---

## SECTION 7: PHASE 5 — REVENUE DASHBOARDS + ALERTS

**Duration:** 2–3 weeks
**Owner:** System Administrator + Founder (design sign-off)

### Objective
Surface all intelligence in the Founder Dashboard and automate the weekly revenue digest. This phase makes the intelligence operational — not just computed, but seen and acted upon.

### Tasks

**5.1 Founder Dashboard Intelligence Cards (Airtable Interface)**

Add 4 new intelligence cards to the existing Founder Dashboard:

Card 1: Revenue Health
- Composite Revenue_Health_Score per city-brand (color coded GREEN/YELLOW/ORANGE/RED)
- Week-over-week trend arrow
- One-line alert if any city is ORANGE or RED

Card 2: Demand Outlook
- Demand_Score per city for next 30/60/90 days
- Surge window indicator if active
- Link to Pricing Approval Queue (count of pending recommendations)

Card 3: LTV Leaderboard
- Top 10 clients by Composite_LTV
- Churn Risk flag next to any CRITICAL clients
- Next_Booking_Probability for each
- Lifecycle_Stage badge

Card 4: Referral Network Health
- Viral_Coefficient (rolling 90-day)
- Count of ELITE / STRONG referrers
- Top 3 referral sources by revenue this month
- Attribution gap percentage

**5.2 Make Scenario: Weekly Revenue Intelligence Digest**

Scenario ID: `REV-012 Weekly_Revenue_Digest`
- Trigger: Scheduled (Monday 7:00 AM)
- Action: Aggregate all intelligence scores, alerts, and pending recommendations
- Claude prompt: Generate weekly brief narrative (per template in Section 4 of Architecture doc)
- Destination: Slack #sss-intelligence-digest (Founder + Luciana)

**5.3 Alert Routing Configuration**

Configure all intelligence alerts (as defined in each module document) with correct:
- Recipient (Founder vs Luciana vs both)
- Channel (Slack DM vs channel)
- Priority (immediate vs batched in weekly digest)
- Audit_Log linkage

### Phase 5 Success Criteria

- [ ] All 4 Founder Dashboard cards live and displaying accurate data
- [ ] Weekly Revenue Intelligence Digest firing and delivering correctly for 4 weeks
- [ ] All alert types tested with synthetic triggers
- [ ] Founder confirms dashboard cards are useful and accurate
- [ ] No false positive alerts in first 30 days

---

## SECTION 8: PHASE 6 — INTELLIGENCE COMPOUNDING (ONGOING)

**Duration:** Ongoing from Phase 5 completion

### Objective
The intelligence layer improves as it accumulates outcome data. Phase 6 is not a build phase — it is an operational discipline.

### Compounding Mechanisms

**Outcome Tracking**
Every Pricing_Recommendation that reaches Approval_Status = APPROVED is linked to its resulting Booking. The `Outcome_Margin` field records actual margin achieved. Over time, this data shows whether the multiplier formulas are accurate.

**Model Recalibration Triggers**
| Condition | Action |
|---|---|
| Pricing recommendations systematically over-predict demand (actual bookings lag) | Adjust demand score weights — founder reviews |
| LTV tier predictions misalign with actual repeat behavior | Adjust Projected_LTV_12M formula — Luciana flags, founder approves |
| Referral quality scores diverge from actual referred booking close rates | Adjust close rate scoring weights |
| Offer attach rates inconsistently predicted | Adjust Occasion_Affinity map |

**Annual Recalibration Review (January)**
- LTV tier dollar ranges reviewed and adjusted for business growth
- Demand score seasonal index rebuilt from full-year data
- Pricing multiplier caps reviewed by city
- Offer performance scores reviewed against full year
- Referral network depth and viral coefficient trended

**Lessons Integration**
Insights from the intelligence layer feed the `Lessons` table (per Operational Memory Layer governance):
- When a pricing recommendation outperforms expectations → Lesson proposed
- When a client segment shows unexpected churn pattern → Lesson proposed
- When an add-on shows unexpected conversion lift → Lesson proposed

All Lessons from this layer require Luciana review → Founder approval before ACTIVE status.

---

## SECTION 9: DEPENDENCY MAP

```
PREREQUISITE: Airtable Consolidation (70%+ complete)
      │
      ▼
PHASE 1: Data Foundation
  ├── New tables created
  ├── Field extensions deployed
  └── Historical backfill complete
      │
      ▼
PHASE 2: LTV + Relationship Intelligence
  ├── Requires: Phase 1 complete
  ├── Requires: Bookings history ≥ 3 months clean data
  └── Feeds: Phase 3 (LTV tier → pricing priority)
      │
      ▼
PHASE 3: Pricing + Yield Intelligence
  ├── Requires: Phase 1 complete
  ├── Requires: Demand_Signals table populated (Phase 1)
  └── Independent of Phase 2 (can run in parallel)
      │
      ▼
PHASE 4: Referral + Offer Intelligence
  ├── Requires: Phase 1 complete
  ├── Requires: Source attribution (Phase 1 backfill)
  └── Independent of Phases 2–3 (can run in parallel after Phase 1)
      │
      ▼
PHASE 5: Dashboards + Alerts
  ├── Requires: All Phases 1–4 data sources live
  └── Requires: Founder design review of dashboard layout
      │
      ▼
PHASE 6: Ongoing Compounding
  └── Requires: Phase 5 complete + 90 days of outcome data
```

---

## SECTION 10: RISK AND GOVERNANCE

### Implementation Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Airtable consolidation delayed, blocking Phase 1 | HIGH | Intelligence build begins only after consolidation 70% complete |
| LTV scores produce counterintuitive results | MEDIUM | 2-week validation period with Luciana in Phase 2 |
| Pricing recommendations ignored by operations | MEDIUM | Dashboard visibility + Luciana Slack prompts; track review rate |
| Data quality issues undermine intelligence accuracy | HIGH | Phase 1 backfill includes data quality audit; UNKNOWN flags surfaced |
| Alert volume becomes noise (alert fatigue) | MEDIUM | Alert thresholds tuned during Phase 5; weekly digest batches low-priority alerts |
| Founder dashboard cards not used | LOW | Co-design session with Founder before build |

### Governance Requirements

All implementation changes are subject to:
- Founder approval before any new Make scenario goes to Production
- Airtable schema changes require Audit_Log entry
- New Claude prompts require version control in AI_Prompt_Versions table
- No intelligence output can trigger autonomous client communication (all Tier B minimum)
- Intelligence tables are PRODUCTION environment only (no live testing in Production database)

### Rollback Protocol

If any Phase produces unexpected behavior:
1. Make scenario is deactivated immediately
2. Affected Airtable records flagged with Environment = ROLLBACK_REVIEW
3. Founder notified
4. Prior state restored from backup before re-attempting

---

## SECTION 11: SUCCESS METRICS — FULL LAYER

At 6 months post-Phase 5 completion, measure against baseline:

| Metric | Baseline (Pre-Implementation) | Target |
|---|---|---|
| Average Net Margin % | Establish at Phase 1 | +2–3 percentage points |
| Close Rate | Establish at Phase 1 | +5–10 percentage points |
| Average Booking Value | Establish at Phase 1 | +10–15% |
| Upsell Attach Rate | Establish at Phase 1 | +15% absolute |
| Repeat Booking Rate | Establish at Phase 1 | +20% |
| Discount Exposure Rate | Establish at Phase 1 | <10% (down from current) |
| Referral Viral Coefficient | Establish at Phase 1 | >0.5 |
| DIAMOND/PLATINUM churn rate | Establish at Phase 1 | <5% annual |
| Pricing recommendation review rate | N/A (new) | >80% reviewed within 48h |
| Revenue Health Score (avg) | N/A (new) | >75 across all active cities |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION. No implementation begins without explicit founder authorization.*
