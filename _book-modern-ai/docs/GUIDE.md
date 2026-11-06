# The specification — what this book is, and how a chapter is built

**Written 2026-11-06.** This file says what the book *is*. `PROCESS.md` says how it gets made, and
`GOAL.md` says why it exists. Where this file and `PROCESS.md` disagree about the book itself, this
file wins.

**Status: proposal.** Markers as elsewhere: **[STATED]** the owner's words · **[AGREED]** accepted
by both · **[I RECOMMEND]** my proposal, not a decision · **[OPEN]** undecided.

---

## 1. What this book is

**[STATED]** *Modern AI: Research, Science and Engineering.* One book, continuously revised, which
is the owner's single centralised learning resource in place of scattered papers, articles and
documentation.

**[STATED]** It is **fully independent and self-contained**. It is not a continuation, an extension
or a revision of any earlier work, and it has no connection to one in content, scope, structure or
progression. A topic that has been covered elsewhere is developed here from scratch, and **no topic
gets less explanation because something else covered it.**

**[STATED]** It must make the reader able to **understand the science, follow the research, and
build the thing** — not to summarise research.

**[AGREED]** A chapter is **a question with a current answer attached, where the question outlives
every answer it will carry.** This is the single most consequential sentence in the specification;
§5 builds the chapter around it.

## 2. The reader

**[STATED]** The reader works through everything: the explanations, the exercises, the labs and the
recommended projects. He verifies what he learns against authoritative sources and does not take
the book's word for anything.

**[STATED]** The owner is the reader the book is written for. **Whether he is the only one is
`[OPEN]` below** — who it is written for and who may read it are different questions.

**[AGREED 2026-11-06]** what the book may assume:

- **Python** at working level.
- **Nothing** about any subject in the book's own scope.
- **A prerequisite from outside the scope is taught from zero, inside the book, and never sent
  elsewhere.** Where it is taught depends on how many chapters need it:

| Needed by | Taught |
|---|---|
| **One chapter** | **Inline**, in that chapter, from zero |
| **More than one chapter** | **Its own `FOUNDATIONS-ONLY` chapter**, taught once (§3). Later chapters refer to it and do not re-teach it (`OWNERSHIP.tsv`) |

**Why the split.** The one-concept-one-owner rule means the first chapter to need something carries
the whole teaching load for it. Without this split, a chapter about a current result becomes partly a
chapter about linear algebra — and that is the wrong chapter for it. **Nothing is sent outside the
book either way**, which is what the rule was protecting.

**[AGREED 2026-11-06] The owner alone, for now.** So a chapter may assume his Python and his
background, and need not explain what he already knows. **This is the faster book to write and it
matches the stated purpose** — his single learning resource, not a publication.

**The cost of changing it later is real and runs one way:** opening the book up means adding
explanation throughout, not removing it. Nothing in the design depends on the answer staying as it
is, and §3's scope rule is unaffected — a prerequisite is still taught inline from zero, because
*he* may not know it either.

## 3. Scope

**[AGREED 2026-11-06]** The boundary, and it is a boundary about **state** rather than about time
or lineage:

> **The book is about what is currently moving in a subject. It is not about the subject's settled
> foundations.**

**Why it is stated this way.** The owner first proposed drawing the line at the establishment of
language models and their theory, then asked whether that would affect other areas of AI. It would.
A boundary drawn at a point in one developmental lineage locates anything *on* that lineage
precisely and says nothing about anything *off* it. **Three kinds of thing fall through:** an
engineering discipline the lineage never touched, a method whose foundations predate the whole
lineage, and a subject whose own history crosses the line several times. And anything old looks
excluded **for being old**, which is the wrong reason to exclude a live subject.

**None of that names what this field contains** — the research does that. It names the shapes of
thing a lineage boundary cannot place.

A boundary about state applies to every area identically, whatever its lineage, and it needs no
external document to apply.

**[AGREED]** Scope and depth are different questions, and conflating them is the usual error:

| | What decides it |
|---|---|
| **Scope** — which subjects the book is *about* | Whether the answer is still moving |
| **Depth** — what the book *explains* in order to teach a subject in scope | Whatever that subject needs, from zero, inline |

**Teaching a foundation inline does not make it the book's subject.** A chapter on a current result
may teach the mathematics under it in full. The foundation is support; the moving part is the
subject.

**[AGREED]** The test, per claim, which makes this executable rather than aspirational:

> **Has this answer moved, is it disputed, or is it current practice that could change?** If none
> of those, it is foundation.

`CLAIMS.tsv`'s `maturity` column is what records the answer, and `briefs/claim-verifier.md` is what
establishes it. **Without that column the boundary cannot be applied**, which is why the maturity
assessment is part of the research method and not an optional extra.

**A short entry is not a chapter, and does not use the anatomy in §5.** It is one page for a subject
the reader will be asked about but which fails the selection rule — nobody has explained its
mechanism, or no part of it can be built here (`GOAL.md` §10). It states what the subject is, what
it is used for, and **what is not known or not reproducible here, and why.** It carries no durable
question, no lab, no review questions and no `You understand this when` line. **It sits as a marked
section inside the chapter that owns the nearest durable question**, so it is read in context rather
than filed in an appendix; a short entry with no such chapter waits in `PLAN.md` rather than being
dropped. It may own a term in the glossary, under the same rules as any chapter.

**A `FOUNDATIONS-ONLY` chapter has two sources.** The research reports one of them: a settled
subject that the moving subjects are unintelligible without. **The other is found at PLAN, not by
research** — a prerequisite from outside the scope that more than one chapter needs (§2). It is not
a research subject and has no `CLAIMS.tsv` rows of its own unless it makes claims; it exists because
two chapters would otherwise teach the same thing twice.

**One consequence worth stating.** A settled subject still earns a chapter when the moving subjects
are unintelligible without it. The research records that case as `FOUNDATIONS-ONLY`: taught as
established knowledge the reader must know cold, with no dispute section, and present as support
rather than as the book's own subject.

## 4. The language and the voice

**[STATED]** This is the voice. It is not a preference and it is not decoration: it is what makes
the material learnable, and it is as binding as anything else in this file.

### The rules

- Plain, simple and vivid. **Short sentences.** Explain things as you would to a friend.
- **Easy language. Simplicity. Genuinely start from scratch.**
- **Do not write up to an imagined expert.** Do not assume a term has been met before the book
  gives it.
- **Idea first, then commands. Never start a section with a code block.**
- Every command and code sample must work. Run it before it goes in, and show real output.
- **No filler, no hype, no history lessons** unless they explain something.
- **British spelling** everywhere. Proper names keep their own spelling.
- About 80% ASD-STE100: active voice, one idea per sentence, simple words, essential technical
  terms defined in plain language on first use.

### The fourteen habits

**[AGREED]** A rule list is not a voice. These fourteen are the voice, stated as habits a writer
either has or does not.

**Thirteen are in force. The `which set` column says what each one does.** Seven make the material **easy** (1–7), three
keep it **rigorous** (9, 12, 14), three do **both** (8, 10, 13), and one is **conditional** on an
open decision (11). Dropping the easy set produces a textbook that performs rigour through
difficulty; dropping the rigorous set produces a summary that trades depth for ease. The owner has
rejected both.

**If a habit turns out to be wrong, the review of chapter one is where that is found.** These are
written to be followed and corrected, not to be derived again from somewhere else.

