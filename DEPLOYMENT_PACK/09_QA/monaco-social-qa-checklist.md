# She Said Sail: Monaco Social QA Checklist

**Version:** 1.0
**Page:** Monaco Social
**URL:** /experience/monaco-social/
**Framework reference:** master-qa-system.md

This checklist is specific to the Monaco Social experience page. Complete every item before sign-off. Use Pass / Fail / N/A in the brackets. Leave no item blank.

---

## 1. BEFORE YOU QA

Confirm the following before opening the page for QA. If any item below is not confirmed, stop and complete the install first.

- [ ] Global CSS is confirmed loaded site-wide
- [ ] Global JS is confirmed loaded in the footer site-wide
- [ ] All 6 Monaco Social HTML snippets have been added to the page in Elementor
- [ ] SEO meta tags have been applied via Yoast SEO or Insert Headers and Footers
- [ ] JSON-LD structured data is confirmed in page source
- [ ] The request-to-book form has been confirmed to accept the `selected_experience` URL param
- [ ] GTM tag `SSS - View Monaco Social Page` has been published

---

## 2. VISUAL QA (Desktop)

Test at 1440px viewport width and 1280px viewport width.

**Layout and spacing:**
- [ ] Page loads without horizontal scroll at 1440px
- [ ] Page loads without horizontal scroll at 1280px
- [ ] All sections have consistent vertical padding (no sections collapsed or overlapping)
- [ ] No sections show raw HTML or broken widget output

**Hero section:**
- [ ] H1 reads "Monaco Social" in correct heading style
- [ ] Subheadline reads "Champagne-led Riviera energy for birthdays and elevated groups." in italic
- [ ] Hero CTA button is visible, gold fill, navy text
- [ ] Hero background image loads and is not stretched or distorted

**Hero-support section:**
- [ ] Cream background visible
- [ ] Monaco Social name and tagline visible
- [ ] 3 quick-fact pills visible (duration, guest count, starting price)
- [ ] 4 occasion pills visible and spaced correctly
- [ ] No text overflow or clipping

**Experience-description section:**
- [ ] Left-column descriptive copy is visible
- [ ] Right-column "What is included" list is visible
- [ ] Two-column layout holds at 1280px without collapse

**Social-proof section:**
- [ ] Navy background renders correctly
- [ ] 2 testimonials visible with attribution
- [ ] Testimonial text is legible (white or cream on navy)
- [ ] No quote marks missing or doubled

**Occasion-fit section:**
- [ ] Left-column occasion positioning copy is visible
- [ ] Right-column occasion types list is visible
- [ ] Section background and typography match brand system

**Pre-cta-reassurance section:**
- [ ] 3-step process is visible with correct step numbers or icons
- [ ] All 3 steps have copy
- [ ] Section layout is centered or structured correctly

**Bottom-CTA section:**
- [ ] Navy background renders correctly
- [ ] Heading is visible
- [ ] Subtext is visible below the heading
- [ ] CTA button is gold fill with navy text
- [ ] "No commitment" or reassurance note appears below the button

---

## 3. MOBILE QA

Test at 375px (iPhone SE) and 390px (iPhone 14). Use Chrome DevTools device emulation.

**General:**
- [ ] No horizontal scroll at 375px
- [ ] No horizontal scroll at 390px
- [ ] Font sizes are legible at both viewports
- [ ] No text is clipped or hidden behind other elements

**Hero section (mobile):**
- [ ] H1 and subheadline are readable at 375px
- [ ] Hero CTA button is full-width at 375px
- [ ] Hero CTA button is full-width at 390px

**Hero-support section (mobile):**
- [ ] Quick-fact pills wrap or stack cleanly at 375px
- [ ] Occasion pills wrap cleanly and do not cause horizontal overflow
- [ ] No pill text is truncated

**Experience-description section (mobile):**
- [ ] Two-column layout stacks to single column at 375px
- [ ] Left column appears above right column when stacked
- [ ] List items in the right column are readable

**Social-proof section (mobile):**
- [ ] Testimonials stack to single column at 375px
- [ ] Text is legible on navy background at small size

