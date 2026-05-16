# AIRTABLE_FIELD_MAPPING_REGISTRY

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Exact Airtable field references used by every Make scenario. Engineers building Make scenarios reference this document to confirm field names and types before wiring modules.
**Classification:** Confidential — Internal Use Only

---

## IMPORTANT NOTES

1. **Field IDs vs. Field Names:** Make references fields by field ID (fldXXXXXXXXXXXXXX format) in the Airtable module configuration. Field names listed here are the human-readable names — the engineer must map these to field IDs in the Make Airtable module after running get_table_schema for each table.

2. **Field IDs must be retrieved from live Airtable** using the Airtable API or MCP tool `get_table_schema` before building any scenario. This document uses field names as the canonical reference.

3. **Fields marked [TO ADD]** must be created in Airtable before the corresponding Make scenario is built.

4. **Base IDs:**
   - SSS Operations (PRIMARY): `appdZ49WqgjRXxA1R`
   - SSS Financials: `apprDKQtV2GInThwE`

---

## TABLE: REQUESTS (tblTlSB9CO4dTGodg)

Primary operations base: `appdZ49WqgjRXxA1R`

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Name | Single Line Text | M-LEAD-INTAKE | W | Client full name from form |
| Email | Email | M-LEAD-INTAKE | W | Primary contact email |
| Phone | Phone | M-LEAD-INTAKE | W | Mobile number |
| Charter_Date | Date | M-LEAD-INTAKE, M-BOOKING-CREATION | R/W | Requested charter date |
| Group_Size | Number | M-LEAD-INTAKE, M-BOOKING-CREATION | R/W | Guest count |
| Occasion | Text | M-LEAD-INTAKE, M-BRAND-ROUTER | R/W | Occasion type |
| Notes | Long Text | M-LEAD-INTAKE | W | Client notes from form |
| Brand | Single Select | M-BRAND-ROUTER, M-BOOKING-CREATION | R/W | SSS / ME |
| Source_Channel | Single Select | M-LEAD-INTAKE | W | Meta / Google / Organic / Referral / Direct |
| Source_System | Single Select | M-LEAD-INTAKE | W | Always "Make" for automated intake |
| Environment | Single Select | ALL | R/W | Production / Sandbox / Development |
| Status | Single Select | ALL | R/W | NEW → AVAILABILITY_PENDING → AVAILABILITY_CONFIRMED → BOOKING_CREATED → CLOSED |
| Created_At | DateTime | M-LEAD-INTAKE | W | Set on creation |
| Idempotency_Key | Single Line Text [TO ADD] | M-LEAD-INTAKE | W | SHA256 hash for dedup |
| Routing_Confidence | Single Select [TO ADD] | M-BRAND-ROUTER | W | HIGH / MEDIUM / LOW |
| Agent_Status | Single Select | M-ESCALATION-ROUTER | R/W | AI_RESPONDING / HUMAN_REVIEW / ESCALATED / CLOSED |
| Escalation_Reason | Long Text [TO ADD] | M-ESCALATION-ROUTER | R/W | Why escalated |
| AI_Confidence_Score | Number [TO ADD] | M-AI-LEAD-SCORING | W | 0-100 |
| AI_Lead_Score | Number [TO ADD] | M-AI-LEAD-SCORING | W | 0-100 overall score |
| AI_Lead_Priority | Single Select [TO ADD] | M-AI-LEAD-SCORING | W | HIGH / MEDIUM / LOW |
| AI_Lead_Signals | Long Text [TO ADD] | M-AI-LEAD-SCORING | W | Key signals driving score |
| AI_Scored_At | DateTime [TO ADD] | M-AI-LEAD-SCORING | W | Timestamp of score |
| Last_Human_Touch | DateTime [TO ADD] | M-ESCALATION-ROUTER | W | Human interaction timestamp |
| Client_Link | Linked Record (Clients) | M-BOOKING-CREATION | R | Linked Client record |
| Yacht_Link | Linked Record (Yachts) | M-BOOKING-CREATION | R | Vessel preference |
| Package_Link | Linked Record (Packages) | M-BOOKING-CREATION | R | Package selected |
| Linked_Booking_ID | Single Line Text [TO ADD] | M-BOOKING-CREATION | W | Booking record ID after creation |

