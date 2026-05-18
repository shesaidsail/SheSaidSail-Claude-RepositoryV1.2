# She Said Sail: Master Mobile UX System
Version: 1.0
Last Updated: 2026-05-18

---

## 1. MOBILE PHILOSOPHY

The mobile experience is not a scaled-down version of the desktop. It is a carefully considered sequence of emotional moments on a small canvas. Every element earns its place. The woman opening the She Said Sail site from a link in her group chat is making a judgment in seconds: does this feel right? The mobile experience must answer that question with the same clarity and warmth as the full-site experience. That means typography that breathes even at small scale, touch targets that never require a second tap, a hero that fills the screen with the right feeling, and a booking flow that never feels like a chore. Refinement on mobile is not a feature. It is the standard.

---

## 2. TARGET DEVICES AND VIEWPORTS

### Primary Targets

These devices represent the majority of She Said Sail mobile traffic. Every layout decision must be verified at these dimensions.

| Device | Viewport Width |
|---|---|
| iPhone 15 | 390px |
| iPhone 14 Pro | 393px |

### Secondary Targets

| Device | Viewport Width |
|---|---|
| iPhone SE 3rd Generation | 375px |
| iPhone 14 Plus / 15 Plus | 428px |
| Samsung Galaxy S23 | 360px |
| Google Pixel 7 | 412px |

### Minimum Supported Viewport

- 320px: the site must not break at this width. No horizontal scrolling, no overflow, no clipped content.

### Required Test Breakpoints

Always test at: 375px, 390px, 428px before any new page or section goes live. These three widths cover the most common real-world usage.

---

## 3. TYPOGRAPHY SCALING

Typography must remain legible, proportional, and emotionally effective at every mobile size. The goal is not to shrink desktop type. It is to find the right size for the canvas.

| Element | Desktop Size | Mobile Size | Hard Minimum | Notes |
|---|---|---|---|---|
| Hero H1 | 82px | 46px | 40px | Never below 40px at any supported viewport |
| Hero H1 Italic (Playfair accent) | 82px | 46px | 40px | Same scaling as H1, always gold |
| Section Heading | 46px | 34px | 30px | Used for all major section titles |
| Card Heading | 22px | 20px | 18px | Only reduce below 20px if viewport is below 375px |
| Pull Quote / Testimonial | 22-26px | 19px | 17px | Readability critical for social proof sections |
| Body Text | 15-16px | 15px | 14px | Never below 14px. 15px preferred. |
| Body Small (card descriptions) | 13px | 13px | 13px | Unchanged |
| Eyebrow / Label | 10px | 10px | 10px | Unchanged. Already optimized for small scale. |
| CTA Button | 11px | 11px | 11px | Unchanged. Letter-spacing provides legibility. |
| Bottom CTA Heading | 50px | 34px | 30px | Large CTAs scale down to match section padding |
| Nav Link | 12px | 14px | 14px | Increase slightly on mobile for tap-target clarity |
| Footer Link | 13px | 13px | 13px | Unchanged |

### Line-Height on Mobile

Do not reduce line-height on mobile to compensate for smaller type. The same line-height values from desktop apply:
- Body: 1.75-1.85
- Headings: 1.0-1.18
- Card descriptions: 1.7

Generous line-height is part of the brand's calm, unhurried feeling. Tighter line-height makes the text feel rushed.

---

## 4. SPACING RULES ON MOBILE

Spacing on mobile is reduced proportionally but never eliminated. Compressed spacing signals low quality. Maintain the feeling of breathing room within the tighter canvas.

| Property | Desktop Value | Mobile Value | Notes |
|---|---|---|---|
| Section vertical padding | 96px | 64px | Top and bottom of every major section |
| Section horizontal padding | 40px | 24px | Never below 20px |
| Card gap | 28px | 18px | Gap in card stacks |
| Hero min-height | 88vh | 92vh | Slightly taller on mobile to fill the screen |
| Component gap within sections | 28-40px | 20-28px | Between sub-elements |
| Margin below eyebrow | 16px | 16px | Unchanged |
| Margin below section heading | 24px | 20px | Slightly reduced |
| Bottom CTA section padding | 96px | 64px | Same as standard section reduction |
| Logo width | 116px | 86px | Reduced to preserve header space |
| CTA button padding | 17px 36px | 15px 24px | Slightly reduced horizontal padding |

### Full-Width Buttons on Mobile

On viewports below 480px, all CTA buttons must expand to full width. This increases tap surface area and eliminates the awkward half-width button that appears centered in a narrow column.

```css
@media (max-width: 479px) {
  .sss-btn {
    width: 100%;
    text-align: center;
  }
}
```

---

## 5. TOUCH TARGET RULES

Poor touch targets are the most common cause of mobile frustration on luxury brand sites. They force users to retry interactions, which destroys the premium feeling immediately.

### Minimum Sizes

