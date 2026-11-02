<div align="justify">

# Baseline 3 — Three Depth Levels, and the Track Renamed

| | |
| --- | --- |
| **Type** | Design record for an owner-directed curriculum change |
| **Date** | 2026-11-02 |
| **Changes** | [ROADMAP.md](../ROADMAP.md) Baseline 2 → Baseline 3 |
| **Outgoing baseline** | Preserved verbatim at [history/roadmap-baseline-2.md](../history/roadmap-baseline-2.md) |
| **Status** | Implemented. Approved by the owner before any file was edited |

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [What Changed](#1-what-changed)
2. [Why](#2-why)
3. [Where the Research Content Went](#3-where-the-research-content-went)
4. [What Deliberately Did Not Change](#4-what-deliberately-did-not-change)
5. [Consequences for the Maintenance Machinery](#5-consequences-for-the-maintenance-machinery)
6. [Files Touched](#6-files-touched)

</details>

---

## 1. What Changed

Two changes, and nothing else.

1. **The Depth Track has three levels.** Fundamentals → Advanced → Mastery. Research is no longer a
   level of the depth path. The old `ROADMAP.md` §6 was removed and §7–§16 renumbered to §6–§15.
2. **The parallel track is renamed** from *Modern AI Engineering* to
   **Modern AI: Research, Science and Engineering**, and it now carries the research dimension as
   well as current practice.

[⬆ Back to Contents](#contents)

---

## 2. Why

The depth path teaches knowledge whose science is established. A settled subject has no open
questions of its own, so a research *level* at the end of that path had nothing of its own to
study. The evidence for this is in the roadmap's own content: all eight open problems in
[ROADMAP.md §9](../ROADMAP.md#9-research-frontiers) — interpretability as assurance, scalable
oversight, scaling theory, continual learning, world models, discrete diffusion, long-horizon agent
evaluation, theorem proving — belong to the modern layer. None of them is open in classical machine
learning, deep learning or language-model mechanics.

So Research sat at the top of the established path while studying the frontier of the other one.
Moving it into the parallel track puts the open questions where the open questions are, and the
rename says so on the page.

[⬆ Back to Contents](#contents)

---

## 3. Where the Research Content Went

| Content | Before | After |
| --- | --- | --- |
| H1 Research Literacy | §6, "taught at Advanced" | The track's research dimension, still taught at Advanced in guide step 13. Unchanged in substance |
| H2 Research Contribution | §6, and guide step 19 under "Part 4 — Research" | A topic of the track, *Contributing Research*, gated by the existing checkpoint |
| RF1–RF8 Research Frontiers | §10, under the depth path | §9, named as the open problems of the track, and recorded in the register with the new `Open problem` status |
| "Entering Research contribution" gate | A depth-path gate | The gate into the track's research topic. Same criteria |

The numbered path is now 18 steps. No step was renumbered: step 19 was the last one, and it became
a topic rather than a step.

[⬆ Back to Contents](#contents)

---

## 4. What Deliberately Did Not Change

| Kept | Why |
| --- | --- |
| The Knowledge Depth ladder ends at **Research** | That is a depth a block may require, not a stage of the path. Removing it would silently change required depths |
| Every block E1–E10 and F1–F6 | No capability, required depth, prerequisite, assigned resource or page range was altered |
| Mastery G1–G4, including G3 experimental capability | Experiment design stays a universal Mastery capability |
| The nine existing track topics and their opening points | After steps 7, 9, 11, 15 and 16, unchanged |
| The name of the **4-Week Modern AI Scan** | It still describes what it does, and renaming it would drag two state-file labels along for no gain |
| `research/` and `reviews/` report prose | Dated records. Retro-editing them to match a later rename would falsify the record. Only link targets were repaired |

[⬆ Back to Contents](#contents)

---

## 5. Consequences for the Maintenance Machinery

The research process had to be extended, not weakened, because the track is now named for research.

1. **A new status.** The register's lifecycle gains `Open problem`: a question the field has not
   settled, carried as a frontier and never as practice. It is teachable, so that the track can
   present an open question *as* open. `Watching` and `Discovered` remain untaught.
2. **A new scan direction.** [MAINTENANCE.md §4](../MAINTENANCE.md#search-directions) now asks the
   4-week scan to look for active research frontiers — what researchers are trying to solve, which
   directions have substantial evidence, which are contested. Before this change the eleven search
   directions were all engineering-facing, and the word "frontier" appeared nowhere in the
   maintenance procedure, although the landscape report has a Research Frontier Map. That was a gap.
3. **A new scan action.** `Open problem` joins Ignore, Watch, Current Practice, Investigate,
   Superseded and Evidence update.
4. **No check was removed.** The site build still enforces that a topic teaches only entries the
   register lists, with the status the register gives them, citing evidence that exists in the
   report it links to. The phrase check that kept the track from being called a fifth depth level
   now also catches "fourth".

[⬆ Back to Contents](#contents)

---

## 6. Files Touched

| File | Change |
| --- | --- |
| [ROADMAP.md](../ROADMAP.md) | Baseline 3; three levels; §6 removed and sections renumbered; track renamed and given its research dimension |
| [LEARNING-GUIDE.md](../LEARNING-GUIDE.md) | Part 4 removed; step 19 became the *Contributing Research* topic; three levels; track renamed |
| [AGENTS.md](../AGENTS.md) | Three depth levels; the Research level's capabilities moved into the track; track renamed |
| [README.md](../README.md) | Three levels; the Research subsection moved into the track; track renamed |
| [MAINTENANCE.md](../MAINTENANCE.md) | Frontier search direction; `Open problem` action; teachable statuses; track renamed |
| [PROJECT-STATE.md](../PROJECT-STATE.md) | Three levels; 18-step path; track renamed |
| [reviews/modern-practice-register.md](../reviews/modern-practice-register.md) | `Open problem` status; MP-50–MP-57 for RF1–RF8 |
| `scripts/site.toml`, `scripts/sitegen/*.py` | Track name, level list, checkpoint sequence, teachable statuses, baseline number, protected fingerprint |
| [history/roadmap-baseline-2.md](../history/roadmap-baseline-2.md) | New: the outgoing baseline, preserved verbatim |

[⬆ Back to Contents](#contents)

</div>
