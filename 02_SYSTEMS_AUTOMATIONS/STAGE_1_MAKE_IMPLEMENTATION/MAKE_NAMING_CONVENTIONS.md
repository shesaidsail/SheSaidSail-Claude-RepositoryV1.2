# MAKE_NAMING_CONVENTIONS

**Status:** PRODUCTION STANDARD
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** She Said Sail + Mare Executive — All Make Scenarios, Webhooks, Variables, Modules, and Airtable Fields
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

> **Authority Statement:** Every Make scenario, module label, variable name, webhook endpoint, route label, idempotency key, and Airtable field name in the She Said Sail / Mare Executive production system must conform to these conventions. Inconsistency is not a preference issue — it is a debugging liability, an audit trail gap, and a training failure when new team members or future AI agents read system state. These standards apply without exception to sandbox and production environments alike.

---

## 1. MAKE SCENARIO NAMING STANDARD

### 1.1 Format

```
M-[FUNCTION]-[MODIFIER]
```

All caps. Hyphen-separated. No spaces. No lowercase. No special characters beyond hyphens.

| Component | Definition | Examples |
|-----------|-----------|---------|
| `M-` | Mandatory prefix — identifies this as a Make scenario, not an Airtable automation or cron job | Always `M-` |
| `[FUNCTION]` | What the scenario does — single word or compound word | `BRAND`, `LEAD`, `BOOKING`, `STRIPE`, `AUDIT`, `SLACK`, `HEALTH`, `CONCIERGE` |
| `[MODIFIER]` | Clarifies which aspect of the function | `ROUTER`, `INTAKE`, `CREATION`, `DEPOSIT`, `LOGGER`, `ALERTS`, `ASSIGNMENT`, `CONFIRMATION` |

### 1.2 Stage 1 Canonical Scenario Names

| Scenario Name | Function | Purpose |
|--------------|----------|---------|
| `M-BRAND-ROUTER` | Brand classification | Routes inbound request to SSS or ME workflow |
| `M-LEAD-INTAKE` | Lead ingestion | Creates Airtable Request record from inbound form |
| `M-SLACK-ALERTS` | Alert dispatch | Sends all Slack notifications by severity and routing matrix |
| `M-CONCIERGE-ASSIGNMENT` | Broker assignment | Assigns available broker to qualified request |
| `M-STRIPE-DEPOSIT` | Payment processing | Creates deposit link and handles Stripe webhook |
| `M-BOOKING-CREATION` | Booking record | Creates Booking record from confirmed Request |
| `M-BOOKING-CONFIRMATION` | Confirmation delivery | Sends confirmation email and notification |
| `M-AUDIT-LOGGER` | Audit trail | Writes immutable Audit Log entry for every Tier A action |
| `M-HEALTH-001` | System health | Checks all automation metrics every 15 minutes |
| `M-HEALTH-FAILSAFE` | Monitoring redundancy | Verifies HEALTH-001 is running; alerts if offline |

### 1.3 Naming for Future Scenarios

| Future Function | Expected Name Pattern |
|-----------------|----------------------|
| Charter brief generation | `M-CHARTER-BRIEF` |
| 72-hour pre-charter reminder | `M-CHARTER-T72` |
| Post-charter review request | `M-REVIEW-D7` |
| P&L sync to Financials base | `M-FINANCIAL-SYNC` |
| Weekly intelligence digest | `M-DIGEST-WEEKLY` |
| Daily backup | `M-BACKUP-DAILY` |
| Airtable prompt version rollback | `M-PROMPT-ROLLBACK` |

### 1.4 Anti-Patterns (Prohibited)

| Prohibited | Reason | Correct Version |
|-----------|--------|----------------|
| `Lead Intake` | Spaces not allowed | `M-LEAD-INTAKE` |
| `m-lead-intake` | Lowercase not allowed | `M-LEAD-INTAKE` |
| `LeadIntake` | No prefix, no hyphens | `M-LEAD-INTAKE` |
| `LEAD_INTAKE` | Underscore not allowed in scenario names | `M-LEAD-INTAKE` |
| `Scenario 1 - Lead` | Non-descriptive, number-based | `M-LEAD-INTAKE` |
| `SSS Lead to Airtable` | Brand prefix in scenario name not required (brand is context, not scenario identity) | `M-LEAD-INTAKE` |

