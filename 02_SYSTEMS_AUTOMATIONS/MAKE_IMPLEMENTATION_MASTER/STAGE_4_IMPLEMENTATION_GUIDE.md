# STAGE_4_IMPLEMENTATION_GUIDE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Stage:** 4 — Advanced Scaling + Creative Intelligence
**Prerequisite:** Stages 1, 2, and 3 fully deployed and stable
**Goal:** Multi-city scaling engine. Creative intelligence. Platform-ready. Acquisition-ready.
**Classification:** Confidential — Internal Use Only

---

## STAGE 4 OVERVIEW

Stage 4 adds the scaling and creative intelligence infrastructure that supports 5+ cities, advanced content performance analysis, and executive-level reporting for investors and acquisition readiness. Stage 4 scenarios are more complex, more data-intensive, and carry more AI synthesis than prior stages.

Stage 4 principles:
- All Stage 4 AI outputs are Tier 2 or Tier 3 per the data reliability framework
- No Stage 4 scenario takes autonomous action on creative, financial, or personnel matters
- Every Stage 4 scenario that involves AI synthesis is Tier B minimum (human review required before action)
- Stage 4 scenarios can be deployed city-by-city as new markets are added — they are designed for selective activation

---

## SCENARIO 26: M-CREATIVE-INTELLIGENCE

**Purpose:** Weekly analysis of content performance patterns across SSS and ME. Identifies winning hooks, emotional categories, and platform patterns. Delivers actionable content intelligence to Will.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** A (analysis only; content recommendations go to Tier B)

**Module Sequence:**

```
1. Airtable > Search Records: Organic_Content
   — Filter: Published_Date >= today - 30 days
   — Fields: Platform, Content_Type, Hook_Classification, Emotional_Classification,
             Hook_Text, Performance_Score, Hook_Strength, Brand, Creator

2. Airtable > Search Records: Paid_Ads
   — Filter: Status IN [ACTIVE, COMPLETED] AND Budget_Period includes last 30 days
   — Fields: Platform, Ad_Name, CPL, ROAS, Bookings_Attributed, Spent, Status, Brand

3. Aggregate patterns:
   — Top 3 hook types by avg Performance_Score per brand
   — Top 3 emotional categories by conversion-correlated performance
   — Platform distribution: TikTok vs. Instagram performance delta
   — Creator correlation: internal vs. affiliate content performance

4. HTTP > Claude API call
   — Context: aggregated pattern data
   — Prompt: CREATIVE_INTELLIGENCE_SYSTEM
   — Output: creative intelligence brief per brand

5. Airtable > Create Records: two records in Organic_Content intelligence summary view
   (or a dedicated Creative_Intelligence_Log table if created)

6. Slack > DM to Will: "📊 Weekly Creative Intelligence — [SSS/ME] — Top hooks: [hook types] — Platform insight: [summary]"

7. Audit_Log entry
```

**Airtable Tables Touched:**
- Organic_Content (tbl09BGFacWim5Rk7): read
- Paid_Ads (tblVsxlNdP9xHDipE): read

**Failure Points:**
- Fewer than 5 content pieces in 30 days → insufficient data; notify Will ("Not enough content this month for pattern analysis")
- No Performance_Score populated → alert Luciana to enter performance data before next cycle

---

## SCENARIO 27: M-CREATIVE-FATIGUE

**Purpose:** Daily detection of creative fatigue in paid ads. Alert when CPL or ROAS indicates a creative is underperforming relative to its baseline.

**Trigger:** Schedule — daily 8:00 AM

**Autonomy Tier:** A (alert only; no autonomous ad pause or budget change)

**Module Sequence:**

```
1. Airtable > Search Records: Paid_Ads
   — Filter: Status = ACTIVE AND Environment = Production

2. For each active ad:
   a. Calculate: CPL_trend (current CPL vs. 7-day avg CPL)
   b. Calculate: ROAS_trend (current ROAS vs. 7-day avg ROAS)
   c. Fatigue threshold:
      — CPL increased > 40% vs. baseline AND ROAS dropped > 30% → FATIGUE_DETECTED

3. If FATIGUE_DETECTED on any ad:
   — Airtable > Update Record: Paid_Ads
     Fatigue_Flag = true
     Fatigue_Detected_At = {{now}}
   — Slack > DM to Will: "⚠️ CREATIVE FATIGUE — Ad: [Ad_Name] — CPL: +[%] — ROAS: -[%] — Recommend reviewing or pausing."
   — Note: Will makes all ad pause decisions. No autonomous ad changes.

4. Audit_Log entry
```

