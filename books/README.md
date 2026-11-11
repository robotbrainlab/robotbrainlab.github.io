# Books

Every book in one place, one folder per topic, and **one shared LaTeX build in `latex/`.**

## How to build any book

```bash
make -C books/latex list                       # every book that can be built
make -C books/latex BOOK=linux-and-git         # convert markdown, then typeset
make -C books/latex BOOK=linux-and-git pdf     # typeset only
```

The build machinery lives once, in `latex/`: `preamble.tex`, `latexmkrc`, `Makefile`, `front/`,
`tools/` and `styles/`. **No book has its own LaTeX folder.** Each book holds only what is its own —
`book.tex`, `book-meta.tex`, `markdown/`, `chapters/`, `generated/`, `assets/`.

**Two books keep their own preamble**, in `latex/styles/`, because they are too different from the
shared one to merge. Their `book.tex` names the style file. `interview-prep` shares 336 of 344 lines
and could be merged later; `complete-software-engineering-guide` shares 72 and should not be.

## The books

| Folder | What it is | State |
|---|---|---|
| `interview-prep` | *Modern AI Engineering from Zero* — 57 chapters, written for AI/LLM interview preparation | **Finished** (2026-10-31). Temporary: it exists for a job search, not as a permanent library |
| `complete-software-engineering-guide` | *The Complete Software Engineering Guide* — one project carried from idea to production | **Published.** ⚠ See the warning below |
| `linux-and-git` | *Linux and Git from Zero* | **Published**, with lab files |
| `infrastructure-engineering` | *Infrastructure Engineering from Zero* | **Published**, with lab files |
| `apis-to-fastapi` | *APIs to FastAPI* | **Published** |
| `web-applications` | *Web Applications from Zero* | **Not published on its own.** Its six chapters are the pre-book *How Web Applications Work* inside the guide |
| `modern-ai` | *Modern AI: Research, Science and Engineering* | **In research.** No manuscript yet — step 4 of 11, waiting on the owner's ruling on the area proposal |
| `book-template` | The pattern for a new book: `book.tex`, `book-meta.tex` and a worked `sample/` | Reference |
| `backlog/` | Five topics that are a table of contents and nothing else | Not started |

`FUTURE-BOOKS.md` holds the decisions for the two books planned after *modern-ai* — Python, and Core
Machine Learning and Deep Learning. **Neither may start until its rules are written and its table of
contents approved**, which is the owner's instruction.

## ⚠ The guide cannot be rebuilt from Markdown

`complete-software-engineering-guide` reads a Markdown library that **is not in this repository and
not on this machine** — searched 2026-10-08. Only the generated `chapters/*.tex` survive, 57 files,
and they are committed.

**So for that book the `.tex` files are the source.** `make BOOK=complete-software-engineering-guide
clean` is refused by the shared Makefile, because clean deletes `chapters/` and nothing can
regenerate it. `make pdf` works and is the only build it needs.

## Which of these reach the website

The website links to the finished PDFs in place — `cse/index.html` points at
`../books/<slug>/<Title>.pdf`. There is **one copy of each file**. Until 2026-11-11 the PDFs were
duplicated into `cse/books/`, with a written rule to keep the two in sync by hand; the duplicates
are gone.

Everything here is *served*, because Jekyll is off (`/.nojekyll`), but `/robots.txt` keeps the
working material — markdown, chapters, records, labs, tools, the backlog and `modern-ai` — out of
search results. Nothing here is hidden: this repository is public and every file is readable on
github.com.

## New book?

Copy `book-template/book.tex` and `book-template/book-meta.tex` into a new folder beside the others,
add a `markdown/` folder, and build it with `make -C books/latex BOOK=<your-folder>`. Do not copy a
preamble, a Makefile or a `tools/` folder — that is what `latex/` is for.
