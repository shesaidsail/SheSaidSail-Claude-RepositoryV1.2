# STAGE 1 OPEN ISSUES REGISTER
**Project:** She Said Sail + Mare Executive — Make.com Automation System
**Base (Production):** appdZ49WqgjRXxA1R
**Prepared by:** Production Reliability Engineering
**Date:** 2026-05-16
**Document Status:** ACTIVE — update Status column as issues are resolved
**Stage:** Stage 1 (8 core scenarios: M-BRAND-ROUTER through M-AUDIT-LOGGER)

---

> **Register Purpose**
>
> This document is the single consolidated register of every open issue, blocker, and pending decision across all Stage 1 documentation. It is organized by severity and category. The Make build phase must not begin until Section 1 (Critical Blockers) is fully resolved. Sandbox testing must not begin until Section 2 (High Priority Issues) is resolved. Issues in Sections 3–5 must be tracked throughout the build and testing phases.
>
> Issue owners are responsible for updating this register. Luciana owns the register and must confirm Section 1 and Section 2 are cleared before authorizing the Make builder to begin. Will must sign off on all architecture decisions in Section 4.

---

## SECTION 1 — CRITICAL BLOCKERS
**Must resolve before Make build begins. No scenario construction may start until these are cleared.**

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| BLK-001 | `Environment` field missing from most Airtable tables (Requests, Bookings, Clients, Audit_Log, Concierge_Assignments, Packages). Without this field, test records cannot be separated from production records — any test run during Stage 1 permanently contaminates live data. Must add `Environment` (Single Select: production / sandbox / test) to all tables before any Make scenario creates records. | CRITICAL | Will | ALL scenarios | OPEN |
| BLK-002 | `Idempotency_Key` field missing from the Bookings table. M-BOOKING-CREATION requires this field to detect and prevent duplicate booking records on retries or webhook replays. Without it, a single deposit payment can produce multiple booking records, duplicate emails, and duplicate Stripe charges. | CRITICAL | Will | M-BOOKING-CREATION, M-LEAD-INTAKE | OPEN |
| BLK-003 | `Automations_Paused` field in Automation_Health control record not verified. Every scenario requires a read-first kill switch check as Step 1. The Automation_Health table and its control record may not exist. If this is missing, there is no emergency stop mechanism — a runaway scenario cannot be halted from Airtable. Operations team would have no recourse other than accessing Make.com directly during an incident. | CRITICAL | Luciana | ALL scenarios (client-facing) | OPEN |
| BLK-007 | Circular trigger risk on the Bookings table not yet resolved. M-BOOKING-CREATION writes back to the Bookings table after creation (updating Status, Environment, Last_Modified_By). This write re-triggers the "record updated" webhook, creating an infinite execution loop. Left unresolved, this will exhaust the Make operations quota and may result in account suspension. A trigger guard field (`Needs_Make_Processing`, `Make_Processing`) and a field-scoped watch trigger must be designed and implemented before M-BOOKING-CREATION is built. | CRITICAL | Make builder | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION | OPEN |
| BLK-008 | Stripe webhook endpoint URL does not yet exist. The Make webhook URL for M-STRIPE-DEPOSIT can only be generated after the scenario skeleton is created in Make.com. Without this URL, Stripe cannot be configured to send payment events, and M-STRIPE-DEPOSIT cannot receive `payment_intent.succeeded` events. This is a sequential dependency: create the scenario first, then get the URL, then configure Stripe. The Stripe signing secret also cannot be obtained until the webhook endpoint is registered. | BLOCKER | Make builder | M-STRIPE-DEPOSIT | OPEN |
| BLK-009 | Airtable-native automations inventory is incomplete. Airtable supports automations built inside Airtable (separate from Make). Before Make writes to Bookings or Requests tables, every active native automation on those tables must be catalogued. An undocumented native automation could: fire in response to Make's test write and send a real client email, overwrite fields Make just set, or create a circular trigger condition. Luciana must document every native automation and deactivate all that touch fields Make also writes or that send external communications. | CRITICAL | Luciana | M-BOOKING-CREATION, M-LEAD-INTAKE | OPEN |

**Resolution sequence (must follow this order):**
```
1. BLK-003 → Verify/create Automations_Paused before any Make scenario fires
2. BLK-001 → Add Environment field to all tables before any record is created
3. BLK-009 → Complete native automations inventory before writing to Bookings or Requests
4. BLK-007 → Design and implement circular trigger guard before M-BOOKING-CREATION is built
5. BLK-002 → Add Idempotency_Key field before M-BOOKING-CREATION build begins
6. BLK-008 → Generate Stripe webhook URL when M-STRIPE-DEPOSIT skeleton is created in Make
```

**Escalation rule:** Any CRITICAL/BLOCKER item unresolved after 48 hours of assignment escalates to Will via Slack DM. At 72 hours unresolved, the Stage 1 build is paused for the affected scenarios until the blocker is cleared.

