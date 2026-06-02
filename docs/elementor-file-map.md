# Elementor File Map and Inventory

Source of truth for all Elementor exports lives in elementor-source/. Originals are copied in unmodified. Updated import ready copies are written to elementor-updated/.

## Running inventory

Files received: 17 unique (18 uploads, the two 5844 FAQs files were identical duplicates)
Batches received: final tranche signaled
Validation: all 17 valid JSON (version 0.4)
Status: FINAL BATCH COMPLETE. Implementation applied.

## File map

| Original upload | Export id | New name | Purpose | Template type | Import location |
|---|---|---|---|---|---|
| elementor586820260602.json | 5868 | home.json | Homepage | page | Home |
| elementor589420260602.json | 5894 | yachts.json | Yacht listing page | page | Yachts |
| elementor588820260602.json | 5888 | yacht-detail.json | Single yacht detail | page | Yacht Detail template |
| elementor587120260602.json | 5871 | pricing.json | Pricing page | page | Pricing |
| elementor587420260602.json | 5874 | services.json | Services page | page | Services |
| elementor584120260602.json | 5841 | destinations.json | Destinations page | page | Destinations |
| elementor588020260602.json | 5880 | team.json | Team page | page | Team / About |
| elementor588420260602.json | 5884 | testimonial.json | Testimonials page | page | Testimonials |
| elementor584420260602.json | 5844 | faqs.json | FAQ page | page | FAQs |
| elementor583520260602.json | 5835 | blog.json | Blog listing | page | Blog |
| elementor587720260602.json | 5877 | single-post.json | Blog single post | section | Single Post template |
| elementor586520260602.json | 5865 | header.json | Site header | section | Header |
| elementor584720260602.json | 5847 | footer.json | Site footer | section | Footer |
| elementor585920260602.json | 5859 | form-search.json | Charter search form | section | Form Search |
| elementor585620260602.json | 5856 | form-rent.json | Rent / reserve form | section | Form Rent |
| elementor585020260602.json | 5850 | form-contact.json | Contact form | section | Form Contact |
| elementor585320260602.json | 5853 | form-newsletter.json | Newsletter form | section | Form Newsletter |

## Classification of conversion elements

- Testimonials: testimonial.json (Peter Lawson placeholder + lorem), home.json testimonial block, "Trusted by 1000+ clients" trust heading
- Yacht cards: yachts.json, home.json, destinations.json (demo vessel names such as "Welson Lux Yacht")
- Pricing: pricing.json, yacht-detail.json (demo "$950/day", "Rent This Yacht")
- CTA buttons: home, yachts, services, pricing, destinations, header, faqs (Get Started, Learn More, Contact Us, Book Now, Let's Talk!, Read More, Get In Touch, Book a yacht, Booking Form, Support Center)
- FAQ: faqs.json (page) and references on home and destinations
- Team / founder: team.json
- Header and footer: header.json, footer.json
- Forms: form-search, form-rent, form-contact, form-newsletter (preserve all form fields and ids)
- Trust sections: testimonial.json trust heading, plus Why She Said Sail added as importable section

## Placeholder content confirmed and handled

| File | lorem ipsum | Other placeholders |
|---|---|---|
| faqs.json | 40 | demo FAQ answers |
| home.json | 33 | Learn More, Get Started, Read More CTAs |
| services.json | 25 | Learn More, Get Started CTAs |
| pricing.json | 18 | Get Started CTA, demo pricing |
| destinations.json | 17 | Read More CTAs, demo copy |
| team.json | 15 | demo team bios |
| yachts.json | 13 | Get Started, Contact Us CTAs, demo vessels |
| testimonial.json | 10 | Peter Lawson placeholder testimonial |
| yacht-detail.json | 2 | "Rent This Yacht", "$950/day", demo vessel |
| single-post.json | 2 | demo blog content |
| blog.json | 0 | Read More CTA |

## Notes

- No "ADD BOAT PHOTO" text exists in any Elementor export. That placeholder appeared only in the pricing PDF mockup, so there is nothing to remove in the JSON for that item.
- No "Inquire" CTA exists in the Elementor exports. The demo theme uses Get Started, Learn More, Contact Us, Book Now, and similar. Those are the CTAs upgraded.
- The exports are still on theme demo content. Real She Said Sail pricing, fleet, and copy are documented in the content/ files and the Drive source PDFs, and should be layered in alongside these fixes.
