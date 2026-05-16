# STAGE 1 ROLLBACK ORDER
## She Said Sail — Make Orchestration

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  

---

## ROLLBACK PRINCIPLES

1. **Deactivate operational scenarios before infrastructure scenarios.** Operational scenarios depend on infrastructure — deactivating M-AUDIT-LOGGER while M-BOOKING-CREATION is active creates orphaned audit calls.
2. **Never delete scenarios — only deactivate.** Deleted scenarios cannot be recovered without re-importing from these blueprints.
3. **After deactivation, notify Luciana immediately.** Deactivated scenarios mean manual processing is required.
4. **Create a Founder Decision record for any production rollback.** Required by governance.
5. **Document the rollback reason in the Deployment Log.**

---

## FULL ROLLBACK SEQUENCE

Execute in this exact order when rolling back all Stage 1 scenarios:

| Step | Scenario | Action | Reason |
|------|---------|--------|--------|
| 1 | M-BOOKING-CONFIRMATION | Deactivate | Highest-level operational — depends on all others |
| 2 | M-CONCIERGE-ASSIGNMENT | Deactivate | Operational, downstream of M-BOOKING-CREATION |
| 3 | M-BOOKING-CREATION | Deactivate | Stripe webhook — stop processing new deposits |
| 4 | M-STRIPE-DEPOSIT | Deactivate | Stop new payment links from generating |
| 5 | M-LEAD-INTAKE | Deactivate | Stop new lead ingestion |
| 6 | M-BRAND-ROUTER | Deactivate | Called by M-LEAD-INTAKE only |
| 7 | M-SLACK-ALERTS | Deactivate | Last alert infrastructure — leave active if possible |
| 8 | M-AUDIT-LOGGER | Deactivate | Last resort only — disables all audit trail writing |

---

## PARTIAL ROLLBACK — SINGLE SCENARIO

If only one scenario is causing issues:

1. Identify the failing scenario by checking Make execution history
2. Deactivate ONLY that scenario
3. Leave all upstream dependencies active
4. Do NOT deactivate M-AUDIT-LOGGER or M-SLACK-ALERTS unless they are the source of failure
5. Log the partial rollback in Airtable Deployment Log
6. Notify Luciana which workflows are now manual

### Per-Scenario Manual Fallback

| Scenario Deactivated | Manual Fallback |
|---------------------|----------------|
| M-BOOKING-CONFIRMATION | Luciana sends confirmation email manually from hello@shesaidsail.com |
| M-CONCIERGE-ASSIGNMENT | Luciana monitors Bookings table in Airtable for DEPOSIT_PAID records |
| M-BOOKING-CREATION | Luciana monitors Stripe Dashboard for completed deposits; manually updates Airtable |
| M-STRIPE-DEPOSIT | Luciana generates Stripe Payment Links manually from Stripe Dashboard |
| M-LEAD-INTAKE | Luciana monitors Webflow form submissions manually; creates Airtable Requests manually |
| M-BRAND-ROUTER | Default all leads to SSS until router is restored |

---

## ROLLBACK TRIGGERS

Initiate rollback when any of the following conditions are detected:

| Condition | Rollback Scope |
|-----------|---------------|
| Duplicate Airtable records being created | Deactivate the scenario creating duplicates |
| Duplicate Stripe Payment Links being created | Deactivate M-STRIPE-DEPOSIT immediately |
| Client receiving duplicate emails | Deactivate M-BOOKING-CONFIRMATION or M-STRIPE-DEPOSIT |
| Stripe webhook creating wrong booking updates | Deactivate M-BOOKING-CREATION |
| Audit Log not receiving entries | Investigate M-AUDIT-LOGGER; do NOT roll back operational scenarios |
| Make scenario error rate > 10% | Deactivate the failing scenario; investigate |
| Any SEV-1 event | Full rollback until root cause identified |

---

## POST-ROLLBACK PROCESS

After rolling back any scenario:

1. Create Founder Decision record: type = ROLLBACK, detail = reason
2. Create Airtable Deployment Log entry with rollback timestamp
3. DM Will via Slack with rollback summary
4. Diagnose root cause (check Make execution history, Airtable records, Stripe logs)
5. Fix root cause in Development environment
6. Re-validate in Sandbox
7. Re-deploy per import order in `FINAL_STAGE_1_IMPORT_ORDER.md`
8. Update Deployment Log with re-deployment entry

---

## EMERGENCY AUTOMATION FREEZE

If an emergency requires freezing ALL automations immediately:

1. In Airtable, set `Emergency_Flag = true` on the affected Booking record(s)
2. This pauses M-BOOKING-CONFIRMATION for those records (filter guard active)
3. For full system pause, deactivate scenarios in rollback order above
4. M-EMERGENCY-001 (EMERGENCY-001 scenario) should also be active to auto-notify Will when Emergency_Flag is set

---

*She Said Sail · Stage 1 Rollback Order*  
*CONFIDENTIAL — INTERNAL USE ONLY*
