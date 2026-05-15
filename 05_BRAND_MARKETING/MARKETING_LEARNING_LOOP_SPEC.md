# MARKETING_LEARNING_LOOP_SPEC

**Status:** DRAFT — Pre-Phase 4 Architecture
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail · Mare Executive
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Architecture Statement**
>
> This document specifies the complete Marketing Learning Loop — the full lifecycle from content upload through AI tagging, Airtable sync, campaign creation, Synter deployment, performance tracking, winner analysis, and next-generation creative recommendations. Each stage is specified with: inputs, processing logic, outputs, Make scenario IDs, Airtable record changes, and human approval gates. This is the flywheel architecture that makes the SSS creative system self-improving over time.

---

## SECTION 1 — LOOP OVERVIEW

### 1.1 The Learning Loop Concept

The Marketing Learning Loop is a continuous intelligence cycle. Every piece of content that enters the system teaches the system something. Every campaign that runs produces data. Every winner identified refines the next brief. The loop never closes — it compounds.

```
Content Upload
    ↓
AI Tagging (classification + brand compliance)
    ↓
Airtable Sync (record creation + metadata write)
    ↓
Campaign Creation (brief + approval + launch)
    ↓
Platform Deployment (Synter / Meta / TikTok)
    ↓
Performance Tracking (live data sync)
    ↓
Winner Analysis (scoring + pattern extraction)
    ↓
Next-Generation Recommendations (brief regeneration)
    ↑______________________________________________↑
```

Each revolution of the loop produces: better briefs, better assets, better performance.

### 1.2 Human Gates in the Loop

The loop is AI-accelerated but human-governed. Every material decision passes through a human gate.

| Stage | Human Gate | Gatekeeper |
|-------|------------|------------|
| Asset approval | Will reviews APPROVED queue | Will |
| Campaign brief | Will approves before any asset deploys | Will |
| Budget release | Will approves any spend increase | Will |
| Winner promotion | Will approves Winning_Creatives entry | Will |
| DNA pattern approval | Will approves Creative_DNA record | Will |
| Next-gen brief | Will reviews before release to creator | Will |

AI accelerates every stage. AI controls none of them.

---

## SECTION 2 — STAGE 1: CONTENT UPLOAD

### 2.1 Upload Methods

| Method | Source | Who Uploads |
|--------|--------|-------------|
| Manual Google Drive upload | Editor, creator, crew | Any authorized team member |
| Influencer content drop | Influencer submits via shared link or folder | Influencer; Luciana receives |
| Client UGC | Client submits via intake form or DM | Luciana receives and uploads |
| Charter crew capture | Crew uploads from shoot | Crew member or Luciana |
| AI-assisted capture (future) | Automated from approved platforms | TikTok / Meta API (pending activation) |

### 2.2 Upload Requirements

Before any file is considered entered into the loop, it must meet:

| Requirement | Rule |
|-------------|------|
| Naming convention | Must follow [BRAND]_[CITY]_[ASSET_TYPE]_[YYYY-MM-DD]_[DESCRIPTOR]_[VERSION].[EXT] |
| Correct folder | Must land in the correct Google Drive folder path |
| Partial tags | Uploader must tag file description with #brand, #city, #type at minimum |
| Raw footage | Raw footage goes to `00_RAW_FOOTAGE/` — never directly to edited folders |

Files that violate naming conventions are flagged by Make (CREATIVE-UPLOAD-001 pre-validation) and routed to Luciana for correction before entering the loop.

### 2.3 Make Scenario: CREATIVE-UPLOAD-001

| Property | Value |
|----------|-------|
| Trigger | New file detected in designated Google Drive folders (webhook or 30-min scheduled scan) |
| Pre-validation | Check filename against naming convention regex; check folder location |
| If invalid | Create Airtable Dashboard_Notes record: "Upload naming error — file: [name]"; Slack alert to Luciana |
| If valid | Parse filename components (brand, city, type, date, descriptor); create Creative_Assets record |
| Fields written | Asset_Name, Brand, City, Asset_Type, Shoot_Date (from filename), Google_Drive_URL, Status = REVIEW_PENDING |
| Next trigger | Status = REVIEW_PENDING triggers CREATIVE-001 (AI Tagging) |

