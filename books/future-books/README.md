# Python, and Machine Learning and Deep Learning

**The two books still to be written.** `[2026-11-12]` This file was called *“The two books that
come after Modern AI Engineering”*, which is true of the **writing** order and the opposite of the
**reading** order — they are read first and written last. That is the same confusion the book
numbering caused, so the title says the names instead.

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
| **Python** | The language from fundamentals, built against the Fundamentals stage of the roadmap at `../../data-and-intelligence/books/python-roadmap.html` | **Started 2026-11-12.** Contents approved, reviewed and corrected: `../python/TOC.md`, 51 chapters. **No chapter drafted** — decision 8's other half, the rules, is unwritten. `../python/CLAUDE.md` governs a session there |
| **Machine Learning and Deep Learning** | Everything the AI-engineering book black-boxed, **including the mathematics**, and **including transformers in full** | Not started |
| **Modern AI Engineering from Zero** | The finished one. 57 chapters, 4 appendices, 1,413 printed pages | **Finished** 2026-10-31. `../modern-ai-engineering-from-zero/` |

**Reading order is Python, then Machine Learning and Deep Learning, then Modern AI Engineering
from Zero.** The finished book is read last and was written first, which is the whole reason the
other two exist.

## Why these books exist

**`[STATED 2026-11-12]` This is the purpose, in the owner's own words, and every other decision in
this file is tested against it.** It was said on 2026-11-12 and was **not** written down until he
asked whether everything had been noted.

> *"I already have three years of professional experience. However, I want you to **assume that I
> am starting from zero, with no prior knowledge of the subjects**. The reason is that I have
> relied heavily on AI-assisted tools for most of my professional work, so I do not want my years
> of experience to be mistaken for a strong understanding of the underlying concepts.*
>
> *In fact, **this is the sole reason I am creating these three books** and committing to learning
> these subjects properly. I want to move beyond depending on AI-assisted tools and develop the
> knowledge, understanding, and independent problem-solving ability that I currently lack."*

And what success looks like, in his words: *"My goal with these books is to develop a thorough
understanding of AI and its foundational subjects. I want to build a strong foundation first, and
once I have achieved that, I intend to start reading other books independently to deepen my
knowledge further."*

**Three things follow, and they are not decisions — they are the standard decisions are judged by.**

1. **Assume zero knowledge of the subject. Do not assume zero ability.** He has shipped software
   for three years. Every term is defined and nothing is inherited from that experience — but a
   book that re-explains what a function is, or walks him through something a lab already had him
   do, is spending the one thing he is short of. **Zero knowledge, full competence as a reader.**
2. **The test of these books is whether he can read the next book without them**, not whether they
   contain everything. That is what *"start reading other books independently"* asks for, and it is
   the argument that decided decision 11.
3. **He is employed.** *"The main reason I am building these three books is because of my time
   constraints."* Time is the binding constraint on everything here — which is **not** a licence
   to cut understanding, and **is** a reason to prefer a hand-checkable example over an exhaustive
   derivation.

