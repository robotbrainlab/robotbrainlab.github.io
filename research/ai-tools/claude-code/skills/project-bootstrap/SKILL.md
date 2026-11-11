---
name: project-bootstrap
description: >-
  Set up a new project/codebase with solid foundations from day 0. Use this skill
  whenever the user is starting a new project, repo, service, app, library, or
  script and wants it set up properly — phrases like "start a new project",
  "bootstrap", "scaffold", "set up a repo", "init a new <language> project", "create
  a new service", or even just beginning to build something from an empty folder.
  Prefer it over ad-hoc file creation whenever a fresh codebase is being created,
  even if the user doesn't say "bootstrap". It establishes the foundations that are
  painful or impossible to add later: version control, secrets hygiene,
  linting/formatting, a real README, pinned dependencies in an isolated
  environment, and a sane project structure.
---

# Project Bootstrap

Set up a new codebase so it starts on solid ground. These are **Stage 1 foundations** — the
decisions that are cheap now and expensive (sometimes impossible) to retrofit. A committed
secret can't be un-leaked; formatting bolted on later pollutes the whole history. Getting these
right on day 0 is the highest-leverage thing you can do for a project.

## Workflow

1. **Establish the context.** Determine (ask only if you can't infer):
   - Language / runtime (Python, Node/TypeScript, Go, …) and version.
   - Project type (web service / API, CLI, library, script, AI/ML app).
   - Where it lives (existing empty dir, or create one).
2. **Read `references/languages.md`** for the exact tools, files, and commands for that language.
3. **Create the foundations** (below), tailored to the language. Actually create the files — don't
   just describe them.
4. **Verify** it works: the project installs, the linter runs, and (if applicable) `hello world`
   or the test command runs clean.
5. **Summarize** what you set up and what you deliberately deferred to a later stage (so the user
   knows the boundaries, not just what's there).

## The foundations to set up

**Version control**
- `git init` (if not already a repo); a first commit once the scaffold exists.
- Note the branching convention (trunk-based is the sane default for small teams).

**`.gitignore` + secrets hygiene** *(do this before the first commit)*
- A language-appropriate `.gitignore` excluding build artifacts, virtual envs, caches, and `.env`.
- A committed `.env.example` listing every config key with placeholder values — and a real `.env`
  that is git-ignored. **Never write real secrets into tracked files.** If the user pastes a key,
  put it in `.env` (ignored) and a placeholder in `.env.example`.

**Dependencies in an isolated, pinned environment**
- A dependency manifest with **pinned** versions and a lockfile where the ecosystem has one.
- Isolation: a virtualenv (Python), local `node_modules` + lockfile (Node), modules (Go), etc.

**Linter + formatter, enforced**
- Prefer near-zero-config tools so there are no style debates: Black/ruff (Python), Prettier +
  ESLint (Node/TS), gofmt/golangci-lint (Go). Add their config files.

**README** *(even three honest lines beats nothing)*
- What this is · How to run it · How to run the tests. It's the front door; keep it current.

**A task runner** *(nice to have, but cheap and high-value)*
- A `Makefile` or `justfile`/`package.json` scripts with `run`, `test`, `lint`, `install`, so
  common operations are documented as code, not tribal knowledge.

**A sane starting structure**
- Source under `src/` (or the language's idiom), a `tests/` dir, config at the root. Add a
  minimal runnable entry point and one trivial passing test so the loop is closed from line 1.

## A good first commit

End with everything staged and a clean first commit (e.g. `chore: bootstrap project scaffold`),
the linter passing, and the README explaining how to run it. The user should be able to clone the
result and be productive from the README alone — that's the test of a good bootstrap.

## Boundaries (say what you're *not* doing)

This sets up Stage 1 only. Tests-as-discipline, CI, structured logging, validation, deployment,
and observability come later — point the user to a **codebase-health-check** when they're ready to
take the project to the next stage, rather than gold-plating now.
