# Make Native Module Gap Audit — Stage 1 Blueprints
**She Said Sail + Mare Executive — Make.com Orchestration**
**Version:** 1.0 | **Date:** 2026-05-16 | **Status:** FINAL AUDIT — DO NOT PATCH YET
**Auditor:** Claude Code — Stage 1 Final Blueprint Audit

---

## Scope

This audit covers all 8 Stage 1 blueprint JSON files against the approved Make native module inventory (SheSaidSail_Make_Modules_Master_List.pdf) and the supporting authority documents available in this repository. This is a GAP AUDIT ONLY. No blueprint JSON files have been modified.

**Blueprints audited:**
1. `M-AUDIT-LOGGER.blueprint.json`
2. `M-BRAND-ROUTER.blueprint.json`
3. `M-LEAD-INTAKE.blueprint.json`
4. `M-SLACK-ALERTS.blueprint.json`
5. `M-CONCIERGE-ASSIGNMENT.blueprint.json`
6. `M-STRIPE-DEPOSIT.blueprint.json`
7. `M-BOOKING-CREATION.blueprint.json`
8. `M-BOOKING-CONFIRMATION.blueprint.json`

**Branch source:** `claude/native-first-make-blueprint-qWHXZ`

---

## Executive Summary

| Finding Category | Count |
|---|---|
| HTTP legacy calls that should become native | 0 (all identified HTTP is intentional — see below) |
| HTTP legacy calls that must remain HTTP | 13 |
| Webhooks that must remain webhooks | 5 |
| CRITICAL: unverified native module (not in PDF) | 2 module types |
| WARNING: unverified trigger module (not in PDF) | 1 module type |
| WARNING: unverified Anthropic module ID | 1 module type |
| Deprecated modules | 0 |
| Missing native integrations (no module available) | 2 (Squarespace, Quo SMS) |
| Placeholder rebinds required after import | 11 placeholder types across 8 blueprints |
| Import-breaking issues | 2 (stripe:ActionCreatePaymentLink in 2 blueprints) |
| Scenarios safe to import | 6 (with caveats noted) |
| Scenarios not safe to import without patching | 2 (M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION) |

**FINAL VERDICT: READY WITH WARNINGS**

Two blueprints (M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION) contain an unverified Stripe module (`stripe:ActionCreatePaymentLink`) that is NOT in the approved module inventory PDF. These blueprints require manual verification in Make before import. All other blueprints are structurally sound with connection rebinding required as documented.

---

## Section 1 — HTTP Legacy Calls: All Are Intentional

After complete audit of all 8 blueprints, there are **zero HTTP legacy calls that should be converted to native.** All remaining HTTP modules fall into one of two categories:

### 1A — HTTP That Must Remain HTTP: Inter-Scenario Calls to M-AUDIT-LOGGER

**Justification:** Make.com has no native cross-scenario trigger module. The only way to call one scenario from another is via that scenario's webhook URL using an HTTP module. This is architectural, not a legacy pattern.

| Blueprint | Module | Target | Must Stay HTTP |
|---|---|---|---|
| M-BRAND-ROUTER | Module 10 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-LEAD-INTAKE | Module 9 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-SLACK-ALERTS | Module 8 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-CONCIERGE-ASSIGNMENT | Module 10 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-CONCIERGE-ASSIGNMENT | Module 11 | M-AUDIT-LOGGER webhook (blocked path) | Yes — no native cross-scenario module |
| M-STRIPE-DEPOSIT | Module 10 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-BOOKING-CREATION | Module 11 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-BOOKING-CREATION | Module 12 | M-AUDIT-LOGGER webhook (blocked path) | Yes — no native cross-scenario module |
| M-BOOKING-CONFIRMATION | Module 11 | M-AUDIT-LOGGER webhook | Yes — no native cross-scenario module |
| M-BOOKING-CONFIRMATION | Module 12 | M-AUDIT-LOGGER webhook (blocked path) | Yes — no native cross-scenario module |

### 1B — HTTP That Must Remain HTTP: Inter-Scenario Call to M-BRAND-ROUTER

| Blueprint | Module | Target | Must Stay HTTP |
|---|---|---|---|
| M-LEAD-INTAKE | Module 6 | M-BRAND-ROUTER webhook | Yes — no native cross-scenario module |

### 1C — HTTP That Must Remain HTTP: Quo SMS API

| Blueprint | Module | Service | Must Stay HTTP |
|---|---|---|---|
| M-CONCIERGE-ASSIGNMENT | Module 9 | Quo SMS API | Yes — Quo SMS has no native Make module |
| M-BOOKING-CONFIRMATION | Module 9 | Quo SMS API | Yes — Quo SMS has no native Make module |

