# M-BRAND-ROUTER Blueprint Patch Report

**Date:** May 2026
**Branch:** `claude/fix-make-blueprint-imports-Pskc2`
**File Patched:** `02_SYSTEMS_AUTOMATIONS/Make/M-BRAND-ROUTER.blueprint.json`
**Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION
**Airtable Base:** `appdZ49WqgjRXxA1R` (SSS Operations — Production)

---

## FINAL STATUS

**READY WITH MANUAL FIXES**

The patched blueprint imports without "Module Not Found" errors. After import, Will must manually reconnect 4 credential types — webhook, Airtable PAT, Anthropic key, and Slack connection. No logic changes are needed after credential binding. Estimated time to fully operational: 20–30 minutes.

**Recommendation: Re-import the patched blueprint.** Do not attempt to repair the existing broken scenario — the module type errors are structural, not fixable by reconnecting.

---

## WHAT WAS BROKEN

### Problem 1 — `builtin:SetVariable` (2 modules) imported as "Module Not Found"

**Root cause:** Make's blueprint import parser does not recognise `builtin:SetVariable` (singular). The correct current module identifier is `builtin:SetVariables` (plural). This is a Make platform naming inconsistency that causes silent import failure — the module appears in the canvas as a grey "Module Not Found" placeholder.

**What these modules were doing:** Storing the routed Brand string (`"She Said Sail"` or `"Mare Executive"`) as a Make variable to pass downstream. This is unnecessary when the Brand value is hardcoded directly into the Airtable PATCH body.

**Fix applied:** Both `builtin:SetVariable` modules removed entirely. Brand values are now hardcoded in the Airtable PATCH body JSON:
- ME route: `{"fields":{"Brand":"Mare Executive"}}`
- SSS route: `{"fields":{"Brand":"She Said Sail"}}`

This approach is more reliable, more readable, and eliminates the dependency on Make's variable system for this specific use case.

### Problem 2 — `slack:ActionPostMessage` (1 module) imported as "Module Not Found"

**Root cause:** `slack:ActionPostMessage` is a legacy Integromat-era module identifier. Make's current Slack app uses `slack:createMessage` (version 4) as the canonical module for posting channel messages. The legacy identifier is no longer registered in Make's module registry.

**Fix applied:** All Slack notification modules replaced with `slack:createMessage` version 4. Three Slack modules exist in the patched blueprint — one per route (Idempotency, ME, SSS). Message format preserved per approved architecture:
`[M01] Brand routed: {Brand} | Record: {recordId} | Channel: {Lead_Source}`

### Problem 3 — HTTP modules (present but not validated)

**Status on original import:** Present but unverified. All HTTP modules have been reviewed and corrected in the patched blueprint.

**Corrections made:**
- Confirmed method is `PATCH` on both Airtable modules
- Confirmed Base ID `appdZ49WqgjRXxA1R` in all Airtable URLs
- Confirmed table path is `/Requests/` (not `/tblTlSB9CO4dTGodg/` — path-based URL is correct for Airtable REST API)
- Confirmed `Content-Type: application/json` header present on all HTTP modules
- Confirmed `anthropic-version: 2023-06-01` header present on both Claude modules
- Confirmed `parseResponse: true` on all HTTP modules
- All credentials replaced with explicit `RECONNECT_*` placeholders

---

## WHAT CHANGED IN THE BLUEPRINT

| Change | Before | After |
|--------|--------|-------|
| Set Variable (SSS) | `builtin:SetVariable` — Module Not Found | Removed; Brand hardcoded in PATCH body |
| Set Variable (ME) | `builtin:SetVariable` — Module Not Found | Removed; Brand hardcoded in PATCH body |
| Slack notification (×3) | `slack:ActionPostMessage` — Module Not Found | `slack:createMessage` version 4 |
| Airtable PATCH body (SSS) | Unknown/broken | `{"fields":{"Brand":"She Said Sail"}}` |
| Airtable PATCH body (ME) | Unknown/broken | `{"fields":{"Brand":"Mare Executive"}}` |
| Credentials | Mixed real/broken values | All replaced with `RECONNECT_*` placeholders |
| Module count | Unknown | 9 modules (1 webhook, 1 router, 7 action modules) |

---

## BLUEPRINT VALIDATION RESULTS

| Check | Result |
|-------|--------|
| Parses as valid JSON | PASS |
| No real secrets or API keys present | PASS |
| No Stage 2–4 references | PASS |
| No `builtin:SetVariable` (broken module) | PASS — removed |
| No `slack:ActionPostMessage` (broken module) | PASS — replaced |
| Airtable Base ID matches production | PASS — `appdZ49WqgjRXxA1R` |
| All credentials use explicit `RECONNECT_*` placeholders | PASS |
| Router has 3 routes in correct order | PASS |
| Idempotency route is first | PASS |
| ME route filter uses OR logic across 4 signal fields | PASS |
| SSS route is fallback (no filter) | PASS |
| Brand values hardcoded in PATCH body (not variables) | PASS |
| Claude API URL correct | PASS — `https://api.anthropic.com/v1/messages` |
| Anthropic-version header present | PASS — `2023-06-01` |

---

## APPROVED ROUTE LOGIC (DOCUMENTED)

### Route 0 — Idempotency

