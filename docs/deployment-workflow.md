# She Said Sail: Website Deployment Workflow
**Version:** 1.0
**Branch:** feature/luxury-conversion-overhaul

---

## BRANCH STRUCTURE

```
main          Production. What visitors see. Only merge here when tested.
staging       Preview/review. Mirror of what production will look like.
dev           Experimental. Early work, untested ideas.
feature/*     Feature branches. All work starts here.
```

---

## BRANCH RULES

| Branch | Who Merges | When |
|---|---|---|
| main | Founder only | After staging review and explicit approval |
| staging | Dev team | After feature branch is complete and reviewed |
| dev | Dev team | Freely, experimental |
| feature/* | Developer who opens it | Merges to staging when ready for review |

**Never push unfinished work directly to main.**
**Never push directly to main without testing on staging first.**

---

## CURRENT FEATURE BRANCH

```
feature/luxury-conversion-overhaul
```

This branch contains:
- `08_PRODUCT_ENGINEERING/website/custom-css/luxury-overhaul.css`
- `08_PRODUCT_ENGINEERING/website/custom-js/luxury-enhancements.js`
- `08_PRODUCT_ENGINEERING/website/html-snippets/social-proof-strip.html`
- `08_PRODUCT_ENGINEERING/website/html-snippets/hero-occasion-pills.html`
- `08_PRODUCT_ENGINEERING/website/html-snippets/email-capture-section.html`
- `08_PRODUCT_ENGINEERING/website/seo/meta-tags.html`
- All `docs/` and `assets/` additions

---

## DEPLOYMENT FLOW

### Step 1: Develop on Feature Branch

```bash
git checkout feature/luxury-conversion-overhaul
# make changes
git add <specific files>
git commit -m "describe the change and why"
git push -u origin feature/luxury-conversion-overhaul
```

### Step 2: Merge to Staging for Review

```bash
git checkout staging
git merge feature/luxury-conversion-overhaul
git push origin staging
```

Review on staging environment. Get founder approval.

### Step 3: Merge to Main (Production)

Only after staging review and approval:

```bash
git checkout main
git merge staging
git push origin main
```

### Step 4: Tag the Release

```bash
git tag -a v2.0 -m "luxury conversion overhaul: social proof, hero, SEO, mobile UX"
git push origin v2.0
```

---

## HOW TO APPLY CHANGES TO WORDPRESS

Since this GitHub repository manages code and documentation but the live site
runs on WordPress/Elementor, applying changes requires these steps:

### CSS Changes

1. Go to WordPress Admin > Appearance > Customize
2. Click "Additional CSS"
3. Copy the entire contents of `custom-css/luxury-overhaul.css`
4. Paste into the Additional CSS field
5. Click "Publish"

Alternative: Elementor > Site Settings > Custom CSS (applies globally)

### JS Changes

1. Install "Insert Headers and Footers" plugin (free, WPBeginner)
2. Go to Settings > Insert Headers and Footers
3. In the "Scripts in Footer" section, wrap the JS in `<script>` tags:
   ```html
   <script defer>
   /* paste contents of luxury-enhancements.js here */
   </script>
   ```
4. Save

Alternative: Add via child theme's `functions.php` as a deferred script.

### HTML Snippets (Social Proof, Email Capture, Occasion Pills)

Each snippet is added via Elementor:
1. Open Elementor editor on homepage
2. Find the correct placement (noted at the top of each HTML file)
3. Add a new "Container" section (full width, no padding)
4. Inside it, add an HTML widget
5. Paste the snippet HTML
6. Update/Publish

### SEO Meta Tags

Preferred: Yoast SEO or RankMath plugin fields.
Alternative: Insert Headers and Footers plugin, "Scripts in Header" section.

---

## ROLLBACK PROCEDURE

If a change causes issues on production:

```bash
git checkout main
git revert HEAD
git push origin main
```

Or revert CSS by removing/emptying the Additional CSS field in WordPress Customizer.

---

## COMMIT MESSAGE CONVENTIONS

Format: `verb: short description of what changed and why`

Good examples:
- `improve hero emotional positioning`
- `add social proof testimonial strip`
- `fix phone and location dead links`
- `reduce hero overlay opacity for photography warmth`
- `add occasion targeting pills to hero`
- `add email capture nurture section`
- `add Open Graph and Schema meta tags`
- `optimize homepage mobile spacing`

Bad examples:
- `update files`
- `fix stuff`
- `WIP`
- `changes`

---

## RECOMMENDED NEXT COMMITS

After this overhaul merges to staging for review:

1. `update experience card copy: Monaco Social and Pink Palm Club descriptions`
2. `change The Packages label to The Experiences in Elementor`
3. `update hero primary CTA destination to /request-to-book/`
4. `wire email capture form to Klaviyo/Mailchimp webhook`
5. `add real guest testimonials as they come in`
6. `implement conditional script loading for homepage performance`
