---
name: pr-description
description: >-
  Turn a diff into a clear, reviewer-friendly pull-request description. Use when
  the user wants a PR write-up — "write a PR description", "draft the PR", "describe
  this PR", "PR summary", "open a PR for this". Produces a scannable description:
  what changed and why, how it was tested, and exactly what the reviewer should
  focus on.
---

# PR Description

A reviewer's time is scarce. A good PR description tells them what changed, why it matters, and where
to look — so they review the *right* things instead of reverse-engineering the diff.

## Workflow

1. **Read the diff and commits** (`git diff <base>...HEAD`, `git log`) to understand the change as a whole.
2. **Write it to this shape** (trim what doesn't apply):

```markdown
## <concise title>

**What & why**
<The problem this solves and the change made — the why first.>

**Changes**
- <key change>
- ...

**How it was tested**
<Tests added/run, manual verification, edge cases checked.>

**What to review**
<The risky or non-obvious parts — point the reviewer at where their attention matters most.>

<screenshots for UI changes · "Closes #123">
```

3. **Lead with the why**, keep it scannable (bullets over paragraphs), and be honest about anything
   incomplete or worth a closer look. If the repo has a PR template, follow it.
