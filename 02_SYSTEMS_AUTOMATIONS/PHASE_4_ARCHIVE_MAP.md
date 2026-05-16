# Phase 4 Archive and Retirement Map
**Date:** 2026-05-16
**Phase:** Phase 4
**Status:** AUTHORIZED

---

## Section 1 — Base Retirement Map

| Base | Base ID | Status | Retirement Stage | Contents | Action |
|---|---|---|---|---|---|
| She Said Sail (primary) | appdZ49WqgjRXxA1R | KEEP — production | Never retire | 51 tables, all production ops | Optimize and maintain |
| She Said Sail — Financials | apprDKQtV2GInThwE | KEEP — production | Never retire | 9 tables, financial intelligence | Optimize and maintain |
| SSS Sandbox | appxOoLdiIVt733kV | KEEP — sandbox | Never retire | Sandbox testing only | Maintain isolation |
| Field Operations | apppFfA2VZVmamvXe | RETIRE — Phase 5 | 30-day post-migration validation window | 9 tables, all migrated to main base in Phase 3 | Validate then archive |
| Fragmented Ops | app2FbmVD44BXShyx | RETIRE — Phase 5 | After ME_Pricing merge validation (30 days) | 4 tables — Emergency_Protocols, Make_Scenarios, Concierge_Operators migrated Phase 3; ME_Pricing merged Phase 4 | Validate then archive |
| Influencer Outreach | appVWYY9Fp6tKu94m | RETIRE — Phase 5 | 30-day post-migration validation window | 1 table (Influencers, 31 records migrated Phase 3) | Validate then archive |
| SSS Operations Extension | appOQ0MGpQU1W4hoN | RETIRE — immediate | Duplicate content confirmed | 4 tables: Emergency_Protocols (14), Make_Scenarios (20), ME_Pricing, Concierge_Operators — all are duplicates | Export CSV archive → delete |
| She Said Sail copy | appQVZRgKKS0diyVX | AUDIT AND DELETE | Rogue copy — uncontrolled | Unknown — must audit all tables before deletion | List all tables → confirm duplicates → delete |
| Operations v4 | app49vaVbRwuobpPv | AUDIT REQUIRED | Status unknown | Unknown — must run list_tables_for_base before disposition | Audit → disposition decision |

---

## Section 2 — Table Deprecation Map (Main Base)

For each deprecated table: rename prefix `_DEPRECATED_` in Airtable. Do NOT delete. Document rename date and executor.

| Table Name | Table ID | Current Fields | Records | Deprecation Reason | Replace With |
|---|---|---|---|---|---|
| Brand | tbllNjlllEhG92Ozo | 6 | 0 | Airtable default scaffold, never built | N/A — no replacement needed |
| Services | tblBOgArrdfPkvR8B | 6 | 0 | Airtable default scaffold, never built | N/A — no replacement needed |
| Expansion Pipeline | tbllga7euKfd2ykM5 | 6 | 0 | Airtable default scaffold, never built | Cities table covers expansion tracking |
| AI_Prompt_Versions (old) | tbl0FJkA1E6a70cxX | 9 | Unknown | Missing 11 governance fields, not production-ready | Create new table from apppFfA2VZVmamvXe tbl2NSec9JjqW34Xf schema (20 fields) |
| Yacht_Availability (old) | tblDOoV4CHh8t4qpj | 13 | Unknown | Incomplete schema, superseded by richer version | tblkALubyHWjOY6Ul in apppFfA2VZVmamvXe (15 fields, better descriptions) |

---

## Section 3 — Table Deprecation Map (Financials Base)

| Table Name | Table ID | Current Fields | Records | Deprecation Reason | Replace With |
|---|---|---|---|---|---|
| Monthly Revenue | tblpTgps7cRQwDZp2 | 14 | Unknown | Superseded by Financial_Periods | Financial_Periods (tblli6AwOB114dOd1, 17 fields) |

---

## Section 4 — Source Table Deprecations (Post-Phase 3 + Phase 4 Migration)

Tables in source bases that had their data migrated — pending retirement after 30-day validation:

| Source Table | Source Base | Destination Table ID | Destination Base | Migration Phase | Records | Validation Window |
|---|---|---|---|---|---|---|
| Vessel_Maintenance | apppFfA2VZVmamvXe | tblmYWqqIu1Cidb4g | appdZ49WqgjRXxA1R | Phase 3 | 2 | 30 days from 2026-05-15 |
| Emergency_Escalations | apppFfA2VZVmamvXe | tblDbeRf3qO3xvqhK | appdZ49WqgjRXxA1R | Phase 3 | 2 | 30 days from 2026-05-15 |
| Incident_Reports | apppFfA2VZVmamvXe | tblO22Hh9lSTnhuu7 | appdZ49WqgjRXxA1R | Phase 3 | 2 | 30 days from 2026-05-15 |
| Operational_Audits | apppFfA2VZVmamvXe | tblAHYfl31529xUGr | appdZ49WqgjRXxA1R | Phase 3 | 2 | 30 days from 2026-05-15 |
| City_Financials | apppFfA2VZVmamvXe | tblycuku5Yq9s3fIw | appdZ49WqgjRXxA1R | Phase 3 | 2 | 30 days from 2026-05-15 |
| Emergency_Protocols | app2FbmVD44BXShyx | tblsTbNXo4Pa9mDSW | appdZ49WqgjRXxA1R | Phase 3 | 8 | 30 days from 2026-05-15 |
| Make_Scenarios | app2FbmVD44BXShyx | tbl08IpivapVQZUto | appdZ49WqgjRXxA1R | Phase 3 | 8 | 30 days from 2026-05-15 |
| Concierge_Operators | app2FbmVD44BXShyx | tblX61IB2qjDmac8l | appdZ49WqgjRXxA1R | Phase 3 | 3 | 30 days from 2026-05-15 |
| Influencers | appVWYY9Fp6tKu94m | tbl69Cguka4K4qgPO | appdZ49WqgjRXxA1R | Phase 3 | 31 | 30 days from 2026-05-15 |
| ME_Pricing | app2FbmVD44BXShyx | tblwDw2hkKW5moSr9 | appdZ49WqgjRXxA1R | Phase 4 | 5 | 30 days from 2026-05-16 |

---

## Section 5 — Retirement Execution Protocol

For each base retirement, execute in this order:

1. Confirm all migrated tables have been validated (record counts match, governance fields present)
2. Export full CSV backup of the source base (all tables) to `99_ARCHIVE/BASE_EXPORTS/`
3. Label backup: `[BASE_NAME]_[BASE_ID]_RETIRED_[DATE].csv`
4. Create a Governance_Review record documenting the retirement
5. Remove base from any documentation references that imply it is production
6. Delete the base (Airtable base deletion is permanent — do NOT delete without the backup confirmed)

**Validation checklist before any base retirement:**

- [ ] All tables from this base appear in destination base
- [ ] All record counts match
- [ ] Legacy_Record_ID field populated with source record IDs (enables cross-reference)
- [ ] No Make scenario references source base table IDs
- [ ] No Airtable native automation references source base
- [ ] Source base backup CSV exported and stored in `99_ARCHIVE`

---

## Section 6 — Archive Storage Structure (Recommended)

```
99_ARCHIVE/
├── BASE_EXPORTS/
│   ├── apppFfA2VZVmamvXe_RETIRED_[DATE].csv  (Field Operations — pending)
│   ├── app2FbmVD44BXShyx_RETIRED_[DATE].csv  (Fragmented Ops — pending)
│   ├── appVWYY9Fp6tKu94m_RETIRED_[DATE].csv  (Influencer Outreach — pending)
│   └── appOQ0MGpQU1W4hoN_RETIRED_[DATE].csv  (SSS Ops Extension — immediate)
├── PHASE_4_FIELD_EXPORTS/
│   ├── BOOKINGS_deprecated_fields_export_[DATE].csv  (22 checkbox fields)
│   └── PARTNER_OUTREACH_deprecated_fields_export_[DATE].csv  (22 partnership fields)
└── GOVERNANCE_RECORDS/
    └── Phase_4_Retirement_Audit_[DATE].md
```
