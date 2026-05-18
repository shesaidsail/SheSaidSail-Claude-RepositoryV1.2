# SHE SAID SAIL
# MASTER DESIGN SYSTEM

STATUS: PRODUCTION
VERSION: v1.0
APPLIES TO: All web pages — shesaidsail.com

---

## COLOR TOKENS

| Token | Hex | Usage |
|-------|-----|-------|
| --sss-navy | #0a2342 | Primary backgrounds, headings, CTAs |
| --sss-gold | #c9a84c | Accents, labels, borders, hover states |
| --sss-cream | #f9f6f0 | Section backgrounds, cards |
| --sss-linen | #f4f1ec | Page background, email backgrounds |
| --sss-white | #ffffff | Cards, modal backgrounds |
| --sss-text-primary | #1a1a1a | Body copy, primary text |
| --sss-text-muted | #666666 | Supporting text, captions |
| --sss-text-light | #999999 | Labels, metadata |
| --sss-rose | #d4a5a5 | Rose Day Club accent only |
| --sss-divider | #e5e0d8 | Section dividers, borders |

---

## TYPOGRAPHY

### Typeface Stack

Primary serif (headlines): Georgia, 'Times New Roman', serif
Primary sans (body, UI): -apple-system, BlinkMacSystemFont, 'Helvetica Neue', sans-serif
Accent (caps labels): inherit sans, tracked uppercase

### Scale

| Role | Size | Weight | Line Height | Letter Spacing |
|------|------|--------|-------------|----------------|
| Hero headline | 52–64px / 36–44px mobile | 300 | 1.1 | -0.02em |
| Section headline | 36–44px / 28–34px mobile | 300 | 1.2 | -0.01em |
| Sub-headline | 22–26px / 18–22px mobile | 400 | 1.3 | 0 |
| Body large | 18px / 16px mobile | 400 | 1.8 | 0 |
| Body standard | 15–16px | 400 | 1.7 | 0 |
| Label caps | 11px | 500 | 1 | 0.25em |
| Caption | 13px | 400 | 1.5 | 0 |

### Rules

- Headlines always serif, light weight (300)
- Body always sans-serif
- All-caps labels: 10–11px, letter-spacing 0.2–0.3em, uppercase
- No bold headlines
- No italic except for gold signature sign-offs
- No decorative typefaces

---

## SPACING SYSTEM

Base unit: 8px

| Token | Value | Usage |
|-------|-------|-------|
| --space-xs | 8px | Tight inline gaps |
| --space-sm | 16px | Component internal padding |
| --space-md | 24px | Card padding |
| --space-lg | 40px | Section internal spacing |
| --space-xl | 64px | Section top/bottom padding |
| --space-2xl | 96px | Large section breaks |
| --space-3xl | 128px | Hero padding |

Mobile: divide xl+ values by 1.4–1.6

---

## COMPONENT STANDARDS

### Buttons

Primary CTA:
- Background: #0a2342
- Text: #ffffff
- Border: none
- Padding: 16px 36px
- Border-radius: 2px
- Font: 11px uppercase, 0.2em letter-spacing
- Hover: background #c9a84c, text #0a2342, transition 0.2s

Secondary CTA:
- Background: transparent
- Text: #0a2342
- Border: 1px solid #0a2342
- Same padding/typography as primary
- Hover: background #0a2342, text #ffffff

Ghost CTA (on dark backgrounds):
- Background: transparent
- Text: #ffffff
- Border: 1px solid rgba(255,255,255,0.5)
- Hover: border-color #c9a84c, text #c9a84c

### Dividers

Gold rule: 40px wide, 1px, color #c9a84c — used in section openers
Full-width divider: 1px solid #e5e0d8

### Cards

Background: #ffffff or #f9f6f0
Border: none (use shadow sparingly: 0 2px 20px rgba(10,35,66,0.06))
Border-radius: 4px
Padding: 40px (desktop), 28px (mobile)

---

## GRID SYSTEM

Max content width: 1200px
Max text width: 760px
Gutters: 32px desktop, 20px tablet, 16px mobile
Columns: 12-column grid
Side padding mobile: 20px minimum

---

## IMAGERY STANDARDS

- Always full-width heroes: 100vw, min-height 75vh
- Images should feel natural, not staged
- Warm golden light preferred
- No stock photography feel
- Alt text: descriptive, brand-appropriate, no keyword stuffing
- Loading: lazy below fold, eager above fold
- Format: WebP preferred, JPEG fallback

---

## ANIMATION

- Transitions: 0.2s ease (UI states), 0.35s ease (reveals)
- No bounce, no spring, no aggressive motion
- Fade-in on scroll: opacity 0 to 1, translate 20px to 0
- No parallax on mobile
- Respect prefers-reduced-motion

---

## ACCESSIBILITY

- Color contrast minimum: 4.5:1 body, 3:1 large text
- Focus rings: 2px solid #c9a84c, offset 2px
- All images have meaningful alt text
- Forms: visible labels, never placeholder-only
- Buttons: minimum 44x44px touch target on mobile
- Headings: logical H1 > H2 > H3 hierarchy per page
