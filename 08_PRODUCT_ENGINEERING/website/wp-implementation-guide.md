# She Said Sail: WordPress Implementation Guide
**Version:** 2.0
**Branch:** feature/luxury-conversion-overhaul

This is the step-by-step guide for applying every change in this overhaul to the live WordPress/Elementor site.

---

## PREREQUISITES

- WordPress admin access
- Elementor editor access on the homepage
- "Insert Headers and Footers" plugin installed (free)

---

## STEP 1: Apply Custom CSS

**Time required:** 5 minutes

1. Log in to WordPress Admin
2. Go to **Appearance > Customize**
3. Click **Additional CSS** in the left panel
4. Open `08_PRODUCT_ENGINEERING/website/custom-css/luxury-overhaul.css`
5. Copy the entire file
6. Paste into the Additional CSS field (replace any existing content or append at the bottom)
7. Click **Publish**

What this fixes immediately:
- Hero overlay reduced from 50% to 36% (photography breathes)
- Hero headline typography elevated
- Experience card hover effects and image zoom
- Section label styling refined
- CTA button states unified
- Footer redesigned
- Mobile spacing improved across all sections

---

## STEP 2: Apply JavaScript Enhancements

**Time required:** 5 minutes

1. Log in to WordPress Admin
2. Go to **Settings > Insert Headers and Footers** (install plugin if not present)
3. In the **"Scripts in Footer"** section, add:

```html
<script defer>
/* paste the entire contents of custom-js/luxury-enhancements.js here */
</script>
```

4. Save

What this fixes immediately:
- Phone number becomes a tap-to-call link
- Location "Miami, FL" links to Google Maps
- All empty logo/image alt tags filled
- Scroll reveal animation applied to new snippets
- Occasion badges injected into experience cards
- Mobile nav closes on link tap

---

## STEP 3: Add SEO Meta Tags

**Time required:** 10 minutes

Option A (recommended, via Yoast SEO or RankMath):
1. Open the homepage in WordPress editor
2. Scroll to the Yoast/RankMath panel at the bottom
3. Set the Meta Description to: *Private yacht experiences in Miami designed for women-led celebrations. Bachelorettes, birthdays, and the days worth doing properly. Starting from $10,000.*
4. Set the Social (Facebook/OG) Title and Description as noted in `seo/meta-tags.html`
5. Upload the hero photography as the social share image (1200x630 crop)
6. Save

Option B (manual via Insert Headers and Footers):
1. Open `seo/meta-tags.html`
2. Copy the content
3. In **Settings > Insert Headers and Footers**, paste into "Scripts in Header"
4. Save

---

## STEP 4: Add Social Proof Strip

**Time required:** 15 minutes

The social proof strip goes between the Experience Cards section and the "Not Just a Charter" section.

1. Open WordPress homepage in Elementor editor
2. Hover between the two sections mentioned above until you see the blue `+` add section button
3. Click `+`, choose **Container (Full Width)**
4. Set the container padding to 0 on all sides
5. Inside the new container, click `+` and add an **HTML widget**
6. In the HTML widget editor, paste the entire contents of `html-snippets/social-proof-strip.html`
7. Click **Update** and preview

**Verify:**
- Three quote cards appear on a navy background
- Text is readable
- On mobile, cards stack vertically (single column)

---

## STEP 5: Add Occasion Pills to Hero

**Time required:** 10 minutes

The occasion pills go in the hero, between the subheadline text and the CTA button container.

1. Open WordPress homepage in Elementor editor
2. Click inside the hero section
3. Find the inner container that holds: Heading 1, Heading 2 (italic), Subtext, CTA button
4. Click between the subtext widget and the CTA container to find the gap
5. Add a new **HTML widget** in that position
6. Paste the contents of `html-snippets/hero-occasion-pills.html`
7. Click **Update** and preview

**Verify:**
- Pills appear as small outlined text: Bachelorette, Birthday, Girls Trip, Celebration
- They sit above the CTA button
- They are visible against the hero image/overlay

---

## STEP 6: Add Email Capture Section

