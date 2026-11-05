# Research output — systems, hardware and infrastructure

**Run 2026-11-06.** Brief: `pilot-01-systems-brief.md` (in this folder). Pilot run 01.
**Budget used: 11 of 25 searches, 16 of 25 fetches. Zero sub-agents. Stopped on completeness.**

Six subject records, all with the verdict `CHAPTER`. Reproduced as returned, except that my own
framing is removed. The agent's sampling report is at the end and should be read first.

---

## 1 · Accelerator architecture and the memory wall

**NAME** — Accelerator architecture and the memory wall. Also: AI accelerator microarchitecture,
domain-specific architecture, near-memory/processing-in-memory (PIM/PNM), memory-centric computing.

**WHY IT MATTERS** — A transformer's two phases have opposite shapes. Prefill is a dense matrix
multiply with high arithmetic intensity and sits near the compute roof. Autoregressive decode reads
the whole weight set and the whole KV cache to emit one token per sequence, so it is bounded by
bytes moved, not FLOPs. Accelerators have been sold on peak FLOPs while delivered decode throughput
tracks HBM bandwidth, and the gap has widened with every generation. Attention now matters because
reasoning and agent workloads push context toward 10⁶ tokens, where the KV cache can rival or
exceed the weights. The question an engineer faces is which part of the chip is actually idle, and
why.

**FOUNDATIONS** — The roofline model (Williams, Waterman, Patterson, *CACM* 2009): performance is
min(peak FLOP/s, arithmetic intensity × peak bandwidth), so every kernel has a knee. Beneath it:
Amdahl's law; the energy cost of data movement versus arithmetic, where an off-chip DRAM access
costs orders of magnitude more pJ than a MAC (Horowitz, ISSCC 2014); Little's law for latency
hiding; and the physical limits of off-package signalling that motivate stacked HBM and 2.5D/3D
integration. Hennessy and Patterson's "A New Golden Age for Computer Architecture" (2019) is the
standard framing for domain-specific architecture; Jouppi et al.'s TPU paper (ISCA 2017) is the
canonical worked example. **All four references are from the agent's training data and were not
fetched.**

**LIVE RESEARCH** — *28 August 2026*: a survey, "AI Hardware Accelerators for Large Language
Models: Architectures and the Memory Wall" (arXiv:2608.28048, a review article, not peer-reviewed),
compares GPUs, TPUs, Trainium, Groq, Cerebras, FPGAs, PIM/near-memory, neuromorphic and photonic
designs under one roofline framing, and concludes "the decisive constraint on LLM acceleration is
not arithmetic but memory". It names processing-in-memory the most promising near-term response and
judges neuromorphic and photonic computing not production-ready at frontier scale. Its abstract
carries no numbers. *28 April 2026, revised 30 October 2026*: AMMA (arXiv:2604.26103, accepted to
MICRO 2026) replaces GPU compute dies with HBM-PNM cubes in a multi-chiplet part aimed at 1M-token
decode attention, claiming roughly double the usable bandwidth, 15.5× lower attention latency and
6.9× lower energy than an H100. **Unresolved:** whether PNM logic dies can be programmed generally
enough to be worth the area, and what the H100 baseline was tuned to — the abstract does not say.

**ENGINEERING** — Real parts are a compute die (or chiplets) surrounded by stacked HBM on an
interposer, with an on-chip hierarchy (register file → SRAM scratchpad → L2) whose job is to raise
arithmetic intensity enough to reach the compute roof. **Central trade-off:** capacity versus
bandwidth versus cost per stack — more HBM stacks buy both and burn beachfront area, power and
yield. **Second trade-off:** generality versus efficiency — a systolic/tensor-core datapath wins on
dense GEMM and loses on anything irregular. Tools in real use: Nsight Compute and `rocprof` for
achieved-bandwidth and occupancy counters; `nvidia-smi`/DCGM for clocks and power caps; the CUTLASS
profiler; gem5/Accel-Sim or analytic spreadsheets for architecture exploration.

**BUILDABLE** — Take one open 7B–8B model on one GPU and sweep decode batch size from 1 to 256 at
fixed context length. For each step compute the bytes that *must* move (weights + KV cache read per
step) divided by measured step time. Plot against the device's spec HBM peak.
**Measurements:** achieved HBM bandwidth as a percentage of spec peak; arithmetic intensity in
FLOP/byte; the batch size at which the kernel crosses the roofline knee from bandwidth-bound to
compute-bound. **Hardware: one GPU.**

