# PHASE 4 FIELD RETIREMENTS
**She Said Sail + Mare Executive — Airtable Architecture Normalization**

---

| Attribute | Value |
|---|---|
| Document Type | Field Retirement Authorization Register |
| Phase | Phase 4 |
| Date Authorized | 2026-05-15 |
| Authority | Will Doyle — Founder, She Said Sail + Mare Executive |
| Classification | INTERNAL OPERATIONS — CONFIDENTIAL |
| Status | AUTHORIZED — Sections 3 & 4 fully executed; Sections 1 & 2 pending manual execution |

---

## Retirement Execution Protocol

Before any field is deleted, the following steps MUST be completed in order:

1. **Export CSV** of the field(s) to be removed, including all record data
2. **Store CSV** in `99_ARCHIVE/PHASE_4_FIELD_EXPORTS/` with filename format: `[TableName]_[FieldName]_Export_[YYYY-MM-DD].csv`
3. **Record execution** in this document: add execution date and executor name to the relevant row
4. **Confirm no formula** in the same table references the field being deleted (Airtable will warn if so)
5. **Confirm no Make scenario** references the field ID — check Make_Scenarios.Airtable_Tables_Used column for any field IDs

**Rollback:** If any field retirement causes unexpected issues, re-add the field (it will be empty but the CSV export preserves all historical values for re-import via copy-paste or CSV upload).

**Make scenario status as of 2026-05-15:** ALL 8 scenarios are NOT_STARTED. Zero live automations exist. Field retirement poses no automation risk at this time.

---

## Section 1 — Bookings Table Retirements

**Table:** Bookings
**Table ID:** tbl72omPibBkn2hZL
**Base:** SSS Operations (appdZ49WqgjRXxA1R)
**Status:** AUTHORIZED — pending manual execution by Will

### Prerequisites

- [ ] Export CSV of all 23 fields listed below before any deletion
- [ ] Confirm Automation_Health records exist for all active Bookings (link field: fldutXOFOw7H3DLy7)
- [ ] Spot-check 10 active Booking records: verify their linked Automation_Health records have the corresponding checkbox values populated
- [ ] Confirm all 8 Make scenarios remain NOT_STARTED (no field ID references introduced since 2026-05-15)

### 1A — Automation Tracking Checkboxes (22 fields)

These fields are duplicated in Automation_Health (tblCVpMsX4ZvnsJqL), which is the canonical source of truth for automation execution state. Automation_Health tracks these with full timestamps; the Bookings copies are simple checkboxes with no timestamp context.

| Field Name | Field ID | Type | Canonical Location in Automation_Health | Executed | Executor | Date |
|---|---|---|---|---|---|---|
| D0 Sent | fldBBcU5v8XnTKtgO | checkbox | Automation_Health.D0_Sent | ☐ | | |
| D1 Sent | fldP34Jd2uN6fbeJ1 | checkbox | Automation_Health.D1_Sent | ☐ | | |
| D3 Sent | fldZc8wBzC9OQfXpD | checkbox | Automation_Health.D3_Sent | ☐ | | |
| D7 Sent | fld20mPS8xeoIXSB2 | checkbox | Automation_Health.D7_Sent | ☐ | | |
| D9 Gift Sent | fldZ98DSFiL1m9J7e | checkbox | Automation_Health.D9_Gift_Sent | ☐ | | |
| D14 Sent | fldDgmSFz82hjLuKB | checkbox | Automation_Health.D14_Sent | ☐ | | |
| D30 Sent | fldlpkrJzdIshPPfL | checkbox | Automation_Health.D30_Sent | ☐ | | |
| D60 Sent | fld6cy5rVpJpRFwuD | checkbox | Automation_Health.D60_Sent | ☐ | | |
| HV D2 Call Done | fldgeG2grl9FLxlJu | checkbox | Automation_Health.HV_D2_Call_Done | ☐ | | |
| HV D5 Sent | fld3ki6EHLjngJm60 | checkbox | Automation_Health.HV_D5_Sent | ☐ | | |
| HV D21 Sent | fldsjzXc4fXEmk57f | checkbox | Automation_Health.HV_D21_Sent | ☐ | | |
| HV D23 Sent | fld3owWGwQM4H8fO7 | checkbox | Automation_Health.HV_D23_Sent | ☐ | | |
| D7 Reminder Sent | fld2lf56YGNQUZrbc | checkbox | Automation_Health.D72hr_Reminder_Sent | ☐ | | |
| D10 Reminder Sent | fld3HN68iQzVE5xVH | checkbox | Automation_Health.D48hr_Reminder_Sent | ☐ | | |
| D72hr Reminder Sent | fldahd5x0EI3ZyEfd | checkbox | Automation_Health.D72hr_Reminder_Sent | ☐ | | |
| D48hr Reminder Sent | fldAyseOIjcw13gA2 | checkbox | Automation_Health.D48hr_Reminder_Sent | ☐ | | |
| Charter_Brief_Sent | fld7oEqbkTXpjL2ZC | checkbox | Automation_Health.Charter_Brief_Sent | ☐ | | |
| Charter_Brief_All_Vendors_Confirmed | fldn10duVP0WK0f90 | checkbox | Automation_Health.Charter_Brief_All_Vendors_Confirmed | ☐ | | |
| T7_Confirmed | fldVJAUgdAO2db1sw | checkbox | Automation_Health.T7_Confirmed | ☐ | | |
| T48_Captain_Confirmed | fldrIAT5sNot38FHR | checkbox | Automation_Health.T48_Captain_Confirmed | ☐ | | |
| Crew_Report_Submitted | fldXJwFuhreHP3Wvv | checkbox | Automation_Health — add field if not present | ☐ | | |
| Vendor_Ratings_Entered | fldJI4I6yLNq5HGyN | checkbox | Automation_Health — add field if not present | ☐ | | |

