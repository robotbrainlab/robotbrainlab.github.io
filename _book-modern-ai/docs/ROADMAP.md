# Where we are, and what happens next

**Updated 2026-11-06.** Eleven steps from planning to a written book. This file is the session's
starting point: read it first, act on the current step, then update it.

## Current position

**Step 3 is complete. Step 4 is next, and it is the owner's decision.**

| # | Step | Who decides | Deliverable | State |
|---|---|---|---|---|
| 1 | Agree the goal | Owner | `GOAL.md` | **Done** — verified by the owner 2026-11-06 |
| 2 | Agree the method | Owner | `PROCESS.md` | Written. **Contents not yet approved** |
| 3 | Test the research brief | Claude | A verdict on the brief | **Done** — passed all six tests |
| 4 | **Choose the areas to research** | **Owner** | A list of areas, with the reason for the list | **Next** |
| 5 | Run the full research | Claude | A record file per area | Not started |
| 6 | Select the subjects | **Owner** | Subjects that get chapters, and the rejections | Not started |
| 7 | Decide the book's shape | **Owner** | Three open questions closed | Not started |
| 8 | Write the table of contents | **Owner approves** | `PLAN.md` | Not started |
| 9 | Write the acceptance questions | Claude | The question bank | Not started |
| 10 | Build the machinery | Claude | Scripts and gates, each proved by breaking something | Not started |
| 11 | Write chapter one, then the rest | Claude | Chapters | Not started |

**Most of step 10 can run at the same time as step 5**, because most gates do not depend on the
subjects. **Two do** and must wait: the inputs gate's vocabulary list is seeded from the research
(`GATES.md` gate 8), and the boundary gate needs the mathematics decision from step 7
(`GATES.md` gate 2).

## ALL PRE-CONSENSUS RESEARCH IS DISCARDED

Owner's instruction, 2026-11-06: *"We are going to conduct fresh research from scratch, completely
disregarding the previous research, as it was conducted before we reached a consensus."*

No figure from the stopped round of 2026-11-05, and none from the pilot run, may be cited or used to
choose or rank an area. `../discarded/README.md` records what was discarded and the two method-only
results that survived. `CLAIMS.tsv` and `../research/` are empty.

## What step 3 established

The pilot ran one agent on one area with the brief at `../discarded/pilot-01-systems-brief.md`.

**The six tests it was judged against**, listed because a verdict whose criteria are unstated cannot
be re-derived:

| # | Test | Result |
|---|---|---|
| 1 | Did it stop on its own, or have to be stopped? | Stopped on its own, with budget to spare |
| 2 | Every required field present, inside the word limits? | Fields yes; two limits overrun |
| 3 | Any incident or commentary content? | None |
| 4 | Does every number say what it is a share of? | Yes, and it flagged where sources withheld one |
| 5 | Can the claims rows go into `CLAIMS.tsv` unedited? | Nearly — one vocabulary value was missing |
| 6 | Is at least one experiment doable without a large lab? | Yes |

It started **zero** sub-agents, and it refused several numbers it had seen in search results
because it could not confirm them at source.

**Its content is discarded** and sits in `../discarded/`. Only the verdict on the instrument survives:
the brief terminates, it keeps an agent honest about its sources, and it does not sprawl.

**Ten fixes have followed**, and are listed in `briefs/TEMPLATE-area-research.md`, now at **version
3**. Four came from the pilot run — output goes to a file rather than into the conversation, word
limits are enforced, the buildable experiment states its hardware, and the claims vocabulary gained
`source-absence`. Six came from an independent audit of the documentation: the brief now collects
skills and careers and the research-to-engineering transition, produces an area overview, no longer
lets a hardware rule or a recency rule reject a subject before the owner sees it, and no longer
assumes every subject has one canonical reference.

**One thing I previously recorded here is withdrawn.** I wrote that the pilot proved areas should be
small, because the area it was given held more subjects than its cap allowed. **That is a claim
about how big an area of AI is, drawn from a discarded run**, and it would have pre-loaded step 4
with a conclusion the fresh research is supposed to reach.

What survives is a property of the instrument: **a cap forces a choice, and the brief requires the
agent to report what it skipped and why.** So the research itself will say whether an area was too
big for its cap, and the cap is calibrated from that rather than asserted now.

## What step 4 needs

A list of areas, and the reason for the list. **It is the owner's decision, and this document does
not pre-empt it.**

### Where the areas may not come from

| Not from | Why |
|---|---|
| **The discarded research** | No figure from it may rank or choose an area |
| **My own judgement** | I carved the stopped round's areas myself, the owner questioned that carving twice, and it missed several subjects entirely |
| **Any prior taxonomy of the field, however good** | A partition is an argument, not a finding (`GOAL.md` §3.3). One written for a different purpose, or before the current baseline, is worse than none, because its authority is borrowed |

**[WITHDRAWN 2026-11-06]** This section previously listed a set of named areas, taken from a reading
of the owner's curriculum specification, with its internal section and block codes. **That was the
error the whole document warns against**: it handed over a carving of the field one step before the
owner was asked to choose one, and it used internal codes that `../CLAUDE.md` forbids in anything
the owner reads. An independent audit found it, and it is removed rather than reworded.

### Where the scope comes from

**Settled, and stated in exactly one place: `GUIDE.md` §3.** This document does not restate it, not
even in short form — a summary of a rule is a second statement of it, and two statements drift.

What applies it: `CLAIMS.tsv`'s `maturity` column, and `briefs/claim-verifier.md`, which establishes
that column's value.

**[RESOLVED 2026-11-06]** This section previously said the scope rule *"cannot be applied from
these documents"*, named an external curriculum as the largest dependency in the set, and offered
three ways out. **All of that is withdrawn.** The owner settled the boundary as a property of a
subject's state rather than as a position in a curriculum, which removed the dependency entirely —
and leaving the old wording here would have sent the next session to read an external document that
`GUIDE.md` §3 says is not needed. This file is read first, so a stale blocker here is expensive.

**Nothing else about the areas is settled here.** Which areas carry real current activity, how they
divide, and how large each is are for the research to establish.

## The open decisions, and the step that closes each

| Open question | Closes at step | Needs the subjects first? |
|---|---|---|
| Is the method right? | 2 | No |
| Which areas do we research? | **4** | No |
| Breadth, or depth in one area? | 7 | **Yes** |
| How deep does the mathematics go? | 7 | **Yes** |
| What structure, and do four parts fit? | 7 | **Yes** |
| Which area goes deep, if any? | 7 | **Yes** |
| Reference by chapter, or by concept? | 7 | No — decidable now, and cheap to decide early |
| Is the book for the owner alone? | 8 | No |

**Four need the subjects**, and the subjects come from the research — which is why they are marked
open rather than put to the owner. **Three do not**, and could be settled at any time.

**Scope versus depth is no longer on this list.** It is settled in `GUIDE.md` §3, dated and marked
agreed. An earlier version of this table listed it as open.

## Nothing after step 3 may start until step 4 is decided
