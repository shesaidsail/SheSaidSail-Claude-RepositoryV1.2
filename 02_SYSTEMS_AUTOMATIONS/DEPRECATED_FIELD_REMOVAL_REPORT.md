# DEPRECATED_FIELD_REMOVAL_REPORT.md
## She Said Sail + Mare Executive — Deprecated Field Removal Documentation

**Phase:** Final Pre-Make Cleanup — Task 6  
**Execution Date:** 2026-05-16  
**Tables:** Bookings (tbl72omPibBkn2hZL), Partner Outreach (tblnjGWa6JNiogfCo)  
**Base:** appdZ49WqgjRXxA1R (SSS Operations)  
**Status:** DOCUMENTED — DELETION NOT EXECUTED (Will authorization required)  
**Classification:** Confidential — Internal Use Only

---

## CRITICAL PREREQUISITE — CSV EXPORT REQUIRED FIRST

**The Airtable MCP tools do not include a CSV or bulk export function.**

Will must manually export CSV backups before any field deletion:
1. Open appdZ49WqgjRXxA1R
2. Navigate to Bookings table → Grid view → Download CSV
3. Navigate to Partner Outreach table → Grid view → Download CSV
4. Store both CSVs in a dated backup folder before proceeding with deletion
5. Deletion of Airtable fields is IRREVERSIBLE — no undo after confirmation

**NO FIELDS WERE DELETED IN THIS SESSION. This report documents which fields are candidates for removal and why.**

---

## SECTION 1 — BOOKINGS TABLE (tbl72omPibBkn2hZL)

**Current field count:** 151  
**Target field count after cleanup:** ~128 (remove 23 deprecated automation tracking + operational audit fields)  
**Build spec target:** 70 fields (full extraction requires Phase 4 financial field migration)

### 1.1 — Automation Tracking Fields (20 fields) → Extract to Automation_Health

These fields track whether each automated touchpoint was sent. The Automation_Health table (tblCVpMsX4ZvnsJqL) now exists and is linked to Bookings via fldutXOFOw7H3DLy7. These fields should live in one Automation_Health record per Booking, not on the Booking record itself.

**Deletion prerequisite:** Automation_Health table must be fully populated with linked records mirroring current checkbox states for all Bookings BEFORE these fields are removed.

| Field Name | Field ID | Type | Extract To |
|---|---|---|---|
| D0 Sent | fldBBcU5v8XnTKtgO | checkbox | Automation_Health |
| D1 Sent | fldP34Jd2uN6fbeJ1 | checkbox | Automation_Health |
| D3 Sent | fldZc8wBzC9OQfXpD | checkbox | Automation_Health |
| D7 Sent | fld20mPS8xeoIXSB2 | checkbox | Automation_Health |
| D9 Gift Sent | fldZ98DSFiL1m9J7e | checkbox | Automation_Health |
| D14 Sent | fldDgmSFz82hjLuKB | checkbox | Automation_Health |
| D30 Sent | fldlpkrJzdIshPPfL | checkbox | Automation_Health |
| D60 Sent | fld6cy5rVpJpRFwuD | checkbox | Automation_Health |
| HV D2 Call Done | fldgeG2grl9FLxlJu | checkbox | Automation_Health |
| HV D5 Sent | fld3ki6EHLjngJm60 | checkbox | Automation_Health |
| HV D21 Sent | fldsjzXc4fXEmk57f | checkbox | Automation_Health |
| HV D23 Sent | fld3owWGwQM4H8fO7 | checkbox | Automation_Health |
| D10 Reminder Sent | fld3HN68iQzVE5xVH | checkbox | Automation_Health |
| D7 Reminder Sent | fld2lf56YGNQUZrbc | checkbox | Automation_Health |
| D72hr Reminder Sent | fldahd5x0EI3ZyEfd | checkbox | Automation_Health |
| D48hr Reminder Sent | fldAyseOIjcw13gA2 | checkbox | Automation_Health |
| Charter_Brief_Sent | fld7oEqbkTXpjL2ZC | checkbox | Automation_Health |
| Charter_Brief_All_Vendors_Confirmed | fldn10duVP0WK0f90 | checkbox | Automation_Health |
| T7_Confirmed | fldVJAUgdAO2db1sw | checkbox | Automation_Health |
| T48_Captain_Confirmed | fldrIAT5sNot38FHR | checkbox | Automation_Health |

**Subtotal: 20 fields**

### 1.2 — Operational Audit Fields (3 fields) → Extract to Operational_Audits

These fields track post-charter operational data. Per the build spec, this data belongs in a linked Operational_Audits record, not on the Booking itself. The Operational_Audits table (tblAHYfl31529xUGr) exists.

**Deletion prerequisite:** Charter data from these fields must be migrated to linked Operational_Audits records for all completed Bookings BEFORE these fields are removed.

| Field Name | Field ID | Type | Extract To | Note |
|---|---|---|---|---|
| Crew Report | fldhjHjBRRX794aaT | multilineText | Operational_Audits | Keep Charter_Grade (fldmAWa2yufOas9GT) — build spec says retain |
| Crew_Report_Submitted | fldXJwFuhreHP3Wvv | checkbox | Operational_Audits | |
| Charter_NPS | fldjh7c7F1jjAyPrO | rating | Operational_Audits | |

**Subtotal: 3 fields**

**Total Bookings deprecated fields: 23**

### 1.3 — Financial Fields (12 fields) — Phase 4 Extraction

These are NOT in the 23-field deletion scope for this phase. They require Phase 4 P&L Per Charter (Financial base) migration with Make scenario FINANCIAL-001. Documented here for completeness.

| Field Name | Field ID | Type | Phase 4 Action |
|---|---|---|---|
| Net Profit | fldo5UE1UGJHBbj44 | formula | Sync to P&L Per Charter via Make |
| Margin Pct | fldClbWCv5IhDVW46 | formula | Sync to P&L Per Charter via Make |
| Boat Cost | fldrBwR524ljnWpEl | currency | Sync to P&L Per Charter |
| Labor Cost | fldG8mfttezq7rBQT | currency | Sync to P&L Per Charter |
| F&B Cost | fldsAE2ldBsJGPcKx | currency | Sync to P&L Per Charter |
| City Manager Payout | fldNR8IzoWy5iluyb | currency | Sync to P&L Per Charter |
| Referral Commission | fldCZMlZ451FI1dih | currency | Sync to P&L Per Charter |
| Tax Collected | fldXGYVsNHQhLKEoN | currency | Sync to P&L Per Charter |
| Total Cost | fldxszt7eYR7Q1cd5 | formula | Sync to P&L Per Charter |
| City Manager Payout Auto | fldaMeVzkymtTtO1H | formula | Sync to P&L Per Charter |
| Referral Commission Auto | fldWFTpuk7neZh5xi | formula | Sync to P&L Per Charter |
| Revenue Per Guest | fldwKbRboqJ1pFq8w | formula | Sync to P&L Per Charter |

---

## SECTION 2 — PARTNER OUTREACH TABLE (tblnjGWa6JNiogfCo)

**Current field count:** 88  
**Target field count after cleanup:** 66 (remove 22 relationship intelligence fields)  
**Build spec target:** 45 fields (full reduction is a separate Phase 4 scope item)

### 2.1 — Partnership Relationship Fields (22 fields) → Now Live in Partnerships Table

The Partnerships table (tble5DcTo8mahr3lp) was created during Phase 3 migration. Partner Outreach is now linked to Partnerships via field fldk0HofCtGpVKDtc. The following fields contain relationship intelligence data that belongs in Partnerships, not in the outreach pipeline table.

**Deletion prerequisite:** All field data must be migrated to linked Partnerships records BEFORE removal. Will must verify the Partnerships table schema can receive each field, then run a migration (manually or via Make) before deleting.