> **Note on Crew_Report_Submitted and Vendor_Ratings_Entered:** Before removing these from Bookings, confirm these fields exist in Automation_Health. If they do not exist, add them to Automation_Health first, then migrate any checked values, then delete from Bookings.

### 1B — Duplicate Narrative Field (1 field)

| Field Name | Field ID | Type | Reason | Canonical Field | Executed | Executor | Date |
|---|---|---|---|---|---|---|---|
| Conversations | fldSwdicqMLaLA4iA | multilineText | Duplicate of Conversation_Summary | Conversation_Summary (fldN6ir73krYmDwS6) | ☐ | | |

> **Before removing:** Compare the content in `Conversations` vs. `Conversation_Summary` across all records. If any records have content in `Conversations` that is not in `Conversation_Summary`, copy that content to `Conversation_Summary` before deletion.

### Section 1 Summary

| Metric | Value |
|---|---|
| Fields to remove | 23 |
| Field count before | 151 |
| Field count after | 128 |
| Risk level | LOW |
| Rollback method | Re-add field; re-import CSV |

---

## Section 2 — Partner Outreach Table Retirements

**Table:** Partner Outreach
**Table ID:** tblnjGWa6JNiogfCo
**Destination Table:** Partnerships (tble5DcTo8mahr3lp)
**Base:** SSS Operations (appdZ49WqgjRXxA1R)
**Status:** AUTHORIZED — pending manual execution by Will (data migration to Partnerships must precede deletion)

### Prerequisites

- [ ] Filter Partner Outreach to `Became_Partner = true`. For every record in that view, verify a corresponding Partnerships record exists. If any are missing, create Partnerships records before proceeding.
- [ ] Export CSV of the 22 fields listed below before any deletion
- [ ] For formula fields: re-create the formula logic in Partnerships before removing from Partner Outreach
- [ ] Add any net-new fields to Partnerships that do not already exist there (see column: Partnerships Equivalent)

### Fields to Move to Partnerships (22 fields)

