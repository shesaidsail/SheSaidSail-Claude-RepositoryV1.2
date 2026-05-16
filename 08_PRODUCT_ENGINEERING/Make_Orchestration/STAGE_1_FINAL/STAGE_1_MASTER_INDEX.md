# STAGE 1 MASTER INDEX
## She Said Sail — Make Orchestration — Single Authoritative Entry Point

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  
**Owner:** Will Hunt  
**Branch:** `claude/reorganize-stage1-blueprints-kOt7L`  
**Base Commit (main):** `bdfc40e`  
**Directory:** `08_PRODUCT_ENGINEERING/Make_Orchestration/STAGE_1_FINAL/`  
**Classification:** Confidential — Internal Use Only  

> This document is the single entry point for Stage 1 Make orchestration deployment.
> Everything required to import, configure, and run Stage 1 in Make lives in this directory.
> Do not look anywhere else. Do not import blueprints from any other location.

---

## SYSTEM OVERVIEW

Stage 1 automates the core booking acquisition funnel for She Said Sail:

```
Lead Submission → Brand Classification → Request Created
       ↓
Availability Confirmed → Stripe Deposit Link Generated → Deposit Sent
       ↓
Deposit Paid (Stripe Webhook) → Booking Updated → Concierge Assigned
       ↓
Booking Confirmed → Confirmation Email Sent → Audit Logged
```

Every action writes to the immutable Audit Log. Every failure routes to Slack. No step bypasses governance.

---

## AUTHORITATIVE BLUEPRINT FILES

All 8 production-ready blueprints are in `/blueprints`. These are the ONLY authorized files for import.

| # | Blueprint File | Scenario ID | Safe to Import |
|---|---------------|------------|----------------|
| 1 | `blueprints/M-AUDIT-LOGGER.json` | AUDIT-001 | ✅ YES |
| 2 | `blueprints/M-SLACK-ALERTS.json` | ALERTS-001 | ✅ YES |
| 3 | `blueprints/M-BRAND-ROUTER.json` | BRAND-ROUTER-001 | ✅ YES |
| 4 | `blueprints/M-LEAD-INTAKE.json` | INBOUND-001 | ✅ YES |
| 5 | `blueprints/M-STRIPE-DEPOSIT.json` | BOOKING-001 | ✅ YES |
| 6 | `blueprints/M-BOOKING-CREATION.json` | BOOKING-002 | ✅ YES |
| 7 | `blueprints/M-CONCIERGE-ASSIGNMENT.json` | BOOKING-003 | ✅ YES |
| 8 | `blueprints/M-BOOKING-CONFIRMATION.json` | BOOKING-004 | ✅ YES |

**STRIPE NOTE:** `blueprints/M-STRIPE-DEPOSIT.json` uses `http:ActionSendData` calling `https://api.stripe.com/v1/payment_links` with `Stripe-Version: 2023-10-16` header. The deprecated `stripe:ActionCreatePaymentLink` connector is NOT present in any blueprint.

---

## EXACT DEPLOYMENT ORDER

Import and activate in this exact sequence. Each scenario must be live and tested before the next is activated.

| Step | Scenario | Type | Why This Position |
|------|---------|------|-------------------|
| 1 | M-AUDIT-LOGGER | Infrastructure | All scenarios call this first — must exist |
| 2 | M-SLACK-ALERTS | Infrastructure | Error routing required before operational scenarios |
| 3 | M-BRAND-ROUTER | Infrastructure | Called by M-LEAD-INTAKE before any lead processing |
| 4 | M-LEAD-INTAKE | Operational | Depends on steps 1-3 |
| 5 | M-STRIPE-DEPOSIT | Operational | Depends on step 1 |
| 6 | M-BOOKING-CREATION | Operational | Depends on steps 1, 2, 5 |
| 7 | M-CONCIERGE-ASSIGNMENT | Operational | Depends on steps 1, 2, 6 |
| 8 | M-BOOKING-CONFIRMATION | Operational | Depends on steps 1, 7 |

---

## EXACT BLUEPRINT IMPORT ORDER

Same as deployment order. Do not import all 8 at once without reading activation steps.

For full import + activation instructions: `docs/FINAL_STAGE_1_IMPORT_ORDER.md`  
For step-by-step activation with timing: `docs/ACTIVATION_SEQUENCE.md`

---

## REQUIRED CREDENTIALS

Complete credential binding before activating any scenario. Full checklist: `docs/CREDENTIAL_REBINDING_CHECKLIST.md`

