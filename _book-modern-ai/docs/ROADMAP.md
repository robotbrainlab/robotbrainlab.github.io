# Where we are, and what happens next

Eleven steps, from planning to a written book. **This file is the session's starting point:** read
it first, act on the current step, then update it.

## Current position

**Step 4 is next, and it is the owner's decision.**

| # | Step | Who decides | Deliverable | State |
|---|---|---|---|---|
| 1 | Agree the goal | Owner | `GOAL.md` | **Done** |
| 2 | Agree the method | Owner | `PROCESS.md`, `GUIDE.md`, `GATES.md` | Written. **Contents not yet approved** |
| 3 | Write the research brief | Claude | A brief with a capped output, a counted budget and a stopping rule with a fixed point | **Written** — `briefs/TEMPLATE-area-research.md`. **That it terminates is designed, not demonstrated**: no run has exercised it, so step 5's first area is also the test of the brief |
| 4 | **Choose the areas to research** | **Owner** | A list of areas, with the reason for the list | **Next** |
| 5 | Run the research | Claude | One file per area in `../research/` | Not started |
| 6 | Select the subjects | **Owner** | The subjects that get chapters, and the rejections with reasons | Not started |
| 7 | Decide the book's shape | **Owner** | The open questions that need the subjects, and the two that do not have to wait | Not started |
| 8 | Write the table of contents | **Owner approves** | `PLAN.md` | Not started |
| 9 | Write the acceptance questions | Claude | `ACCEPTANCE.md`, filled | Not started |
| 10 | Build the machinery | Claude | `tools/`, each check proved before it is wired in | Not started |
| 11 | Write chapter one, then the rest | Claude | Chapters | Not started |

**Most of step 10 can run alongside step 5.** Three checks cannot be finished there: the inputs
gate's vocabulary is seeded from the research (`GATES.md` gate 8), the boundary gate only lists
until step 7's mathematics decision (gate 2), and the outline gate cannot run at all until the
build toolchain is decided (gate 9).

## What step 4 needs

A list of areas, and **the reason for the list**. It is the owner's decision, and this document does
not pre-empt it.

### Where the areas may not come from

| Not from | Why |
|---|---|
| **A prior taxonomy of the field, however good** | A partition is an argument, not a finding (`GOAL.md` §3.3). One written for another purpose carries authority it did not earn here, and reasons that were somebody else's |
| **My judgement of how the field divides** | Same reason, with less authority. I would be choosing the answer the research is meant to reach |

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

**`GUIDE.md` §3, and nowhere else.** This document does not restate it, not even in short form — a
summary of a rule is a second statement of it, and two statements drift.

## The open decisions, and the step that closes each

| Open question | Closes at step | Needs the subjects first? |
|---|---|---|
| Is the method right? | 2 | No |
| Which areas do we research? | **4** | No |
| Breadth, or depth in one area? | 7 | **Yes** |
| How deep does the mathematics go? | 7 | **Yes** |
| What structure, and whether the book has parts at all | 7 | **Yes** |
| Which area goes deep, if any? | 7 | **Yes** |
| Reference by chapter, or by concept? | 7 | No — decidable now, and cheap to decide early |
| Is the book for the owner alone? | 8 | No |
| **The build toolchain** (`GUIDE.md` §10) | **10** | No — but **step 10 cannot finish without it**, because gate 9 reads the built document |

**Four need the subjects**, and the subjects come from the research — which is why they are marked
open rather than put to the owner now. **The other five do not** and could be settled at any time;
the build toolchain is the one of those with a step waiting on it.

## Nothing after step 3 may start until step 4 is decided
