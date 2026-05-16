# STAGE_1_AUTOMATION_CONFLICT_REPORT.md
## She Said Sail + Mare Executive — Airtable Native Automation Conflict Audit

**Document Status:** FRAMEWORK READY — WILL ACTION REQUIRED TO COMPLETE  
**Audit Date:** 2026-05-16  
**Scope:** All Airtable-native automations touching Stage 1 tables  
**Production Base:** appdZ49WqgjRXxA1R  
**Branch:** claude/stage-1-blocker-resolution-QPy0o  
**Blocker:** B-008 — Circular Trigger Risk on Bookings Status Field

---

## EXECUTIVE SUMMARY

**This report cannot be fully completed by any automated system.** Airtable-native automation configurations are not accessible via the Airtable API. They can only be viewed and audited through the Airtable web interface (Automations tab on each base).

This document provides:
1. The framework Will must use to audit native automations
2. The conflict classification system
3. The safety rules for any automation touching Stage 1 tables
4. The disposition matrix (KEEP / DISABLE / DELETE / REPLACE_IN_MAKE)
5. Placeholder rows Will fills in during the audit

**Will must complete Section 3 (Automation Inventory) before any Make scenario that writes to Bookings is activated in production.**

---

## WHY THIS MATTERS

The Bookings table has 152 fields. Any Airtable native automation using a generic "record updated" trigger — rather than a specific "field changes to" trigger — fires every time Make writes any field to a Booking record. If that automation then sends a Stripe payment link, a Slack message, or triggers a webhook back to Make, the result is:

```
Make writes to Bookings
  → Airtable native automation fires (generic record updated)
    → Automation triggers another Make webhook
      → Make writes to Bookings again
        → Loop begins
```

This is a SEV-1 risk. It can generate duplicate charges, duplicate client messages, and infinite execution chains before manual intervention is possible.

**Resolution:** All generic "record updated" automations on Bookings must be scoped to specific field changes or converted to Make scenarios.

---

## SECTION 1 — AUDIT FRAMEWORK

Will opens `appdZ49WqgjRXxA1R` in Airtable and navigates to **Automations** (left sidebar → Automations icon). For every automation listed:

**Record:**
1. Automation name
2. Enabled/Disabled status
3. Trigger: table, trigger type ("record updated", "field changes to", "record matches conditions when updated", "new record", scheduled)
4. If trigger is "field changes to" — which specific field?
5. Action type: Send email / Send Slack / Create record / Update record / HTTP request / Airtable script
6. Action destination: which table receives the record/update, or which webhook URL receives the HTTP request
7. Does this action call back to Make? (Yes if the action is an HTTP request to a Make webhook URL)
8. Does this action touch Bookings, Requests, Packages, AI_Prompt_Versions, Concierge_Operators, or Notification tables?

---

## SECTION 2 — CONFLICT CLASSIFICATION RULES

| Classification | Definition | Action |
|---------------|-----------|--------|
| **KEEP** | Automation uses a specific field trigger, does not call back to Make, does not conflict with Stage 1 scenarios, and is actively needed for operations | Retain as-is. Document field ID and trigger. |
| **KEEP WITH SCOPE FIX** | Automation uses generic "record updated" trigger on Bookings but performs a safe, non-looping action (internal notification only, no Make callback) | Scope to specific field trigger before Stage 1 go-live. |
| **DISABLE** | Automation is deprecated, redundant with a Make scenario, or uses logic that conflicts with Make | Disable before Stage 1 go-live. Can re-enable later if needed. |
| **DELETE** | Automation is duplicate of a Make scenario, contains stale logic, or was a test/experiment | Delete only after confirming no live operational dependency. |
| **REPLACE_IN_MAKE** | Automation has valid logic but must run through Make for proper auditability, idempotency, and environment isolation | Build equivalent Make scenario, then disable native automation. |

---

## SECTION 3 — AUTOMATION INVENTORY (WILL TO COMPLETE)

**Instructions:** Navigate to Automations tab in appdZ49WqgjRXxA1R. List every automation. Use the classification rules in Section 2.

| # | Name | Status | Table | Trigger Type | Specific Field? | Action Type | Calls Make? | Classification | Notes |
|---|------|--------|-------|-------------|----------------|-------------|-------------|---------------|-------|
| 1 | [WILL FILLS IN] | | | | | | | | |
| 2 | | | | | | | | | |
| 3 | | | | | | | | | |
| 4 | | | | | | | | | |
| 5 | | | | | | | | | |
| 6 | | | | | | | | | |
| 7 | | | | | | | | | |
| 8 | | | | | | | | | |
| 9 | | | | | | | | | |
| 10 | | | | | | | | | |

**Add rows as needed. Every active automation must appear in this table.**

---

## SECTION 4 — KNOWN HIGH-RISK AUTOMATION PATTERNS TO LOOK FOR

During the audit, Will specifically looks for these patterns. Each one is a confirmed circular execution risk:

### Risk Pattern A: Generic "Record Updated" on Bookings → Any Action
```
TRIGGER: Record updated in Bookings (no specific field)
ANY ACTION
```
Risk: Fires on every Make write to any Booking field. Classification: KEEP WITH SCOPE FIX minimum (scope to specific field), or REPLACE_IN_MAKE.

