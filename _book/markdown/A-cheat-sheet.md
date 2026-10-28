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
| The three top-level shape numbers | Vocabulary, width, depth. There are more inside a layer, which is Chapter 12's | 9 |
| Rule of thumb, English prose | 1 token ≈ 4 characters ≈ ¾ of a word; 1,000 tokens ≈ 750 words | 10 |
| What a token really measures | Frequency in the corpus the vocabulary was built from, not meaning or length | 10 |
| The merge step | Merge the commonest adjacent pair; recount; repeat | 10 |
| Why a word is one token | It was common enough for a merge to be spent on it | 10 |
| Which half is dear | Output, at several times input, and one forward pass per token | 10 |
| What a token count is a fact about | One particular model. A count does not carry across vocabularies | 10 |
| The worst case | One token per byte — the most byte-pair encoding can ever charge you | 10 |
| The attention formula | `\(\mathrm{softmax}(QK^{\top}/\sqrt{d_k})\,V\)`{=latex} | 11 |
| What the three views are for | Query = what I want, key = what I offer, value = what I give | 11 |
| Why divide by `\(\sqrt{d_k}\)`{=latex} | A dot product grows with width; without it softmax saturates and attention stops blending. The *square root*, because the slot products partly cancel, so the sum grows like `\(\sqrt{d_k}\)`{=latex} | 11 |
| The score grid | `\(n \times n\)`{=latex}, one entry per pair of positions | 11 |
| Attention cost | `\(O(n^2 d)\)`{=latex} — double the tokens, four times the work | 11 |
| What a row of weights is | Positive, adds to exactly 1, one number per visible position | 11 |
| Why positional encoding exists | The formula's output is a sum, so *the formula* is blind to the order of its inputs. Masked attention is not — the mask is positional | 11 |
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
| What batching shares, and what it does not | The parameters are read once and shared; each request's own cache is not. So the saving is large at short contexts and small at long ones — about 4x at 8,000 tokens each | 15 |

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
| BM25 | `\(\sum_{t \in q} \mathrm{IDF}(t) \cdot \dfrac{f_{t,d}(k_1+1)}{f_{t,d} + k_1(1 - b + b|d|/\mathrm{avgdl})}\)`{=latex} | 26 |
| Its two knobs | `\(k_1 \approx 1.5\)`{=latex} controls saturation, `\(b \approx 0.75\)`{=latex} controls length normalisation. Tuned constants, not derived | 26 |
| What `\(k_1 = 0\)`{=latex} does | Makes term frequency irrelevant: the factor is 1 whatever the count, so only presence matters | 26 |
| Term-frequency ceiling | A term's contribution approaches `\((k_1+1)\)`{=latex} IDF. At `\(k_1=1.5\)`{=latex}, 100 mentions reach 98.5% of 2.5 IDF | 26 |
| Inverse document frequency | `\(\ln\!\left(\dfrac{N - n_t + 0.5}{n_t + 0.5} + 1\right)\)`{=latex}. Without the `+1` it goes negative for a term in over half the collection | 26 |
| Reciprocal rank fusion | `\(\sum_{r} 1/(k + \mathrm{rank}_r(d))\)`{=latex}, conventionally `\(k = 60\)`{=latex}. Uses ranks only, so no score comparability is needed | 26 |
| DCG | `\(\sum_{i=1}^{k} g_i / \log_2(i+1)\)`{=latex} | 26 |
| nDCG | DCG divided by the DCG of the ideal ordering of the same documents | 26 |
| Change of base | `\(\log_c x = \ln x / \ln c\)`{=latex}, so a base-`\(c\)`{=latex} DCG is `\(\ln c\)`{=latex} times the natural-log one | 26 |
| The log base cancels | A derivation: changing base scales DCG and ideal DCG by the same `\(\ln c\)`{=latex}. Base 2, 10 and e all gave nDCG 0.621602 | 26 |
| The gain convention does not | Grade directly gave 0.6216; `\(2^{g}-1\)`{=latex} gave 0.5193 on the same ranking | 26 |
| Why a logarithm at all | Convention, not derivation. It must decrease with position; a log decays slowly, which roughly matches how lists are read | 26 |
| Recall@k against MRR | Recall ignores order, so it suits a first stage. MRR stops at the first non-zero grade, so it cannot see a better answer further down | 26 |
| The reranking ceiling | A derivation: reordering a set cannot add to it, so the candidate set bounds everything the second stage can achieve | 26 |
| Cross-encoder cost | One forward pass per document per query, so a million documents cost a million passes. Hence two stages | 26 |
| What forces symmetry | Putting both sides through the *same function*, as chapter 24's dense retrieval does. Shared weights alone do not: one model given a `query:` or `passage:` marker is not symmetric | 26 |
| What merely permits asymmetry | A two-tower bi-encoder and a cross-encoder are *free* to be asymmetric, not guaranteed to be | 26 |
| Why parsing is the bottleneck | A derivation: every later stage reads the parser's output and none reconsults the file, so no later stage can restore information that output does not contain. Removing text that is there stays available | 27 |
| What a page actually holds | Strings and positions. No sentence, no column, no reading order — those are reconstructed | 27 |
| The three readings | Stream order is a bet on how the file was generated; sorting by position reads across columns; grouping by column needs a threshold fitted to the page | 27 |
| What a chunk boundary decides | What shares one vector, what can be returned together, and which questions are answerable at all | 27 |
| When overlap cannot help | When the chunk is smaller than the answer. 60-character chunks never held a 65-character answer at any overlap | 27 |
| When overlap is the fix | When the chunk is big enough and the cut falls inside the answer | 27 |
| The retrieval ceiling | A derivation: retrieval returns rows, so if no row holds a whole answer, no method, model or reranker can return a single passage that answers it | 27 |
| What that ceiling does *not* say | Where the cuts tile the document, the information is still there across two rows, and the reassembly moves downstream to Chapter 28 rather than becoming impossible. A chunker that discards text is another matter | 27 |
| The ten-minute check | Write five real questions, find the shortest passage answering each, make the chunk bigger than the longest | 27 |
| The first diagnostic | Print the extracted text and read it against the page. Before anything downstream exists | 27 |
| The budget arithmetic | Instruction + question are a fixed cost; each passage costs its length plus its label; the rest is the window, which Chapter 16 owns | 28 |
| Why a greedy fill is a trap | It keeps whatever fits, so the context becomes the highest-ranked *short* passages rather than the top of the ranking — undoing a reranker's ordering, for free, with nothing announcing it | 28 |
| What to do with too small a budget | Raise, do not truncate. A context without its instruction is a different request and still returns a plausible answer | 28 |
| Why neighbour expansion needs a locator | A derivation: adjacency is a property of the document and an index sorted by score has no notion of it. An offset, or an ordinal in the id — but something, recorded at index time | 28 |
| What an expansion costs | Each neighbour halves how many separate hits the budget can hold | 28 |
| The three mechanical citation checks | Does the document exist; is the quote in it; is it at the offset claimed | 28 |
| What a citation must support | That the quote *entails* the statement. The three checks are necessary and not sufficient | 28 |
| What still gets past all three | A real quote attached to the wrong claim; a statement with no citation at all, which the checks never look at; and a quote undone by the document's next sentence | 28 |
| Why a corpus outgrows a window | 100 documents × 2,000 tokens = 200,000, about 1.6× a 128,000-token window | 28 |
| What filling a window costs | Chapter 15's cache is 512 KiB per token, so 128,000 tokens is 62.5 GiB, against 13 GiB of weights. Multiply the per-token figure, not its rounded total — and divide by the head-sharing ratio before quoting any multiple | 28 |
| Long context against retrieval | Different questions: which text is relevant, and how much you can afford to show. Neither replaces the other | 28 |
| Why exhaustive search runs out | Its cost is linear in the collection. Not an inefficiency — it follows from comparing against everything | 29 |
| What an ANN index trades | Exactness for work. Call it a speedup whose cost you have measured, or you have not measured it | 29 |
| The work a probing index does | Centroids + the vectors in the lists probed. The first term never goes away | 29 |
| When an index is worse than none | When you probe every list: 2020 comparisons against brute force's 2000 | 29 |
| How recall is measured here | Against the exhaustive answer, once, offline, on a sample. Chapter 26's recall@k, not Chapter 24's answer key | 29 |
| The number people do not look at | The worst query. Mean 0.925 with a worst of 0.4 is fourteen perfect queries averaged with six partial ones, not a uniform small loss | 29 |
| What post-filtering returns | About `f × s`: fetch `f` from a tenant holding share `s`. 100 × 0.01 ≈ 1, when you asked for 10 | 29 |
| Why pre-filtering can be cheaper | An ANN index avoids comparing against a million vectors; a tenant owning twenty has no such problem | 29 |
| The number to write down for multi-tenancy | The smallest tenant's share of the corpus | 29 |
| The four steps | Read outputs; note each failure; group and count; let the modes choose the metrics | 30 |
| Why the notes come first | Categories you start with tend to be the ones you already believe, and the exercise exists to escape them | 30 |
| How many failures | Forty is a working number: enough for a pattern to repeat, few enough to read in an afternoon. Sampled, not selected | 30 |
| Why the verb grouping fails | It failed both ways on verbs: 5 of 10 groups held several modes, and 6 of 8 modes were split across groups | 30 |
| How to name a mode | After the output, never after the suspected cause. "Contradicts the passage", not "retrieval problem" | 30 |
| The check on the grouping | Every note in exactly one mode. It proves a partition, and not that the partition is right | 30 |
| What a 1-to-5 score gives you | A number, not a decision about a failure. It may correlate with quality and still name no mode | 30 |
| The cost of a metric chosen first | The best actionable check here covers 20 of 40. Perfect it and 20 failures remain | 30 |
| Which check to build first | The one covering the most failures per unit of work — one check here was 20 failures and closed two modes | 30 |
| When to use a judge rather than code | When the check needs a decision about what text means. Code handles every comparison between things that are both literally present | 31 |
| What a judge returns | Pass or fail on one named failure mode. One judge per mode, never a score | 31 |
| The three cheap measurements, in order | Self-agreement (no labels); flip count under an arbitrary change (no labels); then the baseline (no judge needed) | 31 |
| The baseline | What "always pass" scores. 48 of 60 here, 80 per cent, finding nothing | 31 |
| The two numbers to report | Of the real failures, how many caught; of its alarms, how many real. 5 of 12 and 5 of 7 for judge A | 31 |
| Their interview names | Recall is the share of real failures caught; precision the share of alarms that are real. Chapter 26's recall@k is a different quantity — relevant documents reaching the top k | 31 |
| Why one number hides it | 48 of 60 cases are passes, so agreement is mostly agreement about passes. Judge B caught 10 of 12 against A's 5 and scored 82 against 85 | 31 |
| How many cases to label | Enough *failures*, not enough cases. 60 labels bought 12 failures; the catch rate's interval was 12% to 73% | 31 |
| Position bias, measured | Show each pair both ways and count the flips: 16 of 40 here, a 70%-against-30% swing in the headline | 31 |
| Why two scores per case | One verdict cannot say which stage failed. 62.5 per cent end to end was 75 per cent retrieval and 73 per cent generation given good retrieval | 32 |
| The four cells | Fine; answer there and got it wrong (generation's); answer not there (retrieval's); answer not there and right anyway (a failure, counted as a success) | 32 |
| The cell people miss | Right answer, no supporting passage. 3 of 40 here. Nothing can show where it came from, and nothing notices when the document changes | 32 |
| What grounded means | Every claim supported by a retrieved passage. Chapter 28's entailment test applied to every claim, not only the cited ones | 32 |
| Why the unit matters | 3 of 6 claims against 3 of 4 sentences — 25 points, same answer. The coarser unit lets a supported claim vouch for an unsupported one | 32 |
| The two independent measures | Groundedness and answer relevance. A sentence copied from an off-topic retrieved passage is 100% grounded and answers nothing | 32 |
| The no-claims answer | A refusal has nothing to support, so a careless groundedness figure scores it 100% and rewards refusing. Pair it with a refusal detector | 32 |
| Where cases come from | Real failures for the questions people ask; generated questions for a free answer key and coverage | 32 |
| The cost of a generated set | With a word-overlap retriever, 8 of 8 generated against 2 of 8 asked on the same passages — a generated question shares 3 to 6 words with its source, a real one none or one. A retriever that does not match words would narrow the gap; by how much is a measurement, not a prediction | 32 |
| Score against list | A score is the net of fixes and breakages. Version 2 was +1 case = 4 fixed − 3 broken, which is +5 points on twenty cases | 33 |
| The blind spot in a failures-only set | It reported 0 regressions when there were 3, because all three passed the previous version | 33 |
| The two honest sets | Everything, or every case that has ever failed — the second reports the breakage it missed as a standing failure, not as a regression, and catches the NEXT breakage of that case | 33 |
| When a case is a regression | When it fails *more often* than it passed — a tie is not one, and that tie-break moved this set's result from 5 of 5 to 0 of 5 at four repeats | 33 |
| What one run costs | 2 regressions and 2 fixes reported against 1 real fix; all 5 available runs reported a regression that was not there | 33 |
| Criteria drift, measured | The same 40 outputs: 85% in week 1, 72.5% in week 5, 7 flips, 6 of them to fail | 33 |
| How to measure drift | Re-label a sample of old outputs without looking at the old label, and count the flips | 33 |
| What a trace holds | Input, retrieval query and candidates with scores, model and version, tool calls, output, tokens, per-stage timings | 33 |
| The content trade | Drop the 4 content fields of 16 and 5 of 8 questions survive; the 3 lost are the ones needing the text, including whether a case can exist at all | 33 |
| The five fixed paths | Chaining, routing, parallelisation, orchestrator–workers, evaluator–optimiser | 34 |
| The column that matters | Whether the call count is settled by your input or by something a model said. 4 of the chapter's 6 designs, not 6 | 34 |
| Which patterns are not fixed in length | Orchestrator–workers and evaluator–optimiser — a model decides the pieces, a judge decides when to stop | 34 |
| Why a loop costs more than a chain of the same length | It re-sends the whole record each step, so the total has a square in it | 34 |
| The step-limit arithmetic | 10 steps to 20 doubles the calls and multiplies tokens by 3.4; 20 to 40 by 3.7 | 34 |
| Where the window wall is | On a 128,000-token window: step 638 at 200 tokens a step, step 13 at 10,000. The window stops a terse loop nowhere useful and a fat-stepped one in the range where step limits are set | 34 |
| When an agent is warranted | You cannot enumerate the paths **or the shape** — if the shape is one of the five you have a pattern, not an agent — **and** there is a cheap check. The second is a veto on letting a model choose outside a list your code wrote, not a reason for it | 34 |
| What decides the approval point | Whether a wrong step can be undone — not whether to use an agent | 34 |
| The order to try | One call, chain, router, parallelise, orchestrator, evaluator–optimiser, loop. An order of added machinery, not of freedom. Climb when the evaluation set fails | 34 |
| Where a loop's context goes | Tool results — 91.5% of the worked run, against 2.6% instruction and 1.4% tool definitions | 35 |
| The compaction trigger | Room left must be at least the largest single result: `\(\text{window} - p \times \text{window}/100 \ge \text{largest}\)`{=latex} | 35 |
| Worked: trigger | 128,000-token window, 8,400-token largest result, so 93% — not 95% | 35 |
| Up front against just in time | Up front only wins at 11 of 12 documents | 35 |
| First into the must-keep list | The negative results — the cheapest line in it | 35 |
| A note's two fields | Where it came from, and when it was written | 35 |