| Element | Minimum Size | How to Achieve |
|---|---|---|
| Buttons (all types) | 44x44px | Minimum padding, never a decorative-only area |
| Navigation links | 44px height | Add 12px vertical padding minimum |
| Form inputs | 48px height | Required for iOS tap target compliance |
| Submit buttons | 48px height, full width on mobile | Full-width eliminates the side-gap problem |
| Card tap area | Entire card surface | Wrap entire card in `<a>` tag |
| Occasion pills / tags | 36px height minimum | Include vertical padding in pill design |
| Footer links | 36px height | Add padding, do not rely on font size alone |
| Close button (modals, nav) | 44x44px | Ensure the invisible tap area meets minimum even if icon is smaller |

### Spacing Between Targets

Never place two tappable elements within 8px of each other. When targets are adjacent, increase spacing or ensure the tap areas do not overlap.

### Never Rely on Hover States for Mobile

Any interaction that is only triggered by hover does not exist on mobile. All content, labels, or state changes that currently appear on hover must be visible by default or triggered by tap.

---

## 6. CARD STACKING RULES

Cards transition from multi-column grids on desktop to single-column stacks on mobile. This sequence must be smooth and each breakpoint must feel intentional, not like a layout failure.

| Viewport | Column Count | Notes |
|---|---|---|
| Desktop (1024px+) | 3 or 4 columns | Dependent on content type |
| Tablet (768-1023px) | 2 columns | Clean two-up layout |
| Mobile (below 767px) | 1 column | Full-width stack |

### Card Dimensions on Mobile

- Image height: 240px (reduced from 272px desktop)
- Card width: 100% of section container minus horizontal padding
- Card padding (content area): 20px (reduced from 24px desktop)

### Card Order on Mobile

When cards stack to a single column, the visual order should match the logical priority. If the design uses CSS Grid with `order` properties for desktop layout, verify the mobile stacking order is correct.

---

## 7. NAVIGATION ON MOBILE

### Burger Menu Behavior

- Burger menu icon is present below 1024px
- Icon size: 24x24px minimum visible icon, 44x44px tap target
- Opens a full-height overlay panel or slide-in panel from the right or top
- Overlay panel background: white at high opacity (0.98) with backdrop blur
- All nav links visible in a single scroll within the panel (never requires scrolling to reach a link)
- Close button: visible and prominent, 44x44px tap target

### Logo During Mobile Nav

- Logo remains visible in the top-left corner while the burger menu is open
- Do not hide the logo to make room for the open nav. The panel layers over or beside the logo area.

### Auto-Close on Link Tap

When a navigation link is tapped, the mobile menu closes automatically before navigating to the destination. This is handled in JavaScript by listening for tap events on nav links and triggering the menu close before allowing the href to navigate.

### CTA Button in Mobile Navigation

The primary CTA button (inquiry or booking) must remain accessible in the mobile navigation. Place it:
- As the last item in the mobile nav list, visually separated
- Or in the header itself, visible even when the burger menu is closed (if viewport width allows)

Never hide the primary CTA in mobile view. It is the most important interactive element on the page.

---

## 8. FORM FIELDS ON MOBILE

Mobile form experience is where most site conversion happens and most luxury brands fail. These rules prevent the most common friction points.

### Input Specifications

| Property | Value | Reason |
|---|---|---|
| Font size | 16px minimum | Below 16px triggers iOS auto-zoom on focus, which is disorienting |
| Height | 48px minimum | Tap target compliance and visual comfort |
| Border-radius | 4px | Consistent with design system |

### Layout Rules

- All form fields: single column on mobile. Never side-by-side inputs at viewports below 768px.
- This applies to: first name/last name pairs, phone/email pairs, date/time pairs. Stack them vertically.

```css
@media (max-width: 767px) {
  .sss-form-row {
    flex-direction: column;
  }
  .sss-form-row .sss-field {
    width: 100%;
  }
}
```

### Textarea

- Minimum 6 visible rows on mobile
- Do not set a fixed height that makes the textarea too small to read what was typed

### Select Elements

- Use native iOS/Android select pickers for dropdown fields where possible
- Custom styled dropdowns require significantly more testing and are prone to accessibility issues on mobile
- If a custom dropdown is used, ensure it passes through to the native select for mobile viewports

### Submit Button

- Full width on mobile
- Minimum height 48px
- Text remains centered
- Never place the submit button too close to the last input field. 16px minimum gap.

### Hidden Fields

- Hidden fields must have `type="hidden"` and no visible presence in the layout
- Never rely on `display: none` for fields that might affect layout on some mobile browsers

### Error Messages

- Appear below the relevant field immediately after blur or on submit attempt
- Font: Inter 13px
- Color: `rgba(207,46,46,0.8)`
- Never use tooltips or popups for error messages on mobile. Inline errors only.
- Scroll to the first error field automatically when a form fails validation on submit

---

## 9. SOCIAL PROOF ON MOBILE

