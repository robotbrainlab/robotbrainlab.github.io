# What the reader already knows

One row per finished chapter, written when the chapter closes. **Read this before writing any
chapter**, and grep it for `Do not` before writing the opening paragraph.

## Why it exists

A chapter can be internally perfect and wrong about where it sits: it can re-explain something the
reader already has, assume something the reader does not have yet, or claim something false about
what came before. **Only the middle one has a gate** — gate 8 catches a term used before the
chapter that owns it, and only where that term has a Key Terms row. **Nothing machine-checks the
other two**, and this file is their only defence.

## How to use it

**Before writing a chapter:**

1. Read every row above the chapter's position.
2. Read **every** `Do not` row, wherever it sits. Those are the traps.
3. Check the chapter's opening paragraph claims nothing false about what came before.

**When a chapter closes:** add its row. A chapter is not done until its row exists.

## The columns

| Column | What goes in it |
|---|---|
| `Ch` | Chapter number |
| `Question` | The chapter's durable question, copied from the chapter |
| `Taught` | What the reader can now do that they could not before. Capabilities, not topics |
| `Terms introduced` | Every term this chapter bolded and put in its Key Terms table |
| `Shorthand named` | Any field shorthand this chapter named for the first time. Also goes in `LEDGER-SHORTHAND.md` |
| `Do not` | What a later chapter must not do — re-explain, re-assume, or contradict. **Write this as an instruction, not as a description** |
| `Claims` | The `CLAIMS.tsv` ids this chapter rests on, so an overturned claim finds its chapters |

## The rows

| Ch | Question | Taught | Terms introduced | Shorthand named | Do not | Claims |
|---|---|---|---|---|---|---|
| — | — | *No chapters written yet.* | — | — | — | — |

## Writing a good `Do not` row

A description is useless; an instruction is not. Compare:

| Useless | Useful |
|---|---|
| "This chapter covers how the thing is measured" | "Do not re-define the metric. Chapter N owns it. Refer to it and move on" |
| "Introduces the trade-off" | "Do not re-derive the trade-off. Do not state it more strongly than chapter N does — it holds only under the condition named there" |

The second kind is what stops the defect. The first kind is a table of contents.
