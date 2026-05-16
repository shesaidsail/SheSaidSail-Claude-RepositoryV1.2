# GOOGLE DRIVE UPLOAD INSTRUCTIONS — Stage 1 Blueprint Package
**Version:** 1.0
**Date:** 2026-05-16

---

## Overview

This document instructs Will or the systems engineer how to create the Google Drive folder structure and upload all Stage 1 blueprint package files.

The source of all files is the GitHub repository:
`shesaidsail/shesaidsail-claude-repositoryv1.2`
Branch: `claude/stage-1-blueprint-export-K58LA`
Path: `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/`

---

## Option A — Download from GitHub and Upload Manually

### Step 1 — Download the Package from GitHub

**Option A1 — Download as ZIP (recommended for first-time upload):**

1. Go to the GitHub repository
2. Navigate to branch `claude/stage-1-blueprint-export-K58LA`
3. Click **Code** → **Download ZIP**
4. Unzip the downloaded file
5. Navigate to: `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/`

**Option A2 — Clone via git:**
```bash
git clone https://github.com/shesaidsail/shesaidsail-claude-repositoryv1.2.git
git checkout claude/stage-1-blueprint-export-K58LA
cd "08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints"
```

---

### Step 2 — Create Google Drive Folder Structure

1. Go to Google Drive (drive.google.com)
2. Create a new folder: **SSS Make Stage 1 Blueprint Package**
3. Inside that folder, create these 6 subfolders:
   - `01_JSON_Blueprints`
   - `02_Implementation_Specs`
   - `03_Test_Payloads`
   - `04_Import_Support`
   - `05_Webhook_and_Credential_Checklists`
   - `06_Post_Import_QA`

---

### Step 3 — Upload Files to Correct Folders

**Upload to 01_JSON_Blueprints:**
From `json_blueprints/` folder, upload all 8 `.blueprint.json` files:
- M-AUDIT-LOGGER.blueprint.json
- M-BRAND-ROUTER.blueprint.json
- M-LEAD-INTAKE.blueprint.json
- M-SLACK-ALERTS.blueprint.json
- M-CONCIERGE-ASSIGNMENT.blueprint.json
- M-STRIPE-DEPOSIT.blueprint.json
- M-BOOKING-CREATION.blueprint.json
- M-BOOKING-CONFIRMATION.blueprint.json

**Upload to 02_Implementation_Specs:**
From `specs/` folder, upload all 8 `.spec.md` files.

**Upload to 03_Test_Payloads:**
From `test_payloads/` folder, upload all 8 `.test.json` files.

**Upload to 04_Import_Support:**
From `import_support/` folder, upload:
- IMPORT_MANIFEST.md
- MAKE_IMPORT_INSTRUCTIONS.md
- STAGE_1_EXPORT_PACKAGE_README.md

**Upload to 05_Webhook_and_Credential_Checklists:**
From `import_support/` folder, upload:
- CREDENTIAL_REBINDING_CHECKLIST.md
- WEBHOOK_REGISTRATION_CHECKLIST.md

**Upload to 06_Post_Import_QA:**
From `import_support/` folder, upload:
- POST_IMPORT_QA_CHECKLIST.md
- SANDBOX_TEST_SEQUENCE.md
- PRODUCTION_ENABLE_ORDER.md

---

## Option B — Use Google Drive Desktop App (Sync)

If you have Google Drive for Desktop installed:

1. Clone the repository locally (see Step 1, Option A2)
2. Create the SSS Make Stage 1 Blueprint Package folder in your synced Google Drive folder
3. Create subfolders and copy files using your file manager
4. Files will sync automatically to Google Drive

---

## After Upload — Set Permissions

1. Right-click the root folder **SSS Make Stage 1 Blueprint Package**
2. Click **Share**
3. Add permissions:
   - Will (Founder email): **Owner**
   - Systems Engineer (if engaged): **Editor**
   - Luciana: **Viewer**
4. Uncheck "Notify people" if you don't want email notifications sent

---

## Verification Checklist

After uploading, verify:

- [ ] Folder **SSS Make Stage 1 Blueprint Package** exists in Google Drive
- [ ] All 6 subfolders exist
- [ ] 8 `.blueprint.json` files are in `01_JSON_Blueprints/`
- [ ] 8 `.spec.md` files are in `02_Implementation_Specs/`
- [ ] 8 `.test.json` files are in `03_Test_Payloads/`
- [ ] 3 support docs are in `04_Import_Support/`
- [ ] 2 checklist files are in `05_Webhook_and_Credential_Checklists/`
- [ ] 3 QA files are in `06_Post_Import_QA/`
- [ ] Total: 32 files uploaded and accessible
- [ ] Permissions set correctly (Will = Owner)

---

## Updating Files After Changes

When blueprints are updated in GitHub:

1. Download the updated `.blueprint.json` file from GitHub
2. In Google Drive, navigate to `01_JSON_Blueprints/`
3. Right-click the old file → **Move to trash** (or rename with `-ARCHIVED-YYYY-MM-DD`)
4. Upload the new file to the same folder
5. Update the folder description or add a comment noting the version change

**The GitHub repository is always the authoritative source.** Google Drive is for convenience access and sharing with the systems engineer.