| # | Habit | Which set |
|---|---|---|
| 1 | The chapter opens with **what the reader will be able to do** — a capability, never a topic list | easy |
| 2 | The problem is in the **beginner's own voice**: first person, non-technical | easy |
| 3 | **The short answer comes first**, then the detail | easy |
| 4 | Second person, direct, declarative | easy |
| 5 | **Misconceptions cleared by negation** before anything is built | easy |
| 6 | **Start from the difficulty, not the solution** | easy |
| 7 | One everyday comparison, **immediately bounded** — say where it stops holding | easy |
| 8 | **Tables compare; prose explains.** Never prose doing a table's job | both |
| 9 | **One word per concept, forever.** Name the field's shorthand once, then never alternate | rigorous |
| 10 | **Limits are stated as decisions, not gaps** | both |
| 11 | ~~Chapters **keep their promises out loud**~~ — **dropped by §7's decision to reference by concept.** The row and its number stay so that habits 12 to 14 keep theirs | dropped |
| 12 | **The arithmetic is done, not described** | rigorous |
| 13 | Where a subject's **practical stakes** are known, name them plainly and without inflation — what it is used for, what it costs to get wrong | both |
| 14 | **Density without padding.** Density is a feature; filler is not | rigorous |

### Terms

- **Bold** a new term the first time it is explained, and put it in the chapter's `Key Terms`
  table. The Key Terms tables **are** the glossary; it is generated from them.
- Bolding a phrase for emphasis is house style and is **not** a term. Only the Key Terms table
  decides.
- Library and command names go in code font, not bold, and not in the glossary.
- **The field's own shorthand** is handled by `LEDGER-SHORTHAND.md`, which owns the rule for where
  it is named and which chapter may use it. What belongs here is only the voice habit: **one word
  per concept, and never alternate between two.**

## 5. What a chapter is

**[I RECOMMEND]** The anatomy, which follows from §1's sentence about questions and answers.

### Required parts, in order

1. **The question.** One sentence, durable, naming what the chapter will answer for the rest of the
   book's life. It is the chapter's identity and it does not change when the answer does.
2. **An opening paragraph** saying what the reader will be able to do by the end.
3. **`*The problem.*`** — the reader's own words, first person, non-technical.
4. **The answer, in short**, before any detail.

   **[AGREED 2026-11-06] Parts 1 to 4 together are capped at about 400 words** — roughly half a
   page. Each does work the others do not: one names the question, one promises a capability, one
   creates the itch in the reader's own voice, one answers at once. **The risk is not the count but
   the length**: four half-page preambles is a page and a half before anything is taught, which is
   the shape that makes a reader skim to the body. `GATES.md` gate 3 counts the words from the
   chapter title to the first `##`.
5. **The body**, built around a mechanism, with the science, the research and the engineering
   **braided into one argument**. See the rule below.
6. **`## What is disputed`** — when the subject is contested. Fixed shape: the claim, who holds it,
   the counter-claim, who holds that, **what measurement would settle it**, and what to do
   meanwhile.
7. **`## Build it`** — the lab. See §6.
8. **`## Summary, Key Terms, and Review Questions`**, with `### Summary`, `### Key Terms` (Term |
   Meaning), an optional `### Worth Memorising` (numbers, defaults and formulas only), and
   `### Review Questions` (4–6, numbered).

   **[AGREED 2026-11-06] The answers are not here. They are collected in the back matter**, in
   `markdown/ZZ-review-answers.md`, one numbered section per chapter. A reader working alone still
   needs them, but **an answer printed under its question is read rather than recalled** — turning
   to the back is the friction that makes the difference between recognition and memory.

   **This is the one place a chapter is not self-contained**, and it is a real cost, accepted for
   that reason. The answers are still written when the chapter is written, and **three of the four
   review passes still check them against the body**, because an answer key is read as settled and
   is where a correction goes to not happen. Their briefs are given the answers file as well as the
   chapter.
9. **`> **You understand this when** …`** — one sentence.
10. **`## Claims`** — every load-bearing claim in the chapter, with its `CLAIMS.tsv` id.

### The rule that governs the body

**[STATED]** The owner's rule is that the book **bridges** scientific understanding, active research
and practical engineering "rather than treating them as separate disciplines." **`GOAL.md` §4.1 owns
it** and quotes him.

**[I RECOMMEND]**, as `GOAL.md` §4.1 also does and at that strength: dimensions 2, 3 and 4 must not
become three sections. What follows is its consequence for the anatomy above.

