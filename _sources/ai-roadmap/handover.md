# Handover

This file describes what this project is, where it stands **right now**, and what to do next.
It is a starting point, not a substitute for reading the repository.

---

## 0. Instructions for the new session — read before changing anything

Please perform a complete and thorough manual review of the entire repository.

Do not rely on automated searches, keyword lookups, pattern matching, summaries, or selective file
inspection as a substitute for understanding the codebase. Systematically open and review every
relevant file in the repository from beginning to end.

Read the implementation carefully, line by line, and make sure you fully understand how each
component works, how the files interact with one another, and how data and execution flow through
the application.

Do not skip sections because they appear repetitive, straightforward, or unrelated at first glance.
Review the actual implementation rather than making assumptions based on filenames, function names,
documentation, the contents of this handover, or previous context.

Where functionality spans multiple files, trace it across those files. Follow imports, calls,
dependencies, state changes, data transformations, configuration, and execution paths as necessary
to understand how the system actually works end to end.

The objective is to build a complete end-to-end understanding of the repository before continuing
the work described here.

Do not treat `handover.md` as a substitute for reviewing the codebase. It exists to explain the
project's current state and where work stopped, while the repository itself remains the source of
truth for how the system actually works.

Important implementation details, dependencies, edge cases, configuration behaviour, and
interactions between components must not be overlooked. Prioritise completeness and accuracy over
speed. Take whatever review steps are necessary to ensure the entire relevant codebase has genuinely
been examined before proceeding.

Only after completing that review should you use the current-state information and next steps below
to continue development.

**Suggested review order** (the whole repository still needs reading; this is only an efficient
sequence): `AGENTS.md` → `MAINTENANCE.md` → `ROADMAP.md` → `LEARNING-GUIDE.md` → `materials/*.md` →
`scripts/site.toml` → `scripts/sitegen/*.py` (`build.py`, `guide.py`, `markdown.py`, `validate.py`,
`provenance.py`, `extract.py`, `slugs.py`) → `scripts/sitegen/templates/` and `assets/` →
`design/*.md` → `research/*.md` and `reviews/*.md` → `PROJECT-STATE.md`.

---

## 1. What this project is

An evidence-based **learning roadmap for an AI Engineer (Data & Intelligence)**: what to study, in
what order, from which resources, what to build, and how to know you are ready to move on. A
separate, future **Computer Science & Engineering** roadmap is intended to cover general computing;
this repository deliberately excludes it and declares such topics as prerequisites instead.

It is a content repository with a small static-site generator, not an application. There is no
runtime service, no database and no user data. The deliverables are:

- a curriculum specification (`ROADMAP.md`),
- a learner-facing presentation of it (`LEARNING-GUIDE.md`),
- curriculum-authored learning materials (`materials/`),
- a generated static website (`site/`),
- the research, design and maintenance records that justify all of it.

### The curriculum's shape (accepted; do not redesign)

- **Depth path** — 19 numbered steps across four levels: Fundamentals → Advanced → Mastery →
  Research, with three checkpoints between them.
- **Modern AI Engineering** — a *parallel* curriculum of 9 topics covering current engineering
  practice. It is not a fifth level and does not come after Research.
- The two dimensions are presented as **one chronological journey**: each topic has an opening
  condition, a status (**Required**, **Recommended**, **Available**), and a stated return point on
  the numbered path.

---

## 2. How to build and check it

```bash
# environment (Python 3.14, deps pinned)
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt

# build + validate, replacing site/
.venv/bin/python scripts/build_site.py

# build + validate into a throwaway directory (does not touch site/)
.venv/bin/python scripts/build_site.py --out /tmp/check-site
```

The build validates first and **refuses to replace `site/` if any check fails**. Current state:

```
Generated 72 pages from 35 canonical documents (22 learner-guide pages)
Validation: 1461 passed, 0 warnings, 0 errors
```

`site/` is generated output. **Never edit it by hand** — edit the canonical Markdown or the
generator and rebuild.

There is **no git repository here**. Changes are immediate and unversioned; be correspondingly
careful, and prefer writing to a scratch directory when experimenting.

---

## 3. Repository map

| Path | What it is |
| --- | --- |
| `ROADMAP.md` | The accepted curriculum specification, **Baseline 2** (accepted 2026-09-19). Protected — see §6 |
| `LEARNING-GUIDE.md` | The learner's presentation of the curriculum (~3,800 lines). The main content file |
| `materials/` | 13 curriculum-authored learning materials (notes, exercises, simulations, labs, cases, a checklist, a rubric). Learner-facing |
| `scripts/` | The static-site generator (`build_site.py`, `sitegen/`, `site.toml`, templates, CSS/JS assets) |
| `site/` | Generated website (72 pages). Output only |
| `research/` | Six dated evidence reports (landscape, comparison, coverage audits, independence audit, targeted resource research) |
| `reviews/` | Maintenance records: the current-practice register, the 4-week scan, a learner-experience review, `maintenance-state.json` |
| `design/` | Design records: curriculum proposal, learner-guide record (§§1–15), site architecture, content-fidelity audit |
| `history/` | Immutable superseded baselines (v0, Baseline 1). Never edit |
| `AGENTS.md` | Governance: the constitution for how agents may operate on this repository |
| `MAINTENANCE.md` | The maintenance procedure (4-week Modern AI scan, 12-week curriculum review) |
| `PROJECT-STATE.md` | Checkpoint summary of project status (also a site page) |
| `prompts/` | Methodology records (research prompts) |
| `site.zip` | A stale distribution artefact — see §7 |