**Decision 2 is a different reason and both hold.** That one says why a *new* book rather than the
existing ones: the language. This says why he is doing it at all.

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
| 10 | `[STATED 2026-11-12]` ***Python* assumes *Linux and Git from Zero* and is built against the roadmap's Fundamentals stage** | The owner: *"I like the second option, but book should be made in accordance with the fundamentals level in the python roadmap which is in the website."* So the book starts at the first Python program, names the owner's own published book as the prerequisite, and takes its scope and exit criteria from the Fundamentals stage at `../../data-and-intelligence/books/python-roadmap.html` — not from the Advanced or Mastery stages. **The table of contents is to be discussed separately and is not settled here.** `[2026-11-12]` **This row was written before anyone had read what the Fundamentals stage contains** — it is **six phases, 49 projects and three capstones**: 1.1 The Language, 1.2 Writing It Properly, 1.3 How Python Really Works, 1.4 Concurrency, 1.5 Applying Python, 1.6 Capstones. Decisions 15 and 16 say what the book does with them. **`[STATED 2026-11-12]` RULED, and it goes further than this row did:** asked whether *Python* should keep a short Git chapter for the Python-specific part — what to ignore, branching for a refactor, rebase before a pull request — the owner said **drop it**, and added *"make sure you point to the Linux and Git Book."* **So the prerequisite is not a note in a preface; it is a pointer the book repeats where the ground would otherwise be covered twice** — `../python/TOC.md` carries it in the header, in Part I's opening note and in chapter 55's closing table. **One roadmap project is orphaned by this and is named rather than lost:** `1.2 p9`, interactive rebase, which *Linux and Git from Zero* covers only in brief | Teaching the shell, the editor and version control again from zero, which duplicates a published book; or scoping the book to the whole roadmap, all three stages |
| 11 | `[STATED 2026-11-12]` **Show the working that makes a thing work. Name the rest and say where it is** | The owner re-opened his own October rule — *"size is not a constraint and rigour is wanted… every step shown, nothing hidden behind it can be shown that"* — because he is employed and short of time. **The honesty half stays, unchanged and without exception**; it costs almost nothing, because the honest alternative to deriving something is a sentence naming it. **The exhaustive half is dropped**, on his own stated goal: he wants to finish these and then read other books by himself, and a book that leaves him nothing to do builds reliance on itself instead. **The replacement is `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §6, which survived 57 chapters** — a declared line, a list of what is never taught, named boundary cases that may not be widened, and a closing chapter listing everything black-boxed — together with its real instrument: *"Every mechanism chapter carries a worked numeric example small enough to check by hand… This is what stops an explanation from becoming a metaphor that dies on the first follow-up question."* | Showing every step always, which is longest and teaches dependence on this book; or writing short and deepening on request, which changes the book while it is being read |
| 12 | `[STATED 2026-11-12]` **Topics are tiered: some taught, some noted — and the split goes to the owner before anything is written** | He asked the right question before agreeing: *"will there be a chance of missing core topics?"* **The honest answer is yes, and it has already happened here** — robotics was cut at step 4 by a stage that declared no total, so nothing it dropped could be counted (`../modern-ai/docs/LEDGER-DEFECTS.md` entry 5a). Three things bound the risk, and all three already exist: a cut is a written row with a reason, never a silence; **the owner rules on the split**, because he is never handed an unrecommended list; and the drill detects a noted topic that turns out to be load-bearing, since it is read to judge the book and never the reader. **The alternative hides the risk rather than removing it**: a book taught at full depth everywhere is one he may not finish, and it then misses every topic past the page he stopped on, with nothing recording which. **His words: *"I can go with your recommendation, hope you will teach all the core topics."* A hope is not an instrument, so decision 13 gives it a test.** | Everything at equal depth, which is the biggest book and says nothing about what to read first; or core only with the rest cut, which is the silent loss he is trying to avoid |
| 13 | `[2026-11-12]` **"Core" is a test, not a judgement: a topic is TAUGHT if anything else in the book rests on it** | Decision 12 rests on somebody deciding what *core* means, and *"I hope you will teach all the core topics"* cannot be checked. This can: **if a later chapter needs a topic in order to be understood, that topic is taught — no exceptions, no matter how dull.** Everything else is a candidate to be noted, and is proposed as such with its reason. **The test is reviewable**, because the dependency is a fact about the book rather than an opinion about the field. `[I RECOMMEND]` until the owner rules on it — he asked for the commitment, he has not yet seen this form of it | Leaving *core* to my taste, which is unreviewable and is how robotics was cut |
| 14 | `[STATED 2026-11-12]` **The size of *Modern AI Engineering from Zero* is PERMISSION, never a target** | The owner: *"I am okay with the same book size as the Modern AI book."* That book runs to 1,413 printed pages. **This settles that a large book is acceptable. It settles nothing about what goes in one.** `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §11 point 6 names the exact failure to avoid here, found in its own chapter 45: **deciding scope by the page count and then justifying it on other grounds** — *"when a scope argument arrives at the same time as a page worry, the page worry is the one to distrust."* So this figure may never be cited for including something, for excluding something, or as progress | Reading it as a target, which would make the page count the scope rule the owner has twice forbidden |
| 15 | `[STATED 2026-11-12]` ***Python* teaches the language twice, as the roadmap does** | The roadmap teaches 1.1's ground again at depth in 1.3, deliberately, and makes it the one hard ordering: *"1.1 before 1.3, because 1.3 is a second pass over the same ground."* It calls 1.3 *"the hinge of everything here"* and says *"Most self-taught developers never arrive here — which is exactly why they plateau."* **A book would normally merge the two.** The owner kept them apart: first pass to get him writing Python, second to show him why it behaves that way. **The repetition is the mechanism, not a redundancy to optimise away**, and decision 14 has already permitted the length | Teaching it once deeply, which removes the thing the roadmap says works; or a short second pass, which decides in advance which parts surprise a reader |
| 16 | `[STATED 2026-11-12]` **Phase 1.6 is SET as work. Phase 1.5 is split** | 1.6 is three capstones — *"the three things you point at when someone asks what you've built"* — and **a capstone you read is not a capstone**, so the book sets it rather than teaching it. **1.5 is not the same case, and the first version of this row said it was.** 1.5 calls itself *"a vehicle, not a subject"*, but its reading list carries real subject matter: SQLite and SQL, *Use the Index, Luke!*, SQLAlchemy, Alembic, Postgres, Pydantic, httpx, tenacity, FastAPI, password hashing and the OWASP API top ten. **Decision 17 says what happens to it.** For HTTP and API design the book points at `../apis-to-fastapi/` — which is **what the roadmap already does**, naming *APIs to FastAPI* ch. 1–8 as a reading item inside 1.5 | Teaching web frameworks and APIs again in the book's own words, which rewrites eight chapters of a published book; or dropping both phases, which loses the part of Fundamentals that makes the rest stick |
| 17 | `[STATED 2026-11-12]` **The book teaches SQL and databases properly** | The owner was given four options and chose this one. **Nothing he owns covers SQL**, and `../../.claude/HANDOVER.md` already names it: *"The one known gap in Python Fundamentals is SQL. Phase 1.5 opens with five database items, and *Use the Index, Luke!* ch. 1–5 assumes you can already write a join. The failure is silent — a missing index doesn't error, it gets slow later."* **The roadmap says so itself**, in its *What's Not Here* appendix: SQL — *"Joins, indexes, transactions, query plans. **If you learn one thing here, learn this**"* — and under *Covered here?* it answers *"Partly — Phase 1.5 covers enough to build with."* **The one thing it says to learn is the one thing it only partly covers.** A silent failure is the worst kind to leave to a pointer. HTTP and API design are not in the same position, because a book of his already covers them | Pointing at outside SQL material, which leaves the gap his own notes call silent; teaching all of 1.5, which duplicates a published book; or a separate databases book, which is a fourth book to write |
| 18 | `[STATED 2026-11-12]` **Both books use the finished book's chapter shape, exactly** | The owner: *"we have solid information on how the book should be and the chapters should be. Follow exactly from the book already we built. I really love the book."* **So `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §5 “Every chapter” is the spec, copied, not reinvented**: an opening paragraph saying what the chapter gives; *The problem.* and *The question.*; the idea explained before any command or code, with an everyday picture where it helps; every new term bolded and carried into that chapter's `### Key Terms` table, which **is** the glossary; `tip` / `note` / `warning` callouts; **a lab with expected results**; then `## Summary, Key Terms, and Review Questions`, with an optional `### Worth Memorising` for numbers, defaults and formulas only, and 4–6 review questions; and `> **You understand this when** …`. Each part opens with a **“What to ignore for now”** note. **This settles two open rules at once**: the chapter shape, and whether the roadmap's projects become labs — **every chapter has a lab, so they do** | Designing a chapter shape from scratch for books whose reader has already read 57 chapters of this one |
| 19 | `[STATED 2026-11-12]` **Everything transfers, not only the chapter — the owner overruled my recommendation** | I proposed keeping the chapter shape and leaving three things behind: Appendix B's interview bank, Part IV's four threads, and the part names. **The owner ruled against all three**: *"I would prefer having it all, the whole point is for occupation, isn't it."* **He is right, and my reason for excluding the interview bank was wrong.** Its own spec says an answer is *"what the reader should be able to say in about sixty seconds: the mechanism, the trade-off, and how they would check it"*, written **last, from the finished chapters, never from memory**. **That is an instrument for exactly the purpose at the top of this file** — it tests whether he can explain a thing without looking it up, which is what *independent problem-solving ability* means. It serves employability and understanding at once; I had treated them as alternatives. **The four threads transfer too**, asked of each book's own subject, and **the part names transfer as a default** — with one limit below | Keeping only the chapter, which was my recommendation and which he rejected |
| 20 | `[STATED 2026-11-12]` **The part NAMES are a default, not a constraint, and structure still follows the subjects — and the default has now bent once, with the owner's ruling.** **RULED for *Python*:** shown the three options in `../python/TOC.md`, he chose the new names — **Write It · Why It Works That Way · Build With It · What Next**. Only *What Next* survives from the four. The reason is decision 15: the roadmap deliberately has the reader write Python in phase 1.1 before phase 1.3 explains it, so *Understand* would describe 1.3 and mis-describe 1.1. **Decision 19 is not overturned** — the interview bank, the four threads and the chapter shape all still transfer, and *Linux and Git from Zero* keeps all four names, correctly, because its material does arrive in that order. **The ruling is for *Python* only**; *Machine Learning and Deep Learning* gets the same four names as its default and the same test | Decision 19 carries Understand / Use / Apply / What Next across. **The one thing that cannot follow is the division of material into them**, because *Python*'s material arrives in the roadmap's six phases and the machine-learning book's arrives as chapter 17's list. So the names are the starting shape and the **contents decide whether they survive** — `../modern-ai/docs/GOAL.md` §5.3's rule, *structure follows the subjects*, applies here as it does there. **This is not a disagreement with decision 19**: it says when the default would have to bend, and the owner rules on that when he sees the contents | Fixing the four names before the contents exist, which chooses the shape before the material is known |
| 21 | `[I RECOMMEND 2026-11-12]` **Which KINDS of topic get a short entry** | The owner asked *“for what type of topics you will do this?”* **Decision 13 is the test and it does not change: a topic is taught if anything else in the book rests on it.** A short entry is therefore never a judgement that something is unimportant — it is the statement that **nothing else here depends on it**. Five kinds come out that way, each with its own examples: **(1) A sibling the book does not build on** — another model family or another tool doing the same job. Machine learning: graph neural networks, Gaussian processes. Python: Django and Flask, which the roadmap already rules on — *“Framework collecting … pick one and go deep”*. **(2) What a source the book follows already says to skip** — Python: writing your own pytest plugin, where the roadmap says *“skip only ch. 15 (writing them)”*; the C API and metaclass authoring. **(3) What belongs to a later stage** — Python: descriptors, metaprogramming, variance and performance, which the roadmap puts in Advanced, and CPython internals, which it puts in Mastery. **(4) What cannot be built or checked on the owner's machine** — machine learning: behaviour that appears only at a scale nobody here can reach, interpretability that needs the actual weights. This is the route `../modern-ai/docs/GOAL.md` §10 already keeps open for a subject that fails the buildable test. **(5) An open research question** — which the finished book's chapter 17 already handles this way: *why depth helps* is listed as *“An open research question. Not a settled account being withheld”*. **And what is NEVER a short entry: anything another part of the book needs.** That is the test, it is a fact about the book rather than an opinion about the field, and the owner or anyone else can check it. **`[2026-11-12]` The five kinds are NOT a second rule, and saying so matters** — they are the shapes that come out when the one test above is applied, listed so the answer can be seen before the contents exist. The owner did not follow this row until it was put that way, and a reader who takes the five kinds as the rule will start sorting topics by category instead of asking the only question that counts: **does any later part of this book need it?** | Deciding it by how interesting or fashionable a topic is, which is unreviewable and is how robotics was cut |

