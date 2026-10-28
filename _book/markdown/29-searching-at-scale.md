# Searching at Scale

Chapters 24 to 28 built a retrieval system and never once worried about how long the search
took, because no example in them had more than eight documents in it. This chapter is the bill
for that. What
you get for it is the one arithmetic that makes an approximate index necessary, an honest
account of what the approximation costs and how you would measure it, and the question that
decides more retrieval architectures than any other: who is allowed to see which documents.

*The problem.* Brute force was fine for a hundred documents. At a million it takes four seconds.

*The question.* What do you give up to make search fast, how would you know how much, and what
happens when every user may see only part of the corpus?

## The Arithmetic That Forces the Issue

**Exhaustive search** compares the query against every vector in the collection and sorts. It is
what Chapter 24 did, what Chapter 26's BM25 did, and it has one property that matters here:
**its cost is linear in the number of documents.** Double the corpus and you double the work.
That is not a fixable inefficiency; it follows from comparing against everything.

```python
"""A corpus of vectors, seeded so every run is identical."""
import math
import random

DIM = 8
N = 2000
GROUPS = 20

def direction(group):
    """One direction per group, from a seeded generator rather than a
    formula. A PERIODIC formula is the trap: take sin(group * k + d)
    and any two groups whose k apart is near a multiple of 2*pi come
    out almost parallel - a cosine near 1, which is the opposite of
    what twenty distinct groups needs. Seeding sidesteps it, and the
    lab checks the result rather than trusting it."""
    r = random.Random(1000 + group)
    return [r.uniform(-1, 1) for _ in range(DIM)]

def vector(i):
    """A document is its group's direction plus a small wobble, so the
    corpus really is twenty clusters of a hundred - which is what a
    collection of related documents looks like, and what makes
    grouping worth anything."""
    centre = direction(i // (N // GROUPS))
    wobble = random.Random(50000 + i)
    return [centre[d] + 0.15 * wobble.uniform(-1, 1) for d in range(DIM)]

CORPUS = [vector(i) for i in range(N)]

# Which tenant owns each document. Tenant 0 owns one document in a
# hundred; the rest are spread evenly over tenants 1 to 9.
def owner(i):
    return 0 if i % 100 == 0 else 1 + (i % 9)

OWNERS = [owner(i) for i in range(N)]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

def norm(a):
    return math.sqrt(dot(a, a))

def cosine(a, b):
    return dot(a, b) / (norm(a) * norm(b))

def exact_top(query, k=10, allowed=None):
    """Compare against every vector. The answer everything else is
    measured against, and the thing that gets too slow."""
    pool = range(N) if allowed is None else allowed
    scored = sorted(((cosine(query, CORPUS[i]), i) for i in pool),
                    reverse=True)
    return [i for _, i in scored[:k]], (len(pool) if allowed is None
                                        else len(list(allowed)))

QUERY = vector(734)

if __name__ == "__main__":
    print(f"  {N} vectors of {DIM} dimensions, in 20 groups of 100")
    counts = {}
    for o in OWNERS:
        counts[o] = counts.get(o, 0) + 1
    print(f"  tenant 0 owns {counts[0]} documents "
          f"({100 * counts[0] / N:.0f}% of the corpus)")
    print(f"  tenants 1-9 own {min(counts[t] for t in range(1, 10))}"
          f" to {max(counts[t] for t in range(1, 10))} each\n")
    top, compared = exact_top(QUERY, k=10)
    print(f"  exact top 10: {top[:6]}")
    print(f"                {top[6:]}")
    print(f"  comparisons made: {compared}")
```

```text
  2000 vectors of 8 dimensions, in 20 groups of 100
  tenant 0 owns 20 documents (1% of the corpus)
  tenants 1-9 own 220 to 220 each

  exact top 10: [734, 733, 762, 726, 702, 711]
                [772, 748, 732, 791]
  comparisons made: 2000
```

Two thousand documents, two thousand comparisons. The vectors are made by arithmetic rather than
by a model — Chapter 24's practice, for Chapter 24's reason — and they are *clustered on
purpose*, in twenty groups of a hundred, because a corpus of related documents is clustered and
everything in this chapter depends on that being true of yours.

**Note what the exact answer is for.** Every document in the top ten is between 702 and 791:
one group. That is the answer the rest of the chapter is scored against, and the only reason an
approximation can be measured at all.

## Not Comparing Against Everything

The idea is simple and it is the one every approximate index is built on: **group the vectors
once, then at query time look only in the groups that could plausibly contain the answer.**

