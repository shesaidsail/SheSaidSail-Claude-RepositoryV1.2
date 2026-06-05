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
