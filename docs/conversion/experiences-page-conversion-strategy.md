# Experiences Page Conversion Strategy

**Version:** 1.0
**Date:** 2026-05-18
**Branch:** claude/fix-experiences-page-EwvlD
**Status:** Production Ready for WordPress Implementation

---

## Strategic Intent

The Experiences page is the primary atmosphere-selection surface for She Said Sail. Its conversion job is not to explain what each experience is -- it is to help a visitor feel which experience belongs to her, and then make requesting it feel effortless.

The page must shift register from:
"Here are four packages available to book"

to:

"Here is the kind of day you are choosing to give yourself and your group."

---

## Positioning Framework

### Core Positioning Statement

"This is not about choosing a boat. This is about choosing the energy of the day."

### Emotional Territory

The page should occupy the intersection of:
- Effortless luxury
- Social aspiration
- Intimate celebration
- Concierge hospitality

### Tone

- Calm, not urgent
- Confident, not salesy
- Editorial, not transactional
- Warm, not formal
- Feminine without being narrow

---

## Hero Section Strategy

### Primary Objective

Anchor the visitor emotionally before they scroll. The hero should not describe what the company does -- it should set the register of the decision they are about to make.

### Recommended H1 Direction

Option A: "Choose the atmosphere first."
Option B: "The atmosphere changes everything."
Option C: "Designed around the kind of day you want to have."

Selected for implementation: "Choose the atmosphere first."

Rationale: Short, emotionally direct, reframes the selection process, does not use the word "yacht" which can feel transactional.

### Recommended Subheadline

"Four experiences. Each one designed around a different kind of energy -- for birthdays, bachelorettes, girls trips, and intimate celebrations that deserve a day they will remember."

Rationale: Directly names the occasions without sounding SEO-stuffed. Emotional close rather than feature list.

### Hero Visual Direction

- Full-width image or video loop
- Warm golden light preferred
- Movement preferred over static poses
- Champagne, conversation, candid laughter
- No forced eye-contact-with-camera shots
- Overlay should be subtle, warm-tinted, allowing background to breathe

---

## Experience Card Strategy

### Card Hierarchy

Featured card (Monaco Social) should remain visually elevated: wider, taller, more prominent.

Secondary grid (3-column) carries the remaining three experiences.

### Atmosphere Differentiation Matrix

| Experience | Energy Level | Occasion Fit | Hosting Style | Atmosphere Label |
|---|---|---|---|---|
| Monaco Social | High, cinematic | Milestone birthdays, elevated celebrations | Champagne service, curated hosting | Elevated + Cinematic |
| Golden Hour Escape | Low, intimate | Intimate groups, quiet celebrations, couples | Slow-paced, relaxed | Intimate + Unhurried |
| Rose Day Club | Medium, social | Girls trips, bachelorettes, social groups | Swim platform, music, table setting | Social + Sun-Soaked |
| Pink Palm Club | High, vibrant | Miami-energy groups, social birthdays, nightlife-adjacent | Cocktail-forward, movement | Playful + Electric |

### Card Copy Framework

Each card must communicate five things:
1. Atmosphere (the feeling of being there)
2. Energy level (implicit, through language)
3. Occasion fit (who this is for)
4. Social identity (what kind of person chooses this)
5. Sensory detail (one concrete moment)

### Approved Card Copy

**Monaco Social**
Atmosphere label: Elevated and Cinematic

Headline copy: "Monaco Social"

Descriptor: "Champagne-forward Riviera energy for milestone birthdays, elevated celebrations, and long afternoons that feel cinematic. The kind of day that gets photographed."

Occasion badge: "Birthdays + Elevated Groups"

**Golden Hour Escape**
Atmosphere label: Intimate and Unhurried

Headline copy: "Golden Hour Escape"

Descriptor: "Slow coastal pacing designed for intimate groups, long conversations at sunset, and a hosting style that lets the afternoon breathe. Nothing rushed. Everything considered."

Occasion badge: "Intimate Groups + Quiet Celebrations"

**Rose Day Club**
Atmosphere label: Social and Sun-Soaked

Headline copy: "Rose Day Club"

Descriptor: "Swim platform energy, music drifting through the afternoon, beautifully set tables, and effortless movement between moments. Designed for groups that want everything to feel easy."

Occasion badge: "Girls Trips + Bachelorettes"

**Pink Palm Club**
Atmosphere label: Playful and Electric

Headline copy: "Pink Palm Club"

Descriptor: "Miami energy on the water. Cocktails, music, movement, and a group atmosphere that builds through the day. For the groups that want to feel the energy of where they are."

Occasion badge: "Social Groups + Vibrant Birthdays"

### CTA Copy

Primary card CTA: "Explore This Experience"
Secondary CTA visible on hover or mobile tap: "Request to Book"

---

## Social Proof Strategy

### Format

An editorial quote strip. Three quotes. No stars. No logos. No sliders.

### Quote Selection Criteria

- Sound like real people, not marketing copy
- Reference the feeling, not the logistics
- Avoid superlatives ("best", "amazing", "incredible")
- One sentence preferred, two maximum

### Approved Quotes

Quote 1: "This felt more like being hosted than renting a yacht."
Attribution: Birthday Group, Miami

Quote 2: "We did not have to think about anything all day."
Attribution: Bachelorette Party

Quote 3: "The atmosphere felt completely different from every other boat day we have done."
Attribution: Girls Trip, South Beach

### Placement

Between the experience grid and the bottom recommendation CTA. Serves as trust reinforcement before the final conversion ask.

---

## CTA Hierarchy

### Tier 1 (Primary): Request to Book
- Location: Navigation header (existing), bottom section
- Style: Gold button, navy text
- Copy: "Request to Book"
- Event: click_request_to_book

### Tier 2 (Secondary): Explore This Experience
- Location: Each experience card
- Style: Outlined or secondary button
- Copy: "Explore This Experience"
- Event: click_explore_experience

### Tier 3 (Soft): Get Recommendations
- Location: Bottom CTA section
- Style: Opens Tidio chat
- Copy: "Get Recommendations"
- Event: click_get_recommendations

### Rules

No competing primary CTAs on the same visual level. One clear action per section.

---

## Conversion Flow

1. Visitor arrives on Experiences page
2. Hero anchors emotional register: "Choose the atmosphere first"
3. Featured card communicates Monaco Social as the flagship experience
4. Grid section presents three more clearly differentiated options
5. Social proof strip reinforces trust before commitment
6. Bottom CTA captures undecided visitors with low-friction recommendation path
7. Navigation header maintains persistent "Request to Book" throughout scroll

---

## Attribution and Tracking

All card clicks and CTA interactions should push to GTM dataLayer.

UTM parameters should be captured on page load and stored in sessionStorage for downstream Airtable attribution.

See: docs/analytics/experiences-page-events.md
See: docs/backend/experiences-page-tracking-map.md
