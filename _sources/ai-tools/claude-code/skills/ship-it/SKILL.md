---
name: ship-it
description: >-
  Take a project from "runs on my machine" to deployable in production. Use when
  the user wants to deploy or productionize — "ship this", "set up deployment",
  "how do I deploy this", "get this to production", "deploy to <platform>". Sets up
  the full code-to-production path: a clean Dockerfile, a CI pipeline, externalized
  config/secrets, a health check, and the deploy configuration for the chosen
  target, with rollback in mind.
---

# Ship It

Turn working code into a running, deployable service. Match the target's complexity — don't reach
for Kubernetes when a PaaS will do.

## Workflow

1. **Pick the target with the user** (least to most complex):
   - **PaaS** (Fly.io, Render, Railway) — simplest; a config file + a Dockerfile.
   - **A single VM** — Docker + a systemd unit / compose + a reverse proxy (Nginx) + TLS.
   - **Kubernetes** — only if there's genuinely a fleet of services.
2. **Containerize** — a small, multi-stage, non-root Dockerfile with a HEALTHCHECK and a JSON-array
   CMD (so signals reach PID 1). Add `.dockerignore`. (See the `containerize` skill.)
3. **Externalize configuration** — all config via env vars; secrets via the platform's secret store
   (never in the image or git); a committed `.env.example`.
4. **Add a health/readiness endpoint** so the platform can route around a broken instance.
5. **Set up CI** to build, test, and publish the image on push. (See `setup-ci`.)
6. **Write the deploy config** for the target, and note the **rollback** path (redeploy the previous
   image/tag) — a rollback you haven't thought through isn't a rollback.

## Boundary

This gets it *deployed*. Observability, scaling, and resilience are the next steps — point the user
to `add-observability` and `add-resilience`, and to `codebase-health-check` to see what's next.
