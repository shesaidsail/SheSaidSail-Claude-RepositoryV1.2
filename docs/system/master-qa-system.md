# SHE SAID SAIL — MASTER QA SYSTEM
Version: 1.0 | Status: PRODUCTION | Owner: Will Hunt

---

## QA PHILOSOPHY

Every page must pass all checks before launch. No partial launches. No "fix it after."

---

## UNIVERSAL QA CHECKLIST

### Copy QA
- [ ] Zero em dashes on page
- [ ] Zero exclamation marks
- [ ] Zero prohibited words (amazing, unforgettable, elite, etc.)
- [ ] H1 exists exactly once
- [ ] H2/H3 hierarchy is logical
- [ ] All CTA text is sentence case or title case (not ALL CAPS except labels)
- [ ] No orphaned words at end of headings
- [ ] All placeholder text removed
- [ ] Phone/email/address are accurate
- [ ] No lorem ipsum
- [ ] Social proof is real (not invented)

### Visual QA
- [ ] Brand colors match design system exactly
- [ ] Typography matches scale exactly
- [ ] No broken images (all load, correct size)
- [ ] All images have alt text
- [ ] No layout overflow or horizontal scroll
- [ ] Spacing rhythm matches master system
- [ ] Hover states work on all interactive elements
- [ ] Focus states visible on all interactive elements (accessibility)
- [ ] Logo renders correctly at all sizes

### Mobile QA (test at 375px, 390px, 430px)
- [ ] Hero text legible and not truncated
- [ ] CTA buttons full width and 48px+ height
- [ ] No overlapping elements
- [ ] Form fields full width, 16px font
- [ ] No horizontal scroll
- [ ] Images not cropped to hide subject
- [ ] Section spacing feels calm, not cramped
- [ ] Navigation works

### Form QA
- [ ] All required fields marked
- [ ] Validation fires on empty submit
- [ ] Hidden fields populated (source_url, UTMs)
- [ ] `experience` field pre-populated with correct value
- [ ] Submit fires webhook successfully
- [ ] Success state shows after submission
- [ ] Email auto-reply arrives within 2 minutes
- [ ] Airtable Request record created correctly
- [ ] Slack alert fires to #sss-ops-alerts
- [ ] Duplicate submission blocked by idempotency check

### SEO QA
- [ ] Page title: 50–60 chars, includes primary keyword
- [ ] Meta description: 120–155 chars, includes keyword, emotion-first
- [ ] H1 includes primary keyword naturally
- [ ] Open Graph title set
- [ ] Open Graph description set
- [ ] Open Graph image set (1200x630px)
- [ ] Twitter card meta set
- [ ] Canonical URL set
- [ ] No duplicate H1 tags
- [ ] Schema markup present (if applicable)

### Performance QA
- [ ] Google PageSpeed mobile score 80+
- [ ] LCP under 2.5s
- [ ] CLS under 0.1
- [ ] FID/INP under 200ms
- [ ] No render-blocking resources in critical path
- [ ] Images use WebP or optimized JPEG
- [ ] Hero image under 400kb
- [ ] No unused CSS/JS loaded on page

### Analytics QA
- [ ] GTM container loads
- [ ] GA4 pageview fires
- [ ] Form start event fires
- [ ] Form submit event fires with correct labels
- [ ] CTA click events fire
- [ ] Scroll depth events fire
- [ ] UTM parameters captured in dataLayer
- [ ] All events visible in GA4 DebugView

### Backend QA
- [ ] Webhook endpoint is live
- [ ] Idempotency check blocks duplicate leads
- [ ] Environment field writes "Production" correctly
- [ ] Brand field writes "SSS" correctly
- [ ] All webhook payload keys match Make module expectations
- [ ] Error handling: failed webhook does not break page UX

---

## SIGN-OFF GATES

| Gate | Description | Who Signs Off |
|------|-------------|---------------|
| COPY | All copy QA checks pass | Will or designated reviewer |
| VISUAL | All visual QA checks pass | Will or designer |
| MOBILE | All mobile QA checks pass | Tester on real device |
| FORM | Form end-to-end test passes | Developer + Will |
| SEO | SEO QA checks pass | Developer |
| ANALYTICS | Analytics QA checks pass | Developer |
| BACKEND | Backend QA checks pass | Developer |

All 7 gates must pass before page is marked PRODUCTION READY.
