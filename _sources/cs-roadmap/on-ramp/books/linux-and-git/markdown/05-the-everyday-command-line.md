# The Everyday Command Line

This chapter gives you the handful of tools you'll use every day: finding files, reading them, searching inside them, reshaping text, and pulling facts out of JSON. You'll then join them into pipelines that answer real questions in one line. Last, you'll meet environment variables, the settings every program inherits from the shell.

*The problem.* I can move around, but finding a file or reading a log still feels like guessing.

*The question.* How do I find what I need, in files and inside them, without opening everything?

The examples use two sample files from `labs/ch05/` in the book's lab files (see the preface): `app.log`, a web server's log, and `team.json`. From the folder that holds `labs/`, copy them into your sandbox:

```bash
mkdir -p ~/sandbox/logs
cp labs/ch05/app.log ~/sandbox/logs/
cp labs/ch05/team.json ~/sandbox/
```

Then `cd ~/sandbox`.

## Finding Files

`find` walks down a folder tree and prints every path that matches your conditions. Its shape is `find <where> <conditions>`:

`find . -name '*.txt'` lists every `.txt` file under the current folder. The `*` is a wildcard meaning "any characters", so `'*.txt'` matches every name ending in `.txt`. Keep the quotes; they stop the shell from expanding the `*` itself before `find` sees it. Other useful conditions:

| Condition | Matches |
|---|---|
| `-name '*.py'` | Names matching a pattern |
| `-type f` / `-type d` | Only files / only directories |
| `-mtime -1` | Modified in the last day |
| `-size +10M` | Bigger than 10 megabytes |

To see how much space something takes, use `du -sh` ("disk usage, summary, human units"): `du -sh logs` prints `8.0K    logs`.

## Viewing Files

`cat` prints a whole file, which is fine for short files and useless for long ones. For those:

- `head -n 3 file` shows the first three lines; `tail -n 3 file` the last three.
- `wc -l file` counts lines.
- `less file` opens a pager: a viewer that shows one screen at a time. Space goes forward, `b` goes back, `/word` searches, `q` quits.
- `tail -f file` keeps the file open and prints new lines as they're added. It's how you watch a running program's log. Press Ctrl-C to stop.

```bash
wc -l logs/app.log
head -n 3 logs/app.log
```

```text
60 logs/app.log
2026-09-25 09:14:35 INFO POST /cart 200 user=cy
2026-09-25 09:15:45 INFO POST /login 200 user=ada
2026-09-25 09:15:54 INFO GET /books 200 user=dee
```

Each line has a date, a time, a level (`INFO`, `WARN`, or `ERROR`), a request method and path, a status code, and a user.

## Searching Inside Files with grep

`grep` prints the lines that contain a pattern. It's the tool you'll reach for most:

```bash
grep ERROR logs/app.log
```

```text
2026-09-25 09:17:50 ERROR POST /cart 500 user=ada
2026-09-25 09:21:27 ERROR POST /cart 500 user=ben
2026-09-25 09:28:01 ERROR GET /books/42 500 user=ben
…
2026-09-25 09:43:30 ERROR POST /cart 500 user=cy
```

A few options cover most needs:

| Option | Effect |
|---|---|
| `-i` | Ignore upper and lower case |
| `-n` | Show line numbers |
| `-c` | Count matching lines instead of printing them |
| `-v` | Invert: lines that don't match |
| `-r` | Search every file under a folder |
| `-E` | Use extended patterns (see below) |

```bash
grep -c ERROR logs/app.log
grep -r milk .
```

```text
8
./todo.txt:buy milk
```

The pattern is a **regular expression**: a small language for describing text. Plain words match themselves, and a few characters have special meanings:

| Pattern | Matches |
|---|---|
| `.` | Any single character |
| `*` | Zero or more of the thing before it |
| `^` and `$` | The start and the end of a line |
| `[0-9]` | One character from a range |

With `-E`, a vertical bar means "or": `grep -E 'WARN|ERROR'` finds both kinds of line. And `grep -E '^2026-09-25 09:4'` finds lines that *start* with times from 09:40 to 09:49. Put patterns in single quotes so the shell leaves them alone.

## Changing Text with sed

`sed` (stream editor) edits text as it flows past. Its most common use is find and replace, written `s/old/new/`:

```bash
sed 's/user=/by /' logs/app.log | head -2
```

```text
2026-09-25 09:14:35 INFO POST /cart 200 by cy
2026-09-25 09:15:45 INFO POST /login 200 by ada
```

This doesn't change the file; it prints a changed copy. Add `g` at the end (`s/a/b/g`) to replace every match on a line, not just the first.

To edit a file in place, add `-i`. Here the GNU and BSD versions differ: on Linux write `sed -i 's/milk/bread/' todo.txt`; on macOS write `sed -i '' 's/milk/bread/' todo.txt`. The macOS version fails with a confusing error if you leave out the `''`.

> **Warning:** `sed -i` overwrites the file with no undo. Run the command without `-i` first, check the output, then add `-i`.

## Sorting and Counting

