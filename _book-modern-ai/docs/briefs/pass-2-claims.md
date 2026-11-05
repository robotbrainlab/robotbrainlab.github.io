# Pass 2 — adversarial claims

Fill in `<CHAPTER>` and `<CLAIMS-FILE>`.

**What this pass is for.** Pass 1 checks the chapter against its sources. This pass checks the
chapter against **what the project has recorded about the strength of those sources.** A claim can
be faithful to its source and still be stated too strongly, and no other pass looks for that.

---

> Copy everything below this line into the agent.

---

**YOUR JOB**

Read `<CHAPTER>` and `<CLAIMS-FILE>`. Find every place the chapter states something more strongly
than the claims file says it may be stated. Be adversarial: your job is to find these, not to
confirm the chapter is fine.

**THE STRENGTH VOCABULARY**, and what each permits the chapter to say:

| Strength | The chapter may say | The chapter may NOT say |
|---|---|---|
| `peer-reviewed` | "X", stating it plainly | — |
| `preprint` | "X, reported in a preprint" / "one group reports X" | "X is established" |
| `vendor` | "its maker reports X" / "X, according to the company that sells it" | "X", unattributed |
| `own-measurement` | "measured here: X", with the method | "X holds generally" |
| `source-absence` | "the source does not state Y" | anything about what Y is |
| `training-data-unverified` | nothing. **A chapter may not rest on one of these** | anything |

**THE STATE VOCABULARY:**

| State | Consequence for the chapter |
|---|---|
| `verified` | May be stated at its recorded strength |
| `contested` | **Must be presented as disputed**, in the `What is disputed` shape — not as settled, and not in a summary as though settled |
| `superseded` | **Must not be stated as current.** If present at all, it is history, dated, and labelled |
| `unverified` | May not be load-bearing |

**CHECK ALL FIVE OF THESE**

1. **Every load-bearing claim in the chapter has a row** in the claims file. One that does not is a
   finding, and it is the most serious kind.
2. **No claim is stated above its recorded strength.** Quote the chapter's wording and the row.
3. **No `contested` claim is presented as settled** — including in the summary, the key-term table
   and the answer key, which are where this hides.
4. **Every size claim says what it is a share of.** A percentage or a ratio with no denominator is
   a finding.
5. **Every benchmark or comparison result says what it was compared against**, and whether the
   comparison was fair. "Better than X" with no statement of how X was configured is a finding.

**OUTPUT**

```
## Overstated
One per finding: the chapter's wording (quoted) · the claim id · its recorded strength ·
what the chapter may say instead.

## Unrecorded
Load-bearing claims in the chapter with no row in the claims file. Quote each.

## Missing denominators
Size claims that do not say what they are a share of.

## Missing baselines
Comparison results that do not say what they beat, or how it was configured.

## Clean
If a section is clean, say so in one line rather than leaving it out.
```

**BUDGET**

One reading of the chapter against the claims file. **No web searches, no fetches** — this pass
compares two files and nothing else. Verifying a claim at its source is the claim verifier's job,
not yours.

**TARGET**

No number.

**PARTIAL**

If you stop early, name the sections you covered.

**FORBIDDEN**

- **Judging whether a claim is true.** You judge only whether the chapter's wording matches the
  strength on record. A true claim stated too strongly is a finding; a false claim stated at its
  recorded strength is not yours.
- **Fetching a source.**
- **Rewriting the chapter.**

**STOPPING RULE**

**One pass through the chapter against the whole claims file, then write up.** Do not re-read
looking for more.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent. Do not search the web — this pass compares two
files and nothing else.
