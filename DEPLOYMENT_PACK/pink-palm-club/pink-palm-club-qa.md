# PINK PALM CLUB
# QA CHECKLIST

STATUS: READY FOR HUMAN EXECUTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
PAGE: https://shesaidsail.com/experience/pink-palm-club/
QA OWNER: Will Hunt
SYSTEM REFERENCE: docs/system/master-qa-system.md

---

## PRE-LAUNCH QA CHECKLIST

Complete all items before marking the page as production-ready.
Check each box when verified. Note failures in the comments column.

---

### SECTION 1: VISUAL QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| V-01 | Hero image loads within 2.5 seconds on mobile (throttled 4G) | | | |
| V-02 | Hero image is sharp and correctly cropped on all breakpoints | | | |
| V-03 | Gold eyebrow text visible on navy hero overlay | | | |
| V-04 | All body text readable at 4.5:1 contrast minimum | | | |
| V-05 | No text overflows its container on any breakpoint | | | |
| V-06 | No horizontal scroll at any viewport width | | | |
| V-07 | Section spacing is consistent (cream / white / navy alternating rhythm) | | | |
| V-08 | Stats grid displays correctly on desktop (4 columns) | | | |
| V-09 | Stats grid collapses to 2x2 on tablet/mobile | | | |
| V-10 | Gold divider lines are visible and correctly sized (40px) | | | |
| V-11 | Add-on cards display in 3-column grid on desktop | | | |
| V-12 | Add-on cards stack to single column on mobile | | | |
| V-13 | Social proof quotes display in 3-column grid on desktop | | | |
| V-14 | Social proof stacks to single column on mobile | | | |
| V-15 | Form card has correct border and padding | | | |
| V-16 | Floating CTA is hidden on desktop, visible on mobile after hero scroll | | | |
| V-17 | Reassurance strip shows 3 items horizontally on desktop | | | |
| V-18 | Reassurance strip stacks vertically on mobile | | | |
| V-19 | No placeholder text visible on live page | | | |
| V-20 | All images have visible alt attributes | | | |

---

### SECTION 2: TYPOGRAPHY QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| T-01 | Only one H1 on the entire page | | | |
| T-02 | H1 is the hero headline | | | |
| T-03 | H2 used for all major section headings | | | |
| T-04 | H3 used for add-on card names and sub-elements | | | |
| T-05 | No heading levels skipped (no H2 to H4) | | | |
| T-06 | Eyebrow labels are span elements, not headings | | | |
| T-07 | Body text is minimum 16px on mobile | | | |
| T-08 | Form input font size is 16px (no iOS zoom triggered) | | | |
| T-09 | No em dashes anywhere on the page | | | |
| T-10 | No prohibited words: unforgettable, epic, amazing, luxury lifestyle, elite, VIP | | | |
| T-11 | CTA buttons use declarative language (not "Book Now!" or "Click here") | | | |
| T-12 | Font loads correctly (Georgia renders in all tested browsers) | | | |

---

### SECTION 3: MOBILE QA

Tested on:
- iPhone SE (375px) [ ]
- iPhone 14 Pro (393px) [ ]
- iPad (768px) [ ]
- Android (360px) [ ]

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| M-01 | Hero is minimum 75vh on iPhone SE | | | |
| M-02 | Hero headline readable without zooming | | | |
| M-03 | Primary CTA button is full width on mobile | | | |
| M-04 | All touch targets minimum 48px height | | | |
| M-05 | No two-column layouts on mobile (except intentional 2x2 stats) | | | |
| M-06 | Form fields are full width on mobile | | | |
| M-07 | Dropdown selects are easy to use on mobile | | | |
| M-08 | Floating CTA appears after hero scrolls out of view | | | |
| M-09 | Floating CTA disappears correctly | | | |
| M-10 | Smooth scroll to form works when CTA is tapped | | | |
| M-11 | Form success state visible in viewport without extra scrolling | | | |
| M-12 | No iOS zoom triggered when tapping form inputs | | | |
| M-13 | Section padding is 56px top/bottom on mobile | | | |
| M-14 | Horizontal padding is 20px on mobile | | | |

---

### SECTION 4: FORM QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| F-01 | All required fields: first_name, last_name, email, phone, preferred_date, guest_count, occasion | | | |
| F-02 | Required fields show error if submitted empty | | | |
| F-03 | Error messages are specific and helpful | | | |
| F-04 | Error fields are highlighted visually (red border) | | | |
| F-05 | Hidden field "experience" = "Pink Palm Club" on page load | | | |
| F-06 | Hidden field "yacht" = "Lucky Star" on page load | | | |
| F-07 | Hidden field "city" = "Fort Lauderdale" on page load | | | |
| F-08 | Hidden field "duration" = "4 hours" on page load | | | |
| F-09 | Hidden field "boarding_location" populated on page load | | | |
| F-10 | Hidden field "source_url" = full page URL on page load | | | |
| F-11 | Hidden field "utm_source" populated from URL param if present | | | |
| F-12 | Hidden field "utm_medium" populated from URL param if present | | | |
| F-13 | Hidden field "utm_campaign" populated from URL param if present | | | |
| F-14 | Add-on card selections update "add_ons" hidden field | | | |
| F-15 | Form submits without JS errors in console | | | |
| F-16 | Success state shows after submission | | | |
| F-17 | Airtable record created with correct field values | | | |
| F-18 | Airtable record Status = "NEW" | | | |
| F-19 | Airtable record Brand = "SSS" | | | |
| F-20 | Airtable record Environment = "Production" | | | |
| F-21 | Confirmation email received within 3 minutes | | | |
| F-22 | Slack alert in #sss-ops-alerts | | | |
| F-23 | Duplicate submission does NOT create a second record | | | |
| F-24 | Form note below submit button is visible | | | |

