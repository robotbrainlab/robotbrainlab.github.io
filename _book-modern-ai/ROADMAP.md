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

**Step 10 can run at the same time as step 5.** It does not depend on the subjects.

## What step 3 established

The pilot ran one agent on one area with the brief at `briefs/pilot-01-systems.md`.

**It passed all six tests.** It used 11 of 25 searches and 16 of 25 fetches, stopped because its
records were complete rather than because the budget ran out, and started **zero** sub-agents. It
refused three numbers it had seen in search results because it could not confirm them at source.
Its output is in `research/2026-11-06-systems-hardware.md`: six subject records, every one with the
verdict `CHAPTER`.

**Four fixes followed**, and are in `briefs/TEMPLATE-area-research.md` version 2: output goes to a
file rather than into the conversation; the live-research word limit is raised and enforced; the
buildable experiment must state its hardware; and the claims vocabulary gains `source-absence`.

**One finding is not about the brief.** The area was too big. The cap of six worked and hid two
subjects — the economics of the engineering, and datacentre power — plus a probable seventh, memory
and storage below HBM. **So the areas chosen at step 4 should be smaller than the one the pilot
used.**

## What step 4 needs

A list of areas, and the reason for the list. Two things to know before deciding:

1. **A partition is an argument, not a finding** (`GOAL.md` §3.3). Research cannot supply it. It is
   a decision, and it should be made deliberately and written down with its reasons.
2. **The obvious candidate already exists.** The owner's own landscape document defines nineteen
   areas in six strata, and its section B — *"Why the Taxonomy Took This Form"* — records each
   decision with the alternative considered and the reason. The nine areas used in the stopped
   research round were my own seven-way compression of those nineteen plus one of my invention, and
   the owner questioned that carving twice. Nineteen smaller areas fits the pilot's finding better
   than nine large ones.

## The open decisions, and the step that closes each

| Open question | Closes at step |
|---|---|
| Is the method right? | 2 |
| Which areas do we research? | **4** |
| Breadth, or depth in one area? | 7 |
| How deep does the mathematics go? | 7 |
| What structure, and do four parts fit? | 7 |
| Which area goes deep, if any? | 7 |
| Reference by chapter, or by concept? | 7 |
| Is the book for the owner alone? | 8 |
| Is the scope-versus-depth reading right? | Any time — one line from the owner |

**Four of these cannot be answered now.** They need the subjects, and the subjects come from the
research. That is why they are marked open rather than asked.

## Nothing after step 3 may start until step 4 is decided
