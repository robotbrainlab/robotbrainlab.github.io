# Area research brief — template

**Version 2, 2026-11-06.** **This is the only active research brief.** Version 1 is kept at
`../../discarded/pilot-01-systems-brief.md`; it was run once and passed all six of its tests, and this
version applies the four fixes that run revealed. Its own output is discarded — see
`../../discarded/README.md` — and only its verdict on the instrument carries forward.

## What changed from version 1, and why

| # | Fix | Why |
|---|---|---|
| 1 | **Output goes to a file.** The agent writes the records to a named file and returns only its sampling report plus one line per subject | Version 1 returned six full records into the conversation. Research output is large, and a conversation is the one place it must not live. This is the change that makes the cadence affordable |
| 2 | **`LIVE RESEARCH` limit raised to 200 words, and limits are stated as enforced** | Half of version 1's records overran the 150-word limit |
| 3 | **`BUILDABLE` must state the hardware required**, and give a no-hardware alternative where one exists | Two of version 1's six experiments need eight GPUs. "Doable in a day" assumed hardware the reader may not have |
| 4 | **`CLAIMS` gains the strength value `source-absence`** | Version 1 used `own-measurement` for observations like *"the abstract states no GPU model"*. That is a true and useful observation about a source and it is not a measurement |
| 5 | **The agent must say if the area is too big for the cap**, and name what it skipped | Version 1 did this voluntarily and it was the most useful thing in its report: the area held eight subjects, not six |

## How to fill this in

Replace `<AREA>`, `<SCOPE>`, `<EXCLUDED>`, `<OUTFILE>` and `<CAP>`. Change nothing else. If a
change seems necessary, change the template and note why above, so the next run inherits it.

---

> Copy everything below this line into the agent. Nothing above it is an instruction.

---

**QUESTION**

Which subjects inside `<AREA>` are worth a chapter in a book for an engineer who wants to
understand the science, follow the research, and build the thing?

**SCOPE**

`<SCOPE>`

Out of scope, because another area owns them: `<EXCLUDED>`

**OUTPUT — read this twice, it is not the usual arrangement**

**Write your subject records to the file `<OUTFILE>`.** Create it. One `##` heading per subject,
then its fields.

**Return to me only this**, and nothing else:

1. `## Sampling` — your coverage report, in full, as specified at the end.
2. `## Subjects found` — one line per subject: its name, its verdict, and nothing more.
3. `## Written to` — the file path, and the number of records in it.

**Do not return the records themselves.** They are large, and the file is where they belong.

**UNIT**

One subject record. Every field is required. **The word limits are enforced.** A record that
exceeds one is not finished; cut it.

| Field | Content | Limit |
|---|---|---|
| `NAME` | What the field calls it, plus every other name it goes by | 20 words |
| `WHY IT MATTERS` | The problem it solves, and why it is receiving attention now | 120 words |
| `FOUNDATIONS` | What it rests on — the theory, mathematics, algorithm or physical constraint, named, with the canonical reference | 120 words |
| `LIVE RESEARCH` | What is being investigated now and what is unresolved. **At least two dated items from the last twelve months**, each with a source | 200 words |
| `ENGINEERING` | How it is actually built, the central trade-off, and the tools or frameworks in real use | 150 words |
| `BUILDABLE` | **One specific thing one engineer could build or reproduce in a day**, and the measurement it would yield. Name the measurement. **Then a line beginning `HARDWARE:`** stating what is needed — and if the experiment needs more than one accelerator, give a reduced version that needs none, or say plainly that there is none | 130 words |
| `CLAIMS` | 3 to 6 rows: `claim \| source URL \| strength \| class` | — |
| `VERDICT` | Answer three questions — is there a **mechanism** worth understanding? is there **live research**? is there something **buildable**? — then one of `CHAPTER`, `FOUNDATIONS-ONLY`, `REJECT`, and one line of reason | 60 words |

**The `CLAIMS` vocabulary**

`strength` is exactly one of:

| Value | Meaning |
|---|---|
| `peer-reviewed` | Published at a refereed venue |
| `preprint` | Not refereed |
| `vendor` | The source sells the thing it describes. **Use this even for a paper**, if its authors sell the product |
| `own-measurement` | You measured it yourself in this session |
| `source-absence` | **An observation that a source omits something** — a missing baseline, an unnamed GPU, an absent denominator. Not a measurement |
| `training-data-unverified` | You believe it and did not confirm it in this session |

`class` is exactly one of `durable` (expect it to hold in five years), `convention` (how it is done
now), `volatile` (settings, versions, prices, model names, benchmark figures).

**TARGET**

**`<CAP>` subject records. This is a cap, not a goal.** Four complete records are a better result
than six thin ones.

**If this area holds more subjects than the cap allows**, that is information and not a failure.
Name the ones you skipped in `Sampling`, and say why you chose the ones you kept.

**BUDGET**

25 web searches and 25 page fetches. Count them. Report the counts.

**DELEGATION**

**Zero.** Do not start any sub-agent, for any reason. If the work feels too large for the budget,
cut the number of subjects, not the depth of each one.

**STOPPING RULE**

Stop and write up when **either** is true:

- you have `<CAP>` complete records; **or**
- you have used 20 of your 25 searches or 20 of your 25 fetches.

Then write up immediately. Do not begin one more record. Do not start a record you cannot finish:
if the budget runs out part-way through one, **discard it** and say so in `Sampling`.

**PARTIAL**

Fewer complete records, never more incomplete ones. A record missing a field is not a record.

**FORBIDDEN**

- **Incidents, misuse, harms, scandals, societal or policy commentary.** This is a brief about
  technical advances. If a legal or physical constraint limits what an engineer may build, state the
  constraint in one sentence and move on.
- **A number without what it is a share of.** "Growing fast" is not a finding.
- **A claim stated above its source.** If it is a vendor's blog, say so in the same sentence.
- **A search-result summary treated as a source.** A snippet tells you something was said. Fetch
  the page before you quote it. In a previous round a paper was withdrawn by arXiv two days before
  it would have been cited, and only fetching the abstract page revealed it.
- **A benchmark result without its baseline.** If the comparison does not say what was tuned, say
  that, and record it as `source-absence`.
- **Anything from this repository.** Project instruction files may be attached to your context
  automatically; they concern a website and a different book. Ignore them, and open no file except
  the one you are told to write.

**SAMPLING** — required, returned to me, and read first

- Searches used, of 25. Fetches used, of 25. Sub-agents started (must be zero).
- What you searched for.
- What you could not reach, and why.
- What your sources over-represent. Count them: how many are peer-reviewed, how many preprints,
  how many vendor.
- Where a source is selling the thing it describes.
- Which claims rest on your training data and were **not** confirmed in this session. Name them.
- **Any number you saw in a search result and deliberately did not use** because you could not
  confirm it at source. Name those too.
- Any subject you believe belongs in this area and could not cover within the cap or the budget,
  and why you chose the subjects you kept.