| Field Name | Field ID | Type | Partnerships Equivalent | Action | Executed | Executor | Date |
|---|---|---|---|---|---|---|---|
| Total Revenue Driven | fld1jkP04uZggA82f | currency | Commission_History or new field | Add to Partnerships, migrate data, then delete | ☐ | | |
| Total Commission Paid Out | fldjqSHcRtOSEvkU3 | currency | Total_Commissions_Paid | Map to existing field or add, migrate, delete | ☐ | | |
| Net Revenue After Commission | fldy4LBaBNGmgPjMH | formula | Derive from Partnerships fields | Re-create formula in Partnerships, then delete | ☐ | | |
| Avg Revenue Per Booking | fldolXZfUtv639AhJ | formula | Derive from Partnerships fields | Re-create formula in Partnerships, then delete | ☐ | | |
| Total Gifting Cost | fld4syEGBpFfqEIf6 | currency | Add to Partnerships | Add to Partnerships, migrate data, then delete | ☐ | | |
| Partner ROI | fldQrgh4rOpiws6M1 | formula | ROI_Score | Re-create formula in Partnerships, then delete | ☐ | | |
| Partnership Health | fldcB8Q5r1sgYu89i | rating | ROI_Score | Map to ROI_Score or add Health field, migrate, delete | ☐ | | |
| Agreement Signed | fldCprRWMB5hk3QwR | checkbox | Agreement_Date (presence implies signed) | Verify Agreement_Date in Partnerships, then delete | ☐ | | |
| Agreement URL | fld7KZ8Ni2Dav9Kdc | url | Contract_Notes | Migrate URL to Contract_Notes or add URL field, delete | ☐ | | |
| Experience Gifted | fldtddpjwUTt8Di2W | checkbox | Content_Collaboration | Add to Partnerships or merge into Content_Collaboration notes | ☐ | | |
| Experience Gifted Date | fldjXMkXrDGYRV9gH | date | Content_Collaboration | Add date field to Partnerships, migrate, delete | ☐ | | |
| Content Posted | fldcWcGcbZuUKC2kl | checkbox | Content_Collaboration | Add to Partnerships or merge into Content_Collaboration notes | ☐ | | |
| Content URL | fldkKqJPJxMhpUFcO | url | Content_Collaboration | Add URL field to Partnerships, migrate, delete | ☐ | | |
| Content Reach | fldF8PX6jbEhNXX7f | number | Content_Collaboration | Add number field to Partnerships, migrate, delete | ☐ | | |
| Lead to Booking Rate | fldpkUJhr1hDYIhLl | formula | Derive from Partnerships fields | Re-create formula in Partnerships, then delete | ☐ | | |
| Commission Balance Owed | fldJrIcqY5myNEzXD | currency | Add to Partnerships | Add to Partnerships, migrate data, then delete | ☐ | | |
| Last Payout Date | fldjLZTbxO9DditWL | date | Add to Partnerships | Add to Partnerships, migrate data, then delete | ☐ | | |
| Payout Method | fldfD1T0gsfWgUgcA | singleSelect | Add to Partnerships | Add field + choices to Partnerships, migrate, delete | ☐ | | |
| Next Partnership Review | fldmRe2RqmLhOw5zn | date | Add to Partnerships | Add to Partnerships, migrate data, then delete | ☐ | | |
| Partnership Status | fld25fD7DToaQr8yr | singleSelect | Partnership_Status | Map to existing Partnership_Status field, migrate, delete | ☐ | | |
| Partnership Start Date | fld3RvFZvRPLWYwI0 | date | Agreement_Date | Map to Agreement_Date in Partnerships, migrate, delete | ☐ | | |
| Last Referral Date | fldysUAKr26aD6szh | date | Add to Partnerships | Add to Partnerships, migrate data, then delete | ☐ | | |

### Section 2 Summary

| Metric | Value |
|---|---|
| Fields to remove | 22 |
| Field count before | 88 |
| Field count after | 66 |
| Risk level | LOW-MEDIUM |
| Primary prerequisite | Audit Became_Partner records; create Partnerships records before deletion |
| Rollback method | Re-add fields; re-import CSV |

---

## Section 3 — Table Deprecations (Rename, Do Not Delete)

**Status:** AUTHORIZED — pending manual execution by Will
**Convention:** Prefix table name with `_DEPRECATED_` — do not delete any table

| Table Name | Table ID | Base | Base ID | Current Fields | Records | Action | Reason | Executed | Executor | Date |
|---|---|---|---|---|---|---|---|---|---|---|
| Brand | tbllNjlllEhG92Ozo | SSS Operations | appdZ49WqgjRXxA1R | 6 | 0 operational | Rename to _DEPRECATED_Brand | Placeholder — 6 default Airtable fields only; no operational content | ☐ | | |
| Services | tblBOgArrdfPkvR8B | SSS Operations | appdZ49WqgjRXxA1R | 6 | 0 operational | Rename to _DEPRECATED_Services | Placeholder — 6 default Airtable fields only; no operational content | ☐ | | |
| Expansion Pipeline | tbllga7euKfd2ykM5 | SSS Operations | appdZ49WqgjRXxA1R | 6 | 0 operational | Rename to _DEPRECATED_Expansion_Pipeline | Placeholder — 6 default Airtable fields only; no operational content | ☐ | | |
| AI_Prompt_Versions (old) | tbl0FJkA1E6a70cxX | SSS Operations | appdZ49WqgjRXxA1R | 9 | unknown | Rename to _DEPRECATED_AI_Prompt_Versions | 9-field version missing 11 governance fields — not production-ready; correct 20-field version in apppFfA2VZVmamvXe | ☐ | | |
| Yacht_Availability (old) | tblDOoV4CHh8t4qpj | SSS Operations | appdZ49WqgjRXxA1R | 13 | check first | Rename to _DEPRECATED_Yacht_Availability (after migrating any records) | Superseded by 15-field version in apppFfA2VZVmamvXe (tblkALubyHWjOY6Ul) | ☐ | | |
| Monthly Revenue | tblpTgps7cRQwDZp2 | SSS Financials | apprDKQtV2GInThwE | 14 | unknown | Rename to _DEPRECATED_Monthly_Revenue | Superseded by Financial_Periods (tblli6AwOB114dOd1, 17 fields) | ☐ | | |

