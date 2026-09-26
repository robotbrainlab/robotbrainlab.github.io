---
name: upgrade-dependencies
description: >-
  Audit and upgrade a project's dependencies safely. Use when the user wants to
  update packages or check for vulnerabilities — "upgrade dependencies", "update
  the packages", "are there any CVEs / vulnerabilities", "bump the libraries", "we
  are on old versions". Audits for known vulnerabilities and staleness, then
  upgrades incrementally — reading changelogs for breaking changes and running
  tests after each step, never bulk-upgrading and hoping.
---

# Upgrade Dependencies

Every library you depend on is a liability you inherit — its bugs, its CVEs, its breaking changes.
Keep them current, but upgrade *deliberately*, because a careless bulk bump is how a working project
breaks all at once.

## Workflow

1. **Audit.** Run the ecosystem's tools: a vulnerability scan (`npm audit`, `pip-audit`, Dependabot)
   and an "outdated" report. You need both the *security* picture and the *staleness* picture.
2. **Prioritize.** Security fixes first. Then majors that actually matter (deprecations, EOL). Leave
   stable, low-value packages alone — "newer" isn't a goal.
3. **Upgrade incrementally.** One significant package (or a batch of safe patch bumps) at a time:
   - read its **changelog/migration notes** for breaking changes,
   - apply any required code changes,
   - **run the test suite**, and commit that upgrade on its own.
4. **Handle majors carefully** — expect API changes; fix them with the migration guide open. (For a
   large framework jump, treat it as a migration — see the `migrate` skill.)

## Principle

Small, verified, one-at-a-time upgrades with tests after each are recoverable; a single "update
everything" commit that breaks the build is a debugging nightmare with no obvious culprit.
