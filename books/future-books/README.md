# The two books that come after Modern AI Engineering

Recorded 2026-10-31, at the owner's request, **before any table of contents is written.**

Nothing in this file has been started. No chapter, no outline, no folder of its own. The owner
asked for the decisions and the rules to be settled first, because the first book's rules were
established as it went and that cost rework.

## What is being built

Three books in one body of work, read as one path. One exists; the other two do not.

**`[STATED 2026-11-12]` The books are named, never numbered.** This file used to call them book 1,
book 2 and book 3, and the owner had to ask what book 3 meant — it was the finished one, numbered
last because it is read last. **`books/modern-ai/CLAUDE.md` already carries the rule this broke:**
*"No internal codes or shorthand: name things."*

| Book | What it is | State |
|---|---|---|
| **Python** | The language from fundamentals, built against the Fundamentals stage of the roadmap at `../../data-and-intelligence/books/python-roadmap.html` | Not started |
| **Machine Learning and Deep Learning** | Everything the AI-engineering book black-boxed, **including the mathematics**, and **including transformers in full** | Not started |
| **Modern AI Engineering from Zero** | The finished one. 57 chapters, 4 appendices, 1,413 printed pages | **Finished** 2026-10-31. `../interview-prep/` |

**Reading order is Python, then Machine Learning and Deep Learning, then Modern AI Engineering
from Zero.** The finished book is read last and was written first, which is the whole reason the
other two exist.

## Decisions

| # | Decision | Reason | Rejected |
|---|---|---|---|
| 1 | **Write both books, in the same way the first one was written** | The owner asked for it twice and the reason below carries it | Writing neither and pointing at existing books instead — see decision 4, which is why that was wrong |
| 2 | **The reason is the language, not the content** | The owner: *"the language we used in the book is the main reason, many books or references do not use that simple language."* The material exists; the material in plain, controlled language does not. That is the same justification the first book had | Treating "a good book exists" as settled, which confuses the content being available with it being readable |
| 3 | **No deadline** | The 31 December 2026 deadline belonged to Modern AI Engineering, which was written for interviews. The owner will go into interviews on experience and that book. These two are a learning library and are not interview preparation | Carrying the interview deadline across to books that are not for interviews |
| 4 | **They may be large and academic** | Said explicitly by the owner. Size is not a constraint and rigour is wanted. The combination that matters is **academic in that language** — derivations in short sentences, every step shown, nothing behind *it can be shown that* | Keeping them small to fit a deadline that no longer applies; or writing them academic in the register academic books normally use, which is the thing being fixed |
| 5 | **Mathematics is included, inside *Machine Learning and Deep Learning*** | The owner's decision on 2026-10-31. An academic machine-learning book needs real linear algebra, calculus and probability, and chapter 8 of *Modern AI Engineering from Zero* was deliberately the minimum. This book carries its own mathematics rather than assuming a source | Pointing at an outside mathematics source, or a fourth book for mathematics alone |
| 6 | ***Python* first, then *Machine Learning and Deep Learning*** | Dependency, not risk: the machine-learning book assumes you can already write code and run experiments. (The earlier argument for this order was deadline hedging, which decision 3 removed) | Writing the machine-learning book first because it is the more interesting one |
| 7 | ***Machine Learning and Deep Learning* closes chapter 17's gaps rather than naming them** | *Modern AI Engineering from Zero* has a hard rule — mathematics yes, machine-learning and deep-learning theory no — and its chapter 17 names the whole of what it refused: eight things it black-boxed as it went, five more it never needed, and three subjects it calls outside itself rather than gaps (convolutional architectures, recurrent architectures, classical machine learning). **That list is a spine already written.** `[2026-11-12]` Decision 9 extends this: the list is the floor, not the ceiling | Starting the outline from scratch, and ignoring a boundary the finished book already drew |
| 8 | **Nothing is drafted until the rules are written and the table of contents is approved** | The owner asked for the rules to be established before any outline. The rule in *Modern AI Engineering from Zero* was *nothing is drafted until `TOC.md` is approved*; this adds a step before it | Starting the *Python* outline today, which was offered and declined |
| 9 | `[STATED 2026-11-12]` ***Machine Learning and Deep Learning* covers transformers in full, and stands alone** | Asked where the book stops, given that *Modern AI Engineering from Zero* already teaches a transformer's arithmetic by hand — tokens, the embedding table, attention, the stack, logits to a sampled word — and withholds only the *why*. The owner chose the widest of three options: **the architecture and its arithmetic again**, so a reader who opens this book alone is not sent to another one. **Overlap with *Modern AI Engineering from Zero* is deliberate and accepted** | Stopping before transformers, which would have made a clean seam between the two books; or teaching only the theory and leaving the forward pass to *Modern AI Engineering from Zero* |
| 10 | `[STATED 2026-11-12]` ***Python* assumes *Linux and Git from Zero* and is built against the roadmap's Fundamentals stage** | The owner: *"I like the second option, but book should be made in accordance with the fundamentals level in the python roadmap which is in the website."* So the book starts at the first Python program, names the owner's own published book as the prerequisite, and takes its scope and exit criteria from the Fundamentals stage at `../../data-and-intelligence/books/python-roadmap.html` — not from the Advanced or Mastery stages. **The table of contents is to be discussed separately and is not settled here** | Teaching the shell, the editor and version control again from zero, which duplicates a published book; or scoping the book to the whole roadmap, all three stages |

