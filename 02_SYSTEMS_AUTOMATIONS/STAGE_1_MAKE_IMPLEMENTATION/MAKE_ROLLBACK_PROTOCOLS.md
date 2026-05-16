# MAKE.COM ROLLBACK PROTOCOLS — STAGE 1
## She Said Sail + Mare Executive — Production Rollback Governance

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Effective Date:** May 2026  
**Owner:** Will (Founder)  
**Applies To:** All 8 Stage 1 Make.com Scenarios  
**Classification:** Confidential — Internal Use Only  
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

## SECTION 1 — ROLLBACK PHILOSOPHY

### 1.1 Measure Twice, Cut Once

A rollback in this system is a planned, structured operation — not a panic response. The goal is to restore a known-good state within 30 minutes of a rollback decision, with zero data loss, zero orphaned Stripe charges, and zero unauthorized client communications. Every step of a rollback is documented in real time as it happens.

**The three commandments of rollback:**

1. **Stop before you reverse.** Before touching Make, Airtable, or Stripe — pause all affected scenarios first. A running scenario during rollback can write records that contradict your rollback state, creating a worse mess than the original failure.

2. **Data integrity before speed.** A 30-minute clean rollback is better than a 5-minute dirty one. Prioritize: Stripe voids first, Airtable record state second, Make scenario deactivation third, human notification last.

3. **Every action leaves an audit trail.** Every rollback step creates an entry in the Audit_Log or Deployment_Log. A rollback without a paper trail is not a rollback — it is an uncontrolled state change.

### 1.2 Rollback Authority

| Action | Authority |
|--------|-----------|
| Pause a scenario in Make | Luciana or Will |
| Disable a Make scenario (full deactivation) | Will only |
| Void a Stripe payment intent | Will only (Stripe dashboard access) |
| Manually update Airtable records during rollback | Luciana (with Will direction) or Will |
| Declare full Stage 1 rollback | Will only |
| Clear a paused scenario after rollback | Will only |

---

## SECTION 2 — INDIVIDUAL SCENARIO ROLLBACK PROCEDURES

### 2.1 M-AUDIT-LOGGER Rollback

**When to roll back:** M-AUDIT-LOGGER producing duplicate log entries; logging wrong scenario names; Audit_Log records missing required fields causing HEALTH-001 false alerts.

**Rollback steps:**
1. Pause M-AUDIT-LOGGER in Make immediately (do not disable — pause preserves execution history)
2. Write a Deployment_Log record: Action = ROLLBACK, Scenario = M-AUDIT-LOGGER
3. Manually write an Audit_Log entry: "M-AUDIT-LOGGER rolled back at [TIMESTAMP] by [NAME]. Reason: [REASON]"
4. Identify the last known-good Make scenario version in Make's version history
5. Revert to previous version in Make (Scenario > History > Restore)
6. Test the restored version with a manual trigger in Sandbox before re-enabling in Production
7. Re-enable M-AUDIT-LOGGER in Production
8. Update Deployment_Log: action complete, rollback successful

**Data cleanup:** Review Audit_Log records created since the defect started. Mark duplicate or malformed entries with Rollback_Flag = TRUE. Do not delete — governance requires all records to be retained.

**Impact on other scenarios:** All other scenarios continue running; they will produce unlogged executions until M-AUDIT-LOGGER is restored. HEALTH-001 will alert on the logging gap — this is expected and correct.

---

### 2.2 M-BRAND-ROUTER Rollback

**When to roll back:** Brand routing delivering SSS leads to ME workflow or vice versa; webhook trigger not receiving Webflow payloads; idempotency check bypassed causing duplicates.

