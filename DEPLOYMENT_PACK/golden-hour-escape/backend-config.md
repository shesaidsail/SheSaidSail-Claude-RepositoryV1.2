# GOLDEN HOUR ESCAPE — BACKEND CONFIGURATION
Version: 1.0 | Date: May 2026 | Status: READY FOR IMPLEMENTATION

---

## FORM SUBMISSION FLOW

```
User submits form
        |
Webflow form submission fires
        |
Make SSS-LEAD-INTAKE webhook receives payload
        |
Airtable: Idempotency check (LEAD-{email}-{date}-{guests})
        |
    [Duplicate?] -- YES --> Skip creation, return 200
        |
       NO
        |
Airtable: Create Request record in tblTlSB9CO4dTGodg
  - Status: NEW
  - Environment: Production
  - Brand: SSS
  - Experience: Golden Hour Escape
  - All form fields mapped
        |
Gmail: Send branded confirmation email to client
        |
Slack: Post alert to #sss-ops-alerts
        |
Audit Logger: Log action
```

---

## FORM IDENTIFICATION

**Form ID:** `sss-golden-hour-escape-inquiry`
**Experience value:** `Golden Hour Escape`
**Page slug:** `/experience/golden-hour-escape/`

---

## REQUIRED HIDDEN FIELDS

All must be present in the Webflow form and populated by `analytics.js`:

| Field Name | Populated With | Source |
|-----------|----------------|--------|
| `experience` | `Golden Hour Escape` | Static value |
| `source_url` | `window.location.href` | JS |
| `utm_source` | URL param `utm_source` | JS |
| `utm_medium` | URL param `utm_medium` | JS |
| `utm_campaign` | URL param `utm_campaign` | JS |
| `utm_content` | URL param `utm_content` | JS |
| `utm_term` | URL param `utm_term` | JS |
| `page_slug` | `window.location.pathname` | JS |
| `referrer` | `document.referrer` | JS |

---

## AIRTABLE FIELD MAPPING

Webhook payload key --> Airtable Requests field:

| Webhook Key | Airtable Field | Notes |
|-------------|---------------|-------|
| `first_name` | First Name | |
| `last_name` | Last Name | |
| `email` | Email | Used in idempotency key |
| `phone` | Phone | |
| `experience` | Experience | Always "Golden Hour Escape" |
| `preferred_date` | Preferred Date | ISO YYYY-MM-DD |
| `guest_count` | Guest Count | Number |
| `occasion` | Occasion | |
| `city` | City | |
| `add_ons` | Add-Ons Selected | |
| `special_requests` | Special Requests | |
| `source_url` | (used for brand/city routing) | |
| `utm_source` | UTM_Source | |
| `utm_medium` | UTM_Medium | |
| `utm_campaign` | UTM_Campaign | |

**Auto-set by Make (not from form):**
| Field | Value | Set By |
|-------|-------|--------|
| Status | NEW | Make module 5 |
| Environment | Production | Make module 5 |
| Brand | SSS | Make brand routing |
| Source_System | Make | Make module 5 |
| Idempotency_Key | LEAD-{email}-{date}-{guests} | Make module 5 |

---

## MAKE SCENARIO: SSS-LEAD-INTAKE

**Webhook URL:** Configure at make.com -- SSS-LEAD-INTAKE scenario, Module 1 (gateway:CustomWebHook)

**Import file:** `08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/M-LEAD-INTAKE.json`

**Dependencies:**
- SSS-AUDIT-LOGGER must be live
- SSS-SLACK-ALERTS must be live

---

## WEBFLOW FORM CONFIGURATION

1. Navigate to Webflow Designer > Golden Hour Escape page
2. Select the form element
3. Set Form Name: `sss-golden-hour-escape-inquiry`
4. Set Action: (custom webhook URL from Make)
5. Set Method: POST
6. Ensure all field names match the hidden field IDs exactly

**Custom Code -- Before </body> on this page:**
```html
<script src="[CDN_URL]/analytics.js"></script>
```
Or paste the contents of `analytics.js` directly.

---

## CONFIRMATION EMAIL

The branded confirmation email is handled by Make `M-LEAD-INTAKE.json`, Module 6.

The email:
- Uses Gmail OAuth connected to hello@shesaidsail.com
- Subject: "We received your She Said Sail inquiry, [first_name]!"
- Shows: Experience, Preferred Date, Guests, Occasion
- Branded with navy + gold template
- Sign-off: "The She Said Sail Team"

---

## SLACK ALERT

Fires to `#sss-ops-alerts` channel:
```
NEW Lead - She Said Sail
Name: [first] [last]
Experience: Golden Hour Escape
Date: [preferred_date] | Guests: [guest_count]
Occasion: [occasion]
Email: [email] | Phone: [phone]
Source: [source_url]
Record: [airtable_record_id]
```

---

## DUPLICATE LEAD PREVENTION

Idempotency key pattern: `LEAD-{email}-{preferred_date}-{guest_count}`

If a lead already exists with this key, Make skips record creation and returns 200 silently. The confirmation email still fires to avoid a broken user experience.

---

## PRE-LAUNCH CHECKLIST

- [ ] Make SSS-LEAD-INTAKE scenario is active (not paused)
- [ ] Webhook URL is registered in Webflow form action
- [ ] All 9 hidden fields present in Webflow form
- [ ] analytics.js loaded in page footer code
- [ ] Test submission: check Airtable Requests table for new record
- [ ] Test submission: confirm confirmation email received
- [ ] Test submission: confirm Slack alert in #sss-ops-alerts
- [ ] Duplicate test: submit same email+date+guests twice, confirm one record
