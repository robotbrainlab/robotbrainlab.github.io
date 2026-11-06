# Claim verifier

Fill in `<CLAIM-ROW>`. One claim per run.

**When this runs — three occasions, and the first is the one easily forgotten.**

1. **At CONFIRM**, between research and selection, on every claim whose basis is `provisional` and
   which a candidate chapter would rest on. `../CLAIMS.tsv` forbids a chapter resting on an
   unestablished maturity, and this is where that is discharged.
2. **At EXPIRE**, on every claim past its review date.
3. **Whenever a claim is challenged** — by a review pass, or by the owner.

**Why one claim per agent.** One claim can be checked exhaustively in a few fetches. An agent given
twenty checks each shallowly and reports confidence it has not earned.

---

> Copy everything below this line into the agent.

---

**QUESTION**

Does this claim still hold, at the strength it is recorded at — and is the science behind it
settled?

**THE CLAIM**

`<CLAIM-ROW>`

**WHAT TO DO**

1. **Fetch the source.** Not a search summary of it — the page itself. A snippet tells you something
   was said; it does not tell you what the source says **now**. A source can be revised, corrected,
   retracted or withdrawn after it is cited.
2. **Check the claim against the source's own words.** Quote the span that supports it, or the span
   that does not.
3. **Check whether the source has changed.** A new version, an erratum, a retraction notice, a
   withdrawal. **Say the version and the date of what you read.**
4. **Look for a direct rebuttal.** Has anyone published a result contradicting this? **A published
   rebuttal sets `maturity = disputed`** — that is what the value means, whatever the original source
   says. **It does not by itself set `state`.** `state` is your own verdict after reading both sides:
   `contested` if the rebuttal leaves the claim doubtful at its recorded strength, `verified` if the
   claim still holds despite the rebuttal existing. **`maturity = disputed` with `state = verified`
   is a real and expected row** — the dispute is real and you confirmed the claim survives it.
   See `../CLAIMS.tsv`.
5. **Judge the recorded strength.** A paper whose authors sell the thing it measures is `vendor`,
   not `preprint`, however it is published.
6. **Establish its maturity. This is the expensive half of the job and the reason this pass
   exists.** `strength` asks how good the evidence is; `maturity` asks whether the science is
   settled. They are independent — a refereed paper can be the only source for a claim, and a
   preprint can restate something long established.

**The maturity signals, strongest first:**

| Signal | How to look | Why it ranks here |
|---|---|---|
| **Used as a premise** | Find two or three works citing it. Do they say *"since X, we…"* and build on it, or are they still arguing *for* X? | **A field that has stopped re-arguing a claim has accepted it.** Nothing else substitutes for this |
| **Independent replication** | Has a group other than the originators obtained it? | Directly searchable, and it is what "established" rests on |
| **A failed refutation** | A published attempt to break it that did not succeed | Stronger than no attempt at all: a claim nobody tried to break is unexamined, not established |
| **Several communities** | Does more than one field rest on it? | A result known inside one subfield is established only there |
| **Age plus continued use** | Old and still used is established. Old and abandoned is superseded. New and popular is convention, not established | Age alone means nothing; the combination does |

**And two signals that mean *not* established:** the reported number **drifts** between sources, or
the largest version of the claim is the **originating group's** while independent reports are
smaller. In the second case, **record the smaller version as the claim**.

**OUTPUT**

```
## Verdict
One of: verified · contested · superseded · cannot-reach.
The first three are states the row can hold. cannot-reach is NOT a state: it
reports this run, and the row's state stays as it was.

## Evidence
The quoted span from the source that supports or refutes the claim, with the
version and date of what you read.

## Strength
The strength it should be recorded at, and why — especially if it differs from
the recorded one.

## Rebuttal
Any published result contradicting it, with its source. "None found" if none.

## Maturity
One of: established · converging · disputed · single-source · unexamined.
Then the basis, in CLAIMS.tsv's exact vocabulary: which signal you found, and
where. A maturity with no basis will be rejected.

If you could not establish it within budget: write "not established in this
run", leave the recorded maturity as it was, set the basis to `provisional`,
and say which signal you were pursuing. Do NOT write `provisional` as the
maturity — it is a basis value, not a maturity value.

## Scope consequence
The boundary, quoted from GUIDE.md section 3: "The book is about what is
currently moving in a subject. It is not about the subject's settled
foundations." So answer, in one word plus one line of reason:

  SUBJECT  — the answer is still moving, so this belongs as the book's subject
  SUPPORT  — settled, and a moving subject is unintelligible without it
  NEITHER  — settled, and nothing moving depends on it

This feeds the subject's verdict at SELECT (PLAN.md's Verdict column): a
subject whose claims are all SUPPORT is FOUNDATIONS-ONLY, and one whose claims
are all NEITHER is a REJECT. Say which you are contributing to.

## Rewording
If the claim is true but recorded too strongly or too loosely, write the
wording it should have.

## Coverage
Fetches and searches used. What you could not reach.
```

**BUDGET**

10 fetches, 4 searches. Most of it is for the maturity check: finding works that cite this claim
and reading **how** they cite it.

**TARGET**

One claim. One verdict, one maturity with its basis, one scope consequence.

**PARTIAL**

If the budget runs out before the maturity is established, return the verdict and follow the
`Maturity` instruction above. **An honestly unestablished maturity is a result; an asserted one is
not.**

**FORBIDDEN**

- **Substituting another source** when the named one cannot be reached. Return `cannot-reach`.
- **Falling back on what you already know.** An unreachable source is a finding; guessing hides it.
- **Setting a maturity with no basis**, or writing `provisional` as a maturity.
- **Checking more than the one claim you were given.**

**STOPPING RULE**

Stop when the claim has a verdict, a maturity with its basis or an honest statement that it is
unestablished, and a scope consequence — or when the budget is spent. Do not verify a second claim.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
