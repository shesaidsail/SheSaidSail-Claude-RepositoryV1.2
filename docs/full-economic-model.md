# She Said Sail: Full Economic Model and Pricing Scenarios

Objective: not maximum margin and not minimum price. Optimize for fast market penetration, high booking volume, strong review and referral generation, and sustainable profitability. Built on the live Airtable cost model, the real pricing matrix, and 2026 Miami competitor research. No production pricing is changed. The Sandbox profitability engine (Package Economics Engine table) implements these calculations live.

## One unresolved input (state plainly)

The actual broker rate per yacht is still not stored in Airtable. It is the only number that turns the margins below from well grounded estimates into exact figures. For this model the vessel cost is anchored to real 2026 Miami charter rates (below), which is a defensible external benchmark. Replace with the true broker rate in the engine to finalize.

## Competitor research (2026 Miami market)

- Mid luxury yachts (Marquis 66, Azimut 64 class) run about $4,500 to $5,000 for 4 hours.
- 65 to 85ft yachts run about $5,000 to $12,000 per half day. 70 to 100ft run about $8,000 to $14,000 per full day.
- Most listed rates include captain, crew, fuel, and dockage, but food, beverages, decor, and gratuity are extra and add 30 to 50 percent.
- Bachelorette focused operators (Feeling Yachty, Aqua, South Beach Party Boats) cap most yachts at 12 to 13 guests, durations 4 to 6 hours or full day, and sell decor and add ons separately.
- Peak season (December to May) runs 15 to 30 percent above off peak.

Positioning read: She Said Sail sells a fully produced, all inclusive experience (champagne, charcuterie, florals, styling, concierge) where competitors sell a charter plus a la carte extras. The right comparison is competitor charter plus 30 to 50 percent for the extras a client would otherwise assemble. Even on that basis, She Said Sail current prices sit at a real premium, which is exactly why an aggressive penetration price is on the table.

## Variable costs (per charter, representative mid yacht, 12 guests, 6 hours)

Anchored to real data where it exists ($550 labor from Airtable, $100 per guest gift bags per founder), and to market charter rates for the vessel.

| Component | Basis | Rosé | Golden Hour | Pink Palm | Monaco |
|---|---|---|---|---|---|
| Yacht cost (broker rate x 90%) | Market 6hr charter, ASSUMPTION | $6,000 | $6,000 | $6,000 | $6,000 |
| Captain | Bundled in broker rate (vessel) | included | included | included | included |
| Crew | Bundled in broker rate (vessel) | included | included | included | included |
| Fuel | CLIENT PAID pass-through, not an SSS cost | $0 | $0 | $0 | $0 |
| Concierge labor | Airtable $550 flat | $550 | $550 | $550 | $550 |
| Gift bags | $100 per guest x 12 | $1,200 | $1,200 | $1,200 | $1,200 |
| Decor and styling | tier based | $500 | $600 | $900 | $1,200 |
| Food and beverage | tier based (Monaco adds Veuve, caviar) | $1,400 | $1,600 | $2,200 | $2,800 |
| Transportation credits | flat | $150 | $150 | $150 | $150 |
| Credit card fees | about 3% of revenue | varies | varies | varies | varies |
| Sales commission | 5% referral, blended about 2.5% | varies | varies | varies | varies |

Note: captain and crew are bundled in the broker rate. Fuel, gratuity, and tax are NOT in the package price, they are billed to the client on top, so they are margin neutral pass-throughs for She Said Sail (see next section). If your broker rate is bareboat, move captain and crew into their own cost fields in the engine, which already exist.

## Pass-through items (client paid, margin neutral)

The package prices below do not include these. They are added to the client total and washed through, so they are neither She Said Sail revenue nor cost:
- Fuel surcharge. Billed to the client. If the broker rate includes fuel, She Said Sail bills a matching surcharge, net zero.
- Gratuity. Typically 18 to 20 percent, paid by the client to captain and crew. Not She Said Sail revenue or cost.
- Sales and use tax. Miami 7 percent, Fort Lauderdale 6 percent. Collected and remitted.

