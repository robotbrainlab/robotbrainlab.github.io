# Cheat Sheet

The numbers, defaults and formulas worth carrying in your head, in the order the book
introduces them. Every line came from the chapter that teaches it, so nothing here was
written from memory.

## Part I · Mental Model

| Item | Value or formula | Ch |
|---|---|---|
| What cost scales with | The amount of text moved, in and out. Not the difficulty of the question | 1 |
| The two rates are not equal | Text you get back costs several times text you send — about 4× in the book's worked shape | 1 |
| Cost of a feature, per call | (words in × rate in) + (words out × rate out), then × calls × days | 1 |
| Whole-run success over *n* steps | per-step reliability to the power *n* | 4 |
| Ten steps at nine-in-ten | 0.9^10 = 0.349 — about a third of runs finish | 4 |
| Ten steps at ninety-nine in a hundred | 0.99^10 = 0.904 — the same loop, now usable | 4 |
| What that means for a demonstration | A system succeeding a third of the time shows you a good run roughly every third try | 4 |

## Part I · Inside the Model

| Item | Value or formula | Ch |
|---|---|---|
| Dot product | `\(a \cdot b = \sum_i a_i b_i\)`{=latex} | 8 |
| Cosine similarity | `\(a \cdot b / (\lVert a \rVert \lVert b \rVert)\)`{=latex}, between −1 and 1 | 8 |
| Softmax | `\(p_i = \exp(z_i) / \sum_j \exp(z_j)\)`{=latex} | 8 |
| Matrix shape rule | (m × k) times (k × n) gives (m × n); the inner numbers must match | 8 |
| Logarithms turn products into sums | `\(\ln(xy) = \ln x + \ln y\)`{=latex} | 8 |
| `\(e\)`{=latex} | About 2.718. `\(e^x\)`{=latex} is positive for every `\(x\)`{=latex} | 8 |
| Quadratic growth | `\(O(n^2)\)`{=latex}: ten times the input, a hundred times the work | 8 |
| Embedding table size | vocabulary × width numbers. 128,000 × 4,096 = 524,288,000 | 9 |
| The output step | One score per vocabulary entry, so the final shape is (1 × `\(d\)`{=latex}) times (`\(d\)`{=latex} × vocabulary) | 9 |
| What one forward pass yields | Exactly one next-token distribution | 9 |
| Passes for a reply | One per token produced, each over an input one token longer | 9 |
| The three shape numbers | Vocabulary, width, depth | 9 |
| Rule of thumb, English prose | 1 token ≈ 4 characters ≈ ¾ of a word; 1,000 tokens ≈ 750 words | 10 |
| What a token really measures | Frequency in the corpus the vocabulary was built from, not meaning or length | 10 |
| The merge step | Merge the commonest adjacent pair; recount; repeat | 10 |
| Why a word is one token | It was common enough for a merge to be spent on it | 10 |
| Which half is dear | Output, at several times input, and one forward pass per token | 10 |
| What a token count is a fact about | One particular model. A different vocabulary gives a different count | 10 |
| The worst case | One token per byte — the most byte-pair encoding can ever charge you | 10 |
| The attention formula | `\(\mathrm{softmax}(QK^{\top}/\sqrt{d_k})\,V\)`{=latex} | 11 |
| What the three views are for | Query = what I want, key = what I offer, value = what I give | 11 |
| Why divide by `\(\sqrt{d_k}\)`{=latex} | A dot product grows with width; without it softmax saturates and attention stops blending. The *square root*, because the slot products partly cancel, so the sum grows like `\(\sqrt{d_k}\)`{=latex} | 11 |
| The score grid | `\(n \times n\)`{=latex}, one entry per pair of positions | 11 |
| Attention cost | `\(O(n^2 d)\)`{=latex} — double the tokens, four times the work | 11 |
| What a row of weights is | Positive, adds to exactly 1, one number per visible position | 11 |
| Why positional encoding exists | Attention's output is a sum, so it is blind to the order of its inputs | 11 |
| What a layer does | `\(x \leftarrow x + \mathrm{attention}(x)\)`{=latex}, then `\(x \leftarrow x + \mathrm{feedforward}(x)\)`{=latex} | 12 |
| Attention block parameters | `\(4d^2\)`{=latex} — four matrices of `\(d \times d\)`{=latex} | 12 |
| Feed-forward block parameters | `\(2 \times d \times d_{ff}\)`{=latex}, with the middle width `\(d_{ff}\)`{=latex} between about `\(2.5d\)`{=latex} and `\(4d\)`{=latex} | 12 |
| Which half is bigger | Feed-forward, at roughly 57 per cent of a layer | 12 |
| Where the parameters are | In the layers — about nine in ten, at a common shape | 12 |
| Matrices compose | `\(W_2(W_1 x) = (W_2 W_1)x\)`{=latex}, which is why a block without its activation is one matrix | 12 |
| Temperature | `\(p_i = \exp(z_i/T) / \sum_j \exp(z_j/T)\)`{=latex} | 13 |
| What temperature does | Below 1 sharpens, above 1 flattens, never reorders | 13 |
| Temperature and greedy | No effect whatsoever — greedy takes the largest logit either way | 13 |
| Top-p against top-k | Top-p keeps the smallest set reaching `\(p\)`{=latex}; top-k keeps a fixed count | 13 |
| The order of operations | Temperature, then the cut, then draw | 13 |
| Why `\(T=0\)`{=latex} is not a guarantee | Float order, batching, expert routing, provider change | 13 |
| The objective | `\(\mathcal{L} = -\frac{1}{N}\sum_i \log p(t_i \mid t_1 \ldots t_{i-1})\)`{=latex} | 14 |
| Perplexity | `\(\exp(\mathcal{L})\)`{=latex}; a uniform choice among `\(V\)`{=latex} options gives `\(V\)`{=latex} | 14 |
| The update rule | `\(\theta \leftarrow \theta - \eta \nabla_{\theta}\mathcal{L}\)`{=latex} — and that is the edge of this book | 14 |
| The three stages | Pretraining, supervised fine-tuning, preference optimisation | 14 |
| Where knowledge comes from | Pretraining, overwhelmingly | 14 |
| What the loss ignores | Everything except the probability of the token that actually came next | 14 |
| Key–value cache | `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} | 15 |
| At a common shape | 32 layers, `\(d\)`{=latex} 4,096, 2 bytes: 512 KiB per token | 15 |
| An 8,000-token conversation | 3.91 GiB of cache, on top of the weights | 15 |
| Weights at 7 billion parameters | 14 GB at 16 bits, 7 GB at 8, 3.5 GB at 4 | 15 |
| What limits each phase | Prefill: arithmetic. Decode: reading the parameters the pass uses | 15 |
| Why batching is nearly free | The parameters are read once and shared | 15 |