**VERDICT** — Mechanism: yes, the roofline knee explains why decode and prefill want different
silicon. Live research: yes, two 2026 items, one peer-reviewed at MICRO. Buildable: yes.
**CHAPTER.** It is the mechanism every other subject in this area is downstream of.

---

## 2 · Interconnect and collective communication

**NAME** — Interconnect and collective communication. Also: scale-up fabric versus scale-out
network, NVLink/NVSwitch, UALink, Ultra Ethernet, RDMA, collectives, in-network compute, SHARP.

**WHY IT MATTERS** — Above one accelerator the model no longer fits and every step becomes a
communication problem. Tensor parallelism exchanges activations inside each layer and needs the
fast, short scale-up domain; data and pipeline parallelism tolerate the slower scale-out network;
MoE expert parallelism needs all-to-all, the least forgiving pattern of all. **The fabric sets the
shape of the parallelism plan, not the other way round.** It is live now for two reasons: scale-up
domains have grown from 8 to the high tens of accelerators per coherent group, turning an in-node
problem into a switched-fabric problem; and decode puts *small* collectives on the critical path of
every token, so the latency floor — not asymptotic bandwidth — is the user-visible number.

**FOUNDATIONS** — The latency–bandwidth (α–β, Hockney) cost model: time ≈ α + S/β per message,
which splits collectives into a latency-dominated small-message regime and a bandwidth-dominated
large-message one. The bandwidth-optimal ring all-reduce lower bound of 2(N−1)/N × S/β, and the
log-depth latency-optimal tree — which is why production libraries switch algorithm by message
size. Beneath that: bisection bandwidth and topology (fat tree, torus, dragonfly), and the physical
limit that drives all of it, electrical reach at a given signalling rate, which is why scale-up is
short copper and scale-out is optics. **Canonical references (Thakur & Rabenseifner on MPI
collective algorithms; Hoefler et al. on performance modelling) are from training data and were not
fetched.**

**LIVE RESEARCH** — *17 July 2026*: "Every Microsecond Matters: Achieving Near Speed-of-Light
Latency in GPU Collectives" (arXiv:2607.16100) attacks the small-collective regime using
barrier-free synchronisation, symmetric memory and hardware multicast on NCCL's device-side API,
reporting overhead within 7% of an absolute speed-of-light lower bound for small and medium
messages, with improved inter-token latency in LLM inference. **The abstract gives no absolute
latencies, no GPU model and no NVSwitch generation.** *7 April 2026*: the UALink Consortium
ratified four specifications — Common Specification 2.0 (adding in-network compute), a separated
Data Link/Physical Layer 2.0 at 200G signalling, Manageability 1.0 (gNMI, YANG, SAI, Redfish) and
Chiplet 1.0 (compatible with UCIe 3.0); trade press reporting the announcement put silicon in 2027.
Every figure there is a consortium claim with no independent measurement. **Unresolved:** whether
collective offload into the switch pays for its complexity, and whether an open scale-up fabric
reaches parity before the proprietary one moves again.

**ENGINEERING** — Two fabrics, deliberately different. **Scale-up:** load/store/atomic semantics
between accelerators over short switched links, for tensor parallelism and the small
latency-critical collectives. **Scale-out:** RDMA over converged Ethernet or InfiniBand, for data
and pipeline parallelism, where one degraded link makes a ring all-reduce run at the straggler's
rate. **Central trade-off:** latency floor versus reach and cost — every metre of copper, every
retimer and every optical hop adds α, and α is what decode pays per token. Tools: NCCL and RCCL
with `NCCL_ALGO`/`NCCL_PROTO` tuning; nccl-tests for busbw curves; NVSHMEM and symmetric memory for
device-initiated transfer; SHARP for switch-side reduction; DCGM and fabric counters to find the
slow link.

**BUILDABLE** — Run `all_reduce_perf` and `alltoall_perf` from nccl-tests on one multi-GPU node
across message sizes from 8 bytes to 1 GB, then fit the α–β model to the curve.
**Measurements:** the latency floor α in microseconds (the small-message asymptote); achieved bus
bandwidth β in GB/s as a percentage of the link's spec peak; the message size at which the two
regimes cross. Repeat with one GPU's clocks or link width reduced, to see the straggler effect.
**Hardware: one multi-GPU node. No single-GPU substitute.**

