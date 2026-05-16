# ERROR HANDLING AND RETRY ARCHITECTURE
## She Said Sail + Mare Executive — Stage 1 Make.com Implementation

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Effective Date:** May 2026  
**Owner:** Will (Founder)  
**Applies To:** All 8 Stage 1 Make.com Scenarios  
**Classification:** Confidential — Internal Use Only  
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

---

## SECTION 1 — ERROR HANDLING PHILOSOPHY

### 1.1 Core Principle: Fail Loudly, Never Silently

Every failure in the She Said Sail + Mare Executive automation stack must produce a visible, traceable, and actionable artifact. Silent failures — where a scenario encounters an error and stops without logging, alerting, or escalating — are treated as system failures equivalent in severity to the original error.

**The four mandates of error handling in this system:**

1. **Every failure is logged.** No exception may be swallowed without writing a record to the Automation_Failures table in the main Airtable base (appdZ49WqgjRXxA1R). If the Airtable write itself fails, the failure must be logged to Make's native execution history and a direct Slack alert must fire.

2. **Every failure is retried.** No failure is treated as permanent on the first attempt. The retry schedule is deterministic (not random) and escalates on each subsequent failure of the same execution instance.

3. **Every persistent failure escalates to a human.** After the third retry, a human operator (Luciana, then Will) receives a Slack notification with full context. No failure silently exceeds three retries without human awareness.

4. **Every escalation creates a governance artifact.** A fourth-level failure triggers a Founder Decision record (SEV-2) in Airtable, pauses the scenario, and initiates Will's review. The system never auto-resolves SEV-2 or higher without a documented human decision.

### 1.2 Scope of Coverage

This architecture applies to:
- All 8 Stage 1 scenarios: M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, M-AUDIT-LOGGER
- All downstream integrations: Airtable API, Stripe API, Gmail OAuth, Quo SMS API, Slack API
- All webhook ingestion points (Webflow → Make, Stripe → Make)
- All scheduled triggers (HEALTH-001 polling)

---

## SECTION 2 — THE 4-LEVEL RETRY AND ESCALATION HIERARCHY

### 2.1 Failure Level Definitions

| Level | Trigger Condition | Timing | Action | Notified |
|-------|------------------|--------|--------|----------|
| **Level 1** | First execution failure | Immediate | Log to Automation_Failures; retry after 2 minutes | None (silent retry) |
| **Level 2** | Second execution failure (Retry 1 fails) | +2 min from Level 1 | Retry after 5 minutes; increment Failure_Count to 2 | None (silent retry) |
| **Level 3** | Third execution failure (Retry 2 fails) | +5 min from Level 2 | Slack alert to Luciana in #sss-ops-alerts; retry after 10 minutes | Luciana |
| **Level 4** | Fourth execution failure (Retry 3 fails) | +10 min from Level 3 | Slack DM to Will; scenario pauses; create Founder Decision: SEV-2 | Will (DM) |

**Total time from first failure to scenario pause:** ~17 minutes minimum under normal conditions.

### 2.2 Failure Count Reset Policy

The Failure_Count field in the Automation_Failures table resets to 0 only when:
- A previously failing execution completes successfully
- Will manually clears the failure record after root-cause resolution (documented in the Founder Decision)

Failure_Count does NOT reset on scenario republish or Make connection reconnect unless the underlying execution passes validation.

### 2.3 Persistent Failure (SEV-1) Threshold

If a scenario remains paused (Level 4) for 30 or more consecutive minutes without Will action, HEALTH-001 promotes the incident to SEV-1. SEV-1 triggers:
- Slack DM to Will (repeat alert, flagged URGENT)
- Slack message to #sss-emergency-ops
- Audit Log entry with Severity = SEV-1
- If the failing scenario handles client-facing communications (M-BOOKING-CONFIRMATION, M-STRIPE-DEPOSIT), Luciana receives a manual fallback protocol message with client contact details

---

## SECTION 3 — IMPLEMENTING RETRY IN MAKE.COM

### 3.1 Error Handler Route Configuration

In Make, error handling is implemented using the **Error Handler** route on each module that calls an external service. The Error Handler route branches from the module's error socket (the red circle).

**Standard configuration for all Stage 1 scenarios:**

```
Module (e.g., Airtable: Create Record)
  ├── Success → continue route
  └── Error socket → Error Handler module
        └── Set Variable: capture error message, error code, timestamp
              └── Router (branch by error type)
                    ├── Branch 1: Retry-eligible errors → Sleep + Retry module
                    └── Branch 2: Fatal errors → immediate escalation path
```

### 3.2 Make Error Handler Directives

