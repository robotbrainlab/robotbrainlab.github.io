# The Complete Guide to Claude Code

### What it is, how to use it well, and how to extend it with skills, agents, hooks, and MCP

Claude Code is Anthropic's agentic coding tool: you describe what you want in plain language, and it
reads your codebase, edits files, runs commands, and verifies its own work — across many files and
tools in a single request. This is a standalone reference: read it front-to-back to learn the tool,
or jump to a section when you need it.

> **A note on currency.** Claude Code evolves quickly. The concepts here are stable; specific command
> names, flags, and settings keys can change between versions. When something looks off, run `/help`,
> `/doctor`, or check the official docs — and `claude --version` to see what you're on.

---

## Table of Contents

- [What Claude Code Is](#what-claude-code-is)
  - [The core interaction model](#the-core-interaction-model)
- [Getting Started](#getting-started)
  - [Install & authenticate](#install--authenticate)
  - [Interactive vs. one-shot](#interactive-vs-one-shot)
  - [Your first moves in a repo](#your-first-moves-in-a-repo)
- [Effective Prompting](#effective-prompting)
- [Project Memory: CLAUDE.md](#project-memory-claudemd)
- [Slash Commands](#slash-commands)
- [Permissions & Settings](#permissions--settings)
- [Skills — The Deep Dive](#skills--the-deep-dive)
  - [Anatomy](#anatomy)
  - [Where skills live](#where-skills-live)
  - [How triggering works — the most important thing to get right](#how-triggering-works--the-most-important-thing-to-get-right)
  - [Progressive disclosure (why skills stay cheap)](#progressive-disclosure-why-skills-stay-cheap)
  - [When to use a skill (vs. CLAUDE.md vs. a subagent)](#when-to-use-a-skill-vs-claudemd-vs-a-subagent)
  - [Creating and maintaining skills](#creating-and-maintaining-skills)
- [Subagents (Custom Agents)](#subagents-custom-agents)
- [Hooks](#hooks)
- [MCP Servers](#mcp-servers)
- [Other Concepts Worth Knowing](#other-concepts-worth-knowing)
- [Recommended Workflows](#recommended-workflows)
- [Best Practices](#best-practices)
- [Common Patterns & Examples](#common-patterns--examples)
- [Common Pitfalls](#common-pitfalls)
- [Quick Reference](#quick-reference)

---

## What Claude Code Is

Claude Code is one engine behind several interfaces — use whichever fits the moment:

- **Terminal CLI** (`claude`) — the full-featured, power-user home.
- **IDE extensions** — VS Code and JetBrains, with inline diffs, `@`-mentions, and plan review.
- **Desktop app** (macOS/Windows) — visual diffs, side-by-side sessions, scheduled tasks.
- **Web** (claude.ai/code) — browser-based, long-running cloud tasks, works on mobile.
- **Automation** — GitHub Actions / GitLab CI, Slack, and remote control of a local session.

All of them share the same agentic model and the same configuration (`~/.claude/`, `.claude/`), so
skills, settings, and memory you set up apply across them.

### The core interaction model

Claude Code works in a loop: **gather context → (optionally) plan → act → verify → repeat.**

1. **Read** — it explores with Bash, Read, Grep, Glob, WebFetch, changing nothing.
2. **Plan** (optional) — in plan mode it proposes an approach for you to refine before any edits.
3. **Act** — it edits and writes files and runs commands (asking permission by default).
4. **Verify** — it runs tests/builds and iterates on failures.

The practical implication: **give it something to verify** (tests, a build, a script, screenshots),
and it will keep working until that check passes instead of stopping when the code merely "looks done."

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Getting Started

### Install & authenticate

```bash
# macOS / Linux / WSL (auto-updating)
curl -fsSL https://claude.ai/install.sh | bash
# macOS via Homebrew, or Windows via the PowerShell installer, are also supported.

cd your-project
claude            # first run walks you through browser-based login
```

It works with Claude Pro/Max/Team/Enterprise plans or a Claude Console (API) account, and can route
through Amazon Bedrock, Google Vertex, or Microsoft Foundry.

### Interactive vs. one-shot

- **Interactive** (default): `claude` — a back-and-forth session. Press **Esc** any time to stop
  Claude mid-action and redirect (your context is preserved).
- **Continue / resume**: `claude -c` continues the most recent session; `claude -r` opens a picker.
- **One-shot / print** (for scripts and pipes): `claude -p "your prompt"` runs once and exits.
  Add `--output-format json` for structured output; pipe input in with `echo ... | claude -p "..."`.

### Your first moves in a repo

Ask it to orient ("what does this project do?"), make a small change, run the tests, and commit.
Build the habit of giving it a verifiable target: *"fix the login bug where a wrong password shows a
blank screen — write a failing test first, then fix it, then run the tests."*

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Effective Prompting

The difference between mediocre and excellent results is mostly in how you frame the task.

- **Be specific.** "Fix the auth bug" is weak. "Fix the login bug where users see a blank screen
  after a wrong password — check `src/auth/`, especially token refresh — write a failing test first"
  is strong. Point at files, describe the symptom, and state the acceptance criteria.
- **Give it something to verify.** Provide tests, a command, or explicit success conditions. Claude
  self-corrects against a check far better than against vibes.
- **Reference files with `@`.** `review @src/auth/session.ts for vulnerabilities` reads the file
  immediately — no copy-paste.
- **Separate explore from implement.** Use plan mode (below) to investigate and agree on an approach
  *before* edits, so you catch a wrong direction before code is written.
- **Keep tasks focused.** One coherent task per session stretch. Use `/clear` between unrelated
  tasks so stale context doesn't muddy the new one.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Project Memory: CLAUDE.md

`CLAUDE.md` is a markdown file of **persistent instructions Claude reads at the start of every
session** — the project knowledge it can't infer from code.

**Where it lives** (loaded in order, later = more specific):
- `~/.claude/CLAUDE.md` — applies to all your projects.
- `./CLAUDE.md` or `./.claude/CLAUDE.md` — project-specific; commit it so the team shares it.
- `./CLAUDE.local.md` — personal overrides for one project; git-ignore it.

**What to put in it:** build/test/run commands, code-style rules that differ from defaults, testing
conventions, branch/PR etiquette, architectural decisions, environment quirks, and non-obvious
gotchas. **What to leave out:** anything Claude can read from the code, standard language
conventions, long tutorials, or fast-changing details. **Keep it under ~200 lines** — a bloated
CLAUDE.md buries its own rules and they get ignored. For large projects, use path-scoped
`.claude/rules/*.md` and **skills** (below) for task-specific procedures instead of cramming
everything here.

**Bootstrap it** with `/init`, which analyzes the repo and drafts a CLAUDE.md you then refine. Claude
Code also keeps an **auto-memory** (`~/.claude/projects/<project>/memory/`) that persists learnings
across sessions; manage it with `/memory`.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Slash Commands

Slash commands are built-in (and custom) shortcuts. The ones worth knowing:

**Setup & config:** `/init` (draft CLAUDE.md) · `/config` (settings UI) · `/model` (switch model) ·
`/permissions` (allow/deny rules) · `/skills` (list/toggle skills) · `/agents` (manage subagents) ·
`/hooks` (browse hooks) · `/mcp` (manage MCP servers) · `/memory` · `/doctor` (diagnose install).

**Session & context:** `/clear` (fresh start, keeps CLAUDE.md) · `/compact` (summarize to free
context) · `/context` (visualize context usage) · `/resume` · `/rewind` (restore to a checkpoint) ·
`/export`.

**Coding workflows:** `/plan` (read-only exploration) · `/review` (review a PR) · `/code-review`
(review the diff for bugs) · `/simplify` (cleanup-only) · `/security-review` · `/run` & `/verify`
(build/run the app to confirm changes — set up via the run-skill generator) · `/diff`.

Run `/help` for the full, version-current list. **Custom commands/skills** you create appear here as
`/<name>` too (see Skills).

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Permissions & Settings

Claude Code asks before doing anything consequential by default. You tune this with **permission
modes** and **rules**.

**Permission modes** (cycle with **Shift+Tab**, or set `defaultMode`):
- `default` — prompts on first use of each tool. Safe, a bit tedious.
- `acceptEdits` — auto-accepts file edits and common filesystem commands; still asks for the rest.
- `plan` — read-only: explores and answers, never edits.
- `bypassPermissions` — skips prompts. **Only in isolated/sandboxed environments.**

**Settings files** (`settings.json`), from lowest to highest precedence: `~/.claude/settings.json`
(user) → `.claude/settings.json` (project, committed) → `.claude/settings.local.json` (project,
git-ignored) → managed/enterprise settings (can't be overridden).

**Permission rules** — scope what's allowed without prompting, and block what shouldn't be:

```json
{
  "permissions": {
    "allow": ["Bash(npm run test)", "Bash(git commit *)", "Bash(npm run lint)"],
    "deny":  ["Bash(rm -rf *)", "Edit(.env)", "Edit(.git/**)"],
    "ask":   ["Bash(git push *)"]
  },
  "env": { "NODE_ENV": "development" }
}
```

Rules match a tool (`Bash`), a fine-grained specifier (`Bash(npm test)`), wildcards (`Bash(npm *)`),
or file globs (`Edit(/src/**)`). Evaluation is **deny → ask → allow**, first match wins. Note that
Bash wildcards are fragile (they won't catch flags-before-URL or variables) — prefer `deny` rules
for genuinely dangerous commands and hooks for complex validation.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Skills — The Deep Dive

A **skill** is a folder with a `SKILL.md` that packages a repeatable workflow or body of knowledge.
Claude loads a skill **on demand** when your request matches it — which is the key advantage over
CLAUDE.md: CLAUDE.md is in context *every* session, while a skill costs nothing until it's needed.

### Anatomy

```
my-skill/
├── SKILL.md            # required: YAML frontmatter + markdown instructions
├── references/         # optional: docs loaded only when the skill points to them
│   └── details.md
├── scripts/            # optional: code Claude executes (not loaded into context)
└── assets/             # optional: templates, files used in output
```

```yaml
---
name: my-skill
description: >-
  What it does AND when to use it — this is the trigger. Be specific and a little
  pushy about the contexts that should activate it.
# optional: allowed-tools, disable-model-invocation, model, effort, context: fork, paths, ...
---

# My Skill
Imperative instructions. Explain the *why* behind steps so the model can reason, not just follow.
```

### Where skills live

- `~/.claude/skills/<name>/` — **user-level**: available in every project. Best for general,
  cross-project skills (the 32 in this section live here).
- `.claude/skills/<name>/` — **project-level**: scoped to one repo; commit it to share with a team.
- Plugin skills — distributed via plugins.

### How triggering works — the most important thing to get right

Claude sees every skill's **name + description** at session start and decides — based on the
**description** — whether a given request warrants consulting that skill. So:
- **The description is the trigger.** Put both *what it does* and *when to use it* there, including
  the phrasings a user would actually say. Lean slightly pushy — skills tend to *under*-trigger.
- **Simple one-step tasks may not trigger a skill at all**, because Claude can just do them. Skills
  reliably trigger on substantive, multi-step, or specialized work where consulting them pays off.

### Progressive disclosure (why skills stay cheap)

Three levels load lazily: **(1)** name + description, always in context (~tiny); **(2)** the
`SKILL.md` body, loaded only when the skill triggers; **(3)** `references/` files and `scripts/`,
loaded/executed only when the body points to them. Keep `SKILL.md` tight (under ~500 lines) and push
long checklists, templates, and per-variant details into `references/`.

### When to use a skill (vs. CLAUDE.md vs. a subagent)

- **CLAUDE.md** — session-wide *facts* about this project (commands, conventions). Always loaded.
- **Skill** — a reusable *procedure or knowledge* applied to a kind of task (bootstrap a repo, write
  tests, review for craft). Loaded on demand.
- **Subagent** — *delegated* work that should run in its own isolated context (a big investigation,
  a specialized review) and report back a summary. Keeps your main context clean.

### Creating and maintaining skills

1. `mkdir -p ~/.claude/skills/<name>/references`
2. Write `SKILL.md`: a pushy `description`, a focused imperative workflow, the *why* behind each step.
   Embed the knowledge so the skill is self-contained; add `references/` only for long material.
3. **Restart the session** (skills load at startup), then test on a realistic prompt and watch
   whether it triggers and behaves. Refine the `description` if it over- or under-fires.
4. **Maintain from real usage.** The best signal is how it behaves on actual work, not synthetic
   tests — when it misfires, adjust the description or tighten the instructions.
5. For a rigorous loop, the `skill-creator` skill can benchmark a skill with-vs-without on test cases.

The 32 skills in [`skills/`](skills/) and the [skills catalog](skills-catalog.md) are working examples
to copy — open any `SKILL.md` to see the shape.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Subagents (Custom Agents)

A **subagent** is a specialized assistant Claude can delegate to. It runs in its **own context
window** with its own system prompt and tool set, does the work independently, and returns a result.

Define them in `.claude/agents/<name>.md` (project) or `~/.claude/agents/` (user):

```markdown
---
name: security-reviewer
description: Reviews code for injection, auth, secrets, and insecure data handling. Use when code should be security-checked.
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review for injection, authz flaws, plaintext secrets, and
insecure data handling. Give line references and fixes; report findings, not style.
```

Claude delegates automatically when a task matches the description, or you can ask explicitly ("use
the security-reviewer subagent on this"). **Use a subagent** to isolate a context-heavy investigation
or a specialized, repeatable judgement; **use a skill** when the knowledge should guide the main
session directly.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Hooks

**Hooks** are shell commands that run at specific lifecycle points — deterministic automation, unlike
CLAUDE.md's advisory instructions. They're how you enforce "always do X" rules the model can't skip.

Common events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`,
`Notification`, `PreCompact`, `SessionEnd`. Configure them in `settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Edit|Write",
        "hooks": [{ "type": "command",
          "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write" }] }
    ]
  }
}
```

That auto-formats every file Claude edits. Other classic uses: **block** edits to `.env` (a
`PreToolUse` hook that denies), **notify** you when Claude needs attention (`Notification`), or
**verify** the task is actually done before Claude stops (`Stop`). Hooks communicate via exit codes
(exit 2 blocks the action and feeds stderr back to Claude) or structured JSON. Browse what's
configured with `/hooks`.

> If a user asks you to make Claude "always" or "automatically" do something each time an event
> happens, that's a hook — the model can't reliably self-enforce it, but a hook can.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## MCP Servers

The **Model Context Protocol** connects Claude Code to external tools and data — GitHub, a database,
Jira, Slack, Figma, anything with an MCP server. Add one with `/mcp` (interactive), `claude mcp add
<name>`, or in settings under `mcpServers`. Servers can be **local** (run on your machine — direct
filesystem/command access, low latency) or **remote** (shared, cloud-hosted).

At session start Claude discovers the server's tools; their full definitions load on demand (to save
context) when needed. Scope MCP tools with the same permission rules, e.g. `mcp__github__*`. Reach
for MCP when Claude needs to *act on an external system* that isn't a shell command.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Other Concepts Worth Knowing

- **Plan mode** (`/plan`, or Shift+Tab twice) — read-only exploration. Claude investigates and
  proposes a plan; you refine it before any edits. The single best habit for non-trivial work.
- **Checkpoints & rewind** (`/rewind`, or Esc-Esc) — every prompt snapshots the code. You can revert
  Claude's edits, the conversation, or both, even across sessions. (It tracks *Claude's* changes —
  it's not a replacement for git.)
- **Context management** — context fills with conversation, file contents, and command output, and
  performance degrades as it fills. Use `/context` to inspect, `/clear` between unrelated tasks, and
  `/compact` to summarize. Long investigations are best delegated to subagents to keep your context
  clean.
- **Model & effort** — `/model` switches model (Opus / Sonnet / Haiku tiers); higher reasoning
  effort means more thinking on hard problems. Match the model to the task.
- **Images** — paste or reference screenshots/mockups; Claude can compare a UI to a design or read an
  error screenshot.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Recommended Workflows

**Explore → Plan → Implement → Commit** (the default for anything non-trivial):
1. In plan mode: "read `src/auth/` and explain how sessions work."
2. Still planning: "draft a plan for adding OAuth." Refine it together.
3. Exit plan mode: "implement the plan."
4. "Commit with a descriptive message and open a PR."

**Test-Driven** — give it the target up front: "write `validateEmail`. Cases: `a@b.com`→true,
`invalid`→false. Write the tests, implement, run them, fix until green." The verifiable target is
what makes this reliable.

**Debugging** — localize before changing: "this endpoint 500s on large payloads — check the logs,
find which layer fails, form a hypothesis, then fix the root cause and add a regression test."

**Large mechanical changes** — for repo-wide transforms, scope tightly and let Claude work file by
file (or use the batch/worktree tooling) rather than one giant edit.

**Research vs. implementation** — push big investigations to a subagent ("use a subagent to map how
auth works") so the findings come back as a summary and your main context stays focused.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Best Practices

- **Give Claude something to verify** — tests, a build, a script, success criteria. It self-corrects
  against checks, not vibes.
- **Be specific and point at files** with `@`. Vague prompts get vague work.
- **Plan before you implement** anything non-trivial.
- **`/clear` between unrelated tasks**; don't let one session accumulate ten topics.
- **Keep CLAUDE.md lean** (<200 lines); move procedures to skills and path-rules to `.claude/rules/`.
- **Scope permissions deliberately** — allow your safe, frequent commands; deny the dangerous ones.
- **Use the right extension point:** facts → CLAUDE.md; procedures/knowledge → skills; isolated or
  specialized work → subagents; "always do X on event Y" → hooks; external systems → MCP.
- **Commit regularly** — checkpoints revert Claude's edits within a session; git is your real history.
- **After two failed corrections on the same point, `/clear` and re-prompt** more precisely rather
  than fighting a muddied context.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Common Patterns & Examples

**A focused feature prompt**
> Add a `DELETE /notes/:id` endpoint. Follow the pattern in `@src/routes/notes.ts` exactly —
> same validation, error handling, and tests. Run the test suite when done.

**A bug with a built-in check**
> Users report the export button does nothing on Safari. Reproduce it, write a failing test, fix
> the root cause, and confirm the test passes.

**Set up the project once**
> `/init` — then refine the generated CLAUDE.md so it has our real build/test commands and the rule
> that all DB access goes through `repository/`, never raw SQL in handlers.

**Auto-format on every edit** (a hook, in `settings.json`)
> PostToolUse on `Edit|Write` → run the formatter on the changed file.

**Delegate an investigation**
> Use a subagent to trace how a request flows from the API gateway to the database, and report the
> key files and any surprises.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Common Pitfalls

- **Context fills fast.** One big debugging session can consume tens of thousands of tokens and
  degrade quality. Monitor with `/context`; `/clear` and delegate to keep it clean.
- **Bloated CLAUDE.md gets ignored.** Rules buried in noise are forgotten. Prune ruthlessly.
- **"Looks done" ≠ done.** Without a check to run, Claude stops at plausible. Always give it one.
- **Fragile Bash permission patterns.** `Bash(curl http://x/ *)` won't match flags or `https`. Use
  `deny` rules and hooks for real protection, not clever allow-patterns.
- **Checkpoints aren't git.** They track Claude's edits, not external processes or your commits.
- **Skill won't trigger?** The description is almost always the cause — make it more specific about
  *when* to use it, and remember trivial tasks may not trigger any skill.

<sub>[↑ Back to TOC](#table-of-contents)</sub>

## Quick Reference

| Thing | Path / command |
|---|---|
| User settings · CLAUDE.md | `~/.claude/settings.json` · `~/.claude/CLAUDE.md` |
| Project settings · CLAUDE.md | `.claude/settings.json` · `./CLAUDE.md` |
| Local (git-ignored) overrides | `.claude/settings.local.json` · `./CLAUDE.local.md` |
| User · project skills | `~/.claude/skills/<name>/` · `.claude/skills/<name>/` |
| User · project subagents | `~/.claude/agents/<name>.md` · `.claude/agents/<name>.md` |
| Path-scoped rules | `.claude/rules/*.md` |
| Start / continue / resume | `claude` · `claude -c` · `claude -r` |
| One-shot | `claude -p "prompt"` |
| Stop mid-action · rewind | `Esc` · `Esc Esc` / `/rewind` |
| Cycle permission mode | `Shift+Tab` |
| Plan mode · fresh context | `/plan` (or Shift+Tab×2) · `/clear` |
| Bootstrap · diagnose · help | `/init` · `/doctor` · `/help` |

For everything Claude Code can *do for you* in a codebase, see the
[Skills Catalog](skills-catalog.md) and the 32 ready-to-use skills in [`skills/`](skills/).
