# SHE SAID SAIL — MASTER BACKEND SYSTEM
Version: 1.0 | Status: PRODUCTION | Owner: Will Hunt

---

## WEBHOOK ARCHITECTURE

All Webflow form submissions route to:
`SSS_LEAD_INTAKE_HOOK` (Make.com — SSS-LEAD-INTAKE scenario)

The webhook fires to Make, which:
1. Checks for duplicate leads (idempotency)
2. Creates an Airtable Request record
3. Sends branded confirmation email via Gmail
4. Posts Slack alert to #sss-ops-alerts
5. Logs the action in the Audit Logger

---

## REQUIRED FORM FIELDS (ALL PAGES)

The following fields must exist on every inquiry form and map to the webhook payload:

| Field Name (webhook key) | Form Label | Type | Required |
|--------------------------|-----------|------|---------|
| `first_name` | First Name | text | Yes |
| `last_name` | Last Name | text | Yes |
| `email` | Email | email | Yes |
| `phone` | Phone | tel | Yes |
| `experience` | Experience / Package | text/select | Yes |
| `yacht` | Preferred Vessel | text/select | No |
| `preferred_date` | Preferred Date | date | Yes |
| `duration` | Duration | text/select | Yes |
| `guest_count` | Number of Guests | number | Yes |
| `occasion` | Occasion | text/select | Yes |
| `city` | City | text/select | Yes |
| `boarding_location` | Boarding Location | text/select | No |
| `add_ons` | Add-Ons Selected | text | No |
| `special_requests` | Special Requests / Notes | textarea | No |
| `source_url` | (hidden field) | hidden | Yes |
| `utm_source` | (hidden field) | hidden | No |
| `utm_medium` | (hidden field) | hidden | No |
| `utm_campaign` | (hidden field) | hidden | No |
| `page_slug` | (hidden field) | hidden | No |

---

## HIDDEN FIELDS (MANDATORY)

Every form must include these hidden fields:

```html
<input type="hidden" name="source_url" id="source_url">
<input type="hidden" name="utm_source" id="utm_source">
<input type="hidden" name="utm_medium" id="utm_medium">
<input type="hidden" name="utm_campaign" id="utm_campaign">
<input type="hidden" name="utm_content" id="utm_content">
<input type="hidden" name="utm_term" id="utm_term">
<input type="hidden" name="page_slug" id="page_slug">
<input type="hidden" name="referrer" id="referrer">
```

These must be populated via JS before submission.

---

## HIDDEN FIELD POPULATION SCRIPT

```javascript
(function() {
  function getParam(key) {
    var params = new URLSearchParams(window.location.search);
    return params.get(key) || '';
  }
  document.getElementById('source_url').value = window.location.href;
  document.getElementById('utm_source').value = getParam('utm_source');
  document.getElementById('utm_medium').value = getParam('utm_medium');
  document.getElementById('utm_campaign').value = getParam('utm_campaign');
  document.getElementById('utm_content').value = getParam('utm_content');
  document.getElementById('utm_term').value = getParam('utm_term');
  document.getElementById('page_slug').value = window.location.pathname;
  document.getElementById('referrer').value = document.referrer;
})();
```

---

## AIRTABLE FIELD MAPPING

Webhook fields map to Airtable Requests table (tblTlSB9CO4dTGodg):

| Webhook Key | Airtable Field | Notes |
|-------------|---------------|-------|
| `first_name` | First Name | |
| `last_name` | Last Name | |
| `email` | Email | |
| `phone` | Phone | |
| `experience` | Experience | Populated from hidden field or form select |
| `yacht` | Yacht | |
| `preferred_date` | Preferred Date | ISO date string YYYY-MM-DD |
| `duration` | Duration | |
| `guest_count` | Guest Count | Number |
| `occasion` | Occasion | |
| `city` | City | Auto-detect from source_url when possible |
| `boarding_location` | Boarding Location | |
| `add_ons` | Add-Ons Selected | Comma-separated string |
| `special_requests` | Special Requests | |
| `source_url` | (used for brand routing) | SSS vs ME detection |
| `utm_source` | UTM_Source | Write to Requests table |
| `utm_medium` | UTM_Medium | Write to Requests table |
| `utm_campaign` | UTM_Campaign | Write to Requests table |

---

## EXPERIENCE FIELD PRE-POPULATION

Each experience page must pre-populate the `experience` field with its page-specific value so operators can identify the inquiry source.

Golden Hour Escape: `experience = "Golden Hour Escape"`

Use a hidden field or read-only visible field:
```html
<input type="hidden" name="experience" value="Golden Hour Escape">
```

---

## MAKE.COM SCENARIO DEPENDENCIES

| Scenario | Trigger | Depends On |
|---------|---------|-----------|
| SSS-LEAD-INTAKE | Webflow webhook | SSS-AUDIT-LOGGER, SSS-SLACK-ALERTS |
| SSS-BRAND-ROUTER | Webhook | None |
| SSS-BOOKING-CREATION | Airtable (Request status change) | SSS-AUDIT-LOGGER |
| SSS-BOOKING-CONFIRMATION | Airtable (Booking created) | SSS-CONCIERGE-ASSIGNMENT |

---

## NAMING CONVENTIONS

### Form IDs (Webflow)
Pattern: `sss-[page-slug]-inquiry`
Example: `sss-golden-hour-escape-inquiry`

### Hidden Field IDs
Pattern: `sss_[field_name]`
Example: `sss_utm_source`

### GTM Event Names
Pattern: `sss_[action]_[object]`
Examples:
- `sss_form_submit`
- `sss_form_start`
- `sss_cta_click`
- `sss_scroll_depth`
- `sss_section_view`

### GTM Data Layer Keys
- `event_category`: page category (experience, homepage, etc.)
- `event_action`: user action
- `event_label`: specific element or value
- `experience_name`: e.g., "Golden Hour Escape"
- `page_slug`: URL path
- `form_id`: form identifier

---

## AIRTABLE BASE REFERENCE

| Base | ID |
|------|-----|
| SSS Operations | appdZ49WqgjRXxA1R |
| SSS Financials | apprDKQtV2GInThwE |

| Table | ID |
|-------|-----|
| Requests | tblTlSB9CO4dTGodg |
| Bookings | tbl72omPibBkn2hZL |
| Clients | tblr84vRIWC5HmKvo |
| Audit Log | tblrMpTfMk8q1eNHp |
