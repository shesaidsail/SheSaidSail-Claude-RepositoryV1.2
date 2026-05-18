# She Said Sail: Conversion Tracking Plan
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

---

## TRACKING STACK

| Platform | ID | Status |
|---|---|---|
| Google Tag Manager | GTM-WWTT27Z3 | Already installed |
| Google Analytics 4 | GT-WV3X86GZ | Already installed via GTM |
| Meta Pixel | To be created in Meta Business Manager | Not yet installed |
| TikTok Pixel | To be created in TikTok Ads Manager | Not yet installed |

All tracking fires through GTM. No pixels are hardcoded into WordPress.
Add Meta and TikTok pixels as GTM tags (see GTM configuration below).

---

## GA4 EVENTS

### Standard Events (Auto-Collected by GA4)

These require no additional code:
- page_view
- scroll (90% threshold)
- click (outbound links)
- session_start
- first_visit

### Custom Events (Fired via dataLayer.push)

All custom events are pushed via `gtm-datalayer-events.js`.
See `08_PRODUCT_ENGINEERING/website/custom-js/gtm-datalayer-events.js`.

| Event Name | Trigger | Parameters |
|---|---|---|
| view_homepage | Page load on homepage | page_location |
| click_request_to_book | Click on any "Request to Book" CTA | cta_location, page_location |
| click_explore_experiences | Click on hero "Plan Your Experience" or similar | cta_location |
| click_experience_card | Click on any experience card | experience_name, card_position |
| start_booking_form | First interaction with booking form | form_name |
| submit_booking_form | Successful booking form submission | form_name, occasion, group_size |
| submit_email_capture | Email capture form submission | form_location |
| click_phone | Click on tap-to-call phone link | page_location |
| open_chat | Tidio chat opened | page_location |
| view_thank_you_page | Page view on /thank-you/ or confirmation page | -- |

### GA4 Conversion Events

Mark these as conversions in GA4 Admin > Events:
- `submit_booking_form` (primary conversion)
- `view_thank_you_page` (secondary conversion, backup)
- `submit_email_capture` (micro-conversion)

---

## META PIXEL EVENTS

### Standard Events

| GA4 Equivalent | Meta Pixel Event | Parameters |
|---|---|---|
| view_homepage | PageView | (automatic) |
| click_request_to_book | InitiateCheckout | content_name: "Request to Book" |
| submit_booking_form | Lead | content_name: occasion, value: estimated |
| view_thank_you_page | Lead | content_name: "Booking Form Submitted" |
| submit_email_capture | Lead | content_name: "Email Capture" |

### Custom Conversions in Meta

Create custom conversions for:
1. "Booking Form Submitted" = URL contains /thank-you/ OR Meta Pixel Lead event with content_name = occasion value
2. "Email Capture" = Meta Pixel Lead event with content_name = "Email Capture"

### Meta Pixel GTM Tag Configuration

1. In GTM: New Tag > Custom HTML
2. Tag name: Meta Pixel - Base Code
3. HTML:
```html
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_META_PIXEL_ID');
fbq('track', 'PageView');
</script>
```
4. Trigger: All Pages

5. Add separate GTM tags for each conversion event, using Custom HTML that reads from dataLayer:
```html
<script>
fbq('track', 'Lead', {
  content_name: {{dlv_occasion}} || 'booking-form'
});
</script>
```
Trigger: Custom Event = submit_booking_form

---

## TIKTOK PIXEL EVENTS

### Standard Events

| GA4 Equivalent | TikTok Pixel Event | Parameters |
|---|---|---|
| view_homepage | PageView | (automatic) |
| click_request_to_book | ViewContent | content_name: "Request to Book" |
| submit_booking_form | SubmitForm | content_name: occasion |
| view_thank_you_page | CompleteRegistration | -- |
| submit_email_capture | Subscribe | -- |

### TikTok Pixel GTM Tag Configuration

1. In GTM: New Tag > Custom HTML
2. Tag name: TikTok Pixel - Base Code
3. HTML:
```html
<script>
!function (w, d, t) {
  w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];
  ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"];
  ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};
  for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);
  ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e};
  ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";
  ttq._i=ttq._i||{};ttq._i[e]=[];ttq._i[e]._u=i;ttq._t=ttq._t||{};ttq._t[e]=+new Date;
  ttq._o=ttq._o||{};ttq._o[e]=n||{};var o=document.createElement("script");
  o.type="text/javascript";o.async=!0;o.src=i+"?sdkid="+e+"&lib="+t;
  var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
  ttq.load('YOUR_TIKTOK_PIXEL_ID');
  ttq.page();
}(window, document, 'ttq');
</script>
```
4. Trigger: All Pages

