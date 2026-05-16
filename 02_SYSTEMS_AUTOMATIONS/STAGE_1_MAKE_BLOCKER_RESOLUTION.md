# STAGE_1_MAKE_BLOCKER_RESOLUTION.md
## She Said Sail + Mare Executive — Stage 1 Make + Credential Blocker Resolution

**Document Status:** FINAL  
**Audit Date:** 2026-05-16  
**Scope:** Make.com configuration blockers, credential connections, webhook registration, variable standardization  
**Branch:** claude/stage-1-blocker-resolution-QPy0o

---

## SCOPE OF THIS DOCUMENT

This document resolves Make-side and credential-side blockers for Stage 1 scenarios only:
- INBOUND-001: Webflow form → Airtable Request + Slack
- BOOKING-001: Availability confirmed → Stripe payment link + deposit request
- BOOKING-002: Stripe deposit webhook → Booking status update
- EMERGENCY-001: Emergency_Flag trigger → full pause + notifications
- AUDIT-001: Tier A action → Audit Log write

Scenarios not in Stage 1 scope: INBOUND-002 and beyond, CHARTER-001 through CHARTER-007, FINANCIAL-001 through FINANCIAL-003, INTELLIGENCE-001, OUTREACH-001, BACKUP-001, HEALTH-001.

---

## MAKE GOVERNANCE RULES — MANDATORY FOR ALL STAGE 1 SCENARIOS

These rules are non-negotiable. Every Stage 1 scenario must implement them before activation.

---

### MANDATORY PATTERN P-001: Automations_Paused + Emergency_Flag Read-First

**Every outbound client-facing Make scenario must implement this as its first functional step (after webhook validation):**

```
Step 1: Airtable — Get Record (Bookings, Booking_ID from trigger)
Step 2: Router or Filter
  IF Emergency_Flag = true:
    → Write to Automation_Health: Status = PAUSED_EMERGENCY, Booking_ID, Scenario_ID, Timestamp
    → Stop scenario execution (no client message sent)
  IF Automations_Paused = true:
    → Write to Automation_Health: Status = PAUSED_MANUAL, Booking_ID, Scenario_ID, Timestamp
    → Stop scenario execution
Step 3: Continue with scenario logic
```

**Applies to:** BOOKING-001, BOOKING-002, INBOUND-001 (check Do_Not_Auto_Send), EMERGENCY-001  
**Field IDs:**
- `Emergency_Flag`: `fldHxfGgVuAH1SKBO` on Bookings (`tbl72omPibBkn2hZL`)
- `Automations_Paused`: `flduB7GqI7TOdQKUB` on Bookings (`tbl72omPibBkn2hZL`)
- `Do_Not_Auto_Send`: `fld6gF1E5wZ3rHmUg` on Requests (`tblTlSB9CO4dTGodg`)

---

### MANDATORY PATTERN P-002: Idempotency Check

**Every scenario that creates an Airtable record or sends a client message must implement this:**

```
Step A: Compute hash = SHA256(Booking_ID + "_" + Scenario_ID + "_" + Date(TODAY))
Step B: Airtable — Search Records (Bookings) where Idempotency_Key = hash
  IF record found:
    → Log to Automation_Health: Status = DUPLICATE_SKIPPED, hash, Scenario_ID
    → Stop execution
  IF not found:
    → Write hash to Bookings.Idempotency_Key
    → Continue with scenario
```

**Field ID:** `Idempotency_Key` — `fldjxNVa8Cr9RJhIq` on Bookings (`tbl72omPibBkn2hZL`)

---

### MANDATORY PATTERN P-003: Environment Check

**Every scenario reads the Environment field from the triggering Airtable record as step 1:**

```
Step 1: Read record from Airtable
Step 2: Filter
  IF Environment = "Sandbox" OR Environment = "Development":
    → IF current Make scenario is tagged Production:
        → Log skipped test record, stop
  IF Environment = "Production":
    → Continue
```

**Field IDs:**
- Bookings: `Environment` — `fldb2hN3kxhS3TwUT`
- Requests: `Environment` — `fldF8PaiQacfKVtyE`

---

### MANDATORY PATTERN P-004: Audit Log Write Before Completion

**Every Tier A autonomous action must write to Audit Log before the action is considered complete:**

