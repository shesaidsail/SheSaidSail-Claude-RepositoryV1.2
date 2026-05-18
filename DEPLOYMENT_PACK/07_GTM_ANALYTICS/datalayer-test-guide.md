# She Said Sail: DataLayer Test Guide

How to verify all GTM events are firing correctly before publishing the GTM container to production.

---

## Step 1: Open GTM Preview Mode

1. Log in to Google Tag Manager at tagmanager.google.com.
2. Select the She Said Sail container (GTM-TZ5KNRTH).
3. Click the Preview button (top right). A new browser tab opens with the GTM debug panel connected to a preview session.
4. The GTM debug panel (Tag Assistant) shows at the bottom of the preview browser tab.

---

## Step 2: Open the Site in the Preview Browser Tab

1. In the Tag Assistant tab that opened, enter the site URL: `https://shesaidsail.com`
2. Click Connect. The site opens with the GTM debug panel active.
3. The debug panel shows all tags, triggers, and dataLayer events as you interact with the site.

---

## Step 3: Verify Each Event

### Event: view_homepage

**Action:** Load the homepage (no user interaction required).

**GTM Debug Panel:** In the left sidebar, click the page load event. Under Tags Fired, confirm:
- GA4 - Configuration is listed
- GA4 - view_homepage is listed
- Meta Pixel - Base Code is listed
- TikTok Pixel - Base Code is listed

**Parameters to verify:** Click GA4 - view_homepage. Under Event Parameters, confirm:
- `page_path` is present (value: `/`)
- `page_title` is present

**Pass criteria:** All 4 tags listed above are in the Tags Fired section. No errors shown in red.

---

### Event: view_request_page

**Action:** Navigate to `/request-to-book/`.

**GTM Debug Panel:** Click the new page view event. Under Tags Fired, confirm:
- GA4 - view_request_page is listed

**Parameters to verify:** `page_path` = `/request-to-book/`

**Pass criteria:** Tag fires on page load without user interaction.

---

### Event: view_experiences_page

**Action:** Navigate to `/experiences/`.

**GTM Debug Panel:** Confirm GA4 - view_experiences_page is in Tags Fired.

**Parameters to verify:** `page_path` = `/experiences/`

**Pass criteria:** Tag fires on page load.

---

### Event: click_request_to_book

**Action:** On the homepage, click the primary CTA button (e.g., "Request to Book" in the hero section).

**GTM Debug Panel:** A new event appears in the left sidebar. Click it. Under Tags Fired, confirm:
- GA4 - click_request_to_book is listed
- TikTok Pixel - ViewContent is listed

**Parameters to verify:**
- `cta_location` is present and shows the correct location (e.g., "hero", "nav", "bottom-section")
- `page_path` is present

**Pass criteria:** `cta_location` accurately reflects where the button is on the page. Different CTA locations should show different values.

---

### Event: click_experience_card

**Action:** On `/experiences/`, click one of the 4 experience cards.

**GTM Debug Panel:** Confirm GA4 - click_experience_card fires.

**Parameters to verify:**
- `experience_name` is present (e.g., "Monaco Social")
- `card_position` is present (integer: 1, 2, 3, or 4)

**Pass criteria:** `experience_name` matches the card that was clicked. `card_position` reflects the card's position in the grid.

---

### Event: start_booking_form

**Action:** On `/request-to-book/`, click into the first form field (Full Name or Email).

**GTM Debug Panel:** Confirm GA4 - start_booking_form fires on first field focus.

**Parameters to verify:** `form_id` is present.

**Pass criteria:** Event fires exactly once per page session, on the first field interaction. It should not fire again if the user clicks into a second field.

---

### Event: submit_booking_form

**Action:** Complete and submit the Request to Book form with valid test data.

**GTM Debug Panel:** Confirm these tags fire:
- GA4 - submit_booking_form
- Meta Pixel - Lead (submit_booking_form)
- TikTok Pixel - SubmitForm

**Parameters to verify:**
- `occasion` is present and matches what was selected on the form
- `group_size` is present as a number
- `experience_interest` is present

**Pass criteria:** All 3 tags fire. Parameters contain the actual form values, not empty strings.

---

### Event: view_thank_you_page

**Action:** After a successful form submission, confirm the page redirects to `/thank-you/`.

**GTM Debug Panel:** On the thank you page load, confirm:
- GA4 - view_thank_you_page fires
- TikTok Pixel - CompleteRegistration fires

**Parameters to verify:** `conversion_type` = "booking_inquiry"

