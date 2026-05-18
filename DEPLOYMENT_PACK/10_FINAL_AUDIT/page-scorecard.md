# She Said Sail: Page Scorecard

Quick reference for the current state of each page and what still needs to be done.

Last updated: May 2026

| Page | Score | Status |
|---|---|---|
| Homepage | 9.4 / 10 | Frontend complete. Apply CSS, JS, and HTML snippets in Elementor. See `08_PAGE_INSTALL_GUIDES/homepage-install-guide.md`. |
| Request to Book | 8.5 / 10 | HTML snippets ready. Add hidden fields to MetForm. Wire form to Make.com webhook. Confirm /thank-you/ redirect. See `08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md`. |
| Experiences | 8 / 10 | Snippets ready. Apply hero support copy, social proof strip, and bottom CTA in Elementor. See `08_PAGE_INSTALL_GUIDES/experiences-install-guide.md`. |
| /thank-you/ | 7 / 10 | Thank you page snippet ready. Confirm the page exists at /thank-you/ in WordPress. Set it as the MetForm redirect URL after successful submission. |
| Mobile (all pages) | 9 / 10 | DevTools simulation passed. Run `09_QA/mobile-qa-checklist.md` on a real device before sign-off. Test on iPhone 14 (390px) and iPhone SE (375px). |
| Backend (Airtable + Make.com) | 2 / 10 | Schemas and scenario specs are complete. Build the Airtable base first, then create Make.com scenarios. See `05_AIRTABLE_BACKEND/` and `06_MAKE_WEBHOOKS/`. |
| Analytics (GTM + GA4 + Pixels) | 3 / 10 | Events coded in JS. Enter real Pixel IDs into GTM tags. Publish GTM container. Run `09_QA/tracking-qa-checklist.md`. |

---

## Reading the Scorecard

A score reflects the current state of that page or dimension as of this audit. It is not a quality judgment on the design. It reflects how much of the total implementation is complete and functional.

A page scoring 9/10 on frontend but 2/10 on backend means the visible experience is excellent, but the data infrastructure behind it is not yet operational.

The overall site readiness score is **7.1 / 10**. See `10_FINAL_AUDIT/final-site-readiness-audit.md` for the full breakdown.
