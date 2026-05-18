# SHE SAID SAIL
# MASTER MOBILE UX STANDARD

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## MOBILE-FIRST PHILOSOPHY

The majority of She Said Sail guests discover and convert on mobile. All pages must be designed mobile-first and then enhanced for desktop, not the reverse.

---

## BREAKPOINTS

| Name | Width | Target Device |
|------|-------|---------------|
| Mobile | < 768px | iPhone, Android |
| Tablet | 768px to 1024px | iPad |
| Desktop | > 1024px | Laptop, monitor |

---

## MOBILE TYPOGRAPHY

| Element | Min Size | Line Height |
|---------|----------|-------------|
| Hero H1 | 32px | 1.2 |
| H2 | 26px | 1.3 |
| H3 | 22px | 1.35 |
| Body | 16px | 1.8 |
| Caption | 14px | 1.5 |
| Eyebrow | 11px | 1 |
| CTA | 14px | 1 |

Never below 16px for body copy on mobile.

---

## TOUCH TARGETS

- Minimum touch target height: 48px
- Minimum touch target width: 48px
- Minimum spacing between adjacent touch targets: 8px
- CTA buttons: full width on mobile (100%), max-width 480px
- Nav links: minimum 44px tap area

---

## SPACING ON MOBILE

| Element | Mobile Value |
|---------|-------------|
| Section padding top/bottom | 56px |
| Container horizontal padding | 20px |
| Card padding | 24px |
| Form field gap | 16px |
| Stack gap (image above copy) | 32px |

---

## LAYOUT ADAPTATIONS

### Two-column to single-column
- All desktop two-column layouts stack vertically on mobile
- Image always above copy
- Never side-by-side on mobile

### Grid collapses
- Stat grids: 2x2 on mobile (wrap at 2 per row)
- Feature lists: single column always
- Social proof: single column, no side-by-side quotes

### Navigation
- Hamburger menu on mobile
- Full-screen overlay preferred over side drawer
- CTA in nav visible even in mobile menu

### Hero
- 75vh minimum height
- CTA button: full width
- Text anchored to lower third

---

## FORM UX ON MOBILE

- All fields: full width (no grid layout)
- Font size minimum 16px in inputs (prevents iOS zoom)
- Label above field always (never placeholder-only)
- Tap targets for dropdowns: 48px minimum height
- Submit button: full width, 56px height
- Success state: visible in viewport without scrolling

---

## PERFORMANCE ON MOBILE

- Target: LCP under 2.5 seconds on mobile
- Hero image: serve WebP, 1200px max width for mobile
- No render-blocking scripts above fold
- Font loading: font-display: swap
- No layout shift from image loading (aspect-ratio set)

---

## MOBILE SCROLL BEHAVIOR

- Sticky nav: stays visible on scroll
- Floating CTA: appears after scrolling past hero on long pages
- No horizontal scroll at any breakpoint
- Smooth scroll to anchor links

---

## COMMON MOBILE ERRORS TO AVOID

1. Small tap targets on form elements
2. Text too close to screen edges (minimum 20px margin)
3. Images that overflow viewport width
4. CTA buttons that are too small to tap confidently
5. iOS zoom triggered by font-size under 16px in inputs
6. Layout shift when fonts load
7. Hero content hidden behind navigation on small screens
