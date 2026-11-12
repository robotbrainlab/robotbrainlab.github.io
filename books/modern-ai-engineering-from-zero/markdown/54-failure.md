# Failure: How This Breaks, and How I Diagnose It

Chapter 33 built the two instruments this chapter uses and said plainly that it owned only what
your own records hold. Chapter 1 said providers replace models underneath you and that pinning is
how teams stop it happening silently. Chapter 40 read the model name back out of a reply and
handed over the argument for why that one column matters. This chapter is what those three were
pointing at: the failures that arrive without a change of yours, and what it takes to say which
one you are looking at.

*The problem.* It worked last week. Nothing in my code changed.

*The question.* What changed, and what would have let me say so?

## The Answer, First

**Nothing in your code changed and four other things might have**, and the only one that announces
itself is a snapshot the provider has retired, which arrives as a 404 and is the exception that
proves the rule. The sentence at the top of this chapter is almost always true and almost never relevant,
because a system built on a hosted model has a dependency surface that a system built on a library
does not: the model behind a name, your own documents, the service's behaviour under load, and the
standard you are judging by.

| What moved | What notices it | Whose chapter |
|---|---|---|
| The model behind the name you call | The name read back out of the reply, and your suite | Chapter 40 named the field; this chapter runs the suite |
| Your documents | A key that no longer matches its source, and a retrieval case that stops passing | Chapter 41's check; this chapter's index section |
| The service's behaviour under load | A tail that moved with no change in your request | Chapter 52 |
| Your own standard | A blind re-label of old outputs, counted | Chapter 33's criteria drift |

**And the method is one sentence: hold everything, change one thing, run the suite you already
have, and read the cases that moved.** Every word of that is load-bearing. *Hold everything* is
why the next-but-one section is about versioning four things together rather than one. *The suite
you already have* is why it has to exist before you need it, which is Chapter 33's whole subject.
And *read the cases that moved* is the step this chapter's central measurement exists to argue
for, because a score cannot do it and on real data it did not.

**The thing to be clear about from the start is that a provider's update is a change to your
system that you did not make.** Chapter 51 put it in those words and handed over the mechanics.
It has every property of a change: it can fix things, break things, and do both at once. What it
lacks is the one property your process depends on — you did not choose when it happened. So the
work is to take that choice back where you can, and to notice fast where you cannot.

## What You Can Pin, and What a Floating Name Points At

Chapter 40 ended a step on a single finding: ask for `gpt-4o-mini` and the reply says
`gpt-4o-mini-2024-07-18`, so the provider resolves a moving name to a dated one and tells you
which. It drew the right conclusion — a floating name is dangerous not because you cannot find
out what served you but because the answer can change between two runs and nothing raises — and
left the rest here.

The rest turns out to be three facts, and none of them is what the advice *pin your model version*
assumes.

```python
"""What you can pin, what a floating name points at, and what a
retired snapshot does when you call it.

    python3 names.py

Chapter 40 ended a step on one line: ask for `gpt-4o-mini` and the
reply says `gpt-4o-mini-2024-07-18`, so the provider resolves a moving
name to a dated one and tells you which. It then said pinning makes a
retirement loud - a 404 naming the snapshot - and handed the argument
here. This program checks all of it against the provider as it is
today, because every sentence in it is a sentence about a service that
changes.

Three blocks. The first reads the account's own model listing and
asks, per name group, whether there is a dated snapshot to pin at all.
One limit to carry with that count: `DATED` recognises an ISO date and
nothing else, so a provider's older `-0613` and `-0125` style snapshots
are not seen as dated at all. The unpinnable figure is therefore an
UPPER bound, and the listing holds non-chat names too. The second
asks a handful of floating names for one word and prints what answered
beside the newest dated snapshot of the same name. The third calls a
snapshot the provider has retired.
"""
import json
import os
import re
import urllib.error
import urllib.request

MODELS_URL = "https://api.openai.com/v1/models"
CHAT_URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 60
DATED = re.compile(r"^(.*)-(\d{4}-\d{2}-\d{2})$")

#  The floating names this book has called, or would. One call each,
#  asking for a single word.
PROBE = ("gpt-4o", "gpt-4o-mini", "gpt-4.1", "gpt-4.1-mini",
         "gpt-5", "gpt-5-mini", "gpt-4-turbo")
#  A snapshot that was live when chapters 40 to 42 were written.
RETIRED = "gpt-4o-2024-05-13"
#  The two models chapter 43 embedded a corpus with.
EMBEDDING = ("text-embedding-3-small", "text-embedding-3-large")


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def listing():
    req = urllib.request.Request(
        MODELS_URL, headers={"Authorization": f"Bearer {key()}"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return sorted(m["id"] for m in json.load(r)["data"])


def family(name):
    m = DATED.match(name)
    return (m.group(1), m.group(2)) if m else (name, None)


def say_ready(model):
    """One word back, and the only field that matters is `model`."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with one word: ready"}],
        "max_completion_tokens": 16}).encode()
    req = urllib.request.Request(CHAT_URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return json.load(r)["model"], None
    except urllib.error.HTTPError as exc:
        body = json.loads(exc.read().decode()).get("error", {})
        return None, (exc.code, body.get("code"), body.get("message", ""))


if __name__ == "__main__":
    ids = listing()
    fams = {}
    for name in ids:
        base, date = family(name)
        fams.setdefault(base, set())
        if date:
            fams[base].add(date)

    pinnable = {b: d for b, d in fams.items() if d}
    print(f"  THE ACCOUNT'S LISTING: {len(ids)} names,"
          f" {len(fams)} name groups")
    print(f"    groups with a dated snapshot to pin  "
          f"{len(pinnable):3d}")
    print(f"    groups with none                     "
          f"{len(fams) - len(pinnable):3d}")
    print(f"    so a majority of the GROUPS"
          f" {'can' if len(pinnable) * 2 > len(fams) else 'CANNOT'}"
          f" be pinned - and the")
    print("    second figure is an upper bound, because a `-0613` style")
    print("    snapshot is not read as dated here at all.")

    print("\n    and the two chapter 43 embedded a corpus with:")
    for m in EMBEDDING:
        d = fams.get(m, set())
        print(f"      {m:24s} {len(d)} dated snapshot(s)")

    print("\n  WHAT A FLOATING NAME ANSWERS WITH")
    print("    The two right-hand columns are dates, because the")
    print("    group is the name on the left; a served name from a")
    print("    different group would be printed in full.")
    print("    asked          replied     newest listed")
    lag = answered = refused = unlisted = elsewhere = 0
    for name in PROBE:
        served, err = say_ready(name)
        dates = sorted(fams.get(name, set()))
        newest = f"{name}-{dates[-1]}" if dates else None
        if err:
            refused += 1
            print(f"    {name:14s} HTTP {err[0]} {err[1]}")
            continue
        answered += 1
        base, date = family(served)
        shown = date if base == name else served
        if base != name:
            behind, elsewhere = "  ANOTHER GROUP", elsewhere + 1
        elif not dates:
            behind, unlisted = "  (none listed)", unlisted + 1
        elif served == newest:
            behind = ""
        else:
            behind, lag = "  LAGS", lag + 1
        print(f"    {name:14s} {shown:11s} {dates[-1] if dates else '-':11s}"
              f"{behind}")
    print(f"    of {len(PROBE)} floating names: "
          f"{answered - lag - unlisted - elsewhere} answered with the")
    print(f"    newest snapshot listed beside them, {lag} with an older"
          f" one,")
    print(f"    {unlisted} with none listed at all, {elsewhere} from"
          f" another group,")
    print(f"    and {refused} was refused outright - though"
          f" {sum(1 for x in PROBE if x in ids)} of the {len(PROBE)}")
    print("    are in the listing above.")

    print("\n  AND A SNAPSHOT THE PROVIDER HAS RETIRED")
    print(f"    {RETIRED} is in the listing: {RETIRED in ids}")
    served, err = say_ready(RETIRED)
    if err:
        code, name, msg = err
        print(f"    calling it:  HTTP {code}  {name}")
        print(f"    {msg[:58]}")
        print(f"    {msg[58:116]}")
    else:
        print(f"    calling it:  answered, served {served}")
    print("    So the listing is not a statement of what you can")
    print("    call, and a pre-flight check that reads it would")
    print("    pass a model the chat endpoint refuses.")
```

