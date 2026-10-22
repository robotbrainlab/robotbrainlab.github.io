# Modern AI Engineering from Zero

One book, written from zero, to prepare for AI/LLM application engineer interviews by
**31 December 2026**. Temporary by design: this repository exists for that deadline, not as a
permanent library.

It has **nothing to do with any website**. The syllabus came from the author's own research
notes; the book stands alone and never refers to a site, a roadmap or numbered steps.

| | |
|---|---|
| **Start here** | `HANDOVER.md` — decisions, state, what is blocked |
| Spec | `BOOK-GUIDE.md` |
| Table of contents | `TOC.md` |
| Chapter sources | `markdown/` (the only source of truth) |
| Lab files | `labs/` |
| Build | `latex/` — `cd latex && make` |

## Status

| Part | Chapters | Pages | Status |
|---|---|---|---|
| *Before Part I* · Inside the Model | 1–10 | 158 | Not started |
| I · Understand | 11–17 | 98 | Not started |
| II · Use | 18–36 | 304 | Not started |
| III · Apply | 37–45 | 155 | Not started |
| IV · What Next | 46–51 | 110 | Not started |
| Appendices | A–D | 45 | Not started |

About 875 numbered pages in all.

Status values: *Not started* → *Drafting* → *Editing* → *Done*.

## Build

```bash
cd latex
make                                   # markdown -> chapters -> book.pdf
PAGES_MIN=600 PAGES_MAX=1000 make check
```

Needs MacTeX (`latexmk`, `xelatex`), pandoc and poppler (`pdftotext`), all already installed.
