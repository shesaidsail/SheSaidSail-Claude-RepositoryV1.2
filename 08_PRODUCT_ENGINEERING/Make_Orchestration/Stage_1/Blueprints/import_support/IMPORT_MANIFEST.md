# IMPORT MANIFEST — Stage 1 Make Blueprints
**Version:** 1.0
**Date:** 2026-05-16
**Project:** She Said Sail + Mare Executive — Make Orchestration Stage 1
**Status:** READY FOR MAKE SANDBOX IMPORT (with credential rebinding required)

---

## Import Order (MANDATORY — Do Not Deviate)

| Order | Scenario ID | File Name | Trigger Type | Dependencies |
|-------|-------------|-----------|--------------|--------------|
| 1 | M-AUDIT-LOGGER | M-AUDIT-LOGGER.blueprint.json | Webhook (instant) | None — must be first |
| 2 | M-BRAND-ROUTER | M-BRAND-ROUTER.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER webhook URL |
| 3 | M-LEAD-INTAKE | M-LEAD-INTAKE.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER, M-SLACK-ALERTS webhook URLs |
| 4 | M-SLACK-ALERTS | M-SLACK-ALERTS.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER webhook URL |
| 5 | M-CONCIERGE-ASSIGNMENT | M-CONCIERGE-ASSIGNMENT.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER, M-SLACK-ALERTS webhook URLs |
| 6 | M-STRIPE-DEPOSIT | M-STRIPE-DEPOSIT.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER, M-SLACK-ALERTS webhook URLs |
| 7 | M-BOOKING-CREATION | M-BOOKING-CREATION.blueprint.json | Webhook (instant, Stripe) | M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BOOKING-CONFIRMATION webhook URLs |
| 8 | M-BOOKING-CONFIRMATION | M-BOOKING-CONFIRMATION.blueprint.json | Webhook (instant) | M-AUDIT-LOGGER, M-SLACK-ALERTS webhook URLs |

**Critical Note:** M-AUDIT-LOGGER must be imported and its webhook URL captured FIRST. Every other scenario calls it. If you import in the wrong order, you will not be able to fill the webhook URL placeholders correctly.

---

## File Inventory

### JSON Blueprint Files (Make-importable)

| File | Scenario | Import Into Make | Contains Placeholders |
|------|----------|-----------------|----------------------|
| M-AUDIT-LOGGER.blueprint.json | M-AUDIT-LOGGER | YES | YES — Airtable, Slack connections |
| M-BRAND-ROUTER.blueprint.json | M-BRAND-ROUTER | YES | YES — Airtable, Slack connections, webhook URLs |
| M-LEAD-INTAKE.blueprint.json | M-LEAD-INTAKE | YES | YES — Airtable, Slack connections, webhook URLs |
| M-SLACK-ALERTS.blueprint.json | M-SLACK-ALERTS | YES | YES — Slack connection, webhook URLs |
| M-CONCIERGE-ASSIGNMENT.blueprint.json | M-CONCIERGE-ASSIGNMENT | YES | YES — Airtable, Slack, Gmail connections |
| M-STRIPE-DEPOSIT.blueprint.json | M-STRIPE-DEPOSIT | YES | YES — Airtable, Stripe, Gmail, SMS connections |
| M-BOOKING-CREATION.blueprint.json | M-BOOKING-CREATION | YES | YES — Airtable, Stripe, Slack connections |
| M-BOOKING-CONFIRMATION.blueprint.json | M-BOOKING-CONFIRMATION | YES | YES — Airtable, Gmail, SMS, Slack connections |

### Specification Files (Reference Only — Do NOT Import)

| File | Purpose |
|------|---------|
| M-AUDIT-LOGGER.spec.md | Human-readable implementation spec |
| M-BRAND-ROUTER.spec.md | Human-readable implementation spec |
| M-LEAD-INTAKE.spec.md | Human-readable implementation spec |
| M-SLACK-ALERTS.spec.md | Human-readable implementation spec |
| M-CONCIERGE-ASSIGNMENT.spec.md | Human-readable implementation spec |
| M-STRIPE-DEPOSIT.spec.md | Human-readable implementation spec |
| M-BOOKING-CREATION.spec.md | Human-readable implementation spec |
| M-BOOKING-CONFIRMATION.spec.md | Human-readable implementation spec |

### Test Payload Files (Use for Sandbox Validation — Do NOT Import)

| File | Purpose |
|------|---------|
| M-AUDIT-LOGGER.test.json | POST to M-AUDIT-LOGGER webhook in sandbox |
| M-BRAND-ROUTER.test.json | POST to M-BRAND-ROUTER webhook in sandbox |
| M-LEAD-INTAKE.test.json | POST to M-LEAD-INTAKE webhook in sandbox |
| M-SLACK-ALERTS.test.json | POST to M-SLACK-ALERTS webhook in sandbox |
| M-CONCIERGE-ASSIGNMENT.test.json | POST to M-CONCIERGE-ASSIGNMENT webhook in sandbox |
| M-STRIPE-DEPOSIT.test.json | POST to M-STRIPE-DEPOSIT webhook in sandbox |
| M-BOOKING-CREATION.test.json | POST to M-BOOKING-CREATION webhook in sandbox |
| M-BOOKING-CONFIRMATION.test.json | POST to M-BOOKING-CONFIRMATION webhook in sandbox |

---

## Placeholder Summary

Every `.blueprint.json` file contains placeholder strings that MUST be replaced after import. Make will prompt you to reconnect modules — do not skip this step.

| Placeholder | Replace With | Where |
|-------------|-------------|-------|
| `RECONNECT_AIRTABLE_CONNECTION` | Your Airtable PAT connection in Make | All modules writing to Airtable |
| `RECONNECT_SLACK_CONNECTION` | Your Slack OAuth app connection in Make | All Slack modules |
| `RECONNECT_GMAIL_CONNECTION` | Your Gmail OAuth connection in Make | All Gmail modules |
| `RECONNECT_STRIPE_CONNECTION` | Your Stripe connection in Make | All Stripe modules |
| `RECONNECT_SMS_CONNECTION` | Your Quo SMS API connection in Make | All SMS HTTP modules |
| `GENERATED_BY_MAKE_AFTER_IMPORT` | Auto-assigned by Make when scenario is saved | Webhook hook IDs |
| `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` | Actual webhook URL from the target scenario | HTTP modules calling other scenarios |
| `AUTOMATION_HEALTH_TABLE_ID` | Airtable Table ID for Automation_Health table | Airtable modules in M-AUDIT-LOGGER |
| `CONCIERGE_OPERATORS_TABLE_ID` | Airtable Table ID for Concierge_Operators table | Airtable modules in M-CONCIERGE-ASSIGNMENT |
| `WILL_SLACK_USER_ID_PLACEHOLDER` | Will's actual Slack member ID (e.g. U01ABC123) | M-SLACK-ALERTS emergency DM module |

---

## Known Limitations

1. **Webhook URLs are generated post-import.** You cannot pre-fill them. Import in order, capture each URL, then update HTTP modules in dependent scenarios.
2. **Airtable table IDs for new tables** (Automation_Health, Concierge_Operators) must be retrieved from Airtable after those tables are created.
3. **Stripe webhook registration** must be done manually in the Stripe Dashboard, pointing to the M-BOOKING-CREATION webhook URL generated by Make.
4. **SMS connection** requires a Quo SMS account and API key. SMS modules will be disconnected until this is configured.
5. **Sandbox testing** must use Stripe Test Mode and a sandbox Airtable base. Do NOT connect sandbox scenarios to production Airtable base `appdZ49WqgjRXxA1R`.
