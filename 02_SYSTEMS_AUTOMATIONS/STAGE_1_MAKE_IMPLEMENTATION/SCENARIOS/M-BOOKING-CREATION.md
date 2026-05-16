# M-BOOKING-CREATION — Make.com Scenario Build Specification

**Document Version:** 1.0  
**Status:** PENDING BUILD  
**Last Updated:** 2026-05-16  
**Author:** Systems Architecture  
**Pipeline Stage:** Stage 1 — Booking Creation  
**Execution Order:** Module 6 in Stage 1 pipeline (called by M-STRIPE-DEPOSIT)

---

## 1. Scenario Name

`M-BOOKING-CREATION`

---

## 2. Scenario ID

`PENDING-REGISTRATION`

> Upon creation in Make.com, record the assigned Scenario ID here and update all cross-scenario references in M-STRIPE-DEPOSIT (caller) and M-BOOKING-CONFIRMATION (downstream callee).

---

## 3. Trigger Type

**Primary Trigger:** Called by M-STRIPE-DEPOSIT immediately after a Stripe deposit link is successfully generated and written to the Request record.

**Secondary Trigger (Resilience):** Airtable Watch on the Requests table (`tblTlSB9CO4dTGodg`) — fires when `Deposit_Link` field transitions from empty to populated AND `Booking_ID` field is still empty. This secondary trigger catches cases where M-STRIPE-DEPOSIT completes but the downstream call to M-BOOKING-CREATION fails before execution.

**Input received from M-STRIPE-DEPOSIT:**
```json
{
  "request_record_id": "{{airtable_record_id}}",
  "stripe_payment_link": "{{stripe_link_url}}",
  "deposit_amount": "{{deposit_amount_cents}}",
  "package_price": "{{package_price_cents}}",
  "brand": "SSS | ME",
  "city": "{{city_string}}",
  "environment": "Production | Sandbox",
  "triggered_by_scenario": "M-STRIPE-DEPOSIT",
  "stripe_link_generated_at": "{{iso8601_timestamp}}"
}
```

**Trigger Deduplication:** Before any processing begins, M-BOOKING-CREATION performs a Booking existence check (Module 5) using `Request_ID`. If a Booking already exists for this Request, the scenario exits cleanly without duplicate creation. This makes the secondary Airtable Watch trigger safe to run even if M-STRIPE-DEPOSIT already called the scenario successfully.

---

## 4. Exact Module Sequence

### Module 1 — [Airtable] Get Request Record

