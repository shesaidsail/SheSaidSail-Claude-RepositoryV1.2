# She Said Sail: Airtable Intelligence Dashboard Specifications
Version 1.0 | May 2026

---

## OVERVIEW

Airtable Interfaces (the built-in dashboard tool) hosts all operational and intelligence dashboards. No external BI tool is needed for v1. All dashboards are built using Airtable Interface Designer and are accessible directly within the She Said Sail Airtable base.

Eight dashboards are specified below. Each is purpose-built for a specific user and use case. Dashboards are not interchangeable. The Lead Command Center is a daily operational tool. The Learning Library is a monthly strategic tool. Treat them differently.

**Build order recommendation:** Dashboard 1 and 2 first (operational), then 3 and 4 (revenue), then 5 and 6 (intelligence), then 7 and 8 (learning).

---

## DASHBOARD 1: Lead Command Center

**User:** Founder (daily use)
**Purpose:** Real-time view of all new and active inquiries so no lead is missed and no hot prospect waits more than one business day for a response.
**Interface type:** Summary metrics + record lists
**Update frequency:** Real-time (Airtable syncs on page load)

### Metrics Section (top row)

| Metric | Source | Calculation |
|---|---|---|
| Total requests this week | Requests table | Count of records where Created is within current calendar week |
| Hot leads | Requests table | Count of records where Internal Rating = Hot |
| Unassigned requests | Requests table | Count of records where Assigned Concierge field is empty AND Status is not Closed Lost |

### List Section 1: New Requests

Display the 10 most recently created Requests records.

| Column | Field | Notes |
|---|---|---|
| Name | Name | Full name |
| Occasion | Occasion | Single select value |
| Group Size | Group Size | Number |
| Source | UTM Source | From linked UTM record |
| Internal Rating | Internal Rating | Color-coded (Hot = red, Warm = orange, Cold = blue) |
| Status | Status | Current pipeline stage |

### List Section 2: Hot Leads Pending Response

Display all Requests where Internal Rating = Hot and Status = New or Contacted.

| Column | Field |
|---|---|
| Name | Name |
| Submitted At | Submitted At |
| Assigned Concierge | Assigned Concierge |
| Experience Interest | Experience Interest |

### Filters Available

- Occasion (single select filter on Requests)
- Experience Interest (single select filter on Requests)
- Status (single select filter on Requests)

---

## DASHBOARD 2: Booking Pipeline

**User:** Founder and concierge team
**Purpose:** Tracks every request through the funnel from first inquiry to closed booking. Used in daily concierge operations and weekly pipeline reviews.
**Interface type:** Kanban or grouped list by Status + metric summary
**Update frequency:** Real-time

### Kanban / Pipeline Columns

Requests are grouped by Status field:

1. New
2. Contacted
3. Qualified
4. Proposal Sent
5. Booked
6. Closed Lost

Each card displays: Name, Occasion, Experience Interest, Group Size, Assigned Concierge, days since submission.

### Metrics Section

| Metric | Source | Calculation |
|---|---|---|
| Conversion rate this month | Requests table | Count of Booked records this month divided by total Requests this month, expressed as percentage |
| Average days to close | Requests table | Average of (Booked At minus Submitted At) for all Booked records this month |

### Chart: Requests vs. Bookings by Week

- Chart type: Grouped bar chart
- X axis: Week number (last 8 weeks)
- Y axis: Count
- Bar 1: New Requests per week
- Bar 2: Bookings per week

### Filters Available

- Date range (Submitted At)
- Experience Interest
- Occasion

---

## DASHBOARD 3: Revenue Attribution

**User:** Founder
**Purpose:** Tracks every confirmed booking back to the traffic source, campaign, and creative that generated it. Answers the question: where is revenue actually coming from?
**Interface type:** Metric summary + tables + charts
**Update frequency:** Updated each time a Booking is confirmed and M-BOOKING-OUTCOME-001 runs

### Metrics Section

