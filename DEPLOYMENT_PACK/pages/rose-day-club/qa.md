# SHE SAID SAIL
# ROSE DAY CLUB — QA CHECKLIST

PAGE: Rose Day Club
URL: https://shesaidsail.com/experience/rose-day-club/
VERSION: 1.0
STANDARD: master-qa-system.md v1.0

---

## STATUS: READY FOR HUMAN IMPLEMENTATION

All code assets are delivered. QA below is for human verification post-implementation in Webflow.

---

## SECTION 1: COPY QA

- [ ] No em dashes anywhere on page
- [ ] No prohibited words: amazing, unforgettable, epic, luxury lifestyle, elite, premium package, exclusive access, high-end vibe, next-level
- [ ] No hard-close sales language
- [ ] No fake scarcity
- [ ] No "VIP experience" phrasing
- [ ] No "don't hesitate to reach out"
- [ ] Hero headline confirmed: "Sun on the water. Ros&eacute; in hand. Everything handled."
- [ ] H1 is present and singular on the page
- [ ] CTA buttons use approved copy: "Plan Your Day", "Request Your Date", "Send Your Inquiry"
- [ ] FAQ tone is reassuring, not defensive
- [ ] Form labels are human and clear
- [ ] Success message tone is warm and confirms next steps

---

## SECTION 2: VISUAL QA

- [ ] Navy (#0a2342) used correctly in hero, social proof, footer CTA
- [ ] Gold (#c9a84c) used for labels, dividers, accents only
- [ ] Cream (#f9f6f0) used for details strip, gallery background
- [ ] White used for inclusions, FAQ sections
- [ ] Gold rule dividers (40px x 1px) present at section openers
- [ ] Heading hierarchy: H1 (hero) > H2 (section headings) > H3 (form success)
- [ ] Only one H1 on the page
- [ ] Hero image loads and covers full section
- [ ] Overlay gradient present on hero (text is readable)
- [ ] All gallery images load correctly
- [ ] Footer CTA section is navy with white text

---

## SECTION 3: MOBILE QA (Test at 375px, 390px, 768px)

- [ ] No horizontal scroll at 375px
- [ ] No horizontal scroll at 390px
- [ ] Hero text is readable at 375px (H1 minimum 32px)
- [ ] Hero CTA buttons stack vertically at 375px
- [ ] Details grid is 2x2 on mobile (not 4 columns)
- [ ] Inclusions image stacks below list on mobile
- [ ] Gallery grid is 2 columns on mobile
- [ ] Testimonials are single column on mobile
- [ ] Form rows stack to single column on mobile
- [ ] All form inputs minimum 48px height on mobile
- [ ] Sticky CTA bar appears after 30% scroll on mobile
- [ ] Sticky CTA button minimum 44px height
- [ ] Side padding minimum 20px on all sections
- [ ] FAQ accordion is tappable (minimum 52px trigger height)

---

## SECTION 4: FORM QA

- [ ] All required fields validated on submit (first_name, last_name, email, preferred_date, guest_count, occasion)
- [ ] Email field validates email format
- [ ] Hidden field experience = "Rose Day Club"
- [ ] Hidden field page_name = "rose-day-club" (populated by JS)
- [ ] Hidden field brand = "SSS" (populated by JS)
- [ ] Hidden field city = "Fort Lauderdale" (populated by JS)
- [ ] Hidden field source_url populated with current URL (verify with DevTools)
- [ ] UTM hidden fields populate when URL contains UTM params
- [ ] UTM hidden fields read from sessionStorage when URL lacks params
- [ ] Form submits to Make.com SSS_LEAD_INTAKE_HOOK webhook
- [ ] Make.com receives test submission
- [ ] Airtable record created: Experience = "Rose Day Club", Status = NEW
- [ ] Auto-reply email received at test address
- [ ] Slack alert fires to #sss-ops-alerts
- [ ] Duplicate submission blocked (same email + date + guests)
- [ ] Form success state shown after submission
- [ ] Form hides after successful submission

---

## SECTION 5: SEO QA

- [ ] Title tag: "Rose Day Club | Private Yacht Day Experience | She Said Sail" (under 60 chars: 56 chars)
- [ ] Meta description: under 155 characters, present
- [ ] OG:title present
- [ ] OG:description present
- [ ] OG:image present (1200x630px — file: rose-day-club-og.jpg must be uploaded)
- [ ] OG:image:alt present and descriptive
- [ ] Twitter card tags present
- [ ] Canonical URL: https://shesaidsail.com/experience/rose-day-club/
- [ ] Schema markup valid (test at schema.org/validator)
- [ ] Page is indexed (not noindex)
- [ ] H1 contains primary keywords

---

## SECTION 6: PERFORMANCE QA

- [ ] Hero image is WebP or compressed JPEG, under 280KB
- [ ] Hero image uses loading="eager" and fetchpriority="high"
- [ ] All below-fold images use loading="lazy"
- [ ] Gallery images are WebP, under 120KB each
- [ ] rose-day-club.js is deferred (add defer attribute in Webflow)
- [ ] rose-day-club.css is linked in page head
- [ ] Page passes Core Web Vitals in PageSpeed Insights (mobile 70+)
- [ ] No console errors on page load

---

## SECTION 7: ACCESSIBILITY QA

- [ ] All images have descriptive alt text (not empty)
- [ ] Form fields have matching label for/id pairs
- [ ] All buttons have visible focus states
- [ ] Accordion triggers have aria-expanded attributes
- [ ] FAQ accordion answer IDs match aria-controls on triggers
- [ ] Sticky CTA has aria-label
- [ ] Color contrast passes 4.5:1 for body text
- [ ] Color contrast passes 3:1 for large headings on overlays
- [ ] Keyboard navigation works through form and accordion

---

## SECTION 8: ANALYTICS QA

- [ ] GTM container loads on page (verify in browser network tab)
- [ ] GA4 pageview fires on load (GA4 DebugView)
- [ ] sss_form_submit event fires on form submit (GTM preview)
- [ ] sss_cta_click event fires on CTA button clicks (GTM preview)
- [ ] UTM params appear in GA4 session source/medium (DebugView)
- [ ] page_name dimension = "rose-day-club" in data layer (GTM preview)

---

## SIGN-OFF

Sections 1-4: All items must pass before launch.
Sections 5-8: Minimum 80% of items must pass before launch.

Complete this QA log and retain in DEPLOYMENT_PACK/pages/rose-day-club/ for reference.

QA Performed By: _______________
Date: _______________
Status: PENDING HUMAN IMPLEMENTATION
