# She Said Sail: Chatbot QA Checklist
**Version:** 1.0
**Date:** May 2026

Pass/fail checklist for the luxury concierge chatbot. Complete this after the chatbot-js.js and chatbot-css.css are applied via Insert Headers and Footers and the Make.com webhook is wired.

---

## SECTION 1: VISUAL QUALITY

**Desktop (1440px Chrome)**

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Toggle button appears in bottom-right corner, navy circle, gold icon | | | |
| "Concierge" label visible in gold italic beside or below circle | | | |
| Panel opens with float-up animation (not slide from bottom) | | | |
| Panel header is navy with "She Said Sail" and "Concierge" label | | | |
| Bot messages appear in white bubbles, left-aligned | | | |
| User messages appear in navy bubbles, right-aligned | | | |
| Typing indicator shows before each bot message (3 gold dots pulsing) | | | |
| Quick reply pills appear in gold-bordered buttons below bot message | | | |
| Quick reply hover state: navy fill, cream text | | | |
| Input field has gold focus border | | | |
| Send button is navy circle with gold arrow | | | |
| Panel closes with fade-out animation | | | |
| No generic AI icons or generic chat widget appearance | | | |
| No bright gradients, neon colors, or heavy shadows | | | |
| Tidio widget is hidden (confirm #tidio-chat has display:none) | | | |

---

## SECTION 2: VISUAL QUALITY MOBILE (375px iPhone Safari)

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Toggle circle visible bottom-right, 16px from edge | | | |
| "Concierge" label hidden on mobile | | | |
| Gold pulse ring fires once on first visit | | | |
| Panel opens to 65vh height, not full screen | | | |
| Input field does not disappear behind keyboard | | | |
| Input field font size is 16px (no iOS zoom) | | | |
| Quick reply buttons have minimum 44px tap height | | | |
| Messages scroll to bottom on each new message | | | |
| No horizontal overflow on any message bubble | | | |
| Minimize button closes panel cleanly | | | |

---

## SECTION 3: CONVERSATION FLOW

**Test path: Bachelorette, high energy, 9-15 guests, has date, provides email**

| Step | Expected Bot Message | Pass | Fail |
|---|---|---|---|
| Widget opens | "Hi there. What kind of day are you planning for your group?" | | |
| Typing indicator shows before message | 800ms delay before opener appears | | |
| 5 quick replies shown | Bachelorette, Birthday, Girls trip, Something more intimate, Still exploring | | |
| User selects "Bachelorette party" | "A bachelorette in Miami. Great. Is the group more into a high-energy social day, or something more elevated and curated?" | | |
| User selects "High energy" | Pink Palm Club recommendation message | | |
| "Does that sound like the right direction?" appears | After recommendation | | |
| User selects "Yes, that sounds right" | "How many people are you thinking?" | | |
| User selects "9 to 15 guests" | "Do you have a date in mind..." | | |
| User selects "I have a date" | "What date are you looking at?" | | |
| User types a date | "Perfect. What is your first name..." | | |
| User types name | "Thanks, [name]. What is the best email address..." | | |
| User types email | "And a phone number if you would like to hear back by text? Completely optional." | | |
| User selects "Skip for now" | Handoff message with name and experience | | |
| Webhook fires to Make.com | Confirm in Make.com scenario execution log | | |
| GTM chatbot_handoff fires | Confirm in GTM Preview | | |
| STATE_CLOSED message appears | "Talk soon. In the meantime..." | | |

---

## SECTION 4: CONVERSATION FLOW (ALTERNATE PATHS)

| Scenario | Expected behavior | Pass | Fail |
|---|---|---|---|
| User types "anniversary" in opener free text | Routes to STATE 2D (intimate), Golden Hour Escape pre-selected | | |
| User types "birthday" in free text | Routes to STATE 2B | | |
| User selects "Still exploring" | "That is a good place to start..." then atmosphere/size/timing quick replies | | |
| User asks "Can I speak to someone?" | Escalation message fires, collects name and email | | |
| User sends unrecognized input twice | "I want to make sure I get this right..." then jumps to contact capture | | |
| User goes silent 90 seconds | "Still there? No rush." fires | | |
| Invalid email entered | "That does not look quite right. Can you double-check the email address?" | | |
| Valid email entered second time | Proceeds normally to phone step | | |

---

## SECTION 5: COPY QUALITY

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Zero em dashes in any bot message | | | |
| No exclamation marks in any bot message | | | |
| No "Absolutely", "Certainly", "Of course" as openers | | | |
| No "Amazing" / "Wonderful" / "Fantastic" as openers | | | |
| No "How can I help you today?" | | | |
| No "Is there anything else?" | | | |
| No "Book now" language | | | |
| No "Fill out the form" | | | |
| First name used exactly twice (confirmation + handoff) | | | |
| Experience names spelled correctly (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club) | | | |
| Tone is warm, calm, confident, not robotic | | | |

---

## SECTION 6: BACKEND AND DATA

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Airtable receives record after test conversation completes handoff | | | |
| Record shows Request_Type = "Chatbot Lead" | | | |
| Email field populated correctly | | | |
| Experience Interest field maps to correct experience name | | | |
| Occasion field maps correctly | | | |
| UTM fields populate if UTM params are in URL (?utm_source=test) | | | |
| Landing page field shows correct URL | | | |
| source_type = "chatbot" present in payload | | | |
| Acknowledgment email arrives within 2 minutes | | | |
| Slack alert fires in #new-leads | | | |

---

## SECTION 7: ANALYTICS

| Check | Pass | Fail | Notes |
|---|---|---|---|
| chatbot_open fires in GTM Preview on widget open | | | |
| chatbot_start_conversation fires when opener message displays | | | |
| chatbot_select_occasion fires with correct occasion value | | | |
| chatbot_select_experience fires with correct experience_slug | | | |
| chatbot_capture_email fires after valid email submitted | | | |
| chatbot_handoff fires with experience_slug and has_email: true | | | |
| chatbot_complete fires after close message | | | |
| Meta Pixel Lead event fires on chatbot_handoff (if Meta Pixel active) | | | |
| TikTok Pixel CompleteRegistration fires on chatbot_handoff (if TikTok active) | | | |
| No PII (email, phone) included in any GTM event payload | | | |

---

## SECTION 8: PERFORMANCE AND TECHNICAL

| Check | Pass | Fail | Notes |
|---|---|---|---|
| chatbot-js.js loads deferred, after page content | | | |
| No console errors on page load | | | |
| No console errors during conversation | | | |
| Widget does not interfere with Elementor page scrolling | | | |
| Widget does not interfere with other page CTAs | | | |
| No auto-trigger fires on mobile (375px width) | | | |
| Auto-trigger fires on desktop homepage after 60 seconds of activity | | | |
| Auto-trigger fires on experience pages after 45 seconds | | | |
| No auto-trigger on /request-to-book/ | | | |
| Session flag prevents re-trigger after first auto-open | | | |
| window.__sssChatLoaded guard prevents double execution | | | |

---

## SIGN-OFF

| Role | Name | Date | Signed |
|---|---|---|---|
| Web builder | | | |
| Developer (Make.com wiring) | | | |
| Founder approval | | | |
