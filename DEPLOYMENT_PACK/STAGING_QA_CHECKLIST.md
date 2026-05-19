# Staging QA Checklist

**Version:** 1.0
**Purpose:** Fast pass/fail verification before approving any page or system for production.
**Instructions:** Mark each item PASS or FAIL. All items must be PASS before go-live.

---

## Section 1: Global (test on every page)

| # | Check | Result |
|---|---|---|
| 1.1 | Global CSS loads with no errors (DevTools console shows no CSS 404s) | |
| 1.2 | Global JS loads with no errors (DevTools console shows no JS errors on page load) | |
| 1.3 | GTM container fires on page load (GTM Preview shows container active) | |
| 1.4 | GA4 Configuration tag fires on every page (GTM Preview > Tags > GA4 Config shows Fired) | |
| 1.5 | Brand fonts load correctly (Cormorant Garamond for headings, Inter for body) | |
| 1.6 | Site loads over HTTPS with valid SSL certificate | |
| 1.7 | No broken images (no 404 image requests in DevTools Network tab) | |
| 1.8 | Footer phone number is a tappable tel: link on mobile | |

---

## Section 2: Homepage

| # | Check | Result |
|---|---|---|
| 2.1 | Page renders with no layout breaks on desktop (1440px) | |
| 2.2 | Page renders with no layout breaks on mobile (375px) | |
| 2.3 | Occasion pills appear in hero section (bachelorette, birthday, etc.) | |
| 2.4 | Social proof strip appears below experience cards | |
| 2.5 | Email capture section appears above bottom navy CTA | |
| 2.6 | Email capture form submits and shows success message | |
| 2.7 | "Request to Book" CTA buttons link to /request-to-book/ | |
| 2.8 | "Explore Experiences" CTA links to /experiences/ | |
| 2.9 | GTM event `view_homepage` fires on page load | |
| 2.10 | GTM event `click_request_to_book` fires on CTA click | |

---

## Section 3: Request to Book Page

| # | Check | Result |
|---|---|---|
| 3.1 | Concierge reassurance block appears above the form | |
| 3.2 | Form intro text appears between reassurance block and form | |
| 3.3 | Trust note appears below submit button | |
| 3.4 | All required form fields are present (name, email, phone, occasion, experience, date, group size, notes) | |
| 3.5 | Hidden fields are present in the form DOM (utm_source, utm_medium, utm_campaign, utm_content, utm_term, visitor_id, referrer_url, landing_page, source_type, brand) | |
| 3.6 | Submitting the form redirects to /thank-you/ (or shows confirmation message) | |
| 3.7 | After form submit: Airtable Requests table has a new record within 60 seconds | |
| 3.8 | After form submit: Airtable Contacts table has a new or updated record | |
| 3.9 | After form submit: confirmation email arrives at the test address within 5 minutes | |
| 3.10 | After form submit: Slack #new-leads shows the alert | |
| 3.11 | GTM event `start_booking_form` fires on first field focus | |
| 3.12 | GTM event `submit_booking_form` fires on successful submit | |
| 3.13 | UTM values are captured in hidden fields (test by adding ?utm_source=test to URL before loading the page) | |

---

## Section 4: Experiences Page

| # | Check | Result |
|---|---|---|
| 4.1 | Hero support copy appears below page hero | |
| 4.2 | All 4 experience cards show correct descriptions | |
| 4.3 | Social proof strip appears below cards | |
| 4.4 | Bottom CTA appears at page bottom and links to /request-to-book/ | |
| 4.5 | Each experience card links to the correct experience page URL | |
| 4.6 | GTM event `view_experiences_page` fires on page load | |
| 4.7 | GTM event `click_experience_card` fires when clicking an experience card | |

---

## Section 5: Monaco Social Experience Page

| # | Check | Result |
|---|---|---|
| 5.1 | Page renders correctly on desktop and mobile | |
| 5.2 | Hero support section (occasions row) appears below hero | |
| 5.3 | Social proof quotes section appears | |
| 5.4 | "Request to Book" CTA links to /request-to-book/ | |
| 5.5 | GTM event `view_experience_page` fires with `experience_name: Monaco Social` | |

---

## Section 6: Chatbot

