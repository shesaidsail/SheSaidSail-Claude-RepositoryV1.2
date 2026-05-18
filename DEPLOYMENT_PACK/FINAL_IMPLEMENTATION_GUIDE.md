# She Said Sail: Final Implementation Guide

**Version:** 1.0
**Date:** May 2026
**System:** WordPress 6.9.4 + Elementor 4.0.3 + Hello Elementor theme
**Brand:** She Said Sail, luxury yacht charter, Miami
**GTM Container:** GTM-TZ5KNRTH
**GA4 Measurement ID:** GT-WV3X86GZ

---

## Table of Contents

1. Overview
2. Pre-Deployment Prerequisites
3. Installation Order
4. Step 1: Global CSS
5. Step 2: Global JavaScript
6. Step 3: GTM Container Setup
7. Step 4: HTML Snippets
8. Step 5: SEO Metadata and Schema
9. Step 6: Forms and Hidden Fields
10. Step 7: Chatbot Installation
11. Step 8: Airtable Setup
12. Step 9: Make.com Scenarios
13. Step 10: Analytics and Pixels
14. Step 11: Intelligence Layer
15. QA Flow
16. Rollback Procedure
17. Staging vs Production Workflow
18. Known Limitations and Manual Steps
19. Post-Launch Checklist

---

## 1. Overview

This DEPLOYMENT_PACK contains every asset, schema, and instruction needed to deploy the full She Said Sail website system. It covers front-end styling, JavaScript behavior, HTML content sections, SEO metadata, form tracking, chatbot, Airtable backend, Make.com automation, and GTM/analytics.

The pack is a complete snapshot. Nothing is left for interpretation. Every file has a specific destination. Every action in every step references the exact file to open.

### What is in this pack

```
01_GLOBAL_CSS/         One global CSS file, 1523 lines. Covers all pages.
02_GLOBAL_JS/          One global JS file. UTM capture, hidden fields, GTM events, scroll tracking.
03_HTML_SNIPPETS/      Ready-to-paste HTML sections added via Elementor HTML widgets.
  homepage/            Three homepage sections.
  request-to-book/     Four request page sections.
  experiences/         Four experiences page sections.
  monaco-social/       Six Monaco Social experience page sections.
04_SEO_META/           Meta tags and JSON-LD schema for each page.
05_AIRTABLE_BACKEND/   Table schemas, field maps, hidden field specs.
06_MAKE_WEBHOOKS/      Scenario build guides, test payloads, intelligence scenario specs.
07_GTM_ANALYTICS/      GTM events map, GA4 config, Meta Pixel, TikTok Pixel.
08_PAGE_INSTALL_GUIDES/ Step-by-step per-page install guides.
09_QA/                 Pass/fail checklists for each functional area.
10_FINAL_AUDIT/        Site readiness scorecards.
11_HANDOFF_TO_WEB_BUILDER/ Contractor briefing document.
chatbot/               Chatbot CSS, JS, conversation flow, backend mapping, analytics events.
pages/                 Per-page assets for about, contact, faq, golden-hour-escape,
                       journal, pink-palm-club, rose-day-club, and thank-you.
```

### How to use this guide

Read Section 2 (prerequisites) and Section 3 (installation order) before touching anything. Then follow each numbered Step section in order. Each step tells you which file to open, exactly where the content goes, and what to verify when done.

Do not skip steps. Most dependencies flow downward: CSS before JS, JS before forms, Airtable before Make, Make before GTM. Out-of-order installation wastes time.

---

## 2. Pre-Deployment Prerequisites

Confirm every item in this list before starting. If any item is false, resolve it first.

### WordPress and Hosting

- [ ] WordPress version 6.9.4 is installed and accessible at the production domain.
- [ ] Admin credentials are available (user with `administrator` role).
- [ ] SSH or SFTP access is available for any file operations that bypass WP admin.
- [ ] The domain has an active SSL certificate (HTTPS only, no HTTP fallback).
- [ ] A staging environment is available and is a copy of production (see Section 17).

### Plugins (must all be installed and active before starting)

- [ ] **Elementor Pro** (version 4.0.3 or compatible). Verify at Plugins > Installed Plugins.
- [ ] **Hello Elementor** theme is active. Verify at Appearance > Themes.
- [ ] **Insert Headers and Footers** (by WPBeginner). This plugin is required to inject the global JS and GTM snippets. If not installed: Plugins > Add New > search "Insert Headers and Footers" > Install > Activate.
- [ ] **Yoast SEO** (or RankMath). Required for per-page meta description, OG title, OG image. Confirm which is installed and stay consistent.
- [ ] **MetForm** (or Elementor Pro Forms). Required for the Request to Book form with hidden fields.
- [ ] **Tidio** is DISABLED and deactivated before chatbot installation. Tidio must not be running on the same site as the custom chatbot. Confirm at Plugins > Installed Plugins: Tidio shows Inactive or is deleted.

### Third-party accounts

- [ ] Google Tag Manager: access to the GTM-TZ5KNRTH container. You need Publish permission, not just Read.
- [ ] Google Analytics 4: admin access to the property using measurement ID GT-WV3X86GZ.
- [ ] Meta Ads Manager: access to the Business account and pixel. You will need the Pixel ID.
- [ ] TikTok Ads Manager: access to the business account and pixel. You will need the Pixel ID.
- [ ] Airtable: admin access to the workspace where the base will live.
- [ ] Make.com: admin access to the workspace. At least one Airtable connection and one Slack connection must be authorized before building scenarios.
- [ ] Slack: a workspace with at least two channels ready: `#new-leads` (for lead alerts) and `#intelligence` (for weekly reports and booking outcomes).

### Brand and content assets

- [ ] Hero images are available in the media library with dimensions of at least 1920x1080. These must use `fetchpriority="high"` and `loading="eager"` in the HTML. Never use `loading="lazy"` on hero images.
- [ ] The She Said Sail logo is uploaded to the media library. It will need an alt text fix applied by the global JS.
- [ ] The four experience photography assets are uploaded and assigned to the correct Elementor loop items.

### Credentials to collect before starting

Gather all of these before you touch a single file. You will need them mid-installation and cannot pause to hunt for them without risking configuration errors.

| Credential | Where to find it | Used in |
|---|---|---|
| GTM Container ID: GTM-TZ5KNRTH | GTM dashboard > Admin > Container Settings | WordPress head, Step 3 |
| GA4 Measurement ID: GT-WV3X86GZ | GA4 Admin > Data Streams | GTM GA4 Config tag, Step 10 |
| Meta Pixel ID | Meta Events Manager | GTM Meta Pixel tag, Step 10 |
| TikTok Pixel ID | TikTok Ads Manager > Assets > Events | GTM TikTok tag, Step 10 |
| Airtable Personal Access Token | airtable.com > Account > Developer Hub > Create Token | Make.com Airtable connection, Step 8 |
| Airtable Base ID | Browser URL after opening the base: airtable.com/[BASE_ID]/... | Make.com modules, Step 9 |
| Make.com chatbot webhook URL | Created in Step 9, wired into chatbot-js.js in Step 7 | chatbot-js.js |
| Make.com request form webhook URL | Created in Step 9, wired into global JS in Step 9 | she-said-sail-global.js |
| Make.com email capture webhook URL | Created in Step 9, wired into global JS in Step 9 | she-said-sail-global.js |
| Make.com contact form webhook URL | Created in Step 9, wired into contact-html-snippets.html | pages/contact/contact-html-snippets.html |

---

## 3. Installation Order

Follow this sequence exactly. Each phase depends on the previous.

### Phase 1: Global files (affects all pages at once)

| Step | Action | File | Estimated time |
|---|---|---|---|
| 1 | Apply Global CSS | `01_GLOBAL_CSS/she-said-sail-global.css` | 5 min |
| 2 | Add Global JS to footer | `02_GLOBAL_JS/she-said-sail-global.js` | 10 min |
| 3 | Install GTM snippet | GTM-TZ5KNRTH container code | 10 min |

### Phase 2: Homepage

| Step | Action | File | Estimated time |
|---|---|---|---|
| 4 | Add social proof strip | `03_HTML_SNIPPETS/homepage/social-proof-strip.html` | 10 min |
| 5 | Add occasion pills | `03_HTML_SNIPPETS/homepage/hero-occasion-pills.html` | 10 min |
| 6 | Add email capture section | `03_HTML_SNIPPETS/homepage/email-capture-section.html` | 15 min |
| 7 | Add homepage SEO meta | `04_SEO_META/homepage-meta.html` | 5 min |

