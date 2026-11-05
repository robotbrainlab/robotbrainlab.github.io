# How this book gets built

**Written 2026-11-06.** The proposed development framework for *Modern AI: Research, Science and
Engineering*. The purpose of the book is in `GOAL.md` and is deliberately not restated here, so
that a disagreement about method cannot quietly change the goal.

**Status: proposal.** The owner approved *writing this down*. He has not approved its contents.
Markers are the same as `GOAL.md`: **[STATED]** the owner's words · **[AGREED]** accepted by both ·
**[I RECOMMEND]** my proposal, not a decision · **[OPEN]** undecided.

---

## 1. The design principle

**[I RECOMMEND]** one sentence to govern everything below. It is not mine — it is from the first
book's own record for chapter 45, explaining how every figure in a 58-page lab chapter got there:

> *"0 figures transcribed. Defect 68's lesson applied as a mechanism rather than as care."*

**Convert care into mechanism.** Care does not survive a project that never ends. Every rule in
this document that could have been written as "be careful about X" is instead written as a script
that refuses, a file a gate reads, or a brief that cannot be answered the wrong way.

The corollary, also from the first book, and it is the reason the gates are trusted there:

1. **A gate nobody reads the output of is worse than no gate.** Three of nine gates in the source
   project were at some point lying to the suite — one failing on an empty folder, one crashing on
   a renamed column, one printing CLEAN over nothing for a whole build.
2. **The only way to know a gate works is to break something it should catch and watch it exit 1.**
3. **A gate that checked nothing says so** — VACUOUS, never CLEAN.

---

## 2. What is carried over, and what each thing cost

**[STATED]** The owner asked that the new book *"follow all its rules, including the multiple
passes and agent reviews."* **[STATED]** Nothing else carries over: not the content, the scope, the
structure or the progression (`GOAL.md` §2.4).

Each rule below exists because something failed without it. The cost is recorded so that nobody
removes one to save time.

| Carried over | What it cost to learn |
|---|---|
| **One chapter at a time. Never a part at a time** | Context dilution is the cause of invented content. In the source project, *every* invented example across eighteen chapters traced to writing several chapters in one stretch |
| **Sources read in full, immediately before writing** — not earlier in the session | Named in the record, with what was read |
| **Non-scope declared in the record before writing** | Without an edge, review never terminates. Once a chapter claims to handle any case, "what about X?" is always a correct question and every answer creates the next one |
| **A completeness review against the sources, side by side** | Two reviews once passed a chapter with a whole section missing |
| **A fix-verification pass reading only the named changed passages** | The recurring defect is not writing badly — it is fixing a claim where you are looking and missing it where you are not. This pass caught 4 to 13 survivals per chapter, every chapter, without exception |
| **Every fix is a sweep, counted before and after, back matter first** | Four times in three chapters the survivor was in a Summary, a Key Terms row or a Review Answer — sections nobody re-reads because they look like a glossary rather than an argument |
| **In a lab, a corrected claim lives in six places and four are prose** | Programs narrate their own output, and that narration is captured into the chapter |
| **A staged driver that refuses, not a checklist** | *"Prose is what gets skipped"* |
| **The record carries the chapter's hash, written last** | Editing one character afterwards makes the record stale and fails the suite |
| **`amend` for a closed chapter that must change** | The quickest way past a stale hash is to re-hash by hand, which turns the record from evidence into decoration and leaves no trace that a published chapter moved |
| **The stopping rule, with round-2 classification** | Round 2 findings about the *subject* mean the chapter is mis-scoped. Round 2 findings that are round 1's own unswept fixes mean the fix round was itself a drafting event. Conflating them mis-fires — it did, on chapter 46 |
| **A taught-ledger with explicit "Do not" rows** | No gate looks at sequence. A chapter can be internally perfect and wrong about where it sits |
| **A shorthand ledger** — formal name against the word the field actually says | "RAG" appeared in no chapter, no glossary row and no question, while the subject ran across seven chapters |
| **A defect ledger of *classes*, each with its instance and the practice** | A list of mistakes is not reusable. A class is |
| **Concept ownership: each concept owned by exactly one chapter** | Eleven concepts in the first book are touched by several chapters |
| **Correctness outranks the source** | *"A source is evidence that something is said, never evidence that it is true"* |
| **Page budgets never bind, and never decide scope** | The failure is not padding or cutting. It is deciding scope by page count and justifying it on other grounds — which happened, and was caught from the actions rather than the explanation |
| **`You understand this when …`, one sentence per chapter** | The reader's own test |
| **An acceptance bank written before the chapters exist** | A standard the chapter must meet, not a summary of what it happens to contain |
| **The book ships its own lab data** | *"An expected result that depends on the reader's files holds for nobody"* |
| **Labs isolated: own folder, no credential files, keys from the environment** | The repository is public |
| **Claude writes. The owner reads and works through** | Decided, and argued about once already |

