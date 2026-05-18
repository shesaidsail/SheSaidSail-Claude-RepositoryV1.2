# She Said Sail: Optimization Batch Plan
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul
**Reference:** docs/site-inventory/full-site-page-inventory.md

---

## ALREADY COMPLETE

| Page | URL | Deployment Files |
|---|---|---|
| Homepage | / | DEPLOYMENT_PACK/03_HTML_SNIPPETS/homepage/, 04_SEO_META/homepage-meta.html, 08_PAGE_INSTALL_GUIDES/homepage-install-guide.md |
| Request to Book | /request-to-book/ | DEPLOYMENT_PACK/03_HTML_SNIPPETS/request-to-book/, 04_SEO_META/request-to-book-meta.html, 08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md |
| Experiences | /experiences/ | DEPLOYMENT_PACK/03_HTML_SNIPPETS/experiences/, 04_SEO_META/experiences-meta.html, 08_PAGE_INSTALL_GUIDES/experiences-install-guide.md |
| Monaco Social | /experience/monaco-social/ | DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/ (6 files), 04_SEO_META/monaco-social-meta.html, 08_PAGE_INSTALL_GUIDES/monaco-social-install-guide.md, 09_QA/monaco-social-qa-checklist.md, docs/audits/monaco-social-audit-may-2026.md |

---

## BATCH 1: Experience Detail Pages

**Why batch 1:** These are the highest-revenue-adjacent pages. A visitor on an experience detail page has already passed through awareness and consideration. They are evaluating one specific experience. This is the closest point to the booking conversion event. Improving trust, clarity, and CTA quality here has direct, measurable impact on form submissions.

**Pages:**

| Page | URL | Slug | Occasion Target |
|---|---|---|---|
| Golden Hour Escape | /experience/golden-hour-escape/ | golden-hour-escape | Intimate groups, milestone celebrations, sunset hosting |
| Rose Day Club | /experience/rose-day-club/ | rose-day-club | Girls trips, social hosting, rosé and water |
| Pink Palm Club | /experience/pink-palm-club/ | pink-palm-club | Bachelorette groups, social groups, movement and music |

**Files to create per page:**

New consolidated structure under DEPLOYMENT_PACK/pages/[slug]/:

```
DEPLOYMENT_PACK/pages/[slug]/
  [slug]-html-snippets.html     Combined HTML for all 6 sections
  [slug]-metadata.html          SEO meta, OG, Twitter Card, JSON-LD
  [slug]-backend.md             Airtable mapping, hidden field spec, Make routing
  [slug]-analytics.md           GTM events, GA4 spec, pixel events
  [slug]-qa.md                  Pass/fail QA checklist
  [slug]-audit.md               Before/after scores across all 10 dimensions
```

Note: No page-specific CSS or JS files needed. These pages inherit all styles from DEPLOYMENT_PACK/01_GLOBAL_CSS/ and DEPLOYMENT_PACK/02_GLOBAL_JS/. Page-specific inline styles are scoped within the HTML snippets.

**Tracking events needed (per page):**