**Trigger Field for M-BOOKING-CREATION webhook:** `Status` → value = `AVAILABILITY_CONFIRMED`
**Trigger Field for M-ESCALATION-ROUTER webhook:** `Agent_Status` → value = `ESCALATED`
**Trigger Field for M-AI-LEAD-SCORING webhook:** `Status` → value = `NEW`

---

## TABLE: BOOKINGS (tbl72omPibBkn2hZL)

Primary operations base: `appdZ49WqgjRXxA1R`

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Booking_ID | Formula | ALL | R | BK-YYYY-NNNN format |
| Status | Single Select | ALL | R/W | Core state machine field |
| Charter_Date | Date | M-BASIC-LIFECYCLE, M-REVIEW-REQUEST | R | Date of charter |
| Group_Size | Number | M-BOOKING-CREATION, M-CHARTER-BRIEF | R/W | Guest count |
| Package_Price | Currency | M-BOOKING-CREATION | R | Must not be written after CONFIRMED |
| Deposit_Amount | Currency | M-BOOKING-CREATION | R/W | 50% of Package_Price |
| Stripe_Deposit_Link | URL | M-BOOKING-CREATION | W | Payment link URL |
| Stripe_Payment_Intent_ID | Single Line Text | M-STRIPE-DEPOSIT | R/W | Stripe PI ID for matching |
| Deposit_Paid_At | DateTime | M-STRIPE-DEPOSIT | W | Timestamp of deposit receipt |
| Confirmation_Sent_At | DateTime | M-BOOKING-CONFIRMATION | W | When confirmation was sent |
| Concierge_Notified_At | DateTime [TO ADD] | M-CONCIERGE-ASSIGNMENT | W | When concierge was notified |
| Emergency_Flag | Checkbox | ALL outbound | R | Check FIRST — if true, stop all outbound |
| Automations_Paused | Checkbox | ALL outbound | R | Check SECOND — if true, stop all outbound |
| HV_Client | Checkbox | M-BOOKING-CONFIRMATION, M-REVIEW-REQUEST | R | High-value client — routes to human |
| Environment | Single Select | ALL | R | Check on entry — exit if not Production |
| Brand | Single Select | ALL | R/W | SSS / ME |
| City | Single Select | ALL | R/W | Market context |
| Source_System | Single Select | M-BOOKING-CREATION | W | Make |
| Idempotency_Key | Single Line Text [TO ADD] | M-BOOKING-CREATION, M-STRIPE-DEPOSIT | R/W | Dedup key |
| Charter_Grade | Single Select | M-REVIEW-REQUEST, M-REFERRAL-ENGINE | R | A / B / C / D / F |
| D7_Review_Eligible | Formula | M-REVIEW-REQUEST | R | TRUE/FALSE — formula field |
| D72hr_Reminder_Sent | Checkbox | M-BASIC-LIFECYCLE | R/W | Gate for T-72hr message |
| D48hr_Reminder_Sent | Checkbox | M-BASIC-LIFECYCLE | R/W | Gate for T-48hr message |
| D24hr_Reminder_Sent | Checkbox | M-BASIC-LIFECYCLE | R/W | Gate for T-24hr message |
| D12hr_Reminder_Sent | Checkbox | M-BASIC-LIFECYCLE | R/W | Gate for T-12hr message |
| D1_Sent | Checkbox | M-BASIC-LIFECYCLE | R/W | Gate for D1 message |
| D7_Sent | Checkbox | M-REVIEW-REQUEST | R/W | Gate for D7 review request |
| D30_Sent | Checkbox | M-REFERRAL-ENGINE | R/W | Gate for D30 referral |
| D60_Sent | Checkbox | M-REBOOKING-ENGINE | R/W | Gate for D60 rebooking |
| Charter_Brief_Sent | Checkbox | M-VENDOR-NOTIFICATIONS | R | Triggers vendor notifications |
| Charter_Brief_All_Vendors_Confirmed | Checkbox | M-VENDOR-NOTIFICATIONS | W | All vendors acknowledged |
| Balance_Paid | Checkbox | M-BASIC-LIFECYCLE, M-CHARTER-BRIEF | R | Gate for balance collection reminder |
| Agreement_Signed | Checkbox | M-CHARTER-BRIEF | R | Required before Charter Brief for >$5K |
| Chargeback_Risk | Single Select | M-REVIEW-REQUEST | R | LOW / MEDIUM / HIGH / ACTIVE |
| Net_Profit | Formula | M-SYNTER-SYNC | R | Auto-calculated — never written |
| Net_Margin_Pct | Formula | M-REVENUE-HEALTH, M-SYNTER-SYNC | R | Auto-calculated |
| Financial_Sync_Status | Single Select [TO ADD] | M-SYNTER-SYNC | W | SYNCED / FAILED / PENDING |
| Financial_Sync_At | DateTime [TO ADD] | M-SYNTER-SYNC | W | Last sync timestamp |
| Payment_Failure_Count | Number [TO ADD] | M-FAILED-PAYMENT-HANDLER | R/W | Increments on each failure |
| Last_Payment_Failure_At | DateTime [TO ADD] | M-FAILED-PAYMENT-HANDLER | W | Last failure timestamp |
| Payment_Failure_Reason | Single Line Text [TO ADD] | M-FAILED-PAYMENT-HANDLER | W | Stripe failure code |
| Fatigue_Flag | Checkbox | M-CREATIVE-FATIGUE | W | On Paid_Ads table, not Bookings |
| Request_Link | Linked Record (Requests) | M-BOOKING-CREATION | R/W | Source request |
| Client_Link | Linked Record (Clients) | ALL | R | Client context |
| Yacht_Link | Linked Record (Yachts) | M-BOOKING-CREATION, M-CHARTER-BRIEF | R | Vessel |
| Package_Link | Linked Record (Packages) | M-BOOKING-CREATION, M-CHARTER-BRIEF | R | Package |

