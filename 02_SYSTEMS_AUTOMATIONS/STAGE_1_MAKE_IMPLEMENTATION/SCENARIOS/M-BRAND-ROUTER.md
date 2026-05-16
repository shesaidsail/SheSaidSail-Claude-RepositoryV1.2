# M-BRAND-ROUTER — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Lead Intake  
**Execution Order:** Module 4 within M-LEAD-INTAKE (invoked inline, not as separate webhook)

---

## 1. Scenario Name

`M-BRAND-ROUTER`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references.

---

## 3. Trigger Type

**Pattern:** Sub-scenario logic block, invoked inline within M-LEAD-INTAKE via a Router module sequence. M-BRAND-ROUTER is not a standalone webhook-triggered scenario. It is implemented as a dedicated Router + Text Parser module group within the M-LEAD-INTAKE flow, between the duplicate-check module and the Airtable record creation module.

**Invocation point:** After timestamp validation and before duplicate check in M-LEAD-INTAKE.

**Input received from M-LEAD-INTAKE:**
```json
{
  "source": "{{1.source}}",
  "brand_hint": "{{1.brand_hint}}",
  "message": "{{1.message}}",
  "occasion": "{{1.occasion}}",
  "package_interest": "{{1.package_interest}}",
  "submitted_at": "{{1.submitted_at}}"
}
```

**Output written to Make variables (consumed by downstream modules in M-LEAD-INTAKE):**

| Variable Name          | Type   | Example Value          |
|------------------------|--------|------------------------|
| `brand_classification` | String | `SSS`, `ME`, `AMBIGUOUS` |
| `brand_confidence`     | String | `HIGH`, `LOW`          |
| `brand_signal_source`  | String | `hint`, `keyword`, `occasion`, `default` |
| `requires_human_review`| Boolean| `true`, `false`        |

---

## 4. Exact Module Sequence

### Module 4.1 — [Router] Evaluate brand_hint Field

**Make Module Type:** Router (built-in)  
**Position:** Module 4 in M-LEAD-INTAKE sequence  
**Purpose:** First classification pass. If `brand_hint` is explicit and valid, classify immediately. If missing or ambiguous, fall through to keyword scan.

**Routes:**

| Route | Condition | Filter Expression |
|-------|-----------|-------------------|
| Route A: Hint = SSS | `brand_hint` equals `SSS` | `{{1.brand_hint}} = "SSS"` |
| Route B: Hint = ME | `brand_hint` equals `ME` | `{{1.brand_hint}} = "ME"` |
| Route C: No valid hint | All other values including empty, null, `UNKNOWN` | Fallback (no filter) |

---

### Module 4.2A — [Set Variable] brand_classification = SSS (Hint Path)

**Make Module Type:** Set Variable  
**Executes on:** Route A only  

| Variable | Value |
|----------|-------|
| `brand_classification` | `SSS` |
| `brand_confidence` | `HIGH` |
| `brand_signal_source` | `hint` |
| `requires_human_review` | `false` |

---

### Module 4.2B — [Set Variable] brand_classification = ME (Hint Path)

**Make Module Type:** Set Variable  
**Executes on:** Route B only  

| Variable | Value |
|----------|-------|
| `brand_classification` | `ME` |
| `brand_confidence` | `HIGH` |
| `brand_signal_source` | `hint` |
| `requires_human_review` | `false` |

---

### Module 4.3 — [Text Parser] Keyword Scan — SSS Signals

**Make Module Type:** Text Parser > Match Pattern  
**Executes on:** Route C (no valid hint)  
**Purpose:** Scan `message`, `occasion`, and `package_interest` fields for SSS-brand keywords.

**Input text (concatenated):**
```
{{lower(1.message)}} {{lower(1.occasion)}} {{lower(1.package_interest)}}
```

**Pattern (regex):**
```
(sailing|yacht|sunset cruise|bachelorette|birthday|girls trip|girls' trip|engagement|anniversary sail|leisure|recreational|pleasure|private sail|day sail|snorkel)
```

