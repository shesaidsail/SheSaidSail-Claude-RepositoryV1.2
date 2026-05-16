# M-BRAND-ROUTER Manual Fix Guide

**For:** Will (Founder)
**Scenario:** M-BRAND-ROUTER in Make
**Purpose:** Fix the broken imported scenario OR re-import the patched blueprint
**Date:** May 2026

---

## READ THIS FIRST

You have two options:

| Option | When to use | Effort |
|--------|-------------|--------|
| **A — Re-import the patched blueprint** (recommended) | The current broken scenario is a mess — faster to start clean | ~20 min |
| **B — Manually repair the existing scenario** | You've already done partial rebinding you don't want to lose | ~35 min |

The patched blueprint file is: `02_SYSTEMS_AUTOMATIONS/Make/M-BRAND-ROUTER.blueprint.json`

---

## OPTION A — RE-IMPORT THE PATCHED BLUEPRINT

### Step 1 — Delete or archive the broken scenario

1. Open Make → Your scenario list
2. Find `M-BRAND-ROUTER` (the broken one)
3. Click the three-dot menu → **Rename** it to `M-BRAND-ROUTER-BROKEN-DELETE`
4. Do not delete it yet — wait until the new import is confirmed working

### Step 2 — Import the patched blueprint

1. In Make, click **Create a new scenario**
2. Click the three-dot menu (top right of the canvas) → **Import Blueprint**
3. Upload the file: `M-BRAND-ROUTER.blueprint.json`
4. Make should import with **zero "Module Not Found" errors** — the broken module types have been removed and replaced

If you still see "Module Not Found" on any module after import, go to Option B Step 3 for that specific module.

### Step 3 — Reconnect the webhook

1. Click on **Module 1 (webhook)** — it will show `RECONNECT_WEBHOOK_ID`
2. Click the webhook field → **Add** → create a new webhook named: `M-BRAND-ROUTER Inbound`
3. Copy the webhook URL — save it somewhere; you will need it to trigger test runs
4. Click **OK**

### Step 4 — Reconnect Airtable (HTTP modules 4 and 7)

The Airtable PATCH uses HTTP modules, not the native Airtable connector, so there is no "connection" to bind — just a Bearer token in the Authorization header.

For **Module 4** (ME route — PATCH) and **Module 7** (SSS route — PATCH):

1. Click the module → find the **Authorization** header field
2. Replace `RECONNECT_AIRTABLE_CONNECTION` with your Airtable Personal Access Token:
   `Bearer pat_XXXXXXXXXXXX`
3. Confirm the URL reads exactly:
   `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}`
4. Confirm the body reads:
   - Module 4 (ME): `{"fields":{"Brand":"Mare Executive"}}`
   - Module 7 (SSS): `{"fields":{"Brand":"She Said Sail"}}`

> Do NOT use the Airtable-branded Make connector for these modules — it adds extra complexity and the HTTP approach is more portable and simpler to debug.

### Step 5 — Reconnect Anthropic (HTTP modules 5 and 8)

For **Module 5** (ME route — Claude) and **Module 8** (SSS route — Claude):

1. Click the module → find the **x-api-key** header field
2. Replace `RECONNECT_ANTHROPIC_KEY` with your Anthropic API key:
   `sk-ant-XXXXXXXXXXXX`
3. In the **data** (body) field, find `RECONNECT_ME_SYSTEM_PROMPT` or `RECONNECT_SSS_SYSTEM_PROMPT`
4. Replace with the appropriate system prompt from your AI_Prompt_Versions table
   - If prompts are not yet ready: temporarily use `"You are a brand routing assistant for Mare Executive."` and `"You are a brand routing assistant for She Said Sail."` as placeholders — these are safe for testing and do not affect the Airtable write
5. Confirm the URL is: `https://api.anthropic.com/v1/messages`
6. Confirm headers include `anthropic-version: 2023-06-01`

### Step 6 — Reconnect Slack (modules 3, 6, 9)

For **Module 3** (Idempotency Slack), **Module 6** (ME Slack), and **Module 9** (SSS Slack):

1. Click the module → click the **Connection** field
2. Select your existing Slack workspace connection OR click **Add** to authenticate a new one
3. In the **Channel** field:
   - Remove `RECONNECT_OPS_ALERTS_CHANNEL_ID`
   - Click the dropdown and search for `ops-alerts`
   - Select `#ops-alerts`
4. The message text is pre-filled — do not change it

---

## OPTION B — MANUALLY REPAIR THE EXISTING SCENARIO

Use this only if you have partially rebound the broken scenario and want to keep that work.

### Step 1 — Identify which modules are broken

In the existing scenario, look for any module showing **"Module Not Found"** or a red error badge. You should see:

| Expected position | Broken module type | Fix |
|------------------|-------------------|-----|
| Set Variable (appeared 2×) | `builtin:SetVariable` | Delete these entirely — they are not needed |
| Slack notification (appeared 1×) | `slack:ActionPostMessage` | Delete and replace with new Slack module |

### Step 2 — Delete the broken Set Variable modules

1. Click each `SetVariable` module showing "Module Not Found"
2. Check what they were storing — typically `Brand = "She Said Sail"` or `Brand = "Mare Executive"`
3. **These are no longer needed** — the patched blueprint hardcodes the Brand value directly in the Airtable PATCH body
4. Right-click the module → **Delete module** → confirm
5. Reconnect the flow: drag the output arrow from the module before the deleted one to the module after it

### Step 3 — Delete and replace the broken Slack module

