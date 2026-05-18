# SHE SAID SAIL
# MASTER VISUAL DIRECTION

STATUS: PRODUCTION
VERSION: v1.0

---

## VISUAL IDENTITY SUMMARY

She Said Sail's visual language is:

- naturally cinematic
- warm and golden
- composed and editorial
- emotionally present
- unhurried

Not:
- nightclub energy
- influencer maximalism
- cold luxury (white marble, harsh angles)
- stock photography genericness

---

## COLOR APPLICATION

### Navy (#0a2342)

Use for:
- Full-section dark backgrounds (CTA sections, social proof)
- Footer
- Text on light backgrounds
- Button fill

Never use for:
- More than 30% of the page
- Consecutive sections (alternate with cream/white)

### Gold (#c9a84c)

Use for:
- Section opening rules/dividers (40px x 1px)
- Label text (caps, 10–11px)
- Accent borders
- Italic signature copy
- Hover states
- Star ratings

Never use for:
- Large areas of background
- Full headlines
- Body copy

### Cream (#f9f6f0) and Linen (#f4f1ec)

Use for:
- Section backgrounds (alternating with white)
- Card backgrounds
- Quote blocks

### White (#ffffff)

Use for:
- Card backgrounds on cream sections
- Overlay text (on navy)
- Clean spacing

### Rose (#d4a5a5)

Use for:
- Rose Day Club only: subtle accent (border, label, divider)
- Never as primary brand color

---

## TYPOGRAPHY APPLICATION

### Headlines on Light Background

- Color: #0a2342 or #1a1a1a
- Weight: 300 (light)
- Style: normal (not italic for headings)

### Headlines on Dark Background

- Color: #ffffff
- Weight: 300
- Gold accent: use for sub-labels only

### Body on Light

- Color: #3d3d3d or #555555
- Line-height: 1.7–1.9

### Body on Dark

- Color: rgba(255,255,255,0.85)

---

## IMAGERY DIRECTION

### Hero Images

- Horizontal format preferred (16:9 or wider)
- Subject: women on water, celebrating, relaxed and candid
- Light: warm golden hour or bright midday on water
- Mood: joyful but composed, not chaotic
- Composition: subject left or center, space right for text

### Experience Images

- Close crops of details: glassware, deck scenes, food/beverage
- Group shots: natural interaction, candid preferred
- Color: warm tones, turquoise water when possible
- Avoid: posed group photos facing camera directly

### Overlay Treatment

- Hero: gradient overlay, bottom-weighted, navy 30–55% opacity
- Section backgrounds: minimal overlay 10–20%
- Text legibility always checked against overlay

---

## LAYOUT RHYTHM

### Alternating Backgrounds

Section 1: White
Section 2: Cream
Section 3: White
Section 4: Navy (CTA or social proof)
Section 5: White or Cream

Never: two navy sections consecutively.

### White Space Usage

White space is a luxury signal.
Give headlines room to breathe: margin-bottom 24px minimum.
Give sections room: 96px padding desktop.
Do not compress to fit more content.

---

## UI PATTERN LIBRARY

### Gold Rule

```css
.sss-divider {
  width: 40px;
  height: 1px;
  background: #c9a84c;
  margin: 0 auto 24px;
}
```

### Section Label

```css
.sss-label {
  font-size: 11px;
  letter-spacing: 0.25em;
  text-transform: uppercase;
  color: #c9a84c;
  margin-bottom: 16px;
  display: block;
}
```

### Card

```css
.sss-card {
  background: #ffffff;
  border-radius: 4px;
  padding: 40px;
  box-shadow: 0 2px 20px rgba(10,35,66,0.06);
}
```

---

## WHAT LUXURY LOOKS LIKE ON THIS SITE

- Generous negative space
- Restrained color (never more than 3 colors per section)
- Photography doing the emotional work
- Typography doing the clarity work
- CTAs that invite, not demand
- Copy that trusts the reader
- No badge-stacking ("As featured in...", "Award-winning...")
- No countdown timers
- No pop-ups during content reading
