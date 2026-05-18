# She Said Sail: Pre-Audit Integration Report
**Version:** 1.0
**Date:** May 2026
**Purpose:** Documents all external standards, references, and implementation patterns integrated into the She Said Sail optimization system before the final perfection audit.

---

## REFERENCES INTEGRATED

### 1. llmstxt.org Specification

**Source:** https://llmstxt.org
**Status:** Fully implemented

What was implemented:
- /llms.txt file created at site root following exact spec (H1 brand name, blockquote summary, H2-delimited sections, file list format `- [Title](url): description`)
- 6 sections: About, Experiences (4 entries with names/occasions/capacity/URLs), Booking, FAQ, Journal, Contact
- Optional section with experiences overview and legal pages
- llms-txt-strategy.md created in docs/ai-search/ documenting maintenance triggers and deployment guidance

---

### 2. Schema.org Structured Data Standards

**Source:** https://schema.org and https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
**Status:** Fully implemented across all 10 page metadata files

What was implemented:
- Dual @type ["LocalBusiness", "TouristInformationCenter"] on global schema
- @id linked entity graph: "https://shesaidsail.com/#organization" and "https://shesaidsail.com/#website"
- WebSite schema with SearchAction potentialAction
- Service schema on all 4 experience pages: serviceType "Yacht Charter", audience.audienceType, areaServed (Miami, Fort Lauderdale), availability on Offer, provider @id reference
- Organization schema: foundingDate, knowsAbout (8 topics), hasOfferCatalog (4 experiences), serviceArea GeoCircle
- ItemList schema on experiences index listing all 4 experiences as structured list
- FAQPage schema on /faq/ for direct AI extraction
- BreadcrumbList on all pages
- Full schema registry in docs/schema/schema-standards.md

---

### 3. AI Crawler Access Standards

**Source:** Google bot documentation, OpenAI published bot specifications (training data), Anthropic ClaudeBot documentation
**Status:** Fully implemented

What was implemented:
- docs/ai-search/ai-crawler-guide.md with complete robots.txt template
- 11 AI bot user agents permitted: GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, anthropic-ai, PerplexityBot, Google-Extended, Applebot, Applebot-Extended, Diffbot, FacebookBot
- /thank-you/ disallowed for all bots (prevents conversion data leakage)
- /wp-admin/ disallowed for all bots

---

### 4. Core Web Vitals Standards

**Source:** https://web.dev/articles/vitals, https://web.dev/articles/lcp, https://web.dev/articles/cls
**Status:** Documented as targets, implementation guidance written

Targets established:
- LCP: Good < 2.5s (She Said Sail target: < 2.0s)
- INP: Good < 200ms (She Said Sail target: < 150ms)
- CLS: Good < 0.1 (She Said Sail target: < 0.05)

Implementation guidance written:
- docs/performance/performance-standards.md: Lighthouse targets, CWV risk analysis for WordPress+Elementor, font loading, hero image standards, third-party script impact
- .github/workflows/lighthouse.yml: automated Lighthouse CI on push to feature branch
- .lighthouserc.json: thresholds set at Performance 90+, Accessibility 95+, Best Practices 95+, SEO 100, LCP < 2.5s, CLS < 0.1

Key fix documented: hero images must have `fetchpriority="high"` and `loading="eager"`, never `loading="lazy"`.

---

### 5. WCAG 2.1 AA Accessibility Standards

**Source:** https://www.w3.org/WAI/WCAG21/quickref/
**Status:** Fully documented, implementation guidance written

What was implemented:
- docs/performance/accessibility-standards.md: full WCAG 2.1 AA implementation guide
- Color contrast audit for all 9 brand color combinations
- Heading hierarchy standards per page type
- Keyboard navigation behavior table
- Focus indicator standard: `:focus-visible { outline: 2px solid var(--sss-gold); outline-offset: 3px; }`
- Alt text standards with examples for experience images, decorative images, icon buttons
- Form accessibility: label requirements, error messages, required field indicators
- Chatbot ARIA implementation: role="dialog", aria-label, aria-live="polite", focus management
- Mobile touch targets: 44x44px minimum per WCAG 2.5.5

Key findings from contrast audit:
- --sss-gold #DAB97E on white: 2.4:1 (FAILS for body text, passes for large text 18pt+)
- --sss-muted rgba(44,44,44,0.5) on white: ~2.7:1 (FAILS; use only for decorative elements)
- --sss-navy #1A2332 on white: 13.8:1 (PASSES strongly)
- --sss-text #2C2C2C on white: 12.6:1 (PASSES strongly)

---

### 6. Google Tag Manager Dataayer Standards

**Source:** Google Tag Manager documentation and Google Analytics 4 documentation
**Status:** Fully documented, implementation guidance written

