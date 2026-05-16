# WEBHOOK REGISTRATION CHECKLIST — Stage 1 Make Import
**Version:** 1.0
**Date:** 2026-05-16
**Purpose:** Track all webhook registrations required for Stage 1 scenarios

---

## Overview

Stage 1 uses two types of webhooks:
1. **Make-generated instant webhooks** — Make creates a unique URL for each scenario with a webhook trigger. These are captured after import.
2. **Stripe-registered webhooks** — Stripe must be configured to POST to Make's webhook URL when payment events occur.

---

## Make Instant Webhooks (Auto-Generated on Import)

After importing each blueprint, Make generates a unique webhook URL. Capture these URLs and fill in the table below.

| Scenario | Make Webhook URL | Captured | Environment |
|----------|-----------------|----------|-------------|
| M-AUDIT-LOGGER | _(paste here after import)_ | [ ] | Sandbox |
| M-AUDIT-LOGGER | _(paste here after import)_ | [ ] | Production |
| M-BRAND-ROUTER | _(paste here after import)_ | [ ] | Sandbox |
| M-BRAND-ROUTER | _(paste here after import)_ | [ ] | Production |
| M-LEAD-INTAKE | _(paste here after import)_ | [ ] | Sandbox |
| M-LEAD-INTAKE | _(paste here after import)_ | [ ] | Production |
| M-SLACK-ALERTS | _(paste here after import)_ | [ ] | Sandbox |
| M-SLACK-ALERTS | _(paste here after import)_ | [ ] | Production |
| M-CONCIERGE-ASSIGNMENT | _(paste here after import)_ | [ ] | Sandbox |
| M-CONCIERGE-ASSIGNMENT | _(paste here after import)_ | [ ] | Production |
| M-STRIPE-DEPOSIT | _(paste here after import)_ | [ ] | Sandbox |
| M-STRIPE-DEPOSIT | _(paste here after import)_ | [ ] | Production |
| M-BOOKING-CREATION | _(paste here after import)_ | [ ] | Sandbox |
| M-BOOKING-CREATION | _(paste here after import)_ | [ ] | Production |
| M-BOOKING-CONFIRMATION | _(paste here after import)_ | [ ] | Sandbox |
| M-BOOKING-CONFIRMATION | _(paste here after import)_ | [ ] | Production |

**Note:** For each scenario you will typically have two versions — one connected to the Sandbox Airtable base (for testing) and one connected to the Production Airtable base (for live use). Import the blueprint twice with different connections.

---

## How to Find the Webhook URL in Make

1. Open the scenario in Make
2. Click on the first module (the webhook trigger module — should be a black hexagon icon)
3. Click **Copy address to clipboard** (or the chain link icon)
4. The URL format will be: `https://hook.us1.make.com/xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
5. Paste it in the table above

---

## Stripe Webhook Registration (REQUIRED for M-BOOKING-CREATION)

M-BOOKING-CREATION is triggered by Stripe's `payment_intent.succeeded` event. You must register the Make webhook URL with Stripe.

### Sandbox Registration (Stripe Test Mode)

1. Go to [Stripe Dashboard](https://dashboard.stripe.com) → Test mode (toggle ON)
2. Navigate to **Developers** → **Webhooks** → **Add endpoint**
3. **Endpoint URL:** Paste the Sandbox M-BOOKING-CREATION webhook URL from Make
4. **Events to listen to:** Select `payment_intent.succeeded`
5. Click **Add endpoint**
6. Click **Reveal signing secret** → Copy the `whsec_...` value
7. Add this signing secret to the Stripe connection in your Make sandbox scenario

| Item | Value | Done |
|------|-------|------|
| Stripe Webhook Endpoint URL (Test) | _(paste)_ | [ ] |
| Stripe Webhook Signing Secret (Test) | _(stored in Make — do not write here)_ | [ ] |
| Stripe Webhook ID (Test) | _(paste from Stripe Dashboard)_ | [ ] |

### Production Registration (Stripe Live Mode)

**Do NOT complete this until sandbox validation passes.**

1. Go to Stripe Dashboard → **LIVE mode** (toggle OFF test mode)
2. Navigate to **Developers** → **Webhooks** → **Add endpoint**
3. **Endpoint URL:** Paste the Production M-BOOKING-CREATION webhook URL from Make
4. **Events to listen to:** Select `payment_intent.succeeded`
5. Click **Add endpoint**
6. Copy signing secret → add to Make production scenario Stripe connection

| Item | Value | Done |
|------|-------|------|
| Stripe Webhook Endpoint URL (Live) | _(paste)_ | [ ] |
| Stripe Webhook Signing Secret (Live) | _(stored in Make — do not write here)_ | [ ] |
| Stripe Webhook ID (Live) | _(paste from Stripe Dashboard)_ | [ ] |

---

## Inter-Scenario Webhook URL Propagation

After collecting all webhook URLs, update these HTTP modules:

| Source Scenario | HTTP Module Target | Target URL to Insert |
|-----------------|------------------|---------------------|
| M-BRAND-ROUTER | calls M-LEAD-INTAKE | M-LEAD-INTAKE webhook URL |
| M-BRAND-ROUTER | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-LEAD-INTAKE | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-LEAD-INTAKE | calls M-SLACK-ALERTS | M-SLACK-ALERTS webhook URL |
| M-SLACK-ALERTS | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-CONCIERGE-ASSIGNMENT | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-CONCIERGE-ASSIGNMENT | calls M-SLACK-ALERTS | M-SLACK-ALERTS webhook URL |
| M-STRIPE-DEPOSIT | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-STRIPE-DEPOSIT | calls M-SLACK-ALERTS | M-SLACK-ALERTS webhook URL |
| M-BOOKING-CREATION | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-BOOKING-CREATION | calls M-SLACK-ALERTS | M-SLACK-ALERTS webhook URL |
| M-BOOKING-CREATION | calls M-BOOKING-CONFIRMATION | M-BOOKING-CONFIRMATION webhook URL |
| M-BOOKING-CONFIRMATION | calls M-AUDIT-LOGGER | M-AUDIT-LOGGER webhook URL |
| M-BOOKING-CONFIRMATION | calls M-SLACK-ALERTS | M-SLACK-ALERTS webhook URL |

---

## Webflow Integration (Optional — for live form intake)

If Webflow forms are the primary lead source for M-LEAD-INTAKE or M-BRAND-ROUTER:

1. Go to Webflow → Project Settings → Integrations → Webhooks
2. Add a form submission webhook pointing to M-BRAND-ROUTER webhook URL
3. Map Webflow form fields to the expected JSON payload structure (see M-BRAND-ROUTER.test.json for field names)

| Item | Value | Done |
|------|-------|------|
| Webflow Webhook (SSS form) | _(paste M-BRAND-ROUTER URL)_ | [ ] |
| Webflow Webhook (ME form) | _(paste M-BRAND-ROUTER URL)_ | [ ] |

---

## Final Webhook Validation

- [ ] All 8 scenarios have active webhook triggers (not disconnected)
- [ ] All inter-scenario HTTP module URLs are populated with real webhook URLs
- [ ] Stripe sandbox webhook registered and tested (test event received in Make)
- [ ] All webhook URLs stored securely (do NOT store in public documents)
- [ ] Sandbox webhook URLs are NOT registered in Stripe Live mode