### Infrastructure Credentials
| Credential | Source | Required By |
|-----------|--------|-------------|
| `AIRTABLE_PAT` | Airtable > Developer Hub | All scenarios |
| `AIRTABLE_BASE_ID_PRODUCTION` | `appdZ49WqgjRXxA1R` | All scenarios |
| `AUDIT_LOGGER_WEBHOOK_URL` | Generated on M-AUDIT-LOGGER import | All operational scenarios |
| `AUDIT_LOGGER_WEBHOOK_SECRET` | Generate (32-char random) | All operational scenarios |
| `SLACK_ALERTS_WEBHOOK_URL` | Generated on M-SLACK-ALERTS import | M-LEAD-INTAKE, M-BOOKING-CREATION |
| `SLACK_ALERTS_WEBHOOK_SECRET` | Generate (32-char random) | M-SLACK-ALERTS, callers |
| `BRAND_ROUTER_WEBHOOK_URL` | Generated on M-BRAND-ROUTER import | M-LEAD-INTAKE |
| `BRAND_ROUTER_WEBHOOK_SECRET` | Generate (32-char random) | M-BRAND-ROUTER, M-LEAD-INTAKE |

### Platform Credentials
| Credential | Source | Required By |
|-----------|--------|-------------|
| `SLACK_CONNECTION_ID` | Make > Connections > Slack OAuth | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `GMAIL_CONNECTION_ID` | Make > Connections > Gmail OAuth (hello@shesaidsail.com) | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| `STRIPE_SECRET_KEY` | Stripe Dashboard > Restricted Key (payment_links:write) | M-STRIPE-DEPOSIT |
| `STRIPE_WEBHOOK_SIGNING_SECRET` | Stripe Dashboard after webhook registration | M-BOOKING-CREATION |

### Person IDs
| Credential | Source | Required By |
|-----------|--------|-------------|
| `SLACK_WILL_DM_ID` | Slack > Will's profile > Copy member ID | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT |
| `SLACK_LUCIANA_ID` | Slack > Luciana's profile > Copy member ID | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `LUCIANA_AIRTABLE_RECORD_ID` | Airtable > Concierge_Operators or Team_Members table > Luciana's record | M-CONCIERGE-ASSIGNMENT |

---

## REQUIRED WEBHOOKS

Register these external webhooks. Internal Make webhooks are configured automatically.

| # | Platform | Event | Target Scenario | Instructions |
|---|---------|-------|----------------|-------------|
| 1 | Webflow | Form Submission | M-LEAD-INTAKE | `docs/WEBHOOK_REGISTRATION_INSTRUCTIONS.md` |
| 2 | Stripe | `checkout.session.completed` | M-BOOKING-CREATION | `docs/WEBHOOK_REGISTRATION_INSTRUCTIONS.md` |

---

## AIRTABLE DEPENDENCIES

All Stage 1 scenarios read from and write to `appdZ49WqgjRXxA1R` (SSS Operations Production Base).

| Table | Action | Required Fields |
|-------|--------|----------------|
| **Requests** | CREATE (M-LEAD-INTAKE) | Name, Email, Phone, Occasion, Preferred_Date, Guest_Count, Source, Brand, City, Agent_Status, Environment, Source_System, Created_At |
| **Bookings** | UPDATE (M-STRIPE-DEPOSIT) | Status, Package_Price, Client_Name, Client_Email, Charter_Date, Vessel_Name, Package_Name, Guest_Count, Brand, Deposit_Link_Sent, Stripe_Payment_Link_URL, Deposit_Amount |
| **Bookings** | UPDATE (M-BOOKING-CREATION) | Status, Stripe_Deposit_Payment_Intent, Stripe_Deposit_Event_ID, Deposit_Paid_At, Deposit_Amount_Received |
| **Bookings** | UPDATE (M-CONCIERGE-ASSIGNMENT) | Concierge_Assigned (checkbox), Assigned_Concierge (linked record), Concierge_Assigned_At |
| **Bookings** | UPDATE (M-BOOKING-CONFIRMATION) | Confirmation_Sent (checkbox), Confirmation_Sent_At |
| **Audit Log** | CREATE (M-AUDIT-LOGGER) | Audit_UUID, Actor, Action_Type, Scenario_ID, Source_System, Environment, Booking_ID, Request_ID, Client_ID, Before_State, After_State, Payload_Summary, Rollback_Reference, Timestamp |

