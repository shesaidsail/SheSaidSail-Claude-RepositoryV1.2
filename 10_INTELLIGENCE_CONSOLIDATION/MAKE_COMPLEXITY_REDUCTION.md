# MAKE COMPLEXITY REDUCTION
## She Said Sail + Mare Executive — Automation Spaghetti Prevention

**Document ID:** MAKE_COMPLEXITY_REDUCTION
**Status:** CONSOLIDATION AUTHORITY
**Version:** 1.0
**Date:** 2026-05-15
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## SECTION 1 — THE PROBLEM

The proposed intelligence layer architecture, if implemented as written across all three branch documents, would produce:

- 20+ existing Make scenarios (per Systems_Intelligence_Architecture)
- 9 new creative scenarios (per CREATIVE_INTELLIGENCE_ARCHITECTURE)
- ~8 new revenue intelligence scenarios (per REVENUE_INTELLIGENCE_ARCHITECTURE)
- ~5 new executive intelligence scenarios (per EXECUTIVE_INTELLIGENCE_ROADMAP)

**Potential total: 40+ individual Make scenarios.**

At 40+ scenarios, the operational reality becomes:
- A change to one scenario requires auditing 39 others for circular dependencies
- Debugging a Make failure requires tracing chains across scenarios that call each other
- New team members cannot operate the automation layer without weeks of onboarding
- Scenario sprawl is not a linear risk — it compounds exponentially

This document defines the compression strategy.

---

## SECTION 2 — ANTI-SPAGHETTI RULES (PERMANENT)

These rules are permanent governance. No Make scenario may be built that violates them.

### Rule 1: One Trigger Source Per Domain

Each functional domain has exactly ONE primary trigger mechanism. Scenarios within a domain are modules of the master orchestrator for that domain, not independent scenarios with their own triggers.

| Domain | Trigger Authority |
|--------|-----------------|
| Inbound leads | Webflow form webhook → INBOUND-MASTER |
| Booking lifecycle | Airtable Booking status field change → BOOKING-MASTER |
| Charter sequence | Scheduled time trigger → CHARTER-MASTER |
| Financial events | Stripe webhook + Sunday schedule → FINANCIAL-MASTER |
| Intelligence + digests | Thursday 5pm schedule + monthly schedule → INTELLIGENCE-MASTER |
| Creative intelligence | Asset status change + Monday schedule → CREATIVE-MASTER |
| Outreach | Airtable Partner Outreach status + schedule → OUTREACH-MASTER |
| Emergency | Emergency_Flag change → EMERGENCY-001 (standalone — never nested) |
| Audit | Called by orchestrators as a sub-routine — never standalone trigger |
| Health | 15-minute schedule → HEALTH-001 (standalone) |
| Backup | Daily 2am schedule → BACKUP-001 (standalone) |

### Rule 2: No Scenario Calls Another Scenario

Scenarios communicate through Airtable records only.

- Scenario A writes a value to an Airtable field
- Scenario B reads that field on its own trigger cycle
- Scenario A never sends a webhook to Scenario B directly

This prevents cascading failures where one scenario's error propagates through the entire chain.

### Rule 3: No Circular Chains

Make scenario writes to Airtable → Airtable native automation must not re-trigger that Make scenario.

Required: Before any Make scenario writes to Bookings, Requests, or any table with Airtable-native automations, the native automation inventory (Phase 0 of Build Spec) must be confirmed and all native automations scoped to specific field changes that Make does NOT write to.

### Rule 4: Automations_Paused Is Checked First

Every scenario that sends any outbound message (SMS, email, Slack to clients) checks:
1. `Emergency_Flag` on the relevant Booking = false
2. `Automations_Paused` on the relevant Booking = false
3. `Environment` on the relevant Booking = Production

If any of these conditions fail, the scenario logs a record to Automation_Health and exits. It does not retry. It does not send.

### Rule 5: AUDIT-001 Is a Sub-Routine, Not a Trigger

AUDIT-001 is called as a module within orchestrators. It is never activated by a standalone Airtable trigger. Every Tier A action within an orchestrator calls the AUDIT-001 module before the action is considered complete. If AUDIT-001 fails, the orchestrator logs the failure to Automation_Health and creates a Founder Decision alert.

### Rule 6: Error Handling Is Standardized

Every orchestrator uses the same error handling pattern:

```
Attempt action
→ Success: continue, log to Audit_Log via AUDIT-001
→ Failure 1: log to Automation_Health, retry after 2 minutes
→ Failure 2: retry after 5 minutes
→ Failure 3: alert Luciana via Slack (#sss-ops-alerts)
→ Failure 4: alert Will directly, pause scenario, create Founder Decision: SEV-2
→ Persistent (30+ min): SEV-1 — Will initiates manual recovery
```

All orchestrators inherit this pattern. No orchestrator deviates from it.

### Rule 7: Idempotency Keys on All Client-Facing Actions

Every outbound client message is protected by an idempotency key:
- Key = hash of Booking_ID + Scenario_ID + Message_Type
- Key stored on Automation_Health record linked to Booking
- On retry: check key before sending — if key exists, skip send, log skip

