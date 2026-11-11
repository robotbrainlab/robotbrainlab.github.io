# Checking framing runs `h` and `i`, before the consolidation

**Written 2026-11-12, before the consolidator ran.** `ROADMAP.md` step 4 requires it: *"Check each
run against its own coverage section before the consolidator runs, and check the runs against each
other."* **This check is reading, not a script.** Every figure below is quoted from a run's own
words unless it says otherwise.

**The verdict first: both runs pass, and the pair earned its cost.** Each recovered something the
other reports as lost, so consolidating either alone would have lost a whole source's taxonomy.

---

## 1. Each run against the brief's floors

| | Run `h` | Run `i` |
|---|---|---|
| **Source floor** — 8 sources across 4 kinds | **Met.** 9 sources, 5 kinds: review-venue 3, index 2, programme 1, survey 1, practitioner 2 | **Met.** 10 sources, 5 kinds: review-venue 4, index 2, practitioner 2, programme 1, survey 1 |
| **Search floor** — 10 searches | **Met.** 11 of 25 | **Met.** 16 of 25 |
| Fetches | 23 of 25 | 24 of 25 |
| **Sub-agents started** | **0** | **0** |
| Categories reported | 172 | 135 |
| Categories resting on a RECALLED source | **None.** Every unit has a FETCHED source with a URL | **None.** Same |
| Every source opened accounted for | Yes | Yes |
| Sources looked for and not usable, with what was tried | Yes, 6 entries with routes | Yes, 8 entries with routes |

**Both coverage sections are honest about their own weakest point**, unprompted:

- `h`: *"one commercial US conference supplies 36 of the 172 labels, so a large share of this run's
  applied vocabulary rests on a single meeting's programme committee."*
- `i`: *"The `survey` slot is the weakest"* — it fell back to a 2021 report after searching twice
  for a field-wide survey newer than that and finding none reachable.

**Both are honest about an instrument artefact.** Each took all 40 of arXiv's Computer Science
categories, so roughly thirty categories that nobody would call AI are in both lists. `i` states
why in its own words: *"the choice to report it in full was the only alternative to filtering it by
my own judgement. A reader should treat their presence as a property of the instrument."* **That is
the brief working as intended** — the framing run reports, and the consolidator judges kind.

---

## 2. What one run found and the other did not

**Seven sources are common to both**: NeurIPS CFP, ICML CFP, the arXiv taxonomy, the ACM CCS SKOS
file, MLCommons, ISO/IEC JTC 1/SC 42 and the AI Engineer World's Fair. **Three of those seven are
not the same reading**, which matters as much as the sources that differ:

| Common source | Run `h` | Run `i` | Why it matters |
|---|---|---|---|
| ICML | the **2026** call | the **2025** call | Two years of one venue's wording |
| AI Engineer World's Fair | the **2026** programme, 36 distinct labels across 40 track slots | the **2025** programme, 18 tracks | `h`'s is a year newer and twice the size; `i`'s is the one that names `Product Management` |
| ISO/IEC JTC 1/SC 42 | **the body's own host**, `committee.iso.org`, after `iso.org` refused | **a Wikipedia reproduction**, after the same refusal | `h` found the route that works. `i` says its own route *"already disagrees with a 2024 ISO agenda on one group's title"* |

**And four sources are in one run only. Each covers a hole the other run reports:**

| Only in | Source | What it carries | What the other run says about it |
|---|---|---|---|
| `h` | **ACL Rolling Review** | **31 language tracks** — the only fine-grained language taxonomy in either run | `i` has nothing comparable. Both general venues compress all of language into one topic |
| `h` | **AAAI 2025 Presidential Panel**, 17 chapters | `AGI`, `Embodied AI`, `Hardware & AI`, `AI Agents` as standing research chapters | `i` has no AAAI survey |
| `i` | **AAAI-26 keywords**, 16 areas over 296 keywords | A general-AI venue's real routing taxonomy — *"the list authors actually choose from"* | **`h` searched for AAAI's main-track areas and failed**: *"the search returned only the AI for Social Impact track call… AAAI's review-venue categories are absent from this run"* |
| `i` | **Stanford CRFM foundation-models report**, 26 subsections | `Adaptation`, `Training`, `Modeling` as named stages of one pipeline | `h` has no foundation-model survey |

**This is the whole argument for running more than one.** `h` reports AAAI's venue taxonomy as a
hole and `i` fills it. `i` has no language taxonomy and `h` carries 31 tracks of one. **Taking
either run alone would have lost a whole source's filing system with nothing to say it was
missing.** The consolidation must union, never intersect, and the brief says so.

---

## 3. What both runs missed, in the same words

1. **Roles and occupations.** Both looked for a job board; both failed. `h`: *"aijobs.net was
   script-rendered and gave me nothing, and I found no substitute."* `i`: *"the one I looked for,
   ai-jobs.net, appears to have been taken down."* **Between them the only role-shaped labels come
   from the two World's Fair programmes** — `h` names `AI-Native Enterprises`, `AI Architects` and
   `CTO Circle`; `i` names `Product Management`, `L1: AI Architects` and `L2: AI in the Fortune
   500`. **This is the second cycle in which the gap has been reported and the
   owner has asked for a route. It is still open**, and no list produced from these two runs can
   close it.
2. **Non-English filing systems.** All 19 source readings are in English. Neither searched CCF,
   CAAI or JSAI.
3. **Unpublished industrial work.** Every source files work that was submitted, archived,
   presented or standardised.
4. **The newest calls.** `i` names NeurIPS 2026, ICML 2026 and NeurIPS's Datasets & Benchmarks call
   as known to exist and unopened; `h` took NeurIPS's main track only.

---

## 4. Two things to watch in the consolidation's output

**Neither is a defect in the runs. Both are places the next stage can quietly lose something.**

1. **The rule has no verdict for a plain computer-science category.** Its drop clause names four
   kinds — another field's problems, AI's effect on the world, a meeting format or audience, an
   organisation. **`cs.OS`, `cs.NI`, `cs.PL` and most of their siblings are none of those**; they
   are computer science that is not AI. **Both runs took the same 40 arXiv categories**, so the
   union holds 40 of these records after merging, and only about seven of the 40 — `cs.AI`,
   `cs.LG`, `cs.CV`, `cs.CL`, `cs.RO`, `cs.MA`, `cs.NE` — are AI subjects by name. **If the
   consolidation drops the rest under a clause that does not cover them, it has extended the
   rule**, which its own `FORBIDDEN` list prohibits. The honest handling is a named verdict or an
   entry under *what this run could not settle*.
2. **The records with no scope statement.** Both runs say plainly, in many `INCLUDES` fields, *"The
   source gives the name and the level and no scope statement."* The brief says such a record
   **cannot be an `AREA`** and must be `UNCLEAR`. That rule exists because an earlier run gave
   `AREA` to fourteen of them. **A low `UNCLEAR` count in this consolidation is a reason to look,
   not a reason to be pleased.**

---

## 5. What this check did not do

- **It did not read all 307 records.** It read both coverage sections in full, both disagreement
  sections in full, `i`'s level table in full, and a sample of records from each run — enough to
  confirm the format, the honesty of the `INCLUDES` fields and the floors. **Judging all 307 is the
  consolidation's job**, and checking its judgement is the next step's.
- **It did not verify a single source at its URL.** No fetch was made. If a run misquoted a source,
  this check would not catch it.
- **It takes each run's own budget figures as given.** Nothing here can confirm that `h` used 11
  searches or that `i` used 16.
