# SHE SAID SAIL + MARE EXECUTIVE
MIAMI · FORT LAUDERDALE

# RISK INTELLIGENCE SPECIFICATION
Operational Risk Detection · Early Failure Identification · Escalation Architecture · Risk Compounding Prevention

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

The Risk Intelligence system exists to identify operational risk before it becomes operational damage.

Premium hospitality businesses fail silently. A vendor relationship degrades before an incident. A booking pattern signals a refund before the client complains. An AI response crosses a brand boundary before anyone notices. A financial metric drifts before it becomes a loss.

This system:
- continuously scans operational data for risk signals
- classifies and escalates risk to the appropriate authority
- tracks risk resolution
- learns from past risk patterns
- prevents the same risk from recurring without detection

---

# GOVERNING PRINCIPLES

1. Risk detection is proactive — not reactive
2. Every risk has a severity and an owner
3. AI identifies risks — humans resolve them
4. Risk patterns are as important as individual risk events
5. Financial risks receive highest priority
6. Brand risks are silent and compound — they require dedicated detection
7. The same risk recurring twice without a lesson is a system failure

---

# RISK CLASSIFICATION ARCHITECTURE

## Risk Domains

| DOMAIN | DESCRIPTION |
|--------|-------------|
| Operational | Charter execution, vendor performance, city management gaps |
| Financial | Margin erosion, refund exposure, expense anomaly, revenue pattern shifts |
| Brand | Voice drift, client perception, vendor confidentiality, public exposure |
| Client | Dissatisfaction signals, HV client risk, chargeback likelihood, retention risk |
| AI System | Confidence degradation, drift detection, autonomy boundary proximity |
| Vendor | Insurance lapse, performance decline, backup coverage gaps |
| Legal / Compliance | Chargeback signals, dispute indicators, regulatory exposure |
| Expansion | City health, scaling risk, new market instability |

## Severity Levels

| LEVEL | LABEL | DEFINITION | RESPONSE SLA |
|-------|-------|------------|--------------|
| SEV-1 | CRITICAL | Financial or operational integrity at risk — potential loss, legal exposure, or brand damage | Immediate — Will notified within 5 minutes |
| SEV-2 | HIGH | Automation failure, client escalation, vendor incident, significant pattern anomaly | Will notified within 30 minutes |
| SEV-3 | MEDIUM | Reporting inconsistency, minor SOP gap, emerging pattern, non-urgent anomaly | Founder Digest within 24 hours |
| SEV-4 | LOW | Monitoring note, weak signal, informational flag | Weekly digest |

---

# RISK SIGNAL LIBRARY

## Operational Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| Charter Grade = D or F | Booking record field | SEV-2 |
| Emergency_Flag = true | Booking field trigger | SEV-1 |
| City Manager response gap > 2 hours during active charter | Timestamp comparison | SEV-1 |
| Vendor not confirmed 48h before charter | Pre-departure check | SEV-2 |
| Backup vendor bench < 2 per category in any city | Vendor table scan | SEV-3 |
| Charter Brief not generated 72h before charter | Automation health check | SEV-2 |
| Active booking count exceeds city capacity baseline | Booking density scan | SEV-2 |
| SOP deviation logged without resolution | Deviation record age scan | SEV-3 |

## Financial Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| Booking margin < 20% | Formula field trigger | SEV-1 |
| Refund marked without Founder Decision | Financial integrity check | SEV-1 |
| Package price modified post-confirmation | Field modification audit | SEV-1 |
| Expense created and paid in same session | Fraud pattern detection | SEV-1 |
| Ad spend approaching monthly cap | Running total comparison | SEV-2 |
| Revenue 20%+ below prior 30-day average | Period comparison | SEV-2 |
| Contractor payout modified post-initiation | Audit log pattern | SEV-1 |
| 3+ refund requests in 30 days | Request pattern scan | SEV-2 |

## Brand Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| AI response tone flagged in audit | Weekly audit sample | SEV-2 |
| Outbound message contains unapproved pricing language | Content scan | SEV-1 |
| AI hallucination detected in sent message | Audit log review | SEV-2 |
| Vendor shares client content without authorization | Incident report trigger | SEV-1 |
| 1-2 star review received without Will notification | Review monitoring | SEV-2 |
| Public social post detected without Will approval | Platform monitoring | SEV-1 |

