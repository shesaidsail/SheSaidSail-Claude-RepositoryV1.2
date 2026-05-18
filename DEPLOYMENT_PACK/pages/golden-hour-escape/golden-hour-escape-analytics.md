# Golden Hour Escape: Analytics Reference

**Page:** /experience/golden-hour-escape/
**Last updated:** 2026-05-18

---

## Overview

No new GTM tags, triggers, or variables are required for this page. All events are captured automatically by the global She Said Sail tracking script, which fires on any `/experience/*` path and on any link to `/request-to-book/`.

The setup below documents what fires, where it goes, and how to verify it in GTM Preview mode.

---

## Events That Fire Automatically

### Page View Event

| Property | Value |
|---|---|
| Event name | `view_experience_page` |
| Trigger | Any page load on `/experience/*` path |
| Source | Global JS (fires automatically, no configuration needed per page) |

**Data Layer push (example):**

```js
dataLayer.push({
  event: 'view_experience_page',
  experience_slug: 'golden-hour-escape',
  experience_name: 'Golden Hour Escape'
});
```

The global JS reads the slug from the URL path. No page-specific code is needed.

---

### CTA Click Event

| Property | Value |
|---|---|
| Event name | `click_request_to_book` |
| Trigger | Any click on a link to `/request-to-book/` |
| Source | Global JS (fires automatically on any page) |

**Data Layer push (example):**

```js
dataLayer.push({
  event: 'click_request_to_book',
  experience_slug: 'golden-hour-escape',
  cta_location: 'description_section' // or 'bottom_cta'
});
```

Both CTA buttons on the page (Section 2 and Section 6) fire this event. The `cta_location` value distinguishes between them if the global JS supports positional tracking.

---

### Scroll Depth Events

| Property | Value |
|---|---|
| Event names | `scroll_50_percent`, `scroll_90_percent` |
| Trigger | Scroll depth thresholds (50% and 90% of page height) |
| Source | Global JS (fires automatically on any page) |

No page-specific configuration is needed.

---

## GTM Setup

**No new tags, triggers, or variables are required.**

The following pre-existing GTM components handle all tracking for this page:

| Component | Type | Status |
|---|---|---|
| Custom Event Trigger: `view_experience_page` | Trigger | Already exists (see DEPLOYMENT_PACK/07_GTM_ANALYTICS/gtm-events-map.md) |
| Custom Event Trigger: `click_request_to_book` | Trigger | Already exists |
| Custom Event Trigger: `scroll_50_percent` | Trigger | Already exists |
| Custom Event Trigger: `scroll_90_percent` | Trigger | Already exists |
| Data Layer Variable: `dlv_experience_slug` | Variable | Already exists |

If the above triggers and variables are not yet configured in the GTM container, refer to DEPLOYMENT_PACK/07_GTM_ANALYTICS/gtm-events-map.md for the full setup instructions. They are shared across all experience pages and only need to be created once.

---

## GA4 Audience

**Create one new GA4 audience** to enable remarketing and reporting for visitors to this specific experience.

| Setting | Value |
|---|---|
| Audience name | Viewed Golden Hour Escape |
| Condition | `dlv_experience_slug` exactly matches `golden-hour-escape` |
| Event scope | `view_experience_page` |
| Membership duration | 30 days (recommended) |

**Steps to create:**

1. In GA4, go to Configure > Audiences > New Audience.
2. Select "Create a custom audience."
3. Add condition: Event parameter `experience_slug` exactly equals `golden-hour-escape`.
4. Optionally, scope to the event `view_experience_page` for precision.
5. Name the audience "Viewed Golden Hour Escape."
6. Set membership duration to 30 days.
7. Save.

This audience can be used for Google Ads remarketing, GA4 reporting segments, and conversion funnel analysis.

---

## Verification Checklist

Use GTM Preview mode and GA4 DebugView to confirm the following before publishing:

- [ ] Load `/experience/golden-hour-escape/` in GTM Preview
- [ ] Confirm `view_experience_page` fires on page load with `experience_slug: "golden-hour-escape"`
- [ ] Scroll to 50% and confirm `scroll_50_percent` fires
- [ ] Scroll to 90% and confirm `scroll_90_percent` fires
- [ ] Click either CTA button and confirm `click_request_to_book` fires
- [ ] Confirm all events appear in GA4 DebugView with correct parameters

---

## Notes

- The `dlv_experience_slug` Data Layer Variable is what GA4 and GTM use to identify which experience page is being viewed. It must already exist in the GTM container.
- No Airtable or Make.com changes are needed for analytics.
- No new GA4 events need to be created. All event names already exist in the measurement plan.
