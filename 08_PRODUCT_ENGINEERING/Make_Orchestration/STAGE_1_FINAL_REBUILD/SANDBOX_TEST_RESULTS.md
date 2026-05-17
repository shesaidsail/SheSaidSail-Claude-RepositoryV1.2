# SANDBOX TEST RESULTS — STAGE 1 FINAL REBUILD

**Generated:** 2026-05-17  
**Branch:** claude/stage-1-final-rebuild-f4yZF  
**Classification:** Confidential — Internal Use Only

---

## STATUS: PENDING EXECUTION

```
⚠️  TESTS NOT YET RUN
```

Sandbox tests require a live Make.com instance with all 7 scenarios imported and all connections rebound. Claude cannot execute Make scenarios directly. This file is pre-populated with the test structure. The operator must execute each test and record the result.

**Pre-requisites before running any test:**
- [ ] All 7 blueprints imported into Make
- [ ] All connections rebound (Airtable PAT, Slack OAuth, Gmail OAuth)
- [ ] All placeholders replaced with real values
- [ ] Make Slack bot added to all 3 channels
- [ ] Stripe in TEST MODE — `sk_test_` key confirmed
- [ ] Webhook URLs registered in Webflow and Stripe Dashboard
- [ ] Test email address available to receive emails
- [ ] Concierge_Operators table has at least 1 active record for Miami

---

## PHASE 1: Infrastructure Layer (Scenarios 1–2)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 1.1 | OPS-LOGGER: Log only | Audit Log record created, NO Slack | ⬜ | |
| 1.2 | OPS-LOGGER: OPS alert | Audit Log + Slack #sss-ops-alerts 🟢 | ⬜ | |
| 1.3 | OPS-LOGGER: LEAD alert | Audit Log + Slack #sss-lead-intake | ⬜ | |
| 1.4 | OPS-LOGGER: EMERGENCY alert | Audit Log + Slack #sss-emergency-ops 🚨 | ⬜ | |
| 1.5 | BRAND-ROUTER: SSS | Response: brand=SSS, routing_confidence=HIGH | ⬜ | |
| 1.6 | BRAND-ROUTER: ME | Response: brand=ME | ⬜ | |
| 1.7 | BRAND-ROUTER: UNKNOWN | Response: brand=UNKNOWN + Slack WARNING | ⬜ | |

## PHASE 2: Lead Intake (Scenario 3)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 2.1 | LEAD-INTAKE: Full flow | Airtable Request + auto-reply email + Slack LEAD + Audit Log | ⬜ | Use real test email |
| 2.2 | LEAD-INTAKE: Idempotency | Same payload → NO new record, exits at Module 4 | ⬜ | |

## PHASE 3: Stripe Deposit (Scenario 4)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 3.1 | STRIPE-DEPOSIT: Setup | Booking record created manually with Status=DEPOSIT_SENT | ⬜ | Manual Airtable action |
| 3.2 | STRIPE-DEPOSIT: Test webhook | Status=DEPOSIT_PAID + Stripe_Payment_Intent_ID populated + Slack + Audit Log | ⬜ | Via Stripe Dashboard test webhook |

## PHASE 4: Booking Creation (Scenario 5)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 4.1 | BOOKING-CREATION: E2E | Booking created + Stripe price + payment link URL + Status=DEPOSIT_SENT + email + SMS + Audit Log | ⬜ | Verify sk_test_ before running |

## PHASE 5: Concierge Assignment (Scenario 6)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 5.1 | CONCIERGE: Auto-assign | Concierge_Assigned=true + Concierge_Name populated + Slack + Audit Log | ⬜ | Requires active Concierge_Operators record for Miami |

## PHASE 6: Booking Confirmation (Scenario 7)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 6.1 | CONFIRMATION: Send | Gmail + SMS sent + Confirmation_Sent=true + D0 Sent=true + Audit Log | ⬜ | |

## PHASE 7: Safety Gates

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| 7.1 | Automations_Paused gate | NO email/SMS, exits at Module 2 | ⬜ | |
| 7.2 | Idempotency: Already confirmed | NO email/SMS, exits at Module 5 | ⬜ | |

---

## FAILURE TESTS (from FAILURE_TESTS.md)

| Test | Description | Expected | Result | Notes |
|------|-------------|----------|--------|-------|
| F1 | Empty payload to OPS-LOGGER | Silent fail, exits at Module 2, no Airtable record | ⬜ | |
| F2 | Lead Intake — missing fields | Record created with partial data, no crash | ⬜ | |
| F3 | Stripe — wrong event type | Exits at Module 3, no Airtable update | ⬜ | |
| F4 | Stripe — booking already DEPOSIT_PAID | No update, exits at Module 5 | ⬜ | |
| F5 | Confirmation — Automations_Paused=true | No email, exits at Module 2 | ⬜ | |
| F6 | Confirmation — Emergency_Flag=true | No email, exits at Module 3 | ⬜ | |
| F7 | Confirmation — Concierge_Assigned=false | No email, exits at Module 4 | ⬜ | |
| F8 | Concierge — no concierge found | Slack WARNING, Audit Log PENDING_HUMAN | ⬜ | |
| F9 | Brand Router — unknown source | Slack WARNING, UNKNOWN classification | ⬜ | |
| F10 | Booking Creation — duplicate (idempotency) | No new booking, exits at Module 4 | ⬜ | |

---

## HOW TO RECORD RESULTS

Replace ⬜ with:
- ✅ PASS — test passed as expected
- ❌ FAIL — test failed; add notes describing what went wrong
- ⚠️ PARTIAL — partial pass; add notes

**All 15 core tests must show ✅ PASS before production activation.**

---

## STRIPE TEST MODE VERIFICATION

Before running any test, record:

| Check | Confirmed | Date | Operator |
|-------|-----------|------|----------|
| Stripe Dashboard shows TEST MODE | ⬜ | | |
| M-BOOKING-CREATION Module 6 key starts with sk_test_ | ⬜ | | |
| M-BOOKING-CREATION Module 7 key starts with sk_test_ | ⬜ | | |
| No sk_live_ key found anywhere in Make | ⬜ | | |

---

## SIGN-OFF

When all 15 core tests pass:

| Sign-off | Name | Date |
|----------|------|------|
| Operator (test executor) | | |
| Founder (production approval) | Will | |

Founder Decision record recmpAGlPANugZfhw must be updated to Decision = APPROVED before production activation.

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — SANDBOX_TEST_RESULTS.md*
