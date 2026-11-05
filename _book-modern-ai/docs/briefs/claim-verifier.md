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
4. **Look for a direct rebuttal.** One search is enough: has anyone published a result that
   contradicts this? A claim with a published rebuttal is `contested`, whatever its original source
   says.
5. **Judge the recorded strength.** A paper whose authors sell the thing it measures is `vendor`,
   not `preprint`, however it is published.

**OUTPUT**

```
## Verdict
One of: verified · contested · superseded · cannot-reach.

## Evidence
The quoted span from the source that supports or refutes the claim.
The version and date of what you read.

## Strength
The strength it should be recorded at, and why — especially if it differs
from the recorded one.

## Rebuttal
Any published result contradicting it, with its source. "None found" if none.

## Rewording
If the claim is true but recorded too strongly or too loosely, write the
wording it should have.
```

**IF YOU CANNOT REACH THE SOURCE**, say so and return `cannot-reach`. **Do not substitute another
source, and do not fall back on what you already know** — an unreachable source is a finding, and
guessing hides it.

**BUDGET**: 5 fetches, 2 searches.

**DELEGATION: ZERO.** Do not start any sub-agent.
