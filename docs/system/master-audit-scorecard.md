# She Said Sail: Master Audit Scorecard

**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul
**Last Updated:** 2026-05-18

---

## 1. PURPOSE

The scorecard gives a fast, consistent evaluation of any page on the She Said Sail website. Use it at the start of an optimization to set the honest baseline score, and again at the end to measure the result.

Scores are not aspirational. They reflect the current state of the page at the time of evaluation. A score of 7 means work remains. A score of 5 means the page should not ship. The scorecard exists to tell the truth, not to validate effort already spent.

Every audit document for every page on this site uses this exact scorecard.

---

## 2. HOW TO SCORE

Score each of the 10 dimensions from 1 to 10 using the criteria in Sections 3 through 12.

**Overall score formula:**
Sum all 10 dimension scores, then divide by 10. Round to one decimal place.

Record all scores in the table template from Section 13, with a brief note explaining each score.

---

## 3. DIMENSION 1: LUXURY POSITIONING (1-10)

Measures: does the page feel like it belongs to a world-class hospitality brand, or does it feel like a local boat rental listing?

**1-3:** Page feels generic or promotional. Leads with product description, price, or features. Could belong to any charter company or event vendor.

**4-5:** Has some elevated elements (good photography or clean layout) but also contains corporate language, stock-style imagery, or salesy CTAs like "Book Now" or "Get a Quote."

**6-7:** Generally elevated tone and design. Some inconsistencies remain: one section uses overly promotional language, or a button label breaks the editorial tone.

**8-9:** Consistently calm, warm, and editorial throughout. Photography leads. Copy is specific, composed, and avoids promotion. Every section would feel at home in a luxury travel publication.

**10:** Indistinguishable from a world-class luxury hospitality brand. Zero inconsistencies in copy, design, photography selection, or CTA language. No outside reviewer would identify it as a local business website.

---

## 4. DIMENSION 2: EMOTIONAL CONVERSION (1-10)

Measures: does the page make the target visitor feel "this is for me" and "I want this" before they reach the CTA?

**1-3:** No emotional resonance. Purely functional or informational. Could describe any service for any audience.

**4-5:** Has some emotional language but does not connect with the specific occasion (bachelorette, birthday, girls trip). Could be speaking to anyone.

**6-7:** Addresses the target audience with some specificity. Uses occasion language in at least one section. Testimonials may be generic.

**8-9:** The visitor immediately self-identifies. Occasion language is woven throughout. Testimonials have specific names, occasions, and experiences. The page speaks directly to the reason they are on the site.

**10:** The page creates desire and trust simultaneously from the first section to the last. The CTA feels like the natural next step in a decision already made, not a sales moment. No persuasion is needed because the page has already done the work.

---

## 5. DIMENSION 3: MOBILE UX (1-10)

Measures: does the page provide a polished, intentional experience on mobile devices?

**1-3:** Broken layout on mobile. Text is unreadable, CTAs do not work, or sections overlap.

**4-5:** Functional on mobile but not polished. Text may be too small, cards may not stack correctly, or spacing feels cramped.

**6-7:** Correct stacking, readable text, working CTAs. Feels like a responsive desktop page rather than a designed mobile experience.

**8-9:** Smooth, elegant, and intentional on mobile. No layout issues at 375px or 390px. All touch targets meet the 44x44px minimum. Typography is appropriately scaled.

**10:** The mobile experience is as refined as the desktop. The page was designed for mobile from the start, not adapted. No compromises in spacing, typography, or image quality.

---

## 6. DIMENSION 4: TRUST (1-10)

Measures: does the page give visitors enough trust signals to feel confident taking the next step?

**1-3:** No social proof. No real contact information. No price anchor. No testimonials. Nothing on the page reduces purchase anxiety.

**4-5:** Has some trust signals but they are weak or generic (e.g. a star rating with no context, or testimonials without names or occasions).

**6-7:** Real testimonials with first names. Working phone link. Price anchor present. Location referenced.

**8-9:** Multiple trust signals working together: testimonials with full attribution (name, occasion, experience name), concierge language, specific pricing, real tap-to-call phone number, Google Maps link.

**10:** By the end of the page, the visitor has no unanswered trust questions. They know who they are calling, what they will pay, what past guests experienced, and exactly what happens after they submit the form.

---

## 7. DIMENSION 5: BACKEND READINESS (1-10)

Measures: does every form submission create clean, complete, attributable data in the backend?

**1-3:** No form integration. Forms go nowhere, or submissions land in an unmapped email inbox with no Airtable record created.

**4-5:** A form exists and submits somewhere, but hidden tracking fields are missing or the Make.com webhook is not configured.

**6-7:** Form is wired to Make.com and creates an Airtable record, but some UTM fields are missing, deduplication is not implemented, or the audit log is not written.

**8-9:** All 13 hidden fields are mapped, UTM capture works end to end, Airtable receives clean records with correct field values, Slack alert fires, confirmation email sends.

**10:** Complete data pipeline. Every form submission creates the correct Airtable records (Request, linked Contact, linked UTM), triggers the confirmation email, fires the Slack alert, writes the audit log entry, and attributes the submission correctly to its originating campaign. Deduplication works. Test records have been cleaned up.

---

## 8. DIMENSION 6: ANALYTICS READINESS (1-10)

