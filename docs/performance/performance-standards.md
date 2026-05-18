# She Said Sail: Performance Standards

**Version:** 1.0
**Date:** 2026-05-18
**Authority:** Development Lead / Site Owner
**Stack:** WordPress 6.9.4 + Elementor 4.0.3 + Hello Elementor theme
**Hosting:** WordPress managed hosting, no CDN at launch

---

## LIGHTHOUSE TARGETS

These are the minimum acceptable scores for every page on She Said Sail. Scores are measured using Lighthouse in Chrome DevTools or via PageSpeed Insights (pagespeed.web.dev) on the live URL, simulated mobile, throttled connection.

| Category | Minimum Acceptable | Target |
|---|---|---|
| Performance | 90 | 95+ |
| Accessibility | 95 | 100 |
| Best Practices | 95 | 95+ |
| SEO | 100 | 100 |

A score below the minimum acceptable threshold on any page is a launch blocker. Accessibility and SEO at target is required before launch. Performance at target is a post-launch optimization goal if the minimum is met.

---

## CORE WEB VITALS TARGETS

Core Web Vitals are measured at the 75th percentile of real user sessions in Google Search Console. Lab data from Lighthouse is used as a proxy during development. She Said Sail targets are tighter than Google's "Good" thresholds because the brand experience begins at page load. A luxury experience that jitters or loads slowly undermines trust before a word is read.

| Metric | Google "Good" Threshold | She Said Sail Target | Rationale |
|---|---|---|---|
| LCP (Largest Contentful Paint) | Under 2.5s | Under 2.0s | Hero image is the first brand impression. It must load fast. |
| INP (Interaction to Next Paint) | Under 200ms | Under 150ms | Quick reply buttons and CTAs must feel instant. |
| CLS (Cumulative Layout Shift) | Under 0.1 | Under 0.05 | Any perceived jitter undermines a premium brand feeling. |

**Measurement cadence:**
- Before launch: Lighthouse audit on staging URL
- At launch: Lighthouse audit on live URL, plus PageSpeed Insights
- Monthly: Lighthouse audit via scheduled CI run (see devops docs)
- Ongoing: Google Search Console Core Web Vitals report (field data, 28-day rolling)

---

## CURRENT CWV RISKS (FOR THIS STACK)

WordPress and Elementor introduce specific performance risks that must be mitigated before launch. Each risk is documented with its cause and the required fix.

### LCP Risks

**Risk 1: Hero image rendered as CSS background-image by Elementor**

Elementor section backgrounds and column backgrounds use CSS `background-image` rather than `<img>` elements. The browser cannot discover a CSS background image via the preload scanner, so it cannot start downloading the image until CSSOM is built. This delays LCP by 300-800ms on a typical mobile connection.

Fix: For the hero section on the homepage and all experience pages, use an Elementor Image widget (not a section background image) to render the hero as a true `<img>` element. Set the Image widget's image to the hero image. This allows the preload scanner to discover and fetch the image immediately.

If a CSS background is unavoidable (for example, due to a parallax effect), add a preload link in Insert Headers and Footers, Scripts in Header:
```html
<link rel="preload" as="image" href="[hero-image-url]" fetchpriority="high">
```
Replace `[hero-image-url]` with the actual URL of the hero image file.

Also add `fetchpriority="high"` on the `<img>` element itself when using an Elementor Image widget. This can be done via a custom attribute in Elementor's Advanced tab.

**Risk 2: Google Fonts adding DNS + connection + download latency**

Cormorant Garamond and Inter are loaded from `fonts.googleapis.com`. The browser must complete a DNS lookup, TCP connection, TLS handshake, and HTTP request before it can begin downloading the font. During this time, text renders in the fallback system font. Without `font-display: swap`, the browser may hold text invisible until the web font loads (invisible text = no LCP for text-based LCP elements).

Fix: Add preconnect hints before the Google Fonts stylesheet link, and ensure `&display=swap` is appended to the Google Fonts URL. See the Font Loading Optimization section below for the exact implementation.

**Risk 3: Third-party scripts blocking parse and render**

GTM, Meta Pixel, and TikTok Pixel must all be managed carefully. The GTM container snippet is async by design, so it does not block the parser. However, if any tag inside GTM fires synchronously on page load (for example, a custom HTML tag that runs inline JavaScript), it blocks the main thread. Meta Pixel and TikTok Pixel both fire JavaScript on initialization that consumes main thread time.

