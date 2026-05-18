# She Said Sail: AI Search Standards References Incorporated
**Version:** 1.0
**Date:** May 2026
**Purpose:** Documents the external standards and references that informed the She Said Sail AI search and GEO optimization system. This file is a reference record, not a deployment guide.

---

## REFERENCE 1: llmstxt.org

**URL:** https://llmstxt.org
**Standard:** llms.txt File Format Specification
**Proposed by:** Jeremy Howard (Answer.AI), 2024

### What the standard defines

llms.txt is a plain-text markdown file placed at the root of a website (alongside robots.txt and sitemap.xml). Its purpose is to provide LLMs with a structured, token-efficient summary of a site's content and priorities.

**Specification requirements:**

| Element | Status | Description |
|---|---|---|
| H1 heading with site/project name | Required | The only mandatory element |
| Blockquote with brief project summary | Recommended | A 2-4 sentence brand summary |
| H2-delimited file lists | Optional | Sections grouping related links |
| File list format: `- [Title](url): Description` | Required for file lists | Markdown hyperlink with optional colon note |
| Optional section (H2: "Optional") | Special | Items in this section may be skipped if context is short |

**llms.txt vs. llms-full.txt:**
- llms.txt: Index file with links and short descriptions. Primary file.
- llms-full.txt (or llms-ctx.txt): Expanded version with full page content inlined. For AI systems that want the full text without following links.
- She Said Sail implements llms.txt only. A llms-full.txt can be added when the journal has substantial article volume.

**How AI systems use it:**
- Used at inference time when a user asks about the site
- Not primarily for training data (that is handled separately by crawlers)
- Signals content priority to the LLM when generating answers

### What we implemented

- Created `/llms.txt` in the site root following the exact specification format
- H1: She Said Sail
- Blockquote: canonical 3-sentence brand summary
- Sections: About, Experiences (4 experiences with entity descriptions), Booking, FAQ, Journal, Contact
- Optional section: all-experiences overview, legal pages
- All experience entries include: canonical name, occasion fit, group capacity, atmosphere descriptor, and URL
- File is entirely machine-readable markdown with no decorative formatting

---

## REFERENCE 2: Google Structured Data Documentation

**URL:** https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data
**Standard:** Google Search Structured Data Implementation Guidelines

### What the standard defines

Google supports three structured data formats: JSON-LD (recommended), Microdata, and RDFa. JSON-LD is the preferred choice because it does not require mixing markup with visible content.

**Key implementation requirements:**
- Structured data must describe visible page content only. Invisible content markup can result in penalties.
- Use the Rich Results Test tool to validate all schema before deployment.
- Required and recommended properties vary by schema type. Missing required properties disqualifies rich result eligibility.
- Monitor Search Console rich result status reports after deployment.

**AI Overviews implications:**
- Google's AI Overviews draw from structured data for entity understanding, particularly Organization, LocalBusiness, FAQPage, and Service types.
- FAQPage schema is a direct input to answer extraction for question-based queries.
- Accurate, complete structured data increases the likelihood of appearing in AI Overview summaries.

**Validation tool:** https://search.google.com/test/rich-results

### What we implemented based on this reference

- All JSON-LD blocks contain only information visible on the page (no hidden meta markup)
- Added complete required and recommended properties to all Service schemas
- FAQPage schema on /faq/ has 19 complete Question entities, all matching visible page content
- LocalBusiness schema upgraded with more specific properties (foundingDate, hasOfferCatalog, knowsAbout)
- Breadcrumb schemas added to all experience pages and About page
- WebSite schema with SearchAction added to global schema
- Deployment instructions specify Rich Results Test validation before going live

---

## REFERENCE 3: Schema.org

**URL:** https://schema.org
**Standard:** Schema.org Vocabulary (LocalBusiness, Service, Organization, FAQPage, CollectionPage, Article, BreadcrumbList, WebSite)

### Key findings by schema type

**LocalBusiness (used in global-schema.html, all pages):**
- Inherits from both Organization and Place
- Most important properties: name, address, telephone, url, openingHours, aggregateRating, priceRange
- Added in this pass: foundingDate, hasOfferCatalog (linking all 4 experiences), knowsAbout (topical authority signals), @id for linked data entity referencing, serviceArea
- aggregateRating not yet added: requires verified review data. Will be added once the business has published Google reviews.

**Service (used on all 4 experience pages):**
- Core properties: name, description, provider, serviceType, areaServed, offers, audience
- provider should reference the parent LocalBusiness/Organization using @id
- Added in this pass: serviceType ("Yacht Charter"), audience with audienceType, areaServed with City entity, availability on Offer, url on Offer, BreadcrumbList schema on each experience page

