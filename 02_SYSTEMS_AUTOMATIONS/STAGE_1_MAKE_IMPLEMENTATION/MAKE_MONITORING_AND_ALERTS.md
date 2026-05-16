# MAKE_MONITORING_AND_ALERTS

**Status:** PRODUCTION SPECIFICATION
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Ops Lead:** Luciana
**Scope:** She Said Sail + Mare Executive — All Stage 1 Make Scenarios
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED

---

## 1. MONITORING PHILOSOPHY

**Principle: Proactive Detection, Not Reactive Response.**

The monitoring system does not wait for a failure to become visible. It actively interrogates automation state every 15 minutes and generates alerts before a failure cascades into a client-facing incident. The cost of a missed alert is not an inconvenient notification — it is a client receiving no deposit link, a booking state stuck in limbo, a financial sync gap that requires manual reconciliation, or an emergency flag that nobody sees.

**Three non-negotiable monitoring rules:**

1. **Every autonomous action is audited before it is considered complete.** No Make scenario is allowed to execute a Tier A action without a corresponding Audit Log entry. A missing audit entry is not a logging failure — it is a system integrity failure that triggers the same response as a scenario crash.

2. **The monitoring system cannot itself be a single point of failure.** HEALTH-001 must be independently verifiable. If HEALTH-001 stops running, a secondary heartbeat detects this absence within 30 minutes and alerts Will directly.

3. **Alert fatigue kills safety culture.** Alerts are graded by severity. SEV-4 notifications accumulate in a dashboard digest. Only SEV-1 and SEV-2 create immediate interruption. A noisy monitoring system trains operators to ignore it.

**Monitoring covers four domains:**

| Domain | What Is Monitored | Why |
|--------|-------------------|-----|
| Scenario Execution | Failure counts, retry loops, execution gaps | Catch automation breakdowns before they affect clients |
| Data Integrity | Audit Log completeness, duplicate detection | Ensure every autonomous action is traceable and reversible |
| External Systems | Stripe latency, Airtable API error rate | Catch third-party degradation before scenarios fail |
| Operational Safety | Emergency_Flag count, Automations_Paused state | Ensure human override signals are immediately visible |

---

## 2. HEALTH CHECK SCENARIO DESIGN — HEALTH-001

### 2.1 Trigger Configuration

| Parameter | Value |
|-----------|-------|
| Scenario Name | M-HEALTH-001 |
| Trigger Type | Scheduled — Time-based |
| Schedule | Every 15 minutes, 24/7 |
| Environment | Production |
| Timeout | 120 seconds max execution |
| Max Consecutive Failures Before Escalation | 2 (30-minute gap = SEV-2) |

### 2.2 Execution Sequence

```
Step 1:  Read Automation_Health table — all records updated in last 60 minutes
Step 2:  Read Audit Log — check for any gap > 15 minutes during active hours (8am–10pm)
Step 3:  Read Automation_Failures table — count failures in last 60 minutes
Step 4:  Read Bookings table — count records where Emergency_Flag = true
Step 5:  Check Stripe webhook last-received timestamp (read from Automation_Health)
Step 6:  Check Airtable API call log — calculate error rate in last 60 minutes
Step 7:  Check BACKUP-001 last successful run timestamp
Step 8:  Evaluate all metric thresholds (see Section 3)
Step 9:  Route alerts by severity (see Section 5)
Step 10: Write HEALTH-001 result record to Automation_Health table
Step 11: [If all checks pass] Write OK heartbeat to Automation_Health
Step 12: [If HEALTH-001 itself fails] Trigger HEALTH-FAILSAFE (see Section 10)
```

### 2.3 HEALTH-001 Data Requirements

HEALTH-001 depends on the following fields being readable at runtime. These are prerequisites — if any are absent, HEALTH-001 cannot execute correctly.

