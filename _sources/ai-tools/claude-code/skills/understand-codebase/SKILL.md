---
name: understand-codebase
description: >-
  Orient quickly in an unfamiliar codebase. Use when the user has joined or needs
  to understand a repo — "explain this codebase", "how does this project work",
  "help me understand this repo", "where do I start", "walk me through the
  architecture", "what does this do". Finds the entry point, traces one real
  request or flow end-to-end, maps the architecture and data, and surfaces the
  riskiest unknowns — without reading every file top to bottom.
---

# Understand Codebase

The way to understand a system fast is not to read all its code — it's to recover its *shape* by
asking a fixed set of questions and tracing one real path through it.

## Workflow — ask these, in roughly this order

1. **What is it, and why?** Read the README and any docs. What problem does it solve, for whom?
2. **How does it start?** Find the entry point (`main`, `run.py`, a server bootstrap, a `CMD`) and
   what supervises it.
3. **Can it run?** Note the setup/run commands — actually running it teaches a lot.
4. **Where's the boundary?** What's the network entry (port, routes, public surface)?
5. **Trace one real flow end-to-end.** Pick a representative request/command and follow it: routing
   → handler → business logic → data access → response. Find the **route table** — it's the map of
   what the system can do.
6. **Where's the data?** Read the schema (keys, foreign keys, constraints) — it encodes the domain.
7. **What does it depend on?** The dependency manifest and config/env — and what external services.
8. **How is it deployed and observed?** Build/deploy scripts, logs/metrics.

## Output

A concise map: what it is, the entry point, the end-to-end path of one flow, the architecture/layers,
the key files to know, and the **riskiest unknowns** (things that are undocumented or surprising).
Trace one path well rather than skimming everything.
