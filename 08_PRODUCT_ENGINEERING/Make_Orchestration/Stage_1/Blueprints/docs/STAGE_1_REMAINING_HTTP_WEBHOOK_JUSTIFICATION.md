# Stage 1 Remaining HTTP Modules and Webhooks — Justification
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** PRODUCTION REFERENCE

---

## Purpose

Every HTTP module and webhook trigger that remains in Stage 1 blueprints is documented here with its full justification. No HTTP module or webhook is present without a reason.

---

## Webhook Triggers (Custom Webhooks — Kept)

### 1. M-AUDIT-LOGGER — Inbound Webhook Trigger

**Module:** `gateway:CustomWebHook`
**Justification:** M-AUDIT-LOGGER is a fire-and-forget audit sink called by every other scenario. There is no native Make "receive call from another scenario" module. The custom webhook is the standard and correct pattern for inter-scenario communication. The webhook URL must be restricted to Make's own IP ranges in production.
**Risk:** Low. Internal only. No external client exposure.
**Alternative considered:** None. This pattern is required.

---

### 2. M-BRAND-ROUTER — Inbound Webhook Trigger

**Module:** `gateway:CustomWebHook`
**Justification:** M-BRAND-ROUTER is called by M-LEAD-INTAKE after a new lead record is created in Airtable. The trigger must receive the request_id and inquiry data. No native Make cross-scenario module exists. Webhook is the standard pattern.
**Risk:** Low. Internal only. Called only by M-LEAD-INTAKE.
**Alternative considered:** None.

---

### 3. M-LEAD-INTAKE — Squarespace Form Webhook Trigger

**Module:** `gateway:CustomWebHook`
**Justification:** Squarespace has no reliable native Make app for form submissions. The Squarespace platform supports form webhook integration (Storage → Webhook). This is the documented and supported integration pattern. A native Squarespace module in Make exists only for commerce/products and is not applicable to form intake.
**Risk:** Low. Read-only intake. No credentials exposed.
**Alternative considered:** If Squarespace is replaced with Webflow or Typeform, both have native Make modules.

---

### 4. M-SLACK-ALERTS — Inbound Webhook Trigger

**Module:** `gateway:CustomWebHook`
**Justification:** M-SLACK-ALERTS is called by all other scenarios to dispatch operational alerts. Same pattern as M-AUDIT-LOGGER — no native inter-scenario module exists. Webhook is required.
**Risk:** Low. Internal only.

---

### 5. M-STRIPE-DEPOSIT — Stripe Payment Webhook Trigger

**Module:** `gateway:CustomWebHook`
**Justification:**
- Stripe sends payment events as webhooks instantly on payment completion.
- The Make native `stripe:TriggerEvent` uses polling and introduces latency — unacceptable for financial confirmation that must update Airtable and send client confirmation promptly.
- Webhook preserves the full Stripe event object including the `Stripe-Signature` header required for cryptographic verification.
- Stripe's own integration documentation recommends webhook endpoints over polling for payment events.
- Idempotency protection (Stripe can retry failed webhooks) is built into the blueprint.
**Risk:** Medium. External Stripe-originated. Must validate `payment_intent.succeeded` event type (implemented). Must validate `Stripe-Signature` header in Make webhook settings (manual step — see reimport instructions).
**Alternative considered:** `stripe:TriggerEvent` (polling) — rejected due to latency and inability to validate Stripe signature header in polling mode.

---

## HTTP Modules (http:ActionSendData — Kept)

### 6. Inter-Scenario Audit Logger Calls (Multiple Blueprints)

**Present in:** M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION (blocked path variants)
**Module:** `http:ActionSendData` → `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL`
**Justification:** Every scenario must write an immutable audit log entry to M-AUDIT-LOGGER after completing its primary action. Make has no native "call another scenario" module. HTTP POST to M-AUDIT-LOGGER's webhook is the only supported cross-scenario communication pattern. This is a fire-and-forget call — failures do not block the primary scenario flow.
**Risk:** Low. Internal only. Payload contains no secrets — only booking IDs, scenario IDs, outcomes.
**Alternative considered:** Airtable Create Record directly in each scenario. Rejected because: (1) duplicates the Audit Log write logic across 7 scenarios (maintenance burden), (2) M-AUDIT-LOGGER provides centralized audit governance with consistent field mapping and idempotency.

