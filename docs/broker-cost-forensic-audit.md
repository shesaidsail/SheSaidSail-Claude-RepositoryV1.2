# Broker Cost Forensic Audit and Structure Build

Economics validation mode. Goal: determine definitively whether broker rates exist in any accessible system before any pricing decision, then build the exact structure to capture them. No production pricing or production Airtable fields were modified. All new structure is in the SSS Sandbox base.

## 1. Forensic audit: every place searched

Searched all 10 Airtable bases visible to the account, with a full field level sweep of the main She Said Sail base (50 tables) and the Financials base, for: Broker Rate, Broker Cost, Vessel Cost, Charter Cost, Base Cost, Cost Basis, Owner Cost, Supplier Cost, Galati, Gale, Charter Rate, Cost Target, Wholesale Rate, Net Rate, Captain Cost, Crew Cost, Yacht Cost. Searched visible fields, formula fields, lookup fields, linked records, field descriptions, table descriptions, and notes fields.

### What exists (the rule and the broker, but not the rates)

- Bookings.Boat Cost (currency). Field description: "Your cost = Gale rate x 90%." Table has 0 records.
- Packages.Vessel_Cost_Target (currency). Description: "Internal cost target for vessel (broker rate x 90%). Bookings.Boat_Cost should not exceed this for margin integrity." Empty on all She Said Sail packages (populated only on Mare Executive packages).
- Packages.F&B_Cost_Target, Labor_Cost_Target. Empty for She Said Sail, populated for Mare Executive.
- Yachts.Broker (linked record). All 10 yachts link to one broker, Mike Felder, the Gale Yachting contact.
- Yachts.Yacht Notes. Holds positioning text only (for example "Premium Miami flagship", "Serene luxury on the water"), no rates.
- Yachts.Starting From (Manual). Empty.
- City_Financials.Boat_Costs and P&L Per Charter.Boat Cost. Aggregate and per charter actuals, both with 0 records (pre launch).

### What does not exist anywhere

- No per yacht broker rate field. There is no Broker Rate, Charter Rate, Wholesale Rate, Net Rate, or Cost Basis field on the Yachts table or any other table.
- No populated vessel cost for any She Said Sail yacht or package.
- No realized cost data, because Bookings, P&L Per Charter, and City_Financials have no records.

### Why the data is missing from Airtable, and where it actually lives

The operating rule is external: Boat Cost equals the Gale Yachting public charter rate times 90 percent. Gale covers captain, crew, and fuel in a regular charter, and She Said Sail operates as a double broker, marking up Gale's rate. Gale does publish per yacht charter rates, but on individual yacht pages, not on the homepage or a single rate card. Those pages are JavaScript rendered, so an automated fetch returns only the page title, which is why the rates cannot be scraped here. They are fully readable by a person, and were simply never copied into Airtable. The fields meant to cache them (Vessel_Cost_Target, Boat Cost) exist but were left empty for She Said Sail.

Conclusion: broker rates do not exist in any Airtable data store, but they do exist publicly on each Gale yacht page. They must be read from Gale and entered once per yacht and duration. Proven, not assumed.

### Confirmed real rate (sourced from the Gale yacht page)

Another One, the Sanlorenzo 112 SX, Gale charter rates: 8 Hours $25,000, Weekly $130,000, tax and gratuity not included. Applying the rule, Broker_Cost_8hr = $25,000 x 0.90 = $22,500. This has been entered into the Sandbox Yacht Broker Rates table as the first real data point.

### Critical finding exposed by the real rate

The live She Said Sail data lists Another One at a starting price of $25,000 for 8 hours. The Gale rate for the same vessel and duration is also $25,000, so the broker cost is $22,500. If $25,000 is actually charged as the selling price, the flagship is sold at roughly cost, and after labor, F&B, gift, and fees it sells at a loss. The correct retail for Another One is the Packages table value (Rosé $35,500 and up), not $25,000. The $25,000 figure on the yacht and pricing data appears to be the Gale cost mistakenly surfaced as a price. Verify and correct before the flagship is bookable, this is a live margin leak, not a rounding issue.