---

## 2. MAKE FOLDER NAMING STANDARD

### 2.1 Format

Make organizes scenarios into folders. The folder hierarchy follows:

```
[Brand or Shared] / [Stage] / [Functional Domain]
```

### 2.2 Production Folder Tree

```
She Said Sail + Mare Executive (root)
├── SSS
│   ├── Stage 1 — Core Intake and Booking
│   │   ├── M-BRAND-ROUTER
│   │   ├── M-LEAD-INTAKE
│   │   ├── M-CONCIERGE-ASSIGNMENT
│   │   ├── M-STRIPE-DEPOSIT
│   │   ├── M-BOOKING-CREATION
│   │   └── M-BOOKING-CONFIRMATION
│   ├── Stage 1 — Operations Infrastructure
│   │   ├── M-SLACK-ALERTS
│   │   ├── M-AUDIT-LOGGER
│   │   ├── M-HEALTH-001
│   │   └── M-HEALTH-FAILSAFE
│   └── Stage 2 — Charter Lifecycle (future)
├── ME
│   ├── Stage 1 — Core Intake and Booking
│   └── Stage 1 — Operations Infrastructure
├── Shared
│   ├── Infrastructure
│   └── Monitoring
└── _SANDBOX
    ├── SSS — Sandbox
    └── ME — Sandbox
```

### 2.3 Folder Naming Rules

- Use Title Case for folder names
- Hyphens allowed; no underscores in folder names
- Stage number prefix on all stage-specific folders: `Stage 1 — [Domain]`
- Sandbox folder prefixed with underscore to sort to bottom: `_SANDBOX`
- Never place production and sandbox scenarios in the same folder

---

## 3. WEBHOOK NAMING STANDARD

### 3.1 Format

```
WHK-[BRAND]-[FUNCTION]-[ENV]
```

All caps. Hyphen-separated.

| Component | Values | Notes |
|-----------|--------|-------|
| `WHK-` | Always `WHK-` | Identifies as a webhook endpoint |
| `[BRAND]` | `SSS`, `ME`, `SHARED` | Which brand this webhook serves |
| `[FUNCTION]` | Single word — what the webhook receives | `LEAD`, `STRIPE`, `AIRTABLE`, `BOOKING`, `CONCIERGE` |
| `[ENV]` | `PROD`, `SANDBOX` | Never abbreviate as `PRD` — always `PROD` |

### 3.2 Stage 1 Canonical Webhook Names

| Webhook Name | Source System | Make Scenario | Environment | Purpose |
|-------------|--------------|--------------|-------------|---------|
| `WHK-SSS-LEAD-PROD` | Webflow | M-LEAD-INTAKE | Production | SSS form submissions |
| `WHK-ME-LEAD-PROD` | Webflow | M-LEAD-INTAKE | Production | ME form submissions |
| `WHK-SSS-STRIPE-DEPOSIT-PROD` | Stripe | M-STRIPE-DEPOSIT | Production | Deposit payment events |
| `WHK-ME-STRIPE-DEPOSIT-PROD` | Stripe | M-STRIPE-DEPOSIT | Production | ME deposit payment events |
| `WHK-SSS-AIRTABLE-ROUTER-PROD` | Airtable | M-BRAND-ROUTER | Production | New Request record created |
| `WHK-SSS-BOOKING-CREATED-PROD` | Airtable | M-BOOKING-CREATION | Production | New Booking record created |
| `WHK-SSS-CONCIERGE-PROD` | Airtable | M-CONCIERGE-ASSIGNMENT | Production | Request status changed |
| `WHK-SSS-LEAD-SANDBOX` | Webflow (test) | M-LEAD-INTAKE | Sandbox | SSS form submissions — test only |
| `WHK-ME-LEAD-SANDBOX` | Webflow (test) | M-LEAD-INTAKE | Sandbox | ME form submissions — test only |
| `WHK-SSS-STRIPE-DEPOSIT-SANDBOX` | Stripe (test mode) | M-STRIPE-DEPOSIT | Sandbox | Test deposit events |

