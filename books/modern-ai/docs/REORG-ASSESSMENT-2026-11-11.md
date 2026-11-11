# Repository reorganisation — feasibility assessment

**Nothing has been moved, modified or deleted.** This is the assessment you asked for, written
after reading the actual layout: 1,012 tracked files, 6 LaTeX builds, 155 `.tex` files.

## The answer in one line

**Requests 1, 2 and 3 are straightforward. Request 4 is achievable in a different shape than you
describe. Request 5, taken literally, is not possible — and I can show you why in one table.**

---

## 1. Why the folder should be `_books`, and it is not about privacy

**`[2026-11-11, corrected]` The first version of this section said publishing would expose the
books. The owner pushed back, and he was right.** This repository is public. Every file in
`_book/`, `_book-modern-ai/` and `_sources/` can be read on github.com today by anyone. The leading
underscore stops Jekyll serving a folder as part of the website; **it has never been a privacy
mechanism**, and the handover says so in plain words. The real reasons are below, and the first one
is decisive.

### It would stop the website deploying

There is no `_config.yml`, so GitHub Pages runs Jekyll with default settings. **Jekyll processes
every Markdown file in a published folder, and it reads `{{ … }}` and `{% … %}` as template
commands.** The books are full of both, inside ordinary code samples:

| Found in the book Markdown | Where it comes from |
|---|---|
| `{{.Status}}`, `{{.Names}}`, `{{.Image}}`, `{{.State.Health.Status}}` | Docker `--format` strings |
| `{{ github.sha }}`, `{{ secrets.REGISTRY_TOKEN }}` | GitHub Actions workflow examples |

**12 Markdown files carry them** — 3 in `_book/`, 9 in the on-ramp books. `{{.Status}}` is not
valid template syntax, so the build fails. **A failed build deploys nothing**, which means the
website that works today would go down until the last one was found and escaped. Every future code
sample would be able to do it again, and nothing would warn us.

### Scale, and a check that would stop meaning anything

The site publishes **15 MB** today. Publishing the books takes it to about **176 MB** — eleven times
larger. That is under the 1 GB limit, so it is not fatal. But every commit to a book would rebuild
the website, and `_tools/link-check.py` currently proves that all 81 pages resolve. It would have to
grow to hundreds of pages or stop being a meaningful check.

### Drafts become indexed URLs, and that does not undo

`_book/` is a job-search book with a 31 December 2026 deadline, and its own README calls it
temporary. A published page is crawled and cached. **Removing it later does not remove the cache**,
and a half-written chapter with a mistake in it is findable by anyone looking the author up.

### There is also nothing to gain

Nothing links to these folders. Publishing them adds no reader. **The PDFs that should be reachable
already are** — `cse/books/` holds the finished ones and the live pages link to them. That is the
right pattern and it already works: **publish the book, not the workshop.** If you want more books
on the site, we copy the finished PDF into a website folder and link it, exactly as the four on-ramp
books are handled today.

### One correction of fact, because it changes nothing but is worth being right about

These books are **not** open-source material obtained from the internet. *Modern AI Engineering from
Zero*, *Linux and Git from Zero*, *Infrastructure Engineering*, *Web Applications* and *The Complete
Software Engineering Guide* were all written here. The only genuinely third-party file in the
repository is `mermaid.min.js`, vendored with its licence inside the roadmap's site generator.

---

## 2. Why one shared `latex/` directory cannot hold all books

You asked for all books to be built and maintained inside a single `latex` directory, with no
per-book LaTeX folder. **The file names collide.** There are 155 `.tex` files across the six
builds, and these are the duplicates:

| Filename | How many books have one |
|---|---|
| `cover.tex` | 8 |
| `titlepage.tex` | 6 |
| `preface.tex` | 6 |
| `preamble.tex` | 6 |
| `copyright.tex` | 6 |
| `book.tex` | 6 |
| `backcover.tex` | 6 |
| `book-meta.tex` | 5 |
| `highlighting.tex` | 4 |
| `00-preface.tex` | 3 |

Two further problems sit behind the names:

- **`latexmk` writes its output beside the source** — `book.aux`, `book.toc`, `book.pdf`,
  `book.fls`. Six books compiled in one directory overwrite each other's build state, and a failed
  build would leave another book's artefacts behind.
