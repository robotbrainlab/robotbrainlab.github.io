# What the gates cannot catch

Stated plainly, because overselling the suite would defeat its purpose.

Entries 1–10 are **inherited**, not earned here. They come from a 1,222-page book built
under the same template and the same kind of review, where each one was paid for by a
real shipped defect. They are seeded rather than discovered because rediscovering them
at our own expense would be the only alternative. Each is rewritten for this book's
material.

**Add an entry whenever a defect gets past every gate.** An entry is a *class*, with the
instance that produced it and the practice that follows — not a list of mistakes.

---

**1. A rule explained in prose can vanish with no term missing.** The coverage gate
matches words. A whole method section can disappear while every keyword it used survives
elsewhere in the chapter. The reverse check is a hint; following the hint is manual.

**2. A chapter can be internally perfect and wrong about where it sits.** No gate looks
at sequence. `LEDGER-TAUGHT.md` is the only defence, and it has to be read for its
warning rows as well as its ownership rows.

**3. Reviewers miss things and invent things.** Two reviews passed a chapter with a whole
section missing. Six findings in that project were rejected as wrong after verification.
**Verify both directions. A wrong finding costs more than a missed one.**

**4. A well-sourced but badly explained concept.** The gates verify that a topic is
present and inside the boundary. They cannot verify that the explanation teaches.

**5. A rule stated wider than it is true.** Thirteen of twenty findings in one review
round were an absolute with its counter-example in the same chapter. `verify-absolutes.py`
produces the list; testing each one is manual, and it must be tested against the **book**,
not only the chapter.

**6. Markdown that does not render as written.** Bold inside a backtick span printed
literal asterisks in 110 places before anyone read the generated LaTeX. `filter.lua` now
splits those spans — the patch is ported — but **read the `.tex`, not only the markdown,
when a construct is new.**

**7. A miscount.** Five miscounts in one chapter, every one checkable against a table on
the same page: "four of the five" where three were, "the four forms" above a list of six.
**This book is worse exposed than that one** — the key–value cache size, LoRA's parameter
count against 4096², `O(n² d)`, pass^k at 0.95 over 20 steps, cost per million tokens.
**Compute every number in the file, from the thing it describes, before writing it.**

**8. A form the chapter builds on that the book has never printed.** A chapter taught
"take the `nous` form" and demonstrated it on two verbs the book had never given the
reader. For us: a metric, an API parameter, a Python construct or a formula used in a
worked example or a lab step that no earlier chapter introduced. **One grep per input the
procedure runs on** — and the set to grep is every such input the chapter prints
anywhere, not only the ones in the table that states the rule.

**9. A claim that is really a claim about everything already printed.** "These two are
the only pair", "that is the whole difference". It feels like a fact about two things and
is a claim about the whole book. **Grep before writing *only* or *the whole*.**

**10. A fix applied during a self-audit is itself an unreviewed claim.** A self-audit
found and fixed around thirty real defects and introduced two of its own, both by being
confident about a credit or a count. **When a self-audit changes an attribution or a
number, put it on the list the fix-verification agent is given, worded as a claim to be
checked — not as a fix to be confirmed.**

---

## Earned here

**59. One artefact of a source is not the source, and an absence on it is not an absence.**
Chapter 37 checked ten claims circulating about one study against *the arXiv abstract page* and
reported the result as a property of the paper. Four of the ten are in the paper and the page
does not carry them: the per-category shares 41.77 / 36.94 / 21.30, a second split from a later
version, step repetition at 17.14 per cent, and "five frameworks", which the chapter marked
CONTRADICTS when it is the five the taxonomy was built from against the seven the dataset spans.
So the section's most emphatic passage — *two splits disagree, at most one can be right, a
reader who quotes either has quoted a blog post* — was wrong in every clause, and it was wrong
in the Tip, the Summary, a Review Answer and a lab key, because an emphatic finding propagates.

The same reading made the paper a preprint. The abstract page has no venue line; the conference
page labels it a spotlight poster. Entry 58's own instruction covers this — *when two official
pages of one source disagree, say so in the chapter rather than choosing* — and it was followed
for a transport's deprecation date one chapter earlier and not followed here, which is what a
lesson looks like before it has been learned.

**Why no gate reaches it.** `citations.py` reads citations to chapters, so an external source is
outside the suite entirely. `verify-absolutes.py` listed *"four are not in it"* as an absolute
and cannot test one. And the failure is not a wrong statement about a source — it is a true
statement about a page, relabelled. A page saying nothing about X supports *this page does not
say X* and nothing more.

**The practice.** Name the artefact in the sentence, not the source: *the abstract page states
no shares* is checkable and *the paper states none* was not. Before writing that a source lacks
something, fetch the thing itself — the full text, not the landing page — and where artefacts of
one source disagree, print the disagreement. In chapter 37's case the corrected finding is
better than the one it replaced: eight of ten circulating claims are in the paper, the two
"contradictory" splits are one paper at two versions because its dataset grew, and a share
quoted without a version number says nothing. That is a more useful thing to know than that
write-ups are careless.

**58. Given a list, a writer supplies the reason the source withheld.** The 2026-07-28 MCP
specification deprecates roots, sampling and logging. Chapter 36's first draft of that passage
said why: "All three needed a connection held open in both directions, which is exactly what a
stateless protocol gives up." It is a good sentence. The specification's deprecation registry
gives three *unrelated* migration paths — pass directories as tool arguments, call a model
provider directly, log the way you log everything else — and **elicitation needed the same
held-open stream and was kept**, re-expressed as a multi-round-trip request. Roots itself still
works inside the stateless protocol. So the tidy cause was not merely unsupported; the source
contains its counter-example, one page away.

The same paragraph did the smaller version of it twice. The specification says roots "are
informational guidance rather than an access-control mechanism" and that "the protocol does not
enforce that servers stay within roots"; the draft wrote "which directories it may look in",
which is the permission reading the source explicitly disclaims. And it dated the HTTP+SSE
transport's deprecation to this revision with "an offramp of about a year", where the registry
says 2025-03-26 and a removal three months after a policy reaches Final — the release post and
the registry disagree, and reading only the post made the chapter pick a side without knowing
there was one.

**The shape.** A list of things with no stated reason is an invitation, and the reason that
comes to mind is the one that makes the list look designed. No gate can reach this:
`verify-boundary.py` sees no theory, `verify-absolutes.py` lists the sentence as an absolute and
cannot test it, and `citations.py` only reads citations to *chapters*, so an external source is
outside every check the suite has. **When a source enumerates without explaining, write the
enumeration.** And when two official pages of one source disagree, say so in the chapter rather
than choosing — that is what chapter 6's dated-detail row is for.

**And entry 57's grammar half has now happened in consecutive chapters.** Chapter 35 shipped "a
later step that reads it will not has no reason to look"; chapter 36 shipped "the one a generated
wrapper can cannot write". Both are a verb inserted without the old one removed, both reached a
built PDF, and nothing reads grammar. Two in two chapters is a habit, not an accident: **after a
patch to a sentence, read the sentence** — not the diff, which is where the eye goes and where
the old half is invisible.

**57. A fix that cites another chapter to weaken a claim is the easiest kind to get wrong,
and no gate reads a citation.** Chapter 35 over-claimed that a summary drops negative results
"rather than an accident of this example", and the repair demoted it with "In Chapter 6's terms
this is a mechanism argument and not a measured finding". Chapter 6 has no such category. Its
ladder runs demonstration, one study, practitioner report, settled practice — and it keeps **a
derivation** off the ladder altogether as the *strongest* kind of evidence there is: "When a
claim can be derived, derive it." So the repair reached for chapter 6 to demote a claim, and
named the one thing in chapter 6 that would have promoted it. The honest label was there in the
same table: *demonstration — it worked, on an example chosen by the person showing you.* The
same pass mis-cited chapter 4, crediting it with "the stopping condition belongs in your code"
where chapter 4 says a loop needs **all three** of its stopping reasons and the first of them,
the model saying it is done, is not in your code at all.

Both survived the gate suite, `verify-boundary.py` and a completeness review, because a
citation is the one claim a gate cannot evaluate: `citations.py` prints the cited chapter's
`TOC.md` covers line beside the citation and stops there, deliberately. **A fix made by
appealing to another chapter is not applied until that chapter has been re-read at the line,
not recalled** — and the risk is highest when the appeal is being used to narrow something,
because a hedge feels safe and is a claim like any other (entry 54).

Three more of the same round's repairs failed for reasons no gate reaches. One inserted a verb
without removing the old one, leaving "a later step that reads it will not has no reason to look
for tickets" — grammar, which nothing checks. One renamed a noun and left its article, giving
"an catalogue". One replaced a figure with a worse one: "of the order of sixty tokens" became
"121 characters, so about thirty tokens", and 121 was derivable from nothing — the lines it
pointed at are 200 characters, so the figure it replaced had been the closer of the two. **A
patch applying cleanly is not a fix verifying.** Re-read the sentence, and re-derive the number
from the source the sentence names.

**56. No gate asks whether the book names a concept the way the field names it.** The book
teaches retrieval-augmented generation across chapters 2 and 24 to 29 and 32, about 147 printed
pages, and the string "RAG" appeared in no chapter, in `TOC.md`, in the glossary's 216 terms or
in any of the 100 bank questions. The reader searched for it and found nothing. A
word-boundary sweep over nineteen such shorthands found sixteen absent: RAG,
retrieval-augmented, chain-of-thought, few-shot, zero-shot, prompt engineering, vector
database, vector store, LLM-as-a-judge, function calling, agentic, evals, A/B test,
transformer, SFT, KV cache. Every one of them has its concept taught, under a formal name
instead — intermediate reasoning, supervised fine-tuning, key–value cache, evaluation set,
paired comparison, judge, attention — and every gate passed, because a gate can check that a
concept is present, inside the boundary, evidenced, rendered and indexed, and none of them can
check that it is **findable under the name an interviewer will say**. This is not a new policy
either: `BOOK-GUIDE.md` section 6 already states the preference objective as a formula
*because* "interviewers ask what DPO is", and chapter 14 already names DPO and RLHF in the
shape the fix uses. The rule existed for one term and was never swept.

`verify-inputs.py` is the nearest thing to a defence and it points the other way: it fails a
chapter for using field jargon the book has not given the reader, which is a reason not to
write the shorthand rather than a reason to. It also could not see the names it polices —
its escape hatch compared an upper-case entry in `JARGON` against lower-cased bold spans, so a
chapter that *did* name "RAG" or the "KV cache" in bold was reported BARE anyway. One
`term.lower()` fixes it, and nothing had ever reached that branch to find out.