| 22 | `[STATED 2026-11-12]` **When *Python* is finished, three things happen at once** — the CS&E on-ramp points at the book instead of the roadmap page | The owner reversed half of his own *"Literally nothing"* ruling of the same morning, and said so plainly: *"I had previously said that there would be absolutely no changes to the roadmap. Well, I guess this is one exception!"* **What changes: one `href`.** `../../cse/index.html` line 235 carries the Software Engineering Track's *Programming Language From Zero: Python* entry, pointing at `../data-and-intelligence/books/python-roadmap.html`; it points at the book's PDF instead. **The entry's own title does not change** — decision of 2026-10-29, the topic is the language and Python is the instance. **It is conditional: nothing moves until the book is finished**, and until then the link stays exactly as it is. `[STATED 2026-11-12]` **The other two consequences of the same moment**: the on-ramp entries drop their *Coming soon*, and *Machine Learning and Deep Learning* becomes session kind 3 in `../../.claude/CLAUDE.md`, which carries the exact label to use. **The trigger is the owner saying the book is finished, not a built PDF** | Leaving the on-ramp pointing at a reading path once a book of his own covers the same ground; or retiring the roadmap page, which he ruled against and has not reopened |
| 23 | `[OPEN 2026-11-12]` **The Data & Intelligence guide's links to the roadmap page are NOT covered by decision 22, and are far more expensive** | Decision 22 names the CS&E on-ramp only. **The guide is the other half, and it is not one link: 10 of its generated pages carry the roadmap page**, placed there by `../../utilities/build-di-guide.py` through two separate mechanisms — `PYTHON_SWAPS` repoints the 4 pages that tell a reader what to read now, and `NOTE_PAGES` adds a dated note to 7 pages that record earlier work, **each checked to match exactly once, so the build exits rather than publish a page it did not recognise**. **Changing that side means editing the build script and re-running it, not editing a link.** And `../../.claude/HANDOVER.md` records why the 7 note pages were left alone: renaming the resource in them *"would claim that work examined something that did not exist yet"* — an argument that applies to the book as much as it did to the roadmap. **The owner has not ruled on this half** |