---

## 3. What must change, and why

**[I RECOMMEND]** Four structural differences between a book that gets finished and one that does
not. Every new mechanism in §4 answers one of them.

| # | Difference | Consequence |
|---|---|---|
| 1 | **It is never finished** | Revision, not writing, becomes the dominant cost. The inherited machinery pays full price on every revision, forever |
| 2 | **The subjects change each cycle** | Concept ownership cannot be fixed before drafting, which is what makes the taught-ledger work |
| 3 | **The material is contested** | "The chapter contains the answer" is sometimes an impossible standard, because no settled answer exists |
| 4 | **The content is dated** | A claim has a shelf life, and nothing in the inherited machinery carries it |

---

## 4. The new mechanisms

### 4.1 The claim is the unit of evidence

**[I RECOMMEND]** `CLAIMS.tsv`, one row per load-bearing claim. This is the central change.

```
id   claim   source   source_strength   verified_on   class   review_by   state   dependents
```

| Field | Values |
|---|---|
| `source_strength` | `peer-reviewed` · `preprint` · `vendor` · `own-measurement` · `source-absence` · `training-data-unverified` |
| `class` | `durable` (expect it to hold in five years) · `convention` (how it is done now) · `volatile` (settings, versions, prices, model names) |
| `state` | `verified` · `contested` · `superseded` |
| `dependents` | the chapters that rest on it |

What it buys, and this is the answer to difference 1:

- **Revision becomes cheap.** You re-verify *claims*, not chapters. An overturned claim names
  exactly which chapters reopen. Today, finding that costs a full rescan.
- **"Never state above the source" becomes a gate** rather than an intention. A chapter asserting
  something the file records as `contested` fails.
- **The cadence stops being arbitrary.** The book reports what is past its `review_by`. There is no
  twelve-week full rescan; there is a rescan of what expired. This is the answer to difference 4.
- **Superseded claims are kept, never deleted.** The honest record is that something *was*
  believed. It is also the lesson a research engineer most needs.

### 4.2 The dispute is a content type

**[I RECOMMEND]** A fixed shape, so contested material has somewhere to go: the claim, who holds
it, the counter-claim, who holds that, **what measurement would settle it**, and what to do
meanwhile.

The acceptance rule then changes from *"the chapter contains the answer"* to **"the chapter
contains the answer, or the state of the dispute, and says which."** This is the minimum change
that lets the first book's best idea survive contact with frontier material. It answers difference 3.

### 4.3 The reproduction lab has a decision rule, not an expected result

**[I RECOMMEND]** The first book's labs promise results that hold for every reader. A reproduction
lab cannot: the point is that the claim might not hold.

So its contract is: **state the published claim, the procedure, and the decision rule — what counts
as reproducing.** The lab passes if it runs and yields a verdict. **It does not have to agree with
the paper.**

Without this, a lab gets quietly tuned until it confirms its source — which is the same failure as
a published benchmark that compares against an untuned baseline, or an evaluation protocol under
which a random baseline scores well. **The illustrations I had here came from discarded research
and are withdrawn.** The principle stands on its own: a test whose outcome is fixed in advance is
not a test.

### 4.4 Ownership is a checked file

**[I RECOMMEND]** `OWNERSHIP.tsv`: concept → owning chapter → date assigned → previous owner if
moved. A gate fails on two chapters claiming one concept, or on a chapter teaching a concept it
does not own. This answers difference 2: the subject list can change each cycle without the
taught-ledger breaking.

**Note the distinction, because it is easy to collapse** (`GOAL.md` §2.4): duplication *between*
the old book and this one is fine and expected. Duplication *within* this book is a defect. This
file is about the second.

### 4.5 A lab runner that works from the chapter alone

**[I RECOMMEND]** In the first book the author ran the labs. A separate agent that runs a lab
**from the printed chapter only**, in a fresh folder, tests the book's actual promise —
*reproducible from the text alone* — rather than the author's memory of having tested it.

### 4.6 Every brief has a schema

**[I RECOMMEND]** Written once, not re-invented per brief. This is the fix for the failure of
2026-11-05, when three research agents ran for an hour without converging; one was launching four
more sub-agents when it was stopped.

