# STAGE 1 CREDENTIAL BLOCKERS AND ACCESS REGISTRY
**Project:** She Said Sail + Mare Executive — Make.com Automation System
**Base:** appdZ49WqgjRXxA1R
**Document ID:** OUT-002
**Prepared by:** Production Reliability Engineering
**Date:** 2026-05-16
**Purpose:** Definitive registry of every credential gap and Airtable schema gap preventing the Stage 1 Make build from beginning. Use this document as the resolution checklist for Will and Luciana's pre-build session.
**Status:** ACTIVE — Not Ready. Update status fields as each item is resolved.

---

## SECTION 1: EXECUTIVE SUMMARY

### Total Blocker Count

| Category | Count | Severity |
|----------|-------|----------|
| Make connection credentials — NEEDS SETUP | 6 | Critical to High |
| Make connection credentials — BLOCKED | 1 | Blocker (sequential dependency) |
| Make connection credentials — STAGED (not needed Stage 1) | 1 | N/A |
| Airtable schema gaps — missing fields | 27 fields across 5 tables | Critical to Medium |
| Airtable schema gaps — missing table | 1 (Automation_Health) | Critical |
| External dependency gaps | 3 | High to Medium |
| **Total combined blockers** | **39 items** | — |

### Combined Blocker Impact

Every single Make.com scenario in Stage 1 is blocked from being built or tested in sandbox mode. The Make build cannot begin in any meaningful capacity until the CRITICAL-tier items below are resolved. The documentation phase is complete. The build phase is fully blocked.

**Scenarios blocked at all:** ALL 8 (BLK-001, BLK-003)
**Scenarios blocked specifically:** M-STRIPE-DEPOSIT (BLK-008), M-BOOKING-CREATION (BLK-002, BLK-007), M-BRAND-ROUTER (BLK-004), M-AUDIT-LOGGER (BLK-006)

### Estimated Resolution Time

Resolving all CRITICAL and HIGH blockers in a single focused session: **4–8 hours** for Will and Luciana working together. MEDIUM items can follow in a subsequent hour. The Make build can begin immediately upon CRITICAL resolution.

**Fastest path to build start:** Resolve BLK-001 + BLK-003 first (Environment field + Automations_Paused). These two items alone unblock M-AUDIT-LOGGER construction, which is the required first scenario.

---

## SECTION 2: MAKE CONNECTION BLOCKERS

> Storage rule: All credential values live in Make.com's built-in Connection vault only. Never store credential values in Airtable fields, Make data store notes, scenario description fields, source-controlled files, or Slack messages. If a credential is accidentally exposed in any of those locations, treat it as compromised and rotate immediately.

### 2A — Credential Table

| Credential | Connection Name in Make | Status | Owner | Est. Time | Blocks |
|------------|------------------------|--------|-------|-----------|--------|
| Airtable PAT | `SSS_AIRTABLE_PAT` | NEEDS SETUP | Will | 15 min | ALL 8 scenarios |
| Stripe Test Secret Key | `SSS_STRIPE_TEST_SECRET` | NEEDS SETUP | Will | 10 min | M-STRIPE-DEPOSIT |
| Stripe Webhook Signing Secret | `SSS_STRIPE_WEBHOOK_SECRET_TEST` | BLOCKED (BLK-008) | Make builder | 10 min after Make URL exists | M-STRIPE-DEPOSIT |
| Slack Bot Token | `SSS_SLACK_BOT` | NEEDS SETUP | Luciana | 20 min | M-SLACK-ALERTS, all error alerts |
| Gmail OAuth — She Said Sail | `SSS_GMAIL_HELLO` | NEEDS SETUP | Will | 10 min | M-BOOKING-CONFIRMATION |
| Gmail OAuth — Mare Executive | `ME_GMAIL_HELLO` | NEEDS SETUP | Will | 10 min | M-BOOKING-CONFIRMATION |
| Quo SMS API Key | `SSS_QUO_SMS_API` | NEEDS SETUP | Luciana | 15 min | M-STRIPE-DEPOSIT (SMS send) |
| Anthropic API Key | `SSS_ANTHROPIC_API` | STAGED — Stage 2 only | Will | N/A Stage 1 | None in Stage 1 |

### 2B — Per-Credential Detail

---

#### CREDENTIAL: Airtable PAT — `SSS_AIRTABLE_PAT`

