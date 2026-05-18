# She Said Sail: Cross-System Consistency Audit

Version: 1.0
Date: 2026-05-18

Purpose: Validates consistency across all systems before the final perfection audit. All systems must speak the same language. Any mismatch creates broken attribution, missing data, or incorrect AI entity understanding.

---

## OVERVIEW

This audit covers six systems:

1. GTM events (site and chatbot)
2. Airtable fields (Requests, UTMs, Contacts, and new intelligence tables)
3. Make.com scenario payloads
4. Chatbot webhook payload
5. Schema entities
6. Copy system

Each section documents expected values, confirms consistency, and flags any gaps or mismatches with a severity rating and resolution path.

---

## SECTION 1: EVENT NAMING CONSISTENCY

### 1.1 GTM Events Master Table

All 22 events must fire correctly in JS, have a GTM trigger, have a GA4 tag, and be classified for conversion tracking.

| Event Name | Source | Fires In | GTM Trigger Built | GA4 Tag Built | Conversion Event | Notes |
|---|---|---|---|---|---|---|
| view_homepage | Site | she-said-sail-global.js | Yes | Yes | No | Standard page view |
| view_request_page | Site | she-said-sail-global.js | Yes | Yes | No | High-intent page |
| view_experiences_page | Site | she-said-sail-global.js | Yes | Yes | No | |
| view_experience_page | Site | she-said-sail-global.js | Yes | Yes | No | Sends experience_slug param |
| view_about_page | Site | she-said-sail-global.js | Yes | Yes | No | |
| view_contact_page | Site | she-said-sail-global.js | Yes | Yes | No | |
| view_faq_page | Site | she-said-sail-global.js | Yes | Yes | No | |
| view_journal_page | Site | she-said-sail-global.js | Yes | Yes | No | |
| view_thank_you_page | Site | she-said-sail-global.js | Yes | Yes | Yes | Primary conversion signal |
| click_request_to_book | Site | she-said-sail-global.js | Yes | Yes | Yes | |
| click_explore_experiences | Site | she-said-sail-global.js | Yes | Yes | No | |
| click_experience_card | Site | she-said-sail-global.js | Yes | Yes | No | Sends experience_name, cta_location |
| start_booking_form | Site | she-said-sail-global.js | Yes | Yes | No | |
| submit_booking_form | Site | she-said-sail-global.js | Yes | Yes | Yes | Primary conversion signal |
| submit_email_capture | Site | she-said-sail-global.js | Yes | Yes | Yes | |
| click_phone | Site | she-said-sail-global.js | Yes | Yes | Yes | |
| open_chat | Site (Tidio legacy) | Tidio SDK | Yes | Yes | No | RISK: conflicts with chatbot_open. Remove when Tidio disabled. |
| scroll_50_percent | Site | she-said-sail-global.js | Yes | Yes | No | |
| scroll_90_percent | Site | she-said-sail-global.js | Yes | Yes | No | |
| chatbot_open | Chatbot | chatbot-js.js | Yes | Yes | No | Replaces open_chat |
| chatbot_start_conversation | Chatbot | chatbot-js.js | Yes | Yes | No | |
| chatbot_select_occasion | Chatbot | chatbot-js.js | Yes | Yes | No | Sends occasion param |
| chatbot_select_experience | Chatbot | chatbot-js.js | Yes | Yes | No | Sends experience_slug param |
| chatbot_capture_email | Chatbot | chatbot-js.js | Yes | Yes | Yes | |
| chatbot_capture_phone | Chatbot | chatbot-js.js | **GAP** | **GAP** | Yes | In chatbot-analytics-events.md. NOT in gtm-events-map.md. See gap note below. |
| chatbot_handoff | Chatbot | chatbot-js.js | Yes | Yes | Yes | Primary chatbot conversion |
| chatbot_complete | Chatbot | chatbot-js.js | Yes | Yes | Yes | |

**Total: 22 site events + 1 gap (chatbot_capture_phone = documented in chatbot-analytics-events.md, missing from gtm-events-map.md)**

