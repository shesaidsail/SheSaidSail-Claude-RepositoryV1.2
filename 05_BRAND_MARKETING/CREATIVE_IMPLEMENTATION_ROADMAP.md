# CREATIVE_IMPLEMENTATION_ROADMAP

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
> This document is the implementation roadmap for the Creative + Marketing Intelligence Core. It sequences the build across seven phases, defines dependencies on the existing migration plan, specifies what gets built in each phase, and identifies what requires Founder Decisions before implementation. This roadmap does not authorize implementation — it plans for it. No Airtable tables are built until Will issues the authorizing Founder Decision for each phase.

---

## SECTION 1 — PREREQUISITE DEPENDENCIES

### 1.1 Migration Prerequisites

The Creative Intelligence Core cannot be built until specific upstream migration phases complete. These are non-negotiable sequencing dependencies.

| Prerequisite | Source | Status Required Before Creative Build |
|-------------|--------|---------------------------------------|
| Phase 1 complete | Airtable_Final_Build_Spec_v2.0 | Universal fields (UUID, Environment, Brand, City) added to ALL existing tables |
| Phase 2 complete | Airtable_Final_Build_Spec_v2.0 | Governance tables created (AI_Audit, Automation_Health) |
| Phase 3 complete | Airtable_Final_Build_Spec_v2.0 | Influencers table migrated from appVWYY9Fp6tKu94m; Organic_Content optimized; Paid_Ads confirmed solid |
| Google Drive activation | Systems_Intelligence_Architecture_v2.0 Section 1.4 | Founder Decision authorizing Google Drive system activation |
| Meta API sandbox | Systems_Intelligence_Architecture_v2.0 Section 1.4 | Founder approval + sandbox validation for Meta API |
| TikTok API sandbox | Systems_Intelligence_Architecture_v2.0 Section 1.4 | Founder approval + sandbox validation for TikTok API |

**Until Phases 1–3 are confirmed complete, no new Creative Intelligence tables are added to the production base.**

### 1.2 Founder Decisions Required

The following Founder Decisions must be issued before the corresponding implementation phase begins:

| Decision Required | For Phase | Content |
|------------------|-----------|---------|
| FD: CREATIVE_INTELLIGENCE_CORE_APPROVED | Phase 0 | Authorizes this entire roadmap to proceed |
| FD: GOOGLE_DRIVE_SYSTEM_ACTIVATION | Phase 1 | Authorizes Google Drive API connection to Make |
| FD: META_API_SANDBOX_APPROVED | Phase 2 | Authorizes Meta API sandbox validation |
| FD: TIKTOK_API_SANDBOX_APPROVED | Phase 2 | Authorizes TikTok API sandbox validation |
| FD: CREATIVE_TABLES_PRODUCTION_BUILD | Phase 1 | Authorizes table creation in production base |
| FD: META_API_PRODUCTION_APPROVED | Phase 3 | Authorizes Meta API live connection |
| FD: TIKTOK_API_PRODUCTION_APPROVED | Phase 3 | Authorizes TikTok API live connection |
| FD: SCORING_WEIGHTS_V1 | Phase 2 | Authorizes initial scoring weight configuration |
| FD: SYNTER_DEPLOYMENT_INTEGRATION | Phase 3 | Authorizes Synter API connection to Make |

---

## SECTION 2 — PHASE 0: ARCHITECTURE REVIEW AND APPROVAL

**Timeline:** 1–2 weeks
**Gate:** Will reviews and approves all 7 architecture documents
**Prerequisite:** Airtable migration Phases 1–3 must be confirmed complete before Phase 1 of Creative begins

### Phase 0 Deliverables

| Deliverable | Status |
|-------------|--------|
| CREATIVE_INTELLIGENCE_ARCHITECTURE.md | Complete — awaiting approval |
| CONTENT_LIBRARY_STRUCTURE.md | Complete — awaiting approval |
| CREATIVE_DNA_ENGINE.md | Complete — awaiting approval |
| MARKETING_LEARNING_LOOP_SPEC.md | Complete — awaiting approval |
| CONTENT_ROI_INTELLIGENCE.md | Complete — awaiting approval |
| LUXURY_MOMENT_INTELLIGENCE.md | Complete — awaiting approval |
| CREATIVE_IMPLEMENTATION_ROADMAP.md | Complete — awaiting approval |

