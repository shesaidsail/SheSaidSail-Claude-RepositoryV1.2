# STAGE_2_IMPLEMENTATION_GUIDE

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Stage:** 2 — Operational Automation
**Prerequisite:** Stage 1 fully deployed, tested, and stable in production
**Goal:** Reduce operational load. Add safety nets. Add vendor and captain logistics.
**Classification:** Confidential — Internal Use Only

---

## STAGE 2 OVERVIEW

Stage 2 adds the operational safety layer and logistics automation on top of the Stage 1 revenue core. When Stage 2 is complete:

- Yacht availability is locked the moment a deposit is paid (preventing double bookings)
- Double booking is checked before availability is confirmed
- Failed payments trigger a recovery flow
- Vendors and captains are notified from the charter brief
- Charter briefs are generated automatically at T-14
- Escalations are routed correctly and fast
- Referrals are activated at D30
- Rebooking offers are sent at D60
- Automation health is monitored every 15 minutes

Stage 2 never replaces Stage 1 scenarios. It runs alongside them. All Stage 1 scenarios remain active and unchanged.

---

## SCENARIO 9: M-YACHT-AVAILABILITY-LOCK

**Purpose:** Lock the yacht's availability in the Yacht_Availability table the moment a deposit is paid. Prevents the same vessel being offered to another lead on the same date.

**Trigger:** Airtable webhook — Bookings.Status → DEPOSIT_PAID

**Pre-Checks:**
- Environment = Production
- Emergency_Flag = false

**Module Sequence:**

```
1. Watch: Bookings.Status = DEPOSIT_PAID

2. Airtable > Get Record: Booking (full)
   — Extract: Yacht_Link, Charter_Date, Duration, Booking_ID

3. Airtable > Search Records: Yacht_Availability
   — Filter: Yacht = {{yacht_id}} AND Date = {{charter_date}}
   — If no record found → create one

4. If Yacht_Availability record found:
   — Check: Status = AVAILABLE
   — If Status != AVAILABLE → this is a double booking risk → go to step 5a
   — If Status = AVAILABLE → go to step 5b

5a. DOUBLE BOOKING ALERT:
   — Slack > DM to Will + Luciana: "⚠️ AVAILABILITY CONFLICT — [Yacht] is already [Status] on [Date]. Booking [ID] just confirmed. Immediate review required."
   — Airtable > Create Record: Founder_Decisions (Type = BOOKING, Urgency = IMMEDIATE)
   — EXIT without locking (human must resolve)

5b. NORMAL LOCK:
   — Airtable > Update Record: Yacht_Availability
     Status → BOOKED
     Booking_ID → {{booking_id}}
     Locked_At → {{now}}
     Locked_By → Make_M-YACHT-AVAILABILITY-LOCK

6. Audit_Log entry
```

**Airtable Tables Touched:**
- Bookings (tbl72omPibBkn2hZL): read
- Yacht_Availability: read + update

**Failure Points:**
- Yacht_Availability table not yet created → SEV-1 — Stage 2 cannot deploy without this table
- Race condition: two deposits processed simultaneously → idempotency check on Yacht_Availability.Booking_ID prevents double lock

**Rollback:** If booking is cancelled, update Yacht_Availability.Status → AVAILABLE and clear Booking_ID. Triggers for cancellation rollback are in Stage 2 extended scope.

---

## SCENARIO 10: M-DOUBLE-BOOKING-CHECK

**Purpose:** Check yacht availability before Luciana marks a Request as AVAILABILITY_CONFIRMED. Creates a safety gate before Stage 1's M-BOOKING-CREATION runs.

**Trigger:** Airtable webhook — Requests.Status → AVAILABILITY_CONFIRMED

**Module Sequence:**

```
1. Watch: Requests.Status = AVAILABILITY_CONFIRMED

2. Airtable > Get Record: Request (full)
   — Extract: Yacht_Link, Charter_Date, Duration

3. Airtable > Search Records: Yacht_Availability
   — Filter: Yacht = {{yacht_id}} AND Date = {{charter_date}}
   — Filter: Status != AVAILABLE

4. If conflict found:
   — Airtable > Update Record: Requests
     Status → AVAILABILITY_CONFLICT
   — Slack > DM to Luciana: "⚠️ AVAILABILITY CONFLICT — [Yacht] is [conflict status] on [Date]. Request [ID] rolled back. Please select alternate vessel."
   — EXIT (M-BOOKING-CREATION will not trigger since Status is not AVAILABILITY_CONFIRMED)

5. If no conflict:
   — Log: availability confirmed clean
   — EXIT (M-BOOKING-CREATION proceeds normally from its own trigger)

6. Audit_Log entry
```