**VERDICT** — Mechanism: yes, the α–β model and the collective lower bounds predict which
parallelism a fabric can carry. Live research: yes, a July 2026 preprint and an April 2026
specification set. Buildable: yes. **CHAPTER.** The fabric decides the parallelism plan, so it
cannot be left to the training subject.

---

## 3 · Numerical precision and quantisation as a systems concern

**NAME** — Numerical precision and quantisation as a systems concern. Also: low-precision training,
FP8/FP4, microscaling (MX) formats, MXFP4, NVFP4, block floating point, post-training quantisation.

**WHY IT MATTERS** — Precision is the one knob that moves compute, memory capacity, memory
bandwidth and interconnect traffic at once: halving the element width roughly doubles the
tensor-core rate and halves the bytes a bandwidth-bound decode must read. That is why every recent
accelerator generation added a narrower format rather than only more FLOPs. But the format is not a
free choice. Narrow floating point has a tiny dynamic range, and transformer activations have
heavy-tailed outliers, so a naive cast diverges. **The engineering content is in the scaling
scheme** — how many elements share a scale, what type that scale is, and what transform is applied
before quantising — and the systems content is that those choices are baked into the hardware's
instruction set, so they are not tunable after tape-out.

**FOUNDATIONS** — IEEE 754 and the exponent/mantissa split, which fixes the dynamic-range-versus-
resolution trade. Loss scaling and master weights from mixed-precision training (Micikevicius et
al., ICLR 2018). The FP8 E4M3/E5M2 format pair (Micikevicius et al., 2022). Block floating point,
revived as the Open Compute Project's Microscaling (MX) specification, where 32 elements share one
scale — the group size is the whole argument. Stochastic rounding, which makes a quantised gradient
an unbiased estimator rather than a systematically truncated one. Incoherence processing by random
rotation (Hadamard transforms), which spreads outlier energy across a block, from the QuIP line.
**The ICLR 2018, 2022 and QuIP references are from training data and were not fetched.**

**LIVE RESEARCH** — *4 March 2026* (v2 of a September 2025 preprint): "Pretraining Large Language
Models with NVFP4" (arXiv:2509.25149, NVIDIA, ~90 authors) trains a 12B model on 10T tokens in a
4-bit format — described as the longest publicly documented 4-bit training run — reporting training
loss and downstream accuracy comparable to an FP8 baseline, using random Hadamard transforms,
two-dimensional quantisation consistent across forward and backward passes, stochastic rounding,
and selected layers held at higher precision. **It is a vendor paper on a format the vendor sells,
and the abstract page gives neither the benchmark scores nor the names of the high-precision
layers.** *3 March 2026* (v3): "Bridging the Gap Between Promise and Performance for Microscaling
FP4 Quantization" (arXiv:2509.23202) finds NVFP4's small group size "provably neutralizes
traditional outlier mitigation techniques" and MXFP4's power-of-two scales induce high error; its
MR-GPTQ with block-wise Hadamard transforms closes most of the gap, with kernels reaching up to
3.6× layer-wise and 2.2× end-to-end on a B200, and 6×/4× on an RTX 5090 — against an FP16 baseline
whose tuning the abstract does not describe. **Unresolved:** the scaling behaviour of 4-bit
pretraining at larger parameter counts and token horizons.

**ENGINEERING** — Production practice is per-tensor or per-channel FP8 for most GEMMs with BF16
master weights and optimiser state; block-scaled MXFP8/MXFP4/NVFP4 where the hardware has native
block-scaled MMA; and a short list of sensitive layers (embeddings, the final projection,
normalisation, often the first and last blocks) kept wider. **Central trade-off: group size.** Small
groups track local dynamic range better and cost more scale storage and more scale-handling work
per MMA; large groups are cheap and let one outlier wreck a block. **Second trade-off:** a Hadamard
rotation buys accuracy and must be fused into the kernel or it costs more than the format saves.
Tools: Transformer Engine, torchao, llm-compressor, TensorRT Model Optimizer, bitsandbytes,
QuTLASS/CUTLASS for the block-scaled kernels.

