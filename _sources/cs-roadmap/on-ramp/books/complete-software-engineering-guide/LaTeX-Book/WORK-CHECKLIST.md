# Book Work Checklist

Everything still to do on the book, in the order we'll do it.
Rules we agreed: backend only (no AI content); each addition goes where the
reader first needs it; no trimming.

---

## Step 1 — The frame: the end-to-end process map

- [x] **Opening chapter, "How Software Gets Built"** (before Part I)
  - The steps from idea to a running system, and what goes into and comes out of each.
  - Who usually does each step (product, design, frontend, backend, testing, operations).
  - The loop: ship, observe, change, ship again. Most work is changing an existing system.
  - Written for a reader who knows none of the topics yet.
- [x] **"You are here" note** at the start of Parts I–IV and of each Stage 1–11, pointing back to the map.
- [x] **Closing chapter, "The Same Process in a Real Team"** (after Chapter 43)
  - The Notes API journey replayed as a team: who owns what, what they hand to each other.
  - Changing a live system: a new feature going through the whole loop.
  - The same map laid over a website, a mobile app, and a data system: what stays the same, what changes.
- [x] Preface, table of contents and part descriptions updated for the new chapters.

## Step 2 — Topic gaps (added inside existing chapters)

- [x] **Databases — Chapter 33** (new sections 33.10–33.14; tested on SQLite and PostgreSQL)
  - [x] Designing tables: keys, constraints, one-to-many, many-to-many, what an index is (33.11, tags feature)
  - [x] Queries across tables: joins, grouping and counting, the "N+1 queries" problem (33.12)
  - [x] Transactions in depth: isolation, lost updates, locking (33.13)
  - [x] Migrations as a system: numbered files, a small migration runner, safe renames (33.10)
  - [x] Raw SQL vs an ORM (33.14)
  - [x] Verified on PostgreSQL 16: all 62 tests, migration flows, 6 concurrent runners (found and fixed a race), the 33.13 race/lock/deadlock/ON CONFLICT/optimistic claims, the 33.12 queries, the Chapter 39 query, the SQLAlchemy example
  - Done when: you can design tables for a new feature and ship a schema change safely.
