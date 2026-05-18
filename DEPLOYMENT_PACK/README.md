# SHE SAID SAIL
# DEPLOYMENT PACK

STATUS: PRODUCTION
VERSION: v1.0
EFFECTIVE DATE: May 2026
OWNER: Will Hunt

---

## WHAT THIS IS

The Deployment Pack contains all implementation-ready files for each optimized page on SheSaidSail.com.

Every page folder contains:
- CSS: Design system styles scoped to that page
- JS: Analytics, attribution, form handling, and UX enhancement
- HTML snippets: Copy-paste ready sections for Webflow
- Metadata: SEO tags, Open Graph, structured data
- Backend spec: Form-to-Airtable mapping and Make dependencies
- Analytics spec: GTM events, GA4 setup, pixel configuration
- QA checklist: Verification steps before launch
- Audit: Pre and post-optimization scoring

---

## MASTER STANDARDS

All pages are built against the master standards in /docs/system/:

| File | Purpose |
|------|---------|
| master-design-system.md | Colors, typography, spacing, components |
| master-copy-system.md | Voice, tone, prohibited words, copy patterns |
| master-page-structure.md | Section order, layout rules, URL conventions |
| master-mobile-ux.md | Mobile breakpoints, touch targets, spacing |
| master-backend-system.md | Form fields, webhook mapping, Airtable fields |
| master-qa-system.md | QA checklist, failure categories, sign-off |
| master-performance-standard.md | Core Web Vitals targets, image standards |
| master-visual-direction.md | Photography direction, color usage, layout principles |
| master-audit-scorecard.md | 12-dimension scoring system |

---

## PAGE INDEX

| Page | Status | Overall Score | Folder |
|------|--------|--------------|--------|
| Pink Palm Club | Ready for implementation | 9.1/10 projected | /pink-palm-club/ |

---

## HOW TO IMPLEMENT A PAGE

1. Open the page folder in /DEPLOYMENT_PACK/[page-name]/
2. Read the audit doc first to understand what changed and why
3. Read the backend doc to understand form dependencies
4. In Webflow:
   a. Add CSS file contents to Page Settings > Custom Code > Head
   b. Add HTML snippets to the correct page sections
   c. Set form action URL to the Make webhook URL
   d. Set page title and meta description from metadata file
   e. Add all head tags from metadata file to Custom Code > Head
   f. Add JS file contents to Custom Code > Body (before closing tag)
5. Run the QA checklist from the QA doc
6. Submit a live test form and verify end-to-end
7. Run PageSpeed Insights on the live page

---

## IMPLEMENTATION NOTES

- Never put the Make webhook URL in the CSS or JS files. Set it in Webflow form settings only.
- Always test on a real mobile device, not just browser DevTools.
- The JS file must load after the HTML content. Always place in the body before the closing tag.
- UTM parameters are stored in sessionStorage, so they survive single-page-style navigation but not cross-session visits.
- The form's idempotency key prevents duplicate records. If testing, use a different email/date/guest combination each time, or clean up test records in Airtable after QA.

---

## BRANCH

All Deployment Pack files are committed on feature/luxury-conversion-overhaul.
Do not merge to staging or main without Will's approval.
