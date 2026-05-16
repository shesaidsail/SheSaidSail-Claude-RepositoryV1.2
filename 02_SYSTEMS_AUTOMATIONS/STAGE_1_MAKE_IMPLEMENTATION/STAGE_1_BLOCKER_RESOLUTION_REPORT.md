# STAGE 1 BLOCKER RESOLUTION REPORT
**Project:** She Said Sail + Mare Executive — Make.com Automation System  
**Base:** appdZ49WqgjRXxA1R  
**Prepared by:** Production Reliability Engineering  
**Date:** 2026-05-16  
**Stage:** Stage 1 (8 core scenarios)  
**Document Status:** ACTIVE — Update status fields as blockers are resolved

---

## Blocker Summary Table

| Blocker ID | Severity | Description | Owner | Status | Blocks Scenarios |
|------------|----------|-------------|-------|--------|-----------------|
| BLK-001 | CRITICAL | Environment field missing on most tables | Will | OPEN | ALL |
| BLK-002 | CRITICAL | Idempotency_Key missing on Bookings | Will | OPEN | M-BOOKING-CREATION |
| BLK-003 | CRITICAL | Automations_Paused field not verified | Luciana | OPEN | ALL |
| BLK-004 | HIGH | AI_Prompt_Versions table wrong schema | Will | OPEN | M-BRAND-ROUTER |
| BLK-005 | HIGH | D7_Review_Eligible formula missing on Bookings | Will | OPEN | Future (architecture risk) |
| BLK-006 | MEDIUM | Make_Scenarios table in non-production base | Luciana | OPEN | M-AUDIT-LOGGER |
| BLK-007 | HIGH | Circular trigger risk on Bookings | Make builder | OPEN | M-BOOKING-CREATION |
| BLK-008 | BLOCKER | Stripe webhook endpoint URL not documented | Make builder | OPEN | M-STRIPE-DEPOSIT |
| BLK-009 | HIGH | Airtable-native automations inventory incomplete | Luciana | OPEN | M-BOOKING-CREATION |

---

## Priority Resolution Order

Resolve in this exact sequence to unblock scenarios in dependency order:

```
1. BLK-003  →  Must verify Automations_Paused BEFORE any Make scenario fires a write
2. BLK-001  →  Environment field must exist before ANY record is created in any table
3. BLK-009  →  Must know all native automations before writing to Bookings
4. BLK-007  →  Must design circular trigger guard before Bookings scenario is built
5. BLK-002  →  Idempotency_Key must exist before M-BOOKING-CREATION is built
6. BLK-008  →  Stripe endpoint URL needed to configure M-STRIPE-DEPOSIT
7. BLK-004  →  AI_Prompt_Versions schema needed before M-BRAND-ROUTER reads it
8. BLK-006  →  Make_Scenarios table must be in production base before M-AUDIT-LOGGER
9. BLK-005  →  D7_Review_Eligible formula (lowest Stage 1 urgency — document for Stage 2)
```

---

## BLK-001 — Environment Field Missing on Most Tables

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-001 |
| **Severity** | CRITICAL |
| **Owner** | Will |
| **Estimated Effort** | 45–60 minutes |
| **Status** | OPEN |
| **Dependency** | ALL Stage 1 scenarios |

### Description
The `Environment` field (Single Select: `production` / `sandbox` / `test`) is absent from the majority of Airtable tables. Without this field, Make.com scenarios operating in test/sandbox mode cannot be distinguished from production runs. Every record created during development lands in the same dataset as real client records.

### Risk If Not Resolved
- Test leads, test bookings, and test payments will permanently contaminate live client data.
- Airtable views and reports will include synthetic test records; client-facing data integrity is destroyed.
- If a rollback is required, there is no reliable way to identify and purge test records.
- Stripe test-mode payment records cannot be cross-referenced with Airtable sandbox records.

### Resolution Steps
1. Open Airtable base `appdZ49WqgjRXxA1R`.
2. For **each table listed below**, add a new field:
   - Field Name: `Environment`
   - Field Type: Single Select
   - Options: `production`, `sandbox`, `test`
   - Default Value: `sandbox` (during Stage 1 build; switch to `production` at go-live)
