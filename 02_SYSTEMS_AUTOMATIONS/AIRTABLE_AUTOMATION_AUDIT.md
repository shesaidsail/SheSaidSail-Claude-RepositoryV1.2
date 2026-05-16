# AIRTABLE_AUTOMATION_AUDIT.md
## She Said Sail + Mare Executive — Airtable Native Automation Audit

**Phase:** Final Pre-Make Cleanup  
**Execution Date:** 2026-05-16  
**Base Audited:** appdZ49WqgjRXxA1R (SSS Operations)  
**Status:** COMPLETE  
**Classification:** Confidential — Internal Use Only

---

## IMPORTANT SCOPE NOTE

Airtable native automation configurations are not accessible via the Metadata API. This audit documents the known automation landscape based on:

1. Field analysis of all tables (which fields are checkboxes, timestamps, and formula triggers)
2. Governance documentation requirements
3. Architecture risk analysis from the Airtable Final Build Spec v2.0
4. Phase 3 and Phase 4 migration records

**Will must verify each classified automation in the Automation tab of appdZ49WqgjRXxA1R before Stage 1 Make implementation begins.**

---

## SECTION 1 — KNOWN/INFERRED AUTOMATION INVENTORY

### 1.1 Bookings Table (tbl72omPibBkn2hZL) — HIGH RISK

The Bookings table contains 151 fields. Any "record updated" trigger on this table fires on every single field write. This is the highest circular-trigger risk surface in the system.

#### AUTOMATION B-01: Booking Status Notification
- **Trigger:** Status field changes to CONFIRMED
- **Action (inferred):** Sends internal notification or updates linked records
- **Classification:** NEEDS_REVIEW
- **Risk:** If Make writes Status=CONFIRMED, this may double-trigger any internal notification
- **Action:** Scope trigger to ONLY fire when field "Status" changes, not generic "record updated"

#### AUTOMATION B-02: Automations_Paused Safety Gate
- **Trigger:** Automations_Paused = true
- **Action (inferred):** Stops outbound messaging sequences
- **Classification:** KEEP
- **Risk:** CRITICAL — must remain active. Make must read this field before every outbound action.
- **Action:** Confirm this automation exists. If it does not, it must be created before Stage 1.

#### AUTOMATION B-03: 24hr Expiration Alert
- **Trigger:** 24hr Expiration formula field computes a past-due value
- **Action (inferred):** Internal alert or Booking status update
- **Classification:** NEEDS_REVIEW
- **Risk:** May conflict with Make's booking expiration scenario
- **Action:** If Make handles INBOUND-001 expiration logic, this automation must be DISABLED to prevent double execution.

#### AUTOMATION B-04: Charter Grade / D7 Review Trigger
- **Trigger:** Charter status reaches COMPLETED + D7_Review_Eligible = TRUE
- **Action (inferred):** Triggers review request workflow
- **Classification:** REPLACE_IN_MAKE
- **Risk:** This is the exact function of CHARTER-006. If both run, clients receive duplicate review requests.
- **Action:** DISABLE before CHARTER-006 is activated in Make.

#### AUTOMATION B-05: Balance Due Alert
- **Trigger:** Balance Due Date formula triggers an alert
- **Action (inferred):** Internal notification
- **Classification:** NEEDS_REVIEW
- **Risk:** Low — internal only, but may conflict with Make's balance payment scenario
- **Action:** Verify whether this fires outbound or internal only.

#### AUTOMATION B-06: Emergency Flag Escalation
- **Trigger:** Emergency_Flag = true
- **Action (inferred):** Alert to Will or Luciana
- **Classification:** KEEP
- **Risk:** Safe to keep — this is a safety alert, not a client-facing trigger.
- **Note:** Ensure it does NOT trigger Make's EMERGENCY-001 to prevent loop.

#### AUTOMATION B-07: Forfeiture Processing
- **Trigger:** Forfeiture_Processed = true OR Refund_Status changes
- **Action (inferred):** Internal notification
- **Classification:** NEEDS_REVIEW
- **Risk:** If Make handles refund workflows, this must be disabled or scoped.

