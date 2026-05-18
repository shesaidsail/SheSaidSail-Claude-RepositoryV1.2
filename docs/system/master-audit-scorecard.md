# SHE SAID SAIL
# MASTER AUDIT SCORECARD

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## SCORING SYSTEM

Each dimension is scored out of 10.
A page must score 8 or above in each dimension to be considered production-ready.
A page scores 10 in a dimension only when nothing obvious remains that would materially improve that dimension.

---

## SCORING DIMENSIONS

### 1. Luxury Positioning (0-10)
Does the page feel premium, editorial, and emotionally elevated?

| Score | Criteria |
|-------|----------|
| 9-10 | Instantly feels like a premium hospitality brand. Visual and copy restraint. No amateur signals. |
| 7-8 | Generally premium feel, minor inconsistencies. |
| 5-6 | Mixed signals. Some premium elements, some discount or generic elements. |
| 3-4 | Feels like a standard charter website, not a brand. |
| 0-2 | No premium positioning. Generic or off-brand. |

### 2. Emotional Conversion (0-10)
Does the page make the guest feel something that drives them to inquire?

| Score | Criteria |
|-------|----------|
| 9-10 | Emotional arc is clear. Guest feels recognition, desire, and trust before reaching the form. |
| 7-8 | Emotional journey partially complete. Missing a key moment of connection. |
| 5-6 | Informational but not emotional. Guest understands the product but does not feel it. |
| 3-4 | Copy is transactional. No emotional resonance. |
| 0-2 | Page communicates features only. No feeling. |

### 3. Mobile UX (0-10)
Is the mobile experience flawless for a real guest on a real phone?

| Score | Criteria |
|-------|----------|
| 9-10 | Zero friction. All touch targets correct. Typography perfect. Form easy. No scroll issues. |
| 7-8 | Minor spacing or sizing issues that do not materially harm conversion. |
| 5-6 | Noticeable friction. Elements too small or too close. Form is hard to use. |
| 3-4 | Mobile experience broken or very poor. Layout issues. |
| 0-2 | Desktop-only design pushed to mobile. Unusable. |

### 4. Trust (0-10)
Does the page make the guest feel safe and confident enough to submit their information?

| Score | Criteria |
|-------|----------|
| 9-10 | Strong social proof. Reassurance language. Professional photography. Concierge framing. |
| 7-8 | Trust signals present but could be stronger or more specific. |
| 5-6 | Some trust elements but also trust gaps (no social proof, no reassurance, unclear process). |
| 3-4 | Little trust signaling. Guest must take a leap of faith. |
| 0-2 | Page creates doubt or concern. |

### 5. CTA Clarity (0-10)
Is the primary action obvious, compelling, and easy to take?

| Score | Criteria |
|-------|----------|
| 9-10 | One clear CTA above the fold. Logical CTA reappearance. Action verb is specific. No CTA confusion. |
| 7-8 | CTA is clear but could be stronger or better placed. |
| 5-6 | CTA exists but competes with other actions or is weak in language. |
| 3-4 | CTA is unclear or missing in key moments. |
| 0-2 | No clear action for the guest to take. |

### 6. Copy (0-10)
Does the copy meet brand voice standards?

| Score | Criteria |
|-------|----------|
| 9-10 | Every line is on-brand. No prohibited words. No em dashes. Emotionally specific. Concise. |
| 7-8 | Mostly on-brand with minor violations. |
| 5-6 | Some good lines, some generic or off-brand lines. |
| 3-4 | Mostly generic. Prohibited phrases present. Tone is wrong. |
| 0-2 | Off-brand throughout. |

### 7. Visual Consistency (0-10)
Does the page match the She Said Sail design system?

| Score | Criteria |
|-------|----------|
| 9-10 | Perfect palette, typography, spacing. Indistinguishable from other system pages. |
| 7-8 | Mostly consistent, minor deviations. |
| 5-6 | Some on-brand elements, some that feel out of place. |
| 3-4 | Significant visual inconsistency with the system. |
| 0-2 | Completely different visual language. |

### 8. Backend Readiness (0-10)
Is the page connected correctly to the Airtable and Make backend?

| Score | Criteria |
|-------|----------|
| 9-10 | All form fields correct. Hidden fields populated. Idempotency working. Records creating. |
| 7-8 | Mostly connected. Minor field gaps. |
| 5-6 | Form submits but with data quality issues. |
| 3-4 | Form partially connected. Key fields missing. |
| 0-2 | Form not connected to backend. |

### 9. Analytics Readiness (0-10)
Are the right events tracked for conversion optimization?

| Score | Criteria |
|-------|----------|
| 9-10 | GTM fires. All key events tracked. UTM captured. Scroll depth tracked. |
| 7-8 | Core events tracked. Some gaps in advanced tracking. |
| 5-6 | Basic page view tracked. Form events missing or incomplete. |
| 3-4 | Minimal tracking. Most events missing. |
| 0-2 | No tracking. |

### 10. SEO (0-10)
Is the page optimized for search discovery?

| Score | Criteria |
|-------|----------|
| 9-10 | Complete metadata. OG tags. Correct heading hierarchy. Alt text. Canonical set. |
| 7-8 | Most SEO elements present. Minor gaps. |
| 5-6 | Basic title and description present. OG and alt text incomplete. |
| 3-4 | Minimal SEO. Missing most optimization signals. |
| 0-2 | No SEO optimization. |

### 11. Performance (0-10)
Does the page load fast enough to not lose mobile guests?

| Score | Criteria |
|-------|----------|
| 9-10 | LCP under 2.0s mobile. No render-blocking. Images optimized. |
| 7-8 | LCP under 2.5s. Minor optimization opportunities. |
| 5-6 | LCP 2.5 to 3.5s. Identifiable performance issues. |
| 3-4 | LCP over 3.5s. Significant performance problems. |
| 0-2 | LCP over 5s or page fails to load on mobile. |

### 12. Operational Maturity (0-10)
Is the page operationally complete, with QA docs, audit trail, and implementation notes?

| Score | Criteria |
|-------|----------|
| 9-10 | Full QA doc. Audit doc. Backend doc. Analytics doc. Implementation notes. |
| 7-8 | Most documentation present. Minor gaps. |
| 5-6 | Basic documentation. Missing some operational records. |
| 3-4 | Little documentation. Hard to maintain or debug. |
| 0-2 | No documentation. |

---

## OVERALL SCORE CALCULATION

Sum of all 12 dimensions divided by 12.
Round to one decimal place.

Production threshold: 8.5 overall, no dimension below 7.

---

## AUDIT DOCUMENT FORMAT

Each page audit document must include:
1. Page URL
2. Audit date
3. Score table (all 12 dimensions)
4. Conversion leak list
5. Top 5 priority fixes
6. Implementation status
