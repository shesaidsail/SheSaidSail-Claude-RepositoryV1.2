# About Page: Backend Notes

**Page:** `/about/`
**Last updated:** 2026-05-18

---

## Forms

No form exists on this page. No hidden fields are needed. No form submission data is collected from `/about/`.

---

## Make.com Scenarios

No Make.com scenarios are triggered by this page. There is nothing to configure in Make for the current state of the About page.

---

## Airtable

No Airtable records are created by this page. Visitors to `/about/` do not write any data to Airtable directly.

---

## Future Integration Note

If a contact or inquiry CTA is added to this page in the future (for example, an inline inquiry form or a modal trigger), use the existing **M-BRAND-ROUTER** scenario pattern.

Set the `source_url` field to `shesaidsail.com/about` so the referral origin is identifiable in Airtable alongside requests that arrive from other pages. This is consistent with how source tracking works across the rest of the site.

No new Make scenario needs to be created for this purpose. M-BRAND-ROUTER already handles routing based on `source_url`.

---

## GTM Note

The global JavaScript layer fires a `view_about_page` event when a visitor loads any page with the `/about/` path. This event is available immediately in GTM Preview without any page-specific configuration.

Recommended action: use `view_about_page` to build a GA4 audience for remarketing. Target visitors who viewed the About page but did not complete a `submit_booking_form` event. This audience captures warm but undecided visitors who showed brand interest and can be re-engaged via paid social or display.

See `about-analytics.md` for the full GTM and GA4 setup instructions.
