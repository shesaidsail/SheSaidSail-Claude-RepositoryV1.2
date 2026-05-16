# FUTURE_CUSTOM_BACKEND_TRANSITION

**Status:** PRODUCTION DESIGN
**Version:** 1.0
**Effective Date:** May 2026
**Owner:** Will (Founder)
**Purpose:** Document how the Airtable/Make architecture could migrate to custom infrastructure without rewriting business logic. For future planning only — not an active project.
**Classification:** Confidential — Internal Use Only

---

## PURPOSE OF THIS DOCUMENT

This document exists for one reason: when She Said Sail and Mare Executive reach a scale where Airtable and Make become limiting factors — not before — there is a documented path to migrate without starting over.

The migration path protects two things:
1. **Business logic** — the booking lifecycle, brand routing, emergency protocols, financial rules, and governance boundaries do not need to be re-engineered. They translate.
2. **Operational continuity** — the business never goes dark during migration. Every stage is independently deployable.

This is not a plan to execute now. It is institutional knowledge for the future.

---

## SECTION 1 — WHEN TO CONSIDER THIS TRANSITION

### Trigger Signals

The Airtable/Make architecture is appropriate until one or more of these conditions is true:

| Signal | Threshold | Implication |
|--------|-----------|-------------|
| Airtable record volume | > 100,000 records in primary base | Query performance degrades for Make API calls |
| Daily Make scenario executions | > 10,000/day | Make plan costs become a significant operational expense vs. custom infrastructure |
| Concurrent booking volume | > 50 simultaneous charter bookings | Webhook queue delays become operationally significant |
| Engineering team hired | Full-time backend engineer on staff | Internal capability exists to build and maintain custom systems |
| Acquisition process active | Due diligence begins | Investor may require migration to more standard infrastructure |
| Make/Airtable pricing change | > 3× current cost | Financial case for custom infrastructure |
| Multi-brand expansion | > 3 brands on same Airtable base | Schema complexity becomes unmanageable in Airtable's flat structure |

**Not a trigger:**
- Faster response times (current system is fast enough for this business)
- More "control" (more control = more engineering maintenance)
- Wanting a custom brand on the tech stack

### Governance Requirement

Any decision to initiate the custom backend transition requires:
1. Will-created Founder Decision: Type = SYSTEM, context = "Custom backend transition — business case documented"
2. Engineering capacity confirmed (internal or contracted)
3. Full migration plan reviewed by Will before any code is written
4. Parallel running period of minimum 60 days — no Airtable/Make shutdown until custom system proves stable

---

## SECTION 2 — WHAT TRANSLATES DIRECTLY

Every piece of business logic in the current Make/Airtable system maps cleanly to custom backend equivalents. None of it needs to be rethought.

### Booking State Machine

Current: Airtable `Bookings.Status` field with Make monitoring state transitions
Future: Booking model in PostgreSQL/equivalent, with a `state_machine` library or explicit FSM logic

Current states translate exactly:
```
NEW → AVAILABILITY_PENDING → AVAILABILITY_CONFIRMED → DEPOSIT_SENT → DEPOSIT_PAID →
AGREEMENT_PENDING → CONFIRMED → BALANCE_DUE → PAID → COMPLETED → CANCELLED / VOID
```

No state logic changes. The same business rules apply. Only the implementation layer changes.

### Brand Router

Current: Make scenario M-BRAND-ROUTER (URL, form, occasion-based classification)
Future: Single function `classify_brand(form_data, referring_url)` → returns `{brand: "SSS" | "ME", confidence: "HIGH" | "MEDIUM" | "LOW"}`

Logic is identical. Same decision tree. Same default behavior. Same LOW-confidence alert requirement.

### Emergency Protocol

Current: Make scenario M-ESCALATION-ROUTER reads Emergency_Flag from Airtable
Future: `emergency_flag` boolean on Booking model. Middleware on all outbound message endpoints checks this field before any send. Identical safety guarantee.

The rule is structural: **no outbound message may fire if emergency_flag is true on the associated booking**. This is enforced at the middleware/service layer, not the application layer.

### AI Prompt Version Control

Current: AI_Prompt_Versions Airtable table — Make looks up LIVE + Will_Approved = true version
Future: PromptVersion model in database. Same fields. API endpoint: `GET /prompts/{make_variable_name}/active` returns the current LIVE + approved version's content.

Rollback works the same way: set current version to DEPRECATED, set prior version to LIVE. All services re-read on next execution.

### Audit Log

Current: Airtable Audit_Log table — Make writes before every action completes
Future: Immutable audit_events table in PostgreSQL. Append-only (enforced at database permission level — no UPDATE or DELETE granted). Same fields. Same immutability rules.

