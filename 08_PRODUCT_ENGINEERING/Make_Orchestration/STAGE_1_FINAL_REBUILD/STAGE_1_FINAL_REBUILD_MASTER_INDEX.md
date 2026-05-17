# STAGE 1 FINAL REBUILD — MASTER INDEX

**Status:** READY FOR IMPORT  
**Version:** STAGE 1 FINAL REBUILD  
**Build Date:** May 2026  
**Classification:** Confidential — Internal Use Only  
**Owner:** Will (Founder)  
**Airtable Base:** appdZ49WqgjRXxA1R (She Said Sail)  
**Branch:** claude/stage-1-final-rebuild-f4yZF

---

## WHAT THIS REBUILD CHANGES

This rebuild supersedes the contents of `STAGE_1_FINAL/` with the following improvements:

| Change | Detail |
|--------|--------|
| Merged M-AUDIT-LOGGER + M-SLACK-ALERTS | → New single scenario: M-OPS-LOGGER-ALERTER |
| Removed deprecated Stripe module | stripe:createPaymentLink replaced with HTTP → Stripe API (POST /v1/prices + POST /v1/payment_links) |
| Unified logging+alerting calls | All scenarios now make ONE call to OPS-LOGGER-ALERTER per event (was two calls) |
| Idempotency key on Stripe payment links | Idempotency-Key header added to Module 7 in M-BOOKING-CREATION |
| Cleaner variable naming | deposit_amount_cents, client_full_name, brand_display_name etc. |
| Better safety gate labeling | All gates labeled SAFETY GATE N for debugging clarity |
| Improved notes/deployment markers | All scenarios have detailed deployment instructions in notes field |
| Concierge_Name field write | M-CONCIERGE-ASSIGNMENT now writes concierge name to dedicated field |
| Stripe fields standardized | Stripe_Payment_Intent_ID, Stripe_Payment_Link_URL, Stripe_Payment_Link_ID, Stripe_Price_ID, Deposit_Amount |

---

## DIRECTORY STRUCTURE

```
08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL_REBUILD/
├── STAGE_1_FINAL_REBUILD_MASTER_INDEX.md     ← THIS FILE
│
├── blueprints/                                ← IMPORT THESE INTO MAKE
│   ├── M-OPS-LOGGER-ALERTER.json             ← IMPORT FIRST
│   ├── M-BRAND-ROUTER.json                   ← IMPORT SECOND
│   ├── M-LEAD-INTAKE.json                    ← IMPORT THIRD
│   ├── M-STRIPE-DEPOSIT.json                 ← IMPORT FOURTH
│   ├── M-BOOKING-CREATION.json               ← IMPORT FIFTH
│   ├── M-CONCIERGE-ASSIGNMENT.json           ← IMPORT SIXTH
│   └── M-BOOKING-CONFIRMATION.json           ← IMPORT SEVENTH
│
├── docs/
│   ├── FINAL_IMPORT_ORDER.md                 ← START HERE
│   ├── DEPLOYMENT_GUIDE.md                   ← Pre-deployment checklist
│   ├── REBINDING_GUIDE.md                    ← Per-module rebinding steps
│   ├── WEBHOOK_GUIDE.md                      ← Webhook URL registration
│   ├── TESTING_GUIDE.md                      ← 15-test validation suite
│   ├── ROLLBACK_GUIDE.md                     ← Rollback procedures
│   └── ACTIVATION_SEQUENCE.md               ← Final activation steps
│
├── reference/
│   ├── FINAL_MODULE_REFERENCE.md             ← Module definitions and formulas
│   ├── NATIVE_MODULE_USAGE_MATRIX.md         ← Native vs HTTP usage map
│   └── HTTP_EXCEPTION_MATRIX.md             ← Why HTTP was used where it was
│
├── testing/
│   ├── SANDBOX_TEST_SEQUENCE.md              ← Step-by-step test commands
│   ├── TEST_PAYLOADS.json                    ← Ready-to-use test payloads
│   └── FAILURE_TESTS.md                     ← Failure and safety gate tests
│
└── archive/                                   ← Reserved for deprecated versions
```

---

## BLUEPRINT SCENARIOS

| # | File | Make Name | Trigger | Modules | Status |
|---|------|-----------|---------|---------|--------|
| 1 | M-OPS-LOGGER-ALERTER.json | SSS-OPS-LOGGER-ALERTER | Webhook | 12 | ✅ VALIDATED |
| 2 | M-BRAND-ROUTER.json | SSS-BRAND-ROUTER | Webhook (sync) | 13 | ✅ VALIDATED |
| 3 | M-LEAD-INTAKE.json | SSS-LEAD-INTAKE | Webhook (Webflow) | 9 | ✅ VALIDATED |
| 4 | M-STRIPE-DEPOSIT.json | SSS-STRIPE-DEPOSIT | Webhook (Stripe) | 8 | ✅ VALIDATED |
| 5 | M-BOOKING-CREATION.json | SSS-BOOKING-CREATION | Airtable poll | 13 | ✅ VALIDATED |
| 6 | M-CONCIERGE-ASSIGNMENT.json | SSS-CONCIERGE-ASSIGNMENT | Airtable poll | 10 | ✅ VALIDATED |
| 7 | M-BOOKING-CONFIRMATION.json | SSS-BOOKING-CONFIRMATION | Airtable poll | 11 | ✅ VALIDATED |

**All 7 JSON files parse correctly. No deprecated modules. No invalid placeholders.**

---

## PLACEHOLDER REGISTRY

These are the ONLY placeholders that exist in the blueprints. ALL must be replaced before activation.

