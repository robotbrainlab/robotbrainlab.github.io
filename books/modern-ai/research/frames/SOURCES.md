# The source register — REVOKED 2026-11-11

> ## ⚠ This is a record. It is not an input, and no run may be given it.
>
> **`[STATED 2026-11-11]` The owner revoked this register.** His reasoning: a fixed list of sources
> decides what can be found, which makes it scope rather than method, and a run that inherits it is
> not reading the field independently — it is re-reading one earlier run's idea of where the field
> lives. He revoked his own `[AGREED 2026-11-07]` decision to adopt it. `../../docs/GOAL.md` §3.3
> carries the decision and what it costs.
>
> **What replaces it:** each framing run finds its own sources, under a source floor and a search
> floor, and **two or more runs per cycle are unioned, never intersected**
> (`../../docs/briefs/TEMPLATE-area-frame.md`).
>
> **Why this file is kept.** It is evidence of what six runs found between 2026-11-06 and
> 2026-11-07 — which pages were reachable on which date, which returned 403, and what each was
> recorded as carrying. That is history worth having. **Pasting any part of it into a brief is
> forbidden**, including the routes: a route is still a previous run's finding.

**What this was.** Every filing system any framing run had opened, with the level to take from it
and what it was already found to carry. **A framing run read this list and did not choose its own
sources.** That is no longer how framing works.

**Why it exists.** Six framing runs ran between 2026-11-06 and 2026-11-07. Each chose its own
sources, because the brief told it to. **Only two sources were opened by all six** — the arXiv
taxonomy and the MLCommons benchmark index. Four venues were read at different editions by different
runs. So each run re-drew its own input, and **nothing a run discovered was available to the next
one**. Two consequences, both measured:

1. **Coverage did not accumulate.** Run `d` reached a standards body's five working groups through
   a Wikipedia page after the body's own site returned 403. Run `e`, a day later, hit the same 403,
   searched once, gave up, and wrote that this was "the single biggest hole" in its list. **The
   route had already been found and recorded in this directory.** The same happened three times over
   with the ACM classification: `c`, `e` and `f` each hit the same blocked page and each spent
   searches hunting a route of its own.
2. **Improving the brief could not improve the output**, because the brief governs how a run
   reports and the sources govern what there is to report.

**What it is not.** It is not a taxonomy. **The part of it a framing run sees names no area, no
category and no expected outcome** — a source is a place to look, and that is not an answer. The
`CARRIES` column does name categories, which is exactly why it is withheld; see the box below. The
brief still forbids a run from reporting any category it did not read at a source.

**How `CARRIES` is to be read, and why the run never sees it.** Every `CARRIES` line is **what a
named run recorded after reading that page**, not a reading of my own. It is the floor for a
regression check: a run that opens one of these pages and reports less than this has failed, and the
failure is visible without opening the page. Where two runs disagreed about a page, both readings are
given.

> ### The `CARRIES` column is withheld from the framing run
>
> **When this register is pasted into `../../docs/briefs/TEMPLATE-area-frame.md`, the `CARRIES`
> column is deleted first.** The run is given the URL, the kind, the level and the route. It is never
> given what it is expected to find.
>
> **Why.** The brief's oldest rule is that *an instrument told what to expect finds it.* A run shown
> "this page carries AI Alignment" can report AI Alignment without establishing it, and **the check
> then tests nothing** — it compares the run's output against the text the run was handed. The whole
> value of the floor is that the run did not know where the floor was.
>
> **A URL and a level are not answers.** "Open the arXiv taxonomy at the category level" says where to
> read and nothing about what is there; the page decides that. **A list of expected categories is an
> answer.** That is the line, and it is the reason this register can exist at all without breaking the
> rule it sits under.

**Maintaining it.** A framing run may add at most two sources it finds itself, reported for addition
rather than added by the run. Nothing is ever removed: a source that stops resolving becomes
`UNREACHABLE` with the date and what was lost.

**Floors only ever ratchet upwards.** A `CARRIES` floor is built from what an earlier run found, and
an earlier run can have misread the page — **one of these floors was found to be too low within
hours of being written**, by reading the source instead of trusting the run that reported it. So
whenever anybody reads a source properly, the floor rises and stays risen; it is never lowered to
match a run. **A floor that is too low lets a defect through once. It cannot create one.**

