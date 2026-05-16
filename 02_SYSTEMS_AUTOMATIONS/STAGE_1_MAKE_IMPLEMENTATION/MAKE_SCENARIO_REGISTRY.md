# MAKE_SCENARIO_REGISTRY — Stage 1 Implementation
# She Said Sail + Mare Executive

**Document Version:** 1.0
**Status:** ACTIVE — PENDING BUILD
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Scope:** Stage 1 Make Automation — All 8 Scenarios
**Classification:** Confidential — Internal Use Only
**Constitutional Authority:** 00_LOCKED_GOVERNANCE__Founder_Control_and_AI_Authority_Framework_v2.0_LOCKED
**Systems Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION

> **Registry Purpose:** This document is the official source of truth for all Stage 1 Make.com scenarios for She Said Sail and Mare Executive. Every scenario that is built, tested, or deployed must be registered here before it touches any Airtable record. This registry governs scenario identity, dependency, data flow, error handling classification, idempotency keys, and rollback procedures. No scenario reaches production without a completed registry entry.

---

## TABLE OF CONTENTS

| Section | Content |
|---------|---------|
| 1 | Make Folder Structure |
| 2 | Stage 1 Scenario Registry — Master Table |
| 3 | Scenario Detail Sheets (S1–S8) |
| 4 | Scenario Dependency Matrix |
| 5 | Stage 1 Data Flow Summary |
| 6 | Error Handling Level Definitions |
| 7 | Environment and Deployment Rules |
| 8 | Sandbox Test Tracker |

---

## SECTION 1 — MAKE FOLDER STRUCTURE

All Stage 1 scenarios are organized within the following Make folder hierarchy. This structure is mandatory. No scenario lives at the root level.

```
SSS-ME/
  └── Stage 1 — Lead-to-Booking Pipeline/
        ├── M-BRAND-ROUTER
        ├── M-LEAD-INTAKE
        ├── M-SLACK-ALERTS
        ├── M-CONCIERGE-ASSIGNMENT
        ├── M-STRIPE-DEPOSIT
        ├── M-BOOKING-CREATION
        ├── M-BOOKING-CONFIRMATION
        └── M-AUDIT-LOGGER
  └── Stage 2 — Charter Lifecycle/ (future)
  └── Stage 3 — Post-Charter Intelligence/ (future)
  └── _Shared Connections/ (connection store — no scenarios live here)
  └── _Sandbox/ (parallel sandbox copies — tagged SANDBOX in all Airtable writes)
```

**Naming Convention:** All scenario names use uppercase with hyphens. The `M-` prefix is mandatory on all SSS-ME scenarios. This prefix prevents collision with any future Webflow, Stripe, or third-party automation layers that may also use Make.

---

## SECTION 2 — STAGE 1 SCENARIO REGISTRY — MASTER TABLE

| # | Scenario Name | Scenario ID | Status | Trigger Type | Est. Modules | Error Level | Sandbox Status | Production Status |
|---|--------------|-------------|--------|-------------|-------------|------------|----------------|-------------------|
| 1 | M-BRAND-ROUTER | PENDING-REGISTRATION | PENDING BUILD | Called by scenario | 6 | L2 | PENDING | NOT LIVE |
| 2 | M-LEAD-INTAKE | PENDING-REGISTRATION | PENDING BUILD | Webhook (HTTP POST) | 12 | L3 | PENDING | NOT LIVE |
| 3 | M-SLACK-ALERTS | PENDING-REGISTRATION | PENDING BUILD | Called by scenario | 5 | L2 | PENDING | NOT LIVE |
| 4 | M-CONCIERGE-ASSIGNMENT | PENDING-REGISTRATION | PENDING BUILD | Airtable Watch | 10 | L3 | PENDING | NOT LIVE |
| 5 | M-STRIPE-DEPOSIT | PENDING-REGISTRATION | PENDING BUILD | Called by scenario | 9 | L3 | PENDING | NOT LIVE |
| 6 | M-BOOKING-CREATION | PENDING-REGISTRATION | PENDING BUILD | Called by scenario | 14 | L3 | PENDING | NOT LIVE |
| 7 | M-BOOKING-CONFIRMATION | PENDING-REGISTRATION | PENDING BUILD | Airtable Watch | 8 | L2 | PENDING | NOT LIVE |
| 8 | M-AUDIT-LOGGER | PENDING-REGISTRATION | PENDING BUILD | Called by scenario | 7 | L1 | PENDING | NOT LIVE |

> **PENDING-REGISTRATION:** Scenario IDs are assigned by Make upon scenario creation. Replace each instance with the actual Make scenario ID (format: numeric, e.g., 4829371) immediately upon creation. The scenario ID is required in the Audit Log `Source_Scenario_ID` field for every write this registry governs.

---

## SECTION 3 — SCENARIO DETAIL SHEETS

---

### S1 — M-BRAND-ROUTER

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-BRAND-ROUTER |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-BRAND-ROUTER |
| **Status** | PENDING BUILD |
| **Trigger Type** | Called by scenario (subflow — no independent trigger) |
| **Trigger Details** | Invoked by M-LEAD-INTAKE immediately after webhook payload is parsed. Receives: `lead_email`, `inquiry_text`, `referral_source`, `requested_package`, `utm_source`. |
| **Estimated Module Count** | 6 |
| **Error Handling Level** | L2 — Log failure + retry once + alert Luciana via Slack on second failure |
| **Idempotency Key** | `Request_ID` (passed in from M-LEAD-INTAKE) — brand classification is idempotent by definition; re-classification of same request must yield same result or trigger human review |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Read AI_Prompt_Versions for current brand router prompt | SSS-Airtable-Production |
| Anthropic API (Claude) | Brand classification inference | SSS-Claude-API |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| AI_Prompt_Versions | tbl0FJkA1E6a70cxX | Content, Version, Brand, Make_Variable_Name | Retrieve active M-BRAND-ROUTER system prompt |

