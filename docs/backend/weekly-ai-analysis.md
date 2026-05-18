# She Said Sail: Weekly AI Analysis System

Version: 1.0
Date: 2026-05-18

---

## PURPOSE

Every Monday morning at 8:00 AM, the She Said Sail intelligence system compiles the previous seven days of data from Airtable and delivers a structured report to the founder via Slack.

The report has two goals:

1. Eliminate the Monday morning review task. The founder should not need to open Airtable, scroll through records, and manually count anything. The system does this work automatically.

2. Recommend three specific actions for the coming week. Raw metrics are useful. Recommendations are actionable. The combination of both is what transforms a reporting tool into a decision support system.

The weekly report tells the founder: what happened last week, why it likely happened, and what to do next.

---

## DATA INPUTS

The following Airtable data sources are queried by M-WEEKLY-REPORT-001 every Monday at 8:00 AM. All date filters use the range: last Monday 00:00:00 to this Sunday 23:59:59 in the site's operating timezone.

### 1. Requests Table (last 7 days)

Query: all Requests where Submitted_At >= last Monday AND Submitted_At <= last Sunday.

Aggregations:
- Total request count
- Breakdown by Occasion (Bachelorette, Birthday, Girls Trip, Anniversary, Other)
- Breakdown by Experience of Interest (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club, Other / TBD)
- Breakdown by Source (UTM_Source field or lookup from linked UTM record)
- Breakdown by Status (New, Contacted, Proposal Sent, Booked, Closed Lost)
- Breakdown by Request_Type (Form, Chatbot Lead, Email Capture, Contact Form)
- Count of requests with Internal_Rating >= 4 (hot leads)

### 2. Bookings Table (last 7 days)

Query: all Bookings where Deposit_Date >= last Monday AND Deposit_Date <= last Sunday.

Aggregations:
- Total booking count
- Total revenue (sum of Total_Value)
- Average booking value
- Breakdown by Experience
- Breakdown by Group Size bucket (2-4 guests, 5-8 guests, 9-12 guests, 12+ guests)

### 3. Revenue Attribution Table (last 7 days)

Query: all Revenue Attribution records where Booked_At >= last Monday.

Aggregations:
- Revenue by UTM_Source
- Revenue by UTM_Campaign
- Average Days_to_Close
- Average Margin_Percent
- Count of records with no UTM link (unattributed bookings)

### 4. Chatbot Conversations Table (last 7 days)

Query: all Chatbot Conversations records where Created_At >= last Monday.

Aggregations:
- Total conversation count (chatbot_open events reached)
- Total conversations that reached chatbot_start_conversation state
- Total conversations that reached chatbot_capture_email state (partial completion)
- Total conversations that reached chatbot_complete state (full completion)
- Completion rate: chatbot_complete count / chatbot_open count
- Breakdown of completed conversations by Occasion selected
- Breakdown of completed conversations by Experience recommended
- Count of conversations that captured both email and phone

### 5. Experience Performance Table (last 7 days)

Query: Experience Performance records for the current week (populated by M-EXPERIENCE-ROLLUP-001 which runs at 7:30 AM before this scenario).

Data retrieved per experience:
- Leads received
- Bookings confirmed
- Conversion rate (bookings / leads)
- Total revenue
- Average booking value

### 6. Concierge Performance (derived from Requests and Bookings)

Query: Requests from last 7 days where Assigned_Concierge is populated.

Aggregations:
- For each concierge: requests assigned, requests moved to "Contacted" status, requests moved to "Proposal Sent," requests moved to "Booked"
- Stage conversion rates per concierge
- Average Internal_Rating of assigned requests per concierge

Note: this is a simplified concierge performance view. The more detailed concierge scoring is handled by M-CONCIERGE-SCORE-001 and stored in Revenue Attribution records. The weekly report uses the simpler view.

### 7. GA4 API (optional, if integration is configured)