3. Confirm the field appears in the table's field list before proceeding.
4. In Make.com, add a **Set variable** step at the start of every scenario that sets `{{environment}}` from a Make environment variable (not hardcoded).
5. In every Create Record or Update Record module, map `Environment` → `{{environment}}`.

### Tables Requiring the Environment Field
| Table | Current Status |
|-------|----------------|
| Requests | MISSING — add immediately |
| Bookings | MISSING — add immediately |
| Clients | MISSING — add immediately |
| Audit_Log | MISSING — add immediately |
| Automation_Health | New table — include in initial schema |
| Concierge_Assignments | MISSING — verify and add |
| Packages | MISSING — verify and add |

### Airtable Changes Required
Add `Environment` (Single Select) with options `production`, `sandbox`, `test` to all tables listed above.

### Make Changes Required
- Add a scenario-level constant in Make Scenario Settings: `ENVIRONMENT = sandbox`
- Pass `{{ENVIRONMENT}}` into every Airtable Create/Update module's `Environment` field.
- All filter steps that read Airtable data must include: `Environment` = `{{ENVIRONMENT}}` to prevent cross-environment reads.

### Resolution Verification
1. Create a test record in Requests with `Environment = sandbox`.
2. Confirm the record is visible in an Airtable view filtered to `Environment = sandbox`.
3. Confirm a separate view filtered to `Environment = production` does NOT show the test record.
4. Run M-LEAD-INTAKE in Make test mode; verify created Requests record has `Environment = sandbox`.

---

## BLK-002 — Idempotency_Key Field Missing on Bookings

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-002 |
| **Severity** | CRITICAL |
| **Owner** | Will |
| **Estimated Effort** | 20 minutes |
| **Status** | OPEN |
| **Dependency** | M-BOOKING-CREATION |

### Description
The `Idempotency_Key` field does not exist on the Bookings table. M-BOOKING-CREATION must write a unique idempotency key when creating a booking record. Without this field, Make.com has no way to detect and prevent duplicate booking records if the scenario retries due to a timeout, network error, or webhook replay.

### Risk If Not Resolved
- A single client submission can produce 2–5 duplicate Booking records.
- Duplicate bookings trigger duplicate Stripe payment intents → double charges.
- Duplicate bookings trigger duplicate confirmation emails → client confusion.
- No mechanism to detect duplicates after the fact without manual audit.

### Resolution Steps
1. Open the Bookings table in base `appdZ49WqgjRXxA1R`.
2. Add field: `Idempotency_Key` — type: Single Line Text, no default.
3. Mark the field as required in Airtable field settings (if supported by Airtable plan).
4. In Make M-BOOKING-CREATION scenario, generate the key before any write:
   ```
   idempotency_key = SHA256( request_id + client_id + charter_date + timestamp_minute )
   ```
   Use Make's built-in `sha256()` or `md5()` function on a concatenated string.
5. Before creating the Booking record, search Bookings where `Idempotency_Key = {{idempotency_key}}`.
6. If a record is found: halt scenario, log to Audit_Log with `Event_Type = DUPLICATE_PREVENTED`, alert via Slack.
7. If no record is found: proceed with Create Record, writing `Idempotency_Key` in the new record.

### Airtable Changes Required
- Bookings table: Add `Idempotency_Key` (Single Line Text)

### Make Changes Required
- M-BOOKING-CREATION: Add SHA256 generation step before Airtable write.
- M-BOOKING-CREATION: Add Airtable Search Records step (Idempotency_Key lookup) before Create Record.
- M-BOOKING-CREATION: Add Router branch: duplicate found → Audit Log + Slack alert → scenario stops.

### Resolution Verification
1. Add `Idempotency_Key` field to Bookings table — confirm field visible.
2. Trigger M-BOOKING-CREATION twice with identical input data.
3. Confirm only one Booking record is created.
4. Confirm the second run creates an Audit_Log record with `Event_Type = DUPLICATE_PREVENTED`.
5. Confirm Slack alert fires on the second (duplicate) run.

---