```python
"""An approximate index: group the vectors, then search only some groups."""
from corpus import CORPUS, DIM, N, cosine, exact_top, QUERY

def build(nlist=20, rounds=5):
    """Pick nlist starting points spread evenly through the corpus,
    assign every vector to its nearest, recompute the centres, repeat.

    Note the head start, because it matters and the lab checks it: a
    stride of N // nlist over a corpus whose groups are blocks of
    N // nlist drops exactly one starting point in each group. That is
    why this lands on the real groups every time. Seed it at random
    instead and it does not."""
    centroids = [CORPUS[i][:] for i in range(0, N, N // nlist)][:nlist]
    lists = {}
    for _ in range(rounds):
        lists = {c: [] for c in range(nlist)}
        for i, v in enumerate(CORPUS):
            best = max(range(nlist), key=lambda c: cosine(v, centroids[c]))
            lists[best].append(i)
        for c in range(nlist):
            if lists[c]:
                centroids[c] = [sum(CORPUS[i][d] for i in lists[c])
                                / len(lists[c]) for d in range(DIM)]
    return centroids, lists

def search(query, centroids, lists, k=10, nprobe=1):
    """Compare against the centroids, then against only the vectors in
    the nprobe nearest lists."""
    order = sorted(range(len(centroids)),
                   key=lambda c: cosine(query, centroids[c]), reverse=True)
    pool = []
    for c in order[:nprobe]:
        pool += lists[c]
    scored = sorted(((cosine(query, CORPUS[i]), i) for i in pool),
                    reverse=True)
    # The work done is one comparison per centroid plus one per vector
    # in the lists probed.
    return [i for _, i in scored[:k]], len(centroids) + len(pool)

if __name__ == "__main__":
    centroids, lists = build()
    sizes = sorted(len(v) for v in lists.values())
    print(f"  {len(centroids)} lists, holding {sizes[0]} to {sizes[-1]}"
          f" vectors each\n")

    truth, full = exact_top(QUERY, k=10)
    print(f"  exact:  {truth}")
    print(f"          {full} comparisons\n")

    for nprobe in (1, 2, 3):
        got, work = search(QUERY, centroids, lists, k=10, nprobe=nprobe)
        hits = len(set(got) & set(truth))
        print(f"  nprobe {nprobe}: {got}")
        print(f"          {work} comparisons, {hits} of the true 10")
```

```text
  20 lists, holding 100 to 100 vectors each

  exact:  [734, 733, 762, 726, 702, 711, 772, 748, 732, 791]
          2000 comparisons

  nprobe 1: [734, 733, 762, 726, 702, 711, 772, 748, 732, 791]
          120 comparisons, 10 of the true 10
  nprobe 2: [734, 733, 762, 726, 702, 711, 772, 748, 732, 791]
          220 comparisons, 10 of the true 10
  nprobe 3: [734, 733, 762, 726, 702, 711, 772, 748, 732, 791]
          320 comparisons, 10 of the true 10
```

An **approximate nearest neighbour index** — usually shortened to ANN — is any structure that
answers *which vectors are closest* without comparing against all of them, accepting that the
answer may be wrong. This one is the simplest useful kind: a list per group, and a parameter
saying how many groups to look in. Each group it looks in is a **probe**, and that parameter is
the one everything below turns on.

**Read the comparison counts.** 120 against 2000, and the same ten documents. The search did a
seventeenth of the work and lost nothing, which is the result that makes people adopt these
indexes and the result this chapter is about to complicate.

**Two things are worth noticing before it does.**

The work is `nlist + the vectors in the lists probed`, so probing one list of exactly a hundred
costs 20 + 100. **That first term never goes away**, which means probing *every* list costs more
than having no index at all: 20 centroid comparisons plus all 2000 vectors. An index you always
probe exhaustively is strictly worse than brute force.

**And now be careful, because the obvious reading of that is wrong.** The twenty lists hold
exactly a hundred vectors each, and each one holds exactly one of the twenty real groups. It is
tempting to call that a discovery. It is not: `build` starts from one vector every
`N // nlist` — every hundredth — and the real groups are blocks of a hundred, so the
seeding drops *exactly one starting point inside each group*. The clustering was given
the answer and converged to it.

Seed it at random instead and it does not. Over ten random starts the lists come out anywhere
from empty to twice the size, three or four of them straddling two real groups, and not one run
recovers the groups cleanly. **The starting points decide the outcome**, which is a real
property of this kind of clustering rather than a flaw in the program — it is why
implementations run it several times from different starts and keep the best.

So what the twenty tidy lists demonstrate is the *shape* of the index, not the power of the
grouping, and step 2 of the lab has you check both halves.

> **Note:** This is one family of approximate index, chosen because it can be written in thirty
> lines and understood completely. The other family in common use builds a navigable graph over
> the vectors and walks it, which performs differently and has different parameters. The
> *trade* this chapter is about is the same for both and the specific structures are a current
> convention in Chapter 6's sense — do not carry the parameter names anywhere.

## What the Approximation Costs

One query that worked proves nothing, and Chapter 25 is the chapter about why a result that
looks right tells you little. So measure it properly: many queries, scored against the exact
answer.

