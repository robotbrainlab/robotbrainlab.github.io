# Handover — Towards Intelligence (robotbrainlab.github.io)

Last updated: 2026-09-26.

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

## Map

| Path | What it is |
| --- | --- |
| `index.html` | Home page. **Restyled** (live); uses `theme/` |
| `cse/index.html` | CS&E guide (knowledge tree), old dark style |
| `cse/on-ramp.html` | CS&E on-ramp, a table of "from Zero" books, old dark style |
| `cse/books/` | Published book PDFs + lab zips (copies of those in `_sources/cs-roadmap/on-ramp/books/`) |
| `cse/resources.html`, `mathematics/*.html`, `data-intelligence/llm-engineering.html` | "Coming Soon" placeholders, old style |
| `data-intelligence/resources.html` | D&I resources (7 tables), old style |
| `data-intelligence/index.html` | Redirects to `guide/` |
| `data-intelligence/guide/` | **Generated.** The AI Engineer Roadmap site (72 pages). Never edit by hand |
| `theme/site.css`, `theme/site.js` | Shared styling + behaviour for restyled pages |
| `favicon/` | Site icon |
| `_sources/ai-roadmap/` | Source of the D&I guide (a separate research repo; **this is its only copy**) |
| `_sources/ai-tools/` | Claude Code guides, skills, and `html-reference/reference.html` (the design reference) |
| `_sources/cs-roadmap/` | CS&E on-ramp books (Markdown + LaTeX) and `end-to-end/` (empty for now) |
| `_tools/build-di-guide.py` | Builds the D&I guide from `_sources/ai-roadmap/` |
| `_tools/text-check.py` | Proves a page's text and links did not change |
| `_backup/data-intelligence/index.html` | The old D&I guide page with the pipeline diagram |

Removed on purpose, so don't recreate them: the Mathematics and D&I on-ramps, and the old `redesign/`
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
- Justified text stays. The user wants running text justified (`p, li, td, .prose`).

### Process for each page

1. Read the page. Map its structure onto the `theme/site.css` components (`.band`/`.band.alt`,
   `.sec-head`, `.card`, `.grid-2`, `.ctas`/`.btn`, `.prose`, …). Add new components to
   `theme/site.css`, not inline.
2. Rewrite the page: keep the `<head>` meta, add the pre-paint theme `<script>` (copy it from
   `index.html`), link `theme/site.css` (use `../theme/site.css` from subfolders), and load
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
| `index.html` | **Done, live** (2026-09-26): text-check OK, checked light/dark/mobile |
| `cse/index.html` | To do. The large nested knowledge tree maps to cards |
| `cse/on-ramp.html` | To do. One table with row spans; restyle it like the reference's `table.grid` inside a card |
| `data-intelligence/resources.html` | To do. 7 tables, same treatment |
| 5 Coming Soon pages | To do. They share one template |
| `data-intelligence/guide/` (72 pages) | To do last. It has its own ~2,300-line CSS. **Don't touch `_sources/ai-roadmap/`**; add an override stylesheet from `_tools/build-di-guide.py`, the same way that script already adds the home link and the justify rule |

---

## Website work

### D&I guide (AI Engineer Roadmap)

- Source: `_sources/ai-roadmap/`. It has its own governance (`AGENTS.md`, `handover.md`,
  `MAINTENANCE.md`); read them before changing roadmap content. The user considers it a separate
  research repo. **Never change its content, templates or generator for site purposes.**
- Rebuild: `python3 _tools/build-di-guide.py` from the repo root. It runs the roadmap's generator
  (1461 validation checks) into a temp directory, adds the "← Towards Intelligence" top-bar link to
  every page and the justify rule to the guide home, then replaces `data-intelligence/guide/`.
- Don't run the roadmap's `build_site.py --out` straight into the guide, because the link would be
  lost. Never point `--out` at `data-intelligence/`, because it wipes that directory.
- If `.venv` is missing: `cd _sources/ai-roadmap && python3.14 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt`.

### CS&E on-ramp books

- Book sources are in `_sources/cs-roadmap/on-ramp/books/`. The published PDFs and lab zips are copies in
  `cse/books/`; keep them in sync when a book changes.
- Book links open in a new tab (`target="_blank" rel="noopener"`). Books without a PDF yet carry a
  `<span class="book-status">Coming soon</span>` badge. Topics that are skipped at this level say
  *Not necessary at this level*.

### `_sources/` is the only copy

The originals outside this repo were deleted. Commit **every** file in `_sources/` except `.venv/`
and `.DS_Store`. The books' own `.gitignore` files exclude LaTeX output, so use `git add -f` and check that
the number of files on disk matches the `git ls-files` count. Scan for secrets before committing
(the repo is public).

---

## Gotchas

- Keep `.gitignore` rules anchored to the root (`/assets/`, `/docs/`, `/CLAUDE.md`). An unanchored
  `assets/` once silently dropped the D&I guide's CSS from git.
- Git doesn't store empty folders. Use `.gitkeep` (as in `_sources/cs-roadmap/end-to-end/`).
- Pages that aren't restyled yet still load Google Fonts and have their own inline `<style>`. Restyled
  pages don't.
- The Browser pane preview is the user's view too. Reset any viewport emulation when you're done.
