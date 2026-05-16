# STAGE 1 CREDENTIAL AND WEBHOOK CHECKLIST
**Project:** She Said Sail + Mare Executive — Make.com Automation System  
**Base:** appdZ49WqgjRXxA1R  
**Prepared by:** Production Reliability Engineering  
**Date:** 2026-05-16  
**Purpose:** Complete credential inventory, scope requirements, storage locations, rotation schedule, and verification steps for all Stage 1 external connections  
**Status:** ACTIVE — update Status and Test Result columns as each credential is confirmed

---

## Credential Summary Dashboard

| Credential | Service | Make Connection Name | Owner | Status | Test Result |
|------------|---------|---------------------|-------|--------|-------------|
| Airtable PAT | Airtable | `SSS_AIRTABLE_PAT` | Will | NEEDS SETUP | UNTESTED |
| Stripe Test Secret Key | Stripe | `SSS_STRIPE_TEST_SECRET` | Will | NEEDS SETUP | UNTESTED |
| Stripe Test Webhook Secret | Stripe | `SSS_STRIPE_WEBHOOK_SECRET_TEST` | Make builder | BLOCKED (BLK-008) | UNTESTED |
| Slack Bot Token | Slack | `SSS_SLACK_BOT` | Luciana | NEEDS SETUP | UNTESTED |
| Gmail OAuth (SSS) | Gmail | `SSS_GMAIL_HELLO` | Will | NEEDS SETUP | UNTESTED |
| Gmail OAuth (ME) | Gmail | `ME_GMAIL_HELLO` | Will | NEEDS SETUP | UNTESTED |
| Quo SMS API Key | Quo SMS | `SSS_QUO_SMS_API` | Luciana | NEEDS SETUP | UNTESTED |
| Anthropic API Key | Anthropic | `SSS_ANTHROPIC_API` | Will | STAGED (Stage 2) | N/A |

---

## Naming Convention

All Make.com connections follow this naming pattern:
```
{BRAND}_{SERVICE}_{DESCRIPTOR}
SSS_  = She Said Sail (primary — used for both brands unless ME-specific)
ME_   = Mare Executive (only where ME has a distinct credential)
```

All credential values are stored in Make.com's built-in credential vault (Make Connections), never in scenario data stores, Airtable, or source-controlled files. Never paste API keys or secrets into Make scenario notes or description fields.

---

## CREDENTIAL: Airtable Personal Access Token

| Field | Value |
|-------|-------|
| **Credential Name** | SSS Airtable Production PAT |
| **Make Connection Name** | `SSS_AIRTABLE_PAT` |
| **Service** | Airtable |
| **Token Format** | `pat[A-Za-z0-9]{14}.[a-f0-9]{64}` |
| **Owner** | Will |
| **Rotation Schedule** | Every 90 days; immediately if compromised |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### Required Scopes

Generate the PAT at https://airtable.com/create/tokens with the following scopes:

```
data.records:read       — Read records from all tables
data.records:write      — Create and update records
schema.bases:read       — Read table schemas and field definitions
webhook.manage:write    — Create and manage Airtable webhooks (if using native triggers)
```

**Bases the token must access:**
- `appdZ49WqgjRXxA1R` — She Said Sail + Mare Executive production base

### Make Connection Setup

1. In Make.com: Connections → Add a Connection → Airtable
2. Select "OAuth 2.0 / Personal Access Token"
3. Paste the PAT into the token field
4. Name the connection: `SSS_AIRTABLE_PAT`
5. Click Save and Test

### Test Command — Airtable Read Verification

In Make.com, create a one-off test scenario with a single HTTP module:

```
Module: HTTP — Make a Request
URL: https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests
Method: GET
Headers:
  Authorization: Bearer {{SSS_AIRTABLE_PAT}}
Query parameters:
  maxRecords: 1
  view: Grid view
```

Expected response: HTTP 200, JSON body with `records` array.

### Verification Checklist — Airtable

