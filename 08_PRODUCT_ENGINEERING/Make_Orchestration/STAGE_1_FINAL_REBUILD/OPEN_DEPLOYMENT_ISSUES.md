# OPEN DEPLOYMENT ISSUES — STAGE 1 FINAL REBUILD

**Generated:** 2026-05-17  
**Branch:** claude/stage-1-final-rebuild-f4yZF  
**Classification:** Confidential — Internal Use Only

---

## SUMMARY

No blocking infrastructure issues remain. All open items require human-operator action in Make.com, Stripe Dashboard, Webflow, or direct Airtable approval. These cannot be performed by Claude.

---

## OPEN ISSUE 1: Make Import Not Yet Performed

**Severity:** BLOCKING (for go-live)  
**Owner:** Operator  
**Reference:** `docs/FINAL_IMPORT_ORDER.md`

All 7 blueprint JSON files exist in `blueprints/` and are validated. They have not been imported into Make.com. No Make scenario is active.

**Resolution steps:**
1. Log in to Make.com
2. Import M-OPS-LOGGER-ALERTER.json first
3. Copy its webhook URL before proceeding
4. Import remaining 6 scenarios in order
5. Verify each import with module count check per FINAL_IMPORT_ORDER.md

---

## OPEN ISSUE 2: All Connections Unbound

**Severity:** BLOCKING (for go-live)  
**Owner:** Operator  
**Reference:** `docs/REBINDING_GUIDE.md`

All Make connections (Airtable PAT, Slack OAuth, Gmail OAuth) are unbound after import. Scenarios will fail immediately on first run until rebound.

**Connections required:**

| Connection | Scenarios |
|------------|-----------|
| SSS Airtable PAT | ALL 7 |
| SSS Slack OAuth | M-OPS-LOGGER-ALERTER |
| SSS Gmail (hello@shesaidsail.com) | M-LEAD-INTAKE, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |

**Resolution:** Follow REBINDING_GUIDE.md per-module instructions for each scenario.

---

## OPEN ISSUE 3: All Placeholders Unfilled

**Severity:** BLOCKING (for go-live)  
**Owner:** Operator  
**Reference:** `docs/REBINDING_GUIDE.md`

4 placeholder types must be replaced after import. These are in HTTP module URL and header fields — not in notes.

| Placeholder | Count of Occurrences |
|-------------|---------------------|
| `PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE` | 6 scenarios × 1 HTTP module each |
| `PASTE_BRAND_ROUTER_WEBHOOK_URL_HERE` | M-LEAD-INTAKE Module 5 (1 occurrence) |
| `PASTE_STRIPE_SECRET_KEY_HERE` | M-BOOKING-CREATION Modules 6 and 7 (2 occurrences) |
| `PASTE_QUO_SMS_API_KEY_HERE` | M-BOOKING-CREATION Module 12 + M-BOOKING-CONFIRMATION Module 9 (2 occurrences) |

**Resolution:** After importing OPS-LOGGER-ALERTER and BRAND-ROUTER, copy their webhook URLs from Module 1 in each scenario. Enter all values per REBINDING_GUIDE.md.

---

## OPEN ISSUE 4: Webhook URLs Not Registered Externally

**Severity:** BLOCKING (for lead intake and Stripe deposits)  
**Owner:** Operator  
**Reference:** `docs/WEBHOOK_GUIDE.md`

Two external systems need the webhook URLs registered before they will send data to Make:

| System | URL to Register | Target Scenario |
|--------|----------------|-----------------|
| Webflow form | M-LEAD-INTAKE webhook URL | SSS-LEAD-INTAKE |
| Stripe Dashboard | M-STRIPE-DEPOSIT webhook URL | SSS-STRIPE-DEPOSIT |

**Resolution:** Follow WEBHOOK_GUIDE.md. Register Stripe webhook for `payment_intent.succeeded` event only.

---

## OPEN ISSUE 5: Stripe Must Be Verified in TEST Mode

**Severity:** CRITICAL — SAFETY GATE  
**Owner:** Operator

