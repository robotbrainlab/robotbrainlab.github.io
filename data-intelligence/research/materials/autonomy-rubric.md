<div align="justify">

# How Much Freedom Does This Task Need?

| | |
| --- | --- |
| **Type** | Rubric — a decision procedure you apply and defend, not a scoring gadget |
| **For** | [11. Compound AI Systems: Tools, Retrieval and Verification](../LEARNING-GUIDE.md#11-compound-ai-systems-tools-retrieval-and-verification), and again at [15. Trustworthy AI and Security](../LEARNING-GUIDE.md#15-trustworthy-ai-and-security) when the same decision becomes a containment decision |
| **You should already have** | Kapoor et al. on agents and cost-controlled evaluation, the compound-system design of *AI Engineering* chapter 6, and [your own agent loop](agent-loop-exercise.md) |
| **Sources** | Kapoor et al., "AI Agents That Matter" · Kambhampati et al., LLM-Modulo · *AI Engineering* ch 6 |

The reading establishes that autonomy is a cost rather than an achievement, and that the interesting comparison is not "agent versus no agent" but "how much decision freedom does this particular task warrant, at what measured benefit". What it does not give you is a procedure for answering that in a design review. This rubric is that procedure: five questions, four levels, and a rule that stops the answer from being *more*.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Levels](#1-the-levels)
2. [The Five Questions](#2-the-five-questions)
3. [The Rule](#3-the-rule)
4. [A Worked Example](#4-a-worked-example)
5. [Apply It, and Argue With It](#5-apply-it-and-argue-with-it)

</details>

---

## 1. The Levels

Autonomy is not a dial from 0 to 100; it is a small number of distinguishable arrangements.

| Level | What the system does | What a person does | Typical failure |
| --- | --- | --- | --- |
| **L0 — Suggest** | Produces a draft or recommendation | Reviews and acts | Slows the person down if the suggestion is usually wrong |
| **L1 — Act with approval** | Prepares the action, shows exactly what it will do | Approves each action | Approval becomes a rubber stamp under volume |
| **L2 — Act and report** | Takes the action, records what it did | Reviews afterwards, can undo | Damage happens before review; undo may not exist |
| **L3 — Act silently** | Takes the action within limits | Sees aggregates only | Failures are discovered by users, not by you |

Two properties matter more than the labels. **Review that nobody has time for is not review** — L1 with 400 approvals a day is L2 wearing a costume. And **L2 is only meaningful if the action is reversible**; if it is not, L2 is L3.

[⬆ Back to Contents](#contents)

---

## 2. The Five Questions

Answer for a *single task*, not for "the system". A system usually needs different levels for different tasks, and treating it as one decision is the most common mistake this rubric prevents.

1. **Reversibility.** If the action is wrong, can it be undone, and by whom, and in how long? *Unreversible actions cap the level at L1 regardless of every other answer.*
2. **Blast radius.** How many people or records does one wrong action touch? One customer, one team, everyone?
3. **Verifiability.** Can you check the action was right **before** it is taken, automatically? A schema, a policy check, a test, a second model that disagrees usefully? The strength of your verifier is what buys autonomy; nothing else does.
4. **Error rate under repeated trials.** Not "does it work" — at what rate, over how many runs, measured how? Use [the repeated-trial reasoning](repeated-trial-simulation.md): a 95% per-step success rate across six steps completes fewer than three runs in four.
5. **Cost of the alternative.** What does human review cost at your real volume, in time and delay? If a person can review everything comfortably, autonomy is buying you little and costing you risk.

[⬆ Back to Contents](#contents)

---

## 3. The Rule

> Choose the **lowest** level at which the task is worth doing at all, and raise it only with a measurement that shows the higher level is both needed and safe.

In practice:

- Start at L0 or L1 and instrument it. The logs from that period are the evidence for any later increase.
- **Raise a level only with a verifier**, an error-rate measurement over repeated trials, and a rollback you have actually exercised (see [the release and rollback cases](release-and-rollback-cases.md)).
- Write down what would make you **lower** it again. A level with no reduction trigger is a level nobody will ever reduce.
- Record the decision where the system is maintained, not in a document nobody re-reads: one paragraph per task, with the date and the measurement it rested on.

[⬆ Back to Contents](#contents)

---

## 4. A Worked Example

*Task: an internal assistant that answers policy questions and, when asked, files a ticket to the benefits team.*

| Question | Answering | Filing a ticket |
| --- | --- | --- |
| Reversible? | Yes — the answer can be corrected | Partly: a ticket can be closed, but it has been seen |
| Blast radius | One employee | One employee plus a team's queue |
| Verifiable before acting? | Weakly — a grounding check that the answer cites a retrieved passage | Strongly — the ticket has a schema, a category and a required policy reference |
| Measured error rate | 8% ungrounded answers over 200 trials | 2% wrong category over 50 trials, small sample |
| Cost of review | Reviewing every answer defeats the purpose | 6 tickets a day; review is cheap |

**Decision.** Answering: **L2** — act and report, with the grounding check as a gate and a weekly sample reviewed by a person. Filing: **L1** — show the ticket, one click to send, because review is nearly free at this volume and the sample behind the 2% is too small to lean on. **Reduction trigger:** if ungrounded answers exceed 12% in a week, answering drops to L1 until the retrieval is fixed.

Notice that the *more* verifiable task got the *lower* level. That is not a contradiction: verifiability makes higher autonomy defensible, but cheap review makes it unnecessary. Autonomy is a cost you pay when review does not scale.

[⬆ Back to Contents](#contents)

---

## 5. Apply It, and Argue With It

For each distinct task in your own compound system, fill in the five questions, choose a level, and write the reduction trigger. Then do the part that makes it judgment rather than form-filling:

1. **Argue the opposite.** For one task, write the strongest case for the level above the one you chose. If you cannot, you did not understand the trade; if you find it convincing, you have learned something.
2. **Name the measurement you do not have.** Most tasks will have one of the five questions answered by a guess. Say which, and what it would take to replace the guess.
3. **Check the rubber stamp.** For every L1, compute the daily approval volume. Above what volume does your L1 become L2 in practice?

**Completion criterion.** You can defend a level for each task with a measurement, name what would make you lower it, and explain to a colleague who wants "a fully autonomous agent" exactly what evidence would justify one — and what it would cost to produce.

[⬆ Back to Contents](#contents)

</div>
