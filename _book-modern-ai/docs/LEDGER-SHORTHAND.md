# What the field actually calls it

The book teaches a concept under a clear name. Practitioners, papers and interviewers often use a
different one — an abbreviation, a nickname, or a term of art. **Both have to be in the book**, or
a reader searching for the word they will actually hear finds nothing.

## The rule

**The chapter that *owns* a concept names the field's word for it once**, where it explains the
clear name: one sentence in the body, and the shorthand carried in that chapter's Key Terms row.

Every later chapter may then use the shorthand, and **must not re-explain it**.

**A chapter must never use a shorthand earlier than the chapter that names it.** The inputs gate
checks this **for shorthand that has a Key Terms row**, by reading those tables.

**It cannot check a `body`-only shorthand**, because there is no row for it to read. Those are
caught by the completeness review instead, which is given this file's rows for the chapters above
the one under review. **So a `body` entry costs a machine check and gains a human one** — use it
only where the two reasons below genuinely apply.

## Where a shorthand does not get a Key Terms row

Some shorthand is only a spoken name for a practice, or names something wider than the chapter
builds. Name it in the body and leave it out of the Key Terms table. Mark it **body** below.

## Why this file exists separately

A glossary is generated from the Key Terms tables and is therefore organised by the book's own
vocabulary. This file is organised by **the reader's** vocabulary — the words they will meet
outside the book — and it is the only place that mapping is visible as a whole.

**At a research frontier this file has a harder job than usual:** the same technique often carries
three names across three communities, and a reader who knows one cannot find the other two. Where
that happens, list every name and say which community uses which.

## The columns

| Column | What goes in it |
|---|---|
| `Shorthand` | Every word the field uses, comma-separated |
| `What the book calls it` | The clear name |
| `Home` | The chapter that owns the concept and names the shorthand |
| `State` | `Named. Key Terms row added` · `Named, body` · `Not yet named` |
| `Community` | Where each name is used, when they differ |

## The rows

| Shorthand | What the book calls it | Home | State | Community |
|---|---|---|---|---|
| — | *No chapters written yet.* | — | — | — |
