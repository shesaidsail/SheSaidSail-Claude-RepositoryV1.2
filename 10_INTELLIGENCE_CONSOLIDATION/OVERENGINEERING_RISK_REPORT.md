# OVERENGINEERING RISK REPORT
## She Said Sail + Mare Executive — Complexity Audit

**Document ID:** OVERENGINEERING_RISK_REPORT
**Status:** CONSOLIDATION AUTHORITY
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

> **Purpose**
>
> This report identifies every pattern across the intelligence layer architecture that creates complexity without proportional operational value. It is a direct intervention against the natural tendency of well-intentioned systems design to produce bureaucratic overhead. The goal is not to criticize the documents — they are thorough and intellectually rigorous. The goal is to ensure the production system reflects what a luxury concierge company at current scale actually needs, not what a mature enterprise intelligence platform would eventually justify.

---

## SECTION 1 — OVERENGINEERING SEVERITY RATINGS

| Rating | Definition |
|--------|-----------|
| **SEV-OE-1** | Will create operational failure if built as proposed. Must not be built. |
| **SEV-OE-2** | Will create significant operational overhead with marginal value. Should not be built now. |
| **SEV-OE-3** | Will create unnecessary complexity at current scale. Defer or simplify. |
| **SEV-OE-4** | Optimization opportunity — simplification available with no value loss. |

---

## SECTION 2 — CRITICAL OVERENGINEERING RISKS

### OE-001 | Separate AI_Audit Table | SEV-OE-1

**The Pattern:** A separate Airtable table (`AI_Audit`) to store AI quality review records, alongside the existing `Audit_Log` table that already captures every AI action.

**Why It's a Problem:**
- Creates two sources of truth for AI behavior records
- Forces joins between tables that should have one record per event
- Weekly Luciana review requires looking in two places
- Will's monthly review requires reconciling two tables
- Make must write to two tables for every AI action → double the error surface

**Operational Reality:** At current AI scale (Phase 1–2), Claude handles inbound responses and post-charter messages. Weekly volume of AI actions: approximately 30–100. This does not justify a separate audit table.

**Resolution:** Add `Audit_Category` field to Audit_Log. All AI quality review records go there with Category = AI_QUALITY_REVIEW. One table. One query. One source of truth.

---

### OE-002 | Campaign_Creatives Table in Phase 4 | SEV-OE-2

**The Pattern:** A full normalized linking table (`Campaign_Creatives`) to track every deployment of every creative asset to every campaign, with 30+ fields including full platform performance data.

**Why It's a Problem:**
- At current creative volume (estimated <10 paid campaigns/month, <20 organic posts/week), the operational overhead of maintaining a Campaign_Creatives record per deployment exceeds the insight value.
- Organic_Content already tracks organic post performance. Paid_Ads already tracks paid campaign performance. These two tables capture 90% of what Campaign_Creatives would add.
- A separate linking table makes sense when one asset runs on 5+ campaigns simultaneously and you need to compare performance across deployments. That's a Phase 5 problem.

**Operational Reality:** SSS currently has 2 active cities and is in early creative development. The insight gained from comparing "the same asset deployed in Campaign A vs. Campaign B" is not available until there's enough volume to run meaningful A/B tests.

**Resolution:** Defer to Phase 5. Add `Creative_Asset_Link` to Organic_Content and Paid_Ads (linked records to Creative_Assets). This captures the relationship without a separate table.

---

### OE-003 | Five Separate Scoring Tables | SEV-OE-2

**The Pattern:** Separate Airtable tables proposed for: Client_LTV_Scores, Relationship_Scores, Referral_Network (score tracking), Creative_Scoring, and Offer_Performance. Each table holds scores that are fundamentally properties of existing records.

**Why It's a Problem:**
- LTV Score is a property of a Client record. Putting it in a separate table means every Client operation requires a join.
- A separate table for Relationship Scores creates a second record for every client — doubling the data model complexity for no operational benefit.
- Make must maintain 5 additional tables, creating 5 additional failure points.
- The founder dashboard must join 5 tables to show a complete client view.

**The False Justification:** "These are computed values, not static data, so they need their own table." This is incorrect. Computed values are fields. They are refreshed by Make. They live on the source record. Bookings already has `Net_Margin_Pct` as a formula field — a computed value that lives on the Booking record. The same principle applies.

**Resolution:** All scores become fields on their source records. LTV_Score, Relationship_Score, Churn_Risk on Clients. Margin_Score, Performance_Tier on Packages. Referral_Quality_Score on Affiliates.

---

### OE-004 | Winning_Creatives as a Separate Table | SEV-OE-2

**The Pattern:** A standalone `Winning_Creatives` table that holds promoted creative assets, with its own schema including pattern intelligence fields (lookups from Creative_Assets) and archive fields.

**Why It's a Problem:**
- Every field in Winning_Creatives is either a lookup from Creative_Assets or a metadata field (Promoted_At, Will_Approved, Pattern_Summary) that can live as fields on Creative_Assets.
- Two tables with one-to-one relationships (one Winning_Creatives record per Creative_Assets record) is a normalization mistake.
- "Winner" is a status. Status fields live on the source record.