---

## SECTION 2 — HIGH PRIORITY ISSUES
**Resolve before sandbox testing begins. These do not block Make build start but block testing.**

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| BLK-004 | `AI_Prompt_Versions` table has wrong schema — only 9 fields exist, but the architecture requires 26 fields. M-BRAND-ROUTER reads this table to retrieve the active brand routing prompt. Reading from a 9-field table returns null/empty for 17 missing fields, silently breaking brand routing. Missing fields include: `Prompt_Body`, `Is_Active`, `Brand`, `Model`, `Max_Tokens`, `Temperature`, `Version_Number`, `Activated_At`, `Deprecated_At`. Should be fixed now to avoid a schema retrofit during Stage 2. | HIGH | Will | M-BRAND-ROUTER (Stage 2 Claude API calls) | OPEN |
| BLK-005 | `D7_Review_Eligible` formula field missing from Bookings table. This computed field determines whether a booking is 7+ days past charter date and eligible for automated review/follow-up. Not blocking Stage 1 execution, but Stage 2 scenarios are being designed with this field in mind. Adding it during Stage 2 build after Stage 2 specs are finalized will require reopening and modifying all Stage 2 scenarios. Add it now while Bookings schema changes are already in progress (BLK-001, BLK-002). | HIGH | Will | Stage 2 architecture (review workflows) | OPEN |
| BLK-006 | `Make_Scenarios` reference table is in a non-production Airtable base. M-AUDIT-LOGGER reads from this table to enrich audit log entries with scenario context (name, version, status). Maintaining a cross-base dependency on a non-production asset creates a fragile link. If the non-production base is reorganized or access is revoked, M-AUDIT-LOGGER fails silently. The table and its 8 Stage 1 scenario records must be migrated to base `appdZ49WqgjRXxA1R` before M-AUDIT-LOGGER sandbox testing. | MEDIUM | Luciana | M-AUDIT-LOGGER | OPEN |

---

## SECTION 3 — SCENARIO-SPECIFIC OPEN ISSUES

Issues are identified by their source scenario. Each issue is tracked with severity, owner, and dependency on specific tests or blockers.

---

### 3.1 M-BRAND-ROUTER Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| BR-001 | **Tie-breaking rule when SSS and ME keyword scores are equal.** Current default behavior: route to SSS. This business rule has not been explicitly confirmed with Will. If the correct default is ME (or if the call should be flagged as AMBIGUOUS for manual review), the routing logic must be changed before build. | HIGH | Will | M-BRAND-ROUTER build | OPEN |
| BR-002 | **`brand_hint` field reliability.** The routing logic relies on a `brand_hint` field in the inbound payload. Confirm that all intake sources (Webflow form, Typeform, Instagram DM middleware) consistently populate this field. If any source omits it, keyword scoring becomes the sole classifier, increasing misrouting risk. | HIGH | Luciana | M-BRAND-ROUTER build | OPEN |
| BR-003 | **Occasion field exhaustive mapping.** Brand routing uses the `occasion` field as an override signal (e.g., "Corporate Retreat" → ME; "Birthday" → SSS). The current occasion-to-brand mapping may not cover all values that Typeform generates. Luciana must provide the complete list of possible occasion values to confirm the mapping is exhaustive. | MEDIUM | Luciana | M-BRAND-ROUTER accuracy | OPEN |
| BR-004 | **Slack interactive button endpoint.** The new lead Slack alert includes "Classify as SSS" and "Classify as ME" buttons for manual override. These buttons require a separate Make webhook to receive Slack's button-click callbacks (Slack Action URL). It is not confirmed whether this endpoint will be built in Stage 1 or deferred to Stage 2. If deferred, the buttons must be visually disabled or removed from the alert template to prevent user confusion. | MEDIUM | Will | M-SLACK-ALERTS, Stage 2 scope | OPEN |
| BR-005 | **Multi-brand inquiry edge case.** A client may genuinely inquire about both SSS and ME in a single submission. The current scoring logic will classify SSS if SSS keyword count ≥ ME count. No business rule exists for this scenario. Will must decide: route to SSS default, route to ME default, flag as AMBIGUOUS and require manual review, or split into two Request records. | MEDIUM | Will | M-BRAND-ROUTER routing logic | OPEN |
| BR-006 | **URL-based brand detection not implemented.** If the form submission includes a `page_url` or `referring_url` field indicating whether the user was on `shesaidsail.com` vs `mareexecutive.com`, this is a highly reliable brand signal. URL-based detection is not yet in the routing logic. Assess whether Webflow/Typeform passes this field and whether it should be added as a high-confidence override signal. | LOW | Systems | M-BRAND-ROUTER enhancement | OPEN |

---