**Output variable:** `sss_match_count` (number of matches found)

---

### Module 4.4 — [Text Parser] Keyword Scan — ME Signals

**Make Module Type:** Text Parser > Match Pattern  
**Executes on:** Route C (no valid hint)  
**Purpose:** Scan same concatenated text for ME-brand keywords.

**Input text (concatenated):**
```
{{lower(1.message)}} {{lower(1.occasion)}} {{lower(1.package_interest)}}
```

**Pattern (regex):**
```
(corporate|executive|business meeting|team building|team event|incentive|retreat|mare executive|professional|client entertainment|board|offsite|conference|networking|company|enterprise)
```

**Output variable:** `me_match_count` (number of matches found)

---

### Module 4.5 — [Router] Route on Keyword Match Results

**Make Module Type:** Router  
**Purpose:** Determine brand from keyword match counts.

| Route | Condition | Filter Expression |
|-------|-----------|-------------------|
| Route D: SSS wins | SSS matches > 0 AND SSS count >= ME count | `{{4.sss_match_count}} > 0 AND {{4.sss_match_count}} >= {{4.me_match_count}}` |
| Route E: ME wins | ME matches > 0 AND ME count > SSS count | `{{4.me_match_count}} > 0 AND {{4.me_match_count}} > {{4.sss_match_count}}` |
| Route F: Ambiguous / No match | All other (both zero, or tie with zero) | Fallback |

---

### Module 4.6A — [Set Variable] brand_classification = SSS (Keyword Path)

**Make Module Type:** Set Variable  
**Executes on:** Route D  

| Variable | Value |
|----------|-------|
| `brand_classification` | `SSS` |
| `brand_confidence` | `LOW` |
| `brand_signal_source` | `keyword` |
| `requires_human_review` | `false` |

---

### Module 4.6B — [Set Variable] brand_classification = ME (Keyword Path)

**Make Module Type:** Set Variable  
**Executes on:** Route E  

| Variable | Value |
|----------|-------|
| `brand_classification` | `ME` |
| `brand_confidence` | `LOW` |
| `brand_signal_source` | `keyword` |
| `requires_human_review` | `false` |

---

### Module 4.6C — [Set Variable] brand_classification = AMBIGUOUS

**Make Module Type:** Set Variable  
**Executes on:** Route F  

| Variable | Value |
|----------|-------|
| `brand_classification` | `AMBIGUOUS` |
| `brand_confidence` | `LOW` |
| `brand_signal_source` | `default` |
| `requires_human_review` | `true` |

> Default classification pending human review is SSS. The `brand_classification` field in Airtable will be written as `AMBIGUOUS` but the `brand` field (used for operational routing) will default to `SSS` until Luciana reclassifies.

---

### Module 4.7 — [Router] Occasion-Based Override Check

**Make Module Type:** Router  
**Purpose:** Apply occasion-level override for high-confidence cases regardless of keyword scan result. Runs in parallel with keyword scan on Route C, merged via aggregator before Module 4.8.

**Occasion mapping table:**

| Occasion Value (case-insensitive) | Classification | Confidence |
|-----------------------------------|----------------|------------|
| `Bachelorette` | SSS | HIGH |
| `Birthday` | SSS | HIGH |
| `Girls Trip` | SSS | HIGH |
| `Engagement` | SSS | HIGH |
| `Anniversary` | SSS | HIGH |
| `Corporate Event` | ME | HIGH |
| `Team Building` | ME | HIGH |
| `Incentive Trip` | ME | HIGH |
| `Business Meeting` | ME | HIGH |
| `Retreat` | ME | HIGH |
| `Other` | — | (pass to keyword scan) |
| (empty) | — | (pass to keyword scan) |

