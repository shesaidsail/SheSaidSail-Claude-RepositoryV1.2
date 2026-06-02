# She Said Sail: Pricing Strategy Recommendations

Built entirely on the real pricing matrix in the WordPress export (shesaidsail.WordPress.20260602.xml). Goal: high booking volume, strong profitability, market competitiveness, simplicity, and growth, while staying premium. Target buyer feeling: "surprisingly reasonable for what you get." These are recommendations only. No production pricing is changed.

## Important data note on profitability

The export contains retail pricing only. It does not contain cost of goods (vessel cost to She Said Sail, crew cost, food and beverage and styling cost, payment fees, concierge labor, or CAC). Pricing levels, relationships, and over or underpricing below are fully data grounded. The profit math uses clearly labeled assumptions and is structured so real costs can be dropped in. The exact cost inputs needed are listed at the end.

## 1 and 2. Yacht and experience audit (actual current pricing)

All yachts cap at 12 guests. Base = 4 hour Rosé (equals the starting_price).

| Yacht | Length | Cabins | Base (4hr Rosé) | 8hr Monaco (top) | $ per ft (base) | Matrix complete |
|---|---|---|---|---|---|---|
| Carpe Diem | 95ft | 6 | $9,900 | $17,400 | $104 | yes |
| Vasiliki | 76ft | 4 | $10,900 | $19,300 | $143 | yes |
| IV Tranquility | 94ft | 4 | $10,900 | $21,000 | $116 | yes |
| Freedom | 88ft | 4 | $11,500 | $20,400 | $131 | yes |
| Mirracle | 95ft | 4 | $14,250 | $24,250 | $150 | yes |
| Sugaree | 72ft | 3 | $15,500 | $25,900 | $215 | yes |
| Gatsby | 96ft | 4 | $17,250 | $27,900 | $180 | yes |
| GTX80 | 80ft | 3 | $18,500 | $31,500 | $231 | yes |
| Compass | 88ft | 5 | 8hr only $20,900 | $25,900 | n/a | 8hr only |
| Another One | 112ft | 4 | flagship $25,000 | $25,000 (8hr) | n/a | none |

Experience premium structure (consistent across the fleet, measured from the matrix):
- Rosé: base, 1.00
- Golden Hour Escape: about +6 percent (1.06)
- Pink Palm Club: about +12 percent (1.12)
- Monaco Social: about +22 percent (1.22)

Duration structure (measured): 4hr 1.00, 6hr about +16 percent (1.16), 8hr about +33 percent (1.33).

## 3. Likely market positioning

Miami and Fort Lauderdale charters typically advertise an hourly vessel rate that excludes crew gratuity, fuel, food, and drinks. She Said Sail prices are all inclusive and produced (captain, crew, premium beverages, florals, charcuterie, styling, concierge). So a like for like comparison should add roughly 20 to 40 percent to a competitor's headline rate before comparing. Against that, the She Said Sail mid and upper boats are priced at a real premium, and the entry boats are competitive. The brand currently reads as upper premium, not as the easy yes the founder wants.

## 4. Pricing relationship analysis (internal consistency)

Because all boats seat 12, dollar per foot is a fair internal sanity check. The fleet is inconsistent:
- High per foot: GTX80 $231, Sugaree $215, Gatsby $180.
- Low per foot: Carpe Diem $104, IV Tranquility $116, Freedom $131, Vasiliki $143.

Sugaree (the smallest boat at 72ft) and GTX80 (80ft) are priced above larger, higher cabin boats like Mirracle (95ft) and IV Tranquility (94ft). A buyer comparing a 72ft Sugaree at $15,500 against a 95ft Mirracle at $14,250 sees an inconsistency that erodes trust.

## 5. Overpriced offerings (relative to the fleet and the easy yes goal)
- Sugaree: smallest boat, second highest base. Overpriced by roughly 15 to 20 percent.
- GTX80: highest per foot. Premium sport yacht can carry some premium, but the gap is too wide for a volume goal.
- Gatsby: strong vessel, but $17,250 base and $27,900 top is steep for the easy yes positioning.

## 6. Underpriced or value offerings (good volume magnets)
- Carpe Diem: 95ft, 6 cabins, $9,900. Excellent value, the natural volume leader and entry hook.
- IV Tranquility and Vasiliki: solid value, good for first time buyers.
- Freedom: well placed.

