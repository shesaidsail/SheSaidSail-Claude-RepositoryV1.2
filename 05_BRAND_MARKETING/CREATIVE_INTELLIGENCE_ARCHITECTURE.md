# CREATIVE_INTELLIGENCE_ARCHITECTURE

**Status:** DRAFT — Pre-Phase 4 Architecture
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail · Mare Executive · All Current and Future Cities
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Brand Authority:** 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED

---

> **Architecture Statement**
>
> This document specifies the complete Airtable schema and AI intelligence design for the Creative Intelligence Core. It governs five new tables: Creative_Assets, Campaign_Creatives, Winning_Creatives, Creative_Fatigue, and Creative_Scoring. It extends the existing Organic Content and Paid Ads tables. No table is to be built in Airtable until this architecture is approved and the Phase 3 migration is confirmed complete. This document does not govern pricing, proposals, or operational workflows.

---

## SECTION 1 — SYSTEM PURPOSE AND SCOPE

### 1.1 What This System Does

The Creative Intelligence system is a pattern recognition and institutional memory engine. It captures every creative asset produced, tracks what works across campaigns, identifies when creatives stop performing, and builds an evolving intelligence layer that makes the next creative generation smarter than the last.

It is not a content scheduler. It is not a social media tool. It is not a volume engine.

It is a precision creative intelligence system for a luxury brand.

### 1.2 What This System Does Not Do

- Publish content to any platform autonomously
- Modify brand voice or tone
- Optimize for vanity metrics (followers, likes, reach in isolation)
- Chase trends that conflict with brand governance
- Create artificial urgency in any creative

### 1.3 AI Authority in Creative Intelligence

**AI May:**
- Tag assets with emotional classification, hook type, energy profile, platform fit
- Score creatives against the Creative DNA framework
- Detect fatigue signals from performance trend data
- Recommend next-generation hooks based on winning patterns
- Flag brand governance violations for founder review
- Generate caption drafts and hook variations for human review

**AI May Not:**
- Approve any creative for publishing
- Override a founder's creative taste calibration
- Write copy without human review on first deploy
- Determine budget allocation for ad campaigns
- Set creative scoring weights without founder approval

**All creative approvals route to Will first. Always.**

---

## SECTION 2 — TABLE ARCHITECTURE OVERVIEW

### 2.1 New Tables to Build

| Table | ID Prefix | Role | Links To |
|-------|-----------|------|----------|
| Creative_Assets | CA | Master library of every raw and final creative asset | Organic_Content, Campaign_Creatives, Winning_Creatives, Influencers, Affiliates |
| Campaign_Creatives | CC | Links assets to campaigns and tracks deployment | Creative_Assets, Paid_Ads, Creative_Scoring |
| Winning_Creatives | WC | Curated hall of fame — confirmed high-performers | Creative_Assets, Campaign_Creatives, Creative_DNA |
| Creative_Fatigue | CF | Tracks performance decay per asset per platform | Creative_Assets, Campaign_Creatives |
| Creative_Scoring | CS | Composite intelligence score per asset per campaign cycle | Creative_Assets, Campaign_Creatives, Creative_DNA |

### 2.2 Existing Tables Extended by This Architecture

| Table | Table ID | Extensions Required |
|-------|----------|---------------------|
| Organic_Content | tbl09BGFacWim5Rk7 | Add 14 creative intelligence fields (Section 4) |
| Paid_Ads | tblVsxlNdP9xHDipE | Add 9 creative attribution fields (Section 4) |
| Copy/Creative_Assets | tblutlUhd804erPev | Confirm field alignment with new Creative_Assets table |

### 2.3 Dependency Map

```
Creative_Assets (master)
    ↓ linked
    Campaign_Creatives ←→ Paid_Ads
    ↓ linked
    Creative_Scoring ←→ Creative_DNA_Engine (lookup)
    ↓ conditional
    Winning_Creatives (promoted when score threshold met)
    ↓ monitored
    Creative_Fatigue (decay tracking)
```

---

## SECTION 3 — CREATIVE_ASSETS TABLE

### 3.1 Purpose

Creative_Assets is the master library of every piece of creative content produced for SSS and ME — raw footage, edited videos, static images, UGC captures, and copy assets. Every downstream creative workflow links back to a Creative_Assets record. Nothing deploys without a record here.

### 3.2 Full Field Specification

#### Universal Fields (required on all tables)

