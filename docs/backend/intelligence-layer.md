# She Said Sail: Intelligence Layer Architecture

Version: 1.0
Date: 2026-05-18

---

## OVERVIEW

The intelligence layer connects the She Said Sail website, chatbot, and backend into a learning system that gets smarter over time. It extends the existing 7-table Airtable schema and 10-scenario Make.com architecture with new tables, new fields, new scenarios, and weekly AI-generated reporting.

No existing tables are replaced. No existing scenarios are removed. Every addition described in this document is additive only.

The goal is to answer a question that the current backend cannot answer: "What is working, what is not working, and what should we do differently next week?"

---

## ARCHITECTURE DIAGRAM

```
TRAFFIC SOURCES
    |
    |-- Paid Ads (Meta, Google)
    |-- Organic Search
    |-- Social Media (Instagram, TikTok)
    |-- Direct / Referral
    |
    v
WEBSITE (she-said-sail.com)
    |
    |-- GTM fires events: view_homepage, click_request_to_book,
    |   start_booking_form, submit_booking_form, submit_email_capture,
    |   open_chat, scroll_50_percent, scroll_90_percent, etc.
    |
    |-- sss_vid cookie: first-party visitor ID written by she-said-sail-global.js
    |-- UTM parameters: captured in sessionStorage and sent in form payload
    |
    v
CHATBOT (she-said-sail-chatbot.js)
    |
    |-- GTM fires events: chatbot_open, chatbot_start_conversation,
    |   chatbot_select_occasion, chatbot_select_experience,
    |   chatbot_capture_email, chatbot_capture_phone,
    |   chatbot_handoff, chatbot_complete
    |
    |-- On chatbot_complete: sends full conversation JSON to Make webhook
    |
    v
MAKE.COM (webhook receiver)
    |
    |-- EXISTING SCENARIOS (10):
    |   M-WEBFORM-001      Request form capture
    |   M-UTM-001          UTM record creation
    |   M-EMAIL-001        Confirmation email
    |   M-SLACK-001        Slack new lead alert
    |   M-CONCIERGE-001    Concierge assignment
    |   M-ROUTER-001       Brand routing
    |   M-AUDIT-001        Audit logging
    |   M-EMAIL-CAPTURE-001 Homepage email capture
    |   M-CHATBOT-001      Chatbot lead capture
    |   M-CONTACT-001      Contact form capture
    |
    |-- NEW SCENARIOS (4):
    |   M-BOOKING-OUTCOME-001   Links bookings to UTMs and creates attribution record
    |   M-WEEKLY-REPORT-001     Monday morning intelligence report
    |   M-EXPERIENCE-ROLLUP-001 Weekly experience performance aggregation
    |   M-CONCIERGE-SCORE-001   Post-booking concierge quality scoring
    |
    v
AIRTABLE (primary data store)
    |
    |-- EXISTING TABLES (7):
    |   Requests           Form inquiries with Status, UTM fields, Concierge
    |   Bookings           Confirmed charters with revenue, experience, dates
    |   Contacts           One per email, with Lifetime Value rollup
    |   Campaigns          Paid campaign tracking by UTM campaign slug
    |   UTMs               One per form submission, linked to Request and Campaign
    |   Client Notes       Internal notes per Contact or Booking
    |   Audit Log          Immutable Make.com action log
    |
    |-- NEW INTELLIGENCE TABLES (6):
    |   Chatbot Conversations   Full conversation path beyond handoff payload
    |   Revenue Attribution     Booking-to-UTM-to-Campaign link with margin
    |   Experience Performance  Weekly/monthly rollup by experience
    |   Weekly Insights         AI-generated weekly analysis output
    |   Founder Decisions       Decisions made and their outcomes
    |   Lessons Learned         What worked, what did not, and the result
    |
    v
WEEKLY ANALYSIS ENGINE
    |
    |-- M-WEEKLY-REPORT-001 queries all relevant tables
    |-- Formats intelligence payload (JSON)
    |-- Posts raw metrics to Slack #intelligence channel
    |-- Optionally POSTs to Claude API for narrative analysis
    |-- Stores result in Weekly Insights table
    |
    v
OPTIMIZATION RECOMMENDATIONS
    |
    |-- Founder reads Slack report every Monday
    |-- Decisions logged in Founder Decisions table
    |-- Outcomes tracked 4 weeks later in Lessons Learned
    |-- After 4 weeks: trend comparison becomes possible
```

