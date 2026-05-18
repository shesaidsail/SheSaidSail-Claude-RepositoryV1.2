# She Said Sail: Final Site Scorecard

**Version:** 1.0  
**Date:** 2026-05-18  
**Prepared for:** Founder Review, Pre-Staging Deployment  
**Auditor:** Claude Code (AI-assisted technical audit)  
**Purpose:** Honest pre-deployment assessment across all system dimensions. No score inflation.

---

## Scoring Key

| Score | Meaning |
|---|---|
| 9-10 | Excellent: production-grade, no meaningful gaps |
| 7-8 | Good: solid foundation, minor gaps only |
| 5-6 | Adequate: functional but with notable weaknesses |
| 3-4 | Weak: significant gaps that should be addressed |
| 1-2 | Failing: not fit for purpose in current state |

---

## 1. Luxury Positioning and Brand

**Score: 8 / 10**

The brand voice is consistently calm, warm, and premium across all pages and the chatbot. The CSS design system uses a well-chosen palette (deep navy, gold accent, warm white), a clear typographic hierarchy, and restrained animations that reinforce the luxury register. The copy avoids both hyperbole and the hollow phrases common to budget charter sites. The occasion badge system (bachelorette, anniversary, birthday, corporate, sunset) adds personality without cheapening the brand.

