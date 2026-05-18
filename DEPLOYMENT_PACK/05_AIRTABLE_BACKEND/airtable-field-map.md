# She Said Sail: Airtable Field Map

Quick reference for mapping every form field to the correct Airtable table and field. Use this alongside `airtable-table-schema.md` when configuring Make.com modules.

---

## REQUESTS TABLE: Form Fields to Airtable Fields

| Form Field | Airtable Field Name | Field Type | Notes |
|---|---|---|---|
| Full Name | Name | Short Text | Primary field |
| Email | Email | Email | Required |
| Phone | Phone | Phone | Required |
| Occasion (select) | Occasion | Single Select | Options: Bachelorette, Birthday, Girls Trip, Celebration, Corporate, Other |
| Group Size | Group Size | Number | Integer only |
| Preferred Date | Preferred Date | Date | ISO 8601 format |
| Flexible Dates (checkbox) | Flexible Dates | Checkbox | true/false |
| Experience Interest (multi-select) | Experience Interest | Multiple Select | Options: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom, Undecided |
| Message | Notes | Long Text | Free text from form textarea |
| Selected Experience (from URL param) | Experience Interest | Multiple Select | Pre-populate from `?experience=` URL param; merge with user selection |

---

## HIDDEN TRACKING FIELDS: UTMs Table (Linked to Requests)

Each form submission creates one linked UTM record. The Requests table holds a Linked Record field pointing to the UTMs table.

| Hidden Form Field | Airtable Field Name | Field Type | Notes |
|---|---|---|---|
| utm_source | UTM Source | Short Text | e.g., meta, google, instagram |
| utm_medium | UTM Medium | Short Text | e.g., cpc, organic, email |
| utm_campaign | UTM Campaign | Short Text | e.g., summer-2026-bachelorette |
| utm_content | UTM Content | Short Text | e.g., video-reel-v4 |
| utm_term | UTM Term | Short Text | Keyword; blank for social |
| creative_id | Creative ID | Short Text | e.g., CRE-052 |
| landing_page | Landing Page | URL | Full URL including query string |
| source_url | Source URL | URL | Same as landing_page on first touch |
| referrer_url | Referrer URL | URL | document.referrer at form load |
| first_seen_at | First Seen At | Date/Time | ISO 8601, UTC |
| submission_page | Submission Page | Short Text | Pathname only, e.g., /request-to-book/ |
| brand | Brand | Short Text | Hard-coded: shesaidsail |
| service_category | Service Category | Short Text | Hard-coded: yacht-charter |

---

## FIELDS AUTO-SET BY MAKE.COM (Not from the form)

These fields are written by Make.com after it receives the webhook payload. Do not include them in the HTML form.

| Airtable Field | Table | Value Set By Make | Condition |
|---|---|---|---|
| Status | Requests | "New" | Always, on record create |
| Submitted At | Requests | now() (UTC timestamp) | Always, on record create |
| Internal Rating | Requests | "Warm" (default) | Default on create |
| Internal Rating | Requests | "Hot" | Override if: Occasion = Bachelorette OR Group Size >= 15 |
| Contact Linked | Requests | Linked record ID from Contacts | Make looks up or creates Contact by email, then links |
| Audit Entry | Audit Log | New record: action="form_submission" | Always, on record create |

---

## CONTACTS TABLE: Email Capture (Homepage Form)

| Form Field | Airtable Field Name | Field Type | Notes |
|---|---|---|---|
| Email | Email | Email | Primary identifier for deduplication |
| utm_source | UTM Source | Short Text | From hidden field |
| utm_medium | UTM Medium | Short Text | From hidden field |
| utm_campaign | UTM Campaign | Short Text | From hidden field |
| landing_page | Landing Page | URL | Page where email was captured |

Fields set by Make.com for email capture:

| Airtable Field | Value |
|---|---|
| Email Subscribed | true (Checkbox) |
| Source | "email-capture-form" |
| Created At | now() |
| Brand | shesaidsail |

---

## NOTES

- The UTMs table is a separate table linked via a Linked Record field in Requests. This allows one Contact to have multiple UTM touch records over time.
- Do not store raw UTM params directly on the Requests table as Short Text fields. Always create a UTM record and link it.
- The `experience_interest` field is a Multiple Select. If a user selects multiple experiences on the form, pass them as an array to Make.com, and Make.com writes all values to the field.
- If `selected_experience` arrives from the URL param and `experience_interest` is also filled by the user, merge both into the array before writing to Airtable (Make.com router handles the merge logic).