**BUILDABLE** — Load one open 7B checkpoint's weights, pick a handful of real activation batches,
and compute the error of `W·x` against a BF16 reference for INT4, MXFP4 (power-of-two shared scale,
32-element groups) and NVFP4 (E4M3 shared scale, 16-element groups). Repeat with a random Hadamard
rotation applied first. **Measurements:** relative Frobenius error and max-absolute error per
format; the error reduction factor from the rotation; error as a function of group size, sweeping
16/32/64/128. **Hardware: none. This is numerics, not kernels — it runs on a laptop**, and it
reproduces the central claim of both 2026 papers in an afternoon.

**VERDICT** — Mechanism: yes, dynamic range versus group size versus rotation. Live research: yes,
two March 2026 items from opposing vantage points, one vendor and one academic. Buildable: yes,
with no special hardware. **CHAPTER.** It is the one lever that moves compute, capacity and
bandwidth together.

---

## 4 · Compilers and kernels

**NAME** — Compilers and kernels. Also: GPU kernel engineering, tile-based DSLs, Triton,
CUTLASS/CuTe, kernel fusion, autotuning, `torch.compile`, kernel-authoring agents.

**WHY IT MATTERS** — Between a model expressed as tensor operations and silicon that wants tiles
there is a translation nobody can skip. Done badly, a bandwidth-bound chain of elementwise
operations reads and writes HBM once per operation and runs at a fraction of the roof; done well it
is fused into one pass. **This is where the memory-wall subject's number is actually cashed in.**
Attention is the standing example: the algorithm did not change, the memory traffic did. It is live
for two reasons. Newer tensor-core generations expose instructions much harder to target by hand —
asynchronous MMA with its own memory space, cluster-level cooperation, block-scaled operand types —
so the gap between a naive kernel and the roof has widened. And language models are now being
pointed at kernel writing, which raises a sharp question about what abstraction level a search
should operate at.

**FOUNDATIONS** — The polyhedral/loop-transformation tradition — tiling, fusion, software
pipelining — as the formal account of why reordering loops changes memory traffic without changing
results; Halide's separation of algorithm from schedule (Ragan-Kelley et al. 2013) is the clearest
modern statement. Triton's block-level programming model (Tillet, Kung, Cox, MAPL 2019), which
trades per-thread control for a tile abstraction the compiler can schedule. IO-aware algorithm
design, where the objective is HBM accesses rather than FLOPs (FlashAttention, Dao et al., NeurIPS
2022). Underneath all of it, the roofline again, as the bound a kernel is measured against. **All
four references are from training data and were not fetched.**

**LIVE RESEARCH** — *30 March 2026*: "Improving Efficiency of GPU Kernel Optimization Agents using
a Domain-Specific Language and Speed-of-Light Guidance" (arXiv:2603.29010) argues the abstraction
level is the problem. On 59 KernelBench problems, GPT-5-mini generating low-level code was a 0.40×
geomean **regression** against PyTorch; their μCUTLASS DSL took it to 1.27×; and adding
speed-of-light guidance — using first-principles performance bounds to steer and budget the search
— reached 1.56×, while SOL budgeting saved 19–43% of tokens retaining at least 95% of the geomean
speedup. **The abstract does not say whether the PyTorch baseline was eager or compiled, nor which
GPU.** SOL analysis also caught kernels that looked fast but did not compute the intended result.
*6 August 2026* (page last-updated date): NVIDIA's CUTLASS documentation for Blackwell shows what
the target now looks like — layout and tensor-alignment requirements for emitting `tcgen05.mma`, a
restricted set of supported MMA tile shapes, block-scaled kernels, and SM120 choices between
pingpong and cooperative warp-specialised scheduling. **Unresolved:** whether a DSL plus a bound is
enough, or whether autotuning search spaces must shrink as hardware grows more constrained.

**ENGINEERING** — Three layers coexist. Vendor libraries (cuBLAS, cuDNN, hipBLASLt) for standard
shapes. A template layer — CUTLASS/CuTe, now with a Python DSL — where tile shapes, cluster
dimensions, epilogue fusion and pipeline stages are explicit. And Triton for kernels that must be
written and autotuned quickly, which is how most attention and fused-elementwise kernels in open
inference servers are actually shipped. **Central trade-off: control versus portability.**
Hand-written CUTLASS gets closest to the roof on one architecture and must be rewritten for the
next; a Triton kernel recompiles and leaves performance on the table until its configuration space
is re-searched. Tools: `torch.compile`/Inductor, Triton's `autotune`, the CUTLASS profiler, Nsight
Compute for stall reasons, KernelBench as the shared yardstick.