## 7. New recommended pricing structure (simple, rules based)

Move from 120 hand keyed prices (10 yachts times 3 durations times 4 experiences) to a simple system: one base price per yacht plus two small global multiplier tables. This is the core simplicity and growth recommendation, and it maps directly to the Airtable and ACF architecture below.

Rules (rounded to the nearest $100):
- Duration: 4hr 1.00, 6hr 1.16, 8hr 1.33
- Experience: Rosé 1.00, Golden Hour 1.06, Pink Palm 1.12, Monaco 1.22
- Any cell = base times duration multiplier times experience multiplier, rounded to $100.

These multipliers match the current real structure, so only the base price changes per yacht. That keeps the matrix coherent and lets pricing be managed by editing 10 numbers, not 120.

### Three models (base price = 4hr Rosé per yacht)

| Yacht | Current base | Competitive (volume) | Balanced | Market Leader (final) |
|---|---|---|---|---|
| Carpe Diem | $9,900 | $7,900 | $8,900 | $8,900 |
| Vasiliki | $10,900 | $8,900 | $9,500 | $9,500 |
| IV Tranquility | $10,900 | $9,500 | $9,900 | $9,900 |
| Freedom | $11,500 | $9,900 | $10,900 | $10,900 |
| Mirracle | $14,250 | $11,500 | $12,500 | $12,500 |
| Sugaree | $15,500 | $11,900 | $12,900 | $12,500 |
| Gatsby | $17,250 | $13,900 | $14,900 | $14,900 |
| GTX80 | $18,500 | $14,900 | $16,500 | $15,900 |
| Compass | $20,900 (8hr) | base $13,900 | base $14,900 | base $14,900 |
| Another One | $25,000 (8hr) | base $17,900 | base $18,900 | base $18,900 |

Notes: Compass and Another One get a full computed matrix from their base, fixing the current gaps. Market Leader nudges the two overpriced boats (Sugaree, GTX80) closer to the fleet line for consistency.

### Per yacht detail (Market Leader, the recommended final)

Base shown is 4hr Rosé. Full matrix derives from the multipliers.

| Yacht | Current base | Recommended base | Change | Reasoning | Booking impact | Profit impact |
|---|---|---|---|---|---|---|
| Carpe Diem | $9,900 | $8,900 | -10% | Entry hook under $9k, the easy yes magnet | High increase | Lower per unit, highest volume, strong total |
| Vasiliki | $10,900 | $9,500 | -13% | Smallest value boat, accessible first charter | Increase | Slight per unit dip, volume offsets |
| IV Tranquility | $10,900 | $9,900 | -9% | Clean sub $10k value | Increase | Neutral to positive via volume |
| Freedom | $11,500 | $10,900 | -5% | Already well placed, minor trim | Slight increase | Near neutral |
| Mirracle | $14,250 | $12,500 | -12% | 95ft should beat 72ft Sugaree, realign | Increase | Volume offsets per unit |
| Sugaree | $15,500 | $12,500 | -19% | Overpriced per foot as the smallest boat | High increase | Per unit down, large volume gain expected |
| Gatsby | $17,250 | $14,900 | -14% | Strong signature boat at an easier yes price | Increase | Volume offsets |
| GTX80 | $18,500 | $15,900 | -14% | Premium sport yacht, trim the outlier premium | Increase | Volume offsets |
| Compass | $20,900 (8hr) | $14,900 base | new matrix | Fix missing 4 and 6hr, open more booking windows | High increase | More billable slots |
| Another One | $25,000 | $18,900 base | new matrix | Flagship stays top, but bookable across durations | Increase | Captures lost mid bookings |

Resulting headline: a true "from $8,900" entry, a clean mid around $12,500 to $14,900, and a flagship that tops out near $25,000 at 8hr Monaco rather than feeling out of reach at every tier.

## Are the experience premiums justified

Yes, and they are well structured. Golden Hour at about +6 percent, Pink Palm at about +12 percent, and Monaco at about +22 percent are gentle, logical steps that encourage upgrades rather than blocking them. Recommendation: keep these multipliers. They are easy to say yes to and they protect margin on the upgrade path. The only change is to compute them from the base rather than store them by hand.

