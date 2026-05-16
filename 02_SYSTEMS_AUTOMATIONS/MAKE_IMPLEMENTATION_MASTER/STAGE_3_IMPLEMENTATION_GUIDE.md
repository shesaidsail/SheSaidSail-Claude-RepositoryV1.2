# STAGE_3_IMPLEMENTATION_GUIDE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Stage:** 3 — Intelligence Layer
**Prerequisite:** Stages 1 and 2 fully deployed and stable
**Goal:** Operational intelligence + founder leverage. Decision support. NOT autonomous control.
**Classification:** Confidential — Internal Use Only

---

## STAGE 3 OVERVIEW

Stage 3 adds the intelligence layer that converts raw operational data into actionable insight for the founder and operations lead. All Stage 3 outputs are classified as Tier 2 (Operational Intelligence) or Tier 3 (AI Guidance) per the Systems Intelligence Architecture data reliability framework. Stage 3 scenarios provide information and recommendations. They do not make decisions. They do not take autonomous actions on business-critical matters without human review.

Stage 3 runs alongside Stages 1 and 2. No Stage 3 scenario replaces or overrides any Stage 1 or Stage 2 scenario.

**AI Authority in Stage 3:**
- Stage 3 uses Claude API calls for synthesis and pattern recognition
- Every Claude API call uses the current production prompt version from AI_Prompt_Versions
- Every Claude output is logged in Audit_Log with Approval_State classification
- Intelligence outputs are delivered as Slack messages or Airtable record updates — not autonomous decisions
- Intelligence outputs are clearly labeled "AI suggests" or "based on recent patterns" — never presented as Tier 1 facts

---

## SCENARIO 18: M-AI-LEAD-SCORING

**Purpose:** Score every new inbound Request for conversion likelihood and priority. Allows Luciana to prioritize follow-up intelligently.

**Trigger:** Airtable webhook — Requests.Status → NEW (immediately after M-LEAD-INTAKE creates the record)

**Autonomy Tier:** A (score is written to Airtable; no outbound action taken based on score alone)

**Module Sequence:**

```
1. Watch: Requests.Status = NEW

2. Airtable > Get Record: Request (full)
   — Check: Environment = Production

3. Airtable > Get Record: Client (if email matches existing Client)
   — Extract: booking history, charter grades, HV_Client status, LTV

4. Assemble scoring context:
   — Lead source (organic search vs. paid ad vs. referral)
   — Group size (larger groups = higher revenue signal)
   — Occasion (bachelorette and corporate score higher for SSS/ME respectively)
   — Charter date (< 30 days = urgent, > 90 days = exploratory)
   — Message quality (notes length, specificity, questions asked)
   — Prior booking history from matched Client record

5. HTTP > Claude API call
   — Prompt version: AI_Prompt_Versions where Make_Variable_Name = "LEAD_SCORING_SYSTEM"
   — Output: JSON with:
     score: 0-100
     priority: HIGH / MEDIUM / LOW
     confidence: HIGH / MEDIUM / LOW
     key_signals: [list of 2-3 signals that drove the score]
     recommended_action: brief text

6. Airtable > Update Record: Requests
   — AI_Lead_Score → {{score}}
   — AI_Lead_Priority → {{priority}}
   — AI_Scoring_Confidence → {{confidence}}
   — AI_Lead_Signals → {{key_signals}} (Long Text)
   — AI_Scored_At → {{now}}

7. If score >= 80 (HIGH priority):
   — Slack > DM to Luciana: "🔥 HIGH PRIORITY LEAD — [Name] — Score: [score] — [key signal 1] — [key signal 2]"

8. Audit_Log entry
   — Prompt_Version, AI_Confidence_Score, Output summary
   — Approval_State = AUTONOMOUS
```

**Data Reliability:** This is Tier 2 intelligence — based on real records, refreshed on every new lead. Not a prediction. Not a guarantee.

