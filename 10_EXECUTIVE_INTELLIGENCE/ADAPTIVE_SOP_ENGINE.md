# SHE SAID SAIL + MARE EXECUTIVE
MIAMI · FORT LAUDERDALE

# ADAPTIVE SOP ENGINE
Self-Improving Standard Operating Procedures · Operational Drift Detection · SOP Proposal Architecture · Founder-Governed SOP Evolution

STATUS: PRODUCTION
VERSION: v1.0
ENVIRONMENT: PRODUCTION
OWNER: WILL HUNT
SOURCE OF TRUTH: YES
CONSTITUTIONAL AUTHORITY: 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
AMENDMENT REQUIRED FOR MODIFICATION: YES

CONFIDENTIAL · INTERNAL USE ONLY · MAY 2026

---

# PURPOSE

The Adaptive SOP Engine ensures that operational standards improve continuously based on real-world outcomes.

SOPs that were designed in year one should not be identical to SOPs in year three. But they should never change without deliberate founder judgment.

This system:
- detects when an SOP is producing suboptimal outcomes
- surfaces the evidence to Will with a specific improvement proposal
- tracks SOP version history permanently
- ensures no SOP changes without Will approval
- compounds operational quality over time

The system adapts. Will governs. SOPs improve.

---

# GOVERNING PRINCIPLES

1. No SOP changes without Will approval — ever
2. AI identifies improvement opportunities — AI does not implement them
3. Every SOP version is permanent — no version is deleted
4. SOP proposals must include evidence, not just suggestions
5. SOPs are brand-specific and city-specific unless explicitly universal
6. Operational drift from an SOP is a detection event — not a failure tolerance
7. The highest-quality SOP is one that has been tested, learned from, and refined

---

# SOP CLASSIFICATION

## SOP Authority Tiers

| TIER | TYPE | CHANGE AUTHORITY |
|------|------|-----------------|
| Tier 1 — Locked | Governance-level standards | Will via formal amendment |
| Tier 2 — Production | Live operational standards | Will approval required |
| Tier 3 — Active | Current workflow SOPs | Will approval required |
| Tier 4 — Draft | Experimental / not yet deployed | Luciana or AI can propose — Will approves |

## SOP Scope Classification

| SCOPE | APPLIES TO |
|-------|------------|
| Universal | Both brands, all cities |
| Brand-Specific | SSS only or MARE only |
| City-Specific | Single market — Miami, Fort Lauderdale, etc. |
| Context-Specific | Single workflow — e.g., HV Client Protocol only |

---

# SOP DATA MODEL

## Identity Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| SOP UUID | UUID | YES | Immutable — never reassigned |
| SOP ID | Formula | YES | SOP-[CATEGORY]-[SEQ]-v[VERSION] |
| SOP Title | Single Line | YES | Descriptive, searchable |
| Version | Number | YES | Incremented on every approved change |
| Version History Reference | Long Text | YES | Pointer to prior version UUID |
| Status | Single Select | YES | Locked / Production / Active / Draft / Archived |
| Created At | DateTime | YES | Immutable |
| Last Modified At | DateTime | YES | Auto-updated |
| Approved By | Single Select | YES | Will only for Production and above |
| Environment | Single Select | YES | Production / Sandbox / Development |

## Classification Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Category | Single Select | YES | Matches Lessons category taxonomy |
| Brand | Single Select | YES | SSS / MARE / Both |
| City | Single Select | NO | Specific market or Universal |
| Authority Tier | Single Select | YES | Tier 1 / Tier 2 / Tier 3 / Tier 4 |
| AI Authority Level | Single Select | YES | Tier A / Tier B / Tier C |
| Related Lesson IDs | Long Text | NO | UUIDs of lessons that informed this SOP |

## Content Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| SOP Summary | Long Text | YES | What this SOP governs — one paragraph |
| Trigger Conditions | Long Text | YES | When this SOP activates |
| Required Steps | Long Text | YES | Ordered execution steps |
| Decision Points | Long Text | YES | Where judgment is required and by whom |
| Escalation Conditions | Long Text | YES | What triggers escalation out of this SOP |
| Success Criteria | Long Text | YES | How to know the SOP worked |
| Failure Signals | Long Text | YES | How to detect the SOP is not working |
| Exceptions | Long Text | NO | Known valid exceptions to standard path |

## Monitoring Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Application Count | Number | YES | Times this SOP has been used |
| Deviation Count | Number | YES | Times deviation was detected |
| Last Applied At | DateTime | NO | Most recent use |
| Outcome Score | Number | NO | Running average outcome quality (1–10) |
| Improvement Proposal Pending | Checkbox | YES | True = proposal awaiting Will review |
| Last Reviewed At | DateTime | NO | Last Will review |

---

# SOP DRIFT DETECTION

## What Is SOP Drift

SOP drift occurs when:
- an operation is executed differently than the SOP specifies
- outcomes from SOP-governed operations degrade over time
- a lesson identifies a systematic gap in the SOP
- escalations cluster around a single SOP trigger point
- AI detects a recurring deviation pattern in operational records

## Drift Detection Sources

