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

*(empty — add the first entry the first time something gets past every gate)*
