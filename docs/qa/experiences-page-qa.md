# Experiences Page QA Checklist

**Version:** 1.0
**Date:** 2026-05-18
**Branch:** claude/fix-experiences-page-EwvlD
**Status:** Ready for human QA pass after WordPress implementation

---

## Pre-Launch QA Checklist

### Luxury Positioning

- [ ] H1 reads "Choose the atmosphere first." (no em dash, no period optional per design)
- [ ] Subheadline references birthdays, bachelorettes, girls trips
- [ ] Hero copy does not use the word "package" or "package listing"
- [ ] Page tone is calm and editorial, not promotional
- [ ] No urgency language ("limited availability", "book now", "don't miss")

### Experience Cards

- [ ] Monaco Social card is visually featured (larger, wider, or more prominent)
- [ ] All four cards display atmosphere labels
- [ ] All four cards display occasion badges
- [ ] Monaco Social copy matches approved descriptor
- [ ] Golden Hour Escape copy matches approved descriptor
- [ ] Rose Day Club copy matches approved descriptor
- [ ] Pink Palm Club copy matches approved descriptor
- [ ] All card button copy reads "Explore This Experience" (not "Explore Experience")
- [ ] Hover states on cards are subtle, not flashy
- [ ] Image focal crops are appropriate on mobile (faces/moments visible, not cropped awkwardly)

### Social Proof Strip

- [ ] Three quotes visible between experience grid and bottom CTA
- [ ] No star ratings present
- [ ] No slider or carousel
- [ ] Attribution labels are present (Birthday Group Miami, Bachelorette Party, Girls Trip South Beach)
- [ ] Quote text contains no em dashes

### CTA Flow

- [ ] "Request to Book" appears in navigation header
- [ ] Bottom CTA section includes "Get Recommendations" button
- [ ] "Get Recommendations" opens Tidio chat
- [ ] No competing primary CTAs at the same visual level
- [ ] Bottom recommendation section has background image (warm, golden, nautical)

### Mobile UX (test at 390px / iPhone 14 Pro viewport)

- [ ] H1 font size reduces gracefully (recommended 32-36px on mobile)
- [ ] Experience cards stack to single column
- [ ] Card images have consistent height on mobile (recommended 240-260px)
- [ ] CTA buttons are minimum 44px tap target height
- [ ] Social proof quotes are readable at 16px
- [ ] No horizontal overflow or scroll
- [ ] Footer stacks cleanly to single column
- [ ] Spacing between sections is consistent (40-60px recommended on mobile)

### SEO and Metadata

- [ ] Page title is "Experiences | She Said Sail -- Private Yacht Charters Miami" (no em dash, use pipe or colon)
- [ ] Meta description is present and under 160 characters
- [ ] Open Graph title is present
- [ ] Open Graph description is present
- [ ] Open Graph image is set (recommended: Monaco Social hero image or brand lifestyle image)
- [ ] Twitter/X meta tags are present
- [ ] All experience images have descriptive alt text
- [ ] No duplicate H1 elements on the page
- [ ] H2 headings are used for experience names (or H3 if H2 is reserved for sections)
- [ ] Canonical URL is set to /experiences/

### Backend Readiness

- [ ] All experience cards have data-experience-key attributes
- [ ] All experience cards have data-experience-name attributes
- [ ] "Explore This Experience" buttons have data-track-click="explore-experience"
- [ ] "Request to Book" links have data-track-click="request-to-book"
- [ ] "Get Recommendations" button has data-track-click="get-recommendations"
- [ ] UTM capture script is present in page head or GTM
- [ ] sessionStorage writes correctly for experience_interest on card click

### Analytics Readiness

- [ ] GTM fires view_experiences_page on page load
- [ ] GTM fires click_experience_card on experience card click
- [ ] GTM fires click_explore_experience on button click
- [ ] GTM fires click_request_to_book on header and footer button clicks
- [ ] GTM fires scroll_50_percent when user reaches 50% scroll
- [ ] GTM fires scroll_90_percent when user reaches 90% scroll
- [ ] Events visible in GA4 DebugView
- [ ] Meta Pixel events visible in Pixel Helper

### Accessibility

- [ ] All interactive elements have visible focus states
- [ ] Color contrast meets WCAG AA (4.5:1 for body text, 3:1 for large text)
- [ ] Images have non-empty alt attributes
- [ ] Buttons have descriptive accessible labels
- [ ] Page is navigable by keyboard
- [ ] No content flashes or layout shifts on load (check Core Web Vitals)

### Performance

- [ ] Images use lazy loading (loading="lazy") except the first above-fold image
- [ ] First above-fold image uses fetchpriority="high"
- [ ] No render-blocking scripts in head
- [ ] Page passes Core Web Vitals (LCP < 2.5s, CLS < 0.1, INP < 200ms)

---

## Regression Checklist

Verify these existing functions still work after implementation:

- [ ] Navigation header sticky behavior works on scroll
- [ ] Mobile hamburger menu opens and closes
- [ ] Tidio chat still loads
- [ ] Footer social links open correctly
- [ ] GTM container still fires (GTM-WWTT27Z3)
- [ ] GA4 still fires (GT-WV3X86GZ)
- [ ] Individual experience page links work correctly
- [ ] "Request to Book" navigation link works

---

## Sign-Off

| Role | Name | Date | Status |
|---|---|---|---|
| Developer | | | Pending |
| Creative Director | | | Pending |
| Founder | | | Pending |
