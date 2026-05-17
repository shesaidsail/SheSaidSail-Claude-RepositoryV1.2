# REBINDING GUIDE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Per-scenario credential rebinding after import

After importing each blueprint, Make will show broken connection indicators on modules that use external services. This guide provides exact rebinding steps for every module in every scenario.

---

## GLOBAL CONNECTIONS NEEDED

Before rebinding any scenario, ensure these connections exist in Make:

| Connection Type | Connection Name (suggested) | Make Path |
|-----------------|----------------------------|-----------|
| Airtable PAT | SSS Airtable PAT | Make → Connections → Add → Airtable |
| Slack OAuth | SSS Slack | Make → Connections → Add → Slack |
| Gmail OAuth | SSS Gmail (hello@shesaidsail.com) | Make → Connections → Add → Gmail |

HTTP connections (Stripe, Quo SMS) use API key authentication inline in the module — no separate Make connection needed.

---

## SCENARIO 1: SSS-OPS-LOGGER-ALERTER

### Module 3 — airtable:ActionCreateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Audit Log → tblrMpTfMk8q1eNHp
```

### Module 8 — slack:ActionPostMessage
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Slack
Channel: #sss-emergency-ops
(Channel must exist in workspace before rebinding)
```

### Module 10 — slack:ActionPostMessage
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Slack
Channel: #sss-lead-intake
```

### Module 12 — slack:ActionPostMessage
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Slack
Channel: #sss-ops-alerts
```

---

## SCENARIO 2: SSS-BRAND-ROUTER

### Module 6 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Requests → tblTlSB9CO4dTGodg
```

### Module 9 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Requests → tblTlSB9CO4dTGodg
```

### Module 12 — http:ActionSendData (OPS-LOGGER-ALERTER call)
```
=== INSERT YOUR VALUE HERE ===
In the body field, replace:
PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
With the webhook URL copied from SSS-OPS-LOGGER-ALERTER Module 1
```

---

## SCENARIO 3: SSS-LEAD-INTAKE

### Module 3 — airtable:SearchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Requests → tblTlSB9CO4dTGodg
```

### Module 5 — http:ActionSendData (Brand Router call)
```
=== INSERT YOUR VALUE HERE ===
In the url field, replace:
PASTE_BRAND_ROUTER_WEBHOOK_URL_HERE
With the webhook URL from SSS-BRAND-ROUTER Module 1
```

### Module 7 — airtable:ActionCreateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Requests → tblTlSB9CO4dTGodg
```

### Module 8 — gmail:ActionSendEmail
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Gmail
Account: hello@shesaidsail.com
```

### Module 9 — http:ActionSendData (OPS-LOGGER-ALERTER call)
```
=== INSERT YOUR VALUE HERE ===
In the url field, replace:
PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
With the webhook URL from SSS-OPS-LOGGER-ALERTER Module 1
```

---

## SCENARIO 4: SSS-STRIPE-DEPOSIT

### Module 4 — airtable:SearchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 7 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 8 — http:ActionSendData (OPS-LOGGER-ALERTER call)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
```

---

## SCENARIO 5: SSS-BOOKING-CREATION

### Module 1 — airtable:WatchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Base: She Said Sail → appdZ49WqgjRXxA1R
Table: Requests → tblTlSB9CO4dTGodg
Formula: AND({Status} = 'AVAILABILITY_CONFIRMED', {Environment} = 'Production')
```

### Module 3 — airtable:SearchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 5 — airtable:ActionCreateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 6 — http:ActionSendData (Stripe POST /v1/prices)
```
=== INSERT YOUR VALUE HERE ===
In the Authorization header, replace:
PASTE_STRIPE_SECRET_KEY_HERE
With: Bearer sk_test_YOUR_ACTUAL_KEY
(Use TEST key during testing, LIVE key for production)
```

### Module 7 — http:ActionSendData (Stripe POST /v1/payment_links)
```
=== INSERT YOUR VALUE HERE ===
In the Authorization header, replace:
PASTE_STRIPE_SECRET_KEY_HERE
With: Bearer sk_test_YOUR_ACTUAL_KEY
(SAME key as Module 6 — must be consistent)
```

### Module 9 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 11 — gmail:ActionSendEmail
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Gmail
Account: hello@shesaidsail.com
```

### Module 12 — http:ActionSendData (Quo SMS)
```
=== INSERT YOUR VALUE HERE ===
In the Authorization header, replace:
PASTE_QUO_SMS_API_KEY_HERE
With: Bearer YOUR_ACTUAL_QUO_API_KEY
```

### Module 13 — http:ActionSendData (OPS-LOGGER-ALERTER call)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
```

---

## SCENARIO 6: SSS-CONCIERGE-ASSIGNMENT

### Module 1 — airtable:WatchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
Formula: AND({Status} = 'DEPOSIT_PAID', {Concierge_Assigned} = 0, {Environment} = 'Production')
```

### Module 4 — airtable:SearchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Concierge_Operators → tblX61IB2qjDmac8l
```

### Module 7 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 8 — http:ActionSendData (OPS-LOGGER-ALERTER — success branch)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
```

### Module 10 — http:ActionSendData (OPS-LOGGER-ALERTER — failure branch)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
```

---

## SCENARIO 7: SSS-BOOKING-CONFIRMATION

### Module 1 — airtable:WatchRecords
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
Formula: AND({Status} = 'CONFIRMED', {Confirmation_Sent} = 0, {Environment} = 'Production')
```

### Module 6 — airtable:GetRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Clients → tblr84vRIWC5HmKvo
```

### Module 8 — gmail:ActionSendEmail
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Gmail
Account: hello@shesaidsail.com
```

### Module 9 — http:ActionSendData (Quo SMS)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_QUO_SMS_API_KEY_HERE
```

### Module 10 — airtable:ActionUpdateRecord
```
=== MANUAL ACTION REQUIRED ===
Connection: SSS Airtable PAT
Table: Bookings → tbl72omPibBkn2hZL
```

### Module 11 — http:ActionSendData (OPS-LOGGER-ALERTER call)
```
=== INSERT YOUR VALUE HERE ===
Replace: PASTE_OPS_LOGGER_ALERTER_WEBHOOK_URL_HERE
```

---

## REBINDING VERIFICATION CHECKLIST

After rebinding all scenarios, verify:

- [ ] SSS-OPS-LOGGER-ALERTER: Airtable green, Slack green (3 modules)
- [ ] SSS-BRAND-ROUTER: Airtable green (2 modules)
- [ ] SSS-LEAD-INTAKE: Airtable green (2 modules), Gmail green
- [ ] SSS-STRIPE-DEPOSIT: Airtable green (2 modules)
- [ ] SSS-BOOKING-CREATION: Airtable green (4 modules), Gmail green
- [ ] SSS-CONCIERGE-ASSIGNMENT: Airtable green (3 modules)
- [ ] SSS-BOOKING-CONFIRMATION: Airtable green (3 modules), Gmail green
- [ ] All PASTE_... placeholders have been replaced in all scenarios
- [ ] No red connection indicators remain in any scenario

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — REBINDING_GUIDE.md*