**Airtable Tables Written:** None. M-BRAND-ROUTER is read-only. It returns a structured JSON object to the calling scenario.

**Classification Logic:**

| Signal | SSS Indicator | ME Indicator |
|--------|--------------|-------------|
| Package reference | Sunset Sail, Bachelorette, Birthday, Girls Trip | Corporate Charter, Executive Retreat, Client Entertainment |
| Group context | Personal celebration, friends, romance | Client, team, board, executives |
| Referral source | Instagram, TikTok, organic | LinkedIn, Google Business, referral from corporate client |
| Inquiry tone | Emotional, experiential | Professional, efficiency-focused |
| UTM parameter | utm_source=sss or sss-specific campaign | utm_source=me or me-specific campaign |

**Output Structure (returned to calling scenario):**

```json
{
  "brand": "SSS | ME",
  "confidence_score": 0-100,
  "classification_basis": "string — primary signal used",
  "prompt_version_id": "AIV-NNNN",
  "requires_human_review": true | false
}
```

If `confidence_score < 70` or `requires_human_review = true`: M-BRAND-ROUTER writes an escalation flag and M-LEAD-INTAKE routes the request to Luciana for manual brand assignment before proceeding.

**Downstream Triggers:** Returns classification result to M-LEAD-INTAKE. Does not independently trigger any downstream scenario.

**Rollback Procedure:**
1. Identify affected Request records via Audit Log filter: `Source_Scenario = M-BRAND-ROUTER` + `Timestamp` range.
2. Manually update `Brand` field on affected Request records to correct value.
3. Update `Agent_Status` to `HUMAN_REVIEW` on all affected records.
4. Alert Luciana via Slack DM with list of affected REQ IDs.
5. Trigger M-SLACK-ALERTS with rollback notification payload.
6. Log Founder Decision record: FD-type ROLLBACK with affected record count and correction applied.
7. Root-cause the misclassification and update M-BRAND-ROUTER prompt via AI_Prompt_Versions version bump before re-enabling.

**Notes / Blockers:**
- AI_Prompt_Versions table in main base (tbl0FJkA1E6a70cxX) is currently under-spec (9 fields). The brand router prompt must be loaded from this table after schema upgrade is complete. **BLOCKER: Do not build M-BRAND-ROUTER until AI_Prompt_Versions schema upgrade is confirmed.**
- Confidence threshold of 70 is the recommended baseline. Will may adjust after first 50 classifications.

---

### S2 — M-LEAD-INTAKE

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-LEAD-INTAKE |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-LEAD-INTAKE |
| **Status** | PENDING BUILD |
| **Trigger Type** | Webhook — HTTP POST |
| **Trigger Details** | Make custom webhook URL assigned on creation. Webhook receives POST from: Webflow form submission (primary), direct API POST from SSS/ME website contact forms, or manual test payloads via Postman. Header must include `Authorization: Bearer {MAKE_WEBHOOK_SECRET}`. Webhook secret validated as first step before any processing. |
| **Estimated Module Count** | 12 |
| **Error Handling Level** | L3 — Log failure + retry twice + alert Luciana + create Founder Decision on 4th failure |
| **Idempotency Key** | `webhook_payload.email` + `webhook_payload.charter_date` + `webhook_payload.submission_timestamp` — composite key. If a Request with identical composite key exists and was created within the last 60 minutes, M-LEAD-INTAKE skips record creation and logs a duplicate detection event to Audit Log. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Read Clients table (dedup check); write Requests table; write Clients table if new | SSS-Airtable-Production |
| Make Webhook | Incoming POST receiver | Native — no connection object required |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| Clients | tblr84vRIWC5HmKvo | Email, Name, Phone, CLT_ID | Duplicate client detection before record creation |
| Requests | tblTlSB9CO4dTGodg | Email, Charter_Date, Created_At | Idempotency check — prevent duplicate Request records |

**Airtable Tables Written:**

| Table | Table ID | Operation | Key Fields Written |
|-------|----------|-----------|-------------------|
| Requests | tblTlSB9CO4dTGodg | CREATE | See Field Mapping Registry (AIRTABLE_FIELD_MAPPING_REGISTRY.md — Section 2) |
| Clients | tblr84vRIWC5HmKvo | CREATE (new client) or SKIP (existing) | Name, Email, Phone, Brand, Source_System, Environment |

**Downstream Triggers:**

1. Calls M-BRAND-ROUTER (subflow) — passes webhook payload for brand classification.
2. On brand classification returned: writes `Brand` field to Request record.
3. Triggers M-SLACK-ALERTS — passes REQ ID, brand, client name, charter date, and request summary.
4. Triggers M-AUDIT-LOGGER — passes full action context for Audit Log write.
5. If `confidence_score < 70`: sets `Agent_Status = HUMAN_REVIEW` and alerts Luciana directly.