---

## 1. Read these

**Every table here has four columns. The first three go to the framing run. `CARRIES` does not** —
see the box above. Anything a run genuinely needs in order to read a page correctly is in **"Level
and route"**, phrased as where to read and never as what is there.

**`CARRIES` was ratcheted up on 2026-11-07 by run `g`**, which opened all nineteen and is the first
run to do so. Where run `g` found more than an earlier run, its number is the floor now.

### `index` — subject classifications of archives and catalogues

| Source | URL | Level and route | CARRIES — **withheld** |
|---|---|---|---|
| arXiv category taxonomy | `https://arxiv.org/category_taxonomy` | **Category** (subject class). Above: the `cs` group. No level below. **Branch to read, fixed so that cycles compare:** `cs.AI` and the categories its own description names as having their own subject areas, plus `cs.NE` and `stat.ML`. The archive's other `cs` categories are outside that branch — **say so** | **8 categories** (`cs.AI`, `cs.CL`, `cs.CV`, `cs.LG`, `cs.MA`, `cs.NE`, `cs.RO`, `stat.ML`). Run `g` reported them as **7 units**, merging `cs.LG` and `stat.ML` on their identical name and recording the split as a disagreement — a documented merge, not a loss |
| ACM CCS 2012, as the browse-by-subject tree of the UCT computer-science repository | `https://pubs.cs.uct.ac.za/view/subjects/` | **Children of "Computing methodologies"**, and **children of "Artificial intelligence"**. Both levels, with the holdings count each node shows. **This rendering is partial by construction** — only nodes holding items appear, so **name the nodes you would expect at that level and do not find**, and take them from the vocabulary server below | **12 of 16.** Run `g`: 6 + 6 shown against 8 + 8 in the scheme. The four absent here are `Distributed computing methodologies`, `Symbolic and algebraic manipulation`, `Planning and scheduling`, `Search methodologies` — **all four recovered from the vocabulary server by run `g`, and all four lost by runs `c`, `e` and `f`** |
| ACM CCS 2012 on the TemaTres vocabulary server | `https://vocabularyserver.com/acm/12/?tema=5214` (**"Machine learning approaches"**) and `?tema=4748` (**"Computing methodologies"**, from which the "Artificial intelligence" node is reached) | The node's own children, **at each of the two nodes named in the URL column** — the register used to say only "the node's own children", and run `g` correctly reported that as under-specified. **Use the bare `?tema=` form: the `index.php?tema=` form returns 403** and cost run `g` a fetch. **This is the working route to the CCS subtree** — earlier runs failed to reach it by any other route, so do not go looking for one | **29.** Run `g`: 13 children of "Machine learning approaches", plus 8 + 8 at the Computing methodologies and Artificial intelligence levels |

### `review-venue` — submission and review categories