## Client Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| HV client dissatisfaction signal received | Sentiment classification | SEV-1 |
| Chargeback_Risk = HIGH or ACTIVE | Booking field | SEV-1 |
| Client complaint unresolved for 4+ hours | Timestamp + status scan | SEV-2 |
| Hot lead with no response in 2+ hours | Request status + time | SEV-2 |
| Repeat client booking gap > 18 months | Booking history scan | SEV-4 |
| VIP client without HV flag | Client tier classification | SEV-3 |

## AI System Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| AI confidence score < 60% on active inquiry | Confidence field monitor | SEV-2 |
| AI recommendation denied 3+ consecutive times | Approval Queue pattern | SEV-3 |
| Autonomy boundary proximity without escalation | Authority tier check | SEV-2 |
| Prompt version mismatch detected | Prompt version audit | SEV-2 |
| AI output contradicts active lesson | Context comparison | SEV-2 |
| Audit log gap detected | Log continuity check | SEV-1 |

## Vendor Risks

| SIGNAL | DETECTION METHOD | SEVERITY |
|--------|-----------------|----------|
| Vendor insurance expiring within 14 days | Insurance date scan | SEV-2 |
| Vendor insurance lapsed | Insurance date scan | SEV-1 |
| Vendor rating drops below 3 in last 2 charters | Rolling average calculation | SEV-2 |
| Single vendor rating below 2 | Rating field | SEV-1 |
| No backup vendor available for confirmed charter | Vendor coverage check | SEV-1 |

---

# RISK RECORD DATA MODEL

## Identity Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Risk UUID | UUID | YES |
| Risk ID | Formula | YES — RISK-[YYYY]-[SEQ] |
| Created At | DateTime | YES — Immutable |
| Updated At | DateTime | YES |
| Environment | Single Select | YES |
| Brand | Single Select | YES |
| City | Single Select | NO |

## Classification Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Risk Domain | Single Select | YES |
| Risk Type | Single Select | YES |
| Severity | Single Select | YES — SEV-1 through SEV-4 |
| Status | Single Select | YES |
| Source System | Single Select | YES |
| Source Record ID | Single Line | YES — linked record UUID |
| Detection Method | Single Select | YES |

## Content Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Risk Summary | Long Text | YES — what was detected |
| Evidence | Long Text | YES — specific data supporting the risk |
| Potential Impact | Long Text | YES — what happens if unaddressed |
| Recommended Action | Long Text | YES — AI recommended response |
| Escalation Target | Single Select | YES — WILL / LUCIANA / CITY_MANAGER / AUTO |
| Escalated At | DateTime | NO |

## Resolution Fields

| FIELD | TYPE | REQUIRED |
|-------|------|----------|
| Resolved By | Single Select | NO |
| Resolution Type | Single Select | NO |
| Resolution Notes | Long Text | NO |
| Resolved At | DateTime | NO |
| Lesson Generated | Checkbox | NO |
| Lesson UUID | Single Line | NO |
| Recurrence Prevention | Long Text | NO |

---

# RISK STATUS LIFECYCLE

| STATUS | MEANING |
|--------|---------|
| Detected | Risk identified — pending escalation |
| Escalated | Appropriate party notified |
| In Progress | Owner actively addressing |
| Resolved | Risk addressed — outcome documented |
| False Positive | Risk signal did not represent actual risk |
| Recurring | Same risk detected for 2nd+ time |
| Archived | Permanent record — no active status |

---

# ESCALATION ROUTING MATRIX

| SEVERITY | RISK DOMAIN | PRIMARY ESCALATION | SECONDARY |
|----------|-------------|-------------------|-----------|
| SEV-1 | Any | Will — immediate — Slack DM + SMS | Luciana if Will unreachable |
| SEV-2 | Financial | Will within 30 minutes | Luciana immediately |
| SEV-2 | Operational | Luciana immediately | Will if L3+ |
| SEV-2 | Brand | Will within 30 minutes | Luciana aware |
| SEV-2 | Client | Luciana immediately | Will if HV |
| SEV-2 | AI System | Luciana + Will notified | Prompt review triggered |
| SEV-3 | Any | Founder Digest — next day | Luciana review |
| SEV-4 | Any | Weekly digest | No immediate action |

