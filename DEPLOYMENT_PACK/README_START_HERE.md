# She Said Sail: Website Deployment Pack
**Version:** 2.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

Read this first. Everything else follows from here.

For the complete step-by-step installation guide, see: `FINAL_IMPLEMENTATION_GUIDE.md`

---

## WHAT THIS PACK IS

This deployment pack contains every file needed to build and deploy the complete She Said Sail website system. It covers the full site: 13 pages, custom luxury chatbot widget, full Airtable backend (7 core tables + 6 intelligence tables), Make.com automation (10 core scenarios + 4 intelligence scenarios), GTM event tracking (22 events), GA4, Meta Pixel, TikTok Pixel, and complete AI search and SEO optimization.

The pack is organized into numbered folders. Each folder has a specific job.
You do not need to understand the whole pack to use it. Follow the install guides in order.

---

## WHO THIS IS FOR

This pack is for the web builder (contractor or in-house) applying changes to WordPress.
It is also for the developer wiring Airtable and Make.com.
Will (founder) approves decisions and reviews screenshots before each page is published.

---

## FOLDER MAP

```
01_GLOBAL_CSS/         Global CSS file. Goes into WordPress Additional CSS.
02_GLOBAL_JS/          Global JS file. Goes into Insert Headers and Footers, footer.
03_HTML_SNIPPETS/      HTML sections added via Elementor HTML widgets (homepage, experiences, monaco-social, request-to-book).
04_SEO_META/           Meta tags and schema for homepage, experiences, request-to-book, and global.
05_AIRTABLE_BACKEND/   Table schemas and field maps for 7 core tables + 6 intelligence tables.
06_MAKE_WEBHOOKS/      Make.com scenario specs, webhook payloads, and intelligence scenarios.
07_GTM_ANALYTICS/      GTM event map (22 events: 14 site + 8 chatbot), GA4, Meta Pixel, TikTok Pixel.
08_PAGE_INSTALL_GUIDES/ Step-by-step per-page install guides. Web builder follows these.
09_QA/                 Pass/fail checklists. Complete after each section is applied.
10_FINAL_AUDIT/        Readiness audit. Review before merging to production.
11_HANDOFF_TO_WEB_BUILDER/ Contractor briefing document. Start here if you are the builder.
chatbot/               Custom luxury concierge chatbot: CSS, JS, conversation flow, analytics, QA.
pages/                 Per-page HTML snippets and metadata for all 10 additional pages:
  about/               About page.
  contact/             Contact page.
  faq/                 FAQ page.
  golden-hour-escape/  Golden Hour Escape experience page.
  pink-palm-club/      Pink Palm Club experience page.
  rose-day-club/       Rose Day Club experience page.
  journal/             Journal / blog page.
  thank-you/           Thank You page.
FINAL_IMPLEMENTATION_GUIDE.md   Complete step-by-step deployment guide for the entire system.
```

---

## INSTALL ORDER

Follow this exact sequence. Do not skip steps.

### Phase 1: Global Files (applies to all pages at once)

| Step | Action | File | Time |
|---|---|---|---|
| 1 | Apply CSS to WordPress | 01_GLOBAL_CSS/she-said-sail-global.css | 5 min |
| 2 | Add JS to Insert Headers and Footers | 02_GLOBAL_JS/she-said-sail-global.js | 5 min |
| 3 | Add global schema to all pages | 04_SEO_META/global-schema.html | 5 min |

### Phase 2: Homepage

| Step | Action | File | Time |
|---|---|---|---|
| 4 | Add homepage SEO meta | 04_SEO_META/homepage-meta.html | 5 min |
| 5 | Add social proof strip via Elementor HTML widget | 03_HTML_SNIPPETS/homepage/social-proof-strip.html | 15 min |
| 6 | Add occasion pills to hero via Elementor HTML widget | 03_HTML_SNIPPETS/homepage/hero-occasion-pills.html | 10 min |
| 7 | Add email capture section via Elementor HTML widget | 03_HTML_SNIPPETS/homepage/email-capture-section.html | 15 min |
| 8 | Make Elementor copy edits (section labels, card descriptions, CTA text) | See homepage-install-guide.md Step 7 | 20 min |

### Phase 3: Request to Book Page

| Step | Action | File | Time |
|---|---|---|---|
| 9 | Add concierge reassurance block via Elementor | 03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html | 10 min |
| 10 | Add form intro above the form | 03_HTML_SNIPPETS/request-to-book/request-form-intro.html | 5 min |
| 11 | Add trust note below form | 03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html | 5 min |
| 12 | Add SEO meta for this page | 04_SEO_META/request-to-book-meta.html | 5 min |
| 13 | Add hidden fields to the form | 05_AIRTABLE_BACKEND/request-form-hidden-fields.md | 15 min |

