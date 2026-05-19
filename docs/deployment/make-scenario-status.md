# She Said Sail: Make.com Scenario Status

**Date:** 2026-05-19
**Status:** 8 of 10 core scenarios completed manually by Will. M-CHATBOT-001 is the only remaining Phase 2 build. Intelligence layer (4 scenarios) is post-launch.

---

## Phase 1: Core Scenarios (8 of 8 COMPLETE)

| Scenario ID | Purpose | Status | Webhook Dependency | Airtable Dependency | Blueprint Needed |
|---|---|---|---|---|---|
| M-WEBFORM-REQUEST-CAPTURE | Receives Request to Book form payload. Creates Request, Contact, UTM records. Triggers confirmation email and Slack alert. | COMPLETE | WIRE_THIS_REQUEST_FORM_WEBHOOK_URL in she-said-sail-global.js | Requests, Contacts, UTMs, Audit Log tables | No |
| M-UTM-CAPTURE | Creates UTMs record linked to a Request. Recommended as inline step within M-WEBFORM-REQUEST-CAPTURE for v1. | COMPLETE (inline) | None (inline) | UTMs table | No |
| M-EMAIL-CAPTURE | Receives homepage email capture payload. Creates or updates Contact with Email Subscribed = true. | COMPLETE | Commented-out fetch() block in she-said-sail-global.js | Contacts, Audit Log tables | No |
| M-INQUIRY-CONFIRMATION-EMAIL | Sends confirmation email to the person who submitted the Request to Book form. | COMPLETE | Called from M-WEBFORM-REQUEST-CAPTURE | None | No |
| M-SLACK-NEW-LEAD-ALERT | Posts real-time alert to #new-leads Slack channel on new inquiry. | COMPLETE | Called from M-WEBFORM-REQUEST-CAPTURE | None (reads from payload) | No |
| M-AIRTABLE-AUDIT-LOGGER | Centralized logging to Audit Log table. Called from any scenario via webhook. | COMPLETE | Standalone webhook | Audit Log table | No |
| M-BRAND-ROUTER | Routes submissions to the correct brand handler. Pass-through in v1 (She Said Sail is the only brand). | COMPLETE | Called from M-WEBFORM-REQUEST-CAPTURE | None | No |
| M-CONCIERGE-ASSIGNMENT | Watches for new Requests (Status = New, Assigned Concierge empty) and assigns a concierge. | COMPLETE | Airtable Watch Records trigger | Requests table | No |

---

## Phase 2: Chatbot Scenario (0 of 1 COMPLETE)

| Scenario ID | Purpose | Status | Webhook Dependency | Airtable Dependency | Blueprint Needed |
|---|---|---|---|---|---|
| M-CHATBOT-001 | Receives chatbot handoff payload. Creates Request, Contact, UTM, and Chatbot Conversations records. Sends Slack alert. | NOT BUILT | WIRE_THIS_CHATBOT_WEBHOOK_URL in chatbot/chatbot-js.js | Requests, Contacts, UTMs, Chatbot Conversations, Audit Log tables | YES -- see 06_MAKE_BLUEPRINTS/M-CHATBOT-001-blueprint.json |

**Action required:** Build M-CHATBOT-001 before go-live. The chatbot fires a webhook on every completed conversation. Without this scenario, chatbot leads are lost.

---

## Phase 3: Intelligence Layer (0 of 4 COMPLETE -- build post-launch)

These scenarios require real booking data to be useful. Build after the site has been live for at least 2 to 4 weeks and the core system is stable.

| Scenario ID | Purpose | Status | Trigger | Complexity |
|---|---|---|---|---|
| M-BOOKING-OUTCOME-001 | Watches for Request Status = Booked. Creates Revenue Attribution record linking Booking to UTM and Campaign. Posts to #intelligence Slack. | NOT BUILT | Airtable Watch Records (Requests, Status = Booked) | Medium |
| M-WEEKLY-REPORT-001 | Scheduled Monday 8:00 AM. Queries last 7 days of data. Posts intelligence summary to #intelligence Slack. Creates Weekly Insights record. | NOT BUILT | Scheduled (Monday 8:00 AM) | Medium |
| M-EXPERIENCE-ROLLUP-001 | Scheduled Monday 8:30 AM. Aggregates booking and request counts by experience. Creates/updates Experience Performance records. | NOT BUILT | Scheduled (Monday 8:30 AM) | Low |
| M-CONCIERGE-SCORE-001 | Watches for Booking Status = Deposit Received or Paid in Full. Calculates response time and booking rate. Logs to Audit Log. | NOT BUILT | Airtable Watch Records (Bookings, Status change) | Medium |

---

## Webhook URL Wiring Status

All three webhook URL placeholders must be replaced with real Make.com webhook URLs before go-live.

| Placeholder | File | Scenario to Create First | Status |
|---|---|---|---|
| WIRE_THIS_REQUEST_FORM_WEBHOOK_URL | 02_GLOBAL_JS/she-said-sail-global.js | M-WEBFORM-REQUEST-CAPTURE | Complete (Will built scenario; URL needs wiring into JS) |
| Commented-out fetch() block | 02_GLOBAL_JS/she-said-sail-global.js | M-EMAIL-CAPTURE | Complete (Will built scenario; URL needs uncommenting and wiring) |
| WIRE_THIS_CHATBOT_WEBHOOK_URL | chatbot/chatbot-js.js | M-CHATBOT-001 | Blocked (scenario not yet built) |
| WIRE_THIS_CONTACT_WEBHOOK_URL | pages/contact/contact-html-snippets.html | M-CONTACT-001 (create if needed) | Needs contact form scenario |

---

## Summary

- Scenarios to build before launch: **1** (M-CHATBOT-001)
- Scenarios to wire with real URLs: **3 webhook placeholders** in JS files
- Scenarios to build post-launch: **4** (intelligence layer)
- Scenarios complete: **8**