SEV-1 risks pause relevant automations automatically pending Will review.

HV client risks always route to Will regardless of severity classification.

---

# RISK PATTERN DETECTION

Beyond individual risk events, the system monitors for patterns:

## Pattern Types

| PATTERN | DETECTION LOGIC | SEVERITY UPGRADE |
|---------|----------------|-----------------|
| Same risk type 3x in 30 days | Frequency scan by risk type | Upgrade 1 severity level |
| Same city 2 SEV-2s in 7 days | Geographic clustering | Trigger city health review |
| Same vendor 2 incidents in 60 days | Vendor record linkage | Vendor suspension recommendation |
| AI risk 3x in 14 days | AI domain clustering | Prompt review trigger |
| Financial risk in 2+ consecutive weeks | Week-over-week comparison | Will direct briefing |

## Pattern Records

When a risk pattern is detected:

1. Pattern Risk Record created with all constituent risks linked
2. Pattern severity = highest individual severity + 1 level
3. Pattern summary includes timeline and progression
4. Proposal generated: SOP improvement or AI correction
5. Routes to Founder Command Center as priority item

---

# RISK INTELLIGENCE REPORTING

## Founder Risk Brief

Included in every Thursday Digest:

- SEV-1 and SEV-2 risks from past 7 days
- Unresolved risks older than 48 hours
- Risk patterns detected this period
- Risks by domain — volume and trend
- Top recurring risk types
- AI-generated risk narrative: "This week's operational risk profile..."

## Monthly Risk Review

Every first Monday of the month:

- All risks from prior month by domain and severity
- Resolution rate and time-to-resolution
- Risk pattern trends — improving or degrading?
- False positive rate — is detection well-calibrated?
- Risks converted to lessons
- Risks that recurred — lesson failure indicators

---

# RISK-TO-LESSON PIPELINE

Every resolved SEV-1 or SEV-2 risk automatically generates a lesson candidate.

The lesson is pre-populated with:
- Situation = Risk Evidence
- Problem = Risk Summary
- Category = Risk Domain
- Severity = matching risk severity
- Suggested Future Action = Risk Recommended Action

The lesson enters Pending Review for Will to evaluate.

This closes the loop between risk detection and operational learning.

---

# EARLY WARNING SYSTEM

The system maintains a set of leading indicators — signals that precede risk, not just concurrent with it.

| LEADING INDICATOR | PRECEDES | DETECTION WINDOW |
|-------------------|----------|-----------------|
| Hot lead response time trending up | Booking conversion rate decline | 14 days |
| AI confidence trend declining | AI quality failure | 7 days |
| Vendor average rating declining | Vendor incident | 30 days |
| Escalation frequency increasing | Operational instability | 21 days |
| Lesson application rate declining | SOP drift | 30 days |
| Proposal denial rate increasing | AI calibration drift | 14 days |
| Charter Grade average declining | Service quality failure | 30 days |

Leading indicators generate SEV-4 notices that appear in weekly digests — not immediate escalations.

If a leading indicator persists for 2+ weeks without improvement, it upgrades to SEV-3.

---

# GOVERNANCE RULES

1. SEV-1 risks trigger automatic automation pause for affected records
2. No SEV-1 risk may be marked Resolved without Will's explicit input
3. AI may detect and classify risk — it may not resolve it autonomously
4. Risk records are permanent — no deletion
5. False positives must be logged — calibration data
6. Risk escalation routing may not be modified without Will approval
7. HV client risks always route to Will — no exception
8. Financial SEV-1 risks trigger Stripe and Airtable review simultaneously
9. Recurring risks (same risk type 3+ times) always require a lesson

---

# SUCCESS CONDITION

The Risk Intelligence system is functioning correctly when:

- SEV-1 risks reach Will within 5 minutes of detection
- The same risk type does not recur without a lesson existing
- Leading indicators provide 14+ days of warning before operational failure
- Will's risk review takes under 10 minutes in the weekly digest
- Risk-to-lesson pipeline produces active lessons from every SEV-1 resolution
- False positive rate stays below 15% (measured monthly)

---

SHE SAID SAIL + MARE EXECUTIVE · RISK INTELLIGENCE SPECIFICATION
CONFIDENTIAL · INTERNAL USE ONLY