### 3.2 M-LEAD-INTAKE Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| LI-001 | **Emergency_Flag and Automations_Paused storage location.** The scenario spec references reading `Emergency_Flag` and `Automations_Paused` from Airtable. It is not confirmed whether these live in an `Automation_Health` table, a `System_Config` table, or Make Data Stores. Must be resolved as part of BLK-003 resolution. | CRITICAL | Systems / Luciana | M-LEAD-INTAKE Step 1 (kill switch) | OPEN |
| LI-002 | **Bearer token authentication approach.** Two approaches are possible: (A) Include API key in the JSON payload body, validated by a Make filter module; (B) Use Make's built-in webhook authentication (HTTP Basic or header-based). Approach B is architecturally cleaner but requires verifying Make's webhook module supports the chosen method. Will must select the approach before the webhook is registered, as the URL changes between approaches. | HIGH | Will | WHK-SSS-LEAD-INTAKE security model | OPEN |
| LI-003 | **Airtable table ID for Automation_Health.** The scenario references the Automation_Health table by name but the Airtable internal table ID (tbl...) has not been confirmed. Make.com modules require the table ID, not the name. Confirm the table ID before building any module that reads from Automation_Health. | HIGH | Luciana | M-LEAD-INTAKE Step 1 | OPEN |
| LI-004 | **Typeform payload field names.** The field mapping table in the scenario spec assumes specific Typeform field names (e.g., `first_name`, `charter_type`). Typeform's actual payload uses reference keys that may differ from display labels. Luciana must confirm the exact Typeform field reference keys before the mapping module is built. | HIGH | Luciana | M-LEAD-INTAKE field mapping | OPEN |
| LI-005 | **Instagram DM routing middleware.** If leads arrive via Instagram DM, a middleware system (ManyChat, Zapier, or a custom bridge) converts the DM into a webhook POST. The payload format from this middleware is unknown. Confirm the middleware in use and its output payload format before the webhook parser is built. | HIGH | Luciana | M-LEAD-INTAKE multi-source parsing | OPEN |
| LI-006 | **Request_ID_Display format.** Current spec formats the human-readable request ID as `REQ-YYYYMMDD-[6-char suffix]`. Will must confirm this format is correct for operational use, or provide the preferred alternative format. | MEDIUM | Will | M-LEAD-INTAKE record creation | OPEN |
| LI-007 | **Charter_Date field type in Airtable.** Make's `parseDate()` behavior differs depending on whether the Airtable field is a Date (no time) or DateTime field. Confirm the field type in the live Requests table schema before writing the date parsing module. | MEDIUM | Systems | M-LEAD-INTAKE date handling | OPEN |
| LI-008 | **Budget field — string or numeric.** The `budget_range` from the intake form is a free-text string (e.g., "$2,500 - $5,000"). Will must confirm whether to store it as-is (string) or parse it into numeric min/max fields for filtering and reporting. Parsing adds complexity; storing as string is simpler but limits automated budget qualification. | MEDIUM | Will | M-LEAD-INTAKE field mapping | OPEN |
| LI-009 | **Live Airtable field name confirmation.** All field names in the M-LEAD-INTAKE mapping table must be verified against the live Requests table schema (`tblTlSB9CO4dTGodg` in base `appdZ49WqgjRXxA1R`) before the scenario is built. Field name mismatches cause silent write failures in Make — the module succeeds but the data is discarded. Run `get_table_schema(appdZ49WqgjRXxA1R, tblTlSB9CO4dTGodg)` and cross-reference every mapped field before build. | CRITICAL | Systems | M-LEAD-INTAKE all write modules | OPEN |

---

