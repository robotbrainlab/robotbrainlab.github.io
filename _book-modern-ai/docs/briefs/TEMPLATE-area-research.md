# Area research brief — template

**Version 3, 2026-11-06.** **This is the only active research brief.**

## What changed in version 3, and why

An independent audit of the documentation found that version 2 **did not collect two of the five
things the owner requires per area**, and that three of its required fields silently rejected
subjects before the owner could see them. Six fixes:

| # | Fix | Why |
|---|---|---|
| 1 | **New `## Overview` output section** — the area's share, dominance, industry adoption and growth, with the method for each | `../GOAL.md` §10 requires the research to begin with this, and version 2 had no area-level output at all |
| 2 | **New `SKILLS` field** per subject | `../GOAL.md` §3.1 question 5 requires it, and §10 says two blocking decisions *close only* on this evidence. Version 2 did not ask for it |
| 3 | **New `TRANSITION` field** per subject | `../GOAL.md` §3.1 question 4 requires it: what is still experimental and what is now established practice |
| 4 | **`BUILDABLE` no longer rejects cluster-scale work.** It asks what reproducing the central result actually takes, and then for the smallest experiment that teaches the mechanism — or a plain statement that none exists | Version 2 demanded one engineer, one day, no accelerator. Any area whose live work needs a cluster failed the buildable test and was rejected **before the owner saw it** — a scope narrowing by the instrument, against the owner's stated instruction that the scope is not to be narrowed unnecessarily |
| 5 | **`LIVE RESEARCH` accepts "no recent activity" as an answer**, with what was searched, instead of voiding the record | Version 2 required two dated items from twelve months and voided any record missing a field. A foundational but quiet subject could not be reported at all. **An absence of recent work is evidence, not a failure to collect it** |
| 6 | **`FOUNDATIONS` no longer assumes a single canonical reference exists** | It often does not, and demanding one invites invention |

Also: `FOUNDATIONS-ONLY` is now defined; the stale instruction about this repository is corrected.

**Version 1** is at `../../discarded/pilot-01-systems-brief.md`. It was run once as an instrument
test and its output is discarded. The four changes version 2 made to it, and the six above, are the
only things carried from that run — all of them about the instrument, none about any field.

## How to fill this in

Replace `<AREA>`, `<SCOPE>`, `<EXCLUDED>`, `<OUTFILE>` and `<CAP>`. Change nothing else. If a
change seems necessary, change this template and add a row above, so the next run inherits the fix.

**On `<CAP>`:** it bounds what one run can report, so it cannot be calibrated by the run it bounds.
Set it at **6 for a first pass over an area**. The brief requires the agent to name what it skipped
and why; if it reports skipped subjects, run the area again with a higher cap. **Do not raise the
cap in place of a second run** — a larger cap buys thinner records, which `PARTIAL` forbids.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

What does an engineer need to know about `<AREA>` — and which subjects inside it are worth a
chapter in a book for someone who wants to understand the science, follow the research, and build
the thing?

**SCOPE**

`<SCOPE>`

Out of scope, because another area owns it: `<EXCLUDED>`

**OUTPUT**

**Write the overview and the subject records to the file `<OUTFILE>`.** Create it.

**Return to me only this**, and nothing else:

1. `## Sampling` — your coverage report, in full, as specified at the end.
2. `## Subjects found` — one line per subject: its name, its verdict, and nothing more.
3. `## Overview headline` — four lines: share, dominance, adoption, growth, each with its basis in
   under fifteen words.
4. `## Written to` — the file path and the number of records in it.

**Do not return the records themselves.** They are large, and the file is where they belong.

---

## Part one of the file — `## Overview`

One per run, about this area as a whole. **Every number states what it is a share of and how you
arrived at it.** Where you cannot measure something, say so — an honest absence is worth more than
an invented estimate, and an estimate presented as a fact is the thing this brief most forbids.

