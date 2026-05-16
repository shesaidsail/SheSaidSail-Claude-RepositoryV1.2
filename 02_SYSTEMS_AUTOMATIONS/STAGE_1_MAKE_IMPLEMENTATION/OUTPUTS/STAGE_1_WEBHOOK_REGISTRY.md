# STAGE 1 WEBHOOK REGISTRY
**Project:** She Said Sail + Mare Executive — Make.com Automation System
**Base (Production):** appdZ49WqgjRXxA1R
**Prepared by:** Production Reliability Engineering
**Date:** 2026-05-16
**Document Status:** PRE-REGISTRATION — No webhooks registered as of this date. Make build has not yet begun.
**Stage:** Stage 1 (8 core scenarios)

---

> **Registry Purpose and Authority**
>
> This document is the authoritative record of every webhook in the Stage 1 Make.com system. It defines which webhooks exist, what they receive, who may call them, what security controls apply, and what their current registration status is. No webhook URL should be shared with any external system (Webflow, Typeform, Stripe) until it has been registered here and the security checklist in Section 3 is marked complete.
>
> "NOT REGISTERED" means the Make scenario that generates the URL has not yet been created. No URL exists. No external system should be pointed at a placeholder. When a URL is generated, this registry must be updated immediately.
>
> Cross-reference: STAGE_1_CREDENTIAL_AND_WEBHOOK_CHECKLIST.md for credential vault storage; STAGE_1_BLOCKER_RESOLUTION_REPORT.md BLK-008 for Stripe webhook blocker.

---

## SECTION 1 — WEBHOOK ARCHITECTURE OVERVIEW

### 1.1 System Webhook Map

```
EXTERNAL WORLD
─────────────────────────────────────────────────────────────────
  Webflow Form      ──POST──►  WHK-SSS-LEAD-INTAKE  ──►  M-LEAD-INTAKE
  Typeform          ──POST──►  WHK-SSS-LEAD-INTAKE  ──►  M-LEAD-INTAKE
  Direct API POST   ──POST──►  WHK-SSS-LEAD-INTAKE  ──►  M-LEAD-INTAKE

  Webflow Form      ──POST──►  WHK-ME-LEAD-INTAKE   ──►  M-LEAD-INTAKE
  Typeform (ME)     ──POST──►  WHK-ME-LEAD-INTAKE   ──►  M-LEAD-INTAKE

  Stripe (Stage 2)  ──POST──►  WHK-STRIPE-PAYMENT   ──►  M-STRIPE-DEPOSIT
                               [NOT REGISTERED — Stage 2]

MAKE INTERNAL (scenario-to-scenario)
─────────────────────────────────────────────────────────────────
  M-LEAD-INTAKE     ──HTTP──►  WHK-INTERNAL-SLACK     ──►  M-SLACK-ALERTS
  M-LEAD-INTAKE     ──HTTP──►  WHK-INTERNAL-CONCIERGE ──►  M-CONCIERGE-ASSIGNMENT
  ALL scenarios     ──HTTP──►  WHK-INTERNAL-AUDIT     ──►  M-AUDIT-LOGGER
```

### 1.2 Public-Facing vs Internal-Only Webhooks

| Category | Description | Security Requirement | Source Restriction |
|----------|-------------|---------------------|-------------------|
| Public-Facing | Accessible on the open internet; any system can POST to the URL | Bearer token required + timestamp validation required + payload schema validation | Webflow, Typeform, direct API only |
| Internal-Only | Make-to-Make calls only; not published anywhere | Make internal authentication (Make handles this natively); should not be accessible from external systems | Make scenarios only |
| Stage 2 Deferred | URL does not yet exist; must NOT be registered until the receiving scenario passes sandbox testing | All public webhook security requirements apply when eventually registered | Stripe only |

### 1.3 URL Format Convention

Make.com generates webhook URLs in the following format when a Custom Webhook trigger is created:

```
Format:   https://hook.{region}.make.com/{unique-token}
Example:  https://hook.eu1.make.com/abc123def456ghi789

Region values:
  eu1  — European accounts (EU data residency)
  us1  — US accounts (US data residency)
  (Confirm account region in Make.com → Account Settings → Region before registering any Stripe endpoint)

Token:    Unique alphanumeric string — generated once at webhook creation. Regenerating
          invalidates all existing configurations pointing to the old URL.

IMPORTANT: The URL region must be verified before sharing any URL with Stripe. Stripe requires
           the correct endpoint URL and will not retry to a different region if the URL changes.
```

### 1.4 Webhook Naming Convention

All webhooks in this system follow the naming pattern:

```
WHK-{BRAND}-{SYSTEM}-{ENVIRONMENT}

Where:
  BRAND:       SSS = She Said Sail | ME = Mare Executive | INTERNAL = internal only
  SYSTEM:      LEAD-INTAKE | STRIPE-PAYMENT | SLACK-ALERTS | CONCIERGE | AUDIT
  ENVIRONMENT: SANDBOX | PROD (omitted for internal-only webhooks)

Examples:
  WHK-SSS-LEAD-INTAKE-SANDBOX
  WHK-ME-LEAD-INTAKE-PROD
  WHK-STRIPE-PAYMENT-SANDBOX
  WHK-INTERNAL-AUDIT
```

---

## SECTION 2 — STAGE 1 WEBHOOK INVENTORY

### WHK-SSS-LEAD-INTAKE-SANDBOX

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-SSS-LEAD-INTAKE-SANDBOX |
| **Purpose** | Receives inbound She Said Sail (SSS) lead form submissions in the Sandbox environment. Entry point for the full Stage 1 pipeline during development and testing. |
| **Receiving Scenario** | M-LEAD-INTAKE (Sandbox instance) |
| **Environment** | SANDBOX |
| **Make Webhook URL** | NOT REGISTERED — URL generated when M-LEAD-INTAKE scenario is created in Make.com. Update this field immediately on creation. |
| **Authentication Type** | Bearer Token — `Authorization: Bearer {token}` HTTP header |
| **Bearer Token** | PENDING SETUP — store generated token in Make credential vault as `WHK_SSS_LEAD_INTAKE_BEARER_SANDBOX`. Never hardcode in any form or scenario. |
| **Timestamp Validation** | REQUIRED — reject if `submitted_at` field in payload is more than 5 minutes before server time. Return 401. |
| **Payload Schema Validation** | REQUIRED — validate required fields before any Airtable write: `submission_id`, `brand`, `lead.email`, `lead.first_name`, `submitted_at`. Reject malformed JSON or missing required fields. |
| **Source Systems** | Webflow SSS form; Typeform SSS survey; direct POST from Make builder during testing |
| **HTTP Method** | POST |
| **Content-Type** | application/json |
| **Registration Status** | NOT REGISTERED |
| **Registration Owner** | Make builder |
| **URL Recorded In** | [Fill in Make scenario notes field + this document + Airtable Make_Scenarios record for M-LEAD-INTAKE when created] |
| **Shared With** | Webflow team (after registration confirmed and sandbox test passed) |
| **Notes** | Sandbox only. Use test payloads only. Do not share this URL with real form users. |

---

### WHK-ME-LEAD-INTAKE-SANDBOX

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-ME-LEAD-INTAKE-SANDBOX |
| **Purpose** | Receives inbound Mare Executive (ME) lead form submissions in the Sandbox environment. |
| **Receiving Scenario** | M-LEAD-INTAKE (Sandbox instance — ME brand path) |
| **Environment** | SANDBOX |
| **Make Webhook URL** | NOT REGISTERED — generated when M-LEAD-INTAKE scenario is created. Note: M-LEAD-INTAKE may use a single webhook URL for both brands (brand determined from payload `brand` field) or separate URLs. Architecture decision ARCH-004 (bearer token approach) may affect whether one or two URLs are used. Document the approach here when decided. |
| **Authentication Type** | Bearer Token — `Authorization: Bearer {token}` HTTP header |
| **Bearer Token** | PENDING SETUP — may be same token as SSS sandbox or a separate ME token. Confirm with Will (ARCH-004 resolution). Store as `WHK_ME_LEAD_INTAKE_BEARER_SANDBOX`. |
| **Timestamp Validation** | REQUIRED — same 5-minute rule as SSS webhook |
| **Payload Schema Validation** | REQUIRED — same required fields plus ME-specific fields: `lead.company`, `lead.role` (these are expected but not required for rejection) |
| **Source Systems** | Webflow ME form; Typeform ME survey; direct POST during testing |
| **HTTP Method** | POST |
| **Content-Type** | application/json |
| **Registration Status** | NOT REGISTERED |
| **Registration Owner** | Make builder |
| **Notes** | If a single M-LEAD-INTAKE webhook handles both brands (brand field in payload routes internally), this entry describes the ME-bound submissions to the same URL. Document the final approach when the scenario is built. |

---