**BUILDABLE** — Write one fused kernel — softmax, or a GEMM plus bias plus activation — in Triton,
then autotune it over `BLOCK_M`/`BLOCK_N`/`BLOCK_K`, `num_warps` and `num_stages` for one fixed
problem shape. **Measurements:** achieved TFLOP/s and achieved HBM GB/s as a percentage of the
device's roofline bound for that shape; the ratio between the best and worst autotune configuration
(routinely several-fold, which is the point); the same shape's time under `torch.compile` and under
the vendor library. Then change only the sequence length and re-measure without re-tuning, to see
the portability cost directly. **Hardware: one GPU.**

**VERDICT** — Mechanism: yes, tiling and fusion change memory traffic without changing results, and
the roofline scores the outcome. Live research: yes, a March 2026 preprint and NVIDIA documentation
dated August 2026. Buildable: yes. **CHAPTER.** This is where the memory-wall argument is either
cashed in or lost.

---

## 5 · Training systems at scale

**NAME** — Training systems at scale. Also: distributed training, hybrid/5-D parallelism,
ZeRO/FSDP, expert parallelism, scheduling, checkpointing, fault tolerance, silent data corruption.

**WHY IT MATTERS** — A frontier training run is a single tightly coupled job across tens of
thousands of accelerators for weeks, in which every step is a global barrier. Two things follow.
First, the parallelism plan — how the model is cut across tensor, pipeline, data, sequence and
expert dimensions — is a constrained optimisation against memory capacity, collective cost and
fabric topology, and a bad plan shows up directly as low model FLOP utilisation. Second, at that
scale rare hardware faults become routine, and the worst are **silent**: a defective unit corrupts a
computation without raising an error, and the symptom is a loss spike indistinguishable from a
software bug or a numerical instability. **Engineers lose weeks to phantom code problems.** Both
halves are systems problems, not learning problems.

**FOUNDATIONS** — Memory accounting as the first constraint: parameters, gradients, optimiser state
and activations, which is what ZeRO's sharding (Rajbhandari et al., SC 2020) and activation
recomputation trade against communication and recompute. Tensor-parallel layer partitioning
(Megatron-LM, Shoeybi et al. 2019) and pipeline bubble analysis (GPipe; the 1F1B interleaved
schedule). Model FLOP utilisation as the single honest efficiency metric. For reliability: the
classical optimal-checkpoint-interval result, where the interval scales roughly as √(2 × checkpoint
cost × MTBF) (Young 1974; Daly 2006), which is why checkpoint cost and failure rate jointly set how
much work a failure destroys. Determinism — identical inputs producing bit-identical outputs — is
the precondition for comparing replicas at all. **These references are from training data and were
not fetched.**

**LIVE RESEARCH** — *13–15 July 2026*, **peer-reviewed, OSDI '26**: "SDCs in the Wild:
Characterizing and Diagnosing SDC-defective GPUs in Production LLM Training" (Zheng et al.,
Shanghai Jiao Tong University and ByteDance Seed) characterises 23 SDC-defective GPUs harvested
from a production cluster and reports that standard synthetic microbenchmarks — intensive GEMM
stress loops — **miss more than 60% of defective devices**, because faults are aging-dependent,
unit-specific (complex math units failing more often than tensor cores) and data-dependent, and are
caught by neither ECC nor thermal protection. Their fix is execution replay with the exact
production model, checkpoint, workload and data; they report deterministic training costing within
0.01% of step time while cutting normalised debug time by 70%, and that SDCHUNTER mitigated 40
production incidents. *6 May 2026*: Piper (arXiv:2605.05049) models memory, compute and
communication across parallelisation schemes for MoE training, identifying all-to-all latency at
scale, weak compute–communication overlap and low utilisation from imbalanced skinny GEMMs, and
reports 2–3.5× higher MFU than X-MoE and an all-to-all algorithm at 1.2–9× the vendor
implementation's bandwidth. **The abstract gives no absolute MFU, accelerator count or machine
name.**

**ENGINEERING** — Hybrid parallelism, mapped to the fabric: tensor and expert parallelism inside
the scale-up domain, pipeline and data parallelism across it, with sequence/context parallelism for
long contexts. **Central trade-off: memory versus communication versus bubble.** Sharding more
reduces memory and adds collectives; longer pipelines reduce per-stage memory and add bubble;
recomputation trades FLOPs for activation memory. Reliability is engineered as fast asynchronous
checkpointing, hot spares with rapid re-sharding, and now deterministic replay as a first-class
debugging mode rather than a research curiosity. Tools: Megatron-LM, DeepSpeed, PyTorch FSDP2,
Megablocks/expert-parallel kernels, NCCL, Slurm/Kubernetes with gang scheduling, DCGM plus per-step
loss and gradient-norm monitoring.

