# Checking the consolidation of runs `h` and `i`

**Written 2026-11-12, after the run, against `briefs/TEMPLATE-area-consolidate.md`.** The paired
check written *before* it is `CHECK-runs-h-i-2026-11-12.md`, which named two things to watch; both
are answered below.

**Verdict: it passes. Three errors found, all of them in its own summary prose, none of them
changing a verdict.** The lists are right and the summary miscounts them.

---

## 1. The arithmetic closes, and I re-added all of it

| Check | Result |
|---|---|
| Union | 172 (`h`) + 135 (`i`) = **307** ✓ |
| Merge table | 35 + 12 + 12 + 8 + 5 + 2 + 2 + 2 + 2 + 2 + 1 + 1 = **84** ✓ |
| Distinct | 307 − 84 = **223** ✓ |
| Verdicts | 47 + 51 + 9 + 17 + 0 + 99 = **223** ✓ |
| Rejected section | DOMAIN 51 + RECORD 9 + FORMAT 17 + PRODUCT 0 = **77**, and the section says 77 ✓ |

**This is the thing the brief exists to force**, and `LEDGER-DEFECTS.md` entry 5a is why: a stage
that declares no total cannot report a loss. This one declares its input total, closes over it, and
states in its own words that *"every one of the 307 records from the two runs is either a unit
above, a line in Rejected, a line in Unclear, or named inside a `MERGED FROM` or a `BELOW` field."*

## 2. Three errors, all in the summary

| # | What it says | What the list says |
|---|---|---|
| 1 | *"the **ten** arXiv categories that carry AI-adjacent ground"* | It then names **thirteen** — cs.AR, cs.CR, cs.DB, cs.DC, cs.GT, cs.HC, cs.IR, cs.LO, cs.PF, cs.SC, cs.SD, cs.SE, cs.SY — and **thirteen** carry **Close** in the Rejected list. The word is wrong; the list is right |
| 2 | *"the **five** ACM CCS siblings with the same problem"* | **Three** are marked **Close**: Distributed computing methodologies, Modeling and simulation, Symbolic and algebraic manipulation. Computer graphics, Concurrent and Parallel computing methodologies are rejected **without** Close. Its other count — *"six ACM CCS siblings"* under the policies, meaning all CCS siblings rejected — is correct, and the two counts are measuring different things |
| 3 | *"(JWG 3 health, **JWG 7** finance)"* | The Rejected line for the second names it *"Joint Working Group SC 42 – ISO/TC 68: Artificial intelligence"* with **no number**. `JWG 7` is asserted in the summary and unsupported in the list |

**Why this matters more than three numbers.** The summary is what the next stage reads first, and
`GOAL.md` §11 class A is exactly this: *having the summary is worse than having nothing, because
nothing makes you look.* A reader taking *"ten arXiv categories"* forward would re-raise three
fewer borderline rejections than the run actually flagged.

## 3. The two things the pre-check said to watch

**(a) The rule has no verdict for a plain computer-science category.** Predicted, and it happened —
80 such records in the union, 40 from each run. **It handled them the honest way**: filed as
`DOMAIN`, marked *(not AI)* on **every one** of the lines, and given a paragraph of its own under
*Two reading policies*, which says plainly that the brief's six verdicts have no bucket for this
case. **It did not extend the rule to cover them**, which its own `FORBIDDEN` list prohibits. It is
reported upward instead, which is what should happen.

**(b) A low `UNCLEAR` count would have been a reason to look.** It came back at **99 of 223, 44%**
— the honest direction, and far above the fourteen that an earlier run of this brief wrongly called
`AREA`. Policy **P1** is why: a bare track name is not scope, *"however unambiguous it looks"*, so
*Graphs*, *Harness Engineering*, *Evals*, *Security*, *Vision* and *Language* are all undecided.

## 4. What it did right that the brief did not require

- **It declared both rules it had to invent** (P1, scope from an enumerated child list; P2,
  rejecting on a stated *kind* without a scope statement) and marked both overturnable.
- **It declined a merge the brief's own words licensed.** `MLPerf Endpoints` and `MLPerf Inference:
  Datacenter` carry word-for-word the same scope sentence — *"INCLUDES that match"*, which the brief
  names as merge evidence — but both framing runs report that as a defect of the MLCommons page.
  Merging two separately published suites on a copy-paste would be a wrong finding, so it did not.
- **Every `Close` rejection names what would be lost and which surviving area still carries the
  ground** — so a reversal does not need the raw files.
- **The `UNIT` records are complete**: eleven fields plus `MODE`, with `COVERS` carrying the source's
  own quoted words rather than a paraphrase.

## 5. The finding the next stage inherits

**The applied vocabulary is almost entirely undecided, and that is a problem for a book called
*Research, Science and Engineering*.** In the run's own words: *"A book on the engineering of AI
that took only this run's `AREA` list would have almost no engineering in it."*

- Of 47 areas, **13 were named by applied sources** — and **12 of those 13 are MLCommons measurement
  suites**. The thirteenth is one retrieval track.
- **No area is named by both families.** Thirty-four are academic-only.
- *Evals*, *Inference*, *Context Engineering*, *Agent Reliability*, *AI Infrastructure*, *SWE
  Agents*, *Posttraining & Midtraining*, *Memory & Continual Learning*, *Local AI*, *GraphRAG*,
  *Computer Use* and *Agentic Engineering* are **undecided, not rejected**.
- **The cause is mechanical, not a failure of either run**: academic sources publish scope
  sentences and practitioner programmes publish bare track names.

**`briefs/area-proposal.md` already requires a disposition line for every `UNCLEAR` before the owner
sees anything.** With 99 of them, that requirement is now the largest single piece of step 4 part 3,
and it cannot be met by rejecting them in a group — the brief forbids a reason shared between
areas.

**And both runs' own gaps survive**, recorded and not filled: no source files AI work by job or
role, and no source carries a named category for *running a trained model as a product under load*.

## 6. What this check did not do

- **It did not read all 223 unit records.** It read the whole coverage section, the whole Rejected
  section, the Level section, both reading policies and a sample of unit records.
- **It verified no quotation** against its framing record, and none against the original source.
- **It did not re-derive the 84 merges** from the two runs; it checked that the stated merges sum to
  the stated total and that the total reconciles.
