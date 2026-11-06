# Pass 1 — completeness review

Fill in the placeholders. **Where each comes from, because a brief whose fill-ins are guessed is a
brief that asks a different question each time:**

| Placeholder | Source |
|---|---|
| `<CHAPTER>` | The chapter's path |
| `<SOURCES>` | The record's `sources:` field, verbatim |
| `<NON-SCOPE>` | The record's `non-scope:` field, verbatim |
| `<TAUGHT>` | Every `../LEDGER-TAUGHT.md` row above this chapter, and **every `Do not` row wherever it sits** |
| `<VERIFY>` | **Every claim the chapter's own argument turns on** — its `## Claims` section, plus any figure the chapter computed itself. Not a selection: all of them |
| `<KNOWN-DELIBERATE>` | Anything in the record's `absolutes:` or `coverage-misses:` fields that was triaged and deliberately left, with the reason given there |
| `<VOICE>` | `../GUIDE.md` §4 — the rules and the fourteen habits, pasted in full |

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

**WHAT THE READER ALREADY KNOWS**

These are the rows of the taught-ledger above this chapter, including every `Do not` row. **A
chapter that re-explains one of these, or contradicts one, is a cross-chapter error** — and you
cannot find that without this list. If you think one of these rows is itself wrong, say so under
`Scope doubt`.

`<TAUGHT>`

**THE VOICE THIS CHAPTER MUST BE IN**

`<VOICE>`

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
- **The voice.** `<VOICE>` is the specification. A departure from it is a finding; a preference of
  yours that the specification does not share is not. Quote the rule or habit you are applying.

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

**BUDGET**

One reading of the chapter and one of each source, plus re-reads of specific passages to check a
finding. **No web searches.** Everything you need is in the files named.

**TARGET**

There is no number. A finding exists because something is wrong, not to reach a count.

**PARTIAL**

If you cannot finish, say which parts of the chapter and which sources you covered, and stop. **A
partial review that says what it covered is useful; one that implies full coverage is worse than
none.**

**FORBIDDEN**

- **A finding inside the declared non-scope.** Report it under `Scope doubt` or not at all.
- **A finding you have not located.** Quote the passage and give its position.
- **A rewrite.** You report; you do not edit.
- **A style preference.** Unless it breaks a rule in the chapter's own specification, it is not a
  finding.

**STOPPING RULE**

**One pass through the chapter and its sources, then write up.** That is the fixed point: when you
have read both once and checked each finding you raised, you are done. Do not re-read hunting for
more, and do not pad. **If the chapter is sound, say so in one line** — that is a complete and
useful result.

**IF UNSURE, SAY SO RATHER THAN ASSERTING. A WRONG FINDING COSTS MORE THAN A MISSED ONE.**

**DELEGATION: ZERO.** Do not start any sub-agent.
