# Pass 1 — completeness review

Fill in `<CHAPTER>`, `<SOURCES>`, `<NON-SCOPE>`, `<VERIFY>`, `<KNOWN-DELIBERATE>`.

---

> Copy everything below this line into the agent.

---

**YOUR JOB**

Read `<CHAPTER>` and its sources side by side, both in full, and report what is wrong with the
chapter. You are not editing it and not rewriting it. You are finding defects.

**READ BOTH IN FULL.** If you did not read something closely, say which and why, in `Coverage`.

**THE SOURCES**

`<SOURCES>`

**THE SIX FINDING CATEGORIES.** Every finding is exactly one of these. Say which.

| Category | What it means |
|---|---|
| **Omission** | The sources contain something the chapter promised and does not deliver |
| **Alteration** | The chapter states something the sources do not support, or supports differently |
| **False claim** | The chapter states something untrue, whatever the sources say |
| **Self-contradiction** | Two passages in the chapter disagree. **Check the summary, the key-term table and the answer key against the body** — they are read as settled and are where contradictions hide |
| **Out-of-boundary** | The chapter teaches material the mathematics test excludes, without declaring it |
| **Cross-chapter error** | The chapter re-teaches a concept it does not own, uses a term no earlier chapter gave the reader, or contradicts a `Do not` row |

**THIS CHAPTER'S DECLARED NON-SCOPE**

`<NON-SCOPE>`

A finding about something in that list is **out of scope and will be rejected.** Do not report it.
But if you think the non-scope itself is wrong — that the chapter cannot stand without the thing it
excluded — say so once, separately, under `Scope doubt`.

**VERIFY THESE INDEPENDENTLY**, rather than taking the chapter's word:

`<VERIFY>`

**KNOWN AND DELIBERATE.** These are not errors. Do not report them. If you think one is wrong, say
so under `Scope doubt`.

`<KNOWN-DELIBERATE>`

**ALSO CHECK**

- **Every number.** Recompute it against the thing it describes. A chain must hold: a denominator
  must equal the product above it.
- **Every absolute** — *always*, *never*, *every*, *cannot*, *only*. Find a counter-example or say
  none exists.
- **Every claim's strength.** If the chapter states something more strongly than its source does,
  that is an alteration.
- **The capability promise.** The opening says what the reader will be able to do. Can they?
- **Whether the explanation teaches**, which no check can test. Read it once as a reader, with
  nothing else open, and say where you lost the thread.

**OUTPUT**

```
## Findings
One per finding, numbered. Each: category · where (quote the passage) · what is wrong ·
what the sources actually say · how confident you are.

## Scope doubt
Only if you think the non-scope or a deliberate decision is wrong. Otherwise write "none".

## Coverage
What you read in full. What you did not, and why.
```

**STOPPING RULE**

Report every finding you have. Do not pad, and do not hunt for a quota. **If the chapter is sound,
say so in one line** — that is a complete and useful result.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
