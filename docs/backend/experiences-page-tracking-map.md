# Experiences Page Backend Tracking Map

**Version:** 1.0
**Date:** 2026-05-18
**Branch:** claude/fix-experiences-page-EwvlD
**Status:** Ready for Airtable + Make.com implementation

---

## Overview

This document maps all data capture points on the Experiences page to their Airtable destination fields and Make.com automation triggers.

---

## Airtable Field Mapping

### Target Base: She Said Sail Operations
### Target Table: Leads / Booking Inquiries

| Page Event | Data Captured | Airtable Field | Field Type |
|---|---|---|---|
| Page load | UTM source | Lead Source (UTM) | Text |
| Page load | UTM medium | Lead Medium (UTM) | Text |
| Page load | UTM campaign | Lead Campaign (UTM) | Text |
| Page load | UTM content | Lead Content (UTM) | Text |
| Page load | Referrer URL | Referrer | URL |
| Experience card click | experience_key | Experience Interest | Single Select |
| Experience card click | experience_name | Experience Name | Text |
| Experience card click | click timestamp | Interest Timestamp | Date/Time |
| Explore Experience click | experience_slug | Experience Slug | Text |
| Request to Book click | originating_page | Originating Page | Text |
| Request to Book click | experience_interest | Pre-Selected Experience | Single Select |
| Form submission | All fields | Full Lead Record | Multiple |

### Single Select Options for Experience Interest

- monaco-social
- golden-hour-escape
- rose-day-club
- pink-palm-club
- undecided

### Originating Page Values

- experiences-page
- experiences-monaco
- experiences-golden-hour
- experiences-rose
- experiences-pink-palm

---

## Make.com Automation Readiness

### M-EXPERIENCE-CLICK-TRACKING

**Trigger:** Webhook from GTM (experience card click event)
**Payload:**
```json
{
  "event": "click_experience_card",
  "experience_key": "monaco-social",
  "experience_name": "Monaco Social",
  "originating_page": "experiences",
  "timestamp": "2026-05-18T14:22:00Z",
  "session_id": "abc123",
  "utm_source": "instagram",
  "utm_medium": "paid_social",
  "utm_campaign": "spring_2026"
}
```
**Action:** Write click event to Airtable Experience Interactions table
**Status:** Ready for Make.com scenario build

---

### M-REQUEST-ROUTER

**Trigger:** Webhook from Request to Book form submission
**Required fields:**
- experience_interest (pre-populated from sessionStorage)
- utm_source
- utm_campaign
- originating_page
- name, email, phone, event_date, group_size

**Routing Logic:**
1. If experience_interest = monaco-social OR golden-hour-escape: route to Premium Lead queue
2. If experience_interest = rose-day-club OR pink-palm-club: route to Standard Lead queue
3. If experience_interest = undecided: route to Concierge Recommendation queue

**Action:** Create Airtable Lead record, send confirmation email, notify concierge
**Status:** Ready for Make.com scenario build

---

### M-UTM-CAPTURE

**Trigger:** Page load on /experiences/ (fired via GTM)
**Payload:**
```json
{
  "event": "view_experiences_page",
  "page_path": "/experiences/",
  "utm_source": "",
  "utm_medium": "",
  "utm_campaign": "",
  "utm_content": "",
  "referrer": "",
  "session_start": "2026-05-18T14:20:00Z"
}
```
**Action:** Store session data in Airtable Session Log table
**Status:** Ready for Make.com scenario build

---

### M-BOOKING-INTENT-LOGGER

**Trigger:** Webhook when user clicks "Request to Book" from Experiences page
**Payload:**
```json
{
  "event": "click_request_to_book",
  "originating_page": "experiences",
  "experience_interest": "rose-day-club",
  "scroll_depth": 72,
  "time_on_page": 94,
  "utm_source": "instagram",
  "session_id": "abc123"
}
```
**Action:** Write intent record to Airtable, flag for concierge review if high-intent signals present
**Status:** Ready for Make.com scenario build

---

## Hidden Form Field Initialization

The following hidden fields should be present on the Request to Book form and pre-populated via JavaScript on page load:

```javascript
// On /experiences/ page load, store UTM and experience data
(function() {
  const params = new URLSearchParams(window.location.search);
  const session = {
    utm_source:    params.get('utm_source')    || sessionStorage.getItem('utm_source')    || '',
    utm_medium:    params.get('utm_medium')    || sessionStorage.getItem('utm_medium')    || '',
    utm_campaign:  params.get('utm_campaign')  || sessionStorage.getItem('utm_campaign')  || '',
    utm_content:   params.get('utm_content')   || sessionStorage.getItem('utm_content')   || '',
    referrer:      document.referrer           || sessionStorage.getItem('referrer')       || '',
    originating_page: 'experiences'
  };
  Object.keys(session).forEach(function(k) {
    if (session[k]) sessionStorage.setItem(k, session[k]);
  });
})();
```

### Card Click Handler (adds experience to session)

```javascript
document.querySelectorAll('[data-experience-key]').forEach(function(card) {
  card.addEventListener('click', function() {
    const key  = card.getAttribute('data-experience-key');
    const name = card.getAttribute('data-experience-name');
    sessionStorage.setItem('experience_interest', key);
    sessionStorage.setItem('experience_name', name);
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push({
      event: 'click_experience_card',
      experience_key:  key,
      experience_name: name,
      originating_page: 'experiences'
    });
  });
});
```

---

## Data Attributes Required on HTML Elements

| Element | Required Attribute | Value Example |
|---|---|---|
| Monaco Social card | data-experience-key | monaco-social |
| Monaco Social card | data-experience-name | Monaco Social |
| Monaco Social card | data-experience-slug | monaco-social |
| Golden Hour card | data-experience-key | golden-hour-escape |
| Golden Hour card | data-experience-name | Golden Hour Escape |
| Rose Day Club card | data-experience-key | rose-day-club |
| Rose Day Club card | data-experience-name | Rose Day Club |
| Pink Palm Club card | data-experience-key | pink-palm-club |
| Pink Palm Club card | data-experience-name | Pink Palm Club |
| All Explore buttons | data-track-click | explore-experience |
| Request to Book button | data-track-click | request-to-book |
| Get Recommendations CTA | data-track-click | get-recommendations |

---

## Airtable Tables Required

### Experience Interactions (new table)

| Field | Type | Notes |
|---|---|---|
| Interaction ID | Auto Number | |
| Experience Key | Single Select | monaco-social, golden-hour-escape, rose-day-club, pink-palm-club |
| Event Type | Single Select | view, click, explore, book |
| Session ID | Text | |
| UTM Source | Text | |
| UTM Campaign | Text | |
| Timestamp | Date/Time | |
| Page Path | Text | |
| Converted | Checkbox | |

### Session Log (new table)

| Field | Type | Notes |
|---|---|---|
| Session ID | Text | |
| Page | Text | /experiences/ |
| UTM Source | Text | |
| UTM Medium | Text | |
| UTM Campaign | Text | |
| Referrer | URL | |
| Session Start | Date/Time | |
| Scroll Depth Max | Number | Percentage |
| Time on Page | Number | Seconds |
| Experience Interest | Single Select | |
| Converted | Checkbox | |
