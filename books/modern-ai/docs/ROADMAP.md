# Where we are, and what happens next

Eleven steps, from planning to a written book. **This file is the session's starting point:** read
it first, act on the current step, then update it.

**One structural action is pending, with a trigger.** `GUIDE.md`, `PROCESS.md` and `GATES.md` merge
into one specification **once step 7 closes** — those four decisions are what will move them next,
and a merge is a drafting event best done when the text has stopped changing (`PROCESS.md` §11).

**Five approval points per cycle** — areas, subjects, shape, plan, structural changes — and all five
stay for the first cycle. **[AGREED 2026-11-06]** They are reviewed after cycle 1 and not before,
because nobody has run one of these cycles yet and cutting a gate now would be guessing at which
approvals matter. **If a decision waits more than seven days I act on my recommendation and mark it
`[DEFAULTED]`** (`PROCESS.md` §2.1) — **five** things never default `[2026-11-12]`, and that
section lists them.

**`[STATED 2026-11-12]` An independent rules review runs before each of these five approvals**, not
on a calendar. The owner was offered a fixed schedule and chose this: the three reviews of
2026-11-11 found 36 problems **where rules had just changed**, and a calendar review of unchanged
text re-reads the same words at full cost. **This is in addition to `briefs/document-check.md`**,
which runs on a single document before it is called finished and after any rule change; the review
here reads the rules as a set, which is what found the contradictions between files.

## What is next — read this first

**`[2026-11-12]` Step 4, part 3 is done and ruled on. The next action is a short, targeted research
run**, and the owner chose it:

> *"Read them first."*

**What to fetch: a scope statement for each of the 62 categories the consolidation could not judge**
— 33 AI Engineer World's Fair programme tracks and 29 ACL Rolling Review tracks. They are listed by
name, by source, in `research/frames/CONSOLIDATED-2026-11-12.md` under *Unclear*, which also names
the pages that would settle them: ARR's separate area-guide page, and a per-track description for
the programme. **This is a fetch against a named list, not a new framing run.**

**Why it comes before any cut.** 99 of 223 categories are undecided, and **almost the whole
engineering vocabulary is among them** — *Evals*, *Inference*, *Context Engineering*, *Agent
Reliability*, *AI Infrastructure*, *SWE Agents* and the rest. Of the 47 that did pass, 34 are
academic-only and 12 of the remaining 13 are MLCommons benchmark suites. **Cutting now would cut
the half that publishes scope statements and keep nothing of the half that does not**, which cannot
serve `GOAL.md` §1.1's research-oriented engineer.

**Then, and only then:** re-run the `UNCLEAR` dispositions in `docs/PROPOSAL-areas-2026-11-12.md`,
and put the area list to the owner.

**What he already ruled, on 2026-11-12** — all four are recorded in that proposal's own
*THE OWNER'S RULING* section, and the rows below it are already updated:

| | Ruling |
|---|---|
| The 99 undecided | **Read them before choosing any areas** |
| The twelve MLCommons suites | **One area, all twelve named underneath** |
| Robotics / Intelligent Robots / Control methods | **Keep all three; decide after the research** |
| The five remaining same-ground pairs | **Keep apart for now** |

**The list stands at 33 proposed areas**, nothing cut.

## `[STATED 2026-11-12]` An expectation gap, recorded before anything else is planned

**The owner said this at the end of a long day, and it has never been written down:**

> *"I initially thought the entire process would be deployed on Hostinger, and I'd receive a new
> book every three weeks. But this is turning out to be much harder and more time-consuming than I
> expected."*

**That is not what this design does, and the difference is not a detail.** What is built here is a
supervised pipeline with **five approval points per cycle** and **one chapter in cycle 1**. It
cannot run unattended, and it does not produce a book on a schedule. **Nothing in these documents
promised otherwise — and nothing in them asked him what he expected either**, which is the actual
defect.

**He also said what he hopes pays for it, and he may well be right:**

