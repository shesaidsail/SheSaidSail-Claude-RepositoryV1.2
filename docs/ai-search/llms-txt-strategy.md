# She Said Sail: llms.txt Strategy

**Version:** 1.0
**Date:** 2026-05-18

---

## WHAT IS llms.txt

llms.txt is a plain-text file placed at the root of a website (following the same convention as robots.txt and sitemap.xml) intended to help large language models understand a site's content structure and priorities.

The format was proposed by Jeremy Howard of Answer.AI in September 2024. It is not a formal web standard and is not maintained by the W3C or any standards body. However, it has been adopted by a growing number of websites and developers who want to give AI crawlers an explicit, readable summary of what their site contains and which pages matter most.

The file is written in plain text or lightweight markdown. It typically includes a short brand description, a list of important pages with brief descriptions, and any guidance about what the site does and does not cover.

**What it is not:**
- Not a replacement for robots.txt (which controls technical crawler access and blocking).
- Not a sitemap.xml (which provides full URL inventory for search engine crawling).
- Not a structured data format (schema.org handles that on individual pages).

llms.txt is a semantic priority guide. It tells an AI: "Here is what this site is about, and here are the pages that matter most."

---

## WHY WE CREATED IT

She Said Sail is a discovery-driven luxury brand. Most clients do not start their search on the She Said Sail website. They start on a conversational AI assistant, a search engine, or a platform like Perplexity, asking a question like:

- "What are the best bachelorette yacht rentals in Miami?"
- "Private yacht charter Miami for a girls trip, how much does it cost?"
- "Luxury boat party ideas for a birthday in Fort Lauderdale."

Being cited by AI assistants (ChatGPT, Perplexity, Gemini, Claude) when someone asks about bachelorette experiences or yacht charters in Miami is a meaningful acquisition channel. The client who arrives via an AI citation is already primed: they have been told She Said Sail is relevant to their query. The conversion path is shorter.

llms.txt supports this by:

1. **Giving AI crawlers a summary they can use without synthesizing the whole site.** An AI does not need to read every page to know what She Said Sail does. llms.txt puts that summary in one place.

2. **Signaling which pages are most important.** Not all pages carry equal weight. llms.txt tells AI crawlers that the four experience pages, the FAQ, and the booking page are the core of the site. This prioritization matters when an AI is deciding which content to weight most heavily in a response.

3. **Complementing schema.org structured data.** Schema.org markup on individual pages tells AI systems what a specific page is about. llms.txt tells them how all those pages fit together as a brand. Both signals matter.

4. **Complementing robots.txt.** robots.txt controls which pages a crawler is technically allowed to access. llms.txt does not replace that. It adds a semantic layer on top: among the pages that are allowed, here is the priority order and the brand context.

5. **Low cost, meaningful upside.** Creating and maintaining llms.txt requires minimal ongoing effort. Even if only some AI systems read it, the cost of creating it is low enough that the potential citation benefit justifies it.

---

## WHAT WE INCLUDED

The She Said Sail llms.txt file contains the following sections.

**Brand summary**
A two-to-three sentence canonical description of She Said Sail: what the company does, where it operates, who it serves, and the price range. This is the most important section. If an AI reads nothing else in the file, this paragraph alone gives it enough to cite the brand accurately.

**Service area and price range**
Explicit location signals (Miami, Biscayne Bay, Fort Lauderdale) and the starting price ($10,000). These are the two most common factual anchors in conversational queries about luxury yacht charters.

**Priority pages with descriptions**
An ordered list of the site's most important pages, each with a one-sentence description. The order signals priority: homepage first, then experiences overview, then individual experience pages, then booking path, then FAQ.

**Experience pages with entity descriptions**
Each of the four experiences (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club) listed individually with a brief description that includes occasion, atmosphere, and capacity. This allows an AI to distinguish the four offerings from each other without reading four separate pages.

**Booking path**
The /request-to-book/ URL is listed explicitly. This tells AI systems that booking is concierge-led and gives them the correct URL to surface if a user asks how to book.

**FAQ signal**
The /faq/ page is listed with a note that it contains answers to common questions about yacht charters, group sizes, pricing, and occasions. This reinforces the FAQ as a high-priority retrieval source.

