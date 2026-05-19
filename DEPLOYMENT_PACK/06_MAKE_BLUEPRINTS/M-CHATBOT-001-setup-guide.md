# M-CHATBOT-001: Chatbot Lead Handoff Setup Guide

**Blueprint file:** `06_MAKE_BLUEPRINTS/M-CHATBOT-001-blueprint.json`
**Status:** NOT BUILT (must be completed before go-live)
**Time to complete:** 30 to 45 minutes
**Priority:** Required. Without this scenario, every chatbot conversation that reaches the handoff state loses the lead.

---

## What this scenario does

When a visitor completes the chatbot conversation and provides their name, email, and phone number, the chatbot JS fires a webhook with the full conversation payload. This scenario receives that payload and:

1. Checks Airtable Contacts for an existing record with the same email
2. Updates the existing contact (or creates a new one if none found)
3. Creates a UTM record linked to the contact
4. Creates a Request record linked to the contact and UTM
5. Creates a Chatbot Conversations record with the full conversation data
6. Posts a log entry to the Audit Log
7. Sends a Slack alert to #new-leads

---

## Prerequisites

Before building this scenario, confirm:

- [ ] Airtable base is built and contains these tables: Contacts, Requests, UTMs, Chatbot Conversations, Audit Log
- [ ] Airtable base ID is known (found in the Airtable URL: `airtable.com/appXXXXXXX/...`)
- [ ] Make.com account has access to the Airtable app connection
- [ ] Make.com account has access to the Slack app connection
- [ ] Slack #new-leads channel exists
- [ ] M-AIRTABLE-AUDIT-LOGGER scenario is built and its webhook URL is available

---

## Option A: Import the blueprint (recommended)

### Step 1: Create a new scenario

1. Log in to Make.com
2. In the left sidebar, click **Scenarios**
3. Click **Create a new scenario** (top right)
4. Close the module picker that appears

### Step 2: Import the blueprint

1. Click the three-dot menu icon (top right of the scenario canvas, or kebab menu in the scenario header)
2. Click **Import Blueprint**
3. Upload `06_MAKE_BLUEPRINTS/M-CHATBOT-001-blueprint.json`
4. The scenario loads with 10 modules connected

### Step 3: Wire the Airtable base ID

The blueprint uses the placeholder `WIRE_AIRTABLE_BASE_ID` in all Airtable modules. You need to replace this with your real base ID.

1. Click each Airtable module (modules 2, 4, 5, 6, 7, 8)
2. In the **Base** field, select or type your She Said Sail Airtable base
3. In the **Table** field, confirm the correct table is selected
4. Click **OK** to save each module

### Step 4: Wire the Audit Log webhook URL

1. Click module 9 (the HTTP module)
2. Replace `WIRE_AUDIT_LOG_WEBHOOK_URL` with the webhook URL from your M-AIRTABLE-AUDIT-LOGGER scenario
3. Click **OK**

### Step 5: Wire the Slack channel

1. Click module 10 (the Slack module)
2. In the **Channel** field, select **#new-leads** from the dropdown
3. Click **OK**

### Step 6: Activate the webhook trigger

1. Click module 1 (the Webhook module)
2. Click **Add** to create a new webhook
3. Name it: `SSS Chatbot Handoff`
4. Click **Save**
5. Copy the webhook URL that appears (format: `https://hook.us1.make.com/XXXXXXXXXXXXXXXX`)

### Step 7: Wire the webhook URL into the chatbot JS

The chatbot JS has a placeholder that needs the real webhook URL.

1. Open `DEPLOYMENT_PACK/chatbot/chatbot-js.js`
2. Find the line: `xhr.open('POST', 'WIRE_THIS_CHATBOT_WEBHOOK_URL', true);`
3. Replace `WIRE_THIS_CHATBOT_WEBHOOK_URL` with the real webhook URL from Step 6
4. Save the file

