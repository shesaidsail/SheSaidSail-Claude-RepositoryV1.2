# CREATIVE_DNA_ENGINE

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
> The Creative DNA Engine is the intelligence framework that teaches Claude WHY creatives perform — not just what they contain. It tracks the structural and emotional components of every asset: hooks, pacing, retention curves, CTA timing, emotional arc, music character, energy profile, and platform behavior. Over time, it builds a brand-specific model of creative excellence for She Said Sail and Mare Executive. This document is the schema and logic specification. No Airtable table is built until Phase 3 migration is confirmed complete.

---

## SECTION 1 — PURPOSE AND PHILOSOPHY

### 1.1 The Problem This Solves

Most creative systems track WHAT performed. They do not track WHY.

A video gets 500K views. That's the what. But did it perform because:
- The hook created curiosity in the first 2 seconds?
- The champagne pour at 8 seconds triggered an aspiration response?
- The music matched the pacing of the emotional arc?
- The CTA appeared exactly when emotional investment peaked?
- The energy was calm enough to feel aspirational but warm enough to feel social?

Without knowing why, every next creative is guesswork.

The Creative DNA Engine makes guesswork unnecessary.

### 1.2 What the Engine Produces

Over time, the Creative DNA Engine enables Claude to answer:

- "What hook type drives the highest completion rate for SSS bachelorette content on TikTok?"
- "What energy profile converts best for ME executive content on Instagram?"
- "What pacing pattern correlates with highest save rate on Reels?"
- "Which emotional arc triggers the most booking inquiries within 48 hours?"
- "When does CTA placement matter most — and at what second?"
- "What music style reinforces the SSS brand positioning without feeling like nightlife?"

These are questions that cannot be answered without structured DNA tracking across a library of performers.

### 1.3 Founder Calibration Is Non-Negotiable

The Creative DNA Engine is trained by performance data AND calibrated by Will's taste.

Performance data tells you what audiences responded to. Will's calibration tells you which responses align with the brand.

A video may score 90 on engagement. If Will determines the emotional energy is wrong for the brand, the DNA pattern from that video is marked `Brand_Calibrated = false` and excluded from next-generation briefs.

AI never overrides founder taste calibration. This is not configurable.

---

## SECTION 2 — CREATIVE DNA TABLE

### 2.1 Purpose

Creative_DNA is the pattern library. Each record represents one confirmed creative DNA pattern — a set of structural signals that, in combination, correlates with high performance for a specific brand, platform, and emotional category. Patterns are extracted from Winning_Creatives and manually curated by Will.

### 2.2 Full Field Specification

#### Universal Fields

| Field | Type | Rules |
|-------|------|-------|
| UUID | Formula | RECORD_ID() |
| DNA_ID | Formula | DNA-YYYY-NNNN |
| Created_At | Created Time | Auto |
| Updated_At | Last Modified Time | Auto |
| Source_System | Single Select | Will_Manual / AI_Extracted / Hybrid |
| Environment | Single Select | Production / Sandbox |
| Brand | Single Select | SSS / ME |
| City | Single Select | Miami / Fort_Lauderdale / All |

#### Pattern Identity Fields

| Field | Type | Values / Rules |
|-------|------|----------------|
| Pattern_Name | Single Line Text | Human-readable name. E.g., "Champagne_Curiosity_TikTok_v1" |
| Pattern_Status | Single Select | ACTIVE / TESTING / RETIRED / BRAND_CALIBRATED_FALSE |
| Source_Winners | Link to Winning_Creatives | The Winning_Creatives records this pattern was extracted from |
| Pattern_Confidence | Number (0–100) | How many winners share this pattern. Higher = more reliable. |
| Will_Approved | Checkbox | Founder must approve before pattern drives any brief |
| Brand_Calibrated | Checkbox | True = Will confirms this pattern aligns with brand direction |
| Brand_Calibration_Notes | Long Text | Will's qualitative notes on this pattern |

#### Hook DNA Fields

