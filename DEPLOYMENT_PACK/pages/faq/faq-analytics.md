# FAQ Page: Analytics Documentation

**Page:** /faq/
**Slug:** faq

---

## Events That Fire on This Page

### view_faq_page
- **Trigger:** Page load on /faq/ path
- **Source:** Global JS (added in Batch 3 JS update) detects the path and pushes this event automatically
- **No additional implementation required on this page**
- **Parameters:** none beyond standard GA4 page data (page_location, page_title)

### click_request_to_book
- **Trigger:** Click on the "Request to Book" button in the bottom CTA section
- **Source:** Global JS detects clicks on links pointing to /request-to-book/ and fires this event site-wide
- **Element:** `.sss-faq-cta-btn-primary` (href="/request-to-book/")

### click_explore_experiences
- **Trigger:** Click on the "View the Experiences" ghost button in the bottom CTA section
- **Source:** Global JS detects clicks on links pointing to /experiences/
- **Element:** `.sss-faq-cta-btn-ghost` (href="/experiences/")

### scroll_50_percent
- **Trigger:** User scrolls to 50% of page height
- **Source:** Global JS scroll depth tracking, fires automatically on all pages

### scroll_90_percent
- **Trigger:** User scrolls to 90% of page height
- **Source:** Global JS scroll depth tracking, fires automatically on all pages

---

## Events That Do Not Apply to This Page

**click_faq_item:** Not implemented. There is no accordion on this page. All 18 answers are permanently visible in the HTML. There is no per-question interaction to track.

---

## GTM Setup Required

### Custom Event Trigger
- **Trigger name:** CE - view_faq_page
- **Trigger type:** Custom Event
- **Event name:** view_faq_page
- **This trigger fires on:** All custom events where Event Name equals view_faq_page

### GA4 Event Tag
- **Tag name:** GA4 - view_faq_page
- **Tag type:** Google Analytics: GA4 Event
- **Configuration tag:** (existing GA4 Configuration tag)
- **Event name:** view_faq_page
- **Trigger:** CE - view_faq_page

Note: click_request_to_book and click_explore_experiences already have GTM triggers and tags from the global site setup (Batch 3). No new tags needed for those events.

---

## SEO Monitoring Note

After publishing the FAQPage JSON-LD schema in faq-metadata.html, monitor Google Search Console for FAQ rich result appearance:

1. Go to Google Search Console for shesaidsail.com
2. Navigate to Enhancements in the left sidebar
3. Look for an FAQ entry after Google has crawled the updated page
4. Use the Rich Results Test at search.google.com/test/rich-results to check eligibility before and after publish

Rich snippet appearance takes time after publish. It is not verifiable pre-launch.

---

## GA4 Audience: "Visited FAQ - No Submit"

This is a high-intent remarketing audience. FAQ visitors are close to booking. They have researched the product in detail. Capturing them for retargeting captures near-converters.

**Audience name:** Visited FAQ - No Submit
**Audience definition:**
- Include: users who triggered view_faq_page at least once in the last 30 days
- Exclude: users who triggered submit_booking_form at least once in the same period

**Setup location:** GA4 Admin, Audiences section
**Estimated use:** Google Ads or Meta retargeting campaigns targeting high-intent visitors who have not yet submitted a booking request

**Create this audience after:**
- GTM is published with the view_faq_page tag live
- At least 7 days of data have accumulated to confirm the event is firing correctly
- The GA4 Audience Builder shows view_faq_page as an available event condition

---

## Summary Table

| Event | Source | GTM Tag Needed | Notes |
|---|---|---|---|
| view_faq_page | Global JS | Yes (new) | Fires on page load |
| click_request_to_book | Global JS | No (existing) | Bottom CTA primary button |
| click_explore_experiences | Global JS | No (existing) | Bottom CTA ghost button |
| scroll_50_percent | Global JS | No (existing) | Auto on all pages |
| scroll_90_percent | Global JS | No (existing) | Auto on all pages |