**Resolution steps:**
1. Will: Log in to Airtable → Account → API → Create Personal Access Token.
2. Name the token: `SSS-Stage1-Make-Production`.
3. Grant exactly these scopes: `data.records:read`, `data.records:write`, `schema.bases:read`, `webhook.manage:write`.
4. Scope the token to base `appdZ49WqgjRXxA1R` only.
5. In Make.com: Connections → Add → Airtable → Personal Access Token → paste token → name connection `SSS_AIRTABLE_PAT` → Save and Test.
6. Verify Make shows green checkmark on the connection.

**Storage:** Make.com Connection vault only. Token value never leaves the Make credential interface.

**Rotation schedule:** Every 90 days. Will creates a calendar reminder on token creation date. Token expiry date must be documented in the Credential Rotation Calendar (end of this section).

**What breaks if expired:** ALL 8 Make scenarios fail at their first Airtable module. M-AUDIT-LOGGER cannot write to Audit_Log. Luciana and Will receive no Slack alerts (because M-SLACK-ALERTS also depends on Airtable reads). Effective system-wide outage with no audit trail.

---

#### CREDENTIAL: Stripe Test Secret Key — `SSS_STRIPE_TEST_SECRET`

**Resolution steps:**
1. Will: Log in to Stripe Dashboard → toggle to **Test Mode** (confirm "TEST DATA" banner is visible).
2. Developers → API Keys → Reveal Secret Key (or create a restricted key with: Payment Intents: Write, Checkout Sessions: Write, Webhooks: Read).
3. Confirm key begins with `sk_test_` — if it begins with `sk_live_`, stop. Do not use the live key in Stage 1.
4. In Make.com: Connections → Add → Stripe → paste key → name `SSS_STRIPE_TEST_SECRET` → Verify.
5. In Stripe Dashboard (Test Mode) → Settings → Emails → disable "Send emails for successful payments" to prevent Stripe's own receipt emails from reaching real addresses during testing.

**Storage:** Make.com Connection vault only.

**Rotation schedule:** Replace with live key at Stage 1 go-live sign-off. Rotate test key every 6 months if Stage 1 extends beyond that.

**What breaks if expired or revoked:** M-STRIPE-DEPOSIT cannot create Checkout Sessions. Deposit link generation fails. No deposit Slack alert fires. M-BOOKING-CREATION cannot proceed (depends on deposit completion). Entire deposit-to-booking pipeline stops.

---

#### CREDENTIAL: Stripe Webhook Signing Secret — `SSS_STRIPE_WEBHOOK_SECRET_TEST`

**Status: BLOCKED — cannot generate until Make webhook URL exists.**

**Resolution steps (in order):**
1. Make builder creates M-STRIPE-DEPOSIT scenario skeleton in Make with a Custom Webhook trigger module.
2. Make generates a unique webhook URL — format: `https://hook.{region}.make.com/{unique-token}`.
3. Copy the URL. Document it in the `Make_Scenarios` Airtable table row for M-STRIPE-DEPOSIT and in the STAGE_1_CREDENTIAL_AND_WEBHOOK_CHECKLIST.md.
4. Will: Stripe Dashboard (Test Mode) → Developers → Webhooks → Add Endpoint → paste Make URL.
5. Select events: `payment_intent.succeeded`, `payment_intent.payment_failed`, `checkout.session.completed`, `checkout.session.expired`.
6. Save — Stripe generates a signing secret (`whsec_[64 chars]`).
7. Store signing secret in Make: Connections → HTTP custom connection or Make Data Store (restricted) → name: `SSS_STRIPE_WEBHOOK_SECRET_TEST`.
8. Add Stripe signature validation as the FIRST module in M-STRIPE-DEPOSIT after the webhook trigger.

**Current Make webhook URL:** `[TO BE GENERATED — resolve BLK-008]`
**Current signing secret:** `[TO BE STORED IN MAKE VAULT AFTER STEP 6]`

**Storage:** Make.com Data Store (secure variable) or Make Connection vault. Never in Airtable, never in git.

**Rotation schedule:** When Make webhook URL changes (scenario rebuild). At Stage 1 go-live (new endpoint registered in Stripe live mode).

**What breaks if expired:** Stripe sends events to Make but signature validation fails → Make returns HTTP 400 → Stripe marks endpoint as failing → Stripe stops sending events after repeated failures → entire payment event pipeline goes dark silently.

---

#### CREDENTIAL: Slack Bot Token — `SSS_SLACK_BOT`

