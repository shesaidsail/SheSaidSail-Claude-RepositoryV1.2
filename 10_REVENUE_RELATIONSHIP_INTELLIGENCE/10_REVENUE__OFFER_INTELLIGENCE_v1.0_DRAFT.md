# OFFER INTELLIGENCE
**Document ID:** 10_REVENUE__OFFER_INTELLIGENCE_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

Offer Intelligence tracks the performance of every package, add-on, and bundle in the She Said Sail catalog. It identifies what sells, what upsells, what stalls, and what should be retired or repriced. The goal is to maximize revenue per booking without degrading margin or brand positioning.

Offer Intelligence feeds directly into Pricing Intelligence (what to charge) and Relationship Intelligence (what to recommend to whom).

---

## SECTION 2: OFFER TAXONOMY

### Offer Types

| Type | Definition | Example |
|---|---|---|
| **Base Package** | Core charter offering at published price | 4-Hour Bachelorette Charter |
| **Premium Package** | Enhanced charter with elevated vessel or inclusions | Flagship Full-Day Experience |
| **Add-On** | Discrete upsell attached to any booking | Champagne package, Photographer, Catering upgrade |
| **Bundle** | Pre-packaged combination of add-ons at slight premium | "Full Celebration Bundle" |
| **Custom Build** | Bespoke configuration for HV or corporate clients | Founder-approved only |

### Current Offer Gaps (Known from Airtable Audit)

The Packages table currently has only 8 fields — dramatically underdeveloped. Offer Intelligence requires the Packages table to be expanded to 25+ fields per the Airtable Build Spec. Until this expansion is implemented, Offer Intelligence operates on data from the Bookings table (Add_Ons_Selected field and Package_Price).

---

## SECTION 3: OFFER PERFORMANCE METRICS

Each offer (package, add-on, bundle) is scored on four dimensions:

### 1. Attach Rate

```
Attach_Rate = Bookings_With_This_Offer / Total_Eligible_Bookings
```

Eligible bookings are those where the offer could plausibly have been presented (right occasion, right city, right package tier).

**Attach Rate Benchmarks:**
| Offer Type | Target Attach Rate | Alert Threshold |
|---|---|---|
| Premium add-on (photographer, champagne) | >35% | <20% |
| Mid-tier add-on (catering upgrade) | >25% | <15% |
| Bundle | >15% | <8% |
| Premium package upgrade | >20% | <10% |

### 2. Revenue Contribution

```
Revenue_Contribution_Pct = Sum_Revenue_From_Offer / Total_Gross_Revenue_In_Period
```

### 3. Margin Contribution

```
Offer_Margin = (Offer_Revenue − Offer_COGS) / Offer_Revenue
```

Add-on margins are typically higher than base package margins (lower direct costs). The intelligence layer identifies and promotes high-margin add-ons.

### 4. Conversion Lift

When an offer is included in a proposal:
```
Conversion_Lift = Close_Rate_With_Offer / Close_Rate_Without_Offer − 1
```

Positive lift means the offer improves close rate (the package is compelling). Negative lift means the offer may be creating price friction.

---

## SECTION 4: OFFER PERFORMANCE SCORING

Each offer receives an Offer_Performance_Score (0–100):

```
Offer_Performance_Score =
  (Attach_Rate_Score × 0.30) +
  (Margin_Contribution_Score × 0.25) +
  (Revenue_Contribution_Score × 0.25) +
  (Conversion_Lift_Score × 0.20)
```

### Performance Tiers

| Score | Tier | Action |
|---|---|---|
| 80–100 | STAR | Feature prominently in all proposals, prioritize in recommendation engine |
| 60–79 | STRONG | Standard inclusion in relevant proposals |
| 40–59 | AVERAGE | Review presentation and timing; A/B test positioning |
| 20–39 | UNDERPERFORMING | Founder review: reprice, reframe, or retire |
| <20 | FAILING | Retire or restructure before next season |

---

## SECTION 5: OFFER RECOMMENDATION ENGINE

The recommendation engine selects which add-ons to include in each proposal based on the client profile. It does not decide pricing — it decides sequencing and selection.