Deductions: The gold text contrast failure (#DAB97E at 2.4:1) is a brand liability if it ever appears at body text sizes. The 13-page site would benefit from more editorial depth in the journal section at launch to reinforce the premium positioning.

---

## 2. Emotional Conversion Quality

**Score: 8 / 10**

The request-to-book funnel is clear and non-pushy. The chatbot is the primary conversion path and its 12-state conversation flow is emotionally intelligent: it qualifies intent, recommends the right experience, and moves toward booking without feeling like a sales script. The copy at each stage maintains the brand voice rather than switching into transactional mode. The thank-you page reinforces the decision with trust signals rather than just confirming the form submission.

Deductions: Social proof (reviews, testimonials) is structurally positioned correctly, but the volume and freshness of that content cannot be assessed from a code review. If the live site launches with minimal or dated social proof, the conversion quality will suffer regardless of the system quality.

---

## 3. Visual Consistency

**Score: 9 / 10**

The 1523-line custom CSS is the strongest single technical asset in this build. Brand tokens are defined once and referenced throughout. Typography scale, spacing units, color variables, animation durations, and z-index layers are all systematically managed. There are no visual one-offs or orphaned styles found in the CSS review. The chatbot widget, trust badges, occasion badges, and scroll reveal elements all use the same design language as the page-level components.

Deduction: One point held back because Elementor's visual override behavior on the live site cannot be confirmed without deployment; Elementor sometimes introduces inline styles that override custom CSS in unpredictable ways.

---

## 4. Mobile UX

**Score: 6 / 10**

The mobile navigation is implemented with a hamburger toggle and slide behavior. CSS breakpoints cover standard mobile widths. The chatbot widget is positioned to avoid conflict with mobile browser chrome. Touch targets appear correctly sized based on code review.

Score limited to 6 because: this dimension cannot be properly assessed without physical device testing. Mobile spacing on real iOS Safari, actual touch interaction with the chatbot, hero image behavior at narrow widths, and Elementor's responsive column behavior on small screens are all unverified. Mobile is consistently the area where WordPress/Elementor builds diverge most from design intent, and that variance is unknown here.

---

## 5. Trust and Social Proof

**Score: 7 / 10**

Trust badge injection, occasion badges, social proof placement, and review positioning are all correctly structured in the system. The conversion flow does not use dark patterns. The thank-you page reinforces the decision. The request-to-book page has clear next-step messaging.

Score limited to 7 because: the actual content of reviews, testimonials, and social proof has not been reviewed in this audit (it lives in Elementor content, not in the codebase). The infrastructure is strong; the content quality and volume are unknown.

---

## 6. Chatbot Quality

**Score: 8 / 10**

The chatbot is genuinely the standout feature of this build. A 12-state conversation flow with an experience recommendation engine, 8 GTM event integrations, emotionally intelligent copy, and a complete webhook payload architecture is a significant achievement for a pre-launch system. The flow handles qualification, recommendation, phone capture, booking intent, and escalation paths. The copy voice is warm throughout and never breaks register.

Deductions: The webhook URL is currently a placeholder (WIRE_THIS_CHATBOT_WEBHOOK_URL), which means the chatbot has not been tested end-to-end in a live environment. One deduction for the untested state. One deduction for the fact that the chatbot_capture_phone GTM trigger has not yet been built in the GTM container, leaving a gap in phone capture analytics.

---

## 7. Backend Architecture Readiness

**Score: 7 / 10**

The overall architecture is well-designed. The Airtable schema, Make.com scenario chain, and webhook payload structures are coherent and internally consistent. The revenue attribution chain (UTM to session to booking to Airtable) is technically sound. The visitor_id (sss_vid) implementation provides cross-session identity for attribution reporting. The intelligence layer architecture is ambitious and well-documented.

Score limited to 7 because: the intelligence layer tables and scenarios are designed but not built, and the three webhook URLs are placeholders. The architecture is excellent on paper; the implementation is at approximately 70% completion.

---

## 8. Airtable Readiness

**Score: 6 / 10**

The 7 original Airtable tables are built and operational. Table structure, field types, and relationships are correctly designed for the booking and lead capture use cases. The webhook payloads from Make.com are mapped to the correct Airtable fields.

Score limited to 6 because: the 6 intelligence layer tables are not yet created. These are not blocking for core functionality, but they represent a significant planned capability that is incomplete. A score above 6 would require the intelligence tables to exist.

---

## 9. Make.com Readiness

**Score: 6 / 10**

The 10 original Make.com scenarios are built and tested. They cover the core booking and lead capture automation chain. Scenario architecture is clean and the error handling paths are defined.

Score limited to 6 because: the 4 intelligence scenarios are not yet built. Additionally, none of the 3 placeholder webhook URLs have been replaced yet, so even the 10 existing scenarios cannot receive data from the live site until those URLs are wired. The scenarios exist; the connections to the frontend do not yet.

---

## 10. Analytics Readiness

**Score: 7 / 10**

GA4, Meta Pixel, and TikTok Pixel are all configured. All 22 GTM custom events are specified with correct trigger types and parameter definitions. The UTM capture chain feeds sessionStorage attribution data into webhook payloads for Airtable writes. The attribution loop from first visit through to booking record is technically designed correctly.

Score limited to 7 because: the chatbot_capture_phone GTM trigger and GA4 tag are not yet built in the GTM container (a documented gap). Lighthouse CI is not yet activated. The analytics have not been validated on a live deployment.

---

## 11. AI Search Readiness

**Score: 9 / 10**

This is the strongest SEO-adjacent dimension in the build. llms.txt is implemented. JSON-LD schema creates a coherent entity graph with @id linked data connecting the business, location, service types, and review signals. The schema is technically correct and structured for machine reading by both traditional search crawlers and AI-powered search systems. The approach is forward-looking and well-executed.

One point held back for the Rose Day Club / Ros&eacute; Day Club naming inconsistency between schema and display copy. This is documented as an acceptable variance, and the technical choice (unaccented in schema) is defensible, but it is still an inconsistency.

---

## 12. SEO

**Score: 8 / 10**

Meta titles and descriptions are written for all 13+ pages, are unique per page, and are within length limits. Open Graph tags are set. JSON-LD schema is comprehensive. The page set covers the full topic surface area for Miami luxury yacht charter search intent (experience types, occasions, location, booking).

Deductions: Actual Lighthouse SEO scores cannot be confirmed without live deployment. The journal section is structurally present but editorial content depth at launch is unknown; thin journal content would limit long-tail organic performance.

---

## 13. Accessibility

**Score: 5 / 10**

The score here reflects honesty about documented failures rather than architectural problems.

The system has two confirmed WCAG AA contrast failures: gold text #DAB97E at 2.4:1 (requires 4.5:1 for normal text) and muted text rgba(44,44,44,0.5) at approximately 2.7:1. Both failures are documented. Both are limited to decorative and heading contexts in the current design, but that usage has not been verified on the live site.

Interactive elements, form fields, and navigation contrast are not expected to fail, but have not been verified on the live deployed site. Screen reader behavior with the custom chatbot widget has not been tested. Focus management in the chatbot conversation flow is not documented.

This score is not a statement that the site is unusable; it is a statement that accessibility has not been a primary design constraint and two specific known failures exist.

---

## 14. Performance (Theoretical, Not Verified on Live Site)

**Score: 6 / 10**

The performance posture is reasonable for a WordPress/Elementor build. Scroll reveal uses IntersectionObserver. No continuous scroll-event listeners are used. Font loading strategy is defined. Custom JS loads after DOM ready. The chatbot widget is isolated from main thread rendering.

Score limited to 6 because: WordPress/Elementor builds typically score 55-75 on mobile Lighthouse performance without aggressive optimization, and no optimization pass (image compression, cache configuration, CDN setup, CSS/JS minification review) has been verified. Hero image loading attributes cannot be confirmed without live access. Elementor's render pipeline adds overhead that is not visible in a code review. This score reflects a realistic prior for this type of build, not a confirmed measurement.

---

## 15. Operational Maturity

**Score: 7 / 10**

The system is operationally mature in several important ways. The weekly AI intelligence report architecture provides the founder with ongoing signal about booking velocity, attribution performance, and chatbot intent patterns. The Make.com scenarios handle the full automation chain without requiring manual intervention for standard bookings. GTM event coverage gives the team visibility into user behavior at a granular level. The Airtable schema is designed for reporting, not just storage.

Score limited to 7 because: the intelligence layer is not yet built, Lighthouse CI is not yet active, and the three webhook placeholder URLs mean the system has not operated end-to-end in a real environment yet. Operational maturity must be demonstrated, not just designed.

---

## 16. Scalability

**Score: 7 / 10**

The architecture is designed to scale. Airtable can handle several years of booking volume at the projected charter frequency before hitting meaningful record limits. Make.com scenarios are modular and new automation branches can be added without rebuilding the core chain. The chatbot can be extended with new experience types by adding states and routing logic. The CSS design system uses tokens that allow brand updates to propagate with single-point changes. The intelligence layer, once built, provides a data foundation for more sophisticated demand analysis.

Deductions: WordPress/Elementor has inherent scalability constraints for high-traffic scenarios, though a luxury charter site does not face the traffic volumes that would expose those constraints. The primary scalability risk is operational: as booking volume grows, the manual elements of the workflow (captain assignment, calendar management) will need tooling that is not yet designed.

---

## Summary Scorecard

| # | Dimension | Score |
|---|---|---|
| 1 | Luxury Positioning and Brand | 8 |
| 2 | Emotional Conversion Quality | 8 |
| 3 | Visual Consistency | 9 |
| 4 | Mobile UX | 6 |
| 5 | Trust and Social Proof | 7 |
| 6 | Chatbot Quality | 8 |
| 7 | Backend Architecture Readiness | 7 |
| 8 | Airtable Readiness | 6 |
| 9 | Make.com Readiness | 6 |
| 10 | Analytics Readiness | 7 |
| 11 | AI Search Readiness | 9 |
| 12 | SEO | 8 |
| 13 | Accessibility | 5 |
| 14 | Performance (theoretical) | 6 |
| 15 | Operational Maturity | 7 |
| 16 | Scalability | 7 |
| | **Average** | **7.1 / 10** |

---

## Top 3 Strengths

**1. Visual Consistency and Design System (9/10)**
The 1523-line custom CSS is genuinely excellent. Brand tokens, typography scale, animation system, and component styles are all systematically managed. This is the layer that will make the site feel premium on first impression and continue to feel cohesive as content is added.

**2. AI Search and Entity Architecture (9/10)**
The JSON-LD schema entity graph and llms.txt implementation are sophisticated and forward-looking. Most luxury service sites do not have this level of structured data at launch. This is a durable competitive advantage for AI-powered search visibility.

**3. Chatbot Quality (8/10)**
The 12-state emotionally intelligent chatbot is the most differentiated feature in the build. A custom experience recommendation engine with full GTM and Airtable integration, written in a consistent brand voice, is not a standard offering at this price point. It is the primary conversion path and it is well-designed.

---

## Top 3 Weaknesses

**1. Accessibility (5/10)**
Two confirmed WCAG AA contrast failures exist and are unresolved. This is the only dimension that scored below 6. The failures are in brand color choices rather than structural problems, which means they could be addressed without a major redesign, but that work has not been done.

**2. Incomplete Implementation (Make.com and Airtable intelligence layer, 6/10 each)**
The intelligence layer is a significant planned capability that is designed but not built. This is not a blocker for staging, but it means the system is operating at partial capacity. The three placeholder webhook URLs also mean the connection between the live site and the automation backend has not been tested.

**3. Performance Uncertainty (6/10)**
Real Lighthouse scores are unknown. WordPress/Elementor builds can range widely on mobile performance, and no optimization pass has been confirmed. Hero image loading behavior under Elementor's rendering pipeline is unverified. This uncertainty is a risk, not a confirmed failure, but it should be treated as a priority on day one of staging.

---

## Overall Readiness

**STAGING READY**

The system scores 7.1/10 on average across 16 dimensions, with the strongest scores in visual quality, SEO, and AI search readiness. The weaknesses are specific and documented. None of the weaknesses represent fundamental architectural problems; they are implementation gaps and one brand constraint (accessibility) that were knowingly accepted.

The system is staging ready. It is not yet go-live ready without resolving the three placeholder webhook URLs and disabling the Tidio plugin. The intelligence layer is a Phase 2 deliverable and does not affect staging readiness.

For the founder review: this is a well-built system for a pre-launch luxury hospitality website. The gaps are honest and fixable. The strengths are durable.
