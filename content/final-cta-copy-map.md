# Final CTA Copy Map

Goal: replace weak or uncertain CTA language with confident luxury CTAs. The current site and pricing PDF use "INQUIRE" on every vessel card, which signals the price might not be real and invites negotiation. Published pricing deserves confident language.

CTA rules:
- Use "Check Availability" for main booking CTAs (hero, primary nav button)
- Use "Reserve Your Date" near pricing, package, and yacht detail sections
- Use "Find the Right Yacht" where users may be undecided (fleet or landing pages)
- Use "Talk to a Concierge" where trust or help is the main action
- Use "Request a Private Recommendation" for high touch luxury positioning
- Avoid aggressive or cheap sounding language

Note on locations: exact Elementor widget locations will be finalized against the elementor-*.json files once they are in the repo. The locations below reflect the live pricing PDF and the audit findings.

| Original CTA | New CTA | File / Template Location | Reason for change |
|---|---|---|---|
| Inquire | Reserve Your Date | Vessel pricing cards: Gratsky, Sugarree, CTX 80, Compass, Mirracle, Tranquility IV, Vasiliki, Freedom, Carpe Diem (pricing PDF and yacht detail templates) | Pricing is published. "Reserve Your Date" signals confidence, not negotiation, and sits naturally next to a price. |
| Inquire | Reserve Your Date | Pinnacle cards: Carpe Diem Premium, Another One | Same reasoning, top tier vessels especially benefit from confident reservation language. |
| Inquire (main hero or nav) | Check Availability | Homepage hero, primary navigation booking button | The primary booking action should read as a clear, confident next step. |
| Learn More | Find the Right Yacht | Fleet overview or undecided browsing sections | Moves an undecided visitor toward a guided choice rather than passive reading. |
| Get Started | Plan Your Celebration | Request to book intro or landing sections | Frames the action around the celebration, warmer and more specific. |
| Submit | Reserve Your Date | Booking form submit button | "Submit" is transactional and cold. The action is reserving a date. |
| Contact Us | Talk to a Concierge | Footer, help and contact areas | Positions the brand as concierge led, not a generic contact form. |
| Read More | Find the Right Yacht | Vessel teaser blocks | Pushes toward selection instead of more reading. |
| Send | Reserve Your Date | Form send button | Same as Submit, frame it around the outcome. |
| Inquire (high touch context) | Request a Private Recommendation | Premium or undecided high value sections | High touch language for the most elevated positioning. |

## CTA priority for paid traffic

1. Hero: Check Availability
2. Each vessel card: Reserve Your Date
3. Fleet or undecided: Find the Right Yacht
4. Help, trust, footer: Talk to a Concierge
5. Premium positioning: Request a Private Recommendation

## Verification

After the Elementor JSON edits, search the JSON and live pages for any remaining instances of: Inquire, Learn More, Get Started, Submit, Contact Us, Read More, Send. Replace any that remain per the table above. Leave form field internal names and tracking values unchanged, only the visible button text changes.
