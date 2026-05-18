# She Said Sail: Master QA System

**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul
**Last Updated:** 2026-05-18

---

## 1. QA PHILOSOPHY

Quality assurance is not a final step. It is the standard that defines "done."

A page is not done when the code is written. It is not done when it looks correct in one browser at one screen size. A page is done when every item in this checklist passes, every stakeholder has signed off, and the deployment pack is updated to reflect the work.

Skipping any section of this checklist is not acceptable, regardless of deadline pressure. A broken or underperforming page on the live site costs more than any delay.

---

## 2. WHEN TO RUN QA

Run the full QA checklist in each of the following situations:

- Before every merge from the feature branch (`feature/luxury-conversion-overhaul`) to staging
- Before every merge from staging to main
- After any significant WordPress change: CSS updates, plugin installs or removals, Elementor template edits
- After any Make.com scenario change or new scenario activation
- After any GTM tag change, trigger change, or container publish

Partial QA (Sections 3 and 4 only) is acceptable for minor copy edits or image swaps that do not touch code, forms, or integrations.

---

## 3. VISUAL QA

Test at the following breakpoints: desktop 1440px, desktop 1280px, mobile 375px, mobile 390px.

- [ ] Hero photography is warm and visible with overlay at the correct opacity
- [ ] Section headings use Cormorant Garamond at the correct size from the design system
- [ ] Gold accent colors are used only in the locations specified by the design system (no gold for body copy, no gold backgrounds except where specified)
- [ ] No layout breaks at any tested viewport width
- [ ] No text overflow or truncation in any section
- [ ] Cards have correct hover states: lift shadow, border color transition
- [ ] No horizontal scroll at any viewport width
- [ ] Social proof section is visible and positioned between the correct sections
- [ ] Email capture section renders correctly with correct background and input styling
- [ ] Footer renders with correct navy background, correct color, and correct spacing
- [ ] No images are distorted or stretched; all images maintain correct aspect ratios

---

## 4. MOBILE QA

- [ ] Hero is full viewport height on iPhone 14 (390px wide)
- [ ] Hero is full viewport height on iPhone SE (375px wide)
- [ ] All body text is readable without zooming (minimum 16px)
- [ ] All tap targets are minimum 44x44px (buttons, links, nav items)
- [ ] CTA buttons are full width on mobile
- [ ] Cards stack to a single column below 767px
- [ ] Social proof cards stack to a single column on mobile
- [ ] Email capture form stacks vertically with input above button
- [ ] Navigation burger menu opens and closes correctly
- [ ] Navigation closes when a nav link is tapped
- [ ] No horizontal scroll on any mobile viewport
- [ ] Form inputs use minimum 16px font size (prevents iOS auto-zoom behavior)
- [ ] Footer columns stack cleanly with correct spacing

---

## 5. CTA QA