### 3.3 M-SLACK-ALERTS Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| SA-001 | **Slack interactive button endpoint — Stage 1 or Stage 2?** The "Assign Concierge" and "Mark Hot Lead" buttons in lead alert messages require a Slack Action URL endpoint (a separate Make webhook) to handle button-click callbacks. If this is not built in Stage 1, the buttons must be removed from the alert template or visually disabled. An unhandled button click produces a Slack error message visible to the user. Will must decide: build the endpoint in Stage 1, or remove the buttons for now. | HIGH | Will | M-SLACK-ALERTS template design | OPEN |
| SA-002 | **Slack app credentials not yet created.** The `SSS_SLACK_BOT` Make connection requires a Bot User OAuth Token from a Slack app installation. The Slack app ("She Said Sail Bot") has not been created. Required scopes: `chat:write`, `im:write`, `channels:read`, `users:read`. Luciana must create the app, install it to the workspace, and provide the bot token to the Make builder. The bot must also be manually invited to #sss-ops-alerts and #sss-emergency-ops before any M-SLACK-ALERTS test can run. | CRITICAL | Luciana | M-SLACK-ALERTS credential setup | OPEN |
| SA-003 | **Slack Member IDs for Luciana and Will not confirmed.** Slack DMs (Level 4 escalation alerts) require the recipient's Slack Member ID (format: `U01XXXXXXX`), not their display name or email. Luciana must retrieve both Member IDs from Slack (Profile → More → Copy member ID) and store them in Make Data Store before the Level 4 alert path is tested. | HIGH | Luciana | T-009, T-013 (Level 4 DM) | OPEN |
| SA-004 | **Airtable record deep-link URL format not verified.** Slack alerts include a deep link to the Airtable record for quick review. The assumed URL format is `https://airtable.com/appdZ49WqgjRXxA1R/tblTlSB9CO4dTGodg/[RECORD_ID]`. This format must be tested manually in a browser to confirm it resolves to the correct record view before it is embedded in production alerts. | MEDIUM | Systems | M-SLACK-ALERTS link validity | OPEN |
| SA-005 | **Timezone for Slack message timestamps.** The `submitted_at` value is stored as UTC. Slack messages should display the timestamp in the team's working timezone (ET or PT). The `formatDate()` function in the alert template must be configured with the correct timezone offset. Luciana must confirm the preferred display timezone. | MEDIUM | Luciana | M-SLACK-ALERTS display formatting | OPEN |
| SA-006 | **ME brand Slack channel routing.** The current spec routes both SSS and ME lead alerts to #sss-ops-alerts with a brand label in the message. It is not confirmed whether ME should have its own dedicated channel (e.g., #me-ops-alerts). A separate channel improves signal clarity but requires Luciana to monitor two channels. Will must decide the channel strategy. | MEDIUM | Will | M-SLACK-ALERTS routing logic | OPEN |
| SA-007 | **Test alert visual distinction.** During sandbox testing, M-SLACK-ALERTS will fire into #sss-ops-alerts (or sandbox equivalent). The current proposal is to prepend `[TEST]` to all message text when the `environment` field in the calling payload = `sandbox`. Luciana must confirm this approach, or specify whether a dedicated #sss-ops-alerts-sandbox channel should be used instead, to prevent test noise in the production ops channel during sandbox runs. | MEDIUM | Luciana | Sandbox testing procedure | OPEN |
| SA-008 | **Audit_Log table field names must be verified.** M-SLACK-ALERTS writes its own Audit_Log entry. All field names used in the Airtable write module must be verified against the live Audit_Log table schema (`tblrMpTfMk8q1eNHp`) before build. A field name mismatch causes silent data loss — Make writes succeed but data is not stored. | HIGH | Systems | M-SLACK-ALERTS audit write | OPEN |

---

### 3.4 M-CONCIERGE-ASSIGNMENT Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| CA-001 | **Concierge_Operators table is empty at build time.** If the table has no active concierge records, M-CONCIERGE-ASSIGNMENT will follow Route B (NEEDS_MANUAL_ASSIGNMENT) for every request, creating full manual overhead for Luciana. At minimum one active SSS concierge and one active ME concierge must be entered before the first live request. Confirm with Luciana that population will occur before Stage 1 go-live. | HIGH | Luciana | M-CONCIERGE-ASSIGNMENT routing | OPEN |
| CA-002 | **`Cities` field type ambiguity in Concierge_Operators.** The assignment logic filters concierges by city match using a FIND() formula. If `Cities` is a Multi-Select field in Airtable, the formula requires `ARRAYJOIN()`. If it is plain text, FIND() works directly. The wrong formula returns 0 results for all concierge queries. Confirm the field type in the live Concierge_Operators table schema before writing the filter formula. | HIGH | Systems | M-CONCIERGE-ASSIGNMENT Module 4 | OPEN |
| CA-003 | **Non-atomic `Current_Load` increment.** When multiple requests arrive for the same concierge simultaneously (>1 concurrent), Make reads the current `Current_Load` value, increments it, and writes it back. Under concurrency, two simultaneous reads can return the same stale value, resulting in the load counter being undercounted. Stage 1 volume (1–5 requests/day) makes this acceptable, but the issue must be documented and a remedy (Processing_Lock field or Airtable-native atomic increment) must be designed before Stage 2 volume scales. | MEDIUM | Systems | M-CONCIERGE-ASSIGNMENT at scale | OPEN |
| CA-004 | **Manual M-STRIPE-DEPOSIT re-trigger after Route B assignment.** When a request follows Route B (manual assignment by Luciana), there is no automated mechanism to trigger M-STRIPE-DEPOSIT after Luciana completes the assignment. Luciana must trigger it manually in Make. This is an operational gap that should be closed in Stage 2 via an Airtable Watch trigger on `Agent_Status` field change. Document this gap clearly in the Make builder's handoff notes. | MEDIUM | Systems / Luciana | M-STRIPE-DEPOSIT trigger gap | OPEN |
| CA-005 | **Concierge_Operators table migration must be verified.** The Concierge_Operators table was migrated from base `app2FbmVD44BXShyx` to base `appdZ49WqgjRXxA1R`. The migration must be confirmed as complete: all records intact, all field types preserved (especially Single Select and Multi-Select fields), and Make connection updated to reference the new base. Will and Luciana must sign off on migration completeness before M-CONCIERGE-ASSIGNMENT build begins. | HIGH | Will / Luciana | M-CONCIERGE-ASSIGNMENT data integrity | OPEN |

