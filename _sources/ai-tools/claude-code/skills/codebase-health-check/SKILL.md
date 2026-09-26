---
name: codebase-health-check
description: >-
  Assess a codebase's engineering maturity and tell the user what to improve next.
  Use this skill whenever the user wants to audit, assess, review the *setup* of, or
  judge the readiness of a repository — e.g. "is this production-ready?", "what is
  this project missing?", "audit/health-check this codebase", "what should we add
  next?", "is our setup any good?", or before a launch/handover. It scans the repo
  for the practices a good codebase should have, determines which maturity stage it
  is at (Foundation → Excellence), names the missing non-negotiables, and returns a
  prioritized roadmap of what to add next and why. This is about the codebase's
  engineering practices and operational readiness, not about reviewing a single
  file's code quality.
---

# Codebase Health Check

Assess where a codebase stands against a six-stage maturity model and tell the user the
*highest-leverage next steps* — not a generic wishlist. The core idea: each stage manages a
different **category of risk**, and skipping ahead doesn't remove work, it defers it under
worse conditions. **The order matters as much as the content.**

## How to run the assessment

1. **Scan the repository.** Detect what's present using files, configs, and structure — do
   not assume. Useful probes (adapt to the stack):
   - `ls -la`, read `README*`, `.gitignore`, `.env.example`, dependency manifests
     (`package.json`, `pyproject.toml`/`requirements.txt`, `go.mod`, …), lockfiles.
   - `git rev-parse` / `git log --oneline -5` (is it under version control? active?).
   - Look for: linter/formatter config; a `tests/` dir or test files; CI config
     (`.github/workflows/`, `.gitlab-ci.yml`, …); logging usage; error handling patterns;
     input validation; architecture layering; ADRs (`docs/adr/`); health-check endpoints;
     deploy scripts/IaC (`Dockerfile`, `terraform/`, …); metrics/observability; runbooks.
   - Grep for tell-tales: `console.log`/`print(` vs a logger; `except: pass`/empty catch;
     hardcoded secrets/keys; `TODO`/`FIXME` density.
2. **Read `references/maturity-model.md`** for the full stage-by-stage non-negotiables and
   their detection hints. (Load it now — it's the substance of this skill.)
3. **Determine the current stage:** the highest stage whose **non-negotiables are all met**.
   A project with great tests but secrets in git is still stuck at Stage 1 — non-negotiables
   are gates, not points.
4. **Identify the gaps:** the unmet non-negotiables at the current stage *and* the next one.
5. **Prioritize.** Recommend the next 3–6 additions, ordered by leverage. Favor anything
   that "later means never" (secrets hygiene, version control, formatting) and anything that
   unblocks a feedback loop (tests + CI). Explain *why now* for each.

## Output format

```
## Codebase health check — <repo name>

**Current stage: <N> — <stage name>**  <one line on what that means / what risk is managed>

### What's in place ✅
- <present practices, grouped>

### Missing at this stage / the next (gaps)
- ❌ **<practice>** — <what it is, why its absence is a risk here>

### Do next (prioritized)
1. **<highest-leverage thing>** — <concrete action> · *why now:* <reason>
2. ...

**Don't over-invest yet:** <practices that would be premature at this stage, so the user
doesn't gold-plate ahead of need>
```

Two judgment notes that keep this honest and useful:
- **Don't recommend Stage 5 things to a Stage 2 project.** Distributed tracing on a prototype
  is waste. Match advice to where they actually are.
- **A health check is a diagnosis, not a lecture.** Give them the few moves that matter most
  right now, with the reasoning, and stop.
