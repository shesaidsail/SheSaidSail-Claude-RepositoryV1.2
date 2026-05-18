# She Said Sail: Master Design System
Version: 1.0
Last Updated: 2026-05-18

---

## 1. DESIGN PHILOSOPHY

Quiet luxury for She Said Sail means restraint as a form of confidence. Nothing shouts, nothing competes for attention, and nothing needs to justify itself. The design earns trust through precision: generous white space, type that breathes, and color used with intention rather than decoration. Every visual decision should carry emotional weight without spectacle, communicating that this brand understands its audience at a level most companies never reach. When a prospective guest lands on any She Said Sail page, the design itself should say: "You are already taken care of."

---

## 2. COLOR SYSTEM

### Token Reference Table

| Token | Hex / Value | Primary Usage | Never Use For |
|---|---|---|---|
| `--sss-navy` | `#1A2332` | Primary brand color, footer background, form submit buttons, section overlays | Background on small text below 13px unless contrast is verified |
| `--sss-gold` | `#DAB97E` | Eyebrow labels, divider accents, icon highlights, footer column headings, CTA fills | Body text on cream background (fails contrast), borders alone without pairing |
| `--sss-gold-deep` | `#C9A96E` | Hover states on gold elements, secondary CTA hover, text CTA hover color | Large background fills (too warm at scale) |
| `--sss-cream` | `#FAF8F3` | Page base background, section alternating background, navy-section foreground text | Text on white backgrounds (too low contrast) |
| `--sss-warm` | `#F5F0E8` | Alternate section backgrounds, form wrappers, card cluster backgrounds | Body copy color |
| `--sss-text` | `#2C2C2C` | All body copy, nav links, card descriptions, form labels, general text | On navy backgrounds without adjusting to cream |
| `--sss-muted` | `rgba(44,44,44,0.5)` | Eyebrow labels on light backgrounds, card descriptions, supporting copy | Headlines, CTAs, anything that must be read quickly |
| `--sss-border` | `rgba(218,185,126,0.22)` | Card borders, section divider lines, input borders (resting state) | Heavy structural outlines, large framing elements |

### Acceptable Foreground/Background Combinations

| Background | Acceptable Text Colors | Notes |
|---|---|---|
| White `#FFFFFF` | `--sss-text`, `--sss-navy` | Standard page sections |
| Cream `#FAF8F3` | `--sss-text`, `--sss-navy` | Alternating sections, never gold text here |
| Warm `#F5F0E8` | `--sss-text`, `--sss-navy` | Form wrappers, warm tonal sections |
| Navy `#1A2332` | `--sss-cream`, `--sss-gold` | Footer, hero overlays, major CTA sections |
| Gold `#DAB97E` | `--sss-navy` only | CTA buttons with gold fill, small labeled elements |

### Forbidden Combinations

- Gold text on cream background: insufficient contrast, fails WCAG AA
- Gold text on warm background: fails contrast at body sizes
- Muted text on navy: fails contrast entirely
- White text on gold: fails contrast for body sizes
- Navy text on black or very dark images without overlay: unverifiable contrast

### Overlay Opacity Standards

- Hero photography sections: navy overlay at `0.36` opacity
- Hard maximum for photography overlays: `0.45` opacity. Above this point, the photography loses value and the section begins to feel heavy.
- Non-hero image overlays (e.g. feature background images): `0.28` to `0.36` opacity
- Full-color navy sections (no image): no overlay needed, use the solid token

---

## 3. TYPOGRAPHY SYSTEM

### Font Roles

| Font | Variable Role | Emotion | When to Use |
|---|---|---|---|
| Cormorant Garamond | Editorial | Refined, serene, literary | All major headings, section titles, pull quotes |
| Inter | Body | Clear, modern, trustworthy | All body copy, navigation, eyebrows, CTAs, captions, form labels |
| Playfair Display | Accent | Warm, expressive, slightly indulgent | Hero italic accent lines, decorative subheadings only |

### Type Scale

