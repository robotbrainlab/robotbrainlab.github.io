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