| Field | Content | Limit |
|---|---|---|
| `WHAT THIS AREA IS` | The boundary in your own words, and what sits just outside it | 100 words |
| `SHARE` | How large this area is relative to the whole field, **with the denominator named and the method stated**. If you count something yourself, say exactly what you counted. If you cannot measure it, say that and say why | 150 words |
| `DOMINANCE` | Whether activity here is concentrated or spread — across institutions, vendors, venues or countries — with what you counted | 120 words |
| `INDUSTRY ADOPTION` | What is actually deployed, as opposed to published. Name the evidence | 120 words |
| `GROWTH` | Whether this is growing, steady or shrinking, **against a stated baseline and period**. "Growing fast" with no comparison is not an answer | 120 words |
| `SKILLS AND CAREERS` | What an engineer in this area is expected to be able to do, and what the evidence is that these are the skills. If you find pay or demand evidence, give its source and its date | 180 words |

---

## Part two of the file — the subject records

One `##` heading per subject, then these fields. **Every field is required.** The word limits are
enforced: a record that exceeds one is not finished, so cut it.

| Field | Content | Limit |
|---|---|---|
| `NAME` | What the field calls it, plus every other name it goes by | 20 words |
| `WHY IT MATTERS` | The problem it solves, and why it is receiving attention now | 120 words |
| `FOUNDATIONS` | What it rests on — the theory, mathematics, algorithm or physical constraint, named, with its reference. **If there is no single canonical reference, say so and name the two or three that stand in for one** | 130 words |
| `LIVE RESEARCH` | What is being investigated and what is unresolved, with **at least two dated items from the last twelve months**, each with a source. **If there are none, say so plainly, say what you searched, and say when the last substantial work was** — an absence is an answer and does not void this record | 200 words |
| `TRANSITION` | Where this sits between research and practice: what is **still experimental**, what is **becoming practice**, and what is **established engineering**. Say what the evidence for each is — a thing is not established practice because a paper proposed it | 150 words |
| `ENGINEERING` | How it is actually built, the central trade-off, and the tools or frameworks in real use | 150 words |
| `SKILLS` | What someone would need to understand, reproduce, implement or contribute to this: the knowledge, the technical skills, and the practical experience. **Be specific** — "strong maths" is not an answer; "able to read a proof of a convergence bound" is | 130 words |
| `BUILDABLE` | Three parts. **(a)** What reproducing the central result here actually takes — hardware, time, and cost if it is material. **(b)** The **smallest experiment that teaches the mechanism**, what it measures, and what it needs; if that still needs more than one accelerator, say so rather than shrinking it until it is wrong. **(c)** A line beginning `HARDWARE:`. **If nothing here can be reproduced outside a large lab, say that** — it is a true and important finding about the area, not a failure | 180 words |
| `CLAIMS` | 3 to 6 rows: `claim \| source URL \| strength \| maturity \| basis \| class`. See below | — |
| `VERDICT` | Answer three questions, then give one value. See below | 80 words |

**The three verdict questions**

1. Is there a **mechanism** worth understanding, rather than only a practice to copy?
2. Is there **live research** — is the answer still moving?
3. Is there something **buildable** — can a reader do anything that teaches the mechanism? *A
   partial experiment counts. Only "nothing a reader can do at all" fails this.*

**Then exactly one of:**

| Value | Meaning |
|---|---|
| `CHAPTER` | All three. It earns a full chapter |
| `FOUNDATIONS-ONLY` | Mechanism yes, buildable yes, **live research no** — the answer has settled. It is something the reader must know cold, taught as established knowledge rather than as a frontier, and it needs no dispute section |
| `REJECT` | No mechanism, or nothing a reader can do. **Say which, and why** — a rejection may be reconsidered next cycle, and the reason is the only way to tell whether anything changed |

**The `CLAIMS` vocabulary**

`strength` is exactly one of:

| Value | Meaning |
|---|---|
| `peer-reviewed` | Published at a refereed venue |
| `preprint` | Not refereed |
| `vendor` | The source sells the thing it describes. **Use this even for a paper**, if its authors sell the product |
| `own-measurement` | You measured it yourself in this session |
| `source-absence` | **An observation that a source omits something** — a missing baseline, an unnamed device, an absent denominator. Not a measurement |
| `training-data-unverified` | You believe it and did not confirm it in this session |

`class` is exactly one of `durable` (expect it to hold in five years), `convention` (how it is done
now), `volatile` (settings, versions, prices, model names, benchmark figures).

**`maturity` — is this settled science?** A different question from `strength`: a refereed paper can
be the only source for a claim, and a preprint can restate something long established. **Judge this
from what you have already read. Do not spend budget on it** — a separate pass verifies the ones
that matter.