```python
"""What the approximation costs, measured over many queries."""
from corpus import CORPUS, DIM, N, cosine, exact_top
from ivf import build, search

def queries(n=20):
    """Ten are corpus vectors; ten are the midpoint of two corpus
    vectors, which sometimes lands between two groups and sometimes
    does not. The point is a MIXTURE - a real query log is not twenty
    copies of the easy case."""
    out = []
    for q in range(n):
        if q % 2 == 0:
            out.append(CORPUS[q * 97 % N][:])
        else:
            a, b = CORPUS[q * 97 % N], CORPUS[(q * 97 + 150) % N]
            out.append([(x + y) / 2 for x, y in zip(a, b)])
    return out

if __name__ == "__main__":
    centroids, lists = build()
    qs = queries()
    truth = [exact_top(q, k=10)[0] for q in qs]

    print(f"  {len(qs)} queries: 10 corpus vectors, 10 midpoints\n")
    print("  nprobe   comparisons   recall@10   worst query")
    for nprobe in (1, 2, 3, 5, 10, 20):
        works, recalls = [], []
        for q, t in zip(qs, truth):
            got, work = search(q, centroids, lists, k=10, nprobe=nprobe)
            works.append(work)
            recalls.append(len(set(got) & set(t)) / 10)
        mean_work = sum(works) / len(works)
        mean_rec = sum(recalls) / len(recalls)
        print(f"  {nprobe:6d}   {mean_work:11.1f}   {mean_rec:9.3f}"
              f"   {min(recalls):11.1f}")

    # WHY a query loses, checked rather than assumed: compare each
    # query's losses against whether its true top 10 is spread over
    # more than one of the real groups of a hundred.
    lost, spread = [], []
    for i, (q, t2) in enumerate(zip(qs, truth)):
        r = len(set(search(q, centroids, lists, 10, 1)[0]) & set(t2)) / 10
        groups = {j // 100 for j in t2}
        if r < 1.0:
            lost.append(i)
        if len(groups) > 1:
            spread.append(i)
    print(f"\n  at one probe, {len(lost)} of {len(qs)} queries lost")
    print(f"  something:              {lost}")
    print(f"  top 10 spanning two groups: {spread}")
    print(f"  the same set? {lost == spread}")
    print("  So the rule is exact here: a query loses exactly when its")
    print("  answer was never inside one group, and the mean averages")
    print("  fourteen perfect queries with six partial ones.")
    print()
    print(f"  exhaustive is {N} comparisons and recall 1.000 by")
    print("  definition - it IS the answer everything else is scored")
    print("  against, which is the only reason recall can be measured.")
```

```text
  20 queries: 10 corpus vectors, 10 midpoints

  nprobe   comparisons   recall@10   worst query
       1         120.0       0.925           0.4
       2         220.0       0.995           0.9
       3         320.0       1.000           1.0
       5         520.0       1.000           1.0
      10        1020.0       1.000           1.0
      20        2020.0       1.000           1.0

  at one probe, 6 of 20 queries lost
  something:              [3, 5, 7, 9, 17, 19]
  top 10 spanning two groups: [3, 5, 7, 9, 17, 19]
  the same set? True
  So the rule is exact here: a query loses exactly when its
  answer was never inside one group, and the mean averages
  fourteen perfect queries with six partial ones.

  exhaustive is 2000 comparisons and recall 1.000 by
  definition - it IS the answer everything else is scored
  against, which is the only reason recall can be measured.
```

**This is the table the chapter exists for, and the last column is the one people do not look
at.**

At one probe the mean recall is 0.925, which reads as *tolerable*. The worst query scored
*0.4*: it lost six of its ten true neighbours. And the mean is an average over queries that
were easy and queries that were not — the program counts them: **six of twenty lost something,
and fourteen were perfect.** A mean of 0.925 made of fourteen ones and six partials is a very
different object from twenty queries each losing seven per cent.

**And the program checks why, rather than leaving it to a story.** It computes which queries
lost and, separately, which queries have a true top ten drawn from more than one of the real
groups — and prints whether those are the same set. They are: `[3, 5, 7, 9, 17, 19]` both times.
**A query loses exactly when its answer was never inside one group**, which is the whole
mechanism, and all six are midpoint queries while none of the plain corpus vectors loses
anything.

That is a fact about this corpus and not a law — a messier collection would blur it — but it is
checked here rather than asserted, and it tells you what kind of query to worry about: the ones
whose answer straddles whatever boundaries your clustering drew. Chapter 20 is the
chapter about a number that needs a spread round it before it means anything, and this is a
straightforward instance.

**At two probes the mean is 0.995 and at three it is exact**, for 220 and 320 comparisons
against 2000. That is the shape of the trade on this corpus: a little more work buys back almost
everything, and a little more than that buys back all of it. Where those points sit on *your*
corpus is a measurement, not a default.

Note that two probes do *not* cost twice one probe — 220 against 120, not 240 — because the
twenty centroid comparisons are paid once either way. That is the same term that makes probing
everything worse than brute force, showing up as a small discount instead.

**Now the part that sounds like a paradox and is not.** The way to find out what the
approximation costs is to compare it against the exact answer — which means running the
exhaustive search you installed the index to avoid. That is fine, because you run it **once, on
a sample, offline**, and not on every query. But it has a consequence worth stating plainly:
**an approximate index whose recall you have never measured is a speedup of unknown cost.** You
have traded something for latency and you do not know what.