| Metric | Source | Calculation |
|---|---|---|
| Total revenue booked this month | Revenue Attribution table | Sum of Revenue field for all records where Booked At is within current month |
| Top traffic source | Revenue Attribution table | UTM Source value with highest sum of Revenue this month |
| Top campaign | Revenue Attribution table | UTM Campaign value with highest sum of Revenue this month |

### Table: Revenue by Source

Grouped by utm_source value.

| Column | Field |
|---|---|
| Source | utm_source |
| Requests | Count of linked Requests |
| Bookings | Count of linked Bookings |
| Total Revenue | Sum of Revenue |
| Close Rate | Bookings divided by Requests (formula) |
| ROI | Revenue divided by Campaign budget if budget is entered in Campaigns table |

### Table: Revenue by Creative ID

Grouped by creative_id (populated from utm_content field).

| Column | Field |
|---|---|
| Creative ID | creative_id |
| Bookings | Count |
| Total Revenue | Sum of Revenue |
| Average Booking Value | Average of Revenue |

### Filters Available

- Date range (Booked At)
- Experience (linked Booking experience)

---

## DASHBOARD 4: Experience Performance

**User:** Founder
**Purpose:** Side-by-side comparison of all four experiences on lead volume, conversion quality, and revenue output. Used to make experience-level decisions about pricing, capacity, and marketing weight.
**Interface type:** Summary table + charts
**Update frequency:** Updated weekly by M-EXPERIENCE-ROLLUP-001 (Monday 8:00 AM) and on any new booking

### Table: Experience Comparison

One row per experience (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club).

| Column | Source | Notes |
|---|---|---|
| Experience | Experience Performance.Experience Name | Static |
| Requests this month | Experience Performance.Requests This Month | Count |
| Bookings this month | Experience Performance.Bookings This Month | Count |
| Close Rate | Experience Performance.Close Rate | Formatted as percentage |
| Average Booking Value | Experience Performance.Avg Booking Value | Currency |
| Total Revenue | Experience Performance.Total Revenue This Month | Currency |

### Chart: Lead Volume by Experience Over Time

- Chart type: Stacked or grouped line chart
- X axis: Week
- Y axis: Request count
- One line per experience

### Chart: Close Rate by Experience

- Chart type: Horizontal bar chart
- One bar per experience
- Value: Close rate percentage for current month

### Filters Available

- Date range (applies to request and booking counts)

---

## DASHBOARD 5: Chatbot Intelligence

**User:** Founder
**Purpose:** Tracks the chatbot as a standalone conversion channel. Answers whether the chatbot is qualifying leads, capturing emails, and generating bookings at a rate that justifies its role in the funnel.
**Interface type:** Metric summary + tables
**Update frequency:** Real-time (on each Chatbot Conversations record creation)

### Metrics Section

| Metric | Source | Calculation |
|---|---|---|
| Chatbot conversations this week | Chatbot Conversations table | Count of records created this week |
| Chatbot handoff rate | Chatbot Conversations table | Count where outcome = handoff divided by total conversations this week |
| Email capture rate | Chatbot Conversations table | Count where email_captured = true divided by total conversations |
| Chatbot leads converted to bookings | Chatbot Conversations table | Count of records where linked Request has Status = Booked |

### Table: Conversations by Occasion and Experience Recommended

Grouped by occasion field value.

| Column | Field |
|---|---|
| Occasion | occasion |
| Experience Recommended | experience_recommended |
| Conversations | Count |
| Handoff Rate | Handoffs divided by conversations |

### Table: Chatbot Outcomes by Experience Recommended

One row per experience_recommended value.

| Column | Field |
|---|---|
| Experience Recommended | experience_recommended |
| Conversations | Count |
| Handoff Rate | Percentage |
| Bookings | Count of linked Requests that became Bookings |
| Booking Rate | Bookings divided by conversations |

### Filters Available

- Date range (Conversation Created At)
- Occasion

---

## DASHBOARD 6: Concierge Performance

**User:** Founder
**Purpose:** Tracks how effectively each concierge converts inquiries to bookings. Used to identify best practices, spot response time issues, and make staffing decisions.
**Interface type:** Summary table + metric + record list
**Update frequency:** Real-time

