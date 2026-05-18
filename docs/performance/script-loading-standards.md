# She Said Sail: Script Loading Standards

Version: 1.0
Date: 2026-05-18

---

## OVERVIEW

This document defines the correct loading pattern for every script on the She Said Sail site. Poor script loading is the primary cause of poor Lighthouse Performance scores and high Interaction to Next Paint (INP) on WordPress + Elementor sites. Every decision here is intentional and conservative. When in doubt, load later and load with defer.

**Performance targets:**

| Metric | Target | Notes |
|---|---|---|
| Lighthouse Performance (mobile) | 70+ | WordPress + Elementor baseline is often 45-60 without optimization |
| LCP | Under 2.5 seconds | Primary target metric |
| INP | Under 200ms | Interaction responsiveness |
| CLS | Under 0.1 | Font swap and chatbot widget are the two risk areas |
| Total blocking time | Under 300ms | Main thread blockage from synchronous scripts |

---

## THE PROBLEM WITH WORDPRESS + ELEMENTOR

WordPress loads many scripts synchronously by default. Elementor adds its own JS bundle (typically 150-300KB uncompressed). Third-party plugins such as Tidio and GTM plugins often inject scripts into the head without defer or async attributes. The result on a typical WordPress + Elementor site: the main thread is blocked for 2 to 4 seconds before the page becomes interactive.

**She Said Sail's specific constraints:**

1. We control scripts added via Insert Headers and Footers plugin. We do not control Elementor's own script loading strategy.
2. We cannot defer Elementor's JS without risking broken page functionality.
3. We can ensure every script we add does not make the baseline worse.
4. We can eliminate Tidio (the largest controllable performance offender).

The optimization strategy here is specific and achievable without a custom build pipeline.

---

## SCRIPT INVENTORY

Every script that loads on the She Said Sail site, in approximate load order:

| Script | Source | Location | Load Method | We Control It | Notes |
|---|---|---|---|---|---|
| WordPress core (wp-includes) | WordPress | Head | Synchronous | Limited | Required. Cannot defer without breaking WP functionality. |
| Hello Elementor theme CSS | Elementor | Head | Stylesheet link | No | Minimal impact. |
| Elementor frontend CSS | Elementor | Head | Stylesheet link | No | May include critical and non-critical styles together. |
| Google Fonts | Head (via WP or Insert Headers and Footers) | Head | Stylesheet link | Yes | Must add preconnect and display=swap. |
| Chatbot CSS | Insert Headers and Footers | Head | Stylesheet link | Yes | Non-render-blocking if loaded after fonts. Under 8KB target. |
| GTM container snippet | Google Tag Manager plugin | Head | Async script | Yes (via plugin) | GTM snippet itself is async. Loads quickly. Tags inside GTM run after. |
| WordPress jQuery | WordPress | Head or footer | Synchronous or deferred | No | Elementor depends on jQuery. Cannot safely move. |
| Elementor frontend JS | Elementor plugin | Footer | Deferred by Elementor | No | Elementor manages its own JS position. |
| Hello Elementor theme JS | Elementor | Footer | Deferred | No | Minimal file size. |
| she-said-sail-global.js | Insert Headers and Footers | Footer | defer | Yes | Our primary custom JS. All site behavior, UTM capture, form logic. |
| chatbot-js.js | Insert Headers and Footers | Footer | defer | Yes | Chatbot widget. Runs after global.js. |
| Meta Pixel | GTM (not hardcoded) | Via GTM | GTM-managed async | Yes (via GTM) | Never hardcode in head. |
| TikTok Pixel | GTM (not hardcoded) | Via GTM | GTM-managed async | Yes (via GTM) | Never hardcode in head. |
| GA4 | GTM (not hardcoded) | Via GTM | GTM-managed async | Yes (via GTM) | Loaded by GTM after container fires. |
| Tidio | WordPress plugin (being disabled) | Head | Async | Yes (remove it) | Loads full SDK even when CSS-hidden. Must be disabled in WP admin. |

---

## RECOMMENDED HEAD ORDER