### Phase 3: Request to Book page

| Step | Action | File | Estimated time |
|---|---|---|---|
| 8 | Add concierge reassurance block | `03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html` | 10 min |
| 9 | Add request form intro | `03_HTML_SNIPPETS/request-to-book/request-form-intro.html` | 5 min |
| 10 | Add trust note under form | `03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html` | 5 min |
| 11 | Add thank-you message | `03_HTML_SNIPPETS/request-to-book/thank-you-message.html` | 5 min |
| 12 | Add hidden fields to form | `05_AIRTABLE_BACKEND/request-form-hidden-fields.md` | 20 min |
| 13 | Add request to book SEO meta | `04_SEO_META/request-to-book-meta.html` | 5 min |

### Phase 4: Experiences page

| Step | Action | File | Estimated time |
|---|---|---|---|
| 14 | Add hero support copy | `03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html` | 10 min |
| 15 | Add social proof strip | `03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html` | 10 min |
| 16 | Add bottom CTA | `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html` | 10 min |
| 17 | Add experience card content | `03_HTML_SNIPPETS/experiences/experience-card-content.html` | 15 min |
| 18 | Add experiences SEO meta | `04_SEO_META/experiences-meta.html` | 5 min |

### Phase 5: Experience detail pages

| Step | Action | File | Estimated time |
|---|---|---|---|
| 19 | Monaco Social: six sections | `03_HTML_SNIPPETS/monaco-social/` (six files) | 30 min |
| 20 | Monaco Social SEO meta | `04_SEO_META/monaco-social-meta.html` | 5 min |
| 21 | Golden Hour Escape: snippets + meta | `pages/golden-hour-escape/` | 30 min |
| 22 | Rose Day Club: snippets + meta | `pages/rose-day-club/` | 30 min |
| 23 | Pink Palm Club: snippets + meta | `pages/pink-palm-club/` | 30 min |

### Phase 6: Secondary pages

| Step | Action | File | Estimated time |
|---|---|---|---|
| 24 | About page: snippets + meta | `pages/about/` | 20 min |
| 25 | Contact page: snippets + meta | `pages/contact/` | 20 min |
| 26 | FAQ page: snippets + meta | `pages/faq/` | 20 min |
| 27 | Journal page: snippets + meta | `pages/journal/` | 15 min |
| 28 | Thank You page: snippets + meta | `pages/thank-you/` | 15 min |

### Phase 7: Chatbot

| Step | Action | File | Estimated time |
|---|---|---|---|
| 29 | Add chatbot CSS to head | `chatbot/chatbot-css.css` | 5 min |
| 30 | Wire chatbot webhook URL | `chatbot/chatbot-js.js` | 5 min |
| 31 | Add chatbot JS to footer (after global JS) | `chatbot/chatbot-js.js` | 10 min |

### Phase 8: Backend (requires developer, can run in parallel with Phases 5-7)

| Step | Action | Reference | Estimated time |
|---|---|---|---|
| 32 | Build Airtable base (7 original tables) | `05_AIRTABLE_BACKEND/airtable-table-schema.md` | 2 hours |
| 33 | Build Make.com scenarios (10 original) | `06_MAKE_WEBHOOKS/make-webhook-setup.md` | 3 hours |
| 34 | Wire webhook URLs into JS and HTML | See Steps 2, 7, and contact page | 30 min |
| 35 | Build GTM variables, triggers, tags | `07_GTM_ANALYTICS/gtm-events-map.md` | 1.5 hours |
| 36 | Add Meta Pixel via GTM | `07_GTM_ANALYTICS/meta-pixel-events.md` | 30 min |
| 37 | Add TikTok Pixel via GTM | `07_GTM_ANALYTICS/tiktok-pixel-events.md` | 30 min |

### Phase 9: Intelligence layer (build only after all Phase 8 steps are stable)

| Step | Action | Reference | Estimated time |
|---|---|---|---|
| 38 | Modify existing Airtable tables | `05_AIRTABLE_BACKEND/intelligence-tables.md` | 30 min |
| 39 | Add 6 intelligence Airtable tables | `05_AIRTABLE_BACKEND/intelligence-tables.md` | 2 hours |
| 40 | Build 4 intelligence Make.com scenarios | `06_MAKE_WEBHOOKS/intelligence-scenarios.md` | 2 hours |

---

## 4. Step 1: Global CSS

**File:** `01_GLOBAL_CSS/she-said-sail-global.css`
**Destination:** WordPress Admin > Appearance > Customize > Additional CSS
**Time required:** 5 minutes

### What this file does

This 1523-line stylesheet defines all brand tokens, typography, component styles, responsive rules, and animation behavior. It applies to every page on the site. It uses CSS custom properties (variables) so every color, font, and transition can be adjusted from one place.

The CSS is structured in 19 sections:

1. Design Tokens (CSS variables)
2. Global Refinements
3. Navigation Polish
4. Hero Section
5. Section Label System
6. Experience Cards
7. Social Proof Strip
8. Not Just a Charter Section
9. Bottom CTA Banner
10. Email Capture Section
11. Footer Redesign
12. Scroll Reveal System
13. Occasion Pills
14. Global Component Refinements
15. Trust Strip
16. Request to Book Page
17. Experiences Page
18. Mobile and Tablet Responsive
19. Print Styles

### Brand tokens reference

These CSS variables are defined at `:root` level. Do not change them without founder approval.

```css
--sss-navy:      #1A2332
--sss-gold:      #DAB97E
--sss-gold-deep: #C9A96E
--sss-cream:     #FAF8F3
--sss-warm:      #F5F0E8
--sss-text:      #2C2C2C
--sss-muted:     rgba(44,44,44,0.5)
--sss-border:    rgba(218,185,126,0.22)
```

**Accessibility note:** Gold (`#DAB97E`) fails WCAG AA contrast requirements on white backgrounds for body text. Use gold only for large display headings (18pt or larger, bold). Never use gold for paragraph text or links on a light background. Muted text (`rgba(44,44,44,0.5)`) also fails contrast: use it only for decorative labels, not for any text that conveys meaning.

### Step-by-step installation

1. Log in to WordPress admin at `/wp-admin/`.
2. In the left sidebar, go to Appearance > Customize.
3. The WordPress Customizer opens. In the left panel, click "Additional CSS" (at the bottom of the list).
4. A text area appears. Open `01_GLOBAL_CSS/she-said-sail-global.css` in a text editor. Select all (Ctrl+A / Cmd+A). Copy (Ctrl+C / Cmd+C).
5. Click inside the Additional CSS text area in the Customizer. Paste (Ctrl+V / Cmd+V).
6. Click the blue "Publish" button at the top of the Customizer panel.
7. Close the Customizer tab.

### Post-install verification

- Open the homepage in a new browser tab. The page should show deep navy backgrounds, cream section backgrounds, and Cormorant Garamond headings.
- Open DevTools (F12) > Console. Zero CSS errors should appear.
- Open DevTools > Elements > select any `.sss-reveal` element. Its computed styles should show `opacity: 0` and `transform: translateY(24px)` before scroll.
- Resize to 375px width. No horizontal overflow should appear on any page section.

---

## 5. Step 2: Global JavaScript

**File:** `02_GLOBAL_JS/she-said-sail-global.js`
**Destination:** WordPress Admin > Settings > Insert Headers and Footers > Scripts in Footer
**Time required:** 10 minutes

### Critical placement rules

The global JS must go in the **footer**, not the header. The plugin has three text areas: Scripts in Header, Scripts in Body, and Scripts in Footer. Use Scripts in Footer only.

The script tag must use the `defer` attribute:

```html
<script defer>
/* PASTE she-said-sail-global.js CONTENTS HERE */
</script>
```

If you are loading the file as an external URL (hosted on the server or CDN), use:

```html
<script src="https://shesaidsail.com/wp-content/uploads/she-said-sail-global.js" defer></script>
```

Do not use `async`. The `async` attribute can cause the script to run before the DOM is ready, breaking hidden field population. Use `defer` only.

### dataLayer initialization requirement

The `window.dataLayer` array must be initialized BEFORE the GTM snippet. The GTM snippet itself initializes dataLayer internally, but initializing it manually before GTM ensures that any events pushed before GTM fires are not lost.

In the WordPress head (via Insert Headers and Footers > Scripts in Header, or via a custom hook in the theme), add:

```html
<script>
  window.dataLayer = window.dataLayer || [];
</script>
```

This line must appear BEFORE the GTM `<script>` tag in the `<head>`. The installation order is:

1. `window.dataLayer = window.dataLayer || [];` (in head)
2. GTM `<script>` tag (in head)
3. GTM `<noscript>` tag (immediately after `<body>` opening tag)
4. `she-said-sail-global.js` (in footer, with `defer`)
5. `chatbot-js.js` (in footer, AFTER global JS, with `defer`)

### What the global JS does (section by section)

| Section | What it does |
|---|---|
| Section 0: Visitor ID | Generates and persists a UUID cookie (`sss_vid`) for first-party visitor identification. Sets `window.__sssVid`. Runs before all other code. |
| Section 1: UTM Capture | Reads UTM parameters from the URL. Writes them to `sessionStorage` under key `sss_utm`. First-touch attribution only: will not overwrite values already stored. Records `sss_first_seen` to localStorage on first visit. |
| Section 2: Hidden Field Population | On DOM ready, reads UTM data from `sessionStorage` and injects values into hidden form inputs by matching the `name` attribute. Populates: utm_source, utm_medium, utm_campaign, utm_content, utm_term, creative_id, landing_page, source_url, referrer_url, first_seen_at, submission_page, brand, service_category, visitor_id, source_type. |
| Section 3: Trust Fixes | Corrects missing alt text on logo images. Fixes phone links to use `tel:` href. Converts location text to Google Maps links. Fills empty alt text on hero and card images. |
| Section 4: Scroll Reveal | Uses IntersectionObserver to animate elements with the `.sss-reveal` class into view. Falls back gracefully in browsers without IntersectionObserver. |
| Section 5: Header Scroll State | Adds the `.sss-header-scrolled` class to the header element when the user scrolls past 80px. |
| Section 6: Email Capture | Handles submission of `.sss-email-form`. Fires `submit_email_capture` GTM event. Contains a `fetch()` call to the Make.com email capture webhook URL. This call is commented out in the current file and must be wired with a real URL before launch. |
| Section 7: Smooth Scroll | Intercepts anchor links and scrolls to targets with an 80px offset to account for the fixed header. |
| Section 8: Mobile Nav Close | Closes the Elementor burger menu when a nav link is tapped on mobile. |
| Section 9: Occasion Badges | Injects occasion badge text into experience card elements with matching data attributes. |
| Section 10: GTM DataLayer Events | All 18 analytics push calls: page views, CTA clicks, form events, engagement events, scroll depth events. |

### Webhook wiring (required before launch)

The global JS has two locations that need real webhook URLs before the form and email capture go live.

**Email capture webhook** (Section 6 in the file):
Search for `WIRE_THIS_EMAIL_CAPTURE_WEBHOOK_URL` or the commented-out `fetch()` block. Replace the placeholder with the Make.com webhook URL from scenario M-EMAIL-CAPTURE. Uncomment the fetch block.

**Request form webhook** (booking form submit handler, Section 10 area):
Search for `WIRE_THIS_REQUEST_FORM_WEBHOOK_URL`. Replace with the webhook URL from scenario M-WEBFORM-REQUEST-CAPTURE.

Both URLs will look like: `https://hook.eu2.make.com/XXXXXXXXXXXXXX` (region may differ).

### Step-by-step installation

1. Open `02_GLOBAL_JS/she-said-sail-global.js` in a text editor.
2. Select all. Copy.
3. In WordPress admin, go to Settings > Insert Headers and Footers.
4. Find the "Scripts in Footer" text area (the third box).
5. Paste this into the Scripts in Footer text area:

```html
<script defer>
</script>
```

6. Place your cursor between the opening and closing script tags. Paste the copied JS content there.
7. Click Save.

### Post-install verification

Open the homepage in a browser. Open DevTools > Console.

- Type `window.__sssVid` and press Enter. It should return a UUID string (e.g., `"a1b2c3d4-..."`).
- Type `typeof populateHiddenFields` and press Enter. It should return `"function"`.
- Type `window.dataLayer` and press Enter. It should return an array (possibly empty).
- No JavaScript errors should appear in the console on page load.
- Add `?utm_source=test&utm_campaign=deploy` to the homepage URL and reload. Then type `JSON.parse(sessionStorage.getItem('sss_utm'))` in the console. It should return `{utm_source: "test", utm_campaign: "deploy"}`.

---

## 6. Step 3: GTM Container Setup

**GTM Container ID:** GTM-TZ5KNRTH
**Time required:** 10 minutes for snippet install; 1.5 hours for full tag configuration

### Part A: Install the GTM snippet in WordPress

The GTM snippet has two parts.

**Part 1: Head snippet.** Goes in the `<head>` of every page.

Open Insert Headers and Footers > Scripts in Header. Paste the entire block below as one unit -- the dataLayer line must come first:

```html
<script>window.dataLayer = window.dataLayer || [];</script>

<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TZ5KNRTH');</script>
<!-- End Google Tag Manager -->
```

**Part 2: Body noscript fallback.** Goes immediately after the `<body>` opening tag.

In Insert Headers and Footers > Scripts in Body (the second text area), paste:

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TZ5KNRTH"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Click Save.

### Part B: Verify GTM is firing

1. Install the "Tag Assistant Companion" Chrome extension from Google, or use GTM Preview mode.
2. In GTM, click Preview. Enter the site URL. Click Connect.
3. The Tag Assistant panel should appear at the bottom of the browser window showing the GTM container is connected.
4. Navigate to the homepage. The panel should show "Tags Fired on This Page" with at least the GTM initialization.

If the Tag Assistant shows "GTM container not found," verify the head snippet is saved in Insert Headers and Footers and that no caching plugin is serving a stale head.

### Part C: Configure GTM variables

Before creating any tags, create all Data Layer Variables. In GTM > Variables > User-Defined Variables > New:

| Variable Name | Variable Type | Data Layer Key |
|---|---|---|
| DLV - event | Data Layer Variable | `event` |
| DLV - page_location | Data Layer Variable | `page_location` |
| DLV - cta_location | Data Layer Variable | `cta_location` |
| DLV - occasion | Data Layer Variable | `occasion` |
| DLV - group_size | Data Layer Variable | `group_size` |
| DLV - experience_name | Data Layer Variable | `experience_name` |
| DLV - experience_slug | Data Layer Variable | `experience_slug` |
| DLV - card_position | Data Layer Variable | `card_position` |
| DLV - form_name | Data Layer Variable | `form_name` |
| DLV - form_location | Data Layer Variable | `form_location` |

Also create one Custom JavaScript variable:

| Variable Name | Variable Type | Code |
|---|---|---|
| CJS - Page Location | Custom JavaScript | `function(){ return window.location.href; }` |

### Part D: Configure GTM triggers

Create all Custom Event triggers. In GTM > Triggers > New > Custom Event:

**Site triggers:** view_homepage, view_request_page, view_experiences_page, view_experience_page, view_about_page, view_contact_page, view_faq_page, view_journal_page, view_thank_you_page, click_request_to_book, click_explore_experiences, click_experience_card, start_booking_form, submit_booking_form, submit_email_capture, click_phone, scroll_50_percent, scroll_90_percent

**Chatbot triggers:** chatbot_open, chatbot_start_conversation, chatbot_select_occasion, chatbot_select_experience, chatbot_capture_email, chatbot_capture_phone, chatbot_handoff, chatbot_complete

Also create one "All Pages" trigger (Page View type, fires on all pages).

For each trigger, set the Event Name field to exactly the event name listed above. Trigger firing: "All Custom Events" with the matching event name condition.

**Special note on chatbot_capture_phone:** This trigger and its corresponding GA4 tag are not yet in the GTM container from initial setup. You must create this trigger and tag manually. See Step 10 for the full tag list.

### Part E: Publish the container

After all variables, triggers, and tags are created and verified in Preview mode, click Submit in GTM. Add a version name (e.g., "v1 - Initial deployment"). Click Publish.

GTM changes are not live until Published. Never leave the container in a saved-but-unpublished state before launch.

---

## 7. Step 4: HTML Snippets

All HTML snippets are added via Elementor's HTML widget. The process is the same for every snippet:

1. Open the page in the Elementor editor (Pages > find the page > Edit with Elementor).
2. Locate the placement position described below.
3. Hover between existing sections. A blue bar with a "+" icon appears.
4. Click "+" > search "HTML" > drag the HTML widget into position.
5. Paste the snippet content into the HTML Code field.
6. Click Update.

### Homepage snippets

**File:** `03_HTML_SNIPPETS/homepage/social-proof-strip.html`
**Placement:** Between the experience cards section and the "Not Just a Charter" section.
**What it adds:** A horizontal strip showing social proof indicators (review count, press mentions, or trust signals).

