# Deposit Workflow Split — 2026-06-05 (Option A + D)

## Deployed
- Stage 1 = SSS-BOOKING-CREATION (5094918): stripped of auto Stripe link/email/SMS.
  Now: create Booking, link Client, Status="Broker Confirmed", prefill Total Confirmed
  Booking Amount (fldvHvLaQ8BUhkplm) from Request Quoted Price, audit (PENDING_HUMAN).
  Rollback: scenarios_update with 5094918_STAGE0_pre-deposit-split.blueprint.json
  (NOTE: that baseline is the OLD flat-$495 auto-send; only roll back in emergency).
- Stage 2 = SSS-DEPOSIT-SEND (5303151): NEW, currently DEACTIVATED.
  Trigger: Booking where {Send Deposit Link}=1 AND {Stripe_Payment_Link_URL}=BLANK() AND {Total Confirmed Booking Amount}>0.
  Creates dynamic Stripe price (Stripe Deposit (Cents)) -> payment link -> stores ids/url,
  Status=Deposit Sent, Deposit Sent At=now, unchecks Send Deposit Link, deposit email + Quo SMS, audit.
  Rollback: scenarios_delete 5303151 (or leave deactivated).

## Airtable fields (Bookings tbl72omPibBkn2hZL)
- ADDED: Send Deposit Link (checkbox) fldqE231hTdi74Ojp
- ADDED: Deposit Sent At (dateTime) fldIWHdhFWb5rgWiB
- ADDED: Balance Due Amount (formula = Total Confirmed - Deposit Amount) fldTBYtEIRm17hmvr
- RENAMED: Package Price -> "Total Confirmed Booking Amount" (fldvHvLaQ8BUhkplm; id unchanged)
- Existing formulas reused: Deposit Amount = Total*0.5 (fldMa9x5WNl0h7Wta);
  Stripe Deposit (Cents) = Total*50 (fldFPxptv9DD7fuGT).

## BLOCKER
Stripe connection stripe2 (7687405) lacks read_write scope -> Make 'Make an API Call'
to create a Price returns more_permissions_required. Founder must re-auth the Stripe
connection in Make with read_write scope. Then reactivate 5303151 and retest.

## 2026-06-05 — TESTED GREEN
- Stripe write connection: "She Said Sail Stripe Write" id 9267612 (API key). Stage 2 modules 2 & 3 repointed to it.
- Stage 2 (5303151) ACTIVE.
- Stage 1 exec 3fcf734d11134b5bb9da09672bcfc197 (status 1) -> Booking Broker Confirmed, Total $10,000, no link.
- Stage 2 exec e8c38cb8db6c498ea2962856d3e86ff5 (status 1):
  - Stripe Price price_1Tf58YJ4IFUeX7X3Cw6Eucja = unit_amount 500000 ($5,000 = exact 50%)
  - Payment Link plink_1Tf58YJ4IFUeX7X3EZ1gMVp9 / https://buy.stripe.com/cNi14obQm5PM15T0XobMQ0f
  - Booking Status -> Deposit Sent; Deposit Sent At set; Send Deposit Link auto-unchecked; deposit email + Quo SMS sent.
- Idempotency exec c668c7cf427a4418a94bdafc088031bd: re-check + re-run created NO duplicate (URL-not-blank guard held).
- Zero-dollar guard exec 239c21625a204c82b410227d97a78f13: $0 booking skipped (Total>0 gate).
- Paid -> Concierge -> ACTIVE -> Confirmation: NOT executed (requires real $5k card payment). Detection wired: SSS-STRIPE-DEPOSIT matches Stripe_Payment_Link_ID.
- All test records deleted. Orphan Stripe test objects to archive: price_1Tf58YJ4IFUeX7X3Cw6Eucja, plink_1Tf58YJ4IFUeX7X3EZ1gMVp9.
