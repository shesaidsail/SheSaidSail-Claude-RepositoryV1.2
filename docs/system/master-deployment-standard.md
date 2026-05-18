# She Said Sail: Master Deployment Standard
Version: 1.0

This is the authoritative git and deployment workflow for the She Said Sail website. Every developer and AI agent working on this codebase follows these rules. No exceptions without explicit written approval from Will.

---

## 1. BRANCH STRUCTURE

| Branch | Purpose | Who Merges |
|--------|---------|------------|
| `main` | Production. What live visitors see. | Founder (Will) only, after staging review |
| `staging` | Preview and review. Mirror of production. | Dev team, after feature is complete and QA-signed |
| `dev` | Experimental. Early work and untested ideas. | Dev team, freely |
| `feature/*` | All active work starts here. | Merge to staging when QA is complete |

**Current active feature branch:** `feature/luxury-conversion-overhaul`

All work on the luxury conversion overhaul project is committed to `feature/luxury-conversion-overhaul` until the full project is staging-approved and ready for production release.

---

## 2. BRANCH RULES

**Main branch protection:**

- Never push unfinished work directly to `main`
- Never push directly to `main` without staging review and written approval
- Never force push to `main` under any circumstances
- Never skip pre-commit hooks without explicit written permission from Will

**Feature branch naming:**

Feature branches must be named descriptively. Two acceptable formats:

- `feature/[descriptive-name]`: for work that spans multiple pages or is conceptually unified
- `feature/[page-name]-[change-type]`: for work scoped to a single page

**Examples of correct naming:**

- `feature/luxury-conversion-overhaul`
- `feature/homepage-hero-update`
- `feature/request-to-book-form-backend`
- `feature/experiences-page-redesign`

**Examples of incorrect naming:**

- `feature/update`
- `feature/fixes`
- `feature/new`
- `feature/will-changes`
- `test-branch`

---

## 3. COMMIT MESSAGE STANDARD

**Format:**

```
[verb]: [short description of what changed and why]
```

**Rules:**

- Always present tense, imperative mood
- Maximum 72 characters for the summary line
- No em dashes anywhere in commit messages
- No trailing punctuation on the summary line
- If the commit requires more context, add a blank line after the summary and write a body paragraph

**Accepted verbs:**

`add` / `update` / `fix` / `improve` / `remove` / `refactor` / `create` / `merge`

**Rejected verbs and patterns:**

`changed` / `updated` / `fixed` / `various changes` / `WIP` / `temp` / `test` / `misc` / `stuff` / `tweaks`

**Good commit messages:**

```
add social proof strip to homepage between experiences and value prop
fix phone link href in footer to use tel: protocol
update Monaco Social card description for brand voice compliance
improve hero overlay opacity to 0.32 for photography warmth
create master design system documentation
remove unused OWL Carousel plugin dependency
refactor request to book form hidden fields for UTM capture
add GTM dataLayer event for form_start on request to book
```

**Bad commit messages:**

```
update files
various changes
fix stuff
temp fix for homepage
WIP
homepage changes
updated the copy
```

---

## 4. COMMIT GROUPING RULES

Each commit should contain one logical change. The goal is a commit history that can be read like a project log and reversed cleanly if needed.

**Guidelines by change type:**

| What is in the commit | Rule |
|-----------------------|------|
| CSS and HTML for the same feature | Acceptable together in one commit |
| CSS and backend specifications | Separate commits always |
| Multiple unrelated HTML snippets | Separate commits, or group by page if same session |
| Documentation files | Separate from code changes |
| QA checklists | Separate from implementation files |
| Analytics event code | Group with the HTML/JS it relates to |
| SEO metadata changes | Can group multiple pages if it is the same type of change |
| Copy-only changes | Separate from structural or code changes |

**When in doubt:** make a smaller commit. A history of small, well-described commits is far easier to work with than large, mixed commits.

---

## 5. STAGING WORKFLOW

When a feature branch is ready for review, follow these steps in order. Do not skip steps.

**Step 1:** Run the master QA checklist locally against your development environment.

**Step 2:** Confirm all changes are committed to the feature branch. Run `git status` and verify there are no uncommitted changes.

**Step 3:** Push the feature branch to origin.
```
git push origin feature/[branch-name]
```

**Step 4:** Merge the feature branch to `staging`.
```
git checkout staging
git merge feature/[branch-name]
git push origin staging
```

**Step 5:** Apply WordPress-side changes on the staging environment. This includes: CSS additions to Additional CSS, JS additions to Insert Headers and Footers, any Elementor HTML widget additions.

**Step 6:** Run the full QA checklist on the live staging URL. Check every item. Do not mark items as passing without verifying them.