- [ ] Page has exactly one primary CTA at the top of the visual hierarchy
- [ ] Primary CTA links to /request-to-book/
- [ ] CTA button uses the correct gold fill (#DAB97E) with navy text (#1A2332)
- [ ] CTA hover state is correct: transparent fill, cream border, cream text
- [ ] No competing CTAs at the same visual weight on the same screen section
- [ ] All anchor links and button links point to real URLs with no `href="#"` placeholders
- [ ] All CTAs open in the correct target (internal links in same tab, external links in new tab where appropriate)

---

## 6. SEO QA

- [ ] Meta description is present and under 160 characters
- [ ] Open Graph tag `og:title` is present
- [ ] Open Graph tag `og:description` is present
- [ ] Open Graph tag `og:image` is present and the URL returns HTTP 200
- [ ] Twitter Card tags are present (`twitter:card`, `twitter:title`, `twitter:description`)
- [ ] H1 appears exactly once in the page source (verify with browser dev tools or "find in page")
- [ ] All images have non-empty `alt` attributes
- [ ] Schema.org JSON-LD is present on the homepage (`global-schema.html` applied)
- [ ] /request-to-book/ has `noindex` set in the meta robots tag
- [ ] Canonical URL tag is present and points to the correct URL
- [ ] No broken internal links (check manually or with a link checker tool)

---

## 7. ANALYTICS QA

- [ ] GTM container (GTM-WWTT27Z3) fires on the page (verify in GTM Preview Mode)
- [ ] Page view event fires in the dataLayer on load with the correct event name
- [ ] CTA click event fires when the primary CTA is clicked
- [ ] Form start event fires on first interaction with any form field
- [ ] Form submit event fires on successful form submission
- [ ] All events appear in GA4 DebugView (GA4: GT-WV3X86GZ) with correct parameters
- [ ] GTM container is published to production (not only in Preview Mode)
- [ ] No duplicate events are firing (check dataLayer push history in browser console)
- [ ] Meta Pixel fires on page load (verify in Meta Pixel Helper browser extension)
- [ ] TikTok Pixel fires on page load if TikTok is an active ad channel

---

## 8. BACKEND QA

- [ ] All 13 standard hidden tracking fields are present in the form source code
- [ ] Test submission is received by Make.com (visible in execution history)
- [ ] Airtable Request record is created with all UTM fields populated and non-empty
- [ ] Contact record is created correctly or linked to an existing Contact
- [ ] UTM record is created and linked to the Request record
- [ ] Confirmation email is received by the test address within 2 minutes
- [ ] Slack alert is posted to #new-leads
- [ ] Audit Log entry is created with correct timestamp and scenario reference
- [ ] Second submission using the same email address: no duplicate Contact created, new Request created

---

## 9. ACCESSIBILITY QA

- [ ] All images have descriptive alt text (not just file names or empty strings)
- [ ] All form inputs have an associated `<label>` or `aria-label` attribute
- [ ] Focus states are visible on all interactive elements when navigating by keyboard
- [ ] A skip-to-main-content link is present and functional
- [ ] Color contrast for body text on white background passes WCAG AA (minimum 4.5:1 ratio)
- [ ] Color contrast for large text (18px+ or 14px+ bold) on colored backgrounds passes WCAG AA (minimum 3:1 ratio)
- [ ] No information is conveyed by color alone (icons, text, or patterns also communicate the same information)
- [ ] The page can be fully navigated using keyboard only (Tab, Enter, Escape, arrow keys)

---

## 10. PERFORMANCE QA

- [ ] PageSpeed Insights mobile score is 50 or above (target: 65 or above)
- [ ] PageSpeed Insights desktop score is 75 or above (target: 85 or above)
- [ ] LCP (Largest Contentful Paint) is under 4.0 seconds (target: under 2.5 seconds)
- [ ] CLS (Cumulative Layout Shift) is under 0.25 (target: under 0.1)
- [ ] No render-blocking scripts in the `<head>` unless they are deferred or async
- [ ] Hero image file size is under 300KB (target: under 200KB, format: WebP preferred)
- [ ] No unused plugins are loading assets on the page (verify in Network tab of browser DevTools)

---

## 11. TRUST QA

- [ ] Phone number is a real, tappable `tel:` link (not plain text)
- [ ] Location reference links to the correct Google Maps listing
- [ ] At least one testimonial is visible on the page (required on homepage and experiences pages)
- [ ] Price anchor is present on the homepage (starting from $10,000)
- [ ] Form has a trust note below or near the submit button (e.g. concierge will respond within 24 hours)
- [ ] Concierge reassurance block is present on the /request-to-book/ page

---

## 12. CONVERSION QA

- [ ] Social proof section appears before the primary CTA on the page
- [ ] Email capture section is present on the homepage
- [ ] Thank you page exists at /thank-you/ and loads without error
- [ ] Form submission reaches /thank-you/ or shows a clear inline success state
- [ ] No dead ends: every page has a clear, visible next action for the visitor

---

## 13. BRAND QUALITY QA

- [ ] No em dashes anywhere in the page source (search for Unicode em dash character: U+2014)
- [ ] None of the following prohibited words appear in page copy: VIP, party boat, luxury rental, submit inquiry, book now
- [ ] Section labels use "Experiences" not "Packages"
- [ ] Hero copy leads with a feeling or occasion, not a product description
- [ ] Testimonials include specific attribution: first name, occasion type, and experience name where possible

**How to check for em dashes on changed files:**
```bash
grep -rn $'\xe2\x80\x94' [file-or-directory]
```

---

## 14. SIGN-OFF REQUIREMENT

The QA checklist must be signed off before any merge to main.

**Developer or web builder** signs off on Sections 3 through 11 and Section 13. This confirms technical correctness, visual accuracy, and brand compliance.

**Founder (Will)** signs off on Section 12 (conversion judgment), Section 14 (overall approval), and any copy that represents the brand voice.

Do not merge to main until founder sign-off is documented in the pull request or the deployment record. A comment in the GitHub pull request with "Approved for production" is sufficient documentation.
