# GOOGLE DRIVE UPLOAD MANIFEST — Stage 1 Make Blueprint Package
**Version:** 1.0
**Date:** 2026-05-16
**Project:** She Said Sail + Mare Executive — Make Orchestration Stage 1

---

## Google Drive Folder Structure

Create this folder structure in Google Drive before uploading:

```
SSS Make Stage 1 Blueprint Package/
├── 01_JSON_Blueprints/
├── 02_Implementation_Specs/
├── 03_Test_Payloads/
├── 04_Import_Support/
├── 05_Webhook_and_Credential_Checklists/
└── 06_Post_Import_QA/
```

---

## File Upload Manifest

### 01_JSON_Blueprints/ — Make-importable blueprint files

| File Name | Source Path (GitHub) | Importable Into Make | Contains Placeholders | Notes |
|-----------|---------------------|---------------------|-----------------------|-------|
| M-AUDIT-LOGGER.blueprint.json | json_blueprints/M-AUDIT-LOGGER.blueprint.json | YES | YES — Airtable, Slack | Import FIRST |
| M-BRAND-ROUTER.blueprint.json | json_blueprints/M-BRAND-ROUTER.blueprint.json | YES | YES — Airtable, Slack, webhook URLs | Import 2nd |
| M-LEAD-INTAKE.blueprint.json | json_blueprints/M-LEAD-INTAKE.blueprint.json | YES | YES — Airtable, Slack, webhook URLs | Import 3rd |
| M-SLACK-ALERTS.blueprint.json | json_blueprints/M-SLACK-ALERTS.blueprint.json | YES | YES — Slack, webhook URLs | Import 4th |
| M-CONCIERGE-ASSIGNMENT.blueprint.json | json_blueprints/M-CONCIERGE-ASSIGNMENT.blueprint.json | YES | YES — Airtable, Slack, Gmail | Import 5th |
| M-STRIPE-DEPOSIT.blueprint.json | json_blueprints/M-STRIPE-DEPOSIT.blueprint.json | YES | YES — Airtable, Stripe, Gmail, SMS | Import 6th |
| M-BOOKING-CREATION.blueprint.json | json_blueprints/M-BOOKING-CREATION.blueprint.json | YES | YES — Airtable, Stripe, Slack, webhook URLs | Import 7th |
| M-BOOKING-CONFIRMATION.blueprint.json | json_blueprints/M-BOOKING-CONFIRMATION.blueprint.json | YES | YES — Airtable, Gmail, SMS, Slack | Import 8th (before Creation) |

**Important:** These are the SAME files as in the GitHub repository. Google Drive is a delivery/storage location. Import from whichever is more accessible.

---

### 02_Implementation_Specs/ — Reference documentation

| File Name | Source Path (GitHub) | Importable Into Make | Reference Only | Notes |
|-----------|---------------------|---------------------|----------------|-------|
| M-AUDIT-LOGGER.spec.md | specs/M-AUDIT-LOGGER.spec.md | NO | YES | Human-readable flow documentation |
| M-BRAND-ROUTER.spec.md | specs/M-BRAND-ROUTER.spec.md | NO | YES | |
| M-LEAD-INTAKE.spec.md | specs/M-LEAD-INTAKE.spec.md | NO | YES | |
| M-SLACK-ALERTS.spec.md | specs/M-SLACK-ALERTS.spec.md | NO | YES | |
| M-CONCIERGE-ASSIGNMENT.spec.md | specs/M-CONCIERGE-ASSIGNMENT.spec.md | NO | YES | |
| M-STRIPE-DEPOSIT.spec.md | specs/M-STRIPE-DEPOSIT.spec.md | NO | YES | |
| M-BOOKING-CREATION.spec.md | specs/M-BOOKING-CREATION.spec.md | NO | YES | |
| M-BOOKING-CONFIRMATION.spec.md | specs/M-BOOKING-CONFIRMATION.spec.md | NO | YES | |

