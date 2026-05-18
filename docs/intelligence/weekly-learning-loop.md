# She Said Sail: Weekly Learning Loop
Version 1.0 | May 2026

---

## PURPOSE

The weekly learning loop is the mechanism by which She Said Sail improves over time. Every week, data from the previous seven days is analyzed, patterns are identified, recommendations are generated, and decisions are recorded. Over time, the system accumulates knowledge that makes each subsequent week smarter than the last.

This is not passive reporting. It is an active improvement cycle. Data is only valuable when it produces decisions. Decisions are only valuable when their outcomes are tracked. This loop enforces both.

---

## THE LOOP CYCLE

The loop runs on a Monday-to-Monday cadence and has five steps.

### Step 1: Data Collection
**Trigger:** Automatic. Make scenario M-WEEKLY-REPORT-001 runs every Monday at 8:00 AM.

What is collected:
- Requests created in the past 7 days (count, source, experience interest, occasion)
- Bookings confirmed in the past 7 days (count, revenue, experience, source)
- Chatbot conversations (count, handoff rate, email capture rate, top experience recommended)
- Revenue Attribution records linked to bookings this week
- Experience Performance rollup (M-EXPERIENCE-ROLLUP-001 also runs Monday 8:00 AM)

Output: A new record is created in the Weekly Insights table. A Slack message is posted to #intelligence with the structured summary.

### Step 2: AI Analysis
**Trigger:** Automatic if Claude API is integrated. Manual founder review if not yet integrated.

What happens:
- The Weekly Insights record is reviewed against the previous 3 weeks of records
- Patterns are identified (rising close rates, dropping chatbot handoff rate, ad spend concentration, etc.)
- Anomalies are flagged (a source that generated 3x normal requests, a drop in form completions, an experience with zero inquiries)

Output: An AI narrative summary is added to the Weekly Insights record in the AI Summary field. If manual, the founder writes her own interpretation in that field.

### Step 3: Recommendations
**Output of Step 2.** The analysis produces 3 to 5 specific, actionable recommendations. Examples of the right specificity level:

- "Move 20% of Meta budget from campaign reel-v2 to reel-v4, which generated 3x revenue this week."
- "Update the chatbot Golden Hour Escape recommendation copy. The current handoff rate for that path is 15%. All other paths are above 30%."
- "The hero CTA click rate on the homepage dropped 12% this week. Test a new CTA label."

Recommendations are stored in the Weekly Insights record (Recommendations field) and posted in the Slack message.

### Step 4: Founder Decision
**Trigger:** Manual. The founder reviews the weekly report, reads the recommendations, and decides which to act on.

For each recommendation the founder acts on, she creates a record in the Founder Decisions table:
- What was decided
- Why (which data point drove the decision)
- Which Weekly Insights record prompted it
- What outcome she expects
- How success will be measured
- The review date (4 weeks from decision date)

Recommendations she decides not to act on do not require a record. Only decisions that are taken forward are logged.

### Step 5: Outcome Tracking
**Trigger:** Time-based. Four weeks after a Founder Decision is recorded, the Review Date arrives.

What happens:
- The founder revisits the Founder Decisions record
- She fills in the Actual Outcome field with what happened
- If the outcome produced a reusable lesson, she creates a record in the Lessons Learned table
- The decision Status is updated to "Outcome Recorded"

This closes the loop. The knowledge is now stored and searchable for future decisions.

---

## WHAT THE SYSTEM LEARNS ABOUT

Ten areas of learning are tracked through the loop. Each area has a driving question, a data source, a metric, and an example of the learning signal it produces.

### 1. Page Conversion Performance

**Question:** Which pages convert best?

**Data source:** GA4 (click_request_to_book event filtered by page_path) combined with Airtable Requests table (landing_page field populated from UTM source capture).

**Metric:** Conversion rate per landing page = form submissions divided by page visits for that page path.