## BLK-003 — Automations_Paused Field Not Verified in Make Read-First Pattern

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-003 |
| **Severity** | CRITICAL |
| **Owner** | Luciana |
| **Estimated Effort** | 30 minutes (verification) + 2 hours (Make implementation if missing) |
| **Status** | OPEN |
| **Dependency** | ALL Stage 1 scenarios |

### Description
The production architecture requires every Make scenario to begin with a "read-first" check: read a control record from Airtable that contains an `Automations_Paused` boolean. If `true`, the scenario exits immediately without performing any actions. The existence and correct schema of this control record has not been verified. The table housing this field (likely `Automation_Health` or a `System_Config` record) may not exist or may lack the field.

### Risk If Not Resolved
- Operations team has no emergency kill switch for automations.
- If a runaway scenario begins creating duplicate records or sending mass emails, there is no way to halt it from Airtable — every scenario must be individually deactivated inside Make.com.
- During incident response, Make.com access may not be available; Airtable access almost always is.

### Resolution Steps
1. Check if an `Automation_Health` or `System_Config` table exists in base `appdZ49WqgjRXxA1R`.
2. If the table exists: confirm it has a field named `Automations_Paused` (type: Checkbox).
3. If the table or field does NOT exist: create table `Automation_Health` with the schema defined in BLK-003 spec (see below).
4. Create exactly ONE record in `Automation_Health` — this is the global control record.
5. Set `Automations_Paused = false` (unchecked) as the initial state.
6. In every Make scenario, add as Step 1:
   ```
   Module: Airtable — Search Records
   Table: Automation_Health
   Filter: Record_Type = "global_control"
   Fields to retrieve: Automations_Paused, Maintenance_Mode, Emergency_Contact
   ```
7. Add a Filter module immediately after:
   ```
   Condition: {{Automations_Paused}} = false
   If false: Stop scenario execution
   ```
8. Test the kill switch: set `Automations_Paused = true` in Airtable, trigger any scenario, confirm it stops at step 2 without executing further.

### Automation_Health Table Minimum Schema
| Field Name | Type | Notes |
|------------|------|-------|
| Record_Type | Single Line Text | Value: `global_control` |
| Automations_Paused | Checkbox | Default: false |
| Maintenance_Mode | Checkbox | Default: false |
| Paused_By | Single Line Text | Name of person who paused |
| Paused_At | Date/Time | When paused |
| Pause_Reason | Long Text | Why paused |
| Emergency_Contact | Single Line Text | Slack handle to ping |
| Environment | Single Select | production / sandbox / test |

### Airtable Changes Required
- Create `Automation_Health` table with above schema if not present.
- Add `Automations_Paused` checkbox field if table exists but field is missing.
- Create one control record with `Record_Type = global_control`, `Automations_Paused = false`.

### Make Changes Required
- Add Step 1 (Airtable Search) + Step 2 (Filter/Guard) to ALL 8 Stage 1 scenarios.
- This must be implemented BEFORE any scenario is activated in Make.

### Resolution Verification
1. Confirm `Automation_Health` table exists with correct schema.
2. Confirm exactly one record with `Record_Type = global_control` exists.
3. Set `Automations_Paused = true`; trigger M-LEAD-INTAKE; confirm no records are created.
4. Set `Automations_Paused = false`; trigger M-LEAD-INTAKE; confirm normal operation resumes.

---

## BLK-004 — AI_Prompt_Versions Table Has Wrong Schema

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-004 |
| **Severity** | HIGH |
| **Owner** | Will |
| **Estimated Effort** | 2–3 hours |
| **Status** | OPEN |
| **Dependency** | M-BRAND-ROUTER |

### Description
The `AI_Prompt_Versions` table in the main production base (`appdZ49WqgjRXxA1R`) has only 9 fields, but the architecture specification requires 26 fields. The missing fields include version tracking, activation status, prompt body, model parameters, brand scope, and audit metadata. M-BRAND-ROUTER reads from this table to retrieve the active prompt for brand routing logic. Reading from a 9-field table will return null/empty values for the 17 missing fields, silently breaking the brand routing decision.

### Risk If Not Resolved
- M-BRAND-ROUTER may route SSS leads to ME workflows or vice versa.
- Brand routing failures produce incorrect concierge assignments, incorrect email templates, and incorrect Slack alert channels.
- Silent failure: Make scenario will not error; it will silently use default/null values.

