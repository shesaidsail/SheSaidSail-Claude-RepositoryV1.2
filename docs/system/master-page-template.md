# She Said Sail: Master Page Template
Version: 1.0

This is the step-by-step workflow for every future page optimization on the She Said Sail website. A developer or AI system can follow this template to bring any page up to the same standard as the homepage, Request to Book, and Experiences pages. Complete every step in order.

---

## 1. PURPOSE

This template exists because optimization quality must be consistent regardless of who is doing the work. Without a shared standard, individual pages drift from one another in tone, structure, trust signal placement, and technical quality.

Every page touched during the luxury-conversion-overhaul feature branch, and every page added or optimized afterward, follows this exact workflow.

---

## 2. PRE-WORK CHECKLIST

Before beginning any page optimization, confirm the following:

- [ ] Page URL confirmed and accessible
- [ ] Page HTML exported (via view source or from WordPress theme editor)
- [ ] Elementor page ID confirmed (found in WordPress URL when editing the page)
- [ ] Page purpose confirmed: conversion, information, trust, or SEO
- [ ] Current quality score estimated (rough 1 to 10 across the 10 audit dimensions)
- [ ] Target audience for this specific page confirmed (e.g., bachelorette group leader vs. general visitor)
- [ ] Any known technical issues noted before starting

Do not begin optimization work until every item above is confirmed. Starting without page purpose confirmed leads to structural decisions that conflict with the master page structure system.

---

## 3. STEP 1: AUDIT THE PAGE

Score each dimension on a 1 to 10 scale. Record scores before making any changes. The pre-optimization score is the baseline.

**10 Audit Dimensions:**

**1. Emotional positioning**
Does the hero lead with feeling or function? Does the visitor recognize her own occasion in the first visible screen?

**2. Social proof**
Is there any? Is it specific and attributed? Does it appear within the first 3 sections on a conversion page?

**3. CTA clarity**
Is there exactly one primary CTA per page? Is the destination /request-to-book/? Are secondary CTAs visually subordinate?

**4. Trust signals**
Does the page include: phone number, real names (concierge language), specific pricing, testimonials with attribution?

**5. Mobile UX**
Does the page work on a 375px viewport without horizontal scroll? Are tap targets at least 44px? Is form text 16px minimum (prevents iOS zoom)?

**6. Copy quality**
Is all copy on-brand? Does any copy use prohibited words? Any em dashes present? Any passive voice in CTAs? Any "world-class" or superlative language?

**7. SEO**
Is a meta description present and under 160 characters? Are Open Graph title, description, and image set? Does H1 appear exactly once? Do images have descriptive alt text? Is the page indexable (no noindex tag)?

**8. Performance**
Are any unused scripts loading? Is the page loading unnecessary plugins? Is imagery appropriately compressed?

**9. Backend readiness**
If the page contains a form: is the form wired to the Make.com webhook? Are Airtable records being created on submission? Are hidden tracking fields present?

**10. Analytics readiness**
Are GTM dataLayer events firing for: page view, CTA click, form start (first field interaction), and form submit?

---

## 4. STEP 2: SCORE THE PAGE

Use the scoring system from master-audit-scorecard.md. Record the individual score for each of the 10 dimensions listed above.

**Overall score = average of all 10 dimension scores.**

| Score Range | Optimization Level Required |
|-------------|----------------------------|
| Below 7.0 | Full optimization required. Complete all steps. |
| 7.0 to 8.5 | Targeted optimization. Address specific failing dimensions. |
| Above 8.5 | Minor polish only. Do not restructure working pages. |

Record the pre-optimization overall score in the audit document before proceeding.

---

## 5. STEP 3: IDENTIFY ISSUES

After scoring, list every identified issue in a structured format.

**For each issue, record:**

- Issue description (one sentence)
- Dimension affected (from the 10 above)
- Severity: Critical / High / Medium / Low
- Fix type: CSS / JS / HTML snippet / Elementor edit / Backend / Analytics / Copy

**Severity definitions:**

- Critical: blocking conversion or causing user-facing errors
- High: directly reduces conversion probability or trust
- Medium: reduces quality or brand consistency but does not block conversion
- Low: polish, refinement, or preference-level improvement

