<div align="justify">

# Release and Rollback: Four Decisions Under Imperfect Evidence

| | |
| --- | --- |
| **Type** | Case set — decisions to make and defend, not exercises with answers |
| **For** | [6. Evaluation and Testing](../LEARNING-GUIDE.md#6-evaluation-and-testing) (cases 1 and 2, after you have written a success specification) and [16. Operating AI Systems in Production](../LEARNING-GUIDE.md#16-operating-ai-systems-in-production) (all four) |
| **You should already have** | Success specification with costed errors (step 6), paired comparison and intervals (step 4), evaluation validity (step 12, for cases 3 and 4), monitoring and rollback mechanics (*Designing Machine Learning Systems* chs 7–9) |
| **How to use it** | For each case, decide **ship · hold · roll back · gather more evidence**, and write the justification before reading the discussion. The discussion does not contain the answer; it contains what experienced engineers would argue about |
| **Sources** | *Designing Machine Learning Systems* chs 6–9 · Miller, "Adding Error Bars to Evals" · your own step 6 specification |

Deployment mechanics are taught well by the assigned reading: shadow deployment, canaries, staged rollout, rollback triggers. What no resource supplies is practice at the decision those mechanics exist to serve — made with evidence that is always partial, under time pressure, with a cost on every option including waiting. That is a judgment, and judgment is built on cases.

**Rules of engagement.** Every case is decidable: you have enough to defend a position. None has a single right answer; two competent engineers can disagree and both be defensible. What is not defensible is a decision that ignores the specification, treats absence of evidence as evidence of absence, or forgets that *not shipping* is also a decision with costs.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Case 1 — The Improvement That Might Not Be One](#1-case-1--the-improvement-that-might-not-be-one)
2. [Case 2 — The Slice That Got Worse](#2-case-2--the-slice-that-got-worse)
3. [Case 3 — The Provider Changed the Model](#3-case-3--the-provider-changed-the-model)
4. [Case 4 — The Quiet Decline](#4-case-4--the-quiet-decline)
5. [Writing Your Own Rollback Triggers](#5-writing-your-own-rollback-triggers)

</details>

---

## 1. Case 1 — The Improvement That Might Not Be One

**The situation.** Your support-triage classifier routes incoming tickets. The current model is in production and meets the specification: at most 8% of urgent tickets misrouted, measured on a fixed evaluation set of 600 tickets. A colleague has trained a replacement. On the same 600 tickets it misroutes 6.5% of urgent tickets. They would like to ship it today, ahead of a busy week.

**What you also know.** The evaluation set was assembled eight months ago. The two models were compared on it once. The new model is four times more expensive to run and was trained on data that includes the last two months, which the old model never saw. Nobody has computed an interval on the difference.

**Your decision:** ship · hold · roll back · gather more evidence. Write it down with the reason, then continue.

**What is worth arguing about.** A 1.5-point difference on 600 items, of which perhaps 150 are urgent, is a handful of tickets; step 4 tells you how to put an interval on that, and the paired form of the comparison is available for free because both models scored the same items. The cost increase is not a detail — the specification named error costs, and it did not name a budget, which is a gap in the specification rather than a licence to ignore cost. And the training window makes the comparison suspect in a way the interval cannot capture: the newer model saw the recent past, and the evaluation set is from the older past, so a fair comparison needs data neither model has seen. The busy week cuts both ways: it raises the cost of a bad deployment and the cost of a delayed improvement.

[⬆ Back to Contents](#contents)

---

## 2. Case 2 — The Slice That Got Worse

**The situation.** A retrieval-augmented assistant answers policy questions for employees. Your new version improves overall answer accuracy from 71% to 78% on a 400-question evaluation. On the 40 questions that concern parental leave, accuracy falls from 85% to 62%.

**What you also know.** Parental-leave questions are 4% of the evaluation set and, by the traffic logs, about 3% of real questions. Their answers are the ones most often escalated to a human, and the policy behind them changed six weeks ago. The improvement elsewhere is broad, not concentrated in one topic.

**Your decision, with a justification, before reading on.**

**What is worth arguing about.** The aggregate number and the slice number are both real; the specification you wrote in step 6 is what decides which one governs, and if it is silent on slices then this case has just shown you a defect in it. Forty questions is a small denominator — the fall could be a dozen items — so an interval matters here as much as in case 1. The policy change six weeks ago raises a different possibility: that the new version is right and the *evaluation labels* are stale, which would reverse the sign of the finding. Note what that means practically: the cheapest next step may be to re-label 40 questions rather than to retrain anything.

[⬆ Back to Contents](#contents)

---

## 3. Case 3 — The Provider Changed the Model

**The situation.** Your production system calls a hosted model behind a version alias. This morning the provider moved that alias to a new version. Your regression suite — 120 cases with automated checks — passes at 116/120, against 119/120 yesterday. Latency is down 20%. Cost per request is down 30%. Two of the four new failures are in cases about numeric limits; the others look like formatting.

**What you also know.** You did not choose this change and cannot postpone it, though you can pin the previous version for a period. The system is used by about 300 people internally. Nobody has complained yet — it is 09:40.

**Your decision, and when you would revisit it.**

**What is worth arguing about.** Pinning buys time at a price (you will have to move eventually, and pinned versions are retired). Three failures out of 120 may be noise if any of your checks are stochastic — do you know which are? The numeric-limit failures deserve separate treatment from the formatting ones: one class is a correctness change, the other may be a contract your parser can absorb. The absence of complaints at 09:40 is not evidence of quality, which is exactly the trap step 6 warned about; the question is which monitoring signal would show this as harm, and how long it takes to move.

[⬆ Back to Contents](#contents)

---

## 4. Case 4 — The Quiet Decline

**The situation.** Nothing has been deployed for five weeks. Your weekly quality measurement — a model-based judge validated against human labels — reads 0.82, 0.81, 0.83, 0.79, 0.77. The specification's floor is 0.75. Support escalations are up slightly; the sample is small.

**What you also know.** The judge prompt was updated four weeks ago to handle a new answer format. Traffic mix has shifted towards a new customer segment. The human-label validation of the judge was done five weeks ago and has not been repeated.

**Your decision: roll back to what? And if not, what do you do instead?**

**What is worth arguing about.** This case has no deployment to roll back, which is the point: a decline can come from the world rather than from a change you made. Three explanations fit the numbers — the system is worse, the *measurement* is worse (the judge changed), or the *input* is different (the traffic did) — and they demand different responses. Step 12's methods separate them, and the order you test them in is a cost decision: re-validating the judge on 50 human labels is cheap; re-segmenting the metric by customer type is cheaper still and may resolve it in an hour.

[⬆ Back to Contents](#contents)

---

## 5. Writing Your Own Rollback Triggers

Now apply all four cases to your evolving system. Write a short release note containing, in this order:

1. **What would make you ship.** The measurement, the threshold, the slice conditions, and the interval you require.
2. **What would make you roll back**, stated so that it can be checked without you: a named metric, a threshold, a window and a person who acts.
3. **What you will not know at decision time**, listed honestly. This is the part most teams skip and every one of these cases turned on.
4. **How you would explain the decision to someone who does not work in AI** — in four sentences, no metric names.

Completion criterion: you can hand that note to a colleague and they can execute the rollback decision without asking you what you meant. Step 16 asks you to carry out one rollback against this note; the note is what makes that exercise a test of your judgment rather than of your reflexes.

[⬆ Back to Contents](#contents)

</div>
