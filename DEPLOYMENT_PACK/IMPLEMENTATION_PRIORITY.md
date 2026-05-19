# Implementation Priority Plan

**Date:** May 2026
**System:** She Said Sail website deployment
**Goal:** Staging-ready as quickly as possible

Estimated total time: 22 to 27 hours across 3 to 4 working days.

---

## Who does what

| Role | Person | Scope |
|---|---|---|
| Web Builder (Kelsey) | Kelsey | WordPress, Elementor, CSS/JS install, SEO meta, forms |
| Backend Developer | Will or contractor | Airtable, Make.com, webhook wiring |
| Founder review | Will | Page-by-page visual approval before each page is published |

Kelsey can complete Phase 1 independently. Phase 2 (backend) can run in parallel with Phase 1 or immediately after. Will approves each page before it moves to production.

---

## Phase 1: Staging Install (Web Builder)

**Estimated time:** 12 to 15 hours
**Prerequisite:** Staging environment is live, Elementor Pro is installed and active, all plugins from `WORDPRESS_QUICK_INSTALL.md` are active

Complete in this order. Each step depends on the previous one.

### Step 1.1: Global files (1 hour)

| Action | File | Time |
|---|---|---|
| Add CSS to Additional CSS | `01_GLOBAL_CSS/she-said-sail-global.css` | 10 min |
| Add global JS to Insert Headers and Footers footer | `02_GLOBAL_JS/she-said-sail-global.js` | 10 min |
| Add GTM head snippet to Insert Headers and Footers header | See `WORDPRESS_QUICK_INSTALL.md` Section 1 | 5 min |
| Add GTM noscript to Insert Headers and Footers body | See `WORDPRESS_QUICK_INSTALL.md` Section 2 | 5 min |
| Add chatbot JS to Insert Headers and Footers footer | `chatbot/chatbot-js.js` | 10 min |

Verify: reload the homepage in a browser. Styles should apply. Open DevTools console: no JS errors. GTM Preview should show the container loading.

### Step 1.2: Homepage (2 hours)

| Action | File | Time |
|---|---|---|
| Add social proof strip | `03_HTML_SNIPPETS/homepage/social-proof-strip.html` | 15 min |
| Add hero occasion pills | `03_HTML_SNIPPETS/homepage/hero-occasion-pills.html` | 15 min |
| Add email capture section | `03_HTML_SNIPPETS/homepage/email-capture-section.html` | 15 min |
| Add homepage SEO meta (via Yoast) | `04_SEO_META/homepage-meta.html` | 10 min |
| Copy edits in Elementor | `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md` Step 7 | 30 min |

Verify: complete `09_QA/master-qa-checklist.md` homepage section before moving on.

### Step 1.3: Request to Book page (1.5 hours)

| Action | File | Time |
|---|---|---|
| Add concierge reassurance block | `03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html` | 10 min |
| Add form intro | `03_HTML_SNIPPETS/request-to-book/request-form-intro.html` | 5 min |
| Add trust note under form | `03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html` | 5 min |
| Add SEO meta (via Yoast) | `04_SEO_META/request-to-book-meta.html` | 10 min |
| Add hidden fields to form | `05_AIRTABLE_BACKEND/request-form-hidden-fields.md` | 20 min |

Verify: submit the form with test data. Check DevTools console: no errors. (Airtable verification happens in Phase 2.)

### Step 1.4: Experiences page (1.5 hours)

| Action | File | Time |
|---|---|---|
| Add hero support copy | `03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html` | 10 min |
| Add experience card content | `03_HTML_SNIPPETS/experiences/experience-card-content.html` | 15 min |
| Add social proof strip | `03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html` | 15 min |
| Add bottom CTA | `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html` | 10 min |
| Add SEO meta (via Yoast) | `04_SEO_META/experiences-meta.html` | 10 min |

### Step 1.5: Monaco Social experience page (2 hours)

| Action | File | Time |
|---|---|---|
| Add hero support | `03_HTML_SNIPPETS/monaco-social/hero-support.html` | 10 min |
| Add social proof | `03_HTML_SNIPPETS/monaco-social/social-proof.html` | 10 min |
| Review all 6 Monaco Social snippet files | `03_HTML_SNIPPETS/monaco-social/` | 45 min |
| Follow full page install guide | `08_PAGE_INSTALL_GUIDES/monaco-social-install-guide.md` | 30 min |

### Step 1.6: Remaining experience pages (2 hours)

Apply HTML snippets for:
- Golden Hour Escape: `pages/golden-hour-escape/`
- Rose Day Club: `pages/rose-day-club/`
- Pink Palm Club: `pages/pink-palm-club/`

Follow the same pattern as Monaco Social. Each page has its own HTML snippet file.

### Step 1.7: Secondary pages (2 hours)

Apply HTML snippets for:
- About: `pages/about/about-html-snippets.html` (4 sections)
- Contact: `pages/contact/contact-html-snippets.html`
- FAQ: `pages/faq/faq-html-snippets.html`
- Thank You: `pages/thank-you/thank-you-html-snippets.html`
- Journal: `pages/journal/journal-html-snippets.html`

Add Yoast SEO meta for each page (title, description, OG image).

### Step 1.8: Founder review checkpoint

Before moving to Phase 2, Will reviews each page:
- Desktop and mobile screenshots
- Navigation between pages
- Form visibility and fields
- No broken sections, missing styles, or placeholder text

Kelsey sends screenshots. Will approves or flags issues. Issues are resolved before Phase 2 begins.

---

## Phase 2: Backend and Tracking (Backend Developer)

