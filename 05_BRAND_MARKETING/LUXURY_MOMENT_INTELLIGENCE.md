# LUXURY_MOMENT_INTELLIGENCE

**Status:** DRAFT — Pre-Phase 4 Architecture
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail · Mare Executive
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Brand Authority:** 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED

---

> **Architecture Statement**
>
> This document specifies the Luxury Moment Intelligence system — the framework for identifying, classifying, tracking, and learning from the specific emotional peak moments that define the She Said Sail and Mare Executive experience. These are the moments that make content go viral, that make clients come back, and that make the brand unforgettable. The system treats these moments as structured intelligence, not just content. This enables the brand to deliberately create, capture, and compound these moments over time.

---

## SECTION 1 — PHILOSOPHY

### 1.1 The Moment Is the Brand

From Master Brand Governance:

> The yacht is not the product.
> The feeling is the product.

The brand sells emotional relief, social confidence, group cohesion, memory creation, and emotional atmosphere.

The Luxury Moment Intelligence system operationalizes this. It identifies the precise emotional peak moments that, when captured on camera and deployed correctly, make audiences stop scrolling, save content, and send it to their group chat.

These moments are not manufactured. They are designed for and captured when they happen naturally. The system learns which moments resonate most — and builds operational protocols to ensure those moments happen on every charter.

### 1.2 Moment Intelligence Is Bidirectional

Moment intelligence flows in two directions:

**Backward (from content to operations):**
Content that features a champagne pour drives the most saves. → Champagne pours should be a planned moment on every charter. → Crew brief should include champagne pour staging guidance. → Boat provisioning always includes champagne presentation materials.

**Forward (from operations to content):**
New charter type involves a caviar service. → Crew is briefed to capture the reaction. → Captured content enters the creative library as a Luxury Moment asset. → Performance data reveals how this moment performs. → Brief more assets featuring caviar service reactions.

This bidirectional loop is what makes the brand compounding.

---

## SECTION 2 — LUXURY MOMENT TAXONOMY

### 2.1 Moment Categories

All luxury moments are classified into the following taxonomy. This taxonomy is fixed — new categories require a Founder Decision.

| Moment Category | Definition | Brand Signal |
|-----------------|------------|--------------|
| **Champagne_Pour** | The moment of champagne pouring — into glasses, in slow motion, with spray, or ceremonially | Celebration, luxury entry point, social ritual |
| **Proposal_Moment** | An engagement or marriage proposal occurring on charter | Highest emotional intensity moment in SSS catalog |
| **Caviar_Service** | Caviar presentation, plating, or tasting moment | Elevated hospitality, discernment, quiet luxury |
| **Sunset_Reaction** | Authentic emotional reaction to sunset from the water | Natural luxury, contemplative, aspirational |
| **Group_Joy** | Spontaneous group laughter, dancing, celebration energy | Social connection, belonging, effortless fun |
| **Emotional_Reaction** | Any singular emotional reaction face — wonder, delight, relief, joy | Authentic emotion, human luxury signal |
| **Decadent_Detail** | Close-up of a luxury hospitality detail (tablescaping, garnish, floral, glassware) | Taste, attention, elevated hosting |
| **First_Glimpse** | Guests seeing the yacht or the view for the first time — reaction shot | Anticipation payoff, social proof |
| **Intimate_Moment** | A quiet, private moment between people — not performative | Emotional safety, depth, luxury as sanctuary |
| **Crew_Excellence** | A crew member delivering an exceptional hospitality moment — a look, a pour, a gesture | Service standard, brand differentiator |
| **Water_Moment** | Swimming, jumping, relaxing in the water — freedom and release | Escape, luxury as liberation |
| **ME_Executive_Moment** | A power moment specific to Mare Executive — handshake, toast, relationship capital | Executive positioning, controlled confidence |

### 2.2 Moment Intensity Levels

| Level | Definition | Content Priority |
|-------|------------|------------------|
| 1 — Peak | Once-in-a-lifetime moment (proposal, emotional breakthrough, viral reaction) | Highest priority — always capture if present |
| 2 — High | Strong emotional moment (first glimpse, champagne spray, sunset peak) | High priority — plan for and capture |
| 3 — Steady | Consistent luxury moments (champagne pour, caviar service, crew excellence) | Standard — part of every charter shoot list |
| 4 — Background | Ambient luxury details (decadent detail, water ambiance, drone establishing) | Fill material — capture when available |

---

## SECTION 3 — LUXURY_MOMENT_INTELLIGENCE TABLE

### 3.1 Purpose

