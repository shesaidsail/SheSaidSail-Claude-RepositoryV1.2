# Review Architecture

Goal: turn reviews into a trust engine that lifts conversion, SEO, and AI-search, without ever publishing an invented quote. Pairs with content/testimonials-needed.md (collection) and the cleared testimonial slots in elementor-updated/testimonial.json.

## Three places reviews appear

1. Homepage trust strip: 3 short, real quotes near the top, under the Why She Said Sail section. First-name, occasion, vessel.
2. Yacht detail pages: 1 to 2 quotes tied to that vessel or occasion, just above the Reserve Your Date CTA.
3. Dedicated reviews block on the About or Experiences page: the fuller set, 5 to 8 quotes, grouped by occasion (bachelorette, birthday, girls trip, private event).

## Display format (per review)
- Quote: one or two honest lines.
- Attribution: First name, occasion, city, vessel. Example: "Sarah, Bachelorette, Miami, aboard Carpe Diem."
- Optional photo: real client or styled day photo, with permission.

## Collection system (operational)
1. Trigger: post-charter, day +1, the concierge sends the short request message in testimonials-needed.md.
2. Capture: store the quote, first name, occasion, city, vessel, and written permission in Airtable (a Reviews table, not built here, mirrors Google Reviews already in the base).
3. Approve: founder approves before anything goes live.
4. Publish: move an approved quote into the Elementor testimonial widget slot; flip the slot from draft to visible.

## SEO and AI-search hooks (when real reviews exist)
- Add Review and AggregateRating schema (via the SEO plugin) on yacht pages once real ratings exist. Do not add schema for invented ratings.
- Encourage Google reviews in the same post-charter message; Google review volume is the single biggest local-SEO and AI-citation signal for a Miami service business.
- Keep review text as crawlable HTML, not images.

## Launch rule
Three to five real, permissioned quotes are enough to launch the trust strip. Until a slot has a real quote, it stays hidden or in draft. Never show placeholder testimonials to paid traffic.
