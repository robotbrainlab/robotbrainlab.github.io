# Reorganisation plan — both objectives, no compromise

**Nothing has been moved.** This supersedes the "use `_books`" recommendation in
`REORG-ASSESSMENT-2026-11-11.md` §1. That recommendation traded one of your objectives away, and
you were right to refuse it.

## The key: one file turns the whole problem off

**Add `.nojekyll` to the repository root.** GitHub Pages then skips Jekyll entirely and serves every
file exactly as it is.

**I checked whether this site needs Jekyll for anything. It does not:**

| Jekyll feature | Used by this site |
|---|---|
| `_config.yml` | **None** |
| `_layouts/`, `_includes/`, `_data/`, `_posts/` | **None** |
| Front matter (`---` at the top of a page) | **None.** Checked every tracked `.html` |
| Liquid tags in a served page | **None.** Checked every tracked `.html` |

Every page on this site is hand-written HTML, and the Data & Intelligence guide is pre-generated
HTML. **Jekyll contributes nothing here and only adds the risk.** Turning it off changes how no
existing page is served.

### What that one file buys

1. **The Liquid problem disappears, permanently.** The 12 Markdown files containing `{{.Status}}`
   and `{{ secrets.REGISTRY_TOKEN }}` can never break the build, because nothing parses them. **Nor
   can the 19 Jinja2 templates in `_sources/ai-roadmap/scripts/sitegen/templates/`**, which are a
   larger hazard than the Markdown and would have broken the build the moment that folder was ever
   published.
2. **Folder names stop deciding what is published.** `books/` can be called `books/`, exactly as you
   asked. The underscore convention becomes meaningless, so it can go everywhere.
3. **Markdown is served as written** rather than converted, so a `.md` file in the repository and
   the same file on the site are the same text.

### What it costs, stated plainly

**Everything in the repository becomes reachable by URL**, including folders that are hidden today.
Nothing becomes *more* public in the legal sense — the repository is already public and every file
is already readable on github.com — but a URL gets crawled by search engines in a way a GitHub blob
does not.

**The fix is `robots.txt`, and it is one file.** Drafts and working material stay reachable for you
and stay out of search results:

```
User-agent: *
Allow: /$
Allow: /cse/
Allow: /data-intelligence/
Allow: /mathematics/
Allow: /books/*/
Disallow: /books/*/markdown/
Disallow: /books/*/records/
Disallow: /books/latex/
Disallow: /books/backlog/
Disallow: /books/modern-ai/
Disallow: /research/
Disallow: /tools/
Disallow: /backup/
```

So the finished PDFs are findable and the workshop behind them is not. **If you would rather
everything were indexed, delete the `Disallow` lines — it is one file and it changes nothing else.**

---

## The structure

```
robotbrainlab.github.io/
│
├── .nojekyll                       ← NEW. The file that makes all of this work
├── robots.txt                      ← NEW. Reachable, but drafts not indexed
│
├── index.html                      ← the website, unchanged
├── theme/                          ← shared CSS and JS
├── favicon/
├── cse/                            ← pages only; the PDFs move to books/
├── data-intelligence/              ← pages and the generated guide
├── mathematics/
│
├── books/                          ← every book, one folder per topic
│   ├── README.md                   ← one line per book, and its state
│   │
│   ├── latex/                      ← the shared build, one copy of each piece
│   │   ├── preamble.tex            ← replaces 4 byte-identical copies
│   │   ├── Makefile                ← make BOOK=linux-and-git
│   │   ├── front/                  ← titlepage, copyright, backcover
│   │   ├── tools/convert.sh        ← replaces 6 near-identical copies
│   │   └── styles/
│   │       ├── software-engineering-guide.tex
│   │       └── interview-prep.tex
│   │
│   ├── interview-prep/             ← markdown/ chapters/ book.tex records/ *.pdf
│   ├── linux-and-git/
│   ├── infrastructure-engineering/
│   ├── web-applications/
│   ├── apis-to-fastapi/
│   ├── software-engineering-guide/ ← PDF + chapters/*.tex. No Markdown; that is fine
│   ├── modern-ai/                  ← research and docs; no manuscript yet
│   └── backlog/                    ← the five topics that are a TOC and nothing else
│
├── research/                       ← was _sources. The roadmaps and the generator
├── tools/                          ← was _tools. Site build and link checks
└── backup/                         ← was _backup
```

