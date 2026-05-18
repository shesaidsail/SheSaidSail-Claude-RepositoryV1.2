# Contact Page: QA Checklist

Page: /contact/
Last updated: 2026-05-18

Tester: _______________
Date tested: _______________
Environment: _______________

Legend: PASS / FAIL / N/A

---

## Desktop Layout (1440px)

| # | Check | Result | Notes |
|---|---|---|---|
| D1 | Page header renders with gold eyebrow, H1, and subline | | |
| D2 | Booking redirect banner is visible ABOVE the contact form | | |
| D3 | Redirect banner has left gold border and warm cream background | | |
| D4 | "Request to Book" button in banner is gold fill with navy text | | |
| D5 | Thin divider line separates banner from form | | |
| D6 | Contact form heading "Send us a message" renders in Cormorant Garamond | | |
| D7 | Contact form displays all 5 fields: name, email, inquiry type, message, submit | | |
| D8 | Contact details section renders in 3 columns | | |
| D9 | Contact details labels are gold uppercase, values are navy/text | | |

## Desktop Layout (1280px)

| # | Check | Result | Notes |
|---|---|---|---|
| D10 | No layout overflow or horizontal scroll | | |
| D11 | Form inputs do not exceed content column width | | |

---

## Mobile Layout (375px)

| # | Check | Result | Notes |
|---|---|---|---|
| M1 | Page header stacks cleanly, H1 readable at smaller size | | |
| M2 | Booking redirect banner stacks to single column | | |
| M3 | "Request to Book" button spans full width on mobile | | |
| M4 | Contact form is full width, no side overflow | | |
| M5 | All form inputs are tap-friendly: minimum 44px height | | |
| M6 | Select dropdown is tap-friendly and shows chevron | | |
| M7 | Contact details stack to single column | | |
| M8 | No text is truncated or cut off | | |

## Mobile Layout (390px)

| # | Check | Result | Notes |
|---|---|---|---|
| M9 | Layout identical to 375px behavior, no regressions | | |

---

## Booking Redirect

| # | Check | Result | Notes |
|---|---|---|---|
| R1 | Redirect banner is present on the page | | |
| R2 | Banner appears BEFORE the contact form in page order | | |
| R3 | "Request to Book" button links to /request-to-book/ | | |
| R4 | Button uses target="_self" (no new tab) | | |
| R5 | Banner does not appear salesy or pushy in tone | | |

---

## Form Fields

| # | Check | Result | Notes |
|---|---|---|---|
| F1 | Full Name field present (type="text", name="contact_name") | | |
| F2 | Email Address field present (type="email", name="contact_email") | | |
| F3 | Inquiry Type select present (name="inquiry_type") | | |
| F4 | Select has exactly 5 options (not counting placeholder) | | |
| F5 | Options: General Question, Press or Media, Partnership Inquiry, Event Planning Collaboration, Something Else | | |
| F6 | Message textarea present (name="contact_message", rows=6) | | |
| F7 | Submit button present with label "Send Message" | | |
| F8 | Required fields (name, email, inquiry_type, message) block submission if empty | | |
| F9 | Hidden field brand = "shesaidsail" present | | |
| F10 | Hidden field submission_page = "/contact/" present | | |
| F11 | Hidden field source_url is populated by JS with window.location.href | | |
| F12 | NO UTM hidden fields present (utm_source, utm_medium, etc.) | | |
| F13 | NO booking-specific hidden fields present (date_of_charter, guest_count, etc.) | | |

---

## Form Submission

| # | Check | Result | Notes |
|---|---|---|---|
| S1 | Form submits to Make.com webhook (M-CONTACT-001, real URL wired) | | |
| S2 | Payload includes all 7 fields: contact_name, contact_email, inquiry_type, contact_message, brand, submission_page, source_url | | |
| S3 | On success: form hides, .sss-ct-success message displays | | |
| S4 | Success message text: "Your message has been received. We will follow up within 48 hours." | | |
| S5 | On network error: .sss-ct-error message displays | | |
| S6 | Error message text: "Something went wrong. Please try again or email us directly." | | |
| S7 | Submit button is disabled during pending request | | |
| S8 | Airtable record created in Requests table with Request_Type = "General Inquiry" | | |
| S9 | Acknowledgment email received at submitted email address | | |
| S10 | Slack alert posted to #general-inquiries (if Module 3 enabled) | | |

---

## Analytics

| # | Check | Result | Notes |
|---|---|---|---|
| A1 | view_contact_page fires on page load (visible in GTM Preview) | | |
| A2 | submit_contact_form fires on successful submission (visible in GTM Preview) | | |
| A3 | submit_contact_form dataLayer push includes inquiry_type value | | |
| A4 | submit_contact_form dataLayer push includes page_location value | | |
| A5 | click_request_to_book fires when redirect banner button is clicked | | |
| A6 | scroll_50_percent fires at correct scroll depth | | |
| A7 | scroll_90_percent fires at correct scroll depth | | |
| A8 | dlv_inquiry_type DLV created in GTM and reading correct value | | |
| A9 | submit_contact_form is NOT marked as a conversion in GA4 | | |

---

## Phone and Location (Global JS)

| # | Check | Result | Notes |
|---|---|---|---|
| P1 | Phone number in contact details is converted to a tap-to-call tel: link by global JS | | |
| P2 | Location "Miami, FL" is converted to a Google Maps link by global JS | | |

---

## SEO and Metadata

| # | Check | Result | Notes |
|---|---|---|---|
| SE1 | Page title: "Contact She Said Sail | Private Yacht Experiences in Miami" | | |
| SE2 | Meta description matches specification | | |
| SE3 | OG title, description, type, url, site_name, locale all present | | |
| SE4 | OG image placeholder replaced with actual image URL before launch | | |
| SE5 | Twitter card type: summary_large_image | | |
| SE6 | Canonical URL: https://shesaidsail.com/contact/ | | |

---

## Brand and Tone

| # | Check | Result | Notes |
|---|---|---|---|
| B1 | No em dashes anywhere on the page | | |
| B2 | Booking redirect banner is prominent and appears before the form | | |
| B3 | No aggressive sales language on the contact page | | |
| B4 | Tone is direct and helpful, not corporate | | |
| B5 | Cormorant Garamond used for headings | | |
| B6 | Inter used for body text | | |
| B7 | Gold (#DAB97E) used correctly for accents, eyebrows, labels, and buttons | | |
| B8 | Navy (#1A2332) used for headings and primary text | | |

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| Designer | | | |
| Project Lead | | | |

Notes / issues found during QA:

_______________________________________________________________________________

_______________________________________________________________________________

_______________________________________________________________________________
