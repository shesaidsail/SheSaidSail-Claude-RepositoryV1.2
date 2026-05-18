# She Said Sail: Backend Readiness Plan
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

---

## OVERVIEW

This document maps every form field, data point, and operational record to its Airtable destination.
It is the single source of truth for backend integration before launch.

Stack: WordPress/Elementor (frontend) > Make.com (automation) > Airtable (database)

---

## AIRTABLE BASE STRUCTURE

Base name: **She Said Sail Operations**

### Tables

| Table | Primary Purpose |
|---|---|
| Requests | Every inbound inquiry, pre-qualified |
| Bookings | Confirmed and in-progress bookings |
| Contacts | All leads and guests, deduplicated |
| Campaigns | Active paid and organic campaigns |
| UTMs | Raw UTM attribution data per submission |
| Client Notes | Internal notes, concierge log entries |
| Audit Log | Record of all system actions |

---

## TABLE 1: REQUESTS

Captures every homepage form submission and inquiry.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Request ID | Auto Number | Primary identifier. Format: REQ-0001 |
| Status | Single Select | New, Contacted, Qualified, Declined, Converted |
| Name | Short Text | From form: full name |
| Email | Email | From form: email address |
| Phone | Phone | From form: phone number (optional) |
| Occasion | Single Select | Bachelorette, Birthday, Girls Trip, Celebration, Corporate, Other |
| Group Size | Number | From form: estimated headcount |
| Preferred Date | Date | From form: flexible date field |
| Flexible Dates | Checkbox | Checked if no hard date requirement |
| Notes | Long Text | From form: freeform message |
| Experience Interest | Multiple Select | Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom, Undecided |
| Budget Range | Single Select | Under $5k, $5k to $10k, $10k to $15k, $15k+, Undisclosed |
| Submitted At | Date/Time | Timestamp from Make.com at capture |
| Source | Single Select | Meta Ads, TikTok Ads, Google, Instagram Organic, TikTok Organic, Referral, Direct, Other |
| UTM Source | Short Text | Raw utm_source value |
| UTM Medium | Short Text | Raw utm_medium value |
| UTM Campaign | Short Text | Raw utm_campaign value |
| UTM Content | Short Text | Raw utm_content value |
| UTM Term | Short Text | Raw utm_term value |
| Creative ID | Short Text | Ad creative identifier for attribution |
| Landing Page | URL | Full URL of page where form was submitted |
| Referrer URL | URL | HTTP referrer at time of submission |
| First Seen At | Date/Time | Timestamp of first site visit (from cookie/localStorage) |
| Assigned To | Linked Record | Link to team member (from Contacts or Users table) |
| Linked Booking | Linked Record | Link to Bookings table if converted |
| Follow Up Date | Date | Scheduled follow-up date |
| Internal Rating | Single Select | Hot, Warm, Cold |
| Do Not Contact | Checkbox | Opt-out flag |

---

## TABLE 2: BOOKINGS

Tracks all confirmed bookings from deposit to completion.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Booking ID | Auto Number | Format: BKG-0001 |
| Status | Single Select | Deposit Received, Confirmed, In Progress, Complete, Cancelled, Refunded |
| Linked Request | Linked Record | Source request that converted |
| Client Name | Short Text | Primary contact name |
| Client Email | Email | Primary contact email |
| Client Phone | Phone | Primary contact phone |
| Experience | Single Select | Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom |
| Guest Count | Number | Final confirmed headcount |
| Event Date | Date | Confirmed date of experience |
| Departure Time | Short Text | e.g. "3:00 PM" |
| Departure Location | Short Text | Marina/dock name |
| Total Value | Currency | Final contracted price |
| Deposit Amount | Currency | Deposit received |
| Deposit Date | Date | Date deposit cleared |
| Balance Due | Formula | Total Value minus Deposit Amount |
| Balance Due Date | Date | When remaining balance is due |
| Contract Signed | Checkbox | Contract executed |
| Contract Date | Date | Date contract signed |
| Add-Ons | Multiple Select | Catering, Photography, Florals, Custom Playlist, Extra Hours |
| Crew Lead | Short Text | Assigned crew member |
| Captain | Short Text | Assigned captain |
| Internal Notes | Long Text | Operational notes |
| Post-Event Survey Sent | Checkbox | Survey dispatched after event |
| Testimonial Received | Checkbox | Guest submitted a review |
| Testimonial Text | Long Text | Verbatim guest quote |
| Testimonial Permission | Checkbox | Guest approved use |

---

## TABLE 3: CONTACTS

Deduplicated record of all people who have interacted with She Said Sail.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Contact ID | Auto Number | Format: CON-0001 |
| Full Name | Short Text | |
| Email | Email | Unique identifier. Deduplicate on this. |
| Phone | Phone | |
| Type | Single Select | Lead, Guest, Repeat Guest, Partner, Press, Internal |
| Source | Single Select | Web Form, Email Capture, Referral, Manual Entry, Tidio Chat |
| Requests | Linked Record | All linked request records |
| Bookings | Linked Record | All linked booking records |
| Email Subscribed | Checkbox | Opted in to email list |
| Email Subscribed At | Date/Time | |
| Email Platform ID | Short Text | Klaviyo/Mailchimp subscriber ID |
| Tags | Multiple Select | VIP, Bachelorette, Birthday, Girls Trip, Repeat, High-Value |
| Last Contacted | Date | Most recent outreach date |
| Created At | Date/Time | Record creation timestamp |
| Notes | Long Text | |

