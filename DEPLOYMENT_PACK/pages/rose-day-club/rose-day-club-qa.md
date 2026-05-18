# Rose Day Club: QA Checklist

Page: /experience/rose-day-club/
CTA URL: /request-to-book/?selected_experience=rose-day-club
Tester: ___________________
Date: ___________________
Environment: ___________________

Status key: PASS / FAIL / N/A

---

## Desktop Visual (1440px)

| # | Check | Status | Notes |
|---|---|---|---|
| D1 | Hero support section renders on cream (#FAF8F3) background | | |
| D2 | H1 "Rose Day Club" displays in Cormorant Garamond, 52px, navy color | | |
| D3 | Tagline renders italic, 24px, correct copy | | |
| D4 | Quick facts strip shows 3 items in horizontal row with gold borders | | |
| D5 | All 4 occasion pills render in single row, no wrapping | | |
| D6 | Description section renders as two-column grid | | |
| D7 | Includes list shows 6 items with gold dot markers | | |
| D8 | Social proof section renders on navy background | | |
| D9 | Two quote cards render side by side in 2-column grid | | |
| D10 | Quote cards have gold left border (2px solid #DAB97E) | | |
| D11 | Occasion fit section renders on warm cream (#F5F0E8) background | | |
| D12 | Occasion list items have gold left border | | |
| D13 | How It Works section has border-top in gold at correct opacity | | |
| D14 | Step numbers (01/02/03) render in gold, Cormorant Garamond | | |
| D15 | Bottom CTA section renders on navy background | | |
| D16 | Bottom CTA heading is italic Cormorant Garamond in cream color | | |
| D17 | Gold CTA button renders correctly with correct text | | |
| D18 | Disclaimer text renders below button at reduced opacity | | |
| D19 | All sections have 96px top and bottom padding | | |
| D20 | No horizontal scrollbar appears | | |

## Desktop Visual (1280px)

| # | Check | Status | Notes |
|---|---|---|---|
| D21 | Two-column layouts remain intact at 1280px | | |
| D22 | Max-width containers center correctly | | |
| D23 | No text overflow or truncation | | |

---

## Mobile Visual (375px)

| # | Check | Status | Notes |
|---|---|---|---|
| M1 | Hero section padding reduced to 64px | | |
| M2 | H1 renders at 38px on mobile | | |
| M3 | Tagline renders at 20px on mobile | | |
| M4 | Quick facts stack vertically with horizontal dividers | | |
| M5 | Occasion pills wrap to multiple rows cleanly | | |
| M6 | Description section collapses to single column, left (text) first | | |
| M7 | Includes list is full width | | |
| M8 | Social proof quotes stack to single column | | |
| M9 | Occasion fit section collapses to single column | | |
| M10 | Reassurance steps remain readable, numerals align correctly | | |
| M11 | Bottom CTA button is full width (max 340px) | | |
| M12 | No content is cut off or hidden behind other elements | | |
| M13 | All padding reduced to 64px on mobile sections | | |
| M14 | Touch targets (buttons, links) are at least 44px tall | | |

## Mobile Visual (390px)

| # | Check | Status | Notes |
|---|---|---|---|
| M15 | All M1-M14 checks pass at 390px viewport | | |
| M16 | No layout differences between 375px and 390px that cause visual breaks | | |

---

## Content Accuracy

| # | Check | Status | Notes |
|---|---|---|---|
| C1 | Experience name: "Rose Day Club" (exact, no variations) | | |
| C2 | Tagline: "An afternoon charter built for the kind of day your group has been promising each other all year." | | |
| C3 | Duration quick fact: "4 to 5 Hours" | | |
| C4 | Guests quick fact: "Up to 18" | | |
| C5 | Starting From quick fact: "$10,000" | | |
| C6 | Occasion pills: Girls Trip, Birthday Celebration, Bachelorette Day, Friend Reunion | | |
| C7 | Includes list: all 6 items present and correctly spelled | | |
| C8 | Quote 1 attribution: "Natalie S., Girls Trip" | | |
| C9 | Quote 2 attribution: "Jade M., Birthday Celebration" | | |
| C10 | Occasion list: all 4 types present | | |
| C11 | How It Works: 3 numbered steps with correct copy | | |
| C12 | Bottom CTA heading: "Ready to request Rose Day Club?" | | |
| C13 | Bottom CTA subline: "Submit your details and a concierge will reach out within 24 hours." | | |
| C14 | Disclaimer: "No deposit required to inquire. No commitment until you are ready." | | |

---

## CTA Accuracy

| # | Check | Status | Notes |
|---|---|---|---|
| CTA1 | Description section CTA button text: "Request to Book" | | |
| CTA2 | Description CTA links to: /request-to-book/?selected_experience=rose-day-club | | |
| CTA3 | Bottom CTA button text: "Request Rose Day Club" | | |
| CTA4 | Bottom CTA links to: /request-to-book/?selected_experience=rose-day-club | | |
| CTA5 | Both CTA URLs include the full query parameter (no truncation) | | |
| CTA6 | On the RTB page, the hidden field selected_experience populates as "rose-day-club" | | |

---

## SEO

| # | Check | Status | Notes |
|---|---|---|---|
| S1 | Page title tag: "Rose Day Club | She Said Sail" | | |
| S2 | Meta description present, 155 chars or fewer | | |
| S3 | Meta description does not contain prohibited words | | |
| S4 | Canonical URL: https://shesaidsail.com/experience/rose-day-club/ | | |
| S5 | og:title: "Rose Day Club | She Said Sail" | | |
| S6 | og:description matches meta description | | |
| S7 | og:type: "website" | | |
| S8 | og:url: https://shesaidsail.com/experience/rose-day-club/ | | |
| S9 | og:image placeholder is replaced with actual image before launch | | |
| S10 | og:locale: "en_US" | | |
| S11 | og:site_name: "She Said Sail" | | |
| S12 | Twitter card type: "summary_large_image" | | |
| S13 | JSON-LD script present in page source | | |
| S14 | JSON-LD validates without errors (use schema.org validator) | | |
| S15 | JSON-LD minPrice: 10000 | | |
| S16 | JSON-LD provider address: Miami, FL | | |
| S17 | H1 is unique on the page (only one H1) | | |

---

## Backend

| # | Check | Status | Notes |
|---|---|---|---|
| B1 | Hidden field selected_experience populates "rose-day-club" on RTB page load | | |
| B2 | Form submission creates record in Airtable Requests table | | |
| B3 | Airtable record shows brand = "shesaidsail" | | |
| B4 | Airtable record shows service_category = "yacht-charter" | | |
| B5 | Airtable record shows selected_experience = "rose-day-club" | | |
| B6 | Make.com M-BRAND-ROUTER routes submission to She Said Sail flow | | |
| B7 | Confirmation state appears after form submission | | |

---

## Analytics

| # | Check | Status | Notes |
|---|---|---|---|
| A1 | GTM Preview mode active during testing | | |
| A2 | view_experience_page fires on page load | | |
| A3 | view_experience_page includes experience_slug: "rose-day-club" | | |
| A4 | click_request_to_book fires on CTA click (description section) | | |
| A5 | click_request_to_book fires on CTA click (bottom CTA section) | | |
| A6 | scroll_50_percent fires at 50% scroll depth | | |
| A7 | scroll_90_percent fires at 90% scroll depth | | |
| A8 | All events visible in GA4 DebugView with correct parameters | | |

---

## Accessibility

| # | Check | Status | Notes |
|---|---|---|---|
| AC1 | All images have descriptive alt text | | |
| AC2 | CTA buttons have clear, descriptive link text (not "click here") | | |
| AC3 | Color contrast passes WCAG AA for all text on backgrounds | | |
| AC4 | Gold (#DAB97E) on navy (#1A2332) passes contrast check | | |
| AC5 | Body text (#2C2C2C) on cream (#FAF8F3) passes contrast check | | |
| AC6 | Body text (#2C2C2C) on warm (#F5F0E8) passes contrast check | | |
| AC7 | Heading hierarchy is logical (H1, then H2, then H3) | | |
| AC8 | No content relies on color alone to convey meaning | | |
| AC9 | Page is navigable via keyboard | | |

---

## Brand

| # | Check | Status | Notes |
|---|---|---|---|
| BR1 | Zero em dashes in any visible copy | | |
| BR2 | Zero em dashes in any HTML comments or code | | |
| BR3 | No "book now" language present | | |
| BR4 | No use of "luxury" as an adjective | | |
| BR5 | No "unforgettable" in any copy | | |
| BR6 | No "once in a lifetime" in any copy | | |
| BR7 | No "world-class" in any copy | | |
| BR8 | Tone reads warm, social, slightly playful but elevated | | |
| BR9 | Class names all use .sss-rdc-* prefix | | |

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| Designer | | | |
| Copywriter | | | |
| Project Lead | | | |

**Go-live approved:** Yes / No

**Approved by:** ___________________

**Approved date:** ___________________