Luxury_Moment_Intelligence (LMI) is the intelligence record for moment performance. Each record represents one moment category on one platform and accumulates performance data from all content assets that feature that moment type. Over time, this reveals which moments resonate most with audiences — and which moments convert to bookings.

### 3.2 Full Field Specification

#### Universal Fields

| Field | Type | Rules |
|-------|------|-------|
| UUID | Formula | RECORD_ID() |
| LMI_ID | Formula | LMI-YYYY-NNNN |
| Created_At | Created Time | Auto |
| Updated_At | Last Modified Time | Auto |
| Source_System | Single Select | Make / Manual |
| Environment | Single Select | Production / Sandbox |
| Brand | Single Select | SSS / ME |
| City | Single Select | Miami / Fort_Lauderdale / All |

#### Moment Identity Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Moment_Category | Single Select | All categories from Section 2.1 taxonomy |
| Moment_Intensity | Single Select | Peak / High / Steady / Background |
| Platform | Single Select | TikTok / Instagram_Reels / Instagram_Feed / Both |
| Tracking_Period | Single Select | Monthly / Quarterly / Annual |
| Period_Start | Date | |
| Period_End | Date | |

#### Asset Links

| Field | Type | Source |
|-------|------|--------|
| Linked_Assets | Link to Creative_Assets | All assets featuring this moment type |
| Asset_Count | Count | Linked assets |
| Deployed_Asset_Count | Count | Assets with status = DEPLOYED |
| Winner_Asset_Count | Count | Assets promoted to Winning_Creatives |

#### Performance Intelligence

| Field | Type | Formula / Source |
|-------|------|-----------------|
| Avg_Performance_Score | Rollup: AVG | Creative_Scoring scores for linked assets |
| Avg_Completion_Rate | Rollup: AVG | Campaign_Creatives.Completion_Rate_Pct |
| Avg_Save_Rate | Rollup: AVG | Campaign_Creatives.Save_Rate |
| Avg_Engagement_Rate | Rollup: AVG | Campaign_Creatives.Engagement_Rate_Pct |
| Avg_ROAS | Rollup: AVG | Campaign_Creatives.ROAS (paid only) |
| Total_Revenue_Attributed | Rollup: SUM | Campaign_Creatives.Revenue_Attributed |
| Total_Bookings_Attributed | Rollup: SUM | Campaign_Creatives.Bookings_Attributed |
| Viral_Events | Count | Creative_Assets with Viral_Flag = true featuring this moment |
| Moment_ROAS | Formula | Total_Revenue_Attributed / Total_Spend_For_Moment_Assets |
| Booking_Conversion_Rate | Formula | Total_Bookings_Attributed / Total_Impressions_For_Moment |

#### Operational Intelligence Fields

| Field | Type | Purpose |
|-------|------|---------|
| Capture_Rate | Number | % of charters that had this moment captured (manually tracked) |
| Capture_Difficulty | Single Select | Easy / Moderate / Difficult / Requires_Planning |
| Capture_Protocol | Long Text | How crew should plan for and capture this moment |
| Provisioning_Required | Checkbox | True = specific provisioning needed to enable this moment |
| Provisioning_Notes | Long Text | What to include in charter provisioning to enable this moment |
| Charter_Types | Multiple Select | Bachelorette / Birthday / Girls_Trip / ME_Executive / Corporate / Celebration |
| Seasonal_Relevance | Multiple Select | Year_Round / Summer / Winter / Sunset_Season / Holiday |

#### Trend and Will Intelligence Fields

| Field | Type | Values |
|-------|------|--------|
| Trend_Direction | Single Select | Rising / Stable / Declining |
| Will_Priority | Single Select | Focus / Standard / Deprioritize |
| Will_Notes | Long Text | Founder's qualitative read on this moment |
| Next_Quarter_Brief_Target | Number | How many assets featuring this moment to brief next quarter |

---

## SECTION 4 — MOMENT TRACKING IN CREATIVE_ASSETS

### 4.1 Luxury Moment Fields in Creative_Assets

Each Creative_Assets record tracks which luxury moments appear in that asset:

| Field | Type | Values |
|-------|------|--------|
| Luxury_Moment_Types | Multiple Select | All taxonomy categories from Section 2.1 |
| Primary_Luxury_Moment | Single Select | The dominant moment (for filtering and sorting) |
| Moment_Intensity_Level | Single Select | Peak / High / Steady / Background |
| Moment_Timestamp_Seconds | Number | When the primary luxury moment occurs in the video |
| Moment_Duration_Seconds | Number | How long the moment lasts on screen |
| Moment_Quality | Single Select | A (stunning, authentic) / B (good, usable) / C (weak, forced) — Will-set |

### 4.2 AI Moment Detection

