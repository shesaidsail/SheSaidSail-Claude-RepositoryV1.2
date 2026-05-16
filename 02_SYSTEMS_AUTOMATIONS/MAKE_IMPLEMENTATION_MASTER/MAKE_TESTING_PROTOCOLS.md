# MAKE_TESTING_PROTOCOLS

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Fake lead, fake booking, and fake payment testing protocols for all Make scenarios.
**Classification:** Confidential — Internal Use Only

---

## TESTING PRINCIPLES

1. Every scenario is tested in sandbox before production promotion — no exceptions
2. Sandbox testing uses: sandbox Airtable base + Stripe test mode + test Slack channels + test email addresses
3. Production testing uses a controlled fake lead — Will present during first production test
4. Testing is not complete until every failure path is tested — not just the happy path
5. Test data is clearly tagged with Environment = Sandbox or "TEST" prefix in record names
6. Test Stripe transactions are refunded immediately after testing is confirmed

---

## SANDBOX ENVIRONMENT SETUP

Before any testing begins:

| Item | Configuration | Verified |
|------|--------------|---------|
| Sandbox Airtable base | Separate from production — test records only | ☐ |
| Stripe test mode | Test API keys in Make — not live keys | ☐ |
| Test email addresses | test@shesaidsail.com + Will's personal email | ☐ |
| Test phone number | Will's mobile in Quo sandbox mode | ☐ |
| Sandbox Slack channels | #sss-sandbox-leads, #sss-sandbox-bookings, #sss-sandbox-alerts | ☐ |
| Sandbox Webflow form | Separate form pointing to sandbox Make webhook | ☐ |
| Sandbox Make workspace | Separate from production — clearly labeled | ☐ |

---

## SECTION 1 — STAGE 1 TESTING

### Test Suite 1A: Full Lead-to-Review Happy Path

Execute this test end-to-end after all Stage 1 scenarios are deployed to sandbox.

**Test Client:**
```
Name: Test Client — SSS
Email: test@shesaidsail.com
Phone: [Will's mobile]
Charter Date: [14 days from today]
Group Size: 8
Occasion: Birthday
Notes: This is a test submission
Source: Webflow form (sandbox)
```

**Step 1: Lead Intake**
```
Action: Submit sandbox Webflow form with test client data
Expected: Sandbox Requests record created (Environment = Sandbox)
Expected: Slack message in #sss-sandbox-leads
Expected: Brand = SSS (URL is shesaidsail.com)
Expected: Routing_Confidence = HIGH
Expected: Audit_Log entry created
Verify: No record created in PRODUCTION Airtable base
Pass Criteria: All expected outcomes achieved, zero production writes
```

**Step 2: Brand Router Validation**
```
Action: (Already triggered in Step 1)
Expected: Brand = SSS, Routing_Confidence = HIGH
Test variant: Repeat with ME-branded form data → confirm Brand = ME
Pass Criteria: Both brands route correctly
```

**Step 3: Booking Creation**
```
Action: Manually set sandbox Request.Status = AVAILABILITY_CONFIRMED
Expected: Sandbox Booking record created
Expected: Stripe test mode payment link generated ($X deposit amount)
Expected: Deposit request email sent to test@shesaidsail.com
Expected: SMS sent to Will's mobile
Expected: Slack message in #sss-sandbox-bookings
Expected: Audit_Log entry
Verify: Package_Price × 0.5 = Deposit_Amount (correct calculation)
Verify: Stripe metadata includes booking_source, brand, charter_date, environment
Pass Criteria: All expected outcomes, correct amounts, correct metadata
```

**Step 4: Stripe Deposit**
```
Action: In Stripe test mode — trigger payment_intent.succeeded for the test payment link
Expected: Sandbox Booking.Status → DEPOSIT_PAID
Expected: Confirmation email sent to test email
Expected: Slack message in #sss-sandbox-bookings: "✅ DEPOSIT CONFIRMED"
Expected: Audit_Log entry
Verify: Idempotency_Key set on Booking record
Test: Replay the same Stripe event → confirm no duplicate status change, no duplicate email
Pass Criteria: Correct status, idempotency holds on replay
```

