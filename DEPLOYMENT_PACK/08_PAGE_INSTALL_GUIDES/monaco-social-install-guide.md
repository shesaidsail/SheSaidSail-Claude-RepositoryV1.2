# She Said Sail: Monaco Social Page Install Guide

**Version:** 1.0
**Page:** Monaco Social
**URL:** /experience/monaco-social/
**Applies to:** Web builder deploying the Monaco Social experience page optimization

---

## 1. PREREQUISITES

Before beginning this install, confirm the following are already in place from the homepage install guide:

- [ ] Global CSS stylesheet is loaded site-wide (verify in Appearance > Customize > Additional CSS or via Insert Headers and Footers)
- [ ] Global JS file is loaded in the footer site-wide (verify in Insert Headers and Footers > Scripts in Footer)
- [ ] The request-to-book page exists at /request-to-book/
- [ ] The form on /request-to-book/ is confirmed functional and accepting submissions
- [ ] You have WordPress admin access
- [ ] You have Elementor editor access for the Monaco Social page
- [ ] Yoast SEO plugin is installed and active (preferred for SEO step)

If global CSS or JS is not yet applied, stop and complete the homepage install guide first. The snippets on this page depend on the global styles.

---

## 2. INSTALL ORDER

Complete steps in this exact order. Do not skip steps or reorder them.

| Step | Task | Est. Time |
|------|------|-----------|
| 1 | Verify global CSS is already applied | 5 min |
| 2 | Verify global JS is already loaded in footer | 5 min |
| 3 | Apply SEO meta tags via Yoast SEO | 10 min |
| 4 | Add hero-support.html snippet below the hero | 15 min |
| 5 | Add experience-description.html below hero-support | 15 min |
| 6 | Add social-proof.html below experience-description | 10 min |
| 7 | Add occasion-fit.html below social-proof | 10 min |
| 8 | Add pre-cta-reassurance.html below occasion-fit | 10 min |
| 9 | Add bottom-cta.html as the last section above the footer | 10 min |
| 10 | Verify the selected_experience hidden field passes "monaco-social" via URL param | 5 min |
| 11 | Run mobile QA at 375px and 390px viewports | 10 min |

**Total estimated time: approximately 1 hour 45 minutes**

---

## 3. STEP-BY-STEP INSTRUCTIONS

### Step 1: Verify Global CSS

1. In WordPress admin, go to Appearance > Customize > Additional CSS or to Insert Headers and Footers > Scripts in Header.
2. Confirm the She Said Sail global CSS block is present. It should contain the root variables for `--sss-navy`, `--sss-gold`, `--sss-cream`, and the button styles.
3. If it is present: no action needed, proceed to Step 2.
4. If it is not present: stop. Apply global CSS from the homepage install guide before continuing.

### Step 2: Verify Global JS

1. In WordPress admin, go to Insert Headers and Footers > Scripts in Footer.
2. Confirm the She Said Sail global JS block is present. It should contain the `populateHiddenFields()` function and the `initCTATracking()` function.
3. If it is present: no action needed, proceed to Step 3.
4. If it is not present: stop. Apply global JS from the homepage install guide before continuing.

### Step 3: Apply SEO Meta Tags

**Preferred method (Yoast SEO):**

1. Open the Monaco Social page in WordPress editor.
2. Scroll to the Yoast SEO meta box below the editor.
3. In the SEO tab, set the meta description to:
   `Monaco Social is She Said Sail's champagne-led yacht experience in Miami. Built for birthdays and elevated groups. Up to 15 guests. Starting from $10,000.`
4. In the Social tab, set the Facebook/Open Graph image to the Monaco Social hero image. Set the OG title and description to match the values in monaco-social-meta.html.
5. The canonical URL is set automatically by Yoast based on the page URL. Confirm it reads `https://shesaidsail.com/experience/monaco-social/`.

**Manual method (Insert Headers and Footers):**

1. Go to Insert Headers and Footers > Scripts in Header.
2. Paste the full contents of `DEPLOYMENT_PACK/04_SEO_META/monaco-social-meta.html`.
3. Note: the canonical and meta description tags must only appear once site-wide per page. If Yoast is also active, use only one method to avoid duplicate tags.

**JSON-LD:**

1. The JSON-LD block from monaco-social-meta.html can be added via Insert Headers and Footers > Scripts in Header, or via a Custom HTML widget in Elementor placed in a hidden section at the bottom of the page.
2. Confirm the JSON-LD renders in page source before proceeding.

### Step 4: Add hero-support.html