### Risk Pattern B: Status Field Watch → HTTP Request to Make
```
TRIGGER: Bookings.Status changes
ACTION: HTTP request to Make webhook
```
Risk: Circular if Make also writes to Bookings.Status. Classification: REPLACE_IN_MAKE (Move trigger entirely into Make).

### Risk Pattern C: Send Email/SMS Native Automation on Bookings
```
TRIGGER: Any Bookings trigger
ACTION: Send email or send SMS
```
Risk: Does not respect Automations_Paused or Emergency_Flag. Does not create Audit Log. Does not use idempotency. Classification: REPLACE_IN_MAKE (these must run through Make for governance compliance).

### Risk Pattern D: AI Automations on Bookings or Requests
```
TRIGGER: Any trigger on Bookings or Requests
ACTION: "Airtable AI" / "Generate with AI" action
```
Risk: AI actions in native Airtable automations are not governed by the AI_Prompt_Versions version control system. They do not write to the Audit Log. They do not check Will_Approved. Classification: DISABLE or REPLACE_IN_MAKE.

### Risk Pattern E: Automation Calling Another Automation's Target
```
TRIGGER: Any trigger
ACTION: Create record or update record that ANOTHER automation watches
```
Risk: Chain reaction — automation A creates record, automation B watches that table, B fires, B creates another record, etc. Classification: KEEP only if chain is intentional, documented, and non-looping.

---

## SECTION 5 — TABLES TO AUDIT

Automations touching these tables are in scope for Stage 1:

| Table | Table ID | Risk Level | Why |
|-------|----------|-----------|-----|
| Bookings | tbl72omPibBkn2hZL | CRITICAL | 152 fields, all Stage 1 scenarios write here |
| Requests | tblTlSB9CO4dTGodg | HIGH | INBOUND-001 creates records here |
| AI_Prompt_Versions | tbl0FJkA1E6a70cxX | HIGH | Prompt deployment automations may conflict with Make |
| Concierge_Operators | tblX61IB2qjDmac8l | MEDIUM | Assignment automations could loop |
| Packages | tblwDw2hkKW5moSr9 | MEDIUM | Pricing change automations must not fire on Make writes |
| Notifications (if exists) | UNKNOWN | HIGH | Any notification system not through Make is ungoverned |
| Audit Log | tblrMpTfMk8q1eNHp | MEDIUM | Automations watching Audit Log could create log loops |

---

## SECTION 6 — SAFETY RULES AFTER AUDIT

Once the audit is complete, these rules govern all remaining native automations:

**Rule A-1:** No native automation on Bookings may use a generic "record updated" trigger. All must be scoped to specific field changes.

**Rule A-2:** No native automation may send a client-facing email or SMS without checking Automations_Paused and Emergency_Flag. Since native automations cannot check multiple conditions cheaply, all client-facing sends must be in Make.

**Rule A-3:** No native automation may make an HTTP request to a Make webhook URL if Make also writes to the table that triggers the automation.

**Rule A-4:** Any AI-generation native automation on Bookings or Requests must be disabled before Stage 1 go-live. All AI generation flows through Make + Claude API to maintain version control and audit logging.

**Rule A-5:** All active native automations must be documented in this report before Stage 1 production activation. Undocumented automations are treated as unknown risk and must be disabled.

---

## SECTION 7 — EXPECTED SAFE AUTOMATION TYPES

The following native automation types are generally safe to keep as-is (verify during audit):

| Type | Why Safe | Condition |
|------|---------|-----------|
| "New record created" on Audit Log → notification to Will | Audit log additions don't loop | Must not write back to any watched table |
| "Record matches conditions" on Founder Decisions where Urgency = IMMEDIATE → Slack DM | Approval queue trigger | Must not write to Bookings |
| "Scheduled" automation (daily/weekly) → summary generation | Not triggered by Make writes | Must not write to Bookings or Requests |
| "Record created" on Emergency_Escalations → Slack alert | Escalation record creation | Must not change Emergency_Flag or Automations_Paused |

---

## SECTION 8 — WILL ACTION REQUIRED: COMPLETION GATE

**This document becomes a production gate when Section 3 is complete.**

Before Stage 1 production activation, Will must:

1. Complete Section 3 (Automation Inventory) for all tables in Section 5
2. Apply dispositions (KEEP / DISABLE / DELETE / REPLACE_IN_MAKE) to every automation
3. Disable all automations classified DISABLE or REPLACE_IN_MAKE
4. Scope all KEEP WITH SCOPE FIX automations to specific field triggers
5. Sign off on this document by adding a completion declaration below

**Completion Declaration (Will adds when done):**
```
AUDIT COMPLETED BY: Will
DATE: ___________
AUTOMATIONS AUDITED: ___
AUTOMATIONS DISABLED: ___
AUTOMATIONS KEPT (scoped): ___
AUTOMATIONS TO REPLACE IN MAKE: ___
CIRCULAR RISKS CLEARED: YES / NO
STAGE 1 AUTOMATION SAFE: YES / NO — PENDING / CLEARED
```

---

*SHE SAID SAIL + MARE EXECUTIVE*  
*CONFIDENTIAL — INTERNAL USE ONLY*  
*STAGE_1_AUTOMATION_CONFLICT_REPORT.md*  
*Framework authored: 2026-05-16*  
*Authority: 02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION Section 4.8*  
*Blocker: B-008 — Production gate until Will completes Section 3*
