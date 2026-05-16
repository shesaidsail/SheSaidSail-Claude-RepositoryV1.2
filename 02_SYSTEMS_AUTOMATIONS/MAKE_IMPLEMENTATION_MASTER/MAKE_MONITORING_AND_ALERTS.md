# MAKE_MONITORING_AND_ALERTS

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** System health monitoring architecture and alert routing for all Make scenarios.
**Classification:** Confidential — Internal Use Only

---

## MONITORING PHILOSOPHY

The goal of monitoring is not to generate reports. It is to give Will and Luciana the earliest possible signal that something is wrong before a client is affected. Every alert must be:

1. **Actionable** — "X happened, here's what to do"
2. **Routed correctly** — right person, right channel, right urgency
3. **Not noisy** — false positives erode trust in alerts and cause alert fatigue
4. **Self-recovering where possible** — retry logic handles transient failures automatically; alerts fire only when human intervention is needed

---

## SECTION 1 — MONITORING LAYERS

### Layer 1: Make Built-In Error Handler (Per Scenario)

Every scenario has an error handler attached that catches module-level failures. This is the first line of defense. It retries and escalates per the 4-failure chain in ERROR_HANDLING_AND_RETRY_ARCHITECTURE.md.

**What it monitors:** Individual module failures within a single scenario execution
**Response time:** Immediate (on failure)
**Alert channel:** #sss-ops-alerts (Failure 3), DM to Will + Luciana (Failure 4)

### Layer 2: M-AUTOMATION-HEALTH (Every 15 Minutes)

The M-AUTOMATION-HEALTH scenario runs every 15 minutes and looks for systemic issues that per-scenario handlers cannot detect:

- Scheduled scenarios not running on time
- Bookings that should have had automations fire but didn't
- Booking lifecycle states that are stuck or missing
- Financial sync failures
- Audit Log gaps

**What it monitors:** Pattern-level anomalies across scenarios and data
**Response time:** Within 15 minutes of anomaly condition forming
**Alert channel:** #sss-ops-alerts (SEV-2, SEV-3), DM to Will + Luciana (SEV-1)

### Layer 3: Human Review (Daily and Weekly)

Human review catches things that automated monitoring cannot:

- Alert fatigue patterns (are alerts being ignored?)
- False positive patterns (are alerts misconfigured?)
- Business-logic drift (are automation outputs still correct?)
- AI output quality (are Claude responses still accurate?)

**Who:** Luciana daily, Will weekly
**Where:** #sss-ops-alerts channel review, Airtable Automation_Health table

---

## SECTION 2 — ALERT ROUTING MATRIX

### SEV-1 — Immediate (Financial or operational integrity threat)

**Definition:** Duplicate payout, financial record corruption, Emergency_Flag escalation failure, AI system loop, unauthorized pricing, client data breach suspicion

| Alert | Routing | Format |
|-------|---------|--------|
| Financial field modified post-CONFIRMED | DM to Will + DM to Luciana + #sss-ops-alerts | "🚨 SEV-1 — FINANCIAL INTEGRITY — [Booking ID] — [Field] modified after CONFIRMED — Immediate review required" |
| Emergency_Flag escalation failed | DM to Will directly (phone call backup) + #sss-emergency-ops | "🚨 SEV-1 — EMERGENCY ROUTING FAILURE — [Booking ID] — Manual escalation required NOW" |
| Automation failure after 4 retries | DM to Will + DM to Luciana | "🚨 SEV-1 — AUTOMATION FAILURE — [Scenario] failed 4 times — Manual intervention required" |
| Audit Log gap detected | DM to Will | "🚨 SEV-1 — AUDIT GAP — [Count] autonomous actions found without Audit Log entries — Will review required" |
| Duplicate client message (SMS or email) | DM to Luciana (immediate), DM to Will | "🚨 SEV-1 — DUPLICATE MESSAGE — Client [name] received duplicate [message type] — Personal follow-up required" |

**Response SLA:** Will reviews within 15 minutes during waking hours. Emergency action within 30 minutes.

---

### SEV-2 — Within 30 Minutes (Automation failure or system outage)

