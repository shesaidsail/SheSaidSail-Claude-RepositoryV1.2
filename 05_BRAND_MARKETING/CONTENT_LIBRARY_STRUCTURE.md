# CONTENT_LIBRARY_STRUCTURE

**Status:** DRAFT — Pre-Phase 4 Architecture
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail · Mare Executive · All Current and Future Cities
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Architecture Statement**
>
> This document defines the final Google Drive content library architecture for She Said Sail and Mare Executive. It governs folder structure, file naming conventions, tagging conventions, retrieval architecture, archive procedures, and multi-brand / multi-city scalability standards. No Google Drive restructuring begins until Will approves this architecture and the Google Drive / S3 system activation is authorized per Section 1.4 of Systems_Intelligence_Architecture_v2.0_PRODUCTION.

---

## SECTION 1 — DESIGN PRINCIPLES

### 1.1 Core Principles

**Structure serves retrieval.** Every folder and naming decision is optimized for human findability in under 10 seconds and AI queryability without ambiguity.

**Brand isolation is mandatory.** SSS and ME content never co-mingle in the same folder. Brand contamination at the storage layer is a structural failure.

**City is always explicit.** Every asset path includes its city of origin. This enables multi-city performance comparison and multi-city scaling without restructuring.

**Naming encodes intelligence.** File names carry enough metadata that the file can be found, classified, and acted on without opening it.

**Archive is structured, not deleted.** Retired content moves to archive, never to trash. Institutional memory is preserved.

### 1.2 System Role in the Seven-Layer Stack

Google Drive operates at Layer 1.5 — between GitHub governance (L1) and Airtable intelligence (L3). It is the physical asset repository. Airtable holds the metadata and intelligence. Google Drive holds the files. These are complementary, not redundant.

- **Google Drive:** Stores the file
- **Airtable (Creative_Assets):** Stores the metadata, classification, performance data, and status

Every file in Google Drive has a corresponding Creative_Assets record in Airtable with `Google_Drive_URL` linking them.

### 1.3 Pending Activation Requirements

Google Drive as a connected system (Make integration, AI asset ingestion) requires:
- Founder Decision authorizing Google Drive system activation
- Storage governance spec confirmed (this document serves as that spec)
- Make scenario CREATIVE-001 sandbox-validated before production activation
- API credentials stored in credential vault

Manual use of Google Drive (uploading, organizing) may begin immediately after this architecture is approved.

---

## SECTION 2 — MASTER FOLDER STRUCTURE

### 2.1 Root Architecture

```
📁 SSS_CONTENT_LIBRARY/
│
├── 📁 SSS/                          ← She Said Sail brand root
│   ├── 📁 Miami/
│   ├── 📁 Fort_Lauderdale/
│   └── 📁 [City_Name]/              ← Future cities added here
│
├── 📁 ME/                           ← Mare Executive brand root
│   ├── 📁 Miami/
│   ├── 📁 Fort_Lauderdale/
│   └── 📁 [City_Name]/
│
├── 📁 SHARED/                       ← Cross-brand assets (templates only)
│   ├── 📁 Brand_Templates/
│   ├── 📁 Motion_Graphics/
│   └── 📁 Audio_Library/
│
└── 📁 _ARCHIVE/                     ← Retired content — never deleted
    ├── 📁 SSS/
    └── 📁 ME/
```

### 2.2 City Folder Architecture (per brand per city)

```
📁 SSS/Miami/
│
├── 📁 00_RAW_FOOTAGE/
│   ├── 📁 2026/
│   │   ├── 📁 2026-01/
│   │   ├── 📁 2026-05/
│   │   └── 📁 [YYYY-MM]/
│   └── 📁 [YYYY]/
│
├── 📁 01_EDITED_VIDEOS/
│   ├── 📁 Hook_Videos/
│   ├── 📁 Full_Edits/
│   ├── 📁 Testimonials/
│   ├── 📁 BTS/
│   └── 📁 Campaigns/
│       └── 📁 [Campaign_Name]/
│
├── 📁 02_STATIC_IMAGES/
│   ├── 📁 Hero_Images/
│   ├── 📁 Moment_Captures/
│   ├── 📁 Product_Shots/
│   └── 📁 Campaigns/
│       └── 📁 [Campaign_Name]/
│
├── 📁 03_UGC/
│   ├── 📁 Client_Submitted/
│   ├── 📁 Influencer_Deliverables/
│   └── 📁 Crew_Captures/
│
├── 📁 04_COPY_ASSETS/
│   ├── 📁 Captions/
│   ├── 📁 Hook_Scripts/
│   ├── 📁 Ad_Copy/
│   └── 📁 Email_Templates/
│
├── 📁 05_WINNING_CREATIVES/
│   └── [Promoted assets mirrored here — do not move originals]
│
└── 📁 06_APPROVED_FOR_DEPLOY/
    └── [Ready-to-post assets only — cleared by Will]
```