| Element | Desktop Size | Mobile Size | Font | Weight | Line Height | Letter Spacing | When to Use |
|---|---|---|---|---|---|---|---|
| Hero H1 | 82px | 46px | Cormorant Garamond | 400 | 1.0 | -0.015em | Primary hero heading line, brand statement |
| Hero H1 Italic | 82px | 46px | Playfair Display | 400 italic | 1.0 | -0.015em | Second or third line of hero heading, always gold color |
| Section Heading | 46px | 34px | Cormorant Garamond | 400 | 1.18 | 0 | All major content section titles |
| Card Heading | 22px | 20px | Cormorant Garamond | 400 italic | 1.28 | 0 | Individual card or tile titles |
| Pull Quote | 22-26px | 19px | Cormorant Garamond | 400 italic | 1.5 | 0 | Testimonial text, featured callouts |
| Subheading / Lead | 18-20px | 17px | Cormorant Garamond | 400 | 1.55 | 0 | Section supporting text directly under headings |
| Body | 15-16px | 15px | Inter | 300-400 | 1.75-1.85 | 0 | All paragraph copy. Never below 14px. |
| Body Small | 13px | 13px | Inter | 400 | 1.7 | 0 | Card descriptions, secondary supporting text |
| Eyebrow / Label | 10px | 10px | Inter | 500-700 | 1.0 | 0.22-0.26em | Section eyebrows above headings. Always uppercase. |
| CTA Button | 11px | 11px | Inter | 600 | 1.0 | 0.14em | All button text. Always uppercase. |
| Caption / Legal | 11px | 11px | Inter | 400 | 1.6 | 0.04em | Footer copyright, image captions, fine print |
| Nav Link | 12px | 12px | Inter | 500 | 1.0 | 0.1em | Navigation items. Always uppercase. |

### Typography Rules

- Section eyebrows are always: 10px Inter, uppercase, letter-spacing 0.24em, using `--sss-muted` or `--sss-gold` color. Never bold, never larger.
- Decorative headings use weight 400 only. Never 700 or 800 in editorial headings.
- Body copy weight ranges from 300 (light, spacious sections) to 400 (standard). Never 500+ for paragraphs.
- The italic Playfair Display accent line in heroes always uses `--sss-gold` color. This is the single most distinctive typographic element on the site.
- Never mix Cormorant Garamond and Playfair Display in body copy. Playfair is reserved for accent lines only.

---

## 4. SPACING RHYTHM

All spacing is derived from an 8px base unit.

| Property | Desktop Value | Mobile Value | Notes |
|---|---|---|---|
| Section vertical padding | 96px | 64px | Top and bottom of every major section |
| Section inner max-width | 1100px | 100% minus 48px | Content never exceeds 1100px wide |
| Body copy max-width | 560-600px | 100% | Centered, prevents line lengths above 75 characters |
| Card gap | 28px | 18px | Horizontal and vertical gap in card grids |
| Component gap within sections | 28-40px | 20-28px | Between sub-elements within a single section |
| Margin below eyebrow | 16px | 16px | Space between eyebrow label and section heading |
| Margin below section heading | 24px | 20px | Space between heading and supporting subtext or content |
| Heading to subtext gap | 12px | 12px | Tight pairing between heading and its subtitle |
| Section horizontal padding | 40px | 24px | Side padding inside section containers |
| Button vertical padding | 17px | 15px | Internal button padding top and bottom |
| Button horizontal padding | 36px | 24px | Internal button padding left and right |

---

## 5. BUTTON AND CTA SYSTEM

### Button Variants

**Primary CTA (Gold Fill)**
- Background: `--sss-gold` (`#DAB97E`)
- Text color: `--sss-navy`
- Font: 11px Inter, weight 600, uppercase, letter-spacing 0.14em
- Padding: 17px 36px
- Border-radius: 3px
- Border: 1px solid `--sss-gold`
- Hover state: transparent background, `--sss-cream` text, border becomes `rgba(250,248,243,0.45)`
- Transition: 0.35s luxury easing

**Secondary CTA (Outlined)**
- Background: transparent
- Text color: `--sss-navy`
- Border: 1px solid `rgba(26,35,50,0.35)`
- Font: same as primary
- Hover state: `--sss-gold-deep` text color, border color upgrades to `--sss-gold-deep`
- Use when: a supporting action exists alongside a primary CTA

**Ghost CTA (Navy Section Use)**
- Background: `--sss-navy`
- Text color: `--sss-cream`
- Border: 1px solid `rgba(250,248,243,0.25)`
- Hover state: `--sss-cream` background, `--sss-navy` text
- Use when: placed on cream or warm backgrounds where navy fill creates high contrast

**Text CTA (Underline Style)**
- No padding, no border-radius, no background
- Border-bottom: 1px solid `rgba(26,35,50,0.35)`
- Text: same font as buttons, `--sss-navy` color
- Hover: `--sss-gold-deep` color, border-bottom transitions to gold-deep
- Use when: a subtle tertiary action is needed inline with copy or in a card

### Button Rules

- Never use rounded pill buttons (border-radius above 4px)
- Never use gradient fills on buttons
- Never add box-shadow to buttons
- Never use all-caps letter-spacing below 0.12em
- Maximum 2 CTAs per section. The hierarchy must be clear: one primary, one secondary or text style.
- Never use two primary (gold fill) CTAs in the same section

---

## 6. CARD SYSTEM

### Card Style Specification