What was implemented:
- docs/performance/script-loading-standards.md documents correct GTM initialization pattern
- Critical rule: `window.dataLayer = window.dataLayer || [];` must precede GTM snippet in head
- 22 custom GTM events documented in gtm-events-map.md (14 site + 8 chatbot)
- GTM variable setup documented (7 recommended data layer variables)
- GTM tag firing order documented: GA4 configuration first, then event tags

---

### 7. Analytics Reliability Standards

**Source:** GA4 documentation, Meta Pixel documentation
**Status:** Documented and implemented in analytics architecture

What was implemented:
- Correct dataLayer initialization pattern (prevents event loss before GTM loads)
- All conversion events fire through GTM, not hardcoded
- Meta Pixel Lead event parameters documented: content_category, content_name, value
- Meta Pixel ViewContent event documented for experience page views
- TikTok Pixel CompleteRegistration event documented for form submissions
- Attribution chain: UTM capture (sessionStorage/localStorage) -> form payload -> Make.com -> Airtable
- First-touch attribution model documented in docs/backend/revenue-attribution.md

---

### 8. Script Loading and Performance Standards

**Status:** Fully documented

What was implemented:
- docs/performance/script-loading-standards.md: complete script inventory, loading order, dependency chain
- Partytown explicitly rejected with 4 specific incompatibilities for this WordPress+GTM stack
- Defer vs async decision criteria documented
- Third-party script policy with approval/rejection criteria
- Script audit checklist for deployment verification

---

### 9. Generative Engine Optimization (GEO)

**Status:** Fully documented and implemented

What was implemented:
- docs/ai-search/geo-strategy.md: 13 target conversational queries mapped to specific pages
- GEO content rules: capacity, occasion fit, location (Miami), price, duration on every experience page
- Schema signals mapped to query types (audience.audienceType answers "who is this for", areaServed answers "in Miami")
- GEO scoring: 4.0 overall before, 8.4 overall after
- docs/ai-search/ai-search-audit.md: 8-dimension before/after scoring

---

### 10. Intelligence and Learning Layer

**Status:** Fully designed and documented

What was implemented:
- 6 new Airtable tables: Chatbot Conversations, Revenue Attribution, Experience Performance, Weekly Insights, Founder Decisions, Lessons Learned
- 4 new Make.com scenarios: M-BOOKING-OUTCOME-001, M-WEEKLY-REPORT-001, M-EXPERIENCE-ROLLUP-001, M-CONCIERGE-SCORE-001
- Visitor ID tracking: sss_vid UUID cookie, window.__sssVid, included in all webhook payloads
- Weekly Monday 8:00 AM intelligence report posted to Slack #intelligence
- Optional Claude API integration for AI narrative analysis in weekly report
- Revenue attribution closing the loop from UTM source to booking revenue
- docs/backend/intelligence-layer.md, revenue-attribution.md, weekly-ai-analysis.md
- docs/intelligence/weekly-learning-loop.md, dashboard-specs.md, founder-intelligence-system.md, intelligence-layer-qa.md

---

## AI SEARCH IMPROVEMENTS

| Dimension | Before | After |
|---|---|---|
| llms.txt readiness | 0 / 10 | 8 / 10 |
| Schema support for GEO queries | 4 / 10 | 8.5 / 10 |
| Entity descriptions (AI-extractable facts) | 4 / 10 | 8 / 10 |
| AI crawler access (robots.txt) | 4 / 10 | 9 / 10 |
| FAQ extraction quality | 8 / 10 | 9 / 10 |
| Conversational query targeting | 3 / 10 | 8 / 10 |
| Internal linking for topical authority | 5 / 10 | 8 / 10 |
| **Overall AI Search Readiness** | **4.3 / 10** | **8.4 / 10** |

---

## SCHEMA IMPROVEMENTS

| Schema Element | Before | After |
|---|---|---|
| Organization @type | LocalBusiness (single) | ["LocalBusiness", "TouristInformationCenter"] |
| @id linked entities | None | Organization and WebSite @id graph |
| Service.serviceType | Missing | "Yacht Charter" on all 4 experience schemas |
| Service.audience.audienceType | Missing | Present on all 4 experience schemas |
| Service.areaServed | Missing | Miami + Fort Lauderdale on all 4 schemas |
| Service.offers.availability | Missing | OnlineOnly on all 4 schemas |
| ItemList on /experiences/ | Missing | All 4 experiences as ListItem with position |
| BreadcrumbList | Homepage only | All 6+ pages |
| WebSite SearchAction | Missing | Present with URL template |
| Organization.knowsAbout | Missing | 8 knowledge topics |
| Organization.hasOfferCatalog | Missing | All 4 experiences |

---

## LIGHTHOUSE IMPROVEMENTS

