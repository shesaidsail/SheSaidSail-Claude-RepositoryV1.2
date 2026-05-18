# She Said Sail: Production Hardening Audit

**Version:** 1.0
**Date:** 2026-05-18
**Scope:** Post-final-audit production hardening pass
**Auditor:** Claude Code (AI-assisted technical audit)

---

## Scoring Key

| Score | Meaning |
|---|---|
| 9-10 | Excellent: production-grade, no meaningful gaps |
| 7-8 | Good: solid foundation, minor gaps only |
| 5-6 | Adequate: functional but with notable weaknesses |
| 3-4 | Weak: significant gaps that should be addressed |
| 1-2 | Failing: not fit for purpose |

---

## Performance

**Score: 8 / 10**

**Improvements made:**
- Added `will-change: transform, opacity` to `.sss-reveal` elements for GPU compositing ahead of scroll animations.
- Added `will-change: transform` to experience card wrappers; clears to `auto` on hover completion to avoid excessive layer promotion.
- Added `will-change: auto` override in `@media (prefers-reduced-motion: reduce)` to avoid unnecessary compositor layers for users who opt out of motion.
- Added `contain: layout style` to `.sss-social-proof` (the largest rendered section) to isolate layout recalculation.
- Added `contain: layout style paint` to `#sss-chat-widget` so the chatbot panel does not trigger page-level reflows.
- Added `overscroll-behavior: contain` to chat messages area to prevent parent page scroll chain when user reaches top/bottom of chat.
- Added `overflow-x: clip` to `body` to prevent horizontal scroll bleed on mobile, a common source of CLS.
- Reduced `--transition-slow` from `0.65s` to `0.55s` for snappier card hover feel without sacrificing the luxury register.
- Replaced hardcoded `0.85s` card image transition with `var(--transition-slow)` so the token controls it.
- Scroll depth listener (`scroll_50_percent`, `scroll_90_percent`) now removes itself from the window after both events fire, eliminating a permanent passive listener.

**Remaining gaps:**
- Actual Lighthouse scores are unknown without live deployment.
- Hero image `fetchpriority="high"` behavior under Elementor's renderer remains unverified.
- WordPress/Elementor render pipeline adds overhead not visible in code review.

---

## Stability

**Score: 8 / 10**

**Improvements made:**
- Auto-trigger timer (`setupAutoTrigger`) now registers a `pagehide` listener that clears the timer and removes activity listeners on page unload, preventing memory leaks in SPA-adjacent scenarios.
- Mobile keyboard resize handler now checks `isOpen` before calling `scrollToBottom`, preventing unnecessary DOM operations when chat panel is closed.
- `setupMobileKeyboard` resize handler uses `{ passive: true }` option for better scroll performance.
- `out_of_scope` awaiting input handler was missing: free-text input while in that state now correctly routes to `jumpToNameCapture` (yes) or a graceful close message (no), instead of falling through to the fallback unrecognized path.

**Remaining gaps:**
- Elementor element ID selectors (e.g., `.elementor-element-f84aeeb`) are stable within a given build but will break if Elementor regenerates IDs. This is an inherent risk of Elementor-targeted CSS that cannot be mitigated without live site access.
- Three webhook URLs remain as placeholders. This is a known go-live blocker, not a stability defect.

---

## Mobile Polish

**Score: 7 / 10**

**Improvements made:**
- Added `min-height: 40px; display: inline-flex; align-items: center; justify-content: center` to `.sss-occasion-pill` on mobile to meet near-44px tap target guidance for pill-style elements.
- `overscroll-behavior: contain` on chat messages prevents page scroll from triggering when mobile user scrolls to end of chat history.
- `prefers-reduced-motion` reduces all transitions and animations to 0.01ms for users who need it, including the reveal system, card hovers, and global transitions.

**Remaining gaps:**
- Physical device testing is required before go-live. Elementor's responsive behavior on real iOS hardware cannot be confirmed from code review.
- Chat widget height on very small screens (iPhone SE) not verified.

---

## Production Safety

**Score: 8 / 10**

