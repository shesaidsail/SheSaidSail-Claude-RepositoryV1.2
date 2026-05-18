# Golden Hour Escape: Backend Integration Reference

**Page:** /experience/golden-hour-escape/
**Last updated:** 2026-05-18

---

## Airtable Mapping

**Table:** Requests

The following fields are populated when a visitor submits via the request-to-book form after arriving from this experience page.

| Field Name | Field Type | Value / Source |
|---|---|---|
| brand | Single line text | shesaidsail (hidden, pre-set) |
| service_category | Single line text | yacht-charter (hidden, pre-set) |
| selected_experience | Single line text | golden-hour-escape (hidden, pre-populated from URL param) |
| first_name | Single line text | Form input |
| last_name | Single line text | Form input |
| email | Email | Form input |
| phone | Phone number | Form input |
| preferred_date | Date | Form input |
| group_size | Number | Form input |
| message | Long text | Form input |
| submission_timestamp | Date and time | Auto via Make.com |
| source_url | URL | Auto via Make.com (captures referring page) |

No new Airtable tables are required. All submissions from this page route to the existing Requests table.

---

## Hidden Field Values

These three fields must be configured as hidden fields in the request-to-book form. They are pre-set constants for all submissions originating from this experience.

```
brand = "shesaidsail"
service_category = "yacht-charter"
selected_experience = "golden-hour-escape"
```

The `selected_experience` value is delivered via URL parameter on the CTA link. The form reads and pre-populates from this parameter on page load.

---

## CTA URL

All CTAs on this page link to:

```
/request-to-book/?selected_experience=golden-hour-escape
```

This URL parameter is what populates the `selected_experience` hidden field in the form. The link appears in two locations:

- Section 2 (Experience Description): inline "Request to Book" button
- Section 6 (Bottom CTA): "Request Golden Hour Escape" button

---

## MetForm / WPForms: Hidden Field Setup

### MetForm

1. Open the request-to-book form in MetForm editor.
2. Add a Hidden Field element to the form canvas.
3. Set the Field Name to `selected_experience`.
4. Set the Default Value to: `{url_param:selected_experience}`
   - This MetForm dynamic tag reads the value from the URL query string automatically on page load.
5. Repeat for `brand` (default value: `shesaidsail`) and `service_category` (default value: `yacht-charter`).
6. These fields do not render visibly to the user. They pass silently with the form submission.

### WPForms (alternative)

1. In the WPForms form builder, add a Hidden Field.
2. Set the field label to `selected_experience` (used as the field key).
3. Under Default Value, select "Smart Tags" and choose `{query_var key="selected_experience"}`.
4. Save. The field will capture the URL parameter value automatically.
5. Repeat for `brand` (static value: `shesaidsail`) and `service_category` (static value: `yacht-charter`).

---

## Make.com Routing

**Scenario:** M-BRAND-ROUTER (existing scenario, no new scenario required)

The existing M-BRAND-ROUTER scenario handles all inbound form submissions. Routing logic:

1. Webhook receives form payload including the `selected_experience` field.
2. Router module reads `brand` field value.
3. Branch condition: `brand = "shesaidsail"` routes to the She Said Sail flow.
4. Within the She Said Sail flow, `selected_experience = "golden-hour-escape"` is passed through to the Airtable Create Record module and any downstream notification logic.
5. No new routes, filters, or modules are needed for this experience.

The `selected_experience` value is already mapped in the Airtable Create Record module as a field. If it is not yet mapped, add a mapping for the `selected_experience` field using the incoming bundle value.

---

## Notes

- No new Airtable tables or bases are needed.
- No new Make.com scenarios are needed.
- No webhook endpoint changes are needed.
- The only required action is confirming the hidden field dynamic tag is configured in the form, and that `selected_experience` is mapped in the Airtable module within M-BRAND-ROUTER.