During CREATIVE-001 (AI tagging), Claude detects luxury moments present in the asset:

From the classification prompt (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 10.1):
```json
"luxury_moment_types": ["Champagne_Pour", "Sunset_Reaction"],
```

Claude identifies all moment types visible from:
- Hook text or script (if provided)
- File description tags
- Asset type classification

Where video content is available via transcript or description, Claude also estimates:
- Primary luxury moment (dominant one)
- Approximate timestamp of moment occurrence
- Moment quality assessment (based on description quality and context)

Human validation required for all moment quality scores (A/B/C). AI assigns draft — Will confirms.

---

## SECTION 5 — MOMENT PERFORMANCE ANALYTICS

### 5.1 Moment Performance Report (Monthly, Component of CREATIVE-009)

```
LUXURY MOMENT PERFORMANCE — [Month YYYY] — [Brand] — [Platform]

MOMENT CATEGORY RANKINGS (by Avg Performance Score):

1. Sunset_Reaction — Score: [X] | Saves: [%] | Bookings: [N] | ROAS: [X]
2. Champagne_Pour — Score: [X] | Saves: [%] | Bookings: [N] | ROAS: [X]
3. Group_Joy — Score: [X] | Saves: [%] | Bookings: [N] | ROAS: [X]
4. Proposal_Moment — Score: [X] | Saves: [%] | Bookings: [N] | ROAS: [X]
[...]

RISING MOMENTS (Trend_Direction = Rising):
- [Moment]: up [X]% vs. last month

DECLINING MOMENTS:
- [Moment]: down [X]% vs. last month

CAPTURE RATE THIS MONTH:
- Champagne_Pour: [N] of [N] charters captured ([%])
- Sunset_Reaction: [N] of [N] charters captured ([%])
[...]

VIRAL EVENTS THIS MONTH:
[Any assets with Viral_Flag = true — moment type, asset ID, reach]

OPERATIONAL RECOMMENDATIONS:
- [Moment] is underperforming capture rate — recommend crew brief update
- [Moment] has high conversion — recommend brief [N] more assets this type
- [Moment] is declining on TikTok — investigate platform algorithm change
```

### 5.2 Seasonal Moment Analysis

Quarterly (CREATIVE-010 variant): Claude analyzes performance by month to identify seasonal moment patterns:

- Which moments peak in December (holiday season)?
- Which moments peak in June (bachelorette season)?
- Which moments are consistent year-round?

Seasonal intelligence feeds the content calendar planning for each quarter.

---

## SECTION 6 — OPERATIONAL MOMENT PROTOCOLS

### 6.1 Crew Capture Briefs

The moment intelligence system feeds back into charter operations. When a moment category is identified as high-performing, a Crew Capture Brief is generated.

**Crew Capture Brief Structure:**

```
CREW CAPTURE BRIEF — [Moment_Category] — [Charter_Type] — [City]

MOMENT: [Moment_Category]
PRIORITY LEVEL: [Intensity Level]
WHY THIS MATTERS: [Performance data summary — e.g., "Sunset reaction content averages 4.2x save rate vs. other SSS content"]

WHEN TO CAPTURE:
[Specific timing and conditions — e.g., "During golden hour, 30 minutes before official sunset. Guest must be facing water."]

HOW TO CAPTURE:
[Framing, proximity, camera movement guidance — approved for crew distribution]
Camera position: [description]
Framing: [close-up / wide / over shoulder]
Movement: [static / slow push / follow]
Duration: [hold for X seconds]

WHAT TO AVOID:
[Brand compliance reminders — e.g., "Do not capture if group is loud or chaotic. Moment must feel calm and natural."]

PROVISIONING REQUIRED:
[If applicable — e.g., "Champagne must be chilled and staged at bow 15 minutes before pour moment."]

REFERENCE ASSETS:
[CA-IDs of Winning_Creatives that exemplify this moment — crew can review these before charter]
```

### 6.2 Provisioning Integration

When `Provisioning_Required = true` on a Luxury_Moment_Intelligence record, provisioning notes are added to the Charter Brief template for that charter type.

Make scenario CREATIVE-CHARTER-001 (future): When a Booking is confirmed with a charter type that includes specific luxury moment targets, the Charter Brief automation includes moment-specific provisioning flags.

Example:
- Bachelorette charter confirmed → Charter Brief includes: "Champagne staging at bow — provision 2 bottles minimum; note best sunset window for this vessel and location"
- ME Executive charter confirmed → Charter Brief includes: "Executive toast moment — provision premium spirits; ensure table is set before boarding"

---

## SECTION 7 — VIRAL MOMENT TRACKING

### 7.1 Viral Classification