| Alert | Routing | Format |
|-------|---------|--------|
| Scenario 3rd failure | #sss-ops-alerts + Luciana DM | "⚠️ SEV-2 — [Scenario] — 3rd failure — Error: [message] — Monitoring" |
| Stripe webhook latency > 5 minutes | #sss-ops-alerts | "⚠️ SEV-2 — Stripe webhook delayed [X] minutes — Manual reconciliation may be needed" |
| Airtable API error rate > 5% | #sss-ops-alerts + Luciana DM | "⚠️ SEV-2 — Airtable API elevated error rate — Make retrying — Monitoring" |
| Charter Brief not generated 10+ days before charter | Luciana DM | "⚠️ SEV-2 — Charter Brief missing — [Booking ID] — [Client] — Charter in [X] days — Create manually" |
| Financial sync failure (COMPLETED booking with no P&L) | #sss-ops-alerts + Luciana DM | "⚠️ SEV-2 — Financial sync failed — [Booking ID] — P&L not synced — Retry or manual entry needed" |
| M-BASIC-LIFECYCLE not run in > 25 hours | Luciana DM | "⚠️ SEV-2 — Lifecycle scheduler gap — Last run: [timestamp] — Check Make schedule" |

**Response SLA:** Luciana investigates within 30 minutes during business hours. Will informed if manual action required.

---

### SEV-3 — Same Business Day (Reporting or dashboard inconsistency)

| Alert | Routing | Format |
|-------|---------|--------|
| City Health Score not updated in > 25 hours | #sss-ops-alerts | "ℹ️ SEV-3 — City health update missed — [City] — Check schedule" |
| Backup age > 48 hours | #sss-ops-alerts + Will DM | "ℹ️ SEV-3 — Backup stale — Last backup: [timestamp] — Review BACKUP-001 scenario" |
| Airtable API error rate between 1-5% | #sss-ops-alerts | "ℹ️ SEV-3 — Airtable API elevated (minor) — Error rate: [%] — Monitoring" |
| AI Lead Score empty on Request > 30 minutes old | Luciana DM | "ℹ️ SEV-3 — Lead scoring delayed — [Request ID] — Score manually if needed" |

**Response SLA:** Investigated same business day.

---

### SEV-4 — Within 72 Hours (Minor inconsistency)

| Alert | Routing | Format |
|-------|---------|--------|
| D30 or D60 send delayed > 24 hours | #sss-ops-alerts | "ℹ️ SEV-4 — Referral/rebooking send delayed — [Booking ID] — Will send next scheduler run" |
| Partner score not updated (weekly run missed) | #sss-ops-alerts | "ℹ️ SEV-4 — Partner scoring missed weekly run — Check schedule" |

**Response SLA:** Scheduled for resolution within 72 hours.

---

## SECTION 3 — M-AUTOMATION-HEALTH CHECKS

The M-AUTOMATION-HEALTH scenario runs every 15 minutes and checks:

### Check 1: Lifecycle Scheduler Freshness
```
Airtable > Audit_Log > Search:
  Triggering_Event contains "M-BASIC-LIFECYCLE"
  Timestamp >= now - 25 hours

If no records found:
  → SEV-2: "M-BASIC-LIFECYCLE has not run in > 25 hours"
  → DM to Luciana
```

### Check 2: Charter Brief Coverage
```
Airtable > Bookings:
  Status = CONFIRMED
  Charter_Date <= today + 10
  Charter_Brief_Sent = false

If any records found:
  → For each: SEV-2 alert
  → DM to Luciana: "Charter Brief missing — [Booking ID] — Charter in [X] days — Create manually or re-trigger"
```

### Check 3: Unsynced P&L Records
```
Airtable > Bookings:
  Status = COMPLETED
  Financial_Sync_Status != SYNCED
  Charter_Date <= today - 1

If any records found:
  → SEV-2: "Financial sync not completed — [Booking IDs]"
  → DM to Luciana
```

### Check 4: Stuck Requests
```
Airtable > Requests:
  Status = NEW
  Created_At <= now - 4 hours
  AI_Lead_Score = blank

If any records found:
  → SEV-3: "Lead scoring not completed — [Request IDs]"
```

### Check 5: Concierge Not Notified
```
Airtable > Bookings:
  Status = DEPOSIT_PAID
  Concierge_Notified_At = blank
  Deposit_Paid_At <= now - 2 hours

If any records found:
  → SEV-2: "Concierge not notified — [Booking IDs] — Charter in [X] days"
  → DM to Luciana
```

### Check 6: Anomaly Aggregation and Circuit Breaker
```
Count all anomalies found this run.

If anomaly_count > 10:
  → Send one consolidated SEV-1 (not 10 individual SEV-2s)
  → Pause M-AUTOMATION-HEALTH for 30 minutes (avoid alert flood)
  → Will DM: "System alert storm — [count] anomalies — Review #sss-ops-alerts"
```