---

### SECTION 5: SEO QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| S-01 | Page title: "Pink Palm Club | Private Yacht Experience | She Said Sail" | | | |
| S-02 | Meta description: 130-160 characters, contains primary keyword | | | |
| S-03 | og:title is set | | | |
| S-04 | og:description is set | | | |
| S-05 | og:image is set to actual image URL (not placeholder) | | | |
| S-06 | og:image dimensions are 1200x630 | | | |
| S-07 | og:image:alt is set | | | |
| S-08 | twitter:card is set | | | |
| S-09 | twitter:image is set | | | |
| S-10 | Canonical URL is set and matches page URL | | | |
| S-11 | JSON-LD Product schema is present and valid (test at schema.org validator) | | | |
| S-12 | JSON-LD LocalBusiness schema is present | | | |
| S-13 | Hero image alt text is descriptive (not filename) | | | |
| S-14 | Details section image alt text is descriptive | | | |
| S-15 | H1 contains "Pink Palm Club" or related keyword naturally | | | |
| S-16 | No duplicate title or description on this page | | | |
| S-17 | Page is indexed (not noindex) | | | |

---

### SECTION 6: ANALYTICS QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| A-01 | GTM container fires on page load (verify in GTM Preview) | | | |
| A-02 | sss_page_view event fires on load | | | |
| A-03 | sss_form_start fires on first field focus | | | |
| A-04 | sss_cta_click fires on hero CTA click | | | |
| A-05 | sss_cta_click fires on form submit button click | | | |
| A-06 | sss_scroll_depth fires at 25% | | | |
| A-07 | sss_scroll_depth fires at 50% | | | |
| A-08 | sss_scroll_depth fires at 75% | | | |
| A-09 | sss_scroll_depth fires at 100% | | | |
| A-10 | sss_lead_submitted fires on form submit | | | |
| A-11 | sss_lead_submitted_confirmed fires after Webflow success | | | |
| A-12 | GA4 shows events in real-time view | | | |
| A-13 | UTM params from test URL appear in data layer | | | |
| A-14 | Meta Pixel Lead event fires on conversion | | | |
| A-15 | No JS console errors from pink-palm-club.js | | | |

---

### SECTION 7: ACCESSIBILITY QA

| # | Check | Pass | Fail | Notes |
|---|-------|------|------|-------|
| AC-01 | Skip navigation link present and functional | | | |
| AC-02 | All interactive elements keyboard navigable | | | |
| AC-03 | Tab order follows visual page order | | | |
| AC-04 | Focus states visible on all buttons and links | | | |
| AC-05 | Form labels associated with inputs (for/id pairs) | | | |
| AC-06 | Error messages have role="alert" for screen readers | | | |
| AC-07 | Decorative images have aria-hidden="true" | | | |
| AC-08 | Form success state has role="status" | | | |
| AC-09 | Stats section has aria-label | | | |
| AC-10 | Social proof blockquotes use correct cite element | | | |
| AC-11 | Add-on cards have role="checkbox" and aria-checked | | | |
| AC-12 | Color is not the only means of conveying information | | | |

---

### SECTION 8: PERFORMANCE QA

Run on: https://pagespeed.web.dev/ (Mobile view)

| # | Check | Target | Actual | Pass/Fail |
|---|-------|--------|--------|-----------|
| P-01 | LCP (Largest Contentful Paint) | Under 2.5s | | |
| P-02 | FID / INP | Under 100ms | | |
| P-03 | CLS (Cumulative Layout Shift) | Under 0.1 | | |
| P-04 | FCP (First Contentful Paint) | Under 1.8s | | |
| P-05 | Mobile PageSpeed score | 85+ | | |
| P-06 | Hero image served as WebP | Yes | | |
| P-07 | Hero image compressed under 300KB | Yes | | |
| P-08 | No render-blocking scripts in head | Yes | | |
| P-09 | Lazy loading on below-fold images | Yes | | |

---

## QA SIGN-OFF

When all items above are marked Pass:

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA Reviewer | | | |
| Brand Approval | Will Hunt | | |

---

## KNOWN LIMITATIONS (items requiring human action before full 10/10 score)

1. Hero image: Must be provided and compressed to WebP by the design team. Placeholder URL in code.
2. OG image: Must be cropped to 1200x630 and hosted. URL placeholder in metadata snippet.
3. JSON-LD schema: Image URL must be replaced with actual hosted image URL.
4. Social proof: Three placeholder quotes are included. Replace with real guest testimonials before launch.
5. Make webhook URL: Must be updated in Webflow form settings with the live production URL.
6. Pricing: $1,200 starting price must be verified and updated if incorrect.
7. Yacht name "Lucky Star": Must be verified as the correct vessel for this experience.
8. Google Ads conversion tag: CONVERSION_ID and CONVERSION_LABEL placeholders in pink-palm-club.js must be replaced if Google Ads is active.
9. PageSpeed score: Cannot be verified until page is live. Run immediately after launch.
10. Hotjar: Heatmap must be configured in Hotjar dashboard after launch.
