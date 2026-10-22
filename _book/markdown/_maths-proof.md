# Maths Proof Page

A page to prove that notation typesets, that prices stay text, and that the pre-part opener works.

*The problem.* I need to know the equations render before planning a book around them.

*The question.* Does the pipeline carry real notation from Markdown to PDF?

## Inline and display

Attention compares every pair of positions, so the cost grows as `\(O(n^2 d)\)`{=latex} in the
sequence length `\(n\)`{=latex} and the model width `\(d\)`{=latex}. A model at $3 per million
input tokens and $15 per million output tokens is text, not maths, and so is $5.

```{=latex}
\[ \mathrm{Attention}(Q, K, V) = \mathrm{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right) V \]
```

Softmax turns scores into a distribution, with temperature `\(T\)`{=latex} dividing the logits:

```{=latex}
\[ p_i = \frac{\exp(z_i / T)}{\sum_{j=1}^{V} \exp(z_j / T)} \]
```

A low-rank update adds a thin correction to a weight matrix, where
`\(B \in \mathbb{R}^{d \times r}\)`{=latex} and `\(A \in \mathbb{R}^{r \times k}\)`{=latex}:

```{=latex}
\[ W' = W + BA, \qquad r \ll \min(d, k) \]
```

With `\(d = k = 4096\)`{=latex} and `\(r = 16\)`{=latex}, that is
`\(2 \times 4096 \times 16 = 131{,}072\)`{=latex} trainable numbers against
`\(4096^2 = 16{,}777{,}216\)`{=latex} — about 0.8 per cent.

> **Note:** Prices and model names date quickly. The arithmetic does not.

## Summary, Key Terms, and Review Questions

### Summary

The build carries inline and display mathematics, keeps dollar amounts as text, and sets
equations in Garamond-Math.

### Key Terms

| Term | Meaning |
|---|---|
| **Softmax** | Turns a vector of scores into a probability distribution that sums to one |

### Review Questions

1. Why does attention cost grow quadratically in the sequence length?
2. What does temperature do to the logits before softmax?

> **You understand this when** you can say why a rank-16 update to a 4096 × 4096 matrix trains
> under one per cent of its numbers.
