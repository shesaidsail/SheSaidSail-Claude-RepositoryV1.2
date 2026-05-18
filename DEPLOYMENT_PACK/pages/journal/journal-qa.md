# Journal QA Checklist
Page: /journal/
File: journal-qa.md

Tester: ___________________________
Date tested: ___________________________
Environment: ___________________________

Mark each item PASS or FAIL. Add notes where relevant.

---

## Desktop Rendering (test at 1440px and 1280px viewport widths)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| D-01 | Journal header section renders with cream (#FAF8F3) background | | |
| D-02 | Gold eyebrow "THE JOURNAL" is visible above the H1 | | |
| D-03 | H1 reads "Stories, guides, and ideas for celebrating well." | | |
| D-04 | Subline paragraph is visible below the H1 and centered | | |
| D-05 | Article card grid renders in 3 columns | | |
| D-06 | All 6 template article cards are visible | | |
| D-07 | Each card has a placeholder image area, category pill, title, excerpt, read time, and Read More link | | |
| D-08 | Article Page CTA Block renders with warm cream (#F5F0E8) background | | |
| D-09 | CTA block heading reads "Experience it for yourself." in italic Cormorant Garamond | | |
| D-10 | Two ghost buttons appear side by side in the CTA block | | |

---

## Mobile Rendering (test at 375px and 390px viewport widths)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| M-01 | Journal header text is readable, no horizontal overflow | | |
| M-02 | H1 renders at reduced size (target 34px) | | |
| M-03 | Article cards collapse to a single column | | |
| M-04 | Card images stack correctly above card text | | |
| M-05 | Card titles, excerpts, and read times are readable at mobile size | | |
| M-06 | Article CTA block buttons stack to full width vertically | | |
| M-07 | No elements overflow the viewport horizontally | | |

---

## Card Content Verification (6 template cards)

| # | Card Title | Category Pill Present | Excerpt Present | Read Time Present | Read More Link Present | Result |
|---|-----------|----------------------|-----------------|-------------------|----------------------|--------|
| C-01 | What to Expect on Your First Private Yacht Charter | Experience | | | | |
| C-02 | Bachelorette Party Ideas in Miami: Beyond the Club | Bachelorette | | | | |
| C-03 | How to Plan the Perfect Girls Trip to Miami | Planning | | | | |
| C-04 | 5 Reasons the Golden Hour is the Best Time to Be on the Water | On the Water | | | | |
| C-05 | What Our Guests Say: Real Experiences on She Said Sail | Guest Stories | | | | |
| C-06 | How to Choose the Right Yacht Experience for Your Group | Planning | | | | |

---

## Article CTA Block

| # | Check | Result | Notes |
|---|-------|--------|-------|
| A-01 | Eyebrow reads "READY WHEN YOU ARE" | | |
| A-02 | Heading reads "Experience it for yourself." | | |
| A-03 | Body copy reads "Browse the experiences and submit a request when your date is in mind. No commitment required." | | |
| A-04 | "View the Experiences" button links to /experiences/ | | |
| A-05 | "Request to Book" button links to /request-to-book/ | | |
| A-06 | Both buttons render as ghost style (navy border, navy text, transparent fill) | | |
| A-07 | Hover state changes button to navy fill with cream text | | |

---

## SEO

| # | Check | Result | Notes |
|---|-------|--------|-------|
| S-01 | Page title is "The Journal | She Said Sail Private Yacht Experiences Miami" | | |
| S-02 | Meta description is under 155 characters | | |
| S-03 | Meta description matches the text in journal-metadata.html | | |
| S-04 | Canonical tag points to https://shesaidsail.com/journal/ | | |
| S-05 | Open Graph title, description, type, url, and image tags are all present | | |
| S-06 | og:type is set to "website" | | |
| S-07 | Twitter Card meta tags are present (card, title, description, image) | | |
| S-08 | Page is not set to noindex in Yoast, RankMath, or robots meta tag | | |
| S-09 | JSON-LD CollectionPage schema is present in the page source | | |

---

## Individual Article Metadata Template

| # | Check | Result | Notes |
|---|-------|--------|-------|
| T-01 | The article metadata template comment block is present in journal-metadata.html | | |
| T-02 | Template includes Article JSON-LD schema with all required fields | | |
| T-03 | Template includes the internal linking requirement note | | |
| T-04 | Template placeholders are clearly marked with [BRACKETED] notation | | |

---

## Analytics

| # | Check | Result | Notes |
|---|-------|--------|-------|
| AN-01 | Open GTM Preview mode and load /journal/ in the browser | | |
| AN-02 | Confirm view_journal_page fires on page load | | |
| AN-03 | Confirm scroll_50_percent fires when scrolling past the 50% mark | | |
| AN-04 | Confirm scroll_90_percent fires when scrolling past the 90% mark | | |
| AN-05 | Confirm click_explore_experiences fires when clicking a link to /experiences/ | | |
| AN-06 | Confirm click_request_to_book fires when clicking a link to /request-to-book/ | | |

---

## WordPress Configuration

| # | Check | Result | Notes |
|---|-------|--------|-------|
| W-01 | /journal/ slug is active in WordPress (not /blog/) | | |
| W-02 | /journal/ returns HTTP 200 (not a redirect or 404) | | |
| W-03 | Individual article URLs produce the pattern /journal/[article-slug]/ | | |
| W-04 | If /blog/ was previously active, a 301 redirect from /blog/ to /journal/ is in place | | |
| W-05 | Journal articles appear in the XML sitemap | | |

---

## Internal Linking (verify per article once articles are written)

| # | Check | Result | Notes |
|---|-------|--------|-------|
| IL-01 | Every published article contains at least one link to /experiences/ or a specific experience page | | |
| IL-02 | Every published article contains at least one link to /request-to-book/ | | |
| IL-03 | The Article Page CTA Block is present at the bottom of every published article | | |

---

## Brand and Tone

| # | Check | Result | Notes |
|---|-------|--------|-------|
| B-01 | No em dashes appear anywhere on the page or in any article excerpts | | |
| B-02 | Card excerpts read as editorial and informative, not promotional or salesy | | |
| B-03 | Category pills use uppercase Inter, gold color, no background box | | |
| B-04 | Article titles use Cormorant Garamond | | |
| B-05 | Read More links use gold color with border-bottom underline | | |

---

## Sign-Off

Visual QA approved by: ___________________________

SEO check approved by: ___________________________

Analytics confirmed by: ___________________________

Date signed off: ___________________________

Notes:
