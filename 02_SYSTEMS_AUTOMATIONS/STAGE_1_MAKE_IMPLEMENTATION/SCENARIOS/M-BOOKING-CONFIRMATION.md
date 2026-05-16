# M-BOOKING-CONFIRMATION — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Booking Confirmation Preparation  
**Execution Order:** Module 7 in Stage 1 pipeline (called by M-BOOKING-CREATION)

---

## 1. Scenario Name

`M-BOOKING-CONFIRMATION`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references in M-BOOKING-CREATION (caller).

---

## 3. Trigger Type

**Trigger:** Called by M-BOOKING-CREATION immediately after a Booking record is successfully created and the Request record is updated with the Booking link.

**Invocation method:** HTTP POST to M-BOOKING-CONFIRMATION's Make webhook URL (or Make native scenario-to-scenario call).

**Input received from M-BOOKING-CREATION:**
```json
{
  "booking_record_id": "{{airtable_booking_record_id}}",
  "client_record_id": "{{airtable_client_record_id}}",
  "request_record_id": "{{airtable_request_record_id}}",
  "booking_id_human": "{{BK-YYYY-NNNN}}",
  "brand": "SSS | ME",
  "city": "{{city_string}}",
  "environment": "Production | Sandbox",
  "triggered_by_scenario": "M-BOOKING-CREATION",
  "booking_created_at": "{{iso8601_timestamp}}"
}
```

**Secondary trigger (resilience):** Airtable Watch on Bookings table — fires when `Confirmation_Status` field transitions to empty or is populated with value other than `DRAFT_READY` or `SENT` AND `Status = DEPOSIT_SENT`. This catches cases where M-BOOKING-CREATION's downstream call fails after Booking creation.

---

## 4. CRITICAL SAFETY RULE — Stage 1 TEST MODE ONLY

> **THIS IS THE MOST IMPORTANT CONSTRAINT IN THIS SCENARIO.**

**In Stage 1, NO real client emails or SMS messages are sent by this scenario under any circumstances.**

The full behavior in Stage 1:
1. This scenario assembles the complete, brand-accurate confirmation email body using the appropriate SSS or ME template.
2. The assembled email is written to the `Confirmation_Email_Draft` field on the Booking record in Airtable.
3. Timestamps and status fields are updated to indicate the draft is ready for human review.
4. A Slack notification is sent to Luciana in #sss-ops-alerts with the full draft included, prompting her to manually review and send from the appropriate Gmail account.
5. **The Gmail `Send Email` module does NOT appear in this scenario in Stage 1.** It does not exist in the module sequence. It is not configured. It is not connected. It will be added in Stage 2 only.
6. **The Quo SMS module does NOT appear in this scenario in Stage 1.** Same reasoning as Gmail.

**Rationale:** Until sandbox validation is complete and Will has approved the email templates, client-facing communication must remain under direct human control. The automation prepares; the human sends. This preserves the relationship quality of both brands while the system is being validated.

**Stage 2 activation:** See Section 11 (Stage 2 Upgrade Path) for the precise modules that will be added.

---

## 5. Exact Module Sequence

### Module 1 — [Airtable] Get Booking Record