**Processing Sequence:**
```
1. Receive webhook POST
2. Validate Bearer token → 401 if invalid
3. Validate timestamp (reject if >5 minutes old)
4. Parse and sanitize payload
5. Run idempotency check (Airtable query: matching email + charter_date within 60 min)
6. If duplicate → log to Audit Log → return 200 (do not create record)
7. If new → run client dedup check on Clients table
8. Call M-BRAND-ROUTER subflow with payload
9. Receive brand classification result
10. Create Request record in Airtable (all fields per field mapping registry)
11. If new client → Create Client record in Airtable
12. Trigger M-SLACK-ALERTS
13. Trigger M-AUDIT-LOGGER
14. Return 200 OK to webhook source
```

**Rollback Procedure:**
1. Identify affected Request and Client records via Audit Log: `Source_Scenario = M-LEAD-INTAKE` + `Timestamp` range.
2. Set `Status = VOID` on affected Request records. Do not delete — records are immutable.
3. Set `Agent_Status = HUMAN_REVIEW` on all affected records.
4. If Client records were erroneously created: set `Status = VOID` and note in record.
5. Verify no downstream scenarios were triggered (check Audit Log for M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT entries linked to affected REQ IDs).
6. If downstream records created: execute rollback procedures for those scenarios.
7. Log Founder Decision record: FD-type ROLLBACK.

**Notes / Blockers:**
- Webhook URL must be documented in the SSS Credential Vault (not in this file) and rotated on any suspected compromise.
- Webflow form field names must match payload keys exactly. Any Webflow form change requires a corresponding update to M-LEAD-INTAKE payload mapping.
- **DEPENDENCY:** M-BRAND-ROUTER must exist before M-LEAD-INTAKE can be activated.

---

### S3 — M-SLACK-ALERTS

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-SLACK-ALERTS |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-SLACK-ALERTS |
| **Status** | PENDING BUILD |
| **Trigger Type** | Called by scenario (subflow — called by M-LEAD-INTAKE, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION, and any scenario requiring ops notification) |
| **Trigger Details** | Receives structured notification payload from calling scenario. Minimum required payload: `{alert_type, brand, req_id_or_bk_id, message_body, urgency_level}`. |
| **Estimated Module Count** | 5 |
| **Error Handling Level** | L2 — Log failure + retry once. If Slack alert itself fails, the calling scenario does NOT halt — the failure is logged to Automation_Health table and a backup email is sent to hello@shesaidsail.com. |
| **Idempotency Key** | `alert_type` + `req_id_or_bk_id` + `timestamp_floor_5min` — alerts for the same record within the same 5-minute window are deduplicated. This prevents alert storms on rapid re-triggers. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Slack | Post messages to #sss-ops-alerts | SSS-Slack-Workspace |
| Gmail | Backup alert delivery if Slack fails | SSS-Gmail-hello |

**Slack Channel Routing:**

| Alert Type | Target Channel | Urgency |
|-----------|---------------|---------|
| NEW_LEAD | #sss-ops-alerts | Normal |
| BRAND_MISMATCH | #sss-ops-alerts | High |
| BOOKING_CREATED | #sss-ops-alerts | Normal |
| CONCIERGE_ASSIGNED | #sss-ops-alerts | Normal |
| DEPOSIT_LINK_SENT | #sss-ops-alerts | Normal |
| CONFIRMATION_SENT | #sss-ops-alerts | Normal |
| AUTOMATION_FAILURE | #sss-ops-alerts | High |
| ESCALATION_REQUIRED | #sss-ops-alerts + Luciana DM | Urgent |
| SEV-1 or SEV-2 | #sss-ops-alerts + Will DM | Critical |

**Airtable Tables Read:** None. M-SLACK-ALERTS is stateless — it sends the payload it receives. It does not query Airtable.

**Airtable Tables Written:** None directly. Failure states are written by M-AUDIT-LOGGER.

**Downstream Triggers:** None. M-SLACK-ALERTS is a terminal node in all call chains.

**Rollback Procedure:** Slack messages cannot be retracted programmatically. If an erroneous alert was sent:
1. Luciana manually deletes the Slack message in #sss-ops-alerts.
2. Log the erroneous alert in Audit Log with `Approval_State = VOIDED`.
3. No Airtable records require rollback from this scenario.

**Notes / Blockers:**
- Slack OAuth connection must be configured under the SSS Slack workspace app with `chat:write` and `im:write` scopes.
- Backup Gmail send is critical. Slack has documented downtime history. Do not treat Slack failure as a blocking error.
- Message formatting must use Slack Block Kit, not plain text, for all HIGH and CRITICAL urgency alerts.

---

### S4 — M-CONCIERGE-ASSIGNMENT

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-CONCIERGE-ASSIGNMENT |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-CONCIERGE-ASSIGNMENT |
| **Status** | PENDING BUILD |
| **Trigger Type** | Airtable Watch — field change trigger |
| **Trigger Details** | Watches Requests table (tblTlSB9CO4dTGodg). Triggers when: `Status` field changes to `NEW` AND `Agent_Status` is not already set. Polling interval: 15 minutes (production). Sandbox: 15-minute polling on sandbox base. |
| **Estimated Module Count** | 10 |
| **Error Handling Level** | L3 — Log failure + retry twice + alert Luciana + create Founder Decision on 4th failure |
| **Idempotency Key** | `Request_ID` — if `Concierge_Assigned` field is already populated on the target Request record, skip assignment and log a duplicate prevention event to Audit Log. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Read Concierge_Operators table; read/write Requests table | SSS-Airtable-Production |

**Assignment Logic:**