**Safety Note:** This scenario NEVER pauses ads autonomously. Ad spend decisions are Will-only. The scenario surfaces data and waits for human action.

---

## SCENARIO 28: M-SYNTER-SYNC

**Purpose:** Sync completed booking financial data to the SSS Financials base (P&L Per Charter table). Handles the cross-base limitation by making Make the bridge.

**Trigger:** Airtable webhook — Bookings.Status → COMPLETED

**Autonomy Tier:** A

**Module Sequence:**

```
1. Watch: Bookings.Status = COMPLETED

2. Airtable > Get Record: Booking (full)
   — Extract all financial fields:
     Gross_Revenue, Vessel_Cost, Labor_Cost, FB_Cost, Tax_Collected,
     Net_Revenue, Total_Cost, Net_Profit, Net_Margin_Pct,
     CM_Payout, Referral_Commission, Charter_Date, City, Brand,
     Package_Link, Client_Link, Booking_ID

3. SSS Financials Base > Airtable > Search Records: P&L Per Charter (tblFLiODVbQENbL5U)
   — Filter: Booking_ID = {{booking_id}}
   — If found → UPDATE existing record
   — If not found → CREATE new record

4. Airtable > Create/Update Record: P&L Per Charter
   — Fields mapped below (all singleLineText or Number — cross-base linked records not possible)

5. Airtable > Update Record: P&L Per Charter
   — Last_Sync_Timestamp → {{now}}
   — Sync_Status → SYNCED

6. Airtable > Update Record: Bookings (main base)
   — Financial_Sync_Status → SYNCED
   — Financial_Sync_At → {{now}}

7. Audit_Log entry
```

**P&L Per Charter Field Mapping (SSS Financials base):**

| Make Variable | Airtable Field | Type |
|--------------|---------------|------|
| `{{booking.Booking_ID}}` | Booking_ID | Text |
| `{{booking.Charter_Date}}` | Charter_Date | Date |
| `{{booking.Brand}}` | Brand | Text |
| `{{booking.City}}` | City | Text |
| `{{booking.Gross_Revenue}}` | Gross_Revenue | Currency |
| `{{booking.Net_Revenue}}` | Net_Revenue | Currency |
| `{{booking.Total_Cost}}` | Total_Cost | Currency |
| `{{booking.Net_Profit}}` | Net_Profit | Currency |
| `{{booking.Net_Margin_Pct}}` | Net_Margin_Pct | Percent |
| `{{booking.Vessel_Cost}}` | Vessel_Cost | Currency |
| `{{booking.Labor_Cost}}` | Labor_Cost | Currency |
| `{{booking.FB_Cost}}` | FB_Cost | Currency |
| `{{booking.Tax_Collected}}` | Tax_Collected | Currency |
| `{{booking.CM_Payout}}` | CM_Payout | Currency |
| `{{booking.Referral_Commission}}` | Referral_Commission | Currency |
| `{{now}}` | Last_Sync_Timestamp | DateTime |
| `SYNCED` | Sync_Status | Text |

**Failure Points:**
- P&L Per Charter record creation fails → SEV-2 → Sync_Status = FAILED → M-AUTOMATION-HEALTH catches 24hr stale sync
- M-AUTOMATION-HEALTH already monitors for completed bookings without a synced P&L record

---

## SCENARIO 29: M-CAMPAIGN-RECOMMENDER

**Purpose:** Weekly AI-generated campaign recommendation based on content performance, booking patterns, and market signals. Tier B — delivers to Will for review.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** B

**Module Sequence:**