### Phase 0 Actions

- [ ] Will reviews all 7 documents
- [ ] Will issues amendments or approval notes per document
- [ ] Locked governance conflicts (if any) flagged to Will for resolution
- [ ] FD: CREATIVE_INTELLIGENCE_CORE_APPROVED issued by Will
- [ ] Confirm Airtable migration Phase 3 complete before Phase 1 creative build begins

---

## SECTION 3 — PHASE 1: CONTENT LIBRARY AND GOOGLE DRIVE

**Timeline:** 2–3 weeks (after Phase 0 approval)
**Gate:** Google Drive architecture approved; FD: CREATIVE_TABLES_PRODUCTION_BUILD issued
**Prerequisite:** Airtable Phase 3 complete

### Phase 1 Deliverables

**Google Drive (manual — can begin immediately after Phase 0 approval):**
- [ ] Create master folder structure: `SSS_CONTENT_LIBRARY/`
- [ ] Create brand roots: `SSS/` and `ME/`
- [ ] Create city folders for Miami and Fort Lauderdale under each brand
- [ ] Create all sub-folders per CONTENT_LIBRARY_STRUCTURE.md Section 2.2
- [ ] Create `SHARED/` folder with templates and audio library
- [ ] Create `_ARCHIVE/` structure
- [ ] Migrate any existing content to correct folder paths
- [ ] Apply naming convention to any existing files (manually)
- [ ] Set up Google Drive color label system

**Airtable — Phase 1 Tables:**
- [ ] Extend Organic_Content table: add 14 new fields from CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 8.1
- [ ] Extend Paid_Ads table: add 9 new fields from CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 8.2
- [ ] Create Creative_Assets table with full field spec (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 3)
- [ ] Verify Copy/Creative_Assets table field alignment

**Make — Phase 1 Scenarios (sandbox first):**
- [ ] CREATIVE-UPLOAD-001: File detection + naming validation + Creative_Assets record creation
- [ ] CREATIVE-DAILY-001: Daily review queue Slack summary to Will

**Founder Decisions Required:**
- [ ] FD: GOOGLE_DRIVE_SYSTEM_ACTIVATION (if Make → Google Drive integration used)
- [ ] FD: CREATIVE_TABLES_PRODUCTION_BUILD

**Phase 1 Success Criteria:**
- Google Drive folder structure complete and accessible to all authorized team members
- Creative_Assets table live in production
- Organic_Content and Paid_Ads table extensions complete
- First asset uploaded, named correctly, and Creative_Assets record created manually
- Will's daily review queue functioning

---

## SECTION 4 — PHASE 2: AI TAGGING AND CREATIVE INTELLIGENCE TABLES

**Timeline:** 3–4 weeks (after Phase 1 complete)
**Gate:** Phase 1 confirmed complete; FD: META_API_SANDBOX_APPROVED; FD: TIKTOK_API_SANDBOX_APPROVED

### Phase 2 Deliverables

**Airtable — Phase 2 Tables:**
- [ ] Create Campaign_Creatives table (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 4)
- [ ] Create Creative_Scoring table (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 7)
- [ ] Create Creative_Fatigue table (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 6)
- [ ] Create Winning_Creatives table (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 5)
- [ ] Add Luxury Moment fields to Creative_Assets (LUXURY_MOMENT_INTELLIGENCE.md Section 4.1)
- [ ] Add attribution fields to Bookings table (CONTENT_ROI_INTELLIGENCE.md Section 8.2)
- [ ] Create Creator_ROI table (CONTENT_ROI_INTELLIGENCE.md Section 3)

**Make — Phase 2 Scenarios (sandbox validation required before production):**
- [ ] CREATIVE-001: AI tagging via Claude API — sandbox test with 10 real assets
- [ ] CREATIVE-004: Creative Scoring calculation
- [ ] CREATIVE-005: Winner eligibility check + Founder Decision creation
- [ ] CREATIVE-006: Fatigue detection routine