**Improvements made:**
- `click_explore_experiences` GTM event now uses `a[href$="/experiences/"]` (ends-with) instead of `a[href*="/experiences/"]` (contains), preventing the event from firing on clicks to individual experience subpages (`/experiences/monaco-social/`, etc.).
- `submit_email_capture` GTM event parameter standardized to `page_location` (was `form_location`), now consistent with all other GTM event parameter names.
- `chatbot_open` and `chatbot_start_conversation` GTM events now include `page_location` parameter, consistent with all other 8 chatbot events.
- `aria-modal` attribute on chat panel now toggles correctly: `true` when open, `false` when closed. Previously stuck at `false`.
- Legacy plugin safety rule in chatbot CSS broadened from `#tidio-chat` to `#tidio-chat, [id^="tidio"]` to suppress any residual Tidio DOM output regardless of exact ID.
- Header comment in global JS updated to remove `open_chat` (retired Tidio event) from the engagement event list.

**Remaining gaps:**
- WIRE_THIS_CHATBOT_WEBHOOK_URL, WIRE_THIS_CONTACT_WEBHOOK_URL, and email capture webhook remain unwired. All three have correct error handling that will not break the page, but they will not transmit data until wired.
- Tidio plugin must still be disabled in WordPress admin before go-live.

---

## Accessibility

**Score: 6 / 10**

**Improvements made:**
- Removed 9 redundant per-class `:focus-visible` rules that duplicated the global `:focus-visible` rule, reducing CSS specificity noise.
- Global `:focus-visible` rule remains, providing correct 2px gold outline at 3px offset for all interactive elements.
- `@media (prefers-reduced-motion: reduce)` block added to global CSS, covering the scroll reveal system, card hover transforms, and global transitions.
- `.sss-reveal` elements reset to fully visible state (`opacity: 1; transform: none; transition: none`) under reduced motion, so content is never invisible for users who prefer no motion.
- `aria-modal` fix on chat panel improves screen reader behavior when chat is open.
- Added CSS for missing `.sss-concierge-steps`, `.sss-concierge-step`, `.sss-concierge-step-number`, `.sss-concierge-step-text`, and `.sss-concierge-footer-note` classes, so the concierge block renders with correct visual hierarchy instead of bare browser list defaults.

**Known failures (not resolved):**
- Gold text `#DAB97E` at 2.4:1 contrast ratio fails WCAG AA for normal text. Usage restricted to decorative headings and large display text. Must be confirmed on live site.
- Muted text `rgba(44,44,44,0.5)` at approximately 2.7:1 contrast ratio fails for body text. Usage restricted to decorative/supporting captions. Must be confirmed on live site.
- Screen reader behavior with custom chatbot widget has not been tested on physical hardware with VoiceOver or NVDA.

---

## Consistency

**Score: 8 / 10**

**Improvements made:**
- Social proof strip `<h2>` was missing class `.sss-social-proof-heading`. Added. The heading now renders correctly in the editorial serif at the specified size, instead of defaulting to browser/Elementor h2 styles.
- Experiences bottom CTA: `<h2>` missing `.sss-exp-bottom-cta-heading` class added; `<p>` missing `.sss-exp-bottom-cta-copy` class added; button class corrected from non-existent `sss-btn-primary` to `sss-exp-cta-btn`.
- Form intro: `<h2>` missing `.sss-form-intro-heading` class added; `<p>` corrected from non-existent `sss-form-intro-subtext` to `sss-form-intro-copy`.
- Thank-you message: `<h1>` missing `.sss-thankyou-heading` class added; body copy class corrected to `.sss-thankyou-subtext`; `.sss-thankyou-divider` added between heading and copy; non-existent wrapper div `.sss-thankyou-inner` removed.
- Monaco Social bottom CTA button: replaced verbose inline style declaration with `.sss-cta-btn` class (new shared class). Button now has hover state.
- New shared `.sss-cta-btn` CSS class added: gold background, navy text, same sizing and transition as all other primary CTA buttons in the system.
- GTM event parameter `form_location` renamed to `page_location` for `submit_email_capture`, matching all other event parameters in the system.