The governance requirement does not change: every autonomous action generates an audit record before that action is considered complete.

### Financial Protection Rules

Current: Airtable field permissions + Make pre-write checks prevent writing to Package_Price after CONFIRMED status
Future: Service-layer validation: `if booking.status >= CONFIRMED: raise ProtectedFieldError for package_price, net_profit, etc.`

Same rules. Same protected fields. Same authority requirements for override.

---

## SECTION 3 — TECHNOLOGY STACK RECOMMENDATION

When the time comes, this stack is well-matched to the business:

### Backend API

```
Language: Python (FastAPI) or TypeScript (NestJS)
Reasoning:
  - Python: fastest path for AI/Claude integration (Anthropic SDK native)
  - TypeScript/NestJS: better type safety for complex booking state machine
  - Both options have excellent Stripe SDK support

Recommendation: Python/FastAPI if AI integration is the priority
                TypeScript/NestJS if booking complexity is the priority
```

### Database

```
Primary: PostgreSQL (managed — Supabase or AWS RDS)
Why: ACID compliance for financial records, native JSONB for flexible data, row-level security

Bookings table → maps directly from Airtable Bookings table (normalized)
Clients table → maps directly
P&L table → replaces cross-base sync pattern (now linked via FK in same database)
Audit_Log table → append-only, enforced via database trigger or ORM policy
```

### Automation Orchestration

```
Replace Make with one of:
  Option A: Temporal.io — workflow orchestration with built-in retry, idempotency, observability
  Option B: Celery + Redis — for Python stack, simpler for scheduled and triggered tasks
  Option C: Inngest — event-driven, serverless-friendly, TypeScript-native

Recommendation:
  Temporal.io for high-volume or complex long-running workflows
  Inngest for simpler event-driven patterns with less operational overhead

The scenario names (M-LEAD-INTAKE, M-BOOKING-CREATION, etc.) become workflow names.
The module sequences become workflow activities.
The error handling and retry logic maps directly to workflow retry policies.
```

### AI Integration

```
Current: Make HTTP module → Claude API
Future: Anthropic Python/TypeScript SDK with prompt caching enabled

Claude API call pattern stays the same:
  1. Look up current active prompt version from PromptVersion model
  2. Assemble context payload
  3. Call Claude API
  4. Write result to database
  5. Write Audit_Log entry

Prompt caching (enabled in custom backend) reduces API costs significantly at scale.
```

### Webhook Handling

```
Current: Make webhook endpoints
Future: FastAPI/NestJS webhook endpoints

Same security patterns:
  - Bearer token validation
  - Stripe signature validation
  - Timestamp validation (replay protection)
  - Idempotency key check

The idempotency logic and security checks are identical — just moved from Make to the API layer.
```

---

## SECTION 4 — DATA MIGRATION STRATEGY

### From Airtable to PostgreSQL

```
Step 1: Schema translation (no data movement yet)
  Map every Airtable field to a PostgreSQL column
  Formula fields → computed columns or application-layer calculations
  Linked records → foreign keys
  Multi-select fields → JSONB arrays or join tables

Step 2: Read replica period (60 days minimum)
  Custom backend reads from BOTH Airtable API and new PostgreSQL database
  Airtable remains the write source of truth during this period
  Sync job runs every 15 minutes from Airtable → PostgreSQL
  Compare: verify data matches between systems

Step 3: Write migration
  New writes go to PostgreSQL (primary) + sync back to Airtable (for UI continuity)
  Airtable becomes the read layer for Luciana and Will during transition
  Custom backend is the write-primary

Step 4: Airtable deprecation
  After 30+ days of write-primary PostgreSQL with no data discrepancies
  Airtable becomes archive-read-only
  Make scenarios are disabled one by one as equivalents are confirmed working
  Airtable subscription maintained for 90 days archive period
```

### Financial Records

Financial records (P&L Per Charter, Expenses, Payouts) require special migration care:

- All financial records exported to CSV with checksums before migration
- Accountant reviews reconciliation between Airtable and PostgreSQL financial records
- Migration of financial records requires Will approval and Founder Decision
- No financial records are deleted from Airtable until PostgreSQL equivalents are confirmed accurate by CPA

---

## SECTION 5 — BUSINESS LOGIC MIGRATION MAP

This table maps every current Make scenario to its custom backend equivalent:

