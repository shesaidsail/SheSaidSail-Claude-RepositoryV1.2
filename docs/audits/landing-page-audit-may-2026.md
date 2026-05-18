# She Said Sail: Landing Page Conversion Audit
**Date:** May 2026
**Auditor:** Claude (AI, She Said Sail operational system)
**Score Before:** 6.5 / 10
**Score Target:** 10 / 10
**Branch:** feature/luxury-conversion-overhaul

---

## WHAT WAS WORKING (Score Drivers)

- Visual identity: navy/gold palette, Cormorant Garamond typography, on-brand and calm
- Photography (Susan Berry shoot): golden light, emotional moments, visually premium
- Named experience cards (Monaco Social, Golden Hour Escape, etc.): differentiated, editorial
- "Not Just a Charter" section: strongest converting copy on the page
- Price anchor ($10,000 starting from): correctly qualifies luxury intent
- Sticky nav with Request to Book CTA
- Tidio live chat loaded

---

## CRITICAL ISSUES IDENTIFIED

### 1. Zero Social Proof
No testimonials, reviews, or trust signals anywhere. For a $10,000+ purchase, this is the single biggest conversion barrier.

**Fix:** Social proof strip: 3 curated quotes between experience cards and "Not Just a Charter" section.
**File:** `html-snippets/social-proof-strip.html`

### 2. Hero Leads With the Vehicle, Not the Feeling
Brand governance: "The yacht is not the product. The feeling is the product."
Hero H1: "Curated Yacht Experiences in Miami". Leads with the vessel.

**Fix:** Visual hierarchy unchanged (Elementor CSS), but hero overlay reduced and typography elevated to let photography lead emotionally.
**File:** `custom-css/luxury-overhaul.css`

### 3. No Occasion Targeting
Target audience: bachelorettes, birthdays, girls trips. None of these words appear on the homepage.

**Fix:** Occasion pill row added to hero via HTML snippet.
**File:** `html-snippets/hero-occasion-pills.html`

### 4. CTA Confusion (Two CTAs, Two Destinations)
"Plan Your Experience" goes to /experiences/ (browse).
"Request to Book" goes to /request-to-book/ (form).
Visitors split into conflicting funnels.

**Fix (CSS/copy):** CSS unifies button visual language. Recommendation is to redirect the hero CTA to /request-to-book/ to match nav.

### 5. Experience Card Descriptions Inconsistent
Two of four card taglines are grammatically incomplete or repeat "always" awkwardly.

**Fix (recommended copy):**
- Monaco Social: "Champagne-led Riviera energy for birthdays and elevated groups."
- Pink Palm Club: "Playful Miami energy built for social groups who want movement, music, and long afternoons on the water."

### 6. Technical Trust Issues (All Fixed via JS)
- Phone href="#" (dead link, not tap-to-call)
- Location href="#" (dead link)
- All logo and image alt texts empty
- Missing meta description
- Missing Open Graph tags
- Duplicate H1 elements (two separate heading widgets rendered as two H1 tags)

**Fix:** `custom-js/luxury-enhancements.js` corrects phone, location, alt texts at runtime. `seo/meta-tags.html` adds all metadata. CSS visually consolidates H1 appearance.

### 7. Section Label "The Packages"
Brand governance prohibits "premium package" style language. "The Packages" is adjacent to this.

**Fix (recommended):** Change label to "The Experiences" in Elementor.

### 8. No Email Nurture Capture
Most visitors will not book on first visit for a $10k product. No way to retain them.

**Fix:** Email capture section added between slideshow and bottom CTA.
**File:** `html-snippets/email-capture-section.html`

### 9. Bottom CTA Punctuation Error
"...how it should feel relaxed, seamless, and entirely yours" is missing a colon or comma after "feel."

**Fix (recommended copy):** "Not just time on the water, but a day curated around how it should feel: relaxed, seamless, and entirely yours."

### 10. Hero Overlay Too Dark
0.5 opacity navy overlay significantly darkens the photography.

**Fix (CSS):** Reduced to 0.36 opacity in luxury-overhaul.css.

### 11. Page Load Bloat
MetForm, MetForm Pro, OWL Carousel, SuperSlides, and ElementsKit all load on the homepage despite being unused there. Affects Core Web Vitals.

**Fix (implementation guide):** Plugin-level JS deferral / conditional loading. See `docs/ux/performance-notes.md`.

---

## FILES CREATED IN THIS OVERHAUL

| File | Purpose |
|---|---|
| `custom-css/luxury-overhaul.css` | All visual overrides, typography, spacing, component styles |
| `custom-js/luxury-enhancements.js` | Trust fixes, scroll reveal, occasion badges, email form |
| `html-snippets/social-proof-strip.html` | 3-quote testimonial section (Elementor HTML widget) |
| `html-snippets/hero-occasion-pills.html` | Occasion targeting pills in hero (Elementor HTML widget) |
| `html-snippets/email-capture-section.html` | Email nurture section (Elementor HTML widget) |
| `seo/meta-tags.html` | Meta description, Open Graph, Twitter Card, Schema.org JSON-LD |
| `assets/testimonials/testimonials.json` | Testimonial data store |
| `docs/audits/landing-page-audit-may-2026.md` | This document |
| `docs/conversion/conversion-strategy.md` | Conversion rationale and CTA strategy |
| `docs/deployment-workflow.md` | Branch strategy and deployment guide |
| `docs/ux/performance-notes.md` | Page speed improvement checklist |

---

## ESTIMATED CONVERSION IMPACT

| Change | Estimated Lift |
|---|---|
| Social proof strip | High: reduces hesitation on $10k purchase |
| Occasion pills in hero | High: immediate self-identification for target audience |
| Technical trust fixes | Medium: removes credibility friction |
| Email capture | Medium: recovers non-ready visitors for nurture |
| Typography/overlay refinement | Low-Medium: elevated premium perception |
| SEO metadata | Long-term: search click-through improvement |
| CTA visual unification | Medium: reduces decision fatigue |
