# Books

One folder per book. **One shared build in `latex/`.** Nothing generated is committed.

## Build any book

```bash
make -C books/latex list                       # every book that can be built
make -C books/latex BOOK=linux-and-git         # Markdown -> chapters -> PDF
make -C books/latex BOOK=linux-and-git pdf     # typeset only
```

## The shape every book has

| | |
|---|---|
| `book.tex` | the order of the chapters |
| `book-meta.tex` | title, subtitle, author, year — everything that names this book |
| `markdown/` | **the source.** One file per chapter |
| `TOC.md` | the plan |
| `<Title>.pdf` | the delivered book |
| `labs/` | lab files, where a book has them |

**Generated and never committed:** `chapters/`, `generated/`, `book.pdf` and the LaTeX
side files. `books/.gitignore` holds that rule once, for every book.

**One exception, and it is important.** `complete-software-engineering-guide/chapters/` **is**
committed, because that book has no Markdown here and nothing can regenerate it. See the warning
below.

**Book-specific overrides are allowed and are found before the shared copies:** a book may keep its
own `front/`, `tools/`, `assets/`, `content/` or `cover/`. Only the guide does.

## The books

| Folder | What it is | State |
|---|---|---|
| `modern-ai-engineering-from-zero` | *Modern AI Engineering from Zero* | **Finished** (2026-10-31), 57 chapters |
| `complete-software-engineering-guide` | *The Complete Software Engineering Guide* | **Published.** ⚠ see below |
| `linux-and-git` | *Linux and Git from Zero* | **Published**, with labs |
| `infrastructure-engineering` | *Infrastructure Engineering from Zero* | **Published**, with labs |
| `apis-to-fastapi` | *APIs to FastAPI* | **Published.** PDF and cover only — no Markdown source in this repository |
| `rag-from-zero` | *RAG from Zero: A Practical Guide* | **Published** (first edition 2026-09-30), 9 chapters in 3 parts, 2 appendices, 74 pages. `[2026-11-12]` **PDF only** — no Markdown source and no `labs/` in this repository, though the book's copyright page says a `labs` folder accompanies it. Not linked from the website |
| `web-applications` | *Web Applications from Zero* | Not published alone. Its six chapters are the pre-book inside the guide |
| `modern-ai` | *Modern AI: Research, Science and Engineering* | **In research.** No manuscript yet |
| `python` | *Python from Zero* | **Started 2026-11-12.** `TOC.md` only — 51 chapters, approved and reviewed. No manuscript. `CLAUDE.md` governs a session here |
| `future-books` | The decisions for *Python* and *Machine Learning and Deep Learning*, plus five topics that are a `TOC.md` and nothing else | **Decisions, not a book.** Python has started; Machine Learning and Deep Learning has not |

## `latex/` — the shared build

| | |
|---|---|
| `preamble.tex` | the shared preamble. **Four books used to hold byte-identical copies** |
| `Makefile`, `latexmkrc` | the shared build. Six near-identical copies before |
| `front/` | cover, title page, copyright, preface, back cover — all driven by `book-meta.tex` |
| `tools/` | `convert.sh`, the pandoc filter, the index style, the code theme |
| `assets/` | the emoji set, shared by every book that does not override it |
| `styles/` | the two preambles too different to merge: `modern-ai-engineering-from-zero`, `complete-software-engineering-guide` |
| `template/` | `book.tex` + `book-meta.tex` for a new book, with `preview/` and `style-reference.pdf` showing the house style |

## ⚠ The guide cannot be rebuilt from Markdown

`complete-software-engineering-guide` reads a Markdown library that is **not in this repository and
not on this machine** — searched 2026-10-08. Only the generated `chapters/*.tex` survive, 57 files,
and they are committed because they are the source.

`make BOOK=complete-software-engineering-guide clean` is **refused by the Makefile**, because clean
deletes `chapters/`.

## A new book

```bash
mkdir books/<slug> && cp books/latex/template/book*.tex books/<slug>/
mkdir books/<slug>/markdown        # write the chapters here
make -C books/latex BOOK=<slug>
```

Copy no preamble, no Makefile, no `tools/` and no `front/`. That is what `latex/` is for.

## What reaches the website

`cse/index.html` links straight at the delivery PDFs here — **one copy of each file**. Jekyll is off
(`/.nojekyll`) so everything is served, and `/robots.txt` keeps the Markdown, chapters, records,
labs, tools, `future-books/` and `modern-ai/` out of search results. Nothing here is hidden: the
repository is public and every file is readable on github.com.
