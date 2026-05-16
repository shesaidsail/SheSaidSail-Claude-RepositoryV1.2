# MAKE_DEPLOYMENT_ORDER

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Exact implementation sequence for all Make scenarios across all stages. Follow this order without deviation.
**Classification:** Confidential — Internal Use Only

---

## GOVERNING PRINCIPLES

1. Every scenario completes sandbox testing before production promotion
2. Every scenario gets a Founder Decision record of type SYSTEM before production activation
3. Foundation scenarios deploy before dependent scenarios
4. Revenue safety scenarios (payment handling, emergency routing) deploy before intelligence layer
5. No two scenarios that write to the same Airtable table deploy simultaneously — stagger by 24 hours minimum to observe behavior
6. Each scenario runs in isolation for at least 48 hours in production before the next deploys
7. Stage N does not begin until Stage N-1 is stable for a minimum of 2 weeks

---

## PRE-DEPLOYMENT CHECKLIST (BEFORE ANYTHING)

Complete all of the following before the first Make scenario is built:

| # | Item | Owner | Status |
|---|------|-------|--------|
| 1 | Environment field added to Requests table | Will / Luciana | ☐ |
| 2 | Environment field added to Bookings table | Will / Luciana | ☐ |
| 3 | Idempotency_Key field added to Bookings | Will / Luciana | ☐ |
| 4 | Idempotency_Key field added to Requests | Will / Luciana | ☐ |
| 5 | D7_Review_Eligible formula added to Bookings | Will / Luciana | ☐ |
| 6 | AI_Prompt_Versions table replaced with 26-field version | Will | ☐ |
| 7 | Yacht_Availability table created with correct schema | Will / Luciana | ☐ |
| 8 | Automation_Health table created | Will / Luciana | ☐ |
| 9 | Make_Scenarios table migrated to main base | Will / Luciana | ☐ |
| 10 | Concierge_Operators table migrated to main base | Will / Luciana | ☐ |
| 11 | Airtable-native automation inventory completed — all Bookings triggers documented | Will | ☐ |
| 12 | Stripe webhook endpoints documented — existing scenarios listed | Will | ☐ |
| 13 | SSS Sandbox Make organization created | Will | ☐ |
| 14 | SSS Sandbox Airtable base created | Will | ☐ |
| 15 | Slack channels confirmed: #sss-ops-leads, #me-ops-leads, #sss-ops-bookings, #me-ops-bookings, #sss-ops-alerts, #sss-emergency-ops | Will / Luciana | ☐ |
| 16 | Webflow form submission webhook URL configured | Will | ☐ |
| 17 | All API credentials stored in credential vault | Will | ☐ |
| 18 | Founder Decision created: SYSTEM — "Make implementation approved — Stages 1–4" | Will | ☐ |

---

## STAGE 1 DEPLOYMENT SEQUENCE

### Week 1: Foundation

**Day 1–2: M-BRAND-ROUTER**
```
Build: Sandbox Make — brand classification logic
Test: Submit 10 test form payloads with different brand signals
Validate: SSS → SSS, ME → ME, ambiguous → SSS + LOW confidence + alert
Promote: Add to Stage 1 folder in production Make (inactive)
Founder Decision: FD-STAGE1-001
```

**Day 3–4: M-LEAD-INTAKE**
```
Build: Sandbox Make — Webflow webhook to sandbox Airtable Requests
Test: Submit real test form on sandbox Webflow → confirm sandbox Request created
Test: Submit duplicate → confirm idempotency prevents second record
Validate: Slack message appears in test channel (#sss-sandbox-leads)
Validate: Audit_Log entry created in sandbox base
Validate: M-BRAND-ROUTER called correctly — brand field populated
Promote: Production Make — activate ONLY with sandbox Webflow form
Founder Decision: FD-STAGE1-002
Production live test: Submit test lead → confirm production Airtable record created
Activate: Full production — real Webflow form connected
Monitor: 48 hours — zero duplicate records
```

**Day 5: M-STRIPE-DEPOSIT**
```
Build: Sandbox Make — Stripe test mode webhook
Test: Stripe test mode — send test payment_intent.succeeded
Validate: Sandbox Booking status updated, confirmation email sent (to test email), Slack posted
Test: Send duplicate Stripe event → confirm idempotency prevents double processing
Test: Send payment_intent.payment_failed → confirm M-FAILED-PAYMENT-HANDLER triggers correctly
Promote: Production Make — Stripe test mode still active
Note: Do not switch to live Stripe credentials until M-BOOKING-CREATION is deployed
```