1. Click the broken `slack:ActionPostMessage` module
2. Note the channel it was sending to (should be `#ops-alerts`) and copy the message text
3. Right-click → **Delete module**
4. Click the **+** button where it was → search for **Slack** → select **Create a Message**
5. Configure:
   - **Connection:** Select your Slack workspace
   - **Channel:** `#ops-alerts`
   - **Text:** `[M01] Brand routed: {{Brand_value}} | Record: {{1.recordId}} | Channel: {{1.Lead_Source}}`
     - Replace `{{Brand_value}}` with the literal string in your route: `Mare Executive` or `She Said Sail`
6. Reconnect this module to the flow

### Step 4 — Validate the router logic

Confirm the router has exactly 3 routes in this order:

**Route 0 — Idempotency (must be first)**
- Filter: `{{1.Brand}}` is NOT equal to `` (empty string)
- Action: Slack notification only — do not write to Airtable

**Route 1 — Mare Executive**
- Filter (OR logic — any one of these triggers ME):
  - `{{1.Lead_Source}}` contains `Mare Executive`
  - `{{1.Website_Source}}` equals `Website (Mare Executive)`
  - `{{1.Landing_Page}}` contains `mare`
  - `{{1.Notes}}` contains `Brand: ME`
- Action: Airtable PATCH `{"fields":{"Brand":"Mare Executive"}}` → Claude HTTP → Slack

**Route 2 — She Said Sail (fallback — no filter)**
- No filter set — this catches everything that did not match Routes 0 or 1
- Action: Airtable PATCH `{"fields":{"Brand":"She Said Sail"}}` → Claude HTTP → Slack

### Step 5 — Validate Airtable PATCH settings

For BOTH the ME and SSS Airtable HTTP modules:

| Field | Required value |
|-------|---------------|
| Method | PATCH |
| URL | `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}` |
| Header: Authorization | `Bearer YOUR_AIRTABLE_PAT` |
| Header: Content-Type | `application/json` |
| Body (ME route) | `{"fields":{"Brand":"Mare Executive"}}` |
| Body (SSS route) | `{"fields":{"Brand":"She Said Sail"}}` |

### Step 6 — Validate Claude HTTP settings

For BOTH the ME and SSS Claude HTTP modules:

| Field | Required value |
|-------|---------------|
| Method | POST |
| URL | `https://api.anthropic.com/v1/messages` |
| Header: x-api-key | Your Anthropic API key |
| Header: anthropic-version | `2023-06-01` |
| Header: Content-Type | `application/json` |
| Body — model | `claude-sonnet-4-6` |
| Body — system | Your ME or SSS system prompt (or placeholder for now) |

---

## TESTING BEFORE YOU GO LIVE

### Test 1 — ME route

1. In the scenario, click **Run once**
2. Open a browser and POST to the webhook URL with this test body:
   ```json
   {
     "recordId": "recTEST0000001",
     "Lead_Source": "Mare Executive Website",
     "Website_Source": "",
     "Landing_Page": "",
     "Notes": "",
     "Brand": ""
   }
   ```
3. Expected result:
   - Router takes Route 1 (ME)
   - Airtable PATCH fires (check execution log — it will fail with 404 on `recTEST0000001` which is fine)
   - Claude HTTP fires
   - Slack message appears in `#ops-alerts`: `[M01] Brand routed: Mare Executive | Record: recTEST0000001 | Channel: Mare Executive Website`

### Test 2 — SSS default route

```json
{
  "recordId": "recTEST0000002",
  "Lead_Source": "Instagram",
  "Website_Source": "Website (She Said Sail)",
  "Landing_Page": "",
  "Notes": "",
  "Brand": ""
}
```

Expected: Router takes Route 2 (SSS default)

### Test 3 — Idempotency route

```json
{
  "recordId": "recTEST0000003",
  "Lead_Source": "Instagram",
  "Website_Source": "",
  "Landing_Page": "",
  "Notes": "",
  "Brand": "She Said Sail"
}
```

Expected: Router takes Route 0 (Idempotency) — only Slack fires, no Airtable write

### Test 4 — Real Airtable record (final validation)

1. Pick a real Request record from your Airtable Requests table with Brand field empty
2. Use its actual Airtable record ID
3. Run the scenario — confirm Airtable record gets Brand value written correctly
4. Take a screenshot of the Airtable record showing the Brand field filled in

---

## SCREENSHOTS TO TAKE

Take these screenshots and save them before calling this done:

1. **Scenario overview** — full canvas showing all 3 routes and 9 modules
2. **Router filter — Route 1 (ME)** — the 4-condition OR filter
3. **Airtable PATCH body (ME)** — showing `"Brand":"Mare Executive"` hardcoded
4. **Airtable PATCH body (SSS)** — showing `"Brand":"She Said Sail"` hardcoded
5. **Slack module connected** — showing workspace name and `#ops-alerts` selected
6. **Successful test run** — execution log showing all modules green

If you get stuck at any point, screenshot the error you see and share it.

---

## WHAT NOT TO DO

- Do NOT use the native Airtable Make connector for the PATCH — use HTTP only
- Do NOT add Set Variable modules back — hardcoded Brand values in the PATCH body are the correct approach
- Do NOT use `slack:ActionPostMessage` — use **Create a Message** from the Slack app instead
- Do NOT go live without running all three test cases above
- Do NOT connect this to production Airtable records during testing — use `recTEST` IDs until all modules show green

---

*M_BRAND_ROUTER_MANUAL_FIX_GUIDE.md — She Said Sail + Mare Executive*
*Stage 1 Make Build — Confidential Internal Use Only*
