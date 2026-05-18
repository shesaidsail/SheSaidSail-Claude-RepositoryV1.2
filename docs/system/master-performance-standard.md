# SHE SAID SAIL
# MASTER PERFORMANCE STANDARD

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## CORE WEB VITALS TARGETS

| Metric | Target | Acceptable | Fail |
|--------|--------|-----------|------|
| LCP (Largest Contentful Paint) | Under 2.0s | Under 2.5s | Over 2.5s |
| FID / INP (Interaction to Next Paint) | Under 50ms | Under 100ms | Over 200ms |
| CLS (Cumulative Layout Shift) | Under 0.05 | Under 0.1 | Over 0.1 |
| FCP (First Contentful Paint) | Under 1.5s | Under 1.8s | Over 2.0s |
| TTFB (Time to First Byte) | Under 600ms | Under 800ms | Over 1000ms |

All targets measured on mobile, 4G connection, Chrome DevTools throttling.

---

## IMAGE STANDARDS

| Image Type | Format | Max Size | Max Width |
|------------|--------|----------|-----------|
| Hero (mobile) | WebP | 280KB | 1200px |
| Hero (desktop) | WebP | 480KB | 2400px |
| Experience card | WebP | 120KB | 800px |
| Thumbnail | WebP | 60KB | 400px |
| OG / Social share | JPEG | 200KB | 1200x630px |

Fallback: JPEG for browsers without WebP support (use picture element with source).

### Image Lazy Loading
- Hero image: eager load (no lazy)
- All other images: loading="lazy"
- All images: width and height attributes set to prevent CLS

---

## FONT LOADING

```css
@font-face {
  font-display: swap;
}
```

- Georgia is a system font. No external font load required for body.
- If custom fonts used: preload the woff2 in the head.
- Limit web fonts to 2 maximum (one serif, one sans).
- Subset fonts to Latin characters only.

---

## JAVASCRIPT STANDARDS

- No render-blocking scripts above the fold
- All non-critical JS: defer or async attribute
- GTM: loaded asynchronously
- Analytics: non-blocking
- Form enhancement scripts: deferred
- No jQuery unless already in the Webflow bundle
- Total JS payload target: under 200KB gzipped

---

## CSS STANDARDS

- Critical CSS inlined for above-fold content
- Non-critical CSS: loaded with media trick or deferred
- No unused CSS from large frameworks
- Total CSS payload target: under 50KB gzipped

---

## THIRD-PARTY SCRIPTS

| Script | Load Strategy | Priority |
|--------|--------------|---------|
| GTM | Async | High |
| GA4 (via GTM) | Via GTM | Normal |
| Hotjar | Defer | Low |
| Meta Pixel | Defer | Low |
| TikTok Pixel | Defer | Low |

Never load tracking pixels synchronously.
Delay pixels until user interaction if possible (consent-aware loading).

---

## CACHING

- Webflow handles CDN and caching automatically
- Custom assets (CSS, JS) should use versioned file names for cache busting
- No long-lived cache on frequently changing HTML

---

## MONITORING

After any deploy:
1. Run Google PageSpeed Insights on the mobile view
2. Check LCP, FID, CLS are within targets
3. If LCP fails: check image size and hero load strategy
4. If CLS fails: check image aspect ratios and font loading

Target: Green scores (90+) on both mobile and desktop PageSpeed.