Make provides four directives in Error Handler routes. Use them as follows:

| Directive | Use Case in This System | When to Apply |
|-----------|------------------------|---------------|
| **Resume** | External API returned empty but non-fatal response | Quo SMS 200 OK with empty body |
| **Ignore** | NEVER USE — violates fail-loudly principle | Not permitted in production |
| **Rollback** | Transaction that must be reversed if mid-sequence failure | Stripe payment intent created but Airtable write failed |
| **Commit** | Stop the current execution and preserve partial results | After writing Automation_Failures log before retry |

**Critical:** The `Ignore` directive is explicitly prohibited in all production scenarios. Any scenario using `Ignore` in a production Error Handler route is a configuration defect requiring immediate correction.

### 3.3 Retry Module Implementation

Make does not have a native "retry" function. Retry is implemented using the **Repeater** pattern:

```
1. HTTP Error → Error Handler captures: error_code, error_message, timestamp
2. Set Variable: attempt_number = attempt_number + 1
3. Filter: IF attempt_number <= 3 → continue; ELSE → escalation path
4. Tools > Sleep: duration based on attempt_number
   - attempt_number = 1 → sleep 120 seconds (2 minutes)
   - attempt_number = 2 → sleep 300 seconds (5 minutes)
   - attempt_number = 3 → sleep 600 seconds (10 minutes)
5. Retry the originating module
6. On success: update Automation_Failures record (Status = RESOLVED)
7. On continued failure: increment attempt_number and loop
```

---

## SECTION 4 — AIRTABLE AUTOMATION_FAILURES TABLE WRITES

### 4.1 Table Reference

- **Table:** Automation_Failures  
- **Base:** She Said Sail (appdZ49WqgjRXxA1R)  
- **Table ID:** To be confirmed after migration; currently CREATE per Section 2.2 of Airtable Spec

### 4.2 Field Mapping — Write on Level 1 (First Failure)

| Airtable Field | Type | Value Written | Source |
|----------------|------|---------------|--------|
| Scenario_Name | Single Line Text | e.g., `M-LEAD-INTAKE` | Hardcoded in scenario |
| Scenario_ID | Single Line Text | Make scenario ID | Hardcoded in scenario |
| Failure_Timestamp | Date/Time | `{{now}}` | Make built-in |
| Error_Code | Single Line Text | HTTP code or Make error code | Error handler variable |
| Error_Message | Long Text | Full error message string | Error handler variable |
| Failure_Count | Number | 1 (Level 1), 2 (Level 2), etc. | Incremented variable |
| Execution_ID | Single Line Text | Make execution ID | `{{executionId}}` |
| Affected_Record_ID | Single Line Text | Airtable record ID if applicable | Passed from trigger data |
| Brand | Single Select | SSS or ME | Read from trigger payload |
| Environment | Single Select | Production / Sandbox / Development | Hardcoded per deployment |
| Status | Single Select | OPEN | Default on create |
| Retry_Scheduled_At | Date/Time | `{{addSeconds(now, retryDelay)}}` | Computed |
| Escalation_Level | Single Select | L1 / L2 / L3 / L4 | Set per retry count |
| Resolution_Notes | Long Text | (empty on create) | Filled on resolution |

### 4.3 Update on Resolution

When a retry succeeds, the scenario must update the existing Automation_Failures record:

```json
{
  "Status": "RESOLVED",
  "Resolved_At": "{{now}}",
  "Resolution_Notes": "Resolved on attempt {{attempt_number}}. No human action required.",
  "Escalation_Level": "RESOLVED"
}
```

### 4.4 Fallback: If Airtable Write Itself Fails

If the Automation_Failures write fails (Airtable API down or rate limit):
1. Make logs the execution error natively (visible in Make execution history)
2. The scenario immediately fires a direct Slack alert to #sss-ops-alerts with the full error payload in the message body
3. The scenario does NOT retry the Airtable write — it is non-blocking for the escalation path
4. HEALTH-001 will detect the gap in Audit Log coverage on its next 15-minute poll

---

## SECTION 5 — SLACK ALERT TEMPLATES

### 5.1 Level 3 — Alert to Luciana (#sss-ops-alerts)

```
:rotating_light: *AUTOMATION ALERT — Level 3 Failure*
*Scenario:* M-[SCENARIO-NAME]
*Brand:* [SSS | ME]
*Time:* [TIMESTAMP UTC]
*Execution ID:* [MAKE-EXEC-ID]
*Error:* [ERROR_CODE] — [ERROR_MESSAGE]
*Attempts so far:* 3
*Affected Record:* [AIRTABLE-RECORD-ID or "N/A"]
*Next retry in:* 10 minutes

This failure requires your awareness. If the retry does not succeed, Will will be notified.
Automation_Failures record: [AIRTABLE-RECORD-LINK]
```