---

## EXISTING BACKEND ASSESSMENT

### What Exists and Works

- Form submissions from the booking request page are captured by M-WEBFORM-001 and written to the Requests table.
- UTM parameters from URL querystrings are captured by M-UTM-001 and written to the UTMs table, linked to the triggering Request record.
- Confirmation emails are sent by M-EMAIL-001 after every form submission.
- Slack alerts for new leads are sent by M-SLACK-001 to the team.
- Concierge assignment is automated by M-CONCIERGE-001.
- Brand routing (if multi-brand in future) is handled by M-ROUTER-001.
- All Make.com actions are logged immutably by M-AUDIT-001 to the Audit Log table.
- Homepage email capture is handled by M-EMAIL-CAPTURE-001.
- Chatbot handoff payloads are captured by M-CHATBOT-001, which creates a Request record with Request_Type = "Chatbot Lead".
- Contact form submissions are captured by M-CONTACT-001.
- The Contacts table maintains a Lifetime Value rollup and Total Bookings count via Airtable rollup fields.

### What Is Missing

1. Booking records are not linked to UTM or Campaign records. A booking for $14,000 cannot be traced to the ad campaign or traffic source that generated the inquiry. Revenue attribution is impossible.

2. The Bookings table has no margin field. Charter costs (crew, boat, provisioning) are not tracked against revenue. Profit by experience, by source, or by campaign cannot be calculated.

3. There is no close time field anywhere. The number of days between a Request being submitted and a Booking being confirmed is unknown. Concierge response speed cannot be correlated with close rate.

4. Chatbot conversations store only the final handoff payload in the Request record. The conversation path, including which states were visited, which questions were asked, which occasion was selected, and which experience was recommended, is not stored anywhere. Chatbot optimization is impossible without this data.

5. Concierge actions are visible in Client Notes but not scored. There is no numeric metric for concierge performance, response quality, or contribution to bookings. Performance management and bonus calculation have no data foundation.

6. Experience performance is not aggregated. No table or view summarizes conversion rate, average booking value, lead volume, or lead quality by experience (Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club). Marketing optimization by experience is done by intuition, not data.

7. Weekly reporting does not exist. There is no Make scenario, Airtable view, or AI analysis system that compiles weekly performance data and delivers it to the founder. The founder has no structured visibility into what happened last week.

8. Visitor ID is not persisted from GA4 to Airtable. Events visible in GA4 analytics and records stored in Airtable cannot be joined at the visitor level. Attribution analysis must rely on UTM parameters alone.

---

## NEW TABLES REQUIRED

### 1. Chatbot Conversations

Stores the full conversation path for every chatbot session that reaches completion or handoff. Includes: session ID, visitor ID (sss_vid), timestamp sequence of states visited, occasion selected, experience recommended, email captured, phone captured, and the final handoff payload. Linked to the Request record created by M-CHATBOT-001.

Purpose: enables chatbot funnel analysis, identifies where users drop off, and measures which occasion and experience combinations have the highest completion rate.

### 2. Revenue Attribution

Links every confirmed Booking record to its originating Request, UTM record, and Campaign record. Stores revenue, estimated charter cost, gross margin, margin percent, days to close, and all attribution lookups. Created by M-BOOKING-OUTCOME-001 when a Request status moves to Booked.

Purpose: closes the loop between marketing spend and booking revenue.

### 3. Experience Performance

Weekly and monthly rollup of lead and booking metrics grouped by experience. Fields include: experience name, week, leads received, bookings confirmed, conversion rate, total revenue, average booking value, top source, top campaign, and average days to close.

Purpose: tells the founder which experiences are generating revenue and which are underperforming, enabling marketing budget allocation decisions.

### 4. Weekly Insights

Stores the output of M-WEEKLY-REPORT-001 every Monday. Fields include: week date range, all raw metrics, the AI narrative text (if Claude API integration is enabled), and status (reviewed or not reviewed).

Purpose: creates a historical record of weekly performance so trend analysis becomes possible after 4 or more weeks of data.

### 5. Founder Decisions

