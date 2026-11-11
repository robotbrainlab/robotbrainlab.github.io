# The briefs

One file per agent role. **Fill the placeholders in; do not rewrite the brief.** If a brief needs
changing, change the file itself, so the next run inherits the fix instead of re-discovering the
problem — and **say in the commit what the change fixes.** The history belongs in the history, not
in a growing block at the top of a brief an agent has to read past.

| Brief | Role | When it runs |
|---|---|---|
| `TEMPLATE-area-frame.md` | **Framer** — report the categories the field files its work under, faithfully and without filtering | **At step 4, one run and not two** `[2026-11-07]`, in a fresh session outside this repository, before any scout. **How often framing happens at all is `../PROCESS.md` §5's** — at step 4, then only on an approved `RECARVE`, not every cycle |
| `TEMPLATE-area-consolidate.md` | **Consolidator** — turn the framers' records into one candidate area list: classify, merge, pick one level | At step 4, **once**, after the framing run and before the owner rules. Same cadence as the framer, and `../PROCESS.md` §5 owns it |
| `TEMPLATE-area-research.md` | **Scout** — find the subjects in one area | Research stage, one per approved area |
| `claim-verifier.md` | **Claim verifier** — re-check one claim at source, adversarially | **Three occasions, and the brief owns the list** — at CONFIRM, at EXPIRE, and whenever a claim is challenged. `[2026-11-11]` This row named two and dropped CONFIRM, which the brief itself calls the one easily forgotten |
| `pass-1-completeness.md` | **Completeness reviewer** | After a chapter is written |
| `pass-2-claims.md` | **Adversary** — every claim against its recorded strength | After pass 1's fixes |
| `pass-3-lab.md` | **Lab runner** — run the lab from the chapter text alone | After pass 2 |
| `pass-4-fix-verification.md` | **Fix verifier** — the changed passages as its subject, the whole chapter as its search | Last |
| `area-proposal.md` | **Area proposer** — which of the candidate areas the book covers, with what every cut costs | Step 4 part 3, after the consolidation run and before the owner rules. **Not delegated**: Claude works to it in the main session |
| `document-check.md` | **Document checker** — the only instrument that reads what Claude writes: citations that do not hold, contradictions with a marked decision, claims past their evidence | Before any document in `../` is called finished, and after any rule change |

**The writer has no brief here.** Writing a chapter is the six-step loop in `../PROCESS.md` §6, done
in the main session with the sources open, not delegated.

**The area proposal is not delegated either, but it does have a brief** — `area-proposal.md`.
The consolidator returns an **inventory**; what the owner rules on is a **proposal**. Turning one
into the other is Claude's, in the main session, against §1.1's career goal and §3.1's five
questions (`../GOAL.md` §3.3).

**`[2026-11-11, evening]` This section said the stage had no brief, "because an agent cannot do
it".** That argued against *delegating* the judgement and was then read as an argument against
*bounding* it, so the stage that made the largest reduction in the pipeline — 63 areas to 12 — ran
with no output shape, no stopping rule and no forbidden list. An independent review found what it
lost: `Intelligent Robotics`, the best-attested area in the register, and with it **world models**
(which the consolidation had flagged as "the only subject no other source names"), **Control
methods**, **six AAMAS areas**, **expert systems and theorem proving**, and **all five `UNCLEAR`
categories that `TEMPLATE-area-consolidate.md` required the proposal to dispose of.** A brief can
bound a judgement made in the main session; that is what `area-proposal.md` does.

**Never hand him the inventory and call it the list** — that happened, four times, and it is what
`../POSTMORTEM-2026-11-11.md` and §3.3's history note record.

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
demonstrated by inventing their own cutting rules. Splitting the jobs makes the judgement checkable:
**a consolidator's output can be read back against the records it came from, and a filtering
reporter's cannot.**

**`[2026-11-11]` That has now been done once, so it is an observation and not only an argument.**
The consolidation of run `g` was read back against run `g`'s own records
(`../CHECK-consolidation-2026-11-07-g.md`, written before the output existed), and the read-back
found two things the run's own summary did not report: **32 labels it moved into appendices and
never gave a verdict**, and **thirteen kept areas resting on scope the source may not have
written** (`../DIAGNOSIS-2026-11-07.md` §9). **One read-back is one instance**, not a property of
the method.

