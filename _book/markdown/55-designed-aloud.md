# A System Designed Aloud

Chapter 7 said this chapter is the only one that rehearses *saying* the material, and that saying it
is a separate skill from knowing it. Everything in it has been established somewhere else in this
book. What has not been established anywhere is the order you say it in, which is what forty-five
minutes and a whiteboard actually test.

*The problem.* They will give me forty-five minutes and a whiteboard and say "design this". I have
never had to say any of it out loud.

*The question.* In what order do I say it, and which parts do I refuse?

## The Answer, First

**Here is the whole of it, and the order is the content.** The question is the one this chapter is
built on: *design a support assistant that answers from a company's own documents; talk me through
it.*

| # | The move | About how long |
|---|---|---|
| 1 | Clarify the requirement, out loud, in questions | 5 minutes |
| 2 | Say how you would know it worked, before saying how it works | 5 minutes |
| 3 | The retrieval choice, with the reason | 8 minutes |
| 4 | The context, the prompt and the answer | 7 minutes |
| 5 | Cost per request, on the back of an envelope | 5 minutes |
| 6 | The failure modes, named | 5 minutes |
| 7 | What you would measure in week one, and what you would not build yet | 7 minutes |

Those add to forty-two, which leaves three minutes of the forty-five for the interruptions that are
the actual conversation. Treat the times as proportions rather than a schedule: what they say is that
the architecture is under a fifth of it.

**Almost everybody starts at move three.** The architecture is the part that feels like the answer,
it is the part that is pleasant to draw, and it is the part a weaker candidate can also produce. Moves
one, two and seven are where a conversation is actually decided, and all three of them are
*refusals*: refusing to design before the requirement is clear, refusing to describe a system before
saying how you would know it worked, and refusing to build the things that cannot yet be justified.

**And the second move is the one that reorders everything.** Saying *here is how I would measure it*
before *here is how it works* does three things at once. It commits you to a number, which is the
thing an interviewer can push on. It makes every later choice checkable rather than asserted —
"dense retrieval" becomes "dense retrieval, and here is the comparison that would settle it". And it
is the order in which the work is actually cheapest, because an evaluation set written after the
build is a set written to the build.

**One more thing before the moves, and it is about the speaking rather than the system.** Say the
figure and then say what it is a figure about. *Eleven cents a thousand requests* is worth little on
its own; *eleven cents a thousand requests, measured on a six-hundred-token prompt and a
forty-token answer at this month's prices for a small model* is a sentence somebody can argue with,
which is the point of saying it. Every number in this chapter but one is a number this book measured
somewhere, and each is named with its chapter so you can say where it came from — which is also the
honest answer to *how do you know*, and a better one than a confident round figure. The exception is
a published price in move five, and it is dated there for exactly that reason.

## Move One: What You Clarify, and Why It Is Not Stalling

The requirement as given is *answers from a company's own documents*. That is three unknowns
wearing a sentence, and there are five questions worth asking. Ask them as questions, not as
caveats — the difference between *I would need to know the volume* and *how many questions a day,
roughly?* is the difference between hedging and designing.

| Ask | Why it changes the design |
|---|---|
| Who is asking — customers, or the support team? | Decides whether a wrong answer reaches a customer, which decides how much of the next six moves exists |
| How many documents, and do they change? | Chapter 29's arithmetic turns on the first; Chapter 54's index migration on the second |
| How many questions a day? | Everything in move five, and whether the answer is a laptop or a cluster |
| What does the system do when it does not know? | The single highest-value question on this list |
| Is there anything it must never say? | Decides whether you are building a product or a product plus a review process |

**The fourth is the one to ask first if you only ask one.** *What should it do when it does not know*
is a product question that decides a technical one, and almost nobody asks it. Chapter 16 established
that a model's default behaviour is a plausible continuation rather than a refusal, so a system that
has no answer will produce one unless something stops it — and whether something should stop it is
not yours to decide. Chapter 30's failure modes include both *invents a detail* and *refuses when
the answer is there*, and the two are traded against each other by a decision somebody has to make.
Ask who makes it.

**And the first question is the one that scales the whole design.** A tool for the support team,
where a human reads every answer before a customer does, is a different system from one answering
customers directly: the second needs Chapter 32's groundedness verdict, Chapter 28's citations, a
refusal path and a review process, and the first needs retrieval that is good enough to save
somebody a search. Chapter 3's argument applies here with nothing added — the machinery exists
because the model alone cannot be held to an answer — and how much machinery depends entirely on who
is holding it.

