# Airtable Pricing and Profitability Engine: Implementation Record

Built in the SSS Sandbox base (appxOoLdiIVt733kV) only. No production base touched, no production pricing changed, no fields deleted, no Make or ACF dependency altered. This is the validated engine ready for a founder-approved production migration.

## Tables built (Sandbox)

1. Yacht Broker Rates (tblOgNyRLbIUoRYon) — the yacht-level pricing engine.
2. Package Economics Engine (tbls7UDYzvVZXnDYG) — per yacht, duration, experience detail.
3. Add-ons (tbl0H2J3vd80P7oOs) — upsell catalog.

## Field map: Yacht Broker Rates (pricing engine)

Inputs: Yacht Name, Broker_Rate_4hr/6hr/8hr (currency), Current_Price_4hr/6hr/8hr (currency), Recommended_Price_4hr/6hr/8hr (currency), Fleet Tier (Volume/Core Profit/Prestige), Target Margin (percent), Supplier Status (Keep/Renegotiate/Replace/Prestige Only/Candidate), Paid Ads Status (Feature/Do Not Feature/Concierge Only), Homepage Status (Feature/Secondary/Hidden), Notes.

Formulas:
- Broker_Cost_4hr/6hr/8hr = Broker_Rate x 0.90
- Margin_4hr = (Recommended_Price_4hr - Broker_Cost_4hr - 2600 - 5.5% fees) / Recommended_Price_4hr
- Margin_6hr = same with a 2900 stack; Margin_8hr with a 4200 stack
- Margin Warning = if Margin_4hr is below Target Margin, flag BELOW TARGET, else OK

The 2600, 2900, 4200 stacks are the gift-free standard experience cost (labor 550 plus F&B and decor plus transport) at 4, 6, 8 hours. F&B and decor are still estimates.

## Validation results (live in Sandbox)

| Yacht | Tier | Rec 4hr | Margin 4hr | Target | Warning |
|---|---|---|---|---|---|
| Carpe Diem | Volume | $9,900 | 22.8% | 22.5% | OK |
| Freedom | Volume | $11,500 | 28.8% | 22.5% | OK |
| Vasiliki | Volume | $10,900 | 25.2% | 22.5% | OK |
| Tranquility IV | Volume | $10,900 | 21.1% | 22.5% | BELOW TARGET |
| Mirracle | Core | $15,500 | 28.4% | 32.5% | BELOW TARGET |
| Gatsby | Core | $18,500 | 26.9% | 32.5% | BELOW TARGET |
| Sugaree | Renegotiate | $15,500 | 5.1% | 37.5% | BELOW TARGET |
| GTX 80 | Renegotiate | $19,500 | 16.6% | 37.5% | BELOW TARGET |
| Another One | Prestige | $44,000 (8hr) | 33.8% (8hr) | 37.5% | n/a (8hr only) |
| Carpe Diem Premium | Prestige | $38,500 (8hr) | 36.8% (8hr) | 37.5% | n/a (8hr only) |

The warnings are correct and strategic, not errors: Volume mostly clears its 20 to 25% target, Core sits below 32.5% because the market caps the price, and Sugaree and GTX 80 are far below because the Gale cost is too high. These two are flagged Renegotiate, not repriced.

## Field map: Package Economics Engine

Inputs: Package Name, Yacht, Duration (4/6/8 Hours), Experience (Rosé/Golden Hour Escape/Pink Palm Club/Monaco Social), Revenue (price), Boat Cost, Captain Cost, Crew Cost, F&B Cost, Decor Cost, Gift Bag Cost, Gift Bag Included? (checkbox), Transportation Cost, Est Monthly Bookings, Website Publish Status (Draft/Ready/Hold/Published), Founder Approval Status (Pending/Approved/Rejected).

Formulas:
- Total Variable Cost = Boat + Captain + Crew + F&B + Transportation + Decor + Gift Bag
- Gross Profit = Revenue - Total Variable Cost
- Contribution Margin % = Gross Profit / Revenue
- Margin Warning = flag if below 30%
- Monthly Contribution = Gross Profit x Est Monthly Bookings
- Referral Commission = 5% of Revenue (informational)
- City Manager Payout = 10% of Gross Profit (informational)

Gift bag rule encoded: Gift Bag Cost is zero except where Gift Bag Included? is checked (Monaco), or where selected as an add-on. The engine no longer assumes $1,200 on every booking.

Status: structure complete and validated on the seeded rows. Full population of all yacht, duration, experience rows is pending two inputs (real F&B and decor per tier, and the flagship 4hr and 6hr Gale rates). It is mechanical once those arrive.

