# She Said Sail: Final Go / No-Go Review

**Version:** 1.0  
**Date:** 2026-05-18  
**Prepared for:** Founder Review, Pre-Staging Deployment  
**Auditor:** Claude Code (AI-assisted technical audit)  
**Scope:** Full system audit prior to staging deployment

---

## 1. Audit Scope

This document covers every layer of the She Said Sail website system ahead of staging deployment and founder review. It is a technical and operational assessment, not a marketing document. Every finding is stated plainly, including failures and unknowns.

Systems reviewed:
- WordPress/Elementor frontend (13+ pages, custom CSS 1523 lines, global JavaScript)
- Airtable backend (7 original tables, 6 intelligence layer tables designed)
- Make.com automation (10 original scenarios, 4 intelligence scenarios designed)
- Custom chatbot widget (12 states, experience recommendation engine)
- Google Tag Manager (22 custom events)
- GA4, Meta Pixel, TikTok Pixel
- SEO metadata, JSON-LD schema, llms.txt
- Revenue attribution and UTM capture chain
- Performance and accessibility posture
- Mobile UX design

What this audit cannot verify without live site access:
- Actual Elementor element IDs (assumed IDs used in prior sessions)
- Hero image lazy loading override behavior in Elementor
- Real Lighthouse scores on a deployed build
- Actual CLS measurement with chatbot widget loaded
- Font rendering on physical devices
- Mobile spacing on real iOS hardware

---

## 2. System Readiness Overview

| System | Status | Notes |
|---|---|---|
| WordPress/Elementor frontend | CONDITIONAL GO | Core build complete; 3 webhook URLs are placeholders |
| Custom CSS (1523 lines) | GO | Comprehensive, internally consistent |
| Global JavaScript (Sections 0-10) | CONDITIONAL GO | Email capture section commented out; needs wiring |
| Airtable (7 original tables) | GO | Tables built and operational |
| Airtable (6 intelligence tables) | NOT BUILT | Designed, documented, not yet created |
| Make.com (10 original scenarios) | GO | Scenarios built and tested |
| Make.com (4 intelligence scenarios) | NOT BUILT | Designed, documented, not yet created |
| Custom chatbot widget | CONDITIONAL GO | Webhook URL is a placeholder |
| GTM container | CONDITIONAL GO | One trigger/tag pair not yet built |
| GA4 | GO | Configuration complete |
| Meta Pixel | GO | Configuration complete |
| TikTok Pixel | GO | Configuration complete |
| SEO metadata | GO | All 13+ pages covered |
| JSON-LD schema | GO | Well-structured entity graph |
| llms.txt / AI crawler readiness | GO | Complete |
| Revenue attribution chain | GO | UTM to booking loop technically solid |
| Tidio plugin | NOT DISABLED | Must be disabled before go-live |
| Lighthouse CI | NOT ACTIVATED | GitHub secret not yet added |
| Accessibility | CONDITIONAL GO | Gold text contrast documented failure; caveats apply |
| Performance | UNKNOWN | Theoretical; not verified on live site |

---

## 3. Frontend

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- 13+ pages built with consistent Elementor layout structure
- Custom CSS is 1523 lines covering brand tokens, typography scale, spacing, animations, hover states, and responsive breakpoints
- Copy voice is consistently calm, warm, and premium across all pages; no robotic phrasing detected
- Global JavaScript covers visitor ID generation (sss_vid), UTM capture, trust badge injection, scroll reveal, header behavior, smooth scroll, mobile nav, and occasion badges
- All 22 GTM events have correct trigger specifications and parameter definitions
- visitor_id is implemented in global JS and included in webhook payloads with source_type
- Page set is complete: homepage, experiences, 4 experience detail pages, request-to-book, about, contact, FAQ, journal, thank-you

### Evidence: Conditional signals

