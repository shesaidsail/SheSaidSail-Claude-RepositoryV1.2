# ERROR_HANDLING_AND_RETRY_ARCHITECTURE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Unified failure handling framework for all Make scenarios.
**Classification:** Confidential — Internal Use Only

---

## PRINCIPLE

Every Make scenario fails at some point. Network timeouts, Airtable API rate limits, Stripe outages, Claude API errors — they all happen. The question is not "will it fail?" but "what happens when it fails?"

The goal of this framework is:
1. No silent failures (every failure is logged)
2. No lost data (every failure is retriable)
3. No cascading chaos (failures escalate clearly and are contained)
4. No duplicate records or duplicate messages (idempotency protects against retry damage)
5. No client impact from automation failures when possible

---

## SECTION 1 — STANDARD 4-FAILURE ESCALATION CHAIN

Every production scenario implements this escalation chain via Make's error handler routes:

```
Failure 1:
  → Log to Automation_Health (Airtable)
  → Retry after 2 minutes
  → Continue processing remaining records if applicable

Failure 2 (within 60 minutes of Failure 1):
  → Retry after 5 minutes
  → Increment failure_count in Automation_Health
  → Continue

Failure 3:
  → Retry after 10 minutes
  → Slack alert to Luciana in #sss-ops-alerts:
    "⚠️ Automation failure — [Scenario ID] — 3rd failure — [error message] — Monitoring"

Failure 4:
  → Slack DM to Will: "🚨 AUTOMATION FAILURE — [Scenario ID] — 4th failure — Manual intervention required"
  → Slack DM to Luciana: same
  → Scenario pauses (set to OFF in Make — requires manual re-enable after investigation)
  → Airtable > Create Record: Founder_Decisions (Type = SYSTEM, Urgency = SAME_DAY)
    Context: "Make scenario [ID] has failed 4 times. Manual recovery required."
```

**Implementation in Make:** Use Make's error handler module attached to every module group. Set the retry interval and escalation steps as described. The Slack and Airtable write steps in the error handler must themselves have try/catch logic — if they also fail, log to a local text variable and attempt Slack DM only as the last resort.

---

## SECTION 2 — IDEMPOTENCY ARCHITECTURE

Idempotency prevents the same action from executing twice when a scenario retries after a failure.

### 2.1 Idempotency Key Generation

```
SHA256(primary_identifier + scenario_id + date_bucket)

Examples:
M-LEAD-INTAKE:   SHA256(email + "M-LEAD-INTAKE" + date_of_submission)
M-STRIPE-DEPOSIT: Stripe payment_intent_id (already unique)
M-BASIC-LIFECYCLE (D1 send): SHA256(booking_id + "D1" + charter_date)
M-REVIEW-REQUEST: SHA256(booking_id + "D7-REVIEW")
M-REFERRAL-ENGINE: SHA256(booking_id + "D30-REFERRAL")
M-REBOOKING-ENGINE: SHA256(booking_id + "D60-REBOOKING")
```

### 2.2 Idempotency Check Pattern

Every scenario that creates records or sends messages performs this check before acting:

```
1. Calculate idempotency_key
2. Search Airtable: filter {Idempotency_Key} = {{idempotency_key}}
3. If record found with this key → EXIT gracefully (log: "Duplicate — already processed")
4. If no record found → proceed with action
5. After action: write idempotency_key to the record
```

### 2.3 Idempotency Fields Required Per Table

| Table | Field | Used By |
|-------|-------|---------|
| Requests | Idempotency_Key | M-LEAD-INTAKE |
| Bookings | Idempotency_Key | M-BOOKING-CREATION, M-STRIPE-DEPOSIT |
| Audit_Log | Idempotency_Key | All scenarios (check before Audit_Log write) |

### 2.4 Per-Message Idempotency (Lifecycle Sends)

For M-BASIC-LIFECYCLE, idempotency is managed via dedicated boolean fields on Bookings rather than a key field:

| Field | Protects Against |
|-------|-----------------|
| D72hr_Reminder_Sent | Sending T-72 reminder twice |
| D48hr_Reminder_Sent | Sending T-48 logistics twice |
| D24hr_Reminder_Sent | Sending T-24 reminder twice |
| D12hr_Reminder_Sent | Sending day-of message twice |
| D1_Sent | Sending D1 message twice |
| D7_Sent | Sending D7 review request twice |
| D30_Sent | Sending D30 referral twice |
| D60_Sent | Sending D60 rebooking twice |

These fields are written immediately after the send succeeds. If the scenario retries before the write, the message will be sent twice. To prevent this, the write to the boolean field must be the FIRST action after each send — not batched at the end.

---

## SECTION 3 — SCENARIO-SPECIFIC FAILURE MODES AND RESPONSES

