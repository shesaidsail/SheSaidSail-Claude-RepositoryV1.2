# CLIENT LIFETIME VALUE ENGINE
**Document ID:** 10_REVENUE__CLIENT_LTV_ENGINE_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

The Client LTV Engine computes, classifies, and predicts the lifetime revenue contribution of every client in the She Said Sail ecosystem. LTV scores drive prioritization decisions across every module — who gets VIP treatment, who gets proactive outreach, who gets upsell focus, and who is at churn risk.

LTV is not just historical spend. It is a forward-looking signal that combines what a client has generated with what they are likely to generate in the future.

---

## SECTION 2: LTV DEFINITION AND FORMULA

### Realized LTV (Historical)

```
Realized_LTV = SUM(Gross_Revenue) across all COMPLETED bookings for this client
```

This is the simplest and most accurate baseline. Sourced directly from Bookings table.

### Projected LTV (12-Month Forward)

```
Projected_LTV_12M =
  (Avg_Booking_Value × Booking_Frequency_Per_Year × 12_Month_Projection_Multiplier) +
  (Referral_Value_Score × Avg_Booking_Value)

Where:
  Avg_Booking_Value          = Realized_LTV / Total_Completed_Bookings
  Booking_Frequency_Per_Year = Total_Completed_Bookings / Client_Tenure_Years
  12_Month_Projection_Mult   = Based on Recency and Re-engagement probability (0.2–1.0)
  Referral_Value_Score       = Count of attributed referral bookings × 0.5 (network multiplier)
```

### Composite LTV Score (for tier classification)

```
Composite_LTV =
  (Realized_LTV × 0.50) +
  (Projected_LTV_12M × 0.35) +
  (Referral_Revenue_Attributed × 0.15)
```

---

## SECTION 3: LTV TIER CLASSIFICATION

| Tier | Label | Composite LTV Range | Share of Book | Treatment |
|---|---|---|---|---|
| T0 | NEW | <$3,000 | ~40% of clients | Standard service, conversion focus |
| T1 | BRONZE | $3,000–$7,499 | ~25% of clients | Repeat booking nurture |
| T2 | SILVER | $7,500–$14,999 | ~20% of clients | Loyalty recognition, upsell focus |
| T3 | GOLD | $15,000–$29,999 | ~10% of clients | VIP flag candidate, proactive care |
| T4 | PLATINUM | $30,000–$59,999 | ~4% of clients | HV_Client flag recommended, personal treatment |
| T5 | DIAMOND | $60,000+ | ~1% of clients | Founder awareness, maximum relationship investment |

**Note:** These dollar ranges are initial estimates. After 12 months of production data, the ranges should be recalibrated based on actual client distribution. Tier boundaries are founder-adjustable annually.

---

## SECTION 4: RFM SCORING ADAPTATION

RFM (Recency, Frequency, Monetary) is adapted for the charter business context. Each dimension is scored 1–5:

### Recency (R)

| Days Since Last Completed Charter | Score |
|---|---|
| 0–60 days | 5 |
| 61–120 days | 4 |
| 121–200 days | 3 |
| 201–365 days | 2 |
| >365 days | 1 |

### Frequency (F)

| Total Completed Charters | Score |
|---|---|
| 7+ | 5 |
| 4–6 | 4 |
| 3 | 3 |
| 2 | 2 |
| 1 | 1 |

### Monetary (M)

| Realized LTV | Score |
|---|---|
| >$30,000 | 5 |
| $15,000–$29,999 | 4 |
| $7,500–$14,999 | 3 |
| $3,000–$7,499 | 2 |
| <$3,000 | 1 |

### RFM Composite

```
RFM_Score = (R × 2) + (F × 2) + (M × 1)  [max: 25]
```

R and F are weighted higher than M because a recent, frequent client at lower spend is more valuable to the business trajectory than a high-spend churned client.

### RFM Segment Map

| RFM Range | Segment | Action |
|---|---|---|
| 20–25 | CHAMPION | Maximum relationship investment, referral invitation |
| 16–19 | LOYAL | Seasonal proactive outreach, upsell focus |
| 12–15 | PROMISING | Re-engagement sequence, next occasion capture |
| 8–11 | AT_RISK | Reactivation prompt to Luciana |
| <8 | LOST_CAUSE | Low outreach priority, passive re-engagement only |