**Resolution steps:**
1. Luciana (or Will as workspace admin): Go to https://api.slack.com/apps → Create New App → From Scratch.
2. App name: `She Said Sail Bot` — Workspace: She Said Sail Slack workspace.
3. OAuth & Permissions → Bot Token Scopes → Add: `chat:write`, `chat:write.public`, `channels:read`, `users:read`.
4. Install App → Install to Workspace → Authorize.
5. Copy the Bot User OAuth Token (`xoxb-...`).
6. In Make: Connections → Add → Slack → paste token → name `SSS_SLACK_BOT` → Save.
7. In Slack: Run `/invite @She Said Sail Bot` in both `#sss-ops-alerts` and `#sss-emergency-ops`.

**Storage:** Make.com Connection vault only.

**Rotation schedule:** No automatic expiry. Rotate if app is reinstalled or token is revoked. Check token validity monthly in Slack API console.

**What breaks if revoked:** M-SLACK-ALERTS cannot post new lead alerts to #sss-ops-alerts. All 4 error-handling levels (L1–L4) that escalate via Slack go dark. Will and Luciana receive no system alerts. Critical incidents become invisible until someone manually checks Make's execution log.

---

#### CREDENTIAL: Gmail OAuth — She Said Sail — `SSS_GMAIL_HELLO`

**Resolution steps:**
1. Will (must have access to hello@shesaidsail.com or be a Google Workspace admin): In Make.com → Connections → Add → Gmail → OAuth 2.0.
2. Click "Sign in with Google" → sign in as hello@shesaidsail.com.
3. Grant `gmail.send` scope only. Do not grant `gmail.modify` or `mail.google.com`.
4. Name connection: `SSS_GMAIL_HELLO` → Save.
5. Verify in Google Account → Security → Third-party access that scope is limited to gmail.send.
6. In M-BOOKING-CONFIRMATION, confirm the recipient is overridden to `will@shesaidsail.com` for all Stage 1 runs. Do not restore `{{client_email}}` until Stage 1 go-live sign-off.

**Storage:** Make.com OAuth connection vault. OAuth refresh token managed by Make automatically.

**Rotation schedule:** OAuth refresh tokens auto-renew. Reauthorize annually or if Google revokes access (typically triggered by >6 months of inactivity or a security policy change in Google Workspace).

**What breaks if revoked:** M-BOOKING-CONFIRMATION cannot create Gmail drafts. Luciana cannot review and send booking confirmations. Stage 1 confirmation flow breaks. Note: In Stage 1, this scenario is draft-only — no client emails are sent directly by Make, so revocation has lower blast radius than in Stage 2+.

---

#### CREDENTIAL: Gmail OAuth — Mare Executive — `ME_GMAIL_HELLO`

**Resolution steps:** Identical to SSS Gmail setup. Substitute `hello@mareexecutive.com` and connection name `ME_GMAIL_HELLO`. Will must have access to the Mare Executive Google Workspace account.

**Storage, rotation, and breakage impact:** Same as SSS Gmail above.

**Brand routing dependency:** In M-BOOKING-CONFIRMATION, the Router branch sends SSS leads to `SSS_GMAIL_HELLO` (template TPL-EMAIL-001) and ME leads to `ME_GMAIL_HELLO` (template TPL-EMAIL-002). Both connections must be active before M-BOOKING-CONFIRMATION can be built.

---

#### CREDENTIAL: Quo SMS API Key — `SSS_QUO_SMS_API`

**Resolution steps:**
1. Luciana: Retrieve API key from Quo SMS account dashboard.
2. In Make: Connections → Add → HTTP Custom Connection → API Key in Authorization header: `Bearer {{quo_api_key}}` → name `SSS_QUO_SMS_API` → Save.
3. Store Will's test phone number in Make Data Store as `WILL_TEST_PHONE` — all Stage 1 SMS sends go to this number only.
4. Confirm the Quo SMS sender ID is configured to display "She Said Sail" or "Mare Executive" per brand.

**Storage:** Make.com HTTP Connection vault. `WILL_TEST_PHONE` in Make Data Store (not sensitive).

**Rotation schedule:** Every 180 days; immediately if compromised.

**What breaks if expired:** M-STRIPE-DEPOSIT cannot send the deposit link SMS to the client's phone. In Stage 1, SMS goes to Will's test phone only — low blast radius. In Stage 2+, client communications stop.

---

### 2C — Anthropic API Key — `SSS_ANTHROPIC_API` (Staged — Stage 2)

**Status:** STAGED. Obtain and store now, but do NOT connect to any Stage 1 scenario module.

