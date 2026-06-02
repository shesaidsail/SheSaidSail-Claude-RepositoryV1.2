# WordPress and Elementor Manual Steps

This is the paste ready guide for applying the conversion fixes in Elementor. It works whether the edits are applied to the live site by hand or to the elementor-*.json exports once they are in the repo.

General safety rules for any JSON edit:
- Validate JSON syntax after every change
- Preserve element IDs, widget types, styling, and responsive settings
- Do not remove layout data, forms, or tracking snippets
- Change visible text and content only, not internal field names or tracking values
- Keep a clean git diff so every change is reviewable

No em dashes in any copy. Commas, periods, and colons only.

---

## 1. Remove placeholder testimonials

1. Open the testimonial section or template.
2. Find placeholder copy: lorem ipsum, "Phasellus fringilla commodo tellus", Peter Lawson, Customer, and any stock avatar used as a testimonial photo.
3. Replace with real, permissioned quotes from content/testimonials-needed.md.
4. If no real quote is ready for a slot, set that testimonial to draft or hide it. Do not show placeholder testimonials to paid traffic.
5. Use the recommended format: quote, first name, occasion, city, vessel.

## 2. Remove visible ADD BOAT PHOTO placeholders

1. Search every yacht card, pricing section, and yacht page for "ADD BOAT PHOTO".
2. For each vessel, replace the placeholder text with a real image widget.
3. Upload the hero image for that vessel, set alt text and caption per content/yacht-photo-checklist.md.
4. If a real image is not ready, use a clean branded image placeholder, never the literal words "ADD BOAT PHOTO".
5. Preserve the existing card layout and spacing.

## 3. Upgrade CTA language

1. Search for button text: Inquire, Learn More, Get Started, Submit, Contact Us, Read More, Send.
2. Replace visible button text per content/final-cta-copy-map.md:
   - Hero and primary nav: Check Availability
   - Vessel cards and pricing: Reserve Your Date
   - Undecided or fleet: Find the Right Yacht
   - Help, trust, footer: Talk to a Concierge
   - Premium positioning: Request a Private Recommendation
3. Change only the visible label. Leave form submit field names and tracking values unchanged.

## 4. Add weather and rescheduling reassurance

1. Add a small text or icon box widget near pricing, booking, FAQ, and the reserve action.
2. Paste the approved copy from content/weather-reassurance-block.md.
3. Keep typography consistent with surrounding body copy.

## 5. Add package differentiation copy

1. On the pricing page and any vessel card listing the four experiences, add one line under each name.
2. Paste the matching line from content/package-differentiation-copy.md for Rosé, Sunset Social, Pink Palm, Monaco Social.
3. Keep each to one sentence.

## 6. Add or improve How It Works

1. On the homepage and request to book page, add a section using an icon list or step columns.
2. Use the headline and five steps from content/how-it-works-section.md.
3. Add a Check Availability CTA below the steps.

## 7. Add or improve Why She Said Sail

1. On the homepage, add a trust section near the top.
2. Use the headline and bullets from content/why-she-said-sail-section.md as an icon list.
3. Optional CTA below: Find the Right Yacht or Talk to a Concierge.

## 8. Add founder and team section

1. Add an image widget with a clean placeholder for the founder photo.
2. Use the headline and copy from content/founder-team-section.md.
3. The founder will add the real photo later. Set alt text once added.

## 9. Add FAQ block

1. Add an accordion or toggle widget on the homepage, pricing page, and request to book page.
2. Use the questions and answers from content/faq-conversion-block.md.
3. Place near pricing and the reserve action.

---

## Applying changes to the elementor-*.json exports

When the elementor-*.json files are committed to the repo:

1. Updated import ready copies will be written to the elementor-updated/ folder, originals left intact for a clean diff.
2. For each file: parse, locate the target widgets by their text content, edit text and content fields only, then re validate JSON.
3. Re import the updated JSON in Elementor using Import Template or page settings Import.
4. Spot check on desktop and mobile before publishing.

## Import procedure in WordPress

1. In Elementor, go to Templates, then Import, or use the page level import.
2. Upload the updated JSON file.
3. Open the page in the Elementor editor and verify layout, images, and CTAs.
4. Check mobile responsiveness.
5. Publish.