### Recommendation Logic

```
FOR each open Request:
  1. Identify Occasion (from Requests.Occasion)
  2. Identify LTV_Tier (from Client_LTV_Scores)
  3. Identify Brand (SSS vs Mare Executive)
  4. Filter: Active offers that are:
     - Available in this City
     - Relevant to this Occasion
     - Not previously declined by this client
  5. Rank by:
     - Margin_Contribution (highest first)
     - Occasion_Relevance_Score
     - Client_History_Fit (has client taken this before and reacted positively?)
  6. Present:
     - Top 2 add-ons to NEW / BRONZE clients
     - Top 3 add-ons to SILVER / GOLD clients
     - Premium package first + top 3 add-ons to PLATINUM / DIAMOND clients
```

### Occasion → Offer Affinity Map

| Occasion | High-Affinity Offers |
|---|---|
| Bachelorette | Champagne, Photographer, Floral Decor, Party Supplies |
| Birthday | Cake Package, Photographer, Champagne, Personalized Welcome |
| Anniversary | Romantic Decor, Champagne, Private Chef, Sunset Cruise Upgrade |
| Corporate / Executive Retreat | Catering, AV Setup, Premium Vessel, Concierge White-Glove |
| Girls Trip | Champagne, Charcuterie, Music Package, Group Photo |
| Client Hosting | Premium Vessel Upgrade, Catering, Concierge Service |

### Previous Declination Memory

If a client has previously declined a specific add-on and that declination is captured in the client record, the recommendation engine excludes that add-on for 12 months to avoid repeat friction.

---

## SECTION 6: BUNDLE OPTIMIZATION

Bundles are pre-packaged add-on combinations offered at a small premium to individual items. They increase attach rate by reducing decision complexity.

### Bundle Design Principles

1. **3-item max.** More items = decision paralysis.
2. **Slight premium only.** Bundle price = individual prices + 10–15%. Never equal or less (margin erosion and perceived discount).
3. **Occasion-specific naming.** "Celebration Bundle" outperforms "Package A."
4. **Tiered bundles.** Offer a "signature" and "elevated" version to enable anchoring.
5. **Margin floor.** Bundle margin must remain above 25%.

### Bundle Performance Tracking

Bundle_Performance table tracks:
- Bundle_Attach_Rate vs component individual rates
- Bundle_Margin vs component individual margins
- Bundle_Conversion_Lift
- Component contribution within bundle (which item is the "hero")

When Bundle_Attach_Rate falls below 2× individual component Attach_Rate, the bundle is reviewed. When it falls below 1×, it is retired.

---

## SECTION 7: UPSELL TIMING RULES

When an upsell is presented matters as much as what is presented. The intelligence layer generates upsell prompts at the optimal moment in the booking lifecycle.

### Upsell Windows

| Moment | Upsell Type | Rationale |
|---|---|---|
| Proposal stage | Premium package upgrade + top 2 add-ons | Client is in buying mode |
| Deposit confirmed | Mid-tier add-ons (champagne, photographer) | Commitment achieved, receptiveness high |
| D-14 before charter | Final add-on prompt (logistics-friendly items) | Last window before preparation |
| Post-charter (D+7) | Next booking offer only — not add-on upsell | Re-engagement, not immediate sell |

### Upsell Language Rules (Brand Governance)

Upsell language must:
- Feel like a curated recommendation, not a pitch
- Reference client's specific occasion ("Since you're celebrating a bachelorette...")
- Never use urgency language ("before it's gone," "limited availability," "act now")
- Always present as an enhancement, not an add-on purchase

Prohibited upsell language (per Brand Governance):
- "Upgrade now"
- "Add-on"
- "Extra"
- "Only $X more"
- "Don't miss out"

Approved framing:
- "We'd love to include..."
- "Most clients celebrating [occasion] also love..."
- "We can arrange..."
- "One thing that tends to make [occasion] feel complete is..."

---

## SECTION 8: DISCOUNT AVOIDANCE PROTOCOL

Offer Intelligence actively avoids discount-first thinking. The protocol:

### Step 1: Premium First
Before considering any discount, the recommendation engine surfaces the highest-value offer combination available. This is always step 1.

