# She Said Sail: Final QA Checklist
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

Complete this checklist before merging to staging. Every item must pass.
Mark each item: PASS / FAIL / N/A

---

## SECTION 1: VISUAL (DESKTOP)

| # | Check | Status | Notes |
|---|---|---|---|
| 1.1 | Hero photography is warm and visible (overlay at 36%, not 50%) | | |
| 1.2 | Hero headline renders as one unified editorial block | | |
| 1.3 | Occasion pills (Bachelorette, Birthday, Girls Trip, Celebration) are visible above CTA | | |
| 1.4 | CTA button is gold (#DAB97E), hover state is darker gold | | |
| 1.5 | Social proof strip appears between experience cards and "Not Just a Charter" section | | |
| 1.6 | Three testimonial cards are readable on navy background | | |
| 1.7 | Experience cards: hover lift and image zoom on hover | | |
| 1.8 | Email capture section appears between slideshow and bottom CTA | | |
| 1.9 | Email capture form is inline (side by side on desktop) | | |
| 1.10 | Footer uses softer text hierarchy with gold column headings | | |
| 1.11 | No layout breaks at 1440px, 1280px, 1024px viewport widths | | |

---

## SECTION 2: VISUAL (MOBILE)

| # | Check | Status | Notes |
|---|---|---|---|
| 2.1 | Hero is full viewport height on iPhone (375px, 390px) | | |
| 2.2 | Hero headline is readable, not clipped | | |
| 2.3 | Occasion pills wrap cleanly without overflow | | |
| 2.4 | CTA button is full width on mobile | | |
| 2.5 | Experience cards stack to single column | | |
| 2.6 | Social proof quotes stack to single column | | |
| 2.7 | Email capture form stacks vertically on mobile | | |
| 2.8 | Footer stacks cleanly without horizontal scroll | | |
| 2.9 | No horizontal scroll on any page section | | |
| 2.10 | Tap targets (buttons, nav links) are at minimum 44x44px | | |

---

## SECTION 3: CTA AND NAVIGATION

| # | Check | Status | Notes |
|---|---|---|---|
| 3.1 | Sticky nav "Request to Book" button links to /request-to-book/ | | |
| 3.2 | Hero CTA links to /request-to-book/ (updated from /experiences/) | | |
| 3.3 | Experience card CTAs link to correct experience pages | | |
| 3.4 | "Not Just a Charter" section CTA links to /request-to-book/ | | |
| 3.5 | Bottom banner CTA links to /request-to-book/ | | |
| 3.6 | All internal links open in same tab | | |
| 3.7 | No links with href="#" remain (all placeholders resolved) | | |

---

## SECTION 4: FORMS

| # | Check | Status | Notes |
|---|---|---|---|
| 4.1 | Request to Book form loads without errors at /request-to-book/ | | |
| 4.2 | All visible form fields are present per form-tracking-spec.md | | |
| 4.3 | All hidden UTM fields are populated before submission (inspect element) | | |
| 4.4 | Form validation fires for empty required fields | | |
| 4.5 | Form validation fires for invalid email format | | |
| 4.6 | Form submits successfully with all fields populated | | |
| 4.7 | User sees confirmation message or is redirected to /thank-you/ | | |
| 4.8 | Email capture form validates email format | | |
| 4.9 | Email capture form shows success message on submit | | |
| 4.10 | Form does not reload the page on submit | | |

---

## SECTION 5: AIRTABLE INTEGRATION

| # | Check | Status | Notes |
|---|---|---|---|
| 5.1 | New Request record created in Airtable after form submission | | |
| 5.2 | New Contact record created (or linked to existing) | | |
| 5.3 | UTM record created and linked to Request | | |
| 5.4 | All UTM fields populated correctly from test submission | | |
| 5.5 | landing_page field shows correct full URL | | |
| 5.6 | referrer_url field is populated or blank (not erroring) | | |
| 5.7 | first_seen_at field is populated | | |
| 5.8 | brand = "shesaidsail" in UTM record | | |
| 5.9 | Second submission with same email links to existing Contact (no duplicate) | | |
| 5.10 | Audit Log record created per submission | | |

---

## SECTION 6: MAKE.COM AUTOMATION

| # | Check | Status | Notes |
|---|---|---|---|
| 6.1 | M-WEBFORM-001 scenario is active in Make.com | | |
| 6.2 | Webhook URL from Make.com matches the URL in the form fetch() call | | |
| 6.3 | Test submission triggers scenario execution without error | | |
| 6.4 | Confirmation email received by test address within 2 minutes | | |
| 6.5 | Slack alert appears in #new-leads channel | | |
| 6.6 | Airtable records created correctly (per Section 5) | | |
| 6.7 | M-EMAIL-CAPTURE-001 scenario is active | | |
| 6.8 | Email capture submission creates Contact with email_subscribed = true | | |
| 6.9 | Email capture adds subscriber to Klaviyo/Mailchimp list | | |
| 6.10 | Error handling: failed Airtable write logged to Audit Log | | |

---

## SECTION 7: ANALYTICS

| # | Check | Status | Notes |
|---|---|---|---|
| 7.1 | GTM Preview Mode shows container firing on all pages | | |
| 7.2 | GA4 DebugView shows page_view events | | |
| 7.3 | view_homepage event fires on homepage load | | |
| 7.4 | click_request_to_book event fires when CTA is clicked | | |
| 7.5 | click_experience_card event fires with correct experience_name | | |
| 7.6 | submit_email_capture event fires on email form submit | | |
| 7.7 | submit_booking_form event fires on booking form submit | | |
| 7.8 | click_phone event fires on phone link click | | |
| 7.9 | Meta Pixel base code verified via Meta Pixel Helper extension | | |
| 7.10 | TikTok Pixel base code verified via TikTok Pixel Helper extension | | |
| 7.11 | GTM container is published (not just previewed) | | |

---

## SECTION 8: SEO

| # | Check | Status | Notes |
|---|---|---|---|
| 8.1 | View source: meta description is present and matches spec | | |
| 8.2 | View source: og:title is present | | |
| 8.3 | View source: og:description is present | | |
| 8.4 | View source: og:image is present and URL is valid | | |
| 8.5 | View source: Schema.org JSON-LD is present | | |
| 8.6 | View source: only one canonical URL tag (no duplicates) | | |
| 8.7 | H1 tag appears exactly once in page source | | |
| 8.8 | All images have non-empty alt attributes (use browser DevTools) | | |
| 8.9 | Phone number is a real tel: link (not href="#") | | |
| 8.10 | Sitemap.xml is up to date and submitted to Google Search Console | | |

---

## SECTION 9: PAGE SPEED

| # | Check | Status | Notes |
|---|---|---|---|
| 9.1 | Google PageSpeed Insights mobile score >= 60 | | |
| 9.2 | Google PageSpeed Insights desktop score >= 80 | | |
| 9.3 | LCP (Largest Contentful Paint) <= 2.5s | | |
| 9.4 | TBT (Total Blocking Time) <= 200ms | | |
| 9.5 | CLS (Cumulative Layout Shift) <= 0.1 | | |
| 9.6 | Hero image is WebP format or AVIF | | |
| 9.7 | Hero image has explicit width and height attributes | | |
| 9.8 | MetForm, OWL Carousel, SuperSlides not loading on homepage (see performance-notes.md) | | |
| 9.9 | No render-blocking scripts in the <head> above the fold | | |

---

## SECTION 10: ACCESSIBILITY

| # | Check | Status | Notes |
|---|---|---|---|
| 10.1 | All images have non-empty, descriptive alt text | | |
| 10.2 | All form inputs have associated label elements or aria-label | | |
| 10.3 | Color contrast: body text on white >= 4.5:1 | | |
| 10.4 | Color contrast: gold text on navy >= 3:1 | | |
| 10.5 | Keyboard navigation works through hero CTA, nav, cards, form | | |
| 10.6 | Focus states are visible (not hidden by CSS) | | |
| 10.7 | Occasion pills nav has aria-label="Occasion types" | | |
| 10.8 | Email form has aria-label="Email signup" | | |
| 10.9 | Social proof section has aria-label | | |
| 10.10 | Tidio chat is not the only support contact method (phone also present) | | |

---

## SECTION 11: COPY AND BRAND

| # | Check | Status | Notes |
|---|---|---|---|
| 11.1 | No em dashes anywhere on the page (scan source) | | |
| 11.2 | No prohibited words: amazing, awesome, unforgettable, elite, VIP, exclusive | | |
| 11.3 | Section header reads "The Experiences" (not "The Packages") | | |
| 11.4 | Monaco Social description: "Champagne-led Riviera energy for birthdays and elevated groups." | | |
| 11.5 | Pink Palm Club description: "Playful Miami energy built for groups who want movement, music, and long afternoons on the water." | | |
| 11.6 | Bottom CTA copy includes colon: "how it should feel: relaxed, seamless, and entirely yours." | | |
| 11.7 | Hero headline leads with feeling, not the vessel | | |
| 11.8 | Testimonials are attributed to real guests (or clearly marked as representative) | | |
| 11.9 | All phone numbers and contact details are current and accurate | | |

---

## SECTION 12: CONVERSION

| # | Check | Status | Notes |
|---|---|---|---|
| 12.1 | Social proof strip is visible without scrolling past the fold on most screens | | |
| 12.2 | There is one primary CTA per section (no competing CTAs) | | |
| 12.3 | Email capture section is present and renders correctly | | |
| 12.4 | Occasion pills in hero match target audience (Bachelorette, Birthday, Girls Trip, Celebration) | | |
| 12.5 | Price anchor ($10,000 starting from) is visible on homepage | | |
| 12.6 | Tidio live chat is loading and visible | | |
| 12.7 | Experience cards have hover states that invite interaction | | |
| 12.8 | "Not Just a Charter" section is above the fold on tablet | | |

---

## SIGN-OFF

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| Founder | | | |
| QA | | | |

**DO NOT MERGE TO STAGING until all items in Sections 1-9 pass.**
**DO NOT MERGE TO MAIN until Founder sign-off is recorded above.**