### 2.3 Shared Folder Architecture

```
📁 SHARED/
│
├── 📁 Brand_Templates/
│   ├── 📁 SSS_Templates/
│   │   ├── Lower_Thirds/
│   │   ├── Outro_Cards/
│   │   └── Color_Grades/
│   └── 📁 ME_Templates/
│       ├── Lower_Thirds/
│       ├── Outro_Cards/
│       └── Color_Grades/
│
├── 📁 Motion_Graphics/
│   ├── Transitions/
│   ├── Text_Animations/
│   └── Logo_Animations/
│
└── 📁 Audio_Library/
    ├── Licensed_Tracks/
    ├── Ambient_Backgrounds/
    └── VO_Recordings/
```

---

## SECTION 3 — FILE NAMING CONVENTIONS

### 3.1 Naming Formula

All files follow this mandatory naming structure:

```
[BRAND]_[CITY]_[ASSET_TYPE]_[YYYY-MM-DD]_[DESCRIPTOR]_[VERSION].[EXT]
```

**Rule:** No spaces. Underscores only. All uppercase for structural components. Descriptors use Title_Case.

### 3.2 Component Definitions

| Component | Values | Required |
|-----------|--------|----------|
| BRAND | SSS / ME | Always |
| CITY | MIA / FTL / [3-letter code for future cities] | Always |
| ASSET_TYPE | See table below | Always |
| YYYY-MM-DD | ISO date of capture or creation | Always |
| DESCRIPTOR | Max 3 words, underscore-separated, captures scene or hook | Always |
| VERSION | v1 / v2 / v3 / FINAL | Always |
| EXT | mp4 / mov / jpg / png / pdf / docx | Always |

### 3.3 Asset Type Codes

| Code | Meaning |
|------|---------|
| HOOK | Hook video (first 15 seconds focus) |
| FULL | Full-length edited video |
| BTS | Behind the scenes footage |
| TEST | Testimonial video |
| UGC | User-generated content |
| MOMENT | Moment capture (key emotional scene) |
| HERO | Hero image (feature image) |
| PROD | Product / vessel shot |
| CAP | Caption copy |
| SCRIPT | Hook or ad script |
| ADCOPY | Paid ad copy |
| RAW | Unedited raw footage |

### 3.4 Naming Examples

| File | Description |
|------|-------------|
| `SSS_MIA_HOOK_2026-05-10_Champagne_Toast_v1.mp4` | SSS Miami hook video, champagne moment, first version |
| `SSS_FTL_UGC_2026-04-22_Bachelorette_Deck_FINAL.mp4` | SSS Fort Lauderdale UGC, bachelorette on deck, final approved |
| `ME_MIA_HERO_2026-05-01_Executive_Bow_v2.jpg` | Mare Executive Miami hero image, bow shot, second version |
| `SSS_MIA_SCRIPT_2026-05-15_Proposal_Hook_v1.docx` | SSS Miami proposal moment hook script |
| `SSS_MIA_ADCOPY_2026-05-18_Bachelorette_Meta_v3.txt` | Ad copy for Meta campaign targeting bachelorette |

### 3.5 Version Control Rules

- `v1` = first draft or first edit
- `v2`, `v3` = revision rounds
- `FINAL` = approved by Will — no further edits without creating a new version
- Never overwrite a FINAL file — create a new version (v1 of a new date if substantially changed)
- RAW footage: never versioned — RAW files are immutable once captured

### 3.6 Prohibited Naming Patterns

| Prohibited | Reason |
|------------|--------|
| Spaces in filenames | Breaks Make automation URL handling |
| `final_final`, `v2_FINAL_real` | Version confusion — one FINAL only |
| Names without date | Cannot be sorted or retrieved by campaign period |
| Generic names (`video1.mp4`, `IMG_2034.jpg`) | Breaks AI retrieval and audit trail |
| Brand mixing in one filename | Each file belongs to one brand |

---

## SECTION 4 — TAGGING CONVENTIONS

### 4.1 Google Drive Tagging Layer

Google Drive supports custom metadata via file descriptions and color labels. These are used in addition to the file naming system for retrieval.

**Color Label System:**

