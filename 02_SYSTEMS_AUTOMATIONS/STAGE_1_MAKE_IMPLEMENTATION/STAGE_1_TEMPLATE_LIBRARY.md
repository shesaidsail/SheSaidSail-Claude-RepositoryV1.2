# STAGE 1 TEMPLATE LIBRARY
**Project:** She Said Sail + Mare Executive — Make.com Automation System  
**Base:** appdZ49WqgjRXxA1R  
**Prepared by:** Production Reliability Engineering  
**Date:** 2026-05-16  
**Scope:** All message templates for Stage 1 scenarios (Slack, Email, SMS, Error, Audit)  
**Status:** DRAFT — requires brand review by Will and Luciana before activation

---

## Template Index

| Template ID | Type | Scenario | Brand | Channel/Recipient |
|-------------|------|----------|-------|-------------------|
| TPL-SLACK-001 | Slack Block Kit | M-SLACK-ALERTS | Both | #sss-ops-alerts |
| TPL-SLACK-002 | Slack Block Kit | M-CONCIERGE-ASSIGNMENT | Both | #sss-ops-alerts |
| TPL-SLACK-003 | Slack Block Kit | M-STRIPE-DEPOSIT | Both | #sss-ops-alerts |
| TPL-SLACK-004 | Slack Block Kit | M-BOOKING-CREATION | Both | #sss-ops-alerts |
| TPL-EMAIL-001 | HTML Email | M-BOOKING-CONFIRMATION | SSS | Client (TEST MODE) |
| TPL-EMAIL-002 | HTML Email | M-BOOKING-CONFIRMATION | ME | Client (TEST MODE) |
| TPL-SMS-001 | SMS 160-char | M-STRIPE-DEPOSIT | SSS | Client phone (TEST) |
| TPL-SMS-002 | SMS 160-char | M-STRIPE-DEPOSIT | ME | Client phone (TEST) |
| TPL-ERR-001 | Slack Block Kit | Error handler | Both | #sss-emergency-ops |
| TPL-AUDIT-001 | JSON | M-AUDIT-LOGGER | Both | Audit_Log table |

---

## Variable Reference

All variables use Make.com double-brace syntax `{{variable_name}}`. Variables are set in the Make scenario data flow before the template module executes.

| Variable | Source | Type | Notes |
|----------|--------|------|-------|
| `{{lead_name}}` | Requests.Client_Name | String | Full name |
| `{{brand}}` | Requests.Brand | String | "She Said Sail" or "Mare Executive" |
| `{{city}}` | Requests.City | String | Departure city |
| `{{inquiry_type}}` | Requests.Inquiry_Type | String | Charter type |
| `{{request_id}}` | Requests.Record_ID | String | Airtable record ID |
| `{{received_at}}` | Requests.Created_Time | DateTime | ISO 8601 |
| `{{assigned_to}}` | Concierge.Name | String | Concierge full name |
| `{{client_name}}` | Clients.Full_Name | String | |
| `{{client_first_name}}` | Clients.First_Name | String | |
| `{{amount}}` | Bookings.Deposit_Amount | Currency | Formatted with currency symbol |
| `{{stripe_link}}` | Stripe.Payment_Link_URL | URL | |
| `{{booking_id}}` | Bookings.Record_ID | String | |
| `{{charter_date}}` | Bookings.Charter_Date | Date | Formatted: "Saturday, June 14 2026" |
| `{{package}}` | Packages.Package_Name | String | |
| `{{vessel_name}}` | Bookings.Vessel_Name | String | |
| `{{package_name}}` | Packages.Package_Name | String | |
| `{{deposit_amount}}` | Bookings.Deposit_Amount | Currency | |
| `{{group_size}}` | Bookings.Group_Size | Number | |
| `{{booking_link}}` | Airtable interface URL | URL | Client-facing booking portal |
| `{{scenario_name}}` | Make scenario metadata | String | e.g., "M-BRAND-ROUTER" |
| `{{error_code}}` | Make error object | String | |
| `{{error_message}}` | Make error object | String | |
| `{{timestamp}}` | Make now() | DateTime | ISO 8601 |
| `{{affected_record_id}}` | Bundle data | String | Airtable record ID |

---

## TPL-SLACK-001 — New Lead Received Alert

**Scenario:** M-SLACK-ALERTS  
**Channel:** #sss-ops-alerts  
**Trigger:** New record created in Requests table  
**Purpose:** Notify ops team of incoming lead within 60 seconds of submission

### Slack Block Kit JSON Payload