### M-LEAD-INTAKE Failures

| Failure | Cause | Response |
|---------|-------|---------|
| Webhook authentication fails | Invalid bearer token | Return 401. Log. No Airtable action. |
| Airtable Create Record fails | API outage or rate limit | Retry × 4. If persistent: Slack Luciana with raw form data to create manually. |
| Slack post fails | Slack outage | Continue — Airtable record is the source of truth. Luciana checks Airtable directly. |
| Brand router returns error | Unexpected form payload | Default to SSS + LOW confidence. Proceed. Alert Luciana. |
| Duplicate submission detected | Idempotency key match | EXIT cleanly. No error, no action. |

### M-STRIPE-DEPOSIT Failures

| Failure | Cause | Response |
|---------|-------|---------|
| Stripe signature invalid | Invalid webhook or replay | Return 401. Do not process. |
| Booking not found by metadata | Metadata incomplete | Luciana DM with full Stripe event JSON. Manual match required. |
| Airtable update fails | Rate limit or outage | Retry × 4. Stripe will retry webhook delivery for up to 72 hours — idempotency key protects against duplicate processing when retry succeeds. |
| Gmail send fails | Gmail outage | Log in Audit_Log. Luciana DM to send manually. Booking is still marked DEPOSIT_PAID in Airtable — the source of truth is correct. |
| Return non-200 to Stripe | Any unhandled error | Stripe retries. Idempotency key on Bookings.Idempotency_Key prevents duplicate status updates. |

### M-BASIC-LIFECYCLE Failures

| Failure | Cause | Response |
|---------|-------|---------|
| One booking record causes error | Bad data, missing field | Log error for that record. Continue to next booking. Never halt full run. |
| Gmail send fails | Gmail outage | SMS only fallback if phone available. Both fail → Luciana DM with message content. |
| Stripe balance link creation fails | Stripe outage | Send reminder without link. Add note: "Balance link unavailable — Luciana to send manually." |
| Schedule doesn't fire | Make plan issue or Make outage | M-AUTOMATION-HEALTH detects: last lifecycle run > 25 hours → SEV-2 alert |

### M-CHARTER-BRIEF Failures

| Failure | Cause | Response |
|---------|-------|---------|
| Claude API unavailable | Anthropic outage | Do not generate brief. Luciana DM: "Charter Brief AI unavailable for [Booking ID]. Please create manually using the Airtable template." |
| Missing required booking fields | Incomplete data | Block brief generation. List specific missing fields. Luciana DM. |
| AI_Prompt_Versions — no qualifying version | No LIVE + Will_Approved version for CHARTER_BRIEF_SYSTEM | Block. Luciana DM. Will must approve prompt version before brief can generate. |

### M-ESCALATION-ROUTER Failures

| Failure | Cause | Response |
|---------|-------|---------|
| Escalation routing error | Unexpected Escalation_Reason value | Default to L2 (Luciana). Never drop an escalation. |
| Slack DM to Will fails | Will's Slack ID misconfigured | Post to #sss-emergency-ops as fallback. |
| Founder_Decisions creation fails | Airtable outage | Retry × 4. Post full escalation details to #sss-emergency-ops and DM Luciana with raw data. |

### M-AUTOMATION-HEALTH Failures

| Failure | Cause | Response |
|---------|-------|---------|
| Health check itself fails | Make outage or Airtable outage | Cannot self-alert. Daily human review of #sss-ops-alerts is the safety net. Will checks this channel every morning. |
| False positive anomaly | Data anomaly in Airtable | Luciana investigates and marks Automation_Health record as Resolved. Pattern logged for SEV threshold review. |

### M-SYNTER-SYNC Failures

| Failure | Cause | Response |
|---------|-------|---------|
| P&L Per Charter write fails | Financials base outage | Retry × 4. Set Financial_Sync_Status = FAILED on Booking. M-AUTOMATION-HEALTH catches all FAILED syncs within 24 hours. |
| Completed booking has no P&L after 24 hours | FAILED sync not yet resolved | M-AUTOMATION-HEALTH: SEV-2 alert to Luciana. Manual sync or re-trigger required. |

---

## SECTION 4 — CIRCUIT BREAKER PATTERN

For M-AUTOMATION-HEALTH, implement a circuit breaker to prevent alert flooding:

```
IF anomaly_count > 10 in last 30 minutes:
  → Send one consolidated SEV-1 alert (not 10 individual alerts)
  → Pause M-AUTOMATION-HEALTH for 30 minutes
  → Will reviews and re-enables manually

This prevents: alert fatigue that causes Will or Luciana to start ignoring alerts
```

---

## SECTION 5 — STRIPE-SPECIFIC ERROR HANDLING