Client out the door price example, Rosé Day Club 6hr at $16,900: package $16,900 plus fuel surcharge (say $600) plus gratuity at 18 percent on the charter portion (about $3,000) plus 7 percent Miami tax (about $1,183) equals roughly $21,700 all in. This matters for two reasons: it is the number the client actually compares, and it confirms the competitive read, because Miami competitors add the same fuel, gratuity, and tax on top of their charter rate. The like for like base comparison is therefore cleaner than it first appears, and the She Said Sail premium is for the produced experience (styling, F&B, concierge), not for bundling pass-throughs.

## Per package economics at current pricing (Mirracle class, 6 hours)

Because fuel is client paid, it is removed from the cost stack, which raises contribution by roughly the fuel amount versus a fuel inclusive model. Fixed per booking cost before fees: yacht $6,000 + labor $550 + gift $1,200 + transport $150 = $7,900, plus the tier decor and F&B, plus 3% card and 2.5% commission on revenue. Gratuity and tax do not appear because they are pass-throughs.

| Package | Current price | Variable cost (ex fuel) | Contribution | Contribution margin |
|---|---|---|---|---|
| Rosé Day Club | $16,900 | about $10,730 | about $6,170 | about 37% |
| Golden Hour Escape | $17,950 | about $11,260 | about $6,690 | about 37% |
| Pink Palm Club | $19,050 | about $12,250 | about $6,800 | about 36% |
| Monaco Social | $20,900 | about $13,050 | about $7,850 | about 38% |

Takeaway: with fuel, gratuity, and tax handled as client paid pass-throughs, the package price is close to net experience revenue, and contribution margins are a healthy 36 to 38 percent (higher than a fuel inclusive model would show). There is real room to lower price for penetration and still clear the 30 percent floor. Note: the broker rate above is assumed to be vessel and crew only. If it currently includes fuel, lower the yacht cost by the fuel amount and add the matching client surcharge, which lifts contribution by roughly $500 to $1,000 and margins toward 40 percent.

## Fixed costs and break even

Founder stated overhead is $10,000 per month, which we treat as the all in fixed cost (office, software, Airtable, Make, Tidio, website, staff, and an advertising allocation).

- Average contribution per booking at current mid fleet pricing is about $6,800.
- Break even = $10,000 / $6,800, which is about 1.5 bookings per month.
- At 30 percent margin on a $15,000 booking, contribution is about $4,500, so break even is about 2.2 bookings per month.

The business breaks even at roughly 2 bookings per month. This is the single most important fact for strategy: margins per booking are large relative to overhead, so the right move is to price for volume and flywheel (reviews and referrals), not for maximum margin.

## Net profit per booking (representative)

Net profit per booking equals contribution minus the per booking share of the $10,000 fixed cost. At 10 bookings per month, fixed is $1,000 per booking, so net profit per booking is about $5,800 (Balanced). At 20 bookings, fixed is $500 per booking, so net is about $6,300.

## Three strategy scenarios

All respect the 30 percent contribution floor. Differences are price level, resulting margin, and the volume and growth the price is designed to produce.

### A. Market Share Strategy (aggressive)
- Pricing: about 15 percent below current. Mid yacht Rosé 6hr near $14,500.
- Avg booking value about $14,500. Variable about $9,300. Contribution about $5,200. Margin about 36 percent.
- Booking assumption: fastest penetration. Designed to reach 20 to 40 bookings per month within two to three seasons by being the easiest yes in the market and compounding reviews and referrals.
- Trade off: lowest price per booking, highest volume, strongest review and referral flywheel. Still profitable because vessel cost is largely fixed and the floor holds.

