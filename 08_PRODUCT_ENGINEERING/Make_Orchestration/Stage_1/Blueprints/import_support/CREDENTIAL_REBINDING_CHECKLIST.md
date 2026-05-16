# CREDENTIAL REBINDING CHECKLIST — Stage 1 Make Import
**Version:** 1.0
**Date:** 2026-05-16
**Purpose:** Track credential reconnection for all 8 Stage 1 scenarios after blueprint import

---

## Overview

Make.com blueprints do NOT export or import credentials. Every connection (Airtable, Slack, Gmail, Stripe, SMS) must be manually reconnected after each blueprint is imported. This checklist ensures no module is left disconnected.

---

## Connections to Establish in Make (Pre-Import)

Create these connections in Make BEFORE importing blueprints:

| Connection Name | Service | Auth Method | Account |
|----------------|---------|-------------|---------|
| SSS Airtable Production | Airtable | Personal Access Token | appdZ49WqgjRXxA1R |
| SSS Airtable Sandbox | Airtable | Personal Access Token | Sandbox base ID |
| SSS Slack | Slack | OAuth 2.0 | SSS/ME shared workspace |
| SSS Gmail | Gmail | OAuth 2.0 | hello@shesaidsail.com |
| ME Gmail | Gmail | OAuth 2.0 | hello@mareexecutive.com |
| SSS Stripe Live | Stripe | API Key | Live mode |
| SSS Stripe Test | Stripe | API Key | Test mode |
| SSS Quo SMS | HTTP (custom) | API Key header | Quo SMS account |

---

## Per-Scenario Rebinding Checklist

### M-AUDIT-LOGGER

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Search Audit Log (idempotency) | SSS Airtable Production | [ ] |
| Airtable — Create Audit Log Record | SSS Airtable Production | [ ] |
| Airtable — Search Automation_Health | SSS Airtable Production | [ ] |
| Airtable — Update Automation_Health | SSS Airtable Production | [ ] |
| Slack — Error Alert | SSS Slack | [ ] |

Additional manual steps:
- [ ] Replace `AUTOMATION_HEALTH_TABLE_ID` with actual Airtable table ID for Automation_Health
- [ ] Verify webhook URL is generated and recorded

---

### M-BRAND-ROUTER

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Slack — Error Alert | SSS Slack | [ ] |

HTTP modules (no Make connection required — use plain HTTP):
- [ ] Update HTTP module target URL for M-LEAD-INTAKE: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

### M-LEAD-INTAKE

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Search Requests (duplicate check) | SSS Airtable Production | [ ] |
| Airtable — Create Request Record | SSS Airtable Production | [ ] |
| Airtable — Update Existing Request | SSS Airtable Production | [ ] |

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-SLACK-ALERTS: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

### M-SLACK-ALERTS

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Slack — #sss-leads message | SSS Slack | [ ] |
| Slack — #me-leads message | SSS Slack | [ ] |
| Slack — #sss-bookings message | SSS Slack | [ ] |
| Slack — #sss-ops-alerts message | SSS Slack | [ ] |
| Slack — #sss-emergency-ops message | SSS Slack | [ ] |
| Slack — DM to Will (emergency) | SSS Slack | [ ] |

Additional:
- [ ] Replace `WILL_SLACK_USER_ID_PLACEHOLDER` with Will's actual Slack Member ID
- [ ] Confirm all channel names match live Slack workspace

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

### M-CONCIERGE-ASSIGNMENT

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Get Request Record | SSS Airtable Production | [ ] |
| Airtable — Search Concierge_Operators | SSS Airtable Production | [ ] |
| Airtable — Update Request (assign) | SSS Airtable Production | [ ] |
| Airtable — Update Request (no concierge) | SSS Airtable Production | [ ] |
| Gmail — Concierge notification email | SSS Gmail | [ ] |

Additional:
- [ ] Replace `CONCIERGE_OPERATORS_TABLE_ID` with actual Airtable table ID
- [ ] Confirm Gmail "From" address is hello@shesaidsail.com

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-SLACK-ALERTS: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

### M-STRIPE-DEPOSIT

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Get Booking Record | SSS Airtable Production | [ ] |
| Airtable — Search Packages | SSS Airtable Production | [ ] |
| Airtable — Update Booking (deposit link) | SSS Airtable Production | [ ] |
| Stripe — Create Payment Link | SSS Stripe Live (or Test for sandbox) | [ ] |
| Gmail — Deposit request email to client | SSS Gmail | [ ] |
| HTTP — Quo SMS deposit link SMS | SSS Quo SMS | [ ] |

Additional:
- [ ] Verify Stripe Payment Link success URL: https://shesaidsail.com/booking-confirmed
- [ ] Verify Stripe metadata includes: booking_id, brand, environment, type="deposit"
- [ ] Confirm SMS API endpoint and authentication header format

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-SLACK-ALERTS: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

### M-BOOKING-CREATION

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Search Bookings (idempotency) | SSS Airtable Production | [ ] |
| Airtable — Search Requests | SSS Airtable Production | [ ] |
| Airtable — Search/Get Clients | SSS Airtable Production | [ ] |
| Airtable — Create Booking Record | SSS Airtable Production | [ ] |
| Airtable — Update Booking Record | SSS Airtable Production | [ ] |
| Airtable — Update Request Record | SSS Airtable Production | [ ] |

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-SLACK-ALERTS: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-BOOKING-CONFIRMATION: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

Stripe:
- [ ] Register Stripe webhook pointing to this scenario's webhook URL (event: payment_intent.succeeded)
- [ ] Add Stripe Webhook Signing Secret to scenario configuration

---

### M-BOOKING-CONFIRMATION

| Module | Connection Required | Connected? |
|--------|-------------------|------------|
| Airtable — Get Booking Record | SSS Airtable Production | [ ] |
| Airtable — Update Booking (confirmation sent) | SSS Airtable Production | [ ] |
| Gmail — SSS confirmation email | SSS Gmail | [ ] |
| Gmail — ME confirmation email | ME Gmail | [ ] |
| HTTP — Quo SMS confirmation SMS (SSS) | SSS Quo SMS | [ ] |
| HTTP — Quo SMS confirmation SMS (ME) | SSS Quo SMS | [ ] |

HTTP modules:
- [ ] Update HTTP module target URL for M-AUDIT-LOGGER: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`
- [ ] Update HTTP module target URL for M-SLACK-ALERTS: replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT`

---

## Final Validation Before Activation

- [ ] All 8 scenarios have zero disconnected modules (Make shows green checkmarks on all connections)
- [ ] All `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` placeholders replaced with real URLs
- [ ] All `AUTOMATION_HEALTH_TABLE_ID` and `CONCIERGE_OPERATORS_TABLE_ID` replaced
- [ ] `WILL_SLACK_USER_ID_PLACEHOLDER` replaced
- [ ] Stripe webhook registered and signing secret configured
- [ ] Sandbox test run complete (see SANDBOX_TEST_SEQUENCE.md)
- [ ] Will has reviewed and approved production activation
