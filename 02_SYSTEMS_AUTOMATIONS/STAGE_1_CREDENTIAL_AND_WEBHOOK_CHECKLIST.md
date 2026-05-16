# STAGE 1 CREDENTIAL AND WEBHOOK CHECKLIST
## She Said Sail — Pre-Sandbox Make Build Credential Governance

**Status:** REQUIREMENTS DOCUMENTED — Vault Population and Webhook Registration Pending
**Date:** 2026-05-16
**Owner:** Will (Founder)
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION (Section 1.3, Section 18.2)
**Classification:** CONFIDENTIAL — Internal Use Only — No Credentials in This Document

---

## GOVERNANCE RULES

1. No credential is stored in GitHub, Airtable, Make environment variables accessible to non-Will parties, or any frontend code
2. All credentials live in the designated credential vault — location documented separately in writing accessible to Will and Luciana only
3. Every credential entry in the vault includes: service name, credential type, value, created date, last rotation date, rotating party, next rotation date
4. Rotation governance: dashboard access codes rotated every 90 days minimum and on every team member departure
5. This document defines WHAT is required — not WHERE it is stored or its value
6. Webhook secrets are credentials — treated identically to API keys

---

## SECTION 1 — CREDENTIAL VAULT REQUIREMENTS

### 1.1 Stripe

**Purpose in system:** Payment event source of truth. Webhook events → Make. Payment link generation from Make via Stripe API.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Stripe Secret Key | API key (`sk_live_...`) | Make Stripe module — payment link creation, payout reads | 90 days; team departure; any security event |
| Stripe Publishable Key | Public key (`pk_live_...`) | Booking tool frontend (Netlify) — Stripe.js | 90 days |
| Stripe Webhook Signing Secret | Webhook secret (`whsec_...`) | Make webhook endpoint — event validation | On every Make URL change; 90 days |
| Stripe Test Secret Key | API key (`sk_test_...`) | Make sandbox scenarios only | 90 days |
| Stripe Test Webhook Signing Secret | Webhook secret | Make sandbox endpoint validation | On sandbox URL change |

**Vault entry requirements for each:**
- Service: Stripe
- Environment: Production / Sandbox (separate entries)
- Credential type: Secret Key / Publishable Key / Webhook Signing Secret
- Make variable name (how it is referenced in Make): e.g., `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`
- Last rotation: [date]
- Next rotation: [date + 90 days]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm Stripe account is in live mode for production credentials
- [ ] Confirm Stripe account is in test mode for sandbox credentials
- [ ] Confirm Make Stripe module connection uses the correct environment key
- [ ] Confirm Stripe publishable key in Booking tool (Netlify) matches the correct environment

---

### 1.2 Claude (Anthropic API)

**Purpose in system:** Intelligence layer — response generation, classification, context injection. Called by Make via HTTP module with Bearer token.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Anthropic API Key | Bearer token | Make HTTP module — all Claude API calls | Per security baseline; on any suspected exposure; 90 days |

**Vault entry requirements:**
- Service: Anthropic API
- Environment: Production (single key used for all environments — sandbox calls use same key, different prompt versions)
- Credential type: API Key
- Make variable name: `ANTHROPIC_API_KEY`
- Model version in use: claude-sonnet-4-6 (confirm current version in all Make scenarios at build time)
- Last rotation: [date]
- Next rotation: [date + 90 days]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm API key is active and has sufficient usage tier for expected call volume
- [ ] Confirm Make HTTP module header is `Authorization: Bearer {{ANTHROPIC_API_KEY}}`
- [ ] Confirm model ID in Make HTTP request body matches current production model
- [ ] Confirm prompt version ID is read from AI_Prompt_Versions table before each call — not hardcoded in Make

**Governance note:** Every Make scenario that calls the Claude API must:
1. Read the current production prompt version from AI_Prompt_Versions (Will_Approved = true, Status = LIVE)
2. Inject prompt version ID into the Audit Log entry for that action
3. Include AI_Confidence_Score in the response parse and write to the corresponding Airtable field

---

### 1.3 Quo SMS

**Purpose in system:** SMS delivery layer — client-facing text messages triggered by Make.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Quo API Key | API key | Make HTTP module — SMS sends | 90 days; on any suspected exposure |
| Quo Sender ID / Number | Sending number | All Quo SMS sends | Changes with number changes |

**Vault entry requirements:**
- Service: Quo SMS
- Environment: Production (confirm if Quo provides a test/sandbox mode — if so, use for sandbox Make scenarios)
- Credential type: API Key
- Make variable name: `QUO_API_KEY`
- Sender number/ID: [document in vault — not in this file]
- API endpoint base URL: [document in vault]
- Last rotation: [date]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm Quo account is active and SMS credits are sufficient
- [ ] Confirm Make HTTP module uses correct Quo API endpoint and authentication header format
- [ ] Confirm sender number/ID is approved for A2P messaging if required by carrier regulations
- [ ] Confirm opt-out handling is in place — Quo must handle STOP replies; confirm Make does not re-send to opted-out numbers
- [ ] Test with a single SMS in sandbox mode before building full sequence

