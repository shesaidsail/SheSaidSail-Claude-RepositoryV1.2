# She Said Sail: Request to Book Page Install Guide

Audience: WordPress or Elementor web builder. Some steps (hidden fields) require a developer if you are not comfortable editing MetForm field configuration.
Total estimated time: 60 minutes.

The global CSS and JavaScript from the homepage install guide must be applied before starting this guide. If those two steps are not done, complete Steps 1 and 2 of the homepage-install-guide.md first.

---

## Before You Start

Confirm:
- Global CSS is applied (Appearance > Customize > Additional CSS has the She Said Sail stylesheet)
- Global JS is loaded (Insert Headers and Footers > Scripts in Footer has the script block)
- MetForm is installed and active, and the Request to Book form already exists on the page

---

## Step 1: Verify Global CSS Is Applied (2 minutes, no action if already done)

**Check:** Open /request-to-book/ in your browser. The page should display with the same brand typography and colors as the homepage. If not, complete the CSS step from homepage-install-guide.md before continuing.

No additional page-specific CSS is needed for this page. The global stylesheet covers it.

---

## Step 2: Add Concierge Reassurance Block Above the Form (10 minutes)

**What you are adding:** A short block of copy above the form that introduces the concierge experience and sets expectations for what happens after submission.

**File:** `03_HTML_SNIPPETS/request-to-book/concierge-block.html`

**Step-by-step:**
1. Open /request-to-book/ in the Elementor editor (Pages > find the Request to Book page > Edit with Elementor).
2. Scroll to the form widget in the page.
3. Hover just above the form widget. A blue line and "+" icon appear between the element above the form and the form itself.
4. Click "+" to add a widget.
5. Search for "HTML" and drag it into position above the form.
6. Paste the contents of `concierge-block.html` into the HTML Code field.
7. Click Update.

**What to verify:**
- View the page live.
- The concierge reassurance block appears above the form, not inside it.
- On mobile, the block stacks cleanly above the form without overflow.

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 3: Add Request Form Intro Above Form Widget (5 minutes)

**What you are adding:** A short headline and one sentence of copy directly above the form fields, setting context for what the form does.

**File:** `03_HTML_SNIPPETS/request-to-book/form-intro.html`

**Step-by-step:**
1. In the Elementor editor, hover just above the form widget (but below the concierge block you just added).
2. Add another HTML widget.
3. Paste the contents of `form-intro.html`.
4. Click Update.

**What to verify:**
- The intro text appears between the concierge block and the first form field.
- Text is readable on mobile.

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 4: Add Trust Note Below Form Submit Button (5 minutes)

**What you are adding:** A single line of reassuring copy below the Submit button (e.g., "No payment required. We'll be in touch within 24 hours.").

**File:** `03_HTML_SNIPPETS/request-to-book/trust-note.html`

**Step-by-step:**
1. In the Elementor editor, hover just below the form widget.
2. Add an HTML widget below the form.
3. Paste the contents of `trust-note.html`.
4. Click Update.

**What to verify:**
- The trust note appears below the Submit button.
- It does not appear inside the form (if it appears inside the form, you placed the widget in the wrong position; delete and re-add below the form widget, not inside it).

**Rollback:** Right-click the HTML widget > Delete > Update.

---

## Step 5: Add Hidden Form Fields (15 minutes) -- Requires MetForm Access

This step requires editing the MetForm form in Elementor. If you are not comfortable with MetForm field configuration, involve a developer.

**Reference:** Full instructions and field list are in `05_AIRTABLE_BACKEND/request-form-hidden-fields.md`. Follow that document's Step-by-step MetForm instructions.

**Summary of what to do:**
1. Go to MetForm > Forms in WordPress admin.
2. Find the Request to Book form and click Edit.
3. In the Elementor editor for the form, add 14 Hidden Field widgets (one per hidden field).
4. Set each field's name exactly as specified in `request-form-hidden-fields.md` (e.g., `utm_source`, `utm_medium`, etc.).
5. Leave all default values blank. JavaScript will populate them.
6. Save and publish the form.
7. After saving, go to the live /request-to-book/ page, open DevTools > Elements, search for `type="hidden"`. Confirm all 14 hidden input fields appear in the DOM.

**What to verify:**
- Open /request-to-book/ with test UTM params: `?utm_source=test&utm_medium=cpc&utm_campaign=qa-test&creative_id=TEST-001`
- Open DevTools > Console. Type: `populateHiddenFields()` and press Enter.
- Check the Elements tab. Hidden input fields should now have values: `utm_source` = "test", `utm_medium` = "cpc", etc.

