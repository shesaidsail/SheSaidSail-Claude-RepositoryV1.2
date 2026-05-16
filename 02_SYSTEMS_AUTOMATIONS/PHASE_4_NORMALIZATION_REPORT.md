# PHASE 4 NORMALIZATION REPORT
**She Said Sail + Mare Executive — Airtable Architecture Normalization**

---

| Attribute | Value |
|---|---|
| Document Type | Phase 4 Execution Report |
| Phase | Phase 4 |
| Execution Date | 2026-05-15 |
| Authority | Will Doyle — Founder, She Said Sail + Mare Executive |
| Classification | INTERNAL OPERATIONS — CONFIDENTIAL |
| Status | PARTIAL EXECUTION — Actions 1 & 2 executed via MCP; Actions 3–8 authorized, pending manual execution by Will |

---

## Execution Summary

| Action | Description | Status | Method |
|---|---|---|---|
| Action 1 | Packages table expansion (12 → 26 fields) | EXECUTED ✓ | MCP / Claude |
| Action 2 | ME_Pricing merge into Packages (5 records) | EXECUTED ✓ | MCP / Claude |
| Action 3 | Bookings table cleanup (remove 23 fields) | AUTHORIZED — PENDING | Manual Airtable UI |
| Action 4 | Partner Outreach cleanup (move 22 fields) | AUTHORIZED — PENDING | Manual Airtable UI |
| Action 5 | AI_Prompt_Versions table replacement | AUTHORIZED — PENDING | Manual Airtable UI |
| Action 6 | Placeholder table retirement (3 tables) | AUTHORIZED — PENDING | Manual Airtable UI |
| Action 7 | Yacht_Availability old version retirement | AUTHORIZED — PENDING | Manual Airtable UI |
| Action 8 | Monthly Revenue table deprecation | AUTHORIZED — PENDING | Manual Airtable UI |

---

## Action 1 — Packages Table Expansion

**Status: EXECUTED ✓**
**Date:** 2026-05-15
**Table:** Packages (tblwDw2hkKW5moSr9)
**Base:** SSS Operations (appdZ49WqgjRXxA1R)

### Field Count
- Before: 12 fields
- After: 26 fields
- Fields added: 14

### Fields Added

| Field Name | Field ID | Type | Configuration |
|---|---|---|---|
| City | fldiyXqFO7oOEyiCS | singleSelect | Choices: Miami, Fort Lauderdale, All Cities |
| Min_Guests | fldDBD22ElrnOvqt0 | number | Integer |
| Max_Guests | fldA21eZf3e1vQ2in | number | Integer |
| Margin_Floor_Pct | fldlBBMZ56TgEXvPX | percent | Decimal |
| Peak_Multiplier | fldLcwB7iBeeWklHr | number | Precision 2 |
| F&B_Cost_Target | fldd7tBGIGEDT6UWE | currency | USD ($) |
| Vessel_Cost_Target | fldn3hedx6nlyRIDz | currency | USD ($) |
| Labor_Cost_Target | fldAuqJ250x6OxOEj | currency | USD ($) |
| Total_Internal_Cost | fldmuWRy71JOLjBod | formula | `{F&B_Cost_Target} + {Vessel_Cost_Target} + {Labor_Cost_Target}` |
| Implied_Margin | fldCefqEQSMCOXNNc | formula | `IF({Package Price} > 0, ({Package Price} - {Total_Internal_Cost}) / {Package Price}, 0)` |
| Includes_Formatted | flduN43vf5nM5jp7z | multilineText | AI-readable bullet list of inclusions |
| Add_Ons_Matrix | fldh2MxmJWpDmbrps | multilineText | Format: Name \| $Price \| $Cost \| Notes |
| Live | fldSpvpAthpuLeIMX | checkbox | Controls whether package is AI-quotable |
| Will_Approved | fldpdjERlNOwmM9NK | checkbox | Approval gate — must be checked before AI uses package |

### Rationale for Each Field Group

**Pricing controls (City, Min_Guests, Max_Guests, Margin_Floor_Pct, Peak_Multiplier):** The AI pricing engine needs to know which packages are available in which cities, what guest counts they support, the minimum acceptable margin percentage, and how to adjust price for peak season. Without these fields the AI cannot enforce margin floors or generate city-specific quotes.

