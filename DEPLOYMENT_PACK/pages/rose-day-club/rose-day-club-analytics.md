# Rose Day Club: Analytics Implementation Notes

Page: /experience/rose-day-club/
Experience Slug: rose-day-club

---

## Event Tracking Overview

All events for this page fire automatically from global JS. No page-specific tags, triggers, or variables are required in GTM.

---

## Events That Fire on This Page

### Page View Event

**Event name:** `view_experience_page`

**Fires:** On page load, automatically via global JS for all `/experience/*` pages.

**Data layer push:**
```json
{
  "event": "view_experience_page",
  "experience_slug": "rose-day-club",
  "experience_name": "Rose Day Club",
  "brand": "shesaidsail",
  "page_path": "/experience/rose-day-club/"
}
```

No new GTM trigger required. The existing Custom Event Trigger listening for `view_experience_page` already captures this.

---

### CTA Click Event

**Event name:** `click_request_to_book`

**Fires:** On click of any element with the CTA link to `/request-to-book/?selected_experience=rose-day-club`.

**Data layer push:**
```json
{
  "event": "click_request_to_book",
  "experience_slug": "rose-day-club",
  "cta_location": "(hero | description | bottom)",
  "destination_url": "/request-to-book/?selected_experience=rose-day-club"
}
```

The `cta_location` value is populated by the global JS based on which section the click originates from.

No new GTM tag required. The existing `click_request_to_book` tag fires on this event name automatically.

---

### Scroll Depth Events

**Events:** `scroll_50_percent`, `scroll_90_percent`

**Fires:** Automatically via global JS scroll depth listener on all experience pages.

**Data layer push (example at 50%):**
```json
{
  "event": "scroll_50_percent",
  "experience_slug": "rose-day-club",
  "page_path": "/experience/rose-day-club/"
}
```

No new GTM configuration required.

---

## GTM Setup

No new tags required. No new triggers required. No new variables required.

The following existing GTM components already cover Rose Day Club:

| Component | Type | Covers |
|---|---|---|
| view_experience_page | Custom Event Trigger | All /experience/* page views |
| click_request_to_book | Custom Event Tag | All RTB CTA clicks |
| scroll_50_percent | Custom Event Tag | 50% scroll on experience pages |
| scroll_90_percent | Custom Event Tag | 90% scroll on experience pages |
| dlv_experience_slug | Data Layer Variable | Reads experience_slug from datalayer |

---

## GA4 Audience Recommendation

**Audience name:** Viewed Rose Day Club

**Condition:** `dlv_experience_slug` equals `rose-day-club`

**Use:** Retargeting, lookalike expansion, and funnel analysis for this specific experience.

**Suggested segments to build alongside this audience:**

- Viewed Rose Day Club AND clicked CTA (high intent)
- Viewed Rose Day Club AND scrolled 90% (full engagement)
- Viewed Rose Day Club AND did NOT submit a request (re-engagement candidate)

These can be built in GA4 using the existing event and parameter structure. No new parameters are needed.

---

## Verification Steps

1. Load `/experience/rose-day-club/` in Chrome with GTM Preview active.
2. Confirm `view_experience_page` fires on page load with `experience_slug: "rose-day-club"`.
3. Click the "Request to Book" button in the description section. Confirm `click_request_to_book` fires with correct slug and destination URL.
4. Scroll to 50% and 90% of page. Confirm respective scroll events fire.
5. In GA4 DebugView, confirm all four events appear with correct parameters.

---

## No New GTM Work Required

All tracking is handled by existing global infrastructure. Rose Day Club is fully covered on publish.
