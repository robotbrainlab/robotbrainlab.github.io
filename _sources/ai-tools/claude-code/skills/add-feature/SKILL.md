---
name: add-feature
description: >-
  Implement a new feature end-to-end in an existing codebase, following the
  project's own conventions. Use whenever the user asks to add/implement/build a
  feature, endpoint, flow, or capability in a repo that already exists — "add X",
  "implement the Y endpoint", "build the Z flow". It works across the project's
  layers (transport → logic → data → tests) and mirrors existing patterns instead
  of introducing a new style.
---

# Add Feature

The goal is a feature that looks like the rest of the codebase wrote it — same structure, naming,
error handling, and testing — so it's reviewable and maintainable, not a foreign object.

## Workflow

1. **Find the nearest existing example.** Locate a similar feature already in the repo and study
   how it's structured: where files live, naming, how layers connect, how errors are handled, how
   it's tested, how it's wired/registered. **Match this**, don't invent.
2. **Plan the change across the layers** the project uses (e.g. route/handler → service/logic →
   data access → model), and the tests for each.
3. **Implement**, following the established conventions exactly. Validate input at the boundary;
   handle expected errors with clear responses; let unexpected ones propagate.
4. **Add tests** mirroring how the repo tests similar code (happy path + the obvious edge cases).
5. **Update** anything the repo keeps current — README, API docs, changelog — if applicable.
6. **Verify** it actually runs / the tests pass before declaring done.

## Principle

When in doubt, copy the local convention over the "better" idea. Consistency is worth more than
your preferred pattern here — a feature that matches the codebase is easier to review, trust, and
maintain than a cleverer one that doesn't.
