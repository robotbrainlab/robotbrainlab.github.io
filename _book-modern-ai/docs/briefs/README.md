# The briefs

One file per agent role. **Fill the placeholders in; do not rewrite the brief.** If a brief needs
changing, change the file itself, so the next run inherits the fix instead of re-discovering the
problem — and **say in the commit what the change fixes.** The history belongs in the history, not
in a growing block at the top of a brief an agent has to read past.

| Brief | Role | When it runs |
|---|---|---|
| `TEMPLATE-area-frame.md` | **Framer** — report the categories the field files its work under, faithfully and without filtering | Step 4, **twice per cycle**, in a fresh session outside this repository, before any scout |
| `TEMPLATE-area-consolidate.md` | **Consolidator** — turn the framers' records into one candidate area list: classify, merge, pick one level | Step 4, **once**, after the framing runs and before the owner rules |
| `TEMPLATE-area-research.md` | **Scout** — find the subjects in one area | Research stage, one per approved area |
| `claim-verifier.md` | **Claim verifier** — re-check one claim at source, adversarially | Expire stage, and any time a claim is challenged |
| `pass-1-completeness.md` | **Completeness reviewer** | After a chapter is written |
| `pass-2-claims.md` | **Adversary** — every claim against its recorded strength | After pass 1's fixes |
| `pass-3-lab.md` | **Lab runner** — run the lab from the chapter text alone | After pass 2 |
| `pass-4-fix-verification.md` | **Fix verifier** — only the changed passages | Last |

**The writer has no brief here.** Writing a chapter is the six-step loop in `../PROCESS.md` §6, done
in the main session with the sources open, not delegated.

## Report, then consolidate — two agents, never one

**[AGREED 2026-11-07]** A research stage has two jobs and they do not belong to the same agent.

| Job | Who | Rule |
|---|---|---|
| **Report** | The framer, the scout | Record what the sources carry, **faithfully and without filtering.** No selection rule of its own, no judgement about what belongs |
| **Consolidate** | The consolidator | Turn that record into something the owner can rule on: classify by kind, merge duplicates, pick one level. **May reject on kind, never on importance** |

**Why it is two.** The first framing runs were asked to report filing categories and did so
correctly — and filing categories include application domains, session formats, audience labels and
a benchmark vendor's product names, because that is what venues route submissions by. **A faithful
report of how a field files its work is not a list of research areas.**

The tempting fix was a rejection rule inside the framing brief. **That would have made the reporter
the judge**, which is the defect that brief exists to prevent and which its first two runs
demonstrated by inventing their own cutting rules. Splitting the jobs keeps the record honest and
makes the judgement checkable: **a consolidator's output can be read back against the records it
came from, and a filtering reporter's cannot.**

**The same shape already exists one level down.** A scout reports claims; CONFIRM transforms them
into `CLAIMS.tsv` rows (`../PROCESS.md` §5.1). This is that pattern applied to areas.

## The schema every brief follows

**`../PROCESS.md` §4.6 owns the schema**, and this file does not restate it.

**Four slots are in every brief here**, because each fails silently when left out: `OUTPUT`,
`BUDGET`, `STOPPING RULE` and `DELEGATION`.

**The rest are per brief.** The research brief carries all ten, because it produces records rather
than findings and needs `UNIT`, `TARGET` and `SAMPLING` to bound them. **A review brief folds
`UNIT` and `SAMPLING` into `OUTPUT`**, which names its sections and asks for a coverage report, and
states its question as `YOUR JOB` or `QUESTION` — a review returns findings, which have no fixed
unit count to cap. A brief that leaves out one of the four above is defective; a review brief
without `UNIT` is not.

## No agent substitutes matching for reading

**[AGREED 2026-11-07]** Every brief here carries this, word for word, because an agent cannot read
this file:

> **An agent reads and judges. It may not substitute a search, a pattern, a count or a lookup for
> reading.** A pattern match tells you where a string is; it cannot tell you what the thing means.
> Where a search or count is used it is a **hint about where to read**, never the finding.

**The line that has to survive, or this would delete the gates.** **Automation may check form. It
may never judge content.**

| May be automated | May not |
|---|---|
| Does this equation evaluate · does this table have the right number of cells · is this hash stale · does this string appear · how many times | Is this an area · is this claim overstated · does this explanation teach · does this chapter sit in the right place · is this the same category under another name |

The fourteen gates all check form, and `../GATES.md`'s "What no gate reads" already names the
judgements no gate can make. **`tools/sweep.py` is the clearest case**: it counts occurrences, which
is a hint, and `../LEDGER-DEFECTS.md` entry 5 already says the sweep is followed by **reading** the
sections it touched, because a phrasing nobody thought of has no string to search for.

**Why this is a rule and not a preference.** Three times in one day a pattern match was used here to
answer a question about meaning, and all three failed: a sweep for withdrawn evidence found six
places where reading found twenty-five; a pattern over category names both over-matched and missed
two entire classes; and a keyword lookup, seeded with what its author already believed, returned
only what it was given. **Automation gives no context, which is the whole of what the question
asked for.**

## The sentence that goes in every brief here

> If unsure, say so rather than asserting. **A wrong finding costs more than a missed one.**

A missed finding costs one defect. A wrong finding costs a verification, an argument, and sometimes
a change that makes the chapter worse. **It is in all eight**, including the framer, the consolidator, the claim
verifier and the lab runner, because an agent reporting a verdict it has not earned is the same
failure wherever it happens.
