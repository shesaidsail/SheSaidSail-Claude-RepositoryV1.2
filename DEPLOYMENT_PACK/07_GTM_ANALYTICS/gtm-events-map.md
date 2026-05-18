# She Said Sail: GTM Events Map

Master reference for all 22 custom events (14 site events + 8 chatbot events). Use this to configure GTM Tags, Triggers, and Variables. The table below shows every event, what triggers it, what parameters it carries, and which ad platforms receive it.

**Important:** Tidio is disabled. All chat events come from chatbot-js.js. The legacy `open_chat` event has been retired and replaced with `chatbot_open`.

---

## Site Events (she-said-sail-global.js)

| Event Name | Trigger Condition | Parameters | GA4 | Meta Pixel | TikTok Pixel |
|---|---|---|---|---|---|
| `view_homepage` | Page URL matches `/` | `page_location` | Yes | PageView (base) | PageView (base) |
| `view_request_page` | Page URL matches `/request-to-book/` | `page_location` | Yes | No | No |
| `view_experiences_page` | Page URL matches `/experiences/` | `page_location` | Yes | No | No |
| `view_experience_page` | Page URL matches `/experience/*` | `experience_slug`, `page_location` | Yes | No | No |
| `view_about_page` | Page URL matches `/about/` | `page_location` | Yes | No | No |
| `view_contact_page` | Page URL matches `/contact/` | `page_location` | Yes | No | No |
| `view_faq_page` | Page URL matches `/faq/` | `page_location` | Yes | No | No |
| `view_journal_page` | Page URL matches `/journal/` | `page_location` | Yes | No | No |
| `view_thank_you_page` | Page URL matches `/thank-you/` | `page_location` | Yes, Conversion | Lead | CompleteRegistration |
| `click_request_to_book` | Click any `<a href*="request-to-book">` | `cta_location` (hero / nav / bottom-cta / email-capture / unknown), `page_location` | Yes, Conversion | No | No |
| `click_explore_experiences` | Click any `<a href*="/experiences/">` | `page_location` | Yes | No | No |
| `click_experience_card` | Click any `.e-loop-item a` | `experience_name`, `card_position` (integer 1-4), `page_location` | Yes | No | No |
| `start_booking_form` | First focus or change on booking form | `form_name` (request-to-book) | Yes | No | No |
| `submit_booking_form` | Booking form submit | `form_name`, `occasion`, `group_size` (integer) | Yes, Conversion | Lead | SubmitForm |
| `submit_email_capture` | Homepage email form submit | `form_location` | Yes, Micro-Conversion | No | Subscribe |
| `click_phone` | Click any `<a href="tel:...">` | `page_location` | Yes | No | No |
| `scroll_50_percent` | User scrolls to 50% of page depth | `page_location` | Yes | No | No |
| `scroll_90_percent` | User scrolls to 90% of page depth | `page_location` | Yes, Micro-Conversion | No | No |

---

## Chatbot Events (chatbot-js.js)

| Event Name | Trigger Condition | Parameters | GA4 | Meta Pixel | TikTok Pixel |
|---|---|---|---|---|---|
| `chatbot_open` | User clicks the chatbot toggle button | `page_location` | Yes | No | No |
| `chatbot_start_conversation` | First user message sent | `page_location` | Yes | No | No |
| `chatbot_select_occasion` | User selects or confirms an occasion | `occasion` (bachelorette / birthday / girls_trip / intimate / other), `page_location` | Yes | No | No |
| `chatbot_select_experience` | Bot recommends an experience and user confirms | `experience_slug` (monaco-social / golden-hour-escape / rose-day-club / pink-palm-club), `page_location` | Yes | No | No |
| `chatbot_capture_email` | User submits a valid email in the chatbot | `page_location` | Yes, Conversion | Lead | SubmitForm |
| `chatbot_capture_phone` | User submits a phone number in the chatbot | `page_location` | Yes, Conversion | No | No |
| `chatbot_handoff` | Webhook payload fired, handoff message shown | `experience_slug`, `occasion`, `page_location` | Yes, Conversion | Lead | CompleteRegistration |
| `chatbot_complete` | Conversation reaches STATE_CLOSED | `page_location` | Yes | No | No |

---

## GTM Variables Required

