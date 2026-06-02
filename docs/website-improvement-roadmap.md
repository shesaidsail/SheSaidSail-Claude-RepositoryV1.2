# She Said Sail: Definitive Website Improvement Roadmap

Built on the reconstructed live architecture (see docs/live-site-reconstruction-and-audit.md and docs/site-architecture-and-data-plan.md). Stack: WordPress, Elementor Pro Theme Builder, ElementsKit, ACF Pro, MetForm, Ova theme. Content: 10 yachts and 4 experiences as custom post types rendered via ACF dynamic tags. No SEO plugin present. Pricing fragmented across 3 ACF structures. 75 real leads already captured.

Impact scales are relative to a high-ticket model (charters $9,900 to $44,000). Revenue and booking impact are directional estimates based on site structure, not measured funnel data (no GA4 was provided).

Difficulty: Low (config and content), Medium (ACF and template work), High (custom dev or integration).

---

## Project 1: Pricing consolidation

- Expected revenue impact: High. Wrong or blank prices on a high-ticket page directly lose bookings.
- Expected booking impact: High. Every yacht page depends on a correct price rendering.
- Technical difficulty: Medium.
- Time estimate: 1 to 2 days.

Problem (evidence): prices live in 3 overlapping ACF structures with inconsistent coverage. Flat rates (starting_price, 4 or 6 or 8_hour_charter_rate) on all 10 yachts. Experience matrix pricing_price_{4,6,8}hr_{rose,sunset,pinkpalm,monaco} on 9 of 10. Newer yacht_pricing group on only 1. Another One ($25,000 flagship) is the yacht missing the matrix, so its per experience prices render blank.

Implementation plan:
1. Choose one canonical model: keep starting_price plus the experience matrix (pricing_price_{duration}hr_{experience_key}). Retire the yacht_pricing group (id 6941) and any serialized pricing duplicate.
2. Audit all 10 yachts in a spreadsheet exported from the matrix fields, fill gaps, and populate Another One fully.
3. Update the single yacht Theme Builder template so price displays read only from the canonical fields. Remove dynamic tags pointing at the retired group.
4. Add a visible price table per yacht (4, 6, 8 hour columns by experience) using the matrix, plus a clear Starting From value.
5. Delete the retired ACF group and fields after confirming no template references them.
6. QA every yacht page on desktop and mobile for a correct, non blank price.

---

## Project 2: Rank Math implementation

- Expected revenue impact: Medium to High over 3 to 6 months via organic traffic.
- Expected booking impact: Medium, compounding.
- Technical difficulty: Low to Medium.
- Time estimate: 1 to 2 days setup, then ongoing.

Problem (evidence): no SEO plugin meta anywhere in 1231 items. No managed titles, meta descriptions, canonicals, sitemap, or schema today.

Implementation plan:
1. Install Rank Math, run the setup wizard, connect Google Search Console and Bing.
2. Set title and meta templates for yacht and experience CPTs using ACF variables, for example "%title%, Miami Luxury Yacht Charter from %acf(starting_price)%, She Said Sail".
3. Fix structural SEO issues: move /about-4/ to /about/ with redirect, set Home as the root front page and redirect /home/, standardize FAQ naming, consolidate the 4 legal pages to 2.
4. Configure the XML sitemap and submit to Search Console.
5. Set Organization and LocalBusiness defaults (Miami and Fort Lauderdale NAP, social profiles).
6. Add unique titles, meta, and H1s to the 7 intent landing pages targeting queries like "Miami bachelorette yacht charter".

Note: Rank Math is the delivery mechanism for Project 3 schema, so do this before or with Project 3.

---

## Project 3: AI search schema

- Expected revenue impact: Medium and growing as AI search share rises.
- Expected booking impact: Low to Medium now, strategic later.
- Technical difficulty: Low to Medium (mostly via Rank Math).
- Time estimate: 1 to 2 days after Rank Math.

Problem (evidence): zero structured data today. AI engines cannot reliably read the fleet, prices, or FAQs.

Implementation plan:
1. Product or Service schema per yacht via Rank Math, mapping ACF: name, description, price (starting_price), capacity (guests), length, with areaServed Miami and Fort Lauderdale.
2. FAQPage schema on /faq/ using real question and answer pairs.
3. LocalBusiness and Organization schema sitewide with NAP and sameAs social links.
4. Ensure prices and specs render as server side text, not only in JavaScript or images, so crawlers and AI read them.
5. Verify robots allows AI crawlers (GPTBot and similar) if AI visibility is wanted.
6. Add concise factual answer blocks (what is included, weather policy, how booking works) in plain text for extraction.

---

