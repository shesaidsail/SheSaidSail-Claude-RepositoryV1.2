# She Said Sail: Experiences Page Install Guide

Audience: WordPress or Elementor web builder with Elementor editor access.
Total estimated time: 45 minutes.

The global CSS and JavaScript from the homepage install guide must be applied before starting this guide.

---

## Before You Start

Confirm:
- Global CSS is applied (Appearance > Customize > Additional CSS has the She Said Sail stylesheet)
- Global JS is loaded (Insert Headers and Footers > Scripts in Footer has the script block)
- The Experiences page is published and accessible at shesaidsail.com/experiences/
- All 4 experience cards are visible on the page (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club)

---

## Step 1: Verify Global CSS Is Applied (2 minutes, no action if already done)

Open /experiences/ in your browser. The page should display with the brand typography and colors. If not, complete CSS step from homepage-install-guide.md first.

No page-specific CSS is needed for the Experiences page. The global stylesheet covers it.

---

## Step 2: Add Hero Support Copy Below Hero Heading (10 minutes)

**What you are adding:** A short paragraph below the hero section headline that adds editorial context to the page. Something like: "Every charter is designed around your group. Browse our four signature experiences and find the one that fits your celebration."

**File:** `03_HTML_SNIPPETS/experiences/hero-support-copy.html`

**Step-by-step:**
1. Open /experiences/ in the Elementor editor (Pages > Experiences > Edit with Elementor).
2. Scroll to the hero section at the top of the page.
3. Click inside the hero section.
4. Find the hero headline text widget.
5. Hover just below the headline widget (within the same hero section). A blue line and "+" appear.
6. Click "+" to add a widget.
7. Search for "HTML" and drag it into position directly below the headline.
8. Paste the contents of `hero-support-copy.html` into the HTML Code field.
9. Click Update.

**What to verify:**
- View the page live.
- The support copy appears below the hero headline, above the experience cards.
- Text is legible and does not overlap any existing hero elements.
- On mobile, the text wraps cleanly without overflowing.

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 3: Add Experiences Social Proof Strip Below Experience Cards (15 minutes)

**What you are adding:** A review strip below the four experience cards that adds social proof at the point of decision, reinforcing the quality of the charters before the visitor clicks through to request.

**File:** `03_HTML_SNIPPETS/experiences/experiences-social-proof.html`

**Step-by-step:**
1. In the Elementor editor, scroll down past the four experience cards.
2. Find the bottom of the cards section.
3. Hover between the last experience card (or card container) and the next section below it. A blue line and "+" appear.
4. Click "+" to add a new section.
5. Select single full-width column.
6. Add an HTML widget to the new section.
7. Paste the contents of `experiences-social-proof.html`.
8. Click Update.

**What to verify:**
- View the page live.
- The social proof strip appears below all 4 experience cards.
- It appears above the bottom CTA (which you will add in the next step).
- On mobile, the strip stacks cleanly.

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 4: Add Experiences Bottom CTA at Page Bottom (10 minutes)

**What you are adding:** A closing CTA section at the very bottom of the page (above the footer), encouraging visitors who have scrolled through the experiences to take the next step.

**File:** `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html`

**Step-by-step:**
1. In the Elementor editor, scroll to the bottom of the page content area (the last section before the footer).
2. Hover just above the footer element. A blue line and "+" appear between the last content section and the footer.
3. Click "+" to add a new section.
4. Select single full-width column.
5. Add an HTML widget.
6. Paste the contents of `experiences-bottom-cta.html`.
7. Click Update.

**What to verify:**
- View the page live.
- The bottom CTA section appears above the footer.
- The CTA button links to /request-to-book/.
- On mobile, the section is full-width and the button is easy to tap.

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 5: Apply Elementor Copy Edits for Experience Card Descriptions (5 minutes)

These are direct text edits inside the Elementor experience card widgets. Reference the updated card copy in `03_HTML_SNIPPETS/experiences/experience-card-content.html`.

**For each of the 4 experience cards:**

1. Click the text/description widget inside the card.
2. In the left panel, update the description text to match the copy in `experience-card-content.html` for that card.
3. Click Update after each card.

**Cards and their sections in experience-card-content.html:**
- Monaco Social: social, prestige-focused copy
- Golden Hour Escape: romantic, sunset-focused copy
- Rose Day Club: social, dayclub-on-the-water copy
- Pink Palm Club: girls-trip, fun-forward copy

**What to verify:**
- All 4 card descriptions are updated.
- No old placeholder copy remains.
- Card descriptions are readable on mobile (not truncated).

**Rollback:** Use Elementor's revision history (clock icon, bottom left of editor) to revert to a previous saved state.

---

## Step 6: Apply experiences-meta.html (5 minutes)

**What this does:** Sets the OG tags and meta description for the /experiences/ page.

**Option A: Via Yoast SEO or RankMath (preferred)**
1. Edit the Experiences page in WordPress.
2. In the Yoast/RankMath box, set:
   - SEO Title: Our Experiences | She Said Sail Yacht Charters
   - Meta Description: Four signature yacht charter experiences designed for women-led celebrations in Miami and Fort Lauderdale. Bachelorette parties, birthdays, girls trips. Starting from $10,000.
3. Save.

**Option B: Via Insert Headers and Footers**
Conditionally apply the meta tags for the experiences page using a `functions.php` hook or a plugin that supports per-page header injection. Apply the contents of `04_SEO_META/experiences-meta.html` only on `/experiences/`.

**What to verify:**
- View page source on /experiences/.
- `meta name="description"` shows the She Said Sail experiences description.
- `og:title` and `og:description` are present.

**Rollback:** Delete the meta description in Yoast/RankMath or remove the conditional meta tags.

---

## Step 7: Verify and QA

After completing all steps, review the page:

- [ ] Hero support copy visible below the hero headline
- [ ] All 4 experience cards are visible (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club)
- [ ] Experience card descriptions reflect the updated copy from experience-card-content.html
- [ ] Social proof strip appears below the cards
- [ ] Bottom CTA section appears above the footer
- [ ] All CTA buttons on cards and in the bottom CTA section link to /request-to-book/
- [ ] No horizontal scroll on iPhone 14 (390px) viewport
- [ ] Meta description confirmed in page source
- [ ] No console errors

For the full mobile QA checklist, see `09_QA/mobile-qa-checklist.md`.