**The underscores all go.** Once Jekyll is off they mean nothing, and meaningless prefixes are
exactly the confusion you asked me to remove. `_future-books/DECISIONS.md` folds into
`books/README.md`, where the two unstarted books belong.

### One improvement I recommend adding

**The published PDFs are duplicates and the duplication can end.** `cse/books/` holds six files
that are **byte-identical** to the copies under `_sources/` — I compared them. That is 4.8 MB
stored twice, and a standing instruction in the handover to keep them in sync by hand.

With `books/` published, the website links point straight at `books/linux-and-git/Linux and Git from
Zero.pdf` and the second copy is deleted. **One file per book, no sync rule, nothing to forget.**
This edits link targets in `cse/index.html`, so it is a change to the live site and I will do it in
its own commit with the links checked before and after.

---

## The order of work, and why it is this order

**Each step is one commit, so each is revertible on its own with `git revert`.**

| # | Step | Verification before the next step |
|---|---|---|
| 1 | **Add `.nojekyll` alone. Push. Nothing else.** | `curl` every one of the 81 pages and confirm each returns 200 and the expected title. **If anything is wrong, one revert fixes it and not a single file has moved.** |
| 2 | Add `robots.txt` | Fetch it; confirm it serves as plain text |
| 3 | `git mv` the three simple books into `books/` | `make BOOK=…` for each; the PDF must be byte-identical to the one committed |
| 4 | Move `_book/` → `books/interview-prep/` | `bash tools/check-all.sh` must still end `ALL GATES PASS` |
| 5 | Move `_book-modern-ai/` → `books/modern-ai/` | Nothing points into it; a read-through is enough |
| 6 | **Move the Software Engineering Guide, alone** | Rebuild with `make pdf`; the PDF must be byte-identical. **`make clean` must never run** — it deletes `chapters/`, which cannot be regenerated |
| 7 | Share the preamble, Makefile and `convert.sh` | Rebuild **all six** books; every PDF byte-identical |
| 8 | Rename `_sources`→`research`, `_tools`→`tools`, `_backup`→`backup` | Update `CLAUDE.md`, `HANDOVER.md`, `build-di-guide.py`; rebuild the D&I guide |
| 9 | Point the site at `books/` and delete the duplicate PDFs | `link-check.py` reports 0 broken links; `curl` each book link |
| 10 | Update `CLAUDE.md`, `HANDOVER.md`, `link-check.py` for the new layout | `link-check.py` passes |

**Step 1 is deliberately alone.** I cannot test GitHub's build behaviour on this machine; I can only
read the repository. So the one thing I cannot prove locally is proved first, on the live site, with
nothing else in the commit to confuse the result.

## What could still go wrong

| Risk | How it shows | What I do |
|---|---|---|
| `.nojekyll` behaves differently than I expect | A page 404s or serves raw after step 1 | Revert one commit. Nothing has moved |
| A book's relative path breaks on the move | `make` fails, or the PDF differs | Revert that book's commit; the other books are untouched |
| The Software Engineering Guide's `chapters/` is damaged | PDF differs or build fails | It is moved alone, in its own commit, and `git mv` does not alter content |
| A site link is missed in step 9 | `link-check.py` reports it | Fix before pushing; nothing goes live unchecked |
| The D&I guide generator breaks on the rename | `build-di-guide.py` exits | It is checked at every replacement by design and stops rather than publishing a page it does not recognise |

## What I need from you

**One decision, and two confirmations.**

1. **`robots.txt` as drafted** — finished PDFs indexed, working material reachable but not indexed.
   **I recommend this.** Say the word and I will index everything instead.
2. **Confirm the on-ramp books may leave `_sources/`** — it is the one step that conflicts with a
   rule you wrote. **I recommend yes**: they are books, and the rule exists to protect research
   material from website edits, not to keep books buried.
3. **Confirm the underscore removal** (`_sources`→`research`, `_tools`→`tools`, `_backup`→`backup`).
   **I recommend yes**, because once Jekyll is off the prefix means nothing.

Nothing moves until you say so.
