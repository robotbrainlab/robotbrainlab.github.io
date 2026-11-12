# Handover — Towards Intelligence (robotbrainlab.github.io)

Last updated: **2026-11-12**.

## What this repo is

A static GitHub Pages user site, live at https://robotbrainlab.github.io. It's a learning roadmap
across three disciplines: Mathematics, CS & Engineering, and Data & Intelligence. There's no build
system for the hand-written pages; every page is plain HTML.

**`[2026-11-11]` Jekyll is off.** `/.nojekyll` at the repository root tells GitHub Pages to serve
every file exactly as it is. This site never used a Jekyll feature — no `_config.yml`, no
`_layouts`, no front matter, no Liquid in any page — and Jekyll only carried risk: it reads
`{{ … }}` as a template command, and the books are full of that inside ordinary code samples.

**So a leading underscore no longer decides anything, and there are no underscore folders left.**
`_tools` is now `utilities/`, and the books are in `books/`. `_sources` and `_backup` no longer exist at
all: `_sources` was dissolved into the sections it served, and `_backup` went to the Desktop archive
(both 2026-11-11, see the Map). Everything in the repository is served.

The repository is **public**, so every file was already readable on github.com. What changed is
that a file now also has a web address, which search engines collect. **`/robots.txt` decides what
they collect**: the finished books are findable, and markdown, chapters, records, labs, tools,
`books/backlog/`, `books/modern-ai/`, `utilities/` and `backup/` are not.

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
#    Keeps research/, the docs and later tool improvements.
git rm -r -q theme
git checkout 0d44bc0 -- index.html favicon cse mathematics data-intelligence utilities/build-di-guide.py
git commit -m "Roll back the website to before the redesign"
```

Then **look before publishing**: preview locally (Browser pane server `site`, port 8080), run
`python3 utilities/link-check.py` if it still exists (recipes 3 and 4 remove it along with the redesign), and
only then run `git push origin main`. Nothing goes live until that push.

Notes:
- To undo a rollback, revert the rollback commit: `git revert <hash of the rollback>`.
- After a rollback that touches the D&I guide (recipes 3 and 4), don't run `utilities/build-di-guide.py`
  until you've decided what you want. It rebuilds the guide from whatever that script and
  `assets/theme/guide-override.css` currently say.
- After publishing, reload each page once on the phone (pull down) so Safari drops cached styles.
- If Git reports a conflict during a revert, stop with `git revert --abort` (nothing changes) and ask
  Claude to resolve it.

## Map

| Path | What it is |
| --- | --- |
| `index.html` | Home page. **Restyled** (live); uses `assets/theme/` |
| `cse/index.html` | CS&E guide: **restyled**. Starts with the **On-Ramp** section (`#on-ramp`, the "from Zero" book table), then the knowledge tree. Sidebar contents + back-to-top live in `assets/theme/site.js` |
| `books/` | **Every book, one folder per topic, with one shared LaTeX build in `books/latex/`.** `books/README.md` is the index. The website links straight at these PDFs; there is one copy of each |
| `mathematics/index.html`, `cse/resources.html` | "Coming Soon" placeholders: **restyled** (linked from Home and the CS&E guide) |
| `mathematics/resources.html`, `data-and-intelligence/llm-engineering.html`, `data-and-intelligence/resources.html` | **Orphans.** No page links to them (reachable by URL only). `[2026-11-12]` **They are on the site theme now**, so "not part of the restyle" no longer holds: the two Coming Soon pages were rebuilt from `cse/resources.html`, and the resources page keeps its own markup with its components added to `assets/theme/site.css` (`.track-*`, `.resource-table`, `.cell-type`). Google Fonts and the old dark serif styling are gone from all three. Every text item is identical to the published page |
| `data-and-intelligence/index.html` | Redirects to `guide/` |
| `data-and-intelligence/books/python-roadmap.html` | Hand-written, self-contained page (its own CSS, JS and theme switch; no `assets/theme/` link). The Python resource for **both** the D&I guide and the CS&E on-ramp. Not generated — edit it directly. `[2026-11-12]` **It carries the site's chrome now**: the favicon (it had **none**, so its tab showed a blank icon), the gradient brand mark, the home menu, and the shared theme memory — it stored the theme under a third name, `pyroadmap-theme`, and had **no link back into the site at all**. Its own stylesheet was never off-design: same token names, same values as `assets/theme/site.css` |
| `data-and-intelligence/guide/` | **Generated.** The AI Engineer Roadmap site — **75 pages** `[2026-11-12]`, counted; this row said 72. Never edit by hand. Restyled by `assets/theme/guide-override.css`, which the build script links in |
| `assets/theme/site.css`, `assets/theme/site.js` | Shared styling + behaviour for all hand-written pages (currently `?v=8` `[2026-11-12]`). `site.js` writes the theme under **both** names, `ti-theme` and the guide's `air-theme` |
| `assets/theme/guide-override.css` | The D&I guide's restyle: remaps its design tokens (curriculum→blue, evidence→purple, Modern track→green) and components. Version is `OVERRIDE_VERSION` in `utilities/build-di-guide.py` (**currently `18`** `[2026-11-12]`) |
| `assets/` | **Everything the browser downloads**, grouped 2026-11-11: `assets/theme/` and `assets/favicon/`. Kept out of `utilities/` on purpose — `robots.txt` disallows `/utilities/`, and blocking a site's own stylesheet and icon changes how search engines render it |
| `assets/favicon/` | Site icon: "Apex", a neural network converging into a radiant star, the culmination of AI (gradient tile). Also added to the D&I guide pages by the build script |
| `data-and-intelligence/research/` | Source of the D&I guide (a separate research repo; **this is its only copy**) |
| `.claude/` | Claude Code guides, skills, and `html-reference/reference.html` (the design reference) |
| `cse/` | CS&E on-ramp books (Markdown + LaTeX) and `end-to-end/` (empty for now) |
| `utilities/build-di-guide.py` | Builds the D&I guide from `data-and-intelligence/research/` |
| `utilities/text-check.py` | Proves a page's text, links and element ids did not change |
| `utilities/link-check.py` | Checks every internal link and `#anchor` on the site resolves |
| *(moved to the Desktop archive 2026-11-11)* | The old D&I guide page with the pipeline diagram |
| `books/modern-ai-engineering-from-zero/` | ***Modern AI Engineering from Zero*** — a whole separate project living here for safekeeping. **`[2026-11-12]` The folder was `interview-prep/` until today**; the owner renamed it because the book outlived the interview deadline it was named for. See its section below. `[2026-11-12]` This row said "Unpublished (leading `_`)"; **the underscore is gone and so is Jekyll**, so nothing here is unpublished — `/robots.txt` is what keeps it out of search results |
| `books/python/` | ***Python from Zero*** — **started 2026-11-12. `TOC.md` and `CLAUDE.md` only, no manuscript.** 51 chapters built against the Fundamentals stage of `data-and-intelligence/books/python-roadmap.html`, approved by the owner and then reviewed twice and corrected. **It governs itself**: `books/python/CLAUDE.md`. **Nothing is drafted**, and the block is not the contents — decision 8's other half, the rules, is unwritten, and one is live for this book: which of the finished book's gates transfer. **It points at three other books rather than repeating them** — *Linux and Git from Zero*, *APIs to FastAPI*, and the roadmap page, which `[STATED]` nothing happens to |
| `books/future-books/README.md` | **Decisions for *Python* and *Machine Learning and Deep Learning*** — **21 decisions** with their reasons, the rejected alternatives, and the rules still to write. **It is the authority on both books**; neither book's own files restate a decision. `[2026-11-12]` This row said *"Nothing is started. Ten decisions"* — **Python started on 2026-11-12** (see the row above) and the count was out of date. The owner also ruled the books are written **sequentially**, so the file's parallel-writing section no longer describes the plan and is kept only because the ruling is reversible |
| `books/modern-ai/` | ***Modern AI: Research, Science and Engineering*** — **in research, no manuscript.** `[2026-11-12]` It governs itself: `books/modern-ai/CLAUDE.md`, then `docs/ROADMAP.md`, whose **first section, *“What is next — read this first”*, names the next action**: fetch a scope statement for each of the 62 categories the consolidation could not judge, before any area is cut. `[2026-11-12]` This row said that section was a question blocking everything; **the owner has since ruled four times and named that action, so the question is open but blocks nothing**. `docs/HOW-IT-WORKS.md` is the plain map of the process |
| `data-and-intelligence/on-ramp.html` | **The Data & Intelligence on-ramp**, added 2026-11-12. **`[2026-11-12]` Done and live.** The guide's home page carries a **The On-Ramp** button left of its primary action, injected by `utilities/build-di-guide.py`. **That injection runs after `rename()`**, because the section once carried a `button--primary` of its own and `rename()` asserts the home page has exactly one — injecting first made the build exit. The button uses the roadmap's bare `button` class, so it needs no CSS. Three books in reading order — *Python from Zero* and *Machine Learning and Deep Learning* (both Coming soon) and *Modern AI Engineering from Zero*, which is live and carries its own last-updated date. Hand-written, uses `assets/theme/`, width capped at 800px to match the guide's own column. `[2026-11-12]` **It is three `.step-card` blocks now, not a table** — it copied the CS&E on-ramp's three-column table, and with two columns the step number sat alone in an 18% gutter and the card ran into the footer. **Reached from the guide's home page** |
| `books/rag-from-zero/` | *RAG from Zero: A Practical Guide*, added 2026-11-12. **PDF only**, no Markdown source here, and **not linked from any page** |

