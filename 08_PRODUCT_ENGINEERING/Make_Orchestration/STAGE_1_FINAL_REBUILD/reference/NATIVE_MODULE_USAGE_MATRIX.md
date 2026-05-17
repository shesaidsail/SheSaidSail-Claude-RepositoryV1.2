# NATIVE MODULE USAGE MATRIX — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Documents which modules are native Make integrations vs HTTP fallbacks

---

## MATRIX

| Scenario | Module | Module ID | Native or HTTP | Reason |
|----------|--------|-----------|----------------|--------|
| M-OPS-LOGGER-ALERTER | gateway:CustomWebHook | 1 | NATIVE | Standard Make webhook trigger |
| M-OPS-LOGGER-ALERTER | builtin:BasicFilter | 2 | NATIVE (builtin) | |
| M-OPS-LOGGER-ALERTER | airtable:ActionCreateRecord | 3 | NATIVE | Airtable native v3 module |
| M-OPS-LOGGER-ALERTER | builtin:SetVariables | 4 | NATIVE (builtin) | |
| M-OPS-LOGGER-ALERTER | builtin:BasicFilter | 5 | NATIVE (builtin) | |
| M-OPS-LOGGER-ALERTER | builtin:BasicRouter | 6 | NATIVE (builtin) | |
| M-OPS-LOGGER-ALERTER | slack:ActionPostMessage | 8, 10, 12 | NATIVE | Slack native module — preferred |
| M-BRAND-ROUTER | gateway:CustomWebHook | 1 | NATIVE | |
| M-BRAND-ROUTER | airtable:ActionUpdateRecord | 6, 9 | NATIVE | |
| M-BRAND-ROUTER | http:ActionSendData | 12 | HTTP | Internal webhook call — no native needed |
| M-BRAND-ROUTER | gateway:CustomWebHookRespond | 13 | NATIVE | |
| M-LEAD-INTAKE | gateway:CustomWebHook | 1 | NATIVE | |
| M-LEAD-INTAKE | airtable:SearchRecords | 3 | NATIVE | |
| M-LEAD-INTAKE | http:ActionSendData | 5 | HTTP | Internal webhook call to Brand Router |
| M-LEAD-INTAKE | json:TransformToJSON | 6 | NATIVE (builtin) | Parses Brand Router response |
| M-LEAD-INTAKE | airtable:ActionCreateRecord | 7 | NATIVE | |
| M-LEAD-INTAKE | gmail:ActionSendEmail | 8 | NATIVE | Gmail native module |
| M-LEAD-INTAKE | http:ActionSendData | 9 | HTTP | Internal webhook call to OPS-LOGGER-ALERTER |
| M-STRIPE-DEPOSIT | gateway:CustomWebHook | 1 | NATIVE | |
| M-STRIPE-DEPOSIT | airtable:SearchRecords | 4 | NATIVE | |
| M-STRIPE-DEPOSIT | airtable:ActionUpdateRecord | 7 | NATIVE | |
| M-STRIPE-DEPOSIT | http:ActionSendData | 8 | HTTP | Internal webhook call |
| M-BOOKING-CREATION | airtable:WatchRecords | 1 | NATIVE | Airtable polling trigger |
| M-BOOKING-CREATION | airtable:SearchRecords | 3 | NATIVE | |
| M-BOOKING-CREATION | airtable:ActionCreateRecord | 5 | NATIVE | |
| M-BOOKING-CREATION | http:ActionSendData | 6 | **HTTP** | **Stripe POST /v1/prices — see HTTP Exception Matrix** |
| M-BOOKING-CREATION | http:ActionSendData | 7 | **HTTP** | **Stripe POST /v1/payment_links — see HTTP Exception Matrix** |
| M-BOOKING-CREATION | airtable:ActionUpdateRecord | 9 | NATIVE | |
| M-BOOKING-CREATION | gmail:ActionSendEmail | 11 | NATIVE | |
| M-BOOKING-CREATION | http:ActionSendData | 12 | HTTP | Quo SMS API — no native module available |
| M-BOOKING-CREATION | http:ActionSendData | 13 | HTTP | Internal webhook call |
| M-CONCIERGE-ASSIGNMENT | airtable:WatchRecords | 1 | NATIVE | |
| M-CONCIERGE-ASSIGNMENT | airtable:SearchRecords | 4 | NATIVE | |
| M-CONCIERGE-ASSIGNMENT | airtable:ActionUpdateRecord | 7 | NATIVE | |
| M-CONCIERGE-ASSIGNMENT | http:ActionSendData | 8, 10 | HTTP | Internal webhook calls |
| M-BOOKING-CONFIRMATION | airtable:WatchRecords | 1 | NATIVE | |
| M-BOOKING-CONFIRMATION | airtable:GetRecord | 6 | NATIVE | |
| M-BOOKING-CONFIRMATION | gmail:ActionSendEmail | 8 | NATIVE | |
| M-BOOKING-CONFIRMATION | http:ActionSendData | 9 | HTTP | Quo SMS API |
| M-BOOKING-CONFIRMATION | airtable:ActionUpdateRecord | 10 | NATIVE | |
| M-BOOKING-CONFIRMATION | http:ActionSendData | 11 | HTTP | Internal webhook call |

---

## SUMMARY

| Category | Count | Notes |
|----------|-------|-------|
| Native Airtable modules | 17 | All at version 3 |
| Native Slack modules | 3 | slack:ActionPostMessage only |
| Native Gmail modules | 3 | gmail:ActionSendEmail |
| Native Make gateway/builtin | 20+ | Webhooks, filters, routers, set vars |
| HTTP exceptions (Stripe) | 2 | Required — no stable native Stripe payment link module |
| HTTP exceptions (Quo SMS) | 2 | Required — no native Quo SMS module in Make |
| HTTP exceptions (internal) | 8 | Internal webhook calls between scenarios |

---

## DEPRECATED MODULES REMOVED

| Module | Status | Replaced With |
|--------|--------|--------------|
| `stripe:createPaymentLink` | REMOVED — deprecated | `http:ActionSendData` to POST /v1/prices + POST /v1/payment_links |
| `stripe:ActionCreatePaymentLink` | NEVER USED — forbidden | `http:ActionSendData` |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — NATIVE_MODULE_USAGE_MATRIX.md*