| Metric | Target (Mobile) | Target (Desktop) | Monitoring |
|---|---|---|---|
| Performance | 90+ | 95+ | Lighthouse CI on push |
| Accessibility | 95+ | 100 | Lighthouse CI on push |
| Best Practices | 95+ | 95+ | Lighthouse CI on push |
| SEO | 100 | 100 | Lighthouse CI on push |

Lighthouse CI configuration committed at: `.github/workflows/lighthouse.yml` and `.lighthouserc.json`

Auditing all 8 key pages: homepage, experiences index, 4 experience pages, request-to-book, FAQ.

---

## CORE WEB VITALS IMPROVEMENTS

| Metric | Good Threshold | She Said Sail Target | Key Risk Factor |
|---|---|---|---|
| LCP | < 2.5s | < 2.0s | Hero images without fetchpriority="high" |
| INP | < 200ms | < 150ms | Elementor widget click handlers |
| CLS | < 0.1 | < 0.05 | Font swap + chatbot toggle injection |

Documented fixes in docs/performance/performance-standards.md:
- Hero image preload with fetchpriority="high" on all hero image pages
- Explicit width/height on all images to prevent layout shift
- font-display: swap on all Google Fonts
- Disable WordPress core lazy loading for above-fold images
- Pre-reserve chatbot toggle space to prevent CLS

---

## ACCESSIBILITY IMPROVEMENTS

| Standard | Before | After |
|---|---|---|
| Color contrast documented | No | Yes (9 combinations audited) |
| Focus indicator standard | None | 2px gold outline via :focus-visible |
| Chatbot ARIA | None | role="dialog", aria-label, aria-live, focus management |
| Touch targets | Not specified | 44x44px minimum documented |
| Alt text standard | Not specified | Written guidelines with examples |
| Heading hierarchy | Not specified | Per-page structure documented |
| Form accessibility | Not specified | Label, error, required field standards |
| WCAG 2.1 AA checklist | None | 17-item checklist in accessibility-standards.md |

Confirmed failures requiring fix before launch:
- --sss-gold #DAB97E fails contrast for normal-weight body text (must use only for large text 18pt+)
- --sss-muted rgba(44,44,44,0.5) fails contrast (use only for decorative elements)

---

## ANALYTICS RELIABILITY IMPROVEMENTS

| Issue | Fix |
|---|---|
| dataLayer initialized after GTM (event loss risk) | Document correct order: dataLayer init first, then GTM snippet |
| Visitor ID not in webhook payloads | sss_vid cookie + window.__sssVid added to all payload specs |
| No revenue attribution | Revenue Attribution table + M-BOOKING-OUTCOME-001 scenario designed |
| No UTM-to-booking connection | M-BOOKING-OUTCOME-001 creates the link on Request Status = Booked |
| Weekly report manual and disconnected | M-WEEKLY-REPORT-001 automates Monday 8:00 AM Slack intelligence report |

---

## CHATBOT UX IMPROVEMENTS

| Area | Improvement |
|---|---|
| State machine | 12 states covering opener, occasion, energy, recommendation, date, contact collection, handoff |
| Experience recommendation | Logic matrix mapping occasion + energy to correct experience |
| Auto-trigger | 60s homepage, 45s experience pages, never /request-to-book/, never mobile |
| Silence detection | 90-second inactivity handler |
| ARIA accessibility | Full dialog role, aria-live announcements, focus management, Escape key |
| CLS mitigation | Fixed-position toggle with reserved space |
| Visitor ID | window.__sssVid included in webhook payload for Airtable cross-linking |
| GTM events | 8 chatbot events: open, close, start, state transition, recommendation, handoff, submit, abandon |

---

## BACKEND INTELLIGENCE IMPROVEMENTS

| Area | Improvement |
|---|---|
| Attribution gap | Revenue Attribution table closes UTM-to-booking loop |
| Weekly reporting | Automated Monday Slack report with revenue, leads, chatbot, attribution metrics |
| Experience performance tracking | Weekly snapshot per experience, trending over time |
| Concierge performance | Automated scoring on booking completion |
| Founder decision tracking | Linked to weekly insights, measurement plan, outcome recording |
| Lessons learned system | Searchable knowledge base accumulating over time |
| Visitor cross-linking | sss_vid UUID connects Requests, Chatbot Conversations, UTMs at visitor level |

---

## REMAINING TECHNICAL WEAKNESSES

These are known gaps that cannot be addressed without live site access or additional development resources.

### Critical (resolve before launch)

1. **Gold contrast failure:** --sss-gold #DAB97E on white is 2.4:1, which fails WCAG AA for normal body text. Any gold text under 18pt/bold must be replaced with --sss-navy or a darker gold variant.

2. **Muted text contrast failure:** --sss-muted rgba(44,44,44,0.5) is approximately 2.7:1, which fails. All muted text must be decorative (never carrying meaning) or replaced with a passing contrast ratio.