| # | Check | Result |
|---|---|---|
| 6.1 | Chat widget button is visible in the bottom-right corner on all pages | |
| 6.2 | Clicking the button opens the chat panel | |
| 6.3 | Chatbot responds to occasion selection (bachelorette, birthday, etc.) | |
| 6.4 | Chatbot asks energy, group size, recommends an experience | |
| 6.5 | Chatbot collects date, name, email, phone (phone can be skipped) | |
| 6.6 | After completing conversation: webhook fires to Make.com M-CHATBOT-001 | |
| 6.7 | After conversation: Airtable Requests table has a new chatbot-sourced record | |
| 6.8 | After conversation: Airtable Chatbot Conversations table has a record | |
| 6.9 | After conversation: Slack #new-leads shows chatbot alert | |
| 6.10 | GTM event `chatbot_open` fires when widget is opened | |
| 6.11 | GTM event `chatbot_start_conversation` fires | |
| 6.12 | GTM event `chatbot_handoff` fires at conversation completion | |
| 6.13 | Tidio is not installed and active on the same site | |

---

## Section 7: Mobile

| # | Check | Result |
|---|---|---|
| 7.1 | Homepage: all sections stack correctly on 375px width | |
| 7.2 | Request to Book: form is usable on mobile, no fields cut off | |
| 7.3 | Experiences: cards stack to single column | |
| 7.4 | Monaco Social and experience pages: two-column sections stack to single column | |
| 7.5 | Navigation works on mobile (burger menu opens and closes) | |
| 7.6 | Chatbot panel is usable on mobile, input field not obscured by keyboard | |
| 7.7 | All buttons are at least 44px height (minimum tap target) | |
| 7.8 | No horizontal overflow (no side-scrolling on any page) | |

---

## Section 8: GTM and Analytics

| # | Check | Result |
|---|---|---|
| 8.1 | GTM container GTM-TZ5KNRTH is published (not just saved) | |
| 8.2 | GA4 Measurement ID is GT-WV3X86GZ (verify in GTM > Tags > GA4 Config) | |
| 8.3 | GA4 DebugView shows active session during testing | |
| 8.4 | Meta Pixel ID is replaced (not `YOUR_META_PIXEL_ID`) | |
| 8.5 | TikTok Pixel ID is replaced (not `YOUR_TIKTOK_PIXEL_ID`) | |
| 8.6 | No duplicate GA4 Configuration tags firing | |
| 8.7 | GTM dataLayer does not expose PII (no email or phone in dataLayer pushes) | |

---

## Section 9: Airtable and Make.com

| # | Check | Result |
|---|---|---|
| 9.1 | Airtable base exists with all 7 core tables | |
| 9.2 | All Make.com Phase 1 scenarios are active (toggled ON) | |
| 9.3 | M-CHATBOT-001 is built and active | |
| 9.4 | All webhook URL placeholders are replaced with real URLs | |
| 9.5 | Test form submission creates linked records in Requests + Contacts + UTMs | |
| 9.6 | Test chatbot creates linked records in Requests + Contacts + UTMs + Chatbot Conversations | |
| 9.7 | M-CONCIERGE-ASSIGNMENT triggers within 2 minutes of new Request (Status = New, no assigned concierge) | |

---

## Section 10: Thank You Page and Confirmation Flow

| # | Check | Result |
|---|---|---|
| 10.1 | /thank-you/ page loads after form submission | |
| 10.2 | Thank You page content matches the file in `pages/thank-you/` | |
| 10.3 | GTM event `view_thank_you_page` fires on Thank You page load | |
| 10.4 | No "go back" loop: navigating back from Thank You does not re-submit the form | |

---

## Go / No-Go Decision

| Condition | Status |
|---|---|
| All Section 1 (Global) items: PASS | |
| All Section 3 (Request Form) items: PASS | |
| All Section 6 (Chatbot) items: PASS | |
| All Section 8 (GTM) items: PASS | |
| All Section 9 (Airtable + Make) items: PASS | |
| No open FAIL items in any section | |

**Go-live authorized when:** all 6 conditions above are met and Will has given written approval.

Any FAIL items must be resolved and re-verified before authorization. Do not skip re-verification.

---

## Notes

Use this section to log any failures, their root causes, and when they were resolved.

| Item | Failure Description | Resolved Date | Resolved By |
|---|---|---|---|
| | | | |
| | | | |
| | | | |
