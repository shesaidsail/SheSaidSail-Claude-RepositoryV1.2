# PRICING INTELLIGENCE
**Document ID:** 10_REVENUE__PRICING_INTELLIGENCE_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

Pricing Intelligence is the engine that translates demand signals, cost data, and competitive context into precise, defensible pricing recommendations. Its sole output is a **recommendation for founder review** — it has no autonomous pricing authority.

The goal is to maximize revenue per booking while protecting the 20% minimum margin floor and preserving luxury brand positioning. Price is never a signal of desperation. Price is always a signal of value.

---

## SECTION 2: PRICING PHILOSOPHY (BRAND CONSTRAINTS)

Pricing intelligence operates inside rigid brand and commercial constraints:

1. **No urgency pricing language.** Recommendations never use scarcity pressure tactics.
2. **No public discount visibility.** Discounts are relationship rewards, not promotional tools.
3. **Price is a positioning signal.** Lowering price below published rates is a brand dilution event, not a revenue recovery strategy.
4. **Premium anchoring.** The intelligence layer actively recommends price anchoring upward — upsells and premium options are always surfaced before any discount scenario.
5. **Approved discount scenarios only** (per Commercial Authority Framework):
   - Repeat client loyalty: −5%
   - Groups 15+: −$500 fixed
   - Off-peak weekday: −7%
   - Planner first booking: −10% (founder approval required)

---

## SECTION 3: PRICING DATA MODEL

### Inputs to Pricing Intelligence

| Input | Source Table | Field |
|---|---|---|
| Base package price | Packages | Package_Price |
| City-specific variants | Packages | City_Override_Price |
| Demand score (current) | Demand_Signals | Demand_Score |
| Capacity pressure | Bookings | Available_Slots_In_Window |
| Client LTV tier | Client_LTV_Scores | LTV_Tier |
| Client relationship score | Relationship_Scores | Relationship_Score |
| Historical margin at this price | Bookings | Net_Margin_Pct |
| Occasion type | Requests | Occasion |
| Lead time | Requests | Request_to_Confirm_Days |
| Charter grade history for vessel | Yachts | Avg_Charter_Grade |

### Pricing Recommendation Output (Pricing_Recommendations table)

| Field | Type | Description |
|---|---|---|
| Recommendation_ID | UUID | Immutable identifier |
| Created_At | ISO 8601 UTC | Timestamp |
| City | Linked | City record |
| Brand | Single Select | SSS / Mare Executive |
| Package | Linked | Package record |
| Vessel | Linked | Yacht record |
| Date_Window | Date Range | Charter date range for recommendation |
| Base_Price | Currency | Published package price |
| Recommended_Price | Currency | Intelligence recommendation |
| Recommended_Multiplier | Decimal | Recommended_Price / Base_Price |
| Demand_Score_At_Time | Number | Demand score used in calculation |
| Capacity_Pressure_At_Time | Percent | Slot fill rate at time of recommendation |
| Reasoning | Long Text | Claude-generated explanation |
| Discount_Scenario | Single Select | NULL / REPEAT_CLIENT / GROUP_15+ / OFF_PEAK / PLANNER_FIRST |
| Approval_Status | Single Select | PENDING / APPROVED / DENIED / EXPIRED |
| Reviewed_By | Text | Founder or Luciana name |
| Linked_Booking | Linked | If applied, the resulting booking |
| Actual_Price_Charged | Currency | Post-booking actual |
| Outcome_Margin | Percent | Actual net margin achieved |
| Environment | Single Select | PRODUCTION / SANDBOX / DEV |

---

## SECTION 4: PRICING MULTIPLIER FRAMEWORK

### Demand-Based Multiplier

```
Demand_Multiplier = 1.0 + ((Demand_Score − 50) × 0.007)

Examples:
  Demand_Score = 80  →  Multiplier = 1.21  (+21%)
  Demand_Score = 60  →  Multiplier = 1.07  (+7%)
  Demand_Score = 50  →  Multiplier = 1.00  (base)
  Demand_Score = 30  →  Multiplier = 0.86  (−14%, only if approved discount scenario)
```

**Hard cap:** Multiplier cannot exceed 1.35 without founder approval.
**Hard floor:** Multiplier cannot go below 0.90 via autonomous recommendation. Below 0.90 requires founder approval and Approved_Discount_Scenario flag.

### Capacity Pressure Multiplier

```
Capacity_Multiplier:
  <20% slots available  →  +0.10 (pressure premium)
  20–40% available      →  +0.05
  40–70% available      →  +0.00 (no adjustment)
  >70% available        →  −0.05 (eligible for off-peak scenario if approved)
```

### Combined Rate Formula

```
Recommended_Price = Base_Price × (Demand_Multiplier + Capacity_Multiplier)

Subject to:
  1. Recommended_Price >= Base_Price × 1.00 unless Approved_Discount_Scenario
  2. Net_Margin at Recommended_Price >= 20%
  3. Recommended_Price <= Base_Price × 1.35 unless founder approved
```

### Occasion-Based Premium Signal

Certain occasions signal willingness to pay premium. Claude surfaces these as context in the recommendation reasoning — not as a formula input (to avoid encoding client manipulation logic).