**Cost targets (F&B_Cost_Target, Vessel_Cost_Target, Labor_Cost_Target, Total_Internal_Cost, Implied_Margin):** The AI must know internal costs to calculate whether a proposed price maintains the minimum margin. The formula fields derive margin automatically from the three cost target inputs and the package price. This eliminates manual margin calculation.

**AI-readable content (Includes_Formatted, Add_Ons_Matrix):** The AI needs machine-readable package descriptions to accurately represent what is included in a charter quote and what add-ons are available at what cost. `Includes_Formatted` is a bullet list. `Add_Ons_Matrix` uses a pipe-delimited format for structured parsing.

**Governance (Live, Will_Approved):** Only packages with both `Live = true` and `Will_Approved = true` should be quoted by the AI. This prevents the AI from quoting deprecated, unapproved, or draft packages.

---

## Action 2 — ME_Pricing Merge into Packages

**Status: EXECUTED ✓**
**Date:** 2026-05-15
**Source:** app2FbmVD44BXShyx — tblm5p6GQmYEjhZpG (ME_Pricing)
**Destination:** appdZ49WqgjRXxA1R — tblwDw2hkKW5moSr9 (Packages)
**Records migrated:** 5

### Records Created in Packages

| Record ID | Package Name | Price | Brand | City | Guests | Duration | Margin Floor | Peak Multiplier |
|---|---|---|---|---|---|---|---|---|
| receKte1p4egjf3Jw | Client Hosting Charter — Miami | $6,500 | Mare Executive | Miami | 8–25 | 4 hr | 35% | 1.25x |
| recfpvh5MdGkrajlc | Principal Private Charter — Miami | $7,500 | Mare Executive | Miami | 1–2 | 3 hr | 35% | 1.35x |
| rec1cktDMLPV8PHvQ | Client Hosting Charter — Fort Lauderdale | $5,800 | Mare Executive | Fort Lauderdale | 8–25 | 4 hr | 30% | 1.20x |
| recAQMYUI5wWpQeVX | Sunset Close Charter — Miami | $3,800 | Mare Executive | Miami | 6–15 | 2 hr | 30% | 1.20x |
| recHuXfKlLArY4LB9 | Executive Retreat — Full Day Miami | $9,500 | Mare Executive | Miami | 6–20 | 6 hr | 35% | 1.30x |

### Fields Populated on All 5 ME Records

All five records were created with full field population:
- `Includes_Formatted` — AI-readable bullet list of inclusions per package
- `Add_Ons_Matrix` — Pipe-delimited price/cost/notes matrix for all available add-ons
- `F&B_Cost_Target` — Internal F&B cost target
- `Vessel_Cost_Target` — Internal vessel cost target
- `Labor_Cost_Target` — Internal labor cost target
- `Total_Internal_Cost` — Auto-calculated by formula
- `Implied_Margin` — Auto-calculated by formula
- `City` — Miami or Fort Lauderdale
- `Min_Guests` and `Max_Guests` — Per package guest range
- `Margin_Floor_Pct` — 30% or 35% per package
- `Peak_Multiplier` — 1.20x–1.35x per package
- `Source_System` — app2FbmVD44BXShyx (provenance tracking)
- `Environment` — Production
- `Brand` — Mare Executive

### Total Packages Table State Post-Phase 4

| Segment | Record Count | Brand Field |
|---|---|---|
| SSS Packages (pre-existing) | 132 | Not yet populated — Phase 5 data entry task |
| ME Packages (migrated Phase 4) | 5 | Mare Executive ✓ |
| **Total** | **137** | |

> **Note:** The 132 existing SSS packages do not yet have `Brand` populated. This is a data-entry task for Phase 5. The field exists and is ready.

---

## Action 3 — Bookings Table Cleanup

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Table:** Bookings (tbl72omPibBkn2hZL)
**Base:** SSS Operations (appdZ49WqgjRXxA1R)

### Prerequisites (Complete Before Execution)

