---
name: design-doc
description: >-
  Write a focused design doc or RFC for one specific feature or change before
  implementing it. Use whenever the user says "write a design doc for X", "how
  should we approach Y", "draft an RFC", or wants the approach thought through and
  written down before coding a non-trivial change. Produces a crisp one-feature
  design: the problem, the proposed approach, the alternatives considered and why
  they lost, the trade-offs, and a rollout/testing plan.
---

# Design Doc

A design doc forces the thinking before the typing, and gives reviewers something to react to
that is cheaper to change than code.

## Workflow

1. **Read the relevant code and context** so the doc is grounded in how things actually work.
2. **Write it to this structure** (drop sections that don't apply; keep it short):

```markdown
# Design: <feature/change>

## Problem & context
<what we're solving and why now; the current behavior>

## Goals / Non-goals
- Goals: <what this must achieve, observably>
- Non-goals: <explicitly out of scope>

## Proposed approach
<the design, with a sketch/diagram if it helps; how data and control flow>

## Alternatives considered
- <option> — rejected because <reason>   (← the most valuable section; don't skip it)

## Risks & trade-offs
<what we're accepting; what could go wrong>

## Rollout & testing
<how it ships safely (flags, migration, phases) and how it's tested>

## Open questions
> [DECIDE: ...]
```

3. **Pre-fill from the code**; mark genuine unknowns as `> [DECIDE: ...]` rather than guessing.

Keep it to a page or two. A design doc that's read beats a thorough one that isn't.
