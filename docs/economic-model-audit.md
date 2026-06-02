# Economic Model Audit and Sensitivity Analysis

Purpose: verify every assumption before pricing decisions. This audit reconciles the numbers in docs/full-economic-model.md, corrects two over optimistic figures, and stress tests profit. Nothing in production or pricing is changed.

## Headline findings from the audit

1. Two real, documented inputs: concierge labor ($550 flat) and the cost formulas (Boat Cost = broker rate x 90%, Referral 5%, City Manager 10% of net). Everything else used in the model is an estimate, because the She Said Sail cost fields in Airtable are empty and the per yacht broker rate is not stored anywhere.
2. The earlier per package margins (36 to 38 percent) are correct for a mid yacht at 6 hours, and verified below.
3. The earlier scenario contributions ($5,200 / $6,000 / $7,800) were over optimistic. Reconciled to a full cost stack including the $1,200 gift bag, the honest blended figures are lower, roughly $3,800 / $5,000 / $6,300.
4. New finding: entry yacht bookings (about $9,900 to $11,500) are thin once the full cost stack and $1,200 gift bag load in, around 18 to 26 percent, which can fall below the 30 percent floor. The aggressive entry penetration price needs either a smaller gift bag, or a higher entry price, to stay profitable.
5. Profit is most sensitive to broker cost. A 20 percent rise in broker cost cuts monthly profit about 29 percent. This confirms the broker rate is the number to nail down first.

## Assumption ledger

REAL means it comes from Airtable or a founder statement. ASSUMPTION means I estimated it and it needs confirming.

| Input | Value used | Source | Status | Airtable field | Formula |
|---|---|---|---|---|---|
| Boat cost | $6,000 mid 6hr, or 38% of price blended | Mare Executive vessel ratio 37 to 40%, and competitor 6hr charter $6,500 to $9,000 | ASSUMPTION | P&L Boat Cost fldog4wUfiJgv2683 (desc "Broker rate x 90%"); Packages Vessel_Cost_Target fldn3hedx6nlyRIDz (EMPTY for SSS) | Boat Cost = Broker Rate x 0.90 |
| Captain | $0 incremental | Bundled in Miami broker rate | ASSUMPTION (convention) | Sandbox Captain Cost fldXEQdi2a1bXNBZM (empty) | input |
| Crew | $0 incremental | Bundled in Miami broker rate | ASSUMPTION (convention) | Sandbox Crew Cost fld6cWa2vRAwkK96W (empty) | input |
| Fuel | $0 to SSS | Founder: client paid pass-through | REAL (founder) | none (pass-through) | n/a |
| Gift bags | $1,200 = $100 x 12 | Founder statement | REAL value, ASSUMPTION it applies to every booking | none exists yet | $100 x guests |
| Decor and styling | $500 to $1,200 by tier | Estimate | ASSUMPTION | none (fold into F&B field) | tier based |
| Food and beverage | $1,400 to $2,800 by tier | Mare F&B $320 to $1,400, scaled for SSS produced experience | ASSUMPTION | Packages F&B_Cost_Target fldd7tBGIGEDT6UWE (EMPTY for SSS) | tier based |
| Transportation credits | $150 | Estimate | ASSUMPTION | Sandbox Transportation Cost fldsnjXcMEoy0z46f (empty) | flat |
| Concierge labor | $550 flat | Airtable, P&L desc "$550 flat per charter"; Mare Labor_Cost_Target 550 | REAL | P&L Labor Cost fldts12XKlYmhB1fF; Packages Labor_Cost_Target fldAuqJ250x6OxOEj | flat $550 |
| Credit card fees | 3% of revenue | Stripe standard 2.9% + $0.30 | REAL (standard) | none | 0.03 x Revenue |
| Sales commission | 5% referral, blended 2.5% | Airtable, P&L desc "5% of package price" | REAL rate, ASSUMPTION on 50% blend | P&L Referral Commission fldXiKhnDclAxEmAc | 0.05 x Price x referred share |
| City Manager payout | 10% of net profit | Airtable, P&L desc "10% of net profit" | REAL (applies below contribution) | P&L City Manager Payout fldkJLEQruB4bF2Oc | 0.10 x Net Profit |
| Monthly overhead | $10,000 | Founder statement | REAL (founder) | none | fixed |
| Overhead per booking | $10,000 / bookings | Derived | Derived | none | 10000 / N |

Net of this ledger: the two cost items that move the model most, boat cost and gift bags, are the least anchored. Boat cost is an estimate and gift bags are assumed to apply to every booking.

## Exact math: the 36 to 38 percent per package (mid yacht, Mirracle, 6 hours)

Common cost per booking (fixed-ish): boat $6,000 + labor $550 + gift bags $1,200 + transportation $150 = $7,900. Fee rate on revenue: card 3% + blended commission 2.5% = 5.5%.

Per package: variable = $7,900 + decor + F&B + 5.5% of price. Contribution = price minus variable.

| Package | Price | Decor + F&B | 5.5% fees | Variable | Contribution | Margin |
|---|---|---|---|---|---|---|
| Rosé | $16,900 | $500 + $1,400 = $1,900 | $929 | $10,729 | $6,171 | 36.5% |
| Golden Hour | $17,950 | $600 + $1,600 = $2,200 | $987 | $11,087 | $6,863 | 38.2% |
| Pink Palm | $19,050 | $900 + $2,200 = $3,100 | $1,048 | $12,048 | $7,002 | 36.8% |
| Monaco | $20,900 | $1,200 + $2,800 = $4,000 | $1,150 | $13,050 | $7,850 | 37.6% |