```json
{
  "channel": "#sss-ops-alerts",
  "username": "She Said Sail Bot",
  "icon_emoji": ":sailboat:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🆕 New Lead — {{brand}}",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Client:*\n{{lead_name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Brand:*\n{{brand}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Location:*\n{{city}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Inquiry Type:*\n{{inquiry_type}}"
        }
      ]
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Request ID:*\n`{{request_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Received:*\n{{received_at}}"
        }
      ]
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
            "emoji": false
          },
          "style": "primary",
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/{{request_id}}"
        },
        {
          "type": "button",
          "text": {
            "type": "plain_text",
            "text": "Assign Concierge",
            "emoji": false
          },
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/{{request_id}}"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Automated by Make.com · M-SLACK-ALERTS · Environment: {{environment}}"
        }
      ]
    }
  ]
}
```

### Make Module Configuration
- Module: Slack — Create a Message (Block Kit)
- Connection: `SSS_SLACK_BOT`
- Channel: `#sss-ops-alerts` (hardcoded — bot must be invited to channel)
- Parse: `full`
- Fallback text (for notifications): `New lead received from {{lead_name}} — {{brand}}`

---

## TPL-SLACK-002 — Concierge Assignment Notification

**Scenario:** M-CONCIERGE-ASSIGNMENT  
**Channel:** #sss-ops-alerts  
**Trigger:** Concierge assignment written to Requests record  
**Purpose:** Confirm to ops team that a request has been picked up by a concierge

### Slack Block Kit JSON Payload

```json
{
  "channel": "#sss-ops-alerts",
  "username": "She Said Sail Bot",
  "icon_emoji": ":person_in_tuxedo:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "✅ Concierge Assigned — {{brand}}",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Request ID:*\n`{{request_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Assigned To:*\n{{assigned_to}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Client:*\n{{client_name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Brand:*\n{{brand}}"
        }
      ]
    },
    {
      "type": "divider"
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Automated by Make.com · M-CONCIERGE-ASSIGNMENT · Environment: {{environment}}"
        }
      ]
    }
  ]
}
```

### Make Module Configuration
- Module: Slack — Create a Message (Block Kit)
- Connection: `SSS_SLACK_BOT`
- Channel: `#sss-ops-alerts`
- Fallback text: `{{assigned_to}} assigned to request {{request_id}} ({{client_name}})`

---

## TPL-SLACK-003 — Deposit Link Sent Alert

**Scenario:** M-STRIPE-DEPOSIT  
**Channel:** #sss-ops-alerts  
**Trigger:** Stripe payment link generated and sent to client  
**Note:** TEST MODE — no actual client payment link is sent during Stage 1

### Slack Block Kit JSON Payload