### Week 2: Booking Flow

**Day 1–2: M-BOOKING-CREATION**
```
Build: Sandbox Make — reads sandbox Requests, creates sandbox Bookings, generates test Stripe link
Test: Mark sandbox Request as AVAILABILITY_CONFIRMED → confirm Booking created
Validate: Stripe payment link generated (test mode)
Validate: Deposit request email sent (to test email), SMS sent (to test phone)
Validate: Slack message posted
Validate: Audit_Log entry created
Test: Attempt to create second Booking from same Request → confirm idempotency prevents duplicate
Promote: Production Make
Founder Decision: FD-STAGE1-003
Production live test: Mark a real test Request as AVAILABILITY_CONFIRMED with Will present
Monitor: 48 hours
```

**Day 3: M-BOOKING-CONFIRMATION**
```
Build: Sandbox → Production path same as above
Test: Set sandbox Booking.Status = CONFIRMED → confirm confirmation email sent
Test: HV_Client = true path → confirm Luciana DM (not client email)
Test: Emergency_Flag = true → confirm no email sent, no Slack, only Audit_Log entry
Promote: Production
Founder Decision: FD-STAGE1-004
```

**Day 4: M-CONCIERGE-ASSIGNMENT**
```
Build: Test with sandbox Concierge_Operators record (Luciana as test concierge)
Validate: Slack DM sent to test Slack ID on deposit confirmation
Validate: Email fallback when Slack ID missing
Promote: Production
Founder Decision: FD-STAGE1-005
```

**Day 5: Switch Stripe to Live Mode**
```
Update M-STRIPE-DEPOSIT and M-BOOKING-CREATION webhook credentials to live Stripe
Run one test booking end-to-end with a real $1 test transaction (refund immediately)
Confirm everything fires correctly in production with live Stripe
Document: Stripe live webhook URL and secret in credential vault
```

### Week 3: Lifecycle and Review

**Day 1–3: M-BASIC-LIFECYCLE**
```
Build: Sandbox with 5 test Booking records at different lifecycle stages
Test each lifecycle point:
  - T-72hr: Booking with charter date 3 days out → confirm reminder sent + boolean set
  - T-48hr: Booking 2 days out → confirm logistics email sent
  - T-24hr: Booking 1 day out → confirm reminder sent
  - D1: Booking completed yesterday → confirm D1 message sent
Test: Emergency_Flag = true → confirm no messages, Audit_Log shows skip
Test: Automations_Paused = true → confirm no messages
Test: Run twice on same bookings → confirm no duplicates (boolean gates work)
Promote: Production
Founder Decision: FD-STAGE1-006
Monitor: 1 week — watch for any duplicate sends
```

**Day 4–5: M-REVIEW-REQUEST**
```
Build: Sandbox with test Bookings that are 7 days post-charter, various Charter_Grades
Test: D7_Review_Eligible = true → confirm review request sent
Test: D7_Review_Eligible = false → confirm no email sent (silently)
Test: HV_Client = true → confirm Luciana DM only, no client email
Test: Run twice → confirm D7_Sent gate prevents duplicate
Promote: Production
Founder Decision: FD-STAGE1-007
```

**Day 5: Stage 1 Completion Validation**
```
Execute MAKE_TESTING_PROTOCOLS.md — Stage 1 full end-to-end test
Pass all Stage 1 success criteria
Document: All scenario IDs in Make_Scenarios Airtable table
Confirm: Ads can safely run
Will sign-off: Stage 1 complete
```

---

## STAGE 2 DEPLOYMENT SEQUENCE

**Minimum wait:** 2 weeks of stable Stage 1 before beginning Stage 2.

### Week 1: Safety Scenarios

**Day 1–2: M-DOUBLE-BOOKING-CHECK**
```
Deploy before M-YACHT-AVAILABILITY-LOCK — check must exist before lock
Test: Create Yacht_Availability record with Status = BOOKED for a date
Test: Mark Request as AVAILABILITY_CONFIRMED for same yacht + date → confirm conflict detected, Luciana alerted
Test: No conflict → confirm flow continues to M-BOOKING-CREATION normally
Founder Decision: FD-STAGE2-001
```

