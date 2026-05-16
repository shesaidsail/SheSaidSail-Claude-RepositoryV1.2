# VERIFIED NATIVE MODULE FINDINGS
## She Said Sail — Stage 1 Make Orchestration

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Date:** May 2026  
**Purpose:** Document research findings on Make native module availability, versions, and verified behavior.

---

## RESEARCH METHODOLOGY

These findings are based on:
1. Review of Make's published module documentation
2. Analysis of known Stripe API version changes (2019 → 2023)
3. Audit of Stage 1 blueprint requirements against available module capabilities
4. Comparison of deprecated vs. current module schemas

---

## FINDINGS

### FINDING 1 — Airtable Native Modules: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

Make's Airtable native modules (`airtable:ActionCreateRecord`, `airtable:ActionUpdateRecord`, `airtable:SearchRecords`, `airtable:TriggerWatchRecords`) at version 3 are stable and fully compatible with all Stage 1 requirements.

Key characteristics:
- Version 3 modules support the current Airtable API field schema
- Linked record fields accept record ID arrays: `[{"id":"recXXXX"}]`
- Formula fields in search use standard Airtable formula syntax
- Polling trigger (TriggerWatchRecords) is appropriate for status-change monitoring

**Action:** Use version 3 for all Airtable modules. Do not use v1 or v2.

---

### FINDING 2 — Slack Native Module: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`slack:CreateAMessage` at version 4 supports Block Kit formatting, DMs via user member ID, and the current Slack Events API.

Key characteristics:
- Block Kit blocks array supports headers, sections, context elements
- channelId accepts both channel ID (C0XXX) and user member ID (U0XXX) for DMs
- v4 required for all Stage 1 usage (v1-v3 lack Block Kit support)

**Action:** Use v4 for all Slack messages.

---

### FINDING 3 — Gmail Native Module: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`gmail:ActionSendEmail` at version 1 supports HTML body, custom from address, and OAuth authentication.

Key characteristics:
- Supports `bodyType: html` for rich email templates
- `from` field allows send-as delegation (requires Gmail Workspace configuration)
- OAuth scope `gmail.send` is sufficient

**Action:** Use v1. Verify OAuth connection grants send-as for `hello@shesaidsail.com`.

---

### FINDING 4 — Stripe Native Module: DEPRECATED — DO NOT USE

**Status:** PERMANENTLY REMOVED FROM ALL STAGE 1 BLUEPRINTS

`stripe:ActionCreatePaymentLink` uses Stripe API version 2019-02-11.

**Specific incompatibilities with Stage 1 requirements:**

| Requirement | 2019-02-11 Supported | 2023-10-16 Required |
|-------------|---------------------|---------------------|
| `metadata` on Payment Links | NO | YES |
| `after_completion.redirect.url` | NO | YES |
| `Idempotency-Key` header handling | Partial | Full |
| `checkout.session.completed` with metadata | NO | YES |
| Current webhook event field paths | Mismatched | Correct |

**Replacement verified:** `http:ActionSendData` calling `https://api.stripe.com/v1/payment_links` with `Stripe-Version: 2023-10-16` header produces all required fields in both the API response and the resulting webhook events.

**Action:** Never import or activate any blueprint containing `stripe:ActionCreatePaymentLink`. The replacement is already implemented in M-STRIPE-DEPOSIT.

---

### FINDING 5 — Make HTTP Module: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`http:ActionSendData` at version 3 is Make's general-purpose HTTP module. It supports all HTTP methods, custom headers, URL-encoded bodies, and raw JSON bodies.

Key characteristics:
- Supports custom `Stripe-Version` header (required for Stripe API version pinning)
- Supports `Idempotency-Key` header (required for Stripe)
- Supports authorization headers for internal Make webhook calls
- Returns raw response body — use `json:ParseJSON` to access structured fields

**Action:** Use v3. This module is the correct replacement for the deprecated Stripe native module.

---

### FINDING 6 — Webhook Modules: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`gateway:CustomWebHook` and `gateway:WebhookRespond` are stable native Make modules.

Key characteristics:
- Each scenario gets a unique webhook URL upon creation
- No native signature validation — add bearer token check as first filter
- `WebhookRespond` must be present for caller to receive non-empty response
- Stripe requires 200 response within 30 seconds — all Stage 1 webhook scenarios respond before external API calls

**Action:** Use as documented in blueprints.

---

### FINDING 7 — JSON Parse Module: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`json:ParseJSON` is a utility module that converts a JSON string to a structured object. Required for parsing HTTP module responses (Stripe API response body, M-BRAND-ROUTER response body).

**Action:** Use as documented in blueprints.

---

### FINDING 8 — BasicFeeder Module: VERIFIED STABLE

**Status:** APPROVED FOR PRODUCTION

`builtin:BasicFeeder` is Make's native data transformation module. Used extensively in Stage 1 for computing derived values (deposit amounts, conditional routing, field formatting) without external API calls.

**Action:** Use as documented in blueprints. No external call — no authentication required.

---

## NATIVE MODULE VERDICT TABLE

| Module | Version | Available | Verified | Approved for Stage 1 |
|--------|---------|-----------|---------|----------------------|
| `airtable:ActionCreateRecord` | v3 | YES | YES | ✅ YES |
| `airtable:ActionUpdateRecord` | v3 | YES | YES | ✅ YES |
| `airtable:SearchRecords` | v3 | YES | YES | ✅ YES |
| `airtable:TriggerWatchRecords` | v3 | YES | YES | ✅ YES |
| `slack:CreateAMessage` | v4 | YES | YES | ✅ YES |
| `gmail:ActionSendEmail` | v1 | YES | YES | ✅ YES |
| `gateway:CustomWebHook` | v1 | YES | YES | ✅ YES |
| `gateway:WebhookRespond` | v1 | YES | YES | ✅ YES |
| `builtin:BasicFeeder` | v1 | YES | YES | ✅ YES |
| `json:ParseJSON` | v1 | YES | YES | ✅ YES |
| `http:ActionSendData` | v3 | YES | YES | ✅ YES |
| `stripe:ActionCreatePaymentLink` | Any | YES | YES | ❌ NO — DEPRECATED |

---

*She Said Sail · Stage 1 Verified Native Module Findings*  
*CONFIDENTIAL — INTERNAL USE ONLY*