> **Warning:** Recall here is Chapter 26's measure, computed against the exhaustive answer
> rather than against a human's answer key. Keep the two apart. An index with recall 1.000 is
> returning exactly what brute force would have returned — which may still be the wrong
> documents, because Chapters 24 and 25 are about everything that goes wrong *before* the
> search is approximated. Fixing recall against brute force cannot fix a bad embedding.

## Where the Index Lives

A chapter about scale has to say something about deployment, and this is the shortest useful
version.

| | In your process | A separate service |
|---|---|---|
| Where the vectors are | In memory, beside your code | Over a network call |
| Cost of a search | A function call | A function call plus a round trip |
| Who can use it | One process | Everything, including the next application |
| When the data changes | You rebuild or reload | Not your process's problem, whatever it does about it |
| What happens at restart | Rebuild or reload from disk | Your restart does not touch it |
| What you operate | Nothing extra | Another thing that can be down |

**The honest summary is that this is a deployment decision rather than a retrieval one**, and
the deciding question is usually not speed. It is whether more than one thing needs the same
index, and whether you can afford to rebuild it when your process restarts. The arithmetic is worth doing rather than
taking: a million vectors of 768 dimensions at four bytes a number is
`\(10^{6} \times 768 \times 4 = 3.1\)`{=latex} GB, which fits in a process; a hundred million
is 307 GB, which does not, and that is the point where the decision is made for you.

> **Note:** Products in this area change constantly, so this book names none. What does not
> change is the shape of the table: a network hop, an operational burden and shared access on
> one side, and a function call with nothing to run on the other.

## Who Is Allowed to See What

Now the question that reshapes everything above, and the one most systems meet in their second
month: every user may see only their own documents.

```python
"""Each user sees only their own documents. Where you put that filter
decides whether the search works at all."""
from corpus import CORPUS, N, OWNERS, QUERY, cosine, exact_top
from ivf import build, search

def post_filter(query, centroids, lists, tenant, k=10, fetch=100,
                nprobe=2):
    """Search everything, then throw away what this tenant cannot see."""
    got, work = search(query, centroids, lists, k=fetch, nprobe=nprobe)
    kept = [i for i in got if OWNERS[i] == tenant]
    return kept[:k], work

def pre_filter(query, tenant, k=10):
    """Search only what this tenant can see. Exact, over a small pool."""
    mine = [i for i in range(N) if OWNERS[i] == tenant]
    return exact_top(query, k=k, allowed=mine)

if __name__ == "__main__":
    centroids, lists = build()
    owned = {t: sum(1 for o in OWNERS if o == t) for t in (0, 3)}

    for tenant in (3, 0):
        share = 100 * owned[tenant] / N
        print(f"  tenant {tenant} owns {owned[tenant]} of {N} "
              f"documents ({share:.0f}%)")
        got, work = post_filter(QUERY, centroids, lists, tenant)
        print(f"    post-filter (fetch 100): {len(got)}/10 wanted,"
              f" {work} comparisons")
        exact, ework = pre_filter(QUERY, tenant)
        print(f"    pre-filter (exact):      {len(exact)}/10 wanted,"
              f" {ework} comparisons")
        print()

    print("  Post-filtering returns too few, and how few depends on")
    print("  a number nobody checked: the tenant's share of the")
    print("  corpus. Fetch 100 where a tenant owns 1% and roughly")
    print("  one is theirs - and one came back. One is not ten.")
    print()
    print("  Note what pre-filtering cost: 20 comparisons against")
    print("  220. For a small tenant it is both more correct AND")
    print("  cheaper, because the approximate index is solving a")
    print("  problem that tenant does not have.")
    print()
    print("  And the failure is silent: a short list looks like a")
    print("  tenant with little matching content, which is exactly")
    print("  what it looks like when that is true.")
```

```text
  tenant 3 owns 220 of 2000 documents (11%)
    post-filter (fetch 100): 10/10 wanted, 220 comparisons
    pre-filter (exact):      10/10 wanted, 220 comparisons

  tenant 0 owns 20 of 2000 documents (1%)
    post-filter (fetch 100): 1/10 wanted, 220 comparisons
    pre-filter (exact):      10/10 wanted, 20 comparisons

  Post-filtering returns too few, and how few depends on
  a number nobody checked: the tenant's share of the
  corpus. Fetch 100 where a tenant owns 1% and roughly
  one is theirs - and one came back. One is not ten.

  Note what pre-filtering cost: 20 comparisons against
  220. For a small tenant it is both more correct AND
  cheaper, because the approximate index is solving a
  problem that tenant does not have.

  And the failure is silent: a short list looks like a
  tenant with little matching content, which is exactly
  what it looks like when that is true.
```

A **metadata filter** restricts a search to documents with some property — an owner, a date, a
language, a department. **Multi-tenant retrieval** is the case where that property is who the
documents belong to, and it is the one that breaks things, because the filter is not an
optimisation there. It is a correctness requirement: returning another tenant's document is not
a worse answer, it is a disclosure.

