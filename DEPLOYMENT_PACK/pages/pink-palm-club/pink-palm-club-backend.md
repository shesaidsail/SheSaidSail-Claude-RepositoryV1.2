# Pink Palm Club: Backend Documentation

**Experience:** Pink Palm Club
**Page:** /experience/pink-palm-club/
**Last updated:** 2026-05-18

---

## CTA URL

All request buttons on this page link to:

```
/request-to-book/?selected_experience=pink-palm-club
```

This URL parameter pre-populates the `selected_experience` hidden field in MetForm via JavaScript on the request-to-book page.

---

## Airtable Mapping

**Table:** Requests

All 13 standard hidden fields are mapped as follows:

| Field Name | Type | Value |
|---|---|---|
| brand | Single line text | shesaidsail |
| service_category | Single line text | yacht-charter |
| selected_experience | Single line text | pink-palm-club |
| source_url | Single line text | Populated dynamically from `document.referrer` or page URL |
| utm_source | Single line text | Populated from URL parameter `utm_source` |
| utm_medium | Single line text | Populated from URL parameter `utm_medium` |
| utm_campaign | Single line text | Populated from URL parameter `utm_campaign` |
| utm_content | Single line text | Populated from URL parameter `utm_content` |
| utm_term | Single line text | Populated from URL parameter `utm_term` |
| form_id | Single line text | Populated from MetForm form ID |
| submission_timestamp | Single line text | Populated at submission time (ISO 8601) |
| user_agent | Single line text | Populated from `navigator.userAgent` |
| session_id | Single line text | Populated from session cookie or generated UUID |

### Fixed Hidden Field Values for This Experience

```
brand = "shesaidsail"
service_category = "yacht-charter"
selected_experience = "pink-palm-club"
```

---

## MetForm Setup

The `selected_experience` hidden field is pre-populated automatically via the global JS on the request-to-book page. The script reads the `selected_experience` URL parameter and writes the value into the hidden field before form submission.

No manual MetForm configuration is required beyond confirming the hidden field name matches `selected_experience` exactly.

**Verification step:** Load `/request-to-book/?selected_experience=pink-palm-club` and inspect the hidden field value in the DOM. It should read `pink-palm-club`.

---

## Make.com Routing

No new scenarios or tables are required for this experience.

**Routing logic:**

The existing M-BRAND-ROUTER scenario reads the `selected_experience` field from each new Airtable record. When `selected_experience` equals `pink-palm-club`, the router directs the submission through the She Said Sail flow.

The She Said Sail flow handles:

- Concierge notification (email or Slack, depending on current configuration)
- Airtable record status update to "Received"
- Guest confirmation email (if configured)

**No new Make.com scenarios, modules, or webhooks are required.**

---

## Notes

- No new Airtable tables are needed. All Pink Palm Club submissions write to the existing Requests table.
- No new Make.com scenarios are needed. The M-BRAND-ROUTER handles routing by `selected_experience` value automatically.
- Confirm that `selected_experience = "pink-palm-club"` matches the router condition exactly (case-sensitive, hyphenated).
