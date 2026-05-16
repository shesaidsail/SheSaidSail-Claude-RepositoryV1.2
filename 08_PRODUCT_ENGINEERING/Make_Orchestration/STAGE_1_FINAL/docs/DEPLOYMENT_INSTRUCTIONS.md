# STAGE 1 DEPLOYMENT INSTRUCTIONS
## She Said Sail — Make Orchestration

**Status:** PRODUCTION  
**Version:** 1.0  
**Date:** May 2026  
**Owner:** Will Hunt  

---

## ENVIRONMENT REQUIREMENTS

Before deploying any Stage 1 scenario to Production, confirm:

- [ ] Make.com account active with team plan (supports multiple connections)
- [ ] Airtable Production base `appdZ49WqgjRXxA1R` is live and accessible
- [ ] Audit Log table exists in Airtable with required fields (see Reference)
- [ ] Requests table exists with Agent_Status field (Single Select: AI_RESPONDING, HUMAN_REVIEW, ESCALATED, CLOSED)
- [ ] Bookings table has all required Stage 1 fields (see credential checklist)
- [ ] Stripe account active with API keys accessible
- [ ] Slack workspace connected — SSS workspace OAuth app installed
- [ ] Gmail OAuth connection configured for hello@shesaidsail.com
- [ ] #sss-ops-alerts channel exists in Slack workspace
- [ ] #sss-emergency-ops channel exists in Slack workspace

---

## STEP-BY-STEP DEPLOYMENT

### Phase A: Sandbox Validation (Required Before Production)

1. Create a Sandbox scenario copy for each blueprint in Make
2. Point Sandbox Airtable trigger to a test base (NOT appdZ49WqgjRXxA1R)
3. Use Stripe test mode keys (prefix `sk_test_`)
4. Send test data through each scenario end-to-end
5. Verify Airtable records created correctly
6. Verify Slack messages arrive in correct channels
7. Verify no errors in Make scenario history
8. Document sandbox validation completion in Airtable Deployment Log

### Phase B: Production Import

1. In Make, go to Scenarios > Create a new scenario
2. Use the blueprint import option (JSON import)
3. Upload the JSON file from `blueprints/` directory
4. Do NOT activate yet — complete credential binding first

### Phase C: Credential Binding (Per Scenario)

Replace all `{{VARIABLE}}` tokens before activation. See `CREDENTIAL_REBINDING_CHECKLIST.md` for complete list.

**Quick reference — credentials shared across scenarios:**

| Credential Variable | Value Source | Scenarios Using It |
|--------------------|-----------|--------------------|
| `AIRTABLE_BASE_ID_PRODUCTION` | `appdZ49WqgjRXxA1R` | All |
| `AIRTABLE_PAT` | Airtable > Account > Developer Hub > Personal Access Token | All |
| `SLACK_CONNECTION_ID` | Make > Connections > Slack OAuth | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `SLACK_WILL_DM_ID` | Slack: right-click Will's profile > Copy member ID | M-SLACK-ALERTS, M-CONCIERGE-ASSIGNMENT |
| `STRIPE_SECRET_KEY` | Stripe Dashboard > API Keys > Restricted Key | M-STRIPE-DEPOSIT |
| `GMAIL_CONNECTION_ID` | Make > Connections > Gmail OAuth | M-STRIPE-DEPOSIT, M-BOOKING-CONFIRMATION |
| `AUDIT_LOGGER_WEBHOOK_URL` | Generated after M-AUDIT-LOGGER import | M-LEAD-INTAKE, M-STRIPE-DEPOSIT, M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION |
| `SLACK_ALERTS_WEBHOOK_URL` | Generated after M-SLACK-ALERTS import | M-LEAD-INTAKE, M-BOOKING-CREATION |

### Phase D: Activation Sequence

Activate in exact order (see `FINAL_STAGE_1_IMPORT_ORDER.md`):
1. M-AUDIT-LOGGER
2. M-SLACK-ALERTS
3. M-BRAND-ROUTER
4. M-LEAD-INTAKE
5. M-STRIPE-DEPOSIT
6. M-BOOKING-CREATION
7. M-CONCIERGE-ASSIGNMENT
8. M-BOOKING-CONFIRMATION

### Phase E: Post-Activation Testing

Run the full validation sequence from `FINAL_STAGE_1_IMPORT_ORDER.md` section "POST-ACTIVATION VALIDATION SEQUENCE."

### Phase F: Deployment Log Entry

After successful activation, create a Deployment Log record in Airtable:

| Field | Value |
|-------|-------|
| Deployment_ID | DEP-2026-0001 |
| Deployed_By | Will Hunt |
| Deployed_At | (timestamp) |
| Environment | Production |
| Scenarios_Deployed | List all 8 |
| Validation_Status | PASSED |
| Rollback_Procedure | Deactivate in reverse order |
| Notes | Stage 1 initial deployment |

---

## ERROR HANDLING ARCHITECTURE

Every Stage 1 scenario follows the same error escalation pattern:

| Failure | Automatic Response |
|---------|-------------------|
| First failure | Log to Automation_Failures table; retry after 2 minutes |
| Second failure | Retry after 5 minutes |
| Third failure | Slack alert to #sss-ops-alerts via M-SLACK-ALERTS |
| Fourth failure | Slack DM to Will; scenario pauses; Founder Decision: SEV-2 created |
| 30+ minutes persistent | SEV-1 manual recovery required |

Configure this error handling in Make scenario settings (Scenario > Settings > Error Handling).

---

## MONITORING

After deployment, monitor:

- Make scenario execution history — check for errors daily for first week
- Airtable Audit Log table — verify records are being written
- #sss-ops-alerts Slack channel — verify notifications arriving
- Airtable Automation_Failures table — verify no accumulation

Set up Make scenario monitoring alerts: Scenario > Settings > Notifications.

---

*She Said Sail · Stage 1 Deployment Instructions*  
*CONFIDENTIAL — INTERNAL USE ONLY*