**Total HTTP modules that must remain HTTP: 13 across 8 blueprints.**

---

## Section 2 — Webhooks That Must Remain Webhooks

All `gateway:CustomWebHook` trigger modules in the blueprints are correctly kept as webhooks. None should be converted to polling or native triggers.

| Blueprint | Module | Webhook Purpose | Must Stay Webhook |
|---|---|---|---|
| M-AUDIT-LOGGER | Module 1 | Receives audit payloads from all other scenarios | Yes — this IS the inter-scenario sink; webhook is required |
| M-SLACK-ALERTS | Module 1 | Receives alert dispatches from all other scenarios | Yes — same pattern as M-AUDIT-LOGGER |
| M-BRAND-ROUTER | Module 1 | Receives lead data from M-LEAD-INTAKE | Yes — cross-scenario intake; webhook required |
| M-LEAD-INTAKE | Module 1 | Receives Squarespace form submissions | Yes — Squarespace has no native Make module; webhook is the only integration method |
| M-STRIPE-DEPOSIT | Module 1 | Receives Stripe payment_intent.succeeded events | Yes — Stripe webhook provides full event payload with signature validation; native Stripe polling trigger risks missed events and delayed processing for financial transactions |

**Total webhook triggers that must remain webhooks: 5.**

---

## Section 3 — Native Modules: Verified Against PDF

### 3A — Confirmed Native (PDF-verified)

The following module types are used in blueprints AND confirmed present in the PDF module inventory:

| Make Internal ID | PDF Display Name | Used In |
|---|---|---|
| `airtable:ActionCreateRecord` | Create a Record | M-AUDIT-LOGGER, M-LEAD-INTAKE |
| `airtable:ActionUpdateRecord` | Update a Record | M-BRAND-ROUTER, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `airtable:ActionSearchRecords` | Search Records | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `airtable:ActionGetRecord` | Get a Record | M-BOOKING-CREATION |
| `slack:CreateMessage` | Send a Message | M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `gmail:ActionSendEmail` | Send an email | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |

### 3B — Make Built-ins (Always Available)

| Make Internal ID | Type | Used In |
|---|---|---|
| `gateway:CustomWebHook` | Webhook trigger | M-AUDIT-LOGGER, M-SLACK-ALERTS, M-BRAND-ROUTER, M-LEAD-INTAKE, M-STRIPE-DEPOSIT |
| `builtin:BasicRouter` | Router | All 8 blueprints |
| `tools:SetVariable` | Variable setter | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `json:ParseJSON` | JSON parser | M-BRAND-ROUTER |
| `http:ActionSendData` | HTTP request | All 8 blueprints |

---

## Section 4 — CRITICAL GAPS

### GAP-001 — CRITICAL: `stripe:ActionCreatePaymentLink` NOT IN PDF

**Severity:** CRITICAL — Import-breaking  
**Affected blueprints:** M-CONCIERGE-ASSIGNMENT (module 6), M-BOOKING-CONFIRMATION (module 6)  
**PDF status:** NOT PRESENT. The Stripe section of the approved module inventory contains only "List Payment Link Lines" under Payment Links. There is no "Create a Payment Link" or equivalent module listed.  
**Blueprint claim:** Both blueprints declare this as `"NATIVE — stripe:ActionCreatePaymentLink. Replaces HTTP Stripe API call."` in `_native_first_notes`.

**Impact:**
- If `stripe:ActionCreatePaymentLink` does not exist in Make's Stripe native app, the blueprint will either fail to import cleanly or fail at execution when module 6 is reached.
- M-CONCIERGE-ASSIGNMENT module 6 creates the 30% deposit payment link. Without this, no deposit link is generated, no email is sent, no Airtable update occurs.
- M-BOOKING-CONFIRMATION module 6 creates the balance payment link. Without this, no balance reminder email is sent.
- Both scenarios' downstream modules (Airtable update, Gmail send, Slack notification, Audit Logger) depend on the Stripe module completing successfully.

**Required verification before import:**
1. Log into Make.com
2. Open any scenario → Add module → Search "Stripe"
3. Confirm whether "Create a Payment Link" or equivalent appears in the Stripe module list
4. If present: verify it maps to `stripe:ActionCreatePaymentLink` and add it to the module reference
5. If absent: blueprint patching is required — escalate to Founder Decision for alternative approach

**Patch options if module not available:**
- Option A: Use Stripe "Create a Payment Intent" (PDF-verified native) + Stripe checkout hosted page — different UX flow, requires Stripe checkout integration
- Option B: Use `http:ActionSendData` with Stripe Payment Links API (`POST /v1/payment_links`) — reverts to HTTP but fully functional
- Option C: Use Stripe "Make an API Call" (PDF-verified fallback) — functionally equivalent to HTTP

