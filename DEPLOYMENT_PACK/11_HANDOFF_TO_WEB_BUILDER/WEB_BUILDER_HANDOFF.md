# She Said Sail: Web Builder Handoff

---

## WHAT THIS IS

You are applying a design and content upgrade to the She Said Sail website, a luxury yacht charter company based in Miami and Fort Lauderdale. Everything you need is in this deployment pack. Follow this document in order and refer to the linked guides for step-by-step instructions on each task.

---

## BEFORE YOU START

Confirm all three of the following before doing anything else:

1. WordPress admin access confirmed: you can log in to wp-admin and see the dashboard.
2. Elementor editor access confirmed: you can open a page and see the Elementor visual editor, not just the block editor.
3. "Insert Headers and Footers" plugin installed: go to Plugins in WordPress admin and confirm "Insert Headers and Footers" by WPBeginner is active. If not installed, add it from Plugins > Add New before proceeding.

If any of these are not confirmed, contact Will before starting.

---

## INSTALL IN THIS ORDER

Work through the tasks in the numbered order below. Each task builds on the previous one. Do not skip ahead.

**1. Apply the CSS file. Time: 5 minutes.**

File: `01_GLOBAL_CSS/she-said-sail-global.css`

Go to WordPress Admin > Appearance > Customize > Additional CSS. Paste the entire contents of the CSS file into the text area. Click Publish.

See: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Step 1 for exact instructions.

**2. Add the JavaScript file. Time: 5 minutes.**

File: `02_GLOBAL_JS/she-said-sail-global.js`

Go to Settings > Insert Headers and Footers. In the "Scripts in Footer" text area, add a `<script>` block and paste the full contents of the JS file inside it. Click Save.

See: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Step 2 for exact instructions and what the script tag should look like.

**3. Add SEO meta tags for the homepage. Time: 10 minutes.**

File: `04_SEO_META/homepage-meta.html`

Use Yoast SEO or RankMath (preferred) to set the meta description and title on the homepage. If no SEO plugin is installed, use Insert Headers and Footers > Scripts in Header and paste the meta tag file contents.

See: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Step 3.

**4. Add the 3 homepage HTML snippets via Elementor HTML widgets. Time: 30 minutes.**

Files:
- `03_HTML_SNIPPETS/homepage/social-proof-strip.html` (goes below the hero section)
- `03_HTML_SNIPPETS/homepage/occasion-pills.html` (goes inside the hero section, below the headline)
- `03_HTML_SNIPPETS/homepage/email-capture.html` (goes above the footer)

For each snippet: open the homepage in the Elementor editor, add an HTML widget in the correct position, paste the snippet contents, click Update.

See: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Steps 4, 5, and 6 for exact placement instructions.

**5. Make the Elementor copy edits on the homepage. Time: 15 minutes.**

Change "The Packages" to "The Experiences." Update the Monaco Social and Pink Palm Club card descriptions. Fix the bottom CTA punctuation.

See: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Step 7.

**6. Add the Request to Book page snippets. Time: 20 minutes.**

Files:
- `03_HTML_SNIPPETS/request-to-book/concierge-block.html` (above the form)
- `03_HTML_SNIPPETS/request-to-book/form-intro.html` (between concierge block and form)
- `03_HTML_SNIPPETS/request-to-book/trust-note.html` (below the form submit button)

Also: add the 14 hidden MetForm fields (requires MetForm access) and set the /thank-you/ redirect.

See: `08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md` for all steps.

**7. Add the Experiences page snippets. Time: 30 minutes.**

Files:
- `03_HTML_SNIPPETS/experiences/hero-support-copy.html` (below hero headline)
- `03_HTML_SNIPPETS/experiences/experiences-social-proof.html` (below experience cards)
- `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html` (above the footer)

Also: update the 4 experience card descriptions using `03_HTML_SNIPPETS/experiences/experience-card-content.html`.

See: `08_PAGE_INSTALL_GUIDES/experiences-install-guide.md` for all steps.

**8. Confirm GTM is ready to publish. Time: 5 minutes.**

The dataLayer events are already inside the global JS file you loaded in Step 2. GTM just needs to be published to receive them. Open Google Tag Manager (tagmanager.google.com), select the She Said Sail container (GTM-WWTT27Z3), and click Publish. Give the version a name like "v1 - She Said Sail Initial Launch."

Do not create a new GTM container. Do not change the container ID.

---

## AFTER EACH PAGE, SEND WILL:

After completing the homepage, request page, and experiences page, send Will:

1. A screenshot of the page on desktop (full-page, not just the top)
2. A screenshot of the page on mobile (use Chrome DevTools > Toggle Device Toolbar > iPhone 14, 390px)
3. Confirmation that you submitted a test form on /request-to-book/ (screenshot of the thank-you page is ideal)

---

## DO NOT TOUCH THESE

Do not change any of the following without explicit instruction from Will:

- The existing hero photography on any page
- The existing experience names: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club
- The existing Elementor template structure: only add HTML widgets inside existing sections, do not restructure or delete existing sections
- The "Not Just a Charter" section copy: it is already correct
- The GTM container ID (GTM-WWTT27Z3): do not create a new container or add a second GTM script
- The GA4 property (GT-WV3X86GZ): do not create a new GA4 property or change the measurement ID
- The Tidio chat widget code: it is already installed and working
- Any existing page slugs or URLs

---

## ASK WILL BEFORE:

- Adding any new pages to WordPress
- Changing any prices on the site (starting from $10,000 is the stated anchor)
- Deleting any existing Elementor sections (adding and removing your own HTML widgets is fine; deleting pre-existing sections is not)
- Connecting any third-party service not mentioned in this deployment pack (new plugins, new integrations, new accounts)
- Changing any brand colors or fonts
- Changing any URLs, page slugs, or WordPress permalink settings

When in doubt, ask. It is faster to ask than to fix something that should not have been changed.

---

## CONNECT AIRTABLE

Do not set up Airtable yourself unless Will has confirmed the base is created and shared the Base ID with you.

Once Will confirms the Airtable base is ready:
- The schema is in `05_AIRTABLE_BACKEND/airtable-table-schema.md`
- The field mapping is in `05_AIRTABLE_BACKEND/airtable-field-map.md`
- Enter the Base ID and Table IDs into Make.com per the instructions in `06_MAKE_WEBHOOKS/make-webhook-setup.md`

---

## CONNECT MAKE.COM

Do not activate Make.com scenarios until:
1. The hidden fields are confirmed present in the MetForm form (check DevTools > Elements for 14 `type="hidden"` inputs)
2. Will confirms the Airtable base is built and the API key is available

When both are confirmed:
- Webhook URLs from Make.com go into the global JS file at the location marked with the comment `// WIRE THIS to your Make.com webhook`
- The full setup process is in `06_MAKE_WEBHOOKS/make-webhook-setup.md`
- Test with the payloads in `06_MAKE_WEBHOOKS/test-payloads.md` before marking complete

---

## CONNECT GTM

GTM is already installed at GTM-WWTT27Z3. The dataLayer events are in the global JS file.

After applying the JS file (Step 2 above), your only GTM task is:

1. Open tagmanager.google.com
2. Select the GTM-WWTT27Z3 container
3. Click Publish (top right)
4. Name the version "v1 - She Said Sail Initial Launch"
5. Click Publish to confirm

Do not just Preview. Preview mode does not go live. You must Publish.

After publishing, verify using GTM's built-in verification: the container badge should show the current published version number.

---

## IF SOMETHING BREAKS

**CSS rollback (takes under 1 minute):**
Go to WordPress Appearance > Customize > Additional CSS. Delete all the She Said Sail CSS content. Click Publish. The site returns to its previous appearance.

**JS rollback (takes under 1 minute):**
Go to Settings > Insert Headers and Footers > Scripts in Footer. Delete the entire `<script>` block containing the She Said Sail JS. Click Save. The scripts stop loading immediately.

**Elementor rollback (takes under 2 minutes per element):**
In the Elementor editor, right-click the HTML widget you added and click Delete. Click Update. The element is removed.

Note: Elementor also saves revision history. Click the clock icon at the bottom left of the Elementor editor to see previous saved states. You can restore a previous version of the page from there if needed.

These rollback actions are independent. Rolling back CSS does not affect JS. Rolling back an Elementor element does not affect CSS or JS. You can undo each piece separately.

---

## QUESTIONS

**Technical questions about the code:** Check the relevant docs file first. Every snippet has a corresponding guide:
- Homepage snippets: `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md`
- Request page snippets: `08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md`
- Experiences snippets: `08_PAGE_INSTALL_GUIDES/experiences-install-guide.md`
- Airtable: `05_AIRTABLE_BACKEND/`
- Make.com: `06_MAKE_WEBHOOKS/`
- GTM and analytics: `07_GTM_ANALYTICS/`

**Questions about brand, copy, design decisions, or anything you are unsure about:** Ask Will directly before making any changes.
