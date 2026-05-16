# STAGE 1 DOWNLOAD AND UPLOAD INSTRUCTIONS
**Version:** 1.0
**Date:** 2026-05-16
**Project:** She Said Sail + Mare Executive — Make Orchestration Stage 1
**Audience:** Will (Founder) or designated Systems Engineer

---

## Overview

This document covers:
1. How to download the Stage 1 blueprint package from GitHub
2. How to upload files to Google Drive
3. How to import blueprint files directly into Make.com

---

## Part 1 — Downloading from GitHub

### Option A — Download as ZIP (No Technical Setup Required)

1. Open a web browser and go to the GitHub repository
2. Click the **Branch** dropdown and select: `claude/stage-1-blueprint-export-K58LA`
3. Click the green **Code** button
4. Click **Download ZIP**
5. Save the file (name will be something like `shesaidsail-claude-repositoryv1.2-claude-stage-1-blueprint-export-K58LA.zip`)
6. Unzip the file on your computer
7. Navigate to: `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/`

The Make-importable files are in: `.../Blueprints/json_blueprints/`

---

### Option B — Clone the Repository (Requires git)

```bash
git clone https://github.com/shesaidsail/shesaidsail-claude-repositoryv1.2.git
cd shesaidsail-claude-repositoryv1.2
git checkout claude/stage-1-blueprint-export-K58LA
```

Your blueprint files are at:
```
08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/
```

---

### Option C — Download Individual Blueprint Files

For each of the 8 blueprint files:

1. Navigate to the file in GitHub:
   - `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/json_blueprints/M-AUDIT-LOGGER.blueprint.json`
2. Click the **Raw** button
3. Use **File → Save As** in your browser (or Ctrl+S / Cmd+S)
4. Save with the exact filename shown (keep the `.blueprint.json` extension)

Repeat for all 8 files:
- M-AUDIT-LOGGER.blueprint.json
- M-BRAND-ROUTER.blueprint.json
- M-LEAD-INTAKE.blueprint.json
- M-SLACK-ALERTS.blueprint.json
- M-CONCIERGE-ASSIGNMENT.blueprint.json
- M-STRIPE-DEPOSIT.blueprint.json
- M-BOOKING-CREATION.blueprint.json
- M-BOOKING-CONFIRMATION.blueprint.json

---

### Create a Local ZIP Package

If you want to package everything for sharing:

```bash
# From within the repository root
zip -r "SSS_Make_Stage1_Blueprints_2026-05-16.zip" \
  "08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/"
```

Or on Windows using File Explorer: right-click the `Blueprints` folder → **Compress to ZIP file**.

---

## Part 2 — Uploading to Google Drive

### Step 1 — Create the Google Drive Folder

1. Go to drive.google.com
2. Click **+ New** → **New folder**
3. Name it: **SSS Make Stage 1 Blueprint Package**
4. Inside that folder, create 6 subfolders:
   - `01_JSON_Blueprints`
   - `02_Implementation_Specs`
   - `03_Test_Payloads`
   - `04_Import_Support`
   - `05_Webhook_and_Credential_Checklists`
   - `06_Post_Import_QA`

### Step 2 — Upload Files

Open each subfolder and drag-and-drop the relevant files:

| Subfolder | Files to Upload | Source Folder |
|-----------|----------------|---------------|
| 01_JSON_Blueprints | 8 × .blueprint.json | json_blueprints/ |
| 02_Implementation_Specs | 8 × .spec.md | specs/ |
| 03_Test_Payloads | 8 × .test.json | test_payloads/ |
| 04_Import_Support | IMPORT_MANIFEST.md, MAKE_IMPORT_INSTRUCTIONS.md, STAGE_1_EXPORT_PACKAGE_README.md | import_support/ |
| 05_Webhook_and_Credential_Checklists | CREDENTIAL_REBINDING_CHECKLIST.md, WEBHOOK_REGISTRATION_CHECKLIST.md | import_support/ |
| 06_Post_Import_QA | POST_IMPORT_QA_CHECKLIST.md, SANDBOX_TEST_SEQUENCE.md, PRODUCTION_ENABLE_ORDER.md | import_support/ |

---

## Part 3 — Importing into Make.com

### How to Import a Blueprint

1. Log into Make.com
2. Go to your Organization/Team → **Scenarios**
3. Click **Create a new scenario**
4. In the scenario editor, click the **three-dot menu** (⋮) in the top-right corner
5. Click **Import Blueprint**
6. Click **Browse** and select the `.blueprint.json` file you downloaded
7. Click **Import**
8. Make will display a list of modules that need connections
9. Reconnect each module (see CREDENTIAL_REBINDING_CHECKLIST.md)
10. Save the scenario (Ctrl+S or the save icon)
11. Copy the webhook URL from the first module (click it → copy address)

### Import Order

**MANDATORY — import in this exact sequence:**

| Step | File to Import | Action After Import |
|------|---------------|---------------------|
| 1 | M-AUDIT-LOGGER.blueprint.json | Copy webhook URL, reconnect Airtable + Slack, replace AUTOMATION_HEALTH_TABLE_ID |
| 2 | M-SLACK-ALERTS.blueprint.json | Copy webhook URL, reconnect Slack, replace WILL_SLACK_USER_ID, add M-AUDIT-LOGGER URL to HTTP module |
| 3 | M-BRAND-ROUTER.blueprint.json | Copy webhook URL, add M-AUDIT-LOGGER URL to HTTP module (M-LEAD-INTAKE URL added in step 4) |
| 4 | M-LEAD-INTAKE.blueprint.json | Copy webhook URL, reconnect Airtable, add M-AUDIT-LOGGER + M-SLACK-ALERTS URLs, then go back and update M-BRAND-ROUTER with this URL |
| 5 | M-CONCIERGE-ASSIGNMENT.blueprint.json | Copy webhook URL, reconnect Airtable + Gmail + Slack, replace CONCIERGE_OPERATORS_TABLE_ID, add inter-scenario URLs |
| 6 | M-STRIPE-DEPOSIT.blueprint.json | Copy webhook URL, reconnect Airtable + Stripe + Gmail + SMS, add inter-scenario URLs |
| 7 | M-BOOKING-CONFIRMATION.blueprint.json | Copy webhook URL, reconnect Airtable + Gmail + SMS + Slack, add inter-scenario URLs |
| 8 | M-BOOKING-CREATION.blueprint.json | Copy webhook URL, reconnect Airtable + Stripe + Slack, add all inter-scenario URLs including M-BOOKING-CONFIRMATION, register Stripe webhook |

### After All 8 Are Imported

1. Verify all 8 scenarios show no disconnected modules (no red indicators)
2. Run sandbox tests (SANDBOX_TEST_SEQUENCE.md)
3. If all tests pass, activate production (PRODUCTION_ENABLE_ORDER.md)

---

## Troubleshooting

| Problem | Solution |
|---------|---------|
| "Invalid JSON" error on import | Re-download the file. Ensure no characters were added during download. |
| "Unrecognized module" warning | Accept and continue. Verify module configuration manually after import. |
| Module shows as disconnected (red) | Click the module, reconnect the service using your Make connection |
| Webhook URL is missing from the trigger module | Save the scenario first, then click the webhook trigger module to see the URL |
| HTTP module shows error when calling another scenario | Verify the target scenario is ACTIVE (turned ON) in Make |
| Airtable module shows "table not found" | Replace placeholder table ID with the real Airtable table ID |