| Airtable Field | Table | Used For |
|---------------|-------|----------|
| Emergency_Flag | Bookings | SEV-1 emergency detection |
| Automations_Paused | Bookings | Verify override state is propagated |
| Last_Execution_Timestamp | Automation_Health | Gap detection per scenario |
| Last_Success_Timestamp | Automation_Health | Distinguish failure from slow execution |
| Failure_Count_1hr | Automation_Health | Failure threshold evaluation |
| Stripe_Last_Webhook_Received | Automation_Health | Latency monitoring |
| Airtable_API_Error_Count_1hr | Automation_Health | Error rate calculation |
| Backup_Last_Successful_Run | Automation_Health | Backup age check |
| Environment | All tables | Sandbox/production isolation |

---

## 3. METRICS AND THRESHOLDS

### 3.1 Automation Failure Count

| Metric | Definition | Warning Threshold | Alert Threshold | Severity |
|--------|-----------|------------------|-----------------|---------|
| Failures per hour | Count of records in Automation_Failures where Created_At > NOW()-60min | 2 failures | >3 failures | SEV-2 at warning; SEV-1 at alert |

**Detection logic:**

```
airtable_failure_count = COUNT(Automation_Failures WHERE Created_At > NOW() - 60 MINUTES)
IF airtable_failure_count == 2 → log WARNING to Automation_Health
IF airtable_failure_count > 3 → trigger SEV-2 alert → Luciana (#sss-ops-alerts)
IF airtable_failure_count > 6 → trigger SEV-1 alert → Will (DM) + #sss-emergency-ops
```

**Rationale:** 1–2 failures per hour is within acceptable retry behavior. More than 3 indicates a systemic issue: API degradation, schema change, or a scenario in a crash loop. More than 6 means multiple scenarios are failing simultaneously — a probable platform-level incident.

---

### 3.2 Audit Log Gap Detection

| Metric | Definition | Alert Threshold | Severity |
|--------|-----------|-----------------|---------|
| Audit gap | Any Tier A autonomous action executed without a corresponding Audit Log entry | Any single gap detected | SEV-1 |

**This is an unconditional SEV-1. There is no warning tier.**

**Detection logic:**

```
Step 1: Read Automation_Health — all Scenario_Last_Action_Timestamp values
Step 2: For each scenario that executed in the last 60 minutes, query Audit Log
        WHERE Scenario_ID = [scenario] AND Created_At > [last execution timestamp - 5 min]
Step 3: IF zero Audit Log records found for a scenario that executed → SEV-1
Step 4: Write gap detection event to Automation_Failures with Error_Code = AUDIT-GAP-001
Step 5: Alert Will directly — DM + #sss-emergency-ops
```

**Why this is SEV-1:** An autonomous action with no audit trail is ungoverned behavior. It cannot be reviewed, reversed, or attributed. Any autonomous action that does not produce an Audit Log entry represents a systemic failure in the governance layer, not just an automation failure.

---

### 3.3 Stripe Webhook Latency

| Metric | Definition | Warning Threshold | Alert Threshold | Severity |
|--------|-----------|------------------|-----------------|---------|
| Stripe webhook lag | Time between Stripe event timestamp and Make scenario execution start | >2 minutes | >5 minutes | SEV-3 at warning; SEV-2 at alert |

**Detection logic:**

```
stripe_last_webhook_ts = READ Automation_Health.Stripe_Last_Webhook_Received
stripe_last_processed_ts = READ Automation_Health.Stripe_Last_Processed
latency_minutes = (stripe_last_processed_ts - stripe_last_webhook_ts) / 60

IF latency_minutes > 2 → log WARNING
IF latency_minutes > 5 → SEV-2 alert → Luciana
IF latency_minutes > 15 → SEV-1 alert → Will → check Stripe status page
IF no webhook received in 24 hours AND active bookings exist → SEV-2 → verify Stripe connectivity
```

