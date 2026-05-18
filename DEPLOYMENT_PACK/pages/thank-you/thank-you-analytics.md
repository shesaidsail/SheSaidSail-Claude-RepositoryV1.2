# Thank You Page: Analytics Documentation

## Primary Conversion Signal

**Event name:** `view_thank_you_page`

This event is already present in the global site JavaScript. It fires automatically whenever the page path contains `/thank-you/`. No new GTM tags or custom code are required to fire this event.

This event is the primary signal that a Request to Book form was successfully submitted. It should be treated as the top-level conversion across all platforms.

---

## GA4: Mark as Conversion

1. In GA4, go to Admin > Events
2. Find `view_thank_you_page` in the event list (it will appear after the first real page load fires it)
3. Toggle "Mark as conversion" to ON
4. This event will now appear in GA4 Conversions reports and be available as a goal in Google Ads if the account is linked

No custom parameters are needed. The event fires with the standard page_location and page_title properties from GA4's automatic collection.

---

## GTM: Trigger Configuration

The `view_thank_you_page` event fires via a dataLayer push or direct gtag call in the global JS. In GTM, this event should be used as the trigger for the following tags:

### GA4 Conversion Tag (if using server-side or redundant tagging)

- Trigger type: Custom Event
- Event name: `view_thank_you_page`
- Tag: GA4 Event tag or GA4 Configuration tag (if not already firing on all pages)

### Meta Pixel: Lead or Purchase Event

- Trigger: Custom Event matching `view_thank_you_page`
- Tag: Custom HTML or Meta Pixel event tag
- Event to fire: `Lead` (preferred for this funnel type) or `Purchase` if the account is configured around booking completions

Follow the pattern in `DEPLOYMENT_PACK/07_GTM_ANALYTICS/meta-pixel-events.md` for the tag structure.

Example tag body:

```html
<script>
  fbq('track', 'Lead');
</script>
```

### TikTok Pixel: CompleteRegistration or PlaceAnOrder Event

- Trigger: Custom Event matching `view_thank_you_page`
- Tag: Custom HTML tag with TikTok pixel event call
- Event to fire: `CompleteRegistration` (standard for lead form completions) or `PlaceAnOrder` if TikTok campaign is purchase-optimized

Example tag body:

```html
<script>
  ttq.track('CompleteRegistration');
</script>
```

---

## Retargeting Suppression

Visitors who trigger `view_thank_you_page` have already submitted a booking request. Continuing to show them conversion-focused ads is wasteful and can feel intrusive. They should be removed from active remarketing audiences.

### Meta Ads Manager

1. In Meta Events Manager, create a Custom Audience based on the `Lead` (or `Purchase`) pixel event
2. In each active ad set targeting remarketing audiences, add this audience as an exclusion
3. Label the exclusion audience: "Already submitted: Thank You page"

### TikTok Ads Manager

1. In TikTok Events Manager, create a Custom Audience based on the `CompleteRegistration` (or `PlaceAnOrder`) pixel event
2. In each active ad group, add this audience as an exclusion
3. Label the exclusion audience: "Already submitted: Thank You page"

---

## No New GTM Variables or Triggers Required

All configuration described above uses the existing `view_thank_you_page` event already present in the global JS. No new GTM variables, data layer variables, or lookup tables are needed beyond what is documented in `DEPLOYMENT_PACK/07_GTM_ANALYTICS/`.

---

## Implementation Checklist

- [ ] `view_thank_you_page` confirmed firing in GTM Preview when /thank-you/ loads
- [ ] GA4 conversion toggle enabled for `view_thank_you_page`
- [ ] GTM tag firing Meta Pixel Lead event on `view_thank_you_page` trigger
- [ ] GTM tag firing TikTok Pixel CompleteRegistration event on `view_thank_you_page` trigger
- [ ] Meta suppression audience created and applied to active ad sets
- [ ] TikTok suppression audience created and applied to active ad groups