**Resolution:** Add to Creative_Assets: `Winner_Status` (checkbox), `Promoted_At` (DateTime), `Pattern_Summary` (Long Text), `Still_Relevant` (checkbox). Create a **view** called "Winning Creatives" filtered on `Winner_Status = true AND Will_Approved = true`. Zero new tables. Full functionality.

---

### OE-005 | Adaptive SOP Engine as a Separate System | SEV-OE-3

**The Pattern:** A separate "Adaptive SOP Engine" specification that creates a parallel system for SOP evolution alongside the Lessons Engine.

**Why It's a Problem:**
- The Adaptive SOP Engine is described as: "when lessons reach Tested status and are applied consistently, they trigger SOP updates." That is exactly what the Lessons Engine already does — lessons reach Tested status and surface as SOP Update Candidates.
- A separate specification implies a separate implementation: separate Make scenarios, potentially separate tables, separate governance review.
- In practice, a Lesson with subcategory = "SOP_Update_Required" and status = Tested is an SOP Update Candidate. This requires one field addition to the Lessons table, not a new system.

**Resolution:** Add `SOP_Update_Required` checkbox to Lessons table. When Will checks this on an approved lesson, it appears in the Thursday Digest "SOP Updates Pending" section. Will acts on it by updating the relevant GitHub document. Total implementation: one field, one view, one digest section.

---

### OE-006 | Founder Command Center as a Separate Interface | SEV-OE-3

**The Pattern:** The FOUNDER_COMMAND_CENTER_SPEC proposes a new interface for the founder, distinct from the Operations Portal already defined in Systems_Intelligence_Architecture_v2.0.

**Why It's a Problem:**
- Two interfaces means two places to check. Founders default to the one they opened most recently, missing items in the other.
- The Operations Portal (Section VI of Systems_Intelligence_Architecture) already defines: Do This Now, Active Bookings, Escalations, Financial Pulse, HV Alerts, EOD Report, System Health.
- The Founder Command Center adds: Revenue Health Score, Demand Outlook, LTV Leaderboard, Referral Network Health, AI Governance Summary.
- These are additions to the existing interface, not justification for a new one.

**Resolution:** Add intelligence cards to the Operations Portal interface as new sections. One interface. Complete visibility.

---

### OE-007 | Three Separate Weekly Reports | SEV-OE-3

**The Pattern:** Three separate automated intelligence deliveries, all going to the same people (Will and Luciana):
1. Monday Revenue Intelligence Report
2. Thursday Digest (existing INTELLIGENCE-001)
3. Thursday Lessons Digest (separate from Thursday Digest)

**Why It's a Problem:**
- Fragmented intelligence delivery trains people to read whichever report seems most urgent and skip the others.
- Three separate Make scenarios doing similar work (reading from Airtable, assembling structured content, sending to Slack).
- The Monday report is premature — at 2 cities and <40 bookings/month, weekly revenue data in Monday doesn't move meaningfully enough from Thursday to warrant a separate digest.

**Resolution:** ONE Thursday Digest. Revenue section included. Lessons section included. AI quality section included. Urgent alerts (SEV-1, SEV-2) still sent via Slack DM immediately when they occur — this is not weekly intelligence, this is real-time alerting. Those two functions (urgent alerts vs. intelligence digest) should never be merged.

---

### OE-008 | Response Intelligence and AI Proposal Engine as Separate Systems | SEV-OE-4

**The Pattern:** Two specification documents (RESPONSE_INTELLIGENCE_SPEC and AI_PROPOSAL_ENGINE) that define behaviors already covered by Systems_Intelligence_Architecture_v2.0 Sections IV and V.

**Why It's a Problem:**
- RESPONSE_INTELLIGENCE_SPEC defines how Claude handles inbound responses. Systems_Intelligence_Architecture Sections 4.1–4.5 already define this: Tier A vs. Tier B scope, context injection architecture, confidence scoring, prompting rules.
- AI_PROPOSAL_ENGINE defines how Claude generates charter proposals. This is a specific Tier B use case covered by the Claude Orchestration section and the Charter Brief spec.
- Two additional specification documents for behavior already specified creates governance drift risk: which document governs when they conflict?

**Resolution:** The production spec (Systems_Intelligence_Architecture v2.0) governs. RESPONSE_INTELLIGENCE_SPEC and AI_PROPOSAL_ENGINE provide PROMPT CONTENT that belongs in AI_Prompt_Versions table — not system architecture specifications. The prompting detail from those documents should be incorporated into the relevant prompt versions, then archived.

---

### OE-009 | Confidence Calibration as a Tracked System | SEV-OE-4

**The Pattern:** The AI_GOVERNANCE_INTELLIGENCE specification calls for formal monthly confidence calibration tracking, including correlation coefficients (r values) between confidence scores and quality ratings, and a target of r > 0.70.

