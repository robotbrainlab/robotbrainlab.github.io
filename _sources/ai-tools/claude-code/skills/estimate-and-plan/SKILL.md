---
name: estimate-and-plan
description: >-
  Break a feature or task into a buildable, sequenced plan. Use whenever the user
  has something to build and wants it decomposed — "break this down", "plan out
  X", "what are the steps", "how should I sequence this", "roughly how big is
  this". Produces an ordered checklist of right-sized tasks with dependencies and
  rough effort, deliberately surfacing the riskiest unknowns first.
---

# Estimate & Plan

Turn a vague ask into an ordered list of small, shippable steps — and tackle the scary unknowns
before the easy parts, so surprises arrive early when they're cheap.

## Workflow

1. **Restate the goal as an outcome** so the plan has a target, not just tasks.
2. **Decompose into small tasks** — each ideally independently testable/shippable. If a task is
   bigger than ~a day of work, split it.
3. **Sequence by dependency**, but pull the **riskiest/most-uncertain** work earlier (a quick
   "spike" to de-risk it) rather than saving it for last.
4. **Rough-size** each task (S / M / L — don't pretend false precision) and flag the ones that are
   really unknowns in disguise.
5. **Call out** what could derail the plan (missing decision, external dependency, unclear
   requirement) so it's visible up front.

## Output

```
## Plan — <feature>
**Outcome:** <what "done" achieves>

1. [ ] <task>  (S)  — <note / why first>
2. [ ] <task>  (M)  — depends on #1
...
**De-risk first:** <the uncertain task to spike before committing>
**Watch out for:** <the thing most likely to blow up the estimate>
```

Honest plans beat optimistic ones. If something is genuinely unknown, say so and propose a spike.