| Field | Type | Values |
|-------|------|--------|
| Hook_Type | Single Select | Curiosity / Social_Proof / Transformation / Emotion / Authority / Contrast / Question |
| Hook_Duration_Optimal | Number | Optimal hook window in seconds (e.g., 2.5) |
| Hook_Text_Pattern | Long Text | The structural pattern of the hook. E.g., "Open with a single question that implies social risk, then immediately dissolve into luxury resolution." |
| Hook_Strength_Correlation | Single Select | Strong / Moderate / Weak | How strongly this hook type correlates with completion rate |
| Hook_Opening_Visual | Single Select | Action_First / Reaction_First / Product_First / Face_First / Scene_First |
| Hook_Audio_Pattern | Single Select | Music_Lead / VO_Lead / Natural_Sound / Silence_Then_Drop |

#### Pacing and Retention Fields

| Field | Type | Values |
|-------|------|--------|
| Optimal_Pacing | Single Select | Slow / Medium / Fast / Variable |
| Retention_Cliff_Second | Number | When most viewers drop off (identified from platform data) |
| Retention_Lock_Second | Number | When a strong retention lock occurs (e.g., a surprise or peak moment) |
| Edit_Rhythm | Single Select | Consistent_Cuts / Long_Takes / Rhythm_Match / Dynamic |
| Moment_Build_Pattern | Long Text | How the visual/emotional moments sequence. E.g., "Establish atmosphere → introduce tension → resolve with luxury detail → held moment." |

#### Emotional Arc Fields

| Field | Type | Values |
|-------|------|--------|
| Emotional_Arc_Type | Single Select | Steady_Positive / Build_to_Peak / Contrast_Reveal / Sustained_Luxury / Tension_Release |
| Primary_Emotion | Single Select | Joy / Desire / FOMO / Aspiration / Comfort / Belonging / Pride / Surprise |
| Secondary_Emotion | Single Select | Same options |
| Emotional_Peak_Second | Number | When the emotional peak occurs in the video |
| Emotional_Resolution | Single Select | Warm_Closure / Open_Invitation / Aspirational_Hold / Social_Proof_End |
| Emotional_Transition_Count | Number | How many distinct emotional shifts occur |

#### Music and Audio Fields

| Field | Type | Values |
|-------|------|--------|
| Music_Style | Single Select | Soft_Ambient / Upbeat_Pop / RnB_Smooth / Latin_Warm / No_Music / VO_Only |
| Music_Entry_Second | Number | When music enters relative to video start |
| Music_Energy_Match | Single Select | Matches_Visual_Energy / Contrasts_Visual_Energy / Builds_Under_Visual |
| Music_Tempo | Single Select | Slow / Medium_Tempo / Up_Tempo |
| Audio_Mix | Single Select | Music_Dominant / Natural_Sound_Dominant / Equal / VO_Dominant |
| Music_Drop_Present | Checkbox | True = music drop or change used as a creative device |
| Music_Drop_Second | Number | When the drop occurs |

#### Energy Profile Fields

| Field | Type | Values |
|-------|------|--------|
| Energy_Profile | Single Select | Calm_Elevated / Warm_Social / High_Energy / Intimate / Cinematic_Slow |
| Visual_Density | Single Select | Sparse / Moderate / Rich |
| Color_Temperature | Single Select | Warm_Gold / Cool_Blue / Neutral / Sunrise_Pink |
| Lighting_Style | Single Select | Golden_Hour / Natural_Soft / Candlelit / Bright_Natural |
| Movement_Style | Single Select | Handheld_Organic / Stabilized_Smooth / Static_Composed / Mixed |
| Talent_Energy | Single Select | Candid_Natural / Directed_Soft / Candid_High / Performance_Energy |

#### CTA Architecture Fields

| Field | Type | Values |
|-------|------|--------|
| CTA_Present | Checkbox | |
| CTA_Type | Single Select | Book_Now / Learn_More / DM_Us / Visit_Link / None |
| CTA_Optimal_Timing | Number | Optimal second for CTA based on pattern performance |
| CTA_Entry_Style | Single Select | Text_Overlay / VO_Verbal / Both / None |
| CTA_Placement_Principle | Long Text | Why this timing works. E.g., "CTA at 80% completion captures viewers after emotional investment has peaked." |
| CTA_Urgency_Level | Single Select | None / Soft / Moderate — never Hard (brand governance) |