Fix: All pixel base codes go through GTM, not hardcoded in the WordPress head. No custom HTML tags in GTM that execute synchronous code. The `window.dataLayer = window.dataLayer || [];` initialization must appear as an inline script before the GTM snippet.

---

### CLS Risks

**Risk 1: Chat widget layout shift before chatbot is initialized**

If the Tidio plugin is still active in WordPress, it injects a chat widget into the DOM before the custom chatbot loads. Tidio's widget appears at a fixed position but still shifts the layout briefly during injection. The current CSS rule `#tidio-chat { display: none !important; }` in `chatbot-css.css` suppresses the visual render, but the Tidio script still runs, consuming main thread time and potentially causing a late layout shift.

Fix: Disable the Tidio plugin entirely from the WordPress admin (Plugins > Installed Plugins > Tidio > Deactivate). This is a mandatory action before launch. After Tidio is deactivated, the CSS rule can remain as a precaution but will have no effect.

The custom chatbot toggle button is `position: fixed` with explicit `width: 56px; height: 56px`. This occupies no layout flow, so it does not contribute to CLS. The chatbot panel is also fixed-position. No layout shift should occur from the custom chatbot if properly implemented.

**Risk 2: FOUT from Cormorant Garamond at large display sizes**

Cormorant Garamond is used at 40-72px for hero headlines and section titles. With `font-display: swap`, the browser renders text immediately in the fallback font (typically Georgia or a system serif), then swaps to Cormorant Garamond when it loads. At large sizes, the metric difference between the fallback font and Cormorant Garamond can shift layout vertically by 10-20px, causing a visible CLS event.

Fix: Add `size-adjust` to the Cormorant Garamond `@font-face` declaration so the fallback font metrics closely match Cormorant Garamond's metrics. The `size-adjust` value requires measurement. Use Font Style Matcher (meowni.ca/font-style-matcher) to calibrate. Approximate starting value: `size-adjust: 94%` with fallback font `Georgia`. Test and adjust until the swap causes minimal visible shift.

**Risk 3: Elementor images without explicit width and height attributes**

If Elementor renders images without `width` and `height` HTML attributes, the browser allocates no space for the image until it downloads enough data to know the dimensions. This causes the page to reflow as images load, contributing to CLS.

Fix: In Elementor's image widget settings, always set image dimensions. Verify by inspecting rendered HTML for `width` and `height` attributes on `<img>` elements. Elementor 3.x+ adds these attributes when the image has dimensions set in the Media Library. Ensure all uploaded images have dimensions recorded in the WordPress Media Library.

---

### INP Risks

**Risk 1: Oversized GTM container creating main thread bursts**

A GTM container with many tags (analytics, pixels, remarketing, A/B tests, chat scripts) can produce a large block of JavaScript that executes on page load and delays Time to Interactive. Each tag's JavaScript runs serially in the container evaluation phase. If the container is over 200KB compressed, it creates a long task that blocks interactivity.

Fix: Audit the GTM container before launch. Remove any tags related to Tidio (if Tidio is being disabled). Remove any unused or draft tags. Keep the container lean. Target under 10 active tags in production at launch. Review the container size in GTM's Preview mode and monitor Total Blocking Time in Lighthouse.

**Risk 2: chatbot-js.js loaded synchronously**

`chatbot-js.js` is 1,214 lines of JavaScript. If loaded in the `<head>` or in the footer without `defer`, it blocks the main thread during parse and execution. Any user interaction during that window will be queued and delayed, raising INP.

Fix: `chatbot-js.js` must be loaded with the `defer` attribute. It must not be placed in the `<head>`. It must be placed in the footer via Insert Headers and Footers, Scripts in Footer, with `defer`. The script must not call any DOM methods before `DOMContentLoaded`. All event listener registration must be inside a `DOMContentLoaded` callback or equivalent. This is documented in chatbot-mobile-ux.md and applies here as a performance requirement.

**Risk 3: Scroll event listeners creating long tasks**

Scroll event handlers fire on every scroll event, which can be 60 per second or more. If any handler does significant work (DOM queries, style recalculations, network requests), it creates repeated long tasks that degrade INP for scroll-triggered interactions.

Fix: `she-said-sail-global.js` uses IntersectionObserver for scroll reveal animations, which is the correct pattern. Do not add any scroll event listeners (`window.addEventListener('scroll', ...)`) that are not debounced or throttled. Do not let Elementor widgets register their own scroll handlers without review. If a scroll listener is unavoidable, throttle it to fire no more than once every 100ms using a `requestAnimationFrame` guard.

