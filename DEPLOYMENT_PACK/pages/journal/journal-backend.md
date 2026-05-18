# Journal Backend Notes
Page: /journal/
File: journal-backend.md

---

## Forms and Airtable

No form exists on the journal index page. No Airtable writes occur from this page. No Make.com workflows are triggered by visiting or browsing the journal.

Individual journal articles also contain no forms. The only backend touchpoint from the journal section is through CTAs that link visitors to /request-to-book/, where the booking request form and its Airtable/Make.com integration live.

---

## SEO Crawlability

The journal index page at /journal/ must NOT be set to noindex. It should be fully crawlable and included in the XML sitemap.

Individual article pages must also be indexed. Every published article should appear in the sitemap, either through the WordPress sitemap plugin (Yoast or RankMath) auto-discovery, or by manual inclusion if using a static site approach.

---

## Internal Linking Standard for All Journal Articles

Every published article must contain at minimum:

1. At least one link to /experiences/ or to a specific experience page at /experience/[slug]/. This can appear inline in the article body or in the Article Page CTA Block.
2. At least one link to /request-to-book/. The Article Page CTA Block (Section 3 in journal-html-snippets.html) placed at the bottom of every article satisfies this requirement automatically.

These links serve two purposes: they improve crawl depth for search engines, and they create a conversion path for readers who arrive via organic search.

---

## WordPress Setup

If using WordPress with a custom post type or the standard Posts post type for the journal:

- Confirm the permalink structure produces /journal/[article-slug]/ for all articles. The correct WordPress permalink setting is a custom structure with a category or custom base of "journal".
- Avoid /blog/ as the post base if the site navigation uses /journal/. Inconsistent URL structures split link equity and confuse visitors who bookmark or share links.
- If the theme uses a custom post type named "journal", ensure it is registered with the rewrite slug set to "journal" and that has_archive is set to true so the index page at /journal/ is generated automatically.
- If the theme uses the standard WordPress Posts post type, update Settings > Reading or the permalink settings to route posts under /journal/.
- Confirm that /journal/ returns a 200 HTTP status, not a redirect, and that the canonical on the index page matches the URL in the browser bar.

---

## Redirect Note

If /blog/ was previously the active URL for journal content, set up a 301 redirect from /blog/ to /journal/ at the server or plugin level (e.g., Redirection plugin for WordPress). Do not leave /blog/ active in parallel with /journal/ as duplicate content.