| Field Name | Field ID | Type | Extract To |
|---|---|---|---|
| Became Partner | fldXdQSdM5yKSdZGP | checkbox | Partnerships |
| Partnership Start Date | fld3RvFZvRPLWYwI0 | date | Partnerships |
| Partnership Status | fld25fD7DToaQr8yr | singleSelect | Partnerships |
| Total Revenue Driven | fld1jkP04uZggA82f | currency | Partnerships |
| Total Commission Paid Out | fldjqSHcRtOSEvkU3 | currency | Partnerships |
| Net Revenue After Commission | fldy4LBaBNGmgPjMH | formula | Partnerships (recalculates) |
| Avg Revenue Per Booking | fldolXZfUtv639AhJ | formula | Partnerships (recalculates) |
| Total Gifting Cost | fld4syEGBpFfqEIf6 | currency | Partnerships |
| Partner ROI | fldQrgh4rOpiws6M1 | formula | Partnerships (recalculates) |
| Last Referral Date | fldysUAKr26aD6szh | date | Partnerships |
| Partnership Health | fldcB8Q5r1sgYu89i | rating | Partnerships |
| Agreement Signed | fldCprRWMB5hk3QwR | checkbox | Partnerships |
| Agreement URL | fld7KZ8Ni2Dav9Kdc | url | Partnerships |
| Experience Gifted | fldtddpjwUTt8Di2W | checkbox | Partnerships |
| Experience Gifted Date | fldjXMkXrDGYRV9gH | date | Partnerships |
| Content Posted | fldcWcGcbZuUKC2kl | checkbox | Partnerships |
| Content URL | fldkKqJPJxMhpUFcO | url | Partnerships |
| Content Reach | fldF8PX6jbEhNXX7f | number | Partnerships |
| Leads Generated | fldafz9wGetN5PVOZ | number | Partnerships |
| Lead to Booking Rate | fldpkUJhr1hDYIhLl | formula | Partnerships (recalculates) |
| Commission Balance Owed | fldJrIcqY5myNEzXD | currency | Partnerships |
| Payout Method | fldfD1T0gsfWgUgcA | singleSelect | Partnerships |

**Subtotal: 22 fields**

---

## SECTION 3 — DELETION EXECUTION CHECKLIST

Will must complete all items before executing any field deletion:

### Bookings — 23 Fields

- [ ] Export Bookings table as CSV (include all fields)
- [ ] Verify Automation_Health table has a record for every Booking
- [ ] Verify current D0-D60 checkbox states are reflected in Automation_Health records
- [ ] Verify Operational_Audits has linked records for all COMPLETED Bookings
- [ ] Confirm no active Make scenarios write to the 23 fields being removed
- [ ] Delete the 20 automation tracking fields (Section 1.1)
- [ ] Delete the 3 operational audit fields (Section 1.2)
- [ ] Verify Bookings record count unchanged after deletion
- [ ] Verify Automation_Health linked field (fldutXOFOw7H3DLy7) still resolves

### Partner Outreach — 22 Fields

- [ ] Export Partner Outreach table as CSV (include all fields)
- [ ] Verify Partnerships table schema has fields to receive each of the 22 field values
- [ ] Migrate data from Partner Outreach to linked Partnerships records (manually or via Make)
- [ ] Verify data integrity in Partnerships before proceeding
- [ ] Delete the 22 relationship intelligence fields (Section 2.1)
- [ ] Verify Partner Outreach linked field (fldk0HofCtGpVKDtc) resolves to Partnerships

---

## SECTION 4 — RISK ASSESSMENT

| Risk | Level | Mitigation |
|---|---|---|
| Active Airtable automation reads D0-D60 fields before deletion | HIGH | Will must audit B-03 automation (see AIRTABLE_AUTOMATION_AUDIT.md) before deletion |
| Make scenario CHARTER-001 through CHARTER-007 reference D-day fields | HIGH | All Make scenarios are NOT STARTED — no active references to worry about |
| Partner data lost if Partnerships table not ready to receive | HIGH | Complete migration and verify before any deletion |
| Record count change post-deletion (should be zero) | LOW | Verify with list_records_for_table count after deletion |

---

## SUMMARY

| Action | Table | Fields | Status |
|---|---|---|---|
| Remove automation tracking fields | Bookings | 20 | NOT EXECUTED — Will must authorize |
| Remove operational audit fields | Bookings | 3 | NOT EXECUTED — Will must authorize |
| Remove relationship fields | Partner Outreach | 22 | NOT EXECUTED — Will must authorize |
| Financial field extraction | Bookings | 12 | Phase 4 scope — not in this phase |

**TOTAL FIELDS DOCUMENTED FOR REMOVAL: 45 (23 Bookings + 22 Partner Outreach)**  
**FIELDS ACTUALLY DELETED THIS SESSION: 0**

**DEPRECATED_FIELD_REMOVAL_REPORT STATUS: COMPLETE ✓**  
**DELETION: Will must execute manually after CSV backup and data migration verification**

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*DEPRECATED_FIELD_REMOVAL_REPORT.md*  
*Execution Date: 2026-05-16*
