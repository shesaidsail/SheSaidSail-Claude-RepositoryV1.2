# SHE SAID SAIL
# MASTER MOBILE UX STANDARD

STATUS: PRODUCTION
VERSION: v1.0

---

## BREAKPOINTS

| Name | Range | Behavior |
|------|-------|----------|
| Mobile | 0–767px | Single column, stacked |
| Tablet | 768–1023px | 2-column grids, condensed nav |
| Desktop | 1024px+ | Full layout |
| Wide | 1440px+ | Max-width container centered |

---

## MOBILE TYPOGRAPHY

| Element | Mobile Size | Notes |
|---------|-------------|-------|
| H1 hero | 34–40px | Reduce from desktop 52–64px |
| H2 section | 26–30px | Reduce from 36–44px |
| H3 | 20–22px | |
| Body | 15–16px | Never below 15px |
| Label caps | 10–11px | Same as desktop |
| Button text | 11px | Same as desktop |

---

## MOBILE SPACING

- Side padding: 20px minimum
- Section padding top/bottom: 56px (vs 96px desktop)
- Card padding: 24px (vs 40px desktop)
- Stack all grids below 768px
- No horizontal scrolling permitted

---

## TOUCH TARGETS

- All buttons: minimum 44px height, 44px wide
- Form inputs: minimum 48px height
- Nav items: minimum 44px touch zone
- Accordion headers: minimum 52px height
- CTA buttons: full-width on mobile (100% width)

---

## MOBILE CTA BEHAVIOR

- Primary CTA: full-width button, sticky bottom bar on key pages
- Sticky bar: appears after 30% scroll, nav-height from bottom
- Sticky bar dismissible: yes, after tap
- Inquiry form: scroll to form on CTA tap (smooth scroll)
- Phone tap: tel: link always active

---

## MOBILE FORM UX

- Input type="email" triggers email keyboard
- Input type="tel" triggers numeric keyboard
- Input type="date" or date picker: native preferred
- Select menus: native mobile select (no custom JS dropdowns)
- Form fields: full-width on mobile
- Error messages: below field, 13px, red #cc4444
- Success state: green #2a7a4b confirmation message

---

## MOBILE IMAGE STANDARDS

- Hero: use mobile-optimized crop (portrait-friendly, 4:5 ratio)
- Gallery: 2-column, 4px gap
- No hover states on touch (use tap states instead)
- Lazy load all below-fold images
- srcset: provide 400w, 800w, 1200w variants

---

## MOBILE NAVIGATION

- Logo: centered or left, max 120px wide
- Hamburger: right-aligned, 44x44 touch zone
- Menu overlay: full screen, dark background, centered links
- Close button: top right, 44x44
- No nested mobile nav (max 2 levels)

---

## MOBILE PERFORMANCE TARGETS

- First Contentful Paint: under 2s on 4G
- Time to Interactive: under 4s
- Largest Contentful Paint: under 3s
- No layout shift from late-loading content (use aspect-ratio reservations)

---

## MOBILE ACCESSIBILITY

- Minimum font size 15px (never 12px or smaller in body copy)
- Tap targets never overlapping
- No content hidden behind hover-only states
- Sufficient color contrast maintained at all sizes
