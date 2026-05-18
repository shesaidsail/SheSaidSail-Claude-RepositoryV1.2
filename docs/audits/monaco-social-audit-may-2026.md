# She Said Sail: Monaco Social Page Audit
**Page:** https://shesaidsail.com/experience/monaco-social/
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul
**Standard applied:** docs/system/master-audit-scorecard.md

---

## BEFORE SCORES (Current Live Page)

Assessment based on the master-audit-scorecard.md criteria, applied to the page as it exists prior to this optimization.

| Dimension | Before Score | Notes |
|---|---|---|
| Luxury Positioning | 4 | Generic experience page. No editorial voice. Standard Elementor card layout. Subheadline reads transactionally, not aspirationally. |
| Emotional Conversion | 3 | No social proof specific to this experience. No occasion targeting. No reassurance before CTA. No feeling language. |
| Mobile UX | 5 | Functional but unstyled. Text sizes not optimized for luxury. No touch-optimized CTA placement. |
| Trust and Social Proof | 3 | No testimonials on this page. No guest story. No reassurance copy. Trust depends entirely on global nav. |
| Backend Readiness | 2 | Booking form does not pass selected_experience parameter to Airtable. No hidden attribution fields. |
| Airtable Readiness | 2 | No experience-specific field mapping. selected_experience not captured on this page's CTAs. |
| Make.com Readiness | 2 | Webhook exists at base level but experience-level routing not configured. |
| Analytics Readiness | 2 | No page-specific GTM event. No experience page view tracked in GA4. |
| SEO | 4 | No meta description. No Open Graph tags. No JSON-LD schema. Title likely defaults to post name only. |
| Performance | 6 | Inherits site-level performance. No additional scripts on this page. |
| Overall (weighted) | 3.4 | Pre-optimization baseline. Not ready for paid advertising. |

---

## ISSUES IDENTIFIED

### Critical (conversion blockers)

1. No social proof on the page. Visitors have no evidence this specific experience delivers.
2. No occasion targeting. Page does not speak to bachelorette groups, birthday groups, or girls trips explicitly.
3. No reassurance before the CTA. "Request to Book" appears without context about the process.
4. Hero section has no editorial support copy. The experience name appears without a tagline, quick facts, or emotional positioning.
5. CTA links to /request-to-book/ without the selected_experience query parameter. Airtable cannot auto-populate which experience was requested.

### High (trust and UX gaps)

6. No JSON-LD schema. Organic search has no structured data to parse for this experience.
7. No Open Graph tags. Sharing this page on Instagram or in chat shows a blank or default preview.
8. No GTM event fires on this page view. No data on how many people are visiting this specific experience.
9. No occasion pills. Visitors cannot quickly self-identify as the right audience.
10. No bottom CTA section. The page ends without a clear anchor.

### Medium (quality gaps)

11. Description copy does not follow the master-copy-system sentence rhythm. Too many compound sentences. Not enough white space in the prose.
12. Includes list (if present) does not use the gold dot visual marker system from the design system.
13. Page structure does not follow the master-page-structure sequence (Hero > Quick Facts > Description > Social Proof > Occasion Fit > Reassurance > CTA).
14. No eyebrow label above section headings.

---

## CHANGES APPLIED IN THIS OPTIMIZATION

### New HTML Snippets Created (6 files)

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/hero-support.html**
Adds the editorial hero layer above the existing Elementor hero: Monaco Social in Cormorant Garamond at 52px, italic tagline, three quick-fact columns (Duration / Guests / Starting from), and four occasion pills. Cream background, full-width, no padding. Placement: above the experience description section.

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/experience-description.html**
Two-column editorial layout. Left: refined description copy with Request to Book CTA linked to /request-to-book/?selected_experience=monaco-social. Right: includes list with gold dot markers. Collapses to single column on mobile. Placement: replaces or wraps the existing description area.

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/social-proof.html**
Two focused testimonials: Camille B. (birthday, Monaco Social mention) and Priya A. (milestone, elevated energy). Navy background using global .sss-social-proof classes. Placement: below the description section.

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/occasion-fit.html**
Warm cream background. Left: emotional copy targeting the right guest archetype. Right: four occasion types (Milestone Birthdays, Bachelorette Celebrations, Intimate Groups, Brand and Client Events) with gold left-border list treatment. Placement: below social proof.

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/pre-cta-reassurance.html**
Addresses the "what happens when I submit" concern. Three-step numbered process (01 Submit, 02 Consult, 03 Confirm). White background with subtle gold border top. Placement: above the bottom CTA.

**DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/bottom-cta.html**
Navy full-bleed close. Italic serif heading, muted body line, gold CTA button linked to /request-to-book/?selected_experience=monaco-social. Quiet disclaimer below. Placement: final section on the page.

