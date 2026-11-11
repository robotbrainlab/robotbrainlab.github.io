---
name: add-observability
description: >-
  Make a running system observable — add structured logging, key metrics, health
  checks, and request correlation. Use when the user wants to instrument code or
  can't see what's happening — "add logging", "add observability/metrics", "add a
  health check", "instrument this", "I can't tell what's going on in production".
  Wires in the three pillars so the system can be operated, not just run, without
  drowning in noise.
---

# Add Observability

You cannot operate what you cannot see. The goal is to answer "is it healthy? what's slow? what
broke?" from signals, before users complain — without logging so much that nothing is findable.

## What to add

**Structured logging**
- JSON (or key-value) logs, not bare `print`/`console.log`, using the stack's logging library.
- Correct **levels**: DEBUG (tracing) · INFO (normal milestones) · WARN (recoverable anomaly) ·
  ERROR (failure) · CRITICAL (process-ending).
- A **request/correlation ID** threaded through a request so its logs can be tied together.
- **Never log secrets or PII** (tokens, passwords, full card numbers, note contents).

**Metrics (the four golden signals)**
- **Latency** (percentiles, not averages), **Traffic** (request rate), **Errors** (error rate),
  **Saturation** (queue depth, resource use). Expose as counters / gauges / histograms via the
  stack's metrics library (Prometheus client, etc.).

**Health checks**
- A shallow `/health` (is the process up and serving?) and, where useful, a deeper `/ready`
  (can it reach its dependencies?) so load balancers/orchestrators route around broken instances.

## Principle

Log too much and the one line that matters is unfindable; log too little and you're blind. Instrument
the **significant** operations, errors, and state transitions — and make every log greppable by
request ID.