---

## SECTION 3 — STAGE 2: AI TAGGING

### 3.1 Tagging Purpose

AI tagging is the intelligence entry point. When an asset reaches `Status = REVIEW_PENDING`, Claude classifies it across all Creative DNA dimensions. This converts an unstructured media file into structured intelligence.

### 3.2 Make Scenario: CREATIVE-001

| Property | Value |
|----------|-------|
| Trigger | Creative_Assets: Status = REVIEW_PENDING |
| Claude context | Asset metadata + Google Drive file description tags + brand governance context |
| Claude input | Asset_Name, Asset_Type, Brand, Hook_Text (if available), Duration, Creator_Type |
| Claude output | Full classification JSON (see CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 10.1) |
| Fields written | Hook_Type, Emotional_Category, Emotional_Arc, Energy_Profile, Pacing, Music_Style, Platform_Fit, CTA_Present, CTA_Type, Luxury_Moment_Type, Brand_Compliance_Flag, Brand_Compliance_Notes, AI_Confidence_Score |
| Low confidence rule | If AI_Confidence_Score < 70: Status = REVIEW_PENDING; route to Will with confidence flag |
| Brand violation rule | If Brand_Compliance_Flag = true: create Founder Decision (Type = BRAND_COMPLIANCE_REVIEW); Slack DM to Will; Status stays REVIEW_PENDING |
| Clean asset rule | If Brand_Compliance_Flag = false AND confidence ≥ 70: Status = APPROVED_PENDING_WILL_REVIEW |

### 3.3 Will's Daily Review Queue

At 9am daily (CREATIVE-DAILY-001), Make generates a Slack summary to Will:

```
Good morning. Creative review queue:

BRAND_COMPLIANCE_REVIEW: [N] assets flagged
APPROVED_PENDING_WILL_REVIEW: [N] assets ready for approval
LOW_CONFIDENCE_TAGS: [N] assets need manual classification

Review: [Airtable interface link]
```

Will reviews and either:
- Approves (Status = APPROVED)
- Requests revision (Status = NEEDS_REVISION; notes added)
- Archives (Status = ARCHIVED)
- Corrects AI tags (manual field edit logged to Audit_Log)

### 3.4 Tag Quality Learning

When Will corrects an AI tag, Make writes to AI_Audit table:

| Field | Value |
|-------|-------|
| Table | Creative_Assets |
| Record_ID | The CA record corrected |
| Action | AI_Tag_Correction |
| AI_Output | What Claude classified |
| Human_Correction | What Will changed it to |
| Correction_Type | Hook_Type / Emotional_Category / Brand_Compliance / etc. |

This AI_Audit accumulates into training signals for prompt refinement. Quarterly, Will reviews AI_Audit corrections to recalibrate the tagging prompt.

---

## SECTION 4 — STAGE 3: AIRTABLE SYNC

### 4.1 Sync Architecture

Airtable is the single source of truth for all creative intelligence. Google Drive holds files. Airtable holds meaning.

After AI tagging completes, the Creative_Assets record is fully populated. Downstream tables are notified via linked records and Make triggers.

### 4.2 Sync Cascade After Asset Approval

```
Creative_Assets: Status = APPROVED
    ↓
Make writes #status:APPROVED to Google Drive file description (color label update)
    ↓
Make writes #airtable:[CA-ID] to Google Drive file description
    ↓
Organic_Content record created (if organic use intended): linked to Creative_Assets
    ↓
Luciana notified via Slack: "[CA-ID] approved — ready for campaign creation"
    ↓
Will's weekly creative report updated (accumulated count)
```

### 4.3 Cross-Table Sync Rules

