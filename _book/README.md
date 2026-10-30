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
| III · Apply | 40–50 | 190 | **Done** — 11 of 11, 2026-10-30 |
| IV · What Next | 51–57 | 136 | **Drafting** — 2 of 7 done |
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
  48  1015-1101   87   12    725%
  49  1102-1155   54   16    338%
  50  1156-1205   50   18    278%
  51  1207-1233   27   36     75%
  52  1234-1254   21   24     88%
  53  1255-1285   31   20    155%
  54  1286-1322   37   26    142%
  55  1323-1339   17   16    106%
   A  1340-1368   29    -       -
   B  1369-1374    6    -       -

57 chapter(s), 1368 printed pages
```

**Part I is complete: chapters 1–17, 199 printed pages against a 266-page estimate (75%).**
Part II is complete: chapters 18 to 39 come to 475 pages.
**Part IV is 5 of 7.** Part III is complete: chapters 40 to 50, which began with chapter 40, the first chapter in the book that calls a real model, and
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
discards every edit when one fails to match.

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

**Chapter 55 is the book's one synthesis, and it owns nothing — which the build proves rather than
the prose claiming it.** It carries zero index entries, and regenerating the glossary and the cheat
sheet with it in the book leaves both byte-identical: no term, no measurement, no figure of its own.
It has no program either, because its subject is what you can say with a whiteboard. It answers the
question *design a support assistant that answers from a company's own documents; talk me through it*
in **seven moves**, and its thesis is that the order is the content: the architecture is the third of
the seven, and the first, second and last are where the conversation is decided — all three being
refusals. Move two, *say how you would know it worked*, comes before the architecture on purpose, and
that single reordering is most of what the chapter teaches.

**Three places where this book's own measurements contradict the standard answer.** *We would use
hybrid search* is what everybody says, and chapter 45 found fusion measurably worse than dense at
chunk granularity, −0.120 recall and −0.156 nDCG. *Find the biggest failure mode and fix it* is the
standard move, and chapter 46's seventeen failures cannot support a ranking. And the back-of-envelope
arithmetic reproduces chapter 49's $0.11 a thousand from its own token counts, turns it into **$19.80
a month**, and prices the reranker you were about to add at about twice the request it improves — for
a gain chapter 45 could not tell from zero.

**Its reviews were the sharpest of Part IV, because a chapter of quotations is a chapter of chances
to misquote.** Sixteen findings then six. The one worth the entry: the chapter states chapter 45's
measurement correctly in move three — the average length falls from 161.8 terms a document to 37.7 a
chunk — and then nine printed pages later priced the reranker on the *document* figure, which was the
whole basis of a five-times conclusion that is really about twice. **`LEDGER-DEFECTS.md` entry 96** is
that class: a source with two figures of the same kind must be quoted by its qualifier, not by its
chapter, and when the wrong one of two turns up, the repair is to find the quantity you actually need
rather than to swap in its neighbour.

**Chapter 54 is the chapter the provider wrote half of.** Failure, and its spine is that *nothing in
my code changed* is almost always true and almost never relevant: the model behind a name, your
documents, the service under load and your own standard all move, and the only one that announces
itself is a retired snapshot's 404. Three measurements, and two of them needed no provider to do
anything. **Of the ninety-five name groups in one account's listing, thirty-nine carry a dated
snapshot and fifty-six carry none** — both embedding models among them, which is the problem chapter
43 pointed here. `gpt-4o` answers with the August snapshot while November is listed beside it, so a
floating name is not the newest; and a listed dated snapshot returns HTTP 404, so **the listing is
not a statement of what you can call**.

**Then the measurement to take to work: you can run a provider's update today.** `gpt-4o` has had
three dated snapshots and two still answer, so chapter 41's thirty cases and its grader, unchanged,
with only the snapshot different. **Three cases of thirty moved and the score difference of −0.100
ran from −0.200 to +0.000** — it cannot be told from zero, which is chapter 33's reason to report
cases and never a score movement. And reading them is the chapter: `Three years` became `3 years`,
`60` became `60 W`, `Seven` became `7`, and **every one of those answers is correct**. So are all
five of the older snapshot's failures. Both snapshots answer all thirty correctly and the grader
rejects five and eight on notation alone — which makes a regression a claim about the model and the
grader together, and makes *a case that passed now fails* a trigger that needs a second clause
saying somebody reads it.

**The third is the bolded item in its plan.** A half-migrated index lost about forty per cent of its
nDCG with nothing erroring, and it made no difference which encoder the query path used, because
**ten of ten results came from the half matching the query's own model** — two embedding spaces do
not align, so the other half is absent rather than mis-ranked. Its review also corrected the
chapter's arithmetic twice, and `LEDGER-DEFECTS.md` entry 95 is the second: **a fix that adds
evidence is a drafting event, and the count describing the new evidence gets written while looking
at it** rather than computed from it.

**Chapter 53 is the chapter whose subject caught it out twice.** Cost, and its spine is one line
— `(in - cached) x p_in + cached x p_cached + out x p_out` — which is the arithmetic chapters 34
and 37 both counted tokens and handed over, because the cached term is what makes a token count
rank two designs one way and the bill rank them the other. Reconciled against chapter 49's own
dollars to the ninth decimal over 144 requests, it says that **output is a tenth of the tokens and
over a third of the money**, and 68 per cent of it on one of three shapes in the same system. Then
the chapter's own measurement, and it is the one figure in the book that is a column of a single
number: asked three arithmetic questions at four effort settings, a reasoning model's **visible
reply is 10 to 13 tokens in all 72 calls** while the bill multiplies by up to sixteen and 96 per
cent of the dearest setting's output is never sent to you. A cap set below the working returns an
empty string with the whole cap billed and a finish reason of `length`. And the cheapest condition
on a cascade turns out to be the money one — a sixteenfold price gap puts the break-even
escalation rate at 0.94, which no real rule reaches — so the argument that decides it is the
quality one, which is what sank chapter 49's.

**What it got wrong is the part worth reading the record for.** The absolutes check found that
*the only way to get cost attribution is to record the counts* is false, because a key or project
per feature makes the provider's own breakdown the split; the fix added that route and left the
chapter's bolded opening sentence stating the narrow claim it refutes, fourteen lines above. The
fix for *that* introduced an off-by-one pointer. `LEDGER-DEFECTS.md` entry 94 is those three
generations: **a fix that widens a claim has a sweep of its own, and what you grep for is the
narrow claim rather than the new words.** Its companion in the same entry is a thousandfold unit
error — `$1.8792` written as *a dear call* when a function named `per_1k` computed it — which
survived four sites because $1.88 is a plausible price for one call and $0.0019 looks like nothing.

**Chapter 52 is the chapter that took its own headline back.** Speed, and its spine is that
*slow* is four complaints sharing almost no lever: nothing appears for seconds, the words crawl
once they start, it is usually fine and sometimes awful, or every call is quick and the whole
thing is slow. The first is prefill and the queue, the second is decode, the third is three
decisions of your own — a concurrency limit, a retry, a timeout — and the fourth is your
pipeline. Then the lever menu, held by which number each one moves: **sending less** is the only
one that touches both waits and the memory without handing you a different model to re-measure;
**streaming** leaves the total alone, moves the first-token wait down to prefill, and is what
makes that number measurable at all, since no log holds it; a **response cache** of your own is
the only lever that removes the call, and its key has to carry the caller's scope or Chapter 51's
authorisation section is undone. If you serve the model yourself there are four more, and
**speculative decoding** is the one worth the space: a small model proposes, the large one checks
them all in one read of its weights, and under the correct acceptance rule the output is a sample
from the large model's own distribution — so it spends the arithmetic slack that being
memory-bound leaves you, which is the opposite trade from continuous batching.

The one thing it measures is a latency budget, computed from the requests Chapter 49 recorded and
left on disk. **The identity `total ≈ ttft + tpt × (tokens − 1)` holds to a median 0.6 per cent
over 72 of them**, which turns a product target into a cap: a two-second target at the 95th
allows about 114 chunks on the essay shape, which sends 356. And on one 24-request arm the median
is 1.31 seconds, the mean 1.74, and **only three of the twenty-four are slower than the mean** —
so the statistic every dashboard shows describes a request that almost never happens.

Two rounds, 24 findings then 17, and both of the worst were about the same paragraph. The review
found the chapter concluding that *no* reply length meets a two-second target on one of the
shapes, off a 95th percentile that is the twenty-third request of twenty-four — ten lines after
the chapter itself says a tail that thin is an anecdote. The fix was to make the program
bootstrap it. **The fix-verification pass then found that the fix reasoned the way the book has a
section forbidding**: it put an interval round each arm and eyeballed the overlap, where Chapter
20's *Overlapping Intervals Are Not the Test* says the interval goes round the difference. The
data was paired, so the right test was in the file the program already read, and all three
differences contain zero. `LEDGER-DEFECTS.md` entries 92 and 93 are what that cost, and **93 is
the one to read: a repair is held to the standard the chapter is held to.**

**Chapter 51 opens Part IV, and it is the framework chapter 50's lab was the experiment for.**
Seven earlier chapters point at it by name, and what it owes them is one rule: **a model cannot
reliably tell an instruction from data**, which is not a defect better models close but a
property of a component with no channel for metadata. From that follow the two jobs the chapter
actually asks of a reader. Write down every channel by which text neither you nor your code
composed reaches the model — the request, a retrieved passage, a tool result, a tool
*description*, a document's own title, a note the agent wrote, a sub-agent's return, a
compaction summary — because the list is short and nobody has it. Then apply the rule that is
about combinations rather than components: **never combine untrusted input, sensitive access and
external action in one session without approval.** Any two are ordinarily survivable; the three
together give injected text something to ask for and a way to send it, and the four fixes are
removing one, shrinking one, or adding the approval — which is the weakest wherever the action is
frequent, because volume turns review into rubber-stamping.

The rest is the decisions, each made once and each checkable: model output as input to whatever
renders or executes it, where the ordinary escaping and parameterising of web and database work
is the whole answer; a tool acting with the caller's rights rather than the service's, which is
the sixth cause chapter 5's lab dramatised and said this chapter owned; sandboxing what the
model wrote, because a validator reading generated code for safety is a judgement about text
standing where a limit should be; a third-party tool server as a supply-chain dependency on four
counts; what a guardrail is worth, which is the attacks it knows and a failure logged rather
than served; and where a secret lives. It also prints the field's two risk lists and then argues
that a list is a checklist and never a certificate — eight of the LLM list's ten entries changed
number in a single edition, and on the day this was written two numberings were in circulation
on the project's own site.

Two review rounds, 30 findings then 13, and the first found something that reached backwards:
chapter 50 and `LEDGER-TAUGHT.md` row 50 both gave the successful payload's size as 159
characters inside 1,162, which is the arm that got zero — the one that fired is 178 inside 1,181
— so chapter 50 was reopened with `chapter.py amend` to correct it. The second round then found
three errors in the repairs themselves, all in borrowed material: chapter 29's post-filtering
arithmetic kept its answer and lost its input, and chapter 20's rule about repeats was stated
more strongly than chapter 20 states it. `LEDGER-DEFECTS.md` entries 89 to 91 are what that is
worth, and **90 is the one to read: carrying another chapter's finding is quoting it, and a
quotation keeps its variables and not only its answer.**

**Chapter 50 closes Part III by attacking the system the part built.** An instruction goes into
the three places this system reads text it did not write — a retrieved passage, a tool result's
title and the notes store from chapter 48 — and what varies is what the instruction *asks for*,
because that is what turned out to matter. **One cell of twelve fired, on four of four questions.**
Asking for a marker in the reply got nothing in 72 runs across two forms; asking the system to call
an invented tool got nothing in 36; asking it to *stop* citing its passages worked every time. The
rule it took away was the one rule in the system with no code behind it, and the reply from a
successful attack is the finding: correct prose, correct carriers, an empty citation list — **what
is missing is not visible in what is there.** The fix is four lines, it catches all twelve, and it
**prevents nothing**: by the time your code sees the reply the citations are gone, so what it buys
is that the failure is logged rather than served. Chapter 46's regression set, run on that same
reply, passes it on all five checks.

It took two review passes, 20 findings then 15, and the first of them is the one worth the
ledger. **The chapter described three channels that did not exist**: a title lifted from a YAML
header the pipeline had none of, chapter 48's store that was two notes typed by hand with
`store48.py` unimported, and one injected copy where the code appended to every retrieved chunk.
Every gate in this book passed, because the assembler proves no figure was transcribed and nothing
reads a sentence against the function it describes. All three were implemented as written and the
156-call grid run again; the result did not move. The same pass found the file's "invariant" gate
could not fail — it asserted on a stored boolean, and a dispatcher that runs anything still passed
it — and that the chapter's citation check is scored against its own predicate, so its 12 of 12 is
a definition. `LEDGER-DEFECTS.md` entries 86 to 88 are those three, and 88 is the one to read:
**splicing a program's output proves the figures and says nothing about the prose describing the
program.**

**Chapter 49 is the chapter that measures three levers and recommends none of them.** Time to first
token, time per token, prompt-prefix caching and a cheap-model cascade, priced on this book's own
system. Every one fails for a reason that is a fact about the traffic rather than about the lever:
the cache has a minimum prompt length and these requests are under it; the wait at these lengths is
a queue, so quadrupling the prompt moves nothing an eight-pair comparison can detect; and the model
sixteen times the price answers the same 12 of 12, so the cascade pays twice for the same answers.
What it delivers instead is a baseline — **$0.11 per 1,000 requests at a median 1.31 seconds** —
which `TOC.md` says chapter 53 measures against, and three priced refusals. It also owns bank
question 90, *how did you reduce cost per request*, and answers it with the measurement rather than
a story.

Two review passes, 15 findings then 15, and the chapter's own subject turned out to be its biggest
risk. The timing run's first version put each shape in a block, so the shape and the moment it ran
were one variable, and it reported a 0.23-second effect with an interval clear of zero that was the
running order — **a confound in a timing measurement looks like a result with a tight interval.**
The review then found that step 4's whole narrative was fiction (no reply hedged; the escalation
rule fires on `cannot` inside correct refusals), that an answer key demanded the opt-in route where
the documents make account credit the default, that the counts tripled the evidence because the
cheap model's three trials are byte-identical, and that the caching lever was priced off the very
arm the chapter spends a page condemning. `LEDGER-DEFECTS.md` entries 83 to 85 are what the fix
round then cost: a ratio computed from a rounded display, a Summary still leaning on a test the
body repudiates, and **a figure quoted from a summary table when the claim was about one row.**

**Chapter 48 goes back and measures what chapters 35 and 36 said they had not.** Both were
unusually honest about their own evidence — chapter 35 labelled its compaction finding a
demonstration on two hand-written summaries and even named its own doubt, and chapter 36 wrote its
candidate sets into its programs as judgements — so this chapter runs all three claims on one real
agent over the shipped corpus. **Chapter 35's claim is refused and the doubt it could not test is
the finding**: the must-keep list is crossed by polarity *and* by whether a fact carries a number,
and what clears zero is form — not one prose fact survived a single naive summary, 0 of 96
observations against 53 of 108 for facts with a number — while polarity is +0.15 from −0.257 to
+0.548. Its *advice* survives anyway, in one cell: the warning takes negative-and-prose from 0 to
35 per cent and moves nothing else by more than eight points. **Provenance shown to the model
corrected nothing** in eighteen runs, and 3 of 54 runs opened a document in any arm with both
tools available throughout — so chapter 23's rule about who can refuse holds one level down, about
a fact instead of a tool call. And **chapter 36's six things for a description came to one line**:
three of five versions are identical on every column, so the list of ids is the whole effect, and
its worked defect occurred once in 120 runs because a search returning ids the reader accepts
makes a resource choosable rather than nameable.

What it cost is on the record. Two review passes, 23 findings then 13, and **the worst of each was
mine.** The completeness review found that six of forty probe sets were satisfied by the case
statement alone, which every summary restates — so they scored their fact kept without testing
anything. The fix-verification pass then found that the repair's own exclusion had been applied in
one place and not in every place that reads the data, so two ungraded facts entered a mean as
zeros. Between them those two defects moved one headline from +0.43 to +0.21 and turned the central
result over. `LEDGER-DEFECTS.md` entries 79 to 82 are what that is worth, and entry 81 is the one
to read: **a probe can be satisfied by text that is not the fact, and every rule you have about
*when* you wrote the probe is silent about it.**

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
