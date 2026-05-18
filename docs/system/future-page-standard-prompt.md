# She Said Sail: Future Page Standard Prompt

**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul
**Last Updated:** 2026-05-18

---

## 1. PURPOSE

This document contains the reusable prompt for optimizing any future page on the She Said Sail website. The prompt automatically references the correct design system, copy system, deployment pack, and QA standards established across the overhaul project.

Every future page optimization starts with this prompt. It eliminates setup time, prevents drift from the master standard, and ensures every page produced in a new session is consistent with the pages already built.

---

## 2. HOW TO USE

1. Copy the full prompt template from Section 3 below
2. Fill in every `[BRACKETED]` field with the specifics for this page
3. Paste the completed prompt into a new Claude Code session
4. The system will apply all master standards automatically

Do not skip bracketed fields. Incomplete context produces inconsistent output.

---

## 3. THE PROMPT TEMPLATE

```
You are working on the She Said Sail website. She Said Sail is a luxury yacht charter company in Miami, FL. Target audience: women-led group celebrations (bachelorette, birthday, girls trip, relationship celebration). Starting from $10,000.

MASTER STANDARD LOCATION: This repository contains the complete master website standard in docs/system/. Apply all standards from that folder to this optimization.

DEPLOYMENT PACK LOCATION: DEPLOYMENT_PACK/ contains all production CSS, JS, HTML snippets, SEO meta files, and implementation guides. Reuse everything that applies. Do not reinvent components or patterns that already exist.

CRITICAL RULE: Never use em dashes anywhere. Not in copy, code, comments, commit messages, documentation, or metadata. Use colons, commas, or plain sentences instead.

ACTIVE BRANCH: feature/luxury-conversion-overhaul

PAGE TO OPTIMIZE: [PAGE NAME AND URL]

CURRENT STATE: [Brief description of what the page currently does and looks like. Include approximate word count, what sections exist, and any known issues.]

PAGE PURPOSE: [Conversion / Information / Trust / SEO / Other]

TARGET AUDIENCE ON THIS PAGE: [Which segment: bachelorette, birthday, girls trip, all segments, or other. Be specific.]

OPTIMIZATION GOALS:
1. Score this page using docs/system/master-audit-scorecard.md before making any changes. Record the baseline score.
2. Apply docs/system/master-page-template.md steps 1 through 15 in order.
3. Use docs/system/master-design-system.md for all visual decisions.
4. Use docs/system/master-copy-system.md for all copy decisions.
5. Use docs/system/master-mobile-ux.md for all mobile decisions.
6. Reference DEPLOYMENT_PACK/ for all reusable components before creating anything new.
7. Add any new HTML snippets to DEPLOYMENT_PACK/03_HTML_SNIPPETS/[page-name]/.
8. Add SEO meta tags to DEPLOYMENT_PACK/04_SEO_META/[page-name]-meta.html.
9. Update DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/ with a complete install guide for this page.
10. Create a QA checklist in DEPLOYMENT_PACK/09_QA/[page-name]-qa-checklist.md.
11. Create a final audit in docs/audits/[page-name]-final-audit.md with before and after scores.
12. Commit changes in logical groups with descriptive commit messages (no em dashes in any message).
13. Push all commits to feature/luxury-conversion-overhaul.

ADDITIONAL CONTEXT: [Paste the current page HTML here, or list specific known issues, or describe what the page currently achieves and what is missing.]

When complete, report:
- Audit scores (before and after, dimension by dimension)
- Files created (with full paths)
- Files modified (with full paths and a summary of what changed)
- Next recommended action
```

---

## 4. DESIGN CONSISTENCY CHECKLIST

The following standards are enforced automatically when this prompt is used. They are listed here for reference and manual verification.

**Colors (from `docs/system/master-design-system.md`):**
- `--sss-navy: #1A2332` for primary backgrounds and headings
- `--sss-gold: #DAB97E` for primary CTA buttons and accent elements
- `--sss-gold-deep: #C9A96E` for hover states on gold elements
- `--sss-cream: #FAF8F3` for light section backgrounds
- `--sss-warm: #F5F0E8` for warm section backgrounds and alternating sections

**Typography:**
- Follow the type scale exactly as defined in `master-design-system.md`
- No custom font sizes outside the defined scale
- Cormorant Garamond for headings; correct weights as specified