| Source Change | Downstream Effect |
|---------------|-------------------|
| Creative_Assets Status = APPROVED | Notify Luciana; update Google Drive label |
| Creative_Assets Brand_Compliance_Flag = true | Founder Decision created; Will alerted |
| Campaign_Creatives created | Organic_Content or Paid_Ads record updated with Campaign_Creative link |
| Campaign_Creatives performance data updated | Creative_Scoring recalculated |
| Creative_Scoring tier = A or A+ | Winning_Creatives eligibility flagged; Founder Decision created |
| Winning_Creatives Will_Approved = true | Google Drive file label = Blue (winner); DNA pattern extraction triggered |
| Creative_Fatigue Fatigue_Status = CONFIRMED | Campaign_Creatives Deployment_Status updated; Will alerted |

---

## SECTION 5 — STAGE 4: CAMPAIGN CREATION

### 5.1 Campaign Creation Flow

Campaign creation begins after an asset is APPROVED and Will has decided to deploy it.

**Organic Campaign:**
```
Luciana selects approved asset in Airtable interface
    ↓
Creates Organic_Content record (or updates existing)
    ↓
Links to Creative_Assets record
    ↓
Sets: Platform, Planned_Publish_Date, Caption (draft from AI or manual)
    ↓
Routes to Will for caption and timing approval
    ↓
Will approves → Status = READY_TO_PUBLISH
    ↓
Makes scenario CREATIVE-ORG-001: notifies Luciana; schedules reminder
```

**Paid Campaign:**
```
Will or Luciana identifies asset for paid deployment
    ↓
Creates Paid_Ads record linked to Creative_Assets
    ↓
Sets: Platform, Budget, Campaign_Name, Target_Audience, Ad_Set
    ↓
Creates Campaign_Creatives record linking asset to campaign
    ↓
Routes to Will for budget approval (Founder Decision if > approved cap)
    ↓
Will approves → Status = READY_FOR_SYNTER
    ↓
Make scenario CREATIVE-PAID-001: notifies team; prepares Synter deployment package
```

### 5.2 Caption Generation (AI-Assisted)

When an asset is APPROVED and Organic_Content record is created:

CREATIVE-CAPTION-001 (Make): 
- Claude receives: Asset metadata, Hook_Type, Emotional_Category, Platform, Brand
- Claude generates: 3 caption variants (short / medium / story format)
- Variants route to Will or Luciana for selection and edit
- Selected caption stored in Organic_Content.Caption field

Caption rules from Master Brand Governance apply to all AI-generated captions:
- Short sentences preferred
- No em dashes
- No prohibited words
- No fake scarcity
- No corporate jargon

### 5.3 Audience Targeting Intelligence

For paid campaigns, Make injects Winning_Creatives data into the targeting recommendation:

CREATIVE-TARGETING-001 (Make):
- Claude receives: Asset DNA classification, Winning_Creatives with similar DNA, their best-performing audience segments (from Meta/TikTok API data)
- Claude returns: Recommended audience segments, platform targeting parameters, budget allocation suggestion
- Recommendation routes to Will for approval before any targeting is set

---

## SECTION 6 — STAGE 5: SYNTER DEPLOYMENT

### 6.1 What is Synter

Synter is the paid media deployment layer for SSS campaigns. All paid creative deployments flow through Synter before reaching Meta and TikTok platforms.

### 6.2 Deployment Package

When Will approves a paid campaign (Status = READY_FOR_SYNTER), Make generates the deployment package:

```
Deployment Package Contents:
- Creative_Asset: Google_Drive_URL (final approved file)
- Ad_Name: [CC_ID] — [Asset_Name] — [Platform] — [Campaign_Name]
- Brand: SSS / ME
- City: [city]
- Hook_Type: [from Creative_Assets]
- Emotional_Category: [from Creative_Assets]
- Platform: [TikTok / Meta]
- Ad Format: [from Asset Format field]
- Duration: [if video]
- CTA_Type: [from Creative_Assets]
- Budget: [from Paid_Ads record]
- Target Audience: [Will-approved from CREATIVE-TARGETING-001]
- Campaign start date
- Campaign end date (if applicable)
- Budget cap (hard — no autonomous spend beyond this)
```