### Resolution Steps
1. Open `AI_Prompt_Versions` table in base `appdZ49WqgjRXxA1R`.
2. Document all 9 existing fields (names, types, values).
3. Cross-reference against the 26-field specification in `02_SYSTEMS_AUTOMATIONS__Airtable_Final_Build_Spec_v2.0_PRODUCTION.md`.
4. Add the 17 missing fields per the specification — do NOT delete or rename existing fields without confirming they are not referenced by existing Airtable formulas or native automations.
5. For each new field, add a description in Airtable's field description (hover tooltip) to document purpose.
6. After adding fields, create a test prompt record for each brand (SSS, ME) with all 26 fields populated.
7. Mark one record per brand as `Active = true` (or equivalent activation field).
8. In M-BRAND-ROUTER, confirm the Airtable Search module retrieves all required fields by running a test execution.

### Airtable Changes Required
- `AI_Prompt_Versions`: Add 17 missing fields per architecture spec.
- Key missing fields expected to include: `Prompt_Body`, `Is_Active`, `Brand`, `Model`, `Max_Tokens`, `Temperature`, `Version_Number`, `Activated_At`, `Activated_By`, `Deprecated_At`, `Test_Result`, `Notes`.

### Make Changes Required
- M-BRAND-ROUTER: After adding fields, re-map the Airtable Search output to include newly available fields.
- Validate that brand routing logic uses `Brand` field as a filter when searching active prompts.

### Resolution Verification
1. Confirm `AI_Prompt_Versions` table has exactly 26 fields.
2. Confirm at least one record exists per brand with `Is_Active = true`.
3. Run M-BRAND-ROUTER in Make test mode with a mock SSS lead payload.
4. Confirm the scenario correctly identifies brand = SSS and routes accordingly.
5. Repeat with a mock ME lead payload.

---

## BLK-005 — D7_Review_Eligible Formula Field Missing on Bookings

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-005 |
| **Severity** | HIGH |
| **Owner** | Will |
| **Estimated Effort** | 30 minutes |
| **Status** | OPEN |
| **Dependency** | Stage 2 (not blocking Stage 1 execution, but blocks architecture completeness) |

### Description
The `D7_Review_Eligible` formula field is missing from the Bookings table. This computed field determines whether a booking is 7 days past charter date and eligible for automated review/follow-up workflows. While not directly blocking any Stage 1 scenario execution, its absence creates an architectural gap: Stage 2 scenarios will be built assuming this field exists, and retrofitting it after Stage 2 build begins is significantly more disruptive.

### Risk If Not Resolved
- Stage 2 automated review workflows cannot be built as designed.
- Future Make scenarios that filter on `D7_Review_Eligible = true` will fail silently.
- If added after Stage 2 is built, all Stage 2 scenarios must be re-opened to add the field mapping.

### Resolution Steps
1. Open Bookings table in base `appdZ49WqgjRXxA1R`.
2. Add formula field: `D7_Review_Eligible`
3. Formula:
   ```
   IF(
     AND(
       NOT(IS_ERROR({Charter_Date})),
       DATETIME_DIFF(TODAY(), {Charter_Date}, 'days') >= 7,
       NOT({Review_Sent})
     ),
     TRUE(),
     FALSE()
   )
   ```
   *(Adjust field names to match actual Bookings field names for charter date and review sent flag.)*
4. Confirm formula evaluates correctly on existing Bookings test records.
5. Add a Airtable view: "D7 Review Queue" filtered to `D7_Review_Eligible = true` for Luciana's ops monitoring.

### Airtable Changes Required
- Bookings: Add `D7_Review_Eligible` (Formula, returns Boolean)
- Bookings: Confirm `Review_Sent` (Checkbox) exists; add if missing.

### Make Changes Required
- None for Stage 1.
- Document in Stage 2 build spec that this field is available.

### Resolution Verification
1. Create a test Booking with `Charter_Date` = 8 days ago, `Review_Sent` = false.
2. Confirm `D7_Review_Eligible` evaluates to `true`.
3. Create a test Booking with `Charter_Date` = 3 days ago.
4. Confirm `D7_Review_Eligible` evaluates to `false`.