1. **Export CSV** of the 23 fields to be removed. Store in `99_ARCHIVE/PHASE_4_FIELD_EXPORTS/Bookings_Deprecated_Fields_[DATE].csv`
2. **Confirm Automation_Health coverage.** Automation_Health (tblCVpMsX4ZvnsJqL) must have a linked record for all active Bookings. The link field is `fldutXOFOw7H3DLy7`. Spot-check at least 10 active Booking records to confirm their Automation_Health records have data populated.
3. **Confirm no active Make scenarios reference these field IDs.** Current status: all 8 Make scenarios are NOT_STARTED — this prerequisite is satisfied as of 2026-05-15.

### Fields to Remove

See PHASE_4_FIELD_RETIREMENTS.md — Section 1 for the complete field-by-field table with field IDs.

### Expected Result

- Before: 151 fields
- After: 128 fields
- Net reduction: 23 fields

### Risk Level: LOW
No live Make automations reference these fields. Data is preserved in Automation_Health. CSV export provides full rollback capability.

---

## Action 4 — Partner Outreach Cleanup

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Table:** Partner Outreach (tblnjGWa6JNiogfCo)
**Destination:** Partnerships (tble5DcTo8mahr3lp)

### Prerequisites (Complete Before Execution)

1. **Audit all records where `Became_Partner = true`.** For each such record, verify a corresponding Partnerships record exists. If not, create the Partnerships record first.
2. **Export CSV** of the 22 fields before removal. Store in `99_ARCHIVE/PHASE_4_FIELD_EXPORTS/Partner_Outreach_Deprecated_Fields_[DATE].csv`
3. **For formula fields:** The four formula fields (Net Revenue After Commission, Avg Revenue Per Booking, Partner ROI, Lead to Booking Rate) should be re-created as formulas in the Partnerships table, not simply moved. Confirm source fields exist in Partnerships before re-creating.

### Fields to Move

See PHASE_4_FIELD_RETIREMENTS.md — Section 2 for the complete field-by-field table with field IDs and Partnerships equivalents.

### Expected Result

- Before: 88 fields
- After: 66 fields
- Net reduction: 22 fields

### Risk Level: LOW-MEDIUM
Prerequisite audit of `Became_Partner = true` records must complete before execution. Data migration to Partnerships must happen before deletion from Partner Outreach.

---

## Action 5 — AI_Prompt_Versions Table Replacement

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Base:** SSS Operations (appdZ49WqgjRXxA1R)

### Step-by-Step Execution

1. **Note the record count** in tbl0FJkA1E6a70cxX (current 9-field version)
2. **Export all records** to CSV before any action
3. **Create new AI_Prompt_Versions table** using the 20-field schema from apppFfA2VZVmamvXe (tbl2NSec9JjqW34Xf)
4. **Migrate any existing records** from old table to new table (manual re-entry or import)
5. **Rename old table** to `_DEPRECATED_AI_Prompt_Versions` to prevent accidental use
6. **Update any views or interface elements** that reference the old table name

### Missing Fields in Current Version (must exist in replacement)

`Deployed_By`, `Deployed_At`, `Rollback_To_Version`, `Brand`, `Make_Variable_Name`, `Performance_Notes`, `Will_Approved`, `Leads_Processed`, `Leads_Converted`, `Conversion_Rate_Pct`, `Override_Count`

### Risk Level: LOW
Current 9-field version cannot support production AI governance — it is effectively non-functional for its intended purpose. Replacement is entirely additive.

---

## Action 6 — Placeholder Table Retirement

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Base:** SSS Operations (appdZ49WqgjRXxA1R)

### Tables to Rename (Do Not Delete)

| Current Name | Table ID | New Name |
|---|---|---|
| Brand | tbllNjlllEhG92Ozo | _DEPRECATED_Brand |
| Services | tblBOgArrdfPkvR8B | _DEPRECATED_Services |
| Expansion Pipeline | tbllga7euKfd2ykM5 | _DEPRECATED_Expansion_Pipeline |

### Rationale
All three tables contain only the 6 Airtable default fields (Name, Notes, Attachments, Status, Assignee, Due Date). No operational records exist. These are structural placeholders that consume schema bandwidth and create confusion in the table list.

**Do not delete.** The `_DEPRECATED_` prefix convention preserves schema history without the risk of accidental data loss.

### Risk Level: NONE
No records. No formulas reference these tables. No Make scenarios reference these tables.

---

