# She Said Sail: Founder Intelligence System
Version 1.0 | May 2026

---

## PURPOSE

The founder intelligence system ensures that She Said Sail accumulates knowledge systematically. Every optimization decision is recorded. Every outcome is tracked. Every lesson is documented. Over time this creates a compounding intelligence advantage that makes the business smarter, faster.

The system has two Airtable tables at its core: Founder Decisions and Lessons Learned. These tables do not run automatically. They require deliberate action from the founder. That deliberateness is the point. The act of recording a decision forces clarity about why the decision was made, what success looks like, and when to check whether it worked.

---

## THE PROBLEM IT SOLVES

Without a structured decision log, businesses repeat their mistakes. A campaign that failed in Q1 is launched again in Q3 because no one recorded why it failed. A concierge approach that worked brilliantly is lost when a team member leaves. An ad creative that underperformed is tested again because the original test result was never stored in a retrievable format.

The founder intelligence system prevents this in three ways:

1. Every decision made from data is linked to the data that prompted it.
2. Every outcome is recorded four weeks after the decision, not six months later when memory has faded.
3. Every lesson is categorized and tagged so it can be searched, referenced, and shared with new team members.

---

## FOUNDER DECISIONS TABLE

This table records every deliberate operational or marketing decision made by the founder in response to data from the weekly learning loop.

### Full Field Schema

| Field Name | Field Type | Purpose |
|---|---|---|
| Decision ID | Auto number | Unique identifier, auto-assigned |
| Decision Date | Date | The date the decision was made |
| Decision Category | Single select | See options below |
| Decision | Long text | What was decided, written in plain language |
| Reason | Long text | Why this decision was made and what data supported it |
| Weekly Insight | Linked record | The Weekly Insights record that prompted this decision |
| Expected Outcome | Long text | What the founder expects to happen as a result |
| Measurement Plan | Long text | How success will be measured and when the measurement will be taken |
| Review Date | Date | Set to 4 weeks after Decision Date at time of record creation |
| Actual Outcome | Long text | What actually happened. Filled in on or after Review Date. |
| Lesson | Long text | What was learned from comparing expected outcome to actual outcome |
| Lesson Linked | Linked record | Points to the corresponding Lessons Learned record, if one was created |
| Status | Single select | See options below |

### Decision Category Options

- Copy
- Chatbot
- Ad Creative
- Concierge
- Pricing
- Funnel
- Experience
- Operations
- Other

### Status Options

- Active (decision has been made, 4 weeks have not yet passed)
- Under Review (Review Date has arrived, outcome is being assessed)
- Outcome Recorded (Actual Outcome and Lesson fields have been filled in)
- Abandoned (the decision was reversed or the planned change was not implemented)

### Airtable View Recommendations

- **Active Decisions view:** Filter Status = Active, sorted by Review Date ascending. This surfaces decisions whose review dates are coming up soonest.
- **Pending Review view:** Filter Status = Under Review OR Review Date is on or before today. Used in the Monday review session to find decisions that need outcomes recorded.
- **By Category view:** Grouped by Decision Category. Used to see all Concierge decisions together, all Ad Creative decisions together, etc.

---

## LESSONS LEARNED TABLE

This table stores reusable knowledge extracted from the outcomes of Founder Decisions. It is the business's institutional memory. Unlike the Founder Decisions table (which captures intent and outcome), the Lessons Learned table captures the distilled, transferable insight.

### Full Field Schema

| Field Name | Field Type | Purpose |
|---|---|---|
| Lesson ID | Auto number | Unique identifier, auto-assigned |
| Lesson Date | Date | The date the lesson was documented |
| Category | Single select | Same options as Founder Decisions.Decision Category |
| Title | Short text | One sentence that names the lesson clearly |
| What Worked | Long text | Specific description of what performed well and by how much |
| What Did Not Work | Long text | Specific description of what underperformed and by how much |
| Why | Long text | The suspected or confirmed reason the outcome occurred as it did |
| Impact | Single select | High, Medium, or Low (based on revenue or conversion effect) |
| Evidence | Long text | The data that supports the lesson. Include specific numbers. |
| Related Decision | Linked record | Points back to the Founder Decisions record this lesson came from |
| Action Taken | Long text | The specific change made based on this lesson |
| Result of Action | Long text | What happened 4 weeks after the action was taken |
| Tags | Multiple select | See tag options below |

### Tag Options

- seasonal
- pricing
- copy
- funnel
- chatbot
- ads
- experience
- concierge
- mobile

Tags allow cross-category search. A lesson about chatbot copy during Q4 holiday season can be tagged both "chatbot" and "seasonal."

### Impact Definitions

- **High:** The lesson produced or is expected to produce a change of greater than 10% in revenue, close rate, or conversion rate.
- **Medium:** The lesson produced or is expected to produce a change of 3% to 10%.
- **Low:** The lesson is useful but its measurable effect is below 3% or is not directly quantifiable.

### Airtable View Recommendations

- **All Lessons by Date view:** All records, sorted by Lesson Date descending. Default view for the Learning Library dashboard.
- **High Impact view:** Filter Impact = High. Used to quickly review the most valuable lessons.
- **By Category view:** Grouped by Category. Use when onboarding a new concierge or reviewing all chatbot lessons before a redesign.
- **By Tag view:** Grouped by Tags. Use when researching a specific topic that crosses categories.

---

## HOW IT WORKS IN PRACTICE

The following is a complete worked example showing the full loop from weekly data to documented lesson.

### Week 6 Example: Golden Hour Escape Chatbot Path

