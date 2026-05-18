# Contact Page: Optimization Audit

Page: /contact/
Last updated: 2026-05-18

---

## Score Summary

| Dimension | Before | After | Change |
|---|---|---|---|
| Luxury Positioning | 4 | 7 | +3 |
| Emotional Conversion | 3 | 7 | +4 |
| Mobile UX | 5 | 8 | +3 |
| Trust | 4 | 7 | +3 |
| Backend Readiness | 2 | 7 | +5 |
| Analytics Readiness | 2 | 8 | +6 |
| SEO | 4 | 7 | +3 |
| Performance | 7 | 7 | 0 |
| **Overall** | **3.9** | **7.3** | **+3.4** |

---

## Score Notes

### Why the contact page scores lower than experience pages

A score of 7.3 is correct for a contact page. This page is not a conversion destination. Its job is to handle general inquiries cleanly and prevent intent leakage into the booking pipeline. A contact page that does those two things well is a 7/10 page. Pushing for a higher score would require adding conversion pressure that does not belong on this page.

### Emotional Conversion: 7 (not a high-conversion page by design)

The +4 improvement comes from the booking redirect banner, which recovers intent that would otherwise be lost. Before this optimization, a visitor who intended to book but landed on the contact page would either fill out the wrong form (losing all UTM and Airtable routing) or leave. The redirect banner routes booking intent to the correct pipeline before they reach the contact form. This is not conversion pressure: it is correct routing.

### Backend Readiness: 7 (M-CONTACT-001 spec complete, build required)

Score of 7, not 8 or above, because the Make.com scenario M-CONTACT-001 has not yet been built. The specification is complete. Once the scenario is built and the webhook URL is wired into contact-html-snippets.html, this score moves to 9.

### Analytics Readiness: 8 (events documented, DLV build required)

Score of 8 because the dlv_inquiry_type data layer variable has not yet been created in GTM. Events are documented, the dataLayer push is in the form JS, and GTM tags and triggers are specified. Once dlv_inquiry_type is created, this score moves to 9.

### Performance: 7 (unchanged)

No performance changes were made in this optimization pass. The contact page is a lightweight page with no media-heavy sections. Performance score remains at 7 and is not a priority item for this page.

---

## Before: What Was Missing

- No clear separation between booking inquiries and general inquiries
- No booking redirect: visitors with booking intent filled out the wrong form, losing UTM attribution, Airtable routing, and automated email follow-up
- No Make.com routing for contact form submissions: form data had no defined destination
- No analytics events specific to the contact page
- No inquiry type categorization: all contact submissions appeared identical in any backend system
- Metadata was generic and lacked proper OG and Twitter Card tags
- Form inputs were not tap-friendly on mobile
- Contact details were not structured for global JS phone/location link conversion

---

## After: What Changed

- Booking redirect banner added above the contact form: visible, prominent, non-aggressive
- M-CONTACT-001 scenario specified with full module-by-module instructions
- Airtable mapping defined: Requests table, Request_Type = "General Inquiry", Notes field combines message and inquiry type
- Inquiry type dropdown with 5 categorized options
- Analytics events documented: view_contact_page, submit_contact_form with inquiry_type parameter, click_request_to_book
- New DLV dlv_inquiry_type specified for GTM
- GTM tag and trigger setup documented
- Metadata updated: title, meta description, full OG set, Twitter Card, canonical
- Form inputs styled to minimum 44px height on mobile
- Contact details structured with .sss-phone and .sss-location classes for global JS compatibility
- Inline form handler JS: no external dependencies, dataLayer push on success, error handling
- No UTM fields in the contact form payload (correct: contact is not a booking)

---

## Remaining Gaps

### Build required: M-CONTACT-001 scenario

The Make.com scenario must be built before the contact form is live. Until M-CONTACT-001 exists:
- The WIRE_THIS_CONTACT_WEBHOOK_URL placeholder in contact-html-snippets.html is not a real endpoint
- Form submissions will fail silently or return a network error
- No Airtable records will be created
- No acknowledgment emails will be sent

Action: Build M-CONTACT-001 in Make.com, copy the webhook URL, replace WIRE_THIS_CONTACT_WEBHOOK_URL in contact-html-snippets.html. See contact-backend.md for the full scenario specification.

### Build required: dlv_inquiry_type in GTM

The data layer variable dlv_inquiry_type must be created in Google Tag Manager before the submit_contact_form GA4 tag can capture the inquiry_type parameter. Until it is created, the inquiry_type dimension will be blank in GA4 reports.

Action: In GTM, create a Data Layer Variable named dlv_inquiry_type, mapped to data layer key inquiry_type. Assign it to the inquiry_type parameter in the submit_contact_form GA4 Event Tag. Publish a new GTM container version.

### Replace OG image placeholder

contact-metadata.html contains PLACEHOLDER_OG_IMAGE_URL in the og:image and twitter:image tags. This must be replaced with a real image URL before the page is published. A landscape yacht image at 1200x630px is recommended.

---

## What This Optimization Does Not Change

- The booking form at /request-to-book/ and its pipeline are unchanged
- The M-BRAND-ROUTER scenario is unchanged
- The UTM tracking pipeline is unchanged
- Global JS (phone/location conversion, scroll depth, click tracking) is not modified by these files
- The contact page does not attempt to be a conversion page: it handles non-booking inquiries and redirects booking intent cleanly