The Anthropic API key is pre-staged to avoid delays at Stage 2 kickoff. Will obtains the key from https://console.anthropic.com/settings/keys and stores it in Make. No Stage 1 scenario references `SSS_ANTHROPIC_API`. Verify this after every Make build session: search all 8 scenario module configurations for any reference to this connection — there should be zero.

**Billing alert:** Set a $50/month threshold alert in the Anthropic console before storing the key. Zero usage is expected throughout Stage 1.

---

### 2D — Credential Rotation Calendar

| Credential | Connection Name | Creation Date | Rotation Due | Calendar Alert Set |
|------------|----------------|---------------|-------------|-------------------|
| Airtable PAT | `SSS_AIRTABLE_PAT` | [SET ON CREATION] | 90 days | [ ] |
| Stripe Test Key | `SSS_STRIPE_TEST_SECRET` | [SET ON CREATION] | At go-live | N/A |
| Slack Bot Token | `SSS_SLACK_BOT` | [SET ON CREATION] | On reinstall | N/A |
| Gmail SSS OAuth | `SSS_GMAIL_HELLO` | [SET ON CREATION] | 12 months | [ ] |
| Gmail ME OAuth | `ME_GMAIL_HELLO` | [SET ON CREATION] | 12 months | [ ] |
| Quo SMS API Key | `SSS_QUO_SMS_API` | [SET ON CREATION] | 180 days | [ ] |
| Anthropic API Key | `SSS_ANTHROPIC_API` | [SET ON CREATION] | 90 days | [ ] |

---

## SECTION 3: AIRTABLE SCHEMA BLOCKERS

**Total fields to add or correct:** 27 fields across 5 tables plus 1 new table.
All fields must be in place before the corresponding Make scenario is built. Do not build against a schema you have not verified.

### 3A — CRITICAL: Blocks Stage 1 From Running At All

These gaps prevent every scenario from operating. Resolve before opening Make.

---

**FIELD: Environment (Single Select)**
Tables: Requests, Bookings, Clients, Audit_Log, Automation_Health (include in creation)
Options: `production`, `sandbox`, `test` — Default during Stage 1: `sandbox`

| Table | Status | Blocks |
|-------|--------|--------|
| Requests | MISSING | M-LEAD-INTAKE, M-BRAND-ROUTER, M-CONCIERGE-ASSIGNMENT |
| Bookings | MISSING | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Clients | MISSING | M-LEAD-INTAKE, M-BOOKING-CREATION |
| Audit_Log | MISSING | M-AUDIT-LOGGER (all audit entries) |
| Automation_Health | MISSING (table does not exist yet) | ALL (kill switch) |

Resolution: Will adds Environment field to each of the 4 existing tables (15 min). Field is included when creating Automation_Health table. In Make, every scenario sets `ENVIRONMENT = sandbox` as a scenario-level constant and passes it into every Airtable Create/Update module.

Risk if skipped: Test records produced during Make build contaminate the production Airtable dataset permanently. Sandbox runs and real client records become indistinguishable. Rollback is unreliable.

---

**FIELD: Idempotency_Key (Single Line Text)**
Tables: Bookings, Requests (confirm both)

Resolution: Will adds field to Bookings table (and verifies Requests). Make generates the key as SHA256(`request_id + client_email + charter_date + timestamp_epoch`) before any write. Make searches for an existing matching key before creating a new record. If key found: halt, log DUPLICATE_PREVENTED to Audit_Log, alert Slack. If not found: proceed, write key into new record.

Risk if skipped: On any Make retry (network timeout, API rate limit, webhook replay), a second identical Booking record is created. Duplicate Bookings trigger duplicate Stripe sessions and duplicate confirmation emails. No mechanism exists to detect or purge the duplicates without manual audit.

Blocks: M-LEAD-INTAKE, M-BOOKING-CREATION.

---

**TABLE: Automation_Health (MUST BE CREATED)**

This table does not yet exist and must be created before any Make scenario is built. It is the kill switch foundation for the entire system.

Full schema required:

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| Record_Type | Single Line Text | `global_control` | Identifies this as the control record |
| Automations_Paused | Checkbox | `false` | Global kill switch for all Make scenarios |
| Maintenance_Mode | Checkbox | `false` | Secondary pause for planned maintenance |
| Paused_By | Single Line Text | (empty) | Name of person who activated pause |
| Paused_At | Date/Time | (empty) | Timestamp of pause activation |
| Pause_Reason | Long Text | (empty) | Documented reason for pause |
| Emergency_Contact | Single Line Text | `@luciana` | Slack handle to ping on critical issues |
| Environment | Single Select | `sandbox` | Environment this control record governs |