```
1. Gather intelligence from prior M-CREATIVE-INTELLIGENCE run (Airtable read)

2. Airtable > Search Records: Bookings
   — Filter: Created_At >= today - 30 days
   — Group by: Source_Channel, Brand, City
   — Identify: highest converting lead sources

3. Airtable > Search Records: Paid_Ads
   — Top performers (ROAS > threshold) and fatigued (Fatigue_Flag = true)

4. HTTP > Claude API call
   — Context: creative performance, booking source attribution, fatigued ads, top performers
   — Prompt: CAMPAIGN_RECOMMENDER_SYSTEM
   — Output: campaign recommendation (labeled as AI guidance)

5. Airtable > Create Record: Founder_Decisions
   — Type = BRAND, Urgency = WHEN_AVAILABLE
   — Context = campaign recommendation
   — Clear label: "AI Campaign Recommendation — Review before any spend change"

6. Slack > DM to Will: "📣 Weekly Campaign Recommendation ready in Approval Queue"

7. Audit_Log entry (Approval_State = PENDING_HUMAN)
```

---

## SCENARIO 30: M-SOP-INTELLIGENCE

**Purpose:** Monthly analysis of the Lessons table to identify emerging SOPs, contradictions, and stale lessons. Surfaces governance maintenance recommendations.

**Trigger:** Schedule — first Monday of each month, 8:00 AM

**Autonomy Tier:** B

**Module Sequence:**

```
1. Airtable > Search Records: Lessons
   — All ACTIVE lessons, sorted by Severity and Created_At

2. Airtable > Search Records: Lessons
   — Filter: Status = ACTIVE AND Updated_At < today - 90 days
   — These are potentially stale

3. Airtable > Search Records: Founder_Decisions
   — Filter: Created_At >= today - 30 days AND Decision = APPROVED
   — These may contain patterns that should become lessons

4. HTTP > Claude API call
   — Context: all above
   — Prompt: SOP_INTELLIGENCE_SYSTEM
   — Output: recommended new lessons, stale lesson flags, contradiction identifications

5. Airtable > Create Record: Founder_Decisions
   — Type = SYSTEM, Urgency = WHEN_AVAILABLE
   — Context = SOP analysis
   — Proposed_Action: "Review flagged lessons. Create or archive as recommended."

6. Slack > DM to Will: "📚 Monthly SOP Intelligence Report in Approval Queue — [lesson count flagged]"

7. Audit_Log entry
```

---

## SCENARIO 31: M-CITY-LAUNCH

**Purpose:** Automate the checklist-driven launch sequence when a new city is activated by Will.

**Trigger:** Airtable webhook — Cities.Active → true

**Autonomy Tier:** B (launch is significant — all steps require human confirmation)

**Module Sequence:**

```
1. Watch: Cities.Active = true

2. Airtable > Get Record: City (full)
   — Validate launch requirements:
     a. Charter_Brief_Template exists? → if not: BLOCK + Will alert
     b. City_Manager linked? → if not: BLOCK + Will alert
     c. Minimum 2 vendors per service category? → if not: BLOCK + Will alert
     d. Tax_Rate set? → if not: BLOCK + Will alert
     e. Emergency_Contact documented? → if not: BLOCK + Will alert

3. If any blocks:
   — Slack > DM to Will: "🚫 CITY LAUNCH BLOCKED — [City] — Missing: [list]"
   — Airtable > Update Cities: Active = false (rollback activation until requirements met)
   — EXIT

4. If all checks pass:
   a. Slack > Post to #sss-ops-bookings: "🌊 NEW CITY LAUNCHING — [City] — [date]"
   b. Slack > DM to City Manager: Welcome message with Airtable access link and Charter Brief template
   c. Airtable > Create Record: Automation_Health (city launch event log)
   d. Airtable > Create Record: Founder_Decisions (Type = SYSTEM, Urgency = SAME_DAY) — "New city [X] launched. Confirm all pre-launch requirements manually."
   e. Gmail > Send city launch brief to City Manager

5. Audit_Log entry
```

**Failure Points:**
- City launched without charter brief template → blocked. Non-negotiable.
- City Manager Slack ID missing → email only for initial notification; Luciana follows up for Slack access

---

## SCENARIO 32: M-EXECUTIVE-DASHBOARD

**Purpose:** Daily feed of operational metrics to the executive dashboard Airtable interface.

