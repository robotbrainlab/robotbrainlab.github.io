# The gates

Fourteen checks, run by `bash tools/check-all.sh`, which must end `ALL GATES PASS`. **Fourteen
entries, sixteen scripts** — entry 10 is three generators checked the same way.

**None of this is built yet.** `ROADMAP.md` step 10 builds it, and the present tense below is the
specification each script is written against, not a report that it runs.

**Build order inside step 10.** The record, claims, ownership and expiry gates first, because they
guard the files every later chapter depends on. **Entry 10's three generators last** — a glossary,
a cheat sheet and a changelog built from one chapter's tables return nothing until there are many
chapters to be inconsistent with each other.

**`tools/sweep.py` is not a gate** and is not in this suite. It is the tool `PROCESS.md` §2 requires
a fix round to use, so that the sweep's count is derived rather than typed. It belongs with the
driver, and it is needed before the first fix round rather than at the end of step 10.

**This file is the specification.** `PROCESS.md` §9 lists the gates and points here; it does not
describe them. Each entry below says what the gate reads, what makes it fail, and what it prints.

## Three rules about the gates themselves

1. **A gate nobody reads the output of is worse than no gate**, because it is trusted. When the
   suite fails, find out **which** gate and why — every time.
2. **Prove a gate by breaking something it should catch and watching it exit non-zero.** A gate
   that has never failed has never been tested. Record the proof in the gate's own docstring.
   **Exception: a list-only gate cannot be proved this way.** A list-only gate never exits
   non-zero — it reports and the human triages. **Which gates those are is decided by their own
   entries below, not by a list here**, because a list here would go stale when a gate changed:
   a gate is list-only exactly when its entry says it fails on nothing. **Read the entries; do not
   trust a list here, including this sentence's absence of one.**
   **Prove a list-only gate by planting something it should list and confirming it appears in the
   output**, and record that proof in the gate's docstring. Its failure mode is a list nobody reads,
   so its proof is about the list and not the exit code.
   **Gate 14 is not list-only**: it reports between cycle boundaries and exits non-zero at one, so
   it is proved the ordinary way — plant an expired claim and run it at a boundary.
3. **A gate that checked nothing prints `VACUOUS`, never `CLEAN`.** A chapter with no equations
   gets `VACUOUS` from the arithmetic gate, and that is correct. It does not block the suite and it
   does not satisfy a check — see the exit convention below for exactly what that means.

## Exit convention

| Exit | Means |
|---|---|
| `0` with `CLEAN` | Checked something, found nothing wrong |
| `0` with `VACUOUS` | Had nothing to check. **Does not block the suite, and is reported separately** |
| `1` with `FAIL` | Found something. Prints every instance with file and line |

A gate never prints a summary without the instances. A count with no list cannot be acted on.

**What `ALL GATES PASS` means, exactly.** The suite prints it when **no gate exited non-zero**. It
then prints a `VACUOUS:` line naming every gate that had nothing to read, because a `VACUOUS` is
sometimes correct — a chapter with no arithmetic — and sometimes a symptom that the gate could not
find its input. **Reading that line is part of closing a chapter**, and the record asks for every
`VACUOUS` to be explained.

So: `VACUOUS` does not block the suite and does not satisfy a check. A chapter closes with every
gate either `CLEAN`, or `VACUOUS` with a reason given in the record.

---

## 1 · `tools/verify-voice.py` — the book never refers to its own making

**Reads:** every chapter file.
**Fails on:** any sentence referring to the book's own production, its planning documents, the
research that fed it, a website, a roadmap, a curriculum, a learning path, numbered steps, tracks,
or an agent. Also any first-person reference to the writing process.
**How:** a pattern list, in `tools/voice-patterns.txt`, one regex per line with a comment saying
what defect it was added for. The list is the gate; adding a pattern is how the gate learns.
**Seeded, when the gate is built, from `GUIDE.md` §11's first prohibition and §12's last line** —
the two that concern self-reference, which is all this gate can express as a pattern. Of §11's
other prohibitions, strength, unsourced numbers and superseded claims are gate 12's and pass 2's.
**"Never organises by vendor, product, framework or model name" belongs to no instrument** — see
"What no gate reads" below. Thereafter a
pattern is added only when something gets past the gate, and the comment names what.
**Why it is worded this way:** the book is independent and self-contained, so it has no origins to
disclose — and a chapter that mentions the apparatus breaks the reader's footing. *Prove it* by
inserting "as the research found" into a chapter.

