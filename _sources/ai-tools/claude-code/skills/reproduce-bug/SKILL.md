---
name: reproduce-bug
description: >-
  Build a reliable reproduction of a reported bug, especially a production-only
  one. Use when the user needs to recreate an issue — "reproduce this bug", "I
  can't reproduce X locally", "recreate this from the report", "make a failing test
  for this". Identifies what differs between the failing environment and yours,
  reproduces the failure locally, reduces it to the smallest failing case, and
  captures it as a failing test so the fix is verifiable and stays fixed.
---

# Reproduce Bug

A bug you can't reproduce, you can't confidently fix — you can only guess. The job is to turn a
fuzzy report into a deterministic, minimal failing case.

## Workflow

1. **Extract the facts** from the report: the exact symptom, the inputs, the environment, the steps,
   and (crucially) what was *expected* vs what happened.
2. **Find what's different** between the failing context and a working one — the usual suspects:
   data shape, configuration, a version mismatch, concurrency/timing, scale, or specific user state.
   Production-only bugs almost always live in one of these gaps.
3. **Reproduce locally** by recreating those conditions — the same data shape, env vars, dependency
   versions, and (if it's a race) the concurrency.
4. **Reduce** to the smallest input/steps that still trigger it — that's where the cause becomes obvious.
5. **Capture it as a failing test.** Now the fix has a target, and a regression guard so the bug
   can't quietly come back.

Only once it reproduces reliably should you fix it — then the same test going green proves the fix.