```
Final step of every Tier A scenario:
→ Airtable — Create Record (Audit Log, tblrMpTfMk8q1eNHp):
  - Log Entry: [scenario description + output summary]
  - Action Type: [INBOUND_RESPONSE / BOOKING_CONFIRMED / DEPOSIT_SENT / etc.]
  - Timestamp: [NOW() in UTC]
  - Scenario ID: [Make scenario ID]
  - Actor: "Make Automation"
  - Environment: [Production / Sandbox]
  - Brand: [SSS / ME from triggering record]
  - Approval_State: AUTONOMOUS
  - Source_System: Make

IF audit log write fails:
  → Slack alert to #sss-ops-alerts: "AUDIT LOG WRITE FAILED — Scenario [ID] — Manual logging required"
  → Action is NOT considered complete until logged
```

**Table ID:** `tblrMpTfMk8q1eNHp`

---

## STAGE 1 SCENARIO SPECIFICATIONS

---

### SCENARIO: INBOUND-001

**Trigger:** Webflow form submission webhook  
**Environment:** Production only  
**Autonomy Tier:** A  

**Sequence:**
1. Receive webhook payload from Webflow
2. Validate webhook signature (bearer token)
3. Parse form fields: First Name, Last Name, Email, Phone, Occasion, Guest Count, Preferred Date, Experience, Duration
4. Map Brand from form source URL (SSS site → Brand = SSS; ME site → Brand = ME)
5. Check for duplicate: search Requests table for Email + Preferred Date within 24 hours — if found, skip creation and log
6. Create Airtable Request record (`tblTlSB9CO4dTGodg`):
   - All form fields populated
   - Environment = Production
   - Brand = [mapped from URL]
   - Source_System = Make
   - Status = NEW
   - Last_AI_Action = NOW()
7. Send Slack notification to #sss-new-leads (or ME equivalent): Client name, occasion, group size, date
8. Write Audit Log (Pattern P-004)

**Sandbox Rule:** If form submitted from staging URL pattern, set Environment = Sandbox. Slack notification goes to #sss-sandbox-test only.

**No outbound client message in this scenario.** Auto-reply is handled by Webflow native confirmation or separate INBOUND-002 (Stage 2).

**Required Credentials:**
- Airtable: Personal Access Token (scoped to appdZ49WqgjRXxA1R)
- Slack: OAuth app token (workspace: SSS)
- Webflow Webhook: bearer token validation

---

### SCENARIO: BOOKING-001

**Trigger:** Bookings record where Status changes to AVAILABILITY_CONFIRMED (field watch)  
**Environment:** Production only  
**Autonomy Tier:** A  

**Sequence:**
1. Watch Bookings table for Status = AVAILABILITY_CONFIRMED
2. Pattern P-001: Read Emergency_Flag and Automations_Paused — exit if either true
3. Pattern P-003: Read Environment — skip if Sandbox
4. Pattern P-002: Idempotency check for BOOKING-001 + Booking_ID
5. Read Client linked record: Name, Email, Phone
6. Read Package linked record: Package_Name, Price
7. Read Yacht linked record: Vessel_Name
8. **Stripe test mode:** Create Stripe Payment Link (50% of Package Price + Add-Ons)
   - In sandbox: use Stripe test mode only — no live charges
   - In production: use live Stripe mode only after Will confirms production activation
9. Write Stripe Payment Link URL to Bookings.Stripe_Payment_Link
10. Send Gmail (hello@shesaidsail.com) to client: deposit link, booking summary, next steps
11. Send Quo SMS to client phone: "Hi [name], your [experience] on [date] is available! Here's your deposit link: [url]"
12. Update Booking Status = DEPOSIT_SENT
13. Write Audit Log (Pattern P-004)

**Safety checks:**
- If Client Email or Phone is missing: route to Luciana (Slack) — do not attempt send
- If Stripe link creation fails: route to Luciana — do not change Booking Status

**Required Credentials:**
- Airtable: PAT (appdZ49WqgjRXxA1R)
- Stripe: API key + test mode key (separate credentials)
- Gmail: OAuth (hello@shesaidsail.com)
- Quo: API key
- Slack: OAuth (for error routing)

---

### SCENARIO: BOOKING-002