| Color | Meaning |
|-------|---------|
| Green | Approved for Deploy |
| Blue | Winner / High Performer |
| Yellow | In Review |
| Orange | Needs Revision |
| Red | Brand Compliance Flag |
| Grey | Archived |
| No color | New / Unreviewed |

### 4.2 File Description Tags

Each Google Drive file description field contains structured tags in this format:

```
#brand:SSS #city:MIA #type:HOOK #hook:Curiosity #emotion:Aspiration #platform:TikTok,Instagram #status:APPROVED #airtable:CA-2026-0047
```

| Tag | Values |
|-----|--------|
| #brand | SSS / ME |
| #city | MIA / FTL / [city code] |
| #type | HOOK / FULL / BTS / TEST / UGC / MOMENT / HERO / PROD |
| #hook | Curiosity / Social_Proof / Transformation / Emotion / Authority / Contrast |
| #emotion | Joy / Desire / FOMO / Aspiration / Comfort / Belonging / Pride / Surprise |
| #platform | TikTok / Instagram_Reels / Instagram_Feed / Both |
| #status | RAW / IN_EDIT / REVIEW / APPROVED / DEPLOYED / RETIRED |
| #airtable | CA-YYYY-NNNN (Creative_Assets record ID) |
| #moment | Champagne / Proposal / Caviar / Sunset / GroupJoy / Emotional (if luxury moment present) |
| #winner | TRUE (only if promoted to Winning_Creatives) |

### 4.3 Tag Maintenance Rules

- Tags written by editor at upload (partial)
- Tags completed by AI during CREATIVE-001 tagging flow
- #airtable tag written by Make when Creative_Assets record is created
- #winner tag written by Make when Winning_Creatives promotion is confirmed
- #status tag updated by Make at each status transition
- Human never overwrites AI-assigned tags without Will approval

---

## SECTION 5 — RETRIEVAL ARCHITECTURE

### 5.1 Retrieval Scenarios and Paths

**Scenario: Find all winning SSS Miami hook videos**
```
Path: SSS/Miami/05_WINNING_CREATIVES/ 
Filter: Color label = Blue + #type:HOOK
Airtable: Winning_Creatives table → filter Brand=SSS, City=Miami, Asset_Type=Hook_Video
```

**Scenario: Find all UGC from bachelorette charters in 2026**
```
Path: SSS/Miami/03_UGC/Client_Submitted/ (+ FTL equivalent)
Filter: date range 2026 + #emotion:Joy or Pride
Airtable: Creative_Assets → filter Asset_Type=UGC_Edited, Shoot_Date in 2026, Charter_Grade_At_Capture=A
```

**Scenario: Find the specific creative that drove 3+ bookings**
```
Airtable path: Campaign_Creatives → filter Bookings_Attributed ≥ 3 → follow Creative_Asset link → get Google_Drive_URL
```

**Scenario: Find all creatives currently fatiguing on Instagram**
```
Airtable: Creative_Fatigue → filter Platform=Instagram, Fatigue_Status=CONFIRMED → follow Creative_Asset link → get Google_Drive_URL
```

**Scenario: Brief next creative batch**
```
Airtable: Winning_Creatives → filter Brand=SSS, Replicate_Hook=true, Brief_Generated=false → export Pattern_Summary for each → Google Drive path for reference assets
```

### 5.2 AI-Assisted Retrieval (Future)

When Google Drive API is activated:

1. Claude receives a retrieval request (e.g., "find all calm elevated UGC with champagne moments from Miami")
2. Claude generates a structured query: `{brand: SSS, city: MIA, energy_profile: Calm_Elevated, luxury_moment: Champagne_Pour, asset_type: UGC}`
3. Make queries Airtable Creative_Assets table with these filters
4. Returns list of matching assets with Google_Drive_URL links
5. Claude returns a curated shortlist with scoring context

Retrieval AI never downloads or modifies files — read-only access only.

---

## SECTION 6 — ARCHIVE ARCHITECTURE

### 6.1 Archive Triggers

A file is moved to `_ARCHIVE/` when ANY of the following occur:

| Trigger | Source |
|---------|--------|
| Creative_Assets status = ARCHIVED | Airtable status change |
| Creative_Fatigue: Fatigue_Status = RETIRED for > 90 days | Make automated |
| Asset is more than 18 months old with no active deployment | Make scheduled scan |
| Brand compliance violation confirmed by Will | Will manually |
| Campaign completed + asset not promoted to Winning_Creatives | Make automated |

### 6.2 Archive Path Structure

```
_ARCHIVE/
├── SSS/
│   ├── Miami/
│   │   ├── 2025/
│   │   └── 2026/
│   └── Fort_Lauderdale/
│       └── 2026/
└── ME/
    └── Miami/
        └── 2026/
```