---

## BLK-006 — Make_Scenarios Table in Non-Production Base

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-006 |
| **Severity** | MEDIUM |
| **Owner** | Luciana |
| **Estimated Effort** | 1–2 hours |
| **Status** | OPEN |
| **Dependency** | M-AUDIT-LOGGER |

### Description
The `Make_Scenarios` reference table (which stores metadata about each Make scenario: name, ID, description, status, version) currently lives in a non-production Airtable base. M-AUDIT-LOGGER reads from this table to enrich audit log entries with scenario context. Reading across bases in Make requires separate Airtable connections and introduces a dependency on a non-production asset.

### Risk If Not Resolved
- M-AUDIT-LOGGER must maintain two Airtable connections (production base + non-production base).
- If the non-production base is deleted, reorganized, or access is revoked, M-AUDIT-LOGGER fails silently.
- Audit log entries may lack scenario context, making incident investigation harder.

### Resolution Steps
1. Identify the current non-production base housing `Make_Scenarios`.
2. Export all existing records from `Make_Scenarios` (CSV or Airtable copy).
3. Create `Make_Scenarios` table in base `appdZ49WqgjRXxA1R` with matching schema.
4. Import existing records.
5. Add any missing Stage 1 scenario records (one per scenario: M-BRAND-ROUTER through M-AUDIT-LOGGER).
6. Update M-AUDIT-LOGGER in Make to point to the new table in the production base.
7. Verify all 8 Stage 1 scenario records are present and have correct data.
8. Archive (do not delete) the non-production table until M-AUDIT-LOGGER is confirmed working.

### Make_Scenarios Table Schema (Minimum)
| Field | Type | Notes |
|-------|------|-------|
| Scenario_Name | Single Line Text | e.g., M-BRAND-ROUTER |
| Make_Scenario_ID | Number | Make.com internal scenario ID |
| Description | Long Text | What the scenario does |
| Status | Single Select | active / inactive / building / deprecated |
| Version | Single Line Text | e.g., 1.0.0 |
| Last_Deployed | Date/Time | |
| Owner | Single Line Text | |
| Environment | Single Select | production / sandbox / test |

### Airtable Changes Required
- Create `Make_Scenarios` table in base `appdZ49WqgjRXxA1R`.
- Populate with 8 Stage 1 scenario records.

### Make Changes Required
- M-AUDIT-LOGGER: Update Airtable connection for Make_Scenarios lookup to use production base ID.

### Resolution Verification
1. Confirm `Make_Scenarios` table exists in `appdZ49WqgjRXxA1R` with 8 records.
2. Run M-AUDIT-LOGGER in test mode; confirm audit log entry includes scenario name and version.

---

## BLK-007 — Circular Trigger Risk on Bookings Table

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-007 |
| **Severity** | HIGH |
| **Owner** | Make builder |
| **Estimated Effort** | 3–4 hours (design + implementation + testing) |
| **Status** | OPEN |
| **Dependency** | M-BOOKING-CREATION |

### Description
The Bookings table has 129 fields. M-BOOKING-CREATION is triggered by Airtable's "record updated" webhook. Because Make writes back to the Bookings record (e.g., updating `Booking_Status`, `Environment`, `Last_Modified_By`), this write will re-trigger the "record updated" webhook, creating an infinite loop of scenario executions. This is a circular trigger — each run creates a new run.

### Risk If Not Resolved
- Infinite scenario execution loop consuming all Make operations quota.
- Exponential Airtable API calls → rate limit throttling (5 req/sec limit hit within seconds).
- Audit log flooded with identical duplicate entries.
- Make.com account may be suspended for API abuse.