If the chatbot JS is already deployed to WordPress, update it there too:
- WordPress Admin > Settings > Insert Headers and Footers > Scripts in Footer
- Find the chatbot JS block
- Update the URL in place
- Save

### Step 8: Set scenario name and activate

1. Click the scenario name at the top (defaults to something generic)
2. Rename it to: `M-CHATBOT-001: Chatbot Lead Handoff`
3. Click the **ON/OFF toggle** to activate the scenario
4. Confirm the toggle shows ON (blue)

---

## Option B: Build manually

If the blueprint import does not work, build the scenario manually with these 10 modules in order.

### Module 1: Webhook trigger

- Module type: **Webhooks > Custom Webhook**
- Create new webhook named: `SSS Chatbot Handoff`
- No additional configuration needed. The payload schema is detected automatically on first run.

### Module 2: Airtable search (find existing contact)

- Module type: **Airtable > Search Records**
- Base: She Said Sail
- Table: Contacts
- Formula: `{email} = '{{1.email}}'`
- Max records: 1

### Module 3: Router

- Module type: **Flow Control > Router**
- Route 1 filter: "Contact exists" -- condition: `{{length(2.records)}} > 0`
- Route 2 filter: "New contact" -- condition: `{{length(2.records)}} = 0`

### Module 4 (Route 1): Airtable update existing contact

- Module type: **Airtable > Update a Record**
- Base: She Said Sail
- Table: Contacts
- Record ID: `{{2.records[].id}}` (the found record)
- Fields to update:
  - First Name: `{{1.first_name}}`
  - Phone: `{{1.phone}}`
  - Last Source: `chatbot`
  - Last UTM Source: `{{1.utm_source}}`
  - Last UTM Medium: `{{1.utm_medium}}`
  - Last UTM Campaign: `{{1.utm_campaign}}`
  - Last Seen At: `{{now}}`

### Module 5 (Route 2): Airtable create new contact

- Module type: **Airtable > Create a Record**
- Base: She Said Sail
- Table: Contacts
- Fields:
  - First Name: `{{1.first_name}}`
  - Email: `{{1.email}}`
  - Phone: `{{1.phone}}`
  - Visitor ID: `{{1.visitor_id}}`
  - Source: `chatbot`
  - UTM Source: `{{1.utm_source}}`
  - UTM Medium: `{{1.utm_medium}}`
  - UTM Campaign: `{{1.utm_campaign}}`
  - UTM Content: `{{1.utm_content}}`
  - UTM Term: `{{1.utm_term}}`
  - Referrer URL: `{{1.referrer_url}}`
  - First Seen At: `{{now}}`

### Module 6: Airtable create UTM record

- Module type: **Airtable > Create a Record**
- Base: She Said Sail
- Table: UTMs
- Fields:
  - UTM Source: `{{1.utm_source}}`
  - UTM Medium: `{{1.utm_medium}}`
  - UTM Campaign: `{{1.utm_campaign}}`
  - UTM Content: `{{1.utm_content}}`
  - UTM Term: `{{1.utm_term}}`
  - Landing Page: `{{1.landing_page}}`
  - Referrer URL: `{{1.referrer_url}}`
  - Captured At: `{{now}}`
  - Contact: `{{ifempty(4.id, 5.id)}}` (link to Contact record)

Note: After Route 1 and Route 2 converge back to the main flow, use `{{ifempty(4.id, 5.id)}}` to reference whichever contact record was used (updated or created).

### Module 7: Airtable create Request record

- Module type: **Airtable > Create a Record**
- Base: She Said Sail
- Table: Requests
- Fields:
  - First Name: `{{1.first_name}}`
  - Email: `{{1.email}}`
  - Phone: `{{1.phone}}`
  - Occasion: `{{1.occasion}}`
  - Experience Requested: `{{1.selected_experience}}`
  - Group Size: `{{1.guest_count}}`
  - Preferred Date: `{{1.preferred_date}}`
  - Source: `chatbot`
  - Brand: `{{1.brand}}`
  - Status: `New`
  - Visitor ID: `{{1.visitor_id}}`
  - UTM Source: `{{1.utm_source}}`
  - UTM Medium: `{{1.utm_medium}}`
  - UTM Campaign: `{{1.utm_campaign}}`
  - Landing Page: `{{1.landing_page}}`
  - Submitted At: `{{now}}`
  - Contact: `{{ifempty(4.id, 5.id)}}` (link)
  - UTM Record: `{{6.id}}` (link)

