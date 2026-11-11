# Area proposal — step 4 part 3

**Written 2026-11-12 to `briefs/area-proposal.md`, from
`../research/frames/CONSOLIDATED-2026-11-12.md`.** Claude proposes; **the owner rules.**

**The headline recommendation is that almost nothing is cut yet, and why.**

---

## `[STATED 2026-11-12]` THE OWNER'S RULING

**He was given four questions and ruled on all four. Nothing below this line was changed to match;
the proposal as put to him stands, and this records what he decided about it.**

| # | Question | Ruling |
|---|---|---|
| 1 | Choose the areas now from the 47 that carry a scope statement, or read the 99 that do not first? | **Read them first.** One targeted run over the 62 named pages, then he chooses from the whole list. **This is now the next action**, ahead of any cut |
| 2 | The twelve measurement suites: one area or twelve? | **One area, with all twelve named underneath**, so none is lost |
| 3 | Robotics, Intelligent Robots and Control methods: one area or three? | **Keep all three. Decide after the research** says whether they are the same work under three names |
| 4 | The five remaining same-ground pairs | **Keep apart for now**, and let the research settle each |

**What rulings 2, 3 and 4 do to the count.** The consolidation issued **47** `AREA` verdicts. This
proposal folds **3** of them as containers. Ruling 2 folds **12** more into one new area. So the
proposed list is **33 areas**: 32 kept exactly as the consolidation named them, plus one new
measurement area absorbing twelve. **32 + 12 + 3 = 47** — every `AREA` verdict accounted for.

**Rulings 3 and 4 keep eleven rows that a tidier list would have merged.** That is deliberate and
it is his: **keeping a pair costs one reading; merging a pair wrongly hides one of the two**, and
the research is what will settle them with evidence rather than with a judgement nobody can check.

**`[CORRECTED 2026-11-12]` This file said "41 KEEP" below. It is 44** — rows 1 to 32, plus ten
MLPerf rows, plus AILuminate and AlgoPerf. The arithmetic section had it right at 44 and the
heading did not. After ruling 2 the figure is **33**.

---

## Criteria

**`GOAL.md` §1.1 `[STATED]` — the career goal, in the owner's words.** The objective is to become a
strong candidate for roles such as **AI Researcher, Research Engineer, AI Engineer, Machine
Learning Engineer**. Explicitly not staying informed:

> *"My ultimate objective is not simply to stay informed about AI advancements. I want to
> systematically build a deep understanding of both the scientific foundations and the latest
> research and engineering developments across these areas."*

Four capabilities, all four wanted together: **theoretical depth · research awareness ·
experimentation skill · hands-on engineering.** And the identity:

> *"I am not trying to become someone who only studies or summarizes research. I want to develop
> into a **research-oriented engineer** who understands the science, follows the research, and
> knows how to apply that knowledge through engineering."*

**`GOAL.md` §3.1 `[STATED]` — the five questions every area must answer:** ongoing research ·
engineering developments · established scientific knowledge · research-to-engineering transition ·
skills and career relevance.

**`GOAL.md` §3.3:** *"a finding can be wrong. A partition can only be worse or better for a
purpose."*

**No test is invented here.** Where a decision needs one the owner has not written, it is named
under *What this stage could not settle* and left undecided — `briefs/area-proposal.md` requires
that, because the first run of this stage wrote its own operative test and that test is what
removed robotics.

---

## The recommendation, before the rows

**Cut nothing on subject grounds yet. Fold only what the evidence licenses. Then go back for the
62 missing scope statements before any area is cut.**

Three facts drive this, and all three are the consolidation's own:

1. **99 of 223 categories are undecided** — 44% — every one of them for the same reason: the source
   published a name and no scope statement.
2. **Almost the whole engineering vocabulary is in that pile.** Of the 47 areas, 13 were named by
   applied sources and **12 of those 13 are MLCommons measurement suites**. *Evals*, *Inference*,
   *Context Engineering*, *Agent Reliability*, *AI Infrastructure*, *SWE Agents*, *Posttraining &
   Midtraining*, *Memory & Continual Learning*, *Local AI*, *GraphRAG*, *Computer Use*, *Agentic
   Engineering* are all undecided. The consolidation's own sentence: *"A book on the engineering of
   AI that took only this run's `AREA` list would have almost no engineering in it."*
