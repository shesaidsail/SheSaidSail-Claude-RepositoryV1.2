# She Said Sail: Luxury Concierge Chatbot Conversation Flow
**Version:** 1.0
**Date:** May 2026
**Branch:** feature/luxury-conversion-overhaul

This document defines the full conversation tree for the She Said Sail luxury concierge chatbot. Every node, branch, message, and quick reply is specified here. The implementation in chatbot-js.js follows this exact structure.

---

## DESIGN PRINCIPLES

1. One question at a time. Never stack two questions in a single message.
2. Move the conversation forward. Every message has a next step.
3. Collect data invisibly. Qualification happens through natural conversation, not a form.
4. Recommend with confidence. The bot does not present all options and ask the guest to choose. It guides.
5. Know when to stop. Once email is captured, the handoff happens. No endless follow-up questions.
6. The tone is warm hospitality, not support desk. Never robotic. Never overexcited.

---

## TRIGGER CONDITIONS

**Auto-trigger (proactive):**
- On homepage: after 60 seconds of page activity (scroll or mouse movement). Not on page load.
- On experience pages: after 45 seconds. Visitor is already evaluating; engage sooner.
- On /request-to-book/ page: do NOT auto-trigger. Visitor is already taking action.
- Mobile: proactive trigger disabled. Widget available but never auto-opens on mobile.

**Manual trigger:**
- Visitor clicks the chat widget at any time.
- No limit on manual triggers.

**Session guard:**
- If the conversation has already started in this session, reopening shows the existing thread.
- Do not restart the conversation on re-open.

---

## STATE MAP OVERVIEW

```
STATE 0: Idle (widget closed)
STATE 1: Opener
STATE 2: Occasion branch
  2A: Bachelorette
  2B: Birthday
  2C: Girls Trip
  2D: Intimate / Anniversary
  2E: Other / Exploring
STATE 3: Experience recommendation
STATE 4: Group size (if not already captured)
STATE 5: Date
STATE 6: Contact capture (first name, email, optional phone)
STATE 7: Handoff message
STATE 8: Close
```

---

## STATE 0: IDLE

Widget is visible as a compact launcher in the bottom right corner.
Launcher label: "Concierge" in Cormorant Garamond italic, 13px.
On hover: subtle gold glow (see chatbot-css.css).

---

## STATE 1: OPENER

**Trigger:** Widget opened (manually or auto-triggered).

**Bot message (sent after 800ms typing indicator):**
"Hi there. What kind of day are you planning for your group?"

**Quick reply options (presented as pill buttons below the message):**
- "Bachelorette party"
- "Birthday celebration"
- "Girls trip"
- "Something more intimate"
- "Still exploring"

**Free text also accepted.** The JS detects keywords and routes to the appropriate branch.

**GTM event pushed:** `chatbot_open`, `chatbot_start_conversation`

---

## STATE 2A: BACHELORETTE

**Trigger:** User selects "Bachelorette party" or types any of: bachelorette, bach, bride, future mrs, bridal

**Bot message:**
"A bachelorette in Miami. Great. Is the group more into a high-energy social day, or something more elevated and curated?"

**Quick replies:**
- "High energy, music, movement"
- "Elevated and curated"
- "Somewhere in between"

**Collected data:** `occasion = "bachelorette"`

**Branch to STATE 3 with experience recommendation:**
- "High energy" → Pink Palm Club
- "Elevated and curated" → Monaco Social
- "Somewhere in between" → Monaco Social (primary), ask group size for secondary recommendation

---

## STATE 2B: BIRTHDAY

**Trigger:** User selects "Birthday celebration" or types: birthday, bday, turning, celebrating [number]

**Bot message:**
"A birthday celebration. I love that. How many people are you thinking?"

**Quick replies:**
- "4 to 8 guests"
- "9 to 15 guests"
- "16 or more"

**Collected data:** `occasion = "birthday"`

**Branch to STATE 3 with experience recommendation:**
- 4 to 8 → Golden Hour Escape (primary), Monaco Social (secondary)
- 9 to 15 → Monaco Social (primary)
- 16+ → Pink Palm Club

---

## STATE 2C: GIRLS TRIP

**Trigger:** User selects "Girls trip" or types: girls trip, girls weekend, getaway, girls

