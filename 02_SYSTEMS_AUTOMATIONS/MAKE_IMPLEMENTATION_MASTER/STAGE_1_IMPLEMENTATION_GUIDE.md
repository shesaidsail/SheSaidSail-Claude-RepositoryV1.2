# STAGE_1_IMPLEMENTATION_GUIDE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Stage:** 1 — Core Operational MVP
**Goal:** Safe, revenue-generating operational core. Ads can run when this stage is complete.
**Classification:** Confidential — Internal Use Only

---

## STAGE 1 OVERVIEW

Stage 1 creates the minimum viable operational automation layer required to run paid advertising safely. When Stage 1 is fully deployed, tested, and confirmed:

- Every inbound lead from every channel is captured in Airtable automatically
- Every lead is classified as SSS or ME before any processing
- Bookings are created from confirmed requests
- Stripe deposit links are generated and sent
- Deposit confirmations trigger booking confirmation
- Concierge assignment is notified
- Basic charter lifecycle messages are delivered
- Post-charter review requests are sent when eligible

Stage 1 does NOT include: yacht availability locking, charter briefs, vendor notifications, or intelligence layers. Those are Stage 2 and Stage 3.

---

## PRE-STAGE 1 AIRTABLE REQUIREMENTS

The following Airtable conditions must be confirmed true before any Stage 1 scenario is activated. These are hard blockers — not recommendations.

| Blocker | Required State | Verify Method |
|---------|---------------|---------------|
| Environment field on Bookings | Single Select: Production / Sandbox / Development | Open Bookings table, confirm field exists |
| Environment field on Requests | Same | Open Requests table |
| Automations_Paused field on Bookings | Checkbox, exists | Confirm in Bookings schema |
| Emergency_Flag on Bookings | Checkbox, exists | Confirm in Bookings schema |
| Idempotency_Key on Bookings | Single Line Text, exists | Must be added per Airtable build spec |
| D7_Review_Eligible on Bookings | Formula field — returns TRUE/FALSE | Must be added per Airtable build spec |
| AI_Prompt_Versions in main base | 26-field schema, Will_Approved and Status fields present | Airtable build spec Phase 4 |
| Stripe webhook endpoint URL documented | Documented in Make_Scenarios Airtable table | Will audits Stripe → Webhooks |
| Circular trigger audit completed | All Airtable-native automations on Bookings inventoried | Will audits Automation tab |

---

## SCENARIO 1: M-LEAD-INTAKE

**Purpose:** Capture every inbound lead from the website form and create an Airtable Request record. Notify Luciana via Slack.

**Trigger:** Webflow webhook (form submission to Make webhook URL)

**Module Sequence:**

```
1. Webhooks > Custom Webhook
   — Validates Authorization header (Bearer token)
   — Validates timestamp (reject if > 5 minutes old)
   — Parses form fields

2. Tools > Set Variable: idempotency_key
   — Value: SHA256(email + form_submitted_at)

3. Airtable > Search Records (Requests table)
   — Filter: {Idempotency_Key} = {{idempotency_key}}
   — If match found → skip to step 10 (exit, already processed)

4. [SUB-SCENARIO CALL] M-BRAND-ROUTER
   — Input: form source, form fields, referring URL
   — Output: Brand (SSS / ME), routing_confidence

5. Airtable > Create Record (Clients table)
   — Only if no existing Client record with same email
   — Fields: Name, Email, Phone, Brand, Source_System = Make, Environment = Production

6. Airtable > Create Record (Requests table)
   — Fields mapped below

7. Airtable > Update Record (Requests)
   — Set Idempotency_Key = {{idempotency_key}}

8. Slack > Create a Message (#sss-ops-leads or #me-ops-leads based on Brand)
   — Message format defined below

9. Airtable > Create Record (Audit_Log)
   — Fields mapped below

10. Webhooks > Response: 200 OK
```

**Airtable Field Mapping — Requests (tblTlSB9CO4dTGodg):**