**File:** `03_HTML_SNIPPETS/homepage/hero-occasion-pills.html`
**Placement:** Inside the hero section, above the primary CTA button. This requires editing inside an existing Elementor column, not between full-width sections.
**What it adds:** Clickable occasion pills (Bachelorette, Birthday, Girls Trip, etc.) that link to filtered experience views.

**File:** `03_HTML_SNIPPETS/homepage/email-capture-section.html`
**Placement:** Above the bottom navy CTA banner section, as a full-width section.
**What it adds:** Email capture form with an inline input and submit button. This form's submission is handled by the global JS email capture handler in Section 6.

### Request to Book page snippets

**File:** `03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html`
**Placement:** Above the MetForm widget, as a full section. Not inside the form.
**What it adds:** A short introduction to the concierge process, setting expectations for the response timeline and what happens after submission.

**File:** `03_HTML_SNIPPETS/request-to-book/request-form-intro.html`
**Placement:** Between the concierge reassurance block and the first form field. If you cannot place it between the block and the form, place it as the first HTML widget inside the same Elementor column as the form.
**What it adds:** A heading and one sentence of context directly above the form fields.

**File:** `03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html`
**Placement:** Below the form submit button, outside the MetForm widget.
**What it adds:** A single reassurance line (example: "No payment required. We will be in touch within 24 hours.").

**File:** `03_HTML_SNIPPETS/request-to-book/thank-you-message.html`
**Placement:** This file is used on the `/thank-you/` page, not inline. Place it as the primary content section on the Thank You page, or reference `pages/thank-you/thank-you-html-snippets.html` for the full thank-you page build.

### Experiences page snippets

**File:** `03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html`
**Placement:** Below the page heading section and above the experience card grid.
**What it adds:** One to two sentences of supporting copy framing the experience selection.

**File:** `03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html`
**Placement:** Below the experience card grid.
**What it adds:** Social proof strip identical in function to the homepage strip but positioned after the cards.

**File:** `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html`
**Placement:** At the bottom of the page, after the social proof strip.
**What it adds:** A CTA section linking to `/request-to-book/`.

**File:** `03_HTML_SNIPPETS/experiences/experience-card-content.html`
**Placement:** This file contains updated copy for the four experience cards. Apply the copy from this file to the Elementor loop template for experience cards, not as an HTML widget. Edit the card copy fields directly in the Elementor loop item editor.

### Monaco Social page snippets (six files)

Open each file in `03_HTML_SNIPPETS/monaco-social/` and place them in the Elementor editor in the order listed:

1. `hero-support.html`: Below the hero heading.
2. `experience-description.html`: In the main description section.
3. `occasion-fit.html`: In the occasion fit section.
4. `social-proof.html`: After the occasion fit section.
5. `pre-cta-reassurance.html`: Immediately above the final CTA button.
6. `bottom-cta.html`: At the page bottom.

### Other experience pages (Golden Hour Escape, Rose Day Club, Pink Palm Club)

Each experience page has its HTML snippets in `pages/[experience-slug]/[experience-slug]-html-snippets.html`. Open that file. It contains labeled sections with placement instructions at the top of each section as HTML comments.

### Secondary page snippets

Each page in the `pages/` directory has a `-html-snippets.html` file. Placements follow the same Elementor HTML widget method. Open each file and read the HTML comment at the top of each section block for placement context.

| Page | File |
|---|---|
| About | `pages/about/about-html-snippets.html` |
| Contact | `pages/contact/contact-html-snippets.html` |
| FAQ | `pages/faq/faq-html-snippets.html` |
| Journal | `pages/journal/journal-html-snippets.html` |
| Thank You | `pages/thank-you/thank-you-html-snippets.html` |

---

## 8. Step 5: SEO Metadata and Schema

### Preferred method: Yoast SEO plugin fields

For standard per-page SEO fields (meta description, OG title, OG description, OG image), use Yoast SEO (or RankMath) fields on each page. These fields appear below the page editor in WordPress or in the Elementor page settings sidebar.

Fields to populate for every page:

| Field | Source |
|---|---|
| SEO Title | From the `-metadata.html` file for that page |
| Meta Description | From the `-metadata.html` file for that page |
| OG Title | From the `-metadata.html` file for that page |
| OG Description | From the `-metadata.html` file for that page |
| OG Image | Upload the designated hero image to the media library, then assign it here |
| Canonical URL | Set to the clean page URL (no trailing query strings) |

### Where to find per-page metadata

| Page | Metadata file |
|---|---|
| Homepage | `04_SEO_META/homepage-meta.html` |
| Experiences | `04_SEO_META/experiences-meta.html` |
| Monaco Social | `04_SEO_META/monaco-social-meta.html` |
| Request to Book | `04_SEO_META/request-to-book-meta.html` |
| Golden Hour Escape | `pages/golden-hour-escape/golden-hour-escape-metadata.html` |
| Rose Day Club | `pages/rose-day-club/rose-day-club-metadata.html` |
| Pink Palm Club | `pages/pink-palm-club/pink-palm-club-metadata.html` |
| About | `pages/about/about-metadata.html` |
| Contact | `pages/contact/contact-metadata.html` |
| FAQ | `pages/faq/faq-metadata.html` |
| Journal | `pages/journal/journal-metadata.html` |
| Thank You | `pages/thank-you/thank-you-metadata.html` |

### Global schema (JSON-LD): Insert Headers and Footers method

The global schema in `04_SEO_META/global-schema.html` contains a JSON-LD `LocalBusiness` structured data block. It should appear on every page. Because Yoast SEO does not typically handle global custom JSON-LD, inject it via Insert Headers and Footers:

1. Go to Settings > Insert Headers and Footers > Scripts in Header.
2. Paste the full contents of `04_SEO_META/global-schema.html` here.
3. Click Save.

This adds the schema to every page's `<head>`.

### Per-page JSON-LD schema (via Elementor Custom Code)

For pages that have page-specific JSON-LD schema (event schema, FAQ schema, service schema), use Elementor's Custom Code feature:

1. In Elementor, go to the page editor.
2. Click the hamburger menu (top-left) > Site Settings > Custom Code.
3. Add a new code block, location: `<head>`, and paste the JSON-LD block from the page's metadata file.
4. Assign the code block to this page only using Elementor's display conditions.

Alternatively, inject via a plugin like "Header Footer Code Manager" if your Yoast version does not support per-page custom code.

---

## 9. Step 6: Forms and Hidden Fields

### Overview

The Request to Book form uses MetForm (or Elementor Pro Forms). It has two categories of fields: visible user-facing fields and hidden tracking fields. The hidden fields are populated automatically by `she-said-sail-global.js` (Section 2: Hidden Field Population) on DOM ready. The fields must exist in the form's HTML before the JS runs.

### Visible fields (user fills in)

| Field Label | Field Type | Required |
|---|---|---|
| Full Name | Text | Yes |
| Email Address | Email | Yes |
| Phone Number | Tel | Yes |
| Occasion | Select | Yes |
| Group Size | Number | Yes |
| Preferred Date | Date | Yes |
| Flexible Dates | Checkbox | No |
| Experience Interest | Multi-select | No |
| Message / Notes | Textarea | No |

### Hidden fields (JS populates automatically)

Add each of these as a Hidden type field in MetForm. The `name` attribute must match exactly:

| HTML `name` attribute | Populated by | Notes |
|---|---|---|
| `utm_source` | `sessionStorage.sss_utm.utm_source` | First-touch UTM |
| `utm_medium` | `sessionStorage.sss_utm.utm_medium` | First-touch UTM |
| `utm_campaign` | `sessionStorage.sss_utm.utm_campaign` | First-touch UTM |
| `utm_content` | `sessionStorage.sss_utm.utm_content` | Creative variant |
| `utm_term` | `sessionStorage.sss_utm.utm_term` | Paid search keyword |
| `creative_id` | `sessionStorage.sss_utm.creative_id` | Ad creative identifier |
| `landing_page` | `window.location.href` at form load | Full URL |
| `source_url` | `window.location.href` | Same as landing_page |
| `referrer_url` | `document.referrer` | Previous page URL |
| `first_seen_at` | `localStorage.sss_first_seen` | ISO timestamp |
| `submission_page` | `window.location.href` | Full URL at submit time |
| `brand` | Hard-coded: `shesaidsail` | Constant |
| `service_category` | Hard-coded: `yacht-charter` | Constant |
| `visitor_id` | `window.__sssVid` | UUID from sss_vid cookie |
| `source_type` | Hard-coded: `form_lead` | Distinguishes from chatbot leads |

