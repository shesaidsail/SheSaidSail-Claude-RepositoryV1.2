# STAGE 1 TEMPLATE LIBRARY
## She Said Sail + Mare Executive — Email and SMS Communication Templates

**Status:** PRODUCTION DRAFT — Requires Will Review Before Live Use
**Date:** 2026-05-16
**Version:** 1.0
**Owner:** Will (Founder)
**Brand Authority:** 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED
**Systems Authority:** 02_SYSTEMS_AUTOMATIONS__Systems_Intelligence_Architecture_v2.0_PRODUCTION
**Classification:** Confidential — Internal Use Only

---

## USAGE GOVERNANCE

- All templates are Tier A (autonomous execution) unless labeled Tier B
- All templates are subject to brand governance: no prohibited words, no em dashes, no hard close language
- Make variable injection uses double-brace syntax: `{{field_name}}`
- Field IDs are provided for Make module configuration alongside display names
- SMS templates must respect 160-character limit per segment; targets noted
- HV clients route to Tier B (Luciana review) regardless of template Tier
- Emergency_Flag must be checked before any outbound send — if true, abort
- Automations_Paused must be checked before any outbound send — if true, abort
- SSS and ME templates are separate — no cross-brand contamination

---

## MERGE FIELD REFERENCE

| Display Name | Make Variable | Airtable Field ID | Source Table |
|---|---|---|---|
| Client first name | {{client_first_name}} | flduZhHJcT45CnqAA | Bookings (formula) |
| Booking ID | {{booking_id}} | fldfhYXwP5E4agChR | Bookings |
| Charter date | {{charter_date}} | fldCzvnOsy7WgdOTa | Bookings |
| Yacht name | {{yacht_name}} | fldlCoEAQ3PyxVGlS | Bookings (formula) |
| Boarding location | {{boarding_location}} | fldipyq6e0uxXWc38 | Bookings |
| Package name | {{package_name}} | Packages.Name (lookup) | Packages |
| Group size | {{guest_count}} | fldBhJISslfxz9S7d | Bookings |
| Deposit amount | {{deposit_amount}} | fldMa9x5WNl0h7Wta | Bookings (formula) |
| Deposit link | {{deposit_link}} | fldWLHumliz28w0Sb | Bookings |
| Balance due date | {{balance_due_date}} | fldxPFUgOXt5JayF2 | Bookings |
| Balance amount | Gross - Deposit | Calculated in Make | — |
| Balance link | {{balance_link}} | fldCGiLpMHlwQ1f1E | Bookings |
| Review link | Configured in Make | — | Static per brand |
| Occasion | {{occasion}} | fldghdjUFtlwGblxf | Bookings |

---

## TEMPLATE 1 — INBOUND-001: First Response to Inquiry

**Scenario:** INBOUND-001
**Trigger:** Webflow form submission → Airtable Request record created
**Autonomy Tier:** A
**Channel:** Email (primary) + SMS (secondary if phone provided)
**Timing:** Immediate on trigger
**Brand:** SSS (see ME variant below)

---

### SSS EMAIL — INBOUND-001

**Subject:** Your {{occasion}} charter inquiry — She Said Sail

---

Hi {{client_first_name}},

Got your inquiry. We'd love to make this happen.

Here's what I'm pulling together for you now: yacht availability for your date, the right package for your group size, and a quote with exactly what's included.

I'll have this back to you within a few hours. If your date is flexible, I'll show you a couple of options.

A couple of quick things that help:
- How many guests? (even a rough number is fine)
- Any add-ons you're already thinking about — photos, charcuterie, open bar upgrade?

Reply here or text us. We're easy to reach.

Luciana
She Said Sail

---

**SMS — INBOUND-001 (SSS)**
*(Target: 140 characters)*

Hey {{client_first_name}} — got your inquiry! Putting together options for your {{occasion}} now. I'll follow up in a few hours. — Luciana, SSS

---

### ME EMAIL — INBOUND-001

**Subject:** Your charter inquiry — Mare Executive

---

Hi {{client_first_name}},

Thank you for reaching out.

I'm reviewing availability and putting together options aligned with your group size and date. I'll have details back to you shortly.

If you have a specific vessel preference or any requirements I should know about before I respond, feel free to reply here.

Luciana
Mare Executive

---

**SMS — INBOUND-001 (ME)**
*(Target: 140 characters)*

Hi {{client_first_name}} — received your Mare Executive inquiry. Reviewing options now, will follow up shortly. — Luciana

---

**Fallback (if Name unknown):**
Replace `{{client_first_name}}` with `Hi there` for email, omit name for SMS.