## The rules still to be written

This is the next piece of work, and it has not been done. What it has to settle:

- **A shared ledger across the books — and `[2026-11-12]` decision 9 changed what it is for.**
  It was written as *"so the machine-learning book does not re-teach what the AI-engineering book
  taught"*. **That is no longer the rule**: the owner has accepted deliberate overlap, so the
  ledger's job is now to stop the two books **contradicting** each other, not to stop them
  covering the same ground. `LEDGER-TAUGHT.md` stopped chapters contradicting each other inside
  one book; across separate books nothing watches at all, and the commonest defect found while
  writing *Modern AI Engineering from Zero* was two pieces each internally sound and jointly
  contradictory. **Two books teaching attention in two registers is exactly that risk, on
  purpose.**
- **Where the mathematics boundary now sits**, since decision 5 moves it.
  `../interview-prep/docs/BOOK-GUIDE.md` §6 draws a line that the machine-learning book is meant
  to cross, so that book needs its own line drawn in its own terms.
- **Which of the finished book's gates transfer unchanged**, which need changing, and which do not
  apply. The machinery in `../interview-prep/tools/` is reusable and is the part that took longest
  to get right.
- **What a chapter of an academic book in this language looks like** — the structure spec. The
  finished book's chapter shape was built for an interview reader and Part IV changed it once
  already.
- **How the books are read as one path**, which is what the owner asked for: everything in a
  single place for reading. **`[2026-11-12]` This is bigger than it was when it was written.** The
  file then named three books. `../README.md` now lists eight, and one of them — *RAG from Zero*,
  added 2026-11-12 — opens by assuming *"You write Python and have called an API before"* and no
  machine learning at all, which places it between the two unwritten books. **The path has to say
  where every published book sits, not only these three.**
- **`[2026-11-12]` What the deliberate overlap means in practice**, now that decision 9 allows it.
  Two books will teach attention. The rule has to say what each is allowed to assume of the other,
  what a reader who reads only one gets, and which book owns a term when both define it.

## Where this came from

The owner asked for the two books. The first answer given was an objection on three grounds, and
it is recorded here because the project records rejected alternatives and because the objection
was wrong in an instructive way:

1. **The finished book's own rule** — write a from-zero guide only where no good resource exists and the wall
   has been hit twice — was applied by reading *good resource exists* as *the content exists*. The
   rule is about information being available. Readability was treated as free.
2. **The deadline**, which decision 3 shows did not apply to these books.
3. **A measurement used against a question it does not answer.** The objection cited *classical
   machine learning came up in 10 of 54 interview accounts* to argue the material did not warrant a
   book. That figure measures what is **asked**. *Modern AI Engineering from Zero* makes the point itself that the most-asked
   question is not the most-revealing one. Using it to decide whether the owner should understand
   the material is the failure that book's own defect ledger is full of — a claim argued from the
   wrong measurement.

The owner's reason in decision 2 settled it.
