# Thank You Page: QA Checklist

Page: /thank-you/
Purpose: Post-conversion confirmation. No form. No sales pressure.

---

## Desktop QA (1440px viewport)

| Check | Pass | Fail | Notes |
|---|---|---|---|
| All 3 sections render in correct order (header, steps, soft next step) | | | |
| Section 1 background is cream (#FAF8F3) | | | |
| Section 1 eyebrow "REQUEST RECEIVED" is uppercase, gold, small caps style | | | |
| H1 "You are in good hands." renders in Cormorant Garamond, 48px, navy | | | |
| Subline renders in Inter, 18px, muted color | | | |
| Gold divider (60px wide) is visible below subline | | | |
| Section 2 background is white | | | |
| Section 2 heading "What happens next" renders in Cormorant Garamond, 32px, navy | | | |
| 3 steps display in a horizontal row | | | |
| Gold italic numerals (01, 02, 03) are visible in Cormorant Garamond | | | |
| Step headings render in Inter 600, 16px, navy | | | |
| Step body text renders in Inter 400, 15px, muted | | | |
| Section 3 background is warm cream (#F5F0E8) | | | |
| Section 3 heading "While you wait" is italic Cormorant Garamond, 28px, navy | | | |
| Two text links present: "View the Experiences" and "Follow on Instagram" | | | |
| Links have gold bottom border, not filled button style | | | |
| No filled gold buttons on this page | | | |

---

## Mobile QA (375px viewport)

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Section 1 text is readable and not overflowing | | | |
| H1 font size reduces appropriately (36px) | | | |
| Subline remains legible at 16px | | | |
| 3 steps stack to a single column layout | | | |
| Each step is fully readable, numerals and text aligned correctly | | | |
| Section 3 links stack vertically | | | |
| Both links are tap-accessible (sufficient touch target size) | | | |
| No horizontal scroll on any section | | | |

---

## Content Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| H1 text is exactly: "You are in good hands." | | | |
| Section 2 heading is exactly: "What happens next" | | | |
| Step 01 heading: "We review your request" | | | |
| Step 01 body: "Your concierge reviews your date, group size, and any notes you included." | | | |
| Step 02 heading: "We reach out within 24 hours" | | | |
| Step 02 body: "Expect a personal message with next steps, not a generic confirmation." | | | |
| Step 03 heading: "You decide when you are ready" | | | |
| Step 03 body: "There is no pressure, no deposit required until you are happy with every detail." | | | |
| Section 3 heading: "While you wait" | | | |
| "View the Experiences" link points to /experiences/ | | | |
| "Follow on Instagram" link points to https://www.instagram.com/shesaidsail/ | | | |
| Instagram link opens in a new tab | | | |
| No form elements present on this page | | | |
| No aggressive sales language or re-pitch content | | | |

---

## Redirect Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Submitting the Request to Book form on the booking page redirects to exactly /thank-you/ | | | |
| Redirect URL includes trailing slash (/thank-you/ not /thank-you) | | | |
| Redirect confirmed in MetForm widget settings in Elementor | | | |
| No inline success message shown in place of redirect | | | |

---

## noindex Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| View page source: `<meta name="robots" content="noindex, nofollow" />` is present in `<head>` | | | |
| Canonical tag points to https://shesaidsail.com/thank-you/ | | | |
| No Open Graph tags present on this page | | | |
| Google Search Console: page is not indexed (check after deployment) | | | |

---

## Analytics Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| GTM Preview mode: `view_thank_you_page` event fires when /thank-you/ loads | | | |
| GA4 DebugView shows `view_thank_you_page` event on page load | | | |
| `view_thank_you_page` is marked as a conversion event in GA4 Admin > Events | | | |

---

## Pixel Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Meta Pixel Helper Chrome extension shows Lead or Purchase event firing on page load | | | |
| TikTok Pixel Helper shows CompleteRegistration or PlaceAnOrder event firing on page load | | | |

---

## Suppression Audience Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| Meta Ads Manager: suppression audience based on Lead/Purchase pixel event exists | | | |
| Meta Ads Manager: suppression audience applied as exclusion to active ad sets | | | |
| TikTok Ads Manager: suppression audience based on CompleteRegistration event exists | | | |
| TikTok Ads Manager: suppression audience applied as exclusion to active ad groups | | | |

---

## Brand and Tone Verification

| Check | Pass | Fail | Notes |
|---|---|---|---|
| No em dashes anywhere on the page | | | |
| Tone is calm, warm, and reassuring (not automated or transactional) | | | |
| No sales pressure language present | | | |
| No calls to action pushing the visitor to submit another form | | | |
| Page feels like a message from a person, not a system confirmation | | | |

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| Developer | | | |
| QA Reviewer | | | |
| Brand/Copy Reviewer | | | |
| Analytics Reviewer | | | |
| Final Approval | | | |