| Placeholder | Replace With | Appears In |
|-------------|-------------|------------|
| `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE` | Webhook URL from SSS-OPS-LOGGER-ALERTER Module 1 | All 6 dependent scenarios |
| `PASTE_BRAND_ROUTER_WEBHOOK_URL_HERE` | Webhook URL from SSS-BRAND-ROUTER Module 1 | M-LEAD-INTAKE Module 5 |
| `PASTE_STRIPE_SECRET_KEY_HERE` | `Bearer sk_test_YOUR_KEY` (TEST) or `Bearer sk_live_YOUR_KEY` (LIVE) | M-BOOKING-CREATION Modules 6 and 7 |
| `PASTE_QUO_SMS_API_KEY_HERE` | `Bearer YOUR_QUO_API_KEY` | M-BOOKING-CREATION Module 12, M-BOOKING-CONFIRMATION Module 9 |

---

## CONNECTIONS REQUIRING REBINDING

| Connection | Type | Scenarios |
|------------|------|-----------|
| SSS Airtable PAT | Airtable | ALL 7 |
| SSS Slack | Slack OAuth | M-OPS-LOGGER-ALERTER (modules 8, 10, 12) |
| SSS Gmail (hello@shesaidsail.com) | Gmail OAuth | M-LEAD-INTAKE, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |

HTTP connections (Stripe, Quo SMS) use inline API keys — no Make connection setup needed.

---

## AIRTABLE TABLES USED

| Table Name | Table ID | Used By |
|------------|----------|---------|
| Requests | tblTlSB9CO4dTGodg | M-BRAND-ROUTER, M-LEAD-INTAKE, M-BOOKING-CREATION |
| Bookings | tbl72omPibBkn2hZL | M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| Audit Log | tblrMpTfMk8q1eNHp | M-OPS-LOGGER-ALERTER |
| Concierge_Operators | tblX61IB2qjDmac8l | M-CONCIERGE-ASSIGNMENT |
| Clients | tblr84vRIWC5HmKvo | M-BOOKING-CONFIRMATION |

---

## NEW AIRTABLE FIELDS REQUIRED

Create these fields BEFORE importing scenarios:

| Field | Table | Type | Default |
|-------|-------|------|---------|
| Confirmation_Sent | Bookings | Checkbox | unchecked |
| Concierge_Assigned | Bookings | Checkbox | unchecked |
| Concierge_Name | Bookings | Single line text | — |
| Stripe_Payment_Link_URL | Bookings | URL | — |
| Stripe_Payment_Link_ID | Bookings | Single line text | — |
| Stripe_Price_ID | Bookings | Single line text | — |
| Stripe_Payment_Intent_ID | Bookings | Single line text | — |
| Deposit_Amount | Bookings | Number | — |

---

## DEPLOYMENT READING ORDER

1. `docs/DEPLOYMENT_GUIDE.md` — Pre-deployment checklist
2. `docs/FINAL_IMPORT_ORDER.md` — Step-by-step import with verification gates
3. `docs/REBINDING_GUIDE.md` — Per-module rebinding
4. `docs/WEBHOOK_GUIDE.md` — Webhook URL registration
5. `testing/SANDBOX_TEST_SEQUENCE.md` — Run all tests
6. `testing/FAILURE_TESTS.md` — Verify safety gates
7. `docs/ACTIVATION_SEQUENCE.md` — Go live

---

## WHAT IS NOT IN THIS REBUILD

Stage 1 scope only. The following are NOT included:

- Charter lifecycle sequences (D0–D60 touches) — Stage 2
- Post-charter automation (review requests, referrals) — Stage 2
- Financial reconciliation scenarios — Stage 3
- Intelligence and health monitoring — Stage 4
- Webflow form integration setup — requires human operator action
- Stripe product catalog setup — handled per-booking dynamically
- SMS opt-out compliance implementation — Quo SMS handles via STOP reply

---

## VALIDATION SUMMARY

| Check | Status |
|-------|--------|
| All 7 JSON files parse without errors | ✅ PASS |
| No deprecated `stripe:createPaymentLink` module | ✅ PASS |
| No `stripe:ActionCreatePaymentLink` module | ✅ PASS |
| No native stripe: modules in any blueprint | ✅ PASS |
| All Airtable modules at version 3 | ✅ PASS |
| All placeholders are functional (not in notes only) | ✅ PASS |
| Internal webhook calls use OPS-LOGGER-ALERTER (not split logger+slack) | ✅ PASS |
| M-OPS-LOGGER-ALERTER replaces both M-AUDIT-LOGGER and M-SLACK-ALERTS | ✅ PASS |
| Stripe payment link creation uses HTTP API (two-step) | ✅ PASS |
| Idempotency-Key header present on Stripe payment_links call | ✅ PASS |

---

## FINAL VERDICT

```
╔══════════════════════════════════════════╗
║                                          ║
║     ✅  READY FOR IMPORT                 ║
║                                          ║
║  All 7 blueprints validated.             ║
║  All documentation complete.             ║
║  All tests documented.                   ║
║  Follow FINAL_IMPORT_ORDER.md to deploy. ║
║                                          ║
╚══════════════════════════════════════════╝
```

**Remaining blockers before going LIVE:**
1. Airtable new fields must be created manually (see NEW AIRTABLE FIELDS REQUIRED above)
2. Slack channels must be created manually
3. All connections must be rebound after import
4. All placeholders must be filled in with real values
5. Full 15-test sandbox validation must pass
6. Stripe must be in TEST mode for initial activation
7. Founder Decision record must be created before production activation

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL_REBUILD/STAGE_1_FINAL_REBUILD_MASTER_INDEX.md*
