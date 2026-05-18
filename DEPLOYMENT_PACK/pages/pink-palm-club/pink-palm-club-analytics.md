# Pink Palm Club: Analytics Documentation

**Experience:** Pink Palm Club
**Page:** /experience/pink-palm-club/
**Last updated:** 2026-05-18

---

## Overview

All analytics for this page are handled by the global GTM container and global JS already deployed across the She Said Sail site. No new GTM variables, triggers, or tags are required for Pink Palm Club.

---

## Events That Fire Automatically

### Page View

**Event name:** `view_experience_page`

Fired by the global JS on every experience page load. The data layer push includes:

```json
{
  "event": "view_experience_page",
  "experience_slug": "pink-palm-club"
}
```

This event fires as long as the page URL matches `/experience/pink-palm-club/` and the global JS is loaded in the page footer.

### CTA Click

**Event name:** `click_request_to_book`

Fired by the global JS when a visitor clicks any element with the class `.sss-ppc-cta-button` or any anchor linking to `/request-to-book/`. The data layer push includes:

```json
{
  "event": "click_request_to_book",
  "experience_slug": "pink-palm-club",
  "cta_location": "[varies by position: desc | bottom]"
}
```

Both CTA buttons on this page (Section 2 and Section 6) are covered by this trigger.

### Scroll Depth

**Event names:** `scroll_50_percent`, `scroll_90_percent`

Fired by the global JS scroll depth listener. No page-specific configuration required.

```json
{ "event": "scroll_50_percent", "experience_slug": "pink-palm-club" }
{ "event": "scroll_90_percent", "experience_slug": "pink-palm-club" }
```

---

## GA4 Audience Recommendation

**Audience name:** Viewed Pink Palm Club

**Condition:** `dlv_experience_slug` equals `pink-palm-club`

This data layer variable (`dlv_experience_slug`) is already configured in the global GTM container and reads from the `experience_slug` key pushed on `view_experience_page`. No new variable is needed.

**Suggested use:** Retargeting visitors who viewed Pink Palm Club but did not submit a request. This audience is high-intent given the bachelorette focus and should be treated as the highest-priority retargeting segment among the experience pages.

---

## GTM Preview Verification

To verify events are firing correctly after deployment:

1. Open GTM Preview mode and load `/experience/pink-palm-club/`
2. Confirm `view_experience_page` fires on page load with `experience_slug: "pink-palm-club"`
3. Click the "Request to Book" button in Section 2 and confirm `click_request_to_book` fires
4. Click the "Request Pink Palm Club" button in Section 6 and confirm `click_request_to_book` fires
5. Scroll to 50% and 90% depth and confirm the corresponding scroll events fire

---

## No New GTM Configuration Required

- No new variables
- No new triggers
- No new tags

All events flow through the existing global GTM setup. The `experience_slug` value `pink-palm-club` is handled automatically once the page URL and global JS are in place.
