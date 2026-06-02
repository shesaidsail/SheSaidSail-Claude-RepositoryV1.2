#!/usr/bin/env python3
"""Apply She Said Sail conversion psychology fixes to Elementor exports.

Reads every file in elementor-source/, writes an updated import-ready copy
to elementor-updated/. Only text-bearing fields are changed. Element IDs,
widget types, styling, responsive settings, and form widgets are preserved.
No em dashes are introduced.
"""
import json, os, glob, uuid, copy

SRC = "elementor-source"
OUT = "elementor-updated"
os.makedirs(OUT, exist_ok=True)

# --- CTA and demo-phrase replacements (exact match on text-bearing fields) ---
PHRASE_MAP = {
    "Get Started": "Check Availability",
    "Learn More": "Find the Right Yacht",
    "Contact Us": "Talk to a Concierge",
    "Book Now": "Check Availability",
    "Book a yacht": "Reserve Your Date",
    "Book A Yacht": "Reserve Your Date",
    "Let's Talk!": "Talk to a Concierge",
    "Let’s Talk!": "Talk to a Concierge",
    "Get In Touch": "Talk to a Concierge",
    "Booking Form": "Reserve Your Date",
    "Rent This Yacht": "Reserve This Yacht",
    "Trusted by 1000+ clients around the world": "Curated celebrations across Miami and Fort Lauderdale",
}
# Substring replacements applied inside any text-bearing field (not URLs/ids).
# Ordered: most specific first.
SUBSTR_MAP = {
    "odysea@mail.com": "hello@shesaidsail.com",
    "Odysea": "She Said Sail",
    "odysea": "She Said Sail",
}

BRAND_PARAS = [
    "Every She Said Sail day is curated from start to finish. Premium beverages, fresh florals, charcuterie, a captain and crew, and concierge planning are handled before you arrive. You just show up.",
    "This is a produced experience, not a rental. Everything is set, placed, and timed in advance so your group can relax into the day.",
    "From the first message to the last sunset, our concierge team shapes the day around your group, your occasion, and the celebration you have in mind.",
]
BRAND_HEADING = "Designed Around Your Celebration"

# Real FAQ set used to replace the 6 demo accordion questions (by index)
FAQ = [
    ("What happens if the weather changes?",
     "Weather happens. If conditions are not suitable for your charter, our team will walk you through the available rescheduling options and coordinate next steps with the vessel provider. You will not be left to sort it out alone."),
    ("Can you help us choose the right yacht?",
     "That is exactly what we do. Tell us your date, group size, and the kind of day you have in mind, and our concierge team will point you toward the vessels that fit best."),
    ("How far in advance should we book?",
     "Weekend and peak season dates move quickly, so earlier is always better. If your date is close, reach out anyway and we will tell you honestly what is still open."),
    ("Can we bring alcohol?",
     "Premium beverages are already included in every experience, and champagne is part of the arrival. If you would like to bring something specific, just mention it when you reach out."),
    ("How does reserving a date work?",
     "Once we confirm availability for your date and vessel, we send the next steps to secure it. The process is simple, and we guide you through each part."),
    ("What happens after we request availability?",
     "Our concierge team reviews your date and group, confirms the right vessel options, and follows up with clear next steps. No long sales process, just a straight path to your day on the water."),
]

TESTIMONIAL_PLACEHOLDER = ("[REAL TESTIMONIAL NEEDED] Add a real, permissioned client quote here. "
                           "See content/testimonials-needed.md.")

_counter = {"p": 0}

def has_lorem(s):
    return isinstance(s, str) and "lorem ipsum" in s.lower()

def brand_para():
    p = BRAND_PARAS[_counter["p"] % len(BRAND_PARAS)]
    _counter["p"] += 1
    return p

def fix_phrases(s):
    if not isinstance(s, str):
        return s
    if s in PHRASE_MAP:
        return PHRASE_MAP[s]
    for a, b in SUBSTR_MAP.items():
        if a in s:
            s = s.replace(a, b)
    return s