### 3.3 Webhook Registration Record

Every webhook must have a corresponding Make_Scenarios record in Airtable with:
- `Webhook_Name` (WHK format above)
- `Webhook_URL` (Make-generated URL — stored encrypted)
- `Source_System` (which system sends events to this webhook)
- `Environment` (Production / Sandbox)
- `Registered_At` (DateTime)
- `Last_Test_Event_Received` (DateTime)

---

## 4. VARIABLE NAMING IN MAKE MODULES

### 4.1 General Rule

All Make variables use `snake_case`. No camelCase. No PascalCase. No spaces.

```
source_prefix.field_name
```

### 4.2 Source Prefixes

| Source | Prefix | Example |
|--------|--------|---------|
| Airtable | `airtable_` | `airtable_request_id` |
| Stripe | `stripe_` | `stripe_payment_intent_id` |
| Webflow | `webflow_` | `webflow_form_submission_id` |
| Slack | `slack_` | `slack_message_ts` |
| Gmail | `gmail_` | `gmail_thread_id` |
| Quo SMS | `quo_` | `quo_message_sid` |
| Claude API | `claude_` | `claude_response_text` |
| Make (internal) | `make_` | `make_scenario_id` |
| Computed (calculated in Make) | `computed_` | `computed_idempotency_key` |

### 4.3 Stage 1 Key Variable Names

| Variable | Source | Type | Used By |
|---------|--------|------|---------|
| `airtable_request_id` | Airtable → Requests | Text | M-BRAND-ROUTER, M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT |
| `airtable_booking_id` | Airtable → Bookings | Text | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| `airtable_client_id` | Airtable → Clients | Text | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `airtable_brand` | Airtable → Requests | Text (SSS / ME) | M-BRAND-ROUTER — all scenarios read this |
| `airtable_environment` | Airtable → any table | Text | First-step gate — all production scenarios |
| `airtable_emergency_flag` | Airtable → Bookings | Boolean | M-SLACK-ALERTS, HEALTH-001 |
| `airtable_automations_paused` | Airtable → Bookings | Boolean | All outbound scenarios |
| `stripe_payment_intent_id` | Stripe | Text | M-STRIPE-DEPOSIT — written to Bookings |
| `stripe_checkout_session_id` | Stripe | Text | M-STRIPE-DEPOSIT — for idempotency |
| `stripe_amount_paid` | Stripe webhook | Number | M-STRIPE-DEPOSIT → Bookings.Deposit_Amount |
| `stripe_customer_email` | Stripe | Text | M-STRIPE-DEPOSIT — cross-referenced against Client |
| `computed_idempotency_key` | Make | Text | All scenarios that create records or send messages |
| `computed_audit_ref` | Make | Text (AUD-YYYY-NNNN) | M-AUDIT-LOGGER |
| `computed_brand_classification` | Make | Text (SSS / ME) | M-BRAND-ROUTER output |
| `claude_brand_classification` | Claude API response | Text | M-BRAND-ROUTER when AI classification is used |
| `claude_confidence_score` | Claude API response | Number 0–100 | M-BRAND-ROUTER, M-CONCIERGE-ASSIGNMENT |

### 4.4 Variable Anti-Patterns

| Prohibited | Reason | Correct |
|-----------|--------|---------|
| `RequestID` | PascalCase | `airtable_request_id` |
| `request-id` | Hyphens in variables | `airtable_request_id` |
| `id` | No context — which table, which source | `airtable_request_id` |
| `bookingData` | camelCase, no source prefix | `airtable_booking_id` |
| `x`, `temp`, `data` | Non-descriptive | Use full descriptive name |

---

## 5. MODULE LABEL STANDARD

### 5.1 Format

Every module (step) in a Make scenario must have a human-readable label. The default Make labels (`Airtable 1`, `HTTP 2`, `Slack 3`) are prohibited in production scenarios.

