# She Said Sail: Master Backend System

**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul
**Last Updated:** 2026-05-18

---

## 1. BACKEND STACK OVERVIEW

Every page on the She Said Sail website connects to the same data infrastructure. The stack below is the permanent standard. No new page, form, or integration should bypass any layer.

| Component | Tool | Purpose |
|---|---|---|
| Database | Airtable | Stores all requests, bookings, contacts, campaigns, UTMs, notes, audit log |
| Automation | Make.com | Routes form submissions, sends emails, fires Slack alerts, writes audit log |
| Forms | WordPress / MetForm | Collects lead data on /request-to-book/ and email capture sections |
| Email | Klaviyo or Mailchimp | Guest confirmation, nurture sequence |
| Chat | Tidio | Live support |

---

## 2. AIRTABLE NAMING CONVENTIONS

Consistent naming ensures anyone on the team can read, filter, and extend the database without a briefing.

**Tables:** Title Case with no abbreviations.
- Correct: Requests, Contacts, Bookings, Campaigns, UTMs, Audit Log
- Incorrect: req, REQS, tbl_requests, requests_v2

**Fields:** Title Case, descriptive, no abbreviations.
- Correct: UTM Source, UTM Medium, UTM Campaign, Guest Count, Preferred Date
- Incorrect: src, utm_src, Guests, PrefDate

**Views:** Descriptive with filter context included in the name.
- Correct: New Requests, Hot Leads This Week, Upcoming Bookings, All Contacts
- Incorrect: View 1, Filter A, New

**Formula fields:** Named for what they calculate.
- Correct: Balance Due, Days Until Event, Lead Score
- Incorrect: Formula, Calc, F1

**Linked fields:** Named with the linked table.
- Correct: Linked Request, Linked Contact, Linked Campaign
- Incorrect: Link, Ref, ID

### Prohibited Naming Patterns

The following patterns are never used in Airtable field or table names:

- Single-letter fields: no "A", "B", "C"
- Numbered fields: no "Field 1", "Field 2", "Col 3"
- Unclear abbreviations: no "ut_src", "camp_id", "bk_dt"
- CamelCase: use Title Case for Airtable fields; use snake_case only for hidden form inputs and sessionStorage keys

---

## 3. HIDDEN FIELD NAMING CONVENTION

All hidden tracking fields in forms use snake_case. This matches the sessionStorage keys and the Airtable field names exactly so that data flows without transformation.

### Standard 13 Tracking Fields (required on every form)

These 13 fields are present on every form on the site, without exception:

```
utm_source
utm_medium
utm_campaign
utm_content
utm_term
creative_id
landing_page
source_url
referrer_url
first_seen_at
submission_page
brand
service_category
```

### Additional Page-Specific Fields (snake_case)

These fields are added to forms where the data is relevant:

```
selected_experience
occasion
preferred_date
guest_count
budget_range
first_name
last_name
email
phone
notes
```

**Rule:** Any new hidden field always uses snake_case to match the sessionStorage keys and Airtable field names. There are no exceptions to this convention.

---

## 4. UTM CAPTURE STANDARDS

### Attribution Model

First-touch attribution is the standard. UTM parameters from the first page the visitor lands on are preserved for the entire session. If the visitor navigates away and returns without UTMs in the URL, the original UTMs remain in sessionStorage and are submitted with any form.

### Storage Keys

- **Session storage key:** `sss_utm` stored as a JSON object containing all UTM and tracking parameters
- **Local storage key:** `sss_first_seen` stores the ISO timestamp of the visitor's first arrival

### Required UTM Parameters

Every paid campaign must include at minimum:
- `utm_source`
- `utm_medium`
- `utm_campaign`

### Optional UTM Parameters

- `utm_content`: identifies the creative variant or ad copy
- `utm_term`: keyword for search campaigns
- `creative_id`: internal ad ID for cross-referencing with ad platform reporting

### Platform Conventions

Consistent UTM values across platforms allow clean segmentation in GA4 and Airtable.

| Platform | utm_source | utm_medium | utm_campaign |
|---|---|---|---|
| Meta Ads | meta | cpc | [campaign name] |
| TikTok Ads | tiktok | cpc | [campaign name] |
| Instagram organic | instagram | organic | link-in-bio |
| TikTok organic | tiktok | organic | link-in-bio |
| Google Search | google | cpc | [campaign name] |
| Email newsletter | email | newsletter | [send name] |
| Direct referral | referral | partner | [partner name] |

---

## 5. MAKE.COM WEBHOOK NAMING CONVENTION

### Scenario ID Format

```
M-[FUNCTION]-[NUMBER]
```

The scenario name uses UPPERCASE WITH HYPHENS and describes the scenario action precisely.

### Existing Scenarios

| Scenario ID | Scenario Name | Description |
|---|---|---|
| M-WEBFORM-001 | REQUEST-CAPTURE | Receives booking form submissions from /request-to-book/ |
| M-UTM-001 | UTM-CAPTURE | Processes and stores UTM data from form submissions |
| M-ROUTER-001 | BRAND-ROUTER | Routes requests by brand or experience type |
| M-CONCIERGE-001 | CONCIERGE-ASSIGNMENT | Assigns a concierge to each new request |
| M-EMAIL-001 | INQUIRY-CONFIRMATION | Sends confirmation email to form submitter |
| M-SLACK-001 | SLACK-NEW-LEAD-ALERT | Posts new lead alert to Slack #new-leads channel |
| M-AUDIT-001 | AIRTABLE-AUDIT-LOGGER | Writes every automation action to the Audit Log |
| M-EMAILCAP-001 | EMAIL-CAPTURE | Handles email capture form submissions |