**Time required:** 15 minutes

The email capture goes between the slideshow section and the bottom navy CTA banner.

1. Open WordPress homepage in Elementor editor
2. Find the full-width image slideshow section (the one with `--spacer-size: 57vh`)
3. Below that section, before the gold/navy "Step Into the Experience" banner, add a new Container
4. Set the container to full width, no padding
5. Add an **HTML widget** inside it
6. Paste the contents of `html-snippets/email-capture-section.html`
7. Click **Update** and preview

**Wire up the form:**
The form does nothing by default until you connect it to an email service.
Options:
- **Klaviyo**: Create a form, use their embed or List API endpoint
- **Mailchimp**: Use their signup form action URL
- **Make (Zapier-style)**: Create a webhook scenario, update the `fetch()` URL in `luxury-enhancements.js`

**Verify (before wiring):**
- Email capture section appears with correct styling
- Form displays inline on desktop, stacked on mobile
- Visual design matches the rest of the page

---

## STEP 7: Copy Updates in Elementor

**Time required:** 20 minutes

These require direct editing in Elementor:

### 7a. Change "The Packages" to "The Experiences"
1. Click the small text label reading "The Packages" in Elementor
2. Change to: **The Experiences**
3. Update

### 7b. Fix experience card descriptions
- Monaco Social: Change to "Champagne-led Riviera energy for birthdays and elevated groups."
- Pink Palm Club: Change to "Playful Miami energy built for groups who want movement, music, and long afternoons on the water."

### 7c. Update hero CTA destination (optional, recommended)
- Change hero button destination from `/experiences/` to `/request-to-book/`
- Change button text from "Plan Your Experience" to "Request to Book"

### 7d. Fix bottom CTA banner copy punctuation
- Current: "...how it should feel relaxed, seamless, and entirely yours."
- Corrected: "...how it should feel: relaxed, seamless, and entirely yours."

---

## STEP 8: Verify and QA

After applying all changes, check:

**Desktop:**
- [ ] Hero photography is warmer/lighter (overlay reduced)
- [ ] Hero headline reads as one unified block
- [ ] Occasion pills visible above CTA
- [ ] CTA button gold, hover state correct
- [ ] Social proof strip visible between sections
- [ ] Experience cards: hover lift, image zoom on hover
- [ ] Email capture section appears and form works
- [ ] Footer redesigned: softer, more refined
- [ ] Phone number is a real `tel:` link (inspect in browser)
- [ ] Logo alt text shows "She Said Sail" (inspect in browser)

**Mobile (iPhone):**
- [ ] Hero is full height, text readable
- [ ] Occasion pills wrap cleanly
- [ ] Experience cards stack (single column)
- [ ] Social proof quotes stack (single column)
- [ ] Email form stacks vertically
- [ ] CTA button full width
- [ ] Nav closes after tapping a link
- [ ] Footer stacks cleanly

**SEO:**
- [ ] View source shows meta description
- [ ] Open Graph tags present
- [ ] Schema.org JSON-LD present
- [ ] No duplicate H1 warning in Google Search Console (after re-crawl)

---

## STEP 9: Add GTM DataLayer Events Script

**Time required:** 5 minutes

This script sends conversion events to Google Tag Manager so GA4, Meta Pixel, and TikTok Pixel
can track CTA clicks, form submissions, and experience card interactions.

**Where to load:**
Option A (via GTM, recommended):
1. In Google Tag Manager, create a new Tag
2. Tag type: Custom HTML
3. Paste the entire contents of `custom-js/gtm-datalayer-events.js` wrapped in `<script>` tags
4. Trigger: All Pages
5. Save and publish

Option B (via Insert Headers and Footers):
1. Go to Settings > Insert Headers and Footers
2. In "Scripts in Footer", add a second `<script defer>` block
3. Paste the entire contents of `custom-js/gtm-datalayer-events.js`
4. Save

**Important:** Do NOT load this script before `luxury-enhancements.js`. Load order matters.
luxury-enhancements.js should be first in the footer, gtm-datalayer-events.js second.

---

