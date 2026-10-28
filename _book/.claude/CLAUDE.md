# Modern AI Engineering from Zero — session instructions

## First thing in every session

Read these three files, in this order, before you do anything else:

1. `HANDOVER.md` — what this is, every decision and its reason, the current state, and what is
   blocked.
2. `BOOK-GUIDE.md` — the spec: structure, the maths boundary, Markdown and build conventions.
3. `TOC.md` — the plan: 57 chapters and 4 appendices, with page budgets, the
   concept-ownership table, and the writing-order table that is the schedule.

Then check `README.md` for the status of each part, and before writing any chapter read
`LEDGER-TAUGHT.md` (what the reader already knows — grep it for "Do not") and
`LEDGER-DEFECTS.md` (what the gates cannot catch).

**The chapter loop is a driver, not a habit:**

```bash
python3 tools/chapter.py begin NN-slug     # BEFORE the chapter file exists
python3 tools/chapter.py written NN-slug
python3 tools/chapter.py reviewed NN-slug
bash tools/check-all.sh                    # must end ALL GATES PASS
```

**Two things to do before the completeness review, every time, because both have been missed
in four chapters running:**

```bash
bash tools/check-all.sh 2>&1 | grep -E 'FAIL|GATES'   # never a tail: entry 35
grep -o '\\index{[^}]*}' latex/chapters/NN-*.tex | sort -u
```

Read every index entry and ask of each one: *is this a term, or did I bold it for emphasis?*
`verify-index.py` only catches an entry starting with a non-letter, so the rest is judgement, and
bold means **new term** in this book — see `LEDGER-DEFECTS.md` entry 33. Every chapter from 19 to
23 shipped junk entries to a reviewer because this was done after the review rather than before
it.

## The rules that are easy to break

- **Claude writes the book. The owner reads it.** Do not suggest that the owner writes it. This
  was decided and it was argued about once already.
- **The book never mentions a website, a roadmap, a learning path, numbered steps or tracks.**
  Every chapter stands alone.
- **Mathematics yes. Machine-learning and deep-learning theory no.** `BOOK-GUIDE.md` §6 draws the
  exact line, including the one boundary case.
- **Write maths as raw LaTeX, never as `$…$`.** See `HANDOVER.md` §5.
- **Never copy `book-template/preamble.tex` over `latex/preamble.tex`.** This preamble has three
  changes it needs.
- **Never push as the `dlakshmizlk` account.**
- **Nothing is drafted until `TOC.md` is approved.**
- **One chapter at a time. Never a part at a time.** Read its sources in full immediately
  before writing it. Writing several chapters in one stretch is how invention happens.
- **Two reviews per chapter.** The second reads only the changed passages, named.
- **A chapter is not done until its questions in `markdown/B-interview-bank.md` can be
  answered from it.** The hundred questions were written from `TOC.md` before any chapter
  existed, so they are the standard, not a summary. See `BOOK-GUIDE.md` §15.
- **Every applied fix is a sweep: grep book-wide, count before and after. Zero, or it is
  not done.**

## Style

Reply in plain, controlled English (about 80% ASD-STE100). Short sentences. Active voice. Give
the answer first, then what you did and decided, then the explanation. The owner asked for this
on 2026-10-22.

## Handover

@HANDOVER.md
