# She Said Sail: Mobile QA Checklist

Test on all three viewport sizes. Use Chrome DevTools > Toggle Device Toolbar to simulate each device. Also test on at least one real device if possible.

Reviewer: _____________________ Date: _____________________

**Devices to test:**
- iPhone 14: 390px wide
- iPhone SE: 375px wide
- Android mid-range: 360px wide

Mark each item for each device. If an item passes on all three, mark once as Pass. Note the device if a failure is device-specific.

---

## Hero Section

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 1 | Hero image fills the full width of the viewport with no white gaps on sides | | | | |
| 2 | Hero headline text is readable (minimum 28px equivalent, no overflow or truncation) | | | | |
| 3 | Hero subheadline text is readable and does not overlap the headline | | | | |
| 4 | Primary CTA button in hero is at minimum 48px tall and full-width or appropriately sized | | | | |
| 5 | CTA button text is fully visible (no clipping) | | | | |
| 6 | Occasion pills (Bachelorette, Birthday, Girls Trip) stack or wrap cleanly without overflow | | | | |

---

## Navigation

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 7 | Mobile hamburger or nav menu is visible and functional | | | | |
| 8 | Nav menu items are readable and each tap target is at minimum 44px tall | | | | |
| 9 | Logo is visible and not cut off | | | | |

---

## Experience Cards

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 10 | All 4 experience cards are visible (stacked in single column on mobile) | | | | |
| 11 | Card images are not stretched or distorted | | | | |
| 12 | Card titles and descriptions are readable | | | | |
| 13 | Card CTA buttons are full-width or appropriately sized on mobile | | | | |

---

## Social Proof Strip

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 14 | Social proof strip is visible on homepage below hero | | | | |
| 15 | Review text is readable (not too small) | | | | |
| 16 | Star ratings or review icons display correctly | | | | |
| 17 | Reviewer names or attributes are visible | | | | |

---

## Email Capture Section

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 18 | Email capture section is visible near the bottom of the homepage | | | | |
| 19 | Email input field is full-width and easy to tap | | | | |
| 20 | Subscribe button is clearly visible and tappable | | | | |
| 21 | On successful submit, a confirmation message or redirect works correctly | | | | |

---

## CTAs and Links

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 22 | All CTA buttons link to the correct pages | | | | |
| 23 | Phone number link opens the phone dialer on tap | | | | |
| 24 | All links are functional (no 404s) | | | | |

---

## Forms

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 25 | Request to Book form fields are full-width and easy to tap | | | | |
| 26 | Keyboard appears correctly when tapping a text field | | | | |
| 27 | Date picker opens correctly on mobile for the Preferred Date field | | | | |
| 28 | Form submit button is visible and not hidden below the fold when the keyboard is open | | | | |

---

## Layout and Readability

| # | Check | iPhone 14 | iPhone SE | Android 360 | Notes |
|---|---|---|---|---|---|
| 29 | No horizontal scroll on any page (homepage, /request-to-book/, /experiences/) | | | | |
| 30 | Body text is readable at default browser zoom (minimum 16px equivalent) | | | | |

---

## Sign-Off

All 30 items must be marked as Pass before mobile QA is complete.

Signed: _____________________ Date: _____________________