### Phase 4: Experiences Page

| Step | Action | File | Time |
|---|---|---|---|
| 14 | Add hero support copy | 03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html | 10 min |
| 15 | Add experiences social proof strip | 03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html | 15 min |
| 16 | Add bottom CTA | 03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html | 10 min |
| 17 | Apply experience card copy edits | 03_HTML_SNIPPETS/experiences/experience-card-content.html | 15 min |
| 18 | Add SEO meta | 04_SEO_META/experiences-meta.html | 5 min |

### Phase 5: Backend and Tracking (requires developer)

| Step | Action | Reference | Time |
|---|---|---|---|
| 19 | Build Airtable base and tables | 05_AIRTABLE_BACKEND/airtable-table-schema.md | 2 hours |
| 20 | Create Make.com scenarios | 06_MAKE_WEBHOOKS/make-webhook-setup.md | 3 hours |
| 21 | Wire form to Make.com webhook | 06_MAKE_WEBHOOKS/make-webhook-setup.md | 30 min |
| 22 | Set up GTM tags and publish | 07_GTM_ANALYTICS/gtm-events-map.md | 1 hour |
| 23 | Add Meta Pixel via GTM | 07_GTM_ANALYTICS/meta-pixel-events.md | 30 min |
| 24 | Add TikTok Pixel via GTM | 07_GTM_ANALYTICS/tiktok-pixel-events.md | 30 min |

---

## WHERE FILES GO

### Into WordPress Additional CSS

- `01_GLOBAL_CSS/she-said-sail-global.css`
- Path: WordPress Admin > Appearance > Customize > Additional CSS
- Copy the entire file. Paste. Click Publish.

### Into Insert Headers and Footers Plugin (Footer)

- `02_GLOBAL_JS/she-said-sail-global.js`
- Path: WordPress Admin > Settings > Insert Headers and Footers > Scripts in Footer
- Wrap in: `<script defer>` ... `</script>`

### Into Insert Headers and Footers Plugin (Header)

- `04_SEO_META/global-schema.html` (if not using GTM for schema)
- `04_SEO_META/homepage-meta.html` (or via Yoast SEO fields)
- `04_SEO_META/request-to-book-meta.html`
- `04_SEO_META/experiences-meta.html`

Preferred method: use Yoast SEO plugin fields for meta description, OG title, and OG description.
Use Insert Headers and Footers only for schema and tags Yoast does not support.

### Into Elementor (as HTML Widgets)

All files in `03_HTML_SNIPPETS/`:
1. Open the page in Elementor editor
2. Find the placement noted at the top of each snippet file
3. Add a new Container section (full width, no padding)
4. Inside the container, add an HTML widget
5. Paste the snippet content
6. Click Update

### Into GTM (as Custom HTML Tags)

- The JavaScript in `02_GLOBAL_JS/she-said-sail-global.js` handles dataLayer events
- You still need to create GTM tags that consume those events and fire to GA4, Meta Pixel, and TikTok Pixel
- See `07_GTM_ANALYTICS/gtm-events-map.md` for the full GTM setup

### Into Airtable

- Build the base manually using `05_AIRTABLE_BACKEND/airtable-table-schema.md`
- There is no Airtable CSV import. Each table and field must be created by hand.
- The schema document lists every field with its type and configuration.

### Into Make.com

- Build each scenario manually using `06_MAKE_WEBHOOKS/make-webhook-setup.md`
- After creating a scenario, copy its webhook URL
- Paste the webhook URL into the JavaScript file at the marked location (search for "WIRE THIS")

---

## HOW TO TEST EACH PAGE

### Homepage

1. View the homepage in a browser (desktop and mobile)
2. Confirm social proof strip appears between experience cards and "Not Just a Charter" section
3. Confirm occasion pills appear in the hero above the CTA button
4. Confirm email capture section appears above the bottom navy banner
5. Submit the email capture form and confirm the success message appears
6. Check the footer: phone number should be a tappable tel: link on mobile
7. See `09_QA/master-qa-checklist.md` for the full list

### Request to Book Page

1. Open /request-to-book/ in a browser
2. Confirm concierge reassurance block appears above the form
3. Fill in all required fields and submit
4. Confirm you reach /thank-you/ or see a confirmation message
5. Check Airtable: a new Request record should appear within 30 seconds
6. Check email: a confirmation email should arrive within 2 minutes
7. See `09_QA/form-qa-checklist.md` for the full list