#### Platform Fit Fields

| Field | Type | Values |
|-------|------|--------|
| Platform_Primary | Single Select | TikTok / Instagram_Reels / Instagram_Feed / Instagram_Stories |
| Platform_Secondary | Single Select | Same options |
| Optimal_Duration | Number | Optimal video length in seconds for this pattern on primary platform |
| Caption_Style | Single Select | Long_Story / Short_Hook / Question_Open / No_Caption_Needed |
| Hashtag_Strategy | Single Select | Minimal_3_5 / Moderate_6_10 / None |
| Sound_On_Required | Checkbox | True = this pattern requires audio to perform (not silent-scroll friendly) |

#### Pattern Intelligence Fields

| Field | Type | Source |
|-------|------|--------|
| Winner_Count | Count | Linked Winning_Creatives |
| Avg_Performance_Score | Rollup: AVG | From Winning_Creatives → Creative_Scoring |
| Avg_Completion_Rate | Rollup: AVG | From Winning_Creatives |
| Avg_ROAS | Rollup: AVG | From Winning_Creatives |
| Pattern_Summary | Long Text | AI-generated: the narrative of why this pattern works. Max 250 words. |
| Brief_Template | Long Text | The creative brief template derived from this pattern (Section 4) |
| Times_Briefed | Number | How many times this pattern has driven a brief |
| Brief_Success_Rate | Formula | Winning_Creatives linked that came from briefs using this pattern / Times_Briefed |

---

## SECTION 3 — DNA SIGNAL TRACKING FRAMEWORK

### 3.1 The Seven Signal Dimensions

Every creative asset is analyzed across seven DNA dimensions. Together, these dimensions explain why it performed.

**Dimension 1 — Hook Architecture**

The hook is the first 2–5 seconds. It is the only thing that determines whether a viewer stays.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Hook type | Curiosity / Social_Proof / Transformation / Emotion | Different hook types drive different viewer behaviors |
| Hook opening visual | What appears first on screen | First frame drives initial stop rate |
| Hook audio pattern | Music lead vs. VO vs. natural sound | Audio hook determines whether sound-on viewers engage |
| Hook duration | Precise seconds before first cut | Too long = drop-off; too short = no emotional setup |
| Hook text structure | First line of script or overlay | Text hooks compete with visual hooks — calibrate |

**Dimension 2 — Pacing and Retention**

Pacing is the rhythm of editing. Retention is whether viewers stay.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Edit rhythm | Cut frequency and consistency | Fast cuts kill luxury feel; slow cuts kill engagement |
| Retention cliff | Second viewers start leaving | Identifies where the creative loses them |
| Retention lock | Second where retention stabilizes or rises | Identifies the creative device that keeps viewers |
| Moment sequence | Order and timing of key visual moments | Sequencing determines emotional buildup |

**Dimension 3 — Emotional Arc**

Emotion is the product. The arc is the story of how emotion builds and resolves.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Primary emotion | The dominant feeling throughout | Emotion drives save rate and sharing behavior |
| Secondary emotion | The supporting emotional undercurrent | Dual-emotion creatives tend to perform better in SSS content |
| Emotional peak timing | When in the video the peak hits | Peak at 60–80% = strong save and completion correlation |
| Emotional resolution | How the video ends emotionally | Open invitation end = strongest DM and booking conversion |
| Emotional transitions | How many shifts occur | 2–3 shifts = optimal for SSS; ME content prefers 1–2 |

**Dimension 4 — Music and Audio**

Music is not decoration. Music is architecture.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Music style | Genre and tempo character | Wrong music style breaks brand positioning immediately |
| Music entry point | When music enters relative to video | Late music entry = stronger visual hook impact |
| Audio mix balance | Music vs. natural sound vs. VO | SSS winning pattern: natural sound-lead with music building |
| Music drop | Whether a drop or change is used | Strategic drops correlate with retention locks in SSS data |
| Music energy match | Whether music energy matches or contrasts visual | Contrast can be powerful when used deliberately |