---

## SECTION 5: CHURN RISK SCORING

Churn Risk predicts the probability that a client will not book again in the next 12 months.

### Churn Risk Factors

```
Churn_Risk_Score (0–100, higher = more at risk):

Base Risk by Frequency:
  1 booking only:   +40 (single-occasion clients churn at high rates)
  2 bookings:       +20
  3+ bookings:      +5

Recency Penalty:
  90–180 days since last booking:    +15
  181–365 days:                      +30
  >365 days:                         +50

Experience Quality Adjustment:
  Last charter grade A:              −20
  Last charter grade B:              −10
  Last charter grade C/D/F:          +25

Engagement Signal:
  Responded to last outreach:        −15
  Did not respond to last outreach:  +20
  Has upcoming inquiry:              −30 (active pipeline)

Final Churn_Risk_Score = (Base + Penalties − Deductions), clamped to 0–100
```

### Churn Risk Bands

| Score | Band | Action |
|---|---|---|
| 0–20 | LOW | Monitor only |
| 21–40 | MODERATE | Include in seasonal outreach |
| 41–60 | HIGH | Proactive re-engagement prompt to Luciana |
| 61–80 | CRITICAL | Luciana personal outreach + founder awareness if HV |
| 81–100 | LOST | Low-cost passive re-engagement only |

---

## SECTION 6: NEXT BOOKING PROBABILITY SCORE

This score (0–100) estimates the probability of a confirmed booking in the next 90 days. It feeds the Founder Dashboard's demand outlook and helps prioritize Luciana's outreach queue.

```
Next_Booking_Probability =
  (Frequency_Signal × 0.30) +
  (Recency_Momentum × 0.25) +
  (Seasonal_Match × 0.20) +
  (Active_Inquiry_Signal × 0.15) +
  (Occasion_Pattern_Match × 0.10)

Where:
  Frequency_Signal      = F_score / 5 × 100  (normalized RFM frequency)
  Recency_Momentum      = Inverse of Recency churn penalty, scaled 0–100
  Seasonal_Match        = Does this client's historical booking month match next 90 days?
  Active_Inquiry_Signal = 100 if open Request record exists, else 0
  Occasion_Pattern      = Does next 90 days contain client's known occasion type (bachelorette season, etc.)?
```

**Threshold for Outreach Prompt:** Next_Booking_Probability > 65 without an open Request record → generate re-engagement prompt for Luciana.

---

## SECTION 7: LTV ENGINE AIRTABLE ARCHITECTURE

### Client_LTV_Scores Table (New)

| Field | Type | Description |
|---|---|---|
| `Score_ID` | UUID | Immutable |
| `Client` | Linked | Client record |
| `Score_Date` | Date | Computation date |
| `Realized_LTV` | Currency | Historical gross revenue |
| `Projected_LTV_12M` | Currency | Forward 12-month projection |
| `Referral_Revenue_Attributed` | Currency | Revenue from referred bookings |
| `Composite_LTV` | Currency | Weighted LTV for tier classification |
| `LTV_Tier` | Single Select | NEW / BRONZE / SILVER / GOLD / PLATINUM / DIAMOND |
| `RFM_R` | Number | Recency score 1–5 |
| `RFM_F` | Number | Frequency score 1–5 |
| `RFM_M` | Number | Monetary score 1–5 |
| `RFM_Score` | Number | Composite RFM 5–25 |
| `RFM_Segment` | Single Select | CHAMPION / LOYAL / PROMISING / AT_RISK / LOST_CAUSE |
| `Churn_Risk_Score` | Number | 0–100 |
| `Churn_Risk_Band` | Single Select | LOW / MODERATE / HIGH / CRITICAL / LOST |
| `Next_Booking_Probability` | Number | 0–100 |
| `Prior_LTV_Tier` | Single Select | Tier from last computation (for upgrade detection) |
| `Tier_Changed` | Formula | TRUE if LTV_Tier ≠ Prior_LTV_Tier |
| `Environment` | Single Select | PRODUCTION / SANDBOX |

