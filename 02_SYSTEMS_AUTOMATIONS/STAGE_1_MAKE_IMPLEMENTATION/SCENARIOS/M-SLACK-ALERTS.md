# M-SLACK-ALERTS — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Lead Intake (called by M-LEAD-INTAKE)  
**Execution Order:** Module 10 in M-LEAD-INTAKE triggers this scenario

---

## 1. Scenario Name

`M-SLACK-ALERTS`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here. The generated webhook URL must be registered as the target of Module 10 in M-LEAD-INTAKE before M-LEAD-INTAKE can be built.

**Priority:** Build and register M-SLACK-ALERTS BEFORE building M-LEAD-INTAKE Module 10.

---

## 3. Trigger Type

**Pattern:** Custom Webhook (Make-generated URL), called by M-LEAD-INTAKE  
**Make Module Type:** Webhooks > Custom Webhook  
**Method:** POST  
**Content-Type:** application/json  
**Authentication:** Bearer Token (shared inter-scenario token, distinct from the public-facing webhook token in M-LEAD-INTAKE)

**Caller:** M-LEAD-INTAKE (Module 10)  
**Also called by (future):** M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION

**Inbound Payload from Calling Scenario:**
```json
{
  "request_id": "recXXXXXXXXXXXXXX",
  "request_id_display": "REQ-20260516-abc123",
  "alert_type": "new_lead",
  "triggered_by": "M-LEAD-INTAKE",
  "execution_id": "abc123def456",
  "brand_classification": "SSS",
  "requires_human_review": false
}
```

**Supported `alert_type` values:**

| alert_type | Trigger Scenario | Description |
|------------|-----------------|-------------|
| `new_lead` | M-LEAD-INTAKE | New inbound lead received and recorded |
| `assignment` | M-CONCIERGE-ASSIGNMENT | Concierge assigned to a lead |
| `deposit_sent` | M-STRIPE-DEPOSIT | Stripe deposit link sent to client |
| `booking_created` | M-BOOKING-CREATION | Booking record created |
| `booking_confirmed` | M-BOOKING-CONFIRMATION | Booking confirmed by client |
| `error` | Any scenario | Error alert requiring human attention |
| `ambiguous_brand` | M-LEAD-INTAKE | Brand classification requires human review |
| `hot_lead` | Manual or future scenario | Lead flagged as high priority |

> Stage 1 implementation covers: `new_lead` and `error`. Other alert_types are defined here for forward compatibility; their Slack templates are stubbed and marked PENDING.

---

## 4. Exact Module Sequence

### Module 1 — [Webhook] Receive Request ID and Alert Type

**Make Module Type:** Webhooks > Custom Webhook  
**Position:** Module 1 (scenario trigger)  
**Purpose:** Receive the trigger payload from M-LEAD-INTAKE (or other calling scenario).

**Payload fields registered in Make webhook data structure:**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `request_id` | Text | Yes | Airtable Record ID of the Request |
| `request_id_display` | Text | No | Human-readable ID (REQ-YYYYMMDD-suffix) |
| `alert_type` | Text | Yes | One of the supported alert_type values |
| `triggered_by` | Text | Yes | Name of calling scenario |
| `execution_id` | Text | No | Make Execution ID from calling scenario |
| `brand_classification` | Text | No | SSS \| ME \| AMBIGUOUS (from calling scenario cache) |
| `requires_human_review` | Boolean | No | Whether brand needs Luciana review |

**Webhook response:** Immediate 200 OK (processing continues asynchronously).

---

### Module 2 — [HTTP / Tools] Bearer Token Validation

**Make Module Type:** Filter  
**Position:** Module 2  
**Purpose:** Validate inter-scenario bearer token. Prevents external actors from triggering Slack alerts by posting directly to this webhook URL.

**Filter:**
- Label: `Inter-scenario token valid`
- Condition: `{{1.api_key}}` equals `[INTER_SCENARIO_TOKEN]`
- If failed: log to Audit Log (`Event_Type = UNAUTHORIZED_TRIGGER`), halt

> Inter-scenario token is separate from the public webhook token used by M-LEAD-INTAKE. Store in Make Keys under name `INTER_SCENARIO_TOKEN`.

---

### Module 3 — [Airtable] Fetch Request Record

