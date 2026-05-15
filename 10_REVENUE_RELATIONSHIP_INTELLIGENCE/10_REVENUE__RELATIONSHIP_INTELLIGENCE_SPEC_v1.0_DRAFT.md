# RELATIONSHIP INTELLIGENCE SPECIFICATION
**Document ID:** 10_REVENUE__RELATIONSHIP_INTELLIGENCE_SPEC_v1.0_DRAFT
**Status:** DRAFT
**Authority:** Subordinate to all LOCKED governance documents
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Founder (Will)

---

## SECTION 1: PURPOSE

Relationship Intelligence tracks the depth, health, and revenue potential of every relationship in the She Said Sail ecosystem — clients, brokers, planners, affiliates, and corporate accounts. It surfaces signals that prevent relationship decay, identify upsell moments, and flag VIP handling requirements before problems occur.

Relationships are the primary moat of the business. Relationship Intelligence exists to ensure no high-value relationship goes cold through operational oversight.

---

## SECTION 2: RELATIONSHIP ECOSYSTEM MAP

The SSS relationship ecosystem contains five distinct relationship types, each with different scoring logic and action triggers:

| Relationship Type | Primary Table | Revenue Mechanism | Intelligence Priority |
|---|---|---|---|
| **Direct Client** | Clients | Repeat bookings, upsell | HIGHEST |
| **Event Planner / Broker** | Partner_Outreach | Volume referrals, repeat groups | HIGH |
| **Affiliate** | Affiliates | Commission-driven referrals | MEDIUM |
| **Corporate Account** | Clients (Corporate_Flag) | Multi-booking, executive retreats | HIGH |
| **VIP / Whale Client** | Clients (HV_Client) | Premium pricing, referral network | HIGHEST |

---

## SECTION 3: CLIENT RELATIONSHIP SCORING

### Relationship Score Components

Each client receives a Relationship_Score (0–100) computed from five dimensions:

```
Relationship_Score =
  (Recency_Score × 0.25) +
  (Engagement_Depth_Score × 0.20) +
  (Experience_Quality_Score × 0.25) +
  (Revenue_Contribution_Score × 0.20) +
  (Responsiveness_Score × 0.10)
```

### Component Definitions

**Recency_Score (0–25)**
Measures days since last meaningful interaction (booking, inquiry, response):

| Days Since Last Contact | Score |
|---|---|
| 0–30 days | 25 |
| 31–60 days | 20 |
| 61–90 days | 14 |
| 91–180 days | 8 |
| 181–365 days | 3 |
| >365 days | 0 |

**Engagement_Depth_Score (0–20)**
Measures quality of interactions, not just volume:

| Factor | Points |
|---|---|
| Has completed 2+ charters | +8 |
| Has responded to post-charter follow-up | +4 |
| Has referred at least 1 booking | +5 |
| Has left a review (4+ stars) | +3 |
| Max | 20 |

**Experience_Quality_Score (0–25)**
Derived from Charter_Grade history:

| Charter Grade Average | Score |
|---|---|
| All A grades | 25 |
| Mostly A/B | 20 |
| Mix of A/B/C | 14 |
| Any D/F grades | 8 |
| No completed charters | 12 (neutral pending) |

**Revenue_Contribution_Score (0–20)**
Derived from LTV_Tier (see CLIENT_LTV_ENGINE.md):

| LTV Tier | Score |
|---|---|
| DIAMOND | 20 |
| PLATINUM | 17 |
| GOLD | 13 |
| SILVER | 9 |
| BRONZE | 5 |
| NEW | 3 |

**Responsiveness_Score (0–10)**
Measures how quickly client engages with communications:

| Response Pattern | Score |
|---|---|
| Responds within 2 hours consistently | 10 |
| Responds same day | 7 |
| Responds within 48 hours | 4 |
| Slow / inconsistent | 1 |
| No response to last 2 outreaches | 0 |

### Relationship Score Tiers

| Score | Tier | Label | Handling |
|---|---|---|---|
| 85–100 | 1 | CHAMPION | Proactive VIP treatment, referral invitation |
| 70–84 | 2 | LOYAL | Priority handling, upsell focus |
| 55–69 | 3 | ENGAGED | Standard premium service, re-engagement check |
| 40–54 | 4 | COOLING | Re-engagement prompt to Luciana |
| <40 | 5 | AT_RISK | Alert to Luciana, founder-level flag if HV_Client |

---

## SECTION 4: VIP CLIENT PROTOCOL

VIP / HV_Client flag is set manually by founder or Luciana. Relationship Intelligence governs what happens once that flag is set.

### VIP Triggers (Automatic Flag Recommendations)

The system recommends HV_Client flag when ANY of the following occur:
- Client has completed 3+ bookings
- Client's cumulative revenue exceeds $15,000 LTD
- Client has referred 2+ confirmed bookings
- Client has been explicitly marked high-value by founder decision
- Client is known to be a public figure, executive, or influencer (manual input)

