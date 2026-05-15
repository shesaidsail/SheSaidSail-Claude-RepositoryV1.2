# REFERRAL INTELLIGENCE
**Document ID:** 10_REVENUE__REFERRAL_INTELLIGENCE_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

Referral Intelligence maps, scores, and optimizes the referral ecosystem that drives She Said Sail's most efficient revenue. A referred client closes at higher rates, spends more per booking, churns less, and refers again — compounding value across the network.

The referral system is not a loyalty program. It is a relationship honor system. The "mention your name" mechanic is mandatory — referrals are recognized and rewarded through personal acknowledgment and meaningful relationship investment, not points or transactional apps.

---

## SECTION 2: REFERRAL ECOSYSTEM ARCHITECTURE

She Said Sail receives referrals from three distinct source types with different tracking logic:

| Source Type | Tracked In | Commission | Intelligence Priority |
|---|---|---|---|
| **Client Word-of-Mouth** | Clients table (Referral_Source field) | None (relationship honor) | HIGH |
| **Affiliate / Partner** | Affiliates table + Referral_Chain_ID | 5% of gross revenue | HIGH |
| **Planner / Broker** | Partner_Outreach table | Per partnership agreement | HIGHEST |
| **Organic (No Attribution)** | Requests.Source = ORGANIC | None | MEDIUM (attribution gap) |

---

## SECTION 3: REFERRAL ATTRIBUTION MODEL

### Attribution Capture Point

Referral source is captured at the Request stage, not the Booking stage. Every inbound request must have a `Source` and `Referral_Source` field populated before a proposal is generated.

Fields (Requests table — existing, now intelligence-tracked):
- `Source`: ORGANIC / REFERRAL_CLIENT / AFFILIATE / PLANNER / PAID_AD / SOCIAL / UNKNOWN
- `Referral_Source_Client`: Linked to referring client record (if Source = REFERRAL_CLIENT)
- `Referral_Source_Affiliate`: Linked to affiliate record (if Source = AFFILIATE)
- `Referral_Source_Planner`: Linked to Partner_Outreach record (if Source = PLANNER)
- `Referral_Attribution_Confidence`: HIGH / MEDIUM / LOW (was referral explicitly stated vs inferred)

### Attribution Confidence Rules

| Scenario | Attribution_Confidence |
|---|---|
| Client explicitly names referrer during first contact | HIGH |
| Affiliate link used in booking URL | HIGH |
| Planner named by client in inquiry | HIGH |
| Client says "saw you on Instagram" after general search | LOW (Organic) |
| No source information captured | UNKNOWN — trigger Luciana follow-up |

**UNKNOWN Attribution Protocol:** If Source = UNKNOWN after first response, Luciana is prompted to ask naturally during the conversation: *"How did you hear about us?"* This is captured before proposal is sent.

---

## SECTION 4: REFERRAL QUALITY SCORING

Not all referrals are equal. A planner who sends 10 bookings worth $3,000 each is less valuable than one who sends 3 bookings worth $9,000 each. Referral Quality Score captures this nuance.

### Referral Quality Score Formula

Per referral source (client, affiliate, or planner):

```
Referral_Quality_Score (0–100) =
  (Close_Rate_Score × 0.30) +
  (Avg_Booking_Value_Score × 0.25) +
  (Volume_Score × 0.20) +
  (Margin_Score × 0.15) +
  (Repeat_Referral_Score × 0.10)
```

### Component Definitions

**Close_Rate_Score (0–30)**
| Referral Close Rate | Score |
|---|---|
| >75% | 30 |
| 60–75% | 24 |
| 45–60% | 17 |
| 30–45% | 10 |
| <30% | 4 |

**Avg_Booking_Value_Score (0–25)**
| Referred ABV vs City ABV | Score |
|---|---|
| >150% of city ABV | 25 |
| 120–150% | 20 |
| 100–120% | 15 |
| 80–100% | 9 |
| <80% | 3 |

**Volume_Score (0–20)**
| Total Referred Bookings LTD | Score |
|---|---|
| 10+ | 20 |
| 6–9 | 16 |
| 3–5 | 11 |
| 2 | 6 |
| 1 | 2 |