**Then say what you are assuming, and move on.** The useful form is one sentence: *I will assume the
support team, ten thousand documents that change weekly, a few thousand questions a day, and that a
refusal is acceptable — tell me if any of those is wrong and I will say what changes.* That sentence
is doing three jobs: it unblocks the conversation, it invites the correction that makes the rest of
the answer relevant, and it demonstrates that you know which assumptions are load-bearing.

## Move Two: How You Would Know It Worked

Say this before the architecture. It is the move that distinguishes the conversation, and it is also
the one where this book has the most to say that an interviewer will not have heard from the last
four candidates.

**Start with the unit.** A case is one input plus whatever marks the answer right or wrong, which is
Chapter 20's definition, and for this system the input is a question, so a case is a question, the document the answer comes
from, and the answer. Chapter 41 built thirty of those on a corpus of forty documents and that is a
realistic first number to say: thirty cases, written by reading documents and copying answers out of
them, in an afternoon.

**Then the thing that makes thirty cases honest.** Chapter 20's arithmetic for a forty-case score at
0.70 gives one standard deviation of 0.072 over nothing but which cases you drew, so two of those is
**±0.14 spanning ninety-five per cent**. Say that out loud, because it is the difference between *we
will measure it* and *we will measure it, and here is what a set that size can and cannot see.* Then
say the part that follows from it and is not obvious: the way to compare two versions is on the same
cases, because a paired comparison cancels what the two versions share, and the width that remains
is the one that came from which cases you drew. And if you are asked how many cases it takes to
settle something, the honest answer is that it depends on how big the difference is — Chapter 20's
worked case is a difference where two hundred cases clear zero only seventy-two times in a hundred
and four hundred manage ninety-five.

**Then the grader, and this is where to be specific.** Chapter 41's finding is the one to carry:
*a grader is not a neutral instrument.* Its three graders disagreed on the same replies, one of them
rejected every one of the thirty replies of the prompt it was unfair to, and the grader written to be
fair to one prompt forgave the only instruction the other broke — with the headline score never
showing it. So the sentence to say is that you would write the grader against the cases before
seeing any replies, and read the rejected cases by hand the first time, because the first thing a
grader measures is itself.

**Then the two verdicts, kept apart.** Chapter 32 owns this and the distinction is worth stating
precisely because it is the one most often collapsed: *did the passages hold an answer* is a
retrieval question, and *is the answer supported by the passages it cites* is a generation question,
and a system can fail either with the other passing. Four cells, and each one has a different fix.
The cell that catches people is *the answer was there and the reply is wrong*, and Chapter 32 is
clear that finding more passages fixes none of those.

**And then the price, which is the part nobody says.** Chapter 30's method needs about forty failures
to name the failure modes, and Chapter 46 measured what that costs on a working system: eighty
answers held seventeen failures, so forty failures is about a hundred and ninety answers read, and a
hundred failures is about four hundred and seventy. **Say that number.** It converts *we would do
error analysis* from a phrase into a plan with an afternoon's cost attached, and it is the single
most useful figure in this move.

**Two refusals belong here.**

**A judge is not the first instrument.** Chapter 31 owns judges and its own measurement is the
caution: against a baseline that passes everything, which scored forty-eight of sixty on its set, one
judge reached eighty-five per cent while catching five of twelve failures, and the other caught ten
of twelve at the price of nine false alarms. Chapter 46 went further on real output: the two judges it built for
the largest mode code cannot reach scored 44 and 64 per cent, which is **50 and 30 points below** a
judge that passes everything — both of them worse than doing nothing. So the order is checks in code where code can decide, a judge only for
what code cannot, and a judge validated against your own labels before it is believed. Chapter 30's
figures are why the first part of that is not a compromise: a claim-support check caught twenty of
forty failures on its set and closed two whole modes, six of six and three of three.

**And a taxonomy on too few failures does not give you an order.** Chapter 46's seventeen failures
put two modes level at five each, the resampled gap ran from −0.353 to +0.353, and each of four
arguable labels changed the top of the table on its own — two of them producing orders that name
different modes. So *we would find the biggest failure mode and fix it* is a sentence to avoid.
*We would name the modes, and say how many answers it took, and not rank them until the ranking
survives a second reading* is the one that holds.