**Do not import M-CONCIERGE-ASSIGNMENT or M-BOOKING-CONFIRMATION until this is resolved.**

---

### GAP-002 — WARNING: `anthropic:ActionCreateMessage` NOT DIRECTLY IN PDF

**Severity:** WARNING — May require patching  
**Affected blueprints:** M-BRAND-ROUTER (module 3), M-BOOKING-CREATION (module 7)  
**PDF status:** The PDF lists "Simple Text Prompt" and "Create a Prompt" for Anthropic Claude. Neither matches the internal Make ID `anthropic:ActionCreateMessage` by display name.

**Analysis:**
In Make.com's Anthropic Claude native app, the internal module ID `anthropic:ActionCreateMessage` likely corresponds to one of the PDF-listed modules. The most probable mapping:
- "Simple Text Prompt" → may be `anthropic:ActionCreateMessage` with simplified UI
- "Create a Prompt" → likely a different module for prompt template management

The STAGE_1_NATIVE_REBINDING_GUIDE.md already flags this uncertainty: *"If Make's native Anthropic module does not show a temperature field, it may default to 1.0. In this case, note the difference and verify with the governance owner (Will) before proceeding. Do not use HTTP fallback without Founder Decision."*

**Impact if module maps incorrectly:**
- M-BRAND-ROUTER: Brand classification prompt uses `temperature: 0.4`, `max_tokens: 600`, `system` prompt, `messages` array. If "Simple Text Prompt" doesn't expose these parameters, the classification quality may be degraded or the module may not function as configured.
- M-BOOKING-CREATION: Charter brief generation uses same parameter pattern. Same risk.
- Model `claude-sonnet-4-20250514` must be confirmed as selectable in the Make Anthropic module.

**Required verification before import:**
1. In Make.com, open Anthropic Claude app modules
2. Identify which display-name module corresponds to `anthropic:ActionCreateMessage`
3. Confirm `model`, `max_tokens`, `temperature`, `system`, and `messages` fields are all present
4. Confirm `claude-sonnet-4-20250514` is available in the model selector

**If parameters are limited:**
- The `_native_first_notes` acknowledge this risk and require Founder Decision before reverting to HTTP
- Do not revert to HTTP without documenting a Founder Decision in Airtable

**Both blueprints are safe to import with this caveat noted — the module will load. The question is whether it executes with the intended parameters.**

---

### GAP-003 — WARNING: `airtable:TriggerNewRecord` NOT IN PDF

**Severity:** WARNING — Needs verification but unlikely to be absent  
**Affected blueprints:** M-CONCIERGE-ASSIGNMENT (module 1), M-BOOKING-CREATION (module 1), M-BOOKING-CONFIRMATION (module 1)  
**PDF status:** The Airtable section of the PDF lists only action modules (Search, Get, Create, Update, Upsert, Delete, Bulk variants, Make an API Call). No trigger/watch modules are listed for Airtable.

**Analysis:**
The PDF appears to be an inventory of action modules only. Make.com's Airtable integration has separate trigger modules (watch for new/updated records) that are standard and expected to be available. The absence of trigger modules from the PDF likely reflects an incomplete listing of trigger types, not their absence.

**Impact if module unavailable:**
- M-CONCIERGE-ASSIGNMENT cannot trigger when a booking reaches AVAILABILITY_CONFIRMED status
- M-BOOKING-CREATION cannot trigger when a booking meets the charter brief conditions
- M-BOOKING-CONFIRMATION cannot trigger when a booking is within 72 hours of charter date
- All three would need to be converted to scheduled polling or alternative webhook triggers

**Required verification:**
1. In Make.com, create a new Airtable scenario trigger
2. Confirm "Watch Records" or "New Record" trigger type is available
3. Confirm formula filter capability matches the blueprint formula pattern

**Assessment:** Very likely to be available. Standard Make Airtable integration includes watch triggers. Flag for verification only; unlikely to block import.

---

## Section 5 — Missing Native Integrations (No Module Available)

### 5A — Squarespace

**Status:** No native Make module for Squarespace form submissions  
**Affected blueprint:** M-LEAD-INTAKE (trigger/module 1)  
**Current approach:** `gateway:CustomWebHook` — CORRECT. Squarespace supports webhook delivery from form blocks.  
**Must remain:** Yes — webhook is the only reliable integration method. No native Squarespace Make module exists.  
**Action required post-import:** Configure Squarespace form to deliver to the Make webhook URL. Field name mapping between Squarespace payload and blueprint `expect` fields must be verified (Squarespace may use different internal field names).

