# FINAL MODULE REFERENCE — STAGE 1 FINAL REBUILD

**Version:** STAGE 1 FINAL REBUILD  
**Purpose:** Definitive reference for every module used across all 7 scenarios

---

## MODULE CATALOG

### gateway:CustomWebHook (version 1)
- **Purpose:** Instant webhook trigger — receives inbound HTTP POST
- **Used in:** M-OPS-LOGGER-ALERTER, M-BRAND-ROUTER, M-LEAD-INTAKE, M-STRIPE-DEPOSIT
- **Key parameter:** `hook` — placeholder value that Make replaces with the actual webhook ID after import
- **Output:** All fields from the incoming JSON payload as `{{1.field_name}}`
- **Rebinding:** After import, click the module and "Copy address" to get the actual webhook URL
- **Notes:** `maxResults: 1` is standard for webhook triggers

### gateway:CustomWebHookRespond (version 1)
- **Purpose:** Returns a response to the webhook caller
- **Used in:** M-BRAND-ROUTER (synchronous response required)
- **Key parameters:** `status` (HTTP status code), `body` (response body string)
- **Placement:** Must be in the main flow, after the router, at the end
- **Notes:** Not used in fire-and-forget scenarios (OPS-LOGGER-ALERTER, LEAD-INTAKE, STRIPE-DEPOSIT)

### builtin:BasicFilter (version 1)
- **Purpose:** Conditional gate — blocks execution if condition fails
- **Used in:** All scenarios — primary safety and idempotency mechanism
- **Key parameters:** `condition` (left/operator/right), `label` (for debugging), `throw: false` (silent fail)
- **Operators used:**
  - `exist` — field is present and non-empty
  - `notExist` — field is absent or empty
  - `equal` / `notEqual` — exact string match
  - `contain` / `notContain` — substring match
  - `and` — compound condition
- **Behavior:** When condition fails: execution stops for that trigger event. No error raised (throw: false).

### builtin:BasicRouter (version 1)
- **Purpose:** Routes execution to multiple parallel branches
- **Used in:** M-OPS-LOGGER-ALERTER (Slack routing), M-BRAND-ROUTER (brand routing), M-CONCIERGE-ASSIGNMENT (found/not-found routing)
- **Structure:** Contains `routes` array, each with a `flow` array
- **Behavior:** ALL routes are evaluated. Filters at the start of each route determine which branch executes.
- **Note:** In Make, router branches execute sequentially, not in parallel

### builtin:SetVariables (version 1)
- **Purpose:** Computes and stores named variables for use in later modules
- **Used in:** All scenarios
- **Key parameter:** `variables` array of `{name, value}` objects
- **Common uses:**
  - Computing idempotency keys
  - Pre-formatting display values (dates, names)
  - Storing API response values (payment_link_url, audit_record_id)
  - Computing Stripe deposit amounts in cents

### airtable:WatchRecords (version 3)
- **Purpose:** Polling trigger — watches for new/changed records matching a formula
- **Used in:** M-BOOKING-CREATION, M-CONCIERGE-ASSIGNMENT, M-BOOKING-CONFIRMATION
- **Key parameters:** `base`, `table`, `formula` (Airtable formula string), `maxResults`, `sort`
- **Trigger type:** Non-instant (polls on schedule, typically every 15 minutes)
- **Formula pattern:** `AND({Field} = 'VALUE', {Environment} = 'Production')`
- **Rebinding required:** Connection + base + table after import

### airtable:SearchRecords (version 3)
- **Purpose:** Search for records matching a formula
- **Used in:** M-LEAD-INTAKE (idempotency), M-BOOKING-CREATION (idempotency), M-STRIPE-DEPOSIT (find booking), M-CONCIERGE-ASSIGNMENT (find concierge)
- **Key parameters:** `base`, `table`, `filterByFormula`, `maxRecords`
- **Output:** Returns first matching record. If no match, `{{N.id}}` is empty.
- **Idempotency pattern:** Search for existing record before creating → filter on `notExist`

### airtable:GetRecord (version 3)
- **Purpose:** Fetch a specific record by record ID
- **Used in:** M-BOOKING-CONFIRMATION (fetch Client record)
- **Key parameters:** `base`, `table`, `recordId`
- **Output:** All fields of the record as `{{N.fields.FieldName}}`

