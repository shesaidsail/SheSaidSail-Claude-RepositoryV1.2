# STAGE 1 BLUEPRINT EXPORT PACKAGE MANIFEST
**Version:** 1.0
**Date:** 2026-05-16
**Project:** She Said Sail + Mare Executive — Make Orchestration Stage 1
**Repository:** shesaidsail/shesaidsail-claude-repositoryv1.2
**Branch:** claude/stage-1-blueprint-export-K58LA
**Base Path:** 08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/

---

## Complete File List

### JSON Blueprints (Make-importable)

| # | File | Path | Size | Valid JSON | Import Order |
|---|------|------|------|-----------|--------------|
| 1 | M-AUDIT-LOGGER.blueprint.json | json_blueprints/ | — | YES | 1st |
| 2 | M-BRAND-ROUTER.blueprint.json | json_blueprints/ | — | YES | 3rd |
| 3 | M-LEAD-INTAKE.blueprint.json | json_blueprints/ | — | YES | 4th |
| 4 | M-SLACK-ALERTS.blueprint.json | json_blueprints/ | — | YES | 2nd |
| 5 | M-CONCIERGE-ASSIGNMENT.blueprint.json | json_blueprints/ | — | YES | 5th |
| 6 | M-STRIPE-DEPOSIT.blueprint.json | json_blueprints/ | — | YES | 6th |
| 7 | M-BOOKING-CREATION.blueprint.json | json_blueprints/ | — | YES | 8th |
| 8 | M-BOOKING-CONFIRMATION.blueprint.json | json_blueprints/ | — | YES | 7th |

### Specification Files (Reference Only)

| # | File | Path |
|---|------|------|
| 9 | M-AUDIT-LOGGER.spec.md | specs/ |
| 10 | M-BRAND-ROUTER.spec.md | specs/ |
| 11 | M-LEAD-INTAKE.spec.md | specs/ |
| 12 | M-SLACK-ALERTS.spec.md | specs/ |
| 13 | M-CONCIERGE-ASSIGNMENT.spec.md | specs/ |
| 14 | M-STRIPE-DEPOSIT.spec.md | specs/ |
| 15 | M-BOOKING-CREATION.spec.md | specs/ |
| 16 | M-BOOKING-CONFIRMATION.spec.md | specs/ |

### Test Payload Files (Sandbox Use Only)

| # | File | Path |
|---|------|------|
| 17 | M-AUDIT-LOGGER.test.json | test_payloads/ |
| 18 | M-BRAND-ROUTER.test.json | test_payloads/ |
| 19 | M-LEAD-INTAKE.test.json | test_payloads/ |
| 20 | M-SLACK-ALERTS.test.json | test_payloads/ |
| 21 | M-CONCIERGE-ASSIGNMENT.test.json | test_payloads/ |
| 22 | M-STRIPE-DEPOSIT.test.json | test_payloads/ |
| 23 | M-BOOKING-CREATION.test.json | test_payloads/ |
| 24 | M-BOOKING-CONFIRMATION.test.json | test_payloads/ |

### Import Support Files

| # | File | Path |
|---|------|------|
| 25 | IMPORT_MANIFEST.md | import_support/ |
| 26 | MAKE_IMPORT_INSTRUCTIONS.md | import_support/ |
| 27 | CREDENTIAL_REBINDING_CHECKLIST.md | import_support/ |
| 28 | WEBHOOK_REGISTRATION_CHECKLIST.md | import_support/ |
| 29 | POST_IMPORT_QA_CHECKLIST.md | import_support/ |
| 30 | SANDBOX_TEST_SEQUENCE.md | import_support/ |
| 31 | PRODUCTION_ENABLE_ORDER.md | import_support/ |
| 32 | STAGE_1_EXPORT_PACKAGE_README.md | import_support/ |

### Google Drive Package Files

| # | File | Path |
|---|------|------|
| 33 | GOOGLE_DRIVE_UPLOAD_MANIFEST.md | google_drive_package/ |
| 34 | GOOGLE_DRIVE_FOLDER_STRUCTURE.md | google_drive_package/ |
| 35 | GOOGLE_DRIVE_UPLOAD_INSTRUCTIONS.md | google_drive_package/ |

### Root-Level Reports

| # | File | Path |
|---|------|------|
| 36 | STAGE_1_BLUEPRINT_EXPORT_PACKAGE_MANIFEST.md | (this file) |
| 37 | STAGE_1_BLUEPRINT_GENERATION_REPORT.md | root |
| 38 | STAGE_1_IMPORT_READINESS.md | root |
| 39 | STAGE_1_KNOWN_LIMITATIONS.md | root |
| 40 | STAGE_1_DOWNLOAD_AND_UPLOAD_INSTRUCTIONS.md | root |

