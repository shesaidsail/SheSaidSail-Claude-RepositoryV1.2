# BOOKING CREATION — IMPORT STEPS

**Classification:** Confidential — Internal Use Only
**Owner:** Will (Founder)
**Effective Date:** May 2026
**File to import:** `STAGE_1_FINAL/CLEAN_M-BOOKING-CREATION.json`

---

## PRE-IMPORT CHECKLIST

Complete every item before importing. Do not skip.

- [ ] Stripe dashboard confirms **TEST MODE** is active (orange "Test mode" banner visible)
- [ ] Make.com workspace confirmed: **SheSaidSail** (not a personal workspace)
- [ ] Airtable Bookings table (`tbl72omPibBkn2hZL`) has field `Stripe Payment Link` (URL type) — create it if missing
- [ ] Airtable Bookings table has field `Confirmation_Sent` (Checkbox type) — create it if missing
- [ ] Airtable Bookings table has field `Concierge_Assigned` (Checkbox type) — create it if missing
- [ ] `SSS-AUDIT-LOGGER` scenario is already deployed and its webhook URL is known
- [ ] `SSS-SLACK-ALERTS` scenario is already deployed and its webhook URL is known
- [ ] The corrupted `SSS-BOOKING-CREATION` scenario has been deleted (see Step 1)

---

## STEP 1 — DELETE THE CORRUPTED SCENARIO

1. In Make.com, locate the existing `SSS-BOOKING-CREATION` scenario
2. Click the **three-dot menu (⋮)** in the scenario card or editor header
3. Select **Delete**
4. Confirm deletion when prompted
5. Verify the scenario no longer appears in your scenarios list before continuing

**Do not attempt to fix or modify the corrupted scenario. Delete it entirely.**

---

## STEP 2 — CREATE A NEW SCENARIO

1. In Make.com, click **+ Create a new scenario**
2. When the empty canvas opens, immediately click the **three-dot menu (⋮)** in the top toolbar
3. Select **Import Blueprint**
4. Click **Browse** and select: `CLEAN_M-BOOKING-CREATION.json`
5. Click **Import**
6. Make.com loads 11 modules across a trigger + search + router pattern — this is correct

---

## STEP 3 — VERIFY IMPORT LOADED CORRECTLY

Before touching anything, visually verify:

| Module | Position | Module Type | Expected Label |
|--------|----------|-------------|----------------|
| 1 | Far left | Airtable | Watch Records |
| 2 | Second | Airtable | Search Records |
| 3 | Third | Router | BasicRouter |
| 4 | Inside router | Airtable | Create a Record |
| 5 | Inside router | Stripe | Create a Payment Link |
| 6 | Inside router | Airtable | Update a Record |
| 7 | Inside router | Filter | BasicFilter |
| 8 | Inside router | Gmail | Send an Email |
| 9 | Inside router | HTTP | Make a request (Quo SMS) |
| 10 | Inside router | HTTP | Make a request (Audit Logger) |
| 11 | Inside router | HTTP | Make a request (Slack Alerts) |

**If the Stripe module (5) shows as an unknown/unrecognized module:** stop. See Troubleshooting at the bottom of this file.

**If any module shows a red error indicator:** this is expected — it indicates an unbound connection. Do not attempt to fix it by editing field mappings. Proceed to Step 4 (rebinding).

---

## STEP 4 — RENAME THE SCENARIO

1. Click the scenario name at the top of the editor
2. Rename to exactly: `SSS-BOOKING-CREATION`
3. Press Enter to confirm

---

## STEP 5 — REBIND CONNECTIONS

See `BOOKING-CREATION-REBINDING.md` for the complete rebinding procedure.

Complete ALL rebinding before saving. A scenario saved with unbound connections fails silently.

---

## STEP 6 — INJECT PLACEHOLDER URLS

Three HTTP modules contain placeholder text that must be replaced before saving:

**Module 9 — Quo SMS:**
- Click module 9
- Find the `Authorization` header value
- Replace `PASTE_QUO_API_KEY_HERE` with: `Bearer [your Quo API key]`

**Module 10 — Audit Logger:**
- Click module 10
- Find the URL field
- Replace `PASTE_AUDIT_LOGGER_WEBHOOK_URL_HERE` with the actual SSS-AUDIT-LOGGER webhook URL

**Module 11 — Slack Alerts:**
- Click module 11
- Find the URL field
- Replace `PASTE_SLACK_ALERTS_WEBHOOK_URL_HERE` with the actual SSS-SLACK-ALERTS webhook URL

---

## STEP 7 — PRE-SAVE VERIFICATION

Before clicking Save, confirm:

- [ ] Module 1 (Watch Records): base = She Said Sail, table = Requests
- [ ] Module 2 (Search Records): base = She Said Sail, table = Bookings
- [ ] Module 3 (Router): one route visible labeled "New booking — process"
- [ ] Module 4 (Create Record): base = She Said Sail, table = Bookings
- [ ] Module 5 (Stripe): connection shows your Stripe TEST account — NOT live
- [ ] Module 6 (Update Record): base = She Said Sail, table = Bookings
- [ ] Module 7 (Filter): label reads "Automations_Paused — exit before outbound if true"
- [ ] Module 8 (Gmail): account shows hello@shesaidsail.com
- [ ] Module 9 (HTTP): URL = `https://api.quosms.com/v1/messages`, auth header populated
- [ ] Module 10 (HTTP): URL = real Audit Logger webhook URL (no placeholder text)
- [ ] Module 11 (HTTP): URL = real Slack Alerts webhook URL (no placeholder text)
- [ ] Zero red connection warnings on any module

---

## STEP 8 — SAVE

1. Click **Save** (NOT Save and enable)
2. Scenario saves in OFF state — this is correct
3. Do not activate yet

---

## STEP 9 — ACTIVATE

Only activate after completing all tests in `BOOKING-CREATION-TESTING.md`.

1. Toggle the scenario ON using the switch in the top toolbar
2. Confirm the scenario status changes to active (green)
3. Schedule: Every 15 minutes (or as configured)

---

## TROUBLESHOOTING — STRIPE MODULE NOT RECOGNIZED

If module 5 imports as an unknown or broken module after import:

**Option A — Update Make Stripe App:**
1. Go to Make → Apps (left sidebar) → search for Stripe
2. If an update is available, install it
3. Delete the failed scenario
4. Re-import `CLEAN_M-BOOKING-CREATION.json`

**Option B — Use HTTP Fallback:**
If the native Stripe module continues to fail, contact the engineering owner (Will) before making any changes. Do not manually rebuild the Stripe module through the UI.

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*
*08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/docs/BOOKING-CREATION-IMPORT-STEPS.md*
