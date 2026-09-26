<div align="justify">

# Site Generator

Builds the learner site in [site/](../site) from canonical Markdown sources. Generated HTML is disposable presentation: canonical Markdown always takes precedence.

The site has three areas: **Learn** — the learning guide, one page per step, from [LEARNING-GUIDE.md](../LEARNING-GUIDE.md); **Evidence** — the research reports; and **About** — the curriculum specification (`ROADMAP.md`), project, governance, maintenance and design records. Why the learner experience is a guide rather than the specification is recorded in [design/learner-guide.md](../design/learner-guide.md).

## Build

```bash
python3 -m venv .venv && .venv/bin/pip install -r scripts/requirements.txt
.venv/bin/python scripts/build_site.py
```

Then open `site/index.html`, or serve the directory:

```bash
cd site && python3 -m http.server 8765
```

The build fails without writing `site/` if validation reports an error. Rebuild after any change to a canonical Markdown file.

## What is generated

| Page | Source |
| --- | --- |
| `index.html` — Home | `README.md` (title, lead), `LEARNING-GUIDE.md` (parts and steps) |
| `learn/index.html` — how the guide works, and the whole path | `LEARNING-GUIDE.md` |
| `learn/<step>/index.html` — one page per step and checkpoint | `LEARNING-GUIDE.md` |
| `learn/modern-ai-engineering/index.html` — Modern AI Engineering, the fifth section inside Learn (a parallel track, not a depth level) | `LEARNING-GUIDE.md` |
| `learn/<topic>/index.html` — one page per Modern AI Engineering topic | `LEARNING-GUIDE.md` |
| `evidence/current-practice/index.html` — the current-practice register | `reviews/modern-practice-register.md` |
| `about/curriculum/index.html` — the curriculum specification | `ROADMAP.md` |
| `research/index.html` and one page per report | `research/*.md` |
| `reviews/index.html` and one page per review report | `MAINTENANCE.md`, `reviews/maintenance-state.json`, `reviews/*.md` |
| `about/index.html` and one page per document | `README.md`, `PROJECT-STATE.md`, `AGENTS.md`, `MAINTENANCE.md`, `prompts/`, `design/`, `history/` |
| `404.html` | — |

New files under `research/`, `reviews/`, `design/`, `prompts/` and `history/` are discovered automatically through the routes in `site.toml`.

## Layout

| Path | Role |
| --- | --- |
| `build_site.py` | Entry point |
| `site.toml` | Presentation configuration: source → page routes, areas and navigation order, document-kind markers, the canonical labels the presentation keys on. No curriculum content. |
| `sitegen/build.py` | Pipeline: discover → parse → extract → navigate → render → compose → validate → write |
| `sitegen/markdown.py` | Parsing, document model and presentation rendering rules |
| `sitegen/guide.py` | Reads the learner guide's parts, steps and Modern topics, and checks the guide against `ROADMAP.md` |
| `sitegen/provenance.py` | Traces learner-facing claims: Modern topics to the current-practice register, register entries to their evidence, consulted references to the register, and ROADMAP.md to its accepted protected fingerprint |
| `sitegen/extract.py` | Reads explicitly recorded structure: the architecture diagram, report metadata, the Dependency Map, tables and labelled paragraphs |
| `sitegen/slugs.py` | GitHub-compatible heading anchors |
| `sitegen/validate.py` | Build checks, including wording and structure preservation |
| `sitegen/templates/` | HTML structure only |
| `sitegen/assets/` | CSS tokens and styles, progressive-enhancement JavaScript, vendored Mermaid |

## Rules this generator follows

- It never decides curriculum. Steps, resources and dates are read from canonical files, or are left out.
- The guide must correspond to the specification. The build fails unless every block, phase and readiness gate in `ROADMAP.md` is delivered by a guide step or Modern AI Engineering topic (declared in hidden `<!-- covers: -->` markers; §7 phases are checked capability by capability); every assigned resource appears in the step that delivers its block; every extension, specialization and frontier is named; every prerequisite comes earlier in the path; and no internal identifier (E1, F2, EX4 …) is visible on a learner page.
- The guide follows the reading plan in `ROADMAP.md` §14. Each book the plan marks **Complete** must be introduced exactly once, as a complete book, where the plan begins it; later steps may only **revisit** it, and earlier steps may only **read first** a declared excerpt. The books the owner approved for complete reading are listed in `site.toml` (`required_complete`) and must stay Complete. Blanket "not whole books" wording is rejected on learner pages.
- A unit's contents is generated, never hand-maintained. Each unit's `####` areas and `#####` concepts become the page's sections, and the "In this unit" contents is built from those headings, so entries, order and anchors cannot drift; the build fails if they do, if the contents is duplicated, or if it appears after the reading.
- Learning units explain themselves before they assign reading. The build fails unless each unit opens with why it exists, says where the learner is, organizes its subject as named concept areas, connects them, places them in the learner's picture of AI, states capability-based readiness and says why the next unit follows; unless a unit with two or more sources carries a concept-to-resource map naming only assigned or registered resources; and unless every stage introduction states what the stage asks and what it develops; and unless each unit carries a concept hierarchy of at least three areas with at least two concepts each, every concept saying where it is studied, and no area or concept named after a resource (the hierarchy belongs to the curriculum, not to a book). Units that legitimately have no hierarchy are listed in `site.toml` (`no_hierarchy`).
- Learner-facing claims keep their provenance. Each Modern topic declares the register entries it teaches (`<!-- practice: -->`); only Current Practice and Established entries may be taught; every register entry's evidence IDs must exist in the reports it links; every reference a topic **consult**s must be in the register; wording that claims adoption or consensus without evidence (`overclaim_phrases`) is rejected; and ROADMAP.md may differ from its accepted fingerprint only in the §7 current-practice column that the 4-week scan maintains. Whether a sentence says more than its source is reviewed by hand and recorded in `design/learner-guide.md` §10.
- It never changes canonical wording. For every document and every guide step, validation compares the words of the source with the words of the rendered page, in order; documents are also checked for headings, tables, lists, quotes, diagrams, code blocks, rules and links. Composed pages (Home and the landings) may only present words that exist in their sources.
- Interface text is marked `data-chrome`: navigation, markers, labels, panels and controls. Validation excludes it from content and checks it for stale status wording.
- It never links to pages that do not exist. Links to files outside the site render as plain text.
- It fetches nothing at build or read time. Mermaid is vendored under `sitegen/assets/vendor/`. There is no search.

</div>