| Condition | Assignment Action |
|----------|-----------------|
| `Brand = SSS` | Query Concierge_Operators where `Brand_Specialization = SSS` AND `Availability_Status = AVAILABLE` AND `Current_Load < Max_Load` — assign lowest current load |
| `Brand = ME` | Query Concierge_Operators where `Brand_Specialization = ME` AND `Availability_Status = AVAILABLE` AND `Current_Load < Max_Load` — assign lowest current load |
| No available concierge found | Set `Agent_Status = HUMAN_REVIEW`; alert Luciana via M-SLACK-ALERTS with ESCALATION_REQUIRED payload |
| `Agent_Status = HUMAN_REVIEW` already set | Skip — do not overwrite human review state |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| Requests | tblTlSB9CO4dTGodg | Status, Agent_Status, Brand, Concierge_Assigned, Request_ID | Trigger detection + idempotency |
| Concierge_Operators | (migrated from app2FbmVD44BXShyx) | Name, Brand_Specialization, Availability_Status, Current_Load, Max_Load, Email | Assignment selection |

**Airtable Tables Written:**

| Table | Table ID | Operation | Fields Written |
|-------|----------|-----------|---------------|
| Requests | tblTlSB9CO4dTGodg | UPDATE | Concierge_Assigned, Assignment_Timestamp, Agent_Status |

**Downstream Triggers:**
1. Triggers M-AUDIT-LOGGER with assignment event context.
2. Triggers M-SLACK-ALERTS with CONCIERGE_ASSIGNED notification payload.

**Rollback Procedure:**
1. Identify affected Request records via Audit Log: `Source_Scenario = M-CONCIERGE-ASSIGNMENT` + timestamp range.
2. Clear `Concierge_Assigned` field on affected records (set to null/empty).
3. Clear `Assignment_Timestamp`.
4. Reset `Agent_Status` to appropriate prior state.
5. Log rollback event to Audit Log.
6. Notify affected concierge operator via Slack DM (manual step — Luciana executes).

**Notes / Blockers:**
- **BLOCKER:** Concierge_Operators table must be migrated from app2FbmVD44BXShyx into appdZ49WqgjRXxA1R before M-CONCIERGE-ASSIGNMENT can be activated.
- The 15-minute Airtable watch polling interval means assignment may lag by up to 15 minutes from lead creation. This is acceptable for Stage 1. Stage 2 will replace with webhook-based trigger.
- Circular trigger risk: Airtable Watch on Requests → Make updates Requests → do not trigger M-CONCIERGE-ASSIGNMENT again. The idempotency check on `Concierge_Assigned` prevents re-assignment but the watch may still fire. Filter: `Concierge_Assigned IS EMPTY` in the watch condition.

---

### S5 — M-STRIPE-DEPOSIT

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-STRIPE-DEPOSIT |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-STRIPE-DEPOSIT |
| **Status** | PENDING BUILD |
| **Trigger Type** | Called by scenario (subflow — called by M-BOOKING-CREATION after Booking record is confirmed created) |
| **Trigger Details** | Receives: `{booking_id, client_email, client_name, deposit_amount, currency, brand, charter_date, package_name}`. Operates in Stripe TEST MODE for all Sandbox environment records. Switches to Stripe LIVE MODE only when `Environment = Production` AND Founder confirms production activation. |
| **Estimated Module Count** | 9 |
| **Error Handling Level** | L3 — Log failure + retry twice + alert Luciana + pause booking progression on failure |
| **Idempotency Key** | `Booking_ID` — if `Stripe_Payment_Intent_ID` is already populated on the Booking record, skip payment intent creation and return existing link. Stripe Payment Intent IDs are also used as Stripe-side idempotency keys. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Stripe | Create Payment Intent + Payment Link (test mode) | SSS-Stripe-TestMode |
| Airtable | Write Booking and Request records with Stripe data | SSS-Airtable-Production |

**Stripe Configuration:**

| Parameter | Value |
|-----------|-------|
| Mode | TEST (Sandbox) / LIVE (Production — requires explicit activation) |
| Payment Type | Payment Link (URL-based, no card capture in Make) |
| Deposit Calculation | `Package_Price * Deposit_Rate_Pct` — read from Packages table; default 50% if Packages.Deposit_Rate_Pct is null |
| Currency | USD (SSS) / USD (ME) — expand to EUR for future European cities |
| Metadata | `booking_id`, `brand`, `environment`, `make_scenario_id` |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| Bookings | tbl72omPibBkn2hZL | Booking_ID, Package_Price, Stripe_Payment_Intent_ID, Environment | Idempotency + deposit calculation |
| Packages | tblwDw2hkKW5moSr9 | Deposit_Rate_Pct, Package_Price | Deposit amount validation |

**Airtable Tables Written:**

| Table | Table ID | Operation | Fields Written |
|-------|----------|-----------|---------------|
| Bookings | tbl72omPibBkn2hZL | UPDATE | Stripe_Link, Stripe_Payment_Intent_ID, Deposit_Amount, Deposit_Sent_At, Status |
| Requests | tblTlSB9CO4dTGodg | UPDATE | Stripe_Link (reference copy), Deposit_Sent_At |

**Downstream Triggers:**
1. On success: triggers M-BOOKING-CONFIRMATION (passes Stripe_Link and Booking_ID).
2. On success: triggers M-AUDIT-LOGGER.
3. On failure: triggers M-SLACK-ALERTS with AUTOMATION_FAILURE payload; sets Booking `Status = DEPOSIT_PENDING_MANUAL` (non-standard status that flags Luciana for manual Stripe link creation).

