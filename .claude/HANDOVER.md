# Handover — Towards Intelligence (robotbrainlab.github.io)

Last updated: 2026-10-07.

## What this repo is

A static GitHub Pages user site, live at https://robotbrainlab.github.io. It's a learning roadmap
across three disciplines: Mathematics, CS & Engineering, and Data & Intelligence. There's no build
system for the hand-written pages; every page is plain HTML. GitHub Pages runs Jekyll with default
settings (there's no `_config.yml`), so **folders starting with `_` or `.` are never published**. This is
why sources and tools live in `_sources/`, `_tools/`, `_backup/` and `.claude/`.

The GitHub repo itself is **public**, so everything in `_sources/` can be read on github.com, just
not on the website.

## Publishing

- The remote is `git@github-robotbrainlab:robotbrainlab/robotbrainlab.github.io.git`. It's an SSH host
  alias in `~/.ssh/config` that uses `~/.ssh/id_ed25519_robotbrainlab` (the robotbrainlab account).
  **Never push as the dlakshmizlk account.**
- Pushing to `main` deploys. The live site updates in about 1 minute; check it with `curl`.
- The user usually wants changes committed and pushed. Confirm first for anything that changes how the
  live site looks.

## Rolling back the redesign

Every step of the redesign is its own commit, so any part can be undone with `git revert`. A revert
adds a new commit that undoes an old one, so history is never lost and a rollback can itself be undone.
Every recipe below was tested on a copy of the repo (2026-09-27): each applies cleanly and leaves 0
broken links.

| Commit | Date | What it did |
| --- | --- | --- |
| `d6d73ce` | 2026-09-27 | Phone fixes: D&I guide top bar, justified text on phones, very small screens |
| `c08458d` | 2026-09-27 | CS&E On-Ramp merged into the CS&E guide; `cse/on-ramp.html` removed |
| `422f0a0` | 2026-09-26 | **The redesign** of every page except Home (D&I guide, CS&E guide, on-ramp, Coming Soon pages) |
| `8ba365b`, `b05c60d`, `7901163` | 2026-09-26 | Home page redesign (pilot) and its two justification/cache fixes |
| `98f7de6` | 2026-09-26 | New site icon (Apex) |
| `0d44bc0` | 2026-09-26 | **Last commit before any redesign.** The old dark, gold, serif site |

Pick the smallest undo that does what you want. Always revert **newest first**: list the hashes in
that order, as below.

```bash
# 1. Undo only the phone fixes
git revert --no-edit d6d73ce

# 2. Undo only the On-Ramp merge (brings back cse/on-ramp.html and Home's "The On-Ramp" button)
git revert --no-edit c08458d

# 3. Undo the whole redesign of the sub-pages; Home keeps its new look
git revert --no-edit d6d73ce c08458d 422f0a0

# 4. Full reset of the website to before any redesign (old look everywhere, old icon).
#    Keeps _sources/, the docs and later tool improvements.
git rm -r -q theme
git checkout 0d44bc0 -- index.html favicon cse mathematics data-intelligence _tools/build-di-guide.py
git commit -m "Roll back the website to before the redesign"
```

Then **look before publishing**: preview locally (Browser pane server `site`, port 8080), run
`python3 _tools/link-check.py` if it still exists (recipes 3 and 4 remove it along with the redesign), and
only then run `git push origin main`. Nothing goes live until that push.

Notes:
- To undo a rollback, revert the rollback commit: `git revert <hash of the rollback>`.
- After a rollback that touches the D&I guide (recipes 3 and 4), don't run `_tools/build-di-guide.py`
  until you've decided what you want. It rebuilds the guide from whatever that script and
  `theme/guide-override.css` currently say.
- After publishing, reload each page once on the phone (pull down) so Safari drops cached styles.
- If Git reports a conflict during a revert, stop with `git revert --abort` (nothing changes) and ask
  Claude to resolve it.

## Map

| Path | What it is |
| --- | --- |
| `index.html` | Home page. **Restyled** (live); uses `theme/` |
| `cse/index.html` | CS&E guide: **restyled**. Starts with the **On-Ramp** section (`#on-ramp`, the "from Zero" book table), then the knowledge tree. Sidebar contents + back-to-top live in `theme/site.js` |
| `cse/books/` | Published book PDFs + lab zips (copies of those in `_sources/cs-roadmap/on-ramp/books/`) |
| `mathematics/index.html`, `cse/resources.html` | "Coming Soon" placeholders: **restyled** (linked from Home and the CS&E guide) |
| `mathematics/resources.html`, `data-intelligence/llm-engineering.html`, `data-intelligence/resources.html` | **Orphans.** No page links to them (reachable by URL only). Not part of the restyle |
| `data-intelligence/index.html` | Redirects to `guide/` |
| `data-intelligence/books/python-roadmap.html` | Hand-written, self-contained page (its own CSS, JS and theme switch; no `theme/` link). The Python resource for **both** the D&I guide and the CS&E on-ramp. Not generated — edit it directly |
| `data-intelligence/guide/` | **Generated.** The AI Engineer Roadmap site (72 pages). Never edit by hand. Restyled by `theme/guide-override.css`, which the build script links in |
| `theme/site.css`, `theme/site.js` | Shared styling + behaviour for all hand-written pages (currently `?v=6`) |
| `theme/guide-override.css` | The D&I guide's restyle: remaps its design tokens (curriculum→blue, evidence→purple, Modern track→green) and components. Version is `OVERRIDE_VERSION` in `_tools/build-di-guide.py` (currently `10`) |
| `favicon/` | Site icon: "Apex", a neural network converging into a radiant star, the culmination of AI (gradient tile). Also added to the D&I guide pages by the build script |
| `_sources/ai-roadmap/` | Source of the D&I guide (a separate research repo; **this is its only copy**) |
| `_sources/ai-tools/` | Claude Code guides, skills, and `html-reference/reference.html` (the design reference) |
| `_sources/cs-roadmap/` | CS&E on-ramp books (Markdown + LaTeX) and `end-to-end/` (empty for now) |
| `_tools/build-di-guide.py` | Builds the D&I guide from `_sources/ai-roadmap/` |
| `_tools/text-check.py` | Proves a page's text, links and element ids did not change |
| `_tools/link-check.py` | Checks every internal link and `#anchor` on the site resolves |
| `_backup/data-intelligence/index.html` | The old D&I guide page with the pipeline diagram |

Removed on purpose, so don't recreate them: the Mathematics and D&I on-ramps, the separate `cse/on-ramp.html` page
(merged into the CS&E guide on 2026-09-27, so each discipline has one guide; the site is for the owner only, so no redirect is kept), and the old `redesign/`
effort (a different, "technical" style the user rejected).

---

## Restyle work

**Goal:** restyle every page to look like
`_sources/ai-tools/claude-code/html-reference/reference.html`. That means Apple-like light theme by
default with an iOS dark-mode switch, system fonts, sticky blurred nav, alternating bands, cards,
blue accent and gradient emphasis. The rule is **not a single letter of content may change**.

### Rules

- Change only CSS and the wrapping markup and classes. Every text node, every `href`, the `<title>`,
  the meta description/og tags and the `data-label` tooltips must stay identical.
- Don't add visible text through CSS `content:`. Decorative empty `content: ""` is fine; `attr(data-label)`
  reuses existing text.
- Don't split or merge text nodes. For example, don't wrap one word of a sentence in a new `<span>`.
- Justified text stays. The user wants running text justified (`p, li, td, .prose`). The last line
  must stay left-aligned: never use `text-align-last: center` (the reference does, and the user
  flagged it). Keep justified columns wide enough (about 800px for 21px text) to avoid gappy lines.

To restyle the rest of the site unattended, follow `.claude/RESTYLE-RUNBOOK.md` (a `restyle` branch, one commit
per page, nothing pushed).

### Process for each page

1. Read the page. Map its structure onto the `theme/site.css` components (`.band`/`.band.alt`,
   `.sec-head`, `.card`, `.grid-2`, `.ctas`/`.btn`, `.prose`, …). Add new components to
   `theme/site.css`, not inline.
2. Rewrite the page: keep the `<head>` meta, add the pre-paint theme `<script>` (copy it from
   `index.html`), link `theme/site.css?v=N` with the current version (use `../theme/site.css?v=N` from subfolders), and load
   `theme/site.js` at the end. Nav = brand + links + theme switch + hamburger.
3. Run `python3 _tools/text-check.py <page>`. It must print `OK`. It compares against `HEAD`, so run it
   before committing (or pass `--rev <commit>`).
4. Preview it (`.claude/launch.json` server `site`, port 8080). Check light and dark, desktop and
   mobile (375px, no horizontal scroll), the mobile menu, the reveal animations, and the console for
   errors.
5. Show the user before pushing.

### Status

| Page | Status |
| --- | --- |
| All reachable pages | **Done** (2026-09-26) in one commit: Home, the 2 Coming Soon pages, CS&E on-ramp (since merged into the CS&E guide), CS&E guide, and the D&I guide (72 pages via `theme/guide-override.css`). Checks: 81/81 pages text/link/id-identical to the previous `main`, 0 broken internal links, `_sources/` untouched |
| Orphans (`mathematics/resources`, `data-intelligence/resources`, `data-intelligence/llm-engineering`) | Deliberately left in the old style. Nothing links to them |
---

## Website work

### D&I guide (AI Engineer Roadmap)

- Source: `_sources/ai-roadmap/`. It has its own governance (`AGENTS.md`, `handover.md`,
  `MAINTENANCE.md`); read them before changing roadmap content. The user considers it a separate
  research repo. **Never change its content, templates or generator for site purposes.**
- Rebuild: `python3 _tools/build-di-guide.py` from the repo root. It runs the roadmap's generator
  (1461 validation checks) into a temp directory, adds the "← Towards Intelligence" top-bar link to
  every page and the justify rule to the guide home, renames the guide to **Data & Intelligence** in
  its chrome (top bar, tab title, home heading) and its primary action to "Explore the roadmap",
  then replaces `data-intelligence/guide/`. The rename touches chrome only — the roadmap's own
  running text keeps its name, and `_sources/ai-roadmap/` is never written to. Each replacement is
  checked, so the build stops rather than publishing a page it did not recognise.
- **The Python resource points at this site's own page** (2026-10-07, commit `2042d27`).
  `data-intelligence/books/python-roadmap.html` is a staged path through the language that
  sequences *The Python Tutorial* together with uv, ruff, mypy and pytest. The build script does two
  different things with it, both in `PYTHON_SWAPS` and `NOTE_PAGES`, each checked to match exactly
  once:
  - **Renames the resource and repoints the link** on the 4 pages that tell a reader what to read
    now — step 1, step 6, the curriculum map and the ML testing checklist. Step 6 asked for modules,
    a test runner and isolated environments by tutorial chapter (ch 6, §10.11, ch 12); the roadmap
    assigns those same chapters inside Fundamentals, so they are named by stage instead.
  - **Adds a dated note** to the 7 pages that record earlier research, design or review work. Their
    own text is left exactly as written: renaming the resource there would claim that work examined
    something that did not exist yet. The note sits after the document's `doc-meta` block and uses
    the `.ti-update` style in `theme/guide-override.css`.
  If the roadmap source ever changes that resource's wording, these swaps stop matching and **the
  build exits** rather than publishing a page it did not recognise. Fix the strings, don't delete the
  check.
- Don't run the roadmap's `build_site.py --out` straight into the guide, because the link would be
  lost. Never point `--out` at `data-intelligence/`, because it wipes that directory.
- If `.venv` is missing: `cd _sources/ai-roadmap && python3.14 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt`.

### CS&E on-ramp books

- Book sources are in `_sources/cs-roadmap/on-ramp/books/`. The published PDFs and lab zips are copies in
  `cse/books/`; keep them in sync when a book changes.
- Book links open in a new tab (`target="_blank" rel="noopener"`). Books without a PDF yet carry a
  `<span class="book-status">Coming soon</span>` badge. Topics that are skipped at this level say
  *Not necessary at this level*.
- The on-ramp's **Programming** entry (Engineering Track → Building → Software Engineering) links to
  `data-intelligence/books/python-roadmap.html`, not to a "from Zero" PDF. It is the one on-ramp
  entry served by a page rather than a book, so it crosses into `data-intelligence/`. Changed
  2026-10-07; it used to be a "Programming from Zero — Coming soon" placeholder.

### `_sources/` is the only copy

The originals outside this repo were deleted. Commit **every** file in `_sources/` except `.venv/`
and `.DS_Store`. The books' own `.gitignore` files exclude LaTeX output, so use `git add -f` and check that
the number of files on disk matches the `git ls-files` count. Scan for secrets before committing
(the repo is public).

---

## Gotchas

- Keep `.gitignore` rules anchored to the root (`/assets/`, `/docs/`, `/CLAUDE.md`). An unanchored
  `assets/` once silently dropped the D&I guide's CSS from git.
- GitHub Pages lets browsers cache files for 10 minutes (phones often longer). Pages link the theme as
  `theme/site.css?v=N` / `theme/site.js?v=N`. **Bump `N` on every page whenever `theme/` changes**, or
  visitors keep the old styling.
- **Phones (fixed 2026-09-27).** The D&I guide's own CSS sets prose ragged below 48em and its menu button
  has a -0.9rem margin sized for its old tiny brand. `theme/guide-override.css` re-justifies prose (and the
  study-resource entries and step leads) and re-spaces the phone top bar. Only running text is
  justified: `theme/guide-override.css` keeps headings, step and item names, button labels, pull
  quotes and (on phones) the large lead paragraphs ragged right, because they hold three or four
  words per phone line. `theme/site.css` does the same for the site's own buttons. Audit every page at
  320/360/375/390/414/430px for: top-bar overlaps, cut-off brand, real sideways scroll (`scrollTo` then
  `scrollX`, not `scrollWidth`: the guide's hidden drawers overflow but `overflow-x: clip` stops scrolling),
  overlapping or off-screen buttons, and long paragraphs that aren't justified. Load each page in a
  same-origin iframe of that width; this works even while the Browser pane is hidden.
- Git doesn't store empty folders. Use `.gitkeep` (as in `_sources/cs-roadmap/end-to-end/`).
- Only the 3 orphan pages still load Google Fonts and have their own inline `<style>`.
- Headless screenshots: use Chrome with `--force-prefers-reduced-motion`, or the fade-ins may not have
  finished (blank captures). A hidden Browser pane also pauses scroll observers and painting.
- The Browser pane preview is the user's view too. Reset any viewport emulation when you're done.
