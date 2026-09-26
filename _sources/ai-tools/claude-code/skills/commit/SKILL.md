---
name: commit
description: >-
  Write clear, well-structured git commits. Use when the user wants to commit —
  "commit this", "commit my changes", "write a commit message", "git commit". It
  groups related changes into logical commits (not one undifferentiated dump) and
  writes Conventional-Commits-style messages whose body explains the *why*, not the
  *what*. Only commits when the user has asked.
---

# Commit

A good commit message is a message to the future — including you, debugging this line in a year. It
explains *why* the change was made; the diff already shows *what*.

## Workflow

1. **Review the changes** (`git status`, `git diff`) and understand what actually changed.
2. **Group into logical commits.** Don't lump unrelated changes together — a commit should be one
   coherent change that could be reverted on its own. Stage selectively if needed.
3. **Write each message** in Conventional Commits style:
   - `type(scope): short summary` — types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, `perf`.
   - Subject in the imperative mood, ≤ ~72 chars ("add", not "added").
   - A body (when the change isn't trivial) explaining the **why** — the non-obvious reason, the
     constraint, the bug this fixes — not a restatement of the diff.
   - Reference issues/tickets where relevant.
4. **Never commit secrets, `.env`, or generated artifacts.** Check the diff for them first.

## Examples

```
feat(auth): add JWT refresh-token rotation

Access tokens expired mid-session with no recovery, forcing re-login.
Rotating refresh tokens on use keeps sessions alive while limiting the
blast radius of a leaked token.
```
```
fix(api): return 400, not 500, on malformed JSON body
```

Only run `git commit` (and especially `git push`) when the user has asked you to.