**Filter expression (SSS occasions):**
```
{{contains(lower(1.occasion), "bachelorette")}} OR
{{contains(lower(1.occasion), "birthday")}} OR
{{contains(lower(1.occasion), "girls trip")}} OR
{{contains(lower(1.occasion), "engagement")}} OR
{{contains(lower(1.occasion), "anniversary")}}
```

**Filter expression (ME occasions):**
```
{{contains(lower(1.occasion), "corporate")}} OR
{{contains(lower(1.occasion), "team building")}} OR
{{contains(lower(1.occasion), "incentive")}} OR
{{contains(lower(1.occasion), "business meeting")}} OR
{{contains(lower(1.occasion), "retreat")}}
```

> If occasion match fires, it overwrites `brand_classification` and sets `brand_confidence = HIGH`.

---

### Module 4.8 — [Set Variable] Finalize Brand Output

**Make Module Type:** Set Variable  
**Purpose:** Consolidate all classification paths into a single authoritative variable block for downstream consumption.

**Logic (pseudo-code, implemented via Make IF() formulas):**
```
brand_final = if(occasion_override != null, occasion_override, keyword_classification)
confidence_final = if(occasion_override != null, "HIGH", keyword_confidence)
signal_source_final = if(hint_used, "hint", if(occasion_override != null, "occasion", "keyword"))
```

**Output variables available to M-LEAD-INTAKE:**
- `brand_classification` — SSS | ME | AMBIGUOUS
- `brand_confidence` — HIGH | LOW
- `brand_signal_source` — hint | occasion | keyword | default
- `requires_human_review` — true | false

---

## 5. Router Logic — Complete Decision Tree

```
INBOUND PAYLOAD RECEIVED
│
├── brand_hint == "SSS"  →  CLASSIFY: SSS / HIGH / hint
├── brand_hint == "ME"   →  CLASSIFY: ME / HIGH / hint
└── brand_hint is missing/unknown
    │
    ├── occasion matches SSS list  →  CLASSIFY: SSS / HIGH / occasion
    ├── occasion matches ME list   →  CLASSIFY: ME / HIGH / occasion
    └── occasion is neutral/missing
        │
        ├── SSS keyword count > 0 AND >= ME count  →  CLASSIFY: SSS / LOW / keyword
        ├── ME keyword count > 0 AND > SSS count   →  CLASSIFY: ME / LOW / keyword
        └── No keyword matches (both = 0)
            │
            └── CLASSIFY: AMBIGUOUS / LOW / default
                └── Default operational brand: SSS
                └── Flag: requires_human_review = true
                └── Alert: Slack DM to Luciana
```

---

## 6. Airtable Field Mapping

Fields written to the Requests table (`tblTlSB9CO4dTGodg`) by M-LEAD-INTAKE after M-BRAND-ROUTER classification:

| Airtable Field Name        | Make Variable / Source                  | Notes |
|----------------------------|-----------------------------------------|-------|
| `Brand`                    | `{{brand_classification}}`              | SSS, ME, or AMBIGUOUS |
| `Brand_Confidence`         | `{{brand_confidence}}`                  | HIGH or LOW |
| `Brand_Signal_Source`      | `{{brand_signal_source}}`               | hint, occasion, keyword, default |
| `Requires_Human_Brand_Review` | `{{requires_human_review}}`          | Checkbox |

> Full field mapping for the Requests record is documented in M-LEAD-INTAKE.md. This table covers only the brand classification fields output by M-BRAND-ROUTER.

---

## 7. Webhook Structure

M-BRAND-ROUTER does not expose its own webhook. It is invoked as an inline module sequence within M-LEAD-INTAKE. The parent scenario's webhook structure is documented in M-LEAD-INTAKE.md.

**Internal data passed from M-LEAD-INTAKE to M-BRAND-ROUTER module group:**

```json
{
  "source": "website_form",
  "brand_hint": "SSS",
  "message": "Looking for a bachelorette party cruise for 8 people",
  "occasion": "Bachelorette",
  "package_interest": "Sunset Sail"
}
```

