# Project documentation templates

Instantiate the relevant one(s). Fill every section from real context; mark genuine unknowns with
`> [DECIDE: ...]`. These are starting structures, not straitjackets — drop sections that don't apply.

---

## Problem Statement & Goals  *(design-time)*

```markdown
# <Project / Feature> — Problem Statement

## Background & Context
<Why now? What situation/system/workflow does this plug into? What triggered it?>

## Core Problem
<The specific problem, stated as a problem (not a solution), in 1–2 sentences.
Who is affected, how often, and what it costs them.>

## Goals & Success Criteria
- <Goal> — success when <observable, ideally measurable condition>.
- ...

## Out of Scope
- <What this explicitly does NOT cover, and why ("not yet" vs "never").>

## Stakeholders & Users
- Primary users: <who interacts daily>
- Owners/maintainers: <who runs it>
- Decision-makers: <who has final say>

## Constraints & Assumptions
- **Constraints (hard):** <platform, legal, budget, timeline, team>
- **Assumptions (true-until-false):** <what would change the design if wrong>
```

## Architecture & Design  *(design-time)*

```markdown
# <Project> — Architecture & Design

## System Overview
<3–5 sentences: trigger → processing → output. How it exists as a running process.>

## Architecture Diagram
<An ASCII diagram is fine — components, arrows, external systems, storage, APIs.>

## Component Breakdown
| Component | Single responsibility | Inputs | Outputs | Depends on |
|---|---|---|---|---|

## Data Flow
<The journey of data from source to destination, incl. the error paths.>

## External Integrations
<Each external dependency: purpose, auth method, failure mode, the contract.>

## Data Storage & Schema
<Each store: type, key entities/relationships, indexing, retention.>

## Key Design Decisions
<Significant choices + why. Link to ADRs for the big ones.>

## Security Considerations
<AuthN, authZ, secrets, transport, input validation, data sensitivity.>
```

## Architecture Decision Record (ADR)  *(design-time, `docs/adr/NNNN-title.md`)*

```markdown
# ADR-NNNN: <decision in one line>

Status: Proposed | Accepted (<date>) | Deprecated | Superseded by ADR-XXXX

## Context
<The forces that make this decision necessary, written so it still makes sense in two years.>

## Decision
We will <the choice, in active voice>.

## Consequences
+ <What gets easier.>
- <What gets harder — the downside we're knowingly accepting.>

## Alternatives considered
- <Option> — rejected because <reason>.  (← often the most valuable section)
```

## Developer Guide  *(living)*

```markdown
# <Project> — Developer Guide

## Prerequisites
<Runtime + version, package manager, system libs, credentials, how to verify each.>

## Setup
<Clone → isolated env → install → configure (.env) → migrate/seed → smoke test.>

## Running locally
<Dev command, prod-like command, ports/URLs, how to verify it's healthy.>

## Configuration reference
| Variable | Required? | Default | Description |
|---|---|---|---|

## Testing
<How to run the full suite, a single test, and how to add one.>

## Repository structure
<Top-level layout and where things live.>
```

## Operational Guide  *(living)*

```markdown
# <Project> — Operational Guide

## Deployment
<Build → artifact → infra → release strategy → rollback.>

## Monitoring & Health
<Health endpoints, key metrics/alerts (the four golden signals), where the logs are.>

## Common Failure Modes
| Symptom | Likely cause | Diagnose with | Recovery |
|---|---|---|---|

## Restart & Recovery (runbook)
<Assess → stop → fix → restart (exact command) → verify.>

## Data Management
<Retention, backups (and restore testing), PII handling, deletion.>
```

## Changelog  *(living, `CHANGELOG.md`)*

```markdown
# Changelog
All notable changes, newest first. Semantic versioning (major.minor.patch).

## [1.1.0] — <date>
### Added
- <user-visible change>
### Fixed
- <bug fix>
### Security
- <security-relevant change>
```
*(Distinguish a **deploy** (code reaches prod) from a **release** (change becomes visible to users);
feature flags decouple them.)*
