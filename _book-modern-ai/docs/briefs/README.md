# The briefs

One file per agent role. **Fill the placeholders in; do not rewrite the brief.** If a brief needs
changing, change the file itself, so the next run inherits the fix instead of re-discovering the
problem — and **say in the commit what the change fixes.** The history belongs in the history, not
in a growing block at the top of a brief an agent has to read past.

| Brief | Role | When it runs |
|---|---|---|
| `TEMPLATE-area-frame.md` | **Framer** — report the categories the field files its work under, as a candidate area list | Step 4, once per cycle, **before** any scout |
| `TEMPLATE-area-research.md` | **Scout** — find the subjects in one area | Research stage, one per approved area |
| `claim-verifier.md` | **Claim verifier** — re-check one claim at source, adversarially | Expire stage, and any time a claim is challenged |
| `pass-1-completeness.md` | **Completeness reviewer** | After a chapter is written |
| `pass-2-claims.md` | **Adversary** — every claim against its recorded strength | After pass 1's fixes |
| `pass-3-lab.md` | **Lab runner** — run the lab from the chapter text alone | After pass 2 |
| `pass-4-fix-verification.md` | **Fix verifier** — only the changed passages | Last |

**The writer has no brief here.** Writing a chapter is the six-step loop in `../PROCESS.md` §6, done
in the main session with the sources open, not delegated.

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

## The sentence that goes in every brief here

> If unsure, say so rather than asserting. **A wrong finding costs more than a missed one.**

A missed finding costs one defect. A wrong finding costs a verification, an argument, and sometimes
a change that makes the chapter worse. **It is in all seven**, including the framer, the claim verifier and
the lab runner, because an agent reporting a verdict it has not earned is the same failure wherever
it happens.
