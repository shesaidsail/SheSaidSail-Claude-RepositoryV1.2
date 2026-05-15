# CONTENT_ROI_INTELLIGENCE

**Status:** DRAFT — Pre-Phase 4 Architecture
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail · Mare Executive
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Financial Authority:** 00_LOCKED_GOVERNANCE__Financial_OS_v1.0_PRODUCTION

---

> **Architecture Statement**
>
> This document specifies the Content ROI Intelligence system — the framework for tracking economic return across every creative investment: by asset, by creator, by editor, by hook type, by influencer, by repost, and through to booking attribution. It connects the creative intelligence layer to the financial intelligence layer. This document does not govern pricing or proposal systems. It governs creative spend return tracking.

---

## SECTION 1 — PURPOSE AND SCOPE

### 1.1 What This System Measures

Every creative decision is an investment. The Content ROI Intelligence system answers the questions that determine where to invest next:

- Which specific assets drove bookings?
- Which creators generate the most revenue per dollar spent?
- Which editors produce assets that perform best on paid?
- Which hook types are most profitable — not just most engaging?
- Which influencers are genuinely driving revenue vs. only generating vanity metrics?
- Which reposts and UGC shares drove inbound?
- What is the true cost per booking from content?

### 1.2 What This System Does Not Govern

- Overall marketing budget allocation (governed by Will + Financial_OS)
- Pricing or package margins (governed by Commercial_Authority_Framework)
- Contractor payment terms (governed by Financial_OS)
- Influencer contract terms (governed by Legal + Will)

### 1.3 Financial System Integration

Content ROI data flows between:
- **Creative Intelligence tables** (Creative_Assets, Campaign_Creatives, Winning_Creatives) — creative performance layer
- **SSS Operations Base** — Bookings, Affiliates, Influencers tables — attribution layer
- **SSS Financials Base** — P&L Per Charter, Expenses, Financial_Periods — financial layer

Make orchestrates the sync between these layers. Airtable linked records cannot cross bases, so Make writes attribution IDs across bases via field writes.

---

## SECTION 2 — ROAS BY ASSET

### 2.1 Asset-Level ROAS Tracking

Every Creative_Assets record accumulates revenue attribution through its linked Campaign_Creatives records. This produces an asset-level ROAS that tells Will exactly which pieces of content returned the most revenue per dollar spent.

### 2.2 Asset ROAS Calculation

**For Paid Assets:**
```
Asset_ROAS = Total_Revenue_Attributed / Total_Spend_Across_All_Deployments

Where:
- Total_Revenue_Attributed = SUM of Revenue_Attributed from all Campaign_Creatives records linked to this asset
- Total_Spend_Across_All_Deployments = SUM of Spend from all Campaign_Creatives records linked to this asset
```

**For Organic Assets:**
```
Organic_Asset_Revenue = SUM of Revenue_Attributed from all Organic_Content records linked to this asset

(Organic assets have no spend to divide — tracked as organic revenue yield, not ROAS)
```

### 2.3 New Fields Required in Creative_Assets

| Field | Type | Formula / Source |
|-------|------|-----------------|
| Total_Spend_All_Deployments | Rollup: SUM | Campaign_Creatives.Spend |
| Total_Revenue_Attributed | Rollup: SUM | Campaign_Creatives.Revenue_Attributed |
| Asset_ROAS | Formula | Total_Revenue_Attributed / Total_Spend_All_Deployments (paid only) |
| Organic_Revenue_Yield | Rollup: SUM | Organic_Content.Revenue_Attributed |
| Total_Bookings_Driven | Rollup: SUM | Campaign_Creatives.Bookings_Attributed |
| Revenue_Per_Booking | Formula | Total_Revenue_Attributed / Total_Bookings_Driven |
| Cost_Per_Booking | Formula | Total_Spend_All_Deployments / Total_Bookings_Driven |
| ROI_Tier | Formula | A (ROAS ≥ 4) / B (ROAS 2-4) / C (ROAS 1-2) / D (ROAS < 1) / Organic (no spend) |
| Lifetime_Value_Score | Number | Will-set: long-term brand value beyond direct ROAS (1–10 scale) |

### 2.4 Asset ROI Dashboard View (Airtable)