> *"I do believe that the first run of the book will make future runs easier, since we'll likely
> encounter a lot of issues along the way, and resolving them now should help us clear up many
> things for the future."*

**There is evidence for that**: `books/future-books/README.md` records that the machinery in
`../interview-prep/tools/` *"is the part that took longest to get right"* and is reusable. **What
there is no evidence for is the three-week cadence**, and `PROCESS.md` §10 is explicit that cycle
1 exists to measure how long a cycle actually takes, because nobody knows.

**`[2026-11-12]` A measurement, because the cadence question has one and nobody had looked.**
*Modern AI Engineering from Zero* took about **twelve days**: its own commit history begins
2026-10-19 and `../README.md` records it finished 2026-10-31 — 57 chapters, 1,413 printed pages.
**So the owner's three-week expectation was evidence-based, and the evidence was his own.** What is
slow here is not the ambition and not the tooling: **that book's scope was given and this one is
deriving its scope from the field.** Six days have gone on deciding what the book is about.
**`GOAL.md` §3.3 predicted the cost** — *"a partition can only be worse or better for a purpose"*
— but nothing weighed that cost against a cadence the owner had in mind and had not been asked for.

**On deployment, since he named a web host.** Hostinger serves websites; it cannot run this, because
the work is done by Claude wherever it is invoked. The only artefact that would sit on a host is the
finished PDF, which GitHub Pages already serves from this repository. **The automatable parts are
already automated** — the runs, the merging, the gates, the typesetting. **The five approvals are
not, and that is the whole trade**: the robotics loss happened at the one stage that had no
supervision.

**`[OPEN]` This is the first thing to settle in the next session about this book**, ahead of the
area ruling, because the answer changes what is worth building:

- Does he want this pipeline, slower and supervised, for one book done properly?
- Or does he want something closer to what he pictured — and if so, what has to be given up to get
  it, since the five approvals exist to stop the failures `GOAL.md` §11 records?

**Do not answer this for him.**

**`[2026-11-12, later the same day]` It no longer blocks the work, and this paragraph used to say
it did.** After it was written the owner ruled four times on the area proposal and named the next
action himself. **So the question above is still open and still worth asking — but as a question
about the shape of the whole effort, not as a gate in front of step 4.** Carry on with *What is
next*, below.

## How step 4 got here

**Step 4 is next. Two or more independent framing runs record what the field files; a consolidation
run unions them into one candidate list; Claude proposes which of those areas the book covers, with
the reason for each; the owner approves, redraws or rejects that proposal.** `[2026-11-11]` The
third of those four was missing from every document until that day, and its absence put an
unproposed cut on the owner.

**`[STATED 2026-11-11]` The source register is revoked and every run is independent.** The owner
ruled that a fixed source list decides what can be found, which makes it scope rather than method.
**No run is given sources, routes, levels or any earlier run's output.** `GOAL.md` §3.3 carries the
decision, what it costs, and the two things restored to pay for it: the source and search floors,
and more than one run per cycle, unioned.

**[2026-11-07] The whole chain has now been run once as a validation, and its outputs are
disposable.** Framing twice, consolidation once, one scout, one claim verification — then every
output file read against its brief, with four source pages opened to check what the runs claimed.
**21 findings, in `VALIDATION-2026-11-07.md`**, and the brief that caused each is fixed.

**[2026-11-07, later the same day] Two of those findings were wrong, and the diagnosis that replaced
them is the most useful thing the validation produced.** It is in `DIAGNOSIS-2026-11-07.md`, which
supersedes V8 and V11 of the validation file. In short: **the six framing runs were never comparable,
because the brief told each run to choose its own sources.** Only two sources were common to all six.
A route around a blocked page found by one run was unavailable to the next. **The fix at the time
was the source register, now `research/frames/superseded/SOURCES.md`**, built from what the six
runs had already found.

**`[STATED 2026-11-11]` That register is revoked** — see the current position above and `GOAL.md`
§3.3. The diagnosis's measurements still hold and are worth keeping, because they are what the
restored floors exist to mitigate:

1. **A framing run's losses are the only unrecoverable ones** (V13). The consolidator may add no
   category, so what framing misses never reaches the owner. **This is the reason more than one run
   per cycle is now required, and why runs are unioned rather than intersected.**
2. **Coverage does not accumulate between independent runs.** Run `d` found a route round a standards
   body that run `e` then hit and gave up on, a day later, calling it the biggest hole in its list.
   **With the register gone this can happen again**, and the owner accepted that cost for
   independence. The search floor is what pays for it.
3. ~~**One framing run per cycle, not a pair**~~ **— reversed.** The pair existed to expose artefacts
   of a run's own source choice. The register removed the source choice and so removed the reason;
   revoking the register restores both.
4. **Nothing verifies a research run** (V15), and with the register's floor gone, **nothing does
   again.** The source and search floors bound a run's effort, not its correctness. This is the one
   genuinely open question in the research half.

| # | Step | Who decides | Deliverable | State |
|---|---|---|---|---|
| 1 | Agree the goal | Owner | `GOAL.md` | **Done** |
| 2 | Agree the method | Owner | `PROCESS.md`, `GUIDE.md`, `GATES.md` | **Partly approved.** Eight topics were settled on 2026-11-06 — grep `[AGREED 2026-11-06]` for them. The rest stay marked `[I RECOMMEND]` and are ruled on as they come up in practice |
| 3 | Write the research brief | Claude | A brief with a capped output, a counted budget and a stopping rule with a fixed point | **Written and exercised** — `briefs/TEMPLATE-area-research.md`. **It terminates**: the validation run of 2026-11-07 stopped on its fetch limit and wrote up without starting a further record. Three defects it exposed are fixed in the brief; see `VALIDATION-2026-11-07.md` V18–V20, of which **V19 matters most — six of six verdicts came out `CHAPTER`, so three of the four verdicts have still never been issued** |
| 4 | **Establish the research areas** | Claude proposes · **Owner rules** | **Two or more independent framing runs**, each finding its own sources, record what the field files; a consolidation run **unions** them into one candidate list; **Claude proposes the cut against §1.1's purpose, with the reason for each keep and each cut**; the owner approves, redraws or rejects that proposal, with the reasons recorded | **Parts 1–2 must be re-run** `[STATED 2026-11-11]`: the source register is revoked, so the existing 283 categories and 63 areas came from a method the owner has withdrawn. **Part 3 is WITHDRAWN too** — `docs/superseded/PROPOSAL-areas-2026-11-11.md` must not be ruled on; it cut the best-attested area and five further groups of subjects. See "What step 4 needs" below |
| 5 | Run the research | Claude | One file per area in `../research/` | Not started |
| 6 | Select the subjects | Claude sorts · **Owner rules** | What passed the three tests, and every rejection with the test it failed and why. He rules on both | Not started |
| 7 | Decide the book's shape | **Owner** | The four open questions that need the subjects: breadth against depth, the mathematics boundary, the structure, and which area goes deep | Not started |
| 8 | Write the table of contents | **Owner approves** | `PLAN.md` | Not started |
| 9 | Write the acceptance questions | Claude | `ACCEPTANCE.md`, filled | Not started |
| 10 | Build the machinery | Claude | `tools/`, each check proved before it is wired in. **`tools/sweep.py` and the driver come before the first fix round**, not at the end (`GATES.md`) | Not started |
| 11 | Write chapter one, then the rest | Claude | Chapters. **Cycle 1 is one chapter, and both durations are recorded before cycle 2 is sized** (`PROCESS.md` §10) | Not started |

**Most of step 10 can run alongside step 5.** Two checks cannot be finished there: the inputs gate's
vocabulary is seeded from the research (`GATES.md` gate 8), and the boundary gate only lists until
step 7's mathematics decision (gate 2). A third, the outline gate, is built alongside the build
itself because it reads the built document.

## What step 4 needs

**Four parts, in order.** `GOAL.md` §3.3 owns the argument for the split and this document does not
restate it.

