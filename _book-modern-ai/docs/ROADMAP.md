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
`[DEFAULTED]`** (`PROCESS.md` §2.1) — four things never default, and that section lists them.

## Current position

**Step 4 is next. Two framing runs record what the field files, a consolidation run turns that into
one candidate list, and the owner rules on it.**

| # | Step | Who decides | Deliverable | State |
|---|---|---|---|---|
| 1 | Agree the goal | Owner | `GOAL.md` | **Done** |
| 2 | Agree the method | Owner | `PROCESS.md`, `GUIDE.md`, `GATES.md` | **Partly approved.** Eight topics were settled on 2026-11-06 — grep `[AGREED 2026-11-06]` for them. The rest stay marked `[I RECOMMEND]` and are ruled on as they come up in practice |
| 3 | Write the research brief | Claude | A brief with a capped output, a counted budget and a stopping rule with a fixed point | **Written** — `briefs/TEMPLATE-area-research.md`. **That it terminates is designed, not demonstrated**: no run has exercised it, so step 5's first area is also the test of the brief |
| 4 | **Establish the research areas** | Claude proposes · **Owner rules** | Two framing runs record what the field files; a consolidation run turns that into one candidate list; the owner approves, redraws or rejects, with the reasons recorded | **Next** |
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

1. **Two framing runs**, `briefs/TEMPLATE-area-frame.md`, in a fresh session outside this
   repository so no project file is in the agent's context. Each reports the categories the field
   currently files its own work under — each with a fetched source, **the level of that source's own
   hierarchy it was taken from**, what it excludes, and what the run could not reach. **They propose
   a list; they decide nothing.**
2. **A consolidation run**, `briefs/TEMPLATE-area-consolidate.md`, once. The framing runs report
   faithfully, which means they report application domains, session formats, audience labels and
   vendors' product names too — because those are what venues route submissions by. This run gives
   every reported category one verdict, merges the same area reported under different names, and
   picks one level of resolution. **It may reject a category for not being an area. It may never
   reject one for being unimportant** — that is the owner's, and every rejection and merge is listed
   with its reason so he can reverse either.

   **It needs the owner's definition of an area before it can run**, because every rejection it
   makes is an application of that rule. The draft is in the brief and is marked as mine.
3. **The owner rules on that list** — approves it, redraws the boundaries, or rejects it — with the
   evidence for each boundary in front of him, and the two runs' disagreements beside it. **The
   reasons are recorded with the list**, because a later cycle has to be able to ask whether a
   boundary still makes sense.
4. **Somebody turns the approved categories into each scout's `<SCOPE>` and `<EXCLUDED>`**, and
   **that somebody is the owner**, in the same sitting as the approval. A framing run reports what
   work is *filed* in a category; a scout needs the *subjects* it is responsible for. Whoever
   converts one into the other is choosing what the scouts look for, so it is not a clerical step
   and it is not Claude's. Every area's exclusions are written at the same time as every other's,
   from the one approved list.

**Two things to expect, so neither is read as a defect in the runs.** Filing categories do not
record whether a subject is still moving, so a settled area can arrive looking like a live one —
`GUIDE.md` §3's test is per claim and only applies later, which means a scout budget can be spent on
an area that turns out to be foundations. And the runs are forbidden from aiming at areas that are
agent-sized and non-overlapping, because they must report what the sources carry; **closing that gap
is what the owner's redraw is for**, and a boundary he draws is his rather than a source's.

**Step 4 is not finished until the list is approved.** Everything downstream reads "the approved
list at step 4": the scouts' scope and exclusions (`briefs/TEMPLATE-area-research.md`) and the area
numbers in claim ids (`PROCESS.md` §5.1).

### Where the areas may not come from

| Not from | Why |
|---|---|
| **A curriculum, roadmap, course or syllabus** | Built for somebody else's purpose, so it carries authority it did not earn here and reasons that were not about this book (`GOAL.md` §3.3) |
| **My judgement of how the field divides** | I would be choosing the answer the research is meant to reach |
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