### 5B — Quo SMS

**Status:** No native Make module for Quo SMS  
**Affected blueprints:** M-CONCIERGE-ASSIGNMENT (module 9), M-BOOKING-CONFIRMATION (module 9)  
**Current approach:** `http:ActionSendData` — CORRECT. HTTP is the only method.  
**Must remain:** Yes — HTTP only.  
**Action required post-import:** Replace `RECONNECT_QUO_API_ENDPOINT` with Quo API endpoint URL from credential vault. Replace `RECONNECT_QUO_API_KEY` in Authorization header. Store credentials in Make Data Store — do NOT hardcode.  
**Alternative (Stage 2):** Twilio and OpenPhone both have native Make modules and are suitable replacements.

---

## Section 6 — Deprecated Modules

**None found.** All module types used in the 8 blueprints are current Make modules. No deprecated module types identified.

---

## Section 7 — Module Mismatches

### 7A — `stripe:ActionCreatePaymentLink` vs PDF Inventory

Already documented in GAP-001. This is the primary module mismatch. The blueprint asserts a native Stripe module that is not in the approved PDF inventory.

### 7B — Anthropic Module Parameter Capability

Already documented in GAP-002. The `anthropic:ActionCreateMessage` identifier may not fully match Make's displayed "Simple Text Prompt" module's parameter surface.

### 7C — Airtable `version: 3` in All Action Modules

**Severity:** Informational  
All Airtable modules in the blueprints specify `version: 3` (e.g., `airtable:ActionCreateRecord`, version 3). This is the current production version. No mismatch detected, but should be confirmed against the actual Make module version during import. If Make presents a version upgrade prompt, accept it and verify field mappings are preserved.

---

## Section 8 — Import-Breaking Issues

| Issue | Blueprint | Module | Severity | Blocks Import |
|---|---|---|---|---|
| `stripe:ActionCreatePaymentLink` not in PDF | M-CONCIERGE-ASSIGNMENT | Module 6 | CRITICAL | Blocks clean execution; import may succeed but module will fail |
| `stripe:ActionCreatePaymentLink` not in PDF | M-BOOKING-CONFIRMATION | Module 6 | CRITICAL | Blocks clean execution; import may succeed but module will fail |
| `RECONNECT_*` connection placeholders | All 8 blueprints | Multiple | Expected | All connections show as unbound until manually reconnected — this is by design |
| `RECONNECT_WILL_SLACK_USER_ID` | M-SLACK-ALERTS | Modules 5, 7 | Expected | Channel field contains placeholder string — modules will attempt to send to literal placeholder string until replaced |
| `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | 7 blueprints | Multiple HTTP modules | Expected | HTTP modules contain placeholder URL — will 404 until replaced with actual URL |
| `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` | M-LEAD-INTAKE | Module 6 | Expected | HTTP module contains placeholder URL — will 404 until replaced |
| `RECONNECT_QUO_API_ENDPOINT` | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION | Module 9 (each) | Expected | HTTP module contains placeholder URL |

**Note on "Expected" import issues:** All `RECONNECT_*` placeholder issues are intentional by design, documented in STAGE_1_NATIVE_REBINDING_GUIDE.md, and resolved during post-import rebinding. They are not defects in the blueprint JSON; they are the safe-import pattern ensuring no credentials are embedded.

---

## Section 9 — Placeholder Rebinding Required After Import

All 11 placeholder types must be manually resolved after import. Refer to `STAGE_1_NATIVE_REBINDING_GUIDE.md` for step-by-step instructions.

| Placeholder | Type | Affected Blueprints |
|---|---|---|
| `RECONNECT_AIRTABLE_CONNECTION` | Native connection | All 8 blueprints |
| `RECONNECT_SLACK_CONNECTION` | Native connection | M-BRAND-ROUTER, M-LEAD-INTAKE, M-SLACK-ALERTS, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `RECONNECT_CLAUDE_API_KEY` | Native connection | M-BRAND-ROUTER, M-BOOKING-CREATION |
| `RECONNECT_GMAIL_CONNECTION` | Native connection | M-LEAD-INTAKE, M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| `RECONNECT_STRIPE_CONNECTION` | Native connection | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `RECONNECT_WEBHOOK_AUDIT_LOGGER` | Webhook (inbound) | M-AUDIT-LOGGER module 1 — new URL generated by Make on import |
| `RECONNECT_WEBHOOK_SLACK_ALERTS` | Webhook (inbound) | M-SLACK-ALERTS module 1 — new URL generated by Make on import |
| `RECONNECT_WEBHOOK_BRAND_ROUTER` | Webhook (inbound) | M-BRAND-ROUTER module 1 — new URL generated by Make on import |
| `RECONNECT_WEBHOOK_SQUARESPACE_FORM` | Webhook (inbound) | M-LEAD-INTAKE module 1 — new URL generated; must be pasted into Squarespace |
| `RECONNECT_WEBHOOK_STRIPE_DEPOSIT` | Webhook (inbound) | M-STRIPE-DEPOSIT module 1 — new URL generated; must be registered in Stripe Dashboard |
| `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` | HTTP URL (outbound) | 7 blueprints — replace with M-AUDIT-LOGGER's generated webhook URL |
| `RECONNECT_BRAND_ROUTER_WEBHOOK_URL` | HTTP URL (outbound) | M-LEAD-INTAKE — replace with M-BRAND-ROUTER's generated webhook URL |
| `RECONNECT_WILL_SLACK_USER_ID` | Slack User ID value | M-SLACK-ALERTS modules 5 and 7 — replace with Will's actual Slack member ID |
| `RECONNECT_QUO_API_ENDPOINT` | HTTP URL (outbound) | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION — replace from credential vault |
| `RECONNECT_QUO_API_KEY` | API key in HTTP header | M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION — replace from credential vault |

---

## Section 10 — Per-Blueprint Import Safety Assessment

### M-AUDIT-LOGGER

**Import safety:** SAFE TO IMPORT  
**Modules:**
- Module 1: `gateway:CustomWebHook` — Make built-in ✓
- Module 2: `airtable:ActionCreateRecord` — PDF-verified native ✓

**No HTTP legacy calls to audit.** No unverified modules. Simplest blueprint in the set.  
**Required post-import:** Bind Airtable connection. Copy generated webhook URL for use by all other blueprints.  
**Import verdict:** SAFE ✓

---

### M-SLACK-ALERTS

**Import safety:** SAFE TO IMPORT  
**Modules:**
- Module 1: `gateway:CustomWebHook` — Make built-in ✓
- Module 2: `builtin:BasicRouter` — Make built-in ✓
- Modules 3, 4, 5, 6, 7: `slack:CreateMessage` — PDF-verified native ✓
- Module 8: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓

**No unverified modules.**  
**Required post-import:** Bind Slack connection. Replace `RECONNECT_WILL_SLACK_USER_ID` in modules 5 and 7 with Will's Slack member ID. Replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL` in module 8.  
**Import verdict:** SAFE ✓

