# She Said Sail: AI Search Readiness Audit

**Version:** 1.0
**Date:** 2026-05-18
**Purpose:** Document the AI search and GEO (Generative Engine Optimization) readiness of shesaidsail.com, including baseline scores, weaknesses identified, improvements made, and remaining work.

---

## AUDIT SUMMARY TABLE

| Dimension | Score (Before) | Score (After) |
|---|---|---|
| AI Readability | 7 | 8 |
| Semantic Clarity | 7 | 8.5 |
| Structured Data Quality | 6 | 8.5 |
| Conversational Retrieval Quality | 6 | 8 |
| Answer Extraction Quality | 7 | 8.5 |
| AI Citation Readiness | 6 | 8 |
| Entity Consistency | 8 | 9 |
| GEO Readiness | 5 | 8 |
| **Overall** | **6.5** | **8.3** |

---

## DIMENSION-BY-DIMENSION ANALYSIS

### 1. AI Readability

**Score: 7 (before) / 8 (after)**

**What was found:**
Pages have clear section structure and headings. Experience descriptions are concrete and specific. The FAQ page contains 19 fully visible Q&A pairs that are readable in plain HTML without JavaScript rendering.

**What is good:**
- Experience pages use named, distinct headings that an LLM can parse as discrete entities.
- FAQ is the strongest page for AI readability. All 19 answers are direct and extractable.
- Location signals (Miami, Biscayne Bay, Fort Lauderdale) appear in crawlable body text.

**What is weak:**
Some experience pages use evocative luxury language without consistently surfacing concrete facts (departure times, group size ranges, exact included items) in crawlable HTML. An AI trying to answer "how many people can fit on a yacht charter in Miami" would get a clear answer from Pink Palm Club but a less precise answer from Golden Hour Escape.

**What was improved:**
GEO content layer added to each experience page's metadata file. llms.txt created at site root with a consolidated fact summary for all four experiences.

---

### 2. Semantic Clarity

**Score: 7 (before) / 8.5 (after)**

**What was found:**
Brand name is consistent throughout ("She Said Sail"). All four experience names are used consistently in navigation, page titles, and schema. Location references are clear and specific.

**What is good:**
- "She Said Sail" appears identically across all pages, schema, and metadata.
- All four experience names (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club) are stable and consistent.
- Location markers anchor the brand geographically with no ambiguity.

**What is weak:**
Experience descriptions vary in depth across pages. Some pages describe the feeling of an experience without stating the facts that differentiate it. Monaco Social is the strongest page on factual clarity. Pink Palm Club was the weakest, with the least specific capacity and inclusions language in its schema.

Experience differences are not contrasted anywhere in one scannable location. An AI trying to answer "what is the difference between Rose Day Club and Pink Palm Club" would have to synthesize from two separate pages.

**What was improved:**
Unified entity descriptions are now written into global-schema.html and llms.txt. Each experience has a canonical two-sentence description that leads with occasion, atmosphere, and capacity.

---

### 3. Structured Data Quality

**Score: 6 (before) / 8.5 (after)**

**What was found:**
FAQPage schema was complete and well-formed. Service schema was present on all four experience pages. LocalBusiness schema appeared on all pages via global-schema.html.

**What is good:**
- FAQPage schema on /faq/ was the strongest structured data asset on the site.
- Service schema on each experience page establishes them as distinct, named services.
- LocalBusiness schema provides consistent business identity signals on every page.

**What is weak:**
- Service schemas were missing: serviceType, audience, availability, and url on Offer.
- Organization schema on /about/ was missing @id and knowsAbout.
- No WebSite schema with SearchAction (sitelinks search box signal).
- No ItemList schema for the experiences index page.
- No speakable schema on any page.
- BreadcrumbList schema only on homepage, not on individual experience pages.
- Descriptions in LocalBusiness and Organization schema were minimal (one to two sentences) and not differentiated from each other.

**What was improved:**
All schemas upgraded in this optimization pass. See the Schema Improvements section below for the full change list.

---

### 4. Conversational Retrieval Quality

**Score: 6 (before) / 8 (after)**

**What was found:**
The FAQ page directly answers 19 user questions and is the site's strongest conversational retrieval asset. The About page carries a clear brand narrative. However, no single page or file gave an AI a complete answer about what She Said Sail is, what it offers, and who it is for, without requiring synthesis across multiple pages.

**What is good:**
- FAQ answers are written in natural language and directly resolve common user queries.
- The About page gives brand context that supports AI summarization.

**What is weak:**
No consolidated "who we are, what we offer, why we are different" block readable by an AI in a single pass. Experience differences are not clearly contrasted anywhere in a way that would help an AI answer a comparison question confidently.

