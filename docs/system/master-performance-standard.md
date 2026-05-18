# She Said Sail: Master Performance Standard
Version: 1.0
Last Updated: 2026-05-18

---

## 1. WHY PERFORMANCE MATTERS FOR LUXURY BRANDS

A slow site is a trust failure. The She Said Sail customer is booking a $10,000 experience. She has a current-generation iPhone, a fast connection, and zero patience for a page that hesitates. By the time a page takes 4 seconds to load, she has already formed an opinion about the brand: that it is not as polished as it claims to be. Performance is not a technical metric. It is a hospitality signal. The first interaction a prospective guest has with She Said Sail is the page load. That interaction should feel as effortless and well-considered as every other part of the experience.

---

## 2. TARGET METRICS

These targets apply to all pages: homepage, experiences, and inquiry/contact. PageSpeed Insights (mobile and desktop) is the primary measurement tool.

| Metric | Target | Hard Limit | Notes |
|---|---|---|---|
| LCP (Largest Contentful Paint) | Under 2.5s | Never above 4.0s | The hero image is almost always the LCP element. Optimize it first. |
| TBT (Total Blocking Time) | Under 200ms | Never above 600ms | Caused by unused JavaScript loading synchronously on the page |
| CLS (Cumulative Layout Shift) | Under 0.1 | Never above 0.25 | Always set explicit width and height on img elements |
| FID / INP (Interaction to Next Paint) | Under 200ms | Under 500ms | Caused by main thread congestion from heavy scripts |
| PageSpeed mobile score | 65+ | Never below 50 before paid ads run | Mobile is the primary device for the target audience |
| PageSpeed desktop score | 85+ | Never below 70 | Desktop scores are typically 15-25 points higher than mobile |

### Why Mobile Scores Are the Priority

The She Said Sail target audience (women 25-45, socially driven) is predominantly mobile. A link shared in a group chat will be opened on iPhone almost every time. Desktop scores matter for credibility; mobile scores affect real decisions.

### Paid Ads Gate

Do not run paid Meta or Google ads pointing to any page with a mobile PageSpeed score below 50. Ad spend on a slow landing page produces poor conversion and wastes budget. Confirm scores before any campaign launch.

---

## 3. IMAGE OPTIMIZATION STANDARDS

Images are the single largest contributor to page weight on the She Said Sail site. The photography-driven design requires a disciplined image pipeline.

### Format

| Format | Use Case | Notes |
|---|---|---|
| WebP | All new images, all contexts | 25-35% smaller than JPEG at equivalent quality |
| AVIF | Acceptable if browser support is confirmed in analytics | Smaller than WebP but slower to encode |
| JPEG | Legacy fallback only | Do not upload new JPEGs to the site |
| PNG | Only for images requiring transparency | Never use PNG for photography |

### File Size Targets

| Image Type | Target Size | Hard Maximum |
|---|---|---|
| Hero image | 150KB | 200KB |
| Card image (272px height) | 60KB | 80KB |
| Feature/portrait image | 80KB | 120KB |
| Footer or background image | 40KB | 60KB |

### HTML Attributes

Always specify `width` and `height` attributes on all `<img>` elements. This allows the browser to reserve space before the image loads, eliminating CLS caused by images popping in and shifting the layout.

```html
<img
  src="hero-bachelorette.webp"
  width="1440"
  height="900"
  alt="Women celebrating on the deck at golden hour, She Said Sail Miami bachelorette charter"
  loading="eager"
>
```

### Lazy Loading

Apply `loading="lazy"` to all images that are not in the initial viewport. This defers their fetch until the user scrolls toward them.

```html
<img src="experience-card.webp" width="680" height="272" loading="lazy" alt="...">
```

### Hero Image Preload

The hero image must be preloaded in the document `<head>` to ensure it is fetched with high priority before the browser encounters the `<img>` tag in the DOM.

```html
<link rel="preload" as="image" href="hero-image.webp">
```

### Responsive Images with srcset

Use `srcset` for images that appear at different sizes across breakpoints. This ensures mobile users do not download a 1440px image for a 390px viewport.