**Rollback steps:**
1. Immediately contact Webflow developer (or Will, if access available): disable the Webflow form POST webhook to the Make endpoint. This stops all new inbound leads during rollback.
2. Pause M-BRAND-ROUTER in Make
3. Pause M-LEAD-INTAKE, M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT simultaneously (all downstream scenarios that receive routed leads)
4. Write Deployment_Log record: Action = ROLLBACK, Scenario = M-BRAND-ROUTER (and downstream pauses)
5. Identify all Requests records created since the defect (filter by Created_At timestamp)
6. For each misrouted record, manually update: Brand field to correct value; Assigned_Concierge if wrong
7. Alert Luciana: "Brand router is paused. No new leads are being processed. I will notify you when restored."
8. Revert M-BRAND-ROUTER to previous version in Make
9. Test with internal fake webhook payload (both SSS and ME routing)
10. Re-enable M-BRAND-ROUTER; re-enable downstream scenarios in deployment order
11. Re-enable Webflow webhook
12. Update Deployment_Log: rollback complete

**Data cleanup:** All misrouted Request records must be manually corrected. Create an Audit_Log entry for each corrected record. Luciana reviews all corrected records before any follow-up action is taken.

---

### 2.3 M-LEAD-INTAKE Rollback

**When to roll back:** Creating duplicate Request records despite idempotency protection; missing required fields on created records; writing to wrong Airtable table; creating Client records with wrong or blank data.

**Rollback steps:**
1. Pause M-LEAD-INTAKE in Make
2. Disable Webflow webhook (prevents new leads entering the paused scenario queue)
3. Write Deployment_Log record
4. Identify all Request records created since defect timestamp
5. For each record, assess:
   - Duplicate records → mark Status = DUPLICATE; do NOT delete (audit integrity); Luciana reviews manually
   - Records with missing required fields → Luciana manually completes field data; flag with Data_Corrected = TRUE
   - Records with incorrect Client linkage → Luciana manually re-links; log correction in Audit_Log
6. Revert M-LEAD-INTAKE to previous version
7. Test with fake payload: verify all required fields populated, idempotency key written, no duplicates created
8. Re-enable; re-enable Webflow webhook
9. Update Deployment_Log

**Data cleanup:** No Request records are deleted. Duplicates are flagged; the authoritative record is confirmed with Luciana. Client records created in error must have Environment = ROLLBACK_ARTIFACT added to Notes field (do not delete — Client table maintains audit history).

---

### 2.4 M-SLACK-ALERTS Rollback

**When to roll back:** Sending duplicate Slack alerts for the same event; alerting wrong channel; missing alerts that should fire; formatting errors in alert messages causing unreadability.

**Rollback steps:**
1. Pause M-SLACK-ALERTS in Make
2. Write Deployment_Log record
3. Notify Luciana directly (phone or personal message): "Slack automation alerts are paused. I'll notify you of new leads manually until restored."
4. If duplicate alerts were sent: post correction in #sss-ops-alerts: "Correction: the previous [N] alerts were duplicates of [original alert reference]. No action required."
5. Revert M-SLACK-ALERTS to previous version
6. Test: trigger a fake Request creation and verify exactly one Slack alert fires in #sss-ops-alerts
7. Re-enable M-SLACK-ALERTS
8. Update Deployment_Log

**Data cleanup:** No Airtable data cleanup required — M-SLACK-ALERTS does not write Airtable records (only reads and sends Slack). Review Slack message history to confirm duplicate alerts are annotated.

---

### 2.5 M-CONCIERGE-ASSIGNMENT Rollback

**When to roll back:** Assigning wrong concierge; not assigning any concierge; overwriting a manual assignment that Luciana had already set; failing to update the Requests table with assignment.

**Rollback steps:**
1. Pause M-CONCIERGE-ASSIGNMENT in Make
2. Write Deployment_Log record
3. Notify Luciana: "Concierge assignment automation is paused. Please manually assign concierge for any new requests until I restore it."
4. Identify all Requests records with Assigned_At timestamp in the defect window
5. Luciana reviews each record and confirms correct assignment or corrects it manually
6. Log each manual correction in Audit_Log
7. Revert M-CONCIERGE-ASSIGNMENT to previous version
8. Test: create a fake Request record and verify correct assignment fires
9. Re-enable M-CONCIERGE-ASSIGNMENT
10. Update Deployment_Log

---