**CRITICAL CIRCULAR TRIGGER WARNING:**
Airtable native automations on this table must NOT use "any field updated" trigger. They must use specific field triggers. Will must audit all native automations before any Make scenario writes to this table.

**Trigger Fields Used by Make Webhooks:**
- `Status` → AVAILABILITY_CONFIRMED: triggers M-BOOKING-CREATION
- `Status` → DEPOSIT_PAID: triggers M-YACHT-AVAILABILITY-LOCK + M-CONCIERGE-ASSIGNMENT
- `Status` → CONFIRMED: triggers M-BOOKING-CONFIRMATION + M-CHARTER-BRIEF
- `Status` → COMPLETED: triggers M-LTV-ENGINE + M-SYNTER-SYNC
- `Charter_Brief_Sent` → true: triggers M-VENDOR-NOTIFICATIONS
- `Emergency_Flag` → true: triggers M-ESCALATION-ROUTER (L4 path)

---

## TABLE: CLIENTS (tblr84vRIWC5HmKvo)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Name | Single Line Text | M-LEAD-INTAKE, M-BOOKING-CONFIRMATION | R/W | Full name |
| Email | Email | ALL outbound | R | Primary contact |
| Phone | Phone | ALL SMS | R | Mobile |
| HV_Client | Checkbox | M-LTV-ENGINE, M-BOOKING-CONFIRMATION | R/W | High-value flag |
| Total_Bookings_Completed | Number [TO ADD] | M-LTV-ENGINE | W | Count of completed charters |
| Total_Revenue_LTV | Currency [TO ADD] | M-LTV-ENGINE | W | Lifetime revenue |
| Avg_Charter_Value | Currency [TO ADD] | M-LTV-ENGINE | W | Average booking value |
| Last_Charter_Date | Date [TO ADD] | M-LTV-ENGINE | W | Most recent charter date |
| LTV_Updated_At | DateTime [TO ADD] | M-LTV-ENGINE | W | Last LTV calculation |
| Brand | Single Select | M-LEAD-INTAKE | W | SSS / ME |
| Source_System | Single Select | M-LEAD-INTAKE | W | Make |
| Environment | Single Select | ALL | R/W | Production / Sandbox |
| Created_At | DateTime | M-LEAD-INTAKE | W | Client record creation |
| UUID | Formula (RECORD_ID()) | ALL | R | Permanent immutable ID |

---

## TABLE: YACHTS (tblvyZk1SorIQ6KWF)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Vessel_Name | Single Line Text | M-BOOKING-CONFIRMATION, M-CHARTER-BRIEF | R | Display name |
| Marina | Single Line Text | M-CHARTER-BRIEF | R | Boarding location |
| Slip_Number | Single Line Text | M-CHARTER-BRIEF | R | Specific slip |
| Standard_Crew_Notes | Long Text | M-CHARTER-BRIEF | R | Standard crew instructions |

