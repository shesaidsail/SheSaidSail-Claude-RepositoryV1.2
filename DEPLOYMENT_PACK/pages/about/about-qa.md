# About Page: QA Checklist

**Page:** `/about/`
**Last updated:** 2026-05-18

Sign off each item with PASS, FAIL, or N/A. Record tester name and date in the sign-off section at the bottom.

---

## Desktop Layout (test at 1440px and 1280px)

| # | Check | Result |
|---|---|---|
| D-01 | All 4 sections render in correct order: Hero, Brand Story, Values, Bottom CTA | |
| D-02 | Hero: cream background (#FAF8F3), gold eyebrow label, H1 visible, subline visible | |
| D-03 | Brand Story: two-column grid displays correctly (text left, image right) | |
| D-04 | Brand Story: image placeholder visible at correct height (500px) with warm grey background | |
| D-05 | Values: three cards display in a horizontal row | |
| D-06 | Values: each card has gold top border (3px solid #DAB97E) | |
| D-07 | Bottom CTA: navy background, two buttons side by side | |
| D-08 | Bottom CTA: primary button gold fill, secondary button ghost (cream border, transparent background) | |
| D-09 | No horizontal scroll at either breakpoint | |
| D-10 | Section padding is consistent (approximately 96px top and bottom) | |

---

## Mobile Layout (test at 375px and 390px)

| # | Check | Result |
|---|---|---|
| M-01 | Hero: text scales correctly, no overflow | |
| M-02 | Brand Story: text column appears first (top), image placeholder appears below text | |
| M-03 | Brand Story: image placeholder height is 340px on mobile | |
| M-04 | Values: three cards stack to single column | |
| M-05 | Bottom CTA: "View the Experiences" and "Request to Book" buttons stack vertically | |
| M-06 | Bottom CTA: buttons are full width (max-width 320px, centered) | |
| M-07 | Section padding reduces correctly (approximately 64px top and bottom) | |
| M-08 | No text clipping or overflow on any section | |

---

## Content

| # | Check | Result |
|---|---|---|
| C-01 | Hero H1 reads: "Built for the days that matter." | |
| C-02 | Hero eyebrow reads: "OUR STORY" | |
| C-03 | Hero subline is present and begins: "She Said Sail started with a simple observation..." | |
| C-04 | Brand Story section label reads: "WHY WE EXIST" | |
| C-05 | Brand Story H2 reads: "The yacht is not the product." | |
| C-06 | Brand Story body contains 4 paragraphs. No placeholder text present (no "Lorem ipsum") | |
| C-07 | Values heading reads: "What we believe" | |
| C-08 | Value card 1 title reads: "The feeling comes first." | |
| C-09 | Value card 2 title reads: "Celebrations deserve specificity." | |
| C-10 | Value card 3 title reads: "No commitment until you are ready." | |
| C-11 | All 3 value card body paragraphs are present with correct text | |
| C-12 | Bottom CTA H2 reads: "Ready to see what we have planned?" | |

---

## Image Placeholder

| # | Check | Result |
|---|---|---|
| I-01 | `.sss-ab-story-img-placeholder` div is present in the DOM | |
| I-02 | HTML comment is present inside the image column: "Replace with brand photography or founder photo at 600x700px. Warm tones, natural light preferred." | |
| I-03 | Placeholder has `role="img"` and `aria-label` attribute for accessibility | |

---

## CTAs and Links

| # | Check | Result |
|---|---|---|
| L-01 | "View the Experiences" button links to `/experiences/` | |
| L-02 | "Request to Book" button links to `/request-to-book/` | |
| L-03 | Both links open in the same tab (no `target="_blank"` on internal links) | |
| L-04 | Both buttons have visible hover states | |

---

## SEO

| # | Check | Result |
|---|---|---|
| S-01 | Title tag reads: "About She Said Sail | Private Yacht Experiences in Miami" | |
| S-02 | Meta description is present and 155 characters or fewer | |
| S-03 | Canonical tag points to `https://shesaidsail.com/about/` | |
| S-04 | `og:title` is present | |
| S-05 | `og:description` is present | |
| S-06 | `og:type` is set to `website` | |
| S-07 | `og:url` is set to `https://shesaidsail.com/about/` | |
| S-08 | `og:image` tag is present (replace placeholder before launch) | |
| S-09 | `og:site_name` is set to "She Said Sail" | |
| S-10 | `og:locale` is set to `en_US` | |
| S-11 | Twitter card type is `summary_large_image` | |
| S-12 | JSON-LD Organization schema is present and valid (test with Google Rich Results Test or schema.org validator) | |
| S-13 | JSON-LD `sameAs` includes the correct Instagram URL | |

---

## Analytics

| # | Check | Result |
|---|---|---|
| A-01 | `view_about_page` fires in GTM Preview when `/about/` loads | |
| A-02 | `click_request_to_book` fires in GTM Preview when "Request to Book" bottom CTA is clicked | |
| A-03 | `click_explore_experiences` fires in GTM Preview when "View the Experiences" bottom CTA is clicked | |
| A-04 | `scroll_50_percent` fires when user scrolls halfway down the page | |
| A-05 | `scroll_90_percent` fires when user scrolls near the bottom | |
| A-06 | GA4 Event tag for `view_about_page` is confirmed firing in GA4 DebugView | |

---

## Accessibility

| # | Check | Result |
|---|---|---|
| AC-01 | Page has exactly one H1 (located in the Hero section) | |
| AC-02 | Brand Story heading uses H2 | |
| AC-03 | Values section "What we believe" uses H2 | |
| AC-04 | Bottom CTA heading uses H2 | |
| AC-05 | Value card titles use H3 | |
| AC-06 | Heading hierarchy is logical: H1 > H2 > H3, no skipped levels | |
| AC-07 | Image placeholder has `role="img"` and descriptive `aria-label` | |
| AC-08 | All interactive elements (buttons/links) are keyboard navigable | |
| AC-09 | Color contrast on gold eyebrow text meets WCAG AA on cream background (verify with contrast checker) | |
| AC-10 | Color contrast on CTA subline (rgba white at 70% opacity on navy) meets WCAG AA minimum | |

---

## Brand and Copy

| # | Check | Result |
|---|---|---|
| B-01 | No em dashes present anywhere on the page (search for U+2014 character) | |
| B-02 | No use of "passionate about" anywhere in copy | |
| B-03 | No use of "world-class" anywhere in copy | |
| B-04 | No use of "unforgettable" anywhere in copy | |
| B-05 | No use of "luxury" as a standalone adjective in copy | |
| B-06 | Founder (Will) is referenced naturally, not given excessive prominence | |
| B-07 | Bottom CTA offers two options (experiences and request-to-book), not just one | |
| B-08 | No generic mission statement bullet points in the values section | |
| B-09 | No placeholder text ("Lorem ipsum" or similar) anywhere on the page | |
| B-10 | Tone reads as warm and personal, not corporate | |

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| Designer | | | |
| Copywriter | | | |
| Project Lead | | | |

**Pre-launch reminder:** Replace the `og:image` and `twitter:image` placeholders with the final 1200x630 brand photo before the page goes live. Replace the `.sss-ab-story-img-placeholder` div with actual `<img>` markup once brand photography is available.