| Field | Type | Rules |
|-------|------|-------|
| UUID | Formula: RECORD_ID() | Immutable. Never edited. |
| Asset_ID | Formula | Format: CA-YYYY-NNNN (e.g., CA-2026-0001) |
| Created_At | Created Time | Auto-set. Never edited. |
| Updated_At | Last Modified Time | Auto-set. |
| Source_System | Single Select | Manual / Make / AI_Tag / UGC_Capture |
| Environment | Single Select | Production / Sandbox / Development |
| Brand | Single Select | SSS / ME |
| City | Single Select | Miami / Fort_Lauderdale / [future cities] |

#### Core Asset Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Asset_Name | Single Line Text | Required. Follows naming convention (Section 2 of CONTENT_LIBRARY_STRUCTURE.md) |
| Asset_Type | Single Select | Hook_Video / Full_Video / Static_Image / UGC_Raw / UGC_Edited / Caption_Copy / Hook_Script / Testimonial / BTS / Moment_Capture |
| Format | Single Select | 9:16_Vertical / 1:1_Square / 16:9_Horizontal / Static_JPG / Static_PNG / Carousel |
| Duration_Seconds | Number | For video assets only. Leave blank for static. |
| File_Size_MB | Number | Auto-populated from Google Drive sync (future) |
| Google_Drive_URL | URL | Required before record status = APPROVED |
| Thumbnail_URL | URL | Auto-generated or manually set |
| Status | Single Select | RAW / IN_EDIT / REVIEW_PENDING / APPROVED / DEPLOYED / RETIRED / ARCHIVED |

#### Creative DNA Fields (AI-Tagged)

| Field | Type | Values |
|-------|------|--------|
| Hook_Type | Single Select | Curiosity / Social_Proof / Transformation / Emotion / Authority / Contrast / Question / Controversy |
| Hook_Text | Long Text | First 3 seconds of script or opening line. AI-extracted or manually entered. |
| Hook_Duration_Seconds | Number | Precise hook window (0–5 seconds) |
| Emotional_Category | Single Select | Joy / Desire / FOMO / Aspiration / Comfort / Belonging / Pride / Surprise |
| Emotional_Arc | Single Select | Steady_Positive / Build_to_Peak / Contrast_Reveal / Sustained_Luxury / Tension_Release |
| Energy_Profile | Single Select | Calm_Elevated / Warm_Social / High_Energy / Intimate / Cinematic_Slow |
| Pacing | Single Select | Slow / Medium / Fast / Variable |
| Music_Style | Single Select | Soft_Ambient / Upbeat_Pop / RnB_Smooth / Latin_Warm / No_Music / VO_Only |
| Platform_Fit | Multiple Select | TikTok / Instagram_Reels / Instagram_Feed / Instagram_Stories |
| CTA_Present | Checkbox | True = contains call to action |
| CTA_Timing_Seconds | Number | When CTA appears in video |
| CTA_Type | Single Select | Book_Now / Learn_More / DM_Us / Visit_Link / None |
| Luxury_Moment_Type | Multiple Select | Champagne_Pour / Proposal_Moment / Caviar_Service / Sunset_Reaction / Group_Joy / Emotional_Reaction / Decadent_Detail |
| Brand_Compliance_Flag | Checkbox | AI-set. True = flagged for human review. |
| Brand_Compliance_Notes | Long Text | AI-generated flag reason. Will reviews. |

#### Attribution Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creator_Type | Single Select | Internal / Influencer / Client_UGC / Crew / Editor |
| Creator_Link | Link to Influencers or Affiliates | Linked record — one record only |
| Editor | Single Line Text | Editor name or contractor ID |
| Shoot_Date | Date | When footage was captured |
| Published_Date | Date | First publish date (any platform) |
| Booking_Source | Link to Bookings | Booking this asset originated from (if applicable) |
| Charter_Grade_At_Capture | Single Select | A / B / C — pulled from Booking record |

#### Performance Snapshot (rolled up from Campaign_Creatives)

| Field | Type | Source |
|-------|------|--------|
| Total_Impressions | Rollup: SUM | From Campaign_Creatives |
| Total_Engagements | Rollup: SUM | From Campaign_Creatives |
| Best_Performance_Score | Rollup: MAX | From Creative_Scoring |
| Campaign_Count | Count | Linked Campaign_Creatives records |
| Winner_Status | Lookup | From Winning_Creatives (if promoted) |
| Fatigue_Status | Lookup | From Creative_Fatigue (if flagged) |

