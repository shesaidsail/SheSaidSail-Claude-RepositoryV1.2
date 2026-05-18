# Request Page QA Checklist
She Said Sail | v2.0

---

## Form Functionality

- [ ] Occasion cards select one at a time, selection persists visually
- [ ] Experience cards select one at a time, hidden input updates on selection
- [ ] Date field enforces minimum date of today
- [ ] Guest count field rejects non-numeric input
- [ ] Email field validates format before submission
- [ ] All required fields show inline error messages on failed submission
- [ ] Errors scroll into view on mobile
- [ ] Form submit triggers loading state on button
- [ ] Thank-you state appears after submission
- [ ] Form is hidden after thank-you state shows
- [ ] Sticky CTA is hidden after thank-you state shows
- [ ] Thank-you social links open in new tab

---

## Hidden Fields

- [ ] `utm_source` populated from URL parameter on paid traffic test
- [ ] `utm_medium` populated correctly
- [ ] `utm_campaign` populated correctly
- [ ] `landing_page` persists across internal navigation (sessionStorage test)
- [ ] `source_url` reflects current page URL
- [ ] `referrer_url` captures referrer from an external link test
- [ ] `first_seen_at` stores in localStorage on first visit, persists on repeat visits
- [ ] `brand` value is always "she-said-sail"
- [ ] `service_category` value is always "private-yacht-charter"
- [ ] `form_version` value is "rtb-overhaul-v2"

---

## Analytics Events

- [ ] `view_request_page` fires on page load (verify in GTM Preview)
- [ ] `start_booking_form` fires on first field focus
- [ ] `start_booking_form` fires only once per session
- [ ] `field_completion_progress` increments correctly per field
- [ ] `select_occasion` fires on each occasion card click
- [ ] `select_experience_type` fires on each experience card click
- [ ] `click_request_cta` fires on button mousedown
- [ ] `submit_booking_form` fires on valid submission
- [ ] `view_thank_you_page` fires after thank-you state shows
- [ ] `form_submission_error` fires if webhook fails (test by temporarily blocking URL)
- [ ] Meta Pixel `Lead` fires on submission (requires Pixel loaded)
- [ ] TikTok `SubmitForm` fires on submission (requires TikTok Pixel loaded)

---

## Mobile UX (iPhone testing)

- [ ] All input heights are at least 52px (comfortable thumb tap)
- [ ] Occasion cards are readable at 2-column grid on small screens
- [ ] Experience cards stack to 1 column on screens under 480px
- [ ] Email input triggers email keyboard (`inputmode="email"`)
- [ ] Phone input triggers numeric keyboard (`inputmode="tel"`)
- [ ] Guest count triggers numeric keyboard (`inputmode="numeric"`)
- [ ] Date input uses native date picker on mobile
- [ ] Sticky CTA is visible in mobile viewport
- [ ] Sticky CTA hides when form is submitted
- [ ] Safe area inset bottom applied to sticky CTA
- [ ] Fonts are readable without zooming (minimum 15px on inputs)
- [ ] Labels are spaced away from inputs (7px gap)
- [ ] Step headers provide visible navigation landmarks

---

## Accessibility

- [ ] All form inputs have associated `<label>` elements
- [ ] All required fields have `aria-required="true"`
- [ ] Occasion cards use `aria-pressed` attribute
- [ ] Experience cards use `aria-pressed` attribute
- [ ] Trust bar uses `role="complementary"` and `aria-label`
- [ ] Thank-you state uses `aria-live="polite"`
- [ ] Sticky CTA uses `aria-hidden` management on scroll
- [ ] Hero has `aria-labelledby` pointing to `<h1>`
- [ ] Color contrast passes WCAG AA on all body text
- [ ] Focus states are visible on all interactive elements

---

## SEO + Technical

- [ ] Page title: "Request Your Experience | She Said Sail"
- [ ] Meta description present and under 160 characters
- [ ] Canonical tag present
- [ ] OG tags present (title, description, url, image, type)
- [ ] Twitter card tags present
- [ ] Structured data (LD+JSON WebPage schema) valid via schema.org validator
- [ ] No duplicate IDs on page
- [ ] GTM container fires correctly
- [ ] No console errors on load

---

## Webhook Integration

- [ ] Form data posts to Make.com webhook endpoint
- [ ] Webhook receives all required fields including UTMs
- [ ] Graceful fallback: thank-you state shows even if webhook fails
- [ ] Error is logged to dataLayer on failure
- [ ] Webhook URL is environment-variable controlled (not hardcoded in production)

---

## Cross-Browser

- [ ] Chrome (latest)
- [ ] Safari (latest) including iOS Safari
- [ ] Firefox (latest)
- [ ] Samsung Internet (optional but recommended)