**Step 5: Booking Confirmation**
```
Action: Manually set sandbox Booking.Status = CONFIRMED
Expected: Confirmation email sent to test email with charter details
Expected: Slack in #sss-sandbox-bookings: "📋 CONFIRMED"
Expected: Audit_Log entry
Test: Repeat trigger → confirm email not sent twice (Confirmation_Sent_At gate)
Pass Criteria: One email, correct content, no duplicates
```

**Step 6: Concierge Assignment**
```
Action: (Triggered by Status = DEPOSIT_PAID in Step 4)
Expected: Slack DM to test concierge Slack ID (use Will's Slack for test)
Expected: Email to test concierge email
Expected: Concierge_Notified_At set on Booking
Pass Criteria: Notification received, timestamp set
```

**Step 7: Lifecycle Messages**
```
For each lifecycle point, manually adjust Charter_Date on sandbox Booking to simulate the correct days:

T-72hr Test:
  Set Charter_Date = today + 3
  Run M-BASIC-LIFECYCLE
  Expected: D72hr reminder email sent, D72hr_Reminder_Sent = true
  Run again: confirm no second email

T-48hr Test:
  Set Charter_Date = today + 2
  Set D72hr_Reminder_Sent = true (simulate already sent)
  Run M-BASIC-LIFECYCLE
  Expected: D48hr email sent, D48hr_Reminder_Sent = true

[Repeat pattern for T-24hr, day-of (T-12hr), D1]

D1 Test:
  Set Status = COMPLETED, Charter_Date = yesterday
  Run M-BASIC-LIFECYCLE
  Expected: D1 warmth email sent, D1_Sent = true

Pass Criteria: All lifecycle messages sent at correct times, no duplicates
```

**Step 8: Review Request**
```
Set Charter_Date = today - 7
Set Status = COMPLETED
Set Charter_Grade = A
Set D7_Review_Eligible = (formula should calculate true)
Set D7_Sent = false

Run M-REVIEW-REQUEST
Expected: Review request email sent
Expected: D7_Sent = true

Run again: confirm no second email

Test ineligible booking:
Set Charter_Grade = D → D7_Review_Eligible = false
Run → confirm no email sent (silent)

Pass Criteria: Eligible → email sent once. Ineligible → no email.
```

---

### Test Suite 1B: Emergency Stop Test

**Critical test — must pass before production activation.**

```
Setup: One sandbox Booking record with Environment = Production (simulate production record)
Action: Set Emergency_Flag = true
Expected: M-ESCALATION-ROUTER triggers → L4 flow
Expected: Slack to #sss-sandbox-emergency-ops (use sandbox channel)
Expected: Founder_Decision created: Type = EMERGENCY

Now: Attempt to trigger M-BASIC-LIFECYCLE on this booking
Expected: Emergency_Flag check catches it → EXIT immediately → Audit_Log entry: "Halted — Emergency_Flag active"
Expected: No emails, no SMS, no Slack (except the emergency alert from ESCALATION-ROUTER)

Action: Set Emergency_Flag = false (simulate Will clearing)
Expected: Next M-BASIC-LIFECYCLE run processes the booking normally

Pass Criteria: Zero outbound messages while Emergency_Flag = true
```

---

### Test Suite 1C: Brand Routing Edge Cases

```
Test 1: Ambiguous URL — submit form from a URL with no brand signals
Expected: Default to SSS + LOW confidence + Luciana alert

Test 2: ME keywords in occasion — "corporate retreat"
Expected: Brand = ME + appropriate confidence level

Test 3: SSS keywords in occasion — "bachelorette"
Expected: Brand = SSS + HIGH confidence

Test 4: SSS form submission with ME email domain (hypothetical)
Expected: URL-based routing takes precedence → SSS

Pass Criteria: All brand signals resolve correctly, LOW confidence always triggers alert
```

---

### Test Suite 1D: Idempotency Verification

