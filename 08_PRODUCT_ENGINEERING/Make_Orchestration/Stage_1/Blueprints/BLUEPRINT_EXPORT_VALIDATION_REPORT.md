# BLUEPRINT EXPORT VALIDATION REPORT

**Generated:** 2026-05-16  
**Stage:** Stage 1 — Core Automation Layer  
**Status:** BLUEPRINT FILES SUCCESSFULLY GENERATED  
**Environment:** Production-ready (connections require rebinding after import)

---

## FILE TREE

```
08_PRODUCT_ENGINEERING/
└── Make_Orchestration/
    └── Stage_1/
        └── Blueprints/
            ├── BLUEPRINT_EXPORT_VALIDATION_REPORT.md  ← this file
            └── json_blueprints/
                ├── M-AUDIT-LOGGER.blueprint.json
                ├── M-BOOKING-CONFIRMATION.blueprint.json
                ├── M-BOOKING-CREATION.blueprint.json
                ├── M-BRAND-ROUTER.blueprint.json
                ├── M-CONCIERGE-ASSIGNMENT.blueprint.json
                ├── M-LEAD-INTAKE.blueprint.json
                ├── M-SLACK-ALERTS.blueprint.json
                └── M-STRIPE-DEPOSIT.blueprint.json
```

---

## FILE INVENTORY

