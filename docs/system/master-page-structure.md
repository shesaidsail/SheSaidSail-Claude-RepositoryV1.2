# SHE SAID SAIL
# MASTER PAGE STRUCTURE

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## STANDARD EXPERIENCE PAGE STRUCTURE

Every experience page follows this section order. Sections may be expanded or condensed based on complexity, but order must not change.

| Order | Section | Purpose |
|-------|---------|---------|
| 1 | Navigation | Global nav — consistent across all pages |
| 2 | Hero | First impression. Emotional entry point. |
| 3 | Experience Introduction | What this is. Who it is for. |
| 4 | Experience Details | What happens. What is included. |
| 5 | Logistics | Departure, duration, group size, pricing |
| 6 | Add-Ons (if applicable) | Optional enhancements |
| 7 | Social Proof | Reviews or testimonials |
| 8 | Booking CTA Section | Conversion action |
| 9 | Inquiry Form | Lead capture |
| 10 | Reassurance Strip | Reduce post-form anxiety |
| 11 | Footer | Global footer |

---

## SECTION SPECIFICATIONS

### Hero
- Full-bleed image or video background
- Overlay gradient: navy 55% opacity
- Gold eyebrow label (experience name or occasion type)
- H1 headline: scene-based
- One-line subhead
- Single primary CTA (anchors to form)
- No secondary CTA in hero

### Experience Introduction
- Background: cream (#f4f1ec)
- Max width 760px centered
- H2 headline + 2-3 paragraphs
- No images in this section
- Breathing room: 80px top and bottom padding

### Experience Details
- Background: white
- Two-column layout (desktop): left image, right copy
- Or: image full-width above, copy below (mobile default)
- What's included as clean bullet list
- No pricing in this section

### Logistics
- Background: navy (#0a2342)
- White and gold text
- 3-4 column stat grid: Duration, Guests, Departure, Price
- Clean data display, minimal prose

### Social Proof
- Background: cream
- Max 3 quotes
- Name + occasion context
- No star ratings (understated approach)

### Booking CTA Section
- Background: navy or hero-image with overlay
- Centered
- Strong headline
- Single CTA button (primary gold)
- Anchors to form below or opens form modal

### Inquiry Form
- Background: white
- Card container with border
- All fields visible (no accordion or multi-step unless form is complex)
- Hidden fields: utm_source, utm_medium, utm_campaign, utm_content, page_url, experience_name
- Submit CTA: "Request this experience" or "Check availability"

### Reassurance Strip
- Below form
- Icons + short statements: response time, no payment to inquire, concierge contact
- Light background

### Footer
- Full global footer (consistent across all pages)

---

## HEADING HIERARCHY RULES

- One H1 per page (hero)
- H2 for major section headings
- H3 for sub-sections or card titles
- Never skip heading levels
- Eyebrow labels are span elements, not headings

---

## URL AND SLUG CONVENTIONS

Pattern: /experience/[experience-name]/
Example: /experience/pink-palm-club/

- Lowercase with hyphens
- No trailing query strings in canonical URL
- UTM parameters added at campaign level, not baked into page URL

---

## MOBILE STRUCTURE ADAPTATIONS

- All two-column layouts collapse to single column
- Hero height: 75vh minimum
- Stat grids: 2x2 on tablet, stack vertically on mobile if needed
- CTA buttons: full width on mobile
- Form: all fields full width, no grid layout on mobile
- Section padding: 56px top/bottom (versus 80px desktop)