After creating the table: create exactly ONE record with `Record_Type = global_control`, `Automations_Paused = false`, `Environment = sandbox`. This single record is what every Make scenario reads at step 1. Do not create additional records.

Kill switch test (required before any scenario is activated): Set `Automations_Paused = true` in Airtable. Trigger M-AUDIT-LOGGER. Confirm the scenario exits without writing any records. Set back to `false`. Confirm normal operation resumes.

Blocks: ALL 8 scenarios (BLK-003).

---

**FIELD: Packages.Deposit_Rate_Pct (Number)**
Table: Packages

M-STRIPE-DEPOSIT reads the Packages table to determine the deposit percentage for a given charter. The `Deposit_Rate_Pct` field does not exist. Without it, M-STRIPE-DEPOSIT cannot calculate the deposit amount for the Stripe Checkout Session.

Resolution: Will adds `Deposit_Rate_Pct` (Number, decimal, e.g., 0.30 = 30%) to the Packages table and populates at least two test records — one for SSS brand, one for ME brand — before M-STRIPE-DEPOSIT is built.

Blocks: M-STRIPE-DEPOSIT. The scenario's deposit calculation is: `deposit_amount = charter_price × Deposit_Rate_Pct`. If this field is null, the Checkout Session amount is zero or errors.

---

### 3B — HIGH: Blocks Specific Scenarios

---

**Audit_Log: 8 Missing Governance Fields**

The Audit_Log table is missing the following fields required for complete governance entries. M-AUDIT-LOGGER will write partial records and governance compliance will be incomplete without them.

| Field | Type | Purpose |
|-------|------|---------|
| Prompt_Version | Single Line Text | Which AI prompt version was active (Stage 2; include now per spec) |
| AI_Confidence_Score | Number (decimal 0–1) | Confidence score from AI classification |
| Approval_State | Single Select: pending / approved / rejected | Human approval gate tracking |
| Reviewed_By | Single Line Text | Name of reviewer at approval gate |
| Rollback_Linkage | Single Line Text | ID of Deployment_Log entry if this event was rolled back |
| Environment | Single Select | Already captured in CRITICAL section above |
| Brand | Single Select: she_said_sail / mare_executive / both / none | Brand context of the logged action |
| City | Single Line Text | City of the charter (for operational reporting) |

Resolution: Will adds these 7 new fields to Audit_Log (Environment is already covered). Add all enum values to the Single Select fields.

Blocks: M-AUDIT-LOGGER (partial — it can write without these fields, but governance records are incomplete and incident investigation is impaired).

---

**Requests Table: 3 Missing Operational Fields**

| Field | Type | Purpose | Blocks |
|-------|------|---------|--------|
| Escalation_Reason | Long Text | Records why a lead was escalated for human review | M-CONCIERGE-ASSIGNMENT |
| AI_Confidence_Score | Number (decimal 0–1) | Brand classification confidence from M-BRAND-ROUTER | M-BRAND-ROUTER |
| Last_Human_Touch | Date/Time | Last time a human updated this record (ops visibility) | M-CONCIERGE-ASSIGNMENT |

---

**Bookings Table: 6 Missing Operational Fields**

| Field | Type | Purpose | Blocks |
|-------|------|---------|--------|
| D7_Review_Eligible | Formula (Boolean) | True if charter was 7+ days ago and review not yet sent | Stage 2 (add now) |
| HV_Client | Checkbox | Flags this booking as a high-value client (VIP handling) | M-BOOKING-CONFIRMATION |
| Refund_Issued | Checkbox | Tracks whether a refund has been processed | M-STRIPE-DEPOSIT |
| Agent_Status | Single Select: active / inactive / on_leave | Status of the assigned concierge agent | M-CONCIERGE-ASSIGNMENT |
| AI_Confidence_Score | Number (decimal 0–1) | Brand classification confidence written at booking creation | M-BOOKING-CREATION |
| Last_Human_Touch | Date/Time | Last human edit timestamp for ops monitoring | Ops dashboards |

---

**AI_Prompt_Versions Table: Schema Wrong (9 fields, 26 required)**

The `AI_Prompt_Versions` table in base `appdZ49WqgjRXxA1R` has only 9 fields. The architecture specification requires 26. M-BRAND-ROUTER reads from this table to retrieve the active prompt for brand classification. The 17 missing fields include `Prompt_Body`, `Is_Active`, `Brand`, `Model`, `Max_Tokens`, `Temperature`, `Version_Number`, `Activated_At`, `Activated_By`, `Deprecated_At`, and audit metadata.

