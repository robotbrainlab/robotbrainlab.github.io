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

## Part II · Use

| Item | Value or formula | Ch |
|---|---|---|
| The four parts | Instructions, examples, output format, supplied information | 18 |
| The order to put them in | Specification first, data last, so the unchanging part is at the front | 18 |
| Cost of a conversation | Every turn re-sends the whole list; the total over `\(n\)`{=latex} turns grows like `\(n^2\)`{=latex} | 18 |
| Worked: ten turns | 14,250 input tokens against 3,000 for ten separate questions | 18 |
| What never gets dropped | Your specification: the system message, and the example turns if that is where they live | 18 |
| What to change per experiment | One block | 18 |
| Backoff with jitter | `wait = random.uniform(0, min(cap, base * 2 ** attempt))` | 19 |
| Attempts and waits | *n* attempts make *n* − 1 waits. Five attempts at base 0.5 is 7.5 s at worst | 19 |
| How many at once | rate × duration — 120 a minute at 2 seconds each is 4. It bounds concurrency, not rate, so leave a margin | 19 |
| Timeouts | Three: connect, read between chunks, total. Derive the *total* from the token cap | 19 |
| Retryable | 429, 5xx, timeouts. *Not* a malformed request, a bad key, an over-length one, or a 429 from an exhausted quota | 19 |
| What to stream | To a person, yes. One answer you must validate whole, no. Independent units, yes | 19 |
| `asyncio.gather` | One failure loses every result unless you pass `return_exceptions=True` | 19 |
| The resume file | One flushed line per item, or per `(item, stage)` for a pipeline. Keyed by input, holding the result | 19 |
| Spread of a score | `\(\sqrt{n p (1-p)} / n\)`{=latex} — one standard deviation over *which cases you drew*. 40 cases at 0.70 is 0.072, so two of them is the ±0.14 that spans 95 per cent. Run-to-run spread is a different number and is smaller unless the model is uncertain on every case | 20 |
| The bootstrap | Resample your cases with replacement, score each, take the 2.5th and 97.5th percentiles | 20 |
| What to put an interval on | The *difference*, paired. Never two separate intervals and a look | 20 |
| Cost of resolution | Width shrinks as `\(1/\sqrt{n}\)`{=latex}, so halving it costs four times the cases | 20 |
| What carries the comparison | Only the cases where the two versions disagree. Count them and say them out loud | 20 |
| What pairing is worth | Here, 0.400 wide down to 0.250. It cancels the variation the two versions share, so the more they agree, the more it buys | 20 |
| Cases against trials | Cases for the range of inputs, trials for the model's variation. Neither fixes the other | 20 |
| How many trials | Averaging `\(k\)`{=latex} judgements divides a case's own variance by `\(k\)`{=latex}. Two or three, then stop | 20 |
| Typical interval vs detection | A table built from a fixed mix shows the usual interval. Whether a real draw clears zero is a separate number, and lower | 20 |
| Why not prose | No contract, so your code guesses. Right 95 times in 100 is a defect 5 times in 100 | 21 |
| The four layers | Parses · right shape · values possible · values true. Only the first three are free | 21 |
| Rule of three | 0 failures in `\(n\)`{=latex} → the rate may be `\(3/n\)`{=latex}. Exactly, `\(1 - 0.05^{1/n}\)`{=latex} | 21 |
| 0 in 40 | Consistent with a 7.5 per cent failure rate | 21 |
| The repair line | Repair the envelope, never the contents. Needing to know what the model meant makes it a retry | 21 |
| Failure options | Reject · retry · repair · record. Never a silent default | 21 |
| The mechanism | Score → `\(-\infty\)`{=latex} for forbidden tokens → softmax gives 0 → pick. One line, and only while one token survives | 22 |
| What a constraint costs | The mass it deletes, which costs you only when that was the answer rather than the envelope | 22 |
| Why engines differ | Schemas are over characters, generation is over tokens; the legal-token set is precomputed per state | 22 |
| Both wrong checks | First character only is too loose (admits `{}`); a short window is too strict (rejects `{"s`) | 22 |
| Why strict modes can hurt | No room for intermediate tokens, and the model's only scratchpad is its own output. Also: a schema too narrow to hold the right answer | 22 |
| The fix, and its order | A `reasoning` field *before* the answer field — and only if the engine fixes field order | 22 |
| What it never buys | Correctness, or the parts of your schema the engine did not compile | 22 |
| The five steps | You send · model proposes · **you validate and decide** · you run · you return | 23 |
| Who decides | The model decides what to *propose*. Your code decides what *runs* | 23 |
| Why not in the instructions | Nothing in the loop checks a proposal's *values* against them except your code. A strict mode holds a shape, and an enum; not a range, and never a fact about the world | 23 |
| What the model never sees | The function, and every constraint you kept on your side | 23 |
| Description cost | Input on every call. A real tool schema is around 200 characters, so 30 tools is of the order of 1,500 tokens | 23 |
| The refusal to send back | The specific reason, so the next proposal can be better | 23 |
| What you get back | One vector, fixed width, per text. A few hundred to a few thousand numbers | 24 |
| The comparison | Chapter 8's cosine. Scale-free: multiplying a vector by 10 does not move it | 24 |
| What a high cosine is | A fact about two vectors. **Not** evidence that two texts mean the same | 24 |
| Dense retrieval | Embed the documents once, embed the query per search with the same model, sort by cosine | 24 |
| What decides the model | Your language, your domain, your document length. Length first: it is the one that gets forgotten | 24 |
| The hard limit | Every embedding model has a maximum input length. Past it, text is cut off, usually with no error | 24 |
| A raw cosine | Has no meaning on its own. Not comparable across models, queries or corpora — rank, do not threshold | 24 |
| What a benchmark is | One study, somebody else's corpus. A shortlist of three, not a choice of one | 24 |
| The input only you have | The answer key: which document each query is about | 24 |
| Why identifiers fail | A sketch, not a calculation: the vector holds the whole text at a fixed width, so a string appearing once competes for that room with everything else | 25 |
| What kind of claim that is | An observation on Chapter 6's ladder. The mechanism gives a reason to expect it, not a derivation | 25 |
| The illustration | Two notes differing in one character, on stipulated vectors: 0.99983 apart, so a distance of 0.00017 | 25 |
| Similarity against relevance | `\(\cos(a,b) = \cos(b,a)\)`{=latex} always. Relevance depends on which is the question | 25 |
| The negation case | On stipulated vectors, a true answer and its negation sat closer to each other than either did to the query | 25 |
| What the negation case proves | Nothing about which one ranks first. It is a claim about the score: you get no handle on that ordering, so you cannot tune or threshold it | 25 |
| What inspection finds | A wrong result that is present. Not a right result that is missing from the list | 25 |
| What a five-query demo is | A demonstration on Chapter 6's ladder: it can work once | 25 |
