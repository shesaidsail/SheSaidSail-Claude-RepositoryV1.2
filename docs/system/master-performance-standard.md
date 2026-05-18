# SHE SAID SAIL — MASTER PERFORMANCE STANDARD
Version: 1.0 | Status: PRODUCTION | Owner: Will Hunt

---

## CORE WEB VITALS TARGETS

| Metric | Target | Good | Needs Work |
|--------|--------|------|-----------|
| LCP (Largest Contentful Paint) | < 2.5s | < 2.5s | > 4.0s |
| FID / INP (Interaction to Next Paint) | < 200ms | < 200ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | < 0.1 | > 0.25 |
| FCP (First Contentful Paint) | < 1.8s | < 1.8s | > 3.0s |
| TTFB (Time to First Byte) | < 600ms | < 800ms | > 1800ms |

---

## GOOGLE PAGESPEED TARGETS

| Device | Target Score |
|--------|-------------|
| Mobile | 80+ |
| Desktop | 90+ |

---

## IMAGE OPTIMIZATION

| Image Type | Format | Max Size | Dimensions |
|-----------|--------|---------|-----------|
| Hero | WebP or JPEG | 400kb | 1600px wide |
| Hero (mobile) | WebP or JPEG | 200kb | 800px wide |
| Content/card | WebP or JPEG | 150kb | 800px wide |
| OG image | JPEG | 200kb | 1200x630px |

### Implementation
- Use `loading="lazy"` on all images below the fold
- Use `loading="eager"` on hero image (above fold only)
- Include `width` and `height` attributes to prevent CLS
- Provide `srcset` for responsive images where platform supports it
- Use `decoding="async"` on non-critical images

---

## FONTS

- Maximum 2 font weights loaded
- Georgia is a system font (no load cost)
- If loading a web font: preload it in `<head>`, use `font-display: swap`
- No more than 1 external font family

---

## SCRIPTS

- GTM loads asynchronously
- All non-critical JS deferred
- No synchronous third-party scripts in `<head>`
- Analytics scripts load after page paint
- No unused script includes

---

## CSS

- No unused CSS in critical path
- Animate only `transform` and `opacity` (GPU-accelerated)
- No `all: transition` rules
- Minimal CSS resets

---

## WEBFLOW-SPECIFIC

- Publish site after every significant change
- Webflow CDN handles asset delivery automatically
- Disable unused interactions on mobile if they cause jank
- Use Webflow's native image optimization + CDN
- Set correct image dimensions in CMS and Designer

---

## MONITORING

- Connect Google Search Console
- Run PageSpeed Insights after every major page change
- Monitor Core Web Vitals in Google Search Console > Experience
- Alert if mobile score drops below 75
