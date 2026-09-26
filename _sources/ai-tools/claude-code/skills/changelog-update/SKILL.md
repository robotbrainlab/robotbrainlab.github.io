---
name: changelog-update
description: >-
  Update CHANGELOG.md from recent changes. Use when the user wants the changelog
  maintained — "update the changelog", "add this to the changelog", "generate a
  changelog from recent commits", "what changed since the last release". Translates
  recent commits into human-readable, user-facing entries sorted into Keep a
  Changelog categories — written for people deciding whether to upgrade, not for
  tooling.
---

# Changelog Update

A changelog is for *humans* — users and teammates deciding what's new and whether to upgrade. That
makes it different from the git log (which is for and by tooling): it's curated, plain-language, and
grouped by what kind of change it is.

## Workflow

1. **Gather** the changes since the last changelog entry/release (`git log <last-tag>..HEAD`).
2. **Translate to user-facing language.** Rewrite commit messages into clear entries a user would
   understand — describe the effect, not the implementation. Drop pure-internal noise (refactors with
   no visible effect, CI tweaks) unless they matter to consumers.
3. **Sort into Keep a Changelog headings:** **Added · Changed · Deprecated · Removed · Fixed ·
   Security.**
4. **Place** them under an `## [Unreleased]` section (or a new `## [x.y.z] — <date>` if cutting a
   release — see the `release` skill).

## Format

```markdown
## [Unreleased]
### Added
- Cursor-based pagination on the notes list endpoint.
### Fixed
- Malformed request bodies now return 400 instead of 500.
### Security
- Session secret rotated; pre-existing sessions invalidated.
```

Keep entries short, concrete, and about the change's *effect* on the user.