| Property | Value |
|---|---|
| Border-radius | 8px |
| Border | 1px solid `rgba(218,185,126,0.1)` |
| Box-shadow | `0 2px 18px rgba(0,0,0,0.055)` |
| Background | White `#ffffff` |
| Image height (desktop) | 272px |
| Image height (mobile) | 240px |
| Image object-fit | cover |
| Card padding (content area) | 24px |
| Card heading font | Cormorant Garamond, 22px, weight 400 italic |
| Card description font | Inter, 13px, weight 400, line-height 1.7, `--sss-muted` color |

### Hover State

| Property | Value |
|---|---|
| Transform | `translateY(-5px)` |
| Box-shadow | `0 16px 44px rgba(0,0,0,0.09)` |
| Border-color | `rgba(218,185,126,0.28)` |
| Image transform | `scale(1.04)` |
| Image transition | 0.85s luxury easing |
| Card transition | 0.35s luxury easing |

### Card Usage Rules

- Always wrap the entire card in an anchor tag so the full surface is tappable
- Never clip the card heading. If text is long, allow it to wrap.
- Card images should be cropped to feature people and setting, not logo or text
- Never stack more than 4 cards per row on desktop

---

## 7. IMAGE TREATMENT

### Hero Images

- Width: 100% of viewport
- Min-height: 88vh on desktop
- Overlay: `--sss-navy` at `0.36` opacity, via pseudo-element or direct overlay div
- Position: center center, object-fit cover

### Feature and Portrait Images

- Border-radius: 8px
- Box-shadow: `0 24px 64px rgba(0,0,0,0.12)`
- Never stretch or distort aspect ratio

### Photography Rules

- Never crop faces out of frame
- Use moment-driven framing, not posed framing
- Alt text format: "Description, She Said Sail [location or occasion context]"
- Example: "Three women laughing on the deck at sunset, She Said Sail Miami bachelorette charter"

### Technical Standards

- Format: WebP preferred for all new uploads. AVIF acceptable when browser support is confirmed.
- Lazy load: all images below the fold using `loading="lazy"` attribute
- Hero image: preload using `<link rel="preload" as="image">` in the document head
- Always specify `width` and `height` attributes on `<img>` elements to prevent layout shift

---

## 8. SECTION STRUCTURE

### Standard Section Anatomy

Every content section follows this structure:

1. Eyebrow label (optional): 10px Inter, uppercase, letter-spacing 0.24em, muted or gold
2. Section heading: Cormorant Garamond, appropriate scale for context
3. Subtext (optional): 15-16px Inter or Cormorant Garamond lead, centered or left-aligned
4. Content: cards, copy blocks, images, testimonials, etc.
5. CTA (optional): maximum 1 primary CTA per section, 1 supporting secondary

### Eyebrow and Divider Treatment

- Eyebrow always appears above the heading with 16px margin below it
- When flanked by dividers: gold lines, `0.55` opacity, `22px` wide, centered with the label
- Dividers are decorative only. Never use them as structural separators.

### Background Alternation

| Section Type | Background |
|---|---|
| Primary content sections | White `#ffffff` |
| Alternate sections | `--sss-cream` or `--sss-warm` |
| Major CTA sections | `--sss-navy` |
| Social proof sections | `--sss-navy` or `--sss-warm` depending on visual weight |
| Form sections | `--sss-warm` or white |

### CTA Rules per Section

- Maximum 2 CTAs per section
- Never show two competing primary CTAs
- If a section has a secondary CTA, it must visually defer to the primary

---

## 9. ANIMATION STANDARDS

### Scroll Reveal

- Start state: `opacity: 0`, `transform: translateY(18px)`
- End state: `opacity: 1`, `transform: translateY(0)`
- Duration: `0.75s`
- Easing: `cubic-bezier(0.25, 0.46, 0.45, 0.94)` (luxury easing)
- Trigger: IntersectionObserver at 15% visibility threshold

### Stagger Delays for Sequential Elements

| Position | Delay |
|---|---|
| First element | 0s (or base delay) |
| Second element | +0.1s |
| Third element | +0.22s |
| Fourth element | +0.36s |
| Beyond fourth | +0.12s increments, capped at 0.6s total |

### Header Behavior

- Box-shadow appears after 80px of scroll
- Transition for shadow: 0.35s luxury easing
- Class `.sss-header-scrolled` is added by JS at the 80px threshold

### Motion Rules

- Never animate: bouncing, pulsing, spinning, aggressive scaling
- Never use scroll event listeners for animation triggers. Use IntersectionObserver.
- Autoplay video or looping animation must have a pause control
- `prefers-reduced-motion`: when this media query is active, remove all transforms and transitions. Opacity fades are acceptable at reduced or zero duration.

---