### 3.3 AI Tagging Logic for Creative_Assets

When a new Creative_Assets record is created with status = REVIEW_PENDING:

1. Make triggers scenario CREATIVE-001 (to be built)
2. Make calls Claude API with asset metadata + Google Drive thumbnail URL (or transcript for video)
3. Claude returns: Hook_Type, Emotional_Category, Emotional_Arc, Energy_Profile, Pacing, Music_Style, Platform_Fit, CTA_Present, CTA_Type, Luxury_Moment_Type, Brand_Compliance_Flag, Brand_Compliance_Notes
4. Make writes all AI-tagged fields to the Creative_Assets record
5. If Brand_Compliance_Flag = true: create Founder Decision → Type = BRAND_COMPLIANCE_REVIEW; alert Will via Slack
6. If Brand_Compliance_Flag = false: status advances to APPROVED (pending Will's final review queue)

**AI Confidence Rule:** Claude returns a confidence score (0–100) with every tag batch. If confidence < 70, the record routes to Will for manual review rather than auto-advancing.

---

## SECTION 4 — CAMPAIGN_CREATIVES TABLE

### 4.1 Purpose

Campaign_Creatives is the deployment record — it links a specific Creative_Asset to a specific campaign run (organic post or paid ad), tracks that deployment's performance data, and feeds the scoring and fatigue systems. One asset can have many Campaign_Creative records (one per deployment).

### 4.2 Full Field Specification

#### Universal Fields

| Field | Type | Rules |
|-------|------|-------|
| UUID | Formula | RECORD_ID() |
| CC_ID | Formula | CC-YYYY-NNNN |
| Created_At | Created Time | Auto |
| Updated_At | Last Modified Time | Auto |
| Source_System | Single Select | Manual / Make / Meta_API / TikTok_API |
| Environment | Single Select | Production / Sandbox |
| Brand | Single Select | SSS / ME |
| City | Single Select | Miami / Fort_Lauderdale / [future] |

#### Deployment Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creative_Asset | Link to Creative_Assets | Required. One asset per CC record. |
| Campaign_Name | Single Line Text | Required |
| Campaign_Type | Single Select | Organic / Paid_Meta / Paid_TikTok / Paid_Google / Retargeting / Influencer |
| Platform | Single Select | TikTok / Instagram_Reels / Instagram_Feed / Instagram_Stories / Facebook / Google |
| Ad_Set | Link to Paid_Ads | Linked if this is a paid deployment |
| Deployed_At | DateTime | When this creative went live |
| Retired_At | DateTime | When this creative was pulled |
| Days_Active | Formula | DATETIME_DIFF(Retired_At, Deployed_At, 'days') |
| Deployment_Status | Single Select | ACTIVE / PAUSED / COMPLETED / FORCE_RETIRED |

#### Performance Fields (from platform API or manual entry)

| Field | Type | Source |
|-------|------|--------|
| Impressions | Number | Meta API / TikTok API / Manual |
| Reach | Number | Platform API / Manual |
| Views_3s | Number | Video only — 3-second view count |
| Views_Complete | Number | Video only — complete view count |
| Completion_Rate_Pct | Formula | Views_Complete / Impressions * 100 |
| Engagements | Number | Likes + Comments + Shares + Saves |
| Engagement_Rate_Pct | Formula | Engagements / Reach * 100 |
| Saves | Number | Saves / Bookmarks |
| Shares | Number | Platform shares |
| Comments | Number | Comment count |
| Link_Clicks | Number | CTA click-throughs |
| CTR_Pct | Formula | Link_Clicks / Impressions * 100 |
| CPM | Currency | Cost per 1,000 impressions (paid only) |
| CPL | Currency | Cost per qualified lead (paid only) |
| Spend | Currency | Total spend for this deployment (paid only) |
| Leads_Generated | Number | Confirmed qualified leads attributed |
| Bookings_Attributed | Number | Bookings traced to this creative deployment |
| Revenue_Attributed | Currency | Revenue from Bookings_Attributed |
| ROAS | Formula | Revenue_Attributed / Spend |

#### Scoring Integration

| Field | Type | Source |
|-------|------|--------|
| Performance_Score | Lookup | From Creative_Scoring linked record |
| Score_Tier | Lookup | A / B / C / D from Creative_Scoring |
| Fatigue_Flag | Lookup | From Creative_Fatigue if decay detected |

### 4.3 Make Compatibility for Campaign_Creatives

| Trigger | Scenario | Action |
|---------|----------|--------|
| New paid ad deployed | CREATIVE-002 | Create Campaign_Creatives record; link to Creative_Assets and Paid_Ads |
| Weekly performance sync | CREATIVE-003 | Pull Meta/TikTok API data; update performance fields on all ACTIVE records |
| Performance threshold breach | CREATIVE-004 | If CPL > floor or ROAS < minimum: alert Will; flag for fatigue review |
| Campaign retired | CREATIVE-005 | Set Deployment_Status = COMPLETED; trigger Creative_Scoring calculation |

---

## SECTION 5 — WINNING_CREATIVES TABLE

### 5.1 Purpose

Winning_Creatives is the curated hall of fame. An asset earns promotion here when it crosses a defined performance threshold — confirmed by data AND approved by Will. This table drives next-generation creative briefs. Every new creative brief references Winning_Creatives patterns.

### 5.2 Promotion Criteria

An asset is eligible for Winning_Creatives promotion when ALL of the following are true:

| Criteria | Threshold |
|----------|-----------|
| Performance_Score | ≥ 80 (A-tier) |
| Completion_Rate_Pct (video) | ≥ 50% |
| Engagement_Rate_Pct | ≥ 5% |
| Bookings_Attributed (organic) | ≥ 1 OR ROAS ≥ 3.0 (paid) |
| Brand_Compliance_Flag | False (clean — no brand violations) |
| Will_Approved | True (founder approval mandatory) |

Promotion is never automatic. AI identifies eligibility. Will approves promotion.

### 5.3 Full Field Specification

#### Universal Fields

Standard (UUID, WC_ID [WC-YYYY-NNNN], Created_At, Updated_At, Source_System, Environment, Brand, City)

#### Core Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creative_Asset | Link to Creative_Assets | Required. The promoted asset. |
| Promoted_At | DateTime | Date Will approved promotion |
| Promoted_By | Single Select | Will / System_Eligible (awaiting Will approval) |
| Will_Approved | Checkbox | Must be true for record to be active |
| Promotion_Reason | Long Text | Why this creative earned winner status — AI summary + Will notes |

#### Performance at Time of Promotion

| Field | Type | Source |
|-------|------|--------|
| Performance_Score_At_Promotion | Number | Snapshot from Creative_Scoring |
| Completion_Rate_At_Promotion | Number | From best Campaign_Creatives record |
| ROAS_At_Promotion | Number | Best ROAS from any deployment |
| Bookings_Attributed_Total | Number | Total across all deployments |
| Revenue_Generated | Currency | Total revenue attributed |

#### Pattern Intelligence Fields

| Field | Type | Source |
|-------|------|--------|
| Hook_Type | Lookup | From Creative_Assets |
| Emotional_Category | Lookup | From Creative_Assets |
| Energy_Profile | Lookup | From Creative_Assets |
| Music_Style | Lookup | From Creative_Assets |
| Platform_Primary | Lookup | Platform where it performed best |
| Luxury_Moment_Type | Lookup | From Creative_Assets |
| Pattern_Summary | Long Text | AI-generated: what made this win. Max 200 words. |
| Replicate_Hook | Checkbox | Will flags if this hook should be replicated in next brief |
| Brief_Generated | Checkbox | True = next-gen brief has been generated from this winner |

#### Archive Fields

| Field | Type | Rules |
|-------|------|-------|
| Still_Relevant | Checkbox | Will sets false when trend or brand has evolved past this asset |
| Archived_At | DateTime | When marked no longer relevant |
| Archive_Reason | Long Text | Why archived — seasonal, platform algorithm change, brand evolution |

---

## SECTION 6 — CREATIVE_FATIGUE TABLE

### 6.1 Purpose

Creative_Fatigue tracks performance decay per asset per platform. Every asset has a performance half-life. This table surfaces when an asset should be retired, rotated, or rested before it degrades the brand. Catching fatigue early protects ROAS and prevents audience burnout.

### 6.2 Fatigue Detection Logic

Fatigue is detected when a deployed creative shows:

| Signal | Threshold |
|--------|-----------|
| CPM rising | > 20% increase week-over-week for 2 consecutive weeks |
| CTR falling | > 25% decrease week-over-week for 2 consecutive weeks |
| Engagement Rate falling | > 30% drop from peak |
| Completion Rate falling | > 25% drop from peak |
| Frequency rising (paid) | > 3.5 average frequency per week |

AI runs fatigue checks weekly (CREATIVE-006 scenario) across all ACTIVE Campaign_Creatives records.

### 6.3 Full Field Specification

#### Universal Fields

Standard (UUID, CF_ID [CF-YYYY-NNNN], Created_At, Updated_At, Source_System, Environment, Brand, City)

#### Core Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creative_Asset | Link to Creative_Assets | The fatiguing asset |
| Platform | Single Select | TikTok / Instagram_Reels / Instagram_Feed / Facebook |
| Campaign_Creative | Link to Campaign_Creatives | The specific deployment showing fatigue |
| Fatigue_Status | Single Select | MONITORING / EARLY_FATIGUE / CONFIRMED_FATIGUE / RETIRED / RESTED |
| Detection_Date | Date | When fatigue was first flagged |
| Confirmed_Date | Date | When fatigue crossed confirmation threshold |
| Retirement_Date | Date | When creative was pulled |

#### Decay Metrics

| Field | Type | Source |
|-------|------|--------|
| Peak_Performance_Score | Number | Best score from Creative_Scoring |
| Current_Performance_Score | Number | Most recent score |
| Score_Decay_Pct | Formula | (Peak - Current) / Peak * 100 |
| Peak_CTR | Number | Best CTR recorded |
| Current_CTR | Number | Most recent CTR |
| CTR_Decay_Pct | Formula | Calculated |
| Peak_Completion_Rate | Number | Best completion rate |
| Current_Completion_Rate | Number | Most recent |
| Completion_Decay_Pct | Formula | Calculated |
| Days_Until_Retirement | Formula | Based on decay curve projection |

#### Response Fields

| Field | Type | Values |
|-------|------|--------|
| Action_Taken | Single Select | None / Paused / Budget_Reduced / Retired / Rested_30d / Rested_60d |
| Action_Date | Date | When action was taken |
| Action_By | Single Select | Will / Luciana / Make_Auto |
| Rest_And_Return_Date | Date | If resting — when to re-evaluate |
| Replacement_Asset | Link to Creative_Assets | The next creative deployed to replace this one |
| Lessons_Generated | Checkbox | True = fatigue insight logged to Lessons table |
| Lesson_Record | Link to Lessons | The lesson created from this fatigue event |

---

## SECTION 7 — CREATIVE_SCORING TABLE

### 7.1 Purpose

Creative_Scoring is the intelligence calculation layer. It produces a composite performance score for each creative asset at each point in time. Scores are not permanent — they are recalculated with each platform data sync. The scoring model is calibrated by Will and cannot be changed by AI.

### 7.2 Scoring Formula

Performance_Score = (Composite of weighted signals)

**Default Weights (Will-adjustable via Founder Decision):**

| Signal | Weight | Rationale |
|--------|--------|-----------|
| Completion Rate | 30% | Audience retention = quality signal |
| Engagement Rate | 20% | Social connection signal |
| Bookings Attributed | 25% | Revenue impact = highest weight after retention |
| ROAS (paid) | 15% | Direct business value |
| Save Rate | 10% | Aspiration and intent signal |

**Score Tiers:**

| Score | Tier | Action |
|-------|------|--------|
| 90–100 | A+ | Promote to Winning_Creatives immediately |
| 80–89 | A | Flag for Winning_Creatives review |
| 65–79 | B | Solid performer — continue monitoring |
| 50–64 | C | Underperforming — diagnose hook or platform fit |
| < 50 | D | Pull from rotation — review for lessons |

### 7.3 Full Field Specification

#### Universal Fields

Standard (UUID, CS_ID [CS-YYYY-NNNN], Created_At, Updated_At, Source_System, Environment, Brand, City)

#### Core Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Creative_Asset | Link to Creative_Assets | The scored asset |
| Campaign_Creative | Link to Campaign_Creatives | The specific deployment scored |
| Score_Date | DateTime | When this score was calculated |
| Score_Period | Single Select | Week_1 / Week_2 / Week_3 / Week_4 / Month_1 / Month_2 / Month_3+ |

#### Score Components

| Field | Type | Source |
|-------|------|--------|
| Completion_Rate_Score | Number (0–100) | Normalized completion rate |
| Engagement_Rate_Score | Number (0–100) | Normalized engagement rate |
| Booking_Attribution_Score | Number (0–100) | Bookings_Attributed normalized against campaign baseline |
| ROAS_Score | Number (0–100) | ROAS normalized against brand floor |
| Save_Rate_Score | Number (0–100) | Saves/Reach normalized |
| Performance_Score | Formula | Weighted composite per Section 7.2 |
| Score_Tier | Formula | A+ / A / B / C / D based on threshold |

#### Scoring Context

| Field | Type | Purpose |
|-------|------|---------|
| Benchmark_Brand | Number | Average score for Brand+Platform at time of scoring |
| Benchmark_Platform | Number | Platform-wide benchmark (SSS portfolio) |
| Score_vs_Brand_Avg | Formula | Performance_Score - Benchmark_Brand |
| Score_vs_Platform_Avg | Formula | Performance_Score - Benchmark_Platform |
| Scoring_Notes | Long Text | AI interpretation of score drivers. Max 150 words. |
| Weight_Version | Number | Which scoring weight version was applied (links to Founder Decision) |

---

## SECTION 8 — EXTENSIONS TO EXISTING TABLES

### 8.1 Organic_Content Table — New Fields

Add the following to tbl09BGFacWim5Rk7:

| Field | Type | Purpose |
|-------|------|---------|
| Creative_Asset_Link | Link to Creative_Assets | Bridge to master asset library |
| Hook_Duration_Seconds | Number | Precise hook window |
| Emotional_Arc | Single Select | Steady_Positive / Build_to_Peak / Contrast_Reveal / Sustained_Luxury / Tension_Release |
| Energy_Profile | Single Select | Calm_Elevated / Warm_Social / High_Energy / Intimate / Cinematic_Slow |
| Pacing | Single Select | Slow / Medium / Fast / Variable |
| Music_Style | Single Select | Soft_Ambient / Upbeat_Pop / RnB_Smooth / Latin_Warm / No_Music / VO_Only |
| Completion_Rate_Pct | Number | From platform analytics |
| Save_Rate_Pct | Number | Saves / Reach |
| Luxury_Moment_Type | Multiple Select | Champagne_Pour / Proposal_Moment / Caviar_Service / Sunset_Reaction / Group_Joy / Emotional_Reaction |
| Performance_Score | Number | From Creative_Scoring |
| Winner_Status | Checkbox | True = promoted to Winning_Creatives |
| Fatigue_Flag | Checkbox | True = Creative_Fatigue record active |
| Booking_Attribution | Link to Bookings | Booking(s) attributed to this content |
| Revenue_Attributed | Currency | Total attributed revenue |

### 8.2 Paid_Ads Table — New Fields

Add the following to tblVsxlNdP9xHDipE:

| Field | Type | Purpose |
|-------|------|---------|
| Creative_Asset_Link | Link to Creative_Assets | Bridge to master asset library |
| Campaign_Creative_Link | Link to Campaign_Creatives | Deployment record |
| Creative_Fatigue_Flag | Checkbox | AI-detected fatigue signal |
| Fatigue_Alert_Date | DateTime | When fatigue was first flagged |
| Winner_Promoted | Checkbox | True = creative promoted to Winning_Creatives |
| Hook_Type | Lookup | From Creative_Assets |
| Emotional_Category | Lookup | From Creative_Assets |
| Performance_Score | Lookup | From Creative_Scoring |
| Bookings_Attributed | Number | Confirmed booking attribution |
| Revenue_Attributed | Currency | Revenue from attributed bookings |

---

## SECTION 9 — MAKE SCENARIO CATALOG (CREATIVE INTELLIGENCE)

| Scenario ID | Trigger | Action | Autonomy Tier |
|-------------|---------|--------|---------------|
| CREATIVE-001 | Creative_Assets record status = REVIEW_PENDING | Call Claude API for AI tagging; write classified fields; route compliance flags | A (draft only) |
| CREATIVE-002 | New paid ad deployed in platform | Create Campaign_Creatives record; link to Creative_Assets and Paid_Ads | A |
| CREATIVE-003 | Weekly (Monday 8am) | Pull Meta/TikTok API performance data; update all ACTIVE Campaign_Creatives records | A |
| CREATIVE-004 | Performance sync complete | Run Creative_Scoring calculation for all records updated this week | A |
| CREATIVE-005 | Creative_Scoring: Score_Tier = A or A+ | Flag for Winning_Creatives eligibility; create Founder Decision for Will review | B |
| CREATIVE-006 | Weekly (Thursday 9am) | Run fatigue detection across all ACTIVE deployments; create Creative_Fatigue records if thresholds breached | A |
| CREATIVE-007 | Creative_Fatigue: Fatigue_Status = CONFIRMED | Alert Will and Luciana via Slack; create Founder Decision: CREATIVE_RETIREMENT | B |
| CREATIVE-008 | Winning_Creatives: Will_Approved = true | Generate next-gen creative brief from winner patterns; route to Will for review | B (draft) |
| CREATIVE-009 | Monthly (1st of month) | Generate creative performance report; send to Will | A |

---

## SECTION 10 — AI TAGGING PROMPTS (SPEC)

### 10.1 Asset Classification Prompt Structure

Claude receives the following context for each asset classification call:

```
SYSTEM CONTEXT:
You are the creative intelligence engine for She Said Sail (luxury yacht experiences) 
and Mare Executive (executive hospitality). You classify creative assets with precision. 
You never recommend content that conflicts with the Master Brand Governance. 
The brand is: emotionally elevated, calm confidence, soft luxury. 
The brand is never: loud, hype-driven, nightlife-coded, or influencer-chaotic.

ASSET DATA:
- Asset Name: [CA-YYYY-NNNN]
- Asset Type: [Hook_Video / UGC / Static etc]
- Brand: [SSS / ME]
- Hook Text (first 3 seconds): [text or transcript excerpt]
- Creator Type: [Internal / Influencer / UGC]
- Duration: [seconds]

CLASSIFICATION TASK:
Return JSON with:
{
  "hook_type": "[one of: Curiosity / Social_Proof / Transformation / Emotion / Authority / Contrast / Question]",
  "emotional_category": "[one of: Joy / Desire / FOMO / Aspiration / Comfort / Belonging / Pride / Surprise]",
  "emotional_arc": "[one of: Steady_Positive / Build_to_Peak / Contrast_Reveal / Sustained_Luxury / Tension_Release]",
  "energy_profile": "[one of: Calm_Elevated / Warm_Social / High_Energy / Intimate / Cinematic_Slow]",
  "pacing": "[one of: Slow / Medium / Fast / Variable]",
  "music_style": "[one of: Soft_Ambient / Upbeat_Pop / RnB_Smooth / Latin_Warm / No_Music / VO_Only]",
  "platform_fit": ["TikTok", "Instagram_Reels"],
  "cta_present": true/false,
  "cta_timing_seconds": [number or null],
  "cta_type": "[one of: Book_Now / Learn_More / DM_Us / Visit_Link / None]",
  "luxury_moment_types": ["Champagne_Pour", "Sunset_Reaction"],
  "brand_compliance_flag": true/false,
  "brand_compliance_notes": "[if flagged: exact phrase or signal that violated brand governance]",
  "confidence_score": [0-100],
  "classification_notes": "[one sentence: what drives this asset's emotional impact]"
}

BRAND COMPLIANCE CHECK:
Flag true if asset contains: prohibited words (amazing/awesome/unforgettable/luxury lifestyle/elite/baller/epic), 
hard-close sales patterns, fake scarcity, corporate jargon, nightlife energy, spring break energy, screaming groups, 
chaotic editing, or meme energy that conflicts with soft luxury positioning.
```

### 10.2 Winner Pattern Analysis Prompt Structure

When generating pattern summaries for Winning_Creatives:

```
SYSTEM CONTEXT: [same as above]

WINNER DATA:
- Asset: [CA-ID]
- Hook Type: [classified type]
- Emotional Category: [classified]
- Performance Score: [score]
- Completion Rate: [%]
- ROAS: [value]
- Luxury Moments: [list]

TASK:
In exactly 3 sentences: explain WHY this creative performed. 
What emotional signal drove retention. What visual or audio element reinforced the brand. 
What should be replicated in the next brief.

Do not explain what happened. Explain why it worked.
```

---

## GOVERNANCE

This architecture is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED
- 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

No table in this document is to be built in Airtable until Phase 3 migration is confirmed complete and Will has issued a Founder Decision authorizing Creative Intelligence Phase build.

---

SHE SAID SAIL · CREATIVE INTELLIGENCE ARCHITECTURE
CONFIDENTIAL · INTERNAL USE ONLY