Per experience meaning to surface on the site (from real ACF Best For):
- Rosé Day Club: day parties, birthdays, relaxed social groups. The accessible default.
- Golden Hour Escape: romantic escapes and scenic evenings. Small premium.
- Pink Palm Club: bold Miami energy, half or full day. Most booked style.
- Monaco Social: celebrations and high energy hosting. Top tier.

## Final recommendation: one structure

Adopt the Market Leader base prices plus the rules based multipliers. Reasons: it lowers the entry to a true under $9k easy yes, fixes the Sugaree and GTX80 inconsistencies, fills the Compass and Another One gaps, keeps the sensible experience and duration premiums, and collapses pricing management to 10 base numbers. It reads as surprisingly reasonable for an all inclusive produced experience, without abandoning premium positioning at the top.

## Profitability framework and the $10,000 monthly burn

Worked example with labeled assumptions (replace with real costs):
- Assume average booking value about $13,000 (mid of the new range).
- Assume variable costs: vessel cost 50 percent, experience delivery (F&B, florals, styling, crew gratuity contribution) about $2,500, payment fees 3 percent, concierge labor about $300 per booking.
- Estimated contribution per booking under these assumptions is roughly $3,300 to $4,000.
- To cover $10,000 monthly overhead requires roughly 3 bookings per month before marketing, or about 4 to 5 once a reasonable CAC is included.

Implication: even at the lower Market Leader prices, the model is profitable at low volume because absolute margins per booking are large. This supports pricing for volume rather than for maximum price. Final confirmation requires the real cost inputs below.

## Cost inputs needed to finalize profit modeling
1. Vessel cost to She Said Sail per yacht (fixed charter cost or revenue share percent).
2. Experience delivery cost per experience tier (F&B, florals, charcuterie, styling, staff).
3. Crew and captain cost and gratuity handling.
4. Payment processing rate (Stripe).
5. Concierge labor cost per booking.
6. Current blended CAC or target marketing cost per booking.

---

# Airtable and ACF pricing architecture for the new model

Designed for the rules based model. Source of truth in Airtable, published cache in ACF, computed matrix.

## Airtable
Table: Yachts (one row per yacht)
- Fields: yacht_name, wp_post_id, base_price (4hr Rosé), active, publish_to_site (checkbox), last_synced
- Optional override fields per cell only when a yacht needs a manual exception.

Table: Pricing Rules (small, global)
- Duration multipliers: 4hr 1.00, 6hr 1.16, 8hr 1.33
- Experience multipliers: rose 1.00, golden 1.06, pinkpalm 1.12, monaco 1.22

Computation: an Airtable formula or a Make step computes the 12 cell matrix per yacht from base_price times the two multipliers, rounded to $100. The team edits only base_price and, rarely, the global multipliers.

## ACF
Keep the existing experience matrix fields as the published cache the templates already read: starting_price plus pricing_price_{4,6,8}hr_{rose,sunset,pinkpalm,monaco}. Retire the duplicate yacht_pricing group (id 6941) and any serialized pricing field so there is one rendering source. The single yacht template reads only these fields.

## Sync (one way, Airtable to WordPress)
Reuse the planned M-YACHT-PRICING-SYNC Make scenario:
1. Trigger on Airtable record update where publish_to_site is true.
2. Compute the 12 cell matrix (or read computed fields).
3. PATCH /wp-json/wp/v2/yacht/{wp_post_id} with the acf object setting starting_price and the 12 matrix fields.
4. Write last_synced back to Airtable, alert via M-SLACK-ALERTS, log via M-AUDIT-LOGGER.
5. Purge SiteGround cache so new prices show immediately.
Match on wp_post_id and experience_key. Never match on yacht name, because names differ across systems (Gatsby vs Gratsky, GTX80 vs CTX 80, Sugaree vs Sugarree, IV Tranquility vs Tranquility IV).

## Why this is operationally simple
Pricing for the entire fleet becomes 10 base numbers plus 2 tiny multiplier tables. Change a base in Airtable, the matrix recomputes, the site updates through one safe one way sync. No more hand editing 120 cells, and the flagship and Compass gaps cannot recur because every cell is computed.