Grouped and sorted view in Creative_Assets:
- Sort by: Asset_ROAS descending (paid), Organic_Revenue_Yield descending (organic)
- Group by: Brand, then Platform_Primary
- Filter: Status ≠ ARCHIVED
- Show: Asset_ID, Asset_Name, Hook_Type, Emotional_Category, Asset_ROAS, Organic_Revenue_Yield, Total_Bookings_Driven, Cost_Per_Booking, ROI_Tier

---

## SECTION 3 — CREATOR ROI

### 3.1 Who Is a Creator

For ROI purposes, "creator" encompasses:
- Internal content creators (crew, editors shooting organic content)
- Influencers (tracked in Influencers table)
- Client UGC contributors
- Brand partners who produce content

### 3.2 Creator ROI Table — New Table Required

| Table | ID Prefix | Role |
|-------|-----------|------|
| Creator_ROI | CROI | Aggregated performance and financial return per creator identity |

### 3.3 Creator_ROI Table — Full Field Specification

#### Universal Fields

| Field | Type |
|-------|------|
| UUID | Formula: RECORD_ID() |
| CROI_ID | Formula: CROI-YYYY-NNNN |
| Created_At | Created Time |
| Updated_At | Last Modified Time |
| Source_System | Single Select: Make / Manual |
| Environment | Single Select |
| Brand | Single Select |
| City | Single Select |

#### Creator Identity Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creator_Name | Single Line Text | Full name or handle |
| Creator_Type | Single Select | Influencer / Internal / Client_UGC / Brand_Partner |
| Influencer_Link | Link to Influencers | For influencer creators |
| Affiliate_Link | Link to Affiliates | For affiliate creators |
| Creator_Handle | Single Line Text | Social handle (@name) |
| Primary_Platform | Single Select | TikTok / Instagram / Both |
| Follower_Count | Number | At time of most recent campaign |
| Contract_Status | Single Select | Active / Expired / One_Off / No_Contract |

#### Investment Fields

| Field | Type | Source |
|-------|------|--------|
| Total_Fees_Paid | Currency | From Expenses records linked to this creator |
| Total_Products_Gifted_Value | Currency | Estimated value of gifted charters or experiences |
| Total_Investment | Formula | Total_Fees_Paid + Total_Products_Gifted_Value |
| Investment_Period | Single Select | Per_Campaign / Monthly / Quarterly / Annual |

#### Creative Output Fields

| Field | Type | Source |
|-------|------|--------|
| Total_Assets_Produced | Count | Creative_Assets linked (Creator_Link = this record) |
| Assets_Approved | Count | Assets with Status = APPROVED or higher |
| Assets_Deployed | Count | Assets with Status = DEPLOYED |
| Winners_Produced | Count | Assets linked to Winning_Creatives |
| Winner_Rate | Formula | Winners_Produced / Assets_Deployed * 100 |
| Avg_Performance_Score | Rollup: AVG | Creative_Scoring for this creator's assets |

#### Revenue Attribution Fields

| Field | Type | Source |
|-------|------|--------|
| Direct_Bookings_Attributed | Number | Bookings with Source = this creator (tracking link or mention) |
| Assisted_Bookings_Attributed | Number | Bookings where creator content assisted but not direct source |
| Total_Revenue_Attributed | Currency | From attributed Bookings.Revenue |
| Creator_ROAS | Formula | Total_Revenue_Attributed / Total_Investment |
| Revenue_Per_Asset | Formula | Total_Revenue_Attributed / Assets_Deployed |
| Cost_Per_Booking_Creator | Formula | Total_Investment / Direct_Bookings_Attributed |

#### Qualitative Fields

| Field | Type | Values |
|-------|------|--------|
| Brand_Alignment_Score | Number (1–10) | Will-set: how well creator aligns with SSS/ME brand positioning |
| Content_Quality_Score | Number (1–10) | Will-set: raw content quality rating |
| Relationship_Quality | Single Select | Excellent / Good / Adequate / Poor |
| Renewal_Recommendation | Single Select | Renew / Negotiate / Do_Not_Renew |
| Will_Notes | Long Text | Founder's qualitative assessment |

---

## SECTION 4 — EDITOR ROI

### 4.1 Editor Tracking Purpose

