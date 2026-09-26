---
name: release
description: >-
  Cut a versioned release: choose the version bump, update the changelog, and tag.
  Use when the user wants to release — "cut a release", "bump the version", "create
  a release", "tag a new version", "update the changelog and release". Chooses the
  right semantic-version bump from the changes, updates the changelog in Keep a
  Changelog style, bumps the manifest version, and creates an annotated tag —
  distinguishing a deploy from a user-visible release.
---

# Release

A release is a named, trackable point in the project's history. Name it well and record what changed,
so anyone can tell what's in it and whether to upgrade.

## Workflow

1. **Review what changed** since the last release (`git log <last-tag>..HEAD`).
2. **Choose the semantic-version bump** — `MAJOR.MINOR.PATCH`:
   - **PATCH** — backward-compatible bug fixes.
   - **MINOR** — backward-compatible new features.
   - **MAJOR** — a breaking change.
   The version is a promise: same MAJOR → won't break callers.
3. **Update `CHANGELOG.md`** (Keep a Changelog): a new `## [x.y.z] — <date>` section with entries
   grouped under **Added / Changed / Deprecated / Removed / Fixed / Security**. Written for humans.
4. **Bump the version** in the manifest (`package.json`, `pyproject.toml`, …).
5. **Tag it** — an annotated git tag (`git tag -a vX.Y.Z -m ...`).
6. **Draft release notes** — a curated, user-facing summary (distinct from the full changelog).

## Note

A **deploy** (code reaches prod) is not the same as a **release** (a change becomes visible to
users); feature flags decouple them. Cutting a version is about the *release*.
