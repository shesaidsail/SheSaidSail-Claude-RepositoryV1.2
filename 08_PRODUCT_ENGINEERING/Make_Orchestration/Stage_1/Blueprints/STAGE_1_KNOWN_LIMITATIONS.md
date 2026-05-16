# STAGE 1 KNOWN LIMITATIONS
**Version:** 1.0
**Date:** 2026-05-16
**Project:** She Said Sail + Mare Executive — Make Orchestration Stage 1

---

## Category 1 — Make Blueprint Import Limitations

### L-001: Credentials Are Never Exported
**Impact:** HIGH — affects all 8 scenarios
**Description:** Make.com explicitly prevents credential export in blueprint files. Every connection (Airtable, Slack, Gmail, Stripe, SMS) must be manually reconnected after each blueprint import. There is no workaround.
**Mitigation:** CREDENTIAL_REBINDING_CHECKLIST.md provides a per-module checklist to ensure no module is left disconnected.

### L-002: Webhook URLs Are Always Regenerated
**Impact:** HIGH — affects all 8 scenarios
**Description:** Make generates a new, unique webhook URL each time a blueprint is imported. You cannot preserve or predict the URL. All `INSERT_MAKE_WEBHOOK_URL_AFTER_IMPORT` placeholders must be manually replaced after import.
**Mitigation:** Import in the documented order (IMPORT_MANIFEST.md), capture each URL immediately, and propagate per WEBHOOK_REGISTRATION_CHECKLIST.md.

### L-003: Module Version Warnings on Import
**Impact:** LOW — cosmetic only
**Description:** When a blueprint is imported against a slightly newer or older version of a Make module, Make may display warnings about unrecognized module versions. This does not prevent import but requires manual verification of module configuration.
**Mitigation:** After import, verify all router conditions, field mappings, and filter operators match the spec files.

### L-004: Router Filter Conditions Require Manual Review
**Impact:** MEDIUM — functional risk
**Description:** Complex router filter conditions (especially nested AND/OR logic and Make formula expressions) may not serialize perfectly across all Make versions. The import may succeed but conditions may be incomplete.
**Mitigation:** After import, open each router module and manually verify filter conditions match the spec. See per-scenario spec files in `specs/` for exact expected conditions.

### L-005: Error Handler Modules Are Not Fully Representable in Blueprint JSON
**Impact:** MEDIUM — error handling risk
**Description:** Make's error handler configuration (the "break" module connected via error routing) is partially represented in blueprint JSON but may require manual reconnection in the Make scenario editor after import.
**Mitigation:** After importing each scenario, verify the error handler route is connected by checking the scenario in the Make editor. The spec files document the expected error handler behavior for each scenario.

---

## Category 2 — Airtable Dependency Limitations

### L-006: New Tables Do Not Have Known Table IDs
**Impact:** HIGH — blocking for M-AUDIT-LOGGER and M-CONCIERGE-ASSIGNMENT
**Description:** Two tables required by Stage 1 scenarios — `Automation_Health` and `Concierge_Operators` — are new tables that must be created in Airtable. Their Table IDs (format: `tblXXXXXXXXXXXXXX`) are not known until the tables are created. Blueprint placeholders `AUTOMATION_HEALTH_TABLE_ID` and `CONCIERGE_OPERATORS_TABLE_ID` cannot be pre-filled.
**Mitigation:** Create the tables in Airtable first, retrieve their IDs from the Airtable API or URL, then update the Make scenarios before activating.

### L-007: Cross-Base Linked Records Not Possible
**Impact:** HIGH — architectural constraint
**Description:** Airtable does not support linked records between different bases. The SSS Financials base (apprDKQtV2GInThwE) cannot have linked record fields to the SSS Operations base (appdZ49WqgjRXxA1R). Stage 1 scenarios work entirely within the Operations base and write to Financials base via plain text Booking_ID fields only.
**Mitigation:** Stage 1 scenarios are scoped to the Operations base only. Stage 2 will implement the Make-driven sync between bases.

### L-008: Bookings Table at 129 Fields — Performance Risk
**Impact:** MEDIUM — performance degradation risk
**Description:** The Bookings table currently has 129 fields. Make modules reading this table via Airtable API must process all 129 fields per record. This increases API response time and may approach Airtable API payload limits for records with large Long Text fields.
**Mitigation:** Stage 1 Airtable modules use field selection where possible. The Bookings table optimization (reduce to 70 fields) is a Stage 1 prerequisite task documented in the Airtable Field Patch Report.

### L-009: Concierge_Operators Table Has No Live Records
**Impact:** HIGH — M-CONCIERGE-ASSIGNMENT will fail "No Concierge Available" path until records exist
**Description:** The Concierge_Operators table must be populated with active concierge records before M-CONCIERGE-ASSIGNMENT can successfully assign anyone. At import time, the table will be empty.
**Mitigation:** After creating the Concierge_Operators table, populate it with at least one active record per city/brand combination before activating M-CONCIERGE-ASSIGNMENT in production. Use the "No Concierge Available" sandbox test to verify the fallback path works while records are pending.

---

## Category 3 — Stripe Integration Limitations

### L-010: Stripe Webhook Signature Validation Is Configuration-Dependent
**Impact:** HIGH — security and reliability
**Description:** M-BOOKING-CREATION receives Stripe webhooks. Stripe recommends validating the webhook signature (using the `Stripe-Signature` header and the webhook signing secret). Make's native Stripe module handles this automatically when configured correctly, but if the signing secret is not added after import, signature validation does not run.
**Mitigation:** After importing M-BOOKING-CREATION and registering the Stripe webhook, add the signing secret to the Stripe connection in Make immediately. Do NOT activate production until this is confirmed.