Editors are a creative investment. Different editors produce assets with different performance profiles. Editor ROI tracking identifies which editing styles, paces, and talent produce winning assets — so investment in editing can be optimized.

### 4.2 Editor Performance Fields in Creative_Assets

| Field | Type | Values / Rules |
|-------|------|----------------|
| Editor | Single Line Text | Editor name or contractor ID |
| Editor_Contractor_Link | Link to Contractors | Linked to Contractors table record |
| Editor_Fee | Currency | Fee paid for this specific asset edit |

### 4.3 Editor ROI View (Airtable)

A grouped view on Creative_Assets:
- Group by: Editor
- Show: Asset count, Avg Performance_Score, Winner count, Winner Rate, Total editor fees (from Expenses), Avg ROAS of deployed assets
- Sort by: Avg Performance_Score descending

This view gives Will visibility into which editors produce the highest-performing assets relative to their cost.

### 4.4 Editor Fields in Contractors Table

Add to existing Contractors table:

| Field | Type | Purpose |
|-------|------|---------|
| Editor_Specialty | Single Select | Short_Form_Video / Long_Form / Static / Motion_Graphics / All |
| Total_Assets_Edited | Count | Creative_Assets with Editor_Contractor_Link = this record |
| Avg_Asset_Score | Rollup: AVG | From Creative_Scoring via Creative_Assets |
| Winners_Produced | Count | Creative_Assets linked to Winning_Creatives |
| Editor_ROAS_Contribution | Rollup: AVG | Avg ROAS of deployed assets edited by this contractor |
| Total_Editing_Fees_Paid | Rollup: SUM | From Expenses.Amount where Contractor_Link = this record + type = Editing |

---

## SECTION 5 — HOOK PROFITABILITY

### 5.1 Hook Type as Investment Signal

Hook type is a structural creative decision that determines the first 2–5 seconds. Hook type profitability analysis tells Will: which type of creative opening structure delivers the best return on the total cost of producing and deploying that asset.

### 5.2 Hook Profitability Tracking

In Creative_DNA table and as a reporting view across Creative_Assets + Creative_Scoring:

**Hook Profitability Report (monthly, CREATIVE-009 component):**

| Hook Type | Assets Deployed | Avg Performance Score | Avg ROAS | Avg Completion Rate | Avg Cost Per Booking | Winner Rate |
|-----------|-----------------|----------------------|----------|---------------------|----------------------|-------------|
| Curiosity | [N] | [score] | [ROAS] | [%] | [$] | [%] |
| Social_Proof | [N] | [score] | [ROAS] | [%] | [$] | [%] |
| Transformation | [N] | [score] | [ROAS] | [%] | [$] | [%] |
| Emotion | [N] | [score] | [ROAS] | [%] | [$] | [%] |
| Authority | [N] | [score] | [ROAS] | [%] | [$] | [%] |
| Contrast | [N] | [score] | [ROAS] | [%] | [$] | [%] |

This report reveals: which hook type is most profitable, which is overused, which is underserved.

### 5.3 Hook Profitability Fields in Creative_DNA

| Field | Type | Source |
|-------|------|--------|
| Avg_ROAS_This_Pattern | Rollup: AVG | Campaign_Creatives.ROAS via Winning_Creatives |
| Avg_Completion_Rate | Rollup: AVG | Campaign_Creatives.Completion_Rate_Pct |
| Avg_Cost_Per_Booking | Rollup: AVG | Campaign_Creatives.Cost_Per_Booking |
| Total_Revenue_Generated | Rollup: SUM | Campaign_Creatives.Revenue_Attributed |
| Bookings_Generated | Rollup: SUM | Campaign_Creatives.Bookings_Attributed |

---

## SECTION 6 — INFLUENCER ROI

### 6.1 Influencer vs. Creator ROI

Influencer ROI is tracked at a finer level than general creator ROI. Influencers involve contracts, deliverable commitments, tracking links, and often gifted charter experiences — making their investment profile more complex to measure accurately.

### 6.2 Influencer-Specific Fields in Influencers Table

Add to Influencers table (existing, to be migrated from appVWYY9Fp6tKu94m):