| Source | URL | Level and route | CARRIES — **withheld** |
|---|---|---|---|
| **AAAI main technical track call** | `https://aaai.org/conference/aaai/aaai-26/main-technical-track-call/` | The prose "Topics" list, **and every track named beside the main track on the same page.** The tracks beside the main track are part of this level and are easy to read past | **15.** Run `g`: 12 prose topics and 3 subject-named technical tracks, the page's own Summary counting "Three technical tracks (Main Track; AI for Social Impact; AI Alignment)". **Checked at source by hand, 2026-11-07.** Runs `c` and `d` found the alignment track here too; runs `e` and `f` missed it by reading only the later cycle's page |
| AAAI keywords and subtopics | `https://aaai.org/conference/aaai/aaai-26/keywords/` | **Top-level area.** Below: the per-area keywords | **16 areas**, holding 296 keywords (run `g`) |
| AAAI areas and topics, later cycle | `https://aaai.org/conference/aaai/aaai-27/areas-and-topics/` | **Area.** Below: the per-area topics. **Read this page in addition to the main technical track call above, never instead of it** — this one covers the main track alone, and the tracks beside it are not on it | **17 areas**, holding 203 topics, and **no tracks beside the main track.** Run `g` records that these 17 contain no alignment area at all |
| NeurIPS call for papers | `https://neurips.cc/Conferences/<cycle>/CallForPapers` | **Flat topic list.** No level above or below published. **Name the cycle you read** | **21** (2026 cycle). 12 in the 2025 cycle |
| ICLR call for papers | `https://iclr.cc/Conferences/2026/CallForPapers` | **Flat.** **Name the cycle you read** | **20**, in a list the page itself calls non-exhaustive |
| ICML call for papers | `https://icml.cc/Conferences/2026/CallForPapers` | **Flat.** **Name the cycle you read** | **10** |
| ACL main conference call, submission topics | `https://2026.aclweb.org/calls/main_conference_papers/` | The submission-topic list. **Name the cycle you read** | **34** (2026 cycle), the theme track first. **One of the 34 has a stated one-year life** — the theme track changes each cycle and the page says so |
| CVPR call for papers, subject areas | `https://cvpr.thecvf.com/Conferences/2026/CallForPapers` | Subject areas | **37** |
| AAMAS call for papers, areas of interest | `https://cyprusconferences.org/aamas2026/call-for-papers-main-track/` | Areas of interest | **11**, holding about 150 topics |
| IJCAI-ECAI call, **via the AEPIA reproduction** | `https://www.aepia.org/ijcai-ecai-2026-call-for-papers/` | **Flat**, one comma-separated sentence. **Use this route.** The conference's own main-track page carries no area list — it says the keyword list lives on the submission site, which is not public | **14** |

### `practitioner` — industry, standards and benchmark classifications

| Source | URL | Level and route | CARRIES — **withheld** |
|---|---|---|---|
| MLCommons benchmarks index | `https://mlcommons.org/benchmarks/` | **Named suite, and named working group** (the working groups are at `/working-groups/`). **Read the level exhaustively and count it** — an earlier run reported most of this level, not all of it, and lost the entries that were unlike the rest. The loss was invisible in its output | **12 suites and 22 working groups in 4 families** (run `g`, from 34 labels merged to 30 units where a suite and a group share a name). Earlier floor was 12 and 9. **The two suites unlike the rest are the two that measure something other than speed**; run `e` dropped exactly those two |
| MLPerf inference rules, the benchmark tables | `https://raw.githubusercontent.com/mlcommons/inference_policies/master/inference_rules.adoc` | **Area** level, **across both the Datacenter and the Edge table — they share Areas, so count the distinct Areas and not the rows.** Above: the suite. Below: the per-area tasks | **7 distinct Areas** (6 in Datacenter, 4 in Edge, 3 in both). **An earlier floor of 10 was wrong**: it added the two tables' rows and double-counted the three shared Areas |
| LF AI & Data landscape source file | `https://raw.githubusercontent.com/lfai/lfai-landscape/main/landscape.yml` | **Category.** Below: the per-category subcategories. **Read the file as one piece** — it is about 3,470 lines; two earlier runs read it in parts and a category header fell across the split, which cost one category in one run and misplaced it in the other | **14 categories**, holding 45 subcategories. Run `g` read it in one pass and lost none |
| **ISO/IEC JTC 1/SC 42, via Wikipedia quoting the subcommittee's own working-group titles** | `https://en.wikipedia.org/wiki/ISO/IEC_JTC_1/SC_42` | **Working group. The level has two tables and both are part of it** — the subcommittee's own working groups, and the joint working groups it administers with other subcommittees, which sit immediately below in the same section. Below the level: individual standards projects. **Use this route and do not search for another** — the body's own site is in section 3, and this is the only route any run has reached. Take the titles as the subcommittee's, and say that the route is a third party quoting them | **8 groups.** WG 1 Foundational standards · WG 2 Big Data · WG 3 Trustworthiness · WG 4 Use cases and applications · WG 5 Computational approaches and characteristics of artificial intelligence systems · JWG 2 Testing of AI-based systems · JWG 3 AI enabled health informatics · JWG 4 Functional safety and AI systems. **Checked at source by hand, 2026-11-07.** Run `d` found 5 and missed the 3 joint groups; **run `g` found all 8.** The page also says it lists study and advisory groups and then names none — run `g` reported that contradiction. **The only source any run reached that carries terminology, conformance and management-system categories** |

### `programme` — meeting tracks

