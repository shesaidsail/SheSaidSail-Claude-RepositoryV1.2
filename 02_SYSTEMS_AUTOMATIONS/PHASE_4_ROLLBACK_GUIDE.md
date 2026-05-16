# PHASE_4_ROLLBACK_GUIDE.md
**Date:** 2026-05-16
**Phase:** Phase 4
**Status:** ACTIVE — Reference this document before executing any Phase 4 destructive action
**Owner:** Will (Founder)
**Classification:** Confidential — Internal Use Only

---

## Principle

Rollback speed matters more than rollback elegance. If something breaks, reverse it first, document second. Every Phase 4 change is designed to be reversible. No Phase 4 action permanently destroys data.

---

## Section 1 — Executed Phase 4 Changes (Rollback Available)

### CHANGE 1: Packages Table — 14 New Fields Added
**Executed:** 2026-05-16
**Rollback method:** Delete the 14 new fields from tblwDw2hkKW5moSr9 in Airtable UI
**Rollback risk:** LOW — additive change, no existing records were modified
**Rollback time:** 5 minutes

Delete in this order (formulas first, then dependents):

| Order | Field Name | Field ID | Type |
|---|---|---|---|
| 1 | Implied_Margin | fldCefqEQSMCOXNNc | formula |
| 2 | Total_Internal_Cost | fldmuWRy71JOLjBod | formula |
| 3 | Will_Approved | fldpdjERlNOwmM9NK | checkbox |
| 4 | Live | fldSpvpAthpuLeIMX | checkbox |
| 5 | Add_Ons_Matrix | fldh2MxmJWpDmbrps | multilineText |
| 6 | Includes_Formatted | flduN43vf5nM5jp7z | multilineText |
| 7 | Labor_Cost_Target | fldAuqJ250x6OxOEj | currency |
| 8 | Vessel_Cost_Target | fldn3hedx6nlyRIDz | currency |
| 9 | F&B_Cost_Target | fldd7tBGIGEDT6UWE | currency |
| 10 | Peak_Multiplier | fldLcwB7iBeeWklHr | number |
| 11 | Margin_Floor_Pct | fldlBBMZ56TgEXvPX | percent |
| 12 | Max_Guests | fldA21eZf3e1vQ2in | number |
| 13 | Min_Guests | fldDBD22ElrnOvqt0 | number |
| 14 | City | fldiyXqFO7oOEyiCS | singleSelect |

---

### CHANGE 2: ME_Pricing — 5 Records Created in Packages
**Executed:** 2026-05-16
**Rollback method:** Delete 5 records by record ID from tblwDw2hkKW5moSr9
**Rollback risk:** LOW — source data preserved in app2FbmVD44BXShyx tblm5p6GQmYEjhZpG (untouched)
**Rollback time:** 2 minutes

| Record ID | Package Name |
|---|---|
| receKte1p4egjf3Jw | Client Hosting Charter — Miami |
| recfpvh5MdGkrajlc | Principal Private Charter — Miami |
| rec1cktDMLPV8PHvQ | Client Hosting Charter — Fort Lauderdale |
| recAQMYUI5wWpQeVX | Sunset Close Charter — Miami |
| recHuXfKlLArY4LB9 | Executive Retreat — Full Day Miami |

To confirm these are the correct records before deletion: filter Packages by Source_System = app2FbmVD44BXShyx. Should return exactly 5 records.

---

## Section 2 — Pending Phase 4 Changes (Pre-Execution Rollback Requirements)

These changes are **authorized but not yet executed**. Complete pre-execution requirements before proceeding.

---

### PENDING CHANGE 3: Bookings Field Retirements (23 fields)
**Authorization:** Granted in Phase 4
**Rollback risk:** MEDIUM
**Must do before execution:**
1. Export CSV of Bookings table scoped to ONLY the 23 deprecated fields
2. Name file: `BOOKINGS_deprecated_fields_YYYYMMDD.csv`
3. Store at: `99_ARCHIVE/PHASE_4_FIELD_EXPORTS/`
4. Confirm Automation_Health records exist for all Bookings with Status ≠ CANCELLED
5. Confirm no Airtable formula in Bookings table references these fields by name

**Post-execution rollback:**
1. Re-add each of the 23 fields (they will be empty — Airtable does not restore data on field re-add)
2. Re-import values from the CSV export via Airtable CSV import
3. Total rollback time: 30-45 minutes

**The 23 fields (see PHASE_4_FIELD_RETIREMENTS.md for full detail with IDs):**
D0 Sent, D1 Sent, D3 Sent, D7 Sent, D9 Gift Sent, D14 Sent, D30 Sent, D60 Sent, HV D2 Call Done, HV D5 Sent, HV D21 Sent, HV D23 Sent, D7 Reminder Sent, D10 Reminder Sent, D72hr Reminder Sent, D48hr Reminder Sent, Charter_Brief_Sent, Charter_Brief_All_Vendors_Confirmed, T7_Confirmed, T48_Captain_Confirmed, Crew_Report_Submitted, Vendor_Ratings_Entered, Conversations (multilineText duplicate).

---

### PENDING CHANGE 4: Partner Outreach Field Moves (22 fields)
**Authorization:** Granted in Phase 4
**Rollback risk:** MEDIUM
**Must do before execution:**
1. Export CSV of Partner Outreach scoped to the 22 partnership fields
2. Name file: `PARTNER_OUTREACH_deprecated_fields_YYYYMMDD.csv`
3. For every record where Became_Partner = true: document the Partnerships record ID that corresponds (or create one if missing)
4. Verify Partnerships table (tble5DcTo8mahr3lp) has corresponding records for all active partners

