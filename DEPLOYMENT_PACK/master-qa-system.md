# SHE SAID SAIL
# MASTER QA SYSTEM

STATUS: PRODUCTION
VERSION: v1.0

---

## PRE-LAUNCH QA CHECKLIST

Run this checklist on every page before publishing.

---

## SECTION 1: COPY QA

- [ ] No em dashes anywhere on page (headings, body, labels, buttons, tooltips)
- [ ] No prohibited words: amazing, unforgettable, epic, luxury lifestyle, elite, baller, premium package, exclusive access, high-end vibe, next-level
- [ ] No hard-close sales language
- [ ] No fake scarcity ("only 2 spots left" unless factually true)
- [ ] No "VIP experience" phrasing
- [ ] No "don't hesitate to reach out"
- [ ] Headlines match brand voice (observational, calm, confident)
- [ ] CTA buttons use approved copy from master-copy-system.md
- [ ] Form labels are clear and human
- [ ] Error/success messages match brand tone
- [ ] All phone numbers formatted consistently: (000) 000-0000

---

## SECTION 2: VISUAL QA

- [ ] Brand colors used correctly (navy, gold, cream, white)
- [ ] No off-brand typefaces
- [ ] Heading hierarchy correct (H1 > H2 > H3 per page)
- [ ] Only one H1 per page
- [ ] Images load correctly at all breakpoints
- [ ] No broken image placeholders
- [ ] Alt text present on all images
- [ ] Logo loads correctly (desktop and mobile)
- [ ] Footer present and complete

---

## SECTION 3: MOBILE QA

- [ ] Page tested at 375px (iPhone SE)
- [ ] Page tested at 390px (iPhone 14 Pro)
- [ ] Page tested at 768px (iPad)
- [ ] No horizontal scroll at any mobile breakpoint
- [ ] All buttons minimum 44px height on mobile
- [ ] CTA buttons full-width on mobile
- [ ] Font sizes never below 15px body / 10px labels
- [ ] Images cropped appropriately for mobile (not zoomed-out desktop crops)
- [ ] Form fields full-width on mobile
- [ ] Touch targets never overlap

---

## SECTION 4: FORM QA

- [ ] All required fields marked and validated
- [ ] Hidden fields present: source_url, utm_source, utm_medium, utm_campaign, utm_content, utm_term, page_name, brand, city
- [ ] UTM capture script active
- [ ] Form submits to correct Webflow webhook endpoint
- [ ] Make.com receives test submission
- [ ] Airtable record created on test submission
- [ ] Auto-reply email sent on test submission
- [ ] Slack alert fires on test submission
- [ ] Duplicate submission blocked (idempotency check)
- [ ] Form success message shows on submit
- [ ] Form error state shows on failed submit

---

## SECTION 5: SEO QA

- [ ] Title tag present, under 60 characters
- [ ] Meta description present, under 155 characters
- [ ] OG:title present
- [ ] OG:description present
- [ ] OG:image present (1200x630px minimum)
- [ ] OG:type set (website or article)
- [ ] Twitter card tags present
- [ ] Canonical URL correct
- [ ] Schema markup present (LocalBusiness or TouristAttraction where applicable)
- [ ] No duplicate H1 tags
- [ ] Page loads from correct URL (no redirect chains)

---

## SECTION 6: PERFORMANCE QA

- [ ] All images are WebP or compressed JPEG
- [ ] Hero image under 300KB
- [ ] All below-fold images lazy loaded
- [ ] Page CSS minified (or handled by Webflow)
- [ ] Custom JS minified and deferred
- [ ] Google Tag Manager loads without console errors
- [ ] No render-blocking resources above the fold
- [ ] LCP element identified and loading=eager

---

## SECTION 7: ACCESSIBILITY QA

- [ ] Color contrast 4.5:1 for body text
- [ ] Focus states visible on all interactive elements
- [ ] All images have meaningful alt text (not empty, not "image")
- [ ] Form fields have associated labels (for attribute matches id)
- [ ] No content conveyed by color alone
- [ ] Keyboard navigable (tab through form, buttons)
- [ ] Screen reader: heading structure logical

---

## SECTION 8: ANALYTICS QA

- [ ] GTM container loads on page
- [ ] GA4 pageview fires on load
- [ ] Form submission event fires (with page_name, experience dimensions)
- [ ] CTA click events fire
- [ ] UTM parameters captured in analytics session
- [ ] No duplicate pageview events

---

## SIGN-OFF CRITERIA

Page may be published when:
- All Section 1-4 items checked (mandatory)
- All Section 5 items checked (mandatory for new pages)
- Minimum 80% of Section 6-8 items checked

Document QA results in page-specific qa.md file before launch.
