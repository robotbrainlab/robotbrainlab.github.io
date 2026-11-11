# Claude Code Skills Catalog

### Every skill worth having — turning the software-engineering lifecycle into things Claude Code does for you

A **skill** packages a repeatable workflow so Claude Code runs it on demand instead of you
re-explaining it each time. This catalog is the *full set* a developer benefits from, mapped to the
lifecycle in the [Complete Software Engineering Guide](../The-Complete-Software-Engineering-Guide.md):
each phase has *knowledge* (the library) and *action* (a skill that applies it).

**All 32 of these are now built and installed** (sources in [`skills/`](skills/)). This catalog is
the map: what exists, what each does, and the handful (marked 🧩) intentionally left to Claude Code's
built-ins instead of duplicated. To pick one to *reach for*, see [Which to Reach For First](#which-to-reach-for-first).

**Status legend:** ✅ built and installed (source in [`skills/`](skills/)) · 🧩 use Claude Code's
built-in instead (check `/skills`).

---

## Table of Contents

- [How to Read This Catalog](#how-to-read-this-catalog)
- [Discover & Plan](#discover--plan)
- [Write & Design Code](#write--design-code)
- [Test & Verify](#test--verify)
- [Build & Ship](#build--ship)
- [Operate & Make Reliable](#operate--make-reliable)
- [Debug & Understand](#debug--understand)
- [Maintain & Evolve](#maintain--evolve)
- [Everyday Workflow](#everyday-workflow)
- [Which to Reach For First](#which-to-reach-for-first)
- [How to Build One (quick reference)](#how-to-build-one-quick-reference)

<sub>[↑ Back to TOC](#table-of-contents)</sub>

---

## How to Read This Catalog

Skills come in two flavors, and it's worth knowing which you're building:

- **Action skills** *produce or change files* — bootstrap a repo, write tests, add logging. These
  are where Claude Code saves the most effort, because the work is concrete and repetitive.
- **Thinking skills** *structure a conversation or judgement* — frame a problem, review for craft,
  decide an architecture. These reduce effort differently: they stop you skipping the step.

A good skill does **one job**, has a **pushy description** (so it triggers when needed), and is
**self-contained** (embeds its knowledge rather than depending on external files). Keep each under
~500 lines of `SKILL.md`, with longer checklists/templates in a `references/` folder.

> **Don't duplicate the built-ins.** Claude Code already ships review, simplify, verify, run, and
> security tooling. Where a 🧩 appears below, prefer the built-in and only build your own if you want
> a sharply different angle (e.g. craft-focused review vs. bug-focused review).

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Discover & Plan

The front of the lifecycle: decide what to build and frame it before code.

| Skill | What it does | Status |
|---|---|---|
| **frame-the-problem** | Run structured product discovery before building — clarify the real problem (not the proposed solution), the user, the value, the riskiest assumption, and the smallest test. Triggers on "I want to build X", new-idea framing. | ✅ |
| **project-bootstrap** | Set up a new repo with day-0 foundations: git, `.gitignore` + secrets hygiene, pinned deps in an isolated env, linter/formatter, README, smoke test. | ✅ |
| **project-planning-docs** | Generate the doc set a project keeps — problem statement, architecture, ADRs, dev/ops guides, changelog — pre-filled, with open decisions marked. | ✅ |
| **design-doc** | Write a focused design doc / RFC for *one* feature or change before coding it: the problem, the approach, alternatives, the rollout. Lighter than full planning. | ✅ |
| **estimate-and-plan** | Break a feature into sequenced, right-sized tasks with rough effort and dependencies, so a vague ask becomes a buildable plan. | ✅ |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Write & Design Code

Producing good code, and the design decisions just above it.

| Skill | What it does | Status |
|---|---|---|
| **good-code-review** | Review a diff/file for *craft* — naming, functions, deep modules, command/query separation, error-handling, smells — with prioritized before/after suggestions. | ✅ |
| **add-feature** | Implement a feature end-to-end across the project's layers (route → logic → data → test), matching existing conventions instead of inventing new ones. | ✅ |
| **scaffold** | Generate a new module / endpoint / component that mirrors the repo's existing patterns and wiring, so new code looks like it belongs. | ✅ |
| **api-design** | Design an API contract: resource URLs, methods + idempotency, versioning, pagination, consistent error shape, and an OpenAPI spec. | ✅ |
| **schema-design** | Design or evolve a database schema — entities/relationships, normalization, key strategy, audit columns — plus a safe expand/contract migration. | ✅ |
| **refactor** | Restructure a target in small, behavior-preserving steps under tests (deeper and more directed than the built-in cleanup). | 🧩 |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Test & Verify

Making code actually work, and proving it stays working. *(The biggest current gap.)*

| Skill | What it does | Status |
|---|---|---|
| **write-tests** | Generate good tests for a function/module in the project's framework — happy path, edge cases, and one integration test — following the test pyramid, not just the happy path. | ✅ |
| **increase-coverage** | Find the untested *critical* paths (not vanity coverage) and add tests for them, reporting what's still uncovered and why it matters. | ✅ |
| **fix-flaky-tests** | Diagnose and stabilize a flaky test — isolate the nondeterminism (time, ordering, shared state, network) and fix the root cause. | ✅ |
| **verify-change** | Run the app and confirm a change actually works in behavior, not just in theory. | 🧩 |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Build & Ship

Turning code that runs locally into a real, deployed application — the heart of the book.

| Skill | What it does | Status |
|---|---|---|
| **ship-it** | Take a project from "runs locally" to deployable: a multi-stage Dockerfile, a CI pipeline, and the deploy config — the whole code-to-production path in one move. | ✅ |
| **setup-ci** | Stand up a CI pipeline (install → lint → test → build, on push/PR) as the first automated quality gate. | ✅ |
| **containerize** | Write a clean, small, multi-stage Dockerfile (+ compose for local deps) with a non-root user and a healthcheck. | ✅ |
| **release** | Cut a release: choose the semantic-version bump, update the changelog (Keep-a-Changelog), and tag — distinguishing a deploy from a user-visible release. | ✅ |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Operate & Make Reliable

Keeping a running system observable, reliable, and recoverable.

| Skill | What it does | Status |
|---|---|---|
| **codebase-health-check** | Assess a repo's maturity stage, the missing non-negotiables, and a prioritized "do next" list — the maturity model as a diagnostic. | ✅ |
| **add-observability** | Instrument code with structured logging, key metrics, a health/readiness endpoint, and request-ID correlation, so the system can be operated, not just run. | ✅ |
| **add-resilience** | Make outbound calls survive partial failure: explicit timeouts, retries with exponential backoff + jitter, circuit breakers, and idempotency for retryable operations. | ✅ |
| **write-runbook** | Generate step-by-step runbooks for the system's foreseeable incidents (down, DB full, stuck job, dependency outage) — and surface design gaps in the process. | ✅ |
| **incident-postmortem** | Turn an incident into a blameless postmortem: timeline, root cause, contributing factors, and concrete action items. | ✅ |
| **data-lifecycle** | Set up retention policy, backups (with restore testing), PII handling, and safe cleanup jobs for the data a system accumulates. | ✅ |
| **security-review** | Audit for the OWASP-style issues — secrets, authz, injection, transport — before shipping. | 🧩 |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Debug & Understand

Diagnosing what broke, and orienting in code you didn't write.

| Skill | What it does | Status |
|---|---|---|
| **debug-by-layer** | Localize a failure to its layer — client, DNS, proxy, app, database — and run the *right* diagnostic for that layer first, instead of poking randomly. | ✅ |
| **understand-codebase** | Onboard to an unfamiliar repo fast: find the entry point, trace one real request end-to-end, map the architecture, and surface the riskiest unknowns. | ✅ |
| **reproduce-bug** | Reproduce a reported (often production-only) issue locally, building the smallest failing case so it can be fixed and regression-tested. | ✅ |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Maintain & Evolve

Keeping a living codebase healthy over time.

| Skill | What it does | Status |
|---|---|---|
| **upgrade-dependencies** | Audit dependencies for vulnerabilities and staleness, then upgrade safely — reading changelogs for breaking changes and running tests after each step. | ✅ |
| **migrate** | Execute a migration (framework version, library swap, schema change) using expand/contract so the system keeps working at every step. | ✅ |
| **document-codebase** | Generate or refresh the docs an inherited repo is missing — README, architecture overview, API docs — from the actual code. | 🧩 |
| **remove-tech-debt** | Find and prioritize tech debt and dead code (unused deps, commented-out blocks, duplicated knowledge), and clean it up safely. | ✅ |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Everyday Workflow

The small, high-frequency things that add up.

| Skill | What it does | Status |
|---|---|---|
| **commit** | Write clear, conventional-commit messages that explain the *why*, grouped into logical commits rather than one dump. | ✅ |
| **pr-description** | Turn a diff into a reviewer-friendly PR description: what changed, why, how it was tested, and what to look at. | ✅ |
| **changelog-update** | Update `CHANGELOG.md` from recent commits, sorted into Added / Changed / Fixed / Security. | ✅ |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Which to Reach For First

All 32 are installed, so the question isn't *what to build* — it's *which to lean on*. For the
**daily build loop**, these earn their keep most often:

- **project-bootstrap** — every new repo, start it right.
- **write-tests** — the habit that keeps a "working" project from quietly rotting.
- **good-code-review** — keep craft up as you go.
- **debug-by-layer** — the verb you reach for most when something breaks.
- **understand-codebase** — the moment you join a repo you didn't write.
- **ship-it** — when local code needs to become a real, deployed application.

The rest are there when their moment comes — planning a project, cutting a release, an incident, a
migration. The way to invoke one is to **name the verb** ("review this", "ship this", "debug this")
and the matching skill triggers. The ones you actually use will refine themselves from real usage.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## How to Build One (quick reference)

1. `mkdir -p ~/.claude/skills/<skill-name>/references`
2. Write `SKILL.md` with YAML frontmatter (`name`, a **pushy** `description` that says *when* to
   trigger) and an imperative workflow. Put long checklists/templates in `references/`.
3. Embed the knowledge (don't depend on this library's path), and explain the *why* behind each
   step so the model can reason, not just follow.
4. Start a fresh Claude Code session and test it on a realistic prompt. Refine the description if it
   over- or under-triggers.
5. For the rigorous path, the `skill-creator` skill can benchmark a skill with-vs-without on test
   prompts.

The four already-built skills are working examples of this structure — copy their shape.

<sub>[↑ Back to TOC](#table-of-contents)</sub>