**Margin_Score (0–15)**
| Avg Net Margin of Referred Bookings | Score |
|---|---|
| >30% | 15 |
| 25–30% | 12 |
| 20–25% | 8 |
| <20% | 2 |

**Repeat_Referral_Score (0–10)**
| Has referred in 2+ distinct periods (years/seasons) | Score |
|---|---|
| Yes, 3+ periods | 10 |
| Yes, 2 periods | 6 |
| No (single period only) | 0 |

### Quality Score Tiers

| Score | Tier | Label | Treatment |
|---|---|---|---|
| 85–100 | Q1 | ELITE_REFERRER | Maximum recognition, relationship investment, co-marketing potential |
| 65–84 | Q2 | STRONG_REFERRER | Regular acknowledgment, occasional personal outreach |
| 45–64 | Q3 | MODERATE_REFERRER | Standard recognition, improve lead quality coaching for planners |
| 25–44 | Q4 | DEVELOPING | Monitor, light nurture |
| <25 | Q5 | LOW_QUALITY | Low investment; may be sending unqualified leads |

---

## SECTION 5: REFERRAL NETWORK MAPPING

The `Referral_Network` table captures the network topology — who refers whom, and how far connections extend.

### Referral_Network Table (New)

| Field | Type | Description |
|---|---|---|
| `Network_ID` | UUID | Immutable |
| `Referrer_Client` | Linked | Client who sent the referral |
| `Referred_Client` | Linked | New client who was referred |
| `Referral_Date` | Date | When referral was first attributed |
| `First_Booking_Date` | Date | When referred client first booked |
| `Attribution_Confidence` | Single Select | HIGH / MEDIUM / LOW |
| `Referral_Source_Type` | Single Select | CLIENT / AFFILIATE / PLANNER |
| `Revenue_Generated_By_Referred` | Rollup | Total revenue from referred client |
| `Network_Depth` | Number | 1st / 2nd / 3rd degree from original acquisition |
| `Chain_ID` | Text | Groups all referrals from same original source chain |
| `Environment` | Single Select | PRODUCTION / SANDBOX |

### Network Depth Tracking

```
Network Depth:
  Original acquisition = DEPTH_0
  Client referred by Depth_0 = DEPTH_1
  Client referred by Depth_1 = DEPTH_2
  ...

Chain_Revenue = SUM of all revenue across all bookings at every depth in chain
```

This reveals which original acquisition source (planner, paid ad, organic moment) has the highest viral coefficient.

---

## SECTION 6: REFERRAL MOMENT IDENTIFICATION

The intelligence system identifies optimal moments to facilitate a referral — neither too early (transactional) nor too late (missed window).

### Optimal Referral Moment Triggers

| Trigger | Timing | Action |
|---|---|---|
| `POST_CHARTER_PEAK` | D+3 after A-grade charter | Luciana prompted: *"This client had an exceptional experience — referral invite appropriate"* |
| `FIVE_STAR_REVIEW_RECEIVED` | Same day as review posted | Referral acknowledgment message drafted for Luciana review |
| `REPEAT_BOOKING_CONFIRMED` | When second booking confirmed | Personal note with referral mention (non-transactional) |
| `MILESTONE_CHARTER` | Client's 3rd or 5th booking | Milestone recognition + *"you're part of our closest circle"* framing |
| `AMBASSADOR_THRESHOLD` | Client has made 3+ referrals | Formal Ambassador acknowledgment prompt |
| `HIGH_ENTHUSIASM_SIGNAL` | Exceptional post-charter message or review language | Immediate Luciana alert for personal follow-up |

### Referral Moment CONTRAINDICATIONS

The system blocks referral invite prompts when:
- Charter_Grade was C, D, or F (experience was suboptimal)
- Client has an unresolved complaint or open escalation
- Client had a Chargeback_Risk incident
- It has been <72 hours since charter (too soon — let the experience settle)

---

## SECTION 7: REFERRAL REWARD ARCHITECTURE

Per `00_LOCKED_GOVERNANCE__Commercial_Authority_Framework_v1.0_PRODUCTION.md`, referral rewards are relationship-based, not transactional.

### Client-to-Client Referral

