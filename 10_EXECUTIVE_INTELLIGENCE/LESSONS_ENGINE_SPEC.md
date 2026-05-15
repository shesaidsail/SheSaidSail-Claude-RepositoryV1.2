# SHE SAID SAIL + MARE EXECUTIVE
MIAMI · FORT LAUDERDALE

# LESSONS ENGINE SPECIFICATION
Institutional Intelligence Capture · Pattern Recognition · AI Learning Architecture · Compounding Operational Memory

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

The Lessons Engine is the institutional intelligence substrate of She Said Sail and Mare Executive.

Every operational event — booking outcome, client interaction, vendor failure, escalation, pricing decision, response approval — is a source of learning. This specification defines how that learning is captured, structured, weighted, and injected into AI behavior.

The Lessons Engine ensures:
- operational knowledge does not reside in people who leave
- founder calibration is preserved permanently
- AI quality compounds over time
- the same mistake does not occur twice
- winning patterns are identified and repeated deliberately

This is the system that turns operational history into institutional moat.

---

# GOVERNING PRINCIPLES

1. Every significant operational event has a lesson potential
2. Lessons are worthless without founder approval
3. Approved lessons are permanent infrastructure — not notes
4. AI learns from approved lessons only — never from sandbox or unapproved records
5. Lessons compound — their value increases as the system matures
6. Contradictory lessons require explicit founder resolution
7. Lesson quality matters more than lesson volume

---

# LESSON LIFECYCLE

```
OPERATIONAL EVENT
        ↓
LESSON CANDIDATE CREATED
(AI or human)
        ↓
STRUCTURED + CATEGORIZED
        ↓
PENDING WILL REVIEW
        ↓
    [WILL REVIEWS]
       /     \
  APPROVED   DENIED
      ↓           ↓
  ACTIVE      ARCHIVED
      ↓
AI CONTEXT INJECTION
      ↓
OUTCOME TRACKING
      ↓
  APPLIED / TESTED
      ↓
PERIODIC REVALIDATION
```

---

# LESSON CAPTURE SOURCES

| SOURCE | MECHANISM | PRIORITY |
|--------|-----------|----------|
| Founder direct input | Manual creation via interface | Highest |
| Escalation resolution | Auto-generated at escalation close | High |
| Booking outcome | AI-generated post-charter | High |
| Approval Queue denial | Auto-generated on Will denial | High |
| Automation failure | Auto-generated on failure detection | Medium |
| Response quality review | Weekly AI audit surfacing | Medium |
| SOP deviation | Auto-generated when SOP gap detected | Medium |
| Vendor incident | Auto-generated at incident log | Medium |
| AI confidence anomaly | Surfaced when confidence drops below threshold | Low |

---

# LESSON DATA MODEL

## Identity Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Lesson UUID | UUID | YES | Immutable — auto-generated — never reassigned |
| Lesson ID | Formula | YES | Human-readable: LES-[YYYY]-[SEQ] |
| Created At | DateTime | YES | Immutable on creation |
| Updated At | DateTime | YES | Auto-updated on modification |
| Created By | Single Select | YES | FOUNDER / AI / LUCIANA / SYSTEM |
| Environment | Single Select | YES | Production / Sandbox / Development |
| Brand | Single Select | YES | SSS / MARE / BOTH |
| City | Single Select | NO | Miami / Fort Lauderdale / All / Future markets |

## Classification Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Lesson Title | Single Line | YES | Clear, searchable summary |
| Category | Single Select | YES | See Category Taxonomy below |
| Subcategory | Single Select | NO | Finer classification within category |
| Severity | Single Select | YES | Critical / High / Medium / Low |
| Status | Single Select | YES | See Status Lifecycle below |
| Repeatable | Checkbox | YES | True = pattern likely to recur |
| Source Event Type | Single Select | YES | What triggered the lesson |
| Source Record ID | Single Line | NO | Linked booking / request / audit UUID |

## Content Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Situation | Long Text | YES | Context: what was happening |
| Problem | Long Text | YES | What went wrong or what was notable |
| What Happened | Long Text | YES | Factual account of the event |
| What Was Changed | Long Text | NO | Actions taken in response |
| Root Cause | Long Text | NO | Why it happened |
| Outcome Before | Single Select | YES | State before lesson was applied |
| Outcome After | Single Select | NO | State after lesson was applied |
| Why It Worked | Long Text | NO | Success mechanisms |
| Why It Failed | Long Text | NO | Failure mechanisms |
| Suggested Future Action | Long Text | YES | What AI / ops should do differently |
| Emotional Signal | Single Select | NO | Client emotional state if relevant |

