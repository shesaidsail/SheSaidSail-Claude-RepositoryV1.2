# SYSTEM CONSOLIDATION MAP
## She Said Sail + Mare Executive — Intelligence Layer Overlap Analysis

**Document ID:** SYSTEM_CONSOLIDATION_MAP
**Status:** CONSOLIDATION AUTHORITY
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## SECTION 1 — FULL SYSTEM INVENTORY

### 1.1 Source Documents Analyzed

| Document | Branch | Domain | Status |
|----------|--------|--------|--------|
| CREATIVE_INTELLIGENCE_ARCHITECTURE.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| CONTENT_LIBRARY_STRUCTURE.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| CREATIVE_DNA_ENGINE.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| MARKETING_LEARNING_LOOP_SPEC.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| CONTENT_ROI_INTELLIGENCE.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| LUXURY_MOMENT_INTELLIGENCE.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| CREATIVE_IMPLEMENTATION_ROADMAP.md | design-creative-marketing-core-En1eN | Creative | DRAFT |
| REVENUE_INTELLIGENCE_ARCHITECTURE.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| RELATIONSHIP_INTELLIGENCE_SPEC.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| CLIENT_LTV_ENGINE.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| REFERRAL_INTELLIGENCE.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| OFFER_INTELLIGENCE.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| PRICING_INTELLIGENCE.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| REVENUE_IMPLEMENTATION_ROADMAP.md | revenue-relationship-intelligence-KEjpo | Revenue | DRAFT |
| LESSONS_ENGINE_SPEC.md | executive-operational-intelligence-layer-qITnZ | Executive | PRODUCTION |
| ADAPTIVE_SOP_ENGINE.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| RISK_INTELLIGENCE_SPEC.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| RESPONSE_INTELLIGENCE_SPEC.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| AI_GOVERNANCE_INTELLIGENCE.md | executive-operational-intelligence-layer-qITnZ | Executive | PRODUCTION |
| AI_PROPOSAL_ENGINE.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| FOUNDER_COMMAND_CENTER_SPEC.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| EXECUTIVE_INTELLIGENCE_ROADMAP.md | executive-operational-intelligence-layer-qITnZ | Executive | DRAFT |
| 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION.md | main | Core | PRODUCTION |
| 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md | main | Core | PRODUCTION |

---

## SECTION 2 — OVERLAP MATRIX

### 2.1 System-Level Overlaps

| Conflict | System A | System B | Type | Resolution |
|----------|----------|----------|------|-----------|
| OV-01 | AI Audit Table (AI_GOVERNANCE_INTELLIGENCE) | Audit Log (Systems_Intelligence_Architecture Sec XV) | DUPLICATE PURPOSE | MERGE — Audit Log absorbs AI quality records |
| OV-02 | Adaptive SOP Engine | Lessons Engine | DUPLICATE SCOPE | COLLAPSE — SOP evolution is a Lessons output category |
| OV-03 | Founder Command Center | Operations Portal (Sec VI) | DUPLICATE INTERFACE | MERGE — add intelligence cards to existing portal |
| OV-04 | Thursday Digest (INTELLIGENCE-001) | Lessons Digest | DUPLICATE DELIVERY | MERGE — lessons section added to single Thursday Digest |
| OV-05 | Revenue Intelligence Report (Monday) | Thursday Digest | DUPLICATE DELIVERY | MERGE — revenue section moved to Thursday Digest |
| OV-06 | Response Intelligence Spec | Systems Intelligence Architecture Sec IV (Claude Orchestration) | REDUNDANT | ABSORB — Response Intel informs prompt content, not a new system |
| OV-07 | AI Proposal Engine | Sec IV Tier B definition | REDUNDANT | ABSORB — Proposal drafting is existing Tier B behavior |
| OV-08 | Risk Intelligence Spec | Anomaly Detection (Sec VII.5) | PARTIAL OVERLAP | COMPRESS — Risk fields on Bookings, anomaly rules enhanced |
| OV-09 | Creative Scoring (table) | Performance_Score field concept | UNNECESSARY ABSTRACTION | COLLAPSE — Score as fields on Creative_Assets |
| OV-10 | Winning_Creatives (table) | Filtered view concept | UNNECESSARY TABLE | CONVERT to view |
| OV-11 | Client_LTV_Scores (separate table) | Clients table fields | PREMATURE NORMALIZATION | COLLAPSE — LTV fields directly on Clients |
| OV-12 | Relationship_Scores (separate table) | Clients + Partner_Outreach fields | PREMATURE NORMALIZATION | COLLAPSE — Relationship fields directly on records |
| OV-13 | Referral_Network (separate table) | Affiliates + relationship data | PREMATURE NORMALIZATION | COLLAPSE — Referral fields directly on Affiliates |
| OV-14 | Offer_Performance (separate table) | Packages fields | PREMATURE NORMALIZATION | COLLAPSE — Performance fields directly on Packages |
| OV-15 | Campaign_Creatives (Phase 4) | Organic_Content + Paid_Ads (existing) | PREMATURE COMPLEXITY | DEFER — not needed at current creative volume |
| OV-16 | Creative_Fatigue (Phase 4) | Fatigue fields on existing tables | PREMATURE COMPLEXITY | DEFER — fatigue fields on existing tables until volume justifies |
| OV-17 | Marketing Learning Loop | Lessons Engine | OVERLAP | COLLAPSE — Content learning is a Lessons Engine category |
| OV-18 | Content ROI Intelligence | Revenue Intelligence + Creative Intelligence | OVERLAP | COLLAPSE — Attribution fields on Organic_Content + Creative_Assets |
| OV-19 | Content Library Structure | Creative_Assets table | OVERLAP | ABSORB — Content Library naming conventions apply to Creative_Assets |

