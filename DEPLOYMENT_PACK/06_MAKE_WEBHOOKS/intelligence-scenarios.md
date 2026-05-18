# She Said Sail: Intelligence Layer Make.com Scenarios
**Version:** 1.0
**Date:** May 2026
**Purpose:** Defines the four new Make.com automation scenarios that form the intelligence layer. These extend the existing 10-scenario architecture. No existing scenarios are modified.

---

## SCENARIO INDEX

| Scenario ID | Name | Trigger | Purpose |
|---|---|---|---|
| M-BOOKING-OUTCOME-001 | BOOKING-OUTCOME-LINKER | Airtable record change | Links confirmed bookings to UTM and campaign data. Creates Revenue Attribution record. |
| M-WEEKLY-REPORT-001 | WEEKLY-INTELLIGENCE-REPORT | Scheduled (Monday 8:00 AM) | Queries last 7 days of data. Formats intelligence payload. Posts to Slack. Creates Weekly Insights record. |
| M-EXPERIENCE-ROLLUP-001 | EXPERIENCE-PERFORMANCE-ROLLUP | Scheduled (Monday 8:30 AM) | Aggregates booking and request metrics by experience. Creates/updates Experience Performance records. |
| M-CONCIERGE-SCORE-001 | CONCIERGE-PERFORMANCE-SCORER | Airtable record change | When a Booking is confirmed, calculates concierge performance metrics and logs them. |

Build in the order listed. M-BOOKING-OUTCOME-001 must be tested before M-WEEKLY-REPORT-001 runs.

---

## M-BOOKING-OUTCOME-001: BOOKING-OUTCOME-LINKER

**Trigger type:** Airtable - Watch Records (Requests table)
**Watch condition:** Status field changes to "Booked"
**Schedule:** Real-time (fires on every eligible Requests record change)

### Purpose

When a team member updates a Request status to "Booked", this scenario:
1. Creates or finds the linked Booking record
2. Finds the UTM record for that Request
3. Creates a Revenue Attribution record linking Booking + Request + UTM + Campaign
4. Writes to the Audit Log

### Module Sequence

| Step | Module | Configuration |
|---|---|---|
| 1 | Airtable: Watch Records | Table: Requests. Filter: Status = Booked. Watch for new records matching filter only (not updates to existing Booked records). |
| 2 | Airtable: Get a Record | Table: Requests. Record ID: `{{1.id}}`. Expand: UTM Record (linked), Contact (linked), Bookings (linked). |
| 3 | Router | Route A: Booking record already linked. Route B: No booking record yet. |
| 4a (Route A) | Airtable: Get a Record | Table: Bookings. Record ID from linked Bookings field. Get Total Value, Charter Cost, Experience, Deposit Date. |
| 4b (Route B) | Airtable: Create a Record | Table: Bookings. Request: `{{2.id}}`. Contact: linked Contact ID. Experience: from Request.Experience Interest. Status: Deposit Received. Group Size: from Request. Charter Date: from Request.Preferred Date. Note: team must manually fill Total Value and Charter Cost after this record is created. |
| 5 | Tools: Set Variable | booking_id = ID of the Booking record (from 4a or 4b). |
| 6 | Airtable: Get a Record | Table: UTMs. Record ID: from Request.UTM Record linked field. Get all UTM fields. |
| 7 | Airtable: Search Records | Table: Campaigns. Search by: UTM Campaign Slug = `{{6.utm_campaign}}`. |
| 8 | Tools: Set Variable | campaign_id = Campaign record ID if found (may be null for untracked organic traffic). |
| 9 | Airtable: Create a Record | Table: Revenue Attribution. Fields: Booking = booking_id. Request = `{{2.id}}`. UTM Record = `{{6.id}}`. Campaign = campaign_id (if found). UTM Source = `{{6.utm_source}}`. UTM Campaign = `{{6.utm_campaign}}`. UTM Content = `{{6.utm_content}}`. Creative ID = `{{6.creative_id}}`. First Seen At = `{{6.first_seen_at}}`. Request Submitted At = `{{2.submitted_at}}`. Source Type = `{{2.source_type}}`. |
| 10 | Airtable: Update a Record | Table: Requests. Record ID: `{{2.id}}`. Fields: Revenue Attribution = linked to record from Step 9. |
| 11 | Airtable: Update a Record | Table: Bookings. Record ID: booking_id. Fields: Revenue Attribution = linked to record from Step 9. |
| 12 | Call M-AUDIT-001 | Event Type: BOOKING_OUTCOME_LINKED. Linked Record Type: Booking. Linked Record ID: booking_id. Details: "Revenue attribution record created for booking {{booking_id}} from source {{utm_source}}." |
| 13 | Slack: Create a Message | Channel: #intelligence. Message: "Booking confirmed: [Request Name] [Experience] [Group Size] guests. Source: [utm_source] / [utm_campaign]. Airtable: [link]." |