## Move Three: The Retrieval Choice, and Its Measured Reason

Now the architecture, and it is three decisions rather than a diagram.

**The shape first, in one sentence.** The documents are parsed and split once, each piece is embedded
and stored, a question is embedded at request time, the nearest pieces are fetched, and they go into
the prompt with the question. That is Chapter 2's arrangement with Chapter 27's indexing and
Chapter 24's embeddings inside it; say it quickly, because the interesting part is what you
choose inside it.

**Decision one: dense, and not hybrid, and here is the measurement.** This is the place to be
concrete, because *we would use hybrid search* is what everybody says. Chapter 26 owns the three
methods and the fusion of them, and it did something worth copying: it [**refused the verdict**]{.noindex} on
hybrid against dense and said whether it helps you is a measurement. This book then made that
measurement twice on its own corpus. Over whole documents, Chapter 44 found dense beating lexical by +0.223 nDCG
with the interval from +0.110 to +0.352, and fusion beating lexical by +0.195 from +0.111 to +0.300,
while **fusion against dense could not be told from zero** at −0.028 from −0.095 to +0.031.
Chapter 45 then ran the same comparison at the granularity a real system uses — over chunks rather
than whole documents — and got a verdict:

```text
  over chunks, eight queries, paired on the difference

    recall@5
      dense - lexical   +0.311   +0.118 to +0.489   clears
      fused - lexical   +0.192   +0.015 to +0.375   clears
      fused - dense     -0.120   -0.234 to -0.031   clears

    nDCG@5
      dense - lexical   +0.369   +0.167 to +0.571   clears
      fused - lexical   +0.213   +0.055 to +0.397   clears
      fused - dense     -0.156   -0.336 to -0.019   clears
```

**Fusion is measurably worse than dense alone there, on both measures.** That is a real result and it
needs its scope said in the same breath, in Chapter 45's own terms: this corpus, these eight
queries, *this lexical half*, at this granularity — and a mechanism that chapter names, which is
that reciprocal rank fusion gives each list an equal vote, so a weak list costs more the better the
other one is. It is not a claim that hybrid retrieval is bad. It is a claim that *we
would use hybrid* is a decision somebody should have measured, and that on the one corpus this book
measured it on, it lost.

**Decision two: keep a lexical lookup anyway, for a reason that is not the aggregate.** Chapter 25
owns the ways dense retrieval fails and the identifier is one of them; Chapter 43 planted one and
dense search got it wrong, which is a failure the mean hides entirely, because a product code is a
string that similarity has no reason to place near anything. Chapter 44 found BM25 winning a query on
exactly that shape. So the design that follows from both measurements
is dense as the ranking, with an exact lookup for identifiers routed round it — and the honest
caveat, said out loud, is that **this book measured the two retrievers and the fusion of them, and
did not measure that routing**, so it is a design suggested by the evidence rather than one
established by it.

**Decision three: how many candidates, and be exact about what depth buys.** Chapter 44 measured the
candidate set as a ceiling: at a depth of fifteen the best possible ordering reaches a perfect 1.000
and candidate recall is 0.984, so almost everything the key judges relevant is already in the set.
Going from ten candidates to fifteen raises what any reordering could win from 0.119 to 0.152 —
**the headroom goes up with depth, not down**, which is the counter-intuitive half.

**And the headroom is what a reordering could win, so in a design with no reordering stage it buys
nothing delivered.** The top five you send are the same five whether you retrieved ten candidates or
fifteen. So the reason to set the depth at fifteen is that it removes the ceiling, which is what
makes a reranker worth *measuring* later — and Chapter 44's own sentence is the one to carry into
that measurement: *measure the candidate set before you buy a reranker, because deepening it is a
parameter and improving a reranker is a project.* In that chapter the candidates *are* the
reranker's calls, which is how it prices depth — five more candidates is forty more model calls and
about another penny across its eight queries. Without a reranker they
cost a similarity comparison each, which Chapter 29 is the chapter that counts.

**And decision four is not a decision, which is worth saying too.** How the documents are split is
Chapter 27's subject and it is not a setting to pick on a whiteboard: Chapter 45 found a short chunk
taking rank one on a common word, with the mechanism being the average length falling from 161.8
terms to 37.7 rather than any rare term getting rarer. So *we would chunk it* is all you can
honestly say in five minutes, and the next sentence is that chunk size is a thing to measure against
the same graded key as everything else.