**Authentication:** Inherited from M-LEAD-INTAKE webhook. No separate auth for internal module sequences.

---

## 8. Error Handling Logic

All error handling within M-BRAND-ROUTER follows the 4-level framework:

| Level | Trigger | Action |
|-------|---------|--------|
| Level 1 — Module Error | Text Parser regex fails or returns error | Set `brand_classification = AMBIGUOUS`, set `requires_human_review = true`, continue flow |
| Level 2 — Route Dead-end | No route condition matches in Router | Fallback route catches all, sets AMBIGUOUS classification |
| Level 3 — Variable Error | Set Variable module fails | Log to Audit Log, alert #sss-ops-alerts, halt scenario with error status |
| Level 4 — Scenario Crash | Unhandled exception in any module | Make Error Handler module catches, writes to Audit Log with `error_stage = "brand_router"`, sends Slack alert to Luciana |

**Error Handler Module (attached to Router and Text Parser modules):**
- Module Type: Error Handler (Make built-in)
- Directive: Resume (for Level 1-2), Rollback + Stop (for Level 3-4)
- On Resume: inject default values (`brand_classification = AMBIGUOUS`, `requires_human_review = true`)

**Make Error Handler attachment points:**
- Module 4.3 (SSS Text Parser)
- Module 4.4 (ME Text Parser)
- Module 4.5 (Router on keyword counts)

---

## 9. Retry Logic

| Scenario | Retry Behavior |
|----------|----------------|
| Text Parser regex timeout | 2 retries, 5-second interval |
| Variable write failure | 3 retries, 10-second interval |
| Router condition evaluation | No retry (deterministic) |
| Full scenario crash | No auto-retry (prevent duplicate classification) |

> Retry configuration is set in Make.com under Scenario Settings > Error handling. Max retry attempts: 3. Interval: 10 seconds.

---

## 10. Duplicate Prevention

M-BRAND-ROUTER operates on data already deduplicated by M-LEAD-INTAKE. It does not perform its own duplicate check. The idempotency guarantee is:

- Brand classification is deterministic: the same input payload will always produce the same `brand_classification` output.
- If M-LEAD-INTAKE detects a duplicate and halts, M-BRAND-ROUTER module group is never reached.
- If M-BRAND-ROUTER is somehow invoked twice for the same payload (scenario re-run), the Airtable record update is an upsert: writing the same `brand_classification` value to an already-classified record is idempotent.

**Idempotency key:** Inherited from M-LEAD-INTAKE — `SHA256(email + phone + submitted_at)`. This key is checked before M-BRAND-ROUTER executes.

---

## 11. Slack Alert Structure

M-BRAND-ROUTER itself does not post to Slack. However, it sets `requires_human_review = true` for AMBIGUOUS cases, which triggers a specific Slack alert in M-SLACK-ALERTS.

**AMBIGUOUS classification triggers this additional alert block** (appended to the standard new-lead alert):

```json
{
  "type": "section",
  "text": {
    "type": "mrkdwn",
    "text": ":warning: *Brand Classification Ambiguous* — No clear SSS or ME signals detected. Defaulting to SSS. *Luciana: please classify this lead.*"
  }
},
{
  "type": "actions",
  "elements": [
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Classify as SSS" },
      "value": "classify_sss_{{request_id}}",
      "action_id": "brand_classify_sss"
    },
    {
      "type": "button",
      "text": { "type": "plain_text", "text": "Classify as ME" },
      "value": "classify_me_{{request_id}}",
      "action_id": "brand_classify_me"
    }
  ]
}
```

---

## 12. Audit Log Writes

**Table:** `tblrMpTfMk8q1eNHp` (Audit Log)

A brand classification event is logged after Module 4.8 completes.

