# She Said Sail: Chatbot Backend Mapping
**Version:** 1.0
**Date:** May 2026

Defines how chatbot conversation data maps to Airtable, Make.com, and the existing backend architecture.

---

## PAYLOAD STRUCTURE

The chatbot sends one JSON payload to Make.com at STATE 7 (handoff). The payload contains all data collected during the conversation plus UTM attribution read from sessionStorage.

```json
{
  "occasion": "bachelorette",
  "occasion_energy": "high",
  "guest_count": "9 to 15",
  "selected_experience": "monaco-social",
  "preferred_date": "June 14, 2026",
  "first_name": "Mia",
  "email": "mia@example.com",
  "phone": "+13055551234",
  "conversation_summary": "Group of 12 for a bachelorette. Interested in Monaco Social.",
  "landing_page": "https://shesaidsail.com/experience/monaco-social/",
  "utm_source": "instagram",
  "utm_medium": "paid",
  "utm_campaign": "bachelorette-summer-2026",
  "utm_content": "",
  "utm_term": "",
  "referrer_url": "https://www.instagram.com/",
  "brand": "shesaidsail",
  "service_category": "yacht-charter",
  "source_type": "chatbot"
}
```

The `source_type: "chatbot"` field distinguishes chatbot leads from form leads in Airtable. This is a new value for the existing source_type concept. It does not require a new Airtable field if Request_Type is used instead (see below).

---

## AIRTABLE MAPPING

**Target table:** Requests (existing table, no new tables needed)

| Chatbot Payload Field | Airtable Field | Type | Notes |
|---|---|---|---|
| first_name | Name | Single Line Text | First name only from chatbot |
| email | Email | Email | Required to submit chatbot lead |
| phone | Phone | Phone Number | Optional, may be blank |
| occasion | Occasion | Single Select | Map: "bachelorette" to "Bachelorette", "birthday" to "Birthday", "girls_trip" to "Girls Trip", "intimate" to "Intimate / Anniversary" |
| guest_count | Guest Count (Estimate) | Single Line Text | Text range string (e.g., "9 to 15") |
| selected_experience | Experience Interest | Multiple Select | Map slug to display name: "monaco-social" to "Monaco Social" etc. |
| preferred_date | Preferred Date | Single Line Text | Free text; may be "flexible" |
| conversation_summary | Notes | Long Text | Append to any existing notes field |
| utm_source | UTM Source | Single Line Text | Existing hidden field |
| utm_medium | UTM Medium | Single Line Text | Existing hidden field |
| utm_campaign | UTM Campaign | Single Line Text | Existing hidden field |
| landing_page | Landing Page | URL | Existing hidden field |
| referrer_url | Referrer URL | URL | Existing hidden field |
| brand | Brand | Single Select | "She Said Sail" |
| service_category | Service Category | Single Select | "yacht-charter" |
| source_type | Request Type | Single Select | Add "Chatbot Lead" as a new option in the Requests table Request_Type field |

**New Airtable field required:**
Add "Chatbot Lead" as a new option to the existing Request_Type Single Select field in the Requests table. No new tables needed.

---

## MAKE.COM SCENARIO

**Scenario name:** M-CHATBOT-001
**Trigger:** Custom Webhook (new webhook, separate from booking form and contact form)
**Webhook placeholder in chatbot-js.js:** `WIRE_THIS_CHATBOT_WEBHOOK_URL`

**Module sequence:**

Module 1: Webhook (trigger)
Receives the chatbot payload JSON.

Module 2: Airtable Create Record
- Base: She Said Sail
- Table: Requests
- Fields: map from payload using the Airtable mapping table above
- Request_Type: "Chatbot Lead"

Module 3: Email Send (acknowledgment)
- To: email from payload
- Subject: "She Said Sail: we received your request"
- Body: Warm, brief. "Hi [first_name], your concierge will be in touch within 24 hours. We are looking forward to planning this with you."
- Use the same email template style as M-INQUIRY-CONFIRMATION-EMAIL

Module 4: Slack Alert
- Channel: #new-leads
- Message: "New chatbot lead: [first_name], [email], occasion: [occasion], experience: [selected_experience], group: [guest_count], date: [preferred_date]"

Module 5: Airtable Audit Log
- Log the event in the Audit Log table
- Event: "chatbot_lead_created"
- Record_ID: from Module 2 output

**Webhook wiring:**
After creating M-CHATBOT-001 in Make.com:
1. Copy the webhook URL
2. Open DEPLOYMENT_PACK/chatbot/chatbot-js.js in Insert Headers and Footers editor
3. Search for WIRE_THIS_CHATBOT_WEBHOOK_URL
4. Replace with the actual Make.com webhook URL
5. Save

---

## UTM ATTRIBUTION

The chatbot reads UTM data from sessionStorage key 'sss_utm' which is populated by the global JS file (she-said-sail-global.js Section 1: UTM Capture). This is the same first-touch attribution system used by the booking form.

No changes to the UTM capture system are needed. The chatbot piggybacks on the existing sessionStorage values.

If sessionStorage has no UTM data (direct traffic), all UTM fields send as empty strings. This is the correct behavior.

---

## ESCALATION FLAG

When a user explicitly requests human escalation, add an escalation flag to the payload:

```json
{
  ...standard fields...,
  "escalation_requested": true,
  "escalation_reason": "user_requested"
}
```

Make.com M-CHATBOT-001 should check for this flag and:
- Set Request_Type to "Chatbot Escalation" instead of "Chatbot Lead"
- Trigger an immediate Slack alert tagged @concierge

---

## BACKEND COMPATIBILITY SUMMARY

| System | Compatibility | Action Needed |
|---|---|---|
| Airtable Requests table | Full | Add "Chatbot Lead" option to Request_Type field |
| Make.com | Full | Build M-CHATBOT-001 scenario |
| Existing UTM capture | Full | None (reads from sss_utm sessionStorage) |
| Booking form | Full | No interference (separate webhook) |
| Contact form | Full | No interference (separate webhook) |
| Global JS | Full | None (chatbot-js.js reads sessionStorage values set by global JS) |