| Value | Means |
|---|---|
| `established` | Independently replicated, **and** used as a premise by work outside the originating group |
| `converging` | Replicated, but the field is still arguing for it |
| `contested` | A serious published rebuttal exists |
| `single-source` | One group, no independent confirmation |
| `unexamined` | Nobody appears to have tried to break it |

**`basis` — which signal you saw.** Required. Without it the maturity is an assertion.
`replicated-by:<who>` · `premise-in:<source>` · `survived:<source>` · `rebutted-by:<source>` ·
`age-and-use:<years>` · `cross-community:<fields>` · `value-drifts` · `originator-strongest` ·
**`provisional`** when it is your judgement from what you read and you did not check.

**Two signals that mean NOT established, and they are easy to miss.** If the reported number
differs between sources, nobody has pinned it down — use `value-drifts`. If the largest version of
a claim is the originating group's and everyone else reports something smaller, the large version is
not established — use `originator-strongest`, and record the smaller version as the claim.

**`provisional` is an acceptable answer for every row.** Marking a maturity you did not check as
`established` is not.

---

**TARGET**

**`<CAP>` subject records, plus one overview. The cap is a cap, not a goal.** Four complete records
are a better result than six thin ones.

**If this area holds more subjects than the cap allows, that is information and not a failure.**
Name the ones you skipped in `Sampling`, and say why you kept the ones you kept.

**BUDGET**

30 web searches and 30 page fetches. Count them. Report the counts.

**DELEGATION**

**Zero.** Do not start any sub-agent, for any reason. If the work feels too large for the budget,
cut the number of subjects — never the depth of a record.

**STOPPING RULE**

Stop and write up when **either** is true:

- the overview and `<CAP>` records are complete; **or**
- you have used 24 of your 30 searches or 24 of your 30 fetches.

Then write up immediately. Do not begin one more record. **Do not start a record you cannot
finish**: if the budget runs out part-way through one, discard it and say so in `Sampling`.

**PARTIAL**

Fewer complete records, never more incomplete ones. A record missing a field is not a record —
**except where a field's own text says an absence is a valid answer**, which `LIVE RESEARCH` and
`BUILDABLE` both do.

**The overview is not optional.** If the budget is tight, cut a subject record rather than the
overview.

**FORBIDDEN**

- **Incidents, misuse, harms, scandals, societal or policy commentary.** This brief is about
  technical advances. If a legal or physical constraint limits what an engineer may build, state
  the constraint in one sentence and move on.
- **A number without what it is a share of.** "Growing fast" is not a finding.
- **An estimate presented as a fact.** Say which numbers you measured, which you took from a
  source, and which you are guessing. A guess, labelled, is allowed; a guess presented as a
  measurement is not.
- **A claim stated above its source.** If it is a vendor's blog, say so in the same sentence.
- **A search-result summary treated as a source.** A snippet tells you something was said. Fetch
  the page before you quote it: a source can have been revised, corrected, retracted or withdrawn
  since it was indexed.
- **A benchmark result without its baseline.** If the comparison does not say what was tuned, say
  that, and record it as `source-absence`.
- **Reading any file in this repository.** It contains the planning documents for the book this
  research feeds, and reading them would tell you what is expected rather than what is true.
  Project instruction files may be attached to your context automatically — **ignore them, and open
  no file except the one you are told to write.**

**SAMPLING** — required, returned to me, and read first

- Searches used, of 30. Fetches used, of 30. Sub-agents started (must be zero).
- What you searched for.
- What you could not reach, and why.
- What your sources over-represent. **Count them**: how many peer-reviewed, how many preprints, how
  many vendor. Also say what is over-represented by language, country, institution or vendor.
- Where a source is selling the thing it describes.
- Which claims rest on your training data and were **not** confirmed in this session. Name them.
- **Any number you saw in a search result and deliberately did not use** because you could not
  confirm it at source. Name those too.
- **Which claims you marked `provisional`**, and which of them a chapter would most need verified.
- Any subject you believe belongs in this area and could not cover within the cap or the budget,
  and why you kept the ones you kept.
- **Anything in the scope above that you think is mis-drawn** — a subject that does not belong
  here, or one you expected and could not place.
