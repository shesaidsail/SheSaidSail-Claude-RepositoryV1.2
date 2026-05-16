# STAGE_1_MAKE_BUILD_REPORT.md

**Status:** READY FOR REVIEW — PENDING LIVE CREDENTIAL VALIDATION
**Stage:** 1 of 4 — Core Lead-to-Booking-to-Deposit MVP
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Environment:** Sandbox-validated → Pending Production Promotion
**Authority Documents:**
- `02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION.md`
- `02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md`
- `00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED.md`
- `00_LOCKED_GOVERNANCE__Financial_OS_v1.0_PRODUCTION.md`

---

## STAGE 1 OBJECTIVE

Build the operational MVP that allows She Said Sail and Mare Executive to:
- Safely receive leads from web forms
- Route and notify the team instantly via Slack
- Generate AI-assisted first-response drafts
- Send deposit requests via email and SMS
- Process Stripe deposits via webhook
- Create and confirm bookings with confirmation messaging
- Alert the team for agreement requirements on high-value bookings
- Trigger emergency protocols on any flagged booking
- Write immutable audit log entries for every autonomous action

Stage 1 does not include: post-charter sequences (CHARTER-001 through CHARTER-007), financial reconciliation (FINANCIAL-001 through FINANCIAL-003), intelligence digests (INTELLIGENCE-001), partner outreach (OUTREACH-001), backup (BACKUP-001), or health monitoring (HEALTH-001). Those are Stage 2, 3, and 4.

---

## NAMING CONVENTIONS

All scenarios follow this naming format:
```
[DOMAIN]-[SEQ] | [Brand] | [Environment]
```

Examples:
- `INBOUND-001 | SSS | Production`
- `BOOKING-002 | ME | Production`

Webhook endpoint naming:
```
https://hook.make.com/[workspace-id]/[scenario-slug]
```

Scenario slugs follow: `sss-[domain]-[seq]-[environment]`

---

## SCENARIO 1 — INBOUND-001

**Name:** `INBOUND-001 | SSS+ME | Production`
**Trigger:** Webflow form submission (Webhook — POST)
**Autonomy Tier:** A (fully autonomous)
**Priority:** CRITICAL PATH

### Purpose
Receive inbound inquiry from website form. Create Airtable Request record. Send auto-reply to prospect. Alert Luciana via Slack.

### Module Sequence

```
[1] Webhook (Trigger)
    - Method: POST
    - Endpoint: https://hook.make.com/[workspace]/sss-inbound-001-production
    - Authorization: Bearer header validation — reject 401 if invalid
    - Timestamp validation: reject requests older than 5 minutes
    - IP allowlist: Webflow IP range if available

[2] Router — Brand Detection
    - Condition A: Form field "brand" = "SSS" OR referrer contains "shesaidsail.com"
      → Route to SSS branch
    - Condition B: Form field "brand" = "ME" OR referrer contains "mareexecutive.com"
      → Route to ME branch
    - Condition C: Neither → Route to Fallback (alert Luciana, do not create record)

[3] Idempotency Check — Airtable Search
    - Table: Requests (tblTlSB9CO4dTGodg)
    - Filter: {Email} = {{webhook.email}} AND {Created_At} > DATEADD(NOW(), -24, 'hours')
    - If match found: STOP — do not create duplicate; log to Audit Log
    - If no match: continue

[4] Create Airtable Record — Requests
    - Table: Requests (tblTlSB9CO4dTGodg)
    - Fields to write:
      | Airtable Field         | Source                           |
      |------------------------|----------------------------------|
      | Name                   | webhook.name                     |
      | Email                  | webhook.email                    |
      | Phone                  | webhook.phone                    |
      | Brand                  | Router output: SSS / ME          |
      | City                   | webhook.city OR inferred from form|
      | Occasion               | webhook.occasion                 |
      | Group_Size             | webhook.group_size               |
      | Charter_Date_Requested | webhook.charter_date             |
      | Message                | webhook.message                  |
      | Status                 | NEW                              |
      | Agent_Status           | HUMAN_REVIEW                     |
      | Source_System          | Make                             |
      | Environment            | Production                       |
      | Source_Channel         | Webflow                          |
      | Created_At             | NOW()                            |

[5] Create Audit Log Record
    - Table: Audit Log (tblrMpTfMk8q1eNHp)
    - Fields: Action = INBOUND_LEAD_RECEIVED, Entity = Requests,
      Record_ID = {{step4.record_id}}, Brand = {{router}},
      Source_System = Make, Environment = Production,
      Prompt_Version = N/A (no AI in this step), Timestamp = NOW()

[6] Send Auto-Reply Email — Gmail
    - From: hello@shesaidsail.com (SSS) / hello@mareexecutive.com (ME)
    - To: {{webhook.email}}
    - Subject (SSS): "We got your inquiry — She Said Sail 🌊"
    - Subject (ME): "We received your request — Mare Executive"
    - Body: Approved template per brand (see Template Library)
    - Do NOT include: pricing estimates, vessel names, availability claims
    - Automations_Paused check: NOT APPLICABLE (auto-reply is safe regardless)

[7] Send Slack Alert — #sss-new-leads
    - Message format:
      🌊 NEW LEAD — [Brand]
      Name: {{name}}
      Email: {{email}}
      Phone: {{phone}}
      Date Requested: {{charter_date}}
      Occasion: {{occasion}}
      Group Size: {{group_size}}
      City: {{city}}
      Airtable: [direct record link]
    - Channel: #sss-new-leads
    - Also DM: Luciana (direct Slack user ID)

[8] Error Handler
    - On failure: Log to Automation_Failures table
    - Retry: 2 min, 5 min, 10 min
    - After 3 failures: Slack alert to Luciana + Will
    - After 4 failures: Create Founder Decision record: SEV-2
```