- **Every book's `book.tex` uses `\input{chapters/…}` with relative paths.** Flattening them means
  renaming roughly 60 files and rewriting every `\input` in all six books.

**That last point is where it stops being merely expensive.** See issue 4 below.

### What I recommend instead, which gives you what you actually want

**The duplication you want removed is real, and it can all go.** It is not in the chapter files; it
is in the machinery:

| Duplicated today | Copies | Can it be shared? |
|---|---|---|
| `preamble.tex`, 344 lines | 4 **byte-identical** copies | **Yes, immediately** |
| `Makefile` | 6 near-identical copies | **Yes** |
| `tools/convert.sh` | 6 near-identical copies | **Yes** |
| `front/` (titlepage, copyright, backcover) | 6 sets | **Yes, with per-book metadata** |

So: **one `_books/latex/` holding the machinery, and each book keeping only its own content.** You
get one place to maintain the build, and no per-book LaTeX folder — which is the substance of
requests 4 and 5. What you do not get is all the `.tex` files in one directory, because they cannot
share a namespace.

Two books need extras on top of the shared preamble, and these are additions rather than conflicts:

- **The Complete Software Engineering Guide** adds about 20 macros — `\lifecyclepart`,
  `\phasestrip`, `\prebookpart`, `\mapstrip`, `\bookpart`, and the syntax-highlighting tokens.
- **The interview-prep book** adds `\booksubpart`, `\partlevels`, `\subpartlevels`,
  `\toplevelchapters`, and redefines `\indexletter`.

They live in `_books/latex/styles/<book>.tex`, loaded after the shared preamble.

---

## 3. Website files that must not move

`cse/books/` and `data-intelligence/books/` are **not book sources**. They hold the published PDFs
and lab zips that the live pages link to, as copies of the ones under `_sources/`. **If they move,
every book link on the live site breaks.** They stay exactly where they are.

The same applies to `index.html`, `theme/`, `favicon/`, `cse/`, `data-intelligence/` and
`mathematics/`. Your request 1 — website separate from books — is already true today, and the
reorganisation should preserve it rather than disturb it.

---

## 3b. Settled by the owner, 2026-11-11

- **The single-folder LaTeX idea is dropped.** Shared machinery, per-book content, as in §2.
- **A book with no Markdown source stays as a PDF.** Where the Markdown is gone, we keep the PDF
  and the generated `.tex`, and we do not try to reconstruct the source. This simplifies §4 below
  considerably: the Software Engineering Guide needs no rebuild path invented for it.

## 4. The one book where a mistake cannot be undone

**The Complete Software Engineering Guide cannot be rebuilt from its Markdown.** Its
`tools/convert.sh` reads a Markdown library that is not in `_sources/` and not anywhere on this
machine — searched on 2026-10-08. Only the generated `chapters/*.tex` survive, and they are
committed.

**For that book, the `.tex` files are the source.** Consequences for this reorganisation:

- Its 67 `.tex` files must be moved with their content and their relative structure intact.
- **`make clean` must never run** in its directory; it deletes `chapters/` and nothing can
  regenerate them.
- It is the strongest argument against flattening: renaming 60 files and rewriting their `\input`
  lines would be a large edit against the one book with no recovery path.

I would move this book **last**, verify `make pdf` produces a byte-identical PDF, and commit it
separately so it can be reverted alone.

---

## 5. `_sources/` is governed as a separate repository, and this is your call

Your own handover says `_sources/` is a separate research repo: *"never change its content,
templates or generator for site purposes"*, and `_sources/ai-roadmap/` carries its own `AGENTS.md`
and `handover.md`. It holds 607 of the repository's 1,012 tracked files.

But the on-ramp books live inside it, at `_sources/cs-roadmap/on-ramp/books/`. **Moving them to
`_books/` conflicts with that rule**, so it needs your word rather than my judgement.

**I recommend moving them**, because they are books and the rule was written to protect research
material from website edits, not to keep books buried. `_sources/ai-roadmap/` is not a book and
should not move — it is the generator for the live Data & Intelligence guide.

---

## 6. Five of the twelve "books" are empty