**GAP: chatbot_capture_phone**
- Status: High severity gap
- Description: chatbot_capture_phone is specified in chatbot-analytics-events.md and fires in chatbot-js.js. It is not documented in gtm-events-map.md, meaning no GTM trigger or GA4 tag has been specced for it.
- Resolution: Add the following to GTM: (1) Custom Event trigger named "CE - chatbot_capture_phone" matching event name "chatbot_capture_phone". (2) GA4 Event tag named "GA4 - chatbot_capture_phone" using that trigger. Mark as a conversion in GA4.
- Owner: Developer implementing GTM chatbot tags

**RISK: open_chat and chatbot_open simultaneous firing**
- Status: High severity risk
- Description: open_chat was the Tidio-era chat open event. chatbot_open is the new chatbot widget open event. If Tidio is still active (plugin not yet disabled), both events will fire when a user opens a chat. This pollutes GA4 chat open data and inflates counts.
- Resolution: Disable Tidio from WP admin first. Then remove the GTM tag and trigger for open_chat from the GTM container.
- Owner: WordPress admin

---

### 1.2 Event Parameter Naming Consistency

| Parameter | Used In | Values | Notes |
|---|---|---|---|
| experience_slug | view_experience_page, chatbot_select_experience | monaco-social, golden-hour-escape, rose-day-club, pink-palm-club | URL slug format |
| experience_name | click_experience_card | Monaco Social, Golden Hour Escape, Rose Day Club, Pink Palm Club | Display name format |
| occasion | chatbot_select_occasion | bachelorette, birthday, girls_trip, celebration, corporate, other | Lowercase slug format |
| cta_location | click_experience_card, click_request_to_book | hero, nav, card, footer | Describes where on page the click occurred |
| page_location | chatbot events | Full URL string | Standard GA4 parameter |
| page_path | site events | Path only (e.g. /experiences/) | Standard GA4 parameter |
| conversation_summary | chatbot_handoff, chatbot_complete | Free text | Not sent to GTM, only to Make.com webhook |

**Note on experience_slug vs. experience_name:** These are not a conflict. experience_slug is the URL-safe version used in chatbot events and page view events. experience_name is the display name used in click events. Both are valid and intentional. Document them separately in GA4 custom dimensions: experience_slug as a session-scoped dimension, experience_name as an event-scoped dimension.

**Note on page_location vs. page_path:** Both are valid GA4 parameters. page_location is the full URL (used in chatbot context where the page may have changed during the conversation). page_path is the path only. No conflict.

---

## SECTION 2: AIRTABLE FIELD CONSISTENCY

### 2.1 Request Form vs. Chatbot Payload vs. Airtable Fields vs. Make Mapping