3. **No area is named by both an academic and an applied source.** 34 academic-only, 13
   applied-only, zero shared.

**Cutting now would cut the half that has scope statements while the half that does not is still
unread.** `GOAL.md` §1.1 asks for a research-oriented engineer — science *and* research *and*
engineering together — so a list built only from what happens to publish scope sentences cannot
serve it. **That is a judgement about the instrument, not about the field**, and it is the same
shape as the robotics loss: a decision taken where nobody can see what it dropped.

**What to do instead — and this is a recommendation, not a decision taken.** 62 of the 99 are
programme tracks (33) and ACL Rolling Review tracks (29). The consolidation says exactly what would
settle them: for ARR, *"ARR's separate area-guide page, which neither run opened"*; for the
programme, a per-track description. **That is one short, targeted research run with a named list of
pages — not a new framing run.** It would move most of the engineering vocabulary from *undecided*
to *judged*, and only then is a cut safe.

---

## Proposed areas

**44 KEEP as put to the owner; 33 after his ruling 2** (see the ruling, above). Every one passes
`GOAL.md` §1.1 on its own row. **No area is kept or cut by a reason
shared with another** — the brief forbids it.

| # | Area | Sources | Why it serves §1.1 |
|---|---|---|---|
| 1 | Machine Learning | 4 | The largest area in every source carrying it, and the one §1.1 names in a job title. Covers "all aspects of machine learning research … including also robustness, explanation, fairness, and methodology" |
| 2 | Computer Vision | 4 | A named research area of AI in four sources; a modality the owner's target roles build on |
| 3 | Natural Language Processing | 4 | **The one area every kind of source in both runs files.** Its `BELOW` holds the 31 ARR tracks and AAAI's 24 keywords including (Large) Language Models |
| 4 | Knowledge Representation and Reasoning | 4 | The science of representing and inferring; carries theorem proving, which `cs.AI` names and nothing else would keep |
| 5 | Multiagent Systems | 4 | Agents acting together — filed by a venue, an archive and an index. **Cut silently last time**; kept here on four sources |
| 6 | Robotics | 3 | Carved out of `cs.AI` by name in the archive. **The area the first run of this stage cut**; kept |
| 7 | Evaluation | 3 | Engineering includes its measurement. Directly serves capability 3, experimentation skill |
| 8 | Planning and scheduling | 3 | Deciding what to do; a child of "Artificial intelligence" in the one index that subdivides AI |
| 9 | Theory | 3 | The science of what can be learned and at what cost — capability 1, theoretical depth |
| 10 | Deep Learning | 2 | The model class modern AI runs on: "architectures, generative models, optimization for deep networks, foundation models, LLMs" |
| 11 | Reinforcement Learning | 2 | Learning to act; both ML venues file it at the top level |
| 12 | Optimization | 2 | How models are fitted — the mechanism under capability 1 |
| 13 | Probabilistic Methods | 2 | Inference under uncertainty: variational and causal inference, Bayesian methods, Monte Carlo |
| 14 | Reasoning under Uncertainty | 2 | An AI venue's own area for inference, decision and causality. Kept separate from 13 — see the question to the owner |
| 15 | General Machine Learning | 2 | The residual method topic at two venues that are entirely ML; run i's record says the qualifier marks it as such |
| 16 | Infrastructure | 2 | **The engineering of AI** — libraries, scalability, hardware, distributed methods. One of only two engineering-mode areas with a scope statement |
| 17 | Humans and AI | 2 | How systems and people work together; carries explainability and human-in-the-loop ML |
| 18 | Data Mining & Knowledge Management | 2 | Knowledge graphs, recommendation, retrieval-adjacent work, semantic web |
| 19 | Search and Optimization | 2 | Heuristic, adversarial and distributed search; evolutionary computation |
| 20 | Search methodologies | 2 | The index's own search node. Kept separate from 19 — see the question to the owner |
| 21 | Intelligent Robots | 2 | An AI venue's own robotics area, with 12 keywords including Embodied AI. Kept separate from 6 — see the question |
| 22 | Philosophy and Ethics of AI | 2 | Carries AGI, safety, accountability and the philosophical foundations as a submission area |
| 23 | Trustworthy Machine Learning | 1 | "causality, fairness, interpretability, privacy, robustness, safety" — the properties a deployed system must hold. Capability 4 |
| 24 | Social and economic aspects of machine learning | 1 | Judged from the record, not the name: fairness, interpretability, privacy, safety as system properties |
| 25 | Cognitive Modeling & Cognitive Systems | 1 | The science of intelligence as an AI venue files it — capability 1 |
| 26 | Constraint Satisfaction and Optimization | 1 | Solvers, satisfiability, constraint programming |
| 27 | Control methods | 1 | Robotic planning, computational control theory, motion path planning. **Lost silently last time**; kept |
| 28 | Game Theory and Economic Paradigms | 1 | Mechanism design, equilibrium, social choice — and adversarial learning |
| 29 | Planning, Routing, and Scheduling | 1 | The same ground as 8 plus routing and **planning with language models**. Kept separate — see the question |
| 30 | Philosophical/theoretical foundations of artificial intelligence | 1 | Cognitive science and theory of mind as foundations. The smallest CCS node and the only one that is pure science |
| 31 | cs.NE (Neural and Evolutionary Computing) | 1 | Neural networks, connectionism, genetic algorithms, adaptive behaviour — the mechanisms under capability 1 |
| 32 | Retrieval + Search | 1 | **One of only two programme tracks in either run with a scope statement**, and the only applied area that is not a benchmark suite. Engineering of deployed AI |
| 33 | **Measuring AI systems** `[STATED 2026-11-12]` | 1 | **The owner's ruling 2.** One area absorbing all twelve MLCommons suites, each named underneath so none is lost: MLPerf Training · MLPerf Training: HPC · MLPerf Inference: Datacenter · MLPerf Inference: Edge · MLPerf Inference: Mobile · MLPerf Inference: Tiny · MLPerf Endpoints · MLPerf Client · MLPerf Automotive · MLPerf Storage · AILuminate · AlgoPerf. **Evidence for the fold: one source, one body, one purpose** — measuring how fast or how safely an AI system runs. **It loses nothing**: every suite is a named child, and the two the consolidation refused to merge on a copy-pasted sentence stay distinct children rather than becoming one |

