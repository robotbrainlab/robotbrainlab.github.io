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

**Run the stage when you reach it.** The driver exists so the clock, not memory, writes the
time. Where a stage genuinely has to be reconstructed, say so in the field itself — both
chapter 5's and chapter 6's now carry *"approximate, reconstructed"* and the reason — so
the record never claims a precision it does not have.

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