| Field | Type | Values / Rules |
|-------|------|----------------|
| Contract_Value | Currency | Total contracted fee (excluding gifted value) |
| Gifted_Charter_Value | Currency | Estimated retail value of gifted charter experience |
| Total_Influencer_Investment | Formula | Contract_Value + Gifted_Charter_Value |
| Deliverables_Contracted | Number | Number of posts/videos agreed |
| Deliverables_Received | Number | Number of posts actually delivered |
| Deliverable_Rate | Formula | Deliverables_Received / Deliverables_Contracted * 100 |
| Tracking_Link | URL | UTM-tracked link for direct attribution |
| Promo_Code | Single Line Text | If discount code used for attribution |
| Direct_Bookings | Number | Bookings via tracking link or promo code |
| Assisted_Bookings | Number | Bookings that mentioned influencer |
| Total_Revenue_From_Direct | Currency | Revenue from direct bookings |
| Influencer_ROAS | Formula | Total_Revenue_From_Direct / Total_Influencer_Investment |
| Avg_Views_Per_Post | Number | Average views across all delivered posts |
| Avg_Engagement_Rate | Number | Average engagement rate across posts |
| Follower_Quality_Score | Number (1–10) | Will-set: estimated audience quality (real vs. inflated) |
| Brand_Fit_Score | Number (1–10) | Will-set: how well influencer embodies SSS/ME brand |
| Net_Value_Score | Formula | Influencer_ROAS * Brand_Fit_Score / 10 (balanced return metric) |
| Renewal_Status | Single Select | Renew / Negotiate / Do_Not_Renew / Pending_Review |
| Campaign_Link | Link to Creative_Assets | All assets produced by this influencer |
| Creator_ROI_Link | Link to Creator_ROI | Aggregated creator record |

### 6.3 Influencer Attribution Rules

| Scenario | Attribution Method |
|----------|-------------------|
| Booking via tracking link | Strong direct attribution — write Campaign_Creative.Bookings_Attributed |
| Booking mentions promo code | Strong direct attribution |
| Client mentions influencer by name in intake | Moderate assisted attribution — logged to Bookings.Attribution_Notes |
| Client says "saw it on social" — no specific creator | Weak — logged as Unattributed_Organic |
| Booking occurs > 30 days after post | Attribution not credited unless explicit tracking link used |

---

## SECTION 7 — REPOST PERFORMANCE

### 7.1 Repost Tracking Purpose

When SSS or ME content is reposted by followers, planners, or partners, that repost can drive inbound. Tracking repost performance identifies: which content earns organic amplification and what the revenue value of that amplification is.

### 7.2 Repost Tracking Fields in Organic_Content

| Field | Type | Values / Rules |
|-------|------|----------------|
| Repost_Count | Number | Number of confirmed reposts tracked |
| Notable_Repost_Accounts | Long Text | Accounts that reposted with significant reach — manually logged |
| Repost_Reach_Estimated | Number | Estimated additional reach from reposts |
| Repost_Attributed_Inquiries | Number | Inbound inquiries mentioning a repost |
| Repost_Attributed_Bookings | Number | Bookings traced to repost amplification |
| Repost_Revenue | Currency | Revenue from Repost_Attributed_Bookings |
| Viral_Flag | Checkbox | True = content exceeded 10x typical reach through organic sharing |

### 7.3 Planner and Partner Repost Tracking

Partners (planners, affiliates) who repost SSS content contribute to distribution. Track in Partner_Outreach and Affiliates tables:

| Field (add to Affiliates) | Type | Purpose |
|--------------------------|------|---------|
| Content_Shared_Count | Number | How many times this affiliate has shared SSS content |
| Referral_Content_Link | Link to Organic_Content | Which specific content they shared |
| Bookings_From_Shared_Content | Number | Bookings sourced from their sharing |
| Content_Sharing_Value | Currency | Revenue from Bookings_From_Shared_Content |

---

## SECTION 8 — BOOKING ATTRIBUTION ARCHITECTURE

### 8.1 Attribution Model Summary

| Attribution Type | Strength | Source Signal |
|-----------------|----------|---------------|
| Direct paid — tracking link click + booking within 72h | Strong | Meta/TikTok API + Booking.Source |
| Influencer — tracking link or promo code | Strong | Tracking link + Booking.Promo_Code |
| Organic — booking mentions specific content | Moderate | Luciana manually notes in Booking.Attribution_Notes |
| Planner referral — planner credits specific content | Moderate | Partner_Outreach + Booking.Referral_Source |
| Dark social — "saw it somewhere" | Weak | Booking.Attribution_Notes = "Organic unattributed" |
| Repeat client — previous content drove initial booking | Historical | Booking.Client_Source = Prior_Charter |

