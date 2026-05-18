# She Said Sail: Intelligence Layer QA Checklist
Version 1.0 | May 2026

---

## PURPOSE

This checklist validates the intelligence layer before and after deployment. Every check in this document should produce a clear pass or fail result. If a check fails, the failure must be diagnosed and resolved before the intelligence layer is considered operational.

**Run this checklist:**
1. After initial setup of the intelligence layer
2. After any Make.com scenario change
3. After any Airtable schema change
4. Weekly for the first month after deployment
5. Monthly thereafter

---

## SECTION 1: ATTRIBUTION CHAIN VALIDATION

The attribution chain must be intact from traffic source to confirmed revenue. A break at any point in this chain means bookings cannot be attributed to the campaigns that generated them.

| Check | Method | Pass Condition |
|---|---|---|
| UTM params captured on landing | Load the site with ?utm_source=test&utm_medium=qa&utm_campaign=qa-test appended to the URL. Submit the request form. Check the UTMs table in Airtable. | UTMs table has a new record with Source = "test", Medium = "qa", Campaign = "qa-test" |
| UTM record linked to Request | Open the UTMs table record created in the check above. Expand the Request field. | Request field on the UTM record points to the newly submitted Request record |
| sss_utm sessionStorage populated | After landing with UTM params, open browser developer tools. Go to Application, then Session Storage. | Key "sss_utm" exists and contains a JSON object with source, medium, and campaign values matching the test URL params |
| sss_vid cookie set | After landing, check browser developer tools under Application, then Cookies. | Cookie "sss_vid" exists with a non-empty UUID string value |
| Visitor ID in form payload | Open browser Network tab before submitting the form. Submit the form. Inspect the POST request to the Make webhook. | Payload contains a visitor_id field with a UUID value matching the sss_vid cookie |
| Visitor ID stored in UTMs table | Open the UTMs table record created in this test. | Visitor ID field contains the UUID value from the cookie and form payload |
| Request linked to Revenue Attribution on booking | Open the test Request record. Manually change Status to "Booked". Wait for M-BOOKING-OUTCOME-001 to trigger, or trigger it manually in Make. | Revenue Attribution table has a new record with the Request field linked to this test Request |
| Campaign linked in Revenue Attribution | Open the Revenue Attribution record created above. | Campaign field is populated and points to the Campaign record whose UTM slug matches "qa-test" |
| Revenue correct in Attribution record | Open the Revenue Attribution record. | Revenue field value matches the Total Value field on the linked Booking record |
| Days to Close calculated | Open the Revenue Attribution record. | Days to Close formula field returns a positive integer equal to the difference in days between Booked At and First Seen At |

**Section 1 result:** Pass / Fail
**Notes:**

---

## SECTION 2: CHATBOT INTELLIGENCE VALIDATION

The chatbot must generate complete Chatbot Conversations records that are correctly linked to the Requests table and capture the correct occasion, experience, and outcome data.

| Check | Method | Pass Condition |
|---|---|---|
| Chatbot conversation creates Chatbot Conversations record | Open the chatbot on the site. Complete the full conversation flow through to handoff. Submit the handoff form. | Chatbot Conversations table has a new record corresponding to this conversation |
| Conversation linked to Request | Open the Chatbot Conversations record just created. | Request field is populated and points to the new Chatbot Lead record in the Requests table |
| Occasion captured correctly | Run the chatbot and select "Bachelorette" as the occasion. | Chatbot Conversations record has Occasion = "bachelorette" |
| Experience recommended captured | Complete the chatbot through to the recommendation state (state 7). | experience_recommended field on the Conversations record is populated with the experience slug |
| Conversation summary populated | Complete the full chatbot flow through handoff. | conversation_summary field on the Conversations record contains a non-empty text summary of the path taken |
| Email captured in Conversations record | Enter an email address during the chatbot flow. | email_captured field = true AND Chatbot Conversations.Email field contains the submitted email address |
| Chatbot handoff GTM event fires | Complete the chatbot to handoff state. Open GTM Preview mode before starting the conversation. | chatbot_handoff event appears in the GTM Preview dataLayer panel with experience_slug parameter populated and correct has_email boolean |
| Chatbot lead in Requests table | Complete the chatbot through handoff. | Requests table has a new record with Request_Type = "Chatbot Lead" |
| UTM attribution on chatbot lead | Load the site with UTM params in the URL. Then open and complete the chatbot to handoff. | The Chatbot Lead record in the Requests table has utm_source and utm_campaign values matching the URL params |

