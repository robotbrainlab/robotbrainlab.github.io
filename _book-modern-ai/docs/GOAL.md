<div align="justify">

# Modern AI: Research, Science and Engineering — what we are building, and why

## Table of Contents

- [0. How to read this document](#0-how-to-read-this-document)
- [1. The ultimate objective](#1-the-ultimate-objective)
  - [1.1 The career goal](#11-the-career-goal)
  - [1.2 What that means in practice](#12-what-that-means-in-practice)
- [2. The purpose of the book](#2-the-purpose-of-the-book)
  - [2.1 Why a book at all](#21-why-a-book-at-all)
  - [2.2 The problem the book solves](#22-the-problem-the-book-solves)
  - [2.3 What the book is not](#23-what-the-book-is-not)
  - [2.4 Independence](#24-independence)
- [3. The research philosophy](#3-the-research-philosophy)
  - [3.1 The five questions, per area](#31-the-five-questions-per-area)
  - [3.2 The five dimensions, per subject](#32-the-five-dimensions-per-subject)
  - [3.3 Research cannot supply the taxonomy](#33-research-cannot-supply-the-taxonomy)
  - [3.4 Evidence rules](#34-evidence-rules)
  - [3.5 Awareness is separate from research](#35-awareness-is-separate-from-research)
- [4. The learning philosophy](#4-the-learning-philosophy)
  - [4.1 The parts, and how they join](#41-the-parts-and-how-they-join)
  - [4.2 Verification is the owner's own responsibility](#42-verification-is-the-owners-own-responsibility)
  - [4.3 The assumption to make about the reader](#43-the-assumption-to-make-about-the-reader)
- [5. The expected learning experience](#5-the-expected-learning-experience)
  - [5.1 The standard](#51-the-standard)
  - [5.2 The language and the voice](#52-the-language-and-the-voice)
  - [5.3 Structure — not yet decided](#53-structure--not-yet-decided)
  - [5.4 Tracking what changes](#54-tracking-what-changes)
- [6. Why a research-oriented engineer, and not one of the alternatives](#6-why-a-research-oriented-engineer-and-not-one-of-the-alternatives)
- [7. The role of practical work](#7-the-role-of-practical-work)
  - [7.1 What practical work must do](#71-what-practical-work-must-do)
- [8. The continuous evolution of the book](#8-the-continuous-evolution-of-the-book)
- [9. The intended outcome](#9-the-intended-outcome)
- [10. Scope and the areas](#10-scope-and-the-areas)
- [11. Lessons from our discussions — what went wrong and why](#11-lessons-from-our-discussions--what-went-wrong-and-why)
  - [Class A — Claiming without reading](#class-a--claiming-without-reading)
  - [Class B — Answering a different question than the one asked](#class-b--answering-a-different-question-than-the-one-asked)
  - [Class C — Deciding what was the owner's to decide](#class-c--deciding-what-was-the-owners-to-decide)
  - [Class D — Stating a claim above the strength of its evidence](#class-d--stating-a-claim-above-the-strength-of-its-evidence)
  - [Class E — Rebuilding from the last correction instead of from the evidence](#class-e--rebuilding-from-the-last-correction-instead-of-from-the-evidence)
  - [Class F — Private shorthand](#class-f--private-shorthand)
  - [Class G — Instructions with no termination condition](#class-g--instructions-with-no-termination-condition)
  - [Class H — Assessing a thing with an instrument that does not sample it](#class-h--assessing-a-thing-with-an-instrument-that-does-not-sample-it)
  - [Class I — Doing adjacent work instead of the named deliverable](#class-i--doing-adjacent-work-instead-of-the-named-deliverable)
  - [Class J — Treating a superseded document as current](#class-j--treating-a-superseded-document-as-current)
  - [Class K — Continuing to use evidence after it stopped counting](#class-k--continuing-to-use-evidence-after-it-stopped-counting)
  - [What follows for the framework](#what-follows-for-the-framework)
- [12. Additional considerations I identified](#12-additional-considerations-i-identified)
- [13. What this document does not cover](#13-what-this-document-does-not-cover)


This document records the purpose of the book before any of it is designed or written. It exists because several misunderstandings occurred while the purpose was
only in conversation, and because the next person to work on this — including a future session of
mine — will act on what is written here.

It describes **no methodology**. How the book gets built is a separate proposal, deliberately kept
out of this file so that a disagreement about method cannot quietly change the goal.

---

## 0. How to read this document

Every substantive statement carries one of four markers. This is a requirement of the owner's,
made because I have previously presented my own recommendations as settled decisions.

| Marker | Meaning |
|---|---|
| **[STATED]** | The owner said this, in his own words, in conversation. Quoted where the wording matters |
| **[AGREED]** | Proposed by one of us and explicitly accepted by the other |
| **[I RECOMMEND]** | My proposal. **Not a decision.** The owner has not ruled on it |
| **[OPEN]** | A decision that has to be made and has not been |

**Nothing in this document is a decision unless it is marked [STATED] or [AGREED].** An
[I RECOMMEND] item may be wrong, and several of my recommendations in this project already were.

[↑ Back to Table of Contents](#table-of-contents)

---

## 1. The ultimate objective

### 1.1 The career goal

**[STATED]** The objective is to become a strong candidate for roles such as **AI Researcher,
Research Engineer, AI Engineer, Machine Learning Engineer** and related positions.

**[STATED]** The objective is explicitly *not* staying informed:

> "My ultimate objective is not simply to stay informed about AI advancements. I want to
> systematically build a deep understanding of both the scientific foundations and the latest
> research and engineering developments across these areas."

**[STATED]** Four capabilities are named as the target, and all four are wanted together:

1. **Theoretical depth** — understanding the science under the practice.
2. **Research awareness** — following what is being investigated now.
3. **Experimentation skill** — the ability to reproduce, test and evaluate.
4. **Hands-on engineering** — the ability to build the thing.

**[STATED]** The identity being aimed at is a **research-oriented engineer**:

> "I am not trying to become someone who only studies or summarizes research. I want to develop
> into a research-oriented engineer who understands the science, follows the research, and knows
> how to apply that knowledge through engineering."

### 1.2 What that means in practice

**[I RECOMMEND]** this as the operational definition, because it is testable and the alternatives
are not:

> A research-oriented engineer, given a new paper claiming an improvement, can say what the claim
> was measured against, reproduce enough of it to check, and decide whether to put it in a system.

The reason for preferring this definition: it is the only one of the four capabilities in §1.1 that
**transfers when the models change.** A specific architecture, a specific tool and a specific
benchmark all expire; the ability to ask what a claim was measured against does not.

[↑ Back to Table of Contents](#table-of-contents)

---

## 2. The purpose of the book

### 2.1 Why a book at all

**[STATED]** The book replaces scattered material:

> "Rather than relying on scattered resources, research papers, articles, and documentation, I want
> to maintain one centralized, continuously evolving book that serves as my primary learning
> resource."

**[STATED]** It must bring together, in one place: established scientific knowledge, theoretical
foundations, ongoing research, engineering advancements, practical implementations and emerging
developments.

**[STATED]** It must evolve with the field "without losing the structure and continuity of my
learning."

### 2.2 The problem the book solves

**[I RECOMMEND]** this statement of the problem, derived from what the owner has said twice about
losing structure:

A reading list fails in a specific way. A paper read in March and a paper read in September do not
compose into understanding unless something holds the shape between them. Fifty bookmarks are a
record of intentions, not a curriculum. A book supplies three things a reading list cannot:

1. **A place.** Each new finding has to be *placed* relative to what is already known.
2. **A guarantee.** A later addition cannot quietly contradict an earlier one.
3. **A shape that survives replacement.** The structure outlives its own contents.

### 2.3 What the book is not

**[STATED]** The book is a **learning resource**. It is not a portfolio and not a record of
completed work:

> "The book is a learning resource, not a portfolio or a record of my completed work. My actual
> practice, implementations, experiments, and projects are separate from the book."

**[AGREED]** It therefore cannot be used as evidence of what has or has not been learned, built or
practised. Any assessment that treats the absence of a record in the book as the absence of the
activity is making an inference the document does not support. (See §11, class H.)

### 2.4 Independence

**[STATED]** The book is **fully independent and self-contained**. It is not a continuation, an
extension or a revision of any earlier work. It has no connection to one in content, scope,
structure or progression.

**[STATED]** Four consequences, in the owner's own words:

1. The book is **developed entirely from scratch**.
2. Topics will appear here that have been covered elsewhere, and he is **completely comfortable
   with that overlap**.
3. **Duplication is not avoided.**
4. **No topic gets less explanation because something else covered it.** Every topic is approached
   and developed independently, with the necessary depth and completeness.

**[STATED]** Two things were extracted from earlier work before this document was written — a
**voice** and a **method**. Both are now written down as rules in their own right: the voice in
`GUIDE.md` §4, the method in `PROCESS.md`. **Nothing points back at the source, and nothing needs
to.** If a rule turns out to be wrong, the review of chapter one is where that is found.

**[STATED]** No earlier work is a research source. A claim does not become true because a book
states it.

[↑ Back to Table of Contents](#table-of-contents)

---

## 3. The research philosophy

### 3.1 The five questions, per area

**[STATED]** Every major area of AI identified by the research must answer five questions:

| # | Question |
|---|---|
| 1 | **Ongoing research** — what problems are researchers trying to solve now; latest discoveries; emerging directions; unresolved challenges |
| 2 | **Engineering developments** — new architectures, techniques, systems, tools, implementations being built or adopted |
| 3 | **Established scientific knowledge** — theories, principles, methods and findings with strong evidence, and how they underpin the current work |
| 4 | **Research-to-engineering transition** — how discoveries become practice; what is still experimental and what is now established engineering |
| 5 | **Skills and career relevance** — what knowledge, skill and experience are needed to understand, reproduce, implement or contribute |

### 3.2 The five dimensions, per subject

**[STATED]** Identifying an area is not enough. Each important subject *inside* an area needs:

| # | Dimension |
|---|---|
| 1 | **Why it matters** — what problem it solves, why now, why it is worth research and engineering attention |
| 2 | **Scientific foundations** — the theories, mathematics, algorithms and established concepts that make it possible, and how they explain why different approaches work |
| 3 | **Ongoing research** — what is being investigated, what is proposed, what remains unresolved |
| 4 | **Engineering and implementation** — how to design, build, optimise, evaluate and deploy it; the patterns, frameworks, architectural decisions and trade-offs |
| 5 | **Research-to-engineering connection** — how to experiment with new approaches, reproduce results, evaluate effectiveness, and adopt what proves out |

**[STATED]** The owner's guidance is explicitly non-binding in detail: this is *"general guidance
to provide direction and additional context, not as a strict requirement or a narrowly defined
scope."*

### 3.3 Research cannot supply the taxonomy

**[I RECOMMEND]** this principle, which I arrived at after getting it wrong twice in this project,
and which the owner has questioned twice and not yet ruled on:

- **A partition of the field is an argument, not a finding.** No amount of searching produces one,
  because a partition is a decision about what to treat as the same thing — and a decision has
  alternatives and reasons, which is what an argument is and what a measurement is not. **The test:
  a finding can be wrong. A partition can only be worse or better for a purpose.**
- **An unconstrained search returns what is most published and most linked, not what matters most.**
  This is a property of search indexes, not a finding about AI: a research instruction that names no
  areas will over-sample whatever currently dominates the index, whatever that happens to be. So a
  brief that says "research modern AI" measures the index.

  **A brief must not name the concentration it expects to find.** Where the index points is not
  knowable in advance, and an instrument built to expect one answer finds that answer.
- **So a fixed set of research areas is a coverage device**, used to force attention somewhere the
  search index does not point. It is not a claim about the field's natural shape.
- **Consequence:** any percentage computed over a chosen set of areas is a percentage of **that
  choice**, not a property of the field. Measure one area against two different area lists and its
  share changes while the area does not.

**[AGREED 2026-11-06] How this reconciles with the overview the owner asked for.** §10 records his
requirement that the research report each field's estimated share, dominance, adoption and growth.
Taken literally, "share of the field" is the number the paragraph above forbids. The resolution,
agreed with him:

| Replaced by | Why it is sound |
|---|---|
| **Absolute counts with their sources** | Anyone can recount them |
| **Ratios against a denominator somebody else defined** — a named index, a named job board | The denominator is not our choice, so it is checkable |
| **Direct comparisons between areas on one measure** | Both numbers come from the same instrument |

He gets what the requirement was for — which areas are large, which are growing, which are
shrinking — without anybody inventing a total for AI. `briefs/TEMPLATE-area-research.md` states this
as an instruction and forbids the share.

### 3.4 Evidence rules

**[STATED]** The research must prioritise, in the owner's own list:

> New scientific discoveries and technological breakthroughs. Advancements in AI models,
> architectures, algorithms, and capabilities. Emerging technologies, tools, and frameworks.
> Significant research papers and their technical contributions. Practical innovations,
> engineering developments, and real-world applications. Technical challenges, limitations, and
> opportunities for further innovation.

**[STATED]** It must **not** be a report on incidents, misuse or broader societal concerns. The
owner's correction: *"Shouldn't our primary focus be on advancements in research, science, and
technology rather than on how technology is being misused?"*

**[STATED]** Percentages must be evidence-based with the method stated, and subjective estimates
must never be presented as established facts.

**[AGREED]** A claim may not be stated above the strength of its source, and the source is quoted.

**[AGREED]** Every size claim names what it is a share of. "Growing fast" is not a finding.

**[I RECOMMEND]** a definition, because four separate rules turn on the phrase and none of them
defined it:

> **A claim is load-bearing when removing it would change what the chapter teaches.**

Three tests, and one is enough: the chapter's conclusion changes if the claim is false; a reader
would act differently without it; or another claim in the chapter rests on it. A claim that is
true, interesting and removable without touching the argument is **not** load-bearing — it is
colour, and it does not need a `CLAIMS.tsv` row.

**[I RECOMMEND]** three further rules, each paid for by a failure in this project:

1. **A search summary is not a source.** A snippet tells you something was said; it does not tell
   you what the source says **now**. Between indexing and reading, a paper can be revised,
   corrected, retracted or withdrawn — and the snippet will not know. Fetch the page.
2. **A source's own inclusion criteria are part of the finding.** A figure giving the share of
   "notable" items of some kind measures the criteria for notability, not the population: criteria
   built from citations, benchmark records and press coverage select for visibility, and anything
   that is consequential without being visible is outside the denominator by construction. **Check
   what the denominator admits before quoting the ratio.**
3. **Every research instruction carries a termination condition and a fixed output shape.** Three
   research agents in this project searched for an hour without converging, because every
   instruction they had rewarded searching more and none said what finished looked like.

### 3.5 Awareness is separate from research

**[STATED]** The owner wants the rapid expansion of AI tools and services tracked, not only the
scientific literature, and explicitly not limited to named companies.

**[AGREED]** Awareness and research are different activities on different clocks, and the rule that
keeps them apart is: **watch the tools, write down the capability.** A tool release is recorded for
what it proves is now possible, never as news — because a product name is `volatile` and will be
wrong within a cycle, while the capability it demonstrates may be `durable`.

**Where this lands in the method:** the research brief's `TRANSITION` field, which asks what is
still experimental, what is becoming practice and what is established engineering. A tool release
is evidence for the middle column and rarely for the third.

[↑ Back to Table of Contents](#table-of-contents)

---

## 4. The learning philosophy

### 4.1 The parts, and how they join

**[STATED]** Scientific foundations, theory, active research, practical engineering, exercises,
labs and projects are **one process**, not separate disciplines:

> "The book should therefore bridge scientific understanding, active research, and practical
> engineering, rather than treating them as separate disciplines."

**[STATED]** The learning method is: *"learn by understanding, practicing, implementing, and
building"* — not by reading and absorbing.

**[I RECOMMEND]** the structural consequence, which is the single most important design statement
in this document:

> **Dimensions 2, 3 and 4 of §3.2 are one object seen at three distances. They must not become
> three sections.**

Written as three headings, they reproduce exactly the separation the owner rejects.

**The shape of the argument, without an example.** Take any mechanism with a theoretical limit.
*The foundation* is why the limit exists at all. *The live research* is the dispute about where the
limit actually sits. *The engineering* is what practitioners build to work around it — and that
engineering choice is unintelligible without the dispute, because it looks arbitrary until you know
what is contested. One argument, three distances.

**A worked example belongs here and is deliberately not written yet.** An example needs a real
mechanism with a real dispute attached. Writing one now would mean picking a subject before the
research has established that it is in scope, and saying something about current practice with no
source behind it. **The first chapter supplies the example**, and it will be a real one.

**[I RECOMMEND]** that a chapter is therefore organised around **a mechanism or a question**, with
science, research and engineering braided into answering it.

### 4.2 Verification is the owner's own responsibility

**[STATED]** The owner will verify what he learns, by consulting credible authoritative resources,
cross-checking explanations, questioning assumptions, and confirming technical accuracy. He will
not accept the book's contents as correct by default.

**[AGREED]** This answers the concern about independent validation, with one narrow residue, stated
at its true size: cross-checking cannot catch a **consensus error**, where the available sources
agree and are all wrong in the same direction.

**Why that class is possible, by argument rather than by example.** Two mechanisms can produce it.
Where a comparison is run by the people proposing the new thing, the baseline is the one they had
time to configure — and if nobody re-runs it against a well-configured baseline, later work inherits
the gap. And an evaluation protocol with a flaw rewards whatever exploits the flaw, so agreement
across a literature can reflect the protocol rather than the thing measured. **How often either
happens is not claimed here**: the point is only that neither is detectable by reading more
sources, which is what makes a measurement the remedy.

**The remedy is a measurement, not another source**, and the labs are where that measurement
happens. `GUIDE.md` §6's reproduction labs exist for exactly this.

### 4.3 The assumption to make about the reader

**[STATED]** Any assessment of this approach must assume that the owner **thoroughly reads,
studies and works through everything** in the book — theory, exercises, labs and recommended
projects. The book is not something generated and passively read.

[↑ Back to Table of Contents](#table-of-contents)

---

## 5. The expected learning experience

### 5.1 The standard

**[STATED]** The material must be *"easy to learn from while remaining technically rigorous,
comprehensive, and useful for practical engineering and interviews."* Explicitly rejected:

- a conventional textbook with unnecessarily complicated explanations;
- superficial summaries that sacrifice technical depth.

**[STATED]** Language: ASD-STE100 style. Simple, clear, precise. Short sentences. Tables where
they carry the information better. Essential technical terms explained in plain language.
Unnecessary jargon avoided.

**[AGREED]** The target: **technically complete, with nothing unexplained and nothing explained
twice.** Difficulty belongs to the subject, never to the prose.

### 5.2 The language and the voice

**[STATED]** The voice is not a preference and not decoration. It is what makes the material
learnable, and it is as binding as any other rule.

**It is specified in full in `GUIDE.md` §4** — the rules, and the fourteen habits that make them
concrete, seven of which make the material easy and three of which keep it rigorous. Dropping
either set produces something the owner has rejected: a textbook that performs rigour through
difficulty, or a summary that trades depth for ease.

It is stated there as rules a writer follows, with nothing to consult and nothing to imitate.

### 5.3 Structure — not yet decided

**[STATED]** The book has **no connection to any earlier work in structure or progression**
(§2.4). Whatever shape it takes is chosen here, on its merits, for this book.

**[I RECOMMEND]** one sequencing point that matters more than the choice itself: **structure
follows the subjects, not the reverse.** The parts of a book are a claim about how its material
divides, and the material is not known until the research has run. Choosing the parts now would
mean choosing them from my assumptions about what the research will find — which is §11 class C.
**So this section stays open until the subjects exist.**

#### What a progression buys, and what a part is for

**[I RECOMMEND]** recording what any grouping has to earn, separately from the choice of one,
because this is what the candidates below are weighed against:

> **A part is worth having when it is a progression in what the reader can *do*** — comprehend,
> then operate, then construct, then judge. Each stage is useless before the one below it, and each
> is usable on its own. A grouping that is only a filing system for related chapters earns nothing:
> a reading order would do the same work for free.

And one structural idea worth keeping whatever shape is chosen: **cross-cutting properties belong
last, as threads.** Security, speed, cost and failure are not things a reader uses — they are
questions asked of a finished system. Teaching them early teaches them as features.

#### The candidates

**[OPEN]** The book covers many areas, has no end, and must be self-contained per topic. Five
candidates, with what each costs:

| Candidate | What it means | What it costs |
|---|---|---|
| **A · One progression over the whole book** | Comprehend every area, then operate them all, then construct, then judge | "Comprehend all areas" is a very long wait before anything can be built, and the first part becomes most of the book |
| **B · The progression inside each area** | Each area is a small complete book: comprehend → operate → construct → judge | The pattern repeats; cross-area material has no home |
| **C · Shared foundations, then one part per area** | A foundations part first, then an area per part, each with its own progression | Needs the foundations to be genuinely shared, or it becomes a dumping ground |
| **D · Flat by subject, with reading maps** | No parts. Chapters are subjects; maps give several orders through them | Loses the progression that makes the material learnable — the thing §5.1's standard rests on |
| **E · Parts by the five dimensions** | Part per dimension: why it matters, the science, the research, the engineering, reproducing | **Rejected.** The owner's instruction is that the dimensions must *not* become sections (§4.1) |

**[I RECOMMEND]** **C combined with B** — a shared foundations part, then an area per part, each
area carrying its own progression. **Its two halves do not stand equally, and the weaker one is
marked rather than hidden.**

1. **The shared part rests on nothing yet.** It would need some subject to be common to every area,
   and **nothing here establishes that one is.** The research either finds such a subject or it does
   not; until then candidate C has no basis, and it stays on the list only because it is cheap to
   adopt if the research does find one.
2. **An area has to be finishable on its own.** This one does not depend on the research, but it
   does rest on an unmeasured belief, so it is marked: **if text is produced faster than it can be
   worked through — likely, but nobody here has measured it (§12, item 1)** — then an area that is a
   complete unit is something the owner can finish, while an area smeared across the whole book is
   not. If the rates turn out comparable, this reason weakens and B is left standing on nothing
   either.

**So the honest state is:** both halves rest on something unestablished — C on a shared subject the
research has not found, B on a production rate nobody has measured — so the combination is a guess
until the research speaks and the first cycle is timed.

**[I RECOMMEND]** that this stays **[OPEN]** until the subjects are known, for the sequencing
reason at the head of this section. **A structure chosen now is a structure chosen from my
assumptions about the research.**

### 5.4 Tracking what changes

**[AGREED]** The book needs a visible **"What Changed in This Edition"** page. The owner's words:
*"Yes this is exactly what I wanted to see."*

**[AGREED]** Without it, the reader cannot distinguish learning something new from relearning
something revised — which is the central hazard of a book that is revised rather than finished.

[↑ Back to Table of Contents](#table-of-contents)

---

## 6. Why a research-oriented engineer, and not one of the alternatives

**[STATED]** Not exclusively academic research, and not conventional software engineering.

**[I RECOMMEND]** this account of why the middle position is the right target. **It argues from the
owner's stated objective in §1.1, not from evidence about the job market:**

| Position | What it tests | Why it is not the target |
|---|---|---|
| Academic researcher | Producing new results; publication | Requires depth the owner has not chosen, and most of the roles named do not test it |
| Conventional software engineer | Building and shipping systems | Does not require judging a research claim, which is what the named roles do test |
| **Research-oriented engineer** | **Reading the literature, judging a claim, reproducing it, and building on it** | **This is the target** |

**[I RECOMMEND]** the supporting observation, **and it is an unverified belief about hiring, not a
finding**: that an application-role interview tends to ask whether you know the established answer,
while a research-engineer interview tends to ask whether you can read a paper, judge whether its
claim is supported, and reproduce or extend it.

**What the research must settle.** `briefs/TEMPLATE-area-research.md` collects a `SKILLS` field per
subject and a `SKILLS AND CAREERS` field per area, both of which require the evidence to be named.
Until those come back, the claim above is a hypothesis — and the argument it supports (that the book
must carry contested material, not only established material) also follows from the owner's own
stated objective in §1.1, which does not depend on it.

[↑ Back to Table of Contents](#table-of-contents)

---

## 7. The role of practical work

### 7.1 What practical work must do

**[STATED]** Exercises, experiments, implementations and projects reinforce the material. The book
holds them; it does not hold the record of having done them.

**[I RECOMMEND]** **two lab forms, specified in `GUIDE.md` §6.** A lab either **constructs** —
build the thing, then measure it — or **reproduces or refutes** a published claim: does this
improvement survive a fair baseline, does this result hold when the protocol changes, is this
difference real. The second form exists because the book must be able to teach a subject whose
answer is not settled. Which form a chapter uses follows from its subject.

**[I RECOMMEND]** three *shapes* a reproduction lab takes. These are shapes, not labs: **each needs
a real published claim to attach to**, and the research is what supplies those.

| Shape | What the reader does | What the reader finds out |
|---|---|---|
| **Re-measure an interval** | Compute the same estimate two ways, one of them the method a paper used, and measure the gap | **Whether** the method a paper used misleads in the regime the reader works in, and by how much |
| **Score a null baseline** | Run something that cannot work under a published evaluation protocol, and see what it scores | **Whether** that protocol can be satisfied without the thing it claims to measure |
| **Find the envelope's edge** | Run a method inside its stated operating range and then outside it | **Where** its boundaries actually are, against what its abstract states |

**Note the column heading: it asks rather than asserts.** A column saying what each shape *teaches*
would state the finding before the lab had run, in a document whose purpose is to specify how
findings are obtained. **A lab whose conclusion is known in advance is not a lab.**

Until the research supplies the claims, no lab of this form can be written.

[↑ Back to Table of Contents](#table-of-contents)

---

## 8. The continuous evolution of the book

**[STATED]** The book is added to periodically — the current cadence is every twelve weeks — and
must incorporate new findings, research directions, engineering practices and emerging
technologies without losing structure or continuity.

**[AGREED]** A chapter whose subject is settled can be a **closed explanation**. A chapter in this
book cannot be, because the book is revised rather than finished — and that changes what a chapter
is:

> **A chapter is a question with a current answer attached, where the question outlives every
> answer it will carry.**

**[I RECOMMEND]** three design consequences, which I believe are the most serious unsolved problems
in this project:

1. **Quality machinery costs per revision, not per chapter.** Checking a chapter properly is
   expensive: a corrected claim in a lab chapter lives in about six places, four of them prose,
   because a lab's programs narrate their own output; every applied fix is a book-wide sweep counted
   before and after; and a record is hashed last, so any edit makes one stale. **That price is paid
   once in a book with an end.** A book revised every twelve weeks across many areas pays it every
   cycle, forever. **The revision cost, not the writing cost, will decide whether this book survives
   its third cycle.**
2. **An acceptance question needs a right answer, and contested material has none.** The rule works
   when a question has an answer a chapter must contain. For a disputed subject the honest answer is
   sometimes *"this is disputed, and here is the state of the dispute"* — a real answer that a rule
   demanding *the* answer cannot accept.
3. **"Nothing is drafted until the table of contents is approved" collides with a table of contents
   that changes every cycle.** Fixed concept ownership is what makes the taught-ledger work. If
   research reshuffles subjects each cycle, ownership moves, and the ledger that prevents
   re-teaching is the first thing to break.

**[OPEN]** How each of those three is solved.

[↑ Back to Table of Contents](#table-of-contents)

---

## 9. The intended outcome

**[STATED]** The owner wants the research process and the book to help him *"identify what matters,
understand it thoroughly, develop relevant capabilities, and position myself to successfully pursue
these career opportunities."*

**[I RECOMMEND]** this statement of what "done" means for a cycle, because the goal otherwise has
no test:

After a cycle, the owner can, for each subject the cycle covered:

1. state what problem the subject solves and why it is receiving attention;
2. explain the mechanism from the foundations, without notes;
3. name what is currently disputed and what the dispute turns on;
4. build a working instance of it;
5. take a published claim about it and say what it was measured against, then check it;
6. answer, aloud and in about a minute, the questions a research-engineer interview would ask.

[↑ Back to Table of Contents](#table-of-contents)

---

## 10. Scope and the areas

**[STATED]** The research covers the full spectrum of modern AI under the theme *Modern AI:
Research, Science and Engineering*, beginning with a high-level overview that identifies the major
fields and subfields, their estimated share, their relative dominance, their industry relevance and
adoption, their growth potential, and the engineering skills and career opportunities for each.

**[STATED]** The scope is not to be narrowed unnecessarily, and the prior restriction to language
models was wrong.

**[I RECOMMEND]** that the **unit of the book is the subject, not the area.** Research finds
subjects; subjects get chapters. An area is a container used to ensure coverage.

**[I RECOMMEND]** a selection rule, so that depth has a bound. A subject earns a full chapter when
it has all three of:

1. a **mechanism** worth understanding, not merely a practice to copy;
2. **live research**, so following it teaches how to read the literature;
3. something **buildable**, so dimension 5 is possible at all.

**The rule needs no worked examples to be applied.** The research reports `LIVE RESEARCH` and
`BUILDABLE` for each subject, which is exactly what tests 2 and 3 ask for, and its `VERDICT` field
puts all three questions directly.

**What this means in practice:** a subject the field is quietly abandoning fails test 2, and a
subject nobody can build fails test 3 — and both verdicts come from the research record rather than
from my judgement.

**[OPEN]** **Breadth against depth.** Three candidate shapes, and this decision determines almost
everything else:

| Shape | What it costs |
|---|---|
| A thin honest map of every area, and **one area taken to the floor** | Narrower coverage; matches how hiring works |
| **Equal depth across all areas** | No area reaches interview depth; comprehensive |
| A map plus **two areas** to the floor | Roughly doubles the lab and reading work |

**This decision has no evidence behind it yet.** The argument for depth is that if no employer
hires across areas, medium depth everywhere may be worth less than depth in one. That is a
plausible claim about hiring, and **whether it holds is not known here** — the research's
skills-and-careers dimension is what would establish it.

**[OPEN]** **The mathematics boundary.** A boundary calibrated for application engineering — teach
what a model computes when it answers, state how it learned, and move on — is broken by dimension
5, which asks the reader to reproduce a result. Three candidates:

| Candidate | Consequence |
|---|---|
| Enough to **reproduce** a result: the statistics of comparison, and enough optimisation and learning theory to read a training paper critically | Dimension 5 becomes possible; this is my recommendation |
| Enough to **produce** new results: full derivations, optimisation theory, learning theory | Needed to contribute original research; considerably slower |
| **Keep the current boundary** | Fastest; dimension 5 has to be dropped |

**[I RECOMMEND]** the replacement test, if the boundary moves: *does the reader need this to tell
whether a claimed improvement is real, and to build the thing that tests it?* This is sharper than
"go deeper" and still excludes mathematics that only decorates.

**[OPEN]** Which area goes deep, if the shape is asymmetric. **There is no candidate**, and naming
one would mean choosing it from assumption — the question is precisely which area repays depth, so
an answer that does not come from evidence answers nothing. **This closes only after the research
reports its skills-and-careers dimension across every area**, and it depends on the
breadth-against-depth decision above.

**[OPEN]** Whether the book is for the owner alone or eventually for others. It changes what page
one may assume.

**[OPEN]** Whether the labs become public artefacts. The owner has noted that his practice is
separate from the book, so this may be out of the book's scope entirely.

[↑ Back to Table of Contents](#table-of-contents)

---

## 11. Lessons from our discussions — what went wrong and why

**[STATED]** The owner asked for this section explicitly: what misunderstandings, incorrect
assumptions or flawed criticisms occurred, why they were incorrect, and how to avoid repeating
them.

Recorded as **classes**, each with the instances that produced it and the practice that follows,
because a list of mistakes is not reusable and a class is.

### Class A — Claiming without reading

**Instances.** (1) Mapped one document's chapters onto another document's topics from chapter
titles and a summary column, without opening a single topic page — twice, the second time after
being corrected for the first. (2) Said I had looked at a website when I had read a local Markdown
file. (3) Asserted for two days that a document defined a set of areas with reasons, from a one-line
summary of it, and built a carving of my own instead of opening the file. **A summary of a taxonomy
tells you a taxonomy exists; it does not tell you what the categories are** — and having the summary
is worse than having nothing, because nothing makes you look.
(4) Assessed a book's practical content and reported "zero visible evidence" of hands-on work
without opening the directory that held its labs. (5) Stated that the owner had no test for whether
his learning was working, when a document of his carried a per-chapter test and an acceptance bank
written before its chapters — neither of which I had looked for.

**Why it is wrong.** A structural claim about a document is evidence only if the document was read.
Titles are not contents. In the owner's words: *"Did you even look at the website"* and *"Why are
you not even trying to do even the slightest work."*

**The practice.** Before any claim about what a file, directory or document contains or omits, open
it. If it cannot be opened, say the claim is unverified rather than making it.

### Class B — Answering a different question than the one asked

**Instances.** (1) Asked for a content-level comparison of two books, produced a table of purpose,
scope, time-relation and provenance. The owner: *"Worst explanation… I want a genuine review of the
content. How will the above reasons give me a mental model."* (2) Three research briefs asked what
a person must be able to do, and one asked what goes wrong in deployed systems; all three returned
incidents, misuse and societal harm instead of technical advances. The cause was the question, not
the agents.

**Why it is wrong.** Metadata about a thing is not the thing. A brief that asks a question adjacent
to the real one gets a confident answer to the adjacent question.

**The practice.** Restate the question in the answer's first sentence. For a brief, write down the
sentence the output should be able to complete, and check the brief asks for that.

### Class C — Deciding what was the owner's to decide

**Instances.** (1) Pre-fixed the research's partition as "modern practice outside language models".
The owner: *"that is a bad direction. Let the agent or an llm do the research in every direction
amd also let it say only where the dominant modern practice is. Why we decide by ourselves."*
(2) Proposed moving a set of cross-cutting topics out of the part that held them, when a decision
record already in front of me had considered and rejected exactly that. (3) Assumed this book would
build on another piece of work, when nothing had said it would — the owner had to ask whether he had
ever said so. (4) Repeatedly proposed carrying material into the book that a stated scope rule
excluded, naming it in vocabulary the owner had not been given (which is also class F below).

**Why it is wrong.** A decision presented as an analysis removes the owner's choice without telling
him a choice was made.

**The practice.** Read the existing decision record before proposing a change to a decision. Mark
every proposal as a proposal. Where I have fixed something that could have been left open, say so
and say why.

### Class D — Stating a claim above the strength of its evidence

**Instances.** (1) Told the owner that a theoretical limit was settled, refereed and durable, and
recommended building curriculum and a chapter on it. A peer-reviewed rebuttal existed; the limit as
I stated it was contested. **I had the strength of the claim wrong, not the claim itself** — which
is the whole of this class. (2) Asserted that one document *was* a particular kind of thing when my
own evidence showed ten of its sections belonging to no category of that kind — I had noticed the
fact and dropped it, because it spoiled the mapping.

**Why it is wrong.** Dropping the inconvenient half of one's own evidence is the failure the whole
project exists to teach against.

**The practice.** State the strength of the source with the claim. When evidence contradicts a
conclusion I like, report the contradiction in the same sentence as the conclusion.

### Class E — Rebuilding from the last correction instead of from the evidence

**Instance.** Five different answers about this book's scope within an hour, each constructed from
the owner's most recent correction rather than from the documents.

**Why it is wrong.** It looks like responsiveness and is the opposite: it means no position was
ever held for a reason.

**The practice.** After a correction, re-derive the answer from the sources, and say which source
changed my mind.

### Class F — Private shorthand

**Instance.** Used "MP-08", "tier one", "1A/1B/1C" in explanations. The owner: *"I don't even know
what is MP"* and *"What language are you speaking?"*

**The practice.** Name things. No internal codes in anything the owner reads.

### Class G — Instructions with no termination condition

**Instance.** Nine research briefs told each agent to measure things itself, verify at source and
report its own sampling. Every one of those rewards searching more; none said what finished looked
like. Six converged; three were still launching new sub-agents an hour in, one of them about to
start four more.

**Why it is wrong.** An instruction set that only rewards thoroughness has no fixed point.

**The practice.** Every brief states its output shape, its budget, and its stopping rule, and
forbids further delegation beyond a stated depth.

### Class H — Assessing a thing with an instrument that does not sample it

**Instance.** Judged the owner's *approach* by examining the *book*, and reported the absence of a
record of practice in a learning resource as the absence of practice. The owner: *"How can you
determine what I have or haven't learned, practiced, or built simply by examining the book? …I
believe you are confusing the purpose of the learning material with the evidence of learning
outcomes."*

**Why it is wrong, and why this class matters most.** It is the same error that published work
commits whenever a "share of notable X" figure is read as a property of the field rather than of
the inclusion criteria. I spent several messages admiring that discipline and then committed the
error myself, on a document that was never designed to hold the evidence I demanded of it.

**The practice.** Before any claim about a population, name the instrument and ask what it samples.
Where the instrument cannot see the thing, say "I cannot assess this from here" instead of filling
the gap.

### Class I — Doing adjacent work instead of the named deliverable

**Instance.** The owner asked, in several consecutive messages, for the documentation needed before
research to be prepared. In between those requests I read a background document, built an argument
about scope from it, started drafting a candidate area list, and reorganised files. Each of those
was defensible on its own. **None of them was the thing asked for**,
and the documents he had asked for did not exist the whole time. His words: *"you keep doing things your
own way and completely ignoring my instructions, even though I have repeated the same requirements
across multiple requests."*

**Why it is wrong.** An adjacent task that is genuinely useful is the hardest kind of drift to
notice, because every individual step survives the question *"is this worth doing?"* It fails the
only question that matters, which is *"is this what was asked for?"*

**The practice.** Before acting, name the deliverable in one sentence and check the action against
it. When a more interesting question appears mid-task, write it down and finish the deliverable
first. A request repeated twice means the deliverable has not been produced — not that it needs
more context.

### Class J — Treating a superseded document as current

**Instance.** I recommended a document's set of areas as the carving for this book, and called them
better than my own. Two things were wrong, and both were checkable in under a minute. The document
**predated the baseline it described**, which had been revised six weeks after it was written, so it
was superseded. And it had been built to describe a **whole** curriculum, so several of its areas
were foundations material that this book's own scope rule excludes — a rule I had written down two
days earlier. The owner's reply: *"we have made significant changes, and you have completely failed
to account for them."*

**Why it is wrong.** A document's date and its purpose are part of its content. Citing one without
checking either is the same error as citing a number without its denominator.

**The practice.** Before using any document as a basis for a decision: check its date against the
current baseline, and check what it was built for. Say both in the same sentence as the citation.

### Class K — Continuing to use evidence after it stopped counting

**Instance.** Told that a body of evidence no longer counted, I kept arguing from its figures in
the next message, because they were the only evidence I had and they felt too good to drop.

**Why it is wrong.** Evidence gathered under a brief nobody agreed to is evidence of unknown
quality. Keeping it because no replacement exists is how a conclusion outlives its support.

**The practice.** When evidence stops counting, **the argument it supported loses its basis and must
be marked, not re-worded.** §5.3, §7.1 and §10 each record a recommendation whose justification is
absent, and say so in place of asserting one. That is the correct state. **It will be needed again**
— a claim superseded at EXPIRE leaves every chapter resting on it in exactly this position
(`PROCESS.md` §5).

### What follows for the framework

**[I RECOMMEND]** that classes A, C, D, G, H, I, J and K each become a mechanism rather than an
intention. Eight of the eleven can be:

| Class | The mechanism |
|---|---|
| A · claiming without reading | A reading obligation per step in `ROADMAP.md`, naming the files |
| C · deciding what was the owner's | Every statement in this document carries a marker |
| D · claims above their evidence | `CLAIMS.tsv` plus the adversarial pass (`PROCESS.md` §7) |
| G · no termination condition | The brief schema (`PROCESS.md` §4.6) |
| H · wrong instrument | Name the instrument and what it samples, before the claim |
| I · adjacent work | `ROADMAP.md` names one current step and its deliverable |
| J · superseded document | Cite a document's date and purpose in the same sentence as its content |
| K · evidence that stops counting | Mark the argument, never re-word it. §5.3, §7.1 and §10 are the pattern |
**The design principle behind all eight is `PROCESS.md` §1's: convert care into mechanism.** It is
stated there, with its worked example, and not restated here. **Care does not survive a long
project. A mechanism does.**

[↑ Back to Table of Contents](#table-of-contents)

---

## 12. Additional considerations I identified

**[I RECOMMEND]** these as things worth deciding that the owner's list did not name.

1. **The book may be produced faster than it can be read.** Writing text with agent help is
   plausibly much faster than reading it, working its labs and absorbing it — **but nobody has
   measured either rate here, so this is a risk to watch rather than a finding.** The first cycle is
   the measurement: record how long a chapter took to produce and how long it took the owner to work
   through, and the ratio either justifies this concern or retires it. The book therefore needs a
   **reading order and a priority**, not only a structure — otherwise the first cycle produces more
   than a cycle can absorb.
2. **The mirror of the taught-ledger is missing.** There is a record of what the book taught.
   There is no record of what has been run. Given that the owner's practice is deliberately outside
   the book, this may belong outside the book too — but something has to hold it, or no cycle can
   know where the last one stopped.
3. **Superseded material needs a policy, not a deletion.** When a finding is overturned, the
   honest record is that it *was* believed and is no longer. A book that silently replaces its
   claims teaches the current answer and hides the lesson about how answers change — which is the
   specific lesson a research engineer needs.
4. **The research's own findings need a durable home separate from the book.** A research round
   produces checkable claims with sources. **If those live only in a conversation, the next cycle
   re-derives them** — a conversation is the one place a result cannot be re-read or re-checked. If
   instead they live in the book, the book cannot distinguish a claim it verified from a claim it
   was handed. `CLAIMS.tsv` is their home, and `research/` keeps the run each row came from.
5. **The shorthand ledger has a hard job here.** The usual gap is between a formal name and the
   word practitioners actually say. Where a subject is worked on by more than one community, the same technique can carry a
   different name in each, and a reader who knows one cannot find the others. **Whether that is
   common is for the research to report** — the ledger's multi-name rule exists so the case is
   handled when it appears, not because it is claimed to be typical.
6. **Reuse by copying, never by sharing.** Where a script or mechanism is taken from elsewhere, it
   is copied into this project, so that improving this book cannot break anything else.

[↑ Back to Table of Contents](#table-of-contents)

---

## 13. What this document does not cover

- **Methodology.** The development framework, agent workflows, passes, gates, quality standards and
  documentation architecture are a separate proposal, by the owner's instruction.
- **The table of contents.** No subjects are chosen here, and none may be chosen until the research
  has run and the owner has selected from what it returned (`ROADMAP.md` steps 5 and 6).
- **Any decision marked `[OPEN]`.** The count is not stated here on purpose — a hand-maintained
  count drifts out of step with the markers it counts. **Grep for `[OPEN]`.** The ones
  that block the rest are in §10 — the book's shape, the mathematics boundary, and which area goes
  deep if the shape is asymmetric — and all three need the research first.

[↑ Back to Table of Contents](#table-of-contents)

</div>
