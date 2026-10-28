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
| I · Understand — *Mental Model* | 1–7 | 98 | **Done** — 7 of 7, 2026-10-23 |
| I · Understand — *Inside the Model* | 8–17 | 168 | **Done** — 10 of 10, 2026-10-28 |
| II · Use | 18–39 | 362 | **Drafting** — 12 of 22 done |
| III · Apply | 40–50 | 190 | Not started |
| IV · What Next | 51–57 | 136 | Not started |
| Appendices | A–D | 83 | **A (cheat sheet, 131 items), B (100 questions) and C (glossary, 171 terms) in the PDF.** A and C are generated from the chapters and gated; B's answers come as chapters land. D is the LaTeX index |

The estimates above sum to about 1,042 numbered pages. **That is a sum, not a target** — the
book is as long as the material earns, and 1,500 to 2,000 would be welcome rather than a
problem (`BOOK-GUIDE.md` §11 point 5). Do not project a finished length against it.

**Measure with `python3 tools/pages.py`**, which reads the
built PDF and ends each chapter where the next opener begins. Do not subtract folios by hand:
three chapters were over-counted that way (5 as 12 pp, 7 as 9, 8 as 15) because the part and
sub-part opener pages sitting after the last written chapter were counted into it. See
`LEDGER-DEFECTS.md` entry 23. From the current build:

```text
  ch    printed   pp  est  of est
   1     3-12     10   14     71%
   2    13-22     10   18     56%
   3    23-32     10   14     71%
   4    33-42     10   16     62%
   5    43-53     11   14     79%
   6    54-64     11   12     92%
   7    65-72      8   10     80%
   8    74-85     12   14     86%
   9    86-97     12   12    100%
  10    98-113    16   20     80%
  11   114-131    18   24     75%
  12   132-144    13   16     81%
  13   145-157    13   14     93%
  14   158-170    13   22     59%
  15   171-182    12   20     60%
  16   183-192    10   18     56%
  17   193-200     8    8    100%
  18   202-213    12   16     75%
  19   214-232    19   20     95%
  20   233-250    18   18    100%
  21   251-265    15   14    107%
  22   266-279    14   12    117%
  23   281-296    16   16    100%
  24   297-309    13   14     93%
  25   310-323    14   12    117%
  26   324-353    30   28    107%
  27   356-378    23   16    144%
  28   379-400    22   16    138%
  29   401-420    20   14    143%
  30   421-439    19   14    136%
```

**Part I is complete: chapters 1–17, 197 printed pages against a 266-page estimate (74%).**
Part II has begun: chapters 18 to 30 come to 242 pages, so 439 printed pages in all. Chapter 30
opens the evaluation run of the part (30 to 33) and is the first chapter since 17 whose material
is a method rather than a mechanism. Chapter 26
is the longest in the book at 30 pages, and it holds seven Covers items of which three are
formulas that have to be worked rather than quoted.
Chapters 9, 17 and 20 landed exactly on their estimates; **21, 22 and 25 exceed one**, by one
page, two and two. All three gained those pages in their fix passes rather than in drafting,
which is the pattern across Part II: these chapters reach their estimates by answering a Covers
item or a bank question the first draft had missed, not by padding. See `LEDGER-DEFECTS.md`
entry 30 for chapter 19's, the trials half of bank question 45 for chapter 20's, entry 35 for
what chapter 21's review found in the record rather than the prose, and entries 36 and 37 for
chapter 22's. Chapter 25's two pages are the clearest case of all: both reviews found it
claiming more than its support allowed, and every narrowing is longer than the overclaim it
replaced — see entries 40 and 41.

The estimates are estimates, never targets — `BOOK-GUIDE.md` §11. Read `LEDGER-DEFECTS.md`
entry 12 before drawing any conclusion from the percentages.

Status values: *Not started* → *Drafting* → *Editing* → *Done*.

## Build

```bash
cd latex
make                                   # markdown -> chapters -> book.pdf
PAGES_MIN=600 PAGES_MAX=1000 make check
```

Needs MacTeX (`latexmk`, `xelatex`), pandoc and poppler (`pdftotext`), all already installed.