**Dimension 5 — Energy Profile**

Energy profile is the felt quality of the creative — not its content, but its texture.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Overall energy | Calm_Elevated vs. High_Energy etc. | SSS brand requires Calm_Elevated or Warm_Social — never chaotic |
| Visual density | How much is happening on screen | Sparse feels premium; dense feels chaotic for luxury positioning |
| Color temperature | Warm vs. cool vs. neutral palette | Golden warm tones correlate with higher save rates in SSS content |
| Lighting character | Golden hour vs. candlelit vs. bright | Golden hour is the SSS signature lighting signal |
| Talent behavior | How people on screen behave | Candid natural behavior outperforms directed performance for SSS |

**Dimension 6 — CTA Architecture**

When and how a call-to-action appears determines whether emotional investment converts to action.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| CTA timing | At what second the CTA appears | Too early = no emotional investment; too late = viewer gone |
| CTA entry method | Text overlay vs. verbal vs. both | VO-verbal CTA feels more personal for luxury positioning |
| CTA urgency level | Hard vs. soft vs. none | Hard CTA violates brand governance; soft performs better for SSS |
| CTA placement principle | Why this timing works for this emotional arc | Context-aware CTA dramatically outperforms template placement |

**Dimension 7 — Platform Fit**

A creative that wins on TikTok may fail on Instagram. Platform fit is a distinct DNA dimension.

| Signal | What We Track | Why It Matters |
|--------|---------------|----------------|
| Primary platform | Where this format is optimized | Aspect ratio, duration, caption style differ by platform |
| Optimal duration | Best performing length for platform | TikTok sweet spots ≠ Reels sweet spots |
| Sound dependency | Whether the creative requires audio | Instagram Stories often watched silent — critical for format decisions |
| Caption approach | Long story vs. short hook vs. none | Platform algorithm and audience behavior drive caption strategy |

---

## SECTION 4 — CREATIVE BRIEF TEMPLATE GENERATION

### 4.1 How DNA Patterns Drive Briefs

When a DNA pattern earns `Will_Approved = true` and `Brief_Template` is ready, Make can generate a creative brief from that pattern on demand.

The brief is not instructions for what to create. The brief is a structural framework for WHY and HOW to create — the DNA recreated intentionally.

### 4.2 Creative Brief Template Structure

Generated by Claude from the `Brief_Template` field in Creative_DNA:

```
CREATIVE BRIEF — [DNA_ID] — [Pattern_Name]
Generated: [Date]
Brand: [SSS / ME]
Platform: [Platform_Primary]

---

THE GOAL
What emotional experience should the viewer have by the end.
[AI-generated from Emotional_Arc_Type + Primary_Emotion + Emotional_Resolution]

---

THE HOOK (first [Hook_Duration_Optimal] seconds)
Type: [Hook_Type]
Opening visual: [Hook_Opening_Visual]
Audio: [Hook_Audio_Pattern]
Script pattern: [Hook_Text_Pattern]

---

THE PACING
Edit rhythm: [Edit_Rhythm]
Key retention moment: approximately [Retention_Lock_Second] seconds — this is where you must deliver a peak moment.
Moment sequence: [Moment_Build_Pattern]

---

THE EMOTIONAL ARC
Primary emotion: [Primary_Emotion]
Secondary emotion: [Secondary_Emotion]
Emotional peak: approximately [Emotional_Peak_Second] seconds into the video
Resolution style: [Emotional_Resolution]

---

THE ENERGY
Profile: [Energy_Profile]
Lighting: [Lighting_Style]
Talent behavior: [Talent_Energy]
Visual density: [Visual_Density]
Color temperature: [Color_Temperature]

---

THE MUSIC
Style: [Music_Style]
Entry: music enters approximately [Music_Entry_Second] seconds in
Mix: [Audio_Mix]
[If Music_Drop_Present]: Use a music drop or transition at approximately [Music_Drop_Second] seconds

---

THE CTA
Type: [CTA_Type]
Placement: approximately [CTA_Optimal_Timing] seconds
Style: [CTA_Entry_Style]
[CTA_Placement_Principle]

---

LUXURY MOMENT TARGETS
[Luxury_Moment_Types from Source_Winners — the specific moments to capture]

---

BRAND COMPLIANCE CHECKPOINTS
Before submission, confirm:
☐ No prohibited words in any text overlay or VO
☐ Energy profile = [Energy_Profile] — not louder
☐ No hard-close sales patterns
☐ Music style is brand-aligned
☐ Lighting is warm and natural — not nightclub
☐ Talent behavior is candid, not performative

---

REFERENCE WINNERS
[Linked Winning_Creatives — these are the assets that established this pattern]
```