**Section 2 result:** Pass / Fail
**Notes:**

---

## SECTION 3: MAKE SCENARIO VALIDATION

All four intelligence Make scenarios must be active, triggering correctly, and writing records to the correct Airtable tables.

| Check | Method | Pass Condition |
|---|---|---|
| M-WEBFORM-001 active and receiving | Submit a test request form. Check Make.com scenario execution history. | Execution log shows a successful run with no errors |
| M-CHATBOT-001 active and receiving | Complete the chatbot to handoff. Check Make.com scenario execution history. | Execution log shows a successful run with no errors |
| M-BOOKING-OUTCOME-001 trigger fires | Open a test Request record in Airtable. Change Status to "Booked." Check Make.com execution log. | Execution log shows M-BOOKING-OUTCOME-001 triggered within 2 minutes of the status change |
| Revenue Attribution record created | Confirm the above trigger fired. Check Revenue Attribution table. | A new Revenue Attribution record exists, linked to the Request that was set to Booked |
| M-WEEKLY-REPORT-001 scheduled | Open M-WEEKLY-REPORT-001 in Make.com. Check the Scheduling section. | Scenario shows a scheduled run at 8:00 AM every Monday |
| Weekly Insights record created | Wait for the next Monday 8:00 AM run, or use Make's "Run once" to trigger the scenario manually. | Weekly Insights table has a new record with the current week's start date and populated metric fields |
| Slack #intelligence receives weekly report | After the Monday run, check the #intelligence Slack channel. | A structured Slack message appears with request count, booking count, revenue, and recommendations sections |
| M-EXPERIENCE-ROLLUP-001 runs | Check Make.com execution log for Monday morning. | M-EXPERIENCE-ROLLUP-001 shows a successful execution on the same Monday as M-WEEKLY-REPORT-001 |
| No duplicate records in any table | Submit a form twice using the same email address. Wait for both Make runs to complete. | Contacts table has exactly one record for that email address. The second submission linked to the existing Contact, not a new one. |
| Audit Log entries for all key actions | After completing the test form submission, chatbot handoff, and booking status change, open the Audit Log table. | Three entries exist: one for form_submission, one for chatbot_lead_created, one for booking_outcome_linked |

**Section 3 result:** Pass / Fail
**Notes:**

---

## SECTION 4: EVENT PERSISTENCE VALIDATION

All 22 GTM events (14 site events and 8 chatbot events) must fire correctly and reach GA4. No PII must appear in any event payload.

| Check | Method | Pass Condition |
|---|---|---|
| GTM fires on all pages | Open GTM Preview mode. Visit the homepage, each experience page, and the contact page. | Tag firing summary shows the Google Analytics tag fires on all page views. No tag errors in the Preview console. |
| chatbot_open fires | With GTM Preview active, click the chatbot toggle button on any page. | chatbot_open event appears in the GTM Preview dataLayer with trigger_type = "manual" |
| chatbot_handoff fires | Complete the chatbot conversation to the handoff state with GTM Preview active. | chatbot_handoff event appears in the dataLayer with both experience_slug and has_email parameters populated |
| submit_booking_form fires | Fill out and submit the request form with GTM Preview active. | submit_booking_form event appears in the dataLayer with occasion and group_size parameters |
| All events reaching GA4 | Open GA4 DebugView (Admin, DebugView). On the site, trigger the key events listed above. | Events appear in the GA4 DebugView panel in real time with correct parameter values |
| No PII in GTM events | Inspect the chatbot_capture_email event in GTM Preview or the dataLayer console. | The event parameters do not contain the email address string itself. Only a boolean (has_email = true) or anonymized indicator is present. |
| UTM data in GA4 | Load the site with UTM params. Navigate to a second page. Check GA4 DebugView. | Session source, medium, and campaign in GA4 match the UTM params in the landing URL |