| Folder | Tracked files |
|---|---|
| `data-structures-and-algorithms` | 1 |
| `databases` | 1 |
| `distributed-systems` | 1 |
| `networking` | 1 |
| `operating-systems` | 1 |

Each holds a `TOC.md` and nothing else. **I recommend `_books/_backlog/`** so the `_books/` listing
shows only real books. They are not deleted and the handover's note that `databases/TOC.md` is the
next book worth writing still holds.

---

## 7. Two smaller things, neither urgent

- **`_book-modern-ai/` has no manuscript yet** — it is research, records and governance. It fits
  the topic-folder shape but will have no `latex/` content until step 11.
- **`_book/`'s git history already has one break.** Its 31 commits arrived by subtree merge with
  their old paths, so `git log --follow` does not trace a file across that move. A second move adds
  a second break. Recoverable, but worth knowing before you approve.

---

## The proposed structure

```
robotbrainlab.github.io/
│
├── index.html                      ← the website, unchanged
├── theme/                          ← shared CSS and JS
├── favicon/
├── cse/                            ← incl. cse/books/*.pdf, linked from live pages
├── data-intelligence/              ← incl. the generated guide
├── mathematics/
│
├── _books/                         ← everything book. Never published
│   ├── README.md                   ← one line per topic, and its state
│   │
│   ├── latex/                      ← THE shared build. One copy of each piece
│   │   ├── preamble.tex            ← replaces 4 identical copies
│   │   ├── Makefile                ← make BOOK=linux-and-git
│   │   ├── front/                  ← titlepage, copyright, backcover
│   │   ├── tools/convert.sh        ← replaces 6 near-identical copies
│   │   └── styles/
│   │       ├── software-engineering-guide.tex
│   │       └── interview-prep.tex
│   │
│   ├── interview-prep/             ← one folder per topic
│   │   ├── markdown/  chapters/  book.tex  records/  *.pdf
│   ├── modern-ai/                  ← research + docs; no manuscript yet
│   ├── linux-and-git/
│   ├── infrastructure-engineering/
│   ├── web-applications/
│   ├── software-engineering-guide/ ← move last, verify, commit alone
│   ├── apis-to-fastapi/
│   └── _backlog/                   ← the five TOC-only topics
│
├── _research/                      ← optional rename of _sources. See below
│   ├── ai-roadmap/                 ← generator for the live D&I guide. Do not move
│   ├── ai-tools/
│   └── interview-research/
│
├── _tools/                         ← site build and link checks
└── _backup/
```

**On renaming `_sources/` to `_research/`:** it reads better, but the name appears in `CLAUDE.md`,
`HANDOVER.md`, `_tools/build-di-guide.py` and the roadmap's own governance files. **I recommend
leaving it as `_sources/` for now** and doing it as a separate change if you still want it — one
rename at a time is easier to verify and to revert.

---

## What this costs, honestly

| Step | Risk | Why |
|---|---|---|
| Create `_books/`, move the three simple books | **Low** | `git mv`, relative paths inside each book are preserved |
| Move `_book/` and `_book-modern-ai/` | **Low**, one history break | Nothing outside them points in |
| Share the preamble and Makefile | **Low** | 4 copies are already byte-identical; the other 2 become `styles/` files |
| Move the Software Engineering Guide | **Medium** | The one book with no rebuild path. Move last, verify the PDF, commit alone |
| Move the on-ramp books out of `_sources/` | **Needs your ruling** | Conflicts with the separate-repo rule |
| Rename `_sources/` → `_research/` | **Medium** | Touches `CLAUDE.md`, `HANDOVER.md` and a build script. Recommend deferring |

**Every step is a `git mv`, so every step is revertible with `git revert`.** I would do one commit
per step, run `_tools/link-check.py` after the website-adjacent ones, and rebuild each moved book
to prove its PDF is unchanged before moving the next.

## What I need from you

1. **May the on-ramp books leave `_sources/`?** This is the only one that conflicts with a rule you
   wrote. I recommend yes.
2. **The five empty topics to `_books/_backlog/`** — I recommend yes.
3. Anything in the structure above you want drawn differently.

**No longer open:** the folder is `_books/` — not for privacy, which was never the reason, but
because publishing it breaks the site build on 12 files and gains nothing (§1). The LaTeX question
and the PDF-only question are settled above.

Nothing moves until you say so.