**The same shape already exists one level down.** A scout reports claims; CONFIRM transforms them
into `CLAIMS.tsv` rows (`../PROCESS.md` §5.1). This is that pattern applied to areas.

## The schema every brief follows

**`../PROCESS.md` §4.6 owns the schema**, and this file does not restate it.

**Four slots are in every brief here**, because each fails silently when left out: `OUTPUT`,
`BUDGET`, `STOPPING RULE` and `DELEGATION`.

**The rest are per brief, and there are three kinds here:**

| Kind | Which | Slots |
|---|---|---|
| **Record-producing, bounded by a count** | The scout | Ten slots, **with `SCOPE` where the others head a `UNIT`** — its unit is specified field by field inside `OUTPUT`, which is what the schema asks a `UNIT` for. `TARGET` and `SAMPLING` bound what it returns |
| **Record-producing, bounded by something else** | The framer, the consolidator | `UNIT` yes, and **`TARGET` yes but carrying no count** — each uses the slot to state what bounds it, which is what `../PROCESS.md` §4.6 asks of a brief with no cap. The framer's bound is the source register it is given (`TEMPLATE-area-frame.md`: **the two floors were removed on 2026-11-07** and the register replaced them); the consolidator's is its input, which is finite because the framing files are already written |
| **Finding-producing** | The four passes, the claim verifier, the document checker | **`UNIT` and `SAMPLING` folded into `OUTPUT`**, which names the sections and, in five of the six, asks for coverage in one — `pass-2-claims.md` asks instead through `## Clean` and its `PARTIAL`. The question is stated as `YOUR JOB` or `QUESTION`. **Four cap no number of findings; two cap at one** — the claim verifier ("One claim") and the lab runner ("One verdict"), because each is given a single subject |

A brief that leaves out one of the four universal slots is defective. **A brief with no cap states in
`TARGET` what bounds it in place of one** (`../PROCESS.md` §4.6, which owns the schema and that
sentence).

## No agent substitutes matching for reading

**[AGREED 2026-11-07]** Every brief here carries this rule, because an agent cannot read this file.
**It carries it as a `FORBIDDEN` bullet addressed to the agent, not as the sentence below** —
`[2026-11-11]` this said "word for word", and no brief carries these words. The rule is the same in
all ten; `document-check.md`'s copy adds one sentence about citations and drops two. **A drift is
still visible, because the bullets are near-identical to each other**, which is what the word-for-word
rule in `../CLAUDE.md` exists for:

> **An agent reads and judges. It may not substitute a search, a pattern, a count or a lookup for
> reading.** A pattern match tells you where a string is; it cannot tell you what the thing means.
> Where a search or count is used it is a **hint about where to read**, never the finding.

**The line that has to survive, or this would delete the gates.** **Automation may check form. It
may never judge content.**

| May be automated | May not |
|---|---|
| Does this equation evaluate · does this table have the right number of cells · is this hash stale · does this string appear · how many times | Is this an area · is this claim overstated · does this explanation teach · does this chapter sit in the right place · is this the same category under another name |

The fourteen gates all check form. **`../GATES.md`'s "Form and content" names the judgements no
gate can make** — whether a claim is overstated, whether an explanation teaches, whether a chapter
belongs where it sits — and its "What no gate reads" lists the five rules nothing samples at all.
`[2026-11-11]` This sentence cited the second section for what the first says. **`tools/sweep.py` is the clearest case**: it counts occurrences, which
is a hint, and `../LEDGER-DEFECTS.md` entry 5 already says the sweep is followed by **reading** the
sections it touched, because a phrasing nobody thought of has no string to search for.

**Why this is a rule and not a preference.** Three times in one day a pattern match was used here to
answer a question about meaning, and all three failed: a sweep for withdrawn evidence found six
places where reading found twenty-five; a pattern over category names both over-matched and missed
two entire classes; and a keyword lookup, seeded with what its author already believed, returned
only what it was given. **In all three, automation gave no context, which was the whole of what the
question asked for** — the general form of that sentence is the standing rule the briefs carry, not a
finding drawn from these three.

## The sentence that goes in every brief here

> If unsure, say so rather than asserting. **A wrong finding costs more than a missed one.**

A missed finding costs one defect. A wrong finding costs a verification, an argument, and sometimes
a change that makes the chapter worse. **It is in all ten**, including the framer, the consolidator, the area proposer, the
claim verifier, the lab runner and the document checker, because an agent reporting a verdict it has
not earned is the same failure wherever it happens.