```html
<img
  src="card-experience-800.webp"
  srcset="card-experience-400.webp 400w, card-experience-800.webp 800w, card-experience-1200.webp 1200w"
  sizes="(max-width: 767px) 100vw, (max-width: 1023px) 50vw, 33vw"
  width="800"
  height="272"
  loading="lazy"
  alt="..."
>
```

### Never Upload

- Original camera RAW files or any uncompressed export
- Screenshots at screen resolution passed off as photography
- Unoptimized exports directly from Lightroom or Capture One
- Images wider than 2400px for any web context

---

## 4. JAVASCRIPT STANDARDS

JavaScript is the second most common cause of slow PageSpeed scores on WordPress sites. The goal is to load only what is needed, when it is needed.

### Weight Targets

| Script Category | Target (compressed) | Notes |
|---|---|---|
| Total custom scripts | Under 150KB | All JavaScript written for She Said Sail |
| Third-party scripts per vendor | Under 50KB | GTM, Tidio, etc. each separately |
| Total page JS (all sources) | Under 400KB compressed | Including WordPress core and Elementor |

### Loading Rules

- No synchronous `<script>` tags in the `<head>` without `defer` or `async`
- All custom scripts: load deferred in the footer using `defer` attribute
- GTM: loaded asynchronously (this is standard GTM installation behavior, do not alter)
- Never add `defer` to scripts that depend on DOM-ready unless they include their own event listeners
- Polyfills for browsers with under 1% market share: do not load

### Plugin JavaScript Audit

Run a JS weight audit quarterly. The following plugins load JavaScript globally and should be reviewed:

**Currently unnecessary on the homepage (identified in performance audit):**
- MetForm: loads assets on all pages, not just pages with a MetForm form
- OWL Carousel: if not actively used, remove entirely
- SuperSlides: if not actively used, remove entirely
- ElementsKit: adds significant JS weight site-wide

See `docs/ux/performance-notes.md` for the PHP function that restricts plugin asset loading by page.

### Third-Party Script Priority

Load order priority for third-party scripts:
1. Google Fonts (preconnect only, never blocking render)
2. GTM (async in head)
3. All others: deferred, in footer

---

## 5. CSS STANDARDS

### Weight Targets

| CSS Source | Target |
|---|---|
| Custom CSS (WordPress Additional CSS) | Under 50KB |
| Per-page scoped CSS | Under 10KB per page |
| Total CSS (all sources, compressed) | Under 150KB |

### Writing Rules

- No unused CSS in the WordPress Additional CSS field. Audit quarterly and remove any styles that no longer apply to live elements.
- Minimize use of `!important`. Use it only when Elementor's specificity makes it genuinely unavoidable. Document each instance with a comment.
- Do not duplicate base Elementor styles in custom CSS. Elementor already provides padding, box-sizing, and reset styles.
- Do not load page-specific CSS globally. Scope page styles to the body class of that page:

```css
/* Good: scoped to homepage only */
.page-id-12 .sss-hero-heading {
  font-size: 82px;
}

/* Avoid: applied globally when only needed on one page */
.sss-hero-heading {
  font-size: 82px;
}
```

### Critical CSS

For significant performance improvements, inline the CSS required to render above-the-fold content (hero, header) directly in a `<style>` tag in the `<head>`. This eliminates the render-blocking penalty of loading external stylesheets for the first visible frame.

---

## 6. PLUGIN LIMITS

### Approved Plugins for She Said Sail

The following plugins are approved and should remain active:

| Plugin | Purpose |
|---|---|
| Elementor | Page builder |
| Elementor Pro | Advanced widgets, theme builder |
| Yoast SEO or RankMath | SEO meta, sitemap |
| Insert Headers and Footers | GTM, custom scripts |
| Tidio | Live chat widget |
| WP Rocket or SiteGround Optimizer | Caching, minification |
| ShortPixel or Imagify | Automatic image compression on upload |
| Wordfence | Security scanning and firewall |

### Plugins Requiring Review Before Adding

These categories introduce significant performance or maintenance risk. Any addition requires performance testing before going live:

- Form plugins beyond what is already active
- Slider or carousel plugins (load heavy JS/CSS globally)
- Popup plugins (frequently load on every page, poorly)
- Social media feed plugins (API-dependent, slow, unreliable)

