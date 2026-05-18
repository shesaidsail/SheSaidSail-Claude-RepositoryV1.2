# FAQ Page: Backend Integration Notes

**Page:** /faq/
**Slug:** faq

---

## Backend Summary

This page has no backend integration of its own. It is a pure content page.

There are no forms on the FAQ page. No Airtable writes occur from this page. No Make.com scenarios are triggered by visiting or interacting with the FAQ page.

---

## How Booking Flow Connects

The bottom CTA on this page links directly to /request-to-book/. That page contains the full booking form, which triggers:

- Airtable record creation in the Inquiries table
- Make.com scenario for concierge notification and autoresponder email
- GTM event: submit_booking_form

The FAQ page's role is to remove friction before the visitor arrives at that form. It does not participate in the form submission flow itself.

---

## SEO Integration Note

The FAQPage JSON-LD schema in faq-metadata.html is the primary technical integration for this page. Key points:

- All 18 questions are included in the schema as Question entities with acceptedAnswer text.
- Google may surface these as FAQ rich results in search, expanding the page's search footprint beyond a standard blue link.
- Rich result appearance is not guaranteed and is at Google's discretion. Monitor Google Search Console (Enhancements section) after publishing to confirm eligibility.
- The schema validates against schema.org FAQPage specification. Validate at validator.schema.org before publishing.

---

## Crawlability Note

Because all answers are rendered as visible HTML with no JavaScript accordion, Google's crawler reads the full answer text on every crawl. This means the 18 answers are indexed as page content, contributing to keyword coverage for long-tail searches such as:

- "what is included in a yacht charter miami"
- "how far in advance to book a yacht"
- "yacht charter miami deposit"
- "weather cancellation yacht charter"
- "private yacht charter miami group size"

No additional backend configuration is required to support this. The visible HTML structure handles it.

---

## No Action Required

This page requires no backend setup, no API keys, no webhook configuration, and no Airtable table modifications. Deploy the HTML and metadata files and the page is complete.
