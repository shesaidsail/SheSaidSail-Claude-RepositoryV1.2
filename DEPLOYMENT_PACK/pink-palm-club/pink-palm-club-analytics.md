# PINK PALM CLUB
# ANALYTICS SPECIFICATION

STATUS: READY FOR IMPLEMENTATION
VERSION: v1.0
EFFECTIVE DATE: May 2026
PAGE: https://shesaidsail.com/experience/pink-palm-club/
ANALYTICS OWNER: Will Hunt
SYSTEM REFERENCE: docs/system/master-backend-system.md

---

## TRACKING STACK

| Layer | Tool | Purpose |
|-------|------|---------|
| Tag manager | Google Tag Manager (GTM) | Container for all tracking |
| Analytics | Google Analytics 4 (GA4) | Behavior, conversion, traffic |
| Ad tracking | Meta Pixel | Paid social campaign optimization |
| Ad tracking | TikTok Pixel | TikTok campaign optimization |
| Session recording | Hotjar (if active) | UX observation and heatmaps |

---

## GTM DATA LAYER EVENTS

All events are pushed to window.dataLayer by pink-palm-club.js and picked up by GTM triggers.

### Event: sss_page_view

Fires on page load. Identifies the page and session context.

```json
{
  "event": "sss_page_view",
  "page_type": "experience",
  "experience_name": "Pink Palm Club",
  "page_url": "https://shesaidsail.com/experience/pink-palm-club/",
  "utm_source": "instagram",
  "utm_medium": "paid_social",
  "utm_campaign": "sss-ppc-q2-2026"
}
```

GTM trigger: Custom event "sss_page_view"
GA4 mapping: page_view (automatic) + custom dimensions

---

### Event: sss_form_start

Fires when a guest focuses on any form field for the first time. Fires once per session.

```json
{
  "event": "sss_form_start",
  "experience_name": "Pink Palm Club",
  "page_url": "https://shesaidsail.com/experience/pink-palm-club/"
}
```

GTM trigger: Custom event "sss_form_start"
GA4 mapping: form_start
Use: Funnel analysis -- how many guests engage with the form vs. submit it

---

### Event: sss_lead_submitted

Fires when the guest clicks submit and validation passes. Fires before the server response.

```json
{
  "event": "sss_lead_submitted",
  "experience_name": "Pink Palm Club",
  "city": "Fort Lauderdale",
  "utm_source": "instagram",
  "utm_campaign": "sss-ppc-q2-2026"
}
```

GTM trigger: Custom event "sss_lead_submitted"
GA4 mapping: generate_lead
Meta Pixel: Lead event
TikTok Pixel: SubmitForm event

---

### Event: sss_lead_submitted_confirmed

Fires after Webflow confirms the form submission was received. This is the most reliable conversion signal.

```json
{
  "event": "sss_lead_submitted_confirmed",
  "experience_name": "Pink Palm Club",
  "city": "Fort Lauderdale"
}
```

GTM trigger: Custom event "sss_lead_submitted_confirmed"
GA4 mapping: Conversion event (mark as conversion in GA4)
Google Ads: Conversion action (if running Google Ads)

---

### Event: sss_cta_click

Fires when any button with class ppc-btn or data-cta attribute is clicked.

```json
{
  "event": "sss_cta_click",
  "cta_text": "Check availability",
  "cta_location": "hero",
  "experience_name": "Pink Palm Club"
}
```

GTM trigger: Custom event "sss_cta_click"
GA4 mapping: select_content
Use: Identify which CTAs drive the most form engagement

CTA locations tracked:
- hero (hero primary CTA)
- hero-secondary (hero ghost CTA)
- mid-page-cta (navy CTA section)
- form-submit (form submit button)
- floating-mobile (fixed bottom CTA on mobile)

---

### Event: sss_scroll_depth

Fires at 25%, 50%, 75%, and 100% page scroll depth. Does not fire duplicate events for the same milestone in one session.

```json
{
  "event": "sss_scroll_depth",
  "depth_pct": 75,
  "experience_name": "Pink Palm Club"
}
```

