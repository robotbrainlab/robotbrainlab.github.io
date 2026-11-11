# Book template (O'Reilly style, Markdown → PDF)

> **`BOOK-GUIDE.md` (at the repository root) is the authority on each book's structure, style, and conventions.** This README covers the build. Where they seem to differ, follow the guide.

The shared build for every "from Zero" book. It produces a PDF in the design of
*APIs to FastAPI*: 7 × 9.1875 in pages (504 × 661.5 pt), Crimson Pro body text,
Source Sans 3 headings, Source Code Pro code, right-aligned chapter openers, part
pages with a "What to ignore for now" note, and tip/note/warning callouts with icons.

**The Markdown is the only source of truth.** `chapters/` and `generated/` are rebuilt on
every `make`; never edit them.

Pipeline: `../markdown/*.md` → `tools/convert.sh` (pandoc + `tools/filter.lua`) →
`chapters/*.tex` → `latexmk` (XeLaTeX + makeindex) → `book.pdf`.

## Start a new book

```bash
cd books/<slug>
mkdir -p markdown latex labs
cp -R ../book-template/{Makefile,latexmkrc,preamble.tex,book.tex,book-meta.tex,tools,front,.gitignore} latex/
```

Then:

1. Edit `latex/book-meta.tex`: title, subtitles, tagline, edition, year, revision history,
   tested versions, category and back-cover blurb. Nothing else holds book metadata.
2. Write `markdown/00-preface.md`, the chapters (`01-….md`, …), and the appendices (`A-….md`, `B-….md`, …), with the glossary as the last one.
3. List them in `latex/book.tex` (parts and order), then build.

Layout:

```
books/<slug>/
  TOC.md
  markdown/     00-preface.md, 01-….md, 02-….md, …, A-….md, B-….md (appendices; the glossary is the last)
  latex/        this template: book.tex, book-meta.tex, preamble.tex, Makefile, tools/, front/
```

Do not change `preamble.tex` or `tools/` inside one book: fix the template, then copy the
changed file into each book, so all books stay in the same series design.

## Build

Requirements: pandoc 3, MacTeX (`/Library/TeX/texbin`, put on `PATH` by the Makefile),
python3 and poppler (`pdfinfo`, `pdffonts`) for the checks.

```bash
cd books/<slug>/latex
make            # Markdown -> chapters/*.tex -> book.pdf
make check      # pre-flight (below)
```

The PDF lands in `books/<slug>/latex/book.pdf`. When the book is finished, copy it to
`books/<slug>/<Book Title>.pdf` (next to its folders, as `books/apis-to-fastapi/` does).

Other targets: `make convert` (only regenerate `chapters/`), `make pdf` (only typeset),
`make clean`.

## The sample book

`sample/` is a two-chapter mini book that uses every feature. It is the best reference for
the conventions: read `sample/markdown/*.md` next to `sample/sample.pdf`.

```bash
cd books/book-template
make sample     # copies the template into sample/latex/, builds, writes sample/sample.pdf
```

Only `sample/markdown/`, `sample/latex/book.tex` and `sample/latex/book-meta.tex` are its
sources; everything else in `sample/latex/` is copied from the template by `make sample`.
`sample/preview/` holds rendered pages for a quick look at the design.

## Markdown conventions

One Markdown file per chapter. The dialect is CommonMark with pipe tables, definition
lists, attributes, GitHub alerts, footnotes and smart quotes (`commonmark_x`). `$…$` is **not**
math, so "$5" stays text. Files starting with `_` are drafts and are skipped.