---

## Recommended Download Instructions from GitHub

### Option 1 — Download ZIP (No git required)

1. Go to: https://github.com/shesaidsail/shesaidsail-claude-repositoryv1.2
2. Switch to branch: `claude/stage-1-blueprint-export-K58LA`
3. Click **Code** → **Download ZIP**
4. Unzip and navigate to: `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/`
5. The `json_blueprints/` subfolder contains all 8 Make-importable files

### Option 2 — Clone via git

```bash
git clone https://github.com/shesaidsail/shesaidsail-claude-repositoryv1.2.git
cd shesaidsail-claude-repositoryv1.2
git checkout claude/stage-1-blueprint-export-K58LA
ls "08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/"
```

### Option 3 — Download Individual Files

Navigate directly to each blueprint file on GitHub and click **Raw** → **Save As** to download individual `.blueprint.json` files.

---

## Recommended ZIP Packaging Instructions

To create a standalone ZIP for sharing with the systems engineer:

```bash
cd /path/to/repo
zip -r "SSS_Make_Stage1_Blueprints_2026-05-16.zip" \
  "08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/"
```

The ZIP file will contain the complete folder structure and all 40 files.

---

## Make Import Order (MANDATORY)

Import in this exact sequence:

| Step | Scenario | Reason |
|------|----------|--------|
| 1 | M-AUDIT-LOGGER | All other scenarios call this. Must be live first. |
| 2 | M-SLACK-ALERTS | Many scenarios call this for alerts. Needed before lead intake. |
| 3 | M-BRAND-ROUTER | Calls M-LEAD-INTAKE — import M-LEAD-INTAKE next. |
| 4 | M-LEAD-INTAKE | Called by M-BRAND-ROUTER. |
| 5 | M-CONCIERGE-ASSIGNMENT | Depends on Airtable Concierge_Operators table existing. |
| 6 | M-STRIPE-DEPOSIT | Depends on Bookings records existing. |
| 7 | M-BOOKING-CONFIRMATION | Must be live before M-BOOKING-CREATION calls it. |
| 8 | M-BOOKING-CREATION | Last — requires Stripe webhook. Enable last. |

---

## Post-Import Credential Rebinding Steps

After importing each blueprint, complete these rebinding steps:

### All Scenarios
1. Reconnect Airtable module → Select "SSS Airtable Production" connection (Personal Access Token for appdZ49WqgjRXxA1R)
2. Reconnect Slack module → Select "SSS Slack" connection
3. Save scenario

### Scenario-Specific Steps

| Scenario | Additional Rebinding |
|----------|---------------------|
| M-AUDIT-LOGGER | Replace AUTOMATION_HEALTH_TABLE_ID with real Airtable table ID |
| M-SLACK-ALERTS | Replace WILL_SLACK_USER_ID_PLACEHOLDER with Will's Slack Member ID |
| M-CONCIERGE-ASSIGNMENT | Replace CONCIERGE_OPERATORS_TABLE_ID; reconnect Gmail |
| M-STRIPE-DEPOSIT | Reconnect Stripe (Test mode first), Gmail, SMS; verify success URL |
| M-BOOKING-CREATION | Reconnect Stripe; register Stripe webhook; add signing secret |
| M-BOOKING-CONFIRMATION | Reconnect Gmail (SSS + ME accounts), SMS |

### All HTTP Modules
Replace `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` with actual webhook URLs captured from each scenario after import. See WEBHOOK_REGISTRATION_CHECKLIST.md for the propagation map.

---

## Sandbox Test Order

After all 8 scenarios are imported and configured:

1. TEST 1 — M-AUDIT-LOGGER baseline + idempotency
2. TEST 2 — M-SLACK-ALERTS (all 4 alert types)
3. TEST 3 — M-BRAND-ROUTER → M-LEAD-INTAKE chain + duplicate detection
4. TEST 4 — M-LEAD-INTAKE standalone
5. TEST 5 — M-CONCIERGE-ASSIGNMENT (found + not found)
6. TEST 6 — M-STRIPE-DEPOSIT (Stripe test link creation)
7. TEST 7 — M-BOOKING-CREATION (Stripe test event simulation + idempotency)
8. TEST 8 — M-BOOKING-CONFIRMATION (SSS + ME brands)
9. TEST 9 — Full end-to-end chain

All tests must pass before production activation. See SANDBOX_TEST_SEQUENCE.md.