**Bot message:**
"A girls trip is one of my favorites to help plan. What kind of energy is the group going for?"

**Quick replies:**
- "Social and lively"
- "Relaxed and scenic"
- "Bit of both"

**Collected data:** `occasion = "girls_trip"`

**Branch to STATE 3:**
- Social → Rose Day Club (primary), Pink Palm Club (secondary)
- Relaxed → Golden Hour Escape (primary)
- Both → Rose Day Club

---

## STATE 2D: INTIMATE / ANNIVERSARY

**Trigger:** User selects "Something more intimate" or types: anniversary, intimate, proposal, just us, couple, relationship, milestone

**Bot message:**
"Our Golden Hour Escape was designed for moments like that. It is quieter, more personal, and timed around the light of late afternoon. Can I tell you a bit more about it?"

**Quick replies:**
- "Yes, tell me more"
- "What other options do you have?"

**Collected data:** `occasion = "intimate"`, pre-selected: `selected_experience = "golden-hour-escape"`

**If "tell me more":**
Bot: "It runs about 3 to 4 hours, fits up to 12 guests, and the experience is designed to feel slow and intentional. Not a party. Just a beautiful afternoon on the water. Starting from $10,000. Is this for a specific date, or are you still in early planning?"
→ Skip to STATE 5 (date)

**If "other options":**
→ Go to STATE 3 with all experiences listed briefly

---

## STATE 2E: STILL EXPLORING

**Trigger:** User selects "Still exploring" or types: not sure, maybe, exploring, thinking, don't know

**Bot message:**
"That is a good place to start. Can you tell me a little about the occasion? Even just a word or two works."

**[Free text input - no quick replies]**

**Collected data:** `occasion = [free text input]`

**JS routes based on keyword detection** from the free text response into the most appropriate branch (2A through 2D). If no clear keyword match, bot responds:

"Got it. We have four experiences that cover different energies, from quiet and intimate to social and lively. What matters more to your group: the atmosphere, the group size, or the timing?"

**Quick replies:**
- "The atmosphere"
- "The group size"
- "The timing"

Then routes to a simplified STATE 3 overview.

---

## STATE 3: EXPERIENCE RECOMMENDATION

The bot recommends one primary experience based on occasion and energy. It describes the experience emotionally, not technically.

**Recommendation messages:**

**Pink Palm Club:**
"Pink Palm Club sounds like it could be exactly right. It is designed for larger groups who want music, movement, and a real Miami energy. High energy, social, and completely private. Up to 22 guests."

**Monaco Social:**
"Monaco Social is probably the best fit. Think champagne, Riviera energy, and a polished afternoon on the water. It is our most popular choice for bachelorettes and birthday groups who want something memorable without it feeling like a party boat."

**Golden Hour Escape:**
"The Golden Hour Escape tends to be perfect for that. It is quieter, more personal, and timed around sunset. The kind of afternoon where you slow down and actually feel like you are somewhere special. Up to 12 guests."

**Rose Day Club:**
"Rose Day Club was basically made for that. A warm afternoon charter with a social, hosted feel. Good rosé, good music, everyone together. It tends to be the one groups end up booking every year."

**After recommendation, follow with:**
"Does that sound like the right direction?"

**Quick replies:**
- "Yes, that sounds right"
- "Tell me more"
- "What are the other options?"

**If "yes" or "tell me more":**
→ Collect group size if not already captured (STATE 4), then move to STATE 5.

**If "other options":**
Bot gives a brief 2-line summary of each experience, then asks "Which feels closest?"

---

## STATE 4: GROUP SIZE (if not already captured)

**Bot message:**
"How many people are you thinking? An approximate is fine."

**Quick replies:**
- "Under 10"
- "10 to 15"
- "16 or more"
- "Not sure yet"

**Collected data:** `guest_count = [value]`

→ Proceed to STATE 5.

---

## STATE 5: DATE

**Bot message:**
"Do you have a date in mind, or are you still in the early planning stages?"

**Quick replies:**
- "I have a date"
- "Still planning"

**If "I have a date":**
Bot: "What date are you looking at?"
[Free text input]
**Collected data:** `preferred_date = [input]`