The following is the complete content to add in Insert Headers and Footers, "Scripts in Header" field. Add these in order. Items already handled by WordPress plugins are noted and do not need to be added manually.

```html
<!-- STEP 1: dataLayer initialization -->
<!-- Must appear before the GTM snippet. GTM pushes events to dataLayer on load. -->
<!-- If dataLayer is not pre-initialized, GTM creates it but any pre-GTM pushes are lost. -->
<script>window.dataLayer = window.dataLayer || [];</script>

<!-- STEP 2: GTM snippet -->
<!-- Added automatically by the official Google Tag Manager for WordPress plugin. -->
<!-- Do not manually add the GTM snippet here. The plugin places it correctly. -->
<!-- Plugin: Google Tag Manager for WordPress (GTM4WP) by Thomas Geiger -->

<!-- STEP 3: Google Fonts preconnect -->
<!-- Preconnect reduces DNS lookup + TLS handshake time by 100-300ms. -->
<!-- Must appear before the Google Fonts stylesheet link. -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- STEP 4: Google Fonts stylesheet -->
<!-- Combined URL for all She Said Sail typefaces. -->
<!-- display=swap: text renders immediately in fallback font, then swaps when font loads. -->
<!-- Prevents invisible text (FOIT) during font load. -->
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400;1,600&family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600&display=swap">

<!-- STEP 5: Chatbot CSS -->
<!-- Non-render-blocking because it is a stylesheet. -->
<!-- Loading here instead of footer prevents a flash of unstyled chatbot widget on DOMContentLoaded. -->
<!-- Replace [chatbot-css-url] with the actual file URL from WordPress media library or CDN. -->
<link rel="stylesheet" href="[chatbot-css-url]">
```

**Per-page additions (not global, add to individual page head via Elementor page settings or a page-specific code block):**

```html
<!-- LCP image preload: homepage and each experience page -->
<!-- Add only on pages where the hero image IS the largest contentful paint element. -->
<!-- Replace [hero-image-url] with the actual image URL. -->
<!-- Do not use this on pages without a large hero image. -->
<link rel="preload" as="image" href="[hero-image-url]" fetchpriority="high">
```

---

## RECOMMENDED FOOTER ORDER

The following is the content to add in Insert Headers and Footers, "Scripts in Footer" field.

```html
<!-- STEP 1: Primary site JS -->
<!-- defer: parses after HTML, executes before DOMContentLoaded, respects source order. -->
<!-- Do not use async here: async would execute before the DOM is fully parsed. -->
<!-- Replace [she-said-sail-global-js-url] with the actual file URL. -->
<script defer src="[she-said-sail-global-js-url]"></script>

<!-- STEP 2: Chatbot JS -->
<!-- defer: executes after global.js (source order is preserved with defer). -->
<!-- chatbot-js.js reads sessionStorage values written by global.js. -->
<!-- Order dependency: global.js must execute first. defer in order guarantees this. -->
<!-- Replace [chatbot-js-url] with the actual file URL. -->
<script defer src="[chatbot-js-url]"></script>
```

---

## DEFER VS. ASYNC: WHY DEFER

Both `defer` and `async` prevent a script from blocking HTML parsing. The difference is execution timing:

| Attribute | Parsing | Execution timing | Order preserved |
|---|---|---|---|
| (none) | Blocked while script loads and executes | Immediately on encounter | Yes (sequential) |
| async | Not blocked | As soon as script downloads (may be before DOM is ready) | No |
| defer | Not blocked | After HTML is fully parsed, before DOMContentLoaded | Yes |

**For she-said-sail-global.js and chatbot-js.js, defer is required because:**

1. Both scripts access the DOM (form fields, button elements, cookie values). async risks executing before the DOM exists.
2. chatbot-js.js depends on sessionStorage values written by global.js. If async causes chatbot-js.js to execute first, it reads empty sessionStorage.
3. defer preserves source order: global.js executes, then chatbot-js.js. This is the correct dependency order.

Use async only for scripts with no DOM dependencies and no order dependencies (for example, a standalone analytics SDK that initializes itself).

---