### How to add hidden fields in MetForm

1. Open the Request to Book page in the Elementor editor.
2. Click the MetForm widget to select it, then click the pencil (edit) icon.
3. In the MetForm field list, click "+ Add Field."
4. Select "Hidden" as the field type.
5. In the "Field ID / Name" field, enter the exact `name` value from the table above (e.g., `utm_source`).
6. Leave the default value blank for UTM fields. For `brand`, set default value to `shesaidsail`. For `service_category`, set default value to `yacht-charter`. For `source_type`, set default value to `form_lead`.
7. Repeat for all 15 hidden fields.
8. Click Update.

### Verifying hidden field population

1. Open `/request-to-book/?utm_source=test&utm_campaign=verify` in the browser.
2. Open DevTools > Elements.
3. Find any `<input type="hidden" name="utm_source">` element.
4. Its `value` attribute should read `"test"`.
5. Find `<input type="hidden" name="visitor_id">`. It should contain a UUID string matching `window.__sssVid`.

If the fields are empty, confirm that: the global JS is loaded (check console for errors), the field `name` attributes match exactly, and the form is not inside an iframe.

### Email capture form (homepage)

The homepage email capture form is in `03_HTML_SNIPPETS/homepage/email-capture-section.html`. It is a custom HTML form, not a MetForm widget. It uses the CSS class `.sss-email-form` and has one input with `name="email"`. The global JS Section 6 handles submission. The only hidden field needed here is `source_type`, which the JS sets to `email_capture` in the webhook payload.

The contact form on the Contact page has its own webhook placeholder `WIRE_THIS_CONTACT_WEBHOOK_URL` in `pages/contact/contact-html-snippets.html`. Wire this with the appropriate Make.com scenario webhook URL.

---

## 10. Step 7: Chatbot Installation

**Files:** `chatbot/chatbot-css.css` and `chatbot/chatbot-js.js`
**Time required:** 20 minutes

### Prerequisites

- Tidio must be fully deactivated (not just toggled off in its own settings, but deactivated at the WordPress Plugins level) before proceeding.
- Global JS (Step 2) must already be installed. Chatbot JS depends on `window.__sssVid` and `window.dataLayer` which are set by global JS.
- The chatbot webhook URL from Make.com must be available before wiring the JS.

### Part A: Install chatbot CSS (head)

The chatbot CSS must go in the `<head>`, not the footer. This ensures the chat widget is styled before it renders, preventing a flash of unstyled content.

1. Open `chatbot/chatbot-css.css` in a text editor. Select all. Copy.
2. In WordPress admin, go to Settings > Insert Headers and Footers > Scripts in Header.
3. Add this block (the CSS content goes inside the `<style>` tags):

```html
<style>
/* She Said Sail Chatbot CSS */
/* Paste the full contents of chatbot/chatbot-css.css here */
</style>
```

4. Click Save.

### Part B: Wire the chatbot webhook URL

Before adding the JS to WordPress, you must replace the webhook placeholder:

1. Open `chatbot/chatbot-js.js` in a text editor.
2. Search for `WIRE_THIS_CHATBOT_WEBHOOK_URL`.
3. Replace it with the Make.com webhook URL from the M-CHATBOT-001 scenario (or the equivalent webhook you create in Step 9).
4. Save the file.

The URL will look like: `https://hook.eu2.make.com/XXXXXXXXXXXXXX`

### Part C: Install chatbot JS (footer, after global JS)

The chatbot JS must load AFTER the global JS. Source order in the footer determines execution order. The chatbot uses `window.__sssVid` and `window.dataLayer`, both of which are set by the global JS.

1. Open the edited `chatbot/chatbot-js.js`. Select all. Copy.
2. In WordPress admin, go to Settings > Insert Headers and Footers > Scripts in Footer.
3. You will see the global JS script block already there from Step 2. Paste the chatbot script block AFTER the global JS block:

```html
<script defer>
/* She Said Sail Chatbot JS */
/* Paste the full contents of chatbot/chatbot-js.js here */
</script>
```

4. Click Save.

The footer text area should now contain two script blocks in this order:

```
[global JS block]
[chatbot JS block]
```

### Part D: Chatbot behavior overview

The chatbot is a pure vanilla JS state machine with no dependencies. It creates its own DOM elements and injects them into the page body. States:

```
idle > opener > occasion > energy > size > recommendation > date > name > email > phone > handoff > closed
```

At `handoff` state, the chatbot fires a webhook payload to Make.com with: occasion, occasion_energy, guest_count, selected_experience, preferred_date, first_name, email, phone, conversation_summary, landing_page, UTM fields, visitor_id, brand, service_category, and source_type ("chatbot").

It also fires GTM events at each state transition. See `chatbot/chatbot-analytics-events.md` for the full event list.

### Part E: Verify chatbot installation

1. Open the homepage in a browser.
2. A chat toggle icon should appear in the bottom-right corner (the Tidio icon should NOT appear).
3. Click the toggle. The chat widget should open with the opener greeting.
4. Open DevTools > Console. Type `window.__sssChatLoaded`. It should return `true`.
5. Open DevTools > Network. Complete a full chatbot conversation through to the handoff step. The network panel should show a POST request to the Make.com webhook URL with status 200.
6. In GTM Preview mode, confirm `chatbot_open`, `chatbot_start_conversation`, `chatbot_select_occasion`, and `chatbot_handoff` events appear in the panel.

---

## 11. Step 8: Airtable Setup

**Reference files:** `05_AIRTABLE_BACKEND/airtable-table-schema.md`, `05_AIRTABLE_BACKEND/airtable-field-map.md`, `05_AIRTABLE_BACKEND/intelligence-tables.md`
**Time required:** 2 hours for original 7 tables; 2 additional hours for intelligence layer

### Part A: Create the base

1. Log in to Airtable at airtable.com.
2. In your workspace, click "+ Add a base."
3. Choose "Start from scratch."
4. Name the base: "She Said Sail CRM."
5. Note the Base ID from the URL: `airtable.com/[BASE_ID]/...`

### Part B: Create tables in order

Create tables in this specific order. Tables that use linked record fields must exist before the fields that link to them are created.

**Creation order:**

1. Contacts (create first, because Requests links to it)
2. Campaigns (create second, because UTMs links to it)
3. UTMs (links to Requests and Campaigns)
4. Requests (links to Contacts and UTMs)
5. Bookings (links to Requests and Contacts)
6. Client Notes (links to Contacts and Bookings)
7. Audit Log (no links, standalone)

For detailed field specifications for each table (field name, type, select options, formulas), refer to `05_AIRTABLE_BACKEND/airtable-table-schema.md`. Every field type, single-select option, and formula is documented there.

### Part C: Key fields to note

**Requests table:** The `Status` single-select field must have exactly these options in this order: New, Contacted, Qualified, Proposal Sent, Booked, Closed Lost. The Make.com scenario M-BOOKING-OUTCOME-001 watches for "Booked" specifically.

**UTMs table primary field:** The primary field is a Formula field, not a plain text field. Formula: `utm_source & " / " & utm_campaign & " / " & submission_page`. Create this formula field as the primary field when creating the table.

**Bookings table:** The `Balance Due` field is a Formula: `Total Value - Deposit Paid`. Create the Total Value and Deposit Paid currency fields before creating the formula.

### Part D: Create views

For each table, create the views documented in `airtable-table-schema.md`. Views are not optional: Make.com scenarios and team members rely on specific views to operate efficiently.

Key views to create first:

| Table | View | Filter |
|---|---|---|
| Requests | New Requests | Status = New |
| Requests | Hot Leads | Internal Rating = Hot |
| Contacts | Email Subscribers | Email Subscribed = true |
| Bookings | Upcoming Charters | Charter Date is on or after today |
| Audit Log | Errors | Status = Error |

### Part E: Get your Airtable credentials for Make.com

1. Go to airtable.com > Account > Developer Hub.
2. Click "Create token."
3. Name it: "She Said Sail Make Integration."
4. Scopes: select `data.records:read`, `data.records:write`, `schema.bases:read`.
5. Base access: select the "She Said Sail CRM" base.
6. Copy the token. Store it securely. You will not see it again.

---

## 12. Step 9: Make.com Scenarios

**Reference file:** `06_MAKE_WEBHOOKS/make-webhook-setup.md`
**Time required:** 3 hours for 10 original scenarios; 2 additional hours for 4 intelligence scenarios

### Build order

Do not deviate from this order. Later scenarios depend on earlier ones being tested and stable.