GTM trigger: Custom event "sss_scroll_depth"
GA4 mapping: scroll (custom parameter for depth_pct)
Use: Identify where guests stop reading. Below 50% = top content is not engaging enough.

---

## GA4 CONVERSION SETUP

In Google Analytics 4:

1. Mark "sss_lead_submitted_confirmed" as a conversion event
2. Create audience: "Pink Palm Club Leads" (users who triggered sss_lead_submitted_confirmed)
3. Create funnel exploration:
   - Step 1: sss_page_view
   - Step 2: sss_form_start
   - Step 3: sss_lead_submitted
   - Step 4: sss_lead_submitted_confirmed

Key metric: Step 1 to Step 4 conversion rate. Target: 3% minimum.

---

## UTM PARAMETER CONVENTION

Use these UTM parameters on all paid and organic links to this page:

| Parameter | Value Convention | Example |
|-----------|-----------------|---------|
| utm_source | Platform (lowercase) | instagram, google, tiktok, email |
| utm_medium | Channel type | paid_social, organic_social, cpc, email |
| utm_campaign | Campaign identifier | sss-ppc-q2-2026 |
| utm_content | Creative identifier | hero-video-reel-1 |
| utm_term | Keyword (paid search) | bachelorette yacht fort lauderdale |

Example URL:
https://shesaidsail.com/experience/pink-palm-club/?utm_source=instagram&utm_medium=paid_social&utm_campaign=sss-ppc-q2-2026&utm_content=hero-video-reel-1

UTM parameters are captured in sessionStorage by pink-palm-club.js and:
1. Stored for the full session (survives navigation within the site)
2. Injected into hidden form fields before submission
3. Pushed to the GTM data layer on page view
4. Sent to Airtable via Make form handler

---

## META PIXEL EVENTS

| GA4 Event | Meta Standard Event | Custom Parameters |
|-----------|-------------------|------------------|
| sss_page_view | PageView | content_name: "Pink Palm Club" |
| sss_lead_submitted_confirmed | Lead | content_name: "Pink Palm Club", content_category: "Yacht Charter" |

Implementation: Via GTM tag, firing on the corresponding custom event triggers.

---

## TIKTOK PIXEL EVENTS

| GA4 Event | TikTok Standard Event |
|-----------|----------------------|
| sss_page_view | ViewContent |
| sss_lead_submitted_confirmed | SubmitForm |

Implementation: Via GTM tag.

---

## GTM VARIABLE REFERENCE

Create these GTM variables for use across tags:

| Variable Name | Type | Value |
|--------------|------|-------|
| DL - experience_name | Data Layer Variable | experience_name |
| DL - utm_source | Data Layer Variable | utm_source |
| DL - utm_medium | Data Layer Variable | utm_medium |
| DL - utm_campaign | Data Layer Variable | utm_campaign |
| DL - cta_location | Data Layer Variable | cta_location |
| DL - depth_pct | Data Layer Variable | depth_pct |

---

## HOTJAR (if active)

On this page, enable:
- Heatmap recording
- Session recording (sample 20% of sessions)

Key questions to answer with Hotjar:
1. Do users scroll past the stats section to the form?
2. Where do users abandon the form?
3. Is the floating mobile CTA being tapped?
4. Do add-on cards get clicked?

---

## ANALYTICS QA CHECKLIST

- [ ] GTM container fires on page load (check GTM Preview mode)
- [ ] sss_page_view event appears in GTM Preview on load
- [ ] sss_form_start fires when first form field is focused
- [ ] sss_cta_click fires when hero CTA is clicked
- [ ] sss_scroll_depth fires at 25%, 50%, 75%, 100%
- [ ] sss_lead_submitted fires on form submit click
- [ ] sss_lead_submitted_confirmed fires after Webflow form success
- [ ] GA4 real-time shows events flowing through
- [ ] UTM params from test URL appear in hidden form fields
- [ ] Airtable record contains UTM fields after test submission
- [ ] Meta Pixel fires Lead event on conversion (use Meta Pixel Helper extension)