**Operational Note:** This scenario runs BEFORE M-BOOKING-CREATION. It uses the same trigger field (Requests.Status → AVAILABILITY_CONFIRMED) but its job is to validate, not create. The order-of-operations risk is managed by making M-BOOKING-CREATION read-check the Yacht_Availability table as well.

**Failure Points:**
- Yacht not linked to Request → alert Luciana: cannot check availability without vessel assignment

---

## SCENARIO 11: M-FAILED-PAYMENT-HANDLER

**Purpose:** Handle Stripe payment failures gracefully. Notify client, alert Luciana, update booking status.

**Trigger:** Stripe webhook — `payment_intent.payment_failed`

**Module Sequence:**

```
1. Webhooks > Custom Webhook (Stripe)
   — Validate Stripe-Signature
   — Extract: payment_intent_id, failure_reason, metadata

2. Airtable > Search Records: Bookings
   — Filter: {Stripe_Payment_Intent_ID} = {{payment_intent_id}} OR
             metadata.request_id matches Request_ID field

3. Read: Emergency_Flag, Automations_Paused, Status

4. Airtable > Update Record: Bookings
   — Payment_Failure_Count → increment by 1
   — Last_Payment_Failure_At → {{now}}
   — Payment_Failure_Reason → {{failure_reason}}

5. DECISION TREE by failure count:

   Failure 1:
   — Gmail > Send email to client: "Your card was declined. Here's your deposit link to try again: [link]"
   — SMS > Send SMS: same message, short version
   — Slack > #sss-ops-bookings: "❌ Payment failed — [Client] — Attempt 1/3 — Reason: [reason]"

   Failure 2:
   — Gmail > Send email: "Second attempt failed. Please call us to complete your booking."
   — Slack > #sss-ops-bookings: "❌ Payment failed — [Client] — Attempt 2/3 — Luciana: please follow up directly"
   — Slack > DM to Luciana: "Second payment failure — [Client] — personal follow-up needed"

   Failure 3+:
   — Gmail > Send email: "We're holding your booking date for 24 hours. Please contact us directly."
   — Airtable > Update Bookings: Status → PAYMENT_FAILED
   — Slack > DM to Luciana + Will: "3rd payment failure — [Client] — Booking at risk. Manual action required."
   — Airtable > Create Record: Founder_Decisions (Type = BOOKING, Urgency = SAME_DAY)

6. Audit_Log entry
```

**Failure Points:**
- Booking not found from Stripe metadata → Luciana DM with raw Stripe data for manual reconciliation
- Client contact info missing → Luciana DM only (no client outreach possible)

---

## SCENARIO 12: M-VENDOR-NOTIFICATIONS

**Purpose:** Notify vendors (catering, decor, captain) when a charter brief has been sent and confirmed.

**Trigger:** Airtable webhook — Bookings.Charter_Brief_Sent → true

**Module Sequence:**

```
1. Watch: Bookings.Charter_Brief_Sent = true

2. Airtable > Get Record: Booking (full)

3. Airtable > Get Linked Records: Vendors (linked to Booking or via Package)
   — Extract each vendor: Name, Email, Phone, Service_Type, Vendor_Notes

4. For each Vendor:
   a. Check: Emergency_Flag on Booking → if true, skip all vendor notifications
   b. Gmail > Send vendor brief email
      — Template: VENDOR_CHARTER_BRIEF
      — Include: charter date, boarding time, client expectations, vendor-specific notes
   c. Airtable > Update: Vendor_Notified = true, Vendor_Notified_At = {{now}}
   d. Wait 2 seconds between vendor sends (rate limiting)

5. Airtable > Update Record: Bookings
   — Charter_Brief_All_Vendors_Confirmed = false (set to true when all acknowledge — manually or via reply webhook)

6. Slack > #sss-ops-bookings: "Vendor notifications sent for [Booking ID] — [charter date]"

7. Audit_Log entry for each vendor notification
```

**Failure Points:**
- Vendor email missing → Luciana DM with vendor name and charter details
- Charter date T-48 and vendors not yet notified → M-AUTOMATION-HEALTH alerts

---

## SCENARIO 13: M-CHARTER-BRIEF

**Purpose:** Generate the Charter Brief document from confirmed Airtable booking data and route for Luciana review before T-14 delivery.

**Trigger:** Airtable webhook — Bookings.Status → CONFIRMED

**Autonomy Tier:** B — Claude generates, Luciana reviews before sending to City Manager

**Module Sequence:**

