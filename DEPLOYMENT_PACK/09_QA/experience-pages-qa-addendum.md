# She Said Sail: Experience Pages QA Addendum

**Version:** 1.0
**Applies to:** All individual She Said Sail experience pages
**Scope:** Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, and any future experience pages added to the site

This addendum supplements the master QA checklist. It defines the minimum requirements that every experience page must meet, and the consistency standards that must hold across all experience pages together. Run this addendum alongside each experience-specific QA checklist.

---

## WHAT EVERY EXPERIENCE PAGE MUST HAVE

The following elements are required on every individual experience page. If any item is missing, the page is not ready to go live.

**Structure and content:**
- [ ] Experience name as H1 (single occurrence; must appear exactly once in the page source)
- [ ] Tagline as italic subheadline directly below or near the H1
- [ ] Quick facts strip showing duration, guest count, and starting price
- [ ] Occasion pills or an occasion positioning section identifying who the experience is for
- [ ] Descriptive copy in She Said Sail brand voice explaining what the experience is and who it is for
- [ ] A "What is included" list covering the key elements of the experience
- [ ] At least 1 testimonial that is specific to this experience or clearly attributed to a guest of this experience
- [ ] Pre-CTA reassurance block (the 3-step or process block that reduces friction before the CTA)
- [ ] Bottom CTA section linking to `/request-to-book/?selected_experience=[slug]`

**SEO and technical:**
- [ ] SEO meta description that mentions the experience name and at least one occasion type
- [ ] JSON-LD Service schema specific to this experience (name, description, price, provider)
- [ ] Canonical URL pointing to the specific experience page (not the /experiences/ parent page)
- [ ] og:image is a real, uploaded image (not a placeholder URL)
- [ ] og:image dimensions are 1200x630px

**Mobile:**
- [ ] Mobile layout verified at 375px viewport (iPhone SE)
- [ ] Mobile layout verified at 390px viewport (iPhone 14)
- [ ] All CTA buttons are full-width at mobile viewports

**Backend:**
- [ ] The `selected_experience` URL param passes correctly to the request-to-book form
- [ ] Confirm by visiting `/request-to-book/?selected_experience=[slug]` and inspecting the hidden field value in the DOM

---

## WHAT EACH EXPERIENCE PAGE MUST NOT HAVE

The following are disqualifying issues. Each item must be confirmed absent before sign-off.

**Content quality:**
- [ ] No duplicate content: the experience page must go deeper than any generic copy already on the homepage or /experiences/ page. It must not simply repeat the same sentences.
- [ ] No generic yacht charter language that is not specific to this experience. Copy about "the Miami skyline" or "the open water" must be tied to the specific experience, not floating generic filler.
- [ ] No CTAs that link to `/experiences/` instead of `/request-to-book/`. CTAs should always move the user toward booking, not back to the experience index.
- [ ] The word "package" does not appear anywhere on the page (use "experience" instead)

**CTAs:**
- [ ] No CTA uses the text "Book Now"
- [ ] No CTA uses the text "Submit"
- [ ] No CTA uses the text "Inquire Now"

**Brand violations:**
- [ ] No em dashes anywhere on the page
- [ ] The word "VIP" does not appear
- [ ] The phrase "party boat" does not appear
- [ ] The phrase "luxury rental" does not appear
- [ ] The word "exclusive" does not appear

---

## CONSISTENCY CHECK ACROSS ALL EXPERIENCE PAGES

These checks are performed when two or more experience pages are live. They ensure visual and functional consistency across the experience page family. Run this section whenever a new experience page is published or an existing one is updated.

**Snippet structure:**
- [ ] All live experience pages use the same 6-section snippet structure: hero-support, experience-description, social-proof, occasion-fit, pre-cta-reassurance, bottom-cta
- [ ] If a new experience page deviates from the 6-section structure, this is documented and approved before launch

**Design and typography:**
- [ ] All experience pages use the same typography scale and spacing system as defined in the global CSS
- [ ] Section backgrounds follow the same pattern across experience pages (cream, white, navy, cream, white, navy) unless a deliberate deviation is approved
- [ ] CTA button styles are consistent across all experience pages (gold fill, navy text, same border radius and padding)

**URL and form patterns:**
- [ ] All experience page CTAs use the `?selected_experience=[slug]` URL pattern
- [ ] The slug used in the URL param matches the slug used in the form submission data for that experience
- [ ] Slugs are lowercase, hyphenated, and match the URL structure: `monaco-social`, `golden-hour-escape`, `rose-day-club`, `pink-palm-club`

**Testimonials:**
- [ ] Each experience page has at least 1 testimonial that is not recycled from the homepage
- [ ] No two experience pages use the exact same testimonial text
- [ ] All testimonials have attribution (at minimum a first name and occasion type, or a date)

**SEO:**
- [ ] No two experience pages share the same meta description
- [ ] No two experience pages share the same og:title
- [ ] Each experience page has a unique JSON-LD schema referencing its own name, description, and URL
- [ ] Canonical URLs are unique per page and do not point to the same destination

**Analytics:**
- [ ] Each experience page fires a unique GTM page view event: `view_monaco_social`, `view_golden_hour_escape`, `view_rose_day_club`, `view_pink_palm_club`
- [ ] No two experience pages fire the same GTM page view event name
- [ ] All experience pages fire `click_request_to_book` when the hero CTA or bottom CTA is clicked (handled by global JS)
