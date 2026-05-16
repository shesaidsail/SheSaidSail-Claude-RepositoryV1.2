# MAKE_ROLLBACK_PROTOCOLS

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Rollback instructions for every scenario and every stage. Validated before each deployment.
**Classification:** Confidential — Internal Use Only

---

## ROLLBACK AUTHORITY

All rollback decisions are Will's authority. Luciana may execute a rollback if:
1. Will is unreachable
2. The scenario is causing active client harm (duplicate messages, financial errors)
3. The action is limited to disabling a scenario in Make (not data correction)

Any data correction (deleting Airtable records, reversing financial writes) requires Will's approval regardless of urgency.

---

## SECTION 1 — UNIVERSAL ROLLBACK STEPS (EVERY SCENARIO)

**Step 1: Stop the scenario**
```
Make dashboard → Scenarios → [Scenario Name] → Toggle OFF
This stops all future executions immediately.
In-progress execution will complete its current module and then stop at the next error handler.
```

**Step 2: Log the rollback**
```
Airtable > Audit_Log > Create Record:
  Triggering_Event: "ROLLBACK — [Scenario ID] — [reason]"
  Output: "Scenario disabled at [timestamp] by [person]"
  Approval_State: HUMAN_APPROVED
  Environment: Production
```

**Step 3: Create Founder Decision**
```
Type: SYSTEM
Urgency: SAME_DAY
Context: "Rollback executed for [Scenario ID]. Reason: [description]. Affected records: [list]. Corrective actions required: [list]."
```

**Step 4: Notify**
```
Slack > DM to Will + Luciana: "ROLLBACK EXECUTED — [Scenario ID] — [reason] — [what was affected]"
```

**Step 5: Assess damage**
```
Identify: What records were created/updated/deleted by the failed scenario?
Identify: What messages were sent to clients?
Determine: Which of these need correction (Airtable records) vs. management (client messages)?
```

**Step 6: Correct**
```
Airtable record corrections: Will approves before any deletion
Client message management: Luciana follows up personally within 2 hours
Financial record corrections: Will approves; document corrective action in Founder Decision
```

**Step 7: Root cause and fix**
```
Reproduce failure in sandbox
Fix the root cause (not the symptom)
Re-test in sandbox with edge cases
Will approves re-deployment
```

---

## SECTION 2 — SCENARIO-SPECIFIC ROLLBACK PROCEDURES

### M-LEAD-INTAKE Rollback

**Risk:** Duplicate Requests records, Client records with incorrect Brand assignment

**Damage Assessment:**
- Query Requests table for records created in the failure window
- Query Audit_Log for all M-LEAD-INTAKE entries in the failure window

**Correction:**
- Duplicate Requests: delete duplicates manually, preserving the oldest record
- Incorrect brand assignment: update Brand field manually on affected Requests
- Client records created incorrectly: update or merge manually

**Client impact:** Minimal — no outbound messages sent at this stage. The Slack alert to Luciana is the only external action and is non-harmful if duplicate.

**Rollback time:** 30 minutes

---

### M-BRAND-ROUTER Rollback

**Risk:** Requests classified with wrong brand

**Damage Assessment:**
- Check Requests.Brand for requests created in failure window
- Check Requests.Routing_Confidence for LOW confidence that was not alerted

**Correction:**
- Update Brand field manually on affected Requests
- Luciana reviews all LOWconfidence requests before any AI outbound

**Client impact:** None — no outbound actions taken by brand router alone

**Rollback time:** 15 minutes

---

### M-BOOKING-CREATION Rollback

**Risk:** Duplicate Bookings records, Stripe payment links sent in error, incorrect amounts

**Pre-rollback (BEFORE DEPLOYING):** Confirm this rollback plan is documented and understood.

**Damage Assessment:**
- Query Bookings for records created in the failure window
- Check Stripe dashboard for payment links created in the failure window
- Check email/SMS delivery records for duplicate sends

**Correction:**
- Duplicate Bookings: delete extras in Airtable (Will approval required if any have Stripe data attached)
- Stripe payment links in error: deactivate in Stripe dashboard (Payment Links → Deactivate)
- Emails sent in error: Luciana calls client to clarify if duplicate messages were received
- SMS sent in error: Luciana follows up via phone if needed