**Rollback Procedure:**
1. Identify affected Booking records via Audit Log.
2. Cancel the Stripe Payment Intent via Stripe Dashboard (manual — not automated).
3. Clear `Stripe_Link`, `Stripe_Payment_Intent_ID`, `Deposit_Amount`, `Deposit_Sent_At` on affected Booking records.
4. Reset Booking `Status` to prior value (pre-write value captured in Audit Log `Source_Data` field).
5. Confirm no payment was captured (check Stripe dashboard for the Payment Intent — must show status: `canceled` not `succeeded`).
6. If payment was already captured: escalate immediately to Will. Do not attempt automated rollback on captured payments.
7. Log Founder Decision record: FD-type ROLLBACK.

**Notes / Blockers:**
- **CRITICAL:** Stripe LIVE MODE must never activate until Will explicitly confirms production readiness. The `Environment` field check is the gating condition. Double-check this logic during sandbox testing.
- Test Stripe keys and live Stripe keys must be stored in separate Make connections. Never store both in the same connection object.

---

### S6 — M-BOOKING-CREATION

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-BOOKING-CREATION |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-BOOKING-CREATION |
| **Status** | PENDING BUILD |
| **Trigger Type** | Called by scenario (subflow — called by M-LEAD-INTAKE after Request record is created and brand classification is confirmed) |
| **Trigger Details** | Receives: `{req_id, brand, client_id, charter_date, group_size, package_id, city, concierge_assigned, environment}`. Booking is only created when: Request Status = NEW AND Brand is confirmed AND minimum required fields are populated. |
| **Estimated Module Count** | 14 |
| **Error Handling Level** | L3 — Log failure + retry twice + alert Luciana + create Founder Decision on 4th failure |
| **Idempotency Key** | `Request_ID` — if a Booking record with `Source_Request_ID = req_id` already exists, skip creation and return existing `Booking_ID`. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Read Request/Client/Package; write Bookings; update Requests | SSS-Airtable-Production |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| Requests | tblTlSB9CO4dTGodg | All intake fields | Source data for Booking creation |
| Clients | tblr84vRIWC5HmKvo | Client_ID, Name, Email, Phone, HV_Client | Link client record to booking |
| Packages | tblwDw2hkKW5moSr9 | Package_Price, Deposit_Rate_Pct, Package_Name, Duration | Pricing data for booking |
| Bookings | tbl72omPibBkn2hZL | Source_Request_ID | Idempotency check |

**Airtable Tables Written:**

| Table | Table ID | Operation | Fields Written |
|-------|----------|-----------|---------------|
| Bookings | tbl72omPibBkn2hZL | CREATE | Full field set — see AIRTABLE_FIELD_MAPPING_REGISTRY.md Section 3 |
| Requests | tblTlSB9CO4dTGodg | UPDATE | Status → BOOKING_CREATED, Linked_Booking_ID, Updated_At |

**Processing Sequence:**
```
1. Receive payload from M-LEAD-INTAKE
2. Run idempotency check: query Bookings where Source_Request_ID = req_id
3. If existing booking found → return existing Booking_ID → exit
4. Read Request record (full data)
5. Read Client record (link data)
6. Read Package record (pricing data)
7. Generate Booking_ID: BK-YYYY-NNNN (formula-based, but Make sets the human-readable ID field)
8. Generate UUID: RECORD_ID() formula — Airtable auto-generates on create
9. Create Booking record with all required fields
10. Update Request record: Status = BOOKING_CREATED, Linked_Booking_ID
11. Call M-STRIPE-DEPOSIT (subflow) with booking context
12. Call M-AUDIT-LOGGER with creation event
13. Return Booking_ID to M-LEAD-INTAKE
```

**Downstream Triggers:**
1. Calls M-STRIPE-DEPOSIT (subflow — directly after booking record confirmed created).
2. Triggers M-AUDIT-LOGGER with full booking creation event.
3. M-STRIPE-DEPOSIT then triggers M-BOOKING-CONFIRMATION.

**Rollback Procedure:**
1. Identify Booking records created in error via Audit Log.
2. Set `Status = VOID` on affected Booking records. Do not delete.
3. Set `Environment = ROLLBACK` on affected records (custom state for visibility).
4. Revert `Status` on linked Request records to `NEW`.
5. Clear `Linked_Booking_ID` on linked Request records.
6. Execute M-STRIPE-DEPOSIT rollback if a payment intent was created.
7. Execute M-BOOKING-CONFIRMATION rollback if confirmation was sent.
8. Log Founder Decision record: FD-type ROLLBACK with full context.

**Notes / Blockers:**
- Booking_ID sequential numbering (BK-2026-NNNN) requires a counter mechanism. In Stage 1, use Airtable formula `RECORD_ID()` to generate the UUID, and set the human-readable ID via an Airtable automation or a separate counter field. Document the counter mechanism before build.
- **DEPENDENCY:** Packages table must have Deposit_Rate_Pct and Package_Price fields populated before M-BOOKING-CREATION can calculate deposit amounts correctly.

---