### WHK-SSS-LEAD-INTAKE-PROD

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-SSS-LEAD-INTAKE-PROD |
| **Purpose** | Receives inbound She Said Sail (SSS) lead form submissions in the Production environment. Processes real client inquiries. |
| **Receiving Scenario** | M-LEAD-INTAKE (Production instance) |
| **Environment** | PRODUCTION |
| **Make Webhook URL** | NOT REGISTERED — must NOT be created until sandbox testing is complete and Luciana + Will have signed the Stage 1 test results document. |
| **Authentication Type** | Bearer Token — `Authorization: Bearer {token}` HTTP header |
| **Bearer Token** | PENDING — different token from sandbox; store as `WHK_SSS_LEAD_INTAKE_BEARER_PROD`. Rotate whenever URL is rotated. |
| **Timestamp Validation** | REQUIRED — same 5-minute window |
| **Payload Schema Validation** | REQUIRED |
| **Source Systems** | Webflow SSS production form; Typeform SSS production survey |
| **HTTP Method** | POST |
| **Content-Type** | application/json |
| **Registration Status** | NOT REGISTERED |
| **Registration Prerequisite** | STAGE 1 SANDBOX SIGN-OFF REQUIRED — Luciana signature + Will approval on STAGE_1_TEST_RESULTS.md before this URL may be created or shared |
| **Registration Owner** | Make builder (with Will authorization) |
| **Shared With** | Webflow team only — via SECTION 5 handoff procedure in this document |
| **Notes** | Production webhook. All submissions trigger real Airtable records, real Slack alerts, and real concierge assignment. Do NOT share this URL with test users. |

---

### WHK-ME-LEAD-INTAKE-PROD

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-ME-LEAD-INTAKE-PROD |
| **Purpose** | Receives inbound Mare Executive (ME) lead form submissions in Production. |
| **Receiving Scenario** | M-LEAD-INTAKE (Production instance — ME brand path) |
| **Environment** | PRODUCTION |
| **Make Webhook URL** | NOT REGISTERED — same production sign-off prerequisite as WHK-SSS-LEAD-INTAKE-PROD |
| **Authentication Type** | Bearer Token |
| **Bearer Token** | PENDING — store as `WHK_ME_LEAD_INTAKE_BEARER_PROD` |
| **Timestamp Validation** | REQUIRED |
| **Payload Schema Validation** | REQUIRED |
| **Source Systems** | Webflow ME production form; Typeform ME production survey |
| **HTTP Method** | POST |
| **Content-Type** | application/json |
| **Registration Status** | NOT REGISTERED |
| **Registration Prerequisite** | STAGE 1 SANDBOX SIGN-OFF REQUIRED |
| **Registration Owner** | Make builder (with Will authorization) |
| **Notes** | See WHK-SSS-LEAD-INTAKE-PROD notes. Same restrictions apply for ME. |

---

### WHK-STRIPE-PAYMENT-SANDBOX (STAGE 2 BOUNDARY — DO NOT REGISTER IN STAGE 1)

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-STRIPE-PAYMENT-SANDBOX |
| **Purpose** | Receives Stripe payment event notifications (`payment_intent.succeeded`, `checkout.session.completed`, `payment_intent.payment_failed`, `checkout.session.expired`) in sandbox/test mode. Triggers M-STRIPE-DEPOSIT to update Airtable and advance the booking pipeline after a test payment is confirmed. |
| **Receiving Scenario** | M-STRIPE-DEPOSIT (Sandbox instance) |
| **Environment** | SANDBOX (Stripe TEST MODE only) |
| **Make Webhook URL** | NOT REGISTERED — see BLK-008. This URL is generated when M-STRIPE-DEPOSIT is created in Make.com. |
| **Authentication Type** | Stripe Webhook Signature (`Stripe-Signature` header) — HMAC-SHA256 computed from `whsec_` signing secret |
| **Stripe Signing Secret** | NOT OBTAINED — generated by Stripe when the endpoint is registered in Stripe Dashboard. Store as `SSS_STRIPE_WEBHOOK_SECRET_TEST` in Make Data Store. Never in Airtable, never in scenario notes. |
| **Timestamp Validation** | Stripe includes timestamp in the `Stripe-Signature` header (format: `t={unix_timestamp},v1={hmac}`). Validate this timestamp as part of signature verification — Stripe's standard validation rejects events older than 300 seconds (5 minutes). |
| **Stripe Events to Register** | `payment_intent.created`, `payment_intent.succeeded`, `payment_intent.payment_failed`, `checkout.session.completed`, `checkout.session.expired` |
| **Source Systems** | Stripe (test mode only) — event delivery from Stripe's infrastructure |
| **Registration Status** | NOT REGISTERED — STAGE 2 BOUNDARY |
| **STAGE 1 RESTRICTION** | **DO NOT REGISTER THIS WEBHOOK IN STAGE 1.** The URL must not be created and must not be registered in Stripe until: (1) M-STRIPE-DEPOSIT is built in Make and has passed all internal unit tests; (2) Stripe signature validation is confirmed working in Make; (3) Luciana has approved sandbox testing of the Stripe flow. Premature registration of a Stripe webhook creates a live endpoint that Stripe will deliver real events to, regardless of whether your scenario is ready. |
| **Registration Prerequisite** | M-STRIPE-DEPOSIT scenario built and internally verified; BLK-008 resolved per that document's procedure |
| **Registration Owner** | Make builder (coordinates with Will for Stripe dashboard access) |
| **Notes** | Documented here for planning purposes only. All fields marked PENDING will be completed when this webhook is registered during Stage 2 preparation. |