```
1. Watch: Bookings.Status = CONFIRMED

2. Airtable > Get Record: Booking (full)
   — Check: Charter_Date ≤ today + 21 days? If not → schedule check (BASIC-LIFECYCLE handles T-14 trigger)
   — Check: Agreement_Signed = true (or Will-approved exception in Charter_Notes)
   — Check: Emergency_Flag = false

3. Airtable > Get Linked Records: Client, Yacht, Package, City, Vendors

4. Assemble context payload:
   — Client: Name, Group_Size, Occasion, Add_Ons_Selected, F&B_Notes, Crew_Notes, Emergency_Contact
   — Yacht: Vessel_Name, Marina, Slip_Number, Standard_Crew_Notes
   — Package: Package_Name, Duration, F&B_Standard, Includes_Formatted
   — City: City_Manager_Name, Tax_Rate
   — Booking: Charter_Date, HV_Client, Balance_Paid

5. Check for missing required fields:
   — If any of [Client.Name, Charter_Date, Yacht.Vessel_Name, Group_Size, Package.Package_Name] = empty:
     → Slack DM to Luciana: "Charter Brief blocked — missing [field list]. Please complete before T-14."
     → EXIT

6. HTTP > Claude API call
   — System prompt: Current production version from AI_Prompt_Versions (Will_Approved = true, Status = PRODUCTION, Make_Variable_Name = "CHARTER_BRIEF_SYSTEM")
   — User message: assembled context payload
   — Output: formatted Charter Brief draft

7. Airtable > Create Record or Update: Charter_Brief linked to Booking
   — Store draft text
   — Status = PENDING_LUCIANA_REVIEW

8. Slack > DM to Luciana:
   "📋 Charter Brief draft ready for [Client Name] — [Charter Date]. Review and approve in Airtable. Send at T-48."
   — Include Airtable link

9. Audit_Log entry (Tier B — Approval_State = PENDING_HUMAN)
```

**AI System Prompt Requirements:**
- Prompt version must have Will_Approved = true
- Prompt version must have Status = PRODUCTION
- Prompt version Make_Variable_Name = "CHARTER_BRIEF_SYSTEM"
- If no qualifying prompt found → EXIT + Luciana alert ("Charter Brief AI unavailable — create manually")

**Failure Points:**
- Claude API down → Luciana creates brief manually from Airtable template
- Missing vessel data → Luciana completes manually

---

## SCENARIO 14: M-ESCALATION-ROUTER

**Purpose:** Route escalated requests to the correct human based on escalation type and urgency. Creates Founder Decision records for L3+ situations.

**Trigger:** Airtable webhook — Requests.Agent_Status → ESCALATED

**Module Sequence:**

```
1. Watch: Requests.Agent_Status = ESCALATED

2. Airtable > Get Record: Request (full)
   — Extract: Escalation_Reason, Brand, City, Client_Link, Booking_Link (if any), HV_Client

3. ROUTING LOGIC:

   L4 (Emergency_Flag = true on linked Booking OR escalation_reason contains: "safety", "injury", "media", "legal"):
   — Airtable > Update Bookings: Emergency_Flag = true
   — Airtable > Create Record: Emergency_Escalations
   — Airtable > Create Record: Founder_Decisions (Type = EMERGENCY, Urgency = IMMEDIATE)
   — Slack > Post to #sss-emergency-ops (L4 format per Systems Intelligence Architecture Section 10.3)
   — Slack > DM to Will directly
   — EXIT

   L3 (HV_Client = true OR Financial_Dispute OR Escalation_Reason keywords: "double booking", "vessel issue", "complaint", "refund"):
   — Airtable > Create Record: Founder_Decisions (Type = BOOKING, Urgency = SAME_DAY)
   — Slack > DM to Will + Luciana: "[L3] Escalation — [Client Name] — [Reason] — Action required today"
   — Airtable > Update Requests: Agent_Status = HUMAN_REVIEW

   L2 (All other escalations):
   — Slack > DM to Luciana: "Escalation routed to you — [Client Name] — [Reason]"
   — Airtable > Update Requests: Agent_Status = HUMAN_REVIEW

4. Audit_Log entry
```

**Failure Points:**
- Escalation_Reason field empty → default to L2 routing + flag for Luciana
- Will Slack ID missing → fallback to #sss-emergency-ops channel

---

## SCENARIO 15: M-REFERRAL-ENGINE

**Purpose:** Send referral activation message to clients 30 days after their charter.

**Trigger:** Schedule — daily 7:00 AM (separate from M-BASIC-LIFECYCLE to keep scenarios single-purpose)

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: days_since_charter = 30 (Charter_Date = today - 30)
   — Filter: Status = COMPLETED
   — Filter: D30_Sent = false
   — Filter: Charter_Grade IN [A, B, C]
   — Filter: Emergency_Flag = false
   — Filter: Environment = Production