```text
  THE ACCOUNT'S LISTING: 138 names, 95 name groups
    groups with a dated snapshot to pin   39
    groups with none                      56
    so a majority of the GROUPS CANNOT be pinned - and the
    second figure is an upper bound, because a `-0613` style
    snapshot is not read as dated here at all.

    and the two chapter 43 embedded a corpus with:
      text-embedding-3-small   0 dated snapshot(s)
      text-embedding-3-large   0 dated snapshot(s)

  WHAT A FLOATING NAME ANSWERS WITH
    The two right-hand columns are dates, because the
    group is the name on the left; a served name from a
    different group would be printed in full.
    asked          replied     newest listed
    gpt-4o         2024-08-06  2024-11-20   LAGS
    gpt-4o-mini    2024-07-18  2024-07-18 
    gpt-4.1        2025-04-14  2025-04-14 
    gpt-4.1-mini   2025-04-14  2025-04-14 
    gpt-5          2025-08-07  2025-08-07 
    gpt-5-mini     2025-08-07  2025-08-07 
    gpt-4-turbo    HTTP 404 model_not_found
    of 7 floating names: 5 answered with the
    newest snapshot listed beside them, 1 with an older one,
    0 with none listed at all, 0 from another group,
    and 1 was refused outright - though 7 of the 7
    are in the listing above.

  AND A SNAPSHOT THE PROVIDER HAS RETIRED
    gpt-4o-2024-05-13 is in the listing: True
    calling it:  HTTP 404  model_not_found
    The model `gpt-4o-2024-05-13` has been deprecated, learn m
    ore here: https://platform.openai.com/docs/deprecations
    So the listing is not a statement of what you can
    call, and a pre-flight check that reads it would
    pass a model the chat endpoint refuses.
```

**First: much of what you can call cannot be pinned.** Group the hundred and thirty-eight names in
this account's listing by what precedes a date, and thirty-nine of the ninety-five groups have at
least one dated snapshot while fifty-six have none. **That second figure is an upper bound and the
program says so**: it recognises an ISO date and nothing else, so a provider's older
`gpt-4-0613`-style snapshots are not read as dated at all, and the listing holds names you would
never send a prompt to. What survives the caveat is that *pin the dated name* is advice with a
large exception, and the exception that matters most for this book is the embedding models:
Chapter 43 embedded a corpus with `text-embedding-3-small` and `text-embedding-3-large`, said in
its own program that the name you ask for is all there is, and pointed here. It is all there is.
Zero dated snapshots each.

**Second: a floating name is not the newest.** `gpt-4o` answers with `gpt-4o-2024-08-06` while
`gpt-4o-2024-11-20` sits in the same listing. Of seven floating names probed, five resolved to the
newest dated snapshot beside them, one resolved to an older one, and one was refused outright. So
the floating name is not *the latest model* and it is not *a fixed model* either; it is a pointer
the provider moves on its own schedule, and the only way to know where it points today is to ask
and read the answer. Seven names is not a survey, and what it establishes is enough: the mental
model in which a family name tracks the newest release is wrong for two of the seven in two
different ways.

**Third: the listing is not a statement of what you can call.** `gpt-4o-2024-05-13` is in it, and
calling it returns HTTP 404 with `model_not_found` and a message naming the snapshot and pointing
at a deprecations page. `gpt-4-turbo` — a *floating* name, not a dated one — does the same. All
seven probed names are in the listing, which the program checks rather than asserts. **So a pre-flight check that reads the model list would pass a model the chat endpoint
refuses**, which is worth knowing before you write one, and the check that works is the one
Chapter 40 already gave: send a request and read what comes back.

**And the 404 is the argument for pinning, arriving as evidence.** Chapter 40 predicted it: pinning
makes a retirement loud, immediate, specific and timed by you rather than by a score that moved.
Here it is, on a snapshot that was live when Chapters 40 to 42 were written and is gone now. A team
on `gpt-4o-2024-05-13` got a 404 naming the thing to fix. A team on `gpt-4o` got a different model
and no message at all.

## A Gated Upgrade

Chapter 39 named the instrument. Its *evaluation gate* is the rule a tune has to pass before it
is released, and it has two conditions: the target set moved *and* nothing else did. That chapter
is about a change you made.

A **gated upgrade** is the same instrument pointed at a change you did not make: a provider's new
snapshot does not serve your traffic until it has passed the gate your own changes pass. Nothing
about the gate is new. What is new is everything around it.

- **The input is not yours.** You did not choose the snapshot, its contents or its timing, so the
  gate has to be runnable on demand rather than as a step in your release process.
- **There is a deadline.** The old snapshot is retired on the provider's schedule, which is the
  404 from the previous section. So *do nothing* is not available indefinitely, and the thing to
  find out early is the date.
- **And the gate's second condition is the one that fires.** Chapter 39 says the condition that
  gets dropped is *nothing else moved*. For a provider's update there is no first condition at
  all: no target set moved, because you were not trying to move anything. A gated upgrade is
  Chapter 39's second condition standing on its own.

That last point decides the shape of the work. You are not looking for an improvement. You are
looking for anything that moved in a system where you changed nothing — and the next section is
what that looks like on real traffic.

## A Provider's Update, Run Today

**You do not have to wait for a provider to update anything to measure what an update does**, and
this is the part of the chapter to take to work. The provider has already done it: `gpt-4o` has had
three dated snapshots, two of them still answer, and a team on the floating name took whichever one
it was pointed at without choosing any of them. So hold the prompt, the cases, the grader and the
temperature fixed, change only the snapshot, and count what moves.

The cases and the grader are Chapter 41's, unchanged — its thirty cases and its `normalised`
grader. That matters more than it looks. **A regression set you change while measuring a change
measures nothing**, and the temptation to improve the grader is strongest at exactly the moment you
are about to find something out with it.

```python
"""The same thirty cases against two dated snapshots of one model.

    python3 drift.py

This is the chapter's central measurement and it needs no provider to
update anything, because the provider has already done it twice and
left both of the resulting snapshots callable. `gpt-4o` has had three dated
snapshots - 2024-05-13, 2024-08-06 and 2024-11-20 - and a team on the
floating name took whichever one the provider pointed it at. Two of the
three still answer; `names.py` is where the first one returns a 404. So:
hold the prompt, the cases, the grader and the temperature fixed, change
only the snapshot, and count what moves.

The cases and the grader are chapter 41's, unchanged - `cases.tsv`
and its `normalised` grader, which that chapter is careful to say is
not a neutral instrument. Prompt B is the one the grader is fairest
to, and it is held fixed here because the arm design has one variable.

180 calls. The result is written to `drift.json` and this program
loads it if it is there, so the report below can be re-read for
nothing. Delete the file to measure again.
"""
import json
import os
import pathlib
import random
import re
import statistics as st
import sys
import time
import urllib.request

URL = "https://api.openai.com/v1/chat/completions"
TIMEOUT = 180
#  Dated snapshots of ONE name, in the order the provider released
#  them. Nothing else about the request changes.
#  Two of the three it has had: `gpt-4o-2024-05-13` was the first and the
#  provider has retired it, which `names.py` shows as a 404 naming the
#  snapshot. So the suite can be run across the two that are left, and
#  the third release is a measurement nobody can take any more - which
#  is its own lesson and the reason this program dates its output.
SNAPSHOTS = ("gpt-4o-2024-08-06", "gpt-4o-2024-11-20")
TRIALS = 3
CACHE = pathlib.Path("drift.json")
CORPUS = pathlib.Path(os.environ.get("CORPUS", "corpus")) / "docs"
PRICE = {"in": 2.500, "out": 10.000}      # per million, read 2026-10-30

#  Chapter 41's prompt B, verbatim.
PROMPT = ("Answer the question using only the document below.\n"
          "Reply with the value only: no sentence, no explanation, and no "
          "units unless the question asks for them.\n\n"
          "Document:\n{doc}\n\nQuestion: {q}")

#  Chapter 41's `normalised` grader and its unit list, verbatim. That
#  chapter owns the exact-match grader and answer normalisation, and
#  owns the finding that a grader written to be fair to one prompt
#  forgives the only instruction the other broke. Nothing here is a
#  better grader; it is the SAME grader, which is the point - a
#  regression set you change while measuring a change measures
#  nothing.
UNITS = ("pounds", "pound", "days", "day", "hours", "hour", "years", "year",
         "litres", "litre", "watts", "watt", "millimetres", "mm",
         "centimetres", "cm", "kilograms", "kg", "units", "working days")


def _norm(s):
    s = s.lower().strip()
    s = s.replace("*", "").replace("`", "")
    s = re.sub(r"^(the answer is|it is|answer:)\s*", "", s)
    s = s.strip(" .,:;!?\"'")
    for u in sorted(UNITS, key=len, reverse=True):
        if s.endswith(" " + u):
            s = s[: -len(u) - 1].strip()
    return s.strip(" .,")


def normalised(reply, answer):
    return _norm(reply) == _norm(answer)


def cases(path="cases.tsv"):
    rows = pathlib.Path(path).read_text().strip().split("\n")[1:]
    return [tuple(r.split("\t")) for r in rows]