```
[ ] PAT generated with all 4 required scopes
[ ] PAT grants access to base appdZ49WqgjRXxA1R
[ ] Make connection SSS_AIRTABLE_PAT created and saved
[ ] HTTP test call returns HTTP 200 with records from Requests table
[ ] HTTP test write: Create a record in Requests with Environment = sandbox → success
[ ] HTTP test write: Attempt to read non-existent base → returns 403 (scope isolation confirmed)
[ ] PAT expiry date documented and calendar reminder set for rotation
```

**PAT Expiry Date:** `[TO BE DOCUMENTED]`  
**Calendar reminder set by:** `[TO BE DOCUMENTED]`

---

## CREDENTIAL: Stripe Test Mode API Key

| Field | Value |
|-------|-------|
| **Credential Name** | Stripe Test Secret Key |
| **Make Connection Name** | `SSS_STRIPE_TEST_SECRET` |
| **Service** | Stripe |
| **Key Format** | `sk_test_[A-Za-z0-9]{99}` |
| **Owner** | Will |
| **Rotation Schedule** | At go-live (replace test key with live key); test key rotated every 6 months |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### Stripe Test Mode Notes

- All Stage 1 Stripe operations use test mode exclusively.
- Test mode key prefix: `sk_test_` (live key prefix: `sk_live_` — do NOT use during Stage 1).
- Test mode charges do NOT process real money.
- Test mode payment links DO send emails if Stripe email settings are not disabled — disable Stripe's built-in email notifications during testing.

### Stripe Dashboard Configuration

1. Log in to Stripe Dashboard → toggle to **Test Mode** (top right).
2. Developers → API Keys → Reveal Secret Key (or create a restricted key).
3. If creating a restricted key, required permissions:
   ```
   Payment Intents: Write
   Payment Links: Write
   Checkout Sessions: Write
   Webhooks: Read
   ```
4. Store key in Make: Connections → Add Connection → Stripe → paste key → name `SSS_STRIPE_TEST_SECRET`.

### Make Connection Setup

```
Connection Type: Stripe (built-in Make module) OR HTTP (custom)
If using Stripe Make module:
  - API Key: sk_test_[...]
  - Connection Name: SSS_STRIPE_TEST_SECRET
  - Click Verify → should return Stripe account details

If using HTTP module for Stripe API calls:
  - Base URL: https://api.stripe.com/v1
  - Auth type: Basic Auth
  - Username: sk_test_[...]  (Stripe uses API key as Basic Auth username)
  - Password: (empty)
```

### Disable Stripe Test Email Notifications

In Stripe Dashboard (Test Mode) → Settings → Emails:
- Uncheck "Send emails for successful payments" during Stage 1 testing.
- Recheck when testing confirmation emails separately.

### Verification Checklist — Stripe Test API Key

```
[ ] Stripe account in Test Mode (verify "TEST DATA" banner visible in dashboard)
[ ] Secret key begins with sk_test_
[ ] Make connection SSS_STRIPE_TEST_SECRET created and verified
[ ] Test API call: create a test PaymentIntent via Make HTTP module
    URL: https://api.stripe.com/v1/payment_intents
    Method: POST
    Body: amount=50000&currency=aud&confirm=false
    Expected: HTTP 200, PaymentIntent object returned
[ ] Test PaymentIntent visible in Stripe Dashboard → Test Mode → Payments
[ ] Stripe built-in receipt emails disabled for test mode
[ ] Key is NOT sk_live_ (critical check)
```

---

## CREDENTIAL: Stripe Test Webhook Signing Secret

| Field | Value |
|-------|-------|
| **Credential Name** | Stripe Test Webhook Signing Secret |
| **Make Connection Name** | `SSS_STRIPE_WEBHOOK_SECRET_TEST` (stored as Make data store variable) |
| **Service** | Stripe |
| **Secret Format** | `whsec_[A-Za-z0-9]{64}` |
| **Owner** | Make builder |
| **Rotation Schedule** | When Make webhook URL changes; at go-live |
| **Status** | BLOCKED (BLK-008 — webhook URL not yet generated) |
| **Test Result** | UNTESTED |

### Webhook Event Types to Register

In Stripe Dashboard → Developers → Webhooks → Add Endpoint:

```
Events to register (select ALL of the following):
  payment_intent.created
  payment_intent.succeeded
  payment_intent.payment_failed
  checkout.session.completed
  checkout.session.expired
```

