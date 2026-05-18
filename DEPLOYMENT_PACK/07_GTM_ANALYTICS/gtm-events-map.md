# She Said Sail: GTM Events Map

Master reference for all 14 custom events. Use this to configure GTM Tags, Triggers, and Variables. The table below shows every event, what triggers it, what parameters it carries, and which ad platforms receive it.

---

## Events Reference Table

| Event Name | Trigger Condition | Parameters | GA4 | Meta Pixel | TikTok Pixel |
|---|---|---|---|---|---|
| `view_homepage` | Page URL matches `/` (homepage) | `page_path`, `page_title` | Yes | PageView (base) | PageView (base) |
| `view_request_page` | Page URL matches `/request-to-book/` | `page_path`, `page_title` | Yes | No (page view covered by base) | No |
| `view_experiences_page` | Page URL matches `/experiences/` | `page_path`, `page_title` | Yes | No | No |
| `click_request_to_book` | Click on any element with class `.sss-cta-request` or ID `#cta-request-to-book` | `cta_location` (e.g., "hero", "nav", "bottom-section"), `page_path` | Yes | No | No |
| `click_explore_experiences` | Click on any element with class `.sss-cta-experiences` | `page_path` | Yes | No | No |
| `click_experience_card` | Click on any `.experience-card` or `.sss-card` element | `experience_name` (e.g., "Monaco Social"), `card_position` (integer: 1, 2, 3, 4) | Yes | No | No |
| `start_booking_form` | First interaction with any field inside the Request to Book form (focus event) | `form_id`, `page_path` | Yes | No | No |
| `submit_booking_form` | Successful MetForm submission on `/request-to-book/` | `occasion`, `group_size` (integer), `experience_interest`, `form_id` | Yes, Conversion | Lead | SubmitForm |
| `submit_email_capture` | Successful email capture form submission on homepage | `page_path` | Yes, Micro-Conversion | No | Subscribe |
| `click_phone` | Click on any `<a href="tel:...">` element | `phone_number`, `page_path` | Yes | No | No |
| `open_chat` | Click on Tidio chat widget open button | `page_path` | Yes | No | No |
| `view_thank_you_page` | Page URL matches `/thank-you/` | `page_path`, `conversion_type` ("booking_inquiry") | Yes, Conversion | Lead | CompleteRegistration |
| `scroll_50_percent` | User scrolls to 50% of page depth | `page_path` | Yes | No | No |
| `scroll_90_percent` | User scrolls to 90% of page depth | `page_path` | Yes, Micro-Conversion | No | No |

---

## GTM Variables Required

| Variable Name | Variable Type | Configuration |
|---|---|---|
| DLV - event | Data Layer Variable | Key: `event` |
| DLV - page_path | Data Layer Variable | Key: `page_path` |
| DLV - cta_location | Data Layer Variable | Key: `cta_location` |
| DLV - occasion | Data Layer Variable | Key: `occasion` |
| DLV - group_size | Data Layer Variable | Key: `group_size` |
| DLV - experience_name | Data Layer Variable | Key: `experience_name` |
| DLV - card_position | Data Layer Variable | Key: `card_position` |
| DLV - experience_interest | Data Layer Variable | Key: `experience_interest` |
| DLV - form_id | Data Layer Variable | Key: `form_id` |
| DLV - conversion_type | Data Layer Variable | Key: `conversion_type` |
| CJS - Page Path | Custom JavaScript | Returns `window.location.pathname` |
| CJS - Page Title | Custom JavaScript | Returns `document.title` |

---

## GTM Triggers Required