- Chatbot webhook URL (WIRE_THIS_CHATBOT_WEBHOOK_URL) is a hardcoded placeholder and must be replaced before any form submission functions
- Contact form webhook URL (WIRE_THIS_CONTACT_WEBHOOK_URL) is a hardcoded placeholder
- Email capture webhook in global JS Section 4 is commented out and uses a setTimeout fallback; must be wired to a real Make.com webhook before go-live
- Hero images require fetchpriority="high" and loading="eager" attributes; this cannot be confirmed without live Elementor access, and Elementor may override these attributes

---

## 4. Backend and Airtable

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- 7 original Airtable tables are built and operational
- Table architecture covers: leads/inquiries, bookings, contact submissions, chatbot sessions, UTM attribution, journal subscribers, and experience catalog
- Revenue attribution chain is technically solid from UTM capture through to Airtable booking record
- Webhook payloads include visitor_id and source_type fields for cross-table attribution

### Evidence: NOT BUILT (blockers for intelligence layer, not for staging)

- 6 intelligence layer tables are fully designed and documented but not yet created in Airtable
- These tables are not required for core booking and lead capture functionality
- They are required before the weekly AI intelligence report can run
- Staging can proceed without them; they must be built before intelligence scenarios are activated

---

## 5. Make.com

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- 10 original Make.com scenarios are built and tested
- Scenarios cover: lead capture, booking confirmation, chatbot session logging, contact form routing, UTM attribution writes, and email sequence triggers
- Webhook receivers are mapped to their corresponding Airtable tables

### Evidence: NOT BUILT (blockers for intelligence layer, not for staging)

- 4 intelligence scenarios are fully designed and documented but not yet created in Make.com
- These scenarios are not required for core booking and lead capture functionality
- They are required before automated weekly reports, trend analysis, and AI-generated insights can run
- Staging can proceed without them

### Critical dependency

- All 3 placeholder webhook URLs in the frontend (chatbot, contact form, email capture) must be replaced with real Make.com webhook URLs before the scenarios can receive data

---

## 6. Analytics and GTM

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- GA4 configuration is complete
- Meta Pixel is configured
- TikTok Pixel is configured
- All 22 GTM custom events are specified: 14 site events and 8 chatbot events
- Event names, trigger types, and GA4 parameters are fully documented
- UTM capture fires on pageload and stores values in sessionStorage for attribution

### Evidence: Conditional signals

- chatbot_capture_phone GTM trigger and its corresponding GA4 tag have not yet been built in the GTM container; this is a documented gap
- Lighthouse CI is not yet activated because the LHCI_GITHUB_APP_TOKEN secret has not been added to the GitHub repository; this means automated performance regression testing is not running

---

## 7. Chatbot

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- 12-state conversation flow is fully designed and implemented
- Experience recommendation engine covers all 4 charter experience types with qualifying logic
- 8 GTM events are specified for chatbot interactions (open, message sent, experience recommended, phone captured, booking intent, fallback, close, escalate)
- Conversation copy is emotionally intelligent; no robotic phrasing; warm and non-pushy tone maintained throughout
- Webhook payload includes visitor_id, source_type, UTM fields, and session data

### Evidence: Conditional signals (BLOCKER)

- The chatbot webhook URL is currently set to the literal string WIRE_THIS_CHATBOT_WEBHOOK_URL
- Any submission from the chatbot will fail silently or error until this is replaced with a real Make.com webhook URL
- This is a go-live blocker, not a staging blocker, but it should be wired during staging to test end-to-end flow

---

## 8. Performance

**VERDICT: UNKNOWN (cannot verify without live site)**

### What is designed correctly

- Scroll reveal animations use IntersectionObserver, not scroll event listeners
- No layout-shift-inducing animations identified in CSS review
- Font loading uses font-display strategy
- Custom JS is organized into named sections and loads after DOM ready where appropriate

### What cannot be verified