### Step 2: Value Reframe
If client expresses price sensitivity, the intelligence layer recommends a value reframe (emphasizing what is included, what the experience delivers) rather than a price reduction.

### Step 3: Date Flexibility
If price sensitivity persists, the recommendation is to offer an alternative date (off-peak) rather than a price reduction on the requested date.

### Step 4: Package Adjustment
Reduce package scope (fewer hours, different vessel) to hit a lower price point — but at maintained margin. Never reduce margin to hold the date.

### Step 5: Approved Discount Only
Only after steps 1–4 fail does a discount scenario become relevant — and only approved scenarios apply (per Commercial Authority Framework). Luciana must flag this and receive confirmation before proceeding.

**The intelligence layer generates a Discount_Avoidance_Log entry every time a discount is discussed, showing which steps were attempted.** This creates an institutional record of whether the operation is defending pricing correctly.

---

## SECTION 9: OFFER INTELLIGENCE AIRTABLE ARCHITECTURE

### Offer_Performance Table (New)

| Field | Type | Description |
|---|---|---|
| `Performance_ID` | UUID | Immutable |
| `Offer` | Linked | Package or Add-on record |
| `Offer_Type` | Single Select | PACKAGE / ADD_ON / BUNDLE |
| `Period` | Linked | Financial_Period record |
| `City` | Linked | City record |
| `Brand` | Single Select | SSS / Mare Executive |
| `Presentations` | Number | Times offer was included in proposals |
| `Attachments` | Number | Times offer was confirmed in bookings |
| `Attach_Rate` | Formula | Attachments / Presentations |
| `Gross_Revenue_Generated` | Currency | Total revenue from this offer in period |
| `Avg_Offer_Margin` | Percent | Average margin on offer |
| `Revenue_Contribution_Pct` | Formula | % of period gross revenue |
| `Conversion_Lift` | Percent | Close rate with vs without offer |
| `Performance_Score` | Number | 0–100 composite |
| `Performance_Tier` | Single Select | STAR / STRONG / AVERAGE / UNDERPERFORMING / FAILING |
| `Prior_Period_Score` | Number | Score from prior period |
| `Score_Delta` | Formula | Performance_Score − Prior_Period_Score |
| `Recommendation` | Long Text | Claude-generated action recommendation |
| `Environment` | Single Select | PRODUCTION / SANDBOX |

### Packages Table — Extended Fields (subset relevant to Offer Intelligence)

| Field | Description |
|---|---|
| `Performance_Tier` | Current performance tier lookup |
| `Attach_Rate_YTD` | Year-to-date attach rate |
| `Avg_Margin_YTD` | Year-to-date average margin |
| `Recommended_Multiplier` | Pricing Intelligence recommendation |
| `Last_Reviewed_Date` | Date of last founder review |
| `Status` | ACTIVE / UNDER_REVIEW / RETIRED |
| `Occasion_Affinity` | Multi-select: occasions this offer suits |
| `Min_LTV_Tier` | Minimum client tier for recommendation |

---

## SECTION 10: OFFER INTELLIGENCE ALERTS

| Alert | Trigger | Recipient |
|---|---|---|
| `ADD_ON_UNDERPERFORMING` | Attach rate <threshold for 2 consecutive periods | Luciana |
| `HIGH_MARGIN_OFFER_DECLINING` | High-margin add-on's attach rate drops >10% period-over-period | Luciana + Founder |
| `BUNDLE_INEFFECTIVE` | Bundle attach rate below component individual rate | Luciana |
| `DISCOUNT_FREQUENCY_SPIKE` | Discount_Avoidance_Log shows >15% of proposals reaching Step 5 | Founder |
| `NEW_UPSELL_OPPORTUNITY` | Occasion × LTV segment with attach rate <10% but high margin potential | Luciana |
| `STAR_OFFER_CAPACITY_CONSTRAINT` | STAR-tier offer is often requested but unavailable | Luciana (availability review) |
| `PACKAGE_RETIREMENT_RECOMMENDED` | FAILING tier for 2 consecutive periods | Founder (decision required) |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION.*
