# She Said Sail: Homepage Install Guide

Audience: WordPress or Elementor web builder with WordPress admin access.
Total estimated time: 75 minutes.

Work through the steps in order. Each step builds on the previous one. Do not skip ahead.

---

## Before You Start

Confirm the following:
- You have WordPress admin access (can reach wp-admin)
- Elementor and Elementor Pro are active (check Plugins list)
- "Insert Headers and Footers" plugin is installed and active
- The homepage is currently published and accessible at shesaidsail.com

---

## Step 1: Apply Global CSS (5 minutes)

**Where:** WordPress Admin > Appearance > Customize > Additional CSS

**Step-by-step:**
1. Log in to WordPress admin.
2. In the left sidebar, click Appearance > Customize.
3. In the Customizer panel that opens on the left, click "Additional CSS" at the bottom.
4. A text area appears. Paste the entire contents of `01_GLOBAL_CSS/she-said-sail-global.css` into this text area.
5. Click the blue Publish button at the top of the Customizer panel.
6. Close the Customizer.

**What to verify after:**
- Open the homepage in a new browser tab.
- The brand colors (deep navy, warm cream, coral gold accents) should be visible.
- Typography should reflect the brand fonts.
- No elements should appear broken or unstyled.
- Open DevTools (F12) > Console. No CSS-related errors should appear.

**Rollback:** Return to Appearance > Customize > Additional CSS. Delete all the CSS you pasted. Click Publish. The site returns to its previous styling within seconds.

---

## Step 2: Load Global JavaScript (5 minutes)

**Plugin required:** Insert Headers and Footers (by WPBeginner). If not installed: Plugins > Add New > search "Insert Headers and Footers" > Install > Activate.

**Step-by-step:**
1. In WordPress admin, go to Settings > Insert Headers and Footers.
2. Find the "Scripts in Footer" text area (the third box, not Header or Body).
3. Add the following script tag, with the contents of `02_GLOBAL_JS/she-said-sail-global.js` inside it:

```html
<script>
/* She Said Sail Global JS */
/* Paste the full contents of 02_GLOBAL_JS/she-said-sail-global.js here */
</script>
```

4. Click Save.

**Alternative (if the JS file is hosted):** If the JS file is hosted on a CDN or server:
```html
<script src="https://shesaidsail.com/wp-content/uploads/she-said-sail-global.js" defer></script>
```

**What the script tag looks like when correct:**
- It is inside the "Scripts in Footer" section only, not Headers or Body.
- It is wrapped in `<script>` and `</script>` tags.
- The JavaScript content is between those tags.

**What to verify after:**
- Open the homepage in a browser.
- Open DevTools > Console.
- Type `typeof populateHiddenFields` and press Enter. It should return `"function"`.
- Type `typeof window.dataLayer` and press Enter. It should return `"object"`.
- No JavaScript errors should appear in the console on page load.

**Rollback:** Go to Settings > Insert Headers and Footers > Scripts in Footer. Delete the script block. Click Save.

---

## Step 3: Apply SEO Meta Tags (10 minutes)

**Option A: Via Yoast SEO or RankMath (preferred)**

1. Go to WordPress admin > Pages. Find the Homepage.
2. Click Edit.
3. Scroll to the Yoast SEO or RankMath box at the bottom of the editor.
4. Click Edit Snippet (Yoast) or the snippet preview area (RankMath).
5. Set:
   - SEO Title: She Said Sail | Luxury Yacht Charters, Miami and Fort Lauderdale
   - Meta Description: Luxury yacht charters for women-led celebrations. Bachelorette parties, birthdays, and girls trips in Miami and Fort Lauderdale. Starting from $10,000.
6. Save the page.

**Option B: Via Insert Headers and Footers (if no SEO plugin)**

1. Open `04_SEO_META/homepage-meta.html`.
2. Copy the entire contents.
3. Go to Settings > Insert Headers and Footers.
4. Paste into the "Scripts in Header" text area.
5. Click Save.

**What to verify after:**
- Open the homepage. Right-click > View Page Source (Ctrl+U).
- Search (Ctrl+F) for `meta name="description"`.
- Confirm the description text is the She Said Sail description, not a generic WordPress default.
- Also check for `og:title`, `og:description`, and `og:image` tags.

**Rollback (Option A):** Delete the SEO title and meta description in Yoast/RankMath and save.
**Rollback (Option B):** Go to Insert Headers and Footers > Header and delete the meta tags. Save.

---

## Step 4: Add Social Proof Strip (15 minutes)

**What you are adding:** A horizontal strip of review quotes with reviewer names, appearing below the hero section on the homepage.

**File:** `03_HTML_SNIPPETS/homepage/social-proof-strip.html`

**Exact placement in Elementor:**
1. Open the homepage in the Elementor editor (Pages > Homepage > Edit with Elementor).
2. Scroll down to find the hero section (the top section with the photography and main CTA).
3. Click the area just below the hero section to reveal the section boundaries.
4. Hover between the hero section and the next section. A blue line and a "+" icon appear.
5. Click the "+" to add a new section below the hero.
6. In the "Choose your structure" dialog, select a single full-width column.
7. In the new empty section, click the "+" inside the column to add a widget.
8. Search for "HTML" and drag the "HTML" widget into the section.
9. Click the widget. In the Content tab on the left, paste the entire contents of `social-proof-strip.html` into the HTML Code field.
10. Click Update (bottom left).