### Clients Table — New LTV Fields

| Field | Description |
|---|---|
| `LTV_Tier` | Lookup from latest Client_LTV_Scores record |
| `Churn_Risk` | Lookup from latest Client_LTV_Scores record |
| `Next_Booking_Probability` | Lookup from latest Client_LTV_Scores record |
| `Composite_LTV` | Lookup from latest Client_LTV_Scores record |
| `LTV_Tier_Changed_Flag` | Checkbox — triggers Luciana notification on tier upgrade |

---

## SECTION 8: LTV-DRIVEN PRIORITIZATION RULES

LTV scores drive prioritization across the operation:

### Inbound Request Prioritization

When multiple open requests exist simultaneously, Luciana's queue is sorted by:
1. HV_Client = TRUE (always first)
2. LTV_Tier: DIAMOND → PLATINUM → GOLD → SILVER → BRONZE → NEW
3. Churn_Risk = CRITICAL (elevated within tier)
4. Request creation timestamp

**This does not change response quality for any client. It changes response sequencing for Luciana's bandwidth management.**

### Upsell Targeting Priority

LTV tiers determine upsell approach:

| Tier | Upsell Strategy |
|---|---|
| DIAMOND / PLATINUM | Proactive premium package suggestion before they ask |
| GOLD / SILVER | Add-on bundle recommendation in proposal |
| BRONZE | Single high-value add-on recommendation |
| NEW | Standard package only — build trust before upselling |

### Reactivation Investment Level

| Churn Risk Band | Investment Level | Action |
|---|---|---|
| CRITICAL (DIAMOND/PLATINUM) | Maximum | Founder personal involvement, Luciana direct call |
| CRITICAL (GOLD/SILVER) | High | Luciana personal outreach, personalized offer context |
| CRITICAL (BRONZE/NEW) | Standard | Automated re-engagement email sequence |
| HIGH (any tier) | Medium | Seasonal outreach, occasion prompt |

---

## SECTION 9: REFERRAL VALUE IN LTV CALCULATION

Referral value is captured separately but included in Composite_LTV to properly credit clients who bring network value beyond their own direct spend.

```
Referral_Revenue_Attributed = SUM(Gross_Revenue of all bookings where Referral_Source = this client)

Referral_Value_Contribution_to_LTV = Referral_Revenue_Attributed × 0.15
```

The 0.15 multiplier ensures that a client who sends $50,000 in referral bookings adds $7,500 to their Composite_LTV — meaningful enough to influence tier, but not enough to inflate tiers artificially for clients who have never booked themselves.

---

## SECTION 10: LTV COMPUTATION CADENCE

| Computation | Frequency | Trigger |
|---|---|---|
| Full LTV refresh | Weekly (Sunday night) | Make scheduled trigger |
| Post-booking refresh | After every booking status change to COMPLETED | Make Stripe/Airtable webhook |
| Tier upgrade check | On every refresh | Formula field — Tier_Changed flag |
| Churn risk refresh | Weekly | Runs with full LTV refresh |
| Next_Booking_Probability | Weekly | Runs with full LTV refresh |
| Annual tier range recalibration | January each year | Founder review triggered by system |

---

## SECTION 11: LTV ALERTS

| Alert | Trigger | Recipient |
|---|---|---|
| `LTV_TIER_UPGRADE` | Client moves up one tier | Luciana (recognition prompt) |
| `DIAMOND_CHURN_RISK` | DIAMOND client, Churn_Risk = CRITICAL | Founder (immediate) |
| `PLATINUM_CHURN_RISK` | PLATINUM client, Churn_Risk = CRITICAL | Founder + Luciana |
| `GOLD_CHURN_RISK` | GOLD client, Churn_Risk = HIGH | Luciana |
| `HIGH_PROBABILITY_NO_INQUIRY` | Next_Booking_Probability >65 with no open Request | Luciana (outreach prompt) |
| `NEW_CLIENT_RAPID_REPEAT` | NEW client books second charter within 60 days | Luciana (loyalty recognition trigger) |
| `REFERRAL_VALUE_MILESTONE` | Client's Referral_Revenue_Attributed crosses $10K | Luciana (ambassador recognition prompt) |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION.*
