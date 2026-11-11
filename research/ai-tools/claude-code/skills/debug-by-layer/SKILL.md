---
name: debug-by-layer
description: >-
  Diagnose a failure by localizing it to a layer before changing any code. Use
  when something is broken — "debug this", "why is X failing", "this isn't
  working", "production is erroring", "figure out what's wrong". Instead of poking
  randomly, it bisects the system (client → DNS → proxy → app → database), runs the
  right diagnostic for the suspect layer, forms a hypothesis, and tests the
  cheapest one first — then fixes the root cause and adds a regression test.
---

# Debug by Layer

The fastest debugging isn't cleverness — it's **localizing the failure to a layer** before touching
code. Most wasted debugging time is spent changing things at random in the wrong layer.

## Workflow

1. **Get the exact symptom** — the precise error message, stack trace, status code, and what the
   user did. "It's broken" is not enough to start.
2. **Localize to a layer** by asking, in order: did the request even *arrive* (network / DNS /
   reverse proxy)? did it reach the *app* (access logs)? did it fail in *logic* (app logs / stack
   trace)? did it fail at the *database* (connection, query, lock)? The error and logs tell you
   where to look — bisect, don't guess.
3. **Run the right diagnostic for that layer:**
   - Network/DNS: `curl -v`, `dig`, `ping`, check the port.
   - Reverse proxy: its access/error logs and config.
   - App: structured logs filtered by request ID, the stack trace, a debugger/breakpoint, `strace`.
   - Database: can you connect? the slow/failing query, locks, connection-pool exhaustion.
4. **Hypothesize and test cheaply.** Form one hypothesis, test the cheapest one first, narrow.
5. **Fix the root cause** (not the symptom) and **add a regression test** so it can't silently return.

## Principle

Identify *which layer* it's in within a couple of minutes, with a diagnostic command ready — then
investigate there. Random code changes in the wrong layer are how hours disappear.
