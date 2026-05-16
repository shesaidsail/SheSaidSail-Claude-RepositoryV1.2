# PRODUCTION_GO_LIVE_CHECKLIST

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Final launch checklist before real ads are turned on. Every item must be checked before ad spend begins.
**Classification:** Confidential — Internal Use Only

---

## AUTHORITY STATEMENT

Will signs off on this checklist personally before any paid advertising begins. This checklist cannot be delegated. Luciana may complete the preparation work for each item, but Will personally reviews and confirms every item marked with ⭐.

---

## SECTION A — AIRTABLE READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| A1 | ⭐ Environment field present on Bookings table (Production / Sandbox / Development) | Will confirms | ☐ |
| A2 | ⭐ Environment field present on Requests table | Will confirms | ☐ |
| A3 | Idempotency_Key field present on Bookings (Single Line Text) | Luciana | ☐ |
| A4 | Idempotency_Key field present on Requests (Single Line Text) | Luciana | ☐ |
| A5 | D7_Review_Eligible formula field present on Bookings and calculating correctly | Luciana | ☐ |
| A6 | ⭐ Automations_Paused field present on Bookings (Checkbox) | Will confirms | ☐ |
| A7 | ⭐ Emergency_Flag field present on Bookings (Checkbox) | Will confirms | ☐ |
| A8 | AI_Prompt_Versions table has correct 26-field schema in main base | Luciana | ☐ |
| A9 | At least one AI_Prompt_Version record exists for CHARTER_BRIEF_SYSTEM with Status = LIVE and Will_Approved = true | Will creates | ☐ |
| A10 | Yacht_Availability table created with correct schema | Luciana | ☐ |
| A11 | Automation_Health table created | Luciana | ☐ |
| A12 | Make_Scenarios table exists in main base | Luciana | ☐ |
| A13 | Concierge_Operators table migrated to main base | Luciana | ☐ |
| A14 | ⭐ All production Booking records have Environment = Production (not blank) | Will confirms | ☐ |
| A15 | ⭐ All production Request records have Environment = Production | Will confirms | ☐ |
| A16 | ⭐ Airtable-native automation inventory complete — no circular trigger risk identified | Will reviews | ☐ |
| A17 | Packages table has Live = true checkbox on all active packages | Luciana | ☐ |
| A18 | Packages table has Brand field correctly populated (SSS / ME per package) | Luciana | ☐ |
| A19 | All active City records have Tax_Rate populated | Luciana | ☐ |
| A20 | All Concierge_Operators records have Slack_User_ID populated | Luciana | ☐ |

---

## SECTION B — STRIPE READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| B1 | ⭐ Stripe webhook endpoint for payment_intent.succeeded is configured and pointing to production Make URL | Will confirms | ☐ |
| B2 | ⭐ Stripe webhook endpoint for payment_intent.payment_failed is configured and pointing to production Make URL | Will confirms | ☐ |
| B3 | Stripe webhook signing secret stored in Make credential vault (not in scenario directly) | Will | ☐ |
| B4 | Stripe test mode successfully completed — all webhook events tested | Luciana / Make builder | ☐ |
| B5 | ⭐ Stripe live mode activated — test credentials replaced with live credentials | Will activates | ☐ |
| B6 | Stripe success URL configured: shesaidsail.com/booking-confirmed | Luciana | ☐ |
| B7 | Stripe payment link description format verified: "SSS Charter Deposit — [Client] — [Date]" | Luciana | ☐ |
| B8 | ⭐ One real $1 test transaction completed in production Stripe and refunded immediately | Will + Luciana | ☐ |

---

## SECTION C — MAKE SCENARIO READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| C1 | ⭐ M-LEAD-INTAKE: Active in production, all sandbox tests passed | Will confirms | ☐ |
| C2 | ⭐ M-BRAND-ROUTER: Active in production, SSS + ME routing verified | Will confirms | ☐ |
| C3 | ⭐ M-BOOKING-CREATION: Active in production, Stripe link generation verified | Will confirms | ☐ |
| C4 | ⭐ M-STRIPE-DEPOSIT: Active in production, deposit confirmation flow verified | Will confirms | ☐ |
| C5 | ⭐ M-BOOKING-CONFIRMATION: Active in production, confirmation email verified | Will confirms | ☐ |
| C6 | M-CONCIERGE-ASSIGNMENT: Active in production, Luciana receives test notification | Luciana | ☐ |
| C7 | ⭐ M-BASIC-LIFECYCLE: Active in production, scheduled daily at 7am EST | Will confirms | ☐ |
| C8 | M-REVIEW-REQUEST: Active in production, D7_Review_Eligible gate verified | Luciana | ☐ |
| C9 | All 8 Stage 1 scenarios registered in Make_Scenarios Airtable table with correct Make Scenario IDs | Luciana | ☐ |
| C10 | ⭐ Emergency stop test passed: Emergency_Flag = true halts all outbound messages | Will tests personally | ☐ |
| C11 | All Airtable webhook triggers scoped to specific field changes (not generic "record updated") | Make builder | ☐ |

---

