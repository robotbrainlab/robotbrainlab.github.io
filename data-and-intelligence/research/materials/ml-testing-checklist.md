<div align="justify">

# Testing and Reproducibility for a Learned System

| | |
| --- | --- |
| **Type** | Checklist — work through it once against your own system, then keep it |
| **For** | [6. Evaluation and Testing](../LEARNING-GUIDE.md#6-evaluation-and-testing) |
| **You should already have** | Breck et al., "The ML Test Score"; leakage and splits (steps 3 and 5); modules, a test runner and isolated environments (*The Python Tutorial*, revisited in step 6) |
| **Scope** | The testing an AI system needs *because it learns*. General software testing practice, continuous integration and version control belong to the Computer Science & Engineering roadmap; what is here is what your own readiness criteria require |
| **Sources** | Breck et al., "The ML Test Score" · *Designing Machine Learning Systems* ch 6 |

Breck et al. give you the rubric: the categories of test a production ML system needs and a way to score how many you have. What it does not give you is the concrete first pass for a system of your own, in the order that makes each test possible. That is this checklist. Work through it once, on your evolving system, writing the tests as you go; afterwards it becomes the thing you re-read before a release.

Each item says what to do, what "done" looks like, and what usually goes wrong.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Before Any Test: Make the System Runnable](#1-before-any-test-make-the-system-runnable)
2. [Fixtures: The Data Your Tests Run On](#2-fixtures-the-data-your-tests-run-on)
3. [Data Validation](#3-data-validation)
4. [Leakage](#4-leakage)
5. [Behaviour and Regression](#5-behaviour-and-regression)
6. [Testing a System That Is Not Deterministic](#6-testing-a-system-that-is-not-deterministic)
7. [Reproducibility and Lineage](#7-reproducibility-and-lineage)
8. [Scoring Yourself](#8-scoring-yourself)

</details>

---

## 1. Before Any Test: Make the System Runnable

- [ ] **The code is importable.** The pipeline lives in modules with functions you can call, not in cells that must be run top to bottom. *Done when* a test file can `import` your training, data and evaluation entry points.
- [ ] **One command runs everything.** Training, evaluation and the test suite each start from a single command with no manual steps. *Done when* you can write that command down for someone else.
- [ ] **Configuration is data, not edits.** Paths, thresholds, seeds and model choices live in one config object or file. *Usually goes wrong* when a threshold is typed into three places and only two get changed.

[⬆ Back to Contents](#contents)

---

## 2. Fixtures: The Data Your Tests Run On

A test that reads live data is slow, and it changes meaning without you touching it. A fixture is a small, fixed sample kept with the tests.

- [ ] **A tiny sample of real-shaped data**, twenty to fifty rows, committed with the tests. *Done when* the suite runs offline in seconds.
- [ ] **The awkward cases are in it.** Every bug you have already been bitten by leaves a row behind: the empty field, the duplicate, the out-of-range value, the unicode name, the row from the old schema.
- [ ] **No personal or confidential data.** Synthesize, subset or redact — and record which you did.
- [ ] **The fixture is documented in one line per oddity**, so a later reader knows which rows are deliberate.

[⬆ Back to Contents](#contents)

---

## 3. Data Validation

- [ ] **Schema.** Columns, types and required fields are asserted at the boundary where data enters. *Done when* a renamed upstream column fails a test instead of training a worse model.
- [ ] **Ranges and categories.** Numeric bounds and allowed values are checked; violations are counted, not silently dropped.
- [ ] **Volume and freshness.** The pipeline notices when a batch is a third of its usual size or a week old.
- [ ] **Missingness.** The rate of missing values per field is asserted against an expected range, because *more* missing data and *no* missing data are both signals.

[⬆ Back to Contents](#contents)

---

## 4. Leakage

Leakage is the failure that produces excellent numbers and a useless system, so it gets explicit tests rather than care.

- [ ] **No target-derived feature.** A test asserts that features computed from the label — or from anything unavailable at prediction time — are absent.
- [ ] **The split is honest.** Grouped or time-ordered data is split by group or by time, and a test asserts that no entity appears in both sides.
- [ ] **Preprocessing is fitted on training data only.** Scalers, encoders and vocabularies are fitted inside the training fold. *Usually goes wrong* when a normalization is applied to the whole dataset before splitting.
- [ ] **A leak canary.** Deliberately add a leaking feature in a test and assert that your evaluation improves implausibly — proving the test would notice.

[⬆ Back to Contents](#contents)

---

## 5. Behaviour and Regression

- [ ] **Invariance.** Changes that should not matter do not: an irrelevant field, a different capitalization, a reordering of independent inputs.
- [ ] **Directional expectation.** Changes that should matter do, in the right direction: more of the thing the model is meant to detect should not lower its score.
- [ ] **Slices.** The evaluation reports the groups that matter separately, and the test asserts a floor on each — not just the average.
- [ ] **A regression set that only grows.** Every bug you fix becomes a case in it, with a comment saying what it once did.

[⬆ Back to Contents](#contents)

---

## 6. Testing a System That Is Not Deterministic

Any component that calls a model, samples, or shuffles cannot be tested with equality.

- [ ] **Seeds where seeds work.** Sampling, shuffling and initialization take a seed from the config, and a test asserts that two runs with the same seed agree.
- [ ] **Tolerances where they do not.** Assertions are on ranges — "accuracy at least 0.78", "cost per request under 4 cents" — not on exact values.
- [ ] **Repeated trials for stochastic behaviour.** Where a single run could pass by luck, the test runs k times and asserts on the rate, using the reasoning of [the repeated-trial simulation](repeated-trial-simulation.md). *Usually goes wrong* when a flaky test is re-run until green instead of being made a rate test.
- [ ] **A failure you can read.** When the tolerance test fails, the message says what was measured, over how many runs, and against what threshold.

[⬆ Back to Contents](#contents)

---

## 7. Reproducibility and Lineage

- [ ] **The environment is recorded.** An isolated environment with pinned versions, and a command that recreates it.
- [ ] **The result records what produced it.** Every saved metric carries the data version, code revision, config and seed that produced it. *Done when* you can answer "which data and which settings produced this number?" a month later without guessing.
- [ ] **Data has a version.** Even a dated directory and a hash is enough at this stage; the requirement is that "the training data" names something specific.
- [ ] **Models and prompts are versioned like data.** A prompt is configuration that changes behaviour; treat it as such.
- [ ] **One rerun proves it.** Rebuild the environment, rerun the pipeline from the recorded configuration, and compare against the recorded numbers — deterministic parts exactly, stochastic parts within tolerance.

[⬆ Back to Contents](#contents)

---

## 8. Scoring Yourself

Count the boxes you can tick honestly today, then answer three questions in writing:

1. **Which unticked box would cost you most if it failed silently for a month?** That is your next piece of work, regardless of how many boxes it ticks.
2. **Which test would have caught the last bug you found by accident?** If none would, add it now.
3. **Which of these tests is checking something about the world rather than about your code?** Those are the ones that will fail through no fault of yours — and the ones whose failure messages need to be clearest.

**Completion criterion.** Your evolving system has a suite that runs from one command, uses a committed fixture, fails on a reintroduced leak, tolerates stochastic variation without being flaky, and records what produced each result. Step 16 assumes all of this when it asks you to decide on a release.

[⬆ Back to Contents](#contents)

</div>