### Resolution Steps
1. **Design the trigger guard field**: Add `Make_Processing` (Checkbox) to Bookings table.
2. **Trigger condition**: Configure the Airtable webhook trigger in Make to ONLY fire when `Make_Processing` changes from `false` to `true` (or use a specific trigger field like `Needs_Make_Processing`).
3. **Scenario Step 1**: Immediately upon trigger, write `Make_Processing = true` to the Bookings record — this is the "lock acquired" signal.
4. **Scenario final step**: Write `Make_Processing = false` — "lock released."
5. **Re-trigger guard**: The webhook filter in Make must check: if the trigger was caused by `Make_Processing` field change only, skip. Implement using Make's "watch records" filter limiting to specific fields.
6. **Alternative approach** (simpler): Use a dedicated `Trigger_Field` (Single Line Text) on Bookings. Humans/other automations set `Trigger_Field = "process"`. Make watches ONLY this field. Make clears `Trigger_Field` at the end of its run. Clearing it doesn't re-trigger because Make's filter ignores the field when it becomes empty.
7. **Recommended approach**: Use Make's Airtable module "Watch Records" with field filter limited to `Trigger_Field` only — this prevents the circular trigger at the module configuration level.

### Airtable Changes Required
- Bookings: Add `Make_Processing` (Checkbox, default: false)
- Bookings: Add `Needs_Make_Processing` (Single Line Text) as the trigger field
- Bookings: Add `Last_Make_Run` (Date/Time) for audit trail

### Make Changes Required
- M-BOOKING-CREATION: Configure "Watch Records" trigger with field filter: `Needs_Make_Processing` only.
- M-BOOKING-CREATION: Add guard filter at scenario start: if `Make_Processing = true`, halt (another run is in progress).
- M-BOOKING-CREATION: Write `Make_Processing = true` as first Airtable operation.
- M-BOOKING-CREATION: Write `Make_Processing = false` and clear `Needs_Make_Processing` as final operation.

### Resolution Verification
1. Add all three fields to Bookings.
2. Build the scenario with the trigger guard.
3. Trigger one booking creation.
4. Confirm in Make execution history that exactly ONE scenario run occurs (not a cascade).
5. Confirm `Make_Processing` returns to `false` after scenario completes.
6. Confirm no duplicate Audit_Log entries.

---

## BLK-008 — Stripe Webhook Endpoint URL Not Documented

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-008 |
| **Severity** | BLOCKER |
| **Owner** | Make builder |
| **Estimated Effort** | 1 hour |
| **Status** | OPEN |
| **Dependency** | M-STRIPE-DEPOSIT |

### Description
M-STRIPE-DEPOSIT requires a Stripe webhook to notify Make.com when payment events occur (`payment_intent.succeeded`, `checkout.session.completed`). The Make.com webhook URL for M-STRIPE-DEPOSIT does not yet exist because the scenario has not been created in Make. Without this URL, Stripe cannot be configured to send events, and M-STRIPE-DEPOSIT cannot be tested end-to-end. This is a sequential dependency: Make scenario must be created first to generate the URL.

### Risk If Not Resolved
- M-STRIPE-DEPOSIT cannot receive Stripe events.
- Deposit payments will succeed in Stripe but will NOT trigger booking creation in Airtable.
- No confirmation email or Slack alert fires after payment.
- Entire payment-to-booking flow is broken.

### Resolution Steps
1. Create the M-STRIPE-DEPOSIT scenario skeleton in Make.com (even if only the trigger module is configured).
2. Add a Webhooks module as the trigger: "Custom Webhook."
3. Click "Add" to create a new webhook — Make generates a unique URL in format:
   ```
   https://hook.eu1.make.com/[unique-token]
   ```
   *(Region may vary based on Make account region.)*
4. Copy the generated URL and store it in:
   - This document (update placeholder below)
   - Make scenario settings notes field
   - Airtable `Make_Scenarios` record for M-STRIPE-DEPOSIT
5. Go to Stripe Dashboard → Developers → Webhooks → Add Endpoint.
6. Paste the Make webhook URL.
7. Select events: `payment_intent.created`, `payment_intent.succeeded`, `checkout.session.completed`.
8. Save — Stripe generates a signing secret (format: `whsec_...`).
9. Store signing secret in Make credential vault as `STRIPE_WEBHOOK_SECRET_TEST`.
10. In M-STRIPE-DEPOSIT, add a Stripe webhook signature validation step (see Make Changes below).

**Current Stripe Webhook URL:** `[TO BE GENERATED — update when Make scenario is created]`  
**Stripe Signing Secret:** `[TO BE STORED IN MAKE CREDENTIAL VAULT]`