No client receives duplicate messages from retry logic.

---

## SECTION 3 — CONSOLIDATED SCENARIO CATALOG

### 3.1 Final 11-Scenario Architecture

| # | Scenario ID | Type | Trigger | Core Functions |
|---|------------|------|---------|---------------|
| 1 | **INBOUND-MASTER** | Orchestrator | Webflow form webhook + DM source | Lead capture → Airtable Request record → Auto-reply → Brand routing → Claude response draft → Luciana notification |
| 2 | **BOOKING-MASTER** | Orchestrator | Airtable: Booking status field change | Stripe payment link generation → Deposit tracking → Agreement gate → Confirmation email → Booking record updates |
| 3 | **CHARTER-MASTER** | Orchestrator | Scheduled: T-72h, T-48h, T-24h, T-12h, D+1, D+7, D+30 | Charter brief delivery → Client communication sequence → Balance reminder → D7 review eligibility check → Review request → D30 referral |
| 4 | **FINANCIAL-MASTER** | Orchestrator | Stripe webhooks + Sunday 9pm schedule | Payout receipt → P&L sync to Financial base → Expense anomaly detection → Weekly P&L summary → Payout alert generation |
| 5 | **INTELLIGENCE-MASTER** | Orchestrator | Thursday 5pm + 1st of month extended run | Thursday Digest assembly → Lessons review → AI quality summary → Revenue health section → Creative performance section → Pending approvals → System health summary |
| 6 | **CREATIVE-MASTER** | Orchestrator | Creative_Assets: Status = REVIEW_PENDING + Monday 8am | Claude API asset classification → Score computation → Winner flagging → Founder Decision creation for eligible winners → Monthly creative summary |
| 7 | **OUTREACH-MASTER** | Orchestrator | Airtable: Partner_Outreach Stage change + schedule | Outreach draft generation → Luciana review routing → Follow-up sequence management |
| 8 | **EMERGENCY-001** | Standalone | Emergency_Flag = true (ANY Booking) | Pause all booking automations → Will Slack DM → #sss-emergency-ops alert → Emergency_Escalations record → Founder Decision: EMERGENCY |
| 9 | **AUDIT-001** | Sub-routine | Called by orchestrators (never standalone) | Write immutable Audit_Log record → Validate write success → Alert on failure |
| 10 | **HEALTH-001** | Standalone | Every 15 minutes | Automation failure count check → Audit_Log gap detection → Stripe webhook latency check → Backup age check → Alert on threshold breach |
| 11 | **BACKUP-001** | Standalone | Daily 2am | Full Airtable base CSV export → Store to designated secure location → Log to Governance_Reviews |

### 3.2 Scenario Dependency Map

```
INBOUND-MASTER
    → writes to: Requests, Conversations, Audit_Log (via AUDIT-001)
    → reads from: Clients, Lessons (AI context), AI_Prompt_Versions

BOOKING-MASTER
    → writes to: Bookings, P&L Per Charter (status = COMPLETED), Automation_Health
    → reads from: Clients, Packages, Yachts, Stripe (webhook), Audit_Log (idempotency check)
    → calls: AUDIT-001

CHARTER-MASTER
    → writes to: Automation_Health (send states), Audit_Log (via AUDIT-001)
    → reads from: Bookings, Clients, Cities, Yachts, Brokers
    → calls: AUDIT-001
    → checks: Emergency_Flag, Automations_Paused FIRST

FINANCIAL-MASTER
    → writes to: P&L Per Charter, Financial_Periods, Payouts, Audit_Log, Approval Queue (anomalies)
    → reads from: Bookings, Stripe (webhook), Expenses, Contractors
    → calls: AUDIT-001

INTELLIGENCE-MASTER
    → writes to: (no Airtable writes — reads and generates Slack digest only)
    → reads from: Revenue_Snapshots, Lessons, Audit_Log, Creative_Assets, Approval Queue, Automation_Health
    → sends to: Slack (Will + Luciana)

CREATIVE-MASTER
    → writes to: Creative_Assets (AI tags + scores), Approval Queue (winner candidates)
    → reads from: Creative_Assets, Organic_Content, Paid_Ads, AI_Prompt_Versions
    → calls: AUDIT-001, Claude API

OUTREACH-MASTER
    → writes to: Partner_Outreach, Audit_Log (via AUDIT-001)
    → reads from: Partner_Outreach, Affiliates, Lessons (context)
    → calls: AUDIT-001

EMERGENCY-001
    → writes to: Emergency_Escalations, Approval Queue, Bookings (Automations_Paused = true)
    → reads from: Bookings (Emergency_Flag trigger)
    → sends to: Slack DM (Will), #sss-emergency-ops
    → NEVER calls another scenario

AUDIT-001 (sub-routine)
    → writes to: Audit_Log
    → reads from: Nothing — called with structured payload
    → called by: INBOUND-MASTER, BOOKING-MASTER, CHARTER-MASTER, FINANCIAL-MASTER, CREATIVE-MASTER, OUTREACH-MASTER

HEALTH-001
    → reads from: Automation_Health, Audit_Log, BACKUP-001 last run timestamp
    → writes to: Automation_Health (alert flags)
    → sends to: Slack (Luciana if SEV-3, Will if SEV-2+)
    → NEVER calls another scenario

BACKUP-001
    → reads from: All Airtable tables
    → writes to: External CSV storage
    → logs to: Governance_Reviews
    → NEVER calls another scenario
```

