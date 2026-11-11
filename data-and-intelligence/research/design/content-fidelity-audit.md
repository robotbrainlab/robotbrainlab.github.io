<div align="justify">

# Content-Fidelity Audit

| | |
| --- | --- |
| **Scope of this record** | Two audits. The **First Visual Milestone audit** (2026-09-17, sections 1–21) is preserved unchanged below. The **Final Version 1 audit** (2026-09-18) is [section 22](#22-final-version-1-audit) |
| **Final Version 1 result** | **PASS** — all 16 generated canonical documents match their sources in ordered wording, headings, table cells and code; see [22](#22-final-version-1-audit) |
| **Learner-guide result** | **PASS** (2026-09-19) — the learner experience is now [LEARNING-GUIDE.md](../LEARNING-GUIDE.md); fidelity is checked against the guide, and the guide is checked against ROADMAP.md; see [23](#23-learner-guide-audit) |
| **Audit date** | 2026-09-17 |
| **Audited build** | Generator `0.1.0-milestone1`; pages `index.html`, `research/2026-09-17-data-intelligence-landscape/index.html` |
| **Build currency** | Verified: the source hashes in `site/build-manifest.json` match the current canonical files, so the audited HTML corresponds to today's sources |
| **Question** | Does the generated HTML faithfully present canonical content without silently adding, removing, rewriting, reordering, misclassifying or breaking anything? |
| **Changes made to canonical Markdown** | None |
| **Changes made to generator code** | None (no fidelity bug required a fix) |

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Executive Result](#1-executive-result)
2. [Sources Audited](#2-sources-audited)
3. [Generated Pages Audited](#3-generated-pages-audited)
4. [Structural Comparison](#4-structural-comparison)
5. [Text Preservation Results](#5-text-preservation-results)
6. [Table Comparison](#6-table-comparison)
7. [List Comparison](#7-list-comparison)
8. [Mermaid Comparison](#8-mermaid-comparison)
9. [Link Comparison](#9-link-comparison)
10. [Citation and Source Comparison](#10-citation-and-source-comparison)
11. [Canonical Navigation Comparison](#11-canonical-navigation-comparison)
12. [Evidence-vs-Curriculum Assessment](#12-evidence-vs-curriculum-assessment)
13. [Home-Page Provenance](#13-home-page-provenance)
14. [Generated UI Inventory](#14-generated-ui-inventory)
15. [Character and Format Edge Cases](#15-character-and-format-edge-cases)
16. [Hard-Coded-Content Inspection](#16-hard-coded-content-inspection)
17. [Bugs Found](#17-bugs-found)
18. [Bugs Fixed](#18-bugs-fixed)
19. [Ambiguities Requiring Human Review](#19-ambiguities-requiring-human-review)
20. [Final Fidelity Verdict](#20-final-fidelity-verdict)
21. [Audit Method](#21-audit-method)
22. [Final Version 1 Audit](#22-final-version-1-audit)
23. [Learner-Guide Audit](#23-learner-guide-audit)

</details>

---

## 1. Executive Result

**Overall: PASS WITH NOTES.**

| Audit | Result |
| --- | --- |
| 1. Document structure | **PASS** — 45 canonical headings, identical text, level and order; heading IDs equal GitHub slugs; no duplicates |
| 2. Canonical text preservation | **PASS** — 3,586 content items in identical order; concatenated canonical text is character-identical to the generated text after whitespace normalization |
| 3. Tables | **PASS** — 38/38 tables, 561/561 rows, 2,964/2,964 cells, zero mismatches |
| 4. Lists | **PASS** — 38/38 lists, 188/188 top-level items, nesting and ordered/unordered types preserved |
| 5. Mermaid | **PASS (rendering NOT AUTOMATICALLY VERIFIED)** — 4/4 blocks, source byte-identical, fallback source retained in the DOM; runtime rendering was confirmed only by manual browser inspection |
| 6. Links | **PASS** — 372 canonical links all accounted for; 271 external URLs and labels preserved exactly; 92 in-page anchors resolve; 9 cross-file links correctly rendered as non-links |
| 7. Citations and sources | **PASS** — 514 citation labels in identical order; zero cell-level association errors across 3,177 table cells |
| 8. Canonical navigation | **PASS** — `## Contents` with `<details open>`, 36 Contents links in order, 2 "In this section" lines, 32 "Back to Contents" links, 14 separators |
| 9. Evidence vs curriculum | **PASS** — page is marked, classed and routed as evidence; no curriculum affordances present |
| 10. Home-page provenance | **PASS** — 44 of 58 substantive nodes are literal canonical wording; 14 are approved chrome or verified derived facts; **zero** category-D (invented) content |
| 11. Generated UI inventory | **PASS** — inventory recorded in section 14 |
| 12. Character/format edge cases | **PASS** — non-ASCII character multiset identical; no leaked entities, markup or escapes |
| 13. Source order | **PASS** — positional stream comparison found zero divergences |
| 14. Hidden content invention | **PASS** — zero curriculum/research substance found in 22 generator, template, config, JS and CSS files |

**Issues found: 7. Fidelity violations: 0. Bugs fixed: 0** (two defects were found in the *audit harness* and fixed there). All 7 issues are notes or ambiguities for human review, recorded in sections 17 and 19.

> ⚠️ One structural caveat, by design rather than by defect.
>
> This milestone renders exactly one canonical document in full (the landscape report). The Home page is a composed hub that displays selected canonical fragments. Most of the repository's canonical content is therefore not present on the site yet. That is the approved milestone scope, not a fidelity failure — but it means "the site presents the repository faithfully" is only established for the two audited pages.

[⬆ Back to Contents](#contents)

---

## 2. Sources Audited

| Canonical source | Role in the audited pages | Used for |
| --- | --- | --- |
| `research/2026-09-17-data-intelligence-landscape.md` | Rendered in full as the Evidence page | Audits 1–8, 12, 13 |
| `README.md` | Fragments composed into Home | Home hero, intro, stage descriptions, parallel-track description, maintenance cycles |
| `ROADMAP.md` | Fragments composed into Home | Architecture diagram (stage sequence and parallel track), stage statuses, track phases and status, roadmap status/purpose table |
| `research/2026-09-17-roadmap-comparison.md` | Not rendered; listed in navigation | Evidence area list entry (shown as not generated) |
| `AGENTS.md` | Not rendered | Referenced only as a file name on Home |

[⬆ Back to Contents](#contents)

---

## 3. Generated Pages Audited

| Page | Path | Size |
| --- | --- | --- |
| Home | `site/index.html` | 12 KB |
| Evidence (landscape report) | `site/research/2026-09-17-data-intelligence-landscape/index.html` | 304 KB |

Assets were inspected for hard-coded content (section 16) but not audited for visual design, which was approved separately.

[⬆ Back to Contents](#contents)

---

## 4. Structural Comparison

**Status: PASS.**

| Measure | Canonical Markdown | Generated HTML | Result |
| --- | --- | --- | --- |
| Headings total | 45 | 45 | equal |
| H1 | 1 | 1 | equal |
| H2 | 15 | 15 | equal |
| H3 | 29 | 29 | equal |
| H4 | 0 | 0 | equal (none in source) |
| Heading text and order | — | — | **zero mismatches** across all 45, compared pairwise in document order |
| Heading nesting | — | — | no skipped or re-levelled headings |
| Heading IDs | GitHub slug algorithm | generated IDs | **identical** for all 45 |
| Duplicate IDs in page | — | 0 | none |

Anchor compatibility was tested independently of the generator by recomputing GitHub-style slugs from the canonical heading text (lowercase, punctuation removed, spaces to hyphens, numbered duplicate suffixes) and comparing with the emitted `id` attributes. All 45 matched, which is what makes Markdown and HTML anchors interchangeable.

**Section wrappers.** The generated page contains 14 `<section>` elements for 15 canonical H2s. The difference is the canonical `## Contents` section, which is wrapped in `<nav>` instead (approved decision D6). No heading was lost; see note **N3**.

[⬆ Back to Contents](#contents)

---

## 5. Text Preservation Results

**Status: PASS.**

The audit built an ordered *content stream* from each side — headings, paragraphs, list items, blockquote paragraphs, table cells, code/diagram sources and raw-HTML text — and compared them positionally. This detects omission, duplication, rewriting, truncation and reordering, which a word-frequency test cannot.

| Measure | Result |
| --- | --- |
| Content items (canonical) | 3,586 |
| Content items (generated) | 3,586 |
| Positional divergences | **0** |
| First divergence index | none |
| Concatenated text identity | **identical** (155,393 characters after whitespace normalization) |
| Strong emphasis | 295 → 295 `<strong>` |
| Italic emphasis | 18 → 18 `<em>` |
| Inline code | 515 → 515 (excluding 4 diagram sources and 1 chrome element) |
| Blockquotes | 6 → 6 |
| Separators (`---`) | 14 → 14 `<hr>` |
| Images, strikethrough, line breaks, footnotes, inline HTML | 0 in source, 0 in output |

Findings on the specific risks named in the task:

- **Omitted:** none.
- **Duplicated:** none in the article. Two canonical values (the research execution date and report type) additionally appear in the generated metadata header; that block is marked `data-chrome` and is an approved presentation duplicate (note **N2**).
- **Rewritten / truncated / normalized in a meaning-changing way:** none.
- **Reordered:** none.
- **Accidentally converted into UI chrome:** none. Canonical navigation lines ("In this section", "Back to Contents") are styled but remain in the article as content.

**Callout classification** (Markdown gives enough information to classify safely):

| Canonical construct | Count | Generated class | Result |
| --- | --- | --- | --- |
| Blockquote starting with `⚠️` | 5 | `callout-warning` | correct |
| Blockquote of a single all-bold statement | 1 | `quote-principle` | correct |
| Other blockquotes | 0 | `quote` (plain) | n/a |

No blockquote was given semantic meaning that the source did not express, and the `⚠️` character itself is preserved as text.

[⬆ Back to Contents](#contents)

---

## 6. Table Comparison

**Status: PASS.**

```text
Canonical Markdown tables: 38
Generated HTML tables:     38
```

| Measure | Canonical | Generated | Result |
| --- | --- | --- | --- |
| Tables | 38 | 38 | equal |
| Header rows compared | 38 | 38 | **zero header mismatches** |
| Body rows | 561 | 561 | equal, zero row-order or row-text mismatches |
| Cells | 2,964 | 2,964 | equal |
| Cell-level link/citation association | 3,177 cells checked | — | **zero mismatches** |

- Column order, row order and cell text are preserved exactly in every table.
- No rows disappeared and none were duplicated.
- Responsive wrappers add a `<div class="table-wrap">` around each table and do not alter table semantics: `<table>`, `<thead>`, `<tbody>`, `<tr>`, `<th scope="col">` and `<td>` structure is intact. Wrappers are not counted as tables.
- 28 tables carry the dense/wide presentation class; 28 canonical tables have five or more columns, so the classification is purely structural.
- 197 source-register rows received `id="src-…"` anchors derived from the first cell of each row (their canonical ID). This adds addressability without changing content.

[⬆ Back to Contents](#contents)

---

## 7. List Comparison

**Status: PASS.**

| Measure | Canonical | Generated | Result |
| --- | --- | --- | --- |
| Lists | 38 | 38 | equal |
| Ordered lists | 5 | 5 | equal |
| Unordered lists | 33 | 33 | equal |
| Top-level items | 188 | 188 | equal |
| `<li>` elements total | 188 | 188 | equal |
| Item order and text | — | — | verified by the positional stream comparison (section 5) |

Loose list items containing several paragraphs, and items containing nested sub-lists, were compared paragraph-by-paragraph. Nesting depth, item boundaries and paragraph/list boundaries match the source. No list was flattened, merged or renumbered; ordered-list numbering remains browser-generated from source order.

[⬆ Back to Contents](#contents)

---

## 8. Mermaid Comparison

**Status: PASS, with rendering NOT AUTOMATICALLY VERIFIABLE.**

```text
Canonical Mermaid blocks:   4
Generated Mermaid containers: 4
```

| Check | Result |
| --- | --- |
| Every block appears in the output | Yes — 4 `<figure data-diagram>` elements |
| Source content unmodified | Yes — all 4 sources compare identical to the canonical fence content |
| Recognized as Mermaid rather than ordinary code | Yes — emitted as diagram figures, not as highlighted code blocks; the only fences in the source are `mermaid` |
| Fallback source exists | Yes — each figure contains `<pre class="diagram-source">` with the canonical text, visible when JavaScript is unavailable |
| Failure is recoverable | Yes — on success the script *moves* the source into a `<details>` disclosure rather than deleting it; on parse failure the source stays in place and an error note is added |

**Not automatically verified:** whether Mermaid actually renders each diagram at runtime. This audit is static. During the milestone build I confirmed by manual browser inspection that diagrams render in both themes and that the text fallback is retained, but no automated assertion covers it, and no headless-browser check exists in the implementation. I have not assumed success beyond what was observed manually.

[⬆ Back to Contents](#contents)

---

## 9. Link Comparison

**Status: PASS.**

| Measure | Canonical | Generated | Result |
| --- | --- | --- | --- |
| Links in source | 372 | 363 `<a>` + 9 inert spans = 372 | all accounted for |
| External links | 271 | 271 | href multiset **identical**; labels identical in order |
| External `rel="noopener noreferrer"` | — | 271/271 | applied |
| In-page anchors | 92 | 92 | all resolve to an existing `id` |
| Cross-file links | 9 | 9 inert spans | see below |

**Internal links.** All 92 fragment links resolve, including every canonical Contents entry, both "In this section" lines and all 32 "Back to Contents" links.

**Cross-file links.** The nine links to documents this milestone does not generate (`../prompts/landscape-research.md` ×3, `../ROADMAP.md` ×2, `../README.md` ×2, `../AGENTS.md`, `2026-09-17-roadmap-comparison.md`) render as `<span class="link-unavailable" title="Not generated in this milestone">` with the **canonical link label preserved verbatim** (for example `ROADMAP.md`). No dead link is emitted, and no label was changed. When those pages exist, the same links will resolve.

**External availability** was not checked, as instructed; only value and label preservation were audited.

[⬆ Back to Contents](#contents)

---

## 10. Citation and Source Comparison

**Status: PASS.**

| Check | Result |
| --- | --- |
| Citation labels in source | 514 |
| Citation labels in output | 514 |
| Identical sequence | Yes — exact order match |
| Identifiers dropped | None |
| Identifiers altered or merged | None; ranges and lists such as `[G1–G9, G13, G14, M1–M6]` are preserved as single labels with their dashes intact |
| Citations attached to the correct claim | Yes — positional stream comparison puts every citation in its original sentence, and cell-level checks confirm 3,177 table cells keep their own citations |
| Source URLs altered | None — all 271 external URLs identical |
| References duplicated | None |
| Evidence converted into curriculum metadata | No — citation labels are styled as quiet inline text only; no linking, no reclassification, no badges |

The generator does **not** yet resolve citation IDs to register rows (that is a Version 2 capability). It only applies a typographic class, so there is no possibility of a wrong claim-to-source association. Register rows did receive anchors (section 6), which is addressability, not association.

[⬆ Back to Contents](#contents)

---

## 11. Canonical Navigation Comparison

**Status: PASS.**

| Canonical convention | Canonical | Generated | Result |
| --- | --- | --- | --- |
| `## Contents` heading | present | present (H2, id `contents`) | preserved |
| `<details open>` | present | `<details open>` preserved verbatim | preserved, still open by default |
| `<summary><b>Click to expand / collapse</b></summary>` | present | byte-identical | preserved |
| Contents entries | 36 links | 36 links | **identical (label, href) sequence** |
| Contents group labels | `Orientation`, `Detailed Knowledge Map`, `Maps`, `Audit and Record` | all four present | preserved |
| "In this section" lines | 2 | 2 | preserved as content, styled |
| "Back to Contents" links | 32 | 32 | preserved as content, styled |
| Section separators (`---`) | 14 | 14 `<hr>` | preserved |
| Justify wrapper | `<div align="justify">` | removed; replaced by a stylesheet rule | correct per AGENTS (presentation directive) |

The canonical Contents block and the generated application navigation (area rail, "On this page" rail) coexist; neither replaced the other. The one structural transformation is that the Contents section is wrapped in `<nav>` rather than `<section>` and its H2 is styled as a small label — see note **N3**.

[⬆ Back to Contents](#contents)

---

## 12. Evidence-vs-Curriculum Assessment

**Status: PASS.**

| Check | Result |
| --- | --- |
| Page is marked as evidence | `<p class="doc-kind doc-kind--evidence" data-chrome>` reading "Evidence — research report" + "Not curriculum" |
| Body classification | `class="page-doc kind-evidence"`; evidence accent tone applied to links, rails and the top-bar rule |
| Routing | `research/…` URL; breadcrumb reads `Home / Evidence / <report title>` |
| Area rail | titled "Evidence" with subtitle "Research reports and findings" |
| Research maturity classifications | remain inside canonical tables as plain text; count in output equals count in source (spot check "Emerging": 16 = 16); no badges, colour-coding or vocabulary normalization |
| Landscape areas C1–C19 | remain canonical H3 headings inside the report; not converted into topic pages, navigation entries or curriculum items |
| Curriculum affordances on the page | none — no stage markers, no stage cards, no "learn this", no progress control, no entry actions (verified by class absence: `stage-node`, `stage-name`, `arch-track`, `track-name`, `entry-action`) |
| Links that blur the boundary | none — the only "roadmap" href on the page is a canonical external URL in the source register; the Roadmap navigation item is a non-interactive span |
| Word "Fundamentals" on the page | 2 occurrences, both canonical report text (2 in source) |

The evidence framing survives printing, because the marker is part of the document header rather than the application chrome.

[⬆ Back to Contents](#contents)

---

## 13. Home-Page Provenance

**Status: PASS — no category-D content.**

58 substantive text nodes were extracted from Home (navigation and footer excluded) and classified. 44 match canonical wording literally after markup removal. The remaining 14 are listed below in full.

| # | Displayed text | Class | Provenance |
| --- | --- | --- | --- |
| 1 | "Learning · Research · Curriculum maintenance" | **B** | Site eyebrow; UI wording |
| 2 | "Learning architecture" | **B** | Section title for the overview |
| 3 | "Where things stand" | **B** | Section title for the repository state |
| 4 | "Maintenance" | **B** | Section kicker |
| 5 | "7 sections" (label "Roadmap") | **C** | Count of H3 subsections under `## 1. Fundamentals` in `ROADMAP.md`. **Verified: 7** |
| 6 | "Continue to Roadmap — not generated in this milestone" | **B** | Inert entry action |
| 7 | "Explore Evidence →" | **B** | Entry action |
| 8 | "Reviews — not generated in this milestone" | **B** | Inert entry action |
| 9 | "Understand the Project — not generated in this milestone" | **B** | Inert entry action |
| 10 | "Evidence — research report · Not curriculum" | **B** | Approved evidence label (design §7) |
| 11 | "Reviews" | **B** | Area label |
| 12 | "2026-09-17 · 2 reports in research/" | **C** | Date from the report filename; count of `research/*.md`. **Verified: 2** |
| 13 | "No reviews recorded yet in reviews/" | **C** | `reviews/` contains no Markdown files. **Verified: 0** |
| 14 | "README.md · AGENTS.md" | **C** | Canonical file paths |

**Category-C derivations in the roadmap overview**, and the canonical structure each derives from:

| Displayed structure | Derived from | Verified |
| --- | --- | --- |
| Sequence `Fundamentals → Advanced → Mastery → Research` | The Mermaid diagram in `ROADMAP.md`: `subgraph DEPTH` containing `F["Fundamentals"] --> A["Advanced"] --> M["Mastery"] --> R["Research"]` | Yes — parsed from that diagram, not from a hard-coded list |
| Stage numerals 1–4 | Position in that diagram's chain | Yes; the parallel track deliberately receives **no** numeral, although `ROADMAP.md` numbers its heading "5." |
| Modern AI Engineering as a parallel track | The same diagram: `MAE["Modern AI Engineering<br/>(parallel track)"]` with the bidirectional edge `DEPTH <--> MAE`; plus the canonical sentences "Modern AI Engineering is a **parallel track** rather than a fifth level." (README) and "Modern AI Engineering is not the stage after Research." (ROADMAP) | Yes |
| Axis labels "depth" / "currency" | Bold terms in the README bullets "The four core levels provide **depth**." / "Modern AI Engineering provides **currency**." | Yes — extracted, not typed |
| Stage descriptions | First paragraph of each README H3 stage section | Yes |
| Stage statuses ("Not yet designed.") | `**Status:**` labels in `ROADMAP.md` (3 occurrences) | Yes |
| Track phases | H4 headings under "Starting Point" in `ROADMAP.md` | Yes |
| Track status | `**Status:** Parallel track — detailed curriculum not yet designed.` | Yes |
| Roadmap status/purpose ("Baseline v0", "Preserve the current learning plan…") | The two-column table at the top of `ROADMAP.md` | Yes |
| Latest report title/type | The landscape report's H1 and `**Report type:**` label | Yes |

Canonical fragments appear in source order: the README preamble (lead paragraph, framing paragraph, the two questions, the closing paragraph) is reproduced verbatim and in order.

**Selection, not alteration.** Home shows two of the three H3 subsections under "Keeping the Roadmap Current"; the third, "In Short", contains only a diagram and no paragraph, so the generator's rule (first prose paragraph) skips it. Home also omits most other README and ROADMAP sections. Both are milestone-scope selection, disclosed here rather than silent: no wording was changed, and the full documents are to be rendered when the generator is expanded.

[⬆ Back to Contents](#contents)

---

## 14. Generated UI Inventory

All strings below are presentation chrome authored in templates, JavaScript or the generator. **None is canonical content, and none makes a curriculum or research claim.** Future audits should not read these as content modifications.

| Location | Strings |
| --- | --- |
| Top bar | "Open navigation", "Close navigation", "On this page", "Theme: System / Light / Dark", brand text (from the README H1) |
| Area rail | "Evidence", "Research reports and findings", "Research reports", "not generated yet", "Navigation" |
| Document page | "Home" (breadcrumb), "On this page", "Back to Top" / "Top", "Link to this section", "Close contents" |
| Evidence header | "Evidence — research report", "Not curriculum", "Research execution date", "Report type", "Canonical source" |
| Tables | "Table: <nearest heading>" (accessible name), "Wide table — scroll horizontally" |
| Diagrams | "Diagram: <nearest heading>" (accessible name), "Diagram · text form", "Diagram as text", "This diagram could not be rendered. Its source is shown below.", "Diagram rendering is unavailable. The source is shown below." |
| Code blocks | language label, "Copy", "Copied", "Code copied" |
| Links | " (external link)" (visually hidden), "Not generated in this milestone" (title) |
| Home | "Learning · Research · Curriculum maintenance", "Roadmap", "Repository", "Maintenance" (kickers), "Learning architecture", "Where things stand", "Status", "Roadmap" (labels), "N sections", "Continue to Roadmap", "Explore Evidence", "Reviews", "Understand the Project", "— not generated in this milestone", "N reports in research/", "No reviews recorded yet in reviews/" |
| Footer | "Generated from canonical Markdown:", "Presentation only. Canonical sources take precedence over this page." |
| Navigation labels | "Roadmap", "Evidence", "Reviews", "About", "(not yet available)" |

Chrome inside the article is marked `data-chrome` so machine checks can separate it from content. Shell chrome outside the article is not marked — see note **N1**.

[⬆ Back to Contents](#contents)

---

## 15. Character and Format Edge Cases

**Status: PASS.**

The strongest evidence is the character-level identity established in section 5: the canonical text and the generated text are the same string after whitespace normalization, so no character was corrupted, dropped or double-encoded.

| Case | Result |
| --- | --- |
| Non-ASCII character multiset | **identical** between source and output |
| Distinct non-ASCII characters preserved | `·` `×` `é` `–` `—` `…` `→` `↔` `⚠` `⬆` `️` |
| Ampersands (e.g. "Data & Intelligence") | correct; no `&amp;` visible in text |
| `<` / `>` and raw HTML | no `&lt;`/`&gt;` leakage; the `<div align="justify">` wrapper is removed as a presentation directive and no stray `align="justify"` remains |
| Apostrophes and quotation marks | preserved as authored (typographer conversion is disabled) |
| Em/en dashes and ranges (`2025–2026`) | preserved and distinct |
| Arrows, `⚠️`, `⬆` | preserved, including inside canonical navigation lines |
| Inline code with brackets (`[D26]`) | preserved; backticks do not leak into text |
| Escaped Markdown and literal `**` | no leakage (`**` and backticks absent from rendered text) |
| Long URLs and URLs containing parentheses | preserved exactly; wrapping is CSS-only |
| Mathematical symbols | none in this source; nothing to corrupt |

[⬆ Back to Contents](#contents)

---

## 16. Hard-Coded-Content Inspection

**Status: PASS.**

22 files were scanned (`scripts/*.py`, `scripts/sitegen/**/*.py`, templates, `site.toml`, JavaScript, CSS; the vendored Mermaid bundle excluded) for curriculum or research substance.

| Searched for | Hits |
| --- | --- |
| Curriculum topic words (retrieval-augmented, transformer, diffusion, embeddings, prompting, fine-tuning, RAG, LLM, agentic) | **0** |
| Maturity vocabulary (Established, Current practice, Emerging, Active research, Experimental, Superseded, Declining) | **0** |
| Stage names (Fundamentals, Advanced, Mastery) | **0** |
| Prerequisite or relationship language | **0** |
| Resource recommendations or book titles | **0** |
| Research conclusions | **0** |

`scripts/site.toml` contains only path-to-area mapping, navigation order, the report-matching term "Data & Intelligence Landscape" (a discovery filter, not content) and two canonical section names that Home reads from ("Learning Structure", "Keeping the Roadmap Current"). No topic taxonomy, no stage assignment, no maturity vocabulary, no relationships. Presentation strings exist as expected and are inventoried in section 14.

[⬆ Back to Contents](#contents)

---

## 17. Bugs Found

**Fidelity violations: 0.** No canonical content is added, removed, rewritten, reordered, misclassified or broken in the audited pages.

Seven notes, none of which alters canonical meaning:

| ID | Severity | Finding |
| --- | --- | --- |
| **N1** | Note (latent validation gap) | Application shell chrome outside the article (navigation labels, breadcrumbs, footer, Home kickers, entry actions, stage numerals, the `∥` glyph) is not marked `data-chrome`. The generator's wording check scopes to `<article>`, so the Evidence page is fully covered; Home has no `<article>` and is therefore **not** covered by that check today. Expanding the generator will add more composed pages, so the chrome boundary should be made explicit before then. |
| **N2** | Note (intentional) | The generated document header repeats two canonical values (research execution date, report type) that also appear in the body. Approved in design §7; the block is `data-chrome`-marked. |
| **N3** | Note (intentional) | The canonical `## Contents` section is wrapped in `<nav>` rather than `<section>`, and its H2 is styled as a small uppercase label rather than a document heading. Content and heading level are unchanged, but the visual hierarchy of a canonical heading differs from other H2s. |
| **N4** | Note (accessibility) | Each heading contains a chrome anchor whose accessible name is "Link to this section", so screen readers announce it as part of the heading. Anticipated in the design; worth a decision. |
| **N5** | Note (presentation) | The `∥` glyph is prepended inside the parallel-track H3 (`aria-hidden`, decorative). The canonical name is intact, but a decorative character sits inside a heading element. |
| **N6** | Note (derived) | Home's stage numerals 1–4 come from the canonical diagram's sequence, not from the canonical heading numbers; `ROADMAP.md` numbers Modern AI Engineering "5." and the overview deliberately gives it no numeral. This is correct per AD1, and is recorded so no future reader mistakes it for invention. |
| **N7** | Note (scope) | The milestone site presents only a subset of the repository: one canonical document in full plus selected Home fragments. Faithfulness is therefore established only for the audited pages. |

[⬆ Back to Contents](#contents)

---

## 18. Bugs Fixed

**Generator, template or presentation fixes: 0.** No fidelity bug was found, so nothing was changed and no regeneration was required. The audited build is the build the owner reviewed.

Two defects were found and fixed in the **audit harness** (in the scratchpad, outside the repository), because they produced false positives:

| Harness defect | Effect | Fix |
| --- | --- | --- |
| Text extraction joined inline elements with spaces | 192 spurious diffs such as `[D26] .` versus `[D26].` | Join inline children without separators; insert separators only at block boundaries |
| List-item extraction merged multiple paragraphs in loose list items | 37 spurious diffs and a false "missing final Back to Contents" | Emit each paragraph inside a list item separately, matching Markdown's structure |

After both harness fixes, the comparison reported zero divergences. Recording them matters: the first run *looked* like 192 content failures and was not.

[⬆ Back to Contents](#contents)

---

## 19. Ambiguities Requiring Human Review

| ID | Question for the owner |
| --- | --- |
| **A1** (from N1) | Should shell chrome be marked `data-chrome`, and should the wording check cover composed pages such as Home as well as documents? Recommended before expanding the generator. The change is machine-readable labelling only, with no visual effect — I did not apply it because it is not a fidelity violation. |
| **A2** | Home reuses canonical wording as entry titles in a new context: the README H2 "Keeping the Roadmap Current" titles the **Reviews** card, and the README H1 "AI Engineer Roadmap" titles the **About** card. The wording is canonical and unaltered, but its context is generated. Acceptable, or should these cards use UI labels instead? |
| **A3** (from N3) | Keep the canonical `## Contents` heading styled as a small label, or style it like other H2s? |
| **A4** (from N4) | Keep "Link to this section" in the heading's accessible name, or move the anchor control outside the heading? |
| **A5** (from N5) | Keep the decorative `∥` glyph inside the parallel-track heading, or move it beside the heading? |
| **A6** | Home omits the "In Short" subsection (diagram only, no prose) from the maintenance list. Keep the "first prose paragraph" rule, or render diagram-only subsections too? |

[⬆ Back to Contents](#contents)

---

## 20. Final Fidelity Verdict

> **PASS WITH NOTES.**
>
> For the two audited pages there is strong, independently obtained evidence that the generated HTML presents the canonical source material faithfully — identical headings, identical ordered content stream, character-identical text, intact tables, lists, diagrams, links, citations and canonical navigation — while adding only approved presentation behavior. No canonical Markdown was modified, and no generator change was needed.

Qualifications carried forward:

1. Mermaid **runtime rendering** is not automatically verified (section 8).
2. The chrome boundary is explicit inside articles but not in the shell (**N1** / **A1**).
3. Faithfulness is established for the Home page and one Evidence page only (**N7**).

**Recommendation on expansion.** It is reasonable to expand the generator to the full repository, provided that:

- **A1** is decided first, since more composed pages increase the value of an explicit chrome boundary;
- the ordered-stream comparison used here becomes part of the build check for every rendered document, not just a word comparison;
- documents with constructs absent from the audited sources — code blocks, mathematics, images, footnotes, task lists, deeply nested or duplicate headings — are audited when they first appear, since none of them was exercised by this milestone.

[⬆ Back to Contents](#contents)

---

## 21. Audit Method

Both sides were parsed programmatically; no conclusion rests on visual inspection alone.

| Aspect | Method |
| --- | --- |
| Independence | The Markdown side was parsed with a plain `markdown-it-py` instance and walked by a separate audit harness, so the audit cannot inherit a generator rendering bug. The generator's own validation was not used as evidence. |
| Structure | Heading tuples (level, text) compared pairwise; heading IDs recomputed with an independent GitHub-slug implementation. |
| Sequence and text | Ordered content streams (3,586 items) compared positionally, then concatenated and compared as strings; non-ASCII character multisets compared. |
| Tables | Per-table header lists, row lists and cell text compared; then per-cell link hrefs and citation labels compared (3,177 cells). |
| Lists | List counts by type, top-level item counts, and per-item text through the stream comparison. |
| Diagrams | Fence inventory versus figure inventory; canonical source text compared to the fallback `<pre>` text. |
| Links | Source link tuples (href, label, autolink flag) versus generated anchors and inert spans; fragment targets resolved against the page's `id` set. |
| Home provenance | Every substantive text node extracted, then matched against the **parsed** (markup-free) text of each canonical source; unmatched nodes classified by hand and every derived fact re-verified against the repository. |
| Hard-coded content | Regular-expression scan of 22 generator, template, config, JS and CSS files for curriculum and research vocabulary. |
| Build currency | `site/build-manifest.json` source hashes compared with the current canonical files. |

Audit scripts were kept outside the repository (session scratchpad) to avoid adding unapproved structure. They can be recreated from this section; if the ordered-stream check is adopted as a build check, it should move into `scripts/` with its own review.

[⬆ Back to Contents](#contents)


---

## 22. Final Version 1 Audit

**In this section:** [Result](#result) · [Scope](#scope) · [Independent comparison](#independent-comparison) · [Build checks](#build-checks) · [Composed pages](#composed-pages) · [Milestone notes and ambiguities](#milestone-notes-and-ambiguities) · [Fixes made during the audit](#fixes-made-during-the-audit) · [Known limits](#known-limits)

| | |
| --- | --- |
| **Audit date** | 2026-09-18 |
| **Audited build** | Site Version 1, generator `1.0.0`; 22 pages from 16 canonical documents |
| **Changes made to canonical Markdown** | None to curriculum, research, design or governance content. `README.md` "Current Status" wording was updated as authorized, and this file's title was generalised to cover both audits |

### Result

> **PASS.**
>
> Every canonical document the site presents matches its source exactly in ordered wording, heading sequence, table cells and code and diagram text. Interface text is marked as chrome everywhere, and composed pages present only canonical words or marked interface text.

### Scope

All sixteen Markdown documents reached by the routes in `scripts/site.toml`: `ROADMAP.md`, `README.md`, `AGENTS.md`, `MAINTENANCE.md`, `PROJECT-STATE.md`, three `design/` records, `history/roadmap-baseline-v0.md`, `prompts/landscape-research.md` and six `research/` reports. There are no review reports yet. Composed pages audited: Home, the Roadmap overview, and the Evidence, Reviews and About landings.

### Independent comparison

A harness written for this audit, with its own parser configuration (CommonMark plus tables) and its own HTML extraction, compared each source with the `<article>` of its generated page, excluding `data-chrome`:

| Measure | Result |
| --- | --- |
| Ordered word sequence | Identical for all 16 documents (about 136,000 words) |
| Heading sequence (level and text) | Identical (613 headings) |
| Table cells, in order | Identical (16,418 cells) |
| Code and diagram source text | Identical |

### Build checks

The generator now checks, for every document on every build: ordered wording; counts of headings, tables, lists, quotes, diagrams, code blocks, rules and links; every heading anchor; internal links and anchors across all pages; one `<main>` and one `<h1>` per page; no remote assets; vendored Mermaid present. This adopts the milestone recommendation that ordered comparison become a build check. Deliberate perturbations — reordered words, an inserted word, an unmarked invented word and a removed table — were each caught.

### Composed pages

Home, the Roadmap overview and the landings are built from extracted canonical fragments: the architecture diagram, the stage bullets, block tables, the depth table, labelled paragraphs, the parallel-track table, the Dependency Map, the Maintenance sections and the maintenance state file. Each page's unmarked words must exist in the sources it draws on; all passed. The "what depends on this block" panels in the roadmap list exactly the Dependency Map's 33 hard and 3 recommended edges and infer nothing else.

### Milestone notes and ambiguities

| Item | Version 1 disposition |
| --- | --- |
| **N1 / A1** — shell chrome unmarked | Resolved. Top bar, drawers, area navigation, breadcrumbs, On this page, footer, floating controls, markers, panels and generated labels carry `data-chrome`. Article content was not marked to pass a check |
| **A2** — README headings reused as card titles | Superseded. Home no longer reuses them; cards use interface labels |
| **A3, A4, A5** — Contents styling, heading anchor name, `∥` glyph | Unchanged from the milestone; presentation only, no fidelity effect |
| **A6** — "In Short" omitted from Home | Superseded. Home no longer lists maintenance subsections |
| **N7** — only a subset generated | Resolved. All routed documents are generated |

### Fixes made during the audit

| Defect | Fix |
| --- | --- |
| Plain file names such as `AGENTS.md` were auto-linked as web addresses (`.md` is a top-level domain) | Only bare URLs are linked, as on GitHub |
| Angle-bracket placeholders (`<date>`, `<file>`, `<nearest heading>`) passed through as unknown HTML tags, leaving unbalanced markup | Rendered as visible text |
| A link rewritten for one page leaked into a second render of the same document | Links resolve from the original source address on every render |

### Known limits

- Mermaid runtime rendering is still not verified automatically; the text form is always present.
- The composed-page check verifies vocabulary, not phrasing; composed pages are covered by this audit rather than by the build.
- `ROADMAP.md` §16 says the detailed maintenance procedure "is not yet written"; `MAINTENANCE.md` now exists. The presentation shows the canonical wording unchanged; the correction belongs to the first curriculum review.

[⬆ Back to Contents](#contents)

---

## 23. Learner-Guide Audit

| | |
| --- | --- |
| **Audit date** | 2026-09-19 |
| **Audited build** | Generator `1.1.0`; 47 pages from 18 canonical documents, 24 of them learner-guide pages |
| **Result** | **PASS** |

**What changed.** The learner no longer reads ROADMAP.md as the interface. [LEARNING-GUIDE.md](../LEARNING-GUIDE.md) presents Baseline 1 as one path, one page per step; ROADMAP.md is published under About as the specification ([design/learner-guide.md](learner-guide.md)). Fidelity therefore has two parts: pages must match their own source, and the guide must match the specification.

| Check | Result |
| --- | --- |
| Every document page against its source — ordered words, headings, table cells, code (independent harness) | Identical for all 17 documents |
| All 24 guide pages, concatenated in reading order, against the guide's step sections (independent harness) | Identical (about 6,700 words) |
| Guide delivers every block, capability, path, phase and readiness gate of ROADMAP.md | Pass (build check) |
| Every resource assigned to a block appears in the step that delivers it; every parallel-track resource appears in the guide | Pass (build check) |
| Every prerequisite and phase opening comes earlier in the path | Pass (build check); a deliberate reordering was caught |
| No internal identifier or curriculum-design vocabulary on Home or any learner page | Pass (build check and independent scan) |
| One navigation mechanism on learner pages — no right-hand contents and no in-page Contents block | Pass |
| No pages from the previous architecture remain | Pass |

The earlier requirement that every ROADMAP.md word appear on the learner's roadmap page no longer applies to the learner experience: the specification page still meets it, and the guide pages meet it against the guide.

[⬆ Back to Contents](#contents)

</div>