### The generator, briefly (verify by reading it)

`scripts/build_site.py` is a thin entry point; everything lives in `scripts/sitegen/`:

- `build.py` — `SiteBuilder`: discovers canonical sources via routes in `site.toml`, builds pages,
  composes the learner journey, and runs validation.
- `guide.py` — parses `LEARNING-GUIDE.md` into parts, steps, checkpoints, Modern topics, unit
  concept hierarchies; holds most curriculum-structure checks.
- `markdown.py` — the markdown-it renderer and link resolution.
- `validate.py` — site-level checks (structure, wording preservation, links, typography policy…).
- `provenance.py` — current-practice register parsing and the ROADMAP protected fingerprint.
- `extract.py`, `slugs.py` — table/section extraction and slug rules.
- `templates/`, `assets/` — Jinja2 templates and the site's CSS/JS.

Configuration (routes, labels, validation parameters, expected sequence, protected hash) is in
`scripts/site.toml`. Much validation behaviour is data-driven from that file.

---

## 4. Current state — what is complete and working

Everything below is implemented, validated and visible on the generated site.

1. **Curriculum** — Baseline 2 accepted; 19 Depth steps, 3 checkpoints, 9 Modern topics, 32
   mandatory resources with an explicit reading plan.
2. **Learner guide** — every unit is a self-explaining mini-chapter: plain-language opening, *Where
   you are*, a generated hierarchical contents block, a two-level concept hierarchy (**115 areas /
   320 concepts**), *How these ideas connect*, *Where this fits in AI*, resources with roles,
   concept-to-resource map, practice, capability-based readiness, and a transition.
3. **One journey** — Modern topics declare status and return point; the six Depth steps where topics
   open announce them; the site's Previous/Next pager walks the interleaved order; a quiet skip
   route is offered past detours the path does not depend on.
4. **Explanations** — every unit defines its subject before announcing what it teaches; first-use
   vocabulary is glossed; 8 conceptual diagrams; the explanation boundary is stated to the learner
   ("the roadmap gives a foothold, the resources teach").
5. **Curriculum materials** — all 13 promised materials exist in `materials/`, are linked from the
   units that need them, and the 6 with Python were executed successfully (standard library only,
   seeded, no API keys).
6. **Site** — 72 pages, three areas (Learn · Evidence · About), dark reading theme, unit contents,
   responsive layout, scoped typography policy, versioned assets.
7. **Provenance and governance** — Modern topics trace to the current-practice register (49 entries,
   38 teachable); ROADMAP integrity is enforced by a protected fingerprint; the maintenance cadence
   is recorded in `reviews/maintenance-state.json`.

**Nothing is mid-edit.** There is no partially written file, no half-applied refactor and no
failing check in the repository as it stands.

---

## 5. Where we stopped

The most recent completed work was the **curriculum-authored materials pass**: writing the 13
materials, integrating them into the guide (replacing every "planned material" citation and removing
the interim fallbacks), adding two build checks (every material is linked from the guide; the Python
in every material parses), and recording the pass in `design/learner-guide.md` §15 and
`PROJECT-STATE.md`.

The build passes (1461 checks) and the deliberate-failure suite passed (51 cases, all rejected).

---

## 6. Constraints and assumptions that must be preserved

These are live rules, not history. Breaking one will either fail the build or violate governance.

1. **Canonical hierarchy.** `research/` (evidence) → `design/` (reasoning) → `ROADMAP.md`
   (decision) → `LEARNING-GUIDE.md` (presentation) → `site/` (generated). Lower layers never
   redefine higher ones.
2. **`ROADMAP.md` is protected.** `scripts/site.toml` holds `roadmap_protected_sha256`: the SHA-256
   of `ROADMAP.md` with only the §7 *current-practice* column blanked. Only the 4-week scan may edit
   that column. Any other change fails the build and requires an accepted curriculum change under
   `AGENTS.md` / `MAINTENANCE.md` §6 (human approval).
3. **`history/` is immutable.**
4. **No new resources** without a demonstrated gap and owner approval; the portfolio and reading
   plan are accepted.
5. **Architecture is frozen**: the 19-step sequence, four depth levels, Modern as a parallel
   dimension with its 9 topics, the checkpoints, capability-based readiness, the single evolving
   system, the provenance/maturity model and the maintenance cadence.
6. **Typography policy (current).** Long-form prose is justified in the content column and ragged
   right below 48 em; headings, navigation, labels, tables, controls, code and diagram text are
   never justified. The earlier "justify everything" rule is superseded. Enforced by
   `typography_policy` in `validate.py` against `justified_selectors` in `site.toml`.