1. M-WEBFORM-REQUEST-CAPTURE
2. M-UTM-CAPTURE
3. M-EMAIL-CAPTURE
4. M-INQUIRY-CONFIRMATION-EMAIL
5. M-SLACK-NEW-LEAD-ALERT
6. M-AIRTABLE-AUDIT-LOGGER
7. M-BRAND-ROUTER
8. M-CONCIERGE-ASSIGNMENT
9. M-BOOKING-INTENT-LOGGER
10. M-EXPERIENCE-CLICK-TRACKING

Intelligence scenarios (build only after original 10 are stable and tested):

11. M-BOOKING-OUTCOME-001
12. M-WEEKLY-REPORT-001
13. M-EXPERIENCE-ROLLUP-001
14. M-CONCIERGE-SCORE-001

### Creating each scenario

For each scenario:

1. In Make.com, click "Create a new scenario."
2. Add the trigger module (Custom Webhook or Airtable Watch Records, as specified in `make-webhook-setup.md`).
3. For webhook triggers: click "Add" to create a new webhook. Name it using the scenario ID. Copy the webhook URL immediately after creation.
4. Build each subsequent module in the documented sequence.
5. Save the scenario. Do NOT activate it yet.
6. Test the scenario using the test payloads in `06_MAKE_WEBHOOKS/test-payloads.md` and `06_MAKE_WEBHOOKS/request-capture-payload.json`.
7. Only activate the scenario after a successful test run.

### Webhook URL wiring

After creating each webhook-triggered scenario, wire the URL into the correct location:

| Scenario | Webhook URL goes into |
|---|---|
| M-WEBFORM-REQUEST-CAPTURE | `she-said-sail-global.js`: replace `WIRE_THIS_REQUEST_FORM_WEBHOOK_URL` |
| M-EMAIL-CAPTURE | `she-said-sail-global.js`: uncomment the fetch block, replace the placeholder URL |
| M-CHATBOT-001 (chatbot scenario) | `chatbot/chatbot-js.js`: replace `WIRE_THIS_CHATBOT_WEBHOOK_URL` |
| Contact form scenario | `pages/contact/contact-html-snippets.html`: replace `WIRE_THIS_CONTACT_WEBHOOK_URL` |

After wiring URLs, update the script blocks in Insert Headers and Footers with the edited JS file contents. The live script must contain the real URLs, not the placeholder strings.

### Error handling configuration

For each scenario in Make.com:

1. Click the scenario settings gear icon.
2. Set "Max number of cycles" to 1 (prevents loops on retries).
3. Under "Error handling," enable "Store incomplete executions" so you can inspect failed runs.
4. Set the schedule to "Immediately" for webhook-triggered scenarios.
5. For Airtable Watch Records triggers (M-BOOKING-OUTCOME-001, etc.), set polling interval to "Every 15 minutes."

### Key scenario: M-WEBFORM-REQUEST-CAPTURE module sequence

This is the most complex scenario. The full module sequence is documented in `make-webhook-setup.md`. Key points:

- Module 1: Custom Webhook (receives form payload)
- Module 3: Set Variable for `internal_rating`: if `occasion` is "Bachelorette" OR `group_size` is 15 or more, set "Hot"; otherwise set "Warm"
- Module 5-6: Search Contacts by email; branch on found/not-found
- Module 8: Create UTMs record; link to the new Requests record
- Module 11: Create Audit Log record with action "form_submission"

For the full module-by-module configuration, open `06_MAKE_WEBHOOKS/make-webhook-setup.md` and follow the Scenario M-WEBFORM-REQUEST-CAPTURE section.

---

## 13. Step 10: Analytics and Pixels

**Reference files:** `07_GTM_ANALYTICS/gtm-events-map.md`, `07_GTM_ANALYTICS/ga4-events.md`, `07_GTM_ANALYTICS/meta-pixel-events.md`, `07_GTM_ANALYTICS/tiktok-pixel-events.md`

### GA4 tags

All GA4 tags are configured in GTM, not added directly to the site. The only tag that needs the Measurement ID is the GA4 Configuration tag.

**GA4 Configuration tag:**

1. In GTM, go to Tags > New.
2. Tag type: "Google Analytics: GA4 Configuration."
3. Measurement ID: `GT-WV3X86GZ`
4. Trigger: All Pages.
5. Name the tag: "GA4 - Configuration."
6. Save.

**GA4 Event tags:** Create one GA4 Event tag per event listed in `gtm-events-map.md`. For each tag:

1. Tag type: "Google Analytics: GA4 Event."
2. Configuration Tag: select the GA4 Configuration tag above.
3. Event Name: the exact event name from the events map.
4. Event Parameters: add each parameter listed in the events map, using the corresponding DLV variable.
5. Trigger: the matching Custom Event trigger.

**Conversion events to mark in GA4:**

After publishing GTM, go to GA4 Admin > Events and mark these events as conversions:

- `view_thank_you_page`
- `click_request_to_book`
- `submit_booking_form`
- `click_phone`
- `chatbot_capture_email`
- `chatbot_capture_phone`
- `chatbot_handoff`

Micro-conversions (mark but do not use for bidding):

- `submit_email_capture`
- `scroll_90_percent`

**GA4 Custom Dimensions:** Register these in GA4 Admin > Custom Definitions > Custom Dimensions:

| Dimension Name | Scope | Event Parameter |
|---|---|---|
| cta_location | Event | `cta_location` |
| occasion | Event | `occasion` |
| experience_slug | Event | `experience_slug` |
| experience_name | Event | `experience_name` |
| form_name | Event | `form_name` |

### Meta Pixel tags

Open `07_GTM_ANALYTICS/meta-pixel-events.md` for the exact code snippets.

1. Create a Custom HTML tag named "Meta Pixel - Base Code." Trigger: All Pages. Code: the base pixel snippet from `meta-pixel-events.md`. Replace the placeholder with your actual Meta Pixel ID.
2. Create a Custom HTML tag named "Meta Pixel - Lead (form)." Trigger: CE - submit_booking_form. Code: the Lead event snippet.
3. Create a Custom HTML tag named "Meta Pixel - Lead (chatbot)." Trigger: CE - chatbot_handoff. Code: the Lead event snippet.
4. Create a Custom HTML tag named "Meta Pixel - Lead (chatbot email)." Trigger: CE - chatbot_capture_email. Code: the Lead event snippet.

### TikTok Pixel tags

Open `07_GTM_ANALYTICS/tiktok-pixel-events.md` for the exact code snippets.

1. Create a Custom HTML tag named "TikTok Pixel - Base Code." Trigger: All Pages. Replace the placeholder with your actual TikTok Pixel ID.
2. Create "TikTok Pixel - SubmitForm." Trigger: CE - submit_booking_form.
3. Create "TikTok Pixel - CompleteRegistration." Trigger: CE - view_thank_you_page.
4. Create "TikTok Pixel - Subscribe." Trigger: CE - submit_email_capture.

### chatbot_capture_phone: missing GTM trigger and tag

This event is pushed by `chatbot-js.js` but the trigger and tag are not pre-built in the GTM container. You must create them manually:

1. Create trigger: CE - chatbot_capture_phone. Type: Custom Event. Event name: `chatbot_capture_phone`.
2. Create GA4 Event tag: "GA4 - chatbot_capture_phone." Event name: `chatbot_capture_phone`. Add parameter `page_location`. Trigger: CE - chatbot_capture_phone. Mark as Conversion in GA4 after publishing.

### Publish GTM after all tags are created

After creating all tags, verify in GTM Preview mode:

1. Navigate to each key page (homepage, request to book, an experience page).
2. Confirm the expected `view_*` event fires on each page.
3. Submit the Request to Book form in preview mode. Confirm `start_booking_form` and `submit_booking_form` fire.
4. Submit the email capture form. Confirm `submit_email_capture` fires.

After Preview verification passes, click Submit and publish the container.

---

## 14. Step 11: Intelligence Layer

The intelligence layer adds six new Airtable tables and four new Make.com scenarios. It also requires small modifications to existing Airtable tables and JS files. Build this layer ONLY after the original 7 Airtable tables are stable and the 10 original Make.com scenarios are tested and running cleanly.

**Reference files:** `05_AIRTABLE_BACKEND/intelligence-tables.md`, `06_MAKE_WEBHOOKS/intelligence-scenarios.md`, `02_GLOBAL_JS/global-js-intelligence-addendum.md`

### Part A: Modify existing Airtable tables

Before creating new tables, add these fields to existing tables. Full field specs are in `intelligence-tables.md`.