```
[Action Verb] [Object] → [Destination]
```

| Component | Definition | Examples |
|-----------|-----------|---------|
| `[Action Verb]` | What the module does | `Create`, `Read`, `Update`, `Send`, `Check`, `Route`, `Log`, `Generate`, `Validate` |
| `[Object]` | What it acts on | `Request Record`, `Booking Status`, `Deposit Link`, `Slack Alert`, `Audit Entry` |
| `→ [Destination]` | Where the result goes | `→ Airtable`, `→ Stripe`, `→ Slack #sss-ops-alerts`, `→ Audit Log`, `→ Gmail` |

### 5.2 Stage 1 Module Label Examples

| Scenario | Module Position | Label |
|----------|----------------|-------|
| M-BRAND-ROUTER | 1 | `Read Request Record → Airtable` |
| M-BRAND-ROUTER | 2 | `Validate Environment = Production` |
| M-BRAND-ROUTER | 3 | `Classify Brand (SSS / ME) → Claude API` |
| M-BRAND-ROUTER | 4 | `Route by Brand → Router Module` |
| M-LEAD-INTAKE | 1 | `Receive Form Submission → Webflow Webhook` |
| M-LEAD-INTAKE | 2 | `Check Idempotency Key → Airtable Requests` |
| M-LEAD-INTAKE | 3 | `Create Request Record → Airtable` |
| M-LEAD-INTAKE | 4 | `Send Lead Alert → Slack #sss-ops-alerts` |
| M-LEAD-INTAKE | 5 | `Log Action → Audit Log` |
| M-STRIPE-DEPOSIT | 1 | `Validate Stripe Signature → Webhook` |
| M-STRIPE-DEPOSIT | 2 | `Read Booking Record → Airtable` |
| M-STRIPE-DEPOSIT | 3 | `Check Automations_Paused → Gate` |
| M-STRIPE-DEPOSIT | 4 | `Update Booking Status → DEPOSIT_PAID → Airtable` |
| M-STRIPE-DEPOSIT | 5 | `Write Stripe Metadata → Airtable` |
| M-STRIPE-DEPOSIT | 6 | `Send Deposit Confirmation Alert → Slack #sss-ops-alerts` |
| M-STRIPE-DEPOSIT | 7 | `Log Payment Receipt → Audit Log` |
| M-AUDIT-LOGGER | 1 | `Receive Audit Payload → Internal Webhook` |
| M-AUDIT-LOGGER | 2 | `Generate Audit Reference → AUD-YYYY-NNNN` |
| M-AUDIT-LOGGER | 3 | `Write Audit Record → Airtable Audit Log` |
| M-AUDIT-LOGGER | 4 | `Write Health State → Automation_Health` |
| M-HEALTH-001 | 1 | `Read Automation_Health → Last 60 Minutes` |
| M-HEALTH-001 | 2 | `Read Audit Log → Gap Detection` |
| M-HEALTH-001 | 3 | `Count Failures → Automation_Failures` |
| M-HEALTH-001 | 4 | `Check Emergency_Flag Count → Bookings` |
| M-HEALTH-001 | 5 | `Evaluate All Thresholds → Router` |
| M-HEALTH-001 | 6 | `Send Alerts by Severity → M-SLACK-ALERTS` |
| M-HEALTH-001 | 7 | `Write Health Check Result → Automation_Health` |

### 5.3 Module Label Anti-Patterns

| Prohibited | Reason | Correct |
|-----------|--------|---------|
| `Airtable 1` | Default label — no context | `Read Request Record → Airtable` |
| `HTTP 3` | Default label | `Call Claude API → Brand Classification` |
| `Module` | Completely non-descriptive | Use full action-object-destination format |
| `Send Slack` | Missing object and destination | `Send Lead Alert → Slack #sss-ops-alerts` |
| `Check` | No object | `Check Idempotency Key → Airtable Requests` |

---

## 6. ROUTE NAMING STANDARD (ROUTER MODULES)

