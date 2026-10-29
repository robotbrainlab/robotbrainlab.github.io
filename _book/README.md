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
| II · Use | 18–39 | 362 | **Done** — 22 of 22, 2026-10-29 |
| III · Apply | 40–50 | 190 | **Drafting** — 3 of 11 done |
| IV · What Next | 51–57 | 136 | Not started |
| Appendices | A–D | 83 | **A (cheat sheet, 272 items), B (100 questions) and C (glossary, 270 terms) in the PDF.** A and C are generated from the chapters and gated; B's answers come as chapters land. D is the LaTeX index |

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
  14   158-171    14   22     64%
  15   172-183    12   20     60%
  16   184-194    11   18     61%
  17   195-202     8    8    100%
  18   204-215    12   16     75%
  19   216-234    19   20     95%
  20   235-253    19   18    106%
  21   254-268    15   14    107%
  22   269-283    15   12    125%
  23   284-299    16   16    100%
  24   300-312    13   14     93%
  25   313-326    14   12    117%
  26   327-356    30   28    107%
  27   357-379    23   16    144%
  28   380-401    22   16    138%
  29   402-421    20   14    143%
  30   422-440    19   14    136%
  31   441-465    25   18    139%
  32   466-490    25   16    156%
  33   491-516    26   16    162%
  34   517-539    23   16    144%
  35   540-566    27   22    123%
  36   567-597    31   18    172%
  37   598-623    26   10    260%
  38   624-650    27   14    193%
  39   651-678    28   22    127%
  40   680-704    25   20    125%
  41   705-729    25   18    139%
  42   730-758    29   16    181%
```

**Part I is complete: chapters 1–17, 199 printed pages against a 266-page estimate (75%).**
Part II is complete: chapters 18 to 39 come to 475 pages.
**Part III has begun** with chapter 40, the first chapter in the book that calls a real model, and
the labs now run on the corpus in `labs/corpus/` — 40 documents, 8 queries and 320 graded
judgements, written for the book and dedicated to the public domain. `LEDGER-DEFECTS.md` entry 63
is what the first non-deterministic chapter cost: prose that quotes a figure a re-run can change
is false the moment anything re-embeds, and no gate can see it. **Chapter 41 puts chapter 20's
statistics on real replies** — 180 trials, five graders, five verdicts from the same data — and its
lesson is about the instrument rather than the result: the grader written to be fair to one prompt
forgave the only instruction the other broke, and the headline score never showed it. **Chapter 42
runs the measurement chapters 21, 22 and 23 all defer**, and its lesson is the same shape one level
down: a strict mode can enforce that a part code exists, by compiling your catalogue into the
request, and then it orders a kettle filter for a chair — a grammar can only redirect where your
code can refuse. 753 printed pages of chapters. Chapters 30
to 33 are the evaluation run of the part, and the first chapters since 17 whose material is a
method rather than a mechanism. Their reviews find more per chapter than the mechanism chapters'
did, and almost all of it is the same defect: a claim one notch wider than its demonstration.
**Chapter 38 is where that pattern turned inward**: its review found ten things and every one was
real, but the pass that checked the *repairs* found four of eleven unsound — the fourth chapter
running at roughly that rate. Two of the four were an arithmetic slip and a doubled em dash, which
is why `LEDGER-DEFECTS.md` entry 57's grammar half now names reading the sentence rather than the
diff, and why entry 60 exists at all: chapter 38's own subject, `pass^k`, is a string pandoc
silently turns into a superscript, and the only symptom was two overfull boxes. Chapter 26
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