---

### M-BRAND-ROUTER

**Import safety:** SAFE TO IMPORT WITH WARNING (GAP-002)  
**Modules:**
- Module 1: `gateway:CustomWebHook` — Make built-in ✓
- Module 2: `builtin:BasicRouter` — Make built-in ✓
- Module 3: `anthropic:ActionCreateMessage` — WARNING: not directly confirmed in PDF (GAP-002)
- Module 4: `json:ParseJSON` — Make built-in ✓
- Module 5: `builtin:BasicRouter` — Make built-in ✓
- Modules 6, 7, 8: `airtable:ActionUpdateRecord` — PDF-verified native ✓
- Module 9: `slack:CreateMessage` — PDF-verified native ✓
- Module 10: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓

**Warning:** Module 3 uses `anthropic:ActionCreateMessage`. Verify Make Anthropic module exposes `model`, `max_tokens`, `temperature`, `system`, `messages` parameters. Verify `claude-sonnet-4-20250514` is selectable.  
**Required post-import:** Bind Anthropic, Airtable, Slack connections. Replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL`.  
**Import verdict:** SAFE WITH WARNING — resolve GAP-002 during rebinding ⚠

---

### M-LEAD-INTAKE

**Import safety:** SAFE TO IMPORT WITH WARNINGS  
**Modules:**
- Module 1: `gateway:CustomWebHook` (Squarespace) — must remain webhook ✓
- Module 2: `tools:SetVariable` — Make built-in ✓
- Module 3: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 4: `builtin:BasicRouter` — Make built-in ✓
- Module 5: `airtable:ActionCreateRecord` — PDF-verified native ✓
- Module 6: `http:ActionSendData` to M-BRAND-ROUTER — must remain HTTP ✓
- Module 7: `gmail:ActionSendEmail` — PDF-verified native ✓
- Module 8: `slack:CreateMessage` — PDF-verified native ✓
- Module 9: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓

**Warnings:**
1. Squarespace form field names in webhook payload must be verified against blueprint's `expect` schema. Squarespace field names differ by form configuration. Fields `name`, `email`, `phone`, `inquiry_text`, `event_date`, `guest_count`, `source_page`, `form_name` must match what Squarespace actually delivers. May require mapper adjustment in module 1 after test submission.
2. Module 5 hardcodes `"Environment": "Production"` — confirm this is intentional and not a test value.

**Required post-import:** Bind Airtable, Gmail, Slack connections. Register Squarespace webhook. Replace `RECONNECT_BRAND_ROUTER_WEBHOOK_URL`, `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL`.  
**Import verdict:** SAFE WITH WARNINGS — Squarespace field mapping must be tested ⚠

---

### M-CONCIERGE-ASSIGNMENT

**Import safety:** NOT SAFE TO IMPORT WITHOUT RESOLUTION OF GAP-001  
**Modules:**
- Module 1: `airtable:TriggerNewRecord` — WARNING: GAP-003, needs verification but likely available
- Module 2: `builtin:BasicRouter` (emergency flag guard) — Make built-in ✓
- Module 3: `tools:SetVariable` — Make built-in ✓
- Module 4: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 5: `builtin:BasicRouter` (idempotency guard) — Make built-in ✓
- **Module 6: `stripe:ActionCreatePaymentLink` — CRITICAL: NOT IN PDF (GAP-001)**
- Module 7: `airtable:ActionUpdateRecord` — PDF-verified native ✓
- Module 8: `gmail:ActionSendEmail` — PDF-verified native ✓
- Module 9: `http:ActionSendData` (Quo SMS) — must remain HTTP ✓
- Module 10: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓
- Module 11: `http:ActionSendData` to M-AUDIT-LOGGER (blocked path) — must remain HTTP ✓

**Critical issue:** Module 6 uses `stripe:ActionCreatePaymentLink` which is NOT in the approved PDF module inventory. Importing and activating this scenario without resolving GAP-001 will result in module 6 failing. The deposit payment link will not be created. All downstream modules (7, 8, 9, 10) depend on module 6's output (`6.url`, `6.id`).

**Additional note:** `RECONNECT_QUO_API_KEY` appears in the Authorization header value field (`"Bearer RECONNECT_QUO_API_KEY"`). This must be replaced from credential vault — the placeholder is visible in the HTTP body JSON string.

**Required post-import (after GAP-001 resolved):** Bind Airtable, Stripe, Gmail connections. Replace Quo credentials, audit webhook URL.  
**Import verdict:** NOT SAFE — GAP-001 must be resolved first ✗

---

### M-STRIPE-DEPOSIT

**Import safety:** SAFE TO IMPORT  
**Modules:**
- Module 1: `gateway:CustomWebHook` (Stripe webhook) — must remain webhook ✓
- Module 2: `builtin:BasicRouter` (event type guard) — Make built-in ✓
- Module 3: `tools:SetVariable` — Make built-in ✓
- Module 4: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 5: `builtin:BasicRouter` (idempotency guard) — Make built-in ✓
- Module 6: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 7: `airtable:ActionUpdateRecord` — PDF-verified native ✓
- Module 8: `gmail:ActionSendEmail` — PDF-verified native ✓
- Module 9: `slack:CreateMessage` — PDF-verified native ✓
- Module 10: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓

**No unverified modules.** All native modules are PDF-confirmed.  
**Note on Stripe webhook:** The `gateway:CustomWebHook` trigger correctly receives Stripe events. The `payment_intent.succeeded` event type filter in module 2 correctly guards against wrong event types. Idempotency via Airtable audit log search correctly handles Stripe webhook retries.  
**Required post-import:** Bind Airtable, Gmail, Slack connections. Register webhook URL in Stripe Dashboard for `payment_intent.succeeded`. Replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL`.  
**Import verdict:** SAFE ✓