### 6.1 Format

Make Router modules contain named routes (branches). Every route must be labeled:

```
IF [Condition] → [Action]
```

Conditions use actual field names or values. No vague labels like "Route 1" or "Default."

### 6.2 Stage 1 Router Examples

**M-BRAND-ROUTER — Brand Classification Router:**

| Route | Label |
|-------|-------|
| Route 1 | `IF Brand = SSS → SSS Lead Intake Flow` |
| Route 2 | `IF Brand = ME → ME Lead Intake Flow` |
| Route 3 | `IF Brand = UNKNOWN → Flag for Manual Review → Slack Alert` |

**M-LEAD-INTAKE — Environment Gate Router:**

| Route | Label |
|-------|-------|
| Route 1 | `IF Environment = Production → Continue` |
| Route 2 | `IF Environment = Sandbox → Exit Without Action` |

**M-SLACK-ALERTS — Severity Router:**

| Route | Label |
|-------|-------|
| Route 1 | `IF Severity = SEV-1 → Will DM + #sss-emergency-ops` |
| Route 2 | `IF Severity = SEV-2 → Luciana DM + #sss-ops-alerts` |
| Route 3 | `IF Severity = SEV-3 → #sss-ops-alerts Only` |
| Route 4 | `IF Severity = SEV-4 → Automation_Health Log Only` |

**M-CONCIERGE-ASSIGNMENT — HV Client Router:**

| Route | Label |
|-------|-------|
| Route 1 | `IF HV_Client = TRUE → Assign Senior Broker → Alert Luciana` |
| Route 2 | `IF HV_Client = FALSE → Standard Broker Assignment` |

**M-HEALTH-001 — Alert Threshold Router:**

| Route | Label |
|-------|-------|
| Route 1 | `IF Emergency_Flag > 0 → SEV-1 Alert` |
| Route 2 | `IF Audit_Gap_Detected → SEV-1 Alert` |
| Route 3 | `IF Failure_Count > 3 → SEV-2 Alert` |
| Route 4 | `IF Stripe_Latency > 5min → SEV-2 Alert` |
| Route 5 | `IF Airtable_Error_Rate > 5% → SEV-2 Alert` |
| Route 6 | `IF Backup_Age > 48hrs → SEV-2 Alert` |
| Route 7 | `IF All Checks Pass → SEV-4 Log Only` |

---

## 7. AIRTABLE FIELD NAMING STANDARD

### 7.1 Format

All Airtable fields use `Title_Case_With_Underscores`. No spaces in field names. The human-visible display name in Airtable interfaces may use spaces ("Request ID"), but the underlying field name (used by Make API calls) must be underscore-separated Title_Case.

```
Title_Case_With_Underscores
```

### 7.2 Rules

| Rule | Example |
|------|---------|
| No spaces — underscores only | `Agent_Status` not `Agent Status` |
| Title Case — every word capitalized | `Last_AI_Action` not `last_ai_action` |
| Abbreviations all-caps | `AI`, `HV`, `SMS`, `API`, `UUID`, `SLA` |
| Boolean fields — use `Is_` prefix for clarity | `Is_HV_Client` or `HV_Client` (checkbox implies boolean) |
| Date/time fields — suffix with `_At` or `_Date` | `Created_At`, `Deposit_Paid_At`, `Charter_Date` |
| Count fields — suffix with `_Count` | `Failure_Count_1hr`, `Guests_Count` |
| Percentage fields — suffix with `_Pct` | `Net_Margin_Pct`, `AI_Confidence_Score` |
| ID reference fields — suffix with `_ID` | `Stripe_Payment_Intent_ID`, `Audit_Log_Ref_ID` |
| Formula fields — no suffix convention but name must describe output | `D7_Review_Eligible`, `UUID`, `Implied_Margin` |

### 7.3 Protected Field Naming

Fields that Make must never overwrite are named with a `_PROTECTED` suffix in internal documentation but not in Airtable (since Airtable has no built-in field-lock). The list of protected fields is maintained in FINAL_PRODUCTION_AIRTABLE_ARCHITECTURE.md. Operationally, all formula fields are inherently read-only (Airtable prevents writes), and financial lock fields are listed in the Airtable API token scope (write access excluded for those field IDs).