Prioritize Critical and High issues. Do not skip them in favor of easier Low issues.

---

## 6. STEP 4: IMPROVE LUXURY POSITIONING

Check the page against master-design-system.md and master-copy-system.md.

**Fix the following if present:**

- Hero overlay opacity above 0.40: reduce to reveal the photography
- Hero headline that leads with the product rather than the feeling: rewrite per Section 3 of master-copy-system.md
- Any prohibited words from the master-copy-system.md prohibited phrases list
- Section labels using "package," "service," "rental," or other transactional language
- Any headlines using superlatives (best, most, premier, unparalleled)
- Typography deviating from the master design system (wrong font, wrong weight, wrong size)
- Color usage deviating from the brand palette

Luxury positioning is the foundation. If this step is not done well, no other optimization will compensate.

---

## 7. STEP 5: IMPROVE TRUST

Trust is built through specificity, concierge language, and human signals. Add or verify the following:

- Social proof section present and placed correctly per master-page-structure.md Section 4
- Testimonials are attributed: first name, last initial, occasion type, experience name
- Concierge language is present somewhere on the page: "a real person," "within 24 hours," "personally reviewed"
- Price anchor appears on any page where pricing is relevant
- Real contact information is visible: phone number linked, email accessible
- No vague social proof ("our guests love us," "hundreds of happy clients")

Reference DEPLOYMENT_PACK/03_HTML_SNIPPETS/ for reusable trust components that can be dropped into Elementor HTML widgets.

---

## 8. STEP 6: IMPROVE MOBILE UX

Check against master-mobile-ux.md (to be created as a companion document if not yet present).

**Fix the following if present:**

- Typography too small on mobile (minimum 16px for body text, minimum 14px for labels)
- Form input font size below 16px (causes iOS to zoom into the field on tap)
- Tap targets smaller than 44px height (buttons, links, navigation items)
- Cards not collapsing to single column below 767px
- Horizontal scroll at 375px viewport width
- CTA appearing above the copy that motivates it
- Hero height too tall on mobile (use 92vh, never 100vh, to leave space for the browser chrome)
- Images not loading at appropriate mobile resolution

Test at three breakpoints: 375px (iPhone SE), 768px (iPad portrait), and 1280px (standard laptop). Document any issues found at each breakpoint.

---

## 9. STEP 7: IMPROVE CTA HIERARCHY

Review the page for CTA conflicts. A confused CTA hierarchy is one of the most common conversion killers.

**Audit:**

- Count every CTA on the page (buttons, text links that lead to actions, form submits)
- Identify the primary CTA and its destination
- Identify any CTAs with equal or competing visual weight

**Fix:**

- Remove or visually subordinate any CTAs competing with the primary
- Unify button styling: primary CTA is always the filled/prominent button; secondary is always outlined or text
- Ensure the primary CTA destination is /request-to-book/
- Ensure the experiences page secondary CTA on the homepage points to /experiences/
- On the request to book page: the form submit is the only CTA. No other buttons.

---

## 10. STEP 8: IMPROVE BACKEND READINESS

This step applies to any page containing a form.

**Checklist:**

- [ ] Hidden tracking fields are present per DEPLOYMENT_PACK/05_AIRTABLE_BACKEND/request-form-hidden-fields.md
- [ ] Make.com webhook URL is wired to the form submit action
- [ ] Airtable records are being created on a test submission (verify in the Airtable base)
- [ ] UTM parameters are being captured in hidden fields
- [ ] Source, medium, and campaign values are populated correctly

If any item is missing, complete it before marking this page as staging-ready. A page with a broken or untracked form is not deployment-ready regardless of visual quality.

---

## 11. STEP 9: IMPROVE ANALYTICS READINESS

GTM dataLayer events must be present and firing correctly for every standard user interaction.

**Required events for every page:**

- `view_[pagename]`: fires on page load (e.g., `view_homepage`, `view_experiences`)
- `cta_click`: fires when the primary CTA button is clicked, with label parameter

**Required events for pages with forms:**

- `form_start`: fires on first interaction with any form field
- `form_submit`: fires on successful form submission (after validation, before redirect)

Reference: DEPLOYMENT_PACK/02_GLOBAL_JS/she-said-sail-global.js. Standard page events are already coded for homepage, experiences, and request-to-book. For new pages, add the `view_[pagename]` event push to the page-specific script block.

