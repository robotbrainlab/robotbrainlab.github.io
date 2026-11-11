---
name: write-tests
description: >-
  Write good tests for code, in the project's own test framework. Use whenever the
  user wants tests — "write tests for X", "add unit tests", "test this
  function/module", "cover this with tests" — or right after implementing
  something that ought to be tested. Generates happy-path, edge-case, and (where it
  matters) integration tests that follow the test pyramid and test behavior, not
  implementation — not just the happy path.
---

# Write Tests

Tests are what make code actually work and stay working. Good tests catch regressions, document
intent, and push toward cleaner design — bad tests (happy-path only, testing implementation
details) give false confidence.

## Workflow

1. **Match the repo.** Detect the test framework, directory, naming, and helpers already in use
   and mirror them exactly. Don't introduce a new framework.
2. **Decide what's worth testing** — critical paths, anything with branching/edge logic, and
   anything that has broken before. Aim for meaningful coverage of behavior, not 100%.
3. **Cover the cases that actually fail:**
   - Happy path.
   - **Edge cases** — empty/null, boundaries (0, 1, max), wrong types, duplicates, large input.
   - **Error paths** — invalid input, the dependency failing.
4. **Test behavior, not internals.** Assert on outputs and observable effects, not on private calls,
   so the tests survive refactors.
5. **Use test doubles wisely** — fake/stub the *collaborators you own* (DB, clock); do **not** mock
   third-party libraries you don't own (you'll test your mock, not reality). Add an integration test
   for real seams (code ↔ DB).
6. **Run them** and confirm they pass (and that they'd fail if the behavior broke).

## Test pyramid

Many fast **unit** tests, fewer **integration** tests, very few slow **end-to-end** tests. Inverting
this gives a slow, flaky suite people skip. Keep most tests at the bottom.