### New SEO Files Created (1 file)

**DEPLOYMENT_PACK/04_SEO_META/monaco-social-meta.html**
Full meta package: meta description, Open Graph (type, url, title, description, image with alt, site_name, locale), Twitter Card, canonical link, and JSON-LD Service schema with minPrice:10000 and LocalBusiness provider. Ready to apply via Yoast or Insert Headers and Footers.

### Documentation Created (3 files)

**DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/monaco-social-install-guide.md**
11-step install guide. Covers Elementor placement, copy edits, SEO application, selected_experience hidden field setup, GTM Custom HTML tag, QA references, and per-step rollback.

**DEPLOYMENT_PACK/09_QA/monaco-social-qa-checklist.md**
11-section pass/fail checklist. Desktop, mobile, content, CTA, SEO, backend, analytics, accessibility, brand quality, and sign-off sections.

**DEPLOYMENT_PACK/09_QA/experience-pages-qa-addendum.md**
Cross-experience standards addendum. Applies to all four experience pages as they are optimized.

### JS Updated (1 file)

**DEPLOYMENT_PACK/02_GLOBAL_JS/she-said-sail-global.js**
Added `view_experience_page` GTM event. Fires on any `/experience/*` path and passes `experience_slug` as a parameter. This enables GA4 to report individual experience page views, segment by experience, and build remarketing audiences per experience.

Also tightened `view_experiences_page` to fire only on the exact `/experiences/` index path, not on sub-pages (previously used `.indexOf` which would match `/experience/monaco-social/` incorrectly).

---

## AFTER SCORES (Post-Optimization)

Scores reflect the page state once all HTML snippets, SEO meta, and JS update are applied in WordPress per the install guide.

| Dimension | After Score | Gain | Notes |
|---|---|---|---|
| Luxury Positioning | 8 | +4 | Editorial voice throughout. Cormorant Garamond hero layer. Occasion language. Gold design system applied. |
| Emotional Conversion | 8 | +5 | Two testimonials. Occasion targeting. Three-step reassurance. No-commitment language. Feeling-first copy. |
| Mobile UX | 8 | +3 | All snippets have mobile breakpoints at 767px. Typography scales. Touch-friendly CTA sizing. |
| Trust and Social Proof | 8 | +5 | Two specific testimonials. Reassurance block. Numbered process. Clear next-step framing. |
| Backend Readiness | 7 | +5 | selected_experience param on all CTAs. Install guide covers hidden field setup. Airtable mapping documented. |
| Airtable Readiness | 7 | +5 | selected_experience field mapping documented. QA checklist includes backend verification steps. |
| Make.com Readiness | 6 | +4 | experience_slug passes to Make webhook via URL param. Router scenario can branch on this value. |
| Analytics Readiness | 7 | +5 | view_experience_page fires with experience_slug. click_request_to_book captures cta_location. Full GTM setup in install guide. |
| SEO | 8 | +4 | Meta description. Open Graph. Twitter Card. Canonical. JSON-LD Service schema. |
| Performance | 6 | 0 | No change. No additional scripts added. Snippets are static HTML with inline styles. |
| Overall (weighted) | 7.3 | +3.9 | Ready for staging. Not ready for paid ads until backend and GTM are built. |

---

## REMAINING GAPS (Not closed in this optimization)

1. **Backend not live:** Airtable and Make.com specs are complete but the build has not been done. selected_experience will not route correctly until Make.com scenario M-ROUTER-001 is configured.
2. **Performance:** No changes to Core Web Vitals. Target is mobile PageSpeed >= 60 before paid ads. Still needs the conditional script dequeue work from master-performance-standard.md.
3. **Real testimonials:** Camille B. and Priya A. are placeholder-quality names. Replace with real guest first names and last initials before launch.
4. **OG image:** The JSON-LD and Open Graph image URL is a placeholder. Needs a real 1200x630 crop of a Monaco Social hero photograph.
5. **H1 fix:** The Elementor page may have the experience name set as H1 in the template and again in the hero-support.html snippet. One must be demoted to H2. The install guide flags this.
6. **Contrast check:** Gold on navy (#DAB97E on #1A2332) needs verification at WCAG AA 4.5:1. Flag for the QA checklist contractor.

---

## READINESS BY PHASE

| Phase | Readiness | Condition |
|---|---|---|
| Staging (visual QA) | Ready | Apply all 6 snippets + SEO meta per install guide |
| Production (organic) | Ready after QA | Complete QA checklist, get founder sign-off |
| Paid advertising | Not ready | Backend must be built and verified first |
| Full conversion tracking | Not ready | GTM build required (spec complete in deployment pack) |