**Learning signal:** If /experience/pink-palm-club/ generates 40% of all requests while receiving only 25% of total traffic, that page is the highest-converting experience page. Ad creative should prioritize Pink Palm Club imagery and offers.

---

### 2. Experience Lead Quality

**Question:** Which experiences generate the highest-quality leads?

**Data source:** Airtable Requests table (filtered by Experience Interest field) joined with Bookings table (filtered by Experience field).

**Metric:** Close rate per experience = Bookings divided by Requests for each experience, calculated over a rolling 4-week window.

**Learning signal:** If Monaco Social has a 40% close rate and Rose Day Club has a 20% close rate over the same period, Monaco Social leads convert at twice the rate. Lead generation spend should be weighted toward Monaco Social acquisition until Rose Day Club performance improves.

---

### 3. Chatbot Path Performance

**Question:** Which chatbot paths convert best?

**Data source:** Airtable Chatbot Conversations table. Fields used: experience_recommended, outcome (handoff vs. abandoned), and linked Requests/Bookings records.

**Metric:** Chatbot handoff-to-booking rate per experience_recommended value.

**Learning signal:** If the Pink Palm Club chatbot path converts at 35% from handoff to booking and the Golden Hour Escape path converts at 15%, the Golden Hour Escape path has a framing or qualification problem. The chatbot recommendation logic and copy for that path should be reviewed before the next weekly loop.

---

### 4. Ad Attribution

**Question:** Which ads generate actual bookings?

**Data source:** Revenue Attribution table. Fields used: utm_campaign, creative_id (from utm_content), revenue per record.

**Metric:** Total revenue per campaign slug, total revenue per creative_id.

**Learning signal:** If creative reel-v4 generated $30,000 in confirmed booked revenue and creative reel-v2 generated $4,000 over the same period with similar impression volume, budget should shift to reel-v4 immediately.

---

### 5. CTA Performance

**Question:** Which CTAs perform best?

**Data source:** GA4 click_request_to_book event. The cta_location parameter identifies where on the page the click originated (hero, nav, experience page bottom, chatbot handoff button).

**Metric:** CTA click rate per location. Calculated as clicks from that location divided by total page views where that CTA is present.

**Learning signal:** If the chatbot handoff CTA converts to form submission at 3x the rate of the nav CTA, resources should be directed toward optimizing the chatbot flow rather than nav design. The nav CTA is not the conversion bottleneck.

---

### 6. Concierge Performance

**Question:** Which concierge responses work best?

**Data source:** Airtable Requests table. Fields used: Assigned Concierge (linked to Contacts or team member), linked Booking outcome, Submitted At timestamp, first Internal Note timestamp.

**Metric:** Close rate per assigned concierge. Average days from submission to booking close per concierge.

**Learning signal:** If one concierge approach closes 45% of inquiries within an average of 4 days and another closes 20% within 9 days, the higher-performing approach should be documented. The specific language, sequencing, and follow-up cadence that produces the better result should be captured in Lessons Learned so it can be adopted as the standard approach.

---

### 7. Experience Margin

**Question:** Which experiences produce the highest margins?

**Data source:** Revenue Attribution table. Fields used: gross_margin (calculated field or manual entry), experience name (derived from Booking).

**Metric:** Average gross margin per booking per experience.

**Learning signal:** If Monaco Social generates an average of $6,000 gross margin per booking and Pink Palm Club generates $9,000, there is a pricing and capacity opportunity. Pink Palm Club pricing may be underoptimized, or Monaco Social may have cost structure issues that warrant investigation before the next season.

---

### 8. Drop-off Analysis

**Question:** Where are users dropping off?

**Data source:** GA4 funnel exploration using the four key events in sequence: view_homepage, click_request_to_book, start_booking_form, submit_booking_form.

**Metric:** Drop-off rate at each funnel transition.

**Learning signal:** If 60% of users who fire click_request_to_book never fire start_booking_form, the page between the CTA click and the form has a conversion problem. This is the booking request landing page or form page. Fixing this step has higher leverage than improving any earlier funnel stage.