### Make Changes Required
- Create M-STRIPE-DEPOSIT scenario with Custom Webhook trigger.
- Add Stripe signature validation module immediately after trigger:
  - Retrieve `Stripe-Signature` header from webhook payload.
  - Validate using `STRIPE_WEBHOOK_SECRET_TEST`.
  - If validation fails: return HTTP 400, log to Audit_Log, halt.
- In Make scenario settings: document the webhook URL in the scenario description field.

### Airtable Changes Required
None — this is a Make + Stripe configuration task.

### Resolution Verification
1. Webhook URL is generated and stored.
2. Stripe dashboard shows webhook endpoint as "Active."
3. Run Stripe CLI test: `stripe trigger payment_intent.succeeded`
4. Confirm Make scenario execution log shows the triggered run.
5. Confirm signature validation step passes (HTTP 200 returned to Stripe).
6. Confirm Stripe dashboard shows the test event as "Delivered."

---

## BLK-009 — Airtable-Native Automations Inventory Not Complete

| Field | Value |
|-------|-------|
| **Blocker ID** | BLK-009 |
| **Severity** | HIGH |
| **Owner** | Luciana |
| **Estimated Effort** | 2–3 hours |
| **Status** | OPEN |
| **Dependency** | M-BOOKING-CREATION, M-LEAD-INTAKE |

### Description
Airtable supports native automations (built inside Airtable, separate from Make.com). Before Make.com writes to the Bookings or Requests tables, the team must know which native Airtable automations are active on those tables, what fields they monitor, and what actions they take. An undocumented native automation could: (a) fire in response to Make's write and create conflicting data, (b) overwrite fields that Make just wrote, or (c) trigger an external notification (email/SMS) to a real client during testing.

### Risk If Not Resolved
- Native automation fires on Make's test write → real client email sent during Stage 1 testing.
- Native automation overwrites `Booking_Status` that Make just set → incorrect status in Airtable.
- Circular trigger: native automation updates a field → Make interprets as trigger → Make fires again.
- Data integrity: two systems (Make + native) writing the same fields simultaneously with no coordination.

### Resolution Steps
1. Luciana: Open base `appdZ49WqgjRXxA1R` → Automations tab.
2. Document every active native automation: name, trigger table, trigger condition, actions taken, fields modified, external services called.
3. For each automation on Bookings or Requests: determine if it conflicts with Stage 1 Make scenarios.
4. **Deactivate all native automations that write to fields Make also writes**, or that send external communications (email/SMS).
5. Create a `Native_Automations_Inventory.md` document listing each automation with: Name, Table, Trigger, Actions, Status (active/deactivated for Stage 1), Reactivation Condition.
6. Share inventory with Make builder before M-BOOKING-CREATION or M-LEAD-INTAKE build begins.
7. Flag any native automations that MUST remain active for business operations — these require coordination logic with Make.

### Airtable Changes Required
- Deactivate conflicting native automations (not delete — deactivate with a note explaining why).
- Add description to each native automation documenting its purpose and Stage 1 status.

### Make Changes Required
- None until inventory is complete and conflicts are resolved.
- Make builder must review inventory before finalizing M-BOOKING-CREATION field write sequence.

### Resolution Verification
1. `Native_Automations_Inventory.md` document exists with all automations listed.
2. Luciana signs off that all client-facing automations on Bookings/Requests are deactivated for Stage 1.
3. Run Make M-LEAD-INTAKE test; confirm no unexpected Airtable native automations fire.
4. Check Airtable automation run history for any activity during the test window.

---

## Escalation Protocol

If any CRITICAL or BLOCKER item is not resolved within 48 hours of being assigned:
1. Luciana escalates to Will via Slack DM (not channel message).
2. Will has 24 hours to unblock or reassign.
3. If unresolved at 72 hours: Stage 1 build is paused for that scenario until blocker is cleared.
4. Do not proceed with Make scenario construction for any scenario with an open CRITICAL/BLOCKER dependency.

---

*Document last updated: 2026-05-16. Update Status column and add Resolution Date when each blocker is closed.*
