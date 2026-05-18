# She Said Sail: Make.com Webhook Setup Guide

Step-by-step guide for a developer setting up all Make.com automation scenarios. Follow the sections in order. Do not activate scenarios until all steps in a section are complete.

---

## 1. Prerequisites

Confirm all of the following before starting:

- [ ] Make.com account is active and you have access to the She Said Sail organization (or your personal workspace if building solo)
- [ ] Airtable base is created with all 7 tables (see `05_AIRTABLE_BACKEND/airtable-table-schema.md`)
- [ ] Airtable API key (Personal Access Token) is available: go to airtable.com > Account > Developer Hub > Create Token. Scope: `data.records:read`, `data.records:write`, `schema.bases:read`
- [ ] Airtable Base ID is noted: open the base in your browser, the Base ID is in the URL: `airtable.com/[BASE_ID]/...`
- [ ] Slack workspace is connected in Make.com: go to Make.com > Connections > Add > Slack > Authorize
- [ ] Email platform is connected (Gmail or your transactional email provider): go to Make.com > Connections > Add > Gmail (or SendGrid, Postmark, etc.) > Authorize
- [ ] WordPress site is accessible and the Request to Book form is published with hidden fields added (see `05_AIRTABLE_BACKEND/request-form-hidden-fields.md`)

---

## 2. Order to Create Scenarios

Build scenarios in this order. Later scenarios depend on earlier ones being stable.

