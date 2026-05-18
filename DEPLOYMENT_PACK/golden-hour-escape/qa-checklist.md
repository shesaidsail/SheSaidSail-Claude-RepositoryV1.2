# GOLDEN HOUR ESCAPE — QA CHECKLIST
Version: 1.0 | Date: May 2026 | Status: READY FOR HUMAN QA

Complete all checks before marking page as PRODUCTION READY.
Assign a tester to each section. Record pass/fail and date tested.

---

## SECTION 1: COPY QA

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 1 | Zero em dashes on page | | |
| 2 | Zero exclamation marks | | |
| 3 | Zero prohibited words (amazing, unforgettable, elite, VIP, exclusive, epic, incredible) | | |
| 4 | H1 "The light is best at the end of the day." appears exactly once | | |
| 5 | H2/H3 hierarchy is logical (no H3 before H2) | | |
| 6 | Page title is: Golden Hour Escape | Private Sunset Sailing Charter | She Said Sail | | |
| 7 | Meta description matches spec in metadata.html (120-155 chars) | | |
| 8 | All CTA text: "Reserve your date" / "Plan your escape" / "Send my inquiry" | | |
| 9 | Form has label "Tell us about your group." | | |
| 10 | Reassurance text present below form | | |
| 11 | No lorem ipsum or placeholder text | | |
| 12 | Phone number (754) 701-2228 is correct | | |
| 13 | Email hello@shesaidsail.com is correct | | |

---

## SECTION 2: VISUAL QA

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 14 | Hero background is full-bleed image with navy overlay | | |
| 15 | Eyebrow text is gold, uppercase, tracked | | |
| 16 | CTA button is gold background, navy text | | |
| 17 | Section labels are gold, uppercase, tracked | | |
| 18 | Gold rule dividers appear above section headings | | |
| 19 | Overview strip is navy background with white/gold text | | |
| 20 | Reviews section is navy background | | |
| 21 | Form section is white background | | |
| 22 | No broken images | | |
| 23 | All images have descriptive alt text | | |
| 24 | Hero image loads first (eager loading, not lazy) | | |
| 25 | All other images are lazy loaded | | |
| 26 | Hover state on primary CTA button (darkens to #b8963d) | | |
| 27 | Hover state on secondary CTA button | | |
| 28 | Focus states visible on all form fields | | |

---

## SECTION 3: MOBILE QA

Test on 375px, 390px, 430px width. Test on real device if possible.

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 29 | Hero headline is legible and not truncated (34px+) | | |
| 30 | Hero CTA button is full width on mobile | | |
| 31 | No horizontal scroll at any breakpoint | | |
| 32 | Overview strip shows 2x2 grid on mobile | | |
| 33 | Experience section: image above copy on mobile | | |
| 34 | Includes grid is single column on mobile | | |
| 35 | Add-ons grid is single column on mobile | | |
| 36 | Reviews are single column stacked on mobile | | |
| 37 | All form fields are full width on mobile | | |
| 38 | Form inputs are 16px font (prevents iOS zoom) | | |
| 39 | Submit button is full width on mobile | | |
| 40 | Sticky CTA bar visible on mobile when user is above form | | |
| 41 | Sticky CTA bar hides when form section is in view | | |
| 42 | Adequate section spacing (not cramped) | | |
| 43 | Navigation works on mobile | | |

---

## SECTION 4: FORM QA

Test with a real submission to confirm end-to-end.

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 44 | All required fields show validation on empty submit | | |
| 45 | Email field validates email format | | |
| 46 | Guest count field enforces min 2 / max 13 | | |
| 47 | Date field is date picker (native) | | |
| 48 | Hidden field `experience` = "Golden Hour Escape" | | |
| 49 | Hidden field `source_url` is populated with full URL | | |
| 50 | Hidden field `page_slug` = "/experience/golden-hour-escape/" | | |
| 51 | UTM fields populated when URL has UTM params (test with ?utm_source=test) | | |
| 52 | Form submission fires webhook to Make SSS-LEAD-INTAKE | | |
| 53 | Success state shows after submission | | |
| 54 | Confirmation email received within 2 minutes | | |
| 55 | Email shows correct: Experience, Date, Guests, Occasion | | |
| 56 | Airtable Request record created in tblTlSB9CO4dTGodg | | |
| 57 | Airtable record: Status = NEW | | |
| 58 | Airtable record: Brand = SSS | | |
| 59 | Airtable record: Environment = Production | | |
| 60 | Airtable record: Experience = Golden Hour Escape | | |
| 61 | Slack alert fires to #sss-ops-alerts | | |
| 62 | Duplicate submission test: submit same email+date+guests twice, confirm only one record | | |

---

## SECTION 5: SEO QA

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 63 | Page title: "Golden Hour Escape | Private Sunset Sailing Charter | She Said Sail" (50-60 chars) | | |
| 64 | Meta description: 120-155 chars, emotion-first, includes "sunset sailing" | | |
| 65 | Canonical URL: https://shesaidsail.com/experience/golden-hour-escape/ | | |
| 66 | OG title set | | |
| 67 | OG description set | | |
| 68 | OG image set (1200x630px, under 200kb) | | |
| 69 | OG image alt text set | | |
| 70 | Twitter card meta set | | |
| 71 | Schema markup (Product/Offer) present and valid (test with Google Rich Results Test) | | |
| 72 | H1 contains "light" and page context naturally | | |
| 73 | All images have descriptive, keyword-aware alt text | | |
| 74 | No duplicate H1 tags | | |

---

## SECTION 6: ANALYTICS QA

Use GTM Preview Mode and GA4 DebugView for all checks.

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 75 | GTM container fires on page load | | |
| 76 | `sss_page_view` event fires with experience_name = "Golden Hour Escape" | | |
| 77 | `sss_cta_click` fires when hero CTA is clicked | | |
| 78 | `sss_cta_click` fires when sticky mobile CTA is clicked | | |
| 79 | `sss_form_start` fires on first form field interaction | | |
| 80 | `sss_form_submit` fires with guest_count and occasion values | | |
| 81 | `sss_scroll_depth_50` fires at 50% page scroll | | |
| 82 | `sss_scroll_depth_75` fires at 75% page scroll | | |
| 83 | `sss_section_view` fires for each major section | | |
| 84 | UTM params captured in dataLayer on page with UTM URL | | |
| 85 | All events visible in GA4 DebugView | | |

---

## SECTION 7: PERFORMANCE QA

Run Google PageSpeed Insights: https://pagespeed.web.dev/

| # | Check | Pass/Fail | Notes |
|---|-------|-----------|-------|
| 86 | Mobile PageSpeed score 80+ | | Score: ___ |
| 87 | Desktop PageSpeed score 90+ | | Score: ___ |
| 88 | LCP under 2.5s (mobile) | | Value: ___ |
| 89 | CLS under 0.1 | | Value: ___ |
| 90 | No render-blocking resources reported as critical | | |
| 91 | Hero image has `loading="eager"` | | |
| 92 | All below-fold images have `loading="lazy"` | | |
| 93 | Hero image under 400kb | | Size: ___ |

---

## SIGN-OFF

| Gate | Tester | Date | Pass/Fail |
|------|--------|------|-----------|
| Copy | | | |
| Visual | | | |
| Mobile | | | |
| Form end-to-end | | | |
| SEO | | | |
| Analytics | | | |
| Performance | | | |
| **Final sign-off: Will** | | | |

Page is PRODUCTION READY when all 7 gates pass and Will has signed off.