Verified: 36 to 38 percent holds for a mid yacht at 6 hours. (Correction to the prior doc: Golden Hour variable is $11,087 not $11,260, a rounding fix. Conclusion unchanged.)

## Reconciling the scenario contributions ($5,200 / $6,000 / $7,800 were too high)

The scenarios use lower average prices than the Mirracle example, because they blend entry, mid, and premium yachts. With the same full cost stack, the honest blended numbers are lower. Using boat cost at 38 percent of price for a blended booking:

Contribution = Price minus (0.38 x Price boat + 0.055 x Price fees + $1,900 flat labor/gift/transport + $2,500 average decor and F&B)
Contribution = Price x (1 - 0.435) - $4,400 = 0.565 x Price - $4,400

| Scenario | Avg price | 0.565 x price | minus $4,400 | Contribution | Margin | Prior claim |
|---|---|---|---|---|---|---|
| Market Share | $14,500 | $8,193 | | about $3,800 | about 26% | $5,200 (too high) |
| Balanced | $16,000 | $9,040 | | about $4,640 | about 29% | $6,000 (too high) |
| Premium | $19,000 | $10,735 | | about $6,335 | about 33% | $7,800 (too high) |

The earlier figures overstated contribution by roughly 25 to 35 percent, mainly because they did not fully load the $1,200 gift bag and used a lighter cost stack. Corrected, Market Share and Balanced sit at or just below the 30 percent floor on a blended basis.

## New finding: entry yacht economics are thin

Entry yacht, Carpe Diem Rosé 4 hours, $9,900. Assume 4hr boat cost about $4,000, labor $550, gift $1,200, transport $150, decor + F&B about $1,700, fees 5.5% = $545.

Variable = 4,000 + 550 + 1,200 + 150 + 1,700 + 545 = $8,145. Contribution = 9,900 - 8,145 = $1,755, which is 17.7 percent. Below the 30 percent floor.

The drivers are the $1,200 gift bag and the $550 labor, which are flat and therefore heavy on a low priced booking. Two levers fix it: do not put a full $1,200 gift bag on entry bookings, or set the entry price nearer $11,500 to $12,000. This directly affects the penetration strategy, since the cheapest easy yes is the least profitable.

## Base case for sensitivity

Balanced strategy, representative monthly mix at 10 bookings: 40 percent entry (avg $11,000), 40 percent mid (avg $17,000), 20 percent premium (avg $24,000), blended avg price $16,000.

Per booking contribution by segment (full stack, gift bags on all):
- Entry $11,000: variable about $8,605, contribution about $2,395 (21.8%).
- Mid $17,000: variable about $11,235, contribution about $5,765 (33.9%).
- Premium $24,000: variable about $15,220, contribution about $8,780 (36.6%).

Blended contribution per booking = 0.4 x 2,395 + 0.4 x 5,765 + 0.2 x 8,780 = $5,020.

Base monthly profit at 10 bookings = 10 x 5,020 - 10,000 = $40,200. (Prior doc said $50,000. Corrected down to about $40,200.)

## Sensitivity analysis

Base: 10 bookings, $5,020 contribution per booking, $10,000 fixed, net $40,200. Assume the advertising allocation is about $4,000 of the $10,000 fixed.

| Scenario | What changes | New monthly net | Change vs base |
|---|---|---|---|
| Minus 20% volume | 8 bookings | 8 x 5,020 - 10,000 = $30,160 | minus 25% |
| Plus 20% volume | 12 bookings | 12 x 5,020 - 10,000 = $50,240 | plus 25% |
| Plus 20% ad spend | ad $4,000 to $4,800, fixed $10,800 | 10 x 5,020 - 10,800 = $39,400 | minus 2% |
| Plus 20% broker cost | blended boat $5,780 to $6,936, contribution drops $1,156 to $3,864 | 10 x 3,864 - 10,000 = $28,640 | minus 29% |

Reading:
- Volume moves profit roughly one for one in percentage terms (plus or minus 20 percent volume gives plus or minus 25 percent profit). Growth is the main lever.
- Advertising is a small fixed slice, so a 20 percent ad increase barely dents profit (minus 2 percent), as long as it buys at least a little extra volume. This supports spending into growth.
- Broker cost is the dominant risk. A 20 percent broker increase cuts profit 29 percent. This is why the real broker rate must be entered before committing to lower prices.

Combined downside (minus 20% volume and plus 20% broker cost together): 8 x 3,864 - 10,000 = $20,912, still profitable, but less than half the base. Combined upside (plus 20% volume, broker flat): about $50,240.

## What to confirm before pricing decisions

1. Broker rate per yacht and duration. The single largest swing. Replace the 38 percent estimate.
2. Gift bag policy. Is $100 per guest applied to every booking, or only premium tiers, or as a paid add on? At entry prices it is the difference between profitable and below floor.
3. F&B and decor cost per tier. Currently estimated, fields are empty.
4. Referral share. The 2.5 percent blended commission assumes half of bookings are referred.

Once items 1 to 3 are entered into the Sandbox engine, the contribution and the 30 percent warning become exact, and the scenario numbers should be re run from the engine rather than from the estimates above.

## Corrections logged against docs/full-economic-model.md

- Scenario contributions revised from $5,200 / $6,000 / $7,800 to about $3,800 / $5,000 / $6,300 blended.
- Balanced net profit at 10 bookings revised from $50,000 to about $40,200.
- Added the entry yacht thin margin finding and the gift bag policy question.
- The 36 to 38 percent per package figure for a mid yacht at 6 hours is verified and unchanged.
