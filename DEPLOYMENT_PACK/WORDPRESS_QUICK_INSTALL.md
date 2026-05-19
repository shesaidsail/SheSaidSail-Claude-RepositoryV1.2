# WordPress Quick Install Pack

**Version:** 1.0
**Purpose:** Copy-paste reference for all WordPress admin operations. Use this file instead of hunting through multiple guides.

Everything in this document is a direct action. Each section has a destination and a paste block. No interpretation needed.

---

## Table of Contents

1. Insert Headers and Footers: Scripts in Header
2. Insert Headers and Footers: Scripts in Body (Noscript)
3. Insert Headers and Footers: Scripts in Footer
4. Additional CSS
5. Elementor HTML Widget Placement Map
6. Yoast SEO: Per-Page Meta Fields
7. Hidden Fields in the Request to Book Form
8. Plugin Checklist

---

## 1. Scripts in Header

**Path:** WordPress Admin > Settings > Insert Headers and Footers > Scripts in Header

Paste this entire block. Do not split it. The dataLayer init line must come first.

```html
<script>window.dataLayer = window.dataLayer || [];</script>
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-TZ5KNRTH');</script>
<!-- End Google Tag Manager -->
```

Click **Save**.

---

## 2. Scripts in Body (Noscript Tag)

**Path:** WordPress Admin > Settings > Insert Headers and Footers > Scripts in Body

This is the GTM noscript fallback for users with JavaScript disabled.

