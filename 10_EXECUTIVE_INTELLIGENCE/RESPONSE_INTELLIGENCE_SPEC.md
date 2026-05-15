# SHE SAID SAIL + MARE EXECUTIVE
MIAMI · FORT LAUDERDALE

# RESPONSE INTELLIGENCE SPECIFICATION
AI Response Quality Architecture · Compounding Communication Intelligence · Tone Calibration · Response Pattern Recognition

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

The Response Intelligence system governs how AI communication quality compounds over time.

Every approved response, every modification Will or Luciana makes to an AI draft, every denial of an AI message, every booking that converts or does not convert — contains signal.

This system captures that signal, structures it, and feeds it back into AI response generation so that communication quality improves continuously without requiring manual recalibration.

This is the intelligence layer that transforms raw AI output into She Said Sail–calibrated luxury communication.

---

# GOVERNING PRINCIPLES

1. AI responses must meet luxury hospitality standards — not just be grammatically correct
2. Every human modification to an AI draft is a learning signal
3. Every approval without modification is a positive reinforcement signal
4. Every denial is an explicit boundary signal
5. Confidence scoring must be honest — high confidence on poor outputs is worse than low confidence
6. Response quality is brand-specific — SSS tone and MARE tone are distinct
7. Context matters more than templates — response intelligence enables context-aware communication

---

# RESPONSE QUALITY DIMENSIONS

Every AI response is evaluated across five quality dimensions:

| DIMENSION | DEFINITION | MEASURED BY |
|-----------|------------|-------------|
| Tone Accuracy | Does the response match brand voice for the context? | Human review score + modification rate |
| Accuracy | Is all factual content correct — no hallucinations? | Audit flag + verification check |
| Appropriateness | Is the response calibrated to the client's emotional state? | Escalation outcome + human review |
| Completeness | Does it address what the client asked without excess? | Human review score |
| Conversion Alignment | Does it move the booking forward appropriately? | Booking outcome linkage |

---

# RESPONSE RECORD DATA MODEL

Every AI-generated response that is sent or reviewed generates a Response Record.

## Identity Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Response UUID | UUID | YES — Immutable |
| Response ID | Formula | YES — RESP-[YYYY]-[SEQ] |
| Created At | DateTime | YES — Immutable |
| Environment | Single Select | YES |
| Brand | Single Select | YES — SSS / MARE |
| City | Single Select | NO |

## Context Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Request UUID | Single Line | YES — linked to triggering inquiry |
| Client UUID | Single Line | YES — linked to client record |
| Channel | Single Select | YES — SMS / Email / Slack |
| Context Type | Single Select | YES — See Context Types below |
| Client Tier | Single Select | YES — Standard / HV / VIP |
| Booking Stage | Single Select | YES — Inquiry / Proposal / Active / Post-Charter |
| AI Authority Level | Single Select | YES — Tier A / Tier B |
| Prompt Version | Single Line | YES — version active at generation |
| Model Version | Single Line | YES |

## Content Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| AI Draft | Long Text | YES — original AI output |
| Final Sent Content | Long Text | NO — actual message sent (if modified) |
| Was Modified | Checkbox | YES |
| Modification Summary | Long Text | NO — what changed and why |
| Was Denied | Checkbox | YES |
| Denial Reason | Single Select | NO |
| Denial Notes | Long Text | NO |

## Quality Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| AI Confidence Score | Number | YES — 1–100 |
| Tone Score | Number | NO — 1–10 reviewer score |
| Accuracy Flag | Checkbox | NO — true = hallucination or error detected |
| Appropriateness Score | Number | NO — 1–10 |
| Reviewer | Single Select | NO — WILL / LUCIANA |
| Reviewed At | DateTime | NO |
| Overall Quality Score | Number | NO — calculated average |

## Outcome Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Client Response Received | Checkbox | YES |
| Response Time | Duration | NO — time to client reply |
| Booking Outcome | Single Select | NO — Progressed / Stalled / Lost / Converted |
| Escalation Triggered | Checkbox | NO |
| Lesson Generated | Checkbox | NO |

---

# CONTEXT TYPES

AI responses are classified by context to enable context-specific learning.