1. **Two or more framing runs**, `briefs/TEMPLATE-area-frame.md`, each in a fresh session outside
   this repository so no project file is in the agent's context, **each launched separately and
   given nothing** — no sources, no routes, no levels, no earlier output. Each reports the
   categories the field currently files its own work under, with a fetched source, **the level of
   that source's own hierarchy it was taken from**, what it excludes, and what the run could not
   reach. **They propose a list; they decide nothing.**

   **Check each run against its own coverage section before the consolidator runs**, and check the
   runs against each other. `[STATED 2026-11-11]` There is no register to check against any more,
   so what is checkable is: did each meet the source floor of eight sources across four kinds, did
   each account for every source it opened, and **what did one run find that the other did not?**
   That last question is the whole reason there is more than one run. That check is reading, and it
   takes about an hour per run.

   **`[STATED 2026-11-11]` Run `g` is superseded and parts 1 and 2 must be re-run.** Run `g` was
   handed the nineteen registered sources and told to open exactly those. **Its 283 categories are
   therefore what that source list contains, and the source list is the thing the owner revoked.**
   The run was not careless — it read every source it was given — but its scope came from a previous
   decision, which is precisely what is no longer allowed. **The same follows for the 63 areas
   consolidated from it.**

   Run `g` and its consolidation are kept as records, in
   `research/frames/superseded/`. They are not input to anything, and the next consolidation unions
   this cycle's runs only.

   **`[2026-11-12]` Parts 1 and 2 are done.** Runs `h` and `i` were checked against their own
   coverage sections and against each other (`CHECK-runs-h-i-2026-11-12.md`), then consolidated to
   `research/frames/CONSOLIDATED-2026-11-12.md` — **223 distinct categories from a 307-record
   union, of which 99 are `UNCLEAR`.** The consolidation was then checked against its brief
   (`CHECK-consolidation-2026-11-12.md`): **its arithmetic closes**, and three count errors in its
   own summary are marked in the file. **Part 3, the proposal, is next**, and the 99 undecided
   categories are its largest piece — most of the field's engineering vocabulary is in them.

   **`[STATED 2026-11-12]` The owner confirmed that the 283 categories and the 63 areas are
   history, and the first document sweep ran.** Fifteen files moved: eleven to
   `research/frames/superseded/` and four to `docs/superseded/`, each with a dated line saying what
   superseded it, and each directory with a `README.md` listing them. **Nothing was deleted**
   (`PROCESS.md` §11.1).

   **What is worth carrying as method rather than content** — none of it names a category, so none
   of it offends the independence rule: run `g` wrote its own scope instead of the source's on
   sources that file by a bare label, affecting about 64 of its 283 records
   (`DIAGNOSIS-2026-11-07.md` §8); it put 32 labels into appendices instead of the main list; and
   the consolidation judged the main list only, so those 32 got no verdict. **All three are fixed in
   the briefs**, and the fixes stand whatever the next runs find.

   **[2026-11-11, evening] Part 3 was done and is withdrawn.** `superseded/PROPOSAL-areas-2026-11-11.md` cut
   `Intelligent Robotics` — the best-attested area in the register, 10 of 19 sources — and took
   world models, Control methods, six AAMAS areas, expert systems and theorem proving with it
   without naming any of them. It also ignored a requirement in the consolidation brief to dispose
   of the five `UNCLEAR`. **An independent review found this; the stage had no brief at all.**
   `briefs/area-proposal.md` now binds it. **Part 3 must be run again to that brief**, and the
   withdrawn document carries the full account at its head.

   | | |
   |---|---|
   | Stage 1, framing | reported robotics seven times over. No loss |
   | Stage 2, consolidation | kept it, merged nine names into it, flagged world models as unique. **No loss** |
   | Stage 3, proposal | **cut it.** The only stage with no brief |