## Field map: Add-ons

Inputs: Add-On Name, Customer Price, Cost, Included In Package? (None / Monaco only / Monaco + Pink Palm), Active?, Display On Website?, Notes. Formulas: Gross Profit, Margin %.

Seeded and validated: Gift Bags ($195 per guest, 49% margin, Monaco only), Premium Champagne ($1,450, 52%), DJ ($1,750, 49%), Photographer ($2,250, 60%), Private Chef ($3,750, 41%), Florals ($850, 53%), Decor Upgrade ($1,750, 60%), Transportation ($500, 40%), Other (placeholder). Costs are estimates pending confirmation.

## Views to create (manual, Airtable API cannot create views)

In Yacht Broker Rates:
- Fleet Strategy: group by Fleet Tier, show Recommended prices and Margins.
- Paid Ads Fleet: filter Paid Ads Status is Feature.
- Renegotiate Supplier: filter Supplier Status is Renegotiate or Replace.
- Low Margin Warning: filter Margin Warning is BELOW TARGET.
- Homepage Feature: filter Homepage Status is Feature.

In Package Economics Engine:
- Below Target Margin: filter Margin Warning is below 30%.
- Ready for Founder Approval: filter Founder Approval Status is Pending.
- Website Publish Ready: filter Website Publish Status is Ready.
- Monaco Gift Bag Impact: filter Experience is Monaco Social and Gift Bag Included is checked.
- Volume, Core, Prestige Economics: filter by Fleet Tier (via the Yacht link).

In Add-ons:
- Active Add-ons: filter Active is checked.
- High Margin Add-ons: filter Margin % is at or above 50%.
- Website Add-ons: filter Display On Website is checked.

A founder dashboard is an Airtable Interface, also built manually, using these views.

## Production migration plan (after founder approval)

1. Export this field map (this document).
2. Compare against production Yachts and Packages schemas (already inventoried).
3. Production-safe changes are additive only: add new fields, never rename or delete existing ones.
4. Present the migration as: add Broker_Rate and Broker_Cost, Fleet Tier, Target Margin, Recommended prices, Margin formulas, Supplier and Ads and Homepage status to the production Yachts table; populate Packages.Vessel_Cost_Target and F&B_Cost_Target.
5. Wait for founder approval on each price change.
6. Apply additively to production.
7. Validate formulas compute and match Sandbox.
8. Confirm no customer-facing website price changed (no ACF write until separately approved).
9. Confirm Make scenarios still run (they do not read these new fields, so they are unaffected).
10. Confirm ACF sync readiness (the sync is a separate, later, approved step).

## Final report

1. Base updated: SSS Sandbox (appxOoLdiIVt733kV).
2. Sandbox or production: Sandbox only.
3. Tables changed: Yacht Broker Rates, Package Economics Engine, Add-ons (Add-ons newly created).
4. Fields created: 14 on Yacht Broker Rates (current and recommended prices, three margins, warning, supplier and ads and homepage status, notes), 7 on Package Economics Engine (decor, gift bag cost, gift bag included, publish status, approval status, referral commission, city manager payout), and the full Add-ons table plus its two formula fields. Earlier this session: the Broker_Rate and Broker_Cost and Fleet Tier and Target Margin fields.
5. Fields updated: Package Economics Engine Total Cost renamed to Total Variable Cost and extended to include Decor and Gift Bag.
6. Formulas created: Broker_Cost x3, Margin x3, Margin Warning, Add-ons Gross Profit and Margin, engine Referral Commission and City Manager Payout. Total Variable Cost extended.
7. Views: specified for manual creation (API cannot create views).
8. Missing inputs: real F&B and decor cost per tier, flagship 4hr and 6hr Gale rates, Compass Gale rate.
9. Margin warnings: Tranquility IV (just under its volume target), Mirracle and Gatsby (under core target due to market ceiling), Sugaree and GTX 80 (far under, supplier cost too high).
10. Yachts below target: the five above. Volume Carpe Diem, Freedom, Vasiliki clear target.
11. Pricing conflicts: the live data shows Another One near $25,000, which equals the Gale cost. Flagged to correct.
12. Requires founder approval: every recommended price change, and the entire production migration.
13. Exact next step Sandbox to production: founder reviews the validation table above, approves the price changes and the additive field migration, supplies the three missing inputs, then the fields and values are mirrored into the production Yachts and Packages tables additively, with no website or ACF write until separately approved.
