---
name: migrate
description: >-
  Execute a migration safely — a framework/library version jump, a library swap, or
  a schema/data change. Use when the user is changing a foundation — "migrate from
  X to Y", "upgrade the framework", "switch from <lib> to <lib>", "migrate the
  database", "move to <new thing> without downtime". Performs the change using
  expand/contract and incremental steps so the system keeps working at every point,
  avoiding a big-bang rewrite.
---

# Migrate

The danger in any migration is the big-bang switch where everything changes at once and nothing
works until it's all done. The antidote is to make the change in small, independently-verifiable
steps that keep the system working throughout.

## By kind of migration

**Code (framework/library version):**
- Understand the breaking differences (read the migration guide).
- Migrate **incrementally** — module by module where possible — keeping tests green at each step.
- Use codemods / mechanical find-replace for the rote changes; review the rest by hand.

**Library swap (replace one dependency with another):**
- Introduce a thin **abstraction/interface** over the old library.
- Move call sites behind it, then swap the implementation, then remove the old one.

**Schema / data (the riskiest):**
- Use **expand/contract** for zero downtime: *expand* (add the new column/table, write to both) →
  *backfill* existing rows → *switch reads* to the new shape → *contract* (stop writing, drop the
  old). Each step is independently deployable; at no point is the running app out of sync.
- Migrations are **versioned scripts** in the repo, applied in order. Never hand-edit prod.

## Principle

At every step the system should still work and the tests should still pass. If a step can't be made
safe and reversible, break it into smaller steps until it can.
