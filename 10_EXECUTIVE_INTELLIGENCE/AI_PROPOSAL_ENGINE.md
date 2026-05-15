# SHE SAID SAIL + MARE EXECUTIVE
MIAMI · FORT LAUDERDALE

# AI PROPOSAL ENGINE
AI Recommendation Architecture · Proposal Queue Design · Confidence-Weighted Proposals · Founder Decision Gateway

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

The AI Proposal Engine is how Claude recommends strategic and operational improvements to Will.

AI systems that observe operational patterns without a structured mechanism to share what they're seeing are a wasted resource. AI systems that recommend without governance are a liability.

This engine solves both problems:
- Claude generates structured proposals based on observed patterns
- Every proposal routes through the founder decision gateway
- Proposals are prioritized by confidence, evidence quality, and potential impact
- Will reviews proposals efficiently — one decision at a time
- Approved proposals are tracked to outcome
- Denied proposals create explicit boundaries
- Both outcomes compound intelligence

---

# GOVERNING PRINCIPLES

1. AI proposes — Will decides — always
2. Proposals must include evidence, not just opinion
3. Proposal confidence must be honest — optimistic proposals erode trust
4. No proposal may bypass the review queue
5. Denied proposals are boundaries — they feed back into AI behavior
6. Approved proposals are tracked to outcome — was the proposal correct?
7. Proposal volume must never overwhelm the founder — quality over quantity

---

# PROPOSAL TAXONOMY

## Proposal Categories

| CATEGORY | DESCRIPTION |
|----------|-------------|
| SOP Improvement | Recommends a change to an existing SOP based on observed drift or better pattern |
| New SOP | Recommends creation of an SOP where none exists for a recurring operational pattern |
| Autonomy Expansion | Recommends a Tier B or Tier C category be promoted to Tier A eligibility |
| Autonomy Contraction | Recommends reducing AI autonomy based on quality degradation |
| Lesson Activation | AI identifies a pending lesson as ready for active status |
| Pricing Strategy | Recommends a pricing adjustment based on booking pattern data |
| Vendor Action | Recommends vendor promotion, demotion, or removal based on performance data |
| Outreach Strategy | Recommends changes to planner or broker outreach approach |
| Content Strategy | Recommends creative or advertising adjustments based on performance |
| Operational Efficiency | Recommends automation or workflow improvements |
| Risk Mitigation | Recommends preemptive action on a detected risk pattern |
| Expansion Readiness | Recommends city launch timing or readiness assessment |

---

# PROPOSAL DATA MODEL

## Identity Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Proposal UUID | UUID | YES — Immutable |
| Proposal ID | Formula | YES — PROP-[YYYY]-[SEQ] |
| Created At | DateTime | YES — Immutable |
| Updated At | DateTime | YES |
| Environment | Single Select | YES |
| Brand | Single Select | YES — SSS / MARE / Both |
| City | Single Select | NO |

## Classification Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Category | Single Select | YES |
| Subcategory | Single Select | NO |
| Priority | Single Select | YES — Critical / High / Medium / Low |
| Urgency | Single Select | YES — Immediate / This Week / This Month / Whenever |
| Status | Single Select | YES |
| Source | Single Select | YES — AI Generated / Lessons Engine / Risk Intelligence / Luciana |

## Evidence Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Situation Summary | Long Text | YES — what Claude observed |
| Evidence | Long Text | YES — specific data, records, patterns, counts |
| Evidence Record IDs | Long Text | NO — linked UUIDs supporting the proposal |
| Pattern Duration | Single Select | NO — when pattern started |
| Instances Observed | Number | NO — how many times the pattern occurred |
| Comparison Baseline | Long Text | NO — what normal looks like for comparison |

## Proposal Content Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Proposed Action | Long Text | YES — specific, actionable recommendation |
| Expected Outcome | Long Text | YES — what should improve and by how much |
| Implementation Effort | Single Select | YES — Low / Medium / High |
| Risk If Approved | Long Text | YES — what could go wrong |
| Risk If Not Approved | Long Text | YES — what happens if we don't act |
| Alternatives Considered | Long Text | NO — other options Claude evaluated |
| Related Lessons | Long Text | NO — UUIDs of lessons that support this proposal |
| Related SOP | Long Text | NO — UUID of SOP this would affect |

