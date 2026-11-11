# Command Cheat Sheet

The commands used in this book, in one place.

## Files and Bytes

| Command | What it does |
|---|---|
| `wc -l file` | Count newline characters (lines) |
| `wc -w file` | Count words (runs of non-whitespace) |
| `wc -c file` | Count bytes |
| `xxd file` | Show the bytes in hexadecimal, with their characters |
| `file notes.txt` | Guess what kind of data a file holds (`ASCII text`, `UTF-8 Unicode text`, …) |

## Python

| Snippet | What it does |
|---|---|
| `Path("f.txt").read_text(encoding="utf-8")` | Read and decode a whole file |
| `Counter(words).most_common(3)` | The three most frequent items |
| `python3 -c "…"` | Run a one-line program |
