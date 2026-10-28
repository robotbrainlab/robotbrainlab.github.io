# Glossary

Every term the book defines, with the chapter that owns it. A term is defined in exactly one
chapter; every other chapter refers to it rather than redefining it.

| Term | Meaning | Ch |
|---|---|---|
| **429** | *Too many requests.* The provider's rate limit, on requests per minute and on tokens per minute. Retryable when you are going too fast; the same status comes back when the account is out of credit, which no wait fixes | 19 |
| **Accountability** | Somebody who can be asked to answer for a decision, and who bears a consequence for it. A property of people and organisations, never of a component | 3 |
| **Activation function** | The feed-forward block's one step that is not a matrix multiplication, such as keeping positives and zeroing negatives. Without it the block's two matrices would collapse into one | 12 |
| **Active parameters** | The parameters that actually run for a given token, as against the total the model holds. Cost follows the active figure; the name usually quotes the total | 15 |
| **Agent** | A system in which the model decides what to do next, repeatedly, rather than your code deciding the sequence | 4 |
| **Approval point** | A step the loop cannot pass without a person, enforced in your code rather than requested in the instructions | 4 |
| **Assistant message** | What the model said earlier in the conversation, sent back to it by your code. The model does not remember saying it | 18 |
| **Attention** | The step in which each position takes a weighted blend of information from the others, in amounts computed from the content rather than fixed in advance | 11 |
| **Attention block** | The half of a layer that moves information between positions — Chapter 11's formula in full. The only part of a model that does | 12 |
| **Attention head** | One complete set of query, key and value matrices and the weights they produce. A layer runs several in parallel over slices of the width, and a final matrix mixes their outputs | 11 |
| **Attention weights** | One row of the grid after scaling, masking and softmax: positive numbers adding to 1, saying how much of each position to take | 11 |
| **Autoregressive** | Producing output one token at a time, with each token appended to the input before the next pass | 9 |
| **Backpropagation** | The procedure that computes a derivative for every parameter in one backward sweep through the model. How the gradient of Chapter 14's update rule is obtained. Not taught in this book | 17 |
| **Base model** | A model that has had only pretraining. It continues text rather than answering, which is what the later stages change | 14 |
| **Batch endpoint** | Upload requests, collect results hours later, pay substantially less. For work nobody is waiting on | 19 |
| **Batching** | Running many requests through the same forward pass, so one read of the parameters serves all of them. Close to free up to a point — each request still reads its own cache and does its own arithmetic — which is why the price per token is low and why your neighbours affect your output | 15 |
| **Big-O** | How a cost grows as an input grows, with constants and smaller terms deliberately discarded. Not a measurement of time | 8 |
| **Bootstrap** | Estimating how much a statistic would move by resampling your own cases with replacement. One procedure for every statistic you score, where a closed form is a different formula each time | 20 |
| **Byte-pair encoding** | Building a vocabulary by starting from the 256 single bytes and repeatedly merging the commonest adjacent pair in a corpus until the vocabulary is the size wanted. Starting from bytes is what makes any text at all representable | 10 |
| **Case** | One input plus whatever marks the answer right or wrong. The unit the statistics count — and they count rows, so forty rephrasings of one question are worth nearer one case than forty | 20 |
| **Causal mask** | Setting every score for a later position to minus infinity before softmax, so it gets exactly zero weight. It makes a position's output depend only on what precedes it, so the arithmetic is the same whether or not the rest of the sentence exists | 11 |
| **Check** | Anything that verifies the output before it is used, from a required shape through to a second model's opinion | 2 |
| **Compound system** | A system of several parts with the model as one of them, rather than as the whole product | 2 |
| **Compounding error** | Two things at once across a run: each step's chance of being right multiplies against the others, so a high per-step figure becomes a low whole-run one; and a wrong step's result is carried into the next step as though it were true | 4 |
| **Compute-bound** | A step whose speed is set by the arithmetic it has to do rather than by how fast its numbers arrive. Prefill is; a large enough batch becomes so | 15 |
| **Concept owner** | The single chapter that teaches a given concept. Every other chapter refers to it by number rather than re-teaching it, so the reader never meets three partial explanations of one thing | 7 |
| **Confidence interval** | The range a measurement would fall in most of the time if you repeated it. Here, the 2.5th to 97.5th percentiles of the resampled scores | 20 |
| **Context** | Everything sent to the model on one call: the instructions, any added material, and the request | 2 |
| **Context window** | The maximum number of tokens a model will accept at once. A cost limit rather than a memory, counting the reply as well as the request. The whole conversation is re-sent every call, and something is dropped — or the call refused — when it fills | 16 |
| **Cosine similarity** | The dot product divided by both lengths, which removes magnitude and keeps direction. Always between −1 and 1 | 8 |
| **Cross-entropy** | The training objective: the average of `\(-\log p\)`{=latex} over every position, where `\(p\)`{=latex} is the probability given to the token that actually came next. Zero for a perfect prediction, unbounded for a confident mistake | 14 |
| **Current convention** | How competent engineers work at the moment: true, load-bearing and replaceable. It usually names a technique rather than a reason, and usually has a predecessor you can remember | 6 |
| **Dated detail** | A fact with a date on it — a name, a number, a version. It stops being true when somebody ships something or changes a price | 6 |
| **Decode** | One forward pass per output token. Does almost no arithmetic and is limited by reading every parameter the pass uses out of memory once per token | 15 |
| **Delta** | One streamed piece: what to add to what you have, not the whole answer again | 19 |
| **Depth** | The number of layers in the stack. The last of the three numbers — vocabulary, width, depth — that describe a model's shape | 9 |
| **Dimension** | One slot in a vector. A position in a list, not a direction in space, and usually not nameable on its own | 8 |
| **Direct preference optimisation (DPO)** | The preference objective written as one formula: raise the preferred reply's probability relative to the rejected one, both measured against the model as it was before this stage. Stated in this book, not derived | 14 |
| **Dot product** | Multiply two vectors slot by slot and add the results. Large when both are large in the same slots — and also larger when either is simply longer | 8 |
| **Embedding table** | A matrix with one row per vocabulary entry. Looking a token up in it is how that token enters the model; the rows are called embeddings | 9 |
| **Error analysis** | The part of evaluation that means reading real outputs, sorting the failures into kinds, and working on the largest kind | 5 |
| **Evaluation** | Building and using something that tells you whether a system works: a set of cases, a way to judge each answer, and a number you can compare over time | 5 |
| **Evidence strength** | How much a claim is supported: announcement, demonstration, one study, practitioner report, settled practice — or a derivation, which stands outside the ladder because you can check it yourself | 6 |
| **Examples** | What a good answer looks like, shown rather than described. Part of the specification | 18 |
| **Exponential backoff** | Doubling the wait after each failed attempt, up to a cap, so a struggling system is not hammered | 19 |
| **Feed-forward block** | The half of a layer that works on each position alone: two matrices with an activation between them, the middle several times wider than the ends. Holds more of a layer's parameters than attention does | 12 |
| **Forward pass** | One journey through the model — lookup, the stack once, one distribution out. It produces exactly one distribution | 9 |
| **Foundation model** | A model trained once on general material, then used for many tasks it was not specifically built for | 1 |
| **Generalisation theory** | Why a model fitted to one body of text works on text it never saw — the bias–variance trade-off, and what learning theory proves about it | 17 |
| **Gradient** | For each parameter, how much the loss would rise if that parameter rose. The update rule moves every parameter a small step against it. How it is computed is outside this book | 14 |
| **Greedy decoding** | Always taking the highest-scoring token. What "temperature zero" does in practice, since dividing by zero is not defined | 13 |
| **Hallucination** | Output that is fluent, plausible and not true. Not a malfunction: no step in the computation checks anything, so a plausible continuation is all the mechanism can produce | 16 |
| **Idempotency** | Doing an operation twice has the same effect as doing it once. What makes a retry after a timeout safe | 19 |
| **Inductive bias** | What a design assumes about the world before it sees any data | 17 |
| **Inference** | Running a finished model to get a reply. This is what "using a model" means | 1 |
| **Initialisation** | What the parameters are set to before training begins, and why the choice matters | 17 |
| **Input tokens** | Everything you send on a call — instructions, attached material and the request. Countable exactly before you send | 10 |
| **Instructions** | What to do, what not to do and who to be. Part of the specification, so it changes rarely and is paid for on every call | 18 |
| **Intermediate reasoning** | Emitting the steps of a problem as tokens so that later passes can condition on them. The only way to carry partial work forward, because one pass runs its layers once however hard the question is, and nothing persists between passes | 16 |
| **Interview depth** | Knowing something well enough to give the mechanism, the trade-off, and how you would check it, in about a minute of speech. Not exhaustive, and more than a summary | 7 |
| **Irreversible action** | Something a tool does that cannot be undone once it has happened — a refund, a message, a deletion. The reason a tool's reach is decided before it is offered | 3 |
| **Jitter** | Waiting a random amount up to the backoff rather than exactly it, so many workers do not retry in step | 19 |
| **Key** | The vector saying what a position offers to others, made with `\(W_K\)`{=latex}. Scored against every query | 11 |
| **Key–value cache** | The stored keys and values for every position in every layer, so decode attends to earlier positions without recomputing them. Costs `\(2 \times \text{layers} \times d \times \text{tokens} \times \text{bytes}\)`{=latex} | 15 |
| **Lasting principle** | A reason for doing something, or a shape that does not move, which outlives the technique it was first attached to. It stops being true only if the reason itself is wrong | 6 |
| **Latency** | The delay between sending a request and receiving the reply, felt as a wait before the first word and a pace after it | 1 |
| **Layer** | A block of arithmetic taking one vector per position and returning one per position, same width in as out. Every layer has the same shape and its own numbers | 9 |
| **Length** | What a ruler would measure if the slots were coordinates: square every slot, add them, take the square root | 8 |
| **Logarithm** | The inverse of raising `\(e\)`{=latex} to a power. It turns multiplication into addition, which is why it appears wherever many probabilities are combined | 8 |
| **Logits** | The raw scores from the final matrix multiplication, one per vocabulary entry, before softmax. Can be negative; only the differences between them matter | 13 |
| **Matrix** | A grid of numbers, read as rows or as columns depending on what you are doing | 8 |
| **Memory-bound** | A step whose speed is set by how fast numbers arrive from memory rather than by the arithmetic done with them. Decode reads about one byte for every operation it performs, on hardware built for hundreds | 15 |
| **Merge list** | The merges, in the order they were made. Kept with the model and replayed in that order to tokenise any later text | 10 |
| **Mixture of experts** | Replacing one feed-forward block per layer with several and routing each token through a few of them. The model holds all of them and runs some | 15 |
| **Model** | A service that takes text and returns generated text, charged by the amount of text | 1 |
| **Next-token distribution** | One probability for every entry in the vocabulary, adding to 1, saying how likely each is to come next. The entire output of one call | 9 |
| **Normalisation** | Rescaling the stream to a predictable range before each block reads it, so the numbers do not grow out of hand as layer after layer adds to them | 12 |
| **Numerical stability** | How quantities behave through long chains of arithmetic, and what keeps them in a usable range. The subject behind Chapter 12's one sentence on normalisation. Not taught in this book | 17 |
| **Objective design** | Why one expression rather than another is the right thing for a model to minimise. The question Chapter 14 states its preference objective without answering. Not taught in this book | 17 |
| **Optimisation theory** | The study of when a procedure like the update rule converges, to what, and how fast. Not taught in this book | 17 |
| **Optimiser design** | Choosing and adapting the step size and the form of the update. Not taught in this book | 17 |
| **Output format** | The shape the answer must take, stated rather than hoped for. Part of the specification | 18 |
| **Output tokens** | Everything that comes back. Priced several times higher than input, one forward pass each, and not knowable in advance | 10 |
| **Paired comparison** | Running both versions on the same cases and keeping the results together, so the part of case-to-case variation the two versions share cancels when you subtract | 20 |
| **Parameter** | One number inside the model, set by training and unchanged by inference. The count is what "a 7B model" reports | 9 |
| **People** | The reviewers and approvers who handle the consequential cases and carry responsibility for them | 2 |
| **Perplexity** | The exponential of the cross-entropy. Reads as the number of equally likely options the model is effectively choosing between; a uniform choice among `\(V\)`{=latex} options has perplexity `\(V\)`{=latex} | 14 |
| **Positional encoding** | How a token's position is put into the arithmetic, since the attention formula carries no notion of order. Added to the embedding before the stack, or applied as a rotation to queries and keys, or added to the scores themselves | 11 |
| **Practitioner report** | A survey or a set of accounts of what people say they do. It is a practitioner report however it was published, and it supports what people *do* far better than whether it works | 6 |
| **Preference optimisation** | Training on pairs of replies with a preference between them, to make the preferred kind more likely relative to the other. Changes which of its existing behaviours come out, rather than adding knowledge | 14 |
| **Prefill** | The pass that processes the whole prompt, every position at once. Limited by arithmetic, whose attention part grows with the square of the prompt length and overtakes the rest on a long one. What you wait for before the first word | 15 |
| **Pretraining** | Running the loop on an enormous quantity of general text. Where essentially all of a model's knowledge comes from, and nearly all of the computation | 14 |
| **Quantisation** | Storing each parameter in fewer bits. Halving the bits halves the memory and roughly halves the time spent reading, at a cost in precision that has to be measured | 15 |
| **Query** | The vector saying what a position is looking for, made by multiplying its vector by `\(W_Q\)`{=latex} | 11 |
| **Regularisation** | The techniques that stop a model fitting its training data too closely | 17 |
| **Representation learning** | Why fitting a model to predict text arranges its vectors so that the arrangement is useful for other things. The question Chapter 9 refused. Not taught in this book | 17 |
| **Residual connection** | Adding a block's output to the vector that went into it, rather than replacing it. What lets a layer contribute nothing and pass its input through | 12 |
| **Residual stream** | The running vector passing up through the stack, which every block adds into. By the end it is a sum of every contribution made along the way, with nothing marking which is which | 12 |
| **Retrieval** | Searching your own collection for the passages that bear on a request, so they can be put into the context | 2 |
| **Rubber-stamping** | Approval given without real attention, usually because the volume is too high for any. It costs what review costs and delivers none of its value | 3 |
| **Scaling laws** | The relationships between model size, data, compute and loss, and their derivation | 17 |
| **Semaphore** | A counter that bounds how many jobs run at once. Three words of code, and the difference between concurrency and attacking your own account | 19 |
| **Server-sent events** | A long-lived HTTP response carrying one small event per line as the server produces them. How a streamed reply arrives | 19 |
| **Softmax** | Turns a list of scores into positive numbers that sum to 1, preserving their order and exaggerating the gaps between them | 8 |
| **Step** | One pass through the loop: the model decides, something runs, the result comes back | 4 |
| **Stop condition** | A string you nominate that halts generation when it appears. Providers call it a stop sequence; it is not Chapter 4's stopping condition. One of the ordinary ways a reply ends, alongside the model's own stop token and your maximum | 13 |
| **Stop token** | An entry in the vocabulary meaning *finished*, scored and sampled like any other token. Often called an end-of-sequence token. A model stops talking by predicting that it has stopped | 13 |
| **Stopping condition** | The set of rules that end a run — the model finishing, a step limit, or your code refusing | 4 |
| **Subword** | A token that is part of a word rather than a whole one. What makes it possible to represent a word the vocabulary has never seen | 10 |
| **Supervised fine-tuning** | Running the same loop with the same objective on curated request–response pairs. Turns a model that continues text into one that answers | 14 |
| **Supplied information** | The part of a prompt that is different on every call. The only one of the four parts that is data rather than specification | 18 |
| **System message** | The message holding your instructions and usually the output format. Your specification, set once per conversation and never the thing to drop when the history will not fit — nor are the example turns, if that is where your examples live | 18 |
| **Temperature** | A number the logits are divided by before softmax. Below 1 sharpens the distribution, above 1 flattens it, and it never changes the order | 13 |
| **Token** | One entry in a model's vocabulary — usually a piece text is cut into. Beyond the single bytes, which are always there, which pieces earned an entry is a matter of frequency in the corpus the vocabulary was built from — not of meaning or length | 10 |
| **Token bucket** | A limiter on the *rate* rather than on how many run at once, for when the requests-per-minute limit is the one that hurts | 19 |
| **Tokeniser** | The program that cuts text into tokens and maps them to indexes, using one model's vocabulary and merge list. A different model's tokeniser gives a different count | 10 |
| **Tool** | An action the model may ask for. The model proposes it; your code decides whether to run it | 2 |
| **Tool message** | A result your code returns after the model asked for something. Chapter 23 | 18 |
| **Top-k** | Keeping only the `\(k\)`{=latex} highest-scoring tokens and renormalising. Keeps the same number of options however confident the model is | 13 |
| **Top-p** | Also called nucleus sampling. Keeping the smallest set of tokens whose probabilities add to at least `\(p\)`{=latex}, then renormalising. Narrow where the model is confident, wide where it is not, at the cost of not knowing in advance how many survive | 13 |
| **Total timeout** | The cap on a whole call, as distinct from the gap between chunks that most libraries call the read timeout. Derived from the token cap | 19 |
| **Training** | The one-time process that produced the model's numbers. Not something you do on a request | 1 |
| **Training cut-off** | The point in time after which no text reached the model's training. It knows nothing later, and cannot tell that it does not | 1 |
| **Trials** | Repeated runs of the same case, which measure the model's own variation. Averaged within the case, never counted as extra cases | 20 |
| **Turn** | One exchange — the user's message and the model's reply to it. A conversation is a list of turns, and the whole list is re-sent on each one | 18 |
| **User message** | The request and the material it is about, from the person or from your code on their behalf | 18 |
| **Value** | The vector a position hands over when it is attended to, made with `\(W_V\)`{=latex}. What the weights are spent on | 11 |
| **Vector** | An ordered list of numbers. Two vectors can be compared only if they have the same number of slots | 8 |
| **Vocabulary** | The fixed, numbered list of every entry a model can read or produce — nearly all pieces of text, and a few that are not. Built once, before training, and fixed while you use the model | 9 |
| **Width** | The number of slots in the vectors moving from layer to layer, the same all the way through. Written `\(d\)`{=latex} in formulas | 9 |