**Make Module Type:** Airtable > Get Record  
**Position:** Module 3  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblTlSB9CO4dTGodg` (Requests)  
**Purpose:** Retrieve all fields needed to build the Slack message from the authoritative Airtable record.

**Configuration:**
- Record ID: `{{1.request_id}}`

**Fields retrieved and used in Slack message construction:**

| Airtable Field | Make Variable | Used In |
|----------------|---------------|---------|
| `First_Name` | `{{3.First_Name}}` | Client name display |
| `Last_Name` | `{{3.Last_Name}}` | Client name display |
| `Email` | `{{3.Email}}` | Contact info |
| `Phone` | `{{3.Phone}}` | Contact info |
| `City` | `{{3.City}}` | Location |
| `Charter_Date` | `{{3.Charter_Date}}` | Event details |
| `Group_Size` | `{{3.Group_Size}}` | Event details |
| `Occasion` | `{{3.Occasion}}` | Event details |
| `Package_Interest` | `{{3.Package_Interest}}` | Sales context |
| `Budget` | `{{3.Budget}}` | Sales context |
| `Brand` | `{{3.Brand}}` | Brand routing |
| `Brand_Confidence` | `{{3.Brand_Confidence}}` | Quality indicator |
| `Source` | `{{3.Source}}` | Lead source |
| `UTM_Campaign` | `{{3.UTM_Campaign}}` | Marketing attribution |
| `Submitted_At` | `{{3.Submitted_At}}` | Timing |
| `Requires_Human_Brand_Review` | `{{3.Requires_Human_Brand_Review}}` | Review flag |
| `Request_ID_Display` | `{{3.Request_ID_Display}}` | Human-readable ID |
| `Status` | `{{3.Status}}` | Current status |

**Error Handler on Module 3:**
- If record not found (404): Log to Audit Log, halt with error status
- If Airtable API error: Retry 2x at 10-second intervals; after exhaustion, post fallback Slack alert using data from calling payload only

**Fallback Slack alert (if Airtable fetch fails):**
```
:warning: *M-SLACK-ALERTS: Could not fetch Request record* 
Request ID: {{1.request_id}} | Alert Type: {{1.alert_type}} | Called by: {{1.triggered_by}}
Airtable fetch failed. Manual review required.
```

---

### Module 4 — [Router] Route by alert_type

**Make Module Type:** Router  
**Position:** Module 4  
**Purpose:** Direct the scenario flow to the correct Slack message template based on the `alert_type` value.

**Routes:**

| Route | Condition | Filter Expression | Destination |
|-------|-----------|-------------------|-------------|
| Route A: New Lead | alert_type = new_lead | `{{1.alert_type}} = "new_lead"` | Module 5A |
| Route B: Error | alert_type = error | `{{1.alert_type}} = "error"` | Module 5B |
| Route C: Assignment | alert_type = assignment | `{{1.alert_type}} = "assignment"` | Module 5C (STUB) |
| Route D: Deposit Sent | alert_type = deposit_sent | `{{1.alert_type}} = "deposit_sent"` | Module 5D (STUB) |
| Route E: Booking Created | alert_type = booking_created | `{{1.alert_type}} = "booking_created"` | Module 5E (STUB) |
| Route F: Booking Confirmed | alert_type = booking_confirmed | `{{1.alert_type}} = "booking_confirmed"` | Module 5F (STUB) |
| Route G: Fallback | All others | No filter (fallback) | Module 5G |

---

### Module 5A — [Slack] Post New Lead Alert to #sss-ops-alerts

**Make Module Type:** Slack > Create a Message  
**Position:** Module 5A (on Route A)  
**Channel:** `#sss-ops-alerts`  
**Purpose:** Post a fully formatted Block Kit message announcing the new inbound lead.

**Slack Connection:** Use the authenticated Slack app connection for She Said Sail workspace.

**Message Configuration:**
- Post as: `She Said Sail Ops Bot`
- Icon: `:sailboat:` (SSS) or `:briefcase:` (ME) — set dynamically per brand
- Channel: `#sss-ops-alerts`
- Message format: Block Kit (JSON blocks)

**Full Slack Block Kit JSON — New Lead Alert:**

```json
{
  "text": "New Lead: {{3.First_Name}} {{3.Last_Name}} — {{3.Brand}}",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "{{if(3.Brand = 'SSS', ':sailboat:', ':briefcase:')}} New Lead — {{3.Brand}} | {{3.Request_ID_Display}}",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Client:*\n{{3.First_Name}} {{3.Last_Name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Brand:*\n{{3.Brand}} ({{3.Brand_Confidence}} confidence)"
        },
        {
          "type": "mrkdwn",
          "text": "*Email:*\n{{3.Email}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Phone:*\n{{if(3.Phone, 3.Phone, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*City:*\n{{if(3.City, 3.City, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Source:*\n{{3.Source}}"
        }
      ]
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Charter Date:*\n{{if(3.Charter_Date, formatDate(3.Charter_Date, 'MMM D, YYYY'), '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Group Size:*\n{{if(3.Group_Size, 3.Group_Size, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Occasion:*\n{{if(3.Occasion, 3.Occasion, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Package Interest:*\n{{if(3.Package_Interest, 3.Package_Interest, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Budget:*\n{{if(3.Budget, 3.Budget, '_not provided_')}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Submitted:*\n{{formatDate(3.Submitted_At, 'MMM D, YYYY [at] h:mm A z')}}"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Message:*\n{{if(3.Message, '\"' + 3.Message + '\"', '_No message provided_')}}"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View in Airtable",
            "emoji": true
          },
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/{{1.request_id}}",
          "action_id": "view_airtable_record",
          "style": "primary"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Assign Concierge",
            "emoji": true
          },
          "value": "assign_concierge_{{1.request_id}}",
          "action_id": "assign_concierge"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": ":fire: Mark Hot Lead",
            "emoji": true
          },
          "value": "hot_lead_{{1.request_id}}",
          "action_id": "mark_hot_lead",
          "style": "danger"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Request ID: `{{1.request_id}}` | Campaign: {{if(3.UTM_Campaign, 3.UTM_Campaign, 'direct')}} | Intake Execution: `{{1.execution_id}}`"
        }
      ]
    }
  ]
}
```