### 5.2 Level 4 — DM to Will (Direct Message)

```
:red_circle: *SEV-2 AUTOMATION FAILURE — Immediate Action Required*
*Scenario:* M-[SCENARIO-NAME] is PAUSED
*Brand:* [SSS | ME]
*Time:* [TIMESTAMP UTC]
*Execution ID:* [MAKE-EXEC-ID]
*Error:* [ERROR_CODE] — [ERROR_MESSAGE]
*Total attempts:* 4
*Affected Record:* [AIRTABLE-RECORD-ID or "N/A"]

The scenario has been paused. A Founder Decision (SEV-2) has been created in Airtable.
No further automation will run for this execution until you clear the pause.

*Required actions:*
1. Review Automation_Failures record: [LINK]
2. Review Founder Decision: [LINK]
3. Determine: fix-in-place OR rollback
4. Clear scenario pause in Make when ready to resume
```

### 5.3 SEV-1 Escalation (30+ Minutes Unresolved)

Sent to #sss-emergency-ops AND Will DM:

```
:sos: *SEV-1 ESCALATION — Scenario Paused 30+ Minutes*
*Scenario:* M-[SCENARIO-NAME]
*Paused since:* [TIMESTAMP]
*Duration paused:* [MINUTES] minutes
*Brand impact:* [SSS | ME | BOTH]

If this scenario handles client communications, manual fallback required.
Client context: [CLIENT-NAME], [CHARTER-DATE], [CONCIERGE: LUCIANA]

HEALTH-001 detected this gap. All Audit Log entries are missing for this window.
```

---

## SECTION 6 — IDEMPOTENCY PROTECTION

### 6.1 Purpose

Webhooks from Webflow and Stripe may be delivered more than once (network retries, re-queues). Without idempotency protection, a single lead form submission could create duplicate Request records, trigger duplicate emails/SMS, and generate multiple Stripe payment intents.

### 6.2 Idempotency Key Hash Pattern

Every webhook trigger generates an idempotency key before any write operation:

```
Idempotency_Key = SHA-256(
  source_system +
  "|" +
  unique_payload_field +    // e.g., Webflow submission ID, Stripe event ID
  "|" +
  timestamp_truncated_to_minute  // prevents cross-minute duplicates from re-triggering
)
```

**Examples:**
- Webflow form: `SHA-256("WEBFLOW|sub_01HXYZ|2026-05-16T14:30")`
- Stripe event: `SHA-256("STRIPE|evt_1ABC123|2026-05-16T14:30")`

### 6.3 Check-Before-Write Module Sequence

```
Step 1: Receive webhook
Step 2: Extract idempotency key fields from payload
Step 3: Compute idempotency hash (Tools > Crypto module or formula)
Step 4: Airtable Search Records — filter where Idempotency_Key = [computed hash]
Step 5: Router
  ├── Branch A: Record FOUND → this is a duplicate
  │     └── Terminate execution (Commit directive); no write, no alert
  └── Branch B: Record NOT FOUND → proceed
        ├── Write idempotency key to the new record immediately
        └── Continue with all downstream modules
```

### 6.4 Idempotency Key Storage

The Idempotency_Key field is added to the Requests table (tblTlSB9CO4dTGodg) and the Bookings table (tbl72omPibBkn2hZL). It is a Single Line Text field. A duplicate check on this field prevents double-processing.

---

## SECTION 7 — CIRCUIT BREAKER PATTERN FOR EXTERNAL APIS

### 7.1 Philosophy

If an external API (Stripe, Gmail, Quo SMS) is consistently failing, continued retries waste execution budget and mask the root cause. The circuit breaker pattern detects a threshold of consecutive failures and opens the circuit — halting retries for a cooling period before attempting again.

### 7.2 Circuit Breaker Configuration Per API

| API | Open Threshold | Cooling Period | Half-Open Test | Auto-Close On |
|-----|---------------|----------------|----------------|---------------|
| Stripe | 3 consecutive failures | 15 minutes | Single test request after cooling | Test succeeds |
| Gmail | 3 consecutive failures | 10 minutes | Single test request after cooling | Test succeeds |
| Quo SMS | 5 consecutive failures | 20 minutes | Single test request after cooling | Test succeeds |
| Airtable | 5 consecutive failures | 5 minutes | Single test request after cooling | Test succeeds |

### 7.3 Circuit State Storage in Airtable