---

### WHK-STRIPE-PAYMENT-PROD (STAGE 2 BOUNDARY — DO NOT REGISTER IN STAGE 1)

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-STRIPE-PAYMENT-PROD |
| **Purpose** | Receives Stripe payment events in Production (LIVE mode). Triggers real booking creation and real confirmation emails after a real client payment is confirmed. |
| **Receiving Scenario** | M-STRIPE-DEPOSIT (Production instance) |
| **Environment** | PRODUCTION (Stripe LIVE MODE) |
| **Make Webhook URL** | NOT REGISTERED — Stage 2 |
| **Authentication Type** | Stripe Webhook Signature (same HMAC-SHA256 mechanism, using live signing secret `whsec_live_...`) |
| **Stripe Signing Secret** | NOT OBTAINED — separate live signing secret from the test signing secret. Store as `SSS_STRIPE_WEBHOOK_SECRET_LIVE` when obtained. |
| **Stripe Events to Register** | Same 5 event types as sandbox version |
| **Registration Status** | NOT REGISTERED — STAGE 2 BOUNDARY |
| **STAGE 1 RESTRICTION** | **NEVER register the production Stripe webhook until Stage 1 AND Stage 2 sandbox testing are both complete and signed off by Will. Registering this endpoint connects the production booking pipeline to real Stripe charges.** |
| **Registration Prerequisite** | Stage 1 sign-off + Stage 2 sandbox sign-off + Will explicit production approval |
| **Notes** | Documented for planning purposes only. Do not proceed with this registration until Will gives explicit written authorization. |

---