**[I RECOMMEND]** The operative form: **dimensions 2, 3 and 4 are one object seen at three
distances.** A chapter is organised around a mechanism or a question, and the science, the dispute
and the engineering decision appear together because the engineering decision is unintelligible
without the dispute.

### Every claim carries its evidence

**[AGREED]** A claim may not be stated above the strength of its source, and the source is quoted.
A claim recorded as `contested` in `CLAIMS.tsv` may not be stated as settled, and one recorded as
`superseded` may not be stated as current.

**[AGREED]** **A number appears as a count with its source, or as a ratio against a denominator
somebody else defined.** Never as a share of "the field": nobody can define that denominator, so no
reader can check it. `briefs/TEMPLATE-area-research.md` states the rule for the research; this is
the same rule for the book.

**[AGREED 2026-11-06] Correctness outranks the source.** Where a well-known explanation is wrong,
the book states the correct rule **and flags the correction**, because that is the reader's only way
to learn that the common explanation is wrong. A source is evidence that something is *said*, never
evidence that it is *true*.

**This holds even where no source disputes it** — the case worth catching is the one where a whole
field has it wrong, and a rule that waits for a dissenting citation is silent exactly there. **The
risk it carries is being confidently wrong**, and the guards are the claim's own row with its
strength and the adversarial pass that reads the prose against it (`GATES.md` gate 12,
`briefs/pass-2-claims.md`). A flagged correction that pass 2 cannot support is a finding.

## 6. Labs

**[STATED]** The book teaches by understanding, practising, implementing and building. Labs,
exercises and project recommendations are part of the book. **The book is not a record of having
done them** — the owner's practice lives outside it.

**[AGREED 2026-11-06] One lab per full chapter, and its size varies with the subject.** A lab may
be an afternoon or twenty minutes. **The chapter states the expected effort**, so a week can be
planned, and `briefs/pass-3-lab.md` reports whether that estimate held. A `FOUNDATIONS-ONLY` chapter
and a short entry carry no lab at all (§3, §5).

**[AGREED]** **Two lab forms, and the chapter's subject decides which.**

| Form | What the reader does | Use it when |
|---|---|---|
| **Construct** | Build the thing, then measure it | The subject is settled enough to build from |
| **Reproduce or refute** | Take a published claim and test it: does this improvement survive a fair baseline, does this result hold when the protocol changes, is this difference real | The subject's answer is in dispute |

The second form exists because **the book must be able to teach a subject whose answer is not
settled**, since it covers active research as well as established practice. That is a capability
requirement. It does **not** predict how many subjects will be contested, or which — that is for
the research to find.

### The contract for a reproduction lab

- **State the published claim**, with its source and strength.
- **State the procedure.**
- **State the decision rule** — what counts as reproducing.
- **The lab passes if it runs and yields a verdict. It does not have to agree with the paper.**

That last line is load-bearing. Without it a lab gets quietly tuned until it confirms its source.

### What a lab may assume about the machine

**[AGREED 2026-11-06]** The labs are written for **an Apple Silicon Mac** — unified memory, Metal
acceleration, no discrete NVIDIA GPU and no cluster. **So small models run and fine-tune locally,
most inference work is possible, and a large training run is not.** A lab that needs more than this
says so and gives the reduced version, or says plainly that there is none (below).

**The exact memory figure is not recorded here**, because nobody has written it down. **So every lab
states its own requirement** — memory, disk, and time — rather than relying on a machine
description, and the owner can tell at a glance whether it fits. If the figure is ever recorded,
this paragraph is where it goes.

**[AGREED 2026-11-06] A lab may spend money, up to a few pounds a chapter.** Many current results
can only be reproduced against a hosted model. The conditions:

- **The chapter states the expected cost before the first command**, so the reader chooses before
  spending rather than after.
- **Where a smaller run exists, the chapter gives it**, with what is lost by taking it.
- **A lab that cannot be done without spending says so**, rather than appearing free and failing
  part-way.