Tracks decisions the founder makes in response to weekly reports. Fields include: decision date, linked Weekly Insights record, the decision made (free text), the expected outcome, and the actual outcome (filled in 4 weeks later).

Purpose: closes the loop between intelligence and action, and enables the system to learn which recommendations lead to positive outcomes.

### 6. Lessons Learned

Captures post-decision outcome analysis. Fields include: linked Founder Decision, what was tried, what happened, what to do differently, and a rating (worked / did not work / neutral).

Purpose: builds the institutional memory of the She Said Sail marketing and operations function.

---

## NEW MAKE SCENARIOS REQUIRED

### M-BOOKING-OUTCOME-001: Booking-to-Attribution Link

Trigger: Airtable record update in Requests table where Status changes to "Booked".

When a team member marks a Request as Booked, this scenario finds the linked UTM record for that Request, finds or creates the corresponding Booking record, creates a Revenue Attribution record linking Request + UTM + Campaign + Booking, calculates Days to Close from UTM First_Seen_At to Booking Deposit Date, and writes the action to the Audit Log.

This is the most critical new scenario. Without it, revenue attribution cannot exist.

### M-WEEKLY-REPORT-001: Monday Morning Intelligence Report

Trigger: Scheduled, every Monday at 8:00 AM in the founder's local timezone.

Queries Airtable for Requests, Bookings, Chatbot Conversations, and Revenue Attribution records from the previous 7 days. Aggregates counts, totals, and breakdowns by occasion, experience, source, and campaign. Formats an intelligence payload as JSON. Posts the raw metrics report to the Slack #intelligence channel. Optionally POSTs to the Claude API for narrative analysis. Creates a Weekly Insights record in Airtable with all metrics and the AI narrative.

### M-EXPERIENCE-ROLLUP-001: Weekly Experience Performance Aggregation

Trigger: Scheduled, every Monday at 7:30 AM (runs before M-WEEKLY-REPORT-001).

Queries Requests and Bookings from the previous 7 days. Groups results by Experience field. Calculates lead count, booking count, conversion rate, total revenue, and average booking value per experience. Creates or updates records in the Experience Performance table.

The 7:30 AM execution ensures Experience Performance records are ready when M-WEEKLY-REPORT-001 runs at 8:00 AM.

### M-CONCIERGE-SCORE-001: Post-Booking Concierge Quality Score

Trigger: Airtable record creation in Revenue Attribution table (fires after M-BOOKING-OUTCOME-001 completes).

Uses the Days to Close value from the new Revenue Attribution record to calculate a response speed score. Combines with Booking Total Value to calculate a weighted concierge performance score for the assigned concierge. Updates the relevant Client Notes or a future Concierge Performance table with this score.

---

## VISITOR AND SESSION ID STRATEGY

### The Problem

GA4 generates a client_id for each browser session, which serves as a persistent visitor identifier across sessions. This ID is stored in the GA4 cookie (_ga). However, GA4 does not expose client_id to JavaScript by default. Airtable form submissions and chatbot payloads have no way to include the GA4 client_id, so events in GA4 and records in Airtable cannot be joined at the visitor level.

### Option A: First-Party Cookie (sss_vid)

Generate a UUID-based first-party cookie named sss_vid via the she-said-sail-global.js script on page load. Logic:

```javascript
function getOrCreateVisitorId() {
  let vid = getCookie('sss_vid');
  if (!vid) {
    vid = crypto.randomUUID();
    setCookie('sss_vid', vid, 365); // 365-day expiry
  }
  return vid;
}
const sss_vid = getOrCreateVisitorId();
window.sss_vid = sss_vid; // expose globally
```

This sss_vid is then:
- Pushed to dataLayer on every GTM event (so it appears in GA4 custom dimensions)
- Included in every form submission webhook payload
- Included in every chatbot handoff payload
- Stored in the UTMs table in a new Visitor_ID field

This allows visitor-level joining between GA4 event data and Airtable records without relying on GA4 internal IDs.

### Option B: Session-Level Join via UTM and Timestamp

Without a persistent cookie, join GA4 sessions to Airtable records using UTM campaign slug plus timestamp proximity. A GA4 session tagged utm_campaign=bachelorette-meta-may2026 that occurred within 30 minutes of a Request record tagged with the same campaign slug can be treated as the same session.