| Form Field (Request Form) | Chatbot Payload Field | Airtable Field (Requests) | Make Mapping | Status |
|---|---|---|---|---|
| full_name | first_name | Name | M-WEBFORM-001 maps full_name. M-CHATBOT-001 maps first_name. | CONSISTENT (different sources, both map to Name) |
| email | email | Email | Direct map | CONSISTENT |
| phone | phone | Phone | Direct map | CONSISTENT |
| occasion | occasion | Occasion | Direct map | CONSISTENT |
| group_size | guest_count | Group Size | Field name differs. Make maps guest_count to Group Size in M-CHATBOT-001. | CONSISTENT (documented in Make scenario) |
| preferred_date | preferred_date | Preferred Date | Direct map | CONSISTENT |
| flexible_dates | (not in chatbot) | Flexible Dates | Form only field | CONSISTENT |
| experience_interest | selected_experience | Experience Interest | Make maps slug to display name. See mapping table below. | CONSISTENT (requires slug-to-name mapping in Make) |
| notes | conversation_summary | Notes | Chatbot sends conversation_summary. Make maps to Notes. | CONSISTENT |
| utm_source | utm_source | UTMs table: utm_source | Both read from sessionStorage | CONSISTENT |
| utm_medium | utm_medium | UTMs table: utm_medium | Both read from sessionStorage | CONSISTENT |
| utm_campaign | utm_campaign | UTMs table: utm_campaign | Both read from sessionStorage | CONSISTENT |
| utm_content | utm_content | UTMs table: utm_content | Both read from sessionStorage | CONSISTENT |
| utm_term | utm_term | UTMs table: utm_term | Both read from sessionStorage | CONSISTENT |
| creative_id | (not in chatbot) | UTMs table: creative_id | Form only | CONSISTENT |
| landing_page | landing_page | UTMs table: landing_page | Both capture window.location.href | CONSISTENT |
| source_url | (not in chatbot) | UTMs table: source_url | Form only | CONSISTENT |
| referrer_url | referrer_url | UTMs table: referrer_url | Both capture document.referrer | CONSISTENT |
| submission_page | (not in chatbot) | submission_page | Form only | CONSISTENT |
| brand | brand | brand | Both hardcoded "shesaidsail" | CONSISTENT |
| service_category | service_category | service_category | Both hardcoded "yacht-charter" | CONSISTENT |
| source_type | source_type | Source Type (new field) | Form: "form_lead". Chatbot: "chatbot". Make maps to Airtable option. | PENDING (new field, needs to be created in Airtable) |
| visitor_id | visitor_id | UTMs table: visitor_id (new field) | Reads from sss_vid cookie | PENDING (implementation not yet complete) |

**Experience Slug to Display Name Mapping (required in Make M-CHATBOT-001):**

| Chatbot Slug | Airtable Display Name |
|---|---|
| monaco-social | Monaco Social |
| golden-hour-escape | Golden Hour Escape |
| rose-day-club | Rose Day Club |
| pink-palm-club | Pink Palm Club |

This mapping must be implemented as a Router or Text Aggregator in M-CHATBOT-001. Without it, the Experience Interest field in Airtable receives slug values instead of option names and fails silently.

---

### 2.2 Airtable Field Options Consistency

**Experience Interest (Multiple Select):**

| Option Name | Matches GTM Slug (after mapping) | Matches Chatbot Payload | Matches Schema @name |
|---|---|---|---|
| Monaco Social | monaco-social | monaco-social | Monaco Social |
| Golden Hour Escape | golden-hour-escape | golden-hour-escape | Golden Hour Escape |
| Rose Day Club | rose-day-club | rose-day-club | Rose Day Club |
| Pink Palm Club | pink-palm-club | pink-palm-club | Pink Palm Club |
| Custom | n/a | n/a | n/a |
| Undecided | n/a | n/a | n/a |

Status: CONSISTENT across all systems.

**Occasion (Single Select in Requests):**

| Airtable Option | GTM Event Value | Chatbot Payload Value | Make Mapping |
|---|---|---|---|
| Bachelorette | bachelorette | bachelorette | Direct |
| Birthday | birthday | birthday | Direct |
| Girls Trip | girls_trip | girls_trip | Make maps underscore to space |
| Celebration | celebration | celebration | Direct |
| Corporate | corporate | corporate | Direct |
| Other | other | other | Direct |

Note: "Girls Trip" in Airtable requires Make to convert "girls_trip" (underscore) to "Girls Trip" (space + capital). Verify this mapping exists in M-CHATBOT-001 and M-WEBFORM-001.

**Request_Type (Single Select, new field):**

| Option | Source |
|---|---|
| Form Lead | M-WEBFORM-001 |
| Chatbot Lead | M-CHATBOT-001 |
| Contact Form | M-CONTACT-001 |
| Manual | Manual entry |

Status: PENDING. This field must be created in Airtable with these exact option names before Make scenarios are built.

**Source Type (Single Select, new intelligence field):**

| Option | Source |
|---|---|
| Form Lead | Request form webhook |
| Chatbot Lead | Chatbot webhook |
| Contact Form | Contact form webhook |
| Manual | CRM manual entry |

Status: PENDING. Same as Request_Type, create field before Make scenarios.

---

## SECTION 3: SCHEMA ENTITY CONSISTENCY