## 2 · `tools/verify-boundary.py` — no mathematics outside the declared line

**Reads:** every chapter, plus `tools/boundary-exemptions.tsv`, whose columns are
`chapter`, `passage` (a quoted span), `reason`, `approved_on`.
**Fails on:** a passage that looks like a derivation and carries neither a justification in the
record nor an exemption row.
**How:** `GUIDE.md` §8 gives a **test**, not a list, so this gate cannot decide on its own and does
not try. It flags every passage that looks like a derivation — display mathematics, "it follows
that", "we can show", a proof environment — and each flagged passage must then carry either a
record entry applying §8's test to it, or a row in the exemptions file giving a reason.
**Honest limitation:** this is a hint gate. It cannot judge whether a derivation earns its place.
It makes the list, and a human triages it one by one.
**Until the mathematics boundary is decided** this gate runs **list-only**: it prints every passage
that looks like a derivation and exits 0, exactly as gates 6 and 7 do. It does not print `VACUOUS`
unless the chapter contains no mathematics at all, and it never blocks the suite. The list is
triaged by hand and the triage recorded.

## 3 · `tools/verify-render.py` — the Markdown renders as written

**Reads:** every chapter.
**Fails on:** a list that will run together into one paragraph; a table row with the wrong number
of cells for its header; an unclosed fence; a heading level skipped; a callout not in the three
permitted forms; **mathematics in `$…$` rather than `\(`/`\[` (`GUIDE.md` §8), which is a pattern
check and belongs here**; and
**in a hand-drawn diagram only**, a line wider than 64 characters or a line of a different width
from its neighbours.
**Not checked:** the width of **captured program output**. `GUIDE.md` §10 applies the 64-character
limit to diagrams the author draws, not to what a program prints — and a captured output block may
never be edited by hand (`LEDGER-DEFECTS.md` entry 6), so failing it would leave no permitted
remedy. A program whose output is too wide is fixed **in the program**, by printing narrower.
**How it tells them apart:** a captured block carries the marker `<!-- captured -->` immediately
before it. Writing that marker by hand on a block a program did not produce is a defect no gate can
catch, and it is `LEDGER-DEFECTS.md`'s own territory.
**Why:** **rendering is not correctness, and no other gate looks at it.** Every other check reads
the Markdown for what it says; none of them asks what the page will show. A list that runs together
into one paragraph, or a table row short of a cell, is still perfectly valid Markdown.

## 4 · `tools/verify-arithmetic.py` — every printed equation holds

**Reads:** every chapter.
**Fails on:** a printed arithmetic statement that does not evaluate. Chains too: a denominator must
equal the product above it, and a total must equal its parts.
**How:** parses display and inline arithmetic, evaluates it, compares to the printed result within
the printed precision.
**`VACUOUS` when:** the chapter contains no arithmetic.
**Why a machine does this:** a writer who has checked the body's numbers reliably forgets the lab's.

## 5 · `tools/verify-record.py` — the record is complete, evidenced, fresh and in order

**Reads:** `records/*.md` and the chapters they name.
**Fails on:** any unticked box; any ticked box with no evidence after it; a missing review verdict;
a `sha256` that does not match the chapter; stages dated out of order; an amendment that is
undated, unreasoned, or earlier than the review it follows.
**Why the hash is last:** editing one character of a closed chapter makes its record stale, so a
published chapter cannot move without leaving a trace. **The honest way to change a closed chapter
is `amend`**, whose refusals are specified in `PROCESS.md` §6.1. What this gate adds is the check
that every amendment is dated, reasoned, and not earlier than the review it follows.
**`VACUOUS` when:** no records exist yet.

## 6 · `tools/verify-coverage.py` — what the plan promised and the chapter lacks

**Reads:** `PLAN.md` and every chapter.
**Fails on:** nothing. **This gate always exits 0 and prints a list**, because the check is a word
match and word matching cannot prove an omission.
**Why it exists:** every other check runs chapter → plan and is **structurally blind to omission**.
This one runs plan → chapter.
**Required of the human:** triage every miss **one by one**, and record each in the record's
`coverage-misses` field. A count is not a triage.

## 7 · `tools/verify-absolutes.py` — list every absolute for testing

**Reads:** every chapter.
**Fails on:** nothing. Prints every *always*, *never*, *every*, *all*, *none*, *cannot*, *only*,
*the most*, *the best*, with its line.
**Why:** no gate can test an absolute. This one forces the list to exist and be counted, so the
record can show it was triaged and what was scoped back.