*(As put to the owner this was twelve rows, 33 to 44. His ruling made it one, and the twelve are
carried as its children.)*

## Folds

**Three, each on evidence the brief accepts, and each naming what it carries forward.**

| Fold | Absorbs | Evidence | Carries forward | Loses |
|---|---|---|---|---|
| **Into the eight areas it wraps** | `Artificial intelligence (ACM CCS, above the chosen level)` | The consolidation's own flag: it *"wraps eight areas that are themselves at the chosen level"*, and names all eight. Every one is a kept area above | Nothing to carry: its eight children are rows 2, 3, 4, 8, 20, 27, 30 and — as Multiagent Systems — row 5 | **Nothing.** Its only content is the eight children |
| **Into rows 2, 3 and the speech material under them** | `Applications` (NeurIPS) | Its `COVERS` is "vision, language, speech and audio, Creative AI" and its own `BELOW` says these are Computer Vision, NLP and the speech material under them | Vision → row 2; language and speech → row 3 | **`Creative AI` has no other home in the list.** Named here so it is not lost silently |
| **Into rows 3, 4, 8 and 14** | `cs.AI (Artificial Intelligence)` | Defined by the source by subtraction — "all areas of AI except Vision, Robotics, Machine Learning, Multiagent Systems, and Computation and Language" — and its named contents are "Expert Systems, Theorem Proving …, Knowledge Representation, Planning, and Uncertainty in AI", all of which are kept areas | Knowledge Representation → row 4; Planning → row 8; Uncertainty in AI → row 14; Theorem Proving → row 4's AAAI keyword *Automated Reasoning and Theorem Proving* | **`Expert systems` has no other home in the list.** Named here, not dropped. It was one of the things the first run of this stage lost without naming |

