# She Said Sail: Economics Based Pricing Strategy and Architecture

Built from the live Airtable bases (She Said Sail appdZ49WqgjRXxA1R, Financials apprDKQtV2GInThwE) plus the WordPress export. This replaces assumption based pricing with the real cost model found in Airtable. No production pricing is changed.

## Data sources audited

| Source | Result |
|---|---|
| Airtable: Packages (137 records) | Full retail matrix present. She Said Sail cost fields EMPTY. Mare Executive cost fields populated. |
| Airtable: P&L Per Charter (Financials) | 0 records. No historical margin data. |
| Airtable: Bookings | 0 records. No confirmed bookings. |
| Airtable: Requests (inquiries) | 2 records only (test stage). |
| Airtable: Yachts | 10 yachts, broker linked, but no broker rate field on the yacht. |
| Airtable: Cities | City Manager Payout %, tax rates (Miami 7, Fort Lauderdale 6). |
| WordPress export | Confirms the same retail matrix as ACF. |

Conclusion: the business is pre launch. There is no historical booking, margin, or package selection data to mine. The cost model exists as targets and formulas, but the She Said Sail cost inputs are not filled in.

## The real cost model (from Airtable)

Documented in the P&L Per Charter table and confirmed by populated Mare Executive package records:
- Boat Cost = broker rate times 90 percent. The broker rate is the all in vessel cost (vessel, captain, crew, fuel are bundled by the broker). She Said Sail keeps the 10 percent.
- Labor Cost = $550 flat per charter ($800 for full day in Mare examples).
- F&B Cost = variable. Mare examples: $320 (2hr), $1,020 to $1,175 (4hr), $1,400 (6hr).
- Margin Floor = 30 percent for She Said Sail (Mare 35 to 40 percent).
- City Manager Payout = 10 percent of net profit.
- Referral Commission = 5 percent of package price (referred bookings only).
- Tax = pass through, not a cost (Miami 7 percent, Fort Lauderdale 6 percent).

Real Mare Executive cost ratios (evidence): a $5,800 charter had vessel $2,200, labor $550, F&B $1,020, total cost $3,770, margin 35 percent. A $9,500 charter had vessel $3,500, labor $800, F&B $1,400, total $5,700, margin 40 percent. So vessel cost runs about 37 to 40 percent of retail and total cost about 60 to 65 percent.

## Missing Airtable fields (must be filled to finalize true margins)

1. Packages (She Said Sail): Vessel_Cost_Target, F&B_Cost_Target, Labor_Cost_Target are empty on all She Said Sail rows. Because of this, Implied_Margin shows 100 percent, which is not real.
2. Yachts: no Broker Rate field. Boat Cost depends on broker rate times 90 percent, but the rate per yacht and per duration is not stored anywhere. This is the single most important missing input.
3. No crew, captain, or fuel fields. These are bundled inside the broker rate and cannot be separated from the current data.
4. P&L Per Charter and Bookings are empty, so there is no realized margin, no package mix, and no add on attach rate to analyze.

Until item 2 is filled, all per yacht margins below use a representative vessel cost clearly labeled as an estimate derived from the Mare ratios. Replace with broker rate times 90 percent to finalize.

## Cost model applied (representative, replace vessel cost with real broker rate)

Assumptions used, all labeled:
- Vessel cost per 4 hour charter (estimate): entry boats about $4,000, mid about $5,500, premium about $7,500. Derived from Mare ratios and vessel size. REPLACE with broker rate times 90 percent.
- Labor: $550 (real).
- F&B and styling by experience: Rosé $1,600, Golden Hour $1,800, Pink Palm $2,200, Monaco $2,800 (estimate, no She Said Sail field exists).
- Payment processing: 3 percent of price.
- Margin floor: 30 percent (real).

Key structural insight: the broker rate (vessel cost) is roughly fixed per yacht and duration, not a percentage of the retail price. So the experience premium (Rosé to Monaco) carries almost pure margin, since only F&B and styling rise. And lowering the base price reduces margin dollar for dollar against a fixed vessel cost, which is exactly why the real broker rate is the input that sets the floor.

### Margin floor pricing formula (the rule to adopt)

min_price = (vessel_cost + labor + F&B) / (1 − margin_floor − payment_fee_pct)

Example, entry boat Rosé 4hr at 30 percent floor: (4000 + 550 + 1600) / (1 − 0.30 − 0.03) = 6150 / 0.67 = about $9,180. So an entry Rosé price below about $9,200 breaks the 30 percent floor under these estimates. This is why the entry point should sit near $9,500, not lower, unless the broker rate is actually lower.

## 1 and 2. Yacht and experience economics (current vs recommended)

Base shown is 4hr Rosé. Estimated cost and margin use the assumptions above and must be re run with real broker rates.

| Yacht | Current base | Est. cost | Est. margin | Recommended base | Margin after | Booking impact |
|---|---|---|---|---|---|---|
| Carpe Diem | $9,900 | about $6,450 | about 35% | $9,500 | about 32% | High increase, entry hook |
| Vasiliki | $10,900 | about $6,450 | about 41% | $9,900 | about 35% | Increase |
| IV Tranquility | $10,900 | about $6,450 | about 41% | $10,500 | about 39% | Increase |
| Freedom | $11,500 | about $6,450 | about 44% | $11,500 | about 44% | Hold |
| Mirracle | $14,250 | about $7,950 | about 44% | $12,900 | about 38% | Increase |
| Sugaree | $15,500 | about $7,950 | about 49% | $12,900 | about 38% | High increase, was overpriced |
| Gatsby | $17,250 | about $7,950 | about 54% | $14,900 | about 47% | Increase |
| GTX80 | $18,500 | about $9,950 | about 46% | $15,900 | about 37% | Increase |
| Compass | $20,900 (8hr) | n/a | gaps | base $14,900 (4hr) | about 33% | High increase, fills gaps |
| Another One | $25,000 | n/a | gaps | base $18,900 (4hr) | about 35% | Increase, flagship bookable |

