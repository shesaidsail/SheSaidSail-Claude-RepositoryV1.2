# Golden Hour Escape: QA Checklist

**Page:** /experience/golden-hour-escape/
**Last updated:** 2026-05-18
**Format:** Pass / Fail / N/A for each item. Date and initials when checked.

---

## 1. Desktop Visual (1440px and 1280px)

Test at both 1440px and 1280px viewport widths in Chrome and Safari.

| # | Check | 1440px | 1280px | Notes |
|---|---|---|---|---|
| 1.1 | All 6 sections are present and in correct order | | | Hero Support, Description, Social Proof, Occasion Fit, Reassurance, Bottom CTA |
| 1.2 | Section 1 background is cream (#FAF8F3) | | | |
| 1.3 | Section 2 background is white (#FFFFFF) | | | |
| 1.4 | Section 3 background is navy (#1A2332) | | | |
| 1.5 | Section 4 background is warm cream (#F5F0E8) | | | |
| 1.6 | Section 5 background is white with gold top border | | | |
| 1.7 | Section 6 background is navy (#1A2332) | | | |
| 1.8 | Cormorant Garamond renders for all headings | | | |
| 1.9 | Inter renders for all body and label text | | | |
| 1.10 | Gold color (#DAB97E) appears on pills, dots, numerals, borders, buttons | | | |
| 1.11 | Two-column grid in Section 2 is balanced and aligned | | | |
| 1.12 | Two-column grid in Section 4 is balanced and aligned | | | |
| 1.13 | Two-column grid in Section 5 is balanced and aligned | | | |
| 1.14 | No layout overflow or horizontal scroll at either width | | | |
| 1.15 | Section padding is visually generous (96px top and bottom) | | | |

---

## 2. Mobile Visual (375px and 390px)

Test at both widths. Use Chrome DevTools device simulation and a real iOS device where possible.

| # | Check | 375px | 390px | Notes |
|---|---|---|---|---|
| 2.1 | All 6 sections stack in a single column | | | |
| 2.2 | Section 1 hero text is readable (minimum 20px tagline, 36px H1) | | | |
| 2.3 | Quick facts strip wraps cleanly with no overflow | | | |
| 2.4 | Occasion pills wrap to multiple rows without breaking layout | | | |
| 2.5 | Section 2 left column (editorial) appears above right column (includes list) | | | |
| 2.6 | CTA button in Section 2 is full width on mobile | | | |
| 2.7 | Social proof cards in Section 3 stack vertically | | | |
| 2.8 | Occasion list in Section 4 is fully readable with gold left borders | | | |
| 2.9 | Numbered steps in Section 5 are clear and readable | | | |
| 2.10 | CTA button in Section 6 is full width (max 360px) and centered | | | |
| 2.11 | No horizontal scroll at either mobile width | | | |
| 2.12 | Section padding is 64px top and bottom on mobile | | | |
| 2.13 | Font sizes are readable without pinch-to-zoom | | | |

---

## 3. Content Accuracy

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 3.1 | Experience name is "Golden Hour Escape" (exact, every instance) | | |
| 3.2 | Tagline reads: "An evening charter designed for intimacy, golden light, and the people worth slowing down for." | | |
| 3.3 | Quick fact: Duration is "3 to 4 Hours" | | |
| 3.4 | Quick fact: Guests is "Up to 12" | | |
| 3.5 | Quick fact: Starting From is "$10,000" | | |
| 3.6 | All 4 occasion pills are present: Anniversary, Milestone Birthday, Girls Escape, Intimate Celebration | | |
| 3.7 | Includes list contains exactly 6 items | | |
| 3.8 | Includes list item 1: "Private yacht charter" | | |
| 3.9 | Includes list item 2: "Professional captain and crew" | | |
| 3.10 | Includes list item 3: "Welcome champagne service" | | |
| 3.11 | Includes list item 4: "Curated music and ambiance" | | |
| 3.12 | Includes list item 5: "Sunset timing for golden hour photography" | | |
| 3.13 | Includes list item 6: "Miami skyline access and Biscayne Bay route" | | |
| 3.14 | Both testimonials are present (Sophie M. and Claire R.) | | |
| 3.15 | 3 numbered steps are present (01, 02, 03) | | |
| 3.16 | Occasion Fit section heading: "Who This Experience Is For" | | |
| 3.17 | Reassurance section heading: "How It Works" | | |
| 3.18 | Bottom CTA heading: "Ready to request Golden Hour Escape?" | | |
| 3.19 | Disclaimer text: "No deposit required to inquire. No commitment until you are ready." | | |

---

## 4. CTA

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 4.1 | Section 2 button text: "Request to Book" | | |
| 4.2 | Section 6 button text: "Request Golden Hour Escape" | | |
| 4.3 | Section 2 button URL: /request-to-book/?selected_experience=golden-hour-escape | | |
| 4.4 | Section 6 button URL: /request-to-book/?selected_experience=golden-hour-escape | | |
| 4.5 | Both URLs open /request-to-book/ correctly (200 response, correct page loads) | | |
| 4.6 | URL parameter `selected_experience=golden-hour-escape` is present after clicking both buttons | | |
| 4.7 | Buttons have correct aria-label attributes | | |
| 4.8 | Both buttons change color on hover (gold to deep gold) | | |

---

## 5. SEO

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 5.1 | Meta title: "Golden Hour Escape | She Said Sail" | | |
| 5.2 | Meta description is present | | |
| 5.3 | Meta description is 155 characters or fewer | | Expected: 139 chars |
| 5.4 | og:title is present and correct | | |
| 5.5 | og:description is present | | |
| 5.6 | og:type is "website" | | |
| 5.7 | og:url matches canonical URL | | |
| 5.8 | og:image is present (placeholder or real image) | | |
| 5.9 | og:site_name is "She Said Sail" | | |
| 5.10 | og:locale is "en_US" | | |
| 5.11 | Twitter card type is "summary_large_image" | | |
| 5.12 | Canonical URL: https://shesaidsail.com/experience/golden-hour-escape/ | | |
| 5.13 | JSON-LD is present in the page source | | |
| 5.14 | JSON-LD validates without errors at validator.schema.org | | |
| 5.15 | JSON-LD minPrice is 10000 | | |
| 5.16 | JSON-LD provider address includes Miami and FL | | |

---

## 6. Backend

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 6.1 | Hidden field `selected_experience` is configured in MetForm or WPForms | | |
| 6.2 | Hidden field reads from URL parameter `selected_experience` | | |
| 6.3 | Navigate to /request-to-book/?selected_experience=golden-hour-escape and confirm the hidden field value populates as "golden-hour-escape" | | Inspect form source or use browser dev tools |
| 6.4 | Submit a test form and confirm record appears in Airtable Requests table | | |
| 6.5 | Airtable record shows selected_experience: "golden-hour-escape" | | |
| 6.6 | Airtable record shows brand: "shesaidsail" | | |
| 6.7 | Airtable record shows service_category: "yacht-charter" | | |
| 6.8 | Make.com M-BRAND-ROUTER routes the submission to the She Said Sail flow | | |

---

## 7. Analytics

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 7.1 | Open GTM Preview mode and load /experience/golden-hour-escape/ | | |
| 7.2 | `view_experience_page` event fires on page load | | |
| 7.3 | `experience_slug` value in data layer is "golden-hour-escape" | | |
| 7.4 | Scroll to 50% of page and confirm `scroll_50_percent` fires | | |
| 7.5 | Scroll to 90% of page and confirm `scroll_90_percent` fires | | |
| 7.6 | Click either CTA button and confirm `click_request_to_book` fires | | |
| 7.7 | All events confirmed in GA4 DebugView with correct parameters | | |
| 7.8 | GA4 audience "Viewed Golden Hour Escape" is created and configured | | |

---

## 8. Accessibility

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 8.1 | All images have descriptive alt text | | |
| 8.2 | OG image has alt text attribute | | |
| 8.3 | Both CTA buttons have aria-label attributes | | |
| 8.4 | Ordered list of steps has aria-label attribute | | |
| 8.5 | Gold numerals (01/02/03) have aria-hidden="true" | | Screen readers read the text instead |
| 8.6 | Color contrast: body text (#2C2C2C on white) passes WCAG AA | | Minimum 4.5:1 ratio |
| 8.7 | Color contrast: cream text (#FAF8F3) on navy (#1A2332) passes WCAG AA | | |
| 8.8 | Color contrast: CTA button text (#1A2332) on gold (#DAB97E) passes WCAG AA | | |
| 8.9 | Tab order through the page is logical | | |
| 8.10 | Page is navigable by keyboard alone | | |

---

## 9. Brand Compliance

| # | Check | Pass/Fail | Notes |
|---|---|---|---|
| 9.1 | No em dashes anywhere on the page | | Search page source for U+2014 |
| 9.2 | No "book now" language in any copy | | |
| 9.3 | No use of "luxury" as an adjective | | |
| 9.4 | No use of "unforgettable" | | |
| 9.5 | No use of "once in a lifetime" | | |
| 9.6 | No use of "world-class" | | |
| 9.7 | No star ratings or numerical review scores | | |
| 9.8 | Tone is calm, editorial, and refined throughout | | Subjective review by founder or brand lead |
| 9.9 | All class names use .sss-ghe-* prefix | | |
| 9.10 | All mobile breakpoints use 767px | | |

---

## 10. Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Web Builder | | | |
| Founder Approval | | | |

**Page is approved for publication when both sign-off rows are completed.**

---

## Known Pre-Launch Items

These items are expected to be incomplete at QA and should be tracked separately:

- OG image and Twitter image placeholders must be replaced with the final Golden Hour Escape hero photograph (1200x630px, optimized for web)
- Testimonial names (Sophie M., Claire R.) should be confirmed as real or replaced with verified guest quotes before publishing
- Backend hidden field configuration (item 6.1) must be completed by the web builder
- GTM build (items 7.1 through 7.7) must be verified after GTM container is published