**Rollback:** Open MetForm > Forms > Edit. Delete the 14 hidden field widgets. Save.

---

## Step 6: Set Form Action/Webhook URL (5 minutes, requires Make.com webhook URL)

**Prerequisite:** Make.com must be set up and the M-WEBFORM-REQUEST-CAPTURE webhook URL must be available. If Make.com is not yet set up, skip this step and return to it after completing `06_MAKE_WEBHOOKS/make-webhook-setup.md`.

**Step-by-step:**
1. Open `02_GLOBAL_JS/she-said-sail-global.js` in a text editor.
2. Find the line with the comment `// WIRE THIS to your Make.com webhook`.
3. Replace the empty string with your Make.com webhook URL:
   ```javascript
   var webhookUrl = 'https://hook.eu2.make.com/XXXXXXXXXXXXXX';
   ```
4. Save the file and re-paste it into Insert Headers and Footers > Scripts in Footer (replacing the previous version).
5. Save.

**What to verify:**
- Submit a test form.
- In Make.com, go to the M-WEBFORM-REQUEST-CAPTURE scenario > Run history. A new run should appear with status "Success."
- Check Airtable Requests table for the new record.

**Rollback:** Replace the webhook URL with an empty string in the JS and re-paste. The form will stop submitting to Make.com.

---

## Step 7: Set Up /thank-you/ Redirect on Successful Submission

**Prerequisite:** The /thank-you/ page must exist in WordPress. Go to Pages and confirm a page with the slug `thank-you` exists. If it does not, create one with the title "Thank You" and slug "thank-you", with basic thank you copy, and publish it.

**Configure MetForm redirect:**
1. Go to MetForm > Forms in WordPress admin.
2. Find the Request to Book form and click Edit.
3. In the Elementor editor for the form, click the MetForm widget.
4. In the left panel, look for "Form Actions" or "After Submit" settings.
5. Add or configure the "Redirect" action.
6. Set the redirect URL to: `https://shesaidsail.com/thank-you/`
7. Save.

**What to verify:**
- Submit the test form with valid data.
- Browser should redirect to /thank-you/ within 1-2 seconds of a successful submission.

**Rollback:** Remove the redirect action from the MetForm widget's after-submit settings.

---

## Step 8: Apply request-to-book-meta.html (5 minutes)

**What this does:** Sets the noindex meta tag and OG tags for the /request-to-book/ page.

**Option A: Via Yoast SEO or RankMath (preferred)**
1. Edit the Request to Book page in WordPress.
2. In the Yoast/RankMath box, set:
   - noindex: On (look for "Allow search engines to show this Page in search results" toggle and turn it OFF)
   - SEO Title: Request to Book | She Said Sail
   - Meta Description: Submit your yacht charter inquiry. Luxury women-led celebrations in Miami and Fort Lauderdale. Our team will follow up within 24 hours.
3. Save.

**Option B: Via Insert Headers and Footers**
1. Open `04_SEO_META/request-to-book-meta.html`.
2. Copy the contents.
3. Because Insert Headers and Footers applies globally, use a conditional approach. In WordPress, add the meta tags conditionally using a hook in your child theme's `functions.php`:
   ```php
   add_action('wp_head', function() {
     if (is_page('request-to-book')) {
       echo '<meta name="robots" content="noindex">';
     }
   });
   ```
   Or use Yoast/RankMath as Option A, which handles page-level control more cleanly.

**What to verify:**
- View page source on /request-to-book/: `<meta name="robots" content="noindex">` should be present.
- Confirm Google will not index this page (use Google Search Console's URL Inspection tool after launch).

**Rollback (Option A):** Re-enable indexing in Yoast/RankMath toggle.

---

## Step 9: Verify and QA

After completing all steps, run through this checklist:

- [ ] Concierge reassurance block appears above the form
- [ ] Form intro copy appears between the block and the first field
- [ ] All 10 visible form fields are present
- [ ] Trust note appears below the Submit button
- [ ] 14 hidden fields visible in DevTools Elements tab
- [ ] UTM fields populate correctly from test URL params
- [ ] Form submits without console errors
- [ ] Make.com receives the payload
- [ ] Airtable Requests record created
- [ ] /thank-you/ redirect works after successful submission
- [ ] noindex meta tag confirmed in page source
- [ ] No horizontal scroll on iPhone 14 viewport

For the full form QA checklist, see `09_QA/form-qa-checklist.md`.
