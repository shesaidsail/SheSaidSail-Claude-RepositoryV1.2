# She Said Sail: Make.com Webhook Specification
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

---

## OVERVIEW

Make.com is the automation layer between the WordPress form and Airtable.
This document specifies every scenario, module, and data mapping needed.

Base URL pattern for Make.com webhooks: `https://hook.us1.make.com/YOUR_WEBHOOK_ID`
Replace YOUR_WEBHOOK_ID with the actual ID from each scenario's webhook trigger.

---

## SCENARIO INDEX

| Scenario ID | Name | Trigger | Purpose |
|---|---|---|---|
| M-WEBFORM-001 | REQUEST-CAPTURE | Webhook POST | Captures and stores request form submissions |
| M-UTM-001 | UTM-CAPTURE | Sub-scenario called by M-WEBFORM-001 | Stores raw UTM data per submission |
| M-ROUTER-001 | BRAND-ROUTER | Sub-scenario called by M-WEBFORM-001 | Routes by brand for multi-brand future expansion |
| M-CONCIERGE-001 | CONCIERGE-ASSIGNMENT | Sub-scenario called by M-WEBFORM-001 | Assigns hot leads to team member |
| M-EMAIL-001 | INQUIRY-CONFIRMATION | Sub-scenario called by M-WEBFORM-001 | Sends confirmation email to guest |
| M-SLACK-001 | SLACK-NEW-LEAD-ALERT | Sub-scenario called by M-WEBFORM-001 | Posts new lead alert to Slack |
| M-AUDIT-001 | AIRTABLE-AUDIT-LOGGER | Called after every Airtable write | Writes action to Audit Log table |

---

## M-WEBFORM-001: REQUEST-CAPTURE

**Trigger:** Custom Webhook (POST)
**Webhook URL:** Provided by Make.com after scenario creation. Paste this into the form's fetch() call.

### Module Sequence

1. **Webhook: Watch incoming data**
   - Method: POST
   - Expected content type: application/json

2. **Airtable: Search records (Contacts table)**
   - Search by field: Email
   - Value: `{{1.email}}`
   - Purpose: Check if contact already exists

3. **Router: Contact exists?**

   **Path A: Contact exists (record found)**
   - Airtable: Update record (Contacts table)
     - Last Contacted: now
   - Continue to Step 5

   **Path B: New contact (no record found)**
   - Airtable: Create record (Contacts table)
     - Full Name: `{{1.full_name}}`
     - Email: `{{1.email}}`
     - Phone: `{{1.phone}}`
     - Type: Lead
     - Source: Web Form
     - Email Subscribed: false
     - Created At: now
   - Continue to Step 5

4. (Both paths merge) Set variable: `contact_id` = ID of the Contact record

5. **Airtable: Create record (Requests table)**
   - Status: New
   - Name: `{{1.full_name}}`
   - Email: `{{1.email}}`
   - Phone: `{{1.phone}}`
   - Occasion: `{{1.occasion}}`
   - Group Size: `{{1.group_size}}`
   - Preferred Date: `{{1.preferred_date}}`
   - Flexible Dates: `{{1.flexible_dates}}`
   - Notes: `{{1.message}}`
   - Experience Interest: `{{1.experience_interest}}`
   - Submitted At: now
   - UTM Source: `{{1.utm_source}}`
   - UTM Medium: `{{1.utm_medium}}`
   - UTM Campaign: `{{1.utm_campaign}}`
   - UTM Content: `{{1.utm_content}}`
   - UTM Term: `{{1.utm_term}}`
   - Creative ID: `{{1.creative_id}}`
   - Landing Page: `{{1.landing_page}}`
   - Referrer URL: `{{1.referrer_url}}`
   - First Seen At: `{{1.first_seen_at}}`
   - Linked Contact: `{{contact_id}}`

6. Set variable: `request_id` = ID of the new Request record

7. **Call M-UTM-001** (UTM-CAPTURE sub-scenario)
   - Pass: all UTM fields + request_id

8. **Call M-EMAIL-001** (INQUIRY-CONFIRMATION)
   - Pass: full_name, email, occasion, group_size, request_id