```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-TZ5KNRTH"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

Click **Save**.

---

## 3. Scripts in Footer

**Path:** WordPress Admin > Settings > Insert Headers and Footers > Scripts in Footer

Paste both blocks below, in this order: global JS first, chatbot JS second. Leave a blank line between them.

### 3a. Global JS

```html
<script defer>
/* PASTE THE FULL CONTENTS OF: 02_GLOBAL_JS/she-said-sail-global.js HERE */
/* After pasting, find WIRE_THIS_REQUEST_FORM_WEBHOOK_URL and replace with your Make.com webhook URL */
</script>
```

To paste: open `02_GLOBAL_JS/she-said-sail-global.js`, copy the entire file, replace the comment above with the actual code.

After pasting, find this line and replace the placeholder:

```
fetch('WIRE_THIS_REQUEST_FORM_WEBHOOK_URL', {
```

Replace `WIRE_THIS_REQUEST_FORM_WEBHOOK_URL` with the real Make.com webhook URL from M-WEBFORM-REQUEST-CAPTURE.

Also find the commented-out email capture fetch block and uncomment it, replacing the placeholder URL with the M-EMAIL-CAPTURE webhook URL.

### 3b. Chatbot JS

```html
<script defer>
/* PASTE THE FULL CONTENTS OF: chatbot/chatbot-js.js HERE */
/* After pasting, find WIRE_THIS_CHATBOT_WEBHOOK_URL and replace with your Make.com webhook URL */
</script>
```

To paste: open `chatbot/chatbot-js.js`, copy the entire file, replace the comment above with the actual code.

After pasting, find this line and replace the placeholder:

```
xhr.open('POST', 'WIRE_THIS_CHATBOT_WEBHOOK_URL', true);
```

Replace `WIRE_THIS_CHATBOT_WEBHOOK_URL` with the real Make.com webhook URL from M-CHATBOT-001.

### 3c. Chatbot CSS (if not using Additional CSS)

If you prefer to keep chatbot CSS separate from the global CSS file, add it here too:

```html
<style>
/* PASTE THE FULL CONTENTS OF: chatbot/chatbot-css.css HERE */
</style>
```

Click **Save** after all blocks are in place.

---

## 4. Additional CSS

**Path:** WordPress Admin > Appearance > Customize > Additional CSS

Paste the entire contents of:

```
01_GLOBAL_CSS/she-said-sail-global.css
```

The file is approximately 1500 lines. Paste all of it. Do not remove any of it. If something looks broken after pasting, check the browser console for CSS errors before deleting anything.

Click **Publish**.

---

## 5. Elementor HTML Widget Placement Map

For each item below: open the page in Elementor, find the placement, add a Container section (full width, zero padding, zero margin), add an HTML widget inside, paste the file contents.

| Page | File | Placement |
|---|---|---|
| Homepage | `03_HTML_SNIPPETS/homepage/social-proof-strip.html` | Between experience cards section and "Not Just a Charter" section |
| Homepage | `03_HTML_SNIPPETS/homepage/hero-occasion-pills.html` | Inside hero section, below main headline, above CTA button |
| Homepage | `03_HTML_SNIPPETS/homepage/email-capture-section.html` | Above the bottom navy CTA banner |
| Request to Book | `03_HTML_SNIPPETS/request-to-book/concierge-reassurance-block.html` | Above the form |
| Request to Book | `03_HTML_SNIPPETS/request-to-book/request-form-intro.html` | Between reassurance block and form |
| Request to Book | `03_HTML_SNIPPETS/request-to-book/trust-note-under-form.html` | Below the form submit button |
| Experiences | `03_HTML_SNIPPETS/experiences/experiences-hero-support-copy.html` | Below page hero, above experience cards |
| Experiences | `03_HTML_SNIPPETS/experiences/experience-card-content.html` | Replaces or supplements default card text |
| Experiences | `03_HTML_SNIPPETS/experiences/experiences-social-proof-strip.html` | Below experience cards, above bottom CTA |
| Experiences | `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html` | Bottom of page |
| Monaco Social | `03_HTML_SNIPPETS/monaco-social/hero-support.html` | Below Monaco Social page hero |
| Monaco Social | `03_HTML_SNIPPETS/monaco-social/social-proof.html` | Below experience details section |
| About | `pages/about/about-html-snippets.html` | Full page: hero, brand story, values, bottom CTA (4 sections) |
| Contact | `pages/contact/contact-html-snippets.html` | Full page content |
| FAQ | `pages/faq/faq-html-snippets.html` | Full page content |
| Golden Hour Escape | `pages/golden-hour-escape/golden-hour-escape-html-snippets.html` | Full page content |
| Pink Palm Club | `pages/pink-palm-club/pink-palm-club-html-snippets.html` | Full page content |
| Rose Day Club | `pages/rose-day-club/rose-day-club-html-snippets.html` | Full page content |
| Journal | `pages/journal/journal-html-snippets.html` | Full page content |
| Thank You | `pages/thank-you/thank-you-html-snippets.html` | Full page content |

---

## 6. Yoast SEO: Per-Page Meta Fields

For each page: open the page in WordPress editor, scroll to the Yoast SEO section at the bottom.

| Page | SEO Title | Meta Description | Focus Keyphrase |
|---|---|---|---|
| Homepage | She Said Sail | Miami's luxury yacht charter for bachelorette parties, birthdays, and group celebrations. | luxury yacht charter miami |
| Request to Book | Request to Book a Yacht Charter | She Said Sail | Tell us about your group. We will match you with the right experience and handle every detail from there. | yacht charter request miami |
| Experiences | Yacht Charter Experiences | She Said Sail | Four experiences designed for different occasions: Monaco Social, Golden Hour Escape, Rose Day Club, and Pink Palm Club. | yacht charter experiences miami |
| Monaco Social | Monaco Social Yacht Charter | She Said Sail | The bachelorette and birthday charter. Champagne, Riviera energy, and a polished afternoon on the water. Groups up to 14. | monaco social yacht charter |
| About | About She Said Sail | Built by someone who noticed that women celebrating together deserved better. Here is what we believe and why. | she said sail about |

For OG Image: upload a high-quality brand photo at 1200x630px. Warm tones, water, natural light.

For pages not listed: use the page title as the SEO title prefix and write a one-sentence meta description that describes what the visitor will find on that page.

---

## 7. Hidden Fields in the Request to Book Form

**Purpose:** These fields capture UTM, visitor ID, and session data automatically on form submission. The JS in `she-said-sail-global.js` populates them.

**Path:** Elementor editor > Request to Book page > click the form widget > Edit Element > Content > Form Fields

Add these hidden fields to the form:

| Field Label | Field Type | Field ID (CSS ID) | Default Value |
|---|---|---|---|
| utm_source | Hidden | utm_source | (empty) |
| utm_medium | Hidden | utm_medium | (empty) |
| utm_campaign | Hidden | utm_campaign | (empty) |
| utm_content | Hidden | utm_content | (empty) |
| utm_term | Hidden | utm_term | (empty) |
| visitor_id | Hidden | visitor_id | (empty) |
| referrer_url | Hidden | referrer_url | (empty) |
| landing_page | Hidden | landing_page | (empty) |
| source_type | Hidden | source_type | webform |
| brand | Hidden | brand | shesaidsail |

The global JS targets these fields by their Field ID (the CSS ID field in Elementor's form field settings). The IDs must match exactly.

For full hidden field setup documentation, see: `05_AIRTABLE_BACKEND/request-form-hidden-fields.md`

---

## 8. Plugin Checklist

Confirm all plugins are installed and active before starting any installation steps.

| Plugin | Version | Status | Purpose |
|---|---|---|---|
| Elementor Pro | 4.0.3+ | Must be Active | Page builder. All HTML widgets require this. |
| Hello Elementor | any | Must be Active (as theme) | Base theme. Do not switch to another theme. |
| Insert Headers and Footers | any | Must be Active | Injects GTM, global JS, chatbot JS |
| Yoast SEO | any | Must be Active | Per-page meta and OG tags |
| MetForm or Elementor Pro Forms | any | Must be Active | Request to Book form with hidden fields |
| Tidio | n/a | Must be INACTIVE | Custom chatbot cannot run alongside Tidio |

If Tidio is installed and active, deactivate it before adding the chatbot JS. Both widgets will conflict visually and behaviorally.

---

## Webhook URL Reference

Replace these placeholders with real URLs after building the Make.com scenarios.

| Placeholder | File | Scenario |
|---|---|---|
| `WIRE_THIS_REQUEST_FORM_WEBHOOK_URL` | `02_GLOBAL_JS/she-said-sail-global.js` | M-WEBFORM-REQUEST-CAPTURE |
| `WIRE_THIS_CHATBOT_WEBHOOK_URL` | `chatbot/chatbot-js.js` | M-CHATBOT-001 |
| `WIRE_THIS_CONTACT_WEBHOOK_URL` | `pages/contact/contact-html-snippets.html` | Create M-CONTACT-001 if needed |
| Email capture fetch URL (commented out) | `02_GLOBAL_JS/she-said-sail-global.js` | M-EMAIL-CAPTURE |

After replacing each placeholder, save the file. If the JS is already deployed in Insert Headers and Footers, update it there as well.