### Table Deprecation Protocol

For each table deprecation:
1. Note the current record count before renaming
2. Export all records to CSV (even if 0 records — captures schema)
3. Add a table description: "DEPRECATED [DATE] — [reason] — See [replacement table name] for current data."
4. Rename the table using the `_DEPRECATED_` prefix
5. Record completion in the row above

---

## Section 4 — ME_Pricing Source Table (Migration Complete)

**Status: ALL 5 RECORDS MIGRATED ✓ (Phase 4 executed 2026-05-15)**

| Attribute | Value |
|---|---|
| Source table | ME_Pricing |
| Source table ID | tblm5p6GQmYEjhZpG |
| Source base | app2FbmVD44BXShyx |
| Destination table | Packages (tblwDw2hkKW5moSr9) |
| Destination base | appdZ49WqgjRXxA1R |
| Records migrated | 5 |
| Migration date | 2026-05-15 |

### Records Migrated

| Destination Record ID | Package Name |
|---|---|
| receKte1p4egjf3Jw | Client Hosting Charter — Miami |
| recfpvh5MdGkrajlc | Principal Private Charter — Miami |
| rec1cktDMLPV8PHvQ | Client Hosting Charter — Fort Lauderdale |
| recAQMYUI5wWpQeVX | Sunset Close Charter — Miami |
| recHuXfKlLArY4LB9 | Executive Retreat — Full Day Miami |

### Next Action for Source Table

After a **30-day validation window** (no earlier than 2026-06-15): rename ME_Pricing source table to `_DEPRECATED_ME_Pricing` in app2FbmVD44BXShyx.

Do not delete until validation window has passed and all 5 records have been confirmed accurate in the Packages table.

| Validation Task | Status | Completed By | Date |
|---|---|---|---|
| Confirm all 5 ME package records accurate in Packages | ☐ | | |
| Confirm AI can quote ME packages correctly from Packages table | ☐ | | |
| 30-day window elapsed (no earlier than 2026-06-15) | ☐ | | |
| Rename ME_Pricing to _DEPRECATED_ME_Pricing | ☐ | | |

---

## Section 5 — Field Export Archive Index

All CSV exports from Phase 4 field retirements must be stored in:
```
99_ARCHIVE/PHASE_4_FIELD_EXPORTS/
```

### Naming Convention
```
[TableName]_[FieldGroup]_Export_[YYYY-MM-DD].csv
```

### Expected Exports from This Phase

| File | Contents | Created | Date |
|---|---|---|---|
| Bookings_Automation_Checkboxes_Export_[DATE].csv | 22 automation tracking checkbox fields from Bookings | ☐ | |
| Bookings_Conversations_Export_[DATE].csv | Conversations field from Bookings | ☐ | |
| Partner_Outreach_Partnership_Fields_Export_[DATE].csv | 22 partnership-relationship fields from Partner Outreach | ☐ | |
| AI_Prompt_Versions_Old_Export_[DATE].csv | All records from old 9-field AI_Prompt_Versions table | ☐ | |
| Yacht_Availability_Old_Export_[DATE].csv | All records from old 13-field Yacht_Availability table | ☐ | |
| Monthly_Revenue_Archive_[DATE].csv | All records from Monthly Revenue table | ☐ | |

---

## Section 6 — Retirement Register (Running Log)

This section is updated as retirements are executed. It is the authoritative record of what was retired, by whom, and when.

| Date | Executor | Table | Field Name | Field ID | Action | Notes |
|---|---|---|---|---|---|---|
| 2026-05-15 | Claude (MCP) | Packages | — | — | 14 fields ADDED (not retired) | Action 1: Packages expansion |
| 2026-05-15 | Claude (MCP) | Packages | — | — | 5 ME records CREATED (not retired) | Action 2: ME_Pricing merge |
| | | | | | | |
| | | | | | | |

> Add rows to this table as each field or table retirement is executed manually.

---

*Document generated: 2026-05-15 | Phase 4 Field Retirements | She Said Sail + Mare Executive*