### Error Handling

- If UTM record not found: create Revenue Attribution with Source Type only. Log to Audit Log as Warning.
- If Campaign not found: create Revenue Attribution without Campaign link. This is expected for organic traffic.
- Retry: 1 attempt, no loop (to prevent duplicate Revenue Attribution records).

---

## M-WEEKLY-REPORT-001: WEEKLY-INTELLIGENCE-REPORT

**Trigger type:** Scheduled
**Schedule:** Every Monday at 8:00 AM (configure for US Eastern time)
**Run once per week**

### Purpose

Aggregates last 7 days of data from Airtable and posts an intelligence report to Slack #intelligence. Optionally sends to Claude API for narrative analysis. Creates a Weekly Insights record for trend tracking.

### Date Range Calculation

- Period End: previous Sunday at 23:59:59
- Period Start: previous Monday at 00:00:00
- ISO week: calculated from Period Start

### Module Sequence

| Step | Module | Configuration |
|---|---|---|
| 1 | Tools: Set Variable | period_start = start of last Monday (date calculation). period_end = end of last Sunday. week_label = ISO week string. |
| 2 | Airtable: Search Records | Table: Requests. Filter: Submitted At >= period_start AND Submitted At <= period_end. Get all records. |
| 3 | Tools: Aggregate | Count total requests. Count by Occasion. Count by Experience Interest. Count by Source Type. Count by Internal Rating. Count Closed Lost. |
| 4 | Airtable: Search Records | Table: Bookings. Filter: Deposit Date >= period_start AND Deposit Date <= period_end. |
| 5 | Tools: Aggregate | Count bookings. Sum Total Value (total revenue). Group by Experience. |
| 6 | Airtable: Search Records | Table: Chatbot Conversations. Filter: Started At >= period_start AND Started At <= period_end. |
| 7 | Tools: Aggregate | Count conversations. Count where Outcome = Handoff Completed. Group by Experience Recommended. |
| 8 | Airtable: Search Records | Table: Revenue Attribution. Filter: Booking Confirmed At >= period_start AND Booking Confirmed At <= period_end. |
| 9 | Tools: Aggregate | Identify top UTM Source by count. Identify top UTM Campaign by count. Average Days Total. |
| 10 | Tools: Set Variable | Format complete intelligence_payload as JSON with all metrics. |
| 11 | HTTP: Make a Request (Optional) | POST intelligence_payload to Claude API. System prompt: "You are the She Said Sail intelligence analyst. Review the weekly metrics below and provide: (1) What worked this week - be specific. (2) What needs attention - be specific. (3) Three recommendations for next week. Be direct. Be concise. Luxury brand voice. No em dashes. Max 400 words." API response = ai_narrative. |
| 12 | Airtable: Create a Record | Table: Weekly Insights. Week: week_label. Period Start: period_start. Period End: period_end. Total Requests: from Step 3. Bachelorette Requests: from Step 3. Birthday Requests: from Step 3. Girls Trip Requests: from Step 3. Total Bookings: from Step 5. Total Revenue: from Step 5. Chatbot Conversations: from Step 7. Chatbot Handoffs: from Step 7. Top Traffic Source: from Step 9. Top Campaign: from Step 9. Average Days to Close: from Step 9. Hot Leads Count: from Step 3. Closed Lost Count: from Step 3. AI Analysis: ai_narrative (or empty). Status: Draft. |
| 13 | Slack: Create a Message | Channel: #intelligence. Message: formatted weekly report (see format below). |
| 14 | Call M-AUDIT-001 | Event Type: WEEKLY_REPORT_GENERATED. Details: "Weekly intelligence report generated for {{week_label}}." |

