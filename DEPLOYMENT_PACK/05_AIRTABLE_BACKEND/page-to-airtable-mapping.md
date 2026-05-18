# She Said Sail: Page-to-Airtable Mapping

Which page triggers which Airtable table records, and which Make.com scenarios connect them.

---

## Overview

| Page | URL | Creates / Reads | Make.com Scenario |
|---|---|---|---|
| Homepage | / | Creates: Contacts (email capture) | M-EMAIL-CAPTURE |
| Request to Book | /request-to-book/ | Creates: Requests + UTMs + Contacts | M-WEBFORM-REQUEST-CAPTURE, M-UTM-CAPTURE |
| Thank You | /thank-you/ | Updates: Requests (status update) | M-BRAND-ROUTER |
| Experiences | /experiences/ | No records created or read | GTM only (no Make.com scenario) |

---

## Page: Homepage (/)

**What happens:** A visitor enters their email into the email capture section at the bottom of the homepage and clicks Subscribe.

**Airtable tables affected:**

### Contacts Table
- Make.com checks whether a Contact with that email already exists.
- If the Contact exists: Make.com updates the record and sets `Email Subscribed = true`, `Last Seen At = now()`.
- If the Contact does not exist: Make.com creates a new Contact record with:
  - Email (from form)
  - Email Subscribed: true
  - Source: "email-capture-form"
  - UTM Source, UTM Campaign: from hidden fields
  - Created At: now()
  - Brand: shesaidsail

**Make.com scenario:** M-EMAIL-CAPTURE
- Trigger: Webhook receives email-capture payload from homepage form
- Steps: Parse payload > Search Contacts for matching email > Update or create Contact > Write to Audit Log

**GTM events fired:** `submit_email_capture` (fires on successful form submit)

---

## Page: Request to Book (/request-to-book/)

**What happens:** A visitor fills in the Request to Book form (Name, Email, Phone, Occasion, Group Size, Date, Experience Interest, Message) and submits it.

**Airtable tables affected:**

### Requests Table
- Make.com creates a new Request record with all form fields.
- Status is set to "New".
- Internal Rating is set to "Warm" by default, or "Hot" if Occasion = Bachelorette or Group Size >= 15.
- Submitted At is set to now().

### UTMs Table
- Make.com creates a new UTM record with all hidden tracking fields from the payload.
- The UTM record is linked to the new Request record via the Linked Record field.

### Contacts Table
- Make.com searches for an existing Contact with the submitted email.
- If the Contact exists: updates Full Name, Phone, Last Seen At. Does not overwrite UTM first-touch fields.
- If the Contact does not exist: creates a new Contact with email, name, phone, first-touch UTM fields, Source = "request-to-book-form", Created At = now().
- The Contact record is linked to the new Request record.

### Audit Log Table
- Make.com writes one Audit Log entry: Action = form_submission, Status = Success, Details = summary of the submission.

**Make.com scenarios:**
- M-WEBFORM-REQUEST-CAPTURE: Main scenario. Receives webhook, creates Requests record, calls sub-scenarios.
- M-UTM-CAPTURE: Sub-scenario or module sequence within M-WEBFORM-REQUEST-CAPTURE. Creates UTMs record and links it.
- M-BRAND-ROUTER: Routes the submission to the correct brand handler. For She Said Sail, it checks `brand = shesaidsail` and continues. (This scenario supports future multi-brand expansion.)
- M-CONCIERGE-ASSIGNMENT: Sub-scenario triggered after Request is created. Currently assigns to default concierge. Future: round-robin logic.
- M-INQUIRY-CONFIRMATION-EMAIL: Sends confirmation email to the submitter.
- M-SLACK-NEW-LEAD-ALERT: Posts alert to the #she-said-sail-leads Slack channel.
- M-AIRTABLE-AUDIT-LOGGER: Writes the Audit Log entry.

**GTM events fired:** `start_booking_form` (on first field interaction), `submit_booking_form` (on successful submit)

---

## Page: Thank You (/thank-you/)

**What happens:** After a successful form submission, the user is redirected to /thank-you/. This page fires a GTM event and optionally triggers a Make.com status update.

**Airtable tables affected:**

### Requests Table
- Optional: Make.com scenario M-BRAND-ROUTER can listen for a `view_thank_you_page` GTM event forwarded via a server-side trigger or a small webhook fired from the thank-you page JS.
- If configured: updates the most recent Request for that session from Status = "New" to Status = "Confirmed - Automated Response".
- This step is optional in v1. The confirmation email is a stronger signal. Implement after core integration is stable.

**Make.com scenario:** M-BRAND-ROUTER (optional step, may be deferred to v2)

**GTM events fired:** `view_thank_you_page` (fires on page load, marked as a conversion in GA4 and Meta Pixel)

---

## Page: Experiences (/experiences/)

**What happens:** Visitors browse experience cards. No form is submitted on this page.

**Airtable tables affected:** None. This page does not create or read any Airtable records.

**GTM events fired:**
- `view_experiences_page` (on page load)
- `click_experience_card` (on card click, with `experience_name` and `card_position` parameters)
- `click_request_to_book` (on any CTA button click)

**Make.com scenario:** None for this page.

**Analytics note:** The `view_experiences_page` GTM event feeds the Campaign analytics. In GA4, this event is used to build the "Experiences Browsers" audience for remarketing.

---

## Data Flow Summary

```
Homepage email capture
  -> Make.com M-EMAIL-CAPTURE
  -> Contacts table (create or update)

Request to Book form submit
  -> Make.com M-WEBFORM-REQUEST-CAPTURE
  -> Requests table (create)
  -> UTMs table (create, link to Request)
  -> Contacts table (create or update, link to Request)
  -> Audit Log table (write entry)
  -> M-INQUIRY-CONFIRMATION-EMAIL (email to submitter)
  -> M-SLACK-NEW-LEAD-ALERT (Slack post to team)

/thank-you/ page load
  -> GTM fires view_thank_you_page
  -> GA4 records conversion
  -> Meta Pixel fires Lead event
  -> Optional: Make.com updates Request status
```
