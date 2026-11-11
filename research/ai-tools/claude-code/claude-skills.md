# Section 5 — Claude Code & Skills

### Turning the whole library into tools Claude Code runs for you

Sections 0–4 are *knowledge* — how to build software well. This section is *action*: it operationalizes
that knowledge as **Claude Code skills**, so the practices don't just live in your head, they run on
demand while you build. It also includes a complete, standalone reference for Claude Code itself.

This section is **cross-cutting** — it's not a lifecycle phase, it's the tooling layer that applies
across all of them.

---

## Table of Contents

- [What's in This Section](#whats-in-this-section)
- [The 32 Skills](#the-32-skills)
- [How to Install the Skills](#how-to-install-the-skills)
- [How It Connects to the Library](#how-it-connects-to-the-library)

---

## What's in This Section

| File | What it is |
|---|---|
| **[`claude-code-guide.md`](claude-code-guide.md)** | A complete standalone reference for Claude Code — what it is, effective use, skills, subagents, hooks, MCP, workflows, best practices, and pitfalls. Read this to master the tool. |
| **[`skills-catalog.md`](skills-catalog.md)** | The catalog of every skill worth having, mapped to the lifecycle — the map of what exists and what each does. |
| **[`skills/`](skills/)** | The source of **32 ready-to-use skills** — each a folder with a `SKILL.md` (and `references/` where needed). This is the version-controlled source of truth. |

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## The 32 Skills

Each operationalizes part of the library. Grouped by what you're doing:

- **Discover & Plan** — `frame-the-problem`, `project-bootstrap`, `project-planning-docs`,
  `design-doc`, `estimate-and-plan`
- **Write & Design Code** — `good-code-review`, `add-feature`, `scaffold`, `api-design`,
  `schema-design`
- **Test & Verify** — `write-tests`, `increase-coverage`, `fix-flaky-tests`
- **Build & Ship** — `ship-it`, `setup-ci`, `containerize`, `release`
- **Operate & Make Reliable** — `codebase-health-check`, `add-observability`, `add-resilience`,
  `write-runbook`, `incident-postmortem`, `data-lifecycle`
- **Debug & Understand** — `debug-by-layer`, `understand-codebase`, `reproduce-bug`
- **Maintain & Evolve** — `upgrade-dependencies`, `migrate`, `remove-tech-debt`
- **Everyday Workflow** — `commit`, `pr-description`, `changelog-update`

See the [catalog](skills-catalog.md) for one-line descriptions, and the 🧩 items it lists that are
better served by Claude Code's **built-in** commands (`/code-review`, `/simplify`, `/verify`,
`/security-review`) rather than a custom skill.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## How to Install the Skills

Claude Code reads **user-level** skills from `~/.claude/skills/`. To activate all of these in every
project, copy (or symlink) the sources there:

```bash
# Copy (simple):
cp -R "05-Claude-Skills/skills/." ~/.claude/skills/

# Or symlink each, so edits here stay live (keeps this repo as the source of truth):
for d in "05-Claude-Skills/skills/"*/; do
  ln -s "$(pwd)/$d" ~/.claude/skills/"$(basename "$d")"
done
```

Then **start a fresh Claude Code session** (skills load at startup) and confirm with `/skills`. To
scope a skill to a single project instead, put it under that project's `.claude/skills/`. See
[`claude-code-guide.md`](claude-code-guide.md#skills--the-deep-dive) for how skills trigger and how to
maintain them.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## How It Connects to the Library

Each skill distills the relevant part of the library so it's **self-contained** (it doesn't depend on
this repo's location once installed). The mapping is direct:

- `frame-the-problem` ← Product Discovery (§1)
- `project-planning-docs` ← Project Planning (§2)
- `good-code-review`, `write-tests`, `refactor`, the design skills ← Writing Good Code (§3)
- `project-bootstrap`, `codebase-health-check`, and all the build/ship/operate skills ← the engineering
  practices & maturity model (§3) and the Book (§4)

So the library teaches the *why*, and these skills apply the *what* — the same knowledge, made
operational.

<sub>[↑ Back to TOC](#table-of-contents)</sub>
