# SHE SAID SAIL — MASTER DESIGN SYSTEM
Version: 1.0 | Status: PRODUCTION | Owner: Will Hunt

---

## COLOR SYSTEM

### Primary Palette
| Token | Hex | Usage |
|-------|-----|-------|
| `--color-navy` | `#0a2342` | Hero backgrounds, headers, footers, primary type |
| `--color-gold` | `#c9a84c` | Accents, labels, CTA borders, dividers |
| `--color-gold-light` | `#e8d5a3` | Soft accents, hover states |
| `--color-cream` | `#f4f1ec` | Page backgrounds, section alternates |
| `--color-white` | `#ffffff` | Card backgrounds, text on dark |
| `--color-stone` | `#f9f6f0` | Detail block backgrounds |

### Type Colors
| Token | Hex | Usage |
|-------|-----|-------|
| `--color-text-primary` | `#0a2342` | Headings, key copy |
| `--color-text-body` | `#555555` | Body paragraphs |
| `--color-text-muted` | `#999999` | Labels, captions, supporting text |
| `--color-text-inverse` | `#ffffff` | Text on navy |

---

## TYPOGRAPHY SYSTEM

### Font Stack
- **Serif (headings, display):** Georgia, 'Times New Roman', serif
- **Sans (labels, meta, captions):** 'Helvetica Neue', Arial, sans-serif

### Type Scale
| Level | Size | Weight | Tracking | Usage |
|-------|------|--------|----------|-------|
| `display-xl` | 48–56px | 300 | 0.5px | Hero headline (desktop) |
| `display-lg` | 36–44px | 300 | 0.5px | Hero headline (mobile) |
| `h1` | 32px | 400 | 0 | Page H1 |
| `h2` | 26px | 400 | 0 | Section headings |
| `h3` | 20px | 400 | 0 | Sub-section headings |
| `h4` | 16px | 600 | 0 | Card titles |
| `label` | 11–12px | 700 | 3–4px | Eyebrow text, ALL CAPS |
| `body-lg` | 18px | 400 | 0 | Intro paragraphs |
| `body` | 15–16px | 400 | 0 | Standard body |
| `body-sm` | 13–14px | 400 | 0 | Captions, detail |
| `legal` | 11px | 400 | 0.5px | Footer, disclaimers |

### Hierarchy Rules
- One H1 per page, always
- Section labels: UPPERCASE, tracked, gold color, 11–12px
- Headings: sentence case, no all-caps for anything above label level
- Body: 1.7–1.9 line height
- No orphaned single words at end of headings

---

## SPACING SYSTEM

| Token | Value | Usage |
|-------|-------|-------|
| `--space-2` | 8px | Micro gaps |
| `--space-3` | 12px | Tight gaps |
| `--space-4` | 16px | Standard gaps |
| `--space-6` | 24px | Medium gaps |
| `--space-8` | 32px | Section sub-gaps |
| `--space-12` | 48px | Section padding (mobile) |
| `--space-16` | 64px | Section padding (tablet) |
| `--space-24` | 96px | Section padding (desktop) |
| `--space-32` | 128px | Hero padding |

### Section Rhythm
- Hero: 96–128px vertical padding
- Standard sections: 64–96px vertical padding
- Tight sections: 48–64px vertical padding
- Mobile reduces all by ~30%

---

## GRID SYSTEM

| Breakpoint | Columns | Gutter | Max Width |
|-----------|---------|--------|-----------|
| Mobile (<768px) | 1 | 16px | 100% |
| Tablet (768–1024px) | 2 | 24px | 100% |
| Desktop (>1024px) | 12 | 32px | 1200px |

---

## COMPONENT STANDARDS

### Buttons
- **Primary:** Gold background (#c9a84c), navy text, 14px, tracked, no border-radius or 2–4px max
- **Secondary:** Transparent, gold border 1.5px, gold text
- **Ghost:** No border, navy text, underline on hover
- Minimum tap target: 48px height
- Padding: 16px 40px (desktop), 14px 28px (mobile)
- Letter spacing: 1.5–2px
- Text: sentence case for primary, uppercase for label CTAs

### Cards
- Background: white
- Border: none or 1px solid rgba(201,168,76,0.15)
- Border-radius: 4–6px
- Shadow: 0 2px 20px rgba(10,35,66,0.06)
- Padding: 32–40px

### Dividers
- Gold rule: 1–2px, width 60–80px, centered
- Full-width rule: 1px, rgba(201,168,76,0.2)

### Form Inputs
- Border: 1px solid #ddd
- Focus border: 1px solid #c9a84c
- Border-radius: 4px
- Padding: 12–14px
- Font: Georgia, serif
- Label: uppercase, 11px, tracked, #666

---

## IMAGE STANDARDS

### Hero Images
- Min 1600px wide
- Aspect ratio: 16:9 desktop, 4:3 or portrait mobile
- Overlay: linear-gradient, navy 0.3–0.5 opacity
- Alt text: descriptive, scene-based, never "photo of yacht"

### Content Images
- Warm, golden-hour lighting preferred
- No stock photography feel
- Natural interactions, not posed luxury
- Champagne pours, golden light, relaxed confidence

### Art Direction Priority
1. Emotion and atmosphere first
2. Group dynamic and hosting moments
3. Vessel as background, not foreground

---

## ANIMATION STANDARDS

- No auto-play video with sound
- Fade-in on scroll: 0.4s ease, opacity 0 to 1
- Hover transitions: 0.2s ease
- No bouncing, spinning, or distracting motion
- Mobile: reduce or eliminate scroll animations for performance