### Experiences Page

1. Open /experiences/ in a browser
2. Confirm hero support copy appears below the page header
3. Confirm all 4 experience cards show updated descriptions
4. Confirm social proof strip appears below the cards
5. Confirm bottom CTA appears at page bottom, links to /request-to-book/
6. Click "Request to Book" on any card and confirm it reaches the correct page

---

## HOW TO ROLL BACK

Each change can be undone independently. No change is permanent.

| What to undo | How to undo | Time |
|---|---|---|
| CSS changes | Appearance > Customize > Additional CSS: delete the file content | 2 min |
| JS changes | Insert Headers and Footers: delete the script block | 2 min |
| Any HTML snippet | Elementor: right-click the HTML widget, click Delete, Update | 2 min |
| SEO meta (via Yoast) | Clear the Yoast fields you filled | 2 min |
| SEO meta (via plugin) | Insert Headers and Footers: delete the header block | 2 min |
| Make.com scenarios | Deactivate each scenario in Make.com dashboard | 1 min |
| Airtable records | Delete the test records manually in Airtable | 5 min |

Rolling back does not affect the git repository. CSS, JS, and HTML snippet changes live in WordPress, not in git.

---

## QUICK REFERENCE: CRITICAL RULES

- Never use em dashes in any copy, code, comments, or metadata
- Do not merge to staging or main without founder approval
- Do not change any brand colors, fonts, or the Elementor template structure
- Do not add new plugins without checking with Will
- Do not connect any third-party services not specified in this pack
- The yacht is not the product. The feeling is the product.

---

## FILES IN THIS PACK

### Global

- `README_START_HERE.md` -- this file

### CSS

- `01_GLOBAL_CSS/she-said-sail-global.css`

### JavaScript

- `02_GLOBAL_JS/she-said-sail-global.js`

### HTML Snippets: Homepage

- `03_HTML_SNIPPETS/homepage/social-proof-strip.html`
- `03_HTML_SNIPPETS/homepage/hero-occasion-pills.html`
- `03_HTML_SNIPPETS/homepage/email-capture-section.html`

### HTML Snippets: Request to Book

- `03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html`
- `03_HTML_SNIPPETS/request-to-book/request-form-intro.html`
- `03_HTML_SNIPPETS/request-to-book/thank-you-message.html`
- `03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html`

### HTML Snippets: Experiences

- `03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html`
- `03_HTML_SNIPPETS/experiences/experience-card-content.html`
- `03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html`
- `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html`

### SEO Meta

- `04_SEO_META/homepage-meta.html`
- `04_SEO_META/request-to-book-meta.html`
- `04_SEO_META/experiences-meta.html`
- `04_SEO_META/global-schema.html`

### Airtable Backend

- `05_AIRTABLE_BACKEND/airtable-field-map.md`
- `05_AIRTABLE_BACKEND/request-form-hidden-fields.md`
- `05_AIRTABLE_BACKEND/airtable-table-schema.md`
- `05_AIRTABLE_BACKEND/page-to-airtable-mapping.md`

### Make Webhooks

- `06_MAKE_WEBHOOKS/make-webhook-setup.md`
- `06_MAKE_WEBHOOKS/request-capture-payload.json`
- `06_MAKE_WEBHOOKS/email-capture-payload.json`
- `06_MAKE_WEBHOOKS/test-payloads.md`

### GTM Analytics

- `07_GTM_ANALYTICS/gtm-events-map.md`
- `07_GTM_ANALYTICS/ga4-events.md`
- `07_GTM_ANALYTICS/meta-pixel-events.md`
- `07_GTM_ANALYTICS/tiktok-pixel-events.md`
- `07_GTM_ANALYTICS/datalayer-test-guide.md`

### Page Install Guides

- `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md`
- `08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md`
- `08_PAGE_INSTALL_GUIDES/experiences-install-guide.md`

### QA Checklists

- `09_QA/master-qa-checklist.md`
- `09_QA/mobile-qa-checklist.md`
- `09_QA/form-qa-checklist.md`
- `09_QA/backend-qa-checklist.md`
- `09_QA/tracking-qa-checklist.md`

### Final Audit

- `10_FINAL_AUDIT/final-site-readiness-audit.md`
- `10_FINAL_AUDIT/page-scorecard.md`
- `10_FINAL_AUDIT/launch-go-no-go.md`

### Handoff

- `11_HANDOFF_TO_WEB_BUILDER/WEB_BUILDER_HANDOFF.md`