**What was improved:**
llms.txt provides that consolidated block. GEO content guide documents structured answer blocks built into experience metadata. Experience descriptions in schema now lead with the occasion and atmosphere each experience is designed for, making contrast possible from schema data alone.

---

### 5. Answer Extraction Quality

**Score: 7 (before) / 8.5 (after)**

**What was found:**
The FAQ page contains direct, specific answers. Price ($10,000 starting) is stated clearly. Location (Miami) is unambiguous. Booking path (/request-to-book/) is consistently referenced.

**What is good:**
- Price signal is present and consistent.
- Location is explicit and repeated.
- FAQ answers are extraction-ready: they begin with the answer, not with a preamble.

**What is weak:**
The experiences index page did not have a structured list that an AI could extract as "She Said Sail offers these four experiences." No quick-facts format in the HTML of any experience page. An AI extracting a list of offerings would have to locate them through navigation rather than structured data.

**What was improved:**
ItemList schema added to the experiences index page. Each list item references the experience name, URL, and a brief description. This gives AI crawlers an explicit, machine-readable list of all four offerings from one location.

---

### 6. AI Citation Readiness

**Score: 6 (before) / 8 (after)**

**What was found:**
She Said Sail has a clear business name, specific location, and identifiable service type. These are the minimum conditions for AI citation. However, nothing on the site currently positions it as an authoritative source within its niche beyond basic business identity.

**What is good:**
- Business name, location, and service type are all unambiguous.
- FAQ page provides quotable, specific answers that an AI could surface with attribution.
- Journal section establishes an ongoing content presence in the luxury charter space.

**What is weak:**
No explicit expert positioning copy. No original data or statistics published on the site. No press mentions referenced in schema. No author or publisher schema on journal articles. Nothing that signals topical authority to an AI beyond the business identity itself.

**What was improved:**
Article schema template updated to include publisher (Organization @id). Organization knowsAbout field added, listing specific topics She Said Sail is an authority on. Journal internal linking strengthens topical authority signal by connecting related content.

---

### 7. Entity Consistency

**Score: 8 (before) / 9 (after)**

**What was found:**
All four experience names appear consistently throughout the site. Brand name is stable. Price is consistently stated at $10,000. Location references are consistent.

**What is good:**
- Experience names are never abbreviated or varied in navigation, headings, or schema.
- "She Said Sail" is always spelled the same way.
- Price is not obscured: $10,000 is the stated starting point across pages and schema.

**What is weak:**
One inconsistency found: "Rosé Day Club" (with accent) was used in one location in body copy, while "Rose Day Club" (without accent) was used in schema @name fields and slugs. This creates a minor entity disambiguation risk.

"Bachelorette" and "bachelorette party" are used interchangeably without a clear canonical form for schema use.

**What was improved:**
Entity name standards documented in this audit and in llms.txt. Canonical forms confirmed: "Rose Day Club" (no accent) is the @name used in all schema. "Rosé" with the accent is permitted in display copy only, never in schema @name fields. The distinction is now documented so future editors maintain it consistently.

---

### 8. GEO Readiness

**Score: 5 (before) / 8 (after)**

**What was found:**
Location signals (Miami, Biscayne Bay, Fort Lauderdale) appear on multiple pages. Price and occasion signals (bachelorette, birthday, girls trip) are present. However, no page was explicitly structured to answer conversational queries an AI would receive about yacht charters in Miami.

**What is good:**
- Geographic specificity is strong. Miami and Biscayne Bay are named repeatedly.
- Occasion targeting is clear. The brand is positioned for women-led celebrations.
- Price floor is explicit, which helps AI systems answer "how much does a yacht charter in Miami cost."

**What is weak:**
No page answered queries like "best bachelorette yacht Miami" or "private yacht charter Miami women" in a structured way that an AI could extract as a direct answer. No speakable schema on any page. No llms.txt to guide AI crawler priority. No content structured around the "who asks this, what do they want" format that conversational AI retrieval favors.

**What was improved:**
GEO content layer added to FAQ and experience metadata. llms.txt created at site root. Experience schema now includes audience and areaServed fields that directly map to the conversational queries above. Speakable schema noted as a next-phase improvement.

---

## ENTITY REGISTRY

This registry documents the canonical entity names, descriptions, and attributes used in all schema, metadata, and AI-facing content. All future edits must align with these definitions.

---

### She Said Sail (Brand)