### S7 — M-BOOKING-CONFIRMATION

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-BOOKING-CONFIRMATION |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-BOOKING-CONFIRMATION |
| **Status** | PENDING BUILD |
| **Trigger Type** | Airtable Watch — field change trigger (also callable as subflow) |
| **Trigger Details** | Watches Bookings table (tbl72omPibBkn2hZL). Triggers when: `Stripe_Link` is populated AND `Confirmation_Sent = false` (or unchecked). In Stage 1 test mode, sends confirmation to test email address only — never to real client email. |
| **Estimated Module Count** | 8 |
| **Error Handling Level** | L2 — Log failure + retry once + alert Luciana |
| **Idempotency Key** | `Booking_ID` — if `Confirmation_Sent = true` on the target Booking record, skip send and log duplicate prevention event to Audit Log. This is the primary guard against duplicate client-facing sends. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Read Booking + Client data; write confirmation fields | SSS-Airtable-Production |
| Gmail | Send confirmation email (TEST MODE: to test address only in Sandbox) | SSS-Gmail-hello |

**Email Configuration — Stage 1 Test Mode:**

| Parameter | Sandbox Value | Production Value |
|-----------|--------------|-----------------|
| To address | `sss-test@shesaidsail.com` (internal test inbox) | `{Client.Email}` |
| From address | `hello@shesaidsail.com` | `hello@shesaidsail.com` |
| Reply-to | `hello@shesaidsail.com` | `hello@shesaidsail.com` |
| Subject line | `[TEST] Your {Brand} Charter Booking — {Charter_Date}` | `Your {Brand} Charter Booking — {Charter_Date}` |
| Brand voice | SSS template or ME template per Brand field | Same |

**Airtable Tables Read:**

| Table | Table ID | Fields Read | Purpose |
|-------|----------|-------------|---------|
| Bookings | tbl72omPibBkn2hZL | Booking_ID, Brand, Charter_Date, Package_Name, Stripe_Link, Deposit_Amount, Environment, Confirmation_Sent, Client_ID | Confirmation content + idempotency |
| Clients | tblr84vRIWC5HmKvo | Name, Email, Phone | Personalization + send address |

**Airtable Tables Written:**

| Table | Table ID | Operation | Fields Written |
|-------|----------|-----------|---------------|
| Bookings | tbl72omPibBkn2hZL | UPDATE | Confirmation_Sent (checkbox → true), Confirmation_Sent_At (DateTime), Confirmation_Channel (Single Select → Email) |

**Downstream Triggers:**
1. Triggers M-AUDIT-LOGGER with confirmation send event.
2. Triggers M-SLACK-ALERTS with CONFIRMATION_SENT notification.

**Rollback Procedure:**
1. Identify affected Booking records via Audit Log.
2. Set `Confirmation_Sent = false` (uncheck) on affected records.
3. Clear `Confirmation_Sent_At`.
4. Note: Email sends cannot be retracted. If email was sent to a real client in error during sandbox testing, notify Luciana immediately. Luciana sends a follow-up email acknowledging the test email was sent in error.
5. Log Founder Decision record: FD-type ROLLBACK.

**Notes / Blockers:**
- **CRITICAL SANDBOX RULE:** The `Environment` field check must gate all sends. If `Environment != Production`, send to test inbox only. This check is mandatory at the Gmail module level and is not optional.
- Gmail OAuth must be authenticated under `hello@shesaidsail.com` account.

---

### S8 — M-AUDIT-LOGGER

| Attribute | Value |
|-----------|-------|
| **Scenario Name** | M-AUDIT-LOGGER |
| **Scenario ID** | PENDING-REGISTRATION |
| **Make Folder Path** | SSS-ME / Stage 1 — Lead-to-Booking Pipeline / M-AUDIT-LOGGER |
| **Status** | PENDING BUILD |
| **Trigger Type** | Called by scenario (subflow — called by every other Stage 1 scenario after each significant action) |
| **Trigger Details** | Receives a structured audit payload from the calling scenario. Minimum required payload fields: `{triggering_event, source_scenario_id, source_data, output, destination, brand, city, environment, approval_state, model_version, prompt_version}`. |
| **Estimated Module Count** | 7 |
| **Error Handling Level** | L1 — Log failure to Automation_Health table only. M-AUDIT-LOGGER itself does not escalate on failure (escalation would create infinite loop risk). Audit Logger failures are reviewed daily by Luciana via Automation_Health view. |
| **Idempotency Key** | `triggering_event` + `source_scenario_id` + `timestamp_floor_1min` — prevents duplicate Audit Log entries from retry storms. |
| **Sandbox Test Status** | PENDING |
| **Production Status** | NOT LIVE |

**External Connections Required:**

| Connection | Purpose | Make Connection Name |
|-----------|---------|---------------------|
| Airtable | Write Audit Log record | SSS-Airtable-Production |

**Airtable Tables Read:** None. M-AUDIT-LOGGER writes only. It does not query Airtable before writing.

**Airtable Tables Written:**

| Table | Table ID | Operation | Fields Written |
|-------|----------|-----------|---------------|
| Audit Log | tblrMpTfMk8q1eNHp | CREATE | Full Audit Log field set — see AIRTABLE_FIELD_MAPPING_REGISTRY.md Section 5 |

**Immutability Rules:**
- Audit Log records are NEVER updated after creation. Every event creates a NEW record.
- Make's Airtable token for M-AUDIT-LOGGER has CREATE permission on Audit Log only — not UPDATE or DELETE.
- If a correction to an Audit Log entry is needed, a NEW record is created with `Triggering_Event = AUDIT_CORRECTION` and references the original `Log_ID`.

**Downstream Triggers:** None. M-AUDIT-LOGGER is always the terminal node.