| # | Filename | Repository Path | Bytes | JSON Valid | Import Ready |
|---|----------|-----------------|-------|------------|--------------|
| 1 | M-AUDIT-LOGGER.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-AUDIT-LOGGER.blueprint.json` | 7,597 | ✅ VALID | ✅ READY |
| 2 | M-BRAND-ROUTER.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-BRAND-ROUTER.blueprint.json` | 10,601 | ✅ VALID | ✅ READY |
| 3 | M-LEAD-INTAKE.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-LEAD-INTAKE.blueprint.json` | 10,092 | ✅ VALID | ✅ READY |
| 4 | M-SLACK-ALERTS.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-SLACK-ALERTS.blueprint.json` | 12,076 | ✅ VALID | ✅ READY |
| 5 | M-CONCIERGE-ASSIGNMENT.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-CONCIERGE-ASSIGNMENT.blueprint.json` | 13,964 | ✅ VALID | ✅ READY |
| 6 | M-STRIPE-DEPOSIT.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-STRIPE-DEPOSIT.blueprint.json` | 10,698 | ✅ VALID | ✅ READY |
| 7 | M-BOOKING-CREATION.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-BOOKING-CREATION.blueprint.json` | 9,402 | ✅ VALID | ✅ READY |
| 8 | M-BOOKING-CONFIRMATION.blueprint.json | `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-BOOKING-CONFIRMATION.blueprint.json` | 12,949 | ✅ VALID | ✅ READY |

**Total blueprint files created: 8**  
**Total bytes: 87,379**  
**JSON validation failures: 0**

---

## SCENARIO SUMMARIES

### M-AUDIT-LOGGER
- **Trigger:** Inbound webhook (called by all other scenarios)
- **Purpose:** Immutable audit record creation for every Tier A autonomous action
- **Modules:** Webhook → Router → (Write Audit Record | Idempotency Check → Duplicate Block Alert)
- **Idempotency:** Checks for existing record with matching idempotency key before writing
- **Error handling:** Logs to Automation Failures table + Slack #sss-ops-alerts

### M-BRAND-ROUTER
- **Trigger:** Inbound webhook (called by M-LEAD-INTAKE and any brand classification flow)
- **Purpose:** Classify every inbound request as SSS or ME before AI proceeds; block cross-brand contamination
- **Modules:** Webhook → Router → (SSS Route | ME Route | Ambiguous — Human Classification)
- **Idempotency:** Writes brand classification to Request record with timestamp
- **Error handling:** Ambiguous brand routes to HUMAN_REVIEW + Slack alert; calls M-AUDIT-LOGGER

### M-LEAD-INTAKE
- **Trigger:** Webflow form submission webhook
- **Purpose:** Create Airtable Request record, send auto-reply email, notify Slack, route to M-BRAND-ROUTER
- **Modules:** Webhook → Auth Filter → Idempotency Check → Create Request → Call M-BRAND-ROUTER → Gmail → Slack → Call M-AUDIT-LOGGER
- **Idempotency:** Checks for existing record with matching form submission ID before creating
- **Error handling:** Logs to Automation Failures + Slack alert

### M-SLACK-ALERTS
- **Trigger:** Inbound webhook (called by all scenarios needing Slack notifications)
- **Purpose:** Centralized Slack alert dispatcher — EMERGENCY / SEV-1 / SEV-2 / APPROVAL_REQUIRED / NEW_LEAD
- **Modules:** Webhook → Router → (5 alert type branches) → Call M-AUDIT-LOGGER
- **Idempotency:** Driven by caller's idempotency_key
- **Error handling:** Downstream-only (callers handle failures)

### M-CONCIERGE-ASSIGNMENT
- **Trigger:** Inbound webhook (called after M-BRAND-ROUTER classification)
- **Purpose:** Assign available broker to a Request record; escalate to human if none available
- **Modules:** Webhook → Idempotency Check → Get Request → Search Brokers → Router → (Assign | Escalate + Approval Queue)
- **Idempotency:** Checks for existing assignment before proceeding
- **Error handling:** Logs to Automation Failures + Slack alert; calls M-AUDIT-LOGGER

### M-STRIPE-DEPOSIT
- **Trigger:** Stripe `payment_intent.succeeded` webhook
- **Purpose:** Process deposit payment, update Booking status to DEPOSIT_PAID, send confirmation email, notify Slack
- **Modules:** Stripe webhook → Event type filter → Metadata filter (deposit) → Idempotency Check → Update Booking → Get Booking → Emergency flag check → Gmail → Slack → Call M-AUDIT-LOGGER
- **Idempotency:** Checks Booking status before updating — prevents duplicate processing
- **Error handling:** Logs failure with Stripe event ID; Slack alert with manual action instruction

### M-BOOKING-CREATION
- **Trigger:** Inbound webhook (called when availability is confirmed by Luciana)
- **Purpose:** Promote a Request record to a Booking record; update Request status to PROMOTED_TO_BOOKING
- **Modules:** Webhook → Idempotency Check → Get Request → Create Booking → Update Request → Call M-SLACK-ALERTS → Call M-AUDIT-LOGGER
- **Idempotency:** Checks for existing Booking linked to same Request before creating
- **Error handling:** Logs to Automation Failures + Slack alert

### M-BOOKING-CONFIRMATION
- **Trigger:** Inbound webhook (called when deposit is confirmed paid)
- **Purpose:** Advance Booking to CONFIRMED status, send confirmation email, handle high-value agreement gate
- **Modules:** Webhook → Get Booking → Status/flag filter → Router → (High-Value Agreement Gate | Standard Confirmation → Update Booking → Gmail → Slack) → Call M-AUDIT-LOGGER
- **Idempotency:** Status filter prevents re-confirming an already-confirmed booking
- **Error handling:** Logs to Automation Failures + Slack alert

---

## CONNECTION REBINDING REQUIRED AFTER IMPORT

Every blueprint uses placeholder connection identifiers. After importing into Make, the following connections must be rebound before any scenario can be activated:

| Placeholder | Connection Type | What to Connect |
|-------------|----------------|-----------------|
| `RECONNECT_AIRTABLE_CONNECTION` | Airtable | She Said Sail Production base — Personal Access Token |
| `RECONNECT_SLACK_CONNECTION` | Slack | She Said Sail workspace OAuth app |
| `RECONNECT_STRIPE_CONNECTION` | Stripe (webhook) | Production webhook signing secret |
| `RECONNECT_GMAIL_CONNECTION` | Gmail | hello@shesaidsail.com OAuth |

---

## WEBHOOK URL REBINDING REQUIRED AFTER IMPORT

All inter-scenario webhook calls and the primary trigger webhook for each scenario use the placeholder `INSERT_WEBHOOK_URL_AFTER_IMPORT`. After import, update each scenario's outbound HTTP module URLs to the live webhook URL assigned by Make for the target scenario.

**Cross-scenario webhook wiring map:**

| Calling Scenario | HTTP Module Target | Connect To |
|------------------|--------------------|------------|
| M-LEAD-INTAKE | Call M-BRAND-ROUTER | M-BRAND-ROUTER trigger webhook URL |
| M-LEAD-INTAKE | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-BRAND-ROUTER | SSS downstream webhook | Downstream SSS processing webhook URL |
| M-BRAND-ROUTER | ME downstream webhook | Downstream ME processing webhook URL |
| M-BRAND-ROUTER | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-CONCIERGE-ASSIGNMENT | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-BOOKING-CREATION | Call M-SLACK-ALERTS | M-SLACK-ALERTS trigger webhook URL |
| M-BOOKING-CREATION | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-STRIPE-DEPOSIT | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-BOOKING-CONFIRMATION | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |
| M-SLACK-ALERTS | Call M-AUDIT-LOGGER | M-AUDIT-LOGGER trigger webhook URL |

---

## AIRTABLE TABLE ID REBINDING

Blueprint modules reference table names as human-readable strings (e.g., `tblRequests`, `tblBookings`). After import, verify Make resolves these correctly against the production base. If Make requires internal table IDs, update each Airtable module with the correct `tblXXXXXXXXXX` IDs from the production base schema.

**Required table bindings:**

| Blueprint Reference | Production Table | Notes |
|--------------------|-----------------|-------|
| `tblRequests` | Requests | Lead/inquiry records |
| `tblBookings` | Bookings | Master booking lifecycle |
| `tblBrokers` | Brokers | Concierge/broker availability |
| `tblClients` | Clients | Client PII records |
| `tblAuditLog` | Audit Log | Immutable action record |
| `tblAutomationFailures` | Automation Failures | Failure detection and retry |
| `tblApprovalQueue` | Approval Queue | Founder decision centralization |

---

## MISSING DEPENDENCY WARNINGS

| Warning | Severity | Resolution |
|---------|----------|------------|
| Stripe webhooks require production signing secret validation — the blueprint includes the webhook module but Stripe-side signing validation must be configured in the Make Stripe app connection | HIGH | Configure Stripe webhook signing secret in Make connection settings before activation |
| M-STRIPE-DEPOSIT references `1.body.data.object.metadata.base_id` and `booking_record_id` — these must be set in the Stripe Payment Intent metadata when creating the payment link | HIGH | Ensure M-BOOKING-CREATION or Stripe payment link generation includes these metadata fields |
| Broker availability lookup in M-CONCIERGE-ASSIGNMENT uses field names (`fldAvailability`, `fldCurrentBookingCount`) that must match the production Brokers table schema exactly | MEDIUM | Verify Brokers table field names match blueprint references before activation |
| Email body templates use single-line `\n` escape sequences — verify Gmail module renders these correctly or switch to HTML mode | LOW | Test with a sandbox booking before production activation |
| `sha256()` function in M-AUDIT-LOGGER payload hash — verify Make supports this function in your plan tier | LOW | Replace with `md5()` if `sha256()` is unavailable |

---

## MAKE IMPORT LIMITATIONS

1. **Connections are not portable.** All connection references will be blank after import and must be manually rebound. This is expected behavior for all Make blueprints.
2. **Webhook URLs are assigned at import time.** Make generates a unique webhook URL for each trigger module upon scenario creation. The `INSERT_WEBHOOK_URL_AFTER_IMPORT` placeholder must be replaced in all HTTP modules that call other scenarios.
3. **Blueprint import does not activate scenarios.** All imported scenarios will be in OFF state. Enable in dependency order: M-AUDIT-LOGGER → M-SLACK-ALERTS → M-BRAND-ROUTER → M-LEAD-INTAKE → M-CONCIERGE-ASSIGNMENT → M-BOOKING-CREATION → M-STRIPE-DEPOSIT → M-BOOKING-CONFIRMATION.
4. **Airtable field references use display names.** If the production Airtable base uses internal field IDs, Make may require re-mapping fields in each Airtable module after import.
5. **Make plan tier must support webhooks and router modules.** Verify your Make plan includes instant webhook triggers and the BasicRouter module.
6. **No secrets or API keys are embedded.** All credentials must be supplied via Make's connection manager after import. This is by design.

---

## IMPORT ORDER (DEPENDENCY-SAFE SEQUENCE)

Import and activate in this order to ensure downstream webhooks are available when upstream scenarios reference them:

```
1. M-AUDIT-LOGGER          — no upstream dependencies
2. M-SLACK-ALERTS          — depends on M-AUDIT-LOGGER
3. M-BRAND-ROUTER          — depends on M-AUDIT-LOGGER
4. M-LEAD-INTAKE           — depends on M-BRAND-ROUTER + M-AUDIT-LOGGER
5. M-CONCIERGE-ASSIGNMENT  — depends on M-AUDIT-LOGGER
6. M-BOOKING-CREATION      — depends on M-SLACK-ALERTS + M-AUDIT-LOGGER
7. M-STRIPE-DEPOSIT        — depends on M-AUDIT-LOGGER
8. M-BOOKING-CONFIRMATION  — depends on M-AUDIT-LOGGER
```

---

## FINAL VERDICT

**BLUEPRINT FILES SUCCESSFULLY GENERATED**

- 8 of 8 required `.blueprint.json` files created
- 8 of 8 files validated as syntactically correct JSON
- 8 of 8 files physically exist in repository
- 0 secrets or API keys embedded
- All placeholder conventions applied per spec
- All files are downloadable from repository
- All files are structured for Make blueprint import compatibility