---

## SECTION 4 — SCENARIOS THAT ARE NOT STANDALONE

The following proposed scenarios from the intelligence layer documents are NOT standalone scenarios. They are modules within the orchestrators above.

| Proposed Scenario | Absorbed Into | How |
|------------------|--------------|-----|
| CREATIVE-001 (asset tagging) | CREATIVE-MASTER | Triggered by status change within CREATIVE-MASTER |
| CREATIVE-002 (campaign create) | BOOKING-MASTER | Campaign record creation happens on booking confirmation |
| CREATIVE-003 (weekly performance sync) | CREATIVE-MASTER / Monday module | One Monday trigger pulls platform data |
| CREATIVE-004 (threshold breach) | CREATIVE-MASTER / Monday module | Post-sync check within same execution |
| CREATIVE-005 (winner flagging) | CREATIVE-MASTER / Monday module | Post-scoring check within same execution |
| CREATIVE-006 (fatigue detection) | CREATIVE-MASTER / Thursday module | Embedded in INTELLIGENCE-MASTER Thursday run |
| CREATIVE-007 (fatigue alert) | CREATIVE-MASTER | Alert generation within orchestrator |
| CREATIVE-008 (brief generation) | CREATIVE-MASTER | Winner brief generation on Founder Decision approval |
| CREATIVE-009 (monthly report) | INTELLIGENCE-MASTER | Creative section in Thursday Digest (1st of month = extended) |
| Revenue Intelligence weekly | INTELLIGENCE-MASTER | Revenue section in Thursday Digest |
| Revenue Intelligence Monday report | ELIMINATED | Moved to Thursday Digest |
| Lessons Digest Thursday | INTELLIGENCE-MASTER | Lessons section in Thursday Digest |
| AI Governance weekly report | INTELLIGENCE-MASTER | AI quality section in Thursday Digest |
| Demand Score computation | FINANCIAL-MASTER | Weekly demand computation within financial orchestrator |
| LTV Score update | FINANCIAL-MASTER | Weekly client score update within financial orchestrator |

---

## SECTION 5 — MAKE COMPLEXITY RISK ASSESSMENT

### 5.1 Complexity Risk Indicators to Monitor

The orchestrator architecture is clean. The following conditions indicate emerging spaghetti risk and require immediate architecture review:

| Indicator | Threshold | Response |
|-----------|----------|---------|
| Total active Make scenarios | >15 | Review for consolidation opportunity |
| Scenarios that trigger other scenarios | >0 | Immediate refactoring |
| Scenarios without documented dependency map | Any | Build not permitted |
| Scenarios without error handling | Any | Not permitted in production |
| Average scenario module count | >20 modules | Split into sub-scenarios with Airtable as communication layer |
| Circular dependency instances | Any | SEV-1 — immediate remediation |
| Scenarios touching Bookings without idempotency check | Any | Not permitted |

### 5.2 Phase 4 Scenario Build Checklist

Before any new scenario is built:

- [ ] Dependency map documented: inputs, reads, writes, outputs, downstream effects
- [ ] Circular dependency check against all existing scenarios confirmed clear
- [ ] Idempotency protection designed for all client-facing messages
- [ ] Error handling pattern implemented (matching Rule 6 above)
- [ ] Automations_Paused and Emergency_Flag check as step 1 for all client-facing actions
- [ ] AUDIT-001 call included for every Tier A action
- [ ] Sandbox validation complete before production deployment
- [ ] Founder Decision: SYSTEM logged before production activation
- [ ] Rollback procedure documented

---

## SECTION 6 — PHASE 4 ORCHESTRATOR BUILD SEQUENCE

| Step | Orchestrator | Prerequisites |
|------|-------------|--------------|
| 4.1 | FINANCIAL-MASTER | Phase 3 complete, Financial_Periods table built |
| 4.2 | INTELLIGENCE-MASTER (basic — Thursday Digest) | Phase 3 complete, Lessons table optimized |
| 4.3 | CREATIVE-MASTER | Creative_Assets table built (Phase 4 table step 4.6) |
| 4.4 | INTELLIGENCE-MASTER (enhanced — all sections) | Revenue_Snapshots table built |
| 4.5 | OUTREACH-MASTER | Partner Outreach reduced to 45 fields |

Note: INBOUND-MASTER, BOOKING-MASTER, CHARTER-MASTER, EMERGENCY-001, AUDIT-001, HEALTH-001, BACKUP-001 are Phase 2/3 builds or already exist. They are enhanced during Phase 4 but not rebuilt.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_COMPLEXITY_REDUCTION v1.0*
*Effective May 2026*