Stripe has specific error categories that require specific responses:

| Stripe Error Code | Meaning | Make Response |
|------------------|---------|--------------|
| `payment_intent.payment_failed` + `insufficient_funds` | Client card declined | M-FAILED-PAYMENT-HANDLER — friendly retry message |
| `payment_intent.payment_failed` + `card_declined` | Card declined (generic) | M-FAILED-PAYMENT-HANDLER — retry message + Luciana DM on 2nd failure |
| `payment_intent.payment_failed` + `authentication_required` | 3D Secure required | New payment link with 3D Secure enabled |
| `payment_intent.payment_failed` + `expired_card` | Card expired | Client message: "Your card on file has expired — please use the updated link with a new card" |
| Webhook signature invalid | Replay attack or misconfiguration | 401 response. Log IP. No processing. |
| Rate limit from Stripe API | Too many API calls | Back off 30 seconds. Retry once. If second failure → Luciana DM. |

---

## SECTION 6 — CLAUDE API ERROR HANDLING

All scenarios calling the Claude API implement this fallback:

```
Claude API Call succeeds:
  → Process response normally

Claude API times out (> 30 seconds):
  → Retry once after 10 seconds
  → If second timeout: use graceful degradation

Claude API returns error (non-200):
  → Log error code and message in Audit_Log
  → Graceful degradation

Graceful Degradation Rules by Scenario:
  M-CHARTER-BRIEF → Do not generate. Alert Luciana to create manually.
  M-AI-LEAD-SCORING → Set AI_Lead_Priority = "UNSCORED". Luciana prioritizes manually.
  M-FOUNDER-DIGEST → Send digest with data tables only, no AI synthesis section. Note: "AI synthesis unavailable this week."
  M-PRICING-INTELLIGENCE → Skip this run. Will receives Slack note: "Pricing intelligence skipped — Claude API unavailable."
  M-CONCIERGE-INTELLIGENCE → Skip this run. Same.
```

---

## SECTION 7 — AIRTABLE API ERROR HANDLING

Airtable API rate limits and error codes:

| Error | Cause | Response |
|-------|-------|---------|
| 429 Too Many Requests | Rate limit hit (5 req/sec per base) | Make retries with exponential backoff: 2s, 4s, 8s, 16s |
| 422 Unprocessable Entity | Invalid field value | Log exact payload. Luciana DM with field details. |
| 404 Not Found | Record ID doesn't exist | Log. Investigate data integrity. Luciana DM. |
| 503 Service Unavailable | Airtable outage | Retry × 4 with 5-minute gaps. SEV-2 if persistent > 30 minutes. |
| Record locked | Native Airtable record lock | Wait 30 seconds. Retry once. Log if still locked. |

**Rate Limit Management:**
- M-BASIC-LIFECYCLE adds 500ms delay between individual booking processing loops to avoid hitting rate limits on large booking volumes
- M-VENDOR-NOTIFICATIONS adds 2s delay between individual vendor email sends

---

## SECTION 8 — EMERGENCY OVERRIDE

When Emergency_Flag = true on a Booking, all automation for that booking halts immediately. This is implemented as the first conditional check in every scenario that reads a Booking record:

```
Module: CHECK — Emergency_Flag
Type: Router
Conditions:
  Route 1 (Emergency active): Emergency_Flag = true → EXIT path
  Route 2 (Normal): Emergency_Flag = false → continue

EXIT path:
  1. Log to Audit_Log: "Scenario [ID] halted — Emergency_Flag active on Booking [ID]"
  2. No further actions. No messages. No writes.
  3. Return success response to webhook (200 OK) to prevent Stripe/Webflow from retrying
```

This check is non-negotiable. It executes before any outbound action in every scenario that touches a Booking record.

---

## SECTION 9 — ROLLBACK-SAFE DESIGN

All scenarios that write to Airtable are designed to be rollback-safe:

**Write order priority:**
1. Write the idempotency key FIRST (prevents re-execution on rollback)
2. Write the state-changing field (Status update, boolean flag)
3. Write audit log entry LAST (confirms completion)

**Never batch these writes** — if the scenario fails between writes 2 and 3, the idempotency key prevents re-processing, and the missing audit log entry flags the incomplete action for investigation.

**Financial field protection:**
- No Make scenario writes to `Package_Price`, `Net_Profit`, `Net_Margin_Pct` on Bookings after Status = CONFIRMED
- If a scenario attempts this write (logic error), Airtable field permission should be set to read-only for API tokens after CONFIRMED status
- Make includes a pre-write check: if Status = CONFIRMED AND target field is protected → abort + Will DM

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*ERROR_HANDLING_AND_RETRY_ARCHITECTURE v1.0*
*Effective May 2026*