---

### 1.2 Requests Table (tblTlSB9CO4dTGodg) — HIGH RISK

#### AUTOMATION R-01: New Request Notification
- **Trigger:** New record created in Requests
- **Action (inferred):** Notification to Luciana or Will
- **Classification:** KEEP
- **Risk:** If Make's INBOUND-001 creates the Request record, this fires immediately after. Ensure it does not duplicate Make's response chain.
- **Action:** Confirm trigger is "record created" not "record updated." No conflict if scoped correctly.

#### AUTOMATION R-02: Agent Status Escalation Alert
- **Trigger:** Agent_Status changes to ESCALATE_WILL_IMMEDIATE or ESCALATE_LUCIANA
- **Action (inferred):** Notification to Will or Luciana
- **Classification:** KEEP
- **Risk:** Low — this is a safety net. Even if Make also notifies, duplicate human alerts are acceptable for escalations.

#### AUTOMATION R-03: Stale Request Watchdog
- **Trigger:** Time-based, fires if Request record is older than X hours without Booking
- **Action (inferred):** Internal alert
- **Classification:** NEEDS_REVIEW
- **Risk:** May conflict with Make's lead follow-up logic
- **Action:** If Make handles INBOUND-001 follow-up sequences, disable this automation.

---

### 1.3 AI_Prompt_Versions (tbl0FJkA1E6a70cxX) — LOW RISK

#### AUTOMATION AIV-01: LIVE Status Notification
- **Trigger:** Status changes to LIVE
- **Action (inferred):** Notification to Will
- **Classification:** KEEP
- **Risk:** Low — this is a governance alert. Keep active.
- **Note:** Will_Approved must be true before Status can be LIVE per governance.

---

### 1.4 Yacht_Availability (tblDOoV4CHh8t4qpj) — CRITICAL RISK

#### AUTOMATION YA-01: Availability Status Change Alert
- **Trigger:** Status field changes
- **Action (inferred):** Internal notification or Bookings update
- **Classification:** NEEDS_REVIEW
- **Risk:** CRITICAL — if Make writes to Yacht_Availability via M-YACHT-AVAILABILITY-LOCK, and this automation then writes back to Bookings, a circular loop is possible.
- **Action:** Before M-YACHT-AVAILABILITY-LOCK is built, inventory every Airtable automation that reads or writes to this table. Scope any "record updated" trigger to specific fields only.

#### AUTOMATION YA-02: Double Booking Detection
- **Trigger:** New record created where Yacht + Charter Date matches existing CONFIRMED record
- **Action (inferred):** Alert to Will or Luciana
- **Classification:** REPLACE_IN_MAKE
- **Risk:** M-DOUBLE-BOOKING-CHECK (Make scenario) handles this. Running both creates duplicate alerts.
- **Action:** DISABLE once M-DOUBLE-BOOKING-CHECK is live in Make.

---

### 1.5 Partnerships (tble5DcTo8mahr3lp) — LOW RISK

#### AUTOMATION P-01: New Partnership Record Notification
- **Trigger:** New record created
- **Action (inferred):** Internal notification
- **Classification:** KEEP
- **Risk:** Low — no Make dependencies on Partnerships table in Stage 1.

---

### 1.6 Campaigns (tblTs5px03BPrUpG4) — MEDIUM RISK

#### AUTOMATION CAM-01: Campaign Launch Alert
- **Trigger:** Status changes to ACTIVE
- **Action (inferred):** Notification or Paid Ads record creation
- **Classification:** NEEDS_REVIEW
- **Risk:** If M-UTM-CAPTURE reads from Campaigns, confirm this automation does not overwrite fields Make expects to write.

---

### 1.7 Concierge_Operators (tblX61IB2qjDmac8l) — LOW RISK

No complex automations expected. Table contains operator routing records only.

#### AUTOMATION CO-01: Operator Level Change Alert
- **Trigger:** Level field changes
- **Action (inferred):** Notification
- **Classification:** KEEP
- **Risk:** Low — operator routing changes are infrequent and not in Stage 1 Make scope.

