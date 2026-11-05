# The briefs

One file per agent role. **Fill the placeholders in; do not rewrite the brief.** If a brief needs
changing, change it here and record what changed and why at the top, so the next run inherits the
fix instead of re-discovering the problem.

| Brief | Role | When it runs |
|---|---|---|
| `TEMPLATE-area-research.md` | **Scout** — find the subjects in one area | Research stage |
| `claim-verifier.md` | **Claim verifier** — re-check one claim at source, adversarially | Expire stage, and any time a claim is challenged |
| `pass-1-completeness.md` | **Completeness reviewer** | After a chapter is written |
| `pass-2-claims.md` | **Adversary** — every claim against its recorded strength | After pass 1's fixes |
| `pass-3-lab.md` | **Lab runner** — run the lab from the chapter text alone | After pass 2 |
| `pass-4-fix-verification.md` | **Fix verifier** — only the changed passages | Last |

**The writer has no brief here.** Writing a chapter is the six-step loop in `../PROCESS.md` §6, done
in the main session with the sources open, not delegated.

## The schema every brief follows

**`../PROCESS.md` §4.6 owns the schema.** Every file here carries its slots. Two are the same in
every brief and are repeated because they fail silently:

1. **Delegation depth is zero.** An agent that may spawn agents has no budget.
2. **The stopping rule has a fixed point** — a condition that becomes true and stays true.
   "Report everything you find" is not one.

## The sentence that goes in every review brief

> If unsure, say so rather than asserting. **A wrong finding costs more than a missed one.**

A missed finding costs one defect. A wrong finding costs a verification, an argument, and sometimes
a change that makes the chapter worse.
