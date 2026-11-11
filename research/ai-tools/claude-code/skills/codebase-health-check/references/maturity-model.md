# The Engineering Maturity Model — staged non-negotiables

Six stages, each managing a category of risk. A project's **stage = the highest stage whose
non-negotiables are all met.** "Nice to have" items don't gate a stage; non-negotiables do.

| Stage | Risk it manages | Headline deliverables |
|---|---|---|
| 1. Foundation | Irreversible early mistakes | Version control, secrets hygiene, linting, README |
| 2. Early Development | Silent failures, no feedback loops | Unit tests, logging, CI, error handling, input validation |
| 3. Growing Codebase | Inability to change safely | Architecture layers, integration tests, code review, ADRs |
| 4. Production Readiness | Inability to operate | Metrics/alerting, deploy automation, rollback, runbooks, E2E |
| 5. Scale & Reliability | Systemic / cascading failure | IaC, circuit breakers, idempotency, tracing, verified backups |
| 6. Excellence | Long-term sustainability | Postmortems, perf testing, data lifecycle, versioning, compliance |

---

## Stage 1 — Foundation  *(day 0, hardest to retrofit)*

Non-negotiables:
- **Version control** — a git repo with a clear branching convention. *Detect:* `.git/`, history.
- **Dependency & environment management** — explicit, **pinned** deps; venv/lockfile/container.
  *Detect:* manifest + lockfile; pinned vs floating versions.
- **README** — what it is, how to run it, how to test it. *Detect:* `README*` exists and is real.
- **`.gitignore` + secrets hygiene** — ignores build artifacts/`.env`; `.env.example` documents
  config; **no secrets in source/history**. *Detect:* `.gitignore`, `.env.example`; grep for keys/
  tokens/passwords committed.
- **Linter + formatter**, enforced (prefer zero-config: Black/ruff, Prettier, gofmt).
  *Detect:* config files (`.prettierrc`, `ruff.toml`, `[tool.black]`, etc.).

*Why first:* these are the only practices where "later" genuinely means "never" — committed
secrets can't be un-leaked; retroactive formatting pollutes history.

## Stage 2 — Early Development

Non-negotiables:
- **Unit tests for business logic** (critical paths + edge cases; not 100% coverage). *Detect:*
  test dir/files, a test runner.
- **Structured logging** at sensible levels (not bare `print`/`console.log`). *Detect:* a logging
  library in use.
- **Basic CI** — install + lint + test on every push/PR. *Detect:* `.github/workflows/`, etc.
- **Explicit error handling** — no silently swallowed exceptions. *Detect:* grep `except:\s*pass`,
  empty `catch {}`.
- **Input validation at boundaries** — external input validated where it enters. *Detect:* a
  validation lib (Pydantic/Zod/Joi) or explicit checks at handlers/CLI.

## Stage 3 — Growing Codebase

Non-negotiables:
- **Architecture with separation of concerns** — logic / data / transport in distinct layers.
- **Integration tests** for the important seams (code ↔ DB, service ↔ dependency).
- **Secrets manager / vault** (beyond passing `.env` around) once a team is involved.
- **Dependency vulnerability scanning** (Dependabot, `pip-audit`, Snyk).
- **Code review process** — required reviews before merge.
- **Architecture Decision Records** — short ADRs for significant choices. *Detect:* `docs/adr/`.

## Stage 4 — Production Readiness

Non-negotiables:
- **Metrics & alerting** — request/error rates, latency percentiles, wired to alerts.
- **Health/readiness endpoints** — `/health`, `/ready`.
- **Automated, repeatable deployment** — one command/pipeline, no manual runbook.
- **Rollback strategy** — a defined, *tested* path back.
- **E2E tests for critical paths** — a few, covering core user journeys.
- **Runbooks** — for foreseeable incidents (down, DB full, stuck job, dependency outage).

## Stage 5 — Scale & Reliability

Non-negotiables:
- **Infrastructure as Code** (Terraform/Pulumi/CloudFormation).
- **Graceful degradation & circuit breakers** — survive a non-critical dependency failing.
- **Idempotency** for retryable operations (payments, emails, jobs).
- **Timeouts, retries with exponential backoff + jitter** on every outbound call.
- **Distributed tracing** (OpenTelemetry) once multiple services exist.
- **Verified backups / DR** — tested restores, known RTO/RPO. Untested backup ≠ backup.

## Stage 6 — Excellence

Practices (high value, need foundational maturity first):
- Blameless **postmortems** as institutional practice.
- **Performance testing** in CI; tracked benchmarks; latency budgets.
- **Data retention & lifecycle policies** (and GDPR/compliance where relevant).
- **API versioning & backward-compatibility** strategy for external consumers.
- **Compliance & auditability** (audit logs distinct from app logs) in regulated domains.
- Knowledge-sharing / **bus-factor** reduction; onboarding time as a tracked metric.

---

## Quick "what stage am I?" heuristic

- Secrets in git, no linter, or no real README → **below/at Stage 1**.
- Foundation solid but no tests/CI or swallows errors → **Stage 2 gap**.
- Tests + CI but a god-object architecture, no reviews/ADRs → **Stage 3 gap**.
- Clean architecture but can't observe/deploy/rollback safely → **Stage 4 gap**.
- Operable but fragile under partial failure / no IaC / unverified backups → **Stage 5 gap**.
- All of the above solid → polishing at **Stage 6**.

Always prioritize unmet **lower-stage** non-negotiables before higher-stage shine.