| Source | URL | Level and route | CARRIES — **withheld** |
|---|---|---|---|
| AI Engineer World's Fair, machine-readable programme | `https://ai.engineer/wf/llms.md` | **Track.** Above: the conference day and the room split. Below: individual talks, which are not named categories. **Name the event year.** **Two fetches**: this URL is an HTML shell that loads its content from `https://ai.engineer/worldsfair/<year>/llms-full.md`, and the year it serves moves — it served 2025 in November 2026 and now serves 2026, so **this and the 2025 page below are two editions, not two views of one** | **50 distinct `Track:` values, of which 32 are subject names** (run `g`, 2026 event). The other 18 are room, stage, day and placeholder labels |
| AI Engineer World's Fair, programme page | `https://www.ai.engineer/worldsfair/2025` | **Track. The page contradicts itself about how many tracks it has** — report the number you can count at the level you took, and report the contradiction | **18 subject-named tracks** of 19 labelled entries (run `g`); the 19th names the expo floor. The page separately claims 18 and 12 |

## 2. Do not read these

| Source | Why | Established by |
|---|---|---|
| Stanford HAI AI Index report | **It is not a `survey` source under the brief.** Its chapters file measurements of AI's effect on the world, not submissions, so they answer a different question. The consolidator rejected ten records drawn from it as `RECORD` | Runs `d`, `e`, `f` all read it; the 2026-11-07 brief fix excludes it. Reading it costs a fetch and yields rejects |
| `aima.cs.berkeley.edu/topics.html` | A third-party mirror of the CCS AI subtree on a textbook site, with teaching annotations appended. Run `e` used it only for category names and still recorded that it **disagrees with the UCT rendering about where `Machine learning` sits**. The vocabulary-server route above is authoritative and reachable | Run `e` |

## 3. Unreachable — do not spend searches on these again

| Source | What happened | What is lost, and the route that works |
|---|---|---|
| ACM's own CCS pages — `dl.acm.org/ccs`, `acm.org/about/class/2012`, `acm.org/publications/class-2012-intro` | **403 to runs `c`, `e` and `f`; TLS handshake failure to run `d`.** Internet Archive is blocked to the fetch tool, and two Wayback mirrors failed TLS | The authoritative tree. **Routes that work:** the vocabulary server for the subtree, the UCT repository for a partial rendering. Treat CCS placements as unconfirmed |
| ISO/IEC JTC 1/SC 42 committee page — `iso.org/committee/6794475.html`, `psqca.isolutions.iso.org/committee/6794475.html` | **403 to runs `c`, `e` and `f`.** Run `f` also found the SC 42 business-plan PDF fetched but unreadable (compressed streams), and a third-party standards page carrying no working-group list | The subcommittee's own page. **The route that works is the Wikipedia page in section 1**, which quotes the working-group titles. **This is not a limit of the world** — the 2026-11-07 validation recorded it as one, and that was wrong |
| `aijobs.net`, `ai-jobs.net` | **Both 301-redirect to `foorilla.com`**, whose hiring section carries no categories. Attempted four times across runs `c` and `d` | A role or occupational taxonomy. **No route found.** So MLOps-, research-engineer- and data-engineer-shaped categories are absent from every run, and **the absence is the instrument's, not the field's.** This one is a genuine gap |
| IJCAI 2025 call page — `2025.ijcai.org/?p=1068` | Run `f` reported reading four special tracks from it. **The page would not load when that claim was checked**, so what it carries is unverified | Use the AEPIA route in section 1 instead |

---

## 4. What every source of these kinds misses

Carried forward from the runs' own accounts, because it does not change between runs and should not
be rediscovered each time:

- **Work that is not submitted, reviewed, indexed or advertised anywhere** is invisible to every
  source here. Run `c` names classified and defence work.
- **Categories named only in languages other than English.** Every source in section 1 is English.
- **Anything established since the newest source.** The oldest source here is the ACM scheme of
  2012, fourteen years old.
- **Roles and occupations** — see section 3.
- **The academic and applied halves are nearly disjoint.** Across the four runs merged in
  `MERGED-CANDIDATES.md`, 154 categories were named only by review venues and indexes, 49 only by
  benchmark suites, standards bodies and programmes, and **only 41 by both.** A list drawn from
  either half alone misreports the other.
