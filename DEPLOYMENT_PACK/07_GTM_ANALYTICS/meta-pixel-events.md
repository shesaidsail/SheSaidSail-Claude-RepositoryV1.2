# She Said Sail: Meta Pixel Configuration

How to configure the Meta Pixel via GTM. All code goes into GTM Custom HTML tags.

**Important:** Replace `YOUR_PIXEL_ID` in all code snippets with the actual Meta Pixel ID from your Meta Business Manager account (Meta Events Manager > Data Sources > your pixel).

---

## Standard Event Mapping

| GA4 Event | Meta Pixel Event | Notes |
|---|---|---|
| `view_homepage` | PageView | Fired by base code on all pages |
| `view_request_page` | PageView | Fired by base code on all pages |
| `view_experiences_page` | ViewContent | Optional. Can be added as a separate tag if needed for audience segmentation. |
| `click_request_to_book` | No direct mapping | Captured in GA4 only |
| `submit_booking_form` | Lead | Primary conversion event for Meta campaigns |
| `submit_email_capture` | No direct mapping | Captured in GA4 only |
| `view_thank_you_page` | Lead | Second confirmation. Ensure this does not double-count if `submit_booking_form` also fires Lead. |

**Recommendation:** Use `submit_booking_form` as the primary Lead event. Do not also fire Lead on `view_thank_you_page` unless you de-duplicate using Meta's deduplication event_id parameter. Firing Lead twice for the same user inflates your reported conversions.

---

## GTM Tag: Meta Pixel Base Code

**Tag Name:** Meta Pixel - Base Code
**Tag Type:** Custom HTML
**Trigger:** All Pages

```html
<!-- Meta Pixel Base Code | She Said Sail -->
<!-- Replace YOUR_PIXEL_ID with your actual Meta Pixel ID -->
<script>
!function(f,b,e,v,n,t,s)
{if(f.fbq)return;n=f.fbq=function(){n.callMethod?
n.callMethod.apply(n,arguments):n.queue.push(arguments)};
if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
n.queue=[];t=b.createElement(e);t.async=!0;
t.src=v;s=b.getElementsByTagName(e)[0];
s.parentNode.insertBefore(t,s)}(window, document,'script',
'https://connect.facebook.net/en_US/fbevents.js');
fbq('init', 'YOUR_PIXEL_ID');
fbq('track', 'PageView');
</script>
<noscript>
<img height="1" width="1" style="display:none"
src="https://www.facebook.com/tr?id=YOUR_PIXEL_ID&ev=PageView&noscript=1"/>
</noscript>
<!-- End Meta Pixel Base Code -->
```

**After pasting:**
1. Replace both instances of `YOUR_PIXEL_ID` with the actual pixel ID.
2. Save the tag.
3. Set the trigger to "All Pages."
4. Publish the GTM container.
5. Verify using the Meta Pixel Helper browser extension.

---

## GTM Tag: Meta Pixel Lead Event (submit_booking_form)

**Tag Name:** Meta Pixel - Lead (submit_booking_form)
**Tag Type:** Custom HTML
**Trigger:** CE - submit_booking_form

```html
<!-- Meta Pixel Lead Event | submit_booking_form | She Said Sail -->
<script>
(function() {
  if (typeof fbq === 'undefined') { return; }
  fbq('track', 'Lead', {
    content_name: 'Request to Book Form',
    content_category: 'Yacht Charter',
    currency: 'USD',
    value: 10000
  });
})();
</script>
<!-- End Meta Pixel Lead Event -->
```

**Notes:**
- The `value` parameter is set to 10000 (the starting price for a charter). This helps Meta optimize for high-value leads. Adjust if needed.
- `currency` must be uppercase ISO code.
- This tag fires only when `submit_booking_form` fires in the dataLayer, not on every page.

---

## Custom Conversion Setup in Meta Events Manager

1. Open Meta Business Manager > Events Manager.
2. Select your pixel.
3. Click Custom Conversions > Create Custom Conversion.
4. Set:
   - Name: She Said Sail Form Submit
   - Data source: your pixel
   - Rule: Event = Lead (from the `submit_booking_form` tag above)
   - Category: Lead
   - Value: $10,000
5. Save.

This custom conversion appears in your Meta Ads reporting and is used for campaign optimization.

---

## Meta Ads Audience Setup

### Audience 1: Homepage Visitors (Retargeting)

1. In Meta Ads Manager, go to Audiences > Create Audience > Custom Audience > Website.
2. Set:
   - Source: your pixel
   - Include: people who visited your website
   - URL contains: `shesaidsail.com/` (all pages) OR specifically `shesaidsail.com` equals homepage
   - In the last: 30 days
3. Name: SSS - Homepage Visitors 30d
4. Save.

### Audience 2: Request Page Visitors (High Intent)

1. Create Audience > Custom Audience > Website.
2. Set:
   - Include: people who visited `shesaidsail.com/request-to-book/`
   - In the last: 60 days
3. Name: SSS - Request Page Visitors 60d
4. Save.

### Audience 3: Converters Exclusion

1. Create Audience > Custom Audience > Website.
2. Set:
   - Include: people who triggered the Lead event (submit_booking_form)
   - In the last: 180 days
3. Name: SSS - Converters Exclusion 180d
4. Save.

### How to Use These Audiences in Campaigns

- In your retargeting ad set, under Audiences: Add "SSS - Homepage Visitors 30d."
- Under Exclusions: Add "SSS - Converters Exclusion 180d."
- This ensures you are showing retargeting ads to people who visited but did not submit, and not wasting budget on people who already inquired.

---

## Verification

1. Install the Meta Pixel Helper Chrome extension (free, from Meta).
2. Open your website homepage.
3. Click the Pixel Helper icon in the toolbar.
4. Confirm: PageView event shows with your pixel ID and status "Successful."
5. Open the Request to Book form, submit a test. Confirm: Lead event shows in Pixel Helper.
6. In Meta Events Manager, go to Test Events. Enter your site URL and use the test event tool to confirm events are arriving in real time.