## Action 7 — Yacht_Availability Old Version Retirement

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Table:** Yacht_Availability (tblDOoV4CHh8t4qpj)
**Base:** SSS Operations (appdZ49WqgjRXxA1R)

### Execution Steps

1. **Check record count** in tblDOoV4CHh8t4qpj
2. **If 0 records:** Rename to `_DEPRECATED_Yacht_Availability` immediately
3. **If records exist:** Export CSV, then migrate records to the canonical version in apppFfA2VZVmamvXe (tblkALubyHWjOY6Ul, 15 fields), then rename to `_DEPRECATED_Yacht_Availability`

### Canonical Version Reference
- Base: apppFfA2VZVmamvXe (Field Operations)
- Table: tblkALubyHWjOY6Ul
- Field count: 15 (2 additional fields vs. old version)

### Risk Level: LOW
Old version has no confirmed live records. Richer version in Field Operations base is the correct source.

---

## Action 8 — Monthly Revenue Table Deprecation

**Status: AUTHORIZED — PENDING MANUAL EXECUTION**
**Executor:** Will Doyle
**Table:** Monthly Revenue (tblpTgps7cRQwDZp2)
**Base:** SSS Financials (apprDKQtV2GInThwE)

### Execution Steps

1. **Export all records** from Monthly Revenue to CSV. Store in `99_ARCHIVE/PHASE_4_FIELD_EXPORTS/Monthly_Revenue_Archive_[DATE].csv`
2. **Rename table** to `_DEPRECATED_Monthly_Revenue`
3. **Add description** to the table: "DEPRECATED — Superseded by Financial_Periods (tblli6AwOB114dOd1). Do not write new data to this table. Historical records preserved. See Financial_Periods for all current reporting."

### Canonical Replacement
- Table: Financial_Periods (tblli6AwOB114dOd1) — 17 fields
- Supersedes Monthly Revenue in all reporting use cases

### Risk Level: LOW
Financial_Periods already exists and is the established replacement. Renaming does not delete any data.

---

## Cumulative Phase 4 Impact

### Executed (MCP)

| Metric | Value |
|---|---|
| Fields added to Packages | 14 (12 → 26) |
| ME package records created | 5 |
| Total Packages records post-Phase 4 | 137 (132 SSS + 5 ME) |

### Authorized (Pending Manual Execution by Will)

| Metric | Value |
|---|---|
| Fields authorized for removal from Bookings | 23 (151 → 128) |
| Fields authorized for removal/migration from Partner Outreach | 22 (88 → 66) |
| Tables authorized for _DEPRECATED_ rename in SSS Operations base | 5 |
| Tables authorized for _DEPRECATED_ rename in SSS Financials base | 1 |
| Tables to be replaced (AI_Prompt_Versions) | 1 |
| Fragmented bases authorized for eventual retirement | 4 (pending Phase 5 validation) |

---

## Post-Phase 4 Architecture Score (Projected After Manual Execution)

| Dimension | Pre-Phase 4 | Post-Phase 4 (projected) |
|---|---|---|
| AI pricing readiness (Packages) | 20/100 | 85/100 |
| ME data integration | 25/100 | 100/100 |
| Field normalization (Bookings) | 30/100 | 55/100 |
| Field normalization (Partner Outreach) | 35/100 | 60/100 |
| Table count rationalization | 50/100 | 72/100 |
| Governance field coverage | 88/100 | 90/100 |
| Data migration completeness | 75/100 | 92/100 |
| **Overall** | **61/100** | **79/100** |

---

## Phase 5 Prerequisites

The following items are deferred to Phase 5 and must not be actioned until Phase 4 manual execution is complete and validated:

1. Populate `Brand` field for all 132 existing SSS Packages records
2. Audit appQVZRgKKS0diyVX (She Said Sail rogue copy) — audit before any deletion
3. Audit app49vaVbRwuobpPv (Operations v4) — audit before any retirement
4. Retire appOQ0MGpQU1W4hoN (SSS Operations Extension) — after confirming no unique data
5. Further Bookings field extraction — financial calculation fields are Phase 5 scope
6. Make scenario implementation — begin building live automations once schema is stable
7. Activate Make_Scenarios: update status from NOT_STARTED as scenarios are built

---

*Document generated: 2026-05-15 | Phase 4 Execution | She Said Sail + Mare Executive*