### Idempotency Key
`{{webhook.email}}::{{webhook.charter_date}}::INBOUND-001`
Stored in Audit Log on every execution attempt.

### Webhook URL (Sandbox)
`https://hook.make.com/[workspace]/sss-inbound-001-sandbox`

### Webhook URL (Production)
`https://hook.make.com/[workspace]/sss-inbound-001-production`
**Document in Webflow and Notion after activation.**

### Test Payload
```json
{
  "brand": "SSS",
  "name": "Jane Test",
  "email": "test@shesaidsail-sandbox.com",
  "phone": "+13055550001",
  "city": "Miami",
  "occasion": "Bachelorette",
  "group_size": 10,
  "charter_date": "2026-07-15",
  "message": "Looking to book a sunset bachelorette charter for 10 guests."
}
```

---

## SCENARIO 2 — INBOUND-002

**Name:** `INBOUND-002 | SSS+ME | Production`
**Trigger:** Airtable Record Updated — Requests: Agent_Status changed to AI_RESPONDING
**Autonomy Tier:** A (generates draft) → B (Luciana reviews and sends)
**Priority:** HIGH

### Purpose
When Luciana marks a Request record Agent_Status = AI_RESPONDING, assemble client context and invoke Claude to generate a first-response draft. Write draft to Conversations table. Alert Luciana in Slack with draft for review.

### Module Sequence

```
[1] Airtable Watch Records (Trigger)
    - Table: Requests (tblTlSB9CO4dTGodg)
    - Filter: Agent_Status = AI_RESPONDING AND Environment = Production

[2] Validate Pre-Conditions
    - Check: Automations_Paused ≠ true on linked Booking (if exists)
    - Check: HV_Client flag — if true, escalate to Tier B regardless of content
    - Check: Emergency_Flag on any linked Booking — if true, STOP
    - If any check fails: log to Audit Log, DM Luciana

[3] Fetch Client Intelligence
    - Airtable Search: Clients table by email match
    - Fields to retrieve: Name, HV_Client, Charter_History_Count, Preference_Notes

[4] Fetch Operational Memory — Active Lessons
    - Table: Lessons (tblAben0zR8spPPhE)
    - Filter: AI_Prompt_Tag CONTAINS brand, Severity IN [HIGH, CRITICAL], Approved = true
    - Sort: Severity DESC, Created_At DESC
    - Limit: 5 records

[5] Fetch Production Prompt Version
    - Table: AI_Prompt_Versions
    - Filter: Status = LIVE AND Brand = {{brand}}
    - Return: Prompt_Content, Version_ID

[6] Assemble Claude Context Package
    Context modules (in order):
    1. Brand Router Confirmation: {{brand}}
    2. Client Intelligence: name, occasion, group_size, city, message, HV flag
    3. Operational Memory: lessons from step 4
    4. Booking State: Status = NEW / AVAILABILITY_PENDING (if linked)
    5. System Prompt: from AI_Prompt_Versions
    6. Task Instruction: "Generate first-response draft for this inquiry.
       Do not reference pricing unless Package explicitly confirmed.
       Do not reference specific vessel assignment.
       Do not make availability claims."

[7] HTTP Request — Claude API
    - Model: claude-sonnet-4-6 (or current production version from AI_Prompt_Versions)
    - Max tokens: 800
    - System: {{step5.prompt_content}}
    - User: {{step6.assembled_context}}
    - Temperature: 0 (deterministic brand voice)

[8] Write Draft to Conversations Table
    - Table: Conversations (tblhMocOusidgd3N0)
    - Fields: Brand, Request_Record_ID, Draft_Content, Status = PENDING_REVIEW,
      AI_Prompt_Version_ID, Generated_At = NOW(), Source_System = Make

[9] Update Request Record
    - Table: Requests
    - Fields: Agent_Status = HUMAN_REVIEW, Last_AI_Action = NOW(),
      AI_Confidence_Score = {{claude_response.confidence if available}}

[10] Audit Log Entry
    - Action = AI_DRAFT_GENERATED, Entity = Conversations,
      Prompt_Version = {{step5.version_id}}, Brand = {{brand}}

[11] Slack Alert to Luciana
    - Channel: DM to Luciana
    - Message:
      📝 AI DRAFT READY — [Brand]
      Request: {{request_id}}
      Client: {{name}}
      Draft Preview: {{first_200_chars_of_draft}}
      [Review in Airtable] | [Approve & Send] | [Edit]
    - Note: Luciana manually sends from Conversations record — Make does NOT auto-send

[12] Error Handler
    - On failure: Revert Request.Agent_Status to HUMAN_REVIEW
    - Log failure to Automation_Failures
    - Retry logic: 2 min, 5 min
    - After 2 failures: DM Luciana — "AI draft failed, please respond manually"
```

