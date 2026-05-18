# SHE SAID SAIL
# MASTER PERFORMANCE STANDARD

STATUS: PRODUCTION
VERSION: v1.0

---

## CORE WEB VITALS TARGETS

| Metric | Target | Minimum Acceptable |
|--------|--------|--------------------|
| LCP (Largest Contentful Paint) | < 2.5s | < 4.0s |
| FID / INP (Interaction to Next Paint) | < 100ms | < 200ms |
| CLS (Cumulative Layout Shift) | < 0.1 | < 0.25 |
| FCP (First Contentful Paint) | < 1.8s | < 3.0s |
| TTFB (Time to First Byte) | < 600ms | < 1500ms |

---

## IMAGE OPTIMIZATION

### Format

- Preferred: WebP (90% quality)
- Fallback: JPEG (85% quality)
- No PNG for photographs

### Sizing

| Usage | Max Width | Max File Size |
|-------|-----------|---------------|
| Hero background | 1920px | 280KB |
| Section background | 1440px | 200KB |
| Content image | 800px | 120KB |
| Thumbnail | 400px | 60KB |
| OG image | 1200x630px | 180KB |

### srcset

Provide at minimum: 400w, 800w, 1400w for all content images.

### Loading

- Hero image (LCP): loading="eager", fetchpriority="high"
- All below-fold: loading="lazy"
- Never lazy-load above the fold

---

## JAVASCRIPT STANDARDS

- All custom scripts: deferred or async
- No render-blocking scripts in <head>
- GTM: standard async snippet in <head>
- Third-party scripts: load after page interactive

---

## CSS STANDARDS

- Critical CSS: inline in <head> for above-fold elements
- Webflow handles most CSS delivery
- Custom CSS file: minified, max 20KB additional
- No unused CSS in production

---

## FONT LOADING

- System font stack preferred (no Google Fonts dependency)
- If custom fonts used: preload the primary weight
- font-display: swap for all web fonts
- Subsetting: Latin characters only if custom font used

---

## CACHING

- Static assets: 1-year cache headers
- HTML: short cache (Webflow managed)
- Images: Webflow CDN (automatic)

---

## MOBILE PERFORMANCE

- Test on: Moto G Power equivalent (mid-range Android)
- Target: PageSpeed Insights mobile score 70+
- Ideal: 85+
- Use PageSpeed API to measure before launch

---

## MONITORING

- Core Web Vitals: Google Search Console
- Performance regressions: flag if LCP degrades >20% from baseline
- Real user monitoring: if analytics shows high bounce on mobile, investigate LCP
