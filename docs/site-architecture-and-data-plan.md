# She Said Sail: Live Content Architecture and Data Plan

This document explains how the live She Said Sail site actually renders content, why every Elementor export looked like demo content, and the exact export, import, and data sync plan to optimize the real site. It is based on the full Elementor Website Kit export (She_Said_Sail_Live_Site_June_2026.zip), inspected file by file.

## 1. Executive finding: why exports looked like demo

The page and template exports are only the Elementor layout JSON. The live yacht and experience pages are rendered by Elementor Pro Theme Builder templates that use dynamic tags bound to ACF fields on two custom post types. When you export a template, Elementor stores the dynamic binding (the ACF field key), but the static text shown in the editor preview is the template placeholder or last edited demo text, not the live values.

The real values live in the WordPress database as custom post type posts plus ACF postmeta. Those only travel in the WordPress XML (WXR) files inside the kit (wp-content/yacht/yacht.xml and wp-content/experience/experience.xml), not in the Elementor JSON.

So: the Elementor JSON looks like demo, the XML is the real content. Both were always in the kit. We were reading the layout, not the data.

## 2. The live content architecture

### 2a. Yachts (custom post type: yacht)
10 yacht posts, each with ACF fields. Real titles and starting prices confirmed from yacht.xml:

| Yacht (CPT title) | Starting price (ACF) |
|---|---|
| Gatsby | $17,250 |
| Sugaree | $15,500 |
| GTX80 | $18,500 |
| Compass | $20,900 |
| Mirracle | $14,250 |
| Freedom | $11,500 |
| Vasiliki | $10,900 |
| IV Tranquility | $10,900 |
| Carpe Diem | $9,900 |
| Another One | $25,000 |

Yacht ACF fields (postmeta keys): year, length, cabins, guests, starting_price, gallery, interior_gallery, on_board_features, 4_hour_charter_rate, 6_hour_charter_rate, 8_hour_charter_rate, plus a full per experience pricing matrix: pricing_price_{4hr,6hr,8hr}_{rose,sunset,pinkpalm,monaco} (present on 9 of 10).

### 2b. Experiences (custom post type: experience)
4 experience posts, each with ACF fields. Confirmed from experience.xml:

| Experience (CPT title) | experience_key | best_for (ACF) |
|---|---|---|
| Rosé Day Club | rose | Day parties, birthdays and relaxed social groups |
| Golden Hour Escape | sunset | Romantic escapes and scenic evenings |
| Pink Palm Club | pinkpalm | Half-day or full-day |
| Monaco Social | monaco | Celebrations, group hosting, high-energy social days |

Experience ACF fields (postmeta keys): tagline, best_for, whats_included, signature_styling_kit, signature_moment, pricing, experience_key, duration, elevated_add_ons.

Note the experience_key values (rose, sunset, pinkpalm, monaco) match the suffixes on the yacht pricing matrix fields. That is the join: a yacht page can show the price for each experience by reading pricing_price_4hr_rose, pricing_price_4hr_sunset, and so on.

### 2c. Elementor templates and dynamic tags
The kit contains 56 template JSON files. Of these, 8 use Elementor dynamic tags (`__dynamic__`), and 3 (templates 6000, 6007, 6733) embed ACF field keys such as field_69b75215971c3, field_69b75229971c4, field_69b7525e971c7. These are the Theme Builder single and loop templates that render the yacht and experience CPTs dynamically. The other template exports are static page layouts that show placeholder copy.

### 2d. Supporting structure in the kit
- taxonomies: category, post_tag, nav_menu (menus exported)
- wp-content/nav_menu_item: menu items
- wp-content/metform-form and content/metform-form: booking and contact forms (real form IDs)
- wp-content/elementskit_content, elementskit_template, elementskit_widget: ElementsKit parts
- ova_framework_hf_el: theme (Ova) header and footer builder elements
- site-settings.json, custom-code.json, manifest.json: global settings and tracking

## 3. Answers to the architecture questions

1. Why the live site shows real content while exports show demo: the live pages are Theme Builder templates with dynamic tags bound to ACF fields on the yacht and experience CPTs. Exports capture the layout and the binding, not the database values. The real values are in the CPT XML, which is data, not layout.
2. Does yacht data live in custom post types: yes. Post type yacht, 10 posts, with ACF postmeta.
3. Is content injected via ACF: yes. Specs, pricing, and experience copy are ACF fields, surfaced through dynamic tags. ACF field keys (field_69b75...) appear directly in the dynamic templates.
4. Are Elementor templates pulling dynamic content: yes. 8 templates use dynamic tags; the single yacht and single experience templates bind ACF field keys.
5. Exact data exports needed: see section 4. Most of it is already inside the kit (yacht.xml, experience.xml). The main missing piece is the ACF field group definition export.

## 4. Exact export and import plan

### What I already have from the kit
- Yacht CPT content and ACF values: wp-content/yacht/yacht.xml (complete)
- Experience CPT content and ACF values: wp-content/experience/experience.xml (complete)
- Menus, forms, theme header and footer, global settings, dynamic templates

### What I still need to fully audit and optimize

1. Yachts export (WordPress): you already provided it via the kit XML. If you want a cleaner working copy, use WordPress admin, Tools, Export, choose "Yacht" post type only, to produce a yacht only WXR. Not strictly required since the kit XML is complete.

