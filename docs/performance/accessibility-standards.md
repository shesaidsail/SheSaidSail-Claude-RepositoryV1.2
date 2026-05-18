# She Said Sail: Accessibility Standards

**Version:** 1.0
**Date:** 2026-05-18
**Conformance Target:** WCAG 2.1 Level AA
**Stack:** WordPress 6.9.4 + Elementor 4.0.3 + Hello Elementor theme

---

## WHY ACCESSIBILITY MATTERS FOR THIS BRAND

She Said Sail serves women planning meaningful celebrations: bachelorette parties, birthdays, proposals, and milestones that matter deeply. Guests arrive at this site from all walks of life, including women who navigate the web with a screen reader, a keyboard instead of a mouse, a screen magnifier, or reduced color sensitivity.

Accessibility is not a checkbox or a legal compliance exercise. A guest with a visual impairment, motor difficulty, or hearing sensitivity deserves the same warm, premium experience as any other guest. These standards ensure that warmth is available to everyone.

Every accessibility decision on She Said Sail should be made with that guest in mind. The standard is not "does it pass an audit." The standard is "can someone who cannot see the screen, or cannot use a mouse, or cannot perceive color differences, still book an experience and feel cared for."

---

## COLOR CONTRAST AUDIT

She Said Sail uses a defined color palette. Every text and background combination used on the site has been evaluated against WCAG 2.1 AA contrast requirements.

WCAG 2.1 AA contrast requirements:
- Normal text (under 18pt regular or under 14pt bold): minimum 4.5:1 ratio
- Large text (18pt or larger regular, or 14pt or larger bold): minimum 3:1 ratio
- Decorative text and logos: no requirement (but aim for legibility)

### Full Contrast Audit Table

