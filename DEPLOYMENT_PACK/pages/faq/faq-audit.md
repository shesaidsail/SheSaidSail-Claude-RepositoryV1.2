# FAQ Page: Optimization Audit

**Page:** /faq/
**Slug:** faq
**Audit date:** 2026-05-18
**Auditor:** Optimization Team

Scoring scale: 1 (absent or harmful) to 10 (fully realized).
Baseline: a standard FAQ page with no schema, minimal copy, no brand voice, and no analytics.

---

## Dimension 1: Luxury Positioning

**Before: 3**
A generic FAQ page with plain question-and-answer formatting, no editorial voice, no typography hierarchy, and no design consistency with the brand. Reads like a help center document, not a luxury service.

**After: 8**
Category headings use Cormorant Garamond italic, anchoring the editorial voice of the brand across a utility page. The concierge framing runs throughout: answers describe what the concierge does, what the concierge sends, what the concierge confirms. The tone is calm and knowledgeable, matching the warmth of a five-star property rather than a FAQ wall. The eyebrow "Before You Ask" and the H1 "Everything you want to know." are direct but refined. The bottom CTA uses the full navy-and-gold design language from the rest of the site.

**Remaining gap:** No photography on this page. A single editorial image between the header and the categories would reinforce luxury positioning further.

---

## Dimension 2: Emotional Conversion

**Before: 4**
A generic FAQ page reduces anxiety but a bland one does not build desire or urgency. It answers questions neutrally without converting the emotional state of the reader.

**After: 8**
All 18 questions address real objections that arise before a high-consideration purchase: deposit anxiety, weather fear, not knowing group minimums, not knowing what is included. Each answer closes with enough warmth that the reader feels reassured rather than processed. Inline CTAs after the Booking, Experience, and Group Size categories provide micro-conversion moments inside the content. The bottom CTA names the benefit (hear back within 24 hours) rather than just the action. Together the page moves a visitor from uncertain to ready.

**Remaining gap:** No social proof embedded in the FAQ section. A single quote from a past guest placed between two categories would strengthen emotional conversion further.

---

## Dimension 3: Mobile UX

**Before: 4**
A typical FAQ page with accordion JavaScript often has tap targets that are too small, answers that appear inside collapsed containers with low readability, and no mobile-specific layout consideration.

**After: 8**
All answers are permanently visible. No tap-to-reveal required. Category headings scale from 28px to 24px on mobile. Question text scales from 17px to 16px. The bottom CTA buttons stack full-width at 767px. Padding reduces from 96px to 64px on mobile to preserve reading space. No horizontal overflow. Font sizes and line-heights are set for comfortable reading at all sizes.

**Remaining gap:** Sticky category navigation for very long mobile sessions would improve orientation, but is not essential for launch.

---

## Dimension 4: Trust and Social Proof

**Before: 5**
FAQ pages inherently build trust by existing. They show operational readiness. A bare FAQ scores a baseline 5 because it signals that the business anticipated questions.

**After: 8**
18 confidently answered questions signal operational maturity. The answers cover edge cases (weather, gratuity, group minimums) that only a company with real experience knows to address. The gratuity answer is particularly trust-building: it names the industry standard, explains how it is handled, and promises no surprises. The weather answer is direct without being legalistic. The returning guest answer signals an ongoing relationship, not a transactional one. Together these answers demonstrate that She Said Sail has done this many times and knows exactly what its guests need to know.

**Remaining gap:** The page does not include guest reviews or star ratings. These would raise this dimension to 9 or 10. Could be added as a small testimonial block below the FAQ categories.

---

## Dimension 5: Backend Readiness

**Before: 8**
FAQ pages require no backend. A basic FAQ page scores high here by default.

**After: 9**
The page is correctly structured with no orphaned form fields, no broken API dependencies, and no placeholder backend logic. The documentation in faq-backend.md clearly explains that the page has no backend integration and explains why that is the correct design. The connection to /request-to-book/ is correctly handled as a simple link. The FAQPage schema is a front-end SEO feature with no backend dependency. This dimension is nearly maximized because backend complexity would be incorrect for this page type.

