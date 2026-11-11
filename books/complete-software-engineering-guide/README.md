# The Complete Software Engineering Guide — LaTeX book

A standalone book built from the library's Markdown, sections 1–4:
Part I Product Discovery · Part II Project Planning · Part III Writing the Code ·
Part IV Building Real Applications (43 chapters) · Appendices A–F.

**The Markdown is the only source of truth.** Never edit `chapters/` — it is regenerated
on every build. Edit the `.md` files, then run:

```bash
make
```

The build uses **MacTeX** (latexmk + XeLaTeX) and takes about a minute.
`make tectonic` is a fallback that builds `book-tectonic.pdf` with Tectonic instead
(same design; a few page breaks differ because its packages are older).

## Layout

| Path | What it is |
|---|---|
| `book.tex` | Master file: order of parts, sub-part openers and chapters |
| `preamble.tex` | The whole design: page size, fonts, colours, boxes, headings, contents |
| `front/` | Cover (places `../cover/cover.pdf`, the series cover built in `../cover/`), title, copyright, dedication, preface, back cover |
| `content/` | Markdown for the two book-only chapters: the opening map (*How Software Gets Built*) and the closing chapter (*The Same Process in a Real Team*) |
| `tools/convert.sh` | List of source files and the Markdown → LaTeX conversion |
| `tools/filter.lua` | Conversion rules (headings, listings, diagrams, tables, cross-references) |
| `tools/standalone.pl` | Small wording fixes so the book reads standalone (Markdown untouched) |
| `assets/emoji/` | The few emoji used in code examples, as images |
| `chapters/`, `generated/` | Build output — do not edit |

## Adding a chapter
Add the file to `SOURCES` in `tools/convert.sh` (Book chapters `NN-*.md` are picked up
automatically) and an `\input{chapters/<stem>}` line in `book.tex`.

## "You are here"
Part pages mark their phase on the four-phase strip (`\lifecyclepart`, last argument).
Stage pages take two extra arguments in `book.tex`: the highlighted steps of the six-step map
(1 Discover, 2 Plan, 3 Code, 4 Ship, 5 Run, 6 Grow; e.g. `{3,4}`) and the piece of the system.