**Journal signal**
The /journal/ section is listed as ongoing content about luxury yacht experiences and women-led celebrations. This is a topical authority signal: the brand publishes content in its category, not just sales pages.

---

## WHAT TO AVOID IN llms.txt

**Keyword stuffing**
The file should read like a clear, honest description of the site. Repeating terms like "bachelorette yacht Miami bachelorette boat party Miami yacht" in the file does not help AI systems and may reduce the trustworthiness of the signal. Write descriptions in plain sentences.

**Misleading descriptions**
Do not describe pages as more comprehensive or authoritative than they are. If a journal article is a short brand post, describe it as that. AI systems that crawl and compare the llms.txt description against the actual page content may down-weight sites where the file overpromises.

**Pages that should not be indexed**
The /thank-you/ confirmation page is excluded from llms.txt. It contains no useful content for an AI to cite and should not be surfaced in AI responses. Similarly, any admin, login, or internal pages should be excluded.

**PII or sensitive operational data**
llms.txt is a public file. Do not include contact details beyond what is already public, internal pricing structures, vendor names, or any information that is not intended for public consumption.

**Duplicate content from schema.org**
llms.txt is not a place to copy and paste schema.org markup. It is plain text. Keep descriptions concise and human-readable. The structured data lives in the schema files on each page.

---

## MAINTENANCE

llms.txt should be reviewed and updated in the following situations.

**When a new experience launches**
Add the new experience to the priority pages list with a one-sentence description. Update the brand summary if the total number of experiences changes.

**When pricing changes**
The starting price ($10,000) is stated explicitly in the brand summary. Update it whenever pricing is publicly updated on the site.

**When new journal categories emerge**
If the journal section develops a distinct content category (for example, a destination guide series or a planning guide series), add a note about it in the journal section of the file.

**Annual review**
Review the file once per year to confirm that all URLs are still accurate, all experience names are consistent with current schema, and the brand description reflects how She Said Sail is currently positioning itself.

**When the site structure changes significantly**
If pages are moved, renamed, or retired, update llms.txt accordingly. A file that references broken URLs or outdated page names is worse than no file at all.

---

## DEPLOYMENT

**File location**
The file must be placed at the root of the domain, not in a subdirectory. The correct path is:

```
/llms.txt
```

The file must be publicly accessible at:

```
https://shesaidsail.com/llms.txt
```

It must not require authentication, redirect through another URL, or be blocked by robots.txt.

**In WordPress**
The file can be deployed in one of two ways:

Option 1 (recommended): Upload llms.txt via FTP or SFTP directly to the WordPress root directory (the same directory that contains wp-config.php and the wp-content folder). The file will then be served directly by the web server without passing through WordPress.

Option 2: Use a WordPress plugin that allows custom file serving or custom rewrites. Some SEO plugins (such as Yoast or RankMath in premium versions) may support llms.txt in the future. As of the date of this document, manual upload is the most reliable method.

**Verification**
After uploading, verify the file is accessible by visiting https://shesaidsail.com/llms.txt in a browser. The file should render as plain text. If it triggers a 404 error or a WordPress template page, the upload location is incorrect.

**No registration required**
There is no registry or submission process for llms.txt. AI crawlers that support the convention will discover it by requesting the file at the well-known path. There is nothing to submit or verify with any third party.

---

## LIMITATIONS AND REALISTIC EXPECTATIONS

llms.txt is a best-effort signal, not a guaranteed indexing instruction.

As of 2026, there is no public confirmation that ChatGPT (OpenAI), Gemini (Google), or Claude (Anthropic) crawlers actively read and weight llms.txt files in their retrieval or citation logic. Some AI search tools (including Perplexity) have indicated awareness of the convention.

The file should be understood as:
- A low-cost positive signal with meaningful upside.
- Not a replacement for strong page content, well-formed schema.org markup, and a technically accessible site.
- Part of a broader GEO strategy that includes structured data, FAQ content, entity consistency, and topical authority through the journal.

The strongest signals for AI citation remain: clear, factual content on well-structured pages, complete and accurate schema.org markup, consistent entity names across the site, and direct answers to common user questions.

llms.txt supports all of those. It does not replace any of them.

---

*Strategy document prepared for She Said Sail internal use. Review alongside the AI Search Readiness Audit (ai-search-audit.md) for full context on the GEO optimization pass this document was created as part of.*