Before any testing, the operator MUST confirm:
1. Stripe Dashboard shows TEST MODE toggle active
2. The Stripe key in M-BOOKING-CREATION Modules 6 and 7 starts with `sk_test_`
3. No `sk_live_` key exists anywhere in Make until after full sandbox validation

**Consequence of failure:** Live charges to real customer cards during testing.

---

## OPEN ISSUE 6: Make Slack Bot Not Added to Channels

**Severity:** HIGH (OPS alerts will silently fail)  
**Owner:** Operator

After binding the Slack OAuth connection, the Make bot must be manually invited to each channel:
- `/invite @Make` in #sss-emergency-ops
- `/invite @Make` in #sss-lead-intake
- `/invite @Make` in #sss-ops-alerts

Without this, Slack modules will return channel_not_found or not_in_channel errors.

---

## OPEN ISSUE 7: 15 Sandbox Tests Not Yet Run

**Severity:** BLOCKING (for go-live)  
**Owner:** Operator  
**Reference:** `testing/SANDBOX_TEST_SEQUENCE.md`

All 15 tests require a running Make instance. Results must be recorded in `SANDBOX_TEST_RESULTS.md`.

---

## OPEN ISSUE 8: Founder Decision Awaiting Approval

**Severity:** BLOCKING (for production go-live)  
**Owner:** Will (Founder)  
**Airtable Record:** recmpAGlPANugZfhw

The Founder Decision record has been created with Decision = PENDING. Will must review and set Decision = APPROVED before the system is activated for live leads.

---

## KNOWN SCHEMA NOTES (Not Blocking)

| Note | Detail |
|------|--------|
| Bookings table has legacy "Stripe Payment Intent ID" (spaces) | Preserved. Make writes to new "Stripe_Payment_Intent_ID" (underscore). |
| Bookings table has legacy "Deposit Amount" (formula) | Preserved. Make writes to new "Deposit_Amount" (number, writable). |
| Bookings table has legacy "Last Automation Timestamp" (dateTime) | Preserved. Make writes to new "Last_Automation_Timestamp" (singleLineText). |
| Concierge_Operators table not verified for data | At least one active record for each operating city (e.g., Miami) must exist before Concierge Assignment tests. |
| Clients table structure not audited | M-BOOKING-CONFIRMATION reads from Clients (tblr84vRIWC5HmKvo). Ensure test records exist with email field populated. |

---

## RESOLVED ISSUES

| Issue | Resolution | Date |
|-------|-----------|------|
| Deprecated stripe:createPaymentLink | Replaced with HTTP two-step (POST /v1/prices + POST /v1/payment_links) | 2026-05-17 |
| M-AUDIT-LOGGER and M-SLACK-ALERTS as separate scenarios | Merged into single M-OPS-LOGGER-ALERTER | 2026-05-17 |
| Confirmation_Sent field missing | Field already existed in Bookings table | 2026-05-17 |
| Concierge_Assigned field missing | Field already existed in Bookings table | 2026-05-17 |
| Concierge_Name field missing | Created (fldetyaVfuwPq6hzj) | 2026-05-17 |
| Stripe_Payment_Link_URL field missing | Created (fldbPuAUbLvQTZPzw) | 2026-05-17 |
| Stripe_Payment_Link_ID field missing | Created (fldEC9EFiPtEpO66x) | 2026-05-17 |
| Stripe_Price_ID field missing | Created (fldWl27SDNmaco9s0) | 2026-05-17 |
| Stripe_Payment_Intent_ID underscore version missing | Created (fldSHaDJL28tAZabo) | 2026-05-17 |
| Deposit_Amount writable version missing | Created as number field (fldgEA1WUGqrprEqw) | 2026-05-17 |
| Last_Automation_Timestamp underscore version missing | Created (fld0PxUx9HrUF794K) | 2026-05-17 |
| #sss-ops-alerts Slack channel missing | Created by Will | 2026-05-17 |
| Founder Decision record missing | Created (recmpAGlPANugZfhw) | 2026-05-17 |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — OPEN_DEPLOYMENT_ISSUES.md*
