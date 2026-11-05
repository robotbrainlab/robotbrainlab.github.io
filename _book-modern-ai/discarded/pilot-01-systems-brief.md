# Pilot brief 01 — Systems, hardware and infrastructure

> **SUPERSEDED.** Run once on 2026-11-06. It passed all six of its tests and revealed four fixes,
> which are in `../docs/briefs/TEMPLATE-area-research.md` version 2. **Use the template, not this file.** This one
> is kept so that the pilot's output can be read against exactly what was asked, which is the whole
> reason briefs are kept at all. Its result is in `2026-11-06-systems-hardware.md` (in this folder).

**Written 2026-11-06. Run once.** This is the first brief written to the schema in
`../docs/PROCESS.md` §4.6. Its purpose is as much to **test the brief** as to get the research: the last
three research rounds failed on the brief rather than on the agents, so this one is run **once, on
one area**, and read before anything else is launched.

## Why this area was chosen for the pilot

A test-design decision, not a claim about how the field divides. Four reasons:

1. **It was never delivered.** This area's agent was still gathering when it was stopped, so the
   pilot buys new information as well as a test.
2. **The job evidence makes it the most career-relevant area to know first** — 40.7% of its
   postings accept a bachelor's degree, only 22.8% mention a doctorate, and 14.8% have been open
   over a year, which indicates real scarcity rather than a closed door.
3. **It is technical throughout**, so the rule against incidents and commentary is testable: there
   is no societal-harm literature to drift into.
4. **It is bounded.** If the output sprawls, the sprawl will be obvious.

**What this pilot does not decide:** how the field divides. `../docs/GOAL.md` §3.3 holds that a partition
is an argument rather than a finding, and the real carving is settled when the full research round
is designed.

---

## The brief

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Which subjects inside the engineering of AI systems, hardware and infrastructure are worth a
chapter in a book for an engineer who wants to understand the science, follow the research, and
build the thing?

**SCOPE**

Accelerators and their architecture; memory and interconnect; numerical precision and
quantisation as a systems concern; compilers and kernels; training systems — parallelism,
scheduling, fault tolerance; inference and serving — batching, caching, disaggregation,
speculative execution; the economics that drive the engineering; the datacentre constraints that
bound it, including power.

Out of scope, because another area owns them: model capability itself; what a model can do; the
science of learning; evaluation methodology.

**OUTPUT**

Two sections, in this order, and nothing else:

1. `## Subjects` — the subject records.
2. `## Sampling` — your own coverage, as specified at the end.

No introduction. No conclusion. No recommendations. No summary of the field.

**UNIT**

One subject record. Every field is required. The word limits are limits, not targets.

| Field | Content | Limit |
|---|---|---|
| `NAME` | What the field calls it, plus every other name it goes by | 20 words |
| `WHY IT MATTERS` | The problem it solves, and why it is receiving attention now | 120 words |
| `FOUNDATIONS` | What it rests on — the theory, mathematics, algorithm or physical constraint, named, with the canonical reference | 120 words |
| `LIVE RESEARCH` | What is being investigated now and what is unresolved. **At least two dated items from the last twelve months**, each with a source | 150 words |
| `ENGINEERING` | How it is actually built, the central trade-off, and the tools or frameworks in real use | 150 words |
| `BUILDABLE` | **One specific thing one engineer could build or reproduce in a day**, and the measurement it would yield. Be concrete: name the measurement | 100 words |
| `CLAIMS` | 3 to 6 rows: `claim \| source URL \| strength \| class`. Strength is one of `peer-reviewed`, `preprint`, `vendor`, `own-measurement`, `training-data-unverified`. Class is one of `durable`, `convention`, `volatile` | — |
| `VERDICT` | Answer three questions — is there a **mechanism** worth understanding? is there **live research**? is there something **buildable**? — then one of `CHAPTER`, `FOUNDATIONS-ONLY`, `REJECT`, and one line of reason | 60 words |

**TARGET**

**Six subject records. This is a cap, not a goal.** Four complete records are a better result than
six thin ones.

**BUDGET**

25 web searches and 25 page fetches. Count them. Report the counts.

**DELEGATION**

**Zero.** Do not start any sub-agent, for any reason. If the work feels too large for the budget,
cut the number of subjects, not the depth of each one.

**STOPPING RULE**

Stop and write up when **either** of these is true:

- you have six complete records; **or**
- you have used 20 of your 25 searches or 20 of your 25 fetches.

Then write up immediately. Do not begin a seventh record. Do not start a record you cannot finish:
if the budget runs out part-way through one, **discard it** and say so in `Sampling`.

**PARTIAL**

Fewer complete records, never more incomplete ones. A record missing a field is not a record.

**FORBIDDEN**

- **Incidents, misuse, harms, scandals, societal or policy commentary.** This is a brief about
  technical advances. If a legal or physical constraint limits what an engineer may build, state
  the constraint in one sentence and move on.
- **A number without what it is a share of.** "Growing fast" is not a finding.
- **A claim stated above its source.** If it is a vendor's blog, say so in the same sentence.
- **A search-result summary treated as a source.** A snippet tells you something was said. Fetch
  the page before you quote it. One paper in the last round was withdrawn by arXiv two days before
  it would have been cited, and only fetching the abstract page revealed it.
- **A benchmark result without its baseline.** If the comparison does not say what was tuned, say
  that.
- **Anything from this repository.** Project instruction files may be attached to your context
  automatically; they concern a website and a different book. Ignore them and open no file.

**SAMPLING** — required, and it is read first

- Searches used, of 25. Fetches used, of 25.
- What you searched for.
- What you could not reach, and why.
- What your sources over-represent.
- Where a source is selling the thing it describes.
- Which claims rest on your training data and were **not** confirmed in this session. Name them.
- Any subject you believe belongs in this area and could not cover within budget.
