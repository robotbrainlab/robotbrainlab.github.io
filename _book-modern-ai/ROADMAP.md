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

## ALL PRE-CONSENSUS RESEARCH IS DISCARDED

Owner's instruction, 2026-11-06: *"We are going to conduct fresh research from scratch, completely
disregarding the previous research, as it was conducted before we reached a consensus."*

No figure from the stopped round of 2026-11-05, and none from the pilot run, may be cited or used to
choose or rank an area. `discarded/README.md` records what was discarded and the three method-only
results that survived. `CLAIMS.tsv` and `research/` are empty.

## What step 3 established

The pilot ran one agent on one area with the brief at `discarded/pilot-01-systems-brief.md`.

**It passed all six tests.** It used 11 of 25 searches and 16 of 25 fetches, stopped because its
records were complete rather than because the budget ran out, and started **zero** sub-agents. It
refused three numbers it had seen in search results because it could not confirm them at source.

**Its content is discarded** and sits in `discarded/`. Only the verdict on the instrument survives:
the brief terminates, it keeps an agent honest about its sources, and it does not sprawl.

**Four fixes followed**, and are in `briefs/TEMPLATE-area-research.md` version 2: output goes to a
file rather than into the conversation; the live-research word limit is raised and enforced; the
buildable experiment must state its hardware; and the claims vocabulary gains `source-absence`.

**One finding is about the cap rather than the field.** The area the pilot was given held more
subjects than its cap of six allowed. **So the areas chosen at step 4 should be small.**

## What step 4 needs

A list of areas, and the reason for the list.

**Where the areas may NOT come from:**

- **The discarded research.** No figure from it may rank or choose an area.
- **My own judgement.** The nine areas of the stopped round were mine, the owner questioned that
  carving twice, and they missed several subjects entirely.
- **`_sources/ai-roadmap/research/2026-09-17-data-intelligence-landscape.md`.** I recommended its
  nineteen areas on 2026-11-06 and the recommendation is **withdrawn**. Two reasons. It predates
  Baseline 3, so it is superseded. And it is a baseline reconstruction of the *whole* Data &
  Intelligence curriculum — its C1 Mathematical Foundations and C4 Statistical and Classical ML are
  Fundamentals material — so importing it would break this book's own scope rule.

**Where the scope DOES come from: the current specification**, `_sources/ai-roadmap/ROADMAP.md`,
Baseline 3, accepted 2026-11-02. Read 2026-11-06. This is a reading of the owner's current
document, not a research finding.

| Section | What it is | In this book's scope? |
|---|---|---|
| §3 Fundamentals (E1–E10) | Depth Track | **No** — the scope rule excludes it |
| §4 Advanced (F1–F6) | Depth Track | **No** |
| §5 Mastery | Depth Track | **No** |
| **§6 Modern AI: Research, Science and Engineering** | The parallel track — three phases, plus the research dimension H1/H2 | **Yes.** This is the book's name |
| **§7 Important Extensions (EX1–EX9)** | Broadly valuable, not required before normal progression | **Yes** — not Fundamentals, Advanced or Mastery |
| **§8 Specializations (SP1–SP10)** | Selective depth | **Yes** — same reason |
| **§9 Research Frontiers (RF1–RF8)** | The open problems of §6 | **Yes** — §9 says explicitly that these are §6's open problems |

**[OPEN] This reading needs the owner's confirmation.** The scope rule as stated names only
Fundamentals, Advanced and Mastery. Extensions, Specializations and Research Frontiers are separate
sections of the specification, so on a literal reading they are in scope — and that is where
vision, embodied AI, time series, ranking and recommendation, symbolic methods, graph learning,
speech, AI for science, systems depth and human-AI oversight all live. If the intention was to
exclude them too, the book is an LLM-systems book and §6 alone is its scope.

**Everything after that is for the fresh research to establish**, not for me to assert: which of
those areas carry real current activity, how they divide, and how small each has to be.

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