Removed on purpose, so don't recreate them: the Mathematics on-ramp (commit `a3c706f`,
2026-09-26, which removed `mathematics/on-ramp.html` and its home-page link), the separate
`cse/on-ramp.html` page
(merged into the CS&E guide on 2026-09-27, so each discipline has one guide; the site is for the owner only, so no redirect is kept), and the old `redesign/`
effort (a different, "technical" style the user rejected).

---

## Restyle work

**Goal:** restyle every page to look like
`.claude/design-reference.html`. That means Apple-like light theme by
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

1. Read the page. Map its structure onto the `assets/theme/site.css` components (`.band`/`.band.alt`,
   `.sec-head`, `.card`, `.grid-2`, `.ctas`/`.btn`, `.prose`, …). Add new components to
   `assets/theme/site.css`, not inline.
2. Rewrite the page: keep the `<head>` meta, add the pre-paint theme `<script>` (copy it from
   `index.html`), link `assets/theme/site.css?v=N` with the current version (use `../assets/theme/site.css?v=N` from subfolders), and load
   `assets/theme/site.js` at the end. Nav = brand + links + theme switch + hamburger.
3. Run `python3 utilities/text-check.py <page>`. It must print `OK`. It compares against `HEAD`, so run it
   before committing (or pass `--rev <commit>`).