**Remaining gap:** One point withheld because the og:image is a placeholder and needs to be replaced before launch. That is a minor content gap, not a backend gap.

---

## Dimension 6: Analytics Readiness

**Before: 2**
No page view event, no interaction tracking, no audience definitions. A standard FAQ page often has only default GA4 pageview data with no meaningful segmentation.

**After: 8**
The view_faq_page event fires on load, enabling accurate measurement of FAQ reach. The global JS handles click_request_to_book and click_explore_experiences automatically. Scroll depth events provide engagement depth data. The GA4 audience "Visited FAQ - No Submit" is documented as a high-intent remarketing segment, which is a meaningful strategic addition. GTM setup instructions are specific and complete.

**Remaining gap:** The GA4 audience cannot be verified until GTM is published and data accumulates. Audience creation is documented but not yet executed.

---

## Dimension 7: SEO

**Before: 3**
No FAQPage schema. No meta description. No canonical tag. No Open Graph. Accordion-style FAQ pages hide answer text from Google's crawler or force an extra rendering step. Rich snippet potential: zero.

**After: 9**
FAQPage JSON-LD schema includes all 18 questions. This is the maximum schema coverage possible for this page and gives Google the complete set of Q&A pairs to evaluate for rich result eligibility. All answers are visible in HTML, so they are fully indexed without JavaScript rendering dependency. The meta title targets the primary keyword (private yacht charters Miami). The meta description is 139 characters, under the 155-character limit. Canonical tag is set. Open Graph is complete. Internal links to /request-to-book/ and /experiences/ distribute page authority. The 18 answers contain natural keyword phrases for long-tail queries that reach this page from organic search.

**Remaining gap:** Rich snippet appearance is at Google's discretion and cannot be confirmed pre-launch. Monitor Google Search Console post-publish.

---

## Dimension 8: Performance

**Before: 7**
A basic FAQ page with minimal CSS scores reasonably well for performance. Accordion JavaScript adds weight but is typically small.

**After: 8**
No JavaScript accordion. The FAQ section is pure HTML and CSS. There are no third-party scripts added by this page beyond the global JS already loaded site-wide. All styles use custom properties from the existing design system. No new fonts are introduced. Render-blocking resources are not added. The additional CSS for this page is minimal and can be inlined or bundled with the global stylesheet.

**Remaining gap:** Page-level performance depends on the CMS or static site renderer, which is outside the scope of these optimization files.

---

## Score Summary

| Dimension | Before | After | Change |
|---|---|---|---|
| Luxury Positioning | 3 | 8 | +5 |
| Emotional Conversion | 4 | 8 | +4 |
| Mobile UX | 4 | 8 | +4 |
| Trust and Social Proof | 5 | 8 | +3 |
| Backend Readiness | 8 | 9 | +1 |
| Analytics Readiness | 2 | 8 | +6 |
| SEO | 3 | 9 | +6 |
| Performance | 7 | 8 | +1 |
| **Overall Average** | **4.4** | **8.3** | **+3.9** |

---

## Remaining Gaps After This Optimization

1. FAQPage rich snippet verification: can only be confirmed after publishing and Google crawling the live URL. Check Google Search Console Enhancements section 2 to 4 weeks post-launch.

2. GA4 audience creation: "Visited FAQ - No Submit" must be created in GA4 Admin after GTM is published and view_faq_page data is confirmed live. Estimated setup time: 15 minutes.

3. og:image placeholder: replace the image comment placeholder in faq-metadata.html with a real 1200x630 brand photo before publishing.

4. Optional trust enhancement: a small testimonial block between categories would raise Trust and Social Proof from 8 to 9 or 10. Not required for launch.

5. Optional luxury enhancement: a single editorial image added to the page would raise Luxury Positioning from 8 to 9. Not required for launch.