def fix_body(s, wrap_p=False):
    """Body text: replace lorem with brand copy, else phrase/substr fix."""
    if has_lorem(s):
        para = brand_para()
        return f"<p>{para}</p>" if (wrap_p or s.strip().startswith("<")) else para
    return fix_phrases(s)

def fix_heading(s):
    if has_lorem(s):
        return BRAND_HEADING
    return fix_phrases(s)

# Counters
stats = {"cta": 0, "lorem": 0, "testimonial": 0, "faq": 0, "peter": 0}

def walk(node):
    if isinstance(node, dict):
        wt = node.get("widgetType")
        st = node.get("settings")
        if isinstance(st, dict):
            # Buttons / generic text CTAs
            for k in ("text", "button_text"):
                if k in st and isinstance(st[k], str):
                    new = fix_phrases(st[k])
                    if new != st[k]:
                        if st[k] in PHRASE_MAP:
                            stats["cta"] += 1
                        st[k] = new
            # Headings
            if "title" in st and isinstance(st["title"], str):
                old = st["title"]
                new = fix_heading(old)
                if new != old:
                    if has_lorem(old):
                        stats["lorem"] += 1
                    st["title"] = new
            # image-box / icon-box / call-to-action description and title text
            for k in ("description_text", "title_text", "sub_title", "caption", "description"):
                if k in st and isinstance(st[k], str):
                    old = st[k]
                    new = fix_body(old, wrap_p=old.strip().startswith("<"))
                    if new != old:
                        if has_lorem(old):
                            stats["lorem"] += 1
                        st[k] = new
            # Text editor bodies
            if "editor" in st and isinstance(st["editor"], str):
                old = st["editor"]
                if old.strip() in ("<p>Peter Lawson</p>", "Peter Lawson"):
                    st["editor"] = "<p>Real testimonial needed</p>"
                    stats["peter"] += 1
                else:
                    new = fix_body(old, wrap_p=True)
                    if new != old:
                        if has_lorem(old):
                            stats["lorem"] += 1
                        st["editor"] = new
            # ElementsKit accordion (FAQ)
            if "ekit_accordion_items" in st and isinstance(st["ekit_accordion_items"], list):
                for i, item in enumerate(st["ekit_accordion_items"]):
                    q, a = FAQ[i % len(FAQ)]
                    if "acc_title" in item:
                        item["acc_title"] = q
                        stats["faq"] += 1
                    if "acc_content" in item:
                        item["acc_content"] = f"<p>{a}</p>"
            # ElementsKit testimonial data
            if "ekit_testimonial_data" in st and isinstance(st["ekit_testimonial_data"], list):
                for item in st["ekit_testimonial_data"]:
                    if "client_name" in item:
                        item["client_name"] = "Real testimonial needed"
                    if "designation" in item:
                        item["designation"] = ""
                    if "review" in item:
                        item["review"] = TESTIMONIAL_PLACEHOLDER
                    stats["testimonial"] += 1
            # icon-list items text
            if "icon_list" in st and isinstance(st["icon_list"], list):
                for item in st["icon_list"]:
                    if isinstance(item, dict) and isinstance(item.get("text"), str):
                        old = item["text"]
                        new = fix_body(old)
                        if new != old:
                            if has_lorem(old):
                                stats["lorem"] += 1
                            item["text"] = new
        for v in node.values():
            walk(v)
    elif isinstance(node, list):
        for v in node:
            walk(v)

for path in sorted(glob.glob(f"{SRC}/*.json")):
    with open(path) as f:
        data = json.load(f)
    walk(data)
    out = os.path.join(OUT, os.path.basename(path))
    with open(out, "w") as f:
        json.dump(data, f, ensure_ascii=True, separators=(",", ":"))

print("Stats:", json.dumps(stats))
print("Files written:", len(glob.glob(f"{OUT}/*.json")))