**Post-execution rollback:**
1. Re-add the 22 fields to Partner Outreach
2. Re-import values from CSV export
3. Remove duplicate entries from Partnerships if they were created as part of this migration
4. Total rollback time: 45-60 minutes

---

### PENDING CHANGE 5: AI_Prompt_Versions Table Replacement
**Authorization:** Granted in Phase 4
**Rollback risk:** LOW (no live Make scenarios reference this table yet)
**Must do before execution:**
1. Export all records from tbl0FJkA1E6a70cxX (old version)
2. Document any Airtable native automations referencing this table ID
3. Confirm no active Make scenario references this table ID

**Post-execution rollback:**
1. Rename new table to `_TEMP_AI_Prompt_Versions`
2. Rename old table back to `AI_Prompt_Versions`
3. Total rollback time: 5 minutes

---

### PENDING CHANGE 6: Placeholder Table Renames
**Authorization:** Granted in Phase 4
**Rollback risk:** NEGLIGIBLE
**Tables:** Brand (tbllNjlllEhG92Ozo), Services (tblBOgArrdfPkvR8B), Expansion Pipeline (tbllga7euKfd2ykM5)
**Rollback method:** Rename tables back to original names
**Rollback time:** 2 minutes

---

### PENDING CHANGE 7: Monthly Revenue Table Deprecation
**Authorization:** Granted in Phase 4
**Rollback risk:** NEGLIGIBLE
**Table:** tblpTgps7cRQwDZp2 in apprDKQtV2GInThwE
**Pre-execution:** Export all records as CSV
**Rollback method:** Rename back to `Monthly Revenue`
**Rollback time:** 1 minute

---

### PENDING CHANGE 8: Yacht_Availability Schema Replacement
**Authorization:** Granted in Phase 4
**Rollback risk:** MEDIUM
**Must do before execution:**
1. Check record count in tblDOoV4CHh8t4qpj — if any records exist, export as CSV
2. Confirm no Make scenario references tblDOoV4CHh8t4qpj
3. Confirm no Bookings linked to old Yacht_Availability via fldNTt4COtPabzNYK

**Post-execution rollback:**
1. Rename new table back to original name
2. Rename deprecated table back to Yacht_Availability
3. If records were migrated: delete from new table, restore from CSV to old table
4. Rollback time: 20-30 minutes

---

## Section 3 — Base Retirement Rollbacks (Phase 5 — Highest Risk)

Base retirement is the highest-risk action in the entire migration. Once a base is deleted from Airtable, it cannot be recovered without a CSV backup.

**For every base retirement, the rollback window is BEFORE deletion:**

| Base | Rollback Trigger | Rollback Action | Rollback Window |
|---|---|---|---|
| apppFfA2VZVmamvXe | Any migrated record found to be incomplete | Stop retirement, do not delete | Before deletion confirmed |
| app2FbmVD44BXShyx | ME_Pricing merge found to have errors | Stop retirement, do not delete | 30 days from 2026-05-16 |
| appVWYY9Fp6tKu94m | Influencer records found missing | Stop retirement, do not delete | 30 days from 2026-05-15 |
| appOQ0MGpQU1W4hoN | Duplicate confirmed as containing unique data | Stop retirement, audit contents | Before deletion confirmed |

**If a base has already been deleted and no CSV backup exists:** There is no rollback. This is why the CSV backup is a hard prerequisite, not a recommendation.

---

## Section 4 — Rollback Governance Protocol

Before executing any rollback:
1. Create a Founder Decisions record: Request Type = SYSTEM, document the rollback reason
2. Will approval required if rollback affects: financial fields, attribution fields, formula integrity, base deletion
3. Log in Audit_Log: Action_Type = ROLLBACK, include record IDs affected
4. Update State_Transition_Log: From State = Phase 4 action, To State = pre-Phase 4 state

After rollback completes:
1. Update this document with the rollback date, executor, and outcome
2. Update PHASE_4_NORMALIZATION_REPORT.md to reflect the reversal
3. Diagnose root cause before re-attempting the change

---

## Section 5 — Rollback Status Tracker

| Change | Rollback Available | Source Preserved | Pre-Execution Backup | Rollback Time |
|---|---|---|---|---|
| Packages 14 new fields | ✅ | N/A (additive) | N/A | 5 min |
| 5 ME package records | ✅ | ✅ app2FbmVD44BXShyx intact | N/A | 2 min |
| Bookings 23 fields (pending) | ✅ pending backup | N/A | ❌ NOT YET DONE | 30-45 min |
| Partner Outreach 22 fields (pending) | ✅ pending backup | N/A | ❌ NOT YET DONE | 45-60 min |
| AI_Prompt_Versions replacement (pending) | ✅ | N/A | ❌ NOT YET DONE | 5 min |
| Placeholder renames (pending) | ✅ | N/A | N/A | 2 min |
| Monthly Revenue deprecation (pending) | ✅ | ✅ pending export | ❌ NOT YET DONE | 1 min |
| Yacht_Availability replacement (pending) | ✅ | pending export | ❌ NOT YET DONE | 20-30 min |
| Base retirements (Phase 5) | ✅ before deletion | ✅ sources intact | ❌ NOT YET DONE | 2-4 hrs |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL — INTERNAL USE ONLY*