### 2.6 M-STRIPE-DEPOSIT Rollback

**When to roll back:** Creating Stripe payment intents with incorrect amounts; sending deposit request emails to wrong email addresses; creating duplicate payment intents; using test-mode keys in Production.

**CRITICAL — Stripe actions required before any Make changes:**

1. **Will opens Stripe dashboard immediately.**
2. **Identify all payment intents created in the defect window** (filter by Created timestamp in Stripe Developers > Logs).
3. **For each payment intent:**
   - If status = `requires_payment_method` (not yet paid): void the intent immediately
   - If status = `requires_confirmation`: cancel the intent
   - If status = `succeeded` (client paid incorrectly): Do NOT void. Flag for Will's manual review. Contact client directly before any refund action.
4. Write a Founder Decision record for any succeeded payment intent that requires manual resolution.

**Make rollback steps (after Stripe cleanup):**
5. Pause M-STRIPE-DEPOSIT in Make
6. Write Deployment_Log record
7. Revert M-STRIPE-DEPOSIT to previous version
8. Update Bookings/Requests records: remove any Stripe_Payment_Intent_ID values that were voided/cancelled
9. Test with Stripe test card in Sandbox before re-enabling Production
10. Will explicitly re-authorizes Production activation (GATE-04 and GATE-05 re-confirmed)
11. Re-enable M-STRIPE-DEPOSIT
12. Update Deployment_Log

**Data cleanup:** Every voided or cancelled Stripe payment intent must have a corresponding note in the affected Booking or Request record: "Payment intent [PI_ID] voided during rollback on [DATE]. Reason: [REASON]."

---

### 2.7 M-BOOKING-CREATION Rollback

**When to roll back:** Creating Booking records with wrong linked records (wrong Client, wrong Yacht, wrong Package); creating Booking records with incorrect Status; creating duplicate Booking records.

**Rollback steps:**
1. Pause M-BOOKING-CREATION in Make
2. Write Deployment_Log record
3. Identify all Booking records created in the defect window (filter by Created_At)
4. For each Booking record:
   - Assess: is there a real Stripe payment intent associated? If yes → do not delete; flag and resolve manually
   - If no Stripe association and the Booking is a duplicate or incorrect: mark Status = ROLLBACK_VOID; add note in Charter_Notes field; do NOT delete
   - If linked records are wrong: Luciana manually corrects all linked fields; log each correction in Audit_Log
5. Revert M-BOOKING-CREATION to previous version
6. Test: verify Booking creation with all correct linked records and correct Status
7. Re-enable M-BOOKING-CREATION
8. Update Deployment_Log

**Data cleanup:** No Booking records are deleted. Records marked ROLLBACK_VOID are excluded from all operational views. They remain in the table for audit purposes.

---

### 2.8 M-BOOKING-CONFIRMATION Rollback

**When to roll back:** Sending confirmation emails with wrong client name, wrong charter date, wrong vessel, wrong amount; sending SMS to wrong phone number; sending duplicate confirmation communications; sending confirmation before deposit is confirmed.

**CRITICAL — This is the highest-stakes individual rollback because real communications have reached real clients.**

**Immediate actions (within 5 minutes of detection):**
1. Pause M-BOOKING-CONFIRMATION in Make immediately
2. Luciana calls the client directly (phone) if an incorrect confirmation was sent
3. Will is notified immediately — Will reviews the incorrect communication before Luciana calls

**Make rollback steps:**
4. Write Deployment_Log record: include full detail of what was sent incorrectly and to whom
5. Write Audit_Log entry: CRITICAL flag, full description
6. Revert M-BOOKING-CONFIRMATION to previous Make version
7. Update Booking record: set Confirmation_Sent = FALSE; add note in Charter_Notes with incorrect communication details
8. Test in Sandbox with fake client data before ANY re-enable
9. Will explicitly approves re-enable (GATE-07 re-confirmed)
10. Re-enable M-BOOKING-CONFIRMATION
11. Update Deployment_Log

