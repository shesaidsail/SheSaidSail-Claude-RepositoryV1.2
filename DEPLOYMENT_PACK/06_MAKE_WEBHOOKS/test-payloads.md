# She Said Sail: Make.com Test Payloads and Verification Steps

Use this document after all Make.com scenarios are built and active. Run these tests before enabling paid traffic.

---

## Test URL Format

Always open the site with test UTM parameters so you can identify test submissions in Airtable:

```
https://shesaidsail.com/request-to-book/?utm_source=test&utm_medium=test&utm_campaign=qa-test-20260518&creative_id=TEST-001
```

Replace `20260518` with today's date in YYYYMMDD format so you can find test records by date.

---

## Test 1: Standard Form Submission (M-WEBFORM-REQUEST-CAPTURE)

**What to send:**

Open the test URL above. Fill in the form with:
- Full Name: QA Test User
- Email: qa-test@example.com
- Phone: 305-555-0000
- Occasion: Bachelorette
- Group Size: 12
- Preferred Date: (any future date)
- Experience Interest: Monaco Social
- Message: This is a QA test submission. Please ignore.

Click Submit.

**What to verify in Airtable:**

- [ ] Requests table: new record exists with the form data
- [ ] Status = "New"
- [ ] Internal Rating = "Hot" (Bachelorette + group size >= 12 qualifies)
- [ ] Submitted At is populated with current timestamp
- [ ] UTMs table: new UTM record exists with utm_source = "test", utm_campaign = "qa-test-20260518", creative_id = "TEST-001"
- [ ] UTM record is linked to the new Request record
- [ ] Contacts table: new Contact exists with email = qa-test@example.com
- [ ] Contact is linked to the new Request record
- [ ] Audit Log table: new entry with Action = "form_submission", Status = "Success"

**What to check in email:**

- [ ] Confirmation email arrives at qa-test@example.com within 2 minutes
- [ ] Email subject includes "QA Test User"
- [ ] Email body shows correct occasion (Bachelorette), group size (12), and experience (Monaco Social)

**What to check in Slack:**

- [ ] Slack alert appears in #she-said-sail-leads channel within 2 minutes
- [ ] Alert shows name, occasion, group size, source (test), and email

---

## Test 2: Email Capture (M-EMAIL-CAPTURE)

**What to send:**

Go to the homepage. Enter `qa-emailcapture@example.com` in the email capture form. Click Subscribe.

**What to verify in Airtable:**

- [ ] Contacts table: new record with email = qa-emailcapture@example.com
- [ ] Email Subscribed = true
- [ ] Source = "email-capture-form"
- [ ] Audit Log: new entry with Action = "contact_created"

---

## Test 3: Deduplication Test (Submit Same Email Twice)

**Purpose:** Verify that submitting the same email twice does not create two Contact records.

**What to send:**

Submit the Request to Book form twice using the same email address (qa-dedup@example.com). Use slightly different data on the second submission (different group size).

**What to verify:**

- [ ] Requests table: two separate Request records (this is correct, two inquiries)
- [ ] Contacts table: exactly ONE Contact record for qa-dedup@example.com (not two)
- [ ] The Contact's Last Seen At is updated to the time of the second submission
- [ ] Both Request records are linked to the same Contact record

**Pass criteria:** If you see two Contact records with the same email, the deduplication logic in Make.com is not working. Review the Search Records module in M-WEBFORM-REQUEST-CAPTURE and confirm it is filtering by Email (exact match) before routing to Create or Update.

---

## Test 4: Error Test (Malformed Email)

**Purpose:** Verify that invalid emails are caught at the JavaScript validation layer and never reach Make.com.

**What to send:**

On the Request to Book form, type `not-an-email` in the Email field and click Submit.

**What to verify:**

- [ ] The form does NOT submit. A validation error message appears below the Email field.
- [ ] No network request is fired to the Make.com webhook (check DevTools > Network tab: no POST request should appear).
- [ ] No new records appear in Airtable.

**Pass criteria:** The error message appears inline, the form stays open, and the user can correct the email and resubmit. This validation is handled by MetForm's built-in email validation, not by Make.com. If a malformed email reaches Make.com, the JavaScript or MetForm validation is not working.

---

## Test 5: Internal Rating Logic

**Test 5a: Hot rating for Bachelorette**

Submit the form with Occasion = Bachelorette, Group Size = 5.

Verify: Internal Rating = "Hot" in Airtable (Bachelorette alone triggers Hot).

**Test 5b: Hot rating for large group**

Submit the form with Occasion = Birthday, Group Size = 15.

Verify: Internal Rating = "Hot" in Airtable (Group Size >= 15 triggers Hot).

**Test 5c: Warm rating for standard inquiry**

Submit the form with Occasion = Girls Trip, Group Size = 8.

Verify: Internal Rating = "Warm" in Airtable.

---

## Test 6: Thank You Page Redirect

**What to do:**

After a successful form submission, verify the browser redirects to /thank-you/ within 2 seconds.

**What to verify:**

- [ ] Browser URL changes to https://shesaidsail.com/thank-you/
- [ ] The thank you page loads without a 404 error
- [ ] GTM Preview shows `view_thank_you_page` event firing
- [ ] GA4 DebugView shows the conversion event

---

## Rollback: How to Delete Test Records in Airtable

After completing all tests, delete test records to keep the base clean.

**Step-by-step:**

1. Open Airtable and navigate to the She Said Sail base.
2. Open the Requests table. Filter by: Submitted At = today AND Email contains "example.com" OR "qa-".
3. Select all matching records (click the checkbox in the first column header to select all visible).
4. Right-click > Delete records.
5. Open the UTMs table. Filter by: Submitted At = today AND UTM Source = "test".
6. Select all and delete.
7. Open the Contacts table. Filter by: Email contains "qa-" OR "example.com".
8. Select and delete (only delete contacts that were created during testing, not any real contacts).
9. Open the Audit Log table. Filter by: Timestamp = today AND Details contains "QA" or "qa-".
10. Select and delete.

**Alternatively:** In Airtable, go to each table, switch to the "All [Records]" view, sort by Created At descending, and manually identify and delete the test records by name/email.

**Important:** Do not delete the Campaign records or Make.com webhook configuration. Only delete the Request, UTM, Contact, and Audit Log records created during testing.
