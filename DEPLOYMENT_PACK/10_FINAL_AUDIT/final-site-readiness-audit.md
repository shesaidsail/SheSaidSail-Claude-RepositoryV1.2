# She Said Sail: Final Site Readiness Audit

Date: May 2026
Prepared by: Claude Code
Audited property: shesaidsail.com
Stack: WordPress 6.9.4, Elementor 4.0.3, Elementor Pro 3.35.1, Hello Elementor theme
GTM: GTM-WWTT27Z3 | GA4: GT-WV3X86GZ
Backend: Airtable + Make.com (specced, not yet built)

---

## Audit Summary

This audit reflects the current state of the deployment pack and frontend work completed. Scores are honest. The site is in strong shape on the frontend and brand presentation layer. The primary gap is backend integration: the form currently cannot route data anywhere until Airtable is built and Make.com is wired.

---

## Dimension Scores

### Homepage Frontend: 9.4 / 10

**What is done:**
- Photography is warm and on-brand. Venue and lifestyle images convey the luxury charter experience clearly.
- Social proof strip added below the hero section with real-format reviews.
- All CTAs unified to consistent copy and styling across the page.
- Occasion pills (Bachelorette, Birthday, Girls Trip) added to the hero to speak directly to the target audience.
- Email capture section added at the bottom of the page.
- "The Packages" section renamed to "The Experiences."
- Monaco Social and Pink Palm Club card descriptions updated to reflect the editorial voice.
- Bottom CTA punctuation corrected.

**Why not 10:**
- Page performance has not been fully optimized. Images are not confirmed as compressed or converted to WebP format. PageSpeed Insights has not been run post-deployment. Until performance is measured and confirmed above 60 on mobile, a perfect score is not warranted.

---

### Request to Book Page: 8.5 / 10

**What is done:**
- Form exists and is functional for user interaction (visible fields, validation on required fields).
- Concierge reassurance block added above the form.
- Request form intro copy added above the form widget.
- Trust note added below the submit button.
- Hidden field specification is complete and ready for implementation.
- noindex meta tag and OG tags are specced and ready to apply.

**Why not higher:**
- Airtable and Make.com are not yet wired. Form submissions currently go nowhere. This is the most critical gap before the site can drive any business value.
- The thank-you page redirect has not been confirmed as set up in MetForm.
- Hidden fields have been specced but not yet confirmed as present in the live form DOM.

---

### Experiences Page: 8 / 10

**What is done:**
- All 4 experience card descriptions improved with editorial voice.
- Social proof strip added below the experience cards.
- Bottom CTA section added at the page foot.
- Hero support copy added below the hero heading.
- OG and meta tags specced and ready to apply.

**Why not higher:**
- The filter and search experience on the Experiences page is basic. Visitors who want to find a specific occasion type (e.g., "what works for a girls trip?") have no filtering tool. This is a known v2 item.
- No experience-specific landing pages exist yet. All 4 experiences share one page, which limits SEO and conversion optimization by experience type.

---

### Mobile UX: 9 / 10

**What is done:**
- All sections stack cleanly on 390px, 375px, and 360px viewports (confirmed via DevTools simulation).
- Tap targets meet minimum 44px requirements on all interactive elements.
- No horizontal scroll detected on any of the three pages.
- Hero, cards, social proof, and email capture all render correctly on small viewports.

**Why not 10:**
- Testing has been done via browser DevTools simulation, not on physical hardware. Real-device testing on iPhone and Android is recommended before launch, particularly for the date picker field behavior and keyboard overlay behavior on the Request to Book form.

---

### SEO: 9 / 10

**What is done:**
- Meta description written and implemented for all three pages.
- Open Graph (og:title, og:description, og:image, og:url) tags configured.
- Twitter Card tags configured.
- Schema.org LocalBusiness markup added for the homepage.
- noindex set on /request-to-book/ to keep the form page out of search results.