**Client communication protocol after incorrect send:** Will drafts the correction or apology communication. Luciana reviews before sending. Never send an automated correction — this must be manual, personal, and from a named human. Log the correction communication in the Conversations table.

---

## SECTION 3 — FULL STAGE 1 ROLLBACK (ALL 8 SCENARIOS)

### 3.1 When to Declare Full Stage 1 Rollback

Full rollback is declared by Will only when:
- More than 3 SEV-2 Founder Decisions created in a 60-minute window (any combination of scenarios)
- A root cause is identified that affects the shared infrastructure (Airtable base misconfiguration, API key compromise, Environment field absent from multiple tables)
- M-AUDIT-LOGGER is down and two or more other scenarios are simultaneously failing
- Any evidence of data integrity compromise across multiple tables

### 3.2 Full Rollback Sequence

Execute in this exact order:

```
Phase 1 — STOP (Target: 5 minutes)
1.1  Will disables Webflow webhook → Make endpoint (stops all new inbound leads)
1.2  Will pauses all 8 Make scenarios simultaneously in Make dashboard
1.3  Luciana sends message to #sss-ops-alerts:
     "All automations paused for emergency maintenance. Manual ops mode active.
      Luciana handling all leads manually. ETA for restoration: TBD."

Phase 2 — SECURE (Target: 10 minutes)
2.1  Will audits Stripe: identify all payment intents from last 4 hours
     — void all unpaid intents created during the defect window
     — flag any paid intents for manual review
2.2  Will confirms Stripe live API key is not compromised
2.3  Will confirms no Airtable field deletions have occurred (check Airtable revision history)

Phase 3 — ASSESS (Target: 10 minutes)
3.1  Will and Luciana review Automation_Failures table: identify all failure records in defect window
3.2  Identify root cause: is this a Make scenario defect? An Airtable schema issue? An API key issue?
3.3  Identify which Airtable records are affected (Requests, Bookings, Clients)
3.4  Create a Founder Decision record: Type = SEV-1, full description of incident

Phase 4 — CLEAN (Target: 15 minutes)
4.1  Luciana manually reviews and corrects all Request records created in defect window
4.2  Luciana manually reviews and corrects all Booking records created in defect window
4.3  Will manually corrects any Stripe-related records
4.4  All corrections logged in Audit_Log with Correction_By and Correction_Timestamp

Phase 5 — RESTORE (Target: after root cause resolution — may be hours later)
5.1  Fix root cause in Development environment first
5.2  Full Sandbox test suite re-executed per MAKE_TESTING_PROTOCOLS.md
5.3  Will signs production re-activation for each scenario per deployment order (MAKE_DEPLOYMENT_ORDER.md)
5.4  Wave-by-wave re-activation following Section 5 of MAKE_DEPLOYMENT_ORDER.md
```

### 3.3 Full Rollback Timeline Target

| Phase | Target Duration | Owner |
|-------|----------------|-------|
| Phase 1 — Stop | 5 minutes | Will + Luciana |
| Phase 2 — Secure | 10 minutes | Will |
| Phase 3 — Assess | 10 minutes | Will + Luciana |
| Phase 4 — Clean | 15 minutes | Luciana (Will directing) |
| Total emergency stabilization | 30 minutes | — |
| Phase 5 — Restore | Variable (hours to days) | Will + Luciana |

---

## SECTION 4 — DATA INTEGRITY DURING ROLLBACK

### 4.1 Record Deletion Policy

**No Airtable records are deleted during any rollback under any circumstances.** All records — including duplicates, incorrect records, and test records — are retained and flagged. Deletion of any Airtable record in a financial or operational table is a SEV-1 event per governance policy (Systems Intelligence Architecture Section 8.4).

### 4.2 Flagging Conventions

| Record State | Flag Method | Field Used |
|-------------|-------------|------------|
| Duplicate record | Status = DUPLICATE | Requests.Status or Bookings.Status |
| Incorrect record from rollback | Charter_Notes / Request_Notes: "ROLLBACK_ARTIFACT — [date]" | Notes fields |
| Stripe-voided payment reference | Charter_Notes: "PI [ID] voided [date] during rollback" | Charter_Notes |
| Manually corrected record | Audit_Log entry with Correction_By + timestamp | Audit_Log |

