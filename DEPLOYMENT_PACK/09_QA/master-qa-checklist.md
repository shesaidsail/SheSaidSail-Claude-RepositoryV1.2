# She Said Sail: Master QA Checklist

High-level launch readiness checklist. For detailed verification of each area, refer to the linked specialist checklists. Complete this checklist last, after all specialist checklists are signed off.

Reviewer: _____________________ Date: _____________________

| # | Check | Pass | Fail | N/A | Notes |
|---|---|---|---|---|---|
| 1 | Global CSS applied to WordPress Additional CSS and rendering correctly on all 3 pages | | | | |
| 2 | Global JavaScript loaded in footer, no console errors on page load | | | | |
| 3 | All 3 pages load and display correctly on desktop: Homepage, Request to Book, Experiences | | | | |
| 4 | Request to Book form submits without errors and passes validation | | | | |
| 5 | Airtable receiving form data: Requests, UTMs, and Contacts records created correctly | | | | |
| 6 | All Make.com scenarios are active (not paused or in draft) | | | | |
| 7 | GTM container published (not just previewed) with all 14 events configured | | | | |
| 8 | Meta Pixel base code verified via Meta Pixel Helper extension | | | | |
| 9 | TikTok Pixel base code verified via TikTok Pixel Helper extension | | | | |
| 10 | SEO meta description present on homepage (verified in browser source or Yoast) | | | | |
| 11 | Mobile layout correct on iPhone 14 (390px): no horizontal scroll, text readable, CTAs tap-able | | | | |
| 12 | Phone number is a live tap-to-call link (href="tel:...") that dials on mobile | | | | |
| 13 | Social proof strip visible on homepage below hero section | | | | |
| 14 | Email capture section visible on homepage and functional (submits, Make.com receives payload) | | | | |
| 15 | /thank-you/ page exists and is reached after successful form submission | | | | |
| 16 | GA4 receiving events in DebugView or Realtime: at minimum page_view and submit_booking_form | | | | |
| 17 | No em dashes present in any visible page copy or HTML source | | | | |
| 18 | No JavaScript console errors on homepage, request page, or experiences page | | | | |
| 19 | Page load time under 3 seconds on 4G simulation (Chrome DevTools > Network > 4G throttle) | | | | |
| 20 | Founder QA sign-off: Will has reviewed homepage, request page, and experiences page on desktop and mobile | | | | |

---

## Sign-Off

All 20 items must be marked Pass or N/A before any paid traffic is directed to the site.

Signed: _____________________ Date: _____________________

**Linked Specialist Checklists:**
- Mobile: `09_QA/mobile-qa-checklist.md`
- Forms: `09_QA/form-qa-checklist.md`
- Backend: `09_QA/backend-qa-checklist.md`
- Tracking: `09_QA/tracking-qa-checklist.md`
