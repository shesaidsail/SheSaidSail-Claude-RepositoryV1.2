# TABLE_RENAME_LOG.md
## She Said Sail + Mare Executive — Table Rename & Naming Audit

**Phase:** Final Pre-Make Cleanup — Task 4  
**Execution Date:** 2026-05-16  
**Base:** appdZ49WqgjRXxA1R (SSS Operations)  
**Status:** COMPLETE — Will action required for UI renames  
**Classification:** Confidential — Internal Use Only

---

## SCOPE NOTE

The Airtable MCP tools do not expose a rename_table endpoint. All renames documented here must be executed by Will in the Airtable UI (Base Settings → Tables → Rename). This report documents the naming issues, the recommended names, and the justification for each.

---

## SECTION 1 — FULL TABLE INVENTORY

| # | Table ID | Current Name | Record Count | Naming Issue | Verdict |
|---|---|---|---|---|---|
| 1 | tblr84vRIWC5HmKvo | Clients | — | None | KEEP |
| 2 | tblUrAVcx4HMdWVsN | Brokers | — | None | KEEP |
| 3 | tblzqHlzECDvJ8KRH | Cities | — | None | KEEP |
| 4 | tblvyZk1SorIQ6KWF | Yachts | — | None | KEEP |
| 5 | tbl72omPibBkn2hZL | Bookings | — | None | KEEP |
| 6 | tblwDw2hkKW5moSr9 | Packages | — | None | KEEP |
| 7 | tblTlSB9CO4dTGodg | Requests | — | None | KEEP |
| 8 | tblnjGWa6JNiogfCo | Partner Outreach | — | Space in name | RENAME → Partner_Outreach |
| 9 | tbl09BGFacWim5Rk7 | Organic Content | — | Space in name | RENAME → Organic_Content |
| 10 | tblVsxlNdP9xHDipE | Paid Ads | — | Space in name | RENAME → Paid_Ads |
| 11 | tbltZIenYJsUrUYIP | Affiliates | — | None | KEEP |
| 12 | tblFCE26qDwfp4Jwd | Founder Decisions | — | Space in name | RENAME → Founder_Decisions |
| 13 | tblrMpTfMk8q1eNHp | Audit Log | — | Space in name | RENAME → Audit_Log |
| 14 | tblWCmLmR1x8CaxNH | State Transition Log | — | Spaces in name | RENAME → State_Transition_Log |
| 15 | tblAben0zR8spPPhE | Lessons | — | None | KEEP |
| 16 | tblE2tMb5A1IqwOzW | Google Reviews | — | Space in name | RENAME → Google_Reviews |
| 17 | tblEqsCswZcLOh3B1 | Google Performance | — | Space in name | RENAME → Google_Performance |
| 18 | tblL9xCyFbl0fGkLB | Dashboard Notes | — | Space in name | RENAME → Dashboard_Notes |
| 19 | tbl18uNpNd7HPBCps | Calls Recommended | — | Space in name | RENAME → Calls_Recommended |
| 20 | tbl4xD1mKhf0QL9Fe | Vendors | — | None | KEEP |
| 21 | tbllNjlllEhG92Ozo | Brand | 4 | Generic/ambiguous name | RENAME → Brand_Registry |
| 22 | tblBOgArrdfPkvR8B | Services | 15 | Generic/ambiguous name | RENAME → Service_Catalog |
| 23 | tbllga7euKfd2ykM5 | Expansion Pipeline | 11 | Space in name | RENAME → Expansion_Pipeline |
| 24 | tblVq6XV6AyOxfXAU | Website/Landing Page | — | Slash breaks API references | RENAME → Landing_Pages |
| 25 | tblutlUhd804erPev | Copy/Creative Assets | — | Slash breaks API references | RENAME → Creative_Assets |
| 26 | tblhMocOusidgd3N0 | Conversations | — | None | KEEP |
| 27 | tbl0FJkA1E6a70cxX | AI_Prompt_Versions | — | None | KEEP |
| 28 | tblDOoV4CHh8t4qpj | Yacht_Availability | — | None | KEEP |
| 29 | tblCVpMsX4ZvnsJqL | Automation_Health | — | None | KEEP |
| 30 | tbltItmUMLearQ7mC | AI_Audit | — | None | KEEP |
| 31 | tblSTy6Rtn7vofF1r | Cybersecurity_Incidents | — | None | KEEP |
| 32 | tbleMkafYH5w5xpO5 | Incapacitation_Actions | — | None | KEEP |
| 33 | tbl0nCmwo6CPa3APJ | Governance_Reviews | — | None | KEEP |
| 34 | tblWrvF72JOrFmPkV | Team_Members | — | None | KEEP |
| 35 | tble5DcTo8mahr3lp | Partnerships | — | None | KEEP |
| 36 | tblbtF1AVzDwkt0gE | Expenses | — | None | KEEP |
| 37 | tblN75TzobD9AEvaq | Contractors | — | None | KEEP |
| 38 | tblu4JbvIxlhS1ehN | Audience_Segments | — | None | KEEP |
| 39 | tblTs5px03BPrUpG4 | Campaigns | — | None | KEEP |
| 40 | tblbhwEaa8D23WmyA | Synter_Sync_Log | 0 | "Synter" may be unrecognized — see note | REVIEW |
| 41 | tblpj4SwaSXu2vbVN | Guests | 0 | None | KEEP |
| 42 | tblmYWqqIu1Cidb4g | Vessel_Maintenance | — | None | KEEP |
| 43 | tblDbeRf3qO3xvqhK | Emergency_Escalations | — | None | KEEP |
| 44 | tblO22Hh9lSTnhuu7 | Incident_Reports | — | None | KEEP |
| 45 | tblBK5EBPh5ppc8vw | Regional_Directors | 0 | None | KEEP |
| 46 | tblAHYfl31529xUGr | Operational_Audits | — | None | KEEP |
| 47 | tblycuku5Yq9s3fIw | City_Financials | — | None | KEEP |
| 48 | tblsTbNXo4Pa9mDSW | Emergency_Protocols | — | None | KEEP |
| 49 | tbl08IpivapVQZUto | Make_Scenarios | — | None | KEEP |
| 50 | tblX61IB2qjDmac8l | Concierge_Operators | — | None | KEEP |
| 51 | tbl69Cguka4K4qgPO | Influencers | — | None | KEEP |