**Airtable fields that must be created before activation:**
- `Confirmation_Sent` (Checkbox) on Bookings table
- `Concierge_Assigned` (Checkbox) on Bookings table
- `Assigned_Concierge` (Linked Record → Concierge_Operators or Team_Members) on Bookings table
- `Deposit_Link_Sent` (Checkbox) on Bookings table

---

## STRIPE DEPENDENCIES

| Dependency | Value | Purpose |
|-----------|-------|---------|
| Stripe API version | `2023-10-16` | Set via `Stripe-Version` header in M-STRIPE-DEPOSIT |
| Payment Links endpoint | `https://api.stripe.com/v1/payment_links` | Used in M-STRIPE-DEPOSIT |
| Webhook event | `checkout.session.completed` | Received by M-BOOKING-CREATION |
| Required metadata fields | `booking_id`, `airtable_record_id`, `payment_type`, `brand`, `environment` | Set in payment link, read in webhook |
| Restricted key permission | `payment_links:write` | Required for M-STRIPE-DEPOSIT |
| Deprecated module | `stripe:ActionCreatePaymentLink` | NOT USED — removed from all blueprints |

---

## SLACK DEPENDENCIES

| Dependency | Value | Purpose |
|-----------|-------|---------|
| `#sss-ops-alerts` | Operational notification channel | All INFO/SEV-2 alerts |
| `#sss-emergency-ops` | Emergency channel | SEV-1 alerts only |
| Will's member ID | `SLACK_WILL_DM_ID` | SEV-1 alerts, HV client notifications |
| Luciana's member ID | `SLACK_LUCIANA_ID` | Concierge assignment DMs, HV Tier B review |
| Slack OAuth app | SSS workspace app | Connected via Make Connections |

---

## ANTHROPIC DEPENDENCIES

Stage 1 does NOT include any direct Claude API calls. All 8 Stage 1 scenarios handle data routing, webhook processing, Stripe operations, and notification delivery.

Anthropic/Claude dependencies begin in Stage 2 (M-INBOUND-RESPONSE-AGENT — INBOUND-002).

---

## TESTING SEQUENCE

Quick reference. Full test cases: `docs/TESTING_CHECKLIST.md`

| Phase | Test | Expected Result |
|-------|------|----------------|
| T-1 | POST to M-AUDIT-LOGGER webhook | Airtable Audit Log record created |
| T-2 | POST SEV-1 to M-SLACK-ALERTS | #sss-emergency-ops + Will DM |
| T-3 | POST to M-BRAND-ROUTER with source=shesaidsail.com | Response: brand=SSS |
| T-4 | Submit Webflow form | Airtable Request created, Slack notified, Audit logged |
| T-5 | Set Booking to AVAILABILITY_CONFIRMED | Stripe Payment Link created, Booking=DEPOSIT_SENT, email sent |
| T-6 | Stripe test webhook: checkout.session.completed | Booking=DEPOSIT_PAID, Slack notified, Audit logged |
| T-7 | Booking at DEPOSIT_PAID | Luciana DM sent, Concierge assigned |
| T-8 | Booking at CONFIRMED | Client confirmation email sent, Audit logged |
| T-9 | Repeat T-4 with same email within 24h | No duplicate Request created |
| T-10 | Repeat T-6 with same Stripe event ID | No duplicate Booking update |

---

## ROLLBACK SEQUENCE

Deactivate in this order if rollback required. Full instructions: `docs/ROLLBACK_ORDER.md`

1. M-BOOKING-CONFIRMATION → Deactivate
2. M-CONCIERGE-ASSIGNMENT → Deactivate
3. M-BOOKING-CREATION → Deactivate
4. M-STRIPE-DEPOSIT → Deactivate
5. M-LEAD-INTAKE → Deactivate
6. M-BRAND-ROUTER → Deactivate
7. M-SLACK-ALERTS → Deactivate (if necessary)
8. M-AUDIT-LOGGER → Deactivate (last resort only)

---

## WHICH FILES ARE AUTHORITATIVE