### Numbering for New Scenarios

When adding a new scenario, use the next available number in its function category:
- Next web form scenario: M-WEBFORM-002
- Next UTM scenario: M-UTM-002
- Next email scenario: M-EMAIL-002
- Next Slack scenario: M-SLACK-002

New function categories follow the same ID format with a new function prefix.

---

## 6. GTM EVENT NAMING CONVENTION

### Format

All custom events use snake_case: `[action]_[object]`

All event names are lowercase with underscores. No camelCase. No hyphens.

### Existing Events

| Event Name | Fires When |
|---|---|
| view_homepage | Visitor loads / |
| view_request_page | Visitor loads /request-to-book/ |
| view_experiences_page | Visitor loads /experiences/ |
| view_thank_you_page | Visitor loads /thank-you/ |
| click_request_to_book | Any "Request to Book" CTA is clicked |
| click_explore_experiences | Any "Explore Experiences" CTA is clicked |
| click_experience_card | A card on the experiences page is clicked |
| start_booking_form | First interaction with the booking form |
| submit_booking_form | Booking form is successfully submitted |
| submit_email_capture | Email capture form is submitted |
| click_phone | Phone number link is clicked |
| open_chat | Tidio chat widget is opened |
| scroll_50_percent | Visitor scrolls 50% down the page |
| scroll_90_percent | Visitor scrolls 90% down the page |

### Naming Rules for New Events

- New page views: `view_[page_name]` (e.g. `view_about_page`, `view_faq_page`)
- New clicks: `click_[element_name]` (e.g. `click_share_button`, `click_gallery_image`)
- New form start events: `start_[form_name]_form` (e.g. `start_contact_form`)
- New form submit events: `submit_[form_name]_form` (e.g. `submit_contact_form`)
- New content interactions: `view_[content_type]` or `click_[content_type]` (e.g. `click_testimonial_card`)

### Data Layer Variable Names

All custom Data Layer Variables in GTM use the prefix `dlv_`:
- `dlv_experience_name`
- `dlv_occasion`
- `dlv_guest_count`
- `dlv_form_name`

---

## 7. FORM MAPPING RULES

Every new form on the site must satisfy all of the following before going live:

1. The form contains all 13 standard hidden tracking fields listed in Section 3
2. A Make.com webhook URL is configured as the form submission action
3. The submission creates a record in the Requests table (or an appropriate dedicated Airtable table for non-inquiry forms)
4. The submission creates a linked UTM record in the UTMs table
5. A confirmation email is sent to the submitter within 2 minutes
6. A Slack alert fires to the appropriate channel (default: #new-leads)
7. An entry is written to the Audit Log

### Table Routing by Form Type

| Form Type | Target Airtable Table |
|---|---|
| Booking inquiry | Requests |
| Email capture | Contacts (email only record) |
| Supplier inquiry | Suppliers (separate table) |
| Press inquiry | Press (separate table) |
| Gift inquiry | Requests (with occasion = Gift) |

Forms with a fundamentally different purpose create records in a new or dedicated Airtable table. They do not go into the Requests table.

---

## 8. DEDUPLICATION RULES

**Contacts:** Deduplicated on email address. One Contact record per email address. Make.com searches the Contacts table for the submitted email before creating a new Contact. If a match is found, the existing Contact is linked to the new Request instead.

**Requests:** Never deduplicated. One Request record per form submission. A person may submit multiple requests and each one is tracked independently.

**UTMs:** One UTM record per form submission. Each UTM record is linked to its parent Request.

**Duplicate detection flow in Make.com:**
1. Receive form submission
2. Search Contacts for matching email
3. If match: link existing Contact to new Request
4. If no match: create new Contact, then link to new Request
5. Always create a new Request record regardless of Contact match

---

## 9. ANALYTICS STANDARDS

Every new page published on the site must include:

- A page view event pushed to the dataLayer on page load:
  ```javascript
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'view_[pagename]',
    page_location: window.location.href
  });
  ```
- At least one CTA click event if the page has a call to action
- A form start event if the page has a form
- A form submit event if the page has a form

Events are fired by `she-said-sail-global.js` or a page-specific extension script that follows the same pattern. No inline `onclick` attributes. All events go through the dataLayer.

---

## 10. QA RULES FOR BACKEND

Before any new form goes live, all of the following must pass:

**Submission test:**
Submit a test using a URL with UTM parameters:
```
?utm_source=test&utm_medium=test&utm_campaign=qa-[date]
```

**Verification checklist:**

- [ ] Airtable: Request record created with all UTM fields populated and non-empty
- [ ] Make.com: scenario executed without error (check execution log)
- [ ] Email: confirmation email received within 2 minutes
- [ ] Slack: alert posted to #new-leads
- [ ] Audit Log: entry created with correct timestamp and scenario ID

**Deduplication test:**

- [ ] Submit the same email address a second time
- [ ] Verify that no duplicate Contact record is created
- [ ] Verify that a new Request record is created (requests are never deduplicated)

**Cleanup:**

After QA is confirmed, delete all test records from Airtable. Do not leave test data in the production base.