**Trigger:** Stripe webhook — `payment_intent.succeeded` (deposit amount)  
**Environment:** Production only  
**Autonomy Tier:** A  

**Sequence:**
1. Receive Stripe webhook
2. Validate Stripe webhook signature (signing secret) — reject if invalid
3. Validate timestamp — reject if >5 minutes old (anti-replay)
4. Extract Booking_ID from Stripe metadata
5. Lookup Booking record in Airtable by Booking_ID
6. Pattern P-003: Environment check — if Sandbox, log to test channel only
7. Pattern P-001: Emergency_Flag + Automations_Paused check — if true, Slack alert + hold
8. Pattern P-002: Idempotency check for BOOKING-002 + Stripe payment_intent ID
9. Update Booking Status = DEPOSIT_PAID
10. Write Deposit_Amount and Deposit_Received_At to Booking record
11. Send Gmail to client: deposit confirmed, what happens next
12. Send Slack to #sss-ops-alerts: Deposit received for [Booking_ID] — [Client Name] — [Amount]
13. Write Audit Log (Pattern P-004)

**Stripe Test Mode:**
- Test webhook endpoint must be separate from production endpoint
- Test mode events use Stripe test signing secret (different from live signing secret)
- Never use a production signing secret in sandbox testing

**Required Credentials:**
- Stripe Webhook Signing Secret (live + test — stored separately)
- Airtable: PAT
- Gmail: OAuth
- Slack: OAuth

---

### SCENARIO: EMERGENCY-001

**Trigger:** Bookings record where Emergency_Flag changes from false to true  
**Environment:** Production + Sandbox (emergency protocol always fires)  
**Autonomy Tier:** A  

**Sequence:**
1. Watch Bookings for Emergency_Flag = true (field-specific trigger — not generic record updated)
2. Set Automations_Paused = true on the Booking record immediately
3. Send Slack DM directly to Will (not channel-only): structured emergency message
4. Post to #sss-emergency-ops channel: L4 Emergency Thread Format (per Section X.3 of Systems Intelligence Architecture)
5. Create Founder Decision record (Approval Queue): Type = EMERGENCY, Urgency = IMMEDIATE, Context = Booking_ID + auto-description
6. Create Emergency_Escalations record (tblDbeRf3qO3xvqhK): Booking_ID, City, Initiated_At, Type, Description
7. Write Audit Log (Pattern P-004)

**Zero client contact in this scenario.** No email. No SMS. No further automation.

**Flag clearance:** Will only — manual Airtable edit. No automation clears Emergency_Flag.

**Required Credentials:**
- Airtable: PAT (write to Bookings, Approval Queue, Emergency_Escalations, Audit Log)
- Slack: OAuth (DM capability + channel post)

---

## CREDENTIAL CONNECTION REQUIREMENTS

All credentials must be stored in Make's credential vault. No credentials in code, webhook URLs, or documentation.

| Credential | System | Type | Stage 1 Required? | Status |
|-----------|--------|------|------------------|--------|
| Airtable PAT | appdZ49WqgjRXxA1R | Personal Access Token | YES | Confirm scoped to production base |
| Airtable PAT | apprDKQtV2GInThwE | Personal Access Token | YES (FINANCIAL-001, Stage 1+) | Confirm scoped to financial base |
| Stripe Live API Key | Stripe | Secret key | YES (BOOKING-001) | **Live mode activation: Will only** |
| Stripe Test API Key | Stripe | Secret key | YES (sandbox testing) | Required before any Stripe scenario testing |
| Stripe Webhook Signing Secret (Live) | Stripe | Signing secret | YES (BOOKING-002) | Register live endpoint first |
| Stripe Webhook Signing Secret (Test) | Stripe | Signing secret | YES (sandbox) | Register test endpoint first |
| Gmail OAuth | hello@shesaidsail.com | OAuth 2.0 | YES (BOOKING-001) | Confirm scope includes send |
| Quo API Key | Quo SMS | API key | YES (BOOKING-001) | Confirm test mode availability |
| Slack OAuth | SSS Workspace | Bot token | YES (EMERGENCY-001) | Confirm DM capability |
| Webflow Webhook Secret | Webflow | Bearer token | YES (INBOUND-001) | Generate in Webflow settings |