---

## SECTION 4 — SLACK MONITORING CHANNELS

### #sss-ops-alerts

**Purpose:** System health, automation errors, SEV-2 and SEV-3 alerts
**Who reads it:** Luciana daily (checks every morning), Will weekly
**What posts here:** All SEV-2 and SEV-3 alerts, daily health summary
**NOT posted here:** Emergency L4 alerts (those go to #sss-emergency-ops)

**Daily Health Summary (posted every morning by M-AUTOMATION-HEALTH first run of the day):**
```
✅ SYSTEM HEALTH — [Date]
  M-BASIC-LIFECYCLE: Last run [X] hours ago — [OK / ALERT]
  M-AUTOMATION-HEALTH: Active — last anomaly [X] hours ago
  Stripe webhooks: [OK / DELAYED]
  Open anomalies: [count]
  Charter Briefs due (next 10 days): [count] generated / [count] pending
  Today's charters: [count]
  Last backup: [timestamp]
```

### #sss-emergency-ops

**Purpose:** L4 emergency coordination only
**Who reads it:** Will + Luciana always
**What posts here:** Emergency_Flag activations, L4 escalation alerts, cybersecurity incidents
**Rule:** No operational chatter in this channel. Emergency and L3/L4 only.

### Will's Slack DM

**What gets sent here:** SEV-1 alerts, Thursday Digest, Emergency escalations, Founder Decision items requiring immediate attention, any 4th-failure automation alert

### Luciana's Slack DM

**What gets sent here:** SEV-2 alerts, HV client routing, charter brief issues, concierge assignment, new booking events requiring her attention

---

## SECTION 5 — AIRTABLE MONITORING VIEWS

The following views should exist in the production Airtable base for human monitoring:

| View Name | Table | Filter | Purpose |
|-----------|-------|--------|---------|
| MONITORING — Open Anomalies | Automation_Health | Resolved = false | All unresolved anomalies |
| MONITORING — Recent Alerts | Automation_Health | Created_At >= today - 7 | Last 7 days of health events |
| MONITORING — Failed Syncs | Bookings | Financial_Sync_Status = FAILED | P&L sync failures |
| MONITORING — Missing Briefs | Bookings | Status = CONFIRMED AND Charter_Brief_Sent = false AND Charter_Date <= today + 14 | Charter brief coverage |
| MONITORING — Failed Payments | Bookings | Payment_Failure_Count >= 1 | Active payment issues |
| MONITORING — Audit Log Gap Check | Audit_Log | Environment = Production AND Timestamp >= today - 1 | Recent audit activity |

---

## SECTION 6 — METRIC THRESHOLDS AND CALIBRATION

These thresholds should be reviewed monthly and adjusted based on observed false positive/negative rates:

| Metric | Current Threshold | Adjust When |
|--------|------------------|------------|
| Lifecycle scheduler gap | > 25 hours | If daily run timing is moved, adjust accordingly |
| Charter brief warning window | 10 days before charter | Adjust based on how long Luciana needs to review |
| Financial sync timeout | 24 hours after COMPLETED | Can reduce to 12 hours as team becomes faster |
| M-AUTOMATION-HEALTH run frequency | Every 15 minutes | Can increase to every 5 minutes if volume grows |
| SEV-2 automation failure threshold | 3 failures in 60 minutes | Adjust if noise level is too high |
| AI lead scoring delay alert | 30 minutes | Adjust based on Claude API response time patterns |

---

## SECTION 7 — MONITORING ESCALATION CONTACTS

All contact information stored in credential vault. Summary:

| Role | Contact | Used For |
|------|---------|---------|
| Will (primary) | Will's Slack DM | SEV-1, SEV-2 requiring founder decision |
| Will (emergency) | Will's mobile | L4 emergency if Slack unreachable |
| Luciana (primary) | Luciana's Slack DM | SEV-2, operational alerts |
| Luciana (backup) | Luciana's email | If Slack unreachable |
| Make Support | Make support channel | Make platform outages |
| Airtable Support | Airtable enterprise support | Airtable API outages |
| Stripe Support | Stripe dashboard support | Stripe webhook or payment issues |
| Anthropic Status | status.anthropic.com | Claude API outages |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_MONITORING_AND_ALERTS v1.0*
*Effective May 2026*
