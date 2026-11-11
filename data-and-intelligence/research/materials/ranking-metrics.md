<div align="justify">

# Measuring an Ordered List

| | |
| --- | --- |
| **Type** | Conceptual note with a worked comparison — what ranking metrics reward, and why classification metrics do not apply |
| **For** | [9. Retrieval and Search](../LEARNING-GUIDE.md#9-retrieval-and-search), used again in [14. Advanced Retrieval and Ranking](../LEARNING-GUIDE.md#14-advanced-retrieval-and-ranking) |
| **You should already have** | Precision, recall and the metrics of *Hands-On ML* chapter 3, and retrieval evaluation as *Speech and Language Processing* chapter 11 presents it |
| **Needs** | Python, standard library only |
| **Sources** | *Speech and Language Processing* ch 11 · *Introduction to Information Retrieval* ch 8, for the definitions in full |

The textbook covers precision, recall and mean average precision for retrieval. Two metrics you will meet constantly — **MRR** and **nDCG** — it does not, and the reason they exist is more important than their formulas: a retriever's output is an *ordered list*, and a metric that ignores order cannot tell you whether the thing you need is at position 1 or position 40.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Why Classification Metrics Do Not Transfer](#1-why-classification-metrics-do-not-transfer)
2. [Three Metrics and What Each Rewards](#2-three-metrics-and-what-each-rewards)
3. [A Case Where They Disagree](#3-a-case-where-they-disagree)
4. [Choosing One, and Defending It](#4-choosing-one-and-defending-it)

</details>

---

## 1. Why Classification Metrics Do Not Transfer

In classification, an item is right or wrong and the cases are independent. In retrieval, three things change at once.

- **Position matters.** A relevant document at rank 1 and the same document at rank 20 are not the same result, because the next stage — a person reading, or a model whose context you are filling — sees only the top few.
- **The cutoff is yours.** You choose how many results to take, so every number is really "precision *at k*", and the k is part of the claim.
- **Relevance is not always binary.** Many collections have degrees: exactly what was asked, related, tangential.

So the question a retrieval metric answers is not "how many did it get right" but "how good is this ordering for the use it will be put to" — and different uses want different answers, which is why there is more than one metric.

[⬆ Back to Contents](#contents)

---

## 2. Three Metrics and What Each Rewards

| Metric | In one sentence | It rewards | Use it when |
| --- | --- | --- | --- |
| **Precision@k** | Of the top k results, what fraction are relevant | Filling a fixed window with relevant material, order within the window ignored | You will pass exactly k passages to a model and each costs context |
| **MRR** — mean reciprocal rank | Average of 1/(rank of the first relevant result) | Getting *one* right answer as high as possible; everything after the first relevant hit is ignored | There is a single correct answer and the user stops at it |
| **nDCG@k** — normalized discounted cumulative gain | Sum of the relevance grades in the top k, each discounted by how far down it sits, divided by the best possible such sum | Graded relevance *and* position; the best documents first, the mediocre ones tolerated below | Relevance has degrees, and the order within the window matters |

Two properties are worth holding onto. MRR is blind to everything after the first relevant result — a list with one perfect hit at rank 1 and rubbish below scores 1.0. And nDCG is normalized per query, so it can be averaged across queries of different difficulty without the easy ones dominating.

[⬆ Back to Contents](#contents)

---

## 3. A Case Where They Disagree

Two retrievers return five results for the same query. Relevance grades are 0 (irrelevant), 1 (related) and 2 (exactly what was asked).

```python
"""Three metrics, two rankings, one disagreement."""
import math

# Relevance grades in returned order.
ranking_a = [2, 0, 0, 1, 1]   # the perfect document first, then weak results
ranking_b = [0, 1, 2, 1, 1]   # a weak start, then solid, the perfect document third

def precision_at_k(grades: list[int], k: int) -> float:
    return sum(1 for g in grades[:k] if g > 0) / k

def reciprocal_rank(grades: list[int]) -> float:
    for i, g in enumerate(grades, start=1):
        if g > 0:
            return 1 / i
    return 0.0

def dcg(grades: list[int], k: int) -> float:
    return sum((2 ** g - 1) / math.log2(i + 1) for i, g in enumerate(grades[:k], start=1))

def ndcg_at_k(grades: list[int], k: int) -> float:
    ideal = dcg(sorted(grades, reverse=True), k)
    return dcg(grades, k) / ideal if ideal else 0.0

for name, grades in (("A", ranking_a), ("B", ranking_b)):
    print(f"{name}: P@3 {precision_at_k(grades, 3):.2f}   "
          f"RR {reciprocal_rank(grades):.2f}   nDCG@3 {ndcg_at_k(grades, 3):.2f}   "
          f"nDCG@5 {ndcg_at_k(grades, 5):.2f}")
```

Before running it, predict which ranking wins under each metric. Then run it and answer:

1. Which metric prefers A, which prefers B, and what does each one's preference say about the *use* it assumes?
2. If these five passages are going into a model's context and all five will be read, which metric describes what you care about?
3. If a person will read the first result and stop, which one does?
4. nDCG@3 and nDCG@5 disagree in magnitude for the same ranking. What does that tell you about quoting "nDCG" without a k?

[⬆ Back to Contents](#contents)

---

## 4. Choosing One, and Defending It

For your evolving system's retrieval, write three lines and keep them next to your evaluation code:

1. **The metric and its k**, with the sentence "this is the right metric because the results are used by …".
2. **The relevance scale** you are judging with, and who applies it — including whether "related" is a grade you can label consistently.
3. **The failure the metric cannot see.** Every choice above is blind to something: precision@k to order, MRR to everything after the first hit, nDCG to whether the top result was actually *the* answer. Name yours.

**Completion criterion.** You can measure your retriever with a metric whose choice you can defend, and you can explain to someone proposing a different metric exactly what changing it would reward. Step 14 leans on this: when several pipeline stages each move the number, knowing what the number rewards is how you tell an improvement from a reshuffle.

[⬆ Back to Contents](#contents)

</div>