The Make_Scenarios table (to be migrated to main base per Airtable Spec Section 5) maintains a Circuit_State field per scenario:

| Field | Type | Values |
|-------|------|--------|
| Circuit_State | Single Select | CLOSED / OPEN / HALF-OPEN |
| Circuit_Opened_At | Date/Time | Timestamp of first circuit-open event |
| Consecutive_Failures | Number | Count resets on any success |

### 7.4 Make Implementation

At the start of every scenario that calls an external API:
```
Step 1: Read Make_Scenarios record for this scenario
Step 2: Check Circuit_State
  ├── CLOSED → proceed normally
  ├── OPEN → check if cooling period has elapsed
  │     ├── Cooling still active → terminate with Commit; log skipped execution
  │     └── Cooling elapsed → set state to HALF-OPEN; run single test
  └── HALF-OPEN → run single test request
        ├── Success → set CLOSED; reset Consecutive_Failures; proceed
        └── Failure → reset cooling period; set OPEN again
```

---

## SECTION 8 — WEBHOOK REPLAY ATTACK PREVENTION

### 8.1 Timestamp Validation Window

All inbound webhooks (Webflow form submissions, Stripe events) must pass a timestamp validity check before any processing begins. The validation window is **5 minutes**.

### 8.2 Implementation

```
Step 1: Extract webhook timestamp from payload header or body
        - Stripe: X-Stripe-Signature header contains timestamp (t=...)
        - Webflow: X-W-Signature header; timestamp in body
Step 2: Compute age of webhook
        age_seconds = {{timestamp}} - {{now}}
Step 3: Filter: IF age_seconds > 300 (5 minutes) → reject
        └── Log to Automation_Failures: Error_Code = WEBHOOK_REPLAY
        └── Return HTTP 200 to sender (do not return 4xx — prevents retry storms)
        └── Terminate execution (Commit)
Step 4: IF age_seconds <= 300 → proceed to idempotency check (Section 6)
```

### 8.3 Stripe Signature Verification

Stripe webhooks additionally require signature verification using the Stripe signing secret:

```
Expected_Signature = HMAC-SHA256(
  key = STRIPE_WEBHOOK_SIGNING_SECRET,
  message = webhook_timestamp + "." + raw_request_body
)
Compare to: Stripe-Signature header value (v1=...)
IF mismatch → reject immediately; log STRIPE_INVALID_SIGNATURE; do not process
```

The Stripe signing secret is stored in Make as an encrypted Connection variable, never in plaintext in the scenario.

---

## SECTION 9 — ENVIRONMENT GUARD

### 9.1 Purpose

Every scenario must detect its operating environment at startup and refuse to run in the wrong context. A Production scenario must not process Sandbox records. A Sandbox scenario must not send real emails, real SMS, or real Stripe charges.

### 9.2 Implementation — Environment Check Module

**First module in every Stage 1 scenario after the trigger:**

```
Step 1: Read the Environment field from the triggering record
        (Requests.Environment, Bookings.Environment, etc.)
Step 2: Read the SCENARIO_ENVIRONMENT variable (set in Make scenario settings)
        - Production scenarios: SCENARIO_ENVIRONMENT = "Production"
        - Sandbox scenarios: SCENARIO_ENVIRONMENT = "Sandbox"
Step 3: Filter
  ├── Record.Environment = SCENARIO_ENVIRONMENT → proceed
  ├── Record.Environment = "Sandbox" AND SCENARIO_ENVIRONMENT = "Production"
  │     └── EXIT: Log skipped execution; return; no alert needed
  └── Record.Environment = "Production" AND SCENARIO_ENVIRONMENT = "Sandbox"
        └── EXIT: Log WARNING to Automation_Failures; alert Luciana immediately
              (Production record in Sandbox scenario = configuration error)
```

### 9.3 Sandbox Override for M-BRAND-ROUTER

M-BRAND-ROUTER is the entry point for all inbound webhooks. In Sandbox mode, M-BRAND-ROUTER appends `[SANDBOX]` to the brand routing tag and routes to sandbox-only versions of downstream scenarios. It never invokes the Production scenario IDs.

---

## SECTION 10 — FAILURE MODE HANDLING

### 10.1 Airtable API Rate Limit (HTTP 429)

Airtable's API rate limit is 5 requests per second per base. At high volume, M-LEAD-INTAKE or M-BOOKING-CREATION may hit this limit.

