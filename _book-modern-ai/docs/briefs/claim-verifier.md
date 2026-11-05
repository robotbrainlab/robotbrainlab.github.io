# Claim verifier

Fill in `<CLAIM-ROW>`. One claim per run.

**When this runs.** At the expire stage, for every claim past its review date. Also any time a
claim is challenged, by a reviewer or by the owner.

**Why one claim per agent.** A single claim can be checked against its source exhaustively in a few
fetches. An agent given twenty claims checks each one shallowly and reports confidence it has not
earned.

---

> Copy everything below this line into the agent.

---

**YOUR JOB**

Here is one recorded claim. Go to its source and establish whether it still holds, whether it is
disputed, and whether the strength it is recorded at is right.

**THE CLAIM**

`<CLAIM-ROW>`

**WHAT TO DO**

1. **Fetch the source.** Not a search summary of it — the page itself. A snippet tells you
   something was said; it does not tell you what the source says now. A source can be revised,
   corrected, retracted or withdrawn after it is cited.
2. **Check the claim against the source's own words.** Quote the span that supports it, or the span
   that does not.
3. **Check whether the source has changed.** A new version, an erratum, a retraction notice, a
   withdrawal. **Say the version and date you read.**
4. **Look for a direct rebuttal.** Has anyone published a result that contradicts this? A claim
   with a published rebuttal is `contested`, whatever its original source says.
5. **Establish its maturity, which is the expensive half of this job and the reason this pass
   exists.** `strength` asks how good the evidence is; `maturity` asks whether the science is
   settled. They are independent. Look for these, in this order:

   | Look for | How |
   |---|---|
   | **Independent replication** | Has a group other than the originators obtained it? |
   | **Used as a premise** | Find two or three works citing it. Do they say *"since X, we…"* and build on it, or are they still arguing *for* X? **A field that has stopped re-arguing a claim has accepted it** — this is the strongest signal and the one nothing else substitutes for |
   | **A failed refutation** | A published attempt to break it that did not succeed. Stronger than no attempt at all |
   | **Age plus continued use** | Old and still used is established. Old and abandoned is superseded. New and popular is convention, not established |
   | **Several communities** | Does more than one field rest on it? |

   And two that mean **not** established: the reported number **drifts** between sources, or the
   largest version is the **originating group's** while independent reports are smaller. In the
   second case, record the smaller version as the claim.
6. **Judge the recorded strength.** A paper whose authors sell the thing it measures is `vendor`,
   not `preprint`, however it is published.

**OUTPUT**

```
## Verdict
One of: verified · contested · superseded · cannot-reach.
If cannot-reach, this claim's state stays as it was and the row records the attempt.

## Evidence
The quoted span from the source that supports or refutes the claim.
The version and date of what you read.

## Strength
The strength it should be recorded at, and why — especially if it differs
from the recorded one.

## Rebuttal
Any published result contradicting it, with its source. "None found" if none.

## Maturity
One of: established · converging · contested · single-source · unexamined.
Then the basis, in the exact vocabulary of CLAIMS.tsv — which signal you found,
and where. A maturity with no basis will be rejected.

## Scope consequence
One line. The book is about what is MOVING in a subject, not about its settled
foundations. So: does this claim belong in the book as subject matter, or as
support for something that is moving? Say which.

## Rewording
If the claim is true but recorded too strongly or too loosely, write the
wording it should have.
```

**IF YOU CANNOT REACH THE SOURCE**, say so and return `cannot-reach`. **Do not substitute another
source, and do not fall back on what you already know** — an unreachable source is a finding, and
guessing hides it.

**BUDGET**

10 fetches, 4 searches. The maturity check is what most of that is for: finding works that cite
this claim and reading **how** they cite it.

**TARGET**

One claim. One verdict, one maturity, one basis.

**PARTIAL**

If the budget runs out before the maturity is established, return the verdict with
`maturity: provisional` and say what you did not get to. **A provisional maturity is an honest
result; an asserted one is not.**

**FORBIDDEN**

- **Substituting another source** when the named one cannot be reached. Return `cannot-reach`.
- **Falling back on what you already know.** An unreachable source is a finding; guessing hides it.
- **Setting a maturity with no basis.** It will be rejected.
- **Checking more than the one claim you were given.**

**STOPPING RULE**

Stop when the claim has a verdict and a maturity with its basis, or when the budget is spent. Do
not verify a second claim.

**DELEGATION: ZERO.** Do not start any sub-agent.