---

## TABLE: PACKAGES (tblwDw2hkKW5moSr9)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Package_Name | Single Line Text | M-BOOKING-CREATION, M-CHARTER-BRIEF | R | Display name |
| Price | Currency | M-BOOKING-CREATION | R | Full package price |
| Margin_Floor_Pct | Percent [TO ADD] | M-REVENUE-HEALTH | R | Min acceptable margin |
| F&B_Standard | Long Text [TO ADD] | M-CHARTER-BRIEF | R | Standard F&B instructions |
| Includes_Formatted | Long Text [TO ADD] | M-CHARTER-BRIEF | R | AI-readable includes list |
| Live | Checkbox [TO ADD] | M-BOOKING-CREATION | R | Must be true to use package |
| Brand | Single Select [TO ADD] | M-BRAND-ROUTER, M-PRICING-INTELLIGENCE | R | SSS / ME |
| City | Single Select [TO ADD] | M-BOOKING-CREATION | R | City-specific pricing |
| Duration | Single Line Text | M-CHARTER-BRIEF | R | Charter duration |
| Add_Ons_Matrix | Long Text [TO ADD] | M-CHARTER-BRIEF | R | Add-on options and prices |

---

## TABLE: YACHT_AVAILABILITY (new table — replace tblDOoV4CHh8t4qpj)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Yacht | Linked Record (Yachts) | M-YACHT-AVAILABILITY-LOCK, M-DOUBLE-BOOKING-CHECK | R/W | Vessel |
| Date | Date | M-YACHT-AVAILABILITY-LOCK, M-DOUBLE-BOOKING-CHECK | R/W | Charter date |
| Status | Single Select | M-YACHT-AVAILABILITY-LOCK | R/W | AVAILABLE / BOOKED / BLOCKED / MAINTENANCE |
| Booking_ID | Single Line Text | M-YACHT-AVAILABILITY-LOCK | W | Booking that locked this date |
| Locked_At | DateTime | M-YACHT-AVAILABILITY-LOCK | W | Lock timestamp |
| Locked_By | Single Line Text | M-YACHT-AVAILABILITY-LOCK | W | Scenario ID that locked |

---

## TABLE: CONCIERGE_OPERATORS (migrate from app2FbmVD44BXShyx)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Name | Single Line Text | M-CONCIERGE-ASSIGNMENT | R | Operator name |
| Email | Email | M-CONCIERGE-ASSIGNMENT | R | Contact email |
| Slack_User_ID | Single Line Text | M-CONCIERGE-ASSIGNMENT | R | For Slack DM routing |
| City | Linked Record (Cities) | M-CONCIERGE-ASSIGNMENT | R | Assigned city |
| Status | Single Select | M-CONCIERGE-ASSIGNMENT | R | ACTIVE / INACTIVE |

---

## TABLE: VENDORS (tbl4xD1mKhf0QL9Fe)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Name | Single Line Text | M-VENDOR-NOTIFICATIONS | R | Vendor business name |
| Email | Email | M-VENDOR-NOTIFICATIONS | R | Contact email |
| Service_Type | Single Select | M-VENDOR-NOTIFICATIONS | R | Catering / Decor / Captain / Other |
| Vendor_Notes | Long Text | M-VENDOR-NOTIFICATIONS | R | Vendor-specific instructions |
| Vendor_Notified | Checkbox | M-VENDOR-NOTIFICATIONS | W | Notification sent flag |
| Vendor_Notified_At | DateTime | M-VENDOR-NOTIFICATIONS | W | When notified |
| City | Single Select | M-VENDOR-NOTIFICATIONS | R | Vendor's city |

---

## TABLE: CITIES (tblzqHlzECDvJ8KRH)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| City_ID | Single Line Text | M-CITY-HEALTH, M-CITY-LAUNCH | R | CITY-XXX format |
| City_Name | Single Line Text | ALL | R | Display name |
| Active | Checkbox | M-CITY-LAUNCH | R | Will-only modification |
| Tax_Rate | Percent | M-SYNTER-SYNC | R | Local tax rate |
| City_Status | Single Select | M-CITY-HEALTH | R/W | NORMAL / PROBATION / SUSPENDED |
| City_Health_Score | Number | M-CITY-HEALTH | W | 0-100 calculated score |
| Health_Score_Updated_At | DateTime [TO ADD] | M-CITY-HEALTH | W | Timestamp |
| City_Manager | Linked Record (Concierge_Operators) | M-CONCIERGE-ASSIGNMENT | R | Assigned operator |