**Requests table additions:**
- Source Type (Single Select: Form Lead, Chatbot Lead, Contact Form, Manual)
- Visitor ID (Short Text)
- Chatbot Conversation (Linked Record to new Chatbot Conversations table; create this link AFTER creating the Chatbot Conversations table)
- Revenue Attribution (Linked Record to new Revenue Attribution table; create this link AFTER creating that table)

**Bookings table additions:**
- Charter Cost (Currency)
- Gross Margin (Formula: Total Value minus Charter Cost)
- Margin Percent (Formula: Gross Margin divided by Total Value, percent)
- Days to Close (Formula: Charter Date minus linked Request's Submitted At)
- Revenue Attribution (Linked Record)

**Campaigns table additions:**
- Total Revenue (Rollup from linked Revenue Attribution records)
- Total Bookings (Rollup count)
- ROI Percent (Formula)
- Cost Per Booking (Formula)

### Part B: Create intelligence tables (in order)

Create tables in this order because later tables link to earlier ones:

1. Chatbot Conversations
2. Revenue Attribution
3. Experience Performance
4. Weekly Insights
5. Founder Decisions
6. Lessons Learned

Full field specifications for each table are in `05_AIRTABLE_BACKEND/intelligence-tables.md`.

### Part C: Update visitor_id in all webhook payloads

The visitor_id must be included in every Make.com payload. If it was not already added in Step 9, make these additions now per `02_GLOBAL_JS/global-js-intelligence-addendum.md`:

- `she-said-sail-global.js`: Add `visitor_id: window.__sssVid || ''` to the request form payload and the email capture payload.
- `chatbot/chatbot-js.js`: Add `visitor_id: window.__sssVid || ''` to the `fireWebhook()` function's payload object.
- `pages/contact/contact-html-snippets.html`: Add `visitor_id: window.__sssVid || ''` to the contact form submit handler payload.
- Update the script blocks in Insert Headers and Footers with the edited file contents.

### Part D: Build four intelligence Make.com scenarios

Build in this order per `intelligence-scenarios.md`:

**M-BOOKING-OUTCOME-001 (BOOKING-OUTCOME-LINKER):**
Trigger: Airtable Watch Records on Requests table, watching for Status changes to "Booked." Creates Revenue Attribution record linking Booking, Request, UTM, and Campaign. Posts to `#intelligence` Slack channel. Full module sequence in `intelligence-scenarios.md`.

**M-WEEKLY-REPORT-001 (WEEKLY-INTELLIGENCE-REPORT):**
Trigger: Scheduled, Monday 8:00 AM. Queries last 7 days of Requests, Bookings, and UTMs data. Formats an intelligence summary. Posts to `#intelligence` Slack channel. Creates Weekly Insights Airtable record.

**M-EXPERIENCE-ROLLUP-001 (EXPERIENCE-PERFORMANCE-ROLLUP):**
Trigger: Scheduled, Monday 8:30 AM. Aggregates booking and request counts by experience. Creates or updates Experience Performance records in Airtable.

**M-CONCIERGE-SCORE-001 (CONCIERGE-PERFORMANCE-SCORER):**
Trigger: Airtable Watch Records on Bookings table, watching for Status = "Deposit Received" or "Paid in Full." Calculates concierge response time and booking rate. Logs to Audit Log.

---

## 15. QA Flow

Run QA after each phase, not only at the end. Catching issues per phase is faster than debugging a fully integrated system.

### Phase 1 QA (after CSS + JS + GTM)

- [ ] Homepage loads with correct brand colors and fonts.
- [ ] No JS errors in console on any page.
- [ ] `window.__sssVid` is a valid UUID in console.
- [ ] UTM params from URL are captured to `sessionStorage.sss_utm`.
- [ ] GTM Preview shows "GTM-TZ5KNRTH connected."
- [ ] `window.dataLayer` is initialized before the GTM snippet fires.
- [ ] `view_homepage` event appears in GTM Preview on homepage load.

### Phase 2 QA (after HTML snippets)

- [ ] Social proof strip appears in the correct position on homepage and experiences page.
- [ ] Occasion pills appear in the hero section.
- [ ] Email capture section appears above the bottom CTA on homepage.
- [ ] Monaco Social six sections appear in the correct order.
- [ ] All experience page sections stack cleanly on 375px mobile width.
- [ ] No raw HTML appears as text on any page (indicates an Elementor paste error).

### Phase 3 QA (after forms and hidden fields)

Use the form QA checklist at `09_QA/form-qa-checklist.md`. Key checks:

- [ ] Submit the Request to Book form with all fields. Confirm redirect to /thank-you/.
- [ ] Check Airtable Requests table: new record appears within 30 seconds.
- [ ] Check Airtable UTMs table: UTM record linked to the Request appears.
- [ ] Check Airtable Contacts table: new or updated Contact record appears.
- [ ] Confirmation email received within 2 minutes.
- [ ] Slack `#new-leads` receives the lead alert.
- [ ] Hidden field `visitor_id` contains the UUID from `window.__sssVid`.
- [ ] Hidden field `source_type` contains `form_lead`.
- [ ] Hidden field `utm_source` contains the correct value when URL has `?utm_source=test`.
- [ ] Submit the email capture form. `submit_email_capture` event fires in GTM Preview.
- [ ] Make.com M-EMAIL-CAPTURE scenario run log shows a successful execution.

### Phase 4 QA (after chatbot)

Use the checklist at `chatbot/chatbot-qa.md`. Key checks:

- [ ] Chat toggle appears in bottom-right. Tidio is NOT visible.
- [ ] Full conversation flows through all states to handoff.
- [ ] `chatbot_open`, `chatbot_handoff` events appear in GTM Preview.
- [ ] Network panel shows a successful POST to the chatbot webhook URL.
- [ ] Airtable Requests table: new chatbot lead record appears with source_type "chatbot."
- [ ] Mobile: chat widget is usable on 375px screen without overflow.

### Phase 5 QA (after GTM tags and pixels)

Use the checklist at `09_QA/tracking-qa-checklist.md`. Key checks:

- [ ] GA4 DebugView shows events firing on each page.
- [ ] `click_request_to_book` event fires when clicking any request CTA.
- [ ] `submit_booking_form` fires on form submission with `occasion` and `group_size` parameters.
- [ ] `view_thank_you_page` fires on the thank-you page and is marked as a Conversion.
- [ ] Meta Pixel Helper (browser extension) shows the base pixel firing on all pages and the Lead event firing on form submission.
- [ ] TikTok Pixel Helper (browser extension) shows the base pixel firing on all pages.

### Phase 6 QA (after intelligence layer)

Use the checklist at `09_QA/backend-qa-checklist.md`. Key checks:

- [ ] Set a test Request's Status to "Booked" in Airtable. M-BOOKING-OUTCOME-001 creates a Revenue Attribution record within 15 minutes.
- [ ] The Revenue Attribution record links correctly to the Booking, Request, and UTM records.
- [ ] Wait for Monday 8:00 AM (or manually trigger M-WEEKLY-REPORT-001). Confirm Slack `#intelligence` receives the report and a Weekly Insights Airtable record is created.

---

## 16. Rollback Procedure

Every component of this deployment can be independently rolled back. Changes made in WordPress do not affect the git repository. Changes made in Airtable or Make.com do not affect WordPress.

### CSS rollback

1. Go to Appearance > Customize > Additional CSS.
2. Select all content in the text area. Delete it.
3. Click Publish.
4. Time required: 2 minutes.
5. Effect: site reverts to unstyled (theme defaults only).

### Global JS rollback

1. Go to Settings > Insert Headers and Footers > Scripts in Footer.
2. Delete the global JS script block.
3. Click Save.
4. Time required: 2 minutes.
5. Effect: UTM capture, hidden field population, and GTM events stop. Forms still submit (MetForm handles its own submission), but without tracking data.

### GTM rollback

1. In GTM, go to Versions.
2. Find the previous stable version.
3. Click the three-dot menu > Publish this version.
4. Time required: 5 minutes.
5. Effect: all GTM tags revert to the previous version. No site code changes needed.

### HTML snippet rollback (per snippet)

1. Open the affected page in the Elementor editor.
2. Right-click the HTML widget containing the snippet.
3. Click Delete.
4. Click Update.
5. Time required: 2 minutes per snippet.

### SEO metadata rollback

If metadata was added via Yoast SEO: go to the page editor, scroll to the Yoast SEO meta box, clear the fields, and click Update.

If metadata was added via Insert Headers and Footers: go to Settings > Insert Headers and Footers > Scripts in Header. Remove the relevant script or style block. Click Save.

### Chatbot rollback

1. Go to Settings > Insert Headers and Footers > Scripts in Footer. Delete the chatbot JS block. Click Save.
2. Go to Settings > Insert Headers and Footers > Scripts in Header. Delete the chatbot CSS block. Click Save.
3. If Tidio should be re-enabled: go to Plugins > Installed Plugins > find Tidio > Activate.
4. Time required: 5 minutes.

### Make.com scenario rollback

1. Open Make.com and navigate to the She Said Sail workspace.
2. Find the scenario you want to disable.
3. Click the toggle to deactivate the scenario. It will stop accepting webhook calls immediately.
4. Existing Airtable data is not affected by deactivating a scenario.
5. Time required: 1 minute per scenario.

### Airtable rollback

Airtable does not have a one-click rollback. To undo table modifications:

- For new tables: delete the table (this deletes all records and is irreversible).
- For new fields added to existing tables: go to the table, click the field header, and click "Delete field." This is irreversible for data already in that field.
- For view changes: views can be deleted or reverted manually.

Before making any intelligence layer table modifications, export a CSV of affected tables as a backup.

---

## 17. Staging vs Production Workflow

### What staging must verify before pushing to production

Staging should be a full copy of production including the same WordPress version, the same plugin versions, and the same Elementor templates. Staging must use a different GTM container (or GTM Preview mode), a different Airtable base (a test base), and sandbox webhook URLs from Make.com.

**Do not use production Airtable credentials in staging.** Test data pollutes production reports. Create a "She Said Sail CRM Test" base and use separate Make.com scenarios pointing to it.

### Staging verification checklist

Run through the full Phase 1 through Phase 5 QA from Section 15 on staging before touching production. Specifically:

- [ ] All HTML snippets render correctly on all 11 pages.
- [ ] Request to Book form submission creates correct Airtable records in the TEST base.
- [ ] Email capture webhook fires and receives a 200 response.
- [ ] Chatbot flows through to handoff and fires the webhook.
- [ ] GTM Preview shows all expected events for each user journey.
- [ ] No JavaScript errors on any page.
- [ ] Mobile view at 375px width: no overflow, no broken layouts on any page.
- [ ] Founder (Will) has reviewed and approved screenshots of every page on both desktop and mobile before any step moves to production.

### Production deployment order

After staging is verified and founder approval is received:

1. Apply CSS to production (Appearance > Customize > Additional CSS).
2. Add Global JS to production footer (Insert Headers and Footers, Scripts in Footer).
3. Add GTM head snippet and body noscript to production (Insert Headers and Footers).
4. Apply HTML snippets page by page.
5. Add SEO metadata page by page.
6. Add chatbot CSS to production header.
7. Update chatbot JS and global JS with production webhook URLs (not the staging URLs).
8. Add chatbot JS to production footer after global JS.
9. In Make.com, activate production scenarios (not staging scenarios).
10. Publish GTM container after verifying events in GTM Preview on production.

---

## 18. Known Limitations and Manual Steps

The following items cannot be automated and require a human to complete them. Each is noted with the exact location where action is required.

### Webhook URLs require manual wiring

All three webhook URL placeholders must be replaced with real URLs before launch. There is no way to generate these URLs without first creating the scenarios in Make.com.

| Placeholder | File | Replace with |
|---|---|---|
| `WIRE_THIS_CHATBOT_WEBHOOK_URL` | `chatbot/chatbot-js.js` | Make.com chatbot scenario webhook URL |
| `WIRE_THIS_CONTACT_WEBHOOK_URL` | `pages/contact/contact-html-snippets.html` | Make.com contact form scenario webhook URL |
| Commented-out email capture fetch block | `02_GLOBAL_JS/she-said-sail-global.js` | Make.com M-EMAIL-CAPTURE webhook URL (uncomment and replace URL) |
| Request form webhook reference | `02_GLOBAL_JS/she-said-sail-global.js` | Make.com M-WEBFORM-REQUEST-CAPTURE webhook URL |

### Airtable fields must be created by hand

There is no import file or API script in this pack. Every Airtable table and field must be created manually through the Airtable interface. The schema documents are specifications, not importable files.

### GTM container must be published manually

GTM changes do not go live until a developer explicitly clicks Submit in GTM and publishes the version. After creating all variables, triggers, and tags, verify in Preview mode, then publish.

### Meta Pixel ID and TikTok Pixel ID are not in this pack

These IDs belong to the business's ad accounts and are not stored in the code repository. Retrieve them from Meta Events Manager and TikTok Ads Manager before building the GTM pixel tags.

### Elementor loop template is managed separately

The experience card loop template is an Elementor Pro Loop template, not an HTML snippet. Changes to the card grid layout (not the copy) require editing the Elementor Loop template directly. The HTML snippet in `03_HTML_SNIPPETS/experiences/experience-card-content.html` provides the copy to enter into the loop template fields, not a replacement template.

### chatbot_capture_phone GTM trigger and tag are not pre-built

As documented in Step 10, this trigger and tag do not exist in the initial GTM container configuration. They must be created manually before the container is published.

### Privacy policy update required

After deploying the `sss_vid` cookie, the She Said Sail privacy policy must be updated to disclose: "We use a first-party cookie to recognize returning visitors for internal analytics purposes. This cookie does not contain personally identifiable information and is not shared with third parties."

### Slack channels must be created before Make scenarios activate

The Make.com scenarios post to `#new-leads` and `#intelligence` Slack channels. These channels must exist in the Slack workspace before any scenario that posts to them is activated. Make.com will throw a 404 error if the channel does not exist.

### Founder approval gates

Per the project brief, Will (founder) must review and approve screenshots before each page is published to production. This is a process gate, not a technical limitation. Build a review step into the deployment timeline between staging verification and production deployment.

---

## 19. Post-Launch Checklist

Complete all items in the first week after launch. These are monitoring and verification tasks, not installation tasks.

### Day 1 (launch day)

- [ ] Confirm GTM container is live and tags are firing. Check GTM > Versions: the published version timestamp should be recent.
- [ ] Open GA4 Realtime report. Navigate the site. Confirm events appear within 30 seconds.
- [ ] Submit a real test inquiry through the Request to Book form using a real email address. Verify: Airtable record created, confirmation email received, Slack `#new-leads` notification received.
- [ ] Complete a full chatbot conversation to handoff on mobile and desktop. Verify: Airtable record created with source_type "chatbot," webhook returned 200.
- [ ] Verify all four experience pages load correctly. Check experience-specific meta titles in browser tab.
- [ ] Verify hero images load with correct priority on desktop and mobile. Open DevTools > Network: hero image should appear near the top of the waterfall, not deferred.
- [ ] Check that the Tidio widget is NOT visible on any page.
- [ ] Verify the sss_vid cookie is set in DevTools > Application > Cookies.

### Days 2 to 3

- [ ] Review Airtable Audit Log for any errors from the past 24 hours. Check the "Errors" view.
- [ ] Review Make.com scenario run history. All active scenarios should show successful executions. Investigate any failed runs.
- [ ] Check GA4 Events report. Confirm event counts are appearing for: view_homepage, click_request_to_book, and submit_booking_form.
- [ ] Verify scroll depth events (`scroll_50_percent`, `scroll_90_percent`) are firing by scrolling through the homepage in GA4 DebugView.

### Day 7

- [ ] Monday morning: confirm M-WEEKLY-REPORT-001 fired at 8:00 AM and M-EXPERIENCE-ROLLUP-001 fired at 8:30 AM. Check Slack `#intelligence` for both reports.
- [ ] Check that Weekly Insights Airtable table has a new record for the past week.
- [ ] Review GA4 Conversions report for the first week. Confirm conversion events are registering with correct counts.
- [ ] Review Meta Events Manager: confirm the base pixel is firing and Lead events are showing up.
- [ ] Check the Contact Requests view in Airtable. All leads from the first week should have correct Source Type (form_lead or chatbot), UTM attribution, and Visitor ID.
- [ ] If any form leads are missing UTM data: check the sessionStorage capture logic in DevTools on the Request to Book page. Confirm hidden field values are populated before form submit.
- [ ] Confirm the site privacy policy has been updated with the sss_vid cookie disclosure.
- [ ] Review `09_QA/master-qa-checklist.md` end to end and confirm all items pass.
- [ ] Deliver final QA report to Will using the scorecards in `10_FINAL_AUDIT/`.

---

*End of Final Implementation Guide.*
*For any step not covered here, refer to the specific file documented in that step. All files referenced in this guide exist in the DEPLOYMENT_PACK directory.*