Resolution: Will documents existing 9 fields, then adds 17 missing fields per the `POST_PHASE_4_SCHEMA_REGISTRY.md` specification. After adding fields, creates one active test record per brand (SSS, ME) with all 26 fields populated. M-BRAND-ROUTER will silently return null for all missing fields if this is not resolved, causing brand routing failures that do not error out — they just misroute leads.

Blocks: M-BRAND-ROUTER (HIGH — silent failure mode, no Make error).

---

### 3C — MEDIUM: Needed for Complete Operation

**Make_Scenarios Table: Currently in Non-Production Base**

The `Make_Scenarios` reference table (storing metadata about each of the 8 Make scenarios) is in a non-production Airtable base. M-AUDIT-LOGGER reads from this table to enrich audit entries with scenario context. Reading across bases requires a second Airtable connection in Make and creates a fragile cross-base dependency.

Resolution: Luciana exports `Make_Scenarios` from the non-production base (CSV). Will creates `Make_Scenarios` in base `appdZ49WqgjRXxA1R` with the schema from BLK-006. Luciana imports records and adds 8 Stage 1 scenario rows. M-AUDIT-LOGGER is updated to reference the production base. Archive (do not delete) the non-production table.

Blocks: M-AUDIT-LOGGER (partial — can function without cross-base lookup but produces audit entries with missing scenario context).

---

### 3D — Schema Blocker Resolution Summary

| Priority | Field / Table | Table | Type | Action | Time | Blocker |
|----------|--------------|-------|------|--------|------|---------|
| CRITICAL | Automation_Health | (New table) | 8 fields | CREATE table | 20 min | BLK-003 |
| CRITICAL | Environment | Requests | Single Select | ADD | 5 min | BLK-001 |
| CRITICAL | Environment | Bookings | Single Select | ADD | 5 min | BLK-001 |
| CRITICAL | Environment | Clients | Single Select | ADD | 5 min | BLK-001 |
| CRITICAL | Environment | Audit_Log | Single Select | ADD | 5 min | BLK-001 |
| CRITICAL | Idempotency_Key | Bookings | Single Line Text | ADD | 5 min | BLK-002 |
| CRITICAL | Idempotency_Key | Requests | Single Line Text | VERIFY/ADD | 5 min | BLK-002 |
| CRITICAL | Deposit_Rate_Pct | Packages | Number | ADD + POPULATE | 20 min | — |
| HIGH | Make_Processing | Bookings | Checkbox | ADD | 5 min | BLK-007 |
| HIGH | Needs_Make_Processing | Bookings | Single Line Text | ADD | 5 min | BLK-007 |
| HIGH | Last_Make_Run | Bookings | Date/Time | ADD | 5 min | BLK-007 |
| HIGH | 8 governance fields | Audit_Log | Various | ADD | 20 min | — |
| HIGH | Escalation_Reason | Requests | Long Text | ADD | 5 min | — |
| HIGH | AI_Confidence_Score | Requests | Number | ADD | 5 min | — |
| HIGH | Last_Human_Touch | Requests | Date/Time | ADD | 5 min | — |
| HIGH | HV_Client | Bookings | Checkbox | ADD | 5 min | — |
| HIGH | Refund_Issued | Bookings | Checkbox | ADD | 5 min | — |
| HIGH | Agent_Status | Bookings | Single Select | ADD | 5 min | — |
| HIGH | AI_Confidence_Score | Bookings | Number | ADD | 5 min | — |
| HIGH | Last_Human_Touch | Bookings | Date/Time | ADD | 5 min | — |
| HIGH | AI_Prompt_Versions | AI_Prompt_Versions | 17 missing fields | ADD + POPULATE | 45 min | BLK-004 |
| MEDIUM | D7_Review_Eligible | Bookings | Formula | ADD | 10 min | BLK-005 |
| MEDIUM | Review_Sent | Bookings | Checkbox | ADD | 5 min | BLK-005 |
| MEDIUM | Make_Scenarios | (New in prod base) | 8 fields | MIGRATE | 60 min | BLK-006 |

---

## SECTION 4: EXTERNAL DEPENDENCY BLOCKERS

These blockers exist outside Make and Airtable. They require coordination with third parties or outstanding configuration decisions.

### EXT-001 — Webflow Form Field Names Not Confirmed

**Status:** UNRESOLVED