---

## 8. IDEMPOTENCY KEY FORMAT

### 8.1 Standard Format

```
[scenario_id]-[record_id]-[timestamp_epoch]
```

| Component | Source | Example |
|-----------|--------|---------|
| `[scenario_id]` | Make scenario name, abbreviated | `LEAD-INTAKE`, `BOOKING-CREATION`, `STRIPE-DEPOSIT` |
| `[record_id]` | Airtable RECORD_ID() of the primary affected record | `recABCD1234XYZ` |
| `[timestamp_epoch]` | Unix epoch at scenario execution start — seconds precision | `1747397400` |

**Full examples:**

| Scenario | Idempotency Key Example |
|----------|------------------------|
| M-LEAD-INTAKE | `LEAD-INTAKE-recABCD1234XYZ-1747397400` |
| M-BOOKING-CREATION | `BOOKING-CREATION-recEFGH5678ABC-1747398000` |
| M-STRIPE-DEPOSIT | `STRIPE-DEPOSIT-recIJKL9012DEF-1747398600` |
| M-BOOKING-CONFIRMATION | `BOOKING-CONF-recMNOP3456GHI-1747399200` |
| M-CONCIERGE-ASSIGNMENT | `CONCIERGE-recQRST7890JKL-1747399800` |

### 8.2 Storage Location

- Written to `Idempotency_Key` field on the primary affected record (Requests or Bookings)
- Also logged in Audit Log: `Idempotency_Key` field

### 8.3 Idempotency Check Logic

```
Step 1: Compute computed_idempotency_key using above format
Step 2: Search Airtable [primary table] WHERE Idempotency_Key = computed_idempotency_key
Step 3: IF record found → scenario exits with log entry "IDEMPOTENCY_DUPLICATE_BLOCKED"
Step 4: IF no record found → proceed with action → write idempotency key on record creation
```

---

## 9. AUDIT LOG REFERENCE FORMAT

### 9.1 Standard Format

```
AUD-YYYY-NNNN
```

| Component | Definition | Example |
|-----------|-----------|---------|
| `AUD-` | Always this prefix | `AUD-` |
| `YYYY` | 4-digit year | `2026` |
| `NNNN` | 4-digit sequential number, padded with leading zeros, resets each year | `0001`, `0042`, `1004` |

**Example:** `AUD-2026-0001` is the first audit entry of 2026. `AUD-2026-1247` is the 1,247th.

### 9.2 Generation Method

Audit reference numbers are generated by M-AUDIT-LOGGER using Airtable's auto-number field or a Make counter. The counter is maintained in a dedicated control record in the Audit Log table with Record name `COUNTER-YYYY`. M-AUDIT-LOGGER reads the current count, increments by 1, writes the new count, and uses the resulting value for the new entry's Audit_ID.

**Critical:** The counter record must be updated atomically with the audit entry creation. If M-AUDIT-LOGGER fails after incrementing the counter but before writing the audit record, the next run detects the gap (counter shows N+1 but no record with that ID exists) and alerts via HEALTH-001.

---

## 10. STRIPE METADATA KEY NAMING

### 10.1 Format

Stripe metadata keys use lowercase snake_case with brand prefix. Stripe metadata is a flat key-value store with 40-character key limit and 500-character value limit.

```
[brand]_[object]_[field]
```

| Brand | Prefix |
|-------|--------|
| She Said Sail | `sss_` |
| Mare Executive | `me_` |

### 10.2 Stage 1 Stripe Metadata Keys

