# elementor-updated

Import ready Elementor files with the conversion psychology fixes applied. Originals are preserved unchanged in elementor-source/. Every file here is valid Elementor JSON (version 0.4) with all element IDs, widget types, styling, and responsive settings preserved. Only text content was changed.

Regenerate any time with:

```
python3 scripts/apply_conversion_fixes.py   # updates the 17 page/section copies
python3 scripts/generate_sections.py        # builds the 4 new section templates
```

## Updated pages and sections (17)

home, yachts, yacht-detail, pricing, services, destinations, team, testimonial, faqs, blog, single-post, header, footer, form-search, form-rent, form-contact, form-newsletter.

Changes applied across these files:
- Removed all lorem ipsum (replaced with on brand copy)
- Removed the Peter Lawson placeholder testimonial and cleared the demo testimonial data (Jhon Malthans, "Customer", lorem reviews) to clearly marked [REAL TESTIMONIAL NEEDED] slots
- Replaced the demo theme brand name "Odysea" with She Said Sail in all visible text, and the demo email odysea@mail.com with hello@shesaidsail.com
- Replaced the unverifiable "Trusted by 1000+ clients" claim with "Curated celebrations across Miami and Fort Lauderdale"
- Upgraded weak CTAs: Get Started and Book Now to Check Availability, Book a yacht and Booking Form to Reserve Your Date, Learn More to Find the Right Yacht, Contact Us / Let's Talk! / Get In Touch to Talk to a Concierge
- Replaced "Rent This Yacht" with "Reserve This Yacht" (brand voice avoids rental language)
- Replaced the 6 generic demo FAQ questions and answers with real She Said Sail questions and calm, accurate answers

Forms (form-search, form-rent, form-contact, form-newsletter) and all metform widgets, field names, and tracking were left intact.

## New importable section templates (4)

- section-how-it-works.json: How She Said Sail Works (5 steps)
- section-why-she-said-sail.json: Why Groups Choose She Said Sail (6 trust bullets)
- section-faq-conversion.json: Questions, Answered (full 10 question accordion)
- section-founder.json: Meet the Team Behind She Said Sail (with founder photo placeholder)

These are valid Elementor section exports. Import each, then place it on the relevant page (How It Works and Why on the homepage and request to book page, FAQ near pricing, Founder on the Team or About page).

## How to import

1. In WordPress, open Elementor Templates, then Import Templates, and upload the file.
2. For the 17 updated pages, you can also use the page level Import in the Elementor editor.
3. Open the page in the editor and verify layout, images, and CTAs.
4. Check mobile responsiveness.
5. Publish.

## Still required (not solvable in JSON)

- Real vessel photos. The demo image URLs still point to the theme author's server (askproject.net/odysea/...). See content/yacht-photo-checklist.md.
- Real testimonials to fill the [REAL TESTIMONIAL NEEDED] slots. See content/testimonials-needed.md. Keep these sections hidden or in draft until real, permissioned quotes are added.
- Founder photo for section-founder.json.
- Real fleet and pricing. These exports are still on theme demo vessels and demo prices. The real fleet and pricing are documented in content/ and the Drive source PDFs and should be layered in.
