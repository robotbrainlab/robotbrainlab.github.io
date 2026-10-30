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
| III · Apply | 40–50 | 190 | **Drafting** — 8 of 11 done |
| IV · What Next | 51–57 | 136 | Not started |
| Appendices | A–D | 83 | **A (cheat sheet, 288 items), B (100 questions) and C (glossary, 274 terms) in the PDF.** A and C are generated from the chapters and gated; B's answers come as chapters land. D is the LaTeX index |

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
  16   184-195    12   18     67%
  17   196-203     8    8    100%
  18   205-216    12   16     75%
  19   217-235    19   20     95%
  20   236-255    20   18    111%
  21   256-270    15   14    107%
  22   271-285    15   12    125%
  23   286-301    16   16    100%
  24   302-314    13   14     93%
  25   315-328    14   12    117%
  26   329-358    30   28    107%
  27   359-381    23   16    144%
  28   382-403    22   16    138%
  29   404-423    20   14    143%
  30   424-442    19   14    136%
  31   443-467    25   18    139%
  32   468-492    25   16    156%
  33   493-518    26   16    162%
  34   519-541    23   16    144%
  35   542-568    27   22    123%
  36   569-599    31   18    172%
  37   600-625    26   10    260%
  38   626-652    27   14    193%
  39   653-680    28   22    127%
  40   682-706    25   20    125%
  41   707-731    25   18    139%
  42   732-760    29   16    181%
  43   761-789    29   16    181%
  44   790-820    31   22    141%
  45   821-885    65   22    295%
  46   886-970    85   18    472%
  47   971-1014   44   12    367%
   A  1016-1038   23    -       -
   B  1039-1044    6    -       -

49 chapter(s), 1038 printed pages
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
code can refuse. **Chapter 43 is the first chapter with real embeddings**, and what it found is
that chapters 24 and 25 argued with stipulated vectors crowded at 0.999 where a real model uses the
whole range: a sentence and its negation sit at 0.8158, not 0.99976, and chapter 25's bolded
arrangement claim half fails. It also found, in its own second review round, that two of its
printed ranks are decided by gaps smaller than the drift between two embeddings of one string —
`LEDGER-DEFECTS.md` entry 67. **Chapter 44 answers chapter 26's question and gets 26's own answer**: two of three
retrieval comparisons clear zero, and hybrid against dense is not one of them. Its three review
rounds also turned up the mechanical cause of a defect this ledger had recorded three times as a
habit of mind — `LEDGER-DEFECTS.md` entry 69, a batch of edits that writes once at the end and
discards every edit when one fails to match. 813 printed pages of chapters. Chapters 30
**Chapter 46 is the one to read if you only read one.** It runs chapters 30, 31 and 33 end to
end on eighty real answers and the method does not do what it is advertised to: forty outputs
hold eight failures rather than forty, seventeen failures give the six failure modes' *names* and
nothing about their *order*, and each of the four arguable labels changes the top of the table on
its own — two produce an order and the two orders point at different modes. The judge built for
the largest mode code cannot reach comes out thirty points **below** a judge that passes
everything, twice, under two instructions. And the regression set has two blind spots: chapter
33's, to cases that never failed, and one no number of cases fixes, to kinds with no check — which
is not hypothetical, because a correct refusal became the wrong product's price across both
versions and every check passed all six times. It took three review passes, 25 findings then 16
then 8, and `records/46-…` says which were mine.

**Chapter 47 is the chapter that caught itself.** It compares one step built as chapter 45's fixed
retrieval path and as chapter 4's loop, on twelve two-document tasks with three trials each, and
its completeness review found that the two designs differed in two ways rather than one: the loop
had been given a smaller per-search budget on my own reasoning that a loop accumulates several
searches' worth and so sees more in total. It mostly searched once — 29 of 36 runs — so the
budget was a handicap and not a trade. A third design was built, the same loop at the fixed path's
budget, and all 108 runs were made again. **The 44-point gap split into 28 points of budget and 17
of design, and neither half clears zero**, so the only comparison in the chapter with a verdict in
it is the one that confounds the two things it asks about. The diagnosis survives where the verdict
does not: 72 of 72 requirements were present in the fixed path's own passages against 63 and 54, so
retrieval was never the problem; all 72 loop runs ended by answering with 63 of them searching once
and four steps unspent, which is the opposite of a loop running away; and the agent's *total* input
tokens are lower than the fixed path's while its cost per success is nearly twice as high.
`LEDGER-DEFECTS.md` entries 77 and 78 are what it cost — a difference designed in on a prediction
about behaviour is a confound, and a resample cannot say what more data would show. Its
fix-verification pass then found entry 76's named example in the chapter written immediately after
that entry: a captured output file not re-run after its program changed.

**Chapter 45 is the capstone lab**: eight programs, the whole pipeline on the shipped corpus, and
every figure spliced from the programs' own captured output so none was retyped. It needed four
review rounds, because rounds 1, 2 and 3 each introduced errors — 20 findings, then 11, then 4,
then 1 — and `LEDGER-DEFECTS.md` entry 71 is what that cost: a round of fixes can invalidate its
own figures, and every new error was a prose claim about program output written without querying
the data first. What it found is worth the trouble: fusion loses to dense at chunk granularity and
the interval clears zero, which is the row chapter 26 refused and 44 could not call; the reranker
buys nothing tellable from zero at 105 model calls while the candidate set is the binding ceiling;
and chapter 28's neighbour expansion would have fixed both retrieval failures for a fifth of what
a deeper fill needed, because both missing passages sat in the row after one already sent. Its
closing result is the one to carry: **the diagnosis survived eight queries and the verdict did
not**, at +0.125 with 95 per cent from −0.250 to +0.500.

**All 44 earlier chapters were independently audited on 2026-10-30** — see `AUDIT-2026-10-30.md`.
One fresh agent per chapter, given only the chapter and told to find its own plan row in `TOC.md`.
**None was rated thin, none had content removed, and no arithmetic error was found in any chapter
that carries arithmetic**; in twenty chapters the agent also ran the programs and confirmed the
printed output byte for byte. Three real defects came out of it and are fixed: chapter 20's claim
that repeats never narrow a comparison interval, false and cited for method by ten chapters;
chapter 16's back matter asserting an accuracy claim its body refuses; and chapter 32's Worth
Memorising row saying what its own ledger row forbids. The audit's two open patterns are
unsourced evidence claims and corrections that reach the body and not the back matter.

Chapters 30 to 33 are the evaluation run of the part, and the first chapters since 17 whose material is a
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
