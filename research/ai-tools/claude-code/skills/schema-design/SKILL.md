---
name: schema-design
description: >-
  Design or evolve a database schema. Use whenever the user is modeling data or
  changing a schema — "design the schema for X", "model these entities", "add a
  table for Y", "what columns should this have", "how do I change this schema
  safely / add a column without downtime". Models entities and relationships,
  normalizes appropriately, chooses keys deliberately, adds audit columns, and
  produces a safe expand/contract migration for changes.
---

# Schema Design

The schema outlives everything else — the app can be rewritten, the table usually can't. Design it
on purpose.

## Designing a new schema

1. **Model entities, attributes, relationships** (and cardinality). The foreign keys *are* the
   relationships — sketch them before writing SQL.
2. **Normalize** so each fact lives in exactly one place (1NF: atomic values, no comma-lists; 2NF/3NF:
   non-key columns depend on the key, the whole key, and nothing but the key). This prevents update/
   insert/delete anomalies. Denormalize only deliberately, accepting the duty to keep copies in sync.
3. **Choose keys.** Prefer **surrogate** keys (a meaningless `id`) over natural ones (real-world
   values change). Know the trade-offs: auto-increment (small, ordered, but guessable/collide on
   merge) vs UUID (globally unique, larger/random) vs ULID (both).
4. **Add audit columns** (`created_at`, `updated_at`) by default; store time as **UTC, timezone-aware**.
5. **Decide soft vs hard delete** on purpose (recoverable/auditable vs simple/space-reclaiming).

## Evolving an existing schema (safely)

- **Additive changes are safe** (a nullable/defaulted column). **Breaking changes** (rename, drop,
  add NOT NULL) need the **expand/contract** pattern: *expand* (add new, write both) → *migrate*
  (backfill) → *contract* (switch reads, drop old) — each step independently deployable, zero downtime.
- Schema changes are **versioned migrations** in the repo, applied in order. Never alter a prod table by hand.

## Output

The `CREATE TABLE` / migration SQL, the key + index strategy, and the reasoning behind each choice.