No monetary commission. Recognition is the reward:
- Personal thank-you from Luciana (named, not templated)
- Notation in client record (Referral_Count field)
- Future priority handling and proactive seasonal invitations
- If referral leads to 3+ bookings: Ambassador recognition, founder personal acknowledgment

### Affiliate Referral Commission

- **5% of gross revenue** for bookings with valid affiliate link
- Paid per confirmed booking (after deposit received)
- Tracked in Affiliates table: `Commission_Due`, `Commission_Paid`, `Payment_Date`
- Requires founder approval for any commission >$1,000 per booking

### Planner / Broker Referral

- Per individual partnership agreement (documented in Partner_Outreach)
- First-booking incentive: 10% discount to referred client (not to planner) — requires founder approval
- Ongoing: relationship investment, priority support, early access to calendar
- No per-referral cash payments unless specifically contracted

---

## SECTION 8: REFERRAL SOURCE PERFORMANCE TRACKING

Monthly report of referral source performance per city:

```
REFERRAL SOURCE PERFORMANCE — [Month] — [City]

Source Type     | Referrals | Close Rate | Avg Booking Value | Total Revenue | Quality Tier
CLIENT_REFERRAL |     12    |    71%     |     $5,800        |   $49,500     | Q2
PLANNER_XYZ     |     8     |    88%     |     $7,200        |   $50,600     | Q1
AFFILIATE_ABC   |     5     |    60%     |     $4,900        |   $14,700     | Q3
ORGANIC         |    24     |    38%     |     $4,200        |   $38,200     | —

INSIGHT: PLANNER_XYZ generates highest quality referrals. ORGANIC volume highest but lowest close rate and ABV.
RECOMMENDATION: Increase relationship investment in PLANNER_XYZ. Review organic conversion funnel.
```

---

## SECTION 9: VIRAL COEFFICIENT TRACKING

Viral Coefficient measures how many new clients each existing client generates over their lifetime:

```
Viral_Coefficient = Total_Referred_Bookings / Total_Client_Count

Target: Viral_Coefficient > 0.5 (every 2 clients generates 1 more)
Champion: Viral_Coefficient > 1.0 (referral machine)
```

When Viral_Coefficient falls below 0.3 for a rolling quarter:
- Alert generated for Luciana: *"Referral velocity declining — review post-charter follow-up sequence and referral moment identification"*
- Founder briefed in weekly revenue digest

---

## SECTION 10: REFERRAL INTELLIGENCE ALERTS

| Alert | Trigger | Recipient |
|---|---|---|
| `ELITE_REFERRER_COOLING` | Q1 referrer, 90+ days no referral | Luciana (relationship check-in prompt) |
| `HIGH_QUALITY_REFERRAL_RECEIVED` | New request attributed to Q1/Q2 referrer | Luciana (priority handling flag) |
| `REFERRAL_MOMENT_IDENTIFIED` | Post-charter peak, A-grade | Luciana (referral invite prompt) |
| `ATTRIBUTION_GAP` | >20% of requests in period are UNKNOWN source | Luciana (source capture reminder) |
| `VIRAL_COEFFICIENT_DROP` | Viral_Coefficient <0.3 for rolling quarter | Founder + Luciana |
| `AMBASSADOR_THRESHOLD_REACHED` | Client makes 3rd referral | Luciana (ambassador recognition prompt) |
| `AFFILIATE_COMMISSION_DUE` | Booking confirmed with affiliate link | Luciana (commission processing prompt) |
| `LOW_QUALITY_REFERRAL_PATTERN` | Referrer's last 3 referrals all lost, <30% close | Luciana (lead quality coaching flag) |

---

## SECTION 11: GOVERNANCE CONSTRAINTS

| Constraint | Source |
|---|---|
| Referral commissions >$1,000 require founder approval | Founder Control Framework |
| Planner first-booking discount (10%) requires founder approval | Commercial Authority Framework |
| No affiliate commissions paid without confirmed booking | Commercial Authority Framework |
| All referral reward acknowledgments are Tier B (Luciana review before send) | Founder Control Framework |
| Referral network data is PII-adjacent — City Manager access restricted | Founder Control Framework |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION.*