## Confidence Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| AI Confidence Score | Number | YES — 1–100 |
| Confidence Basis | Long Text | YES — what drives the confidence level |
| Data Quality | Single Select | YES — Strong / Moderate / Weak / Inferential |
| Sample Size | Number | NO — records analyzed to generate proposal |
| Confidence Caveat | Long Text | NO — honest limitations of the proposal |

## Decision Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Decision | Single Select | NO — Approved / Denied / Modified / Deferred |
| Decision Notes | Long Text | NO — Will's reasoning |
| Modified Proposal | Long Text | NO — Will's version if modified |
| Decided At | DateTime | NO |
| Decided By | Single Select | NO — WILL only |
| Auto-Apply Eligible | Checkbox | NO — Will sets true if this proposal type can auto-apply after 5 approvals |

## Outcome Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Implementation Date | Date | NO |
| Outcome Tracked | Checkbox | NO |
| Actual Outcome | Long Text | NO |
| Proposal Accuracy | Single Select | NO — Accurate / Partially Accurate / Inaccurate |
| Outcome Notes | Long Text | NO |
| Lesson Generated | Checkbox | NO |

---

# PROPOSAL STATUS LIFECYCLE

| STATUS | MEANING |
|--------|---------|
| Queued | Awaiting Will review |
| In Review | Will is actively reviewing |
| Approved | Will approved — awaiting implementation |
| Implementing | Implementation in progress |
| Complete | Implemented and outcome tracking active |
| Denied | Will denied — boundary established |
| Modified | Will approved a modified version |
| Deferred | Valid but not timely — revisit later |
| Superseded | A better proposal replaced this one |
| Archived | Permanent record — no active status |

---

# PROPOSAL PRIORITIZATION ALGORITHM

Proposals are ranked in the review queue by:

| FACTOR | WEIGHT |
|--------|--------|
| Severity of risk if not approved | 35% |
| AI Confidence Score | 25% |
| Evidence quality (Strong > Moderate > Weak > Inferential) | 20% |
| Urgency classification | 15% |
| Expected outcome magnitude | 5% |

Proposals scoring above 80 in the priority calculation surface in Will's daily view.

Proposals scoring below 40 aggregate in the weekly digest.

---

# PROPOSAL GENERATION TRIGGERS

## Automatic Triggers

The system generates a proposal automatically when:

| TRIGGER | PROPOSAL CATEGORY | CONFIDENCE MINIMUM |
|---------|------------------|-------------------|
| SOP drift detected (threshold met) | SOP Improvement | 65% |
| Risk pattern detected (same risk 3x in 30 days) | Risk Mitigation | 70% |
| Lesson in Tested status with 5+ applications | Autonomy Expansion | 75% |
| Vendor rating degradation (pattern confirmed) | Vendor Action | 80% |
| Lead response time degradation (pattern confirmed) | SOP Improvement | 70% |
| Charter Grade decline (4-week trend) | SOP Improvement / Operational Efficiency | 65% |
| AI modification rate increasing (14-day trend) | SOP Improvement / AI Governance | 70% |
| Recurring operational pattern with no SOP | New SOP | 60% |
| Ad performance pattern (30-day trend) | Content Strategy | 60% |

## Manual Triggers

- Will requests a proposal on a specific topic
- Luciana surfaces an observation worth formalizing
- Post-incident review identifies a systematic improvement
- Quarterly review identifies a gap requiring formal recommendation

---

# PROPOSAL QUALITY STANDARDS

Every proposal submitted to the review queue must meet:

**Evidence standard:** The proposal includes specific data — not vague trends. Example: "Response time on hot leads exceeded 2 hours in 7 of the last 14 cases" — not "response times seem slower."

**Specificity standard:** The Proposed Action describes exactly what should change, not just that something should change.

**Honesty standard:** Confidence caveats must reflect genuine limitations. A 60% confidence proposal is not dressed up as 80%.

**Completeness standard:** Both Risk If Approved and Risk If Not Approved are required — proposals that only argue for approval are incomplete.

