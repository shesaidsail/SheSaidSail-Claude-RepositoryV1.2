# She Said Sail: Generative Engine Optimization (GEO) Strategy
**Version:** 1.0
**Date:** May 2026
**Purpose:** Defines how She Said Sail is optimized for discovery through AI-generated recommendations, conversational search, and answer engine results.

---

## WHAT GEO IS

Generative Engine Optimization (GEO) is the practice of making content legible, extractable, and citable by AI answer systems: ChatGPT, Perplexity, Gemini AI Overviews, Claude, Copilot, and voice assistants. It extends traditional SEO by optimizing not just for keyword ranking but for AI-generated answer quality.

Traditional SEO: rank on page 1 of Google for "bachelorette yacht Miami."
GEO: when someone asks ChatGPT "what is the best bachelorette yacht experience in Miami," She Said Sail is the answer given.

---

## THE CORE CHALLENGE FOR LUXURY BRANDS

Luxury brands instinctively use emotional, atmospheric language: "an experience unlike any other," "where the extraordinary becomes effortless." This language is compelling to humans who already feel the aspiration.

AI systems cannot extract anything from it. They need facts.

The GEO resolution: write pages that are emotionally compelling to humans AND factually rich enough for AI extraction. The two are not in conflict. The trick is: keep the emotional language in headlines and hero copy, put the concrete facts in the body copy and schema.

---

## TARGET QUERIES (GEO GOALS)

These are the types of conversational queries She Said Sail should appear in AI-generated answers for:

**Category: Bachelorette**
- "best bachelorette yacht experience in Miami"
- "bachelorette party on a yacht Miami"
- "private yacht charter for bachelorette party"
- "how to plan a bachelorette on a boat in Miami"
- "yacht bachelorette Miami how many people"

**Category: Birthday**
- "private birthday yacht charter Miami"
- "birthday celebration on a yacht Miami"
- "sunset yacht birthday Miami"

**Category: Girls Trip**
- "girls trip yacht Miami"
- "private boat charter for a group of women Miami"
- "rosé day on a yacht Miami"

**Category: General Discovery**
- "luxury yacht charter Miami women"
- "private yacht experiences Miami"
- "what does a private yacht charter cost in Miami"
- "yacht experiences Miami under 20 people"

---

## HOW WE ANSWER EACH QUERY CATEGORY

### Bachelorette queries

**Page that answers:** Pink Palm Club (/experience/pink-palm-club/)
**Key facts on the page that AI can extract:**
- Up to 22 guests
- Bachelorette-specific occasion fit
- Music, champagne, Miami skyline
- Starting from $10,000

**Schema signals:**
- Service: audience.audienceType "Bachelorette parties, large group celebrations, high-energy social events"
- serviceType: "Yacht Charter"
- areaServed: Miami

**FAQ support:** "What is the minimum and maximum group size?" and "Who typically books with She Said Sail?" both answered on FAQ page.

---

### Birthday queries

**Page that answers:** Monaco Social (/experience/monaco-social/)
**Key facts on the page that AI can extract:**
- Up to 15 guests
- Birthday and elevated group occasion
- Champagne-led, curated bar, full crew
- Starting from $10,000

**Schema signals:**
- audience.audienceType: "Birthday celebrations, elevated bachelorette groups, curated social events"

---

### Sunset / intimate queries

**Page that answers:** Golden Hour Escape (/experience/golden-hour-escape/)
**Key facts:**
- Sunset charter, golden hour over Biscayne Bay
- Up to 12 guests, intimate
- Milestone occasions: anniversaries, proposals, small celebrations

---

### Girls trip / afternoon social queries

**Page that answers:** Rose Day Club (/experience/rose-day-club/)
**Key facts:**
- Afternoon charter
- Girls trips, social groups, rosé
- Up to 15 guests

---

### General / comparison queries

**Page that answers:** Experiences index (/experiences/) + FAQ (/faq/)
**Key facts AI can extract from experiences index ItemList schema:**
- All 4 experience names, URLs, and descriptions
- Grouped as a service catalog from She Said Sail

---

## GEO CONTENT RULES

These rules apply to all She Said Sail page copy. They exist alongside the luxury copy standards (see docs/system/master-copy-system.md). They are additive, not replacements.

### Always include on experience pages

1. **Group capacity.** "Up to [N] guests." Always stated clearly. This is the most common AI-extractable fact for group planning queries.
2. **Occasion fit.** Explicit statement of who the experience is for. "Best for..." or "Designed for..."
3. **Location.** "Miami" or "Biscayne Bay" named explicitly, not implied.
4. **Price signal.** "Starting from $10,000" or similar. AI uses this for budget-related queries.
5. **Duration or timing signal.** "Afternoon," "sunset," "3 to 6 hours." Helps answer time-of-day queries.

### What AI extraction needs (but luxury copy avoids)