## 8 · `tools/verify-inputs.py` — no term used before the book gives it

**Reads:** every chapter, in order, and every `Key Terms` table.
**Fails on:** a term used in chapter N whose owning chapter is later than N, or which no chapter
owns.
**How:** builds the given-terms set from the Key Terms tables in reading order, then scans each
chapter for field vocabulary not yet in the set. **It reads prose, not only backticked spans**,
because a term's first appearance is usually a plain word in a sentence. A gate that read only code
font would pass every undefined term that was never typed as code — which is most of them.
**Honest limitation:** the field-vocabulary list is hand-maintained in `tools/field-terms.txt`, and
a term not on it cannot be caught. **It is seeded from the research**: every term appearing in a
`NAME` field of a subject record, plus every term in a `CLAIMS.tsv` claim, goes in when the plan is
approved. That is a real source rather than a guess, and it is why this gate cannot be built before
step 8.

## 9 · `tools/verify-outline.py` — the document outline nests correctly

**Blocked until the build toolchain is decided** (`GUIDE.md` §10, `[OPEN]`). It is the one gate that
reads the output rather than the source, so unlike gate 2 it has nothing to run in list-only mode:
until there is a build, it prints `VACUOUS`.

**Reads:** the built document.
**Fails on:** front matter missing from the outline; a chapter orphaned above its part; a
sub-section nested under the wrong parent; the back matter nested under the last chapter.
**Why:** every other gate reads Markdown. **None of them opens the output.**

## 10 · `tools/glossary.py --check`, `tools/cheatsheet.py --check` and `tools/changelog.py --check` — generated pages are current

**Reads:** every `Key Terms` and `Worth Memorising` table, every chapter record's operation rows, and the three generated pages — the glossary, the cheat sheet and `CHANGELOG.md`.
**Fails on:** any difference between a generated page and what its sources produce.
**Except `CHANGELOG.md`'s `### Boundaries` block**, which is not generated from anything: EXPIRE
appends to it (`CHANGELOG.md`). **`changelog.py` copies that block through unchanged and this gate
skips it** — a generator that rewrote it would delete the only record of where the cycles are.
**Why:** writing a glossary at the end means writing it from memory, and a hand-written changelog
records what the writer remembers changing.

## 11 · `tools/verify-bank.py` — every acceptance question has an owner

**Reads:** `ACCEPTANCE.md` and `records/*.md`.
**Fails on:** a question whose owning chapter is written and whose record does not name it; a record
naming a question that does not exist; a question owned by two chapters; a written chapter with no
question and no deliberate-exemption row; **a question whose `State` is `late:` with no date after
it**, since an undated `late:` cannot be read against the chapter it was added behind.
**See:** `ACCEPTANCE.md` for what a question is and how one is answered.

## 12 · `tools/verify-claims.py` — no claim stated above its evidence

**Reads:** `CLAIMS.tsv`, every chapter, and each chapter's `## Claims` section.
**Fails on:**
- a chapter's `## Claims` section naming an id not in `CLAIMS.tsv`;
- a `CLAIMS.tsv` row whose `dependents` names a chapter that does not list it;
- a row with a `maturity` set and no `maturity_basis`;
- a row with `state = contested` whose chapter does not carry a `## What is disputed` section;
- a row with `state = superseded` cited by a chapter as current;
- a row with `source_strength = training-data-unverified` listed as load-bearing by any chapter.

**What it cannot check:** whether the chapter's *wording* overstates the claim. That is judgement,
and it is pass 2's job (`briefs/pass-2-claims.md`). This gate checks the bookkeeping; the pass reads
the prose.

## 13 · `tools/verify-ownership.py` — one concept, one owner

**Reads:** `OWNERSHIP.tsv` and every chapter's `Key Terms` table.
**Fails on:** two chapters claiming one concept; a chapter with a `Key Terms` row for a concept
another chapter owns; an `OWNERSHIP.tsv` row naming a chapter that does not exist; a row whose
ownership has moved with no `moved_on` date.
**Prints as a warning, not a failure:** any concept whose ownership has moved twice. That is a
signal the carving is wrong, and it belongs in the cycle's operation counts.

## 14 · `tools/verify-expiry.py` — what has gone stale