Three more tools turn lists into answers. `cut` picks columns: `cut -d' ' -f5` means "split on spaces and keep field 5". `sort` puts lines in order (`-n` for numbers, `-r` to reverse). `uniq -c` collapses repeated neighbouring lines into one and counts them, which is why you always `sort` first.

## Building a Pipeline

Now join them. Which pages are requested most? Build the answer one stage at a time, checking the output as you go. First, keep only the path column:

```bash
cut -d' ' -f5 logs/app.log | head -3
```

```text
/cart
/login
/books
```

Sort the paths so duplicates sit together, count them, then sort by the count, largest first, and keep the top three:

```bash
cut -d' ' -f5 logs/app.log | sort | uniq -c | sort -rn | head -3
```

```text
     15 /cart
     13 /login
     12 /books
```

The same pattern answers "who hit the most errors?":

```bash
grep ERROR logs/app.log | cut -d' ' -f7 | sort | uniq -c | sort -rn
```

```text
      4 user=ben
      2 user=cy
      2 user=ada
```

That's the Unix idea from Chapter 1 at work: five small tools, one question answered, no program written.

> **Tip:** Build pipelines one stage at a time, adding `| head` to peek at each step. When the output looks right, add the next stage.

## JSON with jq

Many tools and web APIs speak **JSON**, a text format of objects in `{}` and lists in `[]`, like Python dictionaries and lists. `grep` sees JSON only as lines; `jq` understands its structure:

```bash
jq -r '.[].name' team.json
jq '.[] | select(.active) | .email' team.json
```

```text
Ada
Ben
Cy
Dee
"ada@example.com"
"cy@example.com"
"dee@example.com"
```

`.[]` means "each item in the list" and `.name` picks a field; `-r` prints plain text without quotes. `select(.active)` keeps only items whose `active` is true. `jq . file.json` pretty-prints any JSON file, which alone makes it worth installing.

## Environment Variables

Every program starts with a set of named settings called **environment variables**. The shell has some already: `HOME` is your home folder, `USER` your name, and `PATH` the folder list from Chapter 2. Read one with `$`: `echo $HOME` prints `/home/ada`.

You can create your own, but by default a variable stays inside the current shell. `export` marks it to be passed down to every program the shell starts:

```bash
GREETING=hello
bash -c 'echo "child sees: $GREETING"'
export GREETING
bash -c 'echo "child sees: $GREETING"'
```

```text
child sees: 
child sees: hello
```

Python reads them through `os.environ`. This is how programs get settings without hard-coding them: a database address, a debug switch, an API key.

Settings typed at the prompt vanish when you close the terminal. To keep them, put the `export` lines in your shell's startup file: `~/.bashrc` for bash, `~/.zshrc` for zsh. The shell runs it every time it starts.

## Lab: Interrogate a Log

Copy the two sample files into `~/sandbox` as shown at the start of this chapter, then `cd ~/sandbox`.

1. Count the lines: `wc -l logs/app.log`. **Expected:** `60 logs/app.log`.
2. Count the warnings: `grep -c WARN logs/app.log`. **Expected:** `6`.
3. Show only problems: `grep -v INFO logs/app.log | wc -l`. **Expected:** `14` (six warnings and eight errors).
4. Find where Cy's requests start failing: `grep -n 'ERROR.*user=cy' logs/app.log`. **Expected:** two lines, numbered `40` and `44`.
5. Which path causes the errors? `grep ERROR logs/app.log | cut -d' ' -f5 | sort | uniq -c`. **Expected:** `1 /books/42` and `7 /cart`.
6. Find every JSON file under your sandbox: `find ~/sandbox -name '*.json'`. **Expected:** the path to `team.json`.
7. Count the active team members: `jq '[.[] | select(.active)] | length' team.json`. **Expected:** `3`.
8. Export a variable and read it from Python: `export COLOUR=blue`, then `python3 -c 'import os; print(os.environ["COLOUR"])'`. **Expected:** `blue`.

## Summary, Key Terms, and Review Questions

### Summary

- `find` locates files by name, type, age, or size; `du -sh` shows how big they are.
- `head`, `tail`, `less`, and `wc` let you look at files without opening an editor. `tail -f` follows a growing log.
- `grep` finds lines matching a regular expression; `sed` rewrites text as it flows; `cut`, `sort`, and `uniq -c` turn lines into counts.
- Pipelines join these tools. Build them one stage at a time.
- `jq` reads and filters JSON.
- Environment variables pass settings to programs. `export` passes them to children; startup files make them permanent.

### Key Terms

| Term | Meaning |
|---|---|
| Regular expression | A pattern language for matching text |
| JSON | A text format of objects and lists, used by many tools and APIs |
| Environment variable | A named setting a program inherits when it starts |

### Review Questions

1. Write a `find` command that lists all Python files under your home folder.
2. What's the difference between `grep -c ERROR` and `grep ERROR | wc -l`?
3. Why must you `sort` before `uniq -c`?
4. Why can't your Python program see a variable you set at the prompt, and what fixes it?

> **You understand this when** you can answer "who caused the most errors?" with a pipeline.