---

## TABLE: AUDIT_LOG (tblrMpTfMk8q1eNHp)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Log_ID | Formula | — | R | AUD-YYYY-NNNN |
| Timestamp | DateTime | ALL | W | UTC — written by Make |
| Triggering_Event | Long Text | ALL | W | Event description |
| Source_Data | Long Text | ALL | W | Fields read |
| Output | Long Text | ALL | W | What was done/sent |
| Approval_State | Single Select | ALL | W | AUTONOMOUS / PENDING_HUMAN / HUMAN_APPROVED / HUMAN_REJECTED |
| Brand | Single Select | ALL | W | SSS / ME |
| City | Single Select | ALL | W | Market context |
| Environment | Single Select | ALL | W | Always Production in production |
| Prompt_Version | Single Line Text [TO ADD] | AI scenarios | W | AI_Prompt_Versions record ID |
| AI_Confidence_Score | Number [TO ADD] | AI scenarios | W | Model confidence |
| Reviewed_By | Single Line Text [TO ADD] | Tier B scenarios | W | Human reviewer |
| Rollback_Linkage | Single Line Text [TO ADD] | ALL | W | Record ID + reversal action |

**CRITICAL: Audit_Log records are NEVER deleted and NEVER edited. Write-only after creation.**

---

## TABLE: AI_PROMPT_VERSIONS (new — replaces tbl0FJkA1E6a70cxX)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Prompt_Version_ID | Formula | ALL AI scenarios | R | AIV-NNNN |
| Status | Single Select | ALL AI scenarios | R | DRAFT / TESTING / LIVE / DEPRECATED |
| Will_Approved | Checkbox | ALL AI scenarios | R | Must be true before use |
| Make_Variable_Name | Single Line Text | ALL AI scenarios | R | Match exactly in Make filter |
| Content | Long Text | ALL AI scenarios | R | Full prompt text |
| Brand | Single Select | ALL AI scenarios | R | SSS / ME / BOTH |
| Deployed_At | DateTime | — | R | Immutable |
| Rollback_To_Version | Single Line Text | ROLLBACK-PROMPT-001 | R | Prior version ID |

**Make Filter Pattern:** `{Status} = "LIVE" AND {Will_Approved} = TRUE AND {Make_Variable_Name} = "{{variable_name}}"`

---

## TABLE: FOUNDER_DECISIONS (tblFCE26qDwfp4Jwd)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Request_Title | Single Line Text | M-ESCALATION-ROUTER, M-CHARTER-BRIEF | W | Concise title |
| Request_Type | Single Select | M-ESCALATION-ROUTER | W | EMERGENCY / FINANCIAL / BOOKING / SYSTEM |
| Urgency | Single Select | M-ESCALATION-ROUTER | W | IMMEDIATE / SAME_DAY / THIS_WEEK / WHEN_AVAILABLE |
| Context | Long Text | ALL | W | Full context for Will |
| Proposed_Action | Long Text | ALL | W | What Make/AI is recommending |
| Decision | Single Select | M-AUTOMATION-HEALTH | R | APPROVED / DENIED / DEFERRED |
| Submitted_By | Single Line Text | ALL | W | Scenario ID that created it |
| Created_At | DateTime | ALL | W | Timestamp |

---

## TABLE: P&L PER CHARTER (tblFLiODVbQENbL5U — SSS Financials base apprDKQtV2GInThwE)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Booking_ID | Single Line Text | M-SYNTER-SYNC | R/W | Text field — no linked record cross-base |
| Charter_Date | Date | M-SYNTER-SYNC | W | — |
| Brand | Single Line Text | M-SYNTER-SYNC | W | — |
| City | Single Line Text | M-SYNTER-SYNC | W | — |
| Gross_Revenue | Currency | M-SYNTER-SYNC | W | — |
| Net_Revenue | Currency | M-SYNTER-SYNC | W | — |
| Total_Cost | Currency | M-SYNTER-SYNC | W | — |
| Net_Profit | Currency | M-SYNTER-SYNC | W | — |
| Net_Margin_Pct | Percent | M-SYNTER-SYNC | W | — |
| Vessel_Cost | Currency | M-SYNTER-SYNC | W | — |
| Labor_Cost | Currency | M-SYNTER-SYNC | W | — |
| FB_Cost | Currency | M-SYNTER-SYNC | W | — |
| Tax_Collected | Currency | M-SYNTER-SYNC | W | — |
| CM_Payout | Currency | M-SYNTER-SYNC | W | — |
| Referral_Commission | Currency | M-SYNTER-SYNC | W | — |
| Last_Sync_Timestamp | DateTime [TO ADD] | M-SYNTER-SYNC | W | Last sync from Make |
| Sync_Status | Single Select [TO ADD] | M-SYNTER-SYNC | W | SYNCED / FAILED / PENDING |