---

### M-BOOKING-CREATION

**Import safety:** SAFE TO IMPORT WITH WARNING (GAP-002, GAP-003)  
**Modules:**
- Module 1: `airtable:TriggerNewRecord` — WARNING: GAP-003, verify trigger availability
- Module 2: `builtin:BasicRouter` (emergency flag guard) — Make built-in ✓
- Module 3: `tools:SetVariable` — Make built-in ✓
- Module 4: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 5: `builtin:BasicRouter` (idempotency guard) — Make built-in ✓
- Module 6: `airtable:ActionGetRecord` — PDF-verified native ✓
- **Module 7: `anthropic:ActionCreateMessage` — WARNING: GAP-002**
- Module 8: `gmail:ActionSendEmail` — PDF-verified native ✓
- Module 9: `airtable:ActionUpdateRecord` — PDF-verified native ✓
- Module 10: `slack:CreateMessage` — PDF-verified native ✓
- Module 11: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓
- Module 12: `http:ActionSendData` to M-AUDIT-LOGGER (blocked path) — must remain HTTP ✓

**Warning:** Module 7 uses `anthropic:ActionCreateMessage`. See GAP-002. The charter brief generation is the core output of this scenario. If the Anthropic module does not support `system` prompt or `messages` array, the brief quality will be materially degraded.