**Governance note:** All Quo SMS sends must be preceded by:
- Emergency_Flag = false check
- Automations_Paused = false check

If either is true, Make must log the skip to the Audit Log and halt — no SMS send.

---

### 1.4 Gmail (hello@shesaidsail.com)

**Purpose in system:** Email delivery layer — client-facing emails triggered by Make.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Gmail OAuth Client ID | OAuth 2.0 | Make Gmail module authentication | On app re-registration; on security event |
| Gmail OAuth Client Secret | OAuth 2.0 | Make Gmail module authentication | On app re-registration; on security event |
| Gmail Refresh Token | OAuth 2.0 | Make Gmail module — persistent access | On revocation; annually at minimum |
| Gmail App Password (fallback) | Password | Fallback SMTP if OAuth fails | On main credential rotation |

**Vault entry requirements:**
- Service: Gmail
- Account: hello@shesaidsail.com
- Environment: Production
- Make module: Gmail module (not HTTP — use native Make Gmail module)
- OAuth app name in Google Cloud Console: [document in vault]
- Last token refresh: [date]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm OAuth token is active — test with a Make Gmail send to Will's personal address
- [ ] Confirm sender display name is set correctly: `Luciana | She Said Sail` (SSS) or `Luciana | Mare Executive` (ME)
- [ ] Confirm reply-to address is configured: hello@shesaidsail.com
- [ ] Confirm Gmail sending limits are understood (500/day via Gmail API standard; upgrade to Google Workspace sending limits if needed)
- [ ] Confirm Make email module is using hello@shesaidsail.com, not a personal address

**Governance note:** All Gmail sends must be preceded by:
- Emergency_Flag = false check
- Automations_Paused = false check

The FROM display name must match the brand being served. SSS emails must not show Mare Executive branding and vice versa. The M-BRAND-ROUTER classification must complete before the email module runs.

---

### 1.5 Slack

**Purpose in system:** Internal operations communication — Slack DMs to Will, alerts to #sss-ops-alerts and #sss-emergency-ops channels. Not client-facing.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Slack Bot Token | OAuth Bot Token (`xoxb-...`) | Make Slack module — channel posts, DMs | On token revocation; 90 days; team departure |
| Slack Webhook URL — #sss-ops-alerts | Incoming webhook URL | Make — operational alerts | On webhook deletion/recreation |
| Slack Webhook URL — #sss-emergency-ops | Incoming webhook URL | Make EMERGENCY-001 — emergency alerts | On webhook deletion/recreation |
| Slack User ID — Will | User ID (`U...`) | Make — direct DM to Will | Permanent — does not change |
| Slack User ID — Luciana | User ID (`U...`) | Make — direct DM to Luciana | Permanent — does not change |

**Vault entry requirements:**
- Service: Slack
- Workspace: She Said Sail workspace
- Bot name in Slack: [document in vault]
- Required bot permissions: `chat:write`, `im:write`, `channels:read`
- Make module: Slack module (not HTTP)
- Last token rotation: [date]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm Slack bot is installed in the She Said Sail workspace with correct permissions
- [ ] Confirm bot has access to #sss-ops-alerts channel
- [ ] Confirm bot has access to #sss-emergency-ops channel
- [ ] Confirm Will's Slack User ID is documented in vault (required for DM sends)
- [ ] Confirm Luciana's Slack User ID is documented in vault
- [ ] Test bot send to #sss-ops-alerts before building EMERGENCY-001

**Governance note:** #sss-emergency-ops receives ONLY emergency alerts. Make EMERGENCY-001 posts to this channel only on Emergency_Flag = true. Do not route operational alerts to this channel. It is monitored at all times by Will and Luciana.

---

### 1.6 Airtable (Production Access Token for Make)

**Purpose in system:** Make reads from and writes to Airtable via the Airtable module. Requires a Personal Access Token (PAT) scoped to production base.

| Credential | Type | Required For | Rotation Trigger |
|---|---|---|---|
| Airtable PAT — Production | Personal Access Token | Make Airtable module — read/write to appdZ49WqgjRXxA1R | 90 days; team departure; security event |
| Airtable PAT — Sandbox | Personal Access Token | Make Airtable module — read/write to appxOoLdiIVt733kV | 90 days |
| Airtable PAT — Financials | Personal Access Token | Make Airtable module — read/write to apprDKQtV2GInThwE | 90 days |

