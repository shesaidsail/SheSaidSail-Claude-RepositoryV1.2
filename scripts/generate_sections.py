#!/usr/bin/env python3
"""Generate import-ready Elementor section templates for the new conversion
sections. Each is a valid Elementor 'section' export using core widgets
(and elementskit-accordion for FAQ, which the site already uses)."""
import json, os, uuid

OUT = "elementor-updated"
os.makedirs(OUT, exist_ok=True)

def hid():
    return uuid.uuid4().hex[:8]

def heading(title, size="h2"):
    return {"id": hid(), "elType": "widget", "widgetType": "heading",
            "settings": {"title": title, "header_size": size, "align": "center"},
            "elements": [], "isInner": False}

def text(html):
    return {"id": hid(), "elType": "widget", "widgetType": "text-editor",
            "settings": {"editor": html, "align": "center"},
            "elements": [], "isInner": False}

def icon_list(items):
    return {"id": hid(), "elType": "widget", "widgetType": "icon-list",
            "settings": {"icon_list": [
                {"text": t, "_id": hid(),
                 "selected_icon": {"value": "fas fa-check", "library": "fa-solid"},
                 "link": {"url": "", "is_external": "", "nofollow": "", "custom_attributes": ""}}
                for t in items]},
            "elements": [], "isInner": False}

def accordion(pairs):
    return {"id": hid(), "elType": "widget", "widgetType": "elementskit-accordion",
            "settings": {"ekit_accordion_items": [
                {"acc_title": q, "acc_content": f"<p>{a}</p>",
                 "ekit_acc_is_active": "", "_id": hid()} for q, a in pairs]},
            "elements": [], "isInner": False}

def container(children):
    return {"id": hid(), "elType": "container",
            "settings": {"flex_direction": "column", "content_width": "boxed",
                         "padding": {"unit": "px", "top": "80", "right": "0",
                                     "bottom": "80", "left": "0", "isLinked": False}},
            "elements": children, "isInner": False}

def export(title, children):
    return {"content": [container(children)], "page_settings": [],
            "version": "0.4", "title": title, "type": "section"}

def write(name, doc):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(doc, f, ensure_ascii=True, separators=(",", ":"))

# How It Works
write("section-how-it-works.json", export("How She Said Sail Works", [
    heading("How She Said Sail Works"),
    icon_list([
        "Tell us about your group. Share your date, occasion, guest count, and what kind of day you want.",
        "We recommend the right yacht. Our concierge team narrows the options and points you toward the best fit.",
        "Reserve your date. Once availability is confirmed, we send the next steps to secure your charter.",
        "We handle the details. From timing to add ons, our team helps make the day feel effortless.",
        "Show up and enjoy it. Your group arrives ready for a private yacht experience built around your celebration.",
    ]),
]))

# Why She Said Sail
write("section-why-she-said-sail.json", export("Why Groups Choose She Said Sail", [
    heading("Why Groups Choose She Said Sail"),
    icon_list([
        "Curated yacht recommendations instead of overwhelming boat lists",
        "Concierge style planning from inquiry to charter day",
        "Celebration first experiences for bachelorettes, birthdays, girls trips, and private events",
        "Miami and Fort Lauderdale yacht options",
        "Add ons available for a more elevated day",
        "A planning process designed to feel clear, calm, and handled",
    ]),
]))

# Founder
write("section-founder.json", export("Meet the Team Behind She Said Sail", [
    heading("Meet the Team Behind She Said Sail"),
    text("<p>[FOUNDER PHOTO TO BE ADDED]</p>"),
    text("<p>She Said Sail was built to make private yacht experiences feel more curated, "
         "more personal, and easier to plan. The goal is simple: help groups celebrate on "
         "the water without the stress of figuring everything out alone.</p>"),
]))

# FAQ conversion block (full 10)
faq_pairs = [
    ("What happens if the weather changes?",
     "Weather happens. If conditions are not suitable for your charter, our team will walk you through the available rescheduling options and coordinate next steps with the vessel provider. You will not be left to sort it out alone."),
    ("Can we bring alcohol?",
     "Premium beverages are already included in every experience, and champagne is part of the arrival. If you would like to bring something specific, just mention it when you reach out and we will let you know what works on your vessel."),
    ("Can you help us choose the right yacht?",
     "That is exactly what we do. Tell us your date, group size, and the kind of day you have in mind, and our concierge team will point you toward the vessels that fit best. You do not need to study the whole fleet."),
    ("How far in advance should we book?",
     "Weekend and peak season dates move quickly, so earlier is always better. If your date is close, reach out anyway and we will tell you honestly what is still open."),
    ("Do we need to know exactly what yacht we want?",
     "Not at all. Most groups come to us with a date and an occasion, not a vessel. We narrow the options for you."),
    ("Can you help with bachelorette details or add ons?",
     "Yes. From a DJ or photographer to champagne service, florals, and gift bags, we can shape the day around your group. Add ons are optional, and we only suggest what fits."),
    ("How does reserving a date work?",
     "Once we confirm availability for your date and vessel, we send the next steps to secure it. The process is simple, and we guide you through each part."),
    ("Are yachts available in Miami and Fort Lauderdale?",
     "Yes. We operate across South Florida, with vessels departing from both Miami and Fort Lauderdale."),
    ("Can you help with birthdays, girls trips, and private events?",
     "Absolutely. Bachelorettes, milestone birthdays, girls trips, and private celebrations are the heart of what we do."),
    ("What happens after we request availability?",
     "Our concierge team reviews your date and group, confirms the right vessel options, and follows up with clear next steps. No long sales process, just a straight path to your day on the water."),
]
write("section-faq-conversion.json", export("Questions, Answered", [
    heading("Questions, Answered"),
    accordion(faq_pairs),
]))

print("Generated 4 section templates")
