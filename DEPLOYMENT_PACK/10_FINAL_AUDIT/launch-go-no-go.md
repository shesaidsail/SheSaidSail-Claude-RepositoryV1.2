# She Said Sail: Launch Go/No-Go Checklist

This checklist determines whether the site is ready to receive traffic. Complete in order. All BLOCKERS must be YES before any traffic is directed to the site.

Last reviewed: _____________________ Reviewer: _____________________

---

## MUST BE DONE BEFORE ANY TRAFFIC (Blockers)

All 10 items must be YES. If any item is NO, do not proceed.

| # | Check | YES | NO | Notes |
|---|---|---|---|---|
| 1 | CSS applied to WordPress? Global stylesheet (`01_GLOBAL_CSS/she-said-sail-global.css`) is in WordPress Appearance > Customize > Additional CSS and all three pages render correctly. | | | |
| 2 | JavaScript loaded in footer? `02_GLOBAL_JS/she-said-sail-global.js` is loaded via Insert Headers and Footers (or equivalent) in the footer, with no console errors on page load. | | | |
| 3 | Social proof strip visible on homepage? The review strip appears below the hero section on the homepage without layout issues on desktop. | | | |
| 4 | Email capture section visible on homepage? The email input section is visible near the bottom of the homepage and the input field is functional. | | | |
| 5 | Request to Book form loads and validates? The form on /request-to-book/ loads, all visible fields are present, and client-side validation fires when required fields are empty. | | | |
| 6 | Thank you page exists at /thank-you/? Navigate to `https://shesaidsail.com/thank-you/` and confirm the page loads without a 404 error. | | | |
| 7 | Phone number is a real tap-to-call link? Right-click the phone number on the site and confirm the href is `tel:+1XXXXXXXXXX` with the actual number. Test on mobile that it opens the dialer. | | | |
| 8 | No broken links on homepage, request page, or experiences pages? Click every navigation link, CTA button, and card link. Confirm no 404 errors and no links pointing to `#` or placeholder URLs. | | | |
| 9 | SEO meta description present on homepage? View page source (Ctrl+U) and search for `meta name="description"`. Confirm a real description is present, not a placeholder or empty string. | | | |
| 10 | /request-to-book/ is set to noindex? View page source on /request-to-book/ and search for `noindex`. Confirm `<meta name="robots" content="noindex">` is present. | | | |

**Status: All 10 blockers YES?** YES / NO

If YES: the site can receive organic traffic. Proceed to Section 2 before enabling paid ads.

If NO: identify which items are NO and complete them before any traffic.

---

## SHOULD BE DONE BEFORE PAID ADS (High Priority)

These items are not hard blockers for the site going live to organic visitors, but all 10 must be YES before any money is spent on paid advertising.

| # | Check | YES | NO | Notes |
|---|---|---|---|---|
| 1 | Make.com webhook receiving form data? Submit a test form submission and confirm M-WEBFORM-REQUEST-CAPTURE scenario runs successfully in Make.com run history. | | | |
| 2 | Airtable records being created? After the test submission, confirm a new record exists in the Requests table, a new record in UTMs, and a new or updated record in Contacts. | | | |
| 3 | Confirmation email sending? The submitter receives a confirmation email within 5 minutes of form submission, with the correct name, occasion, and group size in the body. | | | |
| 4 | Slack alert sending? After form submission, a formatted alert appears in the #she-said-sail-leads Slack channel within 2 minutes. | | | |
| 5 | GTM container published? Go to GTM, confirm the container status shows "Published" (not Draft or Preview). The published version has a version number and name. | | | |
| 6 | GA4 receiving events? Open GA4 Admin > DebugView. Load the site on another browser tab. Confirm `page_view` and `view_homepage` events appear in DebugView within 30 seconds. | | | |
| 7 | Meta Pixel verified? Install Meta Pixel Helper Chrome extension. Load the homepage. Confirm the extension shows the Pixel ID as Active with PageView event. | | | |
| 8 | TikTok Pixel verified? Install TikTok Pixel Helper Chrome extension. Load the homepage. Confirm the extension shows the Pixel ID as Active with PageView event. | | | |
| 9 | PageSpeed mobile score >= 60? Run PageSpeed Insights (pagespeed.web.dev) on the homepage URL. Mobile score must be 60 or above. Note the actual score here. | | | Score: _____ |
| 10 | All QA checklists signed off? All four QA checklists (master, mobile, form, backend, tracking) are complete with signatures. | | | |

**Status: All 10 high-priority items YES?** YES / NO

If YES: paid advertising campaigns may be enabled.

If NO: identify blockers and complete them. Do not spend money on ads until form-to-Airtable flow is confirmed working.

---

## Final Sign-Off

Section 1 (Blockers) complete: _____________________ Date: _____________________

Section 2 (High Priority) complete: _____________________ Date: _____________________

Founder approval to enable paid traffic: _____________________ Date: _____________________