Rationale:
- `payment_intent.succeeded` → triggers M-STRIPE-DEPOSIT to update Airtable and create Booking
- `checkout.session.completed` → alternative trigger for payment link completions
- `payment_intent.payment_failed` → triggers failure alert to #sss-ops-alerts
- `checkout.session.expired` → triggers expiry alert to concierge

### Webhook URL Format

```
Format: https://hook.{region}.make.com/{unique-token}
Example: https://hook.eu1.make.com/abc123xyz456...

Current URL: [TO BE GENERATED — resolve BLK-008 first]
Region note: URL region depends on Make.com account region setting.
             Check Make account settings to confirm region before sharing URL with Stripe.
```

### Stripe Signature Validation in Make

Add this as the FIRST module in M-STRIPE-DEPOSIT, immediately after the Custom Webhook trigger:

```
Module: HTTP — Make a Request (or use Make's built-in Stripe verification)

Validation logic:
1. Retrieve header: Stripe-Signature (t=timestamp,v1=hash)
2. Parse timestamp from header: t=...
3. Construct signed payload: "{timestamp}.{raw_request_body}"
4. Compute HMAC-SHA256 of signed payload using STRIPE_WEBHOOK_SECRET
5. Compare computed signature with v1 value from header
6. If mismatch: return HTTP 400 to Stripe, log to Audit_Log, halt scenario
7. If match: return HTTP 200, continue scenario

In Make using built-in Stripe module:
- The Stripe trigger module handles signature validation automatically
- Store webhook secret in Make Data Store as a secure variable
- Reference as: {{datastore.STRIPE_WEBHOOK_SECRET_TEST}}
```

### Test Event Command — Stripe CLI

```bash
# Install Stripe CLI if not already installed:
brew install stripe/stripe-cli/stripe

# Authenticate (use test mode API key):
stripe login --api-key sk_test_[...]

# Forward events to Make webhook URL (for local testing):
stripe listen --forward-to https://hook.eu1.make.com/[token]

# Trigger specific events:
stripe trigger payment_intent.succeeded
stripe trigger checkout.session.completed
stripe trigger payment_intent.payment_failed

# Verify event delivery in terminal output and Make execution log
```

### Verification Checklist — Stripe Webhook

```
[ ] BLK-008 resolved (Make webhook URL generated)
[ ] Webhook endpoint registered in Stripe Test Mode dashboard
[ ] All 5 event types selected
[ ] Signing secret (whsec_...) stored in Make Data Store as STRIPE_WEBHOOK_SECRET_TEST
[ ] Signature validation module added to M-STRIPE-DEPOSIT (step 1)
[ ] Stripe CLI test: stripe trigger payment_intent.succeeded
    → Make execution log shows 1 run
    → Stripe dashboard shows event as "Delivered" (HTTP 200)
[ ] Negative test: send malformed webhook (wrong signature)
    → Make returns HTTP 400
    → No scenario actions executed
    → Audit_Log entry created with Event_Type = ERROR_OCCURRED
[ ] Stripe dashboard shows webhook endpoint status as "Active"
```

---

## CREDENTIAL: Slack Bot OAuth Token

| Field | Value |
|-------|-------|
| **Credential Name** | SSS Slack Bot |
| **Make Connection Name** | `SSS_SLACK_BOT` |
| **Service** | Slack |
| **Token Format** | `xoxb-[0-9]{11}-[0-9]{13}-[A-Za-z0-9]{24}` |
| **Owner** | Luciana |
| **Rotation Schedule** | When bot is reinstalled; Slack tokens do not expire unless revoked |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### Slack App Setup

1. Go to https://api.slack.com/apps → Create New App → From Scratch.
2. App name: `She Said Sail Bot`
3. Workspace: She Said Sail Slack workspace.
4. Navigate to OAuth & Permissions → Bot Token Scopes → Add:

```
Required OAuth Scopes:
  chat:write          — Send messages to channels
  chat:write.public   — Send to channels bot is not a member of (alternative)
  channels:read       — View list of channels (for channel ID lookup)
  users:read          — View user profiles (for @mentions in alerts)
  channels:join       — Bot can join public channels (alternative to invite)
```