**Day 3–4: M-YACHT-AVAILABILITY-LOCK**
```
Test: Deposit confirmed → Yacht_Availability record updated to BOOKED
Test: Attempt to lock already-booked date → confirm conflict alert, no lock
Test: Cancellation (manual) → confirm Yacht_Availability manually reset to AVAILABLE
Founder Decision: FD-STAGE2-002
```

**Day 5: M-FAILED-PAYMENT-HANDLER**
```
Test: Stripe test mode — send payment_intent.payment_failed
Test: 3 consecutive failures → confirm Failure 3 path fires (Luciana DM + Booking status update)
Founder Decision: FD-STAGE2-003
```

### Week 2: Operations Scenarios

**M-CHARTER-BRIEF → M-VENDOR-NOTIFICATIONS → M-ESCALATION-ROUTER**
```
Deploy in this order — Charter Brief must exist before Vendor Notifications
Each: sandbox test → production promotion → 48hr monitoring
Founder Decisions: FD-STAGE2-004, FD-STAGE2-005, FD-STAGE2-006
```

### Week 3: Engagement and Monitoring

**M-REFERRAL-ENGINE → M-REBOOKING-ENGINE → M-AUTOMATION-HEALTH**
```
Referral and Rebooking: test with sandbox bookings at D30 and D60 mark
Automation Health: deploy last — it monitors all other Stage 2 scenarios
Allow M-AUTOMATION-HEALTH to run for 1 week before Stage 3 begins
Founder Decisions: FD-STAGE2-007, FD-STAGE2-008, FD-STAGE2-009
```

---

## STAGE 3 DEPLOYMENT SEQUENCE

**Minimum wait:** 2 weeks of stable Stage 2 before beginning Stage 3.

**AI Prompt Versions required before Stage 3 begins:**
- LEAD_SCORING_SYSTEM prompt version — Will reviewed + Will_Approved = true
- FOUNDER_DIGEST_SYSTEM prompt version — Will reviewed + Will_Approved = true
- All other Stage 3 prompts created and approved before corresponding scenario deploys

### Order:
```
M-LTV-ENGINE (no Claude API — deploy first, purely data aggregation)
M-REVENUE-HEALTH (no Claude API — deploy second)
M-CITY-HEALTH (no Claude API — deploy third)
M-AI-LEAD-SCORING (first Claude API scenario — test scoring logic, validate outputs)
M-FOUNDER-DIGEST (validate Thursday delivery, Will confirms useful)
M-PARTNER-SCORING (no Claude API — deploy after digest confirmed)
M-PRICING-INTELLIGENCE (Claude API + Tier B — Will reviews first recommendation before activating)
M-CONCIERGE-INTELLIGENCE (Claude API + Tier B — Will reviews first report before activating)
```

Each scenario: Founder Decision → build → sandbox test → production → 48hr monitor.

---

## STAGE 4 DEPLOYMENT SEQUENCE

**Minimum wait:** 4 weeks of stable Stage 3 before beginning Stage 4.

### Order:
```
M-SYNTER-SYNC (financial sync — highest priority in Stage 4, no Claude API)
M-EXECUTIVE-DASHBOARD (no Claude API — data aggregation)
M-OPS-HUB (no Claude API — Luciana validates daily)
M-OWNER-HUB (no Claude API — Will validates weekly)
M-CREATIVE-FATIGUE (no Claude API — alert only)
M-CREATIVE-INTELLIGENCE (Claude API — validate first run with Will)
M-CAMPAIGN-RECOMMENDER (Claude API + Tier B — highest caution)
M-SOP-INTELLIGENCE (Claude API + Tier B — monthly, lowest risk)
M-CITY-LAUNCH (Tier B — test with sandbox city activation)
```

---

## ROLLBACK PROCEDURE FOR FAILED DEPLOYMENT

If any scenario fails after production activation:

```
1. Immediately: Disable scenario in Make (toggle off)
2. Within 15 minutes: Audit_Log review — identify affected records
3. Slack: Notify Luciana and Will of exact failure
4. Create Founder Decision: Type = SYSTEM, Urgency = SAME_DAY
5. If client messages were sent in error: Luciana personally follows up within 2 hours
6. If Airtable records were created in error: Will approves deletion or correction
7. Fix in sandbox: reproduce the failure, fix, re-test
8. Re-deploy only after Will approval
9. Document in deployment log: what failed, why, what changed
```

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*MAKE_DEPLOYMENT_ORDER v1.0*
*Effective May 2026*