---

### 3.5 M-STRIPE-DEPOSIT Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| SD-001 | **Stripe webhook URL not yet registered — see BLK-008.** This is the same issue as BLK-008 above, repeated here for completeness. The Make webhook URL for M-STRIPE-DEPOSIT cannot be generated until the scenario skeleton is created in Make.com. Until the URL exists, Stripe cannot be configured, and the Stripe signing secret cannot be obtained. This is the single most critical sequential dependency in Stage 1. | BLOCKER | Make builder | M-STRIPE-DEPOSIT end-to-end flow | OPEN |
| SD-002 | **Packages table existence unconfirmed.** The deposit amount calculation reads from a `Packages` table in base `appdZ49WqgjRXxA1R`. It is not confirmed whether this table exists and is populated. If the table does not exist or has no records, every deposit falls back to the default amount ($750 placeholder — see SD-005). The Make builder must verify the Packages table exists and contains at least one record before the pricing module is built. | HIGH | Will / Luciana | M-STRIPE-DEPOSIT pricing logic | OPEN |
| SD-003 | **Success and cancel URL configuration for Stripe Checkout.** M-STRIPE-DEPOSIT creates a Stripe Checkout Session with `success_url` and `cancel_url` parameters. These URLs must be configured in Stripe before the session can be created. The actual page URLs (e.g., `https://shesaidsail.com/booking/success`) must be confirmed with Will and set in the Make scenario before any Checkout Session test. | HIGH | Will | M-STRIPE-DEPOSIT Checkout config | OPEN |
| SD-004 | **Stripe test key rotation policy at go-live.** The `SSS_STRIPE_TEST_SECRET` connection in Make uses a `sk_test_` key. At production go-live, this must be replaced with the live `sk_live_` key. A documented rotation procedure must exist before Stage 1 sandbox testing begins, so the go-live key swap can be executed without rebuilding or reconfiguring any module. The process: update the Make connection only — scenario modules do not change. Document this in the go-live checklist. | MEDIUM | Will | Production go-live transition | OPEN |
| SD-005 | **Default deposit amount of $750 is a placeholder.** When no Package price can be retrieved (Packages table empty, Package not linked, or price field null), M-STRIPE-DEPOSIT falls back to a hardcoded $750 deposit. This placeholder value has not been confirmed as a valid business rule. Will must confirm the correct fallback deposit amount, or whether no-package requests should be blocked from automated deposit creation entirely. | HIGH | Will | M-STRIPE-DEPOSIT Route B logic | OPEN |
| SD-006 | **Currency assumption.** All Stripe Payment Intent amounts are currently assumed to be in USD (cents). If any charter bookings are transacted in AUD (or another currency), the `currency` parameter in the Stripe API call must be set accordingly. Confirm with Will whether USD-only is correct for Stage 1, or if multi-currency support is needed from the start. | MEDIUM | Will | M-STRIPE-DEPOSIT currency handling | OPEN |

---