### 6.3 Deployment Rules

| Rule | Implementation |
|------|----------------|
| No deployment without Will approval | Status = READY_FOR_SYNTER only set by Will manually or via Founder Decision |
| Budget cap is hard | Synter never authorized to exceed approved budget without new Founder Decision |
| Deployment confirmation written to Airtable | Make writes deployed timestamp and Synter campaign ID to Campaign_Creatives record |
| Deployment logged to Audit_Log | Every paid deployment creates an Audit_Log record |
| Sandbox validation required before new platform activation | No new platform deploys without sandbox test and Founder Decision |

### 6.4 Make Scenario: CREATIVE-PAID-002 (Deployment Trigger)

| Property | Value |
|----------|-------|
| Trigger | Campaign_Creatives: Deployment_Status = READY_FOR_SYNTER |
| Action | Package deployment data; send to Synter API (when connected); write Deployed_At to record; update Status = ACTIVE |
| Failure handling | If Synter API fails: alert Will and Luciana; Status reverts to READY_FOR_SYNTER; retry up to 3 times with 15-min backoff |
| Success | Audit_Log record created; Slack notification to Will |

---

## SECTION 7 — STAGE 6: PERFORMANCE TRACKING

### 7.1 Performance Data Sources

| Platform | Data Type | Sync Method | Frequency |
|----------|-----------|-------------|-----------|
| Meta (Facebook/Instagram) | Impressions, reach, engagements, CTR, CPL, ROAS, spend | Meta API → Make | Weekly (Monday 8am) |
| TikTok | Views, completion rate, engagements, CTR, spend | TikTok API → Make | Weekly (Monday 8am) |
| Organic (Instagram/TikTok) | Reach, saves, shares, comments | Manual entry or future API | Weekly |
| Booking attribution | Bookings with Source = content attribution | Airtable Bookings table | Real-time on booking creation |

### 7.2 Make Scenario: CREATIVE-003 (Weekly Performance Sync)

| Property | Value |
|----------|-------|
| Trigger | Weekly, Monday 8am |
| Action | For each ACTIVE Campaign_Creatives record: call Meta API and/or TikTok API; update performance fields |
| Fields updated | Impressions, Reach, Views_3s, Views_Complete, Completion_Rate_Pct, Engagements, Engagement_Rate_Pct, Saves, Shares, Link_Clicks, CTR_Pct, CPM, CPL, Spend, ROAS |
| After data write | Trigger CREATIVE-004 (scoring recalculation) |
| Error handling | If API call fails: mark record `Data_Sync_Failed = true`; alert Luciana; retry next scheduled sync |

### 7.3 Booking Attribution Model

Attribution connects creative deployments to confirmed bookings.

| Attribution Tier | Definition | How Tracked |
|-----------------|------------|-------------|
| Direct (strong) | Client books within 72 hours of ad click or organic post engagement | Bookings.Source = Paid_Ad + Campaign_Creative linked |
| Assisted (moderate) | Client mentions seeing content in intake form or call | Manual entry by Luciana on Booking record |
| Influencer (strong) | Client books using creator's tracking link or mentions creator | Bookings.Affiliate_Source linked to Influencer |
| Dark social (weak) | Client says "I saw it somewhere" — no specific source | Logged as Unattributed_Organic; not credited to specific asset |

### 7.4 Weekly Performance Alert Rules

After each performance sync, Make runs CREATIVE-ALERT-001:

| Condition | Alert |
|-----------|-------|
| Any active paid ad: ROAS < 1.5 | Alert Will: "ROAS below floor — [Campaign_Name] — current ROAS: [value]" |
| Any active paid ad: CPL > $150 | Alert Will: "CPL above threshold — [Campaign_Name] — current CPL: [value]" |
| Any asset: Score_Tier = A+ | Flag for Winning_Creatives review; Founder Decision created |
| Any asset: Fatigue detected | CREATIVE-006 fatigue routine triggered |
| Total week's spend within 20% of monthly budget cap | Alert Will: "Approaching monthly budget cap" |

