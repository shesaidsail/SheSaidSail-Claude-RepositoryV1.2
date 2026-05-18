# She Said Sail: Airtable Table Schema

Full schema for all 7 Airtable tables. Build them in the order listed. Tables that link to each other are noted; create the target table before creating the linking field.

---

## Table 1: Requests

**Primary Field:** Name (Short Text)
**Purpose:** Stores every inquiry submitted through the Request to Book form.

| Field Name | Field Type | Notes |
|---|---|---|
| Name | Short Text | Primary field. Full name from form. |
| Email | Email | From form. Required. |
| Phone | Phone | From form. Required. |
| Occasion | Single Select | Options: Bachelorette, Birthday, Girls Trip, Celebration, Corporate, Other |
| Group Size | Number | Integer. From form. |
| Preferred Date | Date | Date only (no time). ISO format. |
| Flexible Dates | Checkbox | True if user checked "I have flexible dates". |
| Experience Interest | Multiple Select | Options: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom, Undecided |
| Notes | Long Text | Free text message from form. |
| Status | Single Select | Options: New, Contacted, Qualified, Proposal Sent, Booked, Closed Lost. Default: New. |
| Internal Rating | Single Select | Options: Warm, Hot, Cold. Set by Make.com on create. |
| Submitted At | Date/Time | Set by Make.com. UTC. |
| Submission Page | Short Text | e.g., /request-to-book/ |
| Contact | Linked Record | Links to Contacts table. |
| UTM Record | Linked Record | Links to UTMs table. One-to-one per submission. |
| Assigned Concierge | Collaborator | Assigned team member for follow-up. |
| Follow-up Date | Date | Date concierge should follow up. |
| Internal Notes | Long Text | Internal team notes. Not visible to client. |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| New Requests | Status = New | Submitted At: descending |
| Hot Leads | Internal Rating = Hot | Submitted At: descending |
| Bachelorette Inquiries | Occasion = Bachelorette | Submitted At: descending |
| All Requests | None | Submitted At: descending |
| Unassigned | Assigned Concierge is empty | Submitted At: ascending |

---

## Table 2: Bookings

**Primary Field:** Booking ID (Auto Number)
**Purpose:** Stores confirmed bookings. Created manually or by Make.com when a Request moves to Booked status.

| Field Name | Field Type | Notes |
|---|---|---|
| Booking ID | Auto Number | Primary field. Auto-increments. |
| Request | Linked Record | Links to Requests table. The originating inquiry. |
| Contact | Linked Record | Links to Contacts table. |
| Experience | Single Select | Options: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom |
| Charter Date | Date | Confirmed date of charter. |
| Group Size | Number | Confirmed group size (may differ from inquiry). |
| Total Value | Currency | In USD. e.g., 10000 |
| Deposit Paid | Currency | Amount of deposit received. |
| Deposit Date | Date | Date deposit was received. |
| Balance Due | Formula | Total Value minus Deposit Paid. |
| Balance Due Date | Date | Date final payment is due. |
| Status | Single Select | Options: Deposit Received, Paid in Full, Cancelled, Refunded |
| Contract Signed | Checkbox | True when signed contract is on file. |
| Contract URL | URL | Link to signed contract (Google Drive or DocuSign). |
| Special Requests | Long Text | Dietary, decor, music, or other client requests. |
| Post-Charter Notes | Long Text | Team notes after the event. |
| Review Requested | Checkbox | True if review request email has been sent. |
| Review Received | Checkbox | True if client submitted a review. |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Upcoming Charters | Charter Date >= today | Charter Date: ascending |
| Awaiting Balance | Status = Deposit Received | Balance Due Date: ascending |
| This Month | Charter Date is within this month | Charter Date: ascending |
| All Bookings | None | Charter Date: descending |

---

## Table 3: Contacts

**Primary Field:** Email (Email type)
**Purpose:** One record per unique email address. Links to Requests and Bookings. Used for deduplication.

| Field Name | Field Type | Notes |
|---|---|---|
| Email | Email | Primary field. Unique. |
| Full Name | Short Text | From most recent form submission. |
| Phone | Phone | From most recent form submission. |
| Email Subscribed | Checkbox | True if they opted in via email capture form. |
| Source | Single Select | Options: request-to-book-form, email-capture-form, manual |
| Brand | Short Text | shesaidsail |
| UTM Source (first touch) | Short Text | utm_source from their first submission. |
| UTM Campaign (first touch) | Short Text | utm_campaign from their first submission. |
| Created At | Date/Time | When the Contact record was first created. |
| Last Seen At | Date/Time | Updated by Make.com on each subsequent submission. |
| Requests | Linked Record | All linked Request records for this contact. |
| Bookings | Linked Record | All linked Booking records for this contact. |
| Total Bookings | Count | Rollup: count of linked Booking records. |
| Lifetime Value | Rollup | Sum of Total Value from linked Bookings. |
| Tags | Multiple Select | Options: VIP, Repeat Client, Influencer, Press |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Email Subscribers | Email Subscribed = true | Created At: descending |
| All Contacts | None | Created At: descending |
| VIPs | Tags contains VIP | Last Seen At: descending |
| Repeat Clients | Total Bookings >= 2 | Lifetime Value: descending |

---

## Table 4: Campaigns