9. **Call M-SLACK-001** (SLACK-NEW-LEAD-ALERT)
   - Pass: full_name, email, occasion, utm_source, utm_campaign, request_id

10. **Call M-AUDIT-001** (AIRTABLE-AUDIT-LOGGER)
    - Event Type: FORM_SUBMITTED
    - Linked Record Type: Request
    - Linked Record ID: `{{request_id}}`
    - Triggered By: M-WEBFORM-001

---

## M-UTM-001: UTM-CAPTURE

**Trigger:** Called as sub-scenario from M-WEBFORM-001

### Purpose

Creates a dedicated UTM record in the UTMs table for every form submission.
Provides clean attribution data without polluting the Requests table.

### Module Sequence

1. **Airtable: Create record (UTMs table)**
   - Linked Request: `{{request_id}}`
   - utm_source: `{{utm_source}}`
   - utm_medium: `{{utm_medium}}`
   - utm_campaign: `{{utm_campaign}}`
   - utm_content: `{{utm_content}}`
   - utm_term: `{{utm_term}}`
   - creative_id: `{{creative_id}}`
   - landing_page: `{{landing_page}}`
   - referrer_url: `{{referrer_url}}`
   - source_url: `{{source_url}}`
   - first_seen_at: `{{first_seen_at}}`
   - submission_at: now
   - brand: `{{brand}}`
   - service_category: `{{service_category}}`

2. **Call M-AUDIT-001**
   - Event Type: UTM_RECORD_CREATED
   - Linked Record Type: Request
   - Linked Record ID: `{{request_id}}`

---

## M-ROUTER-001: BRAND-ROUTER

**Trigger:** Called as sub-scenario from M-WEBFORM-001

### Purpose

Routes submissions to the correct team or workflow based on brand field.
Currently She Said Sail only, but designed to support future brand additions.

### Module Sequence

1. **Router: Check brand field**

   **Path A: brand = "shesaidsail"**
   - Set destination: Will (founder) + concierge workflow
   - Continue to M-CONCIERGE-001

   **Path B: brand = other** (future use)
   - Set destination: appropriate team
   - Log unrouted brand to Audit Log

---

## M-CONCIERGE-001: CONCIERGE-ASSIGNMENT

**Trigger:** Called from M-ROUTER-001

### Purpose

Assigns hot leads based on occasion type. Flags urgent or high-value requests.

### Assignment Logic

| Condition | Action |
|---|---|
| Occasion = Bachelorette | Tag Internal Rating as Hot |
| Occasion = Birthday AND Group Size >= 10 | Tag Internal Rating as Hot |
| Group Size >= 15 | Tag Internal Rating as Hot |
| All other submissions | Tag Internal Rating as Warm |

### Module Sequence

1. **Router: Evaluate assignment conditions** (see table above)

2. **Airtable: Update record (Requests table)**
   - Internal Rating: based on routing result
   - Assigned To: Will (founder record ID in Contacts)

3. If Internal Rating is Hot:
   - Set Follow Up Date: today + 1 hour (or same business day)

---

## M-EMAIL-001: INQUIRY-CONFIRMATION-EMAIL

**Trigger:** Called from M-WEBFORM-001 after Request record is created

### Purpose

Sends a warm, on-brand confirmation email to the person who submitted the form.

### Email Specification

**From:** hello@shesaidsail.com
**Reply-To:** hello@shesaidsail.com
**Subject:** We have your request, `{{first_name}}`.

**Body (plain text version):**

```
Hi {{first_name}},

We received your request and we are reviewing it now.

You mentioned: {{occasion}}, {{group_size}} guests.

We will be in touch within 24 hours to talk through the details
and find the right experience for your group.

In the meantime, you can explore our experiences at shesaidsail.com/experiences/

Talk soon,
Will
She Said Sail
```

**HTML version:** Use the brand email template (navy header, Cormorant Garamond heading, Inter body, gold CTA). Match the website visual identity.

**Platform:** Send via Klaviyo transactional email or SendGrid.

### Module Sequence

1. **Email: Send email** (Klaviyo or SendGrid module)
   - To: `{{email}}`
   - Subject: see above
   - Variables: first_name (derived from full_name), occasion, group_size

