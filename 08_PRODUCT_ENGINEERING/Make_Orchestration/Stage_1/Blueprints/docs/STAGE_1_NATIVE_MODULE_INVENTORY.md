# Stage 1 Native Make Module Inventory
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION REFERENCE

---

## Purpose

This document inventories all native Make.com app modules verified for use in Stage 1 blueprints, documents replacement decisions, and records every HTTP module that remains with its justification.

---

## 1. Airtable

**Native Make App:** `airtable` (Make Airtable app — fully supported)

| Module Name | Make Module ID | Stage 1 Use | Decision |
|---|---|---|---|
| Watch Records (trigger) | `airtable:TriggerNewRecord` | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION triggers | **USE NATIVE** |
| Search Records | `airtable:ActionSearchRecords` | Idempotency checks, find booking by Stripe ID | **USE NATIVE** |
| Get a Record | `airtable:ActionGetRecord` | Fetch full booking before Charter Brief generation | **USE NATIVE** |
| Create a Record | `airtable:ActionCreateRecord` | Audit Log writes, Requests table creation | **USE NATIVE** |
| Update a Record | `airtable:ActionUpdateRecord` | Status updates, Booking field updates | **USE NATIVE** |
| Make an API Call | `airtable:MakeApiCall` | Not required for Stage 1 | Not used |

**Replace HTTP Airtable calls:** YES — all HTTP `POST/PATCH/GET` calls to `api.airtable.com` are replaced with native modules.

**Connection placeholder:** `RECONNECT_AIRTABLE_CONNECTION`

**Base ID:** `appdZ49WqgjRXxA1R` (She Said Sail Production)

**Manual setup required:**
1. After import, click each Airtable module → "Add a connection"
2. Use Airtable API key or OAuth connection
3. Verify base ID `appdZ49WqgjRXxA1R` is accessible under the connected account
4. Test with a search on Bookings table `tbl72omPibBkn2hZL`

---

## 2. Slack

**Native Make App:** `slack` (Make Slack app — fully supported)

| Module Name | Make Module ID | Stage 1 Use | Decision |
|---|---|---|---|
| Create a Message | `slack:CreateMessage` | All alert/notification sends | **USE NATIVE** |
| Send Direct Message | `slack:CreateMessage` (DM channel ID) | Will DM for L3/L4 alerts | **USE NATIVE** |
| Watch Messages | `slack:TriggerMessages` | Not needed Stage 1 | Not used |
| Search Messages | `slack:SearchMessages` | Not needed Stage 1 | Not used |
| Upload a File | `slack:UploadFile` | Not needed Stage 1 | Not used |

**Replace HTTP Slack webhook calls:** YES — all incoming webhook HTTP calls replaced with native `slack:CreateMessage`.

**Connection placeholder:** `RECONNECT_SLACK_CONNECTION`

**Additional placeholder:** `RECONNECT_WILL_SLACK_USER_ID` — must be set to Will's Slack User ID (format: U0XXXXXXXXX) for L3/L4 DM routes in M-SLACK-ALERTS.

**Channels used:**
- `#sss-ops-alerts` — L1/L2 operational alerts, Luciana-facing
- `#sss-emergency-ops` — L4 emergencies only
- Will's User ID (DM) — L3/L4 direct escalation

**Manual setup required:**
1. After import, click each Slack module → "Add a connection" → authorize She Said Sail Slack workspace
2. In M-SLACK-ALERTS modules 5 and 7: replace `RECONNECT_WILL_SLACK_USER_ID` with Will's actual Slack User ID
3. To find User ID: Slack → Will's profile → "Copy member ID"

---

## 3. Anthropic Claude

**Native Make App:** `anthropic` (Make Anthropic app — confirmed supported)

| Module Name | Make Module ID | Stage 1 Use | Decision |
|---|---|---|---|
| Create a Message | `anthropic:ActionCreateMessage` | Brand classification, Charter Brief generation | **USE NATIVE** |

**Native module capability verification:**
- ✅ Supports `model` field → `claude-sonnet-4-20250514`
- ✅ Supports `max_tokens` → set to `600`
- ✅ Supports `temperature` → set to `0.4`
- ✅ Supports `system` prompt field
- ✅ Supports `messages` array with `role` (user/assistant) and `content`
- ✅ Returns `content[].text` for response extraction

**Decision:** REPLACE HTTP — all HTTP POST calls to `https://api.anthropic.com/v1/messages` are replaced with native `anthropic:ActionCreateMessage`.

**Connection placeholder:** `RECONNECT_CLAUDE_API_KEY`

**Blueprints using Anthropic native:**
- `M-BRAND-ROUTER` — module 3: brand classification
- `M-BOOKING-CREATION` — module 7: Charter Brief generation

