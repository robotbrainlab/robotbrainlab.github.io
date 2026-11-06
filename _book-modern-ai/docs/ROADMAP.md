# Where we are, and what happens next

Eleven steps, from planning to a written book. **This file is the session's starting point:** read
it first, act on the current step, then update it.

## Current position

**Step 4 is next. A framing run proposes the areas; the owner rules on them.**

| # | Step | Who decides | Deliverable | State |
|---|---|---|---|---|
| 1 | Agree the goal | Owner | `GOAL.md` | **Done** |
| 2 | Agree the method | Owner | `PROCESS.md`, `GUIDE.md`, `GATES.md` | Written. **Contents not yet approved** |
| 3 | Write the research brief | Claude | A brief with a capped output, a counted budget and a stopping rule with a fixed point | **Written** — `briefs/TEMPLATE-area-research.md`. **That it terminates is designed, not demonstrated**: no run has exercised it, so step 5's first area is also the test of the brief |
| 4 | **Establish the research areas** | Claude proposes · **Owner rules** | A candidate list from a framing run, each boundary with its source — then approved, redrawn or rejected, with the reasons recorded | **Next** |
| 5 | Run the research | Claude | One file per area in `../research/` | Not started |
| 6 | Select the subjects | **Owner** | The subjects that get chapters, and the rejections with reasons | Not started |
| 7 | Decide the book's shape | **Owner** | The four open questions that need the subjects, plus the one that does not have to wait but closes here | Not started |
| 8 | Write the table of contents | **Owner approves** | `PLAN.md` | Not started |
| 9 | Write the acceptance questions | Claude | `ACCEPTANCE.md`, filled | Not started |
| 10 | Build the machinery | Claude | `tools/`, each check proved before it is wired in. **`tools/sweep.py` and the driver come before the first fix round**, not at the end (`GATES.md`) | Not started |
| 11 | Write chapter one, then the rest | Claude | Chapters. **Cycle 1 is one chapter, and both durations are recorded before cycle 2 is sized** (`PROCESS.md` §10) | Not started |

**Most of step 10 can run alongside step 5.** Two checks cannot be finished there: the inputs gate's
vocabulary is seeded from the research (`GATES.md` gate 8), and the boundary gate only lists until
step 7's mathematics decision (gate 2). A third, the outline gate, is built alongside the build
itself because it reads the built document.

## What step 4 needs

**Two parts, in order.** `GOAL.md` §3.3 owns the argument for the split and this document does not
restate it.

1. **Two framing runs**, `briefs/TEMPLATE-area-frame.md`, in a fresh session outside this
   repository so no project file is in the agent's context. Each reports the categories the field
   currently files its own work under — each with a fetched source, **the level of that source's own
   hierarchy it was taken from**, what it excludes, and what the run could not reach. **They propose
   a list; they decide nothing.**
2. **The owner rules on that list** — approves it, redraws the boundaries, or rejects it — with the
   evidence for each boundary in front of him, and the two runs' disagreements beside it. **The
   reasons are recorded with the list**, because a later cycle has to be able to ask whether a
   boundary still makes sense.
3. **Somebody turns the approved categories into each scout's `<SCOPE>` and `<EXCLUDED>`**, and
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
