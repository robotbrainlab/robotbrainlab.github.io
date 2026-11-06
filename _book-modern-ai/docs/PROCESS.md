# How this book gets built

**Written 2026-11-06.** The proposed development framework for *Modern AI: Research, Science and
Engineering*. The purpose of the book is in `GOAL.md` and is deliberately not restated here, so
that a disagreement about method cannot quietly change the goal.

**Status: proposal.** The owner approved *writing this down*. He has not approved its contents.
Markers are the same as `GOAL.md`: **[STATED]** the owner's words · **[AGREED]** accepted by both ·
**[I RECOMMEND]** my proposal, not a decision · **[OPEN]** undecided.

---

## 1. The design principle

**[I RECOMMEND]** one sentence to govern everything below:

> **Convert care into mechanism.**

The worked example is a figure in a chapter. Asking a writer to transcribe a program's output
carefully produces an error eventually; splicing the figure from the program's own captured output
means nothing is transcribed at all, so the error cannot happen. The second costs a few lines of
script and removes the failure mode instead of guarding against it.

**Care does not survive a project that never ends.** Every rule in this document that could have
been written as "be careful about X" is instead a script that refuses, a file a gate reads, or a
brief that cannot be answered the wrong way.

**This file owns that principle**; `GOAL.md` §11 cites it. **The three rules about the gates
themselves are `GATES.md`'s** and are not repeated here.

---

## 2. The rules, and why each exists

**[STATED]** The owner asked for **multiple review passes and agent reviews**, and for the method to
be followed rather than improvised. Everything else about the book is independent (`GOAL.md` §2.4).

**Each rule has a reason, and the reason is stated so nobody removes the rule to save time.** A
reason is given as a mechanism — *this is how the defect happens* — rather than as a story about an
occasion, because a story invites the reply that it will not happen here.

| Rule | Why it exists |
|---|---|
| **One chapter at a time. Never a part at a time** | Context dilution causes invented content. Writing several chapters in one stretch pushes the first chapter's sources out of working context, and it then gets written from the pattern of the previous chapters rather than from its material |
| **Sources read in full, immediately before writing** — not earlier in the session | Reading earlier in the session means the sources are out of working context by the time the chapter is written, and the chapter then gets written from memory of them. Named in the record, with what was read |
| **Non-scope declared in the record before writing** | Without an edge, review never terminates. Once a chapter claims to handle any case, "what about X?" is always a correct question and every answer creates the next one |
| **A completeness review against the sources, side by side** | A reviewer checks what is present against the sources; nothing in that act surfaces what is absent from both |
| **A fix-verification pass reading only the named changed passages** | The recurring defect is not writing badly — it is fixing a claim where you are looking and missing it where you are not. A reviewer reading only the changed passages finds survivals a full re-read buries in its own findings |
| **Every fix is a sweep, counted before and after, back matter first** | One claim appears in several phrasings, and the writer applying a fix sees the one the finding quoted. The back matter goes first because a summary, a key-term row and an answer key are read as settled — they look like a glossary rather than an argument — so they are where a fix goes to not happen |
| **In a lab, one claim lives in the prose *and* in the code** | A lab's programs print counts, comparisons and universals, and that printed output is captured into the chapter. So the same claim can exist in the body, the program, the captured block, the summary, a key-term row and an answer — **six places on that list, four of them prose** — and fixing the prose alone makes the chapter contradict its own printed output |
| **A staged driver that refuses, not a checklist** | A checklist in prose is read once and skipped thereafter. A program that will not advance until the current stage's evidence is present cannot be skipped — see §6.1 |
| **The record carries the chapter's hash, written last** | Editing one character afterwards makes the record stale and fails the suite |
| **`amend` for a closed chapter that must change** | The quickest way past a stale hash is to re-hash by hand, which turns the record from evidence into decoration and leaves no trace that a published chapter moved |
| **The stopping rule, with round-2 classification** | Round 2 findings about the *subject* mean the chapter is mis-scoped. Round 2 findings that are round 1's own unswept fixes mean the fix round was itself a drafting event. Conflating them mis-fires, and sends a sound chapter back to be narrowed |
| **A taught-ledger with explicit "Do not" rows** | No gate looks at sequence. A chapter can be internally perfect and wrong about where it sits |
| **A shorthand ledger** — the clear name against the word the field actually says | A book naturally uses its own vocabulary throughout. A reader who searches it for the word they have heard elsewhere then finds nothing, even where the subject is covered at length |
| **A defect ledger of *classes*, each with its instance and the practice** | A list of mistakes is not reusable. A class is |
| **Concept ownership: each concept owned by exactly one chapter** | Some concepts are naturally touched by several chapters, and without an owner each one re-teaches it slightly differently |
| **Correctness outranks the source** (`GUIDE.md` §5 owns the rule) | Received explanations in any technical field include confident wrong ones. A book that follows its sources faithfully will reproduce them, and the reader has no way to tell |
| **Page budgets never bind, and never decide scope** (`GUIDE.md` §9) | Padding and cutting are visible and easy to resist. The failure that is not visible is deciding **scope** by the page count and then justifying the decision on other grounds — which can only be caught by looking at what was dropped, not at the reason given |
| **`You understand this when …`, one sentence per chapter** | The reader's own test |
| **An acceptance bank written before the chapters exist** (`ACCEPTANCE.md`) | A question written after a chapter can only ask about what the chapter contains, so it cannot detect an omission. Written first, it is a standard the chapter must meet |
| **The book ships its own lab data** (`GUIDE.md` §6) | An expected result that depends on the reader's own files holds for nobody, so the lab cannot be checked by anyone |
| **Labs isolated: own folder, no credential files, keys from the environment** | The repository is public |
| **Claude writes. The owner reads and works through everything** | The owner's decision. It is settled: do not propose that he writes it |