## Cuts

**None proposed.** Not one of the 47 areas fails `GOAL.md` §1.1 on its own row, and the brief
forbids cutting an area for being small, quiet or unfashionable. **The case for cutting is a case
about the book's size, which is step 7's question and not this stage's.**

## What each cut takes with it

**Not applicable — nothing is cut.** The three folds' losses are named in the Folds table:
**`Creative AI`** and **`expert systems`**, both of which lose their only home in the list. Both are
recorded under *What this stage could not settle*.

## The five-at-a-time check

**The brief asks for the sentence I would say if the owner asked why the field's own most-filed
subject is not in his book. There is no such sentence to write, because nothing is cut** — and
that is the check doing its job rather than being skipped. The five best-attested areas are
Machine Learning, Computer Vision, Natural Language Processing, Knowledge Representation and
Reasoning and Multiagent Systems, all at four sources. **All five are kept, and Multiagent Systems
and Robotics — the two the first run cut — are rows 5 and 6.**

## Disposition of every `UNCLEAR`

**99 categories. 62 of them get the same disposition, and it is not a cut.**

| Block | Count | Disposition |
|---|---|---|
| AI Engineer World's Fair programme tracks | 33 | **Held, pending one targeted fetch.** These carry most of the engineering vocabulary. Judging them on their names is what policy P1 exists to prevent |
| ACL Rolling Review tracks | 29 | **Held, pending ARR's area-guide page**, which neither run opened. All 31 are already recorded under Natural Language Processing's `BELOW`, so **none is lost whatever happens** — the question is only whether any deserves to be an area of its own |
| Stanford CRFM subsections | 14 | **Held.** Settled by the report's own section text. *Adaptation*, *Training*, *Modeling*, *Systems*, *Interpretability* and *AI safety and alignment* would each be substantial if their scope confirms what the names suggest |
| AAAI Presidential Panel chapters | 13 | **Held.** Settled by the report PDF, which run h could not open. Includes *AI Agents*, *Embodied AI*, *Hardware & AI* and *Artificial General Intelligence* — none of which any other source files as a top-level category |
| ISO/IEC JTC 1/SC 42 groups | 10 | **Held.** Settled by ISO's own committee page, which refused both runs. *WG 3: Trustworthiness* overlaps row 23; the rest do not obviously overlap anything kept |

**No `UNCLEAR` is cut here, and that is deliberate.** Each is undecided because a *source* did not
publish a scope statement — which is a fact about the source, not about the subject. Cutting on
that would be cutting on absence of evidence.

## Borderlines inherited

| The consolidation flagged | What this stage did |
|---|---|
| **13 arXiv categories rejected as *"not AI"* but marked Close** (cs.AR, cs.CR, cs.DB, cs.DC, cs.GT, cs.HC, cs.IR, cs.LO, cs.PF, cs.SC, cs.SD, cs.SE, cs.SY) | **Accepted the rejections.** Each line names the kept area that still carries its AI-specific ground, and I checked that each named area is in fact kept: cs.GT → row 28; cs.HC → row 17; cs.IR → rows 18 and 32; cs.LO → row 4; cs.PF → the MLPerf rows; cs.SD → row 3; cs.SE → row 3's keyword; cs.SY → row 27. **cs.AR (hardware) and cs.DC (distributed) are the two whose ground is carried only by row 16, Infrastructure** — flagged below |
| **3 ACM CCS siblings marked Close** | Accepted. *Distributed computing methodologies* → row 16; *Modeling and simulation* names world models, which has **no home** — flagged below; *Symbolic and algebraic manipulation* → row 4 |
| **5 merges made on thin evidence** | **All five left as the consolidation made them**, and all five named here so the owner can split any: Infrastructure ← Machine Learning Systems · Theory ← Theory of Machine Learning · NLP ← cs.CL · Multiagent Systems ← Distributed artificial intelligence · Machine Learning ← the CCS "Machine learning" node |
| **The declined merge: MLPerf Endpoints / MLPerf Inference: Datacenter** | **Left declined.** Two separately published suites carrying one copy-pasted sentence is a page defect, not identity |
| **The container node above the level** | **Folded** — see Folds |