Recommendations appear in Approval_Queue for Luciana review. Founder must approve flag activation.

### VIP Handling Rules (Once HV_Client = TRUE)

| Scenario | Rule |
|---|---|
| Inbound inquiry | Response within 2 hours (Luciana review required) |
| Request for custom package | Escalate to Luciana immediately, no AI-only response |
| Complaint or dissatisfaction | Immediate L3 escalation per emergency protocol |
| Post-charter follow-up | Luciana personal touchpoint, not automated sequence |
| Re-engagement (90+ days no booking) | Luciana outreach prompt generated with context |
| Discount request | Escalate to founder — no autonomous decision |
| Anniversary / milestone | Relationship_Milestone alert generated 14 days in advance |

### VIP Communication Standards

All VIP client communications must:
- Be reviewed by Luciana before send
- Reference specific past experience details (vessel, date, occasion)
- Offer proactive upgrade or exclusive option — never a discount
- Sound personal, not templated
- Match brand voice exactly (per Brand Governance)

---

## SECTION 5: BROKER AND PLANNER RELATIONSHIP SCORING

Event planners and brokers receive a Relationship_Depth_Score separate from client scoring. They are revenue multipliers — a single strong planner relationship can generate 10–30 bookings annually.

### Broker/Planner Score Components

```
Relationship_Depth_Score =
  (Booking_Volume_Score × 0.30) +
  (Revenue_Attributed_Score × 0.25) +
  (Recency_Score × 0.20) +
  (Lead_Quality_Score × 0.15) +
  (Engagement_Score × 0.10)
```

### Component Definitions

**Booking_Volume_Score (0–30)**
| Referral Bookings LTD | Score |
|---|---|
| 10+ | 30 |
| 6–9 | 24 |
| 3–5 | 17 |
| 1–2 | 8 |
| 0 (prospect) | 0 |

**Revenue_Attributed_Score (0–25)**
Gross revenue generated through this planner, compared to city average planner:
| Relative Revenue | Score |
|---|---|
| >2× city avg | 25 |
| 1.5–2× city avg | 20 |
| 1–1.5× city avg | 14 |
| Below city avg | 7 |

**Lead_Quality_Score (0–15)**
| Factor | Points |
|---|---|
| Close rate on referred leads >60% | +8 |
| Average referred booking value above ABV | +4 |
| Referrals are pre-qualified (minimal back-and-forth) | +3 |

**Relationship Tier (Brokers/Planners)**

| Score | Tier | Action |
|---|---|---|
| 80–100 | STRATEGIC PARTNER | Priority support, exclusive windows, relationship investment |
| 60–79 | ACTIVE PARTNER | Regular outreach, upsell education, co-marketing |
| 40–59 | DEVELOPING | Quarterly check-in, improve lead quality coaching |
| <40 | PROSPECT | Structured outreach sequence |

---

## SECTION 6: RELATIONSHIP LIFECYCLE STAGES

Every client moves through defined lifecycle stages. Intelligence triggers are mapped to stage transitions:

```
PROSPECT → FIRST_INQUIRY → FIRST_BOOKING → REPEAT_CLIENT → LOYAL → CHAMPION → AMBASSADOR
```

| Stage | Definition | Intelligence Trigger |
|---|---|---|
| PROSPECT | No inquiry yet; referral or lead source | None (pre-system) |
| FIRST_INQUIRY | Has submitted request, not yet booked | Close_Rate optimization signal |
| FIRST_BOOKING | Completed exactly 1 charter | D7 review sequence, upsell next booking prompt |
| REPEAT_CLIENT | 2–3 completed charters | Loyalty recognition, relationship score activated |
| LOYAL | 4–6 charters or $10K+ LTV | Proactive seasonal outreach, referral invitation |
| CHAMPION | 7+ charters or $20K+ LTV, or 3+ referrals | HV_Client flag review, personalized milestone treatment |
| AMBASSADOR | Active referrer with 5+ referred bookings | Formalized referral relationship, special acknowledgment |

### Stage Transition Alerts

| Transition | Alert Type | Recipient |
|---|---|---|
| FIRST_INQUIRY → stall 14+ days | `LEAD_COOLING` | Luciana |
| FIRST_BOOKING → 90 days no repeat | `REPEAT_OPPORTUNITY` | Luciana |
| REPEAT → LOYAL milestone | `MILESTONE_REACHED` | Luciana (recognition prompt) |
| LOYAL → CHAMPION | `VIP_FLAG_RECOMMENDED` | Founder (approval required) |
| CHAMPION → 120 days no contact | `CHAMPION_AT_RISK` | Founder (personal alert) |
| Any stage → AMBASSADOR recognition | `AMBASSADOR_ELIGIBLE` | Luciana |