```json
{
  "channel": "#sss-ops-alerts",
  "username": "She Said Sail Bot",
  "icon_emoji": ":credit_card:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "💳 Deposit Link Sent — {{brand}}",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Request ID:*\n`{{request_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Client:*\n{{client_name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Deposit Amount:*\n{{amount}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Brand:*\n{{brand}}"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Stripe Payment Link:*\n<{{stripe_link}}|Click to view in Stripe Dashboard>"
      }
    },
    {
      "type": "divider"
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": ":warning: TEST MODE — No real charge. Automated by Make.com · M-STRIPE-DEPOSIT · Environment: {{environment}}"
        }
      ]
    }
  ]
}
```

---

## TPL-SLACK-004 — Booking Created Alert

**Scenario:** M-BOOKING-CREATION  
**Channel:** #sss-ops-alerts  
**Trigger:** New Booking record created in Airtable

### Slack Block Kit JSON Payload

```json
{
  "channel": "#sss-ops-alerts",
  "username": "She Said Sail Bot",
  "icon_emoji": ":anchor:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "⚓ Booking Created",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Booking ID:*\n`{{booking_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Client:*\n{{client_name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Charter Date:*\n{{charter_date}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Package:*\n{{package}}"
        }
      ]
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Total Amount:*\n{{amount}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Group Size:*\n{{group_size}}"
        }
      ]
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
            "text": "View Booking in Airtable"
          },
          "style": "primary",
          "url": "https://airtable.com/appdZ49WqgjRXxA1R/{{booking_id}}"
        }
      ]
    },
    {
      "type": "context",
      "elements": [
        {
          "type": "mrkdwn",
          "text": "Automated by Make.com · M-BOOKING-CREATION · Environment: {{environment}}"
        }
      ]
    }
  ]
}
```

---

## TPL-EMAIL-001 — Booking Confirmation (She Said Sail)

**Scenario:** M-BOOKING-CONFIRMATION  
**Brand:** She Said Sail  
**From:** hello@shesaidsail.com  
**Reply-To:** hello@shesaidsail.com  
**Subject:** `Your She Said Sail Charter is Confirmed — {{charter_date}}`  
**Note:** TEST MODE ONLY during Stage 1. Send to test address only, never to `{{client_email}}`.

### HTML Email Body

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Charter is Confirmed</title>
  <style>
    body { font-family: Georgia, 'Times New Roman', serif; background-color: #f4f1ec; margin: 0; padding: 0; }
    .container { max-width: 600px; margin: 40px auto; background-color: #ffffff; border-radius: 4px; overflow: hidden; }
    .header { background-color: #1a2744; padding: 40px 40px 30px; text-align: center; }
    .header h1 { color: #c9a96e; font-size: 28px; margin: 0; letter-spacing: 2px; font-weight: normal; }
    .header p { color: #9ab0c4; font-size: 13px; margin: 8px 0 0; letter-spacing: 3px; text-transform: uppercase; }
    .body { padding: 40px; }
    .greeting { font-size: 18px; color: #1a2744; margin-bottom: 20px; }
    .details-box { background-color: #f4f1ec; border-left: 3px solid #c9a96e; padding: 20px 24px; margin: 28px 0; border-radius: 2px; }
    .details-box h3 { color: #1a2744; font-size: 13px; text-transform: uppercase; letter-spacing: 2px; margin: 0 0 16px; }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 10px; font-size: 15px; }
    .detail-label { color: #6b7280; }
    .detail-value { color: #1a2744; font-weight: bold; text-align: right; }
    .cta-button { display: block; width: fit-content; margin: 32px auto; background-color: #1a2744; color: #c9a96e; text-decoration: none; padding: 14px 36px; border-radius: 2px; font-size: 14px; letter-spacing: 2px; text-transform: uppercase; }
    .body-text { color: #374151; font-size: 15px; line-height: 1.7; margin-bottom: 16px; }
    .footer { background-color: #f4f1ec; padding: 24px 40px; text-align: center; }
    .footer p { color: #9ca3af; font-size: 12px; margin: 4px 0; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>SHE SAID SAIL</h1>
      <p>Luxury Sailing Charters</p>
    </div>
    <div class="body">
      <p class="greeting">Dear {{client_first_name}},</p>
      <p class="body-text">
        Your charter with She Said Sail is confirmed. We are delighted to welcome you aboard and are 
        committed to creating an exceptional experience tailored to you and your guests.
      </p>
      <div class="details-box">
        <h3>Your Booking Details</h3>
        <div class="detail-row">
          <span class="detail-label">Booking Reference</span>
          <span class="detail-value">{{booking_id}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Charter Date</span>
          <span class="detail-value">{{charter_date}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Vessel</span>
          <span class="detail-value">{{vessel_name}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Package</span>
          <span class="detail-value">{{package_name}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Group Size</span>
          <span class="detail-value">{{group_size}} guests</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Deposit Paid</span>
          <span class="detail-value">{{deposit_amount}}</span>
        </div>
      </div>
      <p class="body-text">
        Your dedicated concierge will be in touch within 24 hours to coordinate the finer details 
        of your experience — provisions, special requests, and embarkation logistics.
      </p>
      <a href="{{booking_link}}" class="cta-button">View Your Booking</a>
      <p class="body-text">
        If you have any questions before then, please reply to this email or contact us directly 
        at <a href="mailto:hello@shesaidsail.com" style="color:#1a2744;">hello@shesaidsail.com</a>.
      </p>
      <p class="body-text">We look forward to welcoming you aboard.</p>
      <p class="body-text" style="margin-top:32px;">
        With warmth,<br>
        <strong>The She Said Sail Team</strong>
      </p>
    </div>
    <div class="footer">
      <p>She Said Sail · Luxury Sailing Charters</p>
      <p>hello@shesaidsail.com · shesaidsail.com</p>
      <p style="margin-top:12px;font-size:11px;">This booking confirmation was sent automatically. Booking ID: {{booking_id}}</p>
    </div>
  </div>
</body>
</html>
```

### Make Module Configuration (TEST MODE)
- Module: Gmail — Send an Email
- Connection: `SSS_GMAIL_HELLO`
- To: `will@shesaidsail.com` (TEST MODE — hardcoded, NOT `{{client_email}}`)
- Subject: `[TEST] Your She Said Sail Charter is Confirmed — {{charter_date}}`
- Content type: HTML
- Body: above template with all variables mapped from Make data bundle