**Make Module Type:** Airtable — Get a Record  
**Table:** Requests (`tblTlSB9CO4dTGodg`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID Source:** `{{trigger.request_record_id}}` (from calling scenario payload)

**Fields retrieved and used downstream:**

| Field Name            | Airtable Field Type | Used In Module |
|-----------------------|---------------------|----------------|
| `Request_ID`          | Formula             | Module 5, 7    |
| `First_Name`          | Single line text    | Module 4, 7    |
| `Last_Name`           | Single line text    | Module 4, 7    |
| `Email`               | Email               | Module 2, 4    |
| `Phone`               | Phone number        | Module 4       |
| `Brand`               | Single select       | Module 7       |
| `City`                | Single select       | Module 7       |
| `Charter_Date`        | Date                | Module 7       |
| `Charter_Time`        | Single line text    | Module 7       |
| `Group_Size`          | Number              | Module 7       |
| `Package_ID`          | Link to Packages    | Module 7       |
| `Package_Price`       | Currency            | Module 7       |
| `Deposit_Amount`      | Currency            | Module 7       |
| `Deposit_Link`        | URL                 | Module 7       |
| `Occasion`            | Single line text    | Module 7       |
| `Special_Requests`    | Long text           | Module 7       |
| `Concierge_Assigned`  | Link to Users       | Module 7       |
| `Source`              | Single select       | Module 4, 7    |
| `Environment`         | Single select       | Module 7       |

**Error Handler:** If record not found (404), immediately route to Module 11 (error handler). Log to Slack #sss-ops-alerts: "M-BOOKING-CREATION: Request record not found — `{{request_record_id}}`. Scenario halted."

---

### Module 2 — [Airtable] Search Clients Table by Email

**Make Module Type:** Airtable — Search Records  
**Table:** Clients (`tblr84vRIWC5HmKvo`)  
**Base ID:** `appdZ49WqgjRXxA1R`

**Filter formula:**
```
{Email} = "{{1.Email}}"
```

**Max records:** 1  
**Sort:** `Created_At` descending (return most recent if duplicates exist)

**Output evaluated by Module 3 Router:**
- If `{{2.id}}` has a value → Client exists; capture `client_record_id = {{2.id}}`
- If `{{2.id}}` is empty/null → Client does not exist; route to Module 4

**Important:** Email comparison is case-insensitive at the Airtable formula level. Make sure the formula uses lowercase normalization if the platform does not guarantee this:
```
LOWER({Email}) = LOWER("{{1.Email}}")
```

---

### Module 3 — [Router] Client Exists vs. New Client

**Make Module Type:** Router (built-in)  
**Purpose:** Branch on whether a Client record was found in Module 2.

**Route A — Client Exists:**
- Condition: `{{2.id}}` is not empty
- Action: Set Make variable `client_record_id = {{2.id}}`; skip to Module 5
- No Airtable write performed

**Route B — New Client:**
- Condition: `{{2.id}}` is empty
- Action: Proceed to Module 4 (create Client record)

---

### Module 4 — [Airtable] Create Client Record (conditional — Route B only)

**Make Module Type:** Airtable — Create a Record  
**Table:** Clients (`tblr84vRIWC5HmKvo`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Runs only when:** Router Module 3 Route B is active (new client)

**Field mapping — see Section 6 (Client Record Field Mapping) for complete specification.**

**Output:** Capture `{{4.id}}` as `client_record_id` for use in Module 7.

**Error Handler:** If creation fails, route to Module 11. Do not proceed to Booking creation without a valid Client record.

---

### Module 5 — [Airtable] Search Bookings Table for Existing Booking (Idempotency Check)

**Make Module Type:** Airtable — Search Records  
**Table:** Bookings (`tbl72omPibBkn2hZL`)  
**Base ID:** `appdZ49WqgjRXxA1R`

**Filter formula:**
```
{Request_ID} = "{{1.Request_ID}}"
```

**Max records:** 1

**Output evaluated by Module 6 Router:**
- If `{{5.id}}` has a value → Booking already exists; capture `booking_record_id = {{5.id}}`; skip to Module 8
- If `{{5.id}}` is empty → Booking does not exist; proceed to Module 7

> This is the primary idempotency gate. Whether triggered by M-STRIPE-DEPOSIT or by the Airtable Watch secondary trigger, a Booking is never created twice for the same Request.

---

### Module 6 — [Router] Booking Exists vs. New Booking

**Make Module Type:** Router (built-in)  
**Purpose:** Branch on whether a Booking already exists for this Request ID.

**Route A — Booking Exists:**
- Condition: `{{5.id}}` is not empty
- Action: Set `booking_record_id = {{5.id}}`; log to Slack (idempotency triggered, not an error); skip to Module 8

**Route B — New Booking:**
- Condition: `{{5.id}}` is empty
- Action: Proceed to Module 7 (create Booking record)

---

### Module 7 — [Airtable] Create Booking Record

**Make Module Type:** Airtable — Create a Record  
**Table:** Bookings (`tbl72omPibBkn2hZL`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Runs only when:** Router Module 6 Route B is active (new booking)

**Booking ID Generation:** See Section 7 (BK-YYYY-NNNN Generation Logic) for complete specification.

**Field mapping — see Section 5 (Airtable Field Mapping) for complete specification.**

**Output:** Capture `{{7.id}}` as `booking_record_id`.

**Error Handler:** If creation fails, route to Module 11 (error handler with rollback instructions). Do not proceed to Module 8 without a confirmed Airtable record ID.

---

### Module 8 — [Airtable] Update Request Record

**Make Module Type:** Airtable — Update a Record  
**Table:** Requests (`tblTlSB9CO4dTGodg`)  
**Base ID:** `appdZ49WqgjRXxA1R`  
**Record ID:** `{{trigger.request_record_id}}`

**Fields updated:**

| Field Name        | Value                                                  | Notes                             |
|-------------------|--------------------------------------------------------|-----------------------------------|
| `Booking_ID`      | Link to `{{booking_record_id}}`                        | Linked record field               |
| `Status`          | `DEPOSIT_SENT`                                         | Single select — already set by M-STRIPE-DEPOSIT; confirm/re-affirm |
| `Booking_Created_At` | `{{now}}`                                           | Timestamp of this update          |

**Note on Status:** M-STRIPE-DEPOSIT sets Status = `DEPOSIT_SENT` when it generates the link. This module confirms the link via the Booking record connection. Do not regress the status if it has already advanced.

---

### Module 9 — [Slack] Post Booking Created Notification

**Make Module Type:** Slack — Create a Message  
**Channel:** `#sss-ops-alerts`  
**Post As:** She Said Sail Automations (bot)

**Message template:**
```
:white_check_mark: *Booking Created* — {{brand}}
*Booking ID:* {{booking_id_human_readable}}
*Client:* {{1.First_Name}} {{1.Last_Name}} ({{1.Email}})
*Charter Date:* {{1.Charter_Date}} at {{1.Charter_Time}}
*Group Size:* {{1.Group_Size}}
*City:* {{1.City}}
*Deposit Amount:* ${{deposit_amount_formatted}}
*Package:* {{package_name_or_TBD}}
*Status:* DEPOSIT_SENT
*Airtable Booking Record:* https://airtable.com/appdZ49WqgjRXxA1R/tbl72omPibBkn2hZL/{{booking_record_id}}
*Environment:* {{environment}}
_Triggered by: M-BOOKING-CREATION_
```

**Conditional prefix:** If environment = Sandbox, prepend `[SANDBOX TEST] ` to the message.

---

### Module 10 — [HTTP] Call M-AUDIT-LOGGER Sub-Scenario

**Make Module Type:** HTTP — Make a Request (POST to Make webhook URL of M-AUDIT-LOGGER)  
**OR:** Make — Call a Scenario (if using Make's native scenario-linking feature)

**Payload sent to M-AUDIT-LOGGER:**
```json
{
  "triggering_event": "Booking record created for Request {{1.Request_ID}} after Stripe deposit link confirmed",
  "source_data": "Request record ID: {{trigger.request_record_id}}; Client record ID: {{client_record_id}}; Deposit link present: true",
  "scenario_name": "M-BOOKING-CREATION",
  "output": "Booking record created: {{booking_id_human_readable}} ({{booking_record_id}}); Client record: {{client_record_id}} ({{client_is_new}}); Request updated with Booking link",
  "destination": "Airtable Bookings table tbl72omPibBkn2hZL",
  "approval_state": "AUTONOMOUS",
  "brand": "{{1.Brand}}",
  "city": "{{1.City}}",
  "environment": "{{1.Environment}}",
  "affected_record_id": "{{booking_record_id}}",
  "prompt_version": null,
  "ai_confidence_score": null
}
```

**On M-AUDIT-LOGGER failure:** Post to Slack #sss-ops-alerts immediately: "SEV-1: M-AUDIT-LOGGER failed for M-BOOKING-CREATION. Booking `{{booking_id_human_readable}}` created but NOT logged. Manual audit entry required. Booking record ID: `{{booking_record_id}}`."

---

### Module 11 — [Error Handler] Airtable Write Failures and Client Creation Failures

**Make Module Type:** Error Handler (Break / Resume route)  
**Scope:** Attached to Modules 4, 7, and 8

**On error in Module 4 (Client creation failed):**
1. Log error details to Slack #sss-ops-alerts: "M-BOOKING-CREATION FAILED: Could not create Client record for `{{1.Email}}`. Booking creation halted. Manual intervention required. Request ID: `{{1.Request_ID}}`."
2. Set Make variable `booking_creation_failed = true`
3. Do NOT attempt Booking creation
4. Call M-AUDIT-LOGGER with `output = "FAILED: Client creation error"`, `approval_state = "PENDING_HUMAN"`
5. Stop scenario execution

**On error in Module 7 (Booking creation failed):**
1. Log error details to Slack #sss-ops-alerts: "M-BOOKING-CREATION FAILED: Could not create Booking record for Request `{{1.Request_ID}}`. Client record `{{client_record_id}}` exists but no Booking written. Manual cleanup may be required."
2. If Client was newly created in this run (Route B of Module 3), include: "WARNING: New Client record `{{client_record_id}}` was created but Booking failed. Consider deleting orphaned Client if no other Bookings exist for this email."
3. Call M-AUDIT-LOGGER with failure payload
4. Stop scenario execution

**On error in Module 8 (Request update failed):**
1. Booking record `{{booking_record_id}}` exists in Airtable but Request is not linked to it
2. Log to Slack: "M-BOOKING-CREATION PARTIAL FAILURE: Booking created (`{{booking_id_human_readable}}`) but Request record update failed. Request `{{1.Request_ID}}` must be manually linked to Booking `{{booking_record_id}}`."
3. Call M-AUDIT-LOGGER with partial failure payload
4. Do NOT delete the Booking record; it is valid

---

## 5. Airtable Field Mapping — Booking Record Creation

Complete field mapping for the Airtable Create Record call in Module 7. Every field written on initial Booking creation.

| Airtable Field Name       | Field Type          | Value / Source                                              | Notes                                         |
|---------------------------|---------------------|-------------------------------------------------------------|-----------------------------------------------|
| `Booking_ID`              | Formula (read-only) | Auto-generated by Airtable formula AUD-YYYY-NNNN pattern   | Do NOT write; formula field                   |
| `Booking_ID_Human`        | Single line text    | `{{generated_booking_id}}` — see Section 7                  | Written by Make; BK-2026-NNNN format          |
| `Status`                  | Single select       | `DEPOSIT_SENT`                                              | Initial status on creation                    |
| `Brand`                   | Single select       | `{{1.Brand}}` (from Request record)                         | SSS or ME                                     |
| `City`                    | Single select       | `{{1.City}}` (from Request record)                          | e.g., Miami, NYC                              |
| `Client`                  | Link to Clients     | `[{{client_record_id}}]`                                    | Array of one record ID                        |
| `Request`                 | Link to Requests    | `[{{trigger.request_record_id}}]`                           | Array of one record ID                        |
| `Package`                 | Link to Packages    | `[{{1.Package_ID}}]` (if populated)                         | May be empty if package not yet identified    |
| `Charter_Date`            | Date                | `{{1.Charter_Date}}`                                        | ISO 8601 date from Request                    |
| `Charter_Time`            | Single line text    | `{{1.Charter_Time}}`                                        | e.g., "2:00 PM"                               |
| `Group_Size`              | Number              | `{{1.Group_Size}}`                                          | Integer                                       |
| `Package_Price`           | Currency            | `{{1.Package_Price}}`                                       | From Request (sourced from Packages table)    |
| `Deposit_Amount`          | Currency            | `{{trigger.deposit_amount}}` (converted from cents)         | Stripe sends cents; convert to dollars        |
| `Deposit_Link`            | URL                 | `{{trigger.stripe_payment_link}}`                           | Stripe Checkout or Payment Link URL           |
| `Balance_Due`             | Formula (read-only) | `Package_Price - Deposit_Amount`                            | Do NOT write; formula field                   |
| `Occasion`                | Single line text    | `{{1.Occasion}}`                                            | e.g., "Birthday", "Corporate Retreat"         |
| `Special_Requests`        | Long text           | `{{1.Special_Requests}}`                                    | Client notes from intake form                 |
| `Concierge_Assigned`      | Link to Users       | `[{{1.Concierge_Assigned}}]` (if populated)                 | May be empty; assigned in M-CONCIERGE-ASSIGNMENT |
| `Source`                  | Single select       | `{{1.Source}}`                                              | e.g., "Website", "Referral", "Instagram"      |
| `Automations_Paused`      | Checkbox            | `false`                                                     | Default false on creation                     |
| `Emergency_Flag`          | Checkbox            | `false`                                                     | Default false on creation                     |
| `Environment`             | Single select       | `{{trigger.environment}}`                                   | Production or Sandbox                         |
| `Booking_Created_At`      | Date/Time           | `{{now}}`                                                   | Make timestamp at moment of creation          |
| `Created_By_Scenario`     | Single line text    | `M-BOOKING-CREATION`                                        | Traceability field                            |
| `Confirmation_Status`     | Single select       | `PENDING`                                                   | Updated by M-BOOKING-CONFIRMATION             |
| `Confirmation_Email_Draft`| Long text           | *(empty on creation)*                                       | Written by M-BOOKING-CONFIRMATION             |
| `Deposit_Paid`            | Checkbox            | `false`                                                     | Updated by Stripe webhook when paid           |
| `Deposit_Paid_At`         | Date/Time           | *(empty on creation)*                                       | Updated by Stripe webhook                     |
| `Notes_Internal`          | Long text           | *(empty on creation)*                                       | Ops team use only                             |

---

## 6. Client Record Field Mapping

Complete field mapping for the Airtable Create Record call in Module 4. Every field written when creating a new Client record.

| Airtable Field Name   | Field Type       | Value / Source                                              | Notes                                            |
|-----------------------|------------------|-------------------------------------------------------------|--------------------------------------------------|
| `Full_Name`           | Single line text | `{{1.First_Name}} {{1.Last_Name}}`                          | Concatenated from Request fields                 |
| `First_Name`          | Single line text | `{{1.First_Name}}`                                          | From Request record                              |
| `Last_Name`           | Single line text | `{{1.Last_Name}}`                                          | From Request record                              |
| `Email`               | Email            | `{{1.Email}}`                                               | Primary lookup key — must be unique              |
| `Phone`               | Phone number     | `{{1.Phone}}`                                               | From Request record                              |
| `Brand`               | Single select    | `{{1.Brand}}`                                               | SSS or ME (brand at time of first contact)       |
| `City`                | Single select    | `{{1.City}}`                                                | City market at time of first contact             |
| `Source`              | Single select    | `{{1.Source}}`                                              | e.g., "Website", "Referral"                      |
| `Environment`         | Single select    | `{{trigger.environment}}`                                   | Production or Sandbox                            |
| `Client_Since`        | Date             | `{{today}}`                                                 | Date of first Booking, not first inquiry         |
| `Created_By_Scenario` | Single line text | `M-BOOKING-CREATION`                                        | Traceability field                               |
| `Client_Status`       | Single select    | `ACTIVE`                                                    | Active on first booking                          |
| `Total_Bookings`      | Number           | `1`                                                         | Increment if Client already exists (Route A)     |
| `Notes_Internal`      | Long text        | *(empty on creation)*                                       | Ops team use only                                |

> **Route A (existing client):** When Module 3 routes to existing client, update `Total_Bookings` field on the Client record by incrementing: `{{existing_total_bookings + 1}}`. Do NOT update Email, Phone, or Source — those are set at first contact.

---

## 7. BK-YYYY-NNNN Booking ID Generation Logic

The Booking ID must be human-readable, sequential within a calendar year, and collision-safe across concurrent scenario runs.

### Approach: Airtable MAX Formula + Make Increment

**Step 7a — Find the highest existing sequence number for current year:**

In Module 7 (before the Create call), execute a preceding [Airtable] Search Records call:

- **Table:** Bookings (`tbl72omPibBkn2hZL`)
- **Filter formula:**
  ```
  LEFT({Booking_ID_Human}, 7) = "BK-{{YYYY}}-"
  ```
  Where `{{YYYY}}` is the current 4-digit year (e.g., `BK-2026-`)
- **Sort:** `Booking_ID_Human` descending
- **Max records:** 1

**Step 7b — Extract and increment:**

In a [Tools] — Set Variable module:
```
last_booking_id = {{search_result.Booking_ID_Human}}
last_sequence_number = toNumber(right(last_booking_id, 4))
next_sequence_number = last_sequence_number + 1
next_sequence_padded = lpad(toString(next_sequence_number), 4, "0")
generated_booking_id = "BK-" + formatDate(now, "YYYY") + "-" + next_sequence_padded
```

**Step 7c — First booking of the year:**

If the search returns no results (first booking of the calendar year):
```
next_sequence_number = 1
generated_booking_id = "BK-2026-0001"
```

**Step 7d — Collision prevention:**

This approach has a race condition risk if two M-BOOKING-CREATION runs execute within milliseconds of each other. Mitigation:

1. **Primary mitigation:** The idempotency check in Module 5 prevents the most common duplicate scenario (same Request triggered twice).
2. **Secondary mitigation:** Airtable's `Booking_ID_Human` field has a uniqueness validator (configure in Airtable field settings). If a collision occurs, the second write will fail, triggering Module 11.
3. **Recovery:** Module 11 retries the ID generation sequence with a 2-second delay (Make built-in retry on error).
4. **Long-term:** In a high-volume environment (>100 bookings/day), replace this with a dedicated Counter table record that uses Airtable's atomic record update to increment a single counter field.

---

## 8. Duplicate Prevention — Idempotency Detail

The idempotency gate is Module 5 (Airtable search on `Request_ID` field in Bookings table).

**How it works:**

1. Every Booking record stores the `Request_ID` from the originating Airtable Request record (the formula-generated human-readable ID, e.g., `REQ-2026-0042`).
2. Module 5 queries `{Request_ID} = "{{1.Request_ID}}"` against the Bookings table.
3. If any record is found, Module 6 Router takes Route A (skip creation) and jumps directly to Module 8 to ensure the Request record is updated with the Booking link (which may have failed in a prior run).
4. The `Request_ID` field in Bookings is configured as a single line text field (not a linked field) to make the formula filter reliable.

**Edge cases handled:**

| Scenario                                     | Result                                          |
|----------------------------------------------|-------------------------------------------------|
| M-STRIPE-DEPOSIT calls M-BOOKING-CREATION twice | Second call finds existing Booking; skips creation |
| Airtable Watch secondary trigger fires after primary | Finds existing Booking; skips creation      |
| Make scenario retries after a partial failure | Finds existing Booking; continues from Module 8 |
| Two different Requests from the same Client  | Different `Request_ID` values; both Bookings created correctly |

---

## 9. Circular Trigger Risk Mitigation

The Bookings table has 129 fields. Writing to any of those fields via Make can re-trigger any Airtable automation or Make Watch trigger that watches the Bookings table.

**Risk:** M-BOOKING-CREATION writes to the Bookings table (Module 7), which could re-trigger M-BOOKING-CREATION if a Watch trigger is misconfigured.

**Mitigations in place:**

1. **Primary trigger is call-based, not Watch-based.** M-BOOKING-CREATION is called by M-STRIPE-DEPOSIT, not by a Bookings table Watch. The Bookings table Watch in Module 3 (secondary trigger) watches the Requests table, not the Bookings table.

2. **Secondary trigger watches Requests table, not Bookings table.** The Airtable Watch (secondary trigger) watches `Requests.Deposit_Link` population AND `Requests.Booking_ID` being empty. After Module 8 writes `Booking_ID` to the Request, the Watch condition `{Booking_ID} = ""` becomes false, preventing re-trigger.

3. **Idempotency gate stops re-entry.** Even if a Watch trigger fires incorrectly, Module 5 will find the existing Booking and route to Module 6 Route A. No duplicate Booking is ever written.

4. **`Automations_Paused` field check (defensive):** If `{{1.Automations_Paused}}` is true on the Booking record, M-BOOKING-CREATION exits immediately (add this as Module 1a check on the Request record's linked Booking status).

5. **`Created_By_Scenario` field filter:** Any Airtable native automation watching the Bookings table should filter out records where `{Created_By_Scenario}` is not empty to avoid reacting to Make-created records.

---

## 10. Rollback — Deleting a Booking Created in Error

**Scenario:** A Booking record was created incorrectly (wrong data, duplicate due to race condition, test record in Production, etc.) and must be deleted.

**Manual rollback procedure (Ops team):**

1. Open the Booking record in Airtable
2. Note the linked Request record ID and Client record ID
3. Set `Automations_Paused = true` on the Booking record BEFORE deleting (prevents any downstream automation from firing on the deletion)
4. In the linked Request record: clear the `Booking_ID` linked field and revert `Status` to `AVAILABILITY_CONFIRMED` (or the appropriate pre-booking status)
5. Delete the Booking record from Airtable
6. If the Client record was newly created in the same scenario run (i.e., the Client has no other Bookings linked to them), delete the Client record
   - Verify: open Client record and check `Bookings` linked field count. If count = 0, safe to delete
7. Create a corrective Audit Log entry manually (or call M-AUDIT-LOGGER directly) documenting the deletion

**Automated rollback in Module 11 (partial — for same-run errors only):**

If Module 7 (Booking creation) succeeds but Module 8 (Request update) fails catastrophically and the scenario is configured to roll back:

1. [Airtable] Delete the just-created Booking record: `DELETE tbl72omPibBkn2hZL / {{7.id}}`
2. If Module 4 created a new Client in this run: [Airtable] Delete the Client record: `DELETE tblr84vRIWC5HmKvo / {{4.id}}`
3. Log the rollback to Slack and M-AUDIT-LOGGER

> **Important:** Automated rollback is only safe within the same scenario run. Once M-BOOKING-CONFIRMATION has been called downstream, rollback requires manual ops intervention.

---

## 11. Sandbox Test — Verification Checklist

Run the following verification steps after building the scenario in Make. Use `Environment = Sandbox` for all tests.

**Pre-test setup:**
- [ ] Create a test Request record in Airtable with all required fields populated
- [ ] Set `Deposit_Link` to a test URL (e.g., `https://test.stripe.com/fake-link`)
- [ ] Set `Status = AVAILABILITY_CONFIRMED` on the test Request

**Test 1 — New Client, New Booking (happy path):**
- [ ] Call M-BOOKING-CREATION manually with the test Request record ID
- [ ] Verify: New Client record created in `tblr84vRIWC5HmKvo` with correct fields
- [ ] Verify: New Booking record created in `tbl72omPibBkn2hZL` with all 25+ fields populated
- [ ] Verify: Booking_ID_Human follows format `BK-2026-NNNN`
- [ ] Verify: Request record updated with `Booking_ID` linked field and `Status = DEPOSIT_SENT`
- [ ] Verify: Slack #sss-ops-alerts receives booking created notification
- [ ] Verify: Audit Log record created in `tblrMpTfMk8q1eNHp`

**Test 2 — Existing Client:**
- [ ] Run Test 1 with the same email address but a new Request record
- [ ] Verify: No duplicate Client record created
- [ ] Verify: New Booking links to the existing Client record
- [ ] Verify: Existing Client's `Total_Bookings` incremented

**Test 3 — Idempotency (duplicate prevention):**
- [ ] Call M-BOOKING-CREATION twice with the same Request record ID
- [ ] Verify: Only one Booking record exists for this Request
- [ ] Verify: Slack message on second run indicates idempotency route taken
- [ ] Verify: Two Audit Log records exist (one per call)

**Test 4 — Sandbox environment label:**
- [ ] Verify: Booking record has `Environment = Sandbox`
- [ ] Verify: Slack message includes `[SANDBOX TEST]` prefix
- [ ] Verify: Audit Log record has `environment = Sandbox`

**Test 5 — ME brand routing:**
- [ ] Run Test 1 with `Brand = ME`
- [ ] Verify: Booking record has `Brand = ME`
- [ ] Verify: Slack message shows correct brand

---

## 12. Open Issues

| Issue ID | Description                                                                                                         | Owner       | Priority | Status  |
|----------|---------------------------------------------------------------------------------------------------------------------|-------------|----------|---------|
| OI-BC-01 | **Airtable native automation inventory must be complete before this scenario runs.** Any Airtable automations watching the Bookings or Requests tables must be catalogued and confirmed to not conflict with Make writes. | Will / Ops  | CRITICAL | OPEN    |
| OI-BC-02 | **Confirm `Booking_ID_Human` field exists in Airtable Bookings table.** If Airtable uses a formula field for Booking ID generation, the Make write approach must be adjusted to a dedicated text field. | Systems Arch | HIGH    | OPEN    |
| OI-BC-03 | **Confirm `Request_ID` field in Bookings table exists as a plain text field** (not a linked field) to support formula-based filter in Module 5 idempotency check. | Systems Arch | HIGH    | OPEN    |
| OI-BC-04 | **Determine correct Deposit_Amount unit.** Confirm whether M-STRIPE-DEPOSIT passes amount in cents (integer) or dollars (decimal). Conversion logic in Module 7 depends on this. | Systems Arch | HIGH    | OPEN    |
| OI-BC-05 | **Package field may be empty.** If the client did not select a specific package during intake, the Package linked field cannot be written. Confirm how M-BOOKING-CREATION should handle no-package Requests (write without package, or block creation until package is assigned). | Will        | MEDIUM  | OPEN    |
| OI-BC-06 | **Concurrent booking race condition.** If booking volume exceeds 5+ simultaneous creates, the BK-YYYY-NNNN sequence number approach may produce collisions. Evaluate Counter table approach before go-live. | Systems Arch | LOW (Stage 1) | OPEN |
| OI-BC-07 | **Downstream call to M-BOOKING-CONFIRMATION.** Confirm whether M-BOOKING-CREATION should call M-BOOKING-CONFIRMATION directly as its final step (before M-AUDIT-LOGGER), or whether M-BOOKING-CONFIRMATION is triggered separately. Current design assumes direct call. | Systems Arch | HIGH    | OPEN    |

---

## 13. Final Scenario Status

**Build Status:** `PENDING BUILD`

> This scenario cannot be built until OI-BC-01 (Airtable native automation inventory) is resolved and OI-BC-02/OI-BC-03 (field existence confirmation) are verified. These are blockers.

**Dependency chain:**
- Requires: M-STRIPE-DEPOSIT (upstream caller) — must be built and tested first
- Enables: M-BOOKING-CONFIRMATION (downstream callee) — must not be built until this scenario is validated
- Requires: M-AUDIT-LOGGER (sub-scenario) — must be built and tested before this scenario goes to sandbox

**Make.com Scenario Registration Checklist:**
- [ ] Scenario created in Make.com workspace
- [ ] Scenario ID recorded in this document
- [ ] All Airtable connections authenticated
- [ ] Slack connection authenticated
- [ ] Scenario linked from M-STRIPE-DEPOSIT (outbound call configured)
- [ ] Scenario linked to M-BOOKING-CONFIRMATION (outbound call configured)
- [ ] Error handlers attached to Modules 4, 7, 8
- [ ] Scenario set to Active (after sandbox validation complete)
- [ ] Scenario execution log retention set to 30 days minimum

---

*Document maintained by Systems Architecture. All field names and table IDs are authoritative as of 2026-05-16. Verify against live Airtable base before build.*