```
QUESTION        one sentence. The output must answer exactly this
OUTPUT          named sections, in order. Nothing else is returned
UNIT            what one complete item of output looks like, field by field
TARGET          how many units. A cap, not a goal
BUDGET          searches, fetches, wall-clock
DELEGATION      depth allowed. Default: 0
STOPPING RULE   when to write up
PARTIAL         what to do when the budget runs out before the target
FORBIDDEN       what must not appear in the output
SAMPLING        what to report about your own coverage
```

**The two rules that make it terminate:**

1. **Completeness is per unit, and the unit count is capped.** "Report fewer complete units rather
   than more incomplete ones." An instruction that only rewards thoroughness has no fixed point.
2. **Delegation depth 0 by default.** An agent that may spawn agents has no budget.

---

## 5. The cycle

**[I RECOMMEND]**

```
RESEARCH → SELECT → PLAN → WRITE → VERIFY → CLOSE → EXPIRE
```

| Stage | What happens | Approved by |
|---|---|---|
| **Research** | One scout per area, fixed brief schema, delegation depth 0. Output: candidate **subjects**, each a complete unit, plus claims with sources | — |
| **Select** | Subjects filtered by the three-part test (`GOAL.md` §10): a mechanism worth understanding · live research · something buildable. **Rejections recorded with reasons** | **Owner** |
| **Plan** | Subjects become chapters. Ownership assigned. Structure chosen *now*, from the subjects that exist — never before (`GOAL.md` §5.3). Acceptance questions written **before** drafting | **Owner** |
| **Write** | One chapter. Five steps, unchanged from the first book | — |
| **Verify** | Four passes (§7) | — |
| **Close** | Record hashed, ledgers updated, claims linked, changelog entry written | — |
| **Expire** | Claims past `review_by` re-verified. Only affected chapters reopen | — |

**The key property:** EXPIRE replaces the full rescan. A cycle's size is set by what has actually
gone stale, not by the calendar.

### 5.1 What happens when a cycle comes back a different shape

The owner asked this on 2026-11-06 and the framework had no answer. This section is the answer.

**First, an error in the earlier design.** `GOAL.md` §8 says *"a chapter is a question with a
current answer attached, where the question outlives every answer it will carry."* Then §5 above
built the structure out of **subjects**. Subjects are the fast layer. A structure resting on them is
threatened by every cycle.

**[I RECOMMEND] the correction: the book's spine is a set of durable questions. Subjects are the
current answers.**

| Durable question | Today's answer, which will change |
|---|---|
| How do I know a difference is real? | These estimators, these sample sizes |
| What does it cost to serve a model? | These numbers, this hardware |
| How do I adapt a model to my own task? | Today's methods and their costs |

A new subject goes to the question it answers. A dead subject leaves its question standing. The
chapter survives its own content.

#### The six operations

**[I RECOMMEND]** Each is a named operation with a procedure and a record, not a judgement call.
Every one writes a changelog row.

| What the cycle brings | Operation | Cost | Who decides |
|---|---|---|---|
| A new subject answering an existing question | **ADD** | One chapter, or one section | Claude |
| A subject outgrowing its chapter | **SPLIT** | Two chapters; ownership reassigned; both records amended | Claude |
| Two subjects converging | **MERGE** | One chapter; the retired one keeps a record saying where it went | Claude |
| A subject that stops being practice | **RETIRE** | The chapter stays, with a dated note: this *was* current practice | Claude |
| A new subject answering **no existing question** | **NEW QUESTION** | A structural change | **Owner** |
| An area that turns out not to be an area | **RECARVE** | Expensive. No mechanism makes it cheap | **Owner** |

**Nothing is deleted.** A retired subject keeps its chapter with a dated note. This is not
tidiness: it is the lesson a research engineer most needs — that something was believed, by careful
people, and then was not.

#### The test on the carving itself

**[I RECOMMEND]** Every cycle records how many operations of each kind it needed. Then:

- Mostly `ADD` and `RETIRE` → the carving is sound.
- A `RECARVE` every cycle → **the carving is wrong, and the book should be flat.** No parts.
  Chapters are subjects, and reading maps give orders through them.

That is a falsifiable test on the structure, and it runs for free.

#### One trade-off that is not free

The first book binds its chapters tightly. Chapter 11 opens: *"Chapter 9 called a layer a box of
the right shape and promised to open it."* That is part of why it reads as one argument rather than
fifty essays. **Those promises are exactly what makes re-ordering expensive.**

| Choice | Buys | Costs |
|---|---|---|
| Reference by **chapter and promise**, as the first book does | A book that reads as one continuous argument | Every re-order is a sweep through the prose |
| Reference by **concept**, with the location looked up | Re-ordering is nearly free | Less of that one-continuous-argument feeling |