4. Preview it (`.claude/launch.json` server `site`, port 8080). Check light and dark, desktop and
   mobile (375px, no horizontal scroll), the mobile menu, the reveal animations, and the console for
   errors.
5. Show the user before pushing.

### Status

| Page | Status |
| --- | --- |
| All reachable pages | **Done** (2026-09-26) in one commit: Home, the 2 Coming Soon pages, CS&E on-ramp (since merged into the CS&E guide), CS&E guide, and the D&I guide (**75 pages** `[2026-11-12]`; this said 72, via `assets/theme/guide-override.css`). Checks: 81/81 pages text/link/id-identical to the previous `main`, 0 broken internal links, *(dissolved 2026-11-11 — see below)* untouched |
| Orphans (`mathematics/resources`, `data-and-intelligence/resources`, `data-and-intelligence/llm-engineering`) | Deliberately left in the old style. Nothing links to them |
---

## Website work

### D&I guide (AI Engineer Roadmap)

- Source: `data-and-intelligence/research/`. It has its own governance (`AGENTS.md`, `handover.md`,
  `MAINTENANCE.md`); read them before changing roadmap content. The user considers it a separate
  research repo. **Never change its content, templates or generator for site purposes.**
- Rebuild: `python3 utilities/build-di-guide.py` from the repo root. It runs the roadmap's generator
  (1461 validation checks) into a temp directory, adds the "← Towards Intelligence" top-bar link to
  every page and the justify rule to the guide home, renames the guide to **Data & Intelligence** in
  its chrome (top bar, tab title, home heading) and its primary action to "Explore the roadmap",
  then replaces `data-and-intelligence/guide/`. The rename touches chrome only — the roadmap's own
  running text keeps its name, and `data-and-intelligence/research/` is never written to. Each replacement is
  checked, so the build stops rather than publishing a page it did not recognise.
