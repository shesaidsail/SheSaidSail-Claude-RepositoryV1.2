# She Said Sail: Form Tracking Specification
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

---

## PURPOSE

This document specifies every hidden field, UTM capture mechanism, and attribution logic
for the She Said Sail request-to-book form. Any developer implementing or wiring the form
must follow this exactly.

---

## FORM: REQUEST TO BOOK

**URL:** /request-to-book/
**Platform:** WordPress / MetForm (or replacement)
**Submission destination:** Make.com webhook (see make-webhook-spec.md)

---

## VISIBLE FORM FIELDS

| Field | Input Type | Required | Placeholder |
|---|---|---|---|
| Full Name | Text | Yes | Your name |
| Email Address | Email | Yes | Your email |
| Phone Number | Tel | No | Your phone (optional) |
| Occasion | Select | Yes | What are we celebrating? |
| Group Size | Number | Yes | Approx. how many guests? |
| Preferred Date | Date | No | Do you have a date in mind? |
| Flexible Dates | Checkbox | No | I am flexible on dates |
| Experience Interest | Multi-select | No | Which experience interests you? |
| Message | Textarea | No | Tell us a little about the occasion |

### Occasion Options

- Bachelorette
- Birthday
- Girls Trip
- Relationship Celebration
- Corporate / Team
- Other

### Experience Interest Options

- Monaco Social
- Golden Hour Escape
- Rose Day Club
- Pink Palm Club
- Not sure yet, show me everything

---

## HIDDEN TRACKING FIELDS

All hidden fields are populated by JavaScript before form submission.
They are not visible to the user and do not appear in the form UI.

| Field Name | Source | Notes |
|---|---|---|
| utm_source | URL parameter | e.g. meta, tiktok, google, instagram |
| utm_medium | URL parameter | e.g. cpc, social, organic, email |
| utm_campaign | URL parameter | e.g. summer-2026-bachelorette |
| utm_content | URL parameter | Ad creative set or audience segment |
| utm_term | URL parameter | Keyword (Google) or audience label (paid social) |
| creative_id | URL parameter | Custom field for ad creative tracking |
| landing_page | document.location.href | Full URL where form is displayed |
| source_url | document.location.href | Same as landing_page (preserved for analytics) |
| referrer_url | document.referrer | HTTP referrer at time of page load |
| first_seen_at | localStorage: sss_first_seen | Timestamp of first site visit |
| submission_page | document.location.pathname | Path only, e.g. /request-to-book/ |
| brand | Hardcoded: "shesaidsail" | Multi-brand routing field for Make.com |
| service_category | Hardcoded: "yacht-charter" | For future service type routing |

---

## UTM CAPTURE AND PRESERVATION LOGIC

### On First Page Load (Any Page)

```javascript
(function () {
  var params = new URLSearchParams(window.location.search);
  var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'creative_id'];
  var stored  = {};

  try {
    stored = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
  } catch (e) {}

  utmKeys.forEach(function (key) {
    if (params.get(key)) {
      stored[key] = params.get(key);
    }
  });

  try {
    sessionStorage.setItem('sss_utm', JSON.stringify(stored));
  } catch (e) {}

  /* First seen timestamp: write once to localStorage, never overwrite */
  try {
    if (!localStorage.getItem('sss_first_seen')) {
      localStorage.setItem('sss_first_seen', new Date().toISOString());
    }
  } catch (e) {}
})();
```

**Notes:**
- UTMs are stored in `sessionStorage` to persist across internal navigation within the session.
- They are NOT overwritten if the user navigates to a non-UTM URL within the same session.
- `first_seen_at` is written once to `localStorage` and never overwritten, so it always reflects the user's first-ever visit.

### On Form Page Load

```javascript
function populateHiddenFields() {
  var utm = {};
  try {
    utm = JSON.parse(sessionStorage.getItem('sss_utm') || '{}');
  } catch (e) {}

  var fields = {
    utm_source:      utm.utm_source      || '',
    utm_medium:      utm.utm_medium      || '',
    utm_campaign:    utm.utm_campaign    || '',
    utm_content:     utm.utm_content     || '',
    utm_term:        utm.utm_term        || '',
    creative_id:     utm.creative_id     || '',
    landing_page:    window.location.href,
    source_url:      window.location.href,
    referrer_url:    document.referrer   || '',
    first_seen_at:   '',
    submission_page: window.location.pathname,
    brand:           'shesaidsail',
    service_category: 'yacht-charter'
  };

  try {
    fields.first_seen_at = localStorage.getItem('sss_first_seen') || '';
  } catch (e) {}

  Object.keys(fields).forEach(function (name) {
    var input = document.querySelector('input[name="' + name + '"]');
    if (input) input.value = fields[name];
  });
}
```

---

## ATTRIBUTION LOGIC BY TRAFFIC SOURCE

### Meta Ads