## 2. Structure built (Sandbox only)

Base: SSS Sandbox (appxOoLdiIVt733kV). New table: Yacht Broker Rates (tblOgNyRLbIUoRYon).

Fields:
- Yacht Name (text, primary)
- Broker_Rate_4hr, Broker_Rate_6hr, Broker_Rate_8hr (currency inputs, you populate from Gale)
- Broker_Cost_4hr = Broker_Rate_4hr x 0.90 (formula)
- Broker_Cost_6hr = Broker_Rate_6hr x 0.90 (formula)
- Broker_Cost_8hr = Broker_Rate_8hr x 0.90 (formula)

Seeded with 11 yachts (Carpe Diem, Vasiliki, Tranquility IV, Freedom, Mirracle, Sugarree, Gatsby, GTX 80, Compass, Another One, Carpe Diem Premium), rates left empty. Verification row confirms the rule: a $10,000 Gale rate yields Broker_Cost_4hr of $9,000.

This pairs with the Package Economics Engine table (built earlier in Sandbox): the Boat Cost input there should be set to the matching Broker_Cost from this table for the yacht and duration.

## 3. Recalculation status: one real rate in, ten yachts to go

The model recomputes the moment each Gale rate is entered. One is now in: Another One 8hr cost $22,500. The other rates are readable on each Gale yacht page but cannot be auto scraped here (JavaScript rendered). The Sandbox engine computes Gross Profit, Contribution, Margin %, the sub 30 percent warning, and Monthly Contribution automatically as each rate field is filled.

Worked example with the real rate, Another One 8hr: if sold at the Packages retail Rosé $35,500, then contribution = 35,500 minus boat 22,500 minus labor 550 minus F&B and decor (say 3,500) minus gift (Scenario B, premium tier, 1,200) minus fees 5.5% (1,953) = $5,797, a 16 percent margin, which is below the 30 percent floor. To clear 30 percent on this vessel at an 8 hour Monaco, the price needs to be near the Packages Monaco value ($43,900), where contribution rises to roughly $13,700 and margin to about 31 percent. This shows the flagship economics are tight even at published retail, and confirms the $25,000 list price would be a loss.

What to do: for each of the remaining 10 yachts, read the Gale 4, 6, and 8 hour rates from the yacht page and enter them in Yacht Broker Rates. Everything downstream calculates, and the estimated versus actual comparison can then be produced.

## 4. Gift bag analysis

Gift bag cost is $100 per guest times 12 guests, which is $1,200 per booking. This is large relative to price, so the policy materially changes economics. The monthly spend at 10 bookings is the key number.

| Scenario | Policy | Gift cost per booking (blended) | Gift spend at 10 bookings/mo | Margin impact |
|---|---|---|---|---|
| A | No gift bags | $0 | $0 | Best margins. Entry tiers clear the 30% floor. |
| B | Pink Palm Club and Monaco Social only | about $600 (if half of bookings are premium) | about $6,000 | Protects entry margins, keeps the delighter where price supports it. |
| C | Every booking | $1,200 | $12,000 | At 10 bookings this exceeds the entire $10,000 overhead. Crushes entry margins. |

Margin impact by tier (gift bag as a share of price):
- Entry $9,900: $1,200 is 12.1 percent of revenue. With bags, entry margin falls from roughly 30 percent to roughly 18 percent.
- Mid $17,000: $1,200 is 7.1 percent.
- Monaco $20,900: $1,200 is 5.7 percent.

Booking impact assumptions: a curated gift bag is a delighter that supports reviews and referrals, which are explicit goals. Its effect is strongest on premium, photo forward bookings (Pink Palm, Monaco) and weakest on price sensitive entry buyers, who respond more to the headline price than to a gift bag.