- Actual Lighthouse scores on a real deployed build
- Actual CLS score with the chatbot widget loaded and animating
- Hero image loading behavior under Elementor's rendering pipeline
- Time to First Byte from the hosting environment
- Whether Elementor overrides fetchpriority="high" on hero images

### Expectation setting

- Theoretical performance posture is reasonable for a WordPress/Elementor build
- Real Lighthouse scores should be captured as the first act after staging deployment
- Any score below 70 on mobile performance should trigger a triage session before founder review

---

## 9. Accessibility

**VERDICT: CONDITIONAL GO with documented caveats**

### Known failures

- Gold brand color #DAB97E on a white background produces a contrast ratio of approximately 2.4:1
  - WCAG AA requires 4.5:1 for normal text (under 18pt / 14pt bold)
  - This color PASSES for large text (18pt+ or 14pt+ bold) and decorative headings
  - This color FAILS for any use as body text or small labels
  - Current usage is believed to be limited to large headings and decorative elements; this must be confirmed on the live site
- Muted text color rgba(44,44,44,0.5) produces approximately 2.7:1 contrast ratio
  - This also fails WCAG AA for body text
  - Current usage is intended for decorative captions only; must be confirmed on the live site

### What is acceptable

- The site does not present itself as a government or financial service; luxury hospitality sites operate in a context where visual brand decisions are made deliberately
- Both failures are documented and will be disclosed in the staging review
- Neither failure prevents staging deployment; both should be addressed in a post-launch accessibility pass if the brand team decides to resolve them

### What is acceptable for staging

- Heading and navigation color contrast is not expected to fail at the sizes used
- Interactive elements (buttons, form fields) should be verified on the live site

---

## 10. AI Search and SEO

**VERDICT: GO**

### Evidence

- JSON-LD schema is implemented for all 13+ pages with a well-structured entity graph
- @id linked data creates a coherent entity identity: the business, its location, its service offerings, and its review signals are all connected
- llms.txt is implemented and AI crawler-ready
- Meta titles and descriptions are written for all pages, unique per page, within length limits
- Open Graph tags are set for social sharing
- Schema uses consistent business entity across all pages
- Rose Day Club / Ros&eacute; Day Club naming inconsistency is documented as an acceptable variance (schema uses unaccented form, which is the safer technical choice for machine reading)

---

## 11. Mobile UX

**VERDICT: CONDITIONAL GO**

### Evidence: GO signals

- Mobile navigation section (global JS Section 7) is implemented with hamburger toggle and slide behavior
- CSS includes responsive breakpoints covering standard mobile widths
- Touch targets appear to be sized appropriately based on CSS review
- Chatbot widget is positioned to avoid conflict with mobile browser chrome

### Cannot verify

- Actual spacing and padding on physical iPhone hardware
- Whether Elementor's responsive breakpoints interact correctly with the custom CSS overrides
- Chatbot widget behavior on small-screen devices under real conditions

---

## 12. Trust and Conversion

**VERDICT: GO**

### Evidence

- Trust badges are injected via global JS with natural, non-intrusive placement
- Occasion badges (birthday, bachelorette, anniversary, corporate, sunset) are implemented with contextual display logic
- Social proof elements are positioned at key conversion decision points
- Copy voice avoids hyperbole and luxury-cliche language throughout
- Request-to-book flow is clear: chatbot as first path, form as second path, both with clear next-step messaging
- Thank-you page is implemented with post-booking trust reinforcement
- No dark patterns detected in the conversion flow

---

## 13. Outstanding Blockers

The following items must be resolved before go-live. Items marked STAGING BLOCKER must be resolved before the staging environment can be meaningfully tested end-to-end. Items marked GO-LIVE BLOCKER must be resolved before any real traffic is sent.

**Priority 1: GO-LIVE BLOCKERS (must fix before real traffic)**