**`[2026-11-12]` How decisions 15 to 17 were nearly got wrong, recorded because it matters.** The
first version of row 16 was written from regular expressions run over
`../../data-and-intelligence/books/python-roadmap.html` — patterns that pulled out windows of text
around phase numbers, which were then read. **The owner caught it.** `../../.claude/CLAUDE.md`
makes reading rather than pattern-matching a standing rule for every session in this repository,
and it had been committed two commits earlier. Reading the page in full then showed what the
windows had hidden: 1.5's reading list, and with it SQL. **The first row would have dropped SQL
from the book without naming it** — the same shape of loss as robotics, in a different book.

**Then the owner asked for the HTML itself to be read, not a stripped copy of it. That was read
too, and it confirmed the corrections rather than changing them again** — and added two things the
stripped text had flattened. **1.5 links *APIs to FastAPI* as a relative path to this repository's
own PDF**, so the roadmap already serves that book to a reader on the live site. And the *What's
Not Here* appendix answers decision 17 directly, in the roadmap's own voice.

**`[2026-11-12]` One fact from that reading answers the owner's practicality worry directly.** The
roadmap sets its own ratio: *"Aim for 20% reading, 20% drills, 60% building — about 1:3, reading
to building."* **A book is the reading.** So by the roadmap's own design the *Python* book is about
a fifth of Fundamentals, and the rest is building, which no book does for him. It also says *"Read
the project list as a specification, not an assignment"*, and *"A phase is finished when its phase
project is finished and you could explain it to someone else."* **And it lists the inversion as a
failure**, under *What to skip*: *"Reading this page instead of writing code — the ratio should be
roughly 1:3 in the fundamentals… never the other way round."*

