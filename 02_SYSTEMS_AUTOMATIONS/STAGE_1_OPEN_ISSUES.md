# STAGE_1_OPEN_ISSUES.md

**Status:** ACTIVE — Updated May 2026
**Owner:** Will (Founder)
**Scope:** Stage 1 Make build — all known blockers, warnings, and open questions
**Authority:** Issues in this document must be resolved before production promotion unless explicitly accepted as a WARNING by Will.

---

## ISSUE SEVERITY CLASSIFICATION

| Severity | Label | Definition | Can Go Live? |
|----------|-------|------------|-------------|
| BLOCKER | 🔴 BLOCKER | Prevents production activation. Must be resolved first. | No |
| WARNING | 🟡 WARNING | Known gap accepted with mitigation. Will signs off. | Yes — with documented acceptance |
| INFO | 🔵 INFO | Minor gap or future improvement. No immediate action required. | Yes |

---

## BLOCKERS

### BLOCKER-001 — Email Templates Not Created
**Severity:** 🔴 BLOCKER
**Affects:** INBOUND-001, BOOKING-001, BOOKING-002, BOOKING-004
**Description:**
8 client-facing email templates are required before any scenario can go live. None have been drafted or approved. Sending an empty, broken, or placeholder email to a live lead is a brand and client experience failure.

**Required Templates:**
1. Auto-reply SSS (INBOUND-001)
2. Auto-reply ME (INBOUND-001)
3. Deposit Request SSS (BOOKING-001)
4. Deposit Request ME (BOOKING-001)
5. Deposit Confirmation SSS (BOOKING-002)
6. Deposit Confirmation ME (BOOKING-002)
7. Booking Confirmation SSS (BOOKING-004)
8. Booking Confirmation ME (BOOKING-004)

**Resolution Required:**
- Draft all 8 templates
- Will reviews and approves each
- Templates stored in Make or Airtable (not hardcoded in scenario)
- Sign-off recorded in STAGE_1_TEST_RESULTS.md Client Message Safety Review

**Owner:** Will + Luciana
**Target:** Before any scenario promoted to production
**Status:** OPEN

---

### BLOCKER-002 — Airtable Field Gaps on Bookings Table
**Severity:** 🔴 BLOCKER
**Affects:** BOOKING-001, BOOKING-002, BOOKING-003, BOOKING-004, EMERGENCY-001, AUDIT-001
**Description:**
Several fields required by Stage 1 scenarios are not confirmed present in the production Bookings table (tbl72omPibBkn2hZL). The Airtable Final Build Spec identified the table as having 129 fields — but the specific fields below must be verified to exist with the correct type, or added.

**Fields to Confirm or Add:**

| Field | Type | Required By | Status |
|-------|------|-------------|--------|
| Environment | Single Select: Production/Sandbox/Development | ALL scenarios (filter) | MISSING — add |
| Brand | Single Select: SSS/ME | ALL scenarios | CONFIRM EXISTS |
| Automations_Paused | Checkbox | ALL pre-condition checks | CONFIRM EXISTS |
| Emergency_Flag | Checkbox | EMERGENCY-001, all checks | CONFIRM EXISTS |
| HV_Client | Checkbox | INBOUND-002, BOOKING-004 | CONFIRM — may exist as "HV Booking" |
| Agreement_Signed | Checkbox | BOOKING-003, BOOKING-004 | CONFIRM EXISTS |
| Deposit_Pct | Number | BOOKING-001 | MISSING — add or default 50% |
| Stripe_Deposit_Link | URL | BOOKING-001 write | CONFIRM EXISTS |
| Stripe_Payment_Intent_ID | Text | BOOKING-002 write | MISSING — add |
| Deposit_Amount_Received | Currency | BOOKING-002 write | MISSING — add |
| Deposit_Sent_At | DateTime | BOOKING-001 write | CONFIRM EXISTS |
| Deposit_Received_At | DateTime | BOOKING-002 write | MISSING — add |
| Charter_Brief | Long Text | BOOKING-004 write | CONFIRM EXISTS |
| Charter_Brief_Generated_At | DateTime | BOOKING-004 write | MISSING — add |
| Agreement_Alert_Sent_At | DateTime | BOOKING-003 write | MISSING — add |
| Source_System | Single Select | ALL write | MISSING — add |

