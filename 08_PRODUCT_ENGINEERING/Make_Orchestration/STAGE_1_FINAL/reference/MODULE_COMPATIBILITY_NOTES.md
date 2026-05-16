# MODULE COMPATIBILITY NOTES
## She Said Sail — Stage 1 Make Orchestration

**Status:** PRODUCTION REFERENCE  
**Version:** 1.0  
**Date:** May 2026  

---

## AIRTABLE MODULE COMPATIBILITY

### Version Requirements
All Airtable modules must use **version 3**. Version 1 and 2 use a deprecated field schema format that may produce unexpected behavior on new Make workspaces.

### Field Type Compatibility

| Airtable Field Type | Make Mapping | Notes |
|--------------------|-------------|-------|
| Single line text | Plain string value | Direct mapping |
| Long text | Plain string value | Supports newlines via `\n` |
| Single select | Plain string (option name exactly as in Airtable) | Case-sensitive |
| Multiple select | Array of strings | Pass as `["Option1", "Option2"]` |
| Checkbox | Boolean: `true` or `false` | Do NOT pass as string |
| Date | ISO 8601 string `YYYY-MM-DD` | No time component for date-only fields |
| DateTime | ISO 8601 `YYYY-MM-DDTHH:mm:ssZ` | Include timezone |
| Number | Numeric value | No quotes |
| Currency | Numeric value (not formatted string) | Do NOT pass `"$5,000"` — pass `5000` |
| Linked record | Array of record ID objects: `[{"id":"recXXXX"}]` | Cannot pass display value — must use record ID |
| Rollup | Read-only | Cannot be set via API |
| Formula | Read-only | Cannot be set via API |

### Watch Records Polling
`airtable:TriggerWatchRecords` polls on a schedule (minimum 1 minute on paid Make plan). It is NOT instant. For time-sensitive operations (Stripe webhook responses), use `gateway:CustomWebHook` instead. The polling trigger is appropriate for M-STRIPE-DEPOSIT (monitoring availability confirmations) and M-BOOKING-CONFIRMATION (monitoring confirmations set by Luciana).

---

## SLACK MODULE COMPATIBILITY

### Version Requirements
Use `slack:CreateAMessage` **v4** for Block Kit support. Earlier versions send plain text only.

### Channel ID vs. Channel Name
Make's Slack module accepts both channel IDs (C0XXXXXXXXX) and channel names (#sss-ops-alerts). Using channel IDs is more reliable — channel names can change. After setting up Slack, verify channel IDs by right-clicking the channel in Slack > Copy link > extract ID from URL.

### DM vs. Channel Messages
To send a DM to a specific user, pass the user's Slack member ID (U0XXXXXXXXX) as the `channelId`. Do NOT use a channel ID. The user must have the SSS Slack app in their workspace.

### Block Kit Limits
- Maximum 50 blocks per message
- Section field arrays: maximum 10 fields per section
- Text fields: maximum 3000 characters
- All Stage 1 Slack messages are well within limits

---

## STRIPE API COMPATIBILITY

### API Version
All Stripe API calls use **version 2023-10-16** via the `Stripe-Version` header. This version is required for:
- Payment Link metadata support
- Current `checkout.session.completed` event schema
- Idempotency key support

### Deprecated Native Module
The Make native `stripe:ActionCreatePaymentLink` module uses Stripe API version 2019-02-11. This version:
- Does NOT support `metadata` on Payment Links
- Does NOT support `after_completion.redirect.url`
- Does NOT include `metadata` in `checkout.session.completed` webhook events
- Cannot be used for booking_id → airtable_record_id tracking

All Stage 1 Stripe operations use `http:ActionSendData` with the Stripe REST API directly.

### Stripe Webhook Event Schema (2023-10-16)
```
checkout.session.completed event structure:
{
  "id": "evt_XXXXX",
  "type": "checkout.session.completed",
  "data": {
    "object": {
      "id": "cs_XXXXX",
      "payment_intent": "pi_XXXXX",
      "amount_total": 250000,
      "currency": "usd",
      "customer_details": {
        "email": "client@email.com",
        "name": "Client Name"
      },
      "metadata": {
        "booking_id": "BK-2026-0001",
        "airtable_record_id": "recXXXXXXXXXXXXXX",
        "payment_type": "deposit",
        "brand": "SSS",
        "environment": "Production"
      }
    }
  }
}
```

Field paths in M-BOOKING-CREATION map directly to this schema.

### Stripe Idempotency Keys
Format used: `deposit-{booking_id}-{YYYYMMDD}`  
This prevents duplicate Payment Links if the trigger fires multiple times on the same day. Stripe treats two requests with the same Idempotency-Key as the same request and returns the first result.

---

## GMAIL MODULE COMPATIBILITY

### OAuth Scope Requirements
The Gmail OAuth connection must be authorized with at minimum:
- `gmail.send` — to send emails
- `gmail.compose` — required for some Make versions

If `hello@shesaidsail.com` is a Google Workspace account, the Gmail OAuth must be connected as that address OR the connected account must have "Send as" delegation from `hello@shesaidsail.com` in Google Workspace Admin.

### HTML Email
M-STRIPE-DEPOSIT and M-BOOKING-CONFIRMATION send HTML emails. Make's Gmail module supports HTML body when `bodyType` is set to `html`. Test in a real inbox — some email clients render differently.

---

## HTTP MODULE COMPATIBILITY

### `http:ActionSendData` v3 Headers
Headers are defined as an array of name/value pairs:
```json
[
  {"name": "Authorization", "value": "Bearer {{SECRET}}"},
  {"name": "Content-Type", "value": "application/json"}
]
```

### URL-Encoded Body (Stripe API)
For Stripe's REST API, use `bodyType: urlencoded` with body as key/value array:
```json
[
  {"key": "line_items[0][price_data][currency]", "value": "usd"},
  {"key": "metadata[booking_id]", "value": "BK-2026-0001"}
]
```
Nested objects use bracket notation. Arrays use `[index]` suffix.

### JSON Body (Internal Make Calls)
For internal Make webhook calls, use `bodyType: raw` with `contentType: application/json`. The body must be a valid JSON string.

---

## KNOWN MAKE PLATFORM NOTES

### Execution Order
Modules in a Make scenario execute sequentially in the order they appear. Parallel branches are possible with routers but are not used in Stage 1.

### Filter Behavior
When a filter condition is false, the scenario branch stops. Modules after a failed filter do not execute for that iteration. The scenario does NOT error — it simply stops at that point.

### Error Handling
Without explicit error handling, a module error stops the scenario and marks it as failed. For production resilience, configure error handlers on each critical module (make.com scenario > right-click module > Add error handler).

### Make Variables
Variables in `{{double curly braces}}` are Make's dynamic variable syntax. Module output is referenced as `{{moduleNumber.fieldName}}`. For nested objects: `{{1.body.data.object.metadata.booking_id}}`.

---

*She Said Sail · Stage 1 Module Compatibility Notes*  
*CONFIDENTIAL — INTERNAL USE ONLY*