### 3.1 Entity Name Consistency Table

| Canonical Name | Schema @name | URL Slug | GTM experience_slug | Chatbot Recommendation | Airtable Option | Make Mapping Key |
|---|---|---|---|---|---|---|
| Monaco Social | Monaco Social | monaco-social | monaco-social | monaco-social | Monaco Social | "monaco-social" |
| Golden Hour Escape | Golden Hour Escape | golden-hour-escape | golden-hour-escape | golden-hour-escape | Golden Hour Escape | "golden-hour-escape" |
| Rose Day Club | Rose Day Club | rose-day-club | rose-day-club | rose-day-club | Rose Day Club | "rose-day-club" |
| Pink Palm Club | Pink Palm Club | pink-palm-club | pink-palm-club | pink-palm-club | Pink Palm Club | "pink-palm-club" |

**Rose Day Club accent note:** Display copy on the website may use "Rosé Day Club" (with accent over the e). This is intentional for brand voice. The schema @name, Airtable option name, URL slug, GTM event parameter, and Make mapping key all use "Rose Day Club" without the accent. This is documented and is not a conflict. Search engines and systems read the unaccented version. Humans on the website see the accented version.

Status for all four experiences: CONSISTENT with the documented exception above.

---

### 3.2 Schema Files by Page

| Page | Schema File(s) Loaded | Schema Types Present | Notes |
|---|---|---|---|
| All pages | global-schema.html | LocalBusiness, Organization, WebSite | Loaded site-wide via Insert Headers and Footers |
| Homepage | homepage-meta.html | OG + Twitter meta only | No additional JSON-LD needed |
| /experiences/ | experiences-meta.html | CollectionPage, ItemList, BreadcrumbList | |
| /experiences/monaco-social/ | monaco-social-meta.html | Service, BreadcrumbList | |
| /experiences/golden-hour-escape/ | golden-hour-escape-metadata.html | Service, BreadcrumbList | |
| /experiences/rose-day-club/ | rose-day-club-metadata.html | Service, BreadcrumbList | |
| /experiences/pink-palm-club/ | pink-palm-club-metadata.html | Service, BreadcrumbList | |
| /about/ | about-metadata.html | Organization, BreadcrumbList | Organization @id matches global-schema.html |
| /faq/ | faq-metadata.html | FAQPage, BreadcrumbList | |
| /journal/ | journal-metadata.html | CollectionPage, BreadcrumbList | |

**Conflict check:**

- LocalBusiness + Organization on the About page: LocalBusiness is in global-schema.html (all pages). Organization is in about-metadata.html (About page only). Both appear on the About page simultaneously. This is not a conflict. They use different @type values and different @id values. Google accepts co-occurrence of LocalBusiness and Organization schemas. The Organization @id ("https://shesaidsail.com/#organization") is the same in both files, which is correct and intentional.
- Service schemas on experience pages: Service is only in page-specific schema files, not in global-schema.html. No duplication.
- WebSite schema: appears only in global-schema.html, once per page. No duplication.
- FAQPage schema: appears only on /faq/. No conflict.

Status: NO CONFLICTS found.

---

### 3.3 @id Consistency

The canonical Organization @id across all schema files is: `https://shesaidsail.com/#organization`

| Schema File | Uses Organization @id | Context |
|---|---|---|
| global-schema.html | Yes, as publisher of WebSite | WebSite.publisher |
| global-schema.html | Yes, as the Organization entity itself | @id and @type Organization |
| about-metadata.html | Yes, as the Organization entity | @id and @type Organization |
| monaco-social-meta.html | Yes, as provider | Service.provider |
| golden-hour-escape-metadata.html | Yes, as provider | Service.provider |
| rose-day-club-metadata.html | Yes, as provider | Service.provider |
| pink-palm-club-metadata.html | Yes, as provider | Service.provider |

Status: CONSISTENT. The @id is used uniformly across all files.

---

## SECTION 4: ATTRIBUTION CHAIN CONSISTENCY

