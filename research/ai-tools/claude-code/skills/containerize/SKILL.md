---
name: containerize
description: >-
  Write a clean, production-grade Dockerfile (and compose for local deps). Use when
  the user wants to containerize an app — "write a Dockerfile", "containerize
  this", "dockerize the app", "add docker-compose", "make a container image".
  Produces a small, secure, multi-stage Dockerfile with layer caching, a non-root
  user, and a healthcheck — plus a compose file for local dependencies.
---

# Containerize

A good image is small, secure, reproducible, and cache-friendly. A naive one is huge, runs as root,
and rebuilds everything on every code change.

## Dockerfile checklist

- **Slim base image** (e.g. `python:3.12-slim`, `node:20-alpine`, distroless) — not the full OS.
- **Multi-stage build:** compile/install in a builder stage; copy only the artifacts into a slim
  runtime stage. Keeps the final image small and free of build tools.
- **Layer order for caching:** copy the dependency manifest and install deps *before* copying source,
  so a code change doesn't bust the dependency layer.
- **Run as a non-root user** (create one; `USER app`). Containers as root are an avoidable risk.
- **`HEALTHCHECK`** so orchestrators know if the container is actually healthy.
- **JSON-array `CMD`/`ENTRYPOINT`** (`["gunicorn", ...]`) so the process is PID 1 and receives
  signals (graceful shutdown). Shell-form CMD swallows signals.
- **`.dockerignore`** excluding `.git`, `node_modules`, `.env`, caches, tests.
- **Config via env vars**, never baked in; never copy secrets into the image.

## Compose for local dependencies

Provide a `docker-compose.yml` that runs the app alongside its local deps (database, cache) so a
contributor gets a working stack with one command.
