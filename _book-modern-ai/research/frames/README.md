# Framing runs

One file per framing run, named `YYYY-MM-DD-<run-id>.md`, plus **`SOURCES.md`, the source register —
read that first.** It is the list of filing systems a framing run opens, and the run no longer
chooses its own.

**[2026-11-07] Runs no longer come in pairs.** They did, so that "a division that is an artefact of
whichever sources one run opened shows up as a disagreement before the owner rules". **The register
removes the source choice, so it removes the artefact** — and it gives a single run something a pair
never did: a recorded floor of what each page was already found to carry, which a run can be checked
against. `../../docs/DIAGNOSIS-2026-11-07.md` has the measurement behind this.

**Run ids run `a`, `b`, `c`, `d` …** — the next unused letter. Nothing is ever deleted: a superseded
run is still evidence of what a source carried on a date.

**Framing happens at step 4, not every cycle.** The areas persist across cycles; they are re-framed
only when a `RECARVE` is approved (`../../docs/PROCESS.md` §5).

They live in their own directory because the scouts' files in `../` are named
`YYYY-MM-DD-<area-slug>.md`, and a framing run's name would be read as an area.

## What is here

- `2026-11-06-a.md`, `2026-11-06-b.md` — **the first pair, superseded.** Each hit a cap and invented
  its own rule for cutting the list, which is why the brief was changed.
- `2026-11-06-c.md`, `2026-11-06-d.md` — the second pair. 86 and 209 categories, nothing filtered.
  **For a time these held the only record of two things the later pair lost** — a standards body's
  working groups (`d`, which found 5 and missed the 3 joint groups) and a refereed alignment track
  (`c` and `d`). Both were then named in `SOURCES.md` so that a future run reaches them on its own,
  **and run `g` did: it recovered the alignment track and found all 8 groups.** `[2026-11-11]` This
  entry said "the only record" until run `g` superseded it.
- `2026-11-07-e.md`, `2026-11-07-f.md` — the third pair, and **the last pair**. 104 and 77 categories.
- `2026-11-07-g.md` — **the first run over the register, and the current one.** 283 categories from
  all nineteen registered sources, 3,211 lines. It is the only run that opened every source, and the
  only one that recovered both of the things the earlier runs lost. **It is the input to the next
  consolidation run.** `../../docs/CHECK-run-g-2026-11-07.md` is the pass/fail list written *before*
  its output existed, and `../../docs/DIAGNOSIS-2026-11-07.md` §7 is the result of checking it.
- `SOURCES.md` — **the source register.** Every filing system any run opened, the level to take from
  it, what it was already found to carry, and the route round it where it blocks. Built from runs
  `a`–`f`; no new research went into it. **`[2026-11-07]` Its `CARRIES` column was then ratcheted
  upwards by run `g`**, which opened all nineteen — floors only ever rise, so a later run that
  reports less than the register holds has failed, visibly.
- `MERGED-CANDIDATES.md` — runs `a`–`d` merged: 254 distinct categories with their source counts.
  **Not a proposal, and not comparable with a consolidated list** — it is every name any source
  carried, before any rejection on kind.
- `CONSOLIDATED-2026-11-07-g.md` — **run `g` consolidated, and the current candidate list.** 63
  areas from 283 input categories, with a numbered ledger of all 283. **This is what the owner rules
  on at step 4.** Read `../../docs/DIAGNOSIS-2026-11-07.md` §9 first: it names the thirteen areas
  kept on scope that may not be their source's, and the 32 labels that got no verdict.
- `CONSOLIDATED-2026-11-07.md` — runs `e` and `f` consolidated: 181 records, each with one verdict,
  of which 69 are areas. **Read `../../docs/DIAGNOSIS-2026-11-07.md` before comparing this with
  `MERGED-CANDIDATES.md`**: the two count different things, and comparing them directly is what made
  the method look like it was getting worse.