| Text Color | Background Color | Contrast Ratio | Required Ratio | Status | Usage Rule |
|---|---|---|---|---|---|
| --sss-text (#2C2C2C) | --sss-cream (#FAF8F3) | 13.5:1 | 4.5:1 | PASS | Primary body text. No restrictions. |
| --sss-navy (#1A2332) | --sss-cream (#FAF8F3) | 14.2:1 | 4.5:1 | PASS | Header text, CTA labels on cream. No restrictions. |
| --sss-navy (#1A2332) | white (#FFFFFF) | 13.1:1 | 4.5:1 | PASS | Button labels on white. No restrictions. |
| White (#FFFFFF) | --sss-navy (#1A2332) | 13.1:1 | 4.5:1 | PASS | White text on navy backgrounds. No restrictions. |
| --sss-cream (#FAF8F3) | --sss-navy (#1A2332) | 12.9:1 | 4.5:1 | PASS | Cream text on navy sections. No restrictions. |
| --sss-gold (#DAB97E) | --sss-navy (#1A2332) | 3.1:1 | 3:1 (large text) | PASS for large text only | Use only for headings 18pt or larger, or purely decorative elements. Never use gold text on navy for body copy or small labels. |
| --sss-gold (#DAB97E) | white (#FFFFFF) | 2.3:1 | 4.5:1 | FAIL | Do not use gold text on white at any size for informational text. |
| --sss-muted (rgba(44,44,44,0.5)) | white (#FFFFFF) | approximately 3.5:1 | 4.5:1 | FAIL for normal text | See usage rule below. |
| --sss-muted (rgba(44,44,44,0.5)) | --sss-cream (#FAF8F3) | approximately 3.8:1 | 4.5:1 | BORDERLINE FAIL | See usage rule below. |

### Key Findings and Rules

**Gold (#DAB97E) rule:** Gold fails at normal body text size against all light backgrounds. Gold passes only for large text (18pt regular or 14pt bold) against navy. Gold is used on She Said Sail for decorative section dividers, eyebrow labels, and accent marks. Verify that every use of gold text in the final implementation is either large enough to pass or is purely decorative (no information conveyed).

**Muted color rule:** `--sss-muted` (approximately 50% opacity on #2C2C2C) is used for secondary labels and eyebrow text. Against white or cream, it achieves approximately 3.5 to 3.8:1, which fails the 4.5:1 requirement for normal text. This color may only be used for:
- Text that is 18pt (24px) regular or larger, OR
- Text that is 14pt (approximately 18.67px) bold or larger, OR
- Purely decorative text where the information is also conveyed through another element

If any muted-color text is below these size thresholds and is carrying informational content, it must be replaced with `--sss-text (#2C2C2C)`.

**Action required in implementation:** Audit every page for gold text on non-navy backgrounds and muted text below 18pt. This audit should be completed before the Lighthouse accessibility audit.

---

## HEADING HIERARCHY STANDARD

Screen readers and assistive technologies use heading structure to let users navigate a page quickly. A user might jump from heading to heading to find the section they want. Skipping heading levels (for example, placing an H3 directly under an H1) breaks this navigation and confuses the document outline.

### Rules

- One H1 per page. The H1 is the primary title or hero headline.
- H2 for major section headings.
- H3 for sub-sections within H2 sections.
- Never skip a heading level. No H1 to H3 jumps. No H2 to H4 jumps.
- Do not choose heading levels for their visual appearance. Use CSS classes to control size. If a design calls for a large visual label that is not structurally a heading, use a `<p>` or `<span>` with a CSS class, not a heading element.

### Page-by-Page Heading Structure

**Homepage:**
- H1: Hero headline (the primary brand statement visible above the fold)
- H2: Major section headings ("The Experiences," "How It Works," "What Guests Say")
- H3: Individual experience card titles, individual testimonial attribution headings (if styled as headings)

**Experience Detail Pages (one per sailing experience):**
- H1: Experience name (for example, "The Bachelorette Sail")
- H2: Section headings within the page ("What's Included," "How to Book," "Frequently Asked Questions")
- H3: Sub-section headings within any H2 section

**FAQ Page:**
- H1: Page headline ("Everything you want to know." or equivalent)
- H2: Category headings (if FAQ is organized into categories such as "Booking," "What to Expect," "Policies")
- H3: Individual question headings (if individual questions are marked up as headings rather than plain text within an accordion)

**About Page:**
- H1: Primary headline ("About She Said Sail" or the brand story opening line)
- H2: Section headings within the about narrative

**Elementor note:** Elementor allows selecting heading level (H1 through H6) independently of visual size. Always match the heading level to the structural position in the document, not to the desired visual size. Use Elementor's typography settings to control font size separately.

### Verification

Use the HeadingsMap browser extension (available for Chrome and Firefox) to inspect the heading structure of any page. The extension displays the full heading outline and flags skipped levels. Run this check on every page type before launch.

---

## KEYBOARD NAVIGATION STANDARD

Every interactive element on She Said Sail must be operable without a mouse. This includes all navigation links, buttons, form fields, the chatbot, and any interactive Elementor widgets.

### Required Keyboard Behaviors

| Key | Expected Behavior |
|---|---|
| Tab | Moves focus forward through all interactive elements in document order |
| Shift + Tab | Moves focus backward through interactive elements |
| Enter | Activates a focused link or button |
| Space | Activates a focused button (not a link). Also scrolls the page when no interactive element is focused. |
| Escape | Closes open modals, dialogs, and panels (including the chatbot panel) |
| Arrow keys | Navigates within a radio group, select dropdown, or custom listbox |

### Focus Order

Focus must follow a logical sequence: left to right within a row, top to bottom down the page, consistent with the visual layout. Focus must never disappear (jump to an invisible element), skip visible interactive elements, or cycle to the browser address bar unexpectedly.

### Testing Keyboard Navigation

Before launch, navigate each key page entirely using only the keyboard:
1. Reload the page.
2. Press Tab to move through every interactive element.
3. Verify that every link, button, and form field can be reached.
4. Verify that focus order matches visual layout.
5. Activate each interactive element using Enter or Space.
6. Open and close the chatbot using keyboard only.
7. Submit or close any open forms or modals using keyboard only.

If any interactive element cannot be reached or activated by keyboard, it is a WCAG failure that must be fixed before launch.

---

## FOCUS INDICATOR STANDARD

A visible focus indicator is required by WCAG 2.1 AA (Success Criterion 2.4.7). Sighted keyboard users depend on the focus ring to know which element currently has focus. Without a visible focus indicator, keyboard navigation is effectively impossible.

### The Problem with Default WordPress and Elementor Styles

Hello Elementor theme and Elementor widgets frequently suppress the browser's default focus outline using:
```css
:focus { outline: none; }
```
or
```css
* { outline: none; }
```
These rules are WCAG violations. They must be identified and overridden.

### Required Focus Style

Add the following to `she-said-sail-global.css`. This replaces the suppressed outline with a gold focus ring that is visible, on-brand, and accessible:

```css
:focus-visible {
  outline: 2px solid var(--sss-gold);
  outline-offset: 3px;
  border-radius: 2px;
}
```

Using `:focus-visible` instead of `:focus` means the gold ring appears only for keyboard focus, not for mouse clicks. This prevents the focus ring from appearing when a user clicks a button (which would feel visually noisy), while still displaying it for keyboard users who need it.

### Audit Steps

1. Open Chrome DevTools.
2. Search in the Styles panel for `outline: none` and `outline: 0`.
3. Identify which stylesheet and selector is suppressing the outline.
4. Verify that the `:focus-visible` override in `she-said-sail-global.css` is loaded after the suppressing stylesheet.
5. Tab through the page and visually confirm the gold ring appears on every focused element.

### Special Cases

**Chatbot toggle button:** Must show focus indicator when focused via keyboard. The toggle button is 56x56px with `border-radius: 50%`. The focus style should use `outline-offset: 4px` to visually clear the circular button edge.

**Form submit button:** Must show focus indicator. The CTA button style (navy background, cream text) should show the gold outline against the navy background, which is visible at 3.1:1 against navy (acceptable for the outline itself, which is a non-text UI component requiring only 3:1).

**Quick reply buttons in chatbot:** Must show focus indicator. The gold outline against the cream or white button background is clearly visible.

---

## ALT TEXT STANDARD

Every image on every She Said Sail page must have an `alt` attribute. The value of that attribute must be appropriate to the image's purpose.

### Rules for Writing Alt Text

**Descriptive images (photos, experience images, people):**
- Describe what is shown in the image as you would to someone who cannot see it.
- Include the context that matters: location, activity, subject.
- Do not begin alt text with "Image of" or "Photo of." Screen readers already announce that it is an image.
- Good example: `alt="A private sailing yacht anchored near a sandbar in Biscayne Bay, Miami, with three women on the deck"`
- Poor example: `alt="luxury yacht experience"`

**Experience images:**
- Include the experience name and the visual content where relevant.
- Good example: `alt="Guests on the She Said Sail Bachelorette Sail, toasting champagne on a white catamaran at sunset"`

**Logo:**
- Always: `alt="She Said Sail"`
- This is enforced by the global JavaScript which sets the alt attribute on the logo image on load. Verify the inline HTML also has this attribute set correctly in Elementor.

**Decorative images:**
- Images that are purely decorative (background textures, dividers, abstract shapes) and carry no informational content should use `alt=""` (empty string). This tells screen readers to skip the image entirely.
- Never omit the `alt` attribute entirely. Missing `alt` causes screen readers to announce the file name, which is disruptive.

**Icons used as buttons:**
- If an icon-only button has no visible text label, it must have either an `aria-label` or a visually-hidden text element inside it.
- The chatbot close button (X) must have `aria-label="Close chat"` or contain visually-hidden text "Close chat."

### Audit

Run the Lighthouse Accessibility audit (Chrome DevTools > Lighthouse > Accessibility). It will flag images with missing or empty alt attributes. Also run axe DevTools browser extension for a more detailed scan.

---

## FORM ACCESSIBILITY STANDARD

Every visible form input must have an associated label that is programmatically linked to it. This allows screen readers to announce the field name when the user focuses on the input.

### Requirements for Every Form Field

1. A `<label>` element with a `for` attribute matching the input's `id`, OR
2. An `aria-label` attribute on the input itself, OR
3. An `aria-labelledby` attribute pointing to another element's `id` that serves as the label

Placeholder text does not satisfy this requirement. Placeholder text disappears when the user starts typing and is not consistently announced by screen readers. Every input with a placeholder must also have a real label.

### Required Field Indicators

Required fields must be indicated both:
- Visually: with an asterisk (*) or the word "required" near the field label
- Programmatically: with `aria-required="true"` on the `<input>` element

### Error Messages

When a field has a validation error, the error message must be:
- Visible and in close proximity to the field
- Associated with the field via `aria-describedby` so screen readers announce it
- Descriptive: "Please enter a valid email address" rather than "Invalid input"

### Request to Book Form

The Request to Book form is rendered via Elementor's form widget. Elementor's form widget generates `<label>` elements by default, but verify the rendered HTML to confirm. Open the page, inspect the form HTML, and check that each `<input>` has either a `<label for="">` pointing to its `id`, or an `aria-label`.

Hidden fields (`utm_source`, `utm_medium`, `utm_campaign`, `utm_content`, `utm_term`, `form_page`) are not user-visible and do not require labels.

### Chatbot Input Field

The chatbot message input must have an associated label. Options:
- Add `aria-label="Type your message"` to the `<input>` element
- Add a visually-hidden `<label for="chatbot-input">Type your message</label>` element

The send button must have `aria-label="Send message"` if it uses an icon without visible text.

---

## CHATBOT ACCESSIBILITY STANDARD

The custom chatbot widget introduces a modal-like interaction pattern. Modal patterns have specific WCAG requirements around ARIA roles, focus management, and keyboard operation.

### Required ARIA Implementation

| Element | Required ARIA |
|---|---|
| Toggle button (anchor icon) | `aria-label="Chat with our concierge"`, `aria-expanded="false"` (updated to `"true"` when panel is open) |
| Chat panel container | `role="dialog"`, `aria-label="She Said Sail Concierge"`, `aria-modal="true"` |
| Messages container | `role="log"`, `aria-live="polite"`, `aria-relevant="additions"` |
| Typing indicator | `aria-live="off"` (do not announce typing indicator) |
| Message input | `aria-label="Type your message"` or associated `<label>` |
| Send button | `aria-label="Send message"` |
| Close button | `aria-label="Close chat"` |
| Quick reply buttons | Visible text label on each button. No icon-only quick reply buttons. |

### Focus Management

When the chatbot panel opens:
- Focus must move into the panel immediately.
- Focus should land on the first interactive element inside the panel. If quick reply buttons are present, focus lands on the first quick reply button. If no quick reply buttons are present, focus lands on the message input field.

When the chatbot panel closes:
- Focus must return to the toggle button.
- This ensures keyboard users are not left with focus lost somewhere off-screen.

### Focus Trap

When the chatbot panel is open, focus must not leave the panel via Tab. The Tab key must cycle through interactive elements inside the panel only. Pressing Tab on the last focusable element inside the panel must move focus back to the first focusable element inside the panel (wrap-around). Pressing Shift+Tab on the first focusable element must move focus to the last.

Implement this with a focus trap utility in `chatbot-js.js`. Track all focusable elements inside the panel (buttons, inputs, links) and intercept Tab and Shift+Tab keydown events to enforce the cycle.

### Escape Key

When the chatbot panel is open and a keyboard user presses Escape, the panel must close and focus must return to the toggle button.

Add an event listener in `chatbot-js.js`:
```javascript
document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape' && chatPanelIsOpen) {
    closeChatPanel();
    toggleButton.focus();
  }
});
```

### Screen Reader Announcement of New Messages

When a new message appears in the messages container (either a bot message or the user's own message echoed back), the `role="log"` and `aria-live="polite"` attributes cause screen readers to announce the new content automatically. No additional JavaScript is required to trigger this announcement. Verify this behavior by testing with VoiceOver (macOS) or NVDA (Windows).

The typing indicator (the animated dots shown while a bot response is being generated) must NOT be announced. Set `aria-live="off"` on the typing indicator element so screen readers ignore it.

---

## MOBILE ACCESSIBILITY STANDARD

Mobile accessibility overlaps with mobile usability but has specific WCAG implications.

### Touch Target Size

WCAG 2.5.5 (Level AAA) recommends 44x44 CSS pixels for touch targets. At Level AA, the requirement is that targets are large enough to be easily activated. She Said Sail adopts 44x44px as the minimum standard for all tappable elements.

| Element | Required Minimum Size | Current Status |
|---|---|---|
| Chatbot toggle button | 44x44px | Met (56x56px per spec) |
| Chatbot close button | 44x44px | Verify in implementation |
| Quick reply buttons | 44px height minimum | Verify in implementation |
| Form submit button | 44px height minimum | Verify in implementation |
| Navigation links | 44px height minimum on mobile | Verify via CSS padding |
| CTA buttons | 44px height minimum | Verify via CSS padding |

### Text Size and iOS Zoom

iOS Safari automatically zooms in on a form field if the input's `font-size` is under 16px. This zoom disrupts the user experience and causes layout shifts. All visible form inputs on She Said Sail must have `font-size: 16px` or larger in their CSS.

### Viewport Meta Tag

The viewport meta tag must not include `user-scalable=no` or `maximum-scale=1`. These prevent users from zooming in, which is a WCAG 1.4.4 failure (Resize Text). Users must always be able to zoom to 200% without loss of content or functionality.

Correct viewport meta tag:
```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

Verify this in the WordPress head (Appearance > Customize > Additional CSS / theme settings, or view page source). WordPress core typically sets this correctly, but some themes or plugins override it.

### Color as the Only Indicator

WCAG 1.4.1 requires that color is not used as the only visual means of conveying information. On She Said Sail, this applies to:

**Form errors:** A red border on an invalid field is not sufficient. The field must also show a text error message and preferably an icon (such as an exclamation mark). Error state must be perceptible to users who cannot distinguish red from other colors.

**Required fields:** An asterisk (*) is acceptable as a conventional indicator if explained (for example, a note at the top of the form: "* Required field"). Color alone (red label text) is not sufficient.

**Selection state in quick reply buttons:** If a quick reply button has a selected state, that state must be indicated by more than just background color change (for example, a border, a checkmark, or a change in the button text).

---

## ACCESSIBILITY TESTING CHECKLIST

Run this checklist on every page type before launch. The checklist covers both automated and manual tests. Automated tools (Lighthouse, axe) catch approximately 30-40% of accessibility issues. Manual testing is required for focus management, keyboard navigation, and screen reader behavior.

### Automated Tests

| Check | Tool | Pass Condition |
|---|---|---|
| Color contrast | WebAIM Contrast Checker (webaim.org/resources/contrastchecker) | All text combinations pass at 4.5:1 (normal) or 3:1 (large) |
| Missing alt text | Lighthouse Accessibility audit or axe DevTools | Zero images flagged with missing or inappropriate alt text |
| Form label association | axe DevTools | Zero form inputs without associated labels |
| ARIA usage | axe DevTools | Zero invalid ARIA role or attribute errors |
| Lighthouse Accessibility score | Chrome DevTools Lighthouse | Score 95 or above on every page |
| Heading structure | HeadingsMap browser extension | No skipped heading levels, one H1 per page |
| Viewport meta | View page source | No `user-scalable=no` or `maximum-scale=1` present |

### Manual Tests

| Check | Method | Pass Condition |
|---|---|---|
| Keyboard navigation | Tab through entire page without mouse | All interactive elements reached in logical order, all operable with Enter or Space |
| Focus indicator visible | Tab through page, observe each focused element | Every focused element shows a visible gold outline ring |
| Focus management, chatbot open | Open chatbot via keyboard (Enter on toggle button), then Tab | Focus moves inside panel. Focus does not escape to page behind. |
| Focus management, chatbot close | Press Escape or Tab to close button and press Enter | Panel closes, focus returns to toggle button |
| Escape key, chatbot | Open chatbot, press Escape | Panel closes |
| Screen reader, messages | With VoiceOver or NVDA active, open chatbot, receive a bot message | Screen reader announces the new message text without announcing typing indicator |
| Touch targets | Chrome DevTools mobile emulation, inspect element dimensions | All buttons and inputs are at least 44px tall and 44px wide |
| Form errors, color independence | Submit the form with an empty required field | Error state is communicated with text, not color alone |
| Zoom to 200% | Browser zoom to 200% on mobile viewport | No content is clipped, hidden, or loses functionality |

### Screen Reader Test Environments

Test with at least one screen reader before launch:
- VoiceOver on macOS with Safari (most common among screen reader users on premium consumer sites)
- NVDA on Windows with Chrome (free, widely used)

Focus the test on: heading navigation, form field labels, chatbot ARIA behavior, and link text quality.

---

## ONGOING ACCESSIBILITY MAINTENANCE

Accessibility must be treated as a living standard, not a one-time audit. Content editors adding images, changing text, or creating new pages can introduce regressions.

**Content editor rules:**
- Always fill in the Alt Text field when uploading images in WordPress Media Library.
- Do not choose heading levels based on visual appearance.
- Do not paste content from Word or Google Docs directly into Elementor text widgets without checking that heading structure is preserved correctly.
- Never add `outline: none` to any CSS.

**Developer rules:**
- Run axe DevTools before every deployment.
- Run the keyboard navigation manual test before every major change to interactive components.
- When adding a new third-party widget or embed, assess its ARIA and keyboard accessibility before adding it to the site.

**Post-launch audit schedule:**
- Quarterly: run Lighthouse Accessibility audit on all page types.
- Annually: conduct a comprehensive manual accessibility review using the full checklist above.

---

*This document is maintained by the She Said Sail development team. Update this file when new interactive components are added, when the color palette changes, or when WCAG standards are updated.*
