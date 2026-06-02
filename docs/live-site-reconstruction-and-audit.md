# She Said Sail: Live Site Reconstruction and Audit

Based on the full WordPress export (shesaidsail.WordPress.20260602.xml, 1231 items, 11.7 MB) combined with the Elementor Website Kit export. Every claim below cites evidence from those files. No assumptions.

## Do I have enough to reconstruct the site

Yes, enough to reconstruct architecture, content, and data model. Minor items still missing for a full optimization pass are listed at the end, but they do not block this report.

## 1. Website architecture summary

Evidence (post type counts from the export):
- 18 pages (published), 10 yacht, 4 experience, 55 elementor_library, 7 elementor_snippet, 3 acf-field-group, 34 acf-field, 2 acf-post-type, 4 acf-taxonomy, 3 metform-form, 75 metform-entry, 994 attachment, 6 post, 12 nav_menu_item, 2 wp_global_styles, 1 custom_css, 1 wp_navigation.

Published pages and real slugs:
- /home/ (Home), /yachts/ (Yachts), /experiences/ (Experiences), /request-to-book/ (Request to Book), /faq/ (FAQ's), /about-4/ (About), /thank-you/ (Thank You)
- Landing pages: /bachelorette/, /birthday/, /girls-trip/, /luxury-concierge/, /day-club/, /sunset-golden-hour/, /miami-yacht-experience/
- Legal: /terms-conditions/, /terms-of-service/, /copyright-policy/, /privacy-policy/

Rendering model: WordPress plus Elementor Pro plus ElementsKit plus ACF Pro plus MetForm, on the Ova theme (ova_framework header and footer elements in the kit). Yacht and experience pages are Elementor Pro Theme Builder templates using dynamic tags bound to ACF field keys (confirmed: field_69b75215971c3 and similar appear in templates 6000, 6007, 6733). 8 templates use __dynamic__.

Lead capture is live and working: 75 metform-entry records exist, meaning the site has already captured 75 form submissions.

## 2. Yacht architecture summary

Custom post type: yacht. 10 posts, all published:
Another One, Sugaree, GTX80, Compass, Carpe Diem, Gatsby, Mirracle, Freedom, Vasiliki, IV Tranquility.

ACF group "Yacht Fields" (id 5949), 11 fields:
On Board Features, 4 Hour Charter Rate, 6 Hour Charter Rate, 8 Hour Charter Rate, Year, Guests, Length, Cabins, Exterior Gallery, Interior Gallery, Starting Price.

Real starting prices (from postmeta): Gatsby $17,250, Sugaree $15,500, GTX80 $18,500, Compass $20,900, Mirracle $14,250, Freedom $11,500, Vasiliki $10,900, IV Tranquility $10,900, Carpe Diem $9,900, Another One $25,000.

Critical data integrity issue: pricing is stored in three overlapping structures, only partially populated.
1. Flat rates on Yacht Fields: starting_price, 4_hour_charter_rate, 6_hour_charter_rate, 8_hour_charter_rate (all 10).
2. Experience matrix: pricing_price_{4,6,8}hr_{rose,sunset,pinkpalm,monaco} plus a serialized pricing field (present on 9 of 10 yachts, so one yacht, likely Another One, is missing the matrix).
3. Newer namespaced group "Yacht Pricing" (id 6941, fields Available Durations and Pricing): yacht_pricing_* and available_durations (present on only 1 yacht).

So the same prices live in up to three places, and coverage is inconsistent (10 vs 9 vs 1). This must be consolidated before any dynamic pricing or sync work.

## 3. Experience architecture summary

Custom post type: experience. 4 posts, all published:
Rosé Day Club (key rose), Golden Hour Escape (key sunset), Pink Palm Club (key pinkpalm), Monaco Social (key monaco).

ACF group "Experiences" (id 6703), 9 fields:
What's Included, Signature Moment, Signature Styling Kit, Elevated Add Ons, Pricing, Tagline, Best For, Duration, Experience Key.

Real copy confirmed in postmeta, for example Monaco Social What's Included: "Veuve Clicquot champagne upon arrival. A fully styled charcuterie presentation, clean, abundant, ready. A champagne-forward signature cocktail. Curated Riviera-inspired music throughout. Neutral and gold..." and Best For "Celebrations, group hosting, and high-energy social days". Taglines are real per experience.

The experience_key values (rose, sunset, pinkpalm, monaco) are the join keys that match the suffixes on the yacht pricing matrix. That is the dynamic relationship: a yacht page can show a price per experience by reading pricing_price_{duration}hr_{experience_key}.

## 4. Remaining demo content found

Demo markers (lorem ipsum, Peter Lawson, Jhon Malthans, Welson Lux, Odysea, $950/day) by post type:
- elementor_library: 28 items contain demo markers
- post: 6 items (old demo blog posts)
- metform-form: 3 items (placeholder text in form config)
- page (published): 1 item, Day Club, and the only match was the substring "/day", a false positive, not real demo content.

Conclusion: the live pages, yachts, and experiences are essentially clean of demo content. The demo lorem and Peter Lawson live in unused saved templates in the Elementor library and in old demo blog posts. This is why every Elementor template export looked like demo, the library is full of the theme's starter templates, but they are not what renders the live CPT pages. Action: delete or archive the 28 demo library templates and the 6 demo posts so they cannot be accidentally published or indexed.

## 5. Top 10 conversion improvements (from real data)

1. Consolidate the three pricing structures into one. Right now starting_price, the experience matrix, and the yacht_pricing group can disagree, and coverage is 10 vs 9 vs 1. Pick one (recommend the experience matrix plus starting_price) and remove the others. This is the highest priority because inconsistent or missing prices kill high-ticket conversion.
2. Fix the flagship: Another One has a $25,000 starting_price but is the yacht missing the experience matrix (9 of 10 have it). Its per experience prices will render blank. Populate it.
3. Add real testimonials. There are zero real testimonials in the yacht, experience, or page data, only demo ones in the library. Social proof is the single biggest trust gap for a $10k to $44k purchase.
4. Surface experience differentiation on the yacht and pricing pages using the real ACF Best For and Tagline fields (for example Monaco Social, "Celebrations, group hosting, high-energy social days"). The data exists, use it as the self select line.
5. Add weather and rescheduling reassurance near the Request to Book flow (/request-to-book/ is live). Removes the top pre booking anxiety.
6. Resolve yacht name inconsistency (Gatsby vs Gratsky, GTX80 vs CTX 80, Sugaree vs Sugarree, IV Tranquility vs Tranquility IV). Confusing names reduce confidence and break any cross system matching.
7. Strengthen CTAs to luxury confidence language (Check Availability, Reserve Your Date, Talk to a Concierge) consistently across the live templates.
8. Build out the About page (/about-4/) with a real founder story and photo. A human face supports a high trust purchase.
9. Use the 75 captured leads. Confirm MetForm routing and follow up, and add the lead data to the concierge flow. Leads are arriving, make sure none leak.
10. Add a clear How It Works section to Home and Request to Book to remove process anxiety.

## 6. Top 10 SEO improvements (from real data)

1. Install and configure an SEO plugin. There is no Yoast, Rank Math, AIOSEO, or SEOPress meta anywhere in 1231 items. The site currently has no managed titles, meta descriptions, canonicals, or schema. This is the single biggest SEO gap.
2. Fix the About slug. It is /about-4/, which signals deleted and recreated pages. Move to /about/ with a redirect.
3. Consolidate duplicate legal pages. There are four: /terms-conditions/, /terms-of-service/, /copyright-policy/, /privacy-policy/. Overlapping thin pages dilute crawl budget and can create duplicate content. Keep Privacy and one Terms, redirect the rest.
4. Fix the front page. Home lives at /home/. Set it as the WordPress static front page so it serves from the root domain, and redirect /home/ to /.
5. Clean the FAQ naming. The title is "FAQ's" (incorrect apostrophe) and the menu has three inconsistent entries (FAQ's, FAQ, and the HTML entity FAQ&#8217;s). Standardize to FAQs.
6. Add unique title tags and meta descriptions per yacht and per experience, driven by ACF. Target patterns like "Gatsby, Miami Luxury Yacht Charter from $17,250, She Said Sail".
7. Optimize the 994 media attachments. Filenames are stock and generic (artem-pochepetsky-...unsplash.jpg, women-yachting-...). Rename and add alt text using real yacht names plus Miami and Fort Lauderdale keywords.
8. Exploit the intent landing pages already built (/bachelorette/, /birthday/, /girls-trip/, /miami-yacht-experience/, /day-club/, /sunset-golden-hour/). Give each a unique H1, title, and internal links to relevant yachts and experiences targeting queries like "Miami bachelorette yacht charter".
9. Generate and submit an XML sitemap and connect Google Search Console. Neither is evidenced in the export.
10. Add internal linking from experiences and landing pages to the 10 yacht detail pages, and from yachts back to matching experiences, using the experience_key relationship.

## 7. Top 10 AI search improvements (from real data)

1. Add structured data, since there is none today (no SEO plugin). Product or Service schema per yacht with price, capacity, and length lets AI engines quote your fleet directly.
2. Add FAQPage schema to /faq/ with real question and answer pairs so AI assistants can cite answers verbatim.
3. Add LocalBusiness schema with NAP for Miami and Fort Lauderdale so location aware AI answers include She Said Sail.
4. Expose yacht facts as readable text and schema (Guests, Length, Cabins, Year, Starting Price are all in ACF). This lets AI answer "yacht for 12 guests in Miami under 20k".
5. Map experiences to intent. The ACF Best For values (for example "Romantic escapes and scenic evenings" for Golden Hour Escape) align to natural language queries, surface them as plain text.
6. Ensure prices render as server side text, not only inside JavaScript or images, so AI crawlers can read them.
7. Define the brand entity. Add Organization schema with sameAs links to your social profiles to disambiguate "She Said Sail".
8. Confirm robots and any AI crawler rules allow indexing. With no SEO plugin, robots directives are likely defaults, verify GPTBot and similar are not blocked if you want AI visibility.
9. Add concise, factual answer blocks for high intent questions (what is included, weather policy, how booking works) so AI can extract them cleanly.
10. Strengthen E-E-A-T with a real About and author identity. AI engines weight clear authorship and a real operator behind a high value service.

## What is still missing for a complete optimization pass

These were not in the uploads and would sharpen the work, but are not required for this report:
1. The ACF field group export as a standalone file is now effectively covered, the three groups and 34 fields are in this WordPress export. No longer blocking.
2. Live analytics (GA4 or traffic and conversion numbers). The conversion items above are based on structure, not measured funnel data.
3. The live XML sitemap or a definitive list of indexable URLs, to audit exactly what is indexed.
4. Confirmation of Elementor Theme Builder display conditions, to verify which template renders single yacht versus single experience. Strongly inferred from the dynamic templates, not yet seen as explicit conditions.
5. Any existing redirects, to plan the slug fixes safely.
