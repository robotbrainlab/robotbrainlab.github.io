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
