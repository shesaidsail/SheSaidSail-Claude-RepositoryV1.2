# REVENUE INTELLIGENCE ARCHITECTURE
**Document ID:** 10_REVENUE__REVENUE_INTELLIGENCE_ARCHITECTURE_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE AND SCOPE

This document defines the Revenue + Relationship Intelligence Layer for She Said Sail and Mare Executive. It establishes the architecture for seven interconnected intelligence modules that compound operational data into actionable revenue recommendations.

The intelligence layer does not make decisions. It surfaces signals, scores behavior, and recommends actions within the authority framework defined in `00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED.md` and `00_LOCKED_GOVERNANCE__Commercial_Authority_Framework_v1.0_PRODUCTION.md`.

**What this layer maximizes:**
- Net margin (minimum 20% threshold enforced at all times)
- Close rate on inbound requests
- Client Lifetime Value (LTV)
- Referral velocity and quality
- Repeat booking rate
- Pricing efficiency and yield
- Luxury positioning (no discount signals, no urgency language)

**What this layer never does:**
- Override founder pricing authority
- Apply discounts autonomously
- Contact clients without Tier B/C human review
- Recommend pricing exceptions below 20% margin without founder escalation

---

## SECTION 2: INTELLIGENCE MODULE MAP

The Revenue + Relationship Intelligence Layer comprises seven modules. Each module feeds data upstream and receives signals downstream. Together they form a closed-loop intelligence system.

```
┌─────────────────────────────────────────────────────────────────┐
│            REVENUE + RELATIONSHIP INTELLIGENCE LAYER            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────────┐       ┌──────────────────────────────┐    │
│  │  PRICING        │──────▶│  YIELD MANAGEMENT            │    │
│  │  INTELLIGENCE   │       │  (Demand × Capacity × Margin)│    │
│  └────────┬────────┘       └──────────────┬───────────────┘    │
│           │                               │                     │
│           ▼                               ▼                     │
│  ┌─────────────────┐       ┌──────────────────────────────┐    │
│  │  REVENUE        │◀──────│  DEMAND SIGNAL               │    │
│  │  INTELLIGENCE   │       │  INTELLIGENCE                │    │
│  └────────┬────────┘       └──────────────────────────────┘    │
│           │                                                     │
│           ▼                                                     │
│  ┌─────────────────┐       ┌──────────────────────────────┐    │
│  │  OFFER          │──────▶│  CLIENT LTV ENGINE           │    │
│  │  INTELLIGENCE   │       │                              │    │
│  └─────────────────┘       └──────────────┬───────────────┘    │
│                                           │                     │
│                             ┌─────────────▼───────────────┐    │
│                             │  RELATIONSHIP INTELLIGENCE  │    │
│                             └─────────────┬───────────────┘    │
│                                           │                     │
│                             ┌─────────────▼───────────────┐    │
│                             │  REFERRAL INTELLIGENCE      │    │
│                             └─────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
```

### Module Definitions

| Module | Primary Input | Primary Output | Home Document |
|---|---|---|---|
| Revenue Intelligence | Bookings, margins, period data | Revenue health scores, alerts, trends | This document |
| Pricing Intelligence | Package prices, demand, yield | Price recommendations, multipliers | PRICING_INTELLIGENCE.md |
| Demand Signal Intelligence | Inbound volume, search seasonality, booking lead time | Demand scores, surge alerts | This document (Section 5) |
| Yield Management | Capacity, demand signals, pricing | Optimal rate recommendations | This document (Section 6) |
| Relationship Intelligence | Client history, touchpoints, interactions | Relationship scores, VIP alerts | RELATIONSHIP_INTELLIGENCE_SPEC.md |
| Client LTV Engine | Booking history, frequency, spend | LTV scores, churn risk, reactivation signals | CLIENT_LTV_ENGINE.md |
| Offer Intelligence | Package performance, add-on data | Bundle recommendations, upsell signals | OFFER_INTELLIGENCE.md |
| Referral Intelligence | Referral source, conversion, network | Referral quality scores, timing signals | REFERRAL_INTELLIGENCE.md |

---

## SECTION 3: SYSTEM INTEGRATION ARCHITECTURE

This layer is built on top of the existing infrastructure stack defined in `02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION.md`. No new primary platforms are introduced. All intelligence lives in Airtable, is orchestrated by Make, and is reasoned over by Claude.

### Integration Stack

