# She Said Sail: Tracking QA Checklist

Covers GTM, GA4, Meta Pixel, and TikTok Pixel. Complete after the global JS is deployed and before GTM is published to production.

Reviewer: _____________________ Date: _____________________

---

## Section A: GTM Container

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 1 | GTM container GTM-WWTT27Z3 is confirmed installed on the site (verify in page source: `GTM-WWTT27Z3` appears twice, once in the `<head>` and once in `<body>`) | | | |
| 2 | GTM Preview mode connects to the site without errors | | | |
| 3 | All 14 custom events are configured as GTM Triggers (CE - event_name format) | | | |
| 4 | All GA4 event Tags are configured (one Tag per event, 14 total) | | | |
| 5 | GA4 Configuration Tag is present with Measurement ID GT-WV3X86GZ and fires on All Pages | | | |
| 6 | Meta Pixel Base Code Tag is present and fires on All Pages | | | |
| 7 | TikTok Pixel Base Code Tag is present and fires on All Pages | | | |
| 8 | Meta Pixel Lead Tag fires on CE - submit_booking_form trigger only | | | |
| 9 | TikTok SubmitForm Tag fires on CE - submit_booking_form trigger only | | | |
| 10 | TikTok CompleteRegistration Tag fires on CE - view_thank_you_page trigger only | | | |
| 11 | GTM container has been Published (not just previewed). Version name set. | | | |

---

## Section B: All 14 Custom Events Verified in GTM Preview

Use GTM Preview mode and the dataLayer verification snippet from `datalayer-test-guide.md`.

| # | Event Name | Action Taken to Trigger | Verified in GTM Debug Panel | Pass | Fail |
|---|---|---|---|---|---|
| 12 | `view_homepage` | Load homepage | Yes/No | | |
| 13 | `view_request_page` | Load /request-to-book/ | Yes/No | | |
| 14 | `view_experiences_page` | Load /experiences/ | Yes/No | | |
| 15 | `click_request_to_book` | Click a CTA button | Yes/No | | |
| 16 | `click_explore_experiences` | Click explore CTA | Yes/No | | |
| 17 | `click_experience_card` | Click an experience card | Yes/No | | |
| 18 | `start_booking_form` | Click first field in form | Yes/No | | |
| 19 | `submit_booking_form` | Submit the form | Yes/No | | |
| 20 | `submit_email_capture` | Submit email capture | Yes/No | | |
| 21 | `click_phone` | Click phone number link | Yes/No | | |
| 22 | `open_chat` | Click chat widget | Yes/No | | |
| 23 | `view_thank_you_page` | Load /thank-you/ | Yes/No | | |
| 24 | `scroll_50_percent` | Scroll 50% of homepage | Yes/No | | |
| 25 | `scroll_90_percent` | Scroll 90% of homepage | Yes/No | | |

---

## Section C: GA4

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 26 | GA4 DebugView shows page_view event firing on homepage load (GA4 Admin > DebugView) | | | |
| 27 | GA4 DebugView shows `submit_booking_form` event after a test form submission | | | |
| 28 | GA4 DebugView shows `view_thank_you_page` event on /thank-you/ load | | | |
| 29 | `submit_booking_form` is marked as a Conversion in GA4 Admin > Events | | | |
| 30 | `view_thank_you_page` is marked as a Conversion in GA4 Admin > Events | | | |
| 31 | `submit_email_capture` is marked as a Conversion in GA4 Admin > Events | | | |
| 32 | UTM parameters appear in GA4 Realtime or Reports: test with `?utm_source=test&utm_medium=cpc`. Source/Medium report shows "test / cpc" | | | |
| 33 | GA4 funnel exploration is configured with the 4 booking funnel steps | | | |
| 34 | GA4 remarketing audiences (5 audiences) are created in GA4 Admin > Audiences | | | |

---

## Section D: Meta Pixel

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 35 | Meta Pixel Helper Chrome extension shows the Pixel ID on the homepage (no "Not Found" or "Inactive" status) | | | |
| 36 | Meta Pixel Helper shows PageView event firing on homepage load | | | |
| 37 | After submitting the test form, Meta Pixel Helper shows Lead event on /thank-you/ or at form submit | | | |
| 38 | Meta Events Manager > Test Events confirms PageView and Lead events arriving in real time | | | |
| 39 | Custom conversion "She Said Sail Form Submit" is created in Meta Events Manager | | | |
| 40 | Retargeting audiences (Homepage Visitors, Request Page Visitors, Converters Exclusion) are created in Meta Ads Manager | | | |

---

## Section E: TikTok Pixel

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 41 | TikTok Pixel Helper Chrome extension shows the Pixel ID on the homepage | | | |
| 42 | TikTok Pixel Helper shows PageView event on homepage load | | | |
| 43 | After submitting the test form, TikTok Pixel Helper shows SubmitForm event | | | |
| 44 | After loading /thank-you/, TikTok Pixel Helper shows CompleteRegistration event | | | |
| 45 | TikTok Ads Manager > Events > Test Events confirms events arriving | | | |

---

## Section F: Scroll Depth Events

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 46 | `scroll_50_percent` fires exactly once after scrolling halfway down the homepage (not before, not multiple times) | | | |
| 47 | `scroll_90_percent` fires exactly once after scrolling to near the bottom of the homepage | | | |
| 48 | Scroll events fire correctly on /request-to-book/ as well (verify in GTM Preview) | | | |

---

## Sign-Off

All items above must be marked Pass before tracking QA is complete. After sign-off, the GTM container must remain published (not reverted to draft).

Signed: _____________________ Date: _____________________