**Why It's a Problem:**
- At Phase 1–2 AI scale (30–100 Claude calls/week), calculating a statistically meaningful correlation coefficient between confidence and quality requires a large enough sample that monthly calculations will produce unreliable r values.
- The overhead of this process (Luciana must track outcomes for every AI response, a system must compute correlations, Will must review the output) exceeds the operational value of knowing whether Claude's self-confidence is calibrated.
- Luciana's weekly 5-response review already identifies systematic confidence miscalibration intuitively ("Claude keeps saying it's 90% confident but we keep having to heavily edit these"). No r value needed to catch that pattern.

**Resolution:** Track `AI_Confidence_Score` on Audit_Log (as currently specified). Include a summary in the monthly Thursday Digest: "Average AI confidence this month: X%. Average modification rate: Y%." If those two numbers diverge significantly, Will initiates a confidence recalibration review. No separate tracking system required.

---

### OE-010 | Marketing Learning Loop as a Separate System | SEV-OE-4

**The Pattern:** MARKETING_LEARNING_LOOP_SPEC describes a feedback system that takes creative performance data and feeds it into the next creative brief. This is described as a distinct "marketing learning loop" system.

**Why It's a Problem:**
- This is the core function of the Lessons Engine applied to the Creative category.
- A content performance lesson (Hook Type X outperformed Hook Type Y by 40% on TikTok in Miami) is a Lesson with Category = Creator, Subcategory = Hook_Performance.
- The Thursday Digest surfaces this for Will's review.
- Approved lessons inform the next creative brief.
- There is no need for a separate system with its own specification.

**Resolution:** Content performance learnings are captured as Lessons (Category: Creator). The MARKETING_LEARNING_LOOP_SPEC should be archived. Its prompting detail informs how Claude generates lesson candidates from creative performance data — that belongs in AI_Prompt_Versions content.

---

## SECTION 3 — PATTERNS THAT ARE NOT OVERENGINEERED (KEEP AS DESIGNED)

The following systems are correctly scoped and should be built as specified:

| System | Why It's Correct |
|--------|-----------------|
| Lessons Engine (full spec) | The complexity is justified. Lessons are the compounding intelligence substrate. Field richness enables precise AI injection. |
| AI Governance in Audit_Log | After compression, this is lightweight and correct. Weekly review + monthly summary in digest is the right cadence. |
| Revenue_Snapshots (time-series) | Cannot be fields — time-series records require separate rows per period. |
| Demand_Signals (time-series) | Same reason as Revenue_Snapshots. |
| Yield_Log (immutable) | Immutable audit trail for rate decisions — a pricing governance requirement. |
| Pricing_Recommendations (append-only) | Separate from Yield_Log — recommendations before approval need their own record |
| Four revenue intelligence tables | All four justified by their time-series or immutable-log nature. |
| Emergency_001 (standalone) | Safety-critical. No complexity reduction is appropriate here. |
| Full Audit Log compliance | Complete audit logging is not bureaucracy — it's acquisition readiness and AI governance. |
| Lessons approval gate | Will reviewing every lesson before it enters AI context is not overhead — it's the mechanism that keeps institutional intelligence calibrated. |
| CHARTER-MASTER sequence | The D1/D7/D30 post-charter sequence is genuinely high-ROI. |

---

## SECTION 4 — RISK IF OVERENGINEERING IS IGNORED

If the intelligence layer is implemented as proposed across all DRAFT documents without consolidation:

| Risk | Probability | Impact |
|------|------------|--------|
| Table sprawl forces Phase 5 rebuild | HIGH | All Make scenarios referencing eliminated tables break |
| Thursday Digest never gets built because 3 separate reports seem easier | HIGH | Founder loses unified intelligence surface |
| AI_Audit + Audit_Log diverge — different AI events in different tables | HIGH | Compliance audit failure; impossible to reconcile |
| 40+ Make scenarios create circular dependency | MEDIUM | Single scenario failure cascades across system |
| Winning_Creatives table falls out of sync with Creative_Assets | HIGH | Two sources of truth for creative performance |
| Campaign_Creatives built at Phase 4, then rebuilt at Phase 5 with different schema | MEDIUM | Double implementation effort |
| 5 separate scoring tables slow every Airtable view and dashboard card | HIGH | Founder interface becomes unusable as records accumulate |
| Founder reads Monday report + Thursday Digest = stops reading one | HIGH | Intelligence delivery failure |

---

## SECTION 5 — OVERENGINEERING PREVENTION RULES (PERMANENT)

Before any new table, scenario, or system is added to the architecture:

1. **Can this data live as fields on an existing record?** If yes, make it fields.
2. **Is this a status, score, or property of an existing entity?** If yes, it's a field.
3. **Does this require time-series records?** If yes, a separate table is justified.
4. **Does this require an immutable append-only log?** If yes, a separate table is justified.
5. **Does this send to the same recipients as an existing delivery?** If yes, embed it.
6. **Is this a behavior of an existing system applied to a new category?** If yes, add a category to the existing system.
7. **At current operational scale, will this be read more than twice per month?** If no, defer or eliminate.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*OVERENGINEERING_RISK_REPORT v1.0*
*Effective May 2026*
