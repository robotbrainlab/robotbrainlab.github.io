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
| 11 | `[STATED 2026-11-12]` **Show the working that makes a thing work. Name the rest and say where it is** | The owner re-opened his own October rule — *"size is not a constraint and rigour is wanted… every step shown, nothing hidden behind it can be shown that"* — because he is employed and short of time. **The honesty half stays, unchanged and without exception**; it costs almost nothing, because the honest alternative to deriving something is a sentence naming it. **The exhaustive half is dropped**, on his own stated goal: he wants to finish these and then read other books by himself, and a book that leaves him nothing to do builds reliance on itself instead. **The replacement is `../interview-prep/docs/BOOK-GUIDE.md` §6, which survived 57 chapters** — a declared line, a list of what is never taught, named boundary cases that may not be widened, and a closing chapter listing everything black-boxed — together with its real instrument: *"Every mechanism chapter carries a worked numeric example small enough to check by hand… This is what stops an explanation from becoming a metaphor that dies on the first follow-up question."* | Showing every step always, which is longest and teaches dependence on this book; or writing short and deepening on request, which changes the book while it is being read |
| 12 | `[STATED 2026-11-12]` **Topics are tiered: some taught, some noted — and the split goes to the owner before anything is written** | He asked the right question before agreeing: *"will there be a chance of missing core topics?"* **The honest answer is yes, and it has already happened here** — robotics was cut at step 4 by a stage that declared no total, so nothing it dropped could be counted (`../modern-ai/docs/LEDGER-DEFECTS.md` entry 5a). Three things bound the risk, and all three already exist: a cut is a written row with a reason, never a silence; **the owner rules on the split**, because he is never handed an unrecommended list; and the drill detects a noted topic that turns out to be load-bearing, since it is read to judge the book and never the reader. **The alternative hides the risk rather than removing it**: a book taught at full depth everywhere is one he may not finish, and it then misses every topic past the page he stopped on, with nothing recording which. **His words: *"I can go with your recommendation, hope you will teach all the core topics."* A hope is not an instrument, so decision 13 gives it a test.** | Everything at equal depth, which is the biggest book and says nothing about what to read first; or core only with the rest cut, which is the silent loss he is trying to avoid |
| 13 | `[2026-11-12]` **"Core" is a test, not a judgement: a topic is TAUGHT if anything else in the book rests on it** | Decision 12 rests on somebody deciding what *core* means, and *"I hope you will teach all the core topics"* cannot be checked. This can: **if a later chapter needs a topic in order to be understood, that topic is taught — no exceptions, no matter how dull.** Everything else is a candidate to be noted, and is proposed as such with its reason. **The test is reviewable**, because the dependency is a fact about the book rather than an opinion about the field. `[I RECOMMEND]` until the owner rules on it — he asked for the commitment, he has not yet seen this form of it | Leaving *core* to my taste, which is unreviewable and is how robotics was cut |
| 14 | `[STATED 2026-11-12]` **The size of *Modern AI Engineering from Zero* is PERMISSION, never a target** | The owner: *"I am okay with the same book size as the Modern AI book."* That book runs to 1,413 printed pages. **This settles that a large book is acceptable. It settles nothing about what goes in one.** `../interview-prep/docs/BOOK-GUIDE.md` §11 point 6 names the exact failure to avoid here, found in its own chapter 45: **deciding scope by the page count and then justifying it on other grounds** — *"when a scope argument arrives at the same time as a page worry, the page worry is the one to distrust."* So this figure may never be cited for including something, for excluding something, or as progress | Reading it as a target, which would make the page count the scope rule the owner has twice forbidden |

**`[STATED 2026-11-12]` The tables of contents are deferred, for both books, deliberately.** The
owner: *"we can discuss the Table of Contents (TOC) later, but not right now."* **So a session
does not open by offering one, and does not draft one.** Decision 8 already bars drafting a
chapter before a table of contents is approved; this is the step before that — **the table of
contents itself is not on the table yet**, and the work in front of it is the rules below.

**He raises it when he is ready.** Offering it unasked has already been declined once (decision 8's
rejected column). **`[2026-11-12]` What is settled before it** is decisions 11 to 14: how much
working an explanation shows, that topics are tiered, what makes a topic core, and that a large
book is permitted rather than aimed at.

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
  already. `[2026-11-12]` **Decision 11 settles the depth question inside a chapter; this is still
  open about the chapter's shape.**
- **`[2026-11-12]` What a NOTED topic looks like on the page**, now that decision 12 creates one.
  It is not a bare name: what the thing is, why it is not taught here, and where to read it. The
  finished book's chapter 17 is the worked example of this at book scale — *"a boundary you can
  recite is a boundary you can defend"* — and the per-topic form has to be written.
- **`[2026-11-12]` How a noted topic becomes a taught one.** Decision 12 says the drill detects it.
  Nothing yet says what happens next: whether it is written into the book in place, added as an
  appendix, or held for a second edition.
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
