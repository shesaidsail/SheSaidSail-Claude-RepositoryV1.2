# She Said Sail — Page Performance Notes
**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul

---

## CURRENT STATE

The homepage loads a significant amount of JavaScript that is not used on that page.
This affects Core Web Vitals (LCP, TBT, CLS), which in turn affects:
- Google Search ranking
- Perceived load quality for luxury visitors on iPhone
- First impression of operational polish

---

## SCRIPTS LOADING ON HOMEPAGE UNNECESSARILY

| Script | Reason Loaded | Needed on Homepage? |
|---|---|---|
| MetForm / cute-alert.js | Contact form plugin | No — no form on homepage |
| MetForm Pro repeater.js | Form repeater fields | No |
| OWL Carousel | Carousel plugin | No |
| SuperSlides | Slide plugin | No — Elementor handles slideshow |
| ElementsKit widget scripts | Addons plugin | Possibly partial |
| GUM Elementor Addon | Price table addon | No |
| jQuery Migrate | Legacy jQuery shim | Likely removable |

---

## RECOMMENDED FIXES

### Option A: Conditional Script Loading (Developer Required)

In your child theme's `functions.php`, dequeue scripts on the homepage
when they are not needed:

```php
function sss_dequeue_unused_homepage_scripts() {
    if ( is_front_page() ) {
        wp_dequeue_script( 'cute-alert' );
        wp_dequeue_script( 'metform-pro-repeater' );
        wp_dequeue_script( 'gum-elementor-addon' );
        wp_dequeue_script( 'owl.carousel' );
        wp_dequeue_script( 'superslides' );
    }
}
add_action( 'wp_enqueue_scripts', 'sss_dequeue_unused_homepage_scripts', 100 );
```

### Option B: SiteGround Optimizer (No Developer Required)

SiteGround Optimizer (already installed) has an "Exclude Scripts Per Page" feature.
1. Visit the homepage while logged in
2. Open SiteGround Optimizer in the admin bar
3. Under "Exclude from Minification/Combination" add the script URLs listed above

### Option C: Perfmatters Plugin

A lightweight performance plugin that adds per-page script exclusion via a UI.
No code required. Recommended for non-technical management.

---

## IMAGE OPTIMIZATION

Current issue: Experience card images load at 2560px width regardless of display size.
`sizes="(max-width: 2560px) 100vw, 2560px"` is too broad.

Recommended `sizes` for experience cards (displayed at ~280px on desktop):
```html
sizes="(max-width: 767px) 100vw, (max-width: 1200px) 50vw, 25vw"
```

This is controlled in the Elementor loop template (loop item ID 6715).
Elementor Pro does not expose `sizes` directly but SiteGround Optimizer
handles this via its lazy loading and WebP conversion.

---

## WEBP CONVERSION

SiteGround Optimizer (already active) handles WebP conversion.
Verify in SiteGround dashboard that WebP is enabled for all upload directories.

---

## CORE WEB VITALS TARGET

| Metric | Current Estimate | Target |
|---|---|---|
| LCP (Largest Contentful Paint) | 3.5s+ (estimated) | Under 2.5s |
| TBT (Total Blocking Time) | 400ms+ (estimated) | Under 200ms |
| CLS (Cumulative Layout Shift) | Low (Elementor handles) | Under 0.1 |

The biggest LCP gain comes from ensuring the hero slideshow first image loads with `fetchpriority="high"` (already present on the first logo image — verify it applies to the slideshow background too).

---

## FONT LOADING

Three Google Fonts families are loaded: Cormorant Garamond, Inter, Playfair Display.
These are connected via Elementor's font loader with `display=swap`.
This is already correctly configured. No changes needed.