**Step 7:** Take screenshots at desktop (1440px width) and mobile (375px width) for every page that was changed.

**Step 8:** Send the screenshots and the completed QA checklist to Will for review.

**Step 9:** Wait for explicit written approval from Will before proceeding. A verbal acknowledgment is not approval. Approval must be written (Slack, email, or equivalent).

---

## 6. PRODUCTION DEPLOYMENT

After receiving written staging approval from Will:

**Step 1:** Merge `staging` to `main`.
```
git checkout main
git merge staging
git push origin main
```

**Step 2:** Apply the same WordPress changes on the production environment that were applied to staging. Do not assume they carried over. Apply them manually and verify each one.

**Step 3:** Run the abbreviated production QA:
- Visual appearance matches staging screenshots
- Form submission works and creates an Airtable record
- Analytics events are firing in GTM Preview

**Step 4:** Tag the release with a semantic version and short description.
```
git tag -a v[major.minor] -m "[brief description of what this release contains]"
```

**Step 5:** Push the tag.
```
git push origin v[tag-name]
```

**Version numbering:**

- Major version (v2.0, v3.0): significant redesign or structural overhaul
- Minor version (v1.1, v1.2): feature additions, new pages, significant copy or design updates
- Patch (v1.0.1): bug fixes, minor copy corrections, small CSS adjustments

---

## 7. ROLLBACK PROCESS

If something breaks in production, the rollback path depends on what was changed.

**Immediate rollback for CSS or JS changes (under 2 minutes):**

- CSS: remove the addition from WordPress Additional CSS field and save
- JS: remove the addition from Insert Headers and Footers plugin and save
- These do not require any git commands

**Git rollback if `main` was incorrectly updated:**

```
git revert HEAD
git push origin main
```

This creates a new commit that undoes the last commit. It does not rewrite history. It is safe on a shared branch.

Never use `git reset --hard` on `main` or `staging`. This rewrites history and will break any collaborators' local copies.

**WordPress content rollback:**

- Elementor widget: delete the HTML widget from the Elementor canvas and save
- Yoast SEO meta: clear the affected field and save
- Theme customizer settings: use the WordPress revision history if available

**After any rollback:**

Document what happened, what was rolled back, and why. Create a note in the audit log for the affected page.

---

## 8. QA BEFORE MERGE

Every feature branch must pass QA before merging to `staging`. No exceptions.

**QA requirements:**

- All DEPLOYMENT_PACK/09_QA/ checklists relevant to the changed pages must be completed and signed off
- No JavaScript console errors on any changed page at 375px and 1280px viewport
- No em dashes in any changed file

**To check for em dashes in changed files:**

```
git diff staging --name-only | xargs grep -l $'\xe2\x80\x94'
```

If any files are returned, locate and fix every instance before proceeding.

**JS syntax check (for any changed JS files):**

```
node --check [filename.js]
```

**Visual review:**

Test every changed page at:
- 375px width (iPhone SE, smallest common viewport)
- 1280px width (standard laptop)
- 1440px width (large desktop)

---

## 9. PRODUCTION RELEASE CHECKLIST

Before tagging any production release, every item below must be confirmed.

- [ ] All QA checklists for changed pages are signed off
- [ ] Will has reviewed screenshots on staging and given written approval
- [ ] Form submission has been tested end-to-end: form submit creates an Airtable record
- [ ] Analytics events verified in GTM Preview mode: page view, CTA click, form start, form submit
- [ ] PageSpeed score checked and logged (document the score in the release tag message)
- [ ] No JavaScript console errors on any changed page
- [ ] No em dashes in source files (run the grep check above)
- [ ] Rollback plan confirmed: who does it, how fast can it happen

Do not tag a release until every checkbox is checked. A partial release checklist is not a release. It is a staging deployment that has not yet been approved for production.

---

## 10. DEPLOYMENT APPROVAL AUTHORITY

| Action | Who Can Approve |
|--------|----------------|
| Merge feature branch to staging | Developer |
| Merge staging to main | Founder (Will) only |
| Add a new WordPress plugin | Founder approval required |
| Change brand colors in the design system | Founder approval required |
| Change pricing (any mention of starting price) | Founder approval required |
| Change page URLs or slugs | Founder approval required |
| Add new pages to the site | Founder approval required |
| Remove existing pages | Founder approval required |
| Change the form destination or webhook URL | Founder approval required |
| Change Airtable base structure | Founder approval required |

If you are uncertain whether an action requires approval, ask before proceeding. The cost of asking is a short delay. The cost of proceeding without approval when approval was required is a broken production site and a damaged trust relationship.
