# Framing runs

One file per framing run, named `YYYY-MM-DD-<run-id>.md`. **Runs come in pairs** — two independent
runs of the same brief with the same field wording, so a division that is an artefact of whichever
sources one run opened shows up as a disagreement before the owner rules
(`../../docs/briefs/TEMPLATE-area-frame.md`).

**Run ids run `a`, `b`, `c`, `d` …** — a new pair gets the next two letters rather than reusing the
first. **A pair is superseded when the brief is changed between pairs**, and the later pair is the
current one; nothing is deleted, because a superseded run is still evidence of what the sources
carried.

**Framing happens at step 4, not every cycle.** The areas persist across cycles; they are re-framed
only when a `RECARVE` is approved (`../../docs/PROCESS.md` §5).

They live in their own directory because the scouts' files in `../` are named
`YYYY-MM-DD-<area-slug>.md`, and a framing run's name would be read as an area.

## What is here

- `2026-11-06-a.md`, `2026-11-06-b.md` — **the first pair, superseded.** Each hit a cap and invented
  its own rule for cutting the list, which is why the brief was changed.
- `2026-11-06-c.md`, `2026-11-06-d.md` — **the current pair**, run under the fixed brief. 86 and 209
  categories, nothing filtered.
- `MERGED-CANDIDATES.md` — all four runs merged: 250 distinct categories with their source counts.
  **Not a proposal.** The consolidation run turns this into a candidate list; the owner cuts it.