---

### 03_Test_Payloads/ — Sandbox test data

| File Name | Source Path (GitHub) | Importable Into Make | Contains Sensitive Data | Notes |
|-----------|---------------------|---------------------|------------------------|-------|
| M-AUDIT-LOGGER.test.json | test_payloads/M-AUDIT-LOGGER.test.json | NO | NO — test data only | POST to webhook during sandbox testing |
| M-BRAND-ROUTER.test.json | test_payloads/M-BRAND-ROUTER.test.json | NO | NO | |
| M-LEAD-INTAKE.test.json | test_payloads/M-LEAD-INTAKE.test.json | NO | NO | |
| M-SLACK-ALERTS.test.json | test_payloads/M-SLACK-ALERTS.test.json | NO | NO | |
| M-CONCIERGE-ASSIGNMENT.test.json | test_payloads/M-CONCIERGE-ASSIGNMENT.test.json | NO | NO | Update record_id before use |
| M-STRIPE-DEPOSIT.test.json | test_payloads/M-STRIPE-DEPOSIT.test.json | NO | NO | Use Stripe test amounts only |
| M-BOOKING-CREATION.test.json | test_payloads/M-BOOKING-CREATION.test.json | NO | NO | |
| M-BOOKING-CONFIRMATION.test.json | test_payloads/M-BOOKING-CONFIRMATION.test.json | NO | NO | |

---

### 04_Import_Support/ — Operational instructions

| File Name | Source Path (GitHub) | Purpose |
|-----------|---------------------|---------|
| IMPORT_MANIFEST.md | import_support/IMPORT_MANIFEST.md | Master file list and import order |
| MAKE_IMPORT_INSTRUCTIONS.md | import_support/MAKE_IMPORT_INSTRUCTIONS.md | Step-by-step import process |
| STAGE_1_EXPORT_PACKAGE_README.md | import_support/STAGE_1_EXPORT_PACKAGE_README.md | Package overview and quick start |

---

### 05_Webhook_and_Credential_Checklists/ — Configuration tracking

| File Name | Source Path (GitHub) | Purpose |
|-----------|---------------------|---------|
| CREDENTIAL_REBINDING_CHECKLIST.md | import_support/CREDENTIAL_REBINDING_CHECKLIST.md | Track all credential reconnections per scenario |
| WEBHOOK_REGISTRATION_CHECKLIST.md | import_support/WEBHOOK_REGISTRATION_CHECKLIST.md | Track webhook URLs and Stripe registration |

---

### 06_Post_Import_QA/ — Validation and activation

| File Name | Source Path (GitHub) | Purpose |
|-----------|---------------------|---------|
| POST_IMPORT_QA_CHECKLIST.md | import_support/POST_IMPORT_QA_CHECKLIST.md | QA validation before activation |
| SANDBOX_TEST_SEQUENCE.md | import_support/SANDBOX_TEST_SEQUENCE.md | Step-by-step sandbox tests |
| PRODUCTION_ENABLE_ORDER.md | import_support/PRODUCTION_ENABLE_ORDER.md | Controlled production activation |

---

## Google Drive Access Permissions

Recommended access settings for this folder:

| Role | Access Level |
|------|-------------|
| Will (Founder) | Owner |
| Systems Engineer (when engaged) | Editor |
| Luciana (Ops Lead) | Viewer |
| External contractors | Share individual files only — do NOT share full folder |

**Security Note:** These files do not contain live credentials, API keys, or secrets. However, the blueprint files do document the automation architecture. Treat as Confidential — Internal Use Only.

---

## Sync Policy

When blueprints are updated in GitHub, re-upload the updated `.blueprint.json` files to Google Drive `01_JSON_Blueprints/` folder. Delete the old version (or move to an `Archive/` subfolder).

Do NOT rely on Google Drive as the source of truth — GitHub is the authoritative source per the Systems Intelligence Architecture.
