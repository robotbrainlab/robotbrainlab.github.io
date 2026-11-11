# The two books that come after Modern AI Engineering

Recorded 2026-10-31, at the owner's request, **before any table of contents is written.**

Nothing in this file has been started. No chapter, no outline, no folder of its own. The owner
asked for the decisions and the rules to be settled first, because the first book's rules were
established as it went and that cost rework.

## What is being built

Three books in one body of work, read as one path. The first exists; the other two do not.

| # | Book | State |
|---|---|---|
| 1 | **Python** — the language from fundamentals, against the roadmap that already exists at `data-intelligence/books/python-roadmap.html` | Not started |
| 2 | **Core Machine Learning and Deep Learning** — everything up to language models, **including the mathematics** | Not started |
| 3 | **Modern AI Engineering from Zero** | **Finished**, 2026-10-31. Lives in `_book/`. 57 chapters, 4 appendices, 1,413 printed pages |

Book 3 is the one already written, so the work remaining is books 1 and 2.

## Decisions

| # | Decision | Reason | Rejected |
|---|---|---|---|
| 1 | **Write both books, in the same way the first one was written** | The owner asked for it twice and the reason below carries it | Writing neither and pointing at existing books instead — see decision 4, which is why that was wrong |
| 2 | **The reason is the language, not the content** | The owner: *"the language we used in the book is the main reason, many books or references do not use that simple language."* The material exists; the material in plain, controlled language does not. That is the same justification the first book had | Treating "a good book exists" as settled, which confuses the content being available with it being readable |
| 3 | **No deadline** | The 31 December 2026 deadline belonged to Modern AI Engineering, which was written for interviews. The owner will go into interviews on experience and that book. These two are a learning library and are not interview preparation | Carrying the interview deadline across to books that are not for interviews |
| 4 | **They may be large and academic** | Said explicitly by the owner. Size is not a constraint and rigour is wanted. The combination that matters is **academic in that language** — derivations in short sentences, every step shown, nothing behind *it can be shown that* | Keeping them small to fit a deadline that no longer applies; or writing them academic in the register academic books normally use, which is the thing being fixed |
| 5 | **Mathematics is included, inside book 2** | The owner's decision on 2026-10-31. An academic machine-learning book needs real linear algebra, calculus and probability, and book 1's chapter 8 was deliberately the minimum. Book 2 carries its own mathematics rather than assuming a source | Pointing at an outside mathematics source, or a fourth book for mathematics alone |
| 6 | **Python first, then Core ML and Deep Learning** | Dependency, not risk: book 2 assumes you can already write code and run experiments. (The earlier argument for this order was deadline hedging, which decision 3 removed) | Writing book 2 first because it is the more interesting one |
| 7 | **Book 2 closes chapter 17's thirteen gaps rather than naming them** | Book 3 has a hard rule — mathematics yes, machine-learning and deep-learning theory no — and its chapter 17 lists thirteen things it refused by name, with chapter 56 naming the books that cover them. Book 2 sits on the other side of that boundary, so the list is a spine that is already written | Starting book 2's outline from scratch, and re-teaching what book 3 taught |
| 8 | **Nothing is drafted until the rules are written and the table of contents is approved** | The owner asked for the rules to be established before any outline. The first book's rule was *nothing is drafted until TOC.md is approved*; this adds a step before it | Starting the Python outline today, which was offered and declined |

## The rules still to be written

This is the next piece of work, and it has not been done. What it has to settle:

- **A shared ledger across the three books**, so book 2 does not re-teach or re-define what book 3
  taught. Book 3's own `LEDGER-TAUGHT.md` stopped chapters contradicting each other inside one
  book; across separate books nothing watches at all, and the commonest defect found while writing
  book 3 was two pieces each internally sound and jointly contradictory.
- **Where the mathematics boundary now sits**, since decision 5 moves it. Book 3's
  `BOOK-GUIDE.md` §6 draws a line that book 2 is meant to cross, so book 2 needs its own line
  drawn in its own terms.
- **Which of book 3's gates transfer unchanged**, which need changing, and which do not apply.
  The machinery in `_book/tools/` is reusable and is the part that took longest to get right.
- **What a chapter of an academic book in this language looks like** — the structure spec. Book 3's
  chapter shape was built for an interview reader and Part IV changed it once already.
- **How the three books are read as one path**, which is what the owner asked for: everything in a
  single place for reading.

## Where this came from

The owner asked for the two books. The first answer given was an objection on three grounds, and
it is recorded here because the project records rejected alternatives and because the objection
was wrong in an instructive way:

1. **Book 3's own rule** — write a from-zero guide only where no good resource exists and the wall
   has been hit twice — was applied by reading *good resource exists* as *the content exists*. The
   rule is about information being available. Readability was treated as free.
2. **The deadline**, which decision 3 shows did not apply to these books.
3. **A measurement used against a question it does not answer.** The objection cited *classical
   machine learning came up in 10 of 54 interview accounts* to argue the material did not warrant a
   book. That figure measures what is **asked**. Book 3 makes the point itself that the most-asked
   question is not the most-revealing one. Using it to decide whether the owner should understand
   the material is the failure book 3's own defect ledger is full of — a claim argued from the
   wrong measurement.

The owner's reason in decision 2 settled it.