```
For each scenario that creates records or sends messages:

Step 1: Execute scenario once (happy path)
Step 2: Execute exact same trigger again (simulate retry or duplicate webhook)
Step 3: Verify: exactly ONE record created, exactly ONE message sent

Specific tests:
- M-LEAD-INTAKE: Submit same form twice (same email + timestamp)
  Expected: One Requests record only
- M-STRIPE-DEPOSIT: Replay same payment_intent.succeeded event
  Expected: Booking status unchanged (already DEPOSIT_PAID), no duplicate email
- M-REVIEW-REQUEST: Run twice on same D7-eligible booking
  Expected: One review request, D7_Sent blocks second run

Pass Criteria: No duplicates across any scenario
```

---

## SECTION 2 — STAGE 2 TESTING

### Test Suite 2A: Double Booking Prevention

```
Setup:
  Yacht_Availability record: Yacht X, Date Y, Status = BOOKED, Booking_ID = BK-XXXX

Test:
  Create a new Request for Yacht X on Date Y
  Mark Request.Status = AVAILABILITY_CONFIRMED

Expected:
  M-DOUBLE-BOOKING-CHECK detects conflict
  Request.Status rolled back to AVAILABILITY_CONFLICT
  Luciana DM received: "Availability conflict — [Yacht] — [Date]"
  M-BOOKING-CREATION does NOT fire (Status is not AVAILABILITY_CONFIRMED)

Pass Criteria: Zero duplicate bookings created, Luciana alerted immediately
```

### Test Suite 2B: Failed Payment Sequence

```
Setup: Stripe test mode, active payment link for a test booking

Test Failure 1:
  Trigger: Stripe test event payment_intent.payment_failed (card_declined)
  Expected: Client email sent (retry message), SMS sent
  Expected: Booking.Payment_Failure_Count = 1
  Expected: Slack #sandbox-bookings: "❌ Payment failed — Attempt 1/3"

Test Failure 2:
  Trigger same event again
  Expected: Client email sent (second failure — "please call us")
  Expected: Luciana DM
  Expected: Payment_Failure_Count = 2

Test Failure 3:
  Trigger same event again
  Expected: Booking.Status → PAYMENT_FAILED
  Expected: Will DM + Luciana DM (3rd failure)
  Expected: Founder_Decision created

Pass Criteria: All three failure paths fire correctly in sequence
```

### Test Suite 2C: Charter Brief Generation

```
Setup: Sandbox Booking with Status = CONFIRMED, all required fields populated

Test Happy Path:
  Trigger: Set Status = CONFIRMED
  Expected: Claude API call made with assembled context
  Expected: Charter_Brief record created in Airtable with Status = PENDING_LUCIANA_REVIEW
  Expected: Slack DM to Luciana (test Luciana account) with Airtable link

Test Missing Field:
  Remove Client.Name from test record
  Trigger: Set Status = CONFIRMED
  Expected: Missing field detected, brief NOT generated
  Expected: Luciana DM: "Charter Brief blocked — missing: Client.Name"

Test Missing Prompt Version:
  Set all AI_Prompt_Versions for CHARTER_BRIEF_SYSTEM to Status = DEPRECATED
  Trigger: Set Status = CONFIRMED
  Expected: Brief NOT generated
  Expected: Luciana DM: "Charter Brief AI unavailable — create manually"

Pass Criteria: Happy path generates correct brief, missing data blocks correctly, missing prompt blocks correctly
```

### Test Suite 2D: Automation Health Monitor

```
Test Normal State:
  Run M-AUTOMATION-HEALTH
  Expected: No anomalies detected, Audit_Log entry created

Test Stale Booking:
  Create Booking with Status = CONFIRMED, Charter_Date = today + 5, Charter_Brief_Sent = false
  Wait 10 days (or manually update timestamps)
  Run M-AUTOMATION-HEALTH
  Expected: Anomaly detected, Luciana DM sent

Test High Failure Rate:
  Manually create 4+ Automation_Health records with SEV-2 in last hour
  Run M-AUTOMATION-HEALTH
  Expected: SEV-1 alert to Will

Pass Criteria: Anomalies detected correctly, SEV levels fire correctly
```

---

## SECTION 3 — STAGE 3 TESTING

### Test Suite 3A: AI Lead Scoring