## GOOGLE FONTS: DEEP DIVE

Google Fonts is one of the largest controllable LCP and CLS risk factors on She Said Sail.

### Current Risk

If WordPress or Elementor loads Google Fonts without &display=swap, browsers hold the text invisible until the font loads (Flash of Invisible Text, or FOIT). This adds perceived LCP time and can block text rendering for 300ms to 3 seconds on slow connections.

If no preconnect is set, the browser must complete a full DNS lookup and TLS handshake to fonts.googleapis.com and fonts.gstatic.com before font bytes start downloading. This adds 200 to 400ms on typical mobile connections.

### Recommended Setup

1. Remove any Google Fonts URLs that Elementor adds automatically (via Perfmatters or WP Rocket "Remove Google Fonts" option). This prevents duplicate font requests.
2. Add a single combined Google Fonts URL (the one in Step 4 of the head order above) with all required families, weights, and &display=swap.
3. Add preconnect tags (Step 3) before the font link.

### Font Swap CLS Risk Assessment

CLS from font swap is low for She Said Sail for two reasons:

- Cormorant Garamond is a display serif. The fallback (Georgia, Times New Roman) is metrically similar in weight and x-height at large headline sizes. Layout shift at 40px+ heading size is minimal.
- Inter is a humanist sans-serif. The fallback (system-ui, -apple-system) is metrically close at body text sizes (16-18px).

If CLS from font swap is measured above 0.1 after launch, the advanced fix is to add a size-adjust value to the @font-face declaration for fallback fonts. This CSS technique adjusts the fallback font's metrics to match the web font, eliminating layout shift on swap. This is an optional post-launch improvement.

### Self-Hosted Fonts (Advanced Option)

Self-hosting Google Fonts as WOFF2 files eliminates all cross-origin requests for typography. This is the highest-performance option. It requires:

1. Downloading font files from google-webfonts-helper.herokuapp.com
2. Adding them to the WordPress uploads directory or theme folder
3. Declaring @font-face rules in a custom CSS file
4. Removing the Google Fonts external link entirely

Tradeoff: self-hosted fonts do not benefit from Google's CDN cache. On the other hand, browser cache for self-hosted fonts is under our control. Recommended as a post-launch performance improvement if Lighthouse Performance score is still under 75 after initial launch optimizations.

---

## GTM CONTAINER OPTIMIZATION

The GTM container (GTM-WWTT27Z3) loads and executes all tracking code. A bloated or poorly structured container increases Time to Interactive.

### Container Rules for She Said Sail

1. Maximum 25 tags in production. If the count approaches this limit, audit for unused or duplicate tags before adding new ones.
2. No synchronously-executing scripts inside Custom HTML tags. All Custom HTML tags must use async initialization patterns (for example, wrapping third-party pixel code in an IIFE that does not block the thread).
3. Remove the old open_chat trigger and tag after Tidio is confirmed disabled. The trigger will never fire again and adds unnecessary evaluation overhead.
4. Test every new tag in GTM Preview mode before publishing. Unpublished tags have zero impact on production performance.
5. Enable Container built-in variables only for those actually used by active tags and triggers. Each enabled built-in variable is evaluated on every page load. Unused ones add overhead for no benefit.
6. Tag sequencing: if a tag fires on the same event as another tag it depends on, use GTM's Tag Sequencing feature rather than adding artificial delays via setTimeout in Custom HTML tags.

### Current GTM Tag Inventory

**Site tags (14 events, triggering 14 GA4 tags):**

view_homepage, view_request_page, view_experiences_page, view_experience_page, view_about_page, view_contact_page, view_faq_page, view_journal_page, view_thank_you_page, click_request_to_book, click_explore_experiences, click_experience_card, start_booking_form, submit_booking_form, submit_email_capture, click_phone, open_chat (remove after Tidio disabled), scroll_50_percent, scroll_90_percent

**Chatbot tags to build (8 events, each needs a trigger + GA4 tag):**

chatbot_open, chatbot_start_conversation, chatbot_select_occasion, chatbot_select_experience, chatbot_capture_email, chatbot_capture_phone, chatbot_handoff, chatbot_complete