**Rollback Procedure:** Audit Log records are immutable and do not roll back. If an erroneous Audit Log record was created:
1. Create a new Audit Log record with `Triggering_Event = AUDIT_VOID` referencing the erroneous record's `Log_ID`.
2. Mark the erroneous record's `Approval_State = VOIDED` (the one exception to immutability — Approval_State may be updated to VOIDED by Will only).
3. Log Founder Decision: FD-type AUDIT_CORRECTION.

**Notes / Blockers:**
- The Audit Log table (tblrMpTfMk8q1eNHp) requires schema expansion before M-AUDIT-LOGGER can write all required fields. Current schema is missing: `Log_ID`, `Source_Scenario_ID`, `Model_Version`, `Prompt_Version`, `Approval_State` fields. **BLOCKER: Audit Log schema upgrade must complete before M-AUDIT-LOGGER goes live.**
- M-AUDIT-LOGGER's Make connection token must be scoped to CREATE-ONLY on the Audit Log table. Do not grant UPDATE or DELETE permissions to this token.

---

## SECTION 4 — SCENARIO DEPENDENCY MATRIX

This matrix documents which scenarios must exist and be operational before each scenario can be activated. A "REQUIRED" dependency means the listed scenario must be in SANDBOX PASSED status before the dependent scenario can enter sandbox testing.

| Scenario | Requires M-BRAND-ROUTER | Requires M-LEAD-INTAKE | Requires M-SLACK-ALERTS | Requires M-CONCIERGE-ASSIGNMENT | Requires M-STRIPE-DEPOSIT | Requires M-BOOKING-CREATION | Requires M-BOOKING-CONFIRMATION | Requires M-AUDIT-LOGGER |
|----------|------------------------|----------------------|------------------------|--------------------------------|--------------------------|---------------------------|--------------------------------|------------------------|
| **M-BRAND-ROUTER** | — | — | — | — | — | — | — | REQUIRED |
| **M-LEAD-INTAKE** | REQUIRED | — | REQUIRED | — | — | REQUIRED | — | REQUIRED |
| **M-SLACK-ALERTS** | — | — | — | — | — | — | — | — |
| **M-CONCIERGE-ASSIGNMENT** | — | — | REQUIRED | — | — | — | — | REQUIRED |
| **M-STRIPE-DEPOSIT** | — | — | — | — | — | — | — | REQUIRED |
| **M-BOOKING-CREATION** | REQUIRED | — | REQUIRED | — | REQUIRED | — | — | REQUIRED |
| **M-BOOKING-CONFIRMATION** | — | — | REQUIRED | — | — | — | — | REQUIRED |
| **M-AUDIT-LOGGER** | — | — | — | — | — | — | — | — |

**Recommended Build Order (respects all dependencies):**

```
Phase A — Foundation (no dependencies):
  1. M-AUDIT-LOGGER
  2. M-SLACK-ALERTS

Phase B — Classification (depends on Phase A):
  3. M-BRAND-ROUTER

Phase C — Core Pipeline (depends on Phases A + B):
  4. M-STRIPE-DEPOSIT
  5. M-BOOKING-CONFIRMATION
  6. M-CONCIERGE-ASSIGNMENT

Phase D — Orchestrator (depends on all prior phases):
  7. M-BOOKING-CREATION
  8. M-LEAD-INTAKE (final — activates full pipeline)
```

---

## SECTION 5 — STAGE 1 DATA FLOW SUMMARY

```
INBOUND WEBHOOK (Webflow / website form)
          │
          ▼
  M-LEAD-INTAKE ─────────────► M-BRAND-ROUTER (subflow)
          │                            │
          │                     Brand Classification
          │                    (SSS or ME + confidence)
          │                            │
          │◄───────────────────────────┘
          │
          ├─────────────────────────────────────────────────────┐
          │                                                     │
          ▼                                                     ▼
  CREATE Request record (Airtable)               CREATE Client record (if new)
          │
          ├────────────────────────────────────────────────────────────────────┐
          │                                                                    │
          ▼                                                                    ▼
  M-BOOKING-CREATION (subflow)                          M-SLACK-ALERTS (NEW_LEAD)
          │
          ├──────────────────────────────────┐
          │                                  │
          ▼                                  ▼
  CREATE Booking record (Airtable)    UPDATE Request: Status = BOOKING_CREATED
          │
          ▼
  M-STRIPE-DEPOSIT (subflow)
          │
          ▼
  CREATE Stripe Payment Intent + Link (TEST MODE)
          │
          ▼
  UPDATE Booking: Stripe_Link, Payment_Intent_ID, Deposit_Amount, Deposit_Sent_At
          │
          ▼
  M-BOOKING-CONFIRMATION (subflow from M-STRIPE-DEPOSIT)
          │
          ├──────────────────────────────────┐
          │                                  │
          ▼                                  ▼
  SEND confirmation email (TEST inbox)   UPDATE Booking: Confirmation_Sent = true
          │
          └──────────────────────────────────────────────────────────────────┐
                                                                             │
PARALLEL (runs at each stage event):                                        │
  M-CONCIERGE-ASSIGNMENT ◄─── Watches Requests (Airtable Watch)            │
          │                                                                  │
          ▼                                                                  │
  UPDATE Request: Concierge_Assigned, Assignment_Timestamp, Agent_Status    │
          │                                                                  │
          ▼                                                                  │
  M-SLACK-ALERTS (CONCIERGE_ASSIGNED)                                       │
                                                                             │
ALL ACTIONS → M-AUDIT-LOGGER ◄──────────────────────────────────────────────┘
          │
          ▼
  CREATE Audit Log record (tblrMpTfMk8q1eNHp)
```