**If "still planning":**
Bot: "No problem at all. Our concierge can check availability across several dates once we connect."
**Collected data:** `preferred_date = "flexible"`

→ Proceed to STATE 6.

---

## STATE 6: CONTACT CAPTURE

**Step 6a: First name**
Bot: "Perfect. What is your first name? I would love to make sure a concierge follows up with the right details for you."
[Free text input]
**Collected data:** `first_name = [input]`

**GTM event pushed:** chatbot_select_experience (if not already pushed)

**Step 6b: Email**
Bot: "Thanks, [first_name]. What is the best email address to reach you?"
[Email input with basic format validation]
**Collected data:** `email = [input]`

**GTM event pushed:** chatbot_capture_email

**Step 6c: Phone (optional)**
Bot: "And a phone number if you would like to hear back by text? Completely optional."
**Quick replies:**
- [Free text input for phone]
- "Skip for now"

**Collected data:** `phone = [input or null]`

If phone entered: **GTM event pushed:** chatbot_capture_phone

→ Proceed to STATE 7.

---

## STATE 7: HANDOFF

**Bot message:**
"You are all set, [first_name]. I am going to have a concierge review your details and reach out within 24 hours with the best availability for [selected_experience]. Is there anything specific you would like them to know?"

**Quick replies:**
- "That is everything"
- [Free text input for any additional notes]

**Collected data:** `conversation_summary = [any additional notes or null]`

**Actions triggered:**
- POST payload to Make.com M-CHATBOT-001 webhook
- Push GTM event: `chatbot_handoff`
- Push GTM event: `chatbot_complete`

→ Proceed to STATE 8.

---

## STATE 8: CLOSE

**Bot message:**
"Talk soon. In the meantime, you are welcome to browse the experiences at shesaidsail.com/experiences/ if you would like to see more before we connect."

**[No quick replies. Conversation ends.]**

Widget remains open but input is disabled. A subtle "Chat ended" state appears.

---

## ESCALATION RULES

**Escalate to human concierge when:**
- User explicitly asks to speak to a person ("Can I talk to someone?", "Is there a real person?")
- User has a very specific operational question the bot cannot answer (specific vessel, specific date availability, specific pricing)
- User has expressed frustration more than once
- Conversation has gone past 10 exchanges without reaching STATE 6

**Escalation message:**
"Of course. Let me get a concierge to take over from here. They will reach out to you directly within a few hours. Can I confirm your name and email so they know who to contact?"
→ Collect name and email, then send to M-CHATBOT-001 with escalation flag.

**Stop asking questions when:**
- Email has been captured (STATE 6b complete)
- Do not ask for phone if user already declined
- Do not re-ask for occasion or group size already answered

---

## DEAD-END PREVENTION

**If user goes silent for 90 seconds during conversation:**
Bot: "Still there? No rush."

**If user sends a message the bot cannot understand after 2 attempts:**
Bot: "I want to make sure I get this right for you. The quickest path is having a concierge reach out directly. Can I get your name and email?"
→ Jump to STATE 6.

**If user asks a question outside the scope of booking:**
(E.g., "What is the weather like in Miami?", "Do you do corporate events?")
Bot gives a brief honest answer where possible, then redirects:
"We specialize in private celebrations for groups. Would it help if a concierge reached out to discuss what might work for your situation?"

---

## TIMING AND PACING

| Action | Delay |
|---|---|
| First bot message after widget open | 800ms |
| Bot response to user input | 1000ms to 1400ms (randomized, feels human) |
| Typing indicator duration | 800ms to 1200ms |
| Quick replies appear after message | 300ms |
| Auto-trigger (homepage) | 60 seconds of activity |
| Auto-trigger (experience pages) | 45 seconds of activity |

---

## EXPERIENCE QUICK REFERENCE

| Experience | Slug | Cap | Best For |
|---|---|---|---|
| Monaco Social | monaco-social | 18 | Bachelorettes (elevated), birthdays (9-15) |
| Golden Hour Escape | golden-hour-escape | 12 | Intimate groups, anniversaries, small birthdays |
| Rose Day Club | rose-day-club | 18 | Girls trips (social), birthday afternoons |
| Pink Palm Club | pink-palm-club | 22 | Bachelorettes (high energy), large groups |