The testimonials section is a high-value section for conversion. On mobile, it collapses from a multi-column layout to a readable single-column stack.

### Layout Transition

| Viewport | Layout |
|---|---|
| Desktop (1024px+) | 3-column grid |
| Tablet (768-1023px) | 2-column grid |
| Mobile (below 767px) | 1-column stack |

### Quote Card on Mobile

| Property | Desktop Value | Mobile Value |
|---|---|---|
| Card padding | 40px 32px | 32px 24px |
| Quote text size | 19px | 17px |
| Quote text font | Cormorant Garamond, 400 italic | Unchanged |
| Attribution font | Inter 13px | Unchanged |
| Attribution color | `--sss-muted` | Unchanged |

### Stars or Rating Indicators

If star ratings are used, ensure star icons are at least 16px each with 4px spacing. Do not render stars below 12px on mobile.

---

## 10. EMAIL CAPTURE ON MOBILE

The email capture section (newsletter, waitlist, or inquiry prompt) must work clearly on the narrowest supported viewports.

### Layout

- Desktop: inline row with input and button side by side
- Mobile: vertical stack with input on top, button below

### Border-Radius on Mobile Stack

When the input and button stack vertically on mobile, adjust border-radius so they read as a unified unit:

```css
@media (max-width: 479px) {
  .sss-email-input {
    border-radius: 4px 4px 0 0;
    border-bottom: none;
  }
  .sss-email-submit {
    border-radius: 0 0 4px 4px;
    width: 100%;
  }
}
```

### Section Padding on Mobile

Section containing email capture: `64px 24px` (top/bottom, left/right).

---

## 11. HERO ON MOBILE

The hero section is the most critical piece of real estate on mobile. It fills most of the initial viewport and makes the first emotional impression.

### Image Considerations

- The hero image crop must be reviewed at 390px width before going live
- Key subjects (people, faces, the meaningful part of the scene) must be visible at this crop
- If the desktop image crops poorly on mobile, provide a separate mobile-specific image using the `<picture>` element:

```html
<picture>
  <source media="(max-width: 767px)" srcset="hero-mobile.webp">
  <source media="(min-width: 768px)" srcset="hero-desktop.webp">
  <img src="hero-desktop.webp" width="1440" height="900" alt="..." loading="eager">
</picture>
```

### Overlay

- Overlay opacity: unchanged at 0.36 on mobile
- Do not increase the overlay to compensate for a poorly selected mobile crop. Fix the image instead.

### Heading Behavior

- Headings stack naturally and never truncate with ellipsis
- If a heading wraps to 3 lines at 375px, reconsider the copy length or reduce font size to 42px minimum
- Never use `white-space: nowrap` on hero headings

### CTA Button

- Full width on mobile viewports below 480px
- Maintain 24px horizontal margin on either side (button fills content area, not full bleed)

### Occasion Pills

- Pills wrap naturally, never forced to a single row
- Gap between pills: 6px on mobile
- Pill height minimum: 36px including vertical padding

### Min-Height

- Hero min-height on mobile: 92vh
- This ensures the hero fills the screen on most iPhones, including those with bottom navigation bars

---

## 12. LOADING EXPERIENCE ON MOBILE

The loading experience is part of the mobile experience. A blank screen or flash of unstyled content undermines the premium feeling before the first interaction.

### Above-the-Fold Target

All content in the initial viewport must be rendered and visible within 2.5 seconds on a standard 4G connection. This corresponds directly to the LCP target in `master-performance-standard.md`.

### Hero Image

- Compressed to under 200KB
- Preloaded using `<link rel="preload" as="image">` in the document head
- Uses `loading="eager"` (not lazy) since it is above the fold

### Font Loading

Use `font-display: swap` for all custom font declarations. This ensures body text renders in a fallback font immediately, then swaps to the loaded font when ready. This prevents invisible text during the font load window (FOIT).

```css
@font-face {
  font-family: 'Cormorant Garamond';
  src: url('cormorant-garamond.woff2') format('woff2');
  font-display: swap;
}
```

### Critical CSS

Where possible, inline the CSS required to render the header and hero section directly in a `<style>` tag in the document `<head>`. This prevents a render-blocking external stylesheet from delaying the first paint.

### Blank Screen Prevention

The page must never show a blank screen for more than 1 second. If the hero image is still loading, the overlay color and heading should already be visible. This requires:
- A background-color on the hero section (use `--sss-navy`) so the overlay color appears immediately
- Text renders via font-display swap as noted above
- The heading is in the HTML, not injected by JavaScript

### Skeleton or Placeholder States

For sections that load content dynamically (testimonials from a CMS, availability calendars), show a lightweight placeholder with the correct dimensions to prevent CLS while the content loads.

---

*This document governs all mobile UX decisions for She Said Sail web pages. The mobile experience is not secondary. It is the primary context for most She Said Sail customer interactions.*