## Project 4: Yacht page optimization

- Expected revenue impact: High. These are the primary money pages.
- Expected booking impact: High.
- Technical difficulty: Medium.
- Time estimate: 2 to 4 days (template plus content for 10 yachts).

Implementation plan:
1. Depends on Project 1, render correct pricing first.
2. Replace stock specs only layout with outcome led copy plus the spec row (Guests, Length, Cabins, Year from ACF).
3. Show the experience price matrix and a clear Starting From and a strong CTA (Reserve Your Date or Check Availability).
4. Real photography per yacht into the Exterior Gallery and Interior Gallery ACF fields, with alt text using the yacht name plus Miami or Fort Lauderdale.
5. Link each yacht to the experiences it supports using experience_key.
6. Add weather and rescheduling reassurance near the booking form.
7. Lock canonical yacht names (Gatsby, GTX80, Sugaree, IV Tranquility) across title, ACF, and any external system.

---

## Project 5: Experience page optimization

- Expected revenue impact: Medium to High. Experiences drive self selection and upsell.
- Expected booking impact: Medium to High.
- Technical difficulty: Low to Medium.
- Time estimate: 1 to 2 days (4 experiences plus template).

Implementation plan:
1. Surface the real ACF fields already populated: Tagline, Best For, What's Included, Signature Moment, Signature Styling Kit, Elevated Add Ons.
2. On each experience page, show Best For prominently for fast self selection.
3. Cross link each experience to the yachts that offer it and show the from price per yacht via the matrix.
4. Add the Elevated Add Ons as a clear upsell module.
5. Align display names and confirm experience_key mapping (rose, sunset, pinkpalm, monaco) is consistent everywhere.

---

## Project 6: Trust architecture

- Expected revenue impact: High. Trust is the core barrier for a $20k purchase, social proof scored 1 of 10 in the buyer audit.
- Expected booking impact: High.
- Technical difficulty: Low to Medium.
- Time estimate: 2 to 4 days plus content gathering.

Implementation plan:
1. Real testimonials. Create a testimonial source (ACF repeater or a simple CPT) and collect real, permissioned quotes with first name, occasion, vessel. Do not publish invented quotes.
2. Real founder and team on the About page with a photo and a short story.
3. Weather and rescheduling reassurance near pricing and booking.
4. A clear FAQ that answers real anxieties (weather, alcohol, choosing a yacht, how booking works), with FAQPage schema from Project 3.
5. Trust markers: concierge positioning, Miami and Fort Lauderdale coverage, what is included.
6. Remove the 28 demo library templates and 6 demo posts so nothing placeholder can surface or get indexed.

---

## Project 7: Dynamic Airtable pricing sync

- Expected revenue impact: Indirect. Protects against pricing drift and saves operator time.
- Expected booking impact: Low direct, high operational reliability.
- Technical difficulty: High.
- Time estimate: 3 to 5 days.

Prerequisite: Project 1 must be done first. Do not automate a fragmented model.

Implementation plan:
1. Airtable Pricing table, one row per yacht, columns matching the canonical ACF matrix, plus a wp_post_id column and a publish toggle.
2. Enable ACF to REST API and create a dedicated WordPress application password.
3. New Make scenario M-YACHT-PRICING-SYNC: Airtable watch records on update, guard on publish toggle, PATCH /wp-json/wp/v2/yacht/{wp_post_id} with the acf object, write back a synced timestamp, alert via the existing M-SLACK-ALERTS pattern, log via M-AUDIT-LOGGER.
4. One way only, Airtable to WordPress. Match on wp_post_id and experience_key, never on yacht name.
5. Purge SiteGround cache as a final step so new prices show immediately.
6. Reconcile names once and store canonical names in both systems.

---

## Recommended sequence

1. Pricing consolidation (foundation for pages and sync)
2. Rank Math (foundation for SEO and schema)
3. Yacht page optimization
4. Trust architecture
5. Experience page optimization
6. AI search schema
7. Dynamic Airtable pricing sync

---

## Single highest ROI project

Pricing consolidation (Project 1).

Why: it is the highest revenue and booking impact item at only medium difficulty and 1 to 2 days, and it is a hard dependency for the yacht pages, experience pages, and the Airtable sync. Today the flagship Another One and any yacht missing the matrix can render blank or inconsistent prices on a high-ticket purchase, which is a direct, ongoing loss. Fixing it protects every dollar that paid traffic and SEO will later drive, and unblocks the rest of the roadmap. Best return for the least effort, with the broadest downstream benefit.

Close second: Rank Math, because the site currently has no SEO foundation at all, and it is low difficulty with compounding returns and is required for the AI schema work.