**And this is the one decision in the move where there is outside evidence about the answers people
give.** An interviewer who reports running about eighty conversations of this kind found that about
half of candidates defaulted to a fixed size and about a fifth could not define a chunk at all.
That is one account and Chapter 6's ladder puts it where such an account goes — it supports what
people *do* rather than what works. What it is good enough to settle is where the cheap marks are:
*fixed size, because the alternatives cost measurement I have not done* is a better answer than a
confident number, and being able to say what a chunk *is* puts you past a fifth of the room.

## Move Four: The Context, the Prompt and the Answer

Four things here, and the last two are the ones that make the system defensible.

**The prompt has four blocks and their order is a decision.** Chapter 18 puts them in the order
instructions, examples, format, then the supplied information — the unchanging part first by
construction — and Chapter 49 is why that ordering can be worth something beyond tidiness: a
provider that has already processed a leading run of tokens can reuse the work, and on the one shape
in that chapter long enough to qualify, the ordering was worth $0.19 per thousand requests. **Say
the limit in the same breath, because this design is on the wrong side of it.** The grounded shape's
prompt is about 612 tokens — move five uses exactly that figure — against a provider minimum of
1,024, so the prefix cache cannot fire here at all and the $0.19 is a saving this system earns
nothing of. **So the order is worth getting right now rather than worth money now** — free today, and
a change to every prompt in the system later, because the order is written into each of them rather
than configured once.

**The context is a budget, not a window.** Chapter 28 owns the arithmetic and the sentence to carry
is its own: a long window buys the room to be generous and does not remove the need to choose. The
budget is the instruction plus the question plus the passages against what you will send, and
Chapter 16's finding is why *send more* is not free even inside the window — a model's use of a long
context is uneven, and that chapter is explicit about the form that claim may not take. So the
spoken answer is a number: five passages, say, because that is what the candidate-set measurement
supports and because the budget has to be set somewhere you can defend.

**And then citations, which is where the design earns its keep.** Chapter 28 owns the mechanism and
is precise about its limit: three mechanical checks — does the cited document exist, is the quote in
it, is it at the locator claimed — are *necessary and not sufficient*, and what gets past them has
three distinct shapes rather than one. A real quote attached to the wrong claim. A statement with no
citation at all, which the checks never look at, because they only examine citations that exist.
And a quote the document's next sentence undoes. Saying that out loud is worth more than saying *we would add citations*, because it is the
difference between a feature and a check whose coverage you know.

**Then Chapter 32's verdict, with its unit named.** Whether the answer is supported is measured
claim by claim, and the unit is a decision about the measurement rather than a detail: Chapter 32's
worked answer scores three of six by claim and three of four by sentence, which is twenty-five
points of difference from the unit alone, and it does not run reliably in one direction. So the
sentence is *groundedness, by claim, and here is why the unit matters* — and if the room has not
thought about the unit, that is the most useful thing you will say in this move.

**One refusal belongs here.** A schema for the output is Chapter 21's and a strict mode is Chapter
22's, and both are worth having for the citation structure. What neither buys is correctness:
Chapter 42 is the measurement, where a strict mode enforced that a part code existed, by compiling
the catalogue into the request, and then ordered a kettle filter for a chair. A grammar can only
redirect where your code can refuse.

## Move Five: Cost Per Request, on the Back of an Envelope

This is the move where a candidate either has a method or has a feeling, and the method takes
ninety seconds. **Chapter 53 owns the formula and it is one line**: the cost of a request is its
fresh input tokens at the input rate, plus its cached input tokens at the cached rate, plus its
output tokens at the output rate. Everything below is that formula with this book's own measured
token counts in it.

**Start with one request, on figures that exist.** Chapter 49's grounded pipeline sends about 612
input tokens and gets about 38 back, on a small model priced at $0.150 and $0.600 a million:

```text
  one request, this book's own measured shape

    612 input tokens  x $0.150 a million   =  $0.00009180
     38 output tokens x $0.600 a million   =  $0.00002280
                                             -----------
    one request                               $0.00011460
    a thousand requests                       $0.11
```

**That $0.11 per thousand is Chapter 49's published baseline**, and the arithmetic above is how you
get there in front of somebody. Then turn it into the number the room actually wants:

```text
  2,000 conversations a day at 3 questions each

    requests a day        2,000 x 3  =    6,000
    requests a month      6,000 x 30 =  180,000
    at $0.11 a thousand                  $19.80
```

**Twenty dollars a month, and say it plainly, because the surprise is the point.** The model is not
what costs. Chapter 53's finding is the one to pair with it: cost is driven by multipliers that
somebody switches on, not by the price of a token, and the arithmetic for each of them is available
before you build it.

**Then price the stage you were about to add, which is the whole value of this move.** A reranker is
Chapter 26's cross-encoder arrangement: it scores the query against each candidate one at a time, so
its input is the candidates themselves. Sizing one pair is where the assumption goes, so say it out
loud. Chapter 49's own records put 8.625 retrieved passages in 2,285 characters, which is about 265
characters a passage and about 66 tokens by Chapter 10's four-characters rule; add the question and a
short scoring instruction and call a pair 90 tokens.

```text
  one reranking pass, fifteen candidates

    15 x  90 = 1,350 input tokens  x $0.150/M = $0.00020250
    15 x   5 =    75 output tokens x $0.600/M = $0.00004500
                                                -----------
    one request's reranking                      $0.00024750
    a thousand requests                          $0.25
    the whole request it improves                $0.11
```

**The reranker costs about twice the request it is improving**, taking the system from $0.11 to
about $0.36 a thousand — a little over three times — and Chapter 45 measured its gain as not
tellable from zero over 105 model calls. That is the sentence this move exists to let you say, and
it is a different kind of sentence from *reranking is expensive*: it is an estimate, with its
assumption named and its derivation said, next to a measurement of what it buys. **And say which
part of it is the assumption**, because somebody in the room may know their own chunk size and the
figure moves with it linearly.

**And the one-off costs are noise, which is worth knowing so you stop discussing them.** Embedding a
ten-thousand-document corpus at about 250 tokens a document is two and a half million tokens — which
is Chapter 43's own corpus scaled up, 9,740 tokens for forty documents. At the small embedding
model's published price on 30 October 2026, $0.02 a million, that is five cents, once. **That price
is the one figure in this chapter the book did not measure**, so it is the one to date out loud. The vectors themselves, at 1,536 numbers of four bytes
each, are about 61 MB. Chapter 43's own corpus is the measurement behind both figures and its
warning travels with them: *embed everything* sounds free and is not, at a million documents rather
than ten thousand.

```text
  building the index, ten thousand documents

    10,000 x 250 = 2,500,000 tokens x $0.02/M  =  $0.05
    10,000 x 1,536 x 4 bytes       = 61,440,000 bytes
```

**Three things to say about the whole estimate, unprompted.** Every price is dated and the
arithmetic is not — Chapter 1 says so and Chapter 49 writes its prices into a program for exactly
this reason, so what you are demonstrating is a method rather than a figure. The token counts are
this book's own measured ones and your corpus will differ, which is a reason to price your own
traffic rather than to distrust the method. And **people cost more than any of it**: an afternoon of
somebody's time is worth more than a year of the $19.80, which is the argument for spending the
afternoon on the evaluation set rather than on the reranker.

## Move Six: The Failure Modes, Named

**Naming them before you build is the move that most looks like experience**, and the reason it is
available to somebody who has not built this system is that Chapter 46 named them on one that worked.
Eighty answers from this book's own pipeline held seventeen failures, and the six modes they fall
into are the list to say out loud:

| Mode | Of 17 |
|---|---|
| Citation points somewhere else | 5 |
| Answers a neighbouring question | 5 |
| Answers for one case when two apply | 4 |
| Not an answer at all | 1 |
| Contradicts the passage | 1 |
| Citation does not support the claim | 1 |

**Say the two things that table says and the one it does not.** It says the failures are mostly about
*which question was answered* and *whether the citation holds*, not about the model inventing things,
which is where a room's intuition usually goes. It says the rate is near a fifth, which is the number
to plan a review process against. And what it does not say is an order: the top two are level at
five, Chapter 46's resampled gap between them ran from −0.353 to +0.353, and four arguable labels
each moved the top of the table on their own. So name the modes and refuse the ranking, in the same
breath.