### WHK-INTERNAL-SLACK-ALERTS

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-INTERNAL-SLACK-ALERTS |
| **Purpose** | Internal Make-to-Make call from M-LEAD-INTAKE to M-SLACK-ALERTS. Triggers the Slack alert flow after a new Request record is created. Not a public URL. |
| **Receiving Scenario** | M-SLACK-ALERTS |
| **Environment** | Both Sandbox and Production (separate scenario instances per environment) |
| **Make Webhook URL** | NOT REGISTERED — generated when M-SLACK-ALERTS scenario is created in Make.com |
| **Authentication Type** | Make internal — scenario-to-scenario calls use Make's internal infrastructure. No external bearer token required. The URL should not be published or shared outside of Make scenario configurations. |
| **Source Systems** | M-LEAD-INTAKE only |
| **HTTP Method** | POST (Make HTTP module calling the webhook URL) |
| **Registration Status** | NOT REGISTERED |
| **Registration Owner** | Make builder |
| **Registration Sequence** | M-SLACK-ALERTS must be created FIRST (to generate this URL), before M-LEAD-INTAKE is built (M-LEAD-INTAKE needs this URL in its final step) |
| **Notes** | Not a public webhook. Do not publish this URL in Webflow, Typeform, or any external system documentation. If this URL is accidentally exposed, rotate it immediately (regenerate webhook in Make and update M-LEAD-INTAKE's HTTP module). |

---

### WHK-INTERNAL-CONCIERGE-ASSIGNMENT

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-INTERNAL-CONCIERGE-ASSIGNMENT |
| **Purpose** | Internal Make-to-Make call from M-LEAD-INTAKE to M-CONCIERGE-ASSIGNMENT. Triggers concierge lookup and assignment after a Request record is created. |
| **Receiving Scenario** | M-CONCIERGE-ASSIGNMENT |
| **Environment** | Both Sandbox and Production (separate instances) |
| **Make Webhook URL** | NOT REGISTERED — generated when M-CONCIERGE-ASSIGNMENT scenario is created in Make.com |
| **Authentication Type** | Make internal — scenario-to-scenario |
| **Source Systems** | M-LEAD-INTAKE only |
| **HTTP Method** | POST |
| **Registration Status** | NOT REGISTERED |
| **Registration Owner** | Make builder |
| **Registration Sequence** | M-CONCIERGE-ASSIGNMENT must be created before M-LEAD-INTAKE, so this URL can be configured in M-LEAD-INTAKE's flow |
| **Notes** | Internal only. Same security handling as WHK-INTERNAL-SLACK-ALERTS. |

---

### WHK-INTERNAL-AUDIT

| Field | Value |
|-------|-------|
| **Webhook ID** | WHK-INTERNAL-AUDIT |
| **Purpose** | Internal Make-to-Make call from ALL Stage 1 scenarios to M-AUDIT-LOGGER. Called as the final step of every scenario to record execution in the Audit_Log. |
| **Receiving Scenario** | M-AUDIT-LOGGER |
| **Environment** | Both Sandbox and Production (separate instances — critical to use the correct environment's audit logger URL) |
| **Make Webhook URL** | NOT REGISTERED — the FIRST URL that must be generated in the entire Stage 1 build sequence |
| **Authentication Type** | Make internal |
| **Source Systems** | M-LEAD-INTAKE, M-BRAND-ROUTER (inline), M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| **Registration Status** | NOT REGISTERED |
| **Registration Owner** | Make builder |
| **Registration Sequence** | M-AUDIT-LOGGER MUST be the first scenario created in Make.com. This URL must be distributed to all other scenario builders before any other scenario is built. Without this URL, no other scenario can configure its final audit logging step. |
| **Notes** | This is the most critical internal URL in the system. If this URL changes (webhook regenerated), ALL 8 scenarios must be updated to use the new URL. Do not regenerate this webhook without a planned maintenance window and updates to all calling scenarios. |

---

## SECTION 3 — WEBHOOK SECURITY CHECKLIST

Complete this checklist for each public-facing webhook before it is shared with any external system. Internal webhooks do not require this checklist.

### Security Checklist — WHK-SSS-LEAD-INTAKE-SANDBOX

```
PRE-REGISTRATION
[ ] M-LEAD-INTAKE Sandbox scenario exists in Make.com
[ ] Webhook created inside M-LEAD-INTAKE Sandbox scenario — URL generated
[ ] URL recorded in this document immediately on creation
[ ] URL recorded in Make scenario's description/notes field
[ ] URL recorded in Airtable Make_Scenarios record for M-LEAD-INTAKE

AUTHENTICATION
[ ] Bearer token generated (random 32+ character string — use a password manager)
[ ] Bearer token stored in Make credential vault ONLY — not in Airtable, not in this document, not in any source-controlled file
[ ] Bearer token reference name documented here: WHK_SSS_LEAD_INTAKE_BEARER_SANDBOX
[ ] Validation module in M-LEAD-INTAKE confirmed: scenario halts with 401 if token mismatch
[ ] Validation module tested: incorrect token → scenario stops, no Airtable writes

TIMESTAMP VALIDATION
[ ] Timestamp validation module present in M-LEAD-INTAKE (immediately after webhook trigger)
[ ] Rejection threshold configured: submitted_at > 5 minutes old → reject with 401
[ ] Timestamp validation tested: T-008 (stale timestamp payload) → confirmed rejection

PAYLOAD VALIDATION
[ ] Required field check module present: submission_id, brand, lead.email, lead.first_name, submitted_at
[ ] Missing field behavior tested: T-006 (email removed) → confirmed graceful rejection
[ ] Malformed JSON behavior tested: T-007 → confirmed graceful handling

URL ROTATION PROCEDURE DOCUMENTED
[ ] Rotation procedure confirmed: regenerate webhook in Make → update M-LEAD-INTAKE source URL reference → notify Webflow team → confirm Webflow form updated → test one submission
[ ] Rotation responsibility owner documented: Make builder (execution), Luciana (coordination), Will (approval)

SANDBOX ISOLATION CONFIRMED
[ ] This URL routes ONLY to Sandbox scenario instance (not Production)
[ ] Sandbox scenario writes to Sandbox Airtable base only (not appdZ49WqgjRXxA1R)
[ ] Environment field on all created records = sandbox (not production)
```

### Security Checklist — WHK-ME-LEAD-INTAKE-SANDBOX

```
[ ] Same checklist as WHK-SSS-LEAD-INTAKE-SANDBOX, applied to ME brand scenario instance
[ ] Bearer token stored as: WHK_ME_LEAD_INTAKE_BEARER_SANDBOX
[ ] ME brand routing confirmed: payload with brand = ME routes to ME pipeline
[ ] ME brand records confirmed: Environment = sandbox; Brand = ME on created records
```

### Security Checklist — WHK-SSS-LEAD-INTAKE-PROD (complete after sandbox sign-off)

```
PRE-REGISTRATION GATE — ALL MUST BE TRUE BEFORE URL IS CREATED
[ ] Stage 1 Test Results document signed by Luciana
[ ] Stage 1 Test Results approved by Will
[ ] T-001 (SSS full pipeline): PASS
[ ] T-005 (duplicate rejection): PASS
[ ] T-006 (missing field): PASS
[ ] T-007 (malformed JSON): PASS
[ ] T-008 (replay rejection): PASS
[ ] T-009 (failure chain): PASS

AFTER CREATION
[ ] URL generated and recorded in this document
[ ] Production bearer token generated — different from sandbox token
[ ] Production bearer token stored as: WHK_SSS_LEAD_INTAKE_BEARER_PROD
[ ] Production scenario confirmed to write to production base (appdZ49WqgjRXxA1R), NOT sandbox base
[ ] Production Environment field default set to: production
[ ] BLK-009 resolved: all Airtable native automations inventoried and deactivated where required
[ ] URL shared with Webflow team per Section 5 handoff procedure ONLY
```

### Security Checklist — Stripe Webhooks (complete during Stage 2 preparation)

```
NOTE: These items are documented here for future reference.
      No action required during Stage 1.

[ ] BLK-008 resolved: M-STRIPE-DEPOSIT sandbox scenario skeleton created
[ ] WHK-STRIPE-PAYMENT-SANDBOX URL generated in Make
[ ] URL registered in Stripe Test Mode Dashboard → Developers → Webhooks
[ ] All 5 Stripe event types selected in endpoint registration
[ ] Stripe signing secret (whsec_...) stored in Make Data Store as SSS_STRIPE_WEBHOOK_SECRET_TEST
[ ] Stripe signature validation module confirmed working in M-STRIPE-DEPOSIT (Step 1)
[ ] Test event delivered: stripe trigger payment_intent.succeeded
[ ] Stripe dashboard confirms event as "Delivered" (HTTP 200 response from Make)
[ ] Negative test: tampered signature → Make returns 400 → Stripe shows delivery failure
[ ] Stripe test email notifications DISABLED in Stripe Dashboard → Settings → Emails
[ ] livemode field verified = false on all test Stripe objects

PRODUCTION STRIPE WEBHOOK (Stage 2 gate — requires Will authorization)
[ ] Stage 2 sandbox testing complete and signed off
[ ] Will has explicitly authorized production Stripe webhook registration in writing
[ ] Production URL registered in Stripe Live Mode (not Test Mode)
[ ] Live signing secret stored as SSS_STRIPE_WEBHOOK_SECRET_LIVE
[ ] First live payment event delivered and confirmed before go-live announcement
```

---

## SECTION 4 — WEBHOOK REGISTRATION SEQUENCE

The following sequence is mandatory. Deviating from this order creates build dependencies that cannot be resolved cleanly.

### Phase 1 — Internal Webhooks First (Make Build Order)

```
STEP 1: Create M-AUDIT-LOGGER scenario in Make.com
  → Generates: WHK-INTERNAL-AUDIT (Sandbox)
  → Action: Record URL immediately. Distribute to all scenario builders.
  → Gate: M-AUDIT-LOGGER must pass its own unit tests before step 2 proceeds.

STEP 2: Create M-SLACK-ALERTS scenario in Make.com
  → Generates: WHK-INTERNAL-SLACK-ALERTS (Sandbox)
  → Action: Record URL. Configure in M-LEAD-INTAKE when that scenario is built.

STEP 3: Create M-CONCIERGE-ASSIGNMENT scenario in Make.com
  → Generates: WHK-INTERNAL-CONCIERGE-ASSIGNMENT (Sandbox)
  → Action: Record URL. Configure in M-LEAD-INTAKE when that scenario is built.

STEP 4: Create M-STRIPE-DEPOSIT scenario skeleton in Make.com
  → Generates: WHK-STRIPE-PAYMENT-SANDBOX URL (resolves BLK-008)
  → Action: Register in Stripe Test Mode Dashboard. Obtain signing secret. Store as
            SSS_STRIPE_WEBHOOK_SECRET_TEST. Do NOT activate full scenario until
            Stripe integration is ready to test.
```

### Phase 2 — Public Lead Intake Webhooks

```
STEP 5: Create M-LEAD-INTAKE scenario in Make.com (Sandbox instance)
  → Generates: WHK-SSS-LEAD-INTAKE-SANDBOX URL
  → Also generates: WHK-ME-LEAD-INTAKE-SANDBOX URL (if separate, or confirms brand routing
                    from single URL if using shared endpoint)
  → Action: Configure internal calls to WHK-INTERNAL-SLACK-ALERTS and
            WHK-INTERNAL-CONCIERGE-ASSIGNMENT (URLs from Steps 2 and 3).
  → Action: Configure final step to call WHK-INTERNAL-AUDIT (URL from Step 1).
  → Do NOT share URLs externally until sandbox testing is complete.

STEP 6: Run sandbox test T-001 (SSS full pipeline)
  → Gate: T-001 must PASS before proceeding to step 7.

STEP 7: Run all remaining sandbox tests T-002 through T-013
  → Gate: All 13 tests must PASS. Luciana signs test results.
```

### Phase 3 — Production Webhooks (After Sandbox Sign-Off)

```
STEP 8: Will reviews and approves STAGE_1_TEST_RESULTS.md
  → Gate: Will signature required before any production URL is created.

STEP 9: Create M-LEAD-INTAKE Production scenario in Make.com
  → Generates: WHK-SSS-LEAD-INTAKE-PROD URL
  → Generates: WHK-ME-LEAD-INTAKE-PROD URL
  → Action: Configure production URLs in Webflow and Typeform forms per Section 5.
  → Gate: Must use production bearer tokens (not sandbox tokens).

STEP 10: Document all production URLs in this registry.
  → Verify production scenarios point to production Airtable base (appdZ49WqgjRXxA1R),
    NOT the sandbox base.
```

### Phase 4 — NEVER DO (Stage 1 Restrictions)

```
NEVER: Register WHK-STRIPE-PAYMENT-PROD until Stage 2 sandbox testing is signed off.
NEVER: Share a production webhook URL with any external system before Will has signed off.
NEVER: Reuse a sandbox webhook URL for production (they are different scenario instances).
NEVER: Regenerate a Make webhook URL without updating all systems that reference it.
NEVER: Store a webhook URL in Airtable as a field value (URL must live in Make only).
NEVER: Share any internal webhook URL with any system outside of Make.com.
```

---

## SECTION 5 — WEBHOOK URL HANDOFF TO WEBSITE AND FORM TEAMS

When production webhook URLs are ready (after Stage 1 sandbox sign-off), this section defines what must be delivered to the team managing Webflow and Typeform.

### Handoff Package Contents

The Make builder delivers the following to Luciana (who coordinates with the website team). Luciana does not share the package with anyone who does not need the URL for system configuration.

**Deliver to website/form team:**

```
1. Webhook URL
   Format: https://hook.{region}.make.com/{unique-token}
   Environment: Production only (never share sandbox URL with website team)
   One URL per brand (SSS and ME) unless single-endpoint approach is confirmed

2. Authentication header required
   Header name:  Authorization
   Header value: Bearer {token}
   [Token delivered separately and securely — not in the same message as the URL]

3. Required payload format
   All form submissions must POST valid JSON with these required fields:
   {
     "submission_id": "[unique ID from form — required for idempotency]",
     "submitted_at":  "[ISO 8601 UTC timestamp — e.g., 2026-07-15T22:00:00Z]",
     "form_name":     "[form identifier string]",
     "brand":         "[SSS or ME — must match the exact string]",
     "lead": {
       "first_name":  "[string — required]",
       "last_name":   "[string — required]",
       "email":       "[valid email address — required]",
       "phone":       "[E.164 format recommended — e.g., +13055550100]",
       "preferred_contact": "[email or phone]"
     },
     "inquiry": {
       "charter_type": "[string — required]",
       "preferred_date": "[YYYY-MM-DD format]",
       "group_size":   "[integer]",
       "notes":        "[string]"
     },
     "metadata": {
       "source":     "[Webflow or Typeform]",
       "ip_address": "[optional — client IP if available]"
     }
   }

4. Validation rules website team must respect
   - submission_id must be unique per form submission (use a UUID or Webflow's built-in submission ID)
   - submitted_at must be the actual submission timestamp in UTC (not a placeholder)
   - Submissions with submitted_at older than 5 minutes will be rejected with 401
   - brand field must be exactly "SSS" or "ME" (case-sensitive, no spaces)
   - email field is required — submissions without email will be rejected

5. HTTP response behavior the website team should expect
   - 200 OK: submission received and processing started
   - 401 Unauthorized: invalid bearer token or stale timestamp — check credentials and time
   - 400 Bad Request: malformed JSON or missing required field — check payload format
   - 5xx: Make infrastructure error — retry after 60 seconds; alert Luciana if persistent
```

### Website Team Test Procedure

Before connecting the production form to the production webhook URL, the website team must run one test using the sandbox URL:

```
Sandbox test procedure for website/form team:
1. Configure the form to POST to WHK-SSS-LEAD-INTAKE-SANDBOX (sandbox URL)
2. Submit one test entry through the live Webflow/Typeform form interface
3. Confirm Luciana receives a Slack alert in #sss-ops-alerts within 60 seconds
4. Luciana confirms a test record appeared in the Sandbox Airtable base
5. If confirmed: switch form configuration to the production URL
6. If not confirmed: send the exact JSON payload Webflow/Typeform is generating to Luciana for debugging

Note: "Test entry" means using fake data — not a real client's information.
      Suggest: First Name = "WebflowTest", Last Name = "FormTest", Email = "ops-test+webflow@shesaidsail.com"
```

### Webflow Form Configuration Steps

```
In Webflow: Site Settings → Forms → Form Submissions → Webhook
  1. Enable "Send to Webhook" or use Webflow's native webhook settings
  2. Paste the production SSS webhook URL in the endpoint field
  3. Add the Authorization header: Bearer {token} (stored securely — not in Webflow form visible fields)
  4. Select JSON as the body format
  5. Map each Webflow field to the correct JSON key per the payload schema above
  6. Save and test with one sandbox submission before going live

Note: Webflow generates its own submission_id for each form entry. Confirm whether to use
      Webflow's submission ID or generate a custom one. Document the approach in the field
      mapping spec for M-LEAD-INTAKE.
```

### Typeform Configuration Steps

```
In Typeform: Connect → Webhooks → Add a Webhook
  1. Paste the webhook URL (SSS or ME depending on form)
  2. Add Authorization header in the webhook configuration
  3. Map Typeform "reference" keys (not display labels) to the required JSON fields
  4. Enable and test with a form submission

IMPORTANT: Typeform's native webhook payload uses reference keys, not display labels.
           The reference key for "Email Address" may be "email_address" or a custom ID.
           Luciana must confirm Typeform reference keys and provide the mapping before
           M-LEAD-INTAKE is built. See Open Issue LI-004 in STAGE_1_OPEN_ISSUES.md.
```

---

## SECTION 6 — WEBHOOK STATUS DASHBOARD

Current registration status for all Stage 1 webhooks. Update this table whenever a URL is registered or status changes.

| Webhook ID | Scenario | Environment | URL Status | Security Checklist | Last Updated |
|------------|----------|-------------|------------|-------------------|--------------|
| WHK-SSS-LEAD-INTAKE-SANDBOX | M-LEAD-INTAKE | Sandbox | NOT REGISTERED | Incomplete | 2026-05-16 |
| WHK-ME-LEAD-INTAKE-SANDBOX | M-LEAD-INTAKE | Sandbox | NOT REGISTERED | Incomplete | 2026-05-16 |
| WHK-SSS-LEAD-INTAKE-PROD | M-LEAD-INTAKE | Production | NOT REGISTERED | Incomplete — requires sandbox sign-off first | 2026-05-16 |
| WHK-ME-LEAD-INTAKE-PROD | M-LEAD-INTAKE | Production | NOT REGISTERED | Incomplete — requires sandbox sign-off first | 2026-05-16 |
| WHK-STRIPE-PAYMENT-SANDBOX | M-STRIPE-DEPOSIT | Sandbox | NOT REGISTERED — Stage 2 scope | Incomplete | 2026-05-16 |
| WHK-STRIPE-PAYMENT-PROD | M-STRIPE-DEPOSIT | Production | NOT REGISTERED — Stage 2 scope | Incomplete | 2026-05-16 |
| WHK-INTERNAL-SLACK-ALERTS | M-SLACK-ALERTS | Internal | NOT REGISTERED | N/A (internal) | 2026-05-16 |
| WHK-INTERNAL-CONCIERGE-ASSIGNMENT | M-CONCIERGE-ASSIGNMENT | Internal | NOT REGISTERED | N/A (internal) | 2026-05-16 |
| WHK-INTERNAL-AUDIT | M-AUDIT-LOGGER | Internal | NOT REGISTERED | N/A (internal) | 2026-05-16 |

---

## SECTION 7 — WEBHOOK URL LOG

When a URL is generated, record it here. The URL itself should also be stored in Make scenario notes. This log provides a central reference without needing to open each Make scenario.

```
IMPORTANT: This document may be stored in a git repository.
           Do NOT record bearer tokens or signing secrets in this log.
           Record URLs only. Credentials live in Make's credential vault.
```

| Webhook ID | URL | Generated Date | Generated By | Notes |
|------------|-----|----------------|--------------|-------|
| WHK-SSS-LEAD-INTAKE-SANDBOX | [PENDING] | | | |
| WHK-ME-LEAD-INTAKE-SANDBOX | [PENDING] | | | |
| WHK-SSS-LEAD-INTAKE-PROD | [PENDING] | | | Requires sandbox sign-off |
| WHK-ME-LEAD-INTAKE-PROD | [PENDING] | | | Requires sandbox sign-off |
| WHK-STRIPE-PAYMENT-SANDBOX | [PENDING — Stage 2] | | | |
| WHK-STRIPE-PAYMENT-PROD | [PENDING — Stage 2] | | | |
| WHK-INTERNAL-SLACK-ALERTS | [PENDING] | | | Internal only |
| WHK-INTERNAL-CONCIERGE-ASSIGNMENT | [PENDING] | | | Internal only |
| WHK-INTERNAL-AUDIT | [PENDING] | | | Internal only — distribute to all builders |

---

*Document last updated: 2026-05-16. All webhooks are NOT REGISTERED as of this date — Make build has not yet begun.*
*Authority: MAKE_MASTER_ARCHITECTURE.md Section 5 (Webhook Security Model); STAGE_1_CREDENTIAL_AND_WEBHOOK_CHECKLIST.md.*
*Registration Owner: Make builder. Registration Approver: Will (for production URLs). Registry Maintainer: Luciana.*