**Organization (used on About page):**
- Added: @id, knowsAbout, hasOfferCatalog, foundingDate
- sameAs: Instagram URL placeholder (to be updated before go-live)

**FAQPage (used on /faq/):**
- Already complete from prior optimization pass: 19 Question entities
- All answers match visible page copy exactly (per Google's requirement)
- No changes needed

**WebSite (new, added to global-schema.html):**
- Provides site-level entity definition
- potentialAction: SearchAction enables sitelinks search box eligibility in Google

**BreadcrumbList (improved):**
- Previously only on homepage
- Now added to: all 4 experience pages, About page, Experiences index

**CollectionPage (existing on Journal index, Experiences index):**
- Unchanged. Already correctly structured.

**Article (template in journal-metadata.html):**
- Unchanged. Template is correct.

### @id linked data implementation

Per schema.org best practices for linked data, entities are now connected using @id references:
- Organization @id: "https://shesaidsail.com/#organization"
- WebSite @id: "https://shesaidsail.com/#website"
- All Service schemas reference provider with @id: "https://shesaidsail.com/#organization"
- This allows AI systems and Google to build an entity graph connecting the business to its services

---

## REFERENCE 4: OpenAI Bot Documentation

**URL:** https://platform.openai.com/docs/bots (returned 403, used known published spec)
**Standard:** GPTBot, ChatGPT-User, OAI-SearchBot user agents and crawl policy

### Known OpenAI bot specifications

| Bot | User Agent | Purpose |
|---|---|---|
| GPTBot | Mozilla/5.0 ... GPTBot/1.1 | Training data crawl |
| ChatGPT-User | Mozilla/5.0 ... ChatGPT-User/1.1 | Real-time ChatGPT browsing |
| OAI-SearchBot | Mozilla/5.0 ... OAI-SearchBot/1.1 | ChatGPT web search |

**Robots.txt control (per OpenAI documentation):**

To allow all OpenAI bots:
```
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: OAI-SearchBot
Allow: /
```

To block specific paths from GPTBot (e.g., thank-you page which should not be indexed):
```
User-agent: GPTBot
Disallow: /thank-you/
```

### Other major AI crawler bots

| Bot | Publisher | User Agent Fragment |
|---|---|---|
| ClaudeBot | Anthropic | ClaudeBot/1.0 |
| PerplexityBot | Perplexity AI | PerplexityBot/1.0 |
| Googlebot | Google | Googlebot/2.1 |
| Bingbot | Microsoft | bingbot/2.0 |
| Applebot | Apple (Siri/AI) | Applebot/0.1 |
| Diffbot | Diffbot | Diffbot/3.0 |

### What we implemented

See: `docs/ai-search/ai-crawler-guide.md` for the full robots.txt template with AI crawler directives.

---

## STANDARDS SUMMARY: WHAT WAS CHANGED

| Standard | Improvement Made |
|---|---|
| llmstxt.org | Created /llms.txt in correct specification format |
| Google Structured Data | All JSON-LD validated against visible content. Breadcrumbs added. WebSite schema added. |
| Schema.org LocalBusiness | foundingDate, knowsAbout, hasOfferCatalog, @id, serviceArea added |
| Schema.org Service | serviceType, audience, areaServed, availability, @id provider reference added to all 4 |
| Schema.org Organization | @id, knowsAbout, hasOfferCatalog, foundingDate added |
| Schema.org WebSite | New schema added to global block with SearchAction |
| Schema.org BreadcrumbList | Expanded from homepage-only to all experience pages and About |
| OpenAI / AI crawlers | robots.txt addendum created with explicit bot directives |

---

## WHAT THESE STANDARDS DO NOT YET COVER

1. **aggregateRating / Review schema:** Both Google and schema.org recommend these for rich results and trust signals. She Said Sail does not yet have published Google reviews. Add once reviews exist.

2. **speakable schema:** Google's speakable property marks content suitable for text-to-speech / voice assistants. It is experimental and not yet widely validated. Add after core schema is confirmed clean.

3. **VideoObject schema:** If video content is added to experience pages or journal articles, VideoObject schema will significantly increase AI discoverability.

4. **Event schema:** If She Said Sail runs recurring themed departures on specific dates, Event schema (with startDate, endDate, location, offers) would add discoverability for date-specific queries.

5. **llms-full.txt:** A full-text expanded version for AI systems that prefer inlined content. Implement once the journal has 6+ articles.