5. Navigate to Install App → Install to Workspace → Authorize.
6. Copy the Bot User OAuth Token (`xoxb-...`).
7. In Make.com: Connections → Add → Slack → Paste token → Name: `SSS_SLACK_BOT`.

### Channel Invitations

The bot must be invited to the following channels BEFORE any Slack module is tested:

```
Required channels:
  #sss-ops-alerts      — New lead alerts, assignment alerts, deposit alerts, booking alerts
  #sss-emergency-ops   — Error alerts at all 4 severity levels

Invitation command (run in Slack):
  /invite @She Said Sail Bot

Do this in BOTH channels. Failing to invite the bot causes:
  Make error: "not_in_channel" (Slack API error code)
  Scenario halts at Slack module
```

### Test Message Command

In Make.com, create a test run or use the Slack module directly:

```
Module: Slack — Create a Message
Channel: #sss-ops-alerts
Text: [TEST] Stage 1 Slack credential verification — She Said Sail Bot is online. Environment: sandbox
```

Expected: Message appears in #sss-ops-alerts within 5 seconds.

### Verification Checklist — Slack

```
[ ] Slack app created: "She Said Sail Bot"
[ ] All 4 OAuth scopes added (chat:write, chat:write.public, channels:read, users:read)
[ ] App installed to She Said Sail workspace
[ ] Bot User OAuth Token saved in Make: SSS_SLACK_BOT
[ ] Bot invited to #sss-ops-alerts (/invite @She Said Sail Bot)
[ ] Bot invited to #sss-emergency-ops (/invite @She Said Sail Bot)
[ ] Test message sent to #sss-ops-alerts → message visible in channel
[ ] Test message sent to #sss-emergency-ops → message visible in channel
[ ] Block Kit test: TPL-SLACK-001 rendered correctly in #sss-ops-alerts
[ ] @channel mention works in TPL-ERR-001 Level 3/4 (critical alerts)
```

---

## CREDENTIAL: Gmail OAuth — She Said Sail

| Field | Value |
|-------|-------|
| **Credential Name** | SSS Gmail Hello |
| **Make Connection Name** | `SSS_GMAIL_HELLO` |
| **Service** | Gmail / Google OAuth 2.0 |
| **Account** | hello@shesaidsail.com |
| **Owner** | Will |
| **Rotation Schedule** | OAuth tokens auto-refresh; reauthorize annually or if revoked |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### Required Google OAuth Scopes

```
https://www.googleapis.com/auth/gmail.send    — Send email as hello@shesaidsail.com
```

Do NOT request broader scopes (`gmail.modify`, `gmail.readonly`, `mail.google.com`). Minimum scope principle applies.

### Make OAuth Connection Setup

1. In Make.com: Connections → Add → Gmail → OAuth 2.0.
2. Click "Sign in with Google."
3. Sign in as hello@shesaidsail.com (Will must do this step or delegate via Google Workspace admin).
4. Grant `gmail.send` scope only.
5. Name connection: `SSS_GMAIL_HELLO`.
6. Save and verify.

### Test Procedure (TEST MODE — Stage 1)

```
CRITICAL: During Stage 1, ALL email sends must go to a test address.
Never send to a real client email address during Stage 1.

Test recipient: will@shesaidsail.com (or a dedicated test inbox)
Test subject: [STAGE1-TEST] Booking Confirmation Email Render Test

Module: Gmail — Send an Email
Connection: SSS_GMAIL_HELLO
To: will@shesaidsail.com
Subject: [STAGE1-TEST] SSS Confirmation Render — {{charter_date}}
Content type: HTML
Body: TPL-EMAIL-001 with test variable values
```

### Verification Checklist — Gmail SSS

```
[ ] Google OAuth connection created for hello@shesaidsail.com
[ ] Only gmail.send scope granted (verify in Google Account → Security → Third-party access)
[ ] Make connection SSS_GMAIL_HELLO saved and verified
[ ] Test email sent to will@shesaidsail.com
[ ] Email received and HTML renders correctly (no broken styling)
[ ] "From" field shows: She Said Sail <hello@shesaidsail.com>
[ ] Reply-To is set to: hello@shesaidsail.com
[ ] Email does NOT go to spam (if it does, add SPF/DKIM records for shesaidsail.com)
[ ] All template variables render (no {{variable}} placeholders visible in received email)
[ ] M-BOOKING-CONFIRMATION uses test recipient override (NOT {{client_email}}) — verified in scenario config
```