**Client impact:** Medium — duplicate deposit request emails/SMS are confusing but not harmful. Must be managed personally.

**Rollback time:** 60 minutes (includes client management time)

---

### M-STRIPE-DEPOSIT Rollback

**Risk:** Booking status incorrectly set, confirmation email sent without valid deposit, duplicate processing

**Damage Assessment:**
- Check Stripe payment_intent log for the failure window
- Check Bookings for status changes in the failure window
- Check Audit_Log for M-STRIPE-DEPOSIT entries

**Correction:**
- Status incorrectly set: revert Booking.Status manually (Will approval required)
- Confirmation sent without payment: Luciana contacts client to clarify
- Duplicate status update: Booking.Status is idempotent (can be set to same value again without harm) — verify Idempotency_Key is set
- Duplicate confirmation emails: Luciana contacts client apologetically

**Client impact:** Medium — wrong status could allow premature charter confirmation. Must be corrected immediately.

**Rollback time:** 45 minutes

---

### M-BOOKING-CONFIRMATION Rollback

**Risk:** Confirmation emails sent prematurely or to wrong client

**Damage Assessment:**
- Query Audit_Log for M-BOOKING-CONFIRMATION entries in failure window
- Identify affected Booking records

**Correction:**
- Premature confirmation: Luciana contacts client to clarify timing
- Wrong client: Luciana contacts affected clients immediately — apologize, clarify
- HV client routing failure (client email sent instead of Luciana DM): Luciana contacts HV client for personal follow-up

**Client impact:** Medium-High for HV client routing failures. Must be managed personally within 2 hours.

**Rollback time:** 30 minutes (scenario) + 2 hours (client management for HV clients)

---

### M-BASIC-LIFECYCLE Rollback

**Risk:** Duplicate lifecycle messages, messages sent to wrong bookings, messages sent despite Emergency_Flag

**Damage Assessment:**
- Check all send-state boolean fields on Bookings for unexpected true values
- Query Audit_Log for M-BASIC-LIFECYCLE entries in failure window
- Cross-reference: which clients received which messages

**Correction:**
- Duplicate T-72hr reminder: minor inconvenience, Luciana notes in client record
- Duplicate D1 message: embarrassing but manageable — Luciana personal note to client
- Message sent during Emergency_Flag: Will reviews immediately — treat as L3 communication breach
- Wrong messages sent (e.g., D1 sent to a booking not yet chartered): Luciana contacts client apologetically

**CRITICAL:** If Emergency_Flag bypass is detected — escalate to Will immediately. This is a system failure requiring full audit of the failure window.

**Rollback time:** 30 minutes (scenario) + variable (client management)

---

### M-REVIEW-REQUEST Rollback

**Risk:** Review requests sent to ineligible clients (bad charter grade, emergency, chargeback)

**Damage Assessment:**
- Check D7_Sent boolean on Bookings for unexpected true values
- Cross-reference Charter_Grade and Chargeback_Risk for affected bookings
- Determine if any ineligible bookings received review requests

**Correction:**
- Review request to unhappy client (Charter_Grade D/F): Luciana contacts client personally, diverts from public review to private feedback channel
- Review request during active chargeback: Luciana contacts client — do not encourage review action during dispute
- Duplicate review request: minor — note in client record

**Client impact:** High if ineligible clients received review requests — Google reviews from upset clients are permanent.

**Rollback time:** 30 minutes (scenario) + 2 hours (client management for high-risk cases)

---

### M-YACHT-AVAILABILITY-LOCK Rollback

**Risk:** Incorrect availability locks blocking legitimate bookings, missed locks allowing double booking

**Damage Assessment:**
- Query Yacht_Availability for records created in failure window
- Cross-reference with active Bookings for the affected dates

**Correction:**
- Incorrect lock: Update Yacht_Availability.Status → AVAILABLE, clear Booking_ID
- Missed lock: Manually set Yacht_Availability.Status → BOOKED, add Booking_ID

**Client impact:** None directly — this is an internal availability table. Indirect risk of double booking if lock was missed.

**Rollback time:** 30 minutes

---

### M-CHARTER-BRIEF Rollback

**Risk:** Incorrect brief sent to Luciana or City Manager, missing brief for T-14