1. Open the Monaco Social page in Elementor.
2. Locate the hero section (the section containing the H1 "Monaco Social" and the hero CTA button).
3. Add a new section immediately below the hero section.
4. Inside that new section, add a Custom HTML widget.
5. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/hero-support.html` into the widget.
6. Save and preview. The hero-support block should show the Monaco Social tagline, 3 quick-fact pills, and 4 occasion pills on a cream background.

### Step 5: Add experience-description.html

1. Add a new section immediately below the hero-support section.
2. Add a Custom HTML widget inside the new section.
3. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/experience-description.html`.
4. Save and preview. The section should show left-column descriptive copy and a right-column "What is included" list.

### Step 6: Add social-proof.html

1. Add a new section immediately below the experience-description section.
2. Add a Custom HTML widget inside the new section.
3. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/social-proof.html`.
4. Save and preview. The section should display 2 testimonials with attribution on a navy background.

### Step 7: Add occasion-fit.html

1. Add a new section immediately below the social-proof section.
2. Add a Custom HTML widget inside the new section.
3. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/occasion-fit.html`.
4. Save and preview. The section should show occasion positioning copy on the left and a list of occasion types on the right.

### Step 8: Add pre-cta-reassurance.html

1. Add a new section immediately below the occasion-fit section.
2. Add a Custom HTML widget inside the new section.
3. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/pre-cta-reassurance.html`.
4. Save and preview. The section should show a 3-step process block.

### Step 9: Add bottom-cta.html

1. Identify the footer section of the Monaco Social page.
2. Add a new section immediately above the footer.
3. Add a Custom HTML widget inside the new section.
4. Paste the full contents of `DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/bottom-cta.html`.
5. Save and preview. The section should show a navy background, a heading, subtext, a gold CTA button, and a "no commitment" reassurance note below the button.

### Step 10: Verify selected_experience URL Param

1. Open a browser and navigate to: `https://shesaidsail.com/request-to-book/?selected_experience=monaco-social`
2. Inspect the form. Confirm the hidden field named `selected_experience` is pre-populated with the value `monaco-social`.
3. Submit a test entry and confirm the value appears in the form submission data.
4. If the value does not populate, escalate to the developer per the Backend Setup section below.

### Step 11: Mobile QA

1. In Chrome DevTools, set the viewport to 375px (iPhone SE).
2. Review all 6 snippet sections for layout, text overflow, and CTA size.
3. Repeat at 390px (iPhone 14).
4. Check that both CTA buttons are full-width at mobile viewports.
5. Check that occasion pills wrap correctly and do not overflow horizontally.

---

## 4. ELEMENTOR COPY EDITS

Make these changes directly inside the existing Elementor widgets, separate from the HTML snippet installs.

**Page Hero H1:**
- Confirm the H1 reads exactly: `Monaco Social`
- It should not read "Monaco Social Charter," "Monaco Social Experience," or any generic variant.
- H1 must appear exactly once on the page.

**Hero Subheadline:**
- Set the subheadline text below the H1 to: `Champagne-led Riviera energy for birthdays and elevated groups.`
- This should be styled in italic using the site's default italic subheadline class.

**Hero CTA Button:**
- Button text: `Request Monaco Social`
- Button link: `/request-to-book/?selected_experience=monaco-social`
- Button style: gold fill, navy text (matching the global `.sss-btn-primary` class)
- Do not use "Book Now," "Submit," "Inquire," or any other CTA text.

**Existing Experience Description Copy (if present in Elementor):**
- If the Monaco Social page already has descriptive copy in an Elementor text widget, you have two options:
  - Option A (preferred): Hide or delete the Elementor text widget and use the experience-description.html snippet instead.
  - Option B: Update the Elementor text widget copy to match the content in experience-description.html exactly.
- Do not leave duplicate descriptive copy blocks on the page.

---

## 5. SEO APPLICATION

### Yoast SEO Fields (Preferred)

| Field | Value |
|-------|-------|
| SEO Title | Monaco Social \| Private Yacht Experience Miami \| She Said Sail |
| Meta Description | Monaco Social is She Said Sail's champagne-led yacht experience in Miami. Built for birthdays and elevated groups. Up to 15 guests. Starting from $10,000. |
| Canonical URL | Auto-set by Yoast to https://shesaidsail.com/experience/monaco-social/ |
| OG Title | Monaco Social \| Private Yacht Experience Miami \| She Said Sail |
| OG Description | Monaco Social is She Said Sail's champagne-led yacht experience in Miami. Built for birthdays and elevated groups. Up to 15 guests. Starting from $10,000. |
| OG Image | Upload or select the Monaco Social hero image (1200x630px) |

