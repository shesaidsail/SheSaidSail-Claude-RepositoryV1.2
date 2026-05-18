# Request Page Field Mapping
She Said Sail | Backend Readiness v2.0

---

## Airtable Table Target

**Base:** She Said Sail Operations
**Table:** Requests (or Inquiries)

---

## Field Mapping: Form to Airtable

| Form Field Name | Airtable Column | Type | Required | Notes |
|---|---|---|---|---|
| `occasion` | Occasion | Single Select | No | Birthday, Bachelorette, Girls Trip, Anniversary, Corporate, Day on the Water, Proposal, Other |
| `experience` | Experience Type | Single Select | Yes | rose, sunset, pinkpalm, monaco |
| `date` | Preferred Date | Date | Yes | Format: MM-DD-YYYY |
| `guests` | Guest Count | Number | Yes | Integer |
| `mf-listing-fname` | First Name | Single Line Text | Yes | |
| `last_name` | Last Name | Single Line Text | Yes | |
| `email` | Email | Email | Yes | |
| `phone` | Phone | Phone Number | Yes | |
| `budget_range` | Budget Range | Single Select | No | under-10k, 10k-15k, 15k-25k, 25k-40k, 40k-plus, flexible |
| `vision` | Vision Notes | Long Text | No | Freeform vision field |
| `mf-textarea` | Special Requests | Long Text | No | |
| `quoted_price` | Quoted Price | Currency | No | Auto-calculated from pricing engine |
| `base_price` | Base Price | Currency | No | Charter cost before add-ons |
| `addons_total` | Add-ons Total | Currency | No | |
| `addons_list` | Add-ons List | Long Text | No | Comma-separated add-on labels |
| `yacht_name` | Yacht Name | Single Line Text | No | |
| `yacht_slug` | Yacht Slug | Single Line Text | No | Internal slug |
| `brand` | Brand | Single Line Text | Yes | Always: she-said-sail |
| `service_category` | Service Category | Single Line Text | Yes | Always: private-yacht-charter |
| `form_version` | Form Version | Single Line Text | Yes | rtb-overhaul-v2 |

---

## UTM + Attribution Field Mapping

| Form Field Name | Airtable Column | Type |
|---|---|---|
| `utm_source` | UTM Source | Single Line Text |
| `utm_medium` | UTM Medium | Single Line Text |
| `utm_campaign` | UTM Campaign | Single Line Text |
| `utm_content` | UTM Content | Single Line Text |
| `utm_term` | UTM Term | Single Line Text |
| `creative_id` | Creative ID | Single Line Text |
| `landing_page` | Landing Page | URL |
| `source_url` | Source URL | URL |
| `referrer_url` | Referrer URL | URL |
| `first_seen_at` | First Seen At | Date Time |
| `submission_page` | Submission Page | Single Line Text |

---

## Airtable Automation Triggers

When a new record is created in Requests:

1. Route to M-CONCIERGE-ASSIGNMENT based on `service_category` and `brand`
2. Trigger M-WEBFORM-REQUEST-CAPTURE to normalize field values
3. Trigger M-UTM-CAPTURE to log attribution separately
4. Trigger M-BRAND-ROUTER to route to correct notification queue
5. Send confirmation email via M-LEAD-INTAKE with personalized concierge greeting

---

## Make.com Webhook Readiness

### Primary Webhook
**Scenario:** M-WEBFORM-REQUEST-CAPTURE
**Endpoint:** `https://hook.us1.make.com/sse-webform-request-capture`
**Method:** POST
**Content-Type:** application/json
**Payload:** Full form data object as JSON

### Secondary Webhooks
| Scenario | Trigger |
|---|---|
| M-UTM-CAPTURE | On every form submission, separately log UTM data |
| M-BRAND-ROUTER | Route to Slack and email based on brand field |
| M-CONCIERGE-ASSIGNMENT | Assign to concierge queue, send internal notification |
| M-LEAD-INTAKE | Send branded confirmation email to submitter |

---

## Hidden Field Injection Logic

All hidden fields are populated client-side on DOMContentLoaded via JavaScript:

- **UTM fields:** read from `window.location.search`
- **landing_page:** stored in `sessionStorage` on first page load, persisted across session
- **source_url:** `window.location.href` at moment of form load
- **referrer_url:** `document.referrer`
- **first_seen_at:** stored in `localStorage`, set on first ever site visit
- **submission_page:** `window.location.pathname`
- **brand / service_category / form_version:** hardcoded static values

---

## Data Quality Notes

- `budget_range` is optional but highly valuable for lead qualification
- `vision` and `mf-textarea` are both optional to minimize form friction
- `quoted_price` reflects client-side MetForm pricing engine calculation
- If user submits from a yacht page or experience page, `yacht_name`, `yacht_slug`, and `experience` may already be pre-populated
