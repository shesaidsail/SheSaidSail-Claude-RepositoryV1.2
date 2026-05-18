# She Said Sail: Chatbot Analytics Events
**Version:** 1.0
**Date:** May 2026

All GTM dataLayer events fired by chatbot-js.js. These extend the existing event architecture from DEPLOYMENT_PACK/07_GTM_ANALYTICS/gtm-events-map.md.

---

## EVENT REFERENCE TABLE

| Event Name | Trigger | Parameters | GTM Tag | Conversion? |
|---|---|---|---|---|
| chatbot_open | Widget opened (manual or auto) | page_location, trigger_type | GA4 Event | No |
| chatbot_start_conversation | First bot message displayed | page_location | GA4 Event | No |
| chatbot_select_occasion | Occasion detected from user input | occasion, page_location | GA4 Event | No |
| chatbot_select_experience | Experience recommended | experience_slug, occasion, page_location | GA4 Event | No |
| chatbot_capture_email | User submits valid email | page_location, experience_slug | GA4 Event | YES |
| chatbot_capture_phone | User submits phone number | page_location | GA4 Event | No |
| chatbot_handoff | Handoff message sent, webhook fired | experience_slug, occasion, has_email, page_location | GA4 Event + Meta Pixel + TikTok Pixel | YES |
| chatbot_complete | Conversation reaches STATE_CLOSED | experience_slug, occasion, page_location | GA4 Event | No |

---

## EVENT SPECIFICATIONS

### chatbot_open
```javascript
window.dataLayer.push({
  event: 'chatbot_open',
  trigger_type: 'manual', // or 'auto'
  page_location: window.location.href
});
```
Fires: every time the widget opens.
Use to track open rate relative to page visitors.

---

### chatbot_start_conversation
```javascript
window.dataLayer.push({
  event: 'chatbot_start_conversation',
  page_location: window.location.href
});
```
Fires: when the opener message is shown to the user (after the 800ms delay).
Use to distinguish opens (widget clicked) from conversations started (opener displayed).

---

### chatbot_select_occasion
```javascript
window.dataLayer.push({
  event: 'chatbot_select_occasion',
  occasion: 'bachelorette', // bachelorette | birthday | girls_trip | intimate | other
  page_location: window.location.href
});
```
Fires: when occasion is detected from user input or quick reply selection.
Use to segment chatbot traffic by occasion type in GA4 audiences.

---

### chatbot_select_experience
```javascript
window.dataLayer.push({
  event: 'chatbot_select_experience',
  experience_slug: 'monaco-social',
  occasion: 'bachelorette',
  page_location: window.location.href
});
```
Fires: when the bot recommends a specific experience (STATE_RECOMMENDATION).
Use to measure which experiences are most recommended and most pursued through the chatbot.

---

### chatbot_capture_email
```javascript
window.dataLayer.push({
  event: 'chatbot_capture_email',
  experience_slug: 'monaco-social',
  page_location: window.location.href
});
```
Fires: immediately after a valid email is submitted by the user.
Mark as GA4 Conversion: YES. This is the primary chatbot lead event.
Do not include the actual email address in the event (PII).

---

### chatbot_capture_phone
```javascript
window.dataLayer.push({
  event: 'chatbot_capture_phone',
  page_location: window.location.href
});
```
Fires: when user provides a phone number (optional step).
Not a conversion. Use to measure phone capture rate as a secondary metric.

---

### chatbot_handoff
```javascript
window.dataLayer.push({
  event: 'chatbot_handoff',
  experience_slug: 'monaco-social',
  occasion: 'bachelorette',
  has_email: true,
  page_location: window.location.href
});
```
Fires: when the handoff message is shown and the Make.com webhook fires.
Mark as GA4 Conversion: YES. This is the equivalent of a form submission from a chatbot conversation.
Also fire Meta Pixel Lead event and TikTok Pixel CompleteRegistration on this trigger (same as view_thank_you_page).

---

### chatbot_complete
```javascript
window.dataLayer.push({
  event: 'chatbot_complete',
  experience_slug: 'monaco-social',
  occasion: 'bachelorette',
  page_location: window.location.href
});
```
Fires: when the closing message is displayed (STATE_CLOSED).
Not a primary conversion. Use to measure full conversation completion rate.

---

## GTM SETUP REQUIRED

### New Data Layer Variables
Create these DLVs in GTM:

| DLV Name | Data Layer Variable | Type |
|---|---|---|
| dlv_chatbot_occasion | occasion | Data Layer Variable |
| dlv_chatbot_experience | experience_slug | Data Layer Variable |
| dlv_chatbot_trigger | trigger_type | Data Layer Variable |
| dlv_chatbot_has_email | has_email | Data Layer Variable |

### New Custom Event Triggers
Create one trigger per event:

| Trigger Name | Event Name |
|---|---|
| CE - chatbot_open | chatbot_open |
| CE - chatbot_start_conversation | chatbot_start_conversation |
| CE - chatbot_select_occasion | chatbot_select_occasion |
| CE - chatbot_select_experience | chatbot_select_experience |
| CE - chatbot_capture_email | chatbot_capture_email |
| CE - chatbot_handoff | chatbot_handoff |
| CE - chatbot_complete | chatbot_complete |

### New GA4 Event Tags

| Tag Name | Trigger | Event Name | Parameters |
|---|---|---|---|
| GA4 - chatbot_open | CE - chatbot_open | chatbot_open | page_location, dlv_chatbot_trigger |
| GA4 - chatbot_start_conversation | CE - chatbot_start_conversation | chatbot_start_conversation | page_location |
| GA4 - chatbot_select_occasion | CE - chatbot_select_occasion | chatbot_select_occasion | dlv_chatbot_occasion, page_location |
| GA4 - chatbot_select_experience | CE - chatbot_select_experience | chatbot_select_experience | dlv_chatbot_experience, dlv_chatbot_occasion, page_location |
| GA4 - chatbot_capture_email | CE - chatbot_capture_email | chatbot_capture_email | dlv_chatbot_experience, page_location |
| GA4 - chatbot_handoff | CE - chatbot_handoff | chatbot_handoff | dlv_chatbot_experience, dlv_chatbot_occasion, dlv_chatbot_has_email, page_location |
| GA4 - chatbot_complete | CE - chatbot_complete | chatbot_complete | dlv_chatbot_experience, dlv_chatbot_occasion, page_location |

### Pixel Tags for chatbot_handoff

**Meta Pixel (on CE - chatbot_handoff trigger):**
```html
<script>
fbq('track', 'Lead', {
  content_name: {{dlv_chatbot_experience}},
  content_category: 'chatbot_lead',
  value: 0,
  currency: 'USD'
});
</script>
```

**TikTok Pixel (on CE - chatbot_handoff trigger):**
```html
<script>
ttq.track('CompleteRegistration', {
  content_name: {{dlv_chatbot_experience}},
  content_type: 'chatbot_lead'
});
</script>
```

---

## GA4 AUDIENCES

**Chatbot Engaged (warm audience):**
Condition: chatbot_start_conversation fired
Membership duration: 30 days
Use: retarget people who started chatting but did not complete

**Chatbot Converted (suppression):**
Condition: chatbot_handoff fired
Membership duration: 90 days
Use: suppress from ads to avoid showing ads to people who already submitted

**Chatbot by Experience (experience-specific):**
Condition: chatbot_select_experience fired WHERE dlv_chatbot_experience = "[slug]"
Create one audience per experience
Membership duration: 30 days
Use: serve experience-specific ads to people who showed interest in that experience through the chatbot

---

## KEY METRICS TO MONITOR

| Metric | How to Measure |
|---|---|
| Open rate | chatbot_open / page_sessions |
| Conversation start rate | chatbot_start_conversation / chatbot_open |
| Occasion capture rate | chatbot_select_occasion / chatbot_start_conversation |
| Experience interest rate | chatbot_select_experience / chatbot_select_occasion |
| Email capture rate | chatbot_capture_email / chatbot_start_conversation |
| Handoff rate | chatbot_handoff / chatbot_start_conversation |
| Completion rate | chatbot_complete / chatbot_handoff |

Build a GA4 Exploration or Looker Studio report tracking these funnel steps.

---

## RELATIONSHIP TO EXISTING EVENTS

The existing `open_chat` event (fired by global JS via Tidio API) is replaced by `chatbot_open` for the new custom widget.

Once the custom widget is live and Tidio is hidden, the Tidio-based `open_chat` event will no longer fire. Update the GTM tag previously tied to `open_chat` to use `chatbot_open` instead. Do not create a duplicate tag.