**Resolution Required:**
- Audit Bookings table field-by-field against above list
- Add all MISSING fields per type specification
- Confirm all CONFIRM EXISTS fields have correct type
- Schema changes require Will approval per governance rules

**Owner:** Will (schema authority) + Luciana (field audit)
**Target:** Before sandbox test execution
**Status:** OPEN

---

### BLOCKER-003 — Requests Table Field Gaps
**Severity:** 🔴 BLOCKER
**Affects:** INBOUND-001, INBOUND-002
**Description:**
The Requests table (tblTlSB9CO4dTGodg) is missing governance-required fields needed for INBOUND-002 to write AI state properly.

**Fields to Confirm or Add:**

| Field | Type | Status |
|-------|------|--------|
| Agent_Status | Single Select: AI_RESPONDING/HUMAN_REVIEW/ESCALATED/CLOSED | EXISTS as "Agent Status" — confirm type |
| Last_AI_Action | DateTime | EXISTS as "Last_Agent_Message_Timestamp" — rename |
| Escalation_Reason | Long Text | MISSING — create |
| AI_Confidence_Score | Number 0-100 | MISSING — create |
| Last_Human_Touch | DateTime | MISSING — create |
| Environment | Single Select: Production/Sandbox/Development | MISSING — create |
| Brand | Single Select: SSS/ME | CONFIRM EXISTS |
| Source_System | Single Select | MISSING — create |
| Source_Channel | Single Select: Webflow/Instagram/Direct/Other | CONFIRM OR CREATE |

**Resolution Required:**
- Audit Requests table against above list
- Create missing fields, confirm existing field types
- Will approval for any schema change

**Owner:** Will + Luciana
**Target:** Before sandbox test execution
**Status:** OPEN

---

### BLOCKER-004 — Audit Log Table Field Gaps
**Severity:** 🔴 BLOCKER
**Affects:** AUDIT-001 (affects all scenarios)
**Description:**
The Audit Log table (tblrMpTfMk8q1eNHp) was confirmed in the Airtable Final Build Spec as needing 8 missing governance fields. Without these fields, AUDIT-001 cannot write complete records.

**Fields to Add:**

| Field | Type |
|-------|------|
| Scenario_Name | Text |
| Scenario_ID | Text |
| AI_Prompt_Version_ID | Text |
| Idempotency_Key | Text |
| Success | Checkbox |
| Environment | Single Select: Production/Sandbox/Development |
| Brand | Single Select: SSS/ME |
| Source_System | Single Select: Make/Manual/API |

**Resolution Required:**
- Add all 8 fields to Audit Log table
- Will approval required

**Owner:** Will
**Target:** Before any scenario goes live — Audit Log is the first dependency
**Status:** OPEN

---

### BLOCKER-005 — Sandbox Airtable Base Not Confirmed
**Severity:** 🔴 BLOCKER
**Affects:** All testing
**Description:**
The governance requires a dedicated SSS Sandbox base for Make scenario testing. This base does not have a confirmed Base ID in the current architecture. Sandbox testing must not touch production data. Without this base, testing cannot proceed safely.

**Resolution Required:**
- Create SSS Sandbox base by cloning SSS Operations (appdZ49WqgjRXxA1R) schema
- Populate with realistic test data only — no real client information
- Document Base ID in this file once created
- Configure all Make sandbox scenarios to point to sandbox base

**Sandbox Base ID (populate when created):** `______________________`

**Owner:** Will
**Target:** Before any sandbox testing begins
**Status:** OPEN