---

## GTM CONFIGURATION

### Variables Required

Create these Data Layer Variables in GTM:

| Variable Name | Data Layer Key | Type |
|---|---|---|
| dlv_event_name | event | Data Layer Variable |
| dlv_cta_location | cta_location | Data Layer Variable |
| dlv_experience_name | experience_name | Data Layer Variable |
| dlv_card_position | card_position | Data Layer Variable |
| dlv_occasion | occasion | Data Layer Variable |
| dlv_group_size | group_size | Data Layer Variable |
| dlv_form_name | form_name | Data Layer Variable |
| dlv_page_location | page_location | Data Layer Variable |

### Triggers Required

| Trigger Name | Type | Condition |
|---|---|---|
| CE - click_request_to_book | Custom Event | Event name = click_request_to_book |
| CE - submit_booking_form | Custom Event | Event name = submit_booking_form |
| CE - submit_email_capture | Custom Event | Event name = submit_email_capture |
| CE - click_experience_card | Custom Event | Event name = click_experience_card |
| CE - click_phone | Custom Event | Event name = click_phone |
| CE - view_thank_you_page | Page View | Page Path contains /thank-you/ |

### Tags Required

| Tag Name | Tag Type | Trigger |
|---|---|---|
| GA4 - Page View | Google Tag (GA4) | All Pages |
| GA4 - click_request_to_book | GA4 Event | CE - click_request_to_book |
| GA4 - submit_booking_form | GA4 Event | CE - submit_booking_form |
| GA4 - submit_email_capture | GA4 Event | CE - submit_email_capture |
| GA4 - click_experience_card | GA4 Event | CE - click_experience_card |
| GA4 - click_phone | GA4 Event | CE - click_phone |
| Meta Pixel - Base Code | Custom HTML | All Pages |
| Meta Pixel - Lead (Booking) | Custom HTML | CE - submit_booking_form |
| Meta Pixel - Lead (Email) | Custom HTML | CE - submit_email_capture |
| TikTok Pixel - Base Code | Custom HTML | All Pages |
| TikTok Pixel - SubmitForm | Custom HTML | CE - submit_booking_form |
| TikTok Pixel - Subscribe | Custom HTML | CE - submit_email_capture |

---

## GA4 AUDIENCES FOR REMARKETING

Create in GA4 > Audience Builder, then share to Meta Ads and Google Ads:

| Audience Name | Condition | Membership Duration |
|---|---|---|
| Homepage Visitors | page_view on homepage | 30 days |
| Request to Book Clickers | click_request_to_book fired | 60 days |
| Form Starters | start_booking_form fired | 30 days |
| Email Captures | submit_email_capture fired | 90 days |
| High Intent: Card + CTA | click_experience_card AND click_request_to_book | 14 days |
| Excluded: Converters | submit_booking_form fired | 180 days |

---

## REPORTING STRUCTURE

### Weekly Metrics to Review

- Sessions (homepage and /request-to-book/)
- click_request_to_book count
- submit_booking_form count
- submit_email_capture count
- CTR: sessions to click_request_to_book
- Form completion rate: start_booking_form to submit_booking_form
- Source breakdown: Meta, TikTok, Google, Organic, Direct

### GA4 Exploration Reports

Create these explorations in GA4:

1. **Conversion Funnel**
   - Step 1: view_homepage
   - Step 2: click_request_to_book
   - Step 3: start_booking_form
   - Step 4: submit_booking_form

2. **Source Performance**
   - Dimension: source/medium
   - Metrics: sessions, click_request_to_book, submit_booking_form

3. **Experience Card Performance**
   - Dimension: experience_name
   - Metric: click_experience_card count

---

## LAUNCH CHECKLIST: ANALYTICS

- [ ] GTM-WWTT27Z3 verified firing on all pages (use GTM Preview Mode)
- [ ] GA4 GT-WV3X86GZ verified receiving data (use GA4 DebugView)
- [ ] All custom dataLayer events verified firing in GTM Preview
- [ ] GA4 custom events appearing in DebugView
- [ ] Meta Pixel ID created and base code tag live
- [ ] Meta Pixel verified firing via Meta Pixel Helper browser extension
- [ ] TikTok Pixel ID created and base code tag live
- [ ] TikTok Pixel verified firing via TikTok Pixel Helper extension
- [ ] Conversion events marked in GA4 Admin
- [ ] GA4 Audiences created
- [ ] GA4 Audiences shared to Meta Ads and Google Ads
- [ ] GTM published (not just previewed)