```
GitHub (governance + prompt versioning)
    │
    ▼
Claude (intelligence reasoning)
    │
    ▼
Airtable (operational brain + intelligence tables)
    │
    ▼
Make (automation orchestration + signal processing)
    │
    ├──▶ Slack (founder + ops alerts)
    ├──▶ Gmail/Quo (client communications — Tier B/C only)
    └──▶ Stripe (payment signal ingestion)
```

### New Airtable Tables Required

The following tables are added to the SSS Operations base:

| Table Name | Purpose |
|---|---|
| `Revenue_Snapshots` | Weekly/monthly revenue health captures per city, brand, period |
| `Client_LTV_Scores` | Computed LTV tier, RFM scores, churn risk per client |
| `Relationship_Scores` | Relationship depth score per client and broker/planner |
| `Referral_Network` | Referral source graph, quality scores, attribution chains |
| `Offer_Performance` | Package and add-on attach rates, revenue contribution, margin per offer |
| `Pricing_Recommendations` | AI-generated pricing signals awaiting founder review |
| `Demand_Signals` | Rolling demand metrics, surge windows, inventory pressure scores |
| `Yield_Log` | Record of rate recommendations, approval states, outcomes |

### Existing Tables Extended

| Existing Table | New Fields Added |
|---|---|
| `Clients` | `LTV_Score`, `LTV_Tier`, `Relationship_Score`, `Churn_Risk`, `Referral_Quality_Score`, `Next_Booking_Probability`, `VIP_Flag`, `Days_Since_Last_Charter` |
| `Bookings` | `Yield_Score`, `Demand_Window`, `Offer_Source`, `Upsell_Revenue`, `Upsell_Attach_Rate`, `Referral_Chain_ID` |
| `Packages` | `Margin_Score`, `Attach_Rate`, `Revenue_Contribution_Pct`, `Performance_Tier`, `Recommended_Multiplier` |
| `Affiliates` | `Referral_Quality_Score`, `Network_Depth`, `Revenue_Generated_LTD`, `Avg_Booking_Value` |
| `Partner_Outreach` | `Relationship_Depth_Score`, `Revenue_Attributed`, `Referral_Velocity` |

---

## SECTION 4: REVENUE INTELLIGENCE MODULE

### Purpose
Revenue Intelligence is the master health layer. It aggregates across all other modules to produce revenue health scores, identify anomalies, and surface executive-level insights for the Founder Dashboard.

### Core Metrics Tracked

**Booking-Level Metrics (existing fields, now intelligence-scored):**
- Gross Revenue = Package_Price + Add_Ons_Revenue
- Net Revenue = Gross_Revenue − Tax_Collected
- Net Profit = Net_Revenue − (Vessel_Cost + Labor_Cost + F&B_Cost)
- Net Margin% = Net_Profit / Net_Revenue (minimum 20% enforced)
- Yield_Score = Actual_Net_Margin / City_Benchmark_Margin

**Period-Level Metrics (captured in Revenue_Snapshots):**
- Monthly Recurring Revenue equivalent (MRR_Equiv): rolling 30-day gross revenue
- Revenue Per Available Charter Day (RevPACD): Gross_Revenue / Available_Charter_Days
- Average Booking Value (ABV): Gross_Revenue / Confirmed_Bookings
- Upsell Penetration Rate: Bookings_With_Add_Ons / Total_Bookings
- Discount Exposure Rate: Discounted_Bookings / Total_Bookings (target: <10%)
- Close Rate: Confirmed_Bookings / Total_Qualified_Requests
- Margin Erosion Index: Bookings_Below_25pct_Margin / Total_Bookings

**Brand-Level Metrics:**
- SSS vs Mare Executive margin comparison
- City-level RevPACD ranking
- Package tier contribution mix (entry / mid / premium)

### Revenue Health Score

A composite 0–100 score computed weekly per city-brand combination:

```
Revenue_Health_Score =
  (Net_Margin_Avg × 0.30) +
  (Close_Rate × 0.20) +
  (ABV_vs_Benchmark × 0.15) +
  (Upsell_Penetration × 0.15) +
  (Discount_Exposure_Inverse × 0.10) +
  (Repeat_Booking_Rate × 0.10)
```

**Score Bands:**
| Score | Status | Action |
|---|---|---|
| 85–100 | GREEN | Monitor only |
| 70–84 | YELLOW | Weekly review, identify improvement levers |
| 55–69 | ORANGE | Founder briefed, action plan required |
| <55 | RED | Founder alert, immediate review |

### Revenue Alert Types