## 10. FORM STANDARDS

### Input Field Specification

| Property | Value |
|---|---|
| Height | 48px minimum |
| Border | 1px solid `rgba(26,35,50,0.22)` |
| Border on focus | 1px solid `--sss-gold-deep` |
| Border on error | 1px solid `rgba(207,46,46,0.5)` |
| Border-radius | 4px |
| Font | Inter, 14px, weight 400 |
| Placeholder color | `rgba(44,44,44,0.32)` |
| Font size (mobile) | 16px minimum (prevents iOS auto-zoom) |

### Form Wrapper

- Background: white `#ffffff`
- Padding: 48px
- Border-radius: 8px
- Box-shadow: `0 4px 24px rgba(0,0,0,0.07)`

### Submit Button

- Follows the Ghost CTA style or Primary CTA style depending on background
- On white or cream backgrounds: use Primary (gold fill)
- Minimum height: 48px
- Full width on mobile viewports

### Form Accessibility

- Every input must have an associated `<label>` or `aria-label`
- Error messages appear below the field, 13px Inter, `rgba(207,46,46,0.8)`
- Success state: field border transitions to `rgba(34,139,34,0.5)`
- Do not disable the submit button until after a failed submission

---

## 11. NAVIGATION STANDARDS

### Desktop Navigation

| Property | Value |
|---|---|
| Logo width | 116px |
| Nav link font | 12px Inter, weight 500, uppercase, letter-spacing 0.1em |
| Nav link color | `--sss-navy` |
| Nav link hover color | `--sss-gold-deep` |
| Nav link hover transition | 0.2s |
| CTA button in nav | Primary style, reduced: 11px, padding 12px 24px |

### Sticky Header

- `backdrop-filter: blur(12px)`
- Background: `rgba(255,255,255,0.97)`
- Box-shadow on scroll: `0 2px 24px rgba(0,0,0,0.08)`, triggered at 80px
- Class: `.sss-header-scrolled` added by JS

### Mobile Navigation

- Burger menu visible below 1024px
- Opens full-height overlay or slide-in panel
- Logo remains visible in top-left while menu is open
- Nav closes automatically when any link is tapped
- CTA button remains accessible within mobile menu

---

## 12. FOOTER STANDARDS

### Footer Specification

| Property | Value |
|---|---|
| Background | `--sss-navy` |
| Logo width | 108px |
| Logo opacity | 0.9 |
| Column heading font | 9px Inter, uppercase, letter-spacing 0.26em |
| Column heading color | `--sss-gold` |
| Link font | 13px Inter |
| Link color | `rgba(250,248,243,0.55)` |
| Link hover color | `--sss-cream` |
| Contact icon color | `--sss-gold` at 0.65 opacity, hover to 1.0 |
| Copyright font | 11px Inter |
| Copyright color | `rgba(250,248,243,0.28)` |
| Bottom bar background | `rgba(0,0,0,0.18)` |
| Bottom bar border-top | `rgba(255,255,255,0.06)` |

---

## 13. ACCESSIBILITY STANDARDS

### Color Contrast Requirements

| Context | Minimum Ratio | Standard |
|---|---|---|
| Body text on white or cream | 4.5:1 | WCAG AA |
| Large text (18px+ regular, 14px+ bold) on background | 3:1 | WCAG AA |
| Interactive element labels | 4.5:1 | WCAG AA |
| Placeholder text | Not required to pass (supplementary only) | Best practice: 3:1 |

### Focus States

- All interactive elements: 2px solid `--sss-gold`, `outline-offset: 3px`
- Never remove focus outlines with `outline: none` unless a visible custom alternative is applied
- Focus styles must be visible on both light and dark backgrounds

### Tap Targets

- Minimum size: 44x44px for all buttons, links, and interactive controls
- Minimum spacing between adjacent tap targets: 8px

### Semantic HTML Requirements

- Heading hierarchy must be logical: H1 appears once per page, followed by H2, H3 in order
- All images must have non-empty `alt` attributes. Decorative-only images use `alt=""`
- All form inputs must have associated `<label>` elements or `aria-label` attributes
- Navigation landmarks: use `<nav>`, `<main>`, `<footer>`, `<header>` appropriately

### Skip Navigation

- A skip link to `#main-content` must be the first focusable element on every page
- It may be visually hidden until focused: `position: absolute`, moves to visible position on `:focus`

### Reduced Motion

- Wrap all transforms and transitions in a media query check
- When `prefers-reduced-motion: reduce` is active: remove `translateY` effects, set transition durations to 0 or near-0
- Opacity-only fades are acceptable for users who prefer reduced motion

---

*This document governs all design decisions for She Said Sail web properties. Any deviation from these standards requires documented justification and design lead approval.*
