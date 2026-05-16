# M-BRAND-ROUTER Manual Setup Guide

**For:** Will / She Said Sail + Mare Executive
**Scenario:** M01 M-BRAND-ROUTER
**File to import:** `M-BRAND-ROUTER.blueprint.json`

This guide uses plain language. No Make expertise needed. Follow each step in order.

---

## Before You Start

You will need:
- Access to your Make account (make.com)
- Your Airtable personal access token
- Your Anthropic (Claude) API key
- Admin access to the `ops-alerts` Slack channel
- The SSS and ME system prompt texts (stored separately)

---

## Step 1 — Import the Blueprint

1. Log in to make.com
2. Go to **Scenarios** in the left sidebar
3. Click the three-dot menu (top right of Scenarios page) → **Import Blueprint**
4. Upload the file: `M-BRAND-ROUTER.blueprint.json`
5. Make will display a preview of the scenario — click **Save**
6. The scenario will appear in your Scenarios list — do NOT activate it yet

**Screenshot to take:** The scenario canvas showing all 9 modules connected.

---

## Step 2 — Reconnect Slack

Do this for **Slack module 3**, **Slack module 6**, and **Slack module 9**. All three use the same connection.

1. Click **Slack module 3** (the first Slack module — fallback alert)
2. Under **Connection**, click **Add connection** (or **Reconnect** if a broken one exists)
3. A Slack login window will open — sign in to your Slack workspace
4. Authorise Make to post to your workspace
5. After authorisation, select your workspace from the dropdown
6. Verify the **Channel** field shows `ops-alerts`
7. Verify the **Text** field shows: `[M01] BRAND UNDETECTED — defaulted to SSS | Record: {{1.id}} | Source: {{1.Lead_Source}} | LUCIANA REVIEW REQUIRED`
8. Click **OK** to save the module
9. Repeat for **Slack module 6** and **Slack module 9** — select the same Slack connection you just created

**Screenshot to take:** Each Slack module showing the connection name, channel = `ops-alerts`, and the correct text.

---

## Step 3 — Reconnect Airtable (HTTP PATCH modules)

Do this for **HTTP module 4** (SSS PATCH) and **HTTP module 7** (ME PATCH).

1. Click **HTTP module 4**
2. Check the **URL** field — it must read exactly:
   `https://api.airtable.com/v0/appdZ49WqgjRXxA1R/Requests/{{1.recordId}}`
3. Under **Headers**, find the `Authorization` header
4. Replace `RECONNECT_AIRTABLE_CONNECTION` with your Airtable personal access token:
   `Bearer pat_YOURTOKENHERE`
   (Keep the word `Bearer` followed by a space before your token)
5. Verify `Content-Type` header = `application/json`
6. Verify **Method** = `PATCH`
7. Verify **Body type** = `Raw`
8. Verify **Content type** = `JSON (application/json)`
9. Verify **Request content** =
   - Module 4: `{"fields":{"Brand":"She Said Sail"}}`
   - Module 7: `{"fields":{"Brand":"Mare Executive"}}`
10. Verify **Parse response** = Yes
11. Click **OK** to save
12. Repeat for **HTTP module 7**

**Screenshot to take:** Module 4 and Module 7 open, showing the URL, Authorization header (with token), and request body.

---

## Step 4 — Reconnect Claude API (HTTP POST modules)

Do this for **HTTP module 5** (SSS Claude call) and **HTTP module 8** (ME Claude call).

1. Click **HTTP module 5**
2. Verify **URL** = `https://api.anthropic.com/v1/messages`
3. Verify **Method** = `POST`
4. Under **Headers**, check three headers exist:
   - `x-api-key` → replace `RECONNECT_ANTHROPIC_API_KEY` with your actual Anthropic API key
   - `anthropic-version` → must be exactly `2023-06-01`
   - `Content-Type` → must be `application/json`
5. Verify **Body type** = `Raw` and **Content type** = `JSON (application/json)`
6. Open the **Request content** field and verify the JSON body looks like:
   ```json
   {
     "model": "claude-sonnet-4-20250514",
     "max_tokens": 600,
     "temperature": 0.4,
     "system": "RECONNECT_SSS_SYSTEM_PROMPT",
     "messages": [
       {
         "role": "user",
         "content": "Brand routing confirmed: She Said Sail (default). RecordId: {{1.recordId}} | Lead_Source: {{1.Lead_Source}} | Website_Source: {{1.Website_Source}} | Landing_Page: {{1.Landing_Page}}"
       }
     ]
   }
   ```
7. Replace `RECONNECT_SSS_SYSTEM_PROMPT` with the full SSS system prompt text (paste it directly, inside the quotes)
8. Verify **Parse response** = Yes
9. Verify **Evaluate all states as errors** = Yes
10. Click **OK** to save
11. Repeat for **HTTP module 8** — use `RECONNECT_ME_SYSTEM_PROMPT` → paste ME system prompt

**Screenshot to take:** Module 5 and Module 8 open, showing the URL, all three headers, and the JSON body with model = `claude-sonnet-4-20250514`.

---

## Step 5 — Paste the Webhook URL Into Your Trigger Source

1. Click **Webhook module 1** (the first module)
2. Click **Copy address to clipboard** — this gives you the webhook URL
3. Go to wherever this webhook is triggered from (e.g. Airtable automation, Zapier, another Make scenario, a form)
4. Paste the new webhook URL into that trigger
5. Save the trigger source

**Note:** Make generates a new unique URL each time you import a blueprint. You must update your trigger source every time.