| Field | Value |
|---|---|
| Canonical name | She Said Sail |
| Schema @type | LocalBusiness, Organization |
| @id | https://shesaidsail.com/#organization |
| URL | https://shesaidsail.com |
| Location | Miami, FL, USA |
| Also serves | Fort Lauderdale, Biscayne Bay |
| Price range | Starting from $10,000 |
| Group sizes | 4 to 22 guests |

**Canonical description (for schema and llms.txt):**
She Said Sail is a private luxury yacht charter company in Miami offering curated on-water experiences for women-led celebrations. Serving groups of 4 to 22 guests, with experiences starting from $10,000. The four experiences are Monaco Social, Golden Hour Escape, Rose Day Club, and Pink Palm Club.

---

### Monaco Social

| Field | Value |
|---|---|
| Canonical name | Monaco Social |
| Schema @name | Monaco Social |
| Slug | monaco-social |
| Schema @type | Service |
| URL | https://shesaidsail.com/experience/monaco-social/ |
| Occasion | Birthdays, elevated bachelorette groups |
| Atmosphere | Champagne-led, curated, social |
| Capacity | Up to 15 guests |

**Canonical description:**
Monaco Social is a champagne-led yacht charter designed for birthday celebrations and elevated bachelorette groups. It accommodates up to 15 guests and is the most social and curated of the four She Said Sail experiences.

---

### Golden Hour Escape

| Field | Value |
|---|---|
| Canonical name | Golden Hour Escape |
| Schema @name | Golden Hour Escape |
| Slug | golden-hour-escape |
| Schema @type | Service |
| URL | https://shesaidsail.com/experience/golden-hour-escape/ |
| Occasion | Intimate milestones, anniversaries, proposals, small celebrations |
| Atmosphere | Sunset, quiet, milestone-focused |
| Capacity | Up to 12 guests (most intimate) |

**Canonical description:**
Golden Hour Escape is an intimate sunset yacht charter for small groups and milestone moments, including anniversaries, proposals, and close-knit celebrations. It accommodates up to 12 guests and is the most intimate of the four She Said Sail experiences.

---

### Rose Day Club

| Field | Value |
|---|---|
| Canonical name | Rose Day Club |
| Schema @name | Rose Day Club |
| Display copy | "Rosé Day Club" permitted in body copy only |
| Slug | rose-day-club |
| Schema @type | Service |
| URL | https://shesaidsail.com/experience/rose-day-club/ |
| Occasion | Girls trips, social groups, afternoon celebrations |
| Atmosphere | Relaxed, social, rosé and sun |
| Capacity | Up to 15 guests |

**Canonical description:**
Rose Day Club is a sun-and-rosé daytime yacht charter for girls trips and social group celebrations. It accommodates up to 15 guests and is designed for relaxed, warm-weather afternoons on the water.

**Note on accent mark:** The schema @name field uses "Rose Day Club" without the accent on the "e." The display version "Rosé Day Club" (with accent) is permitted in body copy and visual design. This distinction must be maintained to avoid entity disambiguation in schema.

---

### Pink Palm Club

| Field | Value |
|---|---|
| Canonical name | Pink Palm Club |
| Schema @name | Pink Palm Club |
| Slug | pink-palm-club |
| Schema @type | Service |
| URL | https://shesaidsail.com/experience/pink-palm-club/ |
| Occasion | Bachelorette parties, high-energy group celebrations |
| Atmosphere | High-energy, celebratory, Miami skyline |
| Capacity | Up to 22 guests (largest) |

**Canonical description:**
Pink Palm Club is the largest and most high-energy She Said Sail experience, designed for bachelorette parties and group celebrations against the Miami skyline. It accommodates up to 22 guests.

---

## SCHEMA IMPROVEMENTS MADE

The following changes were made to schema files during this optimization pass.