### 3.6 M-BOOKING-CREATION Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| OI-BC-01 | **Airtable native automation inventory must be complete before this scenario runs — see BLK-009.** This is the same issue as BLK-009, elevated here for the booking creation context. Any Airtable native automation watching the Bookings table could fire when M-BOOKING-CREATION writes a record, creating conflicting data or triggering real client communications during testing. All native automations on the Bookings table must be inventoried and deactivated before M-BOOKING-CREATION is tested. | CRITICAL | Luciana / Will | T-003, M-BOOKING-CREATION testing | OPEN |
| OI-BC-02 | **`Booking_ID_Human` field existence unconfirmed.** M-BOOKING-CREATION generates a human-readable Booking ID in the format `BK-YYYY-NNNN`. The scenario writes this to a dedicated text field `Booking_ID_Human` on the Bookings record. If Airtable uses a formula field for Booking ID generation (not a writable text field), the Make write approach must be adjusted. Confirm the field type in the live Bookings table schema before building the ID generation module. | HIGH | Systems | M-BOOKING-CREATION ID generation | OPEN |
| OI-BC-03 | **`Request_ID` field type in Bookings table.** The idempotency check in M-BOOKING-CREATION searches the Bookings table for an existing record with a matching `Request_ID` field. This lookup requires `Request_ID` to be a plain text field (not a linked record field). If it is a linked field, the FIND() filter formula must be replaced with a linked record lookup. Confirm field type before building Module 5. | HIGH | Systems | M-BOOKING-CREATION idempotency check | OPEN |
| OI-BC-04 | **Deposit_Amount unit (cents vs dollars).** M-STRIPE-DEPOSIT passes the deposit amount to M-BOOKING-CREATION. The unit of this value (cents as integer, or dollars as decimal) must be agreed between both scenarios before either is built. A mismatch causes the Bookings record to store either $15,000 when $150 is correct, or $1.50 when $150 is correct. Define the canonical unit and document it in the inter-scenario data contract. | HIGH | Systems | M-BOOKING-CREATION / M-STRIPE-DEPOSIT interface | OPEN |
| OI-BC-05 | **Package field may be empty on Requests.** If the client did not select a specific package during intake, the Package linked field on the Request will be null. M-BOOKING-CREATION cannot write a null linked record without error. Will must decide: allow booking creation without a Package link (write without Package field), or block booking creation and require Package assignment before proceeding. | MEDIUM | Will | M-BOOKING-CREATION Route logic | OPEN |
| OI-BC-06 | **BK-YYYY-NNNN sequential ID race condition at scale.** The booking ID generation uses a counter to produce sequential numbers. At Stage 1 volume (1–5 bookings/day), this is safe. Above approximately 5 concurrent bookings, two simultaneous creates may read the same counter value and produce duplicate IDs. The Counter table approach (atomic increment via Airtable update) should be evaluated before Stage 2 volume scales. Document as a known Stage 1 limitation and a Stage 2 remediation item. | LOW (Stage 1) | Systems | M-BOOKING-CREATION ID generation at scale | OPEN |
| OI-BC-07 | **M-BOOKING-CONFIRMATION call sequence.** The current design assumes M-BOOKING-CREATION calls M-BOOKING-CONFIRMATION directly as its final step (before M-AUDIT-LOGGER). An alternative is to trigger M-BOOKING-CONFIRMATION separately (via Airtable watch or a separate Make webhook). The direct call approach is simpler for Stage 1 but creates tight coupling. Confirm with Systems Arch before building either scenario. | HIGH | Systems | M-BOOKING-CREATION / M-BOOKING-CONFIRMATION integration | OPEN |

---

### 3.7 M-BOOKING-CONFIRMATION Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| BF-001 | **Gmail OAuth connections not yet authenticated for either brand.** M-BOOKING-CONFIRMATION requires two Make OAuth connections: `SSS_GMAIL_HELLO` (hello@shesaidsail.com) and `ME_GMAIL_HELLO` (hello@mareexecutive.com). OAuth must be authorized by Will using the respective Google accounts. This cannot be done by the Make builder — Will must sign in and grant access. Until both connections are active, M-BOOKING-CONFIRMATION cannot send any email, even in test mode. | CRITICAL | Will | M-BOOKING-CONFIRMATION email sends | OPEN |
| BF-002 | **Email templates must receive brand approval from Will.** The SSS and ME HTML email templates (TPL-EMAIL-001, TPL-EMAIL-002) must be reviewed and approved by Will before any email is sent — even to internal test addresses during sandbox testing. Brand copy, logo placement, color palette, and legal footer must all be confirmed correct. Stage 1 review window is during sandbox testing. | CRITICAL | Will | M-BOOKING-CONFIRMATION template validation | OPEN |
| BF-003 | **Confirmation-specific Airtable fields not confirmed to exist.** M-BOOKING-CONFIRMATION writes to multiple fields on the Bookings record after sending confirmation: `Confirmation_Email_Draft`, `Confirmation_Email_Subject`, `Confirmation_Status`, `Confirmation_Prepared_At`, `Confirmation_Prepared_By`, `Confirmation_Recipient`, `Confirmation_Phone`. None of these fields have been confirmed to exist in the live Bookings table. All must be created (if missing) before the scenario write modules are built. | HIGH | Systems | M-BOOKING-CONFIRMATION write modules | OPEN |
| BF-004 | **Stage 2 activation gate — no client emails in Stage 1.** M-BOOKING-CONFIRMATION is designed but must NOT send emails to real client addresses during Stage 1. All email recipients must be overridden to Will's test address. A code-level safeguard (not just a process rule) must be implemented: a Make filter that prevents the `To:` field from being set to any address except the configured test address when `Environment = sandbox`. This filter must be removed only after Will's explicit sign-off at Stage 1 completion. | CRITICAL | Make builder / Will | Stage 1 → Stage 2 promotion gate | OPEN |

---

### 3.8 M-AUDIT-LOGGER Scenario Issues