---

## MAKE FOLDER AND ENVIRONMENT STRUCTURE

### Required Make Organization Before Building

```
Make Workspace: She Said Sail
│
├── Stage 1 — SANDBOX (prefix all with [SANDBOX])
│   ├── [SANDBOX] INBOUND-001
│   ├── [SANDBOX] BOOKING-001
│   ├── [SANDBOX] BOOKING-002
│   └── [SANDBOX] EMERGENCY-001
│
└── Stage 1 — PRODUCTION (activate only after sandbox validation)
    ├── INBOUND-001
    ├── BOOKING-001
    ├── BOOKING-002
    └── EMERGENCY-001
```

**Rule:** No scenario moves from Sandbox to Production folder until:
1. Sandbox scenario has run successfully against test data 3+ times
2. No errors in error log
3. Audit Log writes confirmed
4. Will has reviewed and approved (Founder Decision: SYSTEM recorded in Airtable)

---

## WEBHOOK REGISTRATION REQUIREMENTS

| Scenario | Webhook Type | Registration | Safety |
|----------|-------------|-------------|--------|
| INBOUND-001 | Webflow → Make | Register in Webflow site settings | Separate test and live endpoints |
| BOOKING-001 | Airtable field watch | Make Airtable module watches specific field | Field-specific (not generic record update) |
| BOOKING-002 | Stripe → Make | Register in Stripe Developer → Webhooks | Separate test and live endpoints + signing secrets |
| EMERGENCY-001 | Airtable field watch | Make Airtable module watches Emergency_Flag | Field-specific (not generic record update) |

**Critical Stripe Rule:** Stripe webhooks must be registered for these events ONLY:
- `payment_intent.succeeded` (for BOOKING-002 deposit detection)

Do NOT register all Stripe events. Unused events create noise and performance overhead.

---

## MAKE VARIABLE STANDARDIZATION

All Stage 1 Make scenarios use these standardized variable names:

| Variable | Value | Used In |
|----------|-------|---------|
| `BOOKING_ID` | Airtable Booking ID value | All booking scenarios |
| `CLIENT_EMAIL` | Client email from linked Client record | BOOKING-001 |
| `CLIENT_PHONE` | Client phone from linked Client record | BOOKING-001 |
| `CLIENT_NAME` | Client full name | BOOKING-001 |
| `BRAND` | "SSS" or "ME" from Booking Brand field | All scenarios |
| `ENVIRONMENT` | "Production" or "Sandbox" | All scenarios |
| `SCENARIO_ID` | Make scenario ID (hardcoded per scenario) | Idempotency + Audit Log |
| `IDEMPOTENCY_KEY` | SHA256 hash (see Pattern P-002) | BOOKING-001, BOOKING-002 |

---

## STAGE 1 MAKE READINESS CHECKLIST

| Item | Status | Owner |
|------|--------|-------|
| Make workspace created | PENDING VERIFICATION | Will |
| Sandbox folder structure created | PENDING | Will |
| Airtable PAT created and scoped to production base | PENDING VERIFICATION | Will |
| Airtable PAT created and scoped to financial base | PENDING VERIFICATION | Will |
| Stripe test API key connected to Make | PENDING | Will |
| Stripe live API key connected to Make (locked until go-live approval) | PENDING | Will |
| Stripe test webhook registered + signing secret stored | PENDING | Will |
| Stripe live webhook registered + signing secret stored (locked) | PENDING | Will |
| Gmail OAuth connected | PENDING VERIFICATION | Will |
| Quo API key connected | PENDING VERIFICATION | Will |
| Slack bot token connected | PENDING VERIFICATION | Will |
| Webflow webhook secret configured | PENDING | Will |
| Native automation audit complete (B-008) | PENDING | **Will — BLOCKING** |
| Sandbox scenarios built and tested | PENDING | Will + Ops |
| Founder Decision: SYSTEM logged for Stage 1 production activation | PENDING | Will |

---

*SHE SAID SAIL + MARE EXECUTIVE*  
*CONFIDENTIAL — INTERNAL USE ONLY*  
*STAGE_1_MAKE_BLOCKER_RESOLUTION.md*  
*Authored: 2026-05-16*  
*Authority: 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION*