**Vault entry requirements:**
- Service: Airtable
- Base scope: Separate tokens per base (do not use a single token scoped to all bases)
- Required scopes: `data.records:read`, `data.records:write` for each target base
- Make module: Airtable module (not HTTP)
- Last rotation: [date]
- Rotating party: Will

**Pre-sandbox verification steps:**
- [ ] Confirm sandbox PAT is scoped only to appxOoLdiIVt733kV — cannot accidentally write to production
- [ ] Confirm production PAT is scoped to appdZ49WqgjRXxA1R only
- [ ] Confirm Make scenario connections use the correct PAT per environment
- [ ] Confirm PATs do not have schema modification permissions (data records only)

---

## SECTION 2 — STRIPE WEBHOOK REGISTRATION CHECKLIST

**Status: DO NOT REGISTER — Make webhook URL does not yet exist**

This checklist documents exactly what to do once a Make sandbox scenario URL is available. No registration should occur before that URL exists.

### 2.1 Stripe Events to Register

The following Stripe events must route to Make:

| Event | Stripe Event Name | Triggers Make Scenario | Purpose |
|---|---|---|---|
| Deposit created (payment intent) | `payment_intent.created` | — | Log only — optional monitoring |
| Deposit payment succeeded | `payment_intent.succeeded` (amount = deposit) | BOOKING-002 | Update Booking Status = DEPOSIT_PAID |
| Balance payment succeeded | `payment_intent.succeeded` (amount = balance) | CHARTER-002 | Update Booking Status = PAID |
| Payment failed | `payment_intent.payment_failed` | — | Alert Luciana — no automated client send |
| Payout created | `payout.created` | FINANCIAL-001 | Trigger financial reconciliation |
| Refund created | `charge.refund.updated` | — | Alert Will immediately — Founder Decision required |

**Note on distinguishing deposit vs balance payment:**
Make must distinguish deposit vs balance payment from the same `payment_intent.succeeded` event. Method: compare `payment_intent.amount` against `Deposit Amount` field (fldMa9x5WNl0h7Wta) on the matched Booking record. If amount matches deposit, trigger BOOKING-002. If amount matches balance (Package Price - Deposit), trigger CHARTER-002. Include fallback alert to Luciana for any unmatched amount.

### 2.2 Webhook Endpoint Security Requirements

Every Stripe webhook endpoint in Make must implement:

1. **Signing secret validation** — Make must validate the `Stripe-Signature` header using the webhook signing secret before processing any event
2. **Timestamp validation** — reject events older than 5 minutes (replay attack protection)
3. **Idempotency check** — before any Airtable write, check if the Stripe event ID has already been processed (store event IDs in Audit Log)
4. **401 rejection** — invalid signatures must return 401 immediately, before any processing
5. **HTTPS only** — Make webhook URLs are HTTPS by default — do not accept any HTTP endpoint

### 2.3 Sandbox Webhook Registration (Do First)

Before registering a production Stripe webhook, validate the full flow in sandbox:

**Sandbox prerequisites:**
- [ ] Stripe test mode is active on the sandbox account/key
- [ ] Make sandbox scenario URL exists (generated by Make when scenario is created)
- [ ] Sandbox Make scenario Airtable connection points to appxOoLdiIVt733kV (not production)

**Sandbox registration steps:**
1. [ ] Log into Stripe Dashboard → Developers → Webhooks
2. [ ] Click "Add endpoint" → enter Make sandbox scenario URL
3. [ ] Select events: `payment_intent.succeeded`, `payout.created` (start with these two)
4. [ ] Copy webhook signing secret → store in vault under "Stripe Test Webhook Signing Secret"
5. [ ] Configure Make HTTP module to validate `Stripe-Signature` header using this secret
6. [ ] Use Stripe's "Send test event" to trigger `payment_intent.succeeded` → confirm Make receives and processes
7. [ ] Confirm Airtable sandbox record is created/updated (not production record)
8. [ ] Confirm Audit Log entry created in sandbox base
9. [ ] Document test results in Sandbox_Control table (appxOoLdiIVt733kV, tblSA3xc4vNqBAFL4)

### 2.4 Production Webhook Registration (After Sandbox Validation)

**Production prerequisites:**
- [ ] Sandbox validation complete (Section 2.3 all checked)
- [ ] Will has reviewed sandbox test results
- [ ] Production Make scenario URL exists
- [ ] Founder Decision record created: Type = SYSTEM, Urgency = THIS_WEEK, approving production Stripe webhook registration
- [ ] Audit Log entry created before registration

