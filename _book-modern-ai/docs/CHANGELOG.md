# What Changed in This Edition

**This page is in the book**, not only in its machinery. It is the reader's only way to tell the
difference between learning something new and relearning something that has been revised — which
is the central hazard of a book that is revised rather than finished.

**It is generated**, from the operations each cycle applies (`PROCESS.md` §5.1). Do not write it by
hand: a hand-written changelog records what the writer remembers changing.

## The three kinds, and why the distinction matters to the reader

| Kind | What it means | What the reader should do |
|---|---|---|
| **New** | A subject that was not here before | Read it |
| **Revised** | The subject was here; its answer has changed | Read it again. What you learned may be wrong |
| **Overturned** | Something this book previously stated is now believed to be false | **Read it, and read why.** This is the most valuable row on the page |

**An overturned row is never deleted and never silently rewritten.** It carries the date it was
believed, the date it was overturned, and what changed the verdict. A book that quietly replaces
its claims teaches the current answer and hides the lesson about how answers change — and that
lesson is the one a research engineer most needs.

## The columns

| Column | What goes in it |
|---|---|
| `Cycle` | Which cycle made the change |
| `Kind` | new · revised · overturned |
| `Where` | Chapter, and section if narrower |
| `What` | One sentence, in the reader's terms, not the machinery's |
| `Why` | What changed the verdict — the new evidence, with its source |
| `Claims` | The `CLAIMS.tsv` ids involved |

## Cycles

### Cycle 1 — not yet run

No edition exists. The first entry appears when the first chapter closes.

## What also goes on this page, once per cycle

- **The operation counts**: how many `ADD`, `SPLIT`, `MERGE`, `RETIRE`, `NEW QUESTION` and
  `RECARVE` the cycle needed. These are the test on the structure itself: mostly `ADD` and `RETIRE`
  means the carving is sound; a `RECARVE` every cycle means it is wrong and the book should be flat.
- **What expired and was re-checked**: how many claims passed their review date, and how many came
  back verified, contested or superseded.
