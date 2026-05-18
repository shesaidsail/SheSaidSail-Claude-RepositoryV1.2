# Rose Day Club: Backend Integration Notes

Page: /experience/rose-day-club/
CTA Destination: /request-to-book/?selected_experience=rose-day-club

---

## Airtable Mapping

**Table:** Requests

All 13 standard hidden fields are populated automatically by global JS on page load and form submission. No custom configuration required for this page beyond the values below.

### Hidden Field Values for This Experience

| Field | Value |
|---|---|
| brand | shesaidsail |
| service_category | yacht-charter |
| selected_experience | rose-day-club |
| source_page | /experience/rose-day-club/ |
| source_slug | rose-day-club |
| cta_destination | /request-to-book/?selected_experience=rose-day-club |
| page_type | experience |
| site_section | experiences |
| brand_vertical | yacht-charter |
| form_version | global-v1 |
| submission_channel | web |
| referral_source | (populated dynamically from UTM or referrer) |
| session_id | (populated dynamically by global JS) |

The `selected_experience` field value `rose-day-club` is pre-populated via the URL parameter on the request-to-book page. No additional mapping needed.

---

## Form Setup: MetForm or WPForms

**Method:** Same as Monaco Social install guide, Step 7.

The `selected_experience` hidden field on the /request-to-book/ form reads from the URL query parameter `?selected_experience=` on page load.

When the user arrives at `/request-to-book/?selected_experience=rose-day-club`, the form field auto-populates with `rose-day-club` before any user input.

No changes to the form structure are required. Confirm the hidden field is named exactly `selected_experience` and that the global JS reads the parameter correctly on the RTB page.

**Verification step:** Load `/request-to-book/?selected_experience=rose-day-club` in a browser. Inspect the hidden input field. Confirm value = `rose-day-club`.

---

## Make.com Routing

**Scenario:** M-BRAND-ROUTER

The router reads the `selected_experience` field value from the Airtable Requests record on trigger.

When `selected_experience` = `rose-day-club`, the router follows the She Said Sail branch (same branch as all other shesaidsail experience submissions).

No new tables are required. No new Make.com scenarios are required. No new routing rules are required.

The existing She Said Sail flow handles all experience slugs under the shesaidsail brand. Rose Day Club routes identically to other experiences in the same brand.

---

## Confirmation Behavior

The confirmation page or confirmation message shown after submission does not need experience-specific customization. The global thank-you state covers this.

If a custom confirmation is desired in a future iteration, pass `selected_experience=rose-day-club` as a query parameter to the confirmation URL and use it to surface experience-specific copy.

---

## No New Infrastructure Required

- No new Airtable tables
- No new Airtable fields
- No new Make.com scenarios
- No new form configurations
- No new webhook endpoints

All existing global infrastructure covers this experience.