| Location | Authority Level | Use For |
|----------|----------------|---------|
| `blueprints/*.json` | AUTHORITATIVE — only these files | Blueprint import into Make |
| `docs/FINAL_STAGE_1_IMPORT_ORDER.md` | AUTHORITATIVE | Import order and post-import steps |
| `docs/ACTIVATION_SEQUENCE.md` | AUTHORITATIVE | Day-by-day activation guide |
| `docs/CREDENTIAL_REBINDING_CHECKLIST.md` | AUTHORITATIVE | All credentials per scenario |
| `docs/WEBHOOK_REGISTRATION_INSTRUCTIONS.md` | AUTHORITATIVE | Webflow and Stripe webhook setup |
| `docs/ROLLBACK_ORDER.md` | AUTHORITATIVE | Rollback and manual fallbacks |
| `docs/TESTING_CHECKLIST.md` | AUTHORITATIVE | Pre-production test sign-off |
| `docs/DEPLOYMENT_INSTRUCTIONS.md` | AUTHORITATIVE | Full deployment process |
| `docs/Make_Native_Module_Gap_Audit.md` | AUTHORITATIVE | Module decisions and known gaps |
| `reference/Make_Native_Module_Reference_Master.md` | REFERENCE | Module syntax and parameters |
| `reference/MODULE_INVENTORY.md` | REFERENCE | Module count and external call map |
| `reference/MODULE_COMPATIBILITY_NOTES.md` | REFERENCE | Compatibility rules per module type |
| `reference/VERIFIED_NATIVE_MODULE_FINDINGS.md` | REFERENCE | Research findings, deprecation record |
| `archive/ARCHIVE_INDEX.md` | ARCHIVE | Deprecated file log |
| `STAGE_1_MASTER_INDEX.md` | AUTHORITATIVE | This file — entry point |

---

## BRANCH AND COMMIT INFORMATION

| Field | Value |
|-------|-------|
| Working branch | `claude/reorganize-stage1-blueprints-kOt7L` |
| Base commit (main) | `bdfc40e` — Merge Phase 3 Fragmented Base Migration Report |
| Stage 1 created | `2026-05-16` |
| Repository | `shesaidsail/shesaidsail-claude-repositoryv1.2` |

---

## SAFE TO IMPORT STATUS

| Blueprint | Deprecated Module | Placeholder Corruption | Missing Modules | Make Compatible | SAFE TO IMPORT |
|-----------|------------------|----------------------|----------------|----------------|----------------|
| M-AUDIT-LOGGER | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-SLACK-ALERTS | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-BRAND-ROUTER | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-LEAD-INTAKE | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-STRIPE-DEPOSIT | ❌ None (deprecated module removed) | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-BOOKING-CREATION | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-CONCIERGE-ASSIGNMENT | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |
| M-BOOKING-CONFIRMATION | ❌ None | ❌ None | ❌ None | ✅ Yes | ✅ YES |

**All 8 blueprints are SAFE TO IMPORT.**

Note: `{{VARIABLE}}` tokens in all blueprints are intentional credential placeholders, not placeholder corruption. They must be replaced with real values during credential binding per `docs/CREDENTIAL_REBINDING_CHECKLIST.md`.

---

## REMAINING BLOCKERS

| Blocker | Severity | Resolution |
|---------|---------|-----------|
| Stripe webhook signature validation not implemented natively | MEDIUM | Add Stripe-Signature header validation in M-BOOKING-CREATION post-import. Workaround: Stripe IP allowlist. See `docs/Make_Native_Module_Gap_Audit.md`. |
| `Confirmation_Sent` checkbox field may not exist in Bookings table | HIGH | Create field in Airtable before activating M-BOOKING-CONFIRMATION. |
| `Concierge_Assigned` checkbox and `Assigned_Concierge` linked record fields may not exist | HIGH | Create fields in Airtable before activating M-CONCIERGE-ASSIGNMENT. |
| `AIRTABLE_BASE_ID_ME` not confirmed | MEDIUM | Confirm Mare Executive base ID from Airtable before activating M-BRAND-ROUTER in ME configuration. SSS routing works without it. |
| Webflow hidden brand field may not exist | MEDIUM | Add `brand` hidden field to Webflow forms before activating M-LEAD-INTAKE. Fallback: URL-based detection active. |

---

## CENTRALIZATION STATUS

✅ All 8 Stage 1 blueprint JSON files — located in `blueprints/`  
✅ All operational documentation — located in `docs/`  
✅ All reference material — located in `reference/`  
✅ Archive directory initialized — located in `archive/`  
✅ Master index (this file) — `STAGE_1_MASTER_INDEX.md`  
✅ No conflicting blueprint versions in other locations (Stage 1 blueprints were not previously committed)  
✅ All internal file paths verified — every referenced file exists  
✅ System can be deployed from this folder alone  

**STAGE 1 IS FULLY CENTRALIZED AND DEPLOYMENT-READY.**

---

*She Said Sail · Stage 1 Make Orchestration · Master Index*  
*Built for permanence. Optimized for scale. Designed for acquisition readiness.*  
*CONFIDENTIAL — INTERNAL USE ONLY · MAY 2026*
