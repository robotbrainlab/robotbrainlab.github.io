---
name: incident-postmortem
description: >-
  Write a blameless postmortem after an incident. Use when something went wrong in
  production and the user wants to capture it — "write a postmortem", "document
  this incident", "do a retro on the outage", "what went wrong and how do we stop
  it". Produces a blameless postmortem — timeline, root cause and contributing
  factors, impact, and concrete owned action items — aimed at systemic improvement,
  not blame.
---

# Incident Postmortem

Every significant incident is a chance to make the system better. The goal is systemic improvement,
and that only works if it's **blameless** — focused on what in the system and process allowed the
failure, never on which person made a mistake. A postmortem corpus becomes invaluable institutional
memory.

## Workflow

1. **Reconstruct the timeline** — what happened, with timestamps: when it started, when it was
   detected, the key actions, when it resolved.
2. **Quantify impact** — who/what was affected, for how long, how badly.
3. **Find the root cause** — use the five whys to reach the *systemic* cause (a missing check, an
   unmonitored dependency), not "someone typed the wrong thing." Note contributing factors too.
4. **Capture detection** — how was it found, and how long did that take? (Often the biggest lever.)
5. **Write concrete action items** — each one owned and specific, aimed at preventing recurrence
   or shrinking impact / detection time. "Be more careful" is not an action item; "add an alert on
   cert expiry < 14 days" is.

## Output

```markdown
# Postmortem: <incident> — <date>
## Summary
## Impact
## Timeline
## Root cause & contributing factors
## What went well / what didn't
## Action items   (owner · concrete change · prevents what)
```

Write about systems and processes, never people. The moment it assigns blame, people stop being
honest, and you stop learning.