### Weekly Slack Report Format

```
*She Said Sail: Weekly Intelligence Report*
*Week: [ISO week, e.g., 2026-W20] | [Period Start] to [Period End]*

*REQUESTS*
Total: [X] requests ([+/-X vs last week if available])
Bachelorette: [X] | Birthday: [X] | Girls Trip: [X] | Other: [X]
Hot leads: [X] | Closed lost: [X]
Top source: [utm_source] | Top campaign: [utm_campaign]

*BOOKINGS AND REVENUE*
Bookings confirmed: [X]
Revenue booked: $[X]
Average booking value: $[X]
Top experience: [experience with most bookings]

*CHATBOT*
Conversations: [X] | Handoffs: [X] | Completion rate: [X]%
Top chatbot occasion: [occasion]
Top chatbot recommendation: [experience_recommended]

*ATTRIBUTION*
Average days to close: [X]
Revenue by source: [source]: $[X], [source]: $[X]

*EXPERIENCE BREAKDOWN*
Monaco Social: [X] requests, [X] bookings, [close rate]% close rate
Golden Hour Escape: [X] requests, [X] bookings, [close rate]% close rate
Rose Day Club: [X] requests, [X] bookings, [close rate]% close rate
Pink Palm Club: [X] requests, [X] bookings, [close rate]% close rate

[If Claude API connected:]
*AI ANALYSIS*
[ai_narrative text]
```

---

## M-EXPERIENCE-ROLLUP-001: EXPERIENCE-PERFORMANCE-ROLLUP

**Trigger type:** Scheduled
**Schedule:** Every Monday at 8:30 AM (30 minutes after M-WEEKLY-REPORT-001)

### Purpose

Creates one Experience Performance record per experience per week, populating it with the week's request and booking metrics. Runs for all four experiences every Monday.

### Module Sequence

| Step | Module | Configuration |
|---|---|---|
| 1 | Tools: Set Variable | period_start, period_end, week_label (same as M-WEEKLY-REPORT-001 Step 1). |
| 2 | Repeater | Iterate over the four experience names: ["Monaco Social", "Golden Hour Escape", "Rose Day Club", "Pink Palm Club"]. |
| 3 (per experience) | Airtable: Search Records | Table: Requests. Filter: Submitted At in period AND Experience Interest contains current experience name. Count results. |
| 4 (per experience) | Airtable: Search Records | Table: Bookings. Filter: Deposit Date in period AND Experience = current experience name. Count results. Sum Total Value. |
| 5 (per experience) | Airtable: Search Records | Table: Requests. Filter: Same as Step 3 AND Source Type = Chatbot Lead. Count chatbot leads. |
| 6 (per experience) | Airtable: Create a Record | Table: Experience Performance. Experience: current experience name. Week: week_label. Period Start: period_start. Period End: period_end. Requests This Week: from Step 3. Bookings This Week: from Step 4. Revenue This Week: from Step 4. Chatbot Leads This Week: from Step 5. |
| 7 | Call M-AUDIT-001 | Event Type: EXPERIENCE_ROLLUP_COMPLETED. Details: "Experience performance records created for [week_label]." |

---

## M-CONCIERGE-SCORE-001: CONCIERGE-PERFORMANCE-SCORER

**Trigger type:** Airtable - Watch Records (Bookings table)
**Watch condition:** Status field changes to "Paid in Full"

### Purpose

After a booking is fully paid, scores the concierge who handled the inquiry. Writes a structured performance note to Client Notes.

### Scoring Logic

| Metric | How Calculated | Score Contribution |
|---|---|---|
| Close rate | Whether the inquiry converted to booking | Pass/Fail |
| Days to close | From Revenue Attribution.Days Request to Booking | Fast (<7 days) = +1, Standard (7-21 days) = 0, Slow (>21 days) = -1 |
| Booking value | Total Value from Booking | High (>$15,000) = +1, Standard ($10,000-$14,999) = 0 |
| Notes quality | Count of Client Notes linked to the Contact/Booking | At least 2 notes = Documented, else Undocumented |