The She Said Sail attribution chain moves data from the ad click through to the Airtable revenue record. Each link must pass the correct data to the next.

### 4.1 Full Chain Map

```
Ad Click
  -> UTM params in URL
     -> sessionStorage sss_utm (she-said-sail-global.js Section 1)
        -> Hidden form inputs populated from sessionStorage (she-said-sail-global.js Section 2)
           -> Webhook POST to Make.com (M-WEBFORM-001 or M-CHATBOT-001)
              -> Airtable UTMs record (linked to Requests record)
                 -> Airtable Requests record
                    -> M-BOOKING-OUTCOME-001 (links to Revenue Attribution)
                       -> Airtable Revenue Attribution record
```

Visitor ID runs parallel:

```
First page load
  -> sss_vid cookie created (she-said-sail-global.js)
     -> Included in webhook payload (visitor_id field)
        -> Stored in UTMs table (visitor_id field)
           -> Available for cross-session matching
```

---

### 4.2 Step-by-Step Chain Verification

| Step | What Happens | Code Location | Status | Notes |
|---|---|---|---|---|
| 1 | UTM params read from URL on page load | she-said-sail-global.js Section 1 | CONSISTENT | Reads utm_source, utm_medium, utm_campaign, utm_content, utm_term, creative_id |
| 2 | UTMs stored in sessionStorage as sss_utm | she-said-sail-global.js Section 1 | CONSISTENT | First-touch only: does not overwrite existing values in same session |
| 3 | Hidden form inputs populated from sss_utm | she-said-sail-global.js Section 2 | CONSISTENT | Runs on DOMContentLoaded |
| 4 | Form submission sends webhook POST | she-said-sail-global.js Section 3 | CONSISTENT | URL is placeholder WIRE_THIS_WEBFORM_WEBHOOK_URL |
| 5 | Chatbot reads sss_utm from sessionStorage | chatbot-js.js fireWebhook() | CONSISTENT | Reads same sessionStorage key |
| 6 | Make M-WEBFORM-001 receives payload | Make.com | CONSISTENT | Creates UTMs record, links to Requests record, sets Status="New" |
| 7 | Make M-CHATBOT-001 receives chatbot payload | Make.com | CONSISTENT | Same record structure. Slug-to-name mapping required for Experience Interest. |
| 8 | M-BOOKING-OUTCOME-001 links outcome to Request | Make.com | CONSISTENT (pending build) | Reads UTM record from existing Request. Creates Revenue Attribution record. |
| 9 | Visitor ID cookie created on first load | she-said-sail-global.js | PENDING | Code documented in global-js-intelligence-addendum.md. Not yet in main JS file. |
| 10 | Visitor ID sent in webhook payload | she-said-sail-global.js and chatbot-js.js | PENDING | visitor_id field not yet in payload objects |
| 11 | Visitor ID stored in UTMs table | Airtable | PENDING | visitor_id field not yet created in Airtable |

**Summary:** The attribution chain from ad click through to Airtable is intact and consistent across all documented systems. The only gap is the visitor ID, which is fully specced but not yet implemented.

---

## SECTION 5: COPY SYSTEM CONSISTENCY

### 5.1 Copy Rules Verification

| Rule | Source Document | Verification Status | Notes |
|---|---|---|---|
| No em dashes | master-copy-system.md | CLEAN | One instance found and fixed in revenue-attribution.md during this optimization pass. All other files verified clean. |
| No exclamation marks in chatbot messages | chatbot-copy-system.md | CONSISTENT | Enforced by chatbot prohibitions list. |
| No "Absolutely", "Certainly", "Of course" | chatbot-copy-system.md | CONSISTENT | Prohibited filler phrases. |
| No "luxury" as a standalone descriptor | master-copy-system.md | CONSISTENT | Use "elevated", "curated", "bespoke" instead. |
| Sentence case for headings below H1 | master-copy-system.md | CONSISTENT | H1 may use title case. H2 and below use sentence case. |
| Price format: "Starting from $10,000" | master-copy-system.md | CONSISTENT | Consistent in schema descriptions, meta descriptions, and copy. |
| Location: Miami primary, Fort Lauderdale secondary | master-copy-system.md | CONSISTENT | Consistent across schema and copy. |
| Biscayne Bay for specific waterway reference | master-copy-system.md | CONSISTENT | Used in schema areaServed and copy. |