**Failure Points:**
- Claude API unavailable → write AI_Lead_Score = null, AI_Lead_Priority = "UNSCORED" → Luciana manually prioritizes
- Existing Client record not found → score based on lead data alone; note "First-time lead — no history" in signals

---

## SCENARIO 19: M-LTV-ENGINE

**Purpose:** Update client LTV (Lifetime Value) every time a booking is completed. Track repeat client value.

**Trigger:** Airtable webhook — Bookings.Status → COMPLETED

**Autonomy Tier:** A

**Module Sequence:**

```
1. Watch: Bookings.Status = COMPLETED

2. Airtable > Get Record: Booking
   — Extract: Client_Link, Package_Price, Add_Ons_Total, Net_Profit

3. Airtable > Get Record: Client

4. Airtable > Search Records: Bookings
   — Filter: Client_Link = {{client_id}} AND Status = COMPLETED
   — Count: total completed bookings
   — Sum: total revenue across all completed bookings
   — Calculate: average charter value

5. Airtable > Update Record: Client
   — Total_Bookings_Completed → {{count}}
   — Total_Revenue_LTV → {{total_revenue}}
   — Avg_Charter_Value → {{average_value}}
   — Last_Charter_Date → {{booking.charter_date}}
   — LTV_Updated_At → {{now}}

6. If Total_Bookings_Completed >= 3 AND HV_Client = false:
   — Airtable > Update Client: HV_Client = true
   — Slack > DM to Luciana + Will: "⭐ HV CLIENT UPGRADE — [Name] — [count] bookings — $[total LTV] — Upgraded to HV status"
   — Note: Luciana reviews before any change in communication approach

7. Audit_Log entry
```

**Failure Points:**
- Client record not linked to Booking → log warning, skip LTV update, alert Luciana

---

## SCENARIO 20: M-REVENUE-HEALTH

**Purpose:** Daily revenue health check. Surface revenue trends, outstanding balances, and margin alerts.

**Trigger:** Schedule — daily 8:00 AM

**Autonomy Tier:** A

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: Environment = Production
   — Filter: Status IN [CONFIRMED, DEPOSIT_PAID, PAID, COMPLETED]
   — Filter: Charter_Date >= start of current month

2. Aggregate by status:
   — MTD_Revenue_Booked = sum of Package_Price for CONFIRMED + DEPOSIT_PAID + PAID + COMPLETED
   — MTD_Revenue_Collected = sum for PAID + COMPLETED
   — Deposits_Pending = count of DEPOSIT_PAID (balance not yet collected)
   — Outstanding_Balances = sum of (Package_Price - Deposit_Amount) for DEPOSIT_PAID
   — Avg_Net_Margin_MTD = average Net_Margin_Pct for COMPLETED this month

3. Check margin alerts:
   — Any booking Net_Margin_Pct < 20% AND Status != COMPLETED → Luciana alert

4. Check balance due alerts:
   — Any booking where Charter_Date < today + 5 days AND Status = DEPOSIT_PAID (balance not collected) → urgent alert

5. Airtable > Update or Create Record: City_Financials (per city)
   — Revenue metrics updated

6. Slack > Post to #sss-ops-alerts:
   Daily Revenue Health Report
   — MTD Booked: $[amount]
   — MTD Collected: $[amount]
   — Outstanding Balances: $[amount] ([count] bookings)
   — Avg Margin MTD: [%]
   — Alerts: [any margin or balance due alerts]