- [x] **Testing depth — Chapter 17** (new section 17.8; tests added in Chapter 33 done; 37, 38, 41 still to come with those chapters)
  - [x] What to test at which level (unit, integration, end-to-end)
  - [x] Parametrized tests; fakes and mocks, and where to stop mocking; test data builders (factory fixture)
  - [x] Tests that fail at random, and how to fix them; test-first (found and fixed a real bug: NUL characters gave a 500 on PostgreSQL; rule carried into Chapter 31's Validator)
  - Done when: the tests cover normal use, bad input, failures and permissions.
- [x] **Git workflow — Chapter 17** (new section 17.9): branches, commits, pull requests, code review, protected main, merging, revert, release tags
  - Follow-ups: Chapter 16's debugging section must cover `git bisect` (17.9 points to it); Chapter 37's fake email service is referenced from 17.8.
- [x] **Login and permissions — Chapter 38** (new 38.3 Authentication, 38.4 Authorization; old 38.4–38.8 → 38.5–38.9; 84 tests on SQLite + PostgreSQL)
  - [x] Hashed passwords (bcrypt, cost from BCRYPT_ROUNDS); register, login, logout (DELETE /auth/session)
  - [x] Expiring login tokens stored as hashes; JWT / API keys / OAuth compared
  - [x] protect(blueprint) by default; ownership in every query (mutation-tested: all 8 checks covered); 404 rather than 403
  - [x] Login rate limit (Nginx zone "login"); dummy-hash timing equality (measured); password reset (explained)
  - [x] Found and flagged: Chapter 36's Redis cache key must include the owner (warning in 38.4)
  - Done when: tests prove user A cannot read or change user B's notes. ✔
- [x] **Calling another service — Chapter 37** (new 37.5; old 37.5–37.9 → 37.6–37.10; verified end-to-end with Mailpit)
  - [x] "Email this note" endpoint (202 Accepted) calling an email service; app/email.py owns the conversation
  - [x] Connect/read timeouts; "a timeout doesn't mean it failed" (504); safe retries with an idempotency key
  - [x] Retry-After honoured; one log line per call without private data; fake of OUR function + real misbehaving HTTP server in tests
  - [x] Chapter 38 updated: the email query is the ninth ownership check (mutation-tested); auth reuses Validator.require_email
- [x] **Background jobs — Chapter 41** (new 41.5; old 41.5–41.6 → 41.6–41.7; 99 tests on PostgreSQL; end-to-end with a real worker + Mailpit)
  - [x] Email moved into a job (same 202 contract); PostgreSQL job table (0005); worker = same image, second container (--no-healthcheck)
  - [x] SIGTERM graceful stop (exit 0 verified), retries with backoff + max attempts, PermanentError, lease for crashed workers, idempotency key per job, scheduled jobs via run_at
  - [x] Metrics on :9201 (ready, oldest age, failed, processed) and alert rules; compose snippet validated
  - Done when: a crash mid-job neither loses the job nor runs it twice. ✔ (lease + idempotency key)
- [x] **Debugging — Chapter 16** (new 16.10; old 16.10 → 16.11): method, reading a real traceback, breakpoint()/pdb, `git bisect run` (real session captured), production debugging
- [x] **Profiling — section 36.2**: cProfile on the N+1 vs batched listing (real numbers: 2,010 vs 20 queries, 12× faster), py-spy, flame graphs
- [x] **Async Python — section 36.8**: asyncio demo (1.00 s vs 3.03 s with a blocking call), the whole-stack table, why the Notes API stays sync
- [x] **OpenAPI — section 34.10**: openapi.yaml (validated), CI step, contract test (verified it catches a renamed field)
- Also fixed: TOC page-number column widened for 4-digit pages (book passed 1,000 pages)

## Step 3 — Practice

- [x] **Exercises** at the end of every Part IV chapter (43 chapters × 4: predict, break and fix, extend, explain); solutions written (go into the companion repo)
- [x] **Project chapter, "Notes for Many Users"** (Chapter 44; claims measured: search plans, login burst) — reference solution M1–M5 built and tested (190 tests, 90.8% coverage, PostgreSQL)
  - [x] M1 Accounts and ownership
  - [x] M2 Sharing notes, search, trash and restore
  - [x] M3 Email reminders sent by the worker
  - [x] M4 Full test suite, fake email service, OpenAPI spec
  - [x] M5 Production: CI deploys web + worker, metrics, 7 alerts (promtool-checked), a runbook per alert, a load test, game-day plan, postmortem template (load numbers, game day and postmortem need a real server: Level 2)
- [x] **Companion repository** (`notes-api-companion/`, local git): tags `start`, `project-m1` … `project-m5`, then README + 43 exercise-solution files on `main`. Every tag passes lint, mypy, contract and tests on its own fresh database; `make build` passes at `main`
  - Found and fixed on the way: 10 known vulnerabilities in the book's 2024 pins (Flask, Werkzeug, python-dotenv, requests moved to fixed releases); mypy needed `types-requests`; 6 unguarded ownership checks (mutation tool `make mutate`, now 12 of 12 caught); `/tags/{name}/notes` omitted `updated_at` (strict contract); missing certificate-expiry alert; `::1` flakiness (tests default to 127.0.0.1)
  - M3 reminder measured through Mailpit with the real worker: 1 s after due, one email
  - Not pushed to GitHub: that needs your `gh auth login` (Level 3)

## Step 4 — Prerequisite and boundary

- [x] **Appendix G, Python essentials** used by the book (G.1–G.12: modules, arguments, decorators, type hints, strings, comprehensions, exceptions, `with`, classes, generators, standard library, async); listed in the front-matter TOC and the index
- [x] **"Where to go next"**: last section of the closing chapter: deeper data work, the client, Kubernetes/Terraform, managed cloud services, microservices, algorithms and foundations; each with a first project on the Notes API

## Step 5 — Verification

- [x] Tools installed (Docker Desktop, Python 3.11, shellcheck, hadolint, actionlint, act)
- [x] Level 1 — run the book's code locally: app, tests (PostgreSQL), Docker image (API + worker from one image, migrations, health, metrics on 9200/9201, email through Mailpit, SIGTERM exit 0), Nginx config, scripts, promtool
- [ ] Level 2 (optional, needs your server and domain) — a real server: Ubuntu 22.04 droplet, domain (or sslip.io), HTTPS. Everything else is verified locally.
- [x] Level 3, locally with `act` (no GitHub account needed): test job (lint, mypy, contract, 190 tests, coverage, pip-audit) and publish job (image build + smoke test) pass. Not run: the registry push and the deploy job (need GitHub + a server; optional)
- [x] Every code change tested in the working app; book rebuilt with no warnings
- [x] Versions table in the preface updated (bcrypt, requests, prometheus-flask-exporter, openapi-spec-validator, Mailpit) + note that the companion repo keeps pins current; new preface section on exercises, the project and the companion repository
- [x] Final read-through of every changed chapter: automated checks (artifacts in the PDF text, every "section N.M" reference resolves) + seven parallel reviews (opening/closing/project/Appendix G; Ch 16–33; Ch 34–38; Ch 39/41; the exercises of all 43 chapters), claims tested on real tools. About 90 findings, all fixed, including code bugs:
  - `gunicorn.conf.py` metrics hooks crashed without `PROMETHEUS_MULTIPROC_DIR` (book Ch 35 + companion)
  - login with a password over 72 bytes → 500 on newer bcrypt; login 401 lacked `WWW-Authenticate` (Ch 38 + companion)
  - Ch 39 prod-local compose never migrated; Ch 41 didn't show `send_email(idempotency_key=…)`, the jobs TRUNCATE, or the contract change; Ch 33 listings missing imports; Ch 25 systemd timer had an end-of-line comment (invalid)
  - ~45 exercise/solution fixes (forward references, wrong exit statuses, macOS AirPlay on :5000, wrong SKIP LOCKED explanation — re-measured on PostgreSQL, etc.)
  - Companion history rebuilt so every tag carries the fixes; book 1,070 pages, 0 overfull, 0 undefined

---

## Already done

- [x] Deep proofread and all fixes applied (all four parts)
- [x] Part IV's inner parts renamed Stage 1–11
- [x] Integration-contract material moved to section 34.10, "The API as a Contract"
- [x] Part II worked example, "Planning the Notes API"
- [x] Versions and "a book that will age" note in the preface, plus notes in Chapters 17, 21 and 28