### L-011: Stripe Payment Link Success URL Is Hardcoded
**Impact:** LOW — requires manual update if URL changes
**Description:** M-STRIPE-DEPOSIT creates Stripe Payment Links with a hardcoded success URL: `https://shesaidsail.com/booking-confirmed`. If this URL does not yet exist or needs to be different for ME brand bookings, it must be updated manually in the scenario.
**Mitigation:** Verify the success URL exists before activating M-STRIPE-DEPOSIT in production. Create a separate success URL for ME bookings if needed and update the ME route in M-STRIPE-DEPOSIT.

### L-012: No Stripe Partial-Failure Recovery in Stage 1
**Impact:** MEDIUM — operational risk
**Description:** If M-STRIPE-DEPOSIT creates a Stripe Payment Link successfully but the subsequent Airtable update fails (e.g., network timeout), the link exists in Stripe but the Booking record is not updated. There is no automatic recovery mechanism in Stage 1.
**Mitigation:** Monitor M-STRIPE-DEPOSIT for errors in Make execution logs. If an error occurs after Stripe link creation, manually retrieve the link from the Stripe Dashboard using the booking_id in the metadata, and manually update the Airtable Booking record. Stage 2 will implement idempotency recovery.

---

## Category 4 — Communication Limitations

### L-013: Quo SMS API Integration Requires Manual HTTP Configuration
**Impact:** MEDIUM — SMS functionality depends on correct HTTP module setup
**Description:** Quo SMS is not a native Make connector. SMS modules use the HTTP module with a custom API endpoint and authentication header. The exact Quo SMS API endpoint format and authentication scheme must be verified against the current Quo SMS API documentation after import.
**Mitigation:** Before activating SMS modules, verify the Quo SMS API endpoint URL, authentication header format, and request body structure against the live Quo SMS API documentation. Update HTTP module configuration accordingly.

### L-014: Gmail OAuth Tokens May Expire
**Impact:** LOW — recoverable
**Description:** Gmail OAuth tokens used in Make connections expire periodically and must be reauthorized. If a Gmail connection expires, all Gmail modules across all scenarios will fail silently (the scenario may not show an error until the module runs).
**Mitigation:** Set up Make alert emails for connection failures. Reauthorize Gmail connections in Make when prompted.

---

## Category 5 — Stage Boundary Limitations

### L-015: Stage 1 Does Not Include Scheduled Automations
**Impact:** MEDIUM — post-charter follow-up requires Stage 2
**Description:** Stage 1 is webhook-triggered only. Scheduled automations (D7 review request, D30 referral, weekly P&L digest, 72-hour reminder) are Stage 2–4 scenarios. Stage 1 covers only the booking funnel (lead → deposit → booking → confirmation).
**Mitigation:** This is by design. Do not attempt to add scheduled triggers to Stage 1 scenarios. Document any interim manual processes for post-confirmation follow-up until Stage 2 is deployed.

### L-016: No AI/Claude Integration in Stage 1
**Impact:** MEDIUM — manual response handling
**Description:** Stage 1 does not include Claude API integration for response drafting or lead qualification. All AI features (Inbound Response Agent, context injection, confidence scoring) are Stage 2–4. Request records created by M-LEAD-INTAKE will have Agent_Status="HUMAN_REVIEW" and require Luciana to handle manually.
**Mitigation:** This is by design. Ensure Luciana is monitoring the Requests table and #sss-leads Slack channel for incoming leads.

### L-017: Charter Brief Generation Not Included in Stage 1
**Impact:** LOW — operational process gap
**Description:** Automated Charter Brief generation is not part of Stage 1. After M-BOOKING-CONFIRMATION creates a confirmed booking, the Charter Brief must be created manually.
**Mitigation:** Track as a Stage 2 requirement.

---

## Summary Risk Assessment

| Limitation | Severity | Blocking | Stage 1 Workaround Available |
|------------|----------|---------|------------------------------|
| L-001 Credentials not exported | HIGH | YES — requires manual action | YES — checklist provided |
| L-002 Webhook URLs regenerated | HIGH | YES — requires manual action | YES — propagation map provided |
| L-003 Module version warnings | LOW | NO | YES — manual verification |
| L-004 Router conditions need review | MEDIUM | NO | YES — spec files provided |
| L-005 Error handler wiring | MEDIUM | NO | YES — manual check required |
| L-006 New table IDs unknown | HIGH | YES | YES — create tables first |
| L-007 Cross-base links not possible | HIGH | NO (Stage 1 scope correct) | N/A |
| L-008 129-field Bookings table | MEDIUM | NO | YES — field selection in modules |
| L-009 No concierge records yet | HIGH | YES (for prod) | YES — sandbox test only until populated |
| L-010 Stripe signature validation | HIGH | NO (security risk if skipped) | YES — add signing secret post-import |
| L-011 Hardcoded success URL | LOW | NO | YES — verify URL exists |
| L-012 Stripe partial failure recovery | MEDIUM | NO | YES — manual recovery procedure |
| L-013 Quo SMS HTTP config | MEDIUM | NO | YES — verify API docs post-import |
| L-014 Gmail token expiry | LOW | NO | YES — monitor and reauthorize |
| L-015 No scheduled automations | MEDIUM | NO (Stage 2) | N/A |
| L-016 No AI integration | MEDIUM | NO (Stage 2) | YES — human review workflow |
| L-017 No Charter Brief automation | LOW | NO (Stage 2) | YES — manual creation |
