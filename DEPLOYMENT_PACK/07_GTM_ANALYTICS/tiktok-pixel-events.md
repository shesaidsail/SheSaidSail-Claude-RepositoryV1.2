# She Said Sail: TikTok Pixel Configuration

How to configure the TikTok Pixel via GTM. All code goes into GTM Custom HTML tags.

**Important:** Replace `YOUR_TIKTOK_PIXEL_ID` in all code snippets with the actual TikTok Pixel ID from your TikTok Ads Manager account (Assets > Events > Web Events > your pixel).

---

## Standard Event Mapping

| GA4 Event | TikTok Pixel Event | Notes |
|---|---|---|
| `view_homepage` | PageView | Fired by base code on all pages |
| `view_request_page` | PageView | Fired by base code on all pages |
| `click_request_to_book` | ViewContent | Signals intent to book |
| `submit_booking_form` | SubmitForm | Primary conversion event |
| `view_thank_you_page` | CompleteRegistration | Second confirmation of a completed inquiry |
| `submit_email_capture` | Subscribe | Email list growth event |
| `view_experiences_page` | ViewContent | Optional. Signals browsing intent. |

---

## GTM Tag: TikTok Pixel Base Code

**Tag Name:** TikTok Pixel - Base Code
**Tag Type:** Custom HTML
**Trigger:** All Pages

```html
<!-- TikTok Pixel Base Code | She Said Sail -->
<!-- Replace YOUR_TIKTOK_PIXEL_ID with your actual TikTok Pixel ID -->
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;
  var ttq=w[t]=w[t]||[];
  ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
  ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
  for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
  ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
  ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";
  ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};
  var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;
  var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
  ttq.load('YOUR_TIKTOK_PIXEL_ID');
  ttq.page();
}(window, document, 'ttq');
</script>
<!-- End TikTok Pixel Base Code -->
```

**After pasting:**
1. Replace `YOUR_TIKTOK_PIXEL_ID` with the actual pixel ID.
2. Save the tag.
3. Set the trigger to "All Pages."
4. Publish the GTM container.
5. Verify using the TikTok Pixel Helper browser extension.

---

## GTM Tag: TikTok SubmitForm Event (submit_booking_form)

**Tag Name:** TikTok Pixel - SubmitForm
**Tag Type:** Custom HTML
**Trigger:** CE - submit_booking_form

```html
<!-- TikTok Pixel SubmitForm Event | submit_booking_form | She Said Sail -->
<script>
(function() {
  if (typeof ttq === 'undefined') { return; }
  ttq.track('SubmitForm', {
    content_name: 'Request to Book',
    content_category: 'Yacht Charter',
    content_id: 'request-to-book-form',
    currency: 'USD',
    value: 10000
  });
})();
</script>
<!-- End TikTok Pixel SubmitForm Event -->
```

---

## GTM Tag: TikTok CompleteRegistration Event (view_thank_you_page)

**Tag Name:** TikTok Pixel - CompleteRegistration
**Tag Type:** Custom HTML
**Trigger:** CE - view_thank_you_page

```html
<!-- TikTok Pixel CompleteRegistration Event | view_thank_you_page | She Said Sail -->
<script>
(function() {
  if (typeof ttq === 'undefined') { return; }
  ttq.track('CompleteRegistration', {
    content_name: 'Booking Inquiry Completed',
    currency: 'USD',
    value: 10000
  });
})();
</script>
<!-- End TikTok Pixel CompleteRegistration Event -->
```

---

## GTM Tag: TikTok ViewContent Event (click_request_to_book)

**Tag Name:** TikTok Pixel - ViewContent (click_request_to_book)
**Tag Type:** Custom HTML
**Trigger:** CE - click_request_to_book

```html
<!-- TikTok Pixel ViewContent Event | click_request_to_book | She Said Sail -->
<script>
(function() {
  if (typeof ttq === 'undefined') { return; }
  ttq.track('ViewContent', {
    content_name: 'Request to Book CTA',
    content_category: 'Yacht Charter'
  });
})();
</script>
<!-- End TikTok Pixel ViewContent Event -->
```

---

## GTM Tag: TikTok Subscribe Event (submit_email_capture)

**Tag Name:** TikTok Pixel - Subscribe
**Tag Type:** Custom HTML
**Trigger:** CE - submit_email_capture

```html
<!-- TikTok Pixel Subscribe Event | submit_email_capture | She Said Sail -->
<script>
(function() {
  if (typeof ttq === 'undefined') { return; }
  ttq.track('Subscribe', {
    content_name: 'Email List Signup',
    content_category: 'Newsletter'
  });
})();
</script>
<!-- End TikTok Pixel Subscribe Event -->
```

---

## TikTok Ads: Custom Conversion Setup

1. In TikTok Ads Manager, go to Assets > Events.
2. Select your pixel.
3. Click Manage > Custom Events > Create Custom Event.
4. Set:
   - Event: SubmitForm
   - Optimization goal: Conversions
   - Value: $10,000
5. Save.

Use this custom event in your TikTok ad sets as the optimization event.

---

## TikTok Ads: Audience Setup

### Custom Audience: Website Visitors

1. TikTok Ads Manager > Assets > Audiences > Create Audience > Custom Audience > Website Traffic.
2. Set:
   - Pixel: your pixel
   - Event: PageView
   - URL: All visitors (or filter by shesaidsail.com)
   - In the last: 30 days
3. Name: SSS - TikTok Website Visitors 30d
4. Save.

### Custom Audience: High Intent (Viewed Request Page)

1. Create Audience > Website Traffic.
2. Event: PageView. URL contains: /request-to-book/
3. Last 60 days.
4. Name: SSS - TikTok Request Page Visitors 60d

### Exclusion Audience: Converters

1. Create Audience > Website Traffic.
2. Event: SubmitForm or CompleteRegistration.
3. Last 180 days.
4. Name: SSS - TikTok Converters Exclusion 180d

Use the Converters Exclusion audience in all paid ad sets to avoid retargeting people who already submitted an inquiry.

---

## Verification

1. Install the TikTok Pixel Helper Chrome extension (available in the Chrome Web Store).
2. Open your website homepage.
3. Click the Pixel Helper icon in the toolbar.
4. Confirm: PageView event shows your pixel ID.
5. Submit a test form. Confirm: SubmitForm event appears in the Pixel Helper.
6. In TikTok Ads Manager, go to Assets > Events > Test Events. Enter your pixel ID and site URL to verify events in real time.