1. M-WEBFORM-REQUEST-CAPTURE (main form intake)
2. M-UTM-CAPTURE (sub-flow, called from #1)
3. M-EMAIL-CAPTURE (homepage email form, independent)
4. M-INQUIRY-CONFIRMATION-EMAIL (triggered by #1)
5. M-SLACK-NEW-LEAD-ALERT (triggered by #1)
6. M-AIRTABLE-AUDIT-LOGGER (triggered by #1 and #3)
7. M-BRAND-ROUTER (add last, after core flows are tested)
8. M-CONCIERGE-ASSIGNMENT (add last, after core flows are tested)

---

## 3. Scenario Setup: Step by Step

---

### Scenario M-WEBFORM-REQUEST-CAPTURE

**Purpose:** Receives the Request to Book form payload and creates all Airtable records.

**Trigger type:** Webhook (Custom Webhook)

**Step-by-step:**

1. In Make.com, click Create a new scenario.
2. Click the large plus (+) icon to add the first module.
3. Search for "Webhooks" and select "Custom Webhook."
4. Click "Add" to create a new webhook. Name it: `she-said-sail-request-capture`.
5. Copy the webhook URL shown. It will look like: `https://hook.eu2.make.com/XXXXXXXXXXXXXX` (your region may differ).
6. Click OK. The webhook is now listening.

**Getting the webhook URL:**
The URL is shown immediately after you create the Custom Webhook module. You can also find it later by clicking the webhook module > Edit > copy the URL shown at the top.

**Where to paste the webhook URL in WordPress:**
Open `02_GLOBAL_JS/she-said-sail-global.js`. Find the comment `// WIRE THIS to your Make.com webhook`. Replace the empty string with your webhook URL:
```javascript
var webhookUrl = 'https://hook.eu2.make.com/XXXXXXXXXXXXXX';
```

**Module sequence after the webhook trigger:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Webhooks: Custom Webhook | Trigger. Receives the form payload. |
| 2 | Tools: Set Variable | Parse `group_size` as integer. |
| 3 | Tools: Set Variable | Evaluate `internal_rating`: if `occasion` = "Bachelorette" OR `group_size` >= 15, set "Hot"; else set "Warm". |
| 4 | Airtable: Create a Record | Table: Requests. Map all form fields to Airtable fields per `airtable-field-map.md`. Set Status = "New", Internal Rating = from Step 3, Submitted At = `{{now}}`. |
| 5 | Airtable: Search Records | Table: Contacts. Search by Email = `{{payload.email}}`. |
| 6 | Router | Two routes: Route A (Contact found), Route B (Contact not found). |
| 7a | Airtable: Update a Record (Route A) | Update existing Contact: Full Name, Phone, Last Seen At = `{{now}}`. Link to new Request record. |
| 7b | Airtable: Create a Record (Route B) | Create new Contact with all contact fields. Link to new Request record. |
| 8 | Airtable: Create a Record | Table: UTMs. Map all utm_* and tracking fields. Link to new Request record. |
| 9 | HTTP: Make a Request | Call M-INQUIRY-CONFIRMATION-EMAIL webhook (or use Make.com sub-scenario). |
| 10 | HTTP: Make a Request | Call M-SLACK-NEW-LEAD-ALERT webhook (or use Make.com sub-scenario). |
| 11 | Airtable: Create a Record | Table: Audit Log. Action = "form_submission", Status = "Success", Details = concatenated summary. |

**Activate:** Turn the scenario ON after testing.

---

### Scenario M-UTM-CAPTURE

**Purpose:** Creates a UTMs table record and links it to a Requests record. Called as a sub-scenario from M-WEBFORM-REQUEST-CAPTURE (Step 8 above can be done inline; this scenario exists as a named module for reuse).

**Trigger type:** Webhook (Custom Webhook) or inline within M-WEBFORM-REQUEST-CAPTURE.

**Recommendation:** Implement this inline within M-WEBFORM-REQUEST-CAPTURE (Step 8) in v1. Promote to a standalone scenario in v2 if you need to call it from multiple places.

---

### Scenario M-EMAIL-CAPTURE

**Purpose:** Receives the homepage email capture form payload and creates or updates a Contact.

**Trigger type:** Webhook (Custom Webhook)

**Step-by-step:**

1. Create a new scenario. First module: Webhooks > Custom Webhook.
2. Name it: `she-said-sail-email-capture`.
3. Copy the webhook URL.
4. Paste the URL into the homepage email capture form's submit handler in the JavaScript file. Find the comment `// WIRE THIS to your Make.com email-capture webhook`.

**Module sequence:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Webhooks: Custom Webhook | Receives email-capture payload. |
| 2 | Airtable: Search Records | Table: Contacts. Search by Email = `{{payload.email}}`. |
| 3 | Router | Route A: Contact found. Route B: Contact not found. |
| 4a | Airtable: Update a Record (Route A) | Set Email Subscribed = true, Last Seen At = now(). |
| 4b | Airtable: Create a Record (Route B) | Create Contact: Email, Email Subscribed = true, Source = "email-capture-form", UTM fields, Created At = now(), Brand = shesaidsail. |
| 5 | Airtable: Create a Record | Audit Log. Action = "contact_created" or "contact_updated". |

---

### Scenario M-BRAND-ROUTER

**Purpose:** Routes incoming submissions to the correct brand handler. In v1, She Said Sail is the only brand, so this simply passes through. Designed for future multi-brand expansion.

**Trigger type:** Called from M-WEBFORM-REQUEST-CAPTURE or as a webhook.

**Module sequence:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Router | Check `{{payload.brand}}`. Route A: "shesaidsail". Route B: other (error log). |
| 2 (Route A) | Continue | Pass payload to downstream scenarios as normal. |
| 2 (Route B) | Airtable: Create a Record | Audit Log. Action = "error", Details = "Unknown brand: " + brand value. |

---

### Scenario M-CONCIERGE-ASSIGNMENT

**Purpose:** Assigns a concierge to a new Request after it is created.

**Trigger type:** Airtable Trigger (watches for new records in the Requests table where Status = New and Assigned Concierge is empty).

**Module sequence:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Airtable: Watch Records | Table: Requests. Filter: Status = New. |
| 2 | Tools: Set Variable | Concierge email (hard-code for v1: the team member's email address). |
| 3 | Airtable: Update a Record | Set Assigned Concierge = concierge from Step 2, Follow-up Date = 1 business day from Submitted At. |
| 4 | Airtable: Create a Record | Audit Log. Action = "record_updated", Details = "Concierge assigned." |

---

### Scenario M-INQUIRY-CONFIRMATION-EMAIL

**Purpose:** Sends a confirmation email to the person who submitted the Request to Book form.

**Trigger type:** Webhook (called from M-WEBFORM-REQUEST-CAPTURE) or Airtable Trigger (new Requests record).

**Module sequence:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Webhooks: Custom Webhook | Receives the parsed form data from M-WEBFORM-REQUEST-CAPTURE. |
| 2 | Email/Gmail: Send an Email | To: `{{payload.email}}`. From: your@shesaidsail.com. Subject: "We received your inquiry, [Name]". Body: see below. |

**Email body (plain text):**

```
Hi {{payload.full_name}},

Thank you for reaching out to She Said Sail. We received your inquiry and someone from our team will be in touch within 24 hours.

Your inquiry details:
- Occasion: {{payload.occasion}}
- Group Size: {{payload.group_size}}
- Preferred Date: {{payload.preferred_date}}
- Experience Interest: {{payload.experience_interest}}

If you have any questions in the meantime, you can reach us at hello@shesaidsail.com.

We look forward to celebrating with you.

The She Said Sail Team
shesaidsail.com
```

---

### Scenario M-SLACK-NEW-LEAD-ALERT

**Purpose:** Posts a real-time alert in the Slack channel when a new inquiry is received.

**Trigger type:** Webhook (called from M-WEBFORM-REQUEST-CAPTURE).

**Module sequence:**

| Step | Module | Configuration |
|---|---|---|
| 1 | Webhooks: Custom Webhook | Receives parsed form data. |
| 2 | Slack: Create a Message | Channel: #she-said-sail-leads. Message: see below. |

**Slack message format:**

```
New inquiry from {{payload.full_name}}
Occasion: {{payload.occasion}} | Group: {{payload.group_size}} people | Date: {{payload.preferred_date}}
Experience: {{payload.experience_interest}}
Rating: {{internal_rating}}
Source: {{payload.utm_source}} / {{payload.utm_campaign}}
Email: {{payload.email}} | Phone: {{payload.phone}}
```

---

### Scenario M-AIRTABLE-AUDIT-LOGGER

**Purpose:** Centralized logging. Writes to the Audit Log table. Can be called from any scenario.

**Trigger type:** Webhook (receives a structured log payload from other scenarios).

**Recommended payload format:**
```json
{
  "action": "form_submission",
  "scenario_id": "M-WEBFORM-REQUEST-CAPTURE",
  "related_record_type": "Request",
  "related_record_id": "recXXXXXXXXXXXXXX",
  "details": "New request created for jessica.moore@example.com",
  "status": "Success"
}
```

---

## 4. Testing

### Submit a Test Form

1. Open the Request to Book page with test UTM params:
   `/request-to-book/?utm_source=test&utm_medium=test&utm_campaign=qa-test-20260518&creative_id=TEST-001`
2. Fill in visible fields with test data (use a real email you can check).
3. Submit the form.

### Verify in Airtable

- [ ] Requests table: new record exists with correct data
- [ ] UTMs table: new UTM record exists linked to the Request
- [ ] Contacts table: new Contact exists or existing Contact was updated
- [ ] Audit Log table: new entry with Action = form_submission, Status = Success

### Verify Email and Slack

- [ ] Confirmation email received at the test email address within 2 minutes
- [ ] Slack alert posted in #she-said-sail-leads

### After Testing

Delete the test records in Airtable (see test-payloads.md > Rollback instructions).

---

## 5. Error Handling Configuration

Configure these error handlers in every Make.com scenario:

**Global error handler (add to each scenario):**

1. In the scenario, click the wrench icon > Settings > Enable incomplete executions.
2. Add an Error Handler module after the main flow: Webhooks > Ignore OR Tools > Set Variable + Airtable > Create a Record (write to Audit Log with Status = Error).
3. For email scenarios: if the email send fails, write to Audit Log and continue (do not stop the scenario -- the Airtable record is more important than the email).

**Retry configuration:**
- Set Max number of cycles: 1 (no retry loops for form submissions, to avoid duplicate records).
- For email-only scenarios: Max number of cycles: 3 with a 5-minute delay between retries.

**Incomplete executions:**
- Enable "Store incomplete executions" in every scenario. This lets you inspect and replay failed runs from Make.com > Incomplete Executions.
