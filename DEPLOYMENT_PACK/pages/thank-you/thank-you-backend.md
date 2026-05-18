# Thank You Page: Backend Notes

## Overview

This page has no form. No hidden fields are needed. No new backend automations are triggered by a visitor landing on this page.

All automation is triggered by the Request to Book form submission on the previous page (the booking/contact page containing the MetForm). By the time a visitor reaches /thank-you/, all backend processes have already been initiated.

---

## GTM Event Confirmation

- Event name: `view_thank_you_page`
- Trigger: fires automatically from the global site JS when the page path contains `/thank-you/`
- No additional GTM tags, triggers, or variables are required on this page
- No custom dataLayer pushes are needed

---

## Make.com

All automation is triggered by the Request to Book form submission (on the previous page). Nothing new triggers when a visitor lands on /thank-you/.

Automations already initiated by the time this page loads:

1. Airtable record creation (lead captured)
2. Internal notification to concierge team
3. Confirmation email to the submitter (if configured)

No new Make.com scenarios are needed for this page.

---

## Airtable

The Airtable record is already created by the time the visitor reaches this page. No write operations occur on /thank-you/.

---

## Verification Step: WordPress Redirect URL

This is the one backend item that must be confirmed during QA.

In WordPress, after MetForm processes a submission, it redirects the visitor to a confirmation URL. That URL must be exactly:

```
/thank-you/
```

Confirm the following:

- The redirect path is `/thank-you/` with a trailing slash, not `/thank-you` without one
- The path is not a different URL such as `/confirmation/`, `/success/`, or a full external URL
- WordPress does not show an inline success message instead of redirecting (inline message means the GTM event will not fire on the correct path)

Where to check: MetForm widget settings in Elementor, under the form's "Actions After Submit" or "Redirect" configuration. The redirect URL field should contain `/thank-you/`.

If the redirect path is wrong, the `view_thank_you_page` event will either not fire or fire on the wrong page, breaking all downstream conversion tracking.