---

## SECTION 2 — PRIORITY RENAMES

### CRITICAL — Slash in Name Breaks API References

These tables have forward slashes in their names. While Airtable API references tables by ID (not name), the slash causes problems in: Make module display names, webhook payloads (JSON key encoding), and any formula or script referencing the table name string.

| Current Name | Table ID | Recommended Name | Urgency |
|---|---|---|---|
| Website/Landing Page | tblVq6XV6AyOxfXAU | Landing_Pages | BEFORE Stage 1 |
| Copy/Creative Assets | tblutlUhd804erPev | Creative_Assets | BEFORE Stage 1 |

### HIGH — Ambiguous Names Conflict With Field Names

These tables have generic names that match field names used across the base, creating confusion in Make scenario builder, formula editor, and AI context:

| Current Name | Table ID | Recommended Name | Reason |
|---|---|---|---|
| Brand | tbllNjlllEhG92Ozo | Brand_Registry | Conflicts with "Brand" singleSelect field on 20+ tables |
| Services | tblBOgArrdfPkvR8B | Service_Catalog | Conflicts with "Service Category" field usage — 15 active records (DJ/Entertainment, Private Dining, etc.) |

### MEDIUM — Spaces in Names

Spaces in table names work in Airtable UI but can cause issues in scripting, webhook references, and non-Airtable contexts. Rename during next maintenance window:

| Current Name | Table ID | Recommended Name |
|---|---|---|
| Partner Outreach | tblnjGWa6JNiogfCo | Partner_Outreach |
| Organic Content | tbl09BGFacWim5Rk7 | Organic_Content |
| Paid Ads | tblVsxlNdP9xHDipE | Paid_Ads |
| Founder Decisions | tblFCE26qDwfp4Jwd | Founder_Decisions |
| Audit Log | tblrMpTfMk8q1eNHp | Audit_Log |
| State Transition Log | tblWCmLmR1x8CaxNH | State_Transition_Log |
| Google Reviews | tblE2tMb5A1IqwOzW | Google_Reviews |
| Google Performance | tblEqsCswZcLOh3B1 | Google_Performance |
| Dashboard Notes | tblL9xCyFbl0fGkLB | Dashboard_Notes |
| Calls Recommended | tbl18uNpNd7HPBCps | Calls_Recommended |
| Expansion Pipeline | tbllga7euKfd2ykM5 | Expansion_Pipeline |

---

## SECTION 3 — SYNTER_SYNC_LOG REVIEW NOTE

**Table:** Synter_Sync_Log (tblbhwEaa8D23WmyA)  
**Record Count:** 0 (no records written yet)  
**Schema:** 15 fields — Sync_ID, Environment, Brand, Sync_Type, Direction, Status, Source_Record_ID, Source_Table, Synter_Record_ID, Records_Synced, Error_Message, Make_Scenario, Executed_At, Duration_Seconds, UUID

The name "Synter" appears intentional — "Synter_Record_ID" and "Synter_Asset_ID" (field in Creative_Assets table) suggest "Synter" is a specific third-party system or internal sync engine name. Will must confirm:

1. Is "Synter" an intentional system name (third-party integration, internal brand)?
2. If yes: KEEP name as-is.
3. If "Synter" is a typo of "Sync": RENAME → Make_Sync_Log (better describes the table's purpose given Make_Scenario field).

**No rename executed pending Will confirmation.**

---

## SECTION 4 — TABLES WITH NO RECORDS (REVIEW)

| Table | Table ID | Records | Action |
|---|---|---|---|
| Guests | tblpj4SwaSXu2vbVN | 0 | KEEP — table exists for future guest profile collection |
| Regional_Directors | tblBK5EBPh5ppc8vw | 0 | KEEP — table exists for future city expansion |
| Synter_Sync_Log | tblbhwEaa8D23WmyA | 0 | REVIEW — see Section 3 |

---

## SECTION 5 — RENAME EXECUTION INSTRUCTIONS

Will must perform all renames in Airtable UI:
1. Open base appdZ49WqgjRXxA1R
2. Click the table name tab → right-click → Rename
3. Rename in the order listed in Section 2 (Critical first, then High, then Medium)
4. Verify linked record fields referencing these tables still resolve correctly after rename (table IDs are unchanged — renames are safe)
5. Update any Make scenario display names that reference the old table names (Make modules use table IDs internally, but display names in Make UI use the name at time of configuration)

**CRITICAL RENAMES REQUIRED BEFORE STAGE 1 MAKE IMPLEMENTATION:**
- Website/Landing Page → Landing_Pages
- Copy/Creative Assets → Creative_Assets

---

## SUMMARY

| Category | Count |
|---|---|
| Tables KEEP as-is (no action) | 34 |
| Tables RENAME — CRITICAL (before Stage 1) | 2 |
| Tables RENAME — HIGH (naming clarity) | 2 |
| Tables RENAME — MEDIUM (spaces, next window) | 11 |
| Tables REVIEW (Will confirmation needed) | 1 |
| Tables with 0 records (monitor) | 2 |

**TABLE_RENAME_LOG STATUS: COMPLETE ✓**  
**EXECUTION: Will must perform renames in Airtable UI — no API rename tool available**

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*TABLE_RENAME_LOG.md*  
*Execution Date: 2026-05-16*
