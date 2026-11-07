# The check for run g — written 2026-11-07, BEFORE the run's output existed

**Why it is written first.** If I decide what counts as a pass after reading the output, I will find
that the output passes. The floor below is the register's withheld `CARRIES` column plus the two
known losses, fixed before there was anything to grade.

## A. The two known losses — the whole point of the test

| Must come back | Where it sits | Pass condition |
|---|---|---|
| **A refereed alignment track** | The AAAI main technical track call page, named beside the main track | A unit for it exists, sourced to that page, with its sub-topics in `INCLUDES` |
| **The five working groups of the standards subcommittee** | The Wikipedia page quoting the subcommittee's own titles | Five units: foundational standards · data/big data · trustworthiness · use cases and applications · computational approaches. Each with its level given as a working group |

**The run was told to open both pages and was not told either of these is there.** So recovering them
is evidence. Missing them is a failure of reading, not of sampling.

## B. Coverage — every registered source accounted for by name

Nineteen sources in section 1. The run must name each as opened, or not opened with a reason:

arXiv taxonomy · CCS via UCT · CCS via vocabulary server · AAAI main technical track call ·
AAAI keywords · AAAI areas and topics (later cycle) · NeurIPS CFP · ICLR CFP · ICML CFP · ACL CFP ·
CVPR CFP · AAMAS CFP · IJCAI-ECAI via AEPIA · MLCommons benchmarks · MLPerf inference rules ·
LF AI landscape.yml · SC 42 via Wikipedia · AI Engineer fair `llms.md` · AI Engineer fair 2025 page

**Fail if any source is silently absent** — that is the exact failure the register exists to make
visible, and it is invisible in the candidate list itself.

## C. The regression floor, per source (the withheld column)

| Source | Floor |
|---|---|
| arXiv taxonomy | 8 categories of the AI branch |
| CCS via UCT | Both levels; the nodes missing from this rendering named |
| AAAI keywords | 16 areas |
| AAAI areas and topics, later cycle | 17 areas, and **no** tracks beside the main track |
| NeurIPS 2026 | 21 topics |
| ICLR 2026 | 20 topics |
| ICML 2026 | 10 topic areas |
| IJCAI-ECAI via AEPIA | 14 areas |
| MLCommons benchmarks | **12 suites and 9 working groups — the level read in full.** An earlier run took 10 of 12 |
| MLPerf inference rules | 6 datacenter areas, 4 edge areas |
| LF AI landscape.yml | 14 categories |
| SC 42 via Wikipedia | 5 working groups |
| AI Engineer fair 2025 | 18 tracks, and the page's self-contradiction on the count reported |

**Reported below a floor without a stated reason = fail.** Reported above it = normal, no remark
needed; pages change.

## D. Things that must NOT appear

- **Any category from the AI Index report.** It is in "do not read these". Its presence means the
  run ignored section 2.
- **Any search spent on the three unreachable sources.** Section 3 says not to.
- **Any category with no source**, or sourced to something not in the register and not reported as a
  discovery.
- **A filtered list.** No attestation threshold, no tiebreak, no cap, no ordering by count.

## E. Discovery

At most two new sources reported for addition, with kind and level, **reported and not added to the
list.** Zero is an acceptable answer.

## F. How I check it

By reading the output file, line by line, against A to E. Counts are used only to find the text to
read. **Two source pages to be opened directly**: the AAAI main technical track call, and the
Wikipedia page — because A is the whole test and the run's own word on it is not evidence.

---

## AMENDMENT, made before run g's output was in my context

**I opened both pages of section A myself, in the browser, and read them.** Both floors are confirmed
at source, and one of them was too low.

**1. The alignment track is real and the earlier runs recorded it correctly.** The AAAI-26 main
technical track call page states, in its own Summary: *"Three technical tracks (Main Track; AI for
Social Impact; AI Alignment)"*, and its Calls menu lists "Special Track on AI Alignment" and "Special
Track on AI for Social Impact" beside "Main Technical Track". **So this is not a recollection carried
between runs — it is on the page, and a run that opens the page and misses it has misread it.**

**2. The standards page carries eight groups at the working-group level, not five.** The five that
run `d` recorded are exact, word for word:

| | Title, as the page gives it |
|---|---|
| WG 1 | Foundational standards |
| WG 2 | Big Data |
| WG 3 | Trustworthiness |
| WG 4 | Use cases and applications |
| WG 5 | Computational approaches and characteristics of artificial intelligence systems |

**But the same page carries three joint working groups immediately below that table, and run `d`
reported none of them:**

| | Title, as the page gives it |
|---|---|
| JWG 2 | Testing of AI-based systems (with ISO/IEC JTC 1/SC 7) |
| JWG 3 | AI enabled health informatics (with ISO/TC 215) |
| JWG 4 | Functional safety and AI systems (with IEC/TC 65/SC 65A) |

**So run `d` committed the same partial-level read that the brief now forbids**, on the one source it
alone reached. Two of the three — testing of AI-based systems, and functional safety — are the kind
of engineering category the register says this source uniquely carries. **The floor for this source
is therefore raised from 5 to 8**, and the register is corrected.

**What this says about the register, and it is not bad news.** A floor built from what earlier runs
found can be too low, because an earlier run could misread a page. **Floors only ever ratchet
upwards**: each time anybody reads a source properly, the floor rises and stays risen. A floor that
is too low lets a defect through once; it cannot create one. **And it was my own reading of the page
that found this, not a run's self-report** — which is the whole argument for reading the sources by
hand.