| Occasion | Premium Signal | Action |
|---|---|---|
| Bachelorette | HIGH | Recommend premium add-ons, champagne, photographer |
| Corporate / Executive Retreat | HIGH | Recommend Mare Executive upgrade, concierge premium |
| Anniversary | MEDIUM | Recommend romantic add-on bundle |
| Birthday | MEDIUM | Recommend cake, decoration, photographer |
| Girls Trip | MEDIUM-HIGH | Recommend group add-ons, champagne |
| Client Hosting | HIGH | Recommend premium vessel, VIP concierge |

---

## SECTION 5: LUXURY PRICE ANCHORING

Price anchoring is the practice of presenting higher-value options first so the selected option feels reasonable by comparison. The intelligence layer recommends anchoring in this sequence:

### Recommended Presentation Order (for Luciana / Concierge)

1. **Premium vessel + full package** (highest margin option)
2. **Standard vessel + premium add-ons** (mid-tier with upsell)
3. **Standard vessel + base package** (published rate, no discount)
4. **Off-peak alternative date** (if demand warrants, before any discount)
5. **Approved discount scenario** (only if explicitly qualified and approved)

Claude never recommends jumping to step 4 or 5 without exhausting steps 1–3. The Offer_Intelligence module provides the specific add-on recommendations for steps 1–3.

---

## SECTION 6: COMPETITOR SIGNAL ARCHITECTURE

**Current State:** No live competitor price feed. Competitor intelligence is manual.

**Architecture for Future Integration (Phase 3):**

When activated, competitor signals feed into a `Competitor_Price_Signals` table:

| Field | Description |
|---|---|
| Signal_ID | UUID |
| Source | Manual / Web Scrape / Partner Report |
| Competitor_Name | Masked or named |
| City | City record |
| Charter_Type | Half-day / Full-day / Sunset |
| Reported_Price | Currency |
| Reported_Date | Date |
| Notes | Context |

**Positioning Rule:** She Said Sail does not race to match competitors. Competitor data informs **floor awareness** only — ensuring SSS never prices so high as to lose leads to obviously cheaper alternatives without awareness. Premium positioning is maintained regardless.

---

## SECTION 7: MARGIN PROTECTION RULES

These rules are absolute and override any intelligence recommendation:

1. **20% floor is inviolable.** Any recommendation that would produce margin below 20% is automatically flagged `REQUIRES_FOUNDER_APPROVAL` and cannot be applied by Luciana.

2. **Vessel cost changes must cascade.** If Vessel_Cost increases, Pricing Intelligence must immediately flag all future bookings on that vessel for repricing review.

3. **No compound discounting.** Repeat client discount (5%) cannot stack with off-peak discount (7%). Only the higher discount applies per Commercial Authority Framework.

4. **Protected inventory override.** Any pricing recommendation for a vessel or date flagged as `Protected_Inventory` is automatically elevated to founder review regardless of margin status.

5. **Margin erosion alert.** If recommended price produces margin below 25%, a `MARGIN_CAUTION` flag is added to the recommendation even if it is above the 20% floor.

---

## SECTION 8: PRICING INTELLIGENCE ALERTS

| Alert | Trigger | Recipient |
|---|---|---|
| `PRICE_BELOW_FLOOR` | Recommendation would produce <20% margin | Founder (immediate) |
| `SURGE_WINDOW_ACTIVE` | Demand_Score >75 for 5+ days | Founder + Luciana |
| `PROTECTED_INVENTORY_PRICING` | Recommendation touches protected vessel/date | Founder |
| `MULTIPLIER_CAP_HIT` | Demand would justify >35% premium | Founder |
| `VESSEL_COST_CASCADE` | Vessel_Cost changes, future bookings affected | Luciana |
| `COMPOUND_DISCOUNT_ATTEMPT` | Two discount scenarios applied to same booking | Luciana (block + alert) |
| `STALE_RECOMMENDATION` | Pricing recommendation unreviewed for 72h | Luciana |

---

## SECTION 9: PRICE ELASTICITY TRACKING

Over time, the intelligence layer builds an elasticity picture by tracking:

- **Requests received** at each price point
- **Conversion rate** (Request → Confirmed Booking) by price bracket
- **Abandonment reason** (if captured in Requests.Lost_Reason field)
- **ABV trend** over rolling periods

This data accumulates in `Revenue_Snapshots` and is surfaced monthly in the Founder Dashboard. No autonomous action is taken on elasticity data — it informs founder pricing strategy discussions only.

### Elasticity Heuristics (to be validated by data over time)

| Price Increase | Expected Conversion Impact | Recommended Posture |
|---|---|---|
| +5–10% | Minimal (<2% conversion drop) | Proceed during surge |
| +10–20% | Moderate (2–8% conversion drop) | Surge windows only, founder aware |
| +20–35% | Significant (8–20% drop) | Founder approval required |
| >35% | Unpredictable | Founder decision only |

---

## SECTION 10: ANNUAL PRICING REVIEW TRIGGER

Pricing Intelligence generates an annual pricing review summary each January:

- ABV trend over 12 months vs prior year
- Close rate at each price tier
- Package mix shift (entry/mid/premium)
- Competitor positioning summary (manual)
- Recommended package price adjustments for review
- Recommended new add-on price points

The annual review requires founder approval before any price changes take effect in the Packages table.

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION.*