---

## FONT LOADING OPTIMIZATION

### Option A: Preconnect and display=swap via Google Fonts (Preferred for Launch)

This eliminates the connection latency overhead without requiring self-hosting. Add the following to Insert Headers and Footers, Scripts in Header, above any other Google Fonts reference:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

Ensure the Google Fonts stylesheet URL uses `&display=swap`. The correct URL for the She Said Sail font set is:

```
https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap
```

If WordPress or a plugin is generating the Google Fonts URL automatically (for example, via Elementor's typography settings), ensure the plugin appends `&display=swap`. In Elementor, go to Elementor > Settings > Advanced and check the Google Fonts load method. Use Perfmatters or WP Google Fonts plugin if Elementor's setting does not expose this option.

### Option B: Self-Hosted Fonts (Highest Performance, Post-Launch)

Download the WOFF2 files for Cormorant Garamond, Inter, and Playfair Display from Google Fonts or via the google-webfonts-helper tool (gwfh.mranftl.com). Upload to the WordPress server (for example, `/wp-content/fonts/`). Add `@font-face` declarations to `she-said-sail-global.css` with `font-display: swap`.

Example `@font-face` for Cormorant Garamond Regular:
```css
@font-face {
  font-family: 'Cormorant Garamond';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url('/wp-content/fonts/cormorant-garamond-regular.woff2') format('woff2');
  size-adjust: 94%;
  ascent-override: 90%;
}
```

Benefits: eliminates the DNS lookup and external connection entirely. The font file is served from the same origin as the page, benefiting from any server-side caching configuration.

This is the highest-performance option and is recommended as a post-launch optimization after the site is stable.

---

## HERO IMAGE OPTIMIZATION

The hero image is the LCP element on every key page. It must load as fast as possible.

**Format:** WebP with JPEG fallback (use `<picture>` if possible, or serve WebP directly if server supports content negotiation).

**Dimensions:**
- Maximum 1600px wide at 1x display density
- Supply 2x version (3200px wide) only if the hero is full-bleed on desktop and the image contains fine detail worth the file size cost
- Never serve a hero image wider than 3200px regardless of viewport

**Compression:** 80% quality WebP. Target file size under 200KB for the 1600px version.

**Loading behavior:**
- Do NOT add `loading="lazy"` to the hero image. Lazy loading prevents the browser from fetching the image until it is near the viewport, which defeats LCP.
- Add `fetchpriority="high"` to the hero `<img>` element so the browser prioritizes this image fetch over other resources.
- Elementor adds `loading="lazy"` to images by default since Elementor 3.0. Disable lazy loading specifically for the hero image in Elementor's image widget Advanced settings, or via a custom Elementor hook that removes the `loading` attribute from the first image on the page.

**Explicit dimensions:** Always set `width` and `height` attributes on the hero `<img>` element. This allows the browser to reserve the correct space before the image loads, preventing CLS.

**If Elementor uses CSS background-image for the hero section:**
Add to Insert Headers and Footers, Scripts in Header:
```html
<link rel="preload" as="image" href="[hero-image-url]" fetchpriority="high">
```
Replace `[hero-image-url]` with the exact URL of the hero image. Update this preload link whenever the hero image is changed.

---

## THIRD-PARTY SCRIPT IMPACT

Every third-party script on the page adds latency and main thread execution time. The following documents each script, its performance impact, and the required mitigation.

### GTM (GTM-TZ5KNRTH)

**Load method:** Async snippet in `<head>` via WordPress plugin.
**Performance impact:** The GTM snippet itself is async and does not block HTML parsing. However, it does add an additional HTTP request and a round trip to Google's tag servers. The GTM container JavaScript file is typically 30-80KB compressed. Container evaluation runs on the main thread.
**Estimated impact:** 80-120ms added to Time to Interactive depending on container size.
**Mitigation:**
- Keep the container under 10 active tags at launch.
- Remove all unused tags, triggers, and variables.
- Avoid Custom HTML tags that run synchronous code.
- The `window.dataLayer = window.dataLayer || [];` initialization must appear in the `<head>` before the GTM snippet as a separate inline script.

### Google Analytics GA4 (GT-WV3X86GZ via GTM)

**Load method:** Loaded by GTM as a Google Tag configuration tag.
**Performance impact:** Minimal additional impact when loaded via GTM (the GA4 library is loaded asynchronously by the GTM container after container evaluation). Does not block rendering.
**Mitigation:** Do not add a direct GA4 script tag to the WordPress head. All GA4 tracking goes through GTM.

### Meta Pixel (via GTM, not yet installed)

**Load method:** Will be loaded as a Custom HTML tag inside GTM, firing on All Pages.
**Performance impact:** The Meta Pixel base code loads `connect.facebook.net/en_US/fbevents.js`, approximately 50KB. It initializes synchronously once loaded. Estimated impact: 100-180ms added to main thread work.
**Mitigation:**
- Load only via GTM, never hardcoded in WordPress head.
- Fire the base code only on pages where remarketing is relevant (all pages except potentially the thank-you confirmation page, where the Pixel Purchase event fires separately).
- Do not load fbevents.js in a blocking manner. GTM's Custom HTML tag runs the script asynchronously relative to the page load sequence, which is acceptable.

### TikTok Pixel (via GTM, not yet installed)

**Load method:** Will be loaded as a Custom HTML tag inside GTM, firing on All Pages.
**Performance impact:** Similar to Meta Pixel. The TikTok Pixel library adds approximately 40-60KB. Main thread impact is approximately 80-150ms.
**Mitigation:** Same rules as Meta Pixel. Load only via GTM. Keep the base code tag and the event tags separate so event firing can be controlled with precision.

### Tidio (being disabled, mandatory before launch)

**Status:** Tidio plugin must be deactivated from the WordPress admin before launch. This is not optional.
**Performance impact (while active):** Tidio loads a full chat application asynchronously, but the script and its dependencies add 200-400KB to the page load and consume significant main thread time during initialization. This is the single largest performance liability on the current site.
**Mitigation:** Deactivate Tidio. Delete the plugin if no data needs to be preserved. The custom chatbot replaces all Tidio functionality.

### Custom Chatbot Widget (chatbot-css.css + chatbot-js.js)

**Load method:** CSS via Insert Headers and Footers, Scripts in Header. JS via Insert Headers and Footers, Scripts in Footer with `defer`.
**Performance impact:** Low when correctly loaded with `defer`. The JavaScript file is 1,214 lines. Minified and compressed, target file size is under 15KB. Execution is deferred until after the page is interactive.
**Mitigation:**
- Always load `chatbot-js.js` with `defer`.
- Always load `chatbot-css.css` as a standard `<link>` in the head (CSS is render-blocking but necessary for correct initial layout of the toggle button).
- The chatbot toggle button must be visible and correctly positioned from the first paint (not injected dynamically) so that its appearance does not cause CLS.

### she-said-sail-global.js

**Load method:** Deferred in footer via WordPress Appearance > Customize > Additional CSS (JS), or via Insert Headers and Footers.
**Performance impact:** Minimal. IntersectionObserver-based scroll reveal is efficient. Target file size under 10KB minified.
**Mitigation:** Load with `defer`. Do not add scroll event listeners.

---

## SCRIPT LOADING ORDER (RECOMMENDED)

The following is the correct loading sequence for all custom scripts and styles in WordPress. Incorrect order can break GTM tracking, cause flashes of unstyled content, or delay interactivity.

### In `<head>` (via Insert Headers and Footers, Scripts in Header)

Insert these in the following order, top to bottom:

1. **dataLayer initialization (inline script, required before GTM)**
```html
<script>window.dataLayer = window.dataLayer || [];</script>
```
This must appear before the GTM snippet. It initializes the dataLayer array so any pushes before GTM loads are preserved.

2. **GTM snippet (loaded by WordPress plugin, async)**
The GTM snippet is added by the Google Tag Manager for WordPress plugin or equivalent. Verify it appears after the dataLayer initialization.

3. **Google Fonts preconnect links**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
```

4. **Google Fonts stylesheet link (with display=swap)**
```html
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap" rel="stylesheet">
```

5. **Chatbot CSS link**
```html
<link rel="stylesheet" href="/wp-content/[path-to]/chatbot-css.css">
```
CSS is render-blocking but necessary. Keep the chatbot CSS file small (under 15KB). Non-chatbot styles belong in `she-said-sail-global.css` loaded via WordPress Additional CSS.

### In `<footer>` (via Insert Headers and Footers, Scripts in Footer)

Insert these in the following order, top to bottom:

1. **she-said-sail-global.js with defer**
```html
<script src="/wp-content/[path-to]/she-said-sail-global.js" defer></script>
```

2. **chatbot-js.js with defer**
```html
<script src="/wp-content/[path-to]/chatbot-js.js" defer></script>
```

Both scripts use `defer`, which means they execute in document order after HTML parsing is complete. `she-said-sail-global.js` is placed first because the chatbot script may depend on global site utilities.

---

## IMAGE LAZY LOADING STANDARD

| Image Position on Page | Loading Attribute | Rationale |
|---|---|---|
| Hero image (above the fold, LCP element) | None (omit the attribute) | Must load immediately. Never lazy-load. |
| Site logo | None | Above the fold. Small file. Never lazy-load. |
| First content image immediately below hero | None or `loading="eager"` | Likely visible on first scroll. Lazy-loading delays a visible image. |
| All other images below the fold | `loading="lazy"` | Browser defers fetch until image is near viewport. Reduces initial page weight. |

**Elementor setting:** Elementor 3.0+ adds `loading="lazy"` to all images by default. This is correct behavior for below-the-fold images. For the hero image, disable lazy loading in the Image widget's Advanced tab, or add a WordPress filter to remove the `loading` attribute from the first image:

```php
add_filter( 'wp_lazy_loading_enabled', function( $default, $tag_name, $context ) {
    // Return false for the first image to disable lazy loading
    // Implement per-image logic here based on attachment ID or class
    return $default;
}, 10, 3 );
```

This filter approach requires custom PHP in a child theme or a site-specific plugin. Coordinate with the developer who manages WordPress theme customizations.

---

## CACHING AND CDN RECOMMENDATION

### Server-Side Caching (Required at Launch)

WordPress must have a caching plugin active at launch to avoid generating pages dynamically on every request.

**Recommended plugin:** WP Rocket or LiteSpeed Cache (choose based on hosting environment compatibility).

**Minimum caching configuration:**
- Cache rendered HTML pages: 24-hour expiry
- Cache static assets (CSS, JS, image files): 1-year expiry with versioned filenames (WordPress handles this via `?ver=` query strings by default)
- Enable GZIP or Brotli compression for text files
- Enable browser caching headers for static assets

### CDN Recommendation (Post-Launch, Medium Priority)

A CDN reduces latency for visitors outside the server's geographic region and adds edge-side caching.

**Recommended option:** Cloudflare free tier, DNS-proxied.

Benefits:
- Edge caching for static assets (CSS, JS, images)
- Optional image optimization (WebP conversion, resizing via Cloudflare Polish and Mirage)
- DDoS protection
- Zero additional cost at the free tier

**Priority:** Medium. Not a launch blocker. Add after the site is stable and live. Cloudflare's free tier requires changing nameservers to Cloudflare, which requires a DNS migration plan.

---

## PERFORMANCE MONITORING

### Tools

| Tool | Purpose | URL |
|---|---|---|
| PageSpeed Insights | Synthetic lab data, CWV estimates, Lighthouse report | pagespeed.web.dev |
| Google Search Console | Field data from real users, 28-day rolling CWV report | search.google.com/search-console |
| Chrome DevTools Lighthouse | Local lab audit before deployment | Built into Chrome |
| WebPageTest | Detailed waterfall, filmstrip, multi-step testing | webpagetest.org |
| GA4 Site Speed | Real user timing data if GA4 site speed report is enabled | analytics.google.com |

### Audit Schedule

| Trigger | Action |
|---|---|
| Before launch | Run Lighthouse on staging URL for homepage, one experience page, FAQ page |
| At launch | Run Lighthouse and PageSpeed Insights on live URL for same pages |
| After any major content change (new hero image, new page, new third-party script) | Run Lighthouse on affected pages |
| Monthly | Scheduled Lighthouse run via CI (see devops docs for GitHub Actions configuration) |
| When Google Search Console reports a CWV regression | Run PageSpeed Insights, diagnose with Chrome DevTools, fix and re-audit |

### CWV Regression Response

If Google Search Console reports that any Core Web Vitals metric has moved from "Good" to "Needs Improvement":

1. Run PageSpeed Insights on the affected URL to identify the metric and likely cause.
2. Check the GTM container for recently added tags that fire on page load.
3. Check if any new images have been added to the hero area without explicit dimensions or without disabling lazy loading.
4. Check if any new third-party scripts have been added outside of GTM.
5. Fix the identified issue, deploy, and allow 28 days for field data to reflect the change.

---

*This document is maintained by the She Said Sail development team. Update this file when the technology stack changes (hosting, plugins, new third-party scripts, or CDN addition).*
