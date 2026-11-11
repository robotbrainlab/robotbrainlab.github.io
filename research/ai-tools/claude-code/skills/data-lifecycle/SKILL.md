---
name: data-lifecycle
description: >-
  Set up data retention, backups, deletion, and PII handling. Use when the user is
  dealing with data over time — "set up data retention", "add backups", "how do we
  handle GDPR / right-to-be-forgotten", "clean up old data", "set up a cleanup
  job", "what's our PII policy". Produces a retention policy, a backup approach
  with restore testing, PII handling, and safe cleanup jobs.
---

# Data Lifecycle

"Store everything forever" is not a policy — it's the absence of one. Accumulated data gets
expensive, slow, and legally fraught. Manage it on purpose.

## What to set up

1. **Classify the data** — PII · sensitive · operational · public. Handling differs per class.
2. **Retention policy** — a simple matrix: *data category × how long it lives × why*. (e.g.
   request logs 90 days; soft-deleted records purged after 30; audit logs 7 years; backups 30 days.)
3. **Backups + restore testing** — automated backups at a sensible frequency, **and a tested
   restore**. An untested backup is a hope, not a backup. Know your RTO/RPO.
4. **Safe cleanup jobs** — when deleting old data: **dry-run** first, delete in **batches**,
   **soft-delete before hard-delete**, and write an **audit log** of what was removed.
5. **PII & right-to-be-forgotten** — to honor a deletion request you must know *everywhere* a user's
   PII lives: the primary table, search indexes, caches, **logs** (you shouldn't have logged it),
   analytics, and **backups**. Practice **data minimization** (don't collect what you don't need)
   and **pseudonymization**.

## The trap most teams miss

Deleted data lives on in **backups** for the length of the backup retention window — so "we deleted
it" must account for backups too. Bake that into the policy.

## Output

The retention matrix, the backup/restore plan, and the cleanup job (with its safety rails).
