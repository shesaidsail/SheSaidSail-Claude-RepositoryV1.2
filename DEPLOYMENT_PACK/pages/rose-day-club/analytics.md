# SHE SAID SAIL
# ROSE DAY CLUB — ANALYTICS SPECIFICATION

PAGE: Rose Day Club
URL: https://shesaidsail.com/experience/rose-day-club/
VERSION: 1.0

---

## GA4 CONFIGURATION

### Pageview

Fires automatically on page load via GTM.

Custom dimensions to confirm:
- page_name: "rose-day-club" (via GTM data layer or page variable)
- experience_category: "Day Charter"
- brand: "SSS"

---

## GTM TRIGGERS REQUIRED

### 1. Form Submission Trigger

Type: Form Submission
Form ID: rdc-inquiry-form (or Webflow native form)
Event Name: sss_form_submit

Fires on: form submit success
Data layer push (from rose-day-club.js):
```
{
  event: "sss_form_submit",
  page_name: "rose-day-club",
  experience: "Rose Day Club",
  form_id: "rdc-inquiry-form"
}
```

### 2. CTA Click Trigger

Type: Click
Condition: Click on .rdc-btn elements
Event Name: sss_cta_click

Data layer push:
```
{
  event: "sss_cta_click",
  page_name: "rose-day-club",
  cta_text: {{Click Text}},
  cta_location: {{Click Classes}}
}
```

### 3. Scroll Depth Trigger

Type: Scroll Depth
Thresholds: 25%, 50%, 75%, 90%
Event Name: sss_scroll_depth

Parameters:
- page_name: "rose-day-club"
- scroll_depth: {{Scroll Depth Threshold}}

### 4. FAQ Interaction Trigger

Type: Click
Condition: Click on .rdc-accordion__trigger
Event Name: sss_faq_open

Parameters:
- page_name: "rose-day-club"
- question_text: {{Click Text}} (trimmed)

---

## UTM PARAMETER CAPTURE

Script: rose-day-club.js populateHiddenFields()
Storage: sessionStorage (persists across page navigations within session)

Parameters captured:
- utm_source
- utm_medium
- utm_campaign
- utm_content
- utm_term

All UTM parameters are also passed through the Webflow form as hidden fields to Airtable, enabling offline conversion attribution.

---

## CONVERSION FUNNEL

Primary conversion: sss_form_submit (Rose Day Club Inquiry)

Micro-conversions (leading indicators):
1. Hero CTA click (sss_cta_click, hero section)
2. Inclusions section view (scroll to 50%)
3. Testimonials section view (scroll to 75%)
4. Inquiry section view (scroll to 85%)
5. Form field interaction (any field focus)
6. Form submission (sss_form_submit)

---

## CAMPAIGN URL STRUCTURE

For paid or owned campaigns pointing to this page, use:

```
https://shesaidsail.com/experience/rose-day-club/?utm_source={source}&utm_medium={medium}&utm_campaign={campaign}&utm_content={content}
```

Examples:
- Instagram Organic: utm_source=instagram&utm_medium=social_organic&utm_campaign=rose-day-club
- Instagram Paid: utm_source=instagram&utm_medium=paid_social&utm_campaign=rose-day-club-ads
- Email: utm_source=email&utm_medium=email&utm_campaign=rose-day-club-launch
- Google: utm_source=google&utm_medium=cpc&utm_campaign=sss-rose-day-club

---

## REPORTING DIMENSIONS

In GA4 / Looker Studio, segment by:

- page_name = "rose-day-club" (isolate this page's traffic)
- utm_source (channel attribution)
- utm_campaign (campaign attribution)
- session_default_channel_group (GA4 default channel)

---

## KEY METRICS TO MONITOR

| Metric | Target | Alert Threshold |
|--------|--------|-----------------|
| Conversion rate (form submits / sessions) | 3-6% | Below 1.5% |
| Bounce rate | Below 55% | Above 75% |
| Time on page | 2min+ | Below 45sec |
| Scroll depth 75% | 30%+ of visitors | Below 15% |
| CTA click rate | 8-15% of page views | Below 4% |

---

## VERIFICATION STEPS

Before launch:
- [ ] GTM container loads without errors (check browser console)
- [ ] GA4 pageview fires on page load (check GA4 DebugView)
- [ ] Test form submission triggers sss_form_submit event (GTM preview mode)
- [ ] CTA click triggers sss_cta_click event (GTM preview mode)
- [ ] UTM params captured in hidden fields (inspect form with DevTools)
- [ ] UTM params visible in GA4 session source/medium (DebugView)
- [ ] No duplicate GA4 pageviews (verify single fire)