**Make Module Type:** Airtable — Get a Record  
**Table:** Bookings (`tbl72omPibBkn2hZL`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID Source:** `{{trigger.booking_record_id}}`

**Fields retrieved:**

| Field Name                | Used In Module |
|---------------------------|----------------|
| `Booking_ID_Human`        | 5, 6, 9, 10    |
| `Status`                  | Guard check    |
| `Brand`                   | 4              |
| `City`                    | 9, 10          |
| `Charter_Date`            | 5, 6           |
| `Charter_Time`            | 5, 6           |
| `Group_Size`              | 5, 6           |
| `Package_Price`           | 5, 6           |
| `Deposit_Amount`          | 5, 6           |
| `Balance_Due`             | 5, 6           |
| `Deposit_Link`            | 5, 6           |
| `Occasion`                | 5, 6           |
| `Confirmation_Status`     | Guard check    |
| `Automations_Paused`      | Guard check    |
| `Environment`             | 7, 8, 9, 10    |
| `Client` (linked record)  | Module 2       |
| `Package` (linked record) | Module 3       |
| `Concierge_Assigned`      | 5, 6           |

**Guard checks (abort if conditions are not met):**

- If `{{1.Status}}` is not `DEPOSIT_SENT`: log to Slack and halt. The confirmation template is only appropriate for the DEPOSIT_SENT stage.
- If `{{1.Automations_Paused}}` is `true`: log to Slack and halt. Ops has paused automation for this Booking.
- If `{{1.Confirmation_Status}}` is `DRAFT_READY` or `SENT`: idempotency — draft already exists. Log to Slack and halt.

---

### Module 2 — [Airtable] Get Linked Client Record

**Make Module Type:** Airtable — Get a Record  
**Table:** Clients (`tblr84vRIWC5HmKvo`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID Source:** `{{1.Client[0].id}}` (first linked record from Booking's Client field)

**Fields retrieved:**

| Field Name     | Used In Module | Notes                                   |
|----------------|----------------|-----------------------------------------|
| `First_Name`   | 5, 6, 9        | Primary salutation                      |
| `Last_Name`    | 5, 6           | Full name in subject                    |
| `Email`        | 5, 6           | Recipient address (NOT sent in Stage 1) |
| `Phone`        | 5, 6           | SMS recipient (NOT sent in Stage 1)     |

**Error Handler:** If Client record not found, post to Slack: "M-BOOKING-CONFIRMATION FAILED: No Client record linked to Booking `{{trigger.booking_id_human}}`. Cannot prepare confirmation. Manual review required." Halt scenario.

---

### Module 3 — [Airtable] Get Linked Package Record

**Make Module Type:** Airtable — Get a Record  
**Table:** Packages (table ID to be confirmed in Airtable)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID Source:** `{{1.Package[0].id}}` (first linked record from Booking's Package field)

**Conditional execution:** Only runs if `{{1.Package}}` is not empty. If Package is empty, set variables:
```
package_name = "Custom Charter Package"
package_includes = "Details to be confirmed by your concierge"
fb_standard = "Complimentary beverages and light refreshments"
vessel_name = "To be confirmed"
marina_name = "To be confirmed"
```

**Fields retrieved when Package exists:**

| Field Name         | Used In Module | Notes                                       |
|--------------------|----------------|---------------------------------------------|
| `Package_Name`     | 5, 6           | e.g., "Sunset Sailing Experience"           |
| `Package_Includes` | 5, 6           | Bulleted list of inclusions                 |
| `FB_Standard`      | 5, 6           | e.g., "Premium open bar + charcuterie"      |
| `Vessel_Name`      | 5, 6           | e.g., "S/Y Alegría"                         |
| `Marina_Name`      | 5, 6           | e.g., "Miami Beach Marina, Dock 12"         |
| `Duration_Hours`   | 5, 6           | e.g., "4"                                   |

---

### Module 4 — [Router] Route by Brand

**Make Module Type:** Router (built-in)  
**Source value:** `{{1.Brand}}`

**Route A — SSS (She Said Sail):**
- Condition: `{{1.Brand}}` = `SSS`
- Proceeds to Module 5

**Route B — ME (Mare Executive):**
- Condition: `{{1.Brand}}` = `ME`
- Proceeds to Module 6

**Route C — Unknown Brand (fallback):**
- Condition: Neither SSS nor ME
- Log to Slack: "M-BOOKING-CONFIRMATION: Unknown brand `{{1.Brand}}` for Booking `{{trigger.booking_id_human}}`. Cannot select template. Halting."
- Call M-AUDIT-LOGGER with failure payload
- Halt

---

### Module 5 — [Text Aggregator] Assemble SSS Confirmation Email Body

**Make Module Type:** Tools — Text Aggregator (or Set Variable with multi-line template)  
**Runs when:** Router Module 4 Route A (Brand = SSS)

**Subject line:**
```
Your She Said Sail Booking is Confirmed — {{booking_id_human}} | {{charter_date_formatted}}
```

**Full email body:** See Section 7 (SSS Email Template) for complete HTML template with all variable substitutions.

**Output variable:** `assembled_email_body_html` (consumed by Module 7)  
**Output variable:** `assembled_email_subject` (consumed by Module 7)

---

### Module 6 — [Text Aggregator] Assemble ME Confirmation Email Body

**Make Module Type:** Tools — Text Aggregator (or Set Variable with multi-line template)  
**Runs when:** Router Module 4 Route B (Brand = ME)

**Subject line:**
```
Mare Executive Charter Confirmation — {{booking_id_human}} | {{charter_date_formatted}}
```

**Full email body:** See Section 8 (ME Email Template) for complete HTML template with all variable substitutions.

**Output variable:** `assembled_email_body_html` (consumed by Module 7)  
**Output variable:** `assembled_email_subject` (consumed by Module 7)

---

### Module 7 — [Airtable] Write Assembled Email Draft to Booking Record

**Make Module Type:** Airtable — Update a Record  
**Table:** Bookings (`tbl72omPibBkn2hZL`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID:** `{{trigger.booking_record_id}}`

**Fields written:**

| Field Name                   | Value                                                       |
|------------------------------|-------------------------------------------------------------|
| `Confirmation_Email_Draft`   | `{{assembled_email_body_html}}`                             |
| `Confirmation_Email_Subject` | `{{assembled_email_subject}}`                               |
| `Confirmation_Recipient`     | `{{2.Email}}` (Client email — stored but NOT sent Stage 1) |
| `Confirmation_Phone`         | `{{2.Phone}}` (Client phone — stored but NOT sent Stage 1) |

**Error Handler:** If write fails, post to Slack and halt. Do not continue to Module 8 or 9.

---

### Module 8 — [Airtable] Write Confirmation Timestamps and Status

**Make Module Type:** Airtable — Update a Record  
**Table:** Bookings (`tbl72omPibBkn2hZL`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID:** `{{trigger.booking_record_id}}`

**Fields written:**

| Field Name                    | Value                    | Notes                                    |
|-------------------------------|--------------------------|------------------------------------------|
| `Confirmation_Prepared_At`    | `{{now}}`                | ISO 8601 timestamp                       |
| `Confirmation_Status`         | `DRAFT_READY`            | Signals Luciana that draft is ready      |
| `Confirmation_Prepared_By`    | `M-BOOKING-CONFIRMATION` | Traceability                             |

> **NOTE:** `Confirmation_Status` intentionally does NOT advance to `SENT` in Stage 1. The status moves to `SENT` only after Luciana manually sends the email and updates the Booking record (or in Stage 2 when the Gmail module is activated).

---

### Module 9 — [Slack] Post Confirmation Ready Notification to Luciana

**Make Module Type:** Slack — Create a Message  
**Channel:** `#sss-ops-alerts`  
**Post As:** She Said Sail Automations (bot)

**Message template:**
```
:envelope: *Confirmation Draft Ready — Action Required*

*Booking:* {{trigger.booking_id_human}}
*Client:* {{2.First_Name}} {{2.Last_Name}}
*Email:* {{2.Email}}
*Phone:* {{2.Phone}}
*Charter:* {{1.Charter_Date}} at {{1.Charter_Time}}
*City:* {{1.City}}
*Brand:* {{1.Brand}}
*Package:* {{package_name}}
*Group Size:* {{1.Group_Size}}
*Deposit Amount:* ${{deposit_amount_formatted}}

*ACTION REQUIRED — STAGE 1 MANUAL SEND:*
The confirmation email draft has been written to the Booking record.
Please review and send from *{{gmail_address}}* to *{{2.Email}}*.

:point_right: *Open Booking in Airtable:*
https://airtable.com/appdZ49WqgjRXxA1R/tbl72omPibBkn2hZL/{{trigger.booking_record_id}}

After sending, update `Confirmation_Status` to `SENT` on the Booking record.

_Environment: {{1.Environment}} | Scenario: M-BOOKING-CONFIRMATION_
```

**Variable `gmail_address` resolution:**
- If `Brand = SSS` → `hello@shesaidsail.com`
- If `Brand = ME` → `hello@mareexecutive.com`

**Conditional prefix:** If environment = Sandbox, prepend `[SANDBOX TEST — DO NOT ACTION]` to the message.

---

### Module 10 — [HTTP] Call M-AUDIT-LOGGER Sub-Scenario

**Make Module Type:** HTTP — Make a Request (POST to M-AUDIT-LOGGER webhook)

**Payload sent to M-AUDIT-LOGGER:**
```json
{
  "triggering_event": "Booking confirmation email draft prepared for {{trigger.booking_id_human}}",
  "source_data": "Booking record ID: {{trigger.booking_record_id}}; Client record ID: {{trigger.client_record_id}}; Brand: {{1.Brand}}; Charter Date: {{1.Charter_Date}}",
  "scenario_name": "M-BOOKING-CONFIRMATION",
  "output": "Confirmation_Email_Draft written to Booking record; Confirmation_Status set to DRAFT_READY; Slack notification sent to #sss-ops-alerts for manual send",
  "destination": "Airtable Bookings table tbl72omPibBkn2hZL (draft fields); Slack #sss-ops-alerts (human notification)",
  "approval_state": "PENDING_HUMAN",
  "brand": "{{1.Brand}}",
  "city": "{{1.City}}",
  "environment": "{{1.Environment}}",
  "affected_record_id": "{{trigger.booking_record_id}}",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

**Note on `approval_state`:** This is `PENDING_HUMAN` (not `AUTONOMOUS`) because the confirmation email requires Luciana's manual review and send action before the client communication is complete. The automation has done its portion; a human completes the loop.

**On M-AUDIT-LOGGER failure:** Post to Slack #sss-ops-alerts: "SEV-1: M-AUDIT-LOGGER failed for M-BOOKING-CONFIRMATION. Booking `{{trigger.booking_id_human}}` confirmation draft prepared but NOT logged. Manual audit entry required."

---

### Module 11 — NOTE: Stage 2 Modules (NOT present in Stage 1)

The following modules will be inserted between Modules 8 and 9 in Stage 2, replacing the manual Slack alert with automated sends:

```
[Stage 2 — Module 9a] Gmail — Send Email
  Account: hello@shesaidsail.com OR hello@mareexecutive.com (based on Brand)
  To: {{2.Email}}
  Subject: {{assembled_email_subject}}
  Body: {{assembled_email_body_html}}
  Content type: HTML

[Stage 2 — Module 9b] Quo SMS — Send Message
  To: {{2.Phone}}
  Body: "Hi {{2.First_Name}}, your {{brand_name}} booking is confirmed for {{charter_date_short}}!
         Check your email for full details. Questions? Reply to this message. — {{concierge_name}}"
  From: {{brand_sms_number}}

[Stage 2 — Module 8 update] Change Confirmation_Status write value from DRAFT_READY to SENT
[Stage 2 — Module 8 add field] Confirmation_Sent_At = {{now}}
```

---

## 6. Email Template Variables — Complete List

The following variables are substituted in both the SSS and ME email templates. Every variable must resolve to a non-null value before the Text Aggregator module runs.

| Variable                  | Source                                             | Fallback if empty                           |
|---------------------------|----------------------------------------------------|---------------------------------------------|
| `{{client_first_name}}`   | `{{2.First_Name}}`                                 | `"Valued Guest"` (never expected to be null)|
| `{{booking_id}}`          | `{{trigger.booking_id_human}}`                     | No fallback — halt if null                  |
| `{{charter_date}}`        | `{{1.Charter_Date}}` formatted as `MMMM D, YYYY`  | No fallback — halt if null                  |
| `{{charter_date_short}}`  | `{{1.Charter_Date}}` formatted as `MM/DD/YYYY`    | No fallback — halt if null                  |
| `{{charter_time}}`        | `{{1.Charter_Time}}`                               | `"Time to be confirmed"`                    |
| `{{vessel_name}}`         | `{{3.Vessel_Name}}`                                | `"Your private vessel"`                     |
| `{{marina_name}}`         | `{{3.Marina_Name}}`                                | `"Marina details to follow"`                |
| `{{package_name}}`        | `{{3.Package_Name}}`                               | `"Custom Charter Package"`                  |
| `{{package_includes}}`    | `{{3.Package_Includes}}`                           | `"Full details from your concierge"`        |
| `{{fb_standard}}`         | `{{3.FB_Standard}}`                                | `"Complimentary beverages"`                 |
| `{{duration_hours}}`      | `{{3.Duration_Hours}}`                             | `""`                                        |
| `{{group_size}}`          | `{{1.Group_Size}}`                                 | No fallback — halt if null                  |
| `{{deposit_amount}}`      | `{{1.Deposit_Amount}}` formatted as `$X,XXX.00`   | No fallback — halt if null                  |
| `{{total_amount}}`        | `{{1.Package_Price}}` formatted as `$X,XXX.00`    | `"Confirmed with your concierge"`           |
| `{{balance_due_amount}}`  | `{{1.Balance_Due}}` formatted as `$X,XXX.00`      | `"Balance details to follow"`               |
| `{{balance_due_date}}`    | Charter_Date minus 7 days, formatted `MMMM D, YYYY`| `"14 days before your charter"`            |
| `{{deposit_link}}`        | `{{1.Deposit_Link}}`                               | Omit CTA button if null                     |
| `{{concierge_name}}`      | `{{1.Concierge_Assigned[0].name}}`                 | `"The She Said Sail Team"` / `"The Mare Executive Team"` |
| `{{brand_signature}}`     | Resolved by Router (Section 7/8)                  | No fallback                                 |
| `{{gmail_address}}`       | SSS → `hello@shesaidsail.com` / ME → `hello@mareexecutive.com` | No fallback    |
| `{{brand_name}}`          | `"She Said Sail"` or `"Mare Executive"`            | No fallback                                 |
| `{{occasion}}`            | `{{1.Occasion}}`                                   | *(omit from template if empty)*             |

**Variable validation (pre-template):** Before running the Text Aggregator, add a [Tools] — Set Variable module that checks for null values on all no-fallback variables. If any are null, route to error handler.

---

## 7. SSS Email Template — Full Specification

**Brand tone:** Warm, celebratory, aspirational. She Said Sail is a luxury experience for life's best moments.

**Subject line:**
```
Your She Said Sail Booking is Confirmed — {{booking_id}} | {{charter_date}}
```

**HTML Email Body:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Booking is Confirmed</title>
</head>
<body style="margin:0; padding:0; background-color:#f8f6f2; font-family:'Georgia', serif;">

  <!-- Header -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#1a1a2e; padding:32px 0;">
    <tr>
      <td align="center">
        <img src="https://shesaidsail.com/logo-light.png" alt="She Said Sail" height="48" />
        <p style="color:#c9a96e; font-size:13px; letter-spacing:3px; margin:8px 0 0;">LUXURY SAILING CHARTERS</p>
      </td>
    </tr>
  </table>

  <!-- Body -->
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:0 auto; background-color:#ffffff;">
    <tr>
      <td style="padding:48px 40px 32px;">

        <p style="font-size:22px; color:#1a1a2e; margin:0 0 8px;">You're going sailing, {{client_first_name}}.</p>
        <p style="font-size:15px; color:#666; margin:0 0 32px; line-height:1.6;">
          Your booking is confirmed and we are absolutely delighted to have you aboard.
          Here are your complete charter details.
        </p>

        <!-- Booking Details Box -->
        <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8f6f2; border-left:4px solid #c9a96e; padding:0; margin-bottom:32px;">
          <tr>
            <td style="padding:24px 28px;">
              <p style="font-size:11px; letter-spacing:2px; color:#c9a96e; margin:0 0 16px; font-family:Arial,sans-serif;">BOOKING CONFIRMATION</p>
              <table width="100%" cellpadding="4" cellspacing="0" style="font-family:Arial,sans-serif; font-size:14px; color:#333;">
                <tr><td style="color:#999; width:45%;">Booking Reference</td><td><strong>{{booking_id}}</strong></td></tr>
                <tr><td style="color:#999;">Charter Date</td><td><strong>{{charter_date}}</strong></td></tr>
                <tr><td style="color:#999;">Departure Time</td><td><strong>{{charter_time}}</strong></td></tr>
                <tr><td style="color:#999;">Vessel</td><td><strong>{{vessel_name}}</strong></td></tr>
                <tr><td style="color:#999;">Marina / Dock</td><td><strong>{{marina_name}}</strong></td></tr>
                <tr><td style="color:#999;">Package</td><td><strong>{{package_name}}</strong></td></tr>
                <tr><td style="color:#999;">Group Size</td><td><strong>{{group_size}} guests</strong></td></tr>
              </table>
            </td>
          </tr>
        </table>

        <!-- What's Included -->
        <p style="font-size:11px; letter-spacing:2px; color:#c9a96e; margin:0 0 12px; font-family:Arial,sans-serif;">WHAT'S INCLUDED</p>
        <p style="font-size:14px; color:#444; line-height:1.8; margin:0 0 8px;">{{package_includes}}</p>
        <p style="font-size:14px; color:#444; line-height:1.8; margin:0 0 32px;"><em>Food &amp; Beverage: {{fb_standard}}</em></p>

        <!-- Payment Summary -->
        <p style="font-size:11px; letter-spacing:2px; color:#c9a96e; margin:0 0 12px; font-family:Arial,sans-serif;">PAYMENT SUMMARY</p>
        <table width="100%" cellpadding="6" cellspacing="0" style="font-family:Arial,sans-serif; font-size:14px; color:#333; margin-bottom:32px; border-top:1px solid #eee;">
          <tr style="border-bottom:1px solid #eee;"><td>Total Charter Value</td><td align="right"><strong>{{total_amount}}</strong></td></tr>
          <tr style="border-bottom:1px solid #eee;"><td style="color:#2e7d32;">Deposit Received</td><td align="right" style="color:#2e7d32;"><strong>{{deposit_amount}}</strong></td></tr>
          <tr><td><strong>Balance Due</strong></td><td align="right"><strong>{{balance_due_amount}}</strong></td></tr>
        </table>
        <p style="font-size:13px; color:#888; font-family:Arial,sans-serif; margin:0 0 32px;">
          The remaining balance of <strong>{{balance_due_amount}}</strong> is due by <strong>{{balance_due_date}}</strong>.
          Your concierge will send a payment link closer to the date.
        </p>

        <!-- Concierge Sign-off -->
        <p style="font-size:15px; color:#1a1a2e; line-height:1.7; margin:0 0 8px;">
          Your concierge <strong>{{concierge_name}}</strong> will be in touch soon with final vessel details,
          boarding instructions, and everything you need to know for a perfect day on the water.
        </p>
        <p style="font-size:15px; color:#1a1a2e; line-height:1.7; margin:0 0 32px;">
          Questions before then? Simply reply to this email — we are always here.
        </p>

        <p style="font-size:14px; color:#888; font-family:Arial,sans-serif;">With warmth,</p>
        <p style="font-size:15px; color:#1a1a2e; margin:4px 0 0;"><strong>{{brand_signature}}</strong></p>
        <p style="font-size:13px; color:#888; font-family:Arial,sans-serif; margin:4px 0 0;">She Said Sail — {{gmail_address}}</p>

      </td>
    </tr>
  </table>

  <!-- Footer -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#1a1a2e; padding:24px 0; margin-top:0;">
    <tr>
      <td align="center">
        <p style="color:#666; font-size:11px; font-family:Arial,sans-serif; margin:0;">
          © 2026 She Said Sail. All rights reserved.<br>
          This confirmation was sent to {{2.Email}} for booking {{booking_id}}.
        </p>
      </td>
    </tr>
  </table>

</body>
</html>
```

**`{{brand_signature}}`** resolves to: `"{{concierge_name}} &amp; The She Said Sail Team"`

---

## 8. ME Email Template — Full Specification

**Brand tone:** Professional, efficient, executive-grade. Mare Executive is built for corporate clients who expect precision.

**Subject line:**
```
Mare Executive Charter Confirmation — {{booking_id}} | {{charter_date}}
```

**HTML Email Body:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Charter Confirmation</title>
</head>
<body style="margin:0; padding:0; background-color:#f5f5f5; font-family:Arial,Helvetica,sans-serif;">

  <!-- Header -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0d2137; padding:28px 0;">
    <tr>
      <td align="center">
        <img src="https://mareexecutive.com/logo-light.png" alt="Mare Executive" height="44" />
        <p style="color:#8eb4d4; font-size:11px; letter-spacing:4px; margin:6px 0 0; font-family:Arial,sans-serif;">EXECUTIVE MARITIME EXPERIENCES</p>
      </td>
    </tr>
  </table>

  <!-- Body -->
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width:600px; margin:0 auto; background-color:#ffffff; border:1px solid #ddd;">
    <tr>
      <td style="padding:40px 40px 32px;">

        <p style="font-size:18px; color:#0d2137; margin:0 0 6px; font-weight:bold;">Charter Confirmed — {{booking_id}}</p>
        <p style="font-size:14px; color:#555; margin:0 0 28px; line-height:1.5;">
          Dear {{client_first_name}}, your Mare Executive charter is confirmed.
          Please retain this document for your records.
        </p>

        <!-- Charter Summary -->
        <table width="100%" cellpadding="0" cellspacing="0" style="border:1px solid #dce3ea; margin-bottom:28px;">
          <tr style="background:#0d2137;">
            <td colspan="2" style="padding:12px 20px;">
              <p style="font-size:11px; color:#8eb4d4; letter-spacing:2px; margin:0;">CHARTER DETAILS</p>
            </td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; width:40%; border-bottom:1px solid #eee;">Confirmation Number</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{booking_id}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; border-bottom:1px solid #eee;">Charter Date</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{charter_date}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; border-bottom:1px solid #eee;">Departure Time</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{charter_time}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; border-bottom:1px solid #eee;">Vessel</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{vessel_name}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; border-bottom:1px solid #eee;">Embarkation</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{marina_name}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888; border-bottom:1px solid #eee;">Service Package</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137; border-bottom:1px solid #eee;"><strong>{{package_name}}</strong></td>
          </tr>
          <tr>
            <td style="padding:10px 20px; font-size:13px; color:#888;">Group Size</td>
            <td style="padding:10px 20px; font-size:13px; color:#0d2137;"><strong>{{group_size}} attendees</strong></td>
          </tr>
        </table>

        <!-- Service Inclusions -->
        <p style="font-size:11px; color:#8eb4d4; letter-spacing:2px; margin:0 0 10px; background:#0d2137; padding:10px 20px; margin-left:-40px; margin-right:-40px;">PACKAGE INCLUSIONS</p>
        <div style="padding:0 0 20px;">
          <p style="font-size:14px; color:#444; line-height:1.7; margin:16px 0 8px;">{{package_includes}}</p>
          <p style="font-size:13px; color:#666; font-style:italic; margin:0 0 28px;">Catering: {{fb_standard}}</p>
        </div>

        <!-- Financial Summary -->
        <p style="font-size:11px; color:#8eb4d4; letter-spacing:2px; margin:0 0 10px; background:#0d2137; padding:10px 20px; margin-left:-40px; margin-right:-40px;">FINANCIAL SUMMARY</p>
        <table width="100%" cellpadding="8" cellspacing="0" style="font-size:13px; color:#333; margin:16px 0 8px; border-collapse:collapse;">
          <tr style="border-bottom:1px solid #eee;"><td>Charter Fee</td><td align="right">{{total_amount}}</td></tr>
          <tr style="border-bottom:1px solid #eee; color:#2e7d32;"><td>Deposit Received</td><td align="right">{{deposit_amount}}</td></tr>
          <tr style="font-weight:bold; font-size:14px;"><td>Balance Outstanding</td><td align="right">{{balance_due_amount}}</td></tr>
        </table>
        <p style="font-size:12px; color:#888; margin:4px 0 32px;">
          Balance of {{balance_due_amount}} due by {{balance_due_date}}.
          A payment link will be provided separately.
        </p>

        <!-- Sign-off -->
        <p style="font-size:14px; color:#333; line-height:1.6; margin:0 0 8px;">
          Your dedicated point of contact is <strong>{{concierge_name}}</strong>,
          who will follow up with logistics, boarding instructions, and any pre-charter requirements.
        </p>
        <p style="font-size:14px; color:#333; line-height:1.6; margin:0 0 28px;">
          For any immediate questions, please reply directly to this message.
        </p>

        <p style="font-size:13px; color:#888; margin:0;">Regards,</p>
        <p style="font-size:14px; color:#0d2137; margin:4px 0 0;"><strong>{{brand_signature}}</strong></p>
        <p style="font-size:12px; color:#888; margin:4px 0 0;">Mare Executive — {{gmail_address}}</p>

      </td>
    </tr>
  </table>

  <!-- Footer -->
  <table width="100%" cellpadding="0" cellspacing="0" style="background:#0d2137; padding:20px 0; margin-top:0;">
    <tr>
      <td align="center">
        <p style="color:#4a6a8a; font-size:11px; margin:0;">
          © 2026 Mare Executive. All rights reserved.<br>
          Confirmation sent to {{2.Email}} — Reference: {{booking_id}}
        </p>
      </td>
    </tr>
  </table>

</body>
</html>
```

**`{{brand_signature}}`** resolves to: `"{{concierge_name}}, Mare Executive"`

---

## 9. Airtable Fields Written — Complete Specification

All Airtable writes performed by M-BOOKING-CONFIRMATION, in execution order.

| Module | Table      | Field Name                    | Value Written                     | Field Type       | Stage 1 / Stage 2 |
|--------|------------|-------------------------------|-----------------------------------|------------------|-------------------|
| 7      | Bookings   | `Confirmation_Email_Draft`    | Full assembled HTML body          | Long text        | Stage 1           |
| 7      | Bookings   | `Confirmation_Email_Subject`  | Assembled subject line string     | Single line text | Stage 1           |
| 7      | Bookings   | `Confirmation_Recipient`      | Client email address              | Email            | Stage 1           |
| 7      | Bookings   | `Confirmation_Phone`          | Client phone number               | Phone            | Stage 1           |
| 8      | Bookings   | `Confirmation_Prepared_At`    | ISO 8601 timestamp (`{{now}}`)    | Date/Time        | Stage 1           |
| 8      | Bookings   | `Confirmation_Status`         | `DRAFT_READY`                     | Single select    | Stage 1 (→ `SENT` in Stage 2) |
| 8      | Bookings   | `Confirmation_Prepared_By`    | `M-BOOKING-CONFIRMATION`          | Single line text | Stage 1           |
| S2-9a  | Bookings   | `Confirmation_Sent_At`        | ISO 8601 timestamp                | Date/Time        | **Stage 2 only**  |
| S2-9a  | Bookings   | `Confirmation_Status`         | `SENT` (overwrites `DRAFT_READY`) | Single select    | **Stage 2 only**  |

---

## 10. Rollback — Clearing a Draft for Regeneration

**When to regenerate:** The draft email contains incorrect data (wrong charter date, wrong package name, Ops needs a different tone). Luciana or Will identifies the issue before sending.

**Manual regeneration procedure:**

1. In Airtable, open the Booking record
2. Clear the following fields manually:
   - `Confirmation_Email_Draft` → empty
   - `Confirmation_Email_Subject` → empty
   - `Confirmation_Status` → clear (set to `PENDING` or empty)
   - `Confirmation_Prepared_At` → clear
3. Fix the underlying data error (wrong charter date → fix `Charter_Date` field; wrong package → update `Package` linked field)
4. Trigger M-BOOKING-CONFIRMATION manually by calling its webhook with the Booking record ID
5. Verify the new draft appears in `Confirmation_Email_Draft`

**Automated re-generation trigger (alternative to manual webhook call):**
- If the secondary Airtable Watch trigger on the Bookings table is configured, clearing `Confirmation_Status` to empty will re-fire the Watch and re-trigger M-BOOKING-CONFIRMATION automatically.
- **Caution:** Only use this method after confirming the root-cause data error is fully corrected. Running M-BOOKING-CONFIRMATION against incorrect Booking data will produce another incorrect draft.

**Draft is NOT deleted from Airtable after Stage 2 activation.** Even when Stage 2 sends the email automatically, the `Confirmation_Email_Draft` field retains the sent content as an immutable record of what was communicated to the client.

---

## 11. Stage 2 Upgrade Path — Activating Real Client Sends

Precisely what changes in Stage 2 to activate automated client communication:

**Prerequisites before Stage 2 activation:**
- [ ] Will has reviewed and approved both SSS and ME email templates
- [ ] Gmail OAuth connections for `hello@shesaidsail.com` and `hello@mareexecutive.com` are authenticated in Make.com
- [ ] Quo SMS account connected to Make.com with SSS and ME sending numbers confirmed
- [ ] At minimum 10 sandbox test runs completed with zero template errors
- [ ] Stage 2 activation approved by Will in writing (Slack or email)

**Module changes in Stage 2:**

1. **Insert Module 9a** (after Module 8, before current Slack module):
   - Make module type: Gmail — Send an Email
   - Connection: `hello@shesaidsail.com` (Route A) OR `hello@mareexecutive.com` (Route B)
   - To: `{{2.Email}}`
   - Subject: `{{assembled_email_subject}}`
   - Body: `{{assembled_email_body_html}}`
   - Content type: HTML

2. **Insert Module 9b** (after Module 9a):
   - Make module type: HTTP — Make a Request (to Quo SMS API)
   - OR: Quo SMS native Make module if available
   - To: `{{2.Phone}}`
   - Body (SSS): `"Hi {{client_first_name}}! Your She Said Sail charter on {{charter_date_short}} is confirmed. Check your email for full details. Questions? Reply here. — {{concierge_name}}"`
   - Body (ME): `"{{client_first_name}}, your Mare Executive charter {{booking_id}} on {{charter_date_short}} is confirmed. Full details sent to {{2.Email}}. — {{concierge_name}}"`

3. **Modify Module 8** — add `Confirmation_Sent_At = {{now}}` and change `Confirmation_Status` write value to `SENT`

4. **Modify Module 9 (Slack)** — change message from "ACTION REQUIRED — manual send" to informational "Confirmation automatically sent to client" notification

5. **M-AUDIT-LOGGER payload update** — change `approval_state` from `PENDING_HUMAN` to `AUTONOMOUS`

---

## 12. Open Issues

| Issue ID | Description                                                                                                             | Owner        | Priority | Status |
|----------|-------------------------------------------------------------------------------------------------------------------------|--------------|----------|--------|
| OI-BC-01 | **Gmail OAuth connection must be confirmed for both brands.** `hello@shesaidsail.com` and `hello@mareexecutive.com` must be authenticated in the Make.com workspace before Stage 2. | Will         | CRITICAL | OPEN   |
| OI-BC-02 | **Email templates must be brand-approved by Will** before any client communication goes out. Stage 1 review window is during sandbox testing. | Will         | CRITICAL | OPEN   |
| OI-BC-03 | **Confirm `Confirmation_Email_Draft`, `Confirmation_Email_Subject`, `Confirmation_Status`, `Confirmation_Prepared_At`, `Confirmation_Prepared_By`, `Confirmation_Recipient`, `Confirmation_Phone` fields exist** in Airtable Bookings table. If not, they must be created before this scenario is built. | Systems Arch | HIGH     | OPEN   |
| OI-BC-04 | **Logo image URLs must be confirmed.** Both SSS (`https://shesaidsail.com/logo-light.png`) and ME (`https://mareexecutive.com/logo-light.png`) logo URLs are assumed. Verify actual CDN paths. | Will / Ops  | HIGH     | OPEN   |
| OI-BC-05 | **`Balance_Due_Date` calculation.** Current spec calculates as Charter_Date minus 7 days. Confirm with Will whether this is the correct balance due policy. | Will         | MEDIUM   | OPEN   |
| OI-BC-06 | **Concierge name resolution.** If `Concierge_Assigned` is empty on the Booking, the fallback is the brand team name. Confirm this is acceptable or whether Luciana should always be the default named concierge. | Luciana      | MEDIUM   | OPEN   |
| OI-BC-07 | **Quo SMS integration.** Confirm Quo SMS API credentials and Make.com connection method (native module vs. HTTP) before Stage 2 build begins. | Systems Arch | LOW (Stage 1) | OPEN |
| OI-BC-08 | **ME brand logo and color palette.** The ME template uses `#0d2137` and `#8eb4d4`. Confirm with Will that these match the Mare Executive brand guidelines. | Will         | MEDIUM   | OPEN   |

---

## 13. Final Scenario Status

**Build Status:** `PENDING BUILD`

> This scenario cannot be built until M-BOOKING-CREATION is built and validated, and OI-BC-03 (field existence in Airtable) is confirmed.

**Dependency chain:**
- Requires: M-BOOKING-CREATION (upstream caller) — must be built, tested, and validated first
- Requires: M-AUDIT-LOGGER (sub-scenario) — must be built and tested before this scenario runs
- Enables: Nothing in Stage 1 (final scenario in client communication chain)
- Enables Stage 2: Gmail send + SMS send automation

**Make.com Scenario Registration Checklist:**
- [ ] Scenario created in Make.com workspace
- [ ] Scenario ID recorded in this document
- [ ] All Airtable connections authenticated
- [ ] Slack connection authenticated
- [ ] Error handlers attached to Modules 1, 2, 7, 8
- [ ] Guard checks implemented at Module 1 (Status, Automations_Paused, Confirmation_Status)
- [ ] Scenario linked from M-BOOKING-CREATION (outbound call configured)
- [ ] SSS and ME template variables validated against live Airtable Bookings table field names
- [ ] Will has reviewed both email templates and approved them for sandbox testing
- [ ] Scenario set to Active (after sandbox validation complete)
- [ ] Stage 2 activation checklist pinned in #sss-ops-alerts for reference

---

*Document maintained by Systems Architecture. All field names and table IDs are authoritative as of 2026-05-16. Verify against live Airtable base before build. Templates are subject to brand approval by Will before Stage 1 sandbox testing.*