- Keys still come from the environment and are never read, printed, logged or committed.

**[AGREED 2026-11-06] A lab's expected result must hold on the owner's machine, not on any
machine.** This follows from §2: the book is for him alone. So a lab **pins to his setup and states
what it pinned** — versions, model snapshots, hardware — instead of degrading to the weakest machine
a stranger might have. **Sharper labs, easier to write.** The cost is the same one §2 already
accepted: opening the book up later means revisiting every lab, not just the prose.

### Rules for every lab

- **Isolated and safe.** Its own fresh folder. It never touches anything outside it.
- **State what it needs to run** — memory, disk, **expected effort**, and **expected cost where any
  is incurred.** All four are required, not conditional: the effort figure is what makes a week
  plannable, and the cost figure is what lets the reader decide before spending. Where the full
  experiment needs more than the machine above can do, give a reduced version that fits, **or say
  plainly that there is none.** Do not shrink an experiment until it no longer shows the thing.
- **The book ships its own data** where data is needed, in `data/<chapter-slug>/`, which is
  published beside the book and listed in `PROCESS.md` §11. No lab says "your own files": an
  expected result that depends on the reader's files holds for nobody. A lab may read `data/` and
  its own fresh folder, and nothing else.
- **Declare what was planted.** Where the book builds its own data, it lists every property put
  there deliberately, so no lab can claim to have discovered what was put there for it.
- **Pin versions**, and pin any model to a dated snapshot. Print the identifier that came back
  beside any figure that depends on it.
- **No credential ever** is read, written, printed, logged or committed. Keys come from the
  environment.
- **Expected results must hold on the owner's machine**, pinned and stated (above) — not on every
  machine. Never promise exact output from a stochastic system: say what shape it takes, which
  assertion must pass, or give a range.

## 7. Structure, and the cost of cross-references

**[OPEN]** The book's structure. `GOAL.md` §5.3 holds five candidates and the argument that
**structure follows the subjects** — it cannot be chosen before the research names them. Nothing
here presumes it.

**[AGREED 2026-11-06] Reference by concept.** Name the idea; the reader looks up where it lives.
The alternative was a chapter naming a chapter by number — *"Chapter 9 promised to open this"* —
which reads as one continuous argument and costs a sweep through the prose on every re-order. **This
book is revised on a cycle and will be re-ordered many times**, so the sweep would be paid
repeatedly and forever.

**What it costs, and it is a real loss.** Habit 11 in §4 is dropped: chapters no longer keep their
promises out loud, and the book reads slightly less as a single argument. **Decided early on purpose
— after twenty chapters, reversing it means rewriting every cross-reference in the book.**

## 8. Mathematics

**[OPEN]** How deep the mathematics goes. Three candidates, in `GOAL.md` §10.

**[I RECOMMEND]** one test to decide whether a piece of mathematics belongs:

> **Does the reader need this to tell whether a claimed improvement is real, and to build the thing
> that tests it?**

That is sharper than "go deeper". It admits the statistics of comparison, and enough of whatever
theory a subject's own papers assume that the reader can follow one critically — **which theory
that is depends on the subject, and the research says.** It still excludes mathematics that only
decorates.

**[I RECOMMEND]** Mathematics is written as raw LaTeX, never as `$…$`, so that a price like $5 stays
text. **Inline** mathematics uses `\(` and `\)`; **display** mathematics uses `\[` and `\]`, in a
fenced block. Simple inequalities and units in running prose stay as plain characters: ≤, ≥, ×, ≈.

## 9. Length

**[STATED]** **A page budget is an estimate, never a limit**, and this applies to the whole book as
well as to a chapter.

1. Never pad a chapter to reach a budget. Filler is worse than a short chapter.
2. Never cut material that earns its place to fit one.
3. **Never let a page count decide scope.** The failure to watch for is not padding or cutting —
   those are visible. It is deciding scope by the page count and then justifying it on other
   grounds.
4. Do not report progress as a fraction of a total, and do not raise the gap as a concern.