---

## SCENARIO 3 — BOOKING-001

**Name:** `BOOKING-001 | SSS+ME | Production`
**Trigger:** Airtable Record Updated — Bookings: Status changed to AVAILABILITY_CONFIRMED
**Autonomy Tier:** A
**Priority:** CRITICAL PATH

### Purpose
When Luciana or Will confirms availability on a booking, automatically generate a Stripe deposit payment link and send it to the client via Gmail and Quo SMS. Alert team in Slack.

### Module Sequence

```
[1] Airtable Watch Records (Trigger)
    - Table: Bookings (tbl72omPibBkn2hZL)
    - Filter: Status = AVAILABILITY_CONFIRMED AND Environment = Production

[2] Validate Pre-Conditions
    - Check: Automations_Paused ≠ true
    - Check: Emergency_Flag ≠ true
    - Check: Client email present
    - Check: Package_Price > 0
    - Check: Charter_Date is in the future
    - If any check fails: Log failure, DM Luciana with specific failure reason

[3] Idempotency Check
    - Audit Log search: Booking_ID = {{booking_id}} AND Action = DEPOSIT_LINK_SENT
    - If found: STOP — do not generate duplicate link
    - Log: DUPLICATE_PREVENTION_TRIGGERED

[4] Stripe — Create Payment Link
    - Mode: Production (never sandbox in production run)
    - Amount: {{Package_Price * 0.50}} (50% deposit) — confirm deposit_pct field
    - Currency: USD
    - Metadata: booking_id={{booking_id}}, client_email={{email}}, brand={{brand}}
    - Payment link description: "She Said Sail — Charter Deposit [BK-YYYY-NNNN]"
    - Save: Stripe_Payment_Link → Booking record (Stripe_Deposit_Link field)

[5] Update Airtable — Booking Record
    - Status: DEPOSIT_SENT
    - Stripe_Deposit_Link: {{step4.payment_link_url}}
    - Deposit_Sent_At: NOW()
    - Source_System: Make

[6] Send Gmail — Deposit Request
    - From: hello@shesaidsail.com (SSS) / hello@mareexecutive.com (ME)
    - To: {{client_email}}
    - Subject: "Your charter is almost confirmed — [Brand]"
    - Body: Approved template including:
      - Booking summary (date, vessel, package name, group size)
      - Deposit amount and payment link
      - What happens next
      - Contact for questions
    - Do NOT include: final balance amount in this message

[7] Send Quo SMS — Deposit Notification
    - To: {{client_phone}}
    - Message (SSS): "Hi {{first_name}} — your She Said Sail charter is almost locked in!
      Your deposit link is ready: {{stripe_link}}.
      Questions? Reply to this message or email hello@shesaidsail.com"
    - Char limit: 160 max per segment — verify before send

[8] Audit Log Entry
    - Action = DEPOSIT_LINK_SENT, Entity = Bookings,
      Record_ID = {{booking_id}}, Stripe_Link = {{link}}, Brand = {{brand}}

[9] Slack Alert — #sss-ops-bookings
    - Message:
      💳 DEPOSIT LINK SENT — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Date: {{charter_date}}
      Deposit Amount: ${{deposit_amount}}
      Link expires: [Stripe default]

[10] Error Handler
    - On Stripe failure: Revert Booking.Status to AVAILABILITY_CONFIRMED
    - Log failure to Automation_Failures
    - DM Luciana: "BOOKING-001 FAILED — Stripe link not generated for {{booking_id}}"
    - Retry: 2 min, 5 min — Stripe retries only (not email/SMS)
```

### Deposit Percentage Logic
Default: 50% deposit. Check for `Deposit_Pct` field on Booking record — if populated, use that value. If field missing, use 50%.

---

## SCENARIO 4 — BOOKING-002