| CONTEXT TYPE | DESCRIPTION |
|--------------|-------------|
| Initial Inquiry Response | First response to new inbound lead |
| Qualification Follow-up | Follow-up questions after initial contact |
| Proposal Delivery | Package and pricing proposal |
| Booking Confirmation | Confirming a confirmed booking |
| Pre-Charter Communication | 72h, 48h, day-before prep messages |
| Post-Charter Follow-up | D1, D7, D30 sequences |
| Review Request | Review solicitation message |
| Upsell Attempt | Add-on or upgrade offer |
| Re-engagement | Lead that went cold |
| Escalation Handoff | Transition to human handling |
| HV Client Communication | Any message to an HV-flagged client |
| Broker Communication | Coordination with charter brokers |

---

# AI CONFIDENCE SCORING

Every AI-generated response includes a confidence score from 1–100.

## Confidence Score Factors

| FACTOR | WEIGHT | DESCRIPTION |
|--------|--------|-------------|
| Context completeness | 30% | How complete is the available client + booking context? |
| Lesson alignment | 25% | Do active lessons provide clear guidance for this context? |
| Template match | 20% | Does this context map to a proven response pattern? |
| Ambiguity level | 15% | How many interpretations are possible for the inbound message? |
| Client tier familiarity | 10% | Has this client tier been encountered in similar contexts? |

## Confidence Thresholds

| SCORE RANGE | CLASSIFICATION | BEHAVIOR |
|-------------|----------------|----------|
| 90–100 | High Confidence | Tier A eligible — send with logging |
| 75–89 | Confident | Tier B standard — human review before send |
| 60–74 | Moderate | Tier B flagged — reviewer prompted to scrutinize |
| 40–59 | Low | Tier B required — reviewer alerted to low confidence |
| Below 40 | Very Low | Escalate to human — AI draft provided as reference only |

No Tier A message is sent with confidence below 80 unless explicitly authorized by founder for that context type.

---

# RESPONSE PATTERN RECOGNITION

The system identifies patterns across response records.

## Positive Patterns (Reinforcement)

A response pattern is positive when:
- Same context type
- Modified less than 15% of the time
- Approval rate > 90%
- Associated bookings progress at above-average rate
- No escalations triggered

Positive patterns become:
- Weighted highly in AI context for that context type
- Candidates for lesson creation
- Inputs for SOP refinement

## Negative Patterns (Constraints)

A response pattern is negative when:
- Modification rate > 40% on same context type
- Denial rate > 20%
- Associated escalation rate > 10%
- Repeated accuracy flags in same category

Negative patterns trigger:
- Prompt review recommendation
- Lesson candidate creation
- Risk flag (SEV-3) if pattern persists 14+ days

---

# MODIFICATION SIGNAL INTELLIGENCE

When Will or Luciana modifies an AI draft before sending, the modification is itself intelligence.

## Modification Classification

| MODIFICATION TYPE | WHAT IT SIGNALS |
|------------------|-----------------|
| Tone softening | AI was too direct or cold for context |
| Tone warming | AI was too formal or distant for context |
| Price clarification | AI introduced ambiguity in pricing reference |
| Fact correction | AI hallucinated or used incorrect data |
| Length reduction | AI was verbose for this context type |
| Personalization addition | AI missed available client context |
| Urgency reduction | AI was too pushy for luxury positioning |
| Escalation language removal | AI referenced escalation-level content in standard context |

## Modification Learning Protocol

1. Modification classified by type
2. Classification linked to context type and client tier
3. Pattern analysis: has this modification type occurred 3+ times in same context?
4. If yes: lesson candidate generated
5. If modification involves pricing or brand standards: SEV-3 risk flag created
6. Modification summary stored on Response Record
7. AI prompt recommendation generated if pattern threshold met

---

# RESPONSE QUALITY FEEDBACK LOOP