- **The Python resource points at this site's own page** (2026-10-07, commit `2042d27`).
  `data-and-intelligence/books/python-roadmap.html` is a staged path through the language that
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
    the `.ti-update` style in `assets/theme/guide-override.css`.
  If the roadmap source ever changes that resource's wording, these swaps stop matching and **the
  build exits** rather than publishing a page it did not recognise. Fix the strings, don't delete the
  check.
- Don't run the roadmap's `build_site.py --out` straight into the guide, because the link would be
  lost. Never point `--out` at `data-and-intelligence/`, because it wipes that directory.
- If `.venv` is missing: `cd data-and-intelligence/research && python3.14 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt`.

### CS&E on-ramp books

- Book sources are in `books/`. The published PDFs and lab zips are copies in
  `books/<slug>/`, and the website links straight at them. **`[2026-11-11]` There is one copy now.**
  `cse/books/` held byte-identical duplicates with a rule to keep them in sync by hand; the
  duplicates are deleted and the rule is gone.
- Book links open in a new tab (`target="_blank" rel="noopener"`). Books without a PDF yet carry a
  `<span class="book-status">Coming soon</span>` badge. Topics that are skipped at this level say
  *Not necessary at this level*.
- The on-ramp's **Programming** entry (Software Engineering Track → Development → Application Engineering) links to
  `data-and-intelligence/books/python-roadmap.html`, not to a "from Zero" PDF. It is the one on-ramp
  entry served by a page rather than a book, so it crosses into `data-and-intelligence/`. Changed
  2026-10-07; it used to be a "Programming from Zero — Coming soon" placeholder. The link reads
  **Programming Language From Zero: Python** (2026-10-29) — the topic is the language, Python is the
  instance — while the page's own title stays *Python Roadmap*, because the D&I guide links to it too.
- **Application Engineering's order is deliberate** (2026-10-29): Linux and Git → Programming → APIs.
  Tools first, then the language, then how a program offers its abilities to others.
- **The Complete Software Engineering Guide belongs to no category and no topic.** It is the last row
  of the Software Engineering Track, a single `colspan="3"` cell running the full width of the table
  (2026-10-29). The reason: every other book answers one topic, while the guide is a traversal — one
  project carried from idea to production, read *after* the pieces. Filing a traversal under a topic
  made it read like a fourth sibling of Linux and Git.
  Two earlier attempts failed and are worth not repeating. A labelled row *Across Development* read as
  a third topic under Development; widening that row to `colspan="2"` still left it inside the
  Development block, because the category cell beside it says what owns it. Only leaving the category
  column altogether reads as *across*. Done with existing classes, so no `assets/theme/` change and no
  cache-version bump.
- **Web Applications from Zero is no longer published on its own.** Its six chapters are now the pre-book
  *How Web Applications Work* inside the Complete Software Engineering Guide, sitting after the map
  chapter and before Part I (2026-10-08). `cse/books/web-applications/` was deleted (and `cse/books/` itself on 2026-11-11);
  `books/web-applications/markdown/` stays, because it is the pre-book's source.
  - The chapters are **unnumbered** (`numbered=false` in `convert.sh`). This is load-bearing: Part IV keeps
    chapters 1–44, so every "see Chapter 17" in the guide's prose stays true. Do not make them numbered.
  - The part page uses `\prebookpart` in `LaTeX-Book/preamble.tex` — a copy of `\lifecyclepart` that does
    **not** advance the part counter, so Product Discovery is still Part I and the preface's "four parts"
    stays true. `\phasestrip{0}` highlights none of the four phases, which is correct before the loop starts.
- **⚠ The Complete Software Engineering Guide cannot be rebuilt from Markdown in this repo.** Its
  `utilities/convert.sh` reads a Markdown library (`1-Product-Discovery/`, `2-Project-Planning/`,
  `3-Writing-the-Code/`, `4-Building-Real-Applications/…`) that is **not in this repository and not anywhere on
  this machine** — searched 2026-10-08. Only the generated `LaTeX-Book/chapters/*.tex` survive, and they are
  committed. So `make` fails at the convert step, but `make pdf` works:
  ```
  cd books/complete-software-engineering-guide
  latexmk -xelatex -interaction=nonstopmode -halt-on-error book.tex
  ```
  Treat `chapters/*.tex` as source until that Markdown is found or rewritten. **Never run `make clean`** —
  it deletes `chapters/`, and nothing can regenerate it.