**The practice.** The chapter that owns a concept names the field's word for it once, where it
explains the formal name, and `LEDGER-SHORTHAND.md` holds the list — what is named, what waits
on an unwritten chapter, and what was checked and deliberately left out. A chapter is not
finished until the shorthand for anything it owns is in it.

**55. A program's printed sentence about a comparison it does not compute is not checked by
running the program.** Chapter 33's `regress.py` printed "That set catches all 3 regressions on
the next change, because version 2's breakages are in it now." The program had the data for
that comparison and never performed it. Running the chapter's own numbers gives **0 regressions
and 5 fixes**: the three breakages were *failing* when the set was taken, so the next
comparison sees them go fail-to-pass and reads them as fixes — and the general fact is stronger
than the claim I was making, which is that **a before-and-after comparison cannot report a case
that was already failing as a regression at all.** It reports a standing failure.

Entry 45 is the ancestor of this — a program printing the counter-example to the claim it was
written to demonstrate — but the mechanism is different and worse. There the output refuted the
sentence beside it, so reading the output was enough. Here the output was silent, because the
sentence was about a comparison the program had not been asked to make, and **every check in
the loop passed**: the block was byte-exact against a real run, the arithmetic gate found
nothing, and the first reviewer had to write the comparison themselves to see it. The claim had
also reached the body, the Summary, Worth Memorising and a Review Answer.

**The rule: a sentence that names a comparison is a claim that the comparison was run.** If a
program has the data, make it compute the thing the prose asserts and print it — which in this
case produced a better section than the one it replaced. The same pass turned up a second
finding by the same route: forcing the repeats question into code showed that **four repeats is
worse than three** (5 of 5 against 7 of 10 subsets reporting a regression that is not there)
because a two-two split is not a majority and reads as fail. Nobody would have guessed that,
and nobody had to.

Every `print` in all 33 chapters was then screened for a sentence asserting a comparison
(*catches all*, *reports no*, *would catch*, *finds all*). Two hits, both sound: chapter 30's
"Exact match catches all 40" computes that set, and chapter 33's "it reports no regressions,
and there were 3" computes both halves. So this one was a trap and not a backlog.

**54. A qualifier written to fix an overclaim is itself a claim, and propagating it multiplies
the error.** Chapter 32's generated-set figure — 8 of 8 against 2 of 8 — is an artefact of a
word-overlap retriever, which the first review was right to say needed qualifying. The
qualifier I wrote was **"a dense retriever narrows the gap and does not close it"**, and I put
it in three places plus the body's program. Nothing in the chapter measures a dense retriever
on anything, and chapter 24 says in terms that paraphrase behaviour "is an empirical property
of that model"; with eight passages on eight distinct topics a dense retriever could plausibly
score 8 of 8 on both sets, which closes the gap entirely. So the repair for one unqualified
claim was another unqualified claim, three times over, and **one copy had already been
generated into `markdown/A-cheat-sheet.md`** — the fix propagated the wide form into the
appendix rather than out of it.

The same round over-corrected in the other direction: "no amount of better retrieval touches
it" became "Chapter 28's order and trimming **can**", which is the proposition chapter 28's own
Warning calls "a comfortable thing to believe" and refuses. **Eleven of that round's
twenty-six fixes were unsound** — the worst score of any chapter so far — and the pattern in
nearly all of them is the same: a sentence written to retire an absolute, written at the speed
of a correction rather than the speed of a claim. **Write a fix as though it were the first
draft of a claim, because it is**, and regenerate the appendices before checking rather than
after, so a propagated fix is visible while you are still looking.

**53. Python rounds a printed share half to even, and the book invites the reader to check by
hand.** `f"{25/40:.0%}"` is `62%`, not `63%`, because 62.5 rounds to the even digit. Chapter
32 printed that figure and quoted "62 per cent" ten times, including in a lab step's expected
result, beside a program whose docstring says **"every count below can be had by hand"** — and
a reader who does it by hand gets 62.5 and conventional rounding gives 63, so the only
conclusion available to them is that they have made a mistake. Fixed by printing the one
half-way figure to a decimal place and quoting it as 62.5 throughout. **Which shares are at risk is narrower than it looks**, and
checking that is how this entry avoided its own overclaim: a half-way share is a problem only
when the even digit is the LOWER one. 25/40 is 62.5 and prints 62, where a reader gets 63 —
at risk. 35/40 is 87.5 and prints 88, which is what a reader gets too — not at risk. Out of
forty, the at-risk numerators are 1, 5, 9, 13, 17, 21, 25, 29, 33 and 37. The general rule is
that a figure the reader is told to verify must round the way the reader rounds, and that
`:.0%` does not always. Every printed share in all 32 chapters was then swept for the same
thing — each `N of M … P%` line checked against conventional rounding — and chapter 32 was
the only one, so this is a trap and not a backlog.

**52. A conclusion can need more than the column it was drawn from, and the chapter had already
written the limit down.** Chapter 32 scores each case twice and calls one cell "the answer was
in the retrieved passages and the system got it wrong". It then said that cell "is generation's,
and no amount of better retrieval touches it". Chapter 28 has a whole section on exactly that
cell — *Order, and the Passage That Gets Ignored*, which opens "Chapter 25's closing table
listed one failure it could not place: the right passage retrieved and still not used. That
lands here" — and its levers are the order of the passages, what gets trimmed, and what the
instruction asks. None of that is generation.

What makes this worth an entry rather than a correction is that **the chapter had stated the
limit on its own conclusion one Note away**: the retrieval verdict is defined as whether an
answer was present and explicitly *not* whether they were the best passages, which it hands to
chapter 26. A column built blind to ranking cannot license a claim about whether ranking work
would help. The reviewer found it by reading the Note against the claim. **When a chapter
defines a verdict narrowly, go back and check every conclusion drawn from it against that
definition** — the narrowing is usually written down, and in a voice confident enough to be
mistaken for a licence.

**51. `tools/citations.py` dropped every citation on a four-space-indented line, and said
nothing.** It skipped any line starting with four spaces or a tab, with the comment "program
source and printed output". That worked while every numbered list in the book had
single-digit items, because `1. ` indents its continuation by three. Chapter 31's *What To
Actually Do* reaches item **10**, whose continuation is indented four — and the chapter's one
pointer to chapter 33 sat on exactly that line. The aid reported "cites 4 other chapter(s)"
and the fifth was invisible. Nothing else in the suite looks at citations, and this is the
third review aid in this book to be wrong in the same direction as entry 11's three gates: a
rule written for one shape matching a wider one.

Fixed by tracking fenced blocks instead of indentation — and then fixed again, because the
first repair *skipped* fenced content and so lost the citations a program PRINTS, which are
citations in the book like any other. Chapter 30 prints two of chapter 28's and one of
chapter 31's. Every citation is now listed and the in-fence ones are tagged, which raised
chapter 30's count from 20 to 27 and chapter 31's to 21. **An aid that drops a finding without
saying so is worse than no aid**, and the second repair was the same mistake as the first in
miniature: trading a false negative for a different false negative because the output looked
tidier.

**50. The unit a table is marked in is a claim, and every number derived from it inherits
the error.** Chapter 30's `metrics.py` first mapped each candidate check to the failure
*modes* it caught. That unit is wrong: a check catches failures, and a mode is a group of
them, so the ordinary case is a mode covered in part. Two of the five rows were false as a
result, and **both were refuted by the book itself**. Chapter 28's three mechanical citation
checks were credited with the whole of *Citation does not support*, 8 failures, when they
catch 3 — and chapter 28's own Worth Memorising row says the three are "necessary and not
sufficient" and names three shapes that get past them, four of which are in that mode. And
"exact match against a reference answer" was credited with 13 of 40 by reasoning about which
modes it was *for*, when it fires on all 40, because every failure differs from the reference
answer; its real defect is that it fires on correct paraphrases too, which is precision and
not coverage. **The program computed its percentages correctly from both wrong inputs**, so
nothing in the arithmetic gate, the build or the round-trip check could see it. Re-marked
failure by failure, with a column for how many modes a check closes outright — which also
produced the better lesson, since the partial-coverage case is now taught rather than
hidden. The question to ask of any table of this shape is **what is one row, and is that the
thing the claim is about.**

**49. `filter.lua` silently refuses to index four words, so a Key Term named with one of them
can never have an index entry.** `index_strong` returns nil for any bold whose text
lower-cases to something starting with `note`, `tip`, `warning` or `you understand`, because
those are the book's own admonition labels. Chapter 30's Key Terms table named a term
**Note**. The table itself never indexes — a bold inside a table becomes `\textbf{}` with no
`\index{}`, so **every chapter's index entries come from its body** — and the body's
`**note**` was dropped on the floor by the admonition rule. No gate notices:
`verify-index.py` only checks the shape of entries that exist, and the glossary gate only
checks that the table matches Appendix C. The whole book was grepped and chapter 30 was the
only chapter with such a term; the term was dropped rather than worked around, because
"note" is ordinary English used plainly there rather than a term of the field. **The check is
the one already in the session instructions, run in BOTH directions**: every index entry read
against the Key Terms table, and every Key Term read against the index entries. Only the
first direction had ever caught anything, and it cannot catch this.

**48. `verify-voice.py` has no pattern for the book talking about its own drafting.** Its
patterns cover the planning documents (`BOOK-GUIDE`, `TOC.md`, the roadmap, the website) and
the authoring relationship (`we decided`, `the owner`, `this book was written`). Chapter 30
shipped three sentences to a reviewer saying **"the first draft of this chapter failed that
check"** — once in the body, once in a lab step and once in the Summary — and the gate was
CLEAN on all three, because none of them names a build document or an author. The review did
not raise it either; it was found reading the chapter against the rule rather than against
the gate. The sentences were doing real work, crediting the partition check with catching
something real, so they were rewritten to say what is true of the method rather than what
happened while writing: a note that fits nowhere is the easiest of forty to lose. **A gate
that passes is not the rule**, and this is the second kind of voice violation its patterns
cannot see.

**47. Generated data can have a property you did not put there, and a program's seeding can
encode the answer it is presented as finding.** Chapter 29 made a corpus of twenty clusters with
`sin(group * 1.7 + d)` and said so. It was not twenty. Because 11 × 1.7 = 18.7, within 0.15 of
6π, groups eleven apart came out at cosine **0.9858** against −0.0192 for adjacent ones — so by
the only measure the index uses, the corpus held about eleven clusters, and the index was
splitting 18 of the 20 nominal groups across two lists. Two passages explained their
measurements using a structure the data did not have.

**What made it invisible is that I checked the wrong thing.** The list *sizes* came out 94 to
106, close to the hundred I expected, and that matched. Memberships did not, and nothing prints
memberships unless you ask.