def ask(snapshot, question, doc_id, max_tokens=60):
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    doc = (CORPUS / f"{doc_id}.md").read_text()
    body = json.dumps({
        "model": snapshot,
        "messages": [{"role": "user",
                      "content": PROMPT.format(doc=doc, q=question)}],
        "max_tokens": max_tokens, "temperature": 0,
    }).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {k}",
        "Content-Type": "application/json"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                d = json.load(r)
            break
        except Exception as exc:          # noqa: BLE001 - chapter 19
            if attempt == 3:
                raise
            print(f"      retry {attempt + 1}: {type(exc).__name__}",
                  file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return {"reply": d["choices"][0]["message"]["content"].strip(),
            #  Chapter 40's one line: read the name back. Asking for a
            #  dated snapshot should return it, and the whole argument
            #  for pinning is that this can be checked.
            "served": d["model"],
            "in_tokens": d["usage"]["prompt_tokens"],
            "out_tokens": d["usage"]["completion_tokens"]}


def measure():
    cs = cases()
    rows, seq = [], 0
    total = len(cs) * len(SNAPSHOTS) * TRIALS
    print(f"  {len(cs)} cases x {len(SNAPSHOTS)} snapshots x {TRIALS}"
          f" trials = {total} calls", file=sys.stderr)
    for cid, q, doc, want in cs:
        for trial in range(1, TRIALS + 1):
            for snap in SNAPSHOTS:      # interleaved: chapter 49
                r = ask(snap, q, doc)
                seq += 1
                r.update(case=cid, question=q, doc=doc, answer=want,
                         snapshot=snap, trial=trial, seq=seq,
                         right=normalised(r["reply"], want))
                rows.append(r)
        print(f"    {seq:>3}/{total}  {cid}", file=sys.stderr)
    CACHE.write_text(json.dumps(rows, indent=1))
    return rows


def boot(stat, units, rounds=10000, seed=0):
    """Chapter 20's bootstrap over the CASES, which is what makes the
    comparison below paired: every case ran on both snapshots."""
    rng = random.Random(seed)
    out = [stat([rng.choice(units) for _ in units]) for _ in range(rounds)]
    out.sort()
    return out[int(0.025 * rounds)], out[int(0.975 * rounds)]


def verdict(rows):
    """Chapter 33's rule for a per-case verdict from repeats: a case
    counts as passing when it passes MORE often than it fails. With
    three trials that is two of three, and the cases near fifty-fifty
    are the finding rather than the noise."""
    return sum(1 for r in rows if r["right"]) * 2 > len(rows)


if __name__ == "__main__":
    rows = json.loads(CACHE.read_text()) if CACHE.exists() else measure()

    print("  WHAT CAME BACK WHEN THE NAME WAS READ BACK")
    for snap in SNAPSHOTS:
        served = {r["served"] for r in rows if r["snapshot"] == snap}
        print(f"    asked {snap}")
        print(f"      replied {', '.join(sorted(served))}")

    by = {}
    for r in rows:
        by.setdefault((r["case"], r["snapshot"]), []).append(r)
    cs = sorted({r["case"] for r in rows})
    V = {(c, s): verdict(by[(c, s)]) for c in cs for s in SNAPSHOTS}

    #  Chapter 33 measured three repeats and found them too few where
    #  cases are flaky, so the first thing to report is whether any
    #  case here was flaky at all.
    pairs = [(c, s) for c in cs for s in SNAPSHOTS]
    una = sum(1 for k in pairs if len({r["right"] for r in by[k]}) == 1)
    print(f"\n  WHETHER THE REPEAT COUNT MATTERED")
    print(f"    unanimous case-and-snapshot pairs  {una} of {len(pairs)}")
    for k in pairs:
        if len({r["right"] for r in by[k]}) != 1:
            got = [(r["reply"], r["right"]) for r in by[k]]
            print(f"    the one split: {k[0]} on {k[1][-10:]}")
            print(f"      {got}")

    print(f"\n  THE SAME SUITE, {len(SNAPSHOTS)} SNAPSHOTS,"
          f" {len(cs)} CASES")
    print("    snapshot            pass   of   score")
    for snap in SNAPSHOTS:
        n = sum(1 for c in cs if V[(c, snap)])
        print(f"    {snap}   {n:3d}  {len(cs):3d}   {n / len(cs):.3f}")

    print("\n  AND WHICH CASES MOVED, SNAPSHOT TO SNAPSHOT")
    for a, b in zip(SNAPSHOTS, SNAPSHOTS[1:]):
        gained = [c for c in cs if V[(c, b)] and not V[(c, a)]]
        lost = [c for c in cs if V[(c, a)] and not V[(c, b)]]
        print(f"    {a[-10:]} -> {b[-10:]}"
              f"   {len(lost)} lost, {len(gained)} gained")
        for c in lost:
            print(f"      LOST   {c}")
        for c in gained:
            print(f"      gained {c}")
    first, last = SNAPSHOTS[0], SNAPSHOTS[-1]
    moved = [c for c in cs if V[(c, first)] != V[(c, last)]]
    ever = [c for c in cs
            if len({V[(c, s)] for s in SNAPSHOTS}) > 1]
    print(f"    first to last: {len(moved)} of {len(cs)} cases differ")
    print(f"    moved at any step: {len(ever)} of {len(cs)}")

    print("\n  THE SCORE DIFFERENCE, CHAPTER 20'S WAY")
    for a, b in zip(SNAPSHOTS, SNAPSHOTS[1:]):
        def gap(sample, a=a, b=b):
            return (sum(1 for c in sample if V[(c, b)])
                    - sum(1 for c in sample if V[(c, a)])) / len(sample)
        d = gap(cs)
        lo, hi = boot(gap, cs)
        tell = "cannot tell" if lo <= 0 <= hi else "clears zero"
        print(f"    {a[-10:]}->{b[-10:]} {d:+.3f}"
              f" {lo:+.3f} to {hi:+.3f} {tell}")

    #  Every failure on both snapshots, not only the ones that moved -
    #  because a regression is a DIFFERENCE and the chapter cannot say
    #  what changed without knowing what the other arm was already
    #  getting wrong.
    print("\n  EVERY FAILING CASE, BOTH SNAPSHOTS")
    for snap in SNAPSHOTS:
        bad = [c for c in cs if not V[(c, snap)]]
        print(f"    {snap}  {len(bad)} failing")
        for c in bad:
            rs = by[(c, snap)]
            seen = sorted({r["reply"] for r in rs})
            print(f"      {c}  key {rs[0]['answer']!r:9s} -> "
                  f"{', '.join(repr(x) for x in seen)[:34]}")

    #  Then the cases that moved, read rather than counted - which is
    #  chapter 30's method and the step that makes a verdict an
    #  attribution. Every trial of each is printed, because a case near
    #  fifty-fifty would look like a regression and be the dice.
    print("\n  THE CASES THAT MOVED, READ")
    for c in [x for x in cs if V[(x, SNAPSHOTS[0])]
              and not V[(x, SNAPSHOTS[-1])]]:
        want = by[(c, SNAPSHOTS[0])][0]["answer"]
        print(f"    {c}  wanted {want!r}")
        print(f"      {by[(c, SNAPSHOTS[0])][0]['question'][:52]}")
        for s in SNAPSHOTS:
            got = [r["reply"] for r in by[(c, s)]]
            marks = "".join("y" if r["right"] else "-"
                            for r in by[(c, s)])
            print(f"      {s[-10:]} {marks}  {got[0][:34]!r}")
            if len(set(got)) > 1:
                print(f"        and {len(set(got))} distinct replies"
                      f" in {len(got)} trials")

    #  A diagnostic, not a better grader, and it is fitted to the
    #  failures it then scores: WORDS and SYMBOLS below were written
    #  after reading the three cases above. So this cannot be evidence
    #  that the answers are right - that is what reading the printed
    #  replies is for. Chapter 50 names the general form: when a check
    #  and the thing it is measured against are the same predicate,
    #  the figure is a definition and could not have come out any
    #  other way. What this DOES establish is the weaker and useful
    #  thing: that notation is SUFFICIENT to explain every rejection,
    #  with nothing left over needing another explanation.
    #  Chapter 41 owns the grader and owns the finding that it is not a
    #  neutral instrument.
    WORDS = {"one": "1", "two": "2", "three": "3", "four": "4",
             "five": "5", "six": "6", "seven": "7", "eight": "8",
             "nine": "9", "ten": "10", "ninety": "90"}
    SYMBOLS = ("w", "kg", "mm", "cm", "l", "g")

    def lenient(reply, answer):
        a_, b_ = _norm(reply), _norm(answer)
        for s in sorted(SYMBOLS, key=len, reverse=True):
            if a_.endswith(" " + s):
                a_ = a_[: -len(s) - 1].strip()
        return WORDS.get(a_, a_) == WORDS.get(b_, b_)

    print("\n  A DIAGNOSTIC: THE SAME THREE, NOTATION ACCEPTED")
    L = {(c, s): sum(1 for r in by[(c, s)]
                     if lenient(r["reply"], r["answer"])) * 2
         > len(by[(c, s)]) for c in cs for s in SNAPSHOTS}
    lost_strict = [c for c in cs if V[(c, SNAPSHOTS[0])]
                   and not V[(c, SNAPSHOTS[-1])]]
    lost_lenient = [c for c in lost_strict
                    if L[(c, SNAPSHOTS[0])] and not L[(c, SNAPSHOTS[-1])]]
    print(f"    regressions under the suite's own grader  "
          f"{len(lost_strict)}")
    print(f"    regressions once notation is accepted     "
          f"{len(lost_lenient)}")
    for snap in SNAPSHOTS:
        n = sum(1 for c in cs if L[(c, snap)])
        print(f"    {snap[-10:]} scores {n} of {len(cs)} this way")
    print("    Notation explains every rejection with nothing left")
    print("    over. The grader is fitted to these failures, so the")
    print("    30s are not a quality claim; the evidence that the")
    print("    answers are right is the three replies printed above,")
    print("    read by a person. Which is the step the suite cannot")
    print("    do and the reason a moved verdict is the start of an")
    print("    attribution rather than the end of one.")

    print("\n  AND THE REPLIES THAT MOVED WITHOUT MOVING A VERDICT")
    moved_text = 0
    for c in cs:
        per = {s: {r["reply"] for r in by[(c, s)]} for s in SNAPSHOTS}
        settled = all(len(x) == 1 for x in per.values())
        if settled and len({next(iter(x)) for x in per.values()}) > 1 \
                and len({V[(c, s)] for s in SNAPSHOTS}) == 1:
            moved_text += 1
    print(f"    {moved_text} of {len(cs)} cases answered differently on")
    print(f"    the {len(SNAPSHOTS)} snapshots, settled within each one,")
    print("    and were graded the same either way")

    money = sum((r["in_tokens"] * PRICE["in"]
                 + r["out_tokens"] * PRICE["out"]) / 1e6 for r in rows)
    print(f"\n  THIS MEASUREMENT: {len(rows)} calls, ${money:.4f}")
```

```text
  WHAT CAME BACK WHEN THE NAME WAS READ BACK
    asked gpt-4o-2024-08-06
      replied gpt-4o-2024-08-06
    asked gpt-4o-2024-11-20
      replied gpt-4o-2024-11-20

  WHETHER THE REPEAT COUNT MATTERED
    unanimous case-and-snapshot pairs  59 of 60
    the one split: c30 on 2024-08-06
      [('ten', True), ('10', False), ('10', False)]

  THE SAME SUITE, 2 SNAPSHOTS, 30 CASES
    snapshot            pass   of   score
    gpt-4o-2024-08-06    25   30   0.833
    gpt-4o-2024-11-20    22   30   0.733

  AND WHICH CASES MOVED, SNAPSHOT TO SNAPSHOT
    2024-08-06 -> 2024-11-20   3 lost, 0 gained
      LOST   c20
      LOST   c25
      LOST   c29
    first to last: 3 of 30 cases differ
    moved at any step: 3 of 30

  THE SCORE DIFFERENCE, CHAPTER 20'S WAY
    2024-08-06->2024-11-20 -0.100 -0.200 to +0.000 cannot tell

  EVERY FAILING CASE, BOTH SNAPSHOTS
    gpt-4o-2024-08-06  5 failing
      c13  key 'two'     -> '2'
      c14  key 'ninety'  -> '90'
      c15  key 'ninety'  -> '90'
      c28  key 'ten'     -> '10'
      c30  key 'ten'     -> '10', 'ten'
    gpt-4o-2024-11-20  8 failing
      c13  key 'two'     -> '2'
      c14  key 'ninety'  -> '90', '90 days'
      c15  key 'ninety'  -> '90 days'
      c20  key 'three'   -> '3 years'
      c25  key '60'      -> '60 W'
      c28  key 'ten'     -> '10'
      c29  key 'seven'   -> '7'
      c30  key 'ten'     -> '10'

  THE CASES THAT MOVED, READ
    c20  wanted 'three'
      How many years of warranty does Harbour Plus give?
      2024-08-06 yyy  'Three years'
      2024-11-20 ---  '3 years'
    c25  wanted '60'
      What is the maximum bulb wattage for the HL-3310 lam
      2024-08-06 yyy  '60'
      2024-11-20 ---  '60 W'
    c29  wanted 'seven'
      For how many years are order records kept?
      2024-08-06 yyy  'Seven'
      2024-11-20 ---  '7'

  A DIAGNOSTIC: THE SAME THREE, NOTATION ACCEPTED
    regressions under the suite's own grader  3
    regressions once notation is accepted     0
    2024-08-06 scores 30 of 30 this way
    2024-11-20 scores 30 of 30 this way
    Notation explains every rejection with nothing left
    over. The grader is fitted to these failures, so the
    30s are not a quality claim; the evidence that the
    answers are right is the three replies printed above,
    read by a person. Which is the step the suite cannot
    do and the reason a moved verdict is the start of an
    attribution rather than the end of one.

  AND THE REPLIES THAT MOVED WITHOUT MOVING A VERDICT
    2 of 30 cases answered differently on
    the 2 snapshots, settled within each one,
    and were graded the same either way

  THIS MEASUREMENT: 180 calls, $0.1836
```

**Three cases of thirty moved, all in the same direction, and the score cannot be told from zero.**
Twenty-five of thirty passed on the older snapshot and twenty-two on the newer; the paired
difference is −0.100 with 95 per cent from −0.200 to +0.000, which contains zero at thirty cases.
Chapter 20 owns that test and its verdict here is *cannot tell*.

**And three repeats is the count Chapter 33 showed is not enough**, where cases are flaky: with the
majority rule applied properly, three leaves 7 of 10 subsets reporting a regression that is not
there. Here it did not have to be enough, which the first block of the output says — **fifty-nine of
the sixty case-and-snapshot pairs are unanimous**, and all three that moved went three-nil to
nil-three. The one split is `c30` on the older snapshot, which answered `ten` once and `10` twice, so
the majority rule put it on the failing side; it is also one of the five notation cases below. A
result that survives its repeat count is worth saying so about, because the alternative is a chapter
resting on a configuration its own source chapter calls inadequate.

**So read the two blocks against each other, because they say different things and both are
right.** The score says there is nothing you can establish. The case list says `c20`, `c25` and
`c29` passed on one snapshot and fail on the other with nothing else in the request different.
Chapter 33's step 5 is the resolution and it is not a close call: *report regressions as a list of
cases, never as a score movement — the score is a net and hides the trade.* Here the net is not
hiding a trade. It is hiding three named facts behind an interval that is honest about the aggregate
and silent about them.

**And then the step that turns a verdict into an attribution.** Chapter 30's method is to read the
cases, and reading these three is the whole lesson of the chapter:

| Case | Wanted | The older snapshot | The newer one |
|---|---|---|---|
| c20 | `three` | `Three years` | `3 years` |
| c25 | `60` | `60` | `60 W` |
| c29 | `seven` | `Seven` | `7` |

**Every one of the newer model's three answers is correct.** Three years is three years, the maximum
wattage is sixty watts, and the records are kept for seven years.

**And the block above it is the one that says what actually changed**, because a regression is a
difference and you cannot name it without knowing what the other arm was already getting wrong. The
older snapshot fails five cases, and **all five of those are correct answers too**: `2` where the key
says `two`, `90` for `ninety` twice, `10` for `ten` twice. So the older snapshot was already
answering word-keyed questions in digits on five cases of its own. What the newer one changed is how
far that reaches — two more word-keyed questions, `c20` and `c29` — and one new thing, the bare
symbol `W` on `c25`, where the grader's unit list knows only `watts` and `watt`. Three added
failures: two of the old kind and one of a new one.

**So the baseline itself is a grader artefact, all of it.** Twenty-five of thirty is not twenty-five
right answers and five wrong ones; it is thirty right answers and five notations the grader does not
accept. Chapter 41's finding arrives with nothing added — *a grader is not a neutral instrument*, and
the one written to be fair to one prompt forgives the only instruction the other broke — except that
this time the thing it was not written to be fair to is a model nobody chose.

**The diagnostic puts a number on it and is careful which number.** Accept the other notation and
both snapshots score thirty of thirty, so notation explains every rejection with nothing left over.
That is the claim, and the first thing to say is what it rests on: the lenient grader was written
*after* reading the three cases that moved, so it is fitted to those and cannot be evidence that
their answers are right. **What it was not fitted to is the other five**, and its word-to-digit
table covers them too — which is support from outside the cases it was built for rather than a
circle.
Chapter 50 named the general form of that trap — when a check and the thing it is measured against
are the same predicate, the figure is a definition and could not have come out any other way — and a
grader fitted to the failures it then scores is a mild case of it. The evidence that the answers are
right is the three replies in the table above, read by a person. **Which is exactly the step a
suite cannot take, and the reason a moved verdict is the beginning of an attribution and not the end
of one.**

## What the Suite Got Right, and What It Got Wrong

Separating these matters, because the conclusion to reach for after a result like that is *the suite
is useless* and the opposite is true.

**What it got right is the only thing it was asked to do.** Something changed in a system where
nothing was changed, and the suite said so by name, for 180 calls and eighteen cents. **No score
would have.** This one's interval contains zero, and a dashboard of averages is a score with a
graph round it. A person using the product would not have noticed `3 years` where the key says
`three`, and would have been right not to. What would have found it is somebody reading output,
which is Chapter 30's method and costs an afternoon rather than three minutes — so the suite's
contribution is not that it alone could see this, but that it saw it by name, unprompted, on a
schedule.

**What it got wrong is the word *regression*.** Three cases went from pass to fail and the system's
answers got no worse. A suite's verdict is therefore a claim about the model and the grader
*together*, and when it fires you do not yet know which of the two moved. That is not a defect to be
repaired with a better grader — Chapter 31 is clear that a check is only as right as whoever wrote
it, and Chapter 41 measured what a grader forgives. It is a property of the instrument, and the
practice that follows is one line: **a moved case is read before it is acted on.**

**And two of the thirty answered differently on the two snapshots and were graded the same either
way** — settled within each snapshot, different between them. Those are the cases that say the model
moved and your grader happens not to care, and they appear in no count of verdicts at all. If your
trace keeps the replies you have them; if it keeps only the verdict you do not. That is Chapter 33's
content decision arriving as a diagnostic question rather than as a privacy one.

## Versioning the Whole Thing as One Artefact

The measurement above was attributable for one reason: the only thing that differed between the two
arms was the snapshot. In production that is the condition you have to arrange in advance, and it is
the condition almost nobody has.

Four things decide what your system answers, and all four move:

| What | How it moves | What happens if it moves alone |
|---|---|---|
| The prompt | Somebody edits it | The suite's verdicts move and the trace does not say why |
| The configuration | A model name, a temperature, a retrieval depth, a token cap | The same, and the edit is often in a different repository |
| The index | Documents are added, edited or re-embedded | Retrieval cases move and the answers follow |
| The model | The provider's schedule, or a floating name repointed | Section two of this chapter |

**Chapter 33's trace carries exactly one of the four.** Its field list holds `model`, and that
chapter's own step 10 is the discovery: add the question *which version of the prompt produced this?*
and no field in the list answers it, which is how you find the field you forgot. It then says this
chapter treats the four as one versioned artefact, so here is what that means.

A **versioned artefact** is the prompt, the configuration, the index and the model version released
and recorded together under one identifier. Not four histories you can join on a timestamp — one id,
written into every trace, that resolves to all four. The reason is not tidiness. It is that a failure
you cannot attribute is a failure you cannot fix, and *joining on a timestamp* fails in the two cases
that matter most: a change that was rolled out gradually, so two requests a second apart ran
different versions, and a change to the index, which has no release event at all.

**The index is the one that breaks the discipline**, and it breaks it quietly. A prompt edit is a
commit. An index that gained forty documents overnight is not a commit anywhere, and Chapter 41's
check is the cheapest thing that notices: it asserts that every expected answer still appears in the
document it was drawn from, and the moment somebody edits a document it turns a silently wrong key
into a failed run. Chapter 33 names the same hazard from the other side — a trace that stores a
passage *id* and not its text cannot show you what was sent once the documents change under you.

So the minimum is three things written down together: the model snapshot, a hash or revision of the
prompt and configuration, and a revision of the index. Three strings on every trace, and the question
*what was serving when this failed* has an answer instead of an investigation.

## Re-embedding, and the Index Half Migrated

The index's own version changes for an ordinary reason that turns out not to be ordinary at all:
the embedding model moved.

Chapter 43 embedded this book's corpus with two models and said in its own program that neither has a
dated snapshot to pin, so the name you ask for is all there is and a name that starts serving
something else is this chapter's subject with nothing in between. The section above confirmed it —
zero dated snapshots for either. So the case is live, and so is the case where you choose to change
the model yourself, which is the same work.

Re-embedding a collection because its embedding model changed is an **index migration**, and the
word is doing more work than it looks: the hazard is not the new index, which is fine, nor the old
one, which was fine. It is the state in between.

**Re-embedding a collection is not atomic.** You iterate the documents and write each new vector over
its old one, so for the length of the job some documents hold vectors from the new model and some from
the old, and the query is embedded by whichever model the query path currently uses. Nothing in that
state raises. If the two widths match, the cosine is defined and every search returns ten documents.

```python
"""A half-migrated index, and what it does without erroring.

    python3 migrate.py

Chapter 43 embedded this corpus with two models and found that the
name you ask for is all there is: neither has a dated snapshot, so a
name that starts serving something else is this chapter's subject with
nothing in between. `names.py` confirms it - zero dated snapshots for
either. This program is what happens next.

Re-embedding a collection is not atomic. You iterate the documents and
write each new vector over its old one, so for the length of the job
some documents hold vectors from the new model and some from the old,
and the query is embedded by whichever model the query path currently
uses. Nothing in that state raises: the vectors are the same width, the
cosine is defined, every search returns ten documents.

The two models here are `text-embedding-3-small`, which is 1,536 wide,
and `text-embedding-3-large` asked for 1,536 dimensions rather than its
native 3,072 - so the widths match by construction and a mixed index is
possible. That is the realistic case and the dangerous one; two models
of different widths cannot be mixed at all, which is a migration that
fails loudly and is therefore not this chapter's problem.

The measures are chapter 26's and the code shape is chapter 44's, which
computed both on this same corpus and this same graded key. Nothing
about them is new here. What is new is the fourth arm.
"""
import json
import math
import os
import pathlib
import random
import statistics as st
import urllib.request

ROOT = pathlib.Path(os.environ.get("CORPUS", "corpus"))
DOCS = ROOT / "docs"
URL = "https://api.openai.com/v1/embeddings"
TIMEOUT = 120
WIDTH = 1536
OLD, NEW = "text-embedding-3-small", "text-embedding-3-large"
CACHE = pathlib.Path("migrate-vectors.json")
K = 10
SPLITS = 20          # random half-migrated states, one seed


def key():
    k = os.environ.get("OPENAI_API_KEY")
    if not k:
        raise SystemExit("  set OPENAI_API_KEY and run this again")
    return k


def embed(texts, model):
    """One call for a batch, both models asked for the same width.

    `dimensions` is why this comparison is possible: the v3 models
    return a usable vector of fewer numbers than they natively produce,
    so the new model can be asked for the old one's width.
    """
    body = json.dumps({"model": model, "input": texts,
                       "dimensions": WIDTH}).encode()
    req = urllib.request.Request(URL, body, {
        "Authorization": f"Bearer {key()}",
        "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.load(r)
    rows = sorted(d["data"], key=lambda x: x["index"])
    return ([x["embedding"] for x in rows], d["usage"]["prompt_tokens"],
            d["model"])


def rows(name):
    text = (ROOT / name).read_text().strip().split("\n")
    return [tuple(l.split("\t")) for l in text[1:]]


def corpus():
    paths = sorted(DOCS.glob("*.md"))
    return [p.stem for p in paths], [p.read_text() for p in paths]


def build():
    ids, texts = corpus()
    qs = dict(rows("queries.tsv"))
    qids = sorted(qs)
    out = {"ids": ids, "qids": qids, "served": {}, "tokens": {}}
    for m in (OLD, NEW):
        dv, dt, served = embed(texts, m)
        qv, qt, _ = embed([qs[q] for q in qids], m)
        out[m] = {"docs": dv, "queries": qv}
        out["served"][m] = served
        out["tokens"][m] = dt + qt
    CACHE.write_text(json.dumps(out))
    return out


def cos(a, b):
    num = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return num / (na * nb) if na and nb else 0.0


def key_grades():
    out = {}
    for qid, doc, grade in rows("judgements.tsv"):
        out.setdefault(qid, {})[doc] = int(grade)
    return out


def recall_at(order, grades, k=K):
    total = sum(1 for g in grades.values() if g > 0)
    found = sum(1 for d in order[:k] if grades.get(d, 0) > 0)
    return found / total if total else 0.0


def dcg(order, grades, k=K):
    return sum(grades.get(d, 0) / math.log(i + 1, 2)
               for i, d in enumerate(order[:k], 1))


def ndcg(order, grades, k=K):
    ideal = sorted(grades, key=lambda d: -grades[d])
    best = dcg(ideal, grades, k)
    return dcg(order, grades, k) / best if best else 0.0


def search(ids, doc_vecs, qvec):
    scored = sorted(zip(ids, doc_vecs), key=lambda p: -cos(qvec, p[1]))
    return [d for d, _ in scored]


if __name__ == "__main__":
    v = json.loads(CACHE.read_text()) if CACHE.exists() else build()
    ids, qids = v["ids"], v["qids"]
    grades = key_grades()

    print("  WHAT REPLIED, AND AT WHAT WIDTH")
    for m in (OLD, NEW):
        print(f"    asked {m}")
        print(f"      replied {v['served'][m]}, "
              f"{len(v[m]['docs'][0])} numbers")

    #  The two pure arms: the index before the migration and after it.
    pure = {}
    for label, m in (("before", OLD), ("after", NEW)):
        r = [recall_at(search(ids, v[m]["docs"], v[m]["queries"][i]),
                       grades[q]) for i, q in enumerate(qids)]
        n = [ndcg(search(ids, v[m]["docs"], v[m]["queries"][i]),
                  grades[q]) for i, q in enumerate(qids)]
        pure[label] = (st.mean(r), st.mean(n))

    #  And the half-migrated states. Two things to be exact about.
    #  They are CONSTRUCTED rather than observed: forty documents
    #  embed in one call, so this corpus never passes through a half
    #  state and the arms below simulate what a collection large
    #  enough to need batches goes through. And one arbitrary split
    #  would be one lucky or unlucky arrangement, so this takes SPLITS
    #  of them from one seed and reports the mean and the range.
    rng = random.Random(0)
    half = len(ids) // 2
    mixed = {"old query": [], "new query": []}
    for _ in range(SPLITS):
        done = set(rng.sample(ids, half))
        docs = [v[NEW]["docs"][j] if d in done else v[OLD]["docs"][j]
                for j, d in enumerate(ids)]
        for label, m in (("old query", OLD), ("new query", NEW)):
            r = [recall_at(search(ids, docs, v[m]["queries"][i]),
                           grades[q]) for i, q in enumerate(qids)]
            n = [ndcg(search(ids, docs, v[m]["queries"][i]), grades[q])
                 for i, q in enumerate(qids)]
            mixed[label].append((st.mean(r), st.mean(n)))

    print(f"\n  FOUR INDEXES, {len(qids)} QUERIES, recall@{K} and nDCG@{K}")
    print("    index                    recall    nDCG")
    print(f"    all old, old query       {pure['before'][0]:6.3f}  "
          f"{pure['before'][1]:6.3f}")
    print(f"    all new, new query       {pure['after'][0]:6.3f}  "
          f"{pure['after'][1]:6.3f}")
    for label in ("old query", "new query"):
        rs = [x[0] for x in mixed[label]]
        ns = [x[1] for x in mixed[label]]
        print(f"    half new, {label:10s}     {st.mean(rs):6.3f}  "
              f"{st.mean(ns):6.3f}")
        print(f"      over {SPLITS} random splits:"
              f" {min(ns):.3f} to {max(ns):.3f} nDCG")

    #  Where the ten results came FROM. If the mechanism below is
    #  what it looks like, the half embedded by the other model is not
    #  being mis-ranked - it is not competing at all.
    rng = random.Random(0)
    print(f"\n  WHERE THE TOP {K} CAME FROM, over the same splits")
    print("    query embedded by   from its own half   of 10")
    for label, m in (("the old model", OLD), ("the new model", NEW)):
        rng = random.Random(0)
        own = tot = 0
        for _ in range(SPLITS):
            done = set(rng.sample(ids, half))
            docs = [v[NEW]["docs"][j] if d in done else v[OLD]["docs"][j]
                    for j, d in enumerate(ids)]
            for i, q in enumerate(qids):
                order = search(ids, docs, v[m]["queries"][i])[:K]
                for d in order:
                    new_side = d in done
                    own += (new_side == (m == NEW))
                    tot += 1
        print(f"    {label:19s}  {own / tot * K:14.2f}      {K}")
    pred = pure["before"][0] / 2
    print(f"    so a query reaches about half the collection, and")
    print(f"    half of the before-arm's recall is {pred:.3f} against")
    print(f"    the {st.mean(x[0] for x in mixed['old query']):.3f}"
          f" measured")

    #  And why the mixed arm's recall is not simply half the pure
    #  arm's. Two terms, and the one people reach for is the smaller.
    rng = random.Random(0)
    share, hit = [], []
    for _ in range(SPLITS):
        done = set(rng.sample(ids, half))
        docs = [v[NEW]["docs"][j] if d in done else v[OLD]["docs"][j]
                for j, d in enumerate(ids)]
        for i, q in enumerate(qids):
            rel = [d for d, g in grades[q].items() if g > 0]
            own = [d for d in rel if d not in done]      # old-query arm
            share.append(len(own) / len(rel))
            top = search(ids, docs, v[OLD]["queries"][i])[:K]
            hit.append(sum(1 for d in own if d in top) / len(own)
                       if own else 1.0)
    print("\n  WHY THE MIXED ARM IS NOT SIMPLY HALF, old-query arm")
    print(f"    relevant documents in the query's own half"
          f" {st.mean(share):8.4f}")
    print(f"    of those, the share inside the top {K}  "
          f"{st.mean(hit):10.4f}")
    print(f"    product                                 "
          f"{st.mean(share) * st.mean(hit):8.4f}")
    print(f"    measured recall for that arm            "
          f"{st.mean(x[0] for x in mixed['old query']):8.4f}")
    print(f"    half the pure arm's recall              "
          f"{pure['before'][0] / 2:8.4f}")
    print("    So the second term is the one that moves it: ten slots")
    print("    over half a collection reach almost everything in that")
    print(f"    half, where over the whole of it they reached"
          f" {pure['before'][0]:.3f}.")

    #  The mechanism, and the block above says how complete it is.
    #  Two independently trained embedding spaces have no reason to
    #  align, so a query from one is close to nothing in the other -
    #  which is why the other half does not compete rather than
    #  competing badly.
    print("\n  WHY: THE TWO SPACES DO NOT ALIGN AT ALL")
    print("    query embedded by        vs old docs  vs new docs")
    for label, m in (("the old model", OLD), ("the new model", NEW)):
        same, cross = [], []
        for i, q in enumerate(qids):
            qv = v[m]["queries"][i]
            same += [cos(qv, d) for d in v[OLD if m == OLD else NEW]["docs"]]
            cross += [cos(qv, d) for d in v[NEW if m == OLD else OLD]["docs"]]
        a, b = (same, cross) if m == OLD else (cross, same)
        print(f"    {label:22s}   {st.mean(a):8.4f}    {st.mean(b):8.4f}")
    print("    Every figure is a mean over every query-document")
    print("    pair, relevant or not, so none of them is a quality")
    print("    figure. What they say is that a query is near nothing")
    print("    in the other model's space - a few per cent of its own")
    print("    mean, and negative one way round - which is why the")
    print("    block above found 10 of 10 from the matching half.")

    tok = sum(v["tokens"].values())
    print(f"\n  THIS MEASUREMENT: 4 embedding calls, {tok} tokens")
```

```text
  WHAT REPLIED, AND AT WHAT WIDTH
    asked text-embedding-3-small
      replied text-embedding-3-small, 1536 numbers
    asked text-embedding-3-large
      replied text-embedding-3-large, 1536 numbers

  FOUR INDEXES, 8 QUERIES, recall@10 and nDCG@10
    index                    recall    nDCG
    all old, old query        0.928   0.909
    all new, new query        0.881   0.921
    half new, old query       0.502   0.551
      over 20 random splits: 0.363 to 0.682 nDCG
    half new, new query       0.488   0.555
      over 20 random splits: 0.397 to 0.712 nDCG

  WHERE THE TOP 10 CAME FROM, over the same splits
    query embedded by   from its own half   of 10
    the old model                 10.00      10
    the new model                 10.00      10
    so a query reaches about half the collection, and
    half of the before-arm's recall is 0.464 against
    the 0.502 measured

  WHY THE MIXED ARM IS NOT SIMPLY HALF, old-query arm
    relevant documents in the query's own half   0.5077
    of those, the share inside the top 10      0.9911
    product                                   0.5032
    measured recall for that arm              0.5021
    half the pure arm's recall                0.4641
    So the second term is the one that moves it: ten slots
    over half a collection reach almost everything in that
    half, where over the whole of it they reached 0.928.

  WHY: THE TWO SPACES DO NOT ALIGN AT ALL
    query embedded by        vs old docs  vs new docs
    the old model              0.2367      0.0101
    the new model             -0.0019      0.2374
    Every figure is a mean over every query-document
    pair, relevant or not, so none of them is a quality
    figure. What they say is that a query is near nothing
    in the other model's space - a few per cent of its own
    mean, and negative one way round - which is why the
    block above found 10 of 10 from the matching half.

  THIS MEASUREMENT: 4 embedding calls, 19616 tokens
```

**A half-migrated index lost about forty per cent of its nDCG and nothing errored.** The two pure arms
are where the chapter's corpus usually sits: 0.928 recall and 0.909 nDCG with the old model throughout,
0.881 and 0.921 with the new one. The half-migrated arms are 0.502 and 0.551 with the old query encoder
and 0.488 and 0.555 with the new one — and over twenty random half-migrated states the nDCG runs from
0.363 to 0.682 on the old-query arm and 0.397 to 0.712 on the new one, so the figure depends on which
half happened to be done.

**Two things about those arms before the finding.** They are constructed rather than observed —
forty documents embed in one call, so this corpus never passes through a half-migrated state, and
the arms simulate what a collection large enough to need batches goes through. And the figure moves
with which half happened to be done, which is why there are twenty splits rather than one.

**That said, it does not matter which encoder the query path uses**, and that is the finding which
decides what to do. Switching the query side first does not help and does not hurt; both arms are about the same,
because whichever model embeds the query, half the collection is in the other model's space.

**The mechanism is more complete than "mis-ranked".** Of the ten results returned, **ten came from the
half that matched the query's own model** — on both encoders, over all twenty splits and all eight
queries. The other half does not compete. The cosine block says why: a query embedded by the old model
has a mean cosine of 0.2367 against documents in its own space and 0.0101 against the other, and the
new model gives 0.2374 and −0.0019. **That is Chapter 24's rule arriving as a measurement** — it says
to embed the query with the same model and not a different one, because two models' vectors live in
different spaces and the numbers are not comparable — and what is new here is how complete the
incomparability is. A query is near nothing in the wrong space, so the other half is not mis-ranked;
it is absent. Every figure there is a mean over every query–document
pair, relevant or not, so none of them is a quality figure; what they establish is the alignment, and
the ten-of-ten block is the consequence.

**Then the arithmetic, which does not come out at half and is worth following.** If a query reaches
only its own half, recall might be expected to halve: half of 0.928 is 0.464 against the 0.502
measured. The program decomposes the gap and the term people reach for is the smaller one. A query's
own half holds 0.5077 of its relevant documents, which is the half you expect and contributes
almost nothing to the gap. **The term that moves it is the cutoff**: of the relevant documents in
its own half, 0.9911 land inside the top ten, where over the whole collection the pure arm reached
0.928. Ten slots over twenty competing documents are far more forgiving than ten over forty, so the
mixed arm recovers most of what the pure arm missed — 0.5077 times 0.9911 is 0.5032 against the
0.5021 measured. **Which is a caution about recall at a fixed cutoff rather than about migrations:**
shrink the pool a measure competes over and the measure improves, so the half-migrated arm's recall
is flattered by the very thing that broke it.

So the practice is not *migrate carefully*. It is **never serve a half-migrated index**:

1. Build the new index *beside* the old one, with its own name, and leave the old one serving.
2. Embed the queries with the new model against the new index, and measure — the same measures on the
   same graded key, which is the `all new, new query` row above.
3. Switch the query path and the index together, as one change, because they are one change.
4. Keep the old index until the new one has been serving long enough that you would have heard.

**And the second row of that table is the reason step 2 is not a formality.** At the old model's
width, the new model is better on nDCG and worse on recall — 0.921 against 0.909, and 0.881 against
0.928 — on eight queries, which is a sample Chapter 44 was careful to say settles very little, and
at a width below the 3,072 numbers it natively produces. A migration you were forced into is still a
change whose quality you have to establish, and *the new model is newer* is not that.

**Two things this measurement had that a real migration may not.** The first is widths it could
*make* match: `text-embedding-3-large` returns 1,536 numbers instead of its native 3,072 when you
ask it to, which is the only reason a mixed index was possible here at all. Two models of different widths cannot be mixed —
the cosine is undefined and the code raises — which is a migration that fails loudly and is therefore
not the dangerous one. **The dangerous case is the one where the widths agree**, and that is the case
when a provider repoints a name.

The second is the graded key. Every figure in that table is a figure against eight queries somebody
judged, and a real collection has no such key for the documents it is migrating — which is exactly
why step 2 is the step that gets skipped. If you have no key, the thing you can still do is cheaper
than it sounds: run a sample of real queries against both indexes and read where the two orders
disagree. That is Chapter 30's method on a retrieval change, and it is the only version of step 2
available to most people.

## Attributing a Failure, in the Order the Questions Cost

Chapter 33 owns the trace and says in its own words that it owns only what your trace holds and
why. What belongs here is the order you read it in, because the questions differ enormously in what
they cost to answer and the cheap ones are the ones people reach for last.

| Ask | Answered by | Cost |
|---|---|---|
| Was the model the one I think it was? | The `model` field, read back out of the reply | One column |
| Did the prompt or the configuration move? | The artefact revision on the trace | One column |
| Did the index move? | The index revision, and Chapter 41's key check | One column, one run |
| Did the service get slower rather than worse? | The per-stage timings | Already there |
| Did *my standard* move? | A blind re-label of twenty old outputs, counted | An hour |
| Is the answer actually wrong? | Reading it | Minutes, and the one a judge relocates rather than removes |

**The first four are columns you either have or do not, and that is decided months before the
failure.** This is the whole argument for the versioned artefact: on the day something breaks, the
difference between an afternoon and a fortnight is whether three strings were written on every
request. Chapter 53 made the same argument about a bill and it is the same argument — a record you
did not keep is a question you cannot ask.

**The fifth is the one that gets skipped and it is cheaper than the investigation it replaces.**
Chapter 33 measured it: the same forty outputs, unchanged, scored 85 per cent in week one and 72.5
per cent in week five, with seven labels flipped and six of them from pass to fail. Twelve and a half
points of movement with nothing deployed and nothing fixed. So *it worked last week* has a reading in
which the system is identical and the week-five you is a stricter grader than the week-one you, and
the only way to tell is to re-label old outputs **without looking at what you said last time**.
Twenty of them and an hour are Chapter 33's own figures for what that costs, against the forty its
demonstration used.

**And the last one is last for a reason.** The measurement two sections back is the argument: three
cases went from pass to fail and all three answers were right. If you act on a verdict before reading
it, the first thing you do about a provider's update is undo a model that answered every question
correctly.

**A model judge is the case where two of those questions become one.** Chapter 31 found a judge
holding its verdict on only 17 of 20 showings of the same answer, so its standard is unrepeatable
rather than learned — and when the model under the judge changes, the standard moves outright.
Chapter 33 flagged exactly that and left it here. The consequence is short: a judge is a component
with a version, so it belongs in the artefact like any other, and a gate that uses one has to be
re-run when the judge's own model moves. Otherwise the instrument and the thing it measures move
together and the result is unattributable in both directions.

## Where Your Customers' Text Goes

This belongs in a chapter about failure because it is the failure you cannot roll back. Every other
thing in this chapter is recoverable: pin the old snapshot, rebuild the index, revert the prompt.
Text you sent to somebody else's service last March is sent.

What a provider keeps of what you send, for how long, and what you can delete is its **data
retention**, and the questions worth being able to answer about it are four. The one everybody asks
is among them and is the least useful of them, which is the first thing to say about it.

**Is it used for training?** This is the question that gets asked, and on the provider this book
calls, read on 30 October 2026, the published answer is no for the endpoints its guide covers unless
you opt in. It is worth knowing and it is the
least operationally useful of the four, because it is a single yes-or-no and it does not change what
you can promise anybody.

**What is kept, and for how long?** This is the useful one and it has a different answer per endpoint.
Read on 30 October 2026, the provider's own guide gives abuse-monitoring logs a retention of up to
thirty days by default, keeps stored application state for at least thirty days when you ask it to
store anything, and keeps conversations, vector stores, files, fine-tuning jobs, batches and
evaluations *until you delete them* — which is to say indefinitely, for anything nobody deletes.

**Can it be turned off?** There is a zero-retention arrangement, it requires the provider's prior
approval, and the list of endpoints it does *not* cover is the part to read rather than the headline.
On that list today: vector stores, files, fine-tuning jobs, batches, evaluations, conversations and
the assistants family. **Read that list against your own architecture before you design round it**,
because a retrieval system built on a hosted vector store is built on an endpoint the arrangement
excludes, and the two facts are easy to hold separately and painful to discover together.

**And what can you delete on request?** Chapter 33 named this as a property of *where you put the
trace* rather than of any field, and the same reasoning crosses the boundary: your own trace and the
provider's stored objects are two stores holding the same text, and a deletion request has to reach
both. An object nobody deletes is retained; that is not a loophole, it is the documented behaviour,
and it means deletion is a thing your code does rather than a thing time does.

**Every figure in this section is dated and will move.** That is not a hedge — it is the reason the
section is a list of questions rather than a list of answers. The durable part is which four questions
to ask and which of them is worth least, which is the one that gets asked; the answers are a page on
a provider's site that you read on the day, for the endpoints you actually call.

## Gradual Rollout, and the Trigger You Write First

These are one subject, because a rollout without a trigger is just a slower way to break everything.

A **gradual rollout** serves a change to a share of traffic rather than all of it: some requests take
the new snapshot or the new prompt and the rest do not. Two things it buys, and they are different
things.

**It bounds the exposure.** If the change is bad, it was bad for five per cent of requests for an hour
rather than for all of them until somebody noticed. That is the reason everybody gives and it is the
smaller one.

**And it makes the comparison live.** The two arms are running at the same time on the same traffic,
which removes the nuisance variable Chapter 49 spent a run learning about: when arms run in sequence,
the arm and the moment it ran are one variable. A rollout is Chapter 49's interleaving arranged by the
serving layer instead of by a loop. **Record which arm served each request** —
one more field, and without it a rollout is two populations you cannot separate.

A **rollback trigger** is the condition, written before the release, whose occurrence undoes it.
Chapter 39 owns the rollback itself and says the useful thing about its form: *the previous adapter is
at this path, it was built from this data, it passed this gate on this date, and switching back is
this one change* is a rollback, where *we would go back* is a sentence. What this chapter adds is the
condition, and the measurement in section three decides its shape.

**Do not write the trigger as a score.** On that data a score-shaped trigger would not have fired: the
difference was −0.100 with an interval containing zero, so *roll back if the score drops
significantly* is a trigger that cannot fire on thirty cases, and *roll back if the score drops at all*
fires on noise. Chapter 20 is why both of those are true at once.

**Write it as a named case, and make reading one part of it.** The trigger that works on this evidence
has two clauses: *any case that passed now fails* — which fired, three times, correctly — and *a person
reads those cases before the rollback goes ahead*, which would have stopped it, correctly. One clause
without the other is a worse instrument than the pair. The first alone rolls back a model that answered
everything right. The second alone is a meeting.

| A trigger written as | Would have fired here | And that would have been |
|---|---|---|
| The score drops significantly | No — the interval contains zero | The right outcome, for no reason it could state |
| The score drops at all | Yes, on −0.100 | Wrong, and indistinguishable from noise |
| A case that passed now fails | Yes, naming three | Right that something moved; wrong if acted on alone |
| …and somebody reads them first | Reading stops the rollback | Right, and the only row that is |

**Three more things belong in the trigger and none of them is a score.** A rate of refusals or errors,
which is a shape no quality measure sees. The retry rate, which Chapter 19 says to alarm on and which
moves when the provider is struggling rather than when it is wrong. And the finish reason — Chapter 53
found a reasoning model returning an empty string with its whole cap billed and a `length` in that
field, which is a failure that looks like silence everywhere else.

## What This Chapter Has Not Told You

Five things, deliberately.

**What your trace should hold.** Chapter 33 owns the fields, the content decision and the word
*observability*, and this chapter adds only the order to read them in and three revisions to put beside
them.

**Whether a difference is real.** Chapter 20 owns that, and this chapter leans on it for the interval
that contains zero. The rule that a case is a regression only when it fails more often than it passes
is Chapter 33's, applying Chapter 20's trials to a comparison, and Chapter 33 also owns the
measurement of how many repeats that rule takes.

**How to run a deployment.** Blue-green, feature flags, the mechanics of serving two versions at once:
these are a general engineering subject this book has no special claim on. What is specific to a system
built on a model is which things need the treatment, and that is the four in the artefact.

**Why the model's output moves at all when nothing moved.** Chapter 13 owns the four causes of
non-determinism at temperature zero — floating-point addition, batching, expert routing, and the
provider changing the model or the hardware under it — and is clear that a seed does not fix them. This
chapter owns only the last of the four, and only the part you can pin.

**And what to do when the provider's answer is no.** Everything above assumes a published deprecation
date, a dated snapshot where one exists, and a retention page you can read. Where a provider offers
none of those, the honest answer is that you are running on a dependency you cannot version, and the
decision is a commercial one rather than an engineering one. Chapter 51's supply-chain section is the
nearest thing to a method, and it says the same: know who publishes it, pin what you can pin, and have
a way to notice when it changed.

## Summary and Key Terms

### Summary

*Nothing in my code changed* is almost always true and almost never relevant: four other things move
— the model behind the name you call, your documents, the service's behaviour under load, and your own
standard — and only one of them announces itself. **Much of what you can call cannot be pinned at
all**: grouping one account's hundred and thirty-eight names by what precedes a date gives
ninety-five groups, of which thirty-nine carry a dated snapshot and fifty-six carry none — an upper
bound, because a provider's older `-0613`-style snapshots are not read as dated — with the two
embedding models Chapter 43 used among them. **A floating name is
not the newest** — `gpt-4o` answers with the August snapshot while the November one sits in the same
listing, and of seven floating names probed, five gave the newest beside them, one gave an older one
and one was refused outright. **And the listing is not a statement of what you can call**: a dated
snapshot that is in it returns HTTP 404 `model_not_found` with a message naming it, which is Chapter
40's argument for pinning arriving as evidence — a retirement is loud, specific and timed by you,
where a repointed floating name is none of those. A **gated upgrade** is Chapter 39's evaluation gate
pointed at a change you did not make, and it is that gate's *second* condition standing alone, because
no target set moved. You can run one today without waiting for any provider: hold the prompt, the
cases, the grader and the temperature, change only the snapshot, and **three cases of thirty moved,
all one way, while the score difference of −0.100 ran from −0.200 to +0.000 and could not be told from
zero**. Chapter 33's step 5 settles which to believe — report the cases, never the score movement
— and three repeats was enough here only because **fifty-nine of the sixty case-and-snapshot pairs
were unanimous**, which Chapter 33's own measurement of that count is the reason to check. Then
reading the three is the lesson: `Three years` became `3 years`, `60` became `60 W`, `Seven` became
`7`, and **every one of the newer model's three answers is correct**. And so are the older snapshot's
five failures — `2` for `two`, `90` for `ninety` twice, `10` for `ten` twice — so **digits were
already its behaviour on five cases of its own**, the newer snapshot extends that to two more and
adds the bare `W` on a third, and the baseline of twenty-five of thirty is thirty right answers with five
notations the grader will not take. Accepting the other notation puts both snapshots at thirty of
thirty, which establishes only that notation explains every rejection with nothing left over, since
the lenient grader was fitted to the three that moved, though not to the five it also explains — the evidence that the answers are right is
the replies, read by a person. So the suite was right that something moved and wrong about the word
*regression*: its verdict is a claim about the model and the grader together. A **versioned artefact** is the prompt, the configuration, the index and the model version
released and recorded under one id, because joining four histories on a timestamp fails exactly where
it matters — a gradual rollout, and an index change that has no release event. Chapter 33's trace
carries one of the four. **Re-embedding is where the index version bites**: a half-migrated index lost
about forty per cent of its nDCG with nothing erroring — 0.909 and 0.921 on the two pure arms against
0.551 and 0.555 half done, over ranges of 0.363 to 0.682 and 0.397 to 0.712 across twenty random
splits — and it made no difference which encoder the query path used, because **ten of ten results
came from the half matching the query's own model**, a query's mean cosine being 0.2367 in its own
space and 0.0101 in the other. That is Chapter 24's rule that two models' vectors live in different
spaces, arriving as a measurement, and what is new is how complete it is: the other half is absent
rather than mis-ranked. The mixed arm's recall is not half the pure arm's 0.928 either — 0.464
against 0.502 measured — and the reason is the cutoff rather than the split: a query's own half holds
0.5077 of its relevant documents and **0.9911 of those land in the top ten**, where over the whole
collection the pure arm reached 0.928, so ten slots over twenty competing documents flatter the very
arm they broke. The practice is to build the new index beside the old and switch the query path and
the index as one change, and to measure, because at the old model's width the new model is better on
nDCG and worse on recall on these eight queries. **Where your customers' text goes is the failure you
cannot roll back**: ask what is kept and for how long rather than whether it trains anything, read the
zero-retention arrangement's list of *excluded* endpoints against your own architecture — vector
stores and files were on it on 30 October 2026 — and treat deletion as something your code does. A **gradual rollout**
bounds the exposure and, more usefully, makes the comparison live, so it is Chapter 49's interleaving
arranged by the serving layer; record which arm served each request. And a **rollback trigger** is
written before the release and not as a score: on this evidence *the score drops significantly* could
not fire, *the score drops at all* fires on noise, and what works is a named case that passed and now
fails **plus a person reading it first** — because the first clause alone rolls back a model that
answered everything correctly.

### Key Terms

| Term | Meaning |
|---|---|
| **Gated upgrade** | A provider's new model snapshot treated as a change to your system that you did not make: it does not serve traffic until it has passed the gate your own changes pass. Chapter 39's *evaluation gate* is the instrument; what differs is that the input, its contents and its timing are not yours, that the old snapshot's retirement is a deadline, and that only the gate's second condition — *nothing else moved* — applies, since no target set moved |
| **Versioned artefact** | The prompt, the configuration, the index and the model version released and recorded together under one identifier, written into every trace. Not four histories joined on a timestamp, which fails for a gradual rollout and for an index change, neither of which has a single release moment |
| **Index migration** | Re-embedding a collection because the embedding model changed, or because you chose a new one. The hazard is the half-finished state: if the two widths agree nothing errors, and a query reaches only the half embedded by its own model, because two embedding spaces do not align. Never serve a half-migrated index — build the new one beside the old and switch the query path with it |
| **Gradual rollout** | Serving a change to a share of traffic rather than all of it. Bounds the exposure, and more usefully runs both arms on the same traffic at the same time, which is the interleaving a sequential comparison cannot have. Needs the serving arm recorded per request or it is two populations you cannot separate |
| **Rollback trigger** | The condition, written before a release, whose occurrence undoes it. A score cannot carry it: at thirty cases a real movement does not clear zero and any movement at all is noise. A named case that passed and now fails, plus a person reading that case before the rollback proceeds |
| **Data retention** | What a provider keeps of what you send, for how long, and what you can delete. The retention period varies by endpoint, so the list of endpoints a zero-retention arrangement excludes is the part to read, and the arrangement itself needs the provider's approval. The one failure in this chapter that cannot be rolled back |

### Worth Memorising

| Item | Value or formula |
|---|---|
| What can be pinned | 39 of 95 name groups in one listing carry a dated snapshot; 56 carry none — an upper bound — with both embedding models among them |
| What a floating name answers with | Not the newest. `gpt-4o` → the August snapshot with the November one listed. Of 7 probed: 5 newest, 1 older, 1 refused |
| What the model list is not | A statement of what you can call. A listed dated snapshot returns **HTTP 404 `model_not_found`**, naming it |
| A provider's update, measured | Same prompt, cases, grader and temperature; only the snapshot changed. **3 of 30 cases moved**, score −0.100 from −0.200 to +0.000 — *cannot tell* — and all 3 of the newer model's answers were correct |
| Report which | The cases, by name, never the score movement — Chapter 33's rule, and its majority-of-repeats rule with it. The score is a net; here it was an interval containing three named facts |
| A half-migrated index | nDCG 0.909 → 0.551, nothing erroring, **10 of 10 results from the half matching the query's model**. Mean cosine 0.2367 in its own space, 0.0101 in the other |
| The migration order | New index beside the old, measure on the same graded key, switch the query path and the index as one change, keep the old one |
| A rollback trigger that works | *A case that passed now fails*, **and** somebody reads it before the rollback. Either clause alone is worse than the pair |
| The four that move as one artefact | The prompt · the configuration · the index · the model snapshot. Chapter 33's trace carries one of them |