**What to verify after:**
- View the homepage live (not the editor).
- The social proof strip appears below the hero and above the next section.
- Review text is readable on desktop.
- The strip is visible without scrolling much past the hero (it should be one of the first things a visitor sees after the hero).
- Switch DevTools to mobile view. Confirm the strip stacks and remains readable.

**Rollback:** In the Elementor editor, right-click the HTML widget > Delete. Click Update.

---

## Step 5: Add Occasion Pills to Hero (10 minutes)

**What you are adding:** A row of small pill-shaped labels (Bachelorette, Birthday, Girls Trip) within or just below the hero section headline area.

**File:** `03_HTML_SNIPPETS/homepage/occasion-pills.html`

**Exact placement in Elementor:**
1. In the Elementor editor, scroll to the hero section.
2. Click inside the hero section to make it editable.
3. Find the text widget containing the hero headline.
4. You will add an HTML widget directly below the headline widget, inside the same column.
5. Hover between the headline widget and the next widget (e.g., the subheadline or CTA). A blue line and "+" appear.
6. Click "+" to add a widget.
7. Search for "HTML" and drag it into position.
8. Paste the contents of `occasion-pills.html` into the HTML Code field.
9. Click Update.

**What to verify after:**
- View the homepage live.
- Three pills are visible in or just below the hero headline area.
- Pills display as rounded labels with legible text.
- On mobile, pills wrap to a second line cleanly without overflowing the viewport.

**Rollback:** Right-click the HTML widget > Delete. Click Update.

---

## Step 6: Add Email Capture Section (15 minutes)

**What you are adding:** An email capture section near the bottom of the homepage, with a headline, short copy, email input, and Subscribe button.

**File:** `03_HTML_SNIPPETS/homepage/email-capture.html`

**Exact placement in Elementor:**
1. In the Elementor editor, scroll to near the bottom of the homepage.
2. Find the footer section or the last content section above the footer.
3. Hover just above the footer section. A blue line and "+" appear between the last content section and the footer.
4. Click "+" to add a new section.
5. Select a single full-width column.
6. Add an HTML widget to the new section.
7. Paste the contents of `email-capture.html`.
8. Click Update.

**Before updating:** Open `email-capture.html` and find the comment `// WIRE THIS to your Make.com email-capture webhook`. The email capture form's submission handler needs the Make.com webhook URL. If Make.com is not yet set up, the form will not submit successfully, but you can still add the section visually. Wire the URL after Make.com is configured.

**What to verify after:**
- View the homepage live.
- The email capture section is visible before the footer.
- The email input field is clickable.
- The Subscribe button is visible.
- On mobile, the section stacks cleanly (input above button, or side by side depending on viewport).
- Enter a test email and click Subscribe. If Make.com is wired, confirm the payload arrives. If not wired yet, note that as a pending task.

**Rollback:** Right-click the HTML widget > Delete. Click Update.

---

## Step 7: Elementor Copy Edits (15 minutes)

These are direct text changes in Elementor, not HTML widget additions.

**Change 1: "The Packages" to "The Experiences"**
1. In the Elementor editor, scroll to the section that says "The Packages."
2. Click the heading widget.
3. In the Content tab on the left, change the text to "The Experiences."
4. Click Update.

**Change 2: Monaco Social card description**
1. Find the Monaco Social experience card.
2. Click the text widget inside the card.
3. Update the description to match the copy in `03_HTML_SNIPPETS/experiences/experience-card-content.html` > Monaco Social section.
4. Click Update.

**Change 3: Pink Palm Club card description**
1. Find the Pink Palm Club experience card.
2. Click the text widget inside the card.
3. Update the description to match the copy in `experience-card-content.html` > Pink Palm Club section.
4. Click Update.

**Change 4: Bottom CTA punctuation**
1. Find the bottom CTA section (typically a large headline above the final CTA button).
2. Click the heading widget.
3. Remove any incorrect punctuation (trailing period after a call-to-action headline, or incorrect dash usage).
4. Click Update.

**What to verify after:**
- View each change on the live homepage.
- Confirm "The Experiences" appears, not "The Packages."
- Confirm card descriptions match the intended copy.
- No typos or formatting issues.

**Rollback:** Repeat the same steps and restore the original text. Use Elementor's revision history if you need to revert: Elementor editor > bottom left > the clock icon > revision history.

---

## Step 8: Verify and QA

After completing all steps:

**Desktop checklist:**
- [ ] CSS rendering correctly (brand colors, typography)
- [ ] Social proof strip visible below hero
- [ ] Occasion pills visible in/below hero
- [ ] Email capture section visible before footer
- [ ] "The Experiences" label visible on the experiences cards section
- [ ] All CTA buttons link to /request-to-book/
- [ ] No console errors

**Mobile checklist (use DevTools > Toggle Device Toolbar > iPhone 14 390px):**
- [ ] No horizontal scroll
- [ ] All sections stack cleanly
- [ ] CTA buttons are full-width
- [ ] Text is readable without zooming
- [ ] Social proof strip visible and readable

For the full mobile checklist, see `09_QA/mobile-qa-checklist.md`.