**Claude Prompt Engineering:**
- [ ] Build and sandbox-test asset classification prompt (CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 10.1)
- [ ] Build and sandbox-test winner pattern analysis prompt (Section 10.2)
- [ ] Calibrate confidence threshold (default 70) — adjust based on sandbox results
- [ ] Build caption generation prompt (MARKETING_LEARNING_LOOP_SPEC.md Section 5.2)

**Scoring Weight Configuration:**
- [ ] Will issues FD: SCORING_WEIGHTS_V1 with approved weighting (default per CREATIVE_INTELLIGENCE_ARCHITECTURE.md Section 7.2)
- [ ] Implement weighting formula in Creative_Scoring table

**Platform API — Sandbox:**
- [ ] Meta API sandbox: connect to Make test environment; validate performance data pull
- [ ] TikTok API sandbox: connect to Make test environment; validate performance data pull

**Phase 2 Success Criteria:**
- AI tags 20 real assets in sandbox with ≥ 70% confidence average
- Will reviews and validates AI tag accuracy on 20 assets
- Creative_Scoring produces results that Will considers reasonable
- Fatigue detection runs on test data without false positives
- Winner eligibility check creates accurate Founder Decisions

---

## SECTION 5 — PHASE 3: PERFORMANCE TRACKING AND LIVE API CONNECTIONS

**Timeline:** 2–3 weeks (after Phase 2 validated)
**Gate:** Phase 2 sandbox validation complete; FD: META_API_PRODUCTION_APPROVED; FD: TIKTOK_API_PRODUCTION_APPROVED; FD: SYNTER_DEPLOYMENT_INTEGRATION

### Phase 3 Deliverables

**Platform API — Production:**
- [ ] Meta API: connect live to Make production environment
- [ ] TikTok API: connect live to Make production environment
- [ ] Validate first weekly data sync (CREATIVE-003)
- [ ] Confirm performance fields update correctly on Campaign_Creatives records
- [ ] Activate performance alert rules (CREATIVE-ALERT-001)

**Synter Integration:**
- [ ] Synter API credentials stored in credential vault
- [ ] CREATIVE-PAID-002 scenario built and sandbox-tested
- [ ] First deployment package generated and reviewed by Will
- [ ] Validate Deployed_At timestamp writes correctly to Campaign_Creatives
- [ ] Confirm Audit_Log entry created on every deployment

**Make — Phase 3 Scenarios (production):**
- [ ] CREATIVE-003: Weekly performance sync — live
- [ ] CREATIVE-ALERT-001: Performance threshold alerts — live
- [ ] CREATIVE-007: Fatigue confirmation and retirement — live
- [ ] CREATIVE-PAID-001: Deployment package preparation — live
- [ ] CREATIVE-PAID-002: Synter deployment trigger — live
- [ ] CREATIVE-ORG-001: Organic content publish reminder — live
- [ ] CREATIVE-CAPTION-001: Caption generation — live

**Phase 3 Success Criteria:**
- First weekly performance sync completes without errors
- Performance data visible on Campaign_Creatives records
- First paid campaign deployed through Synter with full audit trail
- First alert triggered and delivered to Will via Slack
- First fatigue detection event fires correctly

---

## SECTION 6 — PHASE 4: CREATIVE DNA ENGINE

**Timeline:** 4–6 weeks (after Phase 3 stable for 2+ weeks)
**Gate:** At least 10 assets scored + 3 Winning_Creatives promoted; Phase 3 stable

### Phase 4 Deliverables

**Airtable — Phase 4 Tables:**
- [ ] Create Creative_DNA table (CREATIVE_DNA_ENGINE.md Section 2)
- [ ] Add Source_DNA_Pattern link field to Creative_Assets
- [ ] Create Luxury_Moment_Intelligence table (LUXURY_MOMENT_INTELLIGENCE.md Section 3)

**DNA Pattern Seeding:**
- [ ] Will manually reviews first 3 Winning_Creatives and identifies shared patterns
- [ ] First DNA pattern created manually by Will (Source_System = Will_Manual)
- [ ] Will approves first pattern (Will_Approved = true, Brand_Calibrated = true)
- [ ] First Brief_Template written for this pattern