---

## SECTION 8 — STAGE 7: WINNER ANALYSIS

### 8.1 Winner Identification Process

Winner analysis runs after each weekly performance sync. The process:

```
CREATIVE-004: Scoring recalculation
    → For each Campaign_Creatives record updated this week:
    → Calculate Performance_Score (weighted composite per Creative_Scoring spec)
    → Write Score_Tier
    
CREATIVE-005: Winner eligibility check
    → For each record with Score_Tier = A or A+:
    → Verify: Brand_Compliance_Flag = false
    → Verify: Completion_Rate_Pct ≥ 50% (video) or Engagement_Rate ≥ 5% (static)
    → Verify: Bookings_Attributed ≥ 1 OR ROAS ≥ 3.0
    → If all criteria met: create Founder Decision (Type = WINNING_CREATIVE_REVIEW)
    → Slack DM to Will: "[CA-ID] is eligible for Winning_Creatives — review Founder Decision"
```

### 8.2 Will's Winner Review

Will reviews the Founder Decision with:
- Link to the asset (Google Drive)
- Full performance metrics summary
- Creative DNA classification
- Pattern_Summary (AI-generated)
- Decision: PROMOTE / HOLD / REJECT

If PROMOTE: Will sets `Winning_Creatives.Will_Approved = true`
If HOLD: Asset continues in standard tracking; re-evaluated next cycle
If REJECT: Will notes reason; asset continues normal lifecycle; reason logged to AI_Audit

### 8.3 Pattern Extraction After Promotion

After Will approves a Winning_Creatives record, CREATIVE-008 triggers:

```
Claude receives: all Winning_Creatives from same Brand/Platform/Hook_Type cluster
Claude identifies: shared DNA signals across 3+ winners
Claude generates: draft Creative_DNA record with Source_System = AI_Extracted
Draft routes to Will: Founder Decision (Type = DNA_PATTERN_REVIEW)
Will reviews, edits, approves
DNA pattern becomes ACTIVE
```

---

## SECTION 9 — STAGE 8: NEXT-GENERATION RECOMMENDATIONS

### 9.1 Brief Generation

After Will approves a DNA pattern, the system can generate next-generation creative briefs.

CREATIVE-008 (brief generation):
- Claude reads the approved Creative_DNA record
- Claude generates a full creative brief using the `Brief_Template` structure (CREATIVE_DNA_ENGINE.md Section 4.2)
- Brief routes to Will for review and edit
- Will releases brief to editor or creator
- New Creative_Assets records created from this brief include `Source_DNA_Pattern` field linking to the parent DNA record

### 9.2 Recommendation Report

Monthly (1st of month), CREATIVE-009 generates and sends to Will:

```
CREATIVE INTELLIGENCE MONTHLY REPORT — [Month YYYY]

PERFORMANCE SUMMARY
Total assets deployed: [N]
Winners identified: [N]
Average Performance Score: [value]
Best performing asset: [CA-ID] — Score: [value] — ROAS: [value]

WHAT'S WORKING
Top Hook Type: [type] — avg score [value]
Top Emotional Category: [category] — avg ROAS [value]
Top Platform: [platform] — avg completion rate [value]%
Top Luxury Moment: [moment] — avg save rate [value]%

WHAT'S FATIGUING
[N] assets flagged for fatigue
Most fatigued: [CA-ID] — retired [date]
Fatigue pattern: [AI summary of what's burning out and why]

DNA PATTERNS ACTIVE
[N] active patterns — [N] briefs generated — [N] briefs converted to winners

NEXT MONTH RECOMMENDATIONS
1. [Hook type] on [platform] — pattern is underserved — [N] slots available
2. [Luxury moment] content is converting at [X]x average — brief [N] more
3. [Asset type] fatigue is high — reduce frequency of [type] temporarily

PENDING DECISIONS
[N] assets pending Will approval
[N] DNA patterns pending review
[N] winner eligibilities pending
```