**Why not 10:**
- H1 tag duplication is not yet resolved in Elementor. The Hello Elementor theme may output an H1 at the theme level and Elementor Pro may output a second H1 in the hero section. This is a known issue that requires a theme setting adjustment or CSS `display:none` on the theme-level H1. Until this is audited and fixed, the SEO score cannot be 10.

---

### Forms: 7.5 / 10

**What is done:**
- Request to Book form exists with all required visible fields.
- Client-side validation is present for required fields and email format.
- Hidden fields are fully specced with field names, sources, and fallbacks.
- populateHiddenFields() JavaScript function is written and ready to deploy.
- MetForm instructions for adding hidden fields are provided.

**Why not higher:**
- Make.com is not yet wired. Form data is not going anywhere post-submission. This is the primary functional gap.
- Hidden fields have not been confirmed as present in the live MetForm instance.
- The confirmation email is specced but not sending.
- The /thank-you/ redirect has not been confirmed as set up.

---

### Airtable Backend: 2 / 10

**What is done:**
- All 7 table schemas are fully specced with field names, types, and notes.
- Views are specced for each table.
- Field mapping from form to Airtable is documented.
- Page-to-Airtable mapping is documented.

**Why not higher:**
- The Airtable base does not yet exist. Nothing has been built. The score reflects documentation completeness only, not implementation.

---

### Make.com Automation: 2 / 10

**What is done:**
- All 8 scenarios are specced with step-by-step module sequences.
- Webhook setup guide is written.
- Test payloads are provided.
- Error handling configuration is documented.

**Why not higher:**
- No Make.com scenarios have been created. Nothing is running. The score reflects documentation completeness only.

---

### Analytics: 3 / 10

**What is done:**
- GTM container GTM-WWTT27Z3 is installed on the site.
- GA4 property GT-WV3X86GZ is installed.
- All 14 custom dataLayer events are coded into the global JavaScript file.
- GA4 events, Meta Pixel tags, and TikTok Pixel tags are fully specced in GTM.

**Why not higher:**
- GTM container has not been published. The events in the JS file fire into the dataLayer, but GTM is not reading them yet.
- GA4 custom events are not verified in GA4 Admin or DebugView.
- Meta Pixel ID is a placeholder. The actual pixel ID has not been entered into the GTM tags.
- TikTok Pixel ID is a placeholder.
- No conversion events are marked in GA4 Admin.

---

### Conversion Readiness: 8 / 10

**What is done:**
- Social proof elements are present and credible.
- Trust signals (concierge note, trust statement below form) are in place.
- Email capture adds a lower-commitment path to capture visitors not ready to book.
- Price anchor ("Starting from $10,000") sets expectations and qualifies visitors.
- Editorial voice is consistent across homepage, experiences, and request page.
- The occasion-specific framing (bachelorette, birthday, girls trip) speaks directly to the target audience.

**Why not higher:**
- The form integration gap is the main risk. If a qualified visitor submits the form right now, the inquiry is lost. No email is sent to the team, no record is created, no follow-up happens. Conversion readiness requires the backend to be operational.

---

## Overall Score: 7.1 / 10

The frontend, brand presentation, copy, and SEO foundation are strong and ready. The remaining work is entirely backend: build the Airtable base, create the Make.com scenarios, wire the webhook URLs, and publish the GTM container. None of those tasks require changes to the design or copy. They are execution steps with clear specifications in this deployment pack.

The site should not receive paid traffic until the form integration is functional and QA complete.

---

## Priority Order for Remaining Work

1. Build Airtable base (all 7 tables, all fields, all views)
2. Create Make.com scenarios (M-WEBFORM-REQUEST-CAPTURE first)
3. Wire webhook URL into WordPress JS file
4. Add hidden fields to MetForm
5. Test form submission end-to-end (form to Airtable to email to Slack)
6. Enter Meta Pixel ID and TikTok Pixel ID into GTM tags
7. Publish GTM container
8. Run full QA checklists
9. Clean up test records
10. Founder sign-off
11. Enable paid traffic