A creative asset is classified as viral when it significantly exceeds normal reach benchmarks for the brand.

**Viral Threshold (SSS portfolio baseline):**

| Platform | Viral Threshold |
|----------|----------------|
| TikTok | > 100,000 views on a single post |
| Instagram Reels | > 50,000 views on a single post |
| Instagram Feed | > 10,000 engagements on a single post |

When any Campaign_Creatives record crosses these thresholds, Make automatically sets `Organic_Content.Viral_Flag = true` (or `Creative_Assets.Viral_Flag = true` for the source asset).

### 7.2 Viral Event Record

When a viral event is detected, Make creates a Lessons table record:

| Field | Value |
|-------|-------|
| Lesson_Type | Viral_Creative_Event |
| Source_Table | Creative_Assets |
| Source_Record | [CA-ID] |
| Lesson_Text | "[Asset name] went viral on [platform] — [views/engagements]. Primary luxury moment: [moment type]. Hook type: [hook]. Emotional category: [emotion]. Performance at viral peak: [score]." |
| Action_Required | Review moment capture conditions; brief similar content; update DNA pattern |
| Will_Reviewed | Pending |

### 7.3 Viral Pattern Intelligence

Each viral event is tagged with its luxury moment type, hook type, and emotional category. After 5+ viral events, Claude identifies if a viral pattern exists — specific moment + hook + platform combinations that consistently break through.

Viral patterns are elevated to Creative_DNA patterns with `Pattern_Name` including "Viral_" prefix and highest priority in brief generation.

---

## SECTION 8 — PROPOSAL MOMENT PROTOCOL

### 8.1 Special Handling for Proposal Moments

Proposal moments are the highest emotional intensity moment in the SSS catalog. They require special handling because:

1. They are genuinely private moments that must not be exploited
2. They require explicit consent from both parties for any content use
3. They represent the brand's deepest promise: holding the most important moments

### 8.2 Proposal Capture Protocol

When a proposal is planned (indicated in Booking.Special_Notes by Luciana or client):

1. Luciana briefs crew privately — not in group charter communication
2. Crew prepares capture position before the moment
3. No phones from group — crew captures only
4. Post-proposal: couple asked privately if they consent to content use
5. If consent: content enters Creative_Assets as UGC_Edited with Creator_Type = Client_UGC; consent noted in file description
6. If no consent: footage deleted from all devices; no record of specific footage created

### 8.3 Consent Documentation

For any Proposal_Moment content used:

| Field (Creative_Assets) | Value |
|------------------------|-------|
| Creator_Type | Client_UGC |
| Content_Consent_Status | Single Select field: VERBAL_CONSENT / WRITTEN_CONSENT / NO_CONSENT / PENDING |
| Consent_Date | Date |
| Consent_Notes | "Couple [first names] verbally consented post-proposal to use in SSS content. Booking [BK-ID] reference." |

No proposal content deploys without `Content_Consent_Status = WRITTEN_CONSENT`. Verbal consent is for internal logging only — not for public deployment.

---

## SECTION 9 — AIRTABLE SCHEMA SUMMARY

**New Table Required:**

| Table | ID Prefix | Key Links |
|-------|-----------|-----------|
| Luxury_Moment_Intelligence | LMI | Creative_Assets (many) |

**New Fields in Existing Tables:**

| Table | New Fields |
|-------|------------|
| Creative_Assets | Luxury_Moment_Types, Primary_Luxury_Moment, Moment_Intensity_Level, Moment_Timestamp_Seconds, Moment_Duration_Seconds, Moment_Quality, Viral_Flag, Content_Consent_Status, Consent_Date, Consent_Notes |
| Organic_Content | Viral_Flag (add if not already present) |

---

## SECTION 10 — GOVERNANCE

Luxury Moment Intelligence touches the most emotionally sensitive moments in the SSS and ME client experience. Content involving peak moments (proposals, emotional reactions, intimate moments) requires the highest care.

**Content Ethics Rules:**
- No moment content used publicly without confirmed consent
- No moment content staged or manufactured to appear authentic
- No moment content that exploits group vulnerability
- No viral moment leveraged in a way that embarrasses the client
- All client UGC used only within the terms of consent given

**Data Access:**
- Will: full access
- Luciana: read access to capture protocols and moment performance
- Crew: access to Crew Capture Briefs only (distributed per charter)
- AI: read access for classification and reporting; no write access to consent fields

This document is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED

**Founder taste calibration governs all moment quality decisions. AI classifies. Will curates.**

---

SHE SAID SAIL · LUXURY MOMENT INTELLIGENCE
CONFIDENTIAL · INTERNAL USE ONLY