**Mitigation context:** Stripe webhook delivery is typically sub-second. Latency above 2 minutes indicates Make queue backup or Stripe delivery retry. Above 5 minutes, deposit confirmation is being delayed, which can block booking status progression and frustrate clients expecting instant confirmation.

---

### 3.4 Airtable API Error Rate

| Metric | Definition | Warning Threshold | Alert Threshold | Severity |
|--------|-----------|------------------|-----------------|---------|
| API error rate | Percentage of Airtable API calls returning 4xx or 5xx in last 60 minutes | >2% | >5% | SEV-3 at warning; SEV-2 at alert |

**Detection logic:**

```
total_api_calls_1hr = READ Automation_Health.Airtable_API_Calls_1hr
error_api_calls_1hr = READ Automation_Health.Airtable_API_Errors_1hr
error_rate = (error_api_calls_1hr / total_api_calls_1hr) * 100

IF error_rate > 2 → log WARNING to Automation_Health
IF error_rate > 5 → SEV-2 alert → Luciana → verify Airtable status
IF error_rate > 20 → SEV-1 alert → Will → consider pausing all scenarios
```

**Note:** 429 (rate limit) errors are classified separately. Sustained 429s indicate Make scenario fan-out exceeding Airtable's API limits (5 req/sec per base). This requires scenario throttling, not just alerting.

---

### 3.5 Last Backup Age

| Metric | Definition | Warning Threshold | Alert Threshold | Severity |
|--------|-----------|------------------|-----------------|---------|
| Backup age | Hours since last confirmed successful BACKUP-001 run | >24 hours | >48 hours | SEV-3 at warning; SEV-2 at alert |

**Detection logic:**

```
backup_last_run = READ Automation_Health.Backup_Last_Successful_Run
backup_age_hours = (NOW() - backup_last_run) / 3600

IF backup_age_hours > 24 → SEV-3 WARNING → log to Automation_Health
IF backup_age_hours > 48 → SEV-2 alert → Luciana → investigate BACKUP-001 failure
IF backup_age_hours > 72 → SEV-1 alert → Will → manual backup required immediately
```

**Rationale:** BACKUP-001 runs at 2am daily. Under normal conditions, the max age is ~24 hours. An alert at 48 hours means BACKUP-001 has missed at least one full cycle. At 72 hours, active charter data is at risk of unrecoverable loss if an Airtable incident occurs.

---

### 3.6 Emergency Flag Count

| Metric | Definition | Alert Threshold | Severity |
|--------|-----------|-----------------|---------|
| Active emergency flags | COUNT of Bookings where Emergency_Flag = true | Any value > 0 | SEV-1 — immediate |

**This metric has no warning tier. Any Emergency_Flag = true triggers SEV-1 immediately.**

**Detection logic:**

```
emergency_flag_count = COUNT(Bookings WHERE Emergency_Flag = true AND Environment = Production)

IF emergency_flag_count > 0:
  → SEV-1 immediately
  → Slack DM to Will
  → Message to #sss-emergency-ops
  → Log to Automation_Failures with Error_Code = EMERGENCY-FLAG-DETECTED
  → Do NOT send any other outbound messages until Will clears the flag
```

**Note:** HEALTH-001 does not create the Emergency Escalation record — that is M-EMERGENCY-001's responsibility when the flag is first set. HEALTH-001's role is to detect if Emergency_Flag is still active and ensure the alert has been received. If HEALTH-001 detects an active flag and no Emergency Escalation record exists for that Booking within the last 30 minutes, it creates a secondary alert: `EMERGENCY-FLAG-NO-ESCALATION-RECORD` at SEV-1.

---

## 4. ALERT ROUTING MATRIX