## Intelligence Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| AI Prompt Tag | Single Line | YES | Tag for AI context injection matching |
| AI Insight | Long Text | NO | AI-generated analysis of the lesson |
| Founder Insight | Long Text | NO | Will's personal annotation |
| Decision Note | Long Text | NO | Will's direct operational instruction |
| Confidence Weight | Number | YES | 1–10 AI weighting score |
| Application Count | Number | YES | Times this lesson has influenced AI output |
| Last Applied At | DateTime | NO | Most recent AI application |
| Contradicts Lesson ID | Single Line | NO | UUID of any contradictory lesson |

## Approval Fields

| FIELD | TYPE | REQUIRED | NOTES |
|-------|------|----------|-------|
| Will Approved | Checkbox | YES | Only Will can check this |
| Reviewed At | DateTime | NO | When Will reviewed |
| Approval Notes | Long Text | NO | Will's approval context |

---

# CATEGORY TAXONOMY

| CATEGORY | SUBCATEGORIES |
|----------|---------------|
| Sales | Lead Qualification · Proposal Timing · Pricing Response · Objection Handling · Close Rate |
| Hospitality | Client Experience · VIP Handling · Service Recovery · Expectation Management |
| Operations | Charter Execution · Vendor Coordination · City Management · Pre-Departure |
| Broker | Coordination · Communication · Commission · Relationship Management |
| Creator | Content Strategy · Hook Performance · Platform Behavior |
| Advertising | Ad Performance · Budget Allocation · Audience Behavior · Fatigue Detection |
| Pricing | Package Design · Margin Defense · Discount Patterns · Upsell Timing |
| Client Behavior | Decision Patterns · Emotional Signals · Repeat Booking · Referral Triggers |
| Relationship | HV Management · Planner Relationships · Affiliate Behavior |
| Expansion | City Launch · Vendor Bench · Market Entry |
| AI System | Confidence Anomaly · Response Quality · Drift Detection · Autonomy Boundary |
| Financial | Revenue Patterns · Expense Behavior · Refund Risk · Margin Erosion |
| Brand | Voice Drift · Positioning Risk · Perception Management |
| Vendor | Performance Patterns · Insurance · Reliability · Backup Coverage |

---

# STATUS LIFECYCLE

| STATUS | MEANING | TRANSITION RULES |
|--------|---------|-----------------|
| Pending Review | Created — awaiting Will approval | Auto-assigned on creation |
| Active | Will-approved — injected into AI context | Will approval only |
| Applied | Lesson has measurably influenced an outcome | System-updated when outcome tracked |
| Tested | Applied in multiple contexts with consistent results | Ops Lead review + Will confirmation |
| Archived | No longer active — retained permanently | Will only — never deleted |

AI uses Active, Applied, and Tested lessons only.

Pending Review and Archived lessons are excluded from AI context.

---

# AI CONTEXT INJECTION PROTOCOL

When Claude processes any operational event, the following sequence executes:

1. **Identify event category** from current context
2. **Query Active + Applied + Tested lessons** matching that category
3. **Filter by Brand** — SSS lessons isolated from MARE unless explicitly shared
4. **Filter by City** — city-specific lessons weighted higher for same-city events
5. **Match AI Prompt Tags** — exact tag matching prioritized
6. **Apply severity weighting**:
   - Critical = 3x weight
   - High = 2x weight
   - Medium = 1x weight
   - Low = 0.5x weight
7. **Apply Decision Notes first** — founder instructions override all other context
8. **Apply recency weighting** — lessons from last 90 days weighted 1.5x
9. **Check for contradictions** — flag any contradictory lessons to surface in response
10. **Generate output** with lesson context embedded

---

# AI WEIGHTING RULES

| SIGNAL | AI RESPONSE |
|--------|-------------|
| Approved + Repeatable + Outcome Improved | Prioritize strongly |
| Outcome Worsened | Treat as hard constraint — avoid similar action |
| Decision Note present | Highest priority — treat as direct founder instruction |
| Will denied similar approval | Treat as explicit boundary |
| Critical severity | Triple weight — always surface to founder |
| Contradictory lessons present | Surface contradiction — do not resolve autonomously |
| Lesson not yet Applied | Weight at 0.75x — not yet operationally proven |
| Lesson Applied 5+ times consistently | Candidate for autonomy threshold review |

---

# LESSON GENERATION TRIGGERS

## Automatic Generation

The system auto-generates a lesson candidate when:

| TRIGGER | CATEGORY | SEVERITY |
|---------|----------|----------|
| L3 or L4 escalation resolved | Operations | High or Critical |
| Approval Queue item denied by Will | Varies | Matches denial severity |
| Charter Grade = D or F | Operations / Hospitality | High |
| Automation failure logged | AI System | High |
| AI confidence score < 60% on sent message | AI System | Medium |
| Vendor rating < 3 | Vendor | High |
| Refund approved | Financial / Hospitality | High |
| SOP deviation detected | Operations | Medium |
| Client dissatisfaction signal received | Hospitality | High |
| Response time > 4 hours on hot lead | Sales | Medium |

## Manual Creation

Will or Luciana may create a lesson at any time.

Manually created lessons enter Pending Review and require Will approval before entering AI context — including lessons created by Will directly.

---

# LESSON QUALITY STANDARDS

Every lesson submitted for founder review must meet:

- Situation: specific, not vague
- Problem: identifies a single clear issue
- Suggested Future Action: actionable instruction, not a description
- AI Prompt Tag: specific enough to match relevant future events
- Category: correctly classified

Lessons failing quality standards are returned to Pending Review with a quality note.

---

# CONTRADICTION RESOLUTION PROTOCOL

When two Active lessons contradict each other:

1. System flags both with Contradicts Lesson ID populated
2. AI does not autonomously resolve the contradiction
3. Contradiction surfaced in next Founder Digest
4. Will reviews and either:
   - Archives one lesson
   - Modifies one lesson
   - Creates a new reconciling lesson
5. Resolution logged with Decision Note

AI never applies contradictory lessons without Will resolution.

---

# BRAND CONTEXT ISOLATION

Lessons are brand-isolated by default.

| RULE | DETAIL |
|------|--------|
| SSS lessons | Do not automatically apply to MARE contexts |
| MARE lessons | Do not automatically apply to SSS contexts |
| Shared lessons | Require Brand = BOTH — only Will can set this |
| Bachelorette intelligence | Isolated from corporate intelligence even within SSS |
| Financial lessons | Isolated by entity |
| City lessons | Isolated by market — Miami lessons do not auto-apply to Fort Lauderdale |

Cross-contamination is a system integrity failure.

---

# LESSONS DIGEST — WEEKLY AUTOMATION

Every Thursday at 5:00 PM:

Make generates a Lessons Digest containing:

- New lessons awaiting Will review
- Lessons applied in the past 7 days and their outcomes
- Lessons applied 5+ times — autonomy threshold candidates
- Contradictions requiring resolution
- High-severity lessons from the past 30 days
- Lessons not applied in 90+ days — archival candidates
- AI-generated observation: "This week's pattern suggests..."

Delivered to: Will + Luciana

---

# GOVERNANCE RULES

1. No lesson record may be deleted — archive only
2. Lesson UUIDs are immutable
3. AI may not promote its own lessons to Active status
4. AI may not archive lessons
5. AI may not modify Decision Notes
6. Sandbox lessons are permanently excluded from AI context
7. All lesson modifications generate an audit log entry
8. Contradictions must be resolved by Will before either lesson reaches full weight
9. Lessons are permanent operational infrastructure — not temporary notes

---

# QUARTERLY GOVERNANCE REVIEW

Every quarter, Will reviews:

- Stale lessons (not applied in 90+ days) — archive or reaffirm
- Contradictory lesson clusters — resolve or consolidate
- AI weighting accuracy — are weighted lessons actually producing better outcomes?
- Category coverage gaps — are there operational areas with no lessons?
- Autonomy threshold candidates from Tested lessons
- Total active lesson count by category

Review is logged in Governance_Reviews table.

---

# DATA RETENTION

| DATA TYPE | RETENTION |
|-----------|-----------|
| Active lessons | Permanent |
| Archived lessons | Permanent |
| Pending Review lessons | Permanent |
| Lesson audit trail | Permanent |
| Sandbox lessons | Quarterly purge — never enter AI context |

Deletion is prohibited. Archive only.

---

# SUCCESS CONDITION

The Lessons Engine is functioning correctly when:

- AI behavior measurably improves over 90-day periods
- The same operational failure does not recur twice without a lesson
- Will reviews lessons in under 5 minutes weekly
- Every L3+ escalation produces at least one lesson
- Autonomy threshold candidates emerge naturally from Tested lesson patterns
- The system compounds institutional intelligence without founder overhead

---

SHE SAID SAIL + MARE EXECUTIVE · LESSONS ENGINE SPECIFICATION
CONFIDENTIAL · INTERNAL USE ONLY