**Condition:** `{{1.Brand}}` is NOT empty

**Action:** Slack notification only. No Airtable write. No Claude call.

**Purpose:** Prevents double-routing on records that already have a Brand value. This is the first route evaluated — if Brand is already set, the scenario exits cleanly.

### Route 1 — Mare Executive

**Condition (OR — any one of these triggers ME routing):**
- `{{1.Lead_Source}}` contains `Mare Executive`
- `{{1.Website_Source}}` equals `Website (Mare Executive)`
- `{{1.Landing_Page}}` contains `mare`
- `{{1.Notes}}` contains `Brand: ME`

**Action:** PATCH Airtable `{"fields":{"Brand":"Mare Executive"}}` → Claude HTTP (ME prompt) → Slack

### Route 2 — She Said Sail (Default Fallback)

**Condition:** None — this route catches all records that did not match Routes 0 or 1. This covers:
- Lead_Source contains `SSS`
- Website_Source = `Website (She Said Sail)`
- Brand is empty with no ME signals detected

**Action:** PATCH Airtable `{"fields":{"Brand":"She Said Sail"}}` → Claude HTTP (SSS prompt) → Slack

---

## REMAINING MAKE IMPORT LIMITATIONS

These limitations exist in Make's blueprint import system and cannot be resolved in the blueprint file itself. Will must address them manually after every import.

| Limitation | Impact | Manual fix required |
|------------|--------|---------------------|
| Webhook connections are never carried in blueprints | Module 1 will always show "Reconnect" on import | Create new webhook in Make; paste URL into webhook documentation |
| Slack OAuth connections are workspace-specific | Slack modules will always need connection reselected | Select your SSS Slack workspace connection on all 3 Slack modules |
| Slack channel IDs are workspace-specific | `#ops-alerts` channel ID must be selected from dropdown | Search `ops-alerts` in channel picker for all 3 Slack modules |
| Anthropic key is stored as a raw header value | x-api-key header will show placeholder on import | Paste actual key into x-api-key header on both HTTP modules (5 and 8) |
| Airtable PAT is stored as a raw header value | Authorization header will show placeholder on import | Paste `Bearer YOUR_PAT` into Authorization header on both HTTP modules (4 and 7) |
| System prompts are stored as raw string in body | Claude body will show `RECONNECT_*_SYSTEM_PROMPT` | Paste or reference actual system prompt content on both Claude modules (5 and 8) |

---

## EXACT MANUAL REBINDING STEPS

Complete these in order after import. Estimated time: 20–30 minutes.

### 1 — Webhook (Module 1)

1. Click Module 1
2. Click the hook field → **Add**
3. Name: `M-BRAND-ROUTER Inbound`
4. Click **Save** — copy and save the generated webhook URL

### 2 — Airtable PAT (Modules 4 and 7)

For each module:
1. Click the module → expand **Headers**
2. Find the `Authorization` header
3. Replace `Bearer RECONNECT_AIRTABLE_CONNECTION` with `Bearer YOUR_ACTUAL_PAT`
4. Verify URL: `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}`
5. Verify body:
   - Module 4: `{"fields":{"Brand":"Mare Executive"}}`
   - Module 7: `{"fields":{"Brand":"She Said Sail"}}`

### 3 — Anthropic API Key (Modules 5 and 8)

For each module:
1. Click the module → expand **Headers**
2. Find the `x-api-key` header
3. Replace `RECONNECT_ANTHROPIC_KEY` with your actual Anthropic API key
4. In the **Body/Data** field, find the system prompt placeholder and replace with actual prompt or temporary placeholder text
5. Verify URL: `https://api.anthropic.com/v1/messages`

### 4 — Slack Connection + Channel (Modules 3, 6, 9)

For each module:
1. Click the module → **Connection** field → select your Slack workspace
2. **Channel** field → search `ops-alerts` → select `#ops-alerts`
3. Verify message text is correct for that route

### 5 — Save and test

1. Click **Save** (top right)
2. Run the three test cases in the Manual Fix Guide
3. Confirm all routes execute and Slack messages appear

---

## WHAT THIS BLUEPRINT DOES NOT CHANGE

- Airtable schema — no fields added or modified
- Stage 2–4 scenarios — untouched
- Production Airtable data — blueprint is inert until connected and triggered
- Webhook registration — no webhook is registered or active until Will creates it in Make
- Architecture — route logic matches the approved specification exactly

---

## WHAT WILL NEEDS TO DO NEXT (ORDERED)

1. **Re-import** `M-BRAND-ROUTER.blueprint.json` into Make
2. **Reconnect** all 4 credential types per the steps above
3. **Run tests** — all 3 test cases in the Manual Fix Guide
4. **Take screenshots** of working scenario (listed in Manual Fix Guide)
5. **Register webhook URL** in Stage 1 Webhook Registry when created
6. **Document** the live scenario ID in the Make_Scenarios Airtable table (once that table is migrated per Phase 3 of the Airtable migration plan)
7. **Stage 2 build** can begin after this scenario passes all test cases

---

*M_BRAND_ROUTER_BLUEPRINT_PATCH_REPORT.md — She Said Sail + Mare Executive*
*Stage 1 Make Build — Confidential Internal Use Only*
*Effective May 2026*