If a GA4 API connection is configured in Make.com, the following metrics are retrieved for the past 7 days:
- Total sessions
- Total users (new and returning)
- Sessions by source / medium
- Conversion rate (sessions that reached view_thank_you_page)
- Top landing pages by session count
- Average session duration

If the GA4 API is not configured, this section of the report is omitted with a note: "GA4 data not available. Configure GA4 API connection to include site traffic metrics."

### 8. Open Leads Outstanding (Requests table, all time)

Query: all Requests where Status is "New" OR "Contacted" OR "Proposal Sent" AND Submitted_At <= 7 days ago.

This shows leads that have been sitting in the pipeline for more than 7 days without being closed. These are the leads most at risk of going cold.

Aggregations:
- Total count of open leads older than 7 days
- Count by Status bucket
- Oldest open lead age (days since submission)

---

## MAKE SCENARIO: M-WEEKLY-REPORT-001

### Trigger

Scheduled execution: every Monday at 8:00 AM (configured in Make.com scheduler module using the founder's local timezone).

### Pre-condition

M-EXPERIENCE-ROLLUP-001 must complete before this scenario runs. M-EXPERIENCE-ROLLUP-001 is scheduled for 7:30 AM Monday. Allow a 30-minute buffer. If M-EXPERIENCE-ROLLUP-001 has not completed by 8:00 AM due to an error, M-WEEKLY-REPORT-001 proceeds with the last available Experience Performance data and includes a note in the Slack report: "Experience rollup data may be from a prior week. Check M-EXPERIENCE-ROLLUP-001 status."

### Module Sequence

**Module 1: Set Variables**
- last_monday: DATE(NOW()) minus 7 days, set to 00:00:00
- last_sunday: DATE(NOW()) minus 1 day, set to 23:59:59
- week_label: formatted string "Mon DD MMM to Sun DD MMM YYYY"

**Module 2: Airtable - Search Records (Requests)**
- Filter: Submitted_At >= {{last_monday}} AND Submitted_At <= {{last_sunday}}
- Fields: Status, Occasion, Experience_Interest, Request_Type, Internal_Rating, Assigned_Concierge, UTM_Source (lookup)
- Max records: 500

**Module 3: Airtable - Search Records (Requests, open leads older than 7 days)**
- Filter: Status IN ["New", "Contacted", "Proposal Sent"] AND Submitted_At <= {{last_monday}}
- Fields: Status, Submitted_At, Occasion, Assigned_Concierge
- Max records: 200

**Module 4: Airtable - Search Records (Bookings)**
- Filter: Deposit_Date >= {{last_monday}} AND Deposit_Date <= {{last_sunday}}
- Fields: Experience, Total_Value, Group_Size, Charter_Date
- Max records: 100

**Module 5: Airtable - Search Records (Revenue Attribution)**
- Filter: Booked_At >= {{last_monday}} AND Booked_At <= {{last_sunday}}
- Fields: Revenue, Gross_Margin, Margin_Percent, UTM_Source, UTM_Campaign, Days_to_Close, Experience
- Max records: 100

**Module 6: Airtable - Search Records (Chatbot Conversations)**
- Filter: Created_At >= {{last_monday}} AND Created_At <= {{last_sunday}}
- Fields: Completed, Occasion_Selected, Experience_Recommended, Email_Captured, Phone_Captured, States_Visited
- Max records: 500

**Module 7: Airtable - Search Records (Experience Performance)**
- Filter: Week_Date = {{last_monday}} (the record created by M-EXPERIENCE-ROLLUP-001 for this week)
- Fields: Experience, Leads, Bookings, Conversion_Rate, Total_Revenue, Average_Booking_Value
- Max records: 10

**Module 8: Tools - Aggregate Requests**
- Count total records from Module 2
- Group and count by: Status, Occasion, Experience_Interest, Request_Type
- Count records where Internal_Rating >= 4
- Group and count by UTM_Source

**Module 9: Tools - Aggregate Bookings and Revenue**
- Count total records from Module 4
- Sum Total_Value
- Calculate average Total_Value
- Group and count by Experience

**Module 10: Tools - Aggregate Revenue Attribution**
- Sum Revenue by UTM_Source (top 3 sources)
- Sum Revenue by UTM_Campaign (top campaign)
- Average Days_to_Close
- Average Margin_Percent
- Count records with no UTM link

**Module 11: Tools - Aggregate Chatbot Conversations**
- Count all records from Module 6
- Count records where Completed = true
- Calculate completion rate
- Group completed records by Occasion_Selected
- Group completed records by Experience_Recommended

**Module 12: Tools - Format Intelligence Payload (JSON)**
Produces a structured JSON object with all aggregated metrics. This JSON is used as input to the Claude API module (Module 13) and as the basis for Slack message formatting (Module 14).

```json
{
  "week": "Mon 11 May to Sun 17 May 2026",
  "requests": {
    "total": 0,
    "by_status": {},
    "by_occasion": {},
    "by_experience_interest": {},
    "by_source": {},
    "by_type": {},
    "hot_leads": 0
  },
  "open_leads_pipeline": {
    "total_open_older_than_7_days": 0,
    "by_status": {}
  },
  "bookings": {
    "total": 0,
    "total_revenue": 0,
    "average_value": 0,
    "by_experience": {}
  },
  "revenue_attribution": {
    "top_sources": [],
    "top_campaign": "",
    "average_days_to_close": 0,
    "average_margin_percent": 0,
    "unattributed_count": 0
  },
  "chatbot": {
    "total_conversations": 0,
    "completed_conversations": 0,
    "completion_rate_percent": 0,
    "by_occasion": {},
    "by_experience_recommended": {}
  },
  "experience_performance": []
}
```

**Module 13 (optional): HTTP - POST to Claude API**
This module is only active if the Claude API integration is enabled. See the AI Analysis Integration section for full configuration.

- Method: POST
- URL: https://api.anthropic.com/v1/messages
- Headers: x-api-key: {{ANTHROPIC_API_KEY}}, anthropic-version: 2023-06-01, Content-Type: application/json
- Body: JSON with system prompt, intelligence payload, and model specification

**Module 14: Slack - Post Message (#intelligence channel)**
Formats and posts the raw metrics block (always) and the AI narrative block (if Module 13 is enabled and returns a response).

**Module 15: Airtable - Create Record (Weekly Insights table)**
- Week: {{week_label}}
- Raw_Metrics_JSON: the intelligence payload from Module 12
- AI_Narrative: Claude API response from Module 13 (blank if not enabled)
- Slack_Posted: true
- Reviewed_By_Founder: false (checkbox, founder checks this after reading)
- Created_At: now

**Module 16: Airtable - Create Record (Audit Log)**
- Action: "Weekly Report Generated"
- Scenario: M-WEEKLY-REPORT-001
- Week: {{week_label}}
- Timestamp: now

---

## AI ANALYSIS INTEGRATION

### When to Enable This

Enable the Claude API integration when:
- The raw metrics report has been running reliably for at least 2 weeks
- The founder has read at least 2 raw reports and understands what the metrics mean
- The Revenue Attribution table has data in it (at least 3-4 bookings attributed)

Do not enable it on the first week of M-WEEKLY-REPORT-001 deployment. Establish baseline metrics first.

### Make.com HTTP Module Configuration

Add this module between Module 12 (Format Intelligence Payload) and Module 14 (Slack Post) in M-WEEKLY-REPORT-001.

- Module type: HTTP - Make a Request
- Method: POST
- URL: https://api.anthropic.com/v1/messages
- Headers:
  - x-api-key: {{ANTHROPIC_API_KEY}} (stored in Make.com environment variables)
  - anthropic-version: 2023-06-01
  - content-type: application/json

Request body (JSON):

```json
{
  "model": "claude-sonnet-4-6",
  "max_tokens": 1024,
  "system": "You are the She Said Sail intelligence analyst. She Said Sail is a luxury yacht charter concierge service specializing in bachelorette parties, birthdays, and girls trips on the water. Your job is to review the weekly metrics payload and produce a clear, direct intelligence report.\n\nYour report must include three sections:\n1. What is working this week (specific, data-referenced)\n2. What needs attention this week (specific, data-referenced)\n3. Three specific recommendations for next week (actionable, numbered)\n\nTone: direct, confident, luxury service mindset. Write as if you are a trusted advisor, not a data dashboard. Use plain language. No em dashes. No filler phrases like 'it is worth noting' or 'it appears that.' State observations directly.",
  "messages": [
    {
      "role": "user",
      "content": "Here is the She Said Sail weekly metrics report for {{week_label}}:\n\n{{intelligence_payload_json}}\n\nGenerate the weekly intelligence report."
    }
  ]
}
```

The response content (choices[0].message.content or content[0].text depending on API version) is stored in a Make.com variable and appended to the Slack message in Module 14.

### Error Handling for Claude API Module

If the Claude API call fails (network error, rate limit, invalid response):
- Log the error to the Audit Log table
- Proceed with Module 14 (post raw metrics to Slack without the AI narrative)
- Include a note in the Slack message: "AI narrative unavailable this week. Raw metrics below."

The weekly report must never fail to post because the AI module returned an error. Raw metrics are always sent, regardless of AI availability.

---

## WEEKLY REPORT FORMAT

### Part 1: Raw Metrics Block (always sent)

```
*She Said Sail | Weekly Intelligence Report*
*Week: [Mon DD MMM] to [Sun DD MMM YYYY]*

---

*REQUESTS RECEIVED*
Total: [X]  (vs last week: [X], [+/- X]%)
Bachelorette: [X]  |  Birthday: [X]  |  Girls Trip: [X]  |  Other: [X]

By experience interest:
Monaco Social: [X]  |  Golden Hour Escape: [X]  |  Rose Day Club: [X]  |  Pink Palm Club: [X]  |  TBD: [X]

By source:
[source 1]: [X]  |  [source 2]: [X]  |  Direct: [X]

Hot leads (rating 4-5): [X]
Chatbot leads: [X]  |  Form leads: [X]  |  Contact form: [X]

---

*BOOKINGS CONFIRMED*
Total: [X]  |  Revenue: $[X,XXX]  |  Avg value: $[X,XXX]

By experience:
Monaco Social: [X] bookings, $[X,XXX]
Golden Hour Escape: [X] bookings, $[X,XXX]
Rose Day Club: [X] bookings, $[X,XXX]
Pink Palm Club: [X] bookings, $[X,XXX]

---

*REVENUE ATTRIBUTION*
Top source: [utm_source] ($[X,XXX])
Top campaign: [utm_campaign_slug] ($[X,XXX])
Avg days to close: [X] days
Avg margin: [XX]%
Unattributed bookings: [X]

---

*CHATBOT*
Conversations opened: [X]  |  Completed: [X]  |  Completion rate: [XX]%
Top occasion in chatbot: [Occasion]
Top experience recommended: [Experience]

---

*OPEN PIPELINE*
Leads open > 7 days: [X]
  New (no contact yet): [X]
  Contacted: [X]
  Proposal sent: [X]

---

*EXPERIENCE PERFORMANCE (this week)*
| Experience | Leads | Bookings | Conv Rate | Revenue |
|---|---|---|---|---|
| Monaco Social | [X] | [X] | [X]% | $[X,XXX] |
| Golden Hour Escape | [X] | [X] | [X]% | $[X,XXX] |
| Rose Day Club | [X] | [X] | [X]% | $[X,XXX] |
| Pink Palm Club | [X] | [X] | [X]% | $[X,XXX] |
```

### Part 2: AI Narrative Block (sent when Claude API is enabled)

```
---

*INTELLIGENCE ANALYSIS*

[Claude API response is inserted here verbatim. The response will contain three sections: What is working, What needs attention, Three recommendations for next week.]
```

If the AI narrative is not available, this section is replaced with:

```
---

*INTELLIGENCE ANALYSIS*
AI narrative not available this week. Review raw metrics above.
```

---

## INTELLIGENCE QUESTIONS THE SYSTEM SHOULD ANSWER WEEKLY

The following ten questions define the intelligence requirements of the weekly report. Each question is mapped to the Airtable data that answers it.

### Question 1: Which traffic source is sending the most qualified leads?

Answered by: Requests table, grouped by UTM_Source, filtered for Internal_Rating >= 4. Source with the highest count of high-rated leads is the most qualified source.

Limitation: UTM_Source is only populated when the form or chatbot submission includes UTM parameters. Direct traffic has no source. Internal rating is a manual field, so it requires concierge input to be meaningful.

### Question 2: Which campaign is generating the most revenue, not just the most leads?

Answered by: Revenue Attribution table, grouped by UTM_Campaign, summed by Revenue. Compare to Campaigns.Budget for ROI. This is the core revenue attribution output.

Limitation: Bookings must be linked to Requests for Revenue Attribution records to be created. Any booking confirmed without a linked Request (e.g., repeat booking entered directly in Bookings) will not appear in this answer.

### Question 3: Which experience converts at the highest rate (leads to bookings)?

Answered by: Experience Performance table (populated by M-EXPERIENCE-ROLLUP-001). Conversion_Rate field per experience shows leads received versus bookings confirmed. The experience with the highest conversion rate is most likely to generate a booking from a lead.

### Question 4: How long does it take to close a booking after first inquiry?

Answered by: Revenue Attribution table, Days_to_Close field, averaged across all bookings this week and grouped by Experience and UTM_Source.

Secondary source: compare Request.Submitted_At to Booking.Deposit_Date for bookings where Revenue Attribution records exist.

### Question 5: Which concierge is converting leads most effectively?

Answered by: Requests table, grouped by Assigned_Concierge. For each concierge: requests assigned, requests that reached "Proposal Sent" status, requests that reached "Booked" status. Calculate stage-by-stage conversion rates.

Limitation: this is a simplified view. The full concierge score (including revenue contribution and response speed) requires M-CONCIERGE-SCORE-001 to have run for several weeks.

### Question 6: Is the chatbot improving lead quality?

Answered by: Compare two subsets of the Requests table. Chatbot leads (Request_Type = "Chatbot Lead") versus form leads (Request_Type = "Form"). For each subset: count, average Internal_Rating, conversion to Booked status. If chatbot leads have a higher conversion rate or higher average rating, chatbot lead quality is stronger.

### Question 7: Where are leads going cold in the pipeline?

Answered by: Requests table, open leads older than 7 days (Status in New, Contacted, Proposal Sent). Group by Status and by Assigned_Concierge. The status with the most stale leads is the pipeline bottleneck. If "Proposal Sent" has the most stale leads, closing is the bottleneck. If "New" has the most stale leads, first contact is the bottleneck.

### Question 8: What occasion is generating the most revenue?

Answered by: Join Requests.Occasion to Revenue Attribution records via the linked Request field. Group Revenue Attribution.Revenue by Request.Occasion. The occasion with the highest total revenue is the primary revenue driver.

Note: this join requires that Revenue Attribution records are linked to Request records, which they are via the Request field in the Revenue Attribution table.

### Question 9: Is the chatbot completion rate improving week over week?

Answered by: Weekly Insights table. Compare this week's Chatbot completion rate to the same metric from the previous week's Weekly Insights record. After 4 weeks: compare to the 4-week rolling average.

This question requires at least 2 weeks of Weekly Insights records before it can be answered.

### Question 10: What is the return on the current ad budget?

Answered by: Campaigns table rollup fields (Total_Revenue_Attributed, Budget, ROI_Percent). The weekly report pulls the top campaign by revenue and displays its ROI. Full campaign ROI is visible in the Campaigns table view created for this purpose.

Limitation: ROI accuracy depends entirely on the Revenue Attribution chain being complete. If bookings are confirmed without triggering M-BOOKING-OUTCOME-001, or if Charter_Cost fields are not filled in by the operations team, the ROI calculation will be inaccurate.

---

## LEARNING LOOP TRIGGER

After M-WEEKLY-REPORT-001 posts the Slack report and creates the Weekly Insights record, the learning loop is initiated.

### Step 1: Weekly Insights Record Created

Module 15 of M-WEEKLY-REPORT-001 creates the Weekly Insights record with all raw metrics (as JSON), the AI narrative (if available), and Reviewed_By_Founder = false.

The founder reads the Slack report, then opens Airtable and checks the Reviewed_By_Founder checkbox on the Weekly Insights record. This confirms receipt and creates an implicit commitment to act on the report.

### Step 2: Founder Decision (Optional but Recommended)

After reviewing the report, the founder can create a record in the Founder Decisions table:
- Link to the Weekly Insights record for this week
- Decision field: "Increase bachelorette Meta budget by 30% for next 2 weeks"
- Expected outcome: "Higher lead volume from Meta, at least 2 additional bookings"
- Outcome date: 2 weeks from now

### Step 3: Outcome Review (4 Weeks Later)

Four weeks after the decision, the founder returns to the Founder Decisions record and fills in:
- Actual_Outcome: "Meta leads increased but 0 additional bookings. Leads were lower quality."
- Rating: Did not work

The founder creates a Lessons Learned record linked to this decision:
- What was tried: "Increased Meta bachelorette budget 30%"
- What happened: "Lead volume increased by 40% but booking conversion dropped. Higher volume did not equal higher quality."
- What to do differently: "Test a different creative rather than increasing budget on existing creatives."
- Rating: Did not work

### Step 4: Trend Analysis After 4 Weeks

After 4 consecutive weeks of Weekly Insights records, the Claude API system prompt in M-WEEKLY-REPORT-001 can be updated to include a historical context section:

```
In addition to this week's metrics, here are the prior 4-week averages for context:
- Average weekly requests: [X]
- Average chatbot completion rate: [X]%
- Average days to close: [X] days
- Average weekly revenue: $[X,XXX]

Identify any significant deviations from these averages in this week's data.
```

This transforms the weekly analysis from a snapshot into a trend-aware report. Deviations from the 4-week average become the primary signal. A week with 40% more requests than average is notable. A week with 40% fewer is a warning.

### Weekly Insights Table Field Specification

| Field Name | Field Type | Source |
|---|---|---|
| Week_Label | Single line text | "Mon DD MMM to Sun DD MMM YYYY" |
| Week_Start_Date | Date | Last Monday date |
| Raw_Metrics_JSON | Long text | Intelligence payload from M-WEEKLY-REPORT-001 |
| Total_Requests | Number | From aggregation |
| Total_Bookings | Number | From aggregation |
| Total_Revenue | Currency | From aggregation |
| Chatbot_Completion_Rate | Percent | From aggregation |
| Average_Days_to_Close | Number | From Revenue Attribution |
| Top_Source | Single line text | Highest revenue UTM source |
| Top_Campaign | Single line text | Highest revenue campaign slug |
| AI_Narrative | Long text | Claude API response (blank if not enabled) |
| Reviewed_By_Founder | Checkbox | Manual |
| Founder_Decisions | Linked record (Founder Decisions) | Manual link |
| Created_At | Created time | Auto |