**Then the fix did it again, one level up.** The rebuilt corpus genuinely has twenty separable
groups, and the index genuinely finds them — but only because `build` seeds from one vector
every `N // nlist` over groups that are blocks of `N // nlist`, so it starts with a point inside
each one. Seeded at random it recovers them in **0 of 10** trials, with lists from empty to
double size. "Discovered rather than told" was false again, for an entirely different reason, in
five places including the program's own docstring.

**So the entry has two halves and they share a cause.** *Check the property you claim, on the
data you generated, by the measure the program actually uses* — not a proxy like size, and not
the formula's intent. And *check what the starting conditions give away*: a demonstration that
finds structure is only a demonstration if it would still find it from somewhere else. Both are
one line of code and neither is reachable by any gate, because a gate reads prose and arithmetic
and this lives in the data and the seed.

A third thing worth carrying: the docstring written to confess the first defect contained three
errors of its own, including a cosine of 0.99 described as "0.99 apart" — which inverts it — and
a mention of an earlier draft of this book, which the voice rule forbids and no pattern caught.
**A confession is new prose. It gets the same reading as anything else.**

**46. A qualifier added to scope a claim can invert it, and the sentence defending it will say
"the direction holds".** Chapter 28 computed that filling a 128,000-token window costs 62.5 GiB
of key-value cache against 13 GiB of weights, and wrote that this is *nearly five times the
memory the model itself occupies*. A review asked for it to be scoped, because chapter 15's own
Note says real systems share one set of keys and values across several heads. So I added the
scope — and then wrote "The direction holds; the factor is the shape of an arithmetic."

**It does not hold, on one of its two readings.** At a sharing ratio of eight the 62.5 GiB
becomes 7.8, which is *less* than the 13 GiB of weights. So "the cache is a real cost" survives
and "the cache dwarfs the model" is refuted — by the very footnote I had just added to protect
the claim. The scoping sentence was doing the opposite of its job: it looked like diligence and
it licensed the headline it was supposed to qualify.

**The test that catches this is one question: after the qualifier, is the headline still true at
the extremes the qualifier admits?** Not *is the claim more careful now* — qualifiers always
look more careful — but *does the range I have just conceded contain a case that refutes me*.
Here the arithmetic took one line and the answer was yes.

This is entry 40's family and worth its own entry because the mechanism is different. Entry 40
is a replacement claim that escapes reading. This is a replacement that gets read, approves of
itself for being modest, and never has its own numbers run.

**45. I wrote a program to demonstrate a claim, and the program printed the counter-example.**
Chapter 27's headline derivation was that *the set of questions your system can answer is
bounded by what is whole inside some row*. I called it the most useful thing in the chapter, put
it in six places and the generated cheat sheet, and had `index.py` print *"the question is
unanswerable from this index"*.

It is false, and the refutation was in the program's own output. The three size-60 rows **tile
the document** — rejoin them and you have the original exactly — so rows 0 and 1 together
contain the whole answer sentence. Return both and a reader has the answer. The chapter printed
all three rows directly above the claim.

Worse, I had handed the reader the mechanism too. Every row stores a `start` offset, which the
chapter calls citation metadata — and an offset plus a document name is exactly how a real system
fetches a retrieved chunk's neighbours. The refutation sat two paragraphs below the claim,
described as a feature.

**Entry 24 says write and run the program before any sentence about it. This is the next failure
along: I checked that the program produced the output I expected, not that the output supported
the claim I was drawing from it.** Those are different readings and only the first is automatic.
The question to ask of a demonstration is not *did it print what I predicted* but *what else
does this output show*, and in this case the answer was sitting in three lines of `repr`.

The narrow claim survives and is better — no retrieval method can return a single *passage* that
answers it, so bad cuts move the reassembly downstream rather than destroying information — and
the program now prints the tiling check and the pair check itself, so it argues both sides.

*And the fix overclaimed in turn*, which is entry 40 for the third chapter running: "bad cuts do
not put the information beyond reach" is true only of cuts that tile, while this chapter's own
method discards page furniture on purpose. A replacement claim is new prose. It gets its own
reading, every time.

**44. Two reviews per chapter was not enough for one whole class of defect, and ten closed
chapters proved it.** The reader asked, on 28 Oct 2026, whether the attention paid to page
counts had damaged the content. An audit said no — no record anywhere shows material cut or
padded to fit a budget, and the page spread runs 56% to 125% with no cluster at 100%. But the
audit surfaced something else: the failure mode that had dominated every recent review, **a
claim stated one notch wider than its own support**, was not named as a class until entries 34,
37 and 40, which came out of chapters 20, 22 and 25. Chapters 1 to 19 were reviewed before any
brief hunted for it. And of the three chapters where a *third* reading was ever run — 23, 25,
26 — it found a blocking teaching error in all three.

So a narrow pass went over chapters 8 to 17, briefed on that one mode and told to reject
omissions, style and coverage outright. **It found 36 claims needing narrowing across ten
chapters, about 3.6 each**, in chapters that were twice-reviewed and gate-clean. The worst were
not vague: chapter 15 told the reader a batch of fifty makes each request cost "something
approaching fifty" times less, where its own next paragraph picks a configuration whose ceiling
is **4.34x**; chapter 16 asserted that the output-as-scratchpad mechanism is why working-out
improves accuracy, which **chapter 22 explicitly refuses** in as many words; chapter 10's claim
that different vocabularies give different token counts is refuted by **its own lab step 8**;
chapter 13 told the reader every token after a flipped near-tie differs, where its own
mechanism requires a tie to flip at all.

**Three things are worth carrying from the shape of it.**

*The crib sections are where this lives.* Of the 36, a large share sat in a Summary, a Key
Terms row, a Worth Memorising row, a lab key or an answer key — and in several cases the
Summary held the *correct* narrow form while a glossary row or an answer held the wide one,
which is the inversion of the usual direction. A fix that reaches the argument and not the
glossary has not been made.

*A gate cannot catch this.* Every one of these chapters passes every gate, and the gates are
not the weaker for it — arithmetic, index shape, bank coverage and citations are all now checked
book-wide. What no machine can check is whether a true sentence is stated at the strength its
evidence carries. That is why the pass had to be a reading.

*The mode is still sharpening.* Each chapter written teaches more about what it looks like, so a
pass run later catches more than the same pass run earlier — which is the argument for running
this again over chapters 18 to 26 once Part II is finished, rather than once per chapter.

**42. A citation is the one claim a reviewer cannot check without leaving the chapter.**
Chapter 23 credited chapter 51's premise to chapter 16 and chapter 21's sentence to chapter 20.
Chapter 25 credited one of chapter 21's to chapter 20 as well. All three read perfectly in place:
the sentence is true, the mechanism is right, and only the number beside the word *chapter* is
wrong. Each survived a completeness review whose brief asked for cross-chapter errors.

**The reason is structural.** Verifying "chapter 16 owns this" means opening `TOC.md`, finding
row 16 and reading its covers list — for every citation, and a dense chapter has thirty. A
reviewer reading the chapter in front of them has no cue that any particular number is the wrong
one, because a wrong number looks exactly like a right one.

So `tools/citations.py NN` prints each cited chapter with that chapter's own covers line beside
it, and the question to ask of every line is *does the chapter I am pointing at actually own
this?* It is now the third pre-review check in `.claude/CLAUDE.md`.

**It is deliberately not a gate**, and the reason is entry 18. The book cites chapters in a dozen
shapes and only seven of 537 citations state ownership outright, so a pattern wide enough to
catch the rest would flag mostly correct prose. The script says this in its own docstring, so
nobody later mistakes its exit code for a verdict.

*Measured, 28 Oct 2026.* A keyword-overlap heuristic was tried over all 26 chapters, to see
whether a gate was possible after all. Matching strong ownership forms only and comparing the
claim against the cited row's covers list, it shortlisted **51** citations; joining each claim
with the two following lines, because most wrap, brought that to **18**. All 18 were then read
by hand against their `TOC.md` rows and **all 18 were correct** — so the heuristic's precision
on this book is zero and the sweep's real finding is that **no false citation is currently in
the book**, chapters 23's and 25's having been fixed. That is the evidence for leaving this an
aid: a gate would have cried wolf eighteen times to catch nothing.

**41. The entry-19 guard was bypassable by crashing.** Chapter 25's `written:` field said
`2026-10-28` — a bare date, where the driver always writes a full offset-aware stamp. It was a
bare date because I filled it in by hand instead of running `chapter.py written`, which is
precisely what entry 19 added that guard to stop. The guard did notice. It then died with
`TypeError: can't compare offset-naive and offset-aware datetimes` instead of refusing.

**A gate that crashes is worse than a gate that is absent**, because a traceback reads as a tool
fault rather than as a verdict about my work. The first thing a crash invites is a workaround —
edit the field, get past it — which is the exact action the guard existed to prevent, now
performed with the guard's blessing. An absent guard at least leaves the question open.
`datetime.fromisoformat` accepts a date, so the value parsed and the comparison was what broke;
the fix is an explicit `tzinfo is None` refusal with the reason in the message, and it is proved
by running it against the bad field.

**And the stamp itself could not be recovered.** The chapter file was untracked, so git held
nothing, and a record's whole job is to be evidence. What went in is an evidence-backed *upper
bound* — a scratchpad file that probes this chapter's own counter-example has mtime 11:03:30, and
it was written after the completeness review, which follows writing — with a
`written-stamp-note:` field saying in full that the value is a bound and not a clock reading.
**When a stamp is lost, record the bound and say it is a bound.** Do not invent a plausible time:
the precision is the whole value of the field, and a fabricated stamp in range is the one thing
nothing else catches.

**40. A retraction can smuggle in a fresh overclaim, because it is written in the same breath.**
Chapter 25 claimed that nothing in dense retrieval prefers a true answer over its negation. The
completeness review killed it: the vectors are stipulated, so they support no claim about any
method, and it is an outcome claim where a mechanism can only support a claim about capability. I
replaced it with "a cosine has no term that represents polarity", labelled it the narrow claim,
and shipped it.

**It proves far more than the thing it was narrowed to.** A cosine has no term representing
*anything* — chapter 9 says outright that no single number in these vectors means a nameable
thing. So the same sentence denies the method any handle on topic, and chapter 24's paraphrase
with no shared words refutes that; this chapter's own closing concession refutes it too. The
replacement was a *worse* claim than the one it retracted, and it carried the retraction's
authority.

The mechanism is the dangerous part. **A retraction feels like the end of the work, so the
sentence that replaces it never gets read as new prose** — and it is new prose, written faster
than the original and under the impression that the thinking has already been done. Entry 38 says
a passage written to answer a review has had one reading; this is the sharper case, because the
passage is *also* the place I am least likely to look again. **Every replacement claim gets its
own reading, and the test is to ask what else it would prove** — if it would license a sentence
the book elsewhere refutes, it proves too much and is not the narrow claim.