### Module 8: Airtable create Chatbot Conversations record

- Module type: **Airtable > Create a Record**
- Base: She Said Sail
- Table: Chatbot Conversations
- Fields: map all conversation fields from the payload (see payload schema below)
- Contact: `{{ifempty(4.id, 5.id)}}` (link)
- Request: `{{7.id}}` (link)
- Completed At: `{{now}}`

### Module 9: HTTP POST to Audit Log

- Module type: **HTTP > Make a Request**
- URL: your M-AIRTABLE-AUDIT-LOGGER webhook URL
- Method: POST
- Body type: Raw
- Content type: JSON
- Body: `{"event": "chatbot_lead_created", "request_id": "{{7.id}}", "contact_id": "{{ifempty(4.id, 5.id)}}", "source": "M-CHATBOT-001", "timestamp": "{{now}}"}`

### Module 10: Slack alert

- Module type: **Slack > Create a Message**
- Channel: #new-leads
- Message: see blueprint for full formatted text

---

## Chatbot payload schema

The chatbot JS sends this payload on every completed conversation:

```json
{
  "occasion": "Bachelorette party",
  "occasion_energy": "social",
  "guest_count": "8",
  "selected_experience": "monaco-social",
  "preferred_date": "June 2026",
  "first_name": "Sarah",
  "email": "sarah@example.com",
  "phone": "305-555-1234",
  "conversation_summary": "Bachelorette, social energy, 8 guests, Monaco Social recommended, June 2026",
  "landing_page": "https://shesaidsail.com/",
  "utm_source": "instagram",
  "utm_medium": "social",
  "utm_campaign": "bachelorette-spring-2026",
  "utm_content": "",
  "utm_term": "",
  "referrer_url": "https://instagram.com",
  "brand": "shesaidsail",
  "service_category": "yacht-charter",
  "visitor_id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "source_type": "chatbot"
}
```

All fields are strings. `phone` may be empty if the user skipped it. `utm_*` fields may be empty for direct traffic.

---

## Testing

### Send a test payload manually

1. With the scenario active and webhook URL copied, open a terminal or use a tool like Postman
2. Send a POST request to the webhook URL with the payload schema above (use your own email)
3. Check Make.com scenario history: it should show a successful run
4. Check Airtable: confirm records appear in Contacts, UTMs, Requests, and Chatbot Conversations
5. Check Slack #new-leads: confirm the alert message appears

### Test through the chatbot

1. Open the site in a browser
2. Click the chatbot widget
3. Complete the full conversation flow through to the handoff step (provide name, email, phone)
4. Within 10 seconds, check Airtable and Slack
5. Confirm all records are created and linked correctly

---

## Airtable field name reference

These are the exact field names the blueprint maps to. If your Airtable field names differ, update the blueprint mapper accordingly.

| Blueprint field | Expected Airtable field name |
|---|---|
| First Name | First Name |
| Email | Email |
| Phone | Phone |
| Occasion | Occasion |
| Experience Requested | Experience Requested |
| Group Size | Group Size (Number field) |
| Preferred Date | Preferred Date |
| Source | Source |
| Status | Status (Single select: New) |
| Visitor ID | Visitor ID |
| UTM Source | UTM Source |
| Submitted At | Submitted At (Date field) |
| Contact | Contact (Link to Contacts table) |
| UTM Record | UTM Record (Link to UTMs table) |

If any field name does not match exactly, the record will be created but that field will be empty. Check the scenario run history in Make.com for any mapping errors after the first test run.