| Alert | Trigger | Recipient | Channel |
|---|---|---|---|
| `MARGIN_EROSION` | 3+ bookings in 7 days below 22% margin | Founder | Slack DM |
| `CLOSE_RATE_DROP` | Close rate falls below 40% over 14-day window | Founder + Luciana | Slack |
| `DISCOUNT_OVEREXPOSURE` | Discount rate exceeds 15% in rolling 30 days | Founder | Slack DM |
| `ABV_DECLINE` | ABV drops >15% vs prior 30-day period | Founder | Slack DM |
| `YIELD_UNDERPERFORMANCE` | RevPACD >20% below city benchmark | Founder + Luciana | Slack |
| `HIGH_VALUE_STALL` | HV client with no booking in 90+ days | Luciana | Slack |

---

## SECTION 5: DEMAND SIGNAL INTELLIGENCE MODULE

### Purpose
Demand Signal Intelligence reads leading indicators of booking demand to allow proactive yield adjustments, inventory holds, and capacity planning before bookings materialize.

### Signal Sources

| Signal | Source | Update Frequency |
|---|---|---|
| Inbound Request Volume | Airtable: Requests table | Real-time (Make webhook) |
| Lead Time Distribution | Airtable: Bookings.Request_to_Confirm_Days | Weekly aggregate |
| Occasion Concentration | Airtable: Bookings.Occasion field | Weekly aggregate |
| Conversion Rate by Day/Month | Airtable: Bookings × Requests | Weekly computation |
| Social Inquiry Spike | Future: Instagram DM / Meta API (Phase 4) | Real-time when active |
| Seasonal Patterns | Historical Bookings rolling 12 months | Monthly model refresh |

### Demand Score Computation

Per city, per 30-day forward window:

```
Demand_Score =
  (Request_Volume_vs_Baseline × 0.35) +
  (Lead_Time_Compression × 0.25) +
  (Occasion_Peak_Proximity × 0.20) +
  (Historical_Seasonal_Index × 0.20)
```

**Demand Bands:**
| Score | Status | Pricing Signal |
|---|---|---|
| >80 | SURGE | Recommend peak multiplier review |
| 60–80 | HIGH | Hold protected inventory, upsell aggressively |
| 40–60 | NORMAL | Standard pricing applies |
| <40 | SOFT | Review off-peak incentives (within approved discount framework) |

### Surge Window Identification

A Surge Window is a calendar period where Demand_Score exceeds 75 for 5+ consecutive days. When identified:
1. Demand_Signals table record created with Surge_Window flag
2. Pricing_Intelligence module is notified to generate multiplier recommendation
3. Founder briefed via Slack with recommended action
4. Protected inventory automatically flagged as non-discountable for window duration

---

## SECTION 6: YIELD MANAGEMENT MODULE

### Purpose
Yield Management combines demand signals, pricing data, and capacity constraints to generate rate recommendations that maximize revenue per available charter day without brand dilution.

### Yield Formula

```
Optimal_Rate = Base_Package_Rate × Demand_Multiplier × Capacity_Pressure_Factor × Brand_Floor_Multiplier

Where:
  Base_Package_Rate      = Published package price (Packages table)
  Demand_Multiplier      = 1.0 + (Demand_Score − 50) / 100  [range: 0.85–1.35]
  Capacity_Pressure      = Available_Slots / Total_Slots_In_Window  [inverse: low availability = higher multiplier]
  Brand_Floor_Multiplier = Never falls below 1.0 (never recommend below published rate)
```

**Multiplier Cap:** Maximum recommended rate increase is 35% above published rate without founder approval.

**Discount Floor:** Minimum allowable recommendation is −7% (off-peak weekday, approved scenario only). Any recommendation below published rate requires explicit Approved_Discount_Scenario flag.

### Yield Log

Every rate recommendation is written to `Yield_Log` with:
- Recommendation_ID (UUID)
- City, Brand, Vessel, Date_Window
- Base_Rate, Recommended_Rate, Multiplier_Applied
- Demand_Score at time of recommendation
- Approval_Status (PENDING / APPROVED / DENIED / EXPIRED)
- Outcome (if booking occurred: Actual_Rate_Charged, Net_Margin_Achieved)
- Reviewed_By

### Inventory Pressure Classification

| Availability | Status | Yield Signal |
|---|---|---|
| <20% slots remaining | CRITICAL | Maximum multiplier, no discounts |
| 20–40% remaining | HIGH | Elevated multiplier, no off-peak discounts |
| 40–70% remaining | NORMAL | Standard pricing |
| >70% remaining | LOW | Off-peak eligible (approved scenarios only) |