*Chapter 26, twice more, and it widens the entry.* It is not only a retraction's replacement
that escapes reading — it is **any qualifier written to narrow an overclaim**. Both of chapter
26's second-round must-fixes were qualifiers added to fix a first-round finding. "It does not
grow with the collection" was corrected to "Only the LAST of those three is flat in n", which is
false (the query embedding is flat in n too) and contradicted the cost table printed two lines
above it. And the bi-encoder correction, which rightly stopped calling it an escape, replaced
that with "a shared-encoder bi-encoder is symmetric" — refuted by chapter 25's own body, which
names a side marker on one shared model as the other route to `f != g`. **A qualifier is a new
claim.** Read it against the thing it sits next to, which in both cases was enough to catch it.

**43. `tools/verify-bank.py`: a record must name the bank questions the bank assigns it.**
BOOK-GUIDE §15 makes the interview bank the standard a chapter is held to, and the failure mode
is never disagreeing with it — it is never looking. Chapter 19 read its range as 39–41 when it
owned 39–42, shipped to review with no answer to q42, and needed a whole new section (entry 30).
Chapter 15 made the same error cheaply: its record said "29, 30 and 31" where the bank assigns
29–32, and q32 happened to be answered anyway. Both were a *remembered range* standing in for a
grep, and an audit on 28 Oct 2026 found the second one.

The gate is weak by construction — a record can name a question it never answered — but it
catches the one error that has now happened twice. Two bugs in it are worth remembering, because
both are entry 18's cry-wolf shape and both flagged correct records: it must expand ranges
("39 to 42" names 40 and 41), and the `q` prefix is load-bearing, since `\b54\b` does not match
inside `q54`. It reported seven false problems before those were fixed. Proved by removing one
question from a record and watching it exit 1.

**39. The arithmetic gate reported 540 equations checked and was checking 56.** Chapter 24
printed a display equation and told the reader to verify it by hand — "because the whole chapter
rests on being able to". The equation was wrong: `0.90 / (0.9695 × 0.9487)` is 0.9785, which
rounds to 0.979, not the 0.978 beside it. `verify-arithmetic.py` reported the file clean.

**It had never looked at that line.** `value()` matches `PURE` against the *raw* text, and `PURE`
admits only digits and arithmetic punctuation — so `\[`, `\]`, `\frac`, `\sqrt` and `\;` all
defeat it, and every display equation in this book has at least one of them. Instrumented over
all 25 chapters: **540 statements found, 56 with two evaluable parts, 480 silently skipped.** The
gate reads text blocks and prose, which is genuinely useful, and it had been reporting a number
ten times its real work since it was written.

**A second hole was live underneath that one.** `places = min(decimals(p) for p, _ in vals)` took
the comparison's precision from the *narrowest* part of a chain, and `decimals()` returns 0 for
any part ending in `)`. So a chain with a bracketed step was compared to zero decimal places,
where everything rounds to 0 and nothing can fail. Proved on a control:
`50 / (37.42 x 4.243) = 50 / 999.99 = 0.315` passed — a wrong divisor in a chain, which is the
exact defect the gate's own documentation says it catches.

**What was changed, and what was not.** `places` now comes from the printed answer, which fails
that control and leaves all 25 chapters clean — tested both ways. The summary now reports
statements found, statements arithmetic-checked, and how many were skipped, and says in words
that display maths and prose are not checked here. **Parsing `\frac` was considered and
rejected**: it needs a brace-balanced rewriter, a strip list, an implicit-multiplication rule,
and moving the `PURE` test off the raw text — and that last one dismantles the only thing keeping
this gate off prose. A gate that cries wolf is worse than a narrow one that says so.

**How to apply.** A gate that prints a count must count what it did, not what it saw. When a
gate has never failed, ask what it would take to make it fail and then do that — entry 27 said
this and it was applied to one gate rather than to the habit. And the discipline that actually
caught this was the completeness review reading a display equation with a calculator, which is
the answer to what covers the 480: a reviewer, named in the brief, told which equations the gate
cannot see.

---

**38. A section added because of a review has not been reviewed.** Chapter 23's completeness
review found that two of its Covers items were narrated rather than shown, and that chapter 18
forwards the tool message here while no message list containing one is printed anywhere in the
book. So a section was written to fix that — and then the fix-verification pass read it, which
made that pass the section's *first* review rather than its second.

The fix-verification noticed this itself and said so: nearly every substantive finding in it was
inside the new section, which is what a *completeness* review produces. A third pass was run on
that section alone, and it found a blocking teaching error the other two had missed. The rule the
section gave for telling a prose answer from a truncated proposal does not separate them — both
fail to parse in exactly the same way, which `handle` demonstrates — and the rule then labelled
the surviving case a failure, which made the chapter's own successful final turn a failure. The
chapter handed that non-rule to the reader twice, in the body and as the fix in a lab step.

**The project's rule is two reviews per chapter, and I had satisfied it in letter.** The second
pass did read the changed passages, as the rule says. But a passage written *in response* to a
review has had one adversarial reading, not two, and the arithmetic does not care that it arrived
late.

**How to apply.** When a review's finding is "this is missing" rather than "this is wrong", the
material you write to answer it starts the loop again for itself. Either name it in the
fix-verification brief as new and unreviewed — which is worth doing anyway, and was done here —
or expect to run a short third pass over that section alone. A focused pass is cheap: this one
read one section and twenty lines of edits, and it caught a false rule that two broader passes
had read straight past, because they were checking a list of findings and it was reading the
prose.

---

**37. I widened a derivation's conclusion and kept the label.** Chapter 6 puts a *derivation*
off the evidence ladder: it "follows from arithmetic, or from a mechanism you can check
yourself", and it supports "whatever the arithmetic covers". Chapter 22 argued that a schema
permitting only `{"answer": …}` forbids the intermediate tokens, and that Chapter 16 has already
established the model's only scratchpad is its own output. That is a derivation, and its
conclusion is exactly: **the scratchpad is gone.**

What the chapter then wrote was that it "predicts exactly where the damage will be", and a lab
key said "expect a loss". Those are claims about *accuracy*, and they need a premise the chapter
has nowhere to get: that writing the working out actually improves the answer on this task. A
model may compress the same computation into one forward pass and be right anyway. So the
chapter had derived a **capability** claim and spent it on an **accuracy** claim, under a label
that says no evidence is required.

The fix-verification pass put it better than I had: the thing off the ladder is the capability
claim, and the accuracy claim sits around demonstration or one study — which is where the
chapter had already, correctly, placed the *size* of the effect. It had the right split one
notch off, so the discipline was visible and still mis-applied.

**It also noticed that one of my two premises was decorative.** "Masking deletes probability
mass" does no work in that argument; the work is done entirely by "the grammar admits only the
final object". A derivation with a spare premise in it is a sign that the conclusion was written
first.

**How to apply.** When you label something a derivation, write the conclusion as narrowly as the
steps support and then read it back on its own. If it contains a word like *worse*, *better*,
*faster* or *damage*, it is probably an outcome claim and outcomes need evidence; what a
mechanism gives you is usually a capability or an impossibility. Then check each premise is load
bearing — drop it and see whether the conclusion still follows. And remember the asymmetry
Chapter 6 relies on: a derivation does not date, so mislabelling an empirical claim as one
exempts it from ever being re-checked.

---

**36. I widened a tolerance three times instead of looking two lines further down the file.**
The index's letter-group glue has a shrink, documented since entry 17. On 2026-10-28 an overfull
box appeared on an index page and I raised that shrink from 3pt to 4pt. Hours later, after
another chapter, a bigger box appeared on the *last* index page and I raised it again, 4pt to
9pt — fully collapsible, which I wrote up as "the end of this line, you cannot shrink below
zero", correctly observing that each round had been triggered by an unrelated chapter's length.

Having observed that, I did not ask why. **The cause was `columns=2` on `\makeindex`, two lines
below the comment I was editing.** It makes imakeidx set the index in `multicol`, and multicol
*balances* the columns on its last page — so the final index page was required to be full, and
no amount of glue could change that. One `\raggedcolumns` lets it be short by design. With that
in place the shrink went back to book.cls's own 3pt and the build is clean at 254, 257 and 272
printed pages, where every shrink value had failed at one page count or another.

The fix-verification pass found it by **bisecting my own fix**: `minus 5pt` still overfull,
`minus 6pt` clean — so 9pt had spent all the remaining headroom for no measured reason, and at
full collapse a bold letter heading butts against the previous group's last entry. It also
falsified the obvious alternative, giving each index entry a little `\parskip` shrink, which
did not move the box at all. That is what told it the slack had to come from somewhere other
than glue.

**How to apply.** When the same gate fails a third time on the same mechanism, stop adjusting
the number. The pattern "an unrelated change's size decides whether this passes" means the
thing has no slack by design, and the fix is to give it slack by design rather than to buy a
little more each time. Read the package options as well as the macro: the behaviour that was
forcing a full page was declared in the setup, not in the code I kept editing. And when you
write "this is the end of this line", treat that sentence as the signal to go and find the
cause — it is an admission that the current lever is exhausted, which is never the same thing
as the problem being solved.

---