7. Audit_Log entry
```

**Data Classification:** Tier 1 for revenue figures (read directly from Airtable confirmed records). Tier 2 for trend observations.

**Failure Points:**
- Bookings table not accessible → SEV-2 → Luciana reviews manually
- City_Financials table not created (Stage 2 dependency) → log locally only until table exists

---

## SCENARIO 21: M-PRICING-INTELLIGENCE

**Purpose:** Weekly analysis of package pricing vs. achieved margins. Surface where pricing may be underperforming. Tier B — delivers recommendation to Will for review, not autonomous action.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** B (Claude generates recommendation; Will reviews before any pricing change)

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: Status = COMPLETED AND Charter_Date >= today - 90 days

2. Airtable > Search Records: Packages
   — All active packages (Live = true)

3. Per package: calculate
   — Bookings_Count (last 90 days)
   — Avg_Net_Margin_Achieved
   — vs. Packages.Margin_Floor_Pct
   — Avg_Add_Ons_Revenue per booking

4. HTTP > Claude API call
   — Context: package data, achieved margins, booking frequency
   — Prompt: PRICING_INTELLIGENCE_SYSTEM
   — Output: recommendations per package

5. Airtable > Create Record: Founder_Decisions
   — Type = SYSTEM, Urgency = WHEN_AVAILABLE
   — Context = Claude pricing analysis
   — Proposed_Action = AI recommendation (labeled "AI suggestion — review before action")

6. Slack > DM to Will: "📊 Weekly Pricing Intelligence ready for review in Approval Queue — [package names with alerts]"

7. Audit_Log entry (Approval_State = PENDING_HUMAN)
```

---

## SCENARIO 22: M-FOUNDER-DIGEST

**Purpose:** Weekly Thursday digest for Will. Consolidates lessons, approvals, patterns, anomalies, and intelligence into one actionable summary.

**Trigger:** Schedule — Thursday 5:00 PM

**Autonomy Tier:** A (Tier A for delivery; Tier B for AI synthesis — labeled clearly)

**Module Sequence:**

```
1. Airtable > Search Records: Lessons
   — Filter: Status = ACTIVE AND Created_At >= today - 7 days
   — Retrieve: Title, Severity, AI_Prompt_Tag, Will_Approved, Outcome

2. Airtable > Search Records: Founder_Decisions (Approval Queue)
   — Filter: Decision = blank (pending) AND Urgency IN [IMMEDIATE, SAME_DAY, THIS_WEEK]

3. Airtable > Search Records: Bookings
   — This week's completions, this week's new bookings, pipeline for next 30 days

4. Airtable > Search Records: Audit_Log
   — Filter: Created_At >= today - 7 days AND Approval_State = AUTONOMOUS
   — Count by Brand and scenario

5. Airtable > Search Records: Automation_Health
   — Filter: Created_At >= today - 7 days
   — Anomaly count and categories

6. HTTP > Claude API call
   — Context: all above data assembled
   — Prompt: FOUNDER_DIGEST_SYSTEM
   — Output: structured digest

7. Slack > DM to Will:
   Subject: Thursday Digest — [Date]
   Sections:
   — Pending Approvals: [count] items waiting
   — This Week's Operations: [booking counts, completions, revenue collected]
   — New Lessons: [count] — [titles]
   — Automation Health: [clean/anomalies]
   — AI Observations: [Claude's synthesized patterns — labeled as AI guidance]
   — Autonomy Candidates: [categories approved 5 consecutive times]

8. Slack > DM to Luciana: same digest

9. Audit_Log entry
```

**AI Labeling Requirement:** All Claude-generated synthesis sections must be prefixed with "AI suggests:" or "Based on recent patterns:" per the data reliability tier requirements in Systems Intelligence Architecture Section 7.2.

---

## SCENARIO 23: M-CITY-HEALTH

**Purpose:** Daily city health score update. Feeds the City_Health_Score field on each City record.

**Trigger:** Schedule — daily 8:00 AM

**Autonomy Tier:** A

**Module Sequence:**