2. For each Booking:
   a. Check Automations_Paused → skip if true
   b. Get linked Client record
   c. Get linked Affiliates record (if any — for commission tracking)

3. Gmail > Send referral email
   — Template: SSS_REFERRAL_ACTIVATION or ME_REFERRAL_ACTIVATION
   — Include: personalized thank you, referral link/code, commission offer for sharing

4. Airtable > Update Bookings: D30_Sent = true, D30_Sent_At = {{now}}

5. Audit_Log entry
```

**Failure Points:**
- Charter_Grade = D or F → skip silently (unsatisfied clients should not receive referral ask)
- Referral code not generated → send without code; log alert for Luciana to follow up with affiliate setup

---

## SCENARIO 16: M-REBOOKING-ENGINE

**Purpose:** Send a rebooking invitation to clients 60 days after their charter.

**Trigger:** Schedule — daily 7:00 AM

**Module Sequence:**

```
1. Airtable > Search Records: Bookings
   — Filter: days_since_charter = 60
   — Filter: Status = COMPLETED
   — Filter: D60_Sent = false
   — Filter: Charter_Grade IN [A, B]
   — Filter: Emergency_Flag = false
   — Filter: Environment = Production

2. For each Booking:
   a. Check: Client has another confirmed upcoming booking? → skip (already rebooked)
   b. Gmail > Send rebooking email
      — Template: SSS_REBOOKING or ME_REBOOKING
      — Include: callback to their experience, upcoming season availability tease, easy booking CTA

3. Airtable > Update: D60_Sent = true, D60_Sent_At = {{now}}

4. Audit_Log entry
```

---

## SCENARIO 17: M-AUTOMATION-HEALTH

**Purpose:** Monitor automation health every 15 minutes. Alert on failures, gaps, and system anomalies.

**Trigger:** Schedule — every 15 minutes

**Module Sequence:**

```
1. Airtable > Search Records: Automation_Health table
   — Filter: Last_Updated < now - 24 hours AND Status = ACTIVE
   — These are bookings whose automation tracking hasn't been touched in 24 hours

2. Airtable > Search Records: Bookings
   — Filter: Status = CONFIRMED AND Charter_Brief_Sent = false AND Charter_Date <= today + 10
   — These are confirmed bookings within 10 days that haven't had a charter brief sent

3. Airtable > Search Records: Bookings
   — Filter: Status = DEPOSIT_PAID AND days_since_deposit > 48 AND Concierge_Notified_At = null

4. Check: Last successful M-BASIC-LIFECYCLE run
   — If > 25 hours ago → SEV-2 alert

5. Check: Audit_Log for any gap in entries in last 60 minutes during business hours
   — If gap detected → SEV-2 alert

6. FOR EACH ANOMALY FOUND:
   — Airtable > Create Record: Automation_Health (log anomaly)
   — SEV classification:
     < 3 anomalies/hour → SEV-3 (log only)
     3-5 anomalies/hour → SEV-2 (Luciana DM)
     5+ anomalies/hour → SEV-1 (Will DM + Luciana DM + #sss-ops-alerts)

7. If any SEV-1:
   — Slack > Post to #sss-ops-alerts: full anomaly report
   — Slack > DM to Will: "SYSTEM HEALTH ALERT — [count] anomalies detected — [summary]"

8. Audit_Log entry: health check completed, anomaly count, actions taken
```

**Failure Points:**
- M-AUTOMATION-HEALTH itself fails → no self-alert possible. This is a known limitation. Will checks #sss-ops-alerts daily as a backup.

---

## STAGE 2 SUCCESS CRITERIA

Stage 2 is complete when:

- [ ] M-YACHT-AVAILABILITY-LOCK has locked at least one yacht in production without error
- [ ] M-DOUBLE-BOOKING-CHECK tested with synthetic conflict — conflict correctly blocked
- [ ] M-FAILED-PAYMENT-HANDLER tested in Stripe test mode — all three failure escalations fired correctly
- [ ] M-CHARTER-BRIEF generated at least one brief reviewed and approved by Luciana
- [ ] M-ESCALATION-ROUTER tested for L2, L3, and L4 routes — all three routed correctly
- [ ] M-AUTOMATION-HEALTH running every 15 minutes — no false positives in first 48 hours
- [ ] M-REFERRAL-ENGINE and M-REBOOKING-ENGINE tested with sandbox bookings

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_2_IMPLEMENTATION_GUIDE v1.0*
*Effective May 2026*