**There are two places to put the filter and they are not equivalent.**

**Post-filtering** searches everything and discards what the user may not see. It is the easy
one to build, because the index needs to know nothing, and the output above is what it does: for
the tenant owning 11% of the corpus it returned all ten, and for the tenant owning 1% it
returned *one*. **The arithmetic is the whole explanation.** Fetch `f` results from a corpus
where a tenant owns a fraction `s` of the documents, and you expect about `f × s` of them to be
theirs. At f = 100 and s = 0.01 that is one, and one is what came back. You asked for ten.

**And nothing reports a failure.** The search ran, the index worked, the filter was correct. A
list of one is indistinguishable from a tenant who genuinely has one relevant document — which
is Chapter 25's invisible miss, arriving through a different door.

**Pre-filtering** restricts the pool before searching, and the second row of each block is the
surprise: for the 1% tenant it was exact *and* cheaper, 20 vector comparisons against 220. The
reason is worth having in words. **An approximate index exists to avoid comparing against a
million vectors. A tenant who owns twenty does not have that problem.**

**One honesty about that 20, because the program hides a cost.** `pre_filter` finds the tenant's
documents with a scan of all two thousand owners, so the path as written still touches every
document — it just does the expensive vector arithmetic on twenty of them. The comparison holds
when you can *list* a tenant's document ids without scanning, which is what an ordinary database
index on a tenant column is for, and which every store you would keep this in already does. The
claim is that twenty vector comparisons beat two hundred, and it needs that one condition
stated. Either way the index is solving a problem that tenant does not have, and paying for it
in both accuracy and work.

**So the shape of the answer to multi-tenancy is a decision about the index itself**, and there
are four arrangements, each with the condition that makes it right:

| Arrangement | Right when |
|---|---|
| **No index at all, exhaustive per tenant** | Every search is confined to one tenant and the biggest tenant is small enough to scan. This is what the program did for tenant 0, and it was exact and cheapest |
| One index per tenant | Tenants are few, and each is large enough that scanning it is too slow |
| One shared index, filter applied during the search | Tenants are many and some are large; needs an index that can restrict as it walks, not after |
| One shared index, post-filter with a large fetch | The smallest tenant's share makes `f × s` comfortably exceed `k`, *and* the search can actually return `f` — see below |

The last is the one to be careful with, because it works in testing — where everyone has a
developer account holding a quarter of the documents — and fails for the real customer with
0.1%. **If you post-filter, the number to write down is the smallest tenant's share**, and the
fetch size follows from it.

**And the fetch has a ceiling you do not set.** An approximate index can only return what it
looked at: at two probes this one examines *200 vectors* — the 220 in the output is the
comparison count, which adds the twenty centroids — so asking it for 500 results yields 200. Raising the fetch therefore means raising the probe count, which is the same as
doing more of the work the index existed to avoid. **Post-filtering is not a knob you can turn
far** — past a point it is exhaustive search with extra steps, and at that point the per-tenant
arrangement in the first row is simply better.

## What To Actually Do

1. **Do not build an index you do not need.** Exhaustive search over ten thousand vectors is
   milliseconds. The arithmetic that forces this chapter starts somewhere around a million, and
   where exactly depends on your dimensions and your latency budget — Chapter 1's latency, as
   the user feels it.
2. **Measure recall before you believe the speedup.** Run exhaustive search once, offline, on a
   sample of real queries, and score the index against it with Chapter 26's recall@k.
3. **Look at the worst query, not the mean.** A mean of 0.925 with a worst of 0.4 is a system
   that fails badly for a minority of questions and reports an average that hides it.
4. **Tune the probe parameter against that measurement**, not against a default. Two probes cost
   less than twice one probe, because the centroid comparisons are paid once, and here they
   bought back almost all the lost recall.
5. **Settle the tenancy question before choosing the index**, because it can make the index
   unnecessary. A per-tenant exhaustive search may be exact, cheaper and simpler.
6. **If you post-filter, write down the smallest tenant's share** and set the fetch from it —
   then check the index can actually return that many, because an approximate search returns at
   most what it examined. Put an alarm on a short result list either way, because the failure is
   otherwise silent.
7. **Decide where the index lives on the operational question**, not the speed one: who else
   needs it, and what happens when your process restarts.

> **Warning:** Steps 2 and 3 are the ones that get skipped, and skipping them is how an
> approximate index becomes a permanent, unexamined loss of quality. The index is fast on the
> first day and nobody measures it again, so the recall it lost is paid every day afterwards by
> whoever asked the question it answered badly.

## Lab: Build One and Break It

Four programs, pure Python, nothing to install. About forty minutes, and there is a key for
every step. Work in a new empty folder.

**Step 1.** Save the first program as `corpus.py` and run it.

*Expected result:* 2000 vectors, tenant 0 owning 1%, and an exact top ten entirely between 702
and 791 — all from the group the query was built from. No clustering has run yet; this is the
corpus construction, and it is what makes the clustering in step 2 possible.