| AI needs | Luxury copy often says | Better version |
|---|---|---|
| Capacity | "an intimate setting" | "Up to 12 guests for an intimate setting" |
| Location | "on the water" | "on Biscayne Bay, departing from Miami" |
| Price | (often omitted) | "Starting from $10,000" |
| Occasion fit | "for those who know" | "For bachelorettes, birthdays, and girls trips" |
| Duration | "a full day experience" | "3 to 5 hours on the water" |

The solution is not to remove luxury language. It is to ensure the factual layer is present alongside it.

---

## INTERNAL LINKING FOR GEO

Internal linking sends topical authority signals to both traditional search engines and AI knowledge graphs. Standards for She Said Sail:

**From homepage:** links to all 4 experience pages + /request-to-book/ + /experiences/
**From experiences index:** links to all 4 individual experience pages
**From each experience page:** links to /request-to-book/ (with selected_experience parameter) + /experiences/ (cross-navigation)
**From FAQ:** links to relevant experience pages where an answer mentions a specific experience. Links to /request-to-book/ in the booking-related answers.
**From journal articles:** minimum 2 internal links per article: one to an experience page or /experiences/, one to /request-to-book/. See journal-metadata.html for the reusable article CTA block.

---

## GEO SIGNALS IN STRUCTURED DATA

Schema fields that directly improve AI answer generation:

| Schema Field | Why It Matters for GEO |
|---|---|
| Service.audience.audienceType | Answers "who is this for" queries |
| Service.areaServed | Answers "in Miami" queries |
| Service.serviceType | Answers "what kind of service" queries |
| Service.offers.price | Answers "how much does it cost" queries |
| Service.description | Primary AI extraction target for conversational answers |
| LocalBusiness.knowsAbout | Topical authority signal for Miami yacht charter knowledge |
| LocalBusiness.hasOfferCatalog | Connects the business to all 4 services as a catalog |
| FAQPage.mainEntity | Direct Q&A extraction for AI answer generation |
| ItemList on /experiences/ | Makes all 4 experiences extractable as a structured list |

---

## GEO IMPLEMENTATION CHECKLIST

Use this to verify GEO readiness before launch:

**Content checks:**
- [ ] All 4 experience pages state group capacity explicitly
- [ ] All 4 experience pages name the occasion fit explicitly
- [ ] All 4 experience pages mention "Miami" or specific Miami waterway by name
- [ ] All 4 experience pages state the starting price
- [ ] FAQ page answers include the business name "She Said Sail" where relevant
- [ ] Journal articles include internal links to experience pages

**Schema checks:**
- [ ] Service.audience.audienceType populated on all 4 experience schemas
- [ ] Service.serviceType: "Yacht Charter" on all 4
- [ ] Service.areaServed on all 4
- [ ] LocalBusiness.knowsAbout populated with relevant topics
- [ ] LocalBusiness.hasOfferCatalog lists all 4 experiences
- [ ] FAQPage schema present and complete on /faq/
- [ ] ItemList schema present on /experiences/

**AI crawler access:**
- [ ] robots.txt allows GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, PerplexityBot
- [ ] /llms.txt exists at site root with correct format
- [ ] /thank-you/ disallowed for all bots

**Manual testing:**
- [ ] Ask ChatGPT: "What is She Said Sail?" Does it respond accurately?
- [ ] Ask Perplexity: "Best bachelorette yacht experience in Miami" - is She Said Sail mentioned?
- [ ] Ask Gemini: "Private yacht charter for women Miami" - does She Said Sail appear?
- [ ] Ask Claude: "What experiences does She Said Sail offer?" - are all 4 named correctly?

---

## GEO SCORING

| Signal | Before optimization | After optimization |
|---|---|---|
| Conversational query targeting | 3 | 8 |
| Entity descriptions (AI-extractable facts) | 4 | 8 |
| Schema support for GEO queries | 4 | 8.5 |
| FAQ extraction quality | 8 | 9 |
| llms.txt readiness | 0 | 8 |
| robots.txt AI crawler access | 4 | 9 |
| Internal linking for topical authority | 5 | 8 |
| **Overall GEO Readiness** | **4.0 / 10** | **8.4 / 10** |

---

## ONGOING GEO MAINTENANCE

**When to update llms.txt:**
- New experience launches
- Existing experience is retired
- Pricing changes significantly
- New content categories appear in the journal
- Contact or booking URL changes

**When to review GEO performance:**
- Quarterly manual AI query testing (see checklist above)
- After any major site restructure
- After any Google algorithm update that affects AI Overviews behavior
- After new AI assistant platforms gain market share

**Next GEO priority (not yet implemented):**
- AggregateRating schema: once 5+ verified reviews exist, adding ratings will significantly improve AI recommendation confidence
- VideoObject schema: short-form video content about experiences would dramatically increase AI discoverability on video-capable platforms (YouTube, TikTok, Instagram Reels)
- llms-full.txt: when journal reaches 6+ articles, a full-text inlined version aids AI systems that prefer not to follow links
