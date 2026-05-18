# Rose Day Club: Optimization Audit

Page: /experience/rose-day-club/
Branch: feature/luxury-conversion-overhaul
Audit date: 2026-05-18

---

## Scorecard Summary

| Dimension | Before | After | Change |
|---|---|---|---|
| Luxury Positioning | 4 | 8 | +4 |
| Emotional Conversion | 3 | 8 | +5 |
| Mobile UX | 5 | 8 | +3 |
| Trust | 3 | 8 | +5 |
| Backend | 2 | 7 | +5 |
| Analytics | 2 | 7 | +5 |
| SEO | 4 | 8 | +4 |
| Performance | 6 | 6 | 0 |
| **Overall** | **3.6** | **7.5** | **+3.9** |

---

## Dimension Rationale

### Luxury Positioning: 4 to 8

**Before:** Standard Elementor layout with generic charter copy. No distinct visual identity. Headline and body copy leaned on common superlatives. The page read like a category page, not an experience page.

**After:** Dedicated typographic system using Cormorant Garamond and Inter throughout. Section-by-section visual rhythm with distinct background alternation. Copy focuses on feeling and occasion, not amenities and specs. The brand positioning ("social hosting from water to table") comes through clearly. No prohibited adjectives or inflated language. The experience is shown through specific, evocative copy rather than asserted with labels.

**Remaining gap:** Photography and real visual assets will move this score further. The HTML is structured to receive and display them well, but the OG image placeholder is not yet replaced.

---

### Emotional Conversion: 3 to 8

**Before:** Descriptive copy with no emotional arc. No testimonials integrated into the page flow. CTA appeared once at the top with generic "book now" language.

**After:** Copy builds an emotional picture across five sections before the CTA closes. The description section opens with the feeling ("an afternoon that feels indulgent without feeling over the top"). Social proof section with two specific, voice-rich testimonials placed at the midpoint. Occasion fit section addresses the reader directly ("You do not need a reason. You just need a date."). Reassurance section reduces friction before the final CTA. The bottom CTA does not demand commitment; it frames the ask as an easy first step.

**Remaining gap:** A real photograph in the hero or description section would significantly increase emotional resonance before the copy does its work.

---

### Mobile UX: 5 to 8

**Before:** Single responsive Elementor stack with no mobile-specific type scaling. Columns stacked in the wrong order on some viewports. Quick facts rendered in a cramped horizontal row on 375px. No scoped mobile styles.

**After:** All six sections have explicit @media (max-width: 767px) breakpoints. H1 scales from 52px to 38px. Tagline scales from 24px to 20px. Quick facts stack vertically with clear dividers. Two-column grids collapse in the correct reading order (left/text first). CTA button expands to full width with max-width constraint. Padding reduced from 96px to 64px across all sections. Pills wrap cleanly without overflow.

**Remaining gap:** Performance (score unchanged at 6) limits the mobile experience on slower connections. This is a hosting and image optimization issue outside the scope of this build.

---

### Trust: 3 to 8

**Before:** No testimonials. No social proof. No process explanation. No reassurance copy near CTAs. Starting price not visible on the experience page.

**After:** Two named testimonials with occasion attribution in a dedicated social proof section. Starting price ($10,000) visible in the quick facts strip. Explicit "How It Works" section with a 3-step process. Disclaimer copy below the CTA ("No deposit required to inquire. No commitment until you are ready.") removes the biggest hesitation point for a high-consideration purchase. The reassurance copy uses second-person language to speak directly to the reader's concern.

**Remaining gap:** Review count and platform attribution (e.g., Google, direct) would add a further trust signal. Currently the testimonials are attributed by first name and occasion only.

---

### Backend: 2 to 7

**Before:** No documentation of field mapping. Hidden field pre-population not verified. No routing documentation. Risk of submissions landing in the wrong flow or missing experience attribution.

**After:** All 13 standard hidden fields documented with expected values. selected_experience field pre-population method documented and tied to the existing Monaco Social install guide (Step 7) for consistency. Make.com routing documented: M-BRAND-ROUTER reads selected_experience and routes to the She Said Sail flow. No new infrastructure required. Verification step documented for the developer.

**Remaining gap:** Automated backend QA (e.g., a test submission that validates field values in Airtable) is not yet part of the deployment workflow. This would push the score to 9.

---

### Analytics: 2 to 7

**Before:** No experience-level data layer events. Page views tracked only at the generic GA4 level. No CTA click tracking. No scroll depth. No way to segment by experience in GA4.

**After:** view_experience_page event fires on load with experience_slug: "rose-day-club". click_request_to_book fires on both CTA instances with slug and destination URL. scroll_50_percent and scroll_90_percent fire via global JS. All four events covered by existing GTM infrastructure with no new tags, triggers, or variables required. GA4 audience recommendation documented for retargeting and funnel analysis.

**Remaining gap:** CTA location parameter (hero / description / bottom) depends on global JS implementation. If that parameter is not yet in the global script, it would need to be added. Segment-level conversion tracking (i.e., which occasion type correlates with highest conversion) requires additional event enrichment not yet in scope.

---

### SEO: 4 to 8

**Before:** Default WordPress title tag. No custom meta description. No Open Graph tags. No JSON-LD. No canonical tag. Experience slug not used as a structured data identifier.

**After:** Custom title tag ("Rose Day Club | She Said Sail"). Meta description at 128 characters (within 155-char limit), includes experience name, occasion types, location, and price anchor. Full Open Graph package including type, locale, image placeholder with correct dimensions. Twitter card at summary_large_image. Canonical tag pointing to correct URL. JSON-LD Service schema with offer, price, provider (LocalBusiness with Miami FL address), and audience description. H1 is the experience name. Heading hierarchy is logical.

**Remaining gap:** OG image placeholder must be replaced with an actual 1200x630 photograph before launch. Without it, social shares will render without a preview image.

---

### Performance: 6 to 6 (unchanged)

**Before:** Standard Elementor page load behavior. No targeted optimization in this build.

**After:** This build does not introduce new performance issues. Styles are scoped inline within HTML snippets (no additional stylesheet requests). No new JavaScript. No new image assets (OG image is a placeholder). The score remains at 6 because the underlying hosting, Elementor overhead, and image optimization strategy are outside the scope of this optimization pack.

**Path to improvement:** Implement WebP images with srcset for the hero and OG image. Evaluate Elementor vs. custom page builder for this section. Defer non-critical scripts. These are infrastructure decisions that belong in a separate performance sprint.

---

## Remaining Gaps Across All Dimensions

1. **Photography.** Real, high-quality photography is the single highest-leverage remaining gap. The entire copy and layout system is built to frame photography that does not yet exist in this pack. This gap affects Luxury Positioning, Emotional Conversion, and SEO simultaneously.

2. **OG image placeholder.** The og:image and twitter:image tags reference a placeholder URL that must be replaced before launch. If the page launches with the placeholder, social shares will break or render blank.

3. **Backend test submission.** A verified test submission that confirms all 13 hidden field values appear correctly in Airtable is not yet completed. This should be the final step before the page goes live.

4. **Global JS verification.** The analytics events (view_experience_page, click_request_to_book, scroll depth) depend on the global JS being present and active on the experience page. Confirm the script loads on /experience/* pages in the WordPress environment.

5. **Performance sprint.** The hosting and Elementor overhead that hold the Performance score at 6 are best addressed in a dedicated sprint after the content and conversion work is stable.