**Name:** `BOOKING-002 | SSS+ME | Production`
**Trigger:** Stripe Webhook — `payment_intent.succeeded` OR `checkout.session.completed`
**Autonomy Tier:** A
**Priority:** CRITICAL PATH

### Purpose
When Stripe confirms a deposit payment, update Booking status to DEPOSIT_PAID, send client confirmation, alert team in Slack.

### Module Sequence

```
[1] Webhook (Trigger)
    - Method: POST
    - Endpoint: https://hook.make.com/[workspace]/sss-booking-002-stripe-deposit-production
    - Stripe webhook signing secret validation: MANDATORY first step
    - Event filter: payment_intent.succeeded OR checkout.session.completed
    - Reject non-matching events with 200 (acknowledged, not processed)

[2] Extract Booking ID from Stripe Metadata
    - Source: event.data.object.metadata.booking_id
    - If missing: log to Automation_Failures, alert Luciana —
      "Stripe deposit received but no booking_id in metadata"
    - STOP if booking_id not found

[3] Idempotency Check
    - Audit Log: Booking_ID = {{booking_id}} AND Action = DEPOSIT_RECEIVED
    - If found: STOP — already processed
    - Log: DUPLICATE_STRIPE_WEBHOOK_IGNORED

[4] Fetch Booking Record — Airtable
    - Table: Bookings
    - Get record by booking_id
    - Verify: Status = DEPOSIT_SENT (expected state)
    - If Status ≠ DEPOSIT_SENT: log anomaly to Audit Log,
      alert Luciana — "Deposit received for booking in unexpected status: {{current_status}}"
      STOP — do not write until Luciana clears

[5] Update Airtable — Booking Record
    - Status: DEPOSIT_PAID
    - Deposit_Received_At: NOW()
    - Stripe_Payment_Intent_ID: {{event.payment_intent_id}}
    - Deposit_Amount_Received: {{event.amount / 100}} (Stripe sends cents)
    - Source_System: Stripe → Make

[6] Audit Log Entry
    - Action = DEPOSIT_RECEIVED, Entity = Bookings,
      Stripe_Payment_Intent = {{payment_intent_id}},
      Amount = {{deposit_amount}}, Brand = {{brand}}

[7] Send Gmail — Deposit Confirmation
    - From: {{brand_email}}
    - To: {{client_email}}
    - Subject: "Your deposit is confirmed — [Brand]"
    - Body: Approved template:
      - Booking ID, date, vessel, package
      - Deposit amount confirmed
      - Next steps (agreement if >$5k, balance reminder, what to expect)
      - Emergency contact

[8] Slack Alert — #sss-ops-bookings
    - Message:
      ✅ DEPOSIT RECEIVED — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Amount Received: ${{deposit_amount}}
      Charter Date: {{charter_date}}
      Next: Agreement check → then CONFIRMED

[9] Trigger Agreement Check (see BOOKING-003)
    - If Total_Package_Price > 5000 AND Agreement_Signed ≠ true:
      → Pass to BOOKING-003 logic inline (or trigger separate scenario)

[10] Error Handler
    - On Airtable write failure: Retry 2 min, 5 min
    - Alert Luciana if Airtable write fails after retry
    - Email/SMS send failures: Log and alert — do NOT retry client messages automatically
    - Stripe webhook acknowledged (200 response) regardless of processing outcome
```

### Stripe Webhook Signing Validation
```
Make: Webhook module → Custom headers → Stripe-Signature
Validation: HMAC-SHA256(payload, stripe_webhook_secret)
If invalid: Return 401, log to Automation_Failures, alert Luciana
```

---

## SCENARIO 5 — BOOKING-003

**Name:** `BOOKING-003 | SSS+ME | Production`
**Trigger:** Airtable Record Updated — Bookings: Status = DEPOSIT_PAID AND Agreement_Signed = false AND Package_Price > 5000
**Autonomy Tier:** A (alert only — no client message)
**Priority:** HIGH

### Purpose
Alert Luciana that a signed agreement is required before this booking can advance to CONFIRMED. Block automated confirmation until Agreement_Signed = true.

### Module Sequence

```
[1] Airtable Watch Records (Trigger)
    - Table: Bookings
    - Filter: Status = DEPOSIT_PAID AND Agreement_Signed = false
             AND Package_Price > 5000 AND Environment = Production

[2] Idempotency Check
    - Audit Log: Booking_ID = {{booking_id}} AND Action = AGREEMENT_REQUIRED_ALERT_SENT
    - If found: STOP — already alerted

[3] Update Booking Record
    - Status: AGREEMENT_PENDING
    - Agreement_Alert_Sent_At: NOW()

[4] Audit Log Entry
    - Action = AGREEMENT_REQUIRED_ALERT_SENT, Entity = Bookings

[5] Slack Alert — Luciana DM + #sss-ops-bookings
    - Message:
      ⚠️ AGREEMENT REQUIRED — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Package Price: ${{price}}
      Charter Date: {{charter_date}}
      ACTION: Send DocuSign/agreement before marking CONFIRMED
      [Open in Airtable]

[6] Error Handler
    - Log to Automation_Failures on any failure
    - DM Will if Luciana cannot be reached
```

