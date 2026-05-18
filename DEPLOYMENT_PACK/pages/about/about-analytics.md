# About Page: Analytics Setup

**Page:** `/about/`
**Last updated:** 2026-05-18

---

## Events Fired on This Page

All events below are fired automatically by the global JavaScript layer. No page-specific code is required.

| Event Name | Trigger | Source |
|---|---|---|
| `view_about_page` | Page load on `/about/` path | Global JS |
| `click_request_to_book` | Click on any link to `/request-to-book/` | Global JS |
| `click_explore_experiences` | Click on any link to `/experiences/` | Global JS |
| `scroll_50_percent` | User scrolls past 50% of page height | Global JS |
| `scroll_90_percent` | User scrolls past 90% of page height | Global JS |

---

## GTM Configuration

### Trigger: CE - view_about_page

- **Trigger type:** Custom Event
- **Event name:** `view_about_page`
- **Use the standard "CE -" naming pattern** consistent with other Custom Event triggers in this GTM container
- This trigger fires once per page load when the global JS pushes `view_about_page` to the dataLayer

### Tag: GA4 Event - view_about_page

- **Tag type:** Google Analytics: GA4 Event
- **Event name:** `view_about_page`
- **Parameters to send:**
  - `page_location` (standard GA4 parameter, already configured as a DLV at the container level)
- **Firing trigger:** CE - view_about_page

No new Data Layer Variable (DLV) configuration is required. `page_location` is already a standard parameter available across the container.

---

## GA4 Audience: Visited About Page, No Form Submit

**Audience name:** Visited About Page - No Form Submit

**Use case:** Remarketing to visitors who showed brand intent (they visited the About page, which signals active consideration) but did not convert. This is a warm audience appropriate for paid social and display retargeting.

**Configuration:**

- Include condition: User triggered `view_about_page` at least once
- Exclude condition: User triggered `submit_booking_form` at least once
- Membership duration: 30 days (adjust based on average consideration window)

**Where to create:** GA4 Admin > Audiences > New Audience > Custom

**Remarketing use:** Export this audience to Google Ads and Meta Ads for retargeting campaigns. Messaging for this audience should acknowledge that they know the brand and prompt action without being repetitive (e.g., "Still thinking it over? Browse the experiences.").

---

## Notes

- No new DLV variables are needed for this page. `page_location` is already a standard parameter.
- The GA4 audience should be created after the GTM build is published and `view_about_page` is confirmed firing in GTM Preview mode.
- `click_request_to_book` and `click_explore_experiences` are fired globally on matching link clicks anywhere on the site. Verify in GTM Preview that they fire correctly from the bottom CTA section of the About page.