---

## SECTION 7: RELATIONSHIP INTELLIGENCE AIRTABLE FIELDS

### Clients Table — New Fields

| Field | Type | Description |
|---|---|---|
| `Relationship_Score` | Formula/Number | Computed 0–100 relationship health score |
| `Relationship_Tier` | Formula/Single Select | CHAMPION / LOYAL / ENGAGED / COOLING / AT_RISK |
| `Lifecycle_Stage` | Single Select | PROSPECT through AMBASSADOR |
| `Days_Since_Last_Contact` | Formula | Today minus last inbound/outbound date |
| `Relationship_Milestone_Date` | Date | Next significant milestone (anniversary, birthday) |
| `VIP_Flag_Recommended` | Checkbox | Recommended by system, pending founder approval |
| `Planner_Relationships` | Linked | Linked planner/broker records |
| `Last_Charter_Grade` | Lookup | Most recent charter grade |
| `Re_Engagement_Due` | Formula | TRUE if Days_Since_Last_Contact > 90 and Stage = LOYAL+ |
| `Referral_Network_Depth` | Number | Count of clients referred by this client |

### Relationship_Scores Table (New)

| Field | Type | Description |
|---|---|---|
| `Score_ID` | UUID | Immutable |
| `Client` | Linked | Client or Partner_Outreach record |
| `Relationship_Type` | Single Select | CLIENT / BROKER / AFFILIATE / CORPORATE |
| `Score_Date` | Date | When score was computed |
| `Total_Score` | Number | 0–100 |
| `Recency_Component` | Number | Component score |
| `Engagement_Component` | Number | Component score |
| `Experience_Component` | Number | Component score |
| `Revenue_Component` | Number | Component score |
| `Tier` | Single Select | CHAMPION / LOYAL / ENGAGED / COOLING / AT_RISK |
| `Prior_Score` | Number | Prior period score for trend |
| `Score_Delta` | Formula | Total_Score − Prior_Score |
| `Alert_Generated` | Checkbox | Whether an alert was sent this cycle |
| `Environment` | Single Select | PRODUCTION / SANDBOX |

---

## SECTION 8: PROACTIVE RELATIONSHIP TRIGGERS

The system generates proactive outreach prompts (for Luciana review and action) based on the following triggers. None are sent automatically — all are Tier B actions requiring human review.

| Trigger | Condition | Prompt Type |
|---|---|---|
| `RE_ENGAGEMENT` | LOYAL+ client, 90+ days no booking | Personalized check-in with next occasion suggestion |
| `ANNIVERSARY` | 1-year anniversary of first charter | Acknowledgment + exclusive seasonal offer invitation |
| `BIRTHDAY` | Client birthday (if captured) 14 days out | Personal birthday message + booking invitation |
| `SEASONAL_PEAK` | LOYAL+ client + upcoming peak window | Early access invitation framing |
| `POST_REFERRAL_THANKS` | New booking attributed to this client's referral | Personal thank-you (non-transactional) |
| `MILESTONE_RECOGNITION` | Stage upgrade to LOYAL, CHAMPION, or AMBASSADOR | Personal recognition message |
| `PLANNER_RECONNECT` | Strategic partner planner, 45+ days no contact | Reconnect prompt with value summary |
| `COLD_CHAMPION_ALERT` | CHAMPION stage, 120+ days no contact | Founder personal alert + Luciana outreach prompt |

---

## SECTION 9: CORPORATE ACCOUNT INTELLIGENCE

Corporate accounts (client hosting, executive retreats, networking events) receive additional intelligence tracking:

| Field | Description |
|---|---|
| `Corporate_Account_Flag` | Boolean — identified as corporate buyer |
| `Corporate_Annual_Value` | Projected annual booking value |
| `Decision_Maker_Contact` | Named contact who approves bookings |
| `Booking_Seasonality` | When they tend to book (Q1, summer, year-end) |
| `Preferred_Vessel` | Noted preference |
| `Billing_Entity` | Corporate name for invoice |
| `Account_Manager` | Luciana or City Manager designation |

Corporate accounts with annual projected value >$25,000 are automatically reviewed for STRATEGIC_PARTNER classification.

---

## SECTION 10: GOVERNANCE CONSTRAINTS

| Constraint | Source |
|---|---|
| All client outreach requires Luciana review (Tier B minimum) | Founder Control Framework |
| HV_Client flag requires founder approval | Founder Control Framework |
| VIP comms cannot be fully automated | Brand Governance + Founder Control |
| Relationship data is PII — City Managers have no access | Founder Control Framework |
| All relationship alerts logged to Audit_Log | Operational Memory Layer |
| Competitor relationship data (broker poaching) is founder-only | Commercial Authority Framework |

---

*This document is DRAFT status. Requires founder review and approval before elevation to PRODUCTION.*