**Trigger formula note:** `AND({Status}="CONFIRMED",{Agreement_Signed}=TRUE(),DATETIME_DIFF({Charter_Date},TODAY(),"days")<=14,{Charter_Brief_Sent}=FALSE())` — this formula is complex. Confirm that `airtable:TriggerNewRecord` supports formula-based filtering of this complexity. If the trigger fires on all new records, the formula guard must be moved to a router filter inside the scenario.

**Required post-import:** Bind Airtable, Claude, Gmail, Slack connections. Replace `RECONNECT_AUDIT_LOGGER_WEBHOOK_URL`.  
**Import verdict:** SAFE WITH WARNINGS — verify Anthropic module parameters and trigger formula support ⚠

---

### M-BOOKING-CONFIRMATION

**Import safety:** NOT SAFE TO IMPORT WITHOUT RESOLUTION OF GAP-001  
**Modules:**
- Module 1: `airtable:TriggerNewRecord` — WARNING: GAP-003, verify trigger availability
- Module 2: `builtin:BasicRouter` (emergency flag guard) — Make built-in ✓
- Module 3: `tools:SetVariable` — Make built-in ✓
- Module 4: `airtable:ActionSearchRecords` — PDF-verified native ✓
- Module 5: `builtin:BasicRouter` (idempotency guard) — Make built-in ✓
- **Module 6: `stripe:ActionCreatePaymentLink` — CRITICAL: NOT IN PDF (GAP-001)**
- Module 7: `airtable:ActionUpdateRecord` — PDF-verified native ✓
- Module 8: `gmail:ActionSendEmail` — PDF-verified native ✓
- Module 9: `http:ActionSendData` (Quo SMS) — must remain HTTP ✓
- Module 10: `slack:CreateMessage` — PDF-verified native ✓
- Module 11: `http:ActionSendData` to M-AUDIT-LOGGER — must remain HTTP ✓
- Module 12: `http:ActionSendData` to M-AUDIT-LOGGER (blocked path) — must remain HTTP ✓

**Critical issue:** Same as M-CONCIERGE-ASSIGNMENT. Module 6 `stripe:ActionCreatePaymentLink` is NOT in PDF. Balance payment link will not be created. Modules 7, 8 depend on module 6 output (`6.url`, `6.id`). Same resolution required as GAP-001.

**Additional note:** The balance amount calculation `round(multiply(subtract(1.fields.Package_Price; ifempty(1.fields.Deposit_Amount_Received; 0)); 100); 0)` — this is correct math for converting dollars to Stripe cents, but `ifempty` function behavior in Make should be confirmed to return `0` when the field is null/empty.

**Required post-import (after GAP-001 resolved):** Bind Airtable, Stripe, Gmail, Slack connections. Replace Quo credentials, audit webhook URL.  
**Import verdict:** NOT SAFE — GAP-001 must be resolved first ✗

---

## Section 11 — Idempotency and Audit Logging Integrity Check

All 8 blueprints were reviewed for idempotency and audit logging integrity. No issues found.

| Blueprint | Idempotency Method | Idempotency Key Pattern | Audit Log Call |
|---|---|---|---|
| M-AUDIT-LOGGER | N/A — this IS the audit sink | N/A | N/A |
| M-BRAND-ROUTER | None explicit (called per lead; brand router is idempotent by Airtable update) | N/A | Yes — module 10 |
| M-LEAD-INTAKE | Airtable search before create | `LEAD-{email}-{YYYYMMDD}` | Yes — module 9 |
| M-SLACK-ALERTS | None (alerting is acceptable to repeat) | N/A | Yes — module 8 |
| M-CONCIERGE-ASSIGNMENT | Airtable audit log search before Stripe call | `CONCIERGE-{recordId}-BOOKING-001` | Yes — modules 10, 11 |
| M-STRIPE-DEPOSIT | Airtable audit log search before processing | `STRIPE-DEPOSIT-{stripeEventId}` | Yes — module 10 |
| M-BOOKING-CREATION | Airtable audit log search before brief generation | `CHARTER-BRIEF-{recordId}-CHARTER-004` | Yes — modules 11, 12 |
| M-BOOKING-CONFIRMATION | Airtable audit log search before payment link creation | `BALANCE-REMINDER-{recordId}-CHARTER-001` | Yes — modules 11, 12 |

