---
name: increase-coverage
description: >-
  Find and close the most important gaps in a project's test coverage. Use when the
  user wants better coverage — "increase test coverage", "what isn't tested", "add
  tests for the gaps", "improve our coverage". Prioritizes by risk, not percentage:
  finds the untested critical and error-prone paths, adds tests there first, and
  reports what's still uncovered and whether it's worth covering.
---

# Increase Coverage

Coverage percentage is a vanity metric; covering the paths that would *hurt if they broke* is the
goal. A repo at 95% can still have its riskiest logic untested.

## Workflow

1. **Get the lay of the land.** Run the project's coverage tool if it has one — but use it to find
   gaps, not as the target.
2. **Rank the gaps by risk, not size:** untested business logic, complex branching, error/edge
   handling, money/data-mutating paths, and anything previously buggy come first. A trivial getter
   left untested is fine.
3. **Add focused tests** for the high-risk gaps, in the repo's style, covering happy + edge + error
   cases (see the `write-tests` approach).
4. **Report honestly:** what you added, and what's still uncovered — with a one-line judgment on
   whether each remaining gap is worth closing or is acceptably low-risk.

Don't chase the last few percent of coverage on trivial code. Spend the effort where a failure
would actually cost something.