```
1. Airtable > Search Records: Cities
   — Filter: Active = true

2. For each City:
   a. Get recent Bookings (last 30 days, completed):
      — Avg_Charter_Grade (A=4, B=3, C=2, D=1, F=0)
      — Booking count
      — Avg_Net_Margin_Pct
      — Incident count (Emergency_Flag events)
      — Vendor_Ratings_Entered count

   b. Calculate City_Health_Score (0-100):
      — Charter grade component (40%): Avg_Charter_Grade / 4 × 40
      — Margin component (30%): Avg_Margin_Pct / target_margin × 30
      — Volume component (20%): normalized bookings vs. expected
      — Incident penalty (10%): −5 per incident in 30 days

   c. Airtable > Update Record: City
      — City_Health_Score → {{score}}
      — Health_Score_Updated_At → {{now}}
      — City_Status: if score < 50 → flag for Will review (not automatic change)

3. Slack > #sss-ops-alerts: daily city health summary
   — "[City]: [score] — [status]" per city

4. If any city < 50:
   — Slack > DM to Will: "⚠️ CITY HEALTH ALERT — [City] scored [score]. Review recommended."

5. Audit_Log entry
```

**Failure Points:**
- No completed bookings in 30 days → score is null, note "Insufficient data" — not a health alert

---

## SCENARIO 24: M-PARTNER-SCORING

**Purpose:** Weekly quality score for partners (affiliates, brokers, planners). Surface high-performing and underperforming relationships.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** A

**Module Sequence:**

```
1. Airtable > Search Records: Affiliates
   — All active affiliates

2. Airtable > Search Records: Partner_Outreach
   — Filter: Stage = ACTIVE_PARTNER

3. For each partner:
   a. Linked bookings (last 90 days): count, total revenue, avg charter grade
   b. Referral conversion rate: Bookings / Referral_Leads_Sent
   c. Response rate (for outreach partners)

4. Airtable > Update Records: Affiliates
   — Partner_Score → calculated score (0-100)
   — Score_Updated_At → {{now}}

5. Slack > DM to Luciana: weekly partner scorecard summary

6. Audit_Log entry
```

---

## SCENARIO 25: M-CONCIERGE-INTELLIGENCE

**Purpose:** Weekly concierge performance report. Identifies patterns across city managers.

**Trigger:** Schedule — Monday 8:00 AM (weekly)

**Autonomy Tier:** B (report generated; Will reviews before any personnel action)

**Module Sequence:**

```
1. Airtable > Search Records: Concierge_Operators
   — All active operators

2. For each operator:
   a. Linked completed Bookings (last 30 days): count, avg charter grade, incident count
   b. Charter_Brief_All_Vendors_Confirmed rate
   c. Escalation count (from Emergency_Escalations linked to their city)

3. HTTP > Claude API call
   — Context: operator performance data
   — Prompt: CONCIERGE_INTELLIGENCE_SYSTEM
   — Output: performance narrative per operator + any flags

4. Airtable > Create Record: Founder_Decisions
   — If any operator flags: Type = PERSONNEL, Urgency = THIS_WEEK
   — AI recommendation labeled as guidance only

5. Slack > DM to Will: "Concierge performance report in Approval Queue — [operator names with flags if any]"

6. Audit_Log entry (Approval_State = PENDING_HUMAN)
```

---

## STAGE 3 SUCCESS CRITERIA

Stage 3 is complete when:

- [ ] M-AI-LEAD-SCORING scoring at least 5 real leads with reasonable scores (human-validated)
- [ ] M-LTV-ENGINE updating Client records on every booking completion
- [ ] M-REVENUE-HEALTH posting daily to #sss-ops-alerts with accurate figures (verified vs. Airtable manually)
- [ ] M-FOUNDER-DIGEST delivered Thursday for 2 consecutive weeks — Will confirms useful and accurate
- [ ] M-CITY-HEALTH scoring all active cities daily
- [ ] All AI outputs labeled with appropriate data reliability tier
- [ ] Will has reviewed at least one M-PRICING-INTELLIGENCE and one M-CONCIERGE-INTELLIGENCE output and confirmed format is actionable

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_3_IMPLEMENTATION_GUIDE v1.0*
*Effective May 2026*