**Step 2.** Save the second as `ivf.py` and run it.

*Expected result:* twenty lists of exactly a hundred, and identical results to exhaustive at
every probe count, for 120 comparisons instead of 2000. Then check the claim the chapter makes
about those lists: add `print({i // 100 for i in lists[c]})` inside the loop and confirm each
list holds exactly one of the twenty real groups.

Then find out *why*, because it is not a discovery. Replace `build`'s seeding with twenty
random indexes — `random.Random(0).sample(range(N), nlist)` — and run it again. The lists come
out anywhere from empty to twice the size, several of them holding two real groups, and the tidy
result is gone. The stride seeding put one starting point inside each group and handed the
clustering its answer.

**Step 3.** Before going on: that looks like a free lunch. What would you need to see before
believing it?

*Expected result:* more than one query. This one sits in the middle of a group, which is the
easy case; the next program is the hard one.

**Step 4.** Save the third program as `tradeoff.py` and run it.

*Expected result:* mean recall 0.925 at one probe rising to 1.000 at three, a worst query of
0.4 at one probe, and `the same set? True` — six queries lost something and the same six have an
answer spanning two groups. Note the last row: twenty probes cost 2020 comparisons against brute
force's 2000.

**Step 5.** In `tradeoff.py`, change `queries` so that *all twenty* sit between two groups —
drop the `if q % 2 == 0` branch and always build the midpoint.

*Expected result:* the mean falls from 0.925 to *0.915* and the number of queries losing
something rises from six to *eight of twenty* — because every query is now the kind that can
straddle a boundary. At two probes the mean is 0.995 with one query still short. **Your measured
recall is a property of the queries you measured it on**, so they had better look like the real
ones.

**Step 6.** In `ivf.py`, change `build` to `nlist=5` and run `tradeoff.py` again.

*Expected result:* five lists, and *not of 400 each* — they come out at 200, 300, 300, 503 and
697, because nothing forces a clustering to divide evenly and five centres cannot split twenty
real groups cleanly. One probe now costs 485 comparisons on average instead of 120.

And the recall gets *worse*, not better: mean 0.885 against 0.925, with a worst query of 0.0.
Four times the work for less accuracy. The reason is the thing step 2 had you check: twenty
lists matched the twenty real groups exactly, so merging them into five forces each probe to
cover several groups at once and to miss several others entirely. **Fewer, bigger lists is not a
safer setting; it is a different one**, and on a corpus whose natural grouping you have already
matched it is strictly worse.

**Step 7.** Save the fourth program as `tenants.py` and run it.

*Expected result:* tenant 3 getting all ten, tenant 0 getting *one*, and pre-filtering beating
post-filtering on both counts for tenant 0 — ten of ten, on twenty comparisons against 220.

**Step 8.** In `tenants.py`, raise `fetch` from 100 to 500 and run it again. Predict the result
first, from the `f × s` arithmetic.

*Expected result:* tenant 0 goes from 1 of 10 to *2 of 10*, on the same 220 comparisons — and
then stops. Try 1000 as well and it is still 2. The arithmetic predicted five at a fetch of 500
and you got two, because `f × s` assumed the search could return 500 results and it cannot: at
two probes it examines *200 vectors*, so it can return at most 200 however much you ask for.
(Note that 200 is the number of *vectors*; the 220 is the comparison count, which adds the
twenty centroids.) **The fetch is capped by the probe.**

That is the sharper version of this section's point. Post-filtering is only tunable up to the
pool, and past that, fetching more means probing more — which means approaching the exhaustive
search the index existed to avoid. The two knobs turn out to be one knob.

**Step 9.** Work out the fetch size that would give tenant 0 ten results on average, then check
whether that is a sensible thing to do.

*Expected result:* about 1000, since `f × 0.01 = 10` — half the corpus, to find ten documents
out of twenty. Check it: at `nprobe=10` the pool is exactly 1000 and holds exactly 10 of tenant
0's documents, which is the arithmetic landing precisely. And ten probes of twenty is half the
exhaustive work. It is not sensible twice over; it is the arithmetic telling you post-filtering
is the wrong arrangement for a tenant this small.

**Step 10.** Write down, for whatever corpus you work with, the smallest tenant's share.

*Expected result:* a number, or the discovery that nobody has it. Either outcome is the point of
the step: by the arithmetic above, that single number decides whether post-filtering can work at
all, and it is the one quantity in this chapter that no program can tell you.

## Summary, Key Terms, and Review Questions

### Summary

**Exhaustive search** compares against every vector, and its cost is linear in the collection —
2000 documents, 2000 comparisons. An **approximate nearest neighbour index** avoids that by
grouping the vectors once and searching only some groups at query time, accepting that the
answer may be wrong. The chapter's index produced twenty lists of exactly a hundred, each
holding exactly one of the twenty real groups — **and not by discovering them**: it starts from
one vector every hundred over groups that are blocks of a hundred, so the seeding puts a point
in each group and hands it the answer. Seed it at random and no run recovers the groups cleanly.
The tidy lists show the index's shape, not the clustering's power. It
answered one query in 120 comparisons against 2000 with the same ten documents. **Two details sit under that.** The work is the number of centroids plus the
vectors in the lists probed, so the centroid term never goes away and probing every list costs
**more** than no index at all — 2020 against 2000. And this is one family of index; the other
common one walks a graph, performs differently, and shares the trade rather than the parameters.