---

## TABLE: ORGANIC_CONTENT (tbl09BGFacWim5Rk7)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Platform | Single Select | M-CREATIVE-INTELLIGENCE | R | TikTok / Instagram / Both |
| Content_Type | Single Select | M-CREATIVE-INTELLIGENCE | R | Hook Video / Testimonial / BTS / Event |
| Hook_Classification | Single Select | M-CREATIVE-INTELLIGENCE | R | Curiosity / Social Proof / Transformation / Emotion / Authority |
| Emotional_Classification | Single Select | M-CREATIVE-INTELLIGENCE | R | Joy / Desire / FOMO / Aspiration / Comfort / Belonging |
| Performance_Score | Number | M-CREATIVE-INTELLIGENCE | R | Composite score |
| Hook_Strength | Single Select | M-CREATIVE-INTELLIGENCE | R | A / B / C / D |
| Brand | Single Select | M-CREATIVE-INTELLIGENCE | R | SSS / ME |
| Published_Date | Date | M-CREATIVE-INTELLIGENCE | R | Actual publish date |

---

## TABLE: PAID_ADS (tblVsxlNdP9xHDipE)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Ad_Name | Single Line Text | M-CREATIVE-FATIGUE, M-CREATIVE-INTELLIGENCE | R | Identifier |
| Platform | Single Select | M-CREATIVE-INTELLIGENCE | R | Meta / TikTok / Google |
| Status | Single Select | M-CREATIVE-FATIGUE | R | ACTIVE / PAUSED / COMPLETED |
| CPL | Currency | M-CREATIVE-FATIGUE, M-CREATIVE-INTELLIGENCE | R | Cost per lead |
| ROAS | Number | M-CREATIVE-FATIGUE, M-CREATIVE-INTELLIGENCE | R | Return on ad spend |
| Bookings_Attributed | Number | M-CREATIVE-INTELLIGENCE | R | Confirmed bookings from ad |
| Spent | Currency | M-CREATIVE-INTELLIGENCE | R | Actual spend |
| Budget | Currency | M-REVENUE-HEALTH | R | Approved monthly cap |
| Brand | Single Select | M-CREATIVE-INTELLIGENCE | R | SSS / ME |
| Fatigue_Flag | Checkbox [TO ADD] | M-CREATIVE-FATIGUE | W | Fatigue detected |
| Fatigue_Detected_At | DateTime [TO ADD] | M-CREATIVE-FATIGUE | W | Detection timestamp |

---

## TABLE: AUTOMATION_HEALTH (new — create per Airtable build spec)

| Field Name | Type | Used By Scenario | Read/Write | Notes |
|-----------|------|-----------------|-----------|-------|
| Check_Timestamp | DateTime | M-AUTOMATION-HEALTH | W | When check ran |
| Anomaly_Type | Single Select | M-AUTOMATION-HEALTH | W | STALE_AUTOMATION / MISSING_BRIEF / UNSYNCED_PL / HEALTH_GAP |
| Booking_ID | Single Line Text | M-AUTOMATION-HEALTH | W | Affected booking if applicable |
| SEV_Level | Single Select | M-AUTOMATION-HEALTH | W | SEV-1 / SEV-2 / SEV-3 / SEV-4 |
| Alert_Sent | Checkbox | M-AUTOMATION-HEALTH | W | Whether Slack alert was sent |
| Resolved | Checkbox | M-AUTOMATION-HEALTH | W | Human-marked resolution |
| Environment | Single Select | M-AUTOMATION-HEALTH | W | Always Production |

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*AIRTABLE_FIELD_MAPPING_REGISTRY v1.0*
*Effective May 2026*