---

## 3. The four properties the machinery has to handle

**[I RECOMMEND]** Four properties of this book that an ordinary book does not have. **Machinery
built for a book that gets finished fails on each of them**, so each of the mechanisms in §4
answers one.

| # | Property | Consequence |
|---|---|---|
| 1 | **It is never finished** | Revision, not writing, becomes the dominant cost. A per-chapter cost that is paid once in a finished book is paid on every revision here, forever |
| 2 | **The subjects change each cycle** | Concept ownership cannot be fixed before drafting, which is what makes the taught-ledger work |
| 3 | **Some of the material will be contested** | "The chapter contains the answer" is then an impossible standard, because no settled answer exists to contain. How much is contested is for the research to say |
| 4 | **The content is dated** | A claim has a shelf life, so something has to carry it. Nothing in a chapter does |

---

## 4. The new mechanisms

### 4.1 The claim is the unit of evidence

**[I RECOMMEND]** `CLAIMS.tsv`, one row per load-bearing claim. This is the central change.

**The schema is in `CLAIMS.tsv`'s own header and comment block, and nowhere else.** A copy here
would drift from the file the moment a column changed, and the copy is what a reader would trust.

Eleven columns. The ones worth naming here, because the rest of this file refers to them:
`maturity` (is the science settled), `class` (how long it will hold), `review_by` (when to look
again), `state` (where it stands in this project) and `dependents` (the chapters that rest on it).

What it buys, and this is the answer to property 1:

- **Revision becomes cheap.** You re-verify *claims*, not chapters. An overturned claim names
  exactly which chapters reopen. Today, finding that costs a full rescan.
- **"Never state above the source" becomes checkable** rather than aspirational, in two parts: a
  gate checks the bookkeeping — a `contested` claim whose chapter carries no dispute section fails —
  and **pass 2 reads the prose**, because whether a sentence overstates its source is judgement and
  no gate can do it (`GATES.md` gate 12).
- **The cadence stops being arbitrary.** The book reports what is past its `review_by`. There is no
  twelve-week full rescan; there is a rescan of what expired. This is the answer to property 4.
- **Superseded claims are kept, never deleted.** The honest record is that something *was*
  believed. It is also the lesson a research engineer most needs.

### 4.2 The dispute is a content type

**[I RECOMMEND]** Contested material needs a place in a chapter, and **`GUIDE.md` §5 owns its
shape** — the claim, the counter-claim, who holds each, what measurement would settle it, and what
to do meanwhile. What belongs in this file is the consequence for acceptance.

The acceptance rule changes from *"the chapter contains the answer"* to **"the chapter
contains the answer, or the state of the dispute, and says which."** This is the minimum change
that lets an acceptance standard survive contact with disputed material. It answers property 3.

### 4.3 The reproduction lab has a decision rule, not an expected result