## Arithmetic

**Closing over the consolidation's own total of 307 records, not over its area list.**

| | Count |
|---|---|
| Records in run `h` | 172 |
| Records in run `i` | 135 |
| **Union** | **307** |
| Names merged into another unit by the consolidation | 84 |
| **Distinct categories the consolidation issued a verdict on** | **223** |

And every one of those 223 is accounted for here:

| Consolidation verdict | Count | This stage |
|---|---|---|
| `AREA` | 47 | **41 KEEP + 3 FOLD** = 44 rows, **plus the 12 measurement suites counted as 12** → 41 keeps includes them; the three folds are the remainder. 44 + 3 = 47 ✓ |
| `DOMAIN` | 51 | Accepted as rejected. 13 arXiv + 3 CCS marked Close are examined above |
| `RECORD` | 9 | Accepted as rejected |
| `FORMAT` | 17 | Accepted as rejected |
| `PRODUCT` | 0 | — |
| `UNCLEAR` | 99 | **All 99 held, none cut.** Disposed of in five blocks above |
| **Total** | **223** | 44 + 3 + 51 + 9 + 17 + 0 + 99 = **223** ✓ |

**Plus the 84 merged names**, which the consolidation folded and this stage did not disturb:
223 + 84 = **307** ✓ — the union total.

**The `BELOW` children are not in the 307.** They are sub-level items inside the runs' own records
— the 31 ARR tracks, AAAI's 296 keywords, the CCS's level-4 nodes — and the consolidation carries
them in `BELOW` fields rather than as units. **Nothing in a `BELOW` field is cut by this proposal**,
because nothing is cut.

## What this stage could not settle

- **Two subjects lose their only home to a fold**, both named rather than dropped: **`Creative AI`**
  (from `Applications`) and **`expert systems`** (from `cs.AI`). What would settle them: whether
  either deserves an area, which needs the owner.
- **`world models` has no home in the kept list.** The consolidation's only route to it is the CCS
  node *Modeling and simulation*, rejected as not-AI but marked Close with the single word "world
  models", and the programme track *Robotics & World Models*, which is `UNCLEAR`. **This is the
  subject the first run of this stage lost**, and it is still not safe.
- **`cs.AR` (hardware) and `cs.DC` (distributed computing)** are rejected, and their AI-specific
  ground is carried only by row 16, Infrastructure, whose own scope statement names hardware once.
  **If the book wants hardware as a subject, Infrastructure is the only thread holding it.**
- **An assumption I am making, named as one:** that the owner's §1.1 roles need the engineering
  vocabulary now in the `UNCLEAR` pile. It is why I recommend fetching the 62 scope statements
  rather than cutting. **If he does not want that vocabulary, the recommendation changes and the
  academic 47 are a complete list.**
- **Six pairs the previous stage declined to merge, and I did not decide**, because the evidence
  bar for a fold is not met and the judgement is his: Robotics / Intelligent Robots · Planning and
  scheduling / Planning, Routing, and Scheduling · Search and Optimization / Search methodologies ·
  Probabilistic Methods / Reasoning under Uncertainty · Trustworthy ML / Social and economic
  aspects of ML · Philosophy and Ethics of AI / Philosophical foundations.
- **Whether the twelve measurement suites are one area or twelve**, which changes the list's shape
  more than any other single question.
- **What I did not read**: seven of the twelve MLPerf unit records in full. They are one source, one
  shape and one sentence apart from each other; I read five and the consolidation's summary of all
  twelve. **Every other one of the 47 records was read in full.**