---

### BLOCKER-006 — Make Credential Vault Not Confirmed
**Severity:** 🔴 BLOCKER
**Affects:** BOOKING-001 (Stripe), BOOKING-002 (Stripe), INBOUND-002 (Claude API), BOOKING-001 (Quo SMS)
**Description:**
All API credentials must be stored in Make's credential vault before scenarios can be built and tested. The following are required and must NOT be stored in any GitHub file, Airtable record, or plain text.

**Required Credentials:**

| Credential | System | Make Connection Name |
|-----------|--------|---------------------|
| Stripe API Key (Test Mode) | Stripe | SSS_Stripe_Test |
| Stripe API Key (Production) | Stripe | SSS_Stripe_Production |
| Stripe Webhook Signing Secret (Test) | Stripe | SSS_Stripe_Webhook_Test |
| Stripe Webhook Signing Secret (Production) | Stripe | SSS_Stripe_Webhook_Production |
| Claude API Key | Anthropic | SSS_Claude_Production |
| Quo SMS API Key | Quo | SSS_Quo_Production |
| Airtable PAT (Production) | Airtable | SSS_Airtable_Production |
| Airtable PAT (Sandbox) | Airtable | SSS_Airtable_Sandbox |
| Gmail OAuth (hello@shesaidsail.com) | Gmail | SSS_Gmail_Production |
| Slack OAuth | Slack | SSS_Slack_Production |

**Resolution Required:**
- Store all credentials in Make before building any scenario
- Test each connection independently before attaching to scenarios
- Confirm Slack OAuth has permission to write to #sss-new-leads, #sss-ops-bookings, #sss-emergency-ops, #sss-ops-alerts, DM to Luciana, DM to Will

**Owner:** Will
**Target:** Before sandbox scenario build begins
**Status:** OPEN

---

### BLOCKER-007 — Stripe Webhook Not Registered
**Severity:** 🔴 BLOCKER
**Affects:** BOOKING-002
**Description:**
The Stripe webhook endpoint for BOOKING-002 does not exist until the Make scenario is built and the webhook URL is generated. The Stripe dashboard must be configured to send payment events to this URL. Until this is done, deposits received via Stripe will NOT trigger Airtable updates or confirmation emails.

**Steps to Resolve:**
1. Build BOOKING-002 Make scenario
2. Copy the Make webhook URL
3. Register in Stripe Dashboard → Developers → Webhooks
4. Subscribe to events: `payment_intent.succeeded`, `checkout.session.completed`
5. Copy Stripe Webhook Signing Secret into Make credential vault
6. Test with Stripe CLI: `stripe trigger payment_intent.succeeded`

**Webhook URL (populate after scenario built):** `______________________`

**Owner:** Will (Stripe access required)
**Target:** Before live payments accepted
**Status:** OPEN

---

## WARNINGS

### WARNING-001 — Quo SMS Character Limits Not Pre-Validated
**Severity:** 🟡 WARNING
**Affects:** BOOKING-001 SMS
**Description:**
The Quo SMS message templates for BOOKING-001 include a Stripe payment link URL. Stripe payment link URLs can be 40-60+ characters. Combined with the message body, total character count may exceed 160-char single SMS boundary. Multi-segment SMS carries higher cost and different deliverability characteristics.

**Mitigation:**
- Use a URL shortener (e.g., bit.ly or custom short domain) for Stripe links in SMS
- OR accept two-segment SMS and confirm Quo pricing for multi-segment
- Pre-measure all SMS templates against 160-char limit before production send

**Accepted By Will:** ☐ Yes ☐ No
**If No:** Resolve before production
**Status:** OPEN

---

