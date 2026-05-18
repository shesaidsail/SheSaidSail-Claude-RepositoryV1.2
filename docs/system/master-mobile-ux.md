# SHE SAID SAIL — MASTER MOBILE UX STANDARDS
Version: 1.0 | Status: PRODUCTION | Owner: Will Hunt

---

## CORE PRINCIPLE

Mobile is the primary experience for this audience. Every design decision must work on a 375px wide screen first.

---

## TYPOGRAPHY — MOBILE

| Element | Desktop | Mobile |
|---------|---------|--------|
| Hero headline | 48–56px | 34–38px |
| Section H2 | 28–32px | 22–26px |
| Body | 16px | 16px (never reduce below 16) |
| Labels | 11px | 11px |
| CTA text | 14–15px | 15px |

Line height: 1.7–1.9 on mobile. No tighter.

---

## SPACING — MOBILE

- Section padding: 56–72px vertical
- Container side padding: 20–24px
- Stack gap between elements: 16–24px
- Between heading and paragraph: 12–16px
- Between paragraph and CTA: 24–32px

---

## TOUCH TARGETS

- Minimum tap target: 48px x 48px
- CTA buttons: full width on mobile (100%)
- Form inputs: minimum 48px height
- Nav links: 44px touch area minimum
- Icons: 44px touch area with padding

---

## HERO — MOBILE

- Height: 85–100vh
- Image: portrait or square crop (not wide landscape)
- Headline: centered, max 90% width
- CTA button: full width, centered
- No hero text smaller than 34px

---

## FORM — MOBILE

- All fields full width (100%)
- Label above field (not floating label)
- 16px font in inputs (prevents iOS zoom)
- Submit button: full width, 56px height
- Field spacing: 16px between fields
- No side-by-side fields on mobile

---

## NAVIGATION — MOBILE

- Hamburger or bottom nav
- Never more than 5 items in mobile nav
- Active state clearly visible
- Logo visible always

---

## IMAGE — MOBILE

- Serve mobile-optimized images (WebP preferred)
- Hero image: portrait or square orientation on mobile
- Avoid wide landscape crops that hide the subject
- Loading: lazy load below fold

---

## PERFORMANCE — MOBILE

- First Contentful Paint target: under 2.5s
- No render-blocking scripts in head
- Defer all non-critical JS
- Compress all images: JPEG/WebP under 200kb for standard, under 400kb for hero
- Minimize custom fonts: 2 weights maximum

---

## SCROLL AND INTERACTION

- Sticky CTA bar on mobile (optional): gold bar at bottom with "Reserve Your Date" when user is past hero
- No horizontal scroll anywhere
- No overlapping elements on small screens
- Adequate section breaks so content doesn't feel compressed

---

## FORM UX — MOBILE SPECIFIC

- Date picker: use native date input (not custom JS calendar) on mobile
- Phone field: `type="tel"` to trigger numeric keyboard
- Email field: `type="email"` to trigger email keyboard
- Guest count: `type="number"` with `min` and `max` attributes
- Select dropdowns: native `<select>` on mobile for best UX
- No multi-step forms on mobile without clear progress indicator

---

## ACCESSIBILITY — MOBILE

- Color contrast: 4.5:1 minimum for all text
- Focus states visible on all interactive elements
- All images have descriptive alt text
- Form fields have proper `<label>` elements
- Error messages appear adjacent to the relevant field