**Then split the six by what can decide them**, because that split is the design decision the table
is for. Chapter 46 built code checks for three of its six: a citation that points somewhere else
(three checks — the id is a passage id, the passage was one of those sent, the quote is in it), a
reply that is not an answer at all (a stub test), and a claim contradicting its passage (every figure
in the answer appears in one). **Those three modes hold seven of the seventeen failures. The other
three hold ten.**

**So the majority of the failures are in modes no substring test reaches**, and naming them is the
useful half of this move. *Answers a neighbouring question* and *answers for one case when two apply*
are both replies that are true of something — just not of what was asked. And *citation does not
support the claim* is the one Chapter 46 is sharpest about: the quote is real, it is in a document
that was sent, and it does not establish the sentence it is attached to, so **nothing mechanical can
tell it from a good citation.** That mode needs Chapter 32's claim-level check, which Chapter 46
named and did not build, and that chapter calls the gap the clearest thing its own non-scope cost.

**Which gives the order for the checks, with Chapter 30's figures behind it.** Build the mechanical
ones first because they are cheap and they close a mode outright rather than denting it — Chapter 30
measured a claim-support check catching twenty of forty failures and closing two whole modes, six of
six and three of three, and a refusal detector catching seven with five in its own mode. Then a judge,
for the modes above that no code reaches, validated against your own labels first. **And say the rule
before somebody asks**: a check catches failures, not modes, so a mode covered in part is the
ordinary case rather than a disappointment.

## Move Seven: Week One, and What You Would Not Build Yet

### What you would measure in week one

Four things, and all four are fields rather than projects.

**Every request traced.** Chapter 33 owns the schema and the decision inside it: ids, counts and
timings on every request cost almost nothing and answer most operational questions, while the content
fields — the question, the retrieved passages, the answer — are what links a trace to a regression
case and are the ones to keep on a sample with a deletion window. Say the split; it is the difference
between having thought about this and having a logging library.

**The two latency numbers, and the first needs a decision.** Chapter 52's point is that the wait
before the first token is not in any log unless you asked for the reply as a stream and timed the
first piece of it — so *add streaming for the measurement* is a reasonable first move even where the
product has no use for words appearing one at a time. Report a middle and a tail rather than a mean:
on one of Chapter 49's twenty-four-request arms the median was 1.31 seconds against a mean of 1.74,
and on Chapter 52's reading of that same arm only three of the twenty-four were slower than the
mean.

**The three token counts and a label.** Chapter 53's rule is that a bill is only attributable if the
provider's own counts are recorded with something saying what the request was *for*, and that the
label is the one field nothing else can be derived into. One column, decided in week one, and
otherwise a month of traffic is a month you cannot account for.

**And three revisions on every request.** Chapter 54's versioned artefact: the model snapshot, a
revision of the prompt and configuration, and a revision of the index. Three strings, and the
difference on the day something breaks between an afternoon and a fortnight. **Read the model name
back out of the reply while you are there** — Chapter 40's one line, and Chapter 54 is why: a
floating name answers with whatever the provider points it at today, and on one probe `gpt-4o`
answered with a snapshot older than the newest one listed beside it.

### What you would not build yet

This is the last thing you say and it is the part that sounds most like judgement, because every item
is a refusal with a reason attached rather than a preference.

| Not yet | The reason, measured |
|---|---|
| A reranker | Chapter 45's gain was not tellable from zero over 105 model calls, and move five priced it at about twice the request it improves |
| Fused retrieval | Chapter 45 found fusion measurably *worse* than dense at this granularity, −0.120 recall and −0.156 nDCG |
| A cascade to a cheaper model | Chapter 49's cheap and capable models both answered 12 of 12, and the cascade cost 5.4 times the cheap one for the same answers |
| An agent loop | Chapter 47 established a method and a diagnosis rather than a ranking: its 44-point gap split into 28 points of search budget and 17 of design, and neither half cleared zero on twelve tasks |
| Several agents | Chapter 37's multiplier is duplication at 6.03 times one agent, or non-termination at 13.79 at a twenty-step limit — not the number of agents |
| A model judge as the primary instrument | Chapter 46's two judges for the largest mode code cannot reach came 50 and 30 points below a judge that passes everything |
| Fine-tuning | Chapter 39's division: retrieval supplies knowledge and tuning changes behaviour, and this requirement is knowledge |
| A hosted vector store | Chapter 54's retention reading: on 30 October 2026 vector stores and files were on the list of endpoints the zero-retention arrangement excludes |