| Trigger Name | Trigger Type | Configuration |
|---|---|---|
| CE - view_homepage | Custom Event | Event name: `view_homepage` |
| CE - view_request_page | Custom Event | Event name: `view_request_page` |
| CE - view_experiences_page | Custom Event | Event name: `view_experiences_page` |
| CE - click_request_to_book | Custom Event | Event name: `click_request_to_book` |
| CE - click_explore_experiences | Custom Event | Event name: `click_explore_experiences` |
| CE - click_experience_card | Custom Event | Event name: `click_experience_card` |
| CE - start_booking_form | Custom Event | Event name: `start_booking_form` |
| CE - submit_booking_form | Custom Event | Event name: `submit_booking_form` |
| CE - submit_email_capture | Custom Event | Event name: `submit_email_capture` |
| CE - click_phone | Custom Event | Event name: `click_phone` |
| CE - open_chat | Custom Event | Event name: `open_chat` |
| CE - view_thank_you_page | Custom Event | Event name: `view_thank_you_page` |
| CE - scroll_50_percent | Custom Event | Event name: `scroll_50_percent` |
| CE - scroll_90_percent | Custom Event | Event name: `scroll_90_percent` |
| All Pages | Page View | All pages |

---

## GTM Tags Required

| Tag Name | Tag Type | Trigger | Configuration |
|---|---|---|---|
| GA4 - Configuration | Google Analytics: GA4 Configuration | All Pages | Measurement ID: GT-WV3X86GZ |
| GA4 - view_homepage | Google Analytics: GA4 Event | CE - view_homepage | Event name: `view_homepage`. Parameters: page_path, page_title. |
| GA4 - view_request_page | Google Analytics: GA4 Event | CE - view_request_page | Event name: `view_request_page`. Parameters: page_path. |
| GA4 - view_experiences_page | Google Analytics: GA4 Event | CE - view_experiences_page | Event name: `view_experiences_page`. Parameters: page_path. |
| GA4 - click_request_to_book | Google Analytics: GA4 Event | CE - click_request_to_book | Event name: `click_request_to_book`. Parameters: cta_location, page_path. |
| GA4 - click_explore_experiences | Google Analytics: GA4 Event | CE - click_explore_experiences | Event name: `click_explore_experiences`. Parameters: page_path. |
| GA4 - click_experience_card | Google Analytics: GA4 Event | CE - click_experience_card | Event name: `click_experience_card`. Parameters: experience_name, card_position. |
| GA4 - start_booking_form | Google Analytics: GA4 Event | CE - start_booking_form | Event name: `start_booking_form`. Parameters: form_id. |
| GA4 - submit_booking_form | Google Analytics: GA4 Event | CE - submit_booking_form | Event name: `submit_booking_form`. Parameters: occasion, group_size, experience_interest. |
| GA4 - submit_email_capture | Google Analytics: GA4 Event | CE - submit_email_capture | Event name: `submit_email_capture`. Parameters: page_path. |
| GA4 - click_phone | Google Analytics: GA4 Event | CE - click_phone | Event name: `click_phone`. Parameters: page_path. |
| GA4 - open_chat | Google Analytics: GA4 Event | CE - open_chat | Event name: `open_chat`. Parameters: page_path. |
| GA4 - view_thank_you_page | Google Analytics: GA4 Event | CE - view_thank_you_page | Event name: `view_thank_you_page`. Parameters: conversion_type. |
| GA4 - scroll_50_percent | Google Analytics: GA4 Event | CE - scroll_50_percent | Event name: `scroll_50_percent`. Parameters: page_path. |
| GA4 - scroll_90_percent | Google Analytics: GA4 Event | CE - scroll_90_percent | Event name: `scroll_90_percent`. Parameters: page_path. |
| Meta Pixel - Base Code | Custom HTML | All Pages | See `meta-pixel-events.md` for code. |
| Meta Pixel - Lead | Custom HTML | CE - submit_booking_form | See `meta-pixel-events.md` for code. |
| TikTok Pixel - Base Code | Custom HTML | All Pages | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - SubmitForm | Custom HTML | CE - submit_booking_form | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - CompleteRegistration | Custom HTML | CE - view_thank_you_page | See `tiktok-pixel-events.md` for code. |
| TikTok Pixel - Subscribe | Custom HTML | CE - submit_email_capture | See `tiktok-pixel-events.md` for code. |