| Alert Type | Primary Recipient | Channel | Secondary Recipient | Channel | Condition |
|-----------|-------------------|---------|--------------------|---------| --------- |
| Automation failure > 3/hr | Luciana | #sss-ops-alerts | Will (DM) | Slack DM | Failure count > 6 |
| Audit Log gap detected | Will | Slack DM | — | #sss-emergency-ops | Always |
| Stripe latency > 5 min | Luciana | #sss-ops-alerts | Will | Slack DM | Latency > 15 min |
| Airtable error rate > 5% | Luciana | #sss-ops-alerts | Will | Slack DM | Error rate > 20% |
| Backup age > 48 hours | Luciana | #sss-ops-alerts | Will | Slack DM | Age > 72 hours |
| Emergency_Flag > 0 | Will | Slack DM | Luciana | #sss-emergency-ops | Always |
| HEALTH-001 itself fails | Will | Slack DM | Luciana | #sss-ops-alerts | Always |
| SEV-1 any cause | Will | Slack DM | Luciana | #sss-emergency-ops | Always |
| Sandbox write to production | Will | Slack DM | — | #sss-emergency-ops | Immediate stop |

**Luciana (#sss-ops-alerts):** Primary operations triage. Handles SEV-3 and SEV-4 independently. Escalates SEV-1 and SEV-2 to Will if Will has not already been alerted.

**Will (DM + #sss-emergency-ops):** Final authority on all SEV-1 events. Only Will may clear an Emergency_Flag, authorize manual recovery, or approve scenario pause during active charter hours.

---

## 5. SEVERITY CLASSIFICATION

### SEV-1 — System Critical

**Definition:** Active harm is possible or occurring. Client-facing operations are at risk or are failing. Emergency flags are active. Audit trail has gaps. Human override is required immediately.

| Attribute | Value |
|-----------|-------|
| Response Time | Will responds within 15 minutes, 24/7 |
| Notification | Slack DM to Will + #sss-emergency-ops message |
| Auto-Action | All affected scenarios paused pending Will decision |
| Resolution Path | Will initiates manual recovery or authorizes specific scenario restart |
| Post-Incident | Postmortem required within 24 hours; Lesson record created |

**SEV-1 triggers:**
- Emergency_Flag detected on any active Booking
- Audit Log gap on any Tier A scenario
- HEALTH-001 offline for > 30 minutes
- Sandbox scenario confirmed to have written to production records
- Any automation failure cascading across 4+ scenarios simultaneously

---

### SEV-2 — Operations Degraded

**Definition:** Automation reliability is reduced. No immediate client harm, but SLA timelines are at risk if not resolved within the hour.

| Attribute | Value |
|-----------|-------|
| Response Time | Luciana responds within 30 minutes during business hours; Will notified if after 9pm |
| Notification | #sss-ops-alerts message + Luciana DM |
| Auto-Action | Affected scenario logged to Automation_Failures; retry logic continues |
| Resolution Path | Luciana investigates; escalates to Will if unresolved after 60 minutes |
| Post-Incident | Operations note added to Lessons table |

**SEV-2 triggers:**
- Automation failure count > 3 per hour
- Stripe webhook latency > 5 minutes
- Airtable API error rate > 5%
- Backup age > 48 hours
- Single scenario in crash loop (>4 consecutive failures)

---

### SEV-3 — Warning State

**Definition:** Metrics are trending toward threshold. No immediate operational impact. Requires awareness and monitoring, not immediate action.

| Attribute | Value |
|-----------|-------|
| Response Time | Luciana reviews within 2 hours |
| Notification | #sss-ops-alerts message (no DM) |
| Auto-Action | Log to Automation_Health; flag in dashboard |
| Resolution Path | Luciana monitors; escalates if condition persists past next HEALTH-001 check |
| Post-Incident | None required unless escalated |

**SEV-3 triggers:**
- Automation failures: 2 per hour (approaching threshold)
- Stripe latency > 2 minutes
- Airtable error rate > 2%
- Backup age > 24 hours

---

### SEV-4 — Informational

**Definition:** System is operating normally. This entry is for visibility and trend analysis only.

| Attribute | Value |
|-----------|-------|
| Response Time | No action required |
| Notification | Dashboard digest (no Slack message) |
| Auto-Action | Log to Automation_Health |
| Resolution Path | None |

**SEV-4 examples:**
- HEALTH-001 completes successfully — all checks pass
- Scenario execution time within normal range
- BACKUP-001 completed successfully
- New record created in Audit Log (routine)

---

## 6. AUTOMATION HEALTH TABLE SPECIFICATION

### Table: Automation_Health

**Location:** SSS Operations base (appdZ49WqgjRXxA1R)
**Table Purpose:** One row per Make scenario per day. Tracks execution state, send states, and health check outcomes. Written by HEALTH-001 and by each scenario on execution. This table replaces the 20+ send-state fields formerly scattered across the Bookings table.

| Field Name | Type | Written By | Purpose |
|-----------|------|-----------|---------|
| UUID | Formula: RECORD_ID() | System | Immutable identifier |
| Scenario_ID | Single Line Text | Each scenario | M-BRAND-ROUTER, M-LEAD-INTAKE, etc. |
| Booking_ID | Linked Record → Bookings | Each scenario | Links health record to booking |
| Environment | Single Select: Production / Sandbox | Each scenario | Isolation gate |
| Brand | Single Select: SSS / ME | Each scenario | Brand context |
| Last_Execution_Timestamp | DateTime | Each scenario | When scenario last ran |
| Last_Success_Timestamp | DateTime | Each scenario | When scenario last succeeded |
| Execution_Status | Single Select: SUCCESS / FAILURE / RETRY / SKIPPED | Each scenario | Current state |
| Failure_Count_Total | Number | Each scenario on failure | Cumulative failures for this record |
| Failure_Count_1hr | Rollup / Make-written | HEALTH-001 | Failures in last 60 minutes |
| Last_Error_Code | Single Line Text | Each scenario | E.g., LEAD-INTAKE-429-2026051614 |
| Last_Error_Message | Long Text | Each scenario | Full error payload |
| Idempotency_Key_Used | Single Line Text | Each scenario | Key used for deduplication |
| Audit_Log_Ref | Single Line Text | Each scenario | AUD-YYYY-NNNN reference |
| Stripe_Last_Webhook_Received | DateTime | M-STRIPE-DEPOSIT | Stripe latency tracking |
| Stripe_Last_Processed | DateTime | M-STRIPE-DEPOSIT | Processing timestamp |
| Airtable_API_Calls_1hr | Number | HEALTH-001 | Total calls in window |
| Airtable_API_Errors_1hr | Number | HEALTH-001 | Error calls in window |
| Backup_Last_Successful_Run | DateTime | M-BACKUP-001 | For age check |
| Health_Check_Result | Single Select: OK / WARNING / CRITICAL | HEALTH-001 | Summary result |
| Health_Check_Timestamp | DateTime | HEALTH-001 | When HEALTH-001 ran |
| Alert_Sent | Checkbox | HEALTH-001 | Prevents duplicate alert sends |
| Alert_Severity | Single Select: SEV-1 / SEV-2 / SEV-3 / SEV-4 | HEALTH-001 | Severity of last alert |
| Created_At | DateTime | System | Record creation timestamp |
| Source_System | Single Select: Make | System | Always Make for this table |

**Write access:** Make API token only. No manual edits. No Airtable native automation writes to this table.

**Circular trigger risk:** LOW. HEALTH-001 writes to this table but does not trigger on it. No Airtable automations watch this table.

---

## 7. SLACK ALERT MESSAGE TEMPLATES

All Slack alert messages follow a consistent structure: `[SEVERITY]` badge, scenario context, specific metric, and required action. Messages are assembled in Make using text aggregators before the Slack send module.

### 7.1 SEV-1: Emergency Flag Detected

```
🚨 *SEV-1 EMERGENCY — ACTIVE FLAG DETECTED*

*Booking:* {{booking_id}} — {{client_name}}
*Charter Date:* {{charter_date}}
*Flag Set At:* {{emergency_flag_timestamp}}
*Environment:* Production

All outbound automations for this booking are paused.

*Required Action:* Only Will can clear this flag.
→ Review Emergency Escalation record in Airtable
→ Reply here when flag is cleared or manual action taken

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.2 SEV-1: Audit Log Gap

```
🚨 *SEV-1 AUDIT FAILURE — MISSING AUDIT LOG ENTRY*

*Scenario:* {{scenario_id}}
*Expected Audit Entry After:* {{scenario_execution_timestamp}}
*Gap Duration:* {{gap_minutes}} minutes

This means an autonomous action executed without a traceable record.
This is a governance integrity failure.

*Required Action:* Will reviews immediately.
→ Identify what action executed (check scenario execution history in Make)
→ Manually create Audit Log entry if action is confirmed
→ Investigate why M-AUDIT-LOGGER did not write

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.3 SEV-2: Automation Failure Threshold

```
⚠️ *SEV-2 — AUTOMATION FAILURE THRESHOLD EXCEEDED*

*Failures in Last Hour:* {{failure_count}} (threshold: 3)
*Most Recent Failing Scenario:* {{last_failing_scenario}}
*Last Error Code:* {{last_error_code}}

*Required Action:* Luciana investigates within 30 minutes.
→ Check Automation_Failures table in Airtable
→ Review Make scenario execution history
→ If unresolved in 60 min, escalate to Will

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.4 SEV-2: Stripe Webhook Latency

```
⚠️ *SEV-2 — STRIPE WEBHOOK LATENCY ALERT*

*Last Webhook Received:* {{stripe_last_webhook_ts}}
*Last Processed:* {{stripe_last_processed_ts}}
*Latency:* {{latency_minutes}} minutes (threshold: 5)

Deposit confirmations may be delayed. Booking status progression is at risk.

*Required Action:* Luciana checks Stripe status page and Make webhook log.
→ https://status.stripe.com
→ Verify webhook endpoint is active in Make

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.5 SEV-2: Airtable API Error Rate

```
⚠️ *SEV-2 — AIRTABLE API ERROR RATE ELEVATED*

*Error Rate (Last Hour):* {{error_rate_pct}}% (threshold: 5%)
*Total API Calls:* {{total_api_calls}}
*Errors:* {{error_count}}

Make scenarios are experiencing Airtable connectivity issues.
Records may not be writing correctly.

*Required Action:* Luciana checks Airtable status page.
→ https://status.airtable.com
→ If confirmed degradation, notify Will and consider pausing non-critical scenarios

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.6 SEV-2: Backup Overdue

```
⚠️ *SEV-2 — BACKUP OVERDUE*

*Last Successful Backup:* {{backup_last_run}}
*Age:* {{backup_age_hours}} hours (threshold: 48)

BACKUP-001 has missed at least one scheduled run.

*Required Action:* Luciana investigates BACKUP-001 failure.
→ Check Make scenario execution history for BACKUP-001
→ Manually trigger backup if scenario is broken
→ If storage destination is down, notify Will

_Detected by HEALTH-001 at {{health_check_timestamp}}_
```

### 7.7 SEV-1: HEALTH-001 Offline

```
🚨 *SEV-1 — MONITORING SYSTEM OFFLINE*

*HEALTH-001 has not executed in {{gap_minutes}} minutes.*
*Last Confirmed Run:* {{last_health_run}}

All monitoring coverage is suspended. System state is unknown.

*Required Action:* Will reviews immediately.
→ Check Make scenario status for HEALTH-001
→ If scenario is paused or erroring, restart manually
→ Run manual health check: review Automation_Failures and Audit Log directly

_This alert was generated by the HEALTH-FAILSAFE heartbeat._
```

---

## 8. DASHBOARD VISIBILITY REQUIREMENTS

The Ops Portal health section surfaces the following monitoring data for Luciana and Will. These are read-only views — no actions are taken from the dashboard without first reviewing the full Airtable record.

### 8.1 Health Status Panel (Ops Portal)

| Widget | Data Source | Refresh |
|--------|------------|---------|
| Overall System Status | Automation_Health.Health_Check_Result (most recent) | Live |
| Last HEALTH-001 Run | Automation_Health.Health_Check_Timestamp | Live |
| Active Emergency Flags | COUNT(Bookings WHERE Emergency_Flag = true) | Live |
| Failure Count (Last Hour) | Automation_Health.Failure_Count_1hr | Live |
| Stripe Webhook Latency | Automation_Health.Stripe latency calculation | Live |
| Airtable Error Rate | Automation_Health.Airtable_API_Errors_1hr / API_Calls_1hr | Live |
| Backup Age | NOW() - Automation_Health.Backup_Last_Successful_Run | Live |
| Open Audit Gaps | COUNT(Automation_Failures WHERE Error_Code CONTAINS 'AUDIT-GAP') | Live |

### 8.2 Scenario Execution Grid

One row per Stage 1 scenario showing:
- Scenario ID and name
- Last execution timestamp
- Last success timestamp
- Current status (OK / WARNING / FAILING)
- Failure count (24hr)

### 8.3 Alert History Feed

Chronological list of all alerts fired in the last 7 days, with:
- Timestamp, severity, scenario, message excerpt, and resolution status.

---

## 9. ESCALATION PATH WHEN MONITORING ITSELF FAILS

HEALTH-001 is itself a Make scenario. It can fail. The following redundancy architecture protects against blind spots in the monitoring layer.

### 9.1 HEALTH-FAILSAFE Mechanism

A secondary scheduled scenario — HEALTH-FAILSAFE — runs every 30 minutes with a single purpose: verify that HEALTH-001 has written a record to Automation_Health within the last 20 minutes. If not, HEALTH-FAILSAFE sends a SEV-1 alert to Will's personal Slack DM and posts to #sss-emergency-ops.

HEALTH-FAILSAFE has no other dependencies. It reads only one field from one table. It is the simplest possible scenario and is intentionally kept minimal to minimize its own failure surface.

### 9.2 Manual Verification Procedure

If both HEALTH-001 and HEALTH-FAILSAFE are offline simultaneously (a scenario requiring platform-level Make failure):

**Will performs the manual health check:**

```
Step 1: Open Airtable → Automation_Failures table
         Filter: Created_At > NOW() - 2 hours
         Review all records

Step 2: Open Airtable → Audit Log table
         Filter: Created_At > NOW() - 2 hours
         Confirm all expected scenario actions are logged

Step 3: Open Airtable → Bookings table
         Filter: Emergency_Flag = true
         If any active: manually notify Luciana

Step 4: Log manual health check to Automation_Health manually
         Source_System = Manual
         Health_Check_Result = [result]
         Note: "HEALTH-001 offline — manual check performed by Will"

Step 5: Open Make dashboard → check HEALTH-001 scenario status
         If inactive: activate and run once manually
         If error: review error and correct before reactivating
```

### 9.3 Platform-Level Failure

If Make is completely offline (not just a single scenario failure), all automation is suspended. In this state:

1. Luciana manually checks active charter bookings in Airtable
2. Any pending Stripe deposits are communicated to clients manually via Gmail
3. Will is notified of Make outage via direct contact (not Slack, which may also be affected)
4. No autonomous actions are taken until Make is confirmed operational
5. Upon restoration, all scenarios are restarted in order: M-HEALTH-001 first, then M-AUDIT-LOGGER, then operational scenarios
6. A postmortem Lesson record is created documenting the outage duration and any client impact

---

*End of MAKE_MONITORING_AND_ALERTS*
*Governed by Systems Intelligence Architecture v2.0 — Section XVI*
*Any modification to thresholds, severity classifications, or alert routing requires Will approval and a Deployment Log entry*
