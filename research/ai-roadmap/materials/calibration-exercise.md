<div align="justify">

# Calibration: Does "70% Confident" Mean Anything?

| | |
| --- | --- |
| **Type** | Exercise — build the diagnostic, then break it |
| **For** | [4. Statistics: Is the Difference Real?](../LEARNING-GUIDE.md#4-statistics-is-the-difference-real) |
| **You should already have** | Metrics and threshold curves (*Hands-On ML* ch 3), sampling variability (*Computational and Inferential Thinking* chs 10–13), and the scikit-learn User Guide section on probability calibration |
| **Needs** | Python, standard library only |
| **Sources** | scikit-learn User Guide §1.16 · *Hands-On ML* ch 3 |

The scikit-learn guide explains what calibration is and how to fix it. What it does not do is put you in the position of an engineer who has two models, both of which report probabilities, and has to work out which reported number can be believed — and then discover that the measurement of calibration is itself a choice with consequences. That is this exercise.

## Contents

<details open>
<summary><b>Click to expand / collapse</b></summary>

1. [Two Different Questions](#1-two-different-questions)
2. [Predict First](#2-predict-first)
3. [The Exercise](#3-the-exercise)
4. [The Part Everyone Gets Wrong](#4-the-part-everyone-gets-wrong)
5. [Carry It Into Your Own System](#5-carry-it-into-your-own-system)

</details>

---

## 1. Two Different Questions

A model that outputs probabilities is answering two questions at once, and they can be answered with very different quality.

- **Discrimination.** Does the model rank positives above negatives? This is what accuracy, ROC and precision–recall curves measure. A model can be perfect here while every probability it reports is wrong.
- **Calibration.** Among the cases where the model says 0.7, do about 70% turn out positive? This is what a reliability diagram measures. A model can be perfectly calibrated while ranking no better than a coin toss.

You need the first when you are choosing what to act on, and the second whenever the number itself enters a decision: routing anything below a confidence threshold to a human, combining a model's probability with a cost, or deferring when uncertain — which is where step 6's costed errors will send you.

[⬆ Back to Contents](#contents)

---

## 2. Predict First

1. Model A ranks every positive above every negative, but reports probabilities squashed towards 0.5. Model B ranks less well but reports probabilities much closer to the observed frequencies. Which has the better AUC? Which has the better calibration error? Which would you rather deploy, and for what decision?
2. You measure calibration error by binning predictions into 10 equal-width bins. What happens to that number if you use 5 bins instead? If you use 50?
3. You have 200 labelled examples. How much of the calibration error you measure do you expect to be real, and how much an artefact of having 200 examples?

[⬆ Back to Contents](#contents)

---

## 3. The Exercise

```python
"""Calibration: ranking quality and probability honesty are different things."""
import random

random.seed(4)

def sample(n: int = 4000) -> list[tuple[float, int]]:
    """Ground truth: each case has a true probability; the label is drawn from it."""
    cases = []
    for _ in range(n):
        true_p = random.random()
        cases.append((true_p, 1 if random.random() < true_p else 0))
    return cases

cases = sample()

# Model A: perfect ranking, squashed probabilities (never confident).
model_a = [(0.5 + (p - 0.5) * 0.4, y) for p, y in cases]
# Model B: honest probabilities, but noisy ranking.
model_b = [(min(1.0, max(0.0, p + random.gauss(0, 0.25))), y) for p, y in cases]

def auc(pred: list[tuple[float, int]], pairs: int = 20000) -> float:
    """Probability that a random positive outranks a random negative."""
    pos = [p for p, y in pred if y == 1]
    neg = [p for p, y in pred if y == 0]
    wins = sum((random.choice(pos) > random.choice(neg)) for _ in range(pairs))
    return wins / pairs

def reliability(pred: list[tuple[float, int]],
                bins: int = 10) -> list[tuple[str, int, float, float]]:
    """Predicted probability against observed frequency, bin by bin."""
    rows = []
    for b in range(bins):
        lo, hi = b / bins, (b + 1) / bins
        chunk = [(p, y) for p, y in pred if lo <= p < hi or (b == bins - 1 and p == 1.0)]
        if not chunk:
            continue
        said = sum(p for p, _ in chunk) / len(chunk)
        happened = sum(y for _, y in chunk) / len(chunk)
        rows.append((f"{lo:.1f}-{hi:.1f}", len(chunk), said, happened))
    return rows

def ece(pred: list[tuple[float, int]], bins: int = 10) -> float:
    """Average gap between claim and reality, weighted by how many cases each bin holds."""
    rows = reliability(pred, bins)
    n = sum(count for _, count, _, _ in rows)
    return sum(count * abs(said - happened) for _, count, said, happened in rows) / n

for name, pred in (("A (perfect ranking, squashed)", model_a),
                   ("B (closer probabilities, noisy ranking)", model_b)):
    print()
    print(f"{name}:  AUC {auc(pred):.3f}   ECE {ece(pred):.3f}")
    print(f"  {'bin':>9} {'n':>5} {'says':>7} {'happens':>9}")
    for label, count, said, happened in reliability(pred):
        print(f"  {label:>9} {count:5d} {said:7.2f} {happened:9.2f}")

# The measurement is a choice: the same model, measured three ways.
print()
print("same models, different bin counts")
for bins in (5, 10, 20, 50):
    print(f"  bins={bins:3d}   A: {ece(model_a, bins):.3f}   B: {ece(model_b, bins):.3f}")

# And with less data.
small = cases[:200]
model_a_small = [(0.5 + (p - 0.5) * 0.4, y) for p, y in small]
print()
print("the same model A on 200 cases instead of 4000")
for bins in (5, 10, 20):
    print(f"  bins={bins:3d}   ECE {ece(model_a_small, bins):.3f}")
```

[⬆ Back to Contents](#contents)

---

## 4. The Part Everyone Gets Wrong

Read the reliability table for model A before reading on. The "says" column and the "happens" column diverge in a specific direction: in the low bins the model says more than happens, in the high bins it says less. That is what under-confidence looks like as a shape rather than as a number, and it is why the diagram is worth more than the single error figure.

Then look at what happened to the numbers when the bin count changed. **Expected calibration error is not a property of the model alone; it is a property of the model and your binning.** With few bins, real miscalibration hides inside wide bins. With many bins, each bin holds few cases and the noise in those small denominators inflates the error. On 200 cases the effect is severe enough that a model can look badly calibrated because you measured it that way.

So the answers to write down are:

1. Which model would you deploy for *ranking tickets by urgency*, and which for *deciding automatically when the model's confidence exceeds 0.9*? Justify each in one sentence.
2. Report model A's calibration error as you would to a colleague, in a way that cannot be misread. (Hint: one number is not enough.)
3. You are asked to compare two teams' calibration figures. What must you establish before the comparison means anything?
4. A colleague fixes calibration by post-processing the scores and reports that the model is now well calibrated on the same data used to fit the correction. What have they actually shown?

[⬆ Back to Contents](#contents)

---

## 5. Carry It Into Your Own System

Take any component of your evolving system that reports a confidence — a classifier from step 3, a retrieval score you have turned into a probability, or a model-based judge later on — and build its reliability table on held-out data. Then decide, explicitly, whether that number is allowed into a decision or is only allowed to rank.

**Completion criterion.** You can look at a reliability table and say what it implies for a threshold you were about to set, and you can defend your choice of bins to someone who chose differently.

[⬆ Back to Contents](#contents)

</div>