## SECTION D — COMMUNICATION SYSTEMS READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| D1 | Gmail OAuth connected to hello@shesaidsail.com in Make | Luciana | ☐ |
| D2 | Quo SMS API key stored in Make credential vault | Will | ☐ |
| D3 | ⭐ Test email received by real client email address — formatting, links, branding verified | Will reviews | ☐ |
| D4 | ⭐ Test SMS received on real mobile — content verified | Will receives | ☐ |
| D5 | SSS email templates created and approved by Will: DEPOSIT_REQUEST, DEPOSIT_CONFIRMED, BOOKING_CONFIRMED | Will approves | ☐ |
| D6 | ME email templates created and approved: DEPOSIT_REQUEST, DEPOSIT_CONFIRMED, BOOKING_CONFIRMED | Will approves | ☐ |
| D7 | All lifecycle email templates approved: T72, T48, T24, D1 | Will approves | ☐ |
| D8 | Review request email template approved | Will approves | ☐ |
| D9 | Slack channels confirmed active: #sss-ops-leads, #me-ops-leads, #sss-ops-bookings, #me-ops-bookings, #sss-ops-alerts, #sss-emergency-ops | Luciana | ☐ |
| D10 | Will's Slack DM is the direct channel for SEV-1 alerts — tested and confirmed | Will | ☐ |
| D11 | Luciana's Slack DM is the channel for SEV-2 alerts — tested and confirmed | Luciana | ☐ |

---

## SECTION E — BRAND AND CONTENT READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| E1 | ⭐ SSS brand routing test: form submission from shesaidsail.com → Brand = SSS | Will tests | ☐ |
| E2 | ME brand routing test: form submission from mareexecutive.com → Brand = ME | Luciana tests | ☐ |
| E3 | ⭐ All client-facing email content reviewed by Will for brand voice compliance | Will | ☐ |
| E4 | All client-facing SMS content reviewed by Will for brand voice compliance | Will | ☐ |
| E5 | No prohibited words in any template (amazing, awesome, unforgettable, elite, epic, etc.) | Will confirms | ☐ |
| E6 | Review request template includes correct Google Review URL for each city | Luciana | ☐ |

---

## SECTION F — FINANCIAL READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| F1 | ⭐ Deposit amount calculation verified: Package_Price × 0.5 = correct deposit | Will verifies | ☐ |
| F2 | ⭐ Net margin formula on Bookings verified: outputs correct percentage for a test booking | Will verifies | ☐ |
| F3 | All active Packages have correctly configured pricing (no $0 packages, no unintended pricing) | Luciana | ☐ |
| F4 | ⭐ Tax rates are set correctly for all active cities | Will confirms | ☐ |
| F5 | Refund process documented for operators: who initiates, who approves, what Make does | Will + Luciana | ☐ |
| F6 | P&L Per Charter table in Financials base has Last_Sync_Timestamp and Sync_Status fields | Luciana | ☐ |

---

## SECTION G — GOVERNANCE AND COMPLIANCE READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| G1 | ⭐ Founder Decision created: "Make Stage 1 approved for production" (Type = SYSTEM) | Will creates | ☐ |
| G2 | ⭐ All 8 Stage 1 scenarios have individual Founder Decision records confirming production approval | Will creates | ☐ |
| G3 | Audit_Log immutability rules confirmed: no delete permission set on Audit_Log table | Will | ☐ |
| G4 | AI_Prompt_Versions — Will_Approved = false is confirmed to block scenario execution | Make builder tests | ☐ |
| G5 | All API credentials rotated within last 90 days | Will confirms | ☐ |
| G6 | All API credentials in credential vault — none in Make scenario text directly | Will confirms | ☐ |
| G7 | Backup scenario (BACKUP-001 or equivalent) running daily and last backup successful | Luciana | ☐ |
| G8 | ⭐ This checklist itself is complete — Will has reviewed every item | Will | ☐ |

---

## SECTION H — OPERATIONAL READINESS

| # | Item | Owner | Status |
|---|------|-------|--------|
| H1 | Luciana has reviewed Stage 1 scenario flows and understands what each scenario does | Luciana | ☐ |
| H2 | Luciana knows how to: pause a scenario in Make, check Audit_Log, check #sss-ops-alerts | Luciana | ☐ |
| H3 | Luciana knows the emergency procedure: set Emergency_Flag = true → all automations halt | Luciana | ☐ |
| H4 | Luciana knows the fallback procedure for each scenario failure (manual backup plans) | Luciana | ☐ |
| H5 | Active bookings and open Requests are cleaned up — no test data in production base | Luciana | ☐ |
| H6 | City Manager(s) in active cities are briefed on new automation system — know what emails/Slack DMs to expect | Luciana | ☐ |
| H7 | ⭐ Will has personally executed the full fake lead → booking → payment → confirmation test in production | Will | ☐ |
| H8 | ⭐ Will is satisfied with the test results and authorizes ads to run | Will | ☐ |

---

## SIGN-OFF

When all items are checked:

```
ADS GO-LIVE AUTHORIZATION

Date: _______________
Stage: Stage 1 — Core Operational MVP
All checklist items confirmed: YES

Will Signature: _______________
Date/Time: _______________

Notes: _______________________________________________
```

---

## POST-GO-LIVE MONITORING (FIRST 48 HOURS)

After ads are turned on, Will and Luciana monitor actively for the first 48 hours:

| Hour | Check | Owner |
|------|-------|-------|
| 0–2 | First inbound lead captured and visible in Airtable | Luciana |
| 0–2 | Brand routing correct on first real lead | Luciana |
| 2–24 | First booking created through automation (if lead converts) | Luciana |
| 24 | #sss-ops-alerts reviewed — no unexpected alerts | Luciana |
| 24 | Audit_Log reviewed — entries present for all automated actions | Luciana |
| 48 | ⭐ Will reviews first 48 hours — confirms system operating correctly | Will |
| 48 | Any anomalies documented in Governance_Reviews table | Will / Luciana |

If any SEV-1 event occurs in first 48 hours:
- Ads paused immediately until resolved
- Will investigates personally
- Document in Governance_Reviews before resuming ads

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*PRODUCTION_GO_LIVE_CHECKLIST v1.0*
*Effective May 2026*
