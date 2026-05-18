# SHE SAID SAIL
# MASTER BACKEND SYSTEM

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## SYSTEM ARCHITECTURE

All web forms connect to: Webflow form submission > Make webhook > Airtable Requests table > Email confirmation > Slack ops alert

Primary base: She Said Sail (appdZ49WqgjRXxA1R)
Primary table: Requests (tblTlSB9CO4dTGodg)
Webhook: SSS-LEAD-INTAKE (SSS_LEAD_INTAKE_HOOK)

---

## REQUIRED FORM FIELDS

Every inquiry form on SheSaidSail.com must submit the following fields to the webhook. Field names must match exactly (case-sensitive).

### Visible Fields

| Field Name | Type | Required | Notes |
|------------|------|----------|-------|
| first_name | text | yes | |
| last_name | text | yes | |
| email | email | yes | |
| phone | tel | yes | |
| experience | text | yes | Pre-filled or dropdown per page |
| yacht | text | no | Pre-filled per page if applicable |
| preferred_date | date | yes | YYYY-MM-DD format |
| duration | text | no | Pre-filled per experience |
| guest_count | number | yes | |
| occasion | select | yes | Bachelorette / Birthday / Girls Trip / Anniversary / Corporate / Other |
| boarding_location | text | no | Pre-filled per experience/city |
| city | text | yes | Miami / Fort Lauderdale |
| add_ons | text | no | Comma-separated |
| special_requests | textarea | no | |

### Hidden Fields (required for attribution)

| Field Name | Source | Populated By |
|------------|--------|-------------|
| source_url | window.location.href | JS on form load |
| utm_source | URL param | JS on form load |
| utm_medium | URL param | JS on form load |
| utm_campaign | URL param | JS on form load |
| utm_content | URL param | JS on form load |
| utm_term | URL param | JS on form load |
| page_slug | path | JS on form load |
| session_id | sessionStorage | JS on form load |

---

## AIRTABLE FIELD MAPPING

| Form Field | Airtable Field | Table |
|------------|----------------|-------|
| first_name | First Name | Requests |
| last_name | Last Name | Requests |
| email | Email | Requests |
| phone | Phone | Requests |
| experience | Experience | Requests |
| yacht | Yacht | Requests |
| preferred_date | Preferred Date | Requests |
| duration | Duration | Requests |
| guest_count | Guest Count | Requests |
| occasion | Occasion | Requests |
| boarding_location | Boarding Location | Requests |
| city | City | Requests |
| add_ons | Add-Ons Selected | Requests |
| special_requests | Special Requests | Requests |
| source_url | Source URL | Requests |
| utm_source | UTM_Source | Requests |
| utm_medium | UTM_Medium | Requests |
| utm_campaign | UTM_Campaign | Requests |

Auto-populated by Make on record creation:
- Status: "NEW"
- Environment: "Production"
- Source_System: "Make"
- Brand: Derived from source_url (SSS vs ME)
- Idempotency_Key: "LEAD-{email}-{date}-{guest_count}"

---

## NAMING CONVENTIONS

### Experience Names (canonical)
Use these exact strings in the experience hidden field. Airtable and Make depend on consistency.

| Page | Experience Value |
|------|-----------------|
| Pink Palm Club | Pink Palm Club |
| Sunset Sailing | Sunset Sailing Charter |
| Bachelorette Experience | Bachelorette Charter |
| Birthday Experience | Birthday Charter |
| Corporate / Mare | Mare Executive Charter |

### UTM Convention

| Parameter | Convention | Example |
|-----------|------------|---------|
| utm_source | Platform name | instagram / google / meta |
| utm_medium | Channel | paid_social / organic / email |
| utm_campaign | Campaign code | sss-ppc-q2-2026 |
| utm_content | Creative ID | hero-video-1 |

---

## MAKE SCENARIO DEPENDENCIES

The SSS-LEAD-INTAKE scenario (M-LEAD-INTAKE.json) must receive the following or it fails to route correctly:

1. email (required for idempotency check)
2. preferred_date (required for idempotency check)
3. guest_count (required for idempotency check)
4. source_url (required for brand detection: SSS vs ME)

All other fields are additive. Missing them does not break the scenario but reduces Airtable record quality.

---

## QA WEBHOOK ENDPOINT

For testing form submissions without creating live records:
Use the TEST_PORTAL.html in the repo root, pointed at a Make sandbox scenario.

Never submit test records to the production webhook.

---

## IDEMPOTENCY RULES

Duplicate submissions are blocked by a Make filter that checks:
FIND("LEAD-{email}-{date}-{guest_count}", {Idempotency_Key})

If a match is found, the new record is not created and the email is not sent. This prevents double-sends on Webflow form re-submissions.

---

## AUTOMATION HEALTH

After any form change or page deploy, verify:
1. Test submission reaches Airtable Requests table with correct field mapping
2. Confirmation email is received within 60 seconds
3. Slack ops alert appears in #sss-ops-alerts
4. Record Status = "NEW"
5. Brand field = "SSS" (not blank, not "ME")