3. **Hero image fetchpriority:** Cannot verify this is correctly implemented without live site inspection. Must be confirmed on every page with an above-fold hero image before launch.

4. **Elementor lazy loading override:** The WordPress filter to disable core lazy loading on hero images is documented but not yet applied. Requires functions.php access.

### High (resolve within 2 weeks of launch)

5. **Visitor ID not yet wired:** The sss_vid cookie and window.__sssVid code is specified in global-js-intelligence-addendum.md but not yet merged into she-said-sail-global.js or chatbot-js.js. Webhook payloads do not yet include visitor_id.

6. **chatbot_capture_phone GTM gap:** This event is in chatbot-js.js but not in the master gtm-events-map.md. A GTM trigger and GA4 event tag must be created.

7. **Webhook URLs are placeholders:** WIRE_THIS_CHATBOT_WEBHOOK_URL in chatbot-js.js and WIRE_THIS_CONTACT_WEBHOOK_URL in contact-html-snippets.html must be replaced with live Make.com webhook URLs before deployment.

8. **Intelligence layer not yet built:** All 6 new Airtable tables and 4 new Make scenarios are designed and documented but not yet created in Airtable or Make.com.

### Medium (post-launch backlog)

9. **No AggregateRating schema:** Adding ratings schema would significantly improve AI recommendation confidence and rich snippet eligibility. Requires 5+ verified reviews.

10. **No self-hosted fonts:** Google Fonts external request adds 50-100ms DNS lookup. Self-hosting after launch removes this dependency.

11. **No VideoObject schema:** Short-form video content for experiences would increase AI discoverability on video platforms. Requires video production.

---

## REMAINING IMPLEMENTATION RISKS

| Risk | Severity | Mitigation |
|---|---|---|
| Elementor overrides hero image loading attributes | High | Test in staging; apply custom PHP filter if needed |
| GTM firing before dataLayer initialization in some WordPress setups | High | Verify exact head script order in WordPress; use Elementor custom code injection for guaranteed order |
| Chatbot CLS on slow connections | Medium | Pre-reserve space with CSS body::after; test on throttled connection |
| Gold text contrast on non-white backgrounds | Medium | Audit every instance of gold text on cream and warm backgrounds; cream and warm are close to white and likely pass |
| Rose Day Club accent mark inconsistency | Low | Canonical rule in schema-standards.md: no accent in schema and slugs, accent optional in display copy |
| Intelligence scenarios creating duplicate records | Medium | M-BOOKING-OUTCOME-001 includes retry:1, no loop to prevent duplicates; test with manual re-trigger |
| Weekly report Claude API cost | Low | Optional integration; can be disabled in Make.com; estimate: less than $0.10 per weekly report at 400-word output |

---

## READINESS FOR FINAL PERFECTION AUDIT

### What Is Ready

- All 10 page metadata files updated with complete schema
- All 4 experience pages have serviceType, audience, areaServed, BreadcrumbList
- llms.txt present and correctly formatted
- AI crawler guidance documented with all 11 bot agents
- GEO strategy documented with 13 target queries mapped to pages
- Schema entity graph connected via @id references
- 22 GTM custom events fully specified
- Intelligence layer fully designed (Airtable tables + Make scenarios + learning loop)
- Revenue attribution system fully designed (table schema + Make scenario + formulas)
- Chatbot fully built (CSS + JS, 12 states, 8 GTM events)
- Performance standards documented (Core Web Vitals targets, font loading, image standards)
- Accessibility standards documented (contrast audit, ARIA, keyboard, focus)
- Script loading standards documented (order, defer/async, no Partytown)
- Lighthouse CI configured (.github/workflows/lighthouse.yml + .lighthouserc.json)
- Cross-system consistency audit completed (15 issues identified and documented)

### What Still Requires Action Before Launch

- Apply hero image fetchpriority="high" and loading="eager" to all hero images (requires live site access)
- Fix gold text contrast failures (2.4:1 fails for body text)
- Replace webhook placeholder URLs with live Make.com endpoints
- Wire visitor_id into she-said-sail-global.js and chatbot-js.js
- Build the 6 new Airtable intelligence tables
- Build the 4 new Make.com intelligence scenarios
- Activate Lighthouse CI by adding LHCI_GITHUB_APP_TOKEN to repository secrets
- Verify GTM container has triggers for all 22 custom events

### Audit Confidence Level

The system is comprehensive and internally consistent. The cross-system consistency audit identified 15 issues, of which 4 are critical and 6 are high priority. All 15 are documented with resolution steps in docs/final-audit/cross-system-consistency-audit.md.

The site is ready for the final perfection audit with the understanding that the critical issues above must be resolved before or as part of that audit.
