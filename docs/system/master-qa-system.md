# SHE SAID SAIL
# MASTER QA SYSTEM

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## QA PHILOSOPHY

Every page passes QA only when a real person on a real mobile device would encounter no friction, no confusion, no broken elements, and feel fully confident inquiring.

---

## MASTER QA CHECKLIST

### Visual QA

- [ ] Hero image loads within 2.5 seconds on mobile
- [ ] Hero image is not pixelated or stretched at any breakpoint
- [ ] All text is readable against its background (4.5:1 minimum contrast)
- [ ] Gold eyebrow text is visible on dark and light backgrounds
- [ ] No text overflows its container on any breakpoint
- [ ] No horizontal scroll at any viewport width
- [ ] Spacing is consistent and rhythmic (not cramped, not bloated)
- [ ] All images have accurate alt text
- [ ] No placeholder text or lorem ipsum visible

### Typography QA

- [ ] H1 is the only H1 on the page
- [ ] Heading hierarchy is correct (H1 > H2 > H3, no skipping)
- [ ] Body text minimum 16px on mobile
- [ ] Input fields minimum 16px font size (prevents iOS zoom)
- [ ] No em dashes anywhere on the page
- [ ] Prohibited words are not present
- [ ] CTA text is action-oriented and declarative

### Mobile QA

- [ ] Tested on iPhone SE (375px viewport)
- [ ] Tested on iPhone 14 Pro (393px viewport)
- [ ] Tested on iPad (768px viewport)
- [ ] All touch targets minimum 48px
- [ ] CTA buttons full width on mobile
- [ ] Form fields full width on mobile
- [ ] No two-column layout on mobile (unless intentional and tested)
- [ ] Nav hamburger menu works
- [ ] Floating CTA appears after hero scroll
- [ ] Smooth scroll to form anchor works

### Form QA

- [ ] All required fields are marked and validated
- [ ] Hidden fields are populated correctly on page load
  - [ ] source_url captures full URL
  - [ ] utm_source captured if present in URL
  - [ ] utm_medium captured if present in URL
  - [ ] utm_campaign captured if present in URL
  - [ ] experience_name pre-filled correctly
- [ ] Form submits without errors
- [ ] Success state is visible and reassuring
- [ ] Error state is visible and specific
- [ ] Airtable record created on submission
- [ ] Confirmation email received within 60 seconds
- [ ] Slack alert received in #sss-ops-alerts
- [ ] No duplicate records created on double-submit

### SEO QA

- [ ] Page title: under 60 characters, includes experience name
- [ ] Meta description: 130-160 characters, includes occasion and location
- [ ] Open Graph title set
- [ ] Open Graph description set
- [ ] Open Graph image set (1200x630, experience hero image)
- [ ] Twitter card tags set
- [ ] Canonical URL set
- [ ] H1 contains primary keyword
- [ ] Alt text on all images
- [ ] No duplicate title or description

### Performance QA

- [ ] LCP under 2.5 seconds (mobile)
- [ ] No render-blocking resources above fold
- [ ] Images served as WebP where possible
- [ ] Hero image compressed (under 300KB)
- [ ] No layout shift (CLS under 0.1)
- [ ] First Input Delay under 100ms

### Analytics QA

- [ ] GTM fires on page load
- [ ] GA4 page view tracked
- [ ] Form submission event tracked (sss_lead_submitted)
- [ ] CTA clicks tracked (sss_cta_click)
- [ ] UTM parameters captured in dataLayer
- [ ] Scroll depth events fire at 25%, 50%, 75%, 100%

### Accessibility QA

- [ ] Skip to content link present
- [ ] All interactive elements keyboard navigable
- [ ] Focus states visible on all interactive elements
- [ ] Form labels associated with inputs (not just placeholders)
- [ ] Error messages announced to screen readers
- [ ] Images with decorative function have empty alt=""
- [ ] Images with informational function have descriptive alt text

### Backend QA

- [ ] Experience name in hidden field matches Airtable canonical
- [ ] Brand detection works (SSS vs ME from source_url)
- [ ] Idempotency key formatted correctly
- [ ] Status field = "NEW" on creation
- [ ] Environment field = "Production"

---

## QA SIGN-OFF CRITERIA

A page passes QA when:
- All checklist items are checked
- A live test submission creates the correct Airtable record
- The page scores 9 or above on the master audit scorecard
- No critical mobile UX issues remain

---

## QA FAILURE CATEGORIES

| Severity | Category | Examples |
|----------|----------|---------|
| P0 - Blocker | Form does not submit | Webhook error, CORS failure, JS error breaking submit |
| P0 - Blocker | No Airtable record created | Wrong field names, idempotency blocking all submissions |
| P1 - Critical | Mobile layout broken | Horizontal scroll, text overflow, touch targets too small |
| P1 - Critical | Hidden fields empty | UTM data lost, source URL not captured |
| P2 - High | Confirmation email not sent | Make scenario failing |
| P2 - High | SEO metadata missing | No OG image, no meta description |
| P3 - Medium | Analytics events missing | GTM not firing, GA4 events absent |
| P3 - Medium | Copy violations | Em dashes, prohibited words |
