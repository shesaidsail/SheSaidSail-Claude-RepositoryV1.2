# Request Page Analytics Events
She Said Sail | Analytics Readiness v2.0

---

## GTM dataLayer Events

All events push to `window.dataLayer` with the following base properties:

```js
{
  event: '<event_name>',
  page_type: 'request_page',
  brand: 'she_said_sail'
}
```

---

### view_request_page

Fires immediately on DOMContentLoaded.

```js
{
  event: 'view_request_page',
  page_type: 'request_page',
  brand: 'she_said_sail'
}
```

GA4 equivalent: `view_request_page`
Meta Pixel: PageView (fires via GTM container)

---

### start_booking_form

Fires on first focus of any form field.

```js
{
  event: 'start_booking_form',
  page_type: 'request_page',
  brand: 'she_said_sail'
}
```

GA4 equivalent: `start_booking_form`
Meta Pixel: `InitiateCheckout`
TikTok: not fired

---

### field_completion_progress

Fires when each distinct required field is completed for the first time.

```js
{
  event: 'field_completion_progress',
  page_type: 'request_page',
  brand: 'she_said_sail',
  field_name: '<name attribute>',
  fields_completed: <integer>
}
```

GA4 equivalent: `field_completion_progress`

---

### select_occasion

Fires when user clicks an occasion card.

```js
{
  event: 'select_occasion',
  page_type: 'request_page',
  brand: 'she_said_sail',
  occasion: '<occasion value>'
}
```

---

### select_experience_type

Fires when user clicks an experience card.

```js
{
  event: 'select_experience_type',
  page_type: 'request_page',
  brand: 'she_said_sail',
  experience: '<rose|sunset|pinkpalm|monaco>'
}
```

---

### click_request_cta

Fires on mousedown of the primary submit button.

```js
{
  event: 'click_request_cta',
  page_type: 'request_page',
  brand: 'she_said_sail'
}
```

---

### submit_booking_form

Fires on validated form submission before webhook call.

```js
{
  event: 'submit_booking_form',
  page_type: 'request_page',
  brand: 'she_said_sail',
  experience: '<value>',
  occasion: '<value>',
  guest_count: '<value>'
}
```

GA4 equivalent: `submit_booking_form`
Meta Pixel: `Lead` with `{ content_name: 'request_to_book' }`
TikTok: `SubmitForm`

---

### view_thank_you_page

Fires after successful form submission and thank-you state is shown.

```js
{
  event: 'view_thank_you_page',
  page_type: 'request_page',
  brand: 'she_said_sail'
}
```

GA4 equivalent: `purchase` (with `value: 0`, `transaction_id: 'sse-<timestamp>'`)

---

### form_submission_error

Fires if webhook call fails (graceful fallback). Form data is also pushed for recovery.

```js
{
  event: 'form_submission_error',
  form_data: { ... }
}
```

---

## Meta Pixel Readiness

| GTM Event | Meta Pixel Event |
|---|---|
| Page view | PageView (via GTM) |
| start_booking_form | InitiateCheckout |
| submit_booking_form | Lead |
| view_thank_you_page | (handled by GA4 purchase event) |

Implementation: Add Meta Pixel base code to `<head>`. The above events fire `fbq()` via the `metaPixelEvent()` helper already present in the page script. No additional wiring required in site code.

---

## TikTok Pixel Readiness

| GTM Event | TikTok Event |
|---|---|
| submit_booking_form | SubmitForm |

Implementation: Add TikTok Pixel base code. Events fire via `ttqEvent()` helper. `ttq` object must be available globally before the form submit handler fires.

---

## GA4 Readiness

All GA4 events call `gtag('event', ...)` via the `ga4Event()` helper. GA4 property `GT-WV3X86GZ` is already loaded on the page.

Recommended GA4 custom events to create in the GA4 interface:
- `view_request_page`
- `start_booking_form`
- `submit_booking_form`
- `field_completion_progress`
- `select_occasion`
- `select_experience_type`
- `click_request_cta`

---

## Conversion Funnel to Track in GA4

1. `view_request_page` (100% baseline)
2. `start_booking_form` (drop-off point 1)
3. `field_completion_progress` with `fields_completed >= 4` (drop-off point 2)
4. `click_request_cta` (intent signal)
5. `submit_booking_form` (conversion)
6. `view_thank_you_page` (confirmed conversion)
