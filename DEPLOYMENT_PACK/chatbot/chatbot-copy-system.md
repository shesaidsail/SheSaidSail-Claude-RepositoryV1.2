# She Said Sail: Chatbot Copy System
**Version:** 1.0
**Date:** May 2026

All message copy for the luxury concierge chatbot. Every line is governed by the rules in this document. The conversation flow references these rules. New messages written for the bot must pass these rules before being added.

---

## VOICE AND TONE RULES

**Always:**
- One sentence per thought. Short, clear, warm.
- First person singular, not plural ("I am going to have a concierge" not "We will have a concierge")
- Warm and helpful, like someone who genuinely wants this day to be right
- Confident. The bot knows the experiences well and guides, not presents options passively.
- Lightly conversational. "No rush." "I love that." "Good choice."

**Never:**
- Em dashes (use colons or commas instead)
- Exclamation marks (not even one)
- "Absolutely" / "Certainly" / "Of course" as openers
- "Amazing" / "Wonderful" / "Fantastic" / "Perfect" as openers (too robotic-enthusiastic)
- "Feel free to" (support-bot language)
- "Please" at the start of a sentence
- "Don't hesitate to" (corporate)
- "We'd be happy to" (generic)
- "Luxury" as an adjective about She Said Sail
- "Unforgettable" / "Once in a lifetime"
- All caps for emphasis
- Multiple question marks
- Emojis (unless user sends them first; then a single warm emoji response is acceptable)

**Tone by state:**

| State | Tone |
|---|---|
| Opener | Warm, open, curious |
| Occasion clarification | Interested, attentive |
| Experience recommendation | Confident, knowledgeable, descriptive |
| Contact capture | Friendly, low-pressure |
| Handoff | Reassuring, complete |
| Close | Warm, brief |
| Escalation | Calm, immediate |

---

## APPROVED OPENERS (for any new message the bot sends)

These words and phrases are approved to open a bot message:

- "A [occasion] in Miami." (factual acknowledgment, warm by position)
- "That sounds like a good place to start."
- "Got it."
- "Good choice."
- "Our [experience] tends to be perfect for that."
- "That is one of my favorites to help plan."
- "No problem at all."
- "You are all set."
- "Talk soon."
- "Perfect." (only in STATE 7/8, not earlier)

---

## ALL MESSAGE COPY (production-ready)

### STATE 1: OPENER
"Hi there. What kind of day are you planning for your group?"

---

### STATE 2A: BACHELORETTE
"A bachelorette in Miami. Great. Is the group more into a high-energy social day, or something more elevated and curated?"

---

### STATE 2B: BIRTHDAY
"A birthday celebration. I love that. How many people are you thinking?"

---

### STATE 2C: GIRLS TRIP
"A girls trip is one of my favorites to help plan. What kind of energy is the group going for?"

---

### STATE 2D: INTIMATE / ANNIVERSARY

Initial response:
"Our Golden Hour Escape was designed for moments like that. It is quieter, more personal, and timed around the light of late afternoon. Can I tell you a bit more about it?"

If user wants more detail:
"It runs about 3 to 4 hours, fits up to 12 guests, and the experience is designed to feel slow and intentional. Not a party. Just a beautiful afternoon on the water. Starting from $10,000. Is this for a specific date, or are you still in early planning?"

---

### STATE 2E: EXPLORING
"That is a good place to start. Can you tell me a little about the occasion? Even just a word or two works."

If no clear keyword detected:
"Got it. We have four experiences that cover different energies, from quiet and intimate to social and lively. What matters more to your group: the atmosphere, the group size, or the timing?"

---

### STATE 3: EXPERIENCE RECOMMENDATIONS

**Pink Palm Club:**
"Pink Palm Club sounds like it could be exactly right. It is designed for larger groups who want music, movement, and a real Miami energy. High energy, social, and completely private. Up to 22 guests."

**Monaco Social:**
"Monaco Social is probably the best fit. Think champagne, Riviera energy, and a polished afternoon on the water. It is our most popular choice for bachelorettes and birthday groups who want something memorable without it feeling like a party boat."

**Golden Hour Escape:**
"The Golden Hour Escape tends to be perfect for that. It is quieter, more personal, and timed around sunset. The kind of afternoon where you slow down and actually feel like you are somewhere special. Up to 12 guests."

**Rose Day Club:**
"Rose Day Club was basically made for that. A warm afternoon charter with a social, hosted feel. Good rosé, good music, everyone together. It tends to be the one groups end up booking every year."

**After recommendation (follow-up):**
"Does that sound like the right direction?"

**If user wants all options:**
"Here is a quick overview. Monaco Social: champagne, polished, social. Golden Hour Escape: quiet, sunset, intimate. Rose Day Club: warm afternoon, social, relaxed. Pink Palm Club: high energy, music, larger groups. Which feels closest to what you have in mind?"

