# Experiences Page Analytics Events

**Version:** 1.0
**Date:** 2026-05-18
**Branch:** claude/fix-experiences-page-EwvlD
**Status:** Ready for GTM implementation

---

## Event Schema Overview

All events follow GA4 naming convention. Events push to window.dataLayer for GTM processing, which distributes to GA4, Meta Pixel, and TikTok Pixel via GTM tags.

---

## Required Events

### view_experiences_page

**Trigger:** Page load on /experiences/
**Method:** GTM Page View trigger or custom event
**GA4 event name:** view_experiences_page

```javascript
window.dataLayer.push({
  event: 'view_experiences_page',
  page_location: window.location.href,
  page_path: '/experiences/',
  utm_source:   new URLSearchParams(window.location.search).get('utm_source')   || '',
  utm_medium:   new URLSearchParams(window.location.search).get('utm_medium')   || '',
  utm_campaign: new URLSearchParams(window.location.search).get('utm_campaign') || '',
  referrer:     document.referrer || ''
});
```

---

### click_experience_card

**Trigger:** Click on any experience card container
**GA4 event name:** click_experience_card
**Meta Pixel event:** ViewContent (with content_name)
**TikTok Pixel event:** ViewContent

```javascript
window.dataLayer.push({
  event: 'click_experience_card',
  experience_key:   'monaco-social',
  experience_name:  'Monaco Social',
  originating_page: 'experiences',
  click_position:   'featured'
});
```

**Parameters:**
- experience_key: string (monaco-social | golden-hour-escape | rose-day-club | pink-palm-club)
- experience_name: string (human readable)
- originating_page: string (experiences)
- click_position: string (featured | grid)

---

### click_explore_experience

**Trigger:** Click on "Explore This Experience" button
**GA4 event name:** click_explore_experience

```javascript
window.dataLayer.push({
  event: 'click_explore_experience',
  experience_key:  'monaco-social',
  experience_name: 'Monaco Social',
  destination_url: 'https://shesaidsail.com/experience/monaco-social/'
});
```

---

### click_request_to_book

**Trigger:** Click on "Request to Book" button or link from Experiences page
**GA4 event name:** click_request_to_book
**Meta Pixel event:** InitiateCheckout
**TikTok Pixel event:** InitiateCheckout

```javascript
window.dataLayer.push({
  event: 'click_request_to_book',
  originating_page:     'experiences',
  experience_interest:  sessionStorage.getItem('experience_interest') || 'undecided',
  destination_url:      'https://shesaidsail.com/request-to-book/'
});
```

---

### click_get_recommendations

**Trigger:** Click on "Get Recommendations" Tidio chat button
**GA4 event name:** click_get_recommendations

```javascript
window.dataLayer.push({
  event: 'click_get_recommendations',
  originating_page: 'experiences',
  experience_interest: sessionStorage.getItem('experience_interest') || 'undecided'
});
```

---

### scroll_50_percent

**Trigger:** User scrolls past 50% of page height
**GA4 event name:** scroll_50_percent
**Method:** GTM Scroll Depth trigger (50% threshold) OR custom scroll listener

```javascript
window.dataLayer.push({
  event: 'scroll_50_percent',
  page_path: '/experiences/'
});
```

---

### scroll_90_percent

**Trigger:** User scrolls past 90% of page height
**GA4 event name:** scroll_90_percent

```javascript
window.dataLayer.push({
  event: 'scroll_90_percent',
  page_path: '/experiences/',
  experience_interest: sessionStorage.getItem('experience_interest') || 'none'
});
```

---

## GTM Tag Configuration

### GA4 Configuration Tag
- Measurement ID: GT-WV3X86GZ (from existing page source)
- Enhanced measurement: on
- Custom events: all above events forwarded

### Meta Pixel Tag
- Event: ViewContent on click_experience_card
- Event: InitiateCheckout on click_request_to_book
- Parameters: content_name = experience_name

### TikTok Pixel Tag
- Event: ViewContent on click_experience_card
- Event: InitiateCheckout on click_request_to_book

### GTM Trigger: Scroll Depth
- Depth threshold: 50% and 90%
- Page: /experiences/

---

## GTM Variables Required

