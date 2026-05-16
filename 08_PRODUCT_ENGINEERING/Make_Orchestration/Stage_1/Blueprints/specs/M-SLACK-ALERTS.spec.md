# M-SLACK-ALERTS — Scenario Specification

**Scenario ID:** M-SLACK-ALERTS
**Version:** 1.0
**Status:** Ready for Import
**Last Updated:** 2026-05-16
**Zone:** us1.make.com
**Brands:** She Said Sail (SSS) | Mare Executive (ME)

---

## Overview

M-SLACK-ALERTS is the centralized Slack notification dispatcher for the She Said Sail / Mare Executive automation stack. All other Make scenarios send alert events to this scenario's webhook rather than posting directly to Slack. This ensures consistent message formatting, channel routing logic, and a single point of control for Slack notifications across the entire platform.

**Key behaviors:**
- Single webhook endpoint accepts all alert event types from all other scenarios
- Routes each alert type to the correct Slack channel with type-specific message formatting
- EMERGENCY alerts post to both `#sss-emergency-ops` channel AND send a direct message to Will
- All dispatched alerts are logged to M-AUDIT-LOGGER
- Scenario execution failures are reported to M-AUDIT-LOGGER as `SCENARIO_ERROR` events

---

## Trigger

| Property | Value |
|---|---|
| Type | Instant Webhook (`gateway:CustomWebHook`) |
| Module ID | 1 |
| Webhook Label | M-SLACK-ALERTS Webhook |
| Webhook ID | GENERATED_BY_MAKE_AFTER_IMPORT |
| Authentication | None (internal Make-to-Make calls; secure by URL obscurity) |
| Method | POST |
| Content-Type | application/json |

---

## Incoming Payload Schema

```json
{
  "alert_type": "NEW_LEAD | BOOKING_CREATED | BOOKING_CONFIRMED | DEPOSIT_RECEIVED | CONCIERGE_ASSIGNED | STRIPE_LINK_SENT | AUTOMATION_ERROR | EMERGENCY",
  "brand": "SSS | MARE_EXECUTIVE",
  "message": "string — human-readable alert description",
  "record_id": "string — Airtable record ID (rec...)",
  "urgency": "LOW | MEDIUM | HIGH | CRITICAL",
  "metadata": {
    "lead_name": "string (NEW_LEAD alerts)",
    "city": "string (NEW_LEAD alerts)",
    "date_requested": "string (NEW_LEAD alerts)",
    "budget_range": "string (NEW_LEAD alerts)",
    "package_interest": "string (NEW_LEAD alerts)",
    "source": "string (NEW_LEAD alerts)",
    "duplicate": "boolean (NEW_LEAD duplicate alerts)",
    "party_size": "string | integer (NEW_LEAD alerts)"
  },
  "timestamp": "ISO 8601 datetime string"
}
```

---

## Alert Type to Channel Routing

| Alert Type | Slack Channel | Notes |
|---|---|---|
| `NEW_LEAD` (SSS brand) | `#sss-leads` | Brand-conditional routing |
| `NEW_LEAD` (MARE_EXECUTIVE brand) | `#me-leads` | Brand-conditional routing |
| `BOOKING_CREATED` | `#sss-bookings` | |
| `BOOKING_CONFIRMED` | `#sss-bookings` | |
| `DEPOSIT_RECEIVED` | `#sss-bookings` | |
| `STRIPE_LINK_SENT` | `#sss-bookings` | |
| `CONCIERGE_ASSIGNED` | `#sss-ops` | |
| `AUTOMATION_ERROR` | `#sss-ops-alerts` | |
| `EMERGENCY` | `#sss-emergency-ops` + DM to Will | Dual dispatch |

---

## Module Flow

### Module 1 — Webhook Trigger (`gateway:CustomWebHook`)
Receives the POST payload. All fields available downstream as `{{1.*}}`.

---

### Module 2 — Router (`builtin:BasicRouter`)

Four routes based on `{{1.alert_type}}`. Routes evaluate in order; first matching filter wins.

---

## Route 1 — Lead Alerts (Module 3)

**Filter:** `{{1.alert_type}}` text:equal `NEW_LEAD`

### Module 3 — Slack ActionPostMessage

| Property | Value |
|---|---|
| Module type | `slack:ActionPostMessage` |
| Channel | `{{if(1.brand = 'MARE_EXECUTIVE', '#me-leads', '#sss-leads')}}` |
| Bot name | She Said Sail Bot |
| Icon | :sailboat: |