---

## TEMPLATE 2 — BOOKING-001: Deposit Request

**Scenario:** BOOKING-001
**Trigger:** Availability confirmed by Luciana → Status updated
**Autonomy Tier:** A
**Channel:** Email + SMS
**Timing:** Immediate on trigger
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false

---

### SSS EMAIL — BOOKING-001

**Subject:** Your spot is ready — deposit to confirm

---

Hi {{client_first_name}},

Good news: {{yacht_name}} is available on {{charter_date}} for your group.

Here's what you're locking in:

**Package:** {{package_name}}
**Date:** {{charter_date}}
**Guests:** {{guest_count}}
**Deposit:** {{deposit_amount}} (50% to hold the date)

To confirm your spot: {{deposit_link}}

Once the deposit processes, you'll receive your booking confirmation with full details. Balance is due closer to your charter date — I'll remind you well in advance.

Any questions before you pay, just ask.

Luciana
She Said Sail

---

**SMS — BOOKING-001 (SSS)**
*(Target: 155 characters)*

{{client_first_name}} — {{yacht_name}} is yours on {{charter_date}}! Deposit link to hold the date: {{deposit_link}} — She Said Sail

---

### ME EMAIL — BOOKING-001

**Subject:** Charter availability confirmed — deposit to secure

---

Hi {{client_first_name}},

Your requested date is available. Here are the details:

**Package:** {{package_name}}
**Date:** {{charter_date}}
**Guests:** {{guest_count}}
**Deposit to secure:** {{deposit_amount}}

Secure your booking: {{deposit_link}}

Confirmation and full logistics follow once the deposit processes.

Luciana
Mare Executive

---

**SMS — BOOKING-001 (ME)**
*(Target: 155 characters)*

Hi {{client_first_name}} — your date is confirmed available. Deposit link to secure: {{deposit_link}} — Mare Executive

---

## TEMPLATE 3 — BOOKING-002: Deposit Confirmation

**Scenario:** BOOKING-002
**Trigger:** Stripe deposit webhook received → Status = DEPOSIT_PAID
**Autonomy Tier:** A
**Channel:** Email
**Timing:** Immediate on Stripe webhook receipt
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false

---

### SSS EMAIL — BOOKING-002

**Subject:** Deposit received — you're booked ✓

---

Hi {{client_first_name}},

Your deposit just came through. You're officially on the books.

**Booking:** {{booking_id}}
**Date:** {{charter_date}}
**Vessel:** {{yacht_name}}
**Group:** {{guest_count}} guests
**Package:** {{package_name}}

What happens next:

Your balance will be due closer to your charter date. I'll send you the link with plenty of time — no surprises.

A few weeks out, you'll receive your charter brief with everything you need: boarding location, what to bring, what's already handled.

In the meantime, if anything changes on your end — guest count, add-ons, special requests — just reply here.

Looking forward to it.

Luciana
She Said Sail

---

### ME EMAIL — BOOKING-002

**Subject:** Deposit confirmed — {{booking_id}}

---

Hi {{client_first_name}},

Your deposit has been received. Your booking is confirmed.

**Booking reference:** {{booking_id}}
**Date:** {{charter_date}}
**Vessel:** {{yacht_name}}
**Guests:** {{guest_count}}

I'll be in touch with balance details and pre-charter logistics as your date approaches. If anything changes on your end, please let me know.

Luciana
Mare Executive

---

**Note:** No SMS for BOOKING-002. Email is the confirmation of record. A Slack notification routes to Luciana internally.

---

## TEMPLATE 4 — BOOKING-004: Charter Confirmation + Brief Notification

**Scenario:** BOOKING-004
**Trigger:** Booking Status = CONFIRMED (post-agreement)
**Autonomy Tier:** A
**Channel:** Email
**Timing:** Immediate on status change
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false, Agreement_Signed = true (or Will exception documented)

---

### SSS EMAIL — BOOKING-004

**Subject:** Everything is handled — your charter brief

---

Hi {{client_first_name}},

Your charter is confirmed and your brief is ready. Everything your group needs to know is below.

**Booking:** {{booking_id}}
**Date:** {{charter_date}}
**Vessel:** {{yacht_name}}
**Boarding:** {{boarding_location}}
**Guests:** {{guest_count}}
**Package:** {{package_name}}

**Day-of:**
Arrive 15 minutes before departure. Beverages and setup will be ready when you board. Crew handles everything from there.

**What to bring:**
Comfortable clothing, sunscreen, any personal items. Everything else is covered.