### 8.2 Booking Attribution Fields in Bookings Table

Add to existing Bookings table:

| Field | Type | Values |
|-------|------|--------|
| Attribution_Type | Single Select | Paid_Direct / Influencer / Organic_Named / Planner_Referral / Dark_Social / Repeat_Client / Word_Of_Mouth / Unknown |
| Attribution_Source | Single Line Text | Campaign name, influencer handle, planner name, content piece ID |
| Content_Asset_Link | Single Line Text | CA-YYYY-NNNN (Creative_Assets record — string field due to cross-table limitation) |
| Attribution_Notes | Long Text | Luciana's notes from intake conversation |
| Attribution_Confidence | Single Select | Strong / Moderate / Weak |

### 8.3 Attribution Reporting (Quarterly)

Quarterly report (CREATIVE-QUARTERLY-001) summarizes attribution across all bookings:

```
ATTRIBUTION REPORT — Q[N] [YYYY]

TOTAL BOOKINGS: [N] | TOTAL REVENUE: [$]

BY ATTRIBUTION TYPE:
- Paid Direct: [N] bookings / [$] revenue / [%] of total
- Influencer: [N] / [$] / [%]
- Organic Named: [N] / [$] / [%]
- Planner Referral: [N] / [$] / [%]
- Dark Social: [N] / [$] / [%]
- Unknown: [N] / [$] / [%]

TOP PERFORMING ASSETS (by bookings attributed):
1. [CA-ID] — [N] bookings — [$] revenue — ROAS [value]
2. [CA-ID] — ...
3. [CA-ID] — ...

TOP PERFORMING INFLUENCERS:
1. [Handle] — [N] bookings — [$] revenue — ROAS [value]
2. ...

CONTENT INVESTMENT SUMMARY:
Total creative spend this quarter: [$]
Total influencer investment: [$]
Total editing investment: [$]
Total content-attributed revenue: [$]
Overall content ROAS: [value]

RECOMMENDATIONS:
[AI-generated: 3 specific investment shifts based on ROI data]
```

---

## SECTION 9 — ROI INTELLIGENCE VIEWS (AIRTABLE)

### 9.1 Required Airtable Views

| View Name | Base Table | Group By | Sort By | Purpose |
|-----------|------------|----------|---------|---------|
| Asset ROI Leaderboard | Creative_Assets | Brand | Asset_ROAS desc | Which assets returned most |
| Creator Performance | Creator_ROI | Creator_Type | Creator_ROAS desc | Which creators deliver most |
| Hook Profitability | Creative_DNA | Hook_Type | Avg_ROAS desc | Which hooks are most profitable |
| Influencer ROI | Influencers | — | Influencer_ROAS desc | Which influencers drive most revenue |
| Attribution Overview | Bookings | Attribution_Type | Revenue desc | How bookings are sourced |
| Fatigue vs ROAS | Creative_Fatigue | Platform | Score_Decay_Pct desc | Fatigue impact on ROAS |

---

## SECTION 10 — GOVERNANCE

Content ROI Intelligence data is financial intelligence. It informs creative investment decisions and creator contract renewals. It is treated as confidential.

**Access:**
- Will: full access to all ROI views and reports
- Luciana: read access to attribution tracking only (no influencer contract values)
- Finance: read access to quarterly attribution reports
- Creators: no access to their own ROI data unless Will decides to share in negotiations

**Data Integrity:**
- Attribution data once set is never modified without a Founder Decision
- Revenue attribution figures that inform financial period reports must reconcile with Bookings.Total_Revenue
- No ROI figure is reported to any external party without Will approval

This document is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 00_LOCKED_GOVERNANCE__Financial_OS_v1.0_PRODUCTION
- 00_LOCKED_GOVERNANCE__Commercial_Authority_Framework_v1.0_PRODUCTION

---

SHE SAID SAIL · CONTENT ROI INTELLIGENCE
CONFIDENTIAL · INTERNAL USE ONLY