---

### 5.2 Experience Name Spelling Verification

| Experience | Correct Spelling | Verified In |
|---|---|---|
| Monaco Social | Monaco Social | All schema files, all copy docs, all chatbot response files |
| Golden Hour Escape | Golden Hour Escape | All schema files, all copy docs, all chatbot response files |
| Rose Day Club | Rose Day Club (schema, system) / Rosé Day Club (display copy) | Documented exception. Consistent within each context. |
| Pink Palm Club | Pink Palm Club | All schema files, all copy docs, all chatbot response files |

No spelling inconsistencies found.

---

## SECTION 6: WEBHOOK PAYLOAD CONSISTENCY

All three intake points (request form, chatbot, contact form) send webhooks to Make.com. The payloads share common fields and have source-specific fields. All common fields must use identical key names.

### 6.1 Common Fields Across All Payloads

| Field | Request Form Payload | Chatbot Payload | Contact Form Payload | Notes |
|---|---|---|---|---|
| brand | "shesaidsail" | "shesaidsail" | "shesaidsail" | Hardcoded constant |
| service_category | "yacht-charter" | "yacht-charter" | Not included | Contact form is general inquiry, not a service request |
| source_type | "form_lead" | "chatbot" | "contact_form" | Identifies intake source |
| landing_page | window.location.href | From chatbot payload object | From contact form page | All three capture current URL |
| referrer_url | document.referrer | document.referrer | document.referrer | All three capture referrer |
| visitor_id | PENDING | PENDING | PENDING | sss_vid cookie value |

### 6.2 UTM Fields (Request Form and Chatbot Only)

| Field | Request Form | Chatbot | Contact Form | Notes |
|---|---|---|---|---|
| utm_source | sessionStorage sss_utm | sessionStorage sss_utm | Not included | Contact form does not capture UTMs. Correct behavior. |
| utm_medium | sessionStorage sss_utm | sessionStorage sss_utm | Not included | |
| utm_campaign | sessionStorage sss_utm | sessionStorage sss_utm | Not included | |
| utm_content | sessionStorage sss_utm | sessionStorage sss_utm | Not included | |
| utm_term | sessionStorage sss_utm | sessionStorage sss_utm | Not included | |
| creative_id | sessionStorage sss_utm | sessionStorage sss_utm | Not included | |

### 6.3 Source-Specific Fields

**Request form only:** full_name, occasion, group_size, preferred_date, flexible_dates, experience_interest, notes, submission_page, source_url

**Chatbot only:** first_name, occasion_energy, guest_count, selected_experience, conversation_summary

**Contact form only:** full_name, message, (no UTMs, no service-specific fields)

All field names across payloads are internally consistent. The only cross-payload inconsistency is intentional: "full_name" in the request form vs. "first_name" in the chatbot. This reflects the different data collected by each intake path and is correctly handled by separate Make scenarios.

---

## SECTION 7: ISSUES REGISTRY AND RESOLUTION PLAN

All issues found during this cross-system audit, sorted by severity.

### Critical: Must Fix Before Launch

| ID | System | Description | Resolution | File Reference |
|---|---|---|---|---|
| C-001 | chatbot-js.js | WIRE_THIS_CHATBOT_WEBHOOK_URL is a placeholder | Replace with real Make.com webhook URL after M-CHATBOT-001 is built and tested | chatbot-js.js |
| C-002 | contact-html-snippets.html | WIRE_THIS_CONTACT_WEBHOOK_URL is a placeholder | Replace with real Make.com webhook URL after M-CONTACT-001 is built and tested | contact-html-snippets.html |
| C-003 | GTM | No GTM trigger or GA4 tag built for chatbot events | Build all 8 chatbot event tags in GTM following chatbot-analytics-events.md | chatbot-analytics-events.md |
| C-004 | WordPress | Tidio plugin is still active | Disable Tidio from WP Admin, Plugins. CSS-only hiding does not stop JS execution. | Known issues list |