**Primary Field:** Campaign Name (Short Text)
**Purpose:** Reference table for tracking marketing campaigns. Linked to UTMs for reporting.

| Field Name | Field Type | Notes |
|---|---|---|
| Campaign Name | Short Text | Primary field. e.g., summer-2026-bachelorette |
| Platform | Single Select | Options: Meta, Google, TikTok, Email, Organic, Influencer, Other |
| Status | Single Select | Options: Active, Paused, Complete, Draft |
| Start Date | Date | Campaign start. |
| End Date | Date | Campaign end. |
| Budget | Currency | Total campaign budget in USD. |
| Objective | Single Select | Options: Awareness, Traffic, Lead Generation, Retargeting |
| UTM Source | Short Text | e.g., meta |
| UTM Medium | Short Text | e.g., cpc |
| UTM Campaign Slug | Short Text | Exact slug used in URLs. Must match utm_campaign param. |
| Creative IDs | Long Text | Comma-separated list of creative IDs used in this campaign. |
| Notes | Long Text | Campaign notes, target audience, creative direction. |
| UTM Records | Linked Record | Links to UTMs table. All UTM records from this campaign. |
| Total Inquiries | Count | Rollup: count of linked UTM records. |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Active Campaigns | Status = Active | Start Date: ascending |
| Meta Campaigns | Platform = Meta | Start Date: descending |
| All Campaigns | None | Start Date: descending |

---

## Table 5: UTMs

**Primary Field:** UTM ID (Formula: `utm_source & " / " & utm_campaign & " / " & submission_page`)
**Purpose:** One record per form submission. Stores all attribution data. Linked to Requests and Campaigns.

| Field Name | Field Type | Notes |
|---|---|---|
| UTM ID | Formula | Auto-generated label. |
| Request | Linked Record | The Request this UTM record belongs to. One-to-one. |
| Campaign | Linked Record | Links to Campaigns table (matched by utm_campaign slug). |
| UTM Source | Short Text | e.g., meta |
| UTM Medium | Short Text | e.g., cpc |
| UTM Campaign | Short Text | e.g., summer-2026-bachelorette |
| UTM Content | Short Text | e.g., video-reel-v4 |
| UTM Term | Short Text | Keyword; often empty for social. |
| Creative ID | Short Text | e.g., CRE-052 |
| Landing Page | URL | Full URL with query string. |
| Source URL | URL | Same as landing page on first touch. |
| Referrer URL | URL | document.referrer. May be blank for direct. |
| First Seen At | Date/Time | When user first arrived (from sessionStorage). |
| Submitted At | Date/Time | When form was submitted. Set by Make.com. |
| Submission Page | Short Text | e.g., /request-to-book/ |
| Brand | Short Text | shesaidsail |
| Service Category | Short Text | yacht-charter |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Meta Traffic | UTM Source = meta | Submitted At: descending |
| Organic Traffic | UTM Medium = organic | Submitted At: descending |
| All UTM Records | None | Submitted At: descending |

---

## Table 6: Client Notes

**Primary Field:** Note ID (Auto Number)
**Purpose:** Stores structured internal notes about contacts and bookings. Keeps the main tables clean.

| Field Name | Field Type | Notes |
|---|---|---|
| Note ID | Auto Number | Primary field. |
| Contact | Linked Record | Links to Contacts table. |
| Booking | Linked Record | Links to Bookings table. Optional. |
| Note Type | Single Select | Options: Call Log, Email Log, Internal Note, Client Preference, Issue, Follow-up |
| Note Date | Date/Time | When the note was created. |
| Created By | Collaborator | Team member who wrote the note. |
| Note | Long Text | The note content. |
| Action Required | Checkbox | True if this note requires a follow-up action. |
| Action Due Date | Date | When the action should be completed. |
| Action Completed | Checkbox | True when the action is done. |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Open Actions | Action Required = true AND Action Completed = false | Action Due Date: ascending |
| All Notes | None | Note Date: descending |
| Call Logs | Note Type = Call Log | Note Date: descending |

---

## Table 7: Audit Log

**Primary Field:** Log ID (Auto Number)
**Purpose:** Immutable record of all automated actions. Written by Make.com. Do not edit manually.

| Field Name | Field Type | Notes |
|---|---|---|
| Log ID | Auto Number | Primary field. |
| Timestamp | Date/Time | When the action occurred. UTC. |
| Action | Single Select | Options: form_submission, contact_created, contact_updated, email_sent, slack_alert_sent, status_changed, record_created, record_updated, error |
| Scenario ID | Short Text | Make.com scenario ID. e.g., M-WEBFORM-REQUEST-CAPTURE |
| Related Record Type | Single Select | Options: Request, Booking, Contact, UTM |
| Related Record ID | Short Text | Airtable record ID of the affected record. |
| Details | Long Text | Human-readable description of what happened. e.g., "New request created for jessica.moore@example.com (Bachelorette, group 11)" |
| Status | Single Select | Options: Success, Warning, Error |
| Error Message | Long Text | If Status = Error, the error details. Leave blank otherwise. |

### Views Required

| View Name | Filter | Sort |
|---|---|---|
| Recent Activity | None | Timestamp: descending (limit 50) |
| Errors | Status = Error | Timestamp: descending |
| Form Submissions | Action = form_submission | Timestamp: descending |
| Today | Timestamp is today | Timestamp: descending |