**Damage Assessment:**
- Check Charter_Brief.Status in Airtable for affected bookings
- Check Audit_Log for M-CHARTER-BRIEF entries

**Correction:**
- Incorrect brief: Luciana generates manually or re-triggers scenario after fixing underlying data issue
- Brief not generated: Luciana creates manually — charter cannot proceed without brief

**Client impact:** None directly — brief goes to City Manager only

**Rollback time:** 45 minutes

---

### M-ESCALATION-ROUTER Rollback

**Risk:** L4 emergency not escalated correctly, L2/L3 boundary misclassified

**This is the highest-risk rollback.** Emergency routing failures can have direct client safety implications.

**Damage Assessment:**
- Check Emergency_Escalations for records created in failure window
- Check Founder_Decisions for EMERGENCY type records
- Confirm Will was notified directly (not just channel)

**Correction:**
- L4 not escalated: Will takes manual control immediately. All charter automations paused manually.
- L2/L3 misclassified upward (harmless — more escalation than needed): Will de-escalates manually
- L2/L3 misclassified downward (Luciana received L3 as L2): Will manually reviews the case

**Client impact:** Potentially High if L4 was misrouted

**Rollback time:** Immediate — this is always an emergency response

---

### M-SYNTER-SYNC Rollback

**Risk:** Incorrect financial data written to P&L Per Charter, duplicate P&L records

**Damage Assessment:**
- Query P&L Per Charter for records created in failure window
- Verify against Bookings records for accuracy

**Correction:**
- Incorrect P&L data: Update P&L Per Charter fields manually (Will approval required)
- Duplicate P&L records: Delete extras (Will approval required)
- P&L written for incomplete/non-completed booking: Delete record (Will approval)

**Financial impact:** Medium — P&L records are used for investor reporting. Incorrect data must be corrected before any period close.

**Rollback time:** 60 minutes + Will review

---

## SECTION 3 — PROMPT VERSION ROLLBACK (AI Scenarios)

When AI drift is detected or a Claude API response is incorrect, prompt rollback is separate from scenario rollback.

**Timeline:** Target 15 minutes from detection to rollback complete.

```
1. Identify: which AI_Prompt_Versions record is the current production version
2. Identify: which version is the prior (stable) version (Rollback_To_Version field)
3. Airtable: Update current production version — Status → DEPRECATED
4. Airtable: Update prior version — Status → LIVE
5. No Make scenario update needed — Make reads the LIVE + Will_Approved = true version dynamically
6. Test: Trigger the affected scenario with a test record → confirm correct prompt used
7. Audit_Log: Document the rollback — from version, to version, reason, timestamp
8. AI_Audit: Log the drift incident with root cause
9. Will: Review all AI-generated messages sent since the drifted version was deployed
```

**NOTE:** Make reads AI_Prompt_Versions on every execution (it does not cache). Rollback takes effect immediately on the next scenario run — no scenario rebuild required.

---

## SECTION 4 — STAGE-LEVEL ROLLBACK

If an entire stage needs to be rolled back (e.g., a Stage 2 scenario is causing cascading issues):

**Stage 2 complete rollback:**
1. Disable all Stage 2 scenarios in Make (one by one — M-AUTOMATION-HEALTH last)
2. Confirm Stage 1 scenarios are still running correctly (they are independent)
3. Assess which Stage 2 scenario caused the issue
4. Fix and re-test in sandbox
5. Re-deploy Stage 2 in the same sequence as the original deployment order

**Stage 1 is never rolled back completely while ads are running.** If a Stage 1 scenario fails:
- Disable only the failing scenario
- Implement manual fallback for that specific function
- Stage 1 as a whole remains operational

---

## SECTION 5 — ROLLBACK TESTING REQUIREMENT

Before each stage deployment, the engineer must verify they can execute a rollback:

```
Pre-deployment rollback test:
1. Deploy scenario to sandbox
2. Run scenario once successfully
3. Manually disable scenario in sandbox Make
4. Verify scenario execution stops immediately
5. Restore sandbox Airtable record to pre-execution state
6. Re-enable scenario
7. Confirm scenario re-runs correctly

If any of these steps fail → the scenario is not ready for production deployment.
```

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_ROLLBACK_PROTOCOLS v1.0*
*Effective May 2026*
