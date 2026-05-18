# She Said Sail: Chatbot Final Audit
**Version:** 1.0
**Date:** May 2026
**Audited against:** docs/system/master-audit-scorecard.md (adapted for chatbot context)

---

## BEFORE SCORES (Current Tidio Chatbot)

Assessment of the existing Tidio chatbot as installed on the live site prior to this redesign.

| Dimension | Score | Evidence |
|---|---|---|
| Emotional Engagement | 2 | Generic opener ("Hi, how can I help you?"). No occasion awareness. No emotional warmth. Feels like a support ticket system. |
| Luxury Positioning | 1 | Tidio default styling (bright blue-purple gradient, generic chat bubble, Times New Roman heading). No brand colors, no brand fonts, no concierge framing. |
| Conversational Quality | 2 | No structured flow. Bot waits for user to type something. No quick replies. No guidance. Most visitors type nothing and close. |
| Mobile UX | 3 | Tidio renders acceptably on mobile but is not optimized. No keyboard handling. Generic mobile appearance. |
| Backend Readiness | 2 | No data capture in chatbot. No connection to Airtable or Make.com. No UTM attribution. Only the open_chat GTM event exists. |
| Analytics Readiness | 2 | One event: open_chat. No conversation depth, no occasion tracking, no email capture event, no handoff event. No funnel visibility. |
| Conversion Potential | 2 | No conversation flow means no qualification path. Visitors who open the chat have no guided path to booking. High drop-off. |
| Trust | 3 | Chat widget presence provides some trust signal, but generic appearance undermines it. No concierge framing. |
| Operational Maturity | 2 | No escalation logic. No silence handling. No handoff protocol. No Make.com integration. |
| **Overall** | **2.1 / 10** | |

---

## AFTER SCORES (Redesigned Luxury Concierge)

Assessment of the full chatbot system as specified in this redesign.

| Dimension | Score | Rationale |
|---|---|---|
| Emotional Engagement | 9 | Progressive conversation that starts with the occasion, recommends experiences emotionally, and moves toward booking through curiosity rather than pressure. Warm copy throughout. No robotic phrases. |
| Luxury Positioning | 8 | Navy/gold/cream visual system matching the site exactly. Cormorant Garamond headers. Refined spacing. No generic AI aesthetics. The widget feels like part of the brand, not a plugin. |
| Conversational Quality | 9 | 11-state conversation tree. One question at a time. Quick replies reduce friction. Keyword detection routes accurately. Silence handling. Escalation logic. Dead-end prevention. Human pacing via typing indicator delays. |
| Mobile UX | 8 | Keyboard handling documented and implemented. No auto-trigger on mobile. 44px tap targets. 16px input font. 65vh panel height. Gold pulse ring on first visit. |
| Backend Readiness | 8 | Full Airtable field mapping documented. M-CHATBOT-001 scenario specified. UTM attribution via sessionStorage. Webhook placeholder in JS for one-step wiring. Escalation flag supported. |
| Analytics Readiness | 9 | 8 GTM events covering the full funnel (open, start, occasion, experience, email, phone, handoff, complete). 4 new DLVs. GA4 conversion events specified. Meta and TikTok pixel events on handoff. 3 GA4 audiences defined. Funnel metrics specified. |
| Conversion Potential | 9 | Guided experience recommendation. Invisible qualification (occasion, group size, date). Warm handoff with 24-hour concierge follow-up framing. No pressure. Email captured before commitment. |
| Trust | 9 | Concierge framing throughout. Named widget ("Concierge" not "Chat"). No commitment language. 24-hour response framing. No fake urgency. Escalation path to real human. |
| Operational Maturity | 8 | Silence detection. Escalation logic. Dead-end recovery. Webhook with Airtable, email, and Slack. QA checklist complete. All edge cases documented in conversation flow. |
| **Overall** | **8.6 / 10** | |

---

## SCORE COMPARISON

| Dimension | Before | After | Gain |
|---|---|---|---|
| Emotional Engagement | 2 | 9 | +7 |
| Luxury Positioning | 1 | 8 | +7 |
| Conversational Quality | 2 | 9 | +7 |
| Mobile UX | 3 | 8 | +5 |
| Backend Readiness | 2 | 8 | +6 |
| Analytics Readiness | 2 | 9 | +7 |
| Conversion Potential | 2 | 9 | +7 |
| Trust | 3 | 9 | +6 |
| Operational Maturity | 2 | 8 | +6 |
| **Overall** | **2.1** | **8.6** | **+6.5** |

---

## MAJOR IMPROVEMENTS MADE

1. **Full conversation state machine.** 11 states from idle to closed, with branches for all 4 occasion types and all 4 experience recommendations. No dead ends.

2. **Experience recommendation engine.** Recommends based on occasion + energy + group size. Not random. Not "here are all options." The bot guides confidently, the way a trained concierge would.

3. **Copy system.** Comprehensive prohibited phrases list, approved openers, tone rules by state, all 20+ production-ready messages. No robotic language.

4. **Luxury visual system.** Custom CSS widget that matches the She Said Sail brand precisely. Tidio hidden. No generic chat aesthetics.

5. **Backend integration.** Make.com M-CHATBOT-001 scenario specified. Airtable field mapping documented. UTM attribution via existing sessionStorage mechanism. One webhook placeholder to wire.

6. **Analytics depth.** 8 GTM events replacing 1. Full funnel visibility. GA4 conversion events. Pixel events on handoff. 3 remarketing audiences.

7. **Mobile UX.** Keyboard handling. No auto-trigger on mobile. Refined spacing. Pulse animation on first visit.

8. **Operational logic.** Silence detection (90s), dead-end recovery, escalation to human concierge, session guards, typing indicator pacing.

---

## REMAINING WEAKNESSES

1. **Not AI-powered.** The conversation is a scripted state machine. It handles the documented flow excellently but cannot answer novel questions or improvise. For a full AI-powered concierge (using Claude or GPT), a separate API integration would be needed with server-side handling.

2. **No conversation history persistence.** Refreshing the page resets the conversation. A returning visitor starts over. This is intentional for privacy but means no continuity across sessions.

3. **Backend not yet wired.** M-CHATBOT-001 scenario must be built in Make.com and the webhook URL must replace `WIRE_THIS_CHATBOT_WEBHOOK_URL` in chatbot-js.js. Until this is done, chatbot leads are not captured in Airtable.

4. **GTM tags not yet built.** The 7 new GTM tags, 4 DLVs, and 7 triggers must be created and published. Until then, no chatbot analytics data appears in GA4.

5. **Tidio configuration not updated.** The CSS hides Tidio (#tidio-chat display:none) but Tidio is still loading. It should be disabled from the WordPress admin to save the page load. This is a 2-minute admin action.

6. **Experience recommendation accuracy.** The current logic uses keyword detection and quick reply selections. A mistyped or ambiguous response may route incorrectly. Human review of early conversations is recommended before scaling paid advertising.

---

## READINESS ASSESSMENT

| Phase | Readiness | Condition |
|---|---|---|
| Visual deployment | Ready | chatbot-css.css and chatbot-js.js applied via Insert Headers and Footers |
| Conversation (without backend) | Ready | chatbot-js.js loaded. Conversations run. No data captured yet. |
| Backend capture | Not ready | M-CHATBOT-001 must be built and webhook wired |
| Analytics | Not ready | GTM tags, DLVs, and triggers must be published |
| Paid traffic | Not ready | Backend + analytics both required before paid ads use chatbot as a conversion signal |