---

## SECTION 3 — DUPLICATE SCORING SYSTEMS

One of the highest-risk patterns in the proposed architecture is the proliferation of separate scoring tables and separate scoring systems. This creates:
- Multiple scores per client/asset with no clear hierarchy
- Founders forced to reconcile competing scores
- Make scenarios computing redundant calculations
- Airtable table explosion from unnecessary normalized tables

### 3.1 Scoring System Inventory

| Score | Location (Proposed) | Consolidation Decision |
|-------|--------------------|-----------------------|
| Client LTV Score | Client_LTV_Scores table | FIELDS on Clients table |
| Relationship Score | Relationship_Scores table | FIELDS on Clients + Partner_Outreach |
| Referral Quality Score | Referral_Network table | FIELDS on Affiliates |
| Revenue Health Score | Revenue_Snapshots table | Revenue_Snapshots record field — KEEP (time-series needed) |
| Demand Score | Demand_Signals table | Demand_Signals record field — KEEP (time-series needed) |
| Creative Performance Score | Creative_Scoring table | FIELDS on Creative_Assets |
| Creative Fatigue Decay | Creative_Fatigue table | DEFER — fields on Campaign_Creatives when built |
| Risk Score | Risk Intelligence Spec (new table proposed) | FIELDS on Bookings |
| AI Confidence Score | AI Audit table | FIELD on Audit_Log (existing) |
| Charter Health Score | Not explicitly proposed | FORMULA on Bookings (D7_Review_Eligible already captures this) |

### 3.2 Retained Scoring Tables (justified)

| Table | Why Standalone | Volume Pattern |
|-------|---------------|----------------|
| Revenue_Snapshots | Weekly time-series by city+brand — one record per period per market | ~8 records/week |
| Demand_Signals | Weekly time-series signal capture | ~8 records/week |
| Yield_Log | Immutable recommendation log — audit trail | ~5–20 records/week |
| Pricing_Recommendations | Audit trail for pricing decisions — append-only | ~5–10 records/week |

---

## SECTION 4 — CONFLICTING LOGIC

### 4.1 Identified Logic Conflicts

