# Journal Page Audit
Page: /journal/
File: journal-audit.md

Scoring scale: 1 (critical gap) to 10 (fully optimized). Each dimension is scored independently.

---

## Before: No Journal, or Default WordPress Blog

State: either no journal section exists, or the site uses a default WordPress blog at /blog/ with no brand styling, no article schema, and no internal linking standard.

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Luxury Positioning | 2 | A default WordPress blog template signals a generic web presence. Serif display fonts and the brand color palette are absent. The experience does not match the caliber of the charter product. |
| Emotional Conversion | 3 | No editorial content means no opportunity to build desire before a visitor reaches the booking page. Traffic that lands on a generic blog is unlikely to continue deeper into the site. |
| Mobile UX | 4 | Default WordPress themes are technically responsive, but the reading experience is not tuned for a luxury audience on mobile. Typography, spacing, and image handling are generic. |
| Trust and Social Proof | 4 | Without editorial content, the brand cannot demonstrate expertise in women-led celebrations, Miami yacht culture, or occasion planning. There is nothing for a researching visitor to engage with. |
| Backend Readiness | 8 | No backend is required for a blog. Score is high because the absence of a form means no backend risk either. WordPress posts are straightforward to manage. |
| Analytics Readiness | 2 | No named custom event exists for journal or blog page views. Organic traffic to the journal cannot be segmented or remarketed. Scroll depth events are absent. |
| SEO | 3 | Default WordPress blog behavior produces generic titles and no structured schema. No targeted meta descriptions. No internal linking standard. The page is not optimized for the search queries the target audience actually uses. |
| Performance | 6 | Default themes load acceptably but carry theme bloat and often load unused CSS and JavaScript. No image optimization standard is in place. |

Overall Before Score: 4.0

---

## After: Structured Journal with Brand Styling, Article CTA Blocks, Schema Template, and Analytics

State: the journal section exists at /journal/ with the branded header, article card grid, Article Page CTA Block on every article, article metadata template with JSON-LD schema, internal linking standard, and the view_journal_page event active in GTM.

| Dimension | Score | Rationale |
|-----------|-------|-----------|
| Luxury Positioning | 8 | Cormorant Garamond display titles, Inter body text, gold category pills, and the cream/navy color palette create a magazine-quality editorial environment. The journal feels like an intentional brand publication, not an afterthought. |
| Emotional Conversion | 7 | The journal converts indirectly. Readers who arrive via organic search, engage with an article, and encounter the Article Page CTA Block are moved toward /experiences/ and /request-to-book/. Conversion is not immediate but builds intent over multiple touchpoints. A 7 reflects the indirect nature of editorial conversion versus a direct CTA page. |
| Mobile UX | 8 | Cards collapse to a single column. Image aspect ratios are preserved. CTA buttons stack full width. Typography is readable at 375px. The one-column card layout on mobile is clean and unhurried. |
| Trust and Social Proof | 8 | Editorial articles on bachelorette planning, girls trip logistics, and on-the-water experiences signal genuine expertise. A guest stories article directly amplifies social proof. The journal format positions She Said Sail as a credible authority, not just a booking service. |
| Backend Readiness | 9 | No form means no backend complexity on the journal. The internal linking standard is documented clearly, and the Article Page CTA Block ensures every article creates a path to the booking form. The 9 (not 10) reflects that WordPress permalink configuration still needs to be confirmed. |
| Analytics Readiness | 8 | view_journal_page fires on index page load. Scroll depth events cover the index. click_request_to_book and click_explore_experiences fire from article CTAs. The GA4 audience "Journal Readers - No Form Submit" is defined for remarketing. The gap to a 10 is the absence of a view_article_page event for individual article tracking, which is documented as a recommended future enhancement. |
| SEO | 8 | Targeted title and meta description. Canonical set correctly. CollectionPage JSON-LD schema on the index. Article JSON-LD schema template provided for every post. Internal linking standard ensures crawl depth. The gap to a 10 is that schema must be applied post by post in Yoast or RankMath and that the framework provides the structure but cannot write the actual articles. |
| Performance | 7 | Snippet-based implementation with no new JavaScript dependencies. CSS is scoped with .sss-jnl-* prefixes. Image aspect-ratio preservation prevents layout shift. The gap to a higher score reflects that actual image optimization, lazy loading, and Core Web Vitals tuning depend on the WordPress theme and hosting environment, which are outside this framework's scope. |

Overall After Score: 7.9

---

## Score Change Summary

| Dimension | Before | After | Change |
|-----------|--------|-------|--------|
| Luxury Positioning | 2 | 8 | +6 |
| Emotional Conversion | 3 | 7 | +4 |
| Mobile UX | 4 | 8 | +4 |
| Trust and Social Proof | 4 | 8 | +4 |
| Backend Readiness | 8 | 9 | +1 |
| Analytics Readiness | 2 | 8 | +6 |
| SEO | 3 | 8 | +5 |
| Performance | 6 | 7 | +1 |
| Overall | 4.0 | 7.9 | +3.9 |

---

## Remaining Gaps and Next Steps

The framework is complete. The following items must be completed by the site owner or content team to close the remaining gaps.

1. Articles must be written. The framework documents the structure, card format, internal linking standard, and SEO metadata template. None of this generates actual article content. Six article topics are identified in the brief. A content calendar and author assignment are needed before the journal can drive organic traffic.

2. Article JSON-LD schema must be applied per post. The template in journal-metadata.html provides the exact schema structure. Each article requires its own schema entry in Yoast SEO or RankMath with the correct headline, datePublished, image URL, and article slug. This cannot be automated without a custom plugin or theme modification.

3. The /journal/ permalink must be confirmed active in WordPress. If the site currently uses /blog/, a 301 redirect from /blog/ to /journal/ is required. The WordPress permalink settings and any custom post type registration must produce /journal/[article-slug]/ URLs before articles are published.

4. view_article_page event is a recommended future enhancement. The global JS currently does not distinguish individual article page views from other page views. Adding a named event with an article_slug parameter would enable per-article performance tracking in GA4 and more granular funnel analysis. The implementation approach is documented in journal-analytics.md.
