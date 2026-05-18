# She Said Sail: Hidden Form Fields Specification

This document tells a developer exactly what hidden fields to add to the Request to Book form, what populates each field, and how to configure them in MetForm (WordPress).

---

## Overview

The form has two categories of fields:
1. Visible fields (Name, Email, Phone, etc.) that the user fills in
2. Hidden fields (UTMs, tracking, brand identifiers) that JavaScript populates automatically before submission

All hidden fields must be present in the form DOM before the form submits. The `populateHiddenFields()` function reads from `sessionStorage`, URL parameters, and `document.referrer` to fill them.

---

## Hidden Field Reference Table

| Field Name (HTML `name` attribute) | Source | Default / Fallback |
|---|---|---|
| `utm_source` | URL param `?utm_source=` | `"direct"` |
| `utm_medium` | URL param `?utm_medium=` | `"none"` |
| `utm_campaign` | URL param `?utm_campaign=` | `""` |
| `utm_content` | URL param `?utm_content=` | `""` |
| `utm_term` | URL param `?utm_term=` | `""` |
| `creative_id` | URL param `?creative_id=` | `""` |
| `landing_page` | `sessionStorage.sss_landing_page` | `window.location.href` |
| `source_url` | `window.location.href` at form load | `window.location.href` |
| `referrer_url` | `sessionStorage.sss_referrer` | `document.referrer` |
| `first_seen_at` | `sessionStorage.sss_first_seen_at` | current ISO timestamp |
| `submission_page` | `window.location.pathname` | `"/request-to-book/"` |
| `brand` | Hard-coded | `"shesaidsail"` |
| `service_category` | Hard-coded | `"yacht-charter"` |
| `selected_experience` | URL param `?experience=` | `""` |

---

## JavaScript: populateHiddenFields() Function

Paste this function into `she-said-sail-global.js` or into a separate inline script block. It must be called after DOM ready and before the form submits.

```javascript
function populateHiddenFields() {
  // Parse URL parameters
  var params = new URLSearchParams(window.location.search);

  function getParam(key, fallback) {
    var val = params.get(key);
    return (val !== null && val !== '') ? val : (fallback || '');
  }

  // Read sessionStorage values set by the global tracking init
  function getSession(key, fallback) {
    try {
      var val = sessionStorage.getItem(key);
      return val ? val : (fallback || '');
    } catch (e) {
      return fallback || '';
    }
  }

  // Map of field name -> value to set
  var fieldValues = {
    'utm_source':       getParam('utm_source', getSession('sss_utm_source', 'direct')),
    'utm_medium':       getParam('utm_medium', getSession('sss_utm_medium', 'none')),
    'utm_campaign':     getParam('utm_campaign', getSession('sss_utm_campaign', '')),
    'utm_content':      getParam('utm_content', getSession('sss_utm_content', '')),
    'utm_term':         getParam('utm_term', getSession('sss_utm_term', '')),
    'creative_id':      getParam('creative_id', getSession('sss_creative_id', '')),
    'landing_page':     getSession('sss_landing_page', window.location.href),
    'source_url':       window.location.href,
    'referrer_url':     getSession('sss_referrer', document.referrer),
    'first_seen_at':    getSession('sss_first_seen_at', new Date().toISOString()),
    'submission_page':  window.location.pathname,
    'brand':            'shesaidsail',
    'service_category': 'yacht-charter',
    'selected_experience': getParam('experience', '')
  };

  // Set each hidden field value in the form
  Object.keys(fieldValues).forEach(function(fieldName) {
    var inputs = document.querySelectorAll('input[name="' + fieldName + '"]');
    inputs.forEach(function(input) {
      input.value = fieldValues[fieldName];
    });
  });
}
```

**When to call this function:**

Call it in two places so the fields are always populated:

1. On DOM ready (in case the user lands directly on the page):
```javascript
document.addEventListener('DOMContentLoaded', function() {
  populateHiddenFields();
});
```

2. Immediately before form submission (catches any race conditions):
```javascript
var form = document.querySelector('.mf-form'); // adjust selector to match MetForm output
if (form) {
  form.addEventListener('submit', function() {
    populateHiddenFields();
  }, true); // useCapture: true ensures this fires before MetForm's own submit handler
}
```

---

## MetForm: Step-by-Step Instructions for Adding Hidden Fields

MetForm is the WordPress form plugin used for the Request to Book form. Follow these steps to add each hidden field.

**Prerequisite:** You must have the MetForm plugin installed and the Request to Book form already created with its visible fields.

### Step 1: Open the form in Elementor

1. Log in to WordPress admin.
2. Go to MetForm > Forms.
3. Find the Request to Book form and click Edit.
4. The form opens inside the Elementor editor.

### Step 2: Add a Hidden Field element

1. In the Elementor panel (left sidebar), search for "Hidden" in the widget search bar.
2. Drag the MetForm "Hidden Field" widget into the form container. Position does not matter visually since it will not be visible, but place it below the last visible field for organizational clarity.

### Step 3: Configure each hidden field

For each field in the table above, repeat the following:

1. Click the Hidden Field widget you just added.
2. In the left panel, set:
   - **Field Label:** Use the field name (e.g., "utm_source"). This is for your reference only.
   - **Field Name:** This is the HTML `name` attribute. Set it exactly as shown in the Field Name column above (e.g., `utm_source`). Do not use spaces or capital letters.
   - **Default Value:** Leave blank. JavaScript will populate it.
   - **Required:** Leave unchecked.
3. Click Update to save.
4. Repeat: drag another Hidden Field widget for the next field.

You need 14 hidden field widgets total.

### Step 4: Verify the fields are in the DOM

1. After saving and publishing, open the Request to Book page in your browser.
2. Right-click anywhere on the page and choose Inspect (or open DevTools with F12).
3. In the Elements tab, search for `type="hidden"` or the field name `utm_source`.
4. Confirm you see 14 hidden input elements with the correct `name` attributes.

### Step 5: Load the script and test

1. Confirm `she-said-sail-global.js` is loaded in the page footer (see homepage-install-guide.md Step 2).
2. Open the page with test UTM params: `/request-to-book/?utm_source=test&utm_medium=cpc&utm_campaign=qa-test&creative_id=TEST-001`
3. Open DevTools Console and type: `populateHiddenFields()` then press Enter.
4. In the Elements tab, verify that the hidden input fields now show the correct values.

### Step 6: Submit a test and verify

Submit the form with test data. In Make.com, open the scenario run history and confirm the payload includes all 14 hidden field values alongside the visible form fields.

---

## Notes for Developers

- MetForm field names must match exactly. A field named `utm_source` in MetForm will appear in the Make.com payload as `utm_source`. Any mismatch will result in empty values in Airtable.
- If MetForm is replaced with a different form plugin (WPForms, Gravity Forms, Fluent Forms), the same hidden field names apply. Only the UI for adding them changes.
- The `populateHiddenFields()` function is idempotent. Calling it multiple times is safe and will not duplicate values.
- `sessionStorage` is cleared when the browser tab is closed. `first_seen_at` and `landing_page` are set once when the user first arrives and persisted in sessionStorage so they survive page navigation within the same session.