Verify all events using GTM Preview mode before marking the page staging-ready.

---

## 12. STEP 10: IMPROVE SEO

SEO is not the primary optimization goal for She Said Sail, but every indexable page should have correct metadata.

**Check and fix:**

- Meta description: present, under 160 characters, written in brand voice (not keyword-stuffed)
- Open Graph title: matches the page H1 or a close variant
- Open Graph description: matches the meta description or a short variant
- Open Graph image: set to a high-quality hero image at 1200 x 630px
- H1: appears exactly once per page. Never used for decorative headings.
- Images: all significant images have descriptive alt text in plain language
- No noindex tag on any page that should be indexed
- Canonical URL is set correctly (no trailing slash issues)

Reference DEPLOYMENT_PACK/04_SEO_META/ for page-specific meta templates.

---

## 13. STEP 11: GENERATE SNIPPETS

When new HTML sections are created during optimization, save them as reusable snippets.

**Naming convention:**

`[page-name]-[section-name].html`

Examples: `homepage-social-proof-strip.html` / `request-to-book-concierge-block.html`

**File location:**

`DEPLOYMENT_PACK/03_HTML_SNIPPETS/[page-name]/`

**Snippet file standards:**

- Placement comment at the top of each file: `<!-- Placement: After experience cards section, before value prop -->`
- All CSS classes follow the `.sss-*` naming convention (e.g., `.sss-proof-strip`, `.sss-concierge-block`)
- Scroll reveal: add `.sss-reveal` class to animated elements. Use `.sss-delay-1`, `.sss-delay-2`, `.sss-delay-3` for staggered reveals.
- No inline styles. All styling goes in the snippet's associated CSS block or in the master stylesheet.

---

## 14. STEP 12: GENERATE DOCS

Create or update documentation files for the page being optimized.

**Always create or update:**

- `docs/audits/[page-name]-audit-[month-year].md`: the pre-optimization audit with scores and issues list
- Any page-specific tracking specifications not already covered by the global analytics doc

**If the page has a new or modified form:**

- Update `DEPLOYMENT_PACK/05_AIRTABLE_BACKEND/` with field mappings for any new form fields
- Update `DEPLOYMENT_PACK/06_MAKE_WEBHOOKS/` with the webhook configuration
- Document the expected Airtable record structure

Documentation is not optional. An undocumented system creates dependency on individuals who remember how it was built. Document as you go.

---

## 15. STEP 13: GENERATE QA CHECKLIST

Before any page moves to staging, it needs a page-specific QA checklist.

**Create:**

`DEPLOYMENT_PACK/09_QA/[page-name]-qa-checklist.md`

Use master-qa-system.md as the base. Customize for page-specific elements:

- For pages with forms: add form submission test, Airtable record verification, redirect confirmation
- For pages with video: add autoplay behavior test, mobile video fallback test
- For pages with custom JS: add console error check, event firing verification

The QA checklist is what the developer (or AI agent) signs off on before requesting staging merge approval.

---

## 16. STEP 14: GENERATE FINAL AUDIT

After optimization is complete, create a final audit document.

**Create:**

`docs/audits/[page-name]-final-audit.md`

**Final audit includes:**

- Pre-optimization scores for all 10 dimensions
- Post-optimization scores for all 10 dimensions
- List of changes made
- List of issues that remain (with justification for deferral if applicable)
- Recommended next actions (what would move this page from its current score to a 9.0 or above)

Be honest in final audits. A page at 7.5 is not an 8.5 because the work was hard. Score against the standard, not against the effort.

---

## 17. STEP 15: COMMIT AND PUSH

Follow the commit and branch rules in master-deployment-standard.md exactly.

**Commit rules summary:**

- Commit in logical groups. One logical change per commit.
- Never commit CSS and backend specs in the same commit.
- Use present tense, imperative mood: "add social proof strip to request to book page"
- No em dashes in commit messages.
- Maximum 72 characters in the summary line.
- Push to the current feature branch. Never directly to staging or main.

After pushing, follow the staging workflow in master-deployment-standard.md Section 5. Do not self-approve a staging merge. Await Will's written approval before merging to main.
