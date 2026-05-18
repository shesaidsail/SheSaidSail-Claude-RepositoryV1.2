# She Said Sail: AI Crawler and robots.txt Guide
**Version:** 1.0
**Date:** May 2026
**Purpose:** Defines how AI crawlers are handled on the She Said Sail site. Covers robots.txt directives, known AI bot user agents, and crawl access policy.

---

## PHILOSOPHY

She Said Sail is a discovery-driven brand. Being found and accurately represented by AI assistants (ChatGPT, Perplexity, Gemini, Claude, Siri) is a meaningful acquisition channel for a luxury service where a single booking generates $10,000 or more in revenue.

The default policy is: allow all reputable AI crawlers on all public pages. Restrict only post-conversion pages that should not surface in AI-generated recommendations.

---

## ROBOTS.TXT TEMPLATE

This is the recommended robots.txt file for shesaidsail.com. Paste into WordPress via a plugin (e.g., Yoast SEO has a robots.txt editor) or upload to the root via FTP.

```
# She Said Sail | robots.txt
# Last updated: May 2026

# Standard search engines
User-agent: Googlebot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/
Disallow: /wp-includes/

User-agent: Bingbot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

# OpenAI bots
# Allow GPTBot: training data crawl (affects ChatGPT knowledge)
User-agent: GPTBot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

# Allow ChatGPT-User: real-time ChatGPT browsing and search
User-agent: ChatGPT-User
Allow: /
Disallow: /thank-you/

# Allow OAI-SearchBot: ChatGPT web search integration
User-agent: OAI-SearchBot
Allow: /
Disallow: /thank-you/

# Anthropic (Claude)
User-agent: ClaudeBot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

User-agent: anthropic-ai
Allow: /
Disallow: /thank-you/

# Perplexity AI
User-agent: PerplexityBot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

# Google AI (Gemini, AI Overviews)
# Googlebot handles this but Googlebot-Extended covers AI training
User-agent: Google-Extended
Allow: /
Disallow: /thank-you/

# Apple (Siri, Apple Intelligence)
User-agent: Applebot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

User-agent: Applebot-Extended
Allow: /
Disallow: /thank-you/

# Diffbot (knowledge graph extraction)
User-agent: Diffbot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

# Meta AI
User-agent: FacebookBot
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/

# General allow for all others
User-agent: *
Allow: /
Disallow: /thank-you/
Disallow: /wp-admin/
Disallow: /wp-includes/

# Sitemap
Sitemap: https://shesaidsail.com/sitemap.xml
```

---

## WHY /thank-you/ IS DISALLOWED

The /thank-you/ page loads after a booking request is submitted. It is a post-conversion state page with no informational value for an AI assistant. Disallowing it prevents AI systems from citing or summarizing it, which would create a confusing user experience if someone found it through AI search.

The page also has `<meta name="robots" content="noindex, nofollow">` in its HTML, which is the primary protection. robots.txt is a secondary layer.

---

## KNOWN AI CRAWLER BOT REFERENCE

| Bot Name | Publisher | User Agent String | Purpose |
|---|---|---|---|
| GPTBot | OpenAI | GPTBot/1.1 | Training data for ChatGPT |
| ChatGPT-User | OpenAI | ChatGPT-User/1.1 | Real-time ChatGPT browsing |
| OAI-SearchBot | OpenAI | OAI-SearchBot/1.1 | ChatGPT search |
| ClaudeBot | Anthropic | ClaudeBot/1.0 | Claude training and retrieval |
| anthropic-ai | Anthropic | anthropic-ai | Anthropic general crawler |
| PerplexityBot | Perplexity | PerplexityBot/1.0 | Perplexity answer engine |
| Google-Extended | Google | Googlebot | Gemini and AI Overviews training |
| Applebot | Apple | Applebot/0.1 | Siri and Apple Intelligence |
| Applebot-Extended | Apple | Applebot-Extended/0.1 | Apple AI training |
| Diffbot | Diffbot | Diffbot/3.0 | Knowledge graph and entity extraction |
| FacebookBot | Meta | facebookexternalhit | Meta AI and Llama |
| Bingbot | Microsoft | bingbot/2.0 | Copilot / Bing |

---

## WHAT AI CRAWLERS READ

AI crawlers behave differently from traditional search crawlers. Key differences:

1. **They read the full page.** Not just meta tags and H1. Full paragraph text, FAQ content, experience descriptions. Write every page assuming an AI will read all of it.

2. **They follow links.** Internal linking between pages matters. A page linked from the homepage is more likely to be crawled and included in an AI's knowledge than an orphan page.

3. **They understand JSON-LD.** Structured data directly informs what AI systems "know" about a business entity. The schema on She Said Sail pages is a primary signal for entity understanding.

4. **They read llms.txt.** Per the llmstxt.org spec, at inference time (when a user asks about the site), AI systems may read /llms.txt to understand site structure and content priorities before generating an answer.

5. **They prefer clear, direct language.** Vague luxury copy ("an experience unlike any other") provides no extractable information. Clear copy ("up to 22 guests, starting from $10,000, Miami and Fort Lauderdale") does.

---

## PRIORITY PAGES FOR AI CRAWL

The pages most important for AI discovery and citation, in priority order:

1. **Homepage** (https://shesaidsail.com/) - Entity definition, brand summary
2. **FAQ** (https://shesaidsail.com/faq/) - Direct question-answer pairs for AI extraction
3. **Experience pages** (all 4) - Specific service information for recommendation queries
4. **About** (https://shesaidsail.com/about/) - Brand story and trust signals
5. **Experiences index** (https://shesaidsail.com/experiences/) - Comparison overview
6. **Journal** (https://shesaidsail.com/journal/) - Topical authority and long-tail discovery
7. **llms.txt** (https://shesaidsail.com/llms.txt) - AI system navigation file

---

## MONITORING AI VISIBILITY

There is no direct Google Search Console equivalent for AI crawler visibility. Monitoring approaches:

1. **Manual query testing:** Ask ChatGPT, Perplexity, Gemini, and Claude: "What is She Said Sail?" and "Best bachelorette yacht experience Miami." Check if the site is cited.

2. **Server logs:** Filter access logs for known AI bot user agent strings to confirm they are crawling.

3. **Google Search Console:** Monitor AI Overviews appearances via the Search Console Performance report. Filter by queries that trigger AI Overviews.

4. **Perplexity.ai:** Perplexity shows its sources. Search for relevant terms and check if She Said Sail appears as a cited source.

Recommended frequency: check quarterly, or after major site changes.
