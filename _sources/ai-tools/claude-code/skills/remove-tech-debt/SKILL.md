---
name: remove-tech-debt
description: >-
  Find, prioritize, and safely clean up technical debt and dead code. Use when the
  user wants to reduce cruft — "remove dead code", "clean up this codebase", "find
  the tech debt", "what should we clean up", "reduce the cruft". Identifies dead
  code, unused dependencies, duplication, and deprecated paths, prioritizes by how
  much they slow change, and removes them under tests without altering behavior.
---

# Remove Tech Debt

Untracked debt compounds silently. The goal is to find it, decide what's actually worth paying down,
and clean it up *without changing behavior* — so the cleanup is safe and reviewable.

## Workflow

1. **Find it:**
   - **Dead code** — commented-out blocks, unreachable branches, unused functions/files.
   - **Unused dependencies / imports** (and the security surface they carry).
   - **Duplicated knowledge** — the same logic in several places.
   - **Deprecated paths**, stale `TODO`/`FIXME`, and modules that are clearly too complex.
2. **Prioritize** by impact, not tidiness. The useful lens is the **debt quadrant** (deliberate vs
   inadvertent × prudent vs reckless) and a simple question: *how much is this slowing down change?*
   Debt in code nobody touches matters less than debt in the hot path.
3. **Clean up safely** — under tests, preserving behavior:
   - Delete dead code aggressively (version control remembers it).
   - Deduplicate by extracting the shared logic.
   - Remove unused deps and confirm the build/tests still pass.
4. **Separate cleanup from features.** Don't change behavior while cleaning — a pure refactor is
   easy to review and trust; a mixed one isn't.
5. **Report** what you removed, and flag anything that needs a bigger, deliberate refactor later.