- **APIs to FastAPI is in both places, on purpose** (2026-10-29). It is an on-ramp entry again, under
  Application Engineering after Programming, *and* it stays in the Python Roadmap at Phase 1.5, where it
  replaced the MDN HTTP reading item on 2026-10-08. The PDF is at `books/apis-to-fastapi/`. This
  reverses the 2026-10-08 decision to reach it only through Programming → Python Roadmap → 1.5; the
  owner wanted it visible as a topic in its own right. Keep both entries in step.
- **Learning method, agreed 2026-10-08.** The roadmap is kept clean and supporting concepts are learned as
  they come up. A new "from Zero" guide is written only when (a) no good from-zero resource exists at this
  level, and (b) the wall has been hit twice. That is how `APIs to FastAPI` came to exist. Don't try to
  close every prerequisite in advance — the regress has no bottom.
- **The one known gap in Python Fundamentals is SQL.** Phase 1.5 opens with five database items, and
  *Use the Index, Luke!* ch. 1–5 assumes you can already write a join. The failure is silent — a missing
  index doesn't error, it gets slow later — so `databases/TOC.md` is the next book worth writing.

### The book sources here are the only copy

The originals outside this repo were deleted. Commit **every** file under `books/` except `.venv/`
and `.DS_Store`. The books' own `.gitignore` files exclude LaTeX output, so use `git add -f` and check that
the number of files on disk matches the `git ls-files` count. Scan for secrets before committing
(the repo is public).

---

## *Modern AI Engineering from Zero* (`books/modern-ai-engineering-from-zero/`)

*Added 2026-10-23.*

**What it is.** A book, *Modern AI Engineering from Zero*. **It is FINISHED** — 2026-10-31, all
57 chapters and 4 appendices, 1,413 printed pages. `[2026-11-12]` This paragraph said Part I was
finished and the rest planned. It was written while the book was being drafted, and it was out of
date in the only sentence that mattered.

**It was written to prepare the owner for AI/LLM application-engineer interviews before
31 December 2026.** `[2026-11-12]` **That is no longer all it is**: it is step 3 of the Data &
Intelligence on-ramp and is linked from the guide, so the note below about removing it when the
job search ends no longer describes the plan.

**Why it is in this repository.** It started as its own local repository. Its GitHub remote
was configured but the repository was never created, so nothing was ever pushed and the only
copy was on one machine. Rather than lose it, the owner chose to keep it here, where a remote
already exists. **It is temporary** and will be removed once the job search ends.

**`books/modern-ai-engineering-from-zero/` is the only copy.** The old folder at `~/LearningLab/towards-intelligence/modern-ai-interview-prep`
was deleted on 2026-10-23, after checking that all 65 of its tracked files were byte-identical
here and all 31 of its commits reachable. Do not go looking for it. The book is also published
on the public repository, which the owner decided deliberately: the content is general
technical material, and the repository was already public on the same terms.

**`[2026-11-12]` It IS on the website now.** The Data & Intelligence on-ramp links its PDF, and
`/robots.txt` already allowed `/books/*/*.pdf`. **This paragraph said the opposite** — that it
must never appear on the live site, guaranteed by a leading underscore and Jekyll. **Both are
gone**: the underscore went on 2026-11-11 and Jekyll is off. It is not part of the restyle. `[2026-11-12]` The link check reports **85 pages**; this said 81.

**Its history came with it.** The move was a subtree-style merge, not a copy, so all 31 of
the book's own commits are in this repository's history. They are reachable but their paths
are the old ones (`markdown/…`, not `books/modern-ai-engineering-from-zero/markdown/…`), so `git log --follow` will not trace
a file across the move. To read a book file's history before the move:

```bash
git log --oneline e8aadd3 -- markdown/05-where-the-work-goes.md
```

**How to work on it.** The book governs itself and does not follow this file. Read, in order:

| Read | For |
| --- | --- |
| `books/modern-ai-engineering-from-zero/docs/HANDOVER.md` | Every decision with its reason, the current state, what is blocked |
| `books/modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` | Scope, the maths boundary, style, the five-step writing loop, the gates |
| `books/modern-ai-engineering-from-zero/TOC.md` | All 57 chapters and 4 appendices, and who owns which concept |
| `books/modern-ai-engineering-from-zero/LEDGER-TAUGHT.md` | What each finished chapter taught, and what a later chapter must not re-introduce |
| `books/modern-ai-engineering-from-zero/LEDGER-DEFECTS.md` | 20 entries of what the gates cannot catch. Read before writing a chapter |