**Occasion-fit section (mobile):**
- [ ] Two-column layout stacks at 375px
- [ ] List is fully visible

**Pre-cta-reassurance section (mobile):**
- [ ] 3-step process stacks vertically at 375px
- [ ] Step copy is readable

**Bottom-CTA section (mobile):**
- [ ] CTA button is full-width at 375px
- [ ] CTA button is full-width at 390px
- [ ] "No commitment" note is visible below the button
- [ ] Heading and subtext are readable

---

## 4. CONTENT QA

Check each snippet and the Elementor copy edits.

**Elementor copy edits:**
- [ ] H1 reads exactly "Monaco Social" (no variation, no extra words)
- [ ] H1 appears exactly once in the page source (right-click > View Source, search for `<h1`)
- [ ] Subheadline reads "Champagne-led Riviera energy for birthdays and elevated groups."
- [ ] Subheadline is styled italic

**hero-support.html:**
- [ ] Monaco Social name visible
- [ ] Tagline visible
- [ ] 3 quick-fact pills visible: duration, guest count, and starting price all present
- [ ] 4 occasion pills visible

**experience-description.html:**
- [ ] Left-column descriptive copy is present and complete
- [ ] Right-column "What is included" list is present
- [ ] All list items in the includes list are visible

**social-proof.html:**
- [ ] 2 testimonials present
- [ ] Both testimonials have attribution (name, occasion, or date)
- [ ] Testimonials are specific to Monaco Social or attributed to guests of this experience

**occasion-fit.html:**
- [ ] Left-column occasion positioning copy is present
- [ ] Right-column occasion types list is present
- [ ] Occasion types are specific to Monaco Social (not generic to all She Said Sail experiences)

**pre-cta-reassurance.html:**
- [ ] All 3 process steps are present
- [ ] Step copy is complete (no truncated or placeholder text)

**bottom-cta.html:**
- [ ] Heading is present
- [ ] Subtext is present
- [ ] CTA button text reads "Request Monaco Social"
- [ ] "No commitment" note is present below the button

**Em dash check:**
- [ ] No em dashes in page source. Right-click the page > View Source. Use browser Find (Ctrl+F or Cmd+F) and paste the Unicode em dash character (the character between these quotes: "") to search. Zero results expected.

**Prohibited words check:**
- [ ] The word "VIP" does not appear anywhere on the page
- [ ] The phrase "party boat" does not appear anywhere on the page
- [ ] The phrase "luxury rental" does not appear anywhere on the page
- [ ] The phrase "best yacht" does not appear anywhere on the page
- [ ] The word "exclusive" does not appear anywhere on the page
- [ ] The word "package" does not appear anywhere on the page

---

## 5. CTA QA

- [ ] Hero CTA button text reads exactly: "Request Monaco Social"
- [ ] Hero CTA button links to: `/request-to-book/?selected_experience=monaco-social`
- [ ] Bottom CTA button links to: `/request-to-book/?selected_experience=monaco-social`
- [ ] No CTA on this page uses the text "Book Now"
- [ ] No CTA on this page uses the text "Submit"
- [ ] No CTA on this page uses the text "Inquire"
- [ ] Hero CTA button is gold fill with navy text on desktop
- [ ] Bottom CTA button is gold fill with navy text on desktop
- [ ] Hero CTA button is full-width on mobile (375px)
- [ ] Bottom CTA button is full-width on mobile (375px)
- [ ] Clicking the hero CTA button opens `/request-to-book/?selected_experience=monaco-social` (not a new tab unless intended)
- [ ] Clicking the bottom CTA button opens `/request-to-book/?selected_experience=monaco-social`

---

## 6. SEO QA