**`[2026-11-12]` One more thing the roadmap already settles, and it bears on why these books exist.**
Its *How to Practise* section does not contain the practice, deliberately: *"There is far more of it
than any document could hold, and the right amount differs for every reader. **Generate it
instead.**"* The generator it names is an LLM — **used under rules it writes out**: never give a
solution to something not attempted first, never use a feature from a later phase, point at the
documentation rather than asserting, and ask what was already tried instead of answering. **That is
worth separating from the dependence the owner wants to end.** An assistant that writes the code is
the thing he is trying to stop needing; one that sets problems and refuses to answer early is the
opposite of it. **Whether the *Python* book carries drills of its own, or sends the reader to that
section, is open** — see the rules below.

**`[STATED 2026-11-12]` The tables of contents are deferred, for both books, deliberately.** The
owner: *"we can discuss the Table of Contents (TOC) later, but not right now."* **So a session
does not open by offering one, and does not draft one.** Decision 8 already bars drafting a
chapter before a table of contents is approved; this is the step before that — **the table of
contents itself is not on the table yet**, and the work in front of it is the rules below.

**He raises it when he is ready.** Offering it unasked has already been declined once (decision 8's
rejected column). **`[2026-11-12]` What is settled before it** is decisions 11 to 14: how much
working an explanation shows, that topics are tiered, what makes a topic core, and that a large
book is permitted rather than aimed at.

