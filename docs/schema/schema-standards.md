# She Said Sail: Schema Implementation Standards
**Version:** 1.0
**Date:** May 2026
**Authority:** docs/ai-search/references-incorporated.md
**Purpose:** Defines the JSON-LD structured data standards for all She Said Sail pages. All schema must follow these standards before deployment.

---

## CORE PRINCIPLES

1. **JSON-LD only.** Google recommends JSON-LD. We do not use Microdata or RDFa. All schema is in `<script type="application/ld+json">` blocks.

2. **Visible content only.** Per Google's guidelines, structured data must describe content that is visible on the page. Do not add schema for information that is not shown to users.

3. **One entity, one @id.** The She Said Sail organization has one canonical @id: `https://shesaidsail.com/#organization`. All pages that reference the business entity use this @id in their provider/publisher fields.

4. **Validate before deploying.** Every schema block must pass the Rich Results Test at https://search.google.com/test/rich-results before going live.

5. **No duplicate types.** Each page has one of each schema type. Two LocalBusiness blocks on the same page creates ambiguity. The global schema (all pages) has LocalBusiness + WebSite + BreadcrumbList. Page-specific schema adds its own type (Service, FAQPage, Article, etc.).

6. **No em dashes in schema.** Schema content follows the same copy rules as all other She Said Sail copy. No em dashes anywhere.

---

## SCHEMA BY PAGE

### All Pages (global-schema.html via Insert Headers and Footers)

**Schema types:** LocalBusiness + Organization (combined @type array), WebSite, BreadcrumbList (homepage only in global block)

**Required fields on LocalBusiness/Organization:**
- @context, @type, @id, name, url, description, telephone, email, address, areaServed, priceRange, openingHoursSpecification, sameAs, logo, image, foundingDate, knowsAbout, hasOfferCatalog

**WebSite schema:**
- @context, @type, @id, name, url, publisher (@id reference), potentialAction (SearchAction)

---

### Homepage (/)

Schema from global block covers this page. No additional page-specific schema needed.

If a homepage-specific schema is added in the future, use:
- @type: WebPage
- breadcrumb: BreadcrumbList with one item (Home)

---

### Experiences Index (/experiences/)

**Schema types:** CollectionPage, ItemList, BreadcrumbList

**ItemList:** Lists all 4 experiences as ListItem objects with position, name, url, description.

**BreadcrumbList:** Home > Experiences

---

### Monaco Social (/experience/monaco-social/)

**Schema types:** Service, BreadcrumbList

**Required Service fields:**
- @type, name, description, url, serviceType, provider (@id reference), offers, audience, areaServed, brand

**Offers required fields:**
- @type: Offer, price, priceCurrency, priceSpecification (minPrice), availability, url

**BreadcrumbList:** Home > Experiences > Monaco Social

---

### Golden Hour Escape (/experience/golden-hour-escape/)

Same Service schema structure as Monaco Social.
**BreadcrumbList:** Home > Experiences > Golden Hour Escape

---

### Rose Day Club (/experience/rose-day-club/)

Same Service schema structure as Monaco Social.
**BreadcrumbList:** Home > Experiences > Rose Day Club
**Note on naming:** Schema @name is "Rose Day Club" (no accent). Display copy may use "Rosé Day Club" where the accent is appropriate. The schema canonical name is without the accent.

---

### Pink Palm Club (/experience/pink-palm-club/)

Same Service schema structure as Monaco Social.
**BreadcrumbList:** Home > Experiences > Pink Palm Club

---

### About (/about/)

**Schema types:** Organization, BreadcrumbList

**Organization fields (supplement to global block):**
- @id (matching global), name, url, description, foundingDate, knowsAbout, hasOfferCatalog, address, sameAs

**BreadcrumbList:** Home > About

---

### FAQ (/faq/)

**Schema types:** FAQPage, BreadcrumbList

**FAQPage:** 19 Question entities with acceptedAnswer. All answers match visible page copy word-for-word.

**BreadcrumbList:** Home > FAQ

---

### Journal Index (/journal/)

**Schema types:** CollectionPage, BreadcrumbList

**CollectionPage:** name, description, url, publisher (@id reference)

**BreadcrumbList:** Home > Journal

---

### Journal Articles (/journal/[slug]/)

**Schema types:** Article, BreadcrumbList

**Article required fields:** headline, datePublished, dateModified, author (Organization), publisher (@id reference), image, url, description

**BreadcrumbList:** Home > Journal > [Article Title]

---

### Request to Book (/request-to-book/)

**Schema types:** WebPage (optional), BreadcrumbList

No Service schema needed on this page. The action of booking is handled by the experience pages.

**BreadcrumbList:** Home > Request to Book

---

### Thank You (/thank-you/)

**No schema.** This page has `noindex, nofollow` robots directive. Do not add structured data to post-conversion pages.

---

### Contact (/contact/)

