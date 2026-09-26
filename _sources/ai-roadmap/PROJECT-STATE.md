<div align="justify">

# Project State

| | |
| --- | --- |
| **Updated** | 2026-09-21 |
| **Status** | **Baseline 2 accepted (2026-09-19). Learner guide and site current. Repository is in maintenance mode.** |
| **Next action** | Learn from the guide. Maintenance runs on the schedule in [reviews/maintenance-state.json](reviews/maintenance-state.json); the next 4-week Modern AI Scan is due 2026-10-17 |

This is a checkpoint for any future session. It summarizes; the linked files are authoritative. If this file and a canonical file disagree, the canonical file wins — see [AGENTS.md — Canonical Truth Hierarchy](AGENTS.md#canonical-truth-hierarchy).

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Current Status](#1-current-status)
2. [Canonical Files](#2-canonical-files)
3. [Curriculum Architecture](#3-curriculum-architecture)
4. [Completed Evidence and Design Work](#4-completed-evidence-and-design-work)
5. [Key Settled Decisions](#5-key-settled-decisions)
6. [Resource Status](#6-resource-status)
7. [Maintenance System](#7-maintenance-system)
8. [Non-Blocking Uncertainties](#8-non-blocking-uncertainties)
9. [Current File Responsibilities](#9-current-file-responsibilities)
10. [Learner Site and Maintenance Mode](#10-learner-site-and-maintenance-mode)

</details>

---

## 1. Current Status

The repository builds and maintains a rigorous, evidence-based **Data & Intelligence** learning roadmap for an AI Engineer. A separate, future Computer Science & Engineering roadmap will cover general computing and software systems.

| Step | Status |
| --- | --- |
| Construction: research, audits, design, independence audit | Complete |
| 1 — Correction Pass | Complete |
| 2 — Final Curriculum Review | Complete (approved after four small corrections) |
| 3 — Baseline 1 | Complete — [ROADMAP.md](ROADMAP.md), accepted 2026-09-18 |
| 4 — Governance + Maintenance | Complete — [AGENTS.md](AGENTS.md), [MAINTENANCE.md](MAINTENANCE.md), [reviews/maintenance-state.json](reviews/maintenance-state.json) |
| 5 — Learner Site Finalization | Complete — learner site Version 1 in `site/` |
| Learner-experience reconciliation | Complete (2026-09-20) — every unit is a structured mini-chapter: its own generated contents over a two-level concept hierarchy (113 areas, 312 concepts) whose entries link to real sections, plus the narrative that explains itself before it assigns reading: context, conceptual organization, connections, an evolving mental model of AI, resource roles and concept-to-resource maps; stage purposes; statistics made visible as a progression. Presentation only; two reading proposals await approval in [reviews/2026-09-20-learner-experience-review.md](reviews/2026-09-20-learner-experience-review.md) |
| Modern AI Engineering restored | Complete (2026-09-19) — a substantive parallel curriculum of nine topics beside the 19-step Depth path, traced to the new [current-practice register](reviews/modern-practice-register.md) and the first [4-week scan](reviews/2026-09-19-modern-ai-scan.md); no new baseline. See [design/learner-guide.md §10](design/learner-guide.md#10-modern-ai-engineering-restored-as-a-parallel-curriculum) |
| Final acceptance correction | Complete — **Baseline 2** accepted 2026-09-19: the reading plan and the parallel track's hands-on resources; the learner guide ([LEARNING-GUIDE.md](LEARNING-GUIDE.md)) and site regenerated |
| Learner-journey orchestration | Complete (2026-09-20) — Depth and Modern presented as one chronological journey: every topic states whether it is required, recommended or available and where the numbered path resumes; the topic table carries the same three facts and is checked against the topics; transitions written from the Depth side at steps 7, 9, 11, 15 and 16; whole books paced with first-reading, continuation and return labelled; two practice instructions disambiguated; step 6 gains the Python engineering its own testing and reproducibility requirements need, from a resource already assigned; planned material given honest fallbacks at steps 4, 6, 11 and 12. Presentation only. See [design/learner-guide.md §12](design/learner-guide.md#12-learner-journey-orchestration) |
| Journey navigation | Complete (2026-09-21) — the generated site's primary Previous/Next controls now walk the one interleaved journey (Depth steps with each Modern topic where it is taken), each detour link carrying that topic's status and each return saying the numbered path resumes; the whole path on Learn shows the same sequence; *Inference, Cost and Production* declares one status instead of two; the corrupted step-5 practice line is repaired. Two checks added (pager follows the journey; no section label inside a sentence) |
| Explanation and mental model | Complete (2026-09-21) — every unit now defines its subject in plain language before announcing what it teaches, with the roadmap's explanation boundary stated to the learner; Modern Orientation rebuilt as a first map of contemporary AI engineering; first-use vocabulary traced and fixed; one diagram added at step 10 and one in Orientation; paid access, revisit origins, fixtures, traceback reading and boundary wording resolved in passing. Presentation only. See [design/learner-guide.md §13](design/learner-guide.md#13-explanation-and-mental-model-pass) |
| Reading experience (UI) | Complete (2026-09-21) — justification scoped to long-form prose at a readable measure and dropped below 48em, with headings, navigation, tables and controls ragged right (superseding the 2026-09-19 blanket rule in [AGENTS.md](AGENTS.md#generated-html-output)); study items set out as role, resource, reading and reason; a skip route past optional Modern detours; phone-sized unit contents, stacked pair tables and keyboard-reachable diagrams; versioned assets. See [design/learner-guide.md §14](design/learner-guide.md#14-reading-experience) |
| Curriculum-authored materials | Complete (2026-09-21) — the thirteen materials ROADMAP §11 promised are written and integrated: framing cases, release and rollback cases, two simulations, a calibration exercise, a ranking-metrics note, a testing and reproducibility checklist, the reinforcement-learning arc, the lifecycle brief, an agent-loop exercise, a fault-injection lab, an autonomy rubric and a note on tool interfaces. They live in `materials/`, are linked from the units that need them, and their code runs. See [design/learner-guide.md §15](design/learner-guide.md#15-curriculum-authored-materials) |

Construction is finished; there is no further construction step. The project now runs in maintenance mode — see [10](#10-learner-site-and-maintenance-mode).

[⬆ Back to Contents](#contents)

---

## 2. Canonical Files

| Question | Canonical answer lives in |
| --- | --- |
| What does the learner learn? | [ROADMAP.md](ROADMAP.md) — **Baseline 2**; presented to learners by [LEARNING-GUIDE.md](LEARNING-GUIDE.md) |
| How must agents operate? | [AGENTS.md](AGENTS.md) — the constitution |
| How is maintenance performed, and what is due? | [MAINTENANCE.md](MAINTENANCE.md) and [reviews/maintenance-state.json](reviews/maintenance-state.json) |
| Why is the curriculum shaped this way? | [design/curriculum-proposal.md](design/curriculum-proposal.md) — revision 4, the accepted design |
| What did the research find? | `research/` — dated evidence reports |
| What was the curriculum before? | [history/roadmap-baseline-v0.md](history/roadmap-baseline-v0.md) — immutable |

**Evidence ≠ Decision ≠ Presentation.** Research is evidence; `ROADMAP.md` is the decision; `site/` is presentation and never defines curriculum.

[⬆ Back to Contents](#contents)

---

## 3. Curriculum Architecture

Full detail is in [ROADMAP.md](ROADMAP.md). In brief:

- **Depth Track:** Fundamentals → Advanced → Mastery → Research. **Modern AI Engineering** is a parallel track, not a fifth level, entered in four prerequisite-gated phases (0 Orientation, 1 First Contact, 2 Grounded Systems, 3 Compound Systems; adaptation practice opens after F1).
- **12 Universal Core areas**, taught through:
  - **9 Fundamentals blocks:** E1 Programming and Data Handling · E2 Mathematics · E3 Statistics, Inference and Experimentation · E4 ML Foundations · E5 Deep Learning and Representations · E7 Foundation Model Mechanics · E8 Retrieval · E9 Data for AI · E10 Evaluation and Measurement. **E6 was retired**; IDs are stable for traceability.
  - **6 Advanced blocks:** F1 Foundation Model Lifecycle · F2 Compound AI Systems · F3 Evaluation Science · F4 Trustworthy AI · F5 AI Systems Engineering and Operations · F6 Advanced Retrieval and Ranking.
- **Mastery:** G1 Design Judgment, G2 Diagnostic Capability, G3 Experimental Capability (universal) · G4 Selective Depth.
- **Research:** H1 Research Literacy (universal) · H2 Research Contribution (optional).
- **Beyond the core:** Important Extensions EX1–EX9 · Specializations SP1–SP10 · Research Frontiers RF1–RF8.
- **Required strand:** Problem Framing and Decision Judgment — E4 → E10 → F2/F5 → G1.
- **Monitoring** begins in Fundamentals (E9 shift and skew; E10 limits of offline evaluation) and deepens in F5.
- **One from-scratch model build** (E7); F1 adapts that model.
- **F1 gates no other block hard.** E8 requires E3 and E5, not E10. F2 context management is Understand → Implement.

[⬆ Back to Contents](#contents)

---

## 4. Completed Evidence and Design Work

All dated 2026-09-17 to 2026-09-18.

| Artifact | What it is |
| --- | --- |
| [Landscape](research/2026-09-17-data-intelligence-landscape.md) | Independent map of the field: 19 areas in 6 strata |
| [Roadmap comparison](research/2026-09-17-roadmap-comparison.md) | Landscape versus Baseline v0 |
| [Resource coverage audit](research/2026-09-18-resource-coverage-audit.md) | What the Baseline v0 resources actually teach |
| [Targeted resource research](research/2026-09-18-targeted-resource-research.md) | Resources for the six unresourced blocks (R1–R9); corrections K1–K4 |
| [Independent capability reconstruction](research/2026-09-18-independent-capability-reconstruction.md) | Blind Phase I by a separate agent; frozen, SHA-256 `8cd1dede…387b` |
| [Independence audit](research/2026-09-18-project-wide-independence-audit.md) | Adversarial Phase II: 0 Critical, 8 Important, 6 Optional, 5 Evidence Update Only; "Ready After Specific Corrections" |
| [Curriculum proposal](design/curriculum-proposal.md) | Design record, revisions 1–4, with full change traceability |
| [Site architecture](design/site-architecture.md) and [content-fidelity audit](design/content-fidelity-audit.md) | Site design; fidelity audits of the first visual milestone (PASS WITH NOTES), the Version 1 site (PASS) and the learner-guide site (PASS) |
| [Learner guide derivation](design/learner-guide.md) | How the one learning path was derived, the book-by-book reading plan, and the accurate record of the Baseline 2 changes |

**Known evidence caveats.** The landscape's anti-anchoring note does not mention that `AGENTS.md`, which lists topics, was read before its taxonomy was built. The coverage audit's statement that no resource could contain MCP-era content was corrected by K2. Research reports are historical evidence and are not edited; later reports carry the corrections.

[⬆ Back to Contents](#contents)

---

## 5. Key Settled Decisions

Reopen only with new evidence through the review process — not by preference.

| Decision | Where recorded |
| --- | --- |
| Concepts before frameworks; modern does not mean important | [AGENTS.md](AGENTS.md) |
| Modern AI Engineering is parallel, never a fifth level | [AGENTS.md](AGENTS.md), [ROADMAP.md](ROADMAP.md) |
| Topics can span depth levels; the 19 landscape areas are not 19 curriculum sections | [AGENTS.md](AGENTS.md) |
| Independent discovery before comparison; the roadmap must be falsifiable | [AGENTS.md — Independent Discovery and Falsification Rule](AGENTS.md#independent-discovery-and-falsification-rule) |
| Resources support curriculum; they do not define it | [AGENTS.md — Resource Independence Rule](AGENTS.md#resource-independence-rule) |
| D1 chapter- and section-level resource assignment | Proposal §Q |
| D2 language concepts integrated into E4, E5, E7; deeper NLP in EX3 | Proposal §Q, C6 |
| D3 vision required, via transfer learning | Proposal §Q |
| D4 a short RL arc in F1, with bandit awareness | Proposal §Q |
| D5 ML-specific testing and reproducibility in D&I; general software practice in CS&E | Proposal §Q, C7 |
| D6 the parallel track may begin before E3; early access is not early mastery | Proposal §Q |
| D7 AI-specific security in D&I; general security foundations in future CS&E | Proposal §Q |
| Independence-audit corrections C1–C8 and Final Review corrections A–D | Proposal, "Independence Audit Corrections" and "Final Review Corrections" |
| Significant `ROADMAP.md` changes need human approval | [AGENTS.md — Human Approval Boundary](AGENTS.md#human-approval-boundary) |

[⬆ Back to Contents](#contents)

---

## 6. Resource Status

- **32 source resources are mandatory.** ROADMAP.md maps their portions to capabilities (coverage); its **reading plan** says how each is read. Coherent core books — *Practical SQL*, *Python for Data Analysis*, *Hands-On ML*, *Designing Machine Learning Systems*, *AI Engineering*, *Build a Large Language Model (From Scratch)*, *Hands-On Large Language Models* and the *Python Tutorial* — are read whole, in order; *LLM Engineer's Handbook* is read through whole, with running it optional. Reference textbooks, papers, standards and specialization material are read in named portions. See [ROADMAP.md §14](ROADMAP.md#14-resource-map).
- **Baseline 2 history.** The two parallel-track books were proposed during learner-guide reconciliation and written into ROADMAP.md before approval, labelled "owner-directed" in error. The owner explicitly approved them, together with the reading plan, in the final acceptance correction on 2026-09-19, which created Baseline 2. Baseline 1 is preserved exactly as accepted at [history/roadmap-baseline-1.md](history/roadmap-baseline-1.md).
- **Eleven planned learner materials** — exercises, notes, rubrics, simulations, a checklist and a lab — are baseline implementation work, produced progressively before a learner reaches each block. They are not research debt. See [ROADMAP.md §11](ROADMAP.md#planned-learner-materials).
- **Conditional:** *NLP in Action* §10.3 in E8, for ANN index choice.
- **F6** has no dedicated mandatory resource.

[⬆ Back to Contents](#contents)

---

## 7. Maintenance System

| | |
| --- | --- |
| **Command** | *Read AGENTS.md and MAINTENANCE.md. Perform the maintenance action that is currently due.* |
| **4-week Modern AI Scan** | Lightweight change scan → `reviews/YYYY-MM-DD-modern-ai-scan.md`, and updates the [current-practice register](reviews/modern-practice-register.md). First run 2026-09-19; next due **2026-10-17** |
| **12-week Curriculum Review** | Independent examination first, then comparison → `reviews/YYYY-MM-DD-curriculum-review.md`. First due **2026-12-11** — the third scan date, so the review subsumes that scan |
| **State** | [reviews/maintenance-state.json](reviews/maintenance-state.json) |
| **Approval** | Significant curriculum changes need human approval; minor changes are narrowly defined in [MAINTENANCE.md](MAINTENANCE.md) |
| **Versioning** | A new baseline number only for significant accepted revisions; outgoing baselines preserved in `history/` |

[⬆ Back to Contents](#contents)

---

## 8. Non-Blocking Uncertainties

Carried as standing maintenance items ([MAINTENANCE.md §10](MAINTENANCE.md#10-standing-maintenance-items)). None blocks the current baseline.

- Whether one small model build remains the most efficient route to understanding model mechanics.
- Whether agent-style systems become universal and durable enough to change their curriculum role.
- Whether an adequate F6 resource becomes available.
- Subsection depth of assigned sections in paid resources, notably *AI Engineering*.
- Whether *AI Engineering* teaches ANN index choice, which would resolve the conditional E8 source.
- [ROADMAP.md §16](ROADMAP.md#16-maintenance-status) still says the detailed maintenance procedure is not yet written; [MAINTENANCE.md](MAINTENANCE.md) now exists. A status-wording correction for the first Curriculum Review; the site presents the canonical wording unchanged.

[⬆ Back to Contents](#contents)

---

## 9. Current File Responsibilities

| Path | Responsibility |
| --- | --- |
| [ROADMAP.md](ROADMAP.md) | Canonical curriculum, Baseline 2 — the detailed specification |
| [LEARNING-GUIDE.md](LEARNING-GUIDE.md) | The learner's guide: the 19-step Depth path and the parallel Modern AI Engineering curriculum of nine topics, presenting the accepted curriculum; checked against ROADMAP.md, including its reading plan, on every build |
| [AGENTS.md](AGENTS.md) | Constitution and operating rules |
| [MAINTENANCE.md](MAINTENANCE.md) | Maintenance operating procedure |
| [PROJECT-STATE.md](PROJECT-STATE.md) | This handoff |
| [README.md](README.md) | Project philosophy and current status |
| `design/` | Curriculum design record; learner-guide derivation and resource reconciliation; site architecture; content-fidelity audit |
| `research/` | Evidence reports — historical, not edited |
| `reviews/` | Maintenance state; the current-practice register; scan and review reports |
| `history/` | Immutable historical baselines: v0 and Baseline 1 |
| `prompts/` | The landscape-research prompt |
| `scripts/` | Site generator Version 1 (Python) and its configuration — see `scripts/README.md` |
| `site/` | Generated learner site — current with Baseline 2; disposable presentation, rebuilt from the canonical files |

[⬆ Back to Contents](#contents)

---

## 10. Learner Site and Maintenance Mode

| | |
| --- | --- |
| **Learner site** | Current with Baseline 2. Areas: **Learn** (the guide, one page per step), **Evidence** (research reports), **About** (the curriculum specification, project, governance, maintenance and reviews, design records, history). Local-first: no backend, no remote assets, vendored Mermaid; no search |
| **Where a learner starts** | `site/index.html` → **Start with step 1**. Or read [LEARNING-GUIDE.md](LEARNING-GUIDE.md) directly |
| **Build** | `.venv/bin/python scripts/build_site.py` from the repository root; open `site/index.html` or serve `site/` with `python3 -m http.server`. Rebuild after any canonical change; the build refuses to replace `site/` if validation fails |
| **Generator** | `scripts/sitegen`, generator `1.1.0`. Routes, areas and presentation options in `scripts/site.toml`; no curriculum content in code or configuration |
| **Maintenance command** | *Read AGENTS.md and MAINTENANCE.md. Perform the maintenance action that is currently due.* |

**Remaining non-blocking items.**

- The eleven planned learner materials are produced progressively ([ROADMAP.md §11](ROADMAP.md#planned-learner-materials)).
- The uncertainties in [8](#8-non-blocking-uncertainties) are carried by maintenance.
- Mermaid diagrams are checked in text form; their runtime rendering is not verified automatically.
- On small screens, block tables stack label above value; some assistive technologies may announce these as plain text rather than a table.

[⬆ Back to Contents](#contents)

</div>
