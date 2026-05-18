# Contact Page: Analytics Specification

Page: /contact/
Last updated: 2026-05-18

---

## Events Overview

| Event Name | Fired By | When |
|---|---|---|
| view_contact_page | Global JS | On page load when path is /contact/ |
| submit_contact_form | Inline form JS (contact-html-snippets.html) | On successful form submission |
| click_request_to_book | Global JS | When visitor clicks any link to /request-to-book/ |
| scroll_50_percent | Global JS | When page scroll depth reaches 50% |
| scroll_90_percent | Global JS | When page scroll depth reaches 90% |

---

## Event Details

### view_contact_page
- Fired by: global JS, path check on /contact/
- No additional parameters needed
- This is a standard page-view-level event. GA4 will also capture the standard page_view event. view_contact_page is the custom event for audience building and filtering.

### submit_contact_form
- Fired by: inline IIFE in the script tag at the bottom of contact-html-snippets.html
- Pushed to window.dataLayer immediately after a successful HTTP response from the Make.com webhook
- Payload pushed to dataLayer:
  ```js
  {
    event: 'submit_contact_form',
    inquiry_type: inquiryType,     // string, one of the 5 dropdown values
    page_location: window.location.href
  }
  ```
- Do NOT mark this event as a conversion in GA4 or Google Ads. Contact form submissions are not bookings. Marking them as conversions dilutes booking conversion data and distorts ROAS calculations.

### click_request_to_book
- Fired by: global JS, listens for clicks on links with href containing /request-to-book/
- This fires on the "Request to Book" button inside the booking redirect banner on the contact page
- Useful for measuring how many contact page visitors are redirected to the booking flow

### scroll_50_percent, scroll_90_percent
- Fired by: global JS scroll depth tracker
- Useful for measuring engagement depth on the contact page
- No additional setup needed beyond what is already in global JS

---

## New Data Layer Variable (DLV) Required

A new DLV must be created in Google Tag Manager before the submit_contact_form GA4 tag can capture the inquiry_type parameter.

### dlv_inquiry_type
- Variable type: Data Layer Variable
- Data Layer Variable Name: inquiry_type
- Default value: (leave blank)
- Version: Version 2

This DLV reads the inquiry_type value pushed to dataLayer by the contact form IIFE. It is used as a parameter in the submit_contact_form GA4 Event Tag.

---

## GTM Setup: Required Tags and Triggers

### 1. Custom Event Trigger: CE - view_contact_page
- Trigger type: Custom Event
- Event name: view_contact_page
- This trigger fires: All Custom Events matching the event name

### 2. GA4 Event Tag: view_contact_page
- Tag type: GA4 Event
- Configuration tag: existing GA4 Configuration Tag
- Event name: view_contact_page
- Trigger: CE - view_contact_page

### 3. Custom Event Trigger: CE - submit_contact_form
- Trigger type: Custom Event
- Event name: submit_contact_form
- This trigger fires: All Custom Events matching the event name

### 4. GA4 Event Tag: submit_contact_form
- Tag type: GA4 Event
- Configuration tag: existing GA4 Configuration Tag
- Event name: submit_contact_form
- Event parameters:
  - Parameter name: inquiry_type
  - Value: {{dlv_inquiry_type}}
- Trigger: CE - submit_contact_form

---

## GA4 Audience Note

Use the submit_contact_form event to exclude contact page submitters from booking remarketing audiences. Visitors who submitted the contact form have a different intent than visitors who abandoned the booking form. Mixing them in the same remarketing audience reduces ad relevance and wastes spend.

Suggested audience exclusion logic in GA4:
- Audience: "Booking Abandoners" (or equivalent)
- Exclude users where event_name equals submit_contact_form

Alternatively, use submit_contact_form to build a separate "Contact Inquiry" audience for nurture campaigns if a separate email or retargeting nurture sequence exists for non-booking contacts.

---

## No Conversion Flag

submit_contact_form must NOT be set as a conversion in GA4 or Google Ads. Contact is not a booking. The booking conversion event is the existing event on the /thank-you/ or post-booking confirmation page. Do not dilute that conversion data.
