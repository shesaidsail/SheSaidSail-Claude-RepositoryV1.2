# DEPLOYMENT GUIDE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Status:** PRODUCTION-READY  
**Owner:** Will (Founder)

---

## OVERVIEW

This guide covers the complete pre-deployment checklist, environment setup, and post-deployment verification for Stage 1.

---

## PRE-DEPLOYMENT CHECKLIST

### A. Airtable Pre-Work

Complete ALL of the following before importing any scenario:

#### She Said Sail Production Base: appdZ49WqgjRXxA1R

**Requests Table (tblTlSB9CO4dTGodg) — verify these fields exist:**
- [ ] First Name (Single line text)
- [ ] Last Name (Single line text)
- [ ] Email (Email)
- [ ] Phone (Phone number)
- [ ] Yacht (Single line text)
- [ ] Experience (Single line text)
- [ ] Duration (Single line text)
- [ ] Preferred Date (Date)
- [ ] Guest Count (Number)
- [ ] Add-Ons Selected (Long text)
- [ ] Occasion (Single line text)
- [ ] Special Requests (Long text)
- [ ] Status (Single select) — values: NEW, AVAILABILITY_CONFIRMED
- [ ] Brand (Single select) — values: SSS, ME, UNKNOWN
- [ ] Environment (Single select) — values: Production, Sandbox
- [ ] Source_System (Single line text)
- [ ] Notes (Long text) — used for idempotency key storage
- [ ] Submission Date (Date or Created time)

**Bookings Table (tbl72omPibBkn2hZL) — verify these fields exist:**
- [ ] Status (Single select) — values: AVAILABILITY_CONFIRMED, DEPOSIT_SENT, DEPOSIT_PAID, CONFIRMED
- [ ] Guest Count (Number)
- [ ] Charter Date (Date)
- [ ] Occasion (Single line text)
- [ ] Boarding Location (Single line text)
- [ ] Charter Notes (Long text)
- [ ] Add-ons (Long text)
- [ ] Brand (Single select) — SSS, ME
- [ ] City (Single line text)
- [ ] Environment (Single select) — Production, Sandbox
- [ ] Source_System (Single line text)
- [ ] Idempotency_Key (Single line text)
- [ ] Automations_Paused (Checkbox) — DEFAULT: unchecked
- [ ] Emergency_Flag (Checkbox) — DEFAULT: unchecked
- [ ] HV Booking (Checkbox) — DEFAULT: unchecked
- [ ] Confirmation_Sent (Checkbox) — **CREATE IF MISSING** — DEFAULT: unchecked
- [ ] Concierge_Assigned (Checkbox) — **CREATE IF MISSING** — DEFAULT: unchecked
- [ ] Concierge_Name (Single line text) — **CREATE IF MISSING**
- [ ] D0 Sent (Checkbox) — DEFAULT: unchecked
- [ ] Last_Automation_Timestamp (Single line text)
- [ ] Booking ID (Formula or Single line text)
- [ ] Client (Link to Clients table)
- [ ] Yacht Name (Single line text)
- [ ] Stripe_Payment_Link_URL (URL) — **CREATE IF MISSING**
- [ ] Stripe_Payment_Link_ID (Single line text) — **CREATE IF MISSING**
- [ ] Stripe_Price_ID (Single line text) — **CREATE IF MISSING**
- [ ] Stripe_Payment_Intent_ID (Single line text) — **CREATE IF MISSING**
- [ ] Deposit_Amount (Number/Currency) — **CREATE IF MISSING**

**Audit Log Table (tblrMpTfMk8q1eNHp) — verify these fields exist:**
- [ ] Timestamp (Date and time)
- [ ] Triggering_Event (Long text)
- [ ] Source_Data (Long text)
- [ ] Output (Long text)
- [ ] Approval_State (Single select) — values: AUTONOMOUS, PENDING_HUMAN, FOUNDER_REQUIRED
- [ ] Reviewed_By (Single line text)
- [ ] Rollback_Linkage (Single line text)
- [ ] Brand (Single select)
- [ ] City (Single line text)
- [ ] Environment (Single select)
- [ ] Model_Version (Single line text)
- [ ] AI_Confidence_Score (Number)
- [ ] Destination (Long text)