| Make Variable | Airtable Field | Type |
|--------------|---------------|------|
| `{{form.first_name}} {{form.last_name}}` | Name | Text |
| `{{form.email}}` | Email | Email |
| `{{form.phone}}` | Phone | Phone |
| `{{form.charter_date}}` | Charter_Date | Date |
| `{{form.group_size}}` | Group_Size | Number |
| `{{form.occasion}}` | Occasion | Text |
| `{{form.notes}}` | Notes | Long Text |
| `SSS` or `ME` | Brand | Single Select |
| `{{form.source_channel}}` | Source_Channel | Single Select |
| `Make` | Source_System | Single Select |
| `Production` | Environment | Single Select |
| `NEW` | Status | Single Select |
| `{{now}}` | Created_At | DateTime |
| `{{idempotency_key}}` | Idempotency_Key | Text |

**Slack Message Format (#sss-ops-leads):**
```
🆕 NEW LEAD — [SSS/ME]
Name: {{form.first_name}} {{form.last_name}}
Date Requested: {{form.charter_date}}
Group: {{form.group_size}} guests
Occasion: {{form.occasion}}
Source: {{form.source_channel}}
→ View in Airtable: [Requests record link]
```

**Audit Log Entry:**
| Field | Value |
|-------|-------|
| Triggering_Event | Webflow form submission |
| Source_Data | Form payload summary |
| Output | Requests record ID created |
| Approval_State | AUTONOMOUS |
| Brand | Brand from router |
| Environment | Production |

**Failure Points:**
- Webflow sends duplicate submission → idempotency check prevents duplicate record
- Airtable API down → Step 3 fails → error handler (see ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md)
- Brand router returns ambiguous → log as ME if email domain is mare-related, else SSS; create Slack alert for Luciana to confirm

**Retry Logic:** Standard 4-failure chain per ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md

**Rollback:** Requests record created can be deleted manually. Client record deletion requires Will approval if PII was written. No outbound messages sent at this stage — rollback is safe.

**Test Procedure:**
1. Submit test form with Environment = Sandbox in a test Webflow form connected to a sandbox Make webhook
2. Confirm Request record created in Sandbox Airtable base (not production)
3. Confirm Slack message posted to #sss-ops-leads-sandbox channel
4. Confirm Audit Log entry created
5. Submit duplicate — confirm only one record exists

---

## SCENARIO 2: M-BRAND-ROUTER

**Purpose:** Classify every inbound request as SSS or ME with high confidence. This is called as a sub-flow within M-LEAD-INTAKE and directly in any scenario requiring brand context.

**Trigger:** Called by M-LEAD-INTAKE (not independently triggered)

**Classification Logic:**

```
1. Check referring URL:
   — shesaidsail.com → SSS
   — mareexecutive.com → ME
   — Ambiguous → proceed to step 2

2. Check form source field (if present):
   — SSS explicitly → SSS
   — ME explicitly → ME
   — Blank → proceed to step 3

3. Check occasion field:
   — Corporate / business / executive / retreat → ME
   — Bachelorette / birthday / girls trip / anniversary → SSS
   — Mixed or blank → proceed to step 4

4. Default assignment:
   — If referring URL contains "mare" or "executive" → ME
   — All others → SSS

5. Log classification confidence:
   — Direct URL match: HIGH
   — Source field match: HIGH
   — Occasion inference: MEDIUM
   — Default: LOW — create Slack alert for Luciana to verify
```

**Output Variables:**
- `brand` = "SSS" or "ME"
- `routing_confidence` = "HIGH" / "MEDIUM" / "LOW"

**Airtable Write:**
- Updates Requests.Brand field with classification result
- Writes Requests.Routing_Confidence field (add this field if not present)

**Failure Points:**
- All signals ambiguous → default to SSS + LOW confidence + Luciana alert
- Never block lead capture on brand ambiguity

**Operational Note:** Brand misrouting is a system failure. LOW confidence alerts must be reviewed by Luciana before any AI-generated outbound response is sent.

---

## SCENARIO 3: M-BOOKING-CREATION

**Purpose:** Create a Booking record when a Request is confirmed by Luciana (availability confirmed). Generate Stripe payment link and send deposit request.

**Trigger:** Airtable webhook — Requests table — Status field changes to `AVAILABILITY_CONFIRMED`

**Pre-Checks (Module 1):**
```
Read Requests record:
- Environment = Production? If not, EXIT.
- Brand confirmed? If missing, EXIT + Slack alert.
- Automations_Paused on linked Booking (if any)? If true, EXIT.
```

**Module Sequence:**

```
1. Airtable > Watch Records (Requests — Status = AVAILABILITY_CONFIRMED)

2. Airtable > Get Record: Requests (full record)

3. Airtable > Search Records: Bookings
   — Filter: {Request_ID} = {{request.id}}
   — If Booking already exists → log duplicate attempt → EXIT

4. Airtable > Get Record: Clients (linked from Request)

5. Airtable > Get Record: Packages (linked from Request)

6. Airtable > Get Record: Yachts (linked from Request)

7. Tools > Set Variable: deposit_amount
   — Formula: Package.Price × 0.5 (rounded to 2 decimal places)

8. Stripe > Create Payment Link
   — Amount: {{deposit_amount}}
   — Currency: USD
   — Description: "SSS Charter Deposit — {{client.name}} — {{charter_date}}"
   — Metadata:
     booking_source: make_m_booking_creation
     request_id: {{request.id}}
     client_id: {{client.id}}
     brand: {{brand}}
     charter_date: {{charter_date}}
     package_id: {{package.id}}
   — Success URL: shesaidsail.com/booking-confirmed
   — Return Stripe Payment Link URL

9. Airtable > Create Record: Bookings (tbl72omPibBkn2hZL)
   — Fields mapped below

10. Airtable > Update Record: Requests
    — Status → BOOKING_CREATED
    — Linked_Booking_ID → {{new_booking.id}}

11. Gmail > Send Email (deposit request to client)
    — Template: SSS_DEPOSIT_REQUEST or ME_DEPOSIT_REQUEST based on brand

12. Quo SMS > Send SMS (deposit link to client phone)
    — Template: SSS_DEPOSIT_SMS or ME_DEPOSIT_SMS based on brand

13. Slack > Post to #sss-ops-bookings (or #me-ops-bookings)
    — Booking created notification

14. Airtable > Create Record: Audit_Log
    — Full action record

15. Webhooks > Response: 200 OK
```

**Airtable Field Mapping — Bookings (tbl72omPibBkn2hZL):**

| Make Variable | Airtable Field | Type |
|--------------|---------------|------|
| `BK-{{year}}-{{sequence}}` | Booking_ID | Formula (set as readable ID) |
| `[Request record ID]` | Request_Link | Linked Record |
| `[Client record ID]` | Client_Link | Linked Record |
| `[Yacht record ID]` | Yacht_Link | Linked Record |
| `[Package record ID]` | Package_Link | Linked Record |
| `{{charter_date}}` | Charter_Date | Date |
| `{{group_size}}` | Group_Size | Number |
| `{{package.price}}` | Package_Price | Currency |
| `{{deposit_amount}}` | Deposit_Amount | Currency |
| `{{stripe_payment_link_url}}` | Stripe_Deposit_Link | URL |
| `DEPOSIT_SENT` | Status | Single Select |
| `{{brand}}` | Brand | Single Select |
| `{{city}}` | City | Single Select |
| `Make` | Source_System | Single Select |
| `Production` | Environment | Single Select |
| `false` | Emergency_Flag | Checkbox |
| `false` | Automations_Paused | Checkbox |
| `{{idempotency_key}}` | Idempotency_Key | Text |

**Stripe Metadata Structure:**
```json
{
  "booking_source": "make_m_booking_creation",
  "request_id": "REQ-2026-XXXX",
  "client_id": "CLT-XXXX",
  "brand": "SSS",
  "charter_date": "2026-06-15",
  "package_id": "[package_airtable_id]",
  "environment": "production"
}
```

**Failure Points:**
- Stripe API down → retry 4× → SEV-2 alert → Luciana creates link manually
- Package Price missing → EXIT + Luciana alert (never send a $0 link)
- Client phone missing → SMS skipped, email only; log in Audit_Log
- Circular trigger risk: ensure Airtable automation on Bookings table does NOT trigger on "record updated" generically — must be scoped to specific field

**Rollback:** Delete Booking record in Airtable. Stripe Payment Link can be deactivated in Stripe dashboard. Email and SMS cannot be recalled — document in Audit_Log.

---

## SCENARIO 4: M-STRIPE-DEPOSIT

**Purpose:** Handle the Stripe deposit payment_intent.succeeded webhook. Update Booking status and send confirmation.

**Note:** This scenario is triggered by Stripe directly, not by Airtable. The Stripe webhook is the trigger.

**Trigger:** Stripe webhook: `payment_intent.succeeded`

**Module Sequence:**

```
1. Webhooks > Custom Webhook (Stripe endpoint)
   — Validate Stripe-Signature header (signing secret)
   — Validate timestamp (reject if > 5 minutes old)
   — Check metadata.environment = "production" — if not, EXIT

2. Tools > Set Variable: booking_id_from_metadata
   — Extract from Stripe event metadata: request_id or booking_id

3. Airtable > Search Records: Bookings
   — Filter: {Idempotency_Key} = {{stripe_payment_intent_id}}
   — If found → EXIT (already processed)

4. Airtable > Search Records: Bookings
   — Filter: {Request_Link} = {{request_id}} OR {Booking_ID} = {{booking_id}}

5. Read: Emergency_Flag, Automations_Paused, Environment
   — If Emergency_Flag = true → EXIT, log, Slack alert
   — If Automations_Paused = true → EXIT, log

6. Airtable > Update Record: Bookings
   — Status → DEPOSIT_PAID
   — Deposit_Paid_At → {{now}}
   — Stripe_Payment_Intent_ID → {{payment_intent_id}}
   — Idempotency_Key → {{stripe_payment_intent_id}}

7. Gmail > Send Confirmation Email
   — Template: SSS_DEPOSIT_CONFIRMED or ME_DEPOSIT_CONFIRMED
   — Include: charter date, package summary, balance due date, next steps

8. Quo SMS > Send Confirmation SMS
   — Template: SSS_DEPOSIT_CONFIRMED_SMS

9. Slack > #sss-ops-bookings: "✅ DEPOSIT CONFIRMED — [Client Name] — [Charter Date] — $[Amount]"

10. Airtable > Create Record: Audit_Log

11. Webhooks > Response: 200 OK (required — Stripe retries on non-200)
```

**Failure Points:**
- Non-200 response to Stripe → Stripe retries up to 3 days. Idempotency check prevents duplicate processing.
- Booking record not found by payment metadata → SEV-2 alert → Luciana reconciles manually
- Client email missing → Slack alert to Luciana to send manually

**Rollback:** If deposit was received in error, refund via Stripe dashboard (Will approval required). Update Booking status manually.

---

## SCENARIO 5: M-BOOKING-CONFIRMATION

**Purpose:** When Booking reaches CONFIRMED status (after agreement signed, or at Will/Luciana's discretion for bookings under $5,000), send the formal charter confirmation to the client.

**Trigger:** Airtable webhook — Bookings table — Status field changes to `CONFIRMED`

**Module Sequence:**

```
1. Airtable > Watch Records: Bookings (Status = CONFIRMED)

2. Airtable > Get Record: full Booking record
   — Check: Environment = Production → else EXIT
   — Check: Emergency_Flag = false → else EXIT + log
   — Check: Automations_Paused = false → else EXIT + log
   — Check: HV_Client flag → if true, route to Luciana for human send (Tier B)

3. Airtable > Get Record: Client (linked)

4. Airtable > Get Record: Package (linked)

5. Airtable > Get Record: Yacht (linked)

6. If HV_Client = false:
   Gmail > Send Confirmation Email (Tier A — autonomous)
   — Template: SSS_BOOKING_CONFIRMED or ME_BOOKING_CONFIRMED
   — Include: booking ID, charter date, vessel name, group size, boarding location, what to expect, balance due date

7. If HV_Client = true:
   Slack > DM to Luciana
   — "HV client [Name] booking confirmed. Please send personal confirmation. Draft below."
   — Include pre-written draft for Luciana to send

8. Airtable > Update Record: Bookings
   — Confirmation_Sent_At → {{now}}
   — Status → CONFIRMED (no change needed — already set)

9. Slack > #sss-ops-bookings: "📋 CONFIRMED — [Client Name] — [Charter Date] — [Vessel] — [Package]"

10. Airtable > Create Record: Audit_Log
    — Approval_State = AUTONOMOUS (or HUMAN_REVIEWED if HV_Client)
```

**Failure Points:**
- HV_Client = true → Tier B flow → Luciana must send manually
- Client email missing → Slack alert to Luciana

---

## SCENARIO 6: M-CONCIERGE-ASSIGNMENT

**Purpose:** Notify the assigned concierge/city manager when a booking is confirmed and deposit paid.

**Trigger:** Airtable webhook — Bookings.Status → DEPOSIT_PAID

**Module Sequence:**

```
1. Watch: Bookings.Status = DEPOSIT_PAID

2. Get Record: Booking, City, Concierge_Operators (linked via City)

3. Check: Emergency_Flag, Automations_Paused

4. Slack > DM to City Manager (if Slack ID in Concierge_Operators record)
   — "New booking assigned: [Client Name] — [Date] — [Package] — [Vessel]"
   — Include: Airtable view link for the booking

5. Gmail > Email to City Manager (backup if Slack unavailable)

6. Airtable > Update Record: Bookings
   — Concierge_Notified_At → {{now}}

7. Audit_Log entry
```

**Failure Points:**
- City Manager Slack ID missing → email fallback → if email also missing → Luciana alert

---

## SCENARIO 7: M-BASIC-LIFECYCLE

**Purpose:** Daily scheduler that evaluates all active bookings and sends timed lifecycle messages.

**Trigger:** Schedule — daily at 7:00 AM (local time — set to EST as primary timezone)

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: Status IN [CONFIRMED, DEPOSIT_PAID, PAID, COMPLETED]
   — Filter: Environment = Production
   — Retrieve: Charter_Date, Status, Client_Link, D7_Review_Eligible,
               Emergency_Flag, Automations_Paused, HV_Client,
               D72hr_Reminder_Sent, D48hr_Reminder_Sent, D24hr_Reminder_Sent,
               D12hr_Reminder_Sent, D1_Sent, Balance_Paid
   — Max 100 records (paginate if needed)

2. For each Booking record:
   a. Check Emergency_Flag → skip if true, log skip
   b. Check Automations_Paused → skip if true, log skip
   c. Calculate days_until_charter = Charter_Date − today
   d. Calculate days_since_charter = today − Charter_Date

   OUTBOUND DECISION TREE:

   T-72hrs (days_until_charter = 3):
   — If D72hr_Reminder_Sent = false AND Status IN [CONFIRMED, DEPOSIT_PAID, PAID]:
     → Send balance due reminder email + SMS
     → Generate Stripe balance payment link (if Status ≠ PAID)
     → Set D72hr_Reminder_Sent = true

   T-48hrs (days_until_charter = 2):
   — If D48hr_Reminder_Sent = false:
     → Send 48hr logistics email (boarding, parking, what to bring)
     → Set D48hr_Reminder_Sent = true

   T-24hrs (days_until_charter = 1):
   — If D24hr_Reminder_Sent = false:
     → Send 24hr reminder with weather note placeholder
     → Set D24hr_Reminder_Sent = true

   T-12hrs (days_until_charter = 0.5 — morning of):
   — If D12hr_Reminder_Sent = false AND Charter_Date = today:
     → Send day-of message (final boarding details)
     → Set D12hr_Reminder_Sent = true

   D1 (days_since_charter = 1):
   — If D1_Sent = false AND Status = COMPLETED:
     → Send D1 warmth message ("We hope you had an incredible time...")
     → Set D1_Sent = true

3. For each message sent:
   — Create Audit_Log entry

4. Slack > #sss-ops-alerts: daily summary of lifecycle actions taken
```

**Failure Points:**
- Booking with Charter_Date today and Emergency_Flag = true → skip all messages + Luciana alert
- Stripe balance link generation fails → send reminder without link + Luciana alert to send manually
- Rate limiting: if more than 30 bookings in the schedule window, paginate and throttle (500ms delay between sends)

**Rollback:** Cannot un-send messages. Flag in Audit_Log. Luciana notified to manage client expectations if message was sent in error.

---

## SCENARIO 8: M-REVIEW-REQUEST

**Purpose:** Send Google Review request to eligible clients 7 days after charter.

**Trigger:** Schedule — daily at 7:00 AM (same schedule run as M-BASIC-LIFECYCLE, separate scenario for clarity)

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: days_since_charter = 7 (Charter_Date = today - 7 days)
   — Filter: D7_Review_Eligible = true
   — Filter: D7_Review_Sent = false (field: D7_Sent)
   — Filter: Status = COMPLETED
   — Filter: Environment = Production

2. For each eligible Booking:
   a. Check Emergency_Flag → skip if true
   b. Check Automations_Paused → skip if true
   c. Check HV_Client:
      — HV_Client = false → send autonomous review request (Tier A)
      — HV_Client = true → Slack DM to Luciana for personal review follow-up

3. Gmail > Send Review Request Email
   — Template: SSS_REVIEW_REQUEST or ME_REVIEW_REQUEST
   — Include: personalized thank you, Google Review link, gentle ask

4. Quo SMS > Send Review SMS (if phone on file)

5. Airtable > Update Record: Bookings
   — D7_Sent = true
   — D7_Sent_At = {{now}}

6. Audit_Log entry
```

**D7_Review_Eligible Formula (must exist in Airtable):**
```
AND(
  Charter_Grade != "D",
  Charter_Grade != "F",
  Emergency_Flag = false,
  Chargeback_Risk != "HIGH",
  Chargeback_Risk != "ACTIVE"
)
```

**Failure Points:**
- D7_Review_Eligible = false for booking → skip silently (no message, no alert — expected)
- Client email missing → SMS only; if SMS also missing → log in Audit_Log

---

## STAGE 1 DEPLOYMENT ORDER

See MAKE_DEPLOYMENT_ORDER.md for the exact sequence. Stage 1 scenarios deploy in this order:

1. M-BRAND-ROUTER (test in isolation first — no Airtable writes)
2. M-LEAD-INTAKE (with sandbox webhook)
3. M-STRIPE-DEPOSIT (with Stripe test mode)
4. M-BOOKING-CREATION (with sandbox Airtable)
5. M-BOOKING-CONFIRMATION (with sandbox Airtable)
6. M-CONCIERGE-ASSIGNMENT (with sandbox Slack channel)
7. M-BASIC-LIFECYCLE (with sandbox bookings)
8. M-REVIEW-REQUEST (with sandbox bookings)

Each scenario goes through: Sandbox build → Sandbox test → Founder approval → Production promotion → Live test with fake lead → Production activation.

---

## STAGE 1 SUCCESS CRITERIA

Stage 1 is complete and ads can run when ALL of the following are true:

- [ ] All 8 scenarios active in production Make
- [ ] Fake lead test completed: lead → Airtable → Stripe → confirmation → lifecycle messages → review request
- [ ] Zero duplicate records created in fake lead test
- [ ] Emergency_Flag pause test passed (set flag → confirm all outbound stopped)
- [ ] Brand routing test passed: SSS form → SSS channel, ME form → ME channel
- [ ] Stripe test mode completed before production Stripe credentials swapped
- [ ] All scenarios registered in Make_Scenarios Airtable table
- [ ] All scenario IDs documented
- [ ] Audit Log entries confirmed for every Tier A action in test
- [ ] Will has reviewed and approved each scenario's first production execution

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_1_IMPLEMENTATION_GUIDE v1.0*
*Effective May 2026*