**Remaining gaps:**
- Elementor inline styles may override custom CSS on the live site in ways not visible from code review. Visual QA on the staged site is required.

---

## Implementation Readiness

**Score: 8 / 10**

The system is more implementation-ready after this pass. Key class-HTML mismatches that would have caused invisible or incorrectly styled sections have been corrected. The JavaScript event tracking system is tighter and more correct. The CSS is lighter (9 redundant rules removed) and more complete (reduced-motion support added, missing component styles added).

---

## Summary Scorecard

| Dimension | Before | After |
|---|---|---|
| Performance | 6 | 8 |
| Stability | 7 | 8 |
| Mobile Polish | 6 | 7 |
| Production Safety | 6 | 8 |
| Accessibility | 5 | 6 |
| Consistency | 6 | 8 |
| Implementation Readiness | 6 | 8 |
| **Average** | **6.0** | **7.6** |

---

## Top 15 Improvements Made

1. Added `@media (prefers-reduced-motion: reduce)` block covering scroll reveal system, card hovers, and global transitions. All animated elements fall back gracefully.
2. Fixed `click_explore_experiences` GTM selector from `href*=` (contains, matched subpages) to `href$=` (ends-with, matches only `/experiences/`).
3. Fixed `aria-modal` toggle on chatbot panel: now `true` when open, `false` when closed.
4. Added `will-change: transform, opacity` to `.sss-reveal` for GPU compositing; clears to `auto` after reveal completes to release the compositor layer.
5. Removed scroll event listener after both `scroll_50_percent` and `scroll_90_percent` events have fired. Listener was permanent.
6. Fixed missing CSS classes in social proof strip, experiences CTA, form intro, and thank-you message snippets. Several sections would have rendered with browser defaults instead of brand styles.
7. Added complete CSS for `.sss-concierge-steps` ordered list. The concierge block would have rendered as an unstyled browser list without these rules.
8. Added `chatbot_open` and `chatbot_start_conversation` GTM events' `page_location` parameter.
9. Fixed `submit_email_capture` GTM parameter from `form_location` to `page_location` for system-wide consistency.
10. Added `overscroll-behavior: contain` to chat messages area, preventing page scroll chain on mobile when user scrolls to end of chat.
11. Added `contain: layout style paint` to chatbot widget container, isolating it from page-level layout recalculation.
12. Added `overflow-x: clip` to body, preventing mobile horizontal scroll bleed that causes CLS.
13. Fixed missing `out_of_scope` awaiting input handler in chatbot: user responses in that state now route correctly instead of falling through.
14. Auto-trigger timer cleanup on `pagehide` prevents memory leak from persistent scroll/mousemove listeners and pending setTimeout.
15. Replaced Monaco Social inline-styled CTA button with `.sss-cta-btn` class, giving it a hover state it previously lacked.

---

## Top 10 Risks Removed

1. GTM `click_explore_experiences` firing on experience detail page clicks (subpage links matched by `href*=` contains selector). Fixed.
2. Chat messages area triggering page body scroll on mobile when reaching top or bottom of conversation. Fixed with `overscroll-behavior: contain`.
3. Permanent `scroll` event listener attached to window even after both depth events had already fired. Fixed.
4. Auto-trigger timer and activity listeners persisting in memory after page unload. Fixed with `pagehide` cleanup.
5. Screen readers receiving incorrect `aria-modal` state from chatbot panel (stuck at `false` even when panel was visually open). Fixed.
6. Social proof strip, experiences CTA, and thank-you heading rendering with browser default styles instead of brand typography because of missing CSS classes. Fixed.
7. Users with `prefers-reduced-motion` seeing all scroll reveal elements hidden (opacity: 0) and never revealed, because the IntersectionObserver still ran and the reveal CSS was never bypassed. Fixed.
8. `out_of_scope` conversation state in chatbot had no handler: any typed response in that state fell through to the unrecognized fallback path. Fixed.
9. Horizontal overflow bleed on mobile (common from Elementor full-width sections) with no `overflow-x` suppression on body. Fixed.
10. Monaco Social CTA button having no hover/focus visual state because it relied entirely on inline styles (which cannot contain pseudo-classes). Fixed by switching to `.sss-cta-btn` class.