| Conflict | System A | System B | Resolution |
|----------|----------|----------|-----------|
| CL-01: Client Scoring Authority | Relationship_Intelligence_Spec: relationship score drives VIP designation | Client_LTV_Engine: LTV tier drives VIP designation | RESOLVED: VIP_Flag = checkbox set by Will only. Both scores are inputs to Will's review, not autonomous VIP setters. |
| CL-02: Discount Authority | Pricing_Intelligence says AI can recommend −7% off-peak | Commercial_Authority_Framework defines approved discount scenarios | RESOLVED: Commercial_Authority_Framework governs. Pricing_Intelligence recommendations require Will approval before any rate applies. |
| CL-03: Offer Autonomy | Offer_Intelligence proposes upsell recommendations sent autonomously | Founder Control Framework requires Tier B for financial recommendations | RESOLVED: Founder Control Framework governs. All upsell recommendations are Tier B — drafted by AI, reviewed by Luciana or Will before sending. |
| CL-04: Creative Approval | CREATIVE_INTELLIGENCE_ARCHITECTURE says brand compliance check gates publishing | Brand Governance says Will reviews all creative | RESOLVED: Both apply in sequence. AI flags compliance. Will approves all creative. No conflict — sequential gates. |
| CL-05: Lessons Auto-Apply | Lessons Engine proposes autonomy threshold after 5 consecutive approvals | AI_GOVERNANCE_INTELLIGENCE says autonomy never expands without explicit Will approval | RESOLVED: Founder Control Framework governs. 5-approval pattern surfaces an ELIGIBILITY candidate. Will must explicitly enable Auto-Apply on that category. AI never self-applies. |
| CL-06: AI confidence and action | Response_Intelligence_Spec allows Tier A action at confidence ≥ 80 | Founder Control Framework defines Tier A scope without confidence as the gating mechanism | RESOLVED: Tier definition governs. Confidence score is a logged data point, not an autonomy gate. Low confidence triggers escalation but high confidence does not expand autonomy. |

---

## SECTION 5 — UNNECESSARY ABSTRACTIONS

### 5.1 Over-Engineered Patterns Identified

| Pattern | Identified In | Why Unnecessary | Action |
|---------|-------------|----------------|--------|
| Separate AI_Audit table | AI_GOVERNANCE_INTELLIGENCE | Audit_Log already logs every AI action; a separate table for AI quality review adds a join without adding value | MERGE into Audit_Log with Audit_Category field |
| Creative_Scoring as a standalone table | CREATIVE_INTELLIGENCE_ARCHITECTURE | Score values are per-asset-per-period; this belongs as fields on Campaign_Creatives (deferred) or Creative_Assets, not a separate table with its own schema | COLLAPSE to fields |
| Winning_Creatives as a standalone table | CREATIVE_INTELLIGENCE_ARCHITECTURE | Winner designation is a status on Creative_Assets, not a separate entity with its own record | CONVERT to filtered view |
| Campaign_Creatives at current scale | CREATIVE_INTELLIGENCE_ARCHITECTURE | At <5 paid campaigns/week, deployment tracking is handled adequately by Organic_Content and Paid_Ads tables. A separate linking table adds complexity with no operational benefit at current volume | DEFER to Phase 5 |
| Separate LTV / Relationship / Referral tables | REVENUE_INTELLIGENCE_ARCHITECTURE et al. | These are scores on client and affiliate records. Creating separate tables for each score type forces multiple lookups for basic client context. Fields on the source tables are correct at this scale. | COLLAPSE to fields |
| Separate Monday revenue report | REVENUE_INTELLIGENCE_ARCHITECTURE | One Thursday Digest is sufficient. Two separate reports to the same person on the same data is overhead, not intelligence. | MERGE into Thursday Digest |
| Adaptive SOP Engine as a separate system | ADAPTIVE_SOP_ENGINE | SOP evolution is an output of the Lessons Engine. A Lessons Engine with a "SOP" subcategory and an "SOP Update Candidate" flag achieves the same result with no new tables, no new Make scenarios, and no new governance overhead. | COLLAPSE into Lessons Engine |
| Founder Command Center as a separate interface | FOUNDER_COMMAND_CENTER_SPEC | Operations Portal already exists and is production infrastructure. Adding intelligence cards to the existing portal achieves the same result without building a second interface with its own codebase and access management. | MERGE into Operations Portal |
| AI Proposal Engine as a separate system | AI_PROPOSAL_ENGINE | Charter proposals are Tier B outputs. The Claude orchestration in Systems_Intelligence_Architecture_v2.0 already defines this behavior. The Proposal Engine provides prompt detail that belongs in AI_Prompt_Versions, not a new operational system. | ABSORB into AI_Prompt_Versions content |

---

## SECTION 6 — REDUNDANT OPERATIONAL STRUCTURES

### 6.1 Make Scenario Redundancy