```
Test High-Score Lead:
  Create Request:
    Source: Referral
    Group_Size: 12
    Occasion: Bachelorette
    Charter_Date: 2 weeks out
    Existing Client with 2 prior bookings
  Expected: AI_Lead_Score >= 75, AI_Lead_Priority = HIGH
  Expected: Luciana DM with high priority alert

Test Low-Score Lead:
  Create Request:
    Source: Meta Ad
    Group_Size: 4
    Occasion: blank
    Charter_Date: 6 months out
    No prior Client record
  Expected: AI_Lead_Score < 40, AI_Lead_Priority = LOW
  Expected: No Luciana DM (below threshold)

Pass Criteria: Scores are reasonable relative to signals. Will reviews first 10 live scores.
```

### Test Suite 3B: Revenue Health Monitor

```
Setup: 10 sandbox Bookings with known revenue figures, various statuses

Run M-REVENUE-HEALTH
Expected:
  MTD_Revenue_Booked = calculated correctly (verified manually)
  Outstanding_Balances = sum of deposit-paid bookings balance due
  Avg_Net_Margin = calculated from COMPLETED bookings

Verify each number against manual Airtable calculation.

Pass Criteria: All financial figures match manual calculation exactly (not approximately)
```

### Test Suite 3C: Thursday Digest

```
Setup: Several Lessons records, 2 pending Approvals, 5 completed Bookings this week

Trigger manually: Run M-FOUNDER-DIGEST

Expected:
  Slack DM to Will with structured digest
  All sections present: Pending Approvals, This Week's Operations, New Lessons, AI Observations
  AI Observations labeled "AI suggests:" or "Based on recent patterns:"
  No Tier 1 data (revenue) mixed with Tier 3 guidance without clear separation

Will reviews first digest and confirms:
  - Data is accurate
  - Format is readable
  - AI labels are correct

Pass Criteria: Will approves format and confirms accuracy
```

---

## SECTION 4 — PRODUCTION LIVE TEST (STAGE 1)

After all sandbox tests pass, execute this controlled production test before enabling ads:

**Participants:** Will + Luciana, both present in real time

**Test Client:** Will uses his own information as a fake client

```
1. Submit Webflow production form (real production URL)
   → Confirm Request record created in PRODUCTION Airtable base
   → Confirm Slack alert in #sss-ops-leads (real channel)

2. Will (as Luciana) marks Request as AVAILABILITY_CONFIRMED
   → Confirm Booking created in PRODUCTION Airtable
   → Confirm Stripe test link generated (MUST USE STRIPE TEST MODE for this test)
   → Confirm email and SMS received

3. Use Stripe test mode card to complete deposit
   → Confirm Booking.Status → DEPOSIT_PAID
   → Confirm confirmation email received
   → Confirm Slack #sss-ops-bookings updated

4. Set Booking.Status = CONFIRMED
   → Confirm confirmation email received

5. Verify Audit_Log entries for all actions

6. Set Emergency_Flag = true
   → Confirm all automations halt
   → Confirm #sss-emergency-ops alert fires
   → Confirm Will receives DM

7. Set Emergency_Flag = false
   → Confirm automations resume on next lifecycle run

8. Delete all test records from production Airtable
   → Will approves each deletion

PASS: All steps complete without error. Will signs off: "Stage 1 production-ready."
ADS CAN NOW RUN.
```

---

## SECTION 5 — REGRESSION TESTING

After every new scenario is deployed to production, run this regression check on all prior scenarios:

```
Check 1: M-LEAD-INTAKE still creating records correctly
  → Submit test form → confirm record created, no errors

Check 2: M-BASIC-LIFECYCLE still processing correctly
  → Manual check of last scheduler run in Audit_Log

Check 3: No new circular triggers introduced
  → Review Airtable Automation Log for any unexpected trigger chains

Check 4: Audit_Log has no gaps
  → Last 24 hours of Audit_Log entries present for all active scenarios

If any check fails: notify Will, investigate before next scenario deployment.
```

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_TESTING_PROTOCOLS v1.0*
*Effective May 2026*