| You write | You get |
|---|---|
| `# Title` (once, first line) | The chapter opener: "CHAPTER N" and the title, right-aligned, with a rule. A leading "Chapter 3:" or "Appendix B:" in the heading is dropped (numbers come from LaTeX). |
| The first paragraph under `# Title` | The chapter intro. |
| `## Section` | A section: in the contents and in the right-hand running head. |
| `### Subsection`, `#### Sub-subsection` | Smaller headings, not in the contents. |
| `**term**` | Bold, and an **index entry** (automatic for bold phrases of up to four words that don't end in `:` `.` `!` `?`; not in the Preface, the Glossary, headings, or the closing summary section). |
| `[**not a term**]{.noindex}` | Bold without an index entry. |
| `[**APIs**]{idx="API"}` / `[plain words]{.idx}` / `[]{idx="port"}` | Index entry under another key / for plain text / invisible. Sub-entries: `idx="line ending!CR LF"`. |
| `> **Tip:** …` | Tip callout, lightbulb icon (a suggestion that saves time or trouble). |
| `> **Note:** …` | Note callout, page icon (a general remark). |
| `> **Warning:** …` | Warning callout, warning-sign icon (can cost data, money, or security). |
| `> [!TIP]`, `> [!NOTE]`, `> [!WARNING]` | The same callouts (GitHub alert syntax). |
| `> **You understand this when** …` | The chapter's self-check: a small tinted box. |
| `> any other quote` | An indented italic quotation. |
| ` ```python `, ` ```bash `, … | Highlighted code, Source Code Pro 7.5 pt, no frame. Long lines wrap with a small hook. **No shell prompt** (`$ `): the build warns if it sees one. |
| ` ``` ` (no language) or ` ```text ` | Program output, same face, a shade lighter. Put it right after the command: the two are kept on one page. |
| A plain block with box-drawing characters (`┌─┐│└┘├┤┬┴┼▶▼`) | A diagram: never wrapped, font size chosen so it fits the text width, strokes join. In this series, keep diagrams at most 64 characters wide, with every line of a box the same width (the build can scale wider ones, and warns below 5 pt). |
| Pipe table | Full-width table: grey header band, top/middle/bottom rules, columns sized from their content. |
| `Term` newline `: definition` (definition list) | "**Term**: definition" entries, sorted A–Z automatically in the file titled `# Glossary`. **This series uses tables instead** (Term \| Meaning) for Key Terms and the glossary; keep a table glossary alphabetical yourself. |
| `![Caption](images/x.png)` | Figure "Figure N-M. Caption"; the path is relative to `markdown/`. |
| `[text](02-other.md#section-id)` | A link inside the PDF (links to files outside the book become plain text, with a warning). |
| `` `\newpage`{=latex} `` | Raw LaTeX, as an escape hatch. |

### Chapter skeleton

The chapter shape used in this series (see `BOOK-GUIDE.md`, section 8.3):

````markdown
# Chapter Title

One short paragraph: what this chapter gives the reader.

*The problem.* The TOC's "Opens with" line.

*The question.* The question that problem raises.

## The Idea

The idea first, in plain words, with an everyday picture. **New term** in bold.

> **Tip:** …

## Using It

Explain, then show the command, then its real output:

```bash
command --flag
```

```text
real output
```

## Lab: Do the Thing

1. Step one. **Expected:** what the reader should see.
2. Step two. **Expected:** …

## Summary, Key Terms, and Review Questions

### Summary

- One line per idea.

### Key Terms

| Term | Meaning |
|---|---|
| New term | One-line meaning |

### Review Questions

1. A question.

> **You understand this when** you can …
````

### The Preface

`markdown/00-preface.md` starts with `# Preface` and has the sections from the book guide:
Who This Book Is For, How This Book Is Organized, How to Use This Book, What You Need
Installed, Conventions Used in This Book. For the conventions list, three one-line callouts
(`> **Tip:** A suggestion that saves time or trouble.` and so on) render exactly like the
API book's icon legend. `front/preface.tex` includes it (and prints a placeholder until it exists).

### Parts, appendices, glossary, index (in `book.tex`)

```latex
\bookpart{I}{Understand}
  {networking theory, the history of the web, and HTTP/2 vs HTTP/3.}   % "What to ignore for now"
\input{chapters/01-what-an-api-is}
...
\bookpart{IV}{What Next}{}            % empty third argument: no note
...
\appendix                             % following chapters are Appendix A, B, …
\input{chapters/90-cheat-sheet}
\input{chapters/99-glossary}          % the glossary is the last appendix
\backmatter
\printindex
\input{front/backcover}
```

The third argument of `\bookpart` is the note text only; "*What to ignore for now:*" is added
for you. The contents get a "Part I. Understand" line per part and an "Appendices" line
before the first appendix.

## Files

| Path | What it is |
|---|---|
| `book.tex` | Master file: parts, chapter order, appendices, index. |
| `book-meta.tex` | Book metadata: title, subtitles, edition, revisions, tested versions, blurb. |
| `preamble.tex` | The series design: page, fonts, headings, running heads, callouts, code, tables, contents, index. |
| `front/` | Cover, title page, copyright page, preface include, back cover (all driven by `book-meta.tex`). |
| `tools/convert.sh` | Converts every `../markdown/*.md` to `chapters/<stem>.tex`; warns about files missing from `book.tex`. |
| `tools/filter.lua` | The conventions above. |
| `tools/code.theme` | The light syntax-highlighting theme (bold keywords, grey italic comments, teal strings). |
| `tools/index.ist` | makeindex style (letter headings). `latexmkrc` tells latexmk to use it. |
| `tools/check.sh` | The pre-flight checks. |
| `chapters/`, `generated/` | Build output: never edit. |

## Pre-flight checklist (`make check`)

Before calling a book done:

- [ ] `make` finishes with no errors.
- [ ] **0 overfull boxes** (nothing runs into the margin). `make check` lists any with the
      source line; usually a long word in a table cell or an over-wide diagram.
- [ ] 0 missing glyphs (a character none of the fonts has), 0 undefined references.
- [ ] Page size 504 × 661.5 pt; CrimsonPro, SourceSans3 and SourceCodePro embedded.
- [ ] Page count inside the target: `make check PAGES_MIN=50 PAGES_MAX=100` (the defaults).
- [ ] "Bold terms not in glossary" is empty (or each one listed is deliberately not a term).
- [ ] Every chapter has its lab, summary, key terms, review questions, and
      "You understand this when…" box; every command and output was really run.
- [ ] Skim the PDF: no heading alone at the foot of a page, no callout icon touching text.

Notes: `make check` also lists "Other fonts". DejaVu Sans Mono (box-drawing diagrams, the
face Menlo is built on) and CMMI5/CMSY5 (the tiny hook arrow on wrapped code lines) are expected.
