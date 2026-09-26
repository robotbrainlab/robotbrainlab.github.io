<div align="justify">

# Framing: Six Situations, One of Which Is Not a Machine-Learning Problem

| | |
| --- | --- |
| **Type** | Case set — decisions to make and defend before any model exists |
| **For** | [3. Machine Learning: Framing Problems and Building Models](../LEARNING-GUIDE.md#3-machine-learning-framing-problems-and-building-models) |
| **You should already have** | *Designing Machine Learning Systems* chapters 1–2, including when not to use machine learning, and *AI Engineering* chapter 1 on planning an application |
| **How to use it** | Work each case in writing before looking at the questions that follow it. Twenty minutes each is enough; the value is in committing to an answer |
| **Sources** | *Designing Machine Learning Systems* chs 1–2 · *AI Engineering* ch 1, pp. 28–35 |

The reading argues that framing decides everything downstream and that some problems should not be solved by learning at all. Arguing is not practising. These cases give you the argument's raw material: six situations described the way they actually arrive — as a request from someone who is not thinking in terms of prediction — and ask you to do the work of turning each into something that can be built, or into a reasoned refusal.

For each case, produce five things:

1. **The decision or action** the system exists to change.
2. **The unit of prediction**: what one example is, and what is predicted about it.
3. **The available inputs** at the moment the prediction must be made — not the moment the data was collected.
4. **A baseline that involves no learning**, specific enough to implement this week.
5. **The cost of each kind of error**, in the operation's own terms.

If a case does not survive those five, say so and say why.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Six Cases](#1-the-six-cases)
2. [The Questions That Separate Good Framings from Plausible Ones](#2-the-questions-that-separate-good-framings-from-plausible-ones)
3. [What to Notice Afterwards](#3-what-to-notice-afterwards)

</details>

---

## 1. The Six Cases

**Case A — "Predict which customers will churn."** A subscription business loses about 3% of customers a month. The head of retention wants a model that flags who will leave so the team can call them. The team can make about 50 calls a week; there are 40,000 customers.

**Case B — "Automate the refund decisions."** Support agents approve or decline refund requests using a five-page policy document. Approvals take about six minutes each; roughly 400 arrive a day. Agents disagree with each other on about one in eight cases when the same request is shown twice.

**Case C — "Tell us which marketing campaign caused the sales lift."** Two campaigns ran last quarter in overlapping regions. Sales rose 11%. Leadership wants a model that attributes the lift.

**Case D — "Find the documents that answer this question."** An internal team wastes hours searching a 90,000-document policy archive. They ask for "AI search".

**Case E — "Predict machine failure before it happens."** A factory has 60 machines with sensors sampled every minute for two years. There have been 11 failures in that period. A failure costs about eight hours of downtime; a precautionary stop costs about 40 minutes.

**Case F — "Score the sales calls for quality."** A sales manager wants every recorded call scored 1–5 for quality, to be used in quarterly reviews. There is no existing definition of quality; the manager says they "know it when they hear it".

[⬆ Back to Contents](#contents)

---

## 2. The Questions That Separate Good Framings from Plausible Ones

Work the five requirements for each case first. Then use these, which are the questions a reviewer would ask.

**Case A.** You can act on 50 customers a week out of 40,000. Does that change the prediction target, the metric, or both? What is the baseline — and is "the 50 highest-value customers" harder to beat than it looks? What is the cost of a false positive when the action is a phone call?

**Case B.** Agents disagree with themselves one time in eight. What does that imply about the best achievable accuracy, and about the labels you would train on? Is the target "what an agent decided" or "what the policy says"? What would change if the answer had to be explained to a customer?

**Case C.** Which of the five requirements can you not produce here, and why? This case is the one where the honest output is a refusal — but a refusal accompanied by what *could* be done instead. Name the design that would have answered the question, and what it would have cost to run it last quarter.

**Case D.** Is this a learning problem at all? What non-learned baseline exists, and how good is it likely to be? Under what measured condition would you add a learned component — and which step of this roadmap teaches you to measure that?

**Case E.** Eleven positive examples. What does that do to the unit of prediction — per machine, per hour, per window? Given the cost ratio, where would you put the threshold before you have any model? What would you do first if you had one week?

**Case F.** There is no definition of quality. Is your first deliverable a model, a rubric, or a measurement of agreement between two humans applying a draft rubric? What is the risk in shipping a model whose target is one manager's judgment, given that the score enters performance reviews?

[⬆ Back to Contents](#contents)

---

## 3. What to Notice Afterwards

Compare your six framings and look for these patterns, which recur for the rest of your career.

- **The request is rarely the problem.** In at least three cases the stated request ("predict churn", "attribute the lift", "score the calls") is not what the operation needs. Write down, for each, the sentence you would say back to the requester.
- **The action constrains the prediction.** Capacity, cost and who acts on the output decide the unit of prediction and the metric more often than the data does.
- **Labels are made, not found.** Two cases require defining the target before any modelling; one requires measuring whether humans can apply the definition at all.
- **Not every case is a machine-learning case.** One of the six cannot be answered by prediction from historical data. If you concluded that more than one qualifies, argue it — that is a defensible position, and defending it is the exercise.

**Completion criterion.** For each case you can state the decision, the unit of prediction, the inputs available at prediction time, a no-learning baseline and the error costs — or explain precisely which of those cannot be produced and what that implies. Your step 3 practice then applies the same five to your own evolving system, and step 6 turns the last of them into a written success specification.

[⬆ Back to Contents](#contents)

</div>