### WARNING-002 — AI Draft Quality Not Validated Against Brand Standards
**Severity:** 🟡 WARNING
**Affects:** INBOUND-002
**Description:**
Claude's first-response draft quality depends on the production prompt in AI_Prompt_Versions. The current AI_Prompt_Versions table in the main base (tbl0FJkA1E6a70cxX) has only 9 fields and is not production-ready per the Airtable Final Build Spec. If INBOUND-002 is activated with the incomplete prompt version table, AI responses may not match brand voice.

**Mitigation:**
- Build proper AI_Prompt_Versions table per spec before INBOUND-002 goes live
- OR: delay INBOUND-002 production activation and use human-only response until AI prompt governance is complete

**Recommended Approach:** INBOUND-001 goes live first (no AI dependency). INBOUND-002 activates only after AI_Prompt_Versions table is rebuilt and Will approves the production prompt.

**Accepted By Will:** ☐ Yes ☐ No
**Status:** OPEN

---

### WARNING-003 — ME Brand Not Fully Configured
**Severity:** 🟡 WARNING
**Affects:** INBOUND-001, BOOKING-001, BOOKING-002, BOOKING-004 (ME branches)
**Description:**
The architecture supports both SSS and ME brand routing. However, if ME-specific Airtable records (ME Packages, ME Packages pricing, ME email templates, ME Slack channels) are not fully configured, ME leads will either error or receive SSS-branded responses.

**Mitigation Options:**
A. Launch Stage 1 for SSS only. Disable ME routing until ME config is complete.
B. Launch for both brands simultaneously but validate ME sandbox tests pass first.

**Recommended:** Option A. Stage 1 launches SSS only. ME activation is a separate go-live gate with its own test run.

**Accepted By Will:** ☐ SSS First (A) ☐ Both simultaneously (B)
**Status:** OPEN

---

### WARNING-004 — Emergency_Flag Poll Interval Creates 60-Second Window
**Severity:** 🟡 WARNING
**Affects:** EMERGENCY-001
**Description:**
EMERGENCY-001 is triggered by Airtable Record Updated (watch). Make's Airtable watch module polls on a configurable interval — minimum effective interval in production is approximately 1-2 minutes. This means up to 2 minutes could pass between Emergency_Flag being set and the emergency protocol activating.

**Mitigation:**
- Acceptable risk given that Will or Luciana would also be taking manual action simultaneously
- Supplement with Airtable Native Automation as a backup trigger for instant response (Airtable → Slack DM to Will) — this fires immediately on field change
- Make scenario handles full protocol; Airtable native automation provides instant notification

**Accepted By Will:** ☐ Yes — acceptable gap ☐ No — mitigate first
**Status:** OPEN

---

### WARNING-005 — Charter Brief Sent Only to Luciana at Stage 1
**Severity:** 🟡 WARNING
**Affects:** BOOKING-004
**Description:**
The Systems Intelligence Architecture defines a T-14 Charter Brief delivery to Luciana (BOOKING-004 scope) and a T-48 delivery to City Manager (Stage 2 scope, CHARTER-005). At Stage 1, City Managers do not receive automated Charter Brief delivery — Luciana must manually forward.

**Mitigation:**
- Luciana is explicitly responsible for T-48 City Manager notification until CHARTER-005 is live
- SOP update required confirming this manual step
- Stage 2 build eliminates this manual step

**Accepted By Will:** ☐ Yes — manual step documented ☐ No
**Status:** OPEN

---

## INFO ITEMS

### INFO-001 — Make Scenario IDs Not Yet Generated
**Severity:** 🔵 INFO
**Description:**
Make internal scenario IDs are assigned when scenarios are built. The STAGE_1_MAKE_BUILD_REPORT.md references them as placeholders. Once built, update all scenario ID references in:
- STAGE_1_MAKE_BUILD_REPORT.md
- Audit Log template (Scenario_ID field)
- Make_Scenarios Airtable table (if built)

**Action:** Populate after build. No production blocker.

---