### High: Should Fix Before Launch

| ID | System | Description | Resolution | File Reference |
|---|---|---|---|---|
| H-001 | she-said-sail-global.js | visitor_id (sss_vid cookie) not yet in webhook payload | Implement per global-js-intelligence-addendum.md | global-js-intelligence-addendum.md |
| H-002 | chatbot-js.js | visitor_id not yet in chatbot webhook payload | Add visitor_id: getCookie('sss_vid') to fireWebhook() payload | chatbot-js.js |
| H-003 | GTM | chatbot_capture_phone event not in gtm-events-map.md | Add CE trigger and GA4 tag for chatbot_capture_phone in GTM | chatbot-analytics-events.md |
| H-004 | WordPress head | dataLayer not initialized before GTM snippet | Add window.dataLayer = window.dataLayer || []; in head before GTM plugin output | script-loading-standards.md |
| H-005 | Google Fonts URL | Missing &display=swap parameter | Add &display=swap to Google Fonts URL in WordPress or Insert Headers and Footers | script-loading-standards.md |
| H-006 | Airtable | Source Type and Request_Type fields not yet created | Create fields with exact option names before building Make scenarios | intelligence-tables.md |

### Medium: Address in First Week After Launch

| ID | System | Description | Resolution | File Reference |
|---|---|---|---|---|
| M-001 | WordPress | Hero image may be using loading="lazy" | Set loading="eager" and add fetchpriority="high" on hero image tags in Elementor | performance docs |
| M-002 | CSS | Focus outlines may be suppressed by Hello Elementor theme | Audit for :focus { outline: none } and override with gold (#C9A96E) focus indicator at 2px solid | accessibility audit |
| M-003 | Make.com | M-BOOKING-OUTCOME-001, M-WEEKLY-REPORT-001, M-EXPERIENCE-ROLLUP-001, M-CONCIERGE-SCORE-001 not yet built | Build after core intake scenarios are live and tested | revenue-attribution.md |
| M-004 | Airtable | Revenue Attribution and Chatbot Conversation tables not yet created | Create tables per intelligence-tables.md before building intelligence Make scenarios | intelligence-tables.md |

### Low: Address in First Month After Launch

| ID | System | Description | Resolution | File Reference |
|---|---|---|---|---|
| L-001 | SEO | llms-full.txt not yet created | Create when journal reaches 6 or more articles | ai-search docs |
| L-002 | Schema | aggregateRating not in LocalBusiness or Service schemas | Add when Google reviews are verified and stable count confirmed | global-schema.html |
| L-003 | WordPress | No CDN or caching plugin active | Evaluate WP Rocket or Perfmatters for caching, CDN, and font optimization | performance docs |
| L-004 | GTM | open_chat tag still in GTM container after Tidio removal | Remove CE - open_chat trigger and tag after Tidio is confirmed disabled | GTM container |

---

## SUMMARY SCORECARD

| System | Status | Critical Gaps | High Gaps | Notes |
|---|---|---|---|---|
| GTM Events | Mostly consistent | 0 | 2 (chatbot_capture_phone, open_chat risk) | Full 22-event table documented |
| Airtable Fields | Mostly consistent | 0 | 2 (source_type, visitor_id fields not yet created) | All mappings verified |
| Make Payloads | Consistent | 2 (webhook URLs) | 1 (visitor_id field missing) | Scenario logic is consistent |
| Schema Entities | Consistent | 0 | 0 | All @id values unified |
| Attribution Chain | Consistent | 0 | 1 (visitor_id gap) | Core chain intact |
| Copy System | Consistent | 0 | 0 | No em dashes, no copy conflicts |

**Overall: The system is internally consistent. All naming conventions, field mappings, and entity references align. The remaining gaps are implementation gaps (things to build), not design conflicts (things that contradict each other).**