**Say the shape of that list rather than reading it out.** Every row is a thing you would build
*after* the measurement that would justify it, and six of the eight have a measurement in this book
that failed to justify them — which is not the same as a measurement against them, and two of the
six are explicitly not verdicts: Chapter 47 established a method and a diagnosis rather than a
ranking, and Chapter 37's multiplier is about duplication rather than about the number of agents. The sentence that lands is the general one: **the cheapest step of any
lever is the one that finds out it cannot help you**, which is Chapter 52's rule, and it costs an
afternoon where building the lever costs a sprint.

**And one item is not on that list on purpose.** A refusal path — the system saying it does not know
— is in the first version, not deferred, because move one established that it is a product decision
and Chapter 16 established that the default is a plausible answer rather than a refusal. Deferring it
is deferring the only behaviour that bounds the damage.

## How to Say It

The content above is the easy half. Four things about the saying.

**Say the structure before you use it.** *I will clarify, then say how I would measure it, then the
retrieval, then the context, then cost, then the failure modes, then what I would watch and what I
would leave out* takes twenty seconds and buys the whole conversation, because the room now knows
you have not forgotten evaluation when you spend eight minutes on retrieval.

**Attach every figure to its measurement, out loud.** *About twice the request it improves, on
fifteen candidates at about ninety tokens a pair* invites the correction that makes the estimate
better, and somebody who knows their own chunk size will give it to you. A round
confident number invites the question *where did that come from*, and there is no good answer to it
except the sentence you could have said first.

**When you do not know, say what would settle it.** This is the single highest-value sentence in a
design conversation and it has a fixed shape: *I do not know, and the measurement that would tell us
is this, on this data, and it would take about this long.* Chapter 44's refusal is the model — it had
eight queries and a graded key and still reported *cannot tell* on one of its three comparisons, and
saying so is a stronger position than a verdict the data cannot carry.

**And know the two ways the conversation fails.** The first is going deep early: fifteen minutes on
chunking strategy is fifteen minutes not spent on the six moves that are left, and it reads as
somebody who optimises before measuring. The second is the opposite — staying at a level where
nothing can be wrong. *We would use a vector database and a good prompt* cannot be argued with and
also cannot be believed. The level that works is the one where every claim has a number or a named
check behind it, which is the level this whole book has been about.

## What This Chapter Has Not Told You

Five things, deliberately.

**Anything new.** This is the only chapter in the book that introduces no term, no measurement and no
figure of its own. Every number in it but one belongs to the chapter that measured it and is named
with that chapter, the exception being a published price that is dated instead, which is also the
honest answer to *how do you know* and the reason the chapter can be read
in an evening.

**The design that is right for your system.** The one above is right for the requirement in the
question and the assumptions stated in move one, and all four of the assumptions in move
one's closing sentence were invented there. Change *the support team* to *customers* and
Chapter 32's verdict, Chapter 28's citations and a review process stop being optional, which is
move one's own list — though none of move seven's eight deferrals moves, because every reason there
is about a measurement rather than about who is asking. Change *ten thousand documents* to *ten million* and
Chapter 29's index arithmetic becomes the first decision rather than an afterthought. Change *a few
thousand questions a day* and move five's $19.80 moves with it linearly. And withdraw *a refusal is
acceptable* and the system needs a different answer for the cases it cannot answer, which is the one
change that has no cheap version.

**How to run the conversation from the other side.** What an interviewer is listening for, how they
score it, what a follow-up question means: none of that is knowable from here, and a book that
guessed at it would be guessing. What is knowable is which claims in your own answer can be
defended, and that is what the seven moves are for.

**Anything about systems this book did not build.** Everything above is a retrieval system answering
from documents on one machine, which is what Part III built and measured. A system that writes to
other systems, holds a conversation over many turns, or acts on the world has failure modes this
book's measurements do not reach — Chapter 51's design rule is the nearest thing, and it is a rule
rather than a measurement.

**And the practice itself.** Reading the seven moves is not the same as saying them, which is the
whole premise of the chapter and is therefore worth stating as a limit rather than a hint. The
version of this that works is said out loud, to a person or to a recording, against a clock, from the
structure rather than from the page.

## Summary and Key Terms

### Summary