---

## CREDENTIAL: Gmail OAuth — Mare Executive

| Field | Value |
|-------|-------|
| **Credential Name** | ME Gmail Hello |
| **Make Connection Name** | `ME_GMAIL_HELLO` |
| **Service** | Gmail / Google OAuth 2.0 |
| **Account** | hello@mareexecutive.com |
| **Owner** | Will |
| **Rotation Schedule** | OAuth tokens auto-refresh; reauthorize annually or if revoked |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### Setup Procedure

Identical to SSS Gmail setup above, substituting `hello@mareexecutive.com` and connection name `ME_GMAIL_HELLO`.

### Verification Checklist — Gmail ME

```
[ ] Google OAuth connection created for hello@mareexecutive.com
[ ] Only gmail.send scope granted
[ ] Make connection ME_GMAIL_HELLO saved and verified
[ ] Test email sent to will@shesaidsail.com (or Will's test address)
[ ] Email received with From: Mare Executive <hello@mareexecutive.com>
[ ] HTML template TPL-EMAIL-002 renders correctly
[ ] All variables populated (no raw {{...}} visible)
[ ] Test mode recipient override confirmed in M-BOOKING-CONFIRMATION scenario config
```

### Gmail Routing Logic in M-BOOKING-CONFIRMATION

```
In M-BOOKING-CONFIRMATION, brand routing determines which Gmail connection is used:

Router branch condition:
  IF {{brand}} = "she_said_sail"
    → Use connection: SSS_GMAIL_HELLO
    → Template: TPL-EMAIL-001
    → From: She Said Sail <hello@shesaidsail.com>
  IF {{brand}} = "mare_executive"
    → Use connection: ME_GMAIL_HELLO
    → Template: TPL-EMAIL-002
    → From: Mare Executive <hello@mareexecutive.com>

IMPORTANT: Both branches must override To: with will@shesaidsail.com during Stage 1.
Remove the override and restore {{client_email}} only at Stage 1 go-live sign-off.
```

---

## CREDENTIAL: Quo SMS API Key

| Field | Value |
|-------|-------|
| **Credential Name** | SSS Quo SMS API |
| **Make Connection Name** | `SSS_QUO_SMS_API` |
| **Service** | Quo SMS |
| **Key Format** | API key (format varies — confirm with Quo SMS documentation) |
| **Owner** | Luciana |
| **Rotation Schedule** | Every 180 days; immediately if compromised |
| **Status** | NEEDS SETUP |
| **Test Result** | UNTESTED |

### API Configuration

```
API Endpoint (outbound SMS):  https://api.quosms.com/v1/messages
                               (confirm current endpoint in Quo SMS developer docs)
Authentication:               API Key in Authorization header OR request body
                               (confirm method with Quo SMS docs)
HTTP Method:                  POST
Content-Type:                 application/json

Request body format (verify against Quo SMS API docs):
{
  "to": "+61[phone_number]",
  "from": "[your_sender_id_or_number]",
  "body": "{{sms_body}}"
}
```

### Rate Limit Awareness

```
Quo SMS rate limits (verify in Quo SMS account):
  Estimated limit: 10–100 messages per minute (confirm exact limit)
  Burst protection: Add a Make Error Handler on HTTP 429 (Too Many Requests)
  On 429: Wait 60 seconds → retry once → if still 429 → alert Slack #sss-ops-alerts

Stage 1 volume: Low (testing only, single sends)
Stage 2+ volume: May require rate limit management if concurrent bookings spike
```

### Storage in Make

```
Do NOT store the Quo SMS API key in:
  - Make scenario data stores (visible to all team members)
  - Airtable fields
  - Any source-controlled file

DO store in:
  - Make Connection: Create custom HTTP connection named SSS_QUO_SMS_API
  - Or: Make Data Store with restricted access (if API key cannot be stored as Make connection)
  - Connection type: API Key in header: Authorization: Bearer {{quo_api_key}}
```

