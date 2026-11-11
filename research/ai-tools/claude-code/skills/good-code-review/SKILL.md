---
name: good-code-review
description: >-
  Review code for craft and maintainability — readability, naming, function and
  module design, error handling, code smells, and refactoring opportunities. Use
  this skill whenever the user asks to "review this code", "is this good code?",
  "make this cleaner", "is this well written?", wants feedback on a function,
  module, file, diff, or PR, or has just finished writing something and wants it
  critiqued for quality (not just correctness). Prefer this over a generic glance
  whenever the goal is code *quality* rather than finding bugs. Reviews against
  first-principles craft and gives concrete, prioritized suggestions with
  before/after examples.
---

# Good-Code Review

Review code the way a thoughtful senior engineer would: not for whether it *works*
(that's the floor), but for whether it's **good** — easy to read, understand, and
change safely six months from now. The enemy is always **complexity**: anything
about the structure that makes the code hard to understand or modify.

## How to run a review

1. **Identify the target.** If the user named a file/function, review that. If they
   said "my changes" or referenced a PR, run `git diff` (or `git diff main...HEAD`)
   and review the diff. If ambiguous, ask briefly.
2. **Read it as a stranger would.** For each unit, ask: how much do I have to hold
   in my head to change this safely (*cognitive load*)? How many places would one
   logical change touch (*change amplification*)? High answers = the real problems.
3. **Walk the checklist below**, but report findings by **impact, not by line order**.
4. **Output prioritized findings** (see format). Be honest and specific; do not
   manufacture nitpicks to fill a list. If the code is genuinely good, say so and
   point out only what would matter.

## The craft checklist

Review against these. Each is a tactic against complexity — cite the principle, not
just taste.

**Naming**
- Names reveal intent (`invoiceDueDateUtc`, not `d`); no noise words (`data`, `tmp`,
  `manager`, `helper`). A name you can't find usually means the thing does too much.

**Functions**
- Small, one thing, one level of abstraction. If you need "and" to describe it, split it.
- Few parameters; suspicious of boolean flag params (usually two functions in a trench coat).
- **Command/Query Separation**: a function either *does* something (side effect, returns
  nothing meaningful) or *answers* something (pure, returns a value) — not both.
- Side effects are obvious from the name/signature, not hidden.

**Modules & design**
- **Information hiding**: small interface, hidden implementation. Expose little, hide much.
- **Deep vs shallow**: prefer modules whose simple interface hides substantial work over
  thin wrappers whose interface is as complex as their body.
- **High cohesion, low coupling**: each unit one job; units touch through narrow interfaces.
- **Separation of concerns**: business logic, data access, transport in distinct layers.
  A handler that also queries the DB *and* sends email is a maintenance trap.
- **No premature complexity**: flag speculative abstraction/patterns added before needed.

**Error handling**
- Expected outcomes (bad input, missing record) → explicit returns; genuine surprises →
  exceptions that propagate to a boundary that can act.
- **Never swallow silently** (`except: pass`, empty catch). Catch narrowly or not at all.

**Comments**
- Comments explain *why* (the non-obvious trade-off/constraint), never restate *what*.
  Flag comments that have drifted out of sync with the code — they actively mislead.

**Code smells** (name them when you see them)
- Long method, large class / god object, long parameter list, primitive obsession,
  feature envy, shotgun surgery, duplicated knowledge, dead/commented-out code.

**Refactoring**
- Where the structure fights the reader, suggest the small, behavior-preserving step that
  fixes it — not a rewrite.

## Output format

```
## Code review — <target>

**Overall:** <1–2 honest sentences: is this good code? what's the headline?>

### High impact
1. **<principle>** — <what & where>. <why it matters>.
   ```<lang>
   // before
   ...
   // after
   ...
   ```

### Worth fixing
- **<principle>** — <concise finding + suggestion>

### Minor / optional
- <small things, grouped>

**What's already good:** <call out real strengths, briefly>
```

Lead with the one or two changes that most reduce complexity. A review that lists
twenty equal-weight nitpicks is less useful than one that says "these two things
matter, the rest is fine."