**Section 4 result:** Pass / Fail
**Notes:**

---

## SECTION 5: AIRTABLE RELATIONSHIP VALIDATION

All linked record relationships between tables must be intact and navigable. A broken link means data from one table cannot be surfaced in another, which corrupts dashboard calculations.

| Check | Method | Pass Condition |
|---|---|---|
| Requests -> UTMs link | Open any Request record that came in via the web form. Click to expand the UTM Record linked field. | The linked UTM record opens correctly and shows the correct source, medium, and campaign for that request |
| Requests -> Contacts link | Open any Request record. Click to expand the Contact linked field. | The linked Contact record opens and the email address on the Contact matches the submitter's email |
| Requests -> Revenue Attribution link | Open a Request record that has Status = Booked. Expand the Revenue Attribution linked field. | A linked Revenue Attribution record is present and opens correctly |
| Bookings -> Revenue Attribution link | Open a Booking record. Expand the Revenue Attribution linked field. | A linked Revenue Attribution record is present and shows correct revenue |
| Revenue Attribution -> Campaign link | Open a Revenue Attribution record where the utm_campaign value matches a record in the Campaigns table. | Campaign linked field is populated and points to the correct Campaign record |
| Chatbot Conversations -> Requests link | Open any Chatbot Conversations record. Expand the Request linked field. | The linked Request record opens and has Request_Type = "Chatbot Lead" |
| Contacts.Lifetime Value correct | Find a Contact record with 2 or more linked Bookings. | Lifetime Value field (rollup or formula) equals the sum of Total Value across all linked Bookings |
| Experience Performance records exist | Open the Experience Performance table. | Exactly 4 records exist, one for each experience: Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club |
| Weekly Insights records accumulating | Open the Weekly Insights table after the first Monday 8:00 AM run. | At least one record exists with a populated Week Start Date and metric fields |

**Section 5 result:** Pass / Fail
**Notes:**

---

## SECTION 6: DATA QUALITY CHECKS

These checks confirm that the data in the system is clean and that no structural data problems have been introduced by the intelligence layer setup.

| Check | Method | Pass Condition |
|---|---|---|
| No orphaned Bookings (no linked Request) | In the Bookings table, create a filter where Request field is empty. | Zero records pass the filter |
| No orphaned UTM records (no linked Request) | In the UTMs table, create a filter where Request field is empty. | Zero records pass the filter |
| No Revenue Attribution records with zero revenue | In the Revenue Attribution table, create a filter where Revenue field is empty or equals 0. | Zero records pass the filter |
| All Hot leads have Assigned Concierge | In the Requests table, filter for Internal Rating = Hot AND Assigned Concierge is empty. | Zero records pass the filter |
| No duplicate emails in Contacts | In the Contacts table, check for any email address that appears on more than one record. This can be done with a formula field or by exporting and checking for duplicates. | Zero duplicate email values |
| All Lessons Learned have Category | In the Lessons Learned table, filter for Category is empty. | Zero records pass the filter |
| All Founder Decisions have Review Date | In the Founder Decisions table, filter for Review Date is empty AND Status = Active. | Zero records pass the filter |

**Section 6 result:** Pass / Fail
**Notes:**

---

## SIGN-OFF TABLE

This table is completed by the person running the QA check. One row must be completed for each section before the intelligence layer is considered deployment-ready.

| Phase | Checked By | Date | Status |
|---|---|---|---|
| Attribution Chain Validation | | | |
| Chatbot Intelligence Validation | | | |
| Make Scenario Validation | | | |
| Event Persistence Validation | | | |
| Airtable Relationship Validation | | | |
| Data Quality Checks | | | |
| First Weekly Report Verified | | | |
| First Lessons Learned Record Created | | | |

**Status options:** Pass, Fail, Partial (document which checks failed in the Notes field for that section)

**Deployment gate:** All 8 rows must show "Pass" before the intelligence layer is considered fully operational.