**Make — Phase 4 Scenarios:**
- [ ] CREATIVE-008: DNA pattern extraction + brief generation — sandbox then live
- [ ] CREATIVE-010: Quarterly DNA pattern usage scan — live
- [ ] Luxury Moment Intelligence sync: monthly rollup calculation — live

**Brief Generation Testing:**
- [ ] First creative brief generated from first approved DNA pattern
- [ ] Will reviews brief for quality and brand alignment
- [ ] Brief released to creator or editor
- [ ] Track whether brief-sourced asset performs above or below benchmark

**Phase 4 Success Criteria:**
- At least 3 active, Will-approved DNA patterns
- First creative brief generated and delivered to creator
- Luxury Moment Intelligence table populated with data from first 3 months of tracking
- Monthly moment performance report generated and useful

---

## SECTION 7 — PHASE 5: CONTENT ROI INTELLIGENCE

**Timeline:** 2–3 weeks (after Phase 4 stable)
**Gate:** Phase 4 stable; at least 20 Campaign_Creatives records with performance data; first booking attribution logged

### Phase 5 Deliverables

**Airtable — Phase 5 Build:**
- [ ] Add all ROI fields to Creative_Assets (Section 2.3 of CONTENT_ROI_INTELLIGENCE.md)
- [ ] Add ROI fields to Influencers table (Section 6.2)
- [ ] Add ROI fields to Affiliates table (Section 7.3)
- [ ] Add editor ROI fields to Contractors table (Section 4.4)
- [ ] Add hook profitability fields to Creative_DNA (Section 5.3)
- [ ] Create all ROI views in Airtable (Section 9.1)

**Make — Phase 5 Scenarios:**
- [ ] CREATIVE-QUARTERLY-001: Quarterly attribution report — live
- [ ] CREATIVE-009 enhancement: add ROI summary to monthly report

**Attribution Workflow:**
- [ ] Luciana trained on attribution logging in Bookings table
- [ ] First 20 past bookings retrospectively attributed (where source is known)
- [ ] Attribution tracking integrated into standard intake process

**Phase 5 Success Criteria:**
- Creator_ROI table shows at least 5 creator records with meaningful data
- Asset ROI Leaderboard view shows ranked assets by ROAS
- First quarterly attribution report generated and reviewed by Will
- Hook profitability ranking visible from Creative_DNA view

---

## SECTION 8 — PHASE 6: LEARNING LOOP MATURITY AND OPTIMIZATION

**Timeline:** Ongoing — begins Month 4+ after Phase 5
**Gate:** All previous phases stable; first full learning loop revolution complete

### Phase 6 Activities

**Loop Velocity Measurement:**
- Track time from upload to recommendation for each asset
- Goal: < 14-day full loop revolution by Month 6
- Weekly velocity report added to CREATIVE-009

**Prompt Recalibration:**
- Review AI_Audit corrections quarterly
- Will reviews correction patterns for prompt improvement opportunities
- Prompt updates via AI_Prompt_Versions governance (version control per existing spec)
- Each prompt update creates a new AIV record and is sandboxed before production

**Scoring Weight Recalibration:**
- After 6 months of data: Will reviews scoring weights against actual booking correlation
- If weights need adjustment: FD issued for new SCORING_WEIGHTS_V2
- Recalibration logged to AI_Prompt_Versions-equivalent for scoring models

**DNA Pattern Library Growth:**
- Target: 10 active DNA patterns by Month 6
- Target: 3+ brief success rate data points per pattern by Month 9
- Quarterly pattern review with Will: retire underperformers, elevate new patterns

**Moment Protocol Evolution:**
- Quarterly review: which luxury moments are rising or declining?
- Capture protocol updates as new moments are identified
- New moment categories require Founder Decision to add to taxonomy

**Multi-City Scaling:**
- When a new city activates: replicate Google Drive folder structure
- Add city to all relevant Airtable field values (via Founder Decision)
- Add city context to AI tagging prompt
- First 30 days in new city: focus on capture, not optimization
- Month 2 in new city: begin DNA comparison — does existing SSS DNA translate to this city?

---

