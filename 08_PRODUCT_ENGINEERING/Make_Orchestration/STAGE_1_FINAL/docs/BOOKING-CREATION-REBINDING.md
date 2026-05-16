# BOOKING CREATION — REBINDING GUIDE

**Classification:** Confidential — Internal Use Only
**Owner:** Will (Founder)
**Effective Date:** May 2026
**Scenario:** SSS-BOOKING-CREATION
**Blueprint:** `CLEAN_M-BOOKING-CREATION.json`

---

## OVERVIEW

After blueprint import, every connection slot shows a red or orange warning. This is expected. You are rebinding — selecting your account's connections — not editing any field mappings.

**Critical rule: rebind connections only. Do not open, edit, or interact with any field mapping inside any module. The imported mappings are correct and will be corrupted by manual edits.**

---

## CONNECTION INVENTORY

| Module | ID | Connection Type | Your Connection |
|--------|----|----------------|-----------------|
| Watch Records | 1 | Airtable PAT | Airtable — SSS PAT |
| Search Records | 2 | Airtable PAT | Airtable — SSS PAT |
| Create Record (Bookings) | 4 | Airtable PAT | Airtable — SSS PAT |
| Create Payment Link | 5 | Stripe | She Said Sail Stripe — TEST MODE |
| Update Record (Bookings) | 6 | Airtable PAT | Airtable — SSS PAT |
| Send Email | 8 | Gmail OAuth | hello@shesaidsail.com |

Modules 3 (Router), 7 (Filter), 9, 10, 11 (HTTP) have no connection to rebind.

---

## MODULE 1 — AIRTABLE WATCH RECORDS

1. Click module 1
2. Click the **Connection** dropdown
3. Select: `Airtable — SSS PAT`
4. After selecting, verify:
   - Base dropdown shows: **She Said Sail**
   - Table dropdown shows: **Requests**
   - Formula field shows: `AND({Status} = 'AVAILABILITY_CONFIRMED', {Environment} = 'Production')`
5. If Base or Table reset to blank after rebinding: re-select from dropdown only — do not retype
6. Close module

---

## MODULE 2 — AIRTABLE SEARCH RECORDS

1. Click module 2
2. Click the **Connection** dropdown
3. Select: `Airtable — SSS PAT`
4. After selecting, verify:
   - Base dropdown shows: **She Said Sail**
   - Table dropdown shows: **Bookings**
   - Filter field contains a formula referencing `{Idempotency_Key}`
5. Close module

---

## MODULE 4 — AIRTABLE CREATE RECORD (BOOKINGS)

1. Click module 4 (inside the router)
2. Click the **Connection** dropdown
3. Select: `Airtable — SSS PAT`
4. After selecting, verify:
   - Base dropdown shows: **She Said Sail**
   - Table dropdown shows: **Bookings**
   - Field mappings are visible (Status, Guest Count, Charter Date, etc.)
5. **Do not click into or modify any field mapping**
6. Close module

---

## MODULE 5 — STRIPE CREATE PAYMENT LINK

**This is the most critical rebinding step. Read carefully.**

1. Click module 5 (Stripe — inside the router)
2. Click the **Connection** dropdown
3. Select: `She Said Sail Stripe (hello...)` — the TEST MODE connection
4. Confirm the connection label includes "test" or the Stripe dashboard shows test mode is active
5. **Do NOT click into the Line Items section**
6. **Do NOT open the Price field**
7. **Do NOT interact with any field inside the module beyond selecting the connection**
8. Close module immediately after selecting the connection

**Why:** The Stripe module uses `price_data` (inline dynamic price creation). Opening the Price field causes Make to render a dropdown of static Stripe prices, which corrupts the mapping. The imported `price_data` structure is invisible in the UI but functional in execution.

**Verify the connection is TEST mode:** Go to Stripe dashboard → confirm "Test mode" banner is visible. If Stripe shows "Live mode", do not proceed. Switch to test mode first.

---

## MODULE 6 — AIRTABLE UPDATE RECORD (BOOKINGS)

1. Click module 6 (inside the router)
2. Click the **Connection** dropdown
3. Select: `Airtable — SSS PAT`
4. After selecting, verify:
   - Base dropdown shows: **She Said Sail**
   - Table dropdown shows: **Bookings**
   - Record ID field shows: `{{4.id}}`
   - Status field shows: `DEPOSIT_SENT`
   - Stripe Payment Link field shows: `{{5.url}}`
5. Close module

**If `Stripe Payment Link` field shows an error:** The field does not exist in Airtable yet. Create it: Airtable → Bookings table → add field named `Stripe Payment Link`, type = URL. Then return to Make and the field will resolve.

---

## MODULE 8 — GMAIL SEND EMAIL

1. Click module 8 (inside the router)
2. Click the **Connection** dropdown (labeled "Account")
3. Select: `hello@shesaidsail.com`
4. Verify:
   - To field shows: `{{1.fields.Email}}`
   - Subject field references the client's first name and brand
   - Body field shows the HTML email template (long string — do not edit)
5. Close module

---

## MODULE 9 — QUO SMS (HTTP)

No connection to rebind. Replace the placeholder API key only:

1. Click module 9
2. Find the **Headers** section
3. Find the `Authorization` header
4. Replace the value: change `Bearer PASTE_QUO_API_KEY_HERE` to `Bearer [actual Quo API key]`
5. The URL (`https://api.quosms.com/v1/messages`) and body field are correct — do not modify
6. Close module

---

## MODULE 10 — AUDIT LOGGER (HTTP)

No connection to rebind. Replace the placeholder URL only:

1. Click module 10
2. Find the **URL** field
3. Replace: `PASTE_AUDIT_LOGGER_WEBHOOK_URL_HERE`
4. With: the webhook URL copied from Make → SSS-AUDIT-LOGGER scenario
5. The body field is correct — do not modify
6. Close module

---

## MODULE 11 — SLACK ALERTS (HTTP)

No connection to rebind. Replace the placeholder URL only:

1. Click module 11
2. Find the **URL** field
3. Replace: `PASTE_SLACK_ALERTS_WEBHOOK_URL_HERE`
4. With: the webhook URL copied from Make → SSS-SLACK-ALERTS scenario
5. The body field is correct — do not modify
6. Close module

---

## POST-REBINDING VERIFICATION

After completing all modules above:

| Check | Expected Result |
|-------|----------------|
| Module 1 connection | Green — no red warning |
| Module 2 connection | Green — no red warning |
| Module 4 connection | Green — no red warning |
| Module 5 connection | Green — Stripe TEST account |
| Module 6 connection | Green — no red warning |
| Module 8 connection | Green — hello@shesaidsail.com |
| Module 9 URL | Real Quo endpoint — no placeholder text |
| Module 10 URL | Real Audit Logger URL — no placeholder text |
| Module 11 URL | Real Slack Alerts URL — no placeholder text |
| Total red warnings | 0 |

If any module still shows a red warning after rebinding: click that module, select the connection again, and close. If the warning persists, the connection in Make → Connections may have expired — re-authenticate it.

---

## AIRTABLE FIELD REFERENCE (READ-ONLY)

These are the Airtable IDs used by this scenario. Do not change these in Make.

| Resource | ID |
|----------|----|
| Base | `appdZ49WqgjRXxA1R` |
| Requests table | `tblTlSB9CO4dTGodg` |
| Bookings table | `tbl72omPibBkn2hZL` |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*
*08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/docs/BOOKING-CREATION-REBINDING.md*