## STEP 10: Add Hidden Tracking Fields to the Booking Form

**Time required:** 15 minutes (requires developer)

The booking form at /request-to-book/ needs hidden input fields to capture UTM attribution.
These fields are populated by JavaScript before the form submits.

If using MetForm:
1. Open the MetForm editor for the request-to-book form
2. Add a Hidden Field widget for each of the following field names:
   - utm_source
   - utm_medium
   - utm_campaign
   - utm_content
   - utm_term
   - creative_id
   - landing_page
   - source_url
   - referrer_url
   - first_seen_at
   - submission_page
   - brand (default value: "shesaidsail")
   - service_category (default value: "yacht-charter")
3. Save the form
4. Verify: submit a test form with UTMs in the URL, check the Make.com scenario payload to confirm fields are populated

See `docs/backend/form-tracking-spec.md` for full field specifications and the JavaScript that populates them.

---

## STEP 11: Wire Forms to Make.com

**Time required:** 30 minutes (requires developer)

After creating Make.com scenarios per `docs/backend/make-webhook-spec.md`:

**For the booking form:**
1. Open `custom-js/luxury-enhancements.js` in the Insert Headers and Footers editor
2. Find the comment that says "Wire this fetch() to your Make.com webhook before going live"
3. Replace the `setTimeout` placeholder with the real `fetch()` call:
```javascript
fetch('https://hook.us1.make.com/YOUR_REQUEST_WEBHOOK_ID', {
  method:  'POST',
  headers: { 'Content-Type': 'application/json' },
  body:    JSON.stringify(payload)
}).then(function () {
  showEmailSuccess(form);
}).catch(function () {
  showEmailSuccess(form);
});
```
4. Replace YOUR_REQUEST_WEBHOOK_ID with the actual Make.com webhook ID
5. Save

**For the email capture form:**
1. In the same file, find the email capture section
2. Replace the placeholder fetch() similarly, using the email capture webhook ID from Make.com
3. Save and test

**Testing:**
1. Submit the booking form with test data and UTMs in the URL: `?utm_source=test&utm_medium=test&utm_campaign=form-test`
2. Check Airtable: new Request record should appear with all UTM fields populated
3. Check email inbox: confirmation email should arrive within 2 minutes
4. Check Slack: #new-leads should show the alert

---

## STEP 12: Rollback Instructions

If any change causes a problem after going live, here is how to undo each one:

**Rollback CSS (2 minutes):**
1. Go to WordPress > Appearance > Customize > Additional CSS
2. Delete the luxury-overhaul.css content (or restore previous CSS if you saved it)
3. Click Publish

**Rollback JavaScript (2 minutes):**
1. Go to Settings > Insert Headers and Footers
2. Delete the script block(s) from Scripts in Footer
3. Save

**Rollback an HTML snippet (5 minutes each):**
1. Open Elementor on the homepage
2. Find the HTML widget for the section you want to remove
3. Right-click the widget, select Delete
4. Update/Publish

**Rollback SEO tags (2 minutes):**
1. Go to Settings > Insert Headers and Footers
2. Delete the meta tags from Scripts in Header (if applied there)
3. OR in Yoast/RankMath: clear the fields you filled

**No git commands needed for WordPress rollback.** WordPress changes are independent of git.
Git rollback (`git revert HEAD`) is only needed if you committed database or config files.

---

## PRIORITY ORDER IF TIME IS LIMITED

Do these first for the highest conversion impact:

1. Custom CSS (Step 1): immediate visual upgrade, 5 minutes
2. Social proof strip (Step 4): highest trust impact, 15 minutes
3. SEO meta tags (Step 3): fixes immediate technical gaps, 10 minutes
4. JavaScript enhancements (Step 2): fixes trust bugs, 5 minutes
5. Occasion pills (Step 5): adds audience targeting, 10 minutes
6. Email capture (Step 6): starts nurture list, 15 minutes
7. GTM events (Step 9): enables analytics tracking, 5 minutes
8. Hidden form fields + Make.com wiring (Steps 10 and 11): closes data loop, 45 minutes