**BUILDABLE** — Two halves, both one-day. **(a)** Train a small transformer on one 8-GPU node and
compute model FLOP utilisation = achieved FLOP/s ÷ device spec peak, sweeping micro-batch size,
sequence length and recomputation on/off, so the memory-versus-throughput curve is a plot rather
than folklore. **(b)** Turn on deterministic algorithms, run two data-parallel replicas on the same
batch, hash a chosen intermediate tensor on each, and confirm bit-identity — then measure the
step-time penalty of determinism as a percentage and compare it with the 0.01% the OSDI paper
reports. Finally flip one bit in one replica's GEMM output and measure how many steps elapse before
the loss curve leaves the run-to-run noise band. **Hardware: 8 GPUs for (a); 2 GPUs for (b).**

**VERDICT** — Mechanism: yes, memory-versus-communication-versus-bubble, and the
checkpoint-interval result. Live research: yes, a peer-reviewed OSDI '26 paper and a May 2026
preprint. Buildable: yes, though (a) needs eight GPUs. **CHAPTER.** The reliability half is the part
engineers are least prepared for and is now well documented.

---

## 6 · Inference serving systems

**NAME** — Inference serving systems. Also: LLM serving, continuous batching, paged KV cache,
prefix caching, prefill/decode disaggregation, speculative decoding, goodput engineering.

**WHY IT MATTERS** — Serving is where the economics of a deployed model are decided, and the
objective is not throughput. A request has two latency targets — time to first token and inter-token
latency — and the useful quantity is **goodput**: the request rate sustainable while requests still
meet both. Prefill and decode fight for the same device: prefill is compute-bound and arrives in
large chunks, decode is bandwidth-bound and wants large batches, and a long prefill scheduled
between decode steps stalls every active stream. Hence the whole current design space — separate
the two phases onto different hardware, cache the KV state so prefix work is not repeated, and
spend spare compute during decode on guessing tokens ahead. **Each buys one target by paying in
another**, which is the thing to understand.

**FOUNDATIONS** — The arithmetic-intensity argument again: decode reads all weights plus the KV
cache per step, so batching is the only way to amortise the read, and Little's law relates batch
occupancy, arrival rate and latency. Continuous (iteration-level) batching, from Orca (OSDI 2022),
which replaced request-level batching. PagedAttention (Kwon et al., SOSP 2023), which applies
virtual-memory paging to the KV cache and turns fragmentation from a capacity ceiling into a
bookkeeping problem. Speculative decoding (Leviathan et al., ICML 2023; Chen et al. 2023), which is
**exact**: a draft is verified by the target model, so accepted tokens are distributed identically
to ordinary sampling — the only loss is wasted compute on rejections. Phase disaggregation for
goodput, from DistServe (OSDI 2024). **All five references are from training data and were not
fetched.**

**LIVE RESEARCH** — *29 September 2026*: vLLM's own guide to disaggregated serving publishes the
negative result as clearly as the positive one. On two L40S GPUs without NVLink serving Qwen2.5-7B
with ~8k prompts at 0.4 req/s, p99 inter-token latency was 169 ms collocated against 29 ms
disaggregated — **but median TTFT was 2.2 s disaggregated against 0.7 s collocated**, because ~1.3 s
of KV transfer lands entirely on the first token, and disaggregation missed a 2 s TTFT target at
every rate tested. The post states that the collocated baseline was `--data-parallel-size 2` and was
not its strongest possible configuration. On one 8-GPU MI300X node with Qwen3-235B-A22B-FP8 at 8
req/s, 73 of 100 requests met a 1 s TTFT and 50 ms ITL target disaggregated against 30 of 100
collocated — about 2.4× goodput on the same hardware. *21 September 2026*: H-Spec
(arXiv:2609.24197) removes the drafter-side KV cache entirely by reusing target-model KV entries in
place, reporting 5.0–13.3% higher mean accepted length and 5.3–12.6% lower batch-1 inter-token
latency over an unnamed best baseline. **The abstract names neither the GPUs nor the serving
engine.** **Unresolved:** whether disaggregation pays below very fast fabrics.

