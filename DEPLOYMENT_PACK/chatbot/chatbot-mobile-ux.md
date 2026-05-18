# She Said Sail: Chatbot Mobile UX Specification
**Version:** 1.0
**Date:** May 2026

Mobile-specific behavior, sizing, and interaction standards for the luxury concierge chatbot. Primary target device: iPhone 14 / 15 (390px viewport width, Safari).

---

## MOBILE DESIGN PRINCIPLES

1. The widget never auto-opens on mobile. The visitor must tap it intentionally.
2. When the panel is open, it occupies most of the screen. This is intentional: conversation deserves focus.
3. Typing on mobile keyboard should never hide the input field. The widget adjusts when the keyboard appears.
4. Tap targets are never smaller than 44x44px.
5. Input font size is 16px minimum to prevent iOS auto-zoom behavior.

---

## WIDGET TOGGLE (CLOSED STATE)

**Desktop:**
- 56x56px navy circle, bottom-right, 24px from edge
- "Concierge" label visible in gold italic serif beside or below the circle
- Box shadow soft

**Mobile (767px and below):**
- Same circle, same colors
- Position: fixed, right 16px, bottom 16px
- "Concierge" label hidden (space constraint)
- Circle has subtle pulsing gold ring on first page visit to draw attention
  - Animation: one pulse cycle, 2s after page load, does not repeat
- When panel is open: toggle button hidden (panel header contains minimize button)

---

## CHAT PANEL (OPEN STATE)

**Desktop:**
- Width: 380px
- Height: 520px
- Position: fixed, right 24px, bottom 88px
- Floats above page content

**Mobile:**
- Width: calc(100vw - 32px), max 380px
- Height: 65vh (this leaves room above for page context)
- Position: fixed, right 16px, bottom 80px (when keyboard not open)
- Overflow: hidden at container level, messages area scrollable internally

**Panel open/close animation:**
- Opens: opacity 0 to 1, translateY(12px) to translateY(0), duration 280ms, luxury easing
- Closes: reverse, duration 220ms
- No slide from bottom. Float-up is more refined.

---

## KEYBOARD HANDLING (iOS SAFARI)

When the user taps the input field on iOS:
1. The virtual keyboard appears and reduces the visible viewport height
2. The chat panel must stay above the keyboard, with the input field visible

Implementation:
- Listen for `visualViewport.resize` if available, otherwise listen for `window.resize`
- On resize (viewport height reduction indicates keyboard open):
  - Set panel `bottom` to `visualViewport.height - panelHeight - 16px` (or similar calculation)
  - Scroll messages to the bottom after a short delay (150ms)
- On keyboard dismiss (viewport height increases):
  - Reset panel bottom to original value

This prevents the common mobile chat problem where the input field is hidden behind the keyboard.

---

## MESSAGE AREA

**Desktop and mobile:**
- Overflow-y: auto with -webkit-overflow-scrolling: touch
- Smooth scrolling to latest message after each message is added
- Messages never overflow horizontally (max-width 80% of panel, word-break: break-word)

**Mobile tap behavior:**
- Tapping a quick reply button: executes immediately, no hover state
- Tapping the messages area (not a button): dismisses keyboard if open
- Long press on messages: no special behavior (do not trigger browser text selection if possible)

---

## QUICK REPLY BUTTONS

**Desktop:** pill buttons, flex-wrap, up to 3 per row
**Mobile:**
- Same pill style
- Font size: 13px
- Min height: 44px
- Flex-wrap: wrap
- When there are more than 3 quick replies, they wrap to multiple rows naturally
- No horizontal scroll (avoid: users do not discover horizontally hidden options)

---

## INPUT FIELD

- Width: 100% of available space in input area
- Height: 44px minimum (touch target)
- Font size: 16px (critical: prevents iOS auto-zoom)
- Padding: 10px 14px
- Autocomplete: off
- Autocorrect: on (natural for mobile typing)
- Spellcheck: true
- Return key: submits message (listen for keypress Enter)
- The send button is 44x44px minimum

---

## SCROLL BEHAVIOR

After every bot message and every user message:
- Scroll `#sss-chat-messages` to `scrollTop = scrollHeight` smoothly
- Delay: 50ms after message is added (allows DOM to update)
- Do not scroll if user has manually scrolled up to read earlier messages
  - Detection: if `scrollTop + clientHeight < scrollHeight - 100`, user has scrolled up. Do not force scroll.
  - Reset once user scrolls back to bottom or sends a new message.

---

## MINIMIZE AND CLOSE

**Panel minimize (desktop and mobile):**
- Clicking the minimize button in the panel header closes the panel
- The toggle button remains visible
- Panel state is preserved (conversation thread retained)
- Reopening shows the same thread

**Session behavior:**
- Conversation data persists for the browser session (stored in memory)
- Refreshing the page resets the chatbot
- No localStorage persistence of conversation (privacy consideration)

---

## ACCESSIBILITY ON MOBILE

- Widget toggle has `aria-label="Chat with our concierge"`
- Panel has `role="dialog"` and `aria-label="She Said Sail Concierge"`
- Messages area has `role="log"` and `aria-live="polite"`
- Focus management: when panel opens, focus moves to the first input or quick reply
- When panel closes, focus returns to the toggle button
- Screen reader: bot messages announced via aria-live, user messages read after send

---

## PROACTIVE TRIGGER (MOBILE SUPPRESSED)

Auto-open is disabled on all mobile viewports (width <= 767px). The reason: auto-opening a full-panel chat on mobile is aggressive and disrupts the page experience. Mobile users discover the widget through the visible launcher.

Detection:
```javascript
var isMobile = window.innerWidth <= 767;
if (!isMobile) {
  // set auto-trigger timers
}
```

---

## PERFORMANCE ON MOBILE

- chatbot-js.js loads deferred (same as global JS, wrapped in `<script defer>`)
- chatbot-css.css loads in the footer with the other global CSS
- No images in the chat widget (SVGs only)
- No external font requests (fonts already loaded by global page CSS)
- Typing indicator: pure CSS animation (no JS animation library)
- Total widget JS: target under 15KB minified
- Total widget CSS: target under 8KB minified

---

## TESTING CHECKLIST (MOBILE SPECIFIC)

- [ ] Widget appears in bottom right on iPhone 14 (390px)
- [ ] Label hidden on mobile, circle visible
- [ ] Tapping circle opens panel without auto-opening
- [ ] Panel height is 65vh, not full screen
- [ ] Input field is visible when keyboard opens (keyboard does not cover input)
- [ ] Input font size is 16px (no iOS auto-zoom)
- [ ] Quick replies all tappable (min 44px height)
- [ ] Messages scroll to bottom automatically
- [ ] User can scroll up to read history
- [ ] Minimize button closes panel and returns focus to toggle
- [ ] Conversation thread retained when panel is minimized and reopened
- [ ] No auto-trigger fires on mobile
- [ ] Wave/pulse animation fires once on first visit
- [ ] Gold pulsing ring visible on first visit toggle