**Manual setup required:**
1. After import, click each Anthropic module → "Add a connection"
2. Enter Anthropic API key from credential vault
3. Connection name: "She Said Sail — Anthropic Claude Production"
4. Test with a simple prompt before activating scenario

---

## 4. Gmail / Google Workspace

**Native Make App:** `gmail` (Make Gmail app — fully supported)

| Module Name | Make Module ID | Stage 1 Use | Decision |
|---|---|---|---|
| Send an Email | `gmail:ActionSendEmail` | All outbound client emails | **USE NATIVE** |
| Create a Draft | `gmail:ActionCreateDraft` | Not needed Stage 1 (Tier B drafts are manual) | Not used |
| Watch Emails | `gmail:TriggerNewEmail` | Not needed Stage 1 | Not used |
| Search Emails | `gmail:ActionSearchEmails` | Not needed Stage 1 | Not used |

**Replace HTTP Gmail API calls:** YES — all HTTP calls to Gmail API replaced with native `gmail:ActionSendEmail`.

**Connection placeholder:** `RECONNECT_GMAIL_CONNECTION`

**From address:** `hello@shesaidsail.com`

**Blueprints using Gmail native:**
- `M-LEAD-INTAKE` — module 7: auto-reply to new leads
- `M-CONCIERGE-ASSIGNMENT` — module 8: deposit request email
- `M-STRIPE-DEPOSIT` — module 8: deposit confirmation email
- `M-BOOKING-CREATION` — module 8: Charter Brief email to City Manager
- `M-BOOKING-CONFIRMATION` — module 8: balance due reminder

**Manual setup required:**
1. After import, click each Gmail module → "Add a connection"
2. Authorize Google account associated with `hello@shesaidsail.com`
3. Verify "From" address is set to `hello@shesaidsail.com` in each module
4. Send a test email to an internal address before activating scenarios
5. **IMPORTANT:** Never activate scenarios that send client emails in sandbox/testing mode without disabling the Gmail send first

---

## 5. Stripe

**Native Make App:** `stripe` (Make Stripe app — fully supported)

| Module Name | Make Module ID | Stage 1 Use | Decision |
|---|---|---|---|
| Watch Events | `stripe:TriggerEvent` | NOT used — webhook preferred for deposit (see note) | KEPT AS WEBHOOK |
| Create Payment Link | `stripe:ActionCreatePaymentLink` | Deposit and balance payment links | **USE NATIVE** |
| Retrieve Payment Intent | `stripe:ActionRetrievePaymentIntent` | Available if needed | Not required |
| Retrieve Checkout Session | `stripe:ActionRetrieveCheckoutSession` | Available if needed | Not required |
| Create Customer | `stripe:ActionCreateCustomer` | Stage 2 | Not Stage 1 |
| Make an API Call | `stripe:MakeApiCall` | Not needed | Not used |

**Decision on Stripe Watch Events vs Webhook:**
The native `stripe:TriggerEvent` polling module is NOT used for M-STRIPE-DEPOSIT. Reasoning:
- Stripe sends webhooks instantly on payment completion
- Polling introduces latency — unacceptable for financial confirmation flow
- Webhook preserves the full Stripe event payload including signature for validation
- Stripe's official integration guidance recommends webhooks for payment events
- **KEEP:** `gateway:CustomWebHook` for M-STRIPE-DEPOSIT trigger
- **USE NATIVE:** `stripe:ActionCreatePaymentLink` for payment link creation in M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION

**Connection placeholder:** `RECONNECT_STRIPE_CONNECTION`

**Stripe webhook setup (M-STRIPE-DEPOSIT):**
1. After import, copy the M-STRIPE-DEPOSIT webhook URL from Make
2. Go to Stripe Dashboard → Developers → Webhooks → Add endpoint
3. Paste the Make webhook URL
4. Subscribe to event: `payment_intent.succeeded`
5. Copy the Signing Secret and store in Make Data Store (do NOT put in blueprint)
6. Add Stripe-Signature validation to the webhook module in Make settings

---

## 6. SMS / Phone Provider — Quo

**Native Make App:** ❌ **QUO HAS NO NATIVE MAKE MODULE**

| Provider | Native Make Module | Decision |
|---|---|---|
| Quo | ❌ None | HTTP module required |
| Twilio | ✅ `twilio:ActionSendSms` | Available if provider switch approved |
| OpenPhone | ✅ `openphone:ActionSendMessage` | Available if provider switch approved |
| SMS by Make | ✅ Built-in | Limited carrier coverage — not recommended for production |

**Current state:** Quo uses HTTP module with API key. This is documented and accepted.