**Conditional block — AMBIGUOUS brand (appended when `requires_human_review = true`):**

This block is appended to the `blocks` array when `{{3.Requires_Human_Brand_Review}} = true`:

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": ":warning: *Brand Classification Ambiguous* — No clear SSS or ME signals detected. Defaulted to SSS. *Luciana: please classify this lead manually.*"
  }
},
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Classify as SSS",
        "emoji": true
      },
      "value": "classify_sss_{{1.request_id}}",
      "action_id": "brand_classify_sss"
    },
    {
      "type": "button",
      "text": {
        "type": "plain_text",
        "text": "Classify as ME",
        "emoji": true
      },
      "value": "classify_me_{{1.request_id}}",
      "action_id": "brand_classify_me"
    }
  ]
}
```

**Implementation note on Slack action buttons:**
The `Assign Concierge`, `Mark Hot Lead`, `Classify as SSS`, and `Classify as ME` buttons use Slack's interactive components (Block Kit action buttons). These buttons send a payload to a Slack app's Interactivity URL. A separate Make scenario (not in Stage 1 scope) must be registered as the Slack app's interactivity endpoint to handle button clicks. Until that scenario is built, buttons will display but generate a "This app is not responding" error when clicked. This is acceptable for Stage 1 — buttons are forward-compatible and provide the Airtable link as an immediate action.

**Conditional bot icon and username:**

| Brand | Bot Username | Bot Icon |
|-------|-------------|---------|
| SSS | `She Said Sail Ops` | `:sailboat:` |
| ME | `Mare Executive Ops` | `:briefcase:` |
| AMBIGUOUS | `She Said Sail Ops` | `:question:` |

In Make's Slack module, set:
- Bot name: `{{if(3.Brand = "ME", "Mare Executive Ops", "She Said Sail Ops")}}`
- Bot icon: `{{if(3.Brand = "ME", ":briefcase:", if(3.Brand = "AMBIGUOUS", ":question:", ":sailboat:"))}}`

---

### Module 5B — [Slack] Post Error Alert to #sss-ops-alerts

**Make Module Type:** Slack > Create a Message  
**Position:** Module 5B (on Route B)  
**Channel:** `#sss-ops-alerts`  
**Purpose:** Post a structured error alert when a downstream scenario encounters a failure.

**Error Alert Slack Block Kit JSON:**

