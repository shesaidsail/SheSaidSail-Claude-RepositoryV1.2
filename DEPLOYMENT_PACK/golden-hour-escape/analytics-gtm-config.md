# GOLDEN HOUR ESCAPE — GTM CONFIGURATION GUIDE
Version: 1.0 | Date: May 2026

---

## GTM CONTAINER

Configure these tags, triggers, and variables in the She Said Sail GTM container.

---

## VARIABLES TO CREATE

### Built-In Variables (enable these if not already enabled)
- Page URL
- Page Path
- Referrer
- Scroll Depth Threshold
- Scroll Depth Units

### Data Layer Variables
Create these as Data Layer Variable type:

| Variable Name | Data Layer Variable Name | Default Value |
|--------------|--------------------------|---------------|
| DLV - Experience Name | experience_name | (not set) |
| DLV - Form ID | form_id | (not set) |
| DLV - Guest Count | guest_count | (not set) |
| DLV - Occasion | occasion | (not set) |
| DLV - Has Date | has_date | (not set) |
| DLV - UTM Source | utm_source | (not set) |
| DLV - UTM Medium | utm_medium | (not set) |
| DLV - UTM Campaign | utm_campaign | (not set) |
| DLV - CTA Location | cta_location | (not set) |
| DLV - Scroll Depth | scroll_depth | 0 |

---

## TRIGGERS TO CREATE

| Trigger Name | Type | Condition |
|-------------|------|-----------|
| TR - GHE Page View | Custom Event | Event equals `sss_page_view` |
| TR - GHE Form Start | Custom Event | Event equals `sss_form_start` |
| TR - GHE Form Submit | Custom Event | Event equals `sss_form_submit` |
| TR - GHE CTA Click | Custom Event | Event equals `sss_cta_click` |
| TR - GHE Scroll 25 | Custom Event | Event equals `sss_scroll_depth_25` |
| TR - GHE Scroll 50 | Custom Event | Event equals `sss_scroll_depth_50` |
| TR - GHE Scroll 75 | Custom Event | Event equals `sss_scroll_depth_75` |
| TR - GHE Section View | Custom Event | Event equals `sss_section_view` |

---

## TAGS TO CREATE

### Tag 1: GA4 - Experience Page View
- **Type:** Google Analytics: GA4 Event
- **Measurement ID:** (your GA4 property ID)
- **Event Name:** experience_page_view
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - page_location: {{Page URL}}
  - utm_source: {{DLV - UTM Source}}
  - utm_medium: {{DLV - UTM Medium}}
  - utm_campaign: {{DLV - UTM Campaign}}
- **Trigger:** TR - GHE Page View

### Tag 2: GA4 - Form Start
- **Type:** Google Analytics: GA4 Event
- **Event Name:** form_start
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - form_id: {{DLV - Form ID}}
- **Trigger:** TR - GHE Form Start

### Tag 3: GA4 - Form Submit (Lead)
- **Type:** Google Analytics: GA4 Event
- **Event Name:** generate_lead
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - form_id: {{DLV - Form ID}}
  - guest_count: {{DLV - Guest Count}}
  - occasion: {{DLV - Occasion}}
  - has_date: {{DLV - Has Date}}
  - utm_source: {{DLV - UTM Source}}
  - utm_medium: {{DLV - UTM Medium}}
  - utm_campaign: {{DLV - UTM Campaign}}
- **Trigger:** TR - GHE Form Submit

### Tag 4: GA4 - CTA Click
- **Type:** Google Analytics: GA4 Event
- **Event Name:** cta_click
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - cta_location: {{DLV - CTA Location}}
- **Trigger:** TR - GHE CTA Click

### Tag 5: GA4 - Scroll Depth
- **Type:** Google Analytics: GA4 Event
- **Event Name:** scroll
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - percent_scrolled: {{DLV - Scroll Depth}}
- **Trigger:** TR - GHE Scroll 50 OR TR - GHE Scroll 75

### Tag 6: GA4 - Section View
- **Type:** Google Analytics: GA4 Event
- **Event Name:** section_view
- **Parameters:**
  - experience_name: {{DLV - Experience Name}}
  - section_name: {{Event Label}} (use built-in Event Label variable)
- **Trigger:** TR - GHE Section View

---

## META ADS / PAID SOCIAL (Optional)

If running Meta/Instagram campaigns:

### Tag 7: Meta Pixel - PageView
- Fire on all pages (global tag, already exists)

### Tag 8: Meta Pixel - Lead Event
- **Type:** Custom HTML
- **HTML:**
```html
<script>
fbq('track', 'Lead', {
  content_name: 'Golden Hour Escape',
  content_category: 'Experience Page',
  currency: 'USD'
});
</script>
```
- **Trigger:** TR - GHE Form Submit

---

## CONVERSION EVENT FOR META ADS

When running Instagram/Facebook ads for Golden Hour Escape:
- UTM parameters: `utm_source=instagram&utm_medium=paid_social&utm_campaign=golden-hour-escape`
- Conversion event: `generate_lead` in GA4
- Meta Pixel event: `Lead`

---

## QA VERIFICATION

After implementing:

1. Enable GTM Preview Mode
2. Navigate to the Golden Hour Escape page
3. Verify `sss_page_view` fires on page load
4. Click a CTA button - verify `sss_cta_click` fires
5. Click into a form field - verify `sss_form_start` fires
6. Submit the form - verify `sss_form_submit` fires with correct parameters
7. Scroll to 50% and 75% - verify scroll events fire
8. Check GA4 DebugView - confirm all events appear with correct parameters
