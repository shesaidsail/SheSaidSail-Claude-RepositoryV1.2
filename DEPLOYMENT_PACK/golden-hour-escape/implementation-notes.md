# GOLDEN HOUR ESCAPE — IMPLEMENTATION NOTES
Version: 1.0 | Date: May 2026

---

## WHAT THIS DEPLOYMENT PACK CONTAINS

| File | Description |
|------|-------------|
| `audit.md` | Pre/post audit scores, identified gaps, improvement rationale |
| `metadata.html` | Complete head metadata: title, meta desc, OG, Twitter, schema |
| `page-copy.md` | Full optimized copy for every page section |
| `styles.css` | Complete page CSS with design system tokens, responsive breakpoints |
| `analytics.js` | GTM dataLayer events, UTM capture, hidden field population |
| `analytics-gtm-config.md` | GTM tags/triggers/variables configuration guide |
| `html-sections.html` | Complete semantic HTML snippets for all page sections |
| `backend-config.md` | Webhook flow, Airtable field mapping, Make configuration |
| `qa-checklist.md` | 93-item QA checklist with sign-off gates |
| `image-direction.md` | Art direction and technical specs for all page images |
| `implementation-notes.md` | This file -- implementation order and human tasks |

---

## IMPLEMENTATION ORDER (RECOMMENDED)

### Phase 1: Foundation (Developer + Will)
1. Open Webflow Designer for Golden Hour Escape page
2. Add metadata from `metadata.html` to page head (Webflow SEO settings)
3. Add custom CSS from `styles.css` to Webflow page custom CSS
4. Confirm GTM container tag is in global site head code

### Phase 2: Content (Designer + Will)
5. Update hero image per `image-direction.md`
6. Replace all copy with optimized copy from `page-copy.md`
7. Apply CSS class names from `styles.css` to Webflow elements
8. Add all section HTML using `html-sections.html` as reference
9. Configure add-ons section with current approved add-ons and prices

### Phase 3: Backend (Developer)
10. Add all hidden form fields to Webflow form
11. Set form action to Make SSS-LEAD-INTAKE webhook URL
12. Add `analytics.js` to page footer custom code
13. Verify experience field = "Golden Hour Escape" (static hidden value)

### Phase 4: Analytics (Developer)
14. Create GTM variables per `analytics-gtm-config.md`
15. Create GTM triggers per `analytics-gtm-config.md`
16. Create GTM tags per `analytics-gtm-config.md`
17. Publish GTM container

### Phase 5: QA (Tester + Will)
18. Complete all 93 QA checklist items in `qa-checklist.md`
19. Run PageSpeed Insights on mobile
20. Submit test form, verify full pipeline
21. Will signs off

### Phase 6: Launch
22. Publish Webflow page
23. Run post-launch smoke test
24. Mark page as PRODUCTION READY in Airtable Website/Landing Page table (tblVq6XV6AyOxfXAU)

---

## WHAT REQUIRES HUMAN DECISIONS BEFORE IMPLEMENTATION

### 1. Add-On Pricing
The add-ons section uses card descriptions only. Prices are not shown in the copy.

Decision required: Should prices be shown on the page, or handled in the inquiry/proposal?
Recommendation: Keep prices off the page for concierge positioning. Confirm or override.

### 2. Real Testimonials
The 3 testimonials in `page-copy.md` are brand-voice examples, not real quotes.

Action required: Replace all 3 testimonials with real verified guest reviews.
Source: Google Reviews table (tblE2tMb5A1IqwOzW) or Google Business Profile reviews.
Ensure you have permission to use any real names.

### 3. OG Image
The metadata references: `https://shesaidsail.com/wp-content/uploads/golden-hour-escape-og.jpg`

Action required: Create or upload a 1200x630px hero image to use for social sharing.
This should be the strongest single image from the golden hour photography library.
Update the OG image URL in `metadata.html` to match the actual Webflow asset URL.

### 4. Hero Image URL
`html-sections.html` uses placeholder `[REPLACE: golden-hour-hero-image.jpg]`.

Action required: Upload hero image to Webflow, copy asset URL, replace placeholder.

### 5. Boarding Location Field
The form in `html-sections.html` does not include a boarding location field.

Decision required: Should the form include a boarding location selector? If so, add it between City and Add-Ons. Options: "Las Olas Marina (Fort Lauderdale) / Bayside Marketplace (Miami) / Other"

### 6. Starting Price
The copy does not mention a starting price.

Decision required: Should the page show a starting price? If so, update the overview strip or add a pricing section between includes and add-ons.

### 7. Availability / Seasonality Notes
No seasonal language is present in the copy.

Decision required: Are there blackout dates or seasonal availability notes that should appear on the page?

---

## WEBFLOW-SPECIFIC NOTES

- All `.ghe-` CSS classes are namespaced to avoid conflicts with Webflow's default classes
- Apply classes via the Style panel's Custom HTML embed or custom attribute fields
- Or rebuild sections in Webflow Designer using the copy and structure from `html-sections.html` as reference
- The sticky CTA bar (`.ghe-sticky-cta`) uses `position: fixed` -- test that it doesn't conflict with Webflow's navbar z-index

---

## AIRTABLE RECORD TO UPDATE POST-LAUNCH

After launch, update this record in Airtable:
- Table: Website/Landing Page (tblVq6XV6AyOxfXAU)
- Record: Golden Hour Escape
- Fields to update: URL confirmed, last reviewed date, QA status

---

## NOTES FOR FUTURE OPTIMIZATION

Items not included in V1 that could further improve the page:

1. **Availability Calendar Widget** -- A visual "popular dates book quickly" signal (without fake scarcity) could reduce friction further.

2. **Video Background (Hero)** -- A 10-15 second looping silent video clip of the golden hour on the water could significantly increase time on page and desire. Only implement if a high-quality clip exists. Mobile should fall back to still image.

3. **FAQ Section** -- A 4-6 item FAQ about the experience (What should I wear? Can we bring our own champagne? What if it rains?) reduces pre-inquiry friction and can improve SEO via FAQ schema.

4. **Location + Departure Detail** -- A small section with a map or departure location description (marina name, what to expect on arrival) would increase reassurance.

5. **Photo Gallery** -- A 6-9 image masonry gallery of actual golden hour charter photos would dramatically increase conversion. The visual proof of the experience is the strongest selling tool.