This approach is less precise because: two people can click the same campaign link in the same 30-minute window, and UTM parameters are not always present on direct or organic visits.

### Recommendation: Option A

Add sss_vid cookie generation to she-said-sail-global.js. Include sss_vid in all webhook payloads sent to Make.com. Add a Visitor_ID field to the UTMs table. Push sss_vid to GA4 as a custom dimension named visitor_id.

This gives the system a durable, privacy-compliant first-party identifier that works across the full attribution chain.

### Airtable Fields to Add for Visitor ID

UTMs table: add field Visitor_ID (single line text). Populated by M-WEBFORM-001 and M-CHATBOT-001 from the sss_vid value in the webhook payload.

---

## ATTRIBUTION CHAIN

The full attribution chain from ad impression to revenue:

```
STEP 1: Ad Impression
  Meta or Google shows an ad to a user.
  The ad URL includes: ?utm_source=meta&utm_medium=paid&utm_campaign=bachelorette-may2026&utm_content=reel-01

STEP 2: UTM Click and Cookie Write
  User clicks the ad and lands on she-said-sail.com.
  she-said-sail-global.js runs on page load:
    - Reads utm_* parameters from URL querystring
    - Writes them to sessionStorage as sss_utm
    - Writes first_seen_at timestamp to localStorage
    - Writes or reads sss_vid cookie

  GTM fires: view_homepage (with all UTM parameters and sss_vid)

STEP 3: Exploration
  User browses the site.
  GTM fires: view_experiences_page, click_experience_card, open_chat

STEP 4: Form Submission or Chatbot Completion
  Option A (Form): User completes the booking request form.
    - Form payload includes: name, email, phone, occasion, experience,
      group_size, date, message, utm_source, utm_medium, utm_campaign,
      utm_content, utm_term, sss_vid
    - Payload sent to Make.com webhook (M-WEBFORM-001)

  Option B (Chatbot): User completes the chatbot flow.
    - Chatbot sends handoff payload including: email, phone, occasion,
      experience_recommended, utm_source, utm_medium, utm_campaign,
      sss_vid, full conversation JSON
    - Payload sent to Make.com webhook (M-CHATBOT-001)

STEP 5: Airtable Record Creation (EXISTING)
  M-WEBFORM-001 or M-CHATBOT-001:
    - Creates Request record in Requests table
    - M-UTM-001 creates UTM record in UTMs table, linked to Request
    - UTM record stores: Source, Medium, Campaign, Content, Visitor_ID, First_Seen_At

STEP 6: Campaign Link (EXISTING)
  M-UTM-001 checks Campaigns table for a record matching utm_campaign slug.
  If found: links UTM record to Campaign record.
  Campaign record accumulates lead count via rollup.

STEP 7: Concierge Follow-up (EXISTING)
  M-CONCIERGE-001 assigns the Request to a concierge.
  Concierge contacts the lead, sends proposal.

STEP 8: Booking Confirmation (NEW)
  Team member updates Request.Status to "Booked".
  M-BOOKING-OUTCOME-001 fires:
    - Finds UTM record linked to this Request
    - Creates or finds Booking record
    - Creates Revenue Attribution record:
        Booking.Total_Value -> Revenue Attribution.Revenue
        Charter cost (manual entry) -> Revenue Attribution.Charter_Cost
        UTM.Campaign -> Revenue Attribution.Campaign
        UTM.Source -> Revenue Attribution.UTM_Source
        Days to Close formula -> Revenue Attribution.Days_to_Close

STEP 9: Revenue is attributed
  The $14,000 booking is now linked to:
    utm_source=meta
    utm_campaign=bachelorette-may2026
    utm_content=reel-01
    experience=Monaco Social
    days_to_close=7
    gross_margin=$5,200
```

Every link in this chain is explicit (a linked record field in Airtable), not inferred. The chain is queryable at any step.

---

## MAKE SCENARIO DEPENDENCY MAP