### `[STATED 2026-11-12]` He raised it. The deferral above is spent for *Python*

**Same day, later: *"After that we will start with the Python book, once Python book is completely
done we will go to ML&DL book."*** That is him raising it, which is the only thing the paragraph
above was waiting for. **`../python/TOC.md` was drafted on that instruction**, approved, then
reviewed twice and corrected — its *What the review found* section records fourteen faults in the
approved list.

**The deferral still stands for *Machine Learning and Deep Learning*.** Nothing about that book's
contents has been raised, offered or drafted, and a session does not open by offering one.

**`[2026-11-12]` And decision 8's other half is still unmet, which the contents list now says in
its own status line.** Approving a table of contents satisfies one of decision 8's two conditions.
**The rules below are the other**, and they are not written. **So nothing is drafted yet** — not
because the contents are unapproved, but because this section is unfinished.

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
  **`[STATED 2026-11-12]` Narrowed, by the owner, and no longer blocking.** He ruled that a
  mechanism cannot differ between books — *"it's like saying 2+2 will differ in explanations"* —
  and he is right. **What is left is vocabulary and cross-references**, not correctness: a word
  used two ways, or one book claiming the other covers something it does not. **So this is a
  running list kept while writing, not a document to finish first.** The section *"The two books
  may be written IN PARALLEL"* at the end of this file holds the full ruling and the evidence.
- **Where the mathematics boundary now sits**, since decision 5 moves it.
  `../modern-ai-engineering-from-zero/docs/BOOK-GUIDE.md` §6 draws a line that the machine-learning book is meant
  to cross, so that book needs its own line drawn in its own terms.
- ~~**Which of the finished book's gates transfer unchanged**, which need changing, and which do
  not apply.~~ — **`[STATED 2026-11-13]` CLOSED by the owner**, who read the proposal and ruled
  *"you can go ahead with your recommendations."* **The ruling is `../python/GATES.md`**, tool by
  tool: five transferred unchanged, eleven changed, three do not apply, and two are new. The
  machinery is built and lives in `../python/tools/`.
  **This was the last live item on this list for *Python from Zero*, so decision 8's second
  condition is now met and drafting is unblocked.** Everything else still open below belongs to
  *Machine Learning and Deep Learning*, or is a running list kept while writing.
  **One rule the owner added in the same sitting**: *a gate must prove it read something* — every
  gate prints how many files it read, and a gate that read zero files fails. He approved it after
  three of the finished book's own gates were found to be reporting success over nothing.
- ~~**What a chapter of an academic book in this language looks like**~~ — **`[2026-11-12]` CLOSED
  by decision 18**: the finished book's chapter shape, copied exactly. Decision 19 names the three
  things above the chapter that do not come with it.
- **`[2026-11-12]` What a NOTED topic looks like on the page** — **the last of the three that
  block a contents list, and decision 18 nearly settles it too.** The finished book's chapter 17
  is the form at book scale: a table of *what you cannot explain* · *where you met it* · *what it
  actually is*, closing with *“a boundary you can recite is a boundary you can defend”*.
  **`[STATED 2026-11-12]` The owner approved the table**, shown to him with worked rows: four
  columns — what this book does not teach · where you met it · what it actually is · where to read
  it — as the closing chapter of each book. **The second column is the point**: you met it, so the
  book did not hide it. **What is left open is which topics go in it**, which decision 21 answers
  in kind rather than by name.