M-LEAD-INTAKE maps incoming Webflow form fields to Airtable fields. The exact field names that Webflow POST submissions use in their JSON payload have not been confirmed against the live Webflow form configuration. If the field names in M-LEAD-INTAKE's mapping do not match the actual Webflow output (e.g., `lead_name` vs. `name` vs. `full_name`), the scenario will fail to read lead data and will write empty or null values to Airtable.

**Resolution:** Will or Luciana exports a test Webflow form submission and confirms the exact JSON field names. The AIRTABLE_FIELD_MAPPING_REGISTRY.md must be updated with the confirmed field names before M-LEAD-INTAKE field mapping is finalized in Make.

**Blocks:** M-LEAD-INTAKE field mapping finalization (can build the scenario skeleton, cannot finalize data mapping until confirmed).

---

### EXT-002 — Concierge_Operators Table May Be Empty

**Status:** UNVERIFIED

M-CONCIERGE-ASSIGNMENT queries the Concierge_Operators table to find the next eligible concierge (Active_Load below capacity cap). If the table has no records with `Status = active`, the scenario will find zero eligible concierges. The scenario will not error — it will write `Assigned_Concierge = null` to the Request record and Luciana will receive no assignment notification.

**Resolution:** Luciana verifies the Concierge_Operators table has at least one active concierge record with all required fields populated: `Name`, `Slack_Handle`, `Active_Load`, `Load_Cap`, `Status = active`, `Brand` (SSS, ME, or both). For sandbox testing, create a test concierge record: `Name = Test Concierge`, `Load_Cap = 10`, `Active_Load = 0`, `Status = active`.

**Blocks:** M-CONCIERGE-ASSIGNMENT sandbox test execution (can build the scenario; cannot verify assignment works until at least one active concierge record exists).

---

### EXT-003 — Packages Table Has No Test Records With Deposit_Rate_Pct

**Status:** UNRESOLVED (field is also missing — see Section 3A)

The Packages table currently has only 8 of 25 required fields and contains no records with `Deposit_Rate_Pct` populated. M-STRIPE-DEPOSIT must look up the package for the incoming inquiry and read `Deposit_Rate_Pct` to calculate the deposit amount. No matching Package record means M-STRIPE-DEPOSIT creates a Checkout Session with a null or zero amount.

**Resolution:** After Will adds `Deposit_Rate_Pct` to the Packages table (Section 3A), Will or Luciana creates at least two test package records:
- One SSS charter package: `Brand = she_said_sail`, `Deposit_Rate_Pct = 0.30` (or the correct rate)
- One ME charter package: `Brand = mare_executive`, `Deposit_Rate_Pct = 0.25` (or the correct rate)

**Blocks:** M-STRIPE-DEPOSIT end-to-end sandbox test.

---

## SECTION 5: RESOLUTION SEQUENCE

Execute in this exact order during a single focused session. Steps are organized to unblock scenarios in their deployment dependency order (M-AUDIT-LOGGER first, M-STRIPE-DEPOSIT last).

**Estimated total session time: 4–6 hours (Will + Luciana together)**

---

**PHASE 1 — AIRTABLE FOUNDATION (Will, ~90 min)**

1. [Will] Create `Automation_Health` table in base `appdZ49WqgjRXxA1R` with all 8 fields per the spec in Section 3A. Create 1 control record: `Record_Type = global_control`, `Automations_Paused = false`. **This is step 1 because the kill switch must exist before anything else is built.**

2. [Will] Add `Environment` (Single Select: production / sandbox / test, default: sandbox) to: Requests, Bookings, Clients, Audit_Log. Four fields, four tables, ~5 min each.

3. [Will] Add `Idempotency_Key` (Single Line Text) to Bookings. Verify it exists on Requests or add it. These two fields unblock M-LEAD-INTAKE and M-BOOKING-CREATION.

4. [Will] Add `Deposit_Rate_Pct` (Number, decimal) to Packages table. Populate two test records (SSS + ME) with deposit rates. Unblocks M-STRIPE-DEPOSIT calculation.

5. [Will] Add the 3 Bookings circular trigger fields: `Make_Processing` (Checkbox), `Needs_Make_Processing` (Single Line Text), `Last_Make_Run` (Date/Time). Unblocks BLK-007.

6. [Will] Add all 8 missing Audit_Log governance fields (listed in Section 3B). Unblocks complete M-AUDIT-LOGGER logging.

