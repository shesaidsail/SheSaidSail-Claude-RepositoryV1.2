# Website Completion Audit and Readiness

Scope: public-facing conversion only. No Airtable, pricing, Make, or production touched. Updated, import-ready Elementor files live in elementor-updated/; copy decks live in content/. This audit shows, per page, the current weakness, the recommended change, and where the exact copy lives.

## Method

Source: WordPress export, the Elementor exports (elementor-source/), and the final operating model. Conversion fixes were applied programmatically (scripts/apply_conversion_fixes.py) and new sections generated (scripts/generate_sections.py), so every change is reproducible and every original is preserved.

## Page-by-page

### Homepage (home.json)
- Weakness: demo theme residue (Odysea brand, lorem ipsum, "Trusted by 1000+ clients"), weak CTAs (Get Started, Book Now), no clear trust or process section, placeholder testimonials.
- Recommended: clean brand and claims, confident CTAs, add Why She Said Sail and How It Works high on the page, add a real-review trust strip.
- Exact copy: applied in elementor-updated/home.json. New sections: section-why-she-said-sail.json, section-how-it-works.json. Hero CTA now Check Availability. Claim replaced with "Curated celebrations across Miami and Fort Lauderdale."

### Yachts / fleet (yachts.json)
- Weakness: undecided-browser language (Learn More, Read More), demo vessels and images.
- Recommended: guide selection with Find the Right Yacht; feature the Volume fleet first per the operating model.
- Exact copy: CTAs updated in elementor-updated/yachts.json. Real fleet and photos pending (content/yacht-photo-checklist.md).

### Yacht detail (yacht-detail.json)
- Weakness: Inquire and Rent This Yacht language; no reassurance near the booking action.
- Recommended: Reserve This Yacht and Reserve Your Date; add a weather and rescheduling reassurance line near the CTA.
- Exact copy: CTAs updated in elementor-updated/yacht-detail.json; reassurance in content/weather-reassurance-block.md; CTA logic in content/final-cta-copy-map.md.

### Experiences / services (services.json)
- Weakness: generic service copy, demo content.
- Recommended: lead with the four experiences and their Best For lines, push add-ons as upsells.
- Exact copy: elementor-updated/services.json updated; differentiation in content/package-differentiation-copy.md.

### Pricing (pricing.json)
- Weakness: Inquire on every card signals price is soft.
- Recommended: Reserve Your Date next to published prices. (Actual numbers are frozen per instruction; only button copy changed.)
- Exact copy: elementor-updated/pricing.json.

### About page
- Weakness: thin, no human, no story; ugly /about-4/ slug.
- Recommended: brand story plus the team. Use the founder paragraph and the Why section.
- Exact copy: section-founder.json (short) and section-team.json (full), content/team-section.md.

### Team page (team.json)
- Weakness: demo team members and bios.
- Recommended: real, human team: Founder, Emma, Tania, plus office and behind-the-scenes photos.
- Exact copy: elementor-updated/section-team.json (new) and content/team-section.md. Names are real; roles, bios, and photos are placeholders for founder approval.

### FAQ (faqs.json)
- Weakness: six generic demo questions and answers.
- Recommended: real questions that remove booking anxiety (weather, alcohol, choosing a yacht, how reserving works, locations).
- Exact copy: elementor-updated/faqs.json updated, plus the full 10-question section-faq-conversion.json.

### Request to Book
- Weakness: cold form language (Submit, Send); no process framing.
- Recommended: Reserve Your Date submit, How It Works above the form, weather reassurance near it.
- Exact copy: form CTA changes in elementor-updated/form-*.json; section-how-it-works.json.

## Cross-cutting

### Reviews
- Weakness: placeholder testimonials (Peter Lawson, lorem, stock avatars) are live, the single biggest trust risk for paid traffic.
- Recommended: cleared to [REAL TESTIMONIAL NEEDED] slots; collect 3 to 5 real quotes before launch.
- Exact copy and system: content/testimonials-needed.md and content/review-architecture.md; cleared slots in elementor-updated/testimonial.json.

### Mobile conversion
- Weakness: long demo sections, CTAs not always thumb-reachable.
- Recommended: keep the new sections short and stacked (they are built as single-column containers that stack cleanly), primary CTA repeated after Why and after How It Works, generous spacing.
- Status: the generated sections are mobile-first containers; verify in the Elementor editor after import.

### SEO copy
- Weakness: no SEO plugin, no meta, ugly slugs, generic image names (see docs/live-site-reconstruction-and-audit.md).
- Recommended: install Rank Math, set ACF-driven titles and meta, fix /about-4/ and the front page, unique H1s on the landing pages. Copy here supports it (clear headings, real questions).

### AI-search discoverability
- Weakness: no structured data, prices and facts sometimes only in JS.
- Recommended: FAQPage schema on the new FAQ section (real Q and A), LocalBusiness and Organization schema, yacht facts as text. The FAQ copy is written as clean Q and A specifically so it is AI-extractable.

## Updated Elementor files (deliverable)

elementor-updated/ contains 17 conversion-fixed pages and forms plus 5 importable section templates: section-why-she-said-sail, section-how-it-works, section-faq-conversion, section-founder, and section-team (new this round). All validated as parseable Elementor 0.4 JSON. Originals preserved in elementor-source/.

## Missing assets required from founder

1. Founder name and photo.
2. Emma role, bio approval, and photo.
3. Tania role, bio approval, and photo.
4. Office and behind-the-scenes or styling photos.
5. Three to five real, permissioned client testimonials.
6. Real vessel photography for the fleet (replace askproject.net demo images).
7. Real fleet and the approved pricing layered onto the pages (frozen here per instruction).
8. SEO plugin install and meta, and the slug and front-page fixes.

## Website readiness score

| Component | Status | Score |
|---|---|---|
| Copy and messaging | Done, on brand | 9/10 |
| Conversion structure (Why, How, FAQ, CTAs, reassurance) | Done | 9/10 |
| Trust architecture (team, reviews framework) | Built, awaiting real assets | 6/10 |
| Real testimonials | Slots ready, none collected | 2/10 |
| Photography (team, office, fleet) | Placeholders only | 2/10 |
| Real fleet and pricing on pages | Frozen, not yet layered | 4/10 |
| SEO and AI-search setup | Specified, not installed | 3/10 |
| Mobile | Built mobile-first, needs editor verification | 7/10 |

Overall copy and structure: about 90 percent complete. Launch-ready including real assets: about 60 percent. The remaining 40 percent is founder-supplied assets (photos, testimonials, fleet, SEO install), not copy or build work.

## Exact next step

Founder supplies the eight assets above. Import the 5 section templates and the updated pages from elementor-updated/ into Elementor (steps in elementor-updated/README.md and docs/wordpress-elementor-manual-steps.md), place the sections, keep testimonial and any photo-dependent sections in draft until real assets are in, then verify mobile and publish. No pricing or production change is included here.
