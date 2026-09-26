# Restyle runbook: an unattended, page-by-page run

This is for Claude to follow **without supervision**, for hours, until every page of the site uses the
new design. The user reviews the result afterwards, commit by commit. Read `.claude/HANDOVER.md`
first ("Restyle work" has the rules and the design reference); this file is the procedure.

## Non-negotiables

1. **Content is frozen.** Not one letter, link, title or meta tag may change. Every page must pass
   `python3 _tools/text-check.py <pages> --rev main` before it is committed. `main` is the untouched
   baseline for the whole run.
2. **Work only on the `restyle` branch. One page (or one page group) per commit.** Never commit to
   `main`, never merge, never push anything, never force, never rewrite history. The user
   can then `git revert` or drop any single page.
3. **Never modify `_sources/`.** The D&I guide is restyled only through `_tools/build-di-guide.py`.
4. **Never ask the user anything during the run. They're away.** If a page can't be made to pass,
   restore it (`git restore <page>`), note why in the log, and move on. Never leave a failing page
   committed.
5. Don't delete files and don't touch `cse/books/`, `favicon/`, `_backup/`, or `.gitignore`.

## Setup (once)

```bash
git switch main && git status --short        # must be clean. If not, stop and log it; do nothing else
git switch -c restyle                        # or `git switch restyle` to resume an earlier run
```

- If resuming, read `.claude/restyle-log.md` and continue from the first page that isn't done.
- Start the preview server: `preview_start` with name `site` (port 8080).
- Create `.claude/restyle-log.md` if it's missing, with a heading and the start time.

## Order (smallest risk first)

| # | Commit | Pages | Notes |
| --- | --- | --- | --- |
| 1 | Coming Soon pages | `mathematics/index.html` (linked from Home), `cse/resources.html` (linked from the CS&E guide) | Same template. Make it a centred hero (eyebrow, big title, text, button) in one commit |
| 2 | CS&E on-ramp | `cse/on-ramp.html` | One big table with row spans. Restyle it like the reference's `table.grid` inside a `.card`; scroll sideways on phones. Keep `target="_blank"` on book links |
| 3 | CS&E guide | `cse/index.html` | ~1,100 lines of nested knowledge tree. Map the levels to bands, cards and lists. The largest hand-written page, so take care |
| 4 | D&I guide | `data-intelligence/guide/` (72 generated pages) | Add an **override stylesheet** (`theme/guide-override.css`) that `_tools/build-di-guide.py` links into every page. Map the guide's own CSS tokens (`data-intelligence/guide/assets/css/tokens.css`) to the theme's colours and fonts. Keep the guide's own light/dark toggle working. Rebuild, then text-check all 72 pages |
| 5 | Consistency pass | all restyled pages | Same nav and footer everywhere, same `?v=N` on every theme link, no leftover Google Fonts or old inline `<style>` blocks |

**Out of scope. Don't touch these:** no page on the site links to them.
`data-intelligence/llm-engineering.html`, `mathematics/resources.html`, `data-intelligence/resources.html`.
`data-intelligence/index.html` is only a redirect. Leave it alone.

## The loop for each page

1. **Read the whole page** before changing it. List its structure: nav, hero, sections, tables, lists
   and scripts.
2. **Restyle it**, following the Rules in HANDOVER.md → Restyle work:
   - `<head>`: keep every meta tag, the title and the favicon link. Add the pre-paint theme script
     (copy it from `index.html`). Link `../theme/site.css?v=N`. Remove the page's own `<style>` block
     and its Google Fonts link once nothing needs them.
   - Nav: `.nav` with the brand, links, theme switch and hamburger. **Keep every existing link's href
     and text.** The restyle may not add links, so reuse the page's existing nav and menu links.
   - Put reusable components in `theme/site.css`, not inline. Bump `?v=N` on **every** restyled page
     whenever `theme/` changes.
   - Keep text nodes whole. Restyle through classes and wrappers only.
3. **Text check:** `python3 _tools/text-check.py <page(s)> --rev main` must say OK. If it doesn't,
   fix the markup, not the text. After 3 failed attempts, restore the page and log it.
4. **Visual check** in the preview (`http://localhost:8080/<page>`):
   - Desktop light, desktop dark (use the switch), mobile 375px light and dark.
   - No sideways scroll on the page itself (`document.documentElement.scrollWidth === innerWidth`).
     Tables may scroll inside their own card.
   - The mobile menu opens and closes. The console shows no errors.
   - Justified text: the last line starts at the left, and lines aren't gappy (see HANDOVER).
   - Every internal link on the page still resolves: fetch each `href` and expect 200.
   - Reset the viewport to desktop afterwards.
5. **Regression check:** `python3 _tools/text-check.py $(git ls-files '*.html' | grep -v '^_') --rev main`.
   Every page that isn't in this commit must still pass too, which catches accidental edits.
6. **Update `.claude/HANDOVER.md`**: set the page's row in the Restyle Status table to
   "Done on `restyle` branch (not live)".
7. **Commit** (only the files for this page, plus `theme/` and HANDOVER if they changed):
   ```
   Restyle <page name> to the new design

   <two or three lines: what the layout became, any new theme components>
   text-check: N/N items identical to main.

   Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
   ```
8. **Log it** in `.claude/restyle-log.md`: the page, the commit hash, anything worth the user's
   attention (awkward layouts, judgement calls, things you'd like them to look at). Commit the log with
   the page.

## Finish

Once every page is done, or none of the remaining ones can pass:

1. Run the full regression text check once more and record the result in the log.
2. Write a **summary at the top of `.claude/restyle-log.md`**: pages done, pages skipped and why, and
   the review instructions below. Commit it.
3. Stop the preview server and end with a short message listing the commits.

## For the user: reviewing the run

```bash
git log --oneline main..restyle        # one commit per page
git switch restyle                     # look at it locally (preview server "site", port 8080)
git revert <hash>                      # undo one page you don't like (on the restyle branch)
git switch main && git merge restyle && git push origin main    # publish everything you kept
git switch main && git branch -D restyle                        # or throw the whole run away
```

Nothing is live until that merge and push.
