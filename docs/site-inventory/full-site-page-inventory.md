# She Said Sail: Full Site Page Inventory
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul
**Source:** Repository analysis + known site structure (live site has bot protection preventing automated crawl)

Note: The live site (shesaidsail.com) returns a CAPTCHA redirect for automated requests. This inventory is compiled from all URL references across the repository, experience slug data in JS and Airtable schema, SEO meta files, install guides, and operational documentation.

---

## INVENTORY TABLE

| # | URL | Page Title (likely) | Page Type | Priority | Conv. Importance | Funnel Role | Optimized | Batch | Backend Needs | Analytics Needs |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | / | She Said Sail | Homepage | Critical | Very High | Awareness + Entry | YES | Done | Email capture webhook | view_homepage, scroll events |
| 2 | /request-to-book/ | Request to Book | Lead Form | Critical | Very High | Decision + Conversion | YES | Done | 13 hidden fields, Make webhook | view_request_page, start_form, submit_form |
| 3 | /experiences/ | Experiences | Index / Gallery | High | High | Consideration | YES | Done | None | view_experiences_page, click_experience_card |
| 4 | /experience/monaco-social/ | Monaco Social | Experience Detail | High | High | Decision | YES | Done | selected_experience param | view_experience_page |
| 5 | /experience/golden-hour-escape/ | Golden Hour Escape | Experience Detail | High | High | Decision | NO | Batch 1 | selected_experience param | view_experience_page |
| 6 | /experience/rose-day-club/ | Rose Day Club | Experience Detail | High | High | Decision | NO | Batch 1 | selected_experience param | view_experience_page |
| 7 | /experience/pink-palm-club/ | Pink Palm Club | Experience Detail | High | High | Decision | NO | Batch 1 | selected_experience param | view_experience_page |
| 8 | /thank-you/ | Thank You | Confirmation | Medium | High | Post-conversion | NO | Batch 2 | Confirmation state check | view_thank_you_page |
| 9 | /about/ | About She Said Sail | Brand / Trust | Medium | Medium | Trust building | NO | Batch 2 | None | view_about_page |
| 10 | /contact/ | Contact | Contact | Medium | Medium | Trust / Direct inquiry | NO | Batch 2 | Contact form to Airtable | view_contact_page, submit_contact_form |
| 11 | /faq/ | FAQ | Trust / SEO | Medium | Medium | Pre-purchase friction removal | NO | Batch 3 | None | view_faq_page, click_faq_item |
| 12 | /blog/ or /journal/ | Journal / Blog | SEO / Editorial | Low-Med | Low direct | Organic discovery, trust | NO | Batch 4 | None | view_journal_page |
| 13 | /terms/ or /terms-of-service/ | Terms | Legal | Low | Low | Compliance | NO | Batch 5 | None | None required |
| 14 | /privacy/ or /privacy-policy/ | Privacy Policy | Legal | Low | Low | Compliance | NO | Batch 5 | None | None required |

---

## NOTES BY PAGE

### Pages 1-4: Already Optimized

**Homepage (/):** CSS, JS, social proof strip, occasion pills, email capture, SEO meta, schema all applied. See DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/homepage-install-guide.md.

**Request to Book (/request-to-book/):** Full 13 hidden fields, Make.com webhook, concierge reassurance block, form intro, trust note, noindex meta applied. See DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/request-to-book-install-guide.md.

**Experiences (/experiences/):** Hero support copy, social proof strip, bottom CTA, experience card content, SEO meta applied. See DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/experiences-install-guide.md.

**Monaco Social (/experience/monaco-social/):** Full optimization complete. 6 HTML snippets, SEO meta, install guide, QA checklist, audit report. See DEPLOYMENT_PACK/03_HTML_SNIPPETS/monaco-social/ and DEPLOYMENT_PACK/08_PAGE_INSTALL_GUIDES/monaco-social-install-guide.md.

---

### Pages 5-7: Batch 1 (Experience Detail Pages)

These three pages follow the exact same structural pattern as Monaco Social. Each one is a decision-stage page where visitors arrive after showing interest in a specific experience. They are the closest pages to the /request-to-book/ conversion event. Optimizing them directly lifts bookings.

