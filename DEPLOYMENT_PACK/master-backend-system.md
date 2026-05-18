# SHE SAID SAIL
# MASTER BACKEND SYSTEM

STATUS: PRODUCTION
VERSION: v1.0
APPLIES TO: All web forms — shesaidsail.com

---

## FORM FIELD NAMING CONVENTIONS

All Webflow form fields must use these exact names.
These map directly to Make.com SSS-LEAD-INTAKE webhook fields.

### Visible Fields

| Field Name (HTML name attr) | Label | Type | Required |
|----------------------------|-------|------|----------|
| first_name | First name | text | yes |
| last_name | Last name | text | yes |
| email | Email | email | yes |
| phone | Phone | tel | no |
| experience | Experience | select | yes |
| yacht | Yacht preference | select | no |
| duration | Duration | select | no |
| preferred_date | Preferred date | date | yes |
| guest_count | Number of guests | number | yes |
| occasion | Occasion | select | yes |
| boarding_location | Boarding location | select | no |
| add_ons | Add-ons | checkbox group | no |
| special_requests | Special requests | textarea | no |
| city | City | hidden (auto-set) | no |

### Hidden Fields (auto-populated via JS)

| Field Name | Source | Purpose |
|------------|--------|---------|
| source_url | window.location.href | Attribution |
| utm_source | URL param utm_source | Campaign tracking |
| utm_medium | URL param utm_medium | Channel tracking |
| utm_campaign | URL param utm_campaign | Campaign name |
| utm_content | URL param utm_content | Creative tracking |
| utm_term | URL param utm_term | Keyword tracking |
| page_name | Static, set per page | Identifies origin page |
| brand | Static "SSS" | Brand identification |

---

## AIRTABLE FIELD MAPPING

Webhook field -> Airtable Requests table field

| Webhook Field | Airtable Field | Notes |
|---------------|----------------|-------|
| first_name | First Name | |
| last_name | Last Name | |
| email | Email | |
| phone | Phone | |
| experience | Experience | |
| yacht | Yacht | |
| duration | Duration | |
| preferred_date | Preferred Date | |
| guest_count | Guest Count | |
| occasion | Occasion | |
| boarding_location | Boarding Location | |
| add_ons | Add-Ons Selected | |
| special_requests | Special Requests | |
| city | City | |
| source_url | (logged to Make audit) | |
| utm_source | (logged to Make audit) | |

Auto-set by Make:
| Airtable Field | Value |
|----------------|-------|
| Status | NEW |
| Environment | Production |
| Source_System | Make |
| Brand | SSS |
| Idempotency_Key | LEAD-{email}-{preferred_date}-{guest_count} |

---

## MAKE.COM INTEGRATION

Webhook: SSS_LEAD_INTAKE_HOOK
Scenario: SSS-LEAD-INTAKE
Trigger: Webflow form submission

Flow:
1. Receive webhook from Webflow form
2. Deduplicate check against Requests table (Idempotency_Key)
3. Create Airtable record if not duplicate
4. Send auto-reply email via Gmail
5. Post Slack alert to #sss-ops-alerts
6. Log to audit trail

---

## EXPERIENCE OPTIONS

These must match exactly between form selects and Airtable values:

| Form Display | Value |
|-------------|-------|
| Rose Day Club | Rose Day Club |
| Private Charter | Private Charter |
| Bachelorette Package | Bachelorette Package |
| Birthday Experience | Birthday Experience |
| Girls Trip | Girls Trip |
| Corporate Outing | Corporate Outing |

---

## OCCASION OPTIONS

| Form Display | Value |
|-------------|-------|
| Bachelorette | Bachelorette |
| Birthday | Birthday |
| Girls Trip | Girls Trip |
| Anniversary | Anniversary |
| Corporate | Corporate |
| Other Celebration | Other Celebration |

---

## UTM PRESERVATION

All pages must capture UTM parameters on load and store in:
1. Hidden form fields (for immediate submission capture)
2. sessionStorage (for cross-page preservation)

Script handles:
- utm_source, utm_medium, utm_campaign, utm_content, utm_term
- Fallback: check sessionStorage if not in URL

---

## IDEMPOTENCY

Duplicate prevention key: LEAD-{email}-{preferred_date}-{guest_count}

If duplicate detected by Make filter: skip Airtable write, skip email, skip Slack. Log to audit only.

---

## CONTACT INFORMATION

Email: hello@shesaidsail.com
Phone: (754) 701-2228
Address: 1314 East Las Olas Blvd #2597, Fort Lauderdale, FL 33301
Airtable Base: appdZ49WqgjRXxA1R (She Said Sail)
Requests Table: tblTlSB9CO4dTGodg