| Key | Value Type | Written By | Example Value |
|-----|-----------|-----------|--------------|
| `sss_booking_id` | Airtable Booking record human ID | M-STRIPE-DEPOSIT | `BK-2026-0042` |
| `sss_request_id` | Airtable Request record human ID | M-STRIPE-DEPOSIT | `REQ-2026-0087` |
| `sss_client_id` | Airtable Client record human ID | M-STRIPE-DEPOSIT | `CLT-0023` |
| `sss_environment` | Production or Sandbox | M-STRIPE-DEPOSIT | `Production` |
| `sss_brand` | Always SSS for SSS payments | M-STRIPE-DEPOSIT | `SSS` |
| `me_booking_id` | ME Booking record human ID | M-STRIPE-DEPOSIT (ME route) | `BK-ME-2026-0011` |
| `me_request_id` | ME Request record human ID | M-STRIPE-DEPOSIT (ME route) | `REQ-ME-2026-0034` |
| `me_client_id` | ME Client record human ID | M-STRIPE-DEPOSIT (ME route) | `CLT-ME-0008` |
| `me_environment` | Production or Sandbox | M-STRIPE-DEPOSIT (ME route) | `Production` |
| `me_brand` | Always ME for ME payments | M-STRIPE-DEPOSIT (ME route) | `ME` |

**Reconciliation rule:** When M-STRIPE-DEPOSIT receives a Stripe webhook, it reads `sss_booking_id` or `me_booking_id` from the metadata to locate the correct Airtable Booking record. This is the only cross-reference between Stripe and Airtable — no other lookup method is used in Stage 1.

---

## 11. ERROR MESSAGE FORMAT

### 11.1 Standard Format

All error messages written to Automation_Failures and logged in Audit Log use:

```
[SCENARIO_ID]-[ERROR_CODE]-[TIMESTAMP]
```

| Component | Format | Example |
|-----------|--------|---------|
| `[SCENARIO_ID]` | Scenario name minus `M-` prefix | `LEAD-INTAKE`, `STRIPE-DEPOSIT`, `HEALTH-001` |
| `[ERROR_CODE]` | Category code (see below) | `429`, `DUPE`, `AUTH`, `FIELD`, `TIMEOUT` |
| `[TIMESTAMP]` | `YYYYMMDDHHMMSS` — no separators | `20260516143022` |

**Full error message example:** `LEAD-INTAKE-429-20260516143022`

### 11.2 Error Code Reference

| Code | Meaning | Typical Cause |
|------|---------|---------------|
| `429` | Airtable or Stripe rate limit | Too many API calls per second |
| `AUTH` | Authentication failure | Expired OAuth token, rotated API key |
| `DUPE` | Idempotency duplicate blocked | Retry triggered an already-processed event |
| `FIELD` | Missing required field | Airtable field not found — schema mismatch |
| `TIMEOUT` | Make module timed out | External API unresponsive > 60 seconds |
| `WEBHOOK` | Webhook validation failed | Invalid signature, expired timestamp |
| `AUDIT-GAP` | Audit Log entry missing | M-AUDIT-LOGGER failed or was skipped |
| `EMERGENCY-FLAG` | Emergency flag detected | booking.Emergency_Flag = true |
| `ENV-GATE` | Environment gate blocked | Sandbox record reached production scenario |
| `CIRCULAR` | Circular trigger detected | Airtable automation re-triggered Make scenario |
| `NULL-FIELD` | Required field returned null | Data integrity issue in source record |

---

## 12. TEST DATA NAMING

### 12.1 Format

All test records, test form submissions, and test payloads use:

```
TEST-[FUNCTION]-[NNNN]
```

| Component | Definition | Example |
|-----------|-----------|---------|
| `TEST-` | Always this prefix — test records are never missing this | `TEST-` |
| `[FUNCTION]` | What is being tested | `LEAD`, `BOOKING`, `STRIPE`, `CONCIERGE`, `AUDIT`, `HEALTH`, `EMERGENCY`, `ENV` |
| `[NNNN]` | 4-digit sequential number within that function | `0001`, `0002`, `0042` |

### 12.2 Stage 1 Test Data Registry