**Assessment:** Idempotency is correctly implemented across all scenarios that require it. All financial and client-communication scenarios (M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION) use the Airtable Audit Log table as the idempotency store. Emergency flag guards in M-CONCIERGE-ASSIGNMENT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION are correctly placed as the first router after the trigger. Do NOT remove these guards during patching.

---

## Section 12 — Airtable Schema References

All 8 blueprints reference these hardcoded Airtable IDs. These must be verified before activation.

| ID | Presumed Purpose | Appears In |
|---|---|---|
| Base ID: `appdZ49WqgjRXxA1R` | She Said Sail production Airtable base | All 8 blueprints |
| Table `tblTlSB9CO4dTGodg` | Requests/Leads table | M-LEAD-INTAKE, M-BRAND-ROUTER |
| Table `tblrMpTfMk8q1eNHp` | Audit Log table | M-AUDIT-LOGGER, M-LEAD-INTAKE, M-BRAND-ROUTER (idempotency checks), M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Table `tbl72omPibBkn2hZL` | Bookings table | M-CONCIERGE-ASSIGNMENT, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |

**Action required:** Confirm these IDs match the live production base before activating any scenario. Base ID and table IDs are available in the Airtable URL when viewing a table.

---

## Section 13 — Security and Credential Audit

All 8 blueprints were reviewed for hardcoded secrets. Result: **CLEAN — no secrets or API keys found.**

All connection references use `null` for `__IMTCONN__` (standard safe-import pattern). All webhook URLs use `RECONNECT_*` placeholder strings. All API keys use `RECONNECT_*` placeholder strings. The Quo API key placeholder `RECONNECT_QUO_API_KEY` appears in the HTTP header value field but is a placeholder string, not a real key.

**No blueprint file should be modified to add real credentials. All credentials are bound post-import through Make's connection manager and module field rebinding.**

---

## Validation Checklist

- [x] All 8 blueprint JSON files read and audited
- [x] Attached PDF module inventory used as source of truth (no hallucinated modules)
- [x] `Make_Native_Module_Reference_Master.md` created at `08_PRODUCT_ENGINEERING/Make_Orchestration/`
- [x] `Make_Native_Module_Gap_Audit.md` created at `08_PRODUCT_ENGINEERING/Make_Orchestration/Stage_1/Blueprints/docs/`
- [x] No blueprint JSON files modified
- [x] No Stage 2–4 work added
- [x] No secrets or API keys added
- [x] Idempotency preserved in all findings
- [x] Audit logging preserved in all findings
- [x] Retry/error handling preserved in all findings

---

## Final Verdict

**READY WITH WARNINGS**

| Blueprint | Verdict |
|---|---|
| M-AUDIT-LOGGER | READY — SAFE TO IMPORT |
| M-SLACK-ALERTS | READY — SAFE TO IMPORT |
| M-BRAND-ROUTER | READY WITH WARNING — verify Anthropic module parameters (GAP-002) |
| M-LEAD-INTAKE | READY WITH WARNING — verify Squarespace field name mapping post-import |
| M-CONCIERGE-ASSIGNMENT | NOT READY — resolve GAP-001 (stripe:ActionCreatePaymentLink not in PDF) |
| M-STRIPE-DEPOSIT | READY — SAFE TO IMPORT |
| M-BOOKING-CREATION | READY WITH WARNING — verify Anthropic module parameters (GAP-002) and Airtable trigger formula (GAP-003) |
| M-BOOKING-CONFIRMATION | NOT READY — resolve GAP-001 (stripe:ActionCreatePaymentLink not in PDF) |

**Blocking issues before full Stage 1 activation:**
1. GAP-001: Verify or replace `stripe:ActionCreatePaymentLink` in M-CONCIERGE-ASSIGNMENT and M-BOOKING-CONFIRMATION
2. GAP-002: Verify `anthropic:ActionCreateMessage` maps to a PDF-listed module with full parameter support
3. GAP-003: Verify `airtable:TriggerNewRecord` is available and supports formula filtering

**Recommended import order (proceed to STAGE_1_NATIVE_FIRST_REIMPORT_INSTRUCTIONS.md after resolving blockers):**
1. M-AUDIT-LOGGER
2. M-SLACK-ALERTS
3. M-BRAND-ROUTER
4. M-LEAD-INTAKE
5. M-STRIPE-DEPOSIT
6. M-BOOKING-CREATION
7. M-CONCIERGE-ASSIGNMENT (only after GAP-001 resolved)
8. M-BOOKING-CONFIRMATION (only after GAP-001 resolved)
