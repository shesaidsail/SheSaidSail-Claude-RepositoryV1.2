# SHE SAID SAIL
# MASTER DESIGN SYSTEM

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt
APPLIES TO: All web pages — SheSaidSail.com and MareExecutive.com

---

## BRAND PALETTE

| Token | Hex | Usage |
|-------|-----|-------|
| --sss-navy | #0a2342 | Primary background, headings, footer |
| --sss-gold | #c9a84c | Accent, CTAs, dividers, eyebrow text |
| --sss-cream | #f4f1ec | Section backgrounds, warm white fill |
| --sss-white | #ffffff | Content cards, form backgrounds |
| --sss-text | #2a2a2a | Body copy |
| --sss-muted | #6b6b6b | Secondary text, captions |
| --sss-border | #e8e3da | Subtle dividers |

---

## TYPOGRAPHY

### Type Scale

| Role | Tag | Font | Size (desktop) | Size (mobile) | Weight | Spacing |
|------|-----|------|----------------|---------------|--------|---------|
| Display | h1 | Georgia, serif | 52px | 36px | 400 | -0.5px |
| Section headline | h2 | Georgia, serif | 38px | 28px | 400 | -0.3px |
| Card headline | h3 | Georgia, serif | 26px | 22px | 400 | 0 |
| Eyebrow | span.eyebrow | System sans | 11px | 11px | 600 | 4px uppercase |
| Body | p | Georgia, serif | 17px | 16px | 400 | 0 |
| Body small | p.small | Georgia, serif | 15px | 15px | 400 | 0 |
| Caption | span.caption | System sans | 13px | 13px | 400 | 1px |
| CTA | button/a | System sans | 14px | 14px | 600 | 2px uppercase |

### Font Stack
```css
--font-serif: Georgia, 'Times New Roman', serif;
--font-sans: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
```

### Line Heights
- Display: 1.15
- Headings: 1.3
- Body: 1.8
- Tight: 1.4

---

## SPACING RHYTHM

Base unit: 8px

| Token | Value | Usage |
|-------|-------|-------|
| --space-xs | 8px | Inline gaps |
| --space-sm | 16px | Form field gaps, label spacing |
| --space-md | 24px | Card padding, small section gaps |
| --space-lg | 48px | Section padding, large gaps |
| --space-xl | 80px | Section top/bottom padding (desktop) |
| --space-2xl | 120px | Hero sections (desktop) |
| --space-mobile-section | 56px | Section top/bottom (mobile) |

---

## COMPONENT STANDARDS

### Hero Section
- Full viewport height on desktop (min 90vh)
- 70vh minimum on mobile
- Overlay: linear-gradient from navy 60% opacity to transparent
- Headline position: lower third, left-aligned
- Gold eyebrow above headline always

### CTA Buttons
- Primary: gold background, navy text, 14px uppercase, 2px letter-spacing, 52px height, 32px horizontal padding
- Secondary: transparent, gold border 1.5px, gold text
- Ghost: transparent, white border, white text (dark backgrounds only)
- Hover state: 8% brightness reduction, no jump effects
- Border-radius: 2px (almost flat, editorial)
- No rounded pill buttons. No box shadows on CTAs.

### Cards
- Background: white
- Border: 1px solid --sss-border
- Border-radius: 4px
- Padding: 32px
- Hover: subtle translate-y(-2px) with 200ms ease

### Dividers
- Thin gold rule: 1px solid #c9a84c, width 40px, centered
- Section dividers: 1px solid --sss-border, full width

### Images
- All images: object-fit cover
- Aspect ratios: Hero 16:9 or full-bleed, Cards 4:3, Portraits 3:4
- Always include descriptive alt text
- No stock photography feel. Authentic lifestyle imagery.

---

## GRID SYSTEM

- Max content width: 1200px
- Gutters: 32px desktop, 20px mobile
- Columns: 12-column grid
- Mobile breakpoint: 768px
- Tablet breakpoint: 1024px

```css
.sss-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 32px;
}
@media (max-width: 768px) {
  .sss-container { padding: 0 20px; }
}
```

---

## VISUAL DIRECTION RULES

1. Negative space is intentional. Never fill every pixel.
2. One gold accent per section maximum.
3. Images lead emotion. Copy supports.
4. No drop shadows on content cards (use border instead).
5. No gradients except on hero overlays.
6. No animations beyond subtle hover states.
7. No carousels on mobile. Stack content vertically.
8. Typography drives hierarchy more than color.

---

## ACCESSIBILITY

- Minimum contrast ratio: 4.5:1 for body text
- Focus states: visible gold outline on interactive elements
- All images have descriptive alt text
- Form labels always visible (no placeholder-only labeling)
- Touch targets minimum 48px height on mobile
- Skip navigation link on all pages

---

## BRAND TONE IN DESIGN

The visual design communicates:
- Calm confidence (white space, restrained palette)
- Editorial authority (serif typography, measured spacing)
- Premium without flash (no gradients, no glows, no loud motion)
- Warmth (cream backgrounds, gold accents)
- Human scale (readable type sizes, generous padding)