### 4.3 Airtable Records That May Exist After a Rollback

| Table | Records Created | Action Required |
|-------|----------------|-----------------|
| Requests | May have duplicates or incomplete records | Flag; do not delete; Luciana reviews |
| Bookings | May have incorrect linked records | Correct manually; flag with note |
| Clients | May have records with missing UUID | Luciana adds UUID manually |
| Automation_Failures | Will have rollback-period records | Retain; add Resolution_Notes after root cause confirmed |
| Audit_Log | May have gap during rollback period | HEALTH-001 detects; add manual entry to close gap |

### 4.4 Pending Stripe Charges

Before any rollback is considered complete, Will must confirm:
1. Zero open (uncollected) Stripe payment intents from the defect window remain active
2. Any client who received a payment link that has been voided must be notified immediately (Luciana calls; Will drafts message)
3. Any payment that was collected incorrectly must have a corresponding Founder Decision: REFUND_REQUIRED created

---

## SECTION 5 — AUDIT LOG ENTRIES DURING ROLLBACK

The following Audit_Log entries are mandatory during any rollback. Write them in real time, not retroactively.

| Event | Audit_Log Entry Required | Written By |
|-------|--------------------------|-----------|
| Decision to roll back made | "Rollback declared for [SCENARIO] at [TIMESTAMP]. Reason: [REASON]. Authorized by Will." | Will |
| Scenario paused in Make | "Make scenario [SCENARIO] paused at [TIMESTAMP] by [NAME]." | Will or Luciana |
| Stripe payment intent voided | "Stripe PI [ID] voided at [TIMESTAMP] by Will. Affected Booking: [ID]." | Will |
| Airtable record manually corrected | "Record [ID] in [TABLE] manually corrected: [FIELD] changed from [OLD] to [NEW] by [NAME]." | Luciana |
| Rollback complete | "Rollback for [SCENARIO] complete at [TIMESTAMP]. All flagged records reviewed. Restoration pending." | Will |

---

## SECTION 6 — VERIFICATION STEPS AFTER ROLLBACK

### 6.1 No Orphaned Records

After rollback cleanup is complete, run these Airtable checks:

```
Check 1: Requests with Status = PENDING and no Assigned_Concierge
         → Find: filter Requests where Assigned_Concierge IS EMPTY and Status = PENDING
         → Expected: 0 records (all should have assignment or be flagged)

Check 2: Bookings with Status = CONFIRMED and no linked Client
         → Find: filter Bookings where Client IS EMPTY and Status = CONFIRMED
         → Expected: 0 records

Check 3: Automation_Failures with Status = OPEN older than 2 hours
         → Find: filter Automation_Failures where Status = OPEN and Created_At < [now - 2h]
         → Expected: 0 records (all should be RESOLVED or escalated to Founder Decision)

Check 4: Audit_Log entries with Gap_Flag = TRUE
         → Find: all records where Gap_Flag = TRUE
         → Expected: 0 records (HEALTH-001 should have cleared or Will acknowledged all gaps)
```

### 6.2 No Pending Stripe Charges

```
Stripe Dashboard Check:
1. Navigate to Stripe Developers > Payments
2. Filter by: Date range = [rollback window]; Status = requires_payment_method
3. Expected: 0 open payment intents from the defect window
4. If any open intents found: Will voids immediately and creates Founder Decision
```

### 6.3 No Duplicate Client Communications Sent

Luciana verifies via Quo SMS dashboard and Gmail sent folder:
- Zero duplicate confirmation emails sent in the defect window
- Zero duplicate SMS sent in the defect window
- If duplicates confirmed: log in Conversations table; Will determines if client apology needed

---

## SECTION 7 — ROLLBACK DECISION MATRIX

### 7.1 Rollback vs. Fix-in-Place