---

## TABLE 4: CAMPAIGNS

Tracks all active marketing campaigns for attribution reporting.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Campaign ID | Short Text | Matches utm_campaign value |
| Campaign Name | Short Text | Human-readable name |
| Platform | Single Select | Meta, TikTok, Google, Email, Organic, Influencer |
| Status | Single Select | Active, Paused, Completed, Draft |
| Start Date | Date | |
| End Date | Date | |
| Budget | Currency | Total allocated budget |
| Spend To Date | Currency | Updated manually or via API |
| Leads Generated | Count | Linked from Requests table |
| Bookings Generated | Count | Linked from Bookings table |
| Revenue Attributed | Rollup | Sum of booking values linked to campaign |
| Cost Per Lead | Formula | Budget divided by Leads Generated |
| Creative IDs | Long Text | Comma-separated list of creative_id values |
| Notes | Long Text | |

---

## TABLE 5: UTMS

Raw UTM data record per form submission. One row per submission.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| UTM ID | Auto Number | Format: UTM-0001 |
| Linked Request | Linked Record | |
| utm_source | Short Text | e.g. meta, tiktok, google, instagram |
| utm_medium | Short Text | e.g. cpc, social, email, organic |
| utm_campaign | Short Text | e.g. summer-2026-bachelorette |
| utm_content | Short Text | e.g. video-reel-v3 |
| utm_term | Short Text | e.g. miami-bachelorette-yacht |
| creative_id | Short Text | Custom ad creative tracking ID |
| landing_page | URL | Page URL where form was submitted |
| referrer_url | URL | HTTP referrer |
| source_url | URL | Full URL with all query params preserved |
| first_seen_at | Date/Time | First visit timestamp |
| submission_at | Date/Time | Form submission timestamp |
| brand | Short Text | shesaidsail (multi-brand routing field) |
| service_category | Short Text | yacht-charter |

---

## TABLE 6: CLIENT NOTES

Timestamped log of every client communication and concierge action.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Note ID | Auto Number | |
| Linked Request | Linked Record | |
| Linked Booking | Linked Record | |
| Linked Contact | Linked Record | |
| Note Type | Single Select | Call, Email, Text, Internal, System, Follow-Up |
| Note | Long Text | |
| Created By | Short Text | Team member or "System" |
| Created At | Date/Time | |
| Follow Up Required | Checkbox | |
| Follow Up Date | Date | |

---

## TABLE 7: AUDIT LOG

System-generated record of all automated actions for debugging and compliance.

### Fields

| Field Name | Type | Notes |
|---|---|---|
| Log ID | Auto Number | |
| Event Type | Short Text | e.g. FORM_SUBMITTED, RECORD_CREATED, EMAIL_SENT |
| Linked Record Type | Single Select | Request, Booking, Contact, Campaign |
| Linked Record ID | Short Text | The ID of the affected record |
| Triggered By | Short Text | Make scenario name or "Manual" |
| Payload | Long Text | JSON snippet of the triggering data |
| Status | Single Select | Success, Error, Skipped |
| Error Message | Short Text | If Status is Error |
| Timestamp | Date/Time | |

---

## MAKE.COM CONNECTIONS

Make.com watches the WordPress webhook for new form submissions and routes data:

1. Receives webhook payload from the form
2. Creates or updates Contact record in Airtable (deduplicate on email)
3. Creates new Request record, linked to Contact
4. Creates UTM record, linked to Request
5. Triggers confirmation email via email platform
6. Posts Slack alert to #new-leads channel
7. Logs action in Audit Log table

See `docs/backend/make-webhook-spec.md` for full scenario specifications.

---

## AIRTABLE VIEWS REQUIRED

### Requests Table Views

| View Name | Filter | Sort | Purpose |
|---|---|---|---|
| New Requests | Status = New | Submitted At desc | Daily triage |
| Hot Leads | Internal Rating = Hot | Submitted At desc | Priority follow-up |
| This Week | Submitted At is this week | Submitted At desc | Weekly report |
| All Requests | None | Submitted At desc | Full history |
| By Campaign | Group by UTM Campaign | Submitted At desc | Attribution reporting |

### Bookings Table Views

| View Name | Filter | Sort | Purpose |
|---|---|---|---|
| Upcoming | Event Date is in next 60 days | Event Date asc | Operations |
| Awaiting Balance | Balance Due > 0, Status = Confirmed | Balance Due Date asc | Finance |
| Complete | Status = Complete | Event Date desc | History |
| Testimonials | Testimonial Received = true | Event Date desc | Content pipeline |

---

## LAUNCH CHECKLIST: BACKEND

- [ ] Airtable base created with all 7 tables
- [ ] All fields created per specification above
- [ ] Make.com webhook scenarios created (see make-webhook-spec.md)
- [ ] Test submission received and verified in Airtable
- [ ] UTM field population verified on test submission
- [ ] Confirmation email sends on test submission
- [ ] Slack alert sends on test submission
- [ ] Audit Log records on test submission
- [ ] Duplicate detection tested (same email twice)
- [ ] Views created per specifications above