### Test Procedure (TEST MODE — Stage 1)

```
CRITICAL: During Stage 1, ALL SMS sends must go to Will's phone.
Never send to a real client phone number during Stage 1.

Test recipient: {{WILL_TEST_PHONE}} — store Will's phone number in Make Data Store
Test message: [TEST] Stage 1 SMS verification — She Said Sail automation system active.

After Stage 1 sign-off, update M-STRIPE-DEPOSIT to use {{client_phone}} instead of {{WILL_TEST_PHONE}}.
```

### Verification Checklist — Quo SMS

```
[ ] Quo SMS API key obtained from Luciana's Quo SMS account
[ ] API key stored in Make connection: SSS_QUO_SMS_API
[ ] Will's test phone number stored in Make Data Store as WILL_TEST_PHONE
[ ] Test SMS sent via Make HTTP module → Will's phone receives message
[ ] SMS body renders correctly (no {{...}} placeholders)
[ ] Message length verified: ≤160 characters for SSS template, ≤160 for ME template
[ ] Sender ID displays correctly (She Said Sail or Mare Executive — configure in Quo SMS account)
[ ] Rate limit confirmed from Quo SMS documentation
[ ] Error handler for HTTP 429 implemented in M-STRIPE-DEPOSIT
[ ] Test mode recipient override confirmed ({{WILL_TEST_PHONE}} not {{client_phone}})
```

---

## CREDENTIAL: Anthropic API Key (STAGED — Stage 2)

| Field | Value |
|-------|-------|
| **Credential Name** | SSS Anthropic API |
| **Make Connection Name** | `SSS_ANTHROPIC_API` |
| **Service** | Anthropic (Claude API) |
| **Key Format** | `sk-ant-api03-[A-Za-z0-9-_]{95}` |
| **Owner** | Will |
| **Rotation Schedule** | Every 90 days |
| **Status** | STAGED — DO NOT ACTIVATE IN STAGE 1 |
| **Test Result** | N/A — Stage 1 does not use Claude API |

### Stage 1 Position

AI/Claude API integration is NOT part of Stage 1. Stage 1 is routing and intake only. The Anthropic API key should be obtained and stored in Stage 1 (to avoid delays when Stage 2 begins), but no Make scenario in Stage 1 should reference `SSS_ANTHROPIC_API`.

### Stage 2 Configuration (Document Now, Implement in Stage 2)

```
API Endpoint: https://api.anthropic.com/v1/messages
Model: claude-sonnet-4-6
Max Tokens: 
  - Brand routing classification: 100 tokens (low)
  - Concierge brief generation: 1,000 tokens (medium)
  - Full context injection: 4,000 tokens (high — Stage 2 only)
Temperature: 0 (for classification tasks), 0.7 (for content generation)

Stage 2 use cases:
  - M-BRAND-ROUTER: Claude classifies ambiguous brand from lead text
  - M-CONCIERGE-ASSIGNMENT: Claude generates concierge briefing from lead data
  - M-BOOKING-CONFIRMATION: Claude personalizes email copy (optional)

Stage 1 impact: NONE. No Stage 1 scenario calls the Anthropic API.
```

### Obtain and Store API Key (Do Now, Activate in Stage 2)

```
1. Will: Generate API key at https://console.anthropic.com/settings/keys
2. Store in Make: Connections → HTTP → Custom API Key connection
   Name: SSS_ANTHROPIC_API
   Auth: x-api-key: {{key}} in Authorization header
   Or: Store in Make Data Store (restricted) if Make HTTP connection not suitable
3. DO NOT connect this credential to any Stage 1 scenario module
4. Document: API key usage limits and billing threshold alerts set at $50/month
```

### Verification Checklist — Anthropic (Staged)

```
[ ] Anthropic account active under Will's credentials
[ ] API key generated and stored in Make Data Store as SSS_ANTHROPIC_API
[ ] Stage 1 scenarios verified: NONE reference SSS_ANTHROPIC_API
[ ] Billing alert set at $50/month in Anthropic console
[ ] Usage tracking enabled in Anthropic console
[ ] Stage 2 implementation notes documented in Stage 2 build spec
[ ] STAGED status acknowledged — activate only after Stage 1 sign-off
```