### Table: Concierge Comparison

One row per assigned concierge.

| Column | Source | Notes |
|---|---|---|
| Concierge | Assigned Concierge field | Name |
| Requests Assigned | Requests table | Count where Assigned Concierge = this person |
| Bookings Closed | Requests table | Count where Assigned Concierge = this person AND Status = Booked |
| Close Rate | Bookings divided by Requests | Percentage |
| Average Days to Close | Requests table | Average of (Booked At minus Submitted At) for this concierge's booked records |

### Metric: Average Response Time

Source: Requests table. Calculated as average hours between Submitted At and the timestamp of the first Internal Note entry for each record. This approximates first response time.

Displayed as a single number (average hours) for the current month.

### List: Requests by Concierge and Status

A record list filtered by the selected concierge (using dashboard filter). Shows each assigned request with its current Status, Submitted At, and days in current status.

### Filters Available

- Date range (Submitted At)
- Assigned Concierge

---

## DASHBOARD 7: Weekly Intelligence Feed

**User:** Founder
**Purpose:** Displays the rolling 8-week history of AI-generated weekly analysis reports. Used during the Monday review session to compare current week performance to recent history and track whether recommendations are being acted on.
**Interface type:** Record list + metric summary + chart + linked table
**Update frequency:** Updated every Monday at 8:00 AM by M-WEEKLY-REPORT-001

### Record List: Weekly Insights (Last 8 Weeks)

Sorted by Week Start Date descending. Displays 8 most recent records.

| Column | Field |
|---|---|
| Week | Week Start Date |
| Total Requests | Total Requests This Week |
| Total Bookings | Total Bookings This Week |
| Revenue | Total Revenue This Week |
| AI Summary | AI Summary (truncated, click to expand) |
| Recommendations | Recommendations field |
| Status | Status (Active, Decisions Made, Closed) |

### Metrics Section

| Metric | Source | Calculation |
|---|---|---|
| 4-week average conversion rate | Weekly Insights | Average Close Rate field across last 4 records |
| 4-week average revenue per week | Weekly Insights | Average Total Revenue This Week across last 4 records |

### Chart: Revenue Trend by Week

- Chart type: Line chart
- X axis: Week Start Date (last 8 weeks)
- Y axis: Total Revenue This Week
- One line showing weekly revenue trend

### Linked Section: Related Founder Decisions

A filtered view of the Founder Decisions table showing decisions linked to the displayed Weekly Insights records. Columns: Decision Date, Category, Decision (truncated), Status.

---

## DASHBOARD 8: Learning Library

**User:** Founder (reviewed weekly and in depth monthly)
**Purpose:** The accumulated knowledge base of She Said Sail. Every lesson learned and every decision tracked is searchable here. This is the business's institutional memory.
**Interface type:** Record lists + metric + filters
**Update frequency:** Updated each time a Lessons Learned or Founder Decisions record is created or modified

### Record List: Lessons Learned

All records, sorted by Lesson Date descending.

| Column | Field |
|---|---|
| Date | Lesson Date |
| Category | Category |
| Title | Title |
| Impact | Impact (color-coded: High = green, Medium = yellow, Low = gray) |
| What Worked | What Worked (truncated) |
| Tags | Tags |

**Filters available on this list:**
- Category (Copy, Chatbot, Ads, Concierge, Pricing, Funnel)
- Impact (High, Medium, Low)
- Tags (multi-select)

### Metric: Total Lessons Documented

Single count of all records in Lessons Learned table. Displayed prominently to reinforce the compounding value of the system over time.

### Record List: Founder Decisions

All records, sorted by Decision Date descending.

| Column | Field |
|---|---|
| Date | Decision Date |
| Category | Decision Category |
| Decision | Decision (truncated) |
| Review Date | Review Date |
| Actual Outcome | Actual Outcome (truncated, blank until filled in) |
| Status | Status |

**Filters available on this list:**
- Status (Active, Under Review, Outcome Recorded, Abandoned)
- Category
- Date range (Decision Date)
