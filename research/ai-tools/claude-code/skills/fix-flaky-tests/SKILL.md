---
name: fix-flaky-tests
description: >-
  Diagnose and fix a flaky test — one that passes sometimes and fails sometimes.
  Use when the user reports intermittent test failures — "fix this flaky test",
  "tests fail randomly in CI", "this passes locally but fails sometimes", "the
  suite is intermittent". Finds the source of nondeterminism and fixes the root
  cause, rather than retrying or disabling the test (which hides the real bug).
---

# Fix Flaky Tests

A flaky test is a real signal — it means something is nondeterministic, often in the *code*, not
just the test. Retrying or `@skip`-ing it buries the warning. Find the cause.

## Workflow

1. **Reproduce.** Run the test many times, both in isolation and as part of the full suite. Whether
   it fails alone or only in the suite is the biggest clue.
2. **Classify the nondeterminism:**
   - **Order dependence** — passes alone, fails in suite → shared/global state leaking between
     tests. Fix: isolate state, reset between tests, remove the shared mutable.
   - **Timing / async** — `sleep`-based waits, real clocks, unawaited promises, races. Fix: control
     the clock, await properly, wait on conditions not durations.
   - **External dependencies** — real network/time/randomness. Fix: mock them; seed randomness;
     inject the clock.
   - **Resource issues** — leaked connections, ports, files. Fix: clean up in teardown.
3. **Fix the root cause**, then re-run many times to confirm it's actually stable.

## Anti-fix

Adding a retry or a longer sleep, or disabling the test, is not a fix — it hides a real
nondeterminism bug that will resurface (often in production, not just CI).