| Variable Name | Type | Value |
|---|---|---|
| DLV - experience_key | Data Layer Variable | experience_key |
| DLV - experience_name | Data Layer Variable | experience_name |
| DLV - originating_page | Data Layer Variable | originating_page |
| DLV - experience_interest | Data Layer Variable | experience_interest |
| DLV - utm_source | Data Layer Variable | utm_source |
| DLV - utm_campaign | Data Layer Variable | utm_campaign |

---

## Full GTM Implementation Script

The following script block should be added via GTM Custom HTML tag, firing on Page View for /experiences/:

```javascript
(function() {
  'use strict';

  // UTM capture and storage
  var params = new URLSearchParams(window.location.search);
  var utmKeys = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term'];
  utmKeys.forEach(function(k) {
    var v = params.get(k);
    if (v) sessionStorage.setItem(k, v);
  });
  if (document.referrer && !sessionStorage.getItem('referrer')) {
    sessionStorage.setItem('referrer', document.referrer);
  }

  // Page view event
  window.dataLayer = window.dataLayer || [];
  window.dataLayer.push({
    event: 'view_experiences_page',
    page_path: '/experiences/',
    utm_source:   sessionStorage.getItem('utm_source')   || '',
    utm_medium:   sessionStorage.getItem('utm_medium')   || '',
    utm_campaign: sessionStorage.getItem('utm_campaign') || '',
    referrer:     sessionStorage.getItem('referrer')     || ''
  });

  // Experience card click tracking
  document.addEventListener('click', function(e) {
    var card = e.target.closest('[data-experience-key]');
    if (!card) return;
    var key  = card.getAttribute('data-experience-key');
    var name = card.getAttribute('data-experience-name');
    var pos  = card.getAttribute('data-experience-position') || 'grid';
    sessionStorage.setItem('experience_interest', key);
    sessionStorage.setItem('experience_name', name);
    window.dataLayer.push({
      event:            'click_experience_card',
      experience_key:   key,
      experience_name:  name,
      originating_page: 'experiences',
      click_position:   pos
    });
  });

  // Explore Experience button tracking
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-track-click="explore-experience"]');
    if (!btn) return;
    var card = btn.closest('[data-experience-key]');
    var key  = card ? card.getAttribute('data-experience-key') : '';
    var name = card ? card.getAttribute('data-experience-name') : '';
    window.dataLayer.push({
      event:           'click_explore_experience',
      experience_key:  key,
      experience_name: name
    });
  });

  // Request to Book tracking
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-track-click="request-to-book"]');
    if (!btn) return;
    window.dataLayer.push({
      event:                'click_request_to_book',
      originating_page:     'experiences',
      experience_interest:  sessionStorage.getItem('experience_interest') || 'undecided'
    });
  });

  // Get Recommendations tracking
  document.addEventListener('click', function(e) {
    var btn = e.target.closest('[data-track-click="get-recommendations"]');
    if (!btn) return;
    window.dataLayer.push({
      event:               'click_get_recommendations',
      originating_page:    'experiences',
      experience_interest: sessionStorage.getItem('experience_interest') || 'undecided'
    });
  });

  // Scroll depth tracking
  var scrollFired = { 50: false, 90: false };
  window.addEventListener('scroll', function() {
    var scrollPct = Math.round(
      (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100
    );
    if (!scrollFired[50] && scrollPct >= 50) {
      scrollFired[50] = true;
      window.dataLayer.push({ event: 'scroll_50_percent', page_path: '/experiences/' });
    }
    if (!scrollFired[90] && scrollPct >= 90) {
      scrollFired[90] = true;
      window.dataLayer.push({
        event:               'scroll_90_percent',
        page_path:           '/experiences/',
        experience_interest: sessionStorage.getItem('experience_interest') || 'none'
      });
    }
  }, { passive: true });

})();
```

---

## GA4 Conversion Events

Mark the following as conversion events in GA4:
- click_request_to_book
- click_explore_experience (secondary)

---

## Meta Pixel Custom Conversions

Create a custom conversion for:
- Event: InitiateCheckout
- Rule: Page URL contains /experiences/
- Name: "Experiences Page Booking Intent"