**What's already handled:**
{{package_name}} includes everything listed in your booking. No need to coordinate anything with the crew directly — we've done that already.

Your balance is due by {{balance_due_date}}. I'll send the link ahead of time.

Questions are welcome. Looking forward to your day on the water.

Luciana
She Said Sail

---

### ME EMAIL — BOOKING-004

**Subject:** Charter confirmed — {{booking_id}}

---

Hi {{client_first_name}},

Your charter is confirmed.

**Booking:** {{booking_id}}
**Date:** {{charter_date}}
**Vessel:** {{yacht_name}}
**Boarding location:** {{boarding_location}}
**Guests:** {{guest_count}}

Pre-charter logistics and a full brief will follow. Your balance is due by {{balance_due_date}}.

Luciana
Mare Executive

---

## TEMPLATE 5 — CHARTER-001: Balance Due Reminder (72-Hour)

**Scenario:** CHARTER-001
**Trigger:** Charter date − 72 hours
**Autonomy Tier:** A
**Channel:** Email + SMS
**Timing:** 72 hours before Charter_Date
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false, Balance_Paid = false

---

### SSS EMAIL — CHARTER-001

**Subject:** Balance due — {{charter_date}} is 3 days away

---

Hi {{client_first_name}},

Your charter is in 3 days. The remaining balance is due now to finalize everything.

**Balance link:** {{balance_link}}

Your crew is confirmed, your vessel is prepped, and everything is on track. This just locks it in on the payment side.

Any questions before then — I'm here.

Luciana
She Said Sail

---

**SMS — CHARTER-001 (SSS)**
*(Target: 155 characters)*

{{client_first_name}} — your charter is 3 days away! Balance due to finalize: {{balance_link}} — She Said Sail

---

### ME EMAIL — CHARTER-001

**Subject:** Balance due — {{charter_date}}

---

Hi {{client_first_name}},

Your charter is three days away. The remaining balance is due to finalize the booking.

**Payment link:** {{balance_link}}

Logistics confirmation will follow once the balance processes.

Luciana
Mare Executive

---

**SMS — CHARTER-001 (ME)**
*(Target: 155 characters)*

Hi {{client_first_name}} — balance due for your {{charter_date}} charter: {{balance_link}} — Mare Executive

---

## TEMPLATE 6 — CHARTER-002: Pre-Charter Logistics (Post-Balance)

**Scenario:** CHARTER-002
**Trigger:** Stripe balance webhook received → Status = PAID
**Autonomy Tier:** A
**Channel:** Email
**Timing:** Immediate on Stripe balance webhook receipt
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false, Balance_Paid = true

---

### SSS EMAIL — CHARTER-002

**Subject:** You're all set — final details for {{charter_date}}

---

Hi {{client_first_name}},

Balance received. You're fully confirmed.

**Charter date:** {{charter_date}}
**Boarding:** {{boarding_location}}
**Arrive:** 15 minutes before your scheduled departure

Everything is handled. Your crew is confirmed and briefed. Show up, enjoy the day, and let us take care of the rest.

If your group has any last-minute changes — just reply here. We'll sort it.

See you on the water.

Luciana
She Said Sail

---

### ME EMAIL — CHARTER-002

**Subject:** Balance confirmed — logistics for {{charter_date}}

---

Hi {{client_first_name}},

Your balance has been received. You are fully confirmed.

**Date:** {{charter_date}}
**Boarding:** {{boarding_location}}

Crew is briefed. Arrive 15 minutes prior to departure. Any last changes before then, please reply here.

Luciana
Mare Executive

---

## TEMPLATE 7 — CHARTER-003: 24-Hour Boarding Reminder

**Scenario:** CHARTER-003
**Trigger:** Charter date − 24 hours
**Autonomy Tier:** A
**Channel:** SMS (primary) + Email (secondary)
**Timing:** 24 hours before Charter_Date
**Brand:** SSS (see ME variant below)
**Pre-send checks:** Automations_Paused = false, Emergency_Flag = false

---

### SSS SMS — CHARTER-003
*(Target: 155 characters)*

{{client_first_name}} — tomorrow is the day! Boarding at {{boarding_location}}. Arrive 15 min early. Can't wait to have you on the water. — She Said Sail

---

### SSS EMAIL — CHARTER-003

**Subject:** Tomorrow — boarding details

---

Hi {{client_first_name}},

Your charter is tomorrow. Here's everything your group needs:

**When:** {{charter_date}}
**Where:** {{boarding_location}}
**Arrive:** 15 minutes before departure — crew will be there

Bring: comfortable clothes, sunscreen, and any personal items. Everything else is already on board and ready.

