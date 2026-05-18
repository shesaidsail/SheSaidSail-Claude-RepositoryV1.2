# SHE SAID SAIL
# ROSE DAY CLUB — BACKEND SPECIFICATION

PAGE: Rose Day Club
URL: https://shesaidsail.com/experience/rose-day-club/
VERSION: 1.0

---

## FORM CONFIGURATION

Form Name (Webflow): Rose Day Club Inquiry
Form ID: rdc-inquiry-form
Webhook: SSS_LEAD_INTAKE_HOOK (Make.com SSS-LEAD-INTAKE scenario)
Airtable Base: appdZ49WqgjRXxA1R (She Said Sail)
Airtable Table: tblTlSB9CO4dTGodg (Requests)

---

## REQUIRED FORM FIELDS

All visible fields — confirm these exist in the Webflow form with exact name attributes:

| name attribute | type | required | validation |
|---------------|------|----------|------------|
| first_name | text | yes | not empty |
| last_name | text | yes | not empty |
| email | email | yes | valid email format |
| phone | tel | no | none |
| preferred_date | date | yes | not empty |
| guest_count | number | yes | 2-13 |
| occasion | select | yes | not empty |
| special_requests | textarea | no | none |

Pre-set hidden fields (set in Webflow as hidden form fields):

| name attribute | value |
|---------------|-------|
| experience | Rose Day Club |

Auto-populated hidden fields (via rose-day-club.js):

| name attribute | source |
|---------------|--------|
| source_url | window.location.href |
| utm_source | URL param or sessionStorage |
| utm_medium | URL param or sessionStorage |
| utm_campaign | URL param or sessionStorage |
| utm_content | URL param or sessionStorage |
| utm_term | URL param or sessionStorage |
| page_name | "rose-day-club" (static) |
| brand | "SSS" (static) |
| city | "Fort Lauderdale" (static) |

---

## MAKE.COM FLOW FOR THIS PAGE

When a Rose Day Club form submits:

1. Webhook receives payload from Webflow
2. Make checks idempotency key: LEAD-{email}-{preferred_date}-{guest_count}
3. If no duplicate: create Requests record in Airtable
4. Send Gmail auto-reply to submitted email
5. Post Slack alert to #sss-ops-alerts with lead details
6. Log to audit trail

Airtable record auto-sets:
- Experience: "Rose Day Club" (from form hidden field)
- Status: NEW
- Environment: Production
- Source_System: Make
- Brand: SSS
- City: Fort Lauderdale

---

## AIRTABLE RECORD MAPPING

| Webflow Form Field | Airtable Field | Notes |
|-------------------|----------------|-------|
| first_name | First Name | |
| last_name | Last Name | |
| email | Email | Dedupe key component |
| phone | Phone | |
| experience | Experience | Pre-set as "Rose Day Club" |
| preferred_date | Preferred Date | Dedupe key component |
| guest_count | Guest Count | Dedupe key component |
| occasion | Occasion | |
| special_requests | Special Requests | |

---

## OCCASION SELECT OPTIONS

These values must match exactly between form and Airtable:

- Bachelorette
- Birthday
- Girls Trip
- Anniversary
- Corporate
- Other Celebration

---

## GTM EVENTS (ANALYTICS)

Trigger: Form submit on form ID "rdc-inquiry-form"
Event name: sss_form_submit
Parameters pushed to dataLayer:
- event: "sss_form_submit"
- page_name: "rose-day-club"
- experience: "Rose Day Club"
- form_id: "rdc-inquiry-form"

CTA click events:
- event: "sss_cta_click"
- page_name: "rose-day-club"
- cta_text: (button text)
- cta_location: (section class)

---

## FORM SUCCESS BEHAVIOR

On successful Webflow form submission:
- Hide the form
- Show .rdc-form__success element
- (Optional) redirect to /thank-you/rose-day-club/ for GTM conversion tracking

---

## DUPLICATE PREVENTION

Make.com filter: checks Requests table for record where Idempotency_Key = LEAD-{email}-{preferred_date}-{guest_count}

If match found: skip create, skip email, skip Slack. Log to audit only.
If no match: proceed normally.

---

## TESTING CHECKLIST

Before launch, verify:

- [ ] Test submission received in Webflow form activity log
- [ ] Make.com scenario triggered on submission
- [ ] Airtable Requests record created with correct fields
- [ ] Experience field = "Rose Day Club"
- [ ] page_name hidden field value = "rose-day-club"
- [ ] source_url captured correctly
- [ ] UTM params captured (test with ?utm_source=test&utm_medium=test in URL)
- [ ] Auto-reply email received at test address
- [ ] Slack alert posted to #sss-ops-alerts
- [ ] Duplicate submission blocked (submit same form twice)
- [ ] GTM form submit event fires (verify in GTM preview mode)
- [ ] GA4 form_submit event visible in DebugView

---

## CONTACT / ESCALATION

For backend issues:
- hello@shesaidsail.com
- (754) 701-2228
- Slack: #sss-ops-alerts (for system alerts)