**Trigger:** Schedule — daily 8:00 AM

**Autonomy Tier:** A

**Module Sequence:**

```
1. Aggregate across all active cities:
   — Today's charters (Charter_Date = today)
   — This week's bookings (new + confirmed)
   — MTD revenue (all brands)
   — Open leads (Requests.Status = NEW or AVAILABILITY_PENDING)
   — Pending founder approvals count
   — Automation health status (from M-AUTOMATION-HEALTH last run)

2. Airtable > Update or Create: Dashboard_Notes record
   — Executive_Dashboard_Last_Updated → {{now}}
   — Metrics stored as structured fields for interface display

3. Audit_Log entry
```

---

## SCENARIO 33: M-OWNER-HUB

**Purpose:** Weekly owner-level summary for any future investor reporting requirements or ownership review.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** A

**Module Sequence:**

```
1. Airtable > Search Records: Financial_Periods (SSS Financials base)
   — Most recent closed period

2. Airtable > Search Records: Bookings
   — This quarter completions, bookings pipeline next 30 days

3. Airtable > Search Records: Cities
   — City health scores, active cities

4. Compile: summary package — revenue, margin, city health, pipeline

5. Airtable > Update: Owner_Hub_Last_Updated

6. Slack > DM to Will: "Weekly Owner Hub Summary — [period] — $[revenue] — [margin%] — [pipeline]"

7. Audit_Log entry
```

---

## SCENARIO 34: M-OPS-HUB

**Purpose:** Daily operational feed for Luciana's ops hub interface. Surfaces what needs action today.

**Trigger:** Schedule — daily 7:30 AM

**Autonomy Tier:** A

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Charter_Date = today: active charters
   — Status = DEPOSIT_PAID: follow up needed
   — Balance_Due_Date = today: urgent balance collection

2. Airtable > Search Records: Requests
   — Status = NEW: unreviewed leads
   — Status = AVAILABILITY_PENDING: awaiting vessel confirmation

3. Airtable > Search Records: Founder_Decisions
   — Decision = blank (pending) AND Urgency = SAME_DAY

4. Compile: "Do This Now" list in priority order

5. Airtable > Update: Dashboard_Notes (ops hub section)

6. Slack > DM to Luciana: "📋 Today's Ops Hub — [charter count] charters today — [lead count] leads to review — [urgent count] urgent items"

7. Audit_Log entry
```

---

## STAGE 4 MULTI-CITY SCALING DESIGN

All Stage 4 scenarios are designed for multi-city operation. Key principles:

**Brand routing is always active** — every scenario reads the Brand field (SSS/ME) and City field before any processing. Intelligence aggregates across cities by default and can be filtered per city.

**City-specific activation:** M-CITY-LAUNCH controls when new city data enters the intelligence layer. New city data does not skew existing city intelligence for 30 days (warmup period).

**Scenario scaling:** All schedule-based scenarios use Airtable Search with Environment = Production and City = Active — they automatically include new cities as they launch. No scenario needs to be rebuilt for new cities.

**Creative intelligence by brand:** M-CREATIVE-INTELLIGENCE runs separately for SSS and ME by default (Brand field filter). A combined cross-brand report can be added as a variant in a later iteration.

---

## STAGE 4 SUCCESS CRITERIA

Stage 4 is complete when:

- [ ] M-CREATIVE-INTELLIGENCE delivering weekly insight for 4 consecutive weeks — Will confirms useful
- [ ] M-CREATIVE-FATIGUE alerting correctly on at least one fatigue event (verified vs. Stripe/ad dashboard)
- [ ] M-SYNTER-SYNC syncing completed bookings to P&L Per Charter — Sync_Status = SYNCED for 100% of completed bookings
- [ ] M-CITY-LAUNCH tested with a city activation/deactivation cycle in sandbox
- [ ] M-EXECUTIVE-DASHBOARD refreshing daily without errors for 2 weeks
- [ ] M-OPS-HUB tested by Luciana — confirms accurate and useful for daily operations
- [ ] All AI synthesis outputs reviewed by Will — confirms labeled correctly as Tier 2/3

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_4_IMPLEMENTATION_GUIDE v1.0*
*Effective May 2026*