| Issue ID | Description | Severity | Owner | Blocks | Status |
|----------|-------------|----------|-------|--------|--------|
| AL-001 | **Audit_Log table field names and Single Select options not confirmed.** M-AUDIT-LOGGER writes to the Audit_Log table (`tblrMpTfMk8q1eNHp`). All field names, field types, and Single Select option values (for `Approval_State`, `Brand`, `City`, `Environment`) must be confirmed against the live table schema before the write modules are built. Single Select writes with an option value that does not exist in Airtable's option list cause a silent failure — the field remains null. | CRITICAL | Systems | M-AUDIT-LOGGER (all writes) | OPEN |
| AL-002 | **`Payload_Hash` and `Make_Run_ID` fields must exist in Audit_Log.** The idempotency check in M-AUDIT-LOGGER uses a `Payload_Hash` field to detect duplicate log entries. The `Make_Run_ID` field stores Make's execution ID for cross-referencing. Both fields must be confirmed to exist as Single Line Text fields in the live Audit_Log table before M-AUDIT-LOGGER is built. If either is missing, add them before build begins. | CRITICAL | Systems | M-AUDIT-LOGGER idempotency | OPEN |
| AL-003 | **M-AUDIT-LOGGER webhook URL must be registered first and distributed to all scenario builders.** M-AUDIT-LOGGER is called by all other Stage 1 scenarios. Its internal webhook URL (Make-generated) must exist before any other scenario is built — scenario builders need this URL to configure their outbound call to M-AUDIT-LOGGER. M-AUDIT-LOGGER must be built and its webhook URL registered before any other Stage 1 scenario construction begins. This is the first scenario to build. | BLOCKER | Systems / Make builder | ALL other Stage 1 scenarios | OPEN |

---

## SECTION 4 — ARCHITECTURE DECISIONS PENDING WILL SIGN-OFF

These are unresolved design decisions that require a Founder Decision before Make build can proceed on the affected scenarios.

| Decision ID | Question | Options | Default if No Decision | Owner | Deadline | Status |
|-------------|----------|---------|------------------------|-------|----------|--------|
| ARCH-001 | **SSS and ME packages in same table or separate tables?** M-STRIPE-DEPOSIT and M-BOOKING-CREATION read from the Packages table. If both brands share one table, a `Brand` filter is required on every query. If separate tables, scenario routing adds complexity. Current spec assumes one shared table. | (A) One Packages table with Brand field; (B) SSS_Packages + ME_Packages separate tables | Option A (one table) | Will | Before M-STRIPE-DEPOSIT build | OPEN |
| ARCH-002 | **Financial_Periods table — ops base or financials base?** The architecture references a `Financial_Periods` table for revenue reporting. It is not confirmed whether this table should live in the main ops base (`appdZ49WqgjRXxA1R`) or in a separate financials base. Cross-base reads in Make require separate Airtable connections. | (A) Same base as ops; (B) Separate financials base | Option A (same base) | Will | Before Stage 2 financials build | OPEN |
| ARCH-003 | **Sandbox base — new base or repurpose a retired base?** Stage 1 testing requires a Sandbox Airtable base that is structurally identical to production but isolated. A new base must be created (or a retired base repurposed) with a complete schema copy. This base must NOT be `appdZ49WqgjRXxA1R`. | (A) Create new empty base and replicate schema; (B) Repurpose an existing retired test base | Option A (new base) | Will | Before any sandbox testing begins | OPEN |
| ARCH-004 | **Bearer token approach for webhook security.** Two approaches are available for authenticating inbound webhooks to M-LEAD-INTAKE: (A) Include an `api_key` field in the JSON request body, validated in the first Make filter module — simpler to implement but key is visible in request body logs; (B) Use an HTTP Authorization header (`Authorization: Bearer [token]`) validated by Make's native webhook authentication — more secure, standard practice. Will must select the approach as it determines the URL structure and authentication configuration in the Webflow/Typeform form setup. | (A) Body api_key field; (B) HTTP Authorization header Bearer token | Option B (Authorization header) | Will | Before WHK-SSS-LEAD-INTAKE-SANDBOX is registered | OPEN |

---

## SECTION 5 — EXTERNAL DEPENDENCIES

Items that require action or confirmation from external services or systems before Stage 1 is fully operational.

