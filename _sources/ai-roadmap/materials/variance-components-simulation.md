<div align="justify">

# Where the Variance Comes From

| | |
| --- | --- |
| **Type** | Simulation — decompose a score, then decide where to spend |
| **For** | [12. Evaluation Science](../LEARNING-GUIDE.md#12-evaluation-science) |
| **You should already have** | Repeated trials ([the step 4 simulation](repeated-trial-simulation.md)), judge validation against human labels, and the reliability and measurement-theory material of *AI Measurement Science* |
| **Needs** | Python, standard library only |
| **Sources** | *AI Measurement Science* chs 5 and 13 · Miller, "Adding Error Bars to Evals" |

*AI Measurement Science* formalizes this as generalizability theory: a score varies across several **facets** at once, and reliability depends on which facet you intend to generalize over. The formalism is exact and hard to feel. This simulation makes it concrete by building a world where you know the truth, measuring it the way you would measure a real system, and then asking the question a budget forces on you: **more items, more repeats, or more judges?**

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [The Three Facets](#1-the-three-facets)
2. [Predict First](#2-predict-first)
3. [The Simulation](#3-the-simulation)
4. [Reading the Result](#4-reading-the-result)
5. [Designing Your Own Evaluation](#5-designing-your-own-evaluation)

</details>

---

## 1. The Three Facets

When you evaluate a generative system with a model-based judge, a score moves for at least three reasons that have nothing to do with the system being better or worse:

- **Items.** You sampled these questions, not others. Some are harder.
- **Generation.** The system answers differently each run, even on the same question.
- **Judging.** The judge scores the same answer differently across runs, prompts or versions — and may be systematically generous or harsh.

A single number hides all three. Worse, the usual instinct — *collect more data* — is only right for one of them at a time, and which one is an empirical question about your system, not a general truth.

[⬆ Back to Contents](#contents)

---

## 2. Predict First

Write these down before running the code.

1. Your evaluation uses 100 items, one generation each, one judge pass. You double the items. By roughly what factor does the run-to-run spread of the overall score shrink?
2. Instead you keep 100 items and generate three answers per item, averaging them. Which facet does that shrink, and what happens to the total spread?
3. The judge has a small systematic bias — it is 0.04 generous on every answer. How much does averaging over more items reduce that bias?

[⬆ Back to Contents](#contents)

---

## 3. The Simulation

```python
"""Which facet drives the variation in an evaluation score?"""
import random
import statistics

random.seed(1234)

N_ITEMS_POOL = 500
ITEM_DIFFICULTY = [random.gauss(0.70, 0.15) for _ in range(N_ITEMS_POOL)]   # true per item
GENERATION_SD = 0.12    # the system answers the same item differently each run
JUDGE_SD = 0.08         # the judge scores the same answer differently each pass
JUDGE_BIAS = 0.04       # and is systematically generous

def score_once(item: int, generations: int, judge_passes: int) -> float:
    """Evaluate one item: average over generations, each scored by judge passes."""
    per_generation = []
    for _ in range(generations):
        answer_quality = ITEM_DIFFICULTY[item] + random.gauss(0, GENERATION_SD)
        judged = [answer_quality + JUDGE_BIAS + random.gauss(0, JUDGE_SD)
                  for _ in range(judge_passes)]
        per_generation.append(statistics.mean(judged))
    return statistics.mean(per_generation)

def evaluation(n_items: int, generations: int = 1, judge_passes: int = 1) -> float:
    items = random.sample(range(N_ITEMS_POOL), n_items)
    return statistics.mean(score_once(i, generations, judge_passes) for i in items)

def spread(n_items: int, generations: int = 1, judge_passes: int = 1,
           repeats: int = 400) -> tuple[float, float]:
    runs = [evaluation(n_items, generations, judge_passes) for _ in range(repeats)]
    return statistics.mean(runs), statistics.stdev(runs)

print("what one evaluation reports, and how much it moves between runs")
designs = [
    ("100 items, 1 generation, 1 judge pass", 100, 1, 1),
    ("200 items, 1 generation, 1 judge pass", 200, 1, 1),
    ("400 items, 1 generation, 1 judge pass", 400, 1, 1),
    ("100 items, 3 generations, 1 judge pass", 100, 3, 1),
    ("100 items, 1 generation, 3 judge passes", 100, 1, 3),
    ("100 items, 3 generations, 3 judge passes", 100, 3, 3),
]
for label, n, g, j in designs:
    mean, sd = spread(n, g, j)
    print(f"  {label:42s} mean {mean:.3f}   run-to-run sd {sd:.4f}")

# Which facet contributes what, holding the others fixed.
def facet_variance() -> None:
    item = 0
    same_item_many_generations = [score_once(item, 1, 1) for _ in range(2000)]
    same_answer_many_judgings = [ITEM_DIFFICULTY[item] + JUDGE_BIAS + random.gauss(0, JUDGE_SD)
                                 for _ in range(2000)]
    print()
    print("variation from each facet, one item at a time")
    print(f"  across items (true difficulty): sd {statistics.stdev(ITEM_DIFFICULTY):.3f}")
    print(f"  one item, generation + judging: sd {statistics.stdev(same_item_many_generations):.3f}")
    print(f"  one answer, judging only:       sd {statistics.stdev(same_answer_many_judgings):.3f}")

facet_variance()

# The bias does not average away.
mean_100, _ = spread(100, 1, 1)
mean_400, _ = spread(400, 3, 3)
print()
print(f"true mean quality of the pool: {statistics.mean(ITEM_DIFFICULTY):.3f}")
print(f"  reported by a small design:  {mean_100:.3f}")
print(f"  reported by a large design:  {mean_400:.3f}")
```

[⬆ Back to Contents](#contents)

---

## 4. Reading the Result

Three lessons, in the order they usually bite.

**More items is not always the answer.** Compare the designs. Adding items shrinks the part of the spread that comes from *which questions you sampled*; repeating generations shrinks the part that comes from *the system's own randomness*; repeating judge passes shrinks the part that comes from *the judge's noise*. If the dominant facet is generation, doubling your evaluation set buys you less than re-running the same set twice — and costs more.

**Bias is not variance.** Look at the last block. Every design reports a number above the pool's true mean, and the large design reports it just as confidently as the small one. Averaging fixes noise; it does nothing to a judge that is generous to everyone. That is why step 12 makes you validate a judge against human labels *before* using it, and why "we ran more items" is not an answer to "is your judge right".

**Now decide.** Suppose one item costs one model call to generate and one to judge, and your budget is 600 calls. Using the numbers above, which design gives the tightest estimate? Write the design and the reasoning; then change `GENERATION_SD` and `JUDGE_SD` to values that fit a system you have actually measured and see whether your answer changes. The point is not the answer — it is that the answer depends on facts about your system that you can measure.

[⬆ Back to Contents](#contents)

---

## 5. Designing Your Own Evaluation

On your evolving system, estimate the three facets crudely but honestly:

1. **Items.** Score your evaluation set once. Take the spread across items.
2. **Generation.** Pick ten items. Generate three answers each. Take the spread within items.
3. **Judging.** Take ten fixed answers. Judge each three times. Take the spread within answers. Then compare the judge with your own labels on those ten to estimate bias, not just noise.

Write a short evaluation design that states how many items, how many generations and how many judge passes you will use, and *why*, given what you measured. Note what you are generalizing over — this system on this kind of question, judged this way — because that sentence is the real claim your score supports.

**Completion criterion.** You can say which facet dominates your system's evaluation, defend where the next hundred model calls should go, and explain why a tighter interval does not make a biased judge correct.

[⬆ Back to Contents](#contents)

</div>