Proposals failing quality standards are returned to generation with a quality note rather than surfaced to Will.

---

# PROPOSAL REVIEW INTERFACE

Will reviews proposals through the Founder Command Center.

The review interface presents for each proposal:
- Proposal title and category
- Evidence summary (3–5 bullet points)
- Proposed action (1–2 sentences)
- Confidence score + basis
- Risks if approved and if not
- One-tap decision: Approve / Deny / Modify / Defer

Target review time per proposal: under 2 minutes for standard proposals.

Complex proposals (Implementation Effort = High or financial impact) include a longer summary and expect 5–10 minute review.

---

# AUTONOMY EXPANSION PROPOSALS

Autonomy expansion proposals deserve specific governance.

A proposal to expand AI autonomy (Tier B → Tier A for a category) requires:

- Minimum 5 consecutive approvals of that action type without modification
- Zero denials of that action type in the past 90 days
- AI Confidence Score consistently above 85% for that action type
- Outcome tracking showing positive results
- Explicit Evidence section showing the specific approval history
- Implementation Effort = High (because the governance change is significant)

Will may approve, deny, or defer with no minimum approval count required to override.

A single denial of an autonomy expansion proposal does not prevent the proposal from being resubmitted after new evidence accumulates.

---

# PROPOSAL LEARNING LOOP

Every decided proposal feeds back into the system:

## Approved Proposals

- Implementation tracked
- Outcome monitored after 30/60/90 days
- Proposal accuracy scored
- If accurate: positive signal for similar future proposals
- If inaccurate: lesson created from the gap

## Denied Proposals

- Denial reason classified and stored
- Decision Note treated as direct founder instruction
- AI behavior updated to avoid generating similar proposals without new evidence
- Denial pattern: if same proposal type denied 3+ times, category enters reduced confidence weighting

## Modified Proposals

- Will's modification is the definitive version
- Modification delta analyzed — what did Will change and why?
- Modification becomes a lesson candidate
- Future proposals in same category use modified version as the quality baseline

---

# PROPOSAL VOLUME GOVERNANCE

The proposal queue must not overwhelm Will.

## Volume Limits

| PRIORITY | DAILY MAXIMUM IN QUEUE |
|----------|----------------------|
| Critical | No limit — all surface immediately |
| High | 3 per day |
| Medium | 5 per week (batch in digest) |
| Low | Monthly digest only |

If volume exceeds these limits:
- Lower priority proposals are batched and deferred
- Volume spike itself generates a diagnostic flag — what is generating excess proposals?
- Volume reduction is a system health signal, not a feature

---

# PROPOSAL REPORTING

## Thursday Digest Contribution

- Proposals awaiting Will decision (count and priority breakdown)
- Top 3 highest-priority proposals this week
- Proposals approved this week and implementation status
- Denial pattern update — any category generating repeated denials

## Monthly Proposal Review

- Total proposals generated
- Approval rate by category
- Average time from generation to decision
- Outcome accuracy rate (how often were approved proposals correct?)
- Top denial patterns — what is AI proposing that Will consistently declines?
- Proposals that resulted in lessons

---

# GOVERNANCE RULES

1. AI may not implement any proposal without Will approval
2. Denied proposals create explicit operational boundaries
3. All proposals are permanent records — no deletion
4. Proposal generation triggers may not be modified without Will approval
5. Autonomy expansion proposals require the full evidence standard — no shortcuts
6. Proposal confidence scores must be calibrated honestly
7. Volume limits protect Will from proposal fatigue
8. Every approved proposal requires outcome tracking — approval without tracking is incomplete governance

---

# SUCCESS CONDITION

The AI Proposal Engine is functioning correctly when:

- Will reviews all Critical and High proposals within 48 hours of generation
- Approved proposals produce measurably positive outcomes at a rate above 70%
- Denied proposals generate explicit operational boundaries that reduce recurrence
- Proposal quality improves over time — evidence standards tighten as the system matures
- AI behavior measurably incorporates denial patterns within 30 days
- Monthly proposal volume stays within governance limits

---

SHE SAID SAIL + MARE EXECUTIVE · AI PROPOSAL ENGINE
CONFIDENTIAL · INTERNAL USE ONLY
