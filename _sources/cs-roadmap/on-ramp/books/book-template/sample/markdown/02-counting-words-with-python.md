# Counting Words with Python

Now that you know a text file is bytes plus an encoding, you can read one correctly from Python. This chapter builds a ten-line program that counts words, runs it from the shell, and shows what its errors mean.

*The problem.* I want to know which words appear most in a file, and counting by hand is hopeless.

*The question.* How do I read a text file correctly from Python and count what's in it?

## Reading a File the Right Way

Python's **`pathlib`** module represents a file path as an object. Its `read_text()` method reads the bytes and decodes them in one step. Always pass the encoding; the default depends on the operating system.

```python
"""Count how often each word appears in a text file."""
import sys
from collections import Counter
from pathlib import Path


def count_words(path: Path) -> Counter:
    text = path.read_text(encoding="utf-8")
    return Counter(text.lower().split())  # split() breaks on any whitespace


if __name__ == "__main__":
    counts = count_words(Path(sys.argv[1]))
    for word, n in counts.most_common(3):
        print(f"{word:<6} {n}")
```

A [**`Counter`**]{idx="Counter (collections)"} is a dictionary that counts things: give it a list, and it maps each item to how many times it appeared. `most_common(3)` returns the three largest counts.

## Running It

Save the program as `count_words.py` next to `notes.txt`, then run:

```bash
python3 count_words.py notes.txt
```

```
the    3
cat    1
sat    1
```

For a quick total, a one-liner is enough. It's long, so the book wraps it; paste it as one line:

```bash
python3 -c "from pathlib import Path; print(sum(len(line.split()) for line in Path('notes.txt').read_text(encoding='utf-8').splitlines()))"
```

```
8
```

> **Tip:** `python3 -c` runs a string as a program. It's handy for checks like this one, but anything you'll run twice belongs in a file.

## When It Fails

If the file doesn't exist, Python stops with a **traceback**: the chain of calls that led to the error, with the error itself on the last line. Read tracebacks from the bottom up.

```
FileNotFoundError: [Errno 2] No such file or directory: 'missing.txt'
```

> **Warning:** Don't hide this error with a bare `except:`. A program that silently prints nothing when its input is missing looks like it worked, and its empty output can overwrite a good report.

## Lab: Count the Words in Your Own File

Pick any text file you have, or create one with three lines of your own. Then:

1. Run `wc -w yourfile.txt` and note the number of words.
2. Run `python3 count_words.py yourfile.txt` and compare the top three words with what you expect.
3. Add a line with capital letters (`The Cat`) and run it again.

**Expected result:** the counts for `the` and `cat` go up by one each, because the program lowercases the text before counting. `wc -w` and the sum of all counts from the program should agree.

## Summary, Key Terms, and Review Questions

### Summary

- `Path.read_text(encoding="utf-8")` reads and decodes a file in one step.
- A **`Counter`** counts items; `most_common(n)` gives the top *n*.
- A **traceback** reads bottom-up: the last line is the error.

### Key Terms

| Term | Meaning |
|---|---|
| pathlib | The standard-library module for file paths |
| Counter | A dictionary subclass that counts items |
| Traceback | The report Python prints when an error stops a program |

### Review Questions

1. Why should you pass `encoding="utf-8"` to `read_text()`?
2. Why does the program call `lower()` before `split()`?
3. Which line of a traceback do you read first?

> **You understand this when** you can predict the output of `count_words.py` for a file you wrote yourself, before you run it.