**Estimated time:** 6 to 8 hours
**Can run in parallel with Phase 1 Steps 1.5 to 1.8**

### Step 2.1: Airtable base setup (2 to 3 hours)

| Action | Reference | Time |
|---|---|---|
| Create She Said Sail Airtable base | `05_AIRTABLE_BACKEND/airtable-table-schema.md` | 15 min |
| Build all 7 core tables with correct field types | Same file | 90 min |
| Build 6 intelligence tables (can do post-launch) | Same file | 60 min |
| Verify field names match exactly (see hidden field map) | `05_AIRTABLE_BACKEND/airtable-field-map.md` | 15 min |

Note: Field names in Airtable must match exactly what the Make.com blueprints and JS hidden fields expect. Mismatches cause silent data loss.

### Step 2.2: Make.com scenarios (2 to 3 hours)

The 8 Phase 1 scenarios are already complete. Only 1 scenario needs to be built.

| Scenario | Action | Reference | Time |
|---|---|---|---|
| M-CHATBOT-001 | Import blueprint and wire connections | `06_MAKE_BLUEPRINTS/M-CHATBOT-001-setup-guide.md` | 30 min |
| All 8 Phase 1 scenarios | Wire real Airtable base ID into each scenario | Each scenario's settings | 30 min |

After building M-CHATBOT-001:
1. Copy the webhook URL
2. Replace `WIRE_THIS_CHATBOT_WEBHOOK_URL` in the deployed chatbot JS (Insert Headers and Footers)

### Step 2.3: Webhook URL wiring (30 min)

| Placeholder | Where to replace | Webhook URL from |
|---|---|---|
| `WIRE_THIS_REQUEST_FORM_WEBHOOK_URL` | Insert Headers and Footers footer (global JS block) | M-WEBFORM-REQUEST-CAPTURE scenario |
| `WIRE_THIS_CHATBOT_WEBHOOK_URL` | Insert Headers and Footers footer (chatbot JS block) | M-CHATBOT-001 scenario |
| Email capture URL (commented out) | Same global JS block | M-EMAIL-CAPTURE scenario |

### Step 2.4: GTM import and publish (30 min)

| Action | Reference | Time |
|---|---|---|
| Import gtm-container-import.json | `07_GTM_ANALYTICS/gtm-import-instructions.md` | 10 min |
| Replace placeholder IDs (GA4, Meta, TikTok) | Same guide, Step 3 | 10 min |
| Preview and verify key events | Same guide, Step 4 | 10 min |
| Publish | Same guide, Step 5 | 5 min |

---

## Phase 3: QA (All)

**Estimated time:** 3 to 4 hours
**Prerequisite:** Phase 1 and Phase 2 complete

### Step 3.1: Backend verification (1 hour)

Submit a test form and complete a test chatbot conversation. Verify:
- [ ] Airtable: Request record created in Requests table
- [ ] Airtable: Contact record created in Contacts table
- [ ] Airtable: UTM record created and linked
- [ ] Airtable: Chatbot Conversations record created (for chatbot test)
- [ ] Slack: #new-leads alert received
- [ ] Email: confirmation email received at the test address

### Step 3.2: Analytics verification (1 hour)

Use GTM Preview mode and GA4 DebugView to verify:
- [ ] GA4 Configuration tag fires on every page
- [ ] `view_homepage` fires on homepage load
- [ ] `click_request_to_book` fires when CTA is clicked
- [ ] `submit_booking_form` fires on successful form submit
- [ ] `chatbot_open` fires when widget is clicked
- [ ] `chatbot_handoff` fires when chatbot conversation completes

### Step 3.3: Full QA checklists (1 to 2 hours)

Complete all checklists in `09_QA/`:
- `master-qa-checklist.md`
- `mobile-qa-checklist.md`
- `form-qa-checklist.md`
- `backend-qa-checklist.md`
- `tracking-qa-checklist.md`

See also `STAGING_QA_CHECKLIST.md` for the condensed go/no-go pass/fail version.

---

## Phase 4: Production Launch

**Estimated time:** 1 to 2 hours
**Prerequisite:** Phase 3 complete, Will approves go-live

### Step 4.1: Pre-launch final check

- [ ] All `09_QA/` checklists are complete with no open issues
- [ ] `STAGING_QA_CHECKLIST.md` shows all items passing
- [ ] Will has reviewed and approved every page on staging
- [ ] Real webhook URLs are wired (not placeholders)
- [ ] GTM is published (not just saved)
- [ ] Airtable base has no test records that should be cleared

### Step 4.2: Launch

1. Point production domain to the staging environment (or push staging to production, depending on hosting setup)
2. Clear any caching plugins
3. Confirm HTTPS is active
4. Submit one real test form on the production domain and verify Airtable and email

### Step 4.3: Post-launch (first 48 hours)

- Monitor Airtable for incoming requests
- Monitor Slack #new-leads for alerts
- Check GA4 Realtime view for active users
- Confirm chatbot fires webhook on completion

---

## Time Summary

| Phase | Who | Estimated Time |
|---|---|---|
| Phase 1: Staging Install | Kelsey | 12 to 15 hours |
| Phase 2: Backend and Tracking | Backend developer | 6 to 8 hours |
| Phase 3: QA | Kelsey + backend developer | 3 to 4 hours |
| Phase 4: Launch | Will + Kelsey | 1 to 2 hours |
| **Total** | | **22 to 29 hours** |

Phase 1 and Phase 2 can overlap after Step 1.4, reducing total clock time to approximately 3 to 4 working days.