```
EXISTING SCENARIOS:
  M-WEBFORM-001
    calls -> M-UTM-001
    calls -> M-EMAIL-001
    calls -> M-SLACK-001
    calls -> M-CONCIERGE-001
    calls -> M-AUDIT-001

  M-CHATBOT-001
    calls -> M-UTM-001
    calls -> M-SLACK-001
    calls -> M-CONCIERGE-001
    calls -> M-AUDIT-001

NEW SCENARIOS:
  M-BOOKING-OUTCOME-001
    triggered by -> Airtable: Request.Status = "Booked"
    calls -> M-AUDIT-001 (existing)
    triggers -> M-CONCIERGE-SCORE-001 (via Revenue Attribution record creation)

  M-CONCIERGE-SCORE-001
    triggered by -> Airtable: Revenue Attribution record created
    calls -> M-AUDIT-001 (existing)

  M-EXPERIENCE-ROLLUP-001
    triggered by -> Schedule (Monday 7:30 AM)
    reads -> Requests table (existing)
    reads -> Bookings table (existing)
    writes -> Experience Performance table (new)
    calls -> M-AUDIT-001 (existing)

  M-WEEKLY-REPORT-001
    triggered by -> Schedule (Monday 8:00 AM)
    reads -> Requests table (existing)
    reads -> Bookings table (existing)
    reads -> Chatbot Conversations table (new)
    reads -> Revenue Attribution table (new)
    reads -> Experience Performance table (new, populated by M-EXPERIENCE-ROLLUP-001)
    writes -> Weekly Insights table (new)
    calls -> Slack API (existing connection)
    calls -> Claude API (optional, new connection)
    calls -> M-AUDIT-001 (existing)
```

---

## DEPLOYMENT ORDER

The following order is designed to extend the existing system safely. Each phase depends on the previous phase being stable before proceeding.

### Phase 1: Visitor ID Foundation (Week 1)

1. Add sss_vid cookie generation to she-said-sail-global.js.
2. Add sss_vid to all GTM event pushes (dataLayer).
3. Add sss_vid as a GA4 custom dimension named visitor_id.
4. Add Visitor_ID field to UTMs table in Airtable.
5. Update M-WEBFORM-001 to include sss_vid in the webhook payload.
6. Update M-CHATBOT-001 to include sss_vid in the chatbot handoff payload.
7. Update M-UTM-001 to write sss_vid to UTMs.Visitor_ID.

Validation: Submit a test form. Confirm sss_vid appears in the UTMs record.

### Phase 2: Chatbot Conversation Storage (Week 1)

1. Create Chatbot Conversations table in Airtable with all fields.
2. Update M-CHATBOT-001 to write full conversation JSON to Chatbot Conversations table.
3. Link Chatbot Conversations records to Request records.

Validation: Complete a test chatbot flow. Confirm Chatbot Conversations record is created and linked.

### Phase 3: Revenue Attribution (Week 2)

1. Create Revenue Attribution table in Airtable with all fields.
2. Build M-BOOKING-OUTCOME-001 in Make.com.
3. Test by changing a test Request status to "Booked" in Airtable.

Validation: Revenue Attribution record appears with correct Booking, Request, UTM, and Campaign links.

### Phase 4: Experience Performance Rollup (Week 2)

1. Create Experience Performance table in Airtable.
2. Build M-EXPERIENCE-ROLLUP-001 in Make.com.
3. Set schedule to Monday 7:30 AM.
4. Run manually once to verify output.

Validation: Experience Performance records created with correct counts and totals.

### Phase 5: Weekly Report and Intelligence Tables (Week 3)

1. Create Weekly Insights table in Airtable.
2. Create Founder Decisions table in Airtable.
3. Create Lessons Learned table in Airtable.
4. Build M-WEEKLY-REPORT-001 in Make.com (raw metrics only, no Claude API yet).
5. Set schedule to Monday 8:00 AM.
6. Run manually once to verify Slack output.

Validation: Slack #intelligence channel receives formatted weekly report. Weekly Insights record created.

### Phase 6: Concierge Scoring (Week 3)

1. Build M-CONCIERGE-SCORE-001 in Make.com.
2. Trigger on Revenue Attribution record creation.

Validation: After a test booking, concierge score is calculated and stored.

### Phase 7: Claude API Narrative Analysis (Week 4, Optional)

1. Set up Claude API connection in Make.com (HTTP module with API key).
2. Add HTTP module to M-WEEKLY-REPORT-001 after metrics aggregation step.
3. Write system prompt for She Said Sail intelligence analyst role.
4. Post Claude API response to Slack alongside raw metrics.

Validation: Monday report includes AI narrative section in Slack.