### Agreement Clearance Path
When Agreement_Signed is set to true on the Booking record, BOOKING-004 triggers.
No Make scenario manually polls for this — Airtable watch handles it.

---

## SCENARIO 6 — BOOKING-004

**Name:** `BOOKING-004 | SSS+ME | Production`
**Trigger:** Airtable Record Updated — Bookings: Status changed to CONFIRMED
**Autonomy Tier:** A (confirmation email) + A (Charter Brief generation)
**Priority:** CRITICAL PATH

### Purpose
When a booking reaches CONFIRMED status (set by Luciana or Will after Agreement_Signed = true), send confirmation email to client with full charter summary. Generate Charter Brief for operational handoff.

### Module Sequence

```
[1] Airtable Watch Records (Trigger)
    - Table: Bookings
    - Filter: Status = CONFIRMED AND Environment = Production

[2] Validate Pre-Conditions
    - Check: Automations_Paused ≠ true
    - Check: Emergency_Flag ≠ true
    - Check: Agreement_Signed = true (required gate — alert if missing)
    - Check: Client email present
    - Check: Yacht record linked and populated
    - Check: Package record linked and populated
    - Fail-fast: if any check fails, DM Luciana with specific failure

[3] Idempotency Check
    - Audit Log: Booking_ID = {{booking_id}} AND Action = CONFIRMATION_EMAIL_SENT
    - If found: STOP

[4] Fetch Related Records
    - Fetch: Clients.Name, Clients.Email, Clients.Phone
    - Fetch: Yachts.Vessel_Name, Yachts.Marina, Yachts.Slip_Number
    - Fetch: Packages.Package_Name, Packages.Duration, Packages.F&B_Standard
    - Fetch: Cities.City_Manager_Name, Cities.Emergency_Contact
    - Fetch: Brokers.Broker_Name (if applicable)

[5] Send Gmail — Booking Confirmation
    - From: {{brand_email}}
    - To: {{client_email}}
    - Subject: "You're confirmed — [Brand] [Occasion] Charter"
    - Body: Approved template including:
      - Booking ID
      - Charter date, time, boarding location
      - Vessel name
      - Package name, duration, inclusions
      - Group size
      - What to bring / what to expect
      - Balance due reminder (not specific amount in this message)
      - Emergency contact

[6] Generate Charter Brief — Claude
    - Assemble: all fields from Section 5.2 of Systems Intelligence Architecture
    - Claude Task: "Format this booking data into the standard She Said Sail Charter Brief.
      Do not invent or add any information not present in the provided data.
      If any required field is missing, insert: [MISSING — ALERT LUCIANA]"
    - Write output to: Charter_Brief field on Booking record
    - Set: Charter_Brief_Generated_At = NOW()

[7] Notify Luciana — Charter Brief Ready
    - Slack DM:
      📋 CHARTER BRIEF GENERATED — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Charter Date: {{charter_date}}
      [Review Brief in Airtable]
      Next: T-14 send to city manager

[8] Audit Log Entry
    - Action = BOOKING_CONFIRMED_EMAIL_SENT + CHARTER_BRIEF_GENERATED
    - Entity = Bookings, Prompt_Version = {{claude_prompt_version}}

[9] Slack Alert — #sss-ops-bookings
    - Message:
      🎉 BOOKING CONFIRMED — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Charter Date: {{charter_date}}
      Vessel: {{vessel_name}}
      Package: {{package_name}}

[10] Error Handler
    - Charter Brief generation failure: Log, DM Luciana — "Manual brief required"
    - Email failure: Retry 2 min — if still fails, DM Luciana to send manually
    - Log all failures to Automation_Failures
```

---

## SCENARIO 7 — EMERGENCY-001

**Name:** `EMERGENCY-001 | SSS+ME | Production`
**Trigger:** Airtable Record Updated — Bookings: Emergency_Flag changed to true
**Autonomy Tier:** A (alerting only — no client messages permitted)
**Priority:** CRITICAL — Must respond within 60 seconds

### Purpose
When Emergency_Flag is set to true on any Booking record, immediately pause all automations for that booking, alert Will and Luciana, create Emergency Escalation and Founder Decision records, and post to #sss-emergency-ops. No client-facing messages are sent under any circumstances.

### Module Sequence