**Pass criteria:** Both tags fire on page load without any user action.

---

### Event: submit_email_capture

**Action:** On the homepage, submit the email capture form.

**GTM Debug Panel:** Confirm:
- GA4 - submit_email_capture fires
- TikTok Pixel - Subscribe fires

**Pass criteria:** Both tags fire after a successful email submit.

---

### Event: click_phone

**Action:** Click the phone number link on any page.

**GTM Debug Panel:** Confirm GA4 - click_phone fires.

**Parameters to verify:** `page_path` is present.

**Pass criteria:** Tag fires on tap/click. Works on mobile simulation (switch to mobile viewport in DevTools).

---

### Event: scroll_50_percent

**Action:** Scroll down the homepage past the halfway point.

**GTM Debug Panel:** Confirm GA4 - scroll_50_percent fires when you pass 50% scroll depth.

**Pass criteria:** Event fires exactly once per page load at 50% depth, not repeatedly.

---

### Event: scroll_90_percent

**Action:** Scroll to near the bottom of any page.

**GTM Debug Panel:** Confirm GA4 - scroll_90_percent fires at 90% scroll depth.

**Pass criteria:** Event fires exactly once per page load at 90% depth.

---

## DataLayer Verification Snippet

Paste this into the browser console to see only She Said Sail relevant events in the dataLayer. This filters out noise from third-party scripts.

```javascript
window.dataLayer.filter(function(e) {
  return e.event && (
    e.event.startsWith('chatbot_') ||
    ['view_homepage', 'view_request_page', 'view_experiences_page', 'view_experience_page',
     'view_about_page', 'view_contact_page', 'view_faq_page', 'view_journal_page',
     'click_request_to_book', 'click_explore_experiences', 'click_experience_card',
     'start_booking_form', 'submit_booking_form', 'submit_email_capture',
     'click_phone', 'view_thank_you_page',
     'scroll_50_percent', 'scroll_90_percent'].includes(e.event)
  );
});
```

This returns an array of all matching dataLayer pushes. Each object should show the event name and its parameters.

**Example of what a correct submit_booking_form entry looks like:**
```json
{
  "event": "submit_booking_form",
  "occasion": "Bachelorette",
  "group_size": 11,
  "experience_interest": "Monaco Social",
  "form_id": "request-to-book",
  "page_path": "/request-to-book/"
}
```

---

## Pass Criteria Summary

| Event | Tags Must Fire | Parameters Must Be Present |
|---|---|---|
| view_homepage | GA4 Config, GA4 view_homepage, Meta Base, TikTok Base | page_path, page_title |
| view_request_page | GA4 view_request_page | page_path |
| view_experiences_page | GA4 view_experiences_page | page_path |
| click_request_to_book | GA4 click_request_to_book, TikTok ViewContent | cta_location (non-empty), page_path |
| click_experience_card | GA4 click_experience_card | experience_name (non-empty), card_position (integer) |
| start_booking_form | GA4 start_booking_form | form_id |
| submit_booking_form | GA4 submit_booking_form, Meta Lead, TikTok SubmitForm | occasion, group_size (number), experience_interest |
| submit_email_capture | GA4 submit_email_capture, TikTok Subscribe | page_path |
| view_thank_you_page | GA4 view_thank_you_page, TikTok CompleteRegistration | conversion_type |
| click_phone | GA4 click_phone | page_location |
| scroll_50_percent | GA4 scroll_50_percent | page_location |
| scroll_90_percent | GA4 scroll_90_percent | page_location |
| chatbot_open | GA4 chatbot_open | page_location |
| chatbot_start_conversation | GA4 chatbot_start_conversation | page_location |
| chatbot_select_occasion | GA4 chatbot_select_occasion | occasion (non-empty), page_location |
| chatbot_select_experience | GA4 chatbot_select_experience | experience_slug (non-empty), page_location |
| chatbot_capture_email | GA4 chatbot_capture_email, Meta Lead | page_location |
| chatbot_capture_phone | GA4 chatbot_capture_phone | page_location |
| chatbot_handoff | GA4 chatbot_handoff, Meta Lead | experience_slug, occasion, page_location |
| chatbot_complete | GA4 chatbot_complete | page_location |

All events must pass before publishing the GTM container. After all pass, click Publish in GTM, give the version a name (e.g., "v1 - She Said Sail Full Event Set"), and submit.

**Note:** The chatbot events require the chatbot widget to be loaded on the page. Test chatbot events on the homepage or an experience page (not /request-to-book/ where the chatbot does not auto-trigger).