### 4.3 Brief Approval Flow

1. Make generates brief from DNA pattern (CREATIVE-008)
2. Brief routes to Will for review
3. Will edits, approves, and releases to editor or creator
4. Brief_Generated = true on the source DNA record
5. New Creative_Assets records created from this brief are tagged with `Source_DNA_Pattern = [DNA_ID]`
6. When brief-sourced assets are scored, performance data feeds back to the source DNA record to calibrate `Brief_Success_Rate`

---

## SECTION 5 — PATTERN LEARNING RULES

### 5.1 How Patterns Are Created

DNA patterns are NOT created automatically. Creation requires:

1. AI identifies 3+ Winning_Creatives that share ≥ 5 of the 7 DNA dimensions
2. AI generates a draft DNA record with `Source_System = AI_Extracted`
3. Draft routes to Will via Founder Decision: DNA_PATTERN_REVIEW
4. Will reviews, edits, adds `Brand_Calibration_Notes`
5. Will sets `Will_Approved = true` and `Brand_Calibrated = true`
6. Pattern becomes active and available for brief generation

### 5.2 Pattern Deprecation Rules

A pattern is retired when:

| Condition | Action |
|-----------|--------|
| No winning creatives sourced from this pattern in 90 days | MONITORING status |
| Platform algorithm change confirmed to affect this format | Will reviews for retirement |
| Brand evolution makes pattern off-brand | Will sets Brand_Calibrated = false; Pattern_Status = BRAND_CALIBRATED_FALSE |
| Less than 50% brief success rate over 10+ briefs | Pattern_Status = TESTING for recalibration |
| Will manually retires | Pattern_Status = RETIRED |

Retired patterns are never deleted. They are institutional memory.

### 5.3 Seasonal Pattern Tracking

Some patterns are seasonal. Bachelorette content patterns in summer differ from winter. The `City` and brief generation date fields allow seasonal filtering.

Make scheduled scan (CREATIVE-010): quarterly, identify which DNA patterns have not been used in 60+ days — alert Will for pattern refresh review.

---

## SECTION 6 — AIRTABLE SCHEMA SUMMARY

**New Table Required:**

| Table | ID Prefix | Key Links |
|-------|-----------|-----------|
| Creative_DNA | DNA | Winning_Creatives (many), Creative_Assets (many) |

**Existing Table Extensions Required:**

| Table | New Fields |
|-------|------------|
| Creative_Assets | Source_DNA_Pattern (link to Creative_DNA) |
| Winning_Creatives | Source_DNA_Patterns (link to Creative_DNA, rollup) |

---

## SECTION 7 — GOVERNANCE

The Creative DNA Engine is the most intellectually sensitive system in the creative intelligence stack. It encodes Will's taste, brand philosophy, and competitive intelligence. Access is restricted.

**Read access:** Will, Luciana (read-only on approved patterns)
**Write access:** Will only (via Founder Decision for new patterns)
**AI access:** Read-only for brief generation context injection
**Make access:** Read for brief generation; write only to update `Times_Briefed` and `Brief_Success_Rate`

This architecture is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED

Founder taste calibration overrides all AI behavior. This is stated in Master Brand Governance and reinforced here.

---

SHE SAID SAIL · CREATIVE DNA ENGINE
CONFIDENTIAL · INTERNAL USE ONLY