```
AI GENERATES RESPONSE
        ↓
CONFIDENCE SCORE ASSIGNED
        ↓
[TIER A] → SENT → OUTCOME LOGGED
        ↓
[TIER B] → HUMAN REVIEWS
    /         \
APPROVED   MODIFIED   DENIED
    ↓          ↓         ↓
LOGGED    CLASSIFIED  CLASSIFIED
    ↓          ↓         ↓
PATTERN   LESSON     LESSON
ANALYSIS  CANDIDATE  CANDIDATE
    ↓          ↓         ↓
        AI CONTEXT UPDATE
        (next Thursday)
```

---

# TONE CALIBRATION BY BRAND AND CONTEXT

## She Said Sail Tone Standards

| CONTEXT | TONE TARGET | AVOID |
|---------|-------------|-------|
| Initial inquiry | Warm, excited, aspirational | Formal, transactional |
| HV client | Exclusive, personal, unhurried | Salesy, rushed |
| Post-charter | Genuinely grateful, memorable | Generic, template-obvious |
| Recovery | Warm, owning it, forward-looking | Defensive, over-apologetic |
| Bachelorette | Fun, celebratory, high energy | Corporate, flat |

## Mare Executive Tone Standards

| CONTEXT | TONE TARGET | AVOID |
|---------|-------------|-------|
| Initial inquiry | Refined, intelligent, professional | Casual, over-familiar |
| Corporate client | Efficient, premium, reliable | Salesy, over-eager |
| HV client | Discreet, exclusive, attentive | Overly effusive |
| Post-event | Measured appreciation, professional | Gushing, informal |

Tone calibration is brand-specific and never cross-contaminated.

---

# WEEKLY AI RESPONSE AUDIT

Every week, Luciana reviews 5 randomly selected AI responses from the past 7 days.

Review includes:
- Tone score (1–10)
- Accuracy check (hallucination or error present?)
- Appropriateness score (1–10)
- Would she modify it? If yes, what and why?
- Overall quality score

Results logged to AI_Audit table.

Any response scoring below 6.0 in any dimension triggers:
- Lesson candidate creation
- Risk flag if pattern (3+ below-threshold scores in same context type)
- Prompt review recommendation if 5+ below-threshold in 30 days

Will reviews audit summary monthly.

---

# PROMPT VERSION LINKAGE

Every response record links to the active prompt version at time of generation.

This enables:
- Prompt version performance comparison
- Quality trend analysis by prompt version
- Rollback decision support — "V3 of this prompt produced 40% fewer modifications than V4"
- Deployment review — new prompt versions are evaluated against quality baseline

Prompt version performance is included in the monthly AI governance review.

---

# RESPONSE INTELLIGENCE REPORTING

## Thursday Digest Contribution

- AI response quality trend (modification rate this week vs. 30-day average)
- Top 3 modification types this week
- Any context types with degrading quality
- Denial patterns requiring attention
- Confidence score averages by context type

## Monthly AI Quality Report

- Modification rate by context type
- Denial rate by context type and reviewer
- Confidence score accuracy (did high-confidence responses actually perform better?)
- Prompt version performance comparison
- Top lessons generated from response intelligence
- Response outcome correlation — which response patterns led to conversions?

---

# GOVERNANCE RULES

1. AI may not send any response that falls below confidence threshold for its Tier
2. Modification data is response intelligence — never discarded
3. Denial reasons must always be classified — unclassified denials are incomplete
4. Tone calibration is brand-specific — cross-brand blending is a system failure
5. AI confidence scores must be honest — inflating confidence to bypass review is a hard prohibition
6. All sent responses are permanently logged — no deletion
7. HV client responses are always Tier B or Tier C — no autonomy exceptions
8. Post-escalation responses require Will review regardless of confidence score

---

# SUCCESS CONDITION

The Response Intelligence system is functioning correctly when:

- AI modification rate trends below 20% within 6 months of deployment
- Confidence scores correlate meaningfully with actual response quality (r > 0.7)
- Context-specific quality scores improve each quarter
- Will identifies zero luxury positioning violations in weekly audit
- Response patterns generate actionable lessons at least monthly
- Brand tone distinction between SSS and MARE is preserved without manual correction

---

SHE SAID SAIL + MARE EXECUTIVE · RESPONSE INTELLIGENCE SPECIFICATION
CONFIDENTIAL · INTERNAL USE ONLY
