# Records

One record per chapter, named exactly like the chapter: `records/01-getting-python.md`
for `markdown/01-getting-python.md`.

**You do not write one by hand.** `python3 tools/chapter.py begin NN-slug` copies
`tools/record-template.md` here and stamps it. The rest of the loop fills it in:

```bash
python3 tools/chapter.py begin    NN-slug     # BEFORE the chapter file exists
python3 tools/chapter.py written  NN-slug
python3 tools/chapter.py reviewed NN-slug     # writes the fingerprint last
```

`tools/verify-record.py` fails when a record is incomplete, out of order, stale, or when
its `absolutes:` number disagrees with what `tools/verify-absolutes.py` counts.

**Empty.** No chapter is written.