---

### 7. M-LEAD-INTAKE → M-BRAND-ROUTER Inter-Scenario Call

**Present in:** M-LEAD-INTAKE module 6
**Module:** `http:ActionSendData` → `RECONNECT_BRAND_ROUTER_WEBHOOK_URL`
**Justification:** After creating the Airtable Request record, M-LEAD-INTAKE must trigger brand classification. Make has no native way to trigger another scenario. HTTP POST to M-BRAND-ROUTER's webhook is the only pattern available. The brand router runs independently, so a fire-and-forget HTTP call is appropriate.
**Risk:** Low. Internal only. Payload contains request_id and inquiry text — no financial data, no credentials.
**Alternative considered:** Combining brand routing logic directly into M-LEAD-INTAKE. Rejected because M-BRAND-ROUTER is designed to be callable from multiple intake sources (not just Squarespace forms) and must remain a standalone reusable module.

---

### 8. M-CONCIERGE-ASSIGNMENT — Quo SMS (Module 9)

**Present in:** M-CONCIERGE-ASSIGNMENT module 9
**Module:** `http:ActionSendData` → `RECONNECT_QUO_API_ENDPOINT`
**Justification:** Quo SMS has no native Make app. HTTP module is the only integration option. The API key must be stored in Make's credential/variable system — never hardcoded.
**Risk:** Medium. External API call. Client phone number transmitted. Requires secure credential storage.
**Alternative considered:**
- **Twilio:** Has native Make module (`twilio:ActionSendSms`). Requires provider switch — Founder Decision required.
- **OpenPhone:** Has native Make module. Requires provider switch — Founder Decision required.
- **Email-to-SMS bridge:** Degraded capability — not recommended for production client comms.
- **Manual SMS:** Acceptable temporary fallback until Quo integration is validated.

---

### 9. M-BOOKING-CONFIRMATION — Quo SMS (Module 9)

**Present in:** M-BOOKING-CONFIRMATION module 9
**Module:** `http:ActionSendData` → `RECONNECT_QUO_API_ENDPOINT`
**Justification:** Same as M-CONCIERGE-ASSIGNMENT module 9. Quo SMS has no native Make module.
**Risk:** Same as above.
**Alternative considered:** Same as above.

---

## Summary Table

| Blueprint | HTTP Module Purpose | Count | Justified | Risk |
|---|---|---|---|---|
| M-AUDIT-LOGGER | None remaining | 0 | — | — |
| M-BRAND-ROUTER | Audit Logger call | 1 | ✅ | Low |
| M-LEAD-INTAKE | Brand Router call + Audit Logger call | 2 | ✅ | Low |
| M-SLACK-ALERTS | Audit Logger call | 1 | ✅ | Low |
| M-CONCIERGE-ASSIGNMENT | Quo SMS + Audit Logger ×2 (success + blocked) | 3 | ✅ | Med (Quo) / Low (Audit) |
| M-STRIPE-DEPOSIT | Audit Logger call | 1 | ✅ | Low |
| M-BOOKING-CREATION | Audit Logger ×2 (success + blocked) | 2 | ✅ | Low |
| M-BOOKING-CONFIRMATION | Quo SMS + Audit Logger ×2 (success + blocked) | 3 | ✅ | Med (Quo) / Low (Audit) |

**Total HTTP modules remaining:** 13
**HTTP modules with medium risk:** 2 (both Quo SMS — same justification)
**HTTP modules with low risk:** 11 (all inter-scenario audit/routing calls)

---

## Webhook Trigger Count

| Trigger Type | Count | Blueprints |
|---|---|---|
| Inter-scenario (internal only) | 3 | M-AUDIT-LOGGER, M-BRAND-ROUTER, M-SLACK-ALERTS |
| Squarespace form intake | 1 | M-LEAD-INTAKE |
| Stripe payment event | 1 | M-STRIPE-DEPOSIT |

**All 5 webhook triggers are justified. None are removable without replacing the underlying integration pattern.**