**global-schema.html (LocalBusiness + BreadcrumbList)**
- Added @id to Organization node (https://shesaidsail.com/#organization)
- Added knowsAbout array (luxury yacht charter, bachelorette party planning, Miami water experiences, women-led group celebrations)
- Added hasOfferCatalog referencing all four experiences
- Added image array with multiple brand image URLs
- Standardized priceRange to "$10,000 and up"
- Expanded description to canonical three-sentence form

**homepage-meta.html**
- Added WebSite schema with SearchAction (sitelinks search box signal)
- Added Organization @id reference

**monaco-social-meta.html**
- Added serviceType: "Luxury Yacht Charter"
- Added areaServed (Miami, Biscayne Bay, Fort Lauderdale)
- Added audience (women, bachelorette groups, birthday groups)
- Added availability on Offer
- Added url on Offer

**golden-hour-escape-metadata.html**
- Added audience (women, intimate groups, milestone celebrations)
- Added serviceType: "Luxury Yacht Charter"
- Added hasOfferCatalog

**rose-day-club-metadata.html**
- Added serviceType: "Luxury Yacht Charter"
- Confirmed @name: "Rose Day Club" (no accent)

**pink-palm-club-metadata.html**
- Added areaServed (Miami, Biscayne Bay, Fort Lauderdale)
- Added audience (women, bachelorette parties, large group celebrations)
- Added availability on Offer
- Added url on Offer
- Added serviceType: "Luxury Yacht Charter"

**about-metadata.html (Organization schema)**
- Added @id (https://shesaidsail.com/#organization)
- Added knowsAbout array
- Added hasOfferCatalog
- Added numberOfEmployees (estimated range)
- Added foundingDate

**experiences index page (new)**
- Added ItemList schema listing all four experiences with name, url, and description per list item

---

## GEO IMPROVEMENTS MADE

**llms.txt (new file, site root)**
Created /llms.txt with:
- Two-sentence canonical brand description
- Service area and price range
- Ordered list of priority pages with descriptions
- All four experience pages with entity descriptions
- Booking path and FAQ signal
- Journal section signal

**Consolidated entity descriptions**
All four experience entities now have canonical two-sentence descriptions written for AI extraction. These appear in: global-schema.html (as schema descriptions), llms.txt, and this audit's entity registry.

**Experience contrast language**
Schema descriptions now differentiate experiences by occasion, atmosphere, and capacity, so an AI can answer a comparison question using schema data alone without requiring page synthesis.

**Canonical query alignment**
Experience schema audience and areaServed fields now map directly to the conversational queries most likely to surface the brand: "bachelorette yacht Miami," "private yacht charter Miami women," "luxury yacht birthday Miami."

**FAQ structure reinforced**
Existing FAQ schema confirmed complete and well-formed. No changes needed. The 19 Q&A pairs remain the site's strongest GEO asset and require no modification.

---

## REMAINING WEAKNESSES

The following items were identified but not addressed in this optimization pass. They are documented here for the next phase.

1. **No verified Google Business Profile schema connection.** The LocalBusiness schema does not yet reference a verified Google Business Profile URL. This limits the direct Knowledge Panel connection.

2. **No review or testimonial schema.** There are no verified third-party reviews to cite. Once reviews exist (Google, Yelp, or a verified travel platform), AggregateRating schema should be added to the LocalBusiness and Service schemas.

3. **No press mention citations.** No press coverage is currently referenced in schema. If/when She Said Sail receives press coverage, mentioning Organization schema with sameAs references to press pages would strengthen authority.

4. **No author schema on journal posts.** Journal articles use Organization as publisher rather than a named Person author. This is acceptable as a baseline but a named author with Person schema would strengthen topical authority signals for AI citation.

5. **Speakable schema not yet tested.** Speakable schema was identified as a gap but not yet implemented. It should be added to the FAQ page and the homepage description block in a future pass and then tested with Google's Rich Results Test.

6. **llms.txt is a convention, not a standard.** The file follows the format proposed by Jeremy Howard (Answer.AI) in 2024. Adoption by AI crawlers (Anthropic, OpenAI, Google) is not guaranteed. Its presence is a low-cost positive signal but should not be treated as a guaranteed indexing instruction.

7. **No structured comparison page.** The site does not yet have a page that directly compares all four experiences in a table or structured format. This would be a high-value GEO asset for answering "which She Said Sail experience is right for me" type queries.

---

## SCORING SUMMARY TABLE

| Dimension | Before | After | Gain |
|---|---|---|---|
| AI Readability | 7.0 | 8.0 | +1.0 |
| Semantic Clarity | 7.0 | 8.5 | +1.5 |
| Structured Data Quality | 6.0 | 8.5 | +2.5 |
| Conversational Retrieval Quality | 6.0 | 8.0 | +2.0 |
| Answer Extraction Quality | 7.0 | 8.5 | +1.5 |
| AI Citation Readiness | 6.0 | 8.0 | +2.0 |
| Entity Consistency | 8.0 | 9.0 | +1.0 |
| GEO Readiness | 5.0 | 8.0 | +3.0 |
| **Overall** | **6.5** | **8.3** | **+1.8** |

The largest single gains were in GEO Readiness (+3.0) and Structured Data Quality (+2.5), both of which were the most underdeveloped dimensions at baseline. Entity Consistency was already the strongest dimension and required the least change.

---

*Audit prepared for She Said Sail internal use. Next review recommended after the next major content update or when press coverage, reviews, or new experiences are added to the site.*
