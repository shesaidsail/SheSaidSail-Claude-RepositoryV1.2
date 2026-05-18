# Request Page Conversion Strategy
She Said Sail | Request to Book Overhaul v2.0

---

## Initial Audit Scores (Pre-Overhaul)

| Dimension | Score | Notes |
|---|---|---|
| Luxury positioning | 5/10 | Heading said "Request to Book" with no editorial framing |
| Emotional conversion | 4/10 | Flat descriptor text: "Submit your request and our concierge will confirm availability within 24 hours" |
| Trust | 5/10 | No concierge reassurance woven into the form |
| Form UX | 5/10 | Poor logical grouping, fields presented in no coherent emotional order |
| Mobile UX | 4/10 | Input height at 10px padding, no sticky CTA, no thumb-zone awareness |
| Copy | 4/10 | Transactional: "Submit", "Fill out form", generic labels |
| Clarity | 5/10 | No step structure, no guidance for the user |
| CTA hierarchy | 4/10 | "Request to Book" button copy matches page title, zero emotional pull |
| Backend readiness | 5/10 | Hidden fields existed but no UTM capture, no landing page, no brand routing |
| Tracking readiness | 3/10 | No dataLayer events beyond GTM container load |
| Airtable readiness | 5/10 | Fields map loosely to Requests table but lacked metadata fields |
| Make.com readiness | 5/10 | MetForm webhook existed but no M-BRAND-ROUTER or M-UTM-CAPTURE hooks |

---

## Identified Conversion Leaks

- No occasion or experience context captured at the start of the form
- No psychological momentum: user is dropped directly into a raw form
- Weak headline "Request to Book" offers no emotional reward for beginning
- No visible next-step guidance after submission
- "Elevated Add-Ons" field placed before contact information, creating friction
- Budget field absent: leads arriving with no budget context reduce operational efficiency
- No multi-step structure: form felt dense and unguided on mobile
- No section rhythm: all fields ran together without breathing room

---

## Emotional Friction Points Removed

| Original | Overhaul |
|---|---|
| "Submit your request" | "Tell us what you are envisioning." |
| "Request to Book" (CTA) | "Begin Planning" |
| "Special Requests" textarea first | Moved to Step 3, after rapport is built |
| No timing expectation | "Most inquiries receive a response within business hours" added |
| No reassurance | Four concierge trust points added before submit |
| No thank-you experience | Full emotionally elevated thank-you state |

---

## Optimized Field Order

### Step 1: The Experience
- Occasion (card selector)
- Experience Type (card selector)
- Preferred Date
- Guest Count

### Step 2: Contact
- First Name / Last Name
- Email / Phone

### Step 3: Vision
- Budget Range
- What You Are Envisioning (open text)
- Special Requests

### Step 4: Submit
- Concierge reassurance block
- "Begin Planning" CTA

---

## Copy Direction

### Avoided Language
- "Submit inquiry"
- "Fill out form"
- "Booking request"
- Generic form labels without context

### Adopted Language
- "Tell us what you are envisioning."
- "We will curate the best options for your group."
- "Every experience is tailored around the atmosphere you want to create."
- "A concierge reviews every request personally."
- "Yacht options are curated manually based on your group."
- "Everything can still be customized after submission."

---

## Thank You Flow

**Headline:** Your experience is now in motion.

**Body:**
Your request has been received. A concierge is now reviewing the best options for your group. We will be in touch within business hours. Everything can still be adjusted after this point.

**Timing note:** Most inquiries receive a response same day.

**Social encouragement:** Instagram, Facebook, TikTok links to build anticipation while waiting.

---

## Trust Layer Architecture

Four concierge trust points surface immediately before the submit CTA:

1. A concierge reviews every request personally.
2. Yacht options are curated manually based on your group size, date, and vision.
3. Everything can still be customized after submission.
4. Most inquiries receive a response within business hours.

Trust bar at top of page (below hero) repeats three micro-assurances:
- No payment required now
- Concierge reviews every request
- Response within business hours