**ENGINEERING** — A server is a scheduler over a paged KV allocator. Requests are admitted per
iteration; prefill is chunked so it interleaves with decode; prefixes are cached and reused across
requests; and under disaggregation the KV blocks are pushed over RDMA by a connector (NIXL,
LMCache, Mooncake, FlexKV, AMD's MoRI-IO) from prefill instances to decode instances, orchestrated
by llm-d or Dynamo rather than a hand-rolled proxy. **Central trade-off: TTFT versus ITL.** Every
mechanism that protects decode latency adds a hop or a transfer that the first token pays for. The
scale of that payment is concrete — Llama-3.1-70B in BF16 holds 320 KiB of KV per token, so a
10k-token prompt is about 3 GB, roughly 65 ms at 400 Gb/s before overhead. Tools: vLLM, SGLang,
TensorRT-LLM, `vllm bench serve`.

**BUILDABLE** — Serve one 7B–8B model locally and run a request-rate sweep with `vllm bench serve`
at fixed prompt and output length, measuring TTFT and ITL distributions at each rate. Then fix an
SLO pair — say TTFT ≤ 1 s and p99 ITL ≤ 50 ms — and plot goodput in requests/second meeting both
targets against offered load, for two configurations (single instance versus
`--data-parallel-size 2`). **Measurements:** the goodput knee in req/s; the offered rate at which
p99 ITL crosses 50 ms; the fraction of requests meeting both SLOs — the same quantity the vLLM post
reports as 73/100 versus 30/100. **Hardware: one GPU.**

**VERDICT** — Mechanism: yes, the TTFT-versus-ITL trade and decode's arithmetic intensity explain
every mechanism in the stack. Live research: yes, two September 2026 items, one of which publishes
its own negative result. Buildable: yes. **CHAPTER.** It is the one subject here an engineer can
fully instrument on hardware they already have.

---

## Sampling — read this first

**Budget used.** 11 searches of 25. 16 fetches of 25. Stopped on completeness, not budget: six
complete records with nine searches and nine fetches to spare. No record discarded part-way. Zero
sub-agents.

**What was searched.** Seven queries for recent primary literature: HBM4/roofline/memory-wall
accelerator architecture; prefill–decode disaggregation and goodput; NVFP4/MXFP4 4-bit pretraining;
FP4 inference quantisation with microscaling and rotation; Triton/CUTLASS kernel DSLs and
autotuning on Blackwell; LLM training fault tolerance and silent data corruption; MoE expert
parallelism and MFU. Four for non-paper sources: UALink specification releases; collective-
communication bandwidth and topology studies; speculative decoding and KV-cache serving
measurements; and one follow-up for the UALink press release URL.

**What could not be reached.** `hpcwire.com` and `businesswire.com` both returned HTTP 403, so the
UALink Consortium press release could not be read at source. The consortium's own front page loaded
and carried no technical figures — no signalling rate, no pod size, no latency, no PHY — so the
UALink claim rests on trade-press reporting (Converge Digest, 7 April 2026), labelled `vendor`
because every figure in it originates with the consortium. The OSDI '26 paper arrived as a
compressed PDF the fetcher could not read; its text was extracted locally with `pdftotext`, so
those claims come from the paper's abstract and introduction. NVIDIA's CUTLASS Blackwell page
turned out to be a table of contents, so its date and section structure are known but not the
tile-shape or data-type constraints themselves. Six arXiv abstract pages omitted the hardware, the
baseline tuning, or both; this is said inline rather than filled from memory.

**What the sources over-represent.** Heavily: arXiv preprints from 2026, a sampling frame that
rewards novelty and self-reported wins. **Nine of twelve substantive sources are preprints or
vendor material; exactly one is peer-reviewed (OSDI '26).** Also over-represented: NVIDIA's
ecosystem. CUTLASS, Triton-on-NVIDIA, NVFP4, Blackwell and NCCL dominate; AMD appears only through
two measurements inside the vLLM post; TPUs, Trainium, Cerebras and Groq appear only as entries in
one survey's taxonomy. Nothing from a Chinese-language or Google-internal systems publication, and
nothing from a hardware vendor other than NVIDIA and AMD. US-only web search also shapes this.

**Where a source is selling what it describes.** The NVFP4 pretraining paper is authored entirely
by NVIDIA and validates a format implemented in NVIDIA tensor cores against an NVIDIA FP8 baseline
— marked `vendor`, not `preprint`. The μCUTLASS paper is by NVIDIA researchers promoting a
CUTLASS-backed DSL. The CUTLASS documentation is NVIDIA's own. The UALink material is a consortium
of companies competing with NVLink describing their own specification; no independent measurement
of UALink exists in anything read. The vLLM post is the project's own blog, though unusually
candid: it discloses that its collocated baseline was not the strongest configuration, and
publishes a case where disaggregation lost on TTFT at every rate tested. AMMA, MR-GPTQ, Piper and
H-Spec all propose the thing they measure, so every speedup is self-reported against a baseline
whose tuning is undisclosed.

**Claims resting on training data, not confirmed.** Every entry in all six `FOUNDATIONS` fields.
Specifically: the roofline model (Williams et al., *CACM* 2009); Horowitz's data-movement energy
figures (ISSCC 2014); the TPU paper (Jouppi et al., ISCA 2017); Hennessy and Patterson's "New
Golden Age"; the α–β/Hockney cost model and the ring all-reduce 2(N−1)/N bound (Thakur &
Rabenseifner); mixed-precision training and loss scaling (Micikevicius et al., ICLR 2018) and the
FP8 E4M3/E5M2 pair (2022); the OCP Microscaling specification's 32-element group size; incoherence
processing by Hadamard rotation (QuIP); Halide's algorithm/schedule separation (Ragan-Kelley et al.
2013); Triton's block model (Tillet et al., MAPL 2019); FlashAttention's IO-aware argument (Dao et
al., NeurIPS 2022); ZeRO (SC 2020), Megatron-LM (2019), GPipe and 1F1B; the Young/Daly
optimal-checkpoint-interval result; Orca's iteration-level batching (OSDI 2022); PagedAttention
(SOSP 2023); speculative decoding's exactness guarantee (Leviathan et al., ICML 2023; Chen et al.
2023); and DistServe (OSDI 2024). Also unconfirmed: the tool and framework names in the
`ENGINEERING` fields for which no page was fetched — Nsight Compute, DCGM, NVSHMEM, SHARP, torchao,
llm-compressor, TensorRT Model Optimizer, Megablocks, SGLang, TensorRT-LLM, nccl-tests,
KernelBench.