The order is the content. **Seven moves**, of which the architecture is one: clarify the requirement
in questions; say how you would know it worked; the retrieval choice; the context, the prompt and the
answer; cost per request; the failure modes; and what you would watch in week one against what you
would not build yet. Almost everybody starts at the third, and the first, second and last are where
the conversation is decided — all three being *refusals*. **Move one** asks five questions and the
highest-value one is *what should it do when it does not know*, because Chapter 16 established that
the default is a plausible answer rather than a refusal and the trade against Chapter 30's *refuses
when the answer is there* is somebody else's decision; then state the assumptions in one sentence and
move on. **Move two comes before the architecture on purpose**: thirty cases of question, document and
answer, a grader written before any reply is seen because Chapter 41's finding is that *a grader is
not a neutral instrument*, Chapter 20's ±0.14 at forty cases from nothing but which cases you drew,
paired comparisons so what the two versions share cancels, Chapter 32's two verdicts kept apart, and
the price nobody says — Chapter 46's eighty answers held seventeen failures, so Chapter 30's forty
failures is about **a hundred and ninety answers read**. Two refusals there: a judge is not the first
instrument (Chapter 46's two judges for the largest mode code cannot reach came 50 and 30 points
*below* one that passes everything), and seventeen failures give no ranking (two modes level at five, a resampled gap from
−0.353 to +0.353). **Move three is measured rather than asserted**: dense beat lexical by +0.311
recall and +0.369 nDCG over chunks, fusion beat lexical, and **fusion lost to dense** at −0.120 and
−0.156 with both intervals clearing — so *we would use hybrid* is the thing to have measured, scoped
to one corpus and eight queries and a mechanism Chapter 45 names. Keep a lexical lookup anyway for
Chapter 43's identifier query, and say that the routing itself is unmeasured. At a candidate depth of
fifteen the ceiling is 1.000 and recall 0.984, and the headroom *rises* from 0.119 to 0.152, so five
more candidates beat a better reranker — and in that chapter the candidates *are* its calls, forty
more across eight queries, where in a design with no reordering stage they are a similarity
comparison each and deliver nothing until something reorders them.
**Move four** puts Chapter 18's four blocks in order, with Chapter 49's $0.19-per-thousand prefix
saving named and out of reach at this system's 612-token prompt against a 1,024-token minimum, treats the context as Chapter 28's budget rather than a window, and lands on citations with
their limit named — three mechanical checks that are necessary and not sufficient, with three
distinct shapes getting past them — plus Chapter 32's unit, where claim and sentence differ by
twenty-five points on one answer. **Move five is one line of arithmetic**: 612 input tokens at $0.150
a million and 38 output at $0.600 give $0.11 a thousand, which is Chapter 49's baseline, so six
thousand requests a day is **$19.80 a month** — and the reranker you were about to add is fifteen
candidates at about ninety tokens a pair — derived from Chapter 49's own 265 characters a passage —
which is $0.25 a thousand, **about twice the request it improves**, for a gain Chapter 45 could not
tell from zero. The index is 2.5 million tokens and 61 MB, once, and five cents at a price this book
did not measure and therefore dates.
**Move six names six failure modes** from Chapter 46's real output — citation points elsewhere 5,
neighbouring question 5, one case when two apply 4, then one each — says the rate is near a fifth,
refuses the order, and splits the six by what can decide them — three have code
checks and hold seven of the seventeen failures, three hold the other ten, and *citation does not
support the claim* is the one nothing mechanical can tell from a good citation, needing Chapter 32's
claim-level check that Chapter 46 named and did not build.
**Move seven** is four fields — a trace split into cheap ids and sampled content, the two latency
numbers with streaming to make the first measurable, the three token counts and a label, and three
revisions as one artefact — and then eight deferrals, six of which have a measurement in this book
that came out against them, with the refusal path deliberately not among them. And on the saying:
state the structure first, attach every figure to its measurement, say what would settle it when you
do not know, and avoid both of the ways the conversation fails — fifteen minutes on chunking, or a
level at which nothing can be wrong.

### Key Terms

**This chapter introduces none, and that is deliberate rather than an omission.** It is the book's
one synthesis: every term in it is owned by an earlier chapter and used here by name, and every
figure but one belongs to the chapter that measured it. For the same reason there is no *Worth Memorising*
table — the numbers above are already in the cheat sheet under the chapters they came from, and
copying them here would file one measurement under two owners.