**[I RECOMMEND]** **`GUIDE.md` §6 owns the two lab forms and the reproduction contract.** The one
line that belongs here, because it is about the method rather than the book: a reproduction lab
**passes if it runs and yields a verdict, whatever the verdict is.**

Without this, a lab gets quietly tuned until it confirms its source. **A test whose outcome is
fixed in advance is not a test.**

### 4.4 Ownership is a checked file

**[I RECOMMEND]** `OWNERSHIP.tsv`: concept → owning chapter → date assigned → previous owner if
moved. A gate fails on two chapters claiming one concept, or on a chapter teaching a concept it
does not own. This answers property 2: the subject list can change each cycle without the
taught-ledger breaking.

**Note the distinction, because it is easy to collapse** (`GOAL.md` §2.4): duplication between this
book and **anything outside it** is fine and expected. Duplication **within** this book is a
defect. This file is about the second.

### 4.5 A lab runner that works from the chapter alone

**[I RECOMMEND]** A writer who runs their own lab cannot test whether the chapter describes it,
because they know what they meant. **A separate agent, running the lab from the printed chapter
only, in a fresh folder, tests the book's actual promise** — reproducible from the text alone —
rather than the author's memory of having tested it. `briefs/pass-3-lab.md` is the brief.

### 4.6 Every brief has a schema

**[I RECOMMEND]** Written once, not re-invented per brief.

**Why a brief needs a schema at all.** An instruction that only rewards thoroughness has no fixed
point: the agent can always search more, and will. A brief without a stated stopping condition and
a capped output therefore does not terminate — and one that may start further agents has no budget
at all, because each new agent brings its own.

```
QUESTION        one sentence. The output must answer exactly this
OUTPUT          named sections, in order. Nothing else is returned
UNIT            what one complete item of output looks like, field by field
TARGET          how many units. A cap, not a goal
BUDGET          counted: searches, fetches, or runs. Whatever the agent can exhaust
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
EXPIRE → RESEARCH → CONFIRM → SELECT → PLAN → WRITE → VERIFY → CLOSE
```

| Stage | What happens | Approved by |
|---|---|---|
| **Expire** | Every claim past its `review_by` is re-verified by `briefs/claim-verifier.md` and becomes `verified`, `contested` or `superseded`. **A superseded claim names its dependent chapters, and only those reopen.** `tools/verify-expiry.py` must be clean before the next stage begins | — |
| **Research** | One scout per area, fixed brief schema, delegation depth 0. Output: candidate **subjects**, each a complete unit, plus claims with sources | — |
| **Confirm** | Every scout claim becomes a `CLAIMS.tsv` row (§5.1). **Then `briefs/claim-verifier.md` runs on each claim whose `maturity_basis` is `provisional` and which a candidate chapter would rest on** — because a chapter may not rest on an unestablished maturity, and nothing else in the cycle discharges that | — |
| **Select** | Subjects filtered by the three-part test (`GOAL.md` §10): a mechanism worth understanding · live research · something buildable. **Rejections recorded with reasons** | **Owner** |
| **Plan** | Subjects become chapters. Ownership assigned. Structure chosen *now*, from the subjects that exist — never before (`GOAL.md` §5.3). Acceptance questions written **before** drafting | **Owner** |
| **Write** | One chapter. Six steps, §6 | — |
| **Verify** | Four passes (§7) | — |
| **Close** | Record hashed, ledgers updated, claims' `dependents` filled, operation rows written for the changelog | — |

**EXPIRE is first, and the order matters.** Put it last and the cycle eats itself: the expiry check
would demand that stale claims be re-verified at a point before the stage that re-verifies them.
First, it also guarantees **no cycle is researched on top of claims known to be stale.**

**A cycle boundary is the moment EXPIRE completes.** `tools/verify-expiry.py` needs a definition and
this is it: CLOSE writes a dated `cycle-boundary` line into `CHANGELOG.md` when the following
EXPIRE finishes clean, and the gate reads the last such line. Between boundaries the gate only
reports; at a boundary it fails on any claim past its review date.

**The key property:** EXPIRE replaces the full rescan. A cycle's size is set by what has actually
gone stale, not by the calendar.

### 5.1 From a scout's claim to a claims row

The scout returns six fields. `CLAIMS.tsv` has eleven. **This is the transformation, and it happens
at CONFIRM**, not by a scout and not by a writer:

| Column | Where it comes from |
|---|---|
| `claim` `source` `maturity` `maturity_basis` `class` | The scout's row, unchanged |
| `source_strength` | The scout's `strength` field, renamed to the file's column name. **Same vocabulary, different column name** — the scout's brief calls it `strength` because the row it writes has no other kind |
| `id` | Assigned here: **the area's number, a hyphen, and a zero-padded counter** — `A03-001`. A number rather than a slug, because a slug can itself contain a hyphen and then the id cannot be parsed. The area's number comes from the approved list at step 4. Never reused, never renumbered |
| `verified_on` | **The date the claim verifier ran**, not the date the scout read it. A row the verifier has not touched leaves this empty, which is what marks it unconfirmed |
| `review_by` | Computed from `class` and `maturity` by the policy in `GATES.md` |
| `state` | `unverified` on arrival. Becomes `verified`, `contested` or `superseded` only through the claim verifier |
| `dependents` | Empty until a chapter lists the claim in its `## Claims` section. Filled at CLOSE, not before |

**Two rules that follow.** A row with an empty `verified_on` has `state = unverified`, and a chapter
may not rest on it. And `dependents` is written from the chapter, never from the plan — a chapter
that does not name a claim does not depend on it, whatever the plan intended.

### 5.2 What happens when a cycle comes back a different shape

A cycle can return more subjects than expected, fewer, or ones that do not fit where the last cycle
put them. **The structure has to absorb that without being rebuilt**, and what makes that possible
is which layer the structure rests on.

**Subjects are the fast layer.** §5 above turns subjects into chapters, so a structure resting on
subjects is threatened by every cycle: each new subject is a candidate chapter and each dead one
leaves a hole. `GOAL.md` §8 gives the way out — *"a chapter is a question with a current answer
attached, where the question outlives every answer it will carry."*

**[I RECOMMEND] the book's spine is a set of durable questions. Subjects are the current answers.**

| Durable question | Today's answer, which will change |
|---|---|
| How do I know a difference is real? | These estimators, these sample sizes |
| What does it cost to run this, and what drives the cost? | These numbers, this hardware |
| What breaks when this is put into production? | Today's failure modes and their fixes |

**These three are illustrations of the *form*, not a claim about what the book will contain.** Each
is drawn from a capability the owner's current specification already names, so none presupposes a
research outcome. **Which questions the book actually carries comes from the research.**

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
tidiness, and §4.1 above owns the rule and its reason. The consequence for an **operation**, which
is what this section is about: `RETIRE` changes a chapter's standing and never removes it.

#### The test on the carving itself

**[I RECOMMEND]** Every cycle records how many operations of each kind it needed. Then:

- Mostly `ADD` and `RETIRE` → the carving is sound.
- A `RECARVE` every cycle → **the carving is wrong, and the book should be flat.** No parts.
  Chapters are subjects, and reading maps give orders through them.

That is a falsifiable test on the structure, and it runs for free.

#### One trade-off that is not free

Binding chapters together with promises — *"chapter 9 promised to open this"* — is part of what
makes a book read as one argument, and it is exactly what makes re-ordering expensive. **`GUIDE.md`
§7 owns that decision**, with the trade-off and the recommendation. It is `[OPEN]`, and it matters
here only because a book revised on a cycle re-orders often.

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

**Six steps, in order. Do not reorder, and do not soften step 1's timing.**

| # | Step |
|---|---|
| 1 | **Read the sources in full, immediately before writing.** Not earlier in the session. Named in the record |
| 2 | **Write the chapter** |
| 3 | **Pass 1, completeness review** — a subagent reads the sources and the chapter side by side |
| 4 | **Apply the findings**, verifying each before accepting it, and sweep each one book-wide, counted |
| 5 | **Pass 2, adversarial claims**, then **pass 3, lab execution** from the chapter text alone. Apply and sweep what they find |
| 6 | **Pass 4, fix-verification** — a subagent reads **only the changed passages**, named |

**Six steps, four passes** (§7). Passes 2 and 3 sit at step 5 because both read the chapter *after*
pass 1's fixes land — running them earlier checks text that is about to change.

**The stopping rule.** One review round is the norm. If round 1 finds no false-teaching error, fix
the rest and ship — no second round. If it does, fix and run one more. If round 2 still finds them,
**classify before concluding**: findings about the chapter's *subject* mean mis-scope, so narrow it;
findings that are round 1's own unswept fixes mean the fix round was a drafting event, so sweep and
verify once more. A third round being contemplated means something structural is wrong — stop and
ask.