UTM parameters set in Meta Business Manager campaign UTM settings:
- utm_source: `meta`
- utm_medium: `cpc`
- utm_campaign: `{campaign.name}` (dynamic)
- utm_content: `{adset.name}` (dynamic)
- creative_id: custom label set per ad creative

### TikTok Ads

UTM parameters set in TikTok Ads Manager:
- utm_source: `tiktok`
- utm_medium: `cpc`
- utm_campaign: `{campaign_name}` (dynamic)
- utm_content: `{adgroup_name}` (dynamic)
- creative_id: custom label per creative

### Google Search (Paid)

UTM parameters via Google Ads auto-tagging or manual UTM:
- utm_source: `google`
- utm_medium: `cpc`
- utm_campaign: campaign name
- utm_term: `{keyword}` (auto-populated by ValueTrack)

### Google Organic

No UTMs. Detected in Make.com by:
- utm_source is empty
- referrer_url contains `google.com`

### Instagram Organic (Link in Bio)

UTM parameters set on the link-in-bio URL:
- utm_source: `instagram`
- utm_medium: `organic`
- utm_campaign: `link-in-bio`

### TikTok Organic (Link in Bio)

UTM parameters set on the link-in-bio URL:
- utm_source: `tiktok`
- utm_medium: `organic`
- utm_campaign: `link-in-bio`

### Direct Traffic

No UTMs. Detected in Make.com by:
- utm_source is empty
- referrer_url is empty

### Email (Newsletter or Automation)

UTM parameters set in email platform (Klaviyo/Mailchimp):
- utm_source: `email`
- utm_medium: `email`
- utm_campaign: email flow or broadcast name

### Referral

No UTMs typically. Detected by:
- utm_source is empty
- referrer_url is present and not a search engine

---

## FORM SUBMISSION PAYLOAD

The webhook payload sent to Make.com on submission. All fields sent as a flat JSON object.

```json
{
  "full_name": "Jane Doe",
  "email": "jane@example.com",
  "phone": "+13051234567",
  "occasion": "Bachelorette",
  "group_size": 12,
  "preferred_date": "2026-07-18",
  "flexible_dates": false,
  "experience_interest": ["Monaco Social", "Golden Hour Escape"],
  "message": "My best friend is getting married in August and we want to surprise her.",
  "utm_source": "meta",
  "utm_medium": "cpc",
  "utm_campaign": "summer-2026-bachelorette",
  "utm_content": "video-reel-v3",
  "utm_term": "",
  "creative_id": "CRE-047",
  "landing_page": "https://shesaidsail.com/request-to-book/?utm_source=meta&utm_medium=cpc&utm_campaign=summer-2026-bachelorette",
  "source_url": "https://shesaidsail.com/request-to-book/?utm_source=meta&utm_medium=cpc&utm_campaign=summer-2026-bachelorette",
  "referrer_url": "https://www.instagram.com/",
  "first_seen_at": "2026-05-15T14:32:00.000Z",
  "submission_page": "/request-to-book/",
  "brand": "shesaidsail",
  "service_category": "yacht-charter"
}
```

---

## DEDUPLICATION RULES

Applied in Make.com before creating Airtable records:

1. Search Contacts table for matching email address
2. If found: link new Request to existing Contact (do not create duplicate Contact)
3. If not found: create new Contact, then create Request linked to it
4. Always create a new Request record (requests are never deduplicated)
5. Always create a new UTM record linked to the Request

---

## EMAIL CAPTURE FORM (HOMEPAGE)

The email capture section on the homepage collects only email address.
It is a lighter-touch conversion step for visitors not ready to book.

### Fields

| Field Name | Source | Notes |
|---|---|---|
| email | User input | Required |
| utm_source | sessionStorage | Same logic as request form |
| utm_medium | sessionStorage | |
| utm_campaign | sessionStorage | |
| landing_page | document.location.href | Always the homepage |
| first_seen_at | localStorage | |
| brand | Hardcoded | "shesaidsail" |
| service_category | Hardcoded | "yacht-charter" |

### Submission Destination

Make.com webhook for email capture:
- Creates or updates Contact record (opt-in flag: email_subscribed = true)
- Adds subscriber to Klaviyo/Mailchimp list
- Does NOT create a Request record (no booking intent signal yet)

---

## TESTING INSTRUCTIONS

Before going live, submit a test form with these UTM parameters:
`?utm_source=test&utm_medium=test&utm_campaign=form-test&creative_id=TEST-001`

Verify in Airtable:
- [ ] Request record created
- [ ] Contact record created (or linked if email already exists)
- [ ] UTM record created with all 5 UTM fields populated
- [ ] landing_page field shows full URL including query string
- [ ] referrer_url field is populated (or empty if navigated directly)
- [ ] first_seen_at field is populated
- [ ] brand = "shesaidsail"
- [ ] service_category = "yacht-charter"

Submit the same email a second time:
- [ ] New Request record created
- [ ] No duplicate Contact record created (linked to existing Contact instead)