```json
{
  "text": ":red_circle: AUTOMATION ERROR — {{1.triggered_by}}",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":red_circle: Automation Error — Action Required",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Scenario:*\n{{1.triggered_by}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Execution ID:*\n`{{1.execution_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Request ID:*\n`{{1.request_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Time:*\n{{formatDate(now, 'MMM D, YYYY [at] h:mm A z')}}"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Error Details:*\n{{if(1.error_message, 1.error_message, 'No error details provided.')}}"
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "View in Airtable",
            "emoji": true
          },
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/{{1.request_id}}",
          "action_id": "view_error_record",
          "style": "danger"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Audit log entry created. Luciana and Will have been notified via DM."
        }
      ]
    }
  ]
}
```

**For Level 3-4 errors:** Also send a Slack DM to Luciana and Will directly.

**Slack DM — Luciana:**
```json
{
  "channel": "@luciana",
  "text": ":red_circle: *Automation Error — Immediate Attention Required*\nScenario: {{1.triggered_by}}\nRequest ID: {{1.request_id}}\nExecution ID: {{1.execution_id}}\nDetails: {{1.error_message}}\n\nPlease check #sss-ops-alerts for full details."
}
```

---

### Module 5C through 5F — [STUB] Future Alert Types

**Status:** PENDING BUILD — Stage 2+ implementation  
**Modules:** 5C (assignment), 5D (deposit_sent), 5E (booking_created), 5F (booking_confirmed)

Each stub module is a Slack > Create a Message with a minimal placeholder message:

```json
{
  "text": "[STUB] Alert type '{{1.alert_type}}' received for {{1.request_id_display}}. Template pending implementation.",
  "channel": "#sss-ops-alerts"
}
```

---

### Module 5G — [Slack] Fallback Unknown Alert Type

**Make Module Type:** Slack > Create a Message  
**Position:** Module 5G (fallback route)  
**Purpose:** Handle any unrecognized `alert_type` values without silent failure.

```json
{
  "text": ":grey_question: Unknown alert type '{{1.alert_type}}' received from {{1.triggered_by}} for Request {{1.request_id_display}}. No template found.",
  "channel": "#sss-ops-alerts"
}
```

---

### Module 6 — [Airtable] Write Audit Log Entry

**Make Module Type:** Airtable > Create Record  
**Position:** Module 6 (runs after all routes converge)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblrMpTfMk8q1eNHp` (Audit Log)  
**Purpose:** Record the Slack alert event in the Audit Log.

**Audit Log Field Mapping:**

| Audit Log Field | Value |
|-----------------|-------|
| `Event_Type` | `SLACK_ALERT_SENT` |
| `Scenario_Name` | `M-SLACK-ALERTS` |
| `Execution_ID` | `{{executionId}}` |
| `Request_ID` | `{{1.request_id}}` |
| `Request_ID_Display` | `{{1.request_id_display}}` |
| `Alert_Type` | `{{1.alert_type}}` |
| `Triggered_By` | `{{1.triggered_by}}` |
| `Caller_Execution_ID` | `{{1.execution_id}}` |
| `Channel` | `#sss-ops-alerts` |
| `Brand` | `{{3.Brand}}` |
| `Timestamp` | `{{now}}` |
| `Status` | `SUCCESS` |
| `Notes` | `Slack {{1.alert_type}} alert posted for {{1.request_id_display}}` |

**On Audit Log failure:** Log to Make execution log (internal) and continue. Audit Log failure is non-fatal to the alert flow.

---

### Module 7 — [Airtable] Update Request Record — Last Alert Timestamp

**Make Module Type:** Airtable > Update Record  
**Position:** Module 7  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Table ID:** `tblTlSB9CO4dTGodg` (Requests)  
**Purpose:** Stamp the Request record with the timestamp of the last Slack alert sent, for operational tracking.

**Update:**
- Record ID: `{{1.request_id}}`
- Field: `Last_Slack_Alert_At` → `{{now}}`
- Field: `Last_Slack_Alert_Type` → `{{1.alert_type}}`

---

### Module 8 — [Airtable] Write Automation Health Entry

**Make Module Type:** Airtable > Update Record  
**Position:** Module 8 (final module)  
**Purpose:** Update health dashboard for M-SLACK-ALERTS.

| Field | Value |
|-------|-------|
| `Scenario` | `M-SLACK-ALERTS` |
| `Last_Run_At` | `{{now}}` |
| `Last_Run_Status` | `SUCCESS` |
| `Last_Execution_ID` | `{{executionId}}` |

---

## 5. Router Logic — Complete Decision Tree

```
WEBHOOK RECEIVED (from M-LEAD-INTAKE or other scenario)
│
├── Inter-scenario token invalid → REJECT (log, halt)
│
├── Fetch Airtable Request record by request_id
│   └── Record not found → fallback alert (data from calling payload), log, halt
│
├── Route by alert_type
│   ├── "new_lead" →
│   │   ├── Build Block Kit new lead message
│   │   ├── Append AMBIGUOUS block if requires_human_review = true
│   │   ├── Set bot name/icon per brand
│   │   └── Post to #sss-ops-alerts
│   │
│   ├── "error" →
│   │   ├── Post error alert to #sss-ops-alerts
│   │   └── Send DM to Luciana + Will
│   │
│   ├── "assignment" | "deposit_sent" | "booking_created" | "booking_confirmed" →
│   │   └── Post STUB message to #sss-ops-alerts (Stage 2+)
│   │
│   └── Unknown → Post fallback unknown-type message
│
├── Write Audit Log entry
├── Update Request record (last alert timestamp)
└── Update Health record → COMPLETE
```

---

## 6. Airtable Field Mapping

Fields written by M-SLACK-ALERTS:

**Requests table (`tblTlSB9CO4dTGodg`) — updates:**

| Field | Value | Module |
|-------|-------|--------|
| `Last_Slack_Alert_At` | `{{now}}` | Module 7 |
| `Last_Slack_Alert_Type` | `{{1.alert_type}}` | Module 7 |

**Audit Log table (`tblrMpTfMk8q1eNHp`) — creates:**

| Field | Value | Module |
|-------|-------|--------|
| `Event_Type` | `SLACK_ALERT_SENT` | Module 6 |
| `Scenario_Name` | `M-SLACK-ALERTS` | Module 6 |
| `Execution_ID` | `{{executionId}}` | Module 6 |
| `Request_ID` | `{{1.request_id}}` | Module 6 |
| `Alert_Type` | `{{1.alert_type}}` | Module 6 |
| `Status` | `SUCCESS` | Module 6 |
| `Timestamp` | `{{now}}` | Module 6 |

---

## 7. Webhook Structure

**Endpoint:** Custom Make webhook (generated URL)  
**Method:** POST  
**Headers:**
```
Content-Type: application/json
Authorization: Bearer [INTER_SCENARIO_TOKEN]
```

**Caller authentication:** The `api_key` field in the payload contains the inter-scenario token. Module 2 validates this before any processing.

**Airtable record link format in Slack:**
```
https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/{{request_id}}
```

> Note: Airtable record deep-links use the Record ID directly. Confirm this URL pattern resolves correctly in the production Airtable base. If Airtable generates a different URL structure for this base, update the `url` field in all Block Kit action button elements.

---

## 8. Error Handling Logic

4-level error handling framework:

| Level | Trigger | Module | Action |
|-------|---------|--------|--------|
| Level 1 — Field Error | Missing field in Airtable record (e.g., First_Name is null) | 3, 5A | Use `if(field, field, "_not provided_")` fallback — all optional fields have nullsafe wrappers in Block Kit JSON |
| Level 2 — Airtable Fetch Failure | Airtable API returns error or record not found | 3 | Retry 2x; if exhausted, post fallback Slack alert using calling payload data only |
| Level 3 — Slack API Failure | Slack returns error (rate limit, channel not found, auth error) | 5A, 5B | Retry 3x at 30-second intervals (Slack rate limit buffer); if exhausted, write to Audit Log, send Make execution alert, DM Luciana via alternative channel |
| Level 4 — Scenario Crash | Unhandled exception | Any | Make Error Handler: write to Audit Log, halt |

**Slack failure escalation procedure:**
1. Attempt original Slack post to #sss-ops-alerts (3 retries, 30-second intervals)
2. If #sss-ops-alerts post fails: attempt DM to Luciana directly
3. If DM also fails: write detailed failure record to Audit Log with `Status = SLACK_DOWN`
4. Write health record with `Status = DEGRADED`
5. Accept that the alert was not delivered — M-LEAD-INTAKE (caller) has already completed successfully

**Critical design principle:** M-SLACK-ALERTS failure must NEVER block the core intake pipeline. The Airtable record exists regardless of whether the Slack alert was delivered. Luciana can always check Airtable directly.

---

## 9. Retry Logic

| Module | Failure Type | Retries | Interval | After Exhaustion |
|--------|-------------|---------|----------|-----------------|
| Module 3 — Airtable Fetch | API timeout / 5xx | 2 | 10 seconds | Fallback alert with partial data |
| Module 5A — Slack New Lead Post | Slack API error / rate limit | 3 | 30 seconds | Log failure, continue to Module 6 |
| Module 5B — Slack Error Post | Slack API error | 3 | 30 seconds | Log failure to Audit Log |
| Module 6 — Audit Log Write | Airtable API error | 2 | 15 seconds | Log to Make execution log, continue |
| Module 7 — Request Record Update | Airtable API error | 2 | 10 seconds | Non-fatal, skip |

**Global Make retry setting:** Scenario Settings > Error handling > 3 attempts, 10-second interval (overridden per module by the values above).

---

## 10. Duplicate Prevention

M-SLACK-ALERTS can be called multiple times for the same `request_id` with different `alert_type` values, and this is correct behavior (e.g., new_lead alert, then assignment alert, then deposit_sent alert). Therefore, deduplication is by `request_id + alert_type` pair, not by `request_id` alone.

**Duplicate detection:**
- Before posting: check Audit Log for existing `SLACK_ALERT_SENT` record where `Request_ID = {{1.request_id}}` AND `Alert_Type = {{1.alert_type}}`
- If found: skip the Slack post, write a `SLACK_ALERT_DUPLICATE_SKIPPED` Audit Log entry, halt

**Implementation:** Add a Module 2.5 (Airtable Search in Audit Log) between the token check (Module 2) and the Airtable fetch (Module 3):

```
Module 2.5 — Airtable > Search Records (Audit Log)
Filter: AND({Request_ID} = "{{1.request_id}}", {Alert_Type} = "{{1.alert_type}}", {Event_Type} = "SLACK_ALERT_SENT")
If total_records > 0: skip, log DUPLICATE_SKIPPED, halt
```

> Exception: `error` alert_type is never deduplicated — each error event should generate its own alert regardless of prior errors for the same request.

---

## 11. Slack Alert Structure

**Full "new_lead" Block Kit message — complete JSON with all variables resolved (example):**

```json
{
  "channel": "#sss-ops-alerts",
  "username": "She Said Sail Ops",
  "icon_emoji": ":sailboat:",
  "text": "New Lead: Sarah Johnson — SSS | REQ-20260516-abc123",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": ":sailboat: New Lead — SSS | REQ-20260516-abc123",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Client:*\nSarah Johnson" },
        { "type": "mrkdwn", "text": "*Brand:*\nSSS (HIGH confidence)" },
        { "type": "mrkdwn", "text": "*Email:*\nsarah@example.com" },
        { "type": "mrkdwn", "text": "*Phone:*\n+13055551234" },
        { "type": "mrkdwn", "text": "*City:*\nMiami" },
        { "type": "mrkdwn", "text": "*Source:*\nwebsite_form" }
      ]
    },
    {
      "type": "section",
      "fields": [
        { "type": "mrkdwn", "text": "*Charter Date:*\nJun 15, 2026" },
        { "type": "mrkdwn", "text": "*Group Size:*\n8" },
        { "type": "mrkdwn", "text": "*Occasion:*\nBachelorette" },
        { "type": "mrkdwn", "text": "*Package Interest:*\nSunset Sail" },
        { "type": "mrkdwn", "text": "*Budget:*\n$500-$1000" },
        { "type": "mrkdwn", "text": "*Submitted:*\nMay 16, 2026 at 2:30 PM EST" }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Message:*\n\"Looking for a bachelorette party cruise for 8 people\""
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "View in Airtable", "emoji": true },
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/recXXXXXXXXXXXXXX",
          "action_id": "view_airtable_record",
          "style": "primary"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Assign Concierge", "emoji": true },
          "value": "assign_concierge_recXXXXXXXXXXXXXX",
          "action_id": "assign_concierge"
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": ":fire: Mark Hot Lead", "emoji": true },
          "value": "hot_lead_recXXXXXXXXXXXXXX",
          "action_id": "mark_hot_lead",
          "style": "danger"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Request ID: `recXXXXXXXXXXXXXX` | Campaign: spring_2026 | Intake Execution: `abc123def456`"
        }
      ]
    }
  ]
}
```

**Variable mapping — Slack message to Airtable fields:**

| Slack Display | Airtable Source | Make Expression |
|---------------|----------------|-----------------|
| Client name | First_Name + Last_Name | `{{3.First_Name}} {{3.Last_Name}}` |
| Brand label | Brand | `{{3.Brand}}` |
| Brand confidence | Brand_Confidence | `{{3.Brand_Confidence}}` |
| Email | Email | `{{3.Email}}` |
| Phone | Phone | `{{if(3.Phone, 3.Phone, "_not provided_")}}` |
| City | City | `{{if(3.City, 3.City, "_not provided_")}}` |
| Source | Source | `{{3.Source}}` |
| Charter Date | Charter_Date | `{{formatDate(3.Charter_Date, "MMM D, YYYY")}}` |
| Group Size | Group_Size | `{{if(3.Group_Size, 3.Group_Size, "_not provided_")}}` |
| Occasion | Occasion | `{{if(3.Occasion, 3.Occasion, "_not provided_")}}` |
| Package Interest | Package_Interest | `{{if(3.Package_Interest, 3.Package_Interest, "_not provided_")}}` |
| Budget | Budget | `{{if(3.Budget, 3.Budget, "_not provided_")}}` |
| Message | Message | `{{if(3.Message, "\"" + 3.Message + "\"", "_No message provided_")}}` |
| Submitted | Submitted_At | `{{formatDate(3.Submitted_At, "MMM D, YYYY [at] h:mm A z")}}` |
| Airtable link | Record ID | `https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/{{1.request_id}}` |
| Campaign | UTM_Campaign | `{{if(3.UTM_Campaign, 3.UTM_Campaign, "direct")}}` |
| Request ID display | Request_ID_Display | `{{1.request_id_display}}` |

---

## 12. Audit Log Writes

**Table:** `tblrMpTfMk8q1eNHp`

Events written by M-SLACK-ALERTS:

| Trigger | Event_Type | Status |
|---------|-----------|--------|
| Unauthorized trigger | `UNAUTHORIZED_TRIGGER` | `REJECTED` |
| Airtable record not found | `SLACK_ALERT_FAILED_NO_RECORD` | `ERROR` |
| Duplicate alert skipped | `SLACK_ALERT_DUPLICATE_SKIPPED` | `SKIPPED` |
| Slack alert posted successfully | `SLACK_ALERT_SENT` | `SUCCESS` |
| Slack post failed after retries | `SLACK_ALERT_FAILED` | `ERROR` |

---

## 13. Automation Health Writes

**On success:**

| Field | Value |
|-------|-------|
| `Scenario` | `M-SLACK-ALERTS` |
| `Last_Run_At` | `{{now}}` |
| `Last_Run_Status` | `SUCCESS` |
| `Last_Execution_ID` | `{{executionId}}` |
| `Alerts_Sent_Today` | Incremented by 1 |

**On Slack failure (degraded mode):**

| Field | Value |
|-------|-------|
| `Last_Failure_At` | `{{now}}` |
| `Last_Run_Status` | `DEGRADED` |
| `Consecutive_Failures` | Incremented |

---

## 14. Rollback Procedure

M-SLACK-ALERTS does not create Request records — it only reads them. Rollback scenarios:

**Scenario A — Slack alert sent for voided Request record:**
1. Luciana identifies the alert in #sss-ops-alerts.
2. Post a correction message in #sss-ops-alerts: `":x: Correction — the lead alert posted above for [Request_ID_Display] has been voided. Record was a test/duplicate. Please disregard."`.
3. In Airtable: void the Request record per M-LEAD-INTAKE rollback procedure.
4. Write Audit Log: `Event_Type = SLACK_ALERT_RETRACTED`, `Notes = reason`.

**Scenario B — Slack alert not sent (Slack was down):**
1. Identify the missed alert from Audit Log (`Event_Type = SLACK_ALERT_FAILED`).
2. In Make.com: navigate to the failed execution in M-SLACK-ALERTS execution history.
3. Click "Re-run this execution" on the failed execution (or manually trigger M-SLACK-ALERTS via webhook with the original `request_id` and `alert_type`).
4. Verify alert appears in #sss-ops-alerts.
5. Write Audit Log: `Event_Type = SLACK_ALERT_RESENT`, `Notes = "Manual re-send after Slack outage"`.

**Scenario C — Wrong alert content (bad field data):**
1. Correct the Airtable Request record fields that were wrong.
2. Manually re-trigger M-SLACK-ALERTS (POST to webhook URL with `request_id` and `alert_type = new_lead`).
3. New alert posts with correct data.
4. Post correction notice in #sss-ops-alerts referencing the original alert.

---

## 15. Sandbox Test Procedure

**Prerequisites:**
- Make.com scenario in INACTIVE state (Run Once mode for testing)
- Airtable test records pre-created or use records from M-LEAD-INTAKE sandbox tests
- Slack channel #sss-ops-alerts accessible (test messages will appear; prefix with `[TEST]`)
- Postman or equivalent tool to send test payloads

**Test Cases:**

### Test 1 — New Lead Alert (SSS, complete data)
**Trigger payload:**
```json
{
  "api_key": "[INTER_SCENARIO_TOKEN]",
  "request_id": "[AIRTABLE_RECORD_ID_FROM_TEST]",
  "request_id_display": "REQ-20260516-test1",
  "alert_type": "new_lead",
  "triggered_by": "M-LEAD-INTAKE",
  "execution_id": "test-execution-001",
  "brand_classification": "SSS",
  "requires_human_review": false
}
```
**Expected:** Full Block Kit message in #sss-ops-alerts with all fields populated. Bot name = "She Said Sail Ops", icon = :sailboat:. No AMBIGUOUS block. Audit Log entry created.

### Test 2 — New Lead Alert (ME brand)
**Trigger payload:** Same as Test 1 but use a Request record with `Brand = ME`  
**Expected:** Bot name = "Mare Executive Ops", icon = :briefcase:. ME brand displayed in message.

### Test 3 — New Lead Alert (AMBIGUOUS, requires human review)
**Trigger payload:** Same as Test 1, `requires_human_review: true`, use record with `Brand = AMBIGUOUS`  
**Expected:** Alert includes AMBIGUOUS warning block with "Classify as SSS" and "Classify as ME" buttons.

### Test 4 — New Lead Alert (partial data — missing phone, city, message)
**Trigger payload:** Test 1 using a Request record where phone, city, and message are null  
**Expected:** `_not provided_` displayed for missing fields. No null reference errors. Alert posts successfully.

### Test 5 — Error Alert
**Trigger payload:**
```json
{
  "api_key": "[INTER_SCENARIO_TOKEN]",
  "request_id": "[AIRTABLE_RECORD_ID]",
  "request_id_display": "REQ-20260516-test5",
  "alert_type": "error",
  "triggered_by": "M-STRIPE-DEPOSIT",
  "execution_id": "test-execution-005",
  "error_message": "Stripe API timeout after 3 retries. Deposit link not sent."
}
```
**Expected:** Error alert in #sss-ops-alerts. DM sent to Luciana and Will.

### Test 6 — Invalid Auth Token
**Trigger payload:** Test 1 with `api_key = "WRONG_TOKEN"`  
**Expected:** `UNAUTHORIZED_TRIGGER` in Audit Log. No Slack alert posted.

### Test 7 — Invalid Request ID (record not found)
**Trigger payload:** Test 1 with `request_id = "recINVALID000000"`  
**Expected:** Fallback Slack alert posted with partial data. `SLACK_ALERT_FAILED_NO_RECORD` in Audit Log.

### Test 8 — Duplicate Alert Detection
**Steps:** Send Test 1 payload twice with the same `request_id` and `alert_type = new_lead`  
**Expected:** First call posts alert. Second call skips post, writes `SLACK_ALERT_DUPLICATE_SKIPPED` to Audit Log.

**Execution Steps:**
1. Ensure at least one Airtable Request record exists in `tblTlSB9CO4dTGodg` (create via M-LEAD-INTAKE sandbox test or manually).
2. Note the Airtable Record ID of the test record.
3. Activate M-SLACK-ALERTS in Run Once mode.
4. Send each test payload via Postman to the webhook URL.
5. After each test: verify Slack message content in #sss-ops-alerts.
6. Verify Audit Log entry created with correct `Event_Type` and `Status`.
7. Verify Request record updated with `Last_Slack_Alert_At` and `Last_Slack_Alert_Type`.
8. Log pass/fail for all 8 tests.
9. Deactivate scenario.

---

## 16. Production Validation Checklist

**Go/No-Go Criteria — ALL must pass:**

- [ ] All 8 sandbox test cases pass
- [ ] SSS new lead alert displays all 16 fields correctly in Slack
- [ ] ME new lead alert correctly changes bot name and icon
- [ ] AMBIGUOUS lead alert includes the classify-brand action buttons
- [ ] Missing/null fields display as `_not provided_` without errors
- [ ] Airtable link in "View in Airtable" button opens correct record in browser
- [ ] Error alert posts to #sss-ops-alerts AND sends DMs to Luciana and Will
- [ ] Invalid auth token correctly rejected (no alert posted, Audit Log entry written)
- [ ] Invalid Record ID triggers fallback alert (not a silent failure)
- [ ] Duplicate alert detection prevents double-posting for same request_id + alert_type
- [ ] Slack failure is non-blocking (scenario completes, failure logged, health record updated)
- [ ] Audit Log entry created for every execution (all 8 event types verified)
- [ ] Request record updated with last alert timestamp after each successful post
- [ ] Slack app connection authenticated and using correct workspace
- [ ] Webhook URL recorded and shared with M-LEAD-INTAKE for Module 10 configuration
- [ ] Inter-scenario token stored in Make Keys (not hardcoded)
- [ ] Luciana has reviewed and approved the Slack alert format for new_lead
- [ ] Luciana has reviewed and approved the AMBIGUOUS classification alert block
- [ ] Will has reviewed and approved the error alert format and DM notification

**Sign-off Required From:**
- [ ] Will (Founder) — error escalation approval
- [ ] Luciana (Ops Lead) — alert format and operational workflow approval

---

## 17. Open Issues

| ID | Issue | Owner | Status |
|----|-------|-------|--------|
| SA-001 | Slack interactive button handling: confirm whether a Slack interactivity endpoint (separate Make scenario) will be built in Stage 1 or deferred to Stage 2. Until built, "Assign Concierge" and "Mark Hot Lead" buttons do nothing when clicked. | Will | OPEN |
| SA-002 | Slack app credentials: confirm the Slack app name, bot token scope, and workspace it is installed in. Verify the app has `chat:write`, `im:write` scopes. | Systems | OPEN |
| SA-003 | DM recipients for error alerts: confirm Slack user IDs or display names for Luciana and Will. Slack DMs require the user's Slack Member ID, not their display name. | Luciana | OPEN |
| SA-004 | Airtable record deep-link URL: verify that `https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/[RECORD_ID]` resolves to the correct record view. Test manually before production. | Systems | OPEN |
| SA-005 | Timezone display in Slack: `submitted_at` is stored in UTC. Confirm desired display timezone for Slack messages (ET, PT, or UTC). Update `formatDate` formula accordingly. | Luciana | OPEN |
| SA-006 | ME brand Slack channel: confirm whether ME leads should alert to #sss-ops-alerts (same channel) or a separate #me-ops-alerts channel. Current spec uses one channel for both brands. | Will | OPEN |
| SA-007 | Test message prefix: confirm how to visually distinguish test alerts from production alerts in #sss-ops-alerts. Current proposal: prepend `[TEST]` to message text when `environment` flag is present in calling payload. | Luciana | OPEN |
| SA-008 | Audit Log table field names: all Audit Log field names must be verified against live schema (`tblrMpTfMk8q1eNHp`) before build. | Systems | OPEN |

---

## 18. Final Scenario Status

**Status: PENDING BUILD**

> This document is the authoritative build specification for M-SLACK-ALERTS. No Make.com scenario has been created yet.

**Build priority:** Build M-SLACK-ALERTS FIRST among Stage 1 scenarios — its webhook URL is required by M-LEAD-INTAKE Module 10, and M-BRAND-ROUTER sandbox tests require it to validate the AMBIGUOUS alert block.

**Build sequence:**
1. Build M-SLACK-ALERTS → register webhook URL
2. Build M-BRAND-ROUTER logic block (embedded in M-LEAD-INTAKE)
3. Build M-LEAD-INTAKE → configure Module 10 with M-SLACK-ALERTS webhook URL
4. Run end-to-end sandbox test: inbound payload → M-LEAD-INTAKE → M-SLACK-ALERTS → #sss-ops-alerts