**Quo HTTP module pattern (all blueprints using SMS):**
```
Module: http:ActionSendData
URL: RECONNECT_QUO_API_ENDPOINT (from credential vault)
Method: POST
Headers: Authorization: Bearer RECONNECT_QUO_API_KEY
Body: JSON payload with to, message fields
```

**Recommendation for Stage 2:**
If Quo proves difficult to maintain or lacks reliable Make compatibility, evaluate switching to Twilio (native Make module, full production support) or OpenPhone. This requires a Founder Decision before provider switch.

**Blueprints using Quo HTTP:**
- `M-CONCIERGE-ASSIGNMENT` — module 9: deposit request SMS
- `M-BOOKING-CONFIRMATION` — module 9: balance due SMS

**Manual setup required:**
1. After import, open each HTTP Quo module
2. Replace `RECONNECT_QUO_API_ENDPOINT` with Quo API endpoint from credential vault
3. Replace `RECONNECT_QUO_API_KEY` with Quo API key from credential vault
4. **NEVER** hardcode credentials directly in the module — use Make's built-in Variables or Data Store
5. Test SMS send to an internal number before activating client-facing scenarios

---

## 7. Google Drive

**Native Make App:** `googledrive` (Make Google Drive app — fully supported)

| Module Name | Decision |
|---|---|
| Watch Files | Not needed Stage 1 |
| Upload a File | Not needed Stage 1 |
| Search Files | Not needed Stage 1 |
| Create Folder | Not needed Stage 1 |

**Stage 1 verdict:** Google Drive not used in any Stage 1 scenario. Available for Stage 2+ (document storage for Charter Briefs, agreements).

---

## 8. Squarespace / Website Forms

**Native Make App:** ❌ **No reliable native Squarespace Make module for form submissions**

Make has limited Squarespace modules focused on commerce/inventory, not form submission intake. No native Squarespace form → Make trigger exists that is production-reliable.

**Decision:** KEEP webhook trigger for M-LEAD-INTAKE.

**Squarespace form setup:**
1. In Squarespace site editor → Form Block → Storage → Add → Webhook
2. Paste the M-LEAD-INTAKE webhook URL from Make
3. Map form fields to expected webhook payload format
4. Test with a form submission before activating

**Note:** If Squarespace is replaced with Webflow or Typeform in future stages, both have native Make modules and form submission support.

---

## 9. Make Built-in Tools (Native Utilities)

All built-in modules used in Stage 1 blueprints:

| Module | Make ID | Use | Blueprints |
|---|---|---|---|
| Router | `builtin:BasicRouter` | All branching logic (guard checks, brand routing, idempotency) | All 8 |
| Set Variable | `tools:SetVariable` | Idempotency key generation | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, M-STRIPE-DEPOSIT, M-LEAD-INTAKE |
| Parse JSON | `json:ParseJSON` | Parse Anthropic Claude response | M-BRAND-ROUTER |
| HTTP Send Data | `http:ActionSendData` | Quo SMS, inter-scenario webhooks, Audit Logger calls | Multiple |
| Custom Webhook | `gateway:CustomWebHook` | Inbound triggers (Squarespace, Stripe, inter-scenario) | M-AUDIT-LOGGER, M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-STRIPE-DEPOSIT |

---

## Module Count Summary

| Scenario | Native Modules | HTTP Modules | Webhook Triggers | Net-New Native |
|---|---|---|---|---|
| M-AUDIT-LOGGER | 1 (Airtable Create) | 0 | 1 | 1 |
| M-BRAND-ROUTER | 5 (Anthropic, Airtable ×3, Slack) | 1 (Audit Logger) | 1 | 5 |
| M-LEAD-INTAKE | 4 (Airtable ×2, Gmail, Slack) | 2 (Brand Router, Audit Logger) | 1 (Squarespace) | 4 |
| M-SLACK-ALERTS | 4 (Slack ×4) | 1 (Audit Logger) | 1 | 4 |
| M-CONCIERGE-ASSIGNMENT | 5 (Airtable ×3, Stripe, Gmail) | 3 (Quo, Audit ×2) | 0 (Airtable trigger) | 5 |
| M-STRIPE-DEPOSIT | 5 (Airtable ×3, Gmail, Slack) | 1 (Audit Logger) | 1 (Stripe) | 5 |
| M-BOOKING-CREATION | 6 (Airtable ×4, Anthropic, Gmail, Slack) | 2 (Audit ×2) | 0 (Airtable trigger) | 6 |
| M-BOOKING-CONFIRMATION | 5 (Airtable ×3, Stripe, Gmail, Slack) | 3 (Quo, Audit ×2) | 0 (Airtable trigger) | 5 |

**Total native modules:** 35 across 8 blueprints
**Total HTTP modules remaining:** 13 (all justified — see STAGE_1_REMAINING_HTTP_WEBHOOK_JUSTIFICATION.md)
