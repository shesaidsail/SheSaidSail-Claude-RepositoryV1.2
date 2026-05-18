# She Said Sail: Backend QA Checklist

Covers Airtable and Make.com. Complete this before running the form submission tests in form-qa-checklist.md.

Reviewer: _____________________ Date: _____________________

---

## Section A: Airtable

### Tables Created

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 1 | Requests table exists | | | |
| 2 | Bookings table exists | | | |
| 3 | Contacts table exists | | | |
| 4 | Campaigns table exists | | | |
| 5 | UTMs table exists | | | |
| 6 | Client Notes table exists | | | |
| 7 | Audit Log table exists | | | |

### Field Schemas Match Specification

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 8 | Requests table: all fields present per `airtable-table-schema.md` including Status (Single Select), Internal Rating (Single Select), Submitted At (Date/Time), UTM Record (Linked Record), Contact (Linked Record) | | | |
| 9 | Requests: Status field has all 6 options: New, Contacted, Qualified, Proposal Sent, Booked, Closed Lost | | | |
| 10 | Requests: Internal Rating field has options: Warm, Hot, Cold | | | |
| 11 | Requests: Occasion field has all 6 options: Bachelorette, Birthday, Girls Trip, Celebration, Corporate, Other | | | |
| 12 | Requests: Experience Interest field has all 6 options: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom, Undecided | | | |
| 13 | UTMs table: all fields present including UTM Source, UTM Medium, UTM Campaign, UTM Content, UTM Term, Creative ID, Landing Page, Source URL, Referrer URL, First Seen At, Submitted At, Submission Page, Brand, Service Category | | | |
| 14 | Contacts table: Email field is the primary field. Email Subscribed (Checkbox), Source (Single Select), and Created At (Date/Time) are present | | | |
| 15 | Audit Log table: Timestamp, Action, Scenario ID, Related Record Type, Status, Error Message fields are present | | | |
| 16 | Linked Records: Requests.UTM Record links correctly to UTMs table | | | |
| 17 | Linked Records: Requests.Contact links correctly to Contacts table | | | |

### Views Created

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 18 | Requests: "New Requests" view exists, filtered to Status = New, sorted by Submitted At descending | | | |
| 19 | Requests: "Hot Leads" view exists, filtered to Internal Rating = Hot | | | |
| 20 | Contacts: "Email Subscribers" view exists, filtered to Email Subscribed = true | | | |
| 21 | Audit Log: "Recent Activity" view exists, sorted by Timestamp descending | | | |
| 22 | Audit Log: "Errors" view exists, filtered to Status = Error | | | |

---

## Section B: Make.com

### Scenario Status

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 23 | M-WEBFORM-REQUEST-CAPTURE scenario exists and is Active (toggle is ON) | | | |
| 24 | M-EMAIL-CAPTURE scenario exists and is Active | | | |
| 25 | M-INQUIRY-CONFIRMATION-EMAIL scenario exists and is Active | | | |
| 26 | M-SLACK-NEW-LEAD-ALERT scenario exists and is Active | | | |
| 27 | M-AIRTABLE-AUDIT-LOGGER scenario exists and is Active | | | |
| 28 | M-BRAND-ROUTER scenario exists and is Active | | | |
| 29 | M-CONCIERGE-ASSIGNMENT scenario exists and is Active | | | |

### Webhook URLs

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 30 | M-WEBFORM-REQUEST-CAPTURE webhook URL is pasted into the WordPress JS file at the correct location | | | |
| 31 | M-EMAIL-CAPTURE webhook URL is pasted into the WordPress JS file at the correct location | | | |
| 32 | Webhook URLs in the JS file are the correct Make.com URLs (not placeholders, not localhost) | | | |

### Deduplication

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 33 | Submit the Request to Book form twice with the same email address | | | |
| 34 | Confirm: two Request records are created (correct), but only ONE Contact record exists for that email | | | |
| 35 | Submit the email capture form twice with the same email address | | | |
| 36 | Confirm: only ONE Contact record exists (not two) with Email Subscribed = true | | | |

### Audit Log

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 37 | After a test form submission, Audit Log has a new record with Action = "form_submission" and Status = "Success" | | | |
| 38 | Audit Log entry includes the submitter's email in the Details field | | | |
| 39 | After an email capture submission, Audit Log has a new record with Action = "contact_created" or "contact_updated" | | | |

### Error Conditions

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 40 | In Make.com, "Store incomplete executions" is enabled on all scenarios | | | |
| 41 | Simulate an Airtable error (temporarily use a wrong field name in a module): verify the Audit Log receives an error entry and the scenario does not crash silently | | | |
| 42 | In Make.com, check that all scenarios have an error handler configured | | | |

### Test Record Cleanup

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 43 | All test records (with email containing "example.com" or "qa-") have been deleted from Requests, UTMs, Contacts, and Audit Log after testing | | | |
| 44 | No test data remains in the production Airtable base | | | |

---

## Sign-Off

All items above must be marked Pass before the backend is considered QA complete.

Signed: _____________________ Date: _____________________