**Spacing:**
- 96px section padding on desktop
- 64px section padding on mobile
- 8px base unit; all spacing is a multiple of 8px

**Buttons (4-level hierarchy):**
1. Primary: gold fill, navy text, used once per section
2. Secondary: navy fill, cream text
3. Ghost: transparent, cream or navy border
4. Text: no border, no fill, underline on hover

**Cards:**
- Border radius: 8px
- Shadow values as defined in the design system
- Hover: lift with shadow increase, smooth transition

**Social proof:**
- Editorial quote card format (no star ratings as primary element)
- Full attribution: first name, occasion type, experience name

**CTAs:**
- Primary destination is always `/request-to-book/`
- No "Book Now" language; use the established CTA copy from `master-copy-system.md`

---

## 5. BACKEND CONSISTENCY CHECKLIST

The following rules are applied automatically. Listed here for reference and manual QA.

**Hidden fields:** Use the exact 13 field names from `docs/system/master-backend-system.md Section 3`. No variations or abbreviations.

**UTM capture:** Reuse the `captureUtm()` function from `she-said-sail-global.js`. Do not write a new UTM capture function.

**Hidden field population:** Reuse the `populateHiddenFields()` function from `she-said-sail-global.js`. Do not write new inline population logic.

**Make.com:** Use existing scenarios if the form type matches an existing scenario (booking inquiry, email capture). Create new scenarios only for interaction types that have no existing scenario equivalent. Follow the `M-[FUNCTION]-[NUMBER]` naming convention.

**Airtable:** Use existing tables unless the data type is fundamentally different. A supplier contact form, a press inquiry form, and a gift inquiry with booking intent each have different routing. Verify the correct table before mapping.

---

## 6. ANALYTICS CONSISTENCY CHECKLIST

The following event standards are applied automatically. Listed here for reference and GTM verification.

**Page view event:** `view_[pagename]` pushed to dataLayer on every page load.

**CTA click events:** `click_[action]` for every primary and secondary CTA on the page.

**Form events:**
- `start_[form_name]_form` on first interaction with any form field
- `submit_[form_name]_form` on successful form submission

**Naming rules for new events:**
- New page views: `view_[page_name]` (e.g. `view_about_page`)
- New CTA clicks: `click_[element_name]` (e.g. `click_share_button`)
- New content interactions: `view_[content_type]` or `click_[content_type]`
- All event names are snake_case, lowercase, no hyphens

**Data Layer Variable names:** All custom GTM DLVs use the prefix `dlv_` (e.g. `dlv_experience_name`, `dlv_occasion`).

---

## 7. PAGES ALREADY OPTIMIZED

Do not re-optimize these pages. Reference them for consistency checks when building new pages.

| Page | URL | Notes |
|---|---|---|
| Homepage | / | Primary brand statement, email capture, social proof |
| Request to Book | /request-to-book/ | Full form with 13 hidden fields, concierge block, noindex |
| Experiences | /experiences/ | Experience card grid, occasion filtering, editorial copy |

When a new page shares a component with these pages (testimonials, email capture, footer, CTA style), pull from the existing implementation in `DEPLOYMENT_PACK/03_HTML_SNIPPETS/` rather than rebuilding.

---

## 8. RECOMMENDED NEXT PAGES TO OPTIMIZE

Listed in priority order based on conversion value, SEO potential, and audience volume.

| Priority | Page | URL Pattern | Reason |
|---|---|---|---|
| 1 | Individual experience pages | /experiences/[name]/ | High conversion value; the specific experience page is often the decision point |
| 2 | About page | /about/ | Trust-building; consistently one of the top 3 visited pages for any service brand |
| 3 | Blog or editorial section | /journal/ or /blog/ | SEO value; brand voice expression; long-term organic traffic compound |
| 4 | Contact page | /contact/ | Frequently visited on mobile; simple to improve; impacts trust directly |
| 5 | FAQ page | /faq/ | Reduces pre-purchase friction; strong SEO; often feeds organic discovery |
| 6 | Occasions landing pages | /bachelorette/, /birthday/ | Direct paid ad destinations for bachelorette and birthday campaigns; high ROI |

When starting a new optimization, begin with Priority 1. Individual experience pages are the closest touchpoint to conversion and benefit immediately from the established design system and copy system.