**Schema types:** ContactPage (optional), BreadcrumbList

**BreadcrumbList:** Home > Contact

---

## ENTITY REGISTRY

These are the canonical values used in all schema and copy. Do not deviate.

### She Said Sail (Organization)

```json
{
  "@type": ["LocalBusiness", "TouristAttraction"],
  "@id": "https://shesaidsail.com/#organization",
  "name": "She Said Sail",
  "url": "https://shesaidsail.com",
  "description": "Private luxury yacht charter company in Miami offering curated on-water experiences for women-led celebrations. Experiences include Monaco Social, Golden Hour Escape, Rose Day Club, and Pink Palm Club. Groups from 4 to 22 guests. Starting from $10,000.",
  "foundingDate": "2022",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Miami",
    "addressRegion": "FL",
    "postalCode": "33132",
    "addressCountry": "US"
  },
  "areaServed": ["Miami", "Fort Lauderdale", "Biscayne Bay"],
  "priceRange": "From $10,000",
  "telephone": "UPDATE_WITH_REAL_PHONE",
  "email": "hello@shesaidsail.com"
}
```

### Monaco Social (Service)

```json
{
  "@type": "Service",
  "name": "Monaco Social",
  "serviceType": "Yacht Charter",
  "description": "Champagne-led yacht experience in Miami for birthdays and elevated social groups. Full crew, curated bar, and Bluetooth sound system. Up to 15 guests.",
  "url": "https://shesaidsail.com/experience/monaco-social/",
  "audience": {
    "@type": "Audience",
    "audienceType": "Birthday celebrations, elevated bachelorette groups, curated social events"
  }
}
```

### Golden Hour Escape (Service)

```json
{
  "@type": "Service",
  "name": "Golden Hour Escape",
  "serviceType": "Yacht Charter",
  "description": "Private sunset yacht charter for intimate groups and milestone moments in Miami. Up to 12 guests.",
  "url": "https://shesaidsail.com/experience/golden-hour-escape/",
  "audience": {
    "@type": "Audience",
    "audienceType": "Intimate celebrations, anniversaries, proposals, small milestone groups"
  }
}
```

### Rose Day Club (Service)

```json
{
  "@type": "Service",
  "name": "Rose Day Club",
  "serviceType": "Yacht Charter",
  "description": "Private afternoon yacht charter for girls trips, birthdays, and social group celebrations in Miami. Up to 15 guests.",
  "url": "https://shesaidsail.com/experience/rose-day-club/",
  "audience": {
    "@type": "Audience",
    "audienceType": "Girls trips, social afternoon groups, birthday celebrations"
  }
}
```

Note: Schema @name is "Rose Day Club" without accent. Display copy may use "Rosé Day Club."

### Pink Palm Club (Service)

```json
{
  "@type": "Service",
  "name": "Pink Palm Club",
  "serviceType": "Yacht Charter",
  "description": "High-energy bachelorette and group celebration yacht charter in Miami. Up to 22 guests, the largest She Said Sail experience.",
  "url": "https://shesaidsail.com/experience/pink-palm-club/",
  "audience": {
    "@type": "Audience",
    "audienceType": "Bachelorette parties, large group celebrations, high-energy social events"
  }
}
```

---

## SCHEMA VALIDATION CHECKLIST

Before deploying any schema block:

| Check | How |
|---|---|
| Valid JSON (no trailing commas, no missing quotes) | Paste into jsonlint.com |
| Passes Google Rich Results Test | https://search.google.com/test/rich-results |
| All @id references resolve to real URLs | Manual check |
| No em dashes in any string value | grep for U+2014 |
| Visible content only (no hidden fields) | Compare schema to page HTML |
| No duplicate @type on same page | Review all schema on that page |
| provider @id matches organization @id | "https://shesaidsail.com/#organization" |

---

## SCHEMA THAT IS NOT YET IMPLEMENTED

These schema types will be relevant as the site grows:

| Schema Type | Trigger Condition | Notes |
|---|---|---|
| AggregateRating | Once 5+ verified Google reviews exist | Add to LocalBusiness and individual Service schemas |
| Review | Once testimonials are verified and attributed | Must include author name, datePublished, reviewRating |
| speakable | After core schema confirmed clean | Google experimental for voice/AI voice assistants |
| VideoObject | If video added to experience or journal pages | Significant AI discoverability increase |
| Event | If specific-date themed sailings are offered | startDate, endDate, location, offers required |
| HowTo | If step-by-step booking guides are published | Good for voice search and AI answer extraction |

---

## SCHEMA THAT WILL NEVER BE ADDED

| Schema Type | Reason |
|---|---|
| AggregateRating with fake data | Schema.org and Google prohibit fabricated reviews |
| Product schema | She Said Sail is a service, not a product |
| JobPosting | Not a hiring site |
| Recipe | Not applicable |
| Schema for /thank-you/ | noindex page, no value |