2. Experiences export (WordPress): same. Tools, Export, "Experience" post type only. Already covered by the kit XML.

3. ACF field group export (the key missing piece): in WordPress admin, ACF, Field Groups, select the Yacht group and the Experience group, then Export, and choose "Export File" to download acf-export-YYYYMMDD.json. This gives field labels, types, choices, conditional logic, and the field group location rules (which post type each group is bound to). The XML only gives field keys and values; the field group export gives the schema and human readable labels. Provide both the Yacht and Experience field groups.

4. SEO and AI search inputs (for the audit portion): export your SEO plugin settings (Yoast or Rank Math) or provide the live URL list or XML sitemap (shesaidsail.com/sitemap_index.xml). Needed to audit titles, meta descriptions, schema, and AI crawlability.

5. Optional but useful: a screenshot or list of Theme Builder conditions (Elementor, Templates, Theme Builder) showing which template is assigned to single yacht and single experience and any archive or loop. This confirms the render path end to end.

## 5. Where pricing should live: ACF, Airtable, or both

Recommendation: both, with Airtable as the source of truth and ACF as the published cache. Reasoning grounded in the existing repo:

- The Airtable Final Build Spec already defines Yacht, Vessel, and Pricing tables. The operation already treats Airtable as the operational system of record.
- ACF is the presentation layer. The website must read pricing from ACF because the Theme Builder templates already bind to ACF fields (pricing_price_*, *_hour_charter_rate, starting_price).
- Editing pricing in two places by hand will drift. So: manage pricing in Airtable, then push to ACF automatically. ACF stays the field the site renders, Airtable stays where the team edits.

Single source of truth: Airtable Pricing table. Published copy: ACF fields on each yacht post. Never hand edit ACF pricing once the sync is live.

## 6. Airtable to Make to WordPress pricing sync (design)

Goal: when pricing changes in Airtable, the matching yacht post's ACF fields update automatically.

Prerequisites:
- Airtable Pricing or Yacht table with one row per yacht, columns for starting_price, 4_hour_charter_rate, 6_hour_charter_rate, 8_hour_charter_rate, and the per experience matrix pricing_price_{4,6,8}hr_{rose,sunset,pinkpalm,monaco}.
- A stable key linking Airtable rows to WordPress posts. Add a wp_post_id column in Airtable for each yacht (the yacht post ID, visible in the XML and in WP admin). This is more reliable than matching by name (note Gatsby vs Gratsky, Sugaree vs Sugarree, GTX80 vs CTX 80 mismatches between systems).
- WordPress REST API access with ACF to REST API enabled, or the WPGraphQL plus ACF, or the native ACF REST support in recent versions. Create an application password for a dedicated WordPress user with edit access to yachts.

Make scenario (new, to add alongside the existing STAGE_1_FINAL scenarios):
1. Trigger: Airtable, Watch Records, on the Pricing or Yacht table, triggering on update.
2. Optional guard: only proceed if a "publish to site" checkbox is true, so drafts do not push.
3. Action: HTTP or WordPress module, PATCH to /wp-json/wp/v2/yacht/{wp_post_id} with a JSON body setting the acf object, for example acf: { starting_price, 4_hour_charter_rate, pricing_price_4hr_rose, ... }. ACF to REST API maps these to the field keys.
4. Confirmation: write back a "last synced" timestamp to Airtable, and post a Slack message via the existing M-SLACK-ALERTS pattern.
5. Logging: append to the existing M-AUDIT-LOGGER pattern so pricing changes are auditable.

This reuses the operation's existing Make and Slack and audit conventions and adds one new scenario, M-YACHT-PRICING-SYNC, rather than introducing a new system.

Direction of sync: one way, Airtable to WordPress. Do not sync WordPress back to Airtable, to keep a single source of truth and avoid loops.

Caching note: if a performance or WebP plugin is active (the meta shows SiteGround Optimizer), clear or purge the page cache after a pricing push so the new price shows immediately. Make can call the cache purge endpoint as a final step if needed.

## 7. Naming reconciliation needed before sync

The CPT names, the pricing PDF, and the demo content disagree. Lock one canonical name per yacht before wiring the sync, and store it in both Airtable and the yacht post title:

| CPT title (live) | Pricing PDF name | Notes |
|---|---|---|
| Gatsby | Gratsky | confirm correct spelling |
| Sugaree | Sugarree | confirm correct spelling |
| GTX80 | CTX 80 | confirm correct name |
| IV Tranquility | Tranquility IV | confirm word order |
| Mirracle, Freedom, Vasiliki, Compass, Carpe Diem, Another One | same | aligned |

Experiences also differ: live CPT uses Rosé Day Club, Golden Hour Escape, Pink Palm Club, Monaco Social, while the pricing PDF used Rosé, Sunset Social, Pink Palm, Monaco Social. The experience_key values (rose, sunset, pinkpalm, monaco) are the stable join keys and should be used in the sync, not the display names.

## 8. What not to do

- Do not keep editing the Elementor page or template JSON to fix content. The visible yacht and experience content is dynamic, so layout edits will not change the data.
- Do not hand edit ACF pricing once the Airtable sync is live.
- Do not match Airtable to WordPress by yacht name. Use wp_post_id and experience_key.