---

### 9. Repeat Booking Campaigns

**Question:** Which campaigns generate repeat bookings?

**Data source:** Airtable Contacts table filtered by Total Bookings greater than or equal to 2. Linked back to the utm_source field on the first Booking or UTM record for that Contact.

**Metric:** Repeat booking rate by original acquisition source.

**Learning signal:** If organic Instagram accounts for 30% of repeat bookings but only 10% of new bookings, organic content has a disproportionate lifetime value impact. Investing in organic content quality produces better retention outcomes than paid acquisition at the same budget level.

---

### 10. Traffic Source Quality

**Question:** Which traffic sources generate luxury buyers?

**Data source:** Revenue Attribution table. Fields used: utm_source, revenue per record, linked Booking.

**Metric:** Average booking value per traffic source. Close rate per source (Bookings divided by Requests where source matches).

**Learning signal:** If Google organic generates $14,000 average booking value and Meta paid generates $10,500 average booking value, Google organic visitors are higher-intent buyers. SEO investment has a higher revenue-per-visitor payoff than Meta paid at current creative performance levels.

---

## WEEKLY LOOP CALENDAR

The loop runs on a fixed Monday-to-Monday cadence. Here is the full week:

**Monday (8:00 AM):** M-WEEKLY-REPORT-001 runs. M-EXPERIENCE-ROLLUP-001 runs. Weekly Insights record is created. Slack message posted to #intelligence. Founder reviews the report before end of day.

**Tuesday to Wednesday:** Founder acts on priority recommendations. Changes may include: updating chatbot copy in chatbot-copy-system.md, adjusting Meta ad budget allocation, revising a CTA label on an experience page, or updating concierge response templates.

**Thursday:** Changes that were made are logged in Founder Decisions table. Each decision gets its own record with the reason, expected outcome, measurement plan, and review date.

**Friday to Sunday:** No loop action required. Conversions and bookings from the week continue to accumulate data for the following Monday report.

**Four weeks after each decision:** The Review Date arrives. The founder opens the Founder Decision record, fills in the Actual Outcome field, and creates a Lessons Learned record if the outcome produced transferable knowledge.

---

## LEARNING VELOCITY

The system builds intelligence over time. Different timeframes unlock different types of insight.

**4 weeks:** Baseline conversion rates are established for each experience, source, and chatbot path. This is the minimum dataset needed to identify what "normal" looks like.

**8 weeks:** First meaningful comparisons between variants are possible. A/B creative tests that started at week 1 have enough data to read. Chatbot path differences are statistically meaningful. Concierge close rate differences are visible.

**12 weeks:** Seasonal patterns begin to appear. Bachelorette inquiry volume in Q1 vs. Q2 becomes visible. Experience demand patterns by season emerge. Ad performance variation by month can be compared.

**6 months:** The full campaign ROI cycle is visible from inquiry to booking to post-charter review. Campaigns that generated bookings in month 1 are now fully resolved with outcomes, lessons, and downstream referral data if tracked.

**1 year:** Repeat booking patterns and lifetime value by original source are available. The Contacts table has enough repeat booking data to segment high-LTV customer profiles by acquisition source, occasion type, and experience preference.

---

## WHAT THE LOOP DOES NOT DO

The loop is powerful but bounded. These are explicit non-functions:

- **It does not automatically make changes.** Every recommendation requires founder review and a deliberate decision before any change is made. The system informs. The founder decides.

- **It does not replace concierge judgment on individual inquiries.** Close rate patterns inform training and approach, but every inquiry is handled by a person who reads the full context.

- **It does not predict future bookings with certainty.** The system identifies patterns in historical data. It does not guarantee that past patterns will hold.

- **It does not track individual visitor behavior beyond form submission.** No individual browsing paths, session recordings, or identity resolution are used. Data collection is at the aggregate and form-submission level.
