---
name: write-runbook
description: >-
  Write operational runbooks for a system's failure modes. Use when the user wants
  incident playbooks — "write a runbook", "document how to handle <incident>",
  "create an on-call guide", "what do we do when the database fills up / the
  service is down". Produces step-by-step runbooks per foreseeable incident, and
  surfaces design gaps in the process.
---

# Write Runbook

Under the stress of a 3 a.m. incident, fresh thinking fails. A runbook is the difference between a
five-minute and a five-hour recovery. Writing one also reveals gaps in the system (a missing alert,
no rollback path) while it's cheap to fix them.

## Workflow

1. **Enumerate the foreseeable incidents**, by layer — e.g. service down / crash-looping, database
   full or slow, a background job stuck, an external dependency unavailable, TLS cert expiry, out of
   memory, disk full.
2. **For each, write the runbook entry:**

```markdown
## Incident: <name>

**Symptoms:** <what the user sees / what the alert says>
**Confirm it:** <the exact diagnostic command(s) to verify the cause>
**Recover:** <step-by-step, with the exact commands>
**Prevent:** <the change that stops it recurring>
```

3. **Note the gaps** you find: if an incident has no alert that would catch it, or no tested
   rollback, flag that as follow-up work — the act of writing the runbook earned that insight.

Keep each entry to commands and steps, not prose — it's read in a hurry.
