# Quo Native SMS Migration — 2026-06-05

Change set: native Quo SMS for She Said Sail. Number +17547012228, connection "My Quo connection" (id 8825028).

## Scenarios changed
- 5279773 SSS-LEAD-INTAKE-V2 — ADD lead-acknowledgment SMS (new module id 40) in Route 1 after Slack notify (7), before audit (8). Gated on new record + phone present. onerror Resume (41). Audit module 8 extended to log ack SMS msg id.
- 5094918 SSS-BOOKING-CREATION — MIGRATE deposit SMS (module 10) from legacy HTTP api.quosms.com (hardcoded bearer token) to native open-phone:sendATextMessageSms. Same copy, same Stripe link, onerror Resume (9001) preserved. Audit module 11 extended to log SMS msg id.

## Phone normalization (E.164, US default), applied to module 10 (1.Phone) and module 40 (2.phone):
{{if(length(replace(P;"/[^0-9]/g";""))=10; "+1"+replace(P;"/[^0-9]/g";"");
   if(length(replace(P;"/[^0-9]/g";""))=11; "+"+replace(P;"/[^0-9]/g";"");
      replace(P;"/[^0-9]/g";"")))}}
- 7083085386 -> +17083085386 ; (708) 308-5386 -> +17083085386 ; 708-308-5386 -> +17083085386 ; +17083085386 -> +17083085386
- Other lengths fall through as digits-only (invalid -> Quo rejects -> Resume, non-blocking).

## Files
- *_ORIGINAL.blueprint.json  = exact pre-change snapshot (ROLLBACK SOURCE)
- *_PROPOSED.blueprint.json   = deployed version

## Rollback
scenarios_update(scenarioId, blueprint=<ORIGINAL file contents>) for the affected scenario.