**Production registration steps:**
1. [ ] Log into Stripe Dashboard → Developers → Webhooks (confirm live mode is active)
2. [ ] Click "Add endpoint" → enter production Make scenario URL
3. [ ] Select events: `payment_intent.succeeded`, `payout.created`, `payment_intent.payment_failed`, `charge.refund.updated`
4. [ ] Copy webhook signing secret → store in vault under "Stripe Webhook Signing Secret (Production)"
5. [ ] Update Make production scenario HTTP module to use production signing secret
6. [ ] Confirm old test signing secret in vault is labeled clearly as TEST (do not confuse with production)
7. [ ] Use Stripe Dashboard → send test event to production endpoint — confirm receipt without creating duplicate records (idempotency check)
8. [ ] Monitor Make scenario execution log for first 24 hours after activation
9. [ ] Log registration in Audit Log: Action_Type = SYSTEM_DEPLOYMENT, Scenario_ID = BOOKING-002, notes = Stripe production webhook registered
10. [ ] Document in Make_Scenarios registry (tbl08IpivapVQZUto): Stripe_Webhook_Endpoint, Registration_Date, Events_Subscribed

### 2.5 Webhook Registration — Fields to Log in Make_Scenarios Registry

When webhook is registered (sandbox and production), update the corresponding Make_Scenarios record in Airtable (tbl08IpivapVQZUto):

| Field to Update | Value |
|---|---|
| Stripe_Endpoint_URL | The Make webhook URL |
| Stripe_Events_Subscribed | payment_intent.succeeded, payout.created, etc. |
| Webhook_Registered_Date | Date of registration |
| Environment | Sandbox / Production |
| Signing_Secret_Location | "Vault — Stripe Webhook Secret" (not the value itself) |

---

## SECTION 3 — PRE-SANDBOX BUILD VERIFICATION CHECKLIST

Complete this checklist before the first Make sandbox scenario is built or tested.

### 3.1 Credentials

- [ ] Stripe test credentials in vault — Secret Key, Webhook Signing Secret (test)
- [ ] Anthropic API key in vault — confirmed active, sufficient tier
- [ ] Quo SMS API key in vault — confirmed active, credits sufficient for test sends
- [ ] Gmail OAuth token in vault — confirmed active, test send successful
- [ ] Slack bot token in vault — confirmed active, test post to #sss-ops-alerts successful
- [ ] Airtable sandbox PAT in vault — scoped to appxOoLdiIVt733kV only
- [ ] Airtable production PAT in vault — scoped to appdZ49WqgjRXxA1R only

### 3.2 Make Environment Configuration

- [ ] Sandbox Make scenario connections use Airtable sandbox PAT (appxOoLdiIVt733kV)
- [ ] Sandbox Make scenario connections use Stripe test key
- [ ] Production Make scenario connections use Airtable production PAT (appdZ49WqgjRXxA1R)
- [ ] All Make API credentials stored in Make's built-in secure data store — not hardcoded in scenario modules
- [ ] Make scenario environment tag is set: all sandbox scenarios tagged Environment = Sandbox

### 3.3 Airtable Readiness

- [ ] Sandbox base (appxOoLdiIVt733kV) is accessible from Make
- [ ] Production base (appdZ49WqgjRXxA1R) Bookings, Requests, and Audit Log tables confirmed accessible from Make
- [ ] Environment field (singleSelect) is present on Bookings and Requests — Make writes "Sandbox" on all sandbox test records
- [ ] Idempotency_Key field (singleLineText) is present on Bookings — Make writes hash key before any record creation

### 3.4 First Scenario to Build and Test

Recommended first sandbox scenario: **INBOUND-001** (simplest — no Stripe, no Claude API, no payment processing)

Test sequence:
1. Simulate Webflow form submission → confirm Airtable Request record created in sandbox
2. Confirm INBOUND-001 auto-reply email sends from hello@shesaidsail.com
3. Confirm Slack notification reaches Luciana
4. Confirm Audit Log entry created
5. Confirm Environment = Sandbox on all created records
6. Log results in Sandbox_Control table

---

## SECTION 4 — CREDENTIAL ROTATION SCHEDULE

| Service | Credential | Next Rotation Due | Owner |
|---|---|---|---|
| Stripe | Secret Key (Production) | 90 days from creation | Will |
| Stripe | Webhook Signing Secret | 90 days; on URL change | Will |
| Anthropic API | API Key | 90 days | Will |
| Quo SMS | API Key | 90 days | Will |
| Gmail | OAuth Refresh Token | Annually | Will |
| Slack | Bot Token | 90 days | Will |
| Airtable | Production PAT | 90 days | Will |
| Airtable | Sandbox PAT | 90 days | Will |

**All rotations logged in vault with:** date, rotating party, new credential reference, previous credential archived (not deleted) for 30-day grace period.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_1_CREDENTIAL_AND_WEBHOOK_CHECKLIST v1.0*
*Date: 2026-05-16*
*Owner: Will (Founder)*
*No credentials stored in this document or this repository*
*Authority: 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION Section 18.2*