### INFO-002 — Webhook URLs Not Yet Generated
**Severity:** 🔵 INFO
**Description:**
INBOUND-001 and BOOKING-002 require webhook URLs that are generated when Make scenarios are built. After build:
1. Document webhook URLs in this file
2. Register INBOUND-001 URL in Webflow form submission settings
3. Register BOOKING-002 URL in Stripe dashboard

**INBOUND-001 Webhook URL (Production):** `______________________`
**BOOKING-002 Stripe Webhook URL (Production):** `______________________`

---

### INFO-003 — Automation_Health Table Not Yet Built
**Severity:** 🔵 INFO
**Affects:** EMERGENCY-001 (step 3 — cancel pending sends)
**Description:**
The Automation_Health table is required for EMERGENCY-001 to identify and cancel pending scheduled sends for a booking. This table was specified in the Airtable Final Build Spec as a new build. It is not yet created. At Stage 1 launch, the cancel-pending-sends step of EMERGENCY-001 will log a warning rather than cancel (since there are no Stage 2+ scheduled sends yet). This is acceptable at Stage 1 since CHARTER-001 through CHARTER-007 are not yet live.

**Action:** Build Automation_Health table in Stage 2 before CHARTER sequences go live.

---

### INFO-004 — AI Audit Table Not Yet Built
**Severity:** 🔵 INFO
**Affects:** INBOUND-002 drift detection
**Description:**
The AI_Audit table required for weekly AI drift review does not yet exist. AI response quality monitoring at Stage 1 is manual — Luciana reviews samples weekly. The formal AI_Audit table is a Stage 2 build item.

---

### INFO-005 — Make Scenario Version Control Not Yet Established
**Severity:** 🔵 INFO
**Description:**
The Make_Scenarios table (specified as a new build from app2FbmVD44BXShyx) does not yet exist in the production base. This table tracks: Scenario_ID, Name, Version, Status, Last_Modified, Dependencies. At Stage 1, scenario documentation lives in GitHub (this file). Make_Scenarios table is a Stage 2 build item.

---

## RESOLUTION TRACKER

| Issue ID | Description | Owner | Target Date | Resolved | Resolved Date |
|----------|-------------|-------|-------------|---------|---------------|
| BLOCKER-001 | Email templates | Will + Luciana | Before production | ☐ | |
| BLOCKER-002 | Bookings field gaps | Will + Luciana | Before sandbox | ☐ | |
| BLOCKER-003 | Requests field gaps | Will + Luciana | Before sandbox | ☐ | |
| BLOCKER-004 | Audit Log field gaps | Will | Before scenarios | ☐ | |
| BLOCKER-005 | Sandbox base | Will | Before testing | ☐ | |
| BLOCKER-006 | Make credentials | Will | Before build | ☐ | |
| BLOCKER-007 | Stripe webhook | Will | Before live payments | ☐ | |
| WARNING-001 | SMS char limits | Luciana | Before production | ☐ | |
| WARNING-002 | AI prompt governance | Will | INBOUND-002 only | ☐ | |
| WARNING-003 | ME brand config | Will | ME launch gate | ☐ | |
| WARNING-004 | Emergency poll gap | Will | Decision required | ☐ | |
| WARNING-005 | City Manager brief | Luciana | SOP update | ☐ | |

---

## STAGE 1 FINAL VERDICT

**Current Status:** PENDING

Blockers outstanding: **7**
Warnings requiring decision: **5**
Production promotion: **BLOCKED until all BLOCKERs resolved**

Once BLOCKER-001 through BLOCKER-007 are resolved and all tests in STAGE_1_TEST_RESULTS.md pass:

> Final verdict options:
> - **READY FOR LIVE LEADS** — all gates pass, no open blockers
> - **READY WITH WARNINGS** — BLOCKERs resolved, warnings documented and accepted by Will
> - **NOT READY** — any BLOCKER unresolved or any Critical test failure

**Final Verdict (Will signs off):** _______________
**Date:** _______________
**Conditions:** _______________