- ~~**`[2026-11-12]` What happens to the roadmap page once *Python* exists.**~~ — **`[STATED
  2026-11-12]` CLOSED by the owner: literally nothing.** He was given three options — leave it and
  decide later, repoint it at the book, or retire it — and answered *"Literally nothing"*. **The
  page stays exactly as it is, permanently, and the book does not touch it.** So the page and the
  book say the same thing in two registers on purpose, which is consistent with decision 9 letting
  books overlap. **Nothing about `../../data-and-intelligence/books/python-roadmap.html` or the
  two pages linking to it changes when *Python* ships** — the Data & Intelligence guide and the
  CS&E on-ramp both keep their links as they are. **This is not a deferral and it is not to be
  reopened as one.**
  **`[STATED 2026-11-12, later the same day]` HALF OF THIS IS REVERSED, by the owner.** His words:
  *"once the new Python book is finished, we'll replace the existing Python roadmap in the CSE
  on-ramp roadmap with it … I actually made this decision today, even though I had previously said
  that there would be absolutely no changes to the roadmap. Well, I guess this is one exception!"*
  **The original wording above is left standing**, because the project records a reversed decision
  rather than rewriting it. Decision 22 carries what now holds.
- ~~**Whether the 49 phase projects become the book's labs**~~ — **`[2026-11-12]` CLOSED by
  decision 18**: every chapter has a lab with expected results, so they do. **What is left is
  smaller**: which roadmap project feeds which chapter's lab, which is drawn with the contents and
  not before.
- **`[2026-11-12]` How a noted topic becomes a taught one.** Decision 12 says the drill detects it.
  Nothing yet says what happens next: whether it is written into the book in place, added as an
  appendix, or held for a second edition.
- **How the books are read as one path**, which is what the owner asked for: everything in a
  single place for reading. **`[2026-11-12]` This is bigger than it was when it was written.** The
  file then named three books. `../README.md` now lists eight, and one of them — *RAG from Zero*,
  added 2026-11-12 — opens by assuming *"You write Python and have called an API before"* and no
  machine learning at all, which places it between the two unwritten books. **The path has to say
  where every published book sits, not only these three.**
- **`[2026-11-12]` Where *Machine Learning and Deep Learning* starts at the bottom.** Decision 9
  settled its top edge exactly. **Nothing settles its floor**: whether it opens from no machine
  learning at all, and whether it assumes *Python* or stands alone there too, the way decision 9
  made it stand alone at the top.
- **`[2026-11-12]` What mathematics floor that book writes from.** Decision 5 says it carries its
  own mathematics. From school algebra? From nothing? The answer changes how much of the book is
  mathematics. **`[STATED 2026-11-12]` Deferred by the owner — *"for now, math is not a problem"*.
  It cannot block anything: *Python* is written first and needs no mathematics decision.** Settle
  it before the machine-learning book's contents are drawn, not before.
- **`[2026-11-12]` What the deliberate overlap means in practice**, now that decision 9 allows it.
  Two books will teach attention. The rule has to say what each is allowed to assume of the other,
  what a reader who reads only one gets, and which book owns a term when both define it.

## `[STATED 2026-11-12]` The two books may be written IN PARALLEL, in separate sessions

**The owner said he might build *Python* and *Machine Learning and Deep Learning* at the same time,
in two Claude Code sessions, and asked for the conflict risk to be recorded before it happens.**

**Each book's own folder is safe.** Two sessions writing `books/python/` and
`books/machine-learning/` cannot collide there. **Everything below is what they share**, and every
one of them is a real way to break the other session's work.

### The five shared things, and the rule for each