| Condition | Decision | Rationale |
|-----------|----------|-----------|
| Error in one scenario, no client-facing impact, fix < 30 minutes | Fix-in-place | Rollback overhead exceeds fix time; no client risk |
| Error in one scenario, client-facing impact (wrong email/SMS sent) | Rollback + fix | Must return to known-good state before any further client contact |
| Error creates duplicate Airtable records, no Stripe impact | Fix-in-place with data cleanup | Data can be corrected without rollback |
| Stripe payment intent created with wrong amount | Rollback M-STRIPE-DEPOSIT | Financial integrity requires rollback |
| Two or more scenarios failing simultaneously | Rollback both | Multi-scenario failure suggests shared infrastructure issue |
| Root cause unknown after 15 minutes of investigation | Full rollback | Unknown cause = unacceptable risk to continue |
| Environment guard bypassed (Sandbox record processed in Production) | Rollback affected scenario | Governance violation requires formal rollback |

---

## SECTION 8 — RECOVERY PROCEDURE AFTER ROLLBACK

### 8.1 Root Cause Documentation (Required Before Re-Deploy)

Before any rolled-back scenario is re-deployed to Production, Will must document the root cause in the Founder Decision record created during the rollback event:

```
ROOT CAUSE ANALYSIS — REQUIRED FIELDS
1. What failed: [specific module, field, or API call]
2. Why it failed: [defect in scenario logic / API key issue / schema mismatch / other]
3. How it was detected: [HEALTH-001 / Luciana observation / client complaint / Slack alert]
4. Impact: [records affected, client communications sent, Stripe intents created]
5. Fix implemented: [exact change made in Make scenario or Airtable]
6. Prevention: [what change prevents recurrence — test case added, idempotency fix, etc.]
7. Test evidence: [Luciana's Sandbox test results confirming fix works]
```

### 8.2 Re-Deploy Steps

1. Apply fix in Development environment
2. Promote to Sandbox; run complete test suite for the affected scenario
3. If the scenario is upstream of others, re-run integration tests for all dependent scenarios
4. Luciana executes and signs test results
5. Will reviews root cause documentation and test results
6. Will re-signs Production Activation Checklist
7. Re-deploy following MAKE_DEPLOYMENT_ORDER.md (correct wave and timing)

---

## SECTION 9 — EMERGENCY ROLLBACK PROCEDURE

### 9.1 Scenario: A Real Client Receives a Message During Testing

This is the most critical emergency scenario. It occurs if:
- A test with real email/phone data is accidentally routed through Production M-BOOKING-CONFIRMATION
- A Sandbox test uses a real client's email address or phone number instead of test data
- Environment guard fails and a live client's data triggers a Sandbox scenario that sends communications

**Immediate response (under 3 minutes):**

```
MINUTE 1:
- Luciana calls Will immediately: "Real client may have received an automated test message."
- Will pauses M-BOOKING-CONFIRMATION in Make within 60 seconds

MINUTE 2:
- Luciana identifies the client: name, email, phone number, message content
- Luciana prepares to call the client

MINUTE 3:
- Will drafts the apology message for the client
- Will determines: was this a test message (confusing but harmless) or incorrect information
  (wrong pricing, wrong date, wrong vessel)?
```

**Client contact protocol:**
- Luciana calls the client within 5 minutes of detection
- Talking points: "We are so sorry — you received a message in error as part of a system test. Please disregard it. Your booking status is [CORRECT STATUS]. A corrected/confirmation message will follow shortly from us directly."
- Will sends a personal email (not automated) to the client within 30 minutes

**System actions:**
- Write Audit_Log entry with CRITICAL flag, full timeline, client name, message content
- Create Founder Decision: COMM-ERROR with full details
- Complete rollback of M-BOOKING-CONFIRMATION per Section 2.8
- Before any re-enable: root cause documented and test data hygiene protocol added to MAKE_TESTING_PROTOCOLS.md

---

*Document Authority: Will (Founder)*  
*Last Review: May 2026*  
*Next Review: After Stage 1 go-live complete*