| Dependency ID | Description | External System | Owner | Required Before | Status |
|---------------|-------------|-----------------|-------|-----------------|--------|
| EXT-001 | **Stripe test API key confirmation.** The `sk_test_` key for the SSS/ME Stripe account must be retrieved from the Stripe Dashboard (Test Mode → Developers → API Keys) and stored in Make as `SSS_STRIPE_TEST_SECRET`. CRITICAL: confirm the key begins with `sk_test_` — never use a `sk_live_` key during Stage 1. | Stripe | Will | M-STRIPE-DEPOSIT build | OPEN |
| EXT-002 | **Slack app creation and bot token.** The "She Said Sail Bot" Slack app must be created at api.slack.com/apps, OAuth scopes added (`chat:write`, `im:write`, `channels:read`, `users:read`), app installed to the workspace, bot token retrieved and stored in Make as `SSS_SLACK_BOT`, and bot manually invited to #sss-ops-alerts and #sss-emergency-ops. | Slack | Luciana | M-SLACK-ALERTS build | OPEN |
| EXT-003 | **Gmail OAuth for hello@shesaidsail.com.** Will must authenticate the `SSS_GMAIL_HELLO` Make connection by signing in to Google as hello@shesaidsail.com and granting `gmail.send` scope only. This OAuth connection cannot be created by the Make builder — it requires Will to perform the Google sign-in step directly in Make.com. | Gmail / Google | Will | M-BOOKING-CONFIRMATION build | OPEN |
| EXT-004 | **Gmail OAuth for hello@mareexecutive.com.** Identical requirement as EXT-003, for the ME brand Gmail account. Will must authenticate the `ME_GMAIL_HELLO` Make connection separately. | Gmail / Google | Will | M-BOOKING-CONFIRMATION build | OPEN |
| EXT-005 | **Quo SMS API key and rate limit confirmation.** The Quo SMS API key must be obtained from Luciana's Quo SMS account and stored in Make as `SSS_QUO_SMS_API`. Additionally, the exact rate limit (requests per minute) must be confirmed from Quo SMS documentation before M-BOOKING-CONFIRMATION is built, so the Make error handler for HTTP 429 can be configured with the correct wait interval. | Quo SMS | Luciana | M-BOOKING-CONFIRMATION SMS module | OPEN |
| EXT-006 | **Concierge_Operators table — at least one active operator per brand.** M-CONCIERGE-ASSIGNMENT cannot function without at least one active SSS concierge and one active ME concierge in the Concierge_Operators table. This is a data population dependency, not a system configuration — Luciana must enter the records before Stage 1 go-live. At minimum: operator name, email, brand scope, city coverage, and `Status = Active`. | Airtable (data population) | Luciana | M-CONCIERGE-ASSIGNMENT testing (T-001, T-002) | OPEN |
| EXT-007 | **Webflow and Typeform form field names confirmed and mapped.** The field names and reference keys in Webflow forms and Typeform surveys must be confirmed before M-LEAD-INTAKE's field mapping module is built. Webflow field names appear in the webhook payload under the keys configured in the Webflow form builder. Typeform reference keys may differ from display labels. Luciana must provide a field-by-field mapping document from both form builders before M-LEAD-INTAKE field mapping is coded. | Webflow / Typeform | Luciana | M-LEAD-INTAKE build | OPEN |

---

## ISSUE STATUS TRACKER

Use this table for rapid weekly status review. Update the Status column as issues are resolved.

| Category | Total Issues | OPEN | IN PROGRESS | RESOLVED | DEFERRED |
|----------|-------------|------|-------------|----------|----------|
| Section 1 — Critical Blockers | 6 | 6 | 0 | 0 | 0 |
| Section 2 — High Priority | 3 | 3 | 0 | 0 | 0 |
| Section 3.1 — M-BRAND-ROUTER | 6 | 6 | 0 | 0 | 0 |
| Section 3.2 — M-LEAD-INTAKE | 9 | 9 | 0 | 0 | 0 |
| Section 3.3 — M-SLACK-ALERTS | 8 | 8 | 0 | 0 | 0 |
| Section 3.4 — M-CONCIERGE-ASSIGNMENT | 5 | 5 | 0 | 0 | 0 |
| Section 3.5 — M-STRIPE-DEPOSIT | 6 | 6 | 0 | 0 | 0 |
| Section 3.6 — M-BOOKING-CREATION | 7 | 7 | 0 | 0 | 0 |
| Section 3.7 — M-BOOKING-CONFIRMATION | 4 | 4 | 0 | 0 | 0 |
| Section 3.8 — M-AUDIT-LOGGER | 3 | 3 | 0 | 0 | 0 |
| Section 4 — Architecture Decisions | 4 | 4 | 0 | 0 | 0 |
| Section 5 — External Dependencies | 7 | 7 | 0 | 0 | 0 |
| **TOTAL** | **68** | **68** | **0** | **0** | **0** |

---

## ISSUE RESOLUTION LOG

When an issue is resolved, record it here. Do not delete entries from Sections 1–5 — update their Status column instead and reference the Resolution Log entry.

| Resolved Date | Issue ID | Resolution Summary | Resolved By |
|---------------|----------|--------------------|-------------|
| | | | |
| | | | |

---

*Document last updated: 2026-05-16. All issues OPEN as of this date — Make build phase has not yet begun.*
*Luciana owns this register. Will must sign off on all Section 4 architecture decisions before Make build begins.*
*Cross-reference: STAGE_1_BLOCKER_RESOLUTION_REPORT.md (Sections 1–2); individual scenario spec Open Issues sections (Section 3).*