**Golden Hour Escape (/experience/golden-hour-escape/):**
- Occasion positioning: intimate groups, sunset events, milestone celebrations
- Badge text from JS: "Intimate groups and sunset hosting"
- Tone: quieter, more refined than Monaco Social. Sunset golden hour aesthetic.
- CTA destination: /request-to-book/?selected_experience=golden-hour-escape

**Rose Day Club (/experience/rose-day-club/):**
- Occasion positioning: social hosting, rosé and water, girls trips with style
- Badge text from JS: "Social hosting from water to table"
- Tone: warm, social, feminine, elevated brunch energy
- CTA destination: /request-to-book/?selected_experience=rose-day-club

**Pink Palm Club (/experience/pink-palm-club/):**
- Occasion positioning: bachelorette, social groups, movement and music
- Badge text from JS: "Social groups who want music and movement"
- Description from JS: "Playful Miami energy built for groups who want movement, music, and long afternoons on the water."
- Tone: more energetic and celebratory than Golden Hour, but still elevated
- CTA destination: /request-to-book/?selected_experience=pink-palm-club

---

### Page 8: Thank You (/thank-you/)

This is the post-submission confirmation page. Visitors arrive here after submitting the Request to Book form. It is a trust and next-steps page, not a conversion page. Key optimization opportunities:
- Confirm what happens next (numbered steps)
- Reduce anxiety post-submission
- Offer a soft secondary engagement (follow on Instagram, add to calendar)
- Track the view_thank_you_page event (already in the global JS)
- No form on this page; no backend changes needed beyond ensuring the GTM event fires

---

### Page 9: About (/about/)

Consistently one of the top 3 visited pages for any service brand. Visitors use it to verify legitimacy and connect with the founder story. Key opportunities:
- Founder story with emotional positioning
- Brand values expressed as felt experience, not bullet points
- Team or crew mention if applicable
- Secondary CTA to /request-to-book/ or /experiences/

---

### Page 10: Contact (/contact/)

Lower priority than the Request to Book form because /request-to-book/ handles all booking inquiries. Contact is primarily for press, partnerships, and non-booking questions. Optimization should:
- Redirect booking intent clearly to /request-to-book/
- Keep the contact form minimal
- Add appropriate routing logic in Make.com if a contact form exists

---

### Page 11: FAQ (/faq/)

Strong SEO and pre-purchase friction removal potential. Common questions to address:
- What is included in the price?
- How far in advance should I book?
- What happens if weather is bad?
- Can I bring my own food/drinks?
- Is this right for my group size?
- What is the deposit/payment structure?
FAQ answers should reinforce brand positioning, not just answer factually.

---

### Page 12: Blog / Journal (/blog/ or /journal/)

Organic traffic compound play. If a journal section exists, optimization should:
- Ensure consistent brand voice
- Add internal links to /experiences/ and /request-to-book/
- Add schema (Article, BlogPosting)
- Confirm indexability

---

### Pages 13-14: Terms and Privacy

Legal pages. No conversion optimization needed. Ensure:
- Correct meta (noindex or index as preferred)
- Schema not needed
- Plain readable formatting

---

## MARE EXECUTIVE

Mare Executive is confirmed as a separate brand entity. It has its own Airtable base (app2FbmVD44BXShyx), its own domain (mareexecutive.com), and its own Make.com routing branch (M-BRAND-ROUTER Branch 2). It is explicitly outside the scope of the She Said Sail website optimization. No Mare Executive pages are included in this inventory.

---

## SUMMARY COUNTS

| Category | Count |
|---|---|
| Total pages inventoried | 14 |
| Already optimized | 4 |
| Remaining pages | 10 |
| Batch 1 (experience detail) | 3 |
| Batch 2 (conversion support) | 3 |
| Batch 3 (trust and SEO) | 2 |
| Batch 4 (editorial/SEO) | 1 |
| Batch 5 (legal/compliance) | 2 |
| Out of scope (Mare Executive) | excluded |