## SECTION 9 — IMPLEMENTATION RISK REGISTER

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| AI tagging confidence too low | Medium | High | Extensive sandbox testing before production; manual review queue for low-confidence assets |
| Platform API rate limits slow performance sync | Low | Medium | Stagger API calls; implement retry logic in CREATIVE-003 |
| Google Drive naming convention non-compliance | High | Medium | CREATIVE-UPLOAD-001 pre-validation; Luciana training; naming convention reference card |
| Over-automation before data volume exists | Medium | High | Phase gates prevent moving forward without minimum data thresholds |
| Brand voice drift in AI-generated captions | Medium | High | All captions human-reviewed; prohibited word list enforced in prompt; Will's final approval on all deployed captions |
| Winner promotion becoming too frequent (dilutes Winning_Creatives) | Low | Medium | Strict threshold enforcement; Will's manual approval gate for every promotion |
| Creative_DNA patterns becoming stale | Medium | Medium | CREATIVE-010 quarterly scan; quarterly Will review of pattern library |
| Influencer attribution dark spots | High | Medium | Multi-signal attribution model; clear intake script for Luciana to ask source question |
| Synter API integration failure | Low | High | Rollback to manual Synter upload; Audit_Log records campaign intent; retry logic with 4x exponential backoff |
| Scoring weight miscalibration | Medium | High | 6-month data review before recalibration; Founder Decision for any weight change |

---

## SECTION 10 — IMPLEMENTATION GOVERNANCE

### 10.1 Decision Authority

| Decision Type | Authority |
|---------------|-----------|
| Phase gate approval | Will only |
| Table creation in production | Founder Decision required |
| Make scenario production activation | Will approval + Audit_Log entry |
| API connections to production | Founder Decision required |
| Scoring weight changes | Founder Decision required |
| DNA pattern approval | Will only |
| New moment category in taxonomy | Founder Decision required |
| Prompt changes | AI_Prompt_Versions governance (Will approval) |

### 10.2 Rollback Protocols

Each phase has a defined rollback path:

| Phase | Rollback Action |
|-------|-----------------|
| Phase 1 (tables) | Archive new tables; revert field additions; restore from pre-build backup |
| Phase 2 (AI tagging) | Disable CREATIVE-001; set all assets back to REVIEW_PENDING (manual queue) |
| Phase 3 (API connections) | Disable Make scenarios; revert to manual data entry; alert Will |
| Phase 4 (DNA engine) | Disable CREATIVE-008; Creative_DNA table set to read-only; briefs generated manually |
| Phase 5 (ROI) | Views and fields remain (data harmless); disable quarterly report scenarios |
| Phase 6 (optimization) | Rollback individual prompt versions; revert scoring weights via Founder Decision |

### 10.3 Quality Gates Per Phase

Before moving to the next phase:
1. Will confirms phase deliverables complete
2. Make scenarios sandbox-validated for new automations
3. No open errors in Automation_Health table
4. No pending Brand Compliance Founder Decisions unresolved
5. Will approves phase completion via Founder Decision or written confirmation

---

## SECTION 11 — SUMMARY TIMELINE

| Phase | Name | Duration | Key Deliverable |
|-------|------|----------|-----------------|
| 0 | Architecture Review | 1–2 weeks | FD: CREATIVE_INTELLIGENCE_CORE_APPROVED |
| 1 | Content Library + Google Drive | 2–3 weeks | Google Drive live; Creative_Assets table created |
| 2 | AI Tagging + Creative Tables | 3–4 weeks | All 5 creative tables built; AI tagging live in sandbox |
| 3 | Performance Tracking + APIs | 2–3 weeks | Meta/TikTok live; Synter live; weekly performance sync |
| 4 | Creative DNA Engine | 4–6 weeks | 3+ approved DNA patterns; first creative brief generated |
| 5 | Content ROI Intelligence | 2–3 weeks | Creator/influencer ROI visible; attribution tracking live |
| 6 | Learning Loop Maturity | Ongoing | Self-improving loop; prompt recalibration; city scaling |

**Total time from Phase 0 to Phase 5 complete: approximately 4–5 months**
(Dependent on Airtable migration Phases 1–3 being complete before Phase 1 creative build begins)

---

SHE SAID SAIL · CREATIVE IMPLEMENTATION ROADMAP
CONFIDENTIAL · INTERNAL USE ONLY