| SOURCE | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| Lesson accumulation | 3+ lessons in same SOP category in 30 days | High |
| Charter grade decline | Average grade drops 1.5+ points over 30 days | High |
| Escalation clustering | 2+ escalations from same SOP trigger in 14 days | High |
| Response time degradation | SOP-governed response time increases 40%+ | Medium |
| Deviation logging | Luciana or City Manager explicitly logs a deviation | Medium |
| Audit anomaly | AI audit finds output inconsistent with SOP | Medium |
| Outcome score decline | Outcome Score drops below 6.0 for any SOP | High |

## Drift Detection Cadence

| REVIEW | FREQUENCY | OWNER |
|--------|-----------|-------|
| Automated drift scan | Weekly — every Monday | System (AI) |
| Deviation log review | Ongoing — triggered by detection | Luciana |
| SOP outcome review | Monthly | Luciana + Will |
| Full SOP library audit | Quarterly | Will |

---

# SOP IMPROVEMENT PROPOSAL PROTOCOL

When drift is detected, the system:

1. **Generates a Drift Detection Record** with:
   - Which SOP
   - Evidence: specific records, lessons, escalations, or metrics
   - Drift classification: Outcome / Process / Frequency / Escalation
   - AI's proposed improvement

2. **Routes to AI Proposal Queue** with:
   - Proposal type: SOP Improvement
   - Supporting evidence linked
   - Specific proposed change to SOP text
   - Expected outcome improvement

3. **Will reviews** the proposal:
   - Approve → new SOP version created + deployed
   - Deny → drift flag cleared, Decision Note added
   - Modify → Will's modified version becomes new SOP

4. **New SOP version** activated:
   - Prior version archived permanently
   - Version number incremented
   - Related lessons updated with new SOP reference
   - Automation scenarios updated if applicable

---

# SOP VERSION CONTROL ARCHITECTURE

Every SOP change is:
- a new version with incremented version number
- linked to the prior version via Version History Reference
- date-stamped and Will-attributed
- permanently retained — no versions deleted

## Version Change Requirements

| CHANGE TYPE | PROCESS |
|-------------|---------|
| Minor wording clarification | Will approval + new version |
| Step addition or removal | Will approval + new version + impact review |
| Escalation condition change | Will approval + governance review |
| AI authority level change | Will approval + governance amendment |
| Category or brand scope change | Will approval + full audit |
| Emergency SOP revision | Will direct instruction + retroactive documentation |

## Version History Record

Every version contains:
- Previous version UUID
- What changed (diff summary)
- Why it changed (evidence reference)
- When it changed
- Who approved it

This history constitutes the institutional evolution record.

---

# AI AUTHORITY WITHIN SOPs

Every SOP specifies the AI authority level for each step.

| AI AUTHORITY LEVEL | MEANING IN SOP CONTEXT |
|-------------------|------------------------|
| Tier A — Autonomous | AI executes this step without human review |
| Tier B — Draft + Review | AI generates; human approves before execution |
| Tier C — Human Only | AI has no role in this step |

AI authority levels within SOPs may not exceed the limits defined in Article III of the Founder Control Framework.

A SOP that specifies Tier A for a step that falls under Tier C governance is automatically invalid. Governance supersedes SOP.

---

# SOP LIBRARY VIEWS

## Active SOPs
All Production and Active SOPs currently governing operations.

## Pending Improvement
SOPs with Improvement Proposal Pending = true.

## Drift Detected
SOPs with active drift detection events not yet resolved.

## Version History
Full audit trail of every SOP version ever deployed.

## By Category
Filtered views for each operational category.

## By Brand
SSS-only and MARE-only views for brand-specific management.

---

# QUARTERLY SOP HEALTH REVIEW

Every quarter, Will reviews:

- SOPs with Outcome Score below 7.0 — improvement candidates
- SOPs with zero Application Count in 90 days — archival candidates
- SOPs with Deviation Count > 5 — structural gap indicators
- SOPs with pending proposals older than 30 days
- SOPs not updated in 12+ months — currency review
- New lessons accumulated since last review — do they require SOP updates?
- AI authority levels — should any Tier B SOPs be promoted to Tier A?

Review documented in Governance_Reviews table.

---

# GOVERNANCE RULES

1. No SOP may be modified without Will approval
2. No SOP version may be deleted
3. AI may never self-modify an SOP
4. AI may propose SOP changes — it may not implement them
5. Drift detection does not authorize deviation from the current SOP
6. SOP deviations require explicit logging even if the outcome was positive
7. Emergency SOP deviations require Will review within 24 hours
8. All SOP improvements are routed through the AI Proposal Queue
9. SOP governance hierarchy: Locked > Production > Active > Draft

---

# SUCCESS CONDITION

The Adaptive SOP Engine is functioning correctly when:

- SOPs improve measurably over quarterly cycles
- Operational drift is detected before it becomes pattern failure
- Will reviews SOP proposals in under 5 minutes each
- The same SOP gap does not generate more than one escalation before producing a proposal
- SOP version history constitutes a readable record of operational evolution
- AI execution quality within SOPs improves as SOPs are refined

---

SHE SAID SAIL + MARE EXECUTIVE · ADAPTIVE SOP ENGINE
CONFIDENTIAL · INTERNAL USE ONLY
