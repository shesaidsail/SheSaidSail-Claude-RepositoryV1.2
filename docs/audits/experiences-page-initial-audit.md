# Experiences Page Initial Audit

**Date:** 2026-05-18
**Auditor:** Claude Code (AI)
**Page:** shesaidsail.com/experiences/
**Branch:** claude/fix-experiences-page-EwvlD

---

## Scores Before Overhaul

| Dimension | Score | Notes |
|---|---|---|
| Luxury positioning | 4/10 | Hero copy is functional but not emotionally elevated |
| Emotional conversion | 3/10 | Cards read as package listings, not atmosphere invitations |
| Clarity | 6/10 | Structure is readable but undifferentiated |
| Atmosphere differentiation | 3/10 | All four experiences feel visually and verbally similar |
| Mobile UX | 5/10 | Cards collapse to 1-column but spacing and typography scaling need work |
| Typography | 5/10 | Correct fonts loaded but hierarchy lacks contrast and weight variation |
| Imagery | 4/10 | Images present but no emotional direction or focal crop guidance |
| CTA hierarchy | 4/10 | Single "Explore Experience" per card, no page-level primary CTA above fold |
| Trust | 2/10 | No social proof, no testimonials, no credibility signals on the page |
| Backend readiness | 2/10 | No data attributes, no hidden fields tied to experience selection |
| Analytics readiness | 2/10 | No GTM events on card clicks or CTA interactions |
| SEO readiness | 3/10 | No Open Graph, no Twitter meta, no structured data, alt tags absent |

**Overall pre-overhaul score: 3.6 / 10**

---

## Identified Weaknesses

### Hero Section

- H1 copy ("A private yachting experience, designed from start to finish.") is generic
- Subheadline does not differentiate occasions or group types
- No emotional hook or aspirational framing
- No visual hierarchy separating hero positioning from card section
- Overlay styling suppresses warmth and light

### Experience Card System

- All four cards use identical visual treatment
- Descriptors are 4-5 word mood phrases with no contextual grounding
  - "Effortless champagne-led Riviera energy right crowd always." -- grammatically incomplete
  - "Slow coastal afternoons that linger and unfold." -- better, but isolated
  - "Social sun-soaked ease from water to table." -- generic
  - "Bold electric Miami energy all day always." -- repetitive structure
- No occasion labels (birthday, bachelorette, girls trip)
- No energy-level signal
- No hosting style description
- No atmosphere differentiation beyond the name
- Card layout is identical across featured and grid sections with no visual hierarchy between the featured Monaco Social and the 3-column grid
- Button copy "Explore Experience" is passive and identical across all cards

### CTA Flow

- No page-level primary CTA above the fold
- Bottom CTA ("Get Recommendations") is the only conversion anchor
- No Request to Book button visible until the very bottom
- Chat-opening CTA for Tidio is the only soft conversion, which has no fallback
- Competing button styles between the "Explore Experience" cards and the bottom CTA

### Social Proof

- No social proof on the page
- No testimonials
- No trust signals
- No photography credit or behind-the-scenes credibility

### Mobile UX

- Cards stack to 1-column correctly
- Typography does not scale down enough on small screens (50px H1 on mobile)
- Padding inconsistent between section containers on mobile
- CTA buttons extend full-width but visual feedback on tap is weak
- Featured card image is very tall on mobile with no focal crop

### SEO and Metadata

- No Open Graph tags
- No Twitter/X meta tags
- Alt attributes are empty on all experience images
- No schema.org structured data
- Page title includes "She Said Sail" suffix but no experience keywords

### Backend and Tracking

- No data-track-* attributes on cards or CTAs
- No dataLayer pushes on any interactions
- No UTM capture on page load
- No hidden form field initialization for experience attribution
- No Airtable field mapping defined

---

## Gap Summary

The page functions as a navigational menu, not a conversion surface. Visitors can find experience names and click through, but there is no emotional pull, no social proof, no atmosphere differentiation, and no tracking of intent signals. Every weakness compounds the others: weak copy plus weak imagery plus no social proof plus no CTA hierarchy equals a page that generates passive browsing rather than active booking intent.
