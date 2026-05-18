# She Said Sail: Global JS Intelligence Addendum
**Version:** 1.0
**Date:** May 2026
**Purpose:** Documents the two additions required to she-said-sail-global.js to support the intelligence layer.
**File to update:** DEPLOYMENT_PACK/02_GLOBAL_JS/she-said-sail-global.js

---

## ADDITION 1: Visitor ID Cookie (sss_vid)

**Where to add:** At the very beginning of the IIFE, before the UTM capture block (Section 1).

**What it does:** Generates a persistent first-party UUID cookie that identifies a browser across sessions. This allows Airtable records (Requests, Chatbot Conversations) to be joined at the visitor level, connecting pre-form behavior to form submissions and bookings.

**Cookie spec:**
- Name: sss_vid
- Value: UUID v4 (randomly generated)
- Expiry: 1 year from creation
- Path: /
- SameSite: Lax (no cross-site sending)
- HttpOnly: false (must be readable by JavaScript for form inclusion)

**Code to add:**

```javascript
// Section 0: Visitor ID
(function generateVisitorId() {
  function uuid4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      var v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  var existing = (document.cookie.match(/(?:^|;\s*)sss_vid=([^;]+)/) || [])[1];
  if (!existing) {
    var vid = uuid4();
    var exp = new Date();
    exp.setFullYear(exp.getFullYear() + 1);
    document.cookie = 'sss_vid=' + vid + '; expires=' + exp.toUTCString() + '; path=/; SameSite=Lax';
    window.__sssVid = vid;
  } else {
    window.__sssVid = existing;
  }
})();
```

**After adding this block:** The visitor ID is available globally as `window.__sssVid`.

---

## ADDITION 2: Include visitor_id in All Webhook Payloads

The visitor ID must be included in every payload sent to Make.com webhooks. Add `visitor_id: window.__sssVid || ''` to the payload object in each of these locations in she-said-sail-global.js:

### Request to Book form payload

Find the payload object in the booking form submit handler. Add:
```javascript
visitor_id: window.__sssVid || '',
```

### Email capture form payload

Find the email capture payload. Add:
```javascript
visitor_id: window.__sssVid || '',
```

### Chatbot handoff payload (chatbot-js.js)

In DEPLOYMENT_PACK/chatbot/chatbot-js.js, find the fireWebhook() function and its payload. The chatbot payload already goes to M-CHATBOT-001. Add:
```javascript
visitor_id: window.__sssVid || '',
```

### Contact form payload (contact-html-snippets.html)

In DEPLOYMENT_PACK/pages/contact/contact-html-snippets.html, find the contact form submit handler and add:
```javascript
visitor_id: window.__sssVid || '',
```

---

## AIRTABLE FIELD ADDITIONS

After making the JS changes above, add these fields to the existing Airtable tables:

**UTMs table:**
Add field: Visitor ID (Short Text). Map from the visitor_id in the webhook payload.

**Chatbot Conversations table** (new table, already documented in intelligence-tables.md):
The Visitor ID field is already specified in the new table definition.

---

## MAKE.COM SCENARIO UPDATES

After adding visitor_id to all payloads:

**M-WEBFORM-001:** In Step 8 (Airtable: Create a Record in UTMs), add the Visitor ID field mapping: `visitor_id: {{1.visitor_id}}`.

**M-CHATBOT-001:** In the Airtable Create Record module (Chatbot Conversations table), add: `visitor_id: {{1.visitor_id}}`.

**M-EMAIL-CAPTURE-001:** No Visitor ID tracking needed on the email capture form (the user hasn't submitted an inquiry yet and there is no UTM record to link). Skip this one.

---

## PRIVACY NOTES

- The sss_vid cookie contains a randomly generated UUID with no PII.
- It is a first-party cookie (set by shesaidsail.com, not a third party).
- It is used only for internal analytics (Airtable record joining). It is not shared with ad platforms.
- It expires after 1 year unless cleared by the user.
- It should be disclosed in the She Said Sail privacy policy as: "We use a first-party cookie to recognize returning visitors for internal analytics purposes. This cookie does not contain personally identifiable information."
- It does not require consent under most interpretations of GDPR for strictly necessary analytics, but adding disclosure to the privacy policy is recommended.