Recommendation: Scenario B. Put gift bags on Pink Palm Club and Monaco Social only, where the price absorbs the cost and the gift reinforces the produced experience. On Rosé Day Club and Golden Hour Escape, offer the existing gift bag as a paid add on (the $195 per guest line already in the catalog) for groups who want it, so it becomes revenue rather than cost. This protects entry profitability, caps gift spend, and still drives reviews and referrals on the premium tiers.

## 5. F&B analysis

| Item | Status | Detail |
|---|---|---|
| Concierge labor $550 | REAL | Airtable P&L and Mare Labor_Cost_Target. Use as is. |
| Mare F&B costs $320 to $1,400 | REAL (sister brand) | Populated Mare packages. Useful ratio anchor, not She Said Sail exact. |
| Experience inclusions | REAL (content) | ACF What's Included per experience (Veuve Clicquot, caviar, charcuterie, florals). Describes what is served, not its cost. |
| She Said Sail F&B per tier ($1,400 to $2,800) | ESTIMATED | My scaling from Mare plus the richer She Said Sail inclusions. Needs confirmation. |
| Decor and styling per tier ($500 to $1,200) | ESTIMATED | No Airtable field exists. Needs a value or a field. |
| Packages.F&B_Cost_Target for She Said Sail | NEEDS INPUT | Field exists, empty for She Said Sail. This is where the real number belongs. |

Bottom line: the only real F&B anchor is the Mare cost band and the inclusion lists. The She Said Sail per tier F&B and decor are estimates and should be entered into F&B_Cost_Target (and a new decor field) once the founder confirms actual catering and styling costs per experience.

## 6. Pricing strategy recalculation (parametric, ready on rate entry)

The three strategies cannot be finalized in dollars until the Gale rates are in. The method is fixed and lives in the engine:

For each package: Contribution = Price minus Boat Cost (Broker_Cost for that yacht and duration) minus Labor ($550) minus F&B minus Decor minus Gift (per Scenario B) minus Transportation minus card fee (3%) minus blended commission (2.5%). Margin = Contribution / Price. The 30 percent warning fires automatically.

Until rates are entered, the best available figures are the audited estimates in docs/economic-model-audit.md (corrected, with gift bags on premium tiers only):
- Market Share: avg price about $14,500, contribution roughly $4,400 to $5,000, margin low 30s.
- Balanced: avg price about $16,000, contribution roughly $5,000 to $5,600, margin mid 30s.
- Premium: avg price about $19,000, contribution roughly $6,300 to $7,000, margin high 30s.
These move directly with the Gale rate, which the sensitivity analysis showed is the dominant driver (a 20 percent broker change moves profit about 29 percent).

## 7. Final recommendation (aligned to growth, reviews, referrals, sustainable profit)

1. Enter the Gale rates first. Nothing else is real until this is done. The structure is ready in Sandbox.
2. Adopt the Balanced price as the standing model, with entry set so that, after a Scenario B gift policy, every package clears the 30 percent floor. Do not drop entry below the floor just to look cheap.
3. Gift bags on Pink Palm Club and Monaco Social only. Paid gift bag add on elsewhere. This funds the review and referral flywheel on premium bookings without breaking entry economics.
4. Run a time boxed founding client launch price on entry and mid yachts to seed reviews and referrals, then settle to Balanced.
5. Reserve Premium pricing for the flagship Another One and peak weekends.
6. Lean into advertising, since the sensitivity analysis showed ad spend is a small fixed slice (a 20 percent increase cut profit only about 2 percent) while volume is the main profit lever.

This maximizes bookings and the review and referral flywheel while staying sustainably profitable, and it stops the two leaks the audit found: below floor entry pricing and gift bags on every booking.

## Audit trail

- Sandbox tables: Package Economics Engine (tbls7UDYzvVZXnDYG), Yacht Broker Rates (tblOgNyRLbIUoRYon).
- Documentation commits: pricing strategy, economics and architecture, full economic model, model audit, and this forensic audit, all on branch claude/confident-johnson-TxYQ9.
- Production She Said Sail base and production pricing: not modified.