---

## Files Cleaned or Updated

| File | Changes |
|---|---|
| `01_GLOBAL_CSS/she-said-sail-global.css` | Removed 9 redundant focus-visible rules; added reduced-motion block; added will-change to reveal and cards; added overflow-x: clip to body; added contain to social proof; reduced transition-slow; added concierge step CSS; added .sss-cta-btn class; fixed card image transition token reference; added mobile tap target for occasion pills |
| `02_GLOBAL_JS/she-said-sail-global.js` | Removed open_chat from header comment; fixed click_explore_experiences selector; fixed submit_email_capture parameter name; replaced inline scroll handler with named function that self-removes |
| `chatbot/chatbot-js.js` | Added page_location to chatbot_open and chatbot_start_conversation; fixed aria-modal toggle; added out_of_scope handler; added pagehide timer cleanup; simplified mobile keyboard handler |
| `chatbot/chatbot-css.css` | Added overscroll-behavior: contain to messages area; added contain: layout style paint to widget; updated legacy plugin suppression rule |
| `03_HTML_SNIPPETS/homepage/social-proof-strip.html` | Added missing .sss-social-proof-heading class to h2 |
| `03_HTML_SNIPPETS/experiences/experiences-bottom-cta.html` | Fixed h2 class, p class, and button class |
| `03_HTML_SNIPPETS/request-to-book/request-form-intro.html` | Fixed h2 and p class names |
| `03_HTML_SNIPPETS/request-to-book/thank-you-message.html` | Fixed h1 class, p class, added divider, added experiences CTA link |
| `03_HTML_SNIPPETS/monaco-social/bottom-cta.html` | Replaced inline-styled CTA button with .sss-cta-btn class |

---

## What Still Requires Live Testing

1. **Lighthouse mobile performance score:** Target baseline 70+. Capture immediately after first staging deploy.
2. **Elementor element ID selectors:** Verify that all `.elementor-element-XXXXXXX` selectors in the global CSS match the actual element IDs generated by Elementor on the live site. These are the highest risk of silent visual failure.
3. **Hero image loading:** Confirm `fetchpriority="high"` and `loading="eager"` are applied and not overridden by Elementor. Check Network tab in DevTools.
4. **Concierge block styling:** The `.sss-concierge-steps` CSS is new. Verify the ordered list renders as intended on the live request-to-book page.
5. **Thank-you page:** Verify the `.sss-thankyou` section renders with correct heading, divider, subtext, and CTA. Previously had class mismatches.
6. **Reduced motion support:** Test with `prefers-reduced-motion: reduce` enabled in OS accessibility settings. Confirm all `.sss-reveal` elements are visible immediately and no animations run.
7. **Chatbot on mobile:** Physical iOS and Android device testing required. Verify keyboard opens without obscuring input, scroll-to-bottom works, and tap targets are adequate.
8. **Gold text contrast:** Confirm `#DAB97E` is only used for large display headings and decorative elements on the live site, not body text.
9. **Scroll depth events:** Verify `scroll_50_percent` and `scroll_90_percent` each fire exactly once per page load in GTM preview mode.
10. **`click_explore_experiences` selector fix:** Confirm the event fires on homepage and experience page "Explore experiences" links but not on individual experience card links.

---

## Final Production Readiness Score

**7.6 / 10** (up from 6.0 pre-hardening)

The system is staging-ready. Core conversion path, analytics, chatbot, SEO, and backend architecture are all sound. The hardening pass resolved the most significant code-level gaps: missing CSS classes causing silent visual failures, a GTM event firing on the wrong links, and a permanent scroll listener. The accessibility and performance scores remain limited by the live-site unknowns common to any Elementor build. These require physical device testing after the first staging deploy.

**GO FOR STAGING.** Wire the three webhook URLs for end-to-end testing.