2. **Call M-AUDIT-001**
   - Event Type: CONFIRMATION_EMAIL_SENT
   - Linked Record Type: Request
   - Linked Record ID: `{{request_id}}`

---

## M-SLACK-001: SLACK-NEW-LEAD-ALERT

**Trigger:** Called from M-WEBFORM-001

### Purpose

Posts a Slack notification to the #new-leads channel when a form is submitted.
Allows Will to respond fast without checking Airtable constantly.

### Slack Message Format

```
*New Request: {{occasion}} for {{group_size}} guests*

Name: {{full_name}}
Email: {{email}}
Phone: {{phone}}
Occasion: {{occasion}}
Group Size: {{group_size}} guests
Date: {{preferred_date}} (flexible: {{flexible_dates}})
Experience: {{experience_interest}}

Source: {{utm_source}} / {{utm_campaign}}
Creative: {{creative_id}}
Landing: {{landing_page}}

Message: {{message}}

Airtable: https://airtable.com/YOUR_BASE/Requests/{{request_id}}
```

### Module Sequence

1. **Slack: Create a message**
   - Channel: #new-leads
   - Message: formatted block above
   - If Internal Rating (from M-CONCIERGE-001) = Hot: add emoji prefix or @channel mention

---

## M-AUDIT-001: AIRTABLE-AUDIT-LOGGER

**Trigger:** Called after every significant Airtable write operation

### Purpose

Records every system action to the Audit Log table. Enables debugging, compliance, and support queries.

### Module Sequence

1. **Airtable: Create record (Audit Log table)**
   - Event Type: `{{event_type}}`
   - Linked Record Type: `{{linked_record_type}}`
   - Linked Record ID: `{{linked_record_id}}`
   - Triggered By: `{{triggered_by}}`
   - Payload: JSON.stringify of key fields (sanitized: no PII in payload)
   - Status: Success (or Error if called from error handler)
   - Timestamp: now

---

## EMAIL CAPTURE SCENARIO (HOMEPAGE)

A separate, lighter webhook for the email capture section on the homepage.

**Scenario: M-EMAIL-CAPTURE-001**

### Module Sequence

1. **Webhook: Watch incoming data**
   - Expected fields: email, utm_source, utm_medium, utm_campaign, landing_page, first_seen_at, brand

2. **Airtable: Search records (Contacts table)**
   - Search by: Email = `{{1.email}}`

3. **Router: Contact exists?**

   **Path A: Exists**
   - Update Email Subscribed = true
   - Update Email Subscribed At = now (if not already set)

   **Path B: New**
   - Create Contact: Email, Source = Web Form, Email Subscribed = true, Email Subscribed At = now

4. **Email platform: Add/update subscriber**
   - Platform: Klaviyo or Mailchimp
   - List: Homepage Nurture
   - Tag: homepage-capture

5. **Call M-AUDIT-001**
   - Event Type: EMAIL_CAPTURE
   - Linked Record Type: Contact

---

## WEBHOOK ENDPOINT CONFIGURATION

After creating each scenario in Make.com:

1. Copy the webhook URL from the scenario's webhook trigger module
2. For the request form: paste into the fetch() call in luxury-enhancements.js
   ```javascript
   fetch('https://hook.us1.make.com/YOUR_REQUEST_WEBHOOK_ID', {
     method: 'POST',
     headers: { 'Content-Type': 'application/json' },
     body: JSON.stringify(payload)
   })
   ```
3. For the email capture form: paste into the fetch() call in the email capture section's JS
4. Activate each scenario in Make.com before going live
5. Test with a real submission and verify Airtable records created correctly

---

## ERROR HANDLING

Make.com should be configured with these error handlers:

- **Webhook timeout:** If WordPress form POST receives no 200 response within 5 seconds, show user a generic "We received your request" message regardless. Never show a technical error to the user.
- **Airtable write failure:** Log to Audit Log with Status = Error. Do not prevent confirmation email from sending.
- **Email send failure:** Log to Audit Log with Status = Error. Manually follow up within 24 hours.
- **Duplicate detection failure:** Log to Audit Log. Worst case: a duplicate Contact is created. Review weekly.