Two rules worth knowing before you open any of them: **one chapter at a time** (never a part
at a time), and **`bash books/modern-ai-engineering-from-zero/tools/check-all.sh` must end `ALL GATES PASS`** before a chapter
is closed. Build the PDF with `bash books/modern-ai-engineering-from-zero/tools/build-probe.sh`, which reports a build's exit
status beside its warning counts and refuses to report the counts at all when the build
failed — read `LEDGER-DEFECTS.md` entry 17 for why that exists.

**Cleaning it up later.** Removing it is one commit, and nothing on the site depends on it:

```bash
git rm -r -q books/modern-ai-engineering-from-zero
git commit -m "Remove Modern AI Engineering from Zero; the job search is over"
```

That leaves the book's 31 commits in the history, so it stays recoverable
(`git checkout <commit> -- markdown/`). To get it out of the history as well, the move
commit `0343354` is the merge to drop — but that is a history rewrite on a published
branch, so do it only if there is a reason, and never without asking.

---

## `[2026-11-12]` One site, one set of chrome

The guide and the site had drifted apart. Five things were put right, after the owner went through
the pages himself and named each one. The rule held throughout: **not a letter of content changed**,
and `utilities/text-check.py` proves it page by page.

- **One theme memory.** The site stored the chosen theme as `ti-theme`, the guide as `air-theme`,
  the Python roadmap as `pyroadmap-theme`. **Three memories, so the theme changed as you crossed
  between them.** Now `site.js` writes the first two, the roadmap page writes the first two, and
  `utilities/build-di-guide.py` puts a bridge in every guide page that applies an arriving choice
  before first paint.
- **The guide's theme control is the site's switch**, markup and behaviour, put in place of the
  roadmap's three-state button by the build script. **The word *System* is gone** from the 75 pages
  with it, and so is that state: a theme is light or dark everywhere now. That is the **only** text
  the rebuild removes, and `text-check` shows it as one line per page.
- **No pills in the top bar.** The guide's `.tool-button` is plain text at the site's link size.
  Nothing in the site's own bar is a filled or outlined button, and now nothing in the guide's is.
- **A home menu replaces the back arrow.** One home button opens *Home page* (purple, ruled off),
  then Mathematics, CS & Engineering and Data & Intelligence. The site's bar carries those three as
  plain links; the guide's bar already holds its own sections and cannot fit three more on a phone.
  **It is on every page now** `[2026-11-12]`: the 75 guide pages and
  `data-and-intelligence/books/python-roadmap.html` carry their own copy, written by the build
  script and by the page itself; the eight hand-written pages share one in `assets/theme/site.css`
  and `assets/theme/site.js` (`?v=10`). **The three discipline links are gone from the bar**: they
  said the same thing the menu says, on every page, right beside it. A bar is now the brand and its
  tile on the left, the home button and the switch on the right. Each page's own section links stay
  — the Python roadmap's six, the guide's *Learn / Evidence / About* — because those are that page's
  navigation, not a copy of the menu, and the mobile menus are untouched. Each page marks its own
  row, and *Home page* is purple (`--root`) above a rule.
- **The gradient tile is on every page.** The mark beside *Data & Intelligence* in the guide now sits
  beside *Towards Intelligence* on all eight hand-written pages and beside *Python Roadmap*. It is
  `--grad` in a 16px rounded square, `aria-hidden`.

**Phones, measured at 320, 375 and 430px:** no page scrolls sideways. The CS&E on-ramp table held
`min-width: 720px` inside a 351px card, so **the card scrolled** while the page did not; below 640px
that table is laid out as blocks and the three column headings are hidden (they stay in the markup).
**The Python roadmap's tables stack too**, and this is how: `table.grid` held 620px (480px when
tight) inside a card about 340px wide. Each cell now carries its own column heading in a
`data-label` attribute, copied from the table's own `<th>`, and the phone layout prints it above
the value with `content: attr(data-label)`. **No new words**: 419 cells were labelled from headings
that are already in the page, which is the one use of CSS `content:` the restyle rules allow.
What still scrolls inside its box, and must: the guide's code and diagram blocks.

