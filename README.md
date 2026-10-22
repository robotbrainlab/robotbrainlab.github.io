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
| Review PDF | `python3 tools/make-toc-pdf.py` — builds `TOC.pdf` from `TOC.md` in the book's own design |

## Status

| Part | Chapters | Pages | Status |
|---|---|---|---|
| I · Understand — *Mental Model* | 1–7 | 98 | **Drafting** — 5 of 7 done |
| I · Understand — *Inside the Model* | 8–17 | 168 | Not started |
| II · Use | 18–39 | 362 | Not started |
| III · Apply | 40–50 | 190 | Not started |
| IV · What Next | 51–57 | 136 | Not started |
| Appendices | A–D | 83 | Not started |

About 1,042 numbered pages in all. Measured from the current build (`latex/book.toc`, 2026-10-23):

| Ch | Printed | Estimate | |
|---|---|---|---|
| 1 | 10 pp (3–12) | 14 | 71% |
| 2 | 10 pp (13–22) | 18 | 56% |
| 3 | 10 pp (23–32) | 14 | 71% |
| 4 | 9 pp (33–41) | 16 | 56% |
| 5 | 12 pp (42–53) | 14 | 86% |

The estimates are estimates, never targets — `BOOK-GUIDE.md` §11. Read `LEDGER-DEFECTS.md`
entry 12 before drawing any conclusion from the percentages; the figures there were taken
before the front matter settled and are a page or two lower than these.

Status values: *Not started* → *Drafting* → *Editing* → *Done*.

## Build

```bash
cd latex
make                                   # markdown -> chapters -> book.pdf
PAGES_MIN=600 PAGES_MAX=1000 make check
```

Needs MacTeX (`latexmk`, `xelatex`), pandoc and poppler (`pdftotext`), all already installed.
