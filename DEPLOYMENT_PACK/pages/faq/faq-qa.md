# FAQ Page: QA Checklist

**Page:** /faq/
**Slug:** faq
**File under test:** faq-html-snippets.html, faq-metadata.html

Tester initials: _______ Date tested: _______

Mark each item PASS, FAIL, or N/A. Note any failures with detail.

---

## Desktop Rendering (1440px and 1280px)

| # | Check | 1440px | 1280px | Notes |
|---|---|---|---|---|
| D1 | Page header section renders with cream background | | | |
| D2 | Gold eyebrow "Before You Ask" visible | | | |
| D3 | H1 "Everything you want to know." displays in Cormorant Garamond | | | |
| D4 | Subline text visible, centered, max-width respected | | | |
| D5 | Thin gold rule visible below subline | | | |
| D6 | FAQ categories section renders with white background | | | |
| D7 | All 7 category headings visible | | | |
| D8 | All 18 Q&A pairs visible with no hidden content | | | |
| D9 | No accordion behavior. All answers display without interaction | | | |
| D10 | Inline text links visible after Booking and Timing category | | | |
| D11 | Inline text links visible after The Experience category | | | |
| D12 | Inline text links visible after Group Size category | | | |
| D13 | Bottom CTA section renders with navy background | | | |
| D14 | H2 "Still have a question?" displays in italic Cormorant Garamond | | | |
| D15 | Gold fill button "Request to Book" links to /request-to-book/ | | | |
| D16 | Ghost button "View the Experiences" links to /experiences/ | | | |
| D17 | Both buttons display side by side (column layout stacking is acceptable) | | | |

---

## Mobile Rendering (375px and 390px)

| # | Check | 375px | 390px | Notes |
|---|---|---|---|---|
| M1 | Page header text readable, no horizontal overflow | | | |
| M2 | H1 scales to mobile font size (36px target) | | | |
| M3 | Subline readable at 16px | | | |
| M4 | Category headings visible, no truncation | | | |
| M5 | Question text (16px) does not overflow container | | | |
| M6 | Answer text readable, line-height comfortable | | | |
| M7 | Max-width constraint does not cause layout issues | | | |
| M8 | Bottom CTA buttons stack full-width | | | |
| M9 | Gold fill button and ghost button both full-width on mobile | | | |
| M10 | No horizontal scroll on any section | | | |

---

## Content Accuracy

| # | Check | Result | Notes |
|---|---|---|---|
| C1 | Category 1 heading: "The Basics" | | |
| C2 | Category 2 heading: "Booking and Timing" | | |
| C3 | Category 3 heading: "The Experience" | | |
| C4 | Category 4 heading: "Logistics" | | |
| C5 | Category 5 heading: "Weather" | | |
| C6 | Category 6 heading: "Group Size" | | |
| C7 | Category 7 heading: "After Your Experience" | | |
| C8 | Total of 18 Q&A pairs present (count manually) | | |
| C9 | Answer to "What is She Said Sail?" matches brief exactly | | |
| C10 | Answer to "Is gratuity included?" mentions 15 to 20 percent | | |
| C11 | Answer to "What is the minimum and maximum group size?" mentions Pink Palm Club | | |
| C12 | Inline link after Booking category links to /request-to-book/ | | |
| C13 | Inline link after The Experience category links to /experiences/ | | |
| C14 | Inline link after Group Size category links to /experiences/ | | |
| C15 | No "FAQ" used as a heading anywhere on the page | | |

---

## Schema Validation

| # | Check | Result | Notes |
|---|---|---|---|
| S1 | Copy full script tag from faq-metadata.html and paste into validator.schema.org | | |
| S2 | Schema type validates as FAQPage | | |
| S3 | All 18 Question entities present in validation output | | |
| S4 | No validation errors reported | | |
| S5 | Run through Google Rich Results Test at search.google.com/test/rich-results | | |
| S6 | Rich Results Test confirms FAQ eligibility | | |

---

## SEO and Metadata

| # | Check | Result | Notes |
|---|---|---|---|
| E1 | Title: "FAQ | She Said Sail Private Yacht Charters Miami" | | |
| E2 | Meta description present and under 155 characters | | |
| E3 | og:title present | | |
| E4 | og:description present | | |
| E5 | og:type set to "website" | | |
| E6 | og:url set to https://shesaidsail.com/faq/ | | |
| E7 | og:image placeholder present (replace before launch) | | |
| E8 | og:site_name set to "She Said Sail" | | |
| E9 | og:locale set to "en_US" | | |
| E10 | Twitter card type: summary_large_image | | |
| E11 | Canonical tag: https://shesaidsail.com/faq/ | | |

---

## Analytics Verification (GTM Preview Mode)

| # | Check | Result | Notes |
|---|---|---|---|
| A1 | Open GTM Preview and load https://shesaidsail.com/faq/ | | |
| A2 | view_faq_page event fires on page load | | |
| A3 | Click "Request to Book" bottom CTA button | | |
| A4 | click_request_to_book event fires | | |
| A5 | Click "View the Experiences" ghost button | | |
| A6 | click_explore_experiences event fires | | |
| A7 | Scroll to 50% of page, scroll_50_percent fires | | |
| A8 | Scroll to 90% of page, scroll_90_percent fires | | |

---

## Accessibility

| # | Check | Result | Notes |
|---|---|---|---|
| AC1 | One H1 on the page (page header) | | |
| AC2 | Category headings use H2 (not H3 or div) | | |
| AC3 | Questions use p with font-weight 600 (not H3 or H4, per design spec) | | |
| AC4 | No images on this page requiring alt text | | |
| AC5 | Links have descriptive text (not "click here") | | |
| AC6 | Color contrast: navy on cream, gold on navy pass WCAG AA | | |

---

## Brand and Tone

| # | Check | Result | Notes |
|---|---|---|---|
| B1 | Zero em dashes in any answer text or heading | | |
| B2 | No robotic FAQ tone. Answers read conversationally | | |
| B3 | No "please note" or "kindly" language anywhere | | |
| B4 | No bullet lists inside answer text | | |
| B5 | Answers are 2 to 4 sentences maximum | | |
| B6 | Page heading is not just "FAQ" | | |

---

## Post-Launch Checks (Cannot Verify Pre-Launch)

| # | Check | Target Date | Result |
|---|---|---|---|
| P1 | Check Google Search Console Enhancements for FAQ rich result | 2 to 4 weeks post-launch | |
| P2 | Run Google Rich Results Test on live URL | 48 hours post-launch | |
| P3 | Confirm GA4 audience "Visited FAQ - No Submit" is accumulating users | 7 days post-launch | |
| P4 | Replace og:image placeholder with actual 1200x630 brand photo | Before launch | |

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| Content Review | | | |
| Analytics Review | | | |
| Final Approval | | | |