| Audit Log Field | Value |
|-----------------|-------|
| `Event_Type` | `BRAND_CLASSIFIED` |
| `Scenario_Name` | `M-BRAND-ROUTER` |
| `Request_ID` | `{{request_id}}` (from M-LEAD-INTAKE) |
| `Brand_Result` | `{{brand_classification}}` |
| `Confidence` | `{{brand_confidence}}` |
| `Signal_Source` | `{{brand_signal_source}}` |
| `Requires_Review` | `{{requires_human_review}}` |
| `Timestamp` | `{{now}}` (ISO 8601) |
| `Execution_ID` | `{{executionId}}` (Make built-in) |
| `Status` | `SUCCESS` or `ERROR` |
| `Error_Detail` | Null on success; error message on failure |

---

## 13. Automation Health Writes

**Table:** Automation Health (field in Requests table or dedicated health table — confirm with Airtable schema)

After successful brand classification:

| Field | Value |
|-------|-------|
| `Last_Brand_Router_Run` | `{{now}}` |
| `Brand_Router_Status` | `OK` |
| `Brand_Router_Execution_ID` | `{{executionId}}` |

On failure:

| Field | Value |
|-------|-------|
| `Brand_Router_Status` | `ERROR` |
| `Brand_Router_Error` | Error message string |
| `Brand_Router_Error_Time` | `{{now}}` |

---

## 14. Rollback Procedure

M-BRAND-ROUTER does not write to Airtable directly; it only sets Make variables. The parent scenario M-LEAD-INTAKE owns all Airtable writes. Therefore, rollback is managed at the M-LEAD-INTAKE level.

**If brand classification produces incorrect result:**

1. Luciana identifies the misclassified Airtable Request record.
2. In Airtable Requests table: manually update `Brand` field to the correct value.
3. Manually update `Brand_Confidence` to `MANUAL_OVERRIDE`.
4. Manually update `Brand_Signal_Source` to `human_override`.
5. Clear `Requires_Human_Brand_Review` checkbox.
6. Write a note in the `Internal_Notes` field: `"Brand manually corrected by [name] on [date]. Original: [old brand]."`.
7. Write a correction entry to Audit Log: Event_Type = `BRAND_OVERRIDE`, Status = `MANUAL`.
8. Re-trigger any downstream notifications if needed (M-SLACK-ALERTS can be manually triggered with the corrected Request ID).

**No automated rollback is required** because no data is destroyed — classification values are overwritten, not deleted.

---

## 15. Sandbox Test Procedure

**Prerequisites:**
- Make.com scenario in INACTIVE state (do not run live)
- Test payloads prepared (see below)
- Airtable test record target identified
- Slack channel: #sss-ops-alerts (test messages acceptable; prefix all test messages with `[TEST]`)

**Test Cases:**

### Test 1 — Explicit SSS brand_hint
```json
{
  "source": "website_form",
  "brand_hint": "SSS",
  "message": "I want to book a sunset sail",
  "occasion": "Birthday",
  "package_interest": "Sunset Sail"
}
```
**Expected:** `brand_classification = SSS`, `brand_confidence = HIGH`, `brand_signal_source = hint`

### Test 2 — Explicit ME brand_hint
```json
{
  "source": "typeform",
  "brand_hint": "ME",
  "message": "Corporate team building event for 20 executives",
  "occasion": "Corporate Event",
  "package_interest": "Executive Package"
}
```
**Expected:** `brand_classification = ME`, `brand_confidence = HIGH`, `brand_signal_source = hint`

### Test 3 — No hint, SSS keyword match
```json
{
  "source": "instagram_dm",
  "brand_hint": "",
  "message": "Looking for a bachelorette party yacht rental",
  "occasion": "",
  "package_interest": ""
}
```
**Expected:** `brand_classification = SSS`, `brand_confidence = LOW`, `brand_signal_source = keyword`

### Test 4 — No hint, ME keyword match
```json
{
  "source": "direct",
  "brand_hint": "",
  "message": "Planning a corporate retreat and need a business meeting venue on water",
  "occasion": "",
  "package_interest": ""
}
```
**Expected:** `brand_classification = ME`, `brand_confidence = LOW`, `brand_signal_source = keyword`