```
[1] Airtable Watch Records (Trigger)
    - Table: Bookings
    - Filter: Emergency_Flag = true AND Automations_Paused ≠ true
              AND Environment = Production
    - Poll frequency: Every 1 minute (do not rely on webhook alone)

[2] Immediately — Set Automations_Paused = true
    - Table: Bookings
    - Field: Automations_Paused = true
    - CRITICAL: This write happens BEFORE any other action.
      If this write fails, retry immediately. No other step proceeds until confirmed.

[3] Cancel Any Pending Scheduled Messages
    - Check Automation_Health for any queued sends on this Booking_ID
    - Set: All pending send records → Status = CANCELLED_EMERGENCY
    - Log: EMERGENCY_AUTOMATION_CANCELLED for each

[4] Create Emergency Escalation Record
    - Table: Emergency_Escalations
    - Fields:
      | Field              | Value                                    |
      |--------------------|------------------------------------------|
      | Booking_ID         | {{booking_id}}                           |
      | Client_Name        | {{client_name}}                          |
      | Charter_Date       | {{charter_date}}                         |
      | Flag_Set_By        | {{modified_by OR unknown}}               |
      | Flag_Set_At        | NOW()                                    |
      | Status             | ACTIVE                                   |
      | Brand              | {{brand}}                                |
      | City               | {{city}}                                 |
      | Environment        | Production                               |
      | Escalation_Level   | 1 (initial — Will escalates if needed)   |

[5] Create Founder Decision Record
    - Table: Founder Decisions
    - Fields:
      | Field             | Value                              |
      |-------------------|------------------------------------|
      | Decision_Type     | EMERGENCY                          |
      | Booking_ID        | {{booking_id}}                     |
      | Status            | PENDING_WILL_REVIEW                |
      | Priority          | CRITICAL                           |
      | Triggered_By      | EMERGENCY-001 Make Scenario        |
      | Created_At        | NOW()                              |
      | SLA               | 30 minutes                         |

[6] Audit Log Entry
    - Action = EMERGENCY_TRIGGERED, Entity = Bookings,
      Sub-action = AUTOMATIONS_PAUSED

[7] Slack DM — Will (immediate)
    - Message:
      🚨 EMERGENCY TRIGGERED — [Brand]
      Booking: {{booking_id}}
      Client: {{client_name}}
      Charter Date: {{charter_date}}
      City: {{city}}
      Automations: PAUSED ✅
      Founder Decision Created: {{fd_record_id}}
      ACTION REQUIRED: Review and clear Emergency_Flag when resolved.
      [Open Booking] | [Open Emergency Record] | [Open Founder Decision]

[8] Slack DM — Luciana (immediate)
    - Same message as Will with note:
      "Will has been notified. Await Will's direction before any client contact."

[9] Slack Post — #sss-emergency-ops
    - Message:
      🚨 EMERGENCY ACTIVE — [Brand] — {{booking_id}}
      All automations paused. Will + Luciana notified.
      Charter Date: {{charter_date}}
      DO NOT contact client until Will clears.

[10] Error Handler
    - If step 2 (Automations_Paused write) fails: Retry every 30 seconds × 10
    - If still failing after 10 attempts: SMS Will directly via Quo
    - Log all failures to Automation_Failures immediately
    - No retry on Slack alerts — just log and continue
```

### Emergency Clearance Path
Emergency_Flag can only be set to false by Will. When cleared:
1. Automations_Paused is manually reviewed and cleared by Will
2. Emergency Escalation record Status updated to RESOLVED
3. Founder Decision record updated with resolution notes
4. Team notified via Slack that emergency is cleared

---

## SCENARIO 8 — AUDIT-001

**Name:** `AUDIT-001 | SSS+ME | Production`
**Trigger:** Called by every other Stage 1 scenario — inline module, not standalone scenario
**Autonomy Tier:** A (mandatory — no exceptions)
**Priority:** CRITICAL — Governs all automation integrity

### Purpose
Write an immutable audit log entry before any Tier A autonomous action is considered complete. The Audit Log is the institutional record of all Make actions. No scenario completes successfully without writing to it.

### Implementation Pattern

AUDIT-001 is not a separate Make scenario. It is a standardized module block inserted into every other scenario at the designated audit step. The standardization ensures:
- No scenario can complete without audit write
- Every entry contains the same required fields
- Failures in the audit write trigger immediate escalation

### Audit Log Record — Required Fields