- view_experience_page (already in global JS, fires on all /experience/* paths)
- click_request_to_book (already in global JS, fires on any link to /request-to-book/)
- click_experience_card (already in global JS, from the Experiences index)
- scroll_50_percent, scroll_90_percent (already in global JS)

No new GTM events required. The existing view_experience_page event captures experience_slug automatically.

**Airtable fields needed:**

No new tables. existing Requests table already includes:
- Experience Interest (Multiple Select): options include all 4 experiences
- selected_experience captured via URL param on CTAs

The hidden field `selected_experience` pre-populates Experience Interest via Make.com Router.

**Make scenarios touched:**

No new scenarios needed. Existing M-BRAND-ROUTER routes on selected_experience. CTA links include ?selected_experience=[slug] which passes through populateHiddenFields() into the form payload.

**Estimated implementation complexity:** Low. These three pages are structurally identical to Monaco Social. The HTML snippet pattern, SEO meta pattern, QA checklist pattern, and audit format are all established.

---

## BATCH 2: Conversion Support Pages

**Why batch 2:** These pages directly support the booking conversion or post-booking relationship. The thank-you page fires the view_thank_you_page event that triggers retargeting suppression. The about page builds trust that closes undecided visitors. The contact page handles non-booking inquiries that could become bookings.

**Pages:**

| Page | URL | Slug | Page Type |
|---|---|---|---|
| Thank You | /thank-you/ | thank-you | Post-conversion confirmation |
| About | /about/ | about | Brand trust and story |
| Contact | /contact/ | contact | Direct inquiry |

**Files to create per page:**

```
DEPLOYMENT_PACK/pages/[slug]/
  [slug]-html-snippets.html
  [slug]-metadata.html
  [slug]-backend.md             (minimal for thank-you, moderate for contact)
  [slug]-analytics.md
  [slug]-qa.md
  [slug]-audit.md
```

**Tracking events needed:**

- Thank You: view_thank_you_page (already in global JS)
- About: view_about_page (new event, simple path check)
- Contact: view_contact_page, submit_contact_form (new events)

**Airtable fields needed:**

Contact page only: if a contact form exists, route to Requests table with source_type = "contact_form" or create a lightweight Contact Inquiry record type within the existing Requests table using a Type field.

**Make scenarios touched:**

Contact form: extend M-BRAND-ROUTER to handle contact form submissions. Route to Requests with Request Type = "General Inquiry". No new scenario needed if the existing webhook payload supports a type field.

**Estimated implementation complexity:** Low to medium. Thank-you and About are HTML/copy only. Contact may require a light form integration.

---

## BATCH 3: Trust and FAQ Pages

**Why batch 3:** FAQ has strong SEO value for long-tail discovery queries (e.g., "how much does a private yacht cost in Miami", "what to wear on a yacht bachelorette"). These pages also reduce pre-purchase friction for visitors who are close to booking but have unanswered questions.

**Pages:**

| Page | URL | Slug | Page Type |
|---|---|---|---|
| FAQ | /faq/ | faq | Pre-purchase friction removal + SEO |
| Blog / Journal | /journal/ or /blog/ | journal | Editorial SEO |

**Files to create per page:**

Same DEPLOYMENT_PACK/pages/[slug]/ structure.

**Tracking events needed:**

- FAQ: view_faq_page, click_faq_item (accordion expand events)
- Journal: view_journal_page, click_article (if article list exists)

**Airtable fields needed:** None.

**Make scenarios touched:** None.

**Estimated implementation complexity:** Low for FAQ (copy and structure). Medium for journal (depends on whether content exists and how it is structured in WordPress).

---

## BATCH 4: Legal and Compliance Pages

**Why batch 4:** These pages require minimal optimization. They need correct meta tags (typically noindex), clear formatting, and a consistent header/footer. No conversion work needed.

**Pages:**

| Page | URL | Slug | Page Type |
|---|---|---|---|
| Terms of Service | /terms/ or /terms-of-service/ | terms | Legal |
| Privacy Policy | /privacy/ or /privacy-policy/ | privacy | Legal / GDPR |

**Files to create per page:**

```
DEPLOYMENT_PACK/pages/[slug]/
  [slug]-metadata.html          noindex meta, minimal OG
  [slug]-qa.md                  Simple 5-item checklist
```

No HTML snippets, no backend docs, no analytics docs needed for legal pages.

**Estimated implementation complexity:** Very low. Meta only.

---

## IMPLEMENTATION ORDER WITHIN EACH BATCH

Within each batch, pages should be created in parallel where possible (they are structurally independent). Commit them as a group once all files in the batch are complete.

```
Batch 1: golden-hour-escape + rose-day-club + pink-palm-club (parallel)
Batch 2: thank-you + about + contact (parallel)
Batch 3: faq + journal (parallel)
Batch 4: terms + privacy (parallel)
```

---

## FILE COUNT PROJECTION

| Batch | Pages | Files per Page | Total Files |
|---|---|---|---|
| 1 | 3 | 6 | 18 |
| 2 | 3 | 6 | 18 |
| 3 | 2 | 5 | 10 |
| 4 | 2 | 2 | 4 |
| **Total** | **10** | | **50** |

---

## READINESS GATE BETWEEN BATCHES

Do not begin a new batch until:

1. All files for the current batch are committed to feature/luxury-conversion-overhaul
2. The experience-pages-qa-addendum.md passes for all pages in the batch
3. No em dashes found in any batch file (grep -rn scan before commit)
4. Founder review completed for Batch 1 before Batch 2 begins (recommended)