**Response:**
- Detect HTTP 429 response
- Do NOT count as a standard failure — 429 is expected under load
- Apply exponential backoff: wait 1s, then 2s, then 4s, then 8s (max 4 attempts)
- If 429 persists after 4 attempts → promote to Level 1 failure; write to Automation_Failures with Error_Code = AIRTABLE_RATE_LIMIT
- Log rate limit hit count in Make_Scenarios.Rate_Limit_Hits field for trending

### 10.2 Stripe Webhook Invalid Signature

**Response:**
- Return HTTP 200 to Stripe immediately (prevents Stripe from retrying)
- Log to Automation_Failures: Error_Code = STRIPE_INVALID_SIGNATURE
- Alert Luciana in #sss-ops-alerts immediately (Level 3 alert, not Level 1 — signature failures are security events)
- Do not process the payload under any circumstances
- Will reviews all STRIPE_INVALID_SIGNATURE events within 24 hours

### 10.3 Slack Connection Down

Slack connectivity failure affects M-SLACK-ALERTS. Because Slack is the alert channel itself, a failure here requires an alternative escalation path.

**Response:**
- Detect Slack API error (connection refused, token invalid, channel not found)
- Attempt Slack reconnect once after 30 seconds
- If still failing: write escalation to Airtable Automation_Failures as normal
- Send escalation email via Gmail to Luciana's personal email (hardcoded failsafe address stored in Make encrypted variables)
- If Gmail also down: create Founder Decision: COMM-FAILURE in Airtable; Will must check Airtable dashboard manually
- HEALTH-001 detects Slack downtime on next 15-minute poll

### 10.4 Gmail OAuth Token Expired

Gmail uses OAuth 2.0. Tokens expire and require refresh. Make auto-refreshes tokens, but the refresh can fail if the token was revoked or if Google's OAuth endpoint is unreachable.

**Response:**
- Detect OAuth error in Gmail module (401 Unauthorized or token_expired)
- Make's Gmail connection will attempt auto-refresh — allow one automatic retry
- If refresh fails: do NOT send email; queue the email content in a Pending_Comms field on the affected Booking or Request record
- Alert Luciana in #sss-ops-alerts: "Gmail OAuth expired — manual email required for [Client Name]"
- Provide Luciana with the full email content from the Pending_Comms field
- Log to Automation_Failures: Error_Code = GMAIL_OAUTH_EXPIRED

---

## SECTION 11 — SILENT FAILURE DETECTION (HEALTH-001)

### 11.1 The Problem

A silent failure occurs when a scenario stops executing — due to a Make plan limit, a disabled scenario, or an unhandled exception — without logging any record to Automation_Failures. The 4-level escalation hierarchy cannot catch what it does not know about.

### 11.2 HEALTH-001 Verification Method

HEALTH-001 runs every 15 minutes. It performs the following Audit Log verification:

```
Step 1: Query Audit_Log (tblrMpTfMk8q1eNHp) for all records created in the last 15 minutes
Step 2: For each active scenario (from Make_Scenarios registry), check:
        - Did this scenario produce at least one Audit_Log entry in the last hour?
        - Exception: scenarios with no triggers in the last hour (check trigger count)
Step 3: For any scenario with ZERO Audit_Log entries AND known triggers:
        └── This is a silent failure candidate
        └── Query Make_Scenarios.Last_Successful_Run timestamp
        └── If Last_Successful_Run > 30 minutes ago → alert Luciana: SILENT_FAILURE_SUSPECTED
Step 4: If any Audit_Log entry shows a gap > 60 minutes for M-AUDIT-LOGGER specifically:
        └── Alert Will immediately — the logging system itself may be compromised
```

### 11.3 Audit Log Gap Fields

The following fields on the Audit_Log table (tblrMpTfMk8q1eNHp) enable gap detection:

| Field | Type | Purpose |
|-------|------|---------|
| Scenario_Name | Single Line Text | Which scenario created this entry |
| Created_At | Date/Time (auto) | Timestamp of log entry |
| Execution_ID | Single Line Text | Make execution ID for cross-reference |
| Gap_Flag | Checkbox | HEALTH-001 sets true when gap detected |
| Gap_Duration_Minutes | Number | Minutes since prior log entry from same scenario |

### 11.4 Silent Failure Response

When HEALTH-001 detects a suspected silent failure:
1. Write an Automation_Failures record with Error_Code = SILENT_FAILURE_SUSPECTED
2. Alert Luciana via #sss-ops-alerts
3. If the silent failure persists for 30+ minutes without human acknowledgment, escalate to Will (DM)
4. Will must verify Make.com dashboard directly — check if the scenario is running, erroring, or disabled

---

*Document Authority: Will (Founder)*  
*Last Review: May 2026*  
*Next Review: 30 days post Stage 1 go-live*