Total tags when chatbot is live: approximately 28 GA4 Event tags + 1 GA4 Config tag + Data Layer Variable tags. Within the recommended limit.

---

## CHATBOT PERFORMANCE IMPACT

The chatbot widget (chatbot-css.css and chatbot-js.js) has these measured performance characteristics:

### File Size Targets

| File | Target (minified) | Current (unminified) | Notes |
|---|---|---|---|
| chatbot-css.css | Under 8KB | Not yet measured | Minify before production |
| chatbot-js.js | Under 15KB | Approximately 1,214 lines | Minify before production |

Minification is expected to reduce chatbot-js.js by 30 to 40 percent. Use a tool such as terser (Node.js CLI) or the minification step in WP Rocket before uploading to WordPress.

### Impact by Metric

| Metric | Impact | Reason |
|---|---|---|
| LCP | None | Both files load in footer with defer. LCP is determined by the hero image, which is already loaded by the time these scripts execute. |
| INP | Minimal | chatbot-js.js adds event listeners after DOMContentLoaded. All listeners are for the chatbot widget area. No interference with main page interactions. |
| CLS | None | The chatbot toggle button is fixed-position with explicit 56px by 56px dimensions. It does not participate in document flow. It cannot cause layout shift. |
| TBT (Total Blocking Time) | Minimal | defer executes JS after HTML parsing. The JS execution itself takes under 5ms on modern devices. |

### Tidio Comparison

Until Tidio is disabled from WP admin, it loads a full chat SDK (approximately 150-400KB) asynchronously from Tidio's CDN. The CSS hide rule (display: none on the Tidio widget) prevents visual display but does not stop JS execution. Tidio's SDK runs its full initialization, creates DOM nodes, and registers event listeners. This adds an estimated 150 to 300ms to Time to Interactive on mobile devices.

Disabling Tidio from WP admin (Plugins, Deactivate) eliminates this overhead entirely. This is the single highest-impact action available before launch.

---

## WHY NOT PARTYTOWN

Partytown (by Builder.io) moves third-party scripts to web workers, freeing the main thread from third-party JS execution overhead. In theory this is ideal for analytics-heavy sites. In practice, Partytown has significant incompatibilities with the She Said Sail stack.

**Specific incompatibilities:**

1. GTM inside Partytown breaks many tags. GTM tags that use synchronous DOM access (click listeners, form submit listeners, element visibility observers) do not work correctly in a web worker context. Our click_request_to_book, start_booking_form, and submit_booking_form events all depend on DOM event listeners.
2. she-said-sail-global.js cannot run in a worker. It reads and writes the DOM directly (populating hidden form inputs, reading cookie values, firing dataLayer pushes on user events). Web workers have no DOM access.
3. chatbot-js.js cannot run in a worker for the same reason. The chatbot renders UI elements directly in the DOM.
4. WordPress + Partytown requires a custom server configuration or plugin. Without a Next.js or Nuxt build system, the implementation requires manual service worker setup. The risk of breaking attribution and conversion tracking during setup is high.
5. There is no WordPress plugin with stable, production-tested Partytown + GTM support as of the writing of this document.

**Recommendation: Do not use Partytown for She Said Sail.** The performance gains from Partytown are real but apply primarily to sites running multiple heavy third-party scripts (five or more SDKs). She Said Sail's approved third-party footprint is small: GTM manages everything, Tidio is being removed, and no additional SDKs are approved. The risk of breaking attribution outweighs the potential gains.

---

## THIRD-PARTY SCRIPT POLICY

The She Said Sail performance budget depends on keeping the third-party script surface area small. Every third-party script is a potential cause of LCP regression, TBT increase, or broken attribution.

### Approved Scripts (Direct, Not via GTM)

| Script | Reason Approved | Load Method |
|---|---|---|
| Google Tag Manager | Container for all other approved scripts | Async in head (GTM plugin) |
| Google Fonts | Core brand typography | Stylesheet in head |

### Approved Scripts (Via GTM Only)