| Field | Type | Source |
|-------|------|--------|
| Record_ID | Formula: AUD-YYYY-NNNN | Auto-generated |
| Action | Single Select | Hardcoded per scenario (see below) |
| Entity | Single Select | Table name that was acted on |
| Entity_Record_ID | Text | Record ID of the affected record |
| Scenario_Name | Text | Exact Make scenario name |
| Scenario_ID | Text | Make internal scenario ID |
| Brand | Single Select: SSS / ME | From router or booking context |
| City | Single Select | From booking context |
| Environment | Single Select: Production / Sandbox | Hardcoded per scenario environment |
| Source_System | Single Select: Make | Always "Make" for automated entries |
| AI_Prompt_Version_ID | Text | AIV-NNNN if AI was invoked; N/A otherwise |
| Timestamp | DateTime | NOW() — immutable |
| Operator | Text | "MAKE_AUTOMATION" for all autonomous actions |
| Notes | Long Text | Additional context specific to action |
| Idempotency_Key | Text | Key used in duplicate check |
| Success | Checkbox | True if action succeeded |

### Standard Action Values by Scenario

| Scenario | Action Values |
|----------|--------------|
| INBOUND-001 | INBOUND_LEAD_RECEIVED, DUPLICATE_PREVENTION_TRIGGERED |
| INBOUND-002 | AI_DRAFT_GENERATED, AI_DRAFT_FAILED |
| BOOKING-001 | DEPOSIT_LINK_SENT, DEPOSIT_LINK_DUPLICATE_BLOCKED |
| BOOKING-002 | DEPOSIT_RECEIVED, DUPLICATE_STRIPE_WEBHOOK_IGNORED, DEPOSIT_STATE_ANOMALY |
| BOOKING-003 | AGREEMENT_REQUIRED_ALERT_SENT |
| BOOKING-004 | BOOKING_CONFIRMED_EMAIL_SENT, CHARTER_BRIEF_GENERATED |
| EMERGENCY-001 | EMERGENCY_TRIGGERED, EMERGENCY_AUTOMATION_CANCELLED, AUTOMATIONS_PAUSED |
| ALL | SCENARIO_FAILURE_LOGGED |

### Audit Write Failure Protocol
If the Audit Log write itself fails:
1. Retry immediately × 3
2. If all retries fail: DM Will and Luciana — "CRITICAL: Audit Log write failed for [scenario] on [record_id]"
3. The triggering action is considered INCOMPLETE until audit log confirms write
4. Create Automation_Failures record manually if Audit Log is unavailable

---

## AIRTABLE FIELD DEPENDENCY MAP — STAGE 1

All scenarios in Stage 1 depend on the following fields being present and correctly typed.

### Bookings Table (tbl72omPibBkn2hZL)
| Field Name | Type | Required By |
|------------|------|-------------|
| Status | Single Select | ALL scenarios |
| Emergency_Flag | Checkbox | EMERGENCY-001, all pre-condition checks |
| Automations_Paused | Checkbox | All scenarios (pre-condition) |
| Agreement_Signed | Checkbox | BOOKING-003, BOOKING-004 |
| Package_Price | Currency | BOOKING-001, BOOKING-003 |
| Deposit_Pct | Number | BOOKING-001 |
| Stripe_Deposit_Link | URL | BOOKING-001 (write), client-facing |
| Stripe_Payment_Intent_ID | Text | BOOKING-002 (write) |
| Deposit_Amount_Received | Currency | BOOKING-002 (write) |
| Deposit_Sent_At | DateTime | BOOKING-001 (write) |
| Deposit_Received_At | DateTime | BOOKING-002 (write) |
| Charter_Brief | Long Text | BOOKING-004 (write) |
| Charter_Brief_Generated_At | DateTime | BOOKING-004 (write) |
| Agreement_Alert_Sent_At | DateTime | BOOKING-003 (write) |
| HV_Client | Checkbox | INBOUND-002, BOOKING-004 |
| Brand | Single Select | ALL scenarios |
| Environment | Single Select | ALL scenarios (filter) |
| Source_System | Single Select | ALL scenarios (write) |

### Requests Table (tblTlSB9CO4dTGodg)
| Field Name | Type | Required By |
|------------|------|-------------|
| Agent_Status | Single Select | INBOUND-001 (write), INBOUND-002 (trigger) |
| Last_AI_Action | DateTime | INBOUND-002 (write) |
| AI_Confidence_Score | Number | INBOUND-002 (write) |
| Escalation_Reason | Long Text | INBOUND-002 (write if escalated) |
| Environment | Single Select | ALL (filter) |
| Brand | Single Select | ALL (router write) |
| Source_System | Single Select | INBOUND-001 (write) |

### Audit Log Table (tblrMpTfMk8q1eNHp)
| Field Name | Type | Required By |
|------------|------|-------------|
| Action | Single Select | AUDIT-001 |
| Entity | Single Select | AUDIT-001 |
| Entity_Record_ID | Text | AUDIT-001 |
| Scenario_Name | Text | AUDIT-001 |
| Brand | Single Select | AUDIT-001 |
| Environment | Single Select | AUDIT-001 |
| AI_Prompt_Version_ID | Text | INBOUND-002 |
| Idempotency_Key | Text | AUDIT-001 |
| Success | Checkbox | AUDIT-001 |