---

## TPL-EMAIL-002 — Booking Confirmation (Mare Executive)

**Scenario:** M-BOOKING-CONFIRMATION  
**Brand:** Mare Executive  
**From:** hello@mareexecutive.com  
**Reply-To:** hello@mareexecutive.com  
**Subject:** `Mare Executive Charter Confirmation — {{booking_id}}`  
**Note:** TEST MODE ONLY during Stage 1.

### HTML Email Body

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Charter Confirmation — Mare Executive</title>
  <style>
    body { font-family: 'Helvetica Neue', Arial, sans-serif; background-color: #f0f0f0; margin: 0; padding: 0; }
    .container { max-width: 600px; margin: 40px auto; background-color: #ffffff; }
    .header { background-color: #0a0a0a; padding: 36px 40px; }
    .header h1 { color: #ffffff; font-size: 22px; margin: 0; letter-spacing: 4px; font-weight: 300; }
    .header p { color: #888888; font-size: 11px; margin: 6px 0 0; letter-spacing: 4px; text-transform: uppercase; }
    .accent-bar { height: 3px; background: linear-gradient(90deg, #b8960c, #f0d060, #b8960c); }
    .body { padding: 40px; }
    .greeting { font-size: 17px; color: #0a0a0a; margin-bottom: 20px; font-weight: 300; }
    .details-box { border: 1px solid #e5e5e5; padding: 24px; margin: 28px 0; }
    .details-box h3 { color: #0a0a0a; font-size: 11px; text-transform: uppercase; letter-spacing: 3px; margin: 0 0 20px; font-weight: 400; border-bottom: 1px solid #e5e5e5; padding-bottom: 12px; }
    .detail-row { display: flex; justify-content: space-between; margin-bottom: 12px; font-size: 14px; }
    .detail-label { color: #888888; font-weight: 300; }
    .detail-value { color: #0a0a0a; font-weight: 500; }
    .cta-button { display: block; width: fit-content; margin: 32px auto; background-color: #0a0a0a; color: #ffffff; text-decoration: none; padding: 14px 40px; font-size: 12px; letter-spacing: 3px; text-transform: uppercase; }
    .body-text { color: #555555; font-size: 14px; line-height: 1.8; margin-bottom: 16px; font-weight: 300; }
    .footer { background-color: #0a0a0a; padding: 24px 40px; text-align: center; }
    .footer p { color: #666666; font-size: 11px; margin: 4px 0; letter-spacing: 1px; }
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <h1>MARE EXECUTIVE</h1>
      <p>Corporate &amp; Executive Charters</p>
    </div>
    <div class="accent-bar"></div>
    <div class="body">
      <p class="greeting">Dear {{client_first_name}},</p>
      <p class="body-text">
        We are pleased to confirm your executive charter with Mare Executive. 
        Your booking has been processed and your dedicated account manager will 
        contact you within the next 24 hours to finalise all arrangements.
      </p>
      <div class="details-box">
        <h3>Booking Confirmation</h3>
        <div class="detail-row">
          <span class="detail-label">Reference Number</span>
          <span class="detail-value">{{booking_id}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Charter Date</span>
          <span class="detail-value">{{charter_date}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Vessel</span>
          <span class="detail-value">{{vessel_name}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Package</span>
          <span class="detail-value">{{package_name}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Guest Count</span>
          <span class="detail-value">{{group_size}}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">Deposit Received</span>
          <span class="detail-value">{{deposit_amount}}</span>
        </div>
      </div>
      <p class="body-text">
        All charter documentation, itinerary details, and pre-departure information 
        will be provided by your account manager. Please retain your reference number 
        for all correspondence.
      </p>
      <a href="{{booking_link}}" class="cta-button">Access Booking Portal</a>
      <p class="body-text">
        For immediate assistance: <a href="mailto:hello@mareexecutive.com" style="color:#0a0a0a;">hello@mareexecutive.com</a>
      </p>
      <p class="body-text" style="margin-top:32px;">
        Yours sincerely,<br>
        <strong>Mare Executive</strong>
      </p>
    </div>
    <div class="footer">
      <p>MARE EXECUTIVE · Corporate &amp; Executive Charters</p>
      <p>hello@mareexecutive.com · mareexecutive.com</p>
      <p style="margin-top:10px;">Ref: {{booking_id}}</p>
    </div>
  </div>
</body>
</html>
```

### Make Module Configuration (TEST MODE)
- Module: Gmail — Send an Email
- Connection: `ME_GMAIL_HELLO`
- To: `will@shesaidsail.com` (TEST MODE — hardcoded)
- Subject: `[TEST] Mare Executive Charter Confirmation — {{booking_id}}`
- Content type: HTML

---

## TPL-SMS-001 — Deposit Request SMS (She Said Sail)

**Scenario:** M-STRIPE-DEPOSIT  
**Brand:** She Said Sail  
**Sender:** SSS short code / long code via Quo SMS  
**Note:** TEST MODE — send to Will's phone only, not client phone  
**Character limit:** 160 characters (single SMS segment)

### SMS Body

```
She Said Sail: Hi {{client_first_name}}, your deposit of {{amount}} is ready. 
Secure your charter here: {{stripe_link}} Questions? hello@shesaidsail.com
```

**Character count check** (with typical variable lengths):  
Base text without variables: ~110 chars. With variables (first name ~8, amount ~6, link ~35): ~159 chars.  
If `{{stripe_link}}` exceeds 30 chars, use a URL shortener in Make before injecting.

### Quo SMS Make Module Configuration (TEST MODE)
- Module: HTTP — Make a Request (Quo SMS REST API)
- To: `{{WILL_TEST_PHONE}}` (Make environment variable — NOT `{{client_phone}}`)
- Body: Above template with variables
- Method: POST
- URL: `https://api.quosms.com/v1/messages` (confirm current API endpoint)

---

## TPL-SMS-002 — Deposit Request SMS (Mare Executive)

**Scenario:** M-STRIPE-DEPOSIT  
**Brand:** Mare Executive  
**Character limit:** 160 characters

### SMS Body

```
Mare Executive: {{client_first_name}}, your charter deposit of {{amount}} is due. 
Complete payment: {{stripe_link}} Queries: hello@mareexecutive.com
```

**Character count check:**  
Base text ~110 chars. With variables: ~155 chars. Within limit.

---

## TPL-ERR-001 — Automation Failure Error Alert

**Scenario:** Error handler (all scenarios)  
**Channel:** #sss-emergency-ops  
**Purpose:** Alert ops team to scenario failures in real time

Four severity levels with distinct formatting:

### Level 1 — WARNING (non-blocking, scenario continues)

```json
{
  "channel": "#sss-emergency-ops",
  "username": "She Said Sail Bot",
  "icon_emoji": ":warning:",
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":warning: *WARNING* · {{scenario_name}}\n*Error:* `{{error_code}}` — {{error_message}}\n*Record:* `{{affected_record_id}}` · *Time:* {{timestamp}}\n_Scenario continued. Monitor for recurrence._"
      }
    }
  ]
}
```

### Level 2 — ERROR (scenario halted, requires investigation)

```json
{
  "channel": "#sss-emergency-ops",
  "username": "She Said Sail Bot",
  "icon_emoji": ":red_circle:",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🔴 ERROR — Scenario Halted",
        "emoji": true
      }
    },
    {
      "type": "section",
      "fields": [
        {
          "type": "mrkdwn",
          "text": "*Scenario:*\n{{scenario_name}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Error Code:*\n`{{error_code}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Message:*\n{{error_message}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Affected Record:*\n`{{affected_record_id}}`"
        },
        {
          "type": "mrkdwn",
          "text": "*Timestamp:*\n{{timestamp}}"
        },
        {
          "type": "mrkdwn",
          "text": "*Environment:*\n{{environment}}"
        }
      ]
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": ":point_right: *Action Required:* Investigate Make.com execution log and Airtable record. Scenario has halted — no further actions will be taken on this bundle."
      }
    }
  ]
}
```

### Level 3 — CRITICAL (data integrity at risk, immediate intervention required)

```json
{
  "channel": "#sss-emergency-ops",
  "username": "She Said Sail Bot",
  "icon_emoji": ":rotating_light:",
  "text": "<!channel> CRITICAL AUTOMATION FAILURE — IMMEDIATE ACTION REQUIRED",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "🚨 CRITICAL — Data Integrity Risk",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<!channel> *CRITICAL failure in {{scenario_name}}*\n\n*Error:* `{{error_code}}`\n*Detail:* {{error_message}}\n*Record at risk:* `{{affected_record_id}}`\n*Time:* {{timestamp}}"
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "*Immediate steps:*\n1. Set `Automations_Paused = true` in Airtable Automation_Health\n2. Check Airtable record `{{affected_record_id}}` for data corruption\n3. Review Make.com execution log for {{scenario_name}}\n4. Contact Make builder if scenario is looping"
      }
    }
  ]
}
```

### Level 4 — FATAL (system offline, all scenarios affected)

```json
{
  "channel": "#sss-emergency-ops",
  "username": "She Said Sail Bot",
  "icon_emoji": ":skull:",
  "text": "<!channel> FATAL: AUTOMATION SYSTEM OFFLINE",
  "blocks": [
    {
      "type": "header",
      "text": {
        "type": "plain_text",
        "text": "☠️ FATAL — Automation System Offline",
        "emoji": true
      }
    },
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": "<!channel> *All Make.com automations may be affected.*\n\n*Last known scenario:* {{scenario_name}}\n*Error:* `{{error_code}}`\n*Time:* {{timestamp}}\n\n*Emergency actions:*\n1. Set `Automations_Paused = true` in Airtable immediately\n2. Deactivate all active Make scenarios manually\n3. Post status in #sss-ops-alerts\n4. Contact Will and Luciana directly"
      }
    }
  ]
}
```

---

## TPL-AUDIT-001 — Audit Log Entry JSON Structure

**Scenario:** M-AUDIT-LOGGER  
**Table:** Audit_Log (base: appdZ49WqgjRXxA1R)  
**Purpose:** Immutable event record for every significant automation action  
**Write mode:** APPEND ONLY — never update existing Audit_Log records

### JSON Structure (Make "Create Record" field mapping)

```json
{
  "Event_ID": "{{sha256(concat(scenario_name, record_id, timestamp))}}",
  "Event_Type": "{{event_type}}",
  "Event_Status": "{{event_status}}",
  "Scenario_Name": "{{scenario_name}}",
  "Scenario_Version": "{{scenario_version}}",
  "Make_Execution_ID": "{{make_execution_id}}",
  "Triggered_By": "{{triggered_by}}",
  "Affected_Table": "{{affected_table}}",
  "Affected_Record_ID": "{{affected_record_id}}",
  "Brand": "{{brand}}",
  "Environment": "{{environment}}",
  "Action_Taken": "{{action_taken}}",
  "Fields_Modified": "{{json_stringify(fields_modified_array)}}",
  "Previous_Values": "{{json_stringify(previous_values_object)}}",
  "New_Values": "{{json_stringify(new_values_object)}}",
  "Error_Code": "{{error_code}}",
  "Error_Message": "{{error_message}}",
  "Client_ID": "{{client_id}}",
  "Request_ID": "{{request_id}}",
  "Booking_ID": "{{booking_id}}",
  "Duration_MS": "{{execution_duration_ms}}",
  "Timestamp": "{{now()}}",
  "Notes": "{{notes}}"
}
```

### Event_Type Enum Values
| Value | Description |
|-------|-------------|
| `LEAD_RECEIVED` | New request record created |
| `BRAND_ROUTED` | Brand routing decision made |
| `CONCIERGE_ASSIGNED` | Concierge assigned to request |
| `DEPOSIT_LINK_CREATED` | Stripe payment link generated |
| `DEPOSIT_RECEIVED` | Stripe payment confirmed |
| `BOOKING_CREATED` | Booking record created |
| `CONFIRMATION_SENT` | Booking confirmation email sent |
| `DUPLICATE_PREVENTED` | Idempotency check blocked duplicate |
| `AUTOMATION_PAUSED_CHECK` | Automations_Paused check executed |
| `ERROR_OCCURRED` | Any scenario error |
| `SCENARIO_STARTED` | Scenario execution began |
| `SCENARIO_COMPLETED` | Scenario execution completed successfully |

### Event_Status Enum Values
| Value | Description |
|-------|-------------|
| `SUCCESS` | Action completed without errors |
| `FAILURE` | Action failed; see Error_Code |
| `SKIPPED` | Action skipped (e.g., paused check) |
| `PARTIAL` | Partial success with warnings |

### Make Module Configuration
- Module: Airtable — Create a Record
- Connection: `SSS_AIRTABLE_PAT`
- Base: `appdZ49WqgjRXxA1R`
- Table: `Audit_Log`
- All fields mapped from Make variables per the JSON structure above
- On error: do NOT retry Audit_Log write (avoid duplicate audit entries); instead alert Slack #sss-emergency-ops

---

*Template Library last updated: 2026-05-16. All templates require brand review before production activation.*  
*During Stage 1 testing: email/SMS templates send to test addresses only. Slack templates are safe to use in staging.*