---

## SECTION 2 — CLASSIFICATION SUMMARY

| Automation ID | Table | Classification | Priority |
|---|---|---|---|
| B-01 | Bookings | NEEDS_REVIEW | HIGH |
| B-02 | Bookings | KEEP | CRITICAL |
| B-03 | Bookings | NEEDS_REVIEW | HIGH |
| B-04 | Bookings | REPLACE_IN_MAKE | HIGH |
| B-05 | Bookings | NEEDS_REVIEW | MEDIUM |
| B-06 | Bookings | KEEP | HIGH |
| B-07 | Bookings | NEEDS_REVIEW | MEDIUM |
| R-01 | Requests | KEEP | HIGH |
| R-02 | Requests | KEEP | CRITICAL |
| R-03 | Requests | NEEDS_REVIEW | MEDIUM |
| AIV-01 | AI_Prompt_Versions | KEEP | LOW |
| YA-01 | Yacht_Availability | NEEDS_REVIEW | CRITICAL |
| YA-02 | Yacht_Availability | REPLACE_IN_MAKE | HIGH |
| P-01 | Partnerships | KEEP | LOW |
| CAM-01 | Campaigns | NEEDS_REVIEW | MEDIUM |
| CO-01 | Concierge_Operators | KEEP | LOW |

---

## SECTION 3 — CIRCULAR LOOP RISK MATRIX

The following automation chains are dangerous if Make writes to Airtable and Airtable automations write back:

| Risk Scenario | Tables Involved | Resolution |
|---|---|---|
| Make writes Booking Status → Airtable automation triggers → Make re-fires | Bookings | Scope all Airtable triggers to specific field changes, not "record updated" |
| Make writes to Yacht_Availability → Airtable automation writes to Bookings → Make re-fires | Yacht_Availability, Bookings | Inventory and disable YA-01 if it writes to Bookings |
| Make creates Request → Airtable automation fires → Make INBOUND-001 double-processes | Requests | Ensure R-01 only notifies humans, does not write fields Make reads |
| Airtable B-04 sends review → Make CHARTER-006 also sends review | Bookings | DISABLE B-04 before CHARTER-006 activation |

---

## SECTION 4 — REQUIRED ACTIONS BEFORE STAGE 1

| Priority | Action | Owner | Blocking Scenario |
|---|---|---|---|
| CRITICAL | Will audits Automation tab in appdZ49WqgjRXxA1R and documents every active automation | Will | All Make scenarios |
| CRITICAL | Confirm Automations_Paused gate (B-02) exists and is active | Will | All client-facing scenarios |
| HIGH | Scope all Bookings "record updated" triggers to specific field changes | Will | All Bookings Make writes |
| HIGH | Disable B-04 (charter review automation) before CHARTER-006 goes live | Will | CHARTER-006 |
| HIGH | Inventory YA-01 and confirm it does not write to Bookings | Will | M-YACHT-AVAILABILITY-LOCK |
| HIGH | Disable YA-02 when M-DOUBLE-BOOKING-CHECK goes live | Will | M-DOUBLE-BOOKING-CHECK |
| MEDIUM | Disable R-03 if Make handles lead follow-up sequences | Will | INBOUND-001 |

---

## SECTION 5 — AUTOMATIONS MAKE WILL REPLACE

The following Airtable native automations should be disabled once their Make equivalents are live and validated:

| Airtable Automation | Make Equivalent | Disable After |
|---|---|---|
| B-04 (Charter review trigger) | CHARTER-006 | CHARTER-006 validated |
| YA-02 (Double booking alert) | M-DOUBLE-BOOKING-CHECK | M-DOUBLE-BOOKING-CHECK validated |
| B-03 (24hr expiration) | INBOUND-001 | INBOUND-001 validated |
| R-03 (Stale request watchdog) | INBOUND-001 | INBOUND-001 validated |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*AIRTABLE_AUTOMATION_AUDIT.md*  
*Execution Date: 2026-05-16*  
*Phase: Final Pre-Make Cleanup*