| Test Reference | Function Tested | Scenario(s) | Description |
|---------------|----------------|-------------|-------------|
| `TEST-LEAD-0001` | SSS brand routing | M-BRAND-ROUTER, M-LEAD-INTAKE | Standard SSS inquiry, all required fields |
| `TEST-LEAD-0002` | ME brand routing | M-BRAND-ROUTER, M-LEAD-INTAKE | Standard ME inquiry, all required fields |
| `TEST-LEAD-0003` | Duplicate lead block | M-LEAD-INTAKE | Same email submitted twice within 10 minutes |
| `TEST-CONCIERGE-0001` | Standard assignment | M-CONCIERGE-ASSIGNMENT | Non-HV client, standard broker pool |
| `TEST-CONCIERGE-0002` | HV client routing | M-CONCIERGE-ASSIGNMENT | HV_Client = true, senior broker assignment |
| `TEST-STRIPE-0001` | Deposit link creation | M-STRIPE-DEPOSIT | Stripe test mode, test card |
| `TEST-STRIPE-0002` | Webhook receipt | M-STRIPE-DEPOSIT | Stripe test webhook, payment_intent.succeeded |
| `TEST-BOOKING-0001` | Booking creation | M-BOOKING-CREATION | From confirmed request, all fields populated |
| `TEST-BOOKING-0002` | Booking confirmation | M-BOOKING-CONFIRMATION | Confirmation email + Slack alert |
| `TEST-EMERGENCY-0001` | Emergency flag | M-SLACK-ALERTS, HEALTH-001 | Emergency_Flag set to true |
| `TEST-AUDIT-0001` | Audit logging | M-AUDIT-LOGGER | All Tier A scenario actions produce audit entries |
| `TEST-HEALTH-0001` | Health check detection | HEALTH-001 | Deliberate failure injected, alert received |
| `TEST-ENV-0001` | Environment isolation | All scenarios | Sandbox records excluded from production |

### 12.3 Test Data Rules

- All test records must have `Environment = Sandbox`
- Test client email: `test+[function]@shesaidsail.com`
- Test client phone: Designated internal test number only
- No real financial figures in test records — use amounts ending in `.42` to identify test data in Stripe (e.g., `$1,000.42`)
- Test records are never migrated to production — they are deleted after sandbox validation is complete

---

## 13. BRANCH AND ENVIRONMENT TAGGING CONVENTIONS

### 13.1 Airtable Record Environment Tags

Every record in every production Airtable table must have:

| Field | Production Value | Sandbox Value | Development Value |
|-------|-----------------|--------------|------------------|
| `Environment` | `Production` | `Sandbox` | `Development` |

Airtable views that operators use must have a default filter: `Environment = Production`. This prevents sandbox test records from appearing in operational views.

### 13.2 Make Scenario Environment Tags

Make scenarios are tagged by folder placement (see Section 2) and by the environment they target. Within each scenario:

- Step 1 (always): Read `Environment` field from the triggering record
- Step 2: Router — `IF Environment ≠ Production → exit scenario with logged note`

The environment check is not optional and is not skipped for urgent scenarios. An emergency scenario that processes a sandbox record is a system failure, not an acceptable shortcut.

### 13.3 Stripe Environment Tags

| Context | Stripe Key | Stripe Dashboard |
|---------|-----------|-----------------|
| Production | `sk_live_...` | Live mode |
| Sandbox / Testing | `sk_test_...` | Test mode |

No cross-environment Stripe key usage is permitted under any circumstance. Stripe test-mode payments never create real charges. Live-mode payments are real charges. Mixing them is a financial and operational failure.

### 13.4 GitHub Document Version Tags

All governance documents carry a version tag in the filename and header:

```
[FOLDER]__[DOCUMENT_NAME]_v[VERSION]_[STATUS].md
```

| Status Value | Meaning |
|-------------|---------|
| `PRODUCTION` | Active, governing |
| `LOCKED` | Immutable — requires Founder Decision to amend |
| `DRAFT` | In development — not governing |
| `DEPRECATED` | Superseded — retained for audit trail |

---

*End of MAKE_NAMING_CONVENTIONS*
*Version 1.0 — Governed by Systems Intelligence Architecture v2.0*
*Any deviation from these conventions in production scenarios requires a Deployment Log entry documenting the exception and Will's approval*
