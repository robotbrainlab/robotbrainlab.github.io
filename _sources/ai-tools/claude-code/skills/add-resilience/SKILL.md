---
name: add-resilience
description: >-
  Make a system survive partial failure. Use when the user wants fault tolerance —
  "add retries", "make this resilient", "add a circuit breaker", "handle
  timeouts", "this cascades when <dependency> is down", "make outbound calls
  safe". Adds explicit timeouts, retries with backoff, circuit breakers,
  idempotency, and graceful degradation so one slow or failing dependency doesn't
  take everything down.
---

# Add Resilience

In any system that talks to other systems, partial failure is normal. A single slow dependency,
unhandled, can exhaust your threads and cascade into a full outage. Design for it explicitly.

## What to add

- **Timeouts on every outbound call.** No call should be able to hang forever — that's the most
  common cause of cascading failure. Set explicit connect and read timeouts.
- **Retries with exponential backoff + jitter** — but **only for idempotent operations**. Backoff
  + jitter prevents a "thundering herd" of synchronized retries hammering a recovering service.
- **Idempotency for retryable operations.** A retried request must not double-charge / double-send.
  Use an **idempotency key** so repeating a request returns the original result.
- **Circuit breakers** for a dependency that's known to be failing: stop sending requests for a
  cooldown (fail fast) instead of piling up doomed calls and exhausting the connection pool.
- **Graceful degradation.** When a *non-critical* dependency is down, the core experience should
  still work (serve a cached value, skip the optional enrichment) rather than failing entirely.

## Principle

Assume every network call can be slow, fail, or be retried. The question for each one is "what
happens if this times out, fails, or runs twice?" — and the answer should be "nothing catastrophic."
