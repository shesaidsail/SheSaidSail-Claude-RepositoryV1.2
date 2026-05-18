# Contact Page: Backend Specification

Page: /contact/
Last updated: 2026-05-18

---

## Contact Form Payload Fields

The contact form submits the following JSON fields to the Make.com webhook. These fields are intentionally minimal. No UTM fields are included. The contact form is separate from the booking form.

| Field | Source | Notes |
|---|---|---|
| contact_name | Form input (name="contact_name") | Required |
| contact_email | Form input (name="contact_email") | Required |
| inquiry_type | Form select (name="inquiry_type") | Required. One of 5 options listed below |
| contact_message | Form textarea (name="contact_message") | Required |
| brand | Hidden field (value="shesaidsail") | Static value |
| submission_page | Hidden field (value="/contact/") | Static value |
| source_url | Hidden field, populated by JS (window.location.href) | Captures query strings and referrer path |

Inquiry type options:
- General Question
- Press or Media
- Partnership Inquiry
- Event Planning Collaboration
- Something Else

---

## Airtable Mapping

Table: Requests (existing table, do not create a new one)

| Airtable Field | Value |
|---|---|
| Request_Type | "General Inquiry" (static string) |
| Name | contact_name |
| Email | contact_email |
| Notes | contact_message + " [Inquiry Type: " + inquiry_type + "]" |
| Brand | "shesaidsail" (from brand field) |
| Source_URL | source_url |

Notes field construction example: "I have a question about media coverage. [Inquiry Type: Press or Media]"

Do not map UTM fields. Do not map date_of_charter, guest_count, or any booking-specific fields. This is a general inquiry record, not a booking record.

---

## New Make.com Scenario: M-CONTACT-001

This is a new, lightweight scenario. It must NOT share a webhook with the booking form scenario (M-BRAND-ROUTER or any existing scenario). Contact inquiries and booking inquiries must remain completely separate in the pipeline.

### Scenario name
M-CONTACT-001

### Trigger: Webhook
- Create a new webhook in Make.com for this scenario.
- Copy the webhook URL.
- Replace the placeholder string WIRE_THIS_CONTACT_WEBHOOK_URL in contact-html-snippets.html with the actual webhook URL.
- Set JSON data structure to match the payload fields listed above.

### Module 1: Airtable Create Record
- Connection: existing Airtable connection
- Base: She Said Sail (existing base)
- Table: Requests
- Field mapping: see Airtable Mapping section above

### Module 2: Email Acknowledgment
- Send to: contact_email (from webhook payload)
- From: hello@shesaidsail.com (or configured sender)
- Subject: "We received your message"
- Body (plain text or simple HTML):

  Hi [contact_name],

  Thank you for reaching out to She Said Sail. We received your message and will follow up within 48 hours.

  If your question is about booking a charter, you can get started faster at shesaidsail.com/request-to-book/

  Talk soon,
  The She Said Sail Team

### Module 3: Slack Alert (optional)
- Workspace: She Said Sail Slack
- Channel: #general-inquiries
- Message format:
  New contact form submission
  From: [contact_name] ([contact_email])
  Type: [inquiry_type]
  Message: [contact_message]
  Source: [source_url]

---

## Wiring Checklist

1. Build M-CONTACT-001 in Make.com.
2. Copy the webhook URL from the trigger module.
3. Open contact-html-snippets.html.
4. Replace the string WIRE_THIS_CONTACT_WEBHOOK_URL with the actual webhook URL (inside the fetch() call in the script tag at the bottom of the file).
5. Save and deploy.
6. Test with a real form submission and confirm:
   - Airtable record created in Requests table with Request_Type = "General Inquiry"
   - Acknowledgment email received at the submitted email address
   - Slack alert posted to #general-inquiries (if Module 3 is enabled)

---

## Important Separation Note

The booking form at /request-to-book/ has its own webhook that routes through M-BRAND-ROUTER with 13 hidden fields including UTM parameters, booking-specific data, and Airtable routing logic.

The contact form at /contact/ uses M-CONTACT-001 and a separate webhook. The two pipelines must not be merged. Routing contact submissions through the booking form webhook would corrupt UTM attribution and booking routing logic.