7. **Learner-facing pages carry no internal identifiers** (block IDs like `E10`, `F2`, `MP-12`).
8. **Evidence discipline.** Contemporary claims are marked settled / current practice / contested
   and traced to `research/` or the register. No unsupported adoption claims (an overclaim lint
   enforces a phrase list).
9. **Stale wording guards.** Phrases such as `planned material` and `(planned)` now fail the build
   if they reappear on a learner page.

---

## 7. Known issues, limitations and open items

Ordered roughly by how much they matter for continuing work.

1. **The deliberate-failure suite is not in the repository.** It lives only in the previous
   session's scratchpad (`failure_tests.py`, 51 cases). It copies the repo to a temp directory,
   mutates one thing per case (a curriculum rule, an orchestration fact, a typography policy, a
   material) and asserts the build rejects it, plus a positive control (an authorised §7
   current-practice edit must still pass). **It will be lost.** Re-creating it inside the repository
   is the highest-value continuity task.
2. **Two stale counts.** `design/learner-guide.md` §11 and the corresponding `PROJECT-STATE.md` row
   say "113 areas, 312 concepts"; the actual figures are **115 areas / 320 concepts**.
3. **`site.zip` is stale** (dated 2026-09-19, predating several passes). Regenerate it or delete it.
4. **Ten dead links on one archived page.** `history/roadmap-baseline-1.md` uses repo-root-relative
   links from inside `history/`, so the generator renders them as plain text and reports them. The
   file is immutable, so the fix belongs in link resolution, not the source.
5. **F6 (step 14, Advanced Retrieval and Ranking) has no dedicated resource.** Disclosed to the
   learner and recorded in `ROADMAP.md` §16. Resolving it is a curriculum change needing research
   and owner approval.
6. **Two reading proposals await owner approval** (`reviews/2026-09-20-learner-experience-review.md`
   §4): read Piech complete; read *Computational and Inferential Thinking* ch 14 whole. Not
   implemented.
7. **Five register entries queued for the 12-week review** (`reviews/modern-practice-register.md`
   §4), including three teachable-but-untaught practices (durable execution, multimodal model use,
   coding assistants).
8. **`ROADMAP.md` §11 row 1** describes one "case set" spanning framing and release decisions; the
   materials implement these as two documents. Recorded, not reconciled — reconciling it would edit
   the protected specification.
9. **Material limitations by design**: the case sets have no answer keys (they are judgment
   exercises), and the agent-loop exercise ships a deliberately crude stand-in for the model that
   the learner is meant to replace.
10. **Unverifiable resource details**: some page ranges come from official tables of contents rather
    than book bodies; noted in `ROADMAP.md` §16.

---

## 8. Maintenance schedule (dates matter)

From `reviews/maintenance-state.json`:

- Baseline 2, accepted 2026-09-19.
- Last 4-week Modern AI scan: 2026-09-19. **Next due: 2026-10-17.**
- Last curriculum review: 2026-09-18. **Next due: 2026-12-11.**

The procedure for both is in `MAINTENANCE.md`. A scan may edit only the §7 current-practice column
plus the register, the scan report and the state file.

---

## 9. What to work on next

No task is forced; pick with the owner. Suggested order:

**A. Put the deliberate-failure suite in the repository** *(recommended first)*
Create it under `scripts/` (for example `scripts/failure_tests.py`) with a documented way to run it.
Each case should mutate one canonical fact or generator behaviour in a throwaway copy and assert the
build rejects it with a specific message, plus the positive control described in §7.1. Without this,
the repository's validation can regress silently.

**B. Small integrity fixes**
Correct the two stale counts (§7.2); regenerate or remove `site.zip` (§7.3); teach link resolution
about root-relative links inside `history/` (§7.4).

**C. Owner decisions, then implementation**
The two reading proposals (§7.6). Both change assigned reading, so they need approval before any
edit to `ROADMAP.md`.

**D. Scheduled maintenance when due**
The 4-week Modern AI scan on 2026-10-17, following `MAINTENANCE.md`.

**E. Larger curriculum work (needs evidence and approval)**
The F6 resource gap (§7.5) and the queued register questions (§7.7).

---

## 10. Verification checklist for the new session

After your repository review, confirm these against the code rather than trusting this file:

- [ ] `.venv/bin/python scripts/build_site.py --out /tmp/check-site` → 1461 checks, 0 errors.
- [ ] `ROADMAP.md`'s protected fingerprint still matches `roadmap_protected_sha256` in
      `scripts/site.toml`.
- [ ] `history/` md5s unchanged (`39901e28…`, `52614141…`).
- [ ] 13 files in `materials/`, each linked from `LEARNING-GUIDE.md`, each Python block parsing.
- [ ] The Learn sidebar shows two tracks; the pager walks the interleaved journey from step 1 to
      step 19.
- [ ] No learner page contains internal identifiers or the phrase "planned material".

Then state plainly where this handover was accurate, where it was wrong, and what you found that it
does not mention.