---

## SECTION 7: DATA GOVERNANCE

### Intelligence Data Principles

1. **Immutability**: Revenue_Snapshots, Yield_Log, and Offer_Performance records are append-only. No deletion.
2. **UUID Governance**: All intelligence table records carry UUID following `00_LOCKED_GOVERNANCE__Financial_OS_v1.0_PRODUCTION.md` UUID standards.
3. **Environment Separation**: All intelligence records carry Environment field (PRODUCTION / SANDBOX / DEV). Intelligence computed in SANDBOX never triggers real alerts.
4. **Audit Linkage**: All Pricing_Recommendations and Yield_Log records link to the Audit_Log table.
5. **Founder Override**: Any intelligence recommendation overridden by founder decision is logged with Founder_Decision_ID linkage.

### Claude's Role in This Layer

Claude operates as the reasoning and synthesis engine:
- **Ingests** aggregated Airtable data via Make-triggered prompts
- **Computes** intelligence scores using defined formulas
- **Drafts** recommendations for founder or Luciana review
- **Never** sends recommendations directly to clients
- **Never** applies pricing changes autonomously
- **Always** cites source data and formula used in recommendation output

All Claude outputs in this layer are **Tier A** (intelligence surfacing) or **Tier B** (recommendation draft for human review). No revenue or pricing action is **Tier A autonomous**.

---

## SECTION 8: REPORTING ARCHITECTURE

### Weekly Revenue Intelligence Report

Delivered every Monday via Slack to Founder and Luciana:

```
SSS REVENUE INTELLIGENCE WEEKLY BRIEF
Week of: [Date]

REVENUE HEALTH SCORES:
  [City A] SSS: 82 (YELLOW) | Mare: — 
  [City B] SSS: 91 (GREEN)

KEY METRICS vs PRIOR WEEK:
  Gross Revenue: $XX,XXX (▲/▼ X%)
  Average Booking Value: $X,XXX (▲/▼ X%)
  Net Margin Avg: XX.X% (▲/▼ Xbps)
  Close Rate: XX% (▲/▼ X%)
  Upsell Penetration: XX%

ACTIVE ALERTS: [List]

TOP OPPORTUNITIES: [List from Offer + LTV modules]

PRICING RECOMMENDATIONS PENDING REVIEW: [Count + link]
```

### Founder Dashboard Intelligence Cards

The Founder Dashboard (Airtable Interface) gains 4 new intelligence cards:
1. **Revenue Health** — composite score with trend arrow
2. **Demand Outlook** — next 30/60/90 day demand score per city
3. **LTV Leaderboard** — top 10 clients by LTV tier + next booking probability
4. **Referral Network Health** — referral velocity, top referrers, pending referral moments

---

## SECTION 9: GOVERNANCE CONSTRAINTS

This layer operates under the following constraints from locked governance:

| Constraint | Source Document |
|---|---|
| AI cannot approve discounts or pricing exceptions | Commercial Authority Framework |
| Pricing exceptions below 20% margin require Will approval | Founder Control Framework |
| Protected inventory cannot be discounted autonomously | Commercial Authority Framework |
| All pricing recommendations require human review before action | Founder Control Framework |
| Referral commissions (5%) and repeat discounts (5%) are the only autonomous offer types | Commercial Authority Framework |
| HV_Client comms always require Luciana review | Founder Control Framework |
| All intelligence outputs are logged to Audit_Log | Operational Memory Layer |

---

## SECTION 10: DOCUMENT CROSS-REFERENCES

| Topic | Document |
|---|---|
| Pricing Intelligence module detail | PRICING_INTELLIGENCE.md |
| Relationship scoring and VIP protocol | RELATIONSHIP_INTELLIGENCE_SPEC.md |
| LTV calculation and tier engine | CLIENT_LTV_ENGINE.md |
| Referral attribution and network mapping | REFERRAL_INTELLIGENCE.md |
| Package performance and upsell intelligence | OFFER_INTELLIGENCE.md |
| Implementation sequence and phases | REVENUE_IMPLEMENTATION_ROADMAP.md |
| Authority tiers (A/B/C) | 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED.md |
| Approved discount scenarios | 00_LOCKED_GOVERNANCE__Commercial_Authority_Framework_v1.0_PRODUCTION.md |
| Financial formulas and margin rules | 00_LOCKED_GOVERNANCE__Financial_OS_v1.0_PRODUCTION.md |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION. All intelligence modules described herein are architectural specifications only — no implementation has occurred.*