2. **A consolidation run**, `briefs/TEMPLATE-area-consolidate.md`, once. The framing runs report
   faithfully, which means they report application domains, session formats, audience labels and
   vendors' product names too — because those are what venues route submissions by. This run gives
   every reported category one verdict, merges the same area reported under different names, and
   picks one level of resolution. **It may reject a category for not being an area. It may never
   reject one for being unimportant** — **that judgement belongs to part 3, where it is proposed with
   its reason and then ruled on**, not to a run that cannot be checked against what it filtered. Every
   rejection and merge is listed with its reason so either can be reversed.

   **It needs the owner's definition of an area before it can run**, because every rejection it
   makes is an application of that rule. The draft is in the brief and is marked as mine.
3. **Claude proposes the cut, then the owner rules on the proposal** — approves it, redraws the
   boundaries, or rejects it — with the evidence for each boundary in front of him.

   **`[2026-11-11]` This step had a hole and the owner fell through it four times.** His row says he
   rules on *the proposed list*; nothing in the table made one. The framing run reports and does not
   decide; the consolidation run may not reject anything for being unimportant. So both runs finish
   and what exists is an inventory of 63 with no recommendation — and asking him to cut an inventory
   is asking him to originate the argument from nothing, which `GOAL.md` §3.3 retracts in his own
   words. **The proposal was `superseded/PROPOSAL-areas-2026-11-11.md`: 12 areas, 27 folded, 24 cut, each with
   its reason, judged against §1.1's career goal and §3.1's five questions, which is what §3.3 says
   the argument is made from.** `GOAL.md` §3.3 now carries the missing row, so the step cannot go
   missing again. **The reasons are recorded with the list**, because a later cycle has to be able to
   ask whether a boundary still makes sense.

   **`[2026-11-11]` This used to say "and the two runs' disagreements beside it".** With one framing
   run per cycle there is no second run to disagree with it, and **what replaces that evidence is the
   register's recorded floor plus the consolidation run's own account of what it could not settle** —
   its `UNCLEAR` list, its close rejections, its thin merges and the areas it kept on thin scope. A
   grep for the phrasings I had in mind did not find this clause on 2026-11-07; opening the file did
   (`POSTMORTEM-2026-11-11.md` §2.3).
4. **`[STATED 2026-11-12]` The approved areas are numbered, in the same sitting as the approval.**
   `A01`, `A02`, `A03` … in the order of the approved list, written into the file that records the
   ruling. **Every claim id is the area's number, a hyphen and a counter** (`PROCESS.md` §5.1), so
   until this happens no claim can get an id — **and until 2026-11-12 no stage assigned one at all.**

   **Why at approval and not in the proposal.** A number is never reused and never renumbered
   (§5.1). The owner cuts areas and redraws boundaries when he rules, so numbering before the
   ruling would mean renumbering after it. The owner was given both options and chose this one.
   **`confirm-claims.md` stops rather than coining a number** for an area that has none.

5. **Somebody turns the approved categories into each scout's `<SCOPE>` and `<EXCLUDED>`**, in the
   same sitting as the approval. `[STATED 2026-11-12]` **The proposal now carries `COVERS` and
   `EXCLUDES` forward from the consolidation** (`briefs/area-proposal.md`), which is what makes
   this step possible: it used to say "from the approved list", and the approved list carried
   neither. A framing run reports what work is *filed* in a category; a scout
   needs the *subjects* it is responsible for. Whoever converts one into the other is choosing what
   the scouts look for, so it is not a clerical step. Every area's exclusions are written at the
   same time as every other's, from the one approved list.

   **`[RESOLVED 2026-11-11]` Claude does it**, in the same sitting as the approval, by the same
   argument that assigns the proposal to Claude — writing a scope from an approved list is applying
   the owner's stated purpose, not originating content from nothing. He corrects any scope he
   disagrees with, as he corrects the proposal. The reasoning that was marked open is kept below
   because it is what the resolution answers.

   **`[history]` How it got here.** This clause used to say "that somebody is the owner … and it is
   not Claude's", undated and unmarked. **`GOAL.md` §3.3, marked `[AGREED 2026-11-06]`, retracts the
   same reasoning one step earlier**: asking the owner to partition the current field is circular,
   because that knowledge is what the book exists to give him, and the argument comes from the
   purpose instead — §1.1's career goal and §3.1's five questions. That reasoning applies to writing
   the scopes exactly as it applied to authoring the list. **It was then marked open rather than
   resolved, which left the work on him a second time; the resolution above closes it.**