7. [Will] Add the 6 missing Bookings operational fields: `HV_Client`, `Refund_Issued`, `Agent_Status`, `AI_Confidence_Score`, `Last_Human_Touch`, `Review_Sent`. Add the formula field `D7_Review_Eligible` last (it depends on `Review_Sent` existing).

8. [Will] Add the 3 missing Requests fields: `Escalation_Reason`, `AI_Confidence_Score`, `Last_Human_Touch`.

9. [Will] Audit `AI_Prompt_Versions` table — document existing 9 fields, add the 17 missing fields per POST_PHASE_4_SCHEMA_REGISTRY.md, create 2 test prompt records (SSS + ME active).

---

**PHASE 2 — EXTERNAL CREDENTIAL SETUP (Will + Luciana, ~75 min)**

10. [Will] Generate Airtable PAT with correct scopes. Create Make connection `SSS_AIRTABLE_PAT`. Run HTTP test: GET /Requests returns HTTP 200. Document PAT expiry date, set calendar reminder.

11. [Will] Retrieve Stripe test secret key from Stripe Dashboard (test mode). Create Make connection `SSS_STRIPE_TEST_SECRET`. Disable Stripe receipt emails for test mode.

12. [Will] Create Gmail OAuth connections `SSS_GMAIL_HELLO` (hello@shesaidsail.com) and `ME_GMAIL_HELLO` (hello@mareexecutive.com) in Make. Verify gmail.send scope only on both.

13. [Luciana] Create Slack Bot `She Said Sail Bot` in Slack API console. Add required OAuth scopes. Install to workspace. Copy `xoxb-...` token. Create Make connection `SSS_SLACK_BOT`. Invite bot to `#sss-ops-alerts` and `#sss-emergency-ops`. Send test message to each channel.

14. [Luciana] Retrieve Quo SMS API key. Create Make HTTP connection `SSS_QUO_SMS_API`. Store Will's test phone as `WILL_TEST_PHONE` in Make Data Store. Send test SMS to Will's phone.

15. [Luciana] Verify Concierge_Operators table has at least one active test concierge record with all required fields.

16. [Will or Luciana] Confirm Webflow form field names by submitting a test form and inspecting the JSON payload. Update AIRTABLE_FIELD_MAPPING_REGISTRY.md.

---

**PHASE 3 — MAKE BUILD (Make builder, starting immediately after Phase 2, ~5–7 hrs)**

17. [Make builder] Build M-AUDIT-LOGGER first. No external API dependencies. Verify sandbox Audit_Log write with all required fields.

18. [Make builder] Build M-SLACK-ALERTS. Test Block Kit templates in both channels.

19. [Make builder] Build M-BRAND-ROUTER. Verify SSS and ME classification routes. Test AMBIGUOUS path (routes to SSS concierge with flag).

20. [Make builder] Build M-LEAD-INTAKE. Test with confirmed Webflow field names. Verify idempotency (submit same payload twice, confirm 1 record created).

21. [Make builder] Build M-CONCIERGE-ASSIGNMENT. Verify round-robin assignment with test concierge record.

22. [Make builder] Build M-STRIPE-DEPOSIT skeleton (webhook trigger module only). **Copy the generated Make webhook URL. Register it in Stripe test-mode dashboard.** Store signing secret as `SSS_STRIPE_WEBHOOK_SECRET_TEST`. Complete scenario build. Verify BLK-008 is resolved.

23. [Make builder] Build M-BOOKING-CREATION. Verify circular trigger guard (one execution per trigger, no cascade).

24. [Make builder] Build M-BOOKING-CONFIRMATION. Confirm output is Gmail draft only — no direct send. Confirm test recipient override is `will@shesaidsail.com`.

---

**PHASE 4 — KILL SWITCH VERIFICATION (Luciana sign-off)**

25. [Luciana] Set `Automations_Paused = true` in Automation_Health. Trigger M-LEAD-INTAKE with a test payload. Confirm zero records created, zero Slack alerts, zero Audit_Log entries. Set back to `false`. Sign off.

---

**SIGN-OFF GATE: Do not activate any Make scenario in production until all 25 steps above are complete and signed off.**

---

*Document last updated: 2026-05-16. Update Status fields as blockers are resolved. This document is not to be committed to any public repository.*
*Cross-references: STAGE_1_BLOCKER_RESOLUTION_REPORT.md, STAGE_1_AIRTABLE_FIELD_PATCH_REPORT.md, STAGE_1_CREDENTIAL_AND_WEBHOOK_CHECKLIST.md, POST_PHASE_4_SCHEMA_REGISTRY.md*
