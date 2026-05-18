# She Said Sail: GA4 Event Configuration

Configuration reference for all GA4 events. Use this alongside the GTM Events Map to set up GA4 event sending and conversion marking.

GA4 Measurement ID: GT-WV3X86GZ

---

## Primary Conversions

These events are marked as conversions in GA4 Admin > Events > Mark as conversion.

### submit_booking_form

| Property | Value |
|---|---|
| Event Name | `submit_booking_form` |
| GTM Trigger | CE - submit_booking_form |
| Parameters Sent | `occasion`, `group_size`, `experience_interest`, `form_id` |
| Conversion | Yes. Mark in GA4 Admin > Events > toggle Conversion column ON. |
| Notes | Fires when MetForm submit succeeds on /request-to-book/. This is the primary lead event. |

### view_thank_you_page

| Property | Value |
|---|---|
| Event Name | `view_thank_you_page` |
| GTM Trigger | CE - view_thank_you_page |
| Parameters Sent | `conversion_type` ("booking_inquiry"), `page_path` |
| Conversion | Yes. Mark in GA4 Admin > Events > toggle Conversion column ON. |
| Notes | Fires when /thank-you/ loads. Second confirmation of a completed inquiry. In GA4, this is used as the primary conversion for campaign reporting because it is page-based and harder to fire accidentally. |

---

## Micro-Conversions

These events are marked as conversions in GA4 Admin to allow reporting on partial funnel completion.

### submit_email_capture

| Property | Value |
|---|---|
| Event Name | `submit_email_capture` |
| GTM Trigger | CE - submit_email_capture |
| Parameters Sent | `page_path` |
| Conversion | Yes. Mark in GA4 Admin > Events. |
| Notes | Fires on homepage email capture. Lower-intent signal than form submission, but useful for email list growth reporting. |

### scroll_90_percent

| Property | Value |
|---|---|
| Event Name | `scroll_90_percent` |
| GTM Trigger | CE - scroll_90_percent |
| Parameters Sent | `page_path` |
| Conversion | Yes. Mark in GA4 Admin > Events. |
| Notes | Fires when user scrolls 90% of any page. High engagement signal. Useful for content quality assessment. |

---

## All Events: Full Reference

| Event Name | Trigger | Parameters | Conversion |
|---|---|---|---|
| `view_homepage` | Page load on / | page_path, page_title | No |
| `view_request_page` | Page load on /request-to-book/ | page_path | No |
| `view_experiences_page` | Page load on /experiences/ | page_path | No |
| `click_request_to_book` | CTA button click | cta_location, page_path | No |
| `click_explore_experiences` | Explore CTA click | page_path | No |
| `click_experience_card` | Experience card click | experience_name, card_position | No |
| `start_booking_form` | First form field interaction | form_id | No |
| `submit_booking_form` | Successful form submit | occasion, group_size, experience_interest | YES |
| `submit_email_capture` | Email capture submit | page_path | YES (micro) |
| `click_phone` | Phone link click | page_path | No |
| `open_chat` | Tidio chat open | page_path | No |
| `view_thank_you_page` | /thank-you/ page load | conversion_type | YES |
| `scroll_50_percent` | Scroll depth 50% | page_path | No |
| `scroll_90_percent` | Scroll depth 90% | page_path | YES (micro) |

---

## How to Mark Events as Conversions in GA4

1. Go to GA4 Admin (gear icon, bottom left of Google Analytics).
2. Under the Property column, click Events.
3. Find the event in the list (it will appear here after it fires at least once, or you can manually create it).
4. Toggle the Conversion column to ON for the events listed above.
5. Confirm: a blue toggle indicates the event is marked as a conversion.

Note: GA4 can take 24-48 hours to show new events after they first fire. Fire each event using GTM Preview mode to confirm data is arriving, then mark them as conversions after they appear in the Events list.

---

## GA4 Audience Definitions for Remarketing

Configure these audiences in GA4 Admin > Audiences. They are used for Google Ads remarketing and can be shared with Meta/TikTok via linked integrations.

### Audience 1: Homepage Visitors 30 Days

| Setting | Value |
|---|---|
| Audience Name | SSS - Homepage Visitors 30d |
| Condition | Event: `view_homepage` |
| Membership Duration | 30 days |
| Use Case | Broad awareness retargeting. |

### Audience 2: Request Page Clickers 60 Days

| Setting | Value |
|---|---|
| Audience Name | SSS - Request Page Visitors 60d |
| Condition | Event: `view_request_page` |
| Membership Duration | 60 days |
| Use Case | High-intent retargeting. These users visited the booking page but may not have submitted. |

### Audience 3: Form Starters 30 Days

| Setting | Value |
|---|---|
| Audience Name | SSS - Form Starters 30d |
| Condition | Event: `start_booking_form` |
| Membership Duration | 30 days |
| Use Case | Highest-intent retargeting. Started the form but did not complete. |

### Audience 4: Email Captures 90 Days

| Setting | Value |
|---|---|
| Audience Name | SSS - Email Subscribers 90d |
| Condition | Event: `submit_email_capture` |
| Membership Duration | 90 days |
| Use Case | Nurture audience. Opted in but has not submitted the booking form. |

### Audience 5: Converters Exclusion 180 Days

| Setting | Value |
|---|---|
| Audience Name | SSS - Converters Exclusion 180d |
| Condition | Event: `submit_booking_form` OR `view_thank_you_page` |
| Membership Duration | 180 days |
| Use Case | Exclusion audience. Add this as an exclusion to all paid campaigns to avoid paying to retarget people who already submitted an inquiry. |

---

## GA4 Funnel Exploration

Use GA4 Explore > Funnel Exploration to visualize the booking funnel. Set up as follows:

**Funnel Name:** She Said Sail Booking Funnel

**Steps:**

| Step | Event | Label |
|---|---|---|
| 1 | `view_homepage` | Homepage Visit |
| 2 | `click_request_to_book` | Clicked Request to Book |
| 3 | `start_booking_form` | Started Form |
| 4 | `submit_booking_form` | Submitted Form |

**Settings:**
- Type: Open funnel (users can enter at any step)
- Counting method: Once per user per session
- Date range: Last 28 days (or last 90 days for enough data)

**What to look for:**
- Drop-off between Step 1 and Step 2: CTA visibility issue
- Drop-off between Step 2 and Step 3: Form page friction (load time, copy, layout)
- Drop-off between Step 3 and Step 4: Form completion friction (too many fields, validation errors, mobile issues)