### Manual Application (Insert Headers and Footers)

If Yoast SEO is not available:

1. Go to Insert Headers and Footers > Scripts in Header.
2. Paste the contents of `DEPLOYMENT_PACK/04_SEO_META/monaco-social-meta.html`.
3. Update the og:image URL with the real uploaded image URL (replace the placeholder).
4. Save.

### JSON-LD Structured Data

The JSON-LD Service schema in monaco-social-meta.html should be added to the page. Options:

- Add it inside the Scripts in Header block alongside the other meta tags.
- Add it via a Custom HTML Elementor widget in a hidden section at the bottom of the page (set section visibility to hidden in Elementor settings).

Confirm the schema renders in page source at `<script type="application/ld+json">`.

---

## 6. BACKEND SETUP

### selected_experience Hidden Field

The hero CTA and the bottom CTA both use the URL:
`/request-to-book/?selected_experience=monaco-social`

The global JS `populateHiddenFields()` function handles UTM parameters automatically. The `selected_experience` field is a query parameter (not a UTM param), so the form must be configured separately to read it.

**Action required for developer:**

1. Open the request-to-book form in its form plugin settings (MetForm, WPForms, Gravity Forms, or equivalent).
2. Confirm a hidden field exists with the name `selected_experience`.
3. Confirm the hidden field's default value is set to pull from the URL parameter `?selected_experience=`.
   - In MetForm: set the hidden field's default value source to "URL Parameter" and set the parameter name to `selected_experience`.
   - In Gravity Forms: use the dynamic population feature with the parameter name `selected_experience`.
   - In WPForms: use the dynamic field population with the parameter key `selected_experience`.
4. Test by visiting `/request-to-book/?selected_experience=monaco-social` and inspecting the hidden field value in the DOM.
5. Submit a test entry and confirm the value `monaco-social` appears in the submission record.

---

## 7. GTM SETUP

### Monaco Social Page View Event

The global JS fires `view_experiences_page` when a user visits `/experiences/`. For the Monaco Social page, add a separate page view event.

**In GTM:**

1. Create a new tag: Custom HTML Tag.
2. Name it: `SSS - View Monaco Social Page`.
3. Paste the following code:

```html
<script>
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'view_monaco_social',
    page_location: window.location.href
  });
</script>
```

4. Set the trigger: Page View, trigger fires on Some Page Views.
5. Condition: Page Path contains `/experience/monaco-social/`
6. Save and publish.

### CTA Click Tracking

The global JS `initCTATracking()` function fires `click_request_to_book` when any link with an href containing `/request-to-book/` is clicked. Because both the hero CTA and the bottom CTA on this page link to `/request-to-book/?selected_experience=monaco-social`, they are already covered by the global JS.

**Confirm the following in GTM preview mode:**

- Navigate to `/experience/monaco-social/` and click the hero CTA button.
- Confirm `click_request_to_book` fires in the GTM preview panel.
- Navigate to the bottom of the page and click the bottom CTA button.
- Confirm `click_request_to_book` fires again.

No additional GTM tags are required for CTA tracking on this page if the global JS is correctly loaded.

---

## 8. QA CHECKLIST REFERENCE

After completing the install, run the full QA checklist found at:

`DEPLOYMENT_PACK/09_QA/monaco-social-qa-checklist.md`

Do not sign off on the install until all items in the checklist are marked pass.

For the general experience page framework, also review:

`DEPLOYMENT_PACK/09_QA/experience-pages-qa-addendum.md`

---

## 9. ROLLBACK INSTRUCTIONS

If any step causes a visible error or layout break on the live page, follow these steps to roll back:

1. **Rollback a single snippet section:** In Elementor, locate the Custom HTML widget containing the broken snippet. Delete that section only. The rest of the page remains intact.

2. **Rollback all snippet sections:** In Elementor, delete each Custom HTML widget section added during this install (hero-support, experience-description, social-proof, occasion-fit, pre-cta-reassurance, bottom-cta). The page returns to its pre-install state.

3. **Rollback SEO meta tags (Yoast method):** In Yoast SEO, clear the meta description, OG title, OG description, and OG image fields. Yoast will fall back to WordPress defaults.

4. **Rollback SEO meta tags (manual method):** In Insert Headers and Footers, remove the Monaco Social meta block from Scripts in Header. Do not remove the global CSS or global JS blocks.

5. **Rollback GTM tag:** In GTM, set the `SSS - View Monaco Social Page` tag to paused. Publish the container. The `view_monaco_social` event stops firing. No other tracking is affected.

After any rollback, document what was rolled back and notify Will before reattempting the install.
