---
name: project-planning-docs
description: >-
  Generate the documentation a well-run project keeps. Use this skill whenever the
  user is planning a new project or feature, wants to document a project's design or
  decisions, or asks for a problem statement, goals/scope doc, architecture or design
  doc, ADR (architecture decision record), developer guide, operational guide /
  runbook, or changelog. Triggers on "let's plan this", "write a design doc",
  "document the architecture", "what docs should this project have", "create an ADR
  for X", "write a problem statement", or kicking off a project before code. It
  produces the right document(s) from proven templates, pre-filled from the codebase
  and conversation, with the spots that need a human decision clearly marked.
---

# Project Planning Docs

Produce the documents a well-run project keeps — the written record of *what* you're building,
*why*, how it's *shaped*, how to *operate* it, and how it *changes*. Good docs are deliverables,
not afterthoughts: a system no one can explain is a system no one can safely change.

The documents split into two kinds, and the distinction matters:
- **Design-time** (write before / early in coding): Problem Statement, Architecture & Design, ADRs.
- **Living** (created and maintained as the system grows): Developer Guide, Operational Guide,
  Changelog.

## Workflow

1. **Decide what's needed.** If the user named a doc (e.g. "write an ADR for choosing Postgres"),
   produce that one. If they're "planning a project", offer the full set and produce the design-time
   docs first. Don't dump six empty templates when they asked for one.
2. **Gather context cheaply.** Read what already exists — the repo, README, existing docs, and the
   conversation — and infer as much as you legitimately can. Don't interrogate the user for things
   you can find or reasonably draft.
3. **Read `references/templates.md`** and instantiate the relevant template(s).
4. **Pre-fill, then mark the gaps.** Fill every section you can from real context. Where a genuine
   human decision or unknown remains, insert a clearly visible `> [DECIDE: <the open question>]`
   placeholder rather than inventing an answer. The value is in a *mostly-done* doc with the open
   questions surfaced — not a blank form, and not confident fiction.
5. **Place the files** under `docs/` (ADRs under `docs/adr/NNNN-title.md`, numbered sequentially),
   unless the user says otherwise. Tell them which are design-time (do now) vs living (maintain).

## What goes in each document (summary — full templates in the reference)

- **Problem Statement & Goals** — background/context, the core problem (stated as a problem, not a
  solution), goals with *observable* success criteria, explicit out-of-scope, stakeholders,
  constraints vs assumptions.
- **Architecture & Design** — system overview, a diagram (ASCII is fine), component breakdown
  (one responsibility each), data flow, external integrations & contracts, data storage & schema,
  key decisions, security considerations.
- **ADR** — one significant decision per file, Nygard format: Status · Context · Decision ·
  Consequences (incl. the alternatives considered and why they lost). Immutable once accepted;
  supersede with a new ADR rather than editing.
- **Developer Guide** — prerequisites, setup, running locally, configuration reference, testing,
  how the repo is structured.
- **Operational Guide** — deployment, monitoring/health, common failure modes, restart/recovery
  runbooks, data management.
- **Changelog** — Keep-a-Changelog style; semantic versioning; deploy vs release.

## Quality bar

- **State problems as problems.** The #1 failure is documenting a solution ("build a dashboard")
  instead of the problem it serves. Push past the requested solution to the underlying need.
- **Success criteria must be observable.** "Improve performance" is not a goal; "p99 < 200ms" is.
- **An ADR's most valuable section is the alternatives** — what you rejected and why. Don't skip it.
- Keep each doc as long as it needs to be and no longer. A crisp one-pager that's read beats a
  thorough document that isn't.