---

## SLACK CHANNEL MAP — STAGE 1

| Channel | Purpose | Scenarios |
|---------|---------|-----------|
| #sss-new-leads | New inbound lead alerts | INBOUND-001 |
| #sss-ops-bookings | Booking lifecycle events | BOOKING-001, BOOKING-002, BOOKING-003, BOOKING-004 |
| #sss-emergency-ops | Emergency alerts only | EMERGENCY-001 |
| #sss-ops-alerts | System failures and anomalies | All error handlers |
| Luciana DM | Operational decisions needed | BOOKING-001-004, EMERGENCY-001 |
| Will DM | Emergency + SEV-2+ failures | EMERGENCY-001, failure escalations |

---

## EMAIL TEMPLATE REGISTRY — STAGE 1

| Template | Scenario | Brand | Status |
|----------|---------|-------|--------|
| Auto-reply — SSS | INBOUND-001 | SSS | REQUIRED — draft in Airtable or Make |
| Auto-reply — ME | INBOUND-001 | ME | REQUIRED — draft in Airtable or Make |
| Deposit Request — SSS | BOOKING-001 | SSS | REQUIRED |
| Deposit Request — ME | BOOKING-001 | ME | REQUIRED |
| Deposit Confirmation — SSS | BOOKING-002 | SSS | REQUIRED |
| Deposit Confirmation — ME | BOOKING-002 | ME | REQUIRED |
| Booking Confirmation — SSS | BOOKING-004 | SSS | REQUIRED |
| Booking Confirmation — ME | BOOKING-004 | ME | REQUIRED |

All templates must be approved by Will before production activation. No placeholder text may be sent to a live client.

---

## STRIPE CONFIGURATION — STAGE 1

| Item | Value |
|------|-------|
| Webhook Endpoint | https://hook.make.com/[workspace]/sss-booking-002-stripe-deposit-production |
| Events to Subscribe | payment_intent.succeeded, checkout.session.completed |
| Signing Secret | Stored in Make credential vault — never in GitHub |
| Metadata Required | booking_id, client_email, brand |
| Test Mode Endpoint | Separate Make scenario — sandbox environment only |

---

## MAKE ENVIRONMENT CONFIGURATION

| Setting | Value |
|---------|-------|
| Production Base | appdZ49WqgjRXxA1R |
| Sandbox Base | SSS Sandbox base ID (create if not existing) |
| Stripe Test Mode | Separate webhook endpoint with sandbox Make scenario |
| Claude API Key | Stored in Make credential vault |
| Quo SMS API Key | Stored in Make credential vault |
| Gmail OAuth | hello@shesaidsail.com — OAuth connected |
| Slack OAuth | Workspace app — OAuth connected |

---

## ROLLBACK PROCEDURES — STAGE 1

### INBOUND-001 Rollback
1. Disable webhook in Make (toggle off)
2. Delete Airtable test records created during bad run
3. Re-enable after fix validated in sandbox

### BOOKING-001 Rollback
1. If Stripe link created but status not updated: Manually set Status = AVAILABILITY_CONFIRMED
2. Disable scenario in Make
3. Luciana sends deposit link manually from Stripe dashboard
4. Re-enable after fix

### BOOKING-002 Rollback
1. Do NOT refund Stripe payment — financial event is immutable
2. If Airtable not updated: Manually set Status = DEPOSIT_PAID
3. Send confirmation email manually from Gmail
4. Log rollback action in Audit Log and Founder Decisions

### EMERGENCY-001 Rollback
No rollback. If Emergency_Flag was set in error:
1. Will sets Emergency_Flag = false
2. Will sets Automations_Paused = false
3. Will logs Founder Decision: EMERGENCY_CLEARED_FALSE_ALARM
4. Team notified in #sss-emergency-ops

---

## FINAL VERDICT — STAGE 1 BUILD

> **READY WITH WARNINGS**

All 8 scenarios are architecturally complete and ready for sandbox build and testing. Production promotion is blocked pending:

1. **Email templates not drafted** — 8 client-facing templates required before any live send
2. **Airtable field gaps** — Several required fields confirmed missing; must be added before scenario activation (see STAGE_1_OPEN_ISSUES.md)
3. **Make credential vault not confirmed** — Stripe signing secret, Quo SMS key, Claude API key must be stored and tested
4. **Sandbox base not confirmed** — SSS Sandbox base needed for test runs without contaminating production
5. **Webhook URLs not yet generated** — Require Make scenario creation before URLs exist

Scenarios are ready to build. Production go-live requires all warnings resolved.

---

*Document generated from authority documents as listed above. No scenario spec in this document supersedes the Systems Intelligence Architecture v2.0 PRODUCTION. In case of conflict, the Systems Intelligence Architecture governs.*