---

## Credential Rotation Calendar

| Credential | Rotation Interval | Next Rotation Due | Calendar Alert Set? |
|-----------|-------------------|-------------------|---------------------|
| Airtable PAT | 90 days | `[90 days from creation]` | [ ] |
| Stripe Test Key | At go-live | At go-live | N/A |
| Slack Bot Token | On reinstall | N/A (no expiry) | N/A |
| Gmail SSS OAuth | Annual | `[1 year from auth]` | [ ] |
| Gmail ME OAuth | Annual | `[1 year from auth]` | [ ] |
| Quo SMS API Key | 180 days | `[180 days from creation]` | [ ] |
| Anthropic API Key | 90 days | `[90 days from creation]` | [ ] |

---

## Credential Compromise Protocol

If any credential is suspected compromised (unauthorized access, accidental exposure in logs, etc.):

```
Immediate response (within 15 minutes):
1. Rotate credential immediately in the issuing service (Stripe/Google/Airtable/Slack dashboard)
2. Update the Make connection with the new credential
3. Set Automations_Paused = true in Airtable Automation_Health (halt all scenarios)
4. Post alert to #sss-emergency-ops: "CREDENTIAL ROTATION IN PROGRESS — [service name]"
5. Check audit log for any unauthorized actions during exposure window
6. Resume automations (Automations_Paused = false) only after new credential is confirmed working

Luciana: Owns the incident response coordination
Will: Owns the credential rotation in all services
```

---

## Final Pre-Activation Gate — All Credentials

Before Stage 1 scenarios are activated in sandbox mode, complete this full checklist:

```
AIRTABLE
[ ] SSS_AIRTABLE_PAT created and verified in Make
[ ] Read test: GET /Requests returns HTTP 200
[ ] Write test: Create sandbox record in Requests → confirmed
[ ] Rotation reminder set (90 days)

STRIPE
[ ] SSS_STRIPE_TEST_SECRET created and verified (sk_test_ prefix confirmed)
[ ] Test PaymentIntent created via Make → visible in Stripe test dashboard
[ ] Built-in Stripe email notifications disabled for test mode
[ ] BLK-008 resolved: webhook URL generated and registered in Stripe
[ ] SSS_STRIPE_WEBHOOK_SECRET_TEST stored in Make Data Store
[ ] Webhook signature validation module in M-STRIPE-DEPOSIT
[ ] stripe trigger payment_intent.succeeded test passed

SLACK
[ ] SSS_SLACK_BOT connection created and verified
[ ] Bot invited to #sss-ops-alerts
[ ] Bot invited to #sss-emergency-ops
[ ] Test message delivered to both channels
[ ] Block Kit templates render correctly

GMAIL SSS
[ ] SSS_GMAIL_HELLO OAuth connection verified
[ ] Test email delivered to will@shesaidsail.com
[ ] HTML renders correctly, no raw variables visible
[ ] From address confirmed: She Said Sail <hello@shesaidsail.com>

GMAIL ME
[ ] ME_GMAIL_HELLO OAuth connection verified
[ ] Test email delivered to will@shesaidsail.com
[ ] HTML renders correctly
[ ] From address confirmed: Mare Executive <hello@mareexecutive.com>

QUO SMS
[ ] SSS_QUO_SMS_API stored in Make
[ ] WILL_TEST_PHONE stored in Make Data Store
[ ] Test SMS delivered to Will's phone
[ ] Character count verified (≤160 for both templates)

ANTHROPIC (STAGED)
[ ] API key obtained and stored as SSS_ANTHROPIC_API
[ ] Confirmed: NOT connected to any Stage 1 scenario module
[ ] Billing alert set at $50/month

SIGN-OFF
[ ] Will has reviewed and confirmed all credential statuses above
[ ] Luciana has confirmed Slack channels are ready and bot is invited
[ ] Make builder has confirmed all connections are named per convention
[ ] No credentials appear in Make scenario notes, Airtable fields, or git history
```

---

*Document last updated: 2026-05-16. Update Status and Test Result columns as each credential is confirmed.*  
*Never commit this document to a public repository — it contains credential naming and scope details.*