| Proposed Separate Scenario | Redundant With | Resolution |
|---------------------------|---------------|-----------|
| CREATIVE-001 (asset tagging) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-002 (campaign create) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-003 (weekly performance sync) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-004 (threshold breach) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-005 (winner flagging) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-006 (fatigue detection) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-007 (fatigue alert) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-008 (brief generation) | CREATIVE-MASTER module | Consolidate into orchestrator |
| CREATIVE-009 (monthly report) | INTELLIGENCE-MASTER | Creative report section in Thursday Digest |
| Separate Revenue intelligence scenarios | FINANCIAL-MASTER + INTELLIGENCE-MASTER | Revenue intelligence embedded in existing orchestrators |
| Separate AI Audit review scenario | INTELLIGENCE-MASTER | AI quality section in Thursday Digest |
| Separate Lessons Digest scenario | INTELLIGENCE-MASTER | Lessons section in Thursday Digest |

### 6.2 Review Cadence Redundancy

| Cadence | Overlap | Resolution |
|---------|---------|-----------|
| Weekly Luciana AI sample review | Overlaps with Thursday Digest AI summary | Luciana reviews → logs to Audit_Log → Thursday Digest AUTO-INCLUDES AI quality summary from Audit_Log |
| Monthly AI Governance Report | Overlaps with monthly Thursday Digest first of month | First Thursday Digest of month = extended AI governance section |
| Weekly Lessons Digest | Overlaps with Thursday Digest | Consolidated into Thursday Digest Operational Intelligence section |
| Monday Revenue Report | Overlaps with Thursday Digest | Consolidated into Thursday Digest Revenue section |

---

## SECTION 7 — CONSOLIDATION DECISIONS SUMMARY

| ID | Decision | Impact | Documents Affected |
|----|----------|--------|-------------------|
| CD-01 | MERGE AI_Audit into Audit_Log | −1 table | AI_GOVERNANCE_INTELLIGENCE |
| CD-02 | COLLAPSE Adaptive SOP Engine into Lessons Engine | −1 system, −0 tables (was document-only) | ADAPTIVE_SOP_ENGINE |
| CD-03 | MERGE Founder Command Center into Operations Portal | −1 interface | FOUNDER_COMMAND_CENTER_SPEC |
| CD-04 | MERGE all digests into Thursday Digest | −3 separate Make scenarios | LESSONS_ENGINE, REVENUE_INTEL, AI_GOVERNANCE |
| CD-05 | ELIMINATE Creative_Scoring table | −1 table → fields on Creative_Assets | CREATIVE_INTELLIGENCE_ARCHITECTURE |
| CD-06 | CONVERT Winning_Creatives to view | −1 table | CREATIVE_INTELLIGENCE_ARCHITECTURE |
| CD-07 | DEFER Campaign_Creatives to Phase 5 | −1 table from Phase 4 | CREATIVE_INTELLIGENCE_ARCHITECTURE |
| CD-08 | DEFER Creative_Fatigue to Phase 5 | −1 table from Phase 4 | CREATIVE_INTELLIGENCE_ARCHITECTURE |
| CD-09 | COLLAPSE Client_LTV_Scores to fields on Clients | −1 table | CLIENT_LTV_ENGINE |
| CD-10 | COLLAPSE Relationship_Scores to fields on Clients + Partner_Outreach | −1 table | RELATIONSHIP_INTELLIGENCE_SPEC |
| CD-11 | COLLAPSE Referral_Network to fields on Affiliates | −1 table | REFERRAL_INTELLIGENCE |
| CD-12 | COLLAPSE Offer_Performance to fields on Packages | −1 table | OFFER_INTELLIGENCE |
| CD-13 | ABSORB Response Intelligence into AI_Prompt_Versions content | −1 spec system | RESPONSE_INTELLIGENCE_SPEC |
| CD-14 | ABSORB AI Proposal Engine into AI_Prompt_Versions content | −1 spec system | AI_PROPOSAL_ENGINE |
| CD-15 | COMPRESS Risk Intelligence into Risk fields on Bookings + enhanced anomaly detection | −1 spec system | RISK_INTELLIGENCE_SPEC |
| CD-16 | ELIMINATE Monday Revenue Report | −1 Make scenario | REVENUE_INTELLIGENCE_ARCHITECTURE |

**Net result:** −9 proposed tables eliminated, −7 proposed separate systems collapsed, −4 separate digest/report mechanisms unified, 35+ proposed scenarios reduced to 11 master orchestrators.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*SYSTEM_CONSOLIDATION_MAP v1.0*
*Effective May 2026*