**[I RECOMMEND]** reference by concept, because this book will be re-ordered many times and the
first book never was. It is a real loss and the owner should decide it knowingly. **[OPEN]**

#### What maintenance actually looks like, per cycle

1. `CLAIMS.tsv` reports every claim past its `review_by`. **Only those get re-checked.**
2. Each re-checked claim becomes `verified`, `contested` or `superseded`.
3. A superseded claim names its `dependents`. **Only those chapters reopen.**
4. The six operations are applied, and each writes a row.
5. `CHANGELOG.md` — "What Changed in This Edition" — is **generated from those rows**, not written
   by hand.

**The work is proportional to what changed, not to how big the book is.** That is the whole purpose
of the claims file, and the only reason a book like this survives its third cycle.

---

## 6. The chapter loop

**[STATED]** Carried over unchanged. Five steps, in order. Do not reorder, and do not soften
step 1's timing.

| # | Step |
|---|---|
| 1 | **Read the sources in full, immediately before writing.** Not earlier in the session. Named in the record |
| 2 | **Write the chapter** |
| 3 | **Completeness review** — a subagent reads the sources and the chapter side by side |
| 4 | **Apply the findings**, verifying each before accepting it, and sweep each one book-wide, counted |
| 5 | **Fix-verification** — a second subagent reads **only the changed passages**, named |

**The stopping rule.** One review round is the norm. If round 1 finds no false-teaching error, fix
the rest and ship — no second round. If it does, fix and run one more. If round 2 still finds them,
**classify before concluding**: findings about the chapter's *subject* mean mis-scope, so narrow it;
findings that are round 1's own unswept fixes mean the fix round was a drafting event, so sweep and
verify once more. A third round being contemplated means something structural is wrong — stop and
ask.

---

## 7. The verification passes

**[I RECOMMEND]** Four. Two are inherited; two are new.

| Pass | Reads | Finds |
|---|---|---|
| **1 · Completeness** | Sources and chapter, both in full | Omission · alteration · false claim · self-contradiction · out-of-boundary theory · cross-chapter error |
| **2 · Adversarial claims** *(new)* | The chapter against `CLAIMS.tsv` | Any claim stated above its recorded source strength |
| **3 · Lab execution** *(new)* | The chapter text only, in a fresh folder | Anything that does not run; anything that runs and disagrees |
| **4 · Fix-verification** | **Only the named changed passages** | Survivals, and errors the fixes introduced |

**Every review brief includes**, because the briefs that work are long and specific:

- the chapter path and its sources, named;
- *"read BOTH in full"*, and anything not read closely;
- the six finding categories above;
- the chapter's **declared non-scope**, so findings outside it can be rejected;
- the relevant taught-ledger rows and boundary cases, so they are not reported as errors — but ask
  the agent to say if it thinks one is wrong;
- specific claims to verify independently, named;
- *"If unsure, say so rather than asserting. A wrong finding costs more than a missed one."*

For pass 4, additionally **every changed passage, listed**. A re-check told only "look at the
chapter" re-reads everything and finds what pass 1 already found.

---

## 8. The agents, and how they are coordinated

**[I RECOMMEND]**

| Agent | Job | May delegate |
|---|---|---|
| **Scout** | One research area → subject units | No |
| **Claim verifier** | Re-check one claim at source, adversarially | No |
| **Writer** | One chapter | No |
| **Completeness reviewer** | Pass 1 | No |
| **Adversary** | Pass 2 | No |
| **Lab runner** | Pass 3 | No |
| **Fix verifier** | Pass 4 | No |

**Coordination:**

- **No agent delegates.** Depth 0, everywhere, unless a brief states otherwise and says why.
- **One chapter in flight at a time.**
- **Scouts may run in parallel.** Everything after SELECT is serial.
- **`CLAIMS.tsv` is the only shared mutable state.** The verifier and the writer touch it in
  different phases, never at the same time.
- **An agent reports its own sampling**: what it searched, what it could not reach, what its
  sources over-represent, and where a source is selling the thing it describes.

---

## 9. The gates

**[I RECOMMEND]** Carry over the first book's eleven, and add three that the new mechanisms require.

