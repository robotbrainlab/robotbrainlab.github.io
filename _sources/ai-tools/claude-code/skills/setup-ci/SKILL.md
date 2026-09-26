---
name: setup-ci
description: >-
  Set up a continuous-integration pipeline. Use when the user wants CI — "set up
  CI", "add a GitHub Actions workflow", "set up the pipeline", "add automated
  checks on PRs", "run tests on push". Stands up a pipeline that installs, lints,
  tests, and builds on every push and pull request, as the first automated quality
  gate that keeps broken code out of shared branches.
---

# Set Up CI

CI is the first automated quality gate: every push gets linted and tested, and broken code can't
quietly reach `main`. Without tests, CI is pointless; with tests but no CI, they're run
inconsistently — you want both.

## Workflow

1. **Detect** the CI platform (default to **GitHub Actions** → `.github/workflows/ci.yml`) and the
   project's real commands (install, lint, test, build) — reuse what's in the README/Makefile/scripts.
2. **Write a workflow** that, on **push and pull_request**:
   - checks out the code and sets up the runtime/version,
   - installs dependencies **with caching** (keep it fast — a slow pipeline gets bypassed),
   - runs the **linter**, then the **tests**, then the **build**.
3. **Make failures block merges** — note that the user should enable branch protection requiring the
   check to pass.
4. **Add a status badge** to the README so the build state is visible.

Keep it lean and fast. Matrix builds, multiple OSes, and deploy steps can come later — the first
job is just "lint + test + build, automatically, on every change."