**Three numbers seen in search snippets and deliberately NOT used**, because they could not be
confirmed in a fetched page: the NVFP4 paper's MXFP4-versus-NVFP4 relative errors (2.5% vs 1.5%)
and its "36% more tokens" equivalence; Piper's absolute figures (trillion-parameter MoE at 20% MFU
on Frontier, X-MoE's 5.23% at 545B); and H-Spec's peak-throughput percentages and 4–25%
KV-utilisation reduction with vLLM concurrency 8–128.

**One date that could not be resolved.** The Triton attention-kernel paper is listed as
arXiv:2511.11581 (implying November 2025) but the fetched abstract page reported a 7 October 2025
submission. Because either date falls just outside the twelve-month window, it was used only in
`FOUNDATIONS`/`CLAIMS` and not as one of a record's two dated items.

**Subjects that belong here and could not be covered within budget.** Two, and they are the two
scope bullets left uncovered.

1. **The economics that drive the engineering** — cost per token as a function of utilisation, the
   capital-versus-operating split, why serving economics push toward disaggregation and
   quantisation, and the depreciation schedule that sets how long a part must earn.
2. **Datacentre constraints, including power** — power delivery and transient response to
   synchronised training load steps, liquid cooling and rack power density, power usage
   effectiveness, and the grid interconnection lead time that bounds how fast capacity can be
   added.

The agent judged these one or two chapters, with an honest risk it did not want to run on a thin
budget: the public sources are dominated by market-research and policy material, and the scope
forbids societal and policy commentary, so doing it properly needs primary engineering sources
(power-delivery papers, Open Compute rack specifications, utility interconnection queue data) it
had no budget left to find. One constraint stated even so: **grid interconnection and water-use
permitting are legal limits on where capacity may be built**, and they bound the engineering
regardless of what the silicon can do.

**A possible seventh subject** rather than a gap in these six: **memory and storage below HBM** —
CXL-attached capacity tiers, KV-cache offload to host DRAM and NVMe, and the data-loading pipeline
that feeds a training run. It appears here only as a fragment.