Files in archive retain their original name plus `_ARCHIVED` suffix:

```
SSS_MIA_HOOK_2026-02-14_Valentine_Group_FINAL_ARCHIVED.mp4
```

### 6.3 Archive Rules

- Files in `_ARCHIVE/` are never deleted — only archived
- Files in `_ARCHIVE/` are read-only — no modifications permitted
- Archive folders are reviewed annually by Will
- Permanent deletion requires a Founder Decision
- Winning_Creatives records in Airtable that link to archived assets are not deleted — they are flagged `Still_Relevant = false`
- Raw footage is never archived to trash under any circumstances

### 6.4 Archive Retention Periods

| Asset Type | Minimum Retention |
|------------|-------------------|
| Raw footage | 36 months minimum |
| Winning creative final edits | Permanent (never deleted) |
| Standard edited videos | 24 months |
| Static images | 24 months |
| UGC (with creator consent on file) | 24 months |
| UGC (no consent documentation) | Delete within 30 days if consent cannot be confirmed |
| Ad copy and scripts | 24 months |

---

## SECTION 7 — MULTI-BRAND SCALABILITY

### 7.1 Adding a New Brand

When a third brand is launched:

1. Add a new root folder at `SSS_CONTENT_LIBRARY/[BRAND_CODE]/`
2. Replicate the city folder architecture exactly
3. Add new Brand code to all Airtable Brand fields (via Founder Decision — schema change)
4. Add new naming prefix for the brand
5. Add new brand to AI tagging prompt system context
6. Update Master Brand Governance with new brand voice spec
7. No cross-brand content sharing — each brand folder is fully isolated

### 7.2 Adding a New City

When SSS or ME expands to a new city:

1. Add new city folder under the relevant brand root: `SSS/[City_Name]/`
2. Replicate the full city folder structure (Sections 00–06)
3. Add 3-letter city code to naming convention table (this document)
4. Add city code to Airtable City field values (via Founder Decision — schema change)
5. Add city to AI tagging prompt context
6. No existing city content is moved — each city maintains independent content library

### 7.3 Multi-City Content Reuse Rules

Some content performs across cities (e.g., a hook shot on a specific yacht that operates in multiple cities):

| Scenario | Handling |
|----------|----------|
| Same asset reused in different city | Create a new Campaign_Creatives record in the new city; link to same Creative_Assets record; use city-specific tagging |
| Asset originally shot in one city recut for another | Create a new Creative_Assets record for the reedited version; link to original as `Source_Asset` |
| Template or motion graphic used across cities | Lives in `SHARED/` — linked from multiple Creative_Assets records |

**Rule:** One physical file = one Creative_Assets record. Never share one record across cities if the deployment context differs.

---

## SECTION 8 — AIRTABLE SYNC ARCHITECTURE

### 8.1 Google Drive ↔ Airtable Sync Flow

```
File uploaded to Google Drive (correct folder + naming convention)
    ↓
Editor tags file description with partial tags (#brand, #city, #type)
    ↓
Make scenario CREATIVE-UPLOAD-001 detects new file (webhook or scheduled scan)
    ↓
Make creates Creative_Assets record in Airtable with:
  - Asset_Name (from filename)
  - Brand, City, Asset_Type (parsed from filename)
  - Google_Drive_URL
  - Status = REVIEW_PENDING
    ↓
CREATIVE-001 triggers AI tagging
    ↓
AI returns full classification → Make writes to Creative_Assets record
    ↓
Make writes #airtable:[CA-ID] tag back to Google Drive file description
    ↓
Status = APPROVED (pending Will review queue)
```

### 8.2 Status Sync Rules

When Creative_Assets status changes in Airtable, Make updates Google Drive color label:

| Airtable Status | Google Drive Color |
|-----------------|-------------------|
| REVIEW_PENDING | Yellow |
| APPROVED | No color (awaiting Will queue) |
| DEPLOYED | Green (active) |
| RETIRED | Grey |
| ARCHIVED | Grey (moved to _ARCHIVE/) |
| Brand compliance flagged | Red |

---

## SECTION 9 — GOVERNANCE

Content library governance is subordinate to:
- 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
- 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED
- 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION (Section 1.4 — Google Drive pending activation)

**Structural changes to this folder architecture require a Founder Decision.**

No Google Drive API connection to Make or AI systems activates before Founder Decision authorizes the Google Drive system activation.

---

SHE SAID SAIL · CONTENT LIBRARY STRUCTURE
CONFIDENTIAL · INTERNAL USE ONLY