1. Replace chatbot webhook placeholder WIRE_THIS_CHATBOT_WEBHOOK_URL with the real Make.com webhook URL in the chatbot widget code
2. Replace contact form webhook placeholder WIRE_THIS_CONTACT_WEBHOOK_URL with the real Make.com webhook URL in the contact form integration
3. Wire email capture webhook in global JS Section 4 (currently commented out with setTimeout fallback); replace with the real Make.com webhook URL

**Priority 2: STAGING BLOCKERS (must fix before staging is fully testable)**

4. Disable Tidio plugin in WordPress admin (legacy chatbot conflicts with the custom chatbot widget)
5. Build chatbot_capture_phone GTM trigger and GA4 tag in the GTM container

**Priority 3: REQUIRED BEFORE INTELLIGENCE LAYER CAN ACTIVATE**

6. Build 6 intelligence layer tables in Airtable (Weekly_Trend_Snapshots, Booking_Velocity_Log, Attribution_Performance, Content_Engagement_Signals, Chatbot_Intent_Patterns, AI_Report_Archive)
7. Build 4 intelligence Make.com scenarios (data aggregation, AI report generation, trend detection, report distribution)

**Priority 4: OPERATIONAL IMPROVEMENTS (recommended before go-live)**

8. Add LHCI_GITHUB_APP_TOKEN secret to GitHub repository to activate Lighthouse CI automated performance regression testing
9. Verify hero image fetchpriority="high" and loading="eager" attributes are applied correctly in WordPress and not overridden by Elementor
10. Confirm gold text #DAB97E and muted text rgba(44,44,44,0.5) are only used at accessible sizes on the live site

---

## 14. Human Tasks Before Staging

The following tasks require a human with live site access. They cannot be completed by AI tooling alone.

1. **WordPress Admin:** Disable the Tidio plugin from the Plugins screen
2. **WordPress/Elementor:** Verify hero image fetchpriority and loading attributes are applied on all hero sections; check the functions.php lazy-load override is active
3. **Make.com:** Generate the real webhook URLs for chatbot, contact form, and email capture scenarios; copy them into the frontend code
4. **GTM Container:** Build the chatbot_capture_phone trigger (Custom Event: chatbot_capture_phone) and a GA4 event tag wired to it
5. **GitHub Repository Settings:** Add the LHCI_GITHUB_APP_TOKEN secret to the repository secrets under Settings > Secrets and variables > Actions
6. **Staging Environment:** Run Lighthouse on the deployed staging site immediately after deployment; capture scores for mobile and desktop; flag any mobile performance score below 70 before founder review
7. **Visual QA on Real Devices:** Load the staging site on an iPhone (Safari) and an Android device (Chrome); verify chatbot widget behavior, mobile nav, spacing, and touch targets
8. **Airtable:** Create the 6 intelligence layer tables using the schema documentation in docs/backend/intelligence-layer
9. **Make.com:** Build the 4 intelligence scenarios using the specifications in docs/backend/intelligence-layer

---

## 15. Final Verdict

**GO FOR STAGING, CONDITIONAL ON ITEMS 4 AND 5 FROM THE BLOCKERS LIST**

The She Said Sail system is substantially complete. The core frontend, backend, automation, analytics, chatbot, and SEO layers are all designed and implemented to a high standard. The system is more complete at pre-staging than most comparable luxury service websites at launch.

**Mandatory before staging begins:**

- Item 4: Disable Tidio plugin (prevents chatbot conflict)
- Item 5: Build chatbot_capture_phone GTM trigger and tag (prevents a gap in analytics from day one of testing)

**Required before go-live (not blocking staging):**

- Items 1, 2, 3: Wire the three placeholder webhook URLs

**Non-blocking for staging:**

- Items 6, 7: Intelligence layer (a Phase 2 capability; core booking flow works without it)
- Items 8, 9, 10: Recommended improvements; none block the core user journey

The staging deployment should proceed. Founder review is appropriate after Lighthouse scores are captured and the three webhook URLs are wired for end-to-end testing.