**Two things to expect, so neither is read as a defect in the runs.** Filing categories do not
record whether a subject is still moving, so a settled area can arrive looking like a live one —
`GUIDE.md` §3's test is per claim and only applies later, which means a scout budget can be spent on
an area that turns out to be foundations. And the runs are forbidden from aiming at areas that are
agent-sized and non-overlapping, because they must report what the sources carry; **closing that gap
is what part 3's proposal is for**, and the owner's redraw after it. A boundary he draws is his
rather than a source's.

**Step 4 is not finished until the list is approved.** Everything downstream reads "the approved
list at step 4": the scouts' scope and exclusions (`briefs/TEMPLATE-area-research.md`) and the area
numbers in claim ids (`PROCESS.md` §5.1).

### Where the areas may not come from

| Not from | Why |
|---|---|
| **A curriculum, roadmap, course or syllabus** | Built for somebody else's purpose, so it carries authority it did not earn here and reasons that were not about this book (`GOAL.md` §3.3) |
| **My judgement of how the field divides** | I would be choosing the answer the research is meant to reach. **`[2026-11-11]` This bars me from inventing the categories; it does not bar me from proposing which of the field's own categories this book covers.** The first would be deciding how AI is shaped — the thing the research exists to find. The second is applying §1.1's stated purpose to a list somebody else drew, which is what part 3 is and what `GOAL.md` §3.3 assigns to me |
| **A category the framing run cannot source** | A boundary with no named source behind it is the agent's invention, which is the same defect as my judgement with less visibility |

**Note what is *not* on that list.** The categories a field currently files its work under are
evidence, not a prior taxonomy: nobody here chose them, they describe the present rather than a
teaching order, and each one is checkable at its source. That is the whole basis of part 1.

### What a good area is

**[I RECOMMEND]**, and these are properties of a *list*, not a claim about what is on it:

- **Each area is small enough that one agent can cover it inside one budget.** The brief caps
  subjects per area and requires the agent to report what it skipped — so a run itself reports
  whether an area was too large, and the list is revised from that.
- **The areas do not overlap.** Every area's exclusions are written at the same time as every
  other's, from the one list, so no subject is claimed twice or by nobody.
- **The list is written with its reasons.** A later cycle has to be able to ask whether a boundary
  still makes sense, which needs the argument and not just the names.

### Where the scope comes from

**`GUIDE.md` §3, and nowhere else.** This document does not restate it, not even in short form
(`../CLAUDE.md` owns the rule about that).

## The open decisions, and the step that closes each

| Open question | Closes at step | Needs the subjects first? |
|---|---|---|
| Is the method right? | 2 | No |
| Which areas do we research? | **4** | No |
| Breadth, or depth in one area? | 7 | **Yes** |
| How deep does the mathematics go? | 7 | **Yes** |
| What structure, and whether the book has parts at all | 7 | **Yes** |
| Which area goes deep, if any? | 7 | **Yes** |
| ~~Reference by chapter, or by concept?~~ | — | **Closed 2026-11-06**: by concept (`GUIDE.md` §7) |
| ~~Is the book for the owner alone?~~ | — | **Closed 2026-11-06**: the owner alone, for now (`GUIDE.md` §2) |
| ~~The build toolchain~~ | — | **Closed 2026-11-06**: pandoc → XeLaTeX (`GUIDE.md` §10) |

**Four need the subjects**, and the subjects come from the research — which is why they are marked
open rather than put to the owner now. **Of the five that did not, three are closed** and the
closures stay on the table so a later cycle can see what was decided and when. The two left are the
method's contents (step 2) and the area list (step 4).

## Nothing after step 4 may start until the area list is approved