### 6.1 The driver

**`tools/chapter.py` is the loop, as a program.** A checklist in prose is read once and skipped
thereafter; a program that refuses to advance cannot be skipped. Four stages, and each refuses:

| Command | Refuses when |
|---|---|
| `chapter.py begin NN-slug` | The chapter file already exists, or the record's `question`, `sources` or `non-scope` fields are empty. **It creates the record from `RECORD-TEMPLATE.md`**, so a chapter cannot start without one |
| `chapter.py written NN-slug` | Any box in the *Before writing* or *While writing* sections is unticked, or is ticked with nothing after it |
| `chapter.py reviewed NN-slug` | Any of the four pass verdicts is missing. **On success it writes the `sha256` last**, so any later edit makes the record stale and fails the record gate |
| `chapter.py amend NN-slug "reason"` | The record is not closed, no reason is given, or the chapter has not actually changed. It appends a dated line to `amended:` and re-hashes |

**`amend` exists because the obvious way to change a closed chapter is dishonest.** The record
carries the chapter's hash, so an edit makes it stale — and the quickest way past that is to
re-hash by hand, which turns the record from evidence into decoration and leaves no trace that a
published chapter moved. `amend` is the honest path, and the record gate checks every amendment is
dated, reasoned, and not earlier than the review it follows.

---

## 7. The verification passes

**[I RECOMMEND]** Four, each reading something the others do not. **Passes 2 and 3 exist because
of §3's properties 3 and 4**: a book carrying contested and dated material needs a reader checking
claims against their recorded strength, and a reader proving a lab runs from the text alone.

| Pass | Reads | Finds |
|---|---|---|
| **1 · Completeness** | Sources and chapter, both in full | Omission · alteration · false claim · self-contradiction · out-of-boundary theory · cross-chapter error |
| **2 · Adversarial claims** | The chapter against `CLAIMS.tsv` | Any claim stated above its recorded source strength |
| **3 · Lab execution** | The chapter text only, in a fresh folder | Anything that does not run; anything that runs and disagrees |
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
| *(no agent)* | **Writing a chapter is not delegated.** It is the loop in §6, done in the main session with the sources open | — |
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

**Specified in `GATES.md`**, which says for each gate what it reads, what makes it fail and what it
prints. This table is the index; that file is the specification. **`GATES.md` also holds the policy
for setting a claim's review date**, which `tools/verify-expiry.py` reads.

| Gate | Catches |
|---|---|
| Voice | Any sentence revealing the book's own making |
| Boundary | Theory outside the declared maths line |
| Render | Markdown that renders wrong on the page |
| Arithmetic | Every printed equation, evaluated — chains too |
| Record | Checklist complete, evidenced, fresh, in order |
| Coverage | Plan → chapter: what was promised and is missing |
| Absolutes | Lists every absolute for testing |
| Inputs | Terms used before the book gives them |
| Outline | The PDF outline nests correctly |
| Glossary · cheat sheet | Generated appendices match their source tables |
| Acceptance bank | Each record names the questions it owns |
| Claims | Every load-bearing claim in a chapter has a `CLAIMS.tsv` row, and no claim is stated above its recorded strength |
| Ownership | No concept claimed by two chapters; no chapter teaching one it does not own |
| Expiry | Lists every claim past its `review_by` |

**Three cannot be built yet, and `GATES.md` says so in each one's own entry** rather than here: the
boundary gate waits on the mathematics decision, the inputs gate on vocabulary the research seeds,
and the outline gate on the build toolchain.

---

## 10. Acceptance criteria

**[I RECOMMEND]**

### Per chapter

**`GUIDE.md` §12 owns this list** and this file does not restate it. `RECORD-TEMPLATE.md` turns it
into checkboxes, which is applying it rather than copying it. **Three criteria belong here instead**,
because they are properties of the process rather than of the book:

- **Every load-bearing claim has a `CLAIMS.tsv` row with its source and strength**
- **Pass 2 clean: no claim stated above its source strength**
- **Pass 3 ran the lab from the chapter text alone and it produced a verdict**

### Per cycle

- Every claim past `review_by` re-verified or marked `superseded`
- Every superseded claim retained, with the date and the reason
- The changelog entry distinguishes **new** from **revised** from **overturned**
- `OWNERSHIP.tsv` has no collisions
- Nothing the owner rejected at SELECT appears in the book

---

## 11. Documentation architecture

**[I RECOMMEND]** A small multi-file structure, not one file. The owner's preference was one
comprehensive file. The reasoning against it: an agent given one very long file spends context on
what it does not need, and **context dilution is what makes an agent invent content** — so a single
file makes the known failure mode more likely, not less. A fix-verifier needs the changed passages
and the finding categories; it does not need the build conventions.

| File | Job | Change rate | Audience |
|---|---|---|---|
| `../CLAUDE.md` | Entry point. Short. Reading order and **the precedence rule** | Almost never | Agents |
| `GOAL.md` | Why the book exists | Rarely; owner approves | Owner |
| `GUIDE.md` | The spec: structure, style, maths line, chapter anatomy, lab rules | Rarely | Both |
| `PROCESS.md` | This file: the cycle, the loop, the passes, brief schemas, stopping rules | When the method changes | Agents |
| `PLAN.md` | A stable spine plus this cycle's subjects, clearly separated | Every cycle; owner approves | Owner |
| `CLAIMS.tsv` | Every load-bearing claim | Continuously | Machine |
| `OWNERSHIP.tsv` | Concept → owning chapter | Per cycle | Machine |
| `LEDGER-TAUGHT.md` · `LEDGER-DEFECTS.md` · `LEDGER-SHORTHAND.md` | What the reader has been given · what the gates cannot catch · the field's own words | Continuously | Both |
| `ROADMAP.md` | Which of the eleven steps we are on, and what is next. **Read first** | Every step | Owner |
| `GATES.md` | What each gate reads, fails on and prints; and the review-date policy | When a gate changes | Both |
| `ACCEPTANCE.md` | The questions each chapter must answer, written before any chapter | Per cycle, before drafting | Both |
| `RECORD-TEMPLATE.md` | The per-chapter record, copied into `records/` | Rarely | Both |
| `CHANGELOG.md` | "What Changed in This Edition" — generated | Every cycle | Owner |
| `data/<chapter-slug>/` | Data a lab ships with | Per chapter | Both |
| `records/NN-slug.md` | Per-chapter evidence | Once, plus amendments | Machine |
| `briefs/*.md` | Filled briefs, kept so a result can be read against what was asked | Per brief | Both |

**Three rules that make multiple files safe**, which is the real answer to the owner's concern:

1. **One file is authoritative per topic**, and `../CLAUDE.md` says which. **A rule may be referred
   to from several files; it may be *stated* in only one.** A second statement is a defect even while
   the two agree, because they will drift. Where a document needs a rule it does not own, it cites
   the owner by filename and section.
2. **The precedence order is written down.** The repository beats every document; a machine-checked
   file beats prose; `GUIDE.md` beats `PROCESS.md` on anything about the book itself. This is the
   rule stated in `../CLAUDE.md`. The figures it cites come from a single preprint and are recorded
   at that strength: evidence, not settled fact.
3. **Nothing is restated for convenience.** Cross-reference by filename and section.

**[I RECOMMEND]** one rule about reuse: **copy, never share.** Where a script or mechanism comes
from another project, it is copied into this one. A shared script means improving this book can
break something else, and it gives this project an external dependency it does not control.

---

## 12. What is not decided

**[OPEN]** Everything in this file, pending the owner's review.

**[OPEN]** Decisions held elsewhere. **This list is a pointer, not a second copy** — each item is
marked `[OPEN]` in the file that owns it, and that file is where its options live:

| Open decision | Owned by |
|---|---|
| The book's shape — breadth against depth | `GOAL.md` §10 |
| How deep the mathematics goes | `GOAL.md` §10, with the test in `GUIDE.md` §8 |
| Which area goes deep, if the shape is asymmetric | `GOAL.md` §10 |
| The structure — which of the candidates the book takes | `GOAL.md` §5.3. **Must wait for the subjects** |
| Reference by chapter, or by concept | `GUIDE.md` §7 |
| Whether the book is for the owner alone | `GOAL.md` §10 |

**None of these blocks the research.** Scope versus depth is **not** open: it is settled in
`GUIDE.md` §3.

**[OPEN]** The three problems in `GOAL.md` §8 that §4 attacks but does not finish: the revision
cost over many cycles, the acceptance rule for contested material, and ownership moving between
cycles. §4.1, §4.2 and §4.4 are proposed answers. None has been tested.