### Test 5 — Ambiguous (no hint, no keywords)
```json
{
  "source": "website_form",
  "brand_hint": "",
  "message": "I need a boat for a special event next month",
  "occasion": "Other",
  "package_interest": ""
}
```
**Expected:** `brand_classification = AMBIGUOUS`, `brand_confidence = LOW`, `requires_human_review = true`

### Test 6 — Occasion override (high-confidence)
```json
{
  "source": "website_form",
  "brand_hint": "",
  "message": "Planning something special",
  "occasion": "Bachelorette",
  "package_interest": ""
}
```
**Expected:** `brand_classification = SSS`, `brand_confidence = HIGH`, `brand_signal_source = occasion`

**Test Execution Steps:**
1. Open M-LEAD-INTAKE scenario in Make.com.
2. Navigate to the M-BRAND-ROUTER module group.
3. Use "Run once" with manual trigger (paste test payload into webhook test tool).
4. Inspect module output after Module 4.8.
5. Verify `brand_classification`, `brand_confidence`, `brand_signal_source`, `requires_human_review` match expected values.
6. Verify Audit Log record was created.
7. For Test 5: verify `requires_human_review = true` and confirm Slack alert includes AMBIGUOUS block.
8. Log all test results in the scenario test log.

---

## 16. Production Validation Checklist

**Go/No-Go Criteria — M-BRAND-ROUTER must pass ALL items before enabling in production:**

- [ ] All 6 sandbox test cases pass with expected outputs
- [ ] Audit Log writes confirmed for each test (6 records created)
- [ ] AMBIGUOUS path triggers correct Slack alert block
- [ ] Occasion override correctly outranks keyword scan result
- [ ] Error handler correctly sets AMBIGUOUS on Text Parser failure (force-test by injecting malformed regex input)
- [ ] Variables are correctly accessible by downstream modules in M-LEAD-INTAKE (test Module 5+ field mapping)
- [ ] No duplicate Audit Log entries created when scenario re-runs on same payload
- [ ] Brand_Confidence = HIGH only fires for hint and occasion paths (never for keyword path)
- [ ] ME keyword list does not match false-positive SSS terms (test: "sailing retreat" — should classify SSS because SSS keyword count equals ME count and SSS is favored on ties)
- [ ] Will has reviewed classification logic and approved keyword lists
- [ ] Luciana has reviewed AMBIGUOUS alert format and approves the Slack buttons

**Sign-off Required From:**
- [ ] Will (Founder) — routing logic approval
- [ ] Luciana (Ops Lead) — operational workflow approval

---

## 17. Open Issues

| ID | Issue | Owner | Status |
|----|-------|-------|--------|
| BR-001 | Tie-breaking rule when SSS and ME keyword counts are equal (currently defaults to SSS) — confirm this is correct business rule | Will | OPEN |
| BR-002 | `brand_hint` field: confirm all intake sources (Typeform, Instagram DM, website form) reliably populate this field | Luciana | OPEN |
| BR-003 | Occasion field values: need exhaustive list of all possible values from Typeform to ensure occasion override mapping is complete | Luciana | OPEN |
| BR-004 | Confirm whether Slack action buttons (Classify as SSS / ME) require a separate Make webhook to receive button click events | Systems | OPEN |
| BR-005 | Multi-brand inquiry (e.g., client asks about both SSS and ME) — current logic will classify SSS if SSS keyword count >= ME count; need business rule for this edge case | Will | OPEN |
| BR-006 | URL-based brand detection (e.g., form submitted from shesaidsail.com vs mareexecutive.com) — not yet implemented in current logic, pending URL field in webhook payload | Systems | OPEN |

---

## 18. Final Scenario Status

**Status: PENDING BUILD**

> This document is the authoritative build specification. No Make.com scenario has been created yet. Begin build only after Will and Luciana have signed off on Sections 5 (Decision Tree) and 16 (Go/No-Go Checklist).
