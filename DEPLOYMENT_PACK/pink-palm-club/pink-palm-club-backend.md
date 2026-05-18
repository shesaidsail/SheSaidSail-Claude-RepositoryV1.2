# PINK PALM CLUB
# BACKEND SPECIFICATION

STATUS: READY FOR IMPLEMENTATION
VERSION: v1.0
EFFECTIVE DATE: May 2026
PAGE: https://shesaidsail.com/experience/pink-palm-club/
BACKEND OWNER: Will Hunt
SYSTEM REFERENCE: docs/system/master-backend-system.md

---

## FORM-TO-WEBHOOK MAPPING

### Webhook Endpoint
SSS_LEAD_INTAKE_HOOK (production Make webhook for SSS-LEAD-INTAKE scenario)
Get current URL from Make > SSS-LEAD-INTAKE > Module 1 (gateway:CustomWebHook)

### Form Name (Webflow)
"Pink Palm Club Inquiry"

---

## FIELD MAPPING TABLE

| HTML field `name` | Populated By | Value | Airtable Field |
|------------------|-------------|-------|----------------|
| first_name | User input | User entry | First Name |
| last_name | User input | User entry | Last Name |
| email | User input | User entry | Email |
| phone | User input | User entry | Phone |
| preferred_date | User input | YYYY-MM-DD | Preferred Date |
| guest_count | User dropdown | 2-13 | Guest Count |
| occasion | User dropdown | See options | Occasion |
| special_requests | User textarea | Free text | Special Requests |
| experience | JS auto | "Pink Palm Club" | Experience |
| yacht | JS auto | "Lucky Star" | Yacht |
| city | JS auto | "Fort Lauderdale" | City |
| duration | JS auto | "4 hours" | Duration |
| boarding_location | JS auto | "Fort Lauderdale Beach Marina" | Boarding Location |
| add_ons | JS (addon click) | Comma-separated selection | Add-Ons Selected |
| source_url | JS auto | window.location.href | Source URL |
| page_slug | JS auto | window.location.pathname | (logged, not mapped to named field) |
| utm_source | JS from URL | URL param value | UTM_Source |
| utm_medium | JS from URL | URL param value | UTM_Medium |
| utm_campaign | JS from URL | URL param value | UTM_Campaign |
| utm_content | JS from URL | URL param value | UTM_Content |
| utm_term | JS from URL | URL param value | (optional, not in current Make mapper) |

---

## AUTO-POPULATED BY MAKE (not in form)

| Airtable Field | Value |
|----------------|-------|
| Status | NEW |
| Environment | Production |
| Source_System | Make |
| Brand | SSS (derived from source_url not containing "mareexecutive.com") |
| Idempotency_Key | LEAD-{email}-{preferred_date}-{guest_count} |

---

## OCCASION DROPDOWN OPTIONS

Match these values exactly in Webflow form options:

| Display label | Submitted value |
|--------------|----------------|
| Bachelorette | Bachelorette |
| Birthday | Birthday |
| Girls trip | Girls Trip |
| Anniversary | Anniversary |
| Corporate outing | Corporate |
| Something else | Other |

---

## CANONICAL EXPERIENCE NAME

The `experience` hidden field must always submit exactly:
**Pink Palm Club**

Airtable filtering, Make routing, and email template use this string. Any variation breaks reporting.

---

## IDEMPOTENCY BEHAVIOR

If a guest submits the form twice with:
- Same email address
- Same preferred_date
- Same guest_count

...the second submission will NOT create a second Airtable record and will NOT trigger a second confirmation email. This is correct behavior and prevents duplicate follow-up.

If the guest changes any one of the three fields, a new record IS created. This is correct -- a genuine change in their request should create a new inquiry.

---

## CONFIRMATION EMAIL BEHAVIOR

On successful record creation:
1. Airtable record Status = "NEW"
2. Make sends HTML confirmation email to guest's email address
3. Email includes: Experience name, Preferred Date, Guest Count, Occasion
4. Email from: hello@shesaidsail.com
5. Slack alert posted to: #sss-ops-alerts

If the confirmation email is not received within 3 minutes of submission, check:
- Make scenario SSS-LEAD-INTAKE is active (not paused)
- Webhook URL in Webflow form matches the live Make webhook URL
- Gmail connection in Make is authenticated

---

## POST-SUBMISSION AIRTABLE RECORD EXAMPLE

| Field | Expected Value |
|-------|---------------|
| First Name | Sarah |
| Last Name | Johnson |
| Email | sarah@example.com |
| Phone | (555) 000-0000 |
| Experience | Pink Palm Club |
| Yacht | Lucky Star |
| City | Fort Lauderdale |
| Preferred Date | 2026-07-15 |
| Duration | 4 hours |
| Guest Count | 8 |
| Occasion | Bachelorette |
| Boarding Location | Fort Lauderdale Beach Marina |
| Add-Ons Selected | Charcuterie Board, Champagne Toast |
| Special Requests | Bride's name is Emma, nut allergy for one guest |
| Status | NEW |
| Environment | Production |
| Brand | SSS |
| Source_System | Make |
| Source URL | https://shesaidsail.com/experience/pink-palm-club/?utm_source=instagram&utm_medium=paid_social |
| UTM_Source | instagram |
| UTM_Medium | paid_social |
| UTM_Campaign | sss-ppc-q2-2026 |
| Idempotency_Key | LEAD-sarah@example.com-2026-07-15-8 |

---

## AIRTABLE INTEGRATION NOTES

Base: She Said Sail (appdZ49WqgjRXxA1R)
Table: Requests (tblTlSB9CO4dTGodg)

The Requests table must have fields for all mapped values above. If UTM fields are not yet present in the Requests table, they should be added as single-line text fields. Reference master-backend-system.md for the full field spec.

---

## MAKE SCENARIO DEPENDENCIES

This page depends on the following Make scenarios being active:
- SSS-LEAD-INTAKE (M-LEAD-INTAKE.json) -- primary intake, Airtable create, confirmation email, Slack alert
- SSS-AUDIT-LOGGER (M-AUDIT-LOGGER.json) -- if routing through the brand router

No changes to the Make scenarios are required to support this page. The existing SSS-LEAD-INTAKE scenario handles all fields as mapped above.

---

## QA STEPS FOR BACKEND VERIFICATION

1. Load https://shesaidsail.com/experience/pink-palm-club/
2. Open browser developer tools > Network tab
3. Complete the form with test data (use a test email address)
4. Submit the form
5. Verify: network request to Make webhook returns 200 status
6. Check Airtable Requests table: new record created with all fields populated
7. Check email inbox: confirmation email received
8. Check Slack: alert in #sss-ops-alerts
9. Submit the identical form again
10. Verify: NO second Airtable record created (idempotency working)

---

## DEPLOYMENT CHECKLIST

- [ ] Webflow form action URL set to production Make webhook URL
- [ ] Webflow form name set to "Pink Palm Club Inquiry"
- [ ] All visible form fields present with correct `name` attributes
- [ ] All hidden fields present with correct `name` attributes (auto-populated by JS)
- [ ] pink-palm-club.js included in Webflow custom code before closing body tag
- [ ] Live test submission verified end-to-end
- [ ] No test records in production Airtable (clean up after QA)
