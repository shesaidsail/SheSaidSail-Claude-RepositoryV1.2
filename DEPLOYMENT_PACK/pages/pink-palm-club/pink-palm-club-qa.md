# Pink Palm Club: QA Checklist

**Experience:** Pink Palm Club
**Page:** /experience/pink-palm-club/
**Last updated:** 2026-05-18

Instructions: Mark each item PASS or FAIL. Resolve all FAILs before sign-off. Do not sign off with any open failures.

---

## Desktop Visual (1440px and 1280px)

| # | Check | Result |
|---|---|---|
| D1 | Hero section renders with cream (#FAF8F3) background at both widths | |
| D2 | H1 "Pink Palm Club" displays in Cormorant Garamond, 52px, navy (#1A2332) | |
| D3 | Tagline renders italic, Cormorant Garamond, 24px, below the H1 | |
| D4 | Quick facts strip shows all three facts: Duration, Guests, Starting From | |
| D5 | All four occasion pills render and are visible without wrapping at 1440px | |
| D6 | Description section shows two-column grid, left column first | |
| D7 | Gold bullet dots display correctly in the includes list | |
| D8 | Social proof section renders with navy (#1A2332) background | |
| D9 | Two quote cards display side by side with gold left border | |
| D10 | Occasion fit section renders with warm cream (#F5F0E8) background | |
| D11 | Occasion list items display with gold left border (2px solid #DAB97E) | |
| D12 | Reassurance section has white background with gold border-top | |
| D13 | Steps 01, 02, 03 display with gold numerals in Cormorant Garamond | |
| D14 | Bottom CTA section renders navy background, full width | |
| D15 | No horizontal scroll at 1440px or 1280px | |
| D16 | Section padding is approximately 96px top and bottom on desktop | |

---

## Mobile Visual (375px and 390px)

| # | Check | Result |
|---|---|---|
| M1 | Hero section renders with 64px padding at 375px | |
| M2 | H1 scales down to 36px on mobile | |
| M3 | Tagline scales down to 20px on mobile | |
| M4 | Quick facts stack cleanly with adequate spacing | |
| M5 | Occasion pills wrap neatly across two rows without overflow | |
| M6 | Description section collapses to single column, left (editorial) first | |
| M7 | "Request to Book" button is full width at 375px | |
| M8 | Social proof quote cards stack to single column on mobile | |
| M9 | Occasion fit section collapses to single column | |
| M10 | Reassurance steps display cleanly in single column | |
| M11 | Bottom CTA button is full width at 375px, max-width 360px | |
| M12 | No content is cut off or overflowing at 375px or 390px | |
| M13 | All breakpoints trigger at 767px (not 768px or other values) | |

---

## Content Accuracy

| # | Check | Result |
|---|---|---|
| C1 | Experience name is exactly "Pink Palm Club" (capitalization correct) | |
| C2 | Tagline reads: "Music on. Group together. Miami behind you. This is the bachelorette day your friend has been waiting for." | |
| C3 | Duration fact reads "4 to 6 Hours" | |
| C4 | Guests fact reads "Up to 22" | |
| C5 | Starting From fact reads "$10,000" | |
| C6 | Four occasion pills present: Bachelorette, Birthday Party, Girls Trip, Group Celebration | |
| C7 | Editorial description is 4 paragraphs, energetic and elevated in tone | |
| C8 | Includes list contains exactly 6 items as specified | |
| C9 | Quote 1 attribution reads "Mia K., Bachelorette Charter" | |
| C10 | Quote 2 attribution reads "Danielle T., Group Birthday" | |
| C11 | Occasion fit section heading reads "Who This Experience Is For" | |
| C12 | Occasion list contains exactly 4 items as specified | |
| C13 | Reassurance heading reads "How It Works" | |
| C14 | Three numbered steps present with 01, 02, 03 labels | |
| C15 | Bottom CTA heading reads "Ready to request Pink Palm Club?" | |
| C16 | Disclaimer reads "No deposit required to inquire. No commitment until you are ready." | |

---

## CTA Accuracy

| # | Check | Result |
|---|---|---|
| CTA1 | Section 2 button text reads "Request to Book" | |
| CTA2 | Section 2 button links to /request-to-book/?selected_experience=pink-palm-club | |
| CTA3 | Section 6 button text reads "Request Pink Palm Club" | |
| CTA4 | Section 6 button links to /request-to-book/?selected_experience=pink-palm-club | |
| CTA5 | Both buttons open in the same tab (no target="_blank") | |
| CTA6 | Hover state on both buttons transitions to #C9A96E (gold-deep) | |
| CTA7 | URL parameter value is lowercase, hyphenated: pink-palm-club | |
| CTA8 | No button uses "book now" language | |

---

## SEO

| # | Check | Result |
|---|---|---|
| S1 | Page title is "Pink Palm Club | She Said Sail" | |
| S2 | Meta description is 155 characters or fewer | |
| S3 | Meta description contains "bachelorette", "Miami", "up to 22", "$10,000" | |
| S4 | Canonical URL is https://shesaidsail.com/experience/pink-palm-club/ | |
| S5 | OG title is "Pink Palm Club | She Said Sail" | |
| S6 | OG type is "website" | |
| S7 | OG image placeholder comment is present | |
| S8 | OG image dimensions are specified as 1200x630 | |
| S9 | Twitter card is set to "summary_large_image" | |
| S10 | JSON-LD script is valid JSON (validate at schema.org/validator) | |
| S11 | JSON-LD @type is "Service" | |
| S12 | JSON-LD minPrice is 10000 with priceCurrency USD | |
| S13 | JSON-LD provider address references Miami, FL | |

---

## Backend

| # | Check | Result |
|---|---|---|
| B1 | Submit the request form via /request-to-book/?selected_experience=pink-palm-club | |
| B2 | Confirm hidden field `selected_experience` arrives in Airtable as "pink-palm-club" | |
| B3 | Confirm hidden field `brand` arrives as "shesaidsail" | |
| B4 | Confirm hidden field `service_category` arrives as "yacht-charter" | |
| B5 | Confirm record appears in the Requests table (not a new table) | |
| B6 | Confirm Make.com M-BRAND-ROUTER picks up the submission and routes correctly | |
| B7 | Confirm concierge notification fires within expected time | |

---

## Analytics

| # | Check | Result |
|---|---|---|
| A1 | GTM Preview mode is active and connected to /experience/pink-palm-club/ | |
| A2 | `view_experience_page` fires on page load | |
| A3 | `experience_slug` value in data layer is "pink-palm-club" | |
| A4 | `click_request_to_book` fires when Section 2 CTA is clicked | |
| A5 | `click_request_to_book` fires when Section 6 CTA is clicked | |
| A6 | `scroll_50_percent` fires at 50% scroll depth | |
| A7 | `scroll_90_percent` fires at 90% scroll depth | |

---

## Accessibility

| # | Check | Result |
|---|---|---|
| AC1 | Both CTA links have descriptive aria-label attributes | |
| AC2 | Social proof section has aria-label="Pink Palm Club guest reviews" | |
| AC3 | Ordered list for steps has aria-label="Booking steps for Pink Palm Club" | |
| AC4 | Step numbers have aria-hidden="true" | |
| AC5 | Color contrast for body text (#2C2C2C on white) passes WCAG AA | |
| AC6 | Color contrast for H1 (#1A2332 on #FAF8F3) passes WCAG AA | |
| AC7 | Color contrast for cream text on navy background passes WCAG AA | |
| AC8 | All interactive elements are keyboard focusable | |
| AC9 | Focus state is visible on CTA buttons | |

---

## Brand Quality

| # | Check | Result |
|---|---|---|
| BQ1 | No em dashes anywhere in the page content | |
| BQ2 | No use of the word "luxury" as an adjective | |
| BQ3 | No use of "unforgettable" | |
| BQ4 | No use of "once in a lifetime" | |
| BQ5 | No use of "world-class" | |
| BQ6 | No "book now" language on any button or link | |
| BQ7 | Tone is energetic and elevated, not hype or breathless | |
| BQ8 | All class names use .sss-ppc-* prefix | |
| BQ9 | No class names from other experience pages (.sss-ms-*, .sss-ghe-*) are used | |

---

## Sign-off

| Role | Name | Date | Status |
|---|---|---|---|
| Web Builder | | | |
| QA Reviewer | | | |
| Project Lead | | | |

All items must be PASS before sign-off. Do not publish the Pink Palm Club page until this checklist is fully signed off.