Note: margins above assume the representative vessel cost. The relative story (Sugaree and GTX80 carry the highest margins and the most room to cut, entry boats are tightest) holds regardless, because vessel cost is roughly fixed by size.

## Experience incremental analysis (are the premiums justified)

Because vessel cost is fixed for a given yacht and duration, the only incremental cost from Rosé up to Monaco is F&B and styling. Using the estimates:

| Step | Price premium (Gatsby 4hr) | Incremental cost (F&B) | Incremental profit | Verdict |
|---|---|---|---|---|
| Rosé to Golden Hour | +$1,000 (about +6%) | about +$200 | about +$800 | Strongly justified |
| Rosé to Pink Palm | +$2,100 (about +12%) | about +$600 | about +$1,500 | Strongly justified |
| Rosé to Monaco | +$3,700 (about +22%) | about +$1,200 | about +$2,500 | Strongly justified |

Recommendation: keep the experience premiums exactly as they are (about +6, +12, +22 percent). They are high margin upsells and easy to say yes to. The only change is to compute them from the base rather than store 120 cells by hand.

## 3. Three models

All respect the 30 percent floor. Differences are the target margin band, which sets how aggressive the base prices are.

### Volume Growth Model
Target margin about 30 to 33 percent. Most competitive prices that still clear the floor. Entry near $9,500, mid $12,500 to $14,900, premium from $14,900. Designed to win price sensitive comparison shoppers. Lowest price, thinnest healthy margin.

### Balanced Growth Model (recommended)
Target margin about 35 to 40 percent. The recommended base column above. Strong booking velocity with healthy margin. Entry $9,500, mid $12,900 to $14,900, premium $15,900 plus. Reads as surprisingly reasonable while protecting profit.

### Market Share Model
Target margin about 25 to 28 percent (requires founder sign off, below the 30 percent floor). Most aggressive, used only for launch momentum or specific campaigns, not as standing price. Entry near $8,900. Use temporarily, not permanently, because it breaks the documented floor.

## Overhead allocation ($10,000 per month)

Using the Balanced model and the representative costs, contribution per booking ranges from about $3,400 (entry) to about $7,800 (mid premium), averaging roughly $4,500 to $5,000.
- Overhead breakeven: $10,000 divided by about $4,750 is roughly 2 to 3 bookings per month before marketing.
- Add a reasonable customer acquisition cost and that is roughly 4 to 5 bookings per month to cover overhead plus marketing.

Because absolute margins per booking are large, the model is profitable at very low volume, which is exactly why pricing for volume rather than for maximum price is the right call. Final confirmation requires the real broker rates.

## Final recommendation

Adopt the Balanced Growth Model with the rules based system: one base price per yacht plus the fixed experience and duration multipliers, with every price validated against the 30 percent margin floor formula once real broker rates are entered. Keep the experience premiums as they are. Fill the Compass and Another One gaps. Bring Sugaree and GTX80 down to the fleet line. This produces a true from $9,500 entry, a clean mid, and a flagship that tops out near $25,000, which reads as much better value than expected while protecting a 35 to 40 percent margin.

## Final pricing architecture: Airtable to Make to ACF to Elementor

Airtable is the single source of truth.

1. Airtable Yachts: add Broker_Rate_4hr, Broker_Rate_6hr, Broker_Rate_8hr (the real vessel cost input), Base_Price (4hr Rosé), wp_post_id, publish_to_site, last_synced.
2. Airtable Packages or a small Pricing Rules table: store the experience multipliers (Rosé 1.00, Golden Hour 1.06, Pink Palm 1.12, Monaco 1.22) and duration multipliers (4hr 1.00, 6hr 1.16, 8hr 1.33), F&B_Cost_Target per experience, Labor_Cost $550, Margin_Floor 0.30.
3. Compute: Airtable formulas derive every cell from base times multipliers, and derive margin from price minus (broker rate times 90 percent plus labor plus F&B plus 3 percent). A guard flags any cell below the 30 percent floor.
4. Make scenario M-YACHT-PRICING-SYNC: on Packages or Yachts update where publish_to_site is true, PATCH /wp-json/wp/v2/yacht/{wp_post_id} with the acf object (starting_price and the 12 matrix fields), write last_synced, alert via M-SLACK-ALERTS, log via M-AUDIT-LOGGER, purge SiteGround cache.
5. ACF renders via the existing fields. Elementor single yacht and experience templates already read these via dynamic tags, so no template change is needed once the fields are consistent.
6. One way only, Airtable to WordPress. Match on wp_post_id and experience_key, never on yacht name (names differ: Gatsby vs Gratsky, GTX80 vs CTX 80, Sugaree vs Sugarree, IV Tranquility vs Tranquility IV).

This makes margin a first class, enforced part of pricing: no price can be published that breaks the floor, and the whole fleet is managed by editing base prices and broker rates, not 120 cells.

## What to provide to finalize

1. Broker rate per yacht per duration (4, 6, 8 hour). This is the one input that converts every margin above from estimate to actual.
2. The She Said Sail F&B and styling cost per experience tier (to fill F&B_Cost_Target).
3. Confirmation of the labor figure for She Said Sail (Mare uses $550, full day $800).
Once these three are in Airtable, the model produces real, enforced margins automatically.