**Measuring the trade is the chapter's point.** Over twenty queries, one probe gave a mean
recall@10 of 0.925 — which reads as tolerable — while the **worst query scored 0.4**, losing six
of its ten true neighbours. **Six of the twenty** lost anything at all, so the mean is fourteen
perfect queries averaged with six partial ones rather than a uniform small loss. And the program
checks *why* instead of telling a story: the queries that lost are exactly the queries whose
true top ten spans more than one real group, printed as `the same set? True`. Two probes brought
the mean to 0.995 and three to exact, for 220 and 320 comparisons — and two probes cost less than
twice one probe, because the centroid comparisons are paid once. The mean hides the failure, which
is Chapter 20's subject arriving in a new place. And the measurement has a shape worth stating:
you score the index against the exhaustive search you installed it to avoid, which is fine
because you run that once, offline, on a sample — but **an index whose recall you have never
measured is a speedup of unknown cost.** Recall here is against brute force, not against
Chapter 24's answer key: an index at recall 1.000 returns exactly what brute force would, which
may still be the wrong documents.

**Where the index lives is a deployment decision, not a retrieval one** — the deciding questions
are whether more than one thing needs it and what happens when your process restarts, not speed.

**And multi-tenancy reshapes all of it.** A **metadata filter** restricts a search by a
property; when that property is ownership, the filter is a correctness requirement rather than
an optimisation, because returning another tenant's document is a disclosure. **Post-filtering**
searches everything and discards: for a tenant owning 11% it returned all ten, and for one
owning 1% it returned one, because fetching `f` results from a tenant holding share `s` yields
about `f × s` of theirs — 100 × 0.01 is one, which is exactly what came back. Nothing reports a failure, and a short list is
indistinguishable from a tenant who genuinely has little. **Pre-filtering** was exact *and*
cheaper for that tenant, 20 comparisons against 220, because an approximate index exists to
avoid comparing against a million vectors and a tenant who owns twenty does not have that
problem. So the arrangement — no index at all with an exhaustive search per tenant, an index
per tenant, a shared index that filters during the search, or a post-filter with a large
fetch — is a decision about the index itself, and if you post-filter, **the number to write down is the smallest tenant's share** — and the fetch cannot
simply be raised to compensate, because an approximate search returns at most what it examined,
so a bigger fetch means more probes and more probes means the exhaustive search the index was
avoiding.

### Key Terms

| Term | Meaning |
|---|---|
| **Exhaustive search** | Comparing the query against every vector. Exact, and linear in the size of the collection |
| **Approximate nearest neighbour index** | A structure that answers which vectors are closest without comparing against all of them, accepting that the answer may be wrong. Shortened to ANN |
| **Probe** | One group the index looks inside at query time. More probes always mean more work, and never less recall — but once recall is exact, further probes buy nothing |
| **Metadata filter** | Restricting a search to documents with some property — an owner, a date, a department |
| **Multi-tenant retrieval** | Retrieval where each user may see only their own documents, so the filter is a correctness requirement rather than an optimisation |
| **Post-filtering** | Searching everything, then discarding what the user may not see. Returns about `f × s` of a tenant's documents from a fetch of `f` at share `s` |
| **Pre-filtering** | Restricting the pool before searching. Exact when the restricted pool is then scanned exhaustively; an index that restricts as it walks is also pre-filtering and is not exact |

### Worth Memorising

| Item | Value or formula |
|---|---|
| Why exhaustive search runs out | Its cost is linear in the collection. Not an inefficiency — it follows from comparing against everything |
| What an ANN index trades | Exactness for work. Call it a speedup whose cost you have measured, or you have not measured it |
| The work a probing index does | Centroids + the vectors in the lists probed. The first term never goes away |
| When an index is worse than none | When you probe every list: 2020 comparisons against brute force's 2000 |
| How recall is measured here | Against the exhaustive answer, once, offline, on a sample. Chapter 26's recall@k, not Chapter 24's answer key |
| The number people do not look at | The worst query. Mean 0.925 with a worst of 0.4 is fourteen perfect queries averaged with six partial ones, not a uniform small loss |
| What post-filtering returns | About `f × s`: fetch `f` from a tenant holding share `s`. 100 × 0.01 ≈ 1, when you asked for 10 |
| Why pre-filtering can be cheaper | An ANN index avoids comparing against a million vectors; a tenant owning twenty has no such problem |
| The number to write down for multi-tenancy | The smallest tenant's share of the corpus |

### Review Questions

1. What does an approximate index buy you, and what does it cost?
2. Each user may see only their own documents. How does that change your retrieval?
3. Your index reports 97 per cent recall. Are you happy?
4. When should you not build an approximate index?
5. How would you measure what your index lost, given that the exact answer is the thing you were trying to avoid computing?