**The home menu's rows go to four different pages.** Mathematics pointed at `index.html#mathematics`,
copying the site's own nav, so two of the four rows landed on the home page and only the scroll
position differed — which reads as a broken link. It points at `mathematics/index.html` now.

---

## Gotchas

- Keep `.gitignore` rules anchored to the root (`/assets/`, `/docs/`, `/CLAUDE.md`). An unanchored
  `assets/` once silently dropped the D&I guide's CSS from git.
- GitHub Pages lets browsers cache files for 10 minutes (phones often longer). Pages link the theme as
  `assets/theme/site.css?v=N` / `assets/theme/site.js?v=N`. **Bump `N` on every page whenever `assets/theme/` changes**, or
  visitors keep the old styling.
- **Phones (fixed 2026-09-27).** The D&I guide's own CSS sets prose ragged below 48em and its menu button
  has a -0.9rem margin sized for its old tiny brand. `assets/theme/guide-override.css` re-justifies prose (and the
  study-resource entries and step leads) and re-spaces the phone top bar. Only running text is
  justified: `assets/theme/guide-override.css` keeps headings, step and item names, button labels, pull
  quotes and (on phones) the large lead paragraphs ragged right, because they hold three or four
  words per phone line. `assets/theme/site.css` does the same for the site's own buttons. Audit every page at
  320/360/375/390/414/430px for: top-bar overlaps, cut-off brand, real sideways scroll (`scrollTo` then
  `scrollX`, not `scrollWidth`: the guide's hidden drawers overflow but `overflow-x: clip` stops scrolling),
  overlapping or off-screen buttons, and long paragraphs that aren't justified. Load each page in a
  same-origin iframe of that width; this works even while the Browser pane is hidden.
- **`[2026-11-12]` Protecting the generated guide — **fix (1) is DONE**; (2) is still optional.**
  Every page the build script writes now opens with a comment naming the script and saying a hand
  edit is erased by the next build, and the script stops rather than writing the comment into a
  page that does not start with a doctype. The drift check below is still unbuilt, and the advice
  stands: leave it until the problem bites. The original note follows.
- **`[2026-11-12]` Protecting the generated guide — the problem it solved.** `data-and-intelligence/guide/` is **75 pages** produced by
  `utilities/build-di-guide.py` from `data-and-intelligence/research/`. **A hand edit to any of
  them is erased by the next build, silently** — and **not one of the 75 says it is generated.**
  Checked 2026-11-12: zero carry a "do not edit" marker, so the only protection is the line in the
  Map above, which works only if somebody read it. Two fixes, in order of cost:
  **(1)** have the build script write an HTML comment at the top of every page it generates —
  *"Made by `utilities/build-di-guide.py`. Hand edits are erased on the next build."* About five
  lines, and it closes most of the risk because anyone who opens the file sees it first.
  **(2)** a drift check beside `link-check.py`: rebuild into a temporary directory and compare with
  what is published. A difference means somebody hand-edited, or the source changed and nobody
  rebuilt. Slower, so it runs before publishing. **Do (1) now and leave (2) until it has bitten
  once** — that was the recommendation and the owner has not ruled on it.
- **`[2026-11-12]` **Fixed on both on-ramps.** A live book title carries a thin blue underline on the D&I step cards (`.step-card .book-title a`) and in the CS&E table (`.onramp-table .book-title a`), so it no longer reads as a *Coming soon* entry. The note below is kept because it records what the defect was.
- **`[2026-11-12]` On both on-ramps, a book you can open looks exactly like one that does not
  exist yet.** Measured: a live `.book-title a` and a Coming-soon `.book-title` both render
  `rgb(245,245,247)` with no underline, so the only signal is the missing badge. **It is the site's
  existing behaviour, not something the D&I on-ramp introduced** — the CS&E table has done this
  since the restyle, with 5 live links and 5 Coming soon in one colour. Left alone because changing
  it changes the CS&E page too, which is a live visual change. The owner has not ruled on it.
- Git doesn't store empty folders. Use `.gitkeep` (as in `cse/end-to-end/`).
- Only the 3 orphan pages still load Google Fonts and have their own inline `<style>`.
- Headless screenshots: use Chrome with `--force-prefers-reduced-motion`, or the fade-ins may not have
  finished (blank captures). A hidden Browser pane also pauses scroll observers and painting.
- The Browser pane preview is the user's view too. Reset any viewport emulation when you're done.