| Shared | Why it is a hazard | The rule |
|---|---|---|
| **This file** | Both sessions record decisions here, in one numbered table. Two sessions appending row 22 is a guaranteed conflict | **Commit a change to this file on its own, immediately, and push it.** Never hold an edit to it across other work |
| **`../latex/`** — `preamble.tex`, `Makefile`, `latexmkrc`, `front/`, `tools/`, `assets/` | **One build serves every book.** A change to the shared preamble changes the other book's PDF silently, and `tools/convert.sh` and `filter.lua` turn Markdown into chapters for both | **Treat `../latex/` as frozen while two books are in flight.** A book needing a change there puts it to the owner as a change to *both* books. A book needing its own style adds `../latex/styles/<slug>.tex`, which is additive and safe — that is what `modern-ai-engineering-from-zero.tex` and `complete-software-engineering-guide.tex` already are |
| **`../README.md`** | Both add a row to the book index | One line each, committed with that book's first commit |
| **`../../.claude/CLAUDE.md`** and **`../../.claude/HANDOVER.md`** | Both sessions may register their book | Same rule as this file: on its own, immediately, pushed |
| **One git branch** | Two sessions committing to `main` means one push is rejected and the other session is mid-work. **The dangerous repair is a force-push** | **Pull before every commit. Never force-push.** If the two sessions are writing at the same time for more than an hour, give each its own branch and merge deliberately |

### The hazard that file discipline does NOT fix

**Decision 9 lets the two books overlap on purpose, and the ledger that would catch a contradiction
is still unwritten** — it is the first item under *The rules still to be written*. **Two parallel
sessions make that worse, not better**: each book can define a term its own way, teach the same
mechanism differently, and neither session will see the other's prose.

**So if the books are written in parallel, the shared ledger stops being a rule to write later and
becomes a precondition.** The commonest defect found while writing *Modern AI Engineering from
Zero* was **two pieces each internally sound and jointly contradictory** — inside one book, where
one author saw both. Across two books and two sessions, nothing is watching at all.

**`[I RECOMMEND]`** either write the shared ledger before the second session starts, or accept
that the two books will need a reconciliation pass afterwards and budget it. ~~**The owner has not
ruled on this.**~~ **`[2026-11-12]` He has now ruled. The two sections below say how.**

### `[STATED 2026-11-12]` SEQUENTIAL, so this hazard does not arise

**The owner will write *Python* first, finish it completely, and only then start *Machine Learning
and Deep Learning*:** *"we will start with the Python book, once Python book is completely done we
will go to ML&DL book."* That is decision 6's order, now confirmed as the **working method** and
not only as a dependency.

**So the condition this whole section is written against is false.** It assumes *neither session
will see the other's prose*. With sequential writing the second book is written against a finished
first one, which its session can read.

**Everything above stays, because the decision is reversible and the five shared things are still
real.** If the two books are ever in flight at once, the five rules in that table apply as written.

### `[STATED 2026-11-12]` Duplication stands — and the owner corrected my framing

He was asked to rule on the shared ledger and answered with an objection instead, which was right:

> *"How will the same concept differ in two books, explanation might be different, but topic is
> same it's like saying 2+2 will differ in explanations."*

**He is correct, and I had overstated the risk.** The paragraph above says each book could *"teach
the same mechanism differently"*. **A mechanism does not differ between books.** Attention's
arithmetic is the same arithmetic, and two books that disagreed about it would both be wrong — a
correctness defect that ordinary checking catches, not something a ledger is needed for.

**What two books can actually do is use a word two ways, or point at each other wrongly.** The
evidence is in the finished book rather than in my judgement:
`../modern-ai-engineering-from-zero/docs/LEDGER-TAUGHT.md` carries the row *"52's **model routing** is distinct from
**chapter 34's routing**, which is one call picking a branch; both chapters say so."* **One book,
one author, and "routing" still had to be disambiguated by hand.** The second kind is pure
bookkeeping: one book saying *the other covers this* when it does not.

**So the shared ledger is downgraded. It is not a precondition and it blocks nothing** — it is a
running list of terms and cross-references, kept while writing, in the form `LEDGER-TAUGHT.md`
already uses. The first item under *The rules still to be written* is amended by this.

**Recorded because this file records corrections.** I put a vocabulary risk to him as a correctness
risk, and recommended blocking work on it. **He refused the framing before he ruled on it.** That is
`../modern-ai/docs/GOAL.md` §11 class D — stating a claim above the strength of its evidence.

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