| Current Scenario | Custom Backend Equivalent | Migration Complexity |
|-----------------|--------------------------|---------------------|
| M-LEAD-INTAKE | POST /leads webhook endpoint | Low — simple API endpoint |
| M-BRAND-ROUTER | brand_classifier() service function | Low — pure logic |
| M-BOOKING-CREATION | BookingService.create_from_request() | Medium — Stripe integration |
| M-STRIPE-DEPOSIT | Stripe webhook handler: payment_intent.succeeded | Low — well-documented pattern |
| M-BOOKING-CONFIRMATION | BookingService.send_confirmation() | Low |
| M-CONCIERGE-ASSIGNMENT | BookingService.assign_concierge() | Low |
| M-BASIC-LIFECYCLE | LifecycleWorker (scheduled task) | Medium — multiple states |
| M-REVIEW-REQUEST | ReviewWorker.send_d7_review() | Low |
| M-YACHT-AVAILABILITY-LOCK | YachtAvailabilityService.lock() with DB transaction | Low — simpler with FK constraints |
| M-DOUBLE-BOOKING-CHECK | YachtAvailabilityService.check_availability() | Low — simpler with DB queries |
| M-FAILED-PAYMENT-HANDLER | Stripe webhook: payment_intent.payment_failed | Low |
| M-CHARTER-BRIEF | CharterBriefService.generate() | Medium — Claude API |
| M-ESCALATION-ROUTER | EscalationService.route() | Low — pure logic |
| M-AUTOMATION-HEALTH | HealthMonitorWorker (scheduled task) | Medium — reads multiple tables |
| M-AI-LEAD-SCORING | LeadScoringService.score() | Medium — Claude API |
| M-LTV-ENGINE | ClientService.update_ltv() | Low — aggregation query |
| M-REVENUE-HEALTH | RevenueHealthWorker (scheduled task) | Low — aggregation queries |
| M-SYNTER-SYNC | FinancialSyncWorker | Low — now same database (no cross-base sync needed) |
| M-FOUNDER-DIGEST | DigestWorker (scheduled task) | Medium — Claude API + aggregation |

**Highest migration complexity:** Scenarios with Claude API calls and complex context assembly. These require careful prompt context re-implementation in the service layer.

**Lowest migration complexity:** Scenarios that are purely data aggregation or simple state transitions.

---

## SECTION 6 — WHAT DOES NOT CHANGE IN MIGRATION

These elements are infrastructure-agnostic and survive the migration unchanged:

1. **Business rules** — margin floor at 20%, Emergency_Flag halts all outbound, HV client routing to human review
2. **Authority tiers** — Tier A, Tier B, Tier C autonomy boundaries
3. **Governance hierarchy** — GitHub documents supersede application configuration
4. **Audit requirements** — every autonomous action generates an immutable audit record
5. **Brand routing requirement** — M-BRAND-ROUTER logic runs first on every inbound flow
6. **Prompt version control** — AI_Prompt_Versions table structure and rollback requirement
7. **Escalation paths** — L1/L2/L3/L4 escalation levels and routing logic
8. **Financial protection rules** — Package_Price and Net_Profit are protected post-CONFIRMED
9. **Human checkpoints** — Tier B outputs require Luciana or Will review before transmission
10. **Sandbox isolation** — test environments never write to production data

These are governance requirements, not infrastructure choices. The custom backend must implement all of them as non-negotiable design constraints.

---

## SECTION 7 — OPERATIONS PORTAL MIGRATION

Current: Airtable Interfaces + hosted Netlify booking tool
Future: Dedicated web application (React/Next.js or similar)

The portal provides:
- Do This Now task queue (maps to: API endpoint reading prioritized open tasks)
- Active Bookings dashboard (maps to: API endpoint filtering confirmed/paid bookings)
- Escalation view (maps to: API endpoint filtering pending Founder Decisions)
- Financial Pulse (maps to: aggregate queries on Bookings and Financial_Periods)
- System Health (maps to: API endpoint reading Automation_Health / health_events table)

The UI surface changes. The data queries and operational logic are identical.

Luciana's booking tool (Netlify) → becomes a view within the custom portal.

---

## FINAL NOTE ON TIMING

Do not migrate prematurely. The Airtable/Make architecture is:
- Fully functional for current and projected scale
- Maintainable by non-engineers (Luciana can manage Airtable directly)
- Deployable and modifiable without code review cycles
- Acquisition-presentable (Airtable is a known, documented system)

The custom backend is appropriate when the business has the scale, the engineering capacity, and the operational maturity to maintain it. Building it prematurely adds complexity, reduces resilience, and creates single points of failure (the engineer who built it).

When the time comes, this document provides the roadmap. Until then, optimize the current system.

---

*SHE SAID SAIL + MARE EXECUTIVE*
*CONFIDENTIAL — INTERNAL USE ONLY*
*FUTURE_CUSTOM_BACKEND_TRANSITION v1.0*
*Effective May 2026*
*Status: Reference document — not an active project*