**35. I read `check-all.sh` through a `tail` and ticked a box that said the gates were clean.**
Chapter 21's record claimed `verify-render.py · verify-voice.py · verify-boundary.py — all
CLEAN`. `verify-render.py` was reporting **six** findings on that chapter and exiting 1: four
`text` lines over the 64-character limit and an inline code span broken across a source line.
I had run `bash tools/check-all.sh 2>&1 | grep -E '…' | tail -20`, and the RENDER section was
above the cut. The suite ended `GATES FAILED`; I read that as the record gate alone, because the
record gate was the failure I was expecting.

**This is entry 28 for the third time in one session** — the first was `patch.py` through
`tail -4`, the second was a transformation script whose replacement silently matched nothing
(entry 29). The pattern is not carelessness about tails. It is that I truncate output when I
already believe I know what it says, which is exactly when the truncation costs something.

**The cost here was a false entry in a record**, which is worse than the defect it hid. Every
other gate's evidence in that record is only as good as the habit that produced this one, and a
reviewer had to find it.

**How to apply.** Run `bash tools/check-all.sh` and read the whole thing, or grep for the
failure token and nothing else: `bash tools/check-all.sh 2>&1 | grep -E 'FAIL|GATES'`. Never a
`tail` or a `head` on a suite that reports per-item status. And before ticking a box that names
a tool, run that tool on its own and read its exit status — `python3 tools/verify-render.py;
echo $?` is two seconds. A record is evidence; a box ticked from a remembered expectation is
not evidence, it is a claim.

---

**34. Every time chapter 20 validated a claim, it validated it against data chosen so the claim
could not fail — and then stated the conclusion without the condition.** The completeness review
found this four times in one chapter, and the four together are worse than any one of them.

- **The headline number.** `one_run()` treats every case as a coin at 0.70. Under that model,
  re-running the same forty cases and drawing forty fresh ones are *the same distribution*
  (measured: 0.0723 and 0.0726), so the chapter's ±0.14 was a case-sampling figure presented as
  run-to-run variation. A realistic set — reliably right on 28 cases, reliably wrong on 12 — has a
  run-to-run spread of 0.022 against the same 0.072 of case-sampling spread.
- **The check that was an identity.** The chapter had the bootstrap's interval for a single run
  "agreeing to three decimal places" with ten thousand real runs, offered as evidence that the
  method works. `A` holds exactly 28 ones of 40, so resampling it *is* Binomial(40, 0.7)/40 — the
  very distribution the other procedure sampled. The exact percentiles are 0.550 and 0.825 too.
  One distribution reached three ways, and it had to agree.
- **A mechanism stated backwards.** "Pairing removed the variation that comes from which cases
  you happened to draw" — if it had, the interval would have zero width, and it is 0.250 wide.
  Pairing cancels the part of that variation the two versions *share*.
- **A typical interval sold as a detection rate.** "Two hundred cases is where this difference
  becomes visible" came from `PATTERN * k`, which replicates the forty-case mix exactly and so
  pins the sample proportions to the population values. Over every real draw of two hundred,
  weighted by likelihood, the interval clears zero 72 times in a hundred.

**What the four have in common** is that the worked example satisfies the claim's hidden
condition, so the condition never announces itself while you are writing. That is entry 25's
shape, and entry 26's, arriving together in the chapter where it does most damage: a statistics
chapter hands the reader sentences to repeat to somebody looking for exactly that gap.

**How to apply.** When a chapter demonstrates a claim, write down what the demonstration assumes
*before* writing the sentence the demonstration supports, and then ask what the same code does
when the assumption is false. Run it. Every one of these four was settled in under a minute by
changing one list and re-running — a near-deterministic set instead of coins, a list that is not
exactly 70 per cent ones, fresh draws instead of a replicated pattern. And treat an exact
agreement as a warning rather than a result: two procedures that match to three decimals are
usually one procedure.

A second lesson, from the same chapter's fix pass. **Three of the nine problems the
fix-verification found were false statements in the Summary and the answer key while the body was
right** — entry 16 recurring inside a pass whose brief was entry 16 — and two more were entry
33's bold-is-a-term class recurring in the chapter that had just paid for that gate. A fix pass
needs its own sweep, with counts, over the back matter and the generated appendices. Reading the
body and believing you are done is how all five got through.

---

**33. Bold means "new term" in this book, and I had been using it for emphasis.**
`latex/tools/filter.lua` turns every bold span of four words or fewer, not ending in
punctuation, into an automatic `\index{}` entry, because in this book a bold short phrase *is*
a new term. Chapter 19 shipped `\index{4}` from `**4** at once keeps you at the limit`, and
nobody noticed, because nothing in the gate suite ever looked at the index.

Chapter 20 made it a build failure. It bolded three intervals, and one of them was
`**−0.050 to +0.200**` with a Unicode minus. makeindex letter-groups on the entry's **first
byte**, so it emitted `\indexletter{<0xE2>}` — half of a two-byte character — into `book.ind`.
XeLaTeX replaced the invalid sequence with U+FFFD, found no glyph for it in the letter-group
font, and `Missing character` went to 1.

`tools/verify-index.py` now rejects any entry whose first character is not an ASCII letter, and
it is wired into `check-all.sh` after the build, because it reads the generated `.tex`. It found
six across the book: two in chapter 15, one in 19 and three in 20. Chapters 15 and 19 were
reopened for it and resealed; neither lost a word of text.

**Its first draft also rejected a non-ASCII character anywhere in an entry, and that was wrong
about the mechanism.** Chapter 7 indexes the four part names, "I · Understand" and its siblings,
and their middle dot is harmless: only the first character becomes a letter group. The strict
version would have made me mangle correct content to satisfy a rule I had reasoned badly — the
same mistake as entry 32, one chapter later, caught this time before it shipped because the gate
printed what it was rejecting and four of the ten hits were obviously innocent.

**How to apply.** Bold is for terms. Emphasis on a number, an interval or a phrase that is not a
term goes in *italics*, or in a bold sentence that ends in a full stop, which the filter skips,
or carries `[**…**]{.noindex}`. When you write a new gate, read every hit of its first run: if
some are plainly fine, the rule is wrong, not the content.

---

**32. A tolerance is not a fix, and a cause you did not read out of the log is not a cause.**
Chapter 19 made the book nineteen pages longer, and the last page of the index landed
0.22693pt over the text height. I decided, without reading the log far enough to see which
file the page belonged to, that it was a long table in the generated glossary. `\vfuzz` did not
suppress the report, so I wrote `tools/overfull.py`: a gate that ignores an overfull `\vbox`
under 1pt, proved against injected failures, wired into both build gates, and carrying a
docstring that stated the glossary as the cause.

**Every part of that was wrong except the arithmetic.** The log says
`(./book.ind [256 … ]` immediately before the box: it is the **index**. `latex/preamble.tex`
already carries ten lines about this exact defect from entry 17 — the index letter-group glue
was once rigid, went overfull by 9.33658pt, and was given flexibility precisely so the index
could absorb being slightly over a page. The shrink was 3pt. Making it 4pt removes the box,
changes no page, and needed one character. The fix-verification pass found this by reading the
log I had not read, and ran the control builds to prove it.

So a gate had been loosened, for a chapter of mine, on a diagnosis I had invented, when the
real fix was available and already written down in the file I was editing around.

**How to apply.** Before touching a gate: read the log until you can name the page *and* the
file the box is on, and say it out loud. Then grep the preamble and the ledger for the
mechanism — if either already discusses it, the fix is almost certainly there and somebody has
already paid for the reasoning. Changing a gate is the last resort and it needs a cause the log
supports in words, not a threshold that makes the symptom go away. The giveaway here was that I
could not state the cause without hedging, and I wrote the docstring anyway.

---

**31. A gate that always fails gates nothing.** `make check` runs `latex/tools/check.sh`, the
documented pre-flight: page size, embedded fonts, overfull boxes, undefined references, text
off the page. It also checked that the book was between 50 and 100 numbered pages, which is the
figure that came with the template. The book passed 100 pages somewhere in Part I, so every run
since has ended `PRE-FLIGHT FAILED` with every real check passing.

Nobody read it, including me. The cost showed up in chapter 19: after the build-gate change
above, `check-all.sh` and `make check` disagreed about whether the book built clean, and the
fix-verification pass had to point that out, because the pre-flight's own verdict carried no
information. The target is now 100–1400, against the roughly 1,040 pages `TOC.md` plans.

**How to apply.** A gate that fails on something you have decided not to care about gets fixed
or retired the same day. A standing failure trains you to skip the output, and skipping the
output is worse than not having the gate — you keep the cost and lose the signal.

---

**30. The interview bank is the standard, and I read a range of it I remembered.** Chapter 19
owns bank questions 39, 40, 41 **and 42**. I wrote the chapter against 39–41, because 39–41 is
what my own working note said, and 42 — *"A multi-step pipeline fails half way. How do you
resume it?"* — was never read. `TOC.md` row 19 promised the same thing in its own words,
*"partial failure in a multi-step pipeline, and how to resume it"*, and the chapter shipped to
review answering neither. It had a section on one job over many items and nothing at all on a
pipeline of stages, which is a different problem with a different resume key.

`verify-coverage.py` passed it, because the Covers list's words appear in the chapter. The
completeness review found it in one grep of the bank.

**How to apply.** The chapter's question list is produced by grepping
`markdown/B-interview-bank.md` for the chapter number, every time, and the grep's result goes
into the record's `sources:` field. Never a remembered range, and never a range copied from a
plan. `BOOK-GUIDE.md` §15 says the bank is the standard rather than a summary; a standard you
quote from memory is not one.

---

**29. The transformation was the experiment, and the transformation silently did nothing.**
Checking chapter 19's claim about `f.flush()` meant running the resume program with the flush
and without it, under `kill -9`. I wrote a script that read the listing out of the markdown and
inserted `os.kill(os.getpid(), 9)` by string replacement. The replacement used the wrong
indentation, matched nothing, and the script carried on.

Both runs then printed `all done` and left ten lines on disk, and I was two seconds from
reading that as *the flush makes no difference* — which is the opposite of the truth. Done
properly: with the flush, ten lines; without it, **zero**.

This is entry 28's shape pointed at a different tool. There the tool reported the miss and I
did not read it; here the tool was mine and reported nothing at all.

**How to apply.** When a string replacement, a patch or an injected line *is* the experiment,
assert that it happened before you trust the result — `assert s.count(old) == 1`, or print the
changed lines and look at them. An experiment whose setup can fail silently produces a number
that means nothing, and it will be a plausible number.

---

**28. I read the tail of a tool's output and took a failure for a success.** `tools/patch.py`
applies edits one at a time and prints a line for each — `ok` or `MISS` — then a summary and a
non-zero exit if anything missed. Chapter 16's first round of fixes was twenty-one edits, so
the output was twenty-one lines plus the summary, and I piped it through `tail -4`.

The four lines I read were the four misses. I found them, fixed those four by hand, and moved
on satisfied. **One of the `MISS` lines was in the part I did not read** — the chapter 6
evidence-ladder sentence, which is the one finding in that round that was about the book's own
discipline rather than about a fact. It stayed in the chapter, and in the built `.tex`, through
a whole build and gate run, and was found only because the fix-verification pass was given the
list of changes and checked each one against the file.

**The tool did its job.** It printed the miss and it exited non-zero. The failure was entirely
in how I read it — and the reason I piped to `tail` is that twenty-one `ok` lines are noise,
which is the same economy that makes long gate output get skimmed (entry 18).

Two practices follow, and the second is the one that generalises:

1. **Never truncate the output of something that reports per-item success.** Grep it for the
   failure token instead — `| grep -E 'MISS|did not apply'` — which is short whether there are
   three edits or thirty.
2. **An exit status is a claim and a summary line is a claim.** `patch.py` exits non-zero and
   says "N edit(s) did not apply"; both were there and neither was read, because the eye went
   to the last few lines. This is entry 17's lesson in a smaller room: *a count from a tool is
   worthless unless you have checked what the tool said about whether it succeeded.*

*And what caught it is worth noting too.* The fix-verification pass is briefed with the list of
changes rather than with the chapter, which means it checks that each one landed rather than
reading for sense. That is the only reason an unapplied edit is visible at all — a reviewer
reading the chapter fresh would have found the original defect again and reported it as new.

**27. A gate that could never have caught the thing it was checking for, and failed everything
else instead.** `verify-render.py` carried a check for an unclosed display-maths fence. It
counted lines beginning ` ```{=latex} ` and failed the file on an odd total.

That can never work. A display fence opens with ` ```{=latex} ` and closes with a bare
` ``` `, so the closing line was never counted — which means the count is the number of
*display blocks in the chapter*, and the check was really asserting that every chapter has an
even number of them. Chapters 8, 11 and 12 happened to have 4, 2 and 0. Chapter 13 has one
display formula, and the gate failed it with "an odd number of ```{=latex} fences - one never
closes" on a file whose fences were all closed.

So the gate was simultaneously **blind** to the defect it was written for and **wrong** about
correct input — the two failure modes this ledger treats as opposites, in one check. It had
been in the suite since the beginning and had never fired, which is exactly what you would
expect of a check that only fires on an odd count of a thing that is usually even.

The fix is the obvious one and is what the loop already tracked: the scanner toggles a
`fence` flag on every ` ``` `, so if that flag is still set when the file ends, a fence never
closed. Proved by appending an unclosed ` ```text ` block and watching it fail, then removing
it and watching it pass.

**The practice.** `LEDGER-DEFECTS` entry 11 says a failing gate is a claim to be checked like
any other, and the first question is whether the gate or the text is wrong. This is the fourth
time the gate was wrong. Add to that question a second one: **when a gate has never fired, ask
what input would make it fire, and check that input is possible.** A check whose trigger
condition cannot occur is not protection; it is a line in a report that makes the suite look
longer than it is.

**26. A true fact, used to support a claim it does not support.** Chapter 12 explains why the
feed-forward block has an activation in it, and reached for the standard argument: a matrix
multiplication followed by another matrix multiplication is a single matrix multiplication, so
without a non-linear step the stack would collapse into one matrix.

The fact is true. `\(W_2(W_1 x) = (W_2 W_1)x\)`{=latex}, always. **The conclusion does not
follow**, because attention is not a matrix multiplication. Softmax is in the middle of it. A
stack with every feed-forward activation removed is still not one matrix, and the book had
already proved it two chapters earlier without noticing: double every input vector in chapter
11's worked example and the output does not double. It goes from
`\((0.216, 3.378, 1.879, 1.013)\)`{=latex} to `\((0.001, 7.996, 3.999, 2.000)\)`{=latex},
because the weights saturate.

The correct claim is narrower and still does the teaching work: without the activation **this
block's** two matrices are one matrix, and no condition can be expressed in it.

**Why this is its own class.** Every gate in this project reads for wrongness in the
*ingredients*. `verify-arithmetic.py` checks that printed equations hold — and this one held.
`verify-absolutes.py` lists absolutes — and "the activation is what stops the stack collapsing"
is a causal claim rather than an absolute, so it did not appear. `verify-boundary.py` passed it
because nothing in it is theory. **A valid fact wired to an invalid conclusion is invisible to
every check that reads the parts rather than the join**, and the only thing that found it was a
reviewer told to verify claims in Python rather than read them.

The practice that follows: **when a chapter uses a fact to justify a design, state what the
fact is a fact *about*, and check that the thing being justified is the same thing.** Here the
fact is about a sequence of matrix multiplications; the thing being justified was a stack that
is not one. Writing "this block's two matrices" instead of "the stack" is the whole fix, and it
is the kind of narrowing that looks like pedantry until somebody asks the follow-up question.

*And the version of this the same chapter also shipped:* "the one step in a model that is not a
matrix multiplication", of the activation. Chapter 11 prints a softmax and a division; chapter
9 prints another softmax. Same shape — a claim about *a model* made from a fact about *a
block*.

**25. A demonstration that works only under a condition the chapter never stated — and the
chapter handed it to the reader as an interview answer.** Chapter 11 proves that attention is
blind to word order by swapping two tokens and showing the output vector is unchanged. The
proof is real and the arithmetic is right. But it holds only when the swap leaves the **last**
position alone, because the last position supplies the query: change the token there and the
output moves for a reason that has nothing to do with order.

The chapter did not say so. Worse, it did two things that made the omission expensive. A Tip
told the reader this was "the answer to give" in an interview and that it is "impossible to
argue with". And a review question asked why attention cannot tell *"the dog bit the man"*
from *"the man bit the dog"* — which is a swap of the last token, so attention **can** tell
them apart. Run on the chapter's own matrices, the output goes from
`(0.216, 3.378, 1.879, 1.013)` to `(0.901, 2.180, 1.963, 1.679)`.

So the answer key contained a counter-example to the chapter's own claim, and the Tip armed
the reader to perform the demonstration in the one way that loses the argument.

**Two things make this its own class.**

*A condition that is satisfied by the worked example is invisible.* Every number on the page
was right, and position 5 was the readout throughout, so the constraint never had occasion to
announce itself. No gate can find a missing precondition: `verify-arithmetic.py` checks that
the printed sums hold, and they did. The completeness review found it only because it was told
to verify claims in Python rather than read them.

*A demonstration offered as an interview answer has to carry its own edge.* The book's purpose
is to make the reader able to say this out loud under questioning. A proof with an unstated
condition is worse than no proof there, because it will be produced confidently in exactly the
situation where somebody is looking for the gap. **When a chapter tells the reader "this is the
answer to give", state what would make it wrong in the same breath.**

*Related, and found in the same pass:* the chapter's own stronger claim — "neither can anything
built out of attention alone" — is false, because the causal mask is defined by position, so a
stack of masked attention is not blind to order even though the formula is. The narrow claim
(*this formula*) is true; the general one is not, and the counter-example was two sections away
in the same chapter. That is entry 5 again, and the rule stands: an absolute about everything
built from a thing is a claim about the whole book, not about the thing.

**24. I wrote a lab step explaining a bug in a program I had not run, and the bug was not
there.** Chapter 10's lab builds a byte-pair vocabulary and then hands the reader a program to
check their hand arithmetic against. Steps 8 and 9 of the first draft said the program had a
bug — that keying its dictionary by the tuple of symbols makes two words collide and
overwrite each other — then explained the collision in a paragraph, told the reader to count
the printed lines and find three instead of five, quoted the wrong output, and set a step
asking them to fix it.

**None of it was true.** All five words reduce to distinct symbol tuples at every step, so
nothing collides and the program prints five correct lines. I had reasoned about the data
structure, found a plausible failure, written it up with its symptom and its fix, and never
run the file. The chapter was two sections from a sentence telling the reader to have the
model write code rather than trust it to count.

What makes this its own entry rather than another instance of entry 22 is the *shape* of the
invention. Entry 22 was arithmetic invented while writing, after the verification step. This
was a **causal story** — a defect, its symptom, and its remedy — which is far more convincing
than a wrong number and has no gate behind it at all. `verify-arithmetic.py` cannot read it:
there is no equation. The completeness review might not have caught it either, since the
explanation is internally coherent and a reviewer who did not run the program would have no
reason to doubt it.

**The rule: a claim about what a program does is a claim to be run, not reasoned.** Every
output block in that lab is now copied from a real run, and the two invented steps were
replaced with two experiments that were actually performed — changing the tie-break, which
turns merge 5 from `er` into `runn`, and raising one word's frequency, which makes an
unrelated word cost four tokens instead of three. Both are better lab steps than the bug
story was, because both teach something true about the procedure rather than something true
about dictionaries.

*Second instance, chapter 13, by somebody who had written this entry.* The lab's program prints
a thousand sampled draws at three temperatures. I wrote the expected-output block from what the
probabilities implied — plausible counts, plausible probabilities — and only then ran it. **Four
of the twelve printed probabilities were wrong** (0.863 for 0.865, 0.456 for 0.455, and two
more) and **every one of the twelve counts was wrong**, because a seeded draw is not something
you can reason your way to. The prose around the block was wrong with it: it said the full stop
"comes up about a tenth of the time" where the real run gives 109 in a thousand, and "twice in a
thousand" where the real run gives 2 — right by luck.

What is worth recording is how it happened the second time. The program was *written* correctly,
the chapter's hand-worked steps were all verified in Python first, and the block was typed last,
in the flow of writing the lab, as if it were prose rather than a result. **Output is not prose.
It is a measurement, and it goes in the file only by being copied out of a terminal.** The rule
from the first instance stands and now has a procedure: write the program, run it, paste the
output, then write the sentences about the output — in that order, never the other.

*And the related near-miss in the same chapter.* The chapter's answer key converted 200 words
to "150 tokens" using the chapter's own rule of thumb upside down — it is 267. The arithmetic
gate passed it, correctly, because the number sits in prose rather than in a maths span.
**The gate reads equations; a crib sheet is not an equation.** Numbers written as English
prose in a Summary or an answer key are outside every gate this book has, and the review is
the only thing that reads them.

**23. The same chapter-length miscount, three times, under a warning against it.** A
chapter's printed length was read by subtracting folios by hand, and the pages counted into
it were the `PART II`, `PART III`, `PART IV` and `APPENDIX A` opener pages that sit
immediately after the last written chapter. Chapter 5 was recorded as 12 pp when it was 8.
Chapter 7 as 9 when it was 8 — the extra page was the *Inside the Model* sub-part opener.
Chapter 8 as **15 against a 14-page estimate**, which made it "the first chapter to exceed
its estimate"; it is 12, which is 86 per cent, and no chapter has exceeded one. That false
figure reached the record, `README.md`, `HANDOVER.md` and a report to the reader.

**What makes this worth an entry is where it happened.** `README.md` already carried the
rule, in bold, two lines under the table: *"Measure a chapter by where its own text ends,
not by where the next chapter starts."* It was written after the chapter 5 instance. The
chapter 8 figure was then entered into that same table, by somebody who had written the
warning, and the arithmetic was done the forbidden way anyway — because the folios are right
there and subtracting them takes five seconds, while opening the PDF and finding the next
opener does not.

So this is `LEDGER-DEFECTS` entry 14's lesson arriving a third time: **when the same defect
comes back, the answer is a gate, not more care.** `tools/pages.py` now reads the built PDF,
finds every chapter, part and appendix opener, ends each chapter one page before the next
opener, and prints the range, the count and the `TOC.md` estimate beside it. It is the only
figure that goes in a record from now on. Proved against the known-good cases (chapters 1,
2, 3 and 6, whose hand figures were right) and against the three wrong ones.

Two smaller things fell out of building it:

1. **A blank page would have broken it, and there are none.** The three blank pages in the
   book are all in the front and back matter, so no chapter is credited with a blank verso.
   If a future chapter ends on one, `pages.py` will count it — and that is the right
   answer for a page budget, since `BOOK-GUIDE.md` §11 counts numbered pages.
2. **The per-chapter percentages in `HANDOVER.md` §3 were wrong for two more chapters**
   (4 and 5) in the other direction, and nobody had noticed, because a figure that is
   roughly right attracts no attention. A measurement nobody can reproduce is not a
   measurement.

**22. "I verified every number" meant the numbers I wrote first.** Chapter 8 is the
mathematics chapter, and its whole argument is that you should substitute small numbers and
check by hand. Before writing a word of it I ran every figure through Python and said so, to
the reader and in this repository. The completeness review then found **six arithmetic
errors**, and a gate written afterwards found a seventh the reviewer had missed.

What actually happened is worth being precise about, because the failure is not carelessness:

- The numbers in the **body** went through Python before writing. Those were all correct.
- The **lab's** vectors were invented *while* writing, after the verification step, and never
  checked. `v = (1, 0, 4, 2)` has squares summing to **21**, and step 2 asserted that both lab
  vectors had length `\(\sqrt{14}\)`. Steps 3 and 4 then printed cosines that followed from
  the false premise. **Three expected results in a row, in a lab whose point is checking your
  own arithmetic.**
- Three more were a subtler class: `3.742 x 4.243 = 15.875` prints the product of the
  *unrounded* lengths, not of the two figures on the page. Same for `37.42 x 4.243 = 158.75`
  and `7.389 + 2.718 + 1.105 = 11.213`. Each is off in the last digit, each is invisible on a
  read-through, and each tells a reader doing exactly what the chapter asked that their own
  correct arithmetic disagrees with the book.

**The rule: verification is a property of the file, not of the session.** Numbers checked
before the writing began say nothing about numbers invented during it. So the check has to run
**against the finished file**, which means it has to be a gate — and `tools/verify-arithmetic.py`
now is one. It parses every printed equation in a `text` block or a maths span, evaluates the
chain, and compares at the precision the answer was printed to. It would have caught four of
the seven on its own, including the one the human reviewer missed
(`7.389 / 2.718 = 2.718`, which is 2.719 when you divide the rounded figures).

*And the gate itself shipped blind for twenty minutes.* Its first version pre-filtered each
block line against a character class that did not contain `=`, so **every equation in a text
block failed the filter and only maths spans were ever checked** — it printed `CLEAN` over 35
equations while ignoring the 29 that mattered. Proved by injecting a wrong total and watching
nothing happen. That is `LEDGER-DEFECTS` entry 18's exact shape, committed by somebody who had
written entry 18. **Prove a new gate by breaking something it should catch, every time, before
believing a single CLEAN it prints.**

**21. An acceptance test written after the thing it tests is not a test.** `TOC.md` said from
the start that Appendix B's hundred questions are written **in week one**, from the contents,
as the standard every chapter is then measured against. That did not happen. The bank was
written on 27 October, four days after Part I was finished, by somebody who had just read all
seven chapters closely.

The result passed — twelve of thirteen Part I questions answerable — and the pass is close to
worthless. A review pass checking the bank against the chapters found that **five of the
thirteen land near a review question the chapter already asks**, four of them almost
word for word:

| Bank | The chapter's own review question |
|---|---|
| 9 | ch 4: "Each step of your agent is right 90% of the time. Your task needs ten steps…" |
| 11 | ch 5: "A user reports a wrong answer. Name three different parts that could have caused it…" |
| 12 (before replacement) | ch 6: "A colleague says 'everyone re-orders their search results now.'…" |
| 13 | ch 6: "A provider's announcement says their new model is 30% better at coding…" |

None of those phrasings is in `TOC.md`. They came from the chapters. **A question
reverse-engineered from an answer tests nothing**, and a suite of them produces a confident
green that means only that the writer could remember what they wrote.

What was done: the bank's header now says plainly that questions 1 to 13 are the exception and
names the five, the worst lift was replaced with a question covering a `TOC.md` item nothing
tested (what to memorise against what to look up), and the one genuine finding was acted on —
question 4 asks for each part's cost, which chapter 2 is forbidden to teach, so its key became
*2–3* rather than widening chapter 2 past its ownership.

**The general rule, which cost Part I its clean pass: a test must be written before, or by
somebody who has not seen, the thing it tests.** Where neither is possible, the test's own
output has to carry the caveat, or a later reader will take a weak pass for a strong one. Two
places in this project already get this right and are worth copying: a chapter's
fix-verification pass is briefed with the findings and *not* the writer's reasoning, and every
gate here was proved by breaking something it should catch rather than by watching it pass.

**20. A reading lab cannot ship its data, and `BOOK-GUIDE.md` §9 still applies to it.**
§9 says **"Expected results must hold for every reader"** and **"Reproducible from the PDF
alone"**, and forbids a lab saying "your own documents" because *"an expected result that
depends on the reader's files holds for nobody"*. Those rules were written with the
retrieval and evaluation labs in mind. Chapters 5 and 6 are awareness chapters with no
code, and both labs were written as *archaeology*: go and find two engineering accounts, or
one recent article, and sort what is in them. That is the same defect wearing different
clothes — the reader's material instead of the reader's files — and it is how chapter 6's
lab came to predict its own result (*"roughly half their **P**s move"*, then *"expect to
move at least one"*).

Chapter 6's lab was rewritten to carry **an invented announcement inside the chapter** —
a fictional model, test, scores and prices — with nine claims and a key, and
finding-a-real-article demoted to an optional last step with no key and no promise. Two
things fell out of it that are worth having:

1. **A specimen you wrote has a right answer, so the lab can be checked.** The reader can
   be wrong and find out, which an "it is the habit that matters" lab never allows.
2. **An invented specimen cannot date.** Naming a real model or benchmark in a chapter
   *about* telling the durable from the dated would have put a dated detail in the one
   chapter that must not have one. The first draft of the rewrite used a real benchmark
   name; that was caught and replaced.

**Chapter 5's lab had the same defect and was fixed the same way**, on the reader's
instruction, after being flagged here and left alone for one turn — narrowing or widening
delivered work is their call, not mine. Its specimen is a twelve-paragraph invented
engineering account; the reader labels each paragraph with one of the four activities, *the
instructions*, or *none of these*, against a key.

Two things that specimen does which are worth copying into any lab of this shape:

1. **It refuses to demonstrate the chapter's own thesis.** The counts come out with *none
   of these* largest at four, two of the four activities at two and two at one, and the lab
   says outright that this supports no claim about which activity takes longest, because
   the author wrote the paragraphs and could have made any of them win. **The first draft
   of that sentence said "a three-way tie at two among the activities"**, which counted
   *the instructions* as an activity — the one thing the chapter forbids on its own line 33
   and in this ledger's own `LEDGER-TAUGHT` row 5. It also happened to make the spread look
   more neutral than it is, since the chapter's own thesis activity is at joint first. The
   honest version states the real counts and says they prove nothing anyway. **A specimen that
   quietly confirmed the chapter would have been worse than the lab it replaced** — it
   would have taught the reader to trust a rigged demonstration, in a chapter whose
   neighbour teaches the opposite.
2. **One step has no answer in the five-cause list.** Step 5 asks which of the chapter's
   five causes produced a wrong answer, and the key is *none of them*: the tool acted with
   the service's rights rather than the caller's. That is the chapter's hard-won "five
   **common** causes" earning its adjective, and it teaches the reader that a list of
   causes trusted too far is its own failure mode.

**19. The `written` stage keeps getting skipped, and a hand-written timestamp is a lie
waiting to fail.** Chapters 2, 3 and now 6: `python3 tools/chapter.py written <slug>` was
not run, so the record's `written:` field was filled in by hand afterwards. In chapters 5
and 6 the invented time was *later than the real `reviewed` stamp the driver had written*,
and `verify-record.py` failed on "stages out of order" both times — correctly.

The gate caught it, so nothing false reached a closed record. But note what the near-miss
was: **a fabricated timestamp that happened to be in the right order would have passed**,
and the record would then assert a time that never happened, in the one file whose whole
job is to be evidence. The hash does not protect this, because the hash covers the chapter,
not the record.

*Fourth instance, chapter 8, and it is now fixed mechanically.* The hand-written stamp was
09:40 when `begun` said 21:41 — nine hours of a day that had not happened. The gate caught the
ordering, as it had twice before, and the pattern was by then unmistakable: **I do not know
what time it is, so every timestamp I write by hand is a guess, and a guess that lands inside
the range passes silently.** Checking only for emptiness was never enough.

`tools/chapter.py reviewed` now **refuses a `written:` stamp that is before `begun:` or in the
future**, and says to run the driver and let the clock write it. Proved against the fabricated
value already in chapter 8's record, which it rejected with both timestamps quoted; the field
was then cleared and `chapter.py written` stamped the real time.

**Run the stage when you reach it.** The driver exists so the clock, not memory, writes the
time. Where a stage genuinely has to be reconstructed, say so in the field itself — chapters 5
and 6 carry *"approximate, reconstructed"* and the reason — so the record never claims a
precision it does not have.

**18. A gate can be structurally blind to a whole class of prose.** Chapter 6 used
*reranker* and *context window* in plain sentences. Both appear **zero** times in chapters
1 to 5, and chapter 6 neither bolded nor defined either: it leaned on the reader already
knowing field jargon the book had not given them. `verify-inputs.py` reported
`new-terms: 0` and was not lying — it read only **backticked** spans, and chapter 6
contains no backticks at all. The gate written to catch exactly this missed it because the
defect arrived in a form the gate could not see.

The fix was to add a second check that walks a curated jargon list and fails on any of
those terms used without being defined there and without appearing earlier. Two things
about building it are worth more than the gate itself:

1. **The first version cried wolf and would have been ignored.** It derived its vocabulary
   by splitting `TOC.md` on word boundaries. It caught the real defect — and flagged
   *combine*, *choice*, *minutes* and *pair*: **30 false positives on one chapter.** The
   second version used a hand-written list, which still flagged chapter 2's "a second model
   **judge** it acceptable", chapter 3's "approval given without real **attention**" and
   chapter 5's "a stack **trace**". Only the third version — jargon with no ordinary-English
   sense — is clean on all six chapters. **A gate that fires on correct input is worse than
   no gate** (rule 1), so a term that doubles as plain English is deliberately absent from
   the list, and this gate will never catch those. The completeness review is what catches
   them, and it is what caught these two.
2. **Proved both ways before wiring in** (rule 2): clean on chapters 1 to 6, and
   `bare-terms: 1 FAIL` on a chapter with one `reranker` appended. The suite's loop was
   proved the same way, not just the script.

*Second instance, same day, different gate.* `verify-absolutes.py` listed **none** of
chapter 7's negative absolutes. The chapter's four-parts table said **"Nothing here is a
lab"** — flatly false, since every chapter of Parts I to III carries one, chapter 7 included,
120 lines further down the same file. The gate's word list held `always|never|all|only|every|
any|none|must|cannot|…` and had no `nothing`, no `nobody`, no `almost`. **An absolute whose
counter-example sits in the same file is the exact thing this gate exists to surface**, and it
printed 38 hits without that one among them. The list now covers the negative forms.

Calibration again decided the shape of the fix: adding `no \w+` as well caught more but added
about 27 hits a chapter, nearly all `no idea`, `no longer`, `no code`. **A hint list too long
to read carefully is the same failure as a gate that cries wolf**, so it was dropped and only
the forms that have actually carried a defect here are listed. Counts rose from 38-83 to
47-99 per chapter, which is still a list a person reads.

**The general lesson.** `verify-inputs.py` was itself born from a defect — the French
book's chapter 38 ran a rule on two verbs the book had never printed. It was written to
stop that, and it stopped the backticked version of it. **When a gate passes a chapter and
the review then finds the very thing the gate exists to catch, the question is not whether
the gate is enabled but whether the defect can reach the page in a form the gate cannot
read.** Ask that of every gate here: `verify-render.py` reads Markdown, so it cannot see a
LaTeX macro; `verify-coverage.py` reads the `TOC.md` Covers list, so it cannot see a promise
made in a chapter's prose; `verify-absolutes.py` lists absolutes and judges none of them.

**17. I read "0 overfull" out of the log of a build that had died.** This is the worst
process failure in the project so far, and it is worth the length.

Chapter 5's two Key Terms opened the index's first `E` letter group and the build went
overfull by exactly `9.33658pt`. Over the next hour I "diagnosed" it, "fixed" it three
different ways, watched the count go to `0`, wrote the fix up in this ledger and in
`HANDOVER.md`, and **every one of those zeros was false**. My fix had used `\newif\ifti@…`
in a block that sits outside `\makeatletter`, so `@` was not a letter, so LaTeX died with
`Missing \begin{document}` on line 415 — and a log from a build that stopped at line 415
contains no overfull boxes at all. I was grepping `book.log` for `Overfull` and reading the
count without once checking the exit status or grepping for `^!`.

Everything I believed for that hour was wrong, including the diagnosis itself. The real
fault was not the leading `\addvspace`. It was **rigidity**: `book.cls`'s own `\indexspace`
is `10pt plus5pt minus3pt`, and `\indexletter` had replaced it with a rigid
`\addvspace{9pt}`. The index was about 9pt more than one page and had no flexibility to
absorb it. Restoring a `minus 3pt` shrink fixed it. The index paginates correctly on its
own — 120 injected entries give three index pages and 0 overfull — so nothing structural
was ever wrong.

**The rules this bought:**

1. **A count from a log is worthless unless the build that wrote it succeeded.** Never
   `grep -c Overfull book.log` by hand. Run `bash tools/build-probe.sh`, which prints
   `exit=`, `latex-errors=`, `overfull=` and `glyphs=` on one line and **refuses to report
   the counts at all** when the build did not succeed. `tools/check-all.sh` already checked
   `make`'s exit status; the hole was entirely in my manual checking, which is exactly the
   place a gate cannot reach.
2. **Every test run before the harness existed had to be thrown away and redone.** Three
   candidate fixes, a pagination test and the whole causal story — all void. Re-running them
   honestly took ten minutes and gave a different answer. **When you discover a measurement
   was broken, re-run every measurement that used it**, not just the last one.
3. **A fix that "works" without an explanation you can state is not a fix.** I could not
   have said why suppressing one 9pt space would fix a 9.33pt overflow. That gap should have
   stopped me, and instead the false `0` reassured me past it.
4. **`@` is not a letter outside `\makeatletter`.** The specific trap: `\newif\ifti@foo`
   fails silently-looking at the top of a run, far from where you are working.

*Third instance, 2026-10-27, and this one was predicted by the paragraph below.* Appendices B
and C were enabled while A (the cheat sheet) is still unwritten. `\appendix` letters by
**position**, not by filename, so the Interview Bank printed as "Appendix A" and the Glossary
as "Appendix B" — while `TOC.md`, `BOOK-GUIDE.md`, the glossary generator and every
cross-reference called them B and C. The reader would have met a book that disagreed with
itself about its own appendix letters. Fixed with `\setcounter{chapter}{1}` and a comment
saying to delete that line when `A-cheat-sheet.md` lands. **A missing FIRST item silently
renumbers everything after it**, which is the same shape as the index's leading `\addvspace`
above.

**And the thing that was true all along:** the apparatus was built against a four-chapter
book, and anything with a first-item or last-item special case — the index, the contents,
running heads, part pages — has not yet met the input that breaks it. When the build breaks
on a new chapter, **suspect the apparatus as readily as the chapter**, and prove which by
putting the old chapter back. That test (old chapter 5 → 0 overfull, on a build that
actually succeeded) is the one measurement from that hour that survived.

**16. A fix reaches the body and not the back matter — four times in three chapters.**
Chapter 1: a claim fixed in the body survived in the Review Answers. Chapter 2: the person
removed from the checks table survived in the Summary *and* in the Key Terms definition.
Chapter 3: the rewritten accountability argument did not reach the Pattern table or Review
Answer 4, and a corrected claim about model confidence survived in Review Answer 3. Every
single survivor was in a Summary, a Key Terms row, or an answer key — sections that get
written once and then read as settled, because they are a glossary or a crib rather than an
argument. **§14.2 already says to sweep them. The instruction is not the problem; doing it
is.** After applying any finding, grep the Summary, Key Terms, Review Questions and Review
Answers for the claim in every phrasing, before touching anything else.

**15. A batch of edits that aborts part-way writes nothing, and the edits it reported as
applied are lost.** Three times now a patch script has asserted its way through a list of
replacements and written the file only at the end, so one mismatched string discarded every
edit before it — while still printing `1 -> 0` for each, which reads exactly like success.
The third time, four findings were silently lost and only turned up when I rendered the
page and saw the old sentence still there. **`tools/patch.py` now applies one edit at a
time and writes after each**, reports misses without stopping, and exits non-zero if
anything missed. The general rule: *a tool that reports progress it has not committed is
worse than one that says nothing.*

*Second instance, chapter 4.* Writing per-edit fixed the losing; it does not stop the
edits **interacting**. A removal with `count: 2` was meant to delete one leftover sentence
and deleted two — because an earlier edit in the same batch had just inserted the second
copy. The Warning lost its conclusion entirely, and `patch.py` reported both as applied,
correctly. **Order the edits so no edit's target string can have been created by an earlier
one in the same batch**, and when a batch both inserts and removes the same text, do it in
two runs with a read in between.

**14. The gates read Markdown. The book is a PDF.** The outline was wrong three times in a
row — front matter missing from it, then sub-parts beside Part I instead of under it, then
chapters beside the sub-parts instead of under them — and the reader found all three. Every
gate passed each time, because every gate opened a `.md` file. **Anything that only exists
after typesetting is unchecked unless something opens the output**: the outline, the running
heads, the page breaks, the index, the cover. `verify-outline.py` now covers the first of
those. The general lesson is the one to keep: when the reader reports something twice, the
answer is a gate, not more care.

**13. The same false claim will come back in the next chapter that needs it.** "A rule is
free and it is **right** every time" was written in chapter 2, fixed there, and then
written again in chapter 3's check table as "Certainty, free, every time". Nobody copied
it; it is simply the sentence that comes to mind when describing a rule-based check, and
the true version — *the same verdict every time, which is not the same as the right one* —
is one word longer and less satisfying. **A corrected claim is not corrected book-wide; it
is corrected in one chapter.** When a fix lands on a claim the book will make again, write
the claim into `LEDGER-TAUGHT.md` in its corrected form, and grep for the wrong form in
every later chapter that touches the subject.

**11. A gate can encode a claim and be wrong the same way the writer would be.**
`verify-render.py` flagged every Review Questions block in chapter 1 as "items run
together into one paragraph". It was wrong: a real `1. ` marker is list syntax and makes
a tight `\begin{enumerate}`, which renders correctly. The defect it was ported for is a
**bold** paragraph marker (`**A1.**`), which is not list syntax and does collapse. I had
broadened the pattern when porting it. **Check a reported finding against the generated
`.tex` before treating it as a defect** — the same instruction the source project gives
for its own coverage gate, which has a known false-positive class of its own.

*Second instance, chapter 2.* `verify-voice.py` failed the chapter on the ordinary English
word **handover** — "a handover to a human" — because the pattern for build-document names
was compiled case-insensitively along with every other pattern. File names are
case-sensitive and now compile that way. **Two of the seven gates have now been wrong
before the chapter was**, both in their first week, and both in the same direction: a
pattern written for one shape matching a wider one. Expect the third.

*Third instance, the same day.* `verify-record.py` read its fields with `^name:\s*(.*)$`.
`\s` matches newlines, so an **empty** field swallowed the line break and returned the
next line's text: `written:` reported as `reviewed:`, and the gate announced "stages out
of order" on a record whose stages were simply not filled in yet. Fixed with
`[^\S\n]*`. **All three were the same mistake** — a character class wider than the thing
it was written for — and all three were found by the gate failing on correct input rather
than by passing bad input. The lesson is not "write better patterns". It is that **a
failing gate is a claim to be checked like any other**, and the first question is always
whether the gate or the text is wrong.

**12. A page budget is a guess until a chapter is built, and the words-per-page figure
does not transfer between books.** Chapter 1 came in at **8 printed pages against a
14-page budget**: 3,097 words of markdown, ~3,067 words printed across pages 8 to 15, so
about **380 words per printed page**. The plan assumed 240, inherited from a book dense
with tables, practice blocks and vocabulary lists. Prose runs far tighter than that.
**Do not pad a chapter to reach its budget, and do not revise 57 budgets off one data
point** — Part I is the most prose-heavy part of this book and the least representative.
Re-measure after a chapter with worked arithmetic (chapter 11) and after a lab
(chapter 40).

*Second data point, chapter 2:* 3,158 words, **11 printed pages against an 18-page
budget** — 61 per cent, where chapter 1 was 71 per cent. Two chapters is still not enough
to revise 55 budgets, and Part I remains the least representative part of the book. **That trigger was cancelled on 22 October 2026**, by the
reader: budgets are a rough estimate, never a limit, and content is not cut to fit one or
padded to reach one. See `BOOK-GUIDE.md` §11.

What survives of this entry is the part that is still true and still useful: **a large gap
is a prompt to re-read the Covers list**, because in both chapters it pointed at something
genuinely thin. It is not a reason to add words, and it is not a reason to re-plan.