**Step 1: Weekly Report**
The Monday report shows Pink Palm Club has a 45% close rate from chatbot leads. Golden Hour Escape has an 18% close rate from chatbot leads. The difference is 27 percentage points.

**Step 2: AI Analysis Note**
The AI narrative in the Weekly Insights record notes: "Golden Hour Escape inquiry quality from the chatbot may be lower than other experiences. Alternatively, the chatbot recommendation copy for intimate or anniversary occasions may not be creating sufficient intent before handoff. Consider reviewing the chatbot recommendation logic for intimate group occasions."

**Step 3: Founder Creates a Decision Record**
- **Decision Category:** Chatbot
- **Decision:** Update chatbot occasion routing so that intimate and anniversary occasions see a stronger explanation of the Golden Hour Escape value proposition before the experience confirmation state. Specifically, add one additional message in state 7 (recommendation) that describes the sunset timing, private feel, and typical group profile for Golden Hour bookings.
- **Reason:** Golden Hour Escape chatbot close rate is 18% vs. 45% for Pink Palm Club. The most likely cause is that the recommendation framing does not communicate the right value for groups that selected "anniversary" or "intimate gathering" as their occasion.
- **Expected Outcome:** Golden Hour Escape chatbot close rate improves from 18% to at least 28% within 4 weeks.
- **Measurement Plan:** Check Chatbot Conversations table at week 10. Filter by experience_recommended = Golden Hour Escape. Compare close rate (linked bookings divided by chatbot leads) to the current 18% baseline.
- **Review Date:** Four weeks from today.

**Step 4: Copy Update**
The chatbot copy system document is updated. The new framing for the Golden Hour Escape recommendation state is implemented.

**Step 5: Four Weeks Later**
The founder opens the Founder Decisions record on Review Date. The Chatbot Conversations table shows: Golden Hour Escape chatbot leads this period have a 28% close rate, up from 18%.

**Actual Outcome field filled in:** "Golden Hour Escape chatbot close rate improved from 18% to 28% after updating the recommendation framing. The new copy emphasized the sunset timing and the private, intimate atmosphere. Improvement of 10 percentage points in 4 weeks."

**Step 6: Lesson Created**
A new Lessons Learned record is created:
- **Title:** Chatbot value proposition framing for intimate occasions improves Golden Hour Escape close rate
- **Category:** Chatbot
- **What Worked:** Adding specific sensory and atmosphere detail to the Golden Hour Escape recommendation message before handoff. Naming the sunset timing and the private feel increased intent in inquiry leads.
- **What Did Not Work:** The original recommendation message named the experience and gave pricing but did not explain why this experience specifically suits intimate groups.
- **Why:** Buyers selecting anniversary or intimate as their occasion need to see emotional fit before they feel confident enough to submit a form.
- **Impact:** High
- **Evidence:** Close rate moved from 18% to 28% across 43 chatbot conversations in the 4-week period.
- **Action Taken:** Updated state 7 recommendation copy in chatbot-copy-system.md.
- **Tags:** chatbot, copy, experience

---

## THE COMPOUND LEARNING EFFECT

The system's value compounds over time. A single lesson is useful. Forty lessons are a strategic asset.

After one year of weekly loops, the Lessons Learned table will contain approximately 30 to 50 documented lessons. The Founder Decisions table will contain 50 to 100 recorded decisions. This body of structured knowledge has several compounding uses:

**Onboarding new team members:** Instead of relying on institutional memory held by individuals, a new concierge can read the Concierge category of Lessons Learned and understand within hours what approaches work and why.

**Scaling the business:** When adding a new experience or market, the existing lesson library provides tested frameworks for chatbot framing, CTA copy, and ad creative approaches that have already been validated.

**AI training material:** If AI analysis is integrated, the Lessons Learned table can be included in the context provided to the AI. This means the AI's weekly analysis is informed by what has already been tried, preventing recommendations that have already been tested and rejected.

**Investor and partner communication:** A structured record of decisions and outcomes demonstrates operational rigor. It shows that the business is run with data, not intuition alone.

---

## MONTHLY INTELLIGENCE REVIEW PROTOCOL

Beyond the weekly loop, a monthly review is conducted on the first Monday of each month. This takes approximately 30 to 45 minutes.

**1. Review all open Founder Decisions where Review Date has passed.**
Open the Pending Review view in the Founder Decisions table. For each record where Review Date is in the past and Status is not Outcome Recorded, fill in the Actual Outcome and Lesson fields. Update Status to Outcome Recorded.

**2. Identify the 3 highest-impact lessons from the previous month.**
Open the Lessons Learned table filtered to records created in the previous month. Sort by Impact descending. Review the top 3 and confirm they are tagged correctly and cross-referenced to related decisions.

**3. Update the Experience Performance records with monthly metrics.**
Open the Experience Performance table. Review the 4 experience records and confirm that the monthly metrics (requests, bookings, close rate, average booking value) are current. If M-EXPERIENCE-ROLLUP-001 is running correctly, these should be up to date. If any field looks stale, trigger the Make scenario manually.

**4. Assess whether any fundamental changes in booking pattern have occurred.**
Compare the current month's Weekly Insights records to the same month from the prior period (if data exists). Look for structural shifts: a source that was previously top-performing is now underperforming, or a new experience is outperforming its prior baseline. If a shift is material, create a Founder Decision record to document the response.

**5. Set priorities for the next month.**
Based on the lessons documented and the patterns visible in the data, identify one to three priority focus areas for the next month. These are not commitments to specific decisions, but areas that deserve close attention in the coming weekly loops. Record them as a note in the most recent Weekly Insights record's Recommendations field or in a standalone Founder Decisions record with Category = Operations.