**Data Objects Flowing Through Stage 1:**

| Object | Created By | Written To | Consumed By |
|--------|-----------|-----------|------------|
| Webhook Payload | External (Webflow) | M-LEAD-INTAKE (memory) | M-BRAND-ROUTER, M-LEAD-INTAKE |
| Brand Classification | M-BRAND-ROUTER | Request.Brand | M-LEAD-INTAKE, M-BOOKING-CREATION |
| Request Record | M-LEAD-INTAKE | Requests table | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION |
| Client Record | M-LEAD-INTAKE | Clients table | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Booking Record | M-BOOKING-CREATION | Bookings table | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| Stripe Payment Link | M-STRIPE-DEPOSIT | Bookings.Stripe_Link | M-BOOKING-CONFIRMATION |
| Confirmation Email | M-BOOKING-CONFIRMATION | Gmail (sent) | End client (or test inbox) |
| Audit Log Record | M-AUDIT-LOGGER | Audit Log table | Human review, compliance |

---

## SECTION 6 — ERROR HANDLING LEVEL DEFINITIONS

Per Systems Intelligence Architecture v2.0, Section 3.4:

| Level | Label | Response Sequence | Scenarios Using |
|-------|-------|------------------|----------------|
| **L1** | Log Only | Failure logged to Automation_Health. No retry. No alert. Human reviews daily. | M-AUDIT-LOGGER |
| **L2** | Log + Retry + Alert Ops | Log to Automation_Health → retry once after 2 min → alert Luciana via Slack if second failure | M-BRAND-ROUTER, M-SLACK-ALERTS, M-BOOKING-CONFIRMATION |
| **L3** | Full Escalation | Log → retry after 2 min → retry after 5 min → alert Luciana after 3rd failure → alert Will + pause scenario + create Founder Decision (SEV-2) after 4th failure | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION |
| **L4** | Emergency | Immediate Will DM + SEV-1 Founder Decision + scenario halt. Reserved for financial errors, data corruption, or security events. | Not used in Stage 1 — escalated from L3 on persistence |

**Error Logging Standard:** All errors write to Automation_Health table with: `Scenario_Name`, `Scenario_ID`, `Error_Code`, `Error_Message`, `Affected_Record_ID`, `Retry_Count`, `Timestamp`, `Resolution_Status`.

---

## SECTION 7 — ENVIRONMENT AND DEPLOYMENT RULES

| Rule | Detail |
|------|--------|
| Sandbox Airtable base | All sandbox scenario testing writes to a designated sandbox base — NEVER to appdZ49WqgjRXxA1R or apprDKQtV2GInThwE |
| Environment field | Every Airtable record created by Make in sandbox must have `Environment = Sandbox` |
| Stripe mode | Sandbox scenarios use Stripe test mode keys exclusively |
| Gmail sends | Sandbox scenarios route all email sends to internal test inbox |
| Production activation | No scenario reaches production without: (1) SANDBOX PASSED status in this registry, (2) Founder approval documented as Founder Decision record, (3) Rollback procedure validated in sandbox |
| Scenario ID documentation | Scenario IDs must be updated in this registry within 24 hours of scenario creation in Make |
| Deployment log | Every production activation creates a Deployment Log record in Airtable with: Scenario_Name, Scenario_ID, Activated_At, Activated_By, Rollback_Procedure_Reference |

---

## SECTION 8 — SANDBOX TEST TRACKER

| Scenario | Sandbox Test Date | Tester | Test Cases Passed | Test Cases Failed | Blockers Resolved | SANDBOX PASSED Date |
|----------|------------------|--------|-------------------|-------------------|------------------|---------------------|
| M-AUDIT-LOGGER | PENDING | — | — | — | — | — |
| M-SLACK-ALERTS | PENDING | — | — | — | — | — |
| M-BRAND-ROUTER | PENDING | — | — | — | — | — |
| M-STRIPE-DEPOSIT | PENDING | — | — | — | — | — |
| M-BOOKING-CONFIRMATION | PENDING | — | — | — | — | — |
| M-CONCIERGE-ASSIGNMENT | PENDING | — | — | — | — | — |
| M-BOOKING-CREATION | PENDING | — | — | — | — | — |
| M-LEAD-INTAKE | PENDING | — | — | — | — | — |

**Minimum Test Cases Required Before SANDBOX PASSED:**

| Scenario | Required Test Cases |
|----------|-------------------|
| M-BRAND-ROUTER | SSS lead (clear), ME lead (clear), ambiguous lead (escalation), missing payload fields |
| M-LEAD-INTAKE | New client + new lead, returning client + new lead, duplicate submission (idempotency), missing required fields, invalid Bearer token |
| M-SLACK-ALERTS | All 5 alert types, Slack failure → Gmail backup, deduplication within 5-min window |
| M-CONCIERGE-ASSIGNMENT | Available concierge (SSS), available concierge (ME), no available concierge (escalation), duplicate trigger (idempotency) |
| M-STRIPE-DEPOSIT | Test payment intent creation, duplicate booking (idempotency), package pricing lookup, environment gate (sandbox → test mode only) |
| M-BOOKING-CREATION | Full end-to-end creation, duplicate request (idempotency), missing package data, Stripe subflow failure |
| M-BOOKING-CONFIRMATION | SSS template send (test inbox), ME template send (test inbox), duplicate trigger (idempotency), environment gate |
| M-AUDIT-LOGGER | Write Audit Log record, duplicate within 1-min window (idempotency), missing required payload fields |
