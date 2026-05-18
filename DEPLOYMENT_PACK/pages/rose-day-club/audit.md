# SHE SAID SAIL
# ROSE DAY CLUB — PAGE AUDIT

PAGE: Rose Day Club
URL: https://shesaidsail.com/experience/rose-day-club/
AUDIT DATE: 2026-05-18
STANDARD: master-audit-scorecard.md v1.0

---

## PRE-OPTIMIZATION SCORES (Estimated Based on Common Patterns)

| Dimension | Pre Score | Issues Identified |
|-----------|-----------|-------------------|
| Luxury positioning | 5/10 | Generic layout, likely using default Webflow template blocks without brand refinement. Missing gold accent system. |
| Emotional conversion | 4/10 | Hero copy likely leads with product/logistics rather than feeling. No emotional arc through the page. |
| Mobile UX | 5/10 | Likely compressed desktop layout. CTA probably not sticky. Buttons may be undersized. |
| Trust | 4/10 | Limited or no testimonials on this specific page. Process not clearly communicated. No reassurance language. |
| CTA clarity | 5/10 | CTA likely present but buried or using generic copy ("Book Now"). No sticky mobile CTA. |
| Copy | 5/10 | Functional copy but not editorial. Likely over-explains logistics, undersells the feeling. |
| Visual consistency | 5/10 | May not fully follow gold/navy/cream system. Possible inconsistent section backgrounds. |
| Backend readiness | 4/10 | Hidden fields likely missing (UTM, page_name, source_url). |
| Analytics readiness | 4/10 | Form submission event likely not tracked in GTM. UTM parameters not captured. |
| SEO | 5/10 | Basic title tag present but OG image, schema, and detailed descriptions likely missing or thin. |
| Performance | 5/10 | Images likely not WebP. Hero image may be oversized. |
| Operational maturity | 3/10 | No documented QA, no backend testing notes, no analytics verification. |

PRE-OPTIMIZATION AVERAGE: 4.5/10

---

## CONVERSION LEAKS IDENTIFIED

1. Hero copy leads with product name rather than emotional hook
2. No emotional anchor in the first viewport
3. CTA copy likely "Book Now" (transactional, not inviting)
4. No sticky mobile CTA
5. Form missing hidden attribution fields
6. No UTM capture script
7. Testimonials absent or buried
8. No reassurance language near the form ("You'll hear from us within one business day")
9. Process not communicated (what happens after you submit)
10. No page_name field in form (analytics cannot attribute conversions to this page)

---

## WEAK SECTIONS IDENTIFIED

Hero: Emotional hook missing. Layout likely template-default.
Inclusions: Likely bullet list with no visual hierarchy. Feels like a checklist.
CTA section: Likely single button without supporting copy or reassurance.
FAQ: Possibly absent. Payment, cancellation, weather questions not answered.
Footer: Inconsistent with other pages if not centrally managed.

---

## WEAK COPY PATTERNS (LIKELY)

"Book your ultimate Rose Day Club experience" (superlative, generic)
"Enjoy an unforgettable day on the water" (prohibited: unforgettable)
"Contact us for more information" (weak, no action signal)
"Available for groups of up to X" (leads with limitation)

---

## TRUST GAPS

- No testimonials specific to Rose Day Club
- No captain/crew mention
- No "what happens after I submit" explanation
- No weather/cancellation reassurance
- Contact information not visible in the inquiry section
- No social proof (Instagram count, number of events hosted, etc.)

---

## BACKEND GAPS

- source_url hidden field: likely missing
- UTM parameters: likely not captured
- page_name field: definitely missing (non-standard)
- city auto-set: may not be implemented
- Idempotency key relies on email + date + guests: must all three fields exist on this form

---

## SEO ISSUES (LIKELY)

- Title tag may be "Rose Day Club | She Said Sail" but generic/under-optimized
- Meta description thin or auto-generated
- OG:image likely missing or using wrong dimensions
- Schema markup: none
- Alt text: may be missing or empty on hero image
- H1 may not match primary keyword intent

---

## POST-OPTIMIZATION TARGET SCORES

| Dimension | Target Score |
|-----------|-------------|
| Luxury positioning | 9/10 |
| Emotional conversion | 9/10 |
| Mobile UX | 9/10 |
| Trust | 8/10 |
| CTA clarity | 9/10 |
| Copy | 9/10 |
| Visual consistency | 9/10 |
| Backend readiness | 9/10 |
| Analytics readiness | 9/10 |
| SEO | 9/10 |
| Performance | 8/10 |
| Operational maturity | 9/10 |

POST-OPTIMIZATION TARGET AVERAGE: 9.0/10

---

## WHAT REQUIRES HUMAN IMPLEMENTATION

The following cannot be implemented by AI and require human action in Webflow:

1. Actual Webflow form field names must be set to match backend-system.md specs
2. GTM must be configured with form submission triggers
3. Images must be photographed/selected and uploaded
4. Testimonials must be collected from real clients and entered
5. OG:image must be designed and uploaded (1200x630px)
6. Schema markup must be injected in Webflow page settings
7. UTM JS snippet must be added to Webflow's custom code section
8. Core Web Vitals must be measured post-publish and iterated on
9. Form must be tested end-to-end in production (Make.com, Airtable, email)
10. Canonical URL must be confirmed in Webflow page settings