---

### STATE 4: GROUP SIZE
"How many people are you thinking? An approximate is fine."

---

### STATE 5: DATE
"Do you have a date in mind, or are you still in the early planning stages?"

If user has a date:
"What date are you looking at?"

If user is still planning:
"No problem at all. Our concierge can check availability across several dates once we connect."

---

### STATE 6: CONTACT CAPTURE

**First name:**
"Perfect. What is your first name? I would love to make sure a concierge follows up with the right details for you."

**Email:**
"Thanks, [first_name]. What is the best email address to reach you?"

**Phone (optional):**
"And a phone number if you would like to hear back by text? Completely optional."

**Skip button label:** "Skip for now"

---

### STATE 7: HANDOFF
"You are all set, [first_name]. I am going to have a concierge review your details and reach out within 24 hours with the best availability for [experience_name]. Is there anything specific you would like them to know?"

**If user adds notes:**
"Got it. I will make sure they see that."
→ Then proceed to STATE 8.

**If user says nothing / "That is everything":**
→ Proceed to STATE 8 directly.

---

### STATE 8: CLOSE
"Talk soon. In the meantime, you are welcome to browse the experiences at shesaidsail.com/experiences/ if you would like to see more before we connect."

---

### ESCALATION
"Of course. Let me get a concierge to take over from here. They will reach out to you directly within a few hours. Can I confirm your name and email so they know who to contact?"

---

### DEAD END / SILENT USER
"Still there? No rush."

### UNRECOGNIZED INPUT (after 2 attempts)
"I want to make sure I get this right for you. The quickest path is having a concierge reach out directly. Can I get your name and email?"

### OUT OF SCOPE QUESTION
"That is a bit outside what I can help with here. If it is something specific about an experience or booking, our concierge can answer that directly. Would it help if they reached out?"

---

## QUICK REPLY BUTTON COPY

All quick replies are short (2 to 5 words), sentence case, no punctuation at the end.

| State | Quick Replies |
|---|---|
| Opener | "Bachelorette party", "Birthday celebration", "Girls trip", "Something more intimate", "Still exploring" |
| 2A Bachelorette energy | "High energy, music, movement", "Elevated and curated", "Somewhere in between" |
| 2B Birthday size | "4 to 8 guests", "9 to 15 guests", "16 or more" |
| 2C Girls trip energy | "Social and lively", "Relaxed and scenic", "Bit of both" |
| 2D Intimate - more info | "Yes, tell me more", "What other options do you have?" |
| 3 After recommendation | "Yes, that sounds right", "Tell me more", "What are the other options?" |
| 4 Group size | "Under 10", "10 to 15", "16 or more", "Not sure yet" |
| 5 Date | "I have a date", "Still planning" |
| 7 Handoff | "That is everything" |
| 6c Phone | "Skip for now" |
| 2E Topics | "The atmosphere", "The group size", "The timing" |

---

## TYPING INDICATOR BEHAVIOR

The bot shows a typing indicator before every message.
Indicator style: three small navy dots, pulsing animation.
Duration: 800ms minimum, 1400ms maximum.
Never skip the typing indicator. It creates pacing that feels human.

---

## EXPERIENCE NAME FORMATTING IN CHAT

Always use the exact experience name as written, not shortened or abbreviated:
- "Monaco Social" (not "Monaco" or "the Monaco")
- "Golden Hour Escape" (not "Golden Hour" or "the Escape")
- "Rose Day Club" (not "Rosé Day" or "the Rose")
- "Pink Palm Club" (not "Pink Palm" or "the Pink")

---

## PROHIBITED PHRASES (complete list)

These may not appear in any bot message under any circumstances:
- em dash (no Unicode U+2014, no -- used as an em dash)
- "Book now"
- "Fill out the form"
- "Click here"
- "Limited availability" (false urgency)
- "Don't miss out"
- "Luxury"
- "Unforgettable"
- "World-class"
- "Best in class"
- "Passionate about"
- "Excited to help"
- "Happy to assist"
- "How can I help you today?"
- "Is there anything else I can help you with?"
- "Thank you for contacting us"
- "Your inquiry has been received"
- "We will get back to you shortly"
- Any greeting starting with "Hello" or "Hey there"

---

## PERSONALIZATION RULES

Once the user provides their first name in STATE 6, the bot uses it exactly twice:
1. When confirming email: "Thanks, [first_name]."
2. In the handoff message: "You are all set, [first_name]."

Do not use the name again after STATE 7. It starts to feel sales-y if overused.

The experience name is used once in the handoff: "best availability for [experience_name]."
If no experience was selected (user escalated early), omit the experience reference: "best availability for your group."