**Message format:**
```
:sailboat: *New Lead* | *{lead_name}*
> Brand: {brand}
> City: {city}
> Date Requested: {date_requested}
> Budget: {budget_range}
> Package Interest: {package_interest}
> Source: {source}
> Record ID: {record_id}
> Urgency: {urgency}
```

Data sourced from: `{{1.metadata.lead_name}}`, `{{1.brand}}`, `{{1.metadata.city}}`, `{{1.metadata.date_requested}}`, `{{1.metadata.budget_range}}`, `{{1.metadata.package_interest}}`, `{{1.metadata.source}}`, `{{1.record_id}}`, `{{1.urgency}}`

---

## Route 2 — Booking Alerts (Modules 4, 5)

**Filter (OR conditions):** alert_type IN [`BOOKING_CREATED`, `BOOKING_CONFIRMED`, `DEPOSIT_RECEIVED`, `STRIPE_LINK_SENT`]

### Module 4 — Set Variable (`builtin:SetVariable`)

Sets `booking_message` using a `switch()` expression to produce alert-type-specific message text:

| alert_type | Message prefix |
|---|---|
| `BOOKING_CREATED` | :new: *Booking Created* |
| `BOOKING_CONFIRMED` | :white_check_mark: *Booking Confirmed* |
| `DEPOSIT_RECEIVED` | :moneybag: *Deposit Received* |
| `STRIPE_LINK_SENT` | :link: *Stripe Payment Link Sent* |
| _(default)_ | :bell: *Booking Update* \| {alert_type} |

All variants append: `| Record: {record_id}` and `> {message}` on a new line.

### Module 5 — Slack ActionPostMessage

| Property | Value |
|---|---|
| Channel | `#sss-bookings` |
| Text | `{{4.booking_message}}` + Brand, Urgency, Timestamp footer |
| Bot name | She Said Sail Bot |
| Icon | :calendar: |

---

## Route 3 — Ops Alerts (Module 6)

**Filter (OR conditions):** alert_type IN [`CONCIERGE_ASSIGNED`, `AUTOMATION_ERROR`]

### Module 6 — Slack ActionPostMessage

| Property | Value |
|---|---|
| Channel | `{{if(1.alert_type = 'AUTOMATION_ERROR', '#sss-ops-alerts', '#sss-ops')}}` |
| Bot name | She Said Sail Bot |
| Icon | :rotating_light: (AUTOMATION_ERROR) / :bust_in_silhouette: (CONCIERGE_ASSIGNED) |

**Message includes:** alert prefix (type-specific), brand, message body, urgency, timestamp.

| alert_type | Channel | Prefix |
|---|---|---|
| `CONCIERGE_ASSIGNED` | `#sss-ops` | :bust_in_silhouette: *Concierge Assigned* |
| `AUTOMATION_ERROR` | `#sss-ops-alerts` | :rotating_light: *Automation Error* |

---

## Route 4 — Emergency (Modules 7, 8)

**Filter:** `{{1.alert_type}}` text:equal `EMERGENCY`

### Module 7 — Slack ActionPostMessage (Channel)

| Property | Value |
|---|---|
| Channel | `#sss-emergency-ops` |
| Bot name | She Said Sail EMERGENCY Bot |
| Icon | :rotating_light: |

**Message format:**
```
:rotating_light::rotating_light: *EMERGENCY ALERT* :rotating_light::rotating_light:
> Brand: {brand}
> Record: {record_id}
> Message: {message}
> Urgency: {urgency}
> Timestamp: {timestamp}
> Details: {metadata}
```

### Module 8 — Slack ActionPostMessage (DM to Will)

| Property | Value |
|---|---|
| Channel | `WILL_SLACK_USER_ID_PLACEHOLDER` (DM by user ID) |
| Bot name | She Said Sail EMERGENCY Bot |
| Icon | :rotating_light: |

**Message format:**
```
:rotating_light: *EMERGENCY — Direct Alert*
> Brand: {brand}
> Record: {record_id}
> Message: {message}
> Urgency: {urgency}
> Timestamp: {timestamp}

Please check #sss-emergency-ops immediately.
```

---

## Post-Router Modules (All Routes)

### Module 9 — HTTP POST to M-AUDIT-LOGGER (Success log)