**Concierge_Operators Table (tblX61IB2qjDmac8l) — verify these fields exist:**
- [ ] Name (Single line text)
- [ ] Status (Single select) — values: Active, Inactive
- [ ] City (Single line text)
- [ ] Phone (Phone number)
- [ ] Email (Email)

**Clients Table (tblr84vRIWC5HmKvo) — verify these fields exist:**
- [ ] Name (Single line text)
- [ ] Email (Email)
- [ ] Phone (Phone number)

**Populate Concierge_Operators with at least one active record before testing.**

---

### B. Slack Pre-Work

Verify these channels exist in your Slack workspace:
- [ ] `#sss-emergency-ops` — emergency alerts, founder-only
- [ ] `#sss-lead-intake` — new lead notifications
- [ ] `#sss-ops-alerts` — general ops alerts

Connect Slack OAuth to Make before importing scenarios.

---

### C. Credentials Pre-Work

Have these ready before deployment:

| Credential | Where To Find | Used In |
|------------|---------------|---------|
| Airtable PAT | Airtable Account → API → Personal Access Tokens | All scenarios |
| Slack OAuth token | Make integrations → Slack → Connect | M-OPS-LOGGER-ALERTER |
| Gmail OAuth | Make integrations → Gmail → Connect | M-LEAD-INTAKE, M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |
| Stripe TEST secret key (sk_test_...) | Stripe Dashboard TEST mode → Developers → API keys | M-BOOKING-CREATION |
| Stripe LIVE secret key (sk_live_...) | Stripe Dashboard LIVE → Developers → API keys | M-BOOKING-CREATION (after testing) |
| Quo SMS API key | Quo SMS dashboard → API | M-BOOKING-CREATION, M-BOOKING-CONFIRMATION |

=== IMPORTANT: TEST MODE FIRST ===
Use `sk_test_...` Stripe key for ALL testing. Switch to `sk_live_...` only after sandbox testing is complete and a Founder Decision record is created.

---

### D. Make Account Pre-Work

- [ ] Make account is active with adequate operations quota
- [ ] You are on a plan that supports webhooks (instant triggers)
- [ ] You have Airtable, Slack, Gmail apps connected in Make under your account
- [ ] Timezone set to your preferred operational timezone (Make → Profile → Timezone)

---

## DEPLOYMENT ENVIRONMENT

| Parameter | Value |
|-----------|-------|
| Make Zone | us1.make.com |
| Airtable Base | appdZ49WqgjRXxA1R |
| Production Environment Flag | Environment = "Production" |
| Sandbox Environment Flag | Environment = "Sandbox" |
| Brand A | SSS (She Said Sail) |
| Brand B | ME (Mare Executive) |

---

## POST-DEPLOYMENT VERIFICATION

After all 7 scenarios are live, verify:

1. [ ] All 7 scenarios show as **Active** in Make
2. [ ] All webhook URLs have been registered where required (see WEBHOOK_GUIDE.md)
3. [ ] All credential connections show as valid (no red indicators)
4. [ ] Airtable Audit Log table is receiving records
5. [ ] Slack #sss-ops-alerts channel is receiving messages
6. [ ] Full end-to-end test from TESTING_GUIDE.md has been completed
7. [ ] Founder Decision record created in Airtable before any real booking is processed

---

## SWITCHING FROM TEST TO LIVE

When ready to process real bookings:

=== MANUAL ACTION REQUIRED ===

1. In M-BOOKING-CREATION, update Modules 6 and 7:
   - Replace `sk_test_...` with `sk_live_...` Stripe secret key
2. In Stripe Dashboard, switch to LIVE mode and register the production webhook
3. Update Stripe webhook endpoint to point to STRIPE_DEPOSIT_WEBHOOK_URL
4. Create a Founder Decision record documenting the live switch
5. Run one real test booking with a low-value transaction

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — DEPLOYMENT_GUIDE.md*