### Review Answers

1. It buys work and it costs exactness, and saying it that way round matters because "it makes
search faster" hides the trade. Exhaustive search compares against every vector, so its cost is
linear in the collection — that is not an inefficiency to optimise away, it follows from
comparing against everything. An approximate index groups the vectors once and looks only in
some groups, so the chapter's index answered in 120 comparisons against 2000. What it costs is
that the answer may be wrong, and the amount is measurable rather than theoretical: over twenty
queries, one probe gave a mean recall of 0.925 and a worst query of 0.4, with six of the twenty
losing something and fourteen perfect. Add the two details
that show you have used one. The work is the centroid comparisons plus the vectors in the lists
probed, so **probing every list is worse than having no index** — 2020 against 2000. And the
loss is not uniform: the queries that suffer are the ones whose answer was never in a single
group, so a mean conceals which questions got badly served.
2. It can change the index itself, which is more than most people expect, and the reason is
arithmetic. The easy arrangement is to search everything and discard what the user may not
see — post-filtering — and it fails quietly for small tenants. Fetch `f` results from a corpus
where a tenant owns share `s` and about `f × s` are theirs: fetch 100 where they own 1% and you
get about one when you asked for ten, and the chapter's run returned exactly one. **Nothing reports an
error**: the search ran, the filter was right, and a list of one looks exactly like a tenant who
genuinely has one relevant document. The alternative is to restrict before searching, and the
surprise is that for a small tenant it was both exact and *cheaper* — 20 comparisons against
220 — because an approximate index exists to avoid comparing against a million vectors and
somebody who owns twenty does not have that problem. So the answer is a choice between an index
per tenant (few, large tenants), one shared index that filters during the search (many small
ones, and it needs an index that can restrict as it walks), and post-filtering with a large
fetch (only when the smallest tenant's share makes `f × s` comfortably exceed `k`, *and* the
search can actually return `f`, which it cannot past the pool it examined). And the arrangement
people forget is no index at all: if every search is confined to one tenant and the biggest
tenant is small, exhaustive per tenant is exact and cheapest, which is what the chapter's own
program did. And add the
last point, because it is the one that bites in production: this is a *correctness* requirement,
not a quality one. Returning another tenant's document is a disclosure, not a worse answer.
3. Not yet, and the follow-up questions are the answer. **Recall against what?** If it is
against the exhaustive search then it means the index returns 97 per cent of what brute force
would, which says nothing about whether brute force was returning the right documents —
Chapters 24 and 25 are about everything that goes wrong before the search is approximated, and
an index at recall 1.000 reproduces those faithfully. **Is 97 the mean, and what is the worst?**
The chapter's own table reads 0.925 mean with a worst query of 0.4, so six queries in twenty
lost something and one of those lost six of its ten results, while the headline looked healthy — and the loss is concentrated rather
than spread: fourteen queries were perfect and six were not, which is a different object from
twenty queries each losing a little. On that corpus the chapter could say exactly which six, by
checking rather than guessing: the ones whose true answer spans more than one of the real
groups. Whether that rule holds on *your* data is itself a thing to check, and the way to check
it is the same exhaustive run. **What was it measured on?** Recall is a property of the queries you measured,
so a sample that does not look like the real traffic gives a number about nothing. **And how
much work did it save?** 97 per cent recall for a tenth of the work is a trade worth making;
97 per cent for a tenth less work is not.
4. When the collection is small enough that exhaustive search is already fast, which is a larger
range than people assume — ten thousand vectors is milliseconds, and the arithmetic only starts
forcing the issue around a million, depending on the dimensions and the latency you can spend.
And when the thing you are searching is naturally small *per query*, which is the multi-tenant
case: if every search is restricted to one tenant's twenty documents, an approximate index over
the whole corpus is solving a problem nobody has, and costing accuracy to do it. The general
form is that an index is worth building when the pool you actually search is large, not when
the corpus is. Add the cost nobody counts: an index is a thing to build, rebuild when the data
changes, reload at restart, and measure — and all of that is permanent, where a slow exhaustive
search is merely slow.
5. By running the exact answer once, offline, on a sample — and the apparent paradox is the
point of the question. You are not avoiding exhaustive search because it is impossible, you are
avoiding it *per query at serving time*. Running it on a few hundred real queries, overnight, is
cheap. Take those queries, compute the true top k by brute force, run the index, and score with
Chapter 26's recall@k. Then three things about how you read it. Report the **worst** query and
not only the mean, because the mean averages over easy queries and the ones the index was always
going to struggle with. Use **real** queries, because recall is a property of what you measured
on. And repeat it when the corpus changes, because the grouping was fitted to the data as it was
— new documents move the centres, and nothing will tell you that the recall you measured in
March no longer holds.

> **You understand this when** you can say why probing every list is worse than having no index,
> and why a tenant who owns twenty documents may be better served by brute force than by the
> index you built for a million.
