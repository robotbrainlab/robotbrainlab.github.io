<div align="justify">

# Maintenance Procedure

| | |
| --- | --- |
| **Role** | The operating procedure for keeping the roadmap current. [AGENTS.md](AGENTS.md) is the constitution; this file is how it is carried out |
| **Current baseline** | Baseline 3, canonical in [ROADMAP.md](ROADMAP.md) |
| **State file** | [reviews/maintenance-state.json](reviews/maintenance-state.json) |
| **Outputs** | Dated reports in `reviews/` |

The human does not need to remember the project's history or calendar. The state file records what was last done and what is due; this file says how to do it.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Normal Maintenance Command](#1-normal-maintenance-command)
2. [Determining the Due Action](#2-determining-the-due-action)
3. [Maintenance State](#3-maintenance-state)
4. [4-Week Modern AI Scan](#4-4-week-modern-ai-scan)
   - [Purpose and Independence](#purpose-and-independence)
   - [Search Directions](#search-directions)
   - [Anti-News-Feed Rule](#anti-news-feed-rule)
   - [Scan Procedure](#scan-procedure)
   - [Scan Report](#scan-report)
5. [12-Week Curriculum Review](#5-12-week-curriculum-review)
   - [Purpose](#purpose)
   - [Inputs](#inputs)
   - [Review Procedure](#review-procedure)
   - [Review Report](#review-report)
6. [Human Approval Boundary](#6-human-approval-boundary)
7. [Minor Changes](#7-minor-changes)
8. [Implementing Approved Changes](#8-implementing-approved-changes)
9. [Baseline Versioning](#9-baseline-versioning)
10. [Standing Maintenance Items](#10-standing-maintenance-items)
11. [Completion Checklist](#11-completion-checklist)
12. [Where the Dominant Practice Is](#12-where-the-dominant-practice-is--the-question-the-next-scan-must-answer)
13. [Staying Current Between Reviews](#13-staying-current-between-reviews)

</details>

---

## 1. Normal Maintenance Command

> **Read AGENTS.md and MAINTENANCE.md. Perform the maintenance action that is currently due.**

On this command, the agent determines the due action from the [state file](#3-maintenance-state) and today's date, performs it, updates the state file, and reports. It does not ask the human to work out dates.

Explicit commands are also supported and may be given at any time:

> **Perform the 4-week Modern AI Scan.**
>
> **Perform the 12-week Curriculum Review.**

An explicit command runs the named action even if it is not yet due. The state file is updated from the date the action was completed.

The scan's search directions changed on 2026-11-03 ([4](#search-directions)), and the next scan must also answer the question in [12](#12-where-the-dominant-practice-is--the-question-the-next-scan-must-answer). Awareness of releases and tooling is kept outside the cadence, in [13](#13-staying-current-between-reviews).

[⬆ Back to Contents](#contents)

---

## 2. Determining the Due Action

1. Read [reviews/maintenance-state.json](reviews/maintenance-state.json). If it is missing or does not parse, **stop**. Report the problem, propose a corrected state from the most recent dated reports in `reviews/` and the baseline header of [ROADMAP.md](ROADMAP.md), and ask the human to confirm before continuing.
2. Compare today's date with the two due dates:

| Condition | Action |
| --- | --- |
| Today ≥ `next_curriculum_review_due` | Perform the **12-week Curriculum Review**. It includes a scan, so no separate scan is run |
| Otherwise, today ≥ `next_modern_ai_scan_due` | Perform the **4-week Modern AI Scan** |
| Neither is due | Perform nothing. Report which action is next and its date |

3. **Overdue actions are performed once.** Do not run a catch-up series of missed scans; cover the whole period since the last action in one report.
4. Report the action taken, the report file created, the state-file changes, and any proposals awaiting human approval.

[⬆ Back to Contents](#contents)

---

## 3. Maintenance State

[reviews/maintenance-state.json](reviews/maintenance-state.json) is **operational metadata, not evidence**. It holds:

| Field | Meaning |
| --- | --- |
| `baseline` | The current baseline number in [ROADMAP.md](ROADMAP.md) |
| `baseline_date` | The date that baseline was accepted |
| `last_modern_ai_scan` | Date of the most recent scan, or `null` |
| `last_curriculum_review` | Date of the most recent curriculum review |
| `next_modern_ai_scan_due` | Date the next scan is due |
| `next_curriculum_review_due` | Date the next curriculum review is due |

**Update rules.** Dates are ISO `YYYY-MM-DD`. Intervals are counted from the date the action is **completed**:

| After | Set |
| --- | --- |
| A 4-week scan | `last_modern_ai_scan` = today; `next_modern_ai_scan_due` = today + 28 days |
| A 12-week review | `last_curriculum_review` = today; `next_curriculum_review_due` = today + 84 days; **and** `last_modern_ai_scan` = today; `next_modern_ai_scan_due` = today + 28 days |
| An accepted new baseline | `baseline` and `baseline_date` |

Compute dates arithmetically; do not estimate them.

[⬆ Back to Contents](#contents)

---

## 4. 4-Week Modern AI Scan

**In this section:** [Purpose and Independence](#purpose-and-independence) · [Search Directions](#search-directions) · [Anti-News-Feed Rule](#anti-news-feed-rule) · [Scan Procedure](#scan-procedure) · [Scan Report](#scan-report)

### Purpose and Independence

**Purpose.** Observe meaningful changes in contemporary AI engineering **without continuously rewriting the curriculum**. **Cadence:** every 4 weeks.

The scan is **lightweight**. It does not require a full independent field reconstruction ([AGENTS.md — Proportional Independence](AGENTS.md#proportional-independence)). It must, however, search the world rather than the roadmap: look for what changed, then ask whether it matters.

### Search Directions

**Changed 2026-11-03.** The directions used to be a list of subjects — model capability, inference
and serving, retrieval, agents, context, adaptation, evaluation, security, multimodality, standards.
Every one of those is a language-model subject, so a scan pointed along them could only return
language-model findings, and twice it did: all 23 sources of the 2026-11-03 scan were language-model
or agent papers, and the current-practice register holds no row about tabular models, time series,
recommenders, media generation or embodied systems. The old list carried a note saying it was "not a
closed taxonomy", and that note lost to the list both times.

**So the directions now name the kind of change to look for, not the technology it happens in.**

- What can engineers now build that they could not before?
- What changed in how systems are put together?
- What changed in how they are measured?
- What changed in how they fail, or are attacked?
- What changed in what they cost, or how fast they are?
- What became a standard, and what was dropped or deprecated?
- What is newly disputed, and what is now settled?
- **Active research frontiers** — what researchers are trying to solve, which directions have
  substantial evidence, which are contested, and which could reshape the field. The track carries
  the open problems, so the scan must look for them. Frontier findings are recorded, never promoted
  to practice.

Nothing in that list points at one technology, so a finding about any part of the field can come
back through it. Language-model work is still found; it simply stops being the only thing the scan
can see.

**Two rules that go with the change.**

1. **Report where practice is concentrated, as a finding in its own right.** Supply no taxonomy to a
   searching agent and name no areas — it builds its own structure from the evidence. Never frame
   any part of the search as "outside language models" or against an existing category: that defines
   the rest of the field by reference to one part of it and sends the agent hunting for a result
   instead of measuring one. **The distribution is a finding, not a premise.**
2. **Every searching agent reports what it searched, what it could not reach, and what its sources
   over-represent.** A claim about the field's shape is worth exactly as much as the sampling behind
   it.

Prefer primary evidence, as ranked in [AGENTS.md — Research Standards](AGENTS.md#research-standards).
Record scientific evidence and engineering adoption as separate signals.

### Anti-News-Feed Rule

The scan is **not**:

- AI news summarization;
- model-release tracking for its own sake;
- a collection of vendor announcements;
- a GitHub-trending digest;
- leaderboard watching.

A development matters **only** if it changes something meaningful about what engineers need to understand or build, system architecture, evaluation, reliability, security, efficiency, or professional practice.

> ⚠️ If nothing meaningful changed, the correct result is: **No curriculum-relevant change.**
>
> A short report that says so is a successful scan.

### Scan Procedure

1. Read the previous scan report, if any, and carry forward its open watch items.
2. Search the period since the last scan (or since `baseline_date` for the first scan) along the directions above and beyond them.
3. For each candidate, test it against the anti-news-feed rule. Discard what fails.
4. For each survivor, decide a status on the [AGENTS.md lifecycle](AGENTS.md#topic-maturity) and an action from the table below, and record it in the [current-practice register](reviews/modern-practice-register.md) with its evidence.
5. Write the report. Update the register — and the learner guide's Modern AI: Research, Science and Engineering topics where a taught practice changed status; only Current Practice, Established and Open problem entries are taught, and the site build enforces this. Update the state file.

| Action | Use when |
| --- | --- |
| **Ignore** | Recorded only to show it was considered |
| **Watch** | Possibly important; evidence or adoption still thin |
| **Current Practice** | Established enough to practise now, not yet durable curriculum |
| **Investigate at 12-week review** | May require a permanent curriculum change |
| **Superseded** | An existing current-practice item has been replaced |
| **Open problem** | An unresolved question the track carries as a frontier, not as practice |
| **Evidence update** | Corrects or refreshes evidence without changing the curriculum |

**What a scan may change.** A scan normally does **not** modify the permanent curriculum. It may update the *current-practice* column of [ROADMAP.md §6 Modern AI: Research, Science and Engineering](ROADMAP.md#6-modern-ai-research-science-and-engineering) when the evidence is recorded in the scan report and the change does not touch the Depth Track, any block's required capability, depth or prerequisites, the durable-concept column, or mandatory resources. Any such edit must be listed in the report and in the completion message, and the site must be regenerated per [AGENTS.md — Generated HTML](AGENTS.md#generated-html). Everything else waits for the 12-week review.

### Scan Report

**Location:** `reviews/YYYY-MM-DD-modern-ai-scan.md`, dated on completion, following the Markdown conventions in [AGENTS.md](AGENTS.md#markdown-source-files).

**Contents:**

1. **Header** — date; period covered; current baseline.
2. **Method** — search directions used; sources consulted; what was deliberately excluded.
3. **Findings** — only meaningful findings:

| Finding | Evidence | Status | Why it matters | Action |
| --- | --- | --- | --- | --- |

4. **Carried-forward watch items** — each with its current status.
5. **Changes made** — any current-practice edits, or "None".
6. **For the next 12-week review** — items marked *Investigate*.
7. **Sources** — URLs with access dates and evidence tiers.

[⬆ Back to Contents](#contents)

---

## 5. 12-Week Curriculum Review

**In this section:** [Purpose](#purpose) · [Inputs](#inputs) · [Review Procedure](#review-procedure) · [Review Report](#review-report)

### Purpose

Decide whether accumulated evidence requires changing the current baseline. **Cadence:** every 12 weeks (84 days).

> **Do not ask: what changed in our roadmap topics?**
>
> **Ask: what does the learner need now, independent of what we currently teach?**

The review applies the [Independent Discovery and Falsification Rule](AGENTS.md#independent-discovery-and-falsification-rule): the independent examination comes **before** the comparison with [ROADMAP.md](ROADMAP.md).

### Inputs

- all scan reports since the last curriculum review;
- fresh primary evidence, both scientific and engineering;
- evidence of engineering adoption and current professional practice;
- failures and limitations that have become clearer;
- changes in maturity and durability;
- learner feedback, if available;
- the running notes file from [13](#13-staying-current-between-reviews), tested rather than accepted;
- resource updates — new editions, withdrawn materials, better candidates — where relevant;
- the [standing maintenance items](#10-standing-maintenance-items).

Scientific importance and engineering adoption are separate signals. Neither is hype, and hype is neither.

### Review Procedure

1. **Pass 1 — Independent current-state reconstruction.** From fresh evidence and the accumulated scans, write down what capabilities and knowledge a contemporary Data & Intelligence AI engineer now needs, and at what depth, **before** re-reading the roadmap's block lists. If the reviewing agent has already studied the roadmap in the same session, delegate Pass 1 to a fresh agent where available, or disclose the limitation in the report.
2. **Pass 2 — Comparison.** Compare Pass 1 with [ROADMAP.md](ROADMAP.md). Classify each difference as Correct, Missing, Excessive, Misplaced, Outdated, Under-specified, Over-specified or Uncertain. Preserve conflicts; do not reconcile them silently.
3. **Resources.** Apply the [Resource Independence](AGENTS.md#resource-independence-rule) and [Resource Compression](AGENTS.md#resource-compression-rule) rules to any proposed resource change.
4. **Bias audit.** Test every item in the [Permanent Bias Checklist](AGENTS.md#permanent-bias-checklist).
5. **Proposals.** Classify each proposed change and apply the [Curriculum Change Rule](AGENTS.md#curriculum-change-rule).
6. **Write the report, update the state file, and present proposals for human approval.** Make no significant change to [ROADMAP.md](ROADMAP.md) before approval.

**Change classification.**

| Class | Meaning |
| --- | --- |
| **Critical** | The current curriculum would produce a meaningful capability defect |
| **Important** | A material improvement in scope, depth, sequencing or efficiency |
| **Optional** | A reasonable refinement, not needed for curriculum integrity |
| **Evidence Update Only** | Corrects evidence without changing the curriculum |

For each Critical or Important proposal, state: current state; finding; evidence; capability consequence; proposed change; learning-cost consequence; confidence.

### Review Report

**Location:** `reviews/YYYY-MM-DD-curriculum-review.md`, dated on completion, following the Markdown conventions in [AGENTS.md](AGENTS.md#markdown-source-files).

**Sections:**

1. Executive Summary
2. Independent Current-State Reconstruction
3. Comparison With Current Baseline
4. Missing Knowledge
5. Excessive or Outdated Knowledge
6. Misplaced Depth
7. Dependency Changes
8. Modern-Practice Changes
9. Resource Changes
10. Anti-Bloat and Compression Findings
11. Bias Audit
12. Proposed Changes
13. Things Explicitly Not Changed
14. Uncertainties
15. Sources

Label important conclusions Observed, Inference, Judgment or Uncertain, with confidence, per [AGENTS.md — Uncertainty](AGENTS.md#uncertainty).

[⬆ Back to Contents](#contents)

---

## 6. Human Approval Boundary

| Maintenance may do without approval | Requires explicit human approval |
| --- | --- |
| Research and analyze | Adding or removing a Universal Core area |
| Write scan and review reports | Materially changing a block's required depth |
| Update the state file | Changing major prerequisites |
| Record watch items and statuses | Promoting an Important Extension into Universal Core |
| Update the current-practice column of [ROADMAP.md §6](ROADMAP.md#6-modern-ai-research-science-and-engineering), as limited in [Scan Procedure](#scan-procedure) | Removing a required capability |
| Make [minor changes](#7-minor-changes) | Substantially changing the mandatory resource burden |
| **Propose** any curriculum change | Any other significant change to [ROADMAP.md](ROADMAP.md) |

After approval, the agent may implement the accepted changes ([8](#8-implementing-approved-changes)).

> ⚠️ Never make a significant change to `ROADMAP.md` silently.

[⬆ Back to Contents](#contents)

---

## 7. Minor Changes

These may be made without an approval cycle, but must be listed in the completion message:

- broken links;
- corrected citation metadata;
- typographical errors;
- clearly superseded URLs for the same resource;
- formatting within [AGENTS.md conventions](AGENTS.md#markdown-source-files);
- factual resource-edition metadata that does not alter what is assigned or learned.

A change is **not** minor if it alters what a learner must learn, to what depth, in what order, or from which assigned portions.

> ⚠️ Do not classify a curriculum-content change as minor to avoid approval.

[⬆ Back to Contents](#contents)

---

## 8. Implementing Approved Changes

1. Confirm the approved scope in the conversation. Implement only that scope.
2. If the change is significant, create a new baseline ([9](#9-baseline-versioning)): copy the current [ROADMAP.md](ROADMAP.md) verbatim to `history/roadmap-baseline-N.md` (N = the outgoing baseline) **before** editing.
3. Edit [ROADMAP.md](ROADMAP.md). Update its baseline number, acceptance date and Maintenance Status section. Then update [LEARNING-GUIDE.md](LEARNING-GUIDE.md) to present the change; the site build fails until the guide and the curriculum correspond.
4. Record the rationale: the curriculum-review report, plus a `design/` note if the design reasoning is substantial.
5. Update [PROJECT-STATE.md](PROJECT-STATE.md) and the state file.
6. Regenerate and verify the site per [AGENTS.md — Generated HTML](AGENTS.md#generated-html).
7. Verify every anchor and relative link, and verify that `history/` files are unchanged.

[⬆ Back to Contents](#contents)

---

## 9. Baseline Versioning

| Event | Baseline |
| --- | --- |
| A significant accepted curriculum revision | Increment the baseline number (Baseline 1 → Baseline 2) |
| Typo fixes, formatting, broken links, citation metadata | No change |
| Site regeneration | No change |
| Scan or review reports; watch-item or status changes | No change |
| Current-practice edits within the scan's limits | No change |

- **Current:** Baseline 3, accepted 2026-11-02.
- **History:** [history/roadmap-baseline-v0.md](history/roadmap-baseline-v0.md), [history/roadmap-baseline-1.md](history/roadmap-baseline-1.md) and [history/roadmap-baseline-2.md](history/roadmap-baseline-2.md). Every future outgoing baseline is preserved alongside them.

> ⚠️ Files in `history/` are immutable. Never overwrite or edit them.

[⬆ Back to Contents](#contents)

---

## 10. Standing Maintenance Items

Non-blocking items carried forward from the construction of Baseline 1. Consider each at the 12-week review. None blocks use of the roadmap, and none is to be researched outside a review.

| Item | Question for the review |
| --- | --- |
| **F6 resource gap** | F6 remains accepted but has no dedicated mandatory teaching resource; cross-references and optional material give partial support. Is there now an adequate resource that materially improves learning of F6 without unnecessary burden? |
| **One small model build** | Does a single from-scratch small language model (E7) remain the most efficient route to model-mechanics understanding? |
| **Action-taking systems** | Have agent-style systems become universal and durable enough to change their curriculum role or depth in F2? |
| **Paid-resource depth** | Page ranges for *AI Engineering* and *Designing Machine Learning Systems* come from official tables of contents; *AI Engineering*'s subsection depth is unverified from body text. Verify when feasible |
| **Conditional ANN source** | Does *AI Engineering*'s "Retrieval Algorithms" section teach approximate nearest-neighbour index choice? If so, drop the conditional *NLP in Action* §10.3 assignment in E8 |
| **Planned learner materials** | Eleven curriculum-authored materials listed in [ROADMAP.md §11](ROADMAP.md#planned-learner-materials) are implementation work, produced progressively. Track which exist; they are not research questions |

[⬆ Back to Contents](#contents)

---

## 11. Completion Checklist

Before reporting any maintenance action as complete:

- The report exists at the specified location and follows the Markdown conventions.
- Every anchor and relative link resolves.
- The state file parses and its dates are computed arithmetically.
- No significant change was made to [ROADMAP.md](ROADMAP.md) without approval; any minor or current-practice edits are listed.
- `history/` files are unchanged.
- If learner-facing canonical content changed, the site was regenerated and checked.
- The completion message states: the action performed, the report path, state changes, changes made, and proposals awaiting approval.

[⬆ Back to Contents](#contents)

---

## 12. Where the Dominant Practice Is — the question the next scan must answer

**Agreed with the owner, 2026-11-03.** This began as a one-off investigation. It is not one: the
bias lived in the scan's standing directions, so fixing it once would have fixed nothing. The
directions in [4](#search-directions) were changed instead, and **the next scan under those
directions is this investigation.**

What it has to answer, alongside its normal findings:

> **Where is the dominant practice in AI engineering, and how is it distributed across the field?**

### Why it matters beyond the scan

It decides the scope of the second book — whether the Modern AI track has ten topics or more — and
it is one of the two tasks blocking that book's first chapter. See `_book/HANDOVER.md` §9.5.

Two outcomes, both useful:

- **Substantial practice outside language models.** The track is short of topics and the register
  needs rows it has never had.
- **Thin.** Then "Modern AI" in this project honestly means the foundation-model layer, and
  [ROADMAP.md §6](ROADMAP.md#6-modern-ai-research-science-and-engineering) should say so in one
  sentence rather than letting the name overclaim.

### The evidence that the bias was real

- The [current-practice register](reviews/modern-practice-register.md) holds 68 entries and **not
  one** concerns tabular models, time series and forecasting, recommenders, media generation or
  embodied systems. Multimodal input is the nearest thing, and that is still a language model.
- All 23 sources of the [2026-11-03 scan](reviews/2026-11-03-modern-ai-scan.md) were language-model
  or agent papers.
- All three blind reconstructions run on 2026-11-03 disclosed the same limit unprompted. One wrote
  that its evidence was "English-language, Western, LLM-centric research. Entirely," and named
  non-LLM work as the largest structural gap in its report.
- [The landscape](research/2026-09-17-data-intelligence-landscape.md) §A point 2 says plainly that
  foundation models reorganised the field **without replacing it**, and two of the twenty frontier
  questions in its §F are not about language models at all.

[⬆ Back to Contents](#contents)

---

## 13. Staying Current Between Reviews

**Agreed with the owner, 2026-11-03.** The scan was being asked to do two jobs and did neither well.

**The two jobs are different.** Knowing that a lab shipped a tool is **awareness**. Deciding what the
curriculum teaches is **research**. The [Anti-News-Feed Rule](#anti-news-feed-rule) bars the scan from
the first, so for two cycles the scan could not report the thing the owner most wanted to know, and
filled the gap with *Watching* rows instead. A four-week research cycle is also the wrong instrument
for it: too slow to hear about a release, and too heavy to be worth running for one.

**So awareness is kept separately, as a running notes file, and it is not research.** Follow release
notes, changelogs and the tools actually in use, as broadly as you like. No report, no register, no
evidence grading, no cadence.

**The one rule that makes it useful rather than noise:**

> **Watch the tools. Write down the capability.**

A product launching tells you nothing. Several products doing the same new thing tells you a
capability has become expected, and that is adoption evidence. So a note reads *"several vendors now
sell X, so it is becoming expected practice"* — never *"company Y shipped Z"*. The product names are
the evidence; the capability is the finding. This is the shape the landscape's §E already uses, where
the products sit in a column headed **"Implementation examples (not categories)"** beside the
capability they evidence.

Two consequences:

- **The notes file is an inbox, not a verdict.** Things land there as they are noticed; the 12-week
  review is where each one is tested against [5](#5-12-week-curriculum-review)'s procedure or thrown
  out. It is listed among that review's inputs.
- **Expect to discard most of it.** The landscape's §E says plainly that engineering importance is
  not scientific importance, and that several widely adopted practices carry little novelty. Most of
  this layer changes nothing about what an engineer must understand.

[⬆ Back to Contents](#contents)

</div>
