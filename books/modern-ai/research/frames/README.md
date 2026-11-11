# Framing runs

One file per framing run, named `YYYY-MM-DD-<run-id>.md`. **Superseded runs and lists are in
`superseded/`**, which has its own `README.md`; nothing there is input to anything.

**`[STATED 2026-11-11]` Every run is independent and is given nothing.** No source list, no routes,
no levels, no earlier output. Each run finds its own sources under a source floor — eight sources
across four kinds — and a search floor of ten searches. **`superseded/SOURCES.md` is a record, not an
input**: the owner revoked it as a register because a fixed source list decides what can be found,
which makes it scope rather than method (`../../docs/GOAL.md` §3.3). **It may not be pasted into
any brief**, including its routes, because a route is still a previous run's finding.

**Runs come in pairs again — two or more per cycle, launched separately and unaware of each other,
and UNIONED.** The pair exists so that "a division that is an artefact of whichever sources one run
opened shows up as a disagreement before the owner rules". It was dropped on 2026-11-07 when the
register removed the source choice, and **restored when the register was revoked.** A category one
run found and another missed is still a category the field files, so the consolidator takes the
union and never the intersection. `../../docs/DIAGNOSIS-2026-11-07.md` has the measurements that
say what independence costs.

**Run ids run `a`, `b`, `c`, `d` …** — the next unused letter. A superseded run is still evidence of
what a source carried on a date, so it is kept — **and moved to `superseded/` in the commit that
supersedes it**, which is `../../docs/PROCESS.md` §11.1's rule and not restated here.

**Framing happens at step 4, not every cycle.** The areas persist across cycles; they are re-framed
only when a `RECARVE` is approved (`../../docs/PROCESS.md` §5).

They live in their own directory because the scouts' files in `../` are named
`YYYY-MM-DD-<area-slug>.md`, and a framing run's name would be read as an area.

## What is here

| File | What it is |
|---|---|
| `2026-11-11-h.md` | **A current framing run.** 172 areas from 9 sources, 2,357 lines. Launched under the independence rule: no register, no routes, nothing from an earlier run |
| `2026-11-11-i.md` | **A current framing run.** 135 areas from 10 sources, 2,034 lines. Launched separately from `h` and unaware of it |
| `CONSOLIDATED-2026-11-12.md` | **The current candidate list** `[2026-11-12]`. The union of `h` and `i`: 307 records, 84 merges, **223 distinct categories** — 47 `AREA`, 51 `DOMAIN`, 9 `RECORD`, 17 `FORMAT`, 0 `PRODUCT`, **99 `UNCLEAR`**. **An inventory, not a recommendation.** Checked against its brief in `../../docs/CHECK-consolidation-2026-11-12.md`: arithmetic closes, three count errors in its own summary are marked in the file |
| `superseded/` | Eleven superseded runs and lists, each with a dated line saying what superseded it. **Input to nothing**, including this consolidation |

**Both current runs independently reported the same gap**: no source they could reach files AI work
by job or role. That is why the source floor gained a practitioner requirement, and the owner asked
for a route to be found. **It is still open.**

**`[2026-11-12]` The consolidation is done. Next is the area proposal**, to
`../../docs/briefs/area-proposal.md`, and `../../docs/ROADMAP.md` step 4 is the authority on what
it needs. **The largest piece of it is the 99 `UNCLEAR` categories**: the brief requires a
disposition line for each one before the owner sees anything, and forbids a reason shared between
areas. **Most of the engineering vocabulary is in that pile** — the consolidation's own finding:
*"A book on the engineering of AI that took only this run's `AREA` list would have almost no
engineering in it."*