### Plugins to Remove If Found Inactive

These plugins were identified as loading assets without being actively used on the live site. If confirmed unused, deactivate and delete:

| Plugin | Reason to Remove |
|---|---|
| MetForm Pro | Loads JS/CSS globally if not scoped |
| OWL Carousel | Heavy carousel library, no current use |
| SuperSlides | Legacy slider, no current use |
| GUM Elementor Addon | Unverified active use |

---

## 7. ANIMATION PERFORMANCE RULES

Poorly implemented animations cause jank, frame drops, and CLS. These rules prevent animation from becoming a performance liability.

### Properties That Are Safe to Animate

Animating these properties uses the GPU and does not trigger layout recalculation:

- `transform` (translate, scale, rotate)
- `opacity`

### Properties That Must Never Be Animated

Animating these properties triggers layout recalculation on every frame, which causes jank on mobile:

- `width`, `height`
- `top`, `left`, `right`, `bottom`
- `margin`, `padding`
- `font-size`

### will-change

Use `will-change: transform` or `will-change: opacity` sparingly. Only apply it to elements that are actively animating. Do not apply it globally or to elements that rarely animate. Excessive `will-change` usage increases GPU memory consumption.

### Concurrency Limit

Maximum 6 simultaneously animated elements on screen at any time. Stagger reveals so that not every element on a page triggers its animation at the same scroll position.

### IntersectionObserver Requirement

All scroll-triggered animations must use IntersectionObserver. Never use scroll event listeners for animation triggers. Scroll event listeners fire on every scroll frame and cause main thread congestion, raising TBT scores.

```javascript
// Correct approach
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('sss-revealed');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });

document.querySelectorAll('.sss-reveal').forEach(el => observer.observe(el));
```

---

## 8. CACHING CONFIGURATION

### Cache Headers

| Asset Type | Cache Duration | Notes |
|---|---|---|
| Images (WebP, JPEG, PNG) | 1 year | Content-addressed filenames preferred |
| CSS and JavaScript | 1 year | Version strings or hashes in filenames |
| HTML pages | 1 hour or less | Pages change more frequently |
| Fonts | 1 year | Google Fonts CDN handles this automatically |

### Server Compression

Enable GZIP or Brotli compression on all text-based assets. This reduces transfer sizes by 60-80% for CSS, JavaScript, and HTML. WP Rocket, SiteGround Optimizer, and Cloudflare all provide this automatically.

### CDN

Use a CDN for image delivery wherever the hosting environment supports it:
- WP Engine: CDN included in plan
- SiteGround: SiteGround CDN or Cloudflare
- Any provider: Cloudflare free tier is acceptable for DNS-proxied CDN delivery

Images served from a CDN are delivered from the nearest edge node, reducing latency for the primary audience (Miami, US, Caribbean travel-adjacent markets).

---

## 9. CORE WEB VITALS AUDIT SCHEDULE

### Monthly Audit Process

1. Run PageSpeed Insights on all 3 primary pages: homepage, experiences page, inquiry/contact page
2. Test mobile and desktop separately for each page
3. Record scores in `docs/ux/performance-notes.md` with the date and any notes on changes made since the last audit

### Alert Thresholds

| Condition | Action Required |
|---|---|
| Any page drops below 50 mobile | Investigate immediately. Pause any paid ads pointing to that page until resolved. |
| LCP above 4.0s on mobile | Identify LCP element and optimize. Priority: hero image size, preload status, render-blocking resources. |
| CLS above 0.25 | Audit all images for missing width/height attributes. Check for font-swap layout shifts. |
| TBT above 600ms | Audit JS load order. Check for synchronous scripts and unused plugin assets. |

### Reporting Location

All audit results are recorded in `docs/ux/performance-notes.md`. Include:
- Date of audit
- PageSpeed scores (mobile and desktop) for each page
- Any metrics in the warning or fail range
- Steps taken or planned to resolve issues

---

*This document governs performance standards for all She Said Sail web pages. Performance is treated as a hospitality quality signal, not an engineering concern in isolation.*
