# Journal Analytics Notes
Page: /journal/
File: journal-analytics.md

---

## Events Fired on the Journal Index Page

### view_journal_page
- Trigger: page load on any URL matching /journal/ or /blog/ path.
- Source: global JS (added in Batch 3 JS update). No additional code needed per page.
- Parameters: none required. The GA4 default page_location and page_title dimensions capture the URL and document title automatically.
- GTM setup: create a Custom Event Trigger named "CE - view_journal_page" that fires when the dataLayer event equals "view_journal_page". Create a GA4 Event Tag named "view_journal_page" using that trigger.

### click_request_to_book
- Trigger: any click on a CTA or link pointing to /request-to-book/, including the Article Page CTA Block placed at the bottom of individual articles.
- Source: global JS fires this automatically on matching link hrefs. No additional code needed.
- Note: this event fires on the journal index page only if a /request-to-book/ link is added to the index. Currently the index page has no such link. The Article Page CTA Block on individual articles does fire this event.

### click_explore_experiences
- Trigger: any click on a link pointing to /experiences/.
- Source: global JS fires automatically on matching link hrefs.
- Note: same as above. The Article Page CTA Block on individual articles fires this event.

### scroll_50_percent and scroll_90_percent
- Trigger: user scrolls to 50% and 90% of the page height on the journal index.
- Source: global JS scroll depth listener on all pages.
- GTM setup: these events are already included in the global scroll depth configuration. No additional GTM tags are needed specifically for the journal index.

---

## Individual Article Page Tracking

The global JS does not currently fire a specific event for individual article page views. Standard GA4 page_view events will capture article visits, but no named custom event distinguishes article reads from other page views.

Recommended future enhancement: add logic to the global JS that detects when the current path matches the pattern /journal/[anything]/ and pushes a view_article_page event to the dataLayer with an article_slug parameter derived from the URL path segment. This would enable article-level funnel analysis and per-topic performance reporting in GA4.

Example dataLayer push for future implementation:

```javascript
if (window.location.pathname.match(/^\/journal\/.+\//)) {
  const slug = window.location.pathname.split('/').filter(Boolean)[1];
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'view_article_page',
    article_slug: slug
  });
}
```

---

## GA4 Audience: Journal Readers with No Form Submission

Name: Journal Readers - No Form Submit
Purpose: Top-of-funnel organic traffic segment for remarketing with experience-focused ads.

Definition:
- Include: users who triggered view_journal_page (visited /journal/ or /blog/).
- Exclude: users who triggered submit_booking_form.

This audience captures readers who found She Said Sail through organic search or social content, engaged with the journal, but have not yet submitted a booking request. Remarketing to this audience with experience-focused creative keeps She Said Sail visible during the consideration phase.

---

## GTM Configuration Summary

Tag: view_journal_page
- Tag type: GA4 Event
- Event name: view_journal_page
- Trigger: CE - view_journal_page (Custom Event, event name equals "view_journal_page")

Trigger: CE - view_journal_page
- Trigger type: Custom Event
- Event name: view_journal_page

Note: click_request_to_book, click_explore_experiences, scroll_50_percent, and scroll_90_percent are handled by the global JS and existing GTM tags from the Batch 3 setup. No additional tags are needed for these events specifically for the journal page.