**Reads:** `CLAIMS.tsv`, **and `CHANGELOG.md` for the last `cycle-boundary` line** — nothing else
defines where a cycle begins, and this gate behaves differently at a boundary.
**Fails on:** nothing when run during a cycle. **Exits 1 only when run with `--at-boundary`**, and
then on any claim past its `review_by` that has not been re-verified. **The flag is the mode, not
the file** — EXPIRE passes it, because the boundary is the stage running and no line in
`CHANGELOG.md` can say "a boundary is happening now". The lines record boundaries already past, and
the gate reads the last one to date its report.
**With no boundary line at all**, as in the first cycle, every claim is treated as due: nothing has
been re-verified yet, which is exactly what EXPIRE must act on.
**Prints always:** every claim within thirty days of expiry, so a cycle can be planned. **Thirty
days is an operational choice**, not a derived figure — long enough to schedule a cycle, short
enough that the list stays readable.
**Why it is not a per-chapter gate:** staleness is a property of time, not of the chapter being
written. Failing a chapter because an unrelated claim expired would make the suite untrustworthy,
which is rule 1.

---

## What no gate reads

**Every rule below is stated somewhere in these documents and sampled by nothing** — no gate, no
review pass, no record checkbox. They are listed here because a rule whose enforcement is assumed
is worse than one known to rest on care: the first is believed, the second is watched.

| Rule | Owner | Why no instrument |
|---|---|---|
| Never organises by vendor, product, framework or model name | `GUIDE.md` §11 | A chapter's organising principle is not a string. It needs a reader asking "what is this chapter arranged around?" |
| Do not report progress as a fraction of a total | `GUIDE.md` §9 | A judgement about framing, not a pattern |
| Scan for secrets before every commit; push only to the named remote | `../CLAUDE.md` | Not a property of the book. It belongs to whoever runs `git`, and nothing a chapter check reads can see it |
| A claim a chapter rests on may not stay `provisional` | `CLAIMS.tsv` | **Discharged by procedure at CONFIRM** (`PROCESS.md` §5), not by a check. Gate 12 fails on a maturity with no basis, which is a different thing |

**All four need a reader, which is why they are listed rather than built.** Two others that were on
this list have been closed instead: the mathematics delimiters are now gate 3's, and `late:` is now
gate 11's once the row carries a date.

---

## Setting a review date

**`tools/verify-expiry.py` needs a policy, and this is it.**

**These intervals are a starting policy, not a measurement.** Nobody has measured how fast a
convention turns over, and the numbers below are chosen to be defensible and adjustable rather than
derived. **The cycle that uses them reports how many claims it re-checked and how many had actually
changed** — and that is the evidence to tune them with. If almost nothing had changed, the interval
is too short; if most things had, it is too long.

`review_by` is set when the row is written, from `class`:

| `class` | `review_by` | Why |
|---|---|---|
| `durable` | **+24 months** | Expected to hold for five years. Checking yearly spends the cycle on things that will not have moved |
| `convention` | **+12 months** | How it is done now. Practice turns over on roughly this scale |
| `volatile` | **+3 months** | Settings, versions, prices, model names, benchmark figures — the things a vendor or a leaderboard can change without notice |

**Two overrides, both shortening:**

- A claim with `maturity` of `single-source` or `unexamined` gets **+6 months regardless of class**.
  It has not been independently confirmed, so its durability is unknown whatever its subject.
- A **load-bearing** claim (`GOAL.md` §3.4 defines the term) gets the **shorter of its class date
  and 12 months**. If removing the claim would change what the chapter teaches, it is checked more
  often.

**Nothing lengthens a review date.** A date is shortened by evidence of fragility and never
extended by confidence.

**One asymmetry worth knowing, because it is the real shape of the cycle-three risk.** The claims
file makes **finding** what must change proportional to what changed. It does not make **applying**
it so. A superseded claim with five dependents reopens five chapters, and each reopened chapter pays
a sweep across the whole book — `PROCESS.md` §2's figure is that one claim lives in about six places,
four of them prose. **So re-verification scales with change and correction scales with the book.**
`PROCESS.md` §5.2's "the work is proportional to what changed, not to how big the book is" is true of
the first half only. Nothing fixes this; `tools/sweep.py` only makes the cost visible and honest.

**One interaction worth knowing.** A `volatile` claim comes due every three months, and a cycle runs
on roughly twelve weeks — so nearly every volatile claim is due at nearly every cycle. **That is
intended.** Nobody owns a version number or a price, so neither can be assumed to hold; a cycle
that did not re-check them would publish figures it had no reason to believe. The cost is bounded
because re-checking one is a single fetch.