| Gate | Catches | Status |
|---|---|---|
| Voice | Any sentence revealing the book's origins | Carried over |
| Boundary | Theory outside the declared maths line | Carried over |
| Render | Markdown that renders wrong on the page | Carried over |
| Arithmetic | Every printed equation, evaluated — chains too | Carried over |
| Record | Checklist complete, evidenced, fresh, in order | Carried over |
| Coverage | Plan → chapter: what was promised and is missing | Carried over |
| Absolutes | Lists every absolute for testing | Carried over |
| Inputs | Terms used before the book gives them | Carried over |
| Outline | The PDF outline nests correctly | Carried over |
| Glossary · cheat sheet | Generated appendices match their source tables | Carried over |
| Acceptance bank | Each record names the questions it owns | Carried over |
| **Claims** | Every load-bearing claim in a chapter has a `CLAIMS.tsv` row, and no claim is stated above its recorded strength | **New** |
| **Ownership** | No concept claimed by two chapters; no chapter teaching one it does not own | **New** |
| **Expiry** | Lists every claim past its `review_by` | **New** |

---

## 10. Acceptance criteria

**[I RECOMMEND]**

### Per chapter

Everything the first book required, plus three:

- All gates pass; every command run; every page looked at
- Acceptance questions answerable from the chapter, **or** answered by a dispute record that says so
- `You understand this when …` present
- **Every load-bearing claim has a `CLAIMS.tsv` row with its source and strength**
- **Pass 3 ran the lab from the chapter text and it produced a verdict**
- **Pass 2 clean: no claim stated above its source strength**

### Per cycle — new, because the first book had no cycles

- Every claim past `review_by` re-verified or marked `superseded`
- Every superseded claim retained, with the date and the reason
- The changelog entry distinguishes **new** from **revised** from **overturned**
- `OWNERSHIP.tsv` has no collisions
- Nothing the owner rejected at SELECT appears in the book

---

## 11. Documentation architecture

**[I RECOMMEND]** A small multi-file structure, not one file. The owner's preference was one
comprehensive file; the reasoning against it is in the chat proposal of 2026-11-06 and in short:
loading one very long file into every agent spends context on irrelevance, and **context dilution
is the documented cause of invented content in this project**. The single file makes the known
failure mode more likely. The first book shipped 57 chapters on seven kinds of document.

| File | Job | Change rate | Audience |
|---|---|---|---|
| `CLAUDE.md` | Entry point. Short. Reading order and **the precedence rule** | Almost never | Agents |
| `GOAL.md` | Why the book exists | Rarely; owner approves | Owner |
| `GUIDE.md` | The spec: structure, style, maths line, chapter anatomy, lab rules | Rarely | Both |
| `PROCESS.md` | This file: the cycle, the loop, the passes, brief schemas, stopping rules | When the method changes | Agents |
| `PLAN.md` | A stable spine plus this cycle's subjects, clearly separated | Every cycle; owner approves | Owner |
| `CLAIMS.tsv` | Every load-bearing claim | Continuously | Machine |
| `OWNERSHIP.tsv` | Concept → owning chapter | Per cycle | Machine |
| `LEDGER-TAUGHT.md` · `LEDGER-DEFECTS.md` · `LEDGER-SHORTHAND.md` | Carried over | Continuously | Both |
| `records/NN.md` | Per-chapter evidence | Once, plus amendments | Machine |
| `briefs/*.md` | Filled briefs, kept so a result can be read against what was asked | Per brief | Both |
| `CHANGELOG.md` | "What Changed in This Edition" — generated | Every cycle | Owner |

**Three rules that make multiple files safe**, which is the real answer to the owner's concern:

1. **One file is authoritative per topic**, and `CLAUDE.md` says which. A rule in two files is a
   defect, and a gate can grep for duplicated rule headings.
2. **The precedence order is written down.** The repository beats every document; a machine-checked
   file beats prose; `GUIDE.md` beats `PROCESS.md` on anything about the book itself. This is the
   first book's own rule, which cites measured evidence that agents follow a stale instruction file
   over the actual code 90.1% of the time.
3. **Nothing is restated for convenience.** Cross-reference by filename and section.

**[I RECOMMEND]** one more thing, and it is about the first book rather than this one: **copy its
tooling, do not share it.** That book is finished as of 2026-10-31. A shared script means improving
this book can break that one.

---

## 12. What is not decided

**[OPEN]** Everything in this file, pending the owner's review.

**[OPEN]** From `GOAL.md`, and none of these block the research:

- The book's shape — breadth against depth (§10)
- The mathematics boundary (§10)
- Which area goes deep, if the shape is asymmetric (§10)
- The structure and whether four parts fit (§5.3) — **and this one must wait for the subjects**
- Whether the book is for the owner alone (§10)
- Confirmation of the scope-versus-depth reading (§2.4)

**[OPEN]** The three problems in `GOAL.md` §8 that §4 attacks but does not finish: the revision
cost over many cycles, the acceptance rule for contested material, and ownership moving between
cycles. §4.1, §4.2 and §4.4 are proposed answers. None has been tested.