| Variable Name | Variable Type | Configuration |
|---|---|---|
| DLV - event | Data Layer Variable | Key: `event` |
| DLV - page_location | Data Layer Variable | Key: `page_location` |
| DLV - cta_location | Data Layer Variable | Key: `cta_location` |
| DLV - occasion | Data Layer Variable | Key: `occasion` |
| DLV - group_size | Data Layer Variable | Key: `group_size` |
| DLV - experience_name | Data Layer Variable | Key: `experience_name` |
| DLV - experience_slug | Data Layer Variable | Key: `experience_slug` |
| DLV - card_position | Data Layer Variable | Key: `card_position` |
| DLV - form_name | Data Layer Variable | Key: `form_name` |
| DLV - form_location | Data Layer Variable | Key: `form_location` |
| CJS - Page Location | Custom JavaScript | Returns `window.location.href` |

---

## GTM Triggers Required

### Site Triggers

| Trigger Name | Trigger Type | Configuration |
|---|---|---|
| CE - view_homepage | Custom Event | Event name: `view_homepage` |
| CE - view_request_page | Custom Event | Event name: `view_request_page` |
| CE - view_experiences_page | Custom Event | Event name: `view_experiences_page` |
| CE - view_experience_page | Custom Event | Event name: `view_experience_page` |
| CE - view_about_page | Custom Event | Event name: `view_about_page` |
| CE - view_contact_page | Custom Event | Event name: `view_contact_page` |
| CE - view_faq_page | Custom Event | Event name: `view_faq_page` |
| CE - view_journal_page | Custom Event | Event name: `view_journal_page` |
| CE - view_thank_you_page | Custom Event | Event name: `view_thank_you_page` |
| CE - click_request_to_book | Custom Event | Event name: `click_request_to_book` |
| CE - click_explore_experiences | Custom Event | Event name: `click_explore_experiences` |
| CE - click_experience_card | Custom Event | Event name: `click_experience_card` |
| CE - start_booking_form | Custom Event | Event name: `start_booking_form` |
| CE - submit_booking_form | Custom Event | Event name: `submit_booking_form` |
| CE - submit_email_capture | Custom Event | Event name: `submit_email_capture` |
| CE - click_phone | Custom Event | Event name: `click_phone` |
| CE - scroll_50_percent | Custom Event | Event name: `scroll_50_percent` |
| CE - scroll_90_percent | Custom Event | Event name: `scroll_90_percent` |
| All Pages | Page View | All pages |

### Chatbot Triggers

| Trigger Name | Trigger Type | Configuration |
|---|---|---|
| CE - chatbot_open | Custom Event | Event name: `chatbot_open` |
| CE - chatbot_start_conversation | Custom Event | Event name: `chatbot_start_conversation` |
| CE - chatbot_select_occasion | Custom Event | Event name: `chatbot_select_occasion` |
| CE - chatbot_select_experience | Custom Event | Event name: `chatbot_select_experience` |
| CE - chatbot_capture_email | Custom Event | Event name: `chatbot_capture_email` |
| CE - chatbot_capture_phone | Custom Event | Event name: `chatbot_capture_phone` |
| CE - chatbot_handoff | Custom Event | Event name: `chatbot_handoff` |
| CE - chatbot_complete | Custom Event | Event name: `chatbot_complete` |

---

## GTM Tags Required

### GA4 Tags