### 9.3 Continuous Loop Completion

Each recommendation feeds back into Stage 1. New briefs create new uploads. New uploads enter AI tagging. The loop accelerates.

**Loop velocity goal:** First loop revolution takes 4–6 weeks (upload to recommendation). By month 6, the loop should run on a 2-week cadence with sufficient data for weekly pattern updates.

---

## SECTION 10 — MAKE SCENARIO CATALOG (COMPLETE LOOP)

| Scenario ID | Stage | Trigger | Action | Tier |
|-------------|-------|---------|--------|------|
| CREATIVE-UPLOAD-001 | Upload | New Google Drive file | Validate naming; create Creative_Assets record | A |
| CREATIVE-001 | AI Tagging | Status = REVIEW_PENDING | Claude AI tagging; write classification fields | A (draft) |
| CREATIVE-DAILY-001 | Airtable Sync | Daily 9am | Compile Will's review queue; Slack summary | A |
| CREATIVE-ORG-001 | Campaign Creation | Organic_Content status = READY_TO_PUBLISH | Notify Luciana; schedule publish reminder | A |
| CREATIVE-CAPTION-001 | Campaign Creation | Organic_Content created | Generate 3 caption variants via Claude | A (draft) |
| CREATIVE-TARGETING-001 | Campaign Creation | Paid_Ads status = TARGETING_REQUIRED | Generate audience targeting recommendation | B |
| CREATIVE-PAID-001 | Deployment | Paid campaign approved | Prepare Synter deployment package | B |
| CREATIVE-PAID-002 | Deployment | Status = READY_FOR_SYNTER | Send to Synter API; write Deployed_At | A |
| CREATIVE-003 | Performance | Weekly Monday 8am | Pull Meta/TikTok API; update Campaign_Creatives | A |
| CREATIVE-004 | Performance | After CREATIVE-003 | Recalculate Creative_Scoring for updated records | A |
| CREATIVE-ALERT-001 | Performance | After CREATIVE-004 | Check alert thresholds; Slack Will if breached | A |
| CREATIVE-005 | Winner Analysis | Score_Tier = A or A+ | Check eligibility criteria; create Founder Decision | B |
| CREATIVE-006 | Performance | Weekly Thursday 9am | Run fatigue detection; create Creative_Fatigue records | A |
| CREATIVE-007 | Performance | Fatigue confirmed | Alert Will; create Founder Decision: CREATIVE_RETIREMENT | B |
| CREATIVE-008 | Recommendations | Winning_Creatives approved | Extract DNA pattern; generate creative brief | B (draft) |
| CREATIVE-009 | Recommendations | Monthly 1st | Generate and send monthly creative report | A |
| CREATIVE-010 | Recommendations | Quarterly | Scan DNA patterns for 60+ day non-use; alert Will | A |

---

## SECTION 11 — GOVERNANCE

The Marketing Learning Loop is the operational execution of the Creative Intelligence system. It is not a fully autonomous system. It is an AI-accelerated intelligence layer governed by human decisions at every material point.

**Loop Authority:**
- Will controls all gates: asset approval, campaign brief approval, budget release, winner promotion, pattern approval
- Luciana manages operational execution: uploads, caption routing, platform scheduling (as delegated by Will)
- Make executes autonomously only at Tier A steps (notifications, data writes, report generation)
- Claude generates drafts only — never publishes, never deploys, never spends

**Loop Integrity:**
- Every autonomous action writes to Audit_Log
- Every draft generation logs to AI_Audit
- Every Founder Decision required for Tier B steps is immutable once Will responds
- Budget caps are hard limits — no autonomous spend escalation under any condition

This specification is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

SHE SAID SAIL · MARKETING LEARNING LOOP SPEC
CONFIDENTIAL · INTERNAL USE ONLY