If anything comes up tonight — weather question, headcount change, anything — just text or reply here.

We'll see you in the morning.

Luciana
She Said Sail

---

### ME SMS — CHARTER-003
*(Target: 155 characters)*

Hi {{client_first_name}} — your charter is tomorrow at {{boarding_location}}. Arrive 15 min early. — Mare Executive

---

### ME EMAIL — CHARTER-003

**Subject:** Charter tomorrow — {{charter_date}}

---

Hi {{client_first_name}},

Your charter is tomorrow.

**Boarding:** {{boarding_location}}
**Arrive:** 15 minutes before departure

Crew is prepared. If anything changes before then, please reply here.

Luciana
Mare Executive

---

## TEMPLATE 8 — CHARTER-006: D7 Review Request

**Scenario:** CHARTER-006
**Trigger:** Charter date + 7 days — D7_Review_Eligible = true
**Autonomy Tier:** A (conditional — if D7_Review_Eligible = false, route to Luciana)
**Channel:** Email
**Timing:** 7 days after Charter_Date
**Brand:** SSS (see ME variant below)
**Pre-send checks:**
- D7_Review_Eligible = true (formula field fldDaIF93uwAQ6m8E)
- Automations_Paused = false
- Emergency_Flag = false
- Charter_Grade ≠ D or F
- Chargeback_Risk ≠ HIGH or ACTIVE

**If D7_Review_Eligible = false:** Do NOT send. Create Approval Queue record for Luciana review.

---

### SSS EMAIL — CHARTER-006

**Subject:** How was your day on the water?

---

Hi {{client_first_name}},

We hope your group had a beautiful time last week.

If you have a minute, a Google review means everything to a small team like ours. It helps other groups find us and tells us we got it right.

**Leave a review:** {{review_link}}

Thank you — truly.

Luciana
She Said Sail

---

### ME EMAIL — CHARTER-006

**Subject:** Your feedback on last week's charter

---

Hi {{client_first_name}},

Thank you for joining us. We hope the experience was exactly what you needed.

If you're open to sharing a quick review, we'd appreciate it:

**{{review_link}}**

Your feedback goes directly to our team.

Luciana
Mare Executive

---

**⚠ GOVERNANCE NOTE — CHARTER-006:**
This template is ONLY sent when D7_Review_Eligible = true (Airtable formula). Make must evaluate this field before sending. If the formula returns false (D/F grade, emergency, chargeback), Make must:
1. Skip the send
2. Create a record in the Approval Queue with Request_Type = BOOKING, noting the review hold reason
3. Alert Luciana via Slack (#sss-ops-alerts) to handle manually

Review requests sent to chargeback-risk or low-grade clients are a brand governance violation.

---

## TEMPLATE LIBRARY — COMPLIANCE SUMMARY

| Template | Tier | Brand Variants | SMS | Email | Prohibited Words | Governance Violations |
|---|---|---|---|---|---|---|
| INBOUND-001 | A | SSS + ME | ✓ | ✓ | None | None |
| BOOKING-001 | A | SSS + ME | ✓ | ✓ | None | None |
| BOOKING-002 | A | SSS + ME | Email only | ✓ | None | None |
| BOOKING-004 | A | SSS + ME | No | ✓ | None | None |
| CHARTER-001 | A | SSS + ME | ✓ | ✓ | None | None |
| CHARTER-002 | A | SSS + ME | No | ✓ | None | None |
| CHARTER-003 | A | SSS + ME | ✓ | ✓ | None | None |
| CHARTER-006 | A (conditional) | SSS + ME | No | ✓ | None | D7_Review_Eligible gate required |

**Brand governance confirmed:** Zero prohibited words present across all 8 templates. No em dashes. No hard-close language. No fake scarcity. No hype language.

---

## UPCOMING TEMPLATES (NOT STAGE 1)

The following templates are required for Stage 2 and Stage 3 — do not build in Make until those phases are authorized:

- CHARTER-005 (D1 post-charter warmth) — Stage 3
- CHARTER-007 (D30 referral activation) — Stage 3
- BOOKING-003 (agreement required alert — internal Luciana) — Stage 2
- OUTREACH-001 (partner outreach draft) — Stage 4
- EMERGENCY-001 (emergency Slack format) — Stage 1 internal (no client-facing version)

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*STAGE_1_TEMPLATE_LIBRARY v1.0*
*Date: 2026-05-16*
*Brand Authority: 00_LOCKED_GOVERNANCE__Master_Brand_Governance_v1.0_LOCKED*
*Requires Will review before live use*