These scripts must never be hardcoded in the WordPress head or Insert Headers and Footers. They must load through GTM tags so they can be tested, paused, and versioned without a WordPress deploy.

| Script | GTM Tag Type | Notes |
|---|---|---|
| GA4 | Google Analytics: GA4 Configuration | One config tag, fires on All Pages |
| Meta Pixel | Custom HTML | Base code only. Events fired via additional tags on relevant triggers. |
| TikTok Pixel | Custom HTML | Base code only. |

### Not Approved

| Script | Reason |
|---|---|
| Any chat widget other than the She Said Sail custom chatbot | Adds SDK weight, conflicts with chatbot |
| Any widget script added directly to WordPress head | Bypasses GTM, cannot be versioned or tested safely |
| Social media embed scripts (Twitter, Instagram, etc.) | Significant performance cost. Use screenshot + link instead of live embed. |
| Retargeting scripts not managed through GTM | Attribution conflict, performance cost |
| Tidio | Being removed. Do not re-enable. |
| Hotjar, FullStory, or other session recording tools | Significant performance cost (often 40-80ms TBT per tool). Not approved for production. |

### Adding a New Script: Approval Checklist

Before any new third-party script is added to She Said Sail, evaluate against all of the following:

1. Is this script available through GTM (as a template or Custom HTML tag)? If yes, it must be added through GTM, not hardcoded.
2. Does this script add more than 50ms TBT on mobile (Lighthouse throttling)? If yes, it is not approved without an offsetting removal.
3. Does this script make external network requests that are not covered by the existing preconnect headers? If yes, add preconnect for its domain.
4. Does this script interfere with the sss_utm sessionStorage or the sss_vid cookie? If yes, it is not approved until the conflict is resolved.
5. Can the same business goal be achieved using existing approved tools (GA4, GTM, the custom chatbot)? If yes, use existing tools.

---

## WORDPRESS PLUGIN RECOMMENDATIONS

These plugins improve script loading performance and are compatible with Elementor:

| Plugin | Purpose | Priority | Notes |
|---|---|---|---|
| Perfmatters | Remove unused scripts, Google Fonts control, lazy load control | High | Lightweight alternative to WP Rocket for script management |
| WP Rocket | Full caching, CDN, minification, font optimization | High (alternative to Perfmatters) | More features, higher cost |
| Autoptimize | JS and CSS minification and concatenation | Medium | Use only if not using WP Rocket |
| Imagify or ShortPixel | Image compression and WebP conversion | High | Hero image compression directly impacts LCP |

Do not install both Perfmatters and WP Rocket. They overlap and conflict. Choose one.

**Critical configuration note for any caching plugin:** Elementor generates CSS files per-page. Caching plugins must be configured to exclude Elementor's dynamic CSS from concatenation and minification. Elementor provides documentation on how to do this for WP Rocket. Always test with GTM Preview open after enabling caching to verify that GTM still fires correctly.

---

## QUICK REFERENCE: BEFORE LAUNCH CHECKLIST

| Item | Action | Owner |
|---|---|---|
| Tidio disabled | WP Admin, Plugins, Deactivate Tidio | WordPress admin |
| dataLayer initialized before GTM | Add window.dataLayer = window.dataLayer || []; in Insert Headers and Footers head section | Developer |
| Google Fonts preconnect added | Add two preconnect link tags before Fonts URL | Developer |
| Google Fonts URL has &display=swap | Verify URL in head includes display=swap | Developer |
| Hero images not lazy-loaded | Verify hero img tags have loading="eager" and fetchpriority="high" in Elementor | Developer |
| she-said-sail-global.js loading with defer | Verify script tag in footer has defer attribute | Developer |
| chatbot-js.js loading with defer | Verify script tag in footer has defer attribute | Developer |
| chatbot-css.css loading in head | Verify stylesheet link is in head, not footer | Developer |
| No third-party scripts hardcoded in head | Audit Insert Headers and Footers head section for any non-approved script tags | Developer |
| GTM container tested in Preview | All 22 events verified firing in GTM Preview before publishing | Developer |