| Property | Value |
|---|---|
| Module type | `http:ActionSendData` |
| URL | INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER webhook) |
| Method | POST |
| handleErrors | true (captures HTTP errors for Make's error log) |

**Payload fields:** scenario_id=`M-SLACK-ALERTS`, event_type=`ALERT_SENT`, alert_type, brand, record_id, urgency, timestamp

### Module 10 — HTTP POST to M-AUDIT-LOGGER (Error handler)

| Property | Value |
|---|---|
| Module type | `http:ActionSendData` |
| URL | INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT (M-AUDIT-LOGGER webhook) |
| Method | POST |
| handleErrors | false (best-effort; must not block) |

**Payload fields:** scenario_id=`M-SLACK-ALERTS`, event_type=`SCENARIO_ERROR`, alert_type, brand, record_id, error_message, timestamp

> Note: Module 10 must be connected to Make's error-handler path. After import, use the Make scenario editor to link module 10 to the error route of the scenario (right-click the module → Set up error handler).

---

## Field Mappings Summary

| Incoming Field | Used In |
|---|---|
| `alert_type` | Router filter, all Slack messages, audit log |
| `brand` | Channel selection (lead alerts, ops alerts), all messages |
| `message` | Slack message body (all routes) |
| `record_id` | All Slack messages, audit log |
| `urgency` | All Slack messages, audit log |
| `metadata.lead_name` | NEW_LEAD message |
| `metadata.city` | NEW_LEAD message |
| `metadata.date_requested` | NEW_LEAD message |
| `metadata.budget_range` | NEW_LEAD message |
| `metadata.package_interest` | NEW_LEAD message |
| `metadata.source` | NEW_LEAD message |
| `timestamp` | All messages, audit log |

---

## Error Handling

| Condition | Behavior |
|---|---|
| Unrecognized alert_type | No router branch matches; Make logs a filter-not-matched warning. Audit log still fires (module 9). |
| Slack API failure | Make retries up to `maxErrors: 3`. If all retries fail, module 10 (error handler) fires SCENARIO_ERROR to M-AUDIT-LOGGER. |
| M-AUDIT-LOGGER call failure (module 9) | handleErrors: true — captured in Make's error log but does not break Slack dispatch. |
| M-AUDIT-LOGGER error handler failure (module 10) | handleErrors: false — silent failure; best-effort only. |

---

## Placeholders to Rebind After Import

| Placeholder | Module(s) | Action Required |
|---|---|---|
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Module 1 — Webhook hook ID | Make auto-assigns on import; copy the generated webhook URL for all calling scenarios |
| `RECONNECT_SLACK_CONNECTION` | Modules 3, 5, 6, 7, 8 | Select the saved Slack OAuth connection for the She Said Sail workspace |
| `WILL_SLACK_USER_ID_PLACEHOLDER` | Module 8 — channel field | Replace with Will's actual Slack user ID (format: `U...`). Find via Slack profile → Copy member ID. |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 9) | Module 9 — HTTP URL | Paste the live webhook URL for M-AUDIT-LOGGER (success log) |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` (module 10) | Module 10 — HTTP URL | Paste the live webhook URL for M-AUDIT-LOGGER (error handler) |

---

## Test Steps

1. Deploy scenario in Make (us1.make.com) and copy the generated webhook URL.
2. Update all other deployed scenarios to use this webhook URL as their M-SLACK-ALERTS target.
3. Send each test payload variant from `M-SLACK-ALERTS.test.json`:

   **new_lead_sss:** Verify message appears in `#sss-leads` with sailboat icon and all lead fields.
   **new_lead_me:** Verify message appears in `#me-leads` (brand = MARE_EXECUTIVE).
   **booking_created:** Verify `:new: *Booking Created*` message appears in `#sss-bookings`.
   **booking_confirmed:** Verify `:white_check_mark: *Booking Confirmed*` in `#sss-bookings`.
   **deposit_received:** Verify `:moneybag: *Deposit Received*` in `#sss-bookings`.
   **stripe_link_sent:** Verify `:link: *Stripe Payment Link Sent*` in `#sss-bookings`.
   **concierge_assigned:** Verify message appears in `#sss-ops` (NOT `#sss-ops-alerts`).
   **automation_error:** Verify message appears in `#sss-ops-alerts` (NOT `#sss-ops`).
   **emergency:** Verify message appears in BOTH `#sss-emergency-ops` AND as a DM to Will.

4. After each test, verify M-AUDIT-LOGGER received an `ALERT_SENT` event with the correct `alert_type`.
5. Test error handling: temporarily break the Slack connection and trigger any alert. Verify M-AUDIT-LOGGER receives a `SCENARIO_ERROR` event.
6. Confirm no duplicate messages appear in any channel.
7. Confirm bot name displays as "She Said Sail Bot" (or "She Said Sail EMERGENCY Bot" for emergency alerts).