### B. Balanced Strategy (recommended)
- Pricing: about 8 to 10 percent below current. Mid yacht Rosé 6hr near $15,500 to $16,000.
- Avg booking value about $16,000. Variable about $10,000. Contribution about $6,000. Margin about 37 to 38 percent.
- Booking assumption: steady strong growth to 10 to 20 bookings per month. Competitive enough to win comparison shoppers, rich enough margin to fund growth.
- Trade off: best blend of penetration and sustainable profit. The standing model.

### C. Premium Strategy
- Pricing: hold current or raise slightly. Mid yacht Rosé 6hr $16,900 and up, flagship to $44,000.
- Avg booking value about $19,000. Variable about $11,200. Contribution about $7,800. Margin about 41 percent.
- Booking assumption: lower volume, 5 to 10 bookings per month, luxury positioning, slower review and referral accumulation.
- Trade off: highest margin per booking, slowest market penetration. Best reserved for the flagship Another One and peak weekends, not the whole fleet.

## Monthly projections by scenario

Net profit = bookings times contribution per booking minus $10,000 fixed.

### A. Market Share (contribution about $5,200 per booking, avg price $14,500)
| Bookings/mo | Revenue | Contribution | Net profit |
|---|---|---|---|
| 5 | $72,500 | $26,000 | $16,000 |
| 10 | $145,000 | $52,000 | $42,000 |
| 20 | $290,000 | $104,000 | $94,000 |
| 40 | $580,000 | $208,000 | $198,000 |

### B. Balanced (contribution about $6,000 per booking, avg price $16,000)
| Bookings/mo | Revenue | Contribution | Net profit |
|---|---|---|---|
| 5 | $80,000 | $30,000 | $20,000 |
| 10 | $160,000 | $60,000 | $50,000 |
| 20 | $320,000 | $120,000 | $110,000 |
| 40 | $640,000 | $240,000 | $230,000 |

### C. Premium (contribution about $7,800 per booking, avg price $19,000)
| Bookings/mo | Revenue | Contribution | Net profit |
|---|---|---|---|
| 5 | $95,000 | $39,000 | $29,000 |
| 10 | $190,000 | $78,000 | $68,000 |
| 20 | $380,000 | $156,000 | $146,000 |
| 40 | $760,000 | $312,000 | $302,000 |

All three are highly profitable at 10 plus bookings per month. The difference is how fast you get there. Market Share and Balanced reach higher volume sooner because they are easier to say yes to and generate reviews and referrals faster.

## Recommendation

Given the stated goals (penetration, volume, reviews, referrals, sustainable profit, explicitly not maximum margin and not minimum price):

1. Adopt the Balanced Strategy as the standing price (about 8 to 10 percent below current, mid yacht Rosé near $15,500 to $16,000, entry near $9,500). It is competitive against the all in comparison, holds about 37 percent contribution, and funds growth.
2. Run a time boxed Market Share launch price for the first one to two seasons on the entry and mid yachts only, to seed reviews and referrals quickly, then settle to Balanced. Frame it as a founding client rate, not a permanent discount, to protect positioning.
3. Reserve the Premium Strategy for the flagship Another One and peak weekends, where volume is naturally capped and margin should be maximized.
4. Keep the experience premiums as they are (about plus 6, 12, 22 percent). They are high margin upsells that raise average booking value without hurting penetration.

This produces the most bookings and the strongest review and referral flywheel while staying comfortably profitable, and it tops out the flagship for margin where volume is not the constraint.

## How this connects to the Sandbox engine

The Package Economics Engine table in the SSS Sandbox already computes Total Cost, Gross Profit, Margin %, the sub 30 percent warning, and Monthly Contribution per package. To turn this model into live numbers:
1. Enter the real broker rate (or the itemized yacht, captain, crew, fuel) per yacht and duration.
2. Enter F&B, decor (in F&B or its own field), gift bags, transportation per tier.
3. The engine flags any scenario price that breaks the 30 percent floor automatically.
4. Choose the scenario price column, validate all green, then replicate the fields and formulas to the production Packages table and sync to ACF via the planned M-YACHT-PRICING-SYNC scenario.

Nothing is replicated to production until you approve.