| Tag Name | Tag Type | Trigger | Key Parameters |
|---|---|---|---|
| GA4 - Configuration | GA4 Configuration | All Pages | Measurement ID: GT-WV3X86GZ |
| GA4 - view_homepage | GA4 Event | CE - view_homepage | event: view_homepage, page_location |
| GA4 - view_request_page | GA4 Event | CE - view_request_page | event: view_request_page, page_location |
| GA4 - view_experiences_page | GA4 Event | CE - view_experiences_page | event: view_experiences_page, page_location |
| GA4 - view_experience_page | GA4 Event | CE - view_experience_page | event: view_experience_page, experience_slug |
| GA4 - view_about_page | GA4 Event | CE - view_about_page | event: view_about_page |
| GA4 - view_contact_page | GA4 Event | CE - view_contact_page | event: view_contact_page |
| GA4 - view_faq_page | GA4 Event | CE - view_faq_page | event: view_faq_page |
| GA4 - view_journal_page | GA4 Event | CE - view_journal_page | event: view_journal_page |
| GA4 - view_thank_you_page | GA4 Event | CE - view_thank_you_page | event: view_thank_you_page, page_location (mark as Conversion) |
| GA4 - click_request_to_book | GA4 Event | CE - click_request_to_book | event: click_request_to_book, cta_location (mark as Conversion) |
| GA4 - click_explore_experiences | GA4 Event | CE - click_explore_experiences | event: click_explore_experiences |
| GA4 - click_experience_card | GA4 Event | CE - click_experience_card | event: click_experience_card, experience_name, card_position |
| GA4 - start_booking_form | GA4 Event | CE - start_booking_form | event: start_booking_form, form_name |
| GA4 - submit_booking_form | GA4 Event | CE - submit_booking_form | event: submit_booking_form, occasion, group_size (mark as Conversion) |
| GA4 - submit_email_capture | GA4 Event | CE - submit_email_capture | event: submit_email_capture (mark as Micro-Conversion) |
| GA4 - click_phone | GA4 Event | CE - click_phone | event: click_phone (mark as Conversion) |
| GA4 - scroll_50_percent | GA4 Event | CE - scroll_50_percent | event: scroll_50_percent |
| GA4 - scroll_90_percent | GA4 Event | CE - scroll_90_percent | event: scroll_90_percent (mark as Micro-Conversion) |
| GA4 - chatbot_open | GA4 Event | CE - chatbot_open | event: chatbot_open |
| GA4 - chatbot_start_conversation | GA4 Event | CE - chatbot_start_conversation | event: chatbot_start_conversation |
| GA4 - chatbot_select_occasion | GA4 Event | CE - chatbot_select_occasion | event: chatbot_select_occasion, occasion |
| GA4 - chatbot_select_experience | GA4 Event | CE - chatbot_select_experience | event: chatbot_select_experience, experience_slug |
| GA4 - chatbot_capture_email | GA4 Event | CE - chatbot_capture_email | event: chatbot_capture_email (mark as Conversion) |
| GA4 - chatbot_capture_phone | GA4 Event | CE - chatbot_capture_phone | event: chatbot_capture_phone (mark as Conversion) |
| GA4 - chatbot_handoff | GA4 Event | CE - chatbot_handoff | event: chatbot_handoff, experience_slug, occasion (mark as Conversion) |
| GA4 - chatbot_complete | GA4 Event | CE - chatbot_complete | event: chatbot_complete |

### Pixel Tags

| Tag Name | Tag Type | Trigger | Configuration |
|---|---|---|---|
| Meta Pixel - Base Code | Custom HTML | All Pages | See `meta-pixel-events.md` for code. |
| Meta Pixel - Lead (form) | Custom HTML | CE - submit_booking_form | See `meta-pixel-events.md` for code. |
| Meta Pixel - Lead (chatbot) | Custom HTML | CE - chatbot_handoff | See `meta-pixel-events.md` for code. |
| Meta Pixel - Lead (chatbot email) | Custom HTML | CE - chatbot_capture_email | See `meta-pixel-events.md` for code. |
| TikTok Pixel - Base Code | Custom HTML | All Pages | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - SubmitForm | Custom HTML | CE - submit_booking_form | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - CompleteRegistration | Custom HTML | CE - view_thank_you_page | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - Subscribe | Custom HTML | CE - submit_email_capture | See `tiktok-pixel-events.md` for code. |

---

## GA4 Custom Dimensions to Register

After building all tags, register these custom dimensions in GA4 Admin > Custom Definitions:

| Dimension Name | Scope | Parameter Key |
|---|---|---|
| Experience Slug | Event | experience_slug |
| Experience Name | Event | experience_name |
| Occasion | Event | occasion |
| CTA Location | Event | cta_location |
| Form Name | Event | form_name |

---

## Conversion Events in GA4

Mark these events as conversions in GA4 Admin > Events:

| Event | Conversion Rationale |
|---|---|
| `submit_booking_form` | Primary macro-conversion |
| `view_thank_you_page` | Secondary macro-conversion (confirms form submission complete) |
| `chatbot_handoff` | Chatbot macro-conversion |
| `chatbot_capture_email` | Chatbot email capture conversion |
| `chatbot_capture_phone` | Chatbot phone capture conversion |
| `click_request_to_book` | High-intent micro-conversion |
| `click_phone` | High-intent micro-conversion |
| `scroll_90_percent` | Engagement micro-conversion |
| `submit_email_capture` | Email acquisition micro-conversion |