- [ ] Meta description is present in page source. Search for `<meta name="description"` in View Source.
- [ ] Meta description reads: "Monaco Social is She Said Sail's champagne-led yacht experience in Miami. Built for birthdays and elevated groups. Up to 15 guests. Starting from $10,000."
- [ ] og:title is present: "Monaco Social | Private Yacht Experience Miami | She Said Sail"
- [ ] og:description is present and matches meta description
- [ ] og:image is present and the URL is a valid, accessible image (not a placeholder path)
- [ ] og:image:width is 1200
- [ ] og:image:height is 630
- [ ] og:image:alt is present
- [ ] og:site_name is "She Said Sail"
- [ ] twitter:card is "summary_large_image"
- [ ] twitter:title is present
- [ ] twitter:description is present
- [ ] twitter:image is present
- [ ] Canonical tag is present: `<link rel="canonical" href="https://shesaidsail.com/experience/monaco-social/" />`
- [ ] No duplicate canonical tags in page source
- [ ] No duplicate meta description tags in page source
- [ ] H1 appears exactly once on the page
- [ ] JSON-LD block is present in page source with `@type: Service`
- [ ] JSON-LD contains the Monaco Social name, description, price, and She Said Sail provider details
- [ ] JSON-LD is valid. Paste the script block contents into schema.org validator (https://validator.schema.org/) and confirm zero errors.

---

## 7. BACKEND QA

- [ ] Navigate to `/request-to-book/?selected_experience=monaco-social`
- [ ] Inspect the page DOM. Confirm the hidden field named `selected_experience` has the value `monaco-social`
- [ ] Submit a test form entry from `/request-to-book/?selected_experience=monaco-social`
- [ ] Open the form submissions log and confirm the test entry shows `selected_experience = monaco-social`
- [ ] Hidden UTM fields are present in the form DOM: `utm_source`, `utm_medium`, `utm_campaign`
- [ ] Confirm that navigating to `/request-to-book/` without URL params does not cause a form error (hidden fields can be empty)

---

## 8. ANALYTICS QA

Use GTM Preview mode for all analytics QA.

- [ ] Open GTM Preview and connect to the Monaco Social page URL
- [ ] On page load, confirm the event `view_monaco_social` fires
- [ ] Confirm `view_monaco_social` includes `page_location` with the Monaco Social URL
- [ ] Click the hero CTA button and confirm `click_request_to_book` fires
- [ ] Click the bottom CTA button and confirm `click_request_to_book` fires
- [ ] Confirm `view_monaco_social` does NOT fire on other pages (test by navigating to the homepage in the same GTM Preview session)
- [ ] Confirm `click_request_to_book` does NOT fire on non-CTA clicks

---

## 9. ACCESSIBILITY QA

- [ ] All images on the page have alt text. Check in View Source for `<img` tags missing `alt=`.
- [ ] og:image:alt is present and descriptive
- [ ] Hero image has descriptive alt text (not blank, not "image")
- [ ] CTA buttons have visible focus states (tab to them using keyboard; a visible outline should appear)
- [ ] Occasion pills are readable by keyboard (if interactive) or marked decorative (if not)
- [ ] Tap targets for CTA buttons are at least 44x44px on mobile. Check by inspecting the button element in DevTools at 375px.
- [ ] Text on navy background meets WCAG AA contrast ratio (minimum 4.5:1 for normal text). Use browser accessibility tools or https://webaim.org/resources/contrastchecker/ if unsure.

---

## 10. BRAND QA

- [ ] No em dashes anywhere on the page (confirmed in Content QA step above)
- [ ] No prohibited words (confirmed in Content QA step above)
- [ ] All copy uses first-person plural voice ("we," "our") or direct second-person ("you," "your") consistent with She Said Sail brand voice
- [ ] The page does not describe She Said Sail as a "company" (use "team" instead)
- [ ] Price references use "starting from" framing, not flat price claims
- [ ] Guest count references are accurate (up to 15 guests for Monaco Social)
- [ ] The word "champagne" is present and used to describe the Monaco Social experience
- [ ] No sentence on the page ends with the experience being described as "one of a kind" or "unlike any other" (generic superlatives not consistent with brand voice)

---

## 11. SIGN-OFF

All items above must be marked Pass before this section is completed.

| Item | Name | Date |
|------|------|------|
| Web builder QA complete | | |
| Will review and sign-off | | |

**Notes (issues found and resolved during QA):**

[Record any issues found and how they were resolved before sign-off.]