**Screenshot to take:** Webhook module open showing the URL, and your trigger source showing the URL pasted in.

---

## Step 6 — Test the Scenario Safely

**Do not activate the scenario yet.**

1. In the scenario canvas, click **Run once** (bottom left)
2. In a separate tab, trigger the webhook manually:
   - Option A: Use Make's built-in webhook test button in Webhook module 1
   - Option B: Send a test POST to the webhook URL using a tool like Postman or curl with a sample record payload
3. Watch the scenario execute — each module will show a green checkmark or red error icon
4. After the run completes, click each module to inspect its input/output

**Safe test payload (use a test record, not a live lead):**
```json
{
  "recordId": "recTEST123456",
  "id": "recTEST123456",
  "Brand": "She Said Sail",
  "Lead_Source": "Test Source",
  "Website_Source": "test.com",
  "Landing_Page": "/test"
}
```

---

## Step 7 — Verify Brand Routing Worked

1. Go to Airtable → base `appdZ49WqgjRXxA1R` → table `Requests`
2. Find the test record you used
3. Check the **Brand** field — it should now show `She Said Sail` or `Mare Executive` depending on your test payload
4. If the Brand field is blank or unchanged, the Airtable PATCH failed — check Step 3

**Screenshot to take:** The Airtable record with the Brand field populated.

---

## Step 8 — Verify Slack Alerts Fired

1. Open Slack and go to the `#ops-alerts` channel
2. You should see one of these messages depending on your test:
   - **SSS route:** `[M01] Brand routed: She Said Sail | Record: recTEST123456 | Source: Test Source | Prompt: SSS_SYSTEM`
   - **ME route:** `[M01] Brand routed: Mare Executive | Record: recTEST123456 | Source: Test Source | Prompt: ME_SYSTEM`
   - **Fallback:** `[M01] BRAND UNDETECTED — defaulted to SSS | Record: recTEST123456 | Source: Test Source | LUCIANA REVIEW REQUIRED`
3. If no message appeared, check the Slack module in Make — look for a red error and read the error message

**Screenshot to take:** The Slack `#ops-alerts` channel showing the test message.

---

## Step 9 — Verify Airtable PATCH Worked

1. Back in Make, click on **HTTP module 4** (or 7) after the test run
2. Click the **Output** tab
3. You should see a JSON response containing `"id": "recTEST123456"` and the updated `fields.Brand`
4. HTTP status should be `200`
5. If status is `401` → your Airtable token is wrong (redo Step 3)
6. If status is `404` → the record ID or base ID is wrong

**Screenshot to take:** Module 4 or 7 output tab showing status 200 and the Brand field value.

---

## Step 10 — Verify Claude API Call Succeeded

1. Click **HTTP module 5** (or 8) after the test run
2. Click the **Output** tab
3. You should see a JSON response like:
   ```json
   {
     "id": "msg_...",
     "type": "message",
     "role": "assistant",
     "content": [{ "type": "text", "text": "..." }],
     "model": "claude-sonnet-4-20250514",
     "stop_reason": "end_turn"
   }
   ```
4. HTTP status should be `200`
5. If status is `401` → your Anthropic API key is wrong (redo Step 4)
6. If status is `400` → the JSON body is malformed — check the request content field for typos

**Screenshot to take:** Module 5 or 8 output tab showing status 200 and the Claude response body.

---

## Common Make Errors and What They Mean

| Error | What It Means | How to Fix |
|---|---|---|
| `401 Unauthorized` on Airtable PATCH | Your Airtable token is invalid or expired | Go to airtable.com → Account → API → generate a new personal access token and paste it in the Authorization header |
| `401 Unauthorized` on Claude API | Your Anthropic API key is wrong or expired | Go to console.anthropic.com → API Keys → create a new key |
| `400 Bad Request` on Claude API | The JSON body has a formatting error | Open HTTP module 5 or 8 and carefully check the request content — common issues: missing quotes, trailing commas, wrong model name |
| `404 Not Found` on Airtable | The record ID or base ID is wrong | Verify the URL uses `appdZ49WqgjRXxA1R` and that `{{1.recordId}}` is mapped from the webhook trigger |
| `channel_not_found` on Slack | Make cannot find the `ops-alerts` channel | Ensure the Slack connection has access to that channel; try typing `ops-alerts` manually if the dropdown doesn't show it |
| Webhook module shows no data | Nothing has triggered the webhook yet | Use the **Run once** button and send a test payload, or check that your trigger source has the correct webhook URL |
| Scenario runs but router skips all routes | Filter conditions are not matching | Check that your test payload includes a `Brand` field; the router evaluates `{{1.Brand}}` |
| Module shows orange warning icon | Module ran but returned an unexpected response | Click the module and read the output — usually means a 4xx or 5xx HTTP status |

---

## Activating the Scenario

Only activate after:
- All modules show green on a test run
- Brand field updated in Airtable
- Slack alert appeared in `#ops-alerts`
- Claude API returned a valid response

To activate:
1. Toggle the **ON/OFF switch** in the top left of the scenario canvas to **ON**
2. The scenario will now run automatically whenever the webhook is triggered

---

## If You Get Stuck

Take screenshots of:
1. The full scenario canvas
2. Each module that has a red or orange icon — both the Settings tab and the Output/Error tab
3. The Slack `#ops-alerts` channel (showing whether the message arrived or not)
4. The Airtable record (showing the Brand field value after the test)
5. The Make scenario history (Scenarios → History) showing the run log

Send these screenshots along with the error message text for fastest diagnosis.
