# GTM Container Import Instructions

**File:** `07_GTM_ANALYTICS/gtm-container-import.json`
**Container:** GTM-TZ5KNRTH
**Time to complete:** 15 minutes

---

## What this file does

`gtm-container-import.json` is a ready-to-import GTM container export. It creates all variables, triggers, and tags in one operation instead of manually building each one.

What gets created on import:

- 11 variables (10 Data Layer Variables + 1 Custom JavaScript)
- 27 triggers (1 All Pages pageview + 26 custom event triggers)
- 35 tags (1 GA4 Configuration + 26 GA4 Event tags + 4 Meta Pixel Custom HTML tags + 4 TikTok Pixel Custom HTML tags)

After import you replace three placeholder values with real IDs and publish.

---

## Before you start

Confirm these before importing:

- [ ] You have access to GTM container GTM-TZ5KNRTH with Publish permission (not just Read)
- [ ] You have your GA4 Measurement ID (format: G-XXXXXXXXX). The She Said Sail GA4 ID is GT-WV3X86GZ.
- [ ] You have your Meta Pixel ID (format: a 15 to 16 digit number)
- [ ] You have your TikTok Pixel ID (format: alphanumeric string from TikTok Ads Manager)

---

## Step 1: Open the GTM container

1. Go to tagmanager.google.com
2. Select account: **She Said Sail**
3. Select container: **GTM-TZ5KNRTH**
4. You should land on the Workspace overview

---

## Step 2: Import the container file

1. In the left sidebar, click **Admin**
2. Under the Container column (right column), click **Import Container**
3. Click **Choose container file**
4. Select `07_GTM_ANALYTICS/gtm-container-import.json` from your local machine
5. Under **Choose workspace**, select **Existing workspace** and choose **Default Workspace**
6. Under **Choose an import option**, select **Merge**
   - Do NOT select Overwrite. Merge preserves any existing tags.
   - If this is a brand-new container with no existing tags, Overwrite is also safe.
7. Click **Confirm**
8. GTM shows you a preview of everything that will be created. Review the counts:
   - Variables: 11
   - Triggers: 27
   - Tags: 35
9. Click **Confirm** again to complete the import

---

## Step 3: Replace placeholder IDs

After import, three placeholder values need to be replaced before the tags will fire correctly.

### 3a. GA4 Measurement ID

1. In the left sidebar, click **Tags**
2. Search for: `GA4 - Configuration`
3. Click the tag to open it
4. Find the field labeled **Measurement ID**
5. It will say `YOUR_GA4_MEASUREMENT_ID`
6. Replace it with: `GT-WV3X86GZ`
7. Click **Save**

### 3b. Meta Pixel ID

1. In the left sidebar, click **Tags**
2. Search for: `Meta`
3. You will see 4 Meta Pixel tags: PageView, ViewContent, InitiateCheckout, Lead
4. Open each one
5. In the HTML, find the line containing `YOUR_META_PIXEL_ID`
6. Replace it with your actual Meta Pixel ID (the 15 to 16 digit number from your Meta Ads account)
7. Save each tag

To find your Meta Pixel ID: Meta Ads Manager > Events Manager > select your pixel > the ID appears at the top.

### 3c. TikTok Pixel ID

1. In the left sidebar, click **Tags**
2. Search for: `TikTok`
3. You will see 4 TikTok Pixel tags: PageView, ViewContent, InitiateCheckout, Lead
4. Open each one
5. In the HTML, find the line containing `YOUR_TIKTOK_PIXEL_ID`
6. Replace it with your actual TikTok Pixel ID
7. Save each tag

To find your TikTok Pixel ID: TikTok Ads Manager > Assets > Events > Web Events > select your pixel.

---

## Step 4: Preview and verify

Before publishing, verify that events fire correctly using GTM Preview mode.

1. Click **Preview** (top right of GTM workspace)
2. Enter the staging or production URL and click **Connect**
3. A browser tab opens with the site. A debug panel appears at the bottom.
4. In the debug panel, click the **Tags** tab to see what fires on each event.

### What to check

| Action on site | Expected event in debug panel |
|---|---|
| Page loads (any page) | GA4 Configuration tag fires |
| Homepage loads | `view_homepage` GA4 event fires |
| Request to Book page loads | `view_request_page` GA4 event fires |
| Click any Request to Book button | `click_request_to_book` event fires |
| Submit the booking form | `submit_booking_form` event fires |
| Chatbot widget opens | `chatbot_open` event fires |
| Chatbot reaches handoff state | `chatbot_handoff` event fires |

If a tag shows as **Fired**, the trigger and tag are working. If it shows as **Not Fired**, check:
- That the dataLayer push is actually happening (use browser console: `window.dataLayer`)
- That the trigger event name matches exactly what the JS pushes
- That the GA4 Measurement ID is correct

---

## Step 5: Publish

Once Preview confirms tags are firing:

1. Click **Submit** (top right of GTM workspace)
2. Under **Submission Configuration**, enter a version name: `Initial import - all events`
3. Add a description: `Import of all GA4 events, Meta Pixel, and TikTok Pixel from gtm-container-import.json`
4. Click **Publish**
5. GTM creates version 1 (or next version number) and the container goes live

Publishing takes effect within 30 seconds. You do not need to touch the WordPress site again after this.

---

## Troubleshooting

**Import fails with a format error**
The JSON file may have been opened and re-saved by a text editor that changed encoding. Do not open the JSON file. Import it directly from the repository folder.

**GA4 events appear in GTM debug but not in GA4 DebugView**
Wait 30 seconds. GA4 DebugView has a delay. If still missing after 2 minutes, verify the Measurement ID matches exactly (including the GT- prefix, not G-).

**Meta or TikTok tags fire but nothing appears in the ad platform**
The pixel ID may be wrong, or the ad platform is still processing. Allow up to 30 minutes for first-time pixel fires to appear.

**A trigger shows as Not Fired but you performed the action**
Open browser DevTools console and run: `window.dataLayer`. Look for the event object. If it is there, the trigger name in GTM may not match. Check for typos. Event names are case-sensitive.

**You see more tags than expected after import**
If the container already had some tags before import and you selected Merge, both sets exist. Delete any duplicates manually in the Tags view.