### airtable:ActionCreateRecord (version 3)
- **Purpose:** Create a new record in a table
- **Used in:** M-OPS-LOGGER-ALERTER (Audit Log), M-LEAD-INTAKE (Request), M-BOOKING-CREATION (Booking)
- **Key parameters:** `base`, `table`, `fields` object
- **Output:** `{{N.id}}` = new record ID, `{{N.fields.FieldName}}` for all fields

### airtable:ActionUpdateRecord (version 3)
- **Purpose:** Update an existing record by record ID
- **Used in:** M-BRAND-ROUTER (set brand), M-STRIPE-DEPOSIT (set DEPOSIT_PAID), M-BOOKING-CREATION (set DEPOSIT_SENT + Stripe fields), M-CONCIERGE-ASSIGNMENT (set assigned), M-BOOKING-CONFIRMATION (set sent flags)
- **Key parameters:** `base`, `table`, `recordId`, `fields` object
- **Notes:** Only specified fields are updated — other fields are unchanged

### slack:ActionPostMessage (version 1)
- **Purpose:** Post a message to a Slack channel
- **Used in:** M-OPS-LOGGER-ALERTER (3 channel routes)
- **Key parameters:** `channel` (channel name with #), `text` (message body)
- **Rebinding required:** Slack OAuth connection + verify channel exists
- **Text formatting:** Slack markdown (`*bold*`, `_italic_`, `\n` for newline)

### gmail:ActionSendEmail (version 1)
- **Purpose:** Send an email via Gmail
- **Used in:** M-LEAD-INTAKE (auto-reply), M-BOOKING-CREATION (deposit email), M-BOOKING-CONFIRMATION (confirmation email)
- **Key parameters:** `account`, `to`, `subject`, `bodyType` (html), `body`
- **Rebinding required:** Gmail OAuth connection linked to hello@shesaidsail.com

### json:TransformToJSON (version 1)
- **Purpose:** Parse a JSON string into a structured object
- **Used in:** M-LEAD-INTAKE (parse Brand Router response)
- **Key parameter:** `input` — the JSON string to parse
- **Output:** Parsed fields accessible as `{{N.field_name}}`
- **Note:** Used because http:ActionSendData returns response as string in `{{N.body}}`

### http:ActionSendData (version 3)
- **Purpose:** Make an outbound HTTP request
- **Used in:** All scenarios — for Stripe API calls, Quo SMS, and internal webhook calls
- **Key parameters:** `url`, `method`, `headers` (array), `body`, `handleErrors`, `useNewZLibDeCompress`
- **handleErrors: false** — scenario fails if HTTP error, Make retry applies
- **handleErrors: true** — error captured in bundle, scenario continues (used for Quo SMS)
- **Content-Type for Stripe:** `application/x-www-form-urlencoded`
- **Content-Type for internal webhooks:** `application/json`
- **Response access:** `{{N.data.field}}` for JSON responses, `{{N.body}}` for raw string

---

## MAKE FORMULA REFERENCE

Common Make formulas used in this system:

| Formula | Usage | Example |
|---------|-------|---------|
| `formatDate(now; "YYYY-MM-DDTHH:mm:ssZ")` | ISO timestamp | Audit log timestamps |
| `formatDate(date; "MMMM D, YYYY")` | Human-readable date | Confirmation emails |
| `ifempty(value; default)` | Fallback for empty values | All scenarios |
| `toNumber(value)` | Convert string to number | Guest count, amounts |
| `multiply(a; b)` | Multiplication | Deposit amount calculation |
| `round(value)` | Round to integer | Stripe cent amounts |
| `divide(a; b)` | Division | Convert cents to dollars |
| `join(array; separator)` | Join array values | Building display strings |
| `split(string; delimiter)` | Split string | Extracting first name |
| `first(array)` | First array element | Linked record IDs |
| `trim(string)` | Remove whitespace | Name formatting |
| `toUpper(string)` | Uppercase | Currency code display |
| `encodeURL(string)` | URL-encode a string | Stripe API form values |
| `sha256(string)` | SHA-256 hash | Idempotency key generation |
| `if(condition; then; else)` | Conditional | Brand display name |
| `SEARCH("term"; {Field})` | Airtable formula search | Idempotency lookup |
| `AND(cond1; cond2)` | Airtable formula AND | Trigger formulas |
| `OR(cond1; cond2)` | Airtable formula OR | Lookup formulas |

---

*SHE SAID SAIL + MARE EXECUTIVE — CONFIDENTIAL*  
*STAGE_1_FINAL_REBUILD — FINAL_MODULE_REFERENCE.md*
