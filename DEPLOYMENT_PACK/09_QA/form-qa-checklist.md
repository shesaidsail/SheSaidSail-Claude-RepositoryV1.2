# She Said Sail: Form QA Checklist

Covers both forms: the Request to Book form on /request-to-book/ and the email capture form on the homepage.

Reviewer: _____________________ Date: _____________________

---

## Section A: Request to Book Form (/request-to-book/)

### Visible Fields

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 1 | Full Name field is present and labeled correctly | | | |
| 2 | Email field is present and labeled correctly | | | |
| 3 | Phone field is present and labeled correctly | | | |
| 4 | Occasion dropdown/select is present with all 6 options: Bachelorette, Birthday, Girls Trip, Celebration, Corporate, Other | | | |
| 5 | Group Size field is present | | | |
| 6 | Preferred Date field is present with a date picker | | | |
| 7 | Flexible Dates checkbox is present | | | |
| 8 | Experience Interest field is present with all 6 options: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Custom, Undecided | | | |
| 9 | Message/Notes textarea is present | | | |
| 10 | Submit button is present and labeled correctly (e.g., "Submit Request" or "Send My Inquiry") | | | |

### Hidden Fields (Verify via DevTools Elements Tab)

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 11 | Hidden field `utm_source` is present in the form DOM | | | |
| 12 | Hidden field `utm_medium` is present | | | |
| 13 | Hidden field `utm_campaign` is present | | | |
| 14 | Hidden field `utm_content` is present | | | |
| 15 | Hidden field `utm_term` is present | | | |
| 16 | Hidden field `creative_id` is present | | | |
| 17 | Hidden field `landing_page` is present | | | |
| 18 | Hidden field `source_url` is present | | | |
| 19 | Hidden field `referrer_url` is present | | | |
| 20 | Hidden field `first_seen_at` is present | | | |
| 21 | Hidden field `submission_page` is present | | | |
| 22 | Hidden field `brand` is present | | | |
| 23 | Hidden field `service_category` is present | | | |
| 24 | Hidden field `selected_experience` is present | | | |

### Validation

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 25 | Submitting the form with Full Name empty shows a validation error | | | |
| 26 | Submitting the form with Email empty shows a validation error | | | |
| 27 | Submitting the form with Phone empty shows a validation error | | | |
| 28 | Submitting with an invalid email format (e.g., "notanemail") shows a validation error | | | |
| 29 | Validation errors appear inline near the relevant field (not only at the top of the form) | | | |
| 30 | No network request is fired to Make.com when validation fails | | | |

### UTM Field Population

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 31 | Load the form with: `?utm_source=test&utm_medium=cpc&utm_campaign=qa-test&creative_id=TEST-001` | | | |
| 32 | After page load, open DevTools > Elements > search for `utm_source`. Value is "test" | | | |
| 33 | `utm_medium` value is "cpc" | | | |
| 34 | `utm_campaign` value is "qa-test" | | | |
| 35 | `creative_id` value is "TEST-001" | | | |
| 36 | `brand` value is "shesaidsail" | | | |
| 37 | `service_category` value is "yacht-charter" | | | |
| 38 | `submission_page` value is "/request-to-book/" | | | |

### Form Submission Flow

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 39 | Form submits successfully with valid test data (no console errors) | | | |
| 40 | Make.com M-WEBFORM-REQUEST-CAPTURE scenario receives the payload (check Make.com run history) | | | |
| 41 | Airtable Requests table has a new record with the correct data | | | |
| 42 | Airtable UTMs table has a new linked record | | | |
| 43 | Airtable Contacts table has a new or updated Contact record | | | |
| 44 | Confirmation email arrives at the test email address within 5 minutes | | | |
| 45 | Slack alert fires in the correct channel within 2 minutes | | | |
| 46 | Browser redirects to /thank-you/ after successful submission | | | |

### Error Handling

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 47 | If the Make.com webhook is unreachable (simulate by temporarily using a bad URL), the user sees a friendly error message, not a raw error or blank screen | | | |
| 48 | The user is NOT redirected to /thank-you/ if the form submission fails | | | |

---

## Section B: Homepage Email Capture Form

| # | Check | Pass | Fail | Notes |
|---|---|---|---|---|
| 49 | Email input field is visible and labeled on the homepage | | | |
| 50 | Submit/Subscribe button is visible and functional | | | |
| 51 | Submitting an invalid email shows a validation error | | | |
| 52 | Submitting a valid email sends the payload to Make.com M-EMAIL-CAPTURE | | | |
| 53 | Airtable Contacts table receives the new Contact or updates the existing one | | | |
| 54 | User sees a confirmation message after successful email submission | | | |
| 55 | Hidden fields `utm_source`, `brand`, `landing_page` are present and populated | | | |

---

## Sign-Off

All items above must be marked Pass before the forms are considered QA complete.

Signed: _____________________ Date: _____________________