### Module Sequence

| Step | Module | Configuration |
|---|---|---|
| 1 | Airtable: Watch Records | Table: Bookings. Filter: Status = Paid in Full. |
| 2 | Airtable: Get a Record | Table: Bookings. Expand: Request (linked), Revenue Attribution (linked). |
| 3 | Airtable: Get a Record | Table: Requests. Get: Assigned Concierge, Submitted At, Experience Interest. |
| 4 | Tools: Calculate | days_to_close = Revenue Attribution.Days Request to Booking. booking_value = Booking.Total Value. |
| 5 | Tools: Set Variable | performance_score based on scoring logic above. performance_note = formatted string. |
| 6 | Airtable: Create a Record | Table: Client Notes. Contact: linked Contact. Booking: Booking ID. Note Type: Internal Note. Note: performance_note string. Created By: System (M-CONCIERGE-SCORE-001). |
| 7 | Call M-AUDIT-001 | Event Type: CONCIERGE_SCORED. Details: "Performance scored for booking [booking_id], concierge [assigned_concierge]." |

---

## MAKE SCENARIO DEPENDENCY MAP

```
M-WEBFORM-001 (existing)
  calls M-UTM-001 (existing)
  calls M-EMAIL-001 (existing)
  calls M-SLACK-001 (existing)
  calls M-CONCIERGE-001 (existing)
  calls M-AUDIT-001 (existing)

M-CHATBOT-001 (existing)
  calls M-AUDIT-001 (existing)

M-BOOKING-OUTCOME-001 (NEW)
  triggered by: Request.Status = Booked (Airtable watch)
  creates: Revenue Attribution record
  calls M-AUDIT-001 (existing)

M-WEEKLY-REPORT-001 (NEW)
  triggered by: schedule (Monday 8:00 AM)
  reads: Requests, Bookings, Chatbot Conversations, Revenue Attribution
  creates: Weekly Insights record
  optionally calls: Claude API (HTTP)
  posts to: Slack #intelligence

M-EXPERIENCE-ROLLUP-001 (NEW)
  triggered by: schedule (Monday 8:30 AM)
  reads: Requests, Bookings
  creates: Experience Performance records (4 per week)
  calls M-AUDIT-001 (existing)

M-CONCIERGE-SCORE-001 (NEW)
  triggered by: Booking.Status = Paid in Full (Airtable watch)
  reads: Bookings, Requests, Revenue Attribution
  creates: Client Notes record
  calls M-AUDIT-001 (existing)
```

---

## VISITOR ID IMPLEMENTATION

The sss_vid cookie enables cross-system visitor linking. Add to she-said-sail-global.js Section 0 (before UTM capture):

```javascript
(function() {
  function generateVid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0;
      var v = c === 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
  if (!document.cookie.match(/sss_vid=/)) {
    var vid = generateVid();
    var expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1);
    document.cookie = 'sss_vid=' + vid + '; expires=' + expires.toUTCString() + '; path=/; SameSite=Lax';
  }
  window.__sssVid = (document.cookie.match(/sss_vid=([^;]+)/) || [])[1] || '';
})();
```

Then include `visitor_id: window.__sssVid` in all webhook payloads (request form, chatbot handoff, contact form, email capture).

---

## TESTING INTELLIGENCE SCENARIOS

### Test M-BOOKING-OUTCOME-001

1. Create a test Request in Airtable with a linked UTM record.
2. Change the Request Status to "Booked."
3. Verify in Make.com execution log: scenario ran.
4. Verify in Airtable: Revenue Attribution record created, linked to Booking and UTM.
5. Verify in Audit Log: BOOKING_OUTCOME_LINKED entry.

### Test M-WEEKLY-REPORT-001

1. Manually trigger the scenario from Make.com (use the "Run once" button).
2. Verify: Weekly Insights record created in Airtable.
3. Verify: Slack message posted to #intelligence.
4. Check all metric fields are populated correctly.

### Test M-EXPERIENCE-ROLLUP-001

1. Manually trigger the scenario.
2. Verify: 4 new Experience Performance records created (one per experience).
3. Check Requests This Week and Bookings This Week match manual count.