Measures: is the page fully instrumented so that every meaningful visitor action is tracked?

**1-3:** No custom tracking. Only the default GA4 page view from the GA4 tag fires.

**4-5:** GTM container is installed and fires, but no custom events have been configured for this page.

**6-7:** Page view event and primary CTA click event are firing. Form events may be missing or not verified in GA4.

**8-9:** All relevant events fire correctly: page view, CTA clicks, form start, form submit, scroll depth. GA4 receives them, conversion events are marked, relevant audiences are defined.

**10:** Full funnel is tracked and verified. Form start, submit, all CTA clicks, scroll depth at 50% and 90%, all confirmed in GA4 DebugView. Meta Pixel and TikTok Pixel verified where applicable. No duplicate events. Data Layer variable names follow the `dlv_` convention.

---

## 9. DIMENSION 7: SEO (1-10)

Measures: is the page technically prepared to rank and share correctly?

**1-3:** No meta description. No Open Graph tags. Duplicate H1 or no H1 present.

**4-5:** Meta description present but Open Graph tags are missing or H1 is incorrect. Page would share poorly on social.

**6-7:** Meta description, Open Graph tags, and correct H1 all present. Twitter Card tags or Schema.org markup missing.

**8-9:** Full metadata suite: meta description, og:title, og:description, og:image, Twitter Card tags, Schema.org JSON-LD, correct single H1, all image alt text populated.

**10:** Complete SEO implementation with no technical warnings in Google Search Console. Canonical URL is correct. Structured data validates in the Rich Results Test. No broken internal links. Pages that should be noindexed (e.g. /request-to-book/) have the correct robots directive.

---

## 10. DIMENSION 8: PERFORMANCE (1-10)

Measures: does the page load fast enough to retain visitors, especially on mobile?

**1-3:** PageSpeed Insights mobile score below 40. LCP above 5 seconds. Page visibly slow.

**4-5:** PageSpeed Insights mobile score 40-54. Unused plugins loading assets. LCP between 4 and 5 seconds.

**6-7:** PageSpeed Insights mobile score 55-64. LCP under 3.5 seconds. Some optimization still available.

**8-9:** PageSpeed Insights mobile score 65-79. LCP under 2.5 seconds. Hero image under 200KB. CLS under 0.1.

**10:** PageSpeed Insights mobile score 80 or above. LCP under 2.0 seconds. CLS under 0.1. No unused plugins loading. All images in WebP format and compressed. No render-blocking resources.

---

## 11. DIMENSION 9: OPERATIONAL MATURITY (1-10)

Measures: is the page maintainable, documented, and deployable by someone who did not build it?

**1-3:** No documentation. The CSS is inline or scattered. Changes require investigation to understand what was done and why.

**4-5:** Some documentation exists but it is incomplete. Key decisions are not explained. There is no deployment guide.

**6-7:** Key files are documented. An implementation guide exists in the deployment pack. Another developer could make changes, but rollback would be difficult.

**8-9:** Full deployment pack coverage: CSS files, JS files, HTML snippets, SEO meta file, install guide, QA checklist, audit document. Rollback instructions are present.

**10:** Any competent developer or web builder can apply, test, rollback, or extend every change on this page using the documentation alone, with no briefing from the original implementer. The deployment pack is complete and up to date.

---

## 12. DIMENSION 10: VISUAL CONSISTENCY (1-10)

Measures: does this page feel like it belongs to the same brand system as every other page on the site?

**1-3:** Uses different colors, fonts, spacing, or design patterns than the established system. Feels like a separate site.

**4-5:** Mostly consistent with some clear outliers: a button using the wrong color, a section with different padding, or a font weight not in the type scale.

**6-7:** Consistent typography and color usage. Minor spacing inconsistencies or component variations that most visitors would not notice.

**8-9:** Fully consistent with the master design system. All components match established patterns for cards, buttons, section headers, testimonials, and email capture.

**10:** Visually indistinguishable from a page designed as part of a single cohesive system. Nothing feels added as an afterthought. A designer reviewing all pages together would see no inconsistencies.

---

## 13. SCORE TABLE TEMPLATE

Copy this table into every audit document and fill in each row.

| Dimension | Score | Notes |
|---|---|---|
| Luxury Positioning | /10 | |
| Emotional Conversion | /10 | |
| Mobile UX | /10 | |
| Trust | /10 | |
| Backend Readiness | /10 | |
| Analytics Readiness | /10 | |
| SEO | /10 | |
| Performance | /10 | |
| Operational Maturity | /10 | |
| Visual Consistency | /10 | |
| **Overall** | **/10** | **Average of above** |

---

## 14. SCORE THRESHOLDS

| Score Range | Status | Recommended Action |
|---|---|---|
| Under 5.0 | Do not ship | Major work required across multiple dimensions before any launch |
| 5.0-6.9 | Soft launch only | Acceptable for organic traffic. Do not run paid ads to this page. |
| 7.0-7.9 | Ready for staging | Pass full QA checklist before pushing to production |
| 8.0-8.9 | Production ready | Minor polish acceptable over time. Safe for paid traffic. |
| 9.0+ | Flagship quality | Use as the reference standard for future pages |

A page that ships at under 7.0 is a liability to the brand and to paid ad spend. The cost of a poor experience is higher than the cost of the delay.