## 10. Markdown and build conventions

**[I RECOMMEND]** These are the conventions the build depends on.

**One thing genuinely stays open**: how chapters are grouped, and therefore whether a chapter's
number means anything beyond reading order. The **file naming does not** — it is fixed below, and
numbering straight through in reading order works whatever the grouping turns out to be.

**The layout, relative to the book's own root** — which is the directory containing `docs/`:

```
docs/        the planning documents. Never built, never published with the book
markdown/    the chapters, one file each, plus ZZ-review-answers.md. The only source of truth
data/        data a lab ships with, one directory per chapter
records/     one evidence record per chapter
research/    what the research returned, one file per area per run
tools/       the gates, the driver, the generators
latex/       generated. Never edited
```

- **One file per chapter.** `markdown/NN-slug.md`.
- **Headings:** `# Chapter Title` with no "Chapter N". First paragraph is the intro, then `##`
  sections and `###` subsections.
- **Callouts:** `> **Tip:** …`, `> **Note:** …`, `> **Warning:** …`. A `Note:` marks anything that
  will date.
- **Code blocks** always carry a language tag. `text` for output. Hand-drawn diagrams go in `text`
  blocks, at most 64 characters wide, every line the same width.
- **A block holding a program's captured output carries `<!-- captured -->` on the line before it.**
  This is how the render check knows not to police its width — a captured block may never be edited
  by hand, so a wide one is fixed in the program. **Writing that marker on a block no program
  produced defeats the check**, and no gate can detect it.
- **Generated appendices.** The glossary comes from the Key Terms tables and the cheat sheet from
  the Worth Memorising tables. Never edit a generated file by hand.
- **The index is generated too**, from the Key Terms tables: one entry per term, pointing at the
  chapter that owns it. **It is not hand-curated**, because a hand-curated index drifts from the
  glossary and the two then disagree about what a term is. The record's instruction to read index
  entries one by one is a check that no entry is a phrase bolded for emphasis rather than a term.
- **The Markdown is the only source of truth.** Never edit generated output.

**[AGREED 2026-11-06] The build toolchain is Markdown → pandoc → XeLaTeX → PDF.** Chosen because a
working version of this chain already exists elsewhere on this machine, so its failure modes are
known rather than to be discovered. **Every script is copied into this project, never shared**
(`PROCESS.md` §11), so improving this book's build cannot break anything else.

This unblocks gate 9, which is the only check that reads the built document rather than the source.

## 11. What the book never does

**[STATED]**

- **Never refers to anything outside itself that organises learning** — a website, a course, a
  curriculum, a learning path, a numbered step or a named track — and never to its own planning
  documents, research or machinery. Every chapter stands alone.
- Never organises by vendor, product, framework or model name. Always by capability.
- Never states a claim above the strength of its source.
- Never presents a subjective estimate as an established fact.
- Never gives a number without its source, or a ratio without a denominator a reader can check.
- Never deletes a superseded claim — **`PROCESS.md` §4.1 owns that rule**, and the book's side of it
  is that such a claim appears dated and labelled, never silently replaced.

## 12. Acceptance — a chapter is not done until

**[I RECOMMEND]**

- Every gate `CLEAN`, or `VACUOUS` with a reason given in the record (`GATES.md`).
- Every command and code sample has been run.
- Its acceptance questions can be answered from it — **or** answered by its `## What is disputed`
  section, which says plainly that the answer is not settled (§5 part 6).
- Every load-bearing claim has a `CLAIMS.tsv` row with its source and strength, and none is stated
  above it.
- The lab has been run **from the chapter text alone**, in a fresh folder, and produced a verdict.
- `You understand this when …` is present.
- `LEDGER-TAUGHT.md` has its row. `LEDGER-SHORTHAND.md` has any shorthand this chapter names.
- `OWNERSHIP.tsv` records every concept the chapter owns, with no collision.
- Every page has been looked at.
- Nothing refers to any outside scheme that organises learning, or to the book's own making (§11).
